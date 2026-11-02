"""Tuning aid (not part of the build): bin-edge distances for the graded figures under the licensed variants.

    python3 task149/generator/tune.py <scratch_target>"""
import collections
import datetime as dt
import sys

import analysis as A
import params as P
import world as W


def edge(x, step):
    r = x / step
    return min(r - int(r) - 0.0, int(r) + 1 - r) * step if False else abs((x / step) - round(x / step) - 0.5 * (1 if (x / step) - round(x / step) >= 0 else -1)) * step


def dist(x, step):
    """Distance from x to the nearest rounding edge at the given step."""
    q = x / step
    frac = q - int(q)
    return min(abs(frac - 0.5), 1.0) * step if True else 0


def main(tgt):
    D = A.load(tgt)
    W0 = A.workers(D)
    f, _ = A.frequencies(D, W0)
    rows, tot = A.boardings(D, f)
    print("golden", round(tot, 2))
    variants = {"base": W0, "long210": A.workers(D, long_min=210), "long270": A.workers(D, long_min=270),
                "long300": A.workers(D, long_min=300), "majority": A.workers(D, rule="majority"),
                "minlong5": A.workers(D, min_long=5)}
    fv = {k: A.frequencies(D, v)[0] for k, v in variants.items()}
    fv["devmean"] = A.frequencies(D, W0, mode="mean")[0]
    fv["split"] = A.frequencies(D, A.workers(D, straddle="split"))[0]
    print("per-destination boardings (nearest 10): value, min-max over variants, edge distance of base")
    for z, s in sorted(D["shares"].items()):
        if s == 0:
            continue
        vals = [D["census"][z] * s * fv[k].get(z, 0) for k in fv]
        b = D["census"][z] * s * f[z]
        same = len({round(v / 10) for v in vals}) == 1
        print(z, s, round(b, 2), round(min(vals), 2), round(max(vals), 2), "edge", round(dist(b, 10), 2), "SAME" if same else "SPLIT")
    for win in [(420, 570), (390, 540), (405, 555), (420, 540), (435, 555), (390, 570), (420, 600), (360, 540), (450, 570)]:
        A.AM = win
        res = {k: A.departures(D, v)[0] for k, v in variants.items()}
        bad = []
        for z in sorted(res["base"]):
            if D["shares"].get(z, 0) == 0:
                continue
            vals = [100 * res[k][z] for k in res]
            if len({round(v) for v in vals}) > 1 or dist(100 * res["base"][z], 1) < 0.15:
                bad.append((z, round(100 * res["base"][z], 2)))
        print("window", win, "bad", bad)


if __name__ == "__main__":
    main(sys.argv[1])
