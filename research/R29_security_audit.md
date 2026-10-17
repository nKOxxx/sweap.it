# SECURITY AUDIT: sweap.it build (R29)
Date: 2026-10-17. Auditor: hub. Method: 18-point baseline (security-baseline
skill) adapted to a local-only CLI product: static scans over every runtime
path, secrets hygiene, git-history secret sweep, injection-surface review,
quarantine-path integrity, trust-boundary analysis, supply chain, cron
attack surface, permissions. Threat model: local single-user CLI; the store
and ledgers are user-owned; hostile input arrives via DB text (prompt
injection into sessions) and via any file a same-user process could write.

## Verdict: PASS with 3 findings, all fixed or documented. Ship-clean.

## Findings

### F1 (FIXED): ~/.neon directory was world-listable (0755)
Files inside were 0600 (no content exposure), but the directory listing
revealed existence and names of DB connection files and an api_key file.
Fixed: chmod 0700. Verified after.

### F2 (FIXED): ~/.sweap data directory was 0755 with 0644 files
The ledgers (wire, regrowth, compaction) and watcher state were
group/other-readable. Content is metadata (sizes, counts, model names),
not conversation text, but the ledgers are the product's spine: lock down.
Fixed: dir 0700, all files 0600. Verified after.

### F3 (FIXED): watcher trusted ledger JSON without validation
sweap_watcher.py interpolated `date` from regrowth_daily.jsonl into its
output message. A tampered ledger line (same-user attacker, or a corrupted
write) could smuggle terminal-escape sequences into the delivered message.
Fixed: load_rows() now validates type + length (10-char ISO date) and
skips malformed rows. Regression run: exit 0, silent (correct).

## Reviewed clean (evidence)

- NETWORK: regex scan (socket, urllib, requests, http.client, ftp, smtp,
  telnet, URLs) over all 13 runtime files: 0 matches. Matches WARRANTY.md.
- EXEC: no eval/exec/os.system/__import__/pty anywhere. All subprocess use:
  none in runtime scripts (the tools are pure sqlite3/json/os).
- SECRETS: 0 secret-pattern hits across all git history (662 objects);
  0 identity/credential strings in any tracked file. .env + render cli.yaml
  at 0600, outside the repo. prices.json carries prices, not secrets.
- SQL INJECTION: 16 f-string SQL sites manually traced. Every interpolated
  value is a column NAME from PRAGMA table_info (schema-derived, not
  user data) or a ?-placeholder count. All VALUES travel as bound
  parameters. The one parameterized UPDATE (diet.py:332) binds both
  fields. No string-built VALUES anywhere.
- QUARANTINE PATH: shard filenames written via basename(); reads verify
  SHA-256 before any use (mismatch = abort); manifest state machine
  (staged -> applied) prevents replay. Residual: manifest `id`/`shard`
  fields are joined into paths without realpath containment - a tampered
  manifest with `../` could read outside the quarantine dir. Requires
  same-user write access to ~/.sweap (= game over anyway). Documented
  hardening note, not exploitable in the product's threat model.
- TRUST BOUNDARY (DB text): no DB-sourced string reaches os.path.join,
  open(), or shell in any script. Ledger/watcher outputs are
  numbers + validated dates only (F3 fix).
- SUPPLY CHAIN: zero third-party dependencies. Imports: argparse,
  collections, datetime, glob, hashlib, json, os, shutil, sqlite3, sys,
  tempfile, time. No requirements.txt, no pip, no lockfile to poison.
  This is the strongest supply-chain posture a Python tool can have.
- DOiS: unbounded SELECTs aggregate in SQL (SUM/COUNT server-side);
  division sites guarded against zero denominators (`if tot else 0.0`).
  One unguarded `.../calls` in sweap.py per-call math: crashes only on a
  zero-call lane (impossible in practice: rows exist only with calls).
  Cosmetic; noted.
- CRON SURFACE: 4 sweap crons run read-only scripts by absolute path from
  ~/.hermes/scripts (owner-writable only). no_agent crons cannot execute
  arbitrary model-driven code. Watcher delivers stdout to chat: bounded
  by F3 validation.
- APPLY GATE: diet/sweep destructive paths require the same manifest id
  TWICE (double-key) + state==staged + hash-verified shards + transaction
  rollback on error (schema-break drill R27 proved abort-on-drift).
- CI GATES: repo is CLI-only, no server, no client bundle: baseline items
  1-3 (client exposure, RLS, route auth) are N/A by architecture. Secret
  scanning = the history sweep above; to be re-run pre-flip and wired as
  a GitHub Action on flip (gitleaks), before any public clone exists.

## Scorecard (18-point baseline, adapted)

| # | item | status |
|---|---|---|
| 1 | client bundle public | N/A (no client) |
| 2 | client checks = UX | N/A |
| 3 | deny-by-default | PASS (dry-run default, read-only, gated apply) |
| 4 | no secret in code/history | PASS (0 hits, files 0600) |
| 5 | evidence per checkbox | PASS (this file) |
| 6 | secrets manager | PASS (OS file perms 0600; no network secrets exist) |
| 7 | RLS / row isolation | N/A (single-user local store) |
| 8 | ORM/parameterized only | PASS (all VALUES bound; schema-name interpolation traced) |
| 9 | generic errors at edge | PASS (CLI: no stack traces to users; sys.exit msgs) |
| 10 | deps pinned/audit | PASS (zero deps - strongest possible) |
| 11 | transport security | N/A (no network) |
| 12 | upload validation | N/A (no uploads) |
| 13 | authN | N/A (local user boundary = OS) |
| 14 | authZ | PASS (OS perms, now 0700/0600) |
| 15 | logging w/o secrets | PASS (ledgers carry no content) |
| 16 | backup/recovery | PASS (quarantine + restore, drill R27) |
| 17 | incident response | PASS (restore path + manifest state machine) |
| 18 | CI gates at flip | PENDING (gitleaks Action wired before repo flip) |

## Commands to re-verify (anyone can run)

    # network/exec/secret scan over all runtime files
    grep -rnE 'socket|urllib|requests|urlopen|os\.system|eval\(|exec\(|api[_-]?key' \
      cli/ scripts/ | grep -v '_comment\|no socket\|no network' || echo CLEAN
    # history secret sweep (needs gitleaks at flip; regex sweep today)
    git log --all -p | grep -cE 'AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{36}|BEGIN.*PRIVATE KEY'
    # permission check
    stat -f '%Sp %N' ~/.sweap ~/.neon ~/.hermes/.env

## Residual risks (accepted, documented)

1. Same-user attacker with write to ~/.sweap can tamper ledgers/manifests.
   Accepted: identical access = attacker already owns the store itself.
2. Manifest path fields not realpath-contained (see above). Hardening
   candidate if sweap ever runs multi-user or as a service.
3. sweap.py per-call division unguarded on a zero-call lane. Cosmetic
   availability nit, unreachable in practice.

## Ruling

The build's core security property is architectural, not procedural:
local-only, zero-dependency, read-only-by-default, reversible-with-proof.
The audit found no vulnerability class the 18-point baseline cares about
unpatched. Three hygiene findings, all fixed same-day with regression
runs. The product may go to a public repo after the flip-time gitleaks
Action lands; the website gate set by the founder is CLEARED from the
security side.
