# R33: Per-vendor carrying charge (the same $0.49 method, all three stores)

**Date**: 2026-10-18. **Worker**: DeepSeek free lane, proc_b8e35e389586,
2m02s, needle `R33-CARRYING-CHARGE-OK` (last line).
**Brief**: `../briefs/R33_carrying_charge_brief.txt` (blind: measured
constants + public list prices only, no conclusions seeded).
**Raw**: `../raw/R33_carrying_charge_raw.txt` (verbatim, untouched).
**Hub recount**: every arithmetic cell re-derived BEFORE reading the
worker's answer (pre-registered), then diffed. Zero worker arithmetic
errors this run; one input problem inherited from filed R32 (ledger below).

## The question

R28 proved the carrying charge for one lane (Hermes/glm-4.6): $0.49 per
1M junk tokens per memory lapse. Does the same arithmetic hold per vendor?
The user's ruling that started this study: "There should be for each model
the % and also the saving."

## Method

carrying charge = input price − cache-read price (per 1M tokens). This is
the extra $ a memory lapse imposes on content that exists only to be
re-read: healthy cache serves it at the cache-read rate, a lapse (0.0%
hit) re-reads it at full input price. Savings-if-dieted = dead-weight
tokens × carrying charge. Falsified if any vendor's cache-read price
equals its input price; verified false for A and B, UNKNOWN for C (no
verified public price list in hand; kept symbolic).

## The table (every cell recounted at the hub)

| Vendor | Store | Dead weight | Charge $/1M junk tok | $ per lapse (this store) | Savings if dieted |
|---|---|---|---|---|---|
| A: Hermes, glm-4.6 | 206.5 MB, 18,210,064 tok measured | **90.69%** exact (n=37,813) | **$0.49** (= $0.60 − $0.11) | **$8.09** | $8.09 [HYPOTHETICAL] |
| B: Claude Code, Sonnet-class | 1.55 MB | 4.8–14.8% band (75–230 KB, dedup only, UNPROVEN till restore test) | **$2.70** (= $3.00 − $0.30) | $0.056–$0.173 (T3 basis) / $0.051–$0.155 (T4 basis) at 4 B/tok [ESTIMATE] | same [HYPOTHETICAL] |
| C: Codex CLI, GPT-6.1-Sol | 172,360 B session file (493 MB disk is program, never re-sent) | 9.5% proven dups; itemized static re-dump surface 12.9–14.4%; filed R32 headline 27% UNRECONSTRUCTED (see ledger) | P_C,in − P_C,cr [SYMBOLIC] | 0.0041·(P_C,in − P_C,cr) at 9.5%; 0.0055–0.0062·(ΔP_C) at itemized re-dump [ESTIMATE] | same [HYPOTHETICAL] |

B bytes→tokens: unmeasured; 4 B/tok assumed (declared), sensitivity shown
at 3/5 B/tok in the raw ($0.068–$0.207 and $0.041–$0.124 on the T4 basis).

## Why the A number dwarfs B and C (read-across law)

The three dead-weight shares are NOT the same construct: A counts stored
tokens of tool exhaust (a content census); B is a reversible-dedup band on
bytes; C is proven-duplicate plus static-surface bytes on one session
file. The $ figures are therefore not "who is worse", they are three
different diseases priced on three different denominators. What IS
comparable: the charge per 1M junk tokens ($0.49 / $2.70 / ΔP_C) — the
price of forgetting, per vendor. B's charge is 5.5x A's because Anthropic
list prices are 5x z.ai's; a lapse costs more on expensive models.

## The two rulers (T5, worker-derived, hub-checked)

Cache hit rate (A: 95.87–98.65% healthy) and dead-weight share (A: 90.69%)
are both true at once: a healthy cache serves junk perfectly well. The
lapse changes the ruler the junk is priced on: hit rate 0.0%, full input
price, and the carrying charge is the gap. Neither number was averaged
into the other; they answer different questions.

## Discrepancy ledger (hub recount)

1. **R32's "static context re-dump: 27%" could not be reconstructed from
   its own itemization** (6 x 4,124 B = 24,744 B = 14.4% of the 172,360 B
   session file; the constant/delta-encodable part ~22.2 KB = 12.9%). The
   brief carried 27% as [ANCHOR] from the filed study; the worker used it
   mechanically (46,537 B upper surface). Hub correction: R33's C-rows use
   itemized bytes; the 27% headline stays quoted as-filed, marked
   UNRECONSTRUCTED. Not a worker error. R32 stays as filed (no silent
   edits to filed studies); an R32 erratum is the founder's call.
2. Worker's B-band arithmetic verified exact at all three B/tok factors
   (pre-registered anchors matched to the cent).
3. Worker's A numerator 16,515,331 tok and $8.09 savings matched the
   pre-registered hub anchors exactly (and reproduce R28's $0.49).

## Second lane (user decree: "use deepseek and the other one"): MiniMax rerun

Same blind brief, no communication between workers
(`../raw/R33_carrying_charge_raw_minimax.txt`, proc_645f0bc04c54, 1m18s,
needle last line). Cross-worker diff, hub-adjudicated:

**Converged exactly (independent derivation, same numbers):** A-row in
full (16,515,331 junk tok; $0.49 charge; $8.09 per lapse), B charge $2.70,
B T4 band at 4 B/tok ($0.051-$0.155, and MiniMax's 3/5 B/tok bracket
$0.041-$0.207 matches DeepSeek's sensitivity table to the cent), the
falsified-if verdicts, and the two-rulers explanation. Two models given
only constants reached the same core table: that is the cross-validation
signal for the method.

**Divergences (hub adjudication, filed-anchors win):**
1. **B dead-weight band**: MiniMax built 19.9%-31.6% by adding the 15.1%
   empty-thinking-signature bytes (and optionally the 16.5% envelope
   framing) to the 4.8% copy. Adjudication: those signatures ARE dead
   content, but they are NOT recoverable by us (vendor-erased), so they
   belong in T1's "junk re-sent" reading and NOT in T4's "savings if
   dieted" - only the filed dedup band 75-230K is dietable. MiniMax used
   its wider band for both; we keep 4.8-14.8% for savings and note
   19.9-31.6% as the "junk including vendor erasure" reading.
2. **C composition**: MiniMax summed 27% + 9.5% = 36.5%. Two defects: the
   27% is the UNRECONSTRUCTED headline (itemized: 14.4%), and the 9.5%
   exact-dup boilerplate lives INSIDE the turn_context records per R32's
   own census (6 of the 13 copies) - summing double-counts. Rejected.
3. **C symbolic charge**: MiniMax invented a cache-ratio carryover
   ("assume GLM's 0.183 ratio holds for GPT") and printed 0.49xP_C as
   "conservative". Cache-read ratios are vendor-specific (zai 0.183,
   Anthropic 0.10); importing one across vendors is an unsupported
   anchor. Rejected; the clean symbolic form (P_C,in - P_C,cr) stands.
4. **MiniMax arithmetic slip** (logged): its A verification line decomposes
   $10.93 full cold send as "useful $1.01 + waste $8.09", but 1.01 + 8.09
   = 9.10, not 10.93 - it mixed the full-price basis ($1.02 + $9.91) with
   the charge basis ($8.09 vs cache). The $8.09 itself is correct; the
   decomposition sentence is not.

Net: both lanes agree on everything the filed anchors determine; every
divergence traces to a worker going beyond the anchors, and in each case
the anchor-honest version is the one filed above. The cross-worker
consensus on A and B charges ($0.49 / $2.70) and the $8.09 headline is
therefore double-derived.

## Verdict

The carrying-charge method generalizes. Per-lapse price of forgetting:
**Hermes $8.09, Claude Code ~$0.05–$0.17, Codex 0.004–0.006 x (unknown
price delta)** on the measured stores. The honest headline is not "A is
worst" but "the charge exists on every vendor, scaled by store size and
list price; B's per-token charge is 5.5x A's." Research file only: no
site, no README table until the founder gates it.
