"""Shared constants and arithmetic for the task124 pack generator (Sabine Crest Energy, summer 2027 block)."""
from __future__ import annotations

import math
from datetime import date, timedelta

import numpy as np

SEED = 124_2027

BOOKS = ["Coast", "East", "Far West", "North", "North Central", "South Central", "Southern", "West"]
CODE = {"Coast": "COAST", "East": "EAST", "Far West": "FWEST", "North": "NORTH", "North Central": "NCENT",
        "South Central": "SCENT", "Southern": "SOUTH", "West": "WEST"}
BOOK_OF_CODE = {v: k for k, v in CODE.items()}
NC = "North Central"
SUMMERS = list(range(2017, 2027))

# ERCOT summer system peaks as this pack carries them (date, hour ending CPT, MW). Constructed for the task,
# shaped on the published summer peaks; not a transcription.
PEAKS = {
    2017: (date(2017, 7, 28), 17, 69_377), 2018: (date(2018, 7, 19), 17, 73_259),
    2019: (date(2019, 8, 12), 17, 74_664), 2020: (date(2020, 8, 14), 17, 74_102),
    2021: (date(2021, 8, 26), 17, 73_518), 2022: (date(2022, 7, 20), 17, 79_871),
    2023: (date(2023, 8, 10), 17, 85_312), 2024: (date(2024, 8, 20), 18, 85_407),
    2025: (date(2025, 8, 18), 18, 84_066), 2026: (date(2026, 7, 29), 17, 86_741),
}

EXTRACT = date(2027, 4, 9)
AS_OF = date(2027, 4, 12)
SEASON_START = date(2027, 6, 1)

HEDGES = {"Coast": 475, "East": 145, "Far West": 95, "North": 80, "North Central": 365, "South Central": 280,
          "Southern": 120, "West": 135}
BLOCK, LOT = 400, 5

# uncovered exposure before the block the answer is built to (MW, unrounded targets for the factor scale solve)
TARGET_EXPOSURE = {"Coast": 251.214, "East": 160.012, "Far West": 113.908, "North": 96.118,
                   "North Central": 340.204, "South Central": 155.096, "Southern": 147.231, "West": 106.142}

FIRST_YEAR_BOOK = 2008
READ_HOURS = list(range(11, 21))        # hours ending 11..20 in the IDR extract
WINDOW_HOURS = [15, 16, 17, 18]          # a called window, 14:00 to 18:00 CPT (hours ending 15..18)

# a member's uncalled draw rises with its zone's heat: ordinary afternoons at its base level, design-day afternoons
# (every closed system peak among them) at its full-load level, a linear rise between the two heat marks
HEAT_LO, HEAT_SAT = 0.68, 0.78
FULL_LIFT, ORDINARY_DROP = 0.08, 0.22
TEMP_SCALE, TEMP_NOISE = 30.0, 0.7      # degrees F of zone maximum per unit of the heat index; vendor scatter
TEMP_BASE = {"Coast": 91, "East": 92, "Far West": 96, "North": 97, "North Central": 95, "South Central": 95,
             "Southern": 94, "West": 95}


def p90(x, method="linear"):
    return float(np.percentile(np.asarray(x, float), 90, method=method))


def lots(E, order=None, total=BLOCK, lot=LOT):
    order = order or BOOKS
    a = {z: 0 for z in E}
    for _ in range(total // lot):
        z = max(order, key=lambda k: (E[k] - a[k], -order.index(k)))
        a[z] += lot
    return a


def lot_margins(E, total=BLOCK, lot=LOT):
    """Lowest value at which a lot was taken and highest value at which none was, over the whole levelling."""
    a = lots(E)
    taken = [E[z] - lot * k for z in E for k in range(a[z] // lot)]
    nxt = [E[z] - a[z] for z in E]
    return min(taken), max(nxt)


def water_level(E, total=BLOCK):
    lo, hi = -1000.0, 2000.0
    for _ in range(200):
        w = (lo + hi) / 2
        s = sum(max(0.0, E[z] - w) for z in E)
        lo, hi = (lo, w) if s < total else (w, hi)
    return (lo + hi) / 2


def continuous_split(E, total=BLOCK):
    w = water_level(E, total)
    return w, {z: max(0.0, E[z] - w) for z in E}


def round_half_up(x: float, step: float = 1.0) -> float:
    return math.floor(x / step + 0.5) * step


def daterange(d0: date, d1: date):
    d = d0
    while d <= d1:
        yield d
        d += timedelta(days=1)


def nerc_holidays(year: int) -> set[date]:
    def obs(d):
        return d + timedelta(days=1) if d.weekday() == 6 else d
    out = {obs(date(year, 1, 1)), obs(date(year, 7, 4)), obs(date(year, 12, 25))}
    d = date(year, 5, 31)
    while d.weekday() != 0:
        d -= timedelta(days=1)
    out.add(d)  # Memorial Day
    d = date(year, 9, 1)
    while d.weekday() != 0:
        d += timedelta(days=1)
    out.add(d)  # Labor Day
    d = date(year, 11, 1)
    n = 0
    while True:
        if d.weekday() == 3:
            n += 1
            if n == 4:
                break
        d += timedelta(days=1)
    out.add(d)  # Thanksgiving
    return out


def billing_holidays(year: int) -> set[date]:
    """Independence Day (Friday before a Saturday, Monday after a Sunday) and Labor Day, the two summer days the
    programme calendar treats as non-business days."""
    j = date(year, 7, 4)
    if j.weekday() == 5:
        j -= timedelta(days=1)
    elif j.weekday() == 6:
        j += timedelta(days=1)
    d = date(year, 9, 1)
    while d.weekday() != 0:
        d += timedelta(days=1)
    return {j, d}


def summer_weekdays(year: int) -> list[date]:
    return [d for d in daterange(date(year, 6, 1), date(year, 9, 30)) if d.weekday() < 5]


def onpeak_hours(year: int, month: int, holidays=True) -> int:
    hol = nerc_holidays(year) if holidays else set()
    d, n = date(year, month, 1), 0
    while d.month == month:
        if d.weekday() < 5 and d not in hol:
            n += 1
        d += timedelta(days=1)
    return 16 * n


def all_hours_7x16(year: int, month: int) -> int:
    d, n = date(year, month, 1), 0
    while d.month == month:
        n += 1
        d += timedelta(days=1)
    return 16 * n


def bin_distance(x: float, step: float) -> float:
    """Distance from x to the nearest rounding edge of a grid of the given step (half-step boundaries)."""
    r = (x / step) % 1.0
    return abs(r - 0.5) * step
