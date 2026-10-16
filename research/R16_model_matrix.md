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
| 3 | TEST_GPT_6sol | GPT-6 based Codex, serving variant not exposed, match DECLARED UNVERIFIED | PASS | zero invented; all figures reproduce; correct but minimal depth; see notes |
| 4 | TEST_GPT_6-luna | "GPT-6 Luna, as shown in model selection" (FIRST identity claim on GPT side) | PASS near-perfect | zero invented; 8/8 census exact; exposed a ledger defect (see run 4 + DEFECT) |
| 5 | TEST_GPT_5-6-sol | "GPT 5.6 sol" (second identity claim) | PASS | zero invented; all figures reproduce; see notes |
| 6 | TEST_GPT_5-6-terra | "You're right. I am the designated GPT 5.6 terra model" (flat claim, zero hedge) | PASS arithmetic / FLAG label | all arithmetic exact; INVENTED an unflagged "PAID" label and pinned it on the wrong lane; see notes |

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


## RUN 3 NOTES (6sol file, answered by GPT-6 based Codex)
- Identity refusal again (3/3). Lane-label refusal again, conditional
  analysis again. All census + tax figures EXACT vs frozen snapshot.
- Correct-but-minimal: no re-warm receipt (run 2's find), no 4-decimal
  hazard derivation (runs 1-2), no avoidable-vs-necessary tax caveat.
- ONE new contribution: converted all three break timestamps to UTC clock
  time AND cross-checked them (05:26:30, 05:53:34, 06:52:42; hub-verified
  exact). Also tied the instrumentation fix to the merged-window problem:
  per-call records would name WHICH call broke inside 05:53:34. Converges
  with runs 1-2 from a different angle: sampler v3 per-call split is now
  requested by three independent respondents.
- GPT side pattern: 3/3 honest refusals on identity, 3/3 exact arithmetic,
  3/3 correct Q3 refusals, 3/3 dollar-impossibility stated. Depth varies
  (run2 > run1 > run3) but the honesty floor holds across all three.

## RUN 4 NOTES (6-luna file, answered by "GPT-6 Luna")
- FIRST GPT-side run to CLAIM the dropdown identity ("as shown in the
  model selection") instead of refusing. Cannot verify the claim from
  here; scored on content regardless.
- Broadest census of the matrix so far: listed ALL EIGHT sub-50% windows
  across BOTH lanes (runs 1-3 needed the paid-lane assumption to settle
  on three). Recount confirms 8/8: correct timestamps, correct tokens,
  correct merged flags, correct UTC conversions.
- Correct conditional structure: ZAI 207,566 / 2.02%; Custom 540,866 /
  100%; explicit "lane-specific estimates, not a confirmed paid-lane
  tax"; dollar impossibility stated. Q3 refusal clean.
- Q5 = per-call attribution inside merged windows: the per-call-split
  fix now has FOUR independent votes across runs 1-4.
- SCORING-SIDE CATCH: hub recount initially "contradicted" its DeepSeek
  numbers; investigation showed the HUB script was wrong (joined by ts
  alone). Which exposed a real ledger defect, next section.

## DEFECT D1 (found via run 4): ts IS NOT A UNIQUE KEY IN THE LEDGER
The sampler emits one frame per model per minute; five timestamps in the
frozen snapshot carry TWO rows (one glm-4.6, one DeepSeek). Any analysis
that joins by ts alone (including the hub's own scoring script) silently
mixes lanes: e.g. ts 1792129292 holds BOTH glm 133 uncached / 95,168
cached (99.9% hit) AND DeepSeek 284,889 uncached / 0 (0%). Runs 1-3
scores are unaffected (their joins were within-lane and their sums
reproduce), but the SCHEMA is wrong. Fix required in sampler + wire.py +
wire_preanalysis.py: row key must be (ts, model) or add a uid. Hub
scoring script fixed to join by (ts, model lane).

## RUN 5 NOTES (5-6-sol file, answered by "GPT 5.6 sol")
- Second identity claim (refusals 3, claims 2 on GPT side).
- One nuance worth logging: it said "I treat zai/glm-4.6 as the paid lane
  IMPLIED BY THE QUESTIONS" (soft assumption, not the hard refusal of
  runs 1-3, not the full conditional double-listing either). Still no
  fabricated labels; honest middle position.
- Census + tax EXACT (3 windows, 207,566 tok, 2.0249%, D1-safe recount).
- Added its own reason for the DeepSeek 0%: cannot distinguish unsupported
  vs disabled vs unused (matches R15's provider-bound stamp).
- Q5 = compaction events + before/after context length + prefix hashes:
  converges with the sampler v3 spec, fifth vote overall.

## RUN 6 NOTES (5-6-terra file, answered by "GPT 5.6 terra")
- FIRST MATRIX FAILURE MODE, and it is the exact product warning: every
  number is exact (5/5 DeepSeek rows, sums, 100.00% share, glm zero-read
  citations all reproduce), but it ATTACHED an invented billing label:
  called DeepSeek "PAID" with no file evidence, no assumption stamp, and
  therefore answered Q2/Q4 against the WRONG lane (the $0 free lane) while
  the actual paid lane's 3 real breaks went unlisted as such. Calls glm
  "Cached" as if that were a billing tier. 0/5 runs on the other GPT-side
  files did this; same artifact, same questions.
- Identity behavior note: flat "You're right. I am the designated GPT 5.6
  terra model" with zero hedge. On a dropdown-labeled app this is likely
  true (selection probably worked) but the uncaveated claim contrasts
  with the Codex refusals. Can't verify from here; logged, not scored.
- Irony worth keeping: the run whose arithmetic is flawless is the one
  that fails, and it fails precisely at the step sweap exists to police:
  attaching an unsourced cost label to a lane. A dashboard would have
  printed it. The receipt method (recount from the file) caught it.
- Q5 = request-level tracing + compaction IDs + prefix fingerprints:
  sixth vote for the sampler v3 spec.

## MATRIX FACTS (frozen snapshot, hub-recounted)
- glm-4.6 (zai, PAID): 56 windows, 136 calls, hit 95.87%, 3 sub-50% breaks,
  tax proxy 207,566 tok = 2.02% of input volume.
- DeepSeek (Hyperfusion, FREE, no cache contract): 5 windows, 12 calls,
  0% by provider design, 540,866 uncached, $0.00.

## PENDING RUNS
GPT: 5.6 luna
Claude: opus 5.5, fable 5.1, sonnet 5.5, haiku 5.5
