"""The routes a solver can take from the window's cases to a set of barangays, on what the pack carries.

res[i, a]: the window's cases among residents of barangay i by age band a (0-14, 15-64, 65 and over);
hist[i, a]: the same barangay's cases by band over 2022 to 2026; pop[i, a]: CBMS residents by band;
emp[i]: CBMS employed residents; W[i, :]: the CBMS share of i's employed residents working in each
barangay (columns 0..N-1) and outside the city (column N). Each route returns the count the plan's
trigger reads for every barangay under that route's placement of each case.
"""
import numpy as np
from scipy.optimize import nnls

TRIGGER = 40


def residence(res, hist, pop, emp, W):
    return res.sum(1)


def local_marker(res, hist, pop, emp, W):
    """The children's and the elderly's rate carried to the whole population (a home-transmission marker)."""
    rate = res[:, [0, 2]].sum(1) / pop[:, [0, 2]].sum(1)
    return rate * pop.sum(1)


def _wc(W, n, renormalise=True):
    Wc = W[:, :n].copy()
    return Wc / Wc.sum(1, keepdims=True) if renormalise else Wc


def fractional(res, hist, pop, emp, W, phi=0.6, renormalise=True):
    """Each working-age case is a worker with the barangay's employment rate; a worker's case is split
    between home (1 - phi) and the place-of-work shares (phi); everyone else stays home."""
    n = res.shape[0]
    erate = np.clip(emp / pop[:, 1], 0, 1)
    work = res[:, 1] * erate
    out = res[:, 0] + res[:, 2] + res[:, 1] * (1 - erate) + (1 - phi) * work
    return out + (phi * work[:, None] * _wc(W, n, renormalise)).sum(0)


def _excess(res, hist):
    kappa = hist[:, 1] / np.maximum(hist[:, [0, 2]].sum(1), 1)
    return np.clip(res[:, 1] - kappa * res[:, [0, 2]].sum(1), 0, None)


def _nonhome(W):
    n = W.shape[0]
    Wn = W[:, :n].copy()
    np.fill_diagonal(Wn, 0.0)
    return Wn / Wn.sum(1, keepdims=True)


def excess_spread(res, hist, pop, emp, W):
    ex = _excess(res, hist)
    return res.sum(1) - ex + (ex[:, None] * _nonhome(W)).sum(0)


def inversion(res, hist, pop, emp, W):
    ex = _excess(res, hist)
    A = emp[:, None] * _nonhome(W)
    coef, _ = nnls(A, ex)
    return res.sum(1) - ex + coef * A.sum(0)


ROUTES_STEP = {
    "fractional_0.5": lambda *a: fractional(*a, phi=0.5),
    "fractional_0.6": lambda *a: fractional(*a, phi=0.6),
    "fractional_0.7": lambda *a: fractional(*a, phi=0.7),
    "fractional_0.8": lambda *a: fractional(*a, phi=0.8),
    "fractional_1.0": lambda *a: fractional(*a, phi=1.0),
    "fractional_0.6_outside_dropped": lambda *a: fractional(*a, phi=0.6, renormalise=False),
    "fractional_1.0_outside_dropped": lambda *a: fractional(*a, phi=1.0, renormalise=False),
    "excess_spread": excess_spread,
    "inversion": inversion,
}
ROUTES_EASY = {
    "residence": residence,
    "local_marker": local_marker,
}


def flagged(counts):
    return set(int(i) for i in np.nonzero(np.asarray(counts) >= TRIGGER - 1e-9)[0])


def margins(counts, gold):
    c = np.asarray(counts)
    inside = [c[i] - TRIGGER for i in gold]
    outside = [TRIGGER - c[i] for i in range(len(c)) if i not in gold]
    return min(inside), min(outside)
