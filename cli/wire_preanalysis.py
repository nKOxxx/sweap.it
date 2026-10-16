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

def main():
    frames = load()
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
    if cr + di + cw:
        print(f"aggregate hit rate: {cr/(cr+di+cw)*100:.1f}%")
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
    print("(baseline only; four-arm interpretation = separate, human-gated step)")

if __name__ == "__main__":
    main()
