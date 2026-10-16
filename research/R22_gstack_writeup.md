# R22: DOES SWEAP HOLD UP AGAINST GSTACK? (direct repo inspection)
Date: 2026-10-16. Method: hub direct inspection of github.com/garrytan/gstack
at current HEAD (cloned depth-1 to /tmp/gstack_probe, 77 skill dirs + docs +
designs + CHANGELOG inspected). Every claim below cites a file in their repo
so anyone can re-run this check. This document is written to be shared: the
test, the evidence, the verdict, and what we would build.

## WHAT GSTACK IS (one line)

Garry Tan's MIT-licensed "software factory" for Claude Code: 23+ specialist
roles and 8 power tools as slash commands (CEO reviewer, eng manager,
designer, QA, security officer, release engineer), turning one builder into
a virtual team.

## THE TEST

The founder's question: our positioning and product were built and measured
on a Hermes-style stack. Does sweap still hold up when the customer runs a
gstack/Claude Code setup instead? Three sub-questions:
1. Does gstack already do what sweap does (overlap/displacement)?
2. Does sweap's plane (the persisted store) even exist on that stack?
3. Does the diet frame survive contact with their story?

## FINDING 1: POSITIONING HOLDS, AND THEIR OWN REPO STRENGTHENS IT

The strongest receipt in their tree: gstack tried to build EXACTLY the
mid-flight compaction product category and TABLED it.

- `docs/designs/GCOMPACTION.md`, status TABLED (2026-04-17): their planned
  `gstack compact` died on architectural reality. PostToolUse hooks cannot
  replace built-in tool output entering the model's context (only MCP tools,
  per Anthropic's own docs and open issue #36843); Read/Grep/Glob execute
  in-process and bypass hooks entirely; the only hack available
  (decision:block + reason injection) they rejected as undocumented,
  disputed, and breakable.
- Why this is our receipt, not our threat: the category sweap measured
  (window/wire mutation breaking provider prefix caches, one-token mutation
  dropping a 98.9% warm lane to 0%) is the same category gstack engineers
  concluded is architecturally unsafe to touch. They shelved it at zero
  code cost. That is a third-party confirmation of our at-rest-only law.
- `docs/designs/SESSION_INTELLIGENCE.md`: their context answer is
  WORKAROUND, not hygiene. Compaction is treated as inevitable
  ("destroys file reads, reasoning chains, and intermediate decisions");
  their fix is writing artifacts to ~/.gstack/projects/<slug>/ and a
  preamble that re-reads them after compaction. They work around the
  memory loss. Nobody in their tree MEASURES what the memory loss costs.
  Break B (compaction 95 seconds before a 50k-token full-price re-bill)
  is exactly the event their design accepts silently and sweap bills.
- `context-save`/`context-restore` skills: manual "save my work" (git state,
  decisions, remaining work) so a future session resumes. Artifact
  persistence, not store hygiene. Complementary: their artifacts CREATE
  store content; sweap is the one that later weighs it.
- `gstack-context-bill` (closest overlap, and it is not close): a read-only,
  OFFLINE audit of what the installed SKILLS TREE costs in tokens
  (always-on frontmatter vs per-invocation files), with --diff and --budget.
  Static, one luggage-weighing of the crew's uniforms. No store census,
  no cache dimension, no breaks, no per-lane truth, not continuous.
  Sweap weighs what the crew actually drags around (the store) and what
  the trips cost (the wire). Distinct plane, stays complementary.

Net: nothing in the shipped tree censuses the store, sweeps dead weight,
measures prompt-cache truth, or attributes break causes. The three-plane
map (wire/window/store) is still unmapped in the highest-profile agent
stack in the ecosystem.

## FINDING 2: THE SWEAP INSTRUMENT DOES NOT HOLD UP AS-IS (the honest gap)

Sweap's instruments are Hermes-store-specific: census and sweep read the
Hermes SQLite state.db; the wire sampler reads Hermes usage tables. A
gstack user's stack persists differently: Claude Code writes per-project
JSONL transcripts under ~/.claude/projects/, and gstack adds its own state
(~/.gstack/: plans, reviews, learnings.jsonl, timeline.jsonl, security
logs).

What that means, concretely:
- The PLANE exists (persisted transcript + artifact stores full of tool
  exhaust; if anything, a 23-specialist stack generates MORE exhaust than
  our single-agent host, so our 90.69% census number likely gets worse,
  which is good for the pitch).
- The PRODUCT does not run there yet. `sweap weigh` / `sweap diet` need a
  store adapter for the Claude Code layout before the diet frame works on
  a gstack machine. [THEORY, to verify on a real transcript: Claude Code
  JSONL carries per-message usage including cache-read token counts, which
  would make the wire ledger EASIER there, direct per-call reads instead
  of snapshot-diff sampling. Verify before claiming.]
- One hard integration rule, learned from their architecture: a sweap
  diet on a gstack machine must treat ~/.gstack/projects/<slug>/ as LIVE
  and PINNED, never sweepable. Their preamble recovery depends on those
  artifacts after every compaction; deleting them would break session
  recovery silently. Provably-dead logic must learn their schema first.
  This is the same discipline that made the Hermes sweep safe (active
  reference checks before anything moves).

## FINDING 3: THE DIET FRAME SURVIVES, AND EXTENDS CLEANLY

Their hero number is speed and scale (810x pace, a virtual team). Ours
answers the question their story creates: a bigger crew drags more junk.

- Contrast line, extended (fourth beat, complementary, no attack):
  "Caveman makes your AI talk less. Jev makes your AI think faster.
  gstack makes your AI a team. Sweep makes your AI weigh less."
  (sweap, not sweep, in final copy; test here showed the pun is a real
  typo risk, worth a spelling check rule in all published copy.)
- The trainer beat gets STRONGER on their stack: 23 specialists hoard
  exhaust continuously; the watch-and-flag loop has more to watch.
- Their own trust machinery (hash-chained egress receipts for every
  off-machine send) speaks our language: local-first is already the
  culture of this audience. Our zero-network-code receipt lands there.

## VERDICT

- POSITIONING: holds. Their repo independently validates the thesis that
  mid-flight mutation is unsafe (tabled compactor) and that compaction
  cost is accepted silently (session intelligence workaround). The store
  and wire planes are untouched territory on the most visible agent stack.
- PRODUCT: does not hold up there YET. One adapter short: a Claude Code
  JSONL store reader for weigh/diet, with gstack artifacts pinned live.
  Until then, all public copy stays honest by saying measured on our
  reference harness.
- FRAME: survives and gains a fourth beat plus a sharper trainer story.

## WHAT WE WOULD BUILD (order, with honest size)

1. sweap weigh --store claude-code: read-only census of
   ~/.claude/projects/**/*.jsonl (dead tool-output share, MB). [MED size:
   schema recon on a real transcript first, the census logic ports.]
2. sweap diet with their schema rules: provably-dead tool results only,
   ~/.gstack/** pinned live by default, quarantine + byte-identical
   restore unchanged. [LARGER: their store anatomy is not yet measured;
   no numbers promised until the census runs.]
3. Wire ledger v4 option: per-call reads from transcript usage fields
   (if the [THEORY] above verifies) instead of snapshot-diff. [SMALL if
   fields exist; this would also simplify the Hermes-side sampler later.]
4. Their /retro-style monthly gain receipt is already our day-30 plan;
   gstack users would meet it as a familiar artifact shape.

## FALSIFIED-IF (what would kill this assessment)

- If a future Claude Code/gstack release ships built-in compaction WITH
  cost receipts, the measurement gap closes and sweap's wedge narrows to
  verification only. Watch their TODOS.md compaction entries and
  Anthropic issue #36843 (the exact unblock they named).
- If the JSONL transcripts turn out NOT to carry per-message usage, the
  wire-ledger-on-gstack story shrinks to a new sampler design (harder,
  not impossible).
- If a real census on a gstack machine shows tool exhaust well BELOW our
  90.69%, the diet pitch weakens there specifically. Current expectation
  is the opposite, but it is a measurement, not a right.

## RE-RUN INSTRUCTIONS (anyone can check)

git clone --depth 1 https://github.com/garrytan/gstack /tmp/gstack_probe
Read: docs/designs/GCOMPACTION.md (status header),
docs/designs/SESSION_INTELLIGENCE.md, context-save/SKILL.md,
context-restore/SKILL.md, README.md (gstack-context-bill row),
ARCHITECTURE.md (egress receipts, ~/.gstack layout).
