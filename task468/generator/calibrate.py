"""Calibration (run once, by hand, before the pack is cut): place each class's golden projection inside its pharmacist
bin so that every reading the fork table names stays inside the same bin, and print each rung's pharmacists. It prints
the price scale per class to carry into world.PRODUCTS; the build itself never calls it.

    python3 task468/generator/calibrate.py
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import methods as M   # noqa: E402
import sim as S       # noqa: E402
import world as W     # noqa: E402


def readings(o):
    """The golden and every reading the fork table names, as projected spend by class."""
    o2 = o.copy()
    o2["seen_start"] = True
    return {"golden": M.golden(o), "cap 12": M.golden(o, cap=12), "cap 24": M.golden(o, cap=24),
            "cap 48": M.golden(o, cap=48), "band 3": M.golden(o, band=3), "band 6": M.golden(o, band=6),
            "starts at first seen": M.golden(o2), "chain": M.chain(o)}


def main():
    x = S.simulate()
    f = x["fills"]
    o = M.prepare(f[(f["date"] >= W.FIRST_MONTH) & (f["date"] <= W.LAST_DAY)])
    P = W.PER_PHARMACIST
    rd = readings(o)
    g = rd["golden"]
    scale = {}
    for c in W.CANDIDATES:
        rel = [rd[k][c] / g[c] for k in rd]
        lo, hi = min(rel), max(rel)
        q = g[c] / P
        k = int(np.floor(q))
        # centre the band of readings in [k, k + 1]
        mid = (k + 0.5) / ((lo + hi) / 2.0)
        scale[c] = mid / q
        print("%-4s quota %.2f readings x%.3f to x%.3f -> scale %.4f (band %.2f to %.2f)" % (
            c, q, lo, hi, scale[c], mid * lo, mid * hi))
    print("scales", {c: round(v, 4) for c, v in scale.items()})
    rungs = {"truth": S.truth_next_year(f), "trailing": M.trailing(o), "run_rate": M.run_rate(o),
             "analog": M.analog(o), "from_start": M.from_start(o)}
    for k, v in list(rd.items()) + list(rungs.items()):
        print("%-22s %s" % (k, " ".join("%s %d (%.2f)" % (c, int(np.ceil(v[c] / P)), v[c] / P) for c in W.CANDIDATES)))


if __name__ == "__main__":
    main()
