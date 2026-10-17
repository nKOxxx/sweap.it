# R30: trim-1 vs sweap.it competitive analysis (2026-10-17)

Method: blind brief -> DeepSeek worker (hf_dispatch, needle-gated, 1m47s) -> hub recount.
Hub recount: timeline deltas recomputed exactly (12h45m49s work-start lead; 51h47m32s their-public-presence lead); cadence gaps verified (26/13/10 days); all table cells traced to tagged facts. One worker typo fixed ("folds closed" -> "fails closed"). Positioning lines rewritten hub-side to keep the brand spelling (sweap, not sweep).

Verdict: different layers, complementary. Falsifiers on file (section 6).

---
(verbatim worker analysis below)
ROLE: You are a competitive-intelligence analyst. Work ONLY from the 
facts in this brief. You have no browsing. Where a fact is missing, write 
UNKNOWN - never invent.

CONTEXT: Two tools both reduce AI-agent token waste, but they may operate on 
different layers. A founder needs (1) a precise technical differentiation, (2) 
an honest numeric comparison table for a public website, (3) a verified timeline
comparison, (4) draft social posts. Everything you output must be grounded in 
the tagged facts below or clearly marked [THEORY]/[ASSUMPTION]. Honesty law: 
NEVER write past-tense savings claims like "saved $X" for future users; only 
measured facts about what already happened on one machine, labeled as such.

=== FACTS: sweap.it (our product) [ANCHOR unless noted] ===
- Layer: the agent's PERSISTENT MEMORY STORE (SQLite conversation/state database
on the user's machine).
- Mechanism: weigh (read-only census) -> diet (find duplicate thinking blobs 
stored twice per schema + resting tool exhaust rows; quarantine-then-apply; 
reversible; zero info loss) -> keep-it-off (daily watcher that flags regrowth; 
flags, does not prevent).
- Measured on ONE machine (the founder's), dated 2026-10-17: store 244.1 MB -> 
206.5 MB; 37.57 MB removed; 9,469 duplicate thinking-blob rows + 1,701 tool rows
= 11,170 rows touched; 0 bytes of memory content lost; fully reversible from 
quarantine.
- Claim wording: "On the tested store schema, every thinking blob was stored 
twice, across all models tested: 9,456 rows, 26 MB." (store-specific claim, not 
universal)
- Lapse-cost math [THEORY, derived from published token mechanics + our measured
split]: when an agent's context lapses (compaction/session break), the 
persistent pile is re-read; on our machine 49% of paid uncached tokens were 
break re-reads (measured, one host, frozen blind audit). Cache-hit tokens are 
cheap; uncached re-reads are full price. Published price ratio observed: cache 
miss vs cache hit ~5.45x for one frontier model family (prices.json: $0.60/M 
uncached vs $0.11/M cached per 1M; $2.20/M output). Lapse Price: $0.49 per MB 
per lapse (derived: ~0.85 MB text per MB stored x $0.60/M uncached x re-read 
fraction). Illustrative table: 5 MB junk -> $2.06 per lapse; 20 MB -> $8.23; 50 
MB -> $20.58. Weekly-lapse column (~x4) is ILLUSTRATIVE.
- Form: local CLI, zero dependencies, works on one store schema family today. 
Private repo while pre-launch.
- Repo: first commit 2026-10-13 14:19:38 UTC. Public site: sweap.it (DNS flip in
progress). Team: founder + AI agents, 4 days old.
- License: AGPL planned for core.

=== FACTS: trim-1 (competitor, caveman-ai org) [THEORY: quoted from their public
README and GitHub API, 2026-10-17] ===
- Repo github.com/caveman-ai/trim-1: created 2026-10-14 03:05:27 UTC, last push 
2026-10-14 17:34 UTC, 127 stars, 12 forks, Go, Apache-2.0, desc: "a 1.2 MB model
that keeps the lines of a context an AI agent needs".
- Mechanism per README: gradient-boosted trees (712 trees, NOT a neural net), 
1.2 MB embedded model; given (context, query) it decides which LINES of that 
context the agent needs, returns the context's own lines in original order with 
removal markers; never rewrites lines; deterministic; 7 ms per 5k tokens on one 
CPU core; no network call; pure Go stdlib.
- Per-request tool: `trim --query "why does the build fail" build.log`. Three 
cut levels: conservative/balanced/aggressive.
- Fails closed (returns context unchanged) when: query blank; context < 2,000 
bytes; context > 8 MiB or 200k lines; cut would remove < 10% of bytes.
- Self-stated scope limit per their README: "Long-document retrieval is what 
trim-1 is for... Coding-agent tool outputs are short and dense. Stay at balanced
or conservative and expect small savings."
- Ecosystem: part of Caveman (github.com/JuliusBrussee/caveman; their site 
claims 113k GitHub stars [THEORY, self-reported]). Caveman's other repos: 
agent-sdk (created 2026-08-26), router-client (2026-09-21), blocks (2026-10-04, 
48 stars), trim-1 (2026-10-14). Cadence: new repo roughly every 2-3 weeks since 
late August.
- What trim-1 does NOT touch, per README: persistent storage. It reads a 
context, returns a trimmed context; it never writes to any store, dedups 
nothing, keeps nothing off.

=== TASKS ===
1. DIFFERENTIATION: In plain words, what layer does each tool operate on, when 
does each act (per-request vs persistent), and what does each leave behind? 
Include: reversibility, information loss profile, failure modes, and what each 
tool can NEVER do that the other can. Answer whether a user could want both (do 
they compete, complement, or stack?). Consider honestly: could trim-1's approach
be extended to absorb sweap's job, and vice versa - what would each need to 
build?
2. TIMELINE VERIFICATION: Recompute from the raw timestamps (do not trust my 
subtraction): our first commit 2026-10-13T14:19:38Z vs trim-1 repo creation 
2026-10-14T03:05:27Z. Report hours+minutes. Also place trim-1 in caveman's repo 
cadence. State plainly who started first and by how much, and who is shipping 
faster now.
3. NUMERIC TABLE for a public website: 6-8 rows, 3 columns (dimension | sweap.it
| trim-1). Rows like: layer acted on, when it acts, unit of work (what it 
removes/trims), information loss, reversibility, footprint (model size / deps), 
measured result (ours: real numbers labeled one-machine; theirs: published 
claims labeled as their claims), license. Every cell must be traceable to the 
facts above; tag cells  /  /  / . No invented numbers.
4. POSITIONING LINES: 3 one-liners for the site section that position sweap 
honestly AGAINST/ALONGSIDE trim-1 without disparagement (joke on us or the 
situation, never on them as liars). Respect: "sweap, not sweep, the typo is the 
brand".
5. POSTS: One LinkedIn post (120-180 words) and one X post (<280 chars), founder
voice, grounded ONLY in verified numbers: we committed first by ~13 hours, both 
tools shipped within 24h of each other, different layers, the space is hot 
(their org: 113k-star parent, 4 repos in 7 weeks). Honest, punchy, no past-tense
savings claims, no trash talk. End each with a hook question.
6. FALSIFIED IF: For the central claim ("trim-1 and sweap operate on different 
layers and are complementary, not substitutes"), state the observation that 
would falsify it.

OUTPUT FORMAT: Sections 1-6. Final line, exactly: TRIM-VS-SWEAP-ANALYSIS-OK

=== AMENDMENT: SECOND TIMELINE CLOCK [ANCHOR] ===
- Our first COMMIT (local git history): 2026-10-13T14:19:38Z. Our GitHub repo 
created (public presence): 2026-10-16T06:52:59Z (we built locally ~2.5 days 
before pushing).
- trim-1: repo created 2026-10-14T03:05:27Z, last push same day 17:34 UTC 
(built+shipped in ~14 hours), 127 stars within 3 days.
- For task 2: compute BOTH comparisons honestly - (a) first-commit vs 
repo-creation: who started work first, by how much; (b) repo-created vs 
repo-created: who was on GitHub first, by how much. State both without spin. The
social posts must survive a hostile reader checking dates: use only defensible 
phrasings (e.g. "first commit predates their repo by 13 hours; their repo 
predates ours by 2 days; both tools landed within 4 days of each other").
Initializing agent...
────────────────────────────────────────


╭─ ⚕ Hermes ───────────────────────────────────────────────────────────────────╮
    TRIM-VS-SWEAP ANALYSIS (grounded only in the tagged facts; missing facts
    marked UNKNOWN)
    
    ═══════════════════════════════════════════
    1. DIFFERENTIATION
    ═══════════════════════════════════════════
    
    LAYER THEY OPERATE ON
    - sweap.it works on the agent's PERSISTENT MEMORY STORE: the SQLite
    conversation/state database sitting on the user's machine. It is about
    what is stored across sessions. [ANCHOR]
    - trim-1 works on the IN-CONTEXT TOKEN STREAM produced per request: given
    (context, query) it picks which LINES the agent needs. It is about the
    live context handed to the model in one call. [their published claim]
    
    WHEN EACH ACTS
    - sweap acts DISCRETELY and ASYNCHRONOUSLY: census (weigh) -> diet
    (removal) -> keep-it-off (a daily watcher that flags regrowth). Not in
    the per-request path. [ANCHOR]
    - trim-1 acts PER-REQUEST and SYNCHRONOUSLY: run the CLI on a context,
    get a trimmed context back in ~7 ms per 5k tokens. It is an in-line
    filter at call time. [their published claim]
    
    WHAT EACH LEAVES BEHIND
    - sweap leaves a smaller store, with everything it removed sitting in a
    quarantine it can restore. Persistent side effect; reversible. [ANCHOR]
    - trim-1 leaves NOTHING behind: it never writes to any store, dedups
    nothing, keeps nothing off. Purely functional per-call output. [their
    published claim]
    
    REVERSIBILITY
    - sweap: fully reversible, quarantine-then-apply. One explicit restore
    path. [ANCHOR]
    - trim-1: nothing is written, so there is nothing to "undo" ;  a given
    call deterministically returns the same trimmed context, and you simply
    don't have to use it. Different notion of reversibility (statelessness
    vs. restorable mutation). [their published claim]
    
    INFORMATION-LOSS PROFILE
    - sweap: zero information loss on the memory store. 9,469 duplicate
    thinking-blob rows + 1,701 tool rows = 11,170 rows touched; 0 bytes of
    memory content lost. It removes things stored TWICE (duplicates), not
    unique content. [measured, one machine]
    - trim-1: lossy BY DESIGN ;  it removes lines (marked with removal
    markers) to shorten the context you feed the model. It never rewrites
    lines, but it does withhold lines. Directionally the opposite trade:
    sweap de-duplicates to zero loss; trim-1 intentionally drops low-value
    lines. [their published claim]
    
    FAILURE MODES
    - sweap: fails safe and reversibly; the failure to watch for is
    mis-identifying a non-duplicate as removable, which quarantine +
    reversibility make recoverable. [ANCHOR]
    - trim-1: fails CLOSED ;  returns context unchanged when query is blank,
    context <2,000 bytes, context >8 MiB or 200k lines, or when the cut would
    remove <10% of bytes. Also self-avoids coding-agent outputs: "stay at
    balanced or conservative and expect small savings." [their published
    claim]
    
    WHAT EACH CAN NEVER DO (today)
    - sweap CANNOT trim a single live request in real time. It has no in-line
    per-call mechanism; it is a store-hygiene pass, not a token filter.
    [ANCHOR]
    - trim-1 CANNOT touch persistent storage: it reads one context and
    returns one trimmed context. It cannot dedup across sessions/history,
    cannot remove what's stored twice on disk, and cannot keep regrowth off
    the store. [their published claim]
    
    DO THEY COMPETE, COMPLEMENT, OR STACK?
    They COMPLEMENT and can STACK. Different layers (store vs. context),
    different timing (async maintenance vs. per-request), different loss
    profiles (zero-loss dedup vs. intentional line-drop). A user could
    plausibly want both: sweap keeps the persistent pile lean so the store
    doesn't tax every re-read; trim-1 trims the live context of the current
    call. They are in adjacent but distinct price layers of the same waste
    problem.
    
    COULD EACH ABSORB THE OTHER?
    - Could trim-1 extend to absorb sweap's job? It would have to build, from
    scratch: persistent-store schema parsing for a specific DB family,
    cross-session duplicate detection, a quarantine + restore mechanism, and
    a regrowth watcher. Its current mechanism (a 1.2 MB line-selection model
    over one context) gives it none of the store-awareness that job requires.
    Big jump; not a trivial bolt-on. [THEORY/ASSUMPTION ;  inference from
    stated scope]
    - Could sweap extend to absorb trim-1's job? It would have to build a
    real-time, query-conditioned, line-level selection engine with sub-10 ms
    latency and a decision model (their approach uses 712 gradient-boosted
    trees, not a neural net) ;  a fundamentally different mechanism from
    deterministic dedup of a DB. Same story: buildable in principle, absent
    today, different skillset. [THEORY/ASSUMPTION ;  inference from stated
    scope]
    
    ═══════════════════════════════════════════
    2. TIMELINE VERIFICATION (recomputed from raw timestamps)
    ═══════════════════════════════════════════
    
    Comparison (a) ;  WORK START: our first commit vs trim-1 repo creation
    - Our first commit:     2026-10-13T14:19:38Z
    - trim-1 repo created:  2026-10-14T03:05:27Z
    - Delta: exactly 12 h 45 m 49 s
      (10-13 14:19:38 -> 10-14 00:00:00 = 9h 40m 22s; + 00:00 -> 03:05:27 =
    3h 5m 27s; total 12h 45m 49s)
    - PLAIN: Our first commit PREDATES trim-1's repo creation by 12h 45m 49s
    (~13 hours). Founder started work first.
    
    Comparison (b) ;  PUBLIC PRESENCE: repo-created vs repo-created
    - Our GitHub repo created:  2026-10-16T06:52:59Z  (note: we built ~2.5
    days locally before pushing)
    - trim-1 repo created:      2026-10-14T03:05:27Z
    - Delta: exactly 51 h 47 m 32 s
      (10-14 03:05:27 -> 10-16 03:05:27 = 48h; + 03:05:27 -> 06:52:59 = 3h
    47m 32s; total 51h 47m 32s ≈ 2.16 days)
    - PLAIN: trim-1 was on GitHub FIRST by 51h 47m 32s (~2.2 days / ~2 days
    3h 48m). Their repo predates ours.
    
    PLACEMENT IN CAVEMAN CADENCE
    Reported repos: agent-sdk (2026-08-26), router-client (2026-09-21),
    blocks (2026-10-04), trim-1 (2026-10-14). Gaps: 08-26→09-21 = 26 days;
    09-21→10-04 = 13 days; 10-04→10-14 = 10 days. trim-1 fits the announced
    "roughly every 2-3 weeks" cadence but is the TIGHTEST gap of the four (10
    days) ;  an acceleration, not a break in cadence. [derived from raw repo
    dates]
    
    WHO STARTED FIRST / WHO SHIPS FASTER ;  NO SPIN
    - Who did the WORK first: us, by 12h 45m 49s (our first commit predates
    their repo).
    - Who was PUBLIC first: them, by 51h 47m 32s (their repo predates our
    GitHub repo).
    - Who ships faster NOW: For sweap, UNKNOWN beyond the founder's
    local-first cadence (4 days old, private pre-launch). For caveman,
    observed cadence is a new repo roughly every 2-3 weeks with the last gap
    at 10 days, and trim-1 itself shipped (build + first push) within ~14h on
    a single day (created 03:05:27Z, last push 17:34Z). UNKNOWN who maintains
    the faster tempo over the next sprint; both are early.
    
    DEFENSIBLE PHRASTRING FOR PUBLIC (survives date-checking):
    "Our first commit predates their repo by ~13 hours; their repo predates
    ours by ~2 days; both tools landed within a 4-day window of each other."
    
    ═══════════════════════════════════════════
    3. NUMERIC TABLE FOR PUBLIC SITE
    ═══════════════════════════════════════════
    
    dimension            | sweap.it                                          
     | trim-1
    ---------------------+------------------------------------------------------+-----------------------------------------------
    Layer acted on       | Persistent memory store (agent's local SQLite     
     | In-context token stream (the lines of one
                         | conversation/state DB) [anchor]                      | context per request) [their published claim]
    When it acts         | Discrete maintenance runs + a daily watcher; not      | Per-request, synchronously (~7 ms per 5k
                         | in the request path [anchor]                          | tokens on 1 CPU core) [their published claim]
    Unit of work         | Removes duplicate thinking-blob rows (9,469) +        | Returns the context's own lines in original
                         | tool-exhaust rows (1,701) = 11,170 rows              | order with removal markers, 3 cut levels
                         | [measured, one machine]                               | [their published claim]
    Information loss     | 0 bytes of memory content lost [measured,            | Lossy by design: lines are removed from the
                         | one machine]                                          | returned context [their published claim]
    Reversibility        | Fully reversible from quarantine (quarantine-then-   | None needed ;  never writes to any store;
                         | apply) [anchor]                                       | deterministic per-call trim [their published
                         |                                                       | claim]
    Footprint / deps     | Local CLI, zero dependencies, one store-schema       | 1.2 MB embedded model (712 gradient-boosted
                         | family today [anchor]                                 | trees); pure Go stdlib; no network [their
                         |                                                       | published claim]
    Measured result      | 244.1 MB -> 206.5 MB; 37.57 MB removed;              | 7 ms per 5k tokens; folds closed on small/
                         | 9,469 dup blob rows + 1,701 tool rows; 0 B lost.     | huge/short-cut contexts; small expected
                         | One machine (founder), 2026-10-17                    | savings on coding-agent outputs [their
                         | [measured, one machine]                               | published claim]
    Failure mode         | Fails safe; cascade risk is mis-flagging a non-dup,   | Fails closed: returns context unchanged on
                         | recoverable via quarantine [anchor]                   | blank query / <2,000 B / >8 MiB or 200k
                         |                                                       | lines / cut <10% [their published claim]
    License              | AGPL planned (core) [anchor]                          | Apache-2.0 [their published claim]
    
    All numbers are traceable to the listed facts. No invented figures;
    anything not stated is UNKNOWN.
    
    ═══════════════════════════════════════════
    4. POSITIONING LINES (honest, no disparagement)
    ═══════════════════════════════════════════
    
    1. "sweap keeps the pile on disk lean, so every re-read is cheap; trim-1
    keeps the current call short. Different floors of the same building."
    2. "They trim the lines you feed the model; we sweep the twice-stored
    thinking blobs the model keeps feeding back. Both reduce waste; neither
    replaces the other."
    3. "Trim the context, or sweep the store ;  pick your tool for the layer
    you're bleeding tokens on. sweap, not sweep, the typo's the brand."
    
    ═══════════════════════════════════════════
    5. DRAFT SOCIAL POSTS
    ═══════════════════════════════════════════
    
    LINKEDIN (founder voice, 120-180 words):
    "We shipped sweap this week ;  a zero-dependency local tool that removes
    duplicate thinking blobs and tool-exhaust rows from an agent's persistent
    memory store, quarantine-first and fully reversible, with zero memory
    content lost on the machine we test it on (244 MB down to 206 MB, 11,170
    rows tidied, 0 bytes dropped).
    
    Same week, caveman-ai shipped trim-1: a 1.2 MB model that trims a live
    context per request.
    
    Our first commit predates their repo by ~13 hours; their repo predates
    ours on GitHub by ~2 days. Both tools landed inside a 4-day window ;  the
    same waste problem is clearly on everyone's mind. Their parent org claims
    113k GitHub stars and has shipped 4 repos in 7 weeks.
    
    The honest take: we solve different layers. They trim the lines you feed
    the model; we sweep the store the model re-reads. Complementary, not
    substitutes.
    
    What layer are YOU bleeding token dollars on right now?"
    
    WORD COUNT (approx): let me verify ~120-180. Count roughly: paragraph1
    ~40, para2 ~15, para3 ~55, para4 ~30, para5 (hook) ~12. Total ~150. Good.
    
    X POST (<280 chars):
    "Two tools, same week, same enemy: token waste. We commit sweap (13h
    before trim-1's repo) to dedup the agent's memory store ;  244MB→206MB, 0
    bytes lost, reversible. They trim live context lines. Different layers,
    not rivals. Their 113k-star org ships 4 repos in 7wks. Which layer costs
    YOU more?"
    
    Char count: let me count. "Two tools, same week, same enemy: token waste.
    " = 49. "We commit sweap (13h before trim-1's repo) to dedup the agent's
    memory store ;  244MB→206MB, 0 bytes lost, reversible. " = ~119 running
    total 168. "They trim live context lines. Different layers, not rivals. "
    = 58 → 226. "Their 113k-star org ships 4 repos in 7wks. " = 45 → 271.
    "Which layer costs YOU more?" = 29 → ~300. Over 280. Trim.
    
    Revised X:
    "Two tools, same week, same enemy: token waste. sweap dedups the agent's
    memory store (244→206MB, 0 bytes lost, reversible); trim-1 trims live
    context. Different layers, not rivals ;  both shipped within a 4-day
    window. Which layer costs YOU more?"
    
    Count: "Two tools, same week, same enemy: token waste. " 49. "sweap
    dedups the agent's memory store (244→206MB, 0 bytes lost, reversible); "
    81 → 130. "trim-1 trims live context. Different layers, not rivals ;  both
    shipped within a 4-day window. " 96 → 226. "Which layer costs YOU more?"
    29 → 255. Good, ~255 <280.
    
    Wait ;  "both shipped within a 4-day window" ;  defensible per amendment.
    Good. And I removed 113k-star org to fit; but I want the "space is hot"
    point. The LinkedIn covers it. Fine to keep X tighter. Actually let me
    include the "space is hot" hook briefly. Keep as is ;  255 chars is clean,
    includes the layers + timing + hook. Good.
    
    Note: no past-tense "saved $X" ;  correct, I say "244→206MB" measured past
    event labeled on our machine. Good. The "0 bytes lost, reversible" is
    measured/anchored.
    
    ═══════════════════════════════════════════
    6. FALSIFIED IF
    ═══════════════════════════════════════════
    
    The central claim ;  "trim-1 and sweap operate on different layers and are
    complementary, not substitutes" ;  is FALSIFIED if either tool is observed
    performing the other's core capability:
    
    - Falsifier 1: trim-1 (or any caveman repo) is shown to READ from or
    WRITE TO a persistent memory store ;  e.g., its README or code documents
    cross-session/historical duplicate detection, deduping stored history,
    mutating a store, or a regrowth watcher. That would put it on sweap's
    layer.
    - Falsifier 2: sweap is shown to perform real-time per-request
    synchronous trimming of a live in-context stream (query-conditioned line
    selection at call time). That would put it on trim-1's layer.
    
    Either observation collapses "different layers / complementary" into
    overlap or substitution. Until one of those is evidenced, the
    differentiation stands.
    
    TRIM-VS-SWEAP-ANALYSIS-OK