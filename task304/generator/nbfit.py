"""task304: negative binomial (NB2) regression with a log link, fitted by IRLS for the coefficients at each overdispersion
value and a bounded profile search for the overdispersion. Used by the analysis (the golden path) and the checks."""
import numpy as np
from scipy.optimize import minimize_scalar
from scipy.special import gammaln


def _irls(X, y, alpha, beta0=None, iters=60):
    beta = np.zeros(X.shape[1]) if beta0 is None else beta0.copy()
    if beta0 is None:
        beta[0] = np.log(max(y.mean(), 1e-3))
    for _ in range(iters):
        eta = X @ beta
        mu = np.exp(eta)
        w = mu / (1.0 + alpha * mu)
        z = eta + (y - mu) / mu
        XtW = X.T * w
        new = np.linalg.solve(XtW @ X, XtW @ z)
        if np.max(np.abs(new - beta)) < 1e-10:
            beta = new
            break
        beta = new
    return beta


def _loglik(y, mu, alpha):
    r = 1.0 / alpha
    return float((gammaln(y + r) - gammaln(r) - gammaln(y + 1) + r * np.log(r / (r + mu)) + y * np.log(mu / (r + mu))).sum())


def nb2(X, y):
    """Maximum likelihood NB2: returns (beta, alpha, loglik)."""
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float)
    start = _irls(X, y, 1e-6)
    cache = {}

    def negprof(la):
        a = float(np.exp(la))
        b = _irls(X, y, a, start)
        cache[la] = b
        return -_loglik(y, np.exp(X @ b), a)

    res = minimize_scalar(negprof, bounds=(np.log(1e-4), np.log(5.0)), method="bounded",
                          options={"xatol": 1e-7, "maxiter": 500})
    a = float(np.exp(res.x))
    b = _irls(X, y, a, cache.get(res.x, start))
    return b, a, _loglik(y, np.exp(X @ b), a)
