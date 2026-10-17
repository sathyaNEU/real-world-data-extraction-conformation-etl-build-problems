"""Names, keys and clocks shared by the generator, the checks and the deliverables."""
from __future__ import annotations

import datetime as dt
from zoneinfo import ZoneInfo

import world as W

MEL = ZoneInfo("Australia/Melbourne")
UTC = dt.timezone.utc

# the extract (WR-26-1187), as Workforce Systems wrote it
F_OFFERS = "callin_offers_20250829_20261112.csv"
F_REGISTER = "callin_register_20250829_20261112.csv"
F_LEGACY = "roster_export_legacy_20250829_20260226.csv"
F_KWS = "roster_lines_kws_20260227_20261112.csv"
F_XMAS = "christmas_roster_2026_published.xlsx"
F_PEOPLE = "kws_people_20261112.csv"
F_AVAIL = "kws_availability_20261112.json"
F_PAYROLL = "payroll_casual_register_20261112.csv"
F_STORES = "stores.csv"
F_STANDARD = "relief_crew_placement_standard.pdf"
F_NOTES = "kws_callin_module_notes.pdf"
F_EA = "ea_2024_casual_employment_summary.pdf"
F_PLAN = "christmas_trading_plan_2026.xlsx"
F_CAL = "vic_school_terms_public_holidays_2025_2026.csv"
F_TRANSMIT = "WR-26-1187_extract_transmittal.txt"
DISTRACTORS = [F_PLAN, F_CAL]
DELIVERABLES = ["relief_crew_placement_xmas2026.pdf", "relief_crew_xmas2026.xlsx"]

STORE_NO = {"RG": 1, "W3": 2, "E2": 3, "W1": 4, "W4": 5, "E1": 6, "W2": 7, "E3": 8}
LOC = {s: "KW%02d" % n for s, n in STORE_NO.items()}
CC = {s: "41%02d" % n for s, n in STORE_NO.items()}
OPENED = {"RG": 1962, "W3": 1978, "E2": 1984, "W1": 1991, "W4": 1996, "E1": 2003, "W2": 2011, "E3": 2017}
CLUSTER_NAME = {"W": "West", "E": "East", None: ""}
BY_LOC = {v: k for k, v in LOC.items()}
BY_CC = {v: k for k, v in CC.items()}
BY_NAME = {W.STORE_NAMES[s].upper(): s for s in W.STORES}

REASON = {"OPEN": "OPN", "ABSENCE": "ABS", "LEAVE": "LVE"}
ANSWER = {"A": "ACCEPTED", "D": "DECLINED", "N": "NO RESPONSE"}


def local_dt(m):
    """engine minutes (store wall clock) -> naive store-time datetime, to the second"""
    return dt.datetime(W.D0.year, W.D0.month, W.D0.day) + dt.timedelta(seconds=int(round(m * 60)))


def to_utc(t):
    """a naive store-time datetime -> aware UTC; a time in the spring-forward gap is read an hour later"""
    a = t.replace(tzinfo=MEL)
    if a.utcoffset() != a.replace(fold=1).utcoffset() and a.fold == 0:
        back = a.astimezone(UTC).astimezone(MEL).replace(tzinfo=None)
        if back != t:               # nonexistent wall time
            a = (t + dt.timedelta(hours=1)).replace(tzinfo=MEL)
    return a.astimezone(UTC)


def utc_str(m):
    return to_utc(local_dt(m)).strftime("%Y-%m-%dT%H:%M:%SZ")


def hhmm(minutes_of_day):
    return "%02d:%02d" % divmod(int(minutes_of_day), 60)


def ampm(minutes_of_day):
    h, m = divmod(int(minutes_of_day), 60)
    suf = "AM" if h < 12 or h == 24 else "PM"
    h12 = h % 12 or 12
    return "%d:%02d %s" % (h12, m, suf)


def paid_hours(start, end):
    return W.paid(end - start) / 60.0
