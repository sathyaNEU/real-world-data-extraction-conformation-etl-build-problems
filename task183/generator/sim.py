"""task183 simulation: each reviewed customer's trading days, card trade by terminal, cash takings, lodgements
(each carrying the cash of the trading days since the customer's previous lodgement), the two fronts' outside cash,
the till service's daily records, the card settlements and the rest of each account's traffic.

The truth lives here and nowhere in the pack: sim.Truth carries every day's cash and card, every lodgement's own
trading window and its outside part, so checks.py can test the pack's answers against it."""
from __future__ import annotations

import datetime as dt
import math
import random

import world as W


def rng(k):
    return random.Random(W.SEED * 1000 + k)


def lognorm(r, sd):
    return math.exp(r.gauss(0.0, sd) - sd * sd / 2.0)


class Truth:
    def __init__(self):
        self.days = list(W.days(dt.date(2024, 12, 1), W.EXPORT_END))
        self.cust = {}

        # a shared footfall series for the region: a weekly level (weather, pay weeks) and a daily wobble
        r = rng(1)
        self.week_level, self.rain = {}, {}
        lvl = 1.0
        for d in self.days:
            if d.weekday() == 0 or d == self.days[0]:
                lvl = lognorm(r, 0.16)
            self.week_level[d] = lvl
            self.rain[d] = r.random() < 0.38
        for c in W.CUSTOMERS:
            self.cust[c["cid"]] = self._one(c)

    # ------------------------------------------------------------------------------------------------------------
    def _one(self, c):
        r = rng(hash_cid(c["cid"]))
        dow = W.DOW[c["trade"]]
        card, cash, paid_out = {}, {}, {}
        mid_share = [1.0] if c["mids"] == 1 else [round(r.uniform(0.62, 0.78), 2)]
        if c["mids"] == 2:
            mid_share.append(round(1 - mid_share[0], 2))
        own = lognorm(r, 0.10)
        for d in self.days:
            open_today = d.weekday() in c["open_days"] and not (d.month == 12 and d.day in (25, 26))
            if c["trade"] in ("barber", "nails") and d in W.BANK_HOLIDAYS:
                open_today = False
            if not open_today:
                card[d], cash[d], paid_out[d] = 0.0, 0.0, 0.0
                continue
            m = dow[d.weekday()] * self.week_level[d] * lognorm(r, 0.11) * own
            if d.day >= 25 or d.day <= 2:
                m *= 1.08
            if c["trade"] == "carwash" and self.rain[d]:
                m *= 0.62
            if d.month == 12 and 10 <= d.day <= 23 and c["trade"] in ("cafe", "convenience", "takeaway"):
                m *= 1.18
            g = round(c["card_week"] / 7.0 * m, 2)
            card[d] = g
            cash[d] = round(c["k"] * g * lognorm(r, 0.06), 2)       # the cash the day leaves to lodge
            paid_out[d] = round(cash[d] * r.uniform(0.015, 0.04), 2)   # small expenses paid from the till

        # refunds: an occasional card refund on a trading day (reduces that day's card sales)
        refunds = {}
        for d in self.days:
            if card[d] > 0 and r.random() < 0.012:
                refunds[d] = round(min(card[d] * 0.3, r.uniform(6, 60)), 2)

        # lodgement days by habit and channel; a lodgement on day d carries the cash of days prev..d-1
        lod = []
        kind, arg = c["habit"]
        first = dt.date(2024, 12, 2)
        if kind == "days":
            for d in self.days:
                if d < first:
                    continue
                if d.weekday() in arg:
                    dd = d
                    while not lodge_ok(dd, c["channel"]):
                        dd += dt.timedelta(days=1)
                    if not lod or dd > lod[-1]:
                        lod.append(dd)
        else:
            lo, hi = arg
            d = first
            while d <= W.EXPORT_END:
                d = d + dt.timedelta(days=r.randint(lo, hi))
                while not lodge_ok(d, c["channel"]):
                    d += dt.timedelta(days=1)
                if d <= W.EXPORT_END:
                    lod.append(d)
        lodgements = []
        prev = dt.date(2024, 12, 1)
        for d in lod:
            window = [x for x in W.days(prev, d - dt.timedelta(days=1))]
            trade_cash = round(sum(cash[x] for x in window), 2)
            if trade_cash < 20.0:
                continue                      # nothing to lodge: the window runs on to the next lodgement
            out = 0.0
            if c["inj"] > 0:
                out = round(c["inj"] * lognorm(r, 0.06), 2)
            amt = round(trade_cash + out, 2)
            if c["channel"] == "post":
                t = dt.time(9 + r.randint(0, 3), r.randint(0, 59))
            else:
                t = dt.time(9 + r.randint(0, 2), r.choice((35, 38, 41, 44, 47, 50, 52, 55, 58)) if r.random() < 0.3
                            else r.randint(0, 59))
                if t.hour == 9 and t.minute < 30:
                    t = dt.time(9, 30 + t.minute % 30)
            lodgements.append(dict(day=d, time=t, amount=amt, trade_cash=trade_cash, outside=out,
                                   window=(prev, d - dt.timedelta(days=1)), channel=c["channel"],
                                   office=c["office"] if c["channel"] == "post" else ""))
            prev = d
        msc_rate = round(r.uniform(0.0058, 0.0112), 5)
        return dict(card=card, cash=cash, paid_out=paid_out, refunds=refunds, lodgements=lodgements,
                    mid_share=mid_share, msc_rate=msc_rate)


def lodge_ok(d, channel):
    if d in W.BANK_HOLIDAYS:
        return False
    if channel == "branch":
        return d.weekday() < 5
    return d.weekday() < 6          # post offices take business lodgements Monday to Saturday


def hash_cid(cid):
    return int(cid.split("-")[1])


TRUTH = None


def truth():
    global TRUTH
    if TRUTH is None:
        TRUTH = Truth()
    return TRUTH
