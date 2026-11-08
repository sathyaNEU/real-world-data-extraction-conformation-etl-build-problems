"""task118 architecture 6: Ravelstoke Rail's 2027 platform dispatch team. Every time is a whole number of
half-minutes after midnight (the running feed's resolution); 720 is 06:00."""
import datetime as dt

SEED = 118
DRAW = 3                    # day-stream offset chosen so every graded figure sits mid-bin
HM = 2                      # half-minutes per minute

# The record: every weekday from Monday 7 September to Friday 27 November 2026 (no bank holiday falls in it).
RECORD_START = dt.date(2026, 9, 7)
RECORD_END = dt.date(2026, 11, 27)
CENSUS_DAY = dt.date(2026, 10, 13)
CLOCK_CHANGE = dt.date(2026, 10, 25)        # BST to GMT, a Sunday
EXPORT_DATE = dt.date(2027, 1, 18)          # the pack's export date (after the Delay Repay pull)

TEAM_SHARE = 0.6                            # three fifths of each train's dwell overrun at the team's station
TEAM_FROM, TEAM_TO = 6 * 60 * HM + 30 * HM, 19 * 60 * HM + 30 * HM   # booked departure 06:30 <= t < 19:30
MIN_TURN = 4 * HM                           # minimum turnround at every terminus, planning rules

LINES = ["N", "E", "S"]
LINE_NAME = {"N": "Crossmoor line", "E": "Ambrey line", "S": "Holm Ferry line"}
STATIONS = {
    "N": ["Crossmoor", "Thornell", "Wensford Bridge", "Haverleigh", "Ostley Lane", "Garside", "Selbury Road",
          "Kestle Park", "Brathwick Road", "Mill Wharf", "Ravelstoke Central"],
    "E": ["Ravelstoke Airport", "Skyfield", "Fellbrook", "Hartlow", "Ambrey", "Ambrey Parkway", "Larchfield",
          "Ashtree", "Pellingham", "Tanner's Row", "Ravelstoke Central"],
    "S": ["Holm Ferry", "Ferry Lane", "Bracken Rise", "Wyndham Road", "Corrie Green", "Holcroft Green", "Marina",
          "Quayside", "Saltgate", "Exchange Street", "Ravelstoke Central"],
}
CRS = {"Crossmoor": "CXM", "Thornell": "THL", "Wensford Bridge": "WSB", "Haverleigh": "HVL", "Ostley Lane": "OSL",
       "Garside": "GSD", "Selbury Road": "SBR", "Kestle Park": "KSP", "Brathwick Road": "BWR", "Mill Wharf": "MLW",
       "Ravelstoke Central": "RVC", "Ravelstoke Airport": "RVA", "Skyfield": "SKF", "Fellbrook": "FLB",
       "Hartlow": "HTW", "Ambrey": "AMB", "Ambrey Parkway": "AMP", "Larchfield": "LCF", "Ashtree": "ASR",
       "Pellingham": "PLG", "Tanner's Row": "TNR", "Holm Ferry": "HMF", "Ferry Lane": "FYL", "Bracken Rise": "BKR",
       "Wyndham Road": "WYR", "Corrie Green": "CRG", "Holcroft Green": "HCG", "Marina": "MRN", "Quayside": "QYS",
       "Saltgate": "SLG", "Exchange Street": "EXS"}
TIPLOC = {"Crossmoor": "CROSMOR", "Thornell": "THORNEL", "Wensford Bridge": "WENSFDB", "Haverleigh": "HAVRLGH",
          "Ostley Lane": "OSTLYLN", "Garside": "GARSIDE", "Selbury Road": "SELBYRD", "Kestle Park": "KESTLPK",
          "Brathwick Road": "BRTHWKR", "Mill Wharf": "MILWHRF", "Ravelstoke Central": "RAVLCEN",
          "Ravelstoke Airport": "RAVLAPT", "Skyfield": "SKYFILD", "Fellbrook": "FELBROK", "Hartlow": "HARTLOW",
          "Ambrey": "AMBREY", "Ambrey Parkway": "AMBRYPW", "Larchfield": "LARCHFD", "Ashtree": "ASHTREE",
          "Pellingham": "PELNGHM", "Tanner's Row": "TANRSRW", "Holm Ferry": "HOLMFRY", "Ferry Lane": "FERYLN",
          "Bracken Rise": "BRAKNRS", "Wyndham Road": "WYNDMRD", "Corrie Green": "CORIEGN", "Holcroft Green": "HOLCFTG",
          "Marina": "MARINA", "Quayside": "QUAYSDE", "Saltgate": "SALTGAT", "Exchange Street": "EXCHGST"}

# Shortlist: key -> (line, station index).
SHORTLIST = {"Ostley Lane": ("N", 4), "Brathwick Road": ("N", 8), "Ambrey Parkway": ("E", 5),
             "Pellingham": ("E", 8), "Holcroft Green": ("S", 5), "Saltgate": ("S", 8)}
GOLDEN_PICK = "Pellingham"

# Sectional running times (half-minutes) for the ten sections of each line, outer end towards Central.
SRT = {"N": [7, 6, 6, 7, 6, 6, 7, 6, 5, 6], "E": [8, 6, 6, 7, 6, 7, 6, 6, 6, 5], "S": [6, 7, 6, 6, 7, 6, 5, 6, 6, 6]}
# Booked dwell (half-minutes) at each calling point: half a minute at the quiet stations, a minute at the busier ones,
# a minute and a half at the two busiest suburban stations (the termini have none).
DWELL_AT = {
    "Thornell": 1, "Wensford Bridge": 1, "Haverleigh": 1, "Ostley Lane": 2, "Garside": 1, "Selbury Road": 1,
    "Kestle Park": 1, "Brathwick Road": 3, "Mill Wharf": 1,
    "Skyfield": 2, "Fellbrook": 1, "Hartlow": 2, "Ambrey": 1, "Ambrey Parkway": 2, "Larchfield": 1, "Ashtree": 1,
    "Pellingham": 2, "Tanner's Row": 1,
    "Ferry Lane": 1, "Bracken Rise": 1, "Wyndham Road": 1, "Corrie Green": 1, "Holcroft Green": 2, "Marina": 2,
    "Quayside": 2, "Saltgate": 3, "Exchange Street": 1,
    "Crossmoor": 2, "Ravelstoke Central": 2, "Ravelstoke Airport": 2, "Holm Ferry": 2,
}
# Allowances in each direction: {section index (inbound numbering, 0 = outer end) : half-minutes}.
ALLOW_IN = {"N": {6: 1, 9: 3}, "E": {6: 1, 9: 1}, "S": {6: 1, 9: 3}}
ALLOW_OUT = {"N": {6: 1, 0: 3}, "E": {6: 1, 0: 2}, "S": {6: 1, 0: 3}}

UNITS_PER_LINE = 10
FIRST_DEP = 6 * 60 * HM
LAST_DEP = 22 * 60 * HM
CYCLE_SPACING = 24          # half-minutes between successive units' first departures (12 minutes)

# Layovers (half-minutes) by the arrival period, at Ravelstoke Central and at the outer end.
PERIODS = ["early", "am", "mid", "pm", "eve"]


def period_of(t):
    h = t / (60.0 * HM)
    if h < 7.0:
        return "early"
    if h < 9.5:
        return "am"
    if h < 16.5:
        return "mid"
    if h < 19.0:
        return "pm"
    return "eve"


LAY_CENTRAL = {"N": {"early": 24, "am": 20, "mid": 28, "pm": 20, "eve": 28},
               "E": {"early": 10, "am": 9, "mid": 28, "pm": 12, "eve": 28},
               "S": {"early": 24, "am": 20, "mid": 28, "pm": 20, "eve": 28}}
LAY_OUTER = {"N": {"early": 24, "am": 24, "mid": 24, "pm": 24, "eve": 24},
             "E": {"early": 16, "am": 16, "mid": 24, "pm": 20, "eve": 24},
             "S": {"early": 24, "am": 24, "mid": 24, "pm": 24, "eve": 24}}

# Ambrey line morning park-and-ride extras: Hartlow, Ambrey Parkway, Pellingham, Ravelstoke Central; units from
# Hartlow sidings, to Ravelstoke Central sidings on arrival; back out as evening extras to Hartlow.
EXTRA_STOPS = [3, 5, 8, 10]
EXTRA_FIRST = 7 * 60 * HM + 21
EXTRA_SPACING = 24
N_EXTRAS = 6
EXTRA_PM_FIRST = 16 * 60 * HM + 70

# Census loads: mean boarders per station by line, direction and period (before the station weights).
LOAD = {
    "N": {"in": {"early": 3, "am": 9, "mid": 3, "pm": 2, "eve": 1.5}, "out": {"early": 1.5, "am": 1.5, "mid": 3, "pm": 9, "eve": 2}},
    "E": {"in": {"early": 3, "am": 4, "mid": 3, "pm": 2, "eve": 1.5}, "out": {"early": 7, "am": 13, "mid": 3, "pm": 8, "eve": 2}},
    "S": {"in": {"early": 3, "am": 9, "mid": 3, "pm": 2, "eve": 1.5}, "out": {"early": 1.5, "am": 1.5, "mid": 3, "pm": 9, "eve": 2}},
}
EXTRA_ON = {3: 85, 5: 125, 8: 10}
LOAD_SCALE = 3.2


def _p(early=0.05, am=0.05, mid=0.05, pm=0.05, eve=0.05):
    return {"early": early, "am": am, "mid": mid, "pm": pm, "eve": eve}


Z = _p()
# Mean dwell overrun (minutes) at each shortlisted station by train kind, direction and period.
OVERRUN = {
    "Ostley Lane": {"all": {"in": _p(0.2, 0.5, 0.2, 0.2, 0.1), "out": Z}, "extra": {"in": Z, "out": Z}},
    "Brathwick Road": {"all": {"in": _p(0.3, 0.85, 0.6, 0.4, 0.2), "out": _p(0.1, 0.3, 0.3, 0.6, 0.2)},
                       "extra": {"in": Z, "out": Z}},
    "Ambrey Parkway": {"all": {"in": _p(0.1, 0.15, 0.2, 0.1, 0.05), "out": Z},
                       "extra": {"in": _p(0.05, 2.1, 0.05, 0.05, 0.05), "out": Z}},
    "Pellingham": {"all": {"in": _p(0.3, 1.35, 0.15, 0.1, 0.05), "out": Z},
                   "extra": {"in": _p(0.05, 0.3, 0.05, 0.05, 0.05), "out": Z}},
    "Holcroft Green": {"all": {"in": _p(0.2, 0.4, 0.3, 0.2, 0.1), "out": Z}, "extra": {"in": Z, "out": Z}},
    "Saltgate": {"all": {"in": _p(0.33, 1.1, 0.77, 0.55, 0.33), "out": _p(0.11, 0.33, 0.44, 0.66, 0.22)},
                 "extra": {"in": Z, "out": Z}},
}
BASE_OVERRUN = 0.05
P_INCIDENT = 0.02           # per train per section
INCIDENT_MEAN = 1.5         # minutes
P_ORIGIN = 0.25             # a unit's first working of the day (or a spare's), late off the depot or sidings
ORIGIN_MEAN = 1.2
# Disruptions: (date, line, inbound/outbound, booked origin departure from, section, minutes for successive trains)
DISRUPTIONS = [
    (dt.date(2026, 9, 22), "N", "in", 10 * 60 * HM + 20, 3, [38, 29, 21, 13, 6]),
    (dt.date(2026, 10, 7), "S", "out", 12 * 60 * HM + 40, 6, [44, 35, 26, 17, 9]),
    (dt.date(2026, 10, 28), "E", "in", 13 * 60 * HM + 10, 2, [33, 25, 18, 10]),
    (dt.date(2026, 11, 17), "S", "in", 11 * 60 * HM + 0, 4, [27, 20, 12, 5]),
    (dt.date(2026, 11, 5), "N", "in", 19 * 60 * HM + 40, 6, [131, 118, 104, 92, 77, 63, 48, 35, 22, 9]),
    (dt.date(2026, 9, 16), "E", "out", 19 * 60 * HM + 50, 5, [86, 74, 61, 49, 36, 24, 12]),
    (dt.date(2026, 10, 22), "S", "in", 20 * 60 * HM + 0, 3, [79, 66, 54, 41, 29, 16]),
]
SPARES = ["336137", "336138"]
UNIT_FAILURES = [(dt.date(2026, 9, 30), "N", 3, 13 * 60 * HM), (dt.date(2026, 10, 20), "E", 6, 12 * 60 * HM),
                 (dt.date(2026, 11, 11), "S", 8, 14 * 60 * HM)]

# Gatelines (ask A): the census week, 15-minute readings of each array's cumulative counters, logged in UTC.
GATE_DAYS = [dt.date(2026, 10, 12) + dt.timedelta(days=k) for k in range(5)]
GATED = {"Brathwick Road": ["BWR-A", "BWR-B"], "Ambrey Parkway": ["AMP-1"], "Pellingham": ["PLG-N", "PLG-S"],
         "Saltgate": ["SLG-MAIN", "SLG-MKT"]}
GATE_OTHER = {"Brathwick Road": 0.07, "Ambrey Parkway": 0.04, "Pellingham": 0.31, "Saltgate": 0.22}
GATE_PARTS = [("before 09:30", 0, 9 * 60 + 30), ("09:30 to 16:30", 9 * 60 + 30, 16 * 60 + 30),
              ("from 16:30", 16 * 60 + 30, 24 * 60)]
COUNTER_WRAP = 65536

# Delay Repay (ask B): Delay Repay 15 bands on the single fare (returns: half the return fare), seasons on the
# daily value; claims for journeys in the record, extracted after the 28-day claim window and appeals.
DR_BANDS = [("15 to 29", 15, 30, 0.25), ("30 to 59", 30, 60, 0.5), ("60 to 119", 60, 120, 1.0),
            ("120 or more", 120, 10 ** 6, 1.0)]
DR_TAKEUP = 0.21
ASK_BANDS = [("15 to 29", 15, 30), ("30 to 59", 30, 60), ("60 or more", 60, 10 ** 6)]
DR_EXTRACT = dt.date(2027, 1, 15)
