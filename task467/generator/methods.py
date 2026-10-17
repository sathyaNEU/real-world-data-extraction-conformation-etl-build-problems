"""The analysis, on a conformed counts table (date, dir, zone, n: trips by local start date, direction and city zone;
voided trips and copies out): the base year's fee-liable pickups, the rank's effect read three ways, the
restatement, the fee and its flip, and the asks' brokerage ledger on conformed trip rows."""
import datetime as dt
import math

import numpy as np
import pandas as pd

import world as W

PRE = (dt.date(2023, 11, 4), dt.date(2024, 11, 3))     # the twelve months before the rank moved
BASE = (dt.date(2025, 1, 1), dt.date(2025, 12, 31))    # the base year


def counts_from_trips(t):
    """Trip rows (dir, zone, meter_on local) to the counts table."""
    d = pd.to_datetime(t["meter_on"]).to_numpy().astype("datetime64[D]")
    c = pd.DataFrame({"date": d, "dir": t["dir"].to_numpy(), "zone": t["zone"].to_numpy(), "n": 1})
    return c.groupby(["date", "dir", "zone"], as_index=False)["n"].sum()


def n(c, window, direction, zones=None):
    a, b = (np.datetime64(w) for w in window)
    m = (c["date"].to_numpy() >= a) & (c["date"].to_numpy() <= b) & (c["dir"].to_numpy() == direction)
    if zones is not None:
        m &= np.isin(c["zone"].to_numpy(), zones)
    return int(c["n"].to_numpy()[m].sum())


def recorded(c):
    """2025's fee-liable pickups as the Office's final file records them."""
    return n(c, BASE, "P")


def share_kept(c, zones, pre=PRE, post=BASE):
    """Pickups' change against drop-offs' change in a set of zones: the share of pickups the rank left."""
    return (n(c, post, "P", zones) / n(c, pre, "P", zones)) / (n(c, post, "D", zones) / n(c, pre, "D", zones))


def strata():
    return {"station": W.STATION_ZONES, "other": W.OTHER_ZONES}


def restated(c, pre=PRE, post=BASE, groups=None):
    """The golden restatement: each stratum's 2025 drop-offs at its own pre-move ratio of pickups to drop-offs, summed
    (the pickups 2025 would have had with taxis at the forecourt rank)."""
    groups = groups or strata()
    return sum(n(c, post, "D", zs) * n(c, pre, "P", zs) / n(c, pre, "D", zs) for zs in groups.values())


def restated_by_zone(c, pre=PRE, post=BASE, floor=30):
    """The same counterfactual zone by zone (a zone with fewer than `floor` pre-move drop-offs takes its stratum's
    ratio)."""
    tot = 0.0
    for zs in strata().values():
        ratio = n(c, pre, "P", zs) / n(c, pre, "D", zs)
        for z in zs:
            p_, d_ = n(c, pre, "P", [z]), n(c, pre, "D", [z])
            tot += n(c, post, "D", [z]) * (p_ / d_ if d_ >= floor else ratio)
    return tot


def share_cost(c):
    """The share of pickups the temporary rank cost: 1 less the recorded over the restated pickups."""
    return 1 - recorded(c) / restated(c)


def rung0(c):
    """The default path: 2025 restated by the pickups' own fall between the twelve months before the move and 2025."""
    a = recorded(c)
    return a / (a / n(c, PRE, "P"))


def rung1(c):
    """The obvious correction: all pickups against all drop-offs."""
    return recorded(c) / share_kept(c, W.CITY_ZONES)


def fee_for(amount, pickups):
    """By-law s.4: the lowest multiple of 25 cents at which the pickups at the fee are not less than the amount."""
    k = math.ceil(amount / pickups / W.FEE_STEP - 1e-12)
    while (k - 1) * W.FEE_STEP * pickups >= amount:
        k -= 1
    while k * W.FEE_STEP * pickups < amount:
        k += 1
    return round(k * W.FEE_STEP, 2)


def flip(recorded_pickups, amount, fee):
    """The shares of pickups the rank cost between which the fee stays where it is (restated = recorded / (1 - share)):
    at or above `lo` the fee recovers the amount, below `hi` one step down still falls short."""
    lo = 1 - recorded_pickups * fee / amount
    hi = 1 - recorded_pickups * (fee - W.FEE_STEP) / amount
    return lo, hi


def settings(amount, pickups):
    return [dict(fee=round(f, 2), revenue=f * pickups, recovers=f * pickups >= amount, surplus=f * pickups - amount)
            for f in W.MENU]


def round_to(x, unit):
    return int(math.floor(x / unit + 0.5)) * unit


# ---------------------------------------------------------------- the asks: the brokerage ledger
def ledger(p):
    """Fee-liable pickups and fees owed by local month and brokerage (at the trip's start), from conformed pickup rows
    with columns meter_on (local) and brokerage."""
    on = pd.to_datetime(p["meter_on"])
    g = pd.DataFrame({"month": on.dt.strftime("%Y-%m"), "brokerage": p["brokerage"].astype(int).to_numpy()})
    g = g.groupby(["month", "brokerage"]).size().reset_index(name="pickups")
    g["owed"] = [round(k * W.FEES[int(m[:4])], 2) for m, k in zip(g["month"], g["pickups"])]
    return g.sort_values(["month", "brokerage"]).reset_index(drop=True)
