"""task172 shared constants and helpers: the file names, the in-fiction dates, the random streams and the writers
that make CSVs reproduce byte for byte."""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import io

import numpy as np

ORG = "Sallowmere Software"
TEAM = "Global Mobility"
COUNSEL = "Marrowby Teale LLP"

F_NOTICES = "renewal_case_notices_2024-01_2026-12.csv"
F_REGISTER = "renewal_case_register.xlsx"
F_ACTIONS = "case_actions_2024-2026.csv"
F_PERMITS = "work_permits_2026-12.xlsx"
F_EMPLOYEES = "employees_2026-12.csv"
F_DEPENDANTS = "dependants_2026-12.csv"
F_TRACKER = "green_card_tracker_2026-12.xlsx"
F_DISPATCH = "packet_dispatch_log_2025-2026.csv"
F_POLICY = "mobility_renewal_standard.pdf"
F_THREAD = "q1_quote_thread.eml"
F_DICT = "data_dictionary.xlsx"
F_MANIFEST = "export_manifest.csv"
F_POSTED = "posted_processing_times_2024-2026.csv"
F_H1B = "h1b_extension_calendar_2027.xlsx"
ALL_FILES = (F_NOTICES, F_REGISTER, F_ACTIONS, F_PERMITS, F_EMPLOYEES, F_DEPENDANTS, F_TRACKER, F_DISPATCH,
             F_POLICY, F_THREAD, F_DICT, F_MANIFEST, F_POSTED, F_H1B)
DISTRACTORS = (F_POSTED, F_H1B)

# the in-fiction calendar
EXPORT = dt.date(2026, 12, 4)              # the case system's export, pulled on a Friday
GO_LIVE = dt.date(2026, 12, 15)            # the portal's quarterly content release
Q_START, Q_END = dt.date(2027, 1, 1), dt.date(2027, 3, 31)
IFR = dt.date(2025, 10, 30)                # renewals filed from this date no longer extend the card
C9_18M = dt.date(2025, 12, 5)              # (c)(9) cards approved from this date run 18 months
C9_5Y = dt.date(2023, 9, 27)               # (c)(9) cards approved from this date (to 4 Dec 2025) ran five years
REGISTER_SWITCH = dt.date(2025, 4, 1)      # the team's register moved to its new case system
DISPATCH_SWITCH = dt.date(2026, 3, 2)      # the mailroom's new dispatch system went live
RECORD_START = dt.date(2024, 1, 1)
MONTH_DAYS = 30.4                          # the standard's month
ASK_A_MONTHS = ((2027, 7), (2027, 8), (2027, 9))
ASK_B_QUARTERS = (("2025 Q4", dt.date(2025, 10, 1), dt.date(2025, 12, 31)),
                  ("2026 Q1", dt.date(2026, 1, 1), dt.date(2026, 3, 31)),
                  ("2026 Q2", dt.date(2026, 4, 1), dt.date(2026, 6, 30)),
                  ("2026 Q3", dt.date(2026, 7, 1), dt.date(2026, 9, 30)))
REFILE_DAYS = 30
CATS = ("(c)(9)", "(c)(26)")

HOLIDAYS = set()
for _y in range(2018, 2029):
    for _m, _d in ((1, 1), (7, 4), (11, 11), (12, 25)):
        HOLIDAYS.add(dt.date(_y, _m, _d))
    # Thanksgiving, Memorial Day, Labor Day, MLK Day, Presidents Day
    _t = dt.date(_y, 11, 1)
    while _t.weekday() != 3:
        _t += dt.timedelta(days=1)
    HOLIDAYS.add(_t + dt.timedelta(days=21))
    _m = dt.date(_y, 5, 31)
    while _m.weekday() != 0:
        _m -= dt.timedelta(days=1)
    HOLIDAYS.add(_m)
    _l = dt.date(_y, 9, 1)
    while _l.weekday() != 0:
        _l += dt.timedelta(days=1)
    HOLIDAYS.add(_l)
    for _mon, _nth in ((1, 3), (2, 3)):
        _x = dt.date(_y, _mon, 1)
        while _x.weekday() != 0:
            _x += dt.timedelta(days=1)
        HOLIDAYS.add(_x + dt.timedelta(days=7 * (_nth - 1)))


def stream(name):
    """an independent, reproducible random stream for one part of the world"""
    h = int.from_bytes(hashlib.sha256(("task172/" + name).encode()).digest()[:8], "little")
    return np.random.default_rng(h)


def busday(d):
    return d.weekday() < 5 and d not in HOLIDAYS


def next_busday(d):
    while not busday(d):
        d += dt.timedelta(days=1)
    return d


def prev_busday(d):
    while not busday(d):
        d -= dt.timedelta(days=1)
    return d


def add_days(d, n):
    return d + dt.timedelta(days=int(round(n)))


def d_iso(d):
    return "" if d is None else d.isoformat()


def d_us(d):
    return "" if d is None else "%02d/%02d/%04d" % (d.month, d.day, d.year)


def parse_iso(s):
    return None if not s else dt.date.fromisoformat(s[:10])


def parse_us(s):
    if not s:
        return None
    m, d, y = s.split("/")
    return dt.date(int(y), int(m), int(d))


def quarter_of(d):
    return "%d Q%d" % (d.year, (d.month - 1) // 3 + 1)


def write_csv(path, head, rows, crlf=True):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\r\n" if crlf else "\n")
    w.writerow(head)
    for r in rows:
        w.writerow(r)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(buf.getvalue())
    return len(rows)


def read_csv(path):
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def half_month(v):
    """round to the nearest half month, halves away from zero"""
    import math
    return math.floor(v * 2 + 0.5) / 2


def edge(v, unit):
    """distance from v to the nearest edge of the printed cell it falls in"""
    c = round(v / unit) * unit
    return unit / 2 - abs(v - c)
