# R12 primary-source harvest: caveman.so growth timeline (harvested 2026-10-15)

All facts below pulled directly from live primary sources by the hub (GitHub API,
HN Algolia API, raw README). No model involvement. DeepSeek analysis rides on top.

## Timeline (all UTC, verified)
- 2026-04-04T10:03Z: repo `JuliusBrussee/caveman` created. Current stars: 111,865.
  Description: "why use many token when few token do trick. Viral skill + proxy for
  coding agents."
- 2026-04-05: HN front page, story id 47647455, submitted by `tosh` (a stranger, not
  the founder). 904 points, 366 comments. Title = repo description verbatim.
- 2026-04-06: HN 47661328 "Show HN: Rocky and Caveman Speak in Claurst CLI..." (5 pts,
  copycat wave begins within 48h).
- 2026-04-08: HN 47691809 "85-token caveman prompt that outperforms the 552-token
  original" (8 pts). Third-party replication starts day 4.
- 2026-07-06: HN 48804967, 2026-07-27: HN 49074296, 2026-07-28: HN 49080605 (46 pts):
  "Does Speaking to Agents Like Cavemen Save 65% of Tokens? We Test". Independent
  benchmark wave, months 3-4.
- 2026-08-18: HN 49352453 "Caveman Saves Tokens by Doing Less, Not Just Saying Less"
  (3 pts). 2026-08-21: HN 49390227 "Caveman prompting saves tokens, until you run it
  in real sessions" (3 pts). Skeptic wave, month 4-5.
- 2026-10-04: bin-v2.0.2. 2026-10-08: bin-v2.1.0 + `@caveman-ai/middleware` npm
  package v1.0.1 + v3.2.0. Productization week (proxy/middleware surface).
- 2026-10-13: v4.0.0 + v4.0.1 + bin-v4.0.0 + bin-v4.0.1 all same day. CLI binary
  distribution era.
- Total releases: 51. Sibling repos: cavegemma, cavekit, caveman-browse.

## README signals (fetched 2026-10-15, 22,518 bytes)
- Sells "Warm cache": "Step away and the provider forgets your session, so the next
  ask pays full price. Caveman keeps Anthropic's prompt cache warm while you pause."
- `caveman stats` surfacing; `caveman browse <url>` = "121 tokens instead of 15,704"
  for a Playwright snapshot of a 200-row table; `/caveman-compress` for memory files
  with backup.
- (From earlier research, e7ea9a2 era): Cloud $300/mo, VPC/enterprise tier, 33.2%
  fewer input tokens claim, 18/18 evals, 0.46x cost, byte-exact recovery, Fortune/
  404 Media/Hackaday/Decrypt/BNR press.

## Launch-thread texture (904-pt thread, 360 comments walked)
- Founder NOT among top commenters (top: TeMPOraL 8, DrewADesign 7, samus 6, dTal 6,
  amelius 6). Community carried the thread.
- Debate substance: tokens-as-thinking objection, output-quality risk, real-session
  skepticism, plus enthusiasm ("75% reduction is insane. Starred").
