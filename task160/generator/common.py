"""task160 constants shared by every generator module.

The Tri-Region Hospital Cooperative (TRHC, fictional) is a member-owned cooperative of hospitals in three regions: the
Southeast (Georgia and South Carolina), Central (Tennessee, Kentucky and West Virginia) and the North (northern
Michigan). It runs a winter surge staffing pool for its members: it books agency RN shifts with two staffing agencies,
Crestfield Medical Staffing and Inland Seas Nursing (both fictional), and funds the agency RN shifts that staff a
member's surge unit while the member's surge plan is active. Each December it files a block for the four weeks from
the first Monday in January, set at the pool's expected draw over those weeks. For 2026-27 the pool grows from the
sixteen Southeast and Central hospitals it has covered since November 2021 to 24, the eight North hospitals joining it
on 1 November 2026. Every member has filed a daily capacity report since 1 July 2021. Every member sits in Eastern time.
The pool manager pulled every file on Monday 21 December 2026; the capacity census closes with the census night of
Sunday 20 December. The 2027 block is filed on Tuesday 22 December.

The seed was fixed by rule before any data was generated: the task number, then the as-of month and day."""
from __future__ import annotations

import datetime as dt
import os

SEED = 1601221

ORG = "Tri-Region Hospital Cooperative"
ORG_SHORT = "TRHC"
POOL = "TRHC Winter Surge Staffing Pool"
AG_C = "Crestfield Medical Staffing"
AG_I = "Inland Seas Nursing"
PEOPLE = {
    "pool_manager": "Brandon Williams",   # winter pool manager: the block, the settlements (the requester)
    "surveillance": "Linda Ashley",       # surveillance lead: wastewater, admissions outlook, capacity census
    "finance": "Shawn Whitaker",          # TRHC finance manager: the close-out summaries
}

HERE = os.path.dirname(os.path.abspath(__file__))
TASK_DIR = os.path.dirname(HERE)
TARGET = os.path.join(TASK_DIR, "target")

D = dt.date
# ------------------------------------------------------------------------------------------------- calendar
AS_OF = D(2026, 12, 21)                 # Monday, the pull
CENSUS_END = D(2026, 12, 20)            # last census night in the capacity export
CENSUS_START = D(2021, 7, 1)            # the cooperative's capacity system's first census night on file
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


# The Southeast's wave peak in each winter (the centre of its hospitals' surge spells); Central's gap behind it, a
# few days in most winters and two and a half weeks in 2024-25, with the route the wave takes inland; the North's lag
# behind Central, its upstream, about four weeks give or take a few days; and each region's wave width and size in each
# winter. This winter's Southeast peak is a month earlier than any on file, and Central trails it by two and a half
# weeks, as in 2024-25.
SE_PEAK = {2022: D(2022, 1, 10), 2023: D(2022, 12, 30), 2024: D(2024, 1, 9), 2025: D(2025, 1, 25),
           2026: D(2026, 1, 17), 2027: D(2026, 11, 25)}
CE_GAP = {2022: 4.0, 2023: 6.0, 2024: 2.0, 2025: 17.0, 2026: 5.0, 2027: 19.0}
NO_LAG = {2022: 33.0, 2023: 35.75, 2024: 28.0, 2025: 31.75, 2026: 33.5, 2027: 31.0}
SIG = {"SE": 7.0, "CE": 4.5, "NO": 3.6}
SIG_W = {"SE": {2022: 1.05, 2023: 0.92, 2024: 1.00, 2025: 1.10, 2026: 0.95, 2027: 1.00},
         "CE": {2022: 0.94, 2023: 1.06, 2024: 1.02, 2025: 0.92, 2026: 1.08, 2027: 0.96},
         "NO": {2022: 1.04, 2023: 0.95, 2024: 1.06, 2025: 1.12, 2026: 0.97, 2027: 1.00}}
AMP = {"SE": 0.20, "CE": 0.20, "NO": 0.245}
AMP_W = {"SE": {2022: 1.06, 2023: 0.93, 2024: 1.09, 2025: 0.95, 2026: 1.02},
         "CE": {2022: 0.96, 2023: 1.07, 2024: 0.94, 2025: 1.05, 2026: 1.00},
         "NO": {2022: 0.972, 2023: 0.971, 2024: 0.936, 2025: 0.959, 2026: 0.926}}
MEMBER_OFF = {"SE": 1.6, "CE": 1.6, "NO": 1.9}          # each member's stable offset, days
MEMBER_JIT = {"SE": 2.3, "CE": 1.8, "NO": 1.9}          # a winter's jitter on it, days
MEMBER_AMP_SD = {"SE": 0.07, "CE": 0.07, "NO": 0.05}
MEMBER_SIG_SD = 0.08
SKEW = {"SE": 0.07, "CE": 0.07, "NO": 0.05}             # a wave rises faster than it falls

REGIONS = {"SE": "Southeast", "CE": "Central", "NO": "North"}

# ------------------------------------------------------------------------------------------------- hospitals
# member_no (old capacity system), facility id (new system), name, city, county, region, staffed med-surg beds,
# surge unit, agency RN shifts a day at Level 1 and Level 2 (the surge plan register), primary agency.
HOSPITALS = [
    ("1104", "GA-0412", "Talcott Hospital", "Atlanta", "Fulton", "SE", 520, "7 North Overflow", (10, 24), "C"),
    ("1107", "GA-0418", "Tolliver General Hospital", "Decatur", "DeKalb", "SE", 340, "5 East Surge", (8, 18), "I"),
    ("1112", "GA-0425", "Gilmartin Medical Center", "Marietta", "Cobb", "SE", 310, "3 South Flex", (8, 18), "C"),
    ("1115", "GA-0431", "Satterfield Medical Center", "Lawrenceville", "Gwinnett", "SE", 430, "6 West Overflow", (10, 24), "C"),
    ("1121", "GA-0437", "Haldane Community Hospital", "Macon", "Bibb", "SE", 260, "4 North Flex", (6, 14), "I"),
    ("1126", "GA-0442", "Lattimore Memorial Hospital", "Rome", "Floyd", "SE", 180, "2 West Surge", (4, 10), "I"),
    ("1130", "SC-0446", "Brennan Memorial Hospital", "Columbia", "Richland", "SE", 300, "8 South Flex", (8, 18), "C"),
    ("1133", "SC-0451", "Kinard Hospital", "Greenville", "Greenville", "SE", 280, "5 North Overflow", (8, 18), "C"),
    ("1138", "SC-0455", "Ruddock Hospital", "Spartanburg", "Spartanburg", "SE", 250, "4 East Surge", (6, 14), "I"),
    ("1202", "TN-0503", "Haverkamp Medical Center", "Knoxville", "Knox", "CE", 450, "9 North Overflow", (10, 22), "C"),
    ("1206", "TN-0508", "Kastner Hospital", "Chattanooga", "Hamilton", "CE", 300, "4 West Flex", (8, 18), "C"),
    ("1210", "KY-0514", "Ellery Medical Center", "Lexington", "Fayette", "CE", 330, "6 South Overflow", (8, 20), "I"),
    ("1214", "KY-0519", "Brinkerhoff Memorial Hospital", "Louisville", "Jefferson", "CE", 290, "5 West Surge", (6, 14), "C"),
    ("1219", "WV-0523", "Zielinski Memorial Hospital", "Charleston", "Kanawha", "CE", 260, "3 North Flex", (6, 14), "I"),
    ("1223", "WV-0528", "Spurlock Memorial Hospital", "Huntington", "Cabell", "CE", 210, "2 East Surge", (4, 10), "I"),
    ("1227", "TN-0532", "Crumley Memorial Hospital", "Johnson City", "Washington", "CE", 160, "3 West Flex", (4, 10), "C"),
    ("1305", "MI-0604", "Ostrander Medical Center", "Traverse City", "Grand Traverse", "NO", 210, "4 South Overflow", (10, 16), "I"),
    ("1309", "MI-0609", "Lindell Hospital", "Petoskey", "Emmet", "NO", 120, "3 East Flex", (6, 10), "I"),
    ("1312", "MI-0613", "Alpena Lakeside Hospital", "Alpena", "Alpena", "NO", 100, "2 North Surge", (4, 10), "C"),
    ("1316", "MI-0617", "Callister Memorial Hospital", "Gaylord", "Otsego", "NO", 80, "2 West Flex", (4, 8), "I"),
    ("1320", "MI-0622", "Clam Lake Community Hospital", "Cadillac", "Wexford", "NO", 75, "1 South Surge", (2, 6), "I"),
    ("1324", "MI-0626", "Superior Shores Medical Center", "Marquette", "Marquette", "NO", 180, "5 East Overflow", (8, 12), "C"),
    ("1328", "MI-0631", "Little Bay de Noc Hospital", "Escanaba", "Delta", "NO", 70, "1 North Flex", (2, 4), "I"),
    ("1333", "MI-0635", "Ashmun Bay Hospital", "Sault Ste. Marie", "Chippewa", "NO", 60, "1 East Surge", (2, 6), "I"),
]
H_FIELDS = ("member_no", "facility_id", "name", "city", "county", "region", "beds", "surge_unit", "grid", "agency")


def hospitals():
    out = [dict(zip(H_FIELDS, h)) for h in HOSPITALS]
    for h in out:
        h["state"] = h["facility_id"][:2]
    return out


def in_pool(h, d):
    """True when hospital h is a pool member on date d."""
    if h["region"] == "NO":
        return d >= NORTH_JOIN
    return d >= POOL_START


# surge plan triggers (the cooperative's model surge plan, every member, unchanged since 2021)
L1_UP, L2_UP, L2_DOWN, L1_DOWN = 0.95, 1.01, 0.98, 0.93
