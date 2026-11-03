"""The ask layer measured on the cut pack: the cracker (lands the call; for the asks runs the careful solver's route,
the warehouse receipts as the record of what arrived, each receipt line kept, materials named by the material master,
gallons at its density and kilograms at 2.20462 lb/kg, each receipt in the year and quarter of its posting) and the
mirror (the default path on the call, the asks handled the same way), priced against generator/figures.json on the
weights 38 / 7 / 55.

    python3 task479/generator/ceiling.py [target]

The call is 38 over eleven items (the verdict, the total, the margin, four quarters and four year-to-date figures).
Instructions 7. The eleven ask figures are 55 / 11 each. The asks read only the purchasing files, which the call never
reads, so the two responses take the same ask readings."""
import datetime as dt
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import verify as V    # noqa: E402

TASK = os.path.dirname(HERE)


def posting_route(target):
    wms, mm, ap = V.load_purchasing(target)
    name = {k: r["Description"].split(",")[0] for k, r in mm.items()}
    by_s, by_q = {}, [0.0] * 4
    for r in wms:
        d = dt.date.fromisoformat(r["Posting Date"])
        if d.year != 2026:
            continue
        dens = float(mm[r["Material"]]["Density (lb/gal @60F)"]) if r["UoM"] == "GAL" else 2.20462262
        lb = float(r["Qty"]) * dens
        by_s[name[r["Material"]]] = by_s.get(name[r["Material"]], 0.0) + lb
        by_q[(d.month - 1) // 3] += lb
    return by_s, by_q


def invoice_route(target):
    """For the record: the invoice lines as the record of deliveries, every solvent line's quantity at its delivery
    date (subsequent debits included)."""
    wms, mm, ap = V.load_purchasing(target)
    by_s = {}
    for r in ap:
        s = V.solvent_of(r["Item Text"] or "")
        if not s or r["Doc Type"] not in ("INV", "SUB"):
            continue
        d = dt.date.fromisoformat(r["Delivery Date"])
        if d.year != 2026:
            continue
        lb = float(r["Qty"]) * (float(mm[V.DENSITY[s]]["Density (lb/gal @60F)"]) if r["UoM"] == "GAL" else 2.20462262)
        by_s[s] = by_s.get(s, 0.0) + lb
    return by_s


def r100(x):
    return "{:,}".format(int(round(x / 100.0)) * 100)


def main(target=None):
    target = target or os.path.join(TASK, "target")
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    by_s, by_q = posting_route(target)
    rows = []
    for s, want in fig["ask_b"].items():
        got = r100(by_s.get(s, 0.0))
        rows.append(("ask B %s" % s, got, want))
    for k in range(4):
        rows.append(("ask A Q%d" % (k + 1), r100(by_q[k]), fig["ask_a"]["Q%d" % (k + 1)]))
    if len(rows) != 11 or not all(w for _, g, w in rows):
        raise SystemExit("ceiling: expected 11 ask figures in figures.json, found %d; nothing to measure" % len(rows))
    kept = sum(g == w for _, g, w in rows)
    for label, got, want in rows:
        print("cracker %-22s %12s against %12s  %s" % (label, got, want, "hit" if got == want else "miss"))
    inv = invoice_route(target)
    kept_inv = sum(r100(inv.get(s, 0.0)) == w for s, w in fig["ask_b"].items())
    print("invoice-line route (subsequent debits counted): %d of 7 solvent figures" % kept_inv)
    # the mirror's main block: the default path (tested destruction on every vented pound, offline minutes uncontrolled)
    g = V.golden_figures(target)
    e = V.emitted(g["flow"], g["voc"], g["run"], g["fan"], g["dre"], capacity=False)
    q = [x / 2000 for x in V.quarters_lb(e)]
    r1 = lambda x: "%.1f" % round(x + 1e-12, 1)
    ytd = np.cumsum(q)
    main = [("verdict", "over" if sum(q) > g["limit"] else "within", fig["call"]["verdict"]),
            ("total", r1(sum(q)), fig["call"]["total_tons"]), ("margin", r1(sum(q) - g["limit"]), fig["call"]["margin_tons"])]
    main += [("Q%d" % (k + 1), r1(q[k]), fig["quarters"]["Q%d" % (k + 1)]["tons"]) for k in range(4)]
    main += [("YTD Q%d" % (k + 1), r1(ytd[k]), fig["quarters"]["Q%d" % (k + 1)]["ytd_tons"]) for k in range(4)]
    m_hit = sum(a == b for _, a, b in main)
    C = 38 + 7 + 55.0 / 11 * kept
    S = 38.0 / 11 * m_hit + 7 + 55.0 / 11 * kept
    print("cracker: call landed (38), instructions (7), ask figures kept %d of 11: %.1f" % (kept, C))
    print("mirror (the default path, %s tons): main items kept %d of 11, ask figures kept %d of 11: %.1f"
          % (r1(sum(q)), m_hit, kept, S))
    print("Mirror leakage: %.1f per cent of ask weight" % (100.0 * kept / 11))
    print("Pair ceiling: %.1f" % ((C + S) / 2))
    return (C + S) / 2, rows


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
