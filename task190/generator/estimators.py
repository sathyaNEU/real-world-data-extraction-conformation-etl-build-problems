"""Every way of reading the band's counterfactual that a competent analyst might take.

The candidate set below is the determinism judge's own grid, not the author's: three fit families,
polynomial orders 1 to 3, bin widths 50 to 500, five windows, the whole near-threshold band left out
of the fit. The 50-dollar width drops out on the data rather than by choice, because at 50 every
segment has empty bins outside the band and no log fit takes one.

What separates the candidates is the record, not a rule. Every split take was moved from at or above
the prescribed threshold to below it, to the cent, so 10,000 to 11,000 carries a deficit the same
size as the band's surplus. One fit measures both. A baseline that implies a surplus below and a
deficit above of different sizes contradicts the record it was fitted to.
"""
import math

BAND_LO, BAND_HI, MIRROR_HI = 9000, 10000, 11000
WINDOWS = [(5000, 16000), (6000, 14000), (7000, 13000), (8000, 12000), (5000, 20000)]
WIDTHS = [50, 100, 200, 250, 500]
FAMILIES = ["poisson", "ols", "log_ols"]
ORDERS = [1, 2, 3]
BALANCE = 0.20          # how far the two sides of the record's balance may disagree


def bins(amounts, lo, hi, step):
    n = int((hi - lo) // step)
    out = [0] * n
    for a in amounts:
        if lo <= a < hi:
            out[int((a - lo) // step)] += 1
    return out


def _solve(A, b):
    m = len(b)
    for c in range(m):
        piv = max(range(c, m), key=lambda r: abs(A[r][c]))
        A[c], A[piv] = A[piv], A[c]
        b[c], b[piv] = b[piv], b[c]
        if abs(A[c][c]) < 1e-14:
            return None
        for r in range(c + 1, m):
            f = A[r][c] / A[c][c]
            for cc in range(c, m):
                A[r][cc] -= f * A[c][cc]
            b[r] -= f * b[c]
    q = [0.0] * m
    for r in range(m - 1, -1, -1):
        q[r] = (b[r] - sum(A[r][c] * q[c] for c in range(r + 1, m))) / A[r][r]
    return q


def _wls(xs, ys, w, order):
    m = order + 1
    A = [[sum(w[i] * xs[i] ** (r + c) for i in range(len(xs))) for c in range(m)]
         for r in range(m)]
    b = [sum(w[i] * ys[i] * xs[i] ** r for i in range(len(xs))) for r in range(m)]
    return _solve(A, b)


def fit(xs, ys, family, order):
    """The fitted profile as a function of the scaled amount, or None if it will not solve."""
    if family == "ols":
        p = _wls(xs, ys, [1.0] * len(xs), order)
        return (lambda x: sum(p[j] * x ** j for j in range(order + 1))) if p else None
    if family == "log_ols":
        zs = [math.log(max(y, 0.5)) for y in ys]
        p = _wls(xs, zs, [1.0] * len(xs), order)
        return (lambda x: math.exp(sum(p[j] * x ** j for j in range(order + 1)))) if p else None
    p = [0.0] * (order + 1)
    p[0] = math.log(max(sum(ys) / float(len(ys)), 1e-9))
    for _ in range(60):                               # iteratively reweighted least squares
        mu = [math.exp(min(30.0, sum(p[j] * x ** j for j in range(order + 1)))) for x in xs]
        z = [sum(p[j] * x ** j for j in range(order + 1)) + (y - m) / max(m, 1e-9)
             for x, y, m in zip(xs, ys, mu)]
        q = _wls(xs, z, mu, order)
        if q is None:
            return None
        done = max(abs(q[j] - p[j]) for j in range(order + 1)) < 1e-11
        p = q
        if done:
            break
    return lambda x: math.exp(min(30.0, sum(p[j] * x ** j for j in range(order + 1))))


def sides(amounts, lo, hi, step, family, order):
    """The surplus the band carries and the deficit 10,000 to 11,000 carries, from one fit.

    Returns None where the specification is not available on this data: an empty bin outside the
    band, too few bins for the order, a window that does not hold both intervals, or a fit that
    will not solve or predicts a non-positive count.
    """
    b = bins(amounts, lo, hi, step)
    n = len(b)
    out = [k for k in range(n) if BAND_LO <= lo + k * step < MIRROR_HI]
    rest = [k for k in range(n) if k not in out]
    if any(b[k] == 0 for k in rest):
        return None
    keep = [k for k in rest if b[k] > 0]
    if len(keep) < order + 3:
        return None
    low = [k for k in range(n) if BAND_LO <= lo + k * step < BAND_HI]
    mir = [k for k in range(n) if BAND_HI <= lo + k * step < MIRROR_HI]
    if not low or not mir:
        return None
    f = fit([(lo + k * step) / 1000.0 for k in keep], [float(b[k]) for k in keep], family, order)
    if f is None:
        return None
    pl = sum(f((lo + k * step) / 1000.0) for k in low)
    pm = sum(f((lo + k * step) / 1000.0) for k in mir)
    if not (0 < pl < 1e7 and 0 < pm < 1e7):
        return None
    return (sum(b[k] for k in low) - pl, pm - sum(b[k] for k in mir))


def candidates():
    """Every (window, width, family, order) in the judge's grid, as labels."""
    out = []
    for lo, hi in WINDOWS:
        for st in WIDTHS:
            for fam in FAMILIES:
                for od in ORDERS:
                    out.append((lo, hi, st, fam, od))
    return out


def reconciled(amounts, lo, hi, step, family, order):
    """The segment's figure under one specification, or None where the record refuses it."""
    s = sides(amounts, lo, hi, step, family, order)
    if s is None:
        return None
    below, above = s
    if abs(below - above) > BALANCE * max(abs(below), abs(above), 1.0):
        return None
    return (below + above) / 2.0


def sweep(by_segment, keys):
    """Every specification the record leaves standing, as (label, {segment: figure})."""
    out = []
    for lo, hi, st, fam, od in candidates():
        vs = {}
        for k in keys:
            v = reconciled(by_segment[k], lo, hi, st, fam, od)
            if v is None:
                vs = None
                break
            vs[k] = v
        if vs:
            out.append(("%d-%d/%d/%s/o%d" % (lo, hi, st, fam, od), vs))
    return out


def one_sided(amounts, lo=5000, hi=16000, step=250, family="poisson", order=1):
    """The band read on its own, which is the rung: the surplus below, unreconciled."""
    s = sides(amounts, lo, hi, step, family, order)
    return None if s is None else s[0]


def chi2_per_dof(amounts, lo=5000, hi=16000, step=250):
    """How well the segment's own trade outside the band fits a log-linear profile."""
    b = bins(amounts, lo, hi, step)
    n = len(b)
    keep = [k for k in range(n) if not (BAND_LO <= lo + k * step < MIRROR_HI) and b[k] > 0]
    xs = [(lo + k * step) / 1000.0 for k in keep]
    ys = [float(b[k]) for k in keep]
    f = fit(xs, ys, "poisson", 1)
    c = sum((y - f(x)) ** 2 / max(f(x), 1e-9) for x, y in zip(xs, ys))
    return c / max(len(xs) - 2, 1)
