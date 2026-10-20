<div align="center">

<img src="assets/sweap-lifter.png" alt="sweap" width="420">

# sweap

**Weigh it. Diet it. Keep it off.**

sweap weighs your AI agent's memory store, diets the dead weight out of it
reversibly, and watches so it stays off. Local-only, stdlib-only, no network.

<a href="research/INDEX.md"><img src="https://img.shields.io/badge/research-27%20studies,_recounted-blue?style=flat-square" alt="research corpus"></a>
<a href="docs/WARRANTY.md"><img src="https://img.shields.io/badge/network%20I%2FO-zero-success?style=flat-square" alt="zero network I/O"></a>
<a href=".github/workflows/receipt_repro.yml"><img src="https://img.shields.io/badge/receipt-CI%20reproducible-success?style=flat-square" alt="receipt reproducible in CI"></a>
<a href="LICENSE"><img src="https://img.shields.io/badge/license-Apache--2.0-green?style=flat-square" alt="license"></a>

<br>

<table>
<tr>
<td align="center" width="25%"><h3>37.57 MB</h3>of dead weight returned in one diet, reversible<br><sub><a href="research/R26_diet_v2_receipt.md">zero rows lost, hash-verified restore (R26)</a></sub></td>
<td align="center" width="25%"><h3>90.69%</h3>of stored transcript tokens were dead tool output<br><sub><a href="research/artifacts/tokenizer_exact_out.txt">exact count, n=37,813 rows, one host</a></sub></td>
<td align="center" width="25%"><h3>431 rows/day</h3>is how fast the dead weight grows back<br><sub><a href="research/R25_regrowth_baseline.md">the watcher speaks when it does (R25)</a></sub></td>
<td align="center" width="25%"><h3>244.1 &rarr; 206.5 MB</h3>the store after that diet, everything intact<br><sub><a href="research/R26_diet_v2_receipt.md">duplicates went, originals stayed</a></sub></td>
</tr>
<tr>
<td align="center" width="25%"><h3>$0.49</h3>carrying charge per 1M junk tokens, per memory lapse<br><sub><a href="research/R28_lapse_price_law.md">arithmetic shown, glm-4.6 list price (R28)</a></sub></td>
<td align="center" width="25%"><h3>$8.09</h3>what one memory lapse cost on the measured store<br><sub><a href="research/R33_carrying_charge/ANALYSIS.md">official price lists, four vendors (R33)</a></sub></td>
<td align="center" width="25%"><h3>0 network calls</h3>ever, in any of the five tools<br><sub><a href="docs/WARRANTY.md">proof, not promise: firewall test on record</a></sub></td>
<td align="center" width="25%"><h3>27 studies</h3>behind every number, recount-law audited<br><sub><a href="research/INDEX.md">three blind tests, two red-team rounds</a></sub></td>
</tr>
</table>

**[The weigh-in](#the-weigh-in) · [The diet](#the-diet) · [The trainer](#the-trainer) · [Commands](#commands) · [Safety law](#safety-law) · [Research](research/INDEX.md)**

</div>

---

## The weigh-in

One command, 30 seconds, read-only. Claude Code stores need no clone:

```bash
curl -sL https://raw.githubusercontent.com/nKOxxx/sweap.it/main/cli/weigh_cc.py | python3
```

Any other store (reference host: Hermes, `~/.hermes/state.db`), or if you
prefer the whole repo: Python 3.9+, macOS or Linux, nothing to install.

```bash
git clone https://github.com/nKOxxx/sweap.it && cd sweap.it
python3 cli/diet.py --dry-run
```

No config, no API key, nothing leaves your machine, nothing is modified.
One real machine's numbers:

```
CLASS A - reasoning mirror (dedup, zero loss):
  9,469 byte-twin rows, 26.08 MB mirror bytes -> NULLed
  (26.08 MB kept intact in the reasoning column)

CLASS B - resting tool exhaust (quarantine + delete):
  1,701 tool rows in ENDED sessions, 7.28 MB

TOTAL target: 11,170 rows, 33.36 MB
DRYRUN-OK
```

Yours will differ; that is the point. Ran it?
[Post your receipt](../../issues/new?template=post_your_receipt.md). Numbers
from real machines go on the public board, credit or anonymous, your call.

## The diet

**Back up your store first.** The weigh-in is read-only, but every
destructive path should start from a copy you control.

```bash
python3 cli/diet.py --quarantine                        # stage: copies + hashes only
python3 cli/diet.py --apply-manifest ID --apply-manifest ID   # gated: type id twice
python3 cli/diet.py --restore ID                        # undo: every byte back
```

What one real diet did (2026-10-17, measured): **244.1 MB to 206.5 MB,
37.57 MB of disk returned, zero information loss.** A rehearsal on a copy
first, then a field-by-field restore comparison of all 11,170 rows: zero
mismatches. A disk and hygiene receipt, not a magic bill-slasher.

## The trainer

Two small scripts on a daily cron, both read-only. The **scale** writes one
line a day; the **watcher** stays silent until the weight creeps back:

```
Junk is creeping back, up 8.3 MB since 2026-10-17. One command: sweap diet.
```

Honest verbs: it finds and cleans, it does not claim to prevent.

## Commands

| command | what | writes? |
|---|---|---|
| `cli/diet.py --dry-run` | the weigh-in: dead weight, duplicates | nothing |
| `cli/diet.py --quarantine` | stage a diet: hashed copies | `~/.sweap/quarantine/` |
| `cli/diet.py --apply-manifest ID x2` | execute the diet (double flag = human gate) | store, reversible |
| `cli/diet.py --restore ID` | put every row back, byte-verified | store |
| `cli/weigh_cc.py` | weigh-in for Claude Code stores | nothing |
| `scripts/sweap_regrowth_snapshot.py` | daily scale line | `~/.sweap/` |
| `scripts/sweap_watcher.py` | the trainer's voice | `~/.sweap/` |

## Why not just compress

In-path compressors shrink requests in flight. sweap works where they can't:
the store at rest, where dead weight accumulates forever and gets re-billed
after every memory lapse. They compose; neither replaces the other.

## Safety law

1. **Inventory never lies.** Every number is measured at run time, stamped
   with its date.
2. **Default to reversible.** Dry-run reads; diet quarantines before it ever
   touches; restore is hash-verified before and after.
3. **Never first-run.** Nothing destructive without a staged manifest and a
   double-flag human gate. A crash mid-apply leaves the store rolled back.
4. **Schema breaks fail loudly.** Apply aborts on any schema drift; old
   backups restore into newer schemas (drilled, R27).
5. **Read-only until the gate.** The default command touches nothing.
6. **Honest receipts.** Every figure says exactly what it is; hypothetical
   figures are labeled, never blended with measured facts.

## Local-only, provably

The five tools import only Python's standard library. No socket, no requests,
no urllib, no shell-outs: a regex scan over every runtime path returns zero
matches, and the scan command is in
[docs/WARRANTY.md](docs/WARRANTY.md). Measured under a hard socket firewall:
weigh-in, scale, watcher, quarantine, and restore all PASS with zero network
available. Unplug the network; sweap works identically.

## Status

Live and public, Apache-2.0. Tools, method, receipts, and a CI-reproducible
check of the classifier (`scripts/repro_receipt.py`, ends `RECEIPT-REPRO-OK`).
Ran it on your machine? That receipt is the product:
[post it](../../issues/new?template=post_your_receipt.md).

In the family: [caveman](https://github.com/JuliusBrussee/caveman) makes your
AI talk less. Jev makes your AI think faster. gstack makes your AI a team.
sweap makes your AI weigh less. Not affiliated with caveman.so; go use both.

## For the thorough

| doc | what it holds |
|---|---|
| [research/INDEX.md](research/INDEX.md) | all 27 studies, one table, with reading paths |
| [docs/CHANGELOG.md](docs/CHANGELOG.md) | which receipts each version carries |
| [docs/DECISIONS.md](docs/DECISIONS.md) | the rulings and why |
| [docs/RESEARCH_LOG.md](docs/RESEARCH_LOG.md) | the dated lab notebook |
| [docs/WARRANTY.md](docs/WARRANTY.md) | the zero-network proof procedure |
| [docs/STORY.md](docs/STORY.md) | the product story |
| [SECURITY.md](SECURITY.md) | the local-only policy |
| [CONTRIBUTING.md](CONTRIBUTING.md) / [AGENTS.md](AGENTS.md) | the laws, for humans and agents |

Sweap, not sweep: the typo is the brand.
