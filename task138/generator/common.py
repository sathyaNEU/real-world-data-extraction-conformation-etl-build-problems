"""task138 constants and helpers shared by every generator module.

Kestrel Bend Irrigation District (fictional), on the east side of California's San Joaquin Valley: nine laterals,
412 turnouts, about 600 fields of permanent crops, alfalfa and pasture, supplied through the Tolan Valley Canal by the
Tolan Valley Water Authority. The district orders its 2027 season's water by 1 February 2027 under its Water Order
Procedure."""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import io

import numpy as np

SEED = 1380206

# ---------------------------------------------------------------------------------------------------- calendar
WEATHER_START = dt.date(1995, 10, 1)
WEATHER_END = dt.date(2027, 1, 31)        # the record runs through the day before the order is due
WINTER_FULL = dt.date(2026, 1, 27)        # the 2025-26 winter's last rain before the 2026 season: every root zone full
DISTRICT_STATION_START = dt.date(2014, 4, 1)
SPLICE = dt.date(2014, 5, 1)              # WOP 6.1: station 39 to 30 April 2014, the District station from 1 May
REPLAY_YEARS = list(range(1997, 2027))    # WOP 2.3: the thirty weather years 1997 to 2026
ORDER_SEASON = 2027
SEASON_START = (2, 1)                     # 1 February
SEASON_END = (10, 31)                     # 31 October
REQUESTS_OPEN = dt.date(2026, 11, 16)
REQUESTS_CLOSE = dt.date(2027, 1, 15)
EXTRACT = dt.date(2027, 2, 1)             # the register, the requests and the orders as extracted
ORDER_DUE = dt.date(2027, 2, 1)
WOP_ADOPTED = dt.date(2019, 4, 16)
TABLES_ADOPTED = dt.date(2025, 12, 9)
METER_BOOK_CLOSED = dt.date(2026, 11, 30)
REALIGN = dt.date(2026, 6, 15)            # the Lateral 5 tail reach served from Lateral 6 from this read
ORDER_SEASONS = [2023, 2024, 2025, 2026]
REMAP = dt.date(2025, 3, 3)               # field register re-mapped after parcel splits (new field ids)
MAG_PROGRAM = dt.date(2025, 2, 10)        # magnetic meters installed (read in hundreds of cubic feet)

# ---------------------------------------------------------------------------------------------------- names
DISTRICT = "Kestrel Bend Irrigation District"
DISTRICT_SHORT = "KBID"
AUTHORITY = "Tolan Valley Water Authority"
PROJECT = "Tolan Valley Project"
CANAL = "Tolan Valley Canal"
STATION39 = "Station 39"
STATION39_NAME = "Kestrel Bend South"     # the state network station, about six miles south-west of the yard
DISTRICT_STATION = "KBID yard station"

PEOPLE = {
    "requester": "Sherry Nixon",          # Water Resources Manager (orders the supply)
    "gm": "Brittany Wall",                # General Manager (signs the procedure's tables)
    "watermaster": "Colleen Ramsey",      # Water Master (riders, meter book, tail weir sheets)
    "scada": "Dennis Zhang",              # SCADA and Instrumentation Technician (flumes, the yard station)
    "engineer": "Travis Grimes",          # District Engineer (structures, the Lateral 5 to 6 connector)
    "authority": "Adam Arnold",           # Water Accounting, Tolan Valley Water Authority
    "conservation": "Kristin Lucas",      # Water Conservation Coordinator (requests, crop report)
}

LATERALS = ["L1", "L2", "L3", "L4", "L5", "L6", "L7", "L8", "L9"]
LATERAL_NAME = {l: "Lateral %s" % l[1:] for l in LATERALS}
# turnouts numbered on each lateral as built; the Lateral 5 tail turnouts keep their 5-numbers after the realignment
TURNOUTS_PER_LATERAL = {"L1": 52, "L2": 48, "L3": 38, "L4": 55, "L5": 58, "L6": 40, "L7": 41, "L8": 36, "L9": 44}
MOVED = ["05-%03d" % k for k in range(21, 35)]   # the Lateral 5 west spur, served from Lateral 6 from REALIGN
ROUTE_DAY = {"L1": 0, "L2": 1, "L3": 2, "L4": 3, "L5": 0, "L6": 1, "L7": 2, "L8": 3, "L9": 4}  # weekday of the read

# ---------------------------------------------------------------------------------------------------- the procedure's tables
CROPS = ["ALM", "PIS", "WAL", "GRW", "CIT", "ALF", "PAS"]
CROP_NAME = {"ALM": "Almonds", "PIS": "Pistachios", "WAL": "Walnuts", "GRW": "Wine grapes", "CIT": "Citrus (oranges)",
             "ALF": "Alfalfa", "PAS": "Irrigated pasture"}
# Table 1: crop coefficient by calendar month (January to December)
KC = {
    "ALM": [0.40, 0.40, 0.62, 0.80, 0.94, 1.08, 1.14, 1.14, 1.04, 0.82, 0.60, 0.42],
    "PIS": [0.22, 0.22, 0.30, 0.58, 0.90, 1.10, 1.18, 1.18, 1.00, 0.72, 0.42, 0.22],
    "WAL": [0.30, 0.30, 0.42, 0.70, 0.95, 1.11, 1.15, 1.15, 1.04, 0.81, 0.50, 0.30],
    "GRW": [0.20, 0.20, 0.25, 0.40, 0.60, 0.74, 0.80, 0.80, 0.70, 0.50, 0.32, 0.20],
    "CIT": [0.64, 0.64, 0.65, 0.66, 0.66, 0.66, 0.66, 0.66, 0.66, 0.66, 0.65, 0.64],
    "ALF": [0.60, 0.70, 0.85, 0.95, 1.00, 1.00, 1.00, 0.96, 0.95, 0.86, 0.72, 0.60],
    "PAS": [0.85, 0.86, 0.90, 0.95, 1.00, 1.00, 1.00, 1.00, 0.96, 0.90, 0.86, 0.85],
}
ROOT_FT = {"ALM": 4.5, "PIS": 5.5, "WAL": 5.5, "GRW": 4.5, "CIT": 4.5, "ALF": 5.5, "PAS": 2.5}   # Table 2
MAD = {"ALM": 0.45, "PIS": 0.45, "WAL": 0.45, "GRW": 0.35, "CIT": 0.45, "ALF": 0.55, "PAS": 0.55}  # Table 2
# Table 3: soil map units (symbol: name, available water capacity in/ft, depth limit ft or None)
SOILS = {
    "128": ("Hanford sandy loam, 0 to 2 percent slopes", 1.25, None),
    "141": ("Exeter loam, 0 to 2 percent slopes", 1.65, 3.3),
    "150": ("Tujunga loamy sand, 0 to 2 percent slopes", 0.85, None),
    "163": ("Greenfield sandy loam, 0 to 2 percent slopes", 1.45, None),
    "175": ("San Joaquin loam, 0 to 2 percent slopes", 1.75, 2.3),
}
# Tables 2 and 3 are the District's planning values. Every root zone's allowable depletion in inches is an odd number of
# hundred-thousandths (allowable depletion fraction, capacity and rooting depth each an odd number of their last unit),
# so no day's depletion, on any station's reported decimals, can land exactly on it.
SOIL_P = [0.30, 0.18, 0.15, 0.27, 0.10]
METHODS = ["Drip", "Micro-sprinkler", "Sprinkler", "Border"]
EA = {"Drip": 0.90, "Micro-sprinkler": 0.85, "Sprinkler": 0.75, "Border": 0.70}                   # Table 4
METHOD_BY_CROP = {"ALM": ["Micro-sprinkler", "Drip"], "PIS": ["Drip", "Micro-sprinkler"],
                  "WAL": ["Micro-sprinkler", "Border"], "GRW": ["Drip"], "CIT": ["Micro-sprinkler", "Drip"],
                  "ALF": ["Border", "Sprinkler"], "PAS": ["Border", "Sprinkler"]}
CROP_SHARE = {"ALM": 0.33, "PIS": 0.14, "WAL": 0.08, "GRW": 0.12, "CIT": 0.08, "ALF": 0.15, "PAS": 0.10}
# Table 5: loss allowances (share of the water put into the lateral; the main canal's of the headgate diversion)
LOSS = {"L1": 0.072, "L2": 0.105, "L3": 0.066, "L4": 0.138, "L5": 0.091, "L6": 0.118, "L7": 0.083, "L8": 0.097,
        "L9": 0.126}
MAIN_LOSS = 0.042

# How the growers run their water (never shipped). Border growers water a field when it has dried to their own
# threshold and run the set until the field is full. Drip, micro-sprinkler and sprinkler growers hold a working
# deficit: each set puts back about what the crop used since the last one, so the field stays near the grower's target
# depletion (a share of its total available water) and is not taken back to field capacity; the targets rise through
# the regulated-deficit stages (almond hull split, pistachio shell hardening, wine grapes after fruit set).
REFILL_METHODS = ("Border",)
TARGET = {   # share of total available water after a set, January to December
    "ALM": [0.20, 0.20, 0.20, 0.20, 0.25, 0.25, 0.44, 0.44, 0.36, 0.36, 0.36, 0.36],
    "PIS": [0.20, 0.20, 0.20, 0.22, 0.44, 0.44, 0.26, 0.26, 0.40, 0.40, 0.40, 0.40],
    "WAL": [0.15, 0.15, 0.15, 0.15, 0.18, 0.18, 0.20, 0.20, 0.26, 0.26, 0.26, 0.26],
    "GRW": [0.20, 0.20, 0.20, 0.20, 0.22, 0.46, 0.46, 0.46, 0.42, 0.42, 0.42, 0.42],
    "CIT": [0.28, 0.28, 0.28, 0.28, 0.30, 0.30, 0.32, 0.32, 0.34, 0.34, 0.34, 0.34],
    "ALF": [0.20, 0.20, 0.20, 0.20, 0.20, 0.20, 0.20, 0.20, 0.22, 0.22, 0.22, 0.22],
    "PAS": [0.20, 0.20, 0.20, 0.20, 0.20, 0.20, 0.20, 0.20, 0.22, 0.22, 0.22, 0.22],
}
TRIGGER_IN = {"Drip": (0.30, 0.50), "Micro-sprinkler": (0.45, 0.75), "Sprinkler": (0.60, 0.95)}
FLOW_PER_ACRE = {"Drip": (0.024, 0.034), "Micro-sprinkler": (0.030, 0.044), "Sprinkler": (0.050, 0.070),
                 "Border": (0.14, 0.20)}
MAX_SET_HOURS = {"Drip": 60.0, "Micro-sprinkler": 48.0, "Sprinkler": 48.0, "Border": 40.0}

# each crop's 2026 last set after harvest (month, day) to (month, day)
LAST_SET_WINDOW = {"ALM": ((9, 4), (9, 28)), "PIS": ((9, 24), (10, 14)), "WAL": ((9, 17), (10, 8)),
                   "GRW": ((9, 1), (9, 24)), "CIT": ((10, 10), (10, 28)), "ALF": ((9, 20), (10, 10)),
                   "PAS": ((10, 6), (10, 28))}

# ---------------------------------------------------------------------------------------------------- the pack
WOP_PDF = "KBID_Water_Order_Procedure_rev2025.pdf"
WOP_TABLES = "KBID_WOP_tables_2027_order.xlsx"
REQUESTS = "kbid_water_requests_2027.xlsx"
REGISTER = "kbid_field_register_2027-02-01.csv"
ST39 = "station39_daily_1995-2027.csv"
YARD = "kbid_station_daily_2014-2027.csv"
ORDERS = "kbid_irrigation_orders_2023-2026.csv"
METER_BOOK = "kbid_meter_book_2026.csv"
SHOP_LOG = "kbid_meter_shop_log_2026.xlsx"
HEADINGS = "kbid_lateral_headings_daily_2026.csv"
WEIRS = "kbid_tail_weir_sheets_2026.csv"
STRUCTURES = "kbid_canal_structures.xlsx"
OPS_LOG = "kbid_canal_operations_log_2026.docx"
DICTIONARY = "kbid_data_dictionary.xlsx"
README = "README_order_working_files.txt"
GROUNDWATER = "kbid_groundwater_levels_2016-2026.csv"
CROP_REPORT = "kbid_crop_report_2026.csv"
NOTICE = "TVWA_2027_initial_allocation_notice.pdf"
DISTRACTORS = [GROUNDWATER, CROP_REPORT, NOTICE]

GOLD_BOOK = "kbid_order_2027.xlsx"
GOLD_CHART = "kbid_order_2027.svg"

AF_PER_CFS_DAY = 1.983471     # 86,400 cubic feet over 43,560
CUFT_PER_AF = 43560.0


def rng(*keys):
    """An independent numpy stream per name: blake2b of the seed and the keys (hash() is salted per process)."""
    h = hashlib.blake2b(("%d|" % SEED + "|".join(str(k) for k in keys)).encode(), digest_size=8).digest()
    return np.random.default_rng(int.from_bytes(h, "big"))


def daterange(a, b):
    d = a
    while d <= b:
        yield d
        d += dt.timedelta(days=1)


def season_days(year):
    return list(daterange(dt.date(year, *SEASON_START), dt.date(year, *SEASON_END)))


def write_csv(path, cols, rows, crlf=False):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\r\n" if crlf else "\n")
    w.writerow(cols)
    n = 0
    for r in rows:
        w.writerow(["" if r.get(c) is None else r.get(c) for c in cols] if isinstance(r, dict) else r)
        n += 1
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(buf.getvalue())
    return n


def ceil_hundred(x):
    import math
    return int(math.ceil(x / 100.0 - 1e-12) * 100)


ORDER_STEP = 1000      # WOP 2.3: the order in whole thousands of acre-feet
MONTH_STEP = 100       # WOP 5.1: each month to the nearest 100 acre-feet


def ceil_to(x, step):
    import math
    return int(math.ceil(x / float(step) - 1e-12) * step)


def round_to(x, step):
    """Round half away from zero to a multiple of step (the deliverables' convention)."""
    import math
    q = x / step
    return int(math.floor(q + 0.5)) * step if q >= 0 else -int(math.floor(-q + 0.5)) * step
