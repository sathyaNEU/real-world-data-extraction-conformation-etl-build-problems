"""Every volatility construction the ladder prices, on aligned daily simple returns of the six holdings.

R: {holding: np.array of daily simple returns}, dates: the matching list of UK business days (the return's end date).
Each estimator returns the portfolio's twelve-month volatility in per cent at a step's policy weights.
"""
import datetime as dt

import numpy as np

import world as W

H = W.HOLDINGS


def wvec(step):
    w = W.weights(step)
    return np.array([w[h] for h in H])


def mat(R):
    return np.vstack([R[h] for h in H]).T


def blocks(X, k, anchor=0):
    """compounded returns over consecutive blocks of k business days, starting at row `anchor`"""
    X = X[anchor:]
    n = (len(X) // k) * k
    G = (1 + X[:n]).reshape(-1, k, X.shape[1]).prod(axis=1) - 1
    return G


def calendar_weeks(X, dates, weekday):
    """compounded returns from one week's last business day on or before `weekday` to the next; a week is kept only
    when the window holds its whole span"""
    keys = [d + dt.timedelta(days=(weekday - d.weekday()) % 7) for d in dates]
    G = []
    start = 0
    n = len(dates)
    while start < n:
        end = start
        while end + 1 < n and keys[end + 1] == keys[start]:
            end += 1
        key = keys[start]
        start_price_date = dates[start - 1] if start > 0 else W.WIN_START
        ok_start = start_price_date <= key - dt.timedelta(days=7)
        ok_end = not any(dates[-1] < key - dt.timedelta(days=j) and W.is_bday(key - dt.timedelta(days=j), "UK")
                         for j in range(0, 7))
        if ok_start and ok_end:
            G.append((1 + X[start:end + 1]).prod(axis=0) - 1)
        start = end + 1
    return np.array(G)


def months(X, dates):
    out, start = [], 0
    n = len(dates)
    while start < n:
        end = start
        while end + 1 < n and (dates[end + 1].year, dates[end + 1].month) == (dates[start].year, dates[start].month):
            end += 1
        out.append((1 + X[start:end + 1]).prod(axis=0) - 1)
        start = end + 1
    return np.array(out)


def vol_of(series, per_year):
    return float(np.sqrt(series.var(ddof=1) * per_year) * 100)


def simple(X, step, k=1, anchor=0, per_year=None):
    G = X if k == 1 else blocks(X, k, anchor)
    p = G @ wvec(step)
    return vol_of(p, per_year or 252.0 / k)


def weekly_cal(X, dates, step, weekday, per_year=52.0):
    p = calendar_weeks(X, dates, weekday) @ wvec(step)
    return vol_of(p, per_year)


def monthly(X, dates, step):
    p = months(X, dates) @ wvec(step)
    return vol_of(p, 12.0)


def leadlag(X, step, lags=1, bartlett=False, per_year=252.0):
    p = X @ wvec(step)
    y = p - p.mean()
    n = len(y)
    v = (y * y).sum() / (n - 1)
    for L in range(1, lags + 1):
        wt = (1 - L / (lags + 1)) if bartlett else 1.0
        v += 2 * wt * (y[L:] * y[:-L]).sum() / (n - 1)
    return float(np.sqrt(v * per_year) * 100)


def leadlag_matrix(X, step, lags=1):
    """the covariance-matrix form: daily covariance plus the lagged cross-covariances of every pair"""
    Y = X - X.mean(axis=0)
    n = len(Y)
    C = Y.T @ Y / (n - 1)
    for L in range(1, lags + 1):
        G = Y[L:].T @ Y[:-L] / (n - 1)
        C = C + G + G.T
    w = wvec(step)
    return float(np.sqrt(w @ C @ w * 252) * 100)


def mixed(X, step, anchor=0):
    """daily volatilities with weekly correlations"""
    sd = X.std(axis=0, ddof=1) * np.sqrt(252)
    C = np.corrcoef(blocks(X, 5, anchor).T)
    w = wvec(step)
    return float(np.sqrt(w @ (C * np.outer(sd, sd)) @ w) * 100)


def pair_ll(X, step):
    """lead and lag added on the UK mandate and North American pair only"""
    w = wvec(step)
    p = X @ w
    base = p.var(ddof=1)
    i, j = H.index("MAND"), H.index("NAEF")
    a, b = X[:, i] * w[i], X[:, j] * w[j]
    a = a - a.mean()
    b = b - b.mean()
    extra = 2 * ((a[1:] * b[:-1]).sum() + (b[1:] * a[:-1]).sum()) / (len(a) - 1)
    return float(np.sqrt((base + extra) * 252) * 100)


def ewma(X, step, lam=0.94, seed_n=20):
    p = X @ wvec(step)
    s2 = p[:seed_n].var()
    for x in p[seed_n:]:
        s2 = lam * s2 + (1 - lam) * x * x
    return float(np.sqrt(s2 * 252) * 100)


def ledoit_wolf_cc(X, step):
    Y = X - X.mean(0)
    T, N = Y.shape
    S = Y.T @ Y / T
    sd = np.sqrt(np.diag(S))
    Rm = S / np.outer(sd, sd)
    rbar = (Rm.sum() - N) / (N * (N - 1))
    F = rbar * np.outer(sd, sd)
    np.fill_diagonal(F, np.diag(S))
    pi_mat = ((Y ** 2).T @ (Y ** 2)) / T - S ** 2
    pi = pi_mat.sum()
    rho = np.diag(pi_mat).sum()
    for i in range(N):
        for j in range(N):
            if i == j:
                continue
            th_ii = ((Y[:, i] ** 3) * Y[:, j]).mean() - S[i, i] * S[i, j]
            th_jj = ((Y[:, j] ** 3) * Y[:, i]).mean() - S[j, j] * S[i, j]
            rho += rbar / 2 * (sd[j] / sd[i] * th_ii + sd[i] / sd[j] * th_jj)
    gamma = ((F - S) ** 2).sum()
    delta = max(0.0, min(1.0, (pi - rho) / gamma / T))
    C = delta * F + (1 - delta) * S
    w = wvec(step)
    return float(np.sqrt(w @ C @ w * 252) * 100), delta


def overlapping_annual(X, step):
    p = X @ wvec(step)
    lv = np.cumprod(1 + p)
    lv = np.concatenate([[1.0], lv])
    a = lv[252:] / lv[:-252] - 1
    return float(a.std(ddof=1) * 100)


# ------------------------------------------------------------------------------------------------ the families

def family(X, dates):
    """{name: function(step)} for every construction, grouped (period matrices built once)"""
    B5 = [blocks(X, 5, k) for k in range(5)]
    CW = [calendar_weeks(X, dates, wd) for wd in range(5)]
    MO = months(X, dates)
    F = {}
    F["R0 daily"] = lambda s: simple(X, s)
    F["R1 ewma 0.94"] = lambda s: ewma(X, s)
    F["R3 ledoit-wolf"] = lambda s: ledoit_wolf_cc(X, s)[0]
    F["R4 monthly"] = lambda s: vol_of(MO @ wvec(s), 12.0)
    # returns over periods of several days: refused by investment policy 4.3 (the returns are daily)
    for k in (2, 3, 4):
        for a in range(k):
            F["W %d-day blocks, anchor %d" % (k, a)] = (lambda s, k=k, a=a: simple(X, s, k, a))
    F["P pair lead-lag"] = lambda s: pair_ll(X, s)
    F["G lead-lag 1"] = lambda s: leadlag(X, s, 1)
    F["G lead-lag 2"] = lambda s: leadlag(X, s, 2)
    F["G newey-west 4"] = lambda s: leadlag(X, s, 4, True)
    F["G newey-west 5"] = lambda s: leadlag(X, s, 5, True)
    F["G cross-lag matrix 1"] = lambda s: leadlag_matrix(X, s, 1)
    F["W daily vols, five-day correlations"] = lambda s: mixed(X, s)
    for k in range(5):
        F["W five-day blocks, anchor %d" % k] = (lambda s, k=k: vol_of(B5[k] @ wvec(s), 52.0))
    for wd, nm in zip(range(5), ["Mon", "Tue", "Wed", "Thu", "Fri"]):
        F["W calendar weeks to %s" % nm] = (lambda s, wd=wd: vol_of(CW[wd] @ wvec(s), 52.0))
    # the same periods from the portfolio's daily return compounded (weights reset each day, not each period)
    for k in range(5):
        F["W five-day blocks of the daily portfolio, anchor %d" % k] = (lambda s, k=k: vol_of(blocks((X @ wvec(s))[:, None], 5, k)[:, 0], 52.0))
    for wd, nm in zip(range(5), ["Mon", "Tue", "Wed", "Thu", "Fri"]):
        F["W calendar weeks of the daily portfolio to %s" % nm] = (
            lambda s, wd=wd: vol_of(calendar_weeks((X @ wvec(s))[:, None], dates, wd)[:, 0], 52.0))
    return F


GOLDEN = lambda n: n.startswith("G ")
PARTIAL = lambda n: n.startswith("P ")
NOT_DAILY = lambda n: n.startswith("W ")       # periods of several days, refused by investment policy 4.3


def call(vols):
    """the largest step whose estimate is not more than the cap"""
    ok = [s for s, v in vols.items() if v <= W.CAP]
    return max(ok) if ok else None


def table(X, dates, steps=None):
    steps = steps or W.STEPS
    F = family(X, dates)
    return {n: {s: f(s) for s in steps} for n, f in F.items()}


def autocorr1(X, step):
    p = X @ wvec(step)
    y = p - p.mean()
    rho = float((y[1:] * y[:-1]).sum() / (y * y).sum())
    return rho, rho * np.sqrt(len(y))


def uk_na(X):
    i, j = H.index("MAND"), H.index("NAEF")
    same = float(np.corrcoef(X[:, i], X[:, j])[0, 1])
    nxt = float(np.corrcoef(X[:-1, i], X[1:, j])[0, 1])
    wk = blocks(X, 5)
    weekly = float(np.corrcoef(wk[:, i], wk[:, j])[0, 1])
    return same, nxt, weekly


def single_vols(X, dates):
    out = {}
    for k, h in enumerate(H):
        d = vol_of(X[:, k], 252)
        w = vol_of(blocks(X, 5)[:, k], 52)
        m = vol_of(months(X, dates)[:, k], 12)
        out[h] = (d, w, m)
    return out
