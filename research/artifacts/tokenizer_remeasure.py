#!/usr/bin/env python3
"""Tokenizer re-measure: token-shares of the Hermes store, stratified sample, o200k_base."""
import sqlite3, os, json, random

db = os.path.expanduser('~/.hermes/state.db')
con = sqlite3.connect(f'file:{db}?mode=ro', uri=True)
rng = random.Random(20261013)

import tiktoken
enc = tiktoken.get_encoding('o200k_base')

def sample(field, role, n=150):
    rows = con.execute(
        f"SELECT {field} FROM messages WHERE role=? AND {field} IS NOT NULL AND LENGTH({field})>0 ORDER BY id",
        (role,)).fetchall()
    picks = rng.sample(rows, min(n, len(rows)))
    tc = tt = 0
    for (txt,) in picks:
        tc += len(txt)
        tt += len(enc.encode(txt))
    return tc, tt, len(picks)

groups = [
    ("tool content", "content", "tool"),
    ("assistant tool_calls JSON", "tool_calls", "assistant"),
    ("assistant prose", "content", "assistant"),
    ("user content", "content", "user"),
]
res = {}
for label, field, role in groups:
    c, t, n = sample(field, role)
    res[label] = (c, t, c / t if t else 0)
    print(f"{label:28s} n={n:3d} chars={c:>10,} tokens={t:>9,} chars/token={c/t:.2f}")

tot_rows = con.execute("SELECT role, SUM(LENGTH(COALESCE(content,''))+LENGTH(COALESCE(tool_calls,''))) FROM messages GROUP BY role").fetchall()
tc_json = con.execute("SELECT SUM(LENGTH(COALESCE(tool_calls,''))) FROM messages WHERE role='assistant'").fetchone()[0] or 0
b = {r[0]: r[1] or 0 for r in tot_rows}
asst_prose_b = b['assistant'] - tc_json
tok = {
    'tool content': b['tool'] / res['tool content'][2],
    'assistant tool_calls': tc_json / res['assistant tool_calls JSON'][2],
    'assistant prose': asst_prose_b / res['assistant prose'][2] if asst_prose_b > 0 else 0,
    'user': b['user'] / res['user content'][2],
}
total_tok = sum(tok.values())
print()
print("TOKEN-SHARE ESTIMATE (o200k_base, stratified sample, chars/token extrapolation):")
for k, v in tok.items():
    print(f"  {k:24s} ~{v/1e6:7.2f}M tokens  share={v/total_tok*100:5.1f}%")
exh = (tok['tool content'] + tok['assistant tool_calls']) / total_tok * 100
print(f"\nTOOL EXHAUST TOKEN SHARE: {exh:.1f}%  (byte share: 89.1%)")
out = {
    'date': '2026-10-13',
    'store': {'bytes': sum(b.values()), 'sessions': 353, 'messages': 37788},
    'sample_ratio_chars_per_token': {k: v[2] for k, v in res.items()},
    'sample_sizes': {k: None for k in res},
    'token_est': tok,
    'total_tokens_est': total_tok,
    'exhaust_token_share_pct': exh,
    'exhaust_byte_share_pct': 89.1,
    'method': 'stratified 150-row sample per class, deterministic seed 20261013, o200k_base, chars/token extrapolation to full store',
}
json.dump(out, open(os.path.expanduser('~/sweap.it/research/tokenizer_remeasure_20261013.json'), 'w'), indent=1)
print("saved -> ~/sweap.it/research/tokenizer_remeasure_20261013.json")
