"""task165 constants and helpers shared by every generator module.

The City of Quellbrook's roads division buys rock salt under a supply contract that rolls over each 1 October at the
tonnage delivered in the supply season just closed (39,100 t for 2025-26). Seasonal tonnage above it is committed by
1 October for each change in winter service approved since that winter closed. On 30 August 2026 Quellbrook Regional
Transit launched its redesigned bus network and the route audit moved 424.0 lane-km of collectors carrying the new
frequent service from Priority 2 (salted at intersections, hills and curves) to Priority 1 (bare pavement). Every file
was pulled on Friday 25 September 2026.

The seed was fixed by rule before any data was generated: the task number, then the as-of month and day."""
from __future__ import annotations

import datetime as dt
import hashlib
import os

SEED = 1650925

CITY = "Quellbrook"
ORG = "City of Quellbrook"
DEPT = "Public Works, Roads Division"
TRANSIT = "Quellbrook Regional Transit"
SUPPLIER = "Northgrit Salt Supply Ltd."
SURVEYOR = "Tessaline Geomatics Inc."
CONTRACTOR = "Kettlewood Road Services"
PEOPLE = {
    "winter_manager": "Doris Wilkerson",   # manager, winter operations: the winter maintenance plan
    "transit_planner": "Kristin Gonzalez",  # QRT service planning: the frequent network street list
    "director": "Andre Nixon",             # director of roads: approves the division's plan and procedures
}

HERE = os.path.dirname(os.path.abspath(__file__))
TASK_DIR = os.path.dirname(HERE)
TARGET = os.path.join(TASK_DIR, "target")

UTC = dt.timezone.utc

# ------------------------------------------------------------------------------------------------- calendar
AS_OF = dt.date(2026, 9, 25)                   # Friday, the pull
PULL_LOCAL = dt.datetime(2026, 9, 25, 10, 15)  # local time of the pull
COMMIT_BY = dt.date(2026, 10, 1)
REDESIGN = dt.date(2026, 8, 30)                # the frequent network launch and the route audit's entries
REALIGN = dt.date(2026, 7, 1)                  # yard boundary realignment (arterials only)
AVL_CUTOVER = dt.date(2023, 10, 1)             # telematics platform replaces the legacy AVL
WINTERS = ["2021-22", "2022-23", "2023-24", "2024-25", "2025-26"]
NEW_WINTERS = ["2023-24", "2024-25", "2025-26"]
LEGACY_WINTERS = ["2021-22", "2022-23"]
SEASON = {w: (dt.date(int(w[:4]), 11, 1), dt.date(int(w[:4]) + 1, 3, 31)) for w in WINTERS}
PLANNING_SEVERITY = 61.7                       # WSI points, the 1991-2020 average of the index
# each winter's Winter Severity Index (sum of event points, 1 November to 31 March)
WSI_TARGET = {"2021-22": 63.4, "2022-23": 50.1, "2023-24": 38.9, "2024-25": 67.2, "2025-26": 58.4}
MOVE_DATES = {"A": dt.date(2022, 11, 1), "B": dt.date(2023, 11, 1), "C": dt.date(2024, 11, 1),
              "D": dt.date(2025, 11, 1)}
FIRST_P1_WINTER = {"A": "2022-23", "B": "2023-24", "C": "2024-25", "D": "2025-26"}

YARDS = ["KLV", "MPF", "RDG", "LKS"]
YARD_NAMES = {"KLV": "Kelvin Road Yard", "MPF": "Mapleford Yard", "RDG": "Ridge Yard", "LKS": "Lakeshore Yard"}

# Eastern time: daylight saving from the second Sunday in March to the first Sunday in November
def _nth_sunday(year, month, n):
    d = dt.date(year, month, 1)
    while d.weekday() != 6:
        d += dt.timedelta(days=1)
    return d + dt.timedelta(days=7 * (n - 1))


def utc_offset_hours(local: dt.datetime) -> int:
    """Hours to add to local Eastern time to reach UTC (5 in standard time, 4 in daylight time)."""
    y = local.year
    start = dt.datetime.combine(_nth_sunday(y, 3, 2), dt.time(2, 0))
    end = dt.datetime.combine(_nth_sunday(y, 11, 1), dt.time(2, 0))
    return 4 if start <= local < end else 5


def to_utc(local: dt.datetime) -> dt.datetime:
    return local + dt.timedelta(hours=utc_offset_hours(local))


def to_local(utc: dt.datetime) -> dt.datetime:
    guess = utc - dt.timedelta(hours=5)
    off = utc_offset_hours(guess + dt.timedelta(hours=1))
    return utc - dt.timedelta(hours=off)


def winter_of(d: dt.date):
    for w, (a, b) in SEASON.items():
        if a <= d <= b:
            return w
    return None


def stable_int(*parts) -> int:
    h = hashlib.sha256("|".join(str(p) for p in parts).encode()).hexdigest()
    return int(h[:12], 16)


def bin_edge_distance(v, unit):
    """Distance from v to the nearest edge of the printed cell round(v/unit)*unit."""
    return unit / 2 - abs(v - round(v / unit) * unit)
