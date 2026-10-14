"""The forecasts of council-funded residents, from stay-level inputs that the shipped files give (or the true timeline
gives, before observation). Every rung of the ladder and the golden family.

Inputs (a dict of numpy arrays, days as integers from world.EPOCH; np.inf where open):
  cf_admit, cf_entry, cf_exit, cf_care, cf_route   council-funded long-stay stays (entry = funding start)
  sf_admit, sf_entry, sf_end, sf_reason, sf_care   self-funders' awards (reason: 'CONV', 'EXIT' or '' when open)
"""
import datetime as dt

import numpy as np

import world as W

MONTH = W.MONTH
# calendar-month clock: month index plus the fraction of the month gone, for every day to 2030
_DAYS = np.arange(0, W.dn(dt.date(2031, 1, 1)))
def _build_cm():
    out = np.empty(len(_DAYS))
    d = W.EPOCH
    k = 0
    while k < len(_DAYS):
        nxt = dt.date(d.year + (d.month == 12), d.month % 12 + 1, 1)
        n = (nxt - d).days
        base = (d.year - 2000) * 12 + (d.month - 1)
        out[k:k + n] = base + np.arange(n) / n
        k += n
        d = nxt
    return out


_CM = _build_cm()


def months(a, b, clock="days"):
    """months from day a to day b"""
    if clock == "days":
        return (np.asarray(b, float) - np.asarray(a, float)) / MONTH
    a = np.asarray(a, float)
    b = np.asarray(b, float)
    fa = np.floor(a).astype(int)
    fb = np.floor(np.where(np.isfinite(b), b, 0)).astype(int)
    out = _CM[np.clip(fb, 0, len(_CM) - 1)] - _CM[np.clip(fa, 0, len(_CM) - 1)]
    return np.where(np.isfinite(b), out, np.inf)


class Hazard:
    """piecewise-constant hazard per month by months since admission, bands of `band` months"""

    def __init__(self, h, band):
        self.h = np.asarray(h, float)
        self.band = band
        self.edges = np.arange(len(h) + 1) * band
        self.cum = np.concatenate([[0.0], np.cumsum(self.h * band)])

    def at(self, d):
        b = np.minimum((np.asarray(d) / self.band).astype(int), len(self.h) - 1)
        return self.h[b]

    def H(self, d):
        d = np.asarray(d, float)
        b = np.minimum((d / self.band).astype(int), len(self.h) - 1)
        return self.cum[b] + self.h[b] * (d - self.edges[b])


def occ_exp(admit, start, end, event, lo, hi, band, nb, clock="days"):
    """occurrence / exposure by duration band: people at risk from max(start, lo) to min(end, hi); an event counts
    when it falls at end inside (lo, hi]"""
    s = np.maximum(start, lo)
    e = np.minimum(end, hi)
    ok = e > s
    m0 = months(admit[ok], s[ok], clock)
    m1 = months(admit[ok], e[ok], clock)
    edges = np.arange(nb + 1) * band
    edges[-1] = 1e9
    expo = np.array([np.clip(np.minimum(m1, edges[b + 1]) - np.maximum(m0, edges[b]), 0, None).sum() for b in range(nb)])
    ev = event[ok] & (end[ok] <= hi) & (end[ok] > lo)
    dur = m1[ev]
    occ = np.bincount(np.minimum((dur / band).astype(int), nb - 1), minlength=nb).astype(float)
    return occ, expo


def rate(occ, expo):
    h = np.divide(occ, expo, out=np.zeros_like(occ), where=expo > 0)
    # the open last band takes the pooled rate of everything beyond it
    return h


DEFAULT = dict(lo=W.HIST_START, band=1.0, step=0.1, exits="pooled", clock="days", cf_clock="admission",
               adm_window=(2024, 2026), sf_clock="admit", post_asof_sf=False)


def fit(I, **kw):
    o = dict(DEFAULT, **kw)
    band, lo, clock = o["band"], o["lo"], o["clock"]
    nb = int(np.ceil(180 / band))
    hi = W.ASOF
    sf_admit = I["sf_admit"] if o["sf_clock"] == "admit" else I["sf_award"]
    # exit hazard of council-funded residents, by months since care home admission (or since funding began)
    cf_clock_admit = I["cf_admit"] if o["cf_clock"] == "admission" else I["cf_entry"]
    ex = np.isfinite(I["cf_exit"])
    HX = {}
    for c in (0, 1):
        m = (I["cf_care"] == c) if o["exits"] == "care" else np.ones(len(I["cf_care"]), bool)
        oc, ep = occ_exp(cf_clock_admit[m], I["cf_entry"][m], I["cf_exit"][m], ex[m], lo, hi, band, nb, clock)
        HX[c] = Hazard(rate(oc, ep), band)
    # self-funders: conversion and other exits, by months since admission
    end = I["sf_end"]
    conv = I["sf_reason"] == "CONV"
    oth = I["sf_reason"] == "EXIT"
    oc, ep = occ_exp(sf_admit, I["sf_entry"], end, conv, lo, hi, band, nb, clock)
    HC = Hazard(rate(oc, ep), band)
    oc2, ep2 = occ_exp(sf_admit, I["sf_entry"], end, oth, lo, hi, band, nb, clock)
    HS = Hazard(rate(oc2, ep2), band)
    return o, HX, HC, HS


def qmonths(clock):
    return np.array([float(months(np.array([W.ASOF]), np.array([q]), clock)[0]) for q in W.QEND])


def survivors(I, o, HX):
    """today's council-funded residents still in place at each quarter end, by care type"""
    clock = o["clock"]
    on = (I["cf_entry"] <= W.ASOF) & (I["cf_exit"] > W.ASOF)
    base_admit = I["cf_admit"] if o["cf_clock"] == "admission" else I["cf_entry"]
    d0 = months(base_admit[on], np.full(on.sum(), W.ASOF), clock)
    care = I["cf_care"][on]
    qm = qmonths(clock)
    out = np.zeros((4, 2))
    for c in (0, 1):
        m = care == c
        for k in range(4):
            out[k, c] = np.exp(-(HX[c].H(d0[m] + qm[k]) - HX[c].H(d0[m]))).sum()
    return out, int(on.sum())


def inflow(rate_by_care, entry_durs, o, HX):
    """a flow entering at rate_by_care per month, each entrant at a duration drawn from entry_durs, surviving to
    each quarter end"""
    qm = qmonths(o["clock"])
    h = o["step"]
    out = np.zeros((4, 2))
    ed = np.asarray(entry_durs, float)
    for k in range(4):
        n = int(np.ceil(qm[k] / h - 1e-9))
        dt_ = qm[k] / n
        tin = (np.arange(n) + 0.5) * dt_
        for c in (0, 1):
            left = qm[k] - tin
            sv = np.array([np.mean(np.exp(-(HX[c].H(ed + l) - HX[c].H(ed)))) for l in left])
            out[k, c] += rate_by_care[c] * dt_ * sv.sum()
    return out


def direct_rate(I, o):
    y0, y1 = o["adm_window"]
    a0, a1 = W.dn(dt.date(y0, 1, 1)), W.dn(dt.date(y1 + 1, 1, 1))
    mo = (y1 - y0 + 1) * 12
    m = (I["cf_route"] == "DIRECT") & (I["cf_entry"] >= a0) & (I["cf_entry"] < a1)
    return np.array([(m & (I["cf_care"] == c)).sum() / mo for c in (0, 1)])


def pool(I):
    on = (I["sf_entry"] <= W.ASOF) & (I["sf_end"] > W.ASOF)
    return on


def project_pool(I, o, HX, HC, HS, competing=True):
    """each current self-funder's conversion by months since admission, deaths and discharges competing, and survival
    after conversion; returns the surviving converted residents at each quarter end by care type"""
    clock = o["clock"]
    on = pool(I)
    sf_admit = I["sf_admit"] if o["sf_clock"] == "admit" else I["sf_award"]
    d0 = months(sf_admit[on], np.full(on.sum(), W.ASOF), clock)
    care = I["sf_care"][on]
    qm = qmonths(clock)
    h = o["step"]
    out = np.zeros((4, 2))
    s = np.ones(len(d0))
    t = 0.0
    T = qm[-1]
    while t < T - 1e-9:
        hh = min(h, T - t)
        for q in qm:
            if t < q - 1e-9 < t + hh:
                hh = q - t
        lc = HC.at(d0 + t)
        lx = HS.at(d0 + t) if competing else 0.0 * lc
        tot = lc + lx
        frac = np.divide(lc, tot, out=np.zeros_like(tot), where=tot > 0)
        p = s * frac * (1 - np.exp(-tot * hh))
        mid = t + hh / 2
        for k in range(4):
            if mid < qm[k]:
                for c in (0, 1):
                    m = care == c
                    dd_ = d0[m] + mid
                    out[k, c] += (p[m] * np.exp(-(HX[c].H(d0[m] + qm[k]) - HX[c].H(dd_)))).sum()
        s = s * np.exp(-tot * hh)
        t += hh
    return out, int(on.sum())


def post_asof_sf(I, o, HX, HC, HS, w2=0.0):
    """self-funders admitted after the as-of date at the 2026 rate who convert and survive to each quarter end"""
    clock = o["clock"]
    a0, a1 = W.dn(dt.date(2026, 1, 1)), W.dn(dt.date(2027, 1, 1))
    m = (I["sf_admit"] >= a0) & (I["sf_admit"] < a1)
    r = np.array([(m & (I["sf_care"] == c)).sum() / 12.0 for c in (0, 1)])
    qm = qmonths(clock)
    out = np.zeros((4, 2))
    h = 0.25
    for k in range(4):
        n = int(np.ceil(qm[k] / h))
        dt_ = qm[k] / n
        for j in range(n):
            tin = (j + 0.5) * dt_
            # an entrant at tin converts by quarter end with the competing-risk probability, then survives; an entrant
            # before 5 April 2027 has their clock moved on w2 weeks that day, the stretch passed converting
            s, t, acc = 1.0, 0.0, np.zeros(2)
            tA = float(months(np.array([W.ASOF]), np.array([D2]), clock)[0])
            a2 = w2 * 7 / MONTH
            sh = 0.0
            jumped = tin >= tA or a2 <= 0
            while t < qm[k] - tin - 1e-9:
                if not jumped and tin + t >= tA - 1e-9:
                    pj = s * (1 - np.exp(-(HC.H(np.array([t + a2]))[0] - HC.H(np.array([t]))[0])))
                    for c in (0, 1):
                        acc[c] += pj * np.exp(-(HX[c].H(np.array([qm[k] - tin]))[0] - HX[c].H(np.array([t]))[0]))
                    s -= pj
                    sh = a2
                    jumped = True
                hh = min(0.25, qm[k] - tin - t)
                if not jumped:
                    hh = min(hh, tA - tin - t)
                lc, lx = float(HC.at(np.array([t + sh]))[0]), float(HS.at(np.array([t]))[0])
                tot = lc + lx
                p = s * (lc / tot) * (1 - np.exp(-tot * hh)) if tot > 0 else 0.0
                for c in (0, 1):
                    acc[c] += p * np.exp(-(HX[c].H(np.array([qm[k] - tin]))[0] - HX[c].H(np.array([t + hh / 2]))[0]))
                s *= np.exp(-tot * hh)
                t += hh
            out[k] += r * dt_ * acc
    return out


def plain(I, **kw):
    """the hazard by months since admission projected as fitted, no change of capital limit in the forward window: the
    default path (R5)"""
    o, HX, HC, HS = fit(I, **kw)
    A, n_cf = survivors(I, o, HX)
    C = inflow(direct_rate(I, o), [0.0], o, HX)
    G, n_sf = project_pool(I, o, HX, HC, HS, True)
    tot = A + C + G
    if o["post_asof_sf"]:
        tot = tot + post_asof_sf(I, o, HX, HC, HS)
    return dict(total=tot.sum(axis=1), by_care=tot, survivors=A.sum(axis=1), direct=C.sum(axis=1), conversions=G.sum(axis=1),
                n_cf=n_cf, n_sf=n_sf, HX=HX, HC=HC, HS=HS, o=o)


# ------------------------------------------------------------------------------------------------ the capital limits

D1, D2 = W.STAGE1, W.STAGE2
RISE1 = W.CAPITAL[2026][1] - W.CAPITAL[2025][1]
RISE2 = W.CAPITAL[2027][1] - W.CAPITAL[2026][1]


def conv_days(I):
    return I["sf_end"][I["sf_reason"] == "CONV"]


def measure(I, weeks=52, how="before", fitres=None):
    """what the 6 April 2026 rise was worth in weeks of conversions: the conversions taking effect that day less an
    ordinary day's, over an ordinary week's. how: 'before' (the weeks before), 'after' (the weeks after, not the day),
    'around' (both), 'model' (the fitted hazard on the pool the day before), 'year' (calendar 2025)"""
    c = conv_days(I)
    on_day = int((c == D1).sum())
    if how == "before":
        flow = ((c >= D1 - 7 * weeks) & (c < D1)).sum() / weeks
    elif how == "after":
        flow = ((c > D1) & (c <= D1 + 7 * weeks)).sum() / weeks
    elif how == "around":
        flow = (((c >= D1 - 7 * weeks) & (c < D1)).sum() + ((c > D1) & (c <= D1 + 7 * weeks)).sum()) / (2 * weeks)
    elif how == "year":
        a0, a1 = W.dn(dt.date(2025, 1, 1)), W.dn(dt.date(2026, 1, 1))
        flow = ((c >= a0) & (c < a1)).sum() / 365.0 * 7
    else:
        o, HX, HC, HS = fitres
        t0 = D1 - 1
        on = (I["sf_entry"] <= t0) & (I["sf_end"] > t0)
        d0 = months(I["sf_admit"][on], np.full(on.sum(), t0), o["clock"])
        flow = float((1 - np.exp(-(HC.H(d0 + 7 / MONTH) - HC.H(d0)))).sum())
    excess = on_day - flow / 7.0
    return dict(on_day=on_day, flow=float(flow), excess=float(excess), w1=float(excess / flow))


def project_members(d0, shift, care, o, HX, HC, HS, w2, mode="jump", competing=True):
    """surviving conversions at each quarter end of self-funders at months since admission d0 on 31 December 2026,
    their capital clocks `shift` months ahead; on 5 April 2027 every clock moves w2 weeks: the self-funders it carries
    past the limit convert that day ('jump'), or only those ('pulse'), or the clocks move and nobody converts that day
    ('shift')"""
    clock = o["clock"]
    qm = qmonths(clock)
    tA = float(months(np.array([W.ASOF]), np.array([D2]), clock)[0])
    a2 = w2 * 7 / MONTH
    h = o["step"]
    out = np.zeros((4, 2))
    s = np.ones(len(d0))
    shift = np.array(shift, float).copy()
    t = 0.0
    T = qm[-1]
    jumped = False

    def credit(p, at):
        for k in range(4):
            if at < qm[k]:
                for cc in (0, 1):
                    m = care == cc
                    if m.any():
                        out[k, cc] += (p[m] * np.exp(-(HX[cc].H(d0[m] + qm[k]) - HX[cc].H(d0[m] + at)))).sum()
    while t < T - 1e-9:
        if not jumped and t >= tA - 1e-9:
            if a2 > 0 and mode in ("jump", "pulse"):
                cd = d0 + shift + t
                pj = s * (1 - np.exp(-(HC.H(cd + a2) - HC.H(cd))))
                credit(pj, t)
                s = s - pj
            if mode in ("jump", "shift"):
                shift = shift + a2
            jumped = True
        hh = min(h, T - t)
        if not jumped and t + hh > tA:
            hh = tA - t
        for q in qm:
            if t < q - 1e-9 < t + hh:
                hh = q - t
        lc = HC.at(d0 + shift + t)
        lx = HS.at(d0 + t) if competing else 0.0 * lc
        tot = lc + lx
        frac = np.divide(lc, tot, out=np.zeros_like(tot), where=tot > 0)
        p = s * frac * (1 - np.exp(-tot * hh))
        credit(p, t + hh / 2)
        s = s * np.exp(-tot * hh)
        t += hh
    return out


def pool_clocks(I, o, w1, apply1=True):
    on = pool(I)
    sf_clock = I["sf_admit"] if o["sf_clock"] == "admit" else I["sf_award"]
    d0 = months(sf_clock[on], np.full(on.sum(), W.ASOF), o["clock"])
    a1 = w1 * 7 / MONTH if apply1 else 0.0
    shift = np.where(I["sf_admit"][on] < D1, a1, 0.0)
    return d0, shift, I["sf_care"][on]


def capital_fit(I, w1, **kw):
    """the conversion hazard on the capital clock: a self-funder in the pool on 6 April 2026 is w1 weeks further on from
    that day, the day's conversions falling in the stretch the clock passed"""
    o = dict(DEFAULT, **kw)
    band, lo, clock = o["band"], o["lo"], o["clock"]
    nb = int(np.ceil(180 / band))
    o2, HX, HC0, HS = fit(I, **kw)
    a1 = w1 * 7 / MONTH
    adm, ent, end = I["sf_admit"], I["sf_entry"], I["sf_end"]
    conv = I["sf_reason"] == "CONV"
    on = (ent < D1) & (end >= D1) & (adm < D1)
    edges = np.arange(nb + 1) * band
    edges[-1] = 1e9
    expo = np.zeros(nb)
    occ = np.zeros(nb)

    def add(m0, m1):
        for b in range(nb):
            expo[b] += np.clip(np.minimum(m1, edges[b + 1]) - np.maximum(m0, edges[b]), 0, None).sum()
    # before 6 April 2026 (or never in the pool that day): months since admission as they run
    s = np.maximum(ent, lo)
    e = np.where(on, np.minimum(D1, W.ASOF), np.minimum(end, W.ASOF))
    ok = e > s
    add(months(adm[ok], s[ok], clock), months(adm[ok], e[ok], clock))
    ev = ok & conv & (end > lo) & (end <= W.ASOF) & ~on
    occ += np.bincount(np.minimum((months(adm[ev], end[ev], clock) / band).astype(int), nb - 1), minlength=nb)
    # the stretch the clock passed on 6 April 2026, and the conversions that took effect that day
    d1 = months(adm[on], np.full(on.sum(), D1), clock)
    add(d1, d1 + a1)
    j = on & conv & (end == D1)
    dj = months(adm[j], np.full(j.sum(), D1), clock) + a1 / 2
    occ += np.bincount(np.minimum((dj / band).astype(int), nb - 1), minlength=nb)
    # after it: w1 weeks further on
    e2 = np.minimum(end, W.ASOF)
    ok2 = on & (e2 > D1)
    add(months(adm[ok2], np.full(ok2.sum(), D1), clock) + a1, months(adm[ok2], e2[ok2], clock) + a1)
    ev2 = ok2 & conv & (end > D1) & (end <= W.ASOF)
    occ += np.bincount(np.minimum(((months(adm[ev2], end[ev2], clock) + a1) / band).astype(int), nb - 1), minlength=nb)
    HC = Hazard(rate(occ, expo), band)
    return o2, HX, HC, HS


def golden(I, w1=None, weeks=52, how="before", mode="jump", apply1=True, drift=1.0, fit_on="admission", **kw):
    """the canonical forecast: today's residents' survival, direct admissions, and each self-funder's conversion by
    months since admission with deaths and discharges competing, the capital clocks of those in the pool on 6 April 2026
    w1 weeks on, and every clock w2 = w1 x 7,000 / 5,000 weeks on from 5 April 2027"""
    fr = fit(I, **kw)
    o, HX, HC, HS = fr
    m = measure(I, weeks, how, fr)
    if w1 is None:
        w1 = m["w1"]
    if fit_on == "capital":
        o, HX, HC, HS = capital_fit(I, w1, **kw)
    w2 = w1 * RISE2 / RISE1 / drift
    A, n_cf = survivors(I, o, HX)
    C = inflow(direct_rate(I, o), [0.0], o, HX)
    d0, shift, care = pool_clocks(I, o, w1, apply1)
    G = project_members(d0, shift, care, o, HX, HC, HS, w2, mode)
    tot = A + C + G
    if o["post_asof_sf"]:
        tot = tot + post_asof_sf(I, o, HX, HC, HS, w2)
    return dict(total=tot.sum(axis=1), by_care=tot, survivors=A.sum(axis=1), direct=C.sum(axis=1), conversions=G.sum(axis=1),
                n_cf=n_cf, n_sf=int(len(d0)), HX=HX, HC=HC, HS=HS, o=o, w1=w1, w2=w2, measure=m)


def count_pulse(I, o, HX, N):
    """N conversions added on 5 April 2027, each surviving from the months since admission at which the register's
    2024 to 2026 conversions took effect (the median)"""
    m = (I["cf_route"] == "CONV") & (I["cf_entry"] >= W.dn(dt.date(2024, 1, 1))) & (I["cf_entry"] < W.dn(dt.date(2027, 1, 1)))
    dur = float(np.median(months(I["cf_admit"][m], I["cf_entry"][m], o["clock"])))
    qm = qmonths(o["clock"])
    tA = float(months(np.array([W.ASOF]), np.array([D2]), o["clock"])[0])
    return np.array([N * np.exp(-(HX[0].H(np.array([dur + q - tA]))[0] - HX[0].H(np.array([dur]))[0])) if q > tA else 0.0
                     for q in qm])


RECAL = [0.0, 0.0, 0.0, 0.0]


def covariate_conversions(I, o, HX):
    """conversions from today's pool with the self-funders' hazards fitted by care type (the payment lines' FNC lines
    mark nursing), projected as fitted"""
    band, lo, clock = o["band"], o["lo"], o["clock"]
    nb = int(np.ceil(180 / band))
    tot = np.zeros(4)
    for c in (0, 1):
        m = I["sf_care"] == c
        oc, ep = occ_exp(I["sf_admit"][m], I["sf_entry"][m], I["sf_end"][m], (I["sf_reason"] == "CONV")[m], lo, W.ASOF, band, nb, clock)
        HCc = Hazard(rate(oc, ep), band)
        oc2, ep2 = occ_exp(I["sf_admit"][m], I["sf_entry"][m], I["sf_end"][m], (I["sf_reason"] == "EXIT")[m], lo, W.ASOF, band, nb, clock)
        HSc = Hazard(rate(oc2, ep2), band)
        on = pool(I) & m
        d0 = months(I["sf_admit"][on], np.full(on.sum(), W.ASOF), clock)
        tot += project_members(d0, np.zeros(len(d0)), I["sf_care"][on], o, HX, HCc, HSc, 0.0).sum(axis=1)
    return tot


def recalibrated(I, o, HX, base):
    """the hazard fitted to December 2025, scaled by 2026's conversions over the conversions it expected of 2026's
    exposure, then projected"""
    band, lo, clock = o["band"], o["lo"], o["clock"]
    nb = int(np.ceil(180 / band))
    y0 = W.dn(dt.date(2026, 1, 1)) - 1
    conv = I["sf_reason"] == "CONV"
    oth = I["sf_reason"] == "EXIT"
    oc, ep = occ_exp(I["sf_admit"], I["sf_entry"], I["sf_end"], conv, lo, y0, band, nb, clock)
    h25 = rate(oc, ep)
    oc6, ep6 = occ_exp(I["sf_admit"], I["sf_entry"], I["sf_end"], conv, y0, W.ASOF, band, nb, clock)
    k = oc6.sum() / (h25 * ep6).sum()
    HCk = Hazard(h25 * k, band)
    oc2, ep2 = occ_exp(I["sf_admit"], I["sf_entry"], I["sf_end"], oth, lo, W.ASOF, band, nb, clock)
    HS = Hazard(rate(oc2, ep2), band)
    on = pool(I)
    d0 = months(I["sf_admit"][on], np.full(on.sum(), W.ASOF), clock)
    G = project_members(d0, np.zeros(len(d0)), I["sf_care"][on], o, HX, HCk, HS, 0.0).sum(axis=1)
    return base.sum(axis=1) + G, [float(k), float(oc6.sum()), float((h25 * ep6).sum()), 0.0]


def conv_entry_durs(I, a0, a1, o):
    m = (I["cf_route"] == "CONV") & (I["cf_entry"] >= a0) & (I["cf_entry"] < a1)
    return months(I["cf_admit"][m], I["cf_entry"][m], o["clock"]) if o["cf_clock"] == "admission" else np.zeros(m.sum())


def rungs(I, census=None):
    """R0 to R4 and the golden, totals at the four quarter ends"""
    o, HX, HC, HS = fit(I)
    A, _ = survivors(I, o, HX)
    C = inflow(direct_rate(I, o), [0.0], o, HX)
    base = A + C
    out = {}
    d = dt.date
    # R1 and R1b: conversions at their run rate, each entrant at the durations past converters entered at
    for name, (y0, y1) in (("R1", (2024, 2026)), ("R1b", (2025, 2026))):
        a0, a1 = W.dn(d(y0, 1, 1)), W.dn(d(y1 + 1, 1, 1))
        m = (I["cf_route"] == "CONV") & (I["cf_entry"] >= a0) & (I["cf_entry"] < a1)
        mo = (y1 - y0 + 1) * 12
        r = np.array([(m & (I["cf_care"] == c)).sum() / mo for c in (0, 1)])
        durs = conv_entry_durs(I, W.dn(d(2024, 1, 1)), W.dn(d(2027, 1, 1)), o)
        out[name] = (base + inflow(r, durs, o, HX)).sum(axis=1)
    # R2 and R3: a pooled conversion rate per self-funder month times today's pool, the pool depleting
    durs = conv_entry_durs(I, W.dn(d(2024, 1, 1)), W.dn(d(2027, 1, 1)), o)
    on = pool(I)
    pl = np.array([(on & (I["sf_care"] == c)).sum() for c in (0, 1)], float)
    for name, (y0, y1) in (("R2", (2024, 2026)), ("R3", (2022, 2024))):
        L, Hh = W.dn(d(y0, 1, 1)), W.dn(d(y1 + 1, 1, 1))
        s3 = np.maximum(I["sf_entry"], L)
        e3 = np.minimum(I["sf_end"], Hh)
        ok = e3 > s3
        sfm = ((e3 - s3)[ok] / MONTH).sum()
        inwin = (I["sf_end"] > L) & (I["sf_end"] <= Hh)
        rc = (inwin & (I["sf_reason"] == "CONV")).sum() / sfm
        rx = (inwin & (I["sf_reason"] == "EXIT")).sum() / sfm
        qm = qmonths("days")
        res = np.zeros((4, 2))
        for k in range(4):
            n = int(np.ceil(qm[k] / 0.1))
            dt_ = qm[k] / n
            p = pl.copy()
            for j in range(n):
                tin = (j + 0.5) * dt_
                for c in (0, 1):
                    sv = np.mean(np.exp(-(HX[c].H(durs + qm[k] - tin) - HX[c].H(durs))))
                    res[k, c] += p[c] * rc * dt_ * sv
                p = p * np.exp(-(rc + rx) * dt_)
        out[name] = (base + res).sum(axis=1)
    G, _ = project_pool(I, o, HX, HC, HS, True)
    out["R5"] = (base + G).sum(axis=1)
    R4, _ = project_pool(I, o, HX, HC, HS, False)
    out["R4"] = (base + R4).sum(axis=1)
    g = golden(I)
    out["golden"] = g["total"]
    m = g["measure"]
    # R6: the day's conversions of 6 April 2026 again on 5 April 2027; R7: scaled by the rise
    out["R6"] = out["R5"] + count_pulse(I, o, HX, m["on_day"])
    out["R7"] = out["R5"] + count_pulse(I, o, HX, m["on_day"] * RISE2 / RISE1)
    # R8: the clocks' jump converts its stretch but the clocks do not move on; R9: the clocks move on, nobody converts
    # that day; R10: the 2027 jump without the 2026 one on today's pool
    out["R8"] = golden(I, mode="pulse")["total"]
    out["R9"] = golden(I, mode="shift")["total"]
    out["R10"] = golden(I, apply1=False)["total"]
    # R5c: the obvious covariates, the conversion and exit hazards by months since admission fitted for residential and
    # nursing self-funders apart; R5r: the hazard recalibrated to its 2026 back-test (fitted to December 2025, scaled by
    # 2026's conversions against what it expected of 2026's exposure)
    out["R5c"] = base.sum(axis=1) + covariate_conversions(I, o, HX)
    out["R5r"], RECAL[:] = recalibrated(I, o, HX, base)
    if census is not None:
        y = np.asarray(census[-36:], float)
        b, c0 = np.polyfit(np.arange(36), y, 1)
        # month ends after December 2026: June 2027 is month 6 ahead
        out["R0"] = np.array([c0 + b * (35 + k) for k in (6, 9, 12, 15)])
    return out
