"""Pairs of traversals of one sector that overlap in time, and what each pair is: whether the two level profiles
(linear from entry to exit) change order while both are in the sector, the moment and level where they do, and
the nearest vertical approach for pairs that do not."""
import numpy as np


def overlapping(t0, t1):
    """Index pairs (i, j), i < j in t0 order, of traversals in the sector at once. t0 must be sorted."""
    n = len(t0)
    k = np.searchsorted(t0, t1, side="left")
    cnt = np.maximum(k - np.arange(n) - 1, 0)
    tot = int(cnt.sum())
    i = np.repeat(np.arange(n), cnt)
    start = np.repeat(np.cumsum(cnt) - cnt, cnt)
    j = np.arange(tot) - start + i + 1
    return i, j


def level(a, b, t0, t1, t):
    return a + (b - a) * (t - t0) / (t1 - t0)


def pair_table(t0, t1, a, b):
    """Every overlapping pair with: lo, hi (the shared interval), d_lo and d_hi (level of i minus level of j at
    each end), cross (the order changes), tx and lx (moment and level where it does), moving (either aircraft
    changes level in the sector) and gap (nearest vertical approach in flight levels when they do not change order,
    0 when they do)."""
    t0 = np.asarray(t0, float)
    t1 = np.asarray(t1, float)
    a = np.asarray(a, float)
    b = np.asarray(b, float)
    i, j = overlapping(t0, t1)
    lo = np.maximum(t0[i], t0[j])
    hi = np.minimum(t1[i], t1[j])
    ok = hi > lo
    i, j, lo, hi = i[ok], j[ok], lo[ok], hi[ok]
    dlo = level(a[i], b[i], t0[i], t1[i], lo) - level(a[j], b[j], t0[j], t1[j], lo)
    dhi = level(a[i], b[i], t0[i], t1[i], hi) - level(a[j], b[j], t0[j], t1[j], hi)
    cross = dlo * dhi < 0
    frac = np.where(cross, dlo / np.where(cross, dlo - dhi, 1.0), 0.0)
    tx = lo + (hi - lo) * frac
    lx = level(a[i], b[i], t0[i], t1[i], tx)
    moving = (a[i] != b[i]) | (a[j] != b[j])
    gap = np.where(cross, 0.0, np.minimum(np.abs(dlo), np.abs(dhi)))
    return dict(i=i, j=j, lo=lo, hi=hi, dlo=dlo, dhi=dhi, cross=cross, tx=tx, lx=lx, moving=moving, gap=gap)


def by_sector(t, nsec=8):
    """Yield (sector index, sorted traversal indices, pair table) for each sector."""
    for s in range(nsec):
        idx = np.nonzero(t["sec"] == s)[0]
        order = idx[np.argsort(t["t0"][idx], kind="stable")]
        pt = pair_table(t["t0"][order], t["t1"][order], t["a"][order], t["b"][order])
        yield s, order, pt
