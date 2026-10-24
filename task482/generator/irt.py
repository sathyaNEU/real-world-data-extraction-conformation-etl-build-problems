"""The item response machinery every route shares: the likelihood of each student's scored responses on the grid,
latent regression by EM, plausible-value draws, and the share estimators the design measures."""
import numpy as np

import world as W


def loglik(y, mods, admin):
    """Log-likelihood of each student's administered responses on the grid W.Q (n x len(Q)). y and admin are
    n x 2 x 5; an item not administered (not reached) carries no information."""
    n = len(y)
    out = np.zeros((n, len(W.Q)))
    for j in range(2):
        for k in range(W.N_ITEM):
            aa = W.A[mods[:, j], k][:, None]; bb = W.B[mods[:, j], k][:, None]
            pq = 1.0 / (1.0 + np.exp(-aa * (W.Q[None, :] - bb)))
            yy = y[:, j, k][:, None]; ad = admin[:, j, k][:, None]
            out += ad * (yy * np.log(pq) + (1 - yy) * np.log(1 - pq))
    return out


def norm_lik(ll):
    return np.exp(ll - ll.max(1, keepdims=True))


def lr_em(L, X, groups=None, iters=300, tol=1e-7):
    """Latent regression theta ~ N(X g, s2) by EM on the grid; L is the normalised likelihood (n x Q).
    groups: per-student group index for a group-specific variance, or None for one variance."""
    n = len(L)
    g = np.zeros(X.shape[1])
    s2 = np.ones(n)
    XtXi = np.linalg.pinv(X.T @ X)
    for _ in range(iters):
        mu = X @ g
        w = L * np.exp(-0.5 * (W.Q[None, :] - mu[:, None]) ** 2 / s2[:, None])
        w /= w.sum(1, keepdims=True)
        gn = XtXi @ (X.T @ (w @ W.Q))
        mu = X @ gn
        r2 = (w * (W.Q[None, :] - mu[:, None]) ** 2).sum(1)
        if groups is None:
            s2 = np.full(n, r2.mean())
        else:
            v = np.bincount(groups, r2) / np.bincount(groups)
            s2 = v[groups]
        done = np.abs(gn - g).max() < tol
        g = gn
        if done:
            break
    mu = X @ g
    w = L * np.exp(-0.5 * (W.Q[None, :] - mu[:, None]) ** 2 / s2[:, None])
    w /= w.sum(1, keepdims=True)
    return w, g, s2


def onehot(idx, k, drop_first=False):
    m = np.eye(k)[idx]
    return m[:, 1:] if drop_first else m


def X_of(c, kind, mask):
    """Design matrices: c holds per-student arrays g (0..2), band (0..4), ed, el, iep, dist (0..D-1), state (0..5)."""
    g = onehot(c["g"][mask], 3); gd = g[:, 1:]
    band = onehot(c["band"][mask], 5, drop_first=True)
    bg = np.column_stack([c["ed"][mask], c["el"][mask], c["iep"][mask]]).astype(float)
    dist = onehot(c["dist"][mask], c["D"])
    st = onehot(c["state"][mask], 6, drop_first=True)
    if kind == "vendor":
        return np.column_stack([g, st, band, bg])
    if kind == "gold":
        return np.column_stack([dist, gd, band, bg])
    if kind == "dist_grade":
        return np.column_stack([dist, gd])
    if kind == "dist_x_grade":
        return onehot(c["dist"][mask] * 3 + c["g"][mask], c["D"] * 3)
    if kind == "dist_only":
        return dist
    if kind == "uncond":
        return np.ones((mask.sum(), 1))
    raise KeyError(kind)


def above(g):
    return (W.Q[None, :] > W.CUT_THETA[g][:, None]).astype(float)


def share_post(dist, g, w, D):
    """Per cent of each district's students at or above the cut, as the mean posterior probability."""
    p = (w * above(g)).sum(1)
    return 100 * np.bincount(dist, p, minlength=D) / np.bincount(dist, minlength=D)


def draw_pv(w, seed, m=5):
    """m plausible values per student from posterior weights on the grid, continuous within each grid cell."""
    r = np.random.default_rng(seed)
    cdf = np.cumsum(w, 1)
    out = []
    for _ in range(m):
        u = r.random(len(w))[:, None]
        k = np.minimum((cdf < u).sum(1), len(W.Q) - 1)
        out.append(W.Q[k] + r.uniform(-0.025, 0.025, len(w)))
    return np.array(out)                       # m x n theta values


def to_scale(theta):
    return np.round(W.SCALE_A + W.SCALE_B * theta, 1)


def share_pv_scale(dist, g, pv_scale, D):
    """Per cent at or above Proficient from scale-score plausible values, averaged over the draws."""
    cut = np.array(W.CUT_SCALE)[g]
    vals = [100 * np.bincount(dist, (p >= cut - 1e-9).astype(float), minlength=D) / np.bincount(dist, minlength=D)
            for p in pv_scale]
    return np.mean(vals, 0)


def share_point(dist, g, est, D):
    return 100 * np.bincount(dist, (est >= W.CUT_THETA[g] - 1e-9).astype(float), minlength=D) / \
        np.bincount(dist, minlength=D)


def tcc_theta(y, mods, admin):
    """Each student's theta from the test characteristic curve of the items they were administered, at their number
    correct."""
    raw = (y * admin).sum((1, 2))
    out = np.empty(len(raw))
    keys = {}
    for i in range(len(raw)):
        keys.setdefault((mods[i, 0], mods[i, 1], admin[i].tobytes()), []).append(i)
    for (m1, m2, ab), idx in keys.items():
        ad = np.frombuffer(ab, dtype=admin.dtype).reshape(2, W.N_ITEM).astype(bool)
        aa = np.concatenate([W.A[m1][ad[0]], W.A[m2][ad[1]]]); bb = np.concatenate([W.B[m1][ad[0]], W.B[m2][ad[1]]])
        tcc = (1 / (1 + np.exp(-aa[None, :] * (W.Q[:, None] - bb[None, :])))).sum(1)
        out[idx] = np.interp(raw[idx], tcc, W.Q)
    return out
