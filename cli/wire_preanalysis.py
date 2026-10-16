#!/usr/bin/env python3
"""Four-arm pre-analysis: turn the wire ledger into the cache-break baseline.

Run manually around 2026-10-29 (two weeks after start). Read-only on the
ledger; prints the measured numbers the four-arm design needs:
  - hit-rate distribution per window (the cache-break sensor)
  - uncached-input per call (the break tax base)
  - merged-window share (resolution honesty)
  - per-model split
Outputs nothing else. No projections: only what the ledger actually recorded.
"""
import json, os, sys
from collections import defaultdict

LEDGER = os.path.expanduser("~/.sweap/wire_ledger.jsonl")

def load():
    frames = []
    with open(LEDGER) as f:
        for line in f:
            try:
                frames.append(json.loads(line))
            except Exception:
                pass
    return frames

def row_key(f):
    """D1 (R16 run 4): ts alone is NOT unique - one row per (session, model)
    per tick. Any per-ts join must use (ts, session, model); v2 rows without
    uid fall back to that triple. Also drops merged_marker helper rows."""
    return (f.get("ts"), f.get("session"), f.get("model"))

def analysis_rows(frames):
    """Only real measurement rows (v3 merged_marker rows are annotations)."""
    return [f for f in frames if f.get("row_kind") != "merged_marker"]

def idle_s(f):
    """D2 (R16 run 8): tick_s/gap_s is the sampler interval, NEVER idle.
    Real per-lane idle: v3 idle_s field; v2 rows: compute from prior row of
    the SAME (session, model) lane, else None."""
    if "idle_s" in f and f.get("idle_s") is not None:
        return f["idle_s"]
    return None  # v2 rows cannot prove idle; absence is honest

def main():
    frames = analysis_rows(load())
    if not frames:
        print("ledger empty")
        return
    t0 = min(f["ts"] for f in frames)
    t1 = max(f["ts"] for f in frames)
    days = (t1 - t0) / 86400 or 1e-9
    calls = sum(f["d_calls"] for f in frames)
    cr = sum(f["d_cache_read"] for f in frames)
    cw = sum(f["d_cache_write"] for f in frames)
    di = sum(f["d_input"] for f in frames)
    do = sum(f["d_output"] for f in frames)
    print(f"=== wire ledger: {t0} .. {t1} UTC-epoch = {days:.1f} days ===")
    print(f"windows: {len(frames):,} | calls: {calls:,} | merged windows: {sum(1 for f in frames if f['merged'])} ({sum(1 for f in frames if f['merged'])/len(frames)*100:.0f}%)")
    print(f"tokens: cache_read {cr:,} | cache_write {cw:,} | uncached_in {di:,} | output {do:,}")
    # LANE LAW (owner decree 2026-10-16): free lanes are reported separately and
    # NEVER blended into the paid hit-rate headline. Free = no cache contract;
    # a 0% hit there is not a defect and does not dilute the paid number.
    FREE_MARKERS = ("deepseek", "hyperfusion", "minimax", "free")
    def is_free(model, provider):
        s = f"{model} {provider}".lower()
        return any(k in s for k in FREE_MARKERS)
    per_lane = {"paid": [0,0,0,0], "free": [0,0,0,0]}
    for f in frames:
        lane = "free" if is_free(f["model"], f.get("provider","")) else "paid"
        m = per_lane[lane]
        m[0] += f["d_calls"]; m[1] += f["d_cache_read"]
        m[2] += f["d_input"] + f["d_cache_write"]; m[3] += f["d_output"]
    for lane in ("paid", "free"):
        c, r, u, o = per_lane[lane]
        if c:
            print(f"[{lane.upper()} lane] {c:,} calls | hit {r/(r+u)*100 if r+u else 0:.1f}% | uncached-in {u:,} | out {o:,}")
    if per_lane["paid"][0] and per_lane["free"][0]:
        print("headline hit rate = PAID lane only (free lane has no cache contract; blend shown for completeness only):")
        c, r, u, o = per_lane["paid"]; print(f"  paid-lane hit: {r/(r+u)*100:.1f}%")
    # per-window hit-rate histogram (the break sensor)
    buckets = defaultdict(int)
    for f in frames:
        tot = f["d_cache_read"] + f["d_input"] + f["d_cache_write"]
        if tot <= 0:
            buckets["no-usage"] += 1
            continue
        h = f["d_cache_read"] / tot
        b = "<50%" if h < .5 else "50-90%" if h < .9 else ">=90%"
        buckets[b] += 1
    print("per-window hit buckets:", dict(sorted(buckets.items())))
    # the four-arm inputs
    brk = [f for f in frames if (f["d_cache_read"] + f["d_input"] + f["d_cache_write"]) > 0
           and f["d_cache_read"] / (f["d_cache_read"] + f["d_input"] + f["d_cache_write"]) < 0.5]
    brk_calls = sum(f["d_calls"] for f in brk)
    brk_uncached = sum(f["d_input"] + f["d_cache_write"] for f in brk)
    print(f"break-suspect windows (<50% hit): {len(brk)} windows / {brk_calls} calls; uncached tokens there: {brk_uncached:,}")
    per_model = defaultdict(lambda: [0, 0, 0])
    for f in frames:
        m = per_model[f["model"]]
        m[0] += f["d_calls"]; m[1] += f["d_cache_read"]; m[2] += f["d_input"] + f["d_cache_write"]
    for m, (c, r, u) in sorted(per_model.items()):
        print(f"  {m}: {c} calls, hit {r/(r+u)*100 if r+u else 0:.1f}%")
    # v3: compaction-event join (events logged via sweap_event.py)
    ev_path = os.path.expanduser("~/.sweap/compaction_events.jsonl")
    if os.path.exists(ev_path):
        events = []
        with open(ev_path) as f:
            for line in f:
                try:
                    e = json.loads(line)
                except Exception:
                    continue
                if e.get("session") == "seed":
                    continue
                events.append(e)
        if events:
            print(f"compaction/prefix events on record: {len(events)}; checking breaks for an event in the prior 60s:")
            for f in brk:
                near = [e for e in events
                        if e.get("session") == f.get("session")
                        and e.get("model") == f.get("model")
                        and 0 <= f["ts"] - e.get("ts", 0) <= 60]
                tag = f"EVENT {near[0]['kind']} (ts {near[0]['ts']})" if near else "no event on record"
                print(f"  break ts {f['ts']} ({f.get('model')}): {tag}")
        else:
            print("compaction event log present but empty (seed only)")
    print("(baseline only; four-arm interpretation = separate, human-gated step)")

if __name__ == "__main__":
    main()
