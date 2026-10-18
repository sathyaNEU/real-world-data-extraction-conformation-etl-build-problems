"""task160 constants shared by every generator module.

The Two Peninsulas Hospital Association (TPHA, fictional) runs a winter surge staffing pool for its member hospitals:
it books agency RN shifts with two staffing agencies, Crestfield Medical Staffing and Inland Seas Nursing (both
fictional), and funds the agency RN shifts that staff a member's surge unit while the member's surge plan is active.
Each December it files a block for the four weeks from the first Monday in January, set at the pool's expected draw
over those weeks. For 2026-27 the pool grows from the sixteen Southeast and West and Central hospitals it has covered
since November 2021 to 24, the eight North hospitals joining it on 1 November 2026. Every member has filed a daily
capacity report since 1 July 2021. The pool manager pulled every file on Monday 21 December 2026; the capacity census
closes with the census night of Sunday 20 December. The 2027 block is filed on Tuesday 22 December.

The seed was fixed by rule before any data was generated: the task number, then the as-of month and day."""
from __future__ import annotations

import datetime as dt
import os

SEED = 1601221

ORG = "Two Peninsulas Hospital Association"
ORG_SHORT = "TPHA"
POOL = "TPHA Winter Surge Staffing Pool"
AG_C = "Crestfield Medical Staffing"
AG_I = "Inland Seas Nursing"
PEOPLE = {
    "pool_manager": "Greg Matthews",      # winter pool manager: the block, the settlements (the requester)
    "surveillance": "Andrew Harvey",      # surveillance lead: wastewater, admissions outlook, capacity census
    "finance": "Shawn Whitaker",          # TPHA finance manager: the close-out summaries
}

HERE = os.path.dirname(os.path.abspath(__file__))
TASK_DIR = os.path.dirname(HERE)
TARGET = os.path.join(TASK_DIR, "target")

D = dt.date
# ------------------------------------------------------------------------------------------------- calendar
AS_OF = D(2026, 12, 21)                 # Monday, the pull
CENSUS_END = D(2026, 12, 20)            # last census night in the capacity export
CENSUS_START = D(2021, 7, 1)            # the association's capacity system's first census night on file
NEW_SYSTEM = D(2024, 7, 1)              # first census night in the new capacity system
FILE_DATE = D(2026, 12, 22)             # the 2027 block is filed
BLOCK_2027 = (D(2027, 1, 4), D(2027, 1, 31))
NORTH_JOIN = D(2026, 11, 1)
POOL_START = D(2021, 11, 1)

WINTERS = [2022, 2023, 2024, 2025, 2026, 2027]          # labelled by the January they hold
CLOSED = [2022, 2023, 2024, 2025, 2026]


def season_bounds(w):
    """The pool season of the winter whose January falls in year w: 1 November to 31 March."""
    return D(w - 1, 11, 1), D(w, 3, 31)


def block_weeks(w):
    """The four weeks from the first Monday in January of year w."""
    d = D(w, 1, 1)
    while d.weekday() != 0:
        d += dt.timedelta(days=1)
    return d, d + dt.timedelta(days=27)


def daterange(a, b):
    d = a
    while d <= b:
        yield d
        d += dt.timedelta(days=1)


# The Southeast region's wave peak in each winter (the centre of its hospitals' surge spells), the stable lags the
# other regions run behind it, and the widths of the waves. 2027's Southeast peak is the earliest on file.
SE_PEAK = {2022: D(2022, 1, 8), 2023: D(2022, 12, 30), 2024: D(2024, 1, 6), 2025: D(2025, 2, 1),
           2026: D(2026, 1, 15), 2027: D(2026, 12, 8)}
LAG = {"SE": 0.0, "WC": 7.0, "NO": 38.5}
SIG = {"SE": 8.0, "WC": 8.0, "NO": 5.0}
AMP = {"SE": 0.20, "WC": 0.20, "NO": 0.22}

REGIONS = {"SE": "Southeast", "WC": "West and Central", "NO": "North"}

# ------------------------------------------------------------------------------------------------- hospitals
# member_no (old capacity system), facility id (new system), name, city, county, region, staffed med-surg beds,
# surge unit, agency RN shifts a day at Level 1 and Level 2 (the surge plan register), primary agency.
HOSPITALS = [
    ("1104", "MI-0412", "Rouge Park Hospital", "Detroit", "Wayne", "SE", 520, "7 North Overflow", (10, 22), "C"),
    ("1107", "MI-0418", "Zielinski Memorial Hospital", "Hamtramck", "Wayne", "SE", 340, "5 East Surge", (8, 18), "I"),
    ("1112", "MI-0425", "Talcott Hospital", "Mount Clemens", "Macomb", "SE", 310, "3 South Flex", (8, 18), "C"),
    ("1115", "MI-0431", "Oakland Pines Medical Center", "Pontiac", "Oakland", "SE", 430, "6 West Overflow", (10, 22), "C"),
    ("1121", "MI-0437", "Gilmartin Medical Center", "Ypsilanti", "Washtenaw", "SE", 260, "4 North Flex", (6, 14), "I"),
    ("1126", "MI-0442", "Raisin Valley Hospital", "Monroe", "Monroe", "SE", 180, "2 West Surge", (4, 10), "I"),
    ("1130", "MI-0446", "Haldane Community Hospital", "Dearborn", "Wayne", "SE", 300, "8 South Flex", (8, 16), "C"),
    ("1133", "MI-0451", "Tolliver General Hospital", "Southfield", "Oakland", "SE", 280, "5 North Overflow", (8, 18), "C"),
    ("1138", "MI-0455", "Kastner Hospital", "Sterling Heights", "Macomb", "SE", 250, "4 East Surge", (6, 14), "I"),
    ("1202", "MI-0503", "Haverkamp Medical Center", "Grand Rapids", "Kent", "WC", 450, "9 North Overflow", (10, 20), "C"),
    ("1206", "MI-0508", "Kalamazoo Lutheran Hospital", "Kalamazoo", "Kalamazoo", "WC", 300, "4 West Flex", (8, 16), "C"),
    ("1210", "MI-0514", "Ellery Medical Center", "Lansing", "Ingham", "WC", 330, "6 South Overflow", (8, 18), "I"),
    ("1214", "MI-0519", "Brennan Memorial Hospital", "Flint", "Genesee", "WC", 290, "5 West Surge", (6, 14), "C"),
    ("1219", "MI-0523", "Ruddock Hospital", "Saginaw", "Saginaw", "WC", 260, "3 North Flex", (6, 14), "I"),
    ("1223", "MI-0528", "Muskegon Harbor Hospital", "Muskegon", "Muskegon", "WC", 210, "2 East Surge", (4, 10), "I"),
    ("1227", "MI-0532", "Brinkerhoff Memorial Hospital", "Battle Creek", "Calhoun", "WC", 160, "3 West Flex", (4, 10), "C"),
    ("1305", "MI-0604", "Ostrander Medical Center", "Traverse City", "Grand Traverse", "NO", 210, "4 South Overflow", (8, 12), "I"),
    ("1309", "MI-0609", "Lindell Hospital", "Petoskey", "Emmet", "NO", 120, "3 East Flex", (4, 8), "I"),
    ("1312", "MI-0613", "Alpena Lakeside Hospital", "Alpena", "Alpena", "NO", 100, "2 North Surge", (4, 8), "C"),
    ("1316", "MI-0617", "Callister Memorial Hospital", "Gaylord", "Otsego", "NO", 80, "2 West Flex", (4, 6), "I"),
    ("1320", "MI-0622", "Clam Lake Community Hospital", "Cadillac", "Wexford", "NO", 75, "1 South Surge", (2, 4), "I"),
    ("1324", "MI-0626", "Superior Shores Medical Center", "Marquette", "Marquette", "NO", 180, "5 East Overflow", (6, 10), "C"),
    ("1328", "MI-0631", "Little Bay de Noc Hospital", "Escanaba", "Delta", "NO", 70, "1 North Flex", (2, 4), "I"),
    ("1333", "MI-0635", "Ashmun Bay Hospital", "Sault Ste. Marie", "Chippewa", "NO", 60, "1 East Surge", (2, 4), "I"),
]
H_FIELDS = ("member_no", "facility_id", "name", "city", "county", "region", "beds", "surge_unit", "grid", "agency")


def hospitals():
    return [dict(zip(H_FIELDS, h)) for h in HOSPITALS]


def in_pool(h, d):
    """True when hospital h is a pool member on date d."""
    if h["region"] == "NO":
        return d >= NORTH_JOIN
    return d >= POOL_START


# surge plan triggers (the association's model surge plan, every member, unchanged since 2021)
L1_UP, L2_UP, L2_DOWN, L1_DOWN = 0.95, 1.01, 0.98, 0.93
