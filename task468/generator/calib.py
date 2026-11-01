"""Design-time screen, run on the world before any file is cut: each ward's 2025 to 2026 index change on every
standard pair and on the pairs with no building work between the sales, plus the median route."""
import sys
from collections import defaultdict

import numpy as np

import params as P
import world as Wm


def bmn(pairs, years=P.YEARS):
    """pairs: list of (year1, year2, log ratio). Annual BMN by OLS, first year the base. Returns {year: log level}"""
    idx = {y: k for k, y in enumerate(years[1:])}
    rows = [(y1, y2, lr) for y1, y2, lr in pairs if y1 != y2]
    X = np.zeros((len(rows), len(idx)))
    yv = np.zeros(len(rows))
    for k, (y1, y2, lr) in enumerate(rows):
        if y2 in idx:
            X[k, idx[y2]] += 1
        if y1 in idx:
            X[k, idx[y1]] -= 1
        yv[k] = lr
    b, *_ = np.linalg.lstsq(X, yv, rcond=None)
    out = {years[0]: 0.0}
    out.update({y: float(b[k]) for y, k in idx.items()})
    return out


def world_pairs(W, clean):
    by = defaultdict(list)
    for s in W.sales:
        if s["cat"] == "A":
            by[s["dw"]].append(s)
    works = defaultdict(list)
    for w in W.works:
        works[w["dw"]].append(w["date"])
    out = defaultdict(list)
    for i, ss in by.items():
        ss.sort(key=lambda s: s["date"])
        for a, b in zip(ss, ss[1:]):
            if clean and any(a["date"] < d < b["date"] for d in works.get(i, [])):
                continue
            out[W.dw[i]["ward"]].append((a["date"].year, b["date"].year, np.log(b["price"] / a["price"])))
    return out


def main():
    W = Wm.simulate()
    allp = world_pairs(W, False)
    clean = world_pairs(W, True)
    med = defaultdict(lambda: defaultdict(list))
    for s in W.sales:
        if s["cat"] == "A":
            med[W.dw[s["dw"]]["ward"]][s["date"].year].append(s["price"])
    print("%-14s %6s %6s %6s %6s  %5s %5s" % ("ward", "true", "all", "clean", "median", "n26", "nflip"))
    for code, name, *_ in P.WARDS:
        a = bmn(allp[name])
        c = bmn(clean[name])
        ch = lambda L: 100 * (np.exp(L[2026] - L[2025]) - 1)
        m = 100 * (np.median(med[name][2026]) / np.median(med[name][2025]) - 1)
        n26 = sum(1 for p in allp[name] if p[1] == 2026)
        nfl = sum(1 for p in allp[name] if p[1] == 2026) - sum(1 for p in clean[name] if p[1] == 2026)
        true = [w for w in P.WARDS if w[1] == name][0][5][-1]
        print("%-14s %6.2f %6.2f %6.2f %6.2f  %5d %5d" % (name, true, ch(a), ch(c), m, n26, nfl))


if __name__ == "__main__":
    main()
