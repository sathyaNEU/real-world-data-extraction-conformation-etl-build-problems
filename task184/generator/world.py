"""The fixed world of task184: Kestland Aviation Security, its eight airports' central checkpoints, the mobile
screening unit, last summer's postings and the summer 2027 planning inputs. Every other module reads its constants
from here."""
import datetime as dt

SEED = 184
AGENCY = "Kestland Aviation Security"
AGENCY_SHORT = "KAS"
AS_OF = dt.date(2027, 4, 23)            # the planning extract the head of screening operations works from
MEMO_DATE = dt.date(2027, 4, 30)

# operations code, name, finance cost centre
AIRPORTS = [
    ("CUL", "Cullinvale", "CC-4102"),
    ("ARD", "Ardcarrig", "CC-4101"),
    ("FAR", "Faranloe", "CC-4106"),
    ("HAL", "Halloran Bay", "CC-4108"),
    ("ESK", "Eskerford", "CC-4105"),
    ("BRN", "Brennagh", "CC-4103"),
    ("DRM", "Dromkeel", "CC-4104"),
    ("GLK", "Glenkessan", "CC-4107"),
]
CODES = [a[0] for a in AIRPORTS]
NAME = {a[0]: a[1] for a in AIRPORTS}
CC = {a[0]: a[2] for a in AIRPORTS}

# the day is 72 intervals of 15 minutes from 04:00 to 22:00
T = 72
OPEN_H, CLOSE_H = 4, 22
LANE_RATE = 37.5                 # passengers per lane per 15 minutes (150 an hour), planning standard 2026
LANE_RATE_2023 = 35.0            # the superseded edition's rate (140 an hour)
STANDARD_MIN = 20.0
TEAM_LANES = 3
TEAM_FROM, TEAM_TO = 5, 21       # the unit's lanes screen from 05:00 to 21:00
STAFF_LANES = 2                  # staff and aircrew search at shift changes, before 05:00 and after 21:00

# each checkpoint: permanent lanes, the lanes rostered outside the banks, and the two banks of departures
# (plateau start and end, local hours); the roster plan staffs every lane from 45 minutes before a bank to an hour
# after it, and the off-peak lanes otherwise. The same summer roster pattern ran in 2026 and is issued for 2027.
CHECKPOINT = {
    #       lanes, off-peak, morning bank, evening bank
    "CUL": (9, 7, (5.50, 7.75), (16.50, 18.50)),
    "ARD": (8, 6, (5.75, 7.75), (16.75, 18.50)),
    "FAR": (8, 6, (5.75, 7.75), (16.75, 18.25)),
    "HAL": (5, 5, (6.00, 7.75), (16.75, 18.25)),
    "ESK": (7, 5, (6.00, 7.50), (17.00, 18.50)),
    "BRN": (6, 5, (6.00, 7.50), (17.00, 18.25)),
    "DRM": (6, 5, (5.75, 7.25), (16.50, 18.00)),
    "GLK": (5, 4, (6.00, 7.50), (17.00, 18.25)),
}
LANES = {c: v[0] for c, v in CHECKPOINT.items()}

# demand: the off-peak flow per 15 minutes and each bank's peak in lanes' worth above the permanent lanes
# (morning, evening). 2027 is the planning sheet's July design day; 2026 is last summer's typical July day.
DEMAND27 = {
    "CUL": (150, 3.15, 2.95), "ARD": (130, 2.95, 2.75), "FAR": (120, 2.85, 2.65), "HAL": (84, 2.40, 2.30),
    "ESK": (105, 2.65, 2.45), "BRN": (90, 2.45, 2.25), "DRM": (80, 2.30, 2.10), "GLK": (75, 2.20, 2.00),
}
DEMAND26 = {
    "CUL": (140, 1.35, 1.25), "ARD": (125, 1.28, 1.18), "FAR": (115, 1.23, 1.13), "HAL": (70, 0.55, 0.50),
    "ESK": (101, 1.13, 1.03), "BRN": (85, 1.08, 0.98), "DRM": (110, 1.00, 0.90), "GLK": (72, 0.95, 0.85),
}

# summer 2027 posting periods and the planning sheet's scale on the July design day
PERIODS = [("late June", dt.date(2027, 6, 15), dt.date(2027, 6, 30)),
           ("July", dt.date(2027, 7, 1), dt.date(2027, 7, 31)),
           ("August", dt.date(2027, 8, 1), dt.date(2027, 8, 31))]
PERIOD_SCALE = {"late June": 0.95, "July": 1.0, "August": 1.02}
DAYS = {n: (d1 - d0).days + 1 for n, d0, d1 in PERIODS}

# last summer: 15 June to 31 August 2026; the unit posted Monday to Sunday, eleven weeks from 15 June
SUMMER26 = (dt.date(2026, 6, 15), dt.date(2026, 8, 31))
POSTINGS_2026 = ["CUL", "DRM", "ARD", "HAL", "FAR", "ESK", "CUL", "BRN", "GLK", "ARD", "ARD"]

# What a checkpoint opens is not its roster pattern. The lanes the pattern staffs for a bank are covered by an
# overtime block shorter than the pattern: for each checkpoint, that many of its bank lanes stay closed from 45
# minutes before the plateau until the stated hours into it, and from that long before the plateau's end to the end
# of the pattern's shoulder. It runs that way every day of the summer, whether or not the unit is there.
#          lanes closed, hours into the plateau
SHORT = {
    "CUL": (1, 0.25),
    "ARD": (1, 0.50),
    "FAR": (1, 0.25),
    "HAL": (0, 0.00),
    "ESK": (2, 0.00),
    "BRN": (1, 0.50),
    "DRM": (1, 0.50),
    "GLK": (1, 0.25),
}

# how each host's duty managers used the unit's week: lanes of their own stood down while the unit screened, through
# the morning bank, through the evening bank, through the quiet middle of the day, and in the last 45 minutes.
#            morning bank, evening bank, quiet middle, last 45 minutes
RELEASE = {
    "CUL": (2, 2, 3, 3),
    "ARD": (2, 2, 3, 3),
    "FAR": (2, 2, 3, 3),
    "HAL": (1, 2, 2, 3),
    "ESK": (1, 2, 2, 2),
    "BRN": (2, 2, 2, 2),
    "DRM": (2, 2, 2, 2),
    "GLK": (2, 2, 2, 2),
}

PEOPLE = {
    "head": ("Ruairi Barnett", "Head of Screening Operations"),
    "analyst": ("Alana Marnan", "Capacity Planning Analyst"),
    "team": ("Fergus Rynne", "Mobile Unit Team Leader"),
    "standard": ("Leon O'Boyle", "Standards and Planning Manager"),
}


def hour_of(i):
    return OPEN_H + i / 4.0


def clock(i):
    m = OPEN_H * 60 + 15 * i
    return "%02d:%02d" % (m // 60, m % 60)


def week_of(d):
    """The 2026 posting week (0 to 10) a date falls in, or None on 31 August."""
    k = (d - SUMMER26[0]).days // 7
    return k if 0 <= k < len(POSTINGS_2026) else None


def host_on(d):
    k = week_of(d)
    return POSTINGS_2026[k] if k is not None else None


def summer26_days():
    d, out = SUMMER26[0], []
    while d <= SUMMER26[1]:
        out.append(d)
        d += dt.timedelta(days=1)
    return out
