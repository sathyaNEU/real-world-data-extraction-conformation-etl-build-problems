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
    # daily index price ($/MMBtu) with a weekly pattern and spells, plus each plant's fixed adder
    days = [dt.date(2026, 1, 1) + dt.timedelta(d) for d in range(366)]
    p, price = 3.10, {}
    for d in days:
        p = max(1.6, p + rng.normal(0, .07) + (.03 if d.month in (7, 8) else -.005))
        price[d] = round(p + (.18 if d.weekday() == 0 else 0), 4)
    adder = {"Cutler Bend": .214, "Ashfork": .187, "Dunmore Flats": .231, "Sable Ridge": .196, "Holt Creek": .0}
    inv = []
    for plant in W.PLANTS:
        units = [u for u in fleet if fleet[u]["plant"] == plant]
        vol = {}
        for u in units:
            x = fleet[u]
            for h in np.where(x["on"])[0]:
                gd = gas_day_of(S.HOURS[h])
                vol[gd] = vol.get(gd, 0.0) + float(x["heat"][h])
        for d in sorted(vol):
            if not (dt.date(2026, 1, 1) <= d <= dt.date(2026, 12, 30)):
                continue
            dth = round(vol[d], 1)
            pr = round(price[d] + adder[plant], 4)
            inv.append(dict(plant=plant, gas_day=d, dth=dth, price=pr, amount=round(dth * pr, 2),
                            invoice="%s-%s" % (W.PLANTS[plant][0], d.strftime("%Y%m"))))
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
        pick = [offs[int(i)] for i in rng.choice(len(offs), size=min(int(rng.integers(3, 8)), len(offs)), replace=False)]
        for h0, span in pick:
            dur = min(span, int(rng.choice([6, 11, 19, 27, 40, 63, 95, 140])) + int(rng.integers(0, 6)))
            num += int(rng.integers(1, 40))
            ev.append(dict(unit=u, event=num, type=str(rng.choice(["U1", "U1", "U2", "U3"])),
                           start=local_of(S.HOURS[h0]), end=local_of(S.HOURS[h0]) + dt.timedelta(hours=dur),
                           cause=int(rng.choice([4000, 4010, 4260, 4511, 5245, 7300, 7310, 9130])), rev=0))
        runs = [r for r in runs if r[1] >= 6]
        for i in rng.choice(len(runs), size=min(int(rng.integers(2, 6)), len(runs)), replace=False):
            h0, span = runs[int(i)]
            dur = int(rng.integers(3, span + 1))
            num += int(rng.integers(1, 40))
            ev.append(dict(unit=u, event=num, type=str(rng.choice(["D1", "D2"])), start=local_of(S.HOURS[h0]),
                           end=local_of(S.HOURS[h0]) + dt.timedelta(hours=dur), cause=int(rng.choice([3410, 4600, 4810])),
                           rev=0, derate=int(rng.integers(20, 90))))
    # re-reports: a full outage whose cause was corrected after the quarter closed is reported again in full under a
    # new event number; the original stays in the report
    full = [e for e in ev if e["type"] in ("U1", "U2", "U3")]
    for u in W.CC:
        mine = [e for e in full if e["unit"] == u and e["end"] < dt.datetime(2026, 8, 20)]
        for e in [mine[int(i)] for i in rng.choice(len(mine), size=min(2, len(mine)), replace=False)][:1 + (u < "D")]:
            num += int(rng.integers(1, 40))
            shift = int(rng.choice([-5, -3, -2, 2, 3, 4, 7]))
            ev.append(dict(e, event=num, cause=int(rng.choice([4010, 4260, 7310])), rev=0, dup=True,
                           end=e["end"] + dt.timedelta(hours=shift)))
    # event numbers run in the order the reports were filed: a few days after an event ends, a correction weeks later
    for e in ev:
        lag = int(rng.integers(35, 80)) if e.get("dup") else int(rng.integers(1, 10))
        e["filed"] = (e["end"] + dt.timedelta(days=lag)).date()
    num = 260100
    for e in sorted(ev, key=lambda e: (e["filed"], e["start"], e["unit"])):
        num += int(rng.integers(1, 9))
        e["event"] = num
    ev.sort(key=lambda e: (e["start"], e["unit"]))
    return dict(price=price, invoices=inv, events=ev)
