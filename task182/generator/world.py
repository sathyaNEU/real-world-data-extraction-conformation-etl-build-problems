"""Drumlorne: the site, the dwellings, the meters, the survey weeks and the designed levels.

Nothing in this module ships. The designed specific levels and residuals fix the world; every figure the
pack and the goldens carry is measured from the built data (dataset-generation 6.1).
"""
import datetime as dt
import math

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

# The Monday morning round. One technician works through the five meters: at each position the meter
# standing there is checked against the calibrator, stopped and lifted, and the next one is set running
# and checked. The round starts at a different time each week and the order rotates, so no two meters go
# in or come out at the same instant and no record is exactly a week long. Every visit is before 07:00,
# so the set-up and pick-up minutes fall outside the assessment period. The seventh round is the
# collection Monday, 12 October, after the survey's last week.
ROUND_MONDAYS = WEEKS + [dt.date(2026, 10, 12)]
ROUND_START = [(4, 48), (5, 2), (4, 41), (4, 57), (4, 36), (5, 6), (4, 52)]
ROUND_GAP = [[0, 26, 49, 74, 97], [0, 22, 47, 71, 94], [0, 28, 52, 79, 101],
             [0, 23, 45, 70, 92], [0, 27, 50, 73, 99], [0, 21, 46, 72, 95],
             [0, 25, 48, 76, 98]]
ROUND_ORDER = [["M1", "M4", "M2", "M5", "M3"], ["M3", "M1", "M5", "M2", "M4"],
               ["M2", "M5", "M1", "M3", "M4"], ["M4", "M2", "M3", "M1", "M5"],
               ["M5", "M3", "M4", "M2", "M1"], ["M1", "M2", "M5", "M4", "M3"],
               ["M3", "M4", "M1", "M5", "M2"]]
# Minutes between stopping a meter at one position and starting it at the next: the drive and the walk in.
TURNAROUND = 20
# What the meter logs while the technician is at it: the minutes the tripod and windshield are handled,
# and the minute the calibrator sits on the microphone for the field check.
SETUP_HANDLING = 2        # minutes of handling as the meter is set up, before the field check
SETUP_AFTER = 1           # minutes of handling between the field check and the technician leaving
PICKUP_HANDLING = 2       # minutes of handling after the closing field check
HANDLING_DB = (61.5, 77.0)


def visit(meter, week):
    """When the technician got to the meter on the Monday of that round, local time."""
    d = ROUND_MONDAYS[week]
    h, m = ROUND_START[week]
    return (dt.datetime(d.year, d.month, d.day, h, m)
            + dt.timedelta(minutes=ROUND_GAP[week][ROUND_ORDER[week].index(meter)]))

# The plant's weekly planned process stop (local), and the unplanned stops, as the event log records them.
# The weekly inspection takes as long as it takes; every one of them is over before the assessment period
# opens at 07:00.
PLANNED_STOPS = [
    (dt.datetime(2026, 9, 1, 4, 45), 120, "weekly MCC inspection and belt check"),
    (dt.datetime(2026, 9, 8, 5, 0), 120, "weekly MCC inspection and belt check"),
    (dt.datetime(2026, 9, 15, 4, 30), 120, "weekly MCC inspection, blower strainer clean and hour "
                                           "counter change on CHP-01"),
    (dt.datetime(2026, 9, 22, 4, 50), 120, "weekly MCC inspection and belt check"),
    (dt.datetime(2026, 9, 29, 4, 40), 120, "weekly MCC inspection, centrifuge scroll check"),
    (dt.datetime(2026, 10, 6, 5, 0), 120, "weekly MCC inspection and belt check"),
]

# The gas engine comes off load on its own from time to time: a gas quality trip, an oil change, a
# service. The blowers and the centrifuges carry on through these, so the plant is never down.
ENGINE_STOPS = [
    (dt.datetime(2026, 9, 3, 13, 20), 95, "CHP-01 tripped on gas quality, flare in service"),
    (dt.datetime(2026, 9, 11, 9, 5), 225, "CHP-01 oil and filter change"),
    (dt.datetime(2026, 9, 23, 20, 40), 140, "CHP-01 tripped on gas quality, flare in service"),
    (dt.datetime(2026, 10, 2, 8, 15), 310, "CHP-01 500 hour service"),
    (dt.datetime(2026, 10, 9, 14, 50), 70, "CHP-01 tripped on jacket water temperature"),
]

# What each source contributes to the plant's sound at a position, as a share of the running plant.
SOURCE_SHARE = {"blowers": 0.55, "engine": 0.20, "centrifuges": 0.25}
UNPLANNED_STOPS = [
    # the only unplanned stop the log holds falls before the survey's first deployment
    (dt.datetime(2026, 8, 26, 2, 10), 22, "ESB supply dip, all drives tripped"),
]

# Equipment the three noise sources run on.
BLOWERS = ["BL-01", "BL-02", "BL-03"]
CENTRIFUGES = ["CF-01", "CF-02"]
ENGINE = "CHP-01"

# Days a centrifuge did not run: the scroll check at the weekly inspection, and the day the second
# machine was down for a bearing.
CF_DOWN = {
    dt.date(2026, 9, 16): ["CF-01", "CF-02"],     # scroll change, no dewatering that day
    dt.date(2026, 9, 29): ["CF-02"],
    dt.date(2026, 10, 1): ["CF-01", "CF-02"],     # liquor tank full, dewatering held over
}
# Runs the shift split in two to draw the liquor tank down, with the minutes into the run it stopped.
CF_SPLIT = {
    ("CF-01", dt.date(2026, 9, 2)): 212,
    ("CF-02", dt.date(2026, 9, 8)): 174,
    ("CF-02", dt.date(2026, 9, 10)): 265,
    ("CF-01", dt.date(2026, 9, 23)): 198,
    ("CF-02", dt.date(2026, 10, 1)): 243,
    ("CF-01", dt.date(2026, 10, 8)): 227,
    ("CF-02", dt.date(2026, 10, 9)): 189,
}

# The five meters. The one-third-octave module is licensed on the first three only.
METERS = [
    {"id": "M1", "serial": "SLM-21884", "model": "Class 1 logging sound level meter", "bands": True,
     "cert": "2026-02-19", "due": "2027-02-18", "found": 94.1, "left": 94.0},
    {"id": "M2", "serial": "SLM-21907", "model": "Class 1 logging sound level meter", "bands": True,
     "cert": "2026-03-12", "due": "2027-03-11", "found": 94.5, "left": 94.1},
    {"id": "M3", "serial": "SLM-22043", "model": "Class 1 logging sound level meter", "bands": True,
     "cert": "2025-11-27", "due": "2026-11-26", "found": 93.8, "left": 94.0},
    {"id": "M4", "serial": "SLM-19651", "model": "Class 1 logging sound level meter", "bands": False,
     "cert": "2026-01-23", "due": "2027-01-22", "found": 93.2, "left": 93.9},
    {"id": "M5", "serial": "SLM-19744", "model": "Class 1 logging sound level meter", "bands": False,
     "cert": "2026-04-08", "due": "2027-04-07", "found": 94.0, "left": 94.0},
]
CAL_REF = 94.0          # the calibrator's reference level, dB
CAL_THRESHOLD = 0.3     # plan 4.1: adjust where the checks differ from the reference by more than this

# The field check either side of each deployment, as the technician wrote them on the sheet: the mean of
# the pair is the deployment's deviation from the calibrator. Two meters sit outside the plan's 0.3 dB
# window all survey (M2 reads high, M4 low); the other three stay inside it and are not corrected. No
# pair's mean lands on the window's edge and no pair spreads more than 0.8 dB, so no deployment is
# dropped under 4.1's second sentence. Means on a tenth: both checks move in the same tenth.
CAL_MEAN = {
    "M1": [94.1, 93.9, 94.0, 94.2, 93.9, 94.1],
    "M2": [94.4, 94.6, 94.5, 94.4, 94.6, 94.5],
    "M3": [93.9, 94.1, 93.8, 94.0, 94.2, 93.9],
    "M4": [93.3, 93.2, 93.4, 93.2, 93.3],
    "M5": [94.0, 94.2, 93.9, 94.1, 94.0],
}
CAL_SPREAD = {
    "M1": [0.2, 0.4, 0.2, 0.0, 0.6, 0.2],
    "M2": [0.8, 0.4, 0.6, 0.2, 0.4, 0.8],
    "M3": [0.2, 0.6, 0.4, 0.2, 0.4, 0.0],
    "M4": [0.6, 0.2, 0.4, 0.8, 0.2],
    "M5": [0.0, 0.4, 0.2, 0.6, 0.2],
}

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
    ("NSL06", "DW-107", "bungalow, Clonaraght road junction", 215,  77, 45.22, 42.70, 7.43, 8.30, 5.1, 0.26),
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
    "NSL06": "road embankment between position and plant",
    "NSL07": "open field, no screening",
    "NSL08": "trees and river bank",
    "NSL09": "open ground, no screening",
    "NSL10": "rising ground and trees",
    "NSL11": "open, facing the access road",
    "NSL12": "roadside hedge",
    "NSL13": "farm buildings between position and plant",
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
# Mounting height the schedule sets for each position, metres above ground, inside the 1.2 to 1.5 m the
# free-field standard allows. The lower positions are the ones where the tripod had to stand clear of a
# roadside hedge or a garden wall.
HEIGHT = {
    "NSL01": 1.5, "NSL02": 1.5, "NSL03": 1.2, "NSL04": 1.5, "NSL05": 1.5, "NSL06": 1.3,
    "NSL07": 1.5, "NSL08": 1.2, "NSL09": 1.5, "NSL10": 1.5, "NSL11": 1.5, "NSL12": 1.2,
    "NSL13": 1.5, "NSL14": 1.4,
}
# The two deployments where the height on the sheet is not the scheduled one, with the sheet's reason.
HEIGHT_DEPART = {("NSL08", 0): 1.5, ("NSL13", 1): 1.2}

# Who deployed and collected each meter: the technician on most, the engineer and the operations
# manager where the week was covered.
CREW = ["technician", "technician", "engineer", "technician", "operations", "technician",
        "technician", "engineer", "technician", "technician", "technician", "operations",
        "engineer", "technician", "technician", "technician", "operations", "technician",
        "technician", "engineer", "technician", "technician", "technician", "operations",
        "technician", "engineer", "technician", "technician"]

# Spells where a meter wrote no measurement: the logger reset or the measurement channel dropped out, and
# the download carries the instrument's no-data value in every level column for those minutes. None falls
# inside a process stop.
NODATA_VALUE = -120.2
NODATA = [
    (("NSL12", 1), dt.datetime(2026, 10, 8, 13, 12), 95, "logger reset, channel down until the mid-week visit"),
    (("NSL05", 0), dt.datetime(2026, 9, 4, 9, 5), 38, "measurement channel dropout"),
    (("NSL09", 1), dt.datetime(2026, 10, 7, 15, 41), 17, "measurement channel dropout"),
]
# The repeated download: this deployment's card was re-read and part of a day came through twice.
DUP_DEPLOYMENT = ("NSL09", 0)
DUP_DAY = dt.date(2026, 9, 10)
DUP_FROM, DUP_TO = 14, 16          # local hours duplicated

# Spells with no rows at all in the historian: the radio link to the PLC has dropped through the whole
# survey, most of them short, one of them most of a day. The counters carry through every one of them.
# None of them covers a 07:00 or a 19:00 stamp on a weekday or a Monday 00:00, so every window a figure
# is read over has a row at both of its ends.
PLC_GAPS = [
    (dt.datetime(2026, 9, 2, 10, 15), 11),
    (dt.datetime(2026, 9, 10, 14, 30), 7),
    (dt.datetime(2026, 9, 16, 11, 15), 5),
    (dt.datetime(2026, 9, 25, 19, 15), 80),
    (dt.datetime(2026, 9, 29, 9, 30), 9),
    (dt.datetime(2026, 10, 7, 8, 0), 13),
]
# And the spells where the link dropped but the historian kept writing: the interface holds the last
# value it had and writes it again every scan, so the rows are there and the plant's state is not. Two a
# week, one inside the working day and one outside it. None covers a 07:00, a 19:00 or a Monday 00:00
# stamp, and none touches a spell with no rows at all.
PLC_HELD = [
    # the daytime ones sit against the week's own dropout, because the link comes back holding the value
    # it had before it went: the run of quarter hours the record does not cover is longer than the run of
    # rows it is missing
    (dt.datetime(2026, 9, 2, 13, 0), 3),
    (dt.datetime(2026, 9, 5, 2, 45), 6),
    (dt.datetime(2026, 9, 10, 16, 15), 4),
    (dt.datetime(2026, 9, 13, 21, 15), 5),
    (dt.datetime(2026, 9, 16, 12, 30), 3),
    (dt.datetime(2026, 9, 19, 4, 0), 4),
    (dt.datetime(2026, 9, 23, 9, 15), 6),
    (dt.datetime(2026, 9, 26, 15, 15), 6),
    (dt.datetime(2026, 9, 29, 11, 45), 4),
    (dt.datetime(2026, 10, 3, 5, 30), 5),
    (dt.datetime(2026, 10, 7, 11, 15), 3),
    (dt.datetime(2026, 10, 11, 20, 45), 5),
]

# The third blower was added when the plant was upgraded and tied into the aeration main downstream of
# the header's flow meter, so it carries its own meter. BL-03 is a fixed-speed machine: it holds the
# output its drive is set to and the header's two machines take the dissolved oxygen trim, so what BL-03
# delivers is no fraction of what the header reads and the ratio of the two moves with the load all day.
# The shift reset BL-03's drive three times over the survey, in normal cubic metres an hour.
BL03_SETTING = [(dt.date(2026, 8, 1), 1320.0), (dt.date(2026, 9, 8), 1395.0),
                (dt.date(2026, 9, 24), 1275.0), (dt.date(2026, 10, 6), 1350.0)]

# Spells where the header's own two machines were isolated and BL-03 carried the lanes on its own: the
# shift takes BL-01 and BL-02 off to clean a strainer or to calibrate the dissolved oxygen probes, before
# the day's assessment period opens and never on the morning of the weekly inspection. The plant is not
# down in them, so they are no part of any residual window, and they are what the header's own meter
# gives itself away in.
BL12_STOPS = [
    (dt.datetime(2026, 9, 10, 5, 0), 45, "BL-01 and BL-02 isolated, DO probe calibration"),
    (dt.datetime(2026, 9, 30, 5, 15), 45, "BL-01 and BL-02 isolated, header strainer clean"),
    (dt.datetime(2026, 10, 8, 4, 45), 60, "BL-01 and BL-02 isolated, DO probe calibration"),
]

# The gas booster on the digester's gas skid runs with the plant and takes a drain and purge cycle once a
# day, and it keeps pushing gas to the flare through the engine's own stops. It makes no measurable sound
# at any monitoring position. Minutes of the purge and the hour of the day it starts, by day of the week.
BOOSTER_PURGE_MIN = 20
BOOSTER_PURGE_AT = [(9, 40), (14, 10), (11, 25), (16, 5), (10, 50), (13, 35), (8, 55)]

# The engine's hour counter was changed during a weekly inspection, with the engine down, so no running
# hour falls either side of the change.
HOUR_COUNTER_SWAP = dt.datetime(2026, 9, 15, 6, 0)

# The met mast. Wind is logged in metres a second until the anemometer swap, kilometres an hour after it.
MAST_SWAP = dt.date(2026, 9, 20)
RAIN_TIP_MM = 0.2

SEED = 182182
# The blower trim's own draw. Chosen by the scan in scratch so that every week's delivered air sits clear
# of the whole-unit rounding edge the note reports it at.
AIR_SEED = 21
# How much of the surroundings' own evening and night texture the record carries. Set by the scan in
# scratch: enough that no position's record is the same shape every day, little enough that the night is
# the plant's own sound and not the road's.
NIGHT_TEX = 0.2

CODES = [p[0] for p in POSITIONS]
BY_CODE = {p[0]: p for p in POSITIONS}


# Residual texture per position, set from the designed spread of each position's own surroundings:
# EVENT_DB is a passby's energy above the steady part, JITTER the minute-to-minute swing of the steady
# part, SLOW the slow weather and stream swing across a week. Fixed by the search in scratch.
EVENT_DB = {c: (10.0, 22.0) for c in CODES}
JITTER = {c: 0.8 for c in CODES}
SLOW = {
    "NSL01": 2.2, "NSL02": 0.7, "NSL03": 1.6, "NSL04": 0.7, "NSL05": 0.6, "NSL06": 0.6,
    "NSL07": 1.7, "NSL08": 2.1, "NSL09": 2.2, "NSL10": 1.5, "NSL11": 2.2, "NSL12": 2.2,
    "NSL13": 1.5, "NSL14": 0.4,
}

# How deep the plant's own level falls inside a minute at each position, as a multiple of the base swing:
# what arrives through a screen, a hedge or moving traffic is modulated more than what arrives across an
# open field, and that depth is what sets how far the record's LA90 sits below its LAeq. Fixed by the scan
# in scratch; it moves the minute LA90 column and no level.
F90 = {c: 1.0 for c in CODES}

# Micro-adjustments to the designed specific levels, so no two positions print the same level and no
# printed level sits on a rounding edge or on the printed value itself. Fixed by the per-position scan in
# scratch; they move no slate.
SHIFT = {
    "NSL01": -0.08051,
    "NSL02": -0.14792,
    "NSL03": -0.28131,
    "NSL04": -0.09112,
    "NSL05": +0.36613,
    "NSL06": -0.92500,
    "NSL07": -0.02562,
    "NSL08": -0.69449,
    "NSL09": -0.19550,
    "NSL10": -0.74610,
    "NSL11": -0.07719,
    "NSL12": -0.29204,
    "NSL13": +0.05014,
    "NSL14": +0.11207,
}


# How much of each tone survives to a position: the blower's 400 Hz blade tone falls away faster with
# distance than the engine's 100 Hz firing tone, and screening takes far more of the higher tone than of
# the lower one, which is how a barrier works. Ordinary air absorption and barrier attenuation.
BARRIER = {}
for _p in POSITIONS:
    _s = SCREEN[_p[0]]
    BARRIER[_p[0]] = (0.55 if ("buildings" in _s or "embankment" in _s or "shed" in _s)
                      else (0.72 if ("hedge" in _s or "trees" in _s or "hedgerow" in _s or "ground and" in _s)
                            else 1.0))
TONE_K = {}
for _p in POSITIONS:
    _d, _b = _p[3], BARRIER[_p[0]]
    TONE_K[_p[0]] = (round(_b ** 3.0 * math.exp(-(_d - 98) / 420.0), 4),
                     round(_b ** 0.8 * math.exp(-(_d - 98) / 1200.0), 4))
