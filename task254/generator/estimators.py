"""Time-to-onset estimators on numpy arrays (no survival library).

x: onset day of the reaction (day 1 = first dose of its course); W: the last day of the course on
which an onset could still be in the database at the lock (the truncation time). Every function
returns a cumulative distribution as (support, F) with F right-continuous, or a quantile.
"""
import math

import numpy as np

MONTH = 30


def reverse_km(x, W):
    """Reverse-time product-limit estimate for right-truncated onsets (Lynden-Bell / Lagakos):
    F(s) = prod_{t > s} (1 - d(t) / R(t)), R(t) = #{i: x_i <= t <= W_i}. Rows with x > W are dropped."""
    x = np.asarray(x, dtype=float)
    W = np.asarray(W, dtype=float)
    keep = x <= W
    x, W = x[keep], W[keep]
    s, d = np.unique(x, return_counts=True)
    xs = np.sort(x)
    ws = np.sort(W)
    R = np.searchsorted(xs, s, side="right") - np.searchsorted(ws, s, side="left")
    h = d / R
    surv = np.cumprod((1.0 - h)[::-1])[::-1]
    F = np.append(surv[1:], 1.0)
    return s, F


def empirical(x, w=None):
    x = np.asarray(x, dtype=float)
    if w is None:
        w = np.ones_like(x)
    w = np.asarray(w, dtype=float)
    order = np.argsort(x, kind="mergesort")
    x, w = x[order], w[order]
    s, idx = np.unique(x, return_index=True)
    cw = np.cumsum(w)
    ends = np.append(idx[1:], len(x)) - 1
    F = cw[ends] / cw[-1]
    return s, F


def cdf_at(s, F, t):
    """F evaluated at t (right-continuous step function, 0 below the support)."""
    i = np.searchsorted(s, t, side="right") - 1
    return 0.0 if i < 0 else float(F[i])


def q_step(s, F, p, eps=1e-12):
    """Smallest support point with F >= p."""
    i = int(np.argmax(F >= p - eps))
    return float(s[i])


def q_interp(s, F, p):
    """Linear interpolation of the step CDF between its jump points (0 at the first point's predecessor)."""
    xs = np.concatenate([[0.0], s])
    Fs = np.concatenate([[0.0], F])
    i = int(np.argmax(Fs >= p))
    if i == 0:
        return float(xs[0])
    x0, x1, f0, f1 = xs[i - 1], xs[i], Fs[i - 1], Fs[i]
    return float(x0 + (p - f0) / (f1 - f0) * (x1 - x0))


def month_of(day):
    return int(math.ceil(day / MONTH - 1e-12))


def month_cut(s, F, p):
    """First 30-day month by the end of which at least p has begun."""
    for m in range(1, 200):
        if cdf_at(s, F, MONTH * m) >= p - 1e-12:
            return m
    raise ValueError("no month reaches p")


def np_quantile(x, p, method):
    return float(np.quantile(np.asarray(x, dtype=float), p, method=method))


def weibull_fit(x):
    """Weibull MLE (untruncated) by profile likelihood: lam = mean(x^k)^(1/k), k by golden-section."""
    x = np.asarray(x, dtype=float)
    lx = np.log(x)
    n = len(x)

    def ll(k):
        lam = np.mean(x ** k) ** (1.0 / k)
        return n * math.log(k) - n * k * math.log(lam) + (k - 1) * lx.sum() - np.sum((x / lam) ** k)

    ks = np.linspace(0.2, 5.0, 481)
    v = [ll(k) for k in ks]
    j = int(np.argmax(v))
    lo, hi = ks[max(j - 1, 0)], ks[min(j + 1, len(ks) - 1)]
    g = (math.sqrt(5) - 1) / 2
    for _ in range(80):
        a = hi - g * (hi - lo)
        b = lo + g * (hi - lo)
        if ll(a) > ll(b):
            hi = b
        else:
            lo = a
    k = 0.5 * (lo + hi)
    lam = np.mean(x ** k) ** (1.0 / k)
    return k, lam


def weibull_q(k, lam, p):
    return lam * (-math.log(1 - p)) ** (1.0 / k)


def _phi_cdf(z):
    return 0.5 * (1.0 + np.vectorize(math.erf)(z / math.sqrt(2.0)))


def trunc_weibull_fit(x, W):
    """Weibull MLE with each onset right-truncated at its own W (grid then coordinate refinement)."""
    x = np.asarray(x, dtype=float)
    W = np.asarray(W, dtype=float)

    def ll(k, lam):
        return float(np.sum(np.log(k / lam) + (k - 1) * np.log(x / lam) - (x / lam) ** k)
                     - np.sum(np.log(np.maximum(1 - np.exp(-(W / lam) ** k), 1e-300))))

    best = None
    for k in np.linspace(0.4, 3.0, 53):
        for lam in np.exp(np.linspace(math.log(40), math.log(4000), 93)):
            v = ll(k, lam)
            if best is None or v > best[0]:
                best = (v, k, lam)
    _, k, lam = best
    dk, dl = 0.05, 0.05
    for _ in range(60):
        moved = False
        for kk, ll_ in ((k + dk, lam), (k - dk, lam), (k, lam * math.exp(dl)), (k, lam * math.exp(-dl))):
            if kk > 0.05:
                v = ll(kk, ll_)
                if v > best[0]:
                    best = (v, kk, ll_)
                    k, lam = kk, ll_
                    moved = True
        if not moved:
            dk, dl = dk / 2, dl / 2
    return k, lam


def trunc_lognormal_fit(x, W):
    x = np.asarray(x, dtype=float)
    W = np.asarray(W, dtype=float)
    lx, lW = np.log(x), np.log(W)

    def ll(mu, s):
        return float(np.sum(-math.log(s) - 0.5 * ((lx - mu) / s) ** 2)
                     - np.sum(np.log(np.maximum(_phi_cdf((lW - mu) / s), 1e-300))))

    best = None
    for mu in np.linspace(math.log(30), math.log(2000), 70):
        for s in np.linspace(0.3, 2.5, 45):
            v = ll(mu, s)
            if best is None or v > best[0]:
                best = (v, mu, s)
    _, mu, s = best
    dm, ds = 0.05, 0.05
    for _ in range(60):
        moved = False
        for mm, ss in ((mu + dm, s), (mu - dm, s), (mu, s + ds), (mu, s - ds)):
            if ss > 0.05:
                v = ll(mm, ss)
                if v > best[0]:
                    best = (v, mm, ss)
                    mu, s = mm, ss
                    moved = True
        if not moved:
            dm, ds = dm / 2, ds / 2
    return mu, s


def lognormal_q(mu, s, p):
    z = {0.8: 0.8416212335729143, 0.95: 1.6448536269514722}[p]
    return math.exp(mu + s * z)
