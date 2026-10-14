#!/usr/bin/env python3
"""sweap wire sampler: turn session-level usage aggregates into a per-call ledger.

The store updates session_model_usage counters in place after every API call.
Snapshot it on a timer; the DIFF between consecutive snapshots is exactly what
the calls in that window consumed (uncached in / cache-read / cache-write /
out). Zero gateway changes, zero traffic interception, read-only on the store.

Output: ~/.sweap/wire_ledger.jsonl, one line per window:
  {"ts":..., "gap_s":..., "session":..., "model":..., "provider":...,
   "d_calls":N, "d_input":N, "d_cache_read":N, "d_cache_write":N, "d_output":N,
   "merged":bool}
merged=true means >1 call landed inside the window (their usages are summed);
gap_s flags sleep/compression gaps. State: ~/.sweap/wire_state.json.

Silent on ticks with no new calls (watchdog pattern: empty stdout = quiet).
"""
import sqlite3, os, json, sys, time

HOME = os.path.expanduser("~")
DB = os.path.join(HOME, ".hermes", "state.db")
STATE = os.path.join(HOME, ".sweap", "wire_state.json")
LEDGER = os.path.join(HOME, ".sweap", "wire_ledger.jsonl")

def snapshot():
    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    rows = con.execute("""SELECT session_id, model, COALESCE(billing_provider,''),
        api_call_count, input_tokens, cache_read_tokens, cache_write_tokens,
        output_tokens FROM session_model_usage""").fetchall()
    con.close()
    return {(r[0], r[1], r[2]): (r[3] or 0, r[4] or 0, r[5] or 0, r[6] or 0, r[7] or 0)
            for r in rows}

def main():
    if not os.path.exists(DB):
        return  # store absent: silent
    now = time.time()
    snap = snapshot()
    prev, t_prev = {}, None
    if os.path.exists(STATE):
        try:
            d = json.load(open(STATE))
            prev = {tuple(k.split("|", 2)): v for k, v in d["snap"].items()}
            t_prev = d["ts"]
        except Exception:
            prev, t_prev = {}, None
    if t_prev is None:
        json.dump({"ts": now, "snap": {"|".join(k): v for k, v in snap.items()}},
                  open(STATE, "w"))
        return  # baseline tick: silent
    gap_s = round(now - t_prev)
    lines = []
    for k, v in snap.items():
        p = prev.get(k)
        if p is None:
            continue  # new session: catch next tick (need a prior to diff)
        d = tuple(b - a for a, b in zip(p, v))
        if d[0] <= 0:
            continue  # no new calls
        dc, di, dcr, dcw, do = d
        lines.append(json.dumps(dict(
            ts=round(now), gap_s=gap_s, session=k[0], model=k[1],
            provider=k[2], d_calls=dc, d_input=di, d_cache_read=dcr,
            d_cache_write=dcw, d_output=do, merged=(dc > 1))))
    with open(LEDGER, "a") as f:
        for l in lines:
            f.write(l + "\n")
    json.dump({"ts": now, "snap": {"|".join(k): v for k, v in snap.items()}},
              open(STATE, "w"))
    # silent unless something looks structurally wrong (watchdog)
    if len(lines) == 0 and gap_s > 3600:
        print(f"sampler: no calls recorded for {gap_s}s; check store/gateway")
    if len(lines) > 200:
        print(f"sampler: burst window ({len(lines)} sessions advanced in {gap_s}s); ledger may be coarse")

if __name__ == "__main__":
    main()
