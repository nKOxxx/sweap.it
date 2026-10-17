<div align="center">

<img src="assets/sweap-lifter.png" alt="sweap" width="480">

# sweap

**Weigh it. Diet it. Keep it off.**

sweap weighs your AI agent's memory store, diets the dead weight out of it
reversibly, and watches so it stays off. Local-only, stdlib-only, no network.

<a href="#the-numbers-behind-the-frame"><img src="https://img.shields.io/badge/measured-244.1%20%E2%86%92%20206.5%20MB-informational?style=flat-square" alt="measured diet"></a>
<a href="research/INDEX.md"><img src="https://img.shields.io/badge/research-25%20studies,_recounted-blue?style=flat-square" alt="research corpus"></a>
<a href="docs/WARRANTY.md"><img src="https://img.shields.io/badge/network%20I%2FO-zero-success?style=flat-square" alt="zero network I/O"></a>
<a href="LICENSE"><img src="https://img.shields.io/badge/license-Apache--2.0-green?style=flat-square" alt="license"></a>
<a href=".github/workflows/receipt_repro.yml"><img src="https://img.shields.io/badge/receipt-CI%20reproducible-success?style=flat-square" alt="receipt reproducible in CI"></a>

<table>
<tr>
<td align="center" width="25%"><h3>37.57 MB</h3>of dead weight returned in one diet<br><sub><a href="research/R26_diet_v2_receipt.md">zero information loss, hash-verified restore</a></sub></td>
<td align="center" width="25%"><h3>90.69%</h3>of stored transcript tokens were dead tool output<br><sub><a href="research/artifacts/tokenizer_exact_out.txt">exact count, n=37,813 rows, one host</a></sub></td>
<td align="center" width="25%"><h3>$0.49</h3>carrying charge per 1M junk tokens per memory lapse<br><sub><a href="research/R28_lapse_price_law.md">suggestive model, arithmetic shown, glm-4.6 list price</a></sub></td>
<td align="center" width="25%"><h3>3 vendors</h3>censused with one method: Hermes, Claude Code, Codex<br><sub><a href="research/INDEX.md">three different diseases, R31 + R32</a></sub></td>
</tr>
</table>

*Figures current as of 2026-10-17. Full receipts per version: [docs/CHANGELOG.md](docs/CHANGELOG.md).*

**[The weigh-in](#the-weigh-in-30-seconds-read-only-your-own-data) · [The diet](#the-diet-reversible-gated-receipt-included) · [The trainer](#the-trainer-watches-so-you-dont-have-to) · [Commands](#commands) · [Research](research/INDEX.md) · [Safety law](#safety-law) · [Local-only, provably](#local-only-provably)**

</div>

---

## Requirements

Python 3.9+ (stdlib only, no packages, no API key). macOS or Linux. The
target store must be a SQLite database (the reference host is Hermes Agent:
`~/.hermes/state.db`; Claude Code stores work with `cli/weigh_cc.py`).

**Back up your store first.** The weigh-in is read-only, but every
destructive path in any tool should start from a copy you control.

```bash
git clone https://github.com/nKOxxx/sweap.it && cd sweap.it
python3 cli/diet.py --dry-run          # the weigh-in: read-only
python3 scripts/repro_receipt.py       # optional: verify our receipt method yourself
```

## Verify our receipt yourself (no AI tools involved)

The headline numbers in this README were measured on one machine. You do not
have to take them on faith: `scripts/repro_receipt.py` builds a deterministic
synthetic store, runs the **real** classifier against it, and checks every
number in under 2 seconds, fully offline. The same check runs in CI on every
push. It verifies the *method*; measuring your own store is the product
(`--dry-run`, above). See [docs/CHANGELOG.md](docs/CHANGELOG.md) for which
receipts each version carries.

Your AI carries dead weight. Every conversation drags it along, and when the
memory lapses, the whole pile gets re-read at full price. sweap weighs your
AI's memory, puts it on a diet, and keeps it off.

Not a cleaner you run once: a trainer that stays. It measures, it diets, it
watches, and it speaks up when the weight creeps back.

*In the family: [caveman](https://github.com/JuliusBrussee/caveman) makes your
AI talk less. Jev makes your AI think faster. gstack makes your AI a team.
sweap makes your AI weigh less.*

## The weigh-in (30 seconds, read-only, your own data)

```bash
git clone https://github.com/nKOxxx/sweap.it && cd sweap.it
python3 cli/diet.py --dry-run
```

No config, no API key, nothing leaves your machine, nothing is modified.
You get your numbers:

```
CLASS A - reasoning mirror (dedup, zero loss):
  9,469 byte-twin rows, 26.08 MB mirror bytes -> NULLed
  (26.08 MB kept intact in the reasoning column)

CLASS B - resting tool exhaust (quarantine + delete):
  1,701 tool rows in ENDED sessions, 7.28 MB

TOTAL target: 11,170 rows, 33.36 MB
DRYRUN-OK
```

One real machine's receipt; yours will differ, that is the point. On the
tested store schema, every thinking blob was stored twice, across all models
tested: 9,456 rows, 26 MB. The weigh-in finds which pattern YOUR store has.

## The diet (reversible, gated, receipt included)

```bash
python3 cli/diet.py --quarantine                        # stage: copies + hashes only
python3 cli/diet.py --apply-manifest ID --apply-manifest ID   # gated: type id twice
python3 cli/diet.py --restore ID                        # undo: every byte back
```

What one real diet did (2026-10-17, measured): **244.1 MB -> 206.5 MB,
37.57 MB of disk returned, zero information loss.** The duplicate copies
went; the originals stayed. A rehearsal on a copy first, then a field-by-field
restore comparison of all 11,170 rows: zero mismatches. The wire savings are
$0.00 and we say so: dead rows never re-sent anything. This is a disk and
hygiene receipt, not a magic bill-slasher.

## The trainer (watches so you don't have to)

Two small scripts on a daily cron, both read-only:

- the **scale**: one line a day into `~/.sweap/regrowth_daily.jsonl` (dead
  weight, sweepable inventory, duplicates, file size)
- the **watcher**: silent on quiet days; when junk creeps back it flags:

```
Junk is creeping back, up 8.3 MB since 2026-10-17. One command: sweap diet.
```

And after a diet, it tells you what came back. Honest verbs: it *finds and
cleans*, it does not claim to *prevent*.

## Commands

| command | what | writes? |
|---|---|---|
| `cli/diet.py --dry-run` | the weigh-in: dead weight, duplicates, resters | nothing |
| `cli/diet.py --quarantine` | stage a diet: full-column hashed copies | `~/.sweap/quarantine/` |
| `cli/diet.py --apply-manifest ID x2` | execute the diet (double flag = human gate) | store, reversible |
| `cli/diet.py --restore ID` | put every row back, byte-verified | store |
| `cli/sweep.py ...` | the v1.1 sweep (dead tool rows only) | same laws |
| `cli/weigh_cc.py` | weigh-in for Claude Code stores | nothing |
| `scripts/sweap_regrowth_snapshot.py` | daily scale line | `~/.sweap/` |
| `scripts/sweap_watcher.py` | the trainer's voice | `~/.sweap/` |

## Why not just compress

In-path compressors shrink requests in flight. sweap works where they can't:
the store at rest, where dead weight accumulates forever and gets re-billed
after every memory lapse. They compose; neither replaces the other. (gstack's
own design notes table their built-in compactor for the same reason we clean
at rest, not mid-flight.)

## Safety law

1. **Inventory never lies.** Every number is measured at run time, stamped
   with its date.
2. **Default to reversible.** Dry-run reads; diet quarantines before it ever
   touches; restore is hash-verified before and after.
3. **Never first-run.** Nothing destructive without a staged manifest and a
   double-flag human gate. A crash mid-apply leaves the store rolled back.
4. **Schema breaks fail loudly.** Apply aborts on any schema drift; old
   backups still restore into newer schemas (drilled, see
   `research/R27_schema_break_drill.md`).
5. **Read-only until the gate.** The default command touches nothing.
6. **Honest receipts.** Content MB and file MB are different numbers; wire
   savings are stamped $0.00 where they are $0.00; hypothetical figures are
   labeled, never blended.

## Local-only, provably

The five tools import only Python's standard library (argparse, datetime,
glob, hashlib, json, os, shutil, sqlite3, sys, tempfile). No socket, no
requests, no urllib, no URLs, no shell-outs: a regex scan over every runtime
path returns zero matches, and the command to re-run the scan is in
[docs/WARRANTY.md](docs/WARRANTY.md). Unplug the network; sweap works
identically. That is not a promise, it is a property of the code.

Measured under a hard socket firewall: weigh-in, scale, watcher, quarantine,
and restore all PASS with zero network available.

## The numbers behind the frame

- 90.69% of stored transcript tokens were dead tool output (exact count,
  n=37,813 rows, one host). Raw receipt:
  [research/artifacts/tokenizer_exact_out.txt](research/artifacts/tokenizer_exact_out.txt);
  the schema of the JSON census artifacts is documented in
  [research/artifacts/README.md](research/artifacts/README.md)
- Diet v2 removed 33.36 MB of content in one pass, 37.57 MB of file, zero
  loss, reversible (2026-10-17 receipt,
  [research/R26_diet_v2_receipt.md](research/R26_diet_v2_receipt.md))
- Regrowth measured at ~431 rows/day (~0.6 MB/day): a monthly diet is
  plenty; the watcher tells you when
  ([research/R25_regrowth_baseline.md](research/R25_regrowth_baseline.md))
- 98.65% cache hit on a healthy lane vs 0.0% after a memory lapse: the gap
  is the carrying charge
  ([research/R15_cache_probe.md](research/R15_cache_probe.md),
  [research/R16_model_matrix.md](research/R16_model_matrix.md))

Every figure is from our own machine, labeled with its date, reproducible
from the tools. Measure yours; that is the entire product.

## Status

The repo is private while one proof layer finishes: an **independent
reproduction of the reference-store receipts** (R26's diet numbers and the
exhaust census) on at least one store this repo does not own. Everything
else is in place: the tools, the method, the receipts, and a CI-reproducible
verification of the classifier (`scripts/repro_receipt.py`). When that
external check lands, the repo goes public unchanged. Private now,
per maintainer choice; the plan, the laws, and the receipts are all in the
open. Apache-2.0. Sweap, not sweep: the typo is the brand.

## For the thorough

- [research/INDEX.md](research/INDEX.md) - all 25 studies, one table, with
  reading paths (the three blind tests, the red-team rounds, the vendor
  census R31 + R32)
- [docs/CHANGELOG.md](docs/CHANGELOG.md) - which receipts each version carries
- [docs/DECISIONS.md](docs/DECISIONS.md) - the rulings and why
- [docs/STORY.md](docs/STORY.md) - the product story
- [docs/RESEARCH_LOG.md](docs/RESEARCH_LOG.md) - the dated lab notebook
- [docs/WARRANTY.md](docs/WARRANTY.md) - the zero-network proof procedure
- [SECURITY.md](SECURITY.md) - the local-only policy and how to verify it
- [CONTRIBUTING.md](CONTRIBUTING.md) - the laws, for contributors and agents
- [AGENTS.md](AGENTS.md) - how AI agents should behave in this repo

Not affiliated with caveman.so; go use both.
