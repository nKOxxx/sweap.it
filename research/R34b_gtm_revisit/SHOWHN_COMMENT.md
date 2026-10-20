# Show HN first comment (paste the moment the post is live)

ARRANGEMENT B (locked 2026-10-20: founder call + hub guess + blind
DeepSeek lane all concur; raw: R35_paper/R35_hn_title_check_raw.txt).

Post headline (HN prepends "Show HN:"):
  90.7% of Our AI Agent's Memory Is Dead Weight

First comment, verbatim from the top:

---

Written twice, billed once. That is the defect we found in how agent
platforms persist model reasoning: the text is stored twice,
byte-identical, under two column names, on 100 percent of rows that
carry it. It is a schema defect, not a usage pattern - which means the
vendor can fix it for every user at once.

We spent a month weighing the rest of the store too. Short version:

- 90.69% of the 18.2M stored transcript tokens in our reference store
  serve no future purpose (exact count, all 37,813 tool rows, no
  sampling).
- The duplication is additional to that: 26.0 MB of reasoning written
  twice under two names.
- Dead weight has a price. A memory lapse re-transmits stored context
  at full input price - 0.135 to 2.70 USD per million junk tokens
  across four vendors' published price lists. For our store that is
  8.09 USD as a ceiling for a wholesale re-read; a real lapse
  re-injects through bounded windows, so actual per-event cost is
  far less. Arithmetic on public price lists, no modeling.
- One reversible diet cut 37.57 MB with zero information loss:
  hash-verified quarantine, restore drilled against a schema change.
- It grows back at ~431 rows/day on our host, so hygiene is a
  schedule, not an emergency.

Every number came out of a blinded protocol: workers derived figures
without seeing expected answers, outputs were needle-gated, the hub
pre-registered its own numbers first and recounted after - and when
the hub was the one wrong (yes, it happened, in the pricing study),
the protocol caught it and the erratum is filed in the repo.

The tooling is free, Apache-2.0, Python stdlib only, runs offline, no
account. Two commands:

Weigh (read-only, 30s, Claude Code stores, nothing to clone):
  curl -sL https://raw.githubusercontent.com/nKOxxx/sweap.it/main/cli/weigh_cc.py | python3

Diet (reversible, gated, hash-verified backup first):
  python3 cli/diet.py --dry-run

Don't trust our numbers - re-run them. There's a self-testing receipt
(builds a synthetic store, re-derives every expected figure, CI-gated
on every push):

  python3 scripts/repro_receipt.py   # ends: RECEIPT-REPRO-OK

And the receipt board is the actual point: run the weigh-in on your
machine, paste the output as a GitHub issue, your numbers go on the
public board verbatim (handle or anonymous, your choice):
  https://sweap.it/#reportcard

Happy to answer anything about the classifier, the reverse-engineered
store schemas (Hermes, Claude Code, Codex), or the restore drill.

---

# notes (do not paste)

- Post Tue-Thu, 07:00-09:00 US Eastern = founder's evening Gulf time.
  Window: Nov 3-10. Founder stays on comments all day; I draft
  replies, he posts them.
- Headline per Arrangement B above. The paper title ("Written Twice,
  Billed Once: The Defect Inside Agent Memory") appears as the repo
  README banner and first comment line, never as the HN headline.
- RISK B (from the title check): some will call the number-led
  headline linkbait or ask why "defect" is buried. Answer with the
  first comment's line 1 - the defect IS the opening. Do not argue
  about headline choice in-thread.
- Never argue pricing methodology in-thread: the $ figures are
  arithmetic on published lists (link the vendor price board
  section); ceiling framing for the 8.09 figure, per the paper.
- If someone asks about the "diet" wording: mechanics are quarantine
  + hash-verify + restore; point to rule 3 on the site's gym-rules
  board.
