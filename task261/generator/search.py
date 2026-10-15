"""Design search after the imputation change: net worth factors for the three older groups and the older groups'
own area effect, scored on every route's ratios (tune.routes on light arrays)."""
from __future__ import annotations

import itertools
import sys

import numpy as np

import common as K
import tune as T
import world as W


def light(k, oa, design=None):
    d = W.core(design)
    nw, _ = W.wealth(d, k, oa)
    w = d["w"] * K.POPULATION_HOUSEHOLDS / d["w"].sum()
    return dict(nw=nw, wgt=w, repw=d["mult"] * w[None, :], older=d["older"], ref=d["ref"])


def score(o):
    c, q, s, b = o["older"]["zc"], o["older"]["zq"], o["older"]["zs"], o["older"]["zb"]
    rc, rq, rs = o["ref"]["zc"], o["ref"]["zq"], o["ref"]["zs"]
    m = []
    m.append(min(c[:4]) - 2.3)              # golden: apart through 55-64 | 65-74
    m.append(1.65 - abs(c[4]))              # golden: 65-74 + 75+
    m.append(1.65 - q[3])                   # default merges 55-64 + 65-74
    m.append(1.65 - abs(q[4]))
    m.append(min(q[:3]) - 2.1)
    m.append(min(abs(s[4]), abs(b[4])) - 2.3)   # SRS routes split 65-74 | 75+
    # the reference person with the contrast: off five segments by a margin (split 65-74 | 75+ or merge 55-64 | 65-74)
    m.append(max(abs(rc[4]) - 2.3, 1.65 - rc[3], 1.65 - rc[2]))
    m.append(max(1.65 - rq[3], 1.65 - rq[2], abs(rq[4]) - 2.3))
    return min(m), m


if __name__ == "__main__":
    best = []
    for k4, k5, sd5, ryp in itertools.product([1.10, 1.165, 1.23], [1.02, 1.10, 1.18], [0.0, 0.25, 0.4], [0.6, 0.7]):
        k = (1, 1, 1, 1, k4, k5)
        o = T.routes(light(k, (0.0, sd5), dict(ref_younger_p=ryp)))
        sc, m = score(o)
        best.append((sc, k4, k5, sd5, ryp, np.round(m, 2)))
        print("%.3f k4 %.3f k5 %.3f sd5 %.2f ryp %.2f %s" % (sc, k4, k5, sd5, ryp, np.round(m, 2)), flush=True)
    best.sort(key=lambda x: -x[0])
    print("BEST", best[:5])
