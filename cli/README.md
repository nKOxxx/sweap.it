# sweap CLI (v1.1)

Two commands, your own data, zero trust required:

    python3 cli/sweap.py     # census: read-only receipt (wire + store + dollar card)
    python3 cli/sweep.py     # sweep: reversible quarantine of dead tool rows

sweap is the auditor lane: it never touches traffic in flight (the compressor
lane does that) and never destroys anything (quarantine first, apply gated,
restore always available).

## sweap.py: the census (read-only)

Answers three questions from your agent store:

1. THE WIRE: what did providers actually bill? (their own usage numbers:
   re-sent tokens per call, cache hit rate per lane)
2. THE STORE: what does your disk carry at rest? (exact tool-exhaust share)
3. THE CARD: what is that worth in dollars, and what is reclaimable?

    python3 cli/sweap.py            # print the card
    python3 cli/sweap.py --json     # also dump machine-readable census
    python3 cli/sweap.py --db PATH  # another Hermes-style state.db

Dollars are RECONSTRUCTED: billed tokens x a price table (built-in v0 or
~/.sweap/prices.json). Verify against invoices before quoting numbers.
Projection lines are stamped [projected, verification pending]; assumption
lines are stamped [ASSUMPTION]. Nothing is presented as measured that is not.

## sweep.py: the sweep (v1.1, reversible)

Quarantines PROVABLY DEAD tool output: rows already compacted out of every
context window (or in finalized sessions). What it never touches:
user + assistant rows (the mandate record), live rows, anything in flight.

    python3 cli/sweep.py --dry-run      # census of the reclaim universe, no writes
    python3 cli/sweep.py --quarantine   # full-column copies + SHA-256 + manifest
    python3 cli/sweep.py --apply-manifest ID --apply-manifest ID   # gated delete
    python3 cli/sweep.py --restore ID   # full reinsert, verified against hashes

Safety machinery (per the R10C hostile safety review, all must-fixes applied):
- quarantine stages ALL columns, hashes every shard, verifies hashes before
  apply AND before restore (truncated/tampered copies abort, never restore)
- apply re-verifies every staged row is still dead (role included) inside one
  BEGIN IMMEDIATE transaction; schema drift aborts; any failure rolls back
- apply ends with a VACUUM INTO swap and reports measured before/after file
  size; FTS ghost count asserted 0 after every apply
- apply gate: the manifest id must be typed twice, identically
- wire savings stamped $0.00, always: dead rows re-send nothing. v1 reclaims
  disk; wire savings are v2 (cache arrangement on live context)

## store adapter
Hermes `state.db` (sessions carry provider-reported input_tokens,
cache_read_tokens, api_call_count; messages carry compaction flags).
Roadmap: adapters for other agent stores that persist usage (Claude Code
JSONL, Codex sessions, LangSmith exports), then the harness-grade per-call
ledger, then v2 live-context cache arrangement.
