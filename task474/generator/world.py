"""The simulated world: candidates, their registrations and every booked sitting on both vendors' papers.

Everything is drawn from named, seeded streams, so the world is the same on every build."""
import datetime as dt
import hashlib

import numpy as np

import params as P


def rng(name):
    h = int(hashlib.sha256(("%d:%s" % (P.SEED, name)).encode()).hexdigest()[:12], 16)
    return np.random.default_rng(h)


def months():
    y, m = P.FIRST_DAY.year, P.FIRST_DAY.month
    while dt.date(y, m, 1) <= P.LAST_DAY:
        yield y, m
        m += 1
        if m == 13:
            y, m = y + 1, 1


def gas_share(d):
    pts = P.GAS_RAMP
    if d < pts[0][0]:
        return 0.0
    for (a, ga), (b, gb) in zip(pts, pts[1:]):
        if a <= d <= b:
            return ga + (gb - ga) * (d - a).days / max((b - a).days, 1)
    return pts[-1][1]


def season_mix(m):
    return P.MIX_SUMMER if 4 <= m <= 9 else P.MIX_WINTER


SEASON = {1: 0.92, 2: 1.0, 3: 1.05, 4: 0.96, 5: 1.12, 6: 1.18, 7: 1.10, 8: 0.86, 9: 1.02, 10: 1.04, 11: 1.0, 12: 0.75}

PROVIDERS = [("TP01", "Northgate College of Building Services", "North West"),
             ("TP02", "Severn Heat Academy", "South West"),
             ("TP03", "Midland Renewables Training", "West Midlands"),
             ("TP04", "Thames Gateway Plumbing School", "London"),
             ("TP05", "Pennine Energy Skills Centre", "Yorkshire and the Humber"),
             ("TP06", "East Anglia Heating Institute", "East of England"),
             ("TP07", "Black Country Installer Training", "West Midlands"),     # merged into TP03 in July 2025
             ("TP08", "Solent Building Services College", "South East"),
             ("TP09", "Tyne and Wear Low Carbon Skills", "North East"),
             ("TP10", "Mercia Gas and Heat Pump Centre", "East Midlands"),
             ("TP11", "Wessex Heat Pump Training", "South West"),
             ("TP12", "Kent Energy Training Partnership", "South East"),
             ("TP13", "Lancashire Heating Engineers' Academy", "North West")]
MERGED = {"TP07": ("TP03", dt.date(2025, 7, 1))}
GAS_PROVIDERS = ["TP10", "TP03", "TP12", "TP05"]     # the conversion courses the gas engineers come through

BRINDLE_CENTRES = [("BR-%03d" % k, nm) for k, nm in enumerate(
    ["Manchester Piccadilly", "Bristol Temple Quay", "Birmingham Colmore", "London Bridge", "Leeds Wellington",
     "Norwich Riverside", "Southampton Ocean Way", "Newcastle Quayside", "Nottingham Castle Marina", "Exeter Sowton",
     "Maidstone Kings Hill", "Preston Docks", "Coventry Westwood", "Sheffield Riverside", "Reading Green Park",
     "Cambridge Science Park"], start=11)]


BANK_HOLIDAYS = {dt.date(*x) for x in [
    (2020, 1, 1), (2020, 4, 10), (2020, 4, 13), (2020, 5, 8), (2020, 5, 25), (2020, 8, 31), (2020, 12, 25), (2020, 12, 28),
    (2021, 1, 1), (2021, 4, 2), (2021, 4, 5), (2021, 5, 3), (2021, 5, 31), (2021, 8, 30), (2021, 12, 27), (2021, 12, 28),
    (2022, 1, 3), (2022, 4, 15), (2022, 4, 18), (2022, 5, 2), (2022, 6, 2), (2022, 6, 3), (2022, 8, 29), (2022, 9, 19),
    (2022, 12, 26), (2022, 12, 27), (2023, 1, 2), (2023, 4, 7), (2023, 4, 10), (2023, 5, 1), (2023, 5, 8), (2023, 5, 29),
    (2023, 8, 28), (2023, 12, 25), (2023, 12, 26), (2024, 1, 1), (2024, 3, 29), (2024, 4, 1), (2024, 5, 6), (2024, 5, 27),
    (2024, 8, 26), (2024, 12, 25), (2024, 12, 26), (2025, 1, 1), (2025, 4, 18), (2025, 4, 21), (2025, 5, 5), (2025, 5, 26),
    (2025, 8, 25), (2025, 12, 25), (2025, 12, 26), (2026, 1, 1), (2026, 4, 3), (2026, 4, 6), (2026, 5, 4), (2026, 5, 25),
    (2026, 8, 31)]}


def working_day(d):
    """test centres sit Monday to Saturday outside the bank holidays of England and Wales"""
    while d.weekday() == 6 or d in BANK_HOLIDAYS:
        d = d + dt.timedelta(days=1)
    return d


def _weekday(r, y, m):
    while True:
        d = dt.date(y, m, int(r.integers(1, 29)))
        if d.weekday() < 6:
            return d


def build():
    r = rng("world")
    persons = []
    # first-time candidates month by month
    for (y, m) in months():
        base = P.FIRST_TIMERS_PER_MONTH[y] * SEASON[m]
        mid = dt.date(y, m, 15)
        g = gas_share(mid)
        n = int(round(base / (1 - g)))
        mix = season_mix(m)
        kinds = list(mix)
        probs = np.array([mix[k] for k in kinds]) * (1 - g)
        kinds.append("gas")
        probs = np.append(probs, g)
        probs = probs / probs.sum()
        for _ in range(n):
            k = kinds[int(r.choice(len(kinds), p=probs))]
            mu, sd = P.KINDS[k]
            theta = float(r.normal(mu, sd))
            first = _weekday(r, y, m)
            if first > P.LAST_DAY:
                continue
            age = {"college": (17, 24), "changer": (24, 50), "installer": (25, 58), "gas": (28, 60)}[k]
            dob = first - dt.timedelta(days=int(r.uniform(age[0], age[1]) * 365.25))
            if k == "gas":
                prov = GAS_PROVIDERS[int(r.integers(0, len(GAS_PROVIDERS)))]
            else:
                prov = PROVIDERS[int(r.integers(0, len(PROVIDERS)))][0]
            reg = first - dt.timedelta(days=int(r.integers(20, 120)))
            persons.append({"kind": k, "theta": theta, "first": first, "dob": dob, "provider": prov,
                            "registered": reg})
    persons.sort(key=lambda p: (p["registered"], p["first"]))
    # sittings: each booked sitting in date order; absent and voided bookings are rebooked and are not attempts
    s = rng("sittings")
    for p in persons:
        p["sittings"] = []
        d = p["first"]
        attempt = 0
        while working_day(d) <= P.LAST_DAY:
            d = working_day(d)
            vendor = "old" if d < P.SWITCH else "new"
            u = s.random()
            if u < P.ABSENT_RATE:
                p["sittings"].append({"date": d, "vendor": vendor, "status": "absent"})
                d = d + dt.timedelta(days=int(s.integers(14, 60)))
                continue
            if u < P.ABSENT_RATE + P.VOID_RATE:
                p["sittings"].append({"date": d, "vendor": vendor, "status": "void"})
                d = d + dt.timedelta(days=int(s.integers(14, 60)))
                continue
            attempt += 1
            th = p["theta"] + (P.RETEST_GAIN if attempt >= 2 else 0.0)
            if vendor == "old":
                score = int(np.clip(round(P.OLD_A + P.OLD_B * th + s.normal(0, P.OLD_ERR)), 0, 100))
            else:
                score = int(np.clip(round(P.NEW_A + P.NEW_B * th + s.normal(0, P.NEW_ERR)), 0, P.NEW_ITEMS))
            p["sittings"].append({"date": d, "vendor": vendor, "status": "sat", "score": score, "attempt": attempt})
            if vendor == "new":
                break                       # new-paper results are held: nobody resits before the Board sets the mark
            if score >= P.OLD_PASS:
                break
            near = d >= P.NEAR_MISS_FROM and P.NEAR_MISS[0] <= score <= P.NEAR_MISS[1]
            if s.random() > (P.NEAR_MISS_RESIT_PROB if near else P.RESIT_PROB):
                break
            low = d >= P.NEAR_MISS_FROM and score < P.NEAR_MISS[0]
            wait = P.LOW_WAIT_DAYS if low else (P.NEAR_MISS_WAIT_DAYS if near else P.RESIT_WAIT_DAYS)
            if not near and s.random() < P.LAPSE_PROB:
                wait = P.LAPSE_WAIT_DAYS            # comes back after a year or more away from the qualification
            d = d + dt.timedelta(days=int(s.integers(*wait)))
            while d.weekday() == 6:
                d = d + dt.timedelta(days=1)
    return persons
