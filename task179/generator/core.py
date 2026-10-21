"""Shared numerics for the task179 generator: lag distributions, truncated fits, growth, renewal projection.
Only the generator imports this file; verify.py carries its own code path."""
import numpy as np
from scipy import stats, optimize

L = 80  # longest lag carried, days


def dgamma_pmf(mean, sd):
    """Discretised gamma on lags 1..L (mass in (k-0.5, k+0.5]), renormalised."""
    sh = (mean / sd) ** 2
    sc = sd * sd / mean
    c = stats.gamma.cdf(np.arange(0, L + 1) + 0.5, sh, scale=sc)
    w = np.diff(c)
    return w / w.sum()


def family_pmf(fam, p):
    a, b = np.exp(p)
    dist = {"gamma": stats.gamma(a, scale=b), "weibull": stats.weibull_min(a, scale=b),
            "lognorm": stats.lognorm(b, scale=a)}[fam]
    c = dist.cdf(np.arange(0, L + 1) + 0.5)
    w = np.diff(c)
    return w / w.sum()


def fit_lags(lags, src_day, last_day, fam="gamma", truncated=True):
    """Maximum likelihood fit of a discretised family to integer lags. With truncated=True each pair is read
    against the longest lag its source could show by last_day (the case's onset no later than last_day)."""
    lags = np.asarray(lags, int)
    maxl = np.clip(np.asarray(last_day - src_day, int), 1, L)
    m = lags.mean()
    p0 = {"gamma": [np.log(2.5), np.log(m / 2.5)], "weibull": [np.log(1.6), np.log(m * 1.1)],
          "lognorm": [np.log(m * 0.85), np.log(0.6)]}[fam]

    def nll(p):
        w = family_pmf(fam, p)
        cw = np.cumsum(w)
        ll = np.log(w[np.clip(lags, 1, L) - 1] + 1e-300)
        if truncated:
            ll = ll - np.log(cw[maxl - 1] + 1e-300)
        return -ll.sum()

    r = optimize.minimize(nll, p0, method="Nelder-Mead", options={"maxiter": 6000, "xatol": 1e-8, "fatol": 1e-8})
    return family_pmf(fam, r.x), float(r.fun)


def reverse_time_npmle(lags, src_day, last_day):
    """Nonparametric estimate for right-truncated lags: the reverse-time hazard (Lagakos, Barraj and De Gruttola)."""
    lags = np.asarray(lags, int)
    maxl = np.asarray(last_day - src_day, int)
    F = np.ones(L + 1)
    for x in range(L, 0, -1):
        at = ((lags <= x) & (maxl >= x)).sum()
        ev = (lags == x).sum()
        F[x - 1] = F[x] * ((1 - ev / at) if at > 0 else 1.0)
    w = np.diff(F)
    return w / w.sum()


def empirical(lags):
    lags = np.asarray(lags, int)
    w = np.bincount(lags[(lags >= 1) & (lags <= L)], minlength=L + 1)[1:].astype(float)
    return w / w.sum()


def mean_of(w):
    return float(np.dot(np.arange(1, L + 1), w))


def growth_rate(daily, first, last):
    """Log-linear least squares on daily counts first..last inclusive (index = day)."""
    x = np.arange(first, last + 1)
    return float(np.polyfit(x, np.log(daily[x]), 1)[0])


def growth_rate_poisson(daily, first, last):
    x = np.arange(first, last + 1)
    y = daily[x]
    xc = x - x.mean()

    def nll(p):
        mu = np.exp(p[0] + p[1] * xc)
        return (mu - y * np.log(mu)).sum()
    r = optimize.minimize(nll, [np.log(y.mean()), 0.04], method="Nelder-Mead", options={"xatol": 1e-10, "fatol": 1e-10})
    return float(r.x[1])


def R_from_growth(r, w):
    return float(1.0 / np.sum(w * np.exp(-r * np.arange(1, L + 1))))


def R_renewal_ratio(daily, w, first, last):
    num = den = 0.0
    for t in range(first, last + 1):
        num += daily[t]
        k = min(L, t)
        den += np.dot(w[:k], daily[t - 1::-1][:k])
    return float(num / den)


def project(daily, last_obs, R, w, cut, cut_from, until):
    """Expected daily onsets after last_obs by the renewal equation; a case with onset on or after cut_from
    transmits at R*(1-cut). Returns the full series to day `until` inclusive (observed then projected)."""
    x = list(map(float, daily[:last_obs + 1]))
    for t in range(last_obs + 1, until + 1):
        lam = 0.0
        for s in range(1, min(L, t) + 1):
            src = t - s
            lam += w[s - 1] * (R if src < cut_from else R * (1 - cut)) * x[src]
        x.append(lam)
    return np.array(x)
