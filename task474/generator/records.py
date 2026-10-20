"""The records behind the two asks, which the call never reads: the gas supplier's daily invoices for each plant (ask
A, each combined-cycle unit's ozone-season fuel cost) and the outage event report (ask B, each unit's ozone-season
forced outage hours)."""
import datetime as dt

import numpy as np

import sources as S
import world as W

DST = (dt.datetime(2026, 3, 8, 2), dt.datetime(2026, 11, 1, 1))   # local daylight time, in standard-time terms


def local_of(t):
    """A standard-time hour as Central clock time."""
    return t + dt.timedelta(hours=1) if DST[0] <= t < DST[1] else t


def gas_day_of(t):
    """The gas day an hour of burn falls in: 9:00 a.m. to 9:00 a.m. Central clock time, named for its first day."""
    c = local_of(t)
    return (c - dt.timedelta(hours=9)).date()


def build(rng, fleet):
    # the Daily Index ($/MMBtu), published for each trading day, a walk that climbs through the July and August heat;
    # gas traded on a trading day flows on every gas day up to and including the next trading day, so a weekend's or
    # a holiday's gas days take one price, traded the business day before; each delivery point's price is the index
    # plus the transporter's fuel retention on it plus its transportation rate
    days = [dt.date(2026, 1, 1) + dt.timedelta(d) for d in range(368)]
    holidays = {dt.date(2026, 1, 1), dt.date(2026, 1, 19), dt.date(2026, 2, 16), dt.date(2026, 4, 3),
                dt.date(2026, 5, 25), dt.date(2026, 7, 3), dt.date(2026, 9, 7), dt.date(2026, 11, 26),
                dt.date(2026, 12, 25)}
    trading = [d for d in days if d.weekday() < 5 and d not in holidays]
    p, walk = 2.95, {}
    for d in days:
        drift = .022 if d.month in (6, 7) or (d.month == 8 and d.day < 20) else (-.02 if d.month in (8, 9) else -.004)
        p = max(1.6, p + rng.normal(0, .06) + drift)
        walk[d] = p
    trade_of, price, k = {}, {}, 0
    prev = dt.date(2025, 12, 31)
    for d in days:
        while k < len(trading) and trading[k] < d:
            prev = trading[k]
            k += 1
        trade_of[d] = prev
        # a strip spanning a weekend or holiday trades at a discount to the weekday market
        span = (trading[k] - prev).days if k < len(trading) else 1
        price[d] = round(walk.get(prev, 2.95) - (.06 if span > 1 else 0), 4)
    fuel = lambda plant, d: W.FUEL_RETENTION[W.PIPELINE[plant]].get(d.month, W.FUEL_RETENTION[W.PIPELINE[plant]][5])
    adder = W.TRANSPORT
    inv = []
    for plant in list(W.PLANTS) + ["Holt Creek"]:
        units = [u for u in fleet if fleet[u]["plant"] == plant]
        vol = {}
        if plant == "Holt Creek":
            # the coal station takes gas for its auxiliary boiler and for flame stabilisation, every day
            for d in days:
                vol[d] = float(rng.gamma(9.0, 70.0)) * (1.0 if d.month in (5, 6, 7, 8, 9) else 1.6)
            units = []
        # the meter station reads midnight to midnight on its own clock, standard time all year, while the gas is
        # priced by the gas day it flows in
        gas = set(vol) if plant == "Holt Creek" else set()
        for u in units:
            x = fleet[u]
            for h in np.where(x["on"])[0]:
                gas.add(gas_day_of(S.HOURS[h]))
                d = S.HOURS[h].date()
                vol[d] = vol.get(d, 0.0) + float(x["heat"][h])
        # the supplier bills a strip as one line, dated on the strip's last gas day, for the strip's whole quantity
        strips = {}
        for d in sorted(gas | set(vol)):
            if dt.date(2026, 1, 1) <= d <= dt.date(2026, 12, 30):
                strips.setdefault(trade_of[d], []).append(d)
        for t, ds in sorted(strips.items()):
            last = max(dd for dd in days if trade_of[dd] == t and dd <= dt.date(2026, 12, 30))
            dth = round(sum(vol.get(dd, 0.0) for dd in ds), 1)
            pr = round(price[ds[0]] * (1 + fuel(plant, ds[0])) + adder[plant], 4)
            inv.append(dict(plant=plant, gas_day=last, dth=dth, price=pr, amount=round(dth * pr, 2),
                            invoice="%s-%s" % (W.PLANTS.get(plant, ("HC",))[0], last.strftime("%Y%m")), days=ds))
    # forced outage events: full outages (U1 immediate, U2 delayed, U3 postponed) and derates (D1, D2), each with a
    # start and an end; some full outages corrected later were re-reported under a new event number
    ev = []
    num = 260100
    lo, hi = 2860, 6580
    for u in W.CC:
        x = fleet[u]
        on = x["on"]
        offs, runs, h = [], [], lo
        while h < hi:
            k = h
            while k < hi and on[k] == on[h]:
                k += 1
            (runs if on[h] else offs).append((h, k - h))
            h = k
        offs = [o for o in offs if o[1] >= 8 and o[0] > lo]
        pick = [offs[int(i)] for i in rng.choice(len(offs), size=min(int(rng.integers(5, 10)), len(offs)), replace=False)]
        for h0, span in pick:
            dur = min(span, int(rng.choice([6, 11, 19, 27, 40, 63, 95, 140])) + int(rng.integers(0, 6)))
            num += int(rng.integers(1, 40))
            ev.append(dict(unit=u, event=num, type=str(rng.choice(["U1", "U1", "U2", "U3"])),
                           start=local_of(S.HOURS[h0]), end=local_of(S.HOURS[h0]) + dt.timedelta(hours=dur),
                           cause=int(rng.choice([4000, 4010, 4260, 4511, 5245, 7300, 7310, 9130])), rev=0))
        runs = [r for r in runs if r[1] >= 6]
        for i in rng.choice(len(runs), size=min(int(rng.integers(2, 6)), len(runs)), replace=False):
            h0, span = runs[int(i)]
            # a derate found in a run (a burner, a feedwater pump) stays on the unit until it is repaired, often past
            # the shutdown and into the hours the unit then stands in reserve
            dur = int(rng.integers(3, span + 1)) + (int(rng.integers(6, 60)) if rng.random() < .55 else 0)
            num += int(rng.integers(1, 40))
            ev.append(dict(unit=u, event=num, type=str(rng.choice(["D1", "D2"])), start=local_of(S.HOURS[h0]),
                           end=local_of(S.HOURS[h0]) + dt.timedelta(hours=dur), cause=int(rng.choice([3410, 4600, 4810])),
                           rev=0, derate=int(round(int(rng.integers(20, 90)) * W.DERATE_SCALE))))
    # re-reports: an outage whose times and cause were corrected after the quarter closed is reported again under a
    # new event number with the corrected start and end; the original stays in the report
    full = [e for e in ev if e["type"] in ("U1", "U2", "U3")]
    for u in W.CC:
        mine = sorted([e for e in full if e["unit"] == u and e["end"] < dt.datetime(2026, 8, 20)
                       and (e["end"] - e["start"]).total_seconds() >= 8 * 3600], key=lambda e: e["start"])
        k = 1 + int(rng.random() < .5)
        for e in [mine[int(i)] for i in rng.choice(len(mine), size=min(k, len(mine)), replace=False)]:
            num += int(rng.integers(1, 40))
            s0 = int(rng.choice([-3, -2, -1, 1, 2]))
            s1 = int(rng.choice([-5, -3, -2, 2, 3, 4, 7]))
            ev.append(dict(e, event=num, cause=int(rng.choice([4010, 4260, 7310])), rev=0, dup=True,
                           start=e["start"] + dt.timedelta(hours=s0), end=e["end"] + dt.timedelta(hours=s1)))
    # event numbers run in the order the reports were filed: a few days after an event ends, a correction weeks later
    for e in ev:
        lag = int(rng.integers(30, 55)) if e.get("dup") else int(rng.integers(1, 10))
        e["filed"] = (e["end"] + dt.timedelta(days=lag)).date()
    for e in ev:
        if e.get("swapped"):
            e["filed"] = (e["end"] + dt.timedelta(days=int(rng.integers(1, 8)))).date()
    num = 260100
    for e in sorted(ev, key=lambda e: (e["filed"], e["start"], e["unit"])):
        num += int(rng.integers(1, 9))
        e["event"] = num
    # revisions: an event reviewed after the quarter closed and found to have been planned work deferred, not a
    # failure, is reported again under its own event number as a maintenance outage (MO) or derate (D4); the event
    # report keeps every revision it was sent
    rv = np.random.default_rng(W.SEED + 2000)
    for u in W.CC:
        mine = [e for e in ev if e["unit"] == u and e["type"] in ("U1", "U2", "U3") and not e.get("dup")
                and W.SEASON[0] <= e["start"].date() and e["end"] < dt.datetime(2026, 8, 25)
                and not any(f is not e and f["unit"] == u and f["start"] < e["end"] and e["start"] < f["end"]
                            for f in ev if f["type"] in ("U1", "U2", "U3"))]
        if mine:
            e = mine[int(rv.integers(0, len(mine)))]
            ev.append(dict(e, type="MO", filed=e["filed"] + dt.timedelta(days=int(rv.integers(20, 46))),
                           revision=True))
        ders = [e for e in ev if e["unit"] == u and e["type"] in ("D1", "D2") and not e.get("revision")
                and e["end"] < dt.datetime(2026, 8, 25)]
        if ders and rv.random() < .6:
            e = ders[int(rv.integers(0, len(ders)))]
            ev.append(dict(e, type="D4", filed=e["filed"] + dt.timedelta(days=int(rv.integers(20, 46))),
                           revision=True))
    ev.sort(key=lambda e: (e["start"], e["unit"], e["filed"]))
    return dict(price=price, invoices=inv, events=ev)
