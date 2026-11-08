"""The ask layer measured on the cut pack: the careful solver's routes through each ask, and the pair arithmetic.

The cracker lands the call and runs the hygiene battery on every order file before it cuts 2025 by division: exact
duplicates and re-sent batches (none survive the check), orphan keys (every AHB article maps through its table, every
superseded group code through the master), returns netted by their own document type or sign, cancelled lines dropped,
transfers to Valuehall and to group companies dropped, AHI's case lines taken at their pack quantity, euro companies at
the rate table's 2025 average. It reads every field by its plain meaning: the AHI archive's quantity in the unit its
UOM column prints (EA); the battery finds AHL's July price credits on a non-stock code no division carries (an orphan
key) and pairs each, as a header amount, to its order's item rows by their value. The stops are the other complete
pipelines a careful solver could file. The full includer reproduces figures.json or this script exits 1. The mirror stops at the call's
most attractive wrong rung (the whole surplus at Valuehall's recovery) and runs the cracker's ask routes.

Run: python3 task458/generator/ceiling.py
"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bundle as B   # noqa: E402
import calc as C     # noqa: E402
from world import DIVISIONS  # noqa: E402

TASK = os.environ.get("T458_ROOT", os.path.dirname(HERE))
TARGET = os.path.join(TASK, "target")
W_CALL, W_IF, W_ASKS = 38.0, 7.0, 55.0
W_REC = 12.0                         # the recommendation itself inside the call side
CALL_PARTS = ("provision", "inventories", "bb", "shortfall", "excess_AHL", "excess_AHI", "excess_AHB")


def battery(target):
    """The hygiene battery's findings on the order files, printed so the route is auditable."""
    o = B.orders(target, ahi_cases="label")
    dup = int(o.duplicated(keep=False).sum())
    known = set(B.division(target))
    orphans = int((~o["code"].isin(known)).sum())
    return {"lines": len(o), "exact duplicates": dup, "orphan keys": orphans,
            "returns netted": int((o.qty < 0).sum()), "cancelled dropped": int((o.kind == "cancelled").sum()),
            "transfers dropped": int((o.kind == "transfer").sum())}


def ask_block(units, gbp, fig):
    ku = sum(1 for d in DIVISIONS if C.rnd(units[d], 1000) == fig["units_2025_by_division"][d])
    kv = sum(1 for d in DIVISIONS if C.rnd(gbp[d], 1000) == fig["sales_2025_gbp_by_division"][d])
    return ku, kv


def call_side(r, fig):
    got = {"provision": C.rnd(r["provision"], 1000000) / 1e6 == fig["provision_gbp_m"],
           "inventories": C.rnd(r["carried"], 500000) / 1e6 == fig["inventories_after_provision_gbp_m"],
           "bb": C.rnd(r["bb"], 500000) / 1e6 == fig["borrowing_base_gbp_m"],
           "shortfall": r["waiver"] and C.rnd(-r["headroom"], 250000) / 1e6 == fig["shortfall_gbp_m"]}
    for k in ("AHL", "AHI", "AHB"):
        got["excess_" + k] = C.rnd(r["excess_sub"][k], 10000) == fig["excess_by_company_gbp"][k]
    rec = W_REC if (r["waiver"] == (fig["call"] == "seek a waiver")) else 0.0
    per = (W_CALL - W_REC) / len(CALL_PARTS)
    return rec + per * sum(1 for k in CALL_PARTS if got[k])


def main():
    fig = json.load(open(os.path.join(TASK, "generator", "figures.json")))
    digest = hashlib.sha256(b"".join(open(os.path.join(TARGET, f), "rb").read() for f in sorted(os.listdir(TARGET))))
    print("ceiling measured on the cut pack (sha256 %s)" % digest.hexdigest()[:16])
    print("battery:", battery(TARGET))
    routes = {
        "full includer: archive lines before 7 July as cases, each price credit on the order line it corrects":
            dict(ahi_cases="each", price_credits="order"),
        "cracker: archive quantity as its EA label; each price credit spread over its order's lines by value":
            dict(ahi_cases="label", price_credits="spread"),
        "stop: cases handled, price credits spread over their order's lines": dict(ahi_cases="each", price_credits="spread"),
        "stop: price credits on the lines they correct, archive as labelled": dict(ahi_cases="label", price_credits="order"),
        "stop: every archive line converted at its case quantity": dict(ahi_cases="all", price_credits="order"),
        "stop: price credits spread over the customer's 2025 lines": dict(ahi_cases="each", price_credits="customer"),
        "stop: price credits left out": dict(ahi_cases="each", price_credits="dropped"),
    }
    per_fig = W_ASKS / 10.0
    kept = {}
    print("\n| Route | Units kept (of 5) | Values kept (of 5) | Ask weight kept |")
    print("|---|---|---|---|")
    for name, kw in routes.items():
        u, v = C.shipped_2025(TARGET, **kw)
        ku, kv = ask_block(u, v, fig)
        kept[name] = per_fig * (ku + kv)
        print("| %s | %d | %d | %.1f of %.0f |" % (name, ku, kv, kept[name], W_ASKS))
    full = list(routes)[0]
    if kept[full] != W_ASKS:
        print("the full includer does not reproduce figures.json")
        sys.exit(1)
    g = C.compute(TARGET)
    mirror = C.compute(TARGET, capacity="none")
    crack_name = list(routes)[1]
    crack = call_side(g, fig) + W_IF + kept[crack_name]
    mirr = call_side(mirror, fig) + W_IF + kept[crack_name]
    full_score = call_side(g, fig) + W_IF + kept[full]
    print("\ncall side: golden route %.1f of %.0f, mirror (whole surplus at Valuehall's recovery) %.1f" %
          (call_side(g, fig), W_CALL, call_side(mirror, fig)))
    print("cracker on the call: %.1f; mirror off the call: %.1f; full includer: %.1f" % (crack, mirr, full_score))
    print("Pair ceiling: %.1f (cracker %.1f with the mirror %.1f); two careful responses on the call at most %.1f each" %
          ((crack + mirr) / 2, crack, mirr, crack))
    print("Mirror leakage: %.1f per cent of ask weight" % (100.0 * kept[crack_name] / W_ASKS))
    half = max(kept[n] for n in list(routes)[2:4])
    print("Best single-device handler keeps %.1f of %.0f ask weight: %.1f on the call, %.1f off it" % (
        half, W_ASKS, call_side(g, fig) + W_IF + half, call_side(mirror, fig) + W_IF + half))
    if (crack + mirr) / 2 > 60 or crack > 70:
        sys.exit(1)


if __name__ == "__main__":
    main()
