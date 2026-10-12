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


def post_asof_sf(I, o, HX, HC, HS):
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
            # an entrant at tin converts by quarter end with the competing-risk probability, then survives
            s, t, acc = 1.0, 0.0, np.zeros(2)
            while t < qm[k] - tin - 1e-9:
                hh = min(0.25, qm[k] - tin - t)
                lc, lx = float(HC.at(np.array([t]))[0]), float(HS.at(np.array([t]))[0])
                tot = lc + lx
                p = s * (lc / tot) * (1 - np.exp(-tot * hh)) if tot > 0 else 0.0
                for c in (0, 1):
                    acc[c] += p * np.exp(-(HX[c].H(np.array([qm[k] - tin]))[0] - HX[c].H(np.array([t + hh / 2]))[0]))
                s *= np.exp(-tot * hh)
                t += hh
            out[k] += r * dt_ * acc
    return out


def golden(I, **kw):
    o, HX, HC, HS = fit(I, **kw)
    A, n_cf = survivors(I, o, HX)
    C = inflow(direct_rate(I, o), [0.0], o, HX)
    G, n_sf = project_pool(I, o, HX, HC, HS, True)
    tot = A + C + G
    if o["post_asof_sf"]:
        tot = tot + post_asof_sf(I, o, HX, HC, HS)
    return dict(total=tot.sum(axis=1), by_care=tot, survivors=A.sum(axis=1), direct=C.sum(axis=1), conversions=G.sum(axis=1),
                n_cf=n_cf, n_sf=n_sf, HX=HX, HC=HC, HS=HS, o=o)


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
    out["golden"] = (base + G).sum(axis=1)
    R4, _ = project_pool(I, o, HX, HC, HS, False)
    out["R4"] = (base + R4).sum(axis=1)
    if census is not None:
        y = np.asarray(census[-36:], float)
        b, c0 = np.polyfit(np.arange(36), y, 1)
        # month ends after December 2026: June 2027 is month 6 ahead
        out["R0"] = np.array([c0 + b * (35 + k) for k in (6, 9, 12, 15)])
    return out
