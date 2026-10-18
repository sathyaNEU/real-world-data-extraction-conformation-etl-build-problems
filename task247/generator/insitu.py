"""task247 in situ: the temperature loggers the dive team keeps at each site's survey depth, swapped on the April and
August service trips, and the hourly readings each logger took from its launch in the lab to its download after
retrieval.

The water at the logger is the site's sea (the simulator's truth for the day) a little cooler at depth while the
summer stratifies, with a small afternoon swing. A logger reads the lab and the boat before it goes in and the deck
and the lab after it comes out. The service trips' times are written down from the boat's GPS: the Ixchel's shows
local time, the Cozumel II's showed UTC until its unit was replaced in June 2026."""
import datetime as dt

import numpy as np

import params as P

LOCAL = dt.timedelta(hours=-5)          # the station keeps UTC-5 all year
FIRST_EXPORT = dt.datetime(2024, 4, 1, 0, 0)

# the service trips: name, boat, days (site order north to south), what was done, whether the GPS showed UTC
TRIPS = [
    ("2023-08", "Ixchel", [dt.date(2023, 8, 14), dt.date(2023, 8, 15), dt.date(2023, 8, 16), dt.date(2023, 8, 17)],
     "swap", False),
    ("2024-04", "Ixchel", [dt.date(2024, 4, 8), dt.date(2024, 4, 9), dt.date(2024, 4, 10), dt.date(2024, 4, 11)],
     "swap", False),
    ("2024-08", "Ixchel", [dt.date(2024, 8, 12), dt.date(2024, 8, 13), dt.date(2024, 8, 14), dt.date(2024, 8, 15)],
     "swap", False),
    ("2025-04", "Ixchel", [dt.date(2025, 4, 7), dt.date(2025, 4, 8), dt.date(2025, 4, 9), dt.date(2025, 4, 10)],
     "swap", False),
    ("2025-08a", "Cozumel II", [dt.date(2025, 8, 11), dt.date(2025, 8, 12), dt.date(2025, 8, 13), dt.date(2025, 8, 14)],
     "retrieve", True),
    ("2025-08b", "Ixchel", [dt.date(2025, 8, 18), dt.date(2025, 8, 19), dt.date(2025, 8, 20), dt.date(2025, 8, 21)],
     "deploy", False),
    ("2026-04", "Cozumel II", [dt.date(2026, 4, 13), dt.date(2026, 4, 14), dt.date(2026, 4, 15), dt.date(2026, 4, 16)],
     "swap", True),
    ("2026-08", "Cozumel II", [dt.date(2026, 8, 10), dt.date(2026, 8, 11), dt.date(2026, 8, 12), dt.date(2026, 8, 13)],
     "swap", False),
    ("2027-04", "Ixchel", [dt.date(2027, 4, 12), dt.date(2027, 4, 13), dt.date(2027, 4, 14), dt.date(2027, 4, 15)],
     "swap", False),
]
DAY_OF_SITE = [0] * 4 + [1] * 4 + [2] * 4 + [3] * 4     # four sites a day, north to south


def _site_times(rng, n, start_h=8.4):
    """the clock times (hours) at which the boat reached each of the day's sites"""
    t, out = start_h + rng.uniform(0, 0.4), []
    for _ in range(n):
        out.append(t)
        t += rng.uniform(1.0, 1.6)
    return out


def make(W, seed=P.LOGGER_SEED):
    rng = np.random.default_rng(seed)
    D = W["D"]
    idx = {d: i for i, d in enumerate(D)}
    true = W["true"]
    mon = np.array([d.month for d in D])
    # stratification: the water at depth runs cooler than the surface in summer
    cool = rng.uniform(0.20, 0.42, P.NSITE)
    summer = np.clip(np.sin(np.pi * (np.array([d.timetuple().tm_yday for d in D]) - 120) / 200.0), 0, None)
    swing = rng.uniform(0.05, 0.11, P.NSITE)
    # each trip: the time each site was visited
    visits = {}
    for name, boat, days, what, utc in TRIPS:
        by_day = {}
        for s in range(P.NSITE):
            by_day.setdefault(DAY_OF_SITE[s], []).append(s)
        for k, sites in by_day.items():
            hours = _site_times(rng, len(sites))
            for s, h in zip(sites, hours):
                t = (dt.datetime.combine(days[k], dt.time(0)) + dt.timedelta(hours=h)).replace(second=0, microsecond=0)
                if t.minute == 0:
                    t += dt.timedelta(minutes=7)            # never on the hour, so no reading sits on a boundary
                visits[(name, s)] = t
    # deployments: a logger goes in at one trip and comes out at the next trip that retrieves
    deps = []
    serial_old, serial_new = 20581406, 21143210
    order = [t for t in TRIPS]
    for s in range(P.NSITE):
        current = None
        for name, boat, days, what, utc in order:
            t = visits[(name, s)]
            if what in ("swap", "retrieve") and current is not None:
                current["retrieved"] = t
                current["retrieved_boat"], current["retrieved_utc"] = boat, utc
                current = None
            if what in ("swap", "deploy"):
                # the dive team needs a few minutes between pulling a logger and putting the next one in
                td = t + dt.timedelta(minutes=int(rng.integers(6, 18))) if what == "swap" else t
                if td.minute == 0:
                    td += dt.timedelta(minutes=3)
                mx = td.date() >= dt.date(2025, 8, 18)
                if mx:
                    serial, serial_new = serial_new, serial_new + int(rng.integers(3, 40))
                else:
                    serial, serial_old = serial_old, serial_old + int(rng.integers(2, 30))
                current = dict(site=s, serial=str(serial), model="MX2203" if mx else "TidbiT v2", deployed=td,
                               deployed_boat=boat, deployed_utc=utc, retrieved=None, retrieved_boat="",
                               retrieved_utc=False, depth=None, offset=float(rng.normal(0, 0.025)))
                deps.append(current)
    # readings: hourly from the launch (the afternoon before the trip, in the lab) to the download. Before it goes in
    # a logger sits in the lab, then in a cooler of the station's tank water on the boat; after it comes out it rides
    # back in that cooler and waits in the lab's seawater tank for the download.
    rows = []
    for d in deps:
        s = d["site"]
        if d["retrieved"] is None:
            continue                                     # still on the reef (the April 2027 loggers)
        launch = dt.datetime.combine(d["deployed"].date() - dt.timedelta(days=1), dt.time(15, 0)) + \
            dt.timedelta(minutes=int(rng.integers(0, 50)))
        packed = dt.datetime.combine(d["deployed"].date(), dt.time(6, 30))
        back = d["retrieved"] + dt.timedelta(hours=float(rng.uniform(1.2, 3.0)))
        if DAY_OF_SITE[s] == 3:
            download = dt.datetime.combine(d["retrieved"].date() + dt.timedelta(days=1), dt.time(8, 40)) + \
                dt.timedelta(minutes=int(rng.integers(0, 60)))
        else:
            download = dt.datetime.combine(d["retrieved"].date(), dt.time(17, 0)) + \
                dt.timedelta(minutes=int(rng.integers(0, 90)))
        lab = rng.uniform(24.2, 25.4)
        t = launch.replace(minute=0) + dt.timedelta(hours=1)
        while t <= download:
            i = idx.get((t - LOCAL).date())              # the UTC day the hour falls in
            if i is None:
                t += dt.timedelta(hours=1)
                continue
            surf = true[s, i] + 0.6 * swing[s] * np.cos(2 * np.pi * (t.hour - 15) / 24)
            if d["deployed"] <= t <= d["retrieved"]:
                v = (true[s, i] - cool[s] * summer[i] + swing[s] * np.cos(2 * np.pi * (t.hour - 16) / 24)
                     + d["offset"] + rng.normal(0, 0.02))
            elif t < packed:
                v = lab + rng.normal(0, 0.25)
            elif t < d["deployed"]:
                v = surf + rng.uniform(0.1, 0.5) + rng.normal(0, 0.05)       # the cooler of tank water
            elif t <= back:
                v = surf + rng.uniform(0.3, 0.9) + rng.normal(0, 0.05)       # the cooler on deck
            else:
                v = surf + rng.uniform(0.2, 0.6) + rng.normal(0, 0.05)       # the lab's seawater tank
            rows.append((d["serial"], t, round(float(v), 2)))
            t += dt.timedelta(hours=1)
    return dict(deps=deps, readings=rows, visits=visits, cool=cool, swing=swing)


def logged(t, utc):
    """the time the boat's GPS showed for a local time t"""
    return t - LOCAL if utc else t
