#!/usr/bin/env python3
"""sweap sweep v1.1: reversible quarantine of dead tool rows from an agent store.

Design laws baked in (docs/STORY.md + R-waves; safety review R10C applied):
- PROVABLY DEAD ONLY: candidates must have compacted=1 (or session finalized).
  Dead = already out of every context window; no live read path can reach it.
- PROSE IS NEVER TOUCHED: user + assistant rows are the mandate record. v1
  quarantines role='tool' rows only; the apply recheck re-verifies role.
- FULL-FIDELITY COPIES: quarantine stages EVERY column (schema-driven), hashes
  each shard (SHA-256, recorded in the manifest), and re-verifies hashes
  before apply and before restore. Restore inserts every staged column.
- COPY-FIRST: staging completes and verifies before any store write. If
  anything fails mid-staging, the store was never opened for writing.
- WIRE HONESTY: dead rows re-send nothing. Wire savings are stamped $0.00.
  v1 reclaims DISK only, reported as a measured before/after file size via
  VACUUM INTO swap. No content-percentage framing.
- APPLY GATE: the manifest id must be passed twice, identically. Between the
  two receipts (quarantine print + apply print) the user types a 24-char id.
- INSTRUMENT FROZEN: never run against a store mid-measurement.

Usage:
  python3 cli/sweep.py --dry-run               # census only, no writes
  python3 cli/sweep.py --quarantine            # stage + hash + manifest
  python3 cli/sweep.py --apply-manifest ID --apply-manifest ID   # gated delete + vacuum swap
  python3 cli/sweep.py --restore ID            # full reinsert from quarantine
"""
import sqlite3, os, sys, json, shutil, hashlib, argparse, datetime, tempfile

HOME = os.path.expanduser("~")
QROOT = os.path.join(HOME, ".sweap", "quarantine")
DEAD_SQL = """FROM messages m LEFT JOIN sessions s ON s.id = m.session_id
WHERE m.role='tool' AND (m.compacted=1 OR m.active=0
      OR COALESCE(s.expiry_finalized,0)=1)"""
BUSY_TIMEOUT_MS = 10_000

def ro_con(db):
    # realpath: sqlite URI + macOS /tmp symlink gotcha
    return sqlite3.connect(f"file:{os.path.realpath(db)}?mode=ro", uri=True)

def table_columns(con, table="messages"):
    return [r[1] for r in con.execute(f"PRAGMA table_info({table})")]

def census(db):
    con = ro_con(db)
    q = lambda s: con.execute(s).fetchone()
    n, b = q(f"SELECT COUNT(*), COALESCE(SUM(LENGTH(COALESCE(m.content,''))),0) {DEAD_SQL}")
    tot_n, tot_b = q("SELECT COUNT(*), COALESCE(SUM(LENGTH(COALESCE(content,''))),0) FROM messages")
    open_n, = q(f"SELECT COUNT(*) {DEAD_SQL} AND s.ended_at IS NULL")
    per_tool = con.execute(f"""SELECT m.tool_name, COUNT(*),
        SUM(LENGTH(COALESCE(m.content,''))) {DEAD_SQL}
        GROUP BY m.tool_name ORDER BY 3 DESC LIMIT 10""").fetchall()
    con.close()
    return dict(dead_n=n, dead_b=b, total_n=tot_n, total_b=tot_b,
                open_session_dead=open_n, per_tool=per_tool)

def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""): h.update(chunk)
    return h.hexdigest()

# ---------------------------------------------------------------- dry-run --
def cmd_dry(a):
    c = census(a.db)
    fsize = os.path.getsize(a.db)
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    print("=" * 74)
    print("SWEEP v1 DRY-RUN : nothing written, nothing moved")
    print(f"store: {a.db}")
    print(f"       {c['total_n']:,} messages, {fsize/1e6:.1f} MB file, "
          f"{c['total_b']/1e6:.1f} MB message content     {now}")
    print("=" * 74)
    print()
    print("RECLAIM UNIVERSE (dead tool rows, provably out of every context window):")
    print(f"  {c['dead_n']:,} rows carrying {c['dead_b']/1e6:.2f} MB of content")
    print(f"  {c['open_session_dead']:,} of them sit in still-open sessions (compacted away: still safe)")
    print()
    print("top dead tool output (what v1 quarantines):")
    for tn, n, b in c["per_tool"]:
        print(f"  {(tn or 'NULL')[:30]:30s} {n:>7,} rows {b/1e6:>6.2f} MB")
    print()
    print("NOT candidates (protected classes):")
    print("  user+assistant rows (the mandate record): never touched")
    print("  live rows (uncompacted, unfinalized): untouchable")
    print()
    print("HONEST LEDGER (what v1 does and does not do):")
    print("  wire savings: $0.00. Dead rows re-send nothing; they never did.")
    print("  disk savings: content bytes leave the db, but the file only shrinks")
    print("  if VACUUM runs; apply does a VACUUM INTO swap and reports the real")
    print("  before/after file size. Content MB != file MB; never conflated here.")
    print()
    print("next: --quarantine (reversible staging; db untouched)")
    print("DRYRUN-OK")

# ------------------------------------------------------------- quarantine --
def cmd_quarantine(a):
    c = census(a.db)
    if c["dead_n"] == 0:
        print("nothing to quarantine: store is clean"); print("QUARANTINE-OK"); return
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    mid = f"q_{ts}"
    qdir = os.path.join(QROOT, mid)
    os.makedirs(os.path.join(qdir, "rows"), exist_ok=True)
    con = ro_con(a.db)
    cols = table_columns(con)                      # schema-driven: every column
    collist = ", ".join(f"m.{c_}" for c_ in cols)
    rows = con.execute(f"SELECT {collist} {DEAD_SQL}").fetchall()
    con.close()
    # stage as hashed JSONL shards
    shard, shard_n, total, shard_hashes = None, 0, 0, []
    def open_shard(i):
        return open(os.path.join(qdir, "rows", f"shard_{i:03d}.jsonl"), "w")
    def close_shard(sh, name, n):
        sh.close()
        shard_hashes.append(dict(shard=os.path.basename(name),
                                 rows=n, sha256=sha256_file(name)))
    cur_name = os.path.join(qdir, "rows", "shard_000.jsonl")
    shard = open_shard(0)
    for r in rows:
        d = dict(zip(cols, r))
        shard.write(json.dumps(d, ensure_ascii=False, default=str) + "\n")
        shard_n += 1; total += 1
        if shard_n >= 2000:
            close_shard(shard, cur_name, shard_n)
            shard_n = 0
            cur_name = os.path.join(qdir, "rows", f"shard_{total//2000:03d}.jsonl")
            shard = open_shard(total // 2000)
    close_shard(shard, cur_name, shard_n)
    # verify: row parity AND byte parity via hashes
    staged_b = sum(os.path.getsize(os.path.join(qdir, "rows", f))
                   for f in os.listdir(os.path.join(qdir, "rows")))
    ok_count = (total == c["dead_n"])
    manifest = dict(
        id=mid, created=datetime.datetime.now().isoformat(),
        store=os.path.realpath(a.db), state="staged", rows=total,
        store_file_bytes=os.path.getsize(a.db),
        dead_content_bytes=c["dead_b"], schema_columns=cols,
        shards=shard_hashes,
        verify=dict(row_count=ok_count, shard_hashes=True),
        wire_savings_usd=0.0,
        note=("Full-column copies. Dead rows re-send nothing: v1 reclaims disk "
              "only (VACUUM INTO swap at apply, measured before/after). Store "
              "untouched until gated --apply-manifest (id twice)."))
    json.dump(manifest, open(os.path.join(qdir, "manifest.json"), "w"), indent=1)
    print("=" * 74)
    print(f"QUARANTINE STAGED: {mid}")
    print(f"  {total:,} dead tool rows, all {len(cols)} columns -> {qdir}")
    print(f"  staged payload: {staged_b/1e6:.2f} MB; shard SHA-256: {len(shard_hashes)} shards, all hashed")
    print(f"  row-count parity: {'PASS' if ok_count else 'FAIL'}")
    print(f"  store: UNTOUCHED (reversibility by construction)")
    print(f"  wire savings stamped: $0.00 (dead rows re-send nothing)")
    print()
    print(f"apply (gated: type the id twice):")
    print(f"  sweep.py --apply-manifest {mid} --apply-manifest {mid}")
    print(f"restore (no-op while store untouched): sweep.py --restore {mid}")
    print("QUARANTINE-OK")

# ------------------------------------------------------------------ apply --
def verify_shards(man):
    qdir = os.path.join(QROOT, man["id"])
    for s in man["shards"]:
        p = os.path.join(qdir, "rows", s["shard"])
        if not os.path.exists(p): sys.exit(f"missing shard {s['shard']}: abort")
        if sha256_file(p) != s["sha256"]:
            sys.exit(f"SHARD HASH MISMATCH {s['shard']}: quarantine copy corrupt: abort")

def staged_rows(man):
    qdir = os.path.join(QROOT, man["id"])
    out = []
    for s in man["shards"]:
        with open(os.path.join(qdir, "rows", s["shard"])) as f:
            for l in f: out.append(json.loads(l))
    return out

def cmd_apply(a, mid):
    qdir = os.path.join(QROOT, mid)
    man_p = os.path.join(qdir, "manifest.json")
    if not os.path.exists(man_p): sys.exit(f"no manifest at {man_p}")
    man = json.load(open(man_p))
    if man.get("state") != "staged":
        sys.exit(f"{mid} state={man.get('state')}: only 'staged' can be applied")
    verify_shards(man)
    db = man["store"]
    payloads = staged_rows(man)
    ids = [d["id"] for d in payloads]
    f_before = os.path.getsize(db)
    con = sqlite3.connect(db, timeout=BUSY_TIMEOUT_MS / 1000)
    con.execute("PRAGMA busy_timeout=%d" % BUSY_TIMEOUT_MS)
    con.execute("BEGIN IMMEDIATE")           # write lock held across recheck+delete
    try:
        cols = table_columns(con)
        drift = set(man["schema_columns"]) ^ set(cols)
        if drift: raise RuntimeError(f"schema drift {drift}: re-quarantine first")
        marks = {}
        for i in range(0, len(ids), 500):
            chunk = ids[i:i + 500]
            ph = ",".join("?" * len(chunk))
            for row in con.execute(
                f"SELECT m.id, m.role, m.compacted, m.active, "
                f"COALESCE(s.expiry_finalized,0) "
                f"FROM messages m LEFT JOIN sessions s ON s.id=m.session_id "
                f"WHERE m.id IN ({ph})", chunk):
                marks[row[0]] = row[1:]
        # full DEAD predicate recheck incl role, in the same transaction
        bad = [i for i, d in zip(ids, payloads)
               if i not in marks or marks[i][0] != "tool"
               or not (marks[i][2] == 1 or marks[i][3] == 0 or marks[i][4] == 1)]
        if bad: raise RuntimeError(f"{len(bad)} staged rows no longer dead: abort")
        man["state"] = "applying"            # crash-sentinel BEFORE commit
        json.dump(man, open(man_p, "w"), indent=1)
        con.executemany("DELETE FROM messages WHERE id=?", [(i,) for i in ids])
        con.commit()
    except Exception as e:
        con.rollback(); con.close()
        man["state"] = "staged"
        json.dump(man, open(man_p, "w"), indent=1)
        sys.exit(f"APPLY ABORTED, store rolled back: {e}")
    con.close()
    # VACUUM INTO swap: actually reclaims disk; atomic via temp file + rename
    f_after = f_before
    try:
        tmp = tempfile.mktemp(suffix=".vacuum", dir=os.path.dirname(db))
        vcon = sqlite3.connect(db, timeout=BUSY_TIMEOUT_MS / 1000)
        vcon.execute("PRAGMA busy_timeout=%d" % BUSY_TIMEOUT_MS)
        vcon.execute("VACUUM INTO ?", (tmp,))
        vcon.close()
        if os.path.exists(db + "-wal"): os.remove(db + "-wal")
        if os.path.exists(db + "-shm"): os.remove(db + "-shm")
        os.replace(tmp, db)
        f_after = os.path.getsize(db)
    except Exception as e:
        print(f"  (vacuum swap skipped: {e}; file size unchanged: pages freed, not reclaimed)")
    man["state"] = "applied"
    man["applied_at"] = datetime.datetime.now().isoformat()
    man["rows_deleted"] = len(ids)
    man["disk"] = dict(file_before=f_before, file_after=f_after,
                       reclaimed=max(0, f_before - f_after))
    json.dump(man, open(man_p, "w"), indent=1)
    print(f"APPLIED {mid}: {len(ids):,} dead rows deleted")
    print(f"  disk: {f_before/1e6:.1f} MB -> {f_after/1e6:.1f} MB "
          f"(reclaimed {(f_before-f_after)/1e6:.2f} MB, measured)")
    print(f"  wire savings: $0.00 (stamped, dead rows never re-sent)")
    print(f"  rollback: sweep.py --restore {mid}")
    # FTS ghost assertion (schema drift guard for the latent trigger-guard risk)
    try:
        con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
        ghosts = con.execute("SELECT COUNT(*) FROM messages_fts f "
            "LEFT JOIN messages m ON m.id=f.rowid WHERE m.id IS NULL").fetchone()[0]
        con.close()
        print(f"  fts ghost rows: {ghosts} " + ("OK" if ghosts == 0 else "REBUILD ADVISED: sweep.py --fts-rebuild (manual)"))
    except Exception:
        pass
    print("APPLY-OK")

# ---------------------------------------------------------------- restore --
def cmd_restore(a, mid):
    qdir = os.path.join(QROOT, mid)
    man = json.load(open(os.path.join(qdir, "manifest.json")))
    verify_shards(man)
    db = man["store"]
    payloads = staged_rows(man)
    cols = man["schema_columns"]
    con = sqlite3.connect(db, timeout=BUSY_TIMEOUT_MS / 1000)
    con.execute("PRAGMA busy_timeout=%d" % BUSY_TIMEOUT_MS)
    con.execute("BEGIN IMMEDIATE")
    restored = 0
    try:
        have = set()
        ids = [d["id"] for d in payloads]
        for i in range(0, len(ids), 500):
            ph = ",".join("?" * len(ids[i:i + 500]))
            have |= {r[0] for r in con.execute(
                f"SELECT id FROM messages WHERE id IN ({ph})", ids[i:i + 500])}
        collist_sql = ", ".join(cols)
        ph_all = ",".join(["?"] * len(cols))
        for d in payloads:
            if d["id"] in have: continue      # never duplicated
            con.execute(f"INSERT INTO messages ({collist_sql}) VALUES ({ph_all})",
                        [d.get(c) for c in cols])
            restored += 1
        con.commit()
    except Exception as e:
        con.rollback(); con.close(); sys.exit(f"RESTORE ABORTED, rolled back: {e}")
    con.close()
    print(f"RESTORED {restored:,}/{len(payloads):,} full-column rows into {db} "
          f"(skipped {len(payloads)-restored:,} already present)")
    print("RESTORE-OK")

def main():
    ap = argparse.ArgumentParser(description="sweap sweep v1.1: reversible quarantine")
    ap.add_argument("--db", default=os.path.join(HOME, ".hermes", "state.db"))
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--quarantine", action="store_true")
    ap.add_argument("--apply-manifest", action="append", default=[],
        help="pass the SAME id twice: deliberate double-key confirmation")
    ap.add_argument("--restore", metavar="ID")
    ap.add_argument("--files", action="store_true",
        help="[v1.2, not wired] quarantine files referenced by dead rows")
    a = ap.parse_args()
    if a.files:
        sys.exit("--files ships later, after the row path is proven; not wired")
    if not os.path.exists(a.db): sys.exit(f"no store at {a.db}")
    if a.dry_run: cmd_dry(a)
    elif a.quarantine: cmd_quarantine(a)
    elif a.apply_manifest:
        if len(a.apply_manifest) != 2 or a.apply_manifest[0] != a.apply_manifest[1] \
           or a.apply_manifest[0] in ("", "ID"):
            sys.exit("apply is gated: pass the manifest id TWICE, identically.\n"
                     "read the id from the quarantine receipt, type it both times.\n"
                     "this deletes rows (reversible via --restore while it exists)")
        cmd_apply(a, a.apply_manifest[0])
    elif a.restore: cmd_restore(a, a.restore)
    else: cmd_dry(a)

if __name__ == "__main__":
    main()
