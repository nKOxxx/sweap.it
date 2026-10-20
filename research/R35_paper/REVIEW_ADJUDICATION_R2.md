# R35 hostile review round 2 - hub adjudication (2026-10-20)

Lane: DeepSeek, session 20261020_172908_039c12, 3m09s, needle OK.
Blinding: clean review copy (DRAFT_v2_review_copy.md, header notes
stripped); referee blind to round 1. Raw: R35_hostile_review_v2_raw.txt.
Verdict: REJECT (top systems venue), 12 findings.

## Ruling per finding

| # | finding | ruling | action |
|---|---|---|---|
| F1 | mirror defect = "bug in authors' own product" | REJECT the premise, ACCEPT the clarity debt: Hermes Agent is a third-party platform (Nous Research); the authors are USERS, not maintainers. The manuscript never says so, and the referee's primary-reject reasoning is built on the opposite assumption. A user-discovered vendor-side defect is STRONGER, not weaker. | v3: one sentence in Sec 2 stating authors = users of a third-party platform |
| F2 | external validity zero, not "limited" | ACCEPT as standing: true and already limitation 1 + the receipt-board program. Not fixable today; not a blocker for arXiv/HN, is a blocker for a top venue. | no text change; inline qualifiers stay |
| F3 | dead/cold "self-refuting" accounting (called fatal) | PARTIALLY ACCEPT: the repair is naming the two axes. Dead is SEMANTIC (serves no purpose). Billing is VOLUMETRIC (every transmitted token costs, useful or not). A lapse's re-injection is volumetric, so dead-classified tokens bill at full input rate if swept. Sec 2 already says the lapse "cannot tell live from dead" - the referee quoted around it. | v3: two sentences in Sec 2 + relabel "dead subset" in 5.2 as "dead-classified subset (semantic label; lapse billing is volumetric)" |
| F4 | $8.09 labeled "at full input price" but is the gap ($0.49 = $0.60 - $0.11; full price gives $9.91) | ACCEPT - genuine catch, arithmetic right, label wrong. $8.09 is the lapse EXCESS over the cache-served counterfactual. | v3: "pays full input rate where the cache would have charged the read rate; the excess on the dead-classified subset is $8.09 (= 16.5M x [$0.60-$0.11])" - same repair for $2.23/$21.07 |
| F5 | session-ended is a proxy; measure deadness via future-read trace | PARTIALLY ACCEPT: R26's wire receipt operationally verifies never-re-transmitted for the REMOVED subset (zero re-sends post-removal, $0.00 stamped). A per-row future-read trace over the full store does not exist. | v3: cite the R26 wire receipt as the operational check; per-row trace logged as future work (R37 candidate, snapshot-diff design) |
| F6 | 431 rows/day in abstract from a 0.9-day window | ACCEPT, and the record now outranks the complaint: the daily watcher has 4 filed days (artifacts/regrowth_daily_20261020.jsonl, copied into repo). Post-diet content regrew ~1.4 MB/day Oct 18-20 vs R25's 0.59 - the rate is activity-dependent and both numbers are now filed. | v3: abstract goes qualitative; 5.3 reports BOTH measurements + the ledger table |
| F7 | protocol is agreement-theater; no positive control; run the poison test NOW | ACCEPT, EXECUTING: R35_poison_control_brief.txt carries cache-read $0.03 (filed list: $0.30). If the blind lane derives the poisoned charge without blinking, arithmetic-validation is proven blind to constants, and record-adjudication is the only catch. | lane proc_d164bb93e46a in flight; result + verdict goes into Sec 4 |
| F8 | census not auditable in-paper; no per-class table summing to 18,210,064 | PARTIALLY ACCEPT: the full live/cold/dead/receipt decomposition does NOT exist in the filed record - building it = new measurement (forbidden this cycle without founder gate). | v3: add what the record HAS (role n's, mirror bytes, census totals); full decomposition logged as R37 candidate for founder |
| F9 | 19.6 MB sweep vs 37.57 MB diet never reconciled | ACCEPT: R26 already contains the two-row ledger; copy it in. Regrowth followed the Oct-14 sweep, not the flagship diet - the paper should say so plainly. | v3: ledger table with dates in 5.3 |
| F10 | title overclaims: "The Defect" universal, "Billed Once" unobserved | FOUNDER CALL - title is founder-locked (2026-10-20, twice confirmed). Presented verbatim. Note the referee's own fix ("One Schema Stores Reasoning Twice...") is precisely the scoped register its own venue analysis says loses list clicks; paper-vs-HN titles may legitimately diverge. | presented; no unilateral change |
| F11 | "no prior work" claim scoped to private schema is vacuous | ACCEPT - one-phrase fix. | v3: "No prior work on the public record..." |
| F12 | "100% across models" small-n; per-model breakdown missing | ACCEPT - and the filed table is better than the referee suspects: R25a has all four models (glm-4.6 7,934; deepseek 1,470; MiniMax 51; glm-4.7 1) PLUS the cross-store negative control (Claude Code does NOT duplicate). The referee's own arithmetic (1,521 remainder) checks against the filed table. | v3: full per-model table + negative-control sentence in Sec 2 |

## Hub self-catch (not from the referee)

v2 says re-sent volume "averages 76,044 tokens per call." The filed
census (sweap_census_out.json) says resend_per_call_median = 76,041.5.
Wrong statistic, wrong digits. v3: "median 76,041.5 tokens per call."

## Round-over-round

Round 1: 10 findings, 8 accepted, 1 rejected (F2 denominator), 1 partial.
Round 2 re-attack: could NOT reproduce round 1's F1 (dead-definition
contradiction - fixed), F6 (point-cost - now ceiling-labeled), F7
(twin-count mismatch - footnoted), F8 (vendor miscount - fixed).
FIXED WOUNDS STAYED FIXED under a fresh blind referee. New material:
F4 (price-basis label), F5 (proxy critique), F9 (ledger), F12
(small-n) - two arithmetic-grade, two table-grade. The "fatal" F3 is a
labeling residual, not an accounting contradiction, once semantic vs
volumetric is stated. Referee's parting line concedes the engineering
habits ("labels upper bounds, refuses to invent a price, flags its own
unreconstructed number") - the record discipline is doing its job.

Standing truth: top-venue reject rests on F1/F2 (single host, zero
external replications). That is the known cost of the founder's
single-machine decree (R25a, 2026-10-17: deferred to natural adoption).
The paper is honestly a strong artifact + blog-grade paper until
outside receipts land. The receipt board is the fix; Show HN is the
recruiting event.
