"""task173 shared constants and writers: the in-fiction calendar, file names, random streams and byte-stable writers."""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import io

import numpy as np

CITY = "City of Hollis Bend"
UTIL = "Hollis Bend Water Utilities"
CONTRACTOR = "Mabry-Teague Utility Constructors, Inc."
AMI_VENDOR = "Halvorsen Metering Services, LLC"
STOP_VENDOR = "Arredondo Field Services"

HIST_START = dt.date(2012, 1, 1)
RECORDS_END = dt.date(2026, 9, 30)      # last day of every extract
PULLED = dt.date(2026, 10, 5)           # extract date
ASSEMBLED = dt.date(2026, 10, 21)       # the planner's folder
CUTOVER = dt.date(2021, 5, 17)          # first day in the new work management system
LEGACY_LAST = dt.date(2021, 5, 14)
FY26 = (dt.date(2025, 10, 1), dt.date(2026, 9, 30))
AMI_FIRST = dt.date(2027, 2, 1)
AMI_LAST = dt.date(2027, 7, 30)

CENTERS = ["NORTH", "SOUTH", "WEST"]
YARD = {"NORTH": "NORTHSIDE YARD", "SOUTH": "PECAN ST YARD", "WEST": "WEST LOOP YARD"}

# bundle paths
F_GIS_SVC = "gis_service_lines_20260930.csv"
F_GIS_MAIN = "gis_water_mains_20260930.csv"
F_PREM = "cis_premises_20260930.csv"
F_METER = "cis_meter_events_2012_2026.csv"
F_LEGACY = "lwms_workorders_2012_2021.csv"
F_EAM = "eam_workorders_2021_2026.xlsx"
F_AMI = "ami_install_schedule_2027.csv"
F_CAP = "cip_2027_water_main_replacement.pdf"
F_BID = "itb_27-0114_service_repair_restoration_bid_schedule.pdf"
F_PAYEST = "mabry_teague_pay_estimates_fy2025_fy2026.xlsx"
F_AP = "ap_payments_contract_23-0388.csv"
F_VALVE = "valve_exercise_log_2019_2026.csv"
F_FLUSH = "unidirectional_flushing_plan_2027.pdf"
F_WX = "hbx_airport_daily_weather_2012_2026.csv"
F_DICT = "field_definitions.txt"
F_MAN = "export_manifest.csv"

DELIV_XLSX = "service_leak_forecast_2027.xlsx"
DELIV_PNG = "service_leaks_by_month.png"
DISTRACTORS = [F_VALVE, F_FLUSH, F_WX]


def stream(name):
    h = int.from_bytes(hashlib.sha256(("task173/v3/" + name).encode()).digest()[:8], "little")
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


def day(d0, k):
    return d0 + dt.timedelta(days=int(k))


def fy_quarter(d):
    """fiscal year (Oct-Sep) and its quarter 1..4"""
    fy = d.year + 1 if d.month >= 10 else d.year
    q = {10: 1, 11: 1, 12: 1, 1: 2, 2: 2, 3: 2, 4: 3, 5: 3, 6: 3, 7: 4, 8: 4, 9: 4}[d.month]
    return fy, q
