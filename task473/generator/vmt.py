"""The DOT's county vehicle miles: each county's 2023 to 2025 annual average daily vehicle miles by functional
class, in thousands (the HPMS submission's county summaries), and the motor vehicle division's licensed drivers."""
import math

import methods as M
import truth as T
import world as W

CLASSES = ("Interstate", "Other Freeways and Expressways", "Other Principal Arterial", "Minor Arterial",
           "Major Collector", "Minor Collector", "Local")
YEAR_SPLIT = {2023: 0.3302, 2024: 0.3335, 2025: 0.3363}
DAYS = {2023: 365, 2024: 366, 2025: 365}
INTERSTATE_COUNTIES = ("001", "003", "009", "011", "013", "015", "017", "019", "025", "027")


def class_shares(fips):
    rng = T.rng_for("classes", fips)
    base = [0.0, 0.05, 0.19, 0.20, 0.17, 0.07, 0.17]
    if fips in INTERSTATE_COUNTIES:
        base[0] = 0.24 if fips != "013" else 0.33
    if fips not in ("013", "009", "023"):
        base[1] = 0.0
    v = [b * float(rng.uniform(0.85, 1.15)) for b in base]
    t = sum(v)
    return [x / t for x in v]


def family_bounds(obs):
    """Each county's completed deaths under the golden completion and the least and most its family gives."""
    fam = M.g_family(obs)
    out = {}
    for c in W.COUNTIES:
        f = c["fips"]
        ds = [fam[k].get(f, 0.0) for k in fam]
        out[f] = (fam["pooled"].get(f, 0.0), min(ds), max(ds))
    return out


def tables(vmt3):
    """DVMT in thousands, one decimal, by county, year and class, summing to each county's three-year miles."""
    out = {}
    for c in W.COUNTIES:
        f = c["fips"]
        sh = class_shares(f)
        cells = {}
        for y in W.YEARS:
            vy = vmt3[f] * YEAR_SPLIT[y]
            for k, cl in enumerate(CLASSES):
                cells[(y, cl)] = round(vy * sh[k] / DAYS[y] / 1000.0, 1)
        tot = sum(v * 1000.0 * DAYS[y] for (y, cl), v in cells.items())
        big = max(CLASSES, key=lambda cl: cells[(2025, cl)])
        cells[(2025, big)] = round(cells[(2025, big)] + (vmt3[f] - tot) / 1000.0 / DAYS[2025], 1)
        out[f] = cells
    return out


def annual(cells, f, days=None):
    days = days or DAYS
    return {y: sum(v * 1000.0 * days[y] for (yy, cl), v in cells[f].items() if yy == y) for y in W.YEARS}


def place(obs):
    """The three-year miles that put each county's rate in the middle of its two-decimal cell under every member of
    the golden completion's family and under 365 days in 2024: the miles the DOT's tables are written to."""
    bounds = family_bounds(obs)
    knob = {c["fips"]: T.knobs(c["fips"])["vmt3"] * 1e8 for c in W.COUNTIES}
    out = {}
    for c in W.COUNTIES:
        f = c["fips"]
        g, lo, hi = bounds[f]
        k = round(g / knob[f] * 1e8, 2)
        f365 = 1.0 + YEAR_SPLIT[2024] / 366.0 / (1.0 - YEAR_SPLIT[2024] / 366.0)
        v = (lo + hi * f365) / 2.0 / k * 1e8
        x = v / 1e8
        if abs(x - round(x)) < 0.06:                  # a three-year total of whole hundreds of millions reads planted
            x = round(x) + (0.06 if x >= round(x) else -0.06)
            v = x * 1e8
        out[f] = v
    return out, bounds
