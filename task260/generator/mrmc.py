"""Multi-reader multi-case ROC statistics for a fully crossed reader study with two conditions (unaided, aided).

Ratings R have shape (2, J, K): condition, reader, case; truth (K,) is 1 for a cancer and 0 for a normal. A reader's
accuracy in a condition is the area under the empirical ROC curve (Mann-Whitney, ties counted half). The gain is the
readers' average aided area minus their average unaided area. Intervals:

    or_test        Obuchowski-Rockette, readers and cases random (Hillis's degrees of freedom), with any covariance
    dbm            Dorfman-Berbaum-Metz on jackknife pseudovalues, readers and cases random (Hillis)
    fixed_readers  cases random, the panel fixed (DeLong or jackknife covariance of the readers' average)
    paired_t       readers random, the cases fixed (each reader's own gain, t across readers)
    boot           percentile bootstrap over cases, readers or both
    pooled         one ROC curve per condition over every reading, DeLong as if readings were independent cases"""
from __future__ import annotations

import numpy as np
from scipy import stats


def psi(pos, neg):
    d = pos[:, None] - neg[None, :]
    return (d > 0) + 0.5 * (d == 0)


def kernels(R, truth):
    """D[i, j] = the m x n matrix of psi(cancer rating, normal rating) for condition i and reader j."""
    pos, neg = truth == 1, truth == 0
    I, J, _ = R.shape
    D = np.empty((I, J, int(pos.sum()), int(neg.sum())))
    for i in range(I):
        for j in range(J):
            D[i, j] = psi(R[i, j, pos], R[i, j, neg])
    return D


def aucs(D):
    return D.mean(axis=(2, 3))


def delong_cov(D):
    """DeLong's covariance of the I*J areas (row-major: condition, then reader)."""
    I, J, m, n = D.shape
    V10 = D.mean(3).reshape(I * J, m)
    V01 = D.mean(2).reshape(I * J, n)
    return np.cov(V10) / m + np.cov(V01) / n


def jackknife(D):
    """Leave-one-case-out areas (I*J, K): the m cancers first, then the n normals."""
    I, J, m, n = D.shape
    flat = D.reshape(I * J, m, n)
    tot = flat.sum((1, 2))
    rows, cols = flat.sum(2), flat.sum(1)
    return np.concatenate([(tot[:, None] - rows) / ((m - 1) * n), (tot[:, None] - cols) / (m * (n - 1))], axis=1)


def jackknife_cov(D):
    th = jackknife(D)
    K = th.shape[1]
    c = th - th.mean(1, keepdims=True)
    return (K - 1) / K * (c @ c.T)


def or_components(C, I, J):
    C4 = C.reshape(I, J, I, J)
    var = np.mean([C4[i, j, i, j] for i in range(I) for j in range(J)])
    cov1 = np.mean([C4[i, j, k, j] for i in range(I) for k in range(I) if k != i for j in range(J)])
    cov2 = np.mean([C4[i, j, i, l] for i in range(I) for j in range(J) for l in range(J) if l != j])
    cov3 = np.mean([C4[i, j, k, l] for i in range(I) for k in range(I) if k != i for j in range(J) for l in range(J)
                    if l != j])
    return var, cov1, cov2, cov3


def or_test(A, C, level=0.95, normal=False, reader_fpc=None):
    """Obuchowski-Rockette for two conditions, readers and cases random, Hillis's denominator degrees of freedom.
    reader_fpc: (panel size, population size) to scale the reader term by a finite-population correction."""
    I, J = A.shape
    var, cov1, cov2, cov3 = or_components(C, I, J)
    mi, mj, mm = A.mean(1), A.mean(0), A.mean()
    ms_tr = ((A - mi[:, None] - mj[None, :] + mm) ** 2).sum() / ((I - 1) * (J - 1))
    case_term = J * max(cov2 - cov3, 0.0)
    reader_term = ms_tr
    if reader_fpc is not None:
        n_, N_ = reader_fpc
        # MS(T*R) carries the reader-by-condition variance plus the error part; correct only the former
        err = var - cov1 - cov2 + cov3
        sig_tr = max(ms_tr - err, 0.0)
        reader_term = sig_tr * (1 - n_ / N_) + err
    den = reader_term + case_term
    df = den ** 2 / (ms_tr ** 2 / ((I - 1) * (J - 1))) if ms_tr > 0 else np.inf
    diff = mi[1] - mi[0]
    se = np.sqrt(2.0 / J * den)
    q = (1 + level) / 2
    crit = stats.norm.ppf(q) if normal else stats.t.ppf(q, df)
    p = 2 * (stats.norm.sf(abs(diff) / se) if normal else stats.t.sf(abs(diff) / se, df))
    return dict(diff=diff, se=se, df=df, lo=diff - crit * se, hi=diff + crit * se, crit=crit, p=p, ms_tr=ms_tr,
                var=var, cov1=cov1, cov2=cov2, cov3=cov3, z=diff / se)


def dbm(D, level=0.95):
    """DBM on jackknife pseudovalues, treatment fixed, readers and cases random (Hillis 2007 denominator)."""
    I, J, m, n = D.shape
    K = m + n
    theta = aucs(D).reshape(I * J, 1)
    Y = (K * theta - (K - 1) * jackknife(D)).reshape(I, J, K)
    g = Y.mean()
    yi, yj, yk = Y.mean((1, 2)), Y.mean((0, 2)), Y.mean((0, 1))
    yij, yik, yjk = Y.mean(2), Y.mean(1), Y.mean(0)
    ms_tr = K * ((yij - yi[:, None] - yj[None, :] + g) ** 2).sum() / ((I - 1) * (J - 1))
    ms_tc = J * ((yik - yi[:, None] - yk[None, :] + g) ** 2).sum() / ((I - 1) * (K - 1))
    res = Y - yij[:, :, None] - yik[:, None, :] - yjk[None, :, :] + yi[:, None, None] + yj[None, :, None] \
        + yk[None, None, :] - g
    ms_trc = (res ** 2).sum() / ((I - 1) * (J - 1) * (K - 1))
    den = ms_tr + max(ms_tc - ms_trc, 0.0)
    df = den ** 2 / (ms_tr ** 2 / ((I - 1) * (J - 1)))
    A = aucs(D)
    diff = A[1].mean() - A[0].mean()
    se = np.sqrt(2.0 / (J * K) * den)
    crit = stats.t.ppf((1 + level) / 2, df)
    return dict(diff=diff, se=se, df=df, lo=diff - crit * se, hi=diff + crit * se, z=diff / se)


def fixed_readers(A, C, level=0.95):
    I, J = A.shape
    w = np.concatenate([-np.ones(J), np.ones(J)]) / J
    se = float(np.sqrt(w @ C @ w))
    diff = A[1].mean() - A[0].mean()
    crit = stats.norm.ppf((1 + level) / 2)
    return dict(diff=diff, se=se, lo=diff - crit * se, hi=diff + crit * se, z=diff / se)


def paired_t(A, level=0.95):
    d = A[1] - A[0]
    J = len(d)
    se = d.std(ddof=1) / np.sqrt(J)
    crit = stats.t.ppf((1 + level) / 2, J - 1)
    return dict(diff=d.mean(), se=se, df=J - 1, lo=d.mean() - crit * se, hi=d.mean() + crit * se, crit=crit,
                z=d.mean() / se, p=2 * stats.t.sf(abs(d.mean()) / se, J - 1))


def signed_rank_p(A):
    return float(stats.wilcoxon(A[1] - A[0]).pvalue)


def boot(D, reps=2000, seed=0, readers=True, cases=True, level=0.95, chunk=250, wts=None):
    """Percentile interval of the gain; cancers and normals are resampled separately. wts: optional reader weights
    (the gain is then the weighted mean of the readers' changes)."""
    I, J, m, n = D.shape
    rng = np.random.default_rng(seed)
    out = []
    left = reps
    while left > 0:
        b = min(chunk, left)
        left -= b
        wp = np.stack([np.bincount(rng.integers(0, m, m), minlength=m) for _ in range(b)]).astype(float) \
            if cases else np.ones((b, m))
        wn = np.stack([np.bincount(rng.integers(0, n, n), minlength=n) for _ in range(b)]).astype(float) \
            if cases else np.ones((b, n))
        W = np.stack([np.bincount(rng.integers(0, J, J), minlength=J) for _ in range(b)]).astype(float) \
            if readers else np.ones((b, J))
        T = np.einsum("ijmn,bn->bijm", D, wn, optimize=True)
        Ab = np.einsum("bijm,bm->bij", T, wp, optimize=True) / (m * n)
        if wts is None:
            out.append(((Ab[:, 1] - Ab[:, 0]) * W).sum(1) / J)
        else:
            Ww = W * np.asarray(wts)[None, :]
            out.append(((Ab[:, 1] - Ab[:, 0]) * Ww).sum(1) / Ww.sum(1))
    g = np.concatenate(out)
    a = (1 - level) / 2
    lo, hi = np.percentile(g, [100 * a, 100 * (1 - a)])
    return dict(lo=float(lo), hi=float(hi), sd=float(g.std(ddof=1)))


def pooled(R, truth, level=0.95):
    """Every reader's readings of a condition pooled into one ROC curve; DeLong's paired test on the pooled areas as
    though each reading were its own case."""
    pos, neg = truth == 1, truth == 0
    P = [R[i][:, pos].ravel() for i in range(2)]
    N = [R[i][:, neg].ravel() for i in range(2)]
    D2 = np.stack([psi(P[i], N[i]) for i in range(2)])
    a = D2.mean((1, 2))
    V10, V01 = D2.mean(2), D2.mean(1)
    C = np.cov(V10) / V10.shape[1] + np.cov(V01) / V01.shape[1]
    se = float(np.sqrt(C[0, 0] + C[1, 1] - 2 * C[0, 1]))
    diff = a[1] - a[0]
    crit = stats.norm.ppf((1 + level) / 2)
    return dict(auc=a, diff=diff, se=se, lo=diff - crit * se, hi=diff + crit * se)


def summary(R, truth, reps=2000, seed=0):
    """Every interval the ladder and the convergence checks use, for one study."""
    D = kernels(R, truth)
    A = aucs(D)
    Cd, Cj = delong_cov(D), jackknife_cov(D)
    return dict(A=A, D=D, gain=A[1].mean() - A[0].mean(), or_jk=or_test(A, Cj), or_dl=or_test(A, Cd), dbm=dbm(D),
                fixed_dl=fixed_readers(A, Cd), fixed_jk=fixed_readers(A, Cj), paired=paired_t(A))
