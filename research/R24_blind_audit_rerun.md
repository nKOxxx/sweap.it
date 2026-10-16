# R24: BLIND AUDIT RERUN ON THE V3.1 LEDGER (the gated pre-publish receipt)
Date: 2026-10-16. Gate: "blind-audit rerun on the v3.1 ledger BEFORE any
publish" (R17 attack 3 / R18 A3). Method: DeepSeek free lane, 9m27s, blind
package frozen 19:46:52 (ledger 177 rows = 92 v2 + 85 v3; 132 compaction
events; NO ground truth), MD5 cbc16ca0b2b03cecea0a6fcc5c14e814, uploaded to
gdrive 06_Outputs. Brief: `research/briefs/R24_blind_audit_brief.txt`.
Clean answer: `R24_blind_audit_clean.txt`. Hub recount (recount wins)
recomputed every figure from the frozen zip independently.

## WHAT THE BLIND AUDITOR GOT RIGHT (verified EXACT against the frozen zip)

- A3, all 4 break candidates: windows, idle numbers, compaction gaps,
  hit rates: 0.7461 (idle 2587s), 0.0000 (39s after compaction),
  0.7427 (78s after compaction), 0.9938 (idle 2165s). ALL EXACT.
- A4, all 6 compaction-cost receipts: v2-era 0.7455@118s, 0.4930@95s,
  0.4924@70s, 0.9784@69s; v3-era 0.0000@39s, 0.7427@78s. ALL EXACT,
  including the second-decimal gap timings.
- A5: correct split between literal-largest d_input (deepseek, not
  break-caused) and largest break-caused / compaction-caused windows.
- A6 sanity + A7 data-quality: found the merged_marker duplicate-uid
  issue (32 dup uids in frozen) INDEPENDENTLY, flagged the dead write
  column, the deepseek 0% ambiguity (no cache vs not instrumented -
  CANNOT-COMPUTE, do not publish), tick drift, and 10 compaction events
  with no ledger rows (unconstructable receipts). All confirmed by hub.

## THE ONE DISCREPANCY (hub caught it, auditor half-caught it)

Auditor A1/A2 lifetime totals (glm 153 calls / 359,216 in / 13,748,864
cr; deepseek 13 / 400,920) match NEITHER the frozen input (glm 143 /
355,285 / 13,038,400; ds 3 / 88,699) nor our later live recount: they sit
BETWEEN the two. Timeline explains it: the audit session itself ran on
the DeepSeek lane for 9m27s while the sampler kept writing. The auditor
re-read the LIVE ledger mid-run instead of pinning to the frozen zip, the
exact violation the frozen-snapshot law exists to prevent. Their own A7
flagged the mismatch ("177 vs 190 depends on read time") but they did not
apply it to their own lifetime table. Per RECOUNT WINS: hub's frozen
figures are the record; auditor's A1/A2 are annotated as mid-run reads.

## FROZEN RECORD (hub recount on MD5 cbc16ca0 zip, authoritative)

- v3 real windows: glm-4.6 calls=143, input=355,285, cache_read=13,038,400,
  hit=97.35%; deepseek-V4-Flash calls=3, input=88,699, cr=0, hit=0%.
- v2 (frozen 92 rows): glm 233/692,938/16,457,216 = 95.96%; ds 12/540,866/0.
- Lifetime incl. v2 (frozen): glm 376 calls, hit 96.37%; ds 0%.
- merged_marker rows: annotation rows that DO carry deltas and share uids
  with their delta row; MUST filter row_kind!=merged_marker (naive sum
  double-counts). Confirmed real defect in the data shape, not the math.

## VERDICT (gate answer)

The instrument ships on evidence, not promise: a blind auditor with zero
ground truth reproduced every break attribution, every compaction-cost
receipt, and every gap timing to the second, and independently found the
one real data-shape trap. HIT-RATE MATH: SOUND. CONDITIONS before publish
(auditor's three, all accepted by hub):
1. Analysis code must dedupe merged_marker rows (filter, not sum-all).
2. Never publish anything derived from d_cache_write (field dead, 0 =
   unverified). Cache-write cost stays out of all copy.
3. Every published number pins a frozen ledger snapshot (MD5-stamped),
   per-lane only (zai vs custom), never blended.
Plus hub's own: deepseek 0% must publish as "cache not instrumented on
this lane", never as a real 0% miss rate (auditor's A7-5, adopted).

## FALSIFIED-IF

Any published figure later fails recomputation against its pinned MD5
snapshot would falsify this receipt. The rerun procedure (freeze, blind
package, needle, hub recount against frozen) is now the standing
pre-publish gate for every future claim.
