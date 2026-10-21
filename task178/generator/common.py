"""task178 shared constants: file names, the in-fiction calendar, the gauge's datums, the random streams and the
writers that make every file reproduce byte for byte."""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import io

import numpy as np

CITY = "City of Port Tessaly"
DEPT = "Department of Public Works"
DIV = "Waterfront and Harbor Engineering"
GAUGE = "Port Tessaly tide gauge"
GAUGE_ID = "PTG-01"

# ------------------------------------------------------------------------------------------------ the pack's files
F_VER = "ptg_verified_15min_1995-01_2026-06.csv"
F_TEL = "ptg_telemetry_6min_2026-05_2026-11.csv"
F_BOARD = "harbormaster_tideboard_hourly_2015-2026.csv"
F_TABLES = "port_tessaly_tide_tables_1995-2027.xlsx"
F_LOG = "ptg_station_log.xlsx"
F_DATUMS = "ptg_datum_sheet_rev2026-06.pdf"
F_SLR = "sea_level_guidance_2026.pdf"
F_BASIS = "granite_wharf_trestle_design_basis.pdf"
F_CLOSE = "dpw_street_closures_2016-2026.csv"
F_WX = "airport_daily_weather_2015-2026.csv"
F_RIVER = "pennock_river_daily_flow_2015-2026.csv"
F_DICT = "ptg_data_dictionary.xlsx"
F_MANIFEST = "export_manifest.csv"
ALL_FILES = (F_VER, F_TEL, F_BOARD, F_TABLES, F_LOG, F_DATUMS, F_SLR, F_BASIS, F_CLOSE, F_WX, F_RIVER, F_DICT,
             F_MANIFEST)
DISTRACTORS = (F_WX, F_RIVER)

# deliverables
G_BOOK = "granite_wharf_trestle_deck.xlsx"
G_CHART = "trestle_deck_exposure.png"

# --------------------------------------------------------------------------------------------- the calendar (UTC)
REC_START = dt.datetime(1995, 1, 1)
VER_END = dt.datetime(2026, 7, 1)          # verified through 30 June 2026
TEL_START = dt.datetime(2026, 5, 1)        # preliminary 6-minute telemetry from 1 May 2026
TEL_END = dt.datetime(2026, 12, 1)         # through 30 November 2026
BOARD_START = dt.datetime(2015, 1, 1)
PULL = dt.datetime(2026, 12, 8, 15, 40)    # the pack assembled (UTC)
WORK_START = dt.date(2027, 4, 1)           # trestle in use, local dates
WORK_END = dt.date(2027, 5, 31)
NEW_STND = dt.datetime(2026, 4, 28)        # station datum re-established after the gauge pier repair
BRACKET_FAIL = dt.datetime(2017, 10, 30, 15, 0)
BRACKET_RESET = dt.datetime(2018, 3, 12, 14, 30)

# ------------------------------------------------------------------------------------------------- datums (feet)
FT = 0.3048
EPOCH = (1983, 2001)          # the National Tidal Datum Epoch the datums and the tide tables use
EPOCH_MID = 1992.0
STND_BELOW_MLLW = 4.21        # station datum (1995) is 4.21 ft below MLLW
NAVD88_ABOVE_MLLW = 5.31      # NAVD88 on the gauge
NEW_STND_SHIFT = 0.12         # the 2026 station datum sits 0.12 ft above the former one
BOARD_ZERO_BELOW_MLLW = 3.00  # the harbormaster's tide board float zero
BRACKET_OFFSET = 0.08         # the primary sensor read 0.08 ft low from the bracket failure to the reset
SLR = 0.0024                  # metres per year relative sea-level rise
DECK_SETTINGS = tuple(round(10.60 + 0.25 * k, 2) for k in range(9))   # 10.60 .. 12.60 ft MLLW
DECK_BAR = 1.0                # expected tides reaching the deck, at most
STREET_LEVEL = 11.80          # Front Street's low point at the gauge, ft MLLW
ASK_A_FROM = dt.date(2016, 11, 1)
ASK_A_TO = dt.date(2026, 11, 30)
ASK_B_YEARS = tuple(range(2017, 2023))
PWWORKS_FROM = dt.datetime(2023, 7, 1)

J2000 = dt.datetime(2000, 1, 1, 12)


def hours(d):
    return (d - J2000).total_seconds() / 3600.0


def from_hours(h):
    return J2000 + dt.timedelta(hours=float(h))


def stream(name):
    h = int.from_bytes(hashlib.sha256(("task178/" + name).encode()).digest()[:8], "little")
    return np.random.default_rng(h)


# --------------------------------------------------------------------------------- US Eastern local time and DST
def _nth_sunday(y, m, n):
    d = dt.date(y, m, 1)
    while d.weekday() != 6:
        d += dt.timedelta(days=1)
    return d + dt.timedelta(days=7 * (n - 1))


def _last_sunday(y, m):
    d = dt.date(y, m + 1, 1) - dt.timedelta(days=1) if m < 12 else dt.date(y, 12, 31)
    while d.weekday() != 6:
        d -= dt.timedelta(days=1)
    return d


def dst_bounds_utc(y):
    """daylight time start and end in UTC (2:00 local) under the rule in force that year"""
    if y >= 2007:
        a, b = _nth_sunday(y, 3, 2), _nth_sunday(y, 11, 1)
    else:
        a, b = _nth_sunday(y, 4, 1), _last_sunday(y, 10)
    return dt.datetime(a.year, a.month, a.day, 7), dt.datetime(b.year, b.month, b.day, 6)


def to_local(t_utc):
    a, b = dst_bounds_utc(t_utc.year)
    off = 4 if a <= t_utc < b else 5
    return t_utc - dt.timedelta(hours=off), ("EDT" if off == 4 else "EST")


def local_to_utc(t_loc):
    """a wall-clock time to UTC (the hour that repeats in November read as daylight time)"""
    a, b = dst_bounds_utc(t_loc.year)
    for off in (4, 5):
        u = t_loc + dt.timedelta(hours=off)
        if (off == 4) == (a <= u < b):
            return u
    return t_loc + dt.timedelta(hours=5)


# ----------------------------------------------------------------------------------------------------- writers
def write_csv(path, head, rows, crlf=True, preamble=None):
    buf = io.StringIO()
    if preamble:
        for line in preamble:
            buf.write(line + ("\r\n" if crlf else "\n"))
    w = csv.writer(buf, lineterminator="\r\n" if crlf else "\n")
    w.writerow(head)
    for r in rows:
        w.writerow(r)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(buf.getvalue())
    return len(rows)


def edge(v, unit):
    c = round(v / unit) * unit
    return unit / 2 - abs(v - c)
