"""The call and every route to it, computed from the tables the pack ships (the bundle dict records.py builds from
the files as written, so every figure here is the shipped files' arithmetic).

Bundle keys used:
  pin[industry][month]      producer price index, inputs to the industry, 2019 = 100 (one decimal)
  pout[industry][month]     producer price index, outputs of the industry
  pxs[section][month]       export price index by SITC section, 2019 = 100
  pms[section][month]       import price index by SITC section
  stocks[industry][month]   TBS book value of stocks at month end, $m (bulletin for Mar to Jun 2026, portal before)
  ratio[industry][month]    TBS stock-to-sales ratio, months
  xsa[section][month]       TBS exports, seasonally adjusted, $m (bulletin for Apr to Jun 2026, portal before)
  msa[section][month]       TBS imports, seasonally adjusted, $m
  portal_xsa, portal_msa, portal_stocks, portal_ratio: the 24 June pull as it stands
  db[(release, quarter, series)] = value ($m), with releases[release] = (date, type, price basis)
  base[component]           the tracker's March-quarter levels; track[component] its June-quarter estimates
  gdp_q1                    March-quarter GDP, the tracker's base
"""
from __future__ import annotations

import math

import numpy as np

import common as K

MONTHS = K.month_list(K.MONTHS0, K.LAST)


def m_idx(m):
    return MONTHS.index(m)


def rebase(series):
    """A 2019 = 100 index rebased to the 2025 average = 1 (the national accounts' 2025 prices)."""
    yr = [v for k, v in series.items() if k.startswith("2025")]
    avg = sum(yr) / len(yr)
    return {k: v / avg for k, v in series.items()}


def as_array(d):
    """A month-keyed dict as an array over MONTHS (NaN where absent)."""
    return np.array([d.get(m, np.nan) for m in MONTHS])


def window(p, m, T):
    return K.window_avg(p, m, T)


# ---------------------------------------------------------------------------------------------------- inventories
def stock_volume(B, c, m, meth, T=None):
    """An industry's month-end stock at 2025 prices under a revaluation method."""
    p = B["p25"][c]
    b = B["stocks"][c][MONTHS[m]]
    t = B["ratio"][c][MONTHS[m]] if T is None else T
    if meth == "turnover":
        return b / window(p, m, t)
    if meth == "monthend":
        return b / p[m]
    if meth == "qavg":
        return b / np.mean(p[m - 2:m + 1])
    if meth == "wac":
        a = 1.0 / (t + 1.0)
        start = MONTHS.index(K.PRICE0)
        cc = p[start]
        for k in range(start + 1, m + 1):
            cc = a * p[k] + (1 - a) * cc
        return b / cc
    if meth == "midint":
        ts = np.linspace(m + 1 - t, m + 1, 600, endpoint=False) + t / 1200.0
        ok = ~np.isnan(p)
        xs = np.arange(len(p))[ok] + 0.5
        return b / np.interp(ts, xs, p[ok]).mean()
    if meth == "midpoint":
        # the index at the centre of the stockholding period, between the monthly indexes (each at mid-month)
        x = m + 0.5 - t / 2.0
        if x >= m:
            return b / p[m]
        k = int(math.floor(x))
        f = x - k
        return b / (p[k] * (1.0 - f) + p[k + 1] * f)
    if meth == "prevmonth":
        return b / p[m - 1]
    if meth == "lagwindow":
        return b / window(p, m - 1, t)
    if meth == "output":
        return b / B["pout25"][c][m]
    if meth == "nominal":
        return b
    raise ValueError(meth)


def cipi(B, q, meth="turnover", end=None, start=None, T=None, Tfun=None):
    """Business change in inventories in quarter q at 2025 prices, every industry summed; end/start override the
    method at one end; Tfun(c, m) supplies a turnover period."""
    m1 = m_idx(K.quarter_end(q))
    m0 = m1 - 3
    tot = 0.0
    for c in K.IND_CODES:
        t1 = Tfun(c, m1) if Tfun else T
        t0 = Tfun(c, m0) if Tfun else T
        tot += stock_volume(B, c, m1, end or meth, t1) - stock_volume(B, c, m0, start or meth, t0)
    return tot


def cipi_aggregate(B, q):
    m1 = m_idx(K.quarter_end(q))

    def lvl(m):
        bt = sum(B["stocks"][c][MONTHS[m]] for c in K.IND_CODES)
        w = {c: B["stocks"][c][MONTHS[m]] / bt for c in K.IND_CODES}
        pa = sum(w[c] * B["p25"][c] for c in K.IND_CODES)
        ta = sum(w[c] * B["ratio"][c][MONTHS[m]] for c in K.IND_CODES)
        return bt / window(pa, m, ta)
    return lvl(m1) - lvl(m1 - 3)


def cipi_avgstock(B, q):
    m1 = m_idx(K.quarter_end(q))
    m0 = m1 - 3
    return sum(np.mean([stock_volume(B, c, m, "monthend") for m in (m1 - 2, m1 - 1, m1)]) -
               np.mean([stock_volume(B, c, m, "monthend") for m in (m0 - 2, m0 - 1, m0)]) for c in K.IND_CODES)


def cipi_layered(B, q):
    """First in, first out from the flows: each month's purchases (cost of sales plus the change in book value) at
    that month's prices, the latest taken first until the month-end book value is covered."""
    m1 = m_idx(K.quarter_end(q))

    def lvl(c, m):
        st = B["stocks"][c]
        sl = B["sales"][c]
        p = B["p25"][c]
        target, vol, k = st[MONTHS[m]], 0.0, m
        while target > 1e-9:
            purch = st[MONTHS[k]] - st[MONTHS[k - 1]] + sl[MONTHS[k]]
            take = min(purch, target)
            vol += take / p[k]
            target -= take
            k -= 1
        return vol
    return sum(lvl(c, m1) - lvl(c, m1 - 3) for c in K.IND_CODES)


# ---------------------------------------------------------------------------------------------------- goods trade
def goods(B, q, flow, src=None):
    """Goods exports or imports in quarter q at 2025 prices: each SITC section's seasonally adjusted value over its
    price index rebased to 2025."""
    vals = B[src or ("xsa" if flow == "x" else "msa")]
    pr = B["px25" if flow == "x" else "pm25"]
    return sum(vals[s][m] / pr[s][m_idx(m)] for s in K.SITC_CODES for m in K.quarter_months(q))


# ---------------------------------------------------------------------------------------------------- the call
def call(B, cipi_q2, x_q2=None, m_q2=None, cipi_q1=None, gdp_q1=None):
    """The June quarter's growth on the March quarter (per cent) and at an annualised rate: the tracker's lines as
    it carries them, the three lines the bulletin feeds from the bulletin. gdp_q1 replaces the March-quarter GDP the
    bulletin lines are taken over (the tracker's own lines are its contributions as it states them)."""
    base = B["base"]
    g1 = B["gdp_q1"] if gdp_q1 is None else gdp_q1
    contrib = {c: (-1.0 if c == "M_S" else 1.0) * (B["track"][c] - base[c]) / B["gdp_q1"] * 100.0
               for c in B["track"]}
    contrib["X_G"] = ((goods(B, "2026Q2", "x") if x_q2 is None else x_q2) - base["X_G"]) / g1 * 100.0
    contrib["M_G"] = -((goods(B, "2026Q2", "m") if m_q2 is None else m_q2) - base["M_G"]) / g1 * 100.0
    contrib["CIPI_NF"] = (cipi_q2 - (base["CIPI_NF"] if cipi_q1 is None else cipi_q1)) / g1 * 100.0
    q = sum(contrib.values())
    return {"q": q, "ann": K.annualise(q), "contrib": contrib}


def golden(B):
    return call(B, cipi(B, "2026Q2"))


def cipi_holding(B, q, prices="turnover"):
    """The change in book value less the holding gain on the average stock, over the quarter's average index: the
    holding gain at the window prices (prices="turnover") or at the month-end indexes."""
    m1 = m_idx(K.quarter_end(q))
    m0 = m1 - 3
    tot = 0.0
    for c in K.IND_CODES:
        p = B["p25"][c]
        b1, b0 = B["stocks"][c][MONTHS[m1]], B["stocks"][c][MONTHS[m0]]
        if prices == "turnover":
            w1, w0 = window(p, m1, B["ratio"][c][MONTHS[m1]]), window(p, m0, B["ratio"][c][MONTHS[m0]])
        else:
            w1, w0 = p[m1], p[m0]
        gain = 0.5 * (b1 + b0) * (w1 - w0) / (0.5 * (w1 + w0))
        tot += (b1 - b0 - gain) / np.mean(p[m1 - 2:m1 + 1])
    return tot


def cipi_book_change(B, q):
    """The change in book value over the quarter's average index."""
    m1 = m_idx(K.quarter_end(q))
    return sum((B["stocks"][c][MONTHS[m1]] - B["stocks"][c][MONTHS[m1 - 3]]) / np.mean(B["p25"][c][m1 - 2:m1 + 1])
               for c in K.IND_CODES)


def mean_ratio(B, m):
    """The industries' average stock-to-sales ratio at month index m, weighted by their book values."""
    bt = sum(B["stocks"][c][MONTHS[m]] for c in K.IND_CODES)
    return sum(B["stocks"][c][MONTHS[m]] * B["ratio"][c][MONTHS[m]] for c in K.IND_CODES) / bt


def methods(B):
    """Every construction of the change in business inventories the design note names: {name: (kind, f(q))}, kind G
    the golden, C another construction of the revaluation over each stockholding period (the corridor), R a rival."""
    T = lambda c, m: B["ratio"][c][MONTHS[m]]
    return {
        "turnover": ("G", lambda q: cipi(B, q)),
        "quarter-average ratio": ("C", lambda q: cipi(B, q, Tfun=lambda c, m: float(np.mean(
            [T(c, k) for k in (m - 2, m - 1, m)])))),
        "previous month's ratio": ("C", lambda q: cipi(B, q, Tfun=lambda c, m: T(c, m - 1))),
        "whole months": ("C", lambda q: cipi(B, q, Tfun=lambda c, m: max(1.0, float(K.round_half_up(T(c, m)))))),
        "mid-month interpolation": ("C", lambda q: cipi(B, q, "midint")),
        "the index at the period's midpoint": ("C", lambda q: cipi(B, q, "midpoint")),
        "holding gains at the period's prices": ("C", lambda q: cipi_holding(B, q, "turnover")),
        "all industries together": ("C", lambda q: cipi_aggregate(B, q)),
        "the industries' average ratio for every industry": ("C", lambda q: cipi(B, q, Tfun=lambda c, m: mean_ratio(B, m))),
        "first in, first out from the flows": ("C", lambda q: cipi_layered(B, q)),
        "month-end": ("R", lambda q: cipi(B, q, "monthend")),
        "quarter average": ("R", lambda q: cipi(B, q, "qavg")),
        "June end only": ("R", lambda q: cipi(B, q, end="turnover", start="monthend")),
        "March end only": ("R", lambda q: cipi(B, q, end="monthend", start="turnover")),
        "weighted-average cost": ("R", lambda q: cipi(B, q, "wac")),
        "two months for every industry": ("R", lambda q: cipi(B, q, Tfun=lambda c, m: 2.0)),
        "ratios rounded up": ("R", lambda q: cipi(B, q, Tfun=lambda c, m: float(math.ceil(T(c, m))))),
        "ratios rounded down": ("R", lambda q: cipi(B, q, Tfun=lambda c, m: max(1.0, float(math.floor(T(c, m)))))),
        "ratios plus a month": ("R", lambda q: cipi(B, q, Tfun=lambda c, m: T(c, m) + 1.0)),
        "the previous month's index": ("R", lambda q: cipi(B, q, "prevmonth")),
        "the period ending the month before": ("R", lambda q: cipi(B, q, "lagwindow")),
        "average stock over the quarter": ("R", lambda q: cipi_avgstock(B, q)),
        "output price indexes": ("R", lambda q: cipi(B, q, "output")),
        "holding gains at month-end prices": ("R", lambda q: cipi_holding(B, q, "monthend")),
        "the change in book value over the quarter's average index": ("R", lambda q: cipi_book_change(B, q)),
        "book values undeflated": ("R", lambda q: cipi(B, q, "nominal")),
    }


def routes(B):
    """Every route to the call: each construction of business inventories, the March quarter rebuilt the same way,
    and the one-sigma moves of the ratios; {name: (kind, annualised per cent)}."""
    out = {}
    T = lambda c, m: B["ratio"][c][MONTHS[m]]
    for name, (kind, f) in methods(B).items():
        out[name] = (kind, call(B, f("2026Q2"))["ann"])
    out["the March quarter rebuilt the same way"] = ("C", call(B, cipi(B, "2026Q2"), cipi_q1=cipi(B, "2026Q1"))["ann"])
    out["month-end, the March quarter rebuilt the same way"] = (
        "R", call(B, cipi(B, "2026Q2", "monthend"), cipi_q1=cipi(B, "2026Q1", "monthend"))["ann"])
    out["ratios 2 per cent longer"] = ("S", call(B, cipi(B, "2026Q2", Tfun=lambda c, m: T(c, m) * 1.02))["ann"])
    out["ratios 2 per cent shorter"] = ("S", call(B, cipi(B, "2026Q2", Tfun=lambda c, m: T(c, m) * 0.98))["ann"])
    return out


def backtest(B, q0="2019Q2", q1="2026Q1"):
    """Each construction's error against the Office's latest estimate of non-farm business inventories, $m."""
    qs = K.quarter_list(q0, q1)
    off = np.array([B["office_cipi"][q] for q in qs])
    out = {}

    def value(f, q):
        try:
            return f(q)
        except KeyError:            # a construction needing months before the pull's first (2019-01)
            return np.nan
    for name, (kind, f) in methods(B).items():
        e = np.array([value(f, q) for q in qs]) - off
        ok = ~np.isnan(e)
        out[name] = {"kind": kind, "n": int(ok.sum()), "rmse": math.sqrt(float(np.mean(e[ok] ** 2))),
                     "mean": float(e[ok].mean()), "max": float(np.abs(e[ok]).max()), "last": float(e[-1]), "errors": e}
    return out
