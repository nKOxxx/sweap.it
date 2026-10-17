# R26: DIET v2 EXECUTED - THE MIRROR DIET (33 MB, zero loss, receipts)
Date: 2026-10-17. User gate: "go ahead." Tool: cli/diet.py (2a83b06),
built on the sweep v1.1 seven-law pattern (reversible-store-surgery skill).

## WHAT RAN

- CLASS A (mirror dedup): 9,469 byte-twin assistant rows; reasoning_content
  NULLed; the reasoning column keeps the full text on every row. Zero info
  loss by construction; reversal = copy back.
- CLASS B (resting tool exhaust): 1,701 tool rows in sessions ended on or
  before 2026-10-08; full-column copies staged, then deleted.
- Manifest: diet2_20261017_120906 (quarantine ~/.sweap/quarantine/, SHA-256
  per shard, gated apply id-twice, crash sentinel, in-transaction recheck).

## RECEIPTS (measured)

- Disk: 244.1 MB -> 206.5 MB, reclaimed 37.57 MB (in-place VACUUM, measured).
  vs Oct-14 sweep (19.6 MB content, 0 MB file shrink): diet v2 doubled the
  content win AND actually shrank the file.
- integrity_check: ok. FTS ghost rows: 0.
- Live writer survived: newest row age 0s post-apply (sampler kept writing
  through diet + vacuum; no stranded inode).
- Twins remaining: 0. Reasoning column preserved: 9,469/9,469. The 300
  one-sided rows (no twin proof) correctly untouched.
- Demo discipline: full round trip ran on a COPY first (apply -37.68 MB,
  restore, field-by-field compare of ALL 11,170 staged rows: 0 mismatches)
  before the live apply was allowed.
- Wire savings: $0.00 stamped (both classes were store-dead; they never
  re-sent anything). This is a disk + hygiene receipt, not a wire claim.

## BUG CAUGHT BY THE DEMO (why the copy-first round trip is law)

First staging wrote both classes' shards into one rows/ directory; the
second class overwrote the first's shard_000 and the hash gate caught it
at apply (SHARD HASH MISMATCH: abort). Fix: per-class shard namespaces
(rows/twins/, rows/rest/). The demo copy absorbed what would have been a
live quarantine corruption. Committed in 2a83b06.

## DIET LEDGER (both diets, measured)

| date | rows | content | file |
|------|------|---------|------|
| Oct-14 sweep v1.1 | 14,955 | -19.6 MB | 261.4 -> 261.4 (freelist only) |
| Oct-17 diet v2 | 11,170 | -33.36 MB | 244.1 -> 206.5 (-37.57 MB) |

Cumulative: ~52.9 MB of dead weight removed in three days on one host,
every byte reversible until quarantine deletion (not scheduled).

## COPY-READY LINE (uses canonical claim, fa2a99d)

On the tested store schema, every thinking blob was stored twice, across
all models tested: 9,456 rows, 26 MB. Diet v2 removed the duplicate copy:
zero information loss, 37.57 MB of disk returned, verified by an
independent restore round trip.

## NEXT

- Daily snapshot (cron 0b4033431228) now watches regrowth from the new
  206.5 MB baseline; tomorrow's line is the first post-diet data point.
- Oct-29 four-arm experiment unchanged; sampler unaffected (writer proven).
- prices.json still owed for the dollar layer.
