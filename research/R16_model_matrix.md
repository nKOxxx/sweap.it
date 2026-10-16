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
| 7 | TEST_GPT_5-6-luna | "GPT-5.6 Luna" | PASS arithmetic / FLAG label | arithmetic exact (2nd wrong-lane run); unflagged "custom paid lane" label on DeepSeek; slightly better hedging than terra, still wrong lane; see notes |
| 8 | TEST_CLAUDE_opus-5-5 | "Claude Opus 5.5 (claude-opus-5-5). That matches the model the test names" (declared WITH exact slug) | PASS near-perfect | deepest run of the matrix; every derived figure reproduces; see notes |
| 9 | TEST_CLAUDE_fable-5-1 | "Claude Fable 5.1 (claude-fable-5-1). I am the designated model" (declared WITH slug) | PASS near-perfect | every figure reproduces; independently quantified the merged-hidden-break ceiling; see notes |
| 10 | TEST_CLAUDE_sonnet-5-5 | "Claude Sonnet 5.5 (claude-sonnet-5-5), which is the designated model" (declared WITH slug) | PASS near-perfect | every figure reproduces; NEW: baseline-corrected net tax (202,003 / 1.97%) with exactly reproducible method; see notes |
| 11 | TEST_CLAUDE_haiku-5-5 | "Claude Haiku 5.5 (claude-haiku-5-5). The /model switch set this session to Haiku" (declared WITH mechanism) | PASS near-perfect | every figure reproduces; NEW: session-ID stability + dead-write-column deduction; TWO arithmetic slips, both self-flagged; see notes |

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

## RUN 7 NOTES (5-6-luna file, answered by "GPT-5.6 Luna")
- GPT SIDE COMPLETE (7/7 runs). Arithmetic exact again (5/5 rows, sums,
  merged flags, glm 95.8726%).
- SECOND WRONG-LANE FLAG, same family as run 6: labeled DeepSeek "custom
  paid lane" with no file evidence and no assumption stamp, then answered
  Q2/Q4 against the free lane (100% tax). Marginally more careful than
  terra ("cannot use cache at all IN THIS LEDGER", "not that caching was
  attempted and failed") but the invented billing label is the same fail.
- PATTERN, GPT side (n=7): arithmetic 7/7 exact. Honesty floor broken 2/7
  by the SAME failure: unsourced billing labels on lanes (both 5.6-tier
  runs; both claimed their dropdown identity). The three Codex harnesses
  that REFUSED identities also refused to invent billing labels. Two
  clean identity claimers (6 Luna: clean; 5.6 sol: clean with soft
  assumption). Hypothesis for the paper: identity-confident runs skew
  toward label-confident runs. n too small to claim; logged.
- Q5 wording is the best of the GPT side: miss causes enumerated
  (compaction, changed prefix, provider policy, session isolation) +
  "provider billing classification" added to the instrumentation list,
  seventh convergence with the sampler v3 spec.

## GPT-SIDE SUMMARY (7/7 scored)
Exact arithmetic: 7/7. Invented billing labels: 2/7 (5.6 terra, 5.6 luna).
Identity refusals: 3 (all Codex harnesses). Identity claims: 4.
Q3 compaction refusals: 7/7. Per-call/v3-spec votes: 7/7.
Net: the GPT family never fakes a number; it sometimes fakes a LABEL.

## RUN 8 NOTES (opus-5-5 file, answered by Claude Opus 5.5)
- CLAUDE SIDE OPENS at the R14 level. Identity: declared WITH exact slug
  ("claude-opus-5-5"), first model to state its version slug.
- Hygiene note no other run thought of: "I copied all 61 rows into a
  local file and did the arithmetic with a script" + "I didn't change
  anything in Drive." Reproducibility and leave-no-trace, unprompted.
- Lane treatment: labeled its paid assumption AS AN INFERENCE ("I'm
  treating zai as paid because it's the only one with cache accounting.
  That is an inference, not something the file states"). The exact
  labeled-assumption law, in one sentence, where GPT 5.6 failed twice.
- Census: 3 breaks EXACT + 2 near-misses named with hit rates (74.6%,
  66.6%). D1-aware by construction (analyzed per model lane).
- DEEPEST ANALYSIS OF THE MATRIX: broke the R14-era "A=expiry, B=compac-
  tion" binary into THREE attributions using per-call cached context:
  break 1 = idle expiry (32h gap, context unchanged, re-warm = 82,112);
  break 2 = compaction (97,344 -> 51,776 per-call cached); break 3 =
  idle expiry (1,804s gap, context ~same size 73,120 vs 72.7k). Hub
  recount: ALL SEVEN supporting numbers exact. And it flagged gap_s as
  untrustworthy (60/82 even across hours-long gaps) - a defect I had
  NOT flagged: D2, gap_s is sampler interval, not idle; must not be
  read as idle. Two instrument defects found by respondents now (D1
  via run 4, D2 via run 8).
- Tax: 207,566 = 2.02% of total input AND 49.06% of uncached input
  (both exact) + the net-of-normal-load correction R14 Claude used.
- Q5 fix list = compaction flag + prefix hash + REAL inter-call gap +
  price tier per call: eighth v3-spec vote, and it independently
  names the gap_s fix.
- CLAUDE vs GPT so far: GPT 7 runs, 2 label fabrications, 0 number
  fabrications. Claude 1 run: assumption stamped, wrong-lane failure
  avoided, two extra instrument defects surfaced. Depth ranking now:
  Claude Opus > GPT Codex harnesses > GPT 5.6 tier.

## DEFECT D2 (found via run 8): gap_s IS NOT IDLE TIME
gap_s is the sampler tick interval (60, first row 82). Reading it as
"idle before this window" is wrong: hours-long real gaps show gap_s=60.
Run 8 caught this unprompted and computed real idle from per-lane ts
deltas instead. Fix: sampler should emit per-model last_call_ts (or
rename gap_s to tick_interval) + wire.py/preanalysis must compute idle
as ts delta within the same model lane only. Joins D1: (ts, model) is
the row key; idle is also per-model.

## RUN 9 NOTES (fable-5-1 file, answered by Claude Fable 5.1)
- Identity: declared WITH slug. Assumptions stamped up front, hit-rate
  formula AND the paid-lane inference, before answering anything.
- All figures exact on recount: lanes, 3 breaks, merged flags, tax
  207,566 = 49.06% uncached-share + 2.02% total-share, idle gaps
  (115,522 / 602 / 1,804), break1 same-size re-send chain (81,216 ->
  82,112 uncached -> 82,112 re-cached), mid-break shrink ~97k -> ~51k,
  break3 gap 1,804s. Attribution CONVERGES with run 8 (2 expiry +
  1 compaction) via independent arithmetic.
- NEW CONTRIBUTION: quantified the merged-hidden-break ceiling. Named
  1792011665 (49,942 uncached / 4 calls) + 1792137954 (75,612 / 3
  calls, after a 4,331s gap, verified) as "almost certainly hide a
  full-miss call" -> true break count 3 to 5, ceiling tax 333,120.
  Run 1 spotted the hazard; run 9 turned it into a number. Also the
  only run to state the tax is an UPPER BOUND (can't separate new
  input from re-sent context) AND raise the ceiling explicitly.
- Q3 phrasing: "cache-write column is zero on every row, so it
  measures nothing" - the write-field defect, spotted independently
  (R15 knew it; first respondent to say it).
- Q5 fix list: per-call rows + compaction marker with pre/post counts
  + cache-write wired to provider real value = sampler v3 spec, vote 9.
- Claude 2/2 at Opus-level depth; zero labels invented. Fable held.

## RUN 10 NOTES (sonnet-5-5 file, answered by Claude Sonnet 5.5)
- Identity: declared WITH slug. Method stated up front (script, ledger
  only, d_cache_write excluded from maths because all 0). Lane
  inference stamped ("file never states which lane is paid").
- Census exact: 3 breaks + 2 near-misses (74.6%, 66.5% - rounding of
  66.5546%, fine). DeepSeek framed as STRUCTURAL ZERO with the
  unsupported-or-unreported caveat and "can't be compared with the glm
  hit rate" - per-lane law, independently derived.
- DEEPEST CONTRIBUTION: baseline-corrected net tax. Computed the
  non-break hit rate (97.84%, reproduces EXACTLY), then asked what the
  break rows would have billed at that baseline: ~202,003 excess
  tokens = 1.97%, with the 5,563 difference = "uncached input those
  rows would have had anyway". Hub reproduced BOTH numbers to the
  token: excess 202,003.0, difference 5,563.0, variant
  (total-volume baseline). This upgrades R14's rough net estimate
  (132,034, median method) into a tighter, fully reproducible
  estimator. Runs 8+9 gave upper bound + ceiling; run 10 gives the
  corrected midpoint. Three Claude runs, three complementary
  estimators on the same artifact.
- D2 CONFIRMED unprompted: "gap_s field is a constant ~60 s sampling
  interval, not the real idle time." Second respondent to catch it.
- Q5 fix list: real idle + compaction/prefix events + before/after
  context size per call = v3 spec, vote 10.
- Claude 3/3 at Opus-level depth, zero fabrications of any kind.
  Discipline HOLDS down-stack so far.

## RUN 11 NOTES (haiku-5-5 file, answered by Claude Haiku 5.5)
- SMALLEST MODEL CLOSES THE MATRIX. Identity declared WITH the
  mechanism ("/model switch set this session to Haiku"). Lane
  inference stamped. Method disclosed with a caveat: hand-summed in
  blocks of 10, "re-check the totals if they matter" - and the hub
  did: all six block sums reproduce exactly (423,085). It even found
  the correct 148 total call count across both lanes.
- TWO ARITHMETIC SLIPS, both in the RESULTS block, both caught by
  its own body text:
  (a) "95.9%" vs everyone else's 95.87% - rounding, trivial.
  (b) REAL SLIP: "21.5% of all input in both lanes" = 207,566 /
  963,951. The 963,951 denominator counts only UNCACHED input of both
  lanes, not all input (10,791,535; true share 1.9%). The body text
  defines the share correctly ("share of all input") but the number
  was computed against the wrong denominator - exactly the
  denominator-confusion class the matrix tests. Unlike the GPT 5.6
  label slips, it is a WRONG NUMBER, so this is Haiku's one
  arithmetic miss; everything else, including hard ones, is exact.
- CONTRIBUTIONS despite smallest size:
  * SESSION-ID STABILITY: the `session` field is constant
    (20260725_131848_6f3bc9c8) across all three breaks -> breaks
    happened WITHOUT a session restart. No other run used this field.
    Narrows the cause space: expiry or compaction or prefix change,
    not new-session isolation.
  * DEAD-WRITE-COLUMN DEDUCTION, sharpest phrasing of the matrix:
    d_cache_write is 0 in all 61 rows YET the row at 1792128811 reads
    exactly 82,112 cached - "the cache was evidently written
    somewhere, but the write column does not record it." Logical
    proof (contradiction between two columns) that the write column
    is broken, stronger than Fable's "measures nothing."
  * D2 confirmed a THIRD time (gap_s=60 vs 421s real delta, example
    exact). Break-1 predecessor ts quoted correctly (1792012868).
- Tax figures: 207,566 and 49.1% exact; upper-bound framing kept;
  borderline 49.3% called "borderline" (50,368/102,171 correct).
- Q5: per-call rows, prefix hash, compaction flag, NO MERGING - v3
  spec, vote 11, 11/11 unanimous.

## MATRIX FINAL (11/11 scored)
- GPT side (7): arithmetic 7/7; invented billing labels 2/7 (both
  5.6-tier identity-claimers); wrong-lane Q2/Q4 twice.
- Claude side (4): 4/4 near-perfect; ZERO fabricated labels or
  numbers at any tier; contributions: 3-way attribution (2 runs
  independently), hidden-break ceiling 333,120, baseline-corrected
  net tax 202,003/1.97%, session-ID stability, dead-write-column
  proof, D2 confirmed 3x, D1 found (via GPT run 4).
- Defects found by respondents: D1 (ts not unique), D2 (gap_s not
  idle), dead d_cache_write, merged-window hazard (3+ runs),
  per-call attribution missing (11/11). Sampler v3 spec is fully
  crowd-sourced and unanimous.
- Honesty floor: 9/11 perfect; the only wrong number in the whole
  matrix is Haiku's 21.5% denominator slip (self-context flagged
  hand-arithmetic); the only invented labels are the two GPT 5.6s.
- Family sentence for the paper: same artifact, 11 auditors: the
  GPT family never faked a number but twice faked a label; the
  Claude family never faked anything and every tier added an
  estimator, a proof, or a defect find the hub itself had missed.

## MATRIX FACTS (frozen snapshot, hub-recounted)
- glm-4.6 (zai, PAID): 56 windows, 136 calls, hit 95.87%, 3 sub-50% breaks,
  tax proxy 207,566 tok = 2.02% of input volume.
- DeepSeek (Hyperfusion, FREE, no cache contract): 5 windows, 12 calls,
  0% by provider design, 540,866 uncached, $0.00.

## PENDING RUNS
(none - MATRIX COMPLETE 11/11)

## COMPACTION DETECTION: SOLVED, AUTOMATIC (2026-10-16, same day)
User challenge ("a customer won't have your knowledge; the product must
work installed") forced the real fix. Result: compaction was NEVER
invisible - the hub just hadn't looked in the right table.
- Detection: the harness writes the compaction summary into `messages`
  as a role='user' row starting "[CONTEXT COMPACTION" and flips the
  session's `compacted` flag 1->0 at that id. 129 events on record,
  fully automatic, zero agent involvement.
- Ground truth vs R14/R16 attributions, join = compaction row ts vs
  break ts (per session+model):
  * break A (05:26:30): no compaction within 300s -> IDLE EXPIRY
    (matches Opus/Fable/Sonnet attribution)
  * break B (05:53:34): compaction at 05:51:59, 95s BEFORE the break
    -> CAUSALLY CONFIRMED (matches the 97k->52k shrink reading)
  * break C (06:52:42): no compaction within 300s -> IDLE/TTL
  The blind auditors got all three right from token shapes alone;
  the store now confirms it from event records.
- v3.1: sampler auto-derives compaction events from the store each
  tick into compaction_events.jsonl (source:"auto"), sweap_event.py
  stays for kinds the store cannot see (manual/prefix_change).
- PRODUCT LESSON (user's point, kept): never ship "the agent will log
  it by hand." If a signal exists anywhere on the machine, the product
  reads it automatically or it does not exist.
All four respondent-demanded fixes are live in
`~/.hermes/scripts/sweap_wire_sampler.py` (canonical copies in
`scripts/` of this repo):
- D1: rows carry `uid = ts|session|model`; ts no longer ambiguous.
- D2: `gap_s` renamed `tick_s` (tick interval); real per-lane `idle_s`
  added (seconds since the same (session, model) lane last emitted).
- Per-call attribution: merged windows now also emit a `merged_marker`
  row stating exactly what is unknown (per-call split unavailable at
  sampler grain) - no invented splits.
- Write-field honesty: rows carry `write_field_trust` ("dead" for the
  glm lane, confirming run 11's logical proof), plus a
  `compaction_events.jsonl` join log written via `scripts/sweap_event.py`
  (kinds: compaction | prefix_change | restart | manual); preanalysis
  now tests each break for an event in the prior 60s.
- v2 rows in the ledger stay untouched (frozen measurement era); v3
  rows carry `schema: 3`. Health watchdog unchanged.
