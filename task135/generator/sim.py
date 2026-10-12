"""The market model and the trust's book.

market(): a half-hourly shock model (UTC) from SIM_START with a global factor whose news runs heavier in US hours,
regional factors on their own hours, rates and credit, and a sterling factor. Every price is the latent level at the
moment it is struck: the mandate's shares at the London close (16:30 London), every Kestwick fund at its 12 noon
valuation point from each market's last available price (the North American fund at the previous New York close,
Europe live, Japan at the same day's Tokyo close, gilts and credit live), overseas funds converted at the noon
sterling rate. Index levels are struck at each market's own close in local currency.

book(): the custodian's view of the trust from the window's first valuation: tax lots of the mandate's shares in
two designations, dividends with ex and pay dates (the REITs in two components), corporate actions, cash, the
Kestwick funds' units, the quarter-end rebalancing and the legacy.
"""
import datetime as dt
import math

import numpy as np

import world as W

SLOT = 30                                  # minutes
PER_DAY = 24 * 60 // SLOT

P_DEFAULT = dict(us_early=2.8, us_late=3.2, eu_boost=2.0, as_w=0.8, SG=0.0098, scale=0.93,
                 SR={"UK": 0.0046, "EU": 0.0048, "US": 0.0052, "JP": 0.0064, "RATES": 0.0036, "CREDIT": 0.0012,
                     "FX": 0.0045},
                 BETA={"UK": 0.90, "EU": 1.00, "US": 1.00, "JP": 0.95}, flight=0.10, cb=0.12, fxg=0.0,
                 fxl={"US": 1.0, "EU": 0.75, "JP": 1.0}, weekend=0.2)
DRIFT_KEYS = ("UK", "US", "EU", "JP", "RATES", "CREDIT")


def _slot_range(h0, h1):
    return range(int(h0 * 2), int(h1 * 2))


def profiles(P):
    g = np.ones(PER_DAY)
    for k in _slot_range(7, 16.5):
        g[k] *= P["eu_boost"]
    for k in _slot_range(13.5, 16.5):
        g[k] *= P["us_early"]
    for k in _slot_range(16.5, 21):
        g[k] *= P["us_late"]
    for k in _slot_range(0, 6.5):
        g[k] *= P["as_w"]
    g /= g.sum()

    def reg(h0, h1):
        p = np.full(PER_DAY, 0.15)
        for k in _slot_range(h0, h1):
            p[k] = 3.0
        return p / p.sum()
    fx = np.ones(PER_DAY)
    for k in _slot_range(7, 17):
        fx[k] = 2.0
    for k in _slot_range(13.5, 16):
        fx[k] = 3.0
    return {"G": g, "UK": reg(8, 16.5), "EU": reg(7, 16.5), "US": reg(14.5, 21), "JP": reg(0, 6.5),
            "RATES": np.ones(PER_DAY) / PER_DAY, "CREDIT": reg(8, 16.5), "FX": fx / fx.sum()}


def t0():
    return dt.datetime(W.SIM_START.year, W.SIM_START.month, W.SIM_START.day, tzinfo=dt.timezone.utc)


def slot_of(d, hh, mm, tz):
    """index of the slot boundary at local time hh:mm on date d in zone tz"""
    when = dt.datetime(d.year, d.month, d.day, hh, mm, tzinfo=tz).astimezone(dt.timezone.utc)
    return int((when - t0()).total_seconds() // (SLOT * 60))


def tokyo_close(d):
    return (15, 30) if d >= dt.date(2024, 11, 5) else (15, 0)


def market(seed, P=None, drift=None):
    """drift: {latent key: {(year, month): total log drift}} spread over the month's market hours"""
    P = P or P_DEFAULT
    r = np.random.default_rng(seed)
    end = W.VAL_DATE + dt.timedelta(days=2)
    ndays = (end - W.SIM_START).days
    T = ndays * PER_DAY
    prof = profiles(P)
    dow = np.array([(W.SIM_START + dt.timedelta(days=k)).weekday() for k in range(ndays)])
    wk = np.where(dow >= 5, math.sqrt(P["weekend"]), 1.0)
    scale_day = np.repeat(wk, PER_DAY)

    def shocks(key, sd):
        return r.normal(0, 1, T) * sd * P.get("scale", 1.0) * np.sqrt(np.tile(prof[key], ndays)) * scale_day
    g = shocks("G", P["SG"])
    reg = {k: shocks(k, P["SR"][k]) for k in ("UK", "EU", "US", "JP", "RATES", "CREDIT", "FX")}
    inc = {k: P["BETA"][k] * g + reg[k] for k in ("UK", "EU", "US", "JP")}
    inc["RATES"] = reg["RATES"] - P["flight"] * g * (P["SR"]["RATES"] / P["SG"])
    inc["CREDIT"] = P["cb"] * g + reg["CREDIT"] + 0.6 * reg["RATES"]
    inc["FX"] = reg["FX"] + P["fxg"] * g          # sterling strength (log, pounds per unit of foreign currency inverted)
    for key, by_month in (drift or {}).items():
        pk = prof["G" if key == "RATES" else key]
        for (y, m), amt in by_month.items():
            a = (dt.date(y, m, 1) - W.SIM_START).days
            b = (dt.date(y + (m == 12), m % 12 + 1, 1) - W.SIM_START).days
            if b <= 0 or a >= ndays:
                continue
            seg = np.tile(pk, b - a) * np.repeat(np.where(dow[a:b] >= 5, 0.0, 1.0), PER_DAY)
            inc[key][a * PER_DAY:b * PER_DAY] += amt * seg / seg.sum()
    cum = {k: np.concatenate([[0.0], np.cumsum(v)]) for k, v in inc.items()}

    uk_days = W.bdays(W.SIM_START + dt.timedelta(days=3), W.VAL_DATE, "UK")
    out = {"days": uk_days}
    lv = {k: [] for k in ("UKF", "NAEF", "EUEF", "JPEF", "GILT", "CORP")}
    for d in uk_days:
        noon = slot_of(d, 12, 0, W.LON)
        fxn = cum["FX"][noon]
        lv["UKF"].append(cum["UK"][slot_of(d, 16, 30, W.LON)])
        u = d - dt.timedelta(days=1)
        while not W.is_bday(u, "US"):
            u -= dt.timedelta(days=1)
        lv["NAEF"].append(cum["US"][slot_of(u, 16, 0, W.NYC)] - P["fxl"]["US"] * fxn)
        lv["EUEF"].append(cum["EU"][noon] - P["fxl"]["EU"] * fxn)
        j = d
        while not W.is_bday(j, "JP"):
            j -= dt.timedelta(days=1)
        lv["JPEF"].append(cum["JP"][slot_of(j, *tokyo_close(j), W.TYO)] - P["fxl"]["JP"] * fxn)
        lv["GILT"].append(cum["RATES"][noon])
        lv["CORP"].append(cum["CREDIT"][noon])
    out.update({k: np.array(v) for k, v in lv.items()})
    # index closes, each on its own market's business days, in local currency
    idx = {}
    for name, key, mkt, (hh, mm), tz in (("UK", "UK", "UK", (16, 30), W.LON), ("US", "US", "US", (16, 0), W.NYC),
                                         ("EU", "EU", "UK", (17, 30), dt.timezone(dt.timedelta(hours=1))),
                                         ("JP", "JP", "JP", (15, 30), W.TYO), ("GILT", "RATES", "UK", (16, 15), W.LON),
                                         ("CORP", "CREDIT", "UK", (16, 30), W.LON)):
        days = W.bdays(W.SIM_START + dt.timedelta(days=3), W.VAL_DATE, mkt)
        vals = []
        for d in days:
            if name == "JP":
                vals.append(cum[key][slot_of(d, *tokyo_close(d), tz)])
            elif name == "EU":
                # 17:30 Central European time (an hour ahead of London in winter and summer alike)
                vals.append(cum[key][slot_of(d, 16, 30, W.LON)])
            else:
                vals.append(cum[key][slot_of(d, hh, mm, tz)])
        idx[name] = (days, np.array(vals))
    out["index"] = idx
    return out


# ------------------------------------------------------------------------------------------------ the book

def nth_weekday(y, m, wd, n):
    d = dt.date(y, m, 1)
    while d.weekday() != wd:
        d += dt.timedelta(days=1)
    d += dt.timedelta(days=7 * (n - 1))
    while not W.is_bday(d, "UK"):
        d += dt.timedelta(days=1)
    return d


def last_bday(y, m):
    d = dt.date(y + (m == 12), m % 12 + 1, 1) - dt.timedelta(days=1)
    while not W.is_bday(d, "UK"):
        d -= dt.timedelta(days=1)
    return d


class Book:
    pass


def fund_prices(M, rng):
    """Kestwick's income and accumulation unit prices (pounds, four decimals) and distributions per income unit,
    every UK business day from the market model's start"""
    days = M["days"]
    out = {}
    start_inc = {"NAEF": 3.4126, "EUEF": 2.1873, "JPEF": 1.6542, "GILT": 0.9815, "CORP": 1.1238}
    acc_ratio = {"NAEF": 1.4417, "EUEF": 1.6235, "JPEF": 1.3981, "GILT": 1.8806, "CORP": 2.0412}
    for f in W.FUNDS:
        lvl = M[f]
        tr = np.exp(lvl - lvl[0])
        months = W.FUNDS[f]["months"]
        per_year = len(months)
        exd = set()
        for y in range(days[0].year, days[-1].year + 1):
            for m in months:
                d = nth_weekday(y, m, 0, 1)            # the first Monday (or next business day) of the month
                if days[0] < d <= days[-1]:
                    exd.add(d)
        inc = np.zeros(len(days))
        dist = np.zeros(len(days))
        inc[0] = start_inc[f]
        y0 = W.FUND_YIELD[f]
        for k in range(1, len(days)):
            p = inc[k - 1] * tr[k] / tr[k - 1]
            if days[k] in exd:
                q = round(p * y0 / per_year * (1 + rng.normal(0, 0.05)), 4)
                dist[k] = q
                p -= q
            inc[k] = p
        acc = acc_ratio[f] * start_inc[f] * tr
        out[f] = dict(inc=np.round(inc, 4), acc=np.round(acc, 4), dist=dist, exd=sorted(exd))
    return out


