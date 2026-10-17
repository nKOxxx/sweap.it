#!/usr/bin/env python3
"""sweap dollar card: price the wire ledger once prices.json is real.

Reads:
  ~/.sweap/prices.json   (founder-supplied facts; null prices = ILLUSTRATIVE mode)
  ~/.sweap/wire_ledger.jsonl  (v3 sampler rows; v2 frozen rows excluded, per-lane law)

Prints, per lane:
  - lifetime sampler-era cost, split uncached / cache-hit / output
  - the BREAK TAX: what each attributed break window cost at miss price vs
    what it would have cost at hit price (the carrying charge, measured)
  - the CACHE LOTTERY: lifetime cost vs every-lane-at-best-hit cost [counterfactual]

Law: prices are never estimated by sweap. If prices.json is unfilled, every
dollar figure prints stamped [ILLUSTRATIVE at $X/M placeholder] and exits 1
(refuses to be piped into copy). No blending across lanes, ever.
"""
import json, os, sys

HOME = os.path.expanduser("~")
PRICES = os.path.join(HOME, ".sweap", "prices.json")
LEDGER = os.path.join(HOME, ".sweap", "wire_ledger.jsonl")


def load_prices():
    if not os.path.exists(PRICES):
        sys.exit("no ~/.sweap/prices.json - the dollar layer stays off until "
                 "the founder fills real console prices (see _how_to_fill).")
    p = json.load(open(PRICES))
    real = {}
    for model, m in p.get("models", {}).items():
        if m.get("input_per_1m_usd") is not None:
            real[model] = m
    return p, real


def load_rows():
    if not os.path.exists(LEDGER):
        sys.exit("no wire ledger yet; the sampler writes it")
    out = []
    with open(LEDGER) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            if r.get("schema") == 3 and r.get("row_kind") != "merged_marker":
                out.append(r)
    return out


def cost(row, price):
    pin = price.get("input_per_1m_usd") or 0.0
    phit = price.get("cache_read_per_1m_usd") or 0.0
    pout = price.get("output_per_1m_usd") or 0.0
    return (row.get("d_input", 0) / 1e6 * pin
            + row.get("d_cache_read", 0) / 1e6 * phit
            + row.get("d_output", 0) / 1e6 * pout)


def main():
    prices_doc, real = load_prices()
    rows = load_rows()
    illustrative = False
    # per-lane law: one card per model, never blended
    lanes = {}
    for r in rows:
        m = r.get("model", "?")
        lanes.setdefault(m, []).append(r)

    for model, lrows in sorted(lanes.items()):
        p = real.get(model)
        if p is None:
            # illustrative placeholder: clearly stamped, never publishable
            p = dict(input_per_1m_usd=0.60, cache_read_per_1m_usd=0.11,
                     output_per_1m_usd=0.0)
            illustrative = True
            stamp = " [ILLUSTRATIVE at $0.60/$0.11 per 1M - NOT REAL PRICES]"
        else:
            stamp = f" [z.ai console, {prices_doc.get('updated') or 'date not stamped'}]"
        unc = sum(r.get("d_input", 0) for r in lrows)
        hit = sum(r.get("d_cache_read", 0) for r in lrows)
        out = sum(r.get("d_output", 0) for r in lrows)
        calls = sum(r.get("d_calls", 0) for r in lrows)
        c_unc = unc / 1e6 * (p["input_per_1m_usd"] or 0)
        c_hit = hit / 1e6 * (p["cache_read_per_1m_usd"] or 0)
        c_out = out / 1e6 * (p.get("output_per_1m_usd") or 0)
        total = c_unc + c_hit + c_out
        # counterfactual: same tokens, ALL at hit price (the lottery's top prize)
        all_hit = unc / 1e6 * (p["cache_read_per_1m_usd"] or c_unc and 0 or 0) + c_hit + c_out
        print("=" * 72)
        print(f"COST CARD - {model}{stamp}")
        print(f"  window: sampler v3 era ({len(lrows)} windows, {calls:,} calls)")
        print(f"  uncached input : {unc:>12,} tok  ${c_unc:>8.2f}")
        print(f"  cache-hit input: {hit:>12,} tok  ${c_hit:>8.2f}")
        if p.get("output_per_1m_usd"):
            print(f"  output         : {out:>12,} tok  ${c_out:>8.2f}")
        print(f"  TOTAL          :              ${total:>8.2f}")
        # break windows: real idle-expiry / compaction breaks are rows where
        # cache hit collapsed; attribute = hit rate < 50% with >=1000 tok uncached
        breaks = [r for r in lrows
                  if (r.get("d_cache_read", 0) + r.get("d_input", 0)) > 0
                  and r.get("d_cache_read", 0)
                  / max(1, r.get("d_cache_read", 0) + r.get("d_input", 0)) < 0.5
                  and r.get("d_input", 0) > 1000]
        tax = 0.0
        for b in breaks:
            re_read = b.get("d_input", 0)
            tax += re_read / 1e6 * ((p["input_per_1m_usd"] or 0) - (p["cache_read_per_1m_usd"] or 0))
        if breaks:
            print(f"  BREAK TAX: {len(breaks)} collapse windows, "
                  f"${tax:.2f} = the price of re-reading at miss price what "
                  f"should have been hits")
    print("=" * 72)
    if illustrative:
        print("STAMP: ILLUSTRATIVE prices - fill ~/.sweap/prices.json from the")
        print("z.ai console to convert these to real dollars. Not publishable.")
        return 1
    print("prices: founder-supplied (see prices.json source stamp)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
