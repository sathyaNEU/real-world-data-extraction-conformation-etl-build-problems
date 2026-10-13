"""The estimators and the decision quantities, shared by the goldens and the checks (verify.py has its own)."""
from scipy.optimize import brentq


def _parts(pools, p):
    """Score, information, the information's derivative and E[l' l''] of the pooled likelihood at p."""
    U = I = dI = k = 0.0
    for m, x in pools:
        q = (1.0 - p) ** m
        pi = 1.0 - q
        d1 = m * (1.0 - p) ** (m - 1)
        d2 = -m * (m - 1) * (1.0 - p) ** (m - 2)
        U += (d1 / pi) if x else (-d1 / q)
        den = pi * q
        I += d1 * d1 / den
        dI += (2.0 * d1 * d2 * den - d1 * d1 * d1 * (1.0 - 2.0 * pi)) / (den * den)
        k += d1 * d2 / den - d1 ** 3 * (1.0 / pi ** 2 - 1.0 / q ** 2)
    return U, I, dI, k


def mle(pools):
    """Maximum likelihood estimate of the per-mosquito infection probability from pools [(size, positive)] of
    varying size, every mosquito in a pool sharing one probability and the test finding any infected one."""
    if not pools or not any(x for m, x in pools):
        return 0.0
    if all(x for m, x in pools):
        raise ValueError("every pool positive")
    return brentq(lambda p: _parts(pools, p)[0], 1e-9, 0.5, xtol=1e-15)


def bcmle(pools):
    """Bias-corrected maximum likelihood estimate: Firth's modified score, the score less the information times the
    first-order bias of the estimate."""
    if not pools or not any(x for m, x in pools):
        return 0.0

    def f(p):
        U, I, dI, k = _parts(pools, p)
        return U - (k - dI) / (2.0 * I)
    return brentq(f, 1e-9, 0.5, xtol=1e-15)


def mir(pools):
    """Minimum infection rate: positive pools over mosquitoes tested."""
    tested = sum(m for m, x in pools)
    return (sum(1 for m, x in pools if x) / tested) if tested else 0.0
