# sweap

**Weigh it. Diet it. Keep it off.**

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
  n=37,813 rows, one host)
- Diet v2 removed 33.36 MB of content in one pass, 37.57 MB of file, zero
  loss, reversible (2026-10-17 receipt)
- Regrowth measured at ~431 rows/day (~0.6 MB/day): a monthly diet is
  plenty; the watcher tells you when
- 98.65% cache hit on a healthy lane vs 0.0% after a memory lapse: the gap
  is the carrying charge

Every figure is from our own machine, labeled with its date, reproducible
from the tools. Measure yours; that is the entire product.

## Status

Private while the proof layers finish. Currently tuned for Hermes Agent
stores (`~/.hermes/state.db`) with a first weigh-in for Claude Code stores;
the diet-frame census generalizes by design. Apache-2.0. Sweap, not sweep:
the typo is the brand.

Not affiliated with caveman.so; go use both.
