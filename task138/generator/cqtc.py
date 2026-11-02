"""Concentration-QTc machinery shared by the golden analysis and the ladder: heart-rate exponents from drug-free
Holter segments, corrected QT, the pre-specified linear mixed-effects model (REML) and its prediction."""
import numpy as np
from scipy import optimize, stats

TIMES = [0.5, 1, 2, 3, 4, 6, 8, 12, 24]


# ---------------------------------------------------------------- heart-rate exponents
def _within(x, y, groups):
    x = x.astype(float).copy()
    y = y.astype(float).copy()
    for g in np.unique(groups):
        m = groups == g
        x[m] -= x[m].mean()
        y[m] -= y[m].mean()
    return float((x @ y) / (x @ x))


def exponent(lrr, lqt, clock, method):
    """One subject's QT-RR exponent from his drug-free segments (log RR, log QT, local clock hour)."""
    if method == "pooled":                      # every segment, one line (the textbook QTcI fit)
        return _within(lrr, lqt, np.zeros(len(lrr)))
    if method == "hour":                        # within each clock hour
        return _within(lrr, lqt, np.floor(clock).astype(int))
    if method == "half_hour":
        return _within(lrr, lqt, np.floor(clock * 2).astype(int))
    if method == "two_hour":
        return _within(lrr, lqt, np.floor(clock / 2).astype(int))
    if method == "three_hour":
        return _within(lrr, lqt, np.floor(clock / 3).astype(int))
    if method in ("harmonic1", "harmonic2", "harmonic3"):
        k = int(method[-1])
        cols = [np.ones(len(lrr)), lrr]
        for j in range(1, k + 1):
            cols += [np.cos(2 * np.pi * j * clock / 24), np.sin(2 * np.pi * j * clock / 24)]
        A = np.column_stack(cols)
        return float(np.linalg.lstsq(A, lqt, rcond=None)[0][1])
    if method == "day_only":                    # waking day only, one line
        m = (clock >= 8) & (clock < 22)
        return _within(lrr[m], lqt[m], np.zeros(m.sum()))
    if method == "day_night":                   # day and night levels apart
        return _within(lrr, lqt, ((clock >= 8) & (clock < 22)).astype(int))
    if method == "linear_pooled":               # QT = a + b RR, as the exponent at the subject's mean RR
        rr = np.exp(lrr) / 1000.0
        qt = np.exp(lqt)
        b = _within(rr, qt, np.zeros(len(rr)))
        return float(b * rr.mean() / qt.mean())
    if method == "linear_hour":
        rr = np.exp(lrr) / 1000.0
        qt = np.exp(lqt)
        b = _within(rr, qt, np.floor(clock).astype(int))
        return float(b * rr.mean() / qt.mean())
    if method in ("four_hour", "six_hour", "eight_hour"):
        w = {"four_hour": 4, "six_hour": 6, "eight_hour": 8}[method]
        return _within(lrr, lqt, np.floor(clock / w).astype(int))
    if method == "stable":                      # steady-rate segments only, one line
        d = np.abs(np.diff(lrr, prepend=lrr[0]))
        m = d < 0.02
        return _within(lrr[m], lqt[m], np.zeros(m.sum()))
    raise ValueError(method)


# ---------------------------------------------------------------- corrections
def corrected(qt, rr, scheme, b=None):
    """qt, rr in ms; scheme: 'own' (power with exponent b), 'F', 'B', 'Fram', 'Hodges', 'power' (fixed b)."""
    rr_s = rr / 1000.0
    if scheme in ("own", "power"):
        return qt / rr_s ** b
    if scheme == "F":
        return qt / rr_s ** (1 / 3)
    if scheme == "B":
        return qt / rr_s ** 0.5
    if scheme == "Fram":
        return qt + 154.0 * (1 - rr_s)
    if scheme == "Hodges":
        return qt + 1.75 * (60000.0 / rr - 60)
    if scheme == "raw":
        return qt
    raise ValueError(scheme)


# ---------------------------------------------------------------- REML mixed model
def lme_reml(y, X, Z, groups):
    ug = list(dict.fromkeys(groups.tolist()))
    idx = [np.where(groups == g)[0] for g in ug]
    q = Z.shape[1]
    n, p = X.shape

    def unpack(th):
        L = np.zeros((q, q))
        k = 0
        for i in range(q):
            for j in range(i + 1):
                L[i, j] = th[k]
                k += 1
        return L @ L.T

    def parts(th):
        G = unpack(th)
        XtVX = np.zeros((p, p))
        XtVy = np.zeros(p)
        logdet = 0.0
        Vinvs = []
        for ii in idx:
            Zi = Z[ii]
            Vi = Zi @ G @ Zi.T + np.eye(len(ii))
            ch = np.linalg.cholesky(Vi)
            Vinv = np.linalg.inv(Vi)
            Vinvs.append(Vinv)
            logdet += 2 * np.log(np.diag(ch)).sum()
            XtVX += X[ii].T @ Vinv @ X[ii]
            XtVy += X[ii].T @ Vinv @ y[ii]
        b = np.linalg.solve(XtVX, XtVy)
        rss = sum(float((y[ii] - X[ii] @ b) @ Vinv @ (y[ii] - X[ii] @ b)) for ii, Vinv in zip(idx, Vinvs))
        s2 = rss / (n - p)
        ll = -0.5 * ((n - p) * np.log(s2) + logdet + np.linalg.slogdet(XtVX)[1])
        return ll, b, s2 * np.linalg.inv(XtVX), s2 * G, s2

    nth = q * (q + 1) // 2
    th0 = np.zeros(nth)
    k = 0
    for i in range(q):
        for j in range(i + 1):
            th0[k] = 1.0 if i == j else 0.0
            k += 1
    best = None
    for start in (th0, th0 * 0.3, th0 * 3.0):
        res = optimize.minimize(lambda th: -parts(th)[0], start, method="Nelder-Mead",
                                options={"maxiter": 6000, "xatol": 1e-7, "fatol": 1e-9})
        if best is None or res.fun < best.fun - 1e-9:
            best = res
    ll, b, cov, G, s2 = parts(best.x)
    return dict(b=b, cov=cov, G=G, s2=s2, ll=ll)


def design(rows, base, slope=True, times=TIMES, baseline_cov=True):
    """rows: dicts with subject, trt, conc, nominal, dq. base: subject -> baseline QTc."""
    subjects = sorted({r["subject"] for r in rows})
    mb = np.mean([base[s] for s in subjects])
    Y, Xr, Zr, G = [], [], [], []
    for r in rows:
        x = [1.0, float(r["trt"]), float(r["conc"])] + [1.0 if r["nominal"] == t else 0.0 for t in times[1:]]
        if baseline_cov:
            x.append(base[r["subject"]] - mb)
        Y.append(r["dq"])
        Xr.append(x)
        Zr.append([1.0, float(r["conc"])] if slope else [1.0])
        G.append(r["subject"])
    return np.array(Y), np.array(Xr), np.array(Zr), np.array(G), subjects


def fit(rows, base, slope=True, baseline_cov=True):
    Y, X, Z, G, subjects = design(rows, base, slope=slope, baseline_cov=baseline_cov)
    out = lme_reml(Y, X, Z, G)
    out.update(n_obs=len(Y), n_subj=len(subjects), p=X.shape[1])
    return out


def predict(model, c, df_rule="residual"):
    x0 = np.zeros(len(model["b"]))
    x0[1] = 1.0
    x0[2] = c
    est = float(x0 @ model["b"])
    se = float(np.sqrt(x0 @ model["cov"] @ x0))
    if df_rule == "residual":
        q = stats.t.ppf(0.95, model["n_obs"] - model["p"])
    elif df_rule == "subjects":
        q = stats.t.ppf(0.95, model["n_subj"] - model["p"])
    else:
        q = stats.norm.ppf(0.95)
    return est, est + q * se, se


def highest_passing(ubs, bound=10.0):
    ok = [d for d in sorted(ubs) if ubs[d] < bound]
    return max(ok) if ok else 0
