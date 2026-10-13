# Sweeper: Research Log

Product thesis + lab notebook for paper #2. Every entry dated, every number
measured, nothing invented. Em-dashes banned per house law.

## 2026-10-13: R1b triage results (DeepSeek, 55s, needle-verified, citation-audited)

**Integrity gate passed:** all 19 arXiv IDs + all named titles in R1b output
verified present in the ledger the worker actually saw (zero inventions),
extended post-receipt to cover the build-order tail: View-oriented
Conversation Compiler, MemRefine, Mem2ActBench, DUET, MemLens, all in
ledger. Audit coverage now 100% of named citations.
and the three load-bearing cites spot-checked against live sources: A Survey
of Context Engineering (2507.13334) resolves on arXiv API with exact title;
Agentic Context Management (2607.21503) resolves on HF API + arXiv abs page
(its arXiv *API* record lags, logged as a known mirror-lag gotcha);
Compression Remembers the Detour resolves on OpenAlex (2026, DOI live).

**The must-read ten (per R1b, verified against ledger):**
1. 2507.13334 Survey of Context Engineering: the field map, borrow taxonomy.
2. 2607.21503 Agentic Context Management: closest framing (memory+cost as
   lifecycle), never builds the hygiene plane, differentiate head-on.
3. 2602.07398 AgentSys: host-plane vs context-plane hierarchy + secure
   deletion stance.
4. Compression Remembers the Detour (OpenAlex): lossy compression AMPLIFIES
   off-task content, the core motivation for distill-before-sweep.
5. 2601.18642 FadeMem: retention curves as seed of deletion semantics.
6. 2604.13725 compression effectiveness on repo tasks: backbone of our
   pre/post benchmark.
7. 2608.04569 Referential Dangling: hard compression leaves dangling refs,
   motivates provenance-preserving preservation (never amputate).
8. 2512.21567 Beyond Heuristics: decision-theoretic memory management,
   formal frame for our gated-cleanup approval loop.
9. LOCA-bench 2602.07962 + MemoryRewardBench 2601.11969: benchmark lane.
10. Billing-audit method (OpenAlex): invert it, audit LOCAL waste instead
    of vendor bills.

**Competitor map (from ledger's GitHub section):** (a) measure-only monitors
(splitrail 223 stars, usage analyzers), (b) single-CLI hacks (llm-cleaner,
ContextGc, pi-hermes-memory-cleanup), (c) memory systems without hygiene,
(d) no genuine overlap: nobody ships gated two-plane reclaim.

**Build order (R1b, ranked by leverage/effort):**
1. context-plane census hardening (measurement before destruction),
2. transcript GC prototype behind the R1b decision framework,
3. pre/post benchmark harness (2604.13725 + LOCA-bench methods),
4. preservation store with provenance + undo (the moat, after sweep proves
   value),
5. benchmark automation for paper time.
Safety invariant from R1b: measurement before destruction, every cleanup
move evidenced.

## 2026-10-13: R1 grind results (DeepSeek R1 + internet harvest)

**Harvest (real fetched metadata, all raw in research/raw/harvest/):**
271 records: arXiv 120 (10 queries), HF papers 80 (8 queries), OpenAlex 39
(4 queries), GitHub 32 (5 queries). Raw JSON preserved verbatim; digest and
R1b brief committed. S2 rate-limited (429) on first pass; OpenAlex used as
substitute. Ledger is append-only; nothing paraphrased into loss.

**Competitor scan verdict (GitHub section, 32 repos):** the itch is universal
(context cleaners, session cleaners, memory cleanups, one literally named
pi-hermes-memory-cleanup) but the field is shallow: monitors that only
measure (blitzclean 234 stars: macOS menu-bar stats; splitrail 223 stars:
token cost tracking), single-CLI hacks at 1-7 stars, memory systems without
hygiene. NOBODY combines host+context planes, gated reversible cleanup, and
distill-before-sweep. The monster seat is empty.

**DeepSeek R1 landscape verdict (34.5KB raw, needle-verified, worker ran its
own arXiv verification):**
- Closest cousin: MemGPT/Letta (arXiv 2310.08560): context as priced paged
  memory. Does NOT do: fixed-overhead composition audit, tool-exhaust share,
  dry-run+quarantine reclaim, host plane.
- Whitespace confirmed under-served: (1) per-call fixed overhead broken into
  system-prompt + per-tool schema bytes, priced; (2) tool-exhaust share of
  transcript bytes as a reclaimable-waste metric (our 85.4% headline);
  (3) gated, itemized, reversible reclaim of production conversation state.
- Transferable theory: mark-sweep roots law (McCarthy 1960) -> hard-deny set
  = reachable state; generational hypothesis (Ungar 1984) -> most context
  dies young, tenure transcripts by age; CCleaner trust loop (analyze, show,
  clean) -> our dry-run-first law.
- Novelty framing per R1: synthesis-and-application. Concede every component,
  own the composition + the gated-reclaim application. Pre-answer attacks
  6 and 10 (flagged by R1 as needing competitor re-verification).

**Research log law adopted:** worker outputs are raw evidence (kept whole in
research/raw/); only measured extractions enter this log, each tagged with
the raw file it came from.

## 2026-10-13: Founder reframe #3: the CCleaner analogy + Cognexia preservation layer

**Founder's restatement:** the basic idea is "something like CCleaner or disk
cleanup for AI models that are run on machines. There must be a shit ton of
potential for optimization, cleanup, summary, etc." And: use his memory
product Cognexia (github.com/nKOxxx/Cognexia, MIT, local-first SQLite +
Markdown, importance-scored memory cards, 37 REST endpoints, 183 tests) so
cleanup does not lose "vital or important information".

**What this changes in the design:**

1. The action triad is now ANALYZE / CLEAN / OPTIMIZE, where OPTIMIZE =
   summary + slimming, not just deletion. CCleaner's genius was the trust
   loop (analyze, show, then clean); sweap.it inherits that loop and adds a
   third C the disk world never had: distillation, because context waste is
   information, and information can be summarized instead of dropped.
2. Deletion semantics upgrade: nothing context-plane gets swept until a
   distillation pass offers to extract its vital content into Cognexia.
   "Archive, never amputate" (RQ2) now has a concrete substrate: memory
   cards with importance scores + provenance back to the swept artifact.
3. Trust architecture: Cognexia is 100% local (no cloud, no telemetry), so
   the combined product can honestly claim "nothing leaves the machine",
   matching sweapit's quarantine-first ethos.
4. Vendor-adjacency risk (logged for the paper): sweapit integrating only
   Cognexia looks self-dealing; design the preservation layer as a pluggable
   interface (Cognexia = reference adapter, others pluggable).

**Paper lineage sharpened:** paper #1 built the institution (hub, mandates,
measurement); paper #2 studies the metabolism of the machine itself (what
accumulates, what must be kept, what can be distilled, what must go) and
ships the janitor + the album (sweapit + Cognexia) as instruments.

## 2026-10-13: Name + v0.1.0

**Name (user decree): sweap.it.** Sweep + AI. Domain check via whois.nic.it:
`Status: AVAILABLE` (2026-10-13). Registration blocked by house no-purchase
law; founder to register. Repo dir renamed ~/sweap.it; binary `sweapit`.

**v0.1.0 shipped same day** (commit 8cbad4d): two-plane doctor + gated sweep.
Design semantics locked: **sweep defaults to dry-run; destruction requires
explicit --no-dry.** (Inverse of the usual CLI convention; for a product
whose job is deletion, the safe path must be the default path. Log this as a
product-law: "default to reversible".)

**First context-plane census results (this host, day 0):**
- Store-wide tool-output share of transcript bytes: **85.4%** (32.75M of
  38.36M chars, 36,810 messages). Paper #1 measured 75.6% on one hub session;
  the census says the infection is worse host-wide.
- Heaviest session: the paper #1 hub itself, 18.3 MB / 29,627 messages.
- Fixed prompt overhead confirmed: 28.7 KB system prompt; tool schemas
  54.3 KB (28 tools) ride every call.

**The one-line product pitch that fell out of the census:** "Your agent's
transcripts are 85% tool exhaust. sweap.it measures it, gates the cleanup,
and proves the reclaim."

## Research questions crystallizing (for paper #2)

- RQ1: What is the composition and growth law of LLM-stack waste, across
  hosts (host plane) and contexts (context plane)?
- RQ2: What deletion semantics are safe for conversation state? (Quarantine-
  before-delete generalizes to transcript GC: archive, never amputate; paper
  #1's INC-004 withdrawal doctrine is the same law applied to claims.)
- RQ3: Can an agent self-sweep without corrupting its own memory/instruments?
  (Our own incident log is the seed dataset.)
- RQ4: Does context-plane cleaning measurably change task performance? (Test:
  pre/post prompt-size, task success, token burn; the HF worker lane gives a
  zero-cost benchmark.)

## 2026-10-13: Founding

**Thesis (user decree):** build "Sweeper for LLMs", the way disk sweepers
cleaned PCs. Continuous agent use accumulates invisible waste; we measure it,
clean it safely, and the build process itself (thesis, measurements, design
decisions, dead ends, user corrections) becomes the next research paper.

**Lineage note:** the product concept emerged from our own pain. This Mac runs
a 24/7 Hermes agent (Telegram + CLI). The founder's review of the first
prototype script (sweeper.py, disk-oriented) triggered the reframe: the real
product is not "delete old files", it is context-economy hygiene for LLM
agents. Paper #1 (Agentic Institutions) measured delegation economics of a
hub; paper #2 measures the entropy of the hub itself and ships the cleaner.

## Baseline measurements (MacBitty, macOS 15.6, Hermes 1 session, 2026-10-13)

Captured via `hermes prompt-size` + `hermes sessions stats` + du/sqlite audits.
These are the paper's "day 0" figures for one host; multi-host census comes later.

| Quantity | Value | Instrument |
|---|---|---|
| Fixed prompt overhead per session | 83.9 KB total | hermes prompt-size |
| of which skills index | 14.5 KB | " |
| of which tool schemas | 54.3 KB (28 tools) | " |
| of which memory + user profile | 4.1 KB | " |
| Sessions | 143 (81 cli, 1 telegram, 61 age buckets in fs) | hermes sessions stats |
| Messages | 36,804 | " |
| state.db | 227.3 MB (+FTS index inside) | du + sqlite |
| Logs | 32 MB | du |
| Session jsonl | 16 MB | du |
| Stray screenshots at ~/.hermes root | 54 files, 16.8 MB | sweeper.py inventory |
| /tmp scratch (non-keep) | 3.4 MB visible; 6 zombie dirs >7d incl. system launchd sockets | sweeper.py dry-run |
| Ghidra download episode (one session) | 544 MB zip + 887 MB tree, deleted same day | session history |

**First observation (the dust metaphor, quantified):** a single active agent
month produced 36.8K messages and a 227 MB store, but the more interesting
number is the fixed overhead: every new session pays 84 KB before the first
user token, of which ~90% is tool+skills catalog. On a 200K-token context,
that is ~0.04% per session, small; but the same catalog rides EVERY API call
of EVERY turn. The LLM dust is not files, it is bytes that are re-paid on
every call (this echoes paper #1's re-payment law, nice continuity).

**Framing to develop (for the paper):** disk sweepers cleaned a scarce,
durable resource (bytes on disk). LLM sweepers clean a scarce, TRANSIENT
resource (context window), where waste has a per-call price and cleanup has
information-loss risk (compression = lossy sweep). Open problems we can
actually measure on ourselves: (a) context bloat census, (b) safe deletion
semantics for conversation state (what may be GC'd, what must persist),
(c) automated decluttering vs human-gated, (d) whether agents can self-sweep
without breaking their own memory (the INC-00x class of our own incident log
is the cautionary dataset).

## Design decisions (log as they happen)

1. **Thin over native first.** Hermes ships `sessions prune --dry-run`,
   `sessions optimize` (VACUUM), `checkpoints prune`, `logs list`. The product
   must not reimplement DB surgery; it orchestrates and reports. (Reinforced
   by user: "make sure to take notes as whilst building this", the tool's
   provenance and safety story matters more than its cleverness.)
2. **Inventory is the product's spine.** Sweep is the action layer; the
   manifest (what is waste, measured) is the sellable artifact, same as
   disk-sweeper "scan" screens were the UX.
3. **Report-only default.** Nothing auto-deletes until the operator says go.
   The founder's clarify-timeout during v0 planning confirmed: gating belongs
   to the human.
4. **Two planes:** (a) host plane, files, stores, logs (the v0 script);
   (b) context plane, prompts, toolsets, memory, transcripts (the product's
   actual differentiator). v0 was plane (a) only; the reframe moved the
   center of gravity to (b).
5. **Safety law inherited from paper #1:** no fabrication of recovered-space
   numbers; every claim measured; withdrawals chase every copy (INC-004
   doctrine applies to release notes, not just papers).

## Dead ends + corrections (kept for the paper's honesty section)

- v0 conflated "declutter my Mac" with "declutter the LLM stack". User
  corrected twice: it is a product, and it is for "LLM's usage".
- clarify() timeout on run-mode choice: the paper gets this as evidence that
  agent-initiated questions cannot block founder decisions; defaulting to
  report-only was the right fallback (write it up).
- ETH paper link (context management) unreachable (maintenance page) on
  2026-10-13; Substack piece retrieved (10,963 chars, prompt-engineering
  framing, in-context vs in-weight memory). Related-work triage logged.

## Next measurements queued

- Prompt-size census across sessions (how many distinct skills/toolsets were
  actually invoked vs carried).
- Transcript bloat: tool-output share of state.db messages (paper #1 measured
  75.6% on one hub session; census the whole store).
- Memory drift: chars in memory stores over time, duplicate/stale entries.
- Compression events: count + payload delta in this host's history (Hermes
  compactions are logged in-session).
