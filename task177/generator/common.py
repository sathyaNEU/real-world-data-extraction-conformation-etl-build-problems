"""task177 shared constants and helpers: the file names, the in-fiction calendar, Manitoba's clock, the random
streams and the writers that make the files reproduce byte for byte."""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import io
import math

import numpy as np

ORG = "Prairie Works Manitoba"
ASSISTANT = "Ask Prairie Works"
BN = "812447093"                       # Prairie Works Manitoba's own business number (the vendor's customer record)
VENDOR = "Riverlot Dialogue Inc."
VENDOR_CITY = "Kitchener, Ontario"
VENDOR_BN = "724906318"                # Riverlot's business number (its GST/HST registration on every invoice)

# ------------------------------------------------------------------------------------------------ the pack's files
F_LEGS = "contact_legs_2026.csv"
F_CONV = "assistant_sessions_2026.jsonl"
F_CLAIMS = "claims_register_2026.csv"
F_XWALK = "contact_details_crosswalk.csv"
F_CODES = "telephony_migration_codes.xlsx"
F_OVERFLOW = "overflow_episodes_2026.csv"
F_PLAN = "assistant_first_rollout_plan.pdf"
F_ACCEPT = "release4_acceptance_summary.pdf"
F_ORDER = "usage_tier_order_form_2027.pdf"
F_INVOICES = "vendor_invoices_2026.xlsx"
F_DICT = "data_dictionary.xlsx"
F_SURVEY = "post_contact_survey_2026.csv"
F_MANIFEST = "export_manifest.csv"
ALL_FILES = (F_LEGS, F_CONV, F_CLAIMS, F_XWALK, F_CODES, F_OVERFLOW, F_PLAN, F_ACCEPT, F_ORDER, F_INVOICES,
             F_DICT, F_SURVEY, F_MANIFEST)
DISTRACTORS = (F_OVERFLOW, F_SURVEY)

# ------------------------------------------------------------------------------------------- the in-fiction calendar
LAUNCH = dt.date(2026, 1, 5)            # Ask Prairie Works went live in the app and on the web (a Monday)
REC_START = LAUNCH                      # both exports start on the launch day
MIGRATION = dt.date(2026, 7, 6)         # the new telephony platform took the lines at 06:00 on this Monday
RETYPE = dt.date(2026, 9, 14)           # the vendor's release 3.4 (account types), live at 07:00
REC_END = dt.date(2027, 1, 3)           # the last day in both exports (a Sunday)
EXPORT_DAY = dt.date(2027, 1, 4)        # the exports were pulled early on this Monday
ORDER_DUE = dt.date(2027, 1, 8)         # the vendor needs the March and April tier by this Friday
POP_DATE = REC_END                      # the planning population: jobseekers with a claim open on this date
AF_START, AF_END = dt.date(2027, 1, 4), dt.date(2027, 2, 28)       # the assistant-first weeks
WIN_START, WIN_END = dt.date(2027, 3, 1), dt.date(2027, 4, 25)     # the forecast window (eight weeks)
QUARTERS = (("2026 Q1", dt.date(2026, 1, 1), dt.date(2026, 3, 31)),
            ("2026 Q2", dt.date(2026, 4, 1), dt.date(2026, 6, 30)),
            ("2026 Q3", dt.date(2026, 7, 1), dt.date(2026, 9, 30)),
            ("2026 Q4", dt.date(2026, 10, 1), dt.date(2026, 12, 31)))

# Manitoba's general holidays the contact centre closes on (2026 and the forecast's months of 2027)
HOLIDAYS = {dt.date(2026, 1, 1), dt.date(2026, 2, 16), dt.date(2026, 4, 3), dt.date(2026, 5, 18), dt.date(2026, 7, 1),
            dt.date(2026, 8, 3), dt.date(2026, 9, 7), dt.date(2026, 9, 30), dt.date(2026, 10, 12),
            dt.date(2026, 11, 11), dt.date(2026, 12, 25), dt.date(2026, 12, 28), dt.date(2027, 1, 1),
            dt.date(2027, 2, 15), dt.date(2027, 3, 26), dt.date(2027, 5, 24)}

# daylight saving time in Manitoba (America/Winnipeg): CDT (UTC-5) from 02:00 on the second Sunday of March to
# 02:00 on the first Sunday of November, CST (UTC-6) otherwise
DST = {2025: (dt.datetime(2025, 3, 9, 2), dt.datetime(2025, 11, 2, 2)),
       2026: (dt.datetime(2026, 3, 8, 2), dt.datetime(2026, 11, 1, 2)),
       2027: (dt.datetime(2027, 3, 14, 2), dt.datetime(2027, 11, 7, 2))}


def utc_offset_hours(local):
    """hours to add to Manitoba local time to get UTC (6 in winter, 5 in summer); a local time inside the
    autumn's repeated hour is read as the first (CDT) pass"""
    a, b = DST[local.year]
    return 5 if a <= local < b else 6


def to_utc(local):
    return local + dt.timedelta(hours=utc_offset_hours(local))


def to_local(utc):
    a, b = DST[utc.year]
    a_utc, b_utc = a + dt.timedelta(hours=6), b + dt.timedelta(hours=5)
    return utc - dt.timedelta(hours=5 if a_utc <= utc < b_utc else 6)


def stream(name):
    """an independent, reproducible random stream for one part of the world"""
    h = int.from_bytes(hashlib.sha256(("task177/" + name).encode()).digest()[:8], "little")
    return np.random.default_rng(h)


def days(a, b):
    """every date from a to b inclusive"""
    n = (b - a).days + 1
    return [a + dt.timedelta(days=i) for i in range(n)]


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


def edge(v, unit):
    """distance from v to the nearest edge of the printed cell it falls in"""
    c = round(v / unit) * unit
    return unit / 2 - abs(v - c)


def pct(v):
    """a share printed as a whole per cent, halves away from zero"""
    return int(math.floor(v * 100 + 0.5))


FORECAST_UNIT = 5                      # the prompt asks for the forecast share to the nearest 5 per cent


def pct5(v):
    """a forecast share printed to the nearest 5 per cent, halves away from zero"""
    return int(FORECAST_UNIT * math.floor(v * 100 / FORECAST_UNIT + 0.5))
