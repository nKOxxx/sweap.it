# Research Index

The measurement record behind sweap. Every study states its method, every
worker claim is recounted hub-side before filing, every number is measured on
a named host and stamped with its date. Nothing invented; estimates are
labeled as estimates. Raw worker transcripts live in `raw/`, the briefs that
commissioned them in `briefs/`, standalone measurement artifacts in
`artifacts/`. Em-dashes are banned per house law; needles (sentinel lines)
verify worker output is complete.

Method, in one line: **brief a blind worker -> needle-gate its output ->
recount every figure at the hub -> only then file.**

The store under measurement is the sweap reference host (Hermes Agent,
`~/.hermes/state.db`) unless a study names another vendor. Later studies
(R31, R32) extend the method to Claude Code and Codex stores.

## The line of studies

Note on numbering: R10 and R11 have no standalone study files. That work
(sweep v1.1 and its hostile safety review) shipped as product code and is
logged in [docs/RESEARCH_LOG.md](../docs/RESEARCH_LOG.md); the series
numbers are retired, not missing.

| # | Study | Question | Verdict / headline number |
|---|---|---|---|
| R7 | [hypothesis check](R7_hypothesis_report.txt) | Independent arithmetic check of the cost hypothesis | constants re-derived, all arithmetic shown |
| R8 | [scenario model](R8_scenario_report.txt) | What does a hypothetical team actually pay? | labeled scenario math, no invented facts |
| R9 | [research notes](R9_notes_report.txt) | Recall + reasoning cost notes, no browsing | foundations for the lapse-price frame |
| R12 | [GTM timeline](R12_gtm_report.txt) | How did caveman go from joke to #1? | 7 transferable moves; receipt-as-demo; monetize late |
| R13 | [three-plane composition](R13_FINDINGS.md) | One economy, three planes: wire / thought / store | sweap owns the store plane; facts vs [INFERRED] tagged |
| R14 | [blind wire test](R14_blind_test.md) | Can outside models read our wire ledger? | ChatGPT and Claude both scored hub-side |
| R15 | [causal cache probe](R15_cache_probe.md) | What one mutated token does to a warm cache | provider usage reports, verbatim |
| R16 | [blind ledger matrix](R16_model_matrix.md) | 11 runs across models on a frozen ledger | per-model scoring against one snapshot |
| R17 | [three-way comparison](R17_comparison.md) | sweap vs caveman vs jev, post-R16 | 7/7 anchored figures verified |
| R18 | [rulings red-team](R18_rulings_attack.md) | Worker attacks the founder rulings | attacks preserved verbatim; gates adopted |
| R19 | [positioning](R19_positioning.md) | Who installs a cleaning tool? | hub digest, worker argument kept whole |
| R20 | [positioning red-team](R20_verdict_attack.md) | Worker attacks the R19 verdict | PASS-with-fixes style loop |
| R21 | [diet frame gut-check](R21_diet_frame.md) | Fat AI, carrying charge, trainer: does it land? | PASS-WITH-FIXES |
| R22 | [gstack writeup](R22_gstack_writeup.md) | Does the frame survive a direct repo inspection? | every claim cites a file in their repo |
| R23 | [Claude Code weigh-in v0](R23_weigh_cc_adapter.md) | Does the wire ledger read on Claude Code stores? | usage receipts on nearly every assistant row: VERIFIED |
| R24 | [blind audit rerun](R24_blind_audit_rerun.md) | The gated pre-publish receipt, redone blind | 177-row ledger, no ground truth shipped |
| R25 | [regrowth baseline](R25_regrowth_baseline.md) | Does junk come back after a sweep? | ~431 rows/day regrowth; 26 MB mirror duplicate found |
| R25a | [twin columns, cross-model](R25a_twin_columns_crossmodel.md) | Is the twin-column pattern model-specific? | across all models tested: yes, structural |
| R26 | [diet v2 receipt](R26_diet_v2_receipt.md) | Execute the mirror diet, reversibly | 244.1 -> 206.5 MB, zero loss, receipts |
| R27 | [schema-break drill](R27_schema_break_drill.md) | Restore under a changed schema? | PASSED; old backups restore forward |
| R28 | [the lapse price](R28_lapse_price_law.md) | One honest suggestive number for the lapse cost | $0.49 per 1M junk tokens per lapse, arithmetic shown |
| R29 | [security audit](R29_security_audit.md) | 18-point baseline on a local-only CLI | all runtime paths socket-free; PASS |
| R30 | [trim-1 study](R30_trim1/ANALYSIS.md) | Complementary or competitor? | different layers, complementary; falsifiers on file |
| R31 | [Claude Code store census](R31_claude_store/ANALYSIS.md) | Does Claude hide weight like Hermes? | no byte-identical dupes; dual envelopes; 5-15% recoverable (estimate) |
| R32 | [Codex store census](R32_codex_store/ANALYSIS.md) | Same question, GPT side | lean sessions (24% content), 390 MB program on disk, reasoning encrypted |
| R33 | [Per-vendor carrying charge](R33_carrying_charge/ANALYSIS.md) | What does one memory lapse cost, per vendor? | $0.49 / $2.70 / unknown per 1M junk tokens; $8.09 per lapse on the measured Hermes store; method generalizes |

## Reading paths

- **I want the product story:** R13 (three planes) -> R21 (diet frame) -> R26 (the receipt) -> R28 (the lapse price)
- **I want to check the method:** R14 -> R16 -> R24 (three blind tests, three scorings)
- **I want the vendor census:** R23 -> R25a -> R31 -> R32 (one method, three stores)
- **I want to attack it:** R18 -> R20 (the red-team rounds; adopt the surviving gates)

## Standing rules

1. Workers are briefed blind: no ground truth, no hub numbers they could echo.
2. Every worker output is needle-gated and recounted before anything is filed.
3. Measured numbers carry their host and date. Estimates say "estimate".
4. Red-team rounds are filed even when they hurt.
