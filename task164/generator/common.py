"""task164 constants and helpers shared by every generator module.

Calloway Valley Power Company is an investor-owned electric utility serving the Calloway Valley and the Sierra
foothills above it through twelve operating districts. The Commission's decision of 12 November 2026 approved 400
proactive replacements of single-phase residential service transformers for 2027, allocated across the districts in
proportion to each district's forecast count of transformers at risk of summer overload. The compliance filing is due
Friday 30 April 2027; its record date is Wednesday 31 March 2027; the program team pulled every extract on Monday
5 April 2027.

The seed was fixed by rule before any data was generated: the task number, then the as-of month and day."""
from __future__ import annotations

import datetime as dt
import os
import zlib

import numpy as np

SEED = 1640405

ORG = "Calloway Valley Power Company"
ORG_SHORT = "Calloway Valley Power"
PEOPLE = {
    "planning": "Megan Stewart",          # Distribution Planning: the transformer load management extract
    "load_research": "Christopher Richardson",   # Load Research: the EV charging study
    "compliance": "Katelyn Duarte",       # Regulatory Compliance: the decision excerpt, the filing tables
    "construction": "Antonio Morgan",     # Construction Services: the 2025-26 pilot's work orders
}

HERE = os.path.dirname(os.path.abspath(__file__))
TASK_DIR = os.path.dirname(HERE)
TARGET = os.path.join(TASK_DIR, "target")

# ------------------------------------------------------------------------------------------------- calendar
DECISION_DATE = dt.date(2026, 11, 12)
RECORD_DATE = dt.date(2027, 3, 31)
AS_OF = dt.date(2027, 4, 5)
FILING_DUE = dt.date(2027, 4, 30)
SUMMERS = (2024, 2025, 2026)
NDAY = 122                                        # 1 June to 30 September
HEAT = {2024: (dt.date(2024, 7, 8), 6), 2025: (dt.date(2025, 8, 18), 5), 2026: (dt.date(2026, 9, 2), 7)}
PILOT_START, PILOT_END = dt.date(2025, 10, 6), dt.date(2026, 4, 24)
DRIVE_START, DRIVE_END = dt.date(2026, 11, 2), dt.date(2027, 2, 19)     # EV-rate enrollment drive
FLEET_START = dt.date(2018, 1, 2)

PF = 0.95                                         # planning power factor, kW to kVA
THRESH = 1.2                                      # at risk above 1.2 times nameplate
TOTAL = 400
T = 20                                            # quarter hours ending 16:15 ... 21:00
QSTART = 16.0 + 0.25 * np.arange(T)               # start hour of each quarter hour in the window
QMID = QSTART + 0.125

SIZES = (10.0, 15.0, 25.0, 37.5, 50.0, 75.0, 100.0)
PREM = {10.0: (1, 2), 15.0: (2, 3), 25.0: (3, 6), 37.5: (5, 8), 50.0: (6, 10), 75.0: (9, 14), 100.0: (12, 18)}
SIZE_GROUP = {10.0: "S", 15.0: "S", 25.0: "M", 37.5: "M", 50.0: "L", 75.0: "L", 100.0: "L"}

RATE_TOU, RATE_CARE, RATE_EV, RATE_FLAT = "R-TOU4", "R-TOU4C", "R-EV2", "R-1"

# name, code, n_tx, size mix (10, 15, 25, 37.5, 50, 75, 100), loading (mean, sd), vehicles per premise mid-2024,
# growth per premise per year, clustering, P(EV rate when a premise's first vehicle arrives), forward vehicles per
# premise (October to March), forward clustering, temperature offset F, share of default-rate vehicle premises the
# winter enrollment drive moves to the EV rate, departures per vehicle-year, CARE share of premises
DISTRICTS = [
    ("Foothill",   "FH", 5183, (.34, .36, .24, .05, .01, 0, 0),  (0.75, .15), .028, .026, 0.2, .22, .052, 0.1, -2.0, 0.00, .110, .30),
    ("Railyard",   "RY", 4617, (.03, .17, .55, .17, .06, .02, 0), (0.88, .14), .028, .014, 0.2, .26, .022, 0.2, 1.0, 0.00, .120, .34),
    ("Canal",      "CN", 4092, (.03, .14, .52, .21, .08, .02, 0), (0.86, .14), .026, .013, 0.2, .25, .020, 0.2, 1.5, 0.00, .120, .31),
    ("Mission",    "MS", 4306, (.02, .10, .42, .26, .15, .05, 0), (0.81, .14), .040, .016, 0.3, .40, .021, 0.3, 0.5, 0.20, .110, .22),
    ("West Bluff", "WB", 3874, (.02, .12, .45, .24, .12, .05, 0), (0.80, .14), .034, .014, 0.3, .38, .020, 0.3, 0.0, 0.18, .110, .21),
    ("Crestview",  "CR", 5021, (0, .02, .10, .18, .38, .27, .05), (0.67, .13), .110, .028, 0.5, .72, .017, 0.4, -1.0, 0.00, .090, .06),
    ("Lakeside",   "LK", 4488, (0, .02, .12, .22, .36, .24, .04), (0.66, .13), .095, .026, 0.5, .70, .017, 0.4, -0.5, 0.00, .090, .07),
    ("Sunrise",    "SR", 4335, (0, .04, .20, .26, .30, .17, .03), (0.71, .13), .070, .021, 0.4, .58, .018, 0.4, 0.5, 0.20, .100, .12),
    ("Sandhill",   "SH", 4229, (.20, .30, .33, .12, .04, .01, 0), (0.77, .15), .026, .024, 0.2, .22, .048, 0.1, 2.0, 0.00, .110, .33),
    ("Kingsley",   "KG", 3962, (.03, .12, .44, .24, .12, .05, 0), (0.82, .14), .045, .016, 0.3, .42, .021, 0.3, 1.0, 0.22, .110, .20),
    ("Highland",   "HL", 3791, (0, .05, .22, .28, .28, .15, .02), (0.68, .13), .085, .024, 0.5, .68, .017, 0.4, -1.5, 0.00, .090, .08),
    ("Brookside",  "BK", 3917, (.06, .20, .47, .18, .07, .02, 0), (0.87, .14), .024, .012, 0.2, .24, .024, 0.2, 1.5, 0.00, .120, .32),
]
NAMES = [d[0] for d in DISTRICTS]
CODES = {d[0]: d[1] for d in DISTRICTS}
PILOT_DISTRICTS = ("Railyard", "Canal", "Brookside")
DRIVE_DISTRICTS = tuple(d[0] for d in DISTRICTS if d[12] > 0)

# owner habits: P(starts on arrival), P(timer at 21:00); the rest timer at 00:00
BEH = {"TOU": (0.75, 0.25), "EV": (0.00, 0.15)}
SLIP = {"TOU": 0.03, "EV": 0.01}                  # timer sessions started on arrival anyway


def rng(*key):
    """One independent stream per component, district and year: a change in one never re-rolls another."""
    return np.random.default_rng([SEED] + [zlib.crc32(k.encode()) if isinstance(k, str) else int(k) for k in key])


def summer_start(year):
    return dt.date(year, 6, 1)


def day_of(year, i):
    return summer_start(year) + dt.timedelta(days=int(i))


def q_end(year, day_index, q):
    """The interval-ending timestamp (local, naive) of quarter hour q on summer day day_index."""
    d = day_of(year, day_index)
    minutes = 16 * 60 + 15 * (q + 1)
    return dt.datetime(d.year, d.month, d.day) + dt.timedelta(minutes=minutes)


def behaviour_class(rate):
    return "EV" if rate == RATE_EV else "TOU"
