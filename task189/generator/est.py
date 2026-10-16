"""Censored-sample mean estimators: the ones a water-quality statistician reaches for.

A result reported below a reporting limit is an observation with an upper bound. All four estimators
here estimate the same quantity, the mean of the samples themselves, and none of them substitutes a
constant. `mle_fill` fits a lognormal to the censored sample with every observation at its own
censoring point and gives each non-detect its conditional expectation; `km_mean` is the Kaplan-Meier
mean of the flipped sample; `cond_fill` fills each non-detect from the quantified results the
sensitive method returned in the same month below the same limit; `truth_mean` is the clean-truth
mean the generator holds and no shipped file carries.
"""
import math

import numpy as np
from scipy.optimize import minimize
from scipy.stats import norm


def mle_fill(vals, lims, det):
    x = np.asarray(vals, float)
    l = np.asarray(lims, float)
    d = np.asarray(det, bool)
    lx = np.log(x[d])
    ll = np.log(l[~d])
    if lx.size < 2:
        return float(np.mean(x))

    def nll(p):
        mu, ls = float(p[0]), float(p[1])
        s = math.exp(ls)
        a = float(np.sum(norm.logpdf((lx - mu) / s) - ls - lx))
        b = float(np.sum(norm.logcdf((ll - mu) / s))) if ll.size else 0.0
        return -(a + b)

    best, bv = None, float("inf")
    base = float(np.mean(lx))
    for mu0 in (base - 1.0, base, base + 1.0):
        for ls0 in (math.log(0.5), math.log(1.0), math.log(1.6)):
            r = minimize(nll, [mu0, ls0], method="Nelder-Mead",
                         options={"xatol": 1e-10, "fatol": 1e-12, "maxiter": 6000})
            if r.fun < bv:
                bv, best = float(r.fun), r.x
    mu, s = float(best[0]), math.exp(float(best[1]))
    tot = float(np.sum(x[d]))
    for c in l[~d]:
        z = (math.log(c) - mu) / s
        p = float(norm.cdf(z))
        tot += (c / 2.0) if p <= 1e-12 else math.exp(mu + s * s / 2.0) * float(norm.cdf(z - s)) / p
    return tot / x.size


def fitted_distribution_mean(vals, lims, det):
    """exp(mu + s^2/2) from the same censored fit: the mean of a fitted distribution, which is not
    the mean of the samples clause 7.2 asks for. Kept only so the separation can be asserted."""
    import math as _m
    x = np.asarray(vals, float)
    l = np.asarray(lims, float)
    d = np.asarray(det, bool)
    lx = np.log(x[d])
    ll = np.log(l[~d])
    if lx.size < 2:
        return float(np.mean(x))

    def nll(p):
        s = _m.exp(p[1])
        a = float(np.sum(norm.logpdf((lx - p[0]) / s) - p[1] - lx))
        b = float(np.sum(norm.logcdf((ll - p[0]) / s))) if ll.size else 0.0
        return -(a + b)

    best, bv = None, float("inf")
    base = float(np.mean(lx))
    for mu0 in (base - 1.0, base, base + 1.0):
        for ls0 in (_m.log(0.5), _m.log(1.0), _m.log(1.6)):
            r = minimize(nll, [mu0, ls0], method="Nelder-Mead",
                         options={"xatol": 1e-10, "fatol": 1e-12, "maxiter": 6000})
            if r.fun < bv:
                bv, best = float(r.fun), r.x
    return _m.exp(float(best[0]) + _m.exp(float(best[1])) ** 2 / 2.0)


def km_mean(vals, lims, det):
    x = np.asarray(vals, float)
    l = np.asarray(lims, float)
    d = np.asarray(det, bool)
    if not d.any():
        return float(np.mean(l) / 2.0)
    M = float(max(float(x[d].max()), float(l.max()))) * 10.0
    t = np.where(d, M - x, M - l)
    ev = d.copy()
    order = np.argsort(t, kind="mergesort")
    t, ev = t[order], ev[order]
    n = int(t.size)
    surv, last, at_risk, i = 1.0, 0.0, n, 0
    area = 0.0
    while i < n:
        ti = float(t[i])
        j, dd = i, 0
        while j < n and float(t[j]) == ti:
            dd += int(ev[j])
            j += 1
        if dd:
            area += surv * (ti - last)
            surv *= (1.0 - dd / at_risk)
            last = ti
        at_risk -= (j - i)
        i = j
    area += surv * (float(t[-1]) - last)
    return M - area


def cond_fill(rows, sensitive_rows):
    """rows and sensitive_rows are (year, month, value, limit, detected) tuples."""
    pool = {}
    for (y, m, v, _rl, dd) in sensitive_rows:
        if dd:
            pool.setdefault((y, m), []).append(v)
    allq = [v for vs in pool.values() for v in vs]
    tot, n = 0.0, 0
    for (y, m, v, rl, dd) in rows:
        n += 1
        if dd:
            tot += v
        else:
            cand = [q for q in pool.get((y, m), []) if q < rl] or [q for q in allq if q < rl]
            tot += (sum(cand) / len(cand)) if cand else rl / 2.0
    return tot / n


def substitute(rows, mode):
    """The constants a solver reaches for; none of them is an estimator."""
    tot, n, kept = 0.0, 0, 0
    for (_y, _m, v, rl, dd) in rows:
        n += 1
        if dd:
            tot += v
            kept += 1
        elif mode == "half":
            tot += rl / 2.0
        elif mode == "full":
            tot += rl
        elif mode == "zero":
            pass
        elif mode == "drop":
            n -= 1
    return tot / n if n else 0.0
