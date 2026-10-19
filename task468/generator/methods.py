"""The projections, on a conformed record of fills (member, cls, date, days, paid at the 2026 schedule): the golden
development by months on therapy at each member's own duration, and the routes a solver takes instead."""
import datetime as dt

import numpy as np
import pandas as pd

import world as W

CAP = 36          # durations from three years on share one cell
EARLY = dt.date(2019, 3, 31)   # a member first seen by here may have started before the files began


def prepare(f):
    """Add month index, first fill (per member and class, in the record) and whether the start is seen."""
    f = f.copy()
    f["mi"] = [W.month_index(d) for d in f["date"]]
    first = f.groupby(["member", "cls"])["date"].transform("min")
    f["first"] = first
    f["fmi"] = [W.month_index(d) for d in first]
    f["seen_start"] = first > EARLY
    return f


def on_therapy(f, day):
    d = pd.Timestamp(day)
    fd = pd.to_datetime(f["date"])
    cov = (fd <= d) & (fd + pd.to_timedelta(f["days"] - 1, unit="D") >= d)
    return f[cov][["member", "cls"]].drop_duplicates()


def month_end(i):
    s = W.month_start(i + 1)
    return s - dt.timedelta(days=1)


def spend_after(f, members, i, months=W.HORIZON):
    """Each listed (member, cls)'s paid amount over the months after month index i."""
    sub = f[(f["mi"] > i) & (f["mi"] <= i + months)]
    sub = sub.merge(members, on=["member", "cls"])
    return sub.groupby(["member", "cls"])["paid26"].sum()


def development(f, cap=CAP, band=1):
    """For each class and duration T (months since first fill, banded, capped), the mean paid amount over the next twelve
    months of the members on therapy at a month end at that duration, over every month end whose twelve months are in
    the record. Members whose start is not seen sit in the capped cell."""
    out = {}
    last = W.N_MONTHS - 1
    for i in range(0, last - W.HORIZON + 1):
        co = on_therapy(f, month_end(i))
        if co.empty:
            continue
        fm = f.drop_duplicates(["member", "cls"])[["member", "cls", "fmi", "seen_start"]]
        co = co.merge(fm, on=["member", "cls"])
        sp = spend_after(f, co[["member", "cls"]], i)
        co = co.set_index(["member", "cls"])
        co["next"] = sp.reindex(co.index, fill_value=0.0)
        co = co.reset_index()
        co["T"] = np.where(co["seen_start"], np.minimum(i - co["fmi"], cap), cap)
        co["T"] = (co["T"] // band) * band
        for (c, t), g in co.groupby(["cls", "T"]):
            s, n = out.get((c, t), (0.0, 0))
            out[(c, t)] = (s + g["next"].sum(), n + len(g))
    return {k: s / n for k, (s, n) in out.items()}


def golden(f, cap=CAP, band=1):
    """Each class's projected paid amount over the program year for its members on therapy on 30 June 2026."""
    f = prepare(f) if "mi" not in f else f
    dev = development(f, cap, band)
    co = on_therapy(f, W.LAST_DAY)
    fm = f.drop_duplicates(["member", "cls"])[["member", "cls", "fmi", "seen_start"]]
    co = co.merge(fm, on=["member", "cls"])
    last = W.N_MONTHS - 1
    co["T"] = np.where(co["seen_start"], np.minimum(last - co["fmi"], cap), cap)
    co["T"] = (co["T"] // band) * band
    out = {}
    for c in W.CANDIDATES:
        g = co[co["cls"] == c]
        tot = 0.0
        for t in g["T"]:
            key = (c, int(t))
            while key not in dev and key[1] > 0:
                key = (c, key[1] - 1)
            tot += dev.get(key, 0.0)
        out[c] = tot
    return out


def from_start(f):
    """Each current member projected by the class's development from first fill (duration zero)."""
    f = prepare(f) if "mi" not in f else f
    dev = development(f)
    co = on_therapy(f, W.LAST_DAY)
    n = co.groupby("cls").size()
    return {c: float(n.get(c, 0)) * dev.get((c, 0), 0.0) for c in W.CANDIDATES}


def trailing(f):
    f = prepare(f) if "mi" not in f else f
    last = W.N_MONTHS - 1
    s = f[(f["mi"] > last - 12) & (f["mi"] <= last)].groupby("cls")["paid26"].sum()
    return {c: float(s.get(c, 0.0)) for c in W.CANDIDATES}


def run_rate(f):
    f = prepare(f) if "mi" not in f else f
    s = f[f["mi"] == W.N_MONTHS - 1].groupby("cls")["paid26"].sum()
    return {c: 12 * float(s.get(c, 0.0)) for c in W.CANDIDATES}


def analog(f):
    """This June's members times last June's members' following-year paid amount per member."""
    f = prepare(f) if "mi" not in f else f
    i = W.N_MONTHS - 13
    prev = on_therapy(f, month_end(i))
    sp = spend_after(f, prev, i).groupby(level="cls").sum()
    n_prev = prev.groupby("cls").size()
    n_now = on_therapy(f, W.LAST_DAY).groupby("cls").size()
    return {c: float(n_now.get(c, 0)) * float(sp.get(c, 0.0)) / max(int(n_prev.get(c, 0)), 1) for c in W.CANDIDATES}


def pharmacists(spend):
    return {c: int(np.ceil(spend[c] / W.PER_PHARMACIST)) for c in W.CANDIDATES}


def chain(f, cap=CAP):
    """The same development built month to month: the share of the members on therapy at a month end who are still on
    therapy at the next, and their paid amount in that month, by duration, chained over the twelve months."""
    f = prepare(f) if "mi" not in f else f
    last = W.N_MONTHS - 1
    fm = f.drop_duplicates(["member", "cls"])[["member", "cls", "fmi", "seen_start"]]
    paid = f.groupby(["member", "cls", "mi"])["paid26"].sum()
    on = {}
    for i in range(0, last + 1):
        co = on_therapy(f, month_end(i)).merge(fm, on=["member", "cls"])
        co["T"] = np.where(co["seen_start"], np.minimum(i - co["fmi"], cap), cap)
        on[i] = co.set_index(["member", "cls"])
    cell = {}
    for i in range(0, last):
        a, b = on[i], on[i + 1]
        still = a.index.isin(b.index)
        nxt = paid.reindex([(m_, c_, i + 1) for m_, c_ in a.index], fill_value=0.0).to_numpy()
        for (c, t), idx in a.groupby(["cls", "T"]).indices.items():
            s = cell.setdefault((c, int(t)), [0.0, 0, 0.0])
            s[0] += still[idx].sum()
            s[1] += len(idx)
            s[2] += nxt[idx].sum()
    out = {}
    for c in W.CANDIDATES:
        tot = 0.0
        for t in on[last][on[last].index.get_level_values("cls") == c]["T"]:
            surv = 1.0
            for k in range(W.HORIZON):
                s = cell.get((c, min(int(t) + k, cap))) or cell.get((c, cap)) or [1.0, 1, 0.0]
                tot += surv * s[2] / s[1]
                surv *= s[0] / s[1]
        out[c] = tot
    return out
