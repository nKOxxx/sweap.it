# R18: SECOND-ROUND RED-TEAM (DeepSeek attacks the FOUNDER RULINGS)
Date: 2026-10-16. Method: DeepSeek-V4-Flash free lane (hf_dispatch, 49s),
brief `research/briefs/R18_rulings_attack_brief.txt`, needle
`R18-RULINGS-ATTACK-OK` last line. Clean: `R18_rulings_attack_clean.txt`
(raw in raw/). Worker em-dash: 0. Verbatim attacks preserved there; below =
hub digest + immediate actions taken same day.

## THE FOUR ATTACKS (digest, severity as rated)

A1 vs RULING 1 (HIGH): "start from somewhere" hides selection bias. Who
installs a hygiene tool? The heaviest, most pain-drenched users; 90.69% may
describe them, not the market. Backfill reproduces a host's own bias: N
similar hosts converge on the same distribution instead of adding variety.
Lane variety (96.3/0/0/1.0/19.2) = one session structure, not cross-team
spread. FALSIFIED IF: 2-3 hosts with materially different workloads
reproduce ~90% exhaust + hit-rate spread, conditional on workload type.
Cheapest test: two non-adjacent hosts, census split by workload category.

A2 vs RULING 2 (HIGH): measurement is continuous (60s) but cleaning happened
ONCE (Oct-14). Dead weight regrows; honest answer to "what does it clean the
second month" is currently "nothing until a human acts." The sweep took the
PROVABLE 48%, while 90.69% of tokens are exhaust: a recoverable gap no
ruling reconciles. And at-rest-only means no protection exactly when it
hurts: mid-session, compaction imminent. FALSIFIED IF: scheduled sweeps
hold dead rows below threshold for a month AND at-rest cleaning measurably
reduces compaction events / full-price spend (sampler as yardstick).
Cheapest test: sweep on a schedule, log regrowth rows/day for 30 days.

A3 vs RULING 3 (MED): the 11-model audit tested the LEDGER; nobody but the
builder ever ran the INSTALL. Internal iteration finds logic bugs, outside
hands find friction/schema/environment bugs. The tool reads a moving target
(harness store schema): drift could make it degrade SILENTLY into plausible
wrong numbers. A rerun on the same host proves stability on one machine,
not correctness across environments. FALSIFIED IF: a non-expert installs
unaided on a fresh machine and a schema-drift simulation produces a visible
warning, never silent wrong output.

A4 vs NOTHING (HIGH, existential, new): the tool's own telemetry is a
privacy bomb nobody addressed. It reads the customer's most private corpus
(prompts, business data, secrets): backfill ingests the entire store, the
sampler writes a continuous ledger of its structure, the sweep hashes every
column. Nothing stated about where derivative data lives or whether any
byte leaves the machine. Trust IS the product here. FALSIFIED IF: published
architecture doc + reproducible proof of full local-first function
(network firewalled, tcpdump zero outbound, on-machine
quarantine/ledger/backfill, audit log of store reads, DPA-ready policy).
Cheapest test: firewalled install + endpoint grep.

## HUB SAME-DAY ACTIONS (before this doc was committed)

- A4 cheapest test RUN: grep of all 8 product files (cli/*.py + scripts
  sweap_*) for requests/urllib/socket/httpx/http(s)/api_key/POST: ZERO
  network lines. Every path referenced is on-machine (~/.sweap/,
  ~/.hermes/state.db, repo research/). The tool is local-only BY
  CONSTRUCTION; sweap's own code contains no transport. Remaining gaps
  turned into product gates, not rebuttals: README data-flow section +
  tcpdump-verified firewalled-install receipt BEFORE public flip.
- A2 answered in roadmap: recurring scheduled sweep (cadence TBD from
  regrowth log: dead rows/day over 30 days, already measurable from the
  live store) so "what does it clean the second month" gets a number.
- A1 accepted: second-host evidence is a time-gated goal (installs), not a
  claim we make today; public copy must label every number
  "one reference host" until then.
- A3 turned into a pre-flip gate: fresh-machine install by a non-builder +
  schema-drift drill (rename a column in a store COPY, require visible
  warning, never silent wrong output).

## NET VERDICT (hub)

Round 2 hurt more than round 1, which is the point. The rulings survived
as DIRECTION; the attacks exposed the missing OPERATIONS: recurring clean,
multi-host evidence, outside-hands install, and a written data-flow
warranty. A4 is the one that would have killed the product in a real
diligence room, and the answer (zero network code, local by construction)
is the strongest card we hold: the hygiene tool that physically cannot
phone home.
