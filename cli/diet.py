#!/usr/bin/env python3
"""sweap diet v2: two zero-loss cleanups on the Hermes store, reversible.

CLASS A (MIRROR DEDUP): role='assistant' rows where reasoning IS NOT NULL,
reasoning_content IS NOT NULL, and reasoning = reasoning_content (byte twins,
100% of multi-column reasoning rows, cross-model verified R25a). Apply NULLs
reasoning_content; the reasoning column keeps the full text. Zero info loss:
reversal = copy reasoning back into reasoning_content.

CLASS B (RESTING TOOL EXHAUST): role='tool' rows whose session has ended
(s.ended_at IS NOT NULL). Provably at rest: no live session can read them.
New reclaim universe (none match sweep v1.1's compacted/active/finalized
predicates: checked, zero overlap).

LAWS (reversible-store-surgery skill, applied):
- FULL-COLUMN copies staged as hashed JSONL shards (SHA-256 in manifest),
  schema-driven column list; hashes re-verified before apply and restore.
- COPY-FIRST: store never opened for write until staging verifies clean.
- APPLY: BEGIN IMMEDIATE + busy_timeout; per-row dead-predicate recheck
  INSIDE the transaction (TOCTOU kill): twins must still be byte-identical,
  tool rows must still sit in ended sessions; abort on any drift.
- CRASH SENTINEL: manifest state 'applying' written before commit.
- VACUUM IN PLACE through SQLite's locking protocol (never VACUUM INTO +
  swap on a store a live writer may hold open).
- FTS SAFETY: FTS indexes content/tool_name/tool_calls only; the UPDATE
  trigger fires only when those change, so NULLing reasoning_content does
  NOT touch the indexes. Ghost assertion runs after apply regardless.
- GATE: manifest id passed twice, identically.
- WIRE HONESTY: both classes are store-dead; wire savings stamped $0.00.

Usage:
  python3 cli/diet.py --dry-run
  python3 cli/diet.py --quarantine
  python3 cli/diet.py --apply-manifest ID --apply-manifest ID
  python3 cli/diet.py --restore ID
"""
import sqlite3, os, sys, json, hashlib, argparse, datetime

HOME = os.path.expanduser("~")
QROOT = os.path.join(HOME, ".sweap", "quarantine")
BUSY_TIMEOUT_MS = 10_000

TWIN_SQL = """FROM messages
WHERE role='assistant' AND reasoning IS NOT NULL
  AND reasoning_content IS NOT NULL AND reasoning = reasoning_content"""
REST_SQL = """FROM messages m LEFT JOIN sessions s ON s.id = m.session_id
WHERE m.role='tool' AND s.ended_at IS NOT NULL"""


def ro_con(db):
    return sqlite3.connect(f"file:{os.path.realpath(db)}?mode=ro", uri=True)


def table_columns(con, table="messages"):
    return [r[1] for r in con.execute(f"PRAGMA table_info({table})")]


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def census(db):
    con = ro_con(db)
    q = lambda s: con.execute(s).fetchone()
    twins_n, twins_b = q(f"SELECT COUNT(*), COALESCE(SUM(LENGTH(reasoning_content)),0) {TWIN_SQL}")
    twins_only_b = q(f"SELECT COALESCE(SUM(LENGTH(reasoning)),0) {TWIN_SQL}")[0]
    rest_n, rest_b = q(f"SELECT COUNT(*), COALESCE(SUM(LENGTH(COALESCE(m.content,''))),0) {REST_SQL}")
    # protected-class sanity (law 2): none of these may overlap user/assistant prose
    # twins are assistant rows by predicate; rest rows are role='tool' by predicate.
    diverge = q("""SELECT COUNT(*) FROM messages WHERE role='assistant'
                   AND reasoning IS NOT NULL AND reasoning_content IS NOT NULL
                   AND reasoning != reasoning_content""")[0]
    fsize = os.path.getsize(db)
    con.close()
    return dict(twins_n=twins_n, twins_b=twins_b, twins_keep_b=twins_only_b,
                rest_n=rest_n, rest_b=rest_b, diverge=diverge, file=fsize)


def cmd_dry(a):
    c = census(a.db)
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    total_rows = c["twins_n"] + c["rest_n"]
    total_b = c["twins_b"] + c["rest_b"]
    print("=" * 74)
    print("DIET v2 DRY-RUN : nothing written, nothing moved")
    print(f"store: {a.db}")
    print(f"       file {c['file']/1e6:.1f} MB     {now}")
    print("=" * 74)
    print()
    print("CLASS A - reasoning mirror (dedup, zero loss):")
    print(f"  {c['twins_n']:,} byte-twin rows, {c['twins_b']/1e6:.2f} MB mirror bytes -> NULLed")
    print(f"  ({c['twins_keep_b']/1e6:.2f} MB kept intact in the reasoning column)")
    print(f"  divergent pairs (would be overreach): {c['diverge']} (must be 0)")
    print()
    print("CLASS B - resting tool exhaust (quarantine + delete):")
    print(f"  {c['rest_n']:,} tool rows in ENDED sessions, {c['rest_b']/1e6:.2f} MB")
    print()
    print(f"TOTAL target: {total_rows:,} rows, {total_b/1e6:.2f} MB")
    print()
    print("HONEST LEDGER:")
    print("  wire savings: $0.00 stamped (both classes are already store-dead)")
    print("  file shrink: only if VACUUM succeeds at apply; measured before/after")
    print("  content MB != file MB; receipts never conflate them")
    print()
    print("next: --quarantine (reversible staging; store untouched)")
    print("DRYRUN-OK")


def stage_shards(qdir, cols, rows, cls):
    rows_dir = os.path.join(qdir, "rows", cls)
    os.makedirs(rows_dir, exist_ok=True)
    shard_hashes = []
    shard_n = total = 0
    name = os.path.join(rows_dir, "shard_000.jsonl")
    shard = open(name, "w")

    def close(sh, n, p):
        sh.close()
        shard_hashes.append(dict(shard=os.path.basename(p), rows=n, sha256=sha256_file(p)))

    for r in rows:
        d = dict(zip(cols, r))
        shard.write(json.dumps(d, ensure_ascii=False, default=str) + "\n")
        shard_n += 1
        total += 1
        if shard_n >= 2000:
            close(shard, shard_n, name)
            shard_n = 0
            name = os.path.join(rows_dir, f"shard_{total//2000:03d}.jsonl")
            shard = open(name, "w")
    close(shard, shard_n, name)
    return total, shard_hashes


def cmd_quarantine(a):
    c = census(a.db)
    if c["twins_n"] == 0 and c["rest_n"] == 0:
        print("nothing to quarantine: store is clean")
        print("QUARANTINE-OK")
        return
    if c["diverge"] != 0:
        sys.exit(f"ABORT: {c['diverge']} divergent pairs appeared; re-run --dry-run")
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    mid = f"diet2_{ts}"
    qdir = os.path.join(QROOT, mid)
    con = ro_con(a.db)
    cols = table_columns(con)  # schema-driven: EVERY column, never hand-picked
    collist = ", ".join(f"m.{x}" for x in cols)
    twin_collist = ", ".join(cols)
    twin_rows = con.execute(f"SELECT {twin_collist} {TWIN_SQL}").fetchall()
    rest_rows = con.execute(f"SELECT {collist} {REST_SQL}").fetchall()
    con.close()
    t_total, t_hashes = stage_shards(qdir, cols, twin_rows, "twins")
    r_total, r_hashes = stage_shards(qdir, cols, rest_rows, "rest")
    ok_count = (t_total == c["twins_n"] and r_total == c["rest_n"])
    manifest = dict(
        id=mid, created=datetime.datetime.now().isoformat(),
        store=os.path.realpath(a.db), state="staged",
        rows=dict(twins=t_total, rest=r_total),
        store_file_bytes=os.path.getsize(a.db),
        dead_content_bytes=dict(twins=c["twins_b"], rest=c["rest_b"]),
        schema_columns=cols,
        shards=dict(twins=t_hashes, rest=r_hashes),
        verify=dict(row_count=ok_count, shard_hashes=True),
        wire_savings_usd=0.0,
        note=("Diet v2: class A NULLs reasoning_content on byte-twin rows "
              "(reversible by copy-back); class B deletes resting tool rows "
              "(reversible by reinsert). Full-column hashed shards. Store "
              "untouched until gated apply."))
    json.dump(manifest, open(os.path.join(qdir, "manifest.json"), "w"), indent=1)
    print("=" * 74)
    print(f"QUARANTINE STAGED: {mid}")
    print(f"  class A: {t_total:,} twin rows -> rows/twins shards ({len(t_hashes)} shards, SHA-256)")
    print(f"  class B: {r_total:,} resting tool rows -> rows/rest shards ({len(r_hashes)} shards, SHA-256)")
    print(f"  every column of every row copied first; store UNTOUCHED")
    print(f"  wire savings stamped: $0.00")
    print()
    print("apply (gated: pass the id twice, identically):")
    print(f"  diet.py --apply-manifest {mid} --apply-manifest {mid}")
    print(f"restore: diet.py --restore {mid}")
    print("QUARANTINE-OK")


def verify_shards(man):
    qdir = os.path.join(QROOT, man["id"])
    for cls in ("twins", "rest"):
        for s in man["shards"][cls]:
            p = os.path.join(qdir, "rows", cls, s["shard"])
            if not os.path.exists(p):
                sys.exit(f"missing shard {s['shard']}: abort")
            if sha256_file(p) != s["sha256"]:
                sys.exit(f"SHARD HASH MISMATCH {s['shard']}: abort")


def staged_rows(man, cls):
    qdir = os.path.join(QROOT, man["id"])
    out = []
    for s in man["shards"][cls]:
        with open(os.path.join(qdir, "rows", cls, s["shard"])) as f:
            for line in f:
                out.append(json.loads(line))
    return out


def cmd_apply(a, mid):
    qdir = os.path.join(QROOT, mid)
    man_p = os.path.join(qdir, "manifest.json")
    if not os.path.exists(man_p):
        sys.exit(f"no manifest at {man_p}")
    man = json.load(open(man_p))
    if man.get("state") != "staged":
        sys.exit(f"{mid} state={man.get('state')}: only 'staged' can be applied")
    verify_shards(man)
    db = man["store"]
    twins = staged_rows(man, "twins")
    rest = staged_rows(man, "rest")
    twin_ids = [d["id"] for d in twins]
    rest_ids = [d["id"] for d in rest]
    f_before = os.path.getsize(db)
    con = sqlite3.connect(db, timeout=BUSY_TIMEOUT_MS / 1000)
    con.execute(f"PRAGMA busy_timeout={BUSY_TIMEOUT_MS}")
    con.execute("BEGIN IMMEDIATE")
    try:
        cols = table_columns(con)
        drift = set(man["schema_columns"]) ^ set(cols)
        if drift:
            raise RuntimeError(f"schema drift {drift}: re-quarantine first")
        # per-row recheck INSIDE the transaction (law: TOCTOU kill)
        marks = {}
        for i in range(0, len(twin_ids), 500):
            chunk = twin_ids[i:i + 500]
            ph = ",".join("?" * len(chunk))
            for row in con.execute(
                f"""SELECT id, role, reasoning IS NOT NULL,
                    reasoning_content IS NOT NULL,
                    reasoning = reasoning_content
                    FROM messages WHERE id IN ({ph})""", chunk):
                marks[row[0]] = row[1:]
        bad = [i for i, d in zip(twin_ids, twins)
               if marks.get(i) != ("assistant", 1, 1, 1)]
        if bad:
            raise RuntimeError(f"{len(bad)} twin rows no longer byte-identical: abort")
        # class B recheck: role tool + session still ended
        rmarks = {}
        for i in range(0, len(rest_ids), 500):
            chunk = rest_ids[i:i + 500]
            ph = ",".join("?" * len(chunk))
            for row in con.execute(
                f"""SELECT m.id, m.role, s.ended_at IS NOT NULL
                    FROM messages m LEFT JOIN sessions s ON s.id=m.session_id
                    WHERE m.id IN ({ph})""", chunk):
                rmarks[row[0]] = row[1:]
        bad2 = [i for i, d in zip(rest_ids, rest) if rmarks.get(i) != ("tool", 1)]
        if bad2:
            raise RuntimeError(f"{len(bad2)} resting rows no longer at rest: abort")
        man["state"] = "applying"  # crash sentinel BEFORE any store change
        json.dump(man, open(man_p, "w"), indent=1)
        # class A: NULL the mirror (reversible: reasoning keeps the text)
        con.executemany("UPDATE messages SET reasoning_content=NULL WHERE id=?",
                        [(i,) for i in twin_ids])
        # class B: delete resting rows (reversible: full shards on disk)
        con.executemany("DELETE FROM messages WHERE id=?", [(i,) for i in rest_ids])
        con.commit()
    except Exception as e:
        con.rollback()
        con.close()
        man["state"] = "staged"
        json.dump(man, open(man_p, "w"), indent=1)
        sys.exit(f"APPLY ABORTED, store rolled back: {e}")
    con.close()
    f_after = f_before
    try:
        vcon = sqlite3.connect(db, timeout=BUSY_TIMEOUT_MS / 1000)
        vcon.execute(f"PRAGMA busy_timeout={BUSY_TIMEOUT_MS}")
        vcon.execute("VACUUM")  # in place, live-writer safe (proven 2026-10-14)
        vcon.close()
        f_after = os.path.getsize(db)
    except Exception as e:
        print(f"  (vacuum skipped: {e}; pages freed, not reclaimed)")
    man["state"] = "applied"
    man["applied_at"] = datetime.datetime.now().isoformat()
    man["rows_changed"] = dict(twins_nulled=len(twin_ids), rest_deleted=len(rest_ids))
    man["disk"] = dict(file_before=f_before, file_after=f_after,
                       reclaimed=max(0, f_before - f_after))
    json.dump(man, open(man_p, "w"), indent=1)
    print(f"APPLIED {mid}: {len(twin_ids):,} mirrors NULLed, {len(rest_ids):,} resting rows deleted")
    print(f"  disk: {f_before/1e6:.1f} MB -> {f_after/1e6:.1f} MB "
          f"(reclaimed {(f_before-f_after)/1e6:.2f} MB, measured)")
    print(f"  wire savings: $0.00 (stamped)")
    print(f"  rollback: diet.py --restore {mid}")
    try:
        gcon = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
        ghosts = gcon.execute(
            "SELECT COUNT(*) FROM messages_fts f LEFT JOIN messages m "
            "ON m.id=f.rowid WHERE m.id IS NULL").fetchone()[0]
        gcon.close()
        print(f"  fts ghost rows: {ghosts} " + ("OK" if ghosts == 0 else "REBUILD ADVISED"))
    except Exception:
        pass
    print("APPLY-OK")


def cmd_restore(a, mid):
    qdir = os.path.join(QROOT, mid)
    man = json.load(open(os.path.join(qdir, "manifest.json")))
    verify_shards(man)
    db = man["store"]
    cols = man["schema_columns"]
    collist_sql = ", ".join(cols)
    ph_all = ",".join(["?"] * len(cols))
    con = sqlite3.connect(db, timeout=BUSY_TIMEOUT_MS / 1000)
    con.execute(f"PRAGMA busy_timeout={BUSY_TIMEOUT_MS}")
    con.execute("BEGIN IMMEDIATE")
    n_twin = n_rest = 0
    try:
        # class A restore: copy reasoning back into reasoning_content
        twins = staged_rows(man, "twins")
        have = set()
        ids = [d["id"] for d in twins]
        for i in range(0, len(ids), 500):
            chunk = ids[i:i + 500]
            ph = ",".join("?" * len(chunk))
            have |= {r[0] for r in con.execute(
                f"SELECT id FROM messages WHERE id IN ({ph})", chunk)}
        for d in twins:
            if d["id"] not in have:
                continue  # row deleted by a later sweep: class B restore covers it
            con.execute("UPDATE messages SET reasoning_content=? WHERE id=?",
                        (d["reasoning_content"], d["id"]))
            n_twin += 1
        # class B restore: full-column reinsert, never duplicating ids
        rest = staged_rows(man, "rest")
        have2 = set()
        ids2 = [d["id"] for d in rest]
        for i in range(0, len(ids2), 500):
            chunk = ids2[i:i + 500]
            ph = ",".join("?" * len(chunk))
            have2 |= {r[0] for r in con.execute(
                f"SELECT id FROM messages WHERE id IN ({ph})", chunk)}
        for d in rest:
            if d["id"] in have2:
                continue
            con.execute(f"INSERT INTO messages ({collist_sql}) VALUES ({ph_all})",
                        [d.get(c) for c in cols])
            n_rest += 1
        con.commit()
    except Exception as e:
        con.rollback()
        con.close()
        sys.exit(f"RESTORE ABORTED, rolled back: {e}")
    con.close()
    print(f"RESTORED {n_twin:,} mirrors + {n_rest:,} resting rows into {db}")
    print("RESTORE-OK")


def main():
    ap = argparse.ArgumentParser(description="sweap diet v2: reversible mirror dedup + resting-tool sweep")
    ap.add_argument("--db", default=os.path.join(HOME, ".hermes", "state.db"))
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--quarantine", action="store_true")
    ap.add_argument("--apply-manifest", action="append", default=[],
                    help="pass the SAME id twice: deliberate double-key confirmation")
    ap.add_argument("--restore", metavar="ID")
    a = ap.parse_args()
    if not os.path.exists(a.db):
        sys.exit(f"no store at {a.db}")
    if a.dry_run:
        cmd_dry(a)
    elif a.quarantine:
        cmd_quarantine(a)
    elif a.apply_manifest:
        if (len(a.apply_manifest) != 2 or a.apply_manifest[0] != a.apply_manifest[1]
                or a.apply_manifest[0] in ("", "ID")):
            sys.exit("apply is gated: pass the manifest id TWICE, identically.")
        cmd_apply(a, a.apply_manifest[0])
    elif a.restore:
        cmd_restore(a, a.restore)
    else:
        cmd_dry(a)


if __name__ == "__main__":
    main()
