"""The forecasting models every route uses, on monthly arrays indexed by month t (t = 0 is January 2019): a Poisson
count model fitted by IRLS (region intercepts, a region or common log trend, month of year, optionally log spend), the
founder pipeline (founder yield per leaver, lag distribution, destination shares) and the 2027 totals."""
from __future__ import annotations

import math

import numpy as np

R = 6


def poisson_glm(y, X, iters=100):
    beta = np.zeros(X.shape[1])
    beta[0] = math.log(max(float(np.mean(y)), 1e-6))
    for _ in range(iters):
        eta = np.clip(X @ beta, -30, 30)
        mu = np.exp(eta)
        z = eta + (y - mu) / mu
        XtW = X.T * mu
        new = np.linalg.solve(XtW @ X + 1e-9 * np.eye(X.shape[1]), XtW @ z)
        if np.max(np.abs(new - beta)) < 1e-10:
            return new
        beta = new
    return beta


def _rows(ts, spend, sbar, region_trend, use_spend):
    rows = []
    for r in range(R):
        for t in ts:
            x = [0.0] * R
            x[r] = 1.0
            tr = [0.0] * (R if region_trend else 1)
            tr[r if region_trend else 0] = t / 12.0
            m = [0.0] * 11
            if t % 12 > 0:
                m[t % 12 - 1] = 1.0
            row = x + tr + m
            if use_spend:
                row.append(math.log(spend[r](t) / sbar[r]))
            rows.append(row)
    return np.array(rows)


def count_forecast(y, spend=None, start=0, end=92, region_trend=True, use_spend=True, horizon=range(96, 108)):
    """Fit y[r](t) for t in [start, end] and return each region's total over the horizon.
    y and spend are callables y[r](t) and spend[r](t) (spend in $K a month; the plan's months for the horizon)."""
    ts = list(range(start, end + 1))
    use = use_spend and spend is not None
    sbar = [float(np.mean([spend[r](t) for t in ts])) for r in range(R)] if use else None
    X = _rows(ts, spend, sbar, region_trend, use)
    yy = np.array([y[r](t) for r in range(R) for t in ts], float)
    b = poisson_glm(yy, X)
    Xf = _rows(list(horizon), spend, sbar, region_trend, use)
    return np.exp(Xf @ b).reshape(R, len(list(horizon))).sum(1)


def lag_pmf_from_links(lags, n=40):
    c = np.bincount(np.asarray(lags, int) - 1, minlength=n)[:n].astype(float)
    return c / c.sum()


def gamma_pmf_from_links(lags, n=40):
    from scipy.stats import gamma
    L = np.asarray(lags, float)
    k, loc, th = gamma.fit(L, floc=0)
    c = gamma.cdf(np.arange(n + 1), k, scale=th)
    p = np.diff(c)
    return p / p.sum()


def window_weight(pmf, t):
    return float(sum(pmf[L] for L in range(len(pmf)) if 96 <= t + 1 + L <= 107))


def founder_yield(landings, dep, pmf, t_lo, t_hi):
    """Founders landing in [t_lo, t_hi] over the leavers that could have founded them by then (each leaver weighted by
    the share of the lag distribution that lands inside the window)."""
    expo = 0.0
    for t, d in dep.items():
        if t > t_hi:
            continue
        lo = max(0, t_lo - t - 1)
        hi = t_hi - t
        if hi <= 0:
            continue
        expo += d * float(pmf[lo:hi].sum())
    return landings / expo if expo > 0 else 0.0


def founder_2027(dep_by_region, future, pmf, p, S, t_obs=92):
    """dep_by_region[r] is a dict month -> leavers; future[r] the planned leavers a month from t_obs + 1;
    p the yield per leaver (scalar or by origin region); S the origin-destination shares (rows sum to one)."""
    p = np.broadcast_to(np.asarray(p, float), (R,))
    out = np.zeros(R)
    months = set()
    for d in dep_by_region:
        months |= set(d)
    for t in sorted(months | set(range(t_obs + 1, 108))):
        w = window_weight(pmf, t)
        if w <= 0:
            continue
        for r in range(R):
            d = dep_by_region[r].get(t, 0) if t <= t_obs else future[r]
            if d:
                out += d * p[r] * w * S[r]
    return out
