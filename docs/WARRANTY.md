# THE SWEAP LOCAL-ONLY WARRANTY
Version 1.0, 2026-10-17. Applies to: cli/diet.py, cli/sweep.py,
cli/weigh_cc.py, scripts/sweap_regrowth_snapshot.py,
scripts/sweap_watcher.py (the "sweap local tools").

## THE WARRANTY, PLAIN

Sweap's local tools never send your data anywhere. Everything they read
stays on your machine. Everything they write stays on your machine. There
is no account, no telemetry, no phone-home, no "anonymous statistics",
no crash reporter, no license check that touches the network.

## WHAT THIS MEANS PRACTICALLY

1. Reads: your AI store files (e.g. ~/.hermes/state.db, ~/.claude/...),
   read-only. Sweap never modifies a store except through the gated,
   quarantined diet/sweep commands you run explicitly.
2. Writes: quarantine copies, hash manifests, and small JSON ledgers under
   ~/.sweap/ on your disk. Nothing else.
3. Network: there is nothing to disable, because there is no network code.
   Pull the ethernet cable; sweap works identically.

## THE PROOF (mechanical, reproducible)

The only Python modules the five tools import: argparse, datetime, glob,
hashlib, json, os, shutil, sqlite3, sys, tempfile. All standard library.
None of socket, requests, urllib, http, ftplib, smtplib, subprocess, or
any URL appears outside comments. A regex scan for network patterns over
every runtime code path returns zero matches. Re-run it yourself:

    grep -rnE 'socket|requests|urllib|https?://|ftplib|smtplib|subprocess' cli/ scripts/

You will find this warranty document and nothing else. No network access
is not a promise sweap makes; it is a property the code has, checkable
without trusting anyone.

## THE LIMITS (what this warranty does NOT say)

- It does not say your AI vendor never sees your data. Sweap cannot
  control what the AI platform itself uploads; sweap only guarantees that
  IT adds nothing.
- Quarantine folders under ~/.sweap/ remain on your disk (that is the
  reversibility guarantee). Delete them when you are confident; until
  then, the bytes they hold stay home like everything else.
- The wire sampler (a separate instrument in this repo, used for research
  on our own machine) is likewise store-read-only; no network code. But
  publishing/sync of any ledger, if a user ever chooses it, is the USER
  moving files; sweap never moves them for you.

## SIGNED

sweap (the diet your AI needs). This warranty covers the five files named
above at the commit it ships with. Any future network feature would ship
in a new file and a new warranty version, loudly, never silently.
