"""Drumlorne: the site, the dwellings, the meters, the survey weeks and the designed levels.

Nothing in this module ships. The designed specific levels and residuals fix the world; every figure the
pack and the goldens carry is measured from the built data (dataset-generation 6.1).
"""
import datetime as dt

SITE = "Drumlorne"
OPERATOR = "Tulcarra Foods"
VILLAGE = "Clonaraght"
PLANT = "effluent treatment plant"
EXTRACT = dt.date(2026, 10, 16)
ORDER_DAY = dt.date(2026, 10, 26)
SURVEY_START = dt.date(2026, 8, 31)
SURVEY_END = dt.date(2026, 10, 11)

PEOPLE = {
    "engineer": ("Keelan Moher", "KM"),
    "operations": ("Aiden Hawthorn", "AH"),
    "technician": ("Orla O'Hurley", "OOH"),
    "operator": ("Cormac Cashman", "CC"),
    "planner": ("Helen Deeny", "HD"),
}

# Assessment period, local time (noise_management_plan 3.2).
DAY_START, DAY_END = 7, 19

# Six survey weeks, Monday to Sunday.
WEEKS = [dt.date(2026, 8, 31) + dt.timedelta(days=7 * i) for i in range(6)]

# The plant's weekly planned process stop (local), and the unplanned stops, as the event log records them.
PLANNED_STOPS = [
    (dt.datetime(2026, 9, 1, 13, 0), 120, "weekly MCC inspection and belt check"),
    (dt.datetime(2026, 9, 8, 9, 30), 120, "weekly MCC inspection and belt check"),
    (dt.datetime(2026, 9, 15, 14, 0), 120, "weekly MCC inspection, blower strainer clean"),
    (dt.datetime(2026, 9, 22, 10, 0), 120, "weekly MCC inspection and belt check"),
    (dt.datetime(2026, 9, 29, 13, 30), 120, "weekly MCC inspection, centrifuge scroll check"),
    (dt.datetime(2026, 10, 6, 8, 30), 120, "weekly MCC inspection and belt check"),
]
UNPLANNED_STOPS = [
    (dt.datetime(2026, 9, 10, 11, 20), 25, "balance tank high level alarm"),
    (dt.datetime(2026, 9, 23, 15, 5), 40, "blower 2 bearing temperature trip"),
    (dt.datetime(2026, 10, 2, 2, 10), 18, "ESB supply dip, all drives tripped"),
]

# Equipment the three noise sources run on.
BLOWERS = ["BL-01", "BL-02", "BL-03"]
CENTRIFUGES = ["CF-01", "CF-02"]
ENGINE = "CHP-01"

# The five meters. The one-third-octave module is licensed on the first three only.
METERS = [
    {"id": "M1", "serial": "SLM-21884", "model": "Class 1 logging sound level meter", "bands": True,
     "pre": 93.9, "post": 94.0},
    {"id": "M2", "serial": "SLM-21907", "model": "Class 1 logging sound level meter", "bands": True,
     "pre": 94.0, "post": 94.8},
    {"id": "M3", "serial": "SLM-22043", "model": "Class 1 logging sound level meter", "bands": True,
     "pre": 93.8, "post": 93.9},
    {"id": "M4", "serial": "SLM-19651", "model": "Class 1 logging sound level meter", "bands": False,
     "pre": 93.5, "post": 93.3},
    {"id": "M5", "serial": "SLM-19744", "model": "Class 1 logging sound level meter", "bands": False,
     "pre": 94.0, "post": 94.1},
]
CAL_REF = 94.0          # the calibrator's reference level, dB
CAL_THRESHOLD = 0.3     # plan 4.1: adjust where the checks differ from the reference by more than this

# The fourteen monitoring positions. S is the designed specific sound level of the plant at the position,
# R the designed residual, v the residual's energetic mean over its own tenth percentile, m its mean over
# the quietest quarter hour, ev the passby rate an hour, strm the share of the residual that is steady.
POSITIONS = [
    # code    dwelling  description                         dist bear S      R      v     m     ev   strm
    ("NSL01", "DW-114", "bungalow, Glasha Lane",             300, 118, 43.91, 33.37, 6.26, 11.03, 1.1, 0.42),
    ("NSL02", "DW-103", "farmhouse, Drumlorne Upper",        165, 206, 47.24, 34.72, 2.09, 5.41, 0.5, 0.78),
    ("NSL03", "DW-121", "dormer, Clonaraght road",           385,  64, 43.47, 39.54, 6.61, 10.33, 4.2, 0.30),
    ("NSL04", "DW-101", "cottage, plant boundary field",      98, 231, 53.12, 39.59, 7.19, 8.25, 3.6, 0.34),
    ("NSL05", "DW-130", "two storey, Rathlone crossroads",   470,  22, 39.56, 33.45, 6.99, 7.90, 1.4, 0.44),
    ("NSL06", "DW-107", "bungalow, Clonaraght road junction", 215,  77, 45.22, 42.09, 7.43, 8.30, 5.1, 0.26),
    ("NSL07", "DW-110", "farmhouse, Coolnagree",             240, 177, 47.87, 36.86, 2.27, 3.42, 0.6, 0.74),
    ("NSL08", "DW-126", "bungalow, Glasha bridge",           420, 141, 41.74, 36.10, 3.69, 7.79, 1.0, 0.62),
    ("NSL09", "DW-112", "cottage, Drumlorne Lower",          275, 254, 44.62, 33.47, 1.95, 6.69, 0.4, 0.80),
    ("NSL10", "DW-134", "farmhouse, Shanvally",              505, 299, 37.49, 33.76, 6.77, 9.83, 1.3, 0.45),
    ("NSL11", "DW-104", "dormer, plant access road",         150,  95, 49.93, 38.31, 6.48, 10.70, 3.1, 0.36),
    ("NSL12", "DW-118", "bungalow, Clonaraght road",         330,  58, 43.55, 37.68, 7.17, 11.28, 3.8, 0.32),
    ("NSL13", "DW-105", "cottage, Drumlorne Upper",          190, 219, 46.02, 32.54, 7.67, 10.44, 0.9, 0.46),
    ("NSL14", "DW-128", "two storey, Coolnagree road",       445, 163, 42.02, 32.76, 4.50, 5.06, 0.8, 0.58),
]
SCREEN = {
    "NSL01": "mature hedgerow between position and plant",
    "NSL02": "open field, no screening",
    "NSL03": "roadside, no screening",
    "NSL04": "open field, no screening",
    "NSL05": "farm buildings between position and plant",
    "NSL06": "roadside, no screening",
    "NSL07": "open field, no screening",
    "NSL08": "trees and river bank",
    "NSL09": "slurry store and shed between position and plant",
    "NSL10": "rising ground and trees",
    "NSL11": "open, facing the access road",
    "NSL12": "roadside hedge",
    "NSL13": "open field, no screening",
    "NSL14": "mature trees along the road",
}
# Complaints: rung 0's material, recorded in the register and in the complaints file.
COMPLAINTS = {"NSL06": 5, "NSL03": 4, "NSL12": 4, "NSL09": 3, "NSL01": 3, "NSL04": 2, "NSL11": 2,
              "NSL08": 1, "NSL02": 0, "NSL05": 0, "NSL07": 0, "NSL10": 0, "NSL13": 0, "NSL14": 0}

# Each position's two deployments: (week index, meter id). The four positions with no band data are on the
# unlicensed meters in both of their weeks.
SCHEDULE = {
    "NSL01": [(0, "M1"), (3, "M3")],
    "NSL02": [(0, "M2"), (3, "M1")],
    "NSL03": [(0, "M3"), (4, "M2")],
    "NSL04": [(0, "M4"), (3, "M2")],
    "NSL05": [(0, "M5"), (3, "M4")],
    "NSL06": [(1, "M1"), (4, "M3")],
    "NSL07": [(1, "M2"), (4, "M1")],
    "NSL08": [(1, "M4"), (4, "M5")],
    "NSL09": [(1, "M3"), (5, "M2")],
    "NSL10": [(1, "M5"), (5, "M4")],
    "NSL11": [(2, "M1"), (5, "M3")],
    "NSL12": [(2, "M2"), (5, "M1")],
    "NSL13": [(2, "M3"), (4, "M4")],
    "NSL14": [(2, "M5"), (3, "M5")],
}
# Mounting height, metres above ground, per deployment index.
MOUNT = {0: 1.5, 1: 1.5}
# The repeated download: this deployment's card was re-read and part of a day came through twice.
DUP_DEPLOYMENT = ("NSL09", 1)
DUP_DAY = dt.date(2026, 9, 10)
DUP_FROM, DUP_TO = 14, 16          # local hours duplicated

# The met mast. Wind is logged in metres a second until the anemometer swap, kilometres an hour after it.
MAST_SWAP = dt.date(2026, 9, 20)
RAIN_TIP_MM = 0.2

SEED = 182182

CODES = [p[0] for p in POSITIONS]
BY_CODE = {p[0]: p for p in POSITIONS}


# Residual texture per position, set from the designed spread of each position's own surroundings:
# EVENT_DB is a passby's energy above the steady part, JITTER the minute-to-minute swing of the steady
# part, SLOW the slow weather and stream swing across a week. Fixed by the search in scratch.
EVENT_DB = {c: (10.0, 22.0) for c in CODES}
JITTER = {c: 0.8 for c in CODES}
SLOW = {
    "NSL01": 2.2, "NSL02": 1.6, "NSL03": 1.6, "NSL04": 0.7, "NSL05": 0.6, "NSL06": 0.6,
    "NSL07": 0.8, "NSL08": 2.1, "NSL09": 2.2, "NSL10": 1.5, "NSL11": 2.2, "NSL12": 2.2,
    "NSL13": 1.5, "NSL14": 0.4,
}
