"""The simulated province: families with a long-run income level and a yearly swing around it, the census year for
every family, five tax years for the families in which a parent filed every year, and the children's earnings from
2014 to 2022. Everything is drawn from named streams (common.rng), region by region."""
from __future__ import annotations

import numpy as np

import common as K


def logistic(z):
    return 1.0 / (1.0 + np.exp(-z))


def region_draw(code, name, n_target, mu, sd, bt, bb, knee, fa, fb, su, tax_draw=None):
    """Families and children of one region (arrays). x_p is the family's long-run log income in 2005 dollars; su is
    the spread of the yearly swing around it, which differs by region with the kind of work families do."""
    r = K.rng("families", code)
    nfam = int(round(n_target / 1.35))
    kids = r.choice([1, 2, 3], nfam, p=[0.70, 0.25, 0.05])
    xp = r.normal(mu, sd, nfam)
    u_census = r.normal(0.0, su, nfam)
    u_tax = r.normal(0.0, su, (nfam, len(K.TAX_YEARS)))
    tax_draw = K.TAX_DRAW.get(code, 0) if tax_draw is None else tax_draw
    if tax_draw:
        u_tax = K.rng("tax-years", code, tax_draw).normal(0.0, su, (nfam, len(K.TAX_YEARS)))
    files = r.random(nfam) < logistic(fa + fb * (xp - mu))
    parents = np.where(r.random(nfam) < 0.83, 2, 1)
    # children
    fam_of = np.repeat(np.arange(nfam), kids)
    rc = K.rng("children", code)
    nch = len(fam_of)
    birth = rc.choice(K.COHORTS, nch)
    sex = np.where(rc.random(nch) < 0.5, "F", "M")
    d = xp[fam_of] - mu
    f = np.where(d > knee, bt * d, bt * knee + bb * (d - knee))
    yp = 10.30 + 0.5 * (mu - 11.0) + f + rc.normal(0.0, K.SIGMA_E, nch)
    ny = len(K.EARN_YEARS)
    age = np.array(K.EARN_YEARS)[None, :] - birth[:, None]
    w = rc.normal(0.0, K.SIGMA_W, (nch, ny))
    real = np.exp(yp[:, None] + 0.03 * (age - 32) + w)
    zero = rc.random((nch, ny)) < logistic(-3.0 - 1.5 * (yp[:, None] - 10.3))
    real = np.where(zero, 0.0, real)
    return dict(code=code, name=name, nfam=nfam, kids=kids, xp=xp, u_census=u_census, u_tax=u_tax, files=files,
                parents=parents, fam_of=fam_of, birth=birth, sex=sex, yp=yp, real=real, age=age, mu=mu)


def province(design=None):
    rows = design or K.REGIONS
    return [region_draw(*row) for row in rows]


# ---------------------------------------------------------------------------------------------- the routes on truth
def outcome(R):
    """log of the child's average real earnings at 30 to 34 (zeros counted); children with no earnings excluded."""
    mask = (R["age"] >= 30) & (R["age"] <= 34)
    avg = np.where(mask, R["real"], 0.0).sum(1) / 5.0
    keep = avg > 0
    return np.log(np.where(keep, avg, 1.0)), keep


def _logit_fit(x, t, iters=25):
    """Logistic regression of t (0/1) on x with an intercept, by Newton's method."""
    X = np.column_stack([np.ones_like(x), x])
    b = np.zeros(2)
    for _ in range(iters):
        p = logistic(X @ b)
        g = X.T @ (t - p)
        h = (X * (p * (1 - p))[:, None]).T @ X
        b = b + np.linalg.solve(h, g)
    return logistic(X @ b)


def routes(regions):
    """Each region's elasticity under the default path (the filers' five-year averages), the census year, the
    census year over the filers' reliability ratio, the golden (the census year's spread less the region's own
    transitory variance measured within its filers), and the reflexes: the census year less a provincial transitory
    variance, the filers' averages with their residual attenuation removed, the filers' averages instrumented by the
    census year, and the filers' averages reweighted by the inverse of each family's chance of filing."""
    pooled_n = pooled_d = 0.0
    reg_s2 = {}
    for R in regions:
        lx = R["xp"][R["files"], None] + R["u_tax"][R["files"]]
        w = float(((lx - lx.mean(1, keepdims=True)) ** 2).sum())
        n = lx.shape[0] * (lx.shape[1] - 1)
        reg_s2[R["name"]] = w / n
        pooled_n += w
        pooled_d += n
    pooled = pooled_n / pooled_d
    out = {}
    for R in regions:
        s2 = reg_s2[R["name"]]
        y, keep = outcome(R)
        fam = R["fam_of"][keep]
        y = y[keep]
        xc_fam = R["xp"] + R["u_census"]
        x1 = xc_fam[fam]
        filer = R["files"][fam]
        lx = R["xp"][:, None] + R["u_tax"]
        xbar = np.log(np.exp(lx).mean(1))[fam]
        c = lambda a, b: float(np.cov(a, b)[0, 1])
        v1 = float(np.var(x1, ddof=1))
        r0 = c(y[filer], xbar[filer]) / float(np.var(xbar[filer], ddof=1))
        r1 = c(y, x1) / v1
        lam = c(xbar[filer], x1[filer]) / float(np.var(x1[filer], ddof=1))
        iv = c(y[filer], x1[filer]) / c(xbar[filer], x1[filer])
        p = _logit_fit(xc_fam - xc_fam.mean(), R["files"].astype(float))[fam][filer]
        wt = 1.0 / p
        yb, xb = y[filer], xbar[filer]
        my, mx = np.average(yb, weights=wt), np.average(xb, weights=wt)
        ipw = float(np.sum(wt * (yb - my) * (xb - mx)) / np.sum(wt * (xb - mx) ** 2))
        out[R["name"]] = dict(r0=r0, r1=r1, r2=r1 / lam, gold=c(y, x1) / (v1 - s2), pool=c(y, x1) / (v1 - pooled),
                              r1c=c(y[filer], xbar[filer]) / (float(np.var(xbar[filer], ddof=1)) - s2 / 5),
                              iv=iv, ipw=ipw, n=int(keep.sum()), filers=float(R["files"].mean()), s2=s2)
    return out, pooled
