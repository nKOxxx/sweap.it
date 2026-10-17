#!/usr/bin/env python3
"""sweap watcher: reads the regrowth ledger, speaks only when there's news.

The trainer's voice (R21 retention story): silent on quiet days, flags when
dead weight creeps back, praises after a diet. Delivery via hermes cron
(no_agent): non-empty stdout gets delivered to chat, empty stdout = silent.

Rules:
- Reads ~/.sweap/regrowth_daily.jsonl (written by sweap_regrowth_snapshot.py,
  cron 10:05 daily). Never touches the store itself.
- FLAG condition: dead weight (mirror + sweepable) grew >= FLAG_MB since the
  last diet/baseline (or >=7 days ago, whichever is fresher).
- QUIET: under threshold. Calm days say nothing (a trainer that nags daily
  gets muted; the flag must mean something).
- After a big DROP between consecutive days (a diet ran), say what came back.
- Honest verbs: "flags", never "prevents". Gain framing: what came back /
  what it costs, not shame.
"""
import json, os, sys, datetime

LEDGER = os.path.expanduser("~/.sweap/regrowth_daily.jsonl")
STATE = os.path.expanduser("~/.sweap/watcher_state.json")
FLAG_MB = 8.0        # R21 verbatim threshold ("up 8 MB since Monday")
MIN_DAYS = 1         # never flag on same-day noise


def load_rows():
    if not os.path.exists(LEDGER):
        return []
    rows = []
    with open(LEDGER) as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def dead_weight(row):
    """Dead weight = reasoning mirror (dedupable dup) + sweepable tool MB."""
    return row.get("mirror_mb", 0.0) + row.get("tool_closed_mb", 0.0)


def main():
    rows = load_rows()
    if len(rows) < 1:
        print("Watcher has no ledger yet (snapshot cron writes it at 10:05).")
        return 0
    state = {}
    if os.path.exists(STATE):
        state = json.load(open(STATE))
    msg = None

    # First run: baseline from the EARLIEST row, then evaluate the last row
    # in this same run (a fresh install must judge its whole history at once,
    # not silently swallow it).
    if "baseline" not in state:
        first = rows[0]
        state["baseline"] = dict(date=first["date"], dead_mb=dead_weight(first),
                                 file_mb=first["db_file_mb"])

    today = rows[-1]
    baseline = state["baseline"]
    dw = dead_weight(today)
    prev = rows[-2] if len(rows) >= 2 else None
    days = (datetime.date.fromisoformat(today["date"])
            - datetime.date.fromisoformat(baseline["date"])).days

    # 1. Diet detection: big file drop between consecutive days
    if prev and (prev["db_file_mb"] - today["db_file_mb"]) >= 5.0:
        lost = prev["db_file_mb"] - today["db_file_mb"]
        msg = (f"Diet detected: {today['date']}. "
               f"Store {prev['db_file_mb']:.1f} -> {today['db_file_mb']:.1f} MB "
               f"({lost:.1f} MB back). Undo is in the quarantine. New baseline set.")
        state["baseline"] = dict(date=today["date"], dead_mb=dw, file_mb=today["db_file_mb"])
    else:
        # 2. Flag: dead weight regrew past threshold since baseline
        grew = dw - baseline["dead_mb"]
        if grew >= FLAG_MB and days >= MIN_DAYS:
            msg = (f"Junk is creeping back, up {grew:.1f} MB since {baseline['date']}. "
                   f"One command: sweap diet.")
            state["baseline"] = dict(date=today["date"], dead_mb=dw, file_mb=today["db_file_mb"])
        elif grew <= -1.0:
            # 3. Shrank without a diet (compaction etc.): quietly re-baseline
            state["baseline"] = dict(date=today["date"], dead_mb=dw, file_mb=today["db_file_mb"])

    json.dump(state, open(STATE, "w"))
    if msg:
        print(msg)
    return 0


if __name__ == "__main__":
    sys.exit(main())
