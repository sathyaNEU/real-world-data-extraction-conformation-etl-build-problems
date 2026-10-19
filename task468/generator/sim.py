"""The clean truth: every specialty member's therapy (when it began, which product, the days' supply each fill carried,
when each fill was dispensed, when the member stopped), from seven years before the claim files begin to the end of the
program year, and each fill's units. The claim files, the crosswalk and the truth of the program year all come from
here."""
import datetime as dt

import numpy as np
import pandas as pd

import world as W

PROD = pd.DataFrame(W.PRODUCTS, columns=["cls", "product", "labeler", "code", "pack", "units", "price", "share", "pack_long",
                                         "rebate"])
PROD["ndc11"] = PROD["labeler"] + PROD["code"] + PROD["pack"]
END_TRUTH = dt.date(2027, 6, 30)


def rng(k):
    return np.random.default_rng([W.SEED, 7, k])


def first_day(m):
    return W.month_start(m)


def episode(r, c, p, prods, pick, start, ds, mid, fills, ep):
    """One therapy episode from its first fill: fills until the member stops (or the course ends) or the truth ends.
    Returns the stop date, or None if the member is still on therapy at the end of the truth."""
    course = p.get("course")
    n_course = int(r.choice(course)) if course else None
    d, k = start, 0
    while d <= END_TRUTH:
        units = prods.loc[pick, "units"] * (ds // 28 if ds >= 84 else 1)
        if k == 0 and p["load"] > 1:
            units = units * p["load"]
        fills.append((mid, c, int(prods.loc[pick, "index"]), d, ds, float(units), k, start, ep))
        k += 1
        if n_course and k >= n_course:
            return d + dt.timedelta(days=ds)
        t = W.month_index(d) - W.month_index(start)
        h = p["stop"](t)
        if ds >= 84:
            h = 1 - (1 - h) ** 3
        if r.random() < h:
            return d + dt.timedelta(days=ds)
        d = d + dt.timedelta(days=ds - int(r.integers(0, 4)))      # specialty refills ship before the supply runs out
    return None


def restart_date(r, c, stop):
    """When (if ever) a member who stopped comes back to the class: some members in every class return after a lapse of
    at least six months; members of the three step-therapy classes who stopped from 2023 on came back in numbers once
    the January 2026 bulletin removed step therapy."""
    if c == "HCV":
        return None
    m_stop = W.month_index(stop)
    if c in W.STEP_THERAPY_REMOVED and W.RETURN_FROM <= m_stop <= 83 and r.random() < W.RETURN_WAVE[c]:
        m = int(r.integers(84, 90))
        if m - m_stop >= 6:
            return W.month_start(m) + dt.timedelta(days=int(r.integers(0, 28)))
    if r.random() < W.RESTART[c]:
        gap = 6 + int(r.exponential(14))
        return W.month_start(m_stop + gap) + dt.timedelta(days=int(r.integers(0, 28)))
    return None


def simulate(price_scale=None):
    """Return dict(fills, members): fills one row per dispensed fill (member, cls, product row, date, days' supply,
    units, fill number in the episode, episode start, episode number), members one row per episode (id, cls, episode,
    start date, stop date or None)."""
    price_scale = price_scale or {}
    r = rng(1)
    fills, members = [], []
    mid = 0
    for ci, (c, p) in enumerate(W.CLASSES.items()):
        prods = PROD[PROD["cls"] == c].reset_index()
        share = prods["share"].to_numpy() / prods["share"].sum()
        for m in range(-W.PRE_MONTHS, W.N_MONTHS + W.HORIZON):
            for _ in range(int(r.poisson(p["starts"](m)))):
                mid += 1
                pick = int(r.choice(len(prods), p=share))
                opts = p["supply"]
                ds = int(opts[int(r.choice(len(opts), p=[o[1] for o in opts]))][0])
                start = first_day(m) + dt.timedelta(days=int(r.integers(0, 28)))
                ep = 0
                while True:
                    stop = episode(r, c, p, prods, pick, start, ds, mid, fills, ep)
                    members.append((mid, c, ep, start, stop))
                    if stop is None or ep >= 2:
                        break
                    back = restart_date(r, c, stop)
                    if back is None or back > END_TRUTH:
                        break
                    start, ep = back, ep + 1
    f = pd.DataFrame(fills, columns=["member", "cls", "prod", "date", "days", "units", "fill_no", "start", "ep"])
    mem = pd.DataFrame(members, columns=["member", "cls", "ep", "start", "stop"])
    f["price"] = PROD.loc[f["prod"], "price"].to_numpy() * f["cls"].map(lambda c: price_scale.get(c, 1.0)).to_numpy()
    f["paid26"] = (f["units"] * f["price"]).round(2) + W.DISPENSING_FEE
    long_pack = PROD.loc[f["prod"], "pack_long"].to_numpy()
    f["ndc11"] = [PROD.loc[p, "labeler"] + PROD.loc[p, "code"] + (lp if (d >= 84 and isinstance(lp, str)) else PROD.loc[p, "pack"])
                  for p, d, lp in zip(f["prod"], f["days"], long_pack)]
    return dict(fills=f, members=mem)


def cohort(f, day=W.LAST_DAY):
    """Members whose fill in a class covers the day: a fill on or before it whose days' supply reaches it."""
    d = pd.Timestamp(day)
    fd = pd.to_datetime(f["date"])
    cov = (fd <= d) & (fd + pd.to_timedelta(f["days"] - 1, unit="D") >= d)
    return f[cov][["member", "cls"]].drop_duplicates()


def truth_next_year(f, day=W.LAST_DAY):
    """The cohort's paid amount (2026 prices) for its fills in the class over the twelve months after the day."""
    co = cohort(f, day)
    d0 = pd.Timestamp(day)
    d1 = pd.Timestamp(dt.date(day.year + 1, day.month, day.day))
    fd = pd.to_datetime(f["date"])
    win = f[(fd > d0) & (fd <= d1)]
    win = win.merge(co, on=["member", "cls"])
    return win.groupby("cls")["paid26"].sum().reindex(W.CANDIDATES, fill_value=0.0).to_dict()
