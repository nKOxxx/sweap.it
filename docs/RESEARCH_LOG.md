# Sweeper: Research Log

Product thesis + lab notebook for paper #2. Every entry dated, every number
measured, nothing invented. Em-dashes banned per house law.

## 2026-10-13: Founding

**Thesis (user decree):** build "Sweeper for LLMs", the way disk sweepers
cleaned PCs. Continuous agent use accumulates invisible waste; we measure it,
clean it safely, and the build process itself (thesis, measurements, design
decisions, dead ends, user corrections) becomes the next research paper.

**Lineage note:** the product concept emerged from our own pain. This Mac runs
a 24/7 Hermes agent (Telegram + CLI). The founder's review of the first
prototype script (sweeper.py, disk-oriented) triggered the reframe: the real
product is not "delete old files", it is context-economy hygiene for LLM
agents. Paper #1 (Agentic Institutions) measured delegation economics of a
hub; paper #2 measures the entropy of the hub itself and ships the cleaner.

## Baseline measurements (MacBitty, macOS 15.6, Hermes 1 session, 2026-10-13)

Captured via `hermes prompt-size` + `hermes sessions stats` + du/sqlite audits.
These are the paper's "day 0" figures for one host; multi-host census comes later.

| Quantity | Value | Instrument |
|---|---|---|
| Fixed prompt overhead per session | 83.9 KB total | hermes prompt-size |
| of which skills index | 14.5 KB | " |
| of which tool schemas | 54.3 KB (28 tools) | " |
| of which memory + user profile | 4.1 KB | " |
| Sessions | 143 (81 cli, 1 telegram, 61 age buckets in fs) | hermes sessions stats |
| Messages | 36,804 | " |
| state.db | 227.3 MB (+FTS index inside) | du + sqlite |
| Logs | 32 MB | du |
| Session jsonl | 16 MB | du |
| Stray screenshots at ~/.hermes root | 54 files, 16.8 MB | sweeper.py inventory |
| /tmp scratch (non-keep) | 3.4 MB visible; 6 zombie dirs >7d incl. system launchd sockets | sweeper.py dry-run |
| Ghidra download episode (one session) | 544 MB zip + 887 MB tree, deleted same day | session history |

**First observation (the dust metaphor, quantified):** a single active agent
month produced 36.8K messages and a 227 MB store, but the more interesting
number is the fixed overhead: every new session pays 84 KB before the first
user token, of which ~90% is tool+skills catalog. On a 200K-token context,
that is ~0.04% per session, small; but the same catalog rides EVERY API call
of EVERY turn. The LLM dust is not files, it is bytes that are re-paid on
every call (this echoes paper #1's re-payment law, nice continuity).

**Framing to develop (for the paper):** disk sweepers cleaned a scarce,
durable resource (bytes on disk). LLM sweepers clean a scarce, TRANSIENT
resource (context window), where waste has a per-call price and cleanup has
information-loss risk (compression = lossy sweep). Open problems we can
actually measure on ourselves: (a) context bloat census, (b) safe deletion
semantics for conversation state (what may be GC'd, what must persist),
(c) automated decluttering vs human-gated, (d) whether agents can self-sweep
without breaking their own memory (the INC-00x class of our own incident log
is the cautionary dataset).

## Design decisions (log as they happen)

1. **Thin over native first.** Hermes ships `sessions prune --dry-run`,
   `sessions optimize` (VACUUM), `checkpoints prune`, `logs list`. The product
   must not reimplement DB surgery; it orchestrates and reports. (Reinforced
   by user: "make sure to take notes as whilst building this", the tool's
   provenance and safety story matters more than its cleverness.)
2. **Inventory is the product's spine.** Sweep is the action layer; the
   manifest (what is waste, measured) is the sellable artifact, same as
   disk-sweeper "scan" screens were the UX.
3. **Report-only default.** Nothing auto-deletes until the operator says go.
   The founder's clarify-timeout during v0 planning confirmed: gating belongs
   to the human.
4. **Two planes:** (a) host plane, files, stores, logs (the v0 script);
   (b) context plane, prompts, toolsets, memory, transcripts (the product's
   actual differentiator). v0 was plane (a) only; the reframe moved the
   center of gravity to (b).
5. **Safety law inherited from paper #1:** no fabrication of recovered-space
   numbers; every claim measured; withdrawals chase every copy (INC-004
   doctrine applies to release notes, not just papers).

## Dead ends + corrections (kept for the paper's honesty section)

- v0 conflated "declutter my Mac" with "declutter the LLM stack". User
  corrected twice: it is a product, and it is for "LLM's usage".
- clarify() timeout on run-mode choice: the paper gets this as evidence that
  agent-initiated questions cannot block founder decisions; defaulting to
  report-only was the right fallback (write it up).
- ETH paper link (context management) unreachable (maintenance page) on
  2026-10-13; Substack piece retrieved (10,963 chars, prompt-engineering
  framing, in-context vs in-weight memory). Related-work triage logged.

## Next measurements queued

- Prompt-size census across sessions (how many distinct skills/toolsets were
  actually invoked vs carried).
- Transcript bloat: tool-output share of state.db messages (paper #1 measured
  75.6% on one hub session; census the whole store).
- Memory drift: chars in memory stores over time, duplicate/stale entries.
- Compression events: count + payload delta in this host's history (Hermes
  compactions are logged in-session).
