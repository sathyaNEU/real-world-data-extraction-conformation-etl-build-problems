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

# the pharmacist bin each class's golden is centred in
TARGET = {"IMM": 13, "MS": 6, "ONC": 5, "HCV": 0, "GLP": 6, "HIV": 5, "AST": 3, "CF": 3, "CGR": 3}


def readings(raw, o):
    """The golden and every reading the fork table names, as projected spend by class."""
    o2 = o.copy()
    o2["seen_start"] = True
    o2["eseen"] = True
    out = {"golden": M.golden(o), "cap 12": M.golden(o, cap=12), "cap 24": M.golden(o, cap=24),
           "cap 48": M.golden(o, cap=48), "band 3": M.golden(o, band=3), "band 6": M.golden(o, band=6),
           "starts at first seen": M.golden(o2), "chain": M.chain(o)}
    for g in (30, 90, 180):
        out["gap %d" % g] = M.golden(M.prepare(raw, gap=g))
    return out


def main():
    x = S.simulate()
    f = x["fills"]
    raw = f[(f["date"] >= W.FIRST_MONTH) & (f["date"] <= W.LAST_DAY)]
    o = M.prepare(raw)
    P = W.PER_PHARMACIST
    rd = readings(raw, o)
    g = rd["golden"]
    for c in W.CANDIDATES:
        rel = [rd[k][c] / g[c] for k in rd]
        lo, hi = min(rel), max(rel)
        k = TARGET[c]
        mid = (k + 0.5) / ((lo + hi) / 2.0)
        print("%-4s quota %.2f readings x%.3f to x%.3f -> scale %.4f (band %.2f to %.2f)" % (
            c, g[c] / P, lo, hi, mid / (g[c] / P), mid * lo, mid * hi))
    rungs = {"truth": S.truth_next_year(f), "first_fill": M.first_fill(o), "trailing": M.trailing(o),
             "run_rate": M.run_rate(o), "analog": M.analog(o), "from_start": M.from_start(o)}
    for k, v in list(rd.items()) + list(rungs.items()):
        print("%-22s %s" % (k, " ".join("%s %d (%.2f)" % (c, int(np.ceil(v[c] / P)), v[c] / P) for c in W.CANDIDATES)))


if __name__ == "__main__":
    main()
