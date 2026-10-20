"""The records cut from the truth: each city's permit system export (permits with their issue and certificate-of-
occupancy dates, including permits that expired and were issued again under a new number, and permits not yet
built), the demolitions, the utility's monthly residential accounts for the cities it serves, the ACS occupancy
and the group quarters survey."""
import datetime as dt

import numpy as np

import sources as S
import world as W

LAG = {"MF": (420, 900), "TH": (240, 420), "SF": (150, 300)}           # days from permit issue to occupancy


def permits(rng, x):
    """[permit dict] per city: one per building (and an earlier expired permit for some), plus buildings permitted
    but not finished by the extract."""
    out = {}
    pid = {"metro": 2400000, "county": 18000, "civic": 5100}
    for c, v in x.items():
        rows = []
        parcel = int(rng.integers(100000, 900000))

        def add(b, issued, co, status, kind, units, project, prc):
            pid[v["system"]] += int(rng.integers(1, 40))
            rows.append(dict(city=c, num=pid[v["system"]], parcel=prc, project=project, issued=issued, co=co,
                             status=status, kind=kind, units=units))
        for j, b in enumerate(sorted(v["blds"], key=lambda b: b["co"])):
            parcel += int(rng.integers(3, 400))
            lag = int(rng.integers(*LAG[b["kind"]]))
            issued = b["co"] - dt.timedelta(lag)
            project = "%s %s" % (("Residences at", "The", "Lofts at", "Commons at", "Flats at")[int(rng.integers(0, 5))],
                                 ("Mill Creek", "Station", "Parkside", "Cedar", "Union", "Riverwalk", "Hillcrest",
                                  "Market", "Lakeview", "Grove", "Ridge", "Harbor")[int(rng.integers(0, 12))]) \
                if b["kind"] == "MF" else ""
            if issued.year >= 2023 and rng.random() < (.32 if b["kind"] == "MF" else .08):
                # the first permit lapsed before work began and the project was permitted again
                first = issued - dt.timedelta(int(rng.integers(200, 420)))
                add(b, first, None, "EXPIRED", b["kind"], b["units"], project, parcel)
            add(b, issued, b["co"], "FINALED", b["kind"], b["units"], project, parcel)
        # permitted and under construction at the extract
        for k in range(int(rng.integers(8, 20))):
            parcel += int(rng.integers(3, 400))
            kind = str(rng.choice(["MF", "SF", "TH"], p=[.35, .5, .15]))
            units = int(rng.integers(60, 300)) if kind == "MF" else (int(rng.integers(4, 9)) if kind == "TH" else 1)
            issued = dt.date(2024, 6, 1) + dt.timedelta(int(rng.integers(0, 640)))
            project = "%s %s" % (("Residences at", "The", "Lofts at", "Commons at", "Flats at")[int(rng.integers(0, 5))],
                                 ("Mill Creek", "Station", "Parkside", "Cedar", "Union", "Riverwalk", "Hillcrest",
                                  "Market", "Lakeview", "Grove", "Ridge", "Harbor")[int(rng.integers(0, 12))]) \
                if kind == "MF" else ""
            if rng.random() < (.4 if kind == "MF" else .08):
                first = issued - dt.timedelta(int(rng.integers(200, 420)))
                add(None, first, None, "EXPIRED", kind, units, project, parcel)
            add(None, issued, None, "ISSUED", kind, units, project, parcel)
        # a stalled apartment project permitted again in 2025 (its 2024 permit had lapsed)
        parcel += int(rng.integers(3, 400))
        units = int(rng.integers(90, 260))
        issued = dt.date(2025, 2, 1) + dt.timedelta(int(rng.integers(0, 300)))
        project = "%s %s" % (("Residences at", "Lofts at", "Commons at")[int(rng.integers(0, 3))],
                             ("Northgate", "Southpoint", "Westfield", "Eastbrook")[int(rng.integers(0, 4))])
        add(None, issued - dt.timedelta(int(rng.integers(220, 400))), None, "EXPIRED", "MF", units, project, parcel)
        add(None, issued, None, "ISSUED", "MF", units, project, parcel)
        out[c] = rows
    return out


def utility(rng, x):
    """[(city, premise, address, bill month, residential meters, active residential accounts)] for the cities the
    utility serves: every apartment building completed since 2020 from its first bill, and the older complexes."""
    rows = []
    start = dt.date(2021, 1, 1)
    bills = []
    d = start
    while d <= dt.date(2026, 3, 1):
        bills.append(d)
        d = dt.date(d.year + d.month // 12, d.month % 12 + 1, 1)
    prem = 7700000
    for c, v in x.items():
        if not v["covered"]:
            continue
        street = ["Oak", "Main", "Pine", "Lake", "Elm", "Station", "Mill", "Union", "Park", "Ridge", "Cedar", "Grove"]
        for b in [b for b in v["blds"] if b["kind"] == "MF"] + \
                [dict(kind="OLD", units=int(rng.integers(24, 260)), co=None) for _ in range(int(rng.integers(80, 110)))]:
            prem += int(rng.integers(1, 50))
            addr = "%d %s %s" % (int(rng.integers(100, 9900)), street[int(rng.integers(0, 12))],
                                 ("St", "Ave", "Blvd", "Dr", "Way")[int(rng.integers(0, 5))])
            occ = v["stock_occ"] * float(rng.uniform(.98, 1.02))
            for bm in bills:
                if b["co"] is not None:
                    first = dt.date(b["co"].year, b["co"].month, 1)
                    if bm < first:
                        continue
                    # the bill month's accounts: the units occupied by mid-month, a little churn
                    mid = bm + dt.timedelta(14)
                    p = S.fill(S.months(b["co"], mid), b["tau"], b["level"])
                else:
                    p = min(.995, occ + rng.normal(0, .012))
                a = int(rng.binomial(b["units"], max(0.0, min(1.0, p))))
                rows.append((c, prem, addr, bm, b["units"], a))
    return rows
