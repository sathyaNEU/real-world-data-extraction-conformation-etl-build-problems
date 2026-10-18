"""task162 constants and helpers shared by every generator module.

Usva Software Oy, Tampere, makes the Usva desktop browser (Windows, macOS, Linux) and runs a bug-triage team for the
reports its users file through the browser's report form. The team's records begin on 1 October 2025, when the team
was set up and the migration to the new tracker scoped its history. The old tracker is retired at 00:00 on Monday
4 January 2027 (Helsinki); a four-week parallel run on both trackers ran from Monday 2 November to Sunday 29 November
2026. Every file was pulled for the first-quarter staffing plan on Friday 18 December 2026.

The seed was fixed by rule before any data was generated: the task number, then the as-of month and day (17 December,
the last day the export holds)."""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import io
import json
import math

import numpy as np

SEED = 1621217

VENDOR = "Usva Software Oy"
BROWSER = "Usva"
PEOPLE = {
    "director": "Juhani Immonen",     # director of engineering: the staffing request (thread)
    "lead": "Ulla Kauppinen",         # triage team lead: the requester (in no file the prompt names)
    "release": "Timo Huttunen",       # release management: the release calendar
    "migration": "Ritva Grönroos",    # tracker migration lead: runbook, parallel-run report, bridge notes; the bridge ran under her account
    "data": "Simo Kinnunen",          # data team: the public data portal series
    "security": "Helena Pakarinen",   # security team: restricted reports
}
TRIAGERS = ["Linnea Kärki", "Johannes Laukkanen", "Saara Väisänen", "Tapio Kallio", "Arja Turunen", "Sakari Puhakka"]
WEBCOMPAT = ["Milla Ojanen", "Antero Järvinen"]

UTC = dt.timezone.utc

# ------------------------------------------------------------------------------------------------- calendar
RECORD_START = dt.date(2025, 10, 1)      # Wednesday: the team's records and the migration's history scope begin
SIM_START = dt.date(2025, 6, 1)          # adoption state warms up before the record
AS_OF = dt.date(2026, 12, 17)            # Thursday: the last day the exports hold
PULL = dt.datetime(2026, 12, 18, 6, 40)  # Friday 06:40 Helsinki: every file pulled for the plan
SIM_END = dt.date(2027, 4, 30)           # truth only, never shipped
RUN_START = dt.date(2026, 11, 2)         # Monday: the parallel run
RUN_END = dt.date(2026, 11, 29)          # Sunday
RUN_EXPORT = dt.datetime(2026, 12, 4, 10, 20)   # Helsinki: the migration team's export of the run
CUTOVER = dt.date(2027, 1, 4)            # Monday 00:00 Helsinki: the new tracker becomes the system of record
Q1_WEEKS = [dt.date(2027, 1, 4) + dt.timedelta(days=7 * k) for k in range(13)]   # Mondays, 4 January to 29 March
STAFF_STD = 120                          # triage items per triager-week

# the release train: (major, release date); dot releases follow
RELEASES = [(31, dt.date(2025, 7, 15)), (32, dt.date(2025, 8, 12)), (33, dt.date(2025, 9, 9)), (34, dt.date(2025, 10, 7)),
            (35, dt.date(2025, 11, 4)), (36, dt.date(2025, 12, 2)), (37, dt.date(2026, 1, 6)), (38, dt.date(2026, 2, 3)),
            (39, dt.date(2026, 3, 3)), (40, dt.date(2026, 4, 7)), (41, dt.date(2026, 5, 5)), (42, dt.date(2026, 6, 2)),
            (43, dt.date(2026, 7, 7)), (44, dt.date(2026, 8, 4)), (45, dt.date(2026, 9, 1)), (46, dt.date(2026, 9, 29)),
            (47, dt.date(2026, 10, 27)), (48, dt.date(2026, 12, 1)), (49, dt.date(2027, 1, 12)), (50, dt.date(2027, 2, 9)),
            (51, dt.date(2027, 3, 9)), (52, dt.date(2027, 4, 6))]
MAJOR_DATE = dict(RELEASES)
# dot releases (x.0.1, some x.0.2): Tuesday or Thursday a week or two after the release
DOTS = {31: [(1, dt.date(2025, 7, 24))], 32: [(1, dt.date(2025, 8, 21))], 33: [(1, dt.date(2025, 9, 18))],
        34: [(1, dt.date(2025, 10, 16)), (2, dt.date(2025, 10, 28))], 35: [(1, dt.date(2025, 11, 13))],
        36: [(1, dt.date(2025, 12, 11))], 37: [(1, dt.date(2026, 1, 15))], 38: [(1, dt.date(2026, 2, 12)), (2, dt.date(2026, 2, 24))],
        39: [(1, dt.date(2026, 3, 12))], 40: [(1, dt.date(2026, 4, 16))], 41: [(1, dt.date(2026, 5, 14))],
        42: [(1, dt.date(2026, 6, 11))], 43: [(1, dt.date(2026, 7, 16))], 44: [(1, dt.date(2026, 8, 13))],
        45: [(1, dt.date(2026, 9, 10)), (2, dt.date(2026, 9, 22))], 46: [(1, dt.date(2026, 10, 8))],
        47: [(1, dt.date(2026, 11, 5))], 48: [(1, dt.date(2026, 12, 10))],
        49: [(1, dt.date(2027, 1, 21))], 50: [(1, dt.date(2027, 2, 18))], 51: [(1, dt.date(2027, 3, 18))], 52: []}
RELEASE_HOUR = 16                         # releases and dot releases go out at 16:00 Helsinki


def second_tuesday(y, m):
    d = dt.date(y, m, 1)
    while d.weekday() != 1:
        d += dt.timedelta(1)
    return d + dt.timedelta(7)


PATCH_TUESDAYS = sorted(second_tuesday(y, m) for y in range(2025, 2028) for m in range(1, 13))

FI_HOLIDAYS = {dt.date(2025, 12, 6), dt.date(2025, 12, 24), dt.date(2025, 12, 25), dt.date(2025, 12, 26),
               dt.date(2026, 1, 1), dt.date(2026, 1, 6), dt.date(2026, 4, 3), dt.date(2026, 4, 6), dt.date(2026, 5, 1),
               dt.date(2026, 5, 14), dt.date(2026, 6, 19), dt.date(2026, 12, 24), dt.date(2026, 12, 25),
               dt.date(2026, 12, 31), dt.date(2027, 1, 1), dt.date(2027, 1, 6), dt.date(2027, 3, 26), dt.date(2027, 3, 29)}


def year_end(d):
    """The year-end lull every browser vendor sees: 21 December to 3 January."""
    return (d.month == 12 and d.day >= 21) or (d.month == 1 and d.day <= 3)


def easter(d):
    return dt.date(2026, 4, 2) <= d <= dt.date(2026, 4, 6) or dt.date(2027, 3, 25) <= d <= dt.date(2027, 3, 29)


# ------------------------------------------------------------------------------------------------- clocks
def _last_sunday(y, m):
    d = dt.date(y, m + 1, 1) - dt.timedelta(days=1) if m < 12 else dt.date(y, 12, 31)
    while d.weekday() != 6:
        d -= dt.timedelta(days=1)
    return d


def helsinki_offset_utc(t_utc):
    """Hours Helsinki is ahead of UTC at UTC time t (EU rules: EEST from 01:00 UTC on the last Sunday of March to 01:00
    UTC on the last Sunday of October)."""
    y = t_utc.year
    start = dt.datetime.combine(_last_sunday(y, 3), dt.time(1, 0))
    end = dt.datetime.combine(_last_sunday(y, 10), dt.time(1, 0))
    return 3 if start <= t_utc < end else 2


def to_utc(t_local):
    for off in (3, 2):
        u = t_local - dt.timedelta(hours=off)
        if helsinki_offset_utc(u) == off:
            return u
    return t_local - dt.timedelta(hours=2)


def from_utc(t_utc):
    return t_utc + dt.timedelta(hours=helsinki_offset_utc(t_utc))


def monday(d):
    return d - dt.timedelta(days=d.weekday())


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


def bin_clearance(x, step):
    """Distance from x to the nearest edge of its rounding cell, as a share of the step (0.5 is the centre)."""
    q = x / step
    return 0.5 - abs(q - math.floor(q + 0.5))


def ceil_clearance(x, step):
    """For a value rounded up to whole steps: the distance to the nearest step boundary as a share of the step."""
    f = x / step - math.floor(x / step)
    return min(f, 1 - f)


def fi_date(d):
    return "%d.%d.%d" % (d.day, d.month, d.year)


MONTH = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
         "November", "December"]
WEEKDAY = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def long_date(d):
    return "%s %d %s %d" % (WEEKDAY[d.weekday()], d.day, MONTH[d.month], d.year)
