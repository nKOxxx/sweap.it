# R15: CAUSAL CACHE PROBE, per-model behavior matrix
Date: 2026-10-16. Tool: ~/.sweap/cache_probe.py. Method: identical ~3.5k-token
real prefix (repo README x3), fresh suffix per call; WARM x3, then ONE early
token mutated (compaction-shaped edit), then REWARM. Numbers = provider's own
usage reports, transcribed verbatim into ~/.sweap/cache_probe_results.json.

## RESULTS (3 models, 15 calls, measured today)

| model            | warm hit          | after 1-token mutation | rewind hit |
|------------------|-------------------|------------------------|------------|
| glm-4.6 (zai)    | 0 / 3520 / 3520   | **0 (FULL BREAK)**     | 3520       |
| DeepSeek (hyper) | 0 / 0 / 0         | 0 (no cache at all)    | 0          |
| MiniMax (hyper)  | 0 / 0 / 0         | 0 (no cache at all)    | 0          |

glm-4.6 tokenization note: 3520 cached of 3562 prompt = 98.9% of the prompt;
the ~42-token remainder is the differing suffix by design.

## FINDINGS

F1. Cache behavior is PROVIDER-AND-MODEL SPECIFIC. One model caches (98.9%
of a warm prefix), two do not cache AT ALL even on identical repeats within
seconds. The "96.63%" belongs to glm-4.6 alone. The user's suspicion that
lanes cannot share one number is CONFIRMED with causal evidence.

F2. glm-4.6's cache is prefix-exact AND instant-resilient: mutating ONE early
token dropped cached to 0 (full-prefix miss, no partial credit), and the
very next call with the original prefix hit 3520 again. Cache survives
briefly alongside the mutation; it is exact-prefix, quickly-reversible.

F3. Implication for the compaction debate (R14): on a caching provider, a
context rewrite = guaranteed full-prefix re-bill. On NON-caching providers,
compaction has ZERO cache cost because there is no cache to break. The H4
"window mutations can be net-negative" risk applies ONLY to caching lanes.
The four-arm experiment must therefore report per-lane: arms B/C/D differ
on glm-like lanes but are indistinguishable on hyperfusion-like lanes.

F4. Prompt-cache presence is also a POSITIONING fact for sweap: the audit
must never assume a provider caches. The receipt should show, per lane:
cache-capable (measured), hit rate, break census, break tax. "This provider
does not honor prompt caching at all" is itself a receipt line users want.

## SCOPE / LIMITS (stamped)
- n=1 probe round per model, 15 calls total, one host, one day. Directional,
  not statistical. The wire ledger adds observational data over time.
- Models requested but not testable today (no credentials on this host):
  Sonnet, "luna", "fable". Provider coverage grows only with keys the USER
  adds; no purchases by agent.
- DeepSeek/MiniMax free lane via Hyperfusion may or may not reflect those
  models' behavior on their first-party APIs (provider-side caching policy
  differs from model-side capability). Stamped [PROVIDER-BOUND].
