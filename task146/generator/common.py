"""task146 constants and helpers shared by every generator module.

A fictional English-speaking country of about 9.1 million people in eight regions. Unemployment insurance is run by
the Unemployment Insurance Board. A claims week runs Sunday to Saturday; a claim takes effect on the Sunday of the week
it is filed; its base period is the first four of the last five completed calendar quarters before the quarter of that
Sunday, and a claimant whose base-period earnings fall below the minimum is found monetarily ineligible. Every Thursday
at 08:30 the board publishes the advance count of initial claims for the claims week ended the previous Saturday;
Rothwell Bank's economics desk sends its clients a preview with its call for the next Thursday's figure."""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import io
import math

import numpy as np

SEED = 1462028

# ---------------------------------------------------------------------------------------------------- calendar
FIRST_SUNDAY = dt.date(2013, 12, 29)      # the claims week ended Saturday 4 January 2014
LEGACY_LAST_SUNDAY = dt.date(2021, 6, 20)  # the legacy claims system's last week (ended 26 June 2021)
CURRENT_FIRST_SUNDAY = dt.date(2021, 6, 27)
ASOF = dt.date(2026, 10, 8)               # Thursday: the release of the week ended 3 October, the preview written
ASOF_LAST_SUNDAY = dt.date(2026, 9, 27)   # the latest week published (ended 3 October 2026)
TARGET_SUNDAY = dt.date(2026, 10, 4)      # the call: the claims week Sunday 4 to Saturday 10 October 2026
TARGET_RELEASE = dt.date(2026, 10, 15)
SIM_LAST_SUNDAY = dt.date(2026, 10, 25)   # the world runs a few weeks past the call (truth only, never shipped)
EXTRACT_PULL = dt.date(2026, 10, 7)       # open-data and register extracts pulled on Wednesday 7 October
PROGRAM_STATS_SEPT = dt.date(2026, 10, 7)  # the September program statistics, fifth working day of October
SIC_SWITCH_SUNDAY = dt.date(2026, 1, 4)   # the board codes industry on SIC 2023 from the claims week of 4 January 2026
PORTAL_LIVE = dt.date(2026, 6, 1)         # the Employer Portal takes layoff notices from 1 June 2026


def sundays(first, last):
    out, d = [], first
    while d <= last:
        out.append(d)
        d += dt.timedelta(days=7)
    return out


SIM_SUNDAYS = sundays(FIRST_SUNDAY, SIM_LAST_SUNDAY)
PUB_SUNDAYS = sundays(FIRST_SUNDAY, ASOF_LAST_SUNDAY)


def saturday(sun):
    return sun + dt.timedelta(days=6)


def quarter_of(d):
    return (d.year, (d.month - 1) // 3 + 1)


def fiscal_year(d):
    """The board's fiscal year runs July to June: FY2026-27 is July 2026 to June 2027."""
    y = d.year if d.month >= 7 else d.year - 1
    return "FY%d-%02d" % (y, (y + 1) % 100)


def next_quarter(q):
    y, k = q
    return (y + 1, 1) if k == 4 else (y, k + 1)


def prev_quarter(q):
    y, k = q
    return (y - 1, 4) if k == 1 else (y, k - 1)


def quarter_label(q):
    return "%d Q%d" % q


# ---------------------------------------------------------------------------------------------------- time zone
def last_sunday(y, m):
    d = dt.date(y, m + 1, 1) - dt.timedelta(days=1) if m < 12 else dt.date(y, 12, 31)
    while d.weekday() != 6:
        d -= dt.timedelta(days=1)
    return d


def first_sunday(y, m):
    d = dt.date(y, m, 1)
    while d.weekday() != 6:
        d += dt.timedelta(days=1)
    return d


def utc_offset_hours(local_dt):
    """Standard time UTC+12; daylight time UTC+13 from 02:00 on the last Sunday of September to 03:00 on the first
    Sunday of April."""
    y = local_dt.year
    start = dt.datetime.combine(last_sunday(y, 9), dt.time(2, 0))
    end = dt.datetime.combine(first_sunday(y, 4), dt.time(3, 0))
    if local_dt >= start or local_dt < end:
        return 13
    return 12


def local_to_utc(local_dt):
    return local_dt - dt.timedelta(hours=utc_offset_hours(local_dt))


def utc_stamp(local_dt):
    return local_to_utc(local_dt).strftime("%Y-%m-%dT%H:%M:%SZ")


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


def nth_weekday(y, m, weekday, n):
    d = dt.date(y, m, 1)
    while d.weekday() != weekday:
        d += dt.timedelta(days=1)
    return d + dt.timedelta(days=7 * (n - 1))


def holidays(y):
    """Public holidays observed, as (date, name). Christmas, Boxing Day and the New Year days move to the following
    Monday or Tuesday when they fall at a weekend."""
    out = []

    def observe(d, name, taken):
        while d.weekday() >= 5 or d in taken:
            d += dt.timedelta(days=1)
        taken.add(d)
        out.append((d, name))

    taken = set()
    observe(dt.date(y, 1, 1), "New Year's Day", taken)
    observe(dt.date(y, 1, 2), "Day after New Year's Day", taken)
    fd = dt.date(y, 2, 6)
    out.append((fd if fd.weekday() < 5 else fd + dt.timedelta(days=7 - fd.weekday()), "Founding Day"))
    e = easter(y)
    out.append((e - dt.timedelta(days=2), "Good Friday"))
    out.append((e + dt.timedelta(days=1), "Easter Monday"))
    rd = dt.date(y, 4, 25)
    out.append((rd if rd.weekday() < 5 else rd + dt.timedelta(days=7 - rd.weekday()), "Remembrance Day"))
    out.append((nth_weekday(y, 6, 0, 1), "Sovereign's Birthday"))
    out.append((nth_weekday(y, 10, 0, 4), "Labour Day"))
    taken = set()
    observe(dt.date(y, 12, 25), "Christmas Day", taken)
    observe(dt.date(y, 12, 26), "Boxing Day", taken)
    return sorted(out)


HOLIDAYS = {}
for _y in range(2013, 2028):
    for _d, _n in holidays(_y):
        HOLIDAYS[_d] = _n


def working_days_lost(sun):
    """Public holidays falling Monday to Friday inside the claims week that starts on sun."""
    return sum(1 for k in range(1, 6) if (sun + dt.timedelta(days=k)) in HOLIDAYS)


# ---------------------------------------------------------------------------------------------------- regions
REGIONS = ["Northern", "Capital", "Eastern", "Midlands", "Western", "Southern", "Coastal", "Island"]
LEGACY_CODE = {"Northern": "NTH", "Capital": "CAP", "Eastern": "EST", "Midlands": "MID", "Western": "WST",
               "Southern": "STH", "Coastal": "CST", "Island": "ISL"}
REGION_NO = {r: i + 1 for i, r in enumerate(REGIONS)}
# each region's share of the country's initial claims, and the depth of its seasonal swing
REGION_SHARE = {"Northern": 0.138, "Capital": 0.262, "Eastern": 0.121, "Midlands": 0.168, "Western": 0.109,
                "Southern": 0.087, "Coastal": 0.072, "Island": 0.043}
REGION_AMP = {"Northern": 1.10, "Capital": 0.82, "Eastern": 1.05, "Midlands": 0.95, "Western": 1.18,
              "Southern": 1.24, "Coastal": 1.15, "Island": 1.32}
REGION_POP = {"Northern": 1203400, "Capital": 2452100, "Eastern": 1081300, "Midlands": 1544800, "Western": 997600,
              "Southern": 812500, "Coastal": 645900, "Island": 371200}


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


# ---------------------------------------------------------------------------------------------------- people
BANK = "Rothwell Bank"
BOARD = "Unemployment Insurance Board"
STATS_OFFICE = "Statistics Office"
PEOPLE = {
    "economist": "Stacey Baxter",      # senior economist, Rothwell Bank, writes the preview (the requester; not in the prompt)
    "analyst": "Tia Hewitt",          # economist on the desk, keeps the notice tracker and the desk's search pages
    "statsmgr": "Nicola Pedersen",    # the board's manager, labour market statistics (the technical notes' contact)
    "employer": "Timothy Laing",      # the board's employer services lead (the portal notice)
}
