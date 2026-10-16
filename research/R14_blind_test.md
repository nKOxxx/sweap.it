# R14: blind wire-ledger test, ChatGPT vs Claude
Date: 2026-10-16. Package: sweap_wire_test.zip (raw 45-row ledger + task brief,
no ground truth included), uploaded to exchange Drive 02_ChatGPT + 03_Claude,
MD5 3f13312d326d954d99562f9634c97d5b both sides.

## Claude (scored 2026-10-16)
Verdict: PASS, near-perfect. Zero invented numbers. Every figure it printed
reproduces from the file.

Q1 lanes: MATCH (paid glm-4.6 102 calls, hit 96.63%: ground truth 96.6%;
free DeepSeek 12 calls, 0%, 540,866 tok: exact). Bonus honesty: states the
"free = no cache contract" framing came from the brief, not the data; the
lane assignment itself derived from data (only model with cache reads).
Q2 breaks: MATCH (exactly 2 paid windows: 82,112/0 and 51,803/50,368 = 49.3%,
correct merged flags, correct session). Bonus: flagged a 74.6% near-miss
window, read gap_s as sampler interval not idle (correct), derived idle from
ts deltas (32.1h before break A: matches hub audit).
Q3 compaction: BEST-IN-CLASS. Refuses to confirm the planted premise from the
file alone (confidence: low), then decomposes: break A prefix did NOT shrink
(81,216 -> 82,112) so 32h cold cache explains it; break B prefix HALVED
(97,344 -> 51,776) = compaction-shaped; other 421-662s idles had no break,
so idle alone cannot explain B. NOTE: this corrects the hub's own earlier
verbal claim that A was the compaction break. The file says A = cold cache,
B = compaction. Claude out-analyzed the tool's author.
Q4 break tax: upper bound 133,915 tok; net 132,034 after median-load
subtraction (627/call), arithmetic shown, merged-window split caveat stated.
= 1.75% of paid input volume from 2 events in 1.4 days. Method defensible.
Q5 limits: exact ground truth (cause attribution impossible from file alone;
needs request-prefix hashes + cache-control placement + app compaction event
log joined to timestamps). That join is the sampler v3 roadmap.

## ChatGPT
PENDING (answer not yet received).

## Product implications
1. The ledger is stranger-auditable: an external AI reproduced lanes, breaks,
   and tax from the raw file with zero hand-holding. The artifact is the demo.
2. Refusal-to-overclaim (Q3) is the exact behavior sweap's register demands;
   incumbent models can do it when the artifact is clean enough.
3. Sampler v3 (optional harness hook) now has a spec written by the test
   itself: prefix-hash + compaction-event join would turn "compaction-shaped"
   into "compaction-caused".
