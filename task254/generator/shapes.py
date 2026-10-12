"""Onset-day distributions: monthly masses joined by a monotone cubic (PCHIP) cumulative curve."""
import math

import numpy as np


def _slopes(x, y):
    h = np.diff(x)
    d = np.diff(y) / h
    m = np.zeros_like(y)
    for k in range(1, len(y) - 1):
        if d[k - 1] * d[k] <= 0:
            m[k] = 0.0
        else:
            w1 = 2 * h[k] + h[k - 1]
            w2 = h[k] + 2 * h[k - 1]
            m[k] = (w1 + w2) / (w1 / d[k - 1] + w2 / d[k])
    m[0] = d[0] * 0.5
    m[-1] = 0.0
    return m


def _eval(x, y, m, t):
    i = np.clip(np.searchsorted(x, t, side="right") - 1, 0, len(x) - 2)
    h = x[i + 1] - x[i]
    s = (t - x[i]) / h
    h00 = 2 * s ** 3 - 3 * s ** 2 + 1
    h10 = s ** 3 - 2 * s ** 2 + s
    h01 = -2 * s ** 3 + 3 * s ** 2
    h11 = s ** 3 - s ** 2
    return h00 * y[i] + h10 * h * m[i] + h01 * y[i + 1] + h11 * h * m[i + 1]


def pmf_months(masses, maxd):
    """Day-level pmf on days 1..maxd from per-30-day-month masses (the last month ends at maxd)."""
    mm = np.array(masses, dtype=float)
    mm = mm / mm.sum()
    knots = np.array([0.0] + [30.0 * (i + 1) for i in range(len(mm))])
    knots[-1] = min(knots[-1], float(maxd))
    C = np.concatenate([[0.0], np.cumsum(mm)])
    m = _slopes(knots, C)
    days = np.arange(0, maxd + 1, dtype=float)
    Fd = np.maximum.accumulate(_eval(knots, C, m, days))
    pmf = np.maximum(np.diff(Fd), 0.0)
    return pmf / pmf.sum()


class Dist:
    def __init__(self, masses, maxd):
        self.pmf = pmf_months(masses, maxd)
        self.cdf = np.cumsum(self.pmf)
        self.maxd = maxd

    def q(self, u):
        return int(np.searchsorted(self.cdf, u, side="left")) + 1

    def F(self, day):
        if day < 1:
            return 0.0
        return float(self.cdf[min(day, self.maxd) - 1])


def lognormal_days(u, median, logsd, lo=1, hi=None):
    """Inverse lognormal at u (Acklam-free: bisection on erf), rounded to whole days."""
    z = _ninv(u)
    v = math.exp(math.log(median) + logsd * z)
    v = max(lo, int(round(v)))
    if hi is not None:
        v = min(v, hi)
    return v


def _ninv(u):
    u = min(max(u, 1e-9), 1 - 1e-9)
    lo, hi = -9.0, 9.0
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if 0.5 * (1 + math.erf(mid / math.sqrt(2))) < u:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)
