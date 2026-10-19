# R34: GTM ideas (launch + first 90 days), DeepSeek worker, hub-adjudicated

- **Date:** 2026-10-19
- **Worker:** DeepSeek (hf_dispatch, 850s budget; landed 1m58s)
- **Brief:** `research/briefs/R34_gtm.txt` (blind: measured anchors only, no conclusions seeded)
- **Raw:** `research/raw/R34_gtm_deepseek_raw.txt` (verbatim; needle GTM-R34-COMPLETE = last line, position-verified)
- **Clean worker copy:** `WORKER_CLEAN.txt` (222 lines, chrome stripped)
- **Hub recount:** structural (all 10 blocks complete, rank + failure-modes + constraint sections present); no arithmetic claimed by worker. UNKNOWN tags used honestly, no invented stats, no contamination signs.

## HUB-SIDE ERRATA on the brief's own anchors (hub seeding, not worker error)

1. **License:** brief said "MIT"; the repo is **Apache-2.0** (LICENSE + README badge agree). Corrected everywhere downstream.
2. **Headline percentage:** brief said "~15.5%"; the repo publishes **MB only** (244.1 -> 206.5). Correct arithmetic from published figures is **15.4%**; the README/site deliberately carries no percentage. Use MB form in public copy.

## The 10 ideas (mechanism in one line each; full blocks in WORKER_CLEAN.txt)

1. **Receipt Reopen** - publish the repro recipe verbatim on the ungated landing page while the repo is still private; converts skeptics into reproducers. Success = an outside machine reports its own number.
2. **Named-Harness Report Card** - WEIGH one real, named harness store and tabulate the top offenders; gives one beachhead community a citable artifact. Success = a member of that community cites it.
3. **Undo Wedge** - lead with reversibility; a 3-step truth-demo (diet -> bytes out -> restore -> identical) on the landing page. Success = someone asks a restore-fidelity question.
4. **Watch-Hook** - publish the KEEP-OFF startup-hook snippet; turns one-shot users into recurring ones. Success = a hook-catching-rebloat report.
5. **Curator Drop** - 5 named curator outlets, rules read first, 3-sentence pitch with the measured number. Success = one named listing.
6. **Air-Gap Pitch** - one audit-proof line for regulated/air-gapped devs; local-only is the whole reason to adopt there. Success = an offline/firewall question.
7. **Restore Proof** - diff-the-store equivalence proof after diet+restore, published verbatim. Success = a data-loss skeptic returns.
8. **Install-Vector Squeeze** - PyPI so install is decoupled from repo visibility. Success = first non-founder usage signal. (Note: hub annotation - collides with the site's own "nothing to install" positioning; treat as optional, not core.)
9. **Your-Number Challenge** - the ask IS the marketing: run WEIGH, post your number; founder seeds with own. Success = an unprompted stranger number.
10. **Comparison Matrix** - local? reversible? account? cost? on a reproducible store; positional win built only from each alternative's own docs. Success = someone disputes or endorses a square.

## Worker's ranking (hub endorses the shape)

1. Receipt Reopen (runs inside the ungated site; builds the artifact everything else cites)
2. Named-Harness Report Card (converts the number into one beachhead audience)
3. Curator Drop (distribution layer; needs receipts from 1+2 first)

Sequencing: 1 builds proof -> 2 aims it -> 5 carries it. Infrastructure-true-early, not launch-moment: 4, 8.

## Failure modes the plan sidesteps (worker-named, hub-checked)

- FM1 no-beachhead ("everyone running agents" = nobody): sidestepped by 2's single-harness focus.
- FM2 vanity metrics: sidestepped; every success signal is an adoption fact (outside repro, community citation, curator listing), not stars/downloads.

## Constraint acknowledgment (worker)

Repo-private-for-2-weeks case: site-native ideas (1, 3, 6, 7, 8) unchanged; report card + curator drop link only the landing page; repo-native mechanics (Show HN, GitHub discovery, recipe-in-repo) defer until the repo opens.

## FALSIFIED IF (top 3, worker's own lines, kept as filed)

- Receipt Reopen: two weeks, no outside machine attempts a reproduction.
- Report Card: no harness-community member references it within two weeks.
- Curator Drop: zero pickups/acknowledgments from the five targets within two weeks.

## HUB VERDICT

Worker run clean; ranking survives adjudication. Adopt sequence 1 -> 2 -> 5 as the launch-week spine, gated on PR #4 merge per option B; prepare site-side assets for 1/3/7 while gated. Ideas 2/5 need the repo public (post-merge). Nothing publishes without the founder's explicit go (research-gating law).
