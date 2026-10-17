# Research artifacts

Standalone measurement outputs behind the studies. Raw and unretouched:
these are the receipts, not prose. Companion files: the studies that
commissioned them (see [../INDEX.md](../INDEX.md)) and the scripts that
produced them, in the same directory.

## tokenizer_exact_out.txt

Output of `tokenizer_exact.py`: the exact, full-store exhaust census.
Key figures: exhaust token share 90.69% and n=37,813 tool rows. Plain
text; the run is logged 2026-10-13 in
[docs/RESEARCH_LOG.md](../../docs/RESEARCH_LOG.md) (the file itself
carries no timestamp).

## sweap_census_out.json

Whole-store census by lane (model family). Schema:

- `generated` - ISO timestamp of the run
- `store` - store path string (local machine)
- `sessions`, `messages` - row counts (int)
- `stored_bytes` - total content bytes measured (int)
- `exhaust_share_pct` - share of stored tokens that is dead tool output (float)
- `lanes` - one dict per model family (e.g. `glm-4.6`, `MiniMaxAI`);
  each holds that lane's message count, byte count, and exhaust share

## tokenizer_remeasure_20261013.json

The stratified-sample remeasure with an exact full-store section. Schema:

- `date` - "2026-10-13"
- `store` - {bytes, sessions, messages} of the measured store (int values)
- `sample_ratio_chars_per_token` - per content class (tool content,
  assistant tool_calls JSON, assistant prose, user content)
- `sample_sizes` - per class; null means "deterministic 150-row stratified
  sample per class" (see `method` field)
- `token_est` - per-class token estimates from the sampled ratios (floats,
  labeled est because they extrapolate)
- `total_tokens_est` - sum of the above (float, est)
- `exhaust_token_share_pct` - 90.8885... from the sampled estimate; the
  EXACT full-store figure (90.69%) lives in `exact_full_store`
- `exact_full_store` - {tokens: per-class exact counts, total,
  exhaust_share_pct: 90.69, rows: 37813, method}: the number the README
  proof table cites
- `method` - one-line description: stratified 150-row sample per class,
  deterministic seed 20261013, o200k_base, plus the exact full-store pass

Reproduce any of it: the producing scripts are in this directory
(`tokenizer_exact.py`, `tokenizer_remeasure.py`); both are standard-library
only and read a store you point them at.
