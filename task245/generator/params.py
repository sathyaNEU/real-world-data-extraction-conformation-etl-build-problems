"""task245 constants: Thornmouth's air quality network in 2027 (seven council stations and five stations the bulk terminal's
operator runs under its permit), the coast's weather, the terminal's dust plume, the analysers' faults and outages, the
council stations' NO2 and the terminal stations' deposition gauges. Everything the simulator draws from is here; nothing
below is read by the solver."""
import datetime as dt
import math

SEED = 245
YEAR = 2027
START = dt.datetime(2027, 1, 1, 0, 0)        # the first hour (ending 01:00 GMT)
DAYS = 365
HOURS = DAYS * 24
AS_OF = dt.date(2028, 3, 17)                 # the request (the audit closes on the 2027 data year)

# code, name, operator, site type, easting and northing (m from the stockyard centre on the network plan's site grid),
# background multiplier, traffic increment level, analyser, faults under heavy loading (1/0), long outage (days, or 0),
# true count target (days above 50), NO2 measured (1/0), role in the ladder
#   F: faults on the terminal's plume hours, noted only once the lost days are rebuilt from the wind
#   E: exceeds as measured; Q: a long outage in a quiet spell; C: clear under every reading
STATIONS = [
    # code    name                  op     type                 x      y      bm    tr   analyser          fault gap  tgt no2 role
    ("TBT1", "North Gate",          "TBT", "industrial",     0,   900,  1.00,  3, "TEOM 1405",        1,    0,  54, 0, "F"),
    ("TBT2", "East Berth",          "TBT", "industrial",   900,     0,  1.00,  3, "TEOM 1405",        1,    0,  22, 0, "C"),
    ("TH3",  "Harbour Walk",        "TBC", "urban industrial",  -950,     0,  1.00,  4, "TEOM 1405-F",      1,    0,  51, 1, "F"),
    ("TBT4", "South Yard",          "TBT", "industrial",     0,  -900,  1.00,  2, "TEOM 1405",        1,    0,  52, 0, "F"),
    ("TBT3", "Rail Sidings",        "TBT", "industrial",  2100,  2100,  1.00,  3, "Fidas 200",        0,    0,  16, 0, "C"),
    ("TBT5", "West Gate",           "TBT", "industrial", -2121,  2121,  1.00,  2, "TEOM 1405",        1,    0,  14, 0, "C"),
    ("TH5",  "Market Street",       "TBC", "roadside", -2200, -2200,  1.05, 14, "BAM 1020",         0,  128,  30, 1, "Q"),
    ("TH6",  "Westholme Avenue",    "TBC", "roadside", -1700, -2600,  1.00, 12, "BAM 1020",         0,  124,  31, 1, "Q"),
    ("TH1",  "Town Hall",           "TBC", "urban background", -2600, -2900,  1.00,  8, "BAM 1020",         0,    0,  24, 1, "C"),
    ("TH2",  "Grangefield",         "TBC", "suburban", -3500, -3500,  0.95,  5, "BAM 1020",         0,    0,  15, 1, "C"),
    ("TH4",  "Ellerby Road",        "TBC", "roadside", -5000, -3000,  0.95,  9, "BAM 1020",         0,    0,  11, 1, "C"),
    ("TH7",  "Rookwood Farm",       "TBC", "rural background", -9000, -6000,  0.85,  0, "BAM 1020",         0,    0,   2, 0, "C"),
]
STOCKYARD_OS = (441630, 539270)     # the stockyard centre, Ordnance Survey national grid (m); the register places each
                                     # station at its offset above plus a few tens of metres of surveyed scatter
CODES = [s[0] for s in STATIONS]
NAME = {s[0]: s[1] for s in STATIONS}
OPERATOR = {s[0]: s[2] for s in STATIONS}
ROLE = {s[0]: s[13] for s in STATIONS}

# synoptic wind regimes on this coast: direction the wind blows from, share of regime starts
REGIMES = [(225, .30), (270, .20), (180, .12), (315, .10), (0, .08), (45, .08), (90, .07), (135, .05)]
SPRING_EAST = (59, 151, 1.6)         # March to May: the easterly regimes (45 and 90 degrees) three times as likely
REGIME_STOP = 0.85                   # a regime lasts geometric(REGIME_STOP) days (mostly one day)
HOURLY_SD = 15.0                     # the hour-to-hour scatter of the wind direction about the day's (degrees)
HOURLY_AR = 0.9                      # its persistence from one hour to the next (AR(1) coefficient)
VEER_HOURS = 2                       # a change of regime veers the wind over this many hours either side of midnight
PLUME_KAPPA = 5.0                    # the plume's angular concentration about the bearing to the terminal
PLUME_AMP = 60.0
ACT_DISCHARGE = 1.15                 # the stockyard's activity while a ship discharges, against
ACT_IDLE = 0.85                     # its activity between calls
LIFT = 0.8                           # the plume's rise with wind speed (1 + LIFT at strong winds)
WET_FACTOR = 0.85                    # the stockyard's dust on a wet day, against a dry one

BG_SEASON = 0.30                     # the regional background's seasonal swing (log), highest in April
BG_SD = 0.18                         # its day-to-day variation (log, AR(1) innovations)
AIRMASS = 0.0                        # log background, easterly continental air against westerly Atlantic air
# regional background episodes (start day, length, extra micrograms per cubic metre at the peak)
EPISODES = [(70, 4, 32), (95, 3, 28), (120, 5, 38), (200, 3, 22), (333, 3, 28)]

# overload faults: a heavy plume arriving (the hour the loading jumps past FAULT_T1) on a filter already holding more than
# FAULT_LOAD (the sum of hourly concentrations since the last exchange) trips the analyser with probability FAULT_Q times
# the station's own multiplier; it stays down until the technician's next round at 10:00, where the filter is exchanged
FAULT_T1 = 60.0
FAULT_LOAD = 1500.0
FAULT_Q = 0.85
ROUND_TBT = (0, 3)                   # the operator's technician's rounds: Mondays and Thursdays at 10:00
ROUND_TBC = (1, 4)                   # the council's: Tuesdays and Fridays at 10:00
FAULT_PRE = "day"                    # ratification rejects the readings earlier on the day of a fault (unstable mass readings)
STABILISE = "day"                    # after a restart, ratification rejects the rest of that day (the mass baseline settling)

# tuned (generator/tune.py): each faulting analyser's fault multiplier and draw, and where each long outage falls
FAULT_MULT = {'TBT1': 0.85, 'TBT2': 1.0, 'TH3': 1.0, 'TBT4': 1.0, 'TBT5': 1.0}
FAULT_SEED = {'TBT1': 2, 'TBT2': 0, 'TH3': 1, 'TBT4': 2, 'TBT5': 0}
GAP_START = {'TH5': (155, 128), 'TH6': (197, 124)}

# NO2 at the council stations (micrograms per cubic metre at 20 C): background multiplier, traffic level, ship NOx near the berths
NO2 = {"TH1": (1.00, 9, 0), "TH2": (0.85, 6, 0), "TH3": (1.002, 7, 6), "TH4": (0.954, 16, 0), "TH5": (1.054, 21, 0),
       "TH6": (1.004, 18, 0)}
NO2_PER_PPB = 1.91                   # 20 C and 101.3 kPa, as the council reports
NO2_LOGGER_FACTOR = 1.88             # the new loggers' default (25 C), applied to NO2 and NOx from each logger's fitting
# the telemetry upgrade: each council NO2 station's new logger, fitted on the council technician's June rounds (GMT)
NO2_LOGGER_FIT = {"TH1": dt.datetime(2027, 6, 8, 10, 0), "TH2": dt.datetime(2027, 6, 8, 13, 0),
                  "TH3": dt.datetime(2027, 6, 11, 10, 0), "TH4": dt.datetime(2027, 6, 11, 13, 0),
                  "TH5": dt.datetime(2027, 6, 1, 10, 0), "TH6": dt.datetime(2027, 6, 15, 13, 0)}
NO2_RESENT = {"TH2": (816, 168), "TH5": (8088, 168)}  # a week of hours imported twice from the analyser's store

# deposit gauges at the operator's stations: BS 1747 funnel gauges to the June 2027 exchange, Frisbee gauges from it
GAUGE_AREA_OLD = math.pi * 0.1525 ** 2  # m2, 305 mm funnel
GAUGE_AREA_NEW = math.pi * 0.1135 ** 2  # m2, 227 mm Frisbee
GAUGE_SWITCH = dt.date(2027, 6, 7)        # the first Monday of June
DEPOSIT_BG = 32.0                    # mg/m2/day away from the stockyard
DEPOSIT_PER_UG = 3.2                 # mg/m2/day of deposit per ug/m3 of the stockyard's PM10 at the gauge
DEPOSIT_K = {"TBT1": 1.005, "TBT2": 1.0, "TBT3": 1.0, "TBT4": 1.0, "TBT5": 1.0}
GAUGE_VOID = ("TBT2", 7)             # the period starting in July: contaminated
