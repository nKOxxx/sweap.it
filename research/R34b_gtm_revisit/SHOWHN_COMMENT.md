# Show HN first comment (paste the moment the post is live)

Builder here. sweap answers a question nobody was asking out loud:
how big is your AI agent's memory store, really, and how much of it
is dead?

Short version of what we found measuring our own machines:

- A production agent store (238 MB on disk) held 90.69% dead tool
  output in its stored transcripts (n=37,813 rows, exact count).
- One reversible diet cut 37.57 MB and lost zero bytes of memory:
  every removal is hash-verified and restorable, drilled against
  schema changes.
- It comes back: ~431 exhaust rows/day regrow after a clean, so
  memory hygiene is a recurring discipline, not a one-time cleanup.
- Dead weight has a carrying charge: after a memory lapse the whole
  pile gets re-read at cache-miss prices. At published list prices
  that is $0.49/1M junk tokens (GLM-4.6) to $2.70/1M (Claude), about
  $8 per lapse on our store. Arithmetic on public price lists, no
  modeling.

The tool is free, Apache-2.0, Python stdlib only, runs offline, no
account. Two commands:

Weigh (read-only, 30s, Claude Code stores, nothing to clone):
  curl -sL https://raw.githubusercontent.com/nKOxxx/sweap.it/main/cli/weigh_cc.py | python3

Diet (reversible, gated, hash-verified backup first):
  python3 cli/diet.py --dry-run

Don't trust our numbers - re-run them. There's a self-testing receipt
(script builds a synthetic store and re-derives every expected figure,
CI-enforced on every push):

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
- Founder stays on comments all day; I draft replies, he posts them.
- Title of the post itself: "Show HN: Sweap - measure and reversibly
  shrink your AI agent's memory store"
- If someone asks about the "diet" wording: it's a trainer metaphor,
  the mechanics are quarantine + hash-verify + restore; point to rule
  3 on the site's gym-rules board.
- Never argue pricing methodology in-thread: the $ table is arithmetic
  on published lists (link the vendor price board section); say that
  and link it.
