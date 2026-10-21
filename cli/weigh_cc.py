#!/usr/bin/env python3
"""sweap weigh --store claude-code
Read-only census of a Claude Code transcript store (~/.claude/projects).
Answers, in the diet frame's language:
  - how much the workspace drags (MB of transcripts)
  - how much of it is dead exhaust (tool_result share)
  - what the wire did (cache hit rate from per-call usage rows)
Zero network calls. Never writes to the store.

Usage: python3 cli/weigh_cc.py [--root ~/.claude/projects]
Output: human weigh-in + JSON line (machine card) on stdout.
"""
import argparse, glob, json, os, sys

def iter_rows(path):
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue

def tool_result_bytes(row):
    """Bytes of tool_result content in a user-role row (the exhaust)."""
    msg = row.get("message") or {}
    if row.get("type") != "user":
        return 0
    content = msg.get("content")
    total = 0
    if isinstance(content, list):
        for block in content:
            if isinstance(block, dict) and block.get("type") == "tool_result":
                c = block.get("content")
                if isinstance(c, str):
                    total += len(c.encode("utf-8", "replace"))
                elif isinstance(c, list):
                    for sub in c:
                        if isinstance(sub, dict) and sub.get("type") == "text":
                            total += len(str(sub.get("text", "")).encode("utf-8", "replace"))
    return total

def text_bytes(row):
    """Bytes of assistant text output (the useful weight, for contrast)."""
    msg = row.get("message") or {}
    if row.get("type") != "assistant":
        return 0
    content = msg.get("content")
    total = 0
    if isinstance(content, list):
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                total += len(str(block.get("text", "")).encode("utf-8", "replace"))
    return total

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=os.path.expanduser("~/.claude/projects"))
    args = ap.parse_args()

    files = sorted(glob.glob(os.path.join(args.root, "**", "*.jsonl"), recursive=True))
    if not files:
        print("no Claude Code transcripts found under", args.root)
        return 1

    S = dict(transcripts=0, bytes_total=0, tool_bytes=0, text_bytes=0,
             thinking_bytes=0, tool_use_bytes=0, attach_bytes=0,
             scaffolding_bytes=0, calls=0, cache_read=0, cache_create=0, input=0)
    for path in files:
        S["transcripts"] += 1
        raw = open(path, "rb").read()
        S["bytes_total"] += len(raw)
        accounted = 0
        for row in iter_rows(path):
            row_line = json.dumps(row).encode("utf-8", "replace")
            tb = tool_result_bytes(row)
            xb = text_bytes(row)
            tk = 0
            tu = 0
            msg = row.get("message") or {}
            c = msg.get("content")
            if row.get("type") == "assistant" and isinstance(c, list):
                for blk in c:
                    if isinstance(blk, dict) and blk.get("type") == "thinking":
                        tk += len(json.dumps(blk).encode("utf-8", "replace"))
                    elif isinstance(blk, dict) and blk.get("type") == "tool_use":
                        tu += len(json.dumps(blk).encode("utf-8", "replace"))
            ab = len(json.dumps(row).encode("utf-8", "replace")) if row.get("type") == "attachment" else 0
            S["tool_bytes"] += tb
            S["text_bytes"] += xb
            S["thinking_bytes"] += tk
            S["tool_use_bytes"] += tu
            S["attach_bytes"] += ab
            accounted += tb + xb + tk + tu + ab
        S["scaffolding_bytes"] += max(0, len(raw) - accounted)
        for row in iter_rows(path):
            msg = row.get("message") or {}
            u = msg.get("usage")
            if isinstance(u, dict):
                S["calls"] += 1
                S["cache_read"] += int(u.get("cache_read_input_tokens") or 0)
                S["cache_create"] += int(u.get("cache_creation_input_tokens") or 0)
                S["input"] += int(u.get("input_tokens") or 0)

    billed_in = S["cache_read"] + S["cache_create"] + S["input"]
    hit = 100.0 * S["cache_read"] / billed_in if billed_in else 0.0
    exhaust_pct = 100.0 * (S["tool_bytes"] + S["thinking_bytes"]) / S["bytes_total"] if S["bytes_total"] else 0.0

    mb = lambda b: b / (1024 * 1024)
    print("WEIGH-IN (Claude Code store: {})".format(args.root))
    print("  transcripts weighed:     {} files, {:.1f} MB".format(S["transcripts"], mb(S["bytes_total"])))
    print("  dead exhaust:            {:.1f} MB  ({:.1f}%: tool results + spent thinking)".format(mb(S["tool_bytes"] + S["thinking_bytes"]), exhaust_pct))
    print("    tool results:          {:.1f} MB".format(mb(S["tool_bytes"])))
    print("    spent thinking:        {:.1f} MB".format(mb(S["thinking_bytes"])))
    print("  tool calls (envelopes):  {:.1f} MB  (request records, not classified)".format(mb(S["tool_use_bytes"])))
    print("  answered text (live):    {:.1f} MB".format(mb(S["text_bytes"])))
    print("  attachments:             {:.1f} MB".format(mb(S["attach_bytes"])))
    print("  scaffolding (envelope):  {:.1f} MB".format(mb(S["scaffolding_bytes"])))
    print("WIRE TRUTH (from {} per-call usage rows):".format(S["calls"]))
    print("  cache reads:   {:>12,} tok".format(S["cache_read"]))
    print("  cache writes:  {:>12,} tok".format(S["cache_create"]))
    print("  fresh input:   {:>12,} tok".format(S["input"]))
    print("  cache hit rate: {:.1f}%".format(hit))
    card = dict(store="claude-code", host_files=S["transcripts"],
                total_mb=round(mb(S["bytes_total"]), 2),
                tool_exhaust_mb=round(mb(S["tool_bytes"]), 2),
                thinking_mb=round(mb(S["thinking_bytes"]), 2),
                tool_use_mb=round(mb(S["tool_use_bytes"]), 2),
                exhaust_pct=round(exhaust_pct, 2),
                calls=S["calls"], cache_read=S["cache_read"],
                cache_create=S["cache_create"], input=S["input"],
                hit_pct=round(hit, 2))
    print(json.dumps(card))
    return 0

if __name__ == "__main__":
    sys.exit(main())
