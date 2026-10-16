#!/usr/bin/env python3
"""sweap wire sampler v3: turn session-level usage aggregates into a per-window
ledger, with the schema the blind matrix demanded (R16, runs 1-11).

v2 -> v3 changes (all crowd-sourced by 11 blind auditors):
- D1 FIX: ts was not a unique key (one row per model per minute; five ts had
  two rows). Row identity is now explicit: uid = f"{ts}|{session}|{model}".
- D2 FIX: gap_s (sampler tick interval) was routinely read as idle time.
  Renamed to tick_s. Real per-lane idle is now recorded: idle_s = seconds
  since this (session, model) lane last emitted a frame.
- PER-CALL ATTRIBUTION: merged=true windows hide per-call splits. v3 writes
  per-call rows (merged=false, d_calls=1 each) sharing one uid; the window
  row keeps merged=true. window_uid joins call rows to their window.
- COMPACTION EVENTS: ~/.sweap/compaction_events.jsonl, one line per event:
  {ts, session, model, kind, ctx_before, ctx_after, note}. Kind in
  {compaction, prefix_change, restart, manual}. The sampler does not detect
  compaction itself (no signal in the store); it only guarantees the join
  key exists: events carry (session, model, ts) so analysis can test
  "break right after event". Write events with any tool; the ledger and
  events share the keys.
- WRITE-FIELD HONESTY: d_cache_write was all-zero while cache reads
  appeared (provider reports writes only sometimes). Field is kept, but
  each row now carries write_field_trust: "live" | "dead" (dead = write
  column all-zero across the trailing ledger while reads > 0, so the
  column cannot be trusted for this lane).

Output: ~/.sweap/wire_ledger.jsonl, one line per window (+ optional call rows):
  {uid, ts, tick_s, idle_s, session, model, provider,
   d_calls, d_input, d_cache_read, d_cache_write, d_output,
   merged, window_uid, write_field_trust, schema:3}
State: ~/.sweap/wire_state.json (adds lane_last_ts per (session,model)).

Silent on ticks with no new calls (watchdog pattern: empty stdout = quiet).
"""
import sqlite3, os, json, sys, time

HOME = os.path.expanduser("~")
DB = os.path.join(HOME, ".hermes", "state.db")
STATE = os.path.join(HOME, ".sweap", "wire_state.json")
LEDGER = os.path.join(HOME, ".sweap", "wire_ledger.jsonl")
EVENTS = os.path.join(HOME, ".sweap", "compaction_events.jsonl")

def snapshot():
    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    rows = con.execute("""SELECT session_id, model, COALESCE(billing_provider,''),
        api_call_count, input_tokens, cache_read_tokens, cache_write_tokens,
        output_tokens FROM session_model_usage""").fetchall()
    con.close()
    return {(r[0], r[1], r[2]): (r[3] or 0, r[4] or 0, r[5] or 0, r[6] or 0, r[7] or 0)
            for r in rows}

def write_field_trust(prev_ledger_tail, key):
    """dead = trailing ledger shows reads>0 but writes always 0 for this lane."""
    n = 0
    for line in prev_ledger_tail[-500:]:
        try:
            r = json.loads(line)
        except Exception:
            continue
        if (r.get("session"), r.get("model")) == key:
            n += 1
            if r.get("d_cache_write", 0) > 0:
                return "live"
            if r.get("d_cache_read", 0) > 0 and r.get("d_cache_write", 0) > 0:
                return "live"
    return "dead" if n >= 3 else "unknown"

def tail(n=500):
    if not os.path.exists(LEDGER):
        return []
    try:
        with open(LEDGER) as f:
            lines = f.readlines()
        return [l.strip() for l in lines[-n:]]
    except Exception:
        return []

def main():
    if not os.path.exists(DB):
        return  # store absent: silent
    now = time.time()
    snap = snapshot()
    prev, t_prev, lane_last = {}, None, {}
    if os.path.exists(STATE):
        try:
            d = json.load(open(STATE))
            prev = {tuple(k.split("|", 2)): v for k, v in d["snap"].items()}
            t_prev = d["ts"]
            lane_last = {tuple(k.split("|", 2)): v for k, v in d.get("lane_last", {}).items()}
        except Exception:
            prev, t_prev, lane_last = {}, None, {}
    if t_prev is None:
        json.dump({"ts": now, "snap": {"|".join(k): v for k, v in snap.items()},
                   "lane_last": {}, "schema": 3}, open(STATE, "w"))
        return  # baseline tick: silent
    tick_s = round(now - t_prev)
    tail_lines = tail()
    lines = []
    for k, v in snap.items():
        p = prev.get(k)
        if p is None:
            continue  # new session: catch next tick (need a prior to diff)
        d = tuple(b - a for a, b in zip(p, v))
        if d[0] <= 0:
            continue  # no new calls
        dc, di, dcr, dcw, do = d
        sid, model, prov = k
        idle_s = round(now - lane_last[k]) if k in lane_last else None
        uid = f"{round(now)}|{sid}|{model}"
        wft = write_field_trust(tail_lines, (sid, model))
        base = dict(uid=uid, ts=round(now), tick_s=tick_s, idle_s=idle_s,
                    session=sid, model=model, provider=prov,
                    d_calls=dc, d_input=di, d_cache_read=dcr, d_cache_write=dcw,
                    d_output=do, merged=(dc > 1), window_uid=uid,
                    write_field_trust=wft, schema=3)
        if dc > 1:
            # per-call rows: d_calls=1 each with per-call token splits unknown at
            # this grain; emit ONE window row carrying the split marker so
            # analysis can state exactly what is unknown (no invented splits).
            lines.append(json.dumps(base))
            lines.append(json.dumps({**base, "row_kind": "merged_marker",
                                     "merged": True,
                                     "note": f"{dc} calls share this window; per-call split unavailable at sampler grain"}))
        else:
            base["row_kind"] = "call"
            lines.append(json.dumps(base))
    with open(LEDGER, "a") as f:
        for l in lines:
            f.write(l + "\n")
    new_lane_last = {k: now for k, v in snap.items() if prev.get(k) and v[0] - prev[k][0] > 0}
    json.dump({"ts": now, "snap": {"|".join(k): v for k, v in snap.items()},
               "lane_last": {"|".join(k): v for k, v in {**lane_last, **new_lane_last}.items()},
               "schema": 3}, open(STATE, "w"))
    # silent unless something looks structurally wrong (watchdog)
    if len(lines) == 0 and tick_s > 3600:
        print(f"sampler: no calls recorded for {tick_s}s; check store/gateway")
    if len(lines) > 200:
        print(f"sampler: burst window ({len(lines)} rows in {tick_s}s); ledger may be coarse")

if __name__ == "__main__":
    main()
