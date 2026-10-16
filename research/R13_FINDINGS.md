# R13 FINDINGS: the three-plane context economy (sweap / caveman / jev)
Date: 2026-10-15. Methods: hub primary-source harvest + hub live-store measurements
+ DeepSeek-V4 landscape/design analysis (needle-verified, 7/7 hub checks PASS).
Everything numeric below is measured on the reference host unless stamped otherwise.

## THE THREE PLANES (identified, verified)
- WIRE: caveman.so (Apache-2.0, 111,865 stars). Proxy compresses REQUEST bytes
  in flight. Claims 33.2% fewer input tokens, 0.46x cost, byte-exact recovery.
- WINDOW: Jev (TypeSafe AI, launched Sep 15 2026; "System One" decision model,
  typed in/typed out, claimed ~100x faster, RLCD-trained). Ecosystem uses it to
  decide which tool outputs leave the live context: fast-jev-compaction
  (7,652 stars) "never rewrites, only deletes, kept stays verbatim"; the author
  of jev-context-router (research prototype) self-reports a conservative
  candidate FAILED a real-agent usefulness gate. Honest failure reporting.
- STORE: sweap (ours). Census + provably-dead-only sweep + byte-identical
  restore + per-call wire ledger (1-min snapshot-diff, no proxy).

## MEASURED TODAY (the new numbers)

1. THE WINDOW/STORE SPLIT (the headline):
   - Tool-content economy, pre-sweep universe: 19.6 MB dead (57%) vs
     14.5 MB live-in-window (43%).
   - Sweep re-verified: all 14,955 swept rows were active=0; live-window
     byte population identical pre/post sweep (H1 PROVEN on this store).
2. RECALL-SAFE WINDOW HYGIENE IS SMALL (the anti-hype number):
   Replaying the DOCUMENTED fast-jev-compaction policy as our own heuristic
   replica [REPLICA: identifier-matching, not their model, not their product]
   across 374 active sessions: only 545 of 7,684 payloads are stale-drop
   candidates = 0.41 MB = 2.8% of live tool bytes. The rest is pinned,
   prose, or still referenced later.
3. READ TOGETHER: a compaction optimizer buys ~3% of the window (recall-safe)
   on our host; the store sweep bought 48% of the FILE; the wire tool claims
   ~33% of request bytes. Different planes, different magnitudes, and H1 says
   the store win is INVARIANT to both other tools.
4. Cache risk (H4, unmeasured here, sampler now accumulating): any window
   mutation mid-session breaks the provider prompt cache and re-bills the
   prefix at full price. A 3% window win can go NET-NEGATIVE if it fires
   often on a cache-tuned lane (ours: 96.3% hit). This is the number the
   category does not publish. The wire ledger is built to measure it.

## DEEPSEEK'S DESIGN (four-arm experiment, for a later wave)
Arms: A baseline / B wire-only / C window-only / D both, plus sweap as the
measuring instrument on every arm. Metrics: tokens sent, billed cost, task
success, cache-hit rate, store bytes at end, restore fidelity. Full design in
research/R13_threepane_report.txt (Jev early-access gap handled by policy
replay, clearly labeled as replica).

## POSITIONING (DeepSeek's verdict, hub-endorsed)
sweap = the honest referee: sits at rest, sees every plane's NET effect on
money (savings minus cache breaks), read-only, byte-identical restore.
"The receipt for what all of them cost you."
