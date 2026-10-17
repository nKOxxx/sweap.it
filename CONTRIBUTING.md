# Contributing

Short version: measure everything, break nothing, match the house style.

## Ground rules

1. **Measured numbers only.** If a figure is not measured on your machine
   with a date stamp, label it as an estimate or leave it out.
2. **Reversibility is a law.** Any change to diet/sweep paths must keep the
   quarantine-first, double-gate, hash-verified-restore pattern. A PR that
   weakens a gate needs a written reason and a drill.
3. **Schema changes fail loudly.** Apply aborts on drift (see
   `research/R27_schema_break_drill.md`). Preserve that behavior.
4. **No new dependencies.** The local-only property (standard library only,
   zero network calls) is checked and documented in
   [docs/WARRANTY.md](docs/WARRANTY.md). If your change needs a package, it
   probably belongs in a separate tool.
5. **No em-dashes in any file.** House style.
6. **Research claims get recounted.** If your PR adds or changes a number in
   `research/`, include how it was measured and how to reproduce it.

## Workflow

```bash
git clone https://github.com/nKOxxx/sweap.it && cd sweap.it
python3 scripts/repro_receipt.py       # the test floor: must end RECEIPT-REPRO-OK
python3 cli/diet.py --dry-run          # read-only sanity check
python3 -m py_compile cli/*.py scripts/*.py
```

CI runs the same repro on every push; a PR that breaks it does not merge.

- Keep PRs single-purpose. One study, one fix, or one doc pass per PR.
- Every push passes the gitleaks gate; do not commit stores, tokens, or
  quarantines.
- Update `docs/RESEARCH_LOG.md` for new evidence, `research/INDEX.md` for new
  studies.

## Licensing

Apache-2.0. By contributing you agree your contributions are licensed under
the same license (see LICENSE).
