# Dead Weight in AI Agent Memory Stores: A Cross-Vendor Census, a Reversible Diet, and a Regrowth Law

Draft v1, 2026-10-20. Status: FIRST DRAFT for founder review. Assembly
from filed studies R7-R36; no new measurements. Every numeral carries a
provenance tag [Rnn] checked by grep against the filed record.

Authorship: TBD (founder decision). Contact: TBD.

## Abstract

Production AI agents keep local memory stores: databases of transcripts,
tool outputs, and reasoning traces that persist between sessions. We
census these stores across three vendors and find that the majority of
stored content is dead weight: duplicated reasoning written twice under
two column names, and tool exhaust that is never re-read. On our
reference store (Hermes Agent, GLM-4.6), 90.69 percent of 18,210,064
stored tokens are dead by exact per-row count [R33]. We show that this
weight has a computable price: because providers bill cached reads at a
discount, any event that invalidates the cache (a memory lapse) re-reads
the dead weight at full input price, at a charge of 0.135 to 2.70 USD
per million junk tokens across five vendors' official price lists
[R33][R36]. We present a reversible diet that removed 37.57 MB from the
reference store with zero information loss and hash-verified quarantine
[R26], measure regrowth at about 431 rows per day [R25], and verify
restoration under a changed schema [R27]. All figures were derived under
a blind-worker protocol with needle-gated outputs and independent hub
recounts [R14][R24]. We release the measurement tools and a
stranger-runnable receipt [R30 context; see Section 7].

## 1. Introduction

An AI agent that works across days needs memory. Current agent platforms
implement this memory as a local store: a database file that accumulates
every transcript, every tool call, every tool result, and (for reasoning
models) every reasoning trace. The store grows with use. Unlike a chat
log, it is load-bearing: agents re-read it to restore context after
restarts, and deployment guides instruct users to preserve it.

This paper is about the plane between the store and the bill. Prior work
on context cost concerns the wire: what a model charges for the tokens
in a single request, and how to compress them. That work is necessary
but it does not ask what is IN the store. A store can hold ten million
tokens of which only a fraction is ever read again, and no wire-level
tool will notice.

We spent 27 filed studies measuring this store plane on real machines
[R-INDEX]. The short version: agent stores are mostly dead weight, the
dead weight re-bills under known conditions, it can be removed
reversibly, and it grows back slowly enough that maintenance is cheap.

Our contributions:

1. A cross-vendor census of dead weight in agent memory stores
   (Hermes/GLM, Claude Code, Codex CLI), by exact per-row count where
   the schema allows it [R23][R25][R25a][R31][R32].
2. A pricing model, the carrying charge: the extra cost a memory lapse
   imposes per million junk tokens, computed from five vendors'
   official price lists [R28][R33][R36].
3. A reversible diet with hash-verified quarantine, executed on a live
   store: 244.1 to 206.5 MB, zero loss [R26], with a schema-change
   restore drill [R27] and an 18-point security audit [R29].
4. A regrowth law: dead weight returns at a measured, modest rate,
   which makes maintenance a scheduling question rather than an
   emergency [R25].
5. A verification protocol for LLM-assisted measurement: blind briefs,
   acceptance needles, pre-registration, and hub recounts, with filed
   errata when the hub itself errs [R14][R16][R18][R20][R24].

## 2. The issue

Two mechanisms fill agent stores with weight that serves no future
request.

**Mirror writes.** The Hermes schema stores model reasoning in a
`reasoning` column and, on the same rows, a `reasoning_content` column.
On the reference store these two columns were byte-identical on all
9,455 assistant rows that carry one: 26.0 MB written twice under two
names, 26 MB of it pure duplication [R25]. The pattern is not specific
to one model: across every model on the host that writes reasoning, the
twin rate was 100 percent (7,934 of 7,934 rows for glm-4.6, 22.12 MB
duplicated) [R25a].

**Resting tool exhaust.** Tool calls store their full request
scaffolding and their outputs. Once a session ends, that content is
never re-read, but it stays in the store and grows. The exact census on
the reference store found 16,514,707 dead tokens (90.69 percent of
18,210,064 stored tokens, exact count over all 37,813 tool rows) [R33].

**Why dead weight bills.** Providers discount repeated input through
prompt caches. A healthy agent session hits the cache: our reference
store measured 95.87 percent hit rate over 56 windows (136 calls), and
98.65 percent on healthy runs [R33]. But a cache miss at session scale
(a memory lapse: a fresh session that must re-read stored context)
pays full input price on everything, healthy or junk. The junk does not
cause the lapse, but the lapse re-prices the junk: from a discounted
rate to the full rate, on every million tokens of it. Healthy sessions
hide the problem; lapses invoice it.

**The gap.** No prior work censuses what is at rest in these stores,
prices it, or demonstrates its reversible removal. That gap is this
paper.

## 3. Related work

**In-path compressors** operate on request traffic in flight.
caveman.so (Apache-2.0) proxies requests and reports 33.2 percent fewer
input tokens across whole sessions [R13]. This work is complementary:
it shrinks what leaves the machine, not what rests in the store.

**Context managers** decide which tool outputs stay in the live context
window; the Jev ecosystem (fast-jev-compaction) deletes rather than
rewrites and keeps retained content verbatim [R13]. Again the unit of
work is the window, not the store.

**Vendor mechanisms** such as prompt caching discount repeated prefixes
but change nothing about what is stored; they are the reason healthy
sessions look cheap and lapses do not [R33].

**Agent memory products** add recall and retrieval. They address what
the agent can find, not what the store carries.

What none of these do: census the store at rest, distinguish live from
dead content by exact count, price the dead content under vendor price
lists, or remove it reversibly with receipts. Store hygiene at rest is
the unclaimed lane.

## 4. How we measured it

**Stores.** Three vendors, one machine each, 2026-10: (A) Hermes Agent
(state.db, SQLite), model glm-4.6, the reference store for deep numbers;
(B) Claude Code local JSONL transcripts, 1.55 MB file [R31]; (C) Codex
CLI v0.163 session JSONL, 172,360 B session file [R32].

**Census method.** Where the schema is relational (store A), we count
exactly: every row classified, tokens measured with the vendor's own
tokenizer surface, no sampling (n = 37,813 tool rows) [R33]. Where the
store is JSONL (B, C), we census bytes by component, join the dual
envelopes, and state bands instead of points [R31][R32].

**Dead-weight criteria.** Content is dead if it is (i) a byte-identical
duplicate of content kept elsewhere in the same row (mirror twins), or
(ii) attached to a session that has ended (resting exhaust), or (iii)
bookkeeping that is never re-read (usage receipts). Criteria are
declared per store; we do not blend constructs across stores [R33].

**The verification protocol.** Every derived number in this paper
passed a four-step protocol [R14][R16][R24]:

1. The hub writes a blind brief: measured constants and official price
   lists only, no expected answers, no conclusions seeded.
2. One or more LLM workers derive the requested figures independently,
   blind to each other and to the hub's expectations. Output must end
   in a declared acceptance needle, or the run is rejected.
3. The hub pre-registers its own expected figures BEFORE reading any
   worker output, then recounts. Divergences are traced to a culprit;
   errors are logged, never averaged away.
4. Everything files: briefs, raw transcripts, adjudications, errata.
   One filed erratum is ours: in study R36 the hub's pre-registered
   expectation used the wrong denominator (total store rather than
   dead-weight subset); the worker was right; the erratum is preserved
   in the record [R36].

The protocol exists because LLM assistants fail in ways that look like
success. Blind briefs prevent answer-echoing; needles prove the output
is complete; pre-registration makes hub error detectable; filing raw
transcripts makes every step auditable after the fact.

**Ethics and footprint.** All measurement is local, read-only on live
stores, executed on copies where writes were possible. No network
calls in the tooling (verified by audit, Section 5.4) [R29].

## 5. Findings

### 5.1 The census: stores are mostly dead weight

| Store | Size | Dead weight | Construct |
|---|---|---|---|
| A: Hermes, glm-4.6 | 244.1 MB pre-diet | **90.69%** of stored tokens, exact (16,514,707 tok; n=37,813 tool rows) | token census [R33] |
| B: Claude Code | 1.55 MB file | 4.8-14.8% band (75-230 KB reversible-dedup only) | byte band [R31] |
| C: Codex CLI | 172,360 B session | 9.5% proven duplicates; 12.9-14.4% itemized static re-dump | byte census [R32] |

The three numbers are three different constructs on three different
denominators (tokens vs bytes; exact vs band) and are not comparable as
a leaderboard [R33]. What they share: in every store, the single
largest component class is content that no future request reads. On
store B, the canonical conversation is 28.1 percent of the file; the
rest is dual envelopes (16.5 percent), empty thinking signatures
(15.1 percent; the vendor erases the text but bills the envelope),
usage receipts (14.3 percent), and attachments (12.0 percent) [R31].
On store C, the session file is 24 percent content; a static
turn-context block re-dumps every turn [R32].

The mirror-twin pattern appeared on every model that writes reasoning:
a 100 percent twin rate on the reference host [R25a]. This is a schema
issue, not a model issue, which means it is fixable at the schema
layer.

### 5.2 The carrying charge: what a lapse costs

Charge per million junk tokens = full input price minus cached input
price, from each vendor's official list (retrieval dates on file)
[R28][R33][R36]:

| Vendor / model | Input | Cache read | Charge $/1M junk tok |
|---|---|---|---|
| MiniMax M3.1-Flash | $0.15 | $0.015 | **$0.135** |
| GLM-4.6 (z.ai) | $0.60 | $0.11 | **$0.49** |
| DeepSeek flash, off-peak | $0.15 | $0.003 | **$0.147** |
| DeepSeek flash, peak | $0.30 | $0.006 | **$0.294** |
| MiniMax M3 (up to 512k input) | $0.30 | $0.06 | **$0.24** |
| MiniMax M3 (above 512k input) | $0.60 | $0.12 | **$0.48** (hypothetical tier here) |
| DeepSeek V4-Pro, off-peak | $0.66 | $0.022 | **$0.638** |
| DeepSeek V4-Pro, peak | $1.32 | $0.044 | **$1.276** |
| Claude Sonnet-class | $3.00 | $0.30 | **$2.70** |
| Codex (GPT-6.1-Sol) | no public list | no public list | symbolic (P_input - P_cache) |

For the reference store (16,514,707 dead tokens), one lapse costs:
$8.09 on GLM-4.6 [R33]; $2.23 (MiniMax M3.1-Flash) to $21.07 (DeepSeek
V4-Pro peak) across the R36 vendors [R36]; $0.051-$0.155 on the Claude
Code store at a declared 4 bytes-per-token assumption (band; the store
is small) [R33]. Codex remains symbolic: no verified public price list
exists in our record, and we decline to invent one [R32][R33].

Every cell in this table was derived independently by two blind LLM
lanes and recounted at the hub; all 14 numeric cells converged exactly
[R36]. The falsification condition (a vendor whose cache-read price
equals its input price, which would collapse the charge to zero) holds
for no vendor on either list [R36].

We run these vendors on free research lanes; the dollar figures are
therefore comparison prices for a paying runner, not bills we paid.
The arithmetic does not depend on who pays.

### 5.3 The regrowth law

After the October 14 sweep removed 19.6 MB, the store regrew 384 tool
rows (0.53 MB) in about 0.9 active days: about 431 rows per day, 0.59
MB per day of new tool exhaust [R25]. New exhaust is attached to open
sessions and becomes removable when sessions close. Regrowth is real
but slow: at this rate, a monthly diet is generous maintenance, not a
chore [R25]. Hygiene is therefore a recurring discipline with a
schedule, not a one-time cleanup.

### 5.4 The diet: reversible removal, verified

The diet executed on the live reference store [R26]:

- Class A (mirror dedup): 9,469 byte-twin rows; the duplicate column
  NULLed; the keeping column retains full text. Zero information loss
  by construction; reversal is a column copy.
- Class B (resting exhaust): 1,701 tool rows from sessions ended before
  the cutoff, full-column copies staged before deletion.
- Safety: SHA-256 per quarantine shard, two-ID gated apply, crash
  sentinel, in-transaction recheck [R26].
- Result: 244.1 to 206.5 MB, 37.57 MB reclaimed by in-place vacuum;
  SQLite integrity_check ok; zero full-text-search ghost rows [R26].
- Restore under schema change: quarantine restored forward after a
  column was added to the schema; drill PASSED [R27].
- Security: 18-point audit; all runtime paths socket-free; quarantine
  path integrity and secrets hygiene verified [R29].

The diet is the answer to "is it safe": removal is reversible by
construction, the reversal path is drilled, and the tool makes no
network calls [R27][R29].

## 6. Limitations

1. **One reference host.** The exact-census numbers (90.69 percent,
   16.5M tokens, 431 rows/day) are one machine, one store, one month.
   Other hosts will differ in degree; the mechanisms (mirror writes,
   resting exhaust) are structural [R25a].
2. **Stores B and C are bands, not points.** JSONL stores resist exact
   token census; we state byte bands with declared assumptions (4
   bytes per token for B, sensitivity shown) [R31][R33].
3. **One vendor row is symbolic.** No verified public Codex price list
   exists in our record; that row stays symbolic rather than guessed
   [R33].
4. **Worker verification has limits.** Blind lanes converge on
   arithmetic, but both lanes could share a wrong premise planted by
   the hub's brief. The R36 erratum shows the hub erring and the
   protocol catching it; it cannot prove brief-error impossible
   [R24][R36].
5. **Prices move.** Vendor lists are dated to retrieval day; charges
   are recomputable from the formula and the stamped lists [R36].
6. **Filed-study errata carried forward.** R32's headline 27 percent
   static re-dump figure could not be reconstructed from its own
   itemization (itemized surface: 12.9-14.4 percent); the filed number
   stays quoted as UNRECONSTRUCTED and the itemized figures are used
   in this paper [R33]. We do not silently edit filed studies.

## 7. Reproduction

The receipt is stranger-runnable: one command builds a deterministic
synthetic store, runs the real classifier against it, re-derives the
expected diet numbers, and exits RECEIPT-REPRO-OK. It runs in CI on
every push [R30]. The tools are stdlib-only Python, offline [R29]. The
full measurement record (27 studies: briefs, raw worker transcripts,
adjudications, errata) ships in the repository [R-INDEX]. Outside
receipts (other hosts running the same census) are welcomed and become
cited evidence as they land.

## 8. Conclusion

Agent memory stores carry dead weight: mirrored reasoning, resting
tool exhaust, bookkeeping. The weight is measurable exactly where the
schema allows, and it has a price that is computable from public
lists: the carrying charge, billed whenever a memory lapse re-reads
the store at full input price. The weight is removable reversibly,
with drills and audits on record, and it returns slowly enough that a
schedule beats an emergency. Memory hygiene is recurring maintenance
with a computable price. We release the census tools, the diet, and
the full measurement record so that the next store can be weighed
before it is billed.

## References (filed studies)

[R-INDEX] research/INDEX.md, 27 studies. [R13] three-plane context
economy. [R14] blind test 1. [R16] model matrix. [R18] rulings attack.
[R20] verdict attack. [R23] Claude Code weigh-in adapter. [R24] blind
audit rerun (177-row ledger). [R25] regrowth baseline. [R25a] twin
columns cross-model. [R26] diet v2 receipt. [R27] schema-break drill.
[R28] lapse price law. [R29] security audit. [R30] trim-1 study +
repro receipt. [R31] Claude Code store census. [R32] Codex store
census. [R33] per-vendor carrying charge. [R36] dual-vendor carrying
charge.
