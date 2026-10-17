"""The Vellmouth subway as the generator holds it before any record is written: lines and stations, platforms,
the morning flows onto and off every platform, the riding calendar, the service plans and the fleet.

Every flow is a rate in people per minute at the morning peak, shaped through the morning by `profile`. A station's
inbound platform on a suburban branch fills the trains that reach the first interchange; at Sallow Park (Lines 1
and 4) and Corran Junction (Line 5) those trains arrive with less room than a headway's arrivals on Tuesday to
Thursday mornings, so the riders a full train cannot take wait for the next one. Nothing in any record says so."""
from __future__ import annotations

import datetime as dt
import math

from common import HOLIDAYS, REDUCED, WINTER_WEEK

# ------------------------------------------------------------------------------------------------- lines
# stations listed in the inbound (morning peak) direction for the radial lines; for the crosstown lines in the
# direction named first. run: minutes from each station to the next.
LINES = {
    "1": dict(name="Line 1", dirs=("S", "N"), inbound="S",
              stations=["Kettle Creek", "Dorrance", "Whitcombe", "Pell Corners", "Norland", "Larch Hill",
                        "Sallow Park", "Hesper Avenue", "Quarry Road", "Civic Center", "Market Street",
                        "Harbor Terminal"],
              run=[3.0, 2.5, 2.5, 3.0, 2.5, 3.0, 2.0, 2.0, 2.5, 1.5, 2.0]),
    "4": dict(name="Line 4", dirs=("S", "N"), inbound="S",
              stations=["Arbor Mills", "Ganton", "Brisco Road", "Coyle Street", "Tamsin Avenue", "Sallow Park",
                        "Ferrier Square", "Market Street", "Wharf Street"],
              run=[3.0, 3.0, 2.5, 2.5, 3.0, 2.5, 2.5, 1.5]),
    "5": dict(name="Line 5", dirs=("W", "E"), inbound="W",
              stations=["Ossory", "Linden Park", "Coldwater", "Marchmont", "Easton Heights", "Brack Road",
                        "Corran Junction", "Ferrier Square", "Civic Center", "Bayfront"],
              run=[3.0, 2.5, 2.5, 3.0, 2.5, 3.0, 2.5, 2.0, 2.0]),
    "2": dict(name="Line 2", dirs=("E", "W"), inbound=None,
              stations=["Westmere", "Holloway", "Garnett Street", "Tanner Street", "Civic Center",
                        "Corran Junction", "Eastgate", "Shore Road"],
              run=[2.5, 2.5, 2.0, 2.0, 2.5, 2.5, 3.0]),
    "3": dict(name="Line 3", dirs=("S", "N"), inbound=None,
              stations=["Northgate", "Elm Rise", "Hesper Avenue", "Garnett Street", "Albrecht Place",
                        "University", "Medical Center"],
              run=[3.0, 2.5, 2.5, 2.5, 2.0, 2.0]),
    "6": dict(name="Line 6", dirs=("E", "W"), inbound=None,
              stations=["Foundry Row", "Albrecht Place", "Quarry Road", "Mint Street", "Civic Center",
                        "Harbor Terminal"],
              run=[2.5, 2.5, 2.0, 2.0, 1.5]),
}
DIR_WORD = {"S": "Southbound", "N": "Northbound", "E": "Eastbound", "W": "Westbound"}

# cars per train by service plan (Line 5 moves to eight cars with the spring 2027 pick)
CARS = {"autumn2026": {"1": 6, "4": 6, "5": 6, "2": 8, "3": 6, "6": 6},
        "spring2027": {"1": 6, "4": 6, "5": 8, "2": 8, "3": 6, "6": 6}}
CAR_MAX = 150        # the fleet register's maximum load per car (people)
CAR_PLANNING = 110   # the fleet register's planning load per car


def headway(line, minute, plan="autumn2026"):
    """Scheduled minutes between trains at the origin for a departure at `minute` after local midnight."""
    peak = {"1": 4.0, "4": 4.0, "5": 4.0, "2": 6.0, "3": 6.0, "6": 7.5}[line]
    shoulder = {"1": 6.0, "4": 6.0, "5": 6.0, "2": 8.0, "3": 8.0, "6": 10.0}[line]
    if 6 * 60 + 30 <= minute < 9 * 60 + 30:
        return peak
    return shoulder


def departures(line, plan="autumn2026", start=5 * 60 + 30, end=10 * 60 + 30):
    out, t = [], float(start)
    while t <= end:
        out.append(t)
        t += headway(line, t, plan)
    return out


def arrival_offsets(line, direction):
    """Minutes from the origin departure to the arrival at each station, in the direction of travel."""
    L = LINES[line]
    stations = L["stations"] if direction == L["dirs"][0] else list(reversed(L["stations"]))
    runs = L["run"] if direction == L["dirs"][0] else list(reversed(L["run"]))
    offs, t = {}, 0.0
    for i, s in enumerate(stations):
        offs[s] = t
        if i < len(runs):
            t += runs[i] + 0.5
    return stations, offs


# ------------------------------------------------------------------------------------------------- complexes
COMPLEX_IDS = {}
_order = []
for _l in ("1", "4", "5", "2", "3", "6"):
    for _s in LINES[_l]["stations"]:
        if _s not in _order:
            _order.append(_s)
# the export's complex ids: assigned when the back office went live, in the order the stations were surveyed
_ids = [204, 207, 209, 212, 215, 218, 221, 226, 229, 233, 236, 239, 241, 244, 247, 250, 252, 255, 258, 261, 263,
        266, 268, 271, 274, 277, 280, 283, 286, 289, 292, 295, 298, 301, 304, 307, 310, 313, 316, 319]
for _s, _i in zip(_order, _ids):
    COMPLEX_IDS[_s] = _i
COMPLEXES = list(_order)

WATCH_COMPLEXES = ["Garnett Street", "Sallow Park", "Hesper Avenue", "Corran Junction", "Ferrier Square",
                   "Albrecht Place", "Quarry Road"]


def lines_at(station):
    return [l for l in LINES if station in LINES[l]["stations"]]


# ------------------------------------------------------------------------------------------------- platforms
# Side platforms serve one direction; an island serves both directions of its line.
ISLANDS = {("Garnett Street", "2"), ("Hesper Avenue", "3"), ("Corran Junction", "2"), ("Albrecht Place", "6"),
           ("Quarry Road", "6"), ("Civic Center", "2"), ("Civic Center", "6"), ("Market Street", "4"),
           ("Eastgate", "2"), ("University", "3"), ("Mint Street", "6"), ("Holloway", "2"), ("Elm Rise", "3")}


def platforms_at(station):
    """[(platform key, line, (directions,))] for every platform at a station."""
    out = []
    for l in lines_at(station):
        if (station, l) in ISLANDS:
            out.append(("%s|%s" % (station, l), l, LINES[l]["dirs"]))
        else:
            for d in LINES[l]["dirs"]:
                out.append(("%s|%s%s" % (station, l, d), l, (d,)))
    return out


# the platform crowding standard's schedule: (platform key, register code, rated capacity)
WATCH = [
    ("Garnett Street|2", "GAR-2", 380),
    ("Garnett Street|3S", "GAR-3S", 300),
    ("Sallow Park|1S", "SAL-1S", 460),
    ("Sallow Park|1N", "SAL-1N", 400),
    ("Sallow Park|4S", "SAL-4S", 500),
    ("Hesper Avenue|1S", "HES-1S", 380),
    ("Hesper Avenue|3", "HES-3", 420),
    ("Corran Junction|5W", "COR-5W", 470),
    ("Corran Junction|2", "COR-2", 360),
    ("Ferrier Square|5W", "FER-5W", 330),
    ("Ferrier Square|4S", "FER-4S", 330),
    ("Ferrier Square|4N", "FER-4N", 330),
    ("Albrecht Place|3S", "ALB-3S", 450),
    ("Albrecht Place|3N", "ALB-3N", 300),
    ("Albrecht Place|6", "ALB-6", 240),
    ("Quarry Road|1S", "QUA-1S", 340),
    ("Quarry Road|6", "QUA-6", 200),
]
WATCH_KEYS = [w[0] for w in WATCH]
CAPACITY = {w[0]: w[2] for w in WATCH}
CODE = {w[0]: w[1] for w in WATCH}

# the hybrid-day sample: last spring's top platform in each complex then on the watch list (Sallow Park joined the
# watch list in September 2026, after the Larch Hill and Tamsin Avenue housing opened, and has no hybrid-day counts)
HYBRID_SAMPLE = ["Garnett Street|2", "Hesper Avenue|3", "Corran Junction|5W", "Ferrier Square|5W",
                 "Albrecht Place|6", "Quarry Road|6"]

# ------------------------------------------------------------------------------------------------- the morning
def profile(minute, mu, sd, early=0.18):
    """Morning arrival shape, 1.0 at its peak: a commuter peak at mu with an early shift-worker shoulder."""
    main = math.exp(-0.5 * ((minute - mu) / sd) ** 2)
    shoulder = early * math.exp(-0.5 * ((minute - (mu - 75)) / 30.0) ** 2)
    base = 0.06
    return (main + shoulder + base) / (1.0 + early * math.exp(-0.5 * (75 / 30.0) ** 2) + base)


# Flows by (station, line, direction): board = street arrivals onto the platform for that direction (people per
# minute at the peak), exit = riders leaving trains of that direction at the station who go out to the street,
# mu and sd the timing (minutes after local midnight). Transfers are listed separately and count both as an
# alighting on the platform they leave and an arrival on the platform they join. Riders further out on a branch
# travel earlier.
_B = {}
def _f(station, line, d, board, exit_, mu=490, sd=34):
    _B[(station, line, d)] = dict(board=board, exit=exit_, mu=mu, sd=sd)

# Line 1
_f('Kettle Creek', '1', 'S', 44.4, 1.0, 467, 28)
_f('Kettle Creek', '1', 'N', 2.5, 3.0, 480, 40)
_f('Dorrance', '1', 'S', 25.8, 1.0, 470, 28)
_f('Dorrance', '1', 'N', 2.5, 3.0, 480, 40)
_f('Whitcombe', '1', 'S', 28.0, 1.0, 473, 28)
_f('Whitcombe', '1', 'N', 2.5, 3.0, 480, 40)
_f('Pell Corners', '1', 'S', 30.4, 1.0, 476, 28)
_f('Pell Corners', '1', 'N', 2.5, 3.0, 480, 40)
_f('Norland', '1', 'S', 32.8, 1.0, 479, 28)
_f('Norland', '1', 'N', 2.5, 3.0, 480, 40)
_f('Larch Hill', '1', 'S', 39.8, 1.0, 482, 28)
_f('Larch Hill', '1', 'N', 2.5, 3.0, 480, 40)
_f('Sallow Park', '1', 'S', 70.7, 6.0, 487, 28)
_f('Sallow Park', '1', 'N', 12.3, 4.0, 482, 40)
_f('Hesper Avenue', '1', 'S', 27.9, 22.0, 489, 32)
_f('Hesper Avenue', '1', 'N', 10.0, 9.0, 480, 40)
_f('Quarry Road', '1', 'S', 37.2, 18.0, 492, 32)
_f('Quarry Road', '1', 'N', 8.0, 10.0, 480, 40)
_f('Civic Center', '1', 'S', 10.0, 95.0, 498, 34)
_f('Civic Center', '1', 'N', 14.0, 18.0, 485, 40)
_f('Market Street', '1', 'S', 6.0, 70.0, 500, 34)
_f('Market Street', '1', 'N', 10.0, 8.0, 485, 40)
_f('Harbor Terminal', '1', 'S', 0.0, 60.0, 503, 34)
_f('Harbor Terminal', '1', 'N', 14.0, 0.0, 485, 40)

# Line 4
_f('Arbor Mills', '4', 'S', 47.1, 1.0, 468, 28)
_f('Arbor Mills', '4', 'N', 2.5, 3.0, 480, 40)
_f('Ganton', '4', 'S', 35.3, 1.0, 472, 28)
_f('Ganton', '4', 'N', 2.5, 3.0, 480, 40)
_f('Brisco Road', '4', 'S', 37.7, 1.0, 475, 28)
_f('Brisco Road', '4', 'N', 2.5, 3.0, 480, 40)
_f('Coyle Street', '4', 'S', 40.1, 1.0, 478, 28)
_f('Coyle Street', '4', 'N', 2.5, 3.0, 480, 40)
_f('Tamsin Avenue', '4', 'S', 44.8, 1.0, 481, 28)
_f('Tamsin Avenue', '4', 'N', 2.5, 3.0, 480, 40)
_f('Sallow Park', '4', 'S', 77.1, 6.0, 487, 28)
_f('Sallow Park', '4', 'N', 8.0, 4.0, 482, 40)
_f('Ferrier Square', '4', 'S', 24.3, 36.0, 492, 32)
_f('Ferrier Square', '4', 'N', 13.9, 8.0, 480, 40)
_f('Market Street', '4', 'S', 5.0, 80.0, 499, 34)
_f('Market Street', '4', 'N', 9.0, 7.0, 485, 40)
_f('Wharf Street', '4', 'S', 0.0, 55.0, 502, 34)
_f('Wharf Street', '4', 'N', 11.0, 0.0, 485, 40)

# Line 5
_f('Ossory', '5', 'W', 42.6, 1.0, 467, 28)
_f('Ossory', '5', 'E', 2.5, 3.0, 480, 40)
_f('Linden Park', '5', 'W', 27.7, 1.0, 470, 28)
_f('Linden Park', '5', 'E', 2.5, 3.0, 480, 40)
_f('Coldwater', '5', 'W', 29.9, 1.0, 473, 28)
_f('Coldwater', '5', 'E', 2.5, 3.0, 480, 40)
_f('Marchmont', '5', 'W', 32.0, 1.0, 476, 28)
_f('Marchmont', '5', 'E', 2.5, 3.0, 480, 40)
_f('Easton Heights', '5', 'W', 32.0, 1.0, 479, 28)
_f('Easton Heights', '5', 'E', 2.5, 3.0, 480, 40)
_f('Brack Road', '5', 'W', 34.1, 1.0, 482, 28)
_f('Brack Road', '5', 'E', 2.5, 3.0, 480, 40)
_f('Corran Junction', '5', 'W', 63.1, 5.0, 488, 28)
_f('Corran Junction', '5', 'E', 9.0, 5.0, 482, 40)
_f('Ferrier Square', '5', 'W', 20.8, 25.0, 491, 32)
_f('Ferrier Square', '5', 'E', 10.0, 8.0, 482, 40)
_f('Civic Center', '5', 'W', 8.0, 95.0, 498, 34)
_f('Civic Center', '5', 'E', 12.0, 14.0, 485, 40)
_f('Bayfront', '5', 'W', 0.0, 50.0, 502, 34)
_f('Bayfront', '5', 'E', 10.0, 0.0, 485, 40)

# Line 2
_f('Westmere', '2', 'E', 12.0, 0.0, 486, 34)
_f('Westmere', '2', 'W', 0.0, 16.0, 486, 34)
_f('Holloway', '2', 'E', 12.0, 2.0, 486, 34)
_f('Holloway', '2', 'W', 6.0, 10.0, 486, 34)
_f('Garnett Street', '2', 'E', 67.7, 8.0, 486, 34)
_f('Garnett Street', '2', 'W', 22.6, 12.0, 486, 34)
_f('Tanner Street', '2', 'E', 20.0, 10.0, 486, 34)
_f('Tanner Street', '2', 'W', 8.0, 14.0, 486, 34)
_f('Civic Center', '2', 'E', 6.0, 60.0, 486, 34)
_f('Civic Center', '2', 'W', 6.0, 70.0, 486, 34)
_f('Corran Junction', '2', 'E', 24.1, 12.0, 486, 34)
_f('Corran Junction', '2', 'W', 72.2, 8.0, 486, 34)
_f('Eastgate', '2', 'E', 6.0, 10.0, 486, 34)
_f('Eastgate', '2', 'W', 30.0, 2.0, 486, 34)
_f('Shore Road', '2', 'E', 0.0, 18.0, 486, 34)
_f('Shore Road', '2', 'W', 34.0, 0.0, 486, 34)

# Line 3
_f('Northgate', '3', 'S', 24.0, 0.0, 484, 33)
_f('Northgate', '3', 'N', 0.0, 12.0, 484, 33)
_f('Elm Rise', '3', 'S', 20.0, 2.0, 484, 33)
_f('Elm Rise', '3', 'N', 4.0, 10.0, 484, 33)
_f('Hesper Avenue', '3', 'S', 9.7, 6.0, 484, 33)
_f('Hesper Avenue', '3', 'N', 4.4, 22.0, 484, 33)
_f('Garnett Street', '3', 'S', 8.2, 10.0, 484, 33)
_f('Garnett Street', '3', 'N', 12.0, 14.0, 484, 33)
_f('Albrecht Place', '3', 'S', 38.0, 12.0, 484, 33)
_f('Albrecht Place', '3', 'N', 26.5, 8.0, 484, 33)
_f('University', '3', 'S', 6.0, 48.0, 484, 33)
_f('University', '3', 'N', 10.0, 6.0, 484, 33)
_f('Medical Center', '3', 'S', 0.0, 40.0, 484, 33)
_f('Medical Center', '3', 'N', 10.0, 0.0, 484, 33)

# Line 6
_f('Foundry Row', '6', 'E', 26.0, 0.0, 486, 34)
_f('Foundry Row', '6', 'W', 0.0, 10.0, 486, 34)
_f('Albrecht Place', '6', 'E', 26.4, 6.0, 486, 34)
_f('Albrecht Place', '6', 'W', 8.8, 12.0, 486, 34)
_f('Quarry Road', '6', 'E', 20.6, 10.0, 486, 34)
_f('Quarry Road', '6', 'W', 10.3, 10.0, 486, 34)
_f('Mint Street', '6', 'E', 12.0, 16.0, 486, 34)
_f('Mint Street', '6', 'W', 6.0, 8.0, 486, 34)
_f('Civic Center', '6', 'E', 4.0, 40.0, 486, 34)
_f('Civic Center', '6', 'W', 8.0, 12.0, 486, 34)
_f('Harbor Terminal', '6', 'E', 0.0, 30.0, 486, 34)
_f('Harbor Terminal', '6', 'W', 10.0, 0.0, 486, 34)

FLOWS = _B

# transfers between platforms at an interchange: (station, from line+dir, to line+dir, people per minute at peak)
TRANSFERS = [
    ("Sallow Park", "1S", "4S", 12), ("Sallow Park", "4S", "1S", 14), ("Sallow Park", "1N", "4N", 2),
    ("Sallow Park", "4N", "1N", 2),
    ("Hesper Avenue", "1S", "3S", 34), ("Hesper Avenue", "1S", "3N", 12), ("Hesper Avenue", "3S", "1S", 10),
    ("Hesper Avenue", "3N", "1S", 8), ("Hesper Avenue", "3S", "1N", 3), ("Hesper Avenue", "1N", "3S", 3),
    ("Quarry Road", "1S", "6E", 14), ("Quarry Road", "1S", "6W", 6), ("Quarry Road", "6E", "1S", 6),
    ("Quarry Road", "6W", "1S", 5),
    ("Corran Junction", "5W", "2W", 12), ("Corran Junction", "2W", "5W", 18), ("Corran Junction", "5W", "2E", 3),
    ("Corran Junction", "2E", "5W", 4), ("Corran Junction", "5E", "2W", 2),
    ("Ferrier Square", "5W", "4S", 14), ("Ferrier Square", "4S", "5W", 12), ("Ferrier Square", "4N", "5W", 3),
    ("Ferrier Square", "5E", "4N", 3), ("Ferrier Square", "4S", "5E", 3),
    ("Garnett Street", "2E", "3S", 14), ("Garnett Street", "3S", "2E", 16), ("Garnett Street", "2W", "3S", 6),
    ("Garnett Street", "3N", "2E", 8), ("Garnett Street", "2E", "3N", 4),
    ("Albrecht Place", "3S", "6E", 8), ("Albrecht Place", "6W", "3S", 10), ("Albrecht Place", "3N", "6E", 10),
    ("Albrecht Place", "6E", "3S", 4), ("Albrecht Place", "6W", "3N", 4),
    ("Civic Center", "1S", "2E", 8), ("Civic Center", "5W", "2W", 6), ("Civic Center", "2E", "6E", 4),
    ("Market Street", "1S", "4S", 4), ("Market Street", "4S", "1S", 4),
    ("Harbor Terminal", "1S", "6W", 2),
]


# ------------------------------------------------------------------------------------------------- the calendar
# morning riding on an ordinary weekday, against the Tuesday-to-Thursday mean (the same across the network within
# a point; each complex carries a small offset of its own, `wd_jitter`)
WEEKDAY = {"Mon": 0.82, "Tue": 1.00, "Wed": 1.01, "Thu": 0.99, "Fri": 0.76}
# riding by month against October, weekday mornings
MONTH = {1: 0.935, 2: 0.965, 3: 1.0, 4: 0.995, 5: 0.99, 6: 0.95, 7: 0.865, 8: 0.845, 9: 0.98, 10: 1.0,
         11: 0.99, 12: 0.94}
# the network's level by year (recovery levelling off), weekday mornings, October = 1 in each year's own terms
YEAR = {2022: 0.80, 2023: 0.885, 2024: 0.935, 2025: 0.965, 2026: 0.98, 2027: 0.987}


def year_level(d):
    """Smooth level through the years, interpolated mid-year to mid-year."""
    y = d.year + (d.timetuple().tm_yday - 0.5) / 365.25 - 0.5
    y0 = int(math.floor(y))
    f = y - y0
    a = YEAR.get(y0, YEAR[min(YEAR, key=lambda k: abs(k - y0))])
    b = YEAR.get(y0 + 1, YEAR[min(YEAR, key=lambda k: abs(k - y0 - 1))])
    return a + (b - a) * f


def day_kind(d):
    if d in HOLIDAYS:
        return "holiday"
    if d.weekday() == 5:
        return "Sat"
    if d.weekday() == 6:
        return "Sun"
    if d in REDUCED:
        return "reduced"
    if d in WINTER_WEEK:
        return "winter"
    return ["Mon", "Tue", "Wed", "Thu", "Fri"][d.weekday()]


# each complex's own Monday and Friday, against the network's (its catchment's share of hybrid workers)
WD_OFFSET = {}
for _i, _s in enumerate(COMPLEXES):
    _a = ((_i * 37) % 11 - 5) / 500.0
    _b = ((_i * 53) % 13 - 6) / 500.0
    WD_OFFSET[_s] = (_a, _b)
WD_OFFSET.update({"Garnett Street": (0.006, -0.004), "Sallow Park": (-0.008, -0.010), "Hesper Avenue": (-0.004, 0.006),
                  "Corran Junction": (0.004, -0.006), "Ferrier Square": (0.010, 0.004), "Albrecht Place": (-0.010, 0.008),
                  "Quarry Road": (0.008, -0.008)})


def weekday_factor(station, wd):
    base = WEEKDAY[wd]
    if wd == "Mon":
        return base + WD_OFFSET[station][0]
    if wd == "Fri":
        return base + WD_OFFSET[station][1]
    return base


def demand_factor(d, jitter=0.0):
    """Morning-peak riding on date d against an ordinary October 2026 Tuesday-to-Thursday morning."""
    k = day_kind(d)
    wd = {"Mon": WEEKDAY["Mon"], "Tue": WEEKDAY["Tue"], "Wed": WEEKDAY["Wed"], "Thu": WEEKDAY["Thu"],
          "Fri": WEEKDAY["Fri"], "reduced": 0.84, "winter": 0.62, "holiday": 0.30, "Sat": 0.28, "Sun": 0.20}[k]
    if k in ("Mon", "Fri"):
        wd += jitter
    return wd * MONTH[d.month] * year_level(d) / year_level(dt.date(2026, 10, 15))


# ------------------------------------------------------------------------------------------------- station elements
# The engineering inventory's view of each station: stairs, escalators and elevators between the street, the
# mezzanines and the platforms. Lines 1 to 4 were built 1968 to 1974 and their drawings are in inches, escalators by
# nominal (balustrade) width, 32 or 48 inches; Lines 5 and 6 (2004 and 2009) are metric, escalators by step width.
# escalators by step width (24 or 40 inches). The older lines' escalators were slowed from 0.5 to 0.45 metres a
# second in the 2019 step-chain programme; the change is in the maintenance system, not the engineering inventory.
ERA_METRIC = {"5", "6"}
STEP_IN_TO_MM = {24: 600, 40: 1000}
SPEED_SET = {"in": 0.45, "mm": 0.5}
SPEED_DESIGN = 0.5


def _plat_label(key):
    station, rest = key.split("|")
    line = rest[0]
    if len(rest) == 1:
        return "Line %s island platform" % line
    return "Line %s %s platform" % (line, DIR_WORD[rest[1:]].lower())


# Escalators at the watch-list complexes: (platform key, unit, size, default direction, direction at 08:00).
# Pairs run one up and one down outside the peaks; in the morning peak station operations turn the pair at a
# boarding platform both down and at an alighting platform both up, and a single escalator at a boarding platform
# down. Step widths: inches on Lines 1 to 4, millimetres on Lines 5 and 6.
WATCH_ESCALATORS = {
    "Garnett Street": [("Garnett Street|2", "E1", 24, "up", "down"), ("Garnett Street|2", "E2", 24, "down", "down"),
                       ("Garnett Street|3S", "E3", 24, "up", "up"), ("Garnett Street|3N", "E5", 24, "up", "up"),
                       ("Garnett Street|3N", "E6", 40, "down", "up")],
    "Sallow Park": [("Sallow Park|1S", "E1", 24, "up", "down"), ("Sallow Park|1S", "E2", 24, "down", "down"),
                    ("Sallow Park|1N", "E3", 24, "up", "up"), ("Sallow Park|4S", "E4", 40, "up", "down"),
                    ("Sallow Park|4S", "E5", 40, "down", "down"), ("Sallow Park|4N", "E6", 24, "up", "up")],
    "Hesper Avenue": [("Hesper Avenue|1S", "E1", 24, "up", "down"), ("Hesper Avenue|1S", "E2", 40, "down", "down"),
                      ("Hesper Avenue|3", "E3", 24, "up", "up"), ("Hesper Avenue|3", "E4", 40, "down", "up"),
                      ("Hesper Avenue|1N", "E5", 24, "up", "up")],
    "Corran Junction": [("Corran Junction|5W", "E1", 1000, "up", "down"), ("Corran Junction|5W", "E2", 1000, "down", "down"),
                        ("Corran Junction|5E", "E3", 800, "up", "up"), ("Corran Junction|2", "E4", 24, "up", "down"),
                        ("Corran Junction|2", "E5", 24, "down", "down"), ("Corran Junction|2", "E6", 24, "up", "up")],
    "Ferrier Square": [("Ferrier Square|5W", "E1", 800, "up", "up"), ("Ferrier Square|5W", "E5", 1000, "down", "up"),
                       ("Ferrier Square|4S", "E2", 24, "up", "up"),
                       ("Ferrier Square|4S", "E3", 40, "down", "up"), ("Ferrier Square|4N", "E4", 24, "up", "down")],
    "Albrecht Place": [("Albrecht Place|3S", "E1", 24, "up", "down"), ("Albrecht Place|3S", "E2", 24, "down", "down"),
                       ("Albrecht Place|3N", "E3", 24, "up", "down"), ("Albrecht Place|6", "E4", 1000, "up", "down"),
                       ("Albrecht Place|6", "E5", 1000, "down", "down"), ("Albrecht Place|3N", "E6", 24, "up", "up")],
    "Quarry Road": [("Quarry Road|1S", "E1", 24, "up", "down"), ("Quarry Road|1S", "E2", 24, "down", "down"),
                    ("Quarry Road|1N", "E3", 24, "up", "up"), ("Quarry Road|6", "E4", 800, "up", "down"),
                    ("Quarry Road|6", "E5", 800, "down", "up")],
}
# street escalators (street to mezzanine) at the larger complexes: unit, size, default direction
STREET_ESCALATORS = {"Garnett Street": [("E4", 40, "up")], "Corran Junction": [("E7", 1000, "up")],
                     "Albrecht Place": [("E7", 24, "up"), ("E8", 24, "down")], "Civic Center": [("E1", 40, "up"), ("E2", 40, "down")],
                     "Harbor Terminal": [("E1", 40, "up")], "Market Street": [("E1", 40, "up")]}

# the planning manual's rated flows, people a minute by step width (mm), at 0.5 m/s and in proportion at other speeds
RATED_FLOW = {600: 40, 800: 60, 1000: 80}


def elements():
    """Every element in the engineering inventory: one dict per stair, escalator and elevator."""
    out = []
    for s in COMPLEXES:
        cid = COMPLEX_IDS[s]
        metric_only = all(l in ERA_METRIC for l in lines_at(s))
        big = s in WATCH_COMPLEXES or s in ("Civic Center", "Market Street", "Harbor Terminal", "University",
                                           "Medical Center", "Bayfront", "Wharf Street", "Eastgate")
        mezz = ["North mezzanine", "South mezzanine"] if big else ["Mezzanine"]
        n_street = 3 if big else 2
        k = 0
        for i in range(n_street):
            k += 1
            w = [72, 84, 96, 66][(cid + i) % 4] if not metric_only else [1800, 2100, 2400][(cid + i) % 3]
            out.append(dict(unit=("%d-S%d" % (cid, k)), complex=s, kind="stair", frm="Street",
                            to=mezz[i % len(mezz)], width=w, unit_sys="mm" if metric_only else "in",
                            direction=""))
        for (u, size, dirn) in STREET_ESCALATORS.get(s, []):
            out.append(dict(unit="%d-%s" % (cid, u), complex=s, kind="escalator", frm="Street", to=mezz[0],
                            width=size, unit_sys="mm" if size >= 600 else "in", direction=dirn))
        # platforms
        lifts = 0
        esc = {e[1]: e for e in WATCH_ESCALATORS.get(s, [])}
        for j, (key, line, dirs) in enumerate(platforms_at(s)):
            metric = line in ERA_METRIC
            label = _plat_label(key)
            busy = key in CAPACITY or big
            n_st = 2 if busy else 1
            for i in range(n_st):
                k += 1
                w = ([60, 56, 64, 72][(cid + j + i) % 4] if not metric else [1700, 1900, 2200][(cid + j + i) % 3])
                out.append(dict(unit="%d-S%d" % (cid, k), complex=s, kind="stair", frm=mezz[(j + i) % len(mezz)],
                                to=label, width=w, unit_sys="mm" if metric else "in", direction=""))
            if s in WATCH_ESCALATORS:
                for u, e in sorted(esc.items()):
                    if e[0] == key:
                        size = e[2]
                        out.append(dict(unit="%d-%s" % (cid, u), complex=s, kind="escalator",
                                        frm=mezz[j % len(mezz)], to=label, width=size,
                                        unit_sys="mm" if size >= 600 else "in", direction=e[3], am=e[4]))
            elif big:
                k2 = sum(1 for o in out if o["complex"] == s and o["kind"] == "escalator") + 1
                size = 1000 if metric else 40
                out.append(dict(unit="%d-E%d" % (cid, k2), complex=s, kind="escalator", frm=mezz[j % len(mezz)],
                                to=label, width=size, unit_sys="mm" if metric else "in", direction="up", am="up"))
            lifts += 1
            out.append(dict(unit="%d-L%d" % (cid, lifts), complex=s, kind="elevator", frm=mezz[j % len(mezz)],
                            to=label, width=0, unit_sys="", direction=""))
        lifts += 1
        out.append(dict(unit="%d-L%d" % (cid, lifts), complex=s, kind="elevator", frm="Street", to=mezz[0],
                        width=0, unit_sys="", direction=""))
    return out


ELEMENTS = elements()


def step_mm(e):
    """An escalator's step width in mm."""
    return STEP_IN_TO_MM[e["width"]] if e["unit_sys"] == "in" else e["width"]
