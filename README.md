# sweap.it

**why pay for context your agent already forgot.**

Agent stacks rot in a place disk cleaners never look: the context plane. Every
API call re-sends your whole history, tool schemas, and months of dead tool
output, and your provider bills all of it. sweap.it measures that rot from your
own store, sweeps the dead weight reversibly, and prints the receipt.

> 90.69% of stored transcript tokens are tool exhaust. Exactly counted,
> not estimated. Your agent's context is mostly corpses.

## The demo (30 seconds, read-only, your own data)

```bash
git clone https://github.com/nKOxxx/sweap.it && cd sweap.it
python3 cli/sweap.py
```

No config, no API key, nothing leaves your machine, nothing is modified.
You get your receipt:

```
==========================================================================
SWEEP CENSUS : context-plane receipt (read-only; nothing was modified)
       373 sessions, 23,960 messages, 21.7 MB stored
==========================================================================

THE WIRE - what providers billed (their own usage report)
lane                calls  re-sent/call cache hit     unc.in  cache-read
glm-4.6            10,277      76,143t     96.3%     28.9M     753.6M

THE STORE - what your disk carries at rest
  tool exhaust: 90.69% of 18,210,064 stored tokens (exact count, o200k)

YOUR DOLLAR CARD
  glm-4.6          $  62.56  (uncached $17.34 + cached $45.22)
  cache lottery: your best lane hits 96.3%; if every lane did,
                 you would pay $72.58 instead of $97.51
--------------------------------------------------------------------------
CARD-OK
```

That is the product thesis in one screen: your numbers, measured, priced,
with the reclaim named. The demo IS the product. (Figures above are one real
host's receipt, yours will differ: that is the point.)

## What it does

| command | what | writes? |
|---|---|---|
| `python3 cli/sweap.py` | context-plane census + dollar card | nothing, read-only |
| `python3 cli/wire.py` | wire-plane ledger (cache-break tax) | nothing, read-only |
| `python3 cli/sweep.py --dry-run` | find provably-dead tool output | nothing |
| `python3 cli/sweep.py --quarantine` | stage dead rows to `~/.sweap/quarantine/` | copies only |
| `python3 cli/sweep.py --apply-manifest M --apply-manifest M` | reclaim the disk (double flag = human gate) | vacuum, reversible |
| `python3 cli/sweep.py --restore M` | put every row back, byte-verified | restore |

Reversibility is proven, not promised: every quarantined row ships with a
SHA-256 over all 23 columns; restore verifies the hash before and after.
A live rehearsal (14,955 rows) restored byte-identical.

## The falsifiable numbers (measure yours, we measured ours)

- **90.69%** of stored transcript tokens are dead tool output
  (n=37,813 rows, exact tokenizer count)
- **48%** of the session-store file is provably-dead tool rows
  (14,955 rows, 19.56 MB); sweeping them reclaimed 23.6 MB on a live store
- **96.3%** cache hit on the best-tuned lane vs **0.0%** on untuned lanes;
  the gap is the "cache lottery", $24.93 over one host's lifetime [reconstructed]
- **$53.80** lifetime cache-break tax on one host [reconstructed from
  provider usage reports]

Community reactions are not benchmarks: run the census on your own store and
check our arithmetic. Every number above is reproducible from the tool.

## Why not just compress (we love caveman, this is the other half)

[Caveman](https://github.com/JuliusBrussee/caveman) (Apache-2.0) shrinks
requests in flight with a proxy: fewer tokens sent. sweap.it audits the store
at rest: fewer tokens carried, re-sent, and billed forever after. They are the
diet, we are the audit. If you run any in-path compressor, sweap tells you
what your store still carries underneath it. The two compose; neither replaces
the other.

## Safety law

1. **Inventory never lies.** Every number is measured at run time.
2. **Default to reversible.** Census reads; sweep quarantines before it ever
   deletes; restore is byte-verified.
3. **Never first-run.** Nothing destructive happens without a staged manifest
   and a double-flag human gate.
4. **Dollar figures are stamped.** `[reconstructed]` / `[projected,
   verification pending]` / `[ASSUMPTION]`, never silently blended with
   measured facts.
5. **Read-only until the gate.** The default command touches nothing.

Currently tuned for Hermes Agent stores (`~/.hermes/state.db`); the census
schema is written to generalize. Apache-2.0. Not affiliated with caveman.so;
go use both.
