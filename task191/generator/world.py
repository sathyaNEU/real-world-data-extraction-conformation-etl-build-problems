"""Stroomhuis: the fixed world behind the April 2027 interconnect augment decision."""
import datetime as dt

SEED = 191
AS_OF = dt.date(2027, 4, 12)               # the telemetry extract date
COMMITTEE = dt.date(2027, 4, 19)           # the capacity committee sits
Q_FROM = dt.date(2027, 1, 1)               # the quarter the decision is about
Q_TO = dt.date(2027, 3, 31)
PRIOR_FROM = dt.date(2025, 1, 1)           # the eight quarters the daily rollup covers
PRIOR_TO = dt.date(2026, 12, 31)

PLATFORM = "Stroomhuis"
REGULATOR = ""                             # none: this is a commercial platform
PEOPLE = {"lead": "Amelia Jekel",          # network planning lead
          "ops": "Rick Claassen"}          # the network operations manager

# the retained minute bands, in local time, and the three evening windows the standard reports on
EVENING_BAND = (19, 22)                    # 19:00 to 21:59 local
DAY_BAND = (12, 15)                        # 12:00 to 14:59 local, the reference band
WINDOWS = [("19:00 to 19:59", 19), ("20:00 to 20:59", 20), ("21:00 to 21:59", 21)]

# (port code, peer, access network type, capacity Gbps, evening load, own spread)
PATHS = [
    ("KZD-01", "Kabelnet Zuid",      "cable",     400, 1.00, 1.00),
    ("VSN-01", "Vastnet",            "fibre",     400, 0.96, 0.94),
    ("DLF-01", "Delfzicht Breedband", "fibre",    200, 1.21, 0.84),
    ("RHN-01", "Rhenia Telecom",     "cable",     200, 0.99, 1.10),
    ("STR-01", "Stroomnet",          "fibre",     100, 0.98, 0.99),
    ("OPL-01", "Opaalnet",           "fixed wireless", 100, 1.02, 1.06),
    ("HVT-01", "Haventrans",         "cable",     100, 0.93, 0.97),
]
RENAMED = ("HAV-01", "HVT-01", dt.date(2027, 2, 12))   # the port renamed inside the quarter
MAINTENANCE = ("STR-01", dt.date(2027, 2, 2), dt.date(2027, 2, 10))   # nine evenings
DST_SPRING = dt.date(2027, 3, 28)          # the Netherlands moves to summer time inside the quarter
# what the maintenance window does to the path it is on: the port runs on one card while the other
# is replaced, so the evening shortfall there is several times its own
MAINTENANCE_LIFT = 2.08
# evening load grew through the two prior years and flattened over the winter
LOAD_TREND = {"2025Q1": 0.93, "2025Q2": 0.95, "2025Q3": 0.97, "2025Q4": 1.00,
              "2026Q1": 1.02, "2026Q2": 1.04, "2026Q3": 1.07, "2026Q4": 1.10,
              "2027Q1": 1.06}
# the worst evening window each quarter's own record shows, which the calibration solves the
# quarter's measurement spread to hit
WORST_WINDOW = {"2025Q1": 392, "2025Q2": 368, "2025Q3": 352, "2025Q4": 441,
                "2026Q1": 489, "2026Q2": 379, "2026Q3": 361, "2026Q4": 452, "2027Q1": 412}
TARGET_ROWS = 25000
