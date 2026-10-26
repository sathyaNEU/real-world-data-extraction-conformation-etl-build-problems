"""The call from the shipped pack: each ward's 2025-26 day-shift compliance, the audited moments carried across every AM
and PM shift of the ward by how far the shift's worked nursing hours fell short of its patients' required care hours,
each shift weighted by its required care hours; the estimator family the data does not close, and the rungs."""
import numpy as np
import pandas as pd

import common as K
import pack as P

BANDS = (0.0, 1.05, 1.15, 1.25, 1.35, 99.0)
FAMILY_BANDS = [(0.0, 1.05, 1.15, 1.25, 1.35, 99.0), (0.0, 1.0, 1.1, 1.2, 1.3, 1.4, 99.0), (0.0, 1.1, 1.2, 1.3, 99.0),
                (0.0, 1.05, 1.2, 1.35, 99.0),
                (0.0, 1.025, 1.075, 1.125, 1.175, 1.225, 1.275, 1.325, 1.375, 99.0)]


def frames(target, d=None, m=None, night=False, **opts):
    d = d if d is not None else P.load(target)
    m = m if m is not None else P.maps(d)
    sh = P.day_shifts(d, m, **opts)
    a = P.ward_audits(d, m)
    wa = a[a["ward"].isin(K.WARD)]
    day = wa if night else wa[wa["shift"].isin(["AM", "PM"])]
    if night:
        day = day.assign(shift=day["shift"].where(day["shift"].isin(["AM", "PM"]), "PM"))
    sess = day.groupby(["session_id", "ward", "date", "shift"]).agg(m=("performed", "size"), c=("performed", "sum"))
    sess = sess.reset_index().merge(sh[["ward", "date", "shift", "v", "req", "worked", "npts"]],
                                    on=["ward", "date", "shift"], how="left")
    sess = sess[sess["v"].notna()]
    return dict(d=d, m=m, shifts=sh, audits=a, ward_audits=wa, sess=sess)


def _fit(sess, bands, link):
    codes = K.WARD
    wi = {c: i for i, c in enumerate(codes)}
    aw = sess["ward"].map(wi).to_numpy()
    m = sess["m"].to_numpy(float)
    c = sess["c"].to_numpy(float)
    b = np.array(bands)
    nb = len(b) - 1
    ab = np.searchsorted(b, sess["v"].to_numpy(), side="right") - 1
    wn = len(codes)
    if link == "add":
        al = np.bincount(aw, c, wn) / np.bincount(aw, m, wn)
        be = np.zeros(nb)
        for _ in range(400):
            den = np.bincount(ab, m, nb)
            be = np.where(den > 0, np.bincount(ab, c - m * al[aw], nb) / np.maximum(den, 1e-9), 0.0)
            be -= be[0]
            al = np.bincount(aw, c - m * be[ab], wn) / np.bincount(aw, m, wn)
        return lambda w, bb: al[w] + be[bb]
    ex = lambda z: 1 / (1 + np.exp(-z))
    p0 = np.bincount(aw, c, wn) / np.bincount(aw, m, wn)
    al = np.log(p0 / (1 - p0))
    be = np.zeros(nb)
    for _ in range(300):
        p = ex(al[aw] + be[ab])
        h = np.bincount(ab, m * p * (1 - p), nb)
        be = be + np.where(h > 0, np.bincount(ab, c - m * p, nb) / np.maximum(h, 1e-9), 0.0)
        be -= be[0]
        p = ex(al[aw] + be[ab])
        al = al + np.bincount(aw, c - m * p, wn) / np.bincount(aw, m * p * (1 - p), wn)
    return lambda w, bb: ex(al[w] + be[bb])


def carried(F, bands=BANDS, link="logit", weight="req"):
    """each ward's compliance over every AM and PM shift: the fitted compliance of the shift's band, weighted"""
    f = _fit(F["sess"], bands, link)
    sh = F["shifts"]
    b = np.array(bands)
    out = {}
    for i, code in enumerate(K.WARD):
        s = sh[sh["ward"] == code]
        bb = np.searchsorted(b, s["v"].to_numpy(), side="right") - 1
        est = f(i, bb)
        w = {"req": s["req"].to_numpy(), "shift": np.ones(len(s)), "worked": s["worked"].to_numpy()}[weight]
        out[code] = float((w * est).sum() / w.sum())
    return out


def knee(F, at=1.05):
    sess, sh = F["sess"], F["shifts"]
    wi = {c: i for i, c in enumerate(K.WARD)}
    n = len(K.WARD)
    X = np.zeros((len(sess), n + 1))
    X[np.arange(len(sess)), sess["ward"].map(wi).to_numpy()] = 1
    X[:, n] = np.maximum(0, sess["v"].to_numpy() - at)
    m = sess["m"].to_numpy(float)
    y = sess["c"].to_numpy(float) / m
    beta = np.linalg.lstsq(X * np.sqrt(m)[:, None], y * np.sqrt(m), rcond=None)[0]
    out = {}
    for code in K.WARD:
        s = sh[sh["ward"] == code]
        est = beta[wi[code]] + beta[n] * np.maximum(0, s["v"].to_numpy() - at)
        out[code] = float((s["req"].to_numpy() * est).sum() / s["req"].sum())
    return out


def unpooled(F, bands=BANDS):
    sess, sh = F["sess"], F["shifts"]
    b = np.array(bands)
    nb = len(b) - 1
    out = {}
    for code in K.WARD:
        s = sess[sess["ward"] == code]
        k = np.searchsorted(b, s["v"].to_numpy(), side="right") - 1
        num = np.bincount(k, s["c"].to_numpy(float), nb)
        den = np.bincount(k, s["m"].to_numpy(float), nb)
        rate = np.where(den > 0, num / np.maximum(den, 1), np.nan)
        for j in range(nb):
            if np.isnan(rate[j]):
                rate[j] = rate[j - 1]
        x = sh[sh["ward"] == code]
        kk = np.searchsorted(b, x["v"].to_numpy(), side="right") - 1
        out[code] = float((x["req"].to_numpy() * rate[kk]).sum() / x["req"].sum())
    return out


def proxy(F, kind):
    """the same carrying with another workload measure: patients per worked hour, or required hours per nurse,
    each against the ward's own usual level, in pooled quantile bands"""
    sess, sh = F["sess"].copy(), F["shifts"].copy()
    fn = (lambda x: x["npts"] / x["worked"]) if kind == "ppn" else (lambda x: x["req"] / (x["worked"] / 8.0))
    sh["q"] = fn(sh)
    rel = sh.groupby("ward")["q"].median()
    sh["r"] = sh["q"] / sh["ward"].map(rel)
    sess["r"] = fn(sess) / sess["ward"].map(rel)
    qs = np.quantile(sh["r"].to_numpy(), [0, .5, .7, .8, .9, 1.0])
    qs[0], qs[-1] = -1.0, 1e9
    s2 = sess.copy()
    s2["v"] = s2["r"]
    f = _fit(s2, tuple(qs), "logit")
    out = {}
    for i, code in enumerate(K.WARD):
        x = sh[sh["ward"] == code]
        bb = np.searchsorted(qs, x["r"].to_numpy(), side="right") - 1
        out[code] = float((x["req"].to_numpy() * f(i, bb)).sum() / x["req"].sum())
    return out


def workload(F, kind="req"):
    """the audited compliance carried across every shift by the shift's workload against the ward's usual level, in
    pooled quintile bands: the care hours its patients required, or the patients it held"""
    sess, sh = F["sess"].copy(), F["shifts"].copy()
    rel = sh.groupby("ward")[kind].median()
    sh["r"] = sh[kind] / sh["ward"].map(rel)
    qs = np.quantile(sh["r"].to_numpy(), [0, .2, .4, .6, .8, 1.0])
    qs[0], qs[-1] = -1.0, 1e9
    s2 = sess.copy()
    s2["v"] = s2[kind] / s2["ward"].map(rel)
    f = _fit(s2, tuple(qs), "logit")
    out = {}
    for i, code in enumerate(K.WARD):
        x = sh[sh["ward"] == code]
        bb = np.searchsorted(qs, x["r"].to_numpy(), side="right") - 1
        out[code] = float((x["req"].to_numpy() * f(i, bb)).sum() / x["req"].sum())
    return out


def family(F):
    res = {}
    for bands in FAMILY_BANDS:
        for link in ("add", "logit"):
            for wt in ("req", "shift", "worked"):
                res[("bands", bands, link, wt)] = carried(F, bands, link, wt)
    res[("knee", 1.05)] = knee(F, 1.05)
    res[("knee", 1.0)] = knee(F, 1.0)
    res[("unpooled",)] = unpooled(F)
    res[("proxy", "rpn")] = proxy(F, "rpn")
    return res


def deviance(F, kind):
    """the binomial deviance of the audited sessions under ward plus pooled quintile bands of a staffing measure
    against the ward's usual level: required care hours over worked hours (v), or patients over worked hours (ppn)"""
    sess, sh = F["sess"].copy(), F["shifts"].copy()
    fn = (lambda x: x["req"] / x["worked"]) if kind == "v" else (lambda x: x["npts"] / x["worked"])
    rel = fn(sh).groupby(sh["ward"]).median()
    r_sh = fn(sh) / sh["ward"].map(rel)
    qs = np.quantile(r_sh.to_numpy(), [0, .5, .7, .8, .9, 1.0])
    qs[0], qs[-1] = -1.0, 1e9
    s2 = sess.assign(v=fn(sess) / sess["ward"].map(rel))
    f = _fit(s2, tuple(qs), "logit")
    p = np.clip(f(s2["ward"].map({c: i for i, c in enumerate(K.WARD)}).to_numpy(),
                  np.searchsorted(qs, s2["v"].to_numpy(), side="right") - 1), 1e-9, 1 - 1e-9)
    c, m = s2["c"].to_numpy(float), s2["m"].to_numpy(float)
    ll = c * np.log(p) + (m - c) * np.log(1 - p)
    return float(-2 * ll.sum())


def rungs(F):
    """R0 the audits as they stand (every ward session); R0d the AM and PM sessions; R1 the AM and PM audit
    compliance weighted by the shifts' required care hours; Rm the same by month and shift; Rp the audits carried
    by patients per worked hour; Rq and Rn by the shift's care hours or its patients against the ward's usual level"""
    wa, sess, sh = F["ward_audits"], F["sess"], F["shifts"]
    out = {"R0": {}, "R0d": {}, "R1": {}, "Rm": {}}
    for code in K.WARD:
        a = wa[wa["ward"] == code]
        out["R0"][code] = float(a["performed"].mean())
        s = sess[sess["ward"] == code]
        out["R0d"][code] = float(s["c"].sum() / s["m"].sum())
        x = sh[sh["ward"] == code].copy()
        for key, f in (("R1", lambda df: df["shift"]), ("Rm", lambda df: df["shift"] + pd.to_datetime(df["date"]).dt.strftime("%m"))):
            g = s.assign(k=f(s)).groupby("k")[["c", "m"]].sum()
            wts = x.assign(k=f(x)).groupby("k")["req"].sum()
            wts = wts[wts.index.isin(g.index)]
            out[key][code] = float(sum(wts[k] * g.loc[k, "c"] / g.loc[k, "m"] for k in wts.index) / wts.sum())
    out["Rp"] = proxy(F, "ppn")
    out["Rq"] = workload(F, "req")
    out["Rn"] = workload(F, "npts")
    return out


def components(F):
    """the two facts every route that lands the call works from: where the audited moments sat against the wards' care
    hours, and the audited compliance on shifts whose worked hours covered the required care against those short"""
    sh, sess = F["shifts"], F["sess"]
    short = sh["req"] > sh["worked"]
    care_short = float(sh.loc[short, "req"].sum() / sh["req"].sum())
    s_short = sess["req"] > sess["worked"]
    mom_short = float(sess.loc[s_short, "m"].sum() / sess["m"].sum())
    comp_cov = float(sess.loc[~s_short, "c"].sum() / sess.loc[~s_short, "m"].sum())
    comp_short = float(sess.loc[s_short, "c"].sum() / sess.loc[s_short, "m"].sum())
    ties = int((sh["req"] == sh["worked"]).sum())
    return dict(care_short=care_short, moments_short=mom_short, comp_covered=comp_cov, comp_short=comp_short,
                shifts=int(len(sh)), short_shifts=int(short.sum()), ties=ties,
                audited_moments=int(sess["m"].sum()), audited_short=int(sess.loc[s_short, "m"].sum()))


def golden(target):
    F = frames(target)
    est = carried(F)
    funded = sorted([c for c in K.WARD if est[c] < K.BENCHMARK / 100.0], key=K.WARD.index)
    return dict(F=F, est=est, funded=funded)
