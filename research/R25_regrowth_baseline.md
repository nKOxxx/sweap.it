# R25: REGROWTH BASELINE + THE 26 MB DUPLICATE FINDING
Date: 2026-10-17 morning. Closes R18 attack A2 ("a hygiene product that
cleans once isn't hygiene") with a measured regrowth number, and finds a
NEW dead-weight category bigger than the one we swept.

## STORE STATE (2026-10-17, DB file 244.1 MB, 25,324 messages)

- Oct-14 sweep removed 14,955 rows / 19.6 MB (48% of file then). Today:
  zero orphaned tool rows (sweep criterion still clean).
- REGROWTH since sweep (~0.9 active days): +384 tool rows / +0.53 MB
  = ~431 rows/day, ~0.59 MB/day of new tool exhaust. None sweepable yet
  (all in still-open sessions; the at-rest-only law means they BECOME
  sweepable when their sessions close).
- Verdict on A2: regrowth is real but slow (0.6 MB/day). At this rate a
  monthly diet is plenty; weekly is generous. The trainer's job on THIS
  store is light. BUT see below: tool exhaust is not the main fat.

## NEW FINDING: THE 26 MB DOUBLE-WRITTEN BRAIN

Column byte audit of `messages`:
- content: 23.0 MB (the actual conversation: user+assistant+tool text)
- tool_calls: 21.4 MB (request scaffolding)
- reasoning: 26.0 MB AND reasoning_content: 26.0 MB, and they are
  BYTE-IDENTICAL: all 9,455 assistant rows that have one carry the exact
  same bytes twice under two column names. ~26 MB of the 244.1 MB file
  is one blob stored twice (spent thinking, the same category the Claude
  Code weigh-in flagged as its biggest dead component).
- DB file 244.1 MB vs ~70 MB of live column bytes: the rest is index
  overhead (FTS copies: messages_fts + trigram mirrors of every row) and
  ~5 MB freelist from the Oct-14 sweep (space returned to SQLite's
  freelist, not the OS).

## WHAT THIS MEANS FOR THE PRODUCT (plain)

1. The diet frame's biggest win on this store is not junk tool output
   (that regrows at 0.6 MB/day); it is DUPLICATED SPENT THINKING: one
   dedup/normalize at the store layer is worth ~26 MB here, more than
   the entire Oct-14 sweep removed, with zero information loss (the two
   columns are identical; keep one, or NULL the mirror at rest).
2. Regrowth answer for month two: tool junk ~18 MB/month if uncleaned;
   thinking duplication grows with every reasoning model call. The
   scheduled diet has real, measured work to do. A2 closed with numbers.
3. Sweepable-now inventory: sessions closed since Oct-14 still hold 0
   tool rows (our traffic this week went to few long-lived sessions), so
   the next sweep trigger should be either closed-session tool rows OR
   the reasoning-mirror dedup, whichever ships first.

## HONEST LABELS

- Regrowth rate is from 0.89 active days on one host: a first
  measurement, will be refined by the daily snapshot.
- The reasoning mirror duplication is a store-schema observation; the
  fix belongs to a diet command that normalizes at rest (never
  mid-flight), with quarantine + byte-identical restore as always.
- No sweep was run today. This round only measured.

## NEXT

- Daily snapshot cron (dead rows, dead MB, reasoning mirror MB) so the
  regrowth curve accumulates for the Oct-29 gate.
- Diet v2 candidate: reasoning-mirror dedup (26 MB win measured, zero
  loss) + closed-session tool rows.
