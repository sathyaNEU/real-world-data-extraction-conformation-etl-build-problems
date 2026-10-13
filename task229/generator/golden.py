"""task229 generator: the golden answers, computed from the shipped files.

The call: each station-month of 2027 on the outlook's flow, shaped inside the day by the operating plan where a plant
peaks, published as the current rating read at the day's mean water level (forward.py's construction), graded under
the standard's sections 3 and 4. Ask A: WY2026 station-days with a water level measured on the day, by month. Ask B:
each station's mean percentage difference of its WY2026 gaugings from the rating in force on the gauging day."""
import os
import re
from datetime import date, datetime, timedelta, timezone

import numpy as np
import pandas as pd

import params as P
import world as W
import forward as FW

LST = timezone(timedelta(hours=P.LST_OFFSET_H))
MONTHS_WY = [(2025, 10), (2025, 11), (2025, 12)] + [(2026, m) for m in range(1, 10)]
MLAB = ["Oct 2025", "Nov 2025", "Dec 2025", "Jan 2026", "Feb 2026", "Mar 2026", "Apr 2026", "May 2026", "Jun 2026",
        "Jul 2026", "Aug 2026", "Sep 2026"]


def load(tgt, F):
    d = pd.read_csv(os.path.join(tgt, F["daily"]), dtype={"station": str, "date": str, "status": str, "platform": str,
                                                          "received_utc": str})
    g = pd.read_csv(os.path.join(tgt, F["gaugings"]), dtype={"gauging_no": str, "station": str, "unit": str,
                                                             "rating": str, "notes": str}, keep_default_na=False)
    reg = pd.read_excel(os.path.join(tgt, F["register"]), sheet_name="Stations", dtype={"replaced_by": str})
    out = pd.read_excel(os.path.join(tgt, F["outlook"]), sheet_name="Outlook 2027", header=4)
    return d, g, reg, out


def chain(reg):
    m = {}
    for _, r in reg.iterrows():
        if isinstance(r.replaced_by, str) and r.replaced_by.strip():
            m[r.station] = r.replaced_by.strip()
    return m


# ---------------------------------------------------------------------------------------------------------- Ask A
def held_mask(d):
    """a row received before the day it covers had ended (a GOES day ends 00:00 UTC the next day; a local
    standard day ends 08:00 UTC the next day)"""
    day = pd.to_datetime(d.date)
    end = day + pd.to_timedelta(np.where(d.platform == "GOES", 24, 32), unit="h")
    rec = pd.to_datetime(d.received_utc.str.replace("Z", ""), format="%Y-%m-%dT%H:%M:%S")
    return (rec < end).values


def ask_a(d, reg):
    ch = chain(reg)
    x = d.copy()
    x["held"] = held_mask(x)
    x = x[(x.date >= P.WY_START.isoformat()) & (x.date <= P.WY_END.isoformat())]
    x["st"] = x.station.map(lambda s: ch.get(s, s))
    meas = x[~x.held].drop_duplicates(["st", "date"])
    meas = meas.assign(ym=meas.date.str[:7])
    out = {}
    for (y, m), lab in zip(MONTHS_WY, MLAB):
        out[lab] = int((meas.ym == "%04d-%02d" % (y, m)).sum())
    return out


# ---------------------------------------------------------------------------------------------------------- Ask B
def fit_rating(h, q):
    """the superseded rating recovered from the record's pairs: Q = C (h - e)^b, e by golden-section search on the
    log-space least squares, C and b by linear regression at each e"""
    h, q = np.asarray(h, float), np.asarray(q, float)
    keep = q > 0
    h, q = h[keep], q[keep]

    def sse(e):
        x = np.log(h - e)
        A = np.c_[np.ones_like(x), x]
        coef, *_ = np.linalg.lstsq(A, np.log(q), rcond=None)
        r = np.log(q) - A @ coef
        return float(r @ r), coef

    lo, hi = h.min() - 2.0, h.min() - 1e-4
    lo = max(lo, -5.0)
    g = (np.sqrt(5) - 1) / 2
    a, b = lo, hi
    c, dd = b - g * (b - a), a + g * (b - a)
    for _ in range(200):
        if sse(c)[0] < sse(dd)[0]:
            b = dd
        else:
            a = c
        c, dd = b - g * (b - a), a + g * (b - a)
    e = (a + b) / 2
    _, coef = sse(e)
    return float(np.exp(coef[0])), float(e), float(coef[1])


def superseded_ratings(d, stations):
    """per site: the rating in force before 1 April 2026 (the 2019 review's), read off every pre-April pair of the
    record, each published discharge being that rating at the day's water level"""
    out = {}
    pre = d[d.date < P.MOVE.isoformat()]
    for s in stations:
        x = pre[pre.station == s].drop_duplicates(["water_level_m", "discharge_m3s"])
        out[s] = fit_rating(x.water_level_m.values, x.discharge_m3s.values)
    return out


def gauging_table(g):
    x = g.copy()
    x["q"] = np.where(x.unit == "L/s", x.discharge / 1000.0, x.discharge)
    t = pd.to_datetime(x.measured_utc.str.replace("Z", ""), format="%Y-%m-%dT%H:%M:%S") + pd.Timedelta(hours=P.LST_OFFSET_H)
    x["day"] = t.dt.date
    agg = x.groupby("gauging_no", as_index=False).agg(station=("station", "first"), day=("day", "first"),
                                                      gh=("gh_m", "first"), q=("q", "sum"))
    return agg


def ask_b(d, g, reg, current):
    """station -> mean percentage difference (unrounded) and the gaugings behind it"""
    ch = chain(reg)
    t = gauging_table(g)
    t = t[(t.day >= P.WY_START) & (t.day <= P.WY_END)].copy()
    sites = sorted(set(t.station))
    old = superseded_ratings(d, [s for s in sites if s != "C122"])
    diffs = []
    for _, r in t.iterrows():
        if r.day < P.MOVE and r.station != "C122":
            par = old[r.station]
        else:
            par = current[r.station]
        qr = float(W.q_of_h(par, r.gh))
        diffs.append(100.0 * (r.q - qr) / qr)
    t["diff"] = diffs
    t["st"] = t.station.map(lambda s: ch.get(s, s))
    out = {}
    for st in W.CURRENT:
        sel = t[t.st == st]
        out[st] = {"mean": float(sel["diff"].mean()), "n": int(len(sel)), "n_pre": int((sel.day < P.MOVE).sum())}
    return out, old


# ---------------------------------------------------------------------------------------------------------- the call
def gauged_tops(GR):
    """the top of each station's gauged range as the rating book prints it"""
    out = {}
    for no, v in GR.items():
        s = ("%#.3g" % v["high"]) if v["high"] < 10 else ("%.1f" % v["high"])
        out[no] = float(s)
    return out


def call(GR):
    tops = gauged_tops(GR)
    sch = FW.schedule(tops)
    first = {no: sch[no][0] for no in W.CURRENT}
    short = {no: sorted(sch[no][1]) for no in W.CURRENT}
    errs = {no: sch[no][2] for no in W.CURRENT}
    return {"first": first, "short": short, "errs": errs, "tops": tops}


def default_path(GR):
    """the default path: each published daily discharge taken as the day's mean flow (error 0), the extrapolation
    rule applied"""
    tops = gauged_tops(GR)
    first, short = {}, {}
    for no in W.CURRENT:
        s = [m for m in range(1, 13) if W.outlook_2027(no, m) > P.EXTRAP * tops[no]]
        short[no] = s
        first[no] = min(s) if s else None
    return {"first": first, "short": short}


def compute(tgt, F, GR):
    d, g, reg, out = load(tgt, F)
    A = ask_a(d, reg)
    cur = {no: W.RATING[no] for no in W.RATING}
    B, old = ask_b(d, g, reg, cur)
    C = call(GR)
    D0 = default_path(GR)
    return {"A": A, "B": B, "old_fit": old, "call": C, "default": D0}


if __name__ == "__main__":
    import sys
    import build as BD
    tgt = sys.argv[1]
    import records as R, truth as T
    TR = T.build_truth()
    G = R.gaugings(TR)
    GR = R.gauged_ranges(G)
    res = compute(tgt, BD.F, GR)
    print("A", res["A"])
    print("B", {k: round(v["mean"], 3) for k, v in res["B"].items()})
    print("first", {k: v for k, v in res["call"]["first"].items() if v})
    print("default", {k: v for k, v in res["default"]["first"].items() if v})
    import pandas as pd
    d, g, reg, out = load(tgt, BD.F)
    Btrue, _ = ask_b(d, g, reg, {no: W.RATING[no] for no in W.RATING})
    tt = gauging_table(g)
    for s, par in res["old_fit"].items():
        sel = tt[(tt.station == s) & (tt.day >= P.WY_START) & (tt.day < P.MOVE)]
        if len(sel):
            e1 = [float(W.q_of_h(par, h) / W.q_of_h(W.OLD_RATING[s], h) - 1) * 100 for h in sel.gh]
            print(s, "max rel error at the pre-April gaugings %.5f pp" % max(abs(x) for x in e1))
