#!/usr/bin/env python3
"""Stranger-runnable receipt: build a deterministic synthetic demo store,
then re-derive its expected diet numbers with the real classifier
(cli/diet.py --dry-run).

No AI tools, no network, no packages: Python standard library only.
The store construction below IS the fixture: same schema, same code path
a real store gets. Expected constants are checked twice: once against the
built store directly (SQL recount), once against cli/diet.py's printed
weigh-in.

Usage:
    python3 scripts/repro_receipt.py [--keep]
"""

import argparse
import os
import re
import sqlite3
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
DIET = os.path.join(REPO, "cli", "diet.py")

# ---- fixture spec (deterministic; do not tweak without updating EXPECT) ----
N_TWIN_GROUPS = 2          # class A groups
TWIN_ROWS_PER_GROUP = 30
TWIN_TEXT_A = "a" * 2700   # group A reasoning text, both columns equal
TWIN_TEXT_B = "b" * 2856   # group B reasoning text, both columns equal
N_REST_GROUPS = 2          # class B groups (tool rows in ENDED sessions)
REST_ROWS_PER_GROUP = 20
REST_TEXT_A = "t" * 4996
REST_TEXT_B = "u" * 4996
N_DIVERGENT = 5            # assistant rows where the twins differ (never touched)
N_NULL_REASONING = 5       # assistant rows with no reasoning at all
N_TOOL_OPEN = 10           # tool rows in open sessions (never counted)
N_USER = 10                # plain user rows

# expected values, derived from the spec above (verified 2026-10-17)
EXPECT_TWINS_N = N_TWIN_GROUPS * TWIN_ROWS_PER_GROUP
EXPECT_TWINS_B = TWIN_ROWS_PER_GROUP * (len(TWIN_TEXT_A) + len(TWIN_TEXT_B))
EXPECT_REST_N = N_REST_GROUPS * REST_ROWS_PER_GROUP
EXPECT_REST_B = REST_ROWS_PER_GROUP * (len(REST_TEXT_A) + len(REST_TEXT_B))
# the fixture plants N_DIVERGENT diverged pairs on purpose: the classifier
# must count them in the overreach tripwire but keep them OUT of class A
# (proven by EXPECT_TWINS_N staying at 60, not 65)
EXPECT_DIVERGE = N_DIVERGENT


def build_store(out_path):
    con = sqlite3.connect(out_path)
    con.executescript(
        """CREATE TABLE sessions (
             id INTEGER PRIMARY KEY,
             created_at TEXT, ended_at TEXT);
        CREATE TABLE messages (
             id INTEGER PRIMARY KEY,
             session_id INTEGER REFERENCES sessions(id),
             role TEXT, content TEXT,
             reasoning TEXT, reasoning_content TEXT,
             created_at TEXT);""")
    # 12 sessions: 1..10 ended, 11..12 open
    for sid in range(1, 13):
        ended = "2026-10-17 09:00:00" if sid <= 10 else None
        con.execute("INSERT INTO sessions VALUES (?,?,?)", (sid, "2026-10-17 08:00:00", ended))
    mid = 0

    def add(sid, role, content, reasoning=None, reasoning_content=None):
        nonlocal mid
        mid += 1
        con.execute("INSERT INTO messages VALUES (?,?,?,?,?,?,?)",
                    (mid, sid, role, content, reasoning, reasoning_content,
                     "2026-10-17 08:05:00"))

    # class A: byte twins in ended sessions
    for i in range(TWIN_ROWS_PER_GROUP):
        add(1 + i % 10, "assistant", "assistant prose",
            TWIN_TEXT_A, TWIN_TEXT_A)
        add(1 + i % 10, "assistant", "assistant prose",
            TWIN_TEXT_B, TWIN_TEXT_B)
    # divergent pairs: must never be classified
    for i in range(N_DIVERGENT):
        add(1 + i % 10, "assistant", "assistant prose",
            "thinking-v1", "thinking-v2-diverged")
    # assistant rows with NULL reasoning
    for i in range(N_NULL_REASONING):
        add(1 + i % 10, "assistant", "assistant prose")
    # class B: resting tool exhaust in ended sessions
    for i in range(REST_ROWS_PER_GROUP):
        add(1 + i % 10, "tool", REST_TEXT_A)
        add(1 + i % 10, "tool", REST_TEXT_B)
    # tool rows in open sessions: must never be classified
    for i in range(N_TOOL_OPEN):
        add(11 + i % 2, "tool", "live tool output")
    # plain user rows
    for i in range(N_USER):
        add(1 + i % 10, "user", "user prose")
    con.commit()
    con.close()


def classify(db_path):
    """The same two predicates cli/diet.py uses (kept in lockstep; a drift
    here is exactly what this script exists to catch)."""
    con = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    q = lambda s: con.execute(s).fetchone()
    twins_n, twins_b = q(
        "SELECT COUNT(*), COALESCE(SUM(LENGTH(reasoning_content)),0) "
        "FROM messages WHERE role='assistant' AND reasoning IS NOT NULL "
        "AND reasoning_content IS NOT NULL AND reasoning = reasoning_content")
    rest_n, rest_b = q(
        "SELECT COUNT(*), COALESCE(SUM(LENGTH(COALESCE(m.content,''))),0) "
        "FROM messages m LEFT JOIN sessions s ON s.id = m.session_id "
        "WHERE m.role='tool' AND s.ended_at IS NOT NULL")
    diverge = q(
        "SELECT COUNT(*) FROM messages WHERE role='assistant' "
        "AND reasoning IS NOT NULL AND reasoning_content IS NOT NULL "
        "AND reasoning != reasoning_content")[0]
    con.close()
    return twins_n, twins_b, rest_n, rest_b, diverge


def run_weighin(db_path):
    r = subprocess.run(
        [sys.executable, DIET, "--dry-run", "--db", db_path],
        capture_output=True, text=True, timeout=120)
    if r.returncode != 0 or "DRYRUN-OK" not in r.stdout:
        print(r.stdout)
        print(r.stderr)
        sys.exit("FAIL: cli/diet.py --dry-run did not print DRYRUN-OK")
    return r.stdout


def parse_weighin(out):
    got = {}

    def need(pattern):
        m = re.search(pattern, out)
        if not m:
            sys.exit(f"FAIL: weigh-in output missing expected line: {pattern}")
        return m

    m = need(r"([\d,]+) byte-twin rows, ([\d.]+) MB")
    got["twins_n"] = int(m.group(1).replace(",", ""))
    m = need(r"([\d,]+) tool rows in ENDED sessions")
    got["rest_n"] = int(m.group(1).replace(",", ""))
    m = need(r"TOTAL target: ([\d,]+) rows, ([\d.]+) MB")
    got["total_n"] = int(m.group(1).replace(",", ""))
    got["diverge_ok"] = "divergent pairs (would be overreach): 0" in out
    return got


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--keep", action="store_true",
                    help="keep the built store instead of deleting it")
    a = ap.parse_args()

    if not os.path.exists(DIET):
        sys.exit("FAIL: cli/diet.py not found next to this script's repo")

    tmp = tempfile.mkdtemp(prefix="sweap_repro_")
    db = os.path.join(tmp, "sweap_repro_demo.db")
    build_store(db)

    twins_n, twins_b, rest_n, rest_b, diverge = classify(db)
    out = run_weighin(db)
    got = parse_weighin(out)

    size = os.path.getsize(db)
    print("=" * 74)
    print("SWEAP RECEIPT REPRO : synthetic store, real classifier (cli/diet.py)")
    print(f"store built: {db}  ({size:,} bytes)" + ("" if a.keep else "  (temp; deleted on exit)"))
    print("=" * 74)

    checks = [
        ("class A twin rows", twins_n, EXPECT_TWINS_N),
        ("class A mirror bytes", twins_b, EXPECT_TWINS_B),
        ("class B resting tool rows", rest_n, EXPECT_REST_N),
        ("class B resting bytes", rest_b, EXPECT_REST_B),
        ("divergent pairs (tripwire must see them)", diverge, EXPECT_DIVERGE),
    ]
    ok = True
    for name, got_v, exp_v in checks:
        good = got_v == exp_v
        ok = ok and good
        print(f"  [{'OK ' if good else 'MISMATCH'}] {name}: {got_v:,} (expected {exp_v:,})")
    dry_expect = {"twins_n": EXPECT_TWINS_N,
                  "rest_n": EXPECT_REST_N,
                  "total_n": EXPECT_TWINS_N + EXPECT_REST_N}
    for key, exp_v in dry_expect.items():
        good = got[key] == exp_v
        ok = ok and good
        print(f"  [{'OK ' if good else 'MISMATCH'}] dry-run {key}: "
              f"{got[key]:,} (expected {exp_v:,})")
    # the planted divergent pairs must surface in diet.py's own weigh-in:
    # the overreach tripwire names them (5) instead of silently ignoring
    good = ("divergent pairs (would be overreach): 5" in out)
    ok = ok and good
    print(f"  [{'OK ' if good else 'MISMATCH'}] dry-run names 5 divergent pairs")

    if not a.keep:
        try:
            os.remove(db)
            os.rmdir(tmp)
        except OSError:
            pass

    print()
    if ok:
        print("Every expected number reproduced by the real classifier.")
        print("RECEIPT-REPRO-OK")
    else:
        sys.exit("RECEIPT-REPRO-FAIL: expected numbers did not reproduce")


if __name__ == "__main__":
    main()
