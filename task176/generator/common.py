"""task176 shared constants and helpers: the in-fiction calendar, the random streams, the file names, the
counties and regions, and the writers that make every file reproduce byte for byte."""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import io

import numpy as np

STATE = "Allerton"
DEPT = "Allerton Department of Early Learning"
OFFICE = "Office of Child Care"
GRANT = "Home Child Care Start-Up Grant"

SIM_START = (2004, 1)                    # the first homes simulated
EXTRACT_FROM = dt.date(2016, 1, 1)       # the licensing extract holds homes licensed on or after this day
MIGRATION = dt.date(2019, 7, 1)          # licensing system migration: legacy licence numbers before it
RECORD_END = dt.date(2026, 12, 31)       # the record runs to this day
PULL = dt.date(2027, 1, 8)               # extracts pulled
ASSEMBLED = dt.date(2027, 1, 12)         # the supply analyst's folder assembled
FORECAST_YEAR = 2027
K_CUTOFF = (9, 1)                        # a child starts kindergarten in the school year after turning 5 on or before 1 September

# counties (FIPS-style code, name, region, weight)
COUNTIES = (
    ("57001", "Ashby", 1, 0.045), ("57003", "Brisco", 3, 0.050), ("57005", "Corrow", 1, 0.040),
    ("57007", "Dunmore", 2, 0.115), ("57009", "Garvey", 4, 0.055), ("57011", "Harlan", 2, 0.215),
    ("57013", "Kessling", 2, 0.060), ("57015", "Lisle", 4, 0.070), ("57017", "Morrow", 3, 0.045),
    ("57019", "Oakhurst", 4, 0.050), ("57021", "Penfield", 1, 0.035), ("57023", "Selden", 5, 0.110),
    ("57025", "Tolland", 3, 0.060), ("57027", "Wexley", 5, 0.050),
)
REGIONS = {1: "Region 1 North", 2: "Region 2 Capital", 3: "Region 3 Valley", 4: "Region 4 South", 5: "Region 5 Lakeshore"}
COUNTY_NAME = {c[0]: c[1] for c in COUNTIES}
COUNTY_REGION = {c[0]: c[2] for c in COUNTIES}

# file names
F_LIC = "fcc_licence_extract_20261231.csv"
F_XW = "licence_number_crosswalk_2019.csv"
F_WS = "capacity_worksheet_children_2016_2026.csv"
F_GRANT = "startup_grant_awards_2023.xlsx"
F_CCAP = "ccap_payment_lines_2026.csv"
F_CACFP = "cacfp_home_claims_2026.csv"
F_VIS = "licensing_visits_2026.csv"
F_CTY = "county_region_lookup.csv"
F_RULES = "family_child_care_licensing_rules_2025.pdf"
F_POL = "ccap_provider_payment_policy_2026.pdf"
F_SUP = "child_care_supply_report_2026q3.pdf"
F_QRIS = "qris_star_ratings_2026.csv"
F_MRS = "market_rate_survey_2025.xlsx"
F_DICT = "data_dictionary.txt"
F_MAN = "export_manifest.csv"
ALL_FILES = (F_LIC, F_XW, F_WS, F_GRANT, F_CCAP, F_CACFP, F_VIS, F_CTY, F_RULES, F_POL, F_SUP, F_QRIS, F_MRS,
             F_DICT, F_MAN)
DISTRACTORS = (F_QRIS, F_MRS, F_CACFP, F_VIS)
DELIVERABLE = "fcc_closures_2027.xlsx"


def stream(name):
    h = int.from_bytes(hashlib.sha256(("task176/" + name).encode()).digest()[:8], "little")
    return np.random.default_rng(h)


def mi(y, m):
    """month index, 0 = January 2004"""
    return (y - SIM_START[0]) * 12 + (m - SIM_START[1])


def ym_of(m):
    return SIM_START[0] + m // 12, m % 12 + 1


def month_start(m):
    y, mo = ym_of(m)
    return dt.date(y, mo, 1)


def month_end(m):
    y, mo = ym_of(m + 1)
    return dt.date(y, mo, 1) - dt.timedelta(days=1)


def dec(d):
    """a date as a decimal year (for ages)"""
    start = dt.date(d.year, 1, 1)
    return d.year + (d - start).days / (dt.date(d.year + 1, 1, 1) - start).days


def kyear(birth):
    """the calendar year in whose September a child born on `birth` starts kindergarten"""
    return birth.year + 5 if (birth.month, birth.day) <= K_CUTOFF else birth.year + 6


def write_csv(path, head, rows, crlf=True, delim=","):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\r\n" if crlf else "\n", delimiter=delim)
    w.writerow(head)
    for r in rows:
        w.writerow(r)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(buf.getvalue())
    return len(rows)


def read_csv(path, delim=","):
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh, delimiter=delim))


def edge(v, unit):
    """distance from v to the nearest edge of the printed cell it falls in at rounding unit `unit`"""
    c = round(v / unit) * unit
    return unit / 2 - abs(v - c)


def rnd(v, unit):
    return int(round(v / unit) * unit)
