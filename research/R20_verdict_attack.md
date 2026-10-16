# R20: SECOND-ROUND POSITIONING RED-TEAM (attacks the R19 verdict)
Date: 2026-10-16. Method: DeepSeek free lane (2m47s), brief
`research/briefs/R20_verdict_attack_brief.txt`, needle
`R20-VERDICT-ATTACK-OK`. Clean: `R20_verdict_attack_clean.txt` (raw in raw/).
Em-dash 0. Hub digest; full attacks verbatim in clean file.

## WHAT THE ATTACK KILLED OR WOUNDED

- "Sweap stops paying for AI work you never asked for" = KILLED as worded
  (HIGH). We attribute breaks, we do not prevent them; "stops" promises
  prevention we don't deliver. Honest verb: FINDS AND CLEANS.
- Receipt-as-bill = WOUNDED (HIGH, three ways): 2.02% honest median may be
  small change (people ignore small bills); the empty-inbox day (96.3% hit
  lane = most days have NO breaks, so the receipt goes silent exactly when
  things go well, no daily ritual, caveman/jev speak present-tense, we'd
  speak past-tense); anger misdirected at the AI vendor, "then why am I
  paying YOU instead of them?"
- Verdict card = WOUNDED as framed (MED): nobody screenshots their own
  waste; a charge is a SHAME object. Fix: flip valence to gain: "here is
  what you GOT BACK today."
- Trust-as-headline = DEMOTED (MED x2): "cannot phone home" is unverifiable
  while the repo is private; privacy-lead reads as the anxious alternative.
  Becomes a quiet README security section, backed by public repo + tcpdump
  receipt at flip time.
- Private repo = the hole under EVERYTHING (HIGH): attribution strength is
  our one unclaimable asset, and with the repo private, a competitor can
  still say "their causes are guesses, one host." The public flip is not
  just distribution, it is the proof layer for the core claim.

## WHAT SURVIVED (worker's T5, hub-endorsed)

The ASSET survives, the FRAMING inverts:
- Core message: "Every byte your AI billed you for and never used, found
  and cleaned, with the receipt to prove it." Accusation -> RECOVERY.
- Card: gain artifact ("what you got back"), not loss artifact.
- Trust: quiet security section, loud only via the public repo.
- GATE (the worker's one number that decides the money story): 30-day
  recovered-dollar figure on the reference host once prices.json lands.
  If median daily recovery can't clear a user-noticeable threshold on most
  days, the monetizable story collapses -> stay clean-and-verify utility.

## SEQUENCE NOW GATED (all pre-decision)

1. prices.json (user's 2 z.ai numbers) -> unlocks dollar conversion.
2. 30-day ledger run (already accumulating via v3.1 sampler) -> the
   recovered-dollar figure -> decides receipt-primary vs clean-and-verify.
3. Repo flip gates (fresh-machine install, schema drill, zero-egress
   receipt) -> makes the attribution claim externally checkable.

STATUS: founder decides with both rounds on the table (R19 proposal vs
R20 inversion). Nothing shipped changes product code; this is copy-level.
