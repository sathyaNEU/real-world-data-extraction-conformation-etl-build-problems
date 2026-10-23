"""task175 shared constants and writers: the in-fiction calendar, file names, and byte-stable writers."""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import io

import numpy as np

CITY = "City of Port Ardell"
UTIL = "Port Ardell Utilities"
PROGRAM = "Utility Extension Program"
APPRAISER = "Calusa County Property Appraiser"

RECORDS_END = dt.date(2026, 12, 31)
ASSEMBLED = dt.date(2027, 1, 8)

# file names (bundle paths)
F_ROLL = "pa_parcel_extract_2026.csv"
F_PLEG = "bldg_permits_legacy_2008_2018.csv"
F_PNEW = "bldg_permits_2019_2026.xlsx"
F_SCHED = "uep_program_schedule_rev12_2026.pdf"
F_PLAT = "plat_unit_index.csv"
F_PREM = "cis_premise_extract_20261231.csv"
F_ACCT = "cis_account_history_20261231.csv"
F_AMI = "ami_headend_installs_fy25_fy26.csv"
F_FEES = "capacity_fee_receipts_fy2026.xlsx"
F_CONV = "revenue_sufficiency_forecast_conventions_fy2027.pdf"
F_DICT = "field_definitions.txt"
F_MAN = "export_manifest.csv"
F_ACS = "acs_2020_2024_port_ardell_tracts.csv"
F_SAR = "uep_special_assessment_roll_2026.csv"

DELIV_XLSX = "uep_2027_permit_forecast.xlsx"
DELIV_PNG = "fy2026_capacity_fees.png"
DISTRACTORS = [F_ACS, F_SAR]


def stream(name):
    h = int.from_bytes(hashlib.sha256(("task175/" + name).encode()).digest()[:8], "little")
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


def iso(d):
    return "" if d is None else d.isoformat()


def mdy(d):
    return "" if d is None else "%02d/%02d/%04d" % (d.month, d.day, d.year)


def to_date(x):
    if x is None:
        return None
    if isinstance(x, np.datetime64):
        if np.isnat(x):
            return None
        return dt.date.fromisoformat(str(x.astype("datetime64[D]")))
    return x


def fq(d):
    """fiscal quarter (1 to 4) and fiscal year of a date; the fiscal year runs October to September"""
    fy = d.year + (1 if d.month >= 10 else 0)
    q = ((d.month - 10) % 12) // 3 + 1
    return fy, q
