"""Estimators of a group's breast cancer risk by 70 for a woman who carries it, from the probands' mothers, sisters and
daughters, and the easy routes beside them. Every function takes ages in completed years as the pedigree carries
them: t is the age at a first breast cancer (ev 1) or the age at the family's history date or at death (ev 0)."""
import numpy as np
from scipy.optimize import minimize

T0 = 70


def km(t, ev, w=None, t0=T0):
    """1 - S just before age t0: events at completed ages below t0, events before censorings at a tied age."""
    t = np.asarray(t, float)
    ev = np.asarray(ev, int)
    w = np.ones_like(t) if w is None else np.asarray(w, float)
    S = 1.0
    for a in range(0, t0):
        at = w[t >= a].sum()
        d = w[(t == a) & (ev == 1)].sum()
        if at > 0 and d > 0:
            S *= 1 - d / at
    return 1 - S


def pop_risk(rates_per_100k, t0=T0):
    """The population's risk by t0 from 5-year band rates per 100,000 (bands from 0-4)."""
    r = np.asarray(rates_per_100k, float)[: t0 // 5]
    return float(1 - np.exp(-(r * 5).sum() / 1e5))


def kin_cohort(t, ev, f_n):
    """Every first-degree relative carries the variant with probability one half: F_rel = (F_c + F_n) / 2."""
    return 2 * km(t, ev) - f_n


BANDS = np.array([0, 40, 50, 60, 70.0])


def _exposure(tc):
    return np.stack([np.clip(tc - BANDS[k], 0, BANDS[k + 1] - BANDS[k]) for k in range(4)], 1)


def _pop_terms(tc, ev, rates):
    """the population's cumulative hazard to each woman's time and its log hazard at her event (5-year bands)"""
    h = np.asarray(rates, float) / 1e5
    edges = np.arange(0, 5 * len(h) + 1, 5)
    full = np.minimum(np.maximum(tc[:, None] - edges[:-1], 0), 5)
    H = (full * h).sum(1)
    lh = np.log(np.maximum(h[np.minimum((tc // 5).astype(int), len(h) - 1)], 1e-12))
    return H, lh


def mendel(t, ev, car, tested, rates=None, form="piecewise"):
    """The likelihood of every woman's history, her genotype where a test gives it and the one-half prior where it
    does not; the noncarrier hazard is the population's (rates given) or estimated with the carrier's."""
    t = np.asarray(t, float)
    ev = np.asarray(ev, int)
    ev = np.where(t < T0, ev, 0)
    tc = np.minimum(t + 0.5, float(T0))
    car = np.asarray(car, int)
    tested = np.asarray(tested, int)
    X = _exposure(tc)
    band = np.clip(np.searchsorted(BANDS, tc, side="right") - 1, 0, 3)
    fixed = rates is not None
    if fixed:
        Hn, lhn = _pop_terms(tc, ev, rates)

    def combine(lc, ln):
        return np.where(tested == 1, np.where(car == 1, lc, ln), np.logaddexp(lc, ln) + np.log(0.5))

    if form == "piecewise":
        k = 4 if fixed else 8

        def nll(th):
            hc = np.exp(th[:4])
            lc = -(X @ hc) + ev * th[:4][band]
            if fixed:
                ln = -Hn + ev * lhn
            else:
                hn = np.exp(th[4:])
                ln = -(X @ hn) + ev * th[4:][band]
            return -combine(lc, ln).sum()
        best = None
        for start in (-5.0, -4.0, -6.0):
            r = minimize(nll, np.full(k, start), method="L-BFGS-B", bounds=[(-14, 0)] * k)
            if best is None or r.fun < best.fun:
                best = r
        hc = np.exp(best.x[:4])
        return float(1 - np.exp(-(hc * np.diff(BANDS)).sum()))
    tt = np.maximum(tc, 0.5)

    def parts(a, b):
        lam, kk = np.exp(a), np.exp(b)
        return (tt * lam) ** kk, np.log(kk) + kk * np.log(lam) + (kk - 1) * np.log(tt)

    def nll(th):
        Hc, lhc = parts(th[0], th[1])
        lc = -Hc + ev * lhc
        if fixed:
            ln = -Hn + ev * lhn
        else:
            H2, lh2 = parts(th[2], th[3])
            ln = -H2 + ev * lh2
        return -combine(lc, ln).sum()
    bnds = [(-9, -2), (-0.5, 2.5)] * (1 if fixed else 2)
    best = None
    for s in ([np.log(1 / 90), np.log(3.0)], [np.log(1 / 70), np.log(2.0)], [np.log(1 / 120), np.log(4.0)]):
        x0 = s + ([] if fixed else [np.log(1 / 150), np.log(3.5)])
        r = minimize(nll, x0, method="L-BFGS-B", bounds=bnds)
        if best is None or r.fun < best.fun:
            best = r
    lam, kk = np.exp(best.x[0]), np.exp(best.x[1])
    return float(1 - np.exp(-(T0 * lam) ** kk))


def retrospective(t, ev, car, tested, rates):
    """The genotype-restricted likelihood: each tested woman's genotype given her history, the one-half prior and the
    population's hazard for a noncarrier, so testing that follows the history leaves it unbiased."""
    t = np.asarray(t, float)
    ev = np.asarray(ev, int)
    ev = np.where(t < T0, ev, 0)
    tc = np.minimum(t + 0.5, float(T0))
    sel = np.asarray(tested, int) == 1
    car = np.asarray(car, int)[sel]
    tc, ev = tc[sel], ev[sel]
    X = _exposure(tc)
    band = np.clip(np.searchsorted(BANDS, tc, side="right") - 1, 0, 3)
    Hn, lhn = _pop_terms(tc, ev, rates)
    ln = -Hn + ev * lhn

    def nll(th):
        lc = -(X @ np.exp(th)) + ev * th[band]
        post = np.where(car == 1, lc, ln) - np.logaddexp(lc, ln)
        return -post.sum()
    best = None
    for start in (-5.0, -4.0, -6.0):
        r = minimize(nll, np.full(4, start), method="L-BFGS-B", bounds=[(-14, 0)] * 4)
        if best is None or r.fun < best.fun:
            best = r
    return float(1 - np.exp(-(np.exp(best.x) * np.diff(BANDS)).sum()))


def ipw_living(t, ev, car, tested, alive):
    """The tested carriers among the living, each weighted by one over the share of the living with her diagnosis
    status (ever affected or not) who were tested."""
    t, ev, car, tested, alive = (np.asarray(x) for x in (t, ev, car, tested, alive))
    w = np.zeros(len(t))
    for a in (0, 1):
        m = (alive == 1) & (ev == a)
        r = tested[m].mean() if m.sum() else 0.0
        w[m & (tested == 1)] = 1.0 / r if r > 0 else 0.0
    sel = (tested == 1) & (car == 1) & (alive == 1)
    return km(t[sel], ev[sel], w[sel])


FAMILY = ("kin", "mendel_pw_fix", "mendel_pw_free", "mendel_wb_fix")
RECORDED = ("retrospective",)
ROUTES = ("default", "naive", "relshare", "sloppy", "kin_testedneg", "ipw_living")


def estimates(t, ev, car, tested, alive, rates, proband_t=None, proband_ev=None):
    """Every estimator and route for one group. car and tested are the laboratory's view: car is read only where
    tested is 1."""
    t, ev, car, tested, alive = (np.asarray(x) for x in (t, ev, car, tested, alive))
    f_n = pop_risk(rates)
    tc = (tested == 1) & (car == 1)
    tn = (tested == 1) & (car == 0)
    out = {}
    out["kin"] = kin_cohort(t, ev, f_n)
    out["mendel_pw_fix"] = mendel(t, ev, car, tested, rates)
    out["mendel_pw_free"] = mendel(t, ev, car, tested)
    out["mendel_wb_fix"] = mendel(t, ev, car, tested, rates, form="weibull")
    out["retrospective"] = retrospective(t, ev, car, tested, rates)
    out["default"] = km(t[tc], ev[tc])
    if proband_t is not None:
        out["naive"] = km(np.concatenate([t[tc], proband_t]), np.concatenate([ev[tc], proband_ev]))
    f_rel = km(t, ev)
    out["relshare"] = f_rel
    out["sloppy"] = 2 * f_rel
    out["kin_testedneg"] = 2 * f_rel - km(t[tn], ev[tn])
    out["ipw_living"] = ipw_living(t, ev, car, tested, alive)
    out["f_rel"] = f_rel
    out["f_n"] = f_n
    return out
