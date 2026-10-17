import numpy as np
from scipy.stats import norm
from scipy.optimize import minimize_scalar
from scipy.special import owens_t

def bvn_cdf(h, k, r):
    """P(X<h, Y<k) for standard bivariate normal with correlation r (vectorised via Owen's T)"""
    h = np.asarray(h, float); k = np.asarray(k, float)
    out = np.zeros(np.broadcast(h, k).shape)
    H, K = np.broadcast_arrays(h, k)
    inf_h, inf_k = np.isinf(H), np.isinf(K)
    # handle infinities
    both = ~inf_h & ~inf_k
    hh, kk = H[both], K[both]
    sq = np.sqrt(1 - r * r)
    with np.errstate(divide="ignore", invalid="ignore"):
        a1 = np.where(hh != 0, (kk - r * hh) / (hh * sq), np.inf)
        a2 = np.where(kk != 0, (hh - r * kk) / (kk * sq), np.inf)
    t1 = np.where(hh != 0, owens_t(hh, a1), 0.0)
    t2 = np.where(kk != 0, owens_t(kk, a2), 0.0)
    beta = np.where((hh * kk < 0) | ((hh * kk == 0) & ((hh + kk) < 0)), 0.5, 0.0)
    val = 0.5 * norm.cdf(hh) + 0.5 * norm.cdf(kk) - t1 - t2 - beta
    # exact zero cases
    zz = (hh == 0) & (kk == 0)
    val = np.where(zz, 0.25 + np.arcsin(r) / (2 * np.pi), val)
    out[both] = val
    # one infinite
    m = inf_h & ~inf_k
    out[m] = np.where(H[m] > 0, norm.cdf(K[m]), 0.0)
    m = ~inf_h & inf_k
    out[m] = np.where(K[m] > 0, norm.cdf(H[m]), 0.0)
    m = inf_h & inf_k
    out[m] = np.where((H[m] > 0) & (K[m] > 0), 1.0, 0.0)
    return out

def thresholds(x, cats=5):
    c = np.array([(x <= j).mean() for j in range(1, cats)])
    c = np.clip(c, 1e-6, 1 - 1e-6)
    return np.r_[-np.inf, norm.ppf(c), np.inf]

def polychoric(x, y, cats=5):
    tx, ty = thresholds(x, cats), thresholds(y, cats)
    tab = np.zeros((cats, cats))
    np.add.at(tab, (x - 1, y - 1), 1)
    def nll(r):
        F = bvn_cdf(tx[:, None], ty[None, :], r)
        P = F[1:, 1:] - F[:-1, 1:] - F[1:, :-1] + F[:-1, :-1]
        return -(tab * np.log(np.clip(P, 1e-12, 1))).sum()
    return minimize_scalar(nll, bounds=(-0.99, 0.99), method="bounded").x

def poly_matrix(X):
    p = X.shape[1]
    R = np.eye(p)
    for i in range(p):
        for j in range(i + 1, p):
            R[i, j] = R[j, i] = polychoric(X[:, i], X[:, j])
    return R
