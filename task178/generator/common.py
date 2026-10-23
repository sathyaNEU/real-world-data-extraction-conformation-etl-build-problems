"""task178 shared constants: the pack's file names, the in-fiction calendar, the gauge's datums, the random streams and
the writers that make every file reproduce byte for byte."""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import io

import numpy as np

COMPANY = "Northfork Water Company"
DIVISION = "Water Resources"
GAUGE_ID = "TUM-02"
GAUGE = "Tumwick River near Sauer"
RIVER = "Tumwick River"

# ------------------------------------------------------------------------------------------------ the pack's files
F_PEAKS = "tum02_annual_peaks_wy1980-2015.csv"
F_STAGE = "tum02_stage_15min_wy2016-2025.csv"
F_MEAS_OLD = "tum02_measurement_notes_1980-2004.xlsx"
F_MEAS_NEW = "tum02_measurements_wy2005-2025.csv"
F_STATION = "tum02_station_description.pdf"
F_LEVELS = "tum02_levels_log.txt"
F_VISITS = "tum02_site_visits_2016-2025.csv"
F_STANDARD = "nfw_design_standard_sec4_hydrology.pdf"
F_STUDY = "sauer_crossing_alternatives_study.pdf"
F_SCADA = "scada_sauer_crossing_2019-2025.csv"
F_WO = "cmms_work_orders_sauer_2019-2025.csv"
F_RAIN = "sauer_flats_plant_rain_daily_1980-2025.csv"
F_KESSEL = "mrt01_marten_creek_annual_peaks.csv"
F_DICT = "tum02_data_dictionary.xlsx"
ALL_FILES = (F_PEAKS, F_STAGE, F_MEAS_OLD, F_MEAS_NEW, F_STATION, F_LEVELS, F_VISITS, F_STANDARD, F_STUDY, F_SCADA,
             F_WO, F_RAIN, F_KESSEL, F_DICT)
DISTRACTORS = (F_RAIN, F_KESSEL)

# deliverables
G_BOOK = "sauer_crossing_design_flow.xlsx"
G_CHART = "sauer_crossing_frequency_curve.svg"

# --------------------------------------------------------------------------------------------- calendar and datums
WY_FIRST, WY_LAST = 1980, 2025
STAGE_WY = tuple(range(2016, 2026))          # the 15-minute export
REGISTER_WY = tuple(range(1980, 2016))       # the annual peak register
DATUM_CHANGE = dt.date(2009, 10, 1)          # gage datum lowered 2.00 ft
DATUM_SHIFT = 2.00                            # stage on the current datum = stage on the old datum + 2.00
DATUM_NAVD_NEW = 182.40                       # current gage datum, ft NAVD88
DATUM_NAVD_OLD = DATUM_NAVD_NEW + DATUM_SHIFT
ADCP_FROM = dt.date(2004, 10, 1)              # the measurement database from water year 2005
CMS_TO = dt.date(2014, 9, 30)                 # ADCP discharges exported in m3/s through water year 2014
CFS_PER_CMS = 35.3147
PULL = dt.datetime(2026, 1, 20, 9, 30)       # the pack assembled, local time
RADAR_INSTALL = dt.datetime(2019, 3, 12, 11, 0)
RADAR_FACE_INSTALL = 199.34                   # ft NAVD88, the sensor face as surveyed at install and set in SCADA
BRACKET_DATE = dt.datetime(2022, 11, 16, 13, 20)
RADAR_FACE_NEW = 199.84                       # the face after the bracket replacement (resurveyed 2023-05-03)
SCADA_UPGRADE = dt.datetime(2022, 6, 21, 10, 0)   # historian clock UTC before, local wall clock after
LOGGER_SWAP = dt.datetime(2025, 6, 11, 10, 40)
LOGGER_FIX = dt.datetime(2025, 8, 27, 11, 15)
LOGGER_OFFSET_ERR = 0.47
SOFFIT_OLD = 193.60                           # the existing pipe's soffit, ft NAVD88 (inspection report)
WORK_WINDOW = ((7, 15), (9, 15))              # in-water work window, local dates, inclusive
ASK_A_YEARS = tuple(range(2016, 2026))
ASK_B_WY = tuple(range(2020, 2026))
AEP = 0.01
REG_SKEW = 0.05
REG_SKEW_MSE = 0.302

# the waterway alternatives: name, discharge passed with the required clearance (cfs)
ALTERNATIVES = (("A", 10400), ("B", 11600), ("C", 12900), ("D", 14700), ("E", 16200), ("F", 17800), ("G", 19500))


def stream(name):
    h = int.from_bytes(hashlib.sha256(("task178v2/" + name).encode()).digest()[:8], "little")
    return np.random.default_rng(h)


def water_year(d):
    return d.year + 1 if d.month >= 10 else d.year


# --------------------------------------------------------------------------------- Pacific local time and DST
def _nth_sunday(y, m, n):
    d = dt.date(y, m, 1)
    while d.weekday() != 6:
        d += dt.timedelta(days=1)
    return d + dt.timedelta(days=7 * (n - 1))


def _last_sunday(y, m):
    d = dt.date(y, m + 1, 1) - dt.timedelta(days=1)
    while d.weekday() != 6:
        d -= dt.timedelta(days=1)
    return d


def dst_bounds_pst(y):
    """daylight time start and end as PST (standard) clock times: 02:00 PST on the start day, 01:00 PST on the end day"""
    if y >= 2007:
        a, b = _nth_sunday(y, 3, 2), _nth_sunday(y, 11, 1)
    else:
        a, b = _nth_sunday(y, 4, 1), _last_sunday(y, 10)
    return dt.datetime(a.year, a.month, a.day, 2), dt.datetime(b.year, b.month, b.day, 1)


def pst_to_local(t):
    a, b = dst_bounds_pst(t.year)
    return t + dt.timedelta(hours=1) if a <= t < b else t


def local_to_pst(t):
    a, b = dst_bounds_pst(t.year)
    u = t - dt.timedelta(hours=1)
    return u if a <= u < b else t


def pst_to_utc(t):
    return t + dt.timedelta(hours=8)


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
    """distance from v to the nearest rounding boundary at this unit (half a unit is mid-bin)"""
    c = round(v / unit) * unit
    return unit / 2 - abs(v - c)
