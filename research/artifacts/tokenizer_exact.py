#!/usr/bin/env python3
"""EXACT full-store token count: every message row, o200k_base. No sampling."""
import sqlite3, os, json
import tiktoken

db = os.path.expanduser('~/.hermes/state.db')
con = sqlite3.connect(f'file:{db}?mode=ro', uri=True)
enc = tiktoken.get_encoding('o200k_base')

tok = {'tool content': 0, 'assistant tool_calls': 0, 'assistant prose': 0, 'user': 0}
n_done = 0
for role, content, tcalls in con.execute("SELECT role, content, tool_calls FROM messages"):
    n_done += 1
    if role == 'tool' and content:
        tok['tool content'] += len(enc.encode(content))
    elif role == 'assistant':
        if tcalls:
            tok['assistant tool_calls'] += len(enc.encode(tcalls))
        if content:
            tok['assistant prose'] += len(enc.encode(content))
    elif role == 'user' and content:
        tok['user'] += len(enc.encode(content))

total = sum(tok.values())
exh = (tok['tool content'] + tok['assistant tool_calls']) / total * 100
print(f"rows scanned: {n_done}")
for k, v in tok.items():
    print(f"  {k:24s} {v:>12,} tokens  share={v/total*100:5.2f}%")
print(f"TOTAL: {total:,} tokens")
print(f"TOOL EXHAUST TOKEN SHARE (EXACT): {exh:.2f}%")
out = json.load(open(os.path.expanduser('~/sweap.it/research/tokenizer_remeasure_20261013.json')))
out['exact_full_store'] = {'tokens': tok, 'total': total, 'exhaust_share_pct': round(exh, 2), 'rows': n_done, 'method': 'exact full-store o200k_base count'}
json.dump(out, open(os.path.expanduser('~/sweap.it/research/tokenizer_remeasure_20261013.json'), 'w'), indent=1)
print("updated JSON with exact pass")
