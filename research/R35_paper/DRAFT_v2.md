# Dead Weight in AI Agent Memory Stores (title options in header note)

Draft v2, 2026-10-20. Founder review copy. Built from v1 + hostile-review
adjudication (REVIEW_ADJUDICATION.md: 8 findings accepted, 1 rejected on
filed facts, 1 partially accepted).

TITLE OPTIONS (founder picks):
  T1 (twin-led, reviewer F10 endorses): "Mirrored Twice, Billed Once:
      Structural Duplication and Measured Dead Weight in AI Agent
      Memory Stores"
  T2 (balanced): "Dead Weight in AI Agent Memory Stores: An Exact
      Census on One Store, Byte Bands on Two More, and a Reversible
      Diet"
  T3 (price-led): "The Carrying Charge of Agent Memory: Pricing and
      Reversibly Removing Dead Weight in Local Agent Stores"

Changes v1 -> v2 per finding: F1 third content state; F2 mirror stated
outside the 90.69%; F3 census renamed; F4 law -> measured rate; F5
guarantee boundary; F6 $8.09 relabeled ceiling; F7 twin-count footnote;
F8 four-vendor phrasing; F9 soft language; F10 twin defect promoted.
Authorship: TBD (founder). All numerals provenance-grepped 94/94 in v1;
v2 re-grepped below.

## Abstract

Production AI agents keep local memory stores: databases of transcripts,
tool outputs, and reasoning traces that persist between sessions. We
identify a structural duplication defect in how agent platforms persist
model reasoning: across every model on our reference host that writes
reasoning, the text is written twice, byte-identical, under two column
names - 26.0 MB duplicated, a 100 percent twin rate across models
[R25][R25a]. The defect is vendor-side and usage-independent, and it is
the only result in this paper that is structural rather than
usage-dependent. We then census the remaining dead weight: on the
reference store (Hermes Agent, GLM-4.6), 16,514,707 of 18,210,064
stored transcript tokens - 90.69 percent by exact per-row count over
all 37,813 tool rows - serve no future purpose (never transmitted
again in healthy operation; transmitted once more, at full price, only
if a memory lapse re-injects stored context) [R33]. Mirrored reasoning
is additional to this figure. We price the transmission: because
providers discount cached reads, a lapse re-prices junk at the gap
between full input and cached input - 0.135 to 2.70 USD per million
junk tokens across four vendors' official price lists, one vendor
staying symbolic for lack of a public list [R33][R36]. We present a
reversible diet that removed 37.57 MB with zero information loss and
hash-verified quarantine [R26], measure regrowth at about 431 rows per
day on the reference host [R25], and verify restoration under a changed
schema [R27]. All derived figures passed a blind-worker protocol with
acceptance needles, pre-registration, and hub recounts; the protocol's
guarantee boundary is stated, and one filed erratum shows it catching a
hub-side error [R14][R24][R36].

## 1. Introduction

An AI agent that works across days needs memory. Current agent
platforms implement this memory as a local store: a database file that
accumulates every transcript, every tool call, every tool result, and
(for reasoning models) every reasoning trace. The store grows with use.
Unlike a chat log, it is load-bearing: agents re-read it to restore
context after restarts, and deployment guides instruct users to
preserve it.

This paper is about the plane between the store and the bill. Prior
work on context cost concerns the wire: what a model charges for the
tokens in a single request, and how to compress them. That work is
necessary but it does not ask what is IN the store. A store can hold
ten million tokens of which only a fraction is ever read again, and no
wire-level tool will notice.

We spent 27 filed studies measuring this store plane on real machines
[R-INDEX]. The short version: agent stores carry content that serves no
future purpose, part of it duplicated by schema design, and the dead
portion re-bills under known conditions; it can be removed reversibly,
and it grows back slowly enough that maintenance is cheap.

Our contributions:

1. A structural duplication defect, identified and measured: agent
   platforms persist model reasoning twice, byte-identical, under two
   column names. On the reference host the twin rate is 100 percent on
   every model that writes reasoning (9,455 rows, 26.0 MB duplicated
   at audit time) [R25][R25a]. The defect is vendor-side and
   independent of user behavior.
2. An exact dead-weight census on one relational store (90.69 percent
   of stored transcript tokens, every row counted, n = 37,813 tool
   rows) and byte-band censuses on two JSONL samples (Claude Code,
   Codex CLI) [R31][R32][R33]. We do not claim the three numbers are
   comparable; they are three constructs on three denominators.
3. A pricing model, the carrying charge: the cost a lapse imposes per
   million junk tokens at transmission, computed from four vendors'
   official price lists, with the fifth vendor symbolic (no public
   list) [R28][R33][R36].
4. A reversible diet with hash-verified quarantine, executed on a live
   store: 244.1 to 206.5 MB, zero loss [R26], restore drilled under
   schema change [R27], security-audited [R29].
5. A measured regrowth rate: about 431 rows per day on the reference
   host, which makes maintenance a scheduling question rather than an
   emergency [R25].
6. A verification protocol for LLM-assisted measurement - blind
   briefs, acceptance needles, pre-registration, hub recounts - with
   its guarantee boundary stated explicitly and a filed erratum
   demonstrating hub-error detection [R14][R16][R24][R36].

## 2. The issue

Three content classes fill agent stores with weight that serves no
future purpose.

**Mirror writes (structural).** The Hermes schema stores model
reasoning in a `reasoning` column and, on the same rows, a
`reasoning_content` column. At audit time these two columns were
byte-identical on all 9,455 assistant rows that carry one: 26.0 MB
written twice under two names [R25]. The pattern is not specific to
one model: across every model on the host that writes reasoning, the
twin rate was 100 percent (7,934 of 7,934 rows for glm-4.6, 22.12 MB
duplicated) [R25a]. This is a schema defect, not a usage pattern -
which means it is fixable at the schema layer, by the vendor, for
every user at once.

**Resting tool exhaust (usage-dependent).** Tool calls store their
full request scaffolding and outputs. Once a session ends, that
content never transmits again in healthy operation - but it stays in
the store and grows. The exact census on the reference store found
16,514,707 such tokens: 90.69 percent of the store's 18,210,064
transcript tokens, exact count over all 37,813 tool rows [R33].

**A note on "dead".** We use dead weight for content that serves no
future purpose in healthy operation. Three states are distinguished:

- live: content the agent re-reads in ordinary operation;
- cold-but-rereadable: stored context a fresh session re-injects after
  a restart or memory lapse - dormant, but transmitted again when the
  lapse happens;
- dead: content that serves no future purpose in any state - never
  transmitted again in healthy operation, and re-priced at full input
  rate only in the lapse event, because the lapse re-reads stored
  context wholesale and cannot tell live from dead.

Dead content does not cause lapses. But a lapse re-transmits it, and
the transmission has a price. That price is measurable per million
junk tokens from public price lists, and it is the subject of
Section 5.2.

**Why dead weight bills.** Providers discount repeated input through
prompt caches. A healthy session hits the cache: our reference store
measured 95.87 percent hit rate over 56 windows (136 calls), 98.65
percent on healthy runs [R33]. A memory lapse (fresh session, 0.0
percent hit) pays full input price on what it re-injects. Healthy
sessions hide the problem; lapses invoice it.

**The gap.** No prior work identifies the mirror-write defect, censuses
what is at rest in these stores, prices the weight under vendor price
lists, or demonstrates reversible removal. That gap is this paper.

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

What none of these do: identify structural duplication in the store
schema, census the store at rest, distinguish live from dead content
by exact count, price the dead content under vendor price lists, or
remove it reversibly with receipts. Store hygiene at rest is the
unclaimed lane.

## 4. How we measured it

**Stores.** Three vendors, one machine each, 2026-10: (A) Hermes Agent
(state.db, SQLite), model glm-4.6, the reference store for exact
numbers; (B) Claude Code local JSONL transcripts, 1.55 MB file [R31];
(C) Codex CLI v0.163 session JSONL, 172,360 B session file [R32]. B
and C are single-file samples, not full stores; we claim exactness
only where the schema allows it (store A) [R33].

**Census method.** Store A is relational: we count exactly, every row
classified, tokens measured with the vendor's tokenizer surface, no
sampling (n = 37,813 tool rows) [R33]. Stores B and C are JSONL: we
census bytes by component, join the dual envelopes, and state bands
instead of points [R31][R32].

**Dead-weight criteria.** Content is dead if it is (i) a byte-identical
duplicate of content kept elsewhere in the same row (mirror twins), or
(ii) attached to a session that has ended (resting exhaust), or (iii)
bookkeeping that is never re-read (usage receipts). Criteria are
declared per store; constructs are not blended across stores [R33].

**The verification protocol.** Every derived number passed a four-step
protocol [R14][R16][R24]:

1. The hub writes a blind brief: measured constants and official price
   lists only, no expected answers, no conclusions seeded.
2. One or more LLM workers derive the requested figures independently,
   blind to each other and to the hub's expectations. Output must end
   in a declared acceptance needle, or the run is rejected.
3. The hub pre-registers its own expected figures BEFORE reading any
   worker output, then recounts. Divergences are traced; errors are
   logged, never averaged away.
4. Everything files: briefs, raw transcripts, adjudications, errata.
   In study R36 the hub's pre-registered expectation used the wrong
   denominator; the worker was right; the erratum is preserved [R36].

**What the protocol guarantees, and what it does not.** The protocol
certifies internal agreement: independent derivations converge, and
hub errors can surface (and did, in R36). It does not certify
correctness against ground truth: a wrong constant planted in the
brief would be reproduced by every blind lane, because all lanes
derive from the brief's stated constants. Needles prove completeness,
not truth; hub recounts prove hub consistency, not external validity.
Vendor prices in this paper are therefore quoted from official
retrieved lists (stamped by date), not from worker outputs, for
exactly this reason. A proposed strengthening - deliberately poisoning
a brief constant to test whether adjudication catches it - is noted
for future work.

**Ethics and footprint.** All measurement is local, read-only on live
stores, executed on copies where writes were possible. No network
calls in the tooling (verified by audit, Section 5.4) [R29].

## 5. Findings

### 5.1 The census: what the stores carry

| Store | Size | Dead weight | Construct |
|---|---|---|---|
| A: Hermes, glm-4.6 | 244.1 MB pre-diet | **90.69%** of stored transcript tokens, exact (16,514,707 tok; n=37,813 tool rows) | token census [R33] |
| B: Claude Code | 1.55 MB file | 4.8-14.8% band (75-230 KB reversible-dedup only) | byte band [R31] |
| C: Codex CLI | 172,360 B session | 9.5% proven duplicates; 12.9-14.4% itemized static re-dump | byte census [R32] |

These are three different constructs on three different denominators
(tokens vs bytes; exact vs band) and are not comparable as a
leaderboard [R33]. Store B's file is 28.1 percent canonical
conversation; the rest is dual envelopes (16.5 percent), empty
thinking signatures (15.1 percent; the vendor erases the text but the
envelope remains), usage receipts (14.3 percent), and attachments
(12.0 percent) [R31]. Store C's session file is 24 percent content; a
static turn-context block re-dumps every turn [R32].

The mirror-twin defect (Section 2) appeared on every model that writes
reasoning: 100 percent twin rate on the reference host, additional to
the 90.69 percent figure above [R25a]. On store A, the single largest
content class is material no future request reads; on B and C, the
single largest classes are envelope and scaffolding, respectively.

### 5.2 The carrying charge: what a lapse's transmission costs

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
| MiniMax M3 (above 512k input) | $0.60 | $0.12 | **$0.48** (tier shown for completeness; inoperative for this store) |
| DeepSeek V4-Pro, off-peak | $0.66 | $0.022 | **$0.638** |
| DeepSeek V4-Pro, peak | $1.32 | $0.044 | **$1.276** |
| Claude Sonnet-class | $3.00 | $0.30 | **$2.70** |
| Codex (GPT-6.1-Sol) | no public list | no public list | symbolic (P_input - P_cache) |

**Scale honesty.** A lapse that re-injected the entire dead subset
(16,514,707 tokens) at full input price would cost $8.09 on GLM-4.6
[R33]; across the R36 vendors, $2.23 (MiniMax M3.1-Flash) to $21.07
(DeepSeek V4-Pro peak) [R36]. These figures are UPPER BOUNDS: they
price the whole dead subset as if transmitted in one event. A real
lapse re-injects through bounded windows; the reference host's
provider-reported re-sent volume averages 76,044 tokens per call
(filed census), so a single-window lapse transmission prices in the
fourth of a cent to a few cents range per call at these charges, and
the $8.09 figure is the ceiling for a wholesale re-read that we have
not observed [R33]. On the Claude Code sample, the band is
$0.051-$0.155 at a declared 4 bytes-per-token assumption [R33]. Codex
stays symbolic: no verified public price list exists in our record,
and we decline to invent one [R32][R33].

Every charge cell was derived independently by two blind LLM lanes and
recounted at the hub; all 14 numeric cells converged exactly [R36].
The falsification condition (a vendor whose cache-read price equals
its input price, collapsing the charge to zero) holds for no vendor on
either list [R36].

We run these vendors on free research lanes; the dollar figures are
comparison prices for a paying runner, not bills we paid.

### 5.3 The regrowth rate

After the October 14 sweep removed 19.6 MB, the store regrew 384 tool
rows (0.53 MB) in about 0.9 active days: about 431 rows per day, 0.59
MB per day of new tool exhaust [R25]. New exhaust is attached to open
sessions and becomes removable when sessions close. Regrowth is real
but slow: at this rate, a monthly diet is generous maintenance [R25].
This is a measured rate on one host over one interval - not a law -
and the receipt board exists to collect other hosts' rates (Section
7). Hygiene is a recurring discipline with a schedule, not a one-time
cleanup.

### 5.4 The diet: reversible removal, verified

The diet executed on the live reference store [R26]:

- Class A (mirror dedup): 9,469 byte-twin rows; the duplicate column
  NULLed; the keeping column retains full text. Zero information loss
  by construction; reversal is a column copy. (Footnote: the audit
  counted 9,455 twins in the morning [R25]; by execution time the
  count was 9,469 [R26] - 14 twins accreted in the interval, matching
  the measured regrowth rate. Both filed numbers are correct at their
  own timestamps.)
- Class B (resting exhaust): 1,701 tool rows from sessions ended
  before the cutoff, full-column copies staged before deletion.
- Safety: SHA-256 per quarantine shard, two-ID gated apply, crash
  sentinel, in-transaction recheck [R26].
- Result: 244.1 to 206.5 MB, 37.57 MB reclaimed by in-place vacuum;
  SQLite integrity_check ok; zero full-text-search ghost rows [R26].
- Restore under schema change: quarantine restored forward after a
  column was added; drill PASSED [R27].
- Security: 18-point audit; all runtime paths socket-free [R29].

The diet is the answer to "is it safe": removal is reversible by
construction, the reversal path is drilled, and the tool makes no
network calls [R27][R29].

## 6. Limitations

1. **One reference host.** The exact numbers (90.69 percent, 16.5M
   tokens, 431 rows/day) are one machine, one store, one month. The
   mechanisms are structural; the magnitudes are ours [R25a]. The
   external-validity program is the public receipt board: other hosts
   running the same census, cited as their receipts land (Section 7).
2. **Stores B and C are single-file samples with bands, not points.**
   JSONL stores resist exact token census; we state byte bands with
   declared assumptions (4 bytes per token for B, sensitivity shown)
   [R31][R33].
3. **One vendor row is symbolic.** No verified public Codex price list
   exists in our record; that row stays symbolic rather than guessed
   [R33].
4. **Worker verification certifies agreement, not correctness.** Blind
   lanes converge on arithmetic; both could share a wrong premise
   planted by the hub's brief. The R36 erratum shows the hub erring
   and the protocol catching it; it cannot prove brief-error
   impossible. Section 4 states the boundary; brief-poison testing is
   proposed future work [R24][R36].
5. **Prices move.** Vendor lists are dated to retrieval day; charges
   are recomputable from the formula and the stamped lists [R36].
6. **Filed-study errata carried forward.** R32's headline 27 percent
   static re-dump could not be reconstructed from its own itemization
   (itemized surface: 12.9-14.4 percent); the filed number stays
   quoted as UNRECONSTRUCTED and the itemized figures are used here
   [R33]. We do not silently edit filed studies.

## 7. Reproduction

The receipt is stranger-runnable: one command builds a deterministic
synthetic store, runs the real classifier against it, re-derives the
expected diet numbers, and exits RECEIPT-REPRO-OK. It runs in CI on
every push [R30]. The tools are stdlib-only Python, offline [R29]. The
full measurement record (27 studies: briefs, raw worker transcripts,
adjudications, errata) ships in the repository [R-INDEX]. The public
receipt board invites outside hosts: each external census becomes
cited evidence, addressing limitation 1 as receipts land.

## 8. Conclusion

Agent memory stores carry dead weight, and part of that weight is not
the user's fault: platforms persist model reasoning twice,
byte-identical, on every model that writes it - a schema defect, same
shape across models, fixable at the source for every user at once.
The usage-dependent remainder is measurable exactly where the schema
allows, and it has a computable transmission price: the carrying
charge, billed when a lapse re-injects stored context at full input
rate. The weight is removable reversibly, with drills and audits on
record, and it returns slowly enough that a schedule beats an
emergency. Memory hygiene is recurring maintenance with a computable
price. We release the census tools, the diet, and the full measurement
record so that the next store can be weighed before it is billed.

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
