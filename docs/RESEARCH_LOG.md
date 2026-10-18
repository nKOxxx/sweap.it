# Sweeper: Research Log

Product thesis + lab notebook for paper #2. Every entry dated, every number
measured, nothing invented. Em-dashes banned per house law.

## 2026-10-13: R4C scope verdict: three variants priced, MVP defined, honest desirability

R4C report 10.4K chars, needle-verified, glyph-clean.

**What "optimize" means operationally (S1):** O1 dollar receipt (day one
measurable from user's own store; wallet saving realizes over weeks, felt
in the wallet), O2 smaller prompts (prune dead skills-index entries + call-
unused tool schemas; measurable day one on before/after pairs), O3 faster
sessions (real but milliseconds, not the selling point), O4 cleaner agent
memory (distill exhaust so context stops re-inflating), plus audit trail
and compliance-friendly reversibility.

**Scope variants (S2):**
- A context-plane only: census + cost card + distill + gated reclaim +
  benchmark harness. 8 weeks. Risk: distillation correctness + harness
  validity.
- B = A + the KEPT file-deletion option (host dust: old tmp, 54
  screenshots, dead logs; quarantine-first with restore, same manifest and
  benchmark gate). 10 weeks (A + 2). Mitigation is placement, not scope:
  lives behind the context plane, never leads messaging or first-run.
- C = B + memory-product consumer + fleet census/remote reclaim. 14-15
  weeks. Risk: fleet ephemerality (the CCleaner trap returns if hosts are
  throwaway) + diluted focus. Hard go/no-go at end of W12: if the fleet
  value case fails, C collapses to B with memory integration already
  shipped as an option. Salvageable B always exists at 12 weeks.
- File option placement: W6-W7 parallel slot of B, reuses reclaim+manifest
  primitives, benchmark-gated by the same harness, NEVER on the harness
  critical path. Amendment satisfied without touching the long pole.

**MVP + desirability (S3, pushback delivered as ordered):** MVP = A shaved
to its spine: one-command install, read-only census on the user's real
store, dollar cost card + waste map, ONE benchmark-verified gated
reversible reclaim with audit trail. File option stays in-codebase behind
a flag, not in the MVP install path. First-run pull ranking:
1. the dollar receipt on their own store (only specific, quantified, true
   pull; must never be inflated for light users),
2. the waste map (satisfying but diagnosis-only: the 234-star monitor
   class already ships it and gets abandoned),
3. reclaim-with-proof (where retention lives, but takes minutes, not
   first-five-minutes).
Honest pushback: organic pull is real but narrow and fragile; the only
self-evidently motivated persona is the PAID HEAVY AGENT OPERATOR who can
read their own dollar number. MVP must be tuned to that persona.

## 2026-10-13: R4B gate redesign: thresholds, product-led market gate, death schedule

R4B report 13.3K chars, needle-verified, glyph-clean. Founder's K2
(founder-personal outreach) replaced wholesale by product-led signals.

**Gate variants (strict / moderate / loose), R4B recommendations:**
- K1 token saving: strict >=20% + zero regression + 3 categories + 2 hosts;
  MODERATE recommended: >=15% reduction, <=3% quality tolerance, 2
  categories, reference host + 1 external re-run; loose >=10%/5%/1 host.
- K3 safety: strict = any single violation kills; moderate (recommended):
  kill only if reproducible AND executed (reached real artifacts); one-off
  aborts = logged findings, 1-week fix deadline.
- K4 REFRAMED from "fixed overhead minor" to "reclaimable share of bill"
  (fixed overhead + reclaimable tool-exhaust tokens vs real invoice):
  strict >=25%; moderate (recommended) >=15% or fixed-overhead >=10%;
  loose >=8%.
- K5 external reproducibility: strict 99% bit-exact; moderate
  (recommended) >=95% byte-identical with all divergence documented and no
  divergence flipping a safety verdict; loose >=90% decision-level.

**The committed market gate (replaces K2):** by end of P5, >=100 distinct
organic installers (registry-verified, deduped, bot-stripped) AND
activation >=40% (installer completes first successful census) AND
second-week return >=30% of completers. Kill: <25 installers, or
activation <30%, or return <15%. Why activation carries the gate: it
directly tests "a product people want to use and which actually optimises
their LLM setup", it is measurable as soon as the artifact is listed, and
it needs zero founder outbound. Stars are vanity, installs are attention;
activation converts attention into the core act.

**Death schedule (die cheap, die early):** K5 fires week 2 (snapshot
reproducibility, cheapest), K4 week 4 (tokenized invoice reconciliation),
market pre-signal week 7 (listing + early activation), K1 week 10
(benchmark), K3 + full market gate weeks 11-14. The two costliest phases
(P2 harness, P3 reclaim) are built ONLY after K5 + K4 + market pre-signal
all return continue. Worst case early death = two cheap-token phases, not
the full build.

## 2026-10-13: R4A Cognexia verdict: SKIP-BUILD-NATIVE (the ordered pushback)

R4A raw on disk, needle-verified, glyph-clean, no citations (none in brief).
Report 11.25K chars. The uncomfortable finding, delivered as ordered:

"Cognexia is a retention product, not a hygiene product. The conditions
that look like product gaps are not bugs in Cognexia, they are the entire
product domain of sweap.it."

- Fit: none of the accepted red-team conditions are native. Two that matter
  most (never-fetched cards must get swept; source stays quarantined until
  a human accepts) run COUNTER to Cognexia's retention design intent.
- Dependency risk: coupling the safety backbone to a single-maintainer
  product adds two-store consistency risk exactly where the guarantee must
  be strongest.
- Verdict: SKIP-BUILD-NATIVE. Backbone = native five-column card store
  (session id, byte range, checksum, card text, fetch counter) with the
  fetch counter and human gate as first-class schema, not conventions.
- Cognexia demoted to optional downstream consumer (Markdown views,
  importance-score priors), human-gated, fully removable without touching
  the guarantee. Its genuine value survives, out of the safety path.
- Flip conditions recorded: INTEGRATE-WITH-EXTENSIONS if provenance
  columns + per-card fetch logging + quarantine write mode land in
  Cognexia CORE; INTEGRATE (full) only if the fleet standardizes on it.

## 2026-10-13: Founder amendments to the R3 ruling (GO suspended, R4 set ordered)

Founder reviewed the GO+gates fork and amended, verbatim where quoted:

1. Cognexia must earn its place: "i would like to see that it makes sense
to use cognexia, otherwise, push back." R4A evaluates fit honestly; if it
does not make sense, the research must say so and propose the alternative.
2. Gate redesign ordered: "run another research deep seek set with several
R's concerning different gate thresholds, skip the buyer-outreach gate,
shrink scope..." R4B reworks K1-K5 with threshold variants.
3. K2 rejected as designed: "which buyer outreach? this is a product. we
will use other products/crm's for buyer outreach." Founder-personal cold
outreach is not a gate mechanism. Distribution is product-led and mediated
by other products, CRMs, marketplaces. R4B redesigns the market gate
around product-led signals.
4. Host plane file deletion KEPT: "there should be an option to delete old
or useless files, btw. lets not drop this." The R2 demotion stands (never
leads) but the capability is back in scope as an option. R4C prices it.
5. Product truth test: "we need to make sure that we build a product that
people will want to use and which will actually optimise their llm
setup." Desirability and measured optimization are the spine of R4C.

R4 set dispatched (serial, DeepSeek lane, needle-locked):
R4A Cognexia fit-or-pushback (integrate / extend / skip-build-native).
R4B kill-gate redesign (thresholds, product-led market gate, distribution).
R4C scope variants + MVP (context plane leads, file deletion kept as
option, what optimize means operationally, desirability).

GO ruling remains suspended until the R4 set is digested and presented.

## 2026-10-13: R3 synthesis: THE OVERVIEW (all six founder exit criteria closed)

R3 raw 19.2KB chars, needle-verified, zero invented citations (all 4 cited
IDs in-brief), zero glyphs. Disposition: GO, conditional, with kill gates.

**1. Landscape + status quo (criterion 1+2):** closed by R1+R1b+R2 waves:
nobody in the 271-record harvest combines snapshot census, measured
fixed-overhead economics, and reversible benchmark-verified reclaim.
Cousins mapped (MemGPT/Letta pages memory, monitors measure-only, 1-7 star
graveyard). The gap is demonstrated, not asserted.

**2. Technical setup (criterion 3):** seven components, ordered:
1a read-only snapshot census + SHA-256 manifest (substrate, self-sweep
paradox enforcement), 1b stored-bytes measurement (85.4% is a stored-bytes
fact, token share is v1.5), 1c fixed-overhead economics (the repitch,
97.7KB/call), then distillation with provenance, gated reclaim,
before/after harness, Cognexia consumer (optional, human-gated). Host
plane demoted to optional convenience, never leads.

**3. Plan + timeline (criterion 4+5):** 14 weeks, one founder + agent
workers. P0 w1-2 snapshot+census reproduction; P1 w3-4 token economics +
cost card; P2 w5-7 benchmark harness (the long pole, no sweep features
during); P3 w8-10 gated reclaim + provenance on sandbox; P4 w11-13
Cognexia integration + hardening; P5 w14 live opt-in deployment + paper
numbers. Paper spans P2-P5 as parallel payoff.

**4. THE VERDICT (criterion 6): GO, conditionally.** The facts rule out
only the host-plane CCleaner, which the plan abandoned. Conditional on:
benchmark phase as the committed kill-or-continue point, plus a live
willingness-to-pay check (cold outreach 10-20 agent-tool developers).
Kill criteria, any one stops the project:
K1 no reproducible token saving without quality regression on held-out set.
K2 no paying/pre-paying buyer or LOI-equivalent from cold outreach post-
   live-experiment.
K3 any safety failure in the wild: hard-deny violation or provenance
   checksum modified.
K4 fixed overhead turns out minor share of real bills once tokenized and
   reconciled against invoices.
K5 census not reproducible by a read-only external observer.

**Coverage audit (what could still move the verdict):** 4a tokenize ~20
real sessions for prompt-side share; 4b reconcile against real invoices;
4c snapshot robustness under concurrent writes; 4d competitor re-sweep
(fresh eyes, 2h); 4e (in raw); 4f cold buyer sample (the single most
verdict-moving activity). R3 recommends 4a+4b+4d+4f before/during P2.

**Founder rule requested:** accept the GO + kill gates, or override. Until
ruled, the project remains research-complete but build-unauthorized.

## 2026-10-13: Founder decree: scrap the prototype, research through to the overview

Verbatim: "why you building a prototype, before the research finished.
scrap the prototype. we are still in research phase and i want to make
sure that everything is covered. at the end of the research, we should
have an overview about landscape and status quo, the techincal setup,
plan, timeline, etc. and most importantly, if this project makes sense"

Actions: src/sweapit.py removed from HEAD (commit 118fb2d; recoverable
from history per our own default-to-reversible law). The v0.1.1 R2 fixes
are scrapped along with it; they live in git history if the build phase
ever resurrects the design. No more code until the overview is delivered
and the founder rules on go/no-go.

Research exit criteria (founder's list, binding):
1. Landscape, 2. status quo, 3. technical setup, 4. plan, 5. timeline,
6. THE VERDICT: does this project make sense.

R3 synthesis wave dispatched to close all six: brief carries only
verified measured facts (census numbers, harvest landscape, accepted
red-team verdicts, product laws) and demands technical blueprint,
phased plan with timeline, explicit go/no-go with kill criteria, and a
coverage audit listing what could still invalidate the verdict.

## 2026-10-13: R2 adversarial verdict (red-team landed, bruises converted to v0.1.1)

R2 raw 20.5KB chars (needle-verified). Sections: preservation-layer review,
fatal flaws, safety holes, measurement validity, RQ audit, self-sweep
paradox, verdict. The bruises, and what we did within the hour:

**F1 (existential, accepted):** the shipped host plane is commodity
(`find -mtime +delete` territory); the differentiator (context plane) is
roadmap. Response: R2 is right, host plane is demoted to "trust-building
surface", context plane becomes the product. This log entry IS the pivot.
**F2 (accepted):** the CCleaner frame is a doomed market analogy (disk is
disposable on fleets; the scarce resource is per-call-priced context).
Repitch on the re-payment law, keep CCleaner only as the trust-loop lineage.
**Safety holes (all three fixed in v0.1.1 same hour):**
- TOCTOU on keep-list: sweep now re-`lstat`s every target and compares
  (dev, ino) against inventory; identity change = SKIP, never delete.
- Symlink escape: `lstat` + `is_symlink()` everywhere; symlinks are
  unlinked as links, never traversed (`followlinks=False`, du uses lstat).
- Hardlink trap ("the fatal one", confirmed real: 3 of our zombie tmp dirs
  are nlink>1): hardlinked deletions report 0B truly freed and say so.
**Measurement validity (85.4% downgraded honestly):** chars != tokens;
stored bytes != prompt bytes (consumption path truncates old tool outputs).
Law adopted: the number is now quoted as "85.4% of STORED transcript bytes;
token share and prompt share unmeasured", and the tokenized re-measure plus
a real prompt-side capture are queued (census hardening, build order #1).
**RQ audit accepted:** RQ1 single-host composition = toy until time-series
+ cross-host; RQ2 (deletion semantics with a held-out-task oracle) = the
publishable core; RQ3 needs protocol separation (external verifier runs the
before/after task set, not the sweeping agent); RQ4 needs the frozen
frozen-snapshot benchmark harness BEFORE more sweep features.
**Self-sweep paradox (accepted, protocol designed):** census contamination
(the measurer writes to the store it measures), observer-as-subject,
selective reporting. Fixes: read-only snapshot at measure time (copy to
quarantine-side archive, measure the copy), external verifier for claims,
log laws above as pre-registration.
**Verdict's three fixes this week (adopted as the backlog):**
1. Repitch on fixed overhead re-paid every call (28.7 + 14.7 + 54.3 KB),
   demote 85.4% to a storage statistic.
2. Frozen-snapshot before/after benchmark protocol with held-out task set,
   before any more sweep features.
3. Cognexia integration: optional, human-gated, per-card provenance +
   checksum + byte-range, retrieval observability, zero-fetch cards get
   swept from the memory store too, and NO agent self-certification of
   "nothing vital lost" (external gate only).

**R-wave complete:** R1 landscape + R1b triage + R2 red-team, all
needle-verified, citation-audited, raw preserved. 3 dispatches, ~10 min
worker time, zero main-model burn.

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

## 2026-10-13 (late) - Persona Swarm R5: 100-persona resonance test (user-ordered)

**Instrument**: deterministic 100-persona corpus, 8 segments (S1 paid-heavy x14, S2 startup-platform x14, S3 indie x14, S4 enterprise x10, S5 eval-MLE x13, S6 agent-maintainer x8, S7 consultant x12, S8 adversarial-skeptic x15), generated from harvest-observed segments + R4C persona, NOT from our pitch (anti-MiroFish circularity law). Stimulus = fixed sweap.it pitch (census, dollar card, distill+gated reclaim, benchmark proof, optional file cleanup). 100 serial free-lane DeepSeek-V4-Flash dispatches, JSONL ledger + per-persona raws. All 100 well-formed, zero failures. Known deviation, logged not patched mid-run: template omitted the dispatch needle so every persona ran twice (acceptance grep failed; format-parse gate held 100/100); 2x free-lane seconds, zero data impact.

**Raw verdicts (hub recount from ledger)**: INSTALL 1, TRY 89, IGNORE 10, HOSTILE 0 -> install+try 90%. Resonance mean 57.3. Would-pay median $15; zeros 28/100.

**Analyst wave** (DeepSeek, 2m24s, needle SWEEPIT_SWARM, report at research/swarm/analyst_report.txt; one arithmetic slip in analyst prose corrected against ledger: 86% -> 90%):

- Segment pulls: paid-heavy 70.3 res / $25 median; enterprise 54.6 res / $60 median (top $500); startup $24.50; eval $25; maintainer 67.6 / $15; consultant $15; indie 57.3 / $5; skeptic 24.7 / $0 (10/15 IGNORE: the adversarial bloc worked).
- Monetizable core = enterprise + paid-heavy + startup + eval. Indie + skeptic = negative-ROI launch market.
- Objection clusters: (1) deletion/reclaim trust + reversibility 28, (2) reference-host numbers do not transfer 15, (3) build-it-myself cron+du 12, (4) wrong pain (forgetting not bytes) 12, (5) pocket change 12, (6) no-quality-loss unproven 9, (7) write path disqualifies 6, (8) two products one skin 4; residual vendor credibility 2.
- Dominant MISSING (55-60 of 100): run census + benchmark READ-ONLY on MY stores, show MY dollar number and MY losslessness before anything writes. Proven restore test (11), local/no-write mode (6), audit artifact (manifest/signed provenance) for clients/compliance.
- Bias audit: uniform 100% TRY in 7 of 8 non-skeptic segments, 1 INSTALL total, 0 HOSTILE = mode collapse toward the safe middle. One-step honesty haircut collapses install+try to 1%. Simulated intent cannot clear any market gate; it is a message/objection instrument only.

**Verdict (R5)**: GO-signal unchanged and still gated on real activation (>=40%, R4B). Swarm deliverables: pitch must lead with proof-on-my-stack read-only wedge (dollar card + losslessness on THEIR data, before any write); deletion trust is the #1 objection cluster and the file-cleanup option must stay quarantined-first and never lead; reclaim positioning = "prove lossless on your stack, then act", merging objection clusters 1+6 into the wedge itself. Target segments: paid-heavy operators + enterprise first.

**Artifacts**: research/swarm/{personas.json, persona_template.txt, analyst_brief.txt, analyst_payload.txt, run_swarm.py, swarm_ledger.jsonl (100), swarm_stats.tsv, raw/P001-P100_raw.txt, analyst_raw.txt, analyst_report.txt}; commits d62b7a1, 76c3354, + this one.

### R5 -> product deltas (PROPOSED, pending founder ruling)

1. First-run = proof run: census + YOUR dollar card shipped first; distill/reclaim behind the proof gate. 2. Per-host numbers only in pitch/onboarding (reference stats demoted to context). 3. `restore-test` as a shipped, self-enforcing gate: reclaim refuses to run until a real round-trip restore passes on that host. 4. Read-only default mode, write path opt-in and permission-separated. 5. File cleanup stays, deeper quarantined: separate subcommand, never in first-run, --files flag. 6. Packaging: free proof-run wedge; paid = reclaim + benchmark + audit bundle (manifest/signed provenance export, compliance demand); target enterprise/paid-heavy/startup/eval, price $20-30 pro. 7. Plan tension: losslessness proof needs the benchmark harness, so harness moves onto the critical path of the first PUBLIC artifact (launch wedge w4 = dollar card only, full proof wedge w8-10), or launch slips right. Unchanged: two-plane model, native card store, R4B gates (swarm clears nothing), death schedule, reversible-by-default.

## 2026-10-13 (late) - Tokenizer re-measure: token-shares EXACT (queued since R1b, closed)

**Gap closed**: R1b demoted 85.4% to a storage statistic with "token share unmeasured, tokenizer re-measure queued". Done today, two passes: (a) stratified sample (150 rows/class, seed 20261013, o200k_base, chars/token extrapolation) then (b) EXACT full-store count, every row.

**Results (exact, o200k_base, 37,813 rows, 353 sessions)**:
- tool-role content: 9,921,737 tok (54.48%)
- assistant tool_calls JSON: 6,593,594 tok (36.21%)
- assistant prose: 727,576 tok (4.00%)
- user content: 967,157 tok (5.31%)
- TOTAL: 18,210,064 tokens. **TOOL EXHAUST = 90.69% of stored TOKENS** (sample estimate 90.9%, validated to 0.2pp).

**Density finding (new, paper-grade)**: tool JSON tokenizes DENSER than prose (3.04 vs 4.10 chars/token), so exhaust token-share exceeds byte-share: 90.7% vs 89.1%. Compression-by-tokenization does not dilute the waste claim; it amplifies it.

**Longitudinal finding (new)**: exhaust byte-share rose 85.4% -> 89.1% as the store grew 38.4MB -> 59.8MB (143 -> 353 sessions) during the research period itself: agent-heavy usage compounds exhaust share over time. The store's own growth during this research is a natural-experiment row.

**Unchanged**: 97.7KB fixed overhead/call (28.7 sysprompt + 14.7 skills index + 54.3 tool schemas), re-paid every call.

**Artifacts**: research/tokenizer_remeasure.py, tokenizer_exact.py, tokenizer_remeasure_20261013.json (sample + exact), tokenizer_exact_out.txt. Commits: this one.

## 2026-10-14 - R7: independent hypothesis check (DeepSeek, blind)

Question from founder (plain): "can we use deepseek to run some numbers on our hypothesis?"
Dispatch: R7_hypothesis.txt -> deepseek, needle HYPOTHESIS-CHECK-OK, 850s budget, landed 78s.
Blind protocol: brief carried ONLY measured constants (A-E), no conclusions of ours.

Hub-side arithmetic audit: ALL CELLS REPRODUCED EXACTLY (H1 32,909.5 tok; 12/12 cost cells;
12/12 breakevens; H5 slope 0.1682%/MB -> 95.8% @100MB; H3 481.6 tok/msg). No corrections needed
(unlike analyst wave). Receipt: research/R7_hypothesis_report.txt.

Findings (all DeepSeek's, arithmetic verified hub-side):
1. Fixed overhead = ~32.9K tokens/call = 25% of a 128K window, 16% of 200K.
2. Dollar envelope: at P=$3/M, $60/mo enterprise WTP crossed at ~600 calls/mo; at P=$0.50,
   $25 crossed at ~1,500 calls/mo; at P=$0.15 the hypothesis weakens sharply ($15 needs ~3,000).
3. Store census understates billed flow: the 97.7KB overhead is ephemeral (never persisted),
   so wire-plane billing >> store-plane census. Two different quantities; do not conflate.
4. H5 projection: exhaust share -> 95.8% at 100MB (linear), but line hits 100% at ~125MB so
   trend must break; byte-share and token-share metrics must not be averaged.
5. ADVERSARIAL (material, accepted):
   A1 density misapplication: JSON density applied to prose-heavy sysprompt/skills; mixed-density
      recount ~29.1K tok (-12%); direction weakens, does not flip.
   A2 PROMPT CACHING (the sign-flip threat): cached prefixes bill at ~10x discount; if paperwork
      is cached it is the CHEAPEST content on the wire. Dollar card MUST read billed tokens
      (cached vs uncached) from provider ledgers, never list-price x bytes.
   A3 stored != billed; single-user dev store; WTP panel is soft signal (already labeled).

VERDICT: hypothesis PARTIALLY supported, conditional: holds for premium-model heavy users
(P=$0.50-3), weak for cheap-model light users. A2 upgrades the W5-8 harness requirement:
billed-token instrumentation with cache visibility is now mandatory for any dollar claim.
Product consequence: proof-run census stays valid (store-plane quantities are real), but the
dollar card's cost line must be built on billed tokens, or Caveman-style calculators become
the trap our own swarm rejected (fake numbers).

Repo: research/briefs/R7_hypothesis.txt, research/raw/R7_hypothesis_deepseek_raw.txt,
research/R7_hypothesis_report.txt (clean extract).

## 2026-10-14 - R8: scenario model (DeepSeek) - hypothetical team, efficiency + cost numbers

Founder ask: "hypothetical start and assumptions... what this could look like in terms of
numbers of efficiency increase and cost decrease." Construct: Team Kite, invented 4-person
startup; inputs tagged [ANCHOR]/[THEORY]/[ASSUMPTION]; all outputs stamped [HYPOTHETICAL].

VERIFIED NUMBERS (hub-side recount agrees with DeepSeek on every headline cell):
- Baseline: 3,000 calls/mo x 60,000 tok (33k anchored paperwork + 27k assumed history),
  blended list $1.25/M, cache multiplier 0.46 -> $103.50/mo, effective $0.575/M.
- I1 prune stale (12.2%): $90.83 (-$12.67). I2 cache layout h .60->.85 (48.9%): $46.40.
  I3 dedup calls -5%: FINAL $44.08/mo = -57.4% cost decrease.
- Efficiency: prefill/call 60,000 -> 52,656 (-12.2%); work-per-dollar 1.74 -> 3.40 M tok/$
  = 1.96x; effective price $0.575 -> $0.294/M.
- Ranking of savings: cache layout (I2) > pruning (I1) > dedup (I3). Product insight: the
  reclaim layer is primarily a CACHE OPTIMIZER, secondarily a deleter.
- Sensitivity (all levers live, corrected hub-side): A4 cache-hit rate dominates
  ($35.64-$136.94 across +-50%), then A2 history split ($35.86-$52.31). A5/A6 minor.
  Two cheap real measurements replace them: vendor billing API (cached-hit rate) + one
  real session dump (tokens/call + exhaust share).
- FALSIFIED IF: real re-sent context < ~10k tok/call.

DISCREPANCY LEDGER (verification worked both directions):
1. Hub recount v1 skipped stale factor -> wrong; DeepSeek's I1 (7,344 tok pruned) correct.
2. Hub work-per-dollar slip (2.23x) -> corrected 1.96x; DeepSeek's "roughly doubles" right.
3. DeepSeek S5 rows A5/A6/A2 used baseline m=0.46 despite "all three levers live" and its
   own formula (x0.235); also used unphysical e=1.275 (+50% exhaust = 127.5%). Corrected
   hub-side; top-2 ranking (A4, A2) unchanged under both readings.
Net: every published R8 number above is the hub-verified version.

Files: research/briefs/R8_scenario.txt, research/raw/R8_scenario_deepseek_raw.txt,
research/R8_scenario_report.txt. Proc: proc_360b8b77f354 (2m18s, deepseek, 850s budget).

## 2026-10-14 - R9: 10k question + delivery-path notes (DeepSeek) + billed-usage census (hub)

Founder ask: settle the 10k kill-condition (average/standard resend per call), note it,
and research how to deliver savings the way the compressor lane does (complementary).

A. DEEPSEEK RECALL NOTE (R9_notes.txt -> research/R9_notes_report.txt, all claims tagged):
- Plain chatbots: ~0.5-15k tok/call, median 3-5k [MED] -> below 10k floor, not the market.
- Coding agents: 15-80k, point est 30-40k mid-task [MED]; Alex Albert anecdote ~2M tok/
  20min session [MED/anecdote]. Fixed paperwork alone ~20-35k on serious stacks.
- Autonomous long-run: mid-run 40-120k [LOW-MED]; auto-compaction flattens the curve [MED].
- A4 verdict: >10k/call is the NORM for agent stacks; 60k heavy median plausible; kill
  check CLEARED; hedge = sample two deployed stacks.
- B1/B2: recommends path 1 first (read-only census CLI dollar card, billed tokens with
  cache visibility), path 2 (client-side cache-optimizer hook) as the savings lever;
  framework adapters weakest (churn, proxy-adjacent).
- B3 biggest risk: billing-surface fidelity (cache itemization across providers); cheapest
  test: reconcile independently-counted tokens against provider billed usage on ONE provider.

B. HUB-SIDE BILLED-USAGE CENSUS (the B3 test, run same day, provider-reported columns
   in state.db sessions: input_tokens, cache_read_tokens, api_call_count; 348 sessions
   with usage, 349 with api_call_count):
  glm-4.6 lane   62 sess, 10,080 calls: 28.3M uncached + 738.3M cache-read -> 96.3% hit,
                 resend/call avg 76,049, per-session median 41,052 (max 111,871)
  deepseek lane 269 sess,  1,697 calls: 127.9M uncached, cache-read 0 (lane reports none),
                 resend/call avg 75,343, median 24,512
  minimax lane    17 sess,     51 calls: 1.86M uncached, cache 0, resend/call 36,497
- FINDING 1: kill condition dead by measurement, not just recall. All three families
  re-send >>10k per call (medians 23k-41k; averages 36k-76k). Team Kite's 60k heavy
  median is inside the measured envelope (glm median 41k, avg 76k).
- FINDING 2 (new, material): cache hit rate is a PROVIDER LOTTERY: 96.3% (glm, automatic
  caching) vs 0% reported (Hyperfusion deepseek lane, minimax lane). Same workload, two
  lanes: one pays ~10% list on the re-send, the other pays full price every call.
  The wire-plane story is two-sided: store exhaust (90.69%) is real, but only cache-poor
  lanes pay full freight re-sending it. Product framing: measure your h, then improve it
  (R8's I2 lever has near-zero headroom on cached lanes, massive headroom on cache-poor).
- CAVEATS: single-user dev store; deepseek/minimax 0% may mean 'not reported' not 'not
  cached'; resend/call from session totals / api_call_count (approximation if retries
  counted). Still: provider-reported billed usage, not assumption.
- R8 addendum: FALSIFIED-IF line is measured-cleared (3 families, all >>10k).

Files: research/briefs/R9_notes.txt, research/raw/R9_notes_deepseek_raw.txt,
research/R9_notes_report.txt, research/billed_usage_census.txt. Proc proc_6159a9abc903.

## 2026-10-14: R11: sweep v1.1 shipped, hostile safety review applied, live store staged

GO received from user ("Formal GO: build sweep v1"). Built, reviewed, fixed,
demoed, staged. Commit chain this entry: see git log.

**Landscape (measured, live store):** 38,397+ messages, 40.8 MB content,
258.6 MB file. Dead rows (compacted=1 OR finalized session; active=0 is a
perfect mirror of compacted=1, 0 exceptions): 30,943 rows / 24.69 MB.
v1 targets TOOL rows only: 14,955 rows / 19.56 MB (48% of message content).
Protected classes: user+assistant prose (the mandate record, never touched),
live rows. token_count is NULL on every row (store never fills it).

**Wire honesty law enforced in code:** dead rows re-send nothing, so v1 wire
savings are stamped $0.00. v1 reclaims disk. v2 (live cache arrangement) is
where wire savings live; never conflate the two planes.

**sweep v1.1 mechanics:** dry-run census; quarantine (full-column copies,
8 SHA-256-hashed JSONL shards, manifest, store untouched); gated apply (id
typed twice; BEGIN IMMEDIATE; per-row dead-recheck including role inside the
transaction; schema-drift abort; crash sentinel state=applying before
commit); VACUUM INTO swap with measured before/after file size; FTS ghost
assertion (external-content fts5 delete-triggers verified, 0 ghosts);
restore (hash-verified, full-column, never duplicates).

**R10C hostile safety review (DeepSeek, 5m06s, 24 tool calls, ran its own
quarantine-apply-restore experiment on a copy):** 7 attack lanes + 3 extras.
Must-fixes all applied: (A1) staging was 9 columns, now schema-driven 23
(its own probe found 3 dead rows carrying effect_disposition; v1.1 restores
all 3, verified); (E1) copy verification was count-only with dead
byte-parity code, now per-shard SHA-256 verified before apply and restore;
(A6/A7) the file did not shrink without VACUUM (verified 0 bytes) and the
48% content-share read as a disk claim, now VACUUM INTO swap + measured
file deltas + explicit content-vs-file separation. Refuted by evidence:
FTS ghost fear (delete triggers fire; verified 0 ghosts post-apply), race
TOCTOU (BEGIN IMMEDIATE covers recheck+delete), gate bypass (none).

**Demo, end to end, on a copy:** quarantine 14,955 rows / 23 columns, apply
(-23.58 MB file, measured), integrity ok, restore, FULL-COLUMN round-trip
14,955/14,955 identical including the 3 effect_disposition rows.

**Live store status:** quarantined as q_20261014_191532 (28.89 MB staged,
8 shards hashed, row parity PASS). Store UNTOUCHED. Apply (and its 23 MB
disk reclaim) waits for a quiet moment: the store must not be mid-write;
instrument-frozen law applies to surgery, not just measurement.

## R12 (2026-10-15): Caveman growth & GTM post-mortem (user-requested, DeepSeek-analyzed)
- Question: how did caveman.so go from zero to 111,865 stars in 6.5 months, and what transfers?
- Primary harvest (hub, verified): research/raw/R12_gtm_timeline_verified.md (GitHub API,
  HN Algolia, README raw; all dates UTC-checked).
- Analysis: DeepSeek-V4-Flash free lane, proc_67372abca73b, 84s, needle R12-GTM-OK,
  8/8 hub spot-checks PASS. Report: research/R12_gtm_report.txt; raw: research/raw/.
- Findings: Day-2 HN 904pts by stranger submitter; founder restraint load-bearing;
  third-party benchmark wave months 3-4 (testability was seeded, not validation);
  August skeptics wrote the October product spec (warm cache); monetization only at
  month 6 (joke is the funnel, infrastructure is the business); 6 flywheels; 7 ranked
  transferable moves. Sweap relevance: receipt-as-demo mirrors phase 0-1 mechanics;
  our falsifiable number = 90.69% exhaust; monetize only after measured proof.

## Repo presentation pass (2026-10-17): the corpus gets a front door

Question: does the repo read as a body of work or a lab drawer? Bar: the
craft level of the best research repos in our radar lane.

Round 1 (DeepSeek, proc_869783855a40, 1m38s, needle REPO-PRESENTATION-AUDIT-OK):
- Scores 8-9 across 7 dimensions; traits T1-T10 mostly PRESENT.
- One worker error caught on recount: called the index table "16 numbered
  rows"; it has 25 (its own prose said "25-study corpus" twice).
- Weakest-element call verified real: every headline number is one machine,
  recounted by the same hub that measured it ("a self-handshake").
- Top-5 must-fixes all applied: (1) scripts/repro_receipt.py - synthetic
  deterministic store, real cli/diet.py classifier, 9/9 checks green twice,
  RECEIPT-REPRO-OK; planted divergent pairs prove the overreach tripwire
  fires. (2) Requirements + backup warning in README. (3) Proof-table cells
  now anchor to their own receipts (90.69% -> R7, $0.49 -> R28, 37.57 MB ->
  R26). (4) docs/CHANGELOG.md + "figures current as of" stamp. (5) Status
  rewritten: names the one missing proof layer (independent reproduction on
  a store we do not own) and what flips the repo public.
- Bonus surfaces: SECURITY.md, CONTRIBUTING.md, AGENTS.md,
  receipt_discrepancy issue template, CI workflow receipt_repro.yml.
- Hub-side own-goal caught pre-audit: CONTRIBUTING briefly said AGPL-3.0;
  LICENSE on disk says Apache-2.0. Fixed before the round-2 dispatch.

Round 2 dispatched blind (new needle REPO-PRESENTATION-AUDIT-R2-OK) on the
fixed files; recount owed on return.

### Repo presentation pass, round 2 (2026-10-17): the auditor bites back

Round 2 (DeepSeek, proc_979a6dd85753, 1m46s, needle REPO-PRESENTATION-AUDIT-R2-OK,
fresh blind brief on the FIXED files incl. repro script + changelog):
- Scores dipped where they should (evidence 7, navigation 7): the loop works.
- Worker catch verified real and it was a HUB slip: changelog 0.2.0 said
  "90.69% now cites R25a" while the README linked R7; both wrong per our own
  verification. Fixed: the cell now points at the exact census artifact
  (research/artifacts/tokenizer_exact_out.txt, holds both 90.69 and 37,813),
  changelog reconciled.
- $0.49 labeled "suggestive model" in the proof table (R28's own word;
  measured/hypothetical no longer share a slot unlabeled).
- R10/R11 numbering gap explained in INDEX (shipped as code, retired numbers).
- research/artifacts/README.md added: full JSON schemas + provenance note;
  hub own-goal caught in review (claimed a production date the artifact does
  not carry; corrected to the log reference).
- DECISIONS.md + STORY.md now linked from README "For the thorough".
- Verification floor upgraded: repro_receipt.py is the test (CI-enforced),
  stated in CONTRIBUTING + AGENTS.
- Plain "what it does" line added under the README tagline.
- Hygiene pre-commit catch: 2 tracked .pyc files + no .gitignore; fixed.
- Left as filed: 5 em-dashes inside R31's verbatim worker transcript
  (verbatim law; hub-authored files all clean).
- Worker gap NOT acted on: "resolve the private-status blocker" - going
  public is the founder's call, gated on the external reproduction; Status
  already says exactly that honestly.

Loop verdict: round 2's remaining must-fix list is empty of presentation
items; the one substantive demand (independent reproduction on a store we
do not own) is the same external proof layer already named in Status.
Presentation bar reached by the audit's own rubric; the gate that remains
is evidence, not craft.

## 2026-10-18: R33 - the carrying charge, per vendor (user ruling: "for each model the % and also the saving")

Trigger: user asked why the README shows one 90.69% when Hermes used to
read 96-98; answered with the two-rulers law (cache hit rate vs dead-weight
share, neither averaged into the other), then ruled "for each model the %
and the saving; we proved 49c for Hermes, do the same for Claude and
Codex". User further decreed: "use deepseek and the other one as much as
possible to get the data."

Brief: blind, measured constants + public list prices only
(research/briefs/R33_carrying_charge_brief.txt). Worker: DeepSeek
(proc_b8e35e389586, 2m02s, needle R33-CARRYING-CHARGE-OK last line).
Hub recount: pre-registered anchors computed BEFORE reading worker output;
all arithmetic verified exact (charges $0.49/$2.70/symbolic; A savings
$8.09; B band $0.051-0.155 at 4 B/tok with 3/5 B/tok sensitivity).

Findings (research/R33_carrying_charge/ANALYSIS.md):
- Charge per 1M junk tokens per lapse: Hermes $0.49, Claude Code $2.70
  (5.5x - expensive models pay more for the same forgetting), Codex
  unknown (no verified public price; symbolic).
- Per lapse on the measured stores: Hermes $8.09, Claude ~$0.05-0.17,
  Codex 0.004-0.006 x price-delta.
- Read-across law: the three dead-weight shares are different constructs
  (stored-token census / dedup band / proven-dup + static surface); the
  comparable number is the charge per 1M junk tokens, not the store totals.

Ledger: one input problem inherited from filed R32 - its "static re-dump
27%" headline cannot be reconstructed from its own itemization (6 x 4,124 B
= 14.4% of 172,360 B; constant part 12.9%). Not a worker error (it used the
anchored headline mechanically); not silently edited (filed studies stay as
filed); R33 C-rows use itemized bytes, 27% marked UNRECONSTRUCTED. R32
erratum = founder's call.

Research law: nothing promoted to site or README; founder gates that.

### R33 annex (same day): DeepSeek + MiniMax at public list prices

User ruling: "Can we just use the public data for deepseek and minimax."
Official price lists fetched live 2026-10-18 (api-docs.deepseek.com,
platform.minimax.io), applied to OUR per-lane measured volumes from the
filed census (2026-10-14). Hub assembly, no workers.

- Charges per 1M junk tokens: DeepSeek flash $0.147 off-peak / $0.294
  peak; MiniMax M3 $0.24 (50%-off pricing; $0.48 at list).
- Our free-lane reality stated in the annex: both lanes measured 0.0%
  cache hit (permanently lapse-priced); billed $0.00 to us; all dollar
  figures are comparison prices at list, not bills paid.
- Completed charge row: glm-4.6 $0.49 | Sonnet-class $2.70 | DeepSeek
  $0.147-0.294 | MiniMax $0.24 | GPT-6.1-Sol unknown.
- Founder ruling on stamps (2026-10-18): official published prices are
  on point; R33 carries no [THEORY]/[ESTIMATE]/[HYPOTHETICAL] tags. The
  facts that matter are stated plainly: prices are the vendors' official
  lists (retrieved 2026-10-18), our lanes paid $0.00, and Codex has no
  public price list. prices.json untouched.
- Founder-approved description of the numbers (2026-10-18): "based on
  calculations and official information/data" - this line is now the
  official sourcing statement at the top of R33 and applies to any
  public use of the table (site, posts, README) when the founder opens
  publicity.

### R33 table LIVE on sweap.it (founder gate opened)

2026-10-18: founder approved publishing the per-vendor carrying-charge
table on the site. Deployed to nKOxxx/sweap-it-site (Pages, sweap.it),
rendered inside the existing price-board section, v7 styles unchanged.
Sourcing line as ruled: "based on calculations and official information/
data." Numbers identical to R33 in this repo: Claude $2.70 | GLM-4.6
$0.49 | MiniMax $0.24 | DeepSeek $0.15-0.29 | Codex n/a. Research-law
note: this is the first research-derived table on the site, published
by explicit founder decision.
