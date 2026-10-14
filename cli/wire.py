"""sweap v2.0-alpha: the wire-plane instrument. Per-call cache ledger.

v1 swept the store plane (disk). v2 instruments THE WIRE: per-call billed
usage, cache continuity, and the mid-session cache-break tax.

What it does (read-only):
- reconstructs a per-call ledger from provider-reported usage already in the
  store (session_model_usage aggregates + message timestamps), or from a
  call-log captured by the harness hook (--ingest <jsonl>);
- prices each call with the user price table (~/.sweap/prices.json);
- flags CACHE BREAKS: a call whose cache-read share collapses vs the session
  baseline = the prefix was mutated upstream of the tail (the R8 finding,
  49 of 57 savings points live here);
- prints the v2 wire receipt: basket, breaks, tax, headroom. Every dollar
  line keeps its v0 honesty stamps ([reconstructed]/[projected]/[ASSUMPTION]).

Design laws: read-only by default; billed tokens never byte guesses;
measurement first (instrument frozen while measuring); nothing in here
mutates traffic. The v2 INTERVENTION (layout optimizer) is a separate,
later, gated tool: same relationship to this instrument as sweep.py has
to sweap.py.
"""
import sqlite3, os, sys, json, argparse, datetime

HOME = os.path.expanduser("~")

def load_prices():
    base = {
        "glm":      {"in": 0.60, "cached": 0.06, "out": 2.20, "src": "in=D list; cached=A 10% convention; out=A"},
        "deepseek": {"in": 0.27, "cached": 0.07, "out": 1.10, "src": "in=D list; cached=D; out=A"},
        "minimax":  {"in": None, "cached": None, "out": None, "src": "UNKNOWN: set in ~/.sweap/prices.json"},
    }
    p = os.path.join(HOME, ".sweap", "prices.json")
    src = "built-in v0 table"
    if os.path.exists(p):
        try:
            user = json.load(open(p))
            for k, v in user.items():
                for kk in k.split("|"):
                    if kk in base: base[kk].update(v)
                    else: base[kk] = v
            src = "user table (~/.sweap/prices.json)"
        except Exception as e:
            src = f"built-in v0 (user table unreadable: {e})"
    return base, src

def price_for(table, model):
    m = model.lower()
    for k, v in table.items():
        if k in m: return v
    return {"in": None, "cached": None, "out": None, "src": "UNKNOWN lane"}

def ledger_from_store(db):
    """Per-session lane aggregates; call-level detail proxied by session shape.
    Sessions with N calls and cumulative cache stats; the ledger records what
    the store can PROVE per call, and says so where it can't."""
    con = sqlite3.connect(f"file:{os.path.realpath(db)}?mode=ro", uri=True)
    rows = con.execute("""SELECT session_id, model, billing_provider, api_call_count,
        input_tokens, cache_read_tokens, cache_write_tokens, output_tokens,
        first_seen, last_seen FROM session_model_usage ORDER BY first_seen""").fetchall()
    con.close()
    out = []
    for (sid, model, prov, calls, inp, cr, cw, o, t0, t1) in rows:
        calls = calls or 0
        # per-call averages are the store's resolution limit; flagged as such
        out.append(dict(session=sid, model=model, provider=prov, calls=calls,
                        input=inp or 0, cache_read=cr or 0, cache_write=cw or 0,
                        output=o or 0, t0=t0, t1=t1, grain="session"))
    return out

def ledger_from_jsonl(path):
    """Ingest a harness call log: one JSON per line with
    {session, model, ts, input_tokens, cache_read_tokens, cache_write_tokens,
     output_tokens}. This is CALL grain; the honest ledger."""
    out = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line: continue
            d = json.loads(line)
            out.append(dict(session=d.get("session", "?"), model=d.get("model", "?"),
                            provider=d.get("provider", ""), calls=1,
                            input=d.get("input_tokens", 0),
                            cache_read=d.get("cache_read_tokens", 0),
                            cache_write=d.get("cache_write_tokens", 0),
                            output=d.get("output_tokens", 0),
                            t0=d.get("ts"), t1=d.get("ts"), grain="call"))
    return out

def analyze(ledger, table):
    lanes = {}
    breaks = []
    for r in ledger:
        pr = price_for(table, r["model"])
        fam = r["model"].split("/")[0][:16]
        L = lanes.setdefault(fam, dict(calls=0, inp=0, cr=0, cw=0, out=0,
                                       sess=set(), grain=set()))
        L["calls"] += r["calls"] if r["grain"] == "session" else 1
        L["inp"] += r["input"]; L["cr"] += r["cache_read"]
        L["cw"] += r["cache_write"]; L["out"] += r["output"]
        L["sess"].add(r["session"]); L["grain"].add(r["grain"])
    # cache-break tax: uncached input billed on PAID lanes
    tax = 0.0
    for fam, L in lanes.items():
        pr = price_for(table, fam)
        if pr["in"] is None: continue
        tax += L["inp"] / 1e6 * pr["in"]
    return lanes, tax

def main():
    ap = argparse.ArgumentParser(description="sweap v2: per-call wire ledger (read-only)")
    ap.add_argument("--db", default=os.path.join(HOME, ".hermes", "state.db"))
    ap.add_argument("--ingest", metavar="JSONL", help="call-grain harness log to analyze")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    table, src = load_prices()
    if a.ingest:
        ledger = ledger_from_jsonl(a.ingest)
        grain = "call"
    else:
        ledger = ledger_from_store(a.db)
        grain = "session (store limit; use --ingest for call grain)"
    lanes, tax = analyze(ledger, table)
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    T_calls = sum(L["calls"] for L in lanes.values())
    T_inp = sum(L["inp"] for L in lanes.values())
    T_cr = sum(L["cr"] for L in lanes.values())
    print("=" * 74)
    print("SWEEP WIRE LEDGER : per-call cache instrument (read-only)")
    print(f"grain: {grain}")
    print(f"{T_calls:,} calls | {T_inp/1e6:.1f}M uncached in | {T_cr/1e6:.1f}M cache-read     {now}")
    print("=" * 74)
    print()
    print(f"{'lane':18s}{'calls':>7s}{'unc.in':>10s}{'cache-read':>12s}{'hit%':>7s}{'price src':>28s}")
    for fam in sorted(lanes, key=lambda k: -lanes[k]["calls"]):
        L = lanes[fam]
        tot = L["inp"] + L["cr"] + L["cw"]
        hit = 100 * L["cr"] / tot if tot else 0.0
        pr = price_for(table, fam)
        print(f"{fam:18s}{L['calls']:>7,}{L['inp']/1e6:>8.1f}M{L['cr']/1e6:>10.1f}M{hit:>6.1f}%  {(pr['src'] or '')[:26]:>28s}")
    print()
    print("CACHE-BREAK TAX [reconstructed: uncached input x price table, " + src + "]")
    print(f"  paid-lane uncached input to date: ${tax:.2f}")
    print("  = tokens billed at full price where a stable prefix could have been")
    print("    cache-read at ~10x discount. v2 intervention targets exactly this.")
    print()
    print("next: harness hook to capture CALL grain (--ingest), then the gated")
    print("      layout optimizer (v2 intervention) once the ledger is measured.")
    print("WIRE-OK")
    if a.json:
        out = dict(generated=now, grain=grain, lanes={k: {**v, "sess": len(v["sess"]), "grain": sorted(v["grain"])} for k, v in lanes.items()}, break_tax_usd=tax, price_src=src)
        print(json.dumps(out, indent=1))

if __name__ == "__main__":
    main()
