"""Death distribution methods on five-year age groups: Hill's general growth balance (two censuses), with or without the
net movement above each age, the Bennett-Horiuchi synthetic extinct generations method, and Brass's growth balance on
one census. Shared by the estimator, the checks and the verifier's own code path is separate (verify.py)."""
import numpy as np

AGES = list(range(0, 80, 5)) + [80]          # group starts; the last group is 80 and over


def tail(arr, i):
    return float(np.sum(arr[i:]))


def ggb_points(p1, p2, d, t, nm=None, xs=range(5, 80, 5), nx_mean="geometric"):
    """The growth balance's points for each age x: (registered death rate above x, birthday rate less growth rate above
    x, plus the net movement rate above x when given). p1, p2: census counts by group; d: registered deaths in the
    interval by group (age at death); nm: net movers in the interval by group; t: years between the censuses. The
    persons at exact age x per year: the two groups either side of x, their geometric mean (or arithmetic), over five,
    the two censuses' values combined geometrically."""
    pts = []
    for x in xs:
        i = AGES.index(x)
        n1, n2 = tail(p1, i), tail(p2, i)
        pyl = t * np.sqrt(n1 * n2)
        r = np.log(n2 / n1) / t
        if nx_mean == "geometric":
            nx = np.sqrt(np.sqrt(p1[i - 1] * p1[i]) * np.sqrt(p2[i - 1] * p2[i])) / 5.0
        else:
            nx = np.sqrt((p1[i - 1] + p1[i]) / 2.0 * (p2[i - 1] + p2[i]) / 2.0) / 5.0
        y = nx * t / pyl - r
        if nm is not None:
            y += tail(nm, i) / pyl
        pts.append((x, tail(d, i) / pyl, y))
    return pts


def fit(pts, lo=15, hi=65, method="orthogonal"):
    sel = [(dx, y) for x, dx, y in pts if lo <= x <= hi]
    dx = np.array([s[0] for s in sel])
    y = np.array([s[1] for s in sel])
    if method == "orthogonal":
        slope = np.std(y) / np.std(dx)
    else:
        slope = np.polyfit(dx, y, 1)[0]
    icpt = float(y.mean() - slope * dx.mean())
    res = y - (icpt + slope * dx)
    return float(slope), icpt, float(np.abs(res).max())


def completeness(p1, p2, d, t, nm=None, lo=15, hi=65, method="orthogonal", nx_mean="geometric"):
    """Completeness of death registration relative to the population: with the intercept ln(k1/k2)/t and the slope
    sqrt(k1 k2)/c, c = sqrt(k1 k2)/slope; the censuses' relative coverage is taken from the intercept and their mean
    coverage as one. The orthogonal fit's slope is the ratio of the two rates' standard deviations."""
    pts = ggb_points(p1, p2, d, t, nm, nx_mean=nx_mean)
    slope, icpt, res = fit(pts, lo, hi, method)
    return 1.0 / slope, icpt, res


def seg(p1, p2, d, t, nm=None, lo=15, hi=65):
    """Synthetic extinct generations with the intercensal growth rate by age: the deaths above each age, carried with
    the age-specific growth rates, against the population at that age; completeness the mean ratio over the range."""
    n = len(AGES)
    pyl = np.array([t * np.sqrt(p1[i] * p2[i]) for i in range(n)])
    r = np.array([np.log(p2[i] / p1[i]) / t for i in range(n)])
    if nm is not None:
        r = r - np.array([nm[i] / pyl[i] for i in range(n)])
    dpy = np.array([d[i] / t for i in range(n)])
    ratios = []
    for x in range(lo, hi + 1, 5):
        i = AGES.index(x)
        # deaths above x carried back to age x with the growth rates of the groups above
        tot = 0.0
        e_open = np.sqrt(p1[-1] * p2[-1]) * t / max(d[-1], 1e-9)
        for j in range(n - 1, i - 1, -1):
            if j < n - 1:
                cum = 5 * np.sum(r[i:j]) + 2.5 * r[j]
            else:
                cum = 5 * np.sum(r[i:j]) + r[j] * e_open
            tot += dpy[j] * np.exp(cum)
        # population at exact age x per year of age
        nx = np.sqrt(np.sqrt(p1[i - 1] * p1[i]) * np.sqrt(p2[i - 1] * p2[i])) / 5.0
        ratios.append(tot / nx)
    return float(np.mean(ratios))


def brass(p, d_annual, lo=15, hi=65, method="orthogonal"):
    """Brass's growth balance on one census, the population taken as stable: entries above x against the deaths above
    x, both per person above x; the slope is one over completeness."""
    pts = []
    for x in range(lo, hi + 1, 5):
        i = AGES.index(x)
        nplus = tail(p, i)
        nx = np.sqrt(p[i - 1] * p[i]) / 5.0
        pts.append((x, tail(d_annual, i) / nplus, nx / nplus))
    slope, icpt, res = fit(pts, lo, hi, method)
    return 1.0 / slope, icpt, res
