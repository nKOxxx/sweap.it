# DECISIONS (sweap.it)

## 2026-10-15: caveman.so adoption, clean-room, license-cleared
- caveman repo `JuliusBrussee/caveman` verified **Apache-2.0** (GitHub API). Not AGPL.
  Copying their approach is license-safe at every level; even code reuse would be
  allowed with attribution.
- Decision: **pattern adoption only, clean-room.** We never read their source; the
  R12 harvest used their README, site, HN thread, and release metadata. Everything
  sweap ships is written from our own store measurements. Nothing to attribute,
  credit given anyway in README (they validated the category).
- Positioning law intact: complementary, never competitor. They compress the wire
  (in-flight proxy); we audit the store (read-only census + verified sweep).
- GTM moves copied (from R12 report): self-describing artifact, receipt-as-demo,
  one falsifiable number in the artifact, ship-raw-fast, no promotion until
  strangers find it, no monetization until demand+metric+gap are all measured.

## 2026-10-17: DNS flip executed by agent (user's GoDaddy API token)
- User volunteered a GoDaddy API token ("go wild") with standing rules: stored in
  ~/.hermes/.env (0600), never echoed, never committed.
- Agent-executed: PUT A/@ -> 185.199.108-111.153 (replaced GoDaddy parking A
  160.153.0.108; first attempt via /records/A hit INVALID_BODY demanding name/type,
  /records/A/@ accepted), PUT CNAME/www -> nkoxxx.github.io (replaced @ placeholder).
  Readback-verified; authoritative NS (ns81/ns82.domaincontrol.com) serving Pages
  IPs within minutes; public 1.1.1.1 propagated ~2 min (old parking TTL 1h).
- http://sweap.it serving site (200, verified title) before cert. Cert issuance in
  progress; https_enforced flip queued once cert lands.
- Same-day: R30 trim-1 competitive research filed (different layers, complementary;
  falsifiers on file; site untouched per user law). Gitleaks gate queued at flip.
