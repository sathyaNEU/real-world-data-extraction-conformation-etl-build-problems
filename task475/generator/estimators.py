"""The estimators a competent analyst could use for a question's difficulty on a paper with optional questions, as
pure functions of a candidates x questions mark matrix (NaN where a question was not answered). Every function
returns the moves: marks added to each question, how much harder it proved than the average question counted once.

    facility      each question's mean mark among those who answered it, against the mean of those means
    fe            two-way additive fit (candidate + question), solved by alternating means; the golden
    fe_ols        the same fit by least squares on question dummies with candidates absorbed
    diff_simple   each question's answerers: mark on it less their mean on their other answers (one step)
    ancova        facility adjusted by regressing the mark on the answerers' mean on their other answers
    random_int    random-intercept model for candidates, variance components by moments, GLS for questions
    logit_fe      the additive fit on the logit of the mark, carried back to expected marks over every candidate
    pairwise      each pair of questions compared on the candidates who answered both, reconciled by least squares
"""
import numpy as np


def _rows(m):
    """Candidates with at least one answer (a script not yet marked carries none)."""
    m = np.asarray(m, float)
    return m[~np.all(np.isnan(m), axis=1)]


def facility(m):
    m = _rows(m)
    f = np.nanmean(m, axis=0)
    return f.mean() - f


def fe(m, tol=1e-12, iters=5000):
    m = _rows(m)
    a = np.nanmean(m, axis=1)
    d = np.zeros(m.shape[1])
    for _ in range(iters):
        dn = np.nanmean(m - a[:, None], axis=0)
        dn = dn - dn.mean()
        an = np.nanmean(m - dn[None, :], axis=1)
        done = np.max(np.abs(dn - d)) < tol and np.max(np.abs(an - a)) < tol
        d, a = dn, an
        if done:
            break
    return -d


def fe_ols(m):
    m = _rows(m)
    n, q = m.shape
    rows, cols = np.where(~np.isnan(m))
    y = m[rows, cols]
    X = np.zeros((len(y), q))
    X[np.arange(len(y)), cols] = 1.0
    Xd, yd = X.copy(), y.copy()
    for i in np.unique(rows):
        k = rows == i
        Xd[k] -= Xd[k].mean(0)
        yd[k] -= yd[k].mean()
    C = np.zeros((q, q - 1))
    C[:q - 1] = np.eye(q - 1)
    C[q - 1] = -1.0
    beta = np.linalg.lstsq(Xd @ C, yd, rcond=None)[0]
    return -(C @ beta)


def diff_simple(m):
    m = _rows(m)
    q = m.shape[1]
    out = []
    for j in range(q):
        s = ~np.isnan(m[:, j])
        oth = m[s].copy()
        oth[:, j] = np.nan
        out.append(np.nanmean(m[s, j] - np.nanmean(oth, axis=1)))
    out = np.array(out)
    return out.mean() - out


def ancova(m):
    m = _rows(m)
    q = m.shape[1]
    out = []
    for j in range(q):
        allo = m.copy()
        allo[:, j] = np.nan
        xall = np.nanmean(allo, axis=1)
        s = ~np.isnan(m[:, j])
        x, y = xall[s], m[s, j]
        ok = ~np.isnan(x)
        sl = np.polyfit(x[ok], y[ok], 1)[0]
        out.append(y.mean() - sl * (np.nanmean(x) - np.nanmean(xall)))
    out = np.array(out)
    return out.mean() - out


def random_int(m):
    m = _rows(m)
    n, q = m.shape
    obs = ~np.isnan(m)
    rows, cols = np.where(obs)
    y = m[rows, cols]
    T = obs.sum(1)
    d = -fe(m)
    a = np.nanmean(m - d[None, :], axis=1)
    res = y - a[rows] - d[cols]
    s2e = (res ** 2).sum() / (len(y) - n - q + 1)
    s2a = max(np.var(a) - s2e / T.mean(), 1e-6)
    lam = 1.0 - np.sqrt(s2e / (s2e + T * s2a))
    X = np.zeros((len(y), q))
    X[np.arange(len(y)), cols] = 1.0
    Xs, ys = X.copy(), y.copy()
    for i in range(n):
        k = rows == i
        if not k.any():
            continue
        Xs[k] -= lam[i] * X[k].mean(0)
        ys[k] -= lam[i] * y[k].mean()
    ones = 1.0 - lam[rows]
    C = np.zeros((q, q - 1))
    C[:q - 1] = np.eye(q - 1)
    C[q - 1] = -1.0
    D = np.column_stack([ones, Xs @ C])
    beta = np.linalg.lstsq(D, ys, rcond=None)[0]
    return -(C @ beta[1:])


def logit_fe(m, top=20.0):
    m = _rows(m)
    z = np.log((m + 0.5) / (top + 0.5 - m))
    e = -fe(z)
    a = np.nanmean(z - e[None, :], axis=1)
    E = np.array([np.mean((top + 1.0) / (1.0 + np.exp(-(a + e[j]))) - 0.5) for j in range(m.shape[1])])
    return E.mean() - E


def pairwise(m):
    """Each pair of questions compared on the candidates who answered both, the pair differences reconciled by least
    squares (each pair weighted by its candidates), each question against the average question."""
    m = _rows(m)
    q = m.shape[1]
    rows, ys, ws = [], [], []
    for a in range(q):
        for b in range(a + 1, q):
            both = ~np.isnan(m[:, a]) & ~np.isnan(m[:, b])
            k = int(both.sum())
            if k == 0:
                continue
            r = np.zeros(q)
            r[a], r[b] = 1.0, -1.0
            rows.append(r)
            ys.append(float(np.mean(m[both, a] - m[both, b])))
            ws.append(np.sqrt(k))
    X = np.array(rows) * np.array(ws)[:, None]
    y = np.array(ys) * np.array(ws)
    C = np.zeros((q, q - 1))
    C[:q - 1] = np.eye(q - 1)
    C[q - 1] = -1.0
    e = C @ np.linalg.lstsq(X @ C, y, rcond=None)[0]
    return -(e - e.mean())


FAMILY = {"fe": fe, "fe_ols": fe_ols, "diff_simple": diff_simple, "ancova": ancova, "random_int": random_int,
          "logit_fe": logit_fe, "pairwise": pairwise}


def edge(v):
    """Distance of each value from the nearest rounding line (x.5)."""
    v = np.asarray(v, float)
    return 0.5 - np.abs(v - np.rint(v))


def apply_moves(m, moves, top=20):
    mv = np.rint(np.asarray(moves, float))
    out = np.where(np.isnan(m), np.nan, np.clip(m + mv[None, :], 0, top))
    return out


def passes(m, moves, mark=50, top=20):
    tot = np.nansum(apply_moves(m, moves, top), axis=1)
    return int((tot >= mark).sum())
