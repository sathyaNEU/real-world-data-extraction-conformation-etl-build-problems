"""Recovering the per-posting rate from a voucher-level indicator.

The platform writes one verdict per voucher, so an entry carrying k postings flags with probability
1 - (1 - r) ** k. The per-entry log likelihood in r has a monotone score, so the maximum has exactly one
root and bisection finds it. `recover_unit` is the estimand executed literally for one population; the
group figure is the sum over units of the unit's rate times the unit's postings.

The likelihood depends on the entries only through, for each distinct posting count, how many entries of
that size flagged and how many did not, so every estimator here works on that grouping. It is exactly
equivalent to working entry by entry and is what makes the generator's per-unit tuning affordable.
"""
import numpy as np

ITERS = 72          # 0.9 / 2 ** 72 is far below any rounding the build grades


def group(k, f):
    """(sizes, flagged per size, entries per size) for one population of entries."""
    k = np.asarray(k, dtype=np.int64)
    f = np.asarray(f, dtype=np.int64)
    if k.size == 0:
        return np.array([]), np.array([]), np.array([])
    sizes, inv = np.unique(k, return_inverse=True)
    n = np.bincount(inv, minlength=sizes.size).astype(np.float64)
    hit = np.bincount(inv, weights=f, minlength=sizes.size)
    return sizes.astype(np.float64), hit, n


def _bisect(fn, lo=1e-10, hi=0.9, iters=ITERS):
    """fn is increasing in r and crosses zero once."""
    a, b = lo, hi
    for _ in range(iters):
        m = (a + b) / 2
        if fn(m) < 0:
            a = m
        else:
            b = m
    return (a + b) / 2


def recover_unit(k, f):
    """Maximum likelihood per-posting rate for one population of entries."""
    s, hit, n = group(k, f)
    if s.size == 0 or hit.sum() == 0:
        return 0.0
    if hit.sum() == n.sum():          # every entry flagged: the rate is not identified from above
        return float("nan")

    def score(r):
        q = (1.0 - r) ** s
        return float((hit * s * q / (np.maximum(1.0 - q, 1e-300) * (1.0 - r))).sum()
                     - ((n - hit) * s / (1.0 - r)).sum())

    # score is decreasing in r, so bisect on its negation
    return _bisect(lambda r: -score(r))


def recover_mom(k, f):
    """Method of moments: match the total flag count to its expectation. A licensed variant."""
    s, hit, n = group(k, f)
    if s.size == 0 or hit.sum() == 0:
        return 0.0
    tot = float(hit.sum())
    return _bisect(lambda r: float((n * (1.0 - (1.0 - r) ** s)).sum()) - tot)


def recover_cloglog(k, f):
    """The complementary log-log form, matched on the total. A licensed variant."""
    s, hit, n = group(k, f)
    if s.size == 0 or hit.sum() == 0:
        return 0.0
    tot = float(hit.sum())
    return _bisect(lambda r: float((n * (1.0 - np.exp(-r * s))).sum()) - tot)


def licensed(k, f):
    """Every licensed estimator's recovered count for one population, as a dict."""
    T = float(np.asarray(k, dtype=np.int64).sum())
    return {"mle": recover_unit(k, f) * T,
            "mom": recover_mom(k, f) * T,
            "cloglog": recover_cloglog(k, f) * T}
