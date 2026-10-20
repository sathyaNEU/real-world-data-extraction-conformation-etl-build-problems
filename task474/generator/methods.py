"""The golden construction and every rung, computed from the generator's own copies of what the pack carries.

The estimand (the Fund's allocation rule): a region's figure for a year is the State Data Center's estimate as last
published; for 2020 to 2022, which it estimated only for the former counties, the region's figure is the part of each
former county's estimate made up of the residents in poverty of the region's towns that year. The Fund is split on the
five years' average. The golden estimates each town's residents in poverty in 2020 to 2022 by its SNAP recipients that
year scaled to the town's own 2020-2024 five-year level (the Bureau's below-poverty count over its mean SNAP recipients
for the same five years), so the year's timing comes from the monthly counts and the level from the survey."""
import numpy as np

import sources as S
import world as W

ROUND_AMOUNT = 10_000
ROUND_PEOPLE = 100


def towns_in(county=None, region=None):
    return [t for t in W.TOWNS if (county is None or t["county"] == county) and (region is None or t["region"] == region)]


def snap_avg(name, years, field="recipients"):
    return float(np.mean([S.snap_year(name, y, field) for y in years]))


# ---------------------------------------------------------------------------------------- town-year estimators
def est_golden(t, y, field="recipients"):
    lvl = S.ACS[t["name"]]["below"]
    return S.snap_year(t["name"], y, field) * lvl / snap_avg(t["name"], range(2020, 2025), field)


def est_window(t, y):
    return float(S.ACS[t["name"]]["below"])


def est_snap(t, y):
    return S.snap_year(t["name"], y)


def est_snap_hh(t, y):
    return S.snap_year(t["name"], y, "households")


def est_universe(t, y):
    return float(S.ACS[t["name"]]["universe"])


def est_pop(t, y):
    return float(t["pop2020"])


def est_midpoint(t, y):
    """The five-year level read as the town's 2022 figure, moved to the other years by its SNAP recipients."""
    return S.ACS[t["name"]]["below"] * S.snap_year(t["name"], y) / S.snap_year(t["name"], 2022)


def est_additive(t, y):
    """The five-year level moved by the year's SNAP recipients less their five-year mean (an additive benchmark)."""
    return S.ACS[t["name"]]["below"] + S.snap_year(t["name"], y) - snap_avg(t["name"], range(2020, 2025))


def est_hedge(t, y):
    """Half the window's share and half the year's SNAP share, inside the county (a split-the-difference route)."""
    raise NotImplementedError     # computed at the share level in series()


def apportion(county, y, est):
    ts = towns_in(county=county)
    vals = {t["name"]: est(t, y) for t in ts}
    den = sum(vals.values())
    out = {}
    for t in ts:
        out[t["region"]] = out.get(t["region"], 0.0) + S.sdc_latest("county", county, y) * vals[t["name"]] / den
    return out


def series(est, piece_level=False, hedge=False, field="recipients"):
    """Each region's figure for 2020 to 2024 under a town-year estimator for the former counties' years."""
    out = {r: {} for r in W.REGION_NAMES}
    for y in W.LEGACY_YEARS:
        for r in W.REGION_NAMES:
            out[r][y] = 0.0
        for c in W.COUNTY_NAMES:
            if hedge:
                a = apportion(c, y, est_window)
                b = apportion(c, y, est_snap)
                for r in a:
                    out[r][y] += 0.5 * (a[r] + b[r])
                continue
            if piece_level:
                vals = {}
                for t in towns_in(county=c):
                    p = vals.setdefault(t["region"], dict(snap_y=0.0, snap_m=0.0, lvl=0.0))
                    p["snap_y"] += S.snap_year(t["name"], y, field)
                    p["snap_m"] += snap_avg(t["name"], range(2020, 2025), field)
                    p["lvl"] += S.ACS[t["name"]]["below"]
                v = {r: p["snap_y"] * p["lvl"] / p["snap_m"] for r, p in vals.items()}
                den = sum(v.values())
                for r, x in v.items():
                    out[r][y] += S.sdc_latest("county", c, y) * x / den
                continue
            for r, x in apportion(c, y, est).items():
                out[r][y] += x
    for y in W.NATIVE_YEARS:
        for r in W.REGION_NAMES:
            out[r][y] = float(S.sdc_latest("region", r, y))
    return out


def series_factors(kind="pop"):
    """The Bureau's county-to-region allocation factors applied to the former counties' estimates."""
    fac = S.alloc_factors()
    out = {r: {} for r in W.REGION_NAMES}
    for y in W.LEGACY_YEARS:
        for r in W.REGION_NAMES:
            out[r][y] = 0.0
        for f in fac:
            out[f["region"]][y] += S.sdc_latest("county", f["county"], y) * (f["afact"] if kind == "pop" else f["afact_hu"])
    for y in W.NATIVE_YEARS:
        for r in W.REGION_NAMES:
            out[r][y] = float(S.sdc_latest("region", r, y))
    return out


def series_carryback():
    """Each region's share of the State in the regions' first year, 2023, applied to the former counties' totals."""
    tot23 = sum(S.sdc_latest("region", r, 2023) for r in W.REGION_NAMES)
    out = {r: {} for r in W.REGION_NAMES}
    for y in W.LEGACY_YEARS:
        st = sum(S.sdc_latest("county", c, y) for c in W.COUNTY_NAMES)
        for r in W.REGION_NAMES:
            out[r][y] = st * S.sdc_latest("region", r, 2023) / tot23
    for y in W.NATIVE_YEARS:
        for r in W.REGION_NAMES:
            out[r][y] = float(S.sdc_latest("region", r, y))
    return out


def series_first_release():
    """The golden construction on each year's first release rather than the figure as last published."""
    saved = S.sdc_latest
    S.sdc_latest = lambda kind, area, year: S.SDC_EST[(kind, area, year)]["first"]
    try:
        return series(est_golden)
    finally:
        S.sdc_latest = saved


def average(ser):
    return {r: float(np.mean([ser[r][y] for y in range(2020, 2025)])) for r in W.REGION_NAMES}


def allocate(avg):
    tot = sum(avg.values())
    return {r: W.FUND * avg[r] / tot for r in W.REGION_NAMES}


def rnd(x, unit):
    return int(unit * round(x / unit))


def routes():
    """Every route a competent analyst could take for the former counties' years, by name."""
    return {
        "G": series(est_golden),
        "G_piece": series(est_golden, piece_level=True),
        "G_households": series(lambda t, y: est_golden(t, y, "households")),
        "R0_window": series(est_window),
        "R1_snap": series(est_snap),
        "R1b_snap_households": series(est_snap_hh),
        "R2_hedge": series(None, hedge=True),
        "R3_pop_factors": series_factors("pop"),
        "R3b_hu_factors": series_factors("hu"),
        "R4_carryback": series_carryback(),
        "R5_universe": series(est_universe),
        "R6_census_pop": series(est_pop),
        "R7_midpoint": series(est_midpoint),
        "R8_additive": series(est_additive),
    }


GOLDEN_FAMILY = ("G", "G_piece", "G_households")


def summary(ser):
    avg = average(ser)
    amt = allocate(avg)
    return dict(series=ser, avg=avg, amount=amt)
