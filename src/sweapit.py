#!/usr/bin/env python3
"""sweapit: the sweeper for your LLM stack.

Two planes, one manifest:
  host plane     files, stores, logs, scratch that agent usage accumulates
  context plane  prompt overhead, tool-schema weight, transcript tool-share,
                 session-store growth (census in v0.1, cleaning roadmap)

Commands:
  sweapit doctor                full read-only manifest (both planes)
  sweapit sweep --older-than N [--dry-run]
                                safe-set cleanup: quarantine stray images,
                                delete stale /tmp scratch, prune cron outputs
  sweapit --json doctor         machine-readable manifest

Safety law: inventory never lies (all numbers measured); sweep is gated
(dry-run default for judgment sets, quarantine before delete); system paths
and active-work paths are hard-denied; context-plane data is read-only in
v0.1 (no conversation-state surgery; native `hermes sessions prune/optimize`
are surfaced, not reimplemented).
"""
import argparse, json, os, re, shutil, sqlite3, subprocess, sys, time
from pathlib import Path

HOME = Path.home()
HERMES = HOME / ".hermes"
KEEP_TMP = {"rea", "hf_paper"}
TMP_DENY_PREFIX = ("com.apple.",)
IMAGE_EXT = {".png", ".jpg", ".jpeg", ".webp", ".gif"}
QUARANTINE = HERMES / "quarantine" / "images"
STATE_DB = HERMES / "state.db"


def du(p: Path) -> int:
    total = 0
    for root, dirs, files in os.walk(p, onerror=lambda e: None, followlinks=False):
        for f in files:
            try: total += os.lstat(os.path.join(root, f)).st_size
            except OSError: pass
    return total


def age_days(p: Path) -> float:
    try: return (time.time() - p.stat().st_mtime) / 86400
    except OSError: return -1.0


def human(n) -> str:
    n = float(n)
    for u in ("B", "K", "M", "G"):
        if n < 1024 or u == "G":
            return f"{int(n)}{u}" if u == "B" else f"{n:.1f}{u}"
        n /= 1024
    return f"{n:.1f}G"


def tmp_entries():
    out = []
    if not Path("/tmp").is_dir(): return out
    for p in Path("/tmp").iterdir():
        if any(p.name.startswith(x) for x in TMP_DENY_PREFIX): continue
        try:
            st = os.lstat(p)
            ident = (st.st_dev, st.st_ino)
            is_link = p.is_symlink()
            nlink = st.st_nlink
            out.append({"name": p.name, "size": du(p) if (p.is_dir() and not is_link) else st.st_size,
                        "age_d": round((time.time() - st.st_mtime) / 86400, 1),
                        "keep": p.name in KEEP_TMP, "ident": ident,
                        "symlink": is_link, "nlink": nlink})
        except OSError: pass
    return sorted(out, key=lambda e: -e["size"])


def image_entries():
    out = []
    if not HERMES.is_dir(): return out
    for p in HERMES.iterdir():
        if p.is_file() and p.suffix.lower() in IMAGE_EXT:
            out.append({"path": str(p), "size": p.stat().st_size, "age_d": round(age_days(p), 1)})
    return out


def cron_entries():
    d = HERMES / "cron" / "output"
    out = []
    if d.is_dir():
        for p in d.rglob("*"):
            if p.is_file():
                out.append({"path": str(p), "size": p.stat().st_size, "age_d": round(age_days(p), 1)})
    return out


def prompt_overhead():
    """Context plane: fixed per-session prompt weight, from hermes prompt-size."""
    try:
        out = subprocess.run(["hermes", "prompt-size"], capture_output=True, text=True, timeout=60).stdout
    except (OSError, subprocess.TimeoutExpired):
        return {"error": "hermes prompt-size unavailable"}
    def grab(pat):
        m = re.search(pat, out)
        return m.group(1) if m else None
    return {
        "system_prompt": grab(r"System prompt total :\s+([\d,.]+ B[^)]*\))"),
        "skills_index": grab(r"skills index\s+:\s+([\d,.]+ B)"),
        "memory": grab(r"memory\s+:\s+([\d,.]+ B)"),
        "user_profile": grab(r"user profile\s+:\s+([\d,.]+ B)"),
        "tool_schemas": grab(r"Tool schemas\s+:\s+([\d,.]+ B[^)]*\))"),
        "raw": out.strip() if out else None,
    }


def session_census():
    """Context plane: store growth + tool-share of transcript bytes (read-only)."""
    res: dict = {"db": str(STATE_DB)}
    try:
        res["db_size"] = STATE_DB.stat().st_size
    except OSError:
        res["db_size"] = None
    if not STATE_DB.exists():
        res["error"] = "no state.db"
        return res
    try:
        con = sqlite3.connect(f"file:{STATE_DB}?mode=ro", uri=True)
        cur = con.cursor()
        res["sessions"] = cur.execute("SELECT COUNT(*) FROM sessions").fetchone()[0]
        res["messages"] = cur.execute("SELECT COUNT(*) FROM messages").fetchone()[0]
        all_chars = cur.execute("SELECT SUM(LENGTH(content)) FROM messages").fetchone()[0] or 0
        tool_chars = cur.execute("SELECT SUM(LENGTH(content)) FROM messages WHERE role='tool'").fetchone()[0] or 0
        res["content_chars"] = all_chars
        res["tool_chars"] = tool_chars
        res["tool_char_share"] = round(tool_chars / all_chars, 4) if all_chars else None
        res["top_sessions"] = [
            {"session": r[0], "messages": r[1], "chars": r[2]}
            for r in cur.execute(
                "SELECT session_id, COUNT(*), SUM(LENGTH(content)) FROM messages "
                "GROUP BY session_id ORDER BY 3 DESC LIMIT 5")
        ]
        con.close()
    except sqlite3.Error as e:
        res["error"] = f"sqlite: {e}"
    return res


def native_surface():
    return {
        "sessions_prune": "hermes sessions prune --older-than 30d --dry-run",
        "storage_optimize": "hermes sessions optimize  # VACUUM, take gateway offline first",
        "checkpoints": "hermes checkpoints prune",
        "logs": "hermes logs list",
    }


def doctor() -> dict:
    tz = tmp_entries()
    iz = image_entries()
    cz = cron_entries()
    return {
        "tool": "sweapit",
        "version": "0.1.1",
        "generated": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "host_plane": {
            "tmp": {"entries": tz, "total": sum(e["size"] for e in tz),
                    "sweepable_over_7d": sum(e["size"] for e in tz if not e["keep"] and e["age_d"] > 7)},
            "stray_images": {"count": len(iz), "total": sum(i["size"] for i in iz), "entries": iz},
            "cron_outputs": {"count": len(cz), "total": sum(c["size"] for c in cz),
                             "over_30d": sum(c["size"] for c in cz if c["age_d"] > 30)},
            "stores": {
                "state_db": human(STATE_DB.stat().st_size) if STATE_DB.exists() else None,
                "logs": human(du(HERMES / "logs")) if (HERMES / "logs").is_dir() else None,
                "sessions_dir": human(du(HERMES / "sessions")) if (HERMES / "sessions").is_dir() else None,
                "skills": human(du(HERMES / "skills")) if (HERMES / "skills").is_dir() else None,
            },
        },
        "context_plane": {
            "prompt_overhead": prompt_overhead(),
            "session_census": session_census(),
        },
        "native_surface": native_surface(),
    }


def render(d: dict) -> str:
    L = [f"# sweap.it manifest {d['generated']}", ""]
    hp, cp = d["host_plane"], d["context_plane"]
    L.append("## host plane")
    t = hp["tmp"]
    L.append(f"  /tmp: {len(t['entries'])} entries, {human(t['total'])} total, {human(t['sweepable_over_7d'])} sweepable (>7d, non-keep)")
    for e in t["entries"][:10]:
        tag = "KEEP" if e["keep"] else ("old" if e["age_d"] > 7 else "recent")
        L.append(f"    {human(e['size']):>8} {e['age_d']:>6}d {tag:<7} {e['name']}")
    si = hp["stray_images"]
    L.append(f"  stray images at ~/.hermes root: {si['count']} files, {human(si['total'])}")
    co = hp["cron_outputs"]
    L.append(f"  cron outputs: {co['count']} files, {human(co['total'])} (>{30}d: {human(co['over_30d'])})")
    st = hp["stores"]
    L.append(f"  stores: state.db {st['state_db']}, logs {st['logs']}, sessions {st['sessions_dir']}, skills {st['skills']}")
    L += ["", "## context plane"]
    po = cp["prompt_overhead"]
    if "error" not in po:
        L.append(f"  fixed prompt overhead per session: {po['system_prompt']}")
        L.append(f"    skills index {po['skills_index']}, tool schemas {po['tool_schemas']}, memory+profile {(po['memory'] or '?')} + {(po['user_profile'] or '?')}")
    sc = cp["session_census"]
    if "error" not in sc:
        L.append(f"  session store: {sc['sessions']} sessions, {sc['messages']:,} messages, db {human(sc['db_size'])}")
        if sc.get("tool_char_share") is not None:
            L.append(f"  tool-output share of transcript bytes: {sc['tool_char_share']*100:.1f}%")
        for s in sc.get("top_sessions", []):
            L.append(f"    {human(s['chars']):>9} {s['messages']:>6} msgs  {s['session']}")
    L += ["", "## native surface (run after review, not reimplemented)"]
    for k, v in d["native_surface"].items():
        L.append(f"  {k}: {v}")
    return "\n".join(L)


def sweep(older_than: float, dry: bool) -> str:
    acted, freed = [], 0
    if not dry:
        (QUARANTINE / time.strftime("%Y%m%d")).mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%d")
    for i in image_entries():
        dst = QUARANTINE / stamp / Path(i["path"]).name
        freed += i["size"]
        acted.append(f"quarantine {i['path']} -> {dst}")
        if not dry: shutil.move(i["path"], dst)
    for e in tmp_entries():
        if e["keep"] or e["age_d"] <= older_than: continue
        p = Path("/tmp") / e["name"]
        try:
            st = os.lstat(p)
        except OSError:
            continue  # vanished between inventory and sweep
        if (st.st_dev, st.st_ino) != tuple(e["ident"]):
            acted.append(f"SKIP /tmp/{e['name']}: identity changed since inventory (TOCTOU guard)")
            continue
        if e["symlink"]:
            freed += 0
            acted.append(f"unlink symlink /tmp/{e['name']} (link only, target untouched)")
            if not dry: p.unlink(missing_ok=True)
            continue
        hardlink = e["nlink"] > 1
        freed += 0 if hardlink else e["size"]
        note = ", hardlink: other links keep the data, 0B truly freed" if hardlink else ""
        acted.append(f"delete /tmp/{e['name']} ({human(e['size'])}, {e['age_d']}d{note})")
        if not dry:
            shutil.rmtree(p, ignore_errors=True) if (p.is_dir() and not p.is_symlink()) else p.unlink(missing_ok=True)
    for c in cron_entries():
        if c["age_d"] <= 30: continue
        freed += c["size"]
        acted.append(f"delete {c['path']} ({human(c['size'])}, {c['age_d']}d)")
        if not dry: Path(c["path"]).unlink(missing_ok=True)
    head = f"{'DRY-RUN' if dry else 'SWEPT'}: {len(acted)} actions, {human(freed)} {'would be ' if dry else ''}freed"
    return head + ("\n" + "\n".join("  " + a for a in acted) if acted else "\n  (safe set clean)")


def main():
    ap = argparse.ArgumentParser(prog="sweapit", description="the sweeper for your LLM stack")
    ap.add_argument("mode", nargs="?", default="doctor", choices=["doctor", "sweep"])
    ap.add_argument("--older-than", type=float, default=7.0)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-dry", action="store_true", help="actually delete (sweep defaults to dry-run)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if a.mode == "doctor":
        d = doctor()
        print(json.dumps(d, indent=1) if a.json else render(d))
    else:
        print(sweep(a.older_than, dry=not a.no_dry))


if __name__ == "__main__":
    main()
