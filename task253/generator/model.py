"""The analysis standard's random-effects model and every count built on it.

Students within year groups (one year level at one sitting) within schools, a fixed overall mean, fitted by
restricted maximum likelihood on the student-level data. The student-level likelihood factorises into the
within-year-group sums of squares (the student variance alone) and the year-group means, so the fit runs on
the year-group means and sizes plus the pooled within-group sum of squares, which is exact.
"""
import math

import numpy as np

SQ2 = math.sqrt(2.0)
_erf = np.vectorize(math.erf)


def phi(z):
    return 0.5 * (1.0 + _erf(np.asarray(z, dtype=float) / SQ2))


def stats(frame):
    """frame: columns school (0..S-1), sitting (0..T-1), score. Returns n[S,T], ybar[S,T], SSW, N."""
    s = frame["school"].to_numpy()
    t = frame["sitting"].to_numpy()
    y = frame["score"].to_numpy(dtype=float)
    S, T = s.max() + 1, t.max() + 1
    n = np.zeros((S, T))
    sm = np.zeros((S, T))
    sq = np.zeros((S, T))
    np.add.at(n, (s, t), 1.0)
    np.add.at(sm, (s, t), y)
    ybar = sm / n
    np.add.at(sq, (s, t), (y - ybar[s, t]) ** 2)
    return n, ybar, float(sq.sum()), float(n.sum()), sq


# ------------------------------------------------------------------------------------------------ likelihood
def _blocks(n, tu, tv, s2):
    """Per-school inverse covariance of the year-group means: V = tu J + diag(tv + s2/n)."""
    d = tv + s2 / n                       # S x T
    w = 1.0 / d
    W = w.sum(1)
    # Sherman-Morrison: V^-1 = D^-1 - (tu D^-1 1 1' D^-1)/(1 + tu W)
    c = tu / (1.0 + tu * W)
    logdet = np.log(d).sum(1) + np.log1p(tu * W)
    return d, w, W, c, logdet


def _vinv_apply(w, c, a):
    """V^-1 a for a of shape S x T (x k)."""
    if a.ndim == 2:
        return w * a - (c * (w * a).sum(1))[:, None] * w
    wa = w[:, :, None] * a
    return wa - c[:, None, None] * wa.sum(1)[:, None, :] * w[:, :, None]


def design(S, T, kind):
    if kind == "mean":
        return np.ones((S, T, 1))
    X = np.zeros((S, T, T))
    for j in range(T):
        X[:, j, j] = 1.0
    return X


def loglik(params, n, ybar, SSW, N, X, reml=True, s2_fixed=None):
    tu, tv = params[0], params[1]
    s2 = params[2] if s2_fixed is None else None
    G = n.size
    if s2_fixed is None:
        within = (N - G) * math.log(s2) + SSW / s2
        sn = s2 / n
    else:
        within = 0.0
        sn = s2_fixed
    d = tv + sn
    w = 1.0 / d
    W = w.sum(1)
    c = tu / (1.0 + tu * W)
    logdet = np.log(d).sum(1) + np.log1p(tu * W)
    ViX = _vinv_apply(w, c, X)
    XtViX = np.einsum("stk,stl->kl", X, ViX)
    Xty = np.einsum("stk,st->k", ViX, ybar)
    beta = np.linalg.solve(XtViX, Xty)
    r = ybar - np.einsum("stk,k->st", X, beta)
    q = float((r * _vinv_apply(w, c, r)).sum())
    ll = within + logdet.sum() + q
    if reml:
        ll += math.log(np.linalg.det(XtViX))
    return -0.5 * ll, beta, XtViX


def _nelder_mead(f, x0, step=0.3, tol=1e-12, maxit=20000):
    k = len(x0)
    pts = [np.array(x0, float)]
    for i in range(k):
        p = np.array(x0, float)
        p[i] += step
        pts.append(p)
    vals = [f(p) for p in pts]
    for _ in range(maxit):
        order = np.argsort(vals)
        pts = [pts[i] for i in order]
        vals = [vals[i] for i in order]
        if abs(vals[-1] - vals[0]) < tol and np.max(np.abs(np.array(pts) - pts[0])) < 1e-9:
            break
        cen = np.mean(pts[:-1], axis=0)
        xr = cen + (cen - pts[-1])
        fr = f(xr)
        if fr < vals[0]:
            xe = cen + 2 * (cen - pts[-1])
            fe = f(xe)
            pts[-1], vals[-1] = (xe, fe) if fe < fr else (xr, fr)
        elif fr < vals[-2]:
            pts[-1], vals[-1] = xr, fr
        else:
            xc = cen + 0.5 * (pts[-1] - cen)
            fc = f(xc)
            if fc < vals[-1]:
                pts[-1], vals[-1] = xc, fc
            else:
                for i in range(1, k + 1):
                    pts[i] = pts[0] + 0.5 * (pts[i] - pts[0])
                    vals[i] = f(pts[i])
    i = int(np.argmin(vals))
    return pts[i], vals[i]


def fit(n, ybar, SSW, N, kind="mean", reml=True, s2_fixed=None, start=None):
    """Variance components by (restricted) maximum likelihood. Returns dict."""
    S, T = n.shape
    X = design(S, T, kind)
    if s2_fixed is None:
        s2_0 = SSW / (N - n.size)
        x0 = np.log(start if start is not None else [250.0, 100.0, s2_0])

        def f(lx):
            return -loglik(np.exp(lx), n, ybar, SSW, N, X, reml)[0]
    else:
        x0 = np.log(start if start is not None else [250.0, 100.0])

        def f(lx):
            return -loglik(np.exp(lx), n, ybar, SSW, N, X, reml, s2_fixed=s2_fixed)[0]
    x, v = _nelder_mead(f, x0)
    x, v = _nelder_mead(f, x, step=0.01)
    p = np.exp(x)
    ll, beta, XtViX = loglik(p, n, ybar, SSW, N, X, reml, s2_fixed=s2_fixed)
    out = {"tu": float(p[0]), "tv": float(p[1]), "s2": float(p[2]) if s2_fixed is None else None,
           "beta": beta, "cov_beta": np.linalg.inv(XtViX), "ll": ll, "kind": kind}
    return out


# ------------------------------------------------------------------------------------------------ posteriors
def school_posterior(n, ybar, tu, tv, s2, mu, var_mu=0.0, sn=None):
    """Each school's underlying average (mean + school effect): normal mean and variance given its
    year-group means. mu may be a scalar or an S x T array (a fixed effect per sitting, the underlying
    average then taken on the sittings' mean scale)."""
    if sn is None:
        sn = s2 / n
    w = 1.0 / (tv + sn)
    W = w.sum(1)
    P = 1.0 / tu + W
    mu_arr = np.broadcast_to(np.asarray(mu, float), n.shape) if np.ndim(mu) else np.full(n.shape, float(mu))
    base = mu_arr.mean(1)
    dev = (w * (ybar - mu_arr)).sum(1) / P
    mean = base + dev
    k = 1.0 - W / P
    var = 1.0 / P + (k ** 2) * var_mu
    return mean, var


def prob_below(mean, var, floor=480.0):
    return phi((floor - mean) / np.sqrt(var))


def poisson_binomial(p):
    dist = np.zeros(len(p) + 1)
    dist[0] = 1.0
    for q in p:
        dist[1:] = dist[1:] * (1 - q) + dist[:-1] * q
        dist[0] *= (1 - q)
    return dist


def median_mode(p):
    d = poisson_binomial(p)
    cdf = np.cumsum(d)
    return int(np.searchsorted(cdf, 0.5)), int(np.argmax(d))


# ------------------------------------------------------------------------------------------------ the family
def golden_probs(n, ybar, SSW, N):
    f = fit(n, ybar, SSW, N)
    mean, var = school_posterior(n, ybar, f["tu"], f["tv"], f["s2"], f["beta"][0])
    return f, mean, var, prob_below(mean, var)


def integrated_probs(n, ybar, SSW, N, f, grid=41, span=4.0):
    """The components' own uncertainty integrated over (flat priors on the variances, the restricted
    likelihood as the posterior, the mean integrated with a flat prior). The student variance is held at
    its estimate (its relative standard error is under one per cent)."""
    S, T = n.shape
    X = design(S, T, "mean")
    s2 = f["s2"]
    # curvature in log space for the grid's extent
    lt = np.log([f["tu"], f["tv"]])

    def ll(a, b):
        return loglik([math.exp(a), math.exp(b), s2], n, ybar, SSW, N, X, True)[0]
    h = 1e-3
    l0 = ll(*lt)
    saa = -(ll(lt[0] + h, lt[1]) - 2 * l0 + ll(lt[0] - h, lt[1])) / h ** 2
    sbb = -(ll(lt[0], lt[1] + h) - 2 * l0 + ll(lt[0], lt[1] - h)) / h ** 2
    sa, sb = span / math.sqrt(saa), span / math.sqrt(sbb)
    A = lt[0] + np.linspace(-sa, sa, grid)
    B = lt[1] + np.linspace(-sb, sb, grid)
    logw, sums, probs = [], [], []
    for a in A:
        for b in B:
            v, beta, XtViX = loglik([math.exp(a), math.exp(b), s2], n, ybar, SSW, N, X, True)
            mean, var = school_posterior(n, ybar, math.exp(a), math.exp(b), s2, beta[0],
                                         var_mu=1.0 / XtViX[0, 0])
            p = prob_below(mean, var)
            logw.append(v + a + b)          # flat prior on the variances: Jacobian of the log grid
            probs.append(p)
    logw = np.array(logw)
    wts = np.exp(logw - logw.max())
    wts /= wts.sum()
    P = np.tensordot(wts, np.array(probs), axes=1)
    return P


def family(n, ybar, SSW, N, sq):
    """Every golden-family variant of each school's probability."""
    out = {}
    f, mean, var, p = golden_probs(n, ybar, SSW, N)
    out["reml"] = p
    fm = fit(n, ybar, SSW, N, reml=False, start=[f["tu"], f["tv"], f["s2"]])
    m2, v2 = school_posterior(n, ybar, fm["tu"], fm["tv"], fm["s2"], fm["beta"][0])
    out["ml"] = prob_below(m2, v2)
    m3, v3 = school_posterior(n, ybar, f["tu"], f["tv"], f["s2"], f["beta"][0], var_mu=f["cov_beta"][0, 0])
    out["mean_unc"] = prob_below(m3, v3)
    fs = fit(n, ybar, SSW, N, kind="sitting", start=[f["tu"], f["tv"], f["s2"]])
    mu_t = np.broadcast_to(fs["beta"], n.shape)
    m4, v4 = school_posterior(n, ybar, fs["tu"], fs["tv"], fs["s2"], mu_t)
    out["sitting"] = prob_below(m4, v4)
    # a residual variance per school: each school's own pooled within-group variance
    df_s = (n - 1).sum(1)
    s2_school = sq.sum(1) / df_s
    sn = s2_school[:, None] / n
    fr = fit(n, ybar, SSW, N, s2_fixed=sn, start=[f["tu"], f["tv"]])
    m5, v5 = school_posterior(n, ybar, fr["tu"], fr["tv"], None, fr["beta"][0], sn=sn)
    out["school_s2"] = prob_below(m5, v5)
    out["integrated"] = integrated_probs(n, ybar, SSW, N, f)
    return f, mean, var, out, fm, fs


def population_share(f, S, floor=480.0):
    return float(S * phi((floor - f["beta"][0]) / math.sqrt(f["tu"])))


def two_level(nn, yb, SSW, N):
    """The school level only (the sittings pooled): ybar_i = mu + u_i + e_i, REML over (tu, s2). Returns
    the components and each school's normal mean and variance."""
    nn = np.asarray(nn, float)
    yb = np.asarray(yb, float)
    G = len(nn)

    def nll(lx):
        tu, s2 = np.exp(lx)
        d = tu + s2 / nn
        w = 1 / d
        mu = (w * yb).sum() / w.sum()
        q = (w * (yb - mu) ** 2).sum()
        return 0.5 * ((N - G) * math.log(s2) + SSW / s2 + np.log(d).sum() + q + math.log(w.sum()))
    x, _ = _nelder_mead(nll, np.log([300.0, SSW / (N - G)]))
    x, _ = _nelder_mead(nll, x, step=0.01)
    tu, s2 = np.exp(x)
    w = 1 / (tu + s2 / nn)
    mu = (w * yb).sum() / w.sum()
    P = 1 / tu + nn / s2
    m = mu + (nn / s2) * (yb - mu) / P
    return {"tu": float(tu), "s2": float(s2), "mu": float(mu)}, m, 1 / P
