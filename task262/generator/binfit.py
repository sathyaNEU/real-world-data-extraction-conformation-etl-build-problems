"""Design tool: put every region's elasticity mid-bin at two decimals under every consistent estimate of the region's
transitory variance (within-family deviations over the five tax years, half the squared year-to-year changes, and
within-family deviations with the census year as a sixth year), computed as the pack's files hold the values, by
nudging the region's upper slope, which moves that region's children only."""
from __future__ import annotations

import sys

import numpy as np

import common as K
import records as RC
import world as W


def pack_arrays(R):
    """The region's values as the pack's files hold them: census income in whole 2000 dollars (a few at or below
    zero), the history in whole 2005 dollars, the children's earnings in whole current dollars."""
    inc = RC.census_income(R)
    hist = np.round(np.exp(R["xp"][R["files"], None] + R["u_tax"][R["files"]]))
    cpi = np.array([K.CPI[y] for y in K.EARN_YEARS])
    nominal = np.round(R["real"] * cpi[None, :] / 100.0)
    deflated = nominal * 100.0 / cpi[None, :]
    mask = (R["age"] >= 30) & (R["age"] <= 34)
    avg = np.where(mask, deflated, 0.0).sum(1) / 5.0
    fam = R["fam_of"]
    keep = (avg > 0) & (inc[fam] > 0)
    x = np.log(inc[fam][keep] * 100.0 / K.CPI[K.CENSUS_YEAR])
    y = np.log(avg[keep])
    xc_f = np.log(np.where(inc > 0, inc, 1) * 100.0 / K.CPI[K.CENSUS_YEAR])[R["files"]]
    kids_f = np.bincount(fam[keep], minlength=R["nfam"])[R["files"]]
    return x, y, np.log(hist), xc_f, (inc > 0)[R["files"]], kids_f


def variants(R):
    """The elasticity under each consistent estimate of the region's swing: within-family deviations over the
    families with a history (the golden), half the squared year-to-year changes, the census year as a sixth year,
    each family weighted by its children in the sample, and only the families with a child in the sample."""
    x, y, lx, xc_f, pos, kids_f = pack_arrays(R)
    n = lx.shape[0]
    ss = ((lx - lx.mean(1, keepdims=True)) ** 2).sum(1)
    within = float(ss.sum()) / (n * 4)
    fd = float((np.diff(lx, axis=1) ** 2).sum()) / (n * 4 * 2)
    l6 = np.column_stack([xc_f[pos], lx[pos]])
    within6 = float(((l6 - l6.mean(1, keepdims=True)) ** 2).sum()) / (l6.shape[0] * 5)
    per_child = float((ss * kids_f).sum()) / (4 * kids_f.sum())
    with_child = float(ss[kids_f > 0].sum()) / (4 * (kids_f > 0).sum())
    c = float(np.cov(y, x)[0, 1])
    v = float(np.var(x, ddof=1))
    return [c / (v - s) for s in (within, fd, within6, per_child, with_child)]


def ok(vals, margin=0.0015):
    r = {round(v, 2) for v in vals}
    if len(r) != 1:
        return False
    v0 = r.pop()
    return all(abs(v - (v0 - 0.005)) >= margin and abs(v - (v0 + 0.005)) >= margin for v in vals)


if __name__ == "__main__":
    design = [list(r) for r in K.REGIONS]
    for i, row in enumerate(design):
        R = W.region_draw(*row)
        v = variants(R)
        print(row[1].ljust(16), " ".join("%.4f" % x for x in v), "OK" if ok(v) else "--")
        if "--fit" in sys.argv and not ok(v, 0.0022):
            best = None
            for step in sorted(np.arange(-0.012, 0.0121, 0.0005), key=abs):
                trial = list(row)
                trial[5] = round(row[5] + float(step), 4)
                v2 = variants(W.region_draw(*trial))
                if ok(v2, 0.0022):
                    best = trial
                    break
            print("   ->", best[5] if best else None, " ".join("%.4f" % x for x in v2) if best else "")
            if best:
                design[i] = best
    if "--fit" in sys.argv:
        print("bt:", [(r[1], r[5]) for r in design])
