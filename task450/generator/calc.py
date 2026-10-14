"""The analysis for task450 on arrays: scoring, every common-item and random-groups equating method, the corridor,
full-academic-year status, campus rates, the designated set and every rung, and the two asks. The pack readers in
checks.py and verify.py feed the same functions from the shipped files."""
import numpy as np

import world as W

LO = W.SCALE_MID - 0.5 / W.SCALE_SLOPE      # a whole-number scale score of 300 or more (rounded)
HI = W.SCALE_MID                            # an unrounded scale score of 300 or more


def scale_of(e):
    """Scale score of a raw score on the 2025 form (or its 2025-form equivalent), unrounded."""
    return W.STANDARD + W.SCALE_SLOPE * (np.asarray(e, float) - W.SCALE_MID)


def score(resp, key):
    return (resp == np.asarray(key)[None, :]).astype(int)


# --------------------------------------------------------------------------------------------- equating ----
def _lin(sx, mx, sy, my):
    return lambda y: sx / sy * (np.asarray(y, float) - my) + mx


def _prank(f, k):
    F = np.cumsum(f)

    def P(x):
        x = np.asarray(x, float)
        xs = np.clip(np.floor(x + 0.5), 0, k).astype(int)
        Fb = np.where(xs > 0, F[np.maximum(xs - 1, 0)], 0.0)
        return Fb + (x - (xs - 0.5)) * f[xs]

    def Q(p):
        out = []
        for pp in np.atleast_1d(p):
            j = min(int(np.searchsorted(F, pp, side="left")), k)
            Fb = F[j - 1] if j > 0 else 0.0
            out.append((pp - Fb) / f[j] + j - 0.5 if f[j] > 0 else j)
        return np.array(out)
    return P, Q


def _jml(R, iters=80):
    obs = ~np.isnan(R)
    Rf = np.nan_to_num(R)
    tot, nobs = Rf.sum(1), obs.sum(1)
    keep = (tot > 0) & (tot < nobs)
    o2, Rf2 = obs[keep], Rf[keep]
    b = np.zeros(R.shape[1])
    th = np.zeros(o2.shape[0])
    for _ in range(iters):
        p = np.where(o2, 1 / (1 + np.exp(-(th[:, None] - b[None, :]))), 0)
        th += (Rf2.sum(1) - p.sum(1)) / np.maximum((p * (1 - p)).sum(1), 1e-6)
        p = np.where(o2, 1 / (1 + np.exp(-(th[:, None] - b[None, :]))), 0)
        b -= (Rf2.sum(0) - p.sum(0)) / np.maximum((p * (1 - p)).sum(0), 1e-6)
        b -= b.mean()
    return b


def _tse(bfrom, bto):
    def f(y):
        res = []
        for yy in np.atleast_1d(y):
            lo, hi = -9.0, 9.0
            for _ in range(70):
                mid = (lo + hi) / 2
                if (1 / (1 + np.exp(-(mid - bfrom)))).sum() < yy:
                    lo = mid
                else:
                    hi = mid
            res.append((1 / (1 + np.exp(-(mid - bto)))).sum())
        return np.array(res)
    return f


def methods(S25, S26, anchor_idx, rasch=True):
    """Every conversion of a 2026 raw score to its 2025-form equivalent. S25, S26: scored 0/1 matrices (students by
    the 50 positions); anchor_idx: the positions (0-based) both forms share."""
    ni = S25.shape[1]
    na = len(anchor_idx)
    X, V1 = S25.sum(1), S25[:, anchor_idx].sum(1)
    Y, V2 = S26.sum(1), S26[:, anchor_idx].sum(1)
    N1, N2 = len(X), len(Y)
    out = {}
    for wv in ("prop", 0.5, 1.0, 0.0):
        w1 = N1 / (N1 + N2) if wv == "prop" else wv
        w2 = 1 - w1

        def synth(g1, g2):
            dv = V1.mean() - V2.mean()
            mx = X.mean() - w2 * g1 * dv
            my = Y.mean() + w1 * g2 * dv
            vx = X.var() - w2 * g1 ** 2 * (V1.var() - V2.var()) + w1 * w2 * g1 ** 2 * dv ** 2
            vy = Y.var() + w1 * g2 ** 2 * (V1.var() - V2.var()) + w1 * w2 * g2 ** 2 * dv ** 2
            return _lin(np.sqrt(vx), mx, np.sqrt(vy), my)
        out["Tucker (w1 %s)" % wv] = synth(np.cov(X, V1)[0, 1] / V1.var(ddof=1), np.cov(Y, V2)[0, 1] / V2.var(ddof=1))
        out["Levine (w1 %s)" % wv] = synth(X.var(ddof=1) / np.cov(X, V1)[0, 1], Y.var(ddof=1) / np.cov(Y, V2)[0, 1])
        h1 = np.bincount(V1, minlength=na + 1) / N1
        h2 = np.bincount(V2, minlength=na + 1) / N2
        fx = np.zeros(ni + 1)
        fy = np.zeros(ni + 1)
        for v in range(na + 1):
            m1, m2 = V1 == v, V2 == v
            if m1.sum():
                fx += np.bincount(X[m1], minlength=ni + 1) / m1.sum() * (w1 * h1[v] + w2 * h2[v])
            if m2.sum():
                fy += np.bincount(Y[m2], minlength=ni + 1) / m2.sum() * (w1 * h1[v] + w2 * h2[v])
        fx /= fx.sum()
        fy /= fy.sum()
        Px, Qx = _prank(fx, ni)
        Py, Qy = _prank(fy, ni)
        out["frequency estimation (w1 %s)" % wv] = (lambda Qx, Py: (lambda y: Qx(Py(y))))(Qx, Py)
        g = np.arange(ni + 1)
        mx_, my_ = (g * fx).sum(), (g * fy).sum()
        out["Braun-Holland (w1 %s)" % wv] = _lin(np.sqrt((g ** 2 * fx).sum() - mx_ ** 2), mx_,
                                                 np.sqrt((g ** 2 * fy).sum() - my_ ** 2), my_)
    yv = _lin(V2.std(), V2.mean(), Y.std(), Y.mean())
    vx = _lin(X.std(), X.mean(), V1.std(), V1.mean())
    out["chained linear"] = lambda y: vx(yv(y))
    PX, QX = _prank(np.bincount(X, minlength=ni + 1) / N1, ni)
    PY, QY = _prank(np.bincount(Y, minlength=ni + 1) / N2, ni)
    PV1, QV1 = _prank(np.bincount(V1, minlength=na + 1) / N1, na)
    PV2, QV2 = _prank(np.bincount(V2, minlength=na + 1) / N2, na)
    out["chained equipercentile"] = lambda y: QX(PV1(QV2(PY(y))))
    if rasch:
        uni = [j for j in range(ni) if j not in anchor_idx]
        M = np.full((N1 + N2, ni + len(uni)), np.nan)
        M[:N1, :ni] = S25
        M[N1:, anchor_idx] = S26[:, anchor_idx]
        M[N1:, ni:] = S26[:, uni]
        bh = _jml(M)
        bX = bh[:ni]
        bY = bh[:ni].copy()
        bY[uni] = bh[ni:]
        out["Rasch true score, concurrent"] = _tse(bY, bX)
        b1, b2 = _jml(S25.astype(float)), _jml(S26.astype(float))
        b2s = b2 + (b1[anchor_idx].mean() - b2[anchor_idx].mean())
        out["Rasch true score, separate, mean/mean"] = _tse(b2s, b1)
    rg = {"identity (the 2025 conversion)": lambda y: np.asarray(y, float),
          "random groups linear": _lin(X.std(), X.mean(), Y.std(), Y.mean()),
          "random groups equipercentile": lambda y: QX(PY(y))}
    return out, rg, dict(N1=N1, N2=N2, mX=X.mean(), mY=Y.mean(), mV1=V1.mean(), mV2=V2.mean())


def passing(conv, cut=LO, ni=W.N_ITEMS):
    """The lowest 2026 raw score whose 2025-form equivalent reaches the cut."""
    e = conv(np.arange(ni + 1))
    return int(np.argmax(e >= cut - 1e-12))


def corridor(out, r, ni=W.N_ITEMS):
    """Margins of every method at passing raw score r: min e(r) above the unrounded cut, the rounded cut above
    max e(r - 1)."""
    ys = np.arange(ni + 1)
    E = {k: f(ys) for k, f in out.items()}
    lo = min(e[r] for e in E.values()) - HI
    hi = LO - max(e[r - 1] for e in E.values())
    return lo, hi, E


# ---------------------------------------------------------------------------------- the shared items' stability ----
def drift_screens(S25, S26, anchor_idx):
    """The standard screens of the shared items for a change in difficulty between the cohorts, each returning the
    flagged positions (0-based): the robust z of each item's Rasch difficulty change, each form calibrated on its own
    year (|z| over 2.7); Mantel-Haenszel D-DIF between the years, matched on the shared-item score (|D| of 1.5 or
    more); the delta plot's perpendicular distance from its major axis (over 1.5); the change in proportion correct
    against the median change (over four median absolute deviations)."""
    from scipy.stats import norm
    idx = list(anchor_idx)
    out = {}
    b1, b2 = _jml(S25.astype(float)), _jml(S26.astype(float))
    d = b2[idx] - b1[idx]
    q1, q3 = np.percentile(d, [25, 75])
    z = (d - np.median(d)) / (0.74 * (q3 - q1))
    out["robust z"] = sorted(idx[j] for j in np.where(np.abs(z) > 2.7)[0])
    V1, V2 = S25[:, idx].sum(1), S26[:, idx].sum(1)
    mh = []
    for it in idx:
        num = den = 0.0
        for v in range(len(idx) + 1):
            m1, m2 = V1 == v, V2 == v
            n1, n2 = int(m1.sum()), int(m2.sum())
            if n1 == 0 or n2 == 0:
                continue
            a = S25[m1, it].sum()
            c = S26[m2, it].sum()
            num += a * (n2 - c) / (n1 + n2)
            den += (n1 - a) * c / (n1 + n2)
        mh.append(-2.35 * np.log(num / den))
    out["Mantel-Haenszel"] = sorted(idx[j] for j in np.where(np.abs(mh) >= 1.5)[0])
    p1 = np.clip(S25[:, idx].mean(0), 1e-4, 1 - 1e-4)
    p2 = np.clip(S26[:, idx].mean(0), 1e-4, 1 - 1e-4)
    x, y = 13 + 4 * norm.ppf(1 - p1), 13 + 4 * norm.ppf(1 - p2)
    sx, sy, sxy = x.var(), y.var(), np.cov(x, y, bias=True)[0, 1]
    slope = (sy - sx + np.sqrt((sy - sx) ** 2 + 4 * sxy ** 2)) / (2 * sxy)
    dist = (slope * x - y + y.mean() - slope * x.mean()) / np.sqrt(slope ** 2 + 1)
    out["delta plot"] = sorted(idx[j] for j in np.where(np.abs(dist) > 1.5)[0])
    g = p2 - p1
    mad = np.median(np.abs(g - np.median(g))) * 1.4826
    out["proportion correct"] = sorted(idx[j] for j in np.where(np.abs(g - np.median(g)) > 4 * mad)[0])
    return out, dict(d=d, z=z, mh=np.array(mh), dist=dist, gap=g)


def screened(S25, S26, anchor_idx):
    """The shared items the robust-z screen keeps: the link runs through these."""
    flagged = set(drift_screens(S25, S26, anchor_idx)[0]["robust z"])
    return [j for j in anchor_idx if j not in flagged]


# ------------------------------------------------------------------------------------------- the campuses ----
def fay(spells, snapshot=W.SNAPSHOT, first=W.WINDOW[0]):
    """The campus a student is full academic year at, or None: enrolled there on the snapshot date and every day
    through the first day of the window, and at no other campus in between."""
    cover = [c for c, a, b in spells if a <= snapshot and (b is None or b >= first)]
    if len(cover) != 1:
        return None
    c = cover[0]
    for c2, a, b in spells:
        if c2 != c and a <= first and (b is None or b >= snapshot):
            return None
    return c


def rated_campus(c):
    return W.CLOSED[1] if c == W.CLOSED[0] else c


def campus_rates(raw, campus_of, fay_of, r, merge_closed=True, use_fay=True, n_min=W.N_MIN):
    """Per rated campus: tested full-academic-year students, those at or above passing raw score r, the rate."""
    agg = {}
    for i in range(len(raw)):
        c = fay_of[i] if use_fay else campus_of[i]
        if c is None:
            continue
        if merge_closed:
            c = rated_campus(c)
        n, k = agg.get(c, (0, 0))
        agg[c] = (n + 1, k + int(raw[i] >= r))
    return {c: (n, k, k / n) for c, (n, k) in agg.items() if n >= n_min}


def designated(rates, line=W.LINE):
    return sorted(c for c, (n, k, v) in rates.items() if v < line)


# -------------------------------------------------------------------------------------------------- the asks ----
def ask_2025(campus_of, raw25, community_of, cut=27):
    """Each learning community's 2025 grade-5 test takers and the share meeting the standard (raw 27 or more on the
    2025 form), the communities as drawn for 2026-27."""
    out = {}
    for c, r in zip(campus_of, raw25):
        k = community_of[rated_campus(c)]
        n, m = out.get(k, (0, 0))
        out[k] = (n + 1, m + int(r >= cut))
    return {k: (n, m, 100.0 * m / n) for k, (n, m) in out.items()}


def enrolled_in_window(spells, window=W.WINDOW):
    a, b = window
    return [c for c, s, e in spells if s <= b and (e is None or e >= a)]


def ask_untested(people, community_of):
    """Grade-5 students enrolled at some time in the testing window with no 2026 test, by learning community.
    people: (spells, tested) per person."""
    out = {}
    for spells, tested in people:
        cs = enrolled_in_window(spells)
        if not cs or tested:
            continue
        ks = sorted({community_of[rated_campus(c)] for c in cs})
        assert len(ks) == 1, ks
        out[ks[0]] = out.get(ks[0], 0) + 1
    return out
