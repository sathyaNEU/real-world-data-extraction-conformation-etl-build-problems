"""The world of task452: the Brannoch Lake Commission's water-year phosphorus load inventory. Constants only."""
import datetime as dt

D = dt.date
SEED = 4522

WY_START = D(2023, 10, 1)            # water year 2024 opens the monitoring record
WY_END = D(2026, 9, 30)              # water year 2026 closes it
WY = 2026
WY26_START = D(2025, 10, 1)
PROVISIONAL_PULL = D(2026, 10, 6)    # the provisional unit values pulled after the water year closed
APPROVED = D(2026, 12, 14)           # the approved water-year 2026 record replaces the provisional one
EXPORT = D(2027, 1, 8)               # the laboratory and gage exports
COMMITTEE = D(2027, 1, 21)           # the technical committee selects the 2027 projects
LAB_CHANGE = D(2025, 7, 1)           # the commission's contract laboratory reports in ug/L from this date

COMMISSION = "Brannoch Lake Commission"
LAKE = "Lake Brannoch"
AGREEMENT = "Brannoch Lake Phosphorus Agreement"
FUND = "Tributary Restoration Fund"
LAB = "Ashgrove College Watershed Laboratory"
GAGER = "Merrifield Hydrometrics"
LAB_OLD = "Ledgemere Environmental Laboratory"     # the commission's contract laboratory to 30 June 2025
LAB_NEW = "Quarry Hill Analytical"                 # from 1 July 2025 (results in ug/L)
PROGRAM = "Brannoch Basin Farm Practice Program"

PEOPLE = {
    "director": ("Matthew Douglas", "Executive Director, Brannoch Lake Commission"),
    "manager": ("Kathy Dominguez", "Water Quality Program Manager, Brannoch Lake Commission"),
    "lab": ("Troy Ramirez", "Director, Ashgrove College Watershed Laboratory"),
    "hydro": ("Loretta Soto", "Hydrologist, Merrifield Hydrometrics"),
}

CFS_DAY_KG = 0.028316846592 * 86400 * 1000 / 1e6     # mg/L x ft3/s x one day -> kg (2.4466)

# code, name, commission station, lab station, gage, station drainage km2, gage drainage km2,
# median flow cfs, flashiness, ln c0 (mg/L at median flow), C-Q slope b, residual sigma, seasonal amp,
# where the laboratory's water-year 2026 storm samples fell (low: modest storms; high: the snowmelt peaks), role
TRIBS = [
    ("FAL", "Fallowmere Brook", "BLC-01", "ACWL-FB", "01-4410", 58.2, 58.2, 21.0, 0.9, -3.30, 0.42, 0.30, 0.04, "low", "clear"),
    ("KES", "Kestle River", "BLC-02", "ACWL-KR", "01-4420", 241.6, 241.6, 96.0, 1.5, -2.95, 0.82, 0.32, 0.04, "low", "gold_top"),
    ("ORR", "Orrinwood Brook", "BLC-03", "ACWL-OB", "01-4430", 74.9, 74.9, 30.0, 1.0, -2.85, 0.55, 0.28, 0.04, "high", "interp_top"),
    ("TAM", "Tamsell River", "BLC-04", "ACWL-TR", "01-4440", 188.3, 188.3, 70.0, 0.8, -3.40, 0.35, 0.28, 0.04, "mid", "clear"),
    ("VAR", "Varrow Brook", "BLC-05", "ACWL-VB", "01-4450", 96.4, 96.4, 38.0, 1.1, -2.70, 0.60, 0.30, 0.04, "mid", "both_top"),
    ("HES", "Hessick River", "BLC-06", "ACWL-HR", "01-4460", 152.7, 152.7, 58.0, 1.3, -2.90, 0.68, 0.30, 0.04, "low", "gold_top"),
    ("PEL", "Pellow Brook", "BLC-07", "ACWL-PB", "01-4470", 41.3, 41.3, 15.0, 0.9, -3.20, 0.45, 0.30, 0.04, "mid", "clear"),
    ("AMB", "Ambrey River", "BLC-08", "ACWL-AR", "01-4480", 133.5, 133.5, 52.0, 1.0, -3.05, 0.62, 0.30, 0.04, "high", "interp_top"),
    ("DUN", "Dunmarsh Brook", "BLC-09", "ACWL-DB", "01-4490", 61.4, 52.8, 19.0, 1.1, -3.10, 0.50, 0.30, 0.04, "mid", "clear"),
    ("COR", "Corriden River", "BLC-10", "ACWL-CR", "01-4500", 207.9, 207.9, 82.0, 0.9, -3.35, 0.40, 0.28, 0.04, "mid", "clear"),
]
CODES = [t[0] for t in TRIBS]
PRIOR_STORMS = {}                  # the laboratory's storm samples a year in water years 2024 and 2025 (3 where unlisted)
NAME = {t[0]: t[1] for t in TRIBS}
ROLE = {t[0]: t[-1] for t in TRIBS}

# streams that join a tributary above its compliance station (the commission's stream network)
SUBSTREAMS = [
    # stream, flows into, joins at river km of the receiving stream
    ("Hollin Brook", "Kestle River", 14.2),
    ("Kestle River North Branch", "Kestle River", 22.8),
    ("Sedge Run", "Hessick River", 9.6),
    ("Little Varrow Brook", "Ambrey River", 11.3),       # named for the Varrow valley it drains from, but it feeds the Ambrey
    ("Copse Brook", "Varrow Brook", 6.1),
    ("Mill Tail Brook", "Tamsell River", 12.4),
    ("Frayne Brook", "Fallowmere Brook", 4.9),
    ("Orrin Mill Brook", "Orrinwood Brook", 3.7),
    ("Tine Brook", "Pellow Brook", 2.8),
    ("Hask Brook", "Corriden River", 15.5),
    ("Dunmarsh Brook West Branch", "Dunmarsh Brook", 7.2),
]
# each compliance station's river km above the lake on its own tributary
STATION_RKM = {"FAL": 1.2, "KES": 3.4, "ORR": 0.9, "TAM": 2.6, "VAR": 1.8, "HES": 4.1, "PEL": 0.7, "AMB": 2.2, "DUN": 1.5,
               "COR": 3.0}

# permitted wastewater facilities: id, name, receiving water, outfall river km on it, design MGD, typical TP mg/L,
# reports (conc: mg/L with flow, mass: lb/d), resubmitted months (index 0 = October 2025), relocation
FACILITIES = [
    ("NE0100211", "Kestle Falls Wastewater Treatment Facility", "Kestle River", 9.8, 0.85, 0.62, "conc", (3,), None),
    ("NE0100327", "Hollin Village Wastewater Treatment Facility", "Hollin Brook", 2.1, 0.22, 0.95, "conc", (), None),
    ("NE0100433", "Hessick Mills Wastewater Treatment Facility", "Hessick River", 11.6, 0.60, 0.70, "mass", (7,), None),
    ("NE0100519", "Sedge Run Cheese Company", "Sedge Run", 1.4, 0.08, 4.10, "conc", (), None),
    ("NE0100625", "Varrow Wastewater Treatment Facility", "Varrow Brook", 4.4, 0.45, 0.55, "conc", (5,), None),
    ("NE0100741", "Little Varrow School District", "Little Varrow Brook", 3.2, 0.03, 2.60, "conc", (), None),
    ("NE0100857", "Ambrey Village Wastewater Treatment Facility", "Ambrey River", 5.3, 0.38, 0.80, "conc", (2,), (6, 0.8)),
    ("NE0100963", "Tamsell Wastewater Treatment Facility", "Mill Tail Brook", 1.9, 0.30, 0.65, "mass", (), None),
    ("NE0101079", "Fallowmere Inn and Conference Center", "Frayne Brook", 0.6, 0.02, 3.10, "conc", (9,), None),
    ("NE0101185", "Orrinwood Wastewater Treatment Facility", "Orrinwood Brook", 2.7, 0.33, 0.58, "conc", (), None),
    ("NE0101291", "Pellow Junction Wastewater Treatment Facility", "Tine Brook", 1.1, 0.12, 0.90, "conc", (4,), None),
    ("NE0101307", "Corriden Wastewater Treatment Facility", "Corriden River", 6.8, 0.70, 0.48, "mass", (), None),
    ("NE0101413", "Dunmarsh Wastewater Treatment Facility", "Dunmarsh Brook", 0.8, 0.26, 0.75, "conc", (), None),
    ("NE0101529", "West Branch Creamery", "Dunmarsh Brook West Branch", 1.6, 0.05, 3.40, "conc", (8,), None),
    ("NE0101635", "Orrin Mill Apartments", "Orrin Mill Brook", 1.0, 0.02, 2.90, "conc", (), None),
    ("NE0101741", "Hask Brook Mobile Home Park", "Hask Brook", 1.3, 0.015, 3.50, "conc", (), None),
    ("NE0101857", "Varrow Valley Fish Hatchery", "Copse Brook", 0.9, 1.20, 0.09, "conc", (), None),
]
GAL_L = 3.785411784
LB_KG = 0.45359237
# the smaller dischargers monitor phosphorus quarterly under their permits: each report covers a calendar quarter
QUARTERLY = {"NE0100327", "NE0100519", "NE0100741", "NE0100963", "NE0101079", "NE0101185", "NE0101291", "NE0101413",
             "NE0101529", "NE0101635", "NE0101741", "NE0101857"}

# cover crop contracts: farms per watershed in the practice program
PRACTICE_CODE = "340"       # cover crop

# weather stations (precipitation, a distractor) and lake stations (in-lake monitoring, a distractor)
WEATHER = [("BLC-W1", "Brannoch Harbor"), ("BLC-W2", "Kestle Falls"), ("BLC-W3", "Hessick Mills")]
LAKE_STATIONS = [("BL-02", "North Basin"), ("BL-04", "Kestle Bay"), ("BL-07", "Main Lake"), ("BL-09", "Ambrey Arm"),
                 ("BL-11", "South Basin")]
# Eastern time: daylight time over water year 2026
DST = [(D(2025, 3, 9), D(2025, 11, 2)), (D(2026, 3, 8), D(2026, 11, 1)), (D(2024, 3, 10), D(2024, 11, 3)),
       (D(2023, 3, 12), D(2023, 11, 5))]


def utc_offset(d):
    """hours behind UTC after 2am on a local date (5 standard, 4 daylight)"""
    return 4 if any(a <= d < b for a, b in DST) else 5


def utc_offset_at(t):
    """hours behind UTC at a UTC instant: daylight time runs from 2am standard time (07:00 UTC) on the start date to
    2am daylight time (06:00 UTC) on the end date"""
    for a, b in DST:
        if dt.datetime(a.year, a.month, a.day, 7) <= t < dt.datetime(b.year, b.month, b.day, 6):
            return 4
    return 5


def local_of(t):
    """the local (Eastern) wall-clock time of a UTC instant"""
    return t - dt.timedelta(hours=utc_offset_at(t))
