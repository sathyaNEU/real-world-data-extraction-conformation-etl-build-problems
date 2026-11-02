"""Fixed parameters of the Ardmuir University Library world (architecture 4)."""
import datetime as dt

SEED = 28104

UTC = dt.timezone.utc
# UK clock changes inside the record (UTC instants)
BST_2025_END = dt.datetime(2025, 10, 26, 1, 0, tzinfo=UTC)
BST_2026_START = dt.datetime(2026, 3, 29, 1, 0, tzinfo=UTC)
BST_2026_END = dt.datetime(2026, 10, 25, 1, 0, tzinfo=UTC)

RECORD_START = dt.datetime(2025, 9, 1, 0, 0, tzinfo=UTC)
EXTRACT = dt.datetime(2026, 10, 31, 5, 40, tzinfo=UTC)      # the October download

# the fund's window (UK local dates), filed in the terms
WIN_START_LOCAL = dt.date(2026, 1, 12)
WIN_END_LOCAL = dt.date(2026, 4, 26)
GRACE_DAYS = 14          # hold-weeks start after the second week
CAP_DAYS = 84            # a hold counts at most twelve weeks
FUND_GBP = 180000

# semesters: (name, teaching start local date, weeks of demand)
SEMESTERS = [
    ("A25", dt.date(2025, 9, 22), 16),
    ("S26", dt.date(2026, 1, 12), 19),
    ("A26", dt.date(2026, 9, 21), 6),
]

# 2026-27 faculties; old (2025-26) faculty codes they absorb
FACULTIES = [
    # code, name, old faculty codes
    ("AHU", "Arts and Humanities", ["AH"]),
    ("SSC", "Social Sciences", ["SS"]),
    ("BUS", "Ardmuir Business School", ["BS"]),
    ("LAW", "Law", ["LW"]),
    ("SAE", "Science and Engineering", ["EN", "PS"]),
    ("LSC", "Life Sciences", ["LS"]),
    ("MED", "Medicine and Dentistry", ["MD"]),
    ("HSC", "Health Sciences", ["NH"]),
]

# behaviour per old faculty: request intensity scale, copies scale, cancel base (per day), sensitivity
# (extra daily cancel probability per expected week of wait ahead)
BEHAVIOUR = {
    # demand: request intensity; copies: copies bought per unit of demand; imp: share of students who give up
    # on a long queue (buy or borrow the book elsewhere); base: daily cancel probability of any waiting hold
    "AH": dict(demand=0.95, copies=1.00, imp=0.10, base=0.004),
    "SS": dict(demand=1.00, copies=1.05, imp=0.14, base=0.004),
    "BS": dict(demand=1.05, copies=1.10, imp=0.55, base=0.005),
    "LW": dict(demand=1.10, copies=0.95, imp=0.62, base=0.005),
    "EN": dict(demand=1.00, copies=1.10, imp=0.22, base=0.004),
    "PS": dict(demand=0.95, copies=1.05, imp=0.18, base=0.004),
    "LS": dict(demand=1.00, copies=1.00, imp=0.20, base=0.004),
    "MD": dict(demand=1.10, copies=1.15, imp=0.58, base=0.005),
    "NH": dict(demand=1.00, copies=0.95, imp=0.40, base=0.005),
}
IMPATIENT_SENS = 0.55     # extra daily cancel probability per week of estimated wait beyond the first

OFFER_HOURS = 48
P_BORROW = 0.86
LOAN_DAYS = [(7, 0.66), (3, 0.19), (1, 0.15)]
P_EARLY_RETURN = 0.24
METER_LOANS = 40

DEMAND_SCALE = 10.0
CROSS_SHARE = 0.5
