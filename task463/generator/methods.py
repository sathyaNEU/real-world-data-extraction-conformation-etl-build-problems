"""Index computations over product-month arrays: P (unit price), Q (units) and E (spending) for one item, rows the
product lines, columns the thirteen months. Every form an analyst might build: direct, chained and multilateral
(GEKS, CCDI), Tornqvist, Fisher, Laspeyres and Jevons, and the item's unit value."""
import math

import numpy as np


def matched(P, a, b):
    return ~np.isnan(P[:, a]) & ~np.isnan(P[:, b]) & (P[:, a] > 0) & (P[:, b] > 0)


def tornqvist(P, Q, E, a, b):
    ok = matched(P, a, b)
    sa = E[ok, a] / E[ok, a].sum()
    sb = E[ok, b] / E[ok, b].sum()
    return math.exp(float(np.sum(0.5 * (sa + sb) * np.log(P[ok, b] / P[ok, a]))))


def fisher(P, Q, E, a, b):
    ok = matched(P, a, b)
    las = np.sum(P[ok, b] * Q[ok, a]) / np.sum(P[ok, a] * Q[ok, a])
    paa = np.sum(P[ok, b] * Q[ok, b]) / np.sum(P[ok, a] * Q[ok, b])
    return math.sqrt(las * paa)


def laspeyres(P, Q, E, a, b):
    ok = matched(P, a, b)
    return float(np.sum(P[ok, b] * Q[ok, a]) / np.sum(P[ok, a] * Q[ok, a]))


def jevons(P, Q, E, a, b):
    ok = matched(P, a, b)
    return math.exp(float(np.mean(np.log(P[ok, b] / P[ok, a]))))


def chained(f, P, Q, E, a=0, b=None):
    b = P.shape[1] - 1 if b is None else b
    v = 1.0
    for m in range(a + 1, b + 1):
        v *= f(P, Q, E, m - 1, m)
    return v


def geks(f, P, Q, E, a=0, b=None):
    """GEKS over every month of the window, the index between months a and b."""
    T = P.shape[1]
    b = T - 1 if b is None else b
    return math.exp(float(np.mean([math.log(f(P, Q, E, a, k)) + math.log(f(P, Q, E, k, b)) for k in range(T)])))


def ccdi(P, Q, E, a=0, b=None):
    """The multilateral Tornqvist (CCDI) over a balanced panel."""
    T = P.shape[1]
    b = T - 1 if b is None else b
    S = E / E.sum(axis=0, keepdims=True)
    sbar = S.mean(axis=1)
    lp = np.log(P)
    lbar = lp.mean(axis=1)

    def lev(t):
        return float(np.sum(0.5 * (S[:, t] + sbar) * (lp[:, t] - lbar)))
    return math.exp(lev(b) - lev(a))


def unit_value(P, Q, E, a, b):
    return float((E[:, b].sum() / Q[:, b].sum()) / (E[:, a].sum() / Q[:, a].sum()))


def rate(x):
    """An index ratio as a percentage change."""
    return (x - 1.0) * 100.0


def drift_free(P, Q, E):
    """The twelve-month change by every comparison that does not chain the months: direct Tornqvist and Fisher, GEKS on
    each, and CCDI."""
    T = P.shape[1] - 1
    return {"direct_tornqvist": rate(tornqvist(P, Q, E, 0, T)), "direct_fisher": rate(fisher(P, Q, E, 0, T)),
            "geks_tornqvist": rate(geks(tornqvist, P, Q, E)), "geks_fisher": rate(geks(fisher, P, Q, E)),
            "ccdi": rate(ccdi(P, Q, E))}


def routes(P, Q, E):
    """The other ways the twelve-month change gets built: linked month-on-month comparisons and unweighted ones."""
    return {"chained_tornqvist": rate(chained(tornqvist, P, Q, E)), "chained_fisher": rate(chained(fisher, P, Q, E)),
            "chained_laspeyres": rate(chained(laspeyres, P, Q, E)), "direct_jevons": rate(jevons(P, Q, E, 0, P.shape[1] - 1)),
            "chained_jevons": rate(chained(jevons, P, Q, E)), "unit_value": rate(unit_value(P, Q, E, 0, P.shape[1] - 1))}
