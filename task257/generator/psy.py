"""Psychometrics for task257, in numpy and scipy only: the bivariate normal distribution function (Genz's BVNU
algorithm), two-step maximum-likelihood polychoric and tetrachoric correlations, Pearson correlations with pairwise
deletion, the retention tests (random-data eigenvalues at the mean and the 95th percentile, eigenvalues above one,
Velicer's MAP in its original and revised forms), common-factor extraction (iterated principal axis, minres and
maximum likelihood) and rotation (varimax, promax, quartimin oblimin and geomin), each item placed under the factor
it loads on most."""
from __future__ import annotations

import numpy as np
from scipy.optimize import minimize, minimize_scalar
from scipy.special import ndtr, ndtri

# Gauss-Legendre half rules used by Genz's BVNU (6, 12 and 20 point rules, positive half)
_GL = {}
for _lg in (3, 6, 10):
    _x, _w = np.polynomial.legendre.leggauss(2 * _lg)
    _keep = _x > 0
    _GL[_lg] = (_x[_keep][::-1].copy(), _w[_keep][::-1].copy())


def bvnu(h, k, r):
    """P(X > h, Y > k) for a standard bivariate normal with correlation r; h, k arrays (finite or +-inf)."""
    h = np.asarray(h, dtype=float)
    k = np.asarray(k, dtype=float)
    h, k = np.broadcast_arrays(h, k)
    out = np.zeros(h.shape)
    inf_h, inf_k = np.isinf(h), np.isinf(k)
    # infinite bounds
    m = (h == np.inf) | (k == np.inf)
    out[m] = 0.0
    m2 = (h == -np.inf) & ~m
    out[m2 & (k == -np.inf)] = 1.0
    sel = m2 & (k != -np.inf)
    out[sel] = ndtr(-k[sel])
    sel = (k == -np.inf) & ~m & ~m2
    out[sel] = ndtr(-h[sel])
    fin = ~(inf_h | inf_k)
    if not fin.any():
        return out
    hh, kk = h[fin], k[fin]
    ar = abs(r)
    lg = 3 if ar < 0.3 else (6 if ar < 0.75 else 10)
    x, w = _GL[lg]
    hk = hh * kk
    if ar < 0.925:
        hs = (hh * hh + kk * kk) / 2
        asr = np.arcsin(r)
        bvn = np.zeros_like(hh)
        for xi, wi in zip(x, w):
            sn = np.sin(asr * (1 - xi) / 2)
            bvn += wi * np.exp((sn * hk - hs) / (1 - sn * sn))
            sn = np.sin(asr * (1 + xi) / 2)
            bvn += wi * np.exp((sn * hk - hs) / (1 - sn * sn))
        bvn = bvn * asr / (4 * np.pi) + ndtr(-hh) * ndtr(-kk)
    else:
        kk2 = -kk if r < 0 else kk.copy()
        hk2 = -hk if r < 0 else hk.copy()
        bvn = np.zeros_like(hh)
        if ar < 1:
            as_ = (1 - r) * (1 + r)
            a = np.sqrt(as_)
            bs = (hh - kk2) ** 2
            c = (4 - hk2) / 8
            d = (12 - hk2) / 16
            asr = -(bs / as_ + hk2) / 2
            t1 = np.where(asr > -100,
                          a * np.exp(np.maximum(asr, -100)) * (1 - c * (bs - as_) * (1 - d * bs / 5) / 3
                                                               + c * d * as_ * as_ / 5), 0.0)
            bvn = t1
            b = np.sqrt(bs)
            sp = np.sqrt(2 * np.pi) * ndtr(-b / a)
            t2 = np.where(hk2 > -100, np.exp(-np.minimum(hk2, 100) / 2) * sp * b * (1 - c * bs * (1 - d * bs / 5) / 3),
                          0.0)
            bvn = bvn - t2
            a2 = a / 2
            for xi, wi in zip(x, w):
                for s in (-1.0, 1.0):
                    xs = (a2 * (s * xi + 1)) ** 2
                    rs = np.sqrt(1 - xs)
                    asr2 = -(bs / xs + hk2) / 2
                    sp2 = 1 + c * xs * (1 + d * xs)
                    ep = np.exp(-hk2 * (1 - rs) / (2 * (1 + rs))) / rs
                    bvn = bvn + np.where(asr2 > -100, a2 * wi * np.exp(np.maximum(asr2, -100)) * (ep - sp2), 0.0)
            bvn = -bvn / (2 * np.pi)
        if r > 0:
            bvn = bvn + ndtr(-np.maximum(hh, kk2))
        else:
            L = np.where(hh < 0, ndtr(kk2) - ndtr(hh), ndtr(-hh) - ndtr(-kk2))
            bvn = np.where(hh >= kk2, -bvn, L - bvn)
    out[fin] = np.clip(bvn, 0.0, 1.0)
    return out


def bvn_cdf(h, k, r):
    """P(X <= h, Y <= k)."""
    return bvnu(-np.asarray(h, dtype=float), -np.asarray(k, dtype=float), r)


def _thresholds(margin):
    c = np.cumsum(margin)[:-1] / margin.sum()
    return np.concatenate([[-np.inf], ndtri(np.clip(c, 1e-12, 1 - 1e-12)), [np.inf]])


def polychoric_pair(x, y, kx, ky, correct=0.0, w=None):
    """Two-step ML polychoric (tetrachoric when both binary) correlation of integer codes 0..kx-1 and 0..ky-1
    (pairwise complete rows only); `correct` is added to empty cells (psych's continuity correction is 0.5);
    w: case weights, scaled to the number of cases. Returns (rho, n)."""
    tab = np.zeros((kx, ky))
    if w is None:
        np.add.at(tab, (x, y), 1)
    else:
        np.add.at(tab, (x, y), w * len(w) / w.sum())
    rk = tab.sum(1) > 0
    ck = tab.sum(0) > 0
    tab = tab[rk][:, ck]
    if correct:
        tab = np.where(tab == 0, correct, tab)
    a = _thresholds(tab.sum(1))
    b = _thresholds(tab.sum(0))
    A, B = np.meshgrid(a, b, indexing="ij")

    def nll(r):
        C = bvn_cdf(A, B, r)
        p = C[1:, 1:] - C[:-1, 1:] - C[1:, :-1] + C[:-1, :-1]
        return -(tab * np.log(np.clip(p, 1e-300, None))).sum()

    res = minimize_scalar(nll, bounds=(-0.995, 0.995), method="bounded", options={"xatol": 1e-7})
    return float(res.x), int(tab.sum())


def latent_corr(X, K, correct=0.0, weights=None):
    """Polychoric / tetrachoric correlation matrix of an (n x p) float array of integer codes 0..K-1 with NaN for
    missing, pairwise deletion. Returns (R, Npair)."""
    n, p = X.shape
    R = np.eye(p)
    Np = np.zeros((p, p), dtype=int)
    ok = ~np.isnan(X)
    for i in range(p):
        for j in range(i + 1, p):
            m = ok[:, i] & ok[:, j]
            r, cnt = polychoric_pair(X[m, i].astype(int), X[m, j].astype(int), int(K[i]), int(K[j]), correct,
                                     None if weights is None else weights[m])
            R[i, j] = R[j, i] = r
            Np[i, j] = Np[j, i] = cnt
    return R, Np


def pearson_corr(X, weights=None):
    """Pearson correlations with pairwise deletion of an (n x p) float array with NaN (optionally weighted)."""
    n, p = X.shape
    R = np.eye(p)
    ok = ~np.isnan(X)
    for i in range(p):
        for j in range(i + 1, p):
            m = ok[:, i] & ok[:, j]
            if weights is None:
                R[i, j] = R[j, i] = np.corrcoef(X[m, i], X[m, j])[0, 1]
            else:
                C = np.cov(X[m, i], X[m, j], aweights=weights[m])
                R[i, j] = R[j, i] = C[0, 1] / np.sqrt(C[0, 0] * C[1, 1])
    return R


def rank_columns(X):
    """Average ranks of each column's observed values (NaN kept), for rank (Spearman) correlations."""
    from scipy.stats import rankdata
    Y = X.copy()
    for j in range(X.shape[1]):
        m = ~np.isnan(X[:, j])
        Y[m, j] = rankdata(X[m, j])
    return Y


def eigen(R):
    return np.sort(np.linalg.eigvalsh(R))[::-1]


def random_eigen(n, p, reps=100, seed=257):
    """Eigenvalues of correlation matrices of normal random data with n rows and p columns: (mean, 95th pct)."""
    rng = np.random.default_rng(seed)
    ev = np.array([eigen(np.corrcoef(rng.standard_normal((n, p)), rowvar=False)) for _ in range(reps)])
    return ev.mean(0), np.percentile(ev, 95, axis=0, method="linear")


def keep_above(ev, ref):
    """Dimensions kept by a random-data comparison: the leading run of eigenvalues above the reference."""
    above = ev > ref
    return int(np.argmin(above)) if not above.all() else len(ev)


def kaiser(ev):
    return int((ev > 1).sum())


def velicer_map(R, power=2):
    """Velicer's minimum average partial test (power 2: 1976; power 4: the 2000 revision). Returns the count."""
    p = R.shape[0]
    w, v = np.linalg.eigh(R)
    idx = np.argsort(w)[::-1]
    w, v = w[idx], v[:, idx]
    load = v * np.sqrt(np.maximum(w, 0))
    off = ~np.eye(p, dtype=bool)
    vals = [np.mean(np.abs(R[off]) ** power)]
    for m in range(1, p - 1):
        A = load[:, :m]
        partial = R - A @ A.T
        dg = np.diag(partial)
        if (dg <= 1e-12).any():
            break
        d = np.sqrt(dg)
        pc = partial / np.outer(d, d)
        vals.append(np.mean(np.abs(pc[off]) ** power))
    return int(np.argmin(vals)), np.array(vals)


# ---------------------------------------------------------------- extraction

def paf(R, k, it=1000, tol=1e-9):
    """Iterated principal-axis factoring from squared multiple correlations."""
    h = 1 - 1 / np.diag(np.linalg.inv(R))
    for _ in range(it):
        Rr = R.copy()
        np.fill_diagonal(Rr, h)
        w, v = np.linalg.eigh(Rr)
        idx = np.argsort(w)[::-1][:k]
        L = v[:, idx] * np.sqrt(np.maximum(w[idx], 0))
        hn = (L ** 2).sum(1)
        if np.max(np.abs(hn - h)) < tol:
            h = hn
            break
        h = hn
    return L


def minres(R, k):
    """Minimum residual (unweighted least squares) extraction over the uniquenesses, as factor_analyzer runs it."""
    p = R.shape[0]

    def loads(psi):
        S = R.copy()
        np.fill_diagonal(S, 1 - psi)
        w, v = np.linalg.eigh(S)
        idx = np.argsort(w)[::-1][:k]
        return v[:, idx] * np.sqrt(np.maximum(w[idx], np.finfo(float).eps * 100))

    def obj(psi):
        S = R.copy()
        np.fill_diagonal(S, 1 - psi)
        L = loads(psi)
        return float(((S - L @ L.T) ** 2).sum())

    start = np.clip(1 / np.diag(np.linalg.inv(R)), 0.005, 1)
    res = minimize(obj, start, method="L-BFGS-B", bounds=[(0.005, 1)] * p, options={"maxiter": 2000, "ftol": 1e-14})
    return loads(res.x)


def ml(R, k):
    """Maximum-likelihood extraction (Joreskog's method, as R's factanal)."""
    p = R.shape[0]

    def parts(psi):
        sc = 1 / np.sqrt(psi)
        Ss = R * np.outer(sc, sc)
        w, v = np.linalg.eigh(Ss)
        idx = np.argsort(w)[::-1]
        return w[idx], v[:, idx]

    def fn(psi):
        w, _ = parts(psi)
        e = w[k:]
        return -(np.sum(np.log(e) - e) - k + p)

    def gr(psi):
        w, v = parts(psi)
        L = v[:, :k] * np.sqrt(np.maximum(w[:k] - 1, 0))
        L = L * np.sqrt(psi)[:, None]
        g = L @ L.T + np.diag(psi) - R
        return np.diag(g) / psi ** 2

    start = (1 - 0.5 * k / p) / np.diag(np.linalg.inv(R))
    res = minimize(fn, np.clip(start, 0.005, 1), jac=gr, method="L-BFGS-B", bounds=[(0.005, 1)] * p,
                   options={"maxiter": 5000, "ftol": 1e-15, "gtol": 1e-10})
    psi = res.x
    w, v = parts(psi)
    L = v[:, :k] * np.sqrt(np.maximum(w[:k] - 1, 0))
    return L * np.sqrt(psi)[:, None]


# ---------------------------------------------------------------- rotation

def varimax(L, normalize=True, it=1000, eps=1e-10):
    p, k = L.shape
    if k < 2:
        return L.copy(), np.eye(k)
    h = np.sqrt((L ** 2).sum(1)) if normalize else np.ones(p)
    X = L / h[:, None]
    T = np.eye(k)
    d = 0.0
    for _ in range(it):
        Z = X @ T
        B = X.T @ (Z ** 3 - Z @ np.diag((Z ** 2).sum(0)) / p)
        u, s, vt = np.linalg.svd(B)
        T = u @ vt
        dn = s.sum()
        if dn < d * (1 + eps):
            break
        d = dn
    return (X @ T) * h[:, None], T


def promax(L, m=4):
    V, T = varimax(L)
    Q = V * np.abs(V) ** (m - 1)
    U = np.linalg.lstsq(V, Q, rcond=None)[0]
    d = np.diag(np.linalg.inv(U.T @ U))
    U = U @ np.diag(np.sqrt(d))
    return V @ U


def _quartimin(L):
    L2 = L ** 2
    k = L.shape[1]
    X = L2 @ (np.ones((k, k)) - np.eye(k))
    return float((L2 * X).sum() / 4), L * X


def _geomin(L, delta=0.01):
    k = L.shape[1]
    L2 = L ** 2 + delta
    pro = np.exp(np.log(L2).sum(1) / k)
    return float(pro.sum()), (2 / k) * (L / L2) * pro[:, None]


def gpa_oblique(A, crit, T0, maxit=5000, tol=1e-8):
    """Gradient projection oblique rotation (Bernaards and Jennrich). Returns the pattern matrix and the criterion."""
    T = T0.copy()
    al = 1.0
    L = A @ np.linalg.inv(T).T
    f, Gq = crit(L)
    G = -(L.T @ Gq @ np.linalg.inv(T)).T
    for _ in range(maxit):
        Gp = G - T @ np.diag((T * G).sum(0))
        s = np.sqrt((Gp ** 2).sum())
        if s < tol:
            break
        al *= 2
        for _ in range(12):
            X = T - al * Gp
            Tt = X / np.sqrt((X ** 2).sum(0))
            Lt = A @ np.linalg.inv(Tt).T
            ft, Gqt = crit(Lt)
            if ft < f - 0.5 * s ** 2 * al:
                break
            al /= 2
        T, L, f, Gq = Tt, Lt, ft, Gqt
        G = -(L.T @ Gq @ np.linalg.inv(T)).T
    return L, f


def oblique(L, kind, starts=6, seed=257):
    crit = _quartimin if kind == "oblimin" else _geomin
    k = L.shape[1]
    best = None
    rng = np.random.default_rng(seed)
    for s in range(starts):
        if s == 0:
            T0 = np.eye(k)
        else:
            Q, _ = np.linalg.qr(rng.standard_normal((k, k)))
            T0 = Q
        P, f = gpa_oblique(L, crit, T0)
        if best is None or f < best[1] - 1e-10:
            best = (P, f)
    return best[0]


EXTRACT = {"principal axis": paf, "minres": minres, "maximum likelihood": ml}
ROTATE = {"varimax": lambda L: varimax(L)[0], "promax": promax, "oblimin": lambda L: oblique(L, "oblimin"),
          "geomin": lambda L: oblique(L, "geomin")}


def placements(L):
    """Each item under the factor it loads on most (absolute loading)."""
    return np.abs(L).argmax(1)


def partition(groups):
    """A canonical form of a partition of item indices: a sorted tuple of sorted tuples."""
    d = {}
    for i, g in enumerate(groups):
        d.setdefault(int(g), []).append(i)
    return tuple(sorted(tuple(v) for v in d.values()))
