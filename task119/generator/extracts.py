"""The 08:00 bed returns, the unit register, the capacity report's figures and the two files the
solution never reads (the level-2 units' returns and the ambulance handover extract)."""
import bisect
import datetime as dt
from collections import defaultdict

import numpy as np

from common import (BEDS, FEED_UNITS, FEED0, RECORD1, TRUSTS, CODE, LETTERS, lm, day_of, unit_open, rng, fmt)
import zoneinfo

LONDON = zoneinfo.ZoneInfo("Europe/London")
from world import daterange


def returns_0800(stays_rows):
    """Occupied beds at 08:00 from the stays as shipped (contiguous bed-episode rows count once)."""
    adm, dis = defaultdict(list), defaultdict(list)
    for s in stays_rows:
        a = lm(dt.datetime.strptime(s["admitted_at"], "%Y-%m-%d %H:%M"))
        b = lm(dt.datetime.strptime(s["discharged_at"], "%Y-%m-%d %H:%M"))
        adm[s["unit_code"]].append(a)
        dis[s["unit_code"]].append(b)
    for u in adm:
        adm[u].sort()
        dis[u].sort()
    rows = []
    for u in FEED_UNITS:
        for d in daterange(FEED0, RECORD1):
            if not unit_open(u, d):
                continue
            t = lm(d, 8, 0)
            occ = bisect.bisect_right(adm[u], t) - bisect.bisect_right(dis[u], t)
            assert 0 <= occ <= BEDS[u], (u, d, occ)
            rows.append({"unit_code": u, "return_date": d.strftime("%Y-%m-%d"), "beds_open": BEDS[u],
                         "beds_occupied_0800": occ})
    return rows


UNIT_NAMES = {
    "RIS-ACC": "Ristenholm General Hospital adult critical care unit",
    "BRK-ACC": "Brackenford Royal Infirmary adult critical care unit",
    "STN-ACC": "Stennock University Hospital adult critical care unit",
    "PRW-ACC": "Prideswick County Hospital adult critical care unit",
    "ELL-ACC": "Ellerdyke Hospital critical care unit",
    "PEL-W3": "Pellowham Hospital escalation beds (level 3)",
    "PEL-HDU": "Pellowham Hospital high dependency unit",
    "TAN-HDU": "Tannerby Hospital high dependency unit",
    "LAT-HDU": "Lathingbury District Hospital high dependency unit",
}


def register_rows():
    R = [
        ("RIS-ACC", "RIS", 3, 28, "2019-04-01", "2022-03-31"),
        ("RIS-ACC", "RIS", 3, 30, "2022-04-01", ""),
        ("BRK-ACC", "BRK", 3, 14, "2019-04-01", "2021-09-30"),
        ("BRK-ACC", "BRK", 3, 16, "2021-10-01", ""),
        ("STN-ACC", "STN", 3, 18, "2019-04-01", ""),
        ("PRW-ACC", "PRW", 3, 10, "2019-04-01", "2022-09-30"),
        ("PRW-ACC", "PRW", 3, 12, "2022-10-01", ""),
        ("ELL-ACC", "ELL", 3, 8, "2019-04-01", "2024-03-31"),
        ("ELL-ACC", "ELL", 2, 6, "2024-04-01", ""),
        ("PEL-HDU", "PEL", 2, 6, "2019-04-01", ""),
        ("PEL-W3", "PEL", 3, 3, "2023-12-04", "2024-03-31"),
        ("TAN-HDU", "TAN", 2, 6, "2019-04-01", ""),
        ("LAT-HDU", "LAT", 2, 8, "2019-04-01", ""),
    ]
    return [{"unit_code": u, "unit_name": UNIT_NAMES[u], "trust_code": t, "care_level": lv, "commissioned_beds": b,
             "valid_from": a, "valid_to": z} for (u, t, lv, b, a, z) in R]


# ------------------------------------------------------------------------------ capacity report figures
REPORT_FROM = dt.date(2024, 4, 1)
REPORT_TO = dt.date(2026, 6, 30)


def month_iter(a, b):
    y, m = a.year, a.month
    while (y, m) <= (b.year, b.month):
        yield y, m
        m += 1
        if m == 13:
            y, m = y + 1, 1


def capacity_figures(returns, referrals):
    """Occupancy at 08:00 by unit and level-3 referrals waiting over four hours from receipt by trust,
    April 2024 to June 2026, from the returns and the referral log as shipped."""
    occ = defaultdict(list)
    for r in returns:
        d = dt.date.fromisoformat(r["return_date"])
        if REPORT_FROM <= d <= REPORT_TO:
            occ[(r["unit_code"], d.year, d.month)].append((r["beds_open"], r["beds_occupied_0800"]))
    units = ["RIS-ACC", "BRK-ACC", "STN-ACC", "PRW-ACC"]
    occ_rows = []
    for (y, m) in month_iter(REPORT_FROM, REPORT_TO):
        for u in units:
            v = occ[(u, y, m)]
            beds = sum(b for b, o in v) / len(v)
            mean_occ = sum(o for b, o in v) / len(v)
            occ_rows.append({"month": "%04d-%02d" % (y, m), "unit": u, "days": len(v), "beds_open": round(beds, 1),
                             "occupied_0800_mean": round(mean_occ, 1), "occupancy_0800_pct": round(100 * mean_occ / beds, 1)})
    waits = defaultdict(lambda: [0, 0])
    for r in referrals:
        if r["level_of_care"] != 3:
            continue
        rec = dt.datetime.strptime(r["received_at"], "%Y-%m-%d %H:%M")
        if not (REPORT_FROM <= rec.date() <= REPORT_TO):
            continue
        key = (r["referring_trust"], rec.year, rec.month)
        waits[key][0] += 1
        if r["outcome_at"]:
            out = dt.datetime.strptime(r["outcome_at"], "%Y-%m-%d %H:%M")
            # elapsed time: CCRS rows hold UTC, platform rows the local clock
            z = dt.timezone.utc if r["referral_id"].startswith("CC") else LONDON
            u = lambda t: t.replace(tzinfo=z).astimezone(dt.timezone.utc)
            if (u(out) - u(rec)).total_seconds() > 4 * 3600:
                waits[key][1] += 1
    wait_rows = []
    for (y, m) in month_iter(REPORT_FROM, REPORT_TO):
        for L in LETTERS:
            c = CODE[L]
            n, k = waits[(c, y, m)]
            wait_rows.append({"month": "%04d-%02d" % (y, m), "trust": c, "level3_referrals": n, "over_4h_from_receipt": k})
    return occ_rows, wait_rows


# ------------------------------------------------------------------------------ files the solution never reads
L2_UNITS = [("TAN-HDU", 6), ("LAT-HDU", 8), ("ELL-ACC", 6), ("PEL-HDU", 6)]


def level2_returns():
    r = rng("l2")
    rows = []
    for u, beds in L2_UNITS:
        occ = beds - 1
        for d in daterange(dt.date(2025, 7, 1), dt.date(2026, 6, 30)):
            occ = int(np.clip(occ + int(r.choice([-2, -1, 0, 0, 1, 1, 2])), max(0, beds - 5), beds))
            if d.weekday() >= 5 and r.random() < 0.3:
                occ = min(beds, occ + 1)
            rows.append({"unit_code": u, "return_date": d.strftime("%Y-%m-%d"), "beds_open": beds,
                         "beds_occupied_0800": occ})
    return rows


SITES = {L: TRUSTS[L][2] for L in LETTERS}


def ambulance_handovers():
    r = rng("amb")
    base = {"A": 5.2, "B": 2.1, "C": 3.6, "D": 3.9, "E": 4.4, "F": 2.4, "G": 2.9, "H": 1.7}
    hour_w = np.array([0.55, 0.45, 0.4, 0.35, 0.35, 0.4, 0.55, 0.8, 1.1, 1.3, 1.4, 1.45, 1.45, 1.4, 1.35, 1.3, 1.3,
                       1.3, 1.25, 1.15, 1.0, 0.9, 0.75, 0.65])
    rows = []
    for d in daterange(dt.date(2025, 7, 1), dt.date(2026, 6, 30)):
        winter = d.month in (12, 1, 2)
        for L in LETTERS:
            for h in range(24):
                if d == dt.date(2026, 3, 29) and h == 1:
                    continue            # the clocks went forward: no 01:00 hour that night
                lam = base[L] * hour_w[h] * (1.12 if winter else 1.0) * (1.06 if d.weekday() == 0 else 1.0)
                n = int(r.poisson(lam))
                if n == 0:
                    rows.append({"site": SITES[L], "trust_code": CODE[L], "arrival_date": d.strftime("%Y-%m-%d"),
                                 "arrival_hour": h, "arrivals": 0, "handover_0_15": 0, "handover_15_30": 0,
                                 "handover_30_60": 0, "handover_60_plus": 0, "hours_lost": "0.0"})
                    continue
                pressure = 0.25 + (0.25 if winter else 0) + (0.12 if L in ("E", "A") else 0) + (0.1 if 10 <= h <= 20 else 0)
                p = np.array([max(0.05, 0.55 - pressure), 0.25, 0.12 + pressure * 0.4, 0.08 + pressure * 0.6])
                p = p / p.sum()
                k = r.multinomial(n, p)
                lost = k[1] * 0.12 + k[2] * 0.5 + k[3] * (1.0 + float(r.random()) * 1.5)
                rows.append({"site": SITES[L], "trust_code": CODE[L], "arrival_date": d.strftime("%Y-%m-%d"),
                             "arrival_hour": h, "arrivals": n, "handover_0_15": int(k[0]), "handover_15_30": int(k[1]),
                             "handover_30_60": int(k[2]), "handover_60_plus": int(k[3]), "hours_lost": "%.1f" % lost})
    return rows
