# AGENTS.md

Notes for AI agents (and their humans) working in this repo.

## What this repo is

sweap weighs AI agent memory stores, diets them reversibly, and watches for
regrowth. The product lives in `cli/` and `scripts/`. The evidence lives in
`research/` (see `research/INDEX.md` first). The marketing surface lives in
`site/` and is locked; do not edit it without an explicit user gate.

## House laws (binding)

1. **Nothing invented.** Every number is measured on a named host and stamped
   with a date. Estimates are labeled "estimate". Hypothetical figures stay
   labeled and never blend with measured ones.
2. **Recount before filing.** Worker/LLM output is unverified until every
   arithmetic claim is rechecked at the hub. Two of the last dozen worker
   claims were wrong on recount.
3. **Reversible by default.** Destructive paths require quarantine first and
   a double human gate (`--apply-manifest ID --apply-manifest ID`).
4. **No em-dashes.** House style; use commas, colons, or parentheses.
5. **Read-only until the gate.** The default command (`--dry-run`) touches
   nothing.
6. **Research never ships to the site** without an explicit user gate.
7. **Commits** use identity `hub <arestheagent@gmail.com>`, e.g.
   `git -c user.name="hub" -c user.email=arestheagent@gmail.com commit`.

## Layout

- `cli/` - diet.py (weigh/quarantine/apply/restore), sweep.py, weigh_cc.py
  (Claude Code adapter), wire.py, sweap.py
- `scripts/` - regrowth snapshot (daily scale line), watcher (the trainer's
  voice), sampler health, dollar card, repro_receipt.py (stranger-runnable
  receipt: synthetic store + real classifier, CI-backed)
- `research/` - R7..R32 studies + `INDEX.md`; `raw/` holds verbatim worker
  transcripts; `briefs/` holds the blind briefs; `artifacts/` holds
  standalone measurement outputs
- `docs/` - RESEARCH_LOG.md (dated lab notebook), DECISIONS.md, STORY.md,
  WARRANTY.md (the local-only proof procedure)
- `site/` - the public page (locked)

## Common tasks

- Verify your change: `python3 scripts/repro_receipt.py` must end
  `RECEIPT-REPRO-OK` (CI enforces this on every push)
- Re-run the weigh-in on your own store: `python3 cli/diet.py --dry-run`
- Add a research study: brief in `research/briefs/`, worker raw in
  `research/raw/`, hub-recounted analysis as `research/R<n>_<name>/ANALYSIS.md`
  or `research/R<n>_<name>.md`, then a row in `research/INDEX.md`.
- Schema work: read R27 first; apply must abort on drift.
