# sweap.it posting schedule v2: when, where, what

Built 2026-10-20 from R34 (GTM study) + launch state.
**v2 (2026-10-20): DeepSeek hostile review applied. 5 must-fixes incorporated;
channel order re-staged per the launch-sequencing law; receipt funnel now
actively recruited. Review verbatim: DEEPSEEK_REVIEW_CLEAN.txt.**
All times Gulf (UTC+4). Nothing posts without the founder's explicit go.

## Where we stand (launch state, 2026-10-20)

- Landing page live: sweap.it (share cards, report card, price board, 3-step CLI)
- Repo public: nKOxxx/sweap.it (receipt template, CI-verified repro, receipt board)
- GitHub topics set (ai-agents, cli, sqlite, local-first, privacy, claude-code, ...)
- Report Card live with founder slips (Receipt #1); slot ready for outside receipts
- Telegram blurb posted by founder (2026-10-20): first tester wave
- Receipts: 1/10 (founder only)
- Daily receipt watcher: reports 09:00 in this chat

## The spine (unchanged; v2 fixes the sequencing, not the spine)

Proof builds first, then aims, then carries:
1. Reproducibility - DONE, live
2. Named-Harness Report Card - DONE, live, awaiting outside slips
3. Curator Drop - needs receipts from 1+2 first

## Phase 0: Oct 20-22 - RECRUIT the first outside receipts (v2 fix #1)

Receipts do not gather; they are recruited (Do Things That Don't Scale).

| When | What |
|---|---|
| Oct 20-21 | Founder sends 10-20 individual 1:1 asks (Telegram DMs) to known agent users: one-liner + the exact command + "paste the output, that's it". Template: ASK_TEMPLATE.md. |
| Oct 21-22 | Founder handles replies personally. I verify each pasted output, check the permission box, add the slip to the Report Card same day. |
| Oct 22 | GitHub hygiene: tag v1.0.0 release on the repo (needed before any HN pointing). |

Gate that ends Phase 0: >= 1 outside receipt filed.

## Phase 1: Oct 23-30 - soft channel first (v2 fix #3, #4)

| When | Where | What |
|---|---|---|
| Oct 23, evening | same Telegram groups | one follow-up, receipts-led: whatever the board shows, honestly ("3 machines weighed in, here are their numbers" or honest status). Never a repost of the blurb. |
| Oct 24-27, wait for organic engagement | r/LocalLLaMA (primary) or r/selfhosted (privacy/offline lede: "runs offline, no signup, stdlib only") | ONE soft-channel post, proof-led. Title deadpan, no "diet". r/commandline as backup venue if neither bites. |
| Oct 25-30 | awesome-lists (named deliverable, v2 fix #5) | submission PRs: awesome-claude-code, awesome-llm-agents (one line each, receipt-board link). I draft, founder approves. |
| sliding | Daily 09:00 | receipt tally; slips added same day |

Gates for Phase 2 (BOTH required): soft-channel post drew organic engagement (comments/upvotes, not just views) AND >= 1 outside receipt.

## Phase 2: Nov 3-10 - Show HN, one owned day (v2 fix #3)

| When | What |
|---|---|
| 48-72h after Phase 1 gates pass (realistic: Nov 3-10) | Show HN, Tuesday-Thursday morning US hours. Title: "Show HN: Sweap - measure and reversibly shrink your AI agent's memory store". First comment pre-written (SHOWHN_COMMENT.md): leads with the measured number, the receipt board, the repro command. |
| That whole day | Founder answers every comment; I feed him receipts/numbers on demand. No other campaign runs this day (v2 fix: X thread cut). |
| Day+1 | X/Twitter: optional single post linking the HN thread (demoted from standalone campaign). Reddit follow-up crosspost only if HN drew real engagement. |

## Phase 3: Nov 10-24 - Curator Drop, 3 outlets not 5 (v2 fix: effort cut)

| When | What |
|---|---|
| Nov 10-14 | Research 3 named curator outlets (not 5): newsletters/directories listing dev tools. Read submission rules first. DeepSeek census, hub-verified. |
| Nov 15-18 | One 3-sentence pitch per outlet. Batch approval: founder reviews all three in ONE session. Stagger sends 2 days apart. |
| Nov 21 | checkpoint: curator lag is 2-4 weeks [MED], so acknowledgment gate extended to Nov 28 (was Nov 16). |

## Automated throughout (zero founder time)

- 09:00 daily: receipt count + who
- New receipt same day: verified, permission checked, slip added to Report Card
- Weekly Sunday: one-line funnel status in this chat

## Kill-switches (v2 fix #2: dates now match the 2-week clocks)

Launch = Oct 20. True 2-week gates:
- Receipt funnel dead if: no outside reproduction attempt by **Nov 3**
- Report Card dead if: no harness-community citation by **Nov 3**
- Curator Drop dead if: zero acknowledgments by **Nov 28** (3+ week curator lag)
No kill-switch fires inside its own success window anymore.

## Explicitly NOT scheduled

- PyPI package: collides with "nothing to install" positioning (R34 annotation)
- Paid anything: no budget line exists
- X thread as a standalone campaign: cut (vanity reach at zero followers; story moves into the Show HN first comment)
- Spam reposts: one receipts-led bump per channel, then silence unless asked
