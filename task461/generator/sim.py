"""The building as it ran: every circuit's half-hourly load, the revenue meter's import, the BMS registers, the June
isolations, the generator's runs, deliveries and stock, the chillers' refrigerant movements and the weather. Every
quantity is a true physical one; pack.py writes each system's record of it."""
import datetime as dt
import math

import numpy as np

import world as W

D = dt.timedelta
HH = D(minutes=30)


def half_hours():
    n = int((W.SIM_END_UTC - W.SIM_START_UTC) / HH)
    return [W.SIM_START_UTC + i * HH for i in range(n + 1)]


def weather(rng):
    days = {}
    d = dt.date(2025, 12, 28)
    prev = 0.0
    while d <= dt.date(2027, 1, 5):
        doy = d.timetuple().tm_yday
        prev = 0.62 * prev + rng.normal(0, 1.6)
        mean = 10.6 - 6.1 * math.cos(2 * math.pi * (doy - 18) / 365.0) + prev
        rng_ = 6.5 + 2.5 * math.sin(2 * math.pi * (doy - 80) / 365.0) + rng.normal(0, 1.1)
        days[d] = dict(tmean=mean, tmax=mean + rng_ / 2, tmin=mean - rng_ / 2,
                       rain=0.0 if rng.random() < 0.52 else round(float(rng.gamma(0.9, 4.2)), 1))
        d += D(days=1)
    return days


def occupancy(local):
    """Share of an office floor's daytime load in use at this local half-hour."""
    day = local.date()
    if day in W.BANK_HOLIDAYS or local.weekday() == 6:
        return 0.0
    h = local.hour + local.minute / 60.0
    if day in (dt.date(2026, 12, 24), dt.date(2026, 12, 29), dt.date(2026, 12, 30), dt.date(2026, 12, 31)):
        return 0.3 * min(1.0, max(0.0, (local.hour - 8) / 2.0)) if 8 <= local.hour < 16 else 0.0
    if local.weekday() == 5:
        return 0.12 if 9 <= h < 13 else 0.0
    if h < 6.5 or h >= 20:
        return 0.0
    if h < 9:
        return (h - 6.5) / 2.5
    if h < 17:
        return 1.0
    return max(0.0, (20 - h) / 3.0)


def simulate(seed=None):
    rng = np.random.default_rng(W.SEED if seed is None else seed)
    wx = weather(rng)
    ts = half_hours()
    n = len(ts)
    loc = [W.to_local(t) for t in ts]
    occ = np.array([occupancy(l) for l in loc])
    temp = np.array([wx[l.date()]["tmean"] + 3.2 * math.sin(2 * math.pi * (l.hour + l.minute / 60 - 9) / 24)
                     for l in loc])
    season = np.array([math.cos(2 * math.pi * (l.timetuple().tm_yday - 15) / 365.0) for l in loc])
    kw = {}
    # tenancies: an office load, and the comms rooms fitted inside three of them
    for tag, desc, occ_name, kind, parent in W.METERS:
        if kind != "supply" or tag in ("EM-114", "EM-118"):
            continue
        t = W.TENANTS[occ_name]
        dayf = np.repeat(rng.normal(1.0, 0.06, size=n // 48 + 2), 48)[:n]
        kw[tag] = (t["night"] + (t["peak"] - t["night"]) * occ * dayf * (1 + 0.05 * season)
                   + rng.normal(0, 0.35, n)).clip(0.4)
    steps = {"EM-102": [(dt.datetime(2026, 10, 6, 1, 30), 0.9)], "EM-105": [(dt.datetime(2026, 3, 3, 1, 30), 2.1)],
             "EM-108": [(dt.datetime(2026, 8, 19, 2, 0), -1.3)]}
    for tag, base in W.ROOM_KW.items():
        x = base * (1 + 0.025 * season) + rng.normal(0, 0.12, n)
        for when, dk in steps[tag]:
            x = x + np.array([dk if l >= when else 0.0 for l in loc])
        kw[tag] = x.clip(0.5)
        kw[W.NESTED[tag]] = kw[W.NESTED[tag]] + kw[tag]           # the room is wired inside its tenancy's supply
    car = W.CARRIER_KW - 1.2 * season + rng.normal(0, 0.2, n)
    for when, dk in ((dt.datetime(2026, 6, 2, 2, 0), 3.2), (dt.datetime(2026, 11, 10, 1, 0), 1.1)):
        car = car + np.array([dk if l >= when else 0.0 for l in loc])
    kw["EM-114"] = car.clip(1.0)
    # base building
    cool = (temp - 13.5).clip(0)
    occd = (occ > 0).astype(float)
    kw["EM-201"] = (44.0 + 96.0 * occd + (14.5 * occd + 5.2) * cool + 21.0 * (season > 0.4) * (1 - occd * 0.5)
                    + rng.normal(0, 1.2, n)).clip(4.0)
    kw["EM-202"] = (6.2 + 27.5 * occ + rng.normal(0, 1.1, n)).clip(1.0)
    kw["EM-203"] = (29.5 + 18.5 * occ + rng.normal(0, 0.8, n)).clip(5.0)
    dark = np.array([1.0 if (l.hour >= 17 or l.hour < 7) else 0.0 for l in loc])
    kw["EM-204"] = (8.8 + 6.1 * occ + 2.6 * dark + rng.normal(0, 0.4, n)).clip(1.0)
    unmetered = (44.75 + 5.2 * dark + rng.normal(0, 0.8, n)).clip(8.0)
    # the June maintenance: each tenant section isolated in turn (a room fed inside a supply goes dark with it)
    iso = {}
    for tag, a, b in W.ISOLATIONS:
        ta = dt.datetime.combine(W.SHUTDOWN_DAY, dt.time(*map(int, a.split(":"))))
        tb = dt.datetime.combine(W.SHUTDOWN_DAY, dt.time(*map(int, b.split(":"))))
        iso[tag] = (ta, tb)
        mask = np.array([ta <= l < tb for l in loc])
        kw[tag][mask] = 0.0
        for room, parent in W.NESTED.items():
            if parent == tag:
                kw[room][mask] = 0.0
                after = np.array([tb <= l < tb + D(hours=1) for l in loc])
                kw[room][after] *= 1.15                          # the room's UPS recharging
                kw[tag][after] += kw[room][after] * 0.15 / 1.15
    supplies = [m[0] for m in W.METERS if m[3] == "supply" and m[0] != "EM-118"]
    total = sum(kw[t] for t in supplies) + sum(kw[t] for t in ("EM-201", "EM-202", "EM-203", "EM-204")) + unmetered
    imp = total * (1 + 0.011 + rng.normal(0, 0.0015, n))       # transformer and cable losses, upstream of every meter
    return dict(ts=ts, loc=loc, kw=kw, imp=imp, unmetered=unmetered, wx=wx, iso=iso, temp=temp,
                gen=generator(rng), fgas=refrigerant(rng))


# ---------------------------------------------------------------------------------------------- the generator
def _monday_tests():
    """Weekly off-load tests, Mondays 10:00 (a bank holiday moves it to the next day), with the year's exceptions."""
    out = []
    d = dt.date(2025, 12, 29)
    while d <= dt.date(2027, 1, 4):
        day = d
        while day in W.BANK_HOLIDAYS:
            day += D(days=1)
        out.append(dict(start=dt.datetime.combine(day, dt.time(10, 0)), minutes=20, kind="Off-load test"))
        d += D(days=7)
    drop = {dt.date(2025, 12, 29), dt.date(2026, 9, 28), dt.date(2026, 12, 29), dt.date(2026, 6, 29)}
    out = [r for r in out if r["start"].date() not in drop]
    out += [dict(start=dt.datetime(2026, 1, 2, 10, 0), minutes=20, kind="Off-load test"),
            dict(start=dt.datetime(2026, 6, 29, 10, 0), minutes=60, kind="On-load test"),
            dict(start=dt.datetime(2026, 10, 2, 10, 0), minutes=20, kind="Off-load test"),
            dict(start=dt.datetime(2027, 1, 2, 10, 0), minutes=60, kind="On-load test")]
    return out


def generator(rng):
    runs = _monday_tests()
    for m in range(1, 13):                                      # monthly on-load test, the second Tuesday
        d = dt.date(2026, m, 1)
        tues = [d + D(days=i) for i in range(14) if (d + D(days=i)).weekday() == 1][1]
        if m != 6:
            runs.append(dict(start=dt.datetime.combine(tues, dt.time(9, 30)), minutes=60, kind="On-load test"))
    runs += [dict(start=dt.datetime(2026, 2, 17, 13, 42), minutes=203, kind="Mains failure"),
             dict(start=dt.datetime(2026, 11, 23, 6, 10), minutes=105, kind="Mains failure")]
    runs.sort(key=lambda r: r["start"])
    for r in runs:
        rate = W.ONLOAD_LPH if r["kind"] != "Off-load test" else W.OFFLOAD_LPH
        if r["kind"] == "Mains failure":
            rate = W.ONLOAD_LPH * float(rng.uniform(0.82, 0.93))
        r["end"] = r["start"] + D(minutes=r["minutes"])
        r["litres"] = r["minutes"] / 60.0 * rate * float(1 + rng.normal(0, 0.03))
    dips = []
    d = dt.datetime(2025, 12, 29, *W.DIP_TIME)
    while d <= dt.datetime(2027, 1, 4, *W.DIP_TIME):
        dips.append(d)
        d += D(days=7)
    events = [(r["end"], "run", r) for r in runs] + [(t, "dip", None) for t in dips]
    events.sort(key=lambda e: (e[0], e[1] != "dip"))
    stock = 2047.0
    deliveries, dip_rows = [], []
    pending = None
    for when, kind, r in events:
        if pending and when >= pending["at"]:
            stock += pending["litres"]
            deliveries.append(pending)
            pending = None
        if kind == "run":
            stock -= r["litres"]
            if stock < 1260 and pending is None:
                at = dt.datetime.combine(when.date() + D(days=2 if when.weekday() < 3 else 4), dt.time(11, 20))
                pending = dict(at=at, litres=float(int(round((2330 - stock + 120) / 50.0)) * 50))
        else:
            dip_rows.append(dict(at=when, litres=stock))
    return dict(runs=runs, dips=dip_rows, deliveries=deliveries)


def tank_litres(mm):
    r = W.TANK_DIAMETER_MM / 2.0
    h = min(max(mm, 0.0), 2 * r)
    area = r * r * math.acos((r - h) / r) - (r - h) * math.sqrt(max(2 * r * h - h * h, 0.0))
    return area * W.TANK_LENGTH_MM / 1e6


def tank_mm(litres):
    lo, hi = 0.0, float(W.TANK_DIAMETER_MM)
    for _ in range(60):
        mid = (lo + hi) / 2
        if tank_litres(mid) < litres:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


# ---------------------------------------------------------------------------------------------- the chillers
def refrigerant(rng):
    rows = []
    for ch, c in W.CHILLERS.items():
        for when, kg in c["topups"]:
            rows.append(dict(at=when, plant=ch, activity="Top-up", kg=kg))
        recovered = round(c["charge"] - c["loss"], 1)
        n_cyl = 3 if c["charge"] > 200 else 2
        parts = rng.dirichlet([6] * n_cyl) * recovered
        parts = [round(float(p), 1) for p in parts]
        parts[-1] = round(recovered - sum(parts[:-1]), 1)
        rows.append(dict(at=c["retube"], plant=ch, activity="Recovery", kg=recovered, cylinders=parts))
        rows.append(dict(at=c["retube"] + D(days=2, hours=3), plant=ch, activity="Recharge", kg=c["charge"]))
    for ch in W.CHILLERS:
        for m in (1, 4, 7, 10):
            rows.append(dict(at=dt.datetime(2026, m, 6 + list(W.CHILLERS).index(ch), 9, 15), plant=ch,
                             activity="Leak check", kg=0.0))
    rows.sort(key=lambda r: (r["at"], r["plant"]))
    return rows
