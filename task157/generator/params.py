"""task157 architecture 3: the world. The Grainford City Region Combined Authority's Lot 2 franchise, run by
Pellbridge Buses from Saltmeadow depot; the Thornsby Bridge closes from 11 January to 28 March 2027 and route 41
diverts over the Ring Road crossing. Every constant the generator, the analysis and the checks share lives here."""
from __future__ import annotations

from datetime import date, timedelta

SEED = 157_2027

# ------------------------------------------------------------------ calendar
TT_START = date(2026, 8, 31)          # the winter timetable and duty schedule take effect (a bank holiday, Sunday service)
TT_END = date(2027, 4, 3)             # both run unchanged to the next registered change date
AVL_FIRST = date(2026, 9, 1)          # the AVL extract: Tuesday 1 September to Sunday 6 December 2026
AVL_LAST = date(2026, 12, 6)
ETM_FIRST = date(2026, 10, 1)         # the ticket machine extract: October and November 2026
ETM_LAST = date(2026, 11, 30)
CLOCK_CHANGE = date(2026, 10, 25)     # BST ends 02:00 local, 01:00 UTC
AS_OF = date(2026, 12, 11)
NOTICE_DUE = date(2026, 12, 21)
CLOSE_FIRST = date(2027, 1, 11)
CLOSE_LAST = date(2027, 3, 28)
BANK_HOLIDAYS = {date(2026, 8, 31): "Summer bank holiday", date(2026, 12, 25): "Christmas Day",
                 date(2026, 12, 28): "Boxing Day (substitute)", date(2027, 1, 1): "New Year's Day",
                 date(2027, 3, 26): "Good Friday", date(2027, 3, 29): "Easter Monday"}
# Grainford Council school terms (the timetable's serviced organisation)
TERMS = [(date(2026, 9, 2), date(2026, 10, 23)), (date(2026, 11, 2), date(2026, 12, 18)),
         (date(2027, 1, 5), date(2027, 2, 12)), (date(2027, 2, 22), date(2027, 3, 25))]

# 2026 events: the bridge's principal inspection (overnight, footway and deck soffit only), the closure notice
INSPECTION = date(2026, 11, 2)
CLOSURE_ANNOUNCED = date(2026, 11, 20)


def days(a, b):
    d = a
    while d <= b:
        yield d
        d += timedelta(days=1)


def is_school_day(d):
    return d.weekday() < 5 and any(a <= d <= b for a, b in TERMS) and d not in BANK_HOLIDAYS


def day_type(d):
    """The timetable a date runs: MF, SA or SU (a bank holiday runs Sunday's)."""
    if d in BANK_HOLIDAYS or d.weekday() == 6:
        return "SU"
    if d.weekday() == 5:
        return "SA"
    return "MF"


def bst(d):
    """True when local time on date d is UTC+1 (the AVL day's service hours never touch 01:00 to 02:00)."""
    return date(2026, 3, 29) <= d < CLOCK_CHANGE


# ------------------------------------------------------------------ stops and timing points
# ATCO codes in the national stop register's form; the operator's own stop codes are used in the duty schedule.
# (atco, name, operator code). Stops on opposite sides of the road carry their own code.
STOPS = {
    # Merchant Row Interchange stands
    "MRI-B": ("2970A0011020", "Merchant Row Interchange (Stand B)", "MRB"),
    "MRI-C": ("2970A0011030", "Merchant Row Interchange (Stand C)", "MRC"),
    "MRI-D": ("2970A0011040", "Merchant Row Interchange (Stand D)", "MRD"),
    "MRI-F": ("2970A0011060", "Merchant Row Interchange (Stand F)", "MRF"),
    "MRI-K": ("2970A0011110", "Merchant Row Interchange (Stand K)", "MRK"),
    # Grainford Bus Station stands
    "GBS-3": ("2970A0020030", "Grainford Bus Station (Stand 3)", "GB3"),
    "GBS-5": ("2970A0020050", "Grainford Bus Station (Stand 5)", "GB5"),
    "GBS-7": ("2970A0020070", "Grainford Bus Station (Stand 7)", "GB7"),
    "GBS-9": ("2970A0020090", "Grainford Bus Station (Stand 9)", "GB9"),
}

# Each route: termini (A city end, B outer end), outbound timing points with run times (off-peak, peak) for each
# link in minutes, the stops between timing points (for the fare stages), headway bands per day type.
# Run times inbound mirror outbound with the per-route inbound adjustment.
ROUTES = {
    "41": dict(name="Merchant Row - Thornsby Bridge - Ravensholme",
               tps=[("MRI-D", "Merchant Row Interchange (Stand D)"), ("TNS", "Tenter Street"),
                    ("THR", "Thornsby Road"), ("TQY", "Thornsby Quay"), ("RVR", "Ravensholme Road"),
                    ("RBS", "Ravensholme Bus Station")],
               run_off=[5, 5, 6, 6, 5], run_pk=[6, 6, 6, 7, 6], inbound_extra=[2, 0, 0, 0, 0],
               km=[1.42, 1.61, 1.18, 2.06, 1.37], km_in=[1.42, 1.74, 1.18, 2.06, 1.29]),
    "27": dict(name="Merchant Row - Castle Mount - Skelbrough",
               tps=[("MRI-B", "Merchant Row Interchange (Stand B)"), ("CSM", "Castle Mount"),
                    ("SKR", "Skelbrough Road"), ("SKW", "Skelbrough, Wrayford Avenue")],
               run_off=[6, 7, 7], run_pk=[7, 8, 8], inbound_extra=[0, 0, 0],
               km=[2.21, 2.48, 2.37], km_in=[2.29, 2.48, 2.37]),
    "58": dict(name="Merchant Row - Garrow Lane - Westerlow General Hospital",
               tps=[("MRI-C", "Merchant Row Interchange (Stand C)"), ("CHS", "Cloth Hall Street"),
                    ("GRR", "Garrow Lane"), ("WGH", "Westerlow General Hospital")],
               run_off=[5, 6, 7], run_pk=[6, 7, 8], inbound_extra=[0, 0, 0],
               km=[1.73, 2.15, 2.52], km_in=[1.73, 2.21, 2.52]),
    "33": dict(name="Merchant Row - Holm Lane - Hesselcote",
               tps=[("MRI-K", "Merchant Row Interchange (Stand K)"), ("HLM", "Holm Lane"),
                    ("UPC", "Hesselcote Centre"), ("UMD", "Hesselcote, Morbeck Drive")],
               run_off=[7, 7, 6], run_pk=[8, 8, 7], inbound_extra=[0, 0, 0],
               km=[2.64, 2.39, 1.92], km_in=[2.64, 2.39, 1.98]),
    "22": dict(name="Merchant Row - Dyer Street - Harlbeck",
               tps=[("MRI-F", "Merchant Row Interchange (Stand F)"), ("DYR", "Dyer Street"),
                    ("HRR", "Harlbeck Road"), ("HLG", "Harlbeck, Langstrow Green")],
               run_off=[6, 8, 7], run_pk=[7, 9, 8], inbound_extra=[0, 0, 0],
               km=[1.98, 3.06, 2.44], km_in=[1.98, 3.06, 2.51]),
    "6": dict(name="Grainford Bus Station - Ring Road - Gatesmoor",
              tps=[("GBS-3", "Grainford Bus Station (Stand 3)"), ("RJ4", "Ring Road, Junction 4"),
                   ("SML", "Saltmeadow Lane"), ("GTC", "Gatesmoor Centre"), ("GCR", "Gatesmoor, Coldharrow Road")],
              run_off=[6, 5, 6, 5], run_pk=[7, 6, 7, 5], inbound_extra=[0, 0, 0, 0],
              km=[2.18, 1.84, 2.11, 1.62], km_in=[2.18, 1.84, 2.11, 1.70]),
    "12": dict(name="Grainford Bus Station - Ring Road - Hollinbrigg",
               tps=[("GBS-5", "Grainford Bus Station (Stand 5)"), ("RJ4", "Ring Road, Junction 4"),
                    ("RJ5", "Ring Road, Junction 5"), ("HLE", "Hollinbrigg"), ("HSS", "Hollinbrigg, Sheep Street")],
               run_off=[6, 5, 6, 5], run_pk=[7, 6, 7, 6], inbound_extra=[0, 0, 0, 0],
               km=[2.18, 1.95, 2.23, 1.58], km_in=[2.18, 1.95, 2.23, 1.66]),
    "14": dict(name="Grainford Bus Station - Marsh Lane - Oxenstall",
               tps=[("GBS-7", "Grainford Bus Station (Stand 7)"), ("MLB", "Mill Bank"), ("MSL", "Marsh Lane"),
                    ("OXC", "Oxenstall")],
               run_off=[7, 7, 8], run_pk=[8, 8, 9], inbound_extra=[0, 0, 0],
               km=[2.42, 2.73, 3.11], km_in=[2.42, 2.73, 3.19]),
    "19": dict(name="Grainford Bus Station - Langstrow Road - Felbeck",
               tps=[("GBS-9", "Grainford Bus Station (Stand 9)"), ("LGR", "Langstrow Road"),
                    ("FBG", "Felbeck Green"), ("FBK", "Felbeck, Church Lane")],
               run_off=[8, 7, 6], run_pk=[9, 8, 7], inbound_extra=[0, 0, 0],
               km=[2.97, 2.51, 2.08], km_in=[2.97, 2.51, 2.15]),
}
ROUTE_ORDER = ["6", "12", "14", "19", "22", "27", "33", "41", "58"]
MRI_ROUTES = ["22", "27", "33", "41", "58"]
GBS_ROUTES = ["6", "12", "14", "19"]

# the timing points' ATCO codes, one per direction (O outbound from the city, I inbound); the terminal stands
# and the outer termini are one stop serving both directions
def _tp_codes():
    codes, seen, n = {}, {}, 0
    for r in ROUTE_ORDER:
        tps = ROUTES[r]["tps"]
        for i, (key, name) in enumerate(tps):
            if key in STOPS:
                codes[(r, key, "O")] = codes[(r, key, "I")] = STOPS[key][0]
                continue
            if key not in seen:
                n += 1
                base = 3100 + n * 10
                last = i == len(tps) - 1
                seen[key] = ("2970A00%05d" % base, "2970A00%05d" % (base if last else base + 1))
            codes[(r, key, "O")], codes[(r, key, "I")] = seen[key]
    return codes


TP_ATCO = _tp_codes()

# fare stages on route 41 (the ticket machines record the stage number); stops between timing points included
FARE_STAGES_41 = [
    (1, "Merchant Row Interchange", ["Merchant Row Interchange (Stand D)"]),
    (2, "Tenter Street", ["Cloth Market", "Tenter Street"]),
    (3, "Thornsby Road", ["Thornsby Road", "Bridge End"]),
    (4, "Thornsby Quay", ["Thornsby Quay"]),
    (5, "Ravensholme Road", ["Ravensholme Road", "Oak Street"]),
    (6, "Ravensholme Bus Station", ["Ravensholme Bus Station"]),
]
UNSERVED_STAGES = (3, 4)     # the diversion leaves every stop in these stages without a bus

# headway bands: (start, end, headway) in minutes after midnight for outbound departures from the city stand;
# inbound departures from the outer stand are timed to the same pattern shifted by the route's offset
HEADWAYS = {
    "41": {"MF": [(5 * 60 + 52, 6 * 60 + 40, 24), (6 * 60 + 52, 19 * 60 + 4, 12), (19 * 60 + 28, 23 * 60 + 28, 24)],
           "SA": [(6 * 60 + 28, 8 * 60 + 4, 24), (8 * 60 + 16, 18 * 60 + 40, 12), (19 * 60 + 4, 23 * 60 + 28, 24)],
           "SU": [(7 * 60 + 40, 23 * 60 + 4, 24)]},
    "27": {"MF": [(5 * 60 + 51, 6 * 60 + 39, 24), (6 * 60 + 51, 19 * 60 + 3, 12), (19 * 60 + 27, 23 * 60 + 15, 24)],
           "SA": [(6 * 60 + 27, 8 * 60 + 3, 24), (8 * 60 + 15, 18 * 60 + 39, 12), (19 * 60 + 3, 23 * 60 + 15, 24)],
           "SU": [(7 * 60 + 39, 22 * 60 + 39, 24)]},
    "58": {"MF": [(5 * 60 + 52, 6 * 60 + 40, 24), (6 * 60 + 52, 19 * 60 + 4, 12), (19 * 60 + 28, 23 * 60 + 16, 24)],
           "SA": [(6 * 60 + 28, 8 * 60 + 4, 24), (8 * 60 + 16, 18 * 60 + 40, 12), (19 * 60 + 4, 23 * 60 + 16, 24)],
           "SU": [(7 * 60 + 40, 22 * 60 + 40, 24)]},
    "33": {"MF": [(6 * 60 + 2, 6 * 60 + 47, 15), (7 * 60 + 2, 19 * 60 + 2, 15), (19 * 60 + 32, 23 * 60 + 2, 30)],
           "SA": [(6 * 60 + 32, 8 * 60 + 2, 30), (8 * 60 + 17, 18 * 60 + 32, 15), (19 * 60 + 2, 23 * 60 + 2, 30)],
           "SU": [(8 * 60 + 2, 22 * 60 + 32, 30)]},
    "22": {"MF": [(6 * 60 + 10, 19 * 60 + 10, 20), (19 * 60 + 40, 23 * 60 + 10, 30)],
           "SA": [(7 * 60 + 10, 18 * 60 + 50, 20), (19 * 60 + 10, 23 * 60 + 10, 30)],
           "SU": [(8 * 60 + 40, 22 * 60 + 40, 30)]},
    "6": {"MF": [(5 * 60 + 45, 6 * 60 + 45, 20), (7 * 60 + 0, 19 * 60 + 0, 10), (19 * 60 + 20, 23 * 60 + 20, 20)],
          "SA": [(6 * 60 + 40, 8 * 60 + 0, 20), (8 * 60 + 10, 18 * 60 + 50, 10), (19 * 60 + 10, 23 * 60 + 10, 20)],
          "SU": [(7 * 60 + 45, 22 * 60 + 45, 20)]},
    "12": {"MF": [(5 * 60 + 55, 6 * 60 + 40, 15), (6 * 60 + 55, 18 * 60 + 55, 15), (19 * 60 + 25, 23 * 60 + 25, 30)],
           "SA": [(6 * 60 + 55, 18 * 60 + 40, 15), (19 * 60 + 10, 23 * 60 + 10, 30)],
           "SU": [(8 * 60 + 25, 22 * 60 + 25, 30)]},
    "14": {"MF": [(5 * 60 + 50, 6 * 60 + 35, 15), (6 * 60 + 50, 19 * 60 + 5, 15), (19 * 60 + 35, 23 * 60 + 5, 30)],
           "SA": [(6 * 60 + 50, 18 * 60 + 50, 15), (19 * 60 + 20, 23 * 60 + 20, 30)],
           "SU": [(8 * 60 + 20, 22 * 60 + 20, 30)]},
    "19": {"MF": [(6 * 60 + 5, 19 * 60 + 5, 20), (19 * 60 + 35, 23 * 60 + 5, 30)],
           "SA": [(7 * 60 + 5, 18 * 60 + 45, 20), (19 * 60 + 15, 23 * 60 + 15, 30)],
           "SU": [(8 * 60 + 35, 22 * 60 + 35, 30)]},
}
# inbound first departures from the outer stand: offset from the outbound pattern, minutes
INBOUND_OFFSET = {"41": 23, "27": 25, "58": 22, "33": 27, "22": 30, "6": 28, "12": 30, "14": 31, "19": 32}
# extra inbound journeys before the first outbound (the first buses run in from the depot end)
EARLY_INBOUND = {"41": [5 * 60 + 23, 5 * 60 + 47], "6": [5 * 60 + 31]}

# the weekday peaks (the traffic management plan's and the published timetable's time bands)
AM_PEAK = (7 * 60 + 30, 9 * 60 + 30)
PM_PEAK = (16 * 60, 18 * 60 + 30)


def peak(day_t, minute):
    if day_t != "MF":
        return False
    return AM_PEAK[0] <= minute < AM_PEAK[1] or PM_PEAK[0] <= minute < PM_PEAK[1]


def band(day_t, minute):
    if day_t == "MF" and AM_PEAK[0] <= minute < AM_PEAK[1]:
        return "AM peak"
    if day_t == "MF" and PM_PEAK[0] <= minute < PM_PEAK[1]:
        return "PM peak"
    return "Other times"


# ------------------------------------------------------------------ the closure (traffic management plan)
DIV_FROM, DIV_TO = "TNS", "RVR"       # route 41 leaves its line after Tenter Street and rejoins at Ravensholme Road
DIV_MIN_PEAK, DIV_MIN_OFF = 13, 10    # added running time between them (weekday peaks, other times)
DIV_KM_OUT, DIV_KM_IN = 3.6, 3.4      # added distance per journey
UNSERVED_TPS = ("THR", "TQY")
CORRIDOR_LINKS = {("6", "RJ4", "SML"), ("12", "RJ4", "RJ5")}   # the Ring Road crossing
CORRIDOR_MIN_PEAK = 2                 # added running time on the crossing in the weekday peaks

# ------------------------------------------------------------------ the performance schedule
EARLY_S, LATE_S = 60, 359             # on time: no more than 1 minute early, no more than 5 minutes 59 seconds late
FLOOR = 80.0

# ------------------------------------------------------------------ the duty schedule
WALK = {("MRI-D", "MRI-B"): 1, ("MRI-D", "MRI-C"): 2, ("MRI-D", "MRI-K"): 4, ("MRI-D", "MRI-F"): 3,
        ("MRI-B", "MRI-D"): 1, ("MRI-C", "MRI-D"): 2, ("MRI-K", "MRI-D"): 4, ("MRI-F", "MRI-D"): 3,
        ("MRI-B", "MRI-C"): 1, ("MRI-C", "MRI-B"): 1, ("MRI-B", "MRI-K"): 4, ("MRI-K", "MRI-B"): 4,
        ("MRI-C", "MRI-K"): 4, ("MRI-K", "MRI-C"): 4, ("MRI-B", "MRI-F"): 3, ("MRI-F", "MRI-B"): 3,
        ("MRI-C", "MRI-F"): 3, ("MRI-F", "MRI-C"): 3, ("MRI-K", "MRI-F"): 4, ("MRI-F", "MRI-K"): 4,
        ("GBS-3", "GBS-5"): 1, ("GBS-5", "GBS-3"): 1, ("GBS-3", "GBS-7"): 2, ("GBS-7", "GBS-3"): 2,
        ("GBS-3", "GBS-9"): 2, ("GBS-9", "GBS-3"): 2, ("GBS-5", "GBS-7"): 1, ("GBS-7", "GBS-5"): 1,
        ("GBS-5", "GBS-9"): 2, ("GBS-9", "GBS-5"): 2, ("GBS-7", "GBS-9"): 1, ("GBS-9", "GBS-7"): 1}
PNB = 20                              # a personal needs break taken at a changeover after a long first piece

PEOPLE = {"authority": "Molly Hughes", "operator": "Shaun Brown", "council": "Damien Ward",
          "scheduler": "Elliott Sharp", "clerk": "Yvonne Warner"}
AUTHORITY = "Grainford City Region Combined Authority"
OPERATOR = "Pellbridge Buses"
COUNCIL = "Grainford City Council"
