"""task159 constants and helpers shared by every generator module.

The Vellmouth Transit Commission runs the city's six-line subway. Its station planning desk files, in each roster
pick notice, the number of weekday-morning platform conductor shifts the pick posts: under the platform crowding
standard a conductor is posted on a watch-list platform on each weekday morning whose forecast peak quarter-hour
accumulation is more than 85 per cent of the platform's rated capacity. The spring 2027 pick runs Monday 1 March to
Friday 25 June 2027 and its notice closes on Wednesday 20 January. The desk pulled every file on Monday 11 January
2027; the fare export closes with the last hour of the Sunday 10 January service day, 00:00 to 01:00 local.

The seed was fixed by rule before any data was generated: the task number, then the as-of month and day."""
from __future__ import annotations

import datetime as dt
import hashlib
import os

SEED = 1590111

ORG = "Vellmouth Transit Commission"
ORG_SHORT = "VTC"
CITY = "Vellmouth"
PEOPLE = {
    "planning_manager": "Beth Lewis",     # station planning manager: the crowding standard, the pick notice
    "service_planner": "Ralph Chambers",  # service planning: the autumn and spring service plans
    "ridership": "Mary Wheeler",          # ridership data: the fare export, the dashboard, the dictionary
    "counts": "Caleb Rowe",               # count programme supervisor: the station census and platform counts
}

UTC = dt.timezone.utc
HERE = os.path.dirname(os.path.abspath(__file__))
TASK_DIR = os.path.dirname(HERE)
TARGET = os.path.join(TASK_DIR, "target")

# ------------------------------------------------------------------------------------------------- calendar
AS_OF = dt.date(2027, 1, 11)                  # Monday, the pull
EXPORT_END = dt.date(2027, 1, 10)             # last local service day in the fare export
NEW_EXPORT_START = dt.date(2024, 6, 3)        # the back office's first service day (parallel run in June)
LEGACY_END = dt.date(2024, 6, 30)             # the legacy system's last service day
LEGACY_START = dt.date(2022, 2, 1)
CUTOVER = dt.date(2024, 7, 1)                 # the back office becomes the system of record
KENNET_JOIN = dt.date(2024, 3, 4)             # Albrecht Place and Kennet Street become one complex
PICK_START = dt.date(2027, 3, 1)
PICK_END = dt.date(2027, 6, 25)
NOTICE_CLOSES = dt.date(2027, 1, 20)
EIGHT_CAR_START = dt.date(2027, 3, 1)         # Line 5 runs eight-car trains from the spring pick
AUTUMN_PICK = (dt.date(2026, 9, 8), dt.date(2026, 12, 18))  # the autumn 2026 pick's service plan in force
CENSUS_WINDOW = (dt.date(2026, 10, 6), dt.date(2026, 10, 29))
COUNT_WINDOW = (dt.date(2026, 10, 6), dt.date(2026, 11, 20))
DST_END_2026 = dt.date(2026, 11, 1)

# Days the subway runs its holiday timetable (Sunday service): the federal holidays below and the day after
# Thanksgiving. Columbus Day, Veterans Day and Juneteenth run the weekday timetable on lighter ridership.
HOLIDAYS = {
    dt.date(2022, 2, 21), dt.date(2022, 5, 30), dt.date(2022, 7, 4), dt.date(2022, 9, 5), dt.date(2022, 11, 24),
    dt.date(2022, 11, 25), dt.date(2022, 12, 26),
    dt.date(2023, 1, 2), dt.date(2023, 1, 16), dt.date(2023, 2, 20), dt.date(2023, 5, 29), dt.date(2023, 7, 4),
    dt.date(2023, 9, 4), dt.date(2023, 11, 23), dt.date(2023, 11, 24), dt.date(2023, 12, 25),
    dt.date(2024, 1, 1), dt.date(2024, 1, 15), dt.date(2024, 2, 19), dt.date(2024, 5, 27), dt.date(2024, 7, 4),
    dt.date(2024, 9, 2), dt.date(2024, 11, 28), dt.date(2024, 11, 29), dt.date(2024, 12, 25),
    dt.date(2025, 1, 1), dt.date(2025, 1, 20), dt.date(2025, 2, 17), dt.date(2025, 5, 26), dt.date(2025, 7, 4),
    dt.date(2025, 9, 1), dt.date(2025, 11, 27), dt.date(2025, 11, 28), dt.date(2025, 12, 25),
    dt.date(2026, 1, 1), dt.date(2026, 1, 19), dt.date(2026, 2, 16), dt.date(2026, 5, 25), dt.date(2026, 7, 3),
    dt.date(2026, 9, 7), dt.date(2026, 11, 26), dt.date(2026, 11, 27), dt.date(2026, 12, 25),
    dt.date(2027, 1, 1), dt.date(2027, 1, 18), dt.date(2027, 2, 15), dt.date(2027, 5, 31),
}
# weekday timetable, lighter riding (schools and federal offices closed)
REDUCED = {
    dt.date(2022, 6, 20), dt.date(2022, 10, 10), dt.date(2022, 11, 11),
    dt.date(2023, 6, 19), dt.date(2023, 10, 9), dt.date(2023, 11, 10),
    dt.date(2024, 6, 19), dt.date(2024, 10, 14), dt.date(2024, 11, 11),
    dt.date(2025, 6, 19), dt.date(2025, 10, 13), dt.date(2025, 11, 11),
    dt.date(2026, 6, 19), dt.date(2026, 10, 12), dt.date(2026, 11, 11),
    dt.date(2027, 6, 18),
}
# the week between Christmas and New Year: weekday timetable, holiday-week riding
WINTER_WEEK = {dt.date(2026, 12, 28), dt.date(2026, 12, 29), dt.date(2026, 12, 30), dt.date(2026, 12, 31),
               dt.date(2025, 12, 26), dt.date(2025, 12, 29), dt.date(2025, 12, 30), dt.date(2025, 12, 31),
               dt.date(2024, 12, 26), dt.date(2024, 12, 27), dt.date(2024, 12, 30), dt.date(2024, 12, 31),
               dt.date(2023, 12, 26), dt.date(2023, 12, 27), dt.date(2023, 12, 28), dt.date(2023, 12, 29),
               dt.date(2022, 12, 27), dt.date(2022, 12, 28), dt.date(2022, 12, 29), dt.date(2022, 12, 30)}

WD = ["Mon", "Tue", "Wed", "Thu", "Fri"]

# the mtime every shipped file carries (the pull, local morning)
PACK_MTIME = dt.datetime(2027, 1, 11, 9, 40)


def daterange(a, b):
    d = a
    while d <= b:
        yield d
        d += dt.timedelta(days=1)


def is_ordinary_weekday(d):
    return d.weekday() < 5 and d not in HOLIDAYS and d not in REDUCED and d not in WINTER_WEEK


def pick_dates():
    """The spring pick's ordinary weekdays (Memorial Day out)."""
    return [d for d in daterange(PICK_START, PICK_END) if d.weekday() < 5 and d not in HOLIDAYS]


def us_eastern_offset(t_local_date, hour):
    """Hours to add to Vellmouth local time to get UTC on a date (US Eastern rules: DST from the second Sunday of
    March 02:00 to the first Sunday of November 02:00)."""
    y = t_local_date.year
    mar = dt.date(y, 3, 8)
    dst_start = mar + dt.timedelta(days=(6 - mar.weekday()) % 7)
    nov = dt.date(y, 11, 1)
    dst_end = nov + dt.timedelta(days=(6 - nov.weekday()) % 7)
    if dst_start < t_local_date < dst_end:
        return 4
    if t_local_date == dst_start:
        return 4 if hour >= 2 else 5
    if t_local_date == dst_end:
        return 5 if hour >= 2 else 4
    return 5


def stable_hash(*parts):
    h = hashlib.sha256("|".join(str(p) for p in parts).encode()).hexdigest()
    return int(h[:12], 16)


# ------------------------------------------------------------------------------------------------- writers
import csv as _csv
import io as _io
import json as _json


def write_csv(path, cols, rows, crlf=False):
    buf = _io.StringIO()
    w = _csv.writer(buf, lineterminator="\r\n" if crlf else "\n")
    w.writerow(cols)
    n = 0
    for r in rows:
        w.writerow(r)
        n += 1
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(buf.getvalue())
    return n


def write_text(path, text):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def fmt_int(n):
    return "{:,}".format(int(n))


def round_half_up(x, step=1.0):
    import math
    return math.floor(x / step + 0.5) * step
