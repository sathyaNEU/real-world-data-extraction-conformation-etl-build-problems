"""The FY2026 transition the asks read: the eight former county agencies' FY2026 awards and the balances unspent at
30 June 2026, and their client service records from the Fund's grants data system, with the address changes the
agencies logged on client profiles and Corbin Community Action's conversion of client numbers on 1 January 2026. None
of it is read by the allocation.

The truth: every service is delivered to a person on a date while they live in one town; energy assistance is one
payment to a household. The extract is what the system holds: each row carries the town on the client's profile when
the extract was cut, a household's energy payment is exported on the row of every member listed in the household, a
Corbin client carries an old number before 1 January 2026 and a new one after, Wexmoor's April 2026 upload was received
twice, and the extract is cut by entry date (1 July 2025 to 30 September 2026)."""
import datetime as dt

import numpy as np

import world as W

FY_START, FY_END = dt.date(2025, 7, 1), dt.date(2026, 6, 30)
ENTRY_FROM, EXTRACT_CUT = dt.date(2025, 7, 1), dt.date(2026, 9, 30)
MIGRATION = dt.date(2026, 1, 1)
MIGRATING = "Corbin"
RESENT = ("Wexmoor", dt.date(2026, 4, 1), dt.date(2026, 4, 30))
SERVICES = [("FD", "Food pantry", 0.47), ("RA", "Rent or utility arrears", 0.10), ("CM", "Case management", 0.18),
            ("TX", "Tax preparation", 0.07), ("EM", "Employment services", 0.08), ("NS", "Nutrition assistance outreach", 0.10)]
SERVICE_NAMES = dict((s[0], s[1]) for s in SERVICES)
SERVICE_NAMES["EA"] = "Energy assistance"
FY2026_FUND = 10_800_000


def fy2026_basis():
    """Each former county's average residents in poverty, 2018 to 2022, as the State Data Center last published them
    (the FY2026 allocation's basis)."""
    import sources as S
    return {c: sum(S.SDC_EST[("county", c, y)]["revised"] for y in range(2018, 2023)) / 5.0 for c in W.COUNTY_NAMES}


def _awards():
    """FY2026 awards: $10,800,000 in proportion to the basis, to the nearest $1,000, the remainder to the largest
    fractions."""
    import sources as S
    b = fy2026_basis()
    k = S._alloc_int(FY2026_FUND // 1000, [b[c] for c in W.COUNTY_NAMES])
    return {c: 1000 * v for c, v in zip(W.COUNTY_NAMES, k)}


AWARD = _awards()
CODE = {"Halden": "HCCAA", "Corbin": "CCA", "Wexmoor": "WOC", "Ashgrove": "AGCS", "Ludbury": "LCAP",
        "Merrick": "MCA", "Stanbridge": "SACA", "Pennock": "PCAC"}


def _day(r, lo, hi):
    return lo + dt.timedelta(days=int(r.integers(0, (hi - lo).days + 1)))


def build():
    r = W.rng("asks")
    towns = W.TOWNS
    byn = W.by_name()
    by_county = {c: [t for t in towns if t["county"] == c] for c in W.COUNTY_NAMES}
    households, people, services, moves = [], [], [], []
    for county in W.COUNTY_NAMES:
        ts = by_county[county]
        w = np.array([t["poor"][2025] * (1.25 if t["kind"] == "city" else 1.0) for t in ts])
        n_hh = int(sum(t["poor"][2025] for t in ts) * r.uniform(0.070, 0.082))
        for _ in range(n_hh):
            home = ts[int(r.choice(len(ts), p=w / w.sum()))]
            size = int(min(max(r.poisson(1.3) + 1, 1), 7))
            hh = dict(agency=county, home=home["name"], size=size, members=[], move=None)
            # a move during the year, mostly inside the former county; from Ormsby often to the four Mill River towns
            if r.random() < 0.135:
                same = [t for t in ts if t["name"] != home["name"]]
                dest = same[int(r.integers(0, len(same)))]
                if home["name"] == "Ormsby" and r.random() < 0.65:
                    dest = byn[["Fenbrook", "Tilcombe", "Carrholt", "Draywick"][int(r.integers(0, 4))]]
                if home["name"] == "Wexport" and r.random() < 0.45:
                    dest = byn[["Marlridge", "Ketmere", "Radstow"][int(r.integers(0, 3))]]
                hh["move"] = (dest["name"], _day(r, FY_START + dt.timedelta(days=40), FY_END - dt.timedelta(days=35)))
                moves.append(hh)
            for k in range(size):
                p = dict(pid=len(people) + 1, hh=len(households), agency=county,
                         age=(int(r.integers(1, 18)) if (k > 0 and r.random() < 0.6) else int(r.integers(19, 86))))
                people.append(p)
                hh["members"].append(p["pid"])
            households.append(hh)
    for hi, hh in enumerate(households):
        def town_on(day):
            return hh["move"][0] if (hh["move"] and day >= hh["move"][1]) else hh["home"]
        city = W.by_name()[hh["home"]]["kind"] == "city"
        n_visits = int(min(r.geometric(0.22 if city else 0.36), 12))
        for _ in range(n_visits):
            svc = SERVICES[int(r.choice(len(SERVICES), p=[s[2] for s in SERVICES]))][0]
            day = _day(r, dt.date(2025, 6, 2), dt.date(2026, 9, 25))
            served = [hh["members"][0]] if svc in ("CM", "TX", "EM", "RA") or r.random() < 0.62 else hh["members"]
            amt = int(r.integers(14, 190)) * 10 if svc == "RA" else 0
            for pid in served:
                services.append(dict(pid=pid, hh=hi, agency=hh["agency"], svc=svc, date=day, town=town_on(day),
                                     amount=amt))
        if r.random() < 0.27:
            day = _day(r, dt.date(2025, 11, 3), dt.date(2026, 3, 31))
            amt = int(r.integers(312, 1291))
            for pid in hh["members"]:
                services.append(dict(pid=pid, hh=hi, agency=hh["agency"], svc="EA", date=day, town=town_on(day),
                                     amount=amt, pay=(hi, day)))
    # entry dates; the extract holds what was entered from 1 July 2025 to the cut
    for s in services:
        lag = int(min(r.geometric(0.30), 30)) if r.random() < 0.94 else int(r.integers(18, 62))
        s["entered"] = s["date"] + dt.timedelta(days=lag)
    return dict(households=households, people=people, services=services, moves=moves)


DATA = build()


def balances():
    r = W.rng("balances")
    out = {}
    for c in W.COUNTY_NAMES:
        aw = AWARD[c]
        unspent = int(round(aw * r.uniform(0.034, 0.091)))
        out[c] = dict(award=aw, spent=aw - unspent, unspent=unspent)
    return out


BALANCES = balances()


def in_fy(day):
    return FY_START <= day <= FY_END


def council_of(town):
    return W.by_name()[town]["region"]


def golden():
    """Ask A: each council's carry-in and the people behind it; ask B: energy assistance paid in each council's towns.
    Computed on the truth, which the extract recovers exactly through the address log and the conversion log."""
    S = [s for s in DATA["services"] if in_fy(s["date"])]
    n = {}                                                    # (agency, council) -> set of people
    for s in S:
        n.setdefault((s["agency"], council_of(s["town"])), set()).add(s["pid"])
    counts = {k: len(v) for k, v in n.items()}
    carry = {g: 0.0 for g in W.REGION_NAMES}
    people = {g: 0 for g in W.REGION_NAMES}
    for c in W.COUNTY_NAMES:
        tot = sum(v for (a, g), v in counts.items() if a == c)
        for (a, g), v in counts.items():
            if a == c:
                carry[g] += BALANCES[c]["unspent"] * v / tot
                people[g] += v
    energy = {g: 0 for g in W.REGION_NAMES}
    seen = set()
    for s in S:
        if s["svc"] == "EA" and s["pay"] not in seen:
            seen.add(s["pay"])
            energy[council_of(s["town"])] += s["amount"]
    return dict(counts=counts, carry=carry, people=people, energy=energy)
