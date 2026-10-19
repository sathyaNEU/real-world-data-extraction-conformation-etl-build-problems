"""The world of task468: the City of Larkhaven's transit department, its candidate routes for the state Department of
Transportation's Frequent Transit Corridors Program (FY2027 round), the departures its buses made from the routes'
designated stops from January to June 2026 as two AVL vendors recorded them, the vendors' trip matchers, and Service
Quality's monthly review of the stop events the matchers left without a trip."""
import datetime as dt
from zoneinfo import ZoneInfo

SEED = 468
TZ = ZoneInfo("America/Chicago")

# ---------------------------------------------------------------- dates
FIRST_DAY = dt.date(2026, 1, 1)
LAST_DAY = dt.date(2026, 6, 30)            # the qualifying period, January to June 2026
GO_LIVE_UTC = dt.datetime(2026, 4, 1, 0, 0, tzinfo=dt.timezone.utc)   # Quinnell's first record (7 p.m. on 31 March)
TIMETABLE_CHANGE = dt.date(2026, 4, 5)     # the April timetable and feed (stop IDs renumbered, stop codes kept)
STATE_HOLIDAYS = [dt.date(2026, 1, 1), dt.date(2026, 1, 19), dt.date(2026, 2, 16), dt.date(2026, 5, 25)]
GOOD_FRIDAY = dt.date(2026, 4, 3)          # the department runs its Saturday timetable; not a state holiday
SNOW_DAY = dt.date(2026, 2, 3)             # the department ran its Saturday timetable that day (not in the feed)
CLASS_DAYS = [(dt.date(2026, 1, 12), dt.date(2026, 3, 6)), (dt.date(2026, 3, 16), dt.date(2026, 5, 1))]
AS_OF = "2026-10-30"
COUNCIL_MEETING = dt.date(2026, 11, 17)
APPLICATION_CLOSES = dt.date(2026, 12, 1)
HOURS = list(range(6, 19))                 # the clock hours from 6 a.m. to 7 p.m.
STANDARD = 4.0                             # departures an hour, averaged over the counting days
CAP = 5                                    # routes an agency may nominate
WINDOW_MIN = 7.0                           # both vendors' trip-matching window either side of the timetable
LOGON_FAULT = 0.005                        # stop events left unmatched by an operator logon fault, any route
ON_TIME = (-60, 300)                       # the state's on-time band, seconds early and late, inclusive

# ---------------------------------------------------------------- stops: code, January stop_id, April stop_id, name
STOPS = {
    "A": ("1040", "10402", "6001", "Main St & 4th St (Transit Mall, bay C)"),
    "B": ("1093", "10931", "6014", "Main St & 9th St"),
    "C": ("2210", "22104", "6102", "Union Station"),
    "D": ("3307", "33071", "6230", "University Ave & College Dr"),
    "E": ("4415", "44150", "6311", "Westgate Transit Center"),
}
STOP_ROUTES = {"A": ["2", "4", "17", "3"], "B": ["6", "9"], "C": ["11", "14", "22", "12"], "D": ["31"],
               "E": ["40", "51", "60"]}
STOP_OF = {r: s for s, rs in STOP_ROUTES.items() for r in rs}
CANDIDATES = ["2", "4", "6", "9", "11", "14", "17", "22", "31", "40", "51"]
ROUTE_NAMES = {"2": "Grand Avenue", "3": "Westside", "4": "Lincoln Avenue", "6": "Oak Street", "9": "Riverside",
               "11": "University Connector", "12": "Northgate", "14": "Elm Park", "17": "Prairie Road",
               "22": "Fairgrounds", "31": "College Hill", "40": "Westgate Crosstown", "51": "Hillcrest", "60": "Mill Creek"}
INTERLINE = [["2", "17"], ["4", "3"], ["6", "9"], ["11", "22"], ["14", "12"], ["40", "51", "60"], ["31"]]
# minutes from a trip's first stop to the designated stop (0 where the trip starts there)
OFFSET = {"2": 17, "4": 14, "17": 19, "3": 12, "6": 11, "9": 9, "11": 0, "14": 0, "22": 0, "12": 0, "31": 13,
          "40": 0, "51": 0, "60": 0}
DWELL = {"2": 4, "4": 3, "17": 4, "3": 3, "6": 1, "9": 1, "31": 1}     # scheduled dwell at a through stop (the pulse)
LAYOVER = {"11": 5, "14": 6, "22": 5, "12": 6, "40": 6, "51": 5, "60": 8}  # buses wait at the terminal before leaving
RUN_MIN = {"2": 52, "4": 48, "17": 55, "3": 44, "6": 38, "9": 35, "11": 31, "14": 34, "22": 41, "12": 37, "31": 33,
           "40": 46, "51": 39, "60": 42}          # first stop to last, outbound
FREQUENCY_BASED = "11"                     # the University Connector runs from frequencies.txt between 6 a.m. and 7 p.m.
# the timetable times each transfer point's timed departures to the half minute in some periods of the day (time
# bands: 0 before 9 a.m., 1 to 3 p.m., 2 after); Arbor holds schedule times to the minute, Quinnell and the feeds to
# the second
PUB_BANDS = {"A": (0, 2), "B": (1, 2), "C": (0, 1), "D": (1, 2), "E": (0, 2)}


def pattern(base, peak=None, early=None, midday=None, late=(3, 3, 2, 2, 1)):
    s = {h: base for h in range(5, 26)}
    if peak is not None:
        for h in (7, 8, 15, 16, 17):
            s[h] = peak
    if midday is not None:
        for h in (10, 11, 12, 13):
            s[h] = midday
    if early is not None:
        s[6] = early
    s[5] = max(1, s[6] - 2)
    for h, cap in zip((19, 20, 21, 22, 23), late):
        s[h] = max(1, min(s[h], cap))
    s[24] = 0
    s[25] = 0
    return s


# scheduled weekday departures an hour from the designated stop, January timetable (hour 24 is after midnight)
SCHED = {"2": pattern(5, peak=6), "4": pattern(5, peak=6), "17": pattern(5), "3": pattern(4),
         "6": pattern(5, peak=6), "9": pattern(5), "11": pattern(6), "14": pattern(5, early=3),
         "22": pattern(5, peak=6), "12": pattern(3), "31": pattern(4), "40": pattern(5, peak=6),
         "51": pattern(5, midday=3), "60": pattern(2)}
SCHED["17"][5] = 5
for _r, _n in (("2", 2), ("17", 1), ("6", 1), ("11", 2), ("22", 1), ("31", 1), ("40", 2)):
    SCHED[_r][24] = _n                     # the late trips that leave after midnight
UNIV_EXTRA = {h: 2 for h in range(7, 16)}  # College Hill's class-day trips (service UNIV, calendar_dates only)
SATURDAY_SHARE = 0.6
SUNDAY_SHARE = 0.5
# the April timetable at the designated stops: what changed
APRIL_CHANGES = {("40", 6): 6, ("22", 19): 3, ("12", 9): 4, ("60", 15): 3}
FRIDAY_EXTRA = {("22", 15): 1, ("22", 16): 1, ("2", 24): 1}      # the April feed's Friday-only trips
CANCEL = {"2": .015, "4": .02, "17": .02, "3": .01, "6": .02, "9": .03, "11": .02, "14": .01, "22": .015,
          "12": .02, "31": .05, "40": .015, "51": .02, "60": .02}
# Riverside's afternoon runs went short of operators: the trips cancelled from 3 p.m. to 6 p.m. on weekdays
SHORT_HANDED = {"9": {15: 0.25, 16: 0.25, 17: 0.25}}


def cancel_p(route, hour, kind):
    if kind in ("WK", "FR") and hour in SHORT_HANDED.get(route, {}):
        return SHORT_HANDED[route][hour]
    return CANCEL[route]


# mean lateness at the designated stop, minutes: before 9 a.m., 9 a.m. to 3 p.m., from 3 p.m.
LATE = {"2": (4.5, 4.5, 5.0), "4": (3.5, 3.5, 4.0), "17": (8.0, 8.0, 8.5), "3": (1.0, 1.0, 1.5),
        "6": (6.0, 6.0, 6.5), "9": (1.0, 1.0, 1.5), "11": (2.0, 2.0, 2.5), "14": (1.0, 1.0, 1.5),
        "22": (2.5, 2.5, 3.0), "12": (1.0, 1.0, 1.0), "31": (1.0, 1.0, 1.5), "40": (1.5, 1.5, 2.0),
        "51": (1.2, 1.2, 1.5), "60": (1.0, 1.0, 1.0)}
LATE_SD = 3.0
REVIEW_BUS_DAYS = 400                      # bus-days Service Quality draws each month
REVIEW_TAKE = 1                            # unmatched events it reviews on each
REVIEW_PICK_SEED = 18                      # the stream for the event reviewed within each drawn bus-day
OUT_OF_SERVICE = {"A": 0.6, "B": 0.2, "C": 0.4, "D": 0.1, "E": 0.3}   # buses an hour through each stop, out of service
FILE_OVERLAP_MIN = 10                      # Quinnell's daily files repeat the previous file's last ten minutes
# average weekday boardings, January to June 2026 (the ridership report's order decides the cap)
RIDERSHIP = {"2": 6850, "4": 6120, "6": 4980, "17": 4450, "9": 3960, "22": 3710, "11": 3240, "31": 2870,
             "40": 2410, "14": 1960, "51": 1380, "3": 2210, "12": 1190, "60": 640}

# ---------------------------------------------------------------- the fleet
FLEET = ["%d" % v for v in list(range(1201, 1243)) + list(range(1601, 1631))]
ASSET = {b: "Q%05d" % (40511 + (i * 37) % 97 + 100 * (i // 97)) for i, b in enumerate(FLEET)}

# ---------------------------------------------------------------- organisations, people, files
CITY = "Larkhaven"
DEPARTMENT = "Larkhaven Transit"
STATE_DOT = "State Department of Transportation"
PROGRAM = "Frequent Transit Corridors Program"
OLD_VENDOR = "Arbor Fleetware"
NEW_VENDOR = "Quinnell Transit Systems"
PEOPLE = {"planning": "Wendy James", "its": "Eric Thomas", "quality": "Alfred Hensley"}
REVIEWERS = ["A. Hensley", "M. Boyd", "J. Collins"]   # Service Quality's analysts (Mitchell Boyd, Jeffery Collins)
TITLES = {"planning": "Manager, Service Planning and Grants, Larkhaven Transit",
          "its": "ITS Systems Administrator, Larkhaven Transit",
          "quality": "Service Quality Analyst, Larkhaven Transit"}

FILES = {
    "avl_q1": "avl_stop_events_2026q1_arbor.csv",
    "avl_q2": "avl_stop_events_2026q2_quinnell.csv",
    "review": "trip_matching_review_2026h1.csv",
    "review_memo": "service_quality_trip_matching_review_2026.pdf",
    "gtfs_jan": "larkhaven_gtfs_20260101.zip",
    "gtfs_apr": "larkhaven_gtfs_20260405.zip",
    "ridership": "ridership_by_route_2026h1.xlsx",
    "guidance": "dot_ftc_program_guidance_fy2027.pdf",
    "change_note": "quinnell_cutover_export_notes.pdf",
    "fleet": "fleet_roster_2026.csv",
    "equity": "title_vi_service_monitoring_2025.pdf",
    "farebox": "farebox_revenue_by_route_2026h1.xlsx",
    "candidates": "ftc_candidate_routes_fy2027.csv",
    "amenities": "facilities_bus_stop_amenities_20260710.csv",
    "shelter_wo": "capital_projects_shelter_work_orders.xlsx",
}
GOLDEN = {"workbook": "larkhaven_frequent_corridor_nominations_fy2027.xlsx"}
DISTRACTORS = ["equity", "farebox"]


def weekdays(a=FIRST_DAY, b=LAST_DAY):
    """The period's weekdays with the state holidays out (the program's counting days)."""
    out, d = [], a
    while d <= b:
        if d.weekday() < 5 and d not in STATE_HOLIDAYS:
            out.append(d)
        d += dt.timedelta(days=1)
    return out


def band(h):
    return 0 if h < 9 else (1 if h < 15 else 2)


def class_day(d):
    return d.weekday() < 5 and any(a <= d <= b for a, b in CLASS_DAYS) and d not in STATE_HOLIDAYS


def pub_sec(route, m):
    """Seconds past the minute of a trip's departure from its route's designated stop in the timetable (m: the
    scheduled minute after the service day's midnight)."""
    return 30 if band(m // 60) in PUB_BANDS[STOP_OF[route]] else 0


def feed(d):
    return "2604" if d >= TIMETABLE_CHANGE else "2601"


def day_type(d, operated=True):
    """The timetable a service day runs: WK, FR (April feed Fridays), SA or SU. Holidays run Sunday service; Good
    Friday runs Saturday service by the feed; the snow day ran Saturday service though the feed shows a weekday."""
    if d in STATE_HOLIDAYS or d.weekday() == 6:
        return "SU"
    if d.weekday() == 5 or d == GOOD_FRIDAY or (operated and d == SNOW_DAY):
        return "SA"
    if d.weekday() == 4 and feed(d) == "2604":
        return "FR"
    return "WK"


def sched(route, day, operated=True):
    """Scheduled departures an hour from the designated stop on a service day's timetable."""
    s = dict(SCHED[route])
    if feed(day) == "2604":
        for (r, h), v in APRIL_CHANGES.items():
            if r == route:
                s[h] = v
    kind = day_type(day, operated)
    if kind == "FR":
        for (r, h), v in FRIDAY_EXTRA.items():
            if r == route:
                s[h] = s[h] + v
    if kind in ("SA", "SU"):
        share = SATURDAY_SHARE if kind == "SA" else SUNDAY_SHARE
        s = {h: (max(1, int(round(v * share))) if v else 0) for h, v in s.items()}
    if route == "31" and class_day(day) and kind in ("WK", "FR"):
        for h, v in UNIV_EXTRA.items():
            s[h] = s[h] + v
    return s
