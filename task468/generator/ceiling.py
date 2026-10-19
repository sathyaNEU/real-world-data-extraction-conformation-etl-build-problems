"""The pair ceiling for task468, measured on the cut pack: the cracker lands the call (the development by months since
each episode of therapy began) and reads the rebate statement's contract year as the calendar year, each product-quarter
once; the mirror stops on the best wrong rung (the same development by months since each member's first fill) and
scores the best of every wrong rebate path. Each criterion is scored against the golden,
pharmacists, spend to the nearest million and rebates to the nearest thousand as exact hits.

    python3 task468/generator/ceiling.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import numpy as np                # noqa: E402

import bundle as B                # noqa: E402
import golden as GO               # noqa: E402
import methods as M               # noqa: E402
import world as W                 # noqa: E402

TASK = os.path.dirname(HERE)
# planning weights: the main block 38 (the whole staffing 6, each class's pharmacists 2, each class's managed spend
# 1.5), instruction-following 7, the nine rebates 55
CALL, PER_PH, PER_SP = 6.0, 2.0, 1.5
IF, ASK = 7.0, 55.0


def score(name, spend, rebates, F):
    ph = M.pharmacists(spend)
    sm = {c: int(np.floor(spend[c] / 1e6 + 0.5)) for c in W.CANDIDATES}
    rk = {c: int(np.floor(rebates[c] / 1000 + 0.5)) for c in W.CANDIDATES}
    hit_ph = [c for c in W.CANDIDATES if ph[c] == F["call"]["pharmacists"][c]]
    hit_sp = [c for c in W.CANDIDATES if sm[c] == F["spend_m"][c]]
    hit_rb = [c for c in W.CANDIDATES if rk[c] == F["rebates_k"][c]]
    main = CALL * (len(hit_ph) == 9) + PER_PH * len(hit_ph) + PER_SP * len(hit_sp)
    ask = ASK * len(hit_rb) / 9.0
    tot = main + IF + ask
    print("%s: pharmacists %d of 9 (%s), spend %d of 9, rebates %d of 9 -> main %.1f + IF %.1f + asks %.1f = %.1f" % (
        name, len(hit_ph), ph, len(hit_sp), len(hit_rb), main, IF, ask, tot))
    for c in W.CANDIDATES:
        print("   %-4s pharmacists %2d (golden %2d)  spend %3d (golden %3d)  rebates %6d (golden %6d)  %s" % (
            c, ph[c], F["call"]["pharmacists"][c], sm[c], F["spend_m"][c], rk[c], F["rebates_k"][c],
            "rebate hit" if c in hit_rb else "rebate miss"))
    return tot, len(hit_rb)


def main(target):
    F = json.load(open(os.path.join(HERE, "figures.json"), encoding="utf-8"))
    g = GO.compute(target)
    crack = score("cracker (lands the call; contract year 2025 read as calendar 2025)", g["spend"],
                  B.rebates_2025(target, "calendar"), F)
    wrong_rb = {k: B.rebates_2025(target, k) for k in ("calendar", "lines", "invoiced")}
    best = max(wrong_rb, key=lambda k: sum(int(np.floor(wrong_rb[k][c] / 1000 + 0.5)) == F["rebates_k"][c]
                                           for c in W.CANDIDATES))
    mirror = score("mirror (months since first fill; rebates %s)" % best, M.first_fill(g["f"]), wrong_rb[best], F)
    pair = (crack[0] + mirror[0]) / 2.0
    print("pair ceiling %.1f (cracker %.1f with %d of 9 rebates, mirror %.1f with %d of 9); mirror leakage %.1f per "
          "cent of ask weight" % (pair, crack[0], crack[1], mirror[0], mirror[1], 100.0 * mirror[1] / 9))
    return pair


if __name__ == "__main__":
    main(os.path.join(TASK, "target"))
