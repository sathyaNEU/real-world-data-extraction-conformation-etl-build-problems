"""Pick a texture salt per build so the design's margins hold and every two-decimal figure sits clear
of its rounding edge. The salts re-draw only the communications texture of that build's installations;
the design parameters do not change. Run once; the chosen salts are written into world.SALT by hand."""
import math
import sys

import numpy as np

import world as W
import sim as S

REF, K = W.REFERENCE, W.K_SE


def figures(shares_cut, shares_late, reads, a_cut, nstream, shares_rows):
    n = len(shares_cut)
    rh = shares_cut.mean()
    se = shares_cut.std(ddof=1) / math.sqrt(n)
    lcl = REF - K * se
    p = a_cut.sum() / reads.sum()
    pooled = 100 * p
    lcl_bin = REF - K * 100 * math.sqrt((rh / 100) * (1 - rh / 100) / reads.sum())
    row = (shares_cut * nstream).sum() / nstream.sum()
    late = shares_late.mean()
    lcl_late = REF - K * shares_late.std(ddof=1) / math.sqrt(n)
    rows = shares_rows.mean()
    lcl_rows = REF - K * shares_rows.std(ddof=1) / math.sqrt(n)
    return dict(n=n, rh=rh, lcl=lcl, pooled=pooled, lcl_bin=lcl_bin, row=row, late=late, lcl_late=lcl_late,
                rows=rows, lcl_rows=lcl_rows)


def edge(x):
    """Distance from x to the nearest two-decimal rounding edge (the x.xx5 points)."""
    return abs((x * 100) % 1 - 0.5) / 100


def ok(b, f):
    if min(edge(f["rh"]), edge(f["lcl"])) < 0.0015:
        return False
    m = f["rh"] - f["lcl"]
    c = {
        "EM3.10.9": m <= -0.2,
        "EM3.11.4": m >= 0.2,
        "EM3.12.0": 0.045 <= m <= 0.12 and f["rh"] < f["lcl_bin"] - 0.012 and f["rh"] < 99.49,
        "EM3.12.1": m <= -0.2 and f["pooled"] >= 99.52,
        "EM3.12.2": m >= 0.2,
        "PX5.2.7": m <= -0.2 and f["late"] - f["lcl_late"] >= 0.2 and f["rows"] - f["lcl_rows"] >= 0.15,
        "PX5.3.0": 0.07 <= m and f["row"] < f["lcl"] - 0.08 and f["pooled"] < f["lcl"] - 0.3,
        "PX5.3.1": m >= 0.5 and f["rh"] < f["lcl_bin"] - 0.1,
    }[b]
    return c


def run(b, salt):
    W.SALT[b] = salt
    insts = S.simulate()
    sel = [i for i in insts if i.group == "full" and i.build_start == b]
    sc, sl, rd, ac, ns, sr = [], [], [], [], [], []
    for i in sel:
        dc = S.day_counts(i)
        k = len(W.PROFILES[i.profile][0])
        exp = sum(x[0] for x in dc)
        cut = exp - sum(x[2] + x[3] for x in dc)
        late = exp - sum(x[3] for x in dc)
        present = [x for x in dc if x[0] - x[2] - x[3] > 0]
        sr.append(100 * sum(x[0] - x[2] - x[3] for x in present) / max(1, sum(x[0] for x in present)))
        sc.append(100 * cut / exp); sl.append(100 * late / exp); rd.append(exp * k); ac.append(cut * k); ns.append(k)
    return figures(np.array(sc), np.array(sl), np.array(rd, float), np.array(ac, float), np.array(ns, float), np.array(sr))


if __name__ == "__main__":
    out, margins = {}, []
    for b in W.RELEASES:
        for salt in range(0, 400):
            f = run(b, salt)
            m = f["rh"] - f["lcl"]
            if ok(b, f) and all(abs(m - x) >= 0.04 for x in margins):
                margins.append(m)
                out[b] = salt
                print(b, salt, {k: round(v, 4) for k, v in f.items()})
                break
        else:
            print("NO SALT", b)
        W.SALT.clear()
        W.SALT.update(out)
    print(out)
