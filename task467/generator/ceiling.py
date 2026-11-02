"""The ask layer measured on the cut pack: the careful solver's routes through each ask, and the pair arithmetic.

The cracker lands the call, reads every field by its plain meaning (the voucher's value as the voucher system writes
it, the voucher's own order field as the order it is for, the issue time's UTC mark converted to UK time, the order
extract's category, the case's topic) and runs the hygiene battery (duplicates and re-sent rows, anti-joins and orphan
keys: every voucher's own order is in the extract, so none is orphaned; partial redemptions and statuses read as the
system writes them). The stops are the other complete pipelines a careful solver could file. The full includer
reproduces figures.json or this script exits 1. The mirror stops at the call's most attractive wrong rung (arrival
order) and runs the cracker's ask routes. Run: python3 task467/generator/ceiling.py
"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import golden as G   # noqa: E402

TASK = os.environ.get("T467_ROOT", os.path.dirname(HERE))
TARGET = os.path.join(TASK, "target")
W_CALL, W_FOLLOW, W_ASKS = 38.0, 7.0, 55.0
N_A, N_B = 6, 12                       # ask figures: A the six months, B six counts and six values
W_A, W_B = W_ASKS * N_A / (N_A + N_B), W_ASKS * N_B / (N_A + N_B)
W_REC = 14.0                            # the payment and the breach months inside the call side


def kept_a(route, gold):
    return sum(1 for k in gold if route[k] == gold[k]) / len(gold)


def kept_b(route, gold):
    cells = [(c, f) for c in G.CATS for f in ("count", "value_gbp")]
    return sum(1 for c, f in cells if route[c][f] == gold[c][f]) / len(cells)


def call_kept(fig, rung):
    """Share of the call side's weight a response on a rung keeps: the payment and breach months (W_REC between them),
    then the six months' four figures each (refunds made, late, share, met) on the rest."""
    per = (W_CALL - W_REC) / 24.0
    got = 0.0
    if rung["payment_gbp"] == fig["payment_gbp"]:
        got += W_REC / 2
    if rung["breach_months"] == fig["breach_months"]:
        got += W_REC / 2
    for k in G.MONTHS:
        g = fig["months"][k]
        late = rung["late"][k]
        made = g["refunds_made"]
        got += per                                                        # refunds made: every route has them
        got += per if late == g["refunds_late"] else 0
        got += per if round(100.0 * late / made, 1) == g["late_share_pct"] else 0
        met = "yes" if (made - late) >= 0.95 * made else "no"
        got += per if met == g["met"] else 0
    return got


def main():
    fig = json.load(open(os.path.join(TASK, "generator", "figures.json")))
    digest = hashlib.sha256(b"".join(open(os.path.join(TARGET, f), "rb").read() for f in sorted(os.listdir(TARGET))))
    print("ceiling measured on the cut pack (sha256 %s)" % digest.hexdigest()[:16])
    gold_a = {k: fig["months"][k]["vouchers_gbp"] for k in G.MONTHS}
    gold_b = fig["categories"]
    rate = G.eur_rate(TARGET)
    routes_a = {
        "full includer: each value in its customer's currency, euros at the reporting rate": G.voucher_values(TARGET),
        "cracker: the value column as pounds": G.voucher_values(TARGET, currency_from="house"),
        "stop: every value converted as euros": {k: int(round(v * rate)) for k, v in
                                                 G.voucher_values(TARGET, currency_from="house").items()},
    }
    # the refund-delay reading of 'the goodwill vouchers customer services issued'
    import bundle as B
    v = B.vouchers(TARGET)
    vv = v[v.reason == "Refund delay"].assign(month=lambda d: d.issued.dt.strftime("%Y-%m"))
    cc = G.customer_currency(TARGET)
    vv = vv.assign(gbp=vv.value * vv.customer_ref.map(lambda c: rate if cc.get(c) == "EUR" else 1.0))
    routes_a["stop: refund-delay vouchers only, currency handled"] = {k: int(round(float(vv[vv.month == k].gbp.sum())))
                                                                     for k in G.MONTHS}
    routes_b = {
        "full includer: the case's order, currency from the customer's orders": G.voucher_categories(TARGET),
        "cracker: the voucher's own order, the value as pounds": G.voucher_categories(TARGET, link="voucher",
                                                                                       currency_from="house"),
        "stop: the case's order, the value as pounds": G.voucher_categories(TARGET, link="case", currency_from="house"),
        "stop: the voucher's own order, currency handled": G.voucher_categories(TARGET, link="voucher"),
    }
    # the over-cleaning half: vouchers whose own order carries no return refund dropped as unmatched
    rf = B.return_refunds_made(TARGET)
    refunded = set(rf.order_ref)
    import pandas as pd
    vb = v[(v.reason == "Refund delay") & (v.issued >= pd.Timestamp(2026, 1, 1)) & (v.issued < pd.Timestamp(2026, 7, 1))]
    vb = vb[vb.order_ref.isin(refunded)]
    o = B.orders(TARGET).set_index("order_ref")
    cat = vb.order_ref.map(o.main_category)
    gbp = vb.value * vb.customer_ref.map(lambda c: rate if cc.get(c) == "EUR" else 1.0)
    routes_b["stop: vouchers whose own order had no refund dropped, currency handled"] = {
        c: {"count": int((cat == c).sum()), "value_gbp": int(round(float(gbp[cat == c].sum())))} for c in G.CATS}
    ok = True
    print("\nAsk A, each month's goodwill vouchers in pounds (6 figures, nearest pound): share kept")
    for name, r in routes_a.items():
        print("  %-78s kept %5.1f%%" % (name, 100 * kept_a(r, gold_a)))
    if routes_a["full includer: each value in its customer's currency, euros at the reporting rate"] != gold_a:
        print("FULL INCLUDER DOES NOT REPRODUCE figures.json (Ask A)")
        ok = False
    print("\nAsk B, refund-delay vouchers by the category of the order the refund was on (12 figures): share kept")
    for name, r in routes_b.items():
        print("  %-78s kept %5.1f%%" % (name, 100 * kept_b(r, gold_b)))
    if routes_b["full includer: the case's order, currency from the customer's orders"] != gold_b:
        print("FULL INCLUDER DOES NOT REPRODUCE figures.json (Ask B)")
        ok = False
    ka = kept_a(routes_a["cracker: the value column as pounds"], gold_a)
    kb = kept_b(routes_b["cracker: the voucher's own order, the value as pounds"], gold_b)
    best_a = max(kept_a(r, gold_a) for n, r in routes_a.items() if not n.startswith("full"))
    best_b = max(kept_b(r, gold_b) for n, r in routes_b.items() if not n.startswith("full"))
    rungs = fig["rungs"]
    mirror_call = call_kept(fig, rungs["r1_arrival_order"])
    cracker = W_CALL + W_FOLLOW + W_A * ka + W_B * kb
    mirror = mirror_call + W_FOLLOW + W_A * ka + W_B * kb
    best_careful = W_CALL + W_FOLLOW + W_A * best_a + W_B * best_b
    leakage = 100.0 * (W_A * ka + W_B * kb) / W_ASKS
    print("\nPair arithmetic (call %.0f with the payment and breach months %.0f, instructions %.0f, Ask A %.1f, Ask B %.1f):"
          % (W_CALL, W_REC, W_FOLLOW, W_A, W_B))
    print("  cracker on the call               %.1f  (asks kept: A %.0f%%, B %.0f%%)" % (cracker, 100 * ka, 100 * kb))
    print("  mirror on arrival order           %.1f  (call side kept %.1f of %.0f)" % (mirror, mirror_call, W_CALL))
    for name in ("r3_random_order", "r2_2025_shares_carried", "r5_newest_by_day"):
        print("  a response on %-22s   %.1f" % (name, call_kept(fig, rungs[name]) + W_FOLLOW + W_A * ka + W_B * kb))
    print("  pair (cracker, mirror)            %.1f" % ((cracker + mirror) / 2))
    print("  mirror leakage                    %.1f per cent of ask weight" % leakage)
    print("  two careful responses on call     %.1f each at most (the best stop on each ask)" % best_careful)
    if (cracker + mirror) / 2 > 60 or best_careful >= 70:
        ok = False
        print("PAIR OVER THE BAR")
    if ka > 0 or kb > 0:
        ok = False
        print("THE CRACKER KEEPS AN ASK FIGURE")
    if leakage >= 50:
        ok = False
        print("MIRROR LEAKAGE OVER 50")
    print("\n%s" % ("ceiling OK" if ok else "ceiling FAILED"))
    return ok


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
