"""Find a seed whose hold line sits mid-bin at two decimals under both readings the standard allows (pooled over both
arms, or averaged arm by arm). Run once; the chosen seed goes into params.SEED."""
import sys
from math import sqrt

import numpy as np

import params as P
import sim


def line_of(exps, data):
    xs, ys, parts = [], [], []
    for e, (c, t) in zip(exps, data):
        if e["kind"] != "clean":
            continue
        for a in (c, t):
            x, y = a["gaps"].astype(float), a["sess"].astype(float)
            xs.append(x)
            ys.append(y)
            r = x.sum() / y.sum()
            parts.append(((x - r * y) ** 2).sum() / (len(x) - 1) / (y.mean() ** 2))
    x, y = np.concatenate(xs), np.concatenate(ys)
    r = x.sum() / y.sum()
    s2 = ((x - r * y) ** 2).sum() / (len(x) - 1) / (y.mean() ** 2)
    f = lambda v: 100 * P.Z * sqrt(2 * v / P.STD_N)
    return f(s2), f(float(np.mean(parts)))


if __name__ == "__main__":
    s0 = int(sys.argv[1]) if len(sys.argv) > 1 else P.SEED
    for s in range(s0, s0 + 40):
        exps, data, tries = sim.corpus(s)
        a, b = line_of(exps, data)
        lo, hi = min(a, b), max(a, b)
        c = round((lo + hi) / 2, 2)
        ok = abs(lo - c) <= 0.0025 and abs(hi - c) <= 0.0025 and round(lo, 2) == round(hi, 2)
        print(s, "%.4f %.4f" % (a, b), "ok" if ok else "")
        if ok:
            break
