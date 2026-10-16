#!/usr/bin/env python3
"""Append an event to ~/.sweap/compaction_events.jsonl (sampler v3 join log).

The ledger records WHAT was billed; this log records WHY the prefix may have
changed. Analysis joins on (session, model, ts): "was there an event in the
60s before this break?"

Usage:
  sweap_event.py --kind compaction  [--ctx-before N] [--ctx-after N] [--note "..."]
  sweap_event.py --kind prefix_change | restart | manual
Kinds: compaction | prefix_change | restart | manual. One line per event:
  {ts, session, model, kind, ctx_before, ctx_after, note}
Session/model default to the latest lane seen in ~/.sweap/wire_state.json
snap order (override with --session / --model).

No detection magic: Hermes compaction is not visible in the store, so events
are recorded by whoever triggers them (the agent, after a compaction, or by
hand). Honesty law: if you did not observe the event, do not log it.
"""
import json, os, time, argparse

HOME = os.path.expanduser("~")
EVENTS = os.path.join(HOME, ".sweap", "compaction_events.jsonl")
STATE = os.path.join(HOME, ".sweap", "wire_state.json")
KINDS = ("compaction", "prefix_change", "restart", "manual")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kind", required=True, choices=KINDS)
    ap.add_argument("--session")
    ap.add_argument("--model")
    ap.add_argument("--ctx-before", type=int, default=None)
    ap.add_argument("--ctx-after", type=int, default=None)
    ap.add_argument("--note", default="")
    a = ap.parse_args()
    session, model = a.session, a.model
    if (not session or not model) and os.path.exists(STATE):
        try:
            snap = json.load(open(STATE)).get("snap", {})
            if snap:
                k = sorted(snap.keys())[-1].split("|", 2)
                session = session or k[0]
                model = model or k[1]
        except Exception:
            pass
    ev = dict(ts=round(time.time()), session=session or "?", model=model or "?",
              kind=a.kind, ctx_before=a.ctx_before, ctx_after=a.ctx_after,
              note=a.note)
    with open(EVENTS, "a") as f:
        f.write(json.dumps(ev) + "\n")
    print(json.dumps(ev))

if __name__ == "__main__":
    main()
