# R23: FIRST WEIGH-IN ON A CLAUDE CODE STORE (adapter v0, verified)
Date: 2026-10-16. Follows R22 (gstack writeup). The R22 [THEORY] is now
VERIFIED: Claude Code transcripts carry per-call usage (cache_read,
cache_creation, input) on nearly every assistant row, so the sweap wire
ledger on that stack is direct reads, not sampling.

## WHAT SHIPPED

`cli/weigh_cc.py` (adapter v0): read-only census of ~/.claude/projects,
zero network calls, never writes to the store. Output = human weigh-in +
JSON card. Committed with this research file.

## FIRST REAL WEIGH-IN (this machine, 2 transcripts, 1.7 MB, 382 calls)

- Dead exhaust: 25.0% of every byte (tool results 0.07 MB + spent
  thinking 0.36 MB)
- Answered text (the useful weight): 0.01 MB
- Attachments: 0.3 MB; envelope scaffolding: 1.0 MB
- Wire truth: 28,876,835 cache-read tokens vs 393,178 cache-write and
  764 fresh = 98.65% hit rate

## HONEST READING (plain language)

1. The adapter WORKS: it reads their store, prints a weigh-in, and the
   wire numbers come straight off disk. One tool, zero integration.
2. The fat is REAL but DIFFERENT in shape: on our Hermes hub the store
   was 57% dead weight; on this small Claude Code store it is 25% dead,
   and the biggest dead component is not tool output, it is SPENT
   THINKING (242 KB of reasoning blocks that already did their job).
   That is a new dead-weight category our Hermes census never had.
   Small sample (2 files), numbers labeled as-is: first measurement,
   not a pattern yet.
3. The cache on this stack is HEALTHY (98.65%) compared to our hub's
   worst lanes, which supports the R22 note: the diet pitch on a
   gstack machine leans on WEIGHT and EXHAUST, not on break receipts;
   the break story stays king on lanes like ours (glm 96.3% was the
   GOOD lane; the free lanes sat at 0%).
4. Scaffolding note: ~57% of raw file bytes are JSON envelope, not
   message content. Never claimed as dead weight; it is the envelope
   the store writes. Separated honestly in the weigh-in.

## NEXT (unchanged queue, now unblocked)

1. Diet for the Claude Code store: provably-dead candidates are tool
   results + spent thinking, with .gstack artifacts and anything
   live-referenced pinned. Schema-break drill before any sweep.
2. More hosts = the census widens (v3.1 backfill pattern, now with a
   second store type).
3. Oct-29 four-arm experiment unchanged; z.ai prices still unlock the
   dollar layer.

FALSIFIED-IF: a multi-file census on a busy machine shows exhaust well
below 25% (pitch weakens there) or usage rows absent on some versions
(wire ledger needs a fallback).
