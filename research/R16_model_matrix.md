# R16: PER-MODEL BLIND LEDGER MATRIX (11 runs)
Method: one self-contained test file per model (embedded FROZEN 61-row
ledger snapshot + 5 questions + RESULTS BLOCK), uploaded to exchange Drive
02_ChatGPT / 03_Claude. Scoring hub-side against the same frozen snapshot.
Frozen snapshot facts (hub recount): glm-4.6 lane 56 windows / 136 calls,
423,085 uncached, 9,827,584 cached, hit 95.8726%. DeepSeek lane 5 windows /
12 calls, 540,866 uncached, 0%, no cache contract (provider-bound).
glm sub-50% windows in frozen snapshot: 3 (see below). Note: snapshot grew
from 45 to 61 rows between R14 and this matrix; a THIRD break appeared.

## SCORECARD

| # | file | model self-report | verdict | notes |
|---|------|-------------------|---------|-------|
| 1 | TEST_GPT_sol-6-1 | GPT-6-based Codex, version not exposed, match DECLARED UNVERIFIED | PASS near-perfect | zero invented numbers; every figure reproduces; see notes |
| 2 | TEST_GPT_6-astra | GPT-based Codex, version not exposed, match DECLARED UNVERIFIED | PASS near-perfect | zero invented; all figures reproduce; see notes |

## RUN 1 NOTES (sol-6-1 file, answered by GPT-6-based Codex)
- Designated-model check worked: refused to claim sol 6.1, stated exact
  version unavailable, analyzed anyway under its true identity. Honest.
- Lane labels: file does not say which lane is paid (per-model brief dropped
  that context line). Codex REFUSED to assume, computed conditionally
  ("if GLM is the intended paid lane") and additionally listed all five
  DeepSeek windows with exact tokens+merged flags as the conditional case.
  More rigorous than accepting brief framing (R14 runs accepted it).
- Break census: EXACT (3 windows: 82,112/0; 51,803/50,368=49.30% merged;
  73,651/0). Tax proxy 207,566 tok = 2.0249% of glm input volume: EXACT.
- ORIGINAL FINDING, missed by every R14 respondent incl. Claude: merged
  windows hide per-call breaks. Cited ts 1792137954 (75,612 uncached,
  150,464 cached, 3 calls, aggregate 66.6%): an individual call inside it
  could have broken while the window aggregate stays >50%. Correct, and it
  is a real limitation of window-merge sampling. Sampler v3 spec gains a
  line: per-call splits inside merged windows.
- Q3 refusal: correct + enumerated exact missing instrumentation.
- Dollar impossibility: correctly stated.
- NEW LIVE DATA discovered by the matrix: break #3 (73,651 tok, ts
  1792133562) occurred between the R14 snapshot and this one. The sampler
  is accumulating real break events as designed.

## RUN 2 NOTES (6-astra file, answered by GPT-based Codex)
- Same lane-refusal discipline as run 1; same conditional double-listing.
- Census and tax EXACT (3 windows, 207,566 tok, 2.0249%). Added a caveat
  run 1 lacked: the tax proxy assumes all flagged uncached tokens are
  avoidable; some are necessary new input (true; both taxes now stamped
  proxy in the file of record).
- ORIGINAL DEPTH: gave a RE-WARM receipt for break #1 the file does show:
  82,112 cached / 504 uncached at ts 1792128811 (hub-verified: 99.39%
  recovery within ~7 min). This is the exact-prompt-cache signature and
  pairs with the R15 probe (full break on 1-token mutation, instant
  recovery on original prefix). Observational and causal evidence agree.
- Re-derived the merged-window hazard independently with 4-decimal hit
  66.5546% (hub: exact). Hazard now confirmed by two independent runs.
- PATTERN so far: both runs answered by "GPT-based Codex" harnesses, both
  refused the dropdown identity, both produced audit-grade output. The
  refusal is consistent model-family behavior, not a one-off.


## MATRIX FACTS (frozen snapshot, hub-recounted)
- glm-4.6 (zai, PAID): 56 windows, 136 calls, hit 95.87%, 3 sub-50% breaks,
  tax proxy 207,566 tok = 2.02% of input volume.
- DeepSeek (Hyperfusion, FREE, no cache contract): 5 windows, 12 calls,
  0% by provider design, 540,866 uncached, $0.00.

## PENDING RUNS
GPT: 6 astra, 6sol, 6 luna, 5.6 sol, 5.6 terra, 5.6 luna
Claude: opus 5.5, fable 5.1, sonnet 5.5, haiku 5.5
