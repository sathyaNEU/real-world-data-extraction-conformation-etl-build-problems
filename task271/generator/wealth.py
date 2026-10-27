"""task271 wealth platform: Fenmarsh Wealth's 2026 client orders and Gresmere Stockbrokers' contract notes for the
ones it dealt. Clean truth first; records.py writes the two systems' own views."""
from __future__ import annotations

import datetime as dt
import math

import numpy as np

import common as K
import world as W

POINTS = [(9, 30), (12, 0), (14, 30)]          # dealing points, London time
# shares suspended from trading on these days: Gresmere dealt none of the platform's orders in them
SUSPENDED = {(31, dt.date(2026, 4, 21)), (31, dt.date(2026, 4, 22)), (31, dt.date(2026, 4, 23)),
             (74, dt.date(2026, 8, 12)), (74, dt.date(2026, 8, 13)), (9, dt.date(2026, 2, 10))}
CUTOFF_MIN = 15                                # orders placed before 15 minutes ahead of a point join it
N_ACCOUNTS = 26000
ORDERS_PER_DAY = 430                           # placed on an average day, weekends and holidays included
SPLIT_LIMIT_PCT = 0.35                         # Gresmere dealt a small-cap order above this share of ADV in two parts
CONS_RATIO = 10                                # the consolidation: ten old shares become one new share


def point_label(i):
    h, m = POINTS[i]
    return "%02d:%02d" % (h, m)


GRESMERE_CUTOFF_MIN = 10                       # Gresmere took orders up to ten minutes before a point in 2026


def assign_point(t_utc, cutoff_min=CUTOFF_MIN):
    """The dealing point a client order placed at a UTC instant joins: the first point on a business day whose
    cut-off is after the order's London wall-clock time; after the last cut-off, the next business day's first."""
    off = K.london_offset(t_utc)
    loc = t_utc.replace(tzinfo=None) + dt.timedelta(hours=off)
    d = loc.date()
    secs = loc.hour * 3600 + loc.minute * 60 + loc.second + loc.microsecond / 1e6
    if d.weekday() < 5 and d not in K.BANK_HOLIDAYS:
        for i, (h, m) in enumerate(POINTS):
            if secs < h * 3600 + m * 60 - cutoff_min * 60:
                return d, i
    return K.next_business_day(d), 0


def simulate(stocks, closes):
    rg = K.rng("wealth")
    days_all = []
    d = dt.date(2025, 12, 27)
    while d <= dt.date(2026, 10, 30):
        days_all.append(d)
        d += dt.timedelta(days=1)
    pop = np.array([{"FTSE 100": 3.2, "FTSE 250": 1.5, "Small cap": 0.6}[s["band"]] * math.exp(rg.normal(0, 0.8))
                    for s in stocks])
    cons = stocks[W.CONSOLIDATED_INDEX]
    pop[cons["i"]] = pop.max() * 1.4               # a retail favourite
    pop = pop / pop.sum()
    accounts = ["FW%07d" % int(x) for x in rg.choice(np.arange(1000000, 9999999), N_ACCOUNTS, replace=False)]
    wrapper_of = {a: ("ISA" if r < 0.46 else ("SIPP" if r < 0.71 else "GIA")) for a, r in
                  zip(accounts, rg.random(N_ACCOUNTS))}
    orders = []
    n = 0
    for day in days_all:
        wd = day.weekday()
        scale = 1.0 if wd < 5 else 0.35
        if day in K.BANK_HOLIDAYS:
            scale = 0.45
        k = int(rg.poisson(ORDERS_PER_DAY * scale))
        # London wall-clock placing times: an evening peak and a morning peak
        mix = rg.random(k)
        hrs = np.where(mix < 0.42, rg.normal(8.6, 1.3, k), np.where(mix < 0.75, rg.normal(12.8, 1.8, k),
                                                                   rg.normal(19.5, 2.0, k)))
        hrs = np.clip(hrs, 0.05, 23.95)
        for j in range(k):
            sec = float(hrs[j] * 3600)
            if any(abs(sec - (h * 3600 + m * 60 - CUTOFF_MIN * 60)) < 1.5 for h, m in POINTS):
                sec += 3.0
            loc = dt.datetime(day.year, day.month, day.day) + dt.timedelta(seconds=sec)
            off = 1 if K.BST_START <= (loc - dt.timedelta(hours=1)).replace(tzinfo=K.UTC) < K.BST_END else 0
            t_utc = (loc - dt.timedelta(hours=off)).replace(tzinfo=K.UTC)
            if t_utc.date() > K.DATA_END or t_utc < dt.datetime(2025, 12, 29, 0, 0, tzinfo=K.UTC):
                continue
            s = stocks[int(rg.choice(len(stocks), p=pop))]
            acct = accounts[int(rg.integers(0, N_ACCOUNTS))]
            side = "BUY" if rg.random() < 0.56 else "SELL"
            basis = "VALUE" if (side == "BUY" and rg.random() < 0.34) else "SHARES"
            st = rg.random()
            status = "DEALT" if st < 0.958 else ("CANCELLED" if st < 0.988 else "REJECTED")
            n += 1
            orders.append(dict(ref="WO%08d" % (20000000 + n), account=acct, wrapper=wrapper_of[acct], stock=s["i"],
                               side=side, basis=basis, t_utc=t_utc, status=status,
                               value=float(round(math.exp(rg.normal(math.log(2500), 0.9)) / 10) * 10),
                               shares_req=None))
    # each order's dealing point; a share order's size in the line's own units when it was placed
    for o in orders:
        pd, pi = assign_point(o["t_utc"])
        o["point_day"], o["point"] = pd, pi
        o["g_day"], o["g_point"] = assign_point(o["t_utc"], GRESMERE_CUTOFF_MIN)
        s = stocks[o["stock"]]
        old_line = o["stock"] == cons["i"] and o["t_utc"].date() < W.CONSOLIDATION_DATE
        if o["basis"] == "SHARES":
            px = s["price"] / (CONS_RATIO if old_line else 1)
            q = int(max(1, round(math.exp(rg.normal(math.log(2600), 0.95)) / (px / 100.0))))
            o["shares_req"] = q
        # the platform cancelled every order in the consolidating line still open when the old line closed
        if old_line and min(pd, o["g_day"]) < W.CONSOLIDATION_DATE <= max(pd, o["g_day"]) and o["status"] == "DEALT":
            o["status"] = "CANCELLED"
        elif old_line and pd >= W.CONSOLIDATION_DATE and o["status"] == "DEALT":
            o["status"] = "CANCELLED"
    return orders


def deal(orders, stocks, closes):
    """Gresmere's dealing in 2026: each point's buys and sells in a stock dealt as two market orders at their own
    prices; a small-cap order above the limit dealt half at its point and half at the next."""
    rg = K.rng("gresmere")
    days = K.trading_days(dt.date(2025, 12, 29), dt.date(2026, 11, 3))
    cons = stocks[W.CONSOLIDATED_INDEX]
    notes = []
    point_px = {}

    def px_at(stock, day, pi, side):
        key = (stock, day, pi, side)
        if key in point_px:
            return point_px[key]
        s = stocks[stock]
        base = closes[stock].get(day)
        if base is None:
            prev = [dd for dd in closes[stock] if dd <= day]
            base = closes[stock][max(prev)] if prev else s["price"]
        frac = [0.15, 0.47, 0.76][pi]
        mid = base * math.exp(rg.normal(0, s["vol"] / 1e4 * math.sqrt(frac)))
        if stock == cons["i"] and day < W.CONSOLIDATION_DATE:
            mid = mid / CONS_RATIO
        half = s["spread"] / 2e4 + 0.0004
        p = mid * (1 + half) if side == "BUY" else mid * (1 - half)
        tk = W.tick(mid)
        p = round(round(p / (tk / 4)) * (tk / 4), 4)
        point_px[key] = p
        return p

    seq = 0
    for o in orders:
        if o["status"] != "DEALT" or o["g_day"] > K.DATA_END:
            continue
        if (o["stock"], o["g_day"]) in SUSPENDED:
            o["unfilled"] = True
            continue
        s = stocks[o["stock"]]
        day, pi = o["g_day"], o["g_point"]
        px = px_at(o["stock"], day, pi, o["side"])
        if o["basis"] == "VALUE":
            shares = int(math.floor((o["value"] - 5.95) / (px / 100.0)))
            if shares < 1:
                o["status"] = "REJECTED"
                continue
        else:
            shares = o["shares_req"]
        o["shares"] = shares
        adv_units = s["adv"] * (CONS_RATIO if (o["stock"] == cons["i"] and day < W.CONSOLIDATION_DATE) else 1)
        parts = [(day, pi, shares)]
        if s["band"] == "Small cap" and shares / adv_units * 100 > SPLIT_LIMIT_PCT:
            first = shares // 2
            nd, npi = (day, pi + 1) if pi < 2 else (K.next_business_day(day), 0)
            if nd <= K.DATA_END:
                parts = [(day, pi, first), (nd, npi, shares - first)]
        o["parts"] = parts
        for pday, ppi, q in parts:
            p = px_at(o["stock"], pday, ppi, o["side"])
            seq += 1
            h, m = POINTS[ppi]
            tmin = h * 60 + m + int(rg.integers(1, 9))
            cons_gbp = round(q * p / 100.0, 2)
            comm = 5.95 if (pday, ppi) == (parts[0][0], parts[0][1]) else 0.0
            ptm = 1.50 if cons_gbp > 10000 else 0.0
            sd = round(cons_gbp * 0.005, 2) if o["side"] == "BUY" else 0.0
            notes.append(dict(order=o["ref"], stock=o["stock"], side=o["side"], day=pday, point=ppi,
                              tmin=tmin, shares=q, price=p, consideration=cons_gbp, commission=comm, ptm=ptm,
                              stamp=sd, seq=seq))
    return notes
