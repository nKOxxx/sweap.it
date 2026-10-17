# FLIP-PREP 1: SCHEMA-BREAK DRILL - PASSED
Date: 2026-10-17. Gate: R18 ruled the public flip needs a schema-break
drill on record. Question: what happens to diet.py's quarantine/restore
when the store schema changes under it?

## DRILL SETUP

Copy of the live store in an isolated sandbox HOME; quarantined with
diet.py (manifest records the 23-column schema); then the schema was
broken by adding a column (future_flag, what a future Hermes version
would do); then restore and apply were attempted against the new schema.

## RESULTS (all three paths, receipts)

1. RESTORE with OLD manifest against NEW schema: WORKS. The manifest
   carries the full column list it staged with; restore inserts exactly
   those columns by name; the new column is untouched. Field-by-field
   compare of every staged row after restore: 0 mismatches; the added
   column's values intact on all rows. Old backups restore into newer
   schemas: the upgrade direction, the one that matters.

2. APPLY with OLD manifest against NEW schema: ABORTS LOUDLY.
   "schema drift {future_flag}: re-quarantine first", store rolled
   back, nothing touched. The drift check (manifest columns XOR live
   columns) refuses to act across a schema change. This is the safety
   direction: never delete based on stale assumptions.

3. RE-QUARANTINE after the break: ADAPTS. New manifest records all 24
   columns including future_flag; apply then works normally. The tool
   heals by re-staging, exactly as the receipt instructs.

## HONEST NOTES

- First re-quarantine attempt hit a transient ro-open failure (hot WAL
  journal right after the rw ALTER). Checkpointing cleared it; ro reads
  fine. Real-world shape: a writer mid-commit can briefly block a
  read-only opener; busy_timeout governs. Not a data risk, an availability
  blip; the tool failed LOUDLY, not wrongly.
- The sandbox copy staged only 2 twins (vs 9,469 live) because a raw
  file copy misses WAL-committed rows; a drill artifact. The drill's
  subject is schema drift, not row census; census parity is proven in
  R26's live run and the demo round trip.

## VERDICT

Schema break: SAFE. Restore survives forward breaks, apply refuses
ambiguous ones loudly, re-quarantine adapts. Flip-prep gate 1 of 4 PASSED.
