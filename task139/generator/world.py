"""The book's contracts, each car's odometer path, the claims the cover pays, the cars' resales and the dealers'
remittances.

Each contract's car runs at its own annual mileage from its odometer at sale; covered repairs arrive per mile at a
rate that is flat to 70,000 miles and climbs past it, and each payment (net of the 100 dollar deductible) climbs with
the odometer too; a small part of the claims arrive per month whatever the mileage. The cover ends at 60 months or
75,000 miles from the sale, whichever comes first, or when the car is sold (the contract is then cancelled and
refunded, and some new owners buy a contract of their own on the same car). Everything draws from its own keyed
stream (common.rng)."""
from __future__ import annotations

import datetime as dt

import numpy as np

import common as K

STEP = 7                                 # days in a simulation step


class Contract:
    __slots__ = ("cid", "channel", "dealer", "vin", "cls", "sale", "o0", "rate", "price", "end", "end_reason",
                 "claims", "lien", "sold_on", "first_req", "owner_cancel", "parent", "new_no", "old_no")


def path_odo(c, d):
    """the car's odometer on date d (linear at the contract's own rate)"""
    return c.o0 + c.rate * (d - c.sale).days / 365.25


def cover_end(c):
    """the date the cover would end by time or mileage, whichever comes first"""
    by_time = K.add_months(c.sale, K.TERM_MONTHS)
    by_miles = c.sale + dt.timedelta(days=int(np.ceil(K.LIMIT / c.rate * 365.25)))
    return min(by_time, by_miles)


_TR = dict(zip("ABCDEFGHJKLMNPRSTUVWXYZ", (1, 2, 3, 4, 5, 6, 7, 8, 1, 2, 3, 4, 5, 7, 9, 2, 3, 4, 5, 6, 7, 8, 9)))
_WT = (8, 7, 6, 5, 4, 3, 2, 10, 0, 9, 8, 7, 6, 5, 4, 3, 2)
_YEARS = "DEFGHJKLMN"                        # model years 2013 to 2022


def _vin(r):
    """a well-formed 17-character VIN: maker, five descriptor characters, the check digit, the model year, the plant
    and a six-digit serial, built from the same fourteen draws the stream always made"""
    chars = "ABCDEFGHJKLMNPRSTUVWXYZ0123456789"
    wmi = ["1G1", "1FA", "2T1", "JTD", "1HG", "5YJ", "3VW", "KMH", "1N4", "JM1"][int(r.integers(0, 10))]
    d = [int(r.integers(0, len(chars))) for _ in range(14)]
    body = wmi + "".join(chars[k] for k in d[0:5]) + "0" + _YEARS[d[5] % 10] + chars[d[6]] + \
        "".join(str(k % 10) for k in d[7:13])
    tot = sum((int(ch) if ch.isdigit() else _TR[ch]) * w for ch, w in zip(body, _WT))
    chk = tot % 11
    return body[:8] + ("X" if chk == 10 else str(chk)) + body[9:]


def simulate():
    r = K.rng('contracts')
    rc = K.rng('claims')
    rs = K.rng('resale')
    days_ret = (K.VALUATION - K.RETAIL_START).days
    days_rs = (K.VALUATION - K.RS_START).days
    dealers = ["D%04d" % (1100 + 7 * j) for j in range(64)]
    dw = r.gamma(1.4, 1.0, len(dealers))
    dw = dw / dw.sum()
    C = []
    n = 0

    def new_contract(channel, sale, o0, rate, dealer, vin, cls, parent=None):
        nonlocal n
        n += 1
        c = Contract()
        c.cid, c.channel, c.dealer, c.vin, c.cls = n, channel, dealer, vin, cls
        c.sale, c.o0, c.rate = sale, float(o0), float(rate)
        base = K.base_price(cls, o0)
        if channel == "DEALER" and sale.year < 2026:      # the earlier manuals' prices
            base = round(base * (1 - 0.025 * (2026 - sale.year)), 0)
        c.price = round(base * (1 + K.LOADING), 2) if channel == "FARELINE" else base
        c.claims, c.lien, c.sold_on, c.first_req, c.owner_cancel, c.parent = [], None, None, None, None, parent
        C.append(c)
        return c

    # retail sales through the dealers, 2019 to September 2026, a little more each year
    t = np.sort(r.uniform(0, 1, K.P['n_ret']) ** 0.85 * days_ret)
    for k in range(K.P['n_ret']):
        sale = K.RETAIL_START + dt.timedelta(days=int(t[k]))
        hi = r.random() < K.P['ret_hi_share']
        o0 = r.uniform(*(K.P['ret_hi'] if hi else K.P['o_ret']))
        rate = K.P['ret_rate'] * np.exp(r.normal(0, 0.25))
        cls = K.CLASSES[int(r.choice(3, p=[0.38, 0.42, 0.20]))]
        c = new_contract("DEALER", sale, round(o0), rate, dealers[int(r.choice(len(dealers), p=dw))], _vin(r), cls)
        c.lien = K.BANKS[int(r.integers(0, len(K.BANKS)))] if r.random() < K.P['financed'] else None
    # Fareline drivers from April 2026: older, higher-mileage cars driven about 44,000 miles a year
    t = np.sort(r.uniform(0, days_rs, K.P['n_rs']))
    for k in range(K.P['n_rs']):
        sale = K.RS_START + dt.timedelta(days=int(t[k]))
        o0 = r.uniform(*K.P['o_rs'])
        rate = K.P['rs_rate'] * np.exp(r.normal(0, 0.25))
        cls = K.CLASSES[int(r.choice(3, p=[0.55, 0.38, 0.07]))]
        new_contract("FARELINE", sale, round(o0), rate, "FARELINE", _vin(r), cls)

    # resales: a retail car is sold at a rate of about 9 per cent a year while its cover runs; the contract ends
    # that day and some new owners buy a contract of their own on the same car through a dealer
    i = 0
    while i < len(C):
        c = C[i]
        i += 1
        end = min(cover_end(c), K.VALUATION)
        c.end, c.end_reason = end, ("valuation" if end == K.VALUATION else "expired")
        if c.channel != "DEALER":
            continue
        span = (end - c.sale).days
        u = rs.exponential(365.25 / K.P['cancel_rate'])
        if u < span:
            sold = c.sale + dt.timedelta(days=int(u))
            c.end, c.end_reason, c.sold_on = sold, "sold", sold
            if rs.random() < K.P['recontract'] and sold + dt.timedelta(days=30) < K.VALUATION:
                s2 = sold + dt.timedelta(days=int(rs.integers(3, 28)))
                o2 = path_odo(c, s2)
                if o2 < 125000:
                    n2 = new_contract("DEALER", s2, round(o2), K.P['ret_rate'] * np.exp(rs.normal(0, 0.25)),
                                      dealers[int(rs.choice(len(dealers), p=dw))] if rs.random() < 0.5 else c.dealer,
                                      c.vin, c.cls, parent=c.cid)
                    n2.lien = K.BANKS[int(rs.integers(0, len(K.BANKS)))] if rs.random() < K.P['financed'] else None
                    if n2.lien == c.lien:
                        n2.lien = None

    # claims: per mile at the odometer, plus a small per-month part, until the cover ends
    for c in C:
        d = c.sale
        while d < c.end:
            e = min(d + dt.timedelta(days=STEP), c.end)
            days = (e - d).days
            o_a, o_b = path_odo(c, d), path_odo(c, e)
            o_b = min(o_b, c.o0 + K.LIMIT)
            miles = max(o_b - o_a, 0.0)
            lam = float(K.haz((o_a + o_b) / 2) * miles + K.P['tcomp'] * days / 30.4375)
            for _ in range(rc.poisson(lam)):
                cd = d + dt.timedelta(days=int(rc.integers(0, max(days, 1))))
                co = path_odo(c, cd)
                if co > c.o0 + K.LIMIT:
                    continue
                pay = float(K.sev(co) * np.exp(rc.normal(-K.P['sev_sd'] ** 2 / 2, K.P['sev_sd'])))
                c.claims.append((cd, int(round(co)), round(pay, 2)))
            d = e
    return C


def truth_lifetime(C):
    """the expected claims over a 2027 Fareline contract's whole cover, for contracts like the 2026 sales (each 2026
    Fareline contract's odometer at sale and annual mileage), and the average price; the world's own answer"""
    rs = [c for c in C if c.channel == "FARELINE"]
    tot = []
    for c in rs:
        o, s = c.o0, 0.0
        months = 0
        days = 0
        while months < K.TERM_MONTHS and o < c.o0 + K.LIMIT:
            miles = min(c.rate / 12.0, c.o0 + K.LIMIT - o)
            mid = o + miles / 2
            s += float(K.haz(mid) * miles + K.P['tcomp']) * float(K.sev(mid))
            o += miles
            months += 1
        tot.append(s)
    cost = float(np.mean(tot))
    price = float(np.mean([c.price for c in rs]))
    return dict(cost=cost, price=price, lr=100 * cost / price)
