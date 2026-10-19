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


def simulate(price_scale=None):
    """Return dict(fills, members): fills one row per dispensed fill (member, cls, product row, date, days' supply,
    units, fill number, first fill date), members one row per member (id, cls, start date, stop date or None)."""
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
                course = p.get("course")
                n_course = int(r.choice(course)) if course else None
                d, k, stop = start, 0, None
                while d <= END_TRUTH:
                    units = prods.loc[pick, "units"] * (ds // 28 if ds >= 84 else 1)
                    if k == 0 and p["load"] > 1:
                        units = units * p["load"]
                    fills.append((mid, c, int(prods.loc[pick, "index"]), d, ds, float(units), k, start))
                    k += 1
                    if n_course and k >= n_course:
                        stop = d + dt.timedelta(days=ds)
                        break
                    t = W.month_index(d) - W.month_index(start)
                    h = p["stop"](t)
                    if ds >= 84:
                        h = 1 - (1 - h) ** 3
                    if r.random() < h:
                        stop = d + dt.timedelta(days=ds)
                        break
                    d = d + dt.timedelta(days=ds - int(r.integers(0, 4)))      # specialty refills ship before the supply runs out
                members.append((mid, c, start, stop))
    f = pd.DataFrame(fills, columns=["member", "cls", "prod", "date", "days", "units", "fill_no", "start"])
    mem = pd.DataFrame(members, columns=["member", "cls", "start", "stop"])
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
