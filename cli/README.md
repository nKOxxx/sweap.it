# sweap CLI (v0)

Read-only context-plane census. One command, your own data, a dollar-card receipt.

sweap is the auditor lane: it never touches traffic in flight (compressor lane
does that), never deletes anything (the quarantined sweep ships later, opt-in,
reversible). It reads your agent store and answers three questions:

1. THE WIRE: what did providers actually bill? (their own usage numbers:
   re-sent tokens per call, cache hit rate per lane)
2. THE STORE: what does your disk carry at rest? (exact tool-exhaust share)
3. THE CARD: what is that worth in dollars, and what is reclaimable?

## Run

    python3 cli/sweap.py            # print the card
    python3 cli/sweap.py --json     # also dump machine-readable census
    python3 cli/sweap.py --db PATH  # another Hermes-style state.db

Dollars are RECONSTRUCTED: billed tokens x a price table (built-in v0 or
~/.sweap/prices.json). Verify against invoices before quoting numbers.
Projection lines are stamped [projected, verification pending]; assumption
lines are stamped [ASSUMPTION]. Nothing is presented as measured that is not.

## v0 store adapter
Hermes `state.db` (sessions carry provider-reported input_tokens,
cache_read_tokens, api_call_count). v1 roadmap: adapters for other agent
stores that persist usage (Claude Code JSONL, Codex sessions, LangSmith
exports), then the harness-grade per-call ledger (W5-8).
