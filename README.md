# sweap.it

**The sweeper for your LLM stack.** Agent use accumulates waste on two
planes: files on the host (session stores, logs, scratch, stray screenshots)
and bytes in the context (prompt overhead, tool schemas, tool exhaust in
transcripts). sweap.it measures both, gates the cleanup, and proves the
reclaim.

Measured on one real host (a 24/7 personal agent, day 0):

- 85.4% of stored transcript bytes are tool outputs (32.75 MB of 38.36 MB)
- 28.7 KB fixed system prompt + 54.3 KB tool schemas paid before the first
  user token, riding every API call
- 227 MB session store, 36,826 messages, 143 sessions in one month of use

Disk sweepers cleaned bytes on disk. sweap.it cleans bytes that are re-paid
on every call.

## Install

```bash
git clone https://github.com/nKOxxx/sweap.it
sudo ln -sf $(pwd)/sweap.it/src/sweapit.py /usr/local/bin/sweapit
```

Currently tuned for Hermes Agent hosts (`~/.hermes`); the manifest and sweep
layers are written to generalize.

## Usage

```bash
sweapit doctor                # read-only two-plane manifest
sweapit --json doctor         # machine-readable
sweapit sweep                 # dry-run by default: shows the action list
sweapit sweep --no-dry        # actually clean the safe set
sweapit sweep --older-than 3  # tighter age threshold for /tmp scratch
```

## Safety law

1. **Inventory never lies.** Every number is measured at run time, nothing
   estimated.
2. **Default to reversible.** `sweep` is dry-run unless you pass `--no-dry`;
   images are quarantined (moved, dated), never hard-deleted.
3. **Never reimplement DB surgery.** Native `hermes sessions prune/optimize`
   are surfaced as recommendations, not re-done badly.
4. **Judgment calls stay human.** The manifest lists what only a person
   should decide; the tool never auto-touches it.

## Research

This repo doubles as the lab notebook for paper #2 (working title: the same
name). See `docs/RESEARCH_LOG.md` (the build log), `research/briefs/` (the
exact briefs sent to external reviewer models), and `research/raw/` (verbatim
outputs; nothing is paraphrased into loss).

## License

MIT
