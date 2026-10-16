"""task147 constants and helpers shared by every generator module.

The Weighhouse Hotel, 480 rooms, in the centre of Callowfort, an invented Irish city. The Callowfort Festival of Arts runs
each August from the first Friday for twenty-four days, with a preview opening night on the Thursday before. The in-house
housekeeping crew cleans up to 380 occupied rooms a day; Brennock Hospitality Staffing supplies one block of temporary
room attendants for one Monday-to-Sunday roster week of the festival season, confirmed on the Thursday five weeks before
the opening night. The property management system's reservation extract was taken at 06:12 on Thursday 1 July 2027."""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import io
import math

import numpy as np

SEED = 1472027

# ---------------------------------------------------------------------------------------------------- the hotel
CAP = 480          # rooms
CREW = 380         # occupied rooms the in-house crew can clean a day (HK-04 3.1)
HOTEL = "The Weighhouse Hotel"
HOTEL_SHORT = "Weighhouse"
CITY = "Callowfort"
FESTIVAL = "Callowfort Festival of Arts"
AGENCY = "Brennock Hospitality Staffing"
AGENCY_SHORT = "Brennock"
BAND = "Velloran"
STADIUM = "Callowfort Park"
CONVENTION = "Callowfort Convention Centre"

PEOPLE = {
    "exec_hk": "Fergus Roddy",       # executive housekeeper (the requester; not in the prompt)
    "rooms_div": "Edel McCay",       # rooms division manager, owner of HK-04
    "agency": "Naoise Meskill",      # Brennock's account manager
    "payroll": "Grainne McGuinn",    # HR and payroll administrator
}

# ---------------------------------------------------------------------------------------------------- calendar
HIST_YEARS = [2022, 2023, 2024, 2025, 2026]
YEAR = 2027
FIRST_ARRIVAL = dt.date(2022, 1, 1)       # the extract holds arrivals from 1 January 2022
SIM_FIRST_NIGHT = dt.date(2021, 12, 20)   # the world starts a little before, so early 2022 nights are full
SIM_LAST_NIGHT = dt.date(2027, 12, 31)
FEST_LEN = 24                             # Friday to the Sunday three weeks and two days later


def first_friday_aug(y):
    d = dt.date(y, 8, 1)
    while d.weekday() != 4:
        d += dt.timedelta(days=1)
    return d


def fest_open(y):
    """The festival's first full day (a Friday)."""
    return first_friday_aug(y)


def opening_night(y):
    """The preview opening night, the Thursday before the first Friday."""
    return fest_open(y) - dt.timedelta(days=1)


def confirmation_day(y):
    """HK-04 4.2: the block is confirmed on the Thursday five weeks before the festival's opening night."""
    return opening_night(y) - dt.timedelta(days=35)


def roster_weeks(y):
    """The five Monday-to-Sunday roster weeks of the festival season: the week before the opening week, the opening
    week and the three full festival weeks (2027: Monday 26 July to Sunday 29 August)."""
    f = fest_open(y)
    mon = f - dt.timedelta(days=f.weekday()) - dt.timedelta(days=7)
    return [(mon + dt.timedelta(days=7 * i), mon + dt.timedelta(days=7 * i + 6)) for i in range(5)]


def season_nights(y):
    w = roster_weeks(y)
    return [w[0][0] + dt.timedelta(days=i) for i in range((w[-1][1] - w[0][0]).days + 1)]


EXTRACT_LOCAL = dt.datetime(2027, 7, 1, 6, 12, 44)     # the PMS extract, local time
CONCERT_NIGHTS = [dt.date(2027, 8, 13), dt.date(2027, 8, 14)]
CONCERT_ANNOUNCED = dt.datetime(2027, 6, 15, 10, 0)    # local
CONCERT_ON_SALE = dt.datetime(2027, 6, 18, 9, 0)       # local


# ---------------------------------------------------------------------------------------------------- time zone
def last_sunday(y, m):
    d = dt.date(y, m + 1, 1) - dt.timedelta(days=1) if m < 12 else dt.date(y, 12, 31)
    while d.weekday() != 6:
        d -= dt.timedelta(days=1)
    return d


def utc_offset_hours(local_dt):
    """Irish Standard Time UTC+1 from 01:00 UTC on the last Sunday of March to 01:00 UTC on the last Sunday of
    October; Greenwich Mean Time otherwise."""
    y = local_dt.year
    start = dt.datetime.combine(last_sunday(y, 3), dt.time(1, 0))
    end = dt.datetime.combine(last_sunday(y, 10), dt.time(2, 0))
    return 1 if start <= local_dt < end else 0


def local_to_utc(local_dt):
    return local_dt - dt.timedelta(hours=utc_offset_hours(local_dt))


def utc_to_local(utc_dt):
    guess = utc_dt + dt.timedelta(hours=1)
    return utc_dt + dt.timedelta(hours=utc_offset_hours(guess))


EXTRACT_UTC = local_to_utc(EXTRACT_LOCAL)

# day index used by the simulation: days since 1 January 2021 (00:00 local), fractional
D0 = dt.date(2021, 1, 1)


def di(d):
    return (d - D0).days


def dd(i):
    return D0 + dt.timedelta(days=int(i))


def to_local(t):
    """A simulation time (fractional days since D0, local clock) as a local datetime."""
    return dt.datetime.combine(D0, dt.time()) + dt.timedelta(days=float(t))


def from_local(ldt):
    return (ldt - dt.datetime.combine(D0, dt.time())).total_seconds() / 86400.0


T_EXTRACT = from_local(EXTRACT_LOCAL)


# ---------------------------------------------------------------------------------------------------- holidays
def easter(y):
    a = y % 19
    b, c = divmod(y, 100)
    d, e = divmod(b, 4)
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = divmod(c, 4)
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    return dt.date(y, month, day)


def first_monday(y, m):
    d = dt.date(y, m, 1)
    while d.weekday() != 0:
        d += dt.timedelta(days=1)
    return d


def bank_holidays(y):
    """Irish public holidays as (date, name)."""
    out = [(dt.date(y, 1, 1), "New Year's Day")]
    feb = dt.date(y, 2, 1)
    if y >= 2023:
        out.append((feb if feb.weekday() == 4 else first_monday(y, 2), "St Brigid's Day"))
    out.append((dt.date(y, 3, 17), "St Patrick's Day"))
    out.append((easter(y) + dt.timedelta(days=1), "Easter Monday"))
    out.append((first_monday(y, 5), "May bank holiday"))
    out.append((first_monday(y, 6), "June bank holiday"))
    out.append((first_monday(y, 8), "August bank holiday"))
    oct_last = dt.date(y, 10, 31)
    while oct_last.weekday() != 0:
        oct_last -= dt.timedelta(days=1)
    out.append((oct_last, "October bank holiday"))
    out.append((dt.date(y, 12, 25), "Christmas Day"))
    out.append((dt.date(y, 12, 26), "St Stephen's Day"))
    return sorted(out)


HOLIDAYS = {}
for _y in range(2021, 2029):
    for _d, _n in bank_holidays(_y):
        HOLIDAYS[_d] = _n


# ---------------------------------------------------------------------------------------------------- helpers
def rng(*keys):
    """An independent numpy stream per name: blake2b of the seed and the keys (hash() is salted per process)."""
    h = hashlib.blake2b(("%d|" % SEED + "|".join(str(k) for k in keys)).encode(), digest_size=8).digest()
    return np.random.default_rng(int.from_bytes(h, "big"))


def write_csv(path, cols, rows, crlf=False, delimiter=","):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\r\n" if crlf else "\n", delimiter=delimiter)
    w.writerow(cols)
    n = 0
    for r in rows:
        w.writerow(["" if r.get(c) is None else r.get(c) for c in cols] if isinstance(r, dict) else r)
        n += 1
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(buf.getvalue())
    return n


def round_to(x, step):
    """Round half away from zero to a multiple of step (the deliverables' convention)."""
    q = x / step
    return int(math.floor(q + 0.5)) * step if q >= 0 else -int(math.floor(-q + 0.5)) * step


def round_dp(x, dp):
    f = 10 ** dp
    return math.floor(x * f + 0.5) / f if x >= 0 else -math.floor(-x * f + 0.5) / f


def bin_clearance(x, step):
    """Distance from x to the nearest rounding edge of its step-wide bin, as a share of the step (0.5 is mid-bin)."""
    q = x / step
    return 0.5 - abs(q - math.floor(q + 0.5))
