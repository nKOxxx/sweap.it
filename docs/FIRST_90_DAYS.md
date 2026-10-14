# sweap.it: THE FIRST 90 DAYS
### Execution receipt: what, when, where, how. One page of rules, three phases, weekly gates.

Owner: Nikola Stojanow. Executor: Hermes (hub). Date of issue: 2026-10-15.
Repo: ~/sweap.it, 35 commits, local only, no remote yet (by design until Day 1).

---

## THE 5 RULES (copied from the Caveman playbook, adapted to us)

R1. SHIP RAW, SHIP FAST. Weeks 1-2 ship as-is. No polish theatre before strangers
    use it. Perfection after feedback, never before.
R2. THE RECEIPT IS THE DEMO. Every public surface (README, post, reply, site) leads
    with `python3 cli/sweap.py` and the 90.69% number. Never lead with features.
R3. NO PROMOTION BY US. We never astroturf, never self-dominate threads, never buy
    attention. Seeding = making the artifact testable, then getting out of the way.
R4. NO MONETIZATION UNTIL THREE THINGS ARE MEASURED: real outside demand,
    a falsifiable metric strangers verified, a named real-world gap. Earliest
    realistic: Day 60+. Cloud/hosted tier is NOT in the first 90 days.
R5. EVERY NUMBER STAYS STAMPED. Measured vs [reconstructed] vs [projected] vs
    [ASSUMPTION] never blend. If a public number is challenged, rerun the census,
    screenshot, reply with the receipt.

Standing position: complementary to caveman.so, never competitor (DECISIONS.md).
License: Apache-2.0. Any contributed code must pass the em-dash check and the
security baseline before merge.

---

## PHASE 1: MAKE IT TOUCHABLE (Days 1-14)
Goal: a stranger can go from zero to their own receipt in under 2 minutes.

WHAT:
1. Public repo. Push ~/sweap.it to github.com/nKOxxx/sweap (Apache-2.0 already in).
   Description (the pitch IS the description):
   "why pay for context your agent already forgot. Read-only receipt for your
   LLM agent store."
   WHERE: github.com, user nKOxxx. WHO: Nikola clicks, hub prepares commands.
2. Generalize install beyond ~/.hermes: census auto-detects the store path
   (env var SWEEP_STORE, then ~/.hermes/state.db, then --store flag). One file,
   one function. Hub does it, Day 1-3.
3. Screenshot of a real receipt (yours, numbers yours, stamp intact) into the repo:
   docs/receipt_example.png. Strangers must SEE the card before running anything.
   Day 3-5.
4. Kill the friction list: fresh-clone smoke test on a bare machine (MacBitty VM
   stands in), fix whatever the 2-minute run trips on. Day 5-8, hub.
5. CHANGELOG.md + VERSION tag v0.1.0 at push. Day 1.

WHEN: Days 1-14. EXIT GATE (all must be true): fresh clone to receipt < 2 min on
a clean VM; README renders correctly on github.com; census survives a store it
has never seen (test on a friend's/anonymized sample, hub-verified).

---

## PHASE 2: LET STRANGERS FIND IT (Days 15-45)
Goal: first outside eyes, first unsolicited verification, zero paid promotion.

WHAT:
1. ONE launch post, when the exit gate above is green. Channel order:
   a. r/LocalLLaMA or r/AI_Agents (softest landing, technical audience)
   b. Hacker News "Show HN" 48-72h later IF the Reddit post drew organic
      engagement (not before; a dead Reddit post predicts a dead HN post)
   Draft title (use verbatim): "Show HN: Sweap - a read-only receipt for what
   your LLM agent store costs you"
   First comment (hub prepares, Nikola posts, ONCE, then silence per R3):
   context (found it measuring my own agent's bill), the 90.69% number, the
   30-second run, what it is NOT (not a proxy, not a compressor, caveman does
   that and we love them).
2. Reply discipline: hub drafts replies to every technical question WITH receipts
   (rerun census, paste output). Nikola posts. Response window: 48h after each
   post, then stop. No bumping.
3. Watch for the SKEPTIC (the August-moment in the Caveman arc): the person who
   says "works on your store, not on mine" or "the exhaust number is inflated
   by X". That comment is the roadmap. Log every one verbatim into
   research/objections.md. Do not argue. Fix or measure, then re-benchmark.
4. Every outsider-run receipt becomes a data point (with permission): store size,
   exhaust share, dollar card. Target: 10 outside stores measured by Day 45.
   WHERE: replies/DMs, logged by hub into research/field_receipts/.

WHEN: Days 15-45. EXIT GATE: >=1 unsolicited third-party run or benchmark;
objections.md has >=5 real objections; field receipts >=5. NO gate on stars.
(Vanity numbers are not a gate; verification is.)

---

## PHASE 3: MEASURE, HARDEN, DECIDE (Days 46-90)
Goal: turn attention into evidence, and evidence into a go/no-go on the company.

WHAT:
1. Ship the skeptic features (whatever Phase 2's objections actually named).
   Likely candidates from existing data: multi-store support, redaction mode
   (receipt that hides content, shows only sizes), a CI mode that fails a build
   when exhaust share crosses a threshold. Hub builds, prioritized BY objection
   frequency, not by our guesses.
2. The measured cache-break atlas: by Day 60 the wire sampler has 45+ days of
   per-minute cache ledgers on this host. Publish the method note (paper #2
   section): how session aggregates + snapshot-diff = per-call attribution.
   This is the alpha-logging the referee demanded; it doubles as the paper's
   measurement section.
3. Paper #2 submits: intervention section = sweep v1.1 + wire ledger + field
   receipts. Target venue per earlier review: FAccT/AIES track or workshop
   first. WHERE: arXiv after the 90-day review; workshop deadline drives date.
4. THE 90-DAY REVIEW (Day 88-90, sitting with Nikola): decide one of
   a. CONTINUE as company track: only if all three R4 measurements exist
      (demand: repeated organic asks + field receipts; metric: outsiders
      reproducing 90%-class exhaust on their stores; gap: a named, repeated
      real-world pain from objections.md).
   b. MERGE as feature/paper: the census folds into the agentic-institutions
      work as its measurement instrument; repo stays public and maintained.
   c. ARCHIVE: no outside verification emerged. Receipt printed, repo stays up,
      lessons logged. No vanity continuation.
   The decision uses only logged evidence, not vibes. Default if evidence is
   thin: (b), not (a).

WHEN: Days 46-90. EXIT GATE: the decision made, in writing, with the three R4
measurements each marked PRESENT or ABSENT.

---

## THE CALENDAR AT A GLANCE

Days 1-3    push public, auto-detect store, v0.1.0 tag           hub
Days 3-8    receipt screenshot, smoke test on clean VM            hub
Days 8-14   fix friction, freeze features, EXIT GATE 1            hub + Nikola
Days 15-21  Reddit post (Nikola posts, hub drafts)                Nikola
Days 22-30  HN if organic signal; 48h reply windows               Nikola + hub
Days 30-45  harvest objections, log field receipts (>=5)          hub
Days 46-60  skeptic features by frequency; wire atlas note        hub
Days 60-75  paper #2 intervention section drafted                 hub
Days 75-88  submission prep, evidence consolidation               hub
Days 88-90  THE REVIEW: continue / merge / archive                Nikola + hub

## WHO DOES WHAT
Hub (Hermes): all code, all drafts, all measurements, all replies-drafts, logging.
Nikola: the 4 clicks that matter (push public, post Reddit, post HN, the Day-90
decision) + every final word that leaves the account with his name on it.
Nobody else: nothing is outsourced; no paid promotion exists at any point.

## BUDGET (unlocked 2026-10-15, owner statement: "I have no issues to actually
put some money on this")
Money buys ASSETS, never ACCELERATION. Gates, receipt-first order, and the
Day-90 evidence decision do not move. Approved now:
- sweap.it domain (available per RDAP check 2026-10-15): ~10-15 EUR/yr.
  Registrar: any ( Porkbun/Cloudflare ); WHOIS privacy on; Nikola's card,
  hub prepares exact clicks.
- sweapit.com defensive redirect (~10 USD/yr), same day.
Still free-tier: hosting (GitHub Pages), CI, everything else.
Gated behind the R4 measurements (Day 60+): any paid infra, paid promotion
(stands forever per R3), design work, .com/.ai upgrades beyond the defensive.

## STANDING LAWS THIS DOCUMENT OBEYS
No fabricated numbers (everything stamped). No em-dash anywhere. English only.
Domain purchase approved (see BUDGET); hosting stays free-tier GitHub Pages.
DeepSeek free lane for any research waves.
Findings land as files; user artifacts are never rewritten.
