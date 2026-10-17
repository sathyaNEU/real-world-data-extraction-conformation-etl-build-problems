"""The analysis on the conformed stop events (bundle.events): each candidate route's average departures in every clock
hour from 6 a.m. to 7 p.m. over the counting days, its stop's unattributed departures shared out by the review's route
mix weighted by its design, the verdicts and the five; the rungs below it; and the asks (Quinnell's record by stop and
month, on-time departures, scheduled waits)."""
import datetime as dt

import numpy as np
import pandas as pd

import world as W

DAYS = W.weekdays()
N = len(DAYS)


def counting(t):
    """The events the standard counts in: counting days, local clock hours 6 to 18, at the five stops."""
    days = set(DAYS)
    m = np.array([d in days for d in t["service_day"]]) & t["hour"].between(6, 18).to_numpy()
    m &= (t["dep"].dt.date == pd.Series(t["service_day"].to_numpy(), index=t.index)).to_numpy()
    return t[m]


def attributed(c):
    """Attributed departures per route and hour, summed over the counting days."""
    a = c[c["attributed"]]
    return a.groupby(["route", "hour"]).size()


def unattributed(c):
    return c[~c["attributed"]].groupby(["stop", "hour"]).size()


def bus_day_unmatched(t):
    """Each bus-day's stop events without a trip at the five stops (the review's frame), by service day."""
    u = t[~t["attributed"]]
    return u.groupby(["bus", "service_day"]).size()


def review_table(t, rv, strict=True):
    """The review log with each reviewed event's design weight: its bus-day's unmatched events over the one reviewed,
    times the month's bus-days listed over those drawn."""
    rv = rv.copy()
    rv["service_day"] = pd.to_datetime(rv["service_date"]).dt.date
    rv["stop"] = rv["stop_code"].map({v[0]: k for k, v in W.STOPS.items()})
    u = bus_day_unmatched(t)
    rv["u"] = [int(u.get((b, d), 0)) for b, d in zip(rv["bus"], rv["service_day"])]
    if strict:
        assert (rv["u"] >= 1).all(), "a reviewed event's bus-day has no unmatched event in the record"
    rv["u"] = rv["u"].clip(lower=1)
    frame = u.reset_index()
    frame["month"] = pd.to_datetime(frame["service_day"]).dt.month
    listed = frame.groupby("month").size()
    drawn = rv.groupby(pd.to_datetime(rv["service_day"]).dt.month).size()
    rv["month"] = pd.to_datetime(rv["service_day"]).dt.month
    rv["w_in"] = rv["u"].astype(float)
    rv["w"] = rv["w_in"] * rv["month"].map(listed / drawn)
    rv["label"] = np.where(rv["route_operated"] == "Not in service", "NIS", rv["route_operated"])
    return rv


def shares(rv, weight="w", by=("stop",)):
    """Each stop's unattributed departures shared among its routes and 'not in service' by the reviewed events."""
    out = {}
    for k, g in rv.groupby(list(by)):
        k = k if isinstance(k, tuple) else (k,)
        if weight is None:
            c = g["label"].value_counts()
        else:
            c = g.groupby("label")[weight].sum()
        out[k] = (c / c.sum()).to_dict()
    return out


def estimate(c, sh, by=("stop",)):
    """Average departures per route and hour: attributed plus the stop's unattributed in that hour by the shares."""
    est = {}
    att = attributed(c)
    for (r, h), v in att.items():
        est[(r, h)] = est.get((r, h), 0.0) + v
    un = c[~c["attributed"]]
    keys = list(by) + ["hour"]
    for k, g in un.groupby(keys):
        p = sh.get(tuple(k[:-1]))
        if p is None:
            continue
        h = k[-1]
        for r, q in p.items():
            if r == "NIS":
                continue
            est[(r, h)] = est.get((r, h), 0.0) + len(g) * q
    return {k: v / N for k, v in est.items()}


def by_band(df):
    return df.assign(band=[W.band(h) for h in df["hour"]])


def lowest(est, route):
    vals = {h: est.get((route, h), 0.0) for h in W.HOURS}
    h = min(vals, key=lambda k: (vals[k], k))
    return vals[h], h


def verdicts(est, ride):
    rows = []
    for r in W.CANDIDATES:
        v, h = lowest(est, r)
        rows.append(dict(route=r, lowest=v, hour=h, meets=v >= W.STANDARD, boardings=ride[r]))
    order = sorted([x for x in rows if x["meets"]], key=lambda x: -x["boardings"])
    five = [x["route"] for x in order[:W.CAP]]
    below = order[W.CAP]["route"] if len(order) > W.CAP else None
    return rows, five, below


def golden(t, rv, strict=True):
    c = counting(t)
    rvw = review_table(t, rv, strict)
    return estimate(c, shares(rvw, "w")), rvw, c


# ---------------------------------------------------------------- the rungs
def matched_only(c):
    return {k: v / N for k, v in attributed(c).items()}


def proportional(c):
    """Each stop-hour's unattributed departures shared in proportion to the routes' attributed ones there."""
    att = attributed(c)
    est = {k: float(v) for k, v in att.items()}
    for (s, h), n in unattributed(c).items():
        rs = W.STOP_ROUTES[s]
        m = {r: att.get((r, h), 0) for r in rs}
        tot = sum(m.values())
        for r in rs:
            est[(r, h)] = est.get((r, h), 0.0) + n * m[r] / tot
    return {k: v / N for k, v in est.items()}


def scheduled(gtfs_minutes_on):
    """The timetable's departures per route and hour averaged over the counting days (the feeds as published)."""
    est = {}
    for d in DAYS:
        for r, m in gtfs_minutes_on(d):
            if m < 1440 and 6 <= m // 60 <= 18:
                est[(r, m // 60)] = est.get((r, m // 60), 0) + 1
    return {k: v / N for k, v in est.items()}


# ---------------------------------------------------------------- the on-time ask
def on_time(c, counts=False, basis="pub"):
    """The share of each candidate's attributed departures (the counting days, 6 a.m. to 7 p.m.) that left no more than
    one minute before and no more than five minutes after the trip's scheduled departure in the feeds ("pub"); with
    basis "sched", against the schedule time each AVL export carries."""
    a = c[c["attributed"]].copy()
    mid = pd.to_datetime(pd.Series(a["service_day"].to_numpy(), index=a.index))
    late = (a["dep"] - mid).dt.total_seconds() - a[basis] * 60.0
    a["ok"] = (late >= W.ON_TIME[0] - 1e-9) & (late <= W.ON_TIME[1] + 1e-9)
    g = a.groupby("route")["ok"]
    if counts:
        return {r: int(g.sum()[r]) for r in W.CANDIDATES}
    return {r: 100.0 * g.mean()[r] for r in W.CANDIDATES}
