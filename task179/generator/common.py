"""task179 shared constants and writers: the in-fiction calendar, file names, random streams and byte-stable writers."""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import io
import json

import numpy as np

STATE = "State of Merrow"
DEPT = "Merrow Department of Corrections"
DIVISION = "Division of Community Supervision"
REGION = "Region 4"
CITY = "Halverton"
HPD = "Halverton Police Department"
COUNTIES = ("Darrow", "Keswick")
DARROW_JAIL = "Darrow County Jail"
KESWICK_JAIL = "Keswick County Jail"
VENDOR = "Belvantis Monitoring Solutions"

SIM_START = dt.date(2013, 1, 1)
RECORDS_START = dt.date(2018, 1, 1)
RECORDS_END = dt.date(2026, 12, 31)
MIGRATION = dt.date(2022, 6, 13)          # legacy OMS to CMS cutover
RECODIFIED = dt.date(2024, 7, 1)          # the criminal code recodification took effect
INSTRUMENT_V2 = dt.date(2023, 7, 1)       # risk instrument revision
GPS_LOG_START = dt.date(2025, 1, 1)
ASSEMBLED = dt.date(2027, 1, 8)
DIRECTIVE_DATE = dt.date(2026, 11, 16)

# bundle file names
F_EPIS = "cms_supervision_episodes_2018-2026.csv"
F_XWALK = "oms_cms_person_crosswalk_2022.csv"
F_ASSESS = "mras_assessments_2017-2026.csv"
F_DARROW = "darrow_county_jail_booking_notices_2018-2026.csv"
F_KESWICK = "keswick_county_jail_bookings_2018-2026.xlsx"
F_HPD = "hpd_violent_incident_victims_2018-2026.csv"
F_GPS = "belvantis_r4_device_events_2025-2026.json"
F_PROG = "program_referrals_2018-2026.csv"
F_DIRECTIVE = "directive_26-07_gps_placement.pdf"
F_CODE = "criminal_code_conversion_table_2024.pdf"
F_SCHED = "belvantis_service_schedule_2025.pdf"
F_BRIEF = "merrow_recidivism_brief_2025.pdf"

DELIV_XLSX = "region4_2027_gps_order.xlsx"
DELIV_DOCX = "region4_2027_category_v_forecast.docx"
DISTRACTORS = [F_PROG, F_BRIEF]

ROUND_CALL = 100


SALT = "s1"


def stream(name):
    h = int.from_bytes(hashlib.sha256(("task179/a5/%s/%s" % (SALT, name)).encode()).digest()[:8], "little")
    return np.random.default_rng(h)


def write_csv(path, head, rows, crlf=True):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\r\n" if crlf else "\n")
    w.writerow(head)
    n = 0
    for r in rows:
        w.writerow(["" if v is None else v for v in r])
        n += 1
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(buf.getvalue())
    return n


def write_json(path, obj):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, indent=1, ensure_ascii=False, sort_keys=False)
        f.write("\n")


def iso(d):
    return "" if d is None else d.isoformat()


def mdy(d):
    return "" if d is None else "%02d/%02d/%04d" % (d.month, d.day, d.year)


def month_index(d):
    return d.year * 12 + d.month - 1


def month_start(mi):
    return dt.date(mi // 12, mi % 12 + 1, 1)


def month_days(mi):
    a = month_start(mi)
    b = month_start(mi + 1)
    return (b - a).days


def add_months(d, n):
    mi = month_index(d) + n
    y, m = mi // 12, mi % 12 + 1
    last = month_days(mi)
    return dt.date(y, m, min(d.day, last))


def quarter(d):
    return (d.month - 1) // 3 + 1


def nearest(v, unit):
    return int(unit * np.floor(v / unit + 0.5))


def edge_distance(v, unit):
    """distance from v to the nearest edge of the cell its rounding prints"""
    c = unit * np.floor(v / unit + 0.5)
    return unit / 2.0 - abs(v - c)
