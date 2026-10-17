#!/usr/bin/env python3
"""sweap daily regrowth snapshot (read-only).
Appends one JSON line per day to ~/.sweap/regrowth_daily.jsonl:
  date, db_file_mb, content_mb, tool_rows, tool_mb, tool_closed_mb (sweepable),
  reasoning_mirror_mb (byte-identical dup), reasoning_mb, freelist_mb.
Never writes to the store. Zero network.
"""
import sqlite3, os, json, datetime, sys

DB = os.path.expanduser('~/.hermes/state.db')
OUT = os.path.expanduser('~/.sweap/regrowth_daily.jsonl')

def main():
    today = datetime.date.today().isoformat()
    # idempotent: skip if today already recorded
    if os.path.exists(OUT):
        with open(OUT) as f:
            if any(json.loads(l).get('date') == today for l in f if l.strip()):
                print(f"{today}: already recorded, skipping")
                return 0
    con = sqlite3.connect(f'file:{DB}?mode=ro', uri=True)
    cur = con.cursor()
    q = lambda sql: cur.execute(sql).fetchone()[0] or 0
    tool_rows = q("SELECT COUNT(*) FROM messages WHERE role='tool'")
    tool_mb = q("SELECT SUM(LENGTH(content)) FROM messages WHERE role='tool'") / 1e6
    tool_closed_mb = q("""SELECT SUM(LENGTH(m.content)) FROM messages m
                          JOIN sessions s ON m.session_id=s.id
                          WHERE m.role='tool' AND s.ended_at IS NOT NULL""") / 1e6
    mirror_mb = q("""SELECT SUM(LENGTH(reasoning)) FROM messages
                     WHERE role='assistant' AND reasoning IS NOT NULL
                       AND reasoning = reasoning_content""") / 1e6
    reasoning_mb = q("SELECT SUM(LENGTH(reasoning)) FROM messages WHERE role='assistant'") / 1e6
    content_mb = q("SELECT SUM(LENGTH(content)) FROM messages") / 1e6
    freelist_mb = cur.execute("PRAGMA freelist_count").fetchone()[0] * cur.execute("PRAGMA page_size").fetchone()[0] / 1e6
    con.close()
    row = dict(date=today, db_file_mb=round(os.path.getsize(DB)/1e6, 2),
               content_mb=round(content_mb, 2), tool_rows=tool_rows,
               tool_mb=round(tool_mb, 2), tool_closed_mb=round(tool_closed_mb, 2),
               reasoning_mb=round(reasoning_mb, 2), mirror_mb=round(mirror_mb, 2),
               freelist_mb=round(freelist_mb, 2))
    with open(OUT, 'a') as f:
        f.write(json.dumps(row) + '\n')
    print(json.dumps(row))
    return 0

if __name__ == '__main__':
    sys.exit(main())
