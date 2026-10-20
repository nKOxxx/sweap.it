# Changelog

All notable changes to the sweap repo and its receipts.
Numbers are measured, dated, and never blended with estimates.

## [Unreleased]

### Added
- `research/R33_carrying_charge/`: the carrying charge priced on official
  vendor lists ($8.09 per memory lapse on the measured store; $0.49-$2.70
  per 1M dead tokens across four vendors).
- `research/R34_gtm/` + `research/R34b_gtm_revisit/`: GTM spine, posting
  schedule v2 (DeepSeek red-teamed), receipt ask template, Show-HN draft.
- `research/R35_paper/OUTLINE.md`: the paper scope (Status: SCOPING).

### Changed
- README v2 (2026-10-20): eight-card number wall up top, every card
  receipt-linked; prose cut by a third; stale status and study count fixed.
- Report Card site: plain-language token rows, zero-free copy, og/twitter
  share card (2026-10-20).

## [0.2.0] - 2026-10-17

### Added
- `scripts/repro_receipt.py`: stranger-runnable receipt. Builds a
  deterministic synthetic demo store, then re-derives its expected diet
  numbers with the real classifier (`cli/diet.py --dry-run`). Proves the
  byte-twin and resting-exhaust predicates, and shows the overreach
  tripwire naming planted divergent pairs. Stdlib only, offline, exits
  `RECEIPT-REPRO-OK` on success.
- CI workflow `receipt_repro.yml`: the repro runs on every push and PR.
- `research/INDEX.md`: index of all 25 studies with method line, reading
  paths, and standing rules.
- `SECURITY.md`, `CONTRIBUTING.md`, `AGENTS.md`.
- Top-of-README proof table, badges, and nav.

### Changed
- README anchor fixes: proof-table cells now cite their own receipts
  (37.57 MB -> R26 receipt, 90.69% -> exact census artifact
  `research/artifacts/tokenizer_exact_out.txt`, $0.49 -> R28 directly).
- Research artifacts moved under `research/artifacts/`.

### Measured
- Receipt repro: 9/9 checks OK on the synthetic fixture, deterministic
  across repeat runs (2026-10-17, Python 3.11.16, macOS arm64).

## [0.1.0] - 2026-10-17

### Measured (the founding receipts)
- Diet v2 on the reference store: 244.1 MB -> 206.5 MB, 37.57 MB of file
  returned, zero information loss; 11,170 rows; field-by-field restore
  comparison, zero mismatches. Full receipt: `research/R26_diet_v2_receipt.md`.
- Exhaust census (exact, full store): 90.69% of stored transcript tokens
  were dead tool output, n=37,813 tool rows. Receipts:
  `research/artifacts/tokenizer_remeasure_20261013.json`,
  `research/artifacts/sweap_census_out.json`.
- Regrowth baseline: ~431 rows/day (~0.6 MB/day) on the reference host.
  `research/R25_regrowth_baseline.md`.
- Schema-break drill PASSED: old backups restore into newer schemas.
  `research/R27_schema_break_drill.md`.
- Security: 18-point baseline, all runtime paths socket-free.
  `research/R29_security_audit.md`.
- Vendor censuses: Claude Code `research/R31_claude_store/ANALYSIS.md`,
  Codex `research/R32_codex_store/ANALYSIS.md`.
