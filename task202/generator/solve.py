"""Clause 9's quantity, and every route to it.

Clause 9 files the quantity: the lowest amount, a multiple of PHP 100, such that when each band's
ceiling is generated from it by schedule B's scale and rounded up to the nearest PHP 100, the share
of the scheme's awards that would be referred is at or below 6.0 per cent. It files no method, and
the seven routes below all execute it; they differ in which distribution the share is computed on.
"""
import numpy as np

import params as P


def band_ceiling(C, b):
    """Schedule B: the band factor applied to the reference ceiling, rounded up to PHP 100."""
    num = int(round(C)) * P.SCALE3[b]            # factor x 1000, exact integers
    return int(-((-num) // (1000 * P.ROUND_TO)) * P.ROUND_TO)


def ceilings(C):
    return {b: band_ceiling(C, b) for b in P.BANDS}


# ---------------------------------------------------------------- the filed share, three ways
def share_cells(C, mean, cnt, shape):
    """The share of the scheme's awards above their band ceiling, with the award distribution built
    per partner-band cell from the cell's own stated average and the award shape."""
    shp = np.sort(np.asarray(shape, float))
    ks = sorted(cnt)
    n = np.array([cnt[k] for k in ks], float)
    thr = np.array([band_ceiling(C, k[1]) / mean[k] for k in ks], float)
    above = 1.0 - np.searchsorted(shp, thr, side="right") / len(shp)
    return float((n * above).sum() / n.sum())


def share_pool(C, vals, bands, weight):
    """The share when the award distribution is taken from a pool of award amounts, each band's
    pool weighted by `weight`."""
    vals = np.asarray(vals, float)
    bands = np.asarray(bands)
    tot = float(sum(weight.values()))
    above = 0.0
    for b in P.BANDS:
        v = np.sort(vals[bands == b])
        if len(v):
            above += weight[b] * (1.0 - np.searchsorted(v, band_ceiling(C, b), side="right") / len(v))
    return above / tot


def lowest(fn, cap=None, lo=1000, hi=90000):
    """The lowest multiple of PHP 100 whose share is at or below the cap (clause 9's own words)."""
    cap = P.COMMITTED_SHARE if cap is None else cap
    a, b = int(lo), int(hi)
    assert fn(b) <= cap, "the search range does not reach the cap"
    if fn(a) <= cap:
        return a
    while b - a > P.ROUND_TO:
        mid = max(int((a + b) // 2 // P.ROUND_TO * P.ROUND_TO), a + P.ROUND_TO)
        if fn(mid) <= cap:
            b = mid
        else:
            a = mid
    return b


# ---------------------------------------------------------------- the ladder
def quantiles_lognormal(cv, n=300000):
    from scipy.stats import norm
    v = np.log(1.0 + cv ** 2)
    q = np.exp(norm.ppf(np.linspace(0.5 / n, 1 - 0.5 / n, n)) * np.sqrt(v) - 0.5 * v)
    return q / q.mean()


def quantiles_gamma(cv, n=300000):
    from scipy.stats import gamma
    k = 1.0 / cv ** 2
    q = gamma.ppf(np.linspace(0.5 / n, 1 - 0.5 / n, n), k, scale=1.0 / k)
    return q / q.mean()


def em_two_component(s, restarts=6, iters=800):
    """A correctly specified two-component lognormal mixture, fitted by EM on the measured shape."""
    l = np.log(np.asarray(s, float))
    best = None
    for r0 in range(restarts):
        rr = np.random.default_rng(1234 + r0)
        mu = np.array([np.quantile(l, 0.3) + rr.normal(0, .1), np.quantile(l, 0.9) + rr.normal(0, .1)])
        sd = np.array([0.25, 0.25]) * np.exp(rr.normal(0, .2, 2))
        pi = np.array([0.8, 0.2])
        ll_old = -1e18
        for _ in range(iters):
            d = np.stack([pi[k] * np.exp(-0.5 * ((l - mu[k]) / sd[k]) ** 2) / sd[k] for k in range(2)])
            tot = np.maximum(d.sum(0), 1e-300)
            ll = float(np.log(tot).sum())
            rz = d / tot
            pi = rz.mean(1)
            mu = (rz * l).sum(1) / rz.sum(1)
            sd = np.sqrt(np.maximum((rz * (l - mu[:, None]) ** 2).sum(1) / rz.sum(1), 1e-6))
            if ll - ll_old < 1e-9:
                break
            ll_old = ll
        if best is None or ll_old > best[0]:
            best = (ll_old, pi.copy(), mu.copy(), sd.copy())
    return best[1], best[2], best[3]


def mixture_quantiles(pi, mu, sd, n=300000):
    from scipy.stats import norm
    grid = np.exp(np.linspace(np.log(0.02), np.log(80.0), 400000))
    cdf = sum(pi[k] * norm.cdf((np.log(grid) - mu[k]) / sd[k]) for k in range(len(pi)))
    q = np.interp(np.linspace(0.5 / n, 1 - 0.5 / n, n), cdf, grid)
    return q / q.mean()


ROUTES = ["R1", "R2", "R3", "R4", "R5a", "R5b"]
LABEL = {
    "R1": "cut the distribution of partner-band average awards, award-count weighted",
    "R2": "cut the portal's award amounts pooled as they stand",
    "R3": "cut the pooled portal rescaled by one portfolio-to-portal ratio",
    "R4": "cut the portal rescaled per band and reweighted to the portfolio's band counts",
    "R5a": "rebuild per partner-band, one lognormal at the portal's coefficient of variation",
    "R5b": "rebuild per partner-band, one gamma at the portal's coefficient of variation",
    "R6": "rebuild per partner-band with the award shape as the portal measures it",
    "Rmix": "rebuild per partner-band, a two-component lognormal mixture fitted by EM",
}


def ladder(W, cap=None):
    """Every route's ceiling, computed forward from the claim returns and the portal."""
    mean, cnt, shape = W["mean"], W["cnt"], W["shape"]
    pw_amt = np.array([a["amount"] for a in W["porwin"]], float)
    pw_band = np.array([a["band"] for a in W["porwin"]])
    w_port = {b: float(sum(v for k, v in cnt.items() if k[1] == b)) for b in P.BANDS}
    w_pilot = {b: float((pw_band == b).sum()) for b in P.BANDS}
    cv = float(shape.std(ddof=1) / shape.mean())
    out = {}
    out["R6"] = lowest(lambda C: share_cells(C, mean, cnt, shape), cap)
    out["R1"] = lowest(lambda C: share_cells(C, mean, cnt, np.array([1.0])), cap)
    out["R2"] = lowest(lambda C: share_pool(C, pw_amt, pw_band, w_pilot), cap)
    port_mean = sum(mean[k] * cnt[k] for k in cnt) / sum(cnt.values())
    ratio = port_mean / pw_amt.mean()
    out["R3"] = lowest(lambda C: share_pool(C, pw_amt * ratio, pw_band, w_pilot), cap)
    rs = np.empty_like(pw_amt)
    for b in P.BANDS:
        sel = pw_band == b
        mb = sum(mean[k] * cnt[k] for k in cnt if k[1] == b) / sum(cnt[k] for k in cnt if k[1] == b)
        rs[sel] = pw_amt[sel] * (mb / pw_amt[sel].mean())
    out["R4"] = lowest(lambda C: share_pool(C, rs, pw_band, w_port), cap)
    out["R5a"] = lowest(lambda C: share_cells(C, mean, cnt, quantiles_lognormal(cv)), cap)
    out["R5b"] = lowest(lambda C: share_cells(C, mean, cnt, quantiles_gamma(cv)), cap)
    pi, mu, sd = em_two_component(shape)
    out["Rmix"] = lowest(lambda C: share_cells(C, mean, cnt, mixture_quantiles(pi, mu, sd)), cap)
    out["_cv"] = cv
    out["_mix_params"] = (pi.tolist(), mu.tolist(), sd.tolist())
    return out


# ---------------------------------------------------------------- the figures the asks owe
def figures_for(C, W):
    """Every graded figure the schedule produces, from the claim returns and the portal."""
    mean, cnt, shape = W["mean"], W["cnt"], W["shape"]
    shp = np.sort(shape)
    nshp = len(shp)
    cs = np.concatenate([[0.0], np.cumsum(shp)])
    cl = ceilings(C)
    per_band = {}
    tot_n = tot_ref = tot_val = tot_refval = 0.0
    for b in P.BANDS:
        bn = bref = bval = brefval = 0.0
        for k in sorted(cnt):
            if k[1] != b:
                continue
            n, m = cnt[k], mean[k]
            i = int(np.searchsorted(shp, cl[b] / m, side="right"))
            above = (nshp - i) / nshp
            vabove = (cs[nshp] - cs[i]) / nshp            # E[shape . 1{shape > t}]
            bn += n
            bref += n * above
            bval += n * m
            brefval += n * m * vabove
        per_band[b] = dict(ceiling=cl[b], awards=bn, referred=bref,
                           referred_share=100.0 * bref / bn,
                           value=bval, referred_value=brefval,
                           referred_value_share=100.0 * brefval / bval,
                           factor=P.SCALE3[b] / 1000.0)
        tot_n += bn
        tot_ref += bref
        tot_val += bval
        tot_refval += brefval
    return dict(C=C, bands=per_band, awards=tot_n, referred=tot_ref,
                referred_share=100.0 * tot_ref / tot_n, value=tot_val,
                referred_value=tot_refval, referred_value_share=100.0 * tot_refval / tot_val,
                cv=float(shape.std(ddof=1) / shape.mean()))
