"""The cracker and the mirror, run on the cut pack (supplemental-stumping Part 1.1, Part 7).

The cracker lands the call (the golden route), runs the hygiene battery and executes every filed rule its path
points at: Rate W-2's billing months and clock hours in prevailing time, the revenue meters, Halvern's posted
peaks, the instructions' delivery-point tables. On the delivery-point export it reads interval_end as the export
gives it (nothing in the pack states another clock), sums every meter a delivery point carries (two meters at every point all season, a third at Bench after June) and, for the services table, takes each service's substation from
the GIS service points. The mirror stops on the default path (the bench wells' energy per acre-foot carried onto the
bottomland cut) and takes the same ask paths.

Weights are Part 0's: the call and its components 38, the instructions 7, the asks 55 over every ask figure; a
response off the call keeps 5 of the 38.

    python3 cracker.py [target]"""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc       # noqa: E402
import common as C  # noqa: E402


def score(fig, A, Cc, n, e):
    hits = 0
    tot = 0
    for dp in C.DPS:
        k = dp.replace(" ", "_")
        for m in C.SEASON:
            tot += 2
            hits += int(int(round(A[(dp, m)] * 1000)) == fig["a_" + k]["2026-%02d" % m])
            hits += int(int(round(Cc[(dp, m)])) == fig["b_" + k]["2026-%02d" % m])
        tot += 2
        hits += int(n[dp] == fig["c_" + k]["services"])
        hits += int(round(e[dp], 1) == fig["c_" + k]["billed_mwh"])
    return hits, tot


def paths(P, crack=()):
    allm = None
    shift = 1 if "clock" in crack else 0
    meters = None if "check" not in crack else [m for m in P.dpi["meter_no"].unique() if m not in calc.CHECKS]
    A = calc.ask_a(P, meters=meters, shift_hours=shift)
    Cc = calc.ask_c(P, meters=meters, shift_hours=shift)
    n, e = calc.ask_b(P, use_gis_label="gis" not in crack)
    return A, Cc, n, e


def pair(keep_c, keep_m, tot):
    cr = 38 + 7 + 55.0 * keep_c / tot
    mi = 5 + 7 + 55.0 * keep_m / tot
    return cr, mi, (cr + mi) / 2


def main(target=None):
    target = target or C.TARGET
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    P = calc.Pack(target)
    out = {}
    hc, tot = score(fig, *paths(P))
    out["cracker_keeps"] = hc
    out["ask_figures"] = tot
    out["mirror_keeps"] = hc        # the mirror takes the same ask paths, off the call
    cr, mi, pr = pair(hc, hc, tot)
    out["cracker"] = round(cr, 1)
    out["mirror"] = round(mi, 1)
    out["pair"] = round(pr, 1)
    out["mirror_leakage_pct"] = round(100.0 * hc / tot, 1)
    for crack in (("clock",), ("check",), ("gis",), ("clock", "check")):
        h, _ = score(fig, *paths(P, crack))
        out["crack_" + "+".join(crack)] = {"keeps": h, "pair": round(pair(h, hc, tot)[2], 1)}
    print(json.dumps(out, indent=1))
    return out


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
