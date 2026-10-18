"""task173 constants and helpers shared by every generator module.

Ashdale Software Inc., Waterloo, Ontario, sells the Ashdale Tax return software and runs Ashdale Tax Live, a tier
in which customers preparing their return can talk to a seasonal tax expert by video, chat or phone. The English
expert queue is staffed by seasonal experts who work remotely on Eastern time; a French queue is staffed from
Montreal and planned on its own. For the deadline fortnight the company books extra agent hours from Hillsborough
Contact Services, a contact-centre outsourcer in Moncton, New Brunswick.

The 2027 filing season (tax year 2026) is planned in October 2026. Every file was pulled for the expert-service
leadership meeting of Monday 2 November 2026 on Friday 30 October 2026.

The seed was fixed by rule before any data was generated: the task number, then the as-of month and day
(30 October)."""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import io
import json
import math

import numpy as np

SEED = 1731030

COMPANY = "Ashdale Software Inc."
PRODUCT = "Ashdale Tax"
SERVICE = "Ashdale Tax Live"
VENDOR = "Hillsborough Contact Services"
VENDOR_SHORT = "HCS"

# drawn with guard.py names --geo Canada --seed 173
PEOPLE = {
    "wfm": "Kimberly Ball",          # workforce planning manager, the requester (in no file the prompt names)
    "vp": "Mario Barnett",           # vice-president, expert services: the booking goes to his leadership meeting
    "training": "Michelle Russell",  # training centre lead: the class calendar
    "demand": "Adam Rojas",          # demand planning analyst: the demand plan
    "vendor": "Tammy Gibson",        # the vendor's account manager
    "crm": "James Richards",         # CRM administrator: the interaction export and its notes
    "finance": "Corey Hughes",       # finance partner
}

UTC = dt.timezone.utc

# ------------------------------------------------------------------------------------------------- calendar
AS_OF = dt.date(2026, 10, 30)            # Friday: every file pulled
MEETING = dt.date(2026, 11, 2)           # Monday: the expert-service leadership meeting
RECALL_CUTOFF = dt.date(2026, 10, 23)    # recall responses counted to 23:59 Eastern
SEASONS_OLD = [2021, 2022, 2023, 2024, 2025]
SEASON_CRM = 2026
SEASON_PLAN = 2027


def deadline(y):
    """The filing deadline for most individuals: 30 April, or the next business day when 30 April is a weekend."""
    d = dt.date(y, 4, 30)
    while d.weekday() >= 5:
        d += dt.timedelta(1)
    return d


def fortnight(y):
    """The deadline fortnight: the 14 days that end on the first Sunday after the filing deadline."""
    d = deadline(y) + dt.timedelta(1)
    while d.weekday() != 6:
        d += dt.timedelta(1)
    return d - dt.timedelta(13), d


def second_monday_january(y):
    d = dt.date(y, 1, 1)
    while d.weekday() != 0:
        d += dt.timedelta(1)
    return d + dt.timedelta(7)


def season_open(y):
    return second_monday_january(y)


def season_close(y):
    return dt.date(y, 5, 31)


def netfile_ramp(y):
    """The fourth Monday of February, when filing volumes take off (NETFILE opens about then)."""
    d = dt.date(y, 2, 1)
    while d.weekday() != 0:
        d += dt.timedelta(1)
    return d + dt.timedelta(21)


ON_HOLIDAYS = {
    dt.date(2021, 2, 15), dt.date(2021, 4, 2), dt.date(2021, 5, 24),
    dt.date(2022, 2, 21), dt.date(2022, 4, 15), dt.date(2022, 5, 23),
    dt.date(2023, 2, 20), dt.date(2023, 4, 7), dt.date(2023, 5, 22),
    dt.date(2024, 2, 19), dt.date(2024, 3, 29), dt.date(2024, 5, 20),
    dt.date(2025, 2, 17), dt.date(2025, 4, 18), dt.date(2025, 5, 19),
    dt.date(2026, 2, 16), dt.date(2026, 4, 3), dt.date(2026, 5, 18),
    dt.date(2027, 2, 15), dt.date(2027, 3, 26), dt.date(2027, 5, 24),
}

# ------------------------------------------------------------------------------------------------- the standard
SCHEDULE_HOURS = 90.0        # each in-house expert's deadline schedule in the fortnight (45 hours a week)
SHRINKAGE = 0.12             # breaks, coaching, meetings and system time
OCCUPANCY = 0.85             # the share of available time the queue is planned to keep busy
HANDLE_PER_EXPERT = SCHEDULE_HOURS * (1 - SHRINKAGE) * OCCUPANCY      # 67.32 handle hours per expert
HANDLE_PER_BILLED = OCCUPANCY                                          # handle hours per billed vendor hour
ORDER_BLOCK = 1000           # the vendor takes deadline-fortnight orders in whole blocks of 1,000 agent hours
RETURNING_2027 = 150
CLASS_SEATS = 60
GROWTH_2027 = 0.034          # the demand plan's growth on the 2026 fortnight (finance's Live-tier forecast)

# ------------------------------------------------------------------------------------------------- clocks
def _nth_sunday(y, m, n):
    d = dt.date(y, m, 1)
    while d.weekday() != 6:
        d += dt.timedelta(1)
    return d + dt.timedelta(7 * (n - 1))


def dst_window_utc(y, std_offset):
    """Canadian DST: from 02:00 local on the second Sunday of March to 02:00 local on the first Sunday of
    November. std_offset is the zone's standard offset from UTC in hours (Eastern -5, Atlantic -4)."""
    start = dt.datetime.combine(_nth_sunday(y, 3, 2), dt.time(2, 0)) - dt.timedelta(hours=std_offset)
    end = dt.datetime.combine(_nth_sunday(y, 11, 1), dt.time(2, 0)) - dt.timedelta(hours=std_offset + 1)
    return start, end


def offset(t_utc, std_offset):
    s, e = dst_window_utc(t_utc.year, std_offset)
    return std_offset + 1 if s <= t_utc < e else std_offset


def to_utc(t_local, std_offset=-5):
    for off in (std_offset + 1, std_offset):
        u = t_local - dt.timedelta(hours=off)
        if offset(u, std_offset) == off:
            return u
    return t_local - dt.timedelta(hours=std_offset)


def from_utc(t_utc, std_offset=-5):
    return t_utc + dt.timedelta(hours=offset(t_utc, std_offset))


def eastern(t_utc):
    return from_utc(t_utc, -5)


def atlantic(t_utc):
    return from_utc(t_utc, -4)


def monday(d):
    return d - dt.timedelta(days=d.weekday())


def iso_z(t):
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


# ------------------------------------------------------------------------------------------------- randomness
def rng(*keys):
    """An independent numpy stream per name: blake2b of the seed and the keys (hash() is salted per process)."""
    h = hashlib.blake2b(("%d|" % SEED + "|".join(str(k) for k in keys)).encode(), digest_size=8).digest()
    return np.random.default_rng(int.from_bytes(h, "big"))


def token(*keys, n=12, alphabet="0123456789abcdef"):
    h = hashlib.blake2b(("%d|" % SEED + "|".join(str(k) for k in keys)).encode(), digest_size=32).digest()
    return "".join(alphabet[b % len(alphabet)] for b in h[:n])


# ------------------------------------------------------------------------------------------------- writing
def write_csv(path, cols, rows, crlf=False):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\r\n" if crlf else "\n")
    w.writerow(cols)
    n = 0
    for r in rows:
        w.writerow(["" if r.get(c) is None else r.get(c) for c in cols] if isinstance(r, dict) else r)
        n += 1
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(buf.getvalue())
    return n


def read_csv(path):
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def write_json(path, obj, indent=None):
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(obj, fh, ensure_ascii=False, indent=indent, separators=(",", ":") if indent is None else (",", ": "))
        fh.write("\n")


def round_half_up(x, nd=0):
    q = x * 10 ** nd
    return math.floor(q + 0.5) / 10 ** nd


def ceil_to(x, step):
    return int(math.ceil(x / step - 1e-12) * step)


def ceil_edge_share(x, step):
    """For a value rounded up to whole steps: the distance to the nearer step boundary, as a share of the step."""
    f = x / step - math.floor(x / step)
    return min(f, 1 - f)


def edge_share(x, step):
    """For a value rounded to the nearest step: the distance to the nearer edge of its cell, as a share of the step
    (0.5 is the centre)."""
    q = x / step
    return 0.5 - abs(q - math.floor(q + 0.5))


MONTH = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
         "November", "December"]
WEEKDAY = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def long_date(d):
    return "%s %d %s %d" % (WEEKDAY[d.weekday()], d.day, MONTH[d.month], d.year)


def short_date(d):
    return "%d %s %d" % (d.day, MONTH[d.month], d.year)
