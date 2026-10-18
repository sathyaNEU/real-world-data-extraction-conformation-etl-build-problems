"""task167 shared constants and helpers: file names, the in-fiction dates, money and date formatting, and the
writers that make office files and CSVs reproduce byte for byte."""
from __future__ import annotations

import csv
import datetime as dt
import io
import os

import world as W

F_REGISTER = "fund_commitments_register.xlsx"
F_ACTIVITY = "investor_capital_activity_2016-04_2026-12.csv"
F_LEGACY = "legacy_administrator_notices_2006-2016.xlsx"
F_FX = "eur_usd_reference_rates_2006-2026.csv"
F_POLICY = "liquidity_and_reserve_policy_2025.pdf"
F_CAPACC = "capital_account_summary_2026-12-31.xlsx"
F_POS = "reserve_custody_positions_2026-12-31.csv"
F_CUSTACT = "reserve_custody_activity_2026.csv"
F_DICT = "data_dictionary.xlsx"
F_MANIFEST = "export_manifest.csv"
F_GRANTS = "grants_budget_2027.docx"
F_PERF = "gp_reported_performance_2026q3.csv"
ALL_FILES = (F_REGISTER, F_ACTIVITY, F_LEGACY, F_FX, F_POLICY, F_CAPACC, F_POS, F_CUSTACT, F_DICT, F_MANIFEST,
             F_GRANTS, F_PERF)
DISTRACTORS = (F_GRANTS, F_PERF)

ORG = W.ORG
OFFICE = "Brandvold Foundation Investment Office"
ADMIN = "fund administrator"
# the in-fiction stamps of each file (UTC ISO for office files)
STAMPS = {
    F_REGISTER: ("2014-03-03T15:12:00Z", "2027-01-11T21:40:00Z"),
    F_LEGACY: ("2016-07-08T13:05:00Z", "2016-07-08T13:22:00Z"),
    F_CAPACC: ("2027-01-13T16:02:00Z", "2027-01-13T16:09:00Z"),
    F_DICT: ("2019-05-20T14:31:00Z", "2027-01-14T17:55:00Z"),
    F_GRANTS: ("2026-11-24T15:47:00Z", "2026-12-11T19:02:00Z"),
}
EXPORT_DAY = dt.date(2027, 1, 14)          # the risk office assembled the files for the 21 January board book


def d_iso(d):
    return d.isoformat()


def d_us(d):
    return "%02d/%02d/%04d" % (d.month, d.day, d.year)


def money(x):
    """an amount in currency units to two decimals, as text"""
    return "%.2f" % round(x + 0.0, 2)


def write_csv(path, head, rows, crlf=True):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\r\n" if crlf else "\n")
    w.writerow(head)
    for r in rows:
        w.writerow(r)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(buf.getvalue())
    return len(rows)


def business_day_before(d, n):
    k = 0
    while k < n:
        d -= dt.timedelta(days=1)
        if d.weekday() < 5:
            k += 1
    return d


def roll_business(d):
    while d.weekday() >= 5 or (d.month, d.day) in ((1, 1), (12, 25), (7, 4)):
        d += dt.timedelta(days=1)
    return d


def us_eastern_offset(t):
    """hours from UTC for US Eastern Time at local time t (second Sunday of March to first Sunday of November)"""
    y = t.year
    mar = dt.datetime(y, 3, 8)
    while mar.weekday() != 6:
        mar += dt.timedelta(days=1)
    nov = dt.datetime(y, 11, 1)
    while nov.weekday() != 6:
        nov += dt.timedelta(days=1)
    return -4 if mar.replace(hour=2) <= t < nov.replace(hour=2) else -5


def us_central_offset(t):
    return us_eastern_offset(t) - 1
