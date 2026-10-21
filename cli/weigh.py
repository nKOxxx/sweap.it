#!/usr/bin/env python3
"""sweap weigh: one front door, every known agent store.

Weighs whichever stores exist on this machine and says plainly which do:
  - Claude Code transcripts (~/.claude/projects/**/*.jsonl) -> cli/weigh_cc.py
  - Hermes session DB (~/.hermes/state.db)                  -> cli/diet.py census
Read-only everywhere: SQLite opened mode=ro, transcripts read, never written.
Zero network calls. Nothing is modified. The classifiers are not copied here:
the shipped tools run as-is, so there is one classifier per store and no drift.

If nothing is found you get an honest zero plus a sample of what a real
receipt looks like, not a bare error.

Usage: python3 cli/weigh.py [--db PATH] [--cc-root PATH]
"""
import argparse, datetime, glob, os, subprocess, sys

SAMPLE_RECEIPT = """\
CLASS A - reasoning mirror (dedup, zero loss):
  9,469 byte-twin rows, 26.08 MB mirror bytes -> NULLed
  (26.08 MB kept intact in the reasoning column)

CLASS B - resting tool exhaust (quarantine + delete):
  1,701 tool rows in ENDED sessions, 7.28 MB

TOTAL target: 11,170 rows, 33.36 MB
DRYRUN-OK"""


def weigh_cc(root, here):
    files = glob.glob(os.path.join(root, "**", "*.jsonl"), recursive=True)
    if not files:
        print("Claude Code: no transcripts under {} (nothing weighed)".format(root))
        return False
    print("-" * 74)
    print("STORE: Claude Code transcripts ({})".format(root))
    print("-" * 74)
    r = subprocess.run([sys.executable, os.path.join(here, "weigh_cc.py"),
                        "--root", root], capture_output=True, text=True)
    sys.stdout.write(r.stdout)
    if r.stderr:
        sys.stderr.write(r.stderr)
    return True


def weigh_hermes(db, here):
    if not os.path.exists(db):
        print("Hermes: no session DB at {} (nothing weighed)".format(db))
        return False
    print("-" * 74)
    print("STORE: Hermes session DB ({})".format(db))
    print("-" * 74)
    sys.path.insert(0, here)
    import diet
    c = diet.census(db)
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    print("  file: {:.1f} MB   {}".format(c["file"] / 1e6, now))
    print("  byte-twin rows (reasoning mirror): {:,} rows, {:.2f} MB".format(
        c["twins_n"], c["twins_b"] / 1e6))
    print("  resting tool rows (ENDED sessions): {:,} rows, {:.2f} MB".format(
        c["rest_n"], c["rest_b"] / 1e6))
    print("  divergent pairs (must be 0): {}".format(c["diverge"]))
    print("  diet plan (what a cleanup would stage): python3 cli/diet.py --dry-run")
    return True


def main():
    ap = argparse.ArgumentParser(
        description="sweap weigh: read-only census of every agent store it finds")
    ap.add_argument("--db", default=os.path.expanduser("~/.hermes/state.db"),
                    help="Hermes session DB path")
    ap.add_argument("--cc-root", default=os.path.expanduser("~/.claude/projects"),
                    help="Claude Code transcripts root")
    a = ap.parse_args()

    here = os.path.dirname(os.path.abspath(__file__))
    if not os.path.exists(os.path.join(here, "weigh_cc.py")):
        # piped from stdin (curl | python3): no sibling files on disk
        print("weigh.py is the combined door; it runs its sibling classifiers in")
        print("place (no copies, no network). Run it from a clone:")
        print("  git clone https://github.com/nKOxxx/sweap.it && cd sweap.it")
        print("  python3 cli/weigh.py")
        return 0

    print("=" * 74)
    print("WEIGH-IN : sweap, every known agent store (read-only; nothing modified)")
    print("=" * 74)

    found = weigh_cc(a.cc_root, here)
    found = weigh_hermes(a.db, here) or found

    if not found:
        print()
        print("No agent stores found on this machine: 0 files, 0 MB. That is an")
        print("honest zero, not a failure. For reference, one real machine's")
        print("receipt (measured 2026-10-17, from the README):")
        print()
        print(SAMPLE_RECEIPT)
        print()
        print("If you run Claude Code, Cursor, or Hermes somewhere, run this door")
        print("there: git clone https://github.com/nKOxxx/sweap.it && python3 cli/weigh.py")
        print("Real machines can post receipts:")
        print("https://github.com/nKOxxx/sweap.it/issues/new?template=post_your_receipt.md")
    else:
        print()
        print("Ran a deeper look or a reversible diet: python3 cli/diet.py --dry-run")
        print("Post your receipt:")
        print("https://github.com/nKOxxx/sweap.it/issues/new?template=post_your_receipt.md")
    print("WEIGH-OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
