"""The analysis: the river's annual 7-day low flows on the guidance's basis, the log-Pearson Type III fitted by
maximum likelihood with the regional skew, every route the ladder names, the scenarios, the block and the flip; and
the ask's Stage 2 periods, golden and stops."""
import math

import numpy as np
from scipy import optimize, special, stats

import world as W

G = W.REGIONAL_SKEW
LT = math.log10(W.SUSPEND_CFS)


def dist(mu, sd):
    return stats.pearson3(G, loc=mu, scale=sd)


A = 4.0 / G ** 2                     # the gamma shape of the logarithms for the regional skew
LGA = special.gammaln(A)


def _parts(mu, sd):
    """The Pearson Type III of the logarithms as xi + b * Y, Y a unit gamma of shape A (b < 0 for a negative skew)."""
    return mu - 2.0 * sd / G, sd * G / 2.0


def fit(obs, above=0, below=0):
    """Maximum likelihood for the mean and standard deviation of the log10 flows, skew held at the regional value:
    exact values, and years known only to lie above (or below) the suspension flow."""
    obs = np.asarray(obs, float)

    def nll(par):
        mu, sd = par[0], math.exp(par[1])
        xi, b = _parts(mu, sd)
        y = (obs - xi) / b
        if np.any(y <= 0):
            return 1e12
        ll = float(np.sum((A - 1) * np.log(y) - y)) - len(obs) * (LGA + math.log(abs(b)))
        if above or below:
            yt = (LT - xi) / b
            if yt <= 0:
                return 1e12
            p_above = float(special.gammainc(A, yt))        # P(log flow > LT) = P(Y < yt) when b < 0
            ll += above * math.log(max(p_above, 1e-300)) + below * math.log(max(1.0 - p_above, 1e-300))
        return -ll
    s0 = np.array([obs.mean(), math.log(obs.std())])
    best = None
    for start in (s0, s0 + [0.05, 0.15], s0 - [0.05, 0.10]):
        r = optimize.minimize(nll, start, method="Nelder-Mead", options=dict(xatol=1e-11, fatol=1e-12, maxiter=6000))
        if best is None or r.fun < best.fun:
            best = r
    return float(best.x[0]), float(math.exp(best.x[1]))


def ema(obs, above, iters=500):
    """The expected moments algorithm with the skew held: each year above the suspension flow enters the moments as
    the conditional expectations of the logarithm and its square above it."""
    obs = np.asarray(obs, float)
    mu, sd = obs.mean(), obs.std()
    for _ in range(iters):
        xi, b = _parts(mu, sd)
        yt = (LT - xi) / b
        p0 = special.gammainc(A, yt)
        e1 = A * special.gammainc(A + 1, yt) / p0
        e2 = A * (A + 1) * special.gammainc(A + 2, yt) / p0
        m1, m2 = xi + b * e1, xi * xi + 2 * xi * b * e1 + b * b * e2
        n = len(obs) + above
        mu = (obs.sum() + above * m1) / n
        sd = math.sqrt((((obs - mu) ** 2).sum() + above * (m2 - 2 * mu * m1 + mu * mu)) / (n - 1))
    return float(mu), float(sd)


def moments(obs):
    obs = np.asarray(obs, float)
    return float(obs.mean()), float(obs.std(ddof=1))


def flow(p, mu, sd):
    return float(10 ** dist(mu, sd).ppf(p))


def withdrawal(q):
    return min(W.PERMIT_MAX_MGD, max(0.0, q - W.PASSBY_CFS) * W.MGD_PER_CFS)


def shortfall(q, demand=None):
    return max(0.0, (demand or W.STAGE2_DEMAND[2027]) - withdrawal(q))


def block(s):
    return round(math.ceil(round(s / W.BLOCK_MGD, 9)) * W.BLOCK_MGD, 1)


def recurrence_at(q, mu, sd):
    return 1.0 / float(dist(mu, sd).cdf(math.log10(q)))


# ---------------------------------------------------------------- the record on the guidance's basis
def record(gauge_minima, reports):
    """gauge_minima {year: cfs}; reports {year: ("measured", cfs) or ("none", None)} for the report years on file.
    Returns the log10 gauged values, the log10 measured report values and the count of years without a suspension."""
    lg = np.log10([v for _, v in sorted(gauge_minima.items())])
    meas = [v for _, (k, v) in sorted(reports.items()) if k == "measured"]
    silent = sum(1 for k, _ in reports.values() if k == "none")
    return lg, np.log10(meas), silent


def routes(lg, lm, silent):
    """Each rung's (mu, sd) on the same record."""
    both = np.concatenate([lg, lm])
    return {
        "R0": fit(lg),                                                     # the gauge alone
        "R0m": moments(lg),
        "R1": fit(both),                                                   # the measured report years added (default)
        "R1m": moments(both),
        "R1b": fit(np.concatenate([both, np.full(silent, LT)])),           # silent years at the suspension flow
        "R1c": fit(lg, below=len(lm)),                                     # measured years as below, silent dropped
        "R1d": fit(lg, above=silent, below=len(lm)),                       # every report year censored
        "R2": fit(both, above=silent),                                     # the censored likelihood (golden)
    }


def decision(mu, sd):
    q = {t: flow(1.0 / t, mu, sd) for t in W.SCENARIOS}
    s = {t: shortfall(q[t]) for t in W.SCENARIOS}
    b = block(s[50])
    q_flip = W.PASSBY_CFS + (W.STAGE2_DEMAND[2027] - b) / W.MGD_PER_CFS
    return dict(mu=mu, sd=sd, flows=q, withdrawals={t: withdrawal(q[t]) for t in W.SCENARIOS}, shortfalls=s,
                block=b, flip_flow=q_flip, flip_years=recurrence_at(q_flip, mu, sd))


# ---------------------------------------------------------------- the ask: each declared Stage 2 period
def ask_periods(days, town, periods):
    """[(from, through, days, average, highest)] of the town's own system supply over each Stage 2 period."""
    out = []
    for a, b in periods:
        i, j = days.index(a), days.index(b)
        v = town[i:j + 1]
        out.append((a, b, j - i + 1, float(np.mean(v)), float(np.max(v))))
    return out
