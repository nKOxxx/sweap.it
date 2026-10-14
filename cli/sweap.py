#!/usr/bin/env python3
"""sweap v0: read-only context-plane census. Prints the dollar card receipt.

Design laws baked in:
- READ-ONLY: opens the store with mode=ro; never writes, never deletes.
- BILLED tokens first (provider-reported usage), never byte guesses.
- Dollars = billed tokens x PRICE TABLE (user-editable); every dollar line
  is stamped [reconstructed] until prices are verified against invoices.
- Two planes reported separately: THE WIRE (billed flow) vs THE STORE (at rest).
v0 store adapter: Hermes state.db. v1: adapters for other agent stores.
"""
import sqlite3, os, json, sys, argparse, datetime

# price table v0: USD per 1M tokens (input, cache-read). EDIT ME / override via
# ~/.sweap/prices.json. Values marked A are ASSUMPTIONS; D are published docs.
# lane-key: substring matched against the store's model string.
PRICES_V0 = {
    "glm":      {"in": 0.60, "cached": 0.06,  "src": "in=D list; cached=A 10% convention"},
    "deepseek": {"in": 0.27, "cached": 0.07,  "src": "in=D list; cached=D cache-hit"},
    "minimax":  {"in": None, "cached": None,  "src": "UNKNOWN: set in ~/.sweap/prices.json"},
    "anthropic": {"in": 3.00, "cached": 0.30, "src": "in=D sonnet list; cached=D"},
}
REFERENCE_HIT = None  # set at runtime = user's own best lane (cache lottery)
STALE_ASSUMPTION = 0.40   # R8 A6, pure assumption, labeled
PRUNE_RATE = 0.80         # R8 I1, hypothetical lever
REF_HIT_FLOOR = 0.60      # only use best-lane reference if best >= this

def load_prices():
    p = os.path.expanduser('~/.sweap/prices.json')
    if os.path.exists(p):
        try:
            user = json.load(open(p))
            for k, v in user.items():
                for kk in k.split('|'):
                    if kk in PRICES_V0: PRICES_V0[kk].update(v)
                    else: PRICES_V0[kk] = v
            return "user table (~/.sweap/prices.json)"
        except Exception as e:
            return f"built-in v0 (user table unreadable: {e})"
    return "built-in v0"

def price_for(model):
    for k, v in PRICES_V0.items():
        if k in model.lower(): return v
    return {"in": None, "cached": None, "src": "UNKNOWN lane: add to price table"}

def main():
    ap = argparse.ArgumentParser(description='sweap census: read-only context receipt')
    ap.add_argument('--db', default=os.path.expanduser('~/.hermes/state.db'))
    ap.add_argument('--json', action='store_true', help='also dump machine-readable census')
    a = ap.parse_args()
    db = a.db
    if not os.path.exists(db):
        sys.exit(f"no store at {db}")
    con = sqlite3.connect(f'file:{db}?mode=ro', uri=True)
    q = lambda s: list(con.execute(s))

    src = load_prices()
    nsess = q("SELECT COUNT(*) FROM sessions")[0][0]
    nmsg = q("SELECT COUNT(*) FROM messages")[0][0]
    nbytes = q("SELECT COALESCE(SUM(LENGTH(content)),0) FROM messages")[0][0]

    # ---- THE WIRE: provider-reported billed usage per lane ----
    lanes = {}
    for model, calls, inp, cr, cw, out in q("""
            SELECT model, SUM(api_call_count), SUM(input_tokens),
                   SUM(COALESCE(cache_read_tokens,0)), SUM(COALESCE(cache_write_tokens,0)),
                   SUM(output_tokens)
            FROM sessions WHERE input_tokens>0 GROUP BY model"""):
        fam = model.split('/')[0][:16]
        L = lanes.setdefault(fam, dict(calls=0, unc=0, cr=0, cw=0, out=0, sess=0, percall=[]))
        L['calls'] += calls or 0; L['unc'] += inp or 0; L['cr'] += cr; L['cw'] += cw
        L['out'] += out or 0; L['sess'] += 1
        if calls:
            L['percall'].append((inp + cr + cw) / calls)

    def stat(lst):
        lst = sorted(lst); n = len(lst)
        return (lst[n//2] if n else 0, lst[n//4] if n else 0, lst[3*n//4] if n else 0)

    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    print("=" * 74)
    print("SWEEP CENSUS : context-plane receipt (read-only; nothing was modified)")
    print(f"store: {db}")
    print(f"       {nsess} sessions, {nmsg:,} messages, {nbytes/1e6:.1f} MB stored     {now}")
    print("=" * 74)
    print()
    print("THE WIRE - what providers billed (their own usage report)")
    print(f"{'lane':18s}{'calls':>7s}{'re-sent/call':>14s}{'cache hit':>10s}{'unc.in':>11s}{'cache-read':>12s}")
    wire_rows = []
    for fam, L in lanes.items():
        med, p25, p75 = stat(L['percall'])
        tot = L['unc'] + L['cr'] + L['cw']
        hit = L['cr'] / tot * 100 if tot else 0.0
        wire_rows.append((fam, L, med, hit))
        print(f"{fam:18s}{L['calls']:>7,}{med:>12,.0f}t{hit:>9.1f}%{L['unc']/1e6:>9.1f}M{L['cr']/1e6:>10.1f}M")
    print()
    print("THE STORE - what your disk carries at rest")
    ex_line, exhaust = "", None
    jf = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'research', 'tokenizer_remeasure_20261013.json')
    if os.path.exists(jf):
        try:
            ex = json.load(open(jf)).get('exact_full_store', {})
            if ex:
                exhaust = ex['exhaust_share_pct']
                ex_line = f"tool exhaust: {exhaust}% of {ex['total']:,} stored tokens (exact count, o200k)"
        except Exception:
            pass
    if not ex_line:
        ex_line = f"stored bytes: {nbytes/1e6:.1f} MB (run with a tokenizer for exact share)"
    print("  " + ex_line)
    print()
    print(f"YOUR DOLLAR CARD  [reconstructed: billed tokens x price table, {src};")
    print("                   verify prices against your invoices before quoting]")
    tot_bill = tot_unc_dollar = tot_cached_dollar = 0.0
    headroom = 0.0
    hits = []
    for fam, L, med, hit in wire_rows:
        pr = price_for(fam)
        if not pr['in']:
            print(f"  {fam:16s} price UNKNOWN -> skipped (set it in ~/.sweap/prices.json)")
            continue
        b_unc = L['unc'] / 1e6 * pr['in']
        b_cached = L['cr'] / 1e6 * pr['cached'] if pr['cached'] is not None else 0.0
        bill = b_unc + b_cached
        tot_bill += bill; tot_unc_dollar += b_unc; tot_cached_dollar += b_cached
        if pr['cached'] is not None: hits.append(hit)
        print(f"  {fam:16s} ${bill:>7.2f}  (uncached ${b_unc:.2f} + cached ${b_cached:.2f})   [{pr['src']}]")
    if hits and tot_bill:
        best = max(hits)
        # cache lottery: re-price every lane at the user's own best hit rate
        if best >= REF_HIT_FLOOR * 100:
            for fam, L, med, hit in wire_rows:
                pr = price_for(fam)
                if not pr['in'] or pr['cached'] is None: continue
                T = L['unc'] + L['cr']
                h = best / 100
                alt = T / 1e6 * (h * pr['cached'] + (1 - h) * pr['in'])
                cur = L['unc'] / 1e6 * pr['in'] + L['cr'] / 1e6 * pr['cached']
                headroom += max(0.0, cur - alt)
            print(f"  cache lottery: your best lane hits {best:.1f}%; if every lane did,")
            print(f"                 you would pay ${tot_bill - headroom:.2f} instead of ${tot_bill:.2f}"
                  f"  [projected, verification pending]")
        stale = headroom * 0 + tot_bill  # placeholder to keep names tidy
        # paperwork + stale-prune line (R8 levers, assumption-labeled)
        print(f"  prune lever: ~{int(PRUNE_RATE*100)}% of ~{int(STALE_ASSUMPTION*100)}% stale history [ASSUMPTION] would")
        print(f"               cut re-sent tokens ~{int(PRUNE_RATE*STALE_ASSUMPTION*100)}% -> save ~${tot_bill*(1-(1-PRUNE_RATE*STALE_ASSUMPTION)):.2f}/period"
              f"  [projected, verification pending]")
    print()
    print("KILL-CHECK  re-sent per call, all lanes >> 10k tokens: scenario alive" if
          all(med > 10000 for _, _, med, _ in wire_rows) else
          "KILL-CHECK  a lane at/below 10k re-sent/call: savings story weak there")
    print("-" * 74)
    print("sweap v0 reads only. cleanup/sweep with quarantine ships later, opt-in, reversible.")
    print("CARD-OK")

    if a.json:
        out = {'generated': now, 'store': db, 'sessions': nsess, 'messages': nmsg,
               'stored_bytes': nbytes, 'exhaust_share_pct': exhaust, 'lanes': {}}
        for fam, L, med, hit in wire_rows:
            out['lanes'][fam] = {k: L[k] for k in ('calls', 'unc', 'cr', 'cw', 'out', 'sess')}
            out['lanes'][fam]['resend_per_call_median'] = med
            out['lanes'][fam]['cache_hit_pct'] = hit
        json.dump(out, open(os.path.expanduser('~/sweap.it/research/sweap_census_out.json'), 'w'), indent=1)
        print("json -> research/sweap_census_out.json")

if __name__ == '__main__':
    main()
