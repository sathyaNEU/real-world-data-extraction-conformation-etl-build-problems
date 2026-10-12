"""Every computation the golden, the ladder and the asks need, from the shipped files alone."""
import calendar
import datetime as dt
import json
import math
import os

import numpy as np
import pandas as pd

import pack as P

WIN = (dt.datetime(2026, 8, 3, 0, 0, 0), dt.datetime(2026, 9, 27, 23, 59, 59))
FOUR = ["PAY-01", "FEE-01", "FEE-02", "CRB-01"]
RATE = 27.5
MONTHS = list(range(1, 10))


def r10(x):
    return int(math.floor(x / 10.0 + 0.5) * 10)


def month_end(m):
    return dt.datetime(2026, m, calendar.monthrange(2026, m)[1], 23, 59, 59)


def load(target):
    f = lambda k: os.path.join(target, P.FILES[k])
    B = {}
    reg = pd.read_csv(f("register"), dtype=str, keep_default_na=False)
    reg["opened"] = pd.to_datetime(reg.opened_at)
    reg["closed"] = pd.to_datetime(reg.closed_at.replace("", None))
    B["reg"] = reg
    hist = pd.read_csv(f("history"), dtype=str)
    hist["t"] = pd.to_datetime(hist.event_at)
    B["hist"] = hist
    recs = [json.loads(line) for line in open(f("social"), encoding="utf-8")]
    soc = pd.DataFrame({"post_id": [r["post_id"] for r in recs], "created_at": [r["created_at"] for r in recs],
                        "k": [int(r["search"]["results_returned"]) for r in recs],
                        "basis": [r["account"]["basis"] for r in recs], "ref": [r["account"]["ref"] for r in recs],
                        "verified": [bool(r["dm"]["verified"]) for r in recs], "matter_no": [r["matter_no"] for r in recs]})
    B["social"] = soc
    mer = pd.read_csv(f("meridel"), dtype=str, keep_default_na=False)
    mer["acct"] = "BCF" + mer.acct_no.str[-12:]
    B["meridel"] = mer
    B["affected"] = set(mer.loc[mer.posted_date != "", "acct"])
    B["affected_any"] = set(mer.acct)
    B["portfolio"] = pd.read_csv(f("portfolio"))
    B["time"] = pd.read_csv(f("time"), dtype={"employee_id": str})
    B["marlowby"] = pd.read_csv(f("marlowby"), dtype=str)
    B["treadwell"] = pd.read_excel(f("treadwell"), sheet_name="Hours")
    return B


def portfolio_rate(B, month_end_="2026-04-30", accounts=True):
    pf = B["portfolio"]
    opened = float(pf.loc[pf.month_end == month_end_, "open_accounts"].iloc[0])
    if accounts:
        return len(B["affected"]) / opened
    mer = B["meridel"]
    return float((mer.posted_date != "").sum()) / opened


def window(B, clock="opened", merged=False):
    reg = B["reg"]
    if clock == "opened":
        t = reg.opened
    else:   # the social post's UTC time for social matters
        soc = B["social"].set_index("matter_no")
        utc = pd.to_datetime(soc.created_at.str.replace("Z", "", regex=False))
        t = reg.opened.copy()
        m = reg.matter_no.isin(utc.index)
        t[m] = utc.reindex(reg.matter_no[m]).values
    sel = (t >= WIN[0]) & (t <= WIN[1])
    if not merged:
        sel &= reg.status != "MERGED"
    w = reg[sel].copy()
    soc = B["social"].set_index("matter_no")
    w["k"] = w.matter_no.map(soc.k)
    return w


def frame(B, codes=None, affected=None, **kw):
    """The window's matters with the flags every method needs."""
    w = window(B, **kw)
    codes = codes or FOUR
    aff = B["affected"] if affected is None else affected
    w["four"] = w.problem_code.isin(codes)
    w["o"] = w.account_ref.isin(aff)
    w["nc"] = w.account_basis == "NAME_CITY"
    return w


def shares(B, w=None, b=None):
    """The name-and-city four-code share arising from the failure, by every estimator."""
    w = frame(B) if w is None else w
    nc = w[w.nc & w.four]
    b = portfolio_rate(B) if b is None else b
    k = nc.k.astype(float).values
    o = nc.o.astype(float).values
    one = nc[nc.k == 1]
    s = {"one_match": float(one.o.mean()), "n": len(nc), "n1": len(one)}
    inv_k = 1.0 / k
    s["inversion"] = float((o.sum() - b * (1 - inv_k).sum()) / inv_k.sum())
    A = np.vstack([np.ones_like(inv_k), inv_k]).T
    c = np.linalg.lstsq(A, o, rcond=None)[0]
    s["regression"] = float(c[0] + c[1])
    t = s["one_match"]
    p1 = t * (inv_k + (1 - inv_k) * b) / (t * inv_k + b * (1 - inv_k))
    p0 = t * (1 - inv_k) * (1 - b) / (1 - t * inv_k - b * (1 - inv_k))
    s["posterior"] = float(np.where(o > 0, p1, p0).mean())
    s["attached"] = float(o.mean())
    s["mean_inv_k"] = float(inv_k.mean())
    ver = w[~w.nc & w.four]
    dm = ver[ver.channel == "Social"]
    s["dm_verified"] = float(dm.o.mean())
    s["all_verified"] = float(ver.o.mean())
    one2 = nc[nc.k <= 2]
    s["one_or_two"] = float(one2.o.mean())
    s["all_nc_codes"] = float(w[w.nc].o.mean())
    return s


def base_of(B, method="one_match", w=None, b=None):
    """Sustained base (mean weekly), the failure's matters a week, and the team under a method."""
    w = frame(B) if w is None else w
    N = len(w)
    ver_aff = int((~w.nc & w.four & w.o).sum())
    nc = w[w.nc & w.four]
    s = shares(B, w, b)
    if method == "attached":
        nc_aff = float(nc.o.sum())
    elif method == "all":
        nc_aff = float(len(nc))
    elif method == "share_over_all_codes":
        nc_aff = s["all_nc_codes"] * len(nc)
    else:
        nc_aff = s[method] * len(nc)
    inc = (ver_aff + nc_aff) / 8.0
    base = (N - ver_aff - nc_aff) / 8.0
    return dict(N=N, ver_aff=ver_aff, nc_n=len(nc), nc_aff=nc_aff, incident=inc, base=base,
                team=int(math.ceil(base / RATE - 1e-12)), social_aff=(int((~w.nc & w.four & w.o & (w.channel == "Social")).sum())
                                                                     + nc_aff) / 8.0)


def open_at_month_ends(B, use="history"):
    out = {}
    if use == "history":
        h = B["hist"].sort_values(["matter_no", "t"])
        for m in MONTHS:
            T = month_end(m)
            last = h[h.t <= T].groupby("matter_no").event.last()
            out[m] = int(last.isin(["OPENED", "REOPENED"]).sum())
    elif use == "register":
        reg = B["reg"]
        for m in MONTHS:
            T = month_end(m)
            out[m] = int(((reg.opened <= T) & (reg.closed.isna() | (reg.closed > T))).sum())
    elif use == "reopen_as_new":
        h = B["hist"]
        for m in MONTHS:
            T = month_end(m)
            opens = int(h[(h.t <= T) & h.event.isin(["OPENED", "REOPENED"])].shape[0])
            closes = int(h[(h.t <= T) & h.event.isin(["CLOSED", "MERGED"])].shape[0])
            out[m] = opens - closes + int(h[(h.t <= T) & (h.event == "REOPENED")].shape[0])
    return out


def _clock(s):
    h, m = s.split(":")
    return int(h) * 60 + int(m)


def flex_hours(B, treadwell="clock", other_programs=False, dedupe=True):
    """Flex hours by month: Fenwright overtime on the Bellcroft program, Marlowby's hours, Treadwell's hours."""
    t = B["time"]
    t = t[t.pay_code == "OT"]
    if not other_programs:
        t = t[t.program == "BCF-CMP"]
    ot = t.groupby(pd.to_datetime(t.work_date).dt.month).hours.sum()
    mw = B["marlowby"]
    if dedupe:
        mw = mw.drop_duplicates()
    mh = mw.assign(m=pd.to_datetime(mw.shift_date, format="%m/%d/%Y").dt.month,
                   h=mw.hours.astype(float)).groupby("m").h.sum()
    tw = B["treadwell"]
    if treadwell == "clock":
        mins = tw.End.map(_clock) - tw.Start.map(_clock) - tw["Break (min)"].astype(int)
        th = (mins / 60.0).groupby(pd.to_datetime(tw["Work Date"]).dt.month).sum()
    elif treadwell == "hhmm":
        hrs = tw.Hours.map(lambda x: int(round(x * 100)) // 100 + (int(round(x * 100)) % 100) / 60.0)
        th = hrs.groupby(pd.to_datetime(tw["Work Date"]).dt.month).sum()
    else:   # read as decimal hours
        th = tw.Hours.astype(float).groupby(pd.to_datetime(tw["Work Date"]).dt.month).sum()
    return {m: float(ot.get(m, 0.0) + mh.get(m, 0.0) + th.get(m, 0.0)) for m in MONTHS}
