"""Elkhorn County, Washington: the fixed world the generator draws from (calendars, map, staff, parameters)."""
import datetime as dt
import math

import numpy as np

SEED = 1302027
START = dt.date(2015, 1, 1)          # the simulated history begins here (the districts have stood since 2012)
RECORD = dt.date(2019, 1, 1)         # the legacy export begins here
CUTOVER = dt.date(2024, 3, 4)        # the replacement inspection system went live (legacy export ends 1 March)
END = dt.date(2026, 12, 31)
PULL = dt.datetime(2027, 1, 8, 9, 40)   # the extracts were pulled on 8 January 2027 (local)
PLAN_DATE = dt.date(2027, 1, 11)
PAPER_END = dt.date(2026, 8, 31)     # return officers on paper day sheets until this date, tablets from 1 September
RETURN_TEAM = dt.date(2022, 2, 1)    # return inspections moved from the district inspectors to a return team
THRESHOLD = 540                      # the plan's staffing rule: a third return officer above this (2 x 270)
FEE_OLD, FEE_NEW, FEE_CHANGE = 152, 168, dt.date(2026, 7, 1)

COUNTY = "Elkhorn County"
DEPT = "Elkhorn County Public Health"
DIVISION = "Environmental Health Division"
SEAT = "Marlow"

# ---------------------------------------------------------------- the familiarity truth (never shipped)
F0, F1 = 1.85, 0.80          # first visit by this inspector to this permit, second visit; third on: nothing
GAMMA_SD = 0.12              # inspectors' own criteria, a modest spread
THETA_SD = 0.50              # establishments within a risk category
BASE = {1: 0.0214, 2: 0.0403, 3: 0.0706}    # unsatisfactory share of a familiar visit by an average inspector
REOPEN_2021 = 0.30           # the first half of 2021, kitchens reopening after the 2020 closures
COVID_STOP = (dt.date(2020, 3, 23), dt.date(2020, 6, 26))   # routine inspections suspended


def lg(p):
    return math.log(p / (1 - p))


def expit(x):
    return 1.0 / (1.0 + math.exp(-x))


# ---------------------------------------------------------------- calendars
def _nth_weekday(y, m, wd, n):
    d = dt.date(y, m, 1)
    d += dt.timedelta(days=(wd - d.weekday()) % 7)
    return d + dt.timedelta(weeks=n - 1)


def _last_weekday(y, m, wd):
    d = dt.date(y, m + 1, 1) - dt.timedelta(days=1) if m < 12 else dt.date(y, 12, 31)
    return d - dt.timedelta(days=(d.weekday() - wd) % 7)


def _observed(d):
    if d.weekday() == 5:
        return d - dt.timedelta(days=1)
    if d.weekday() == 6:
        return d + dt.timedelta(days=1)
    return d


def holidays(y):
    """Elkhorn County's observed holidays for year y, name by date."""
    h = {
        _observed(dt.date(y, 1, 1)): "New Year's Day",
        _nth_weekday(y, 1, 0, 3): "Martin Luther King Jr. Day",
        _nth_weekday(y, 2, 0, 3): "Presidents' Day",
        _last_weekday(y, 5, 0): "Memorial Day",
        _observed(dt.date(y, 7, 4)): "Independence Day",
        _nth_weekday(y, 9, 0, 1): "Labor Day",
        _observed(dt.date(y, 11, 11)): "Veterans Day",
        _nth_weekday(y, 11, 3, 4): "Thanksgiving Day",
        _nth_weekday(y, 11, 3, 4) + dt.timedelta(days=1): "Day after Thanksgiving",
        _observed(dt.date(y, 12, 25)): "Christmas Day",
    }
    if y >= 2022:
        h[_observed(dt.date(y, 6, 19))] = "Juneteenth"
    return h


HOLIDAYS = {}
for _y in range(2014, 2028):
    HOLIDAYS.update(holidays(_y))


def working(d):
    return d.weekday() < 5 and d not in HOLIDAYS


def add_working(d, n):
    while n > 0:
        d += dt.timedelta(days=1)
        if working(d):
            n -= 1
    return d


def working_between(a, b):
    """County working days after a up to and including b."""
    n, d = 0, a
    while d < b:
        d += dt.timedelta(days=1)
        if working(d):
            n += 1
    return n


def dst(day_local):
    """Pacific daylight time in force on this local date (second Sunday of March to first Sunday of November)."""
    y = day_local.year
    return _nth_weekday(y, 3, 6, 2) <= day_local < _nth_weekday(y, 11, 6, 1)


def to_utc(t_local):
    return t_local + dt.timedelta(hours=7 if dst(t_local.date()) else 8)


# ---------------------------------------------------------------- the county map (km)
TOWNS = [  # name, x, y, weight, spread
    ("Marlow", 31.0, 22.0, 0.44, 4.2),
    ("Kessing", 12.0, 33.0, 0.10, 2.4),
    ("Ardell", 47.0, 35.0, 0.09, 2.3),
    ("Wexby", 50.0, 10.0, 0.08, 2.1),
    ("Norrow", 18.0, 9.0, 0.07, 2.0),
    ("Callan", 7.0, 18.0, 0.05, 1.8),
    ("Torvik", 39.0, 41.0, 0.05, 1.7),
    ("Elsby", 56.0, 24.0, 0.04, 1.6),
    (None, 30.0, 22.0, 0.08, 16.0),        # rural roadside, farm stands, the lake resorts
]
ZIP = {"Marlow": ("98362", "98363", "98365"), "Kessing": ("98371",), "Ardell": ("98374",), "Wexby": ("98381",),
       "Norrow": ("98384",), "Callan": ("98388",), "Torvik": ("98391",), "Elsby": ("98395",), None: ("98397",)}

# the eleven 2026 districts (drawn in 2012) and the nine of 2027, as seeds of a nearest-seed map
SEEDS_2026 = {1: (27.5, 25.5), 2: (34.5, 25.5), 3: (27.5, 18.5), 4: (34.5, 18.5), 5: (12.0, 32.0),
              6: (46.0, 34.0), 7: (49.0, 12.0), 8: (17.0, 10.0), 9: (8.0, 19.0), 10: (40.0, 41.0),
              11: (56.0, 23.0)}
SEEDS_2027 = {"A": (25.5, 21.0), "B": (35.5, 22.5), "C": (31.0, 15.5), "D": (14.0, 29.0), "E": (45.0, 37.5),
              "F": (50.0, 13.5), "G": (14.0, 12.0), "H": (31.0, 30.5), "J": (52.5, 29.0)}
DISTRICT_2027_NAME = {"A": "Marlow West", "B": "Marlow East", "C": "Marlow South and Harborview",
                      "D": "Kessing and the North Valley", "E": "Ardell and Torvik", "F": "Wexby and the South Shore",
                      "G": "Norrow and Callan", "H": "Marlow North and Lake Road", "J": "Elsby and the East Hills"}


def nearest(seeds, x, y):
    return min(seeds, key=lambda k: (seeds[k][0] - x) ** 2 + (seeds[k][1] - y) ** 2)


# ---------------------------------------------------------------- staff
# name, middle initial, employee number, role, hire date, separation date, district held (from, to, district)
STAFF = [
    ("Mariah", "J", "Ramirez", "E31876", "Environmental Health Specialist II", dt.date(2006, 9, 11), None, [(None, None, 1)]),
    ("Erik", "T", "Mayer", "E20419", "Environmental Health Specialist III", dt.date(1997, 6, 2), dt.date(2026, 12, 31), [(None, None, 2)]),
    ("Tina", "L", "Rivera", "E44102", "Environmental Health Specialist I", dt.date(2020, 11, 16), None, [(dt.date(2021, 2, 1), None, 3)]),
    ("Andrew", "P", "Mason", "E27733", "Environmental Health Specialist III", dt.date(1996, 3, 18), dt.date(2026, 12, 31), [(None, None, 4)]),
    ("Timothy", "R", "Collins", "E46590", "Environmental Health Specialist I", dt.date(2023, 2, 13), None, [(dt.date(2023, 5, 1), None, 5)]),
    ("Luis", "A", "Saunders", "E35248", "Environmental Health Specialist II", dt.date(2009, 1, 5), None, [(None, None, 6)]),
    ("Kimberly", "D", "Mata", "E41957", "Environmental Health Specialist II", dt.date(2018, 12, 3), None, [(dt.date(2019, 3, 4), None, 7)]),
    ("Jacob", "W", "Curtis", "E33061", "Environmental Health Specialist II", dt.date(2007, 8, 20), None, [(None, None, 8)]),
    ("Angela", "M", "Gonzalez", "E38814", "Environmental Health Specialist II", dt.date(2011, 4, 4), None, [(None, None, 9)]),
    ("Nicole", "S", "Charles", "E22685", "Environmental Health Specialist II", dt.date(2008, 10, 20), None, [(None, None, 10)]),
    ("Jason", "E", "Weaver", "E36297", "Environmental Health Specialist II", dt.date(2013, 2, 25), None, [(None, None, 11)]),
    ("George", "H", "Dixon", "E19034", "Environmental Health Specialist III", dt.date(1990, 5, 7), dt.date(2019, 2, 28), [(None, dt.date(2019, 3, 3), 7)]),
    ("Brandon", "K", "Lloyd", "E21160", "Environmental Health Specialist III", dt.date(1994, 9, 12), dt.date(2021, 1, 29), [(None, dt.date(2021, 1, 31), 3)]),
    ("Paul", "F", "Russell", "E23378", "Environmental Health Specialist III", dt.date(1999, 1, 11), dt.date(2023, 4, 28), [(None, dt.date(2023, 4, 30), 5)]),
    ("Benjamin", "O", "Flores", "E45071", "Return Inspection Officer", dt.date(2022, 1, 10), None, []),
    ("Diane", "C", "Diaz", "E44836", "Return Inspection Officer", dt.date(2021, 12, 6), None, []),
    ("Lisa", "N", "Clarke", "E39420", "Plan Review Specialist", dt.date(2016, 7, 18), None, []),
    ("Sara", "B", "Hughes", "E42213", "Program Assistant", dt.date(2019, 10, 7), None, []),
    ("Valerie", "G", "Wood", "E30552", "Food Safety Program Manager", dt.date(2005, 2, 14), None, []),
    ("Teresa", "M", "Hansen", "E24917", "Environmental Health Director", dt.date(2001, 11, 5), None, []),
]
RETURN_OFFICER = {"north": "E45071", "south": "E44836"}     # Flores the north districts 1, 2, 3, 5, 10; Diaz the rest
NORTH = {1, 2, 3, 5, 10}
RETIRING_2026 = (2, 4)               # Erik Mayer and Andrew Mason retire on 31 December 2026
PLAN_REVIEWER = "E39420"
CLERK = "E42213"

# 2027: the nine districts and the inspector named for each (Appendix A of the plan)
INSPECTOR_2027 = {"A": "E31876", "B": "E27733", "C": "E33061", "D": "E44102", "E": "E35248", "F": "E41957",
                  "G": "E38814", "H": "E46590", "J": "E36297"}


def initials(emp):
    for s in STAFF:
        if s[3] == emp:
            return s[0][0] + s[1] + s[2][0]
    raise KeyError(emp)


def full_name(emp):
    for s in STAFF:
        if s[3] == emp:
            return "%s %s" % (s[0], s[2])
    raise KeyError(emp)


def district_holder(d, day):
    """The employee number holding district d on this day."""
    for s in STAFF:
        for a, b, dd in s[7]:
            if dd == d and (a is None or a <= day) and (b is None or day <= b):
                return s[3]
    raise KeyError((d, day))


def covering_order(d):
    """The districts whose inspectors cover district d on leave days, nearest first."""
    sx, sy = SEEDS_2026[d]
    return sorted((k for k in SEEDS_2026 if k != d),
                  key=lambda k: (SEEDS_2026[k][0] - sx) ** 2 + (SEEDS_2026[k][1] - sy) ** 2)[:4]


COVER_WEIGHTS = (0.4, 0.3, 0.2, 0.1)


def rng(*keys):
    """One independent stream per purpose, so a change to one record set never moves another."""
    h = SEED
    for k in keys:
        for ch in str(k):
            h = (h * 1000003 + ord(ch)) % (2 ** 61 - 1)
    return np.random.default_rng(h)
