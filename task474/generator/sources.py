"""What each source publishes about the world in world.py, measured the way that source measures it:

- the State Data Center's model estimates of residents in poverty, each year first published in December of the
  next year and revised a year later, for the former counties through 2022 and the planning regions from 2023;
- the Department of Social Services' SNAP participation by town and benefit month, January 2019 to June 2026;
- the Bureau's 2020-2024 five-year table of poverty status by sex by age for the towns, the regions and the State;
- the State's population estimates by town (vintage 2025) and the Bureau's county-to-region allocation factors.
"""
import math

import numpy as np

import world as W

AGES = ["Under 5 years", "5 years", "6 to 11 years", "12 to 14 years", "15 years", "16 and 17 years",
        "18 to 24 years", "25 to 34 years", "35 to 44 years", "45 to 54 years", "55 to 64 years",
        "65 to 74 years", "75 years and over"]
KID_SPLIT = [0.29, 0.055, 0.33, 0.165, 0.055, 0.105]          # within under-18
WORK_SPLIT = [0.25, 0.21, 0.19, 0.17, 0.18]                    # within 18 to 64
OLD_SPLIT = [0.56, 0.44]                                        # within 65 and over


def _sdc():
    """Estimates by area and year, each with a first release and (for every year but the latest) a revision."""
    r = W.rng("sdc")
    est = {}
    for y in W.YEARS:
        if y > 2024:
            continue
        if y <= 2022:
            areas = [("county", c) for c in W.COUNTY_NAMES]
            key = "county"
        else:
            areas = [("region", g) for g in W.REGION_NAMES]
            key = "region"
        for kind, a in areas:
            truth = sum(t["poor"][y] for t in W.TOWNS if t[key] == a)
            rev = truth * (1 + r.normal(0, 0.0042))
            first = rev * (1 + r.normal(0, 0.0031))
            se = rev * r.uniform(0.019, 0.026)
            est[(kind, a, y)] = dict(first=int(round(first)), revised=int(round(rev)),
                                     lo=int(round(rev - 1.645 * se)), hi=int(round(rev + 1.645 * se)),
                                     lo1=int(round(first - 1.645 * se * 1.04)), hi1=int(round(first + 1.645 * se * 1.04)))
    return est


SDC_EST = _sdc()


def sdc_latest(kind, area, year):
    """The figure as last published: the revision where one has been published (every year to 2023), else the first."""
    e = SDC_EST[(kind, area, year)]
    return e["revised"] if year <= 2023 else e["first"]


def _statefac(y, m):
    """Statewide SNAP participation among the poor, the same in every town: the 2020 rise and the slow unwinding."""
    k = (y - 2019) * 12 + m
    if k <= 15:                     # to March 2020
        return 1.000 + 0.0006 * k
    if k <= 22:                     # April to October 2020
        return 1.010 + (k - 15) * 0.0165
    if k <= 50:                     # to February 2023
        return 1.125 + 0.0004 * (k - 22)
    if k <= 66:                     # March 2023 to June 2024
        return 1.136 - (k - 50) * 0.0042
    return 1.069 - (k - 66) * 0.0009


SEASON = [1.006, 1.008, 1.004, 0.999, 0.996, 0.993, 0.992, 0.995, 0.998, 1.001, 1.003, 1.005]


def allotment(y, m):
    """Average benefit per household per month: the emergency allotments from April 2020 to February 2023."""
    k = (y - 2019) * 12 + m
    base = 243.0 + 1.6 * (y - 2019) + (19.0 if (y > 2021 or (y == 2021 and m >= 10)) else 0.0)
    if 16 <= k <= 50:
        return base + 262.0
    return base


def _snap():
    """Monthly recipients and households by town: take-up among the poor, the statewide factor and season, a slow
    wobble, and the caseload's own churn (cases opening and closing, persistent month to month, of the size a count
    of that size carries)."""
    r = W.rng("snap")
    rc = W.rng("snap_churn")
    out = {}
    for t in W.TOWNS:
        hh_drift = r.uniform(-0.0006, 0.0006)
        wob = churn = 0.0
        for y in range(2019, 2027):
            for m in range(1, 13):
                if (y, m) > (2026, 6):
                    continue
                wob = 0.7 * wob + r.normal(0, 0.0045)
                base = t["take"] * t["poor_m"][(y, m)] * _statefac(y, m) * SEASON[m - 1] * (1 + wob)
                churn = 0.55 * churn + rc.normal(0, 0.5 * math.sqrt(max(base, 1.0)))
                rec = max(int(round(base + churn)), 0)
                hh = max(int(round(rec / (t["hh"] * (1 + hh_drift * (y - 2022))))), 1 if rec else 0)
                ben = int(round(hh * allotment(y, m) * (1 + r.normal(0, 0.012))))
                out[(t["name"], y, m)] = dict(recipients=rec, households=hh, benefits=ben)
    return out


SNAP = _snap()


_SY = {}


def snap_year(name, y, field="recipients"):
    """A town's calendar-year average monthly count."""
    k = (name, y, field)
    if k not in _SY:
        _SY[k] = sum(SNAP[(name, y, m)][field] for m in range(1, 13)) / 12.0
    return _SY[k]


def _alloc_int(total, weights):
    """Integers summing to total in proportion to weights (largest remainder, ties by position)."""
    raw = [total * w / sum(weights) for w in weights]
    base = [int(math.floor(x)) for x in raw]
    left = total - sum(base)
    order = sorted(range(len(raw)), key=lambda i: (-(raw[i] - base[i]), i))
    for i in order[:left]:
        base[i] += 1
    return base


def _acs():
    """B17001, poverty status in the past 12 months by sex by age, 2020-2024 five-year, for each town: the below-poverty
    total is the five years' mean stock measured with the survey's sampling error, its cells split by the town's age and
    sex profile with cell-level noise; the universe is the five years' household population."""
    r = W.rng("acs")
    rows = {}
    for t in W.TOWNS:
        mean_poor = float(np.mean([t["poor"][y] for y in range(2020, 2025)]))
        cv = 5.6 / math.sqrt(max(mean_poor, 60.0))
        below = max(int(round(mean_poor * (1 + r.normal(0, cv)))), 12)
        univ_mean = float(np.mean([t["popy"][y] for y in range(2020, 2025)])) * r.uniform(0.968, 0.986)
        univ = int(round(univ_mean * (1 + r.normal(0, 0.006))))
        above = univ - below
        k, o = t["kids"], t["old"]
        w_age = [k * s for s in KID_SPLIT] + [(1 - k - o) * s for s in WORK_SPLIT] + [o * s for s in OLD_SPLIT]
        w_age = [max(w * (1 + r.normal(0, 0.10)), 1e-4) for w in w_age]
        fem = [0.50, 0.50, 0.49, 0.50, 0.51, 0.50, 0.55, 0.57, 0.56, 0.54, 0.55, 0.57, 0.64]
        cells_b = []
        for a, wa in enumerate(w_age):
            f = min(max(fem[a] + r.normal(0, 0.02), 0.35), 0.75)
            cells_b += [wa * (1 - f), wa * f]
        below_cells = _alloc_int(below, cells_b)
        # above: a working-age heavier profile
        k2, o2 = max(k - 0.12, 0.14), max(o + 0.02, 0.10)
        w_age2 = [k2 * s for s in KID_SPLIT] + [(1 - k2 - o2) * s for s in WORK_SPLIT] + [o2 * s for s in OLD_SPLIT]
        w_age2 = [max(w * (1 + r.normal(0, 0.05)), 1e-4) for w in w_age2]
        cells_a = []
        for a, wa in enumerate(w_age2):
            f = min(max(0.50 + r.normal(0, 0.012) + (0.06 if a == 12 else 0.0), 0.40), 0.66)
            cells_a += [wa * (1 - f), wa * f]
        above_cells = _alloc_int(above, cells_a)
        rows[t["name"]] = dict(universe=univ, below=below, below_cells=below_cells, above=above,
                               above_cells=above_cells)
    return rows


ACS = _acs()


def acs_moe(value, kind="cell", key=""):
    """A 90 per cent margin of error of the size the survey's tables carry for a count of this size."""
    if value <= 0:
        return 15
    deff = {"cell": 2.9, "total": 3.4, "universe": 0.9}[kind]
    se = math.sqrt(value * deff) * (1.0 + 0.05 * ((sum(map(ord, key)) % 7) - 3))
    return max(int(round(1.645 * se)), 9)


def _population():
    """Vintage 2025 town estimates: 1 April 2020 base and 1 July 2020 to 2025."""
    r = W.rng("pop")
    out = {}
    for t in W.TOWNS:
        out[(t["name"], "base")] = t["pop2020"]
        for y in range(2020, 2026):
            out[(t["name"], y)] = int(round(t["popy"][y] * (1 + r.normal(0, 0.0035))))
    return out


POP = _population()


def alloc_factors():
    """The Bureau's county-to-region allocation factors: each piece's share of its former county's 2020 census
    population (and of its housing units)."""
    out = []
    r = W.rng("afac")
    for county in W.COUNTY_NAMES:
        tot = sum(t["pop2020"] for t in W.TOWNS if t["county"] == county)
        for region in W.REGION_NAMES:
            ts = [t for t in W.TOWNS if t["county"] == county and t["region"] == region]
            if not ts:
                continue
            pop = sum(t["pop2020"] for t in ts)
            hu = sum(int(round(t["pop2020"] / (2.31 + r.uniform(-0.12, 0.14)))) for t in ts)
            out.append(dict(county=county, region=region, pop=pop, afact=pop / tot, hu=hu))
    hu_tot = {}
    for o in out:
        hu_tot[o["county"]] = hu_tot.get(o["county"], 0) + o["hu"]
    for o in out:
        o["afact_hu"] = o["hu"] / hu_tot[o["county"]]
    return out
