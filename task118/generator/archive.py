"""The headline-test archive: simulation of every concluded test at package level, and the estimator
family the build asserts (the golden empirical-Bayes rule and each rival the change log refutes)."""
import numpy as np
from scipy.optimize import minimize

import params as P


def rng_for(*key):
    return np.random.default_rng(np.random.SeedSequence([P.SEED] + list(key)))


# ---------------------------------------------------------------------------------- simulation

def simulate_tests(rng, n, kp, npk, ctr, gate, sig=0.28):
    """Return a list of tests; each test is dict(ns, cs, ship) where ship is the index of the shipped
    package (0 = control kept)."""
    out = []
    ks = rng.choice(np.arange(1, len(kp) + 1), size=n, p=kp)
    for t in range(n):
        k = int(ks[t])
        m = k + 1
        N = npk / ctr * float(np.exp(sig * rng.standard_normal()))
        pc = ctr * float(np.exp(0.2 * rng.standard_normal()))
        delta = P.TRUE_MU + P.TRUE_TAU * rng.standard_normal(k)
        ns = np.maximum(300, np.round(N * rng.uniform(0.97, 1.03, size=m))).astype(np.int64)
        p = np.clip(np.concatenate([[pc], pc * (1 + delta)]), 1e-4, 0.5)
        cs = rng.binomial(ns, p).astype(np.int64)
        while (cs == 0).any():          # a package with no clicks cannot carry a lift; redraw it
            cs = rng.binomial(ns, p).astype(np.int64)
        pv = cs / ns
        j = int(np.argmax(pv[1:])) + 1
        pb = (cs[0] + cs[j]) / (ns[0] + ns[j])
        z = (pv[j] - pv[0]) / np.sqrt(pb * (1 - pb) * (1 / ns[0] + 1 / ns[j]))
        out.append(dict(ns=ns, cs=cs, ship=(j if z > gate else 0)))
    return out


# ---------------------------------------------------------------------------------- estimators

def package_lifts(test):
    """Observed relative lift and its sampling variance for every variant package of one test."""
    ns, cs = test["ns"].astype(float), test["cs"].astype(float)
    p = cs / ns
    r = p[1:] / p[0]
    L = r - 1
    se2 = r ** 2 * ((1 - p[1:]) / (ns[1:] * p[1:]) + (1 - p[0]) / (ns[0] * p[0]))
    return L, se2


def pooled(tests):
    L, S = [], []
    for t in tests:
        a, b = package_lifts(t)
        L.append(a)
        S.append(b)
    return np.concatenate(L), np.concatenate(S)


def prior_mom(L, S2):
    mu = float(L.mean())
    tau2 = float(L.var() - S2.mean())
    return mu, max(tau2, 0.0)


def prior_ml(L, S2, start):
    def nll(x):
        mu, lt = x
        v = np.exp(lt) + S2
        return 0.5 * float(np.sum(np.log(v) + (L - mu) ** 2 / v))
    r = minimize(nll, [start[0], np.log(max(start[1], 1e-6))], method="Nelder-Mead",
                 options=dict(xatol=1e-10, fatol=1e-10, maxiter=4000))
    return float(r.x[0]), float(np.exp(r.x[1]))


def prior_dl(L, S2):
    w = 1 / S2
    mu_w = float(np.sum(w * L) / np.sum(w))
    Q = float(np.sum(w * (L - mu_w) ** 2))
    k = len(L)
    tau2 = max(0.0, (Q - (k - 1)) / (np.sum(w) - np.sum(w ** 2) / np.sum(w)))
    ws = 1 / (S2 + tau2)
    mu = float(np.sum(ws * L) / np.sum(ws))
    return mu, tau2


def test_winning(test, prior, shrink=True):
    """Winning lift of one test: the shipped package's lift (shrunk if asked), zero when control kept."""
    j = test["ship"]
    if j == 0:
        return 0.0
    L, S2 = package_lifts(test)
    if not shrink:
        return float(L[j - 1])
    mu, tau2 = prior
    B = tau2 / (tau2 + S2[j - 1])
    return float(mu + B * (L[j - 1] - mu))


def desk_lift(tests, prior=None, shrink=True, weights=None):
    v = np.array([test_winning(t, prior, shrink) for t in tests])
    if weights is None:
        return float(v.mean())
    w = np.asarray(weights, float)
    return float(np.sum(w * v) / np.sum(w))


def shrink_then_max(tests, prior):
    mu, tau2 = prior
    vals = []
    for t in tests:
        L, S2 = package_lifts(t)
        s = mu + tau2 / (tau2 + S2) * (L - mu)
        vals.append(max(0.0, float(s.max())))
    return float(np.mean(vals))


def absolute_points(tests):
    vals = []
    for t in tests:
        j = t["ship"]
        if j == 0:
            vals.append(0.0)
            continue
        p = t["cs"] / t["ns"]
        vals.append(float(p[j] - p[0]))
    return float(np.mean(vals))


def ship_z(test):
    ns, cs = test["ns"], test["cs"]
    p = cs / ns
    j = int(np.argmax(p[1:])) + 1
    pb = (cs[0] + cs[j]) / (ns[0] + ns[j])
    return float((p[j] - p[0]) / np.sqrt(pb * (1 - pb) * (1 / ns[0] + 1 / ns[j])))
