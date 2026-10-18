"""task167 records: every fund's deal stream, calls, fees, expenses, realisations, distributions and quarterly NAV,
simulated forward from world.py's clean truth, plus the custodian's euro reference rates. One RNG stream per fund
(seeded by the task number and the fund id), so the records rebuild byte for byte."""
from __future__ import annotations

import datetime as dt
import math

import numpy as np

import world as W

MMAX = 240                       # months of fund life simulated (twenty years)
END_M = W.month_index(dt.date(2027, 1, 1))   # first month after the as-of date


class Flow:
    """One cash item of one fund in one month: kind is invest, fee, offset (a fee offset, negative), expense, org, roc,
    gain, income."""
    __slots__ = ("fund", "month", "day", "kind", "amount")

    def __init__(self, fund, month, day, kind, amount):
        self.fund, self.month, self.day, self.kind, self.amount = fund, month, day, kind, amount


def _hold_years(rng, strategy):
    mu = {"Buyout": 5.0, "Growth equity": 4.6, "Venture capital": 6.5, "Private credit": 3.2}[strategy]
    return float(np.clip(rng.lognormal(math.log(mu), 0.30), 1.2, 11.5))


def _multiple(rng, strategy):
    if strategy == "Venture capital":
        if rng.random() < 0.28:
            return float(rng.uniform(0.0, 0.35))
        return float(rng.lognormal(math.log(2.1), 0.75))
    if strategy == "Private credit":
        return float(np.clip(rng.normal(1.0, 0.03), 0.6, 1.05))
    return float(np.clip(rng.lognormal(math.log(1.9), 0.42), 0.15, 7.0))


def simulate_fund(f, market):
    """Returns (flows, quarterly NAV dict {quarter_end_month: nav}, deals list) in the fund's currency."""
    rng = np.random.default_rng([W.SEED, 7, f.id])
    m0 = W.month_index(f.first_close)
    C = f.commitment
    lam = W.DEALS_PER_YEAR / 12.0
    shape = 1.0 / W.DEAL_CV ** 2
    deals = []          # (deal_month, cost, exit_month, multiple)
    for a in range(0, 12 * 9):
        m = m0 + a
        vol = 0.0
        mu = C * W.deal_rate(a, f.strategy) * f.pace
        if mu > 0:
            n = rng.poisson(lam)
            if n > 0:
                vol = float((mu / lam) * rng.gamma(shape, 1.0 / shape, n).sum())
        if a == 0:
            vol += C * W.SEED_DEAL * f.pace * float(rng.lognormal(-0.02, 0.2))
        if vol <= 0:
            continue
        hold = _hold_years(rng, f.strategy)
        deals.append([m, vol, m + int(round(hold * 12)), _multiple(rng, f.strategy)])
    # calls: steady funds call each deal in the month it closes; line-bridged funds carry first-year deals about a year
    called_inv = {}
    for d in deals:
        a = d[0] - m0
        if f.cls == "line":
            delay = (W.LINE_YEAR1_DELAY + int(rng.integers(0, 2))) if a < 12 else W.LINE_LATER_DELAY
        else:
            delay = 0
        cm = d[0] + delay
        d.append(cm)
        called_inv[cm] = called_inv.get(cm, 0.0) + d[1]
    flows = []
    cum = 0.0
    cap = W.CALL_CAP * C
    for a in range(0, MMAX):
        m = m0 + a
        if m >= END_M + 36:
            break
        day = int(rng.integers(3, 27))
        items = []
        inv = called_inv.get(m, 0.0)
        if inv > 0:
            items.append(("invest", inv))
        if a % 3 == 0:
            fee = 3 * W.fee_rate_month(a, f.strategy) * C
            if fee > 0:
                items.append(("fee", fee))
                # buyout and growth managers set the transaction fees they earned on the last quarter's deals
                # against the quarter's fee
                if f.strategy in ("Buyout", "Growth equity") and a >= 3:
                    tx = sum(d[1] for d in deals if m - 3 <= d[0] < m) * 0.0085
                    if tx > 0.0005:
                        items.append(("offset", -min(tx, 0.9 * fee)))
            if a < 150:
                items.append(("expense", W.EXP_RATE / 4 * C * float(rng.uniform(0.6, 1.4))))
        if a == 0:
            items.append(("org", W.ORG_RATE * C))
        for kind, amt in items:
            if amt > 0:
                amt = min(amt, cap - cum)
                if amt <= 0.0005:
                    continue
            # a portfolio call is a share of commitment to four decimals of a per cent; fees, expenses and the rest to
            # the cent
            amt = round(C * round(amt / C, 6), 8) if kind == "invest" else round(amt, 8)
            cum += amt
            flows.append(Flow(f, m, day, kind, amt))
    # realisations and income
    for d in deals:
        dm, cost, em, mult = d[:4]
        if f.strategy == "Private credit":
            # quarterly interest on the loan, principal back at maturity
            q = dm + 3
            while q < em:
                flows.append(Flow(f, q, int(rng.integers(5, 26)), "income", round(cost * 0.024 * float(rng.uniform(0.9, 1.1)), 8)))
                q += 3
        proceeds = cost * mult * math.exp(0.6 * market.get(em, 0.0))
        rday = int(rng.integers(4, 26))
        if proceeds >= cost:
            flows.append(Flow(f, em, rday, "roc", round(cost, 8)))
            if proceeds - cost > 0.0005:
                flows.append(Flow(f, em, rday, "gain", round(proceeds - cost, 8)))
        elif proceeds > 0.0005:
            flows.append(Flow(f, em, rday, "roc", round(proceeds, 8)))
    # NAV at each month end: unrealised deals at a mark that moves from cost toward the exit value with the market
    # (a line-bridged fund's investors' NAV is net of the facility drawings it has not yet called)
    nav = {}
    for me in range(m0, END_M + 24):
        v = 0.0
        for dm, cost, em, mult, cm in deals:
            if dm <= me < em:
                frac = (me - dm) / max(1, em - dm)
                v += cost * math.exp(math.log(max(mult, 0.05)) * frac * 0.85 + 0.6 * market.get(me, 0.0))
            if dm <= me < cm:
                v -= cost
        nav[me] = v
    return flows, nav, deals


def market_path():
    """a common private-markets valuation factor by month (log), 2006 to 2029"""
    rng = np.random.default_rng([W.SEED, 3])
    x, out = 0.0, {}
    shocks = {W.month_index(dt.date(2008, 10, 1)): -0.25, W.month_index(dt.date(2009, 1, 1)): -0.12,
              W.month_index(dt.date(2020, 3, 1)): -0.12, W.month_index(dt.date(2022, 6, 1)): -0.10}
    for m in range(-12, 12 * 24):
        x = 0.97 * x + rng.normal(0.0, 0.025) + shocks.get(m, 0.0)
        out[m] = x
    return out


# EUR/USD reference rates: monthly anchors (the custodian's month-average levels) with daily movement between them
FX_ANCHORS = [(2006, 1, 1.21), (2006, 12, 1.32), (2007, 12, 1.46), (2008, 7, 1.58), (2008, 11, 1.27), (2009, 6, 1.40),
              (2009, 11, 1.49), (2010, 6, 1.22), (2011, 4, 1.45), (2011, 12, 1.31), (2012, 7, 1.23), (2013, 6, 1.32),
              (2014, 5, 1.39), (2014, 12, 1.23), (2015, 3, 1.08), (2015, 12, 1.09), (2016, 6, 1.12), (2016, 12, 1.05),
              (2017, 9, 1.19), (2018, 2, 1.24), (2018, 11, 1.14), (2019, 9, 1.10), (2020, 3, 1.11), (2020, 12, 1.22),
              (2021, 6, 1.20), (2021, 12, 1.13), (2022, 9, 0.99), (2023, 1, 1.08), (2023, 7, 1.11), (2023, 10, 1.06),
              (2024, 6, 1.08), (2024, 12, 1.05), (2025, 2, 1.04), (2025, 6, 1.15), (2025, 12, 1.17), (2026, 6, 1.14),
              (2026, 12, 1.16)]


def fx_rates():
    """{date: rate} for every business day 2006-01-02 to 2026-12-31 (weekends and US/TARGET holidays skipped)"""
    rng = np.random.default_rng([W.SEED, 5])
    anchors = [(dt.date(y, mo, 15), r) for y, mo, r in FX_ANCHORS]
    d = dt.date(2006, 1, 2)
    out = {}
    noise = 0.0
    while d <= dt.date(2026, 12, 31):
        if d.weekday() < 5 and not _holiday(d):
            # interpolate the anchors in time
            for i in range(len(anchors) - 1):
                if anchors[i][0] <= d <= anchors[i + 1][0] or d < anchors[0][0] or (i == len(anchors) - 2):
                    a0, a1 = anchors[i], anchors[i + 1]
                    break
            t = (d - a0[0]).days / max(1, (a1[0] - a0[0]).days)
            t = min(max(t, 0.0), 1.0 if d <= a1[0] else 1.0 + (d - a1[0]).days / 30.0 * 0.0)
            base = a0[1] + (a1[1] - a0[1]) * t
            noise = 0.93 * noise + rng.normal(0.0, 0.0042)
            out[d] = round(base * (1.0 + noise), 4)
        d += dt.timedelta(days=1)
    return out


def _holiday(d):
    return (d.month, d.day) in ((1, 1), (12, 25), (12, 26))


def all_records():
    funds = W.build_world()
    market = market_path()
    recs = {}
    for f in funds:
        flows, nav, deals = simulate_fund(f, market)
        recs[f.id] = (flows, nav, deals)
    return funds, recs, fx_rates()


if __name__ == "__main__":
    funds, recs, fx = all_records()
    tot = sum(len(r[0]) for r in recs.values())
    print("flows", tot, "fx days", len(fx), "year-end rate", fx[dt.date(2026, 12, 31)])
    for f in funds[:3] + [g for g in funds if g.programme][:3]:
        fl = recs[f.id][0]
        y1 = sum(x.amount for x in fl if x.kind in ("invest", "fee", "expense", "org") and x.month - W.month_index(f.first_close) < 12)
        print(f.name, f.cls, f.commitment, "y1 share %.3f" % (y1 / f.commitment), "flows", len(fl))
