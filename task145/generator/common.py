"""task145 constants and helpers shared by every generator module.

Larchwood Express Canada Ltd. is an express carrier whose inbound international shipments arrive at five import
gateways (Mississauga YYZ, Dorval YUL, Richmond YVR, Calgary YYC, Winnipeg YWG). Its clearance system values each
shipment on its commercial invoice in the invoice currency, converts it at the customs exchange rate of its date and
routes it to the gateway's brokerage desk for a formal entry when the value for duty exceeds CAD 3,300 or the goods are
under another government department's (OGD) program; everything else is released under the courier low-value program
(CLVS). The brokerage staffing standard BRK-STD-03 places six new broker posts for 2027 on each gateway's forecast
formal entries per broker post, made on the 2027 network plan (its volumes and its planning rates)."""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import io
import math

import numpy as np

SEED = 1451015

# ---------------------------------------------------------------------------------------------------- the gateways
GATEWAYS = ["YYZ", "YUL", "YVR", "YYC", "YWG"]
DESK = {"YYZ": "Mississauga", "YUL": "Dorval", "YVR": "Richmond", "YYC": "Calgary", "YWG": "Winnipeg"}
PLAN_REGION = {"YYZ": "Ontario (YYZ)", "YUL": "Quebec and Atlantic (YUL)", "YVR": "British Columbia (YVR)",
               "YYC": "Alberta (YYC)", "YWG": "Manitoba and Saskatchewan (YWG)"}
PROVINCE = {"YYZ": "ON", "YUL": "QC", "YVR": "BC", "YYC": "AB", "YWG": "MB"}
TZ = {"YYZ": "America/Toronto", "YUL": "America/Toronto", "YVR": "America/Vancouver", "YYC": "America/Edmonton",
      "YWG": "America/Winnipeg"}
STD_OFFSET = {"YYZ": -5, "YUL": -5, "YVR": -8, "YYC": -7, "YWG": -6}     # hours from UTC in winter

ESTABLISHMENT = {"YYZ": 7, "YUL": 5, "YVR": 6, "YYC": 4, "YWG": 3}       # broker posts at 1 January 2027
NEW_POSTS = 6
STANDARD_LOAD = 560          # BRK-STD-03: a post is placed while the highest load exceeds this
LINE_CAD = 3300.0            # a shipment over this value for duty goes to a formal entry
CHECK_FLOOR_CAD = 2500.0     # the high-value check covers every shipment from this value for duty, and every OGD one

# ---------------------------------------------------------------------------------------------------- calendar
HIST_START = dt.date(2021, 1, 1)
HIST_END = dt.date(2026, 9, 30)
BASE_START = dt.date(2025, 10, 1)        # the network plan's base: the twelve months to September 2026
BASE_END = dt.date(2026, 9, 30)
PLAN_YEAR = 2027
LEGACY_REPORT_END = dt.date(2024, 9, 30)  # the legacy brokerage system's monthly report runs to here
LAYOUT_CHANGE = dt.date(2026, 2, 17)      # the clearance system release that changed the extract layout
PLAN_ISSUED = dt.date(2026, 9, 18)
PULL = dt.date(2026, 10, 7)               # clearance extracts and the gateway report pulled
REVIEW = dt.date(2026, 10, 22)            # the establishment review
REQUEST = dt.date(2026, 10, 13)
FY_START = dt.date(2025, 4, 1)            # the asks: fiscal 2025-26
FY_END = dt.date(2026, 3, 31)
TA_MIGRATION = dt.date(2025, 11, 1)       # the new time and attendance system from this day


def months(start, end):
    out, y, m = [], start.year, start.month
    while (y, m) <= (end.year, end.month):
        out.append((y, m))
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    return out


HIST_MONTHS = months(HIST_START, HIST_END)        # 69 months
BASE_MONTHS = months(BASE_START, BASE_END)        # 12 months
PLAN_MONTHS = [(PLAN_YEAR, m) for m in range(1, 13)]


def days_in(y, m):
    nxt = dt.date(y + (m == 12), m % 12 + 1, 1)
    return (nxt - dt.date(y, m, 1)).days


def fiscal_quarter(d):
    """Larchwood's fiscal year runs April to March: FQ1 April to June ... FQ4 January to March."""
    return {4: 1, 5: 1, 6: 1, 7: 2, 8: 2, 9: 2, 10: 3, 11: 3, 12: 3, 1: 4, 2: 4, 3: 4}[d.month]


# ---------------------------------------------------------------------------------------------------- exchange rates
CURRENCIES = ["USD", "EUR", "GBP", "CNY", "JPY", "CAD"]
# monthly average customs rates, CAD per unit, January 2021 to September 2026 (69 months)
USD_M = [1.274, 1.270, 1.262, 1.249, 1.212, 1.226, 1.252, 1.260, 1.268, 1.247, 1.265, 1.276,
         1.272, 1.267, 1.264, 1.262, 1.278, 1.282, 1.291, 1.300, 1.333, 1.373, 1.355, 1.360,
         1.352, 1.336, 1.357, 1.352, 1.346, 1.322, 1.320, 1.351, 1.353, 1.371, 1.375, 1.335,
         1.342, 1.349, 1.355, 1.368, 1.367, 1.370, 1.375, 1.364, 1.352, 1.376, 1.395, 1.417,
         1.436, 1.432, 1.433, 1.406, 1.385, 1.369, 1.371, 1.382, 1.384, 1.400, 1.408, 1.399,
         1.392, 1.401, 1.410, 1.418, 1.427, 1.421, 1.412, 1.419, 1.423]
EUR_M = [1.545, 1.538, 1.506, 1.502, 1.483, 1.475, 1.483, 1.481, 1.490, 1.444, 1.443, 1.444,
         1.445, 1.440, 1.409, 1.367, 1.357, 1.360, 1.320, 1.313, 1.323, 1.351, 1.383, 1.448,
         1.448, 1.439, 1.457, 1.488, 1.457, 1.446, 1.465, 1.476, 1.453, 1.479, 1.488, 1.476,
         1.463, 1.459, 1.470, 1.479, 1.483, 1.476, 1.495, 1.505, 1.501, 1.502, 1.465, 1.483,
         1.490, 1.494, 1.553, 1.571, 1.562, 1.574, 1.586, 1.581, 1.596, 1.596, 1.588, 1.603,
         1.594, 1.601, 1.612, 1.606, 1.598, 1.590, 1.584, 1.592, 1.597]
GBP_M = [1.742, 1.754, 1.748, 1.731, 1.712, 1.728, 1.739, 1.741, 1.744, 1.718, 1.692, 1.688,
         1.726, 1.716, 1.668, 1.638, 1.598, 1.590, 1.551, 1.547, 1.512, 1.548, 1.592, 1.659,
         1.668, 1.622, 1.651, 1.682, 1.672, 1.681, 1.702, 1.718, 1.691, 1.672, 1.709, 1.693,
         1.701, 1.704, 1.728, 1.722, 1.731, 1.749, 1.772, 1.788, 1.801, 1.812, 1.791, 1.802,
         1.789, 1.802, 1.842, 1.858, 1.861, 1.871, 1.862, 1.851, 1.858, 1.861, 1.870, 1.879,
         1.872, 1.884, 1.893, 1.889, 1.880, 1.874, 1.868, 1.877, 1.882]
USDCNY_M = [6.47] * 12 + [6.60] * 12 + [7.10] * 12 + [7.18] * 12 + [7.20] * 12 + [7.16] * 9
USDJPY_M = [108.0] * 12 + [128.0] * 12 + [140.0] * 12 + [151.0] * 12 + [150.0] * 12 + [151.5] * 9
# the network plan's planning rates for 2027 (Treasury), CAD per unit
PLAN_RATE = {"USD": 1.340, "EUR": 1.680, "GBP": 1.875, "CNY": 0.1880, "JPY": 0.009250, "CAD": 1.0}
RATE_DP = {"USD": 4, "EUR": 4, "GBP": 4, "CNY": 5, "JPY": 7, "CAD": 0}


def monthly_rate(cur, i):
    if cur == "CAD":
        return 1.0
    if cur == "USD":
        return USD_M[i]
    if cur == "EUR":
        return EUR_M[i]
    if cur == "GBP":
        return GBP_M[i]
    if cur == "CNY":
        return USD_M[i] / USDCNY_M[i]
    if cur == "JPY":
        return USD_M[i] / USDJPY_M[i]
    raise KeyError(cur)


# ---------------------------------------------------------------------------------------------------- the shipments
# Each gateway's inbound international shipments are a mix of segments, each a share of the gateway's shipments with a
# value distribution in its invoice currency: 'ln' lognormal (mu, sigma on the log of the value), 'pp' price points
# (single units at listed prices, weights). 'ogd' is the share of the segment's shipments whose goods fall under an OGD
# program (formal entry whatever the value); those carry values from the segment's 'ogd_ln' distribution.
SEGMENTS = {
    "YYZ": [
        dict(cur="USD", share=0.6822, kind="ln", p=(5.05, 1.30), ogd=0.0100, ogd_ln=(4.30, 1.10), lane="US"),
        dict(cur="EUR", share=0.0910, kind="ln", p=(5.30, 1.25), ogd=0.0300, ogd_ln=(4.40, 1.10), lane="EU"),
        dict(cur="GBP", share=0.0341, kind="ln", p=(5.20, 1.25), ogd=0.0200, ogd_ln=(4.30, 1.10), lane="GB"),
        dict(cur="CNY", share=0.1365, kind="ln", p=(7.30, 1.20), ogd=0.0080, ogd_ln=(6.30, 1.10), lane="CN"),
        dict(cur="CAD", share=0.0531, kind="ln", p=(5.40, 1.30), ogd=0.0120, ogd_ln=(4.60, 1.10), lane="US"),
        dict(cur="USD", share=0.0031, kind="pp", p=((2355, 2), (2359, 3), (2365, 3), (2369, 4), (2375, 4), (2379, 4),
                                                     (2385, 3), (2389, 3)), ogd=0.0, lane="US"),
    ],
    "YUL": [
        dict(cur="USD", share=0.4876, kind="ln", p=(5.00, 1.30), ogd=0.0120, ogd_ln=(4.30, 1.10), lane="US"),
        dict(cur="EUR", share=0.4089, kind="ln", p=(5.45, 1.20), ogd=0.0400, ogd_ln=(4.50, 1.10), lane="EU"),
        dict(cur="GBP", share=0.0511, kind="ln", p=(5.20, 1.25), ogd=0.0200, ogd_ln=(4.30, 1.10), lane="GB"),
        dict(cur="CAD", share=0.0472, kind="ln", p=(5.30, 1.30), ogd=0.0150, ogd_ln=(4.60, 1.10), lane="US"),
        dict(cur="EUR", share=0.0055, kind="pp", p=((2005, 3), (2009, 5), (2010, 3), (2015, 4), (2019, 6), (2020, 2),
                                                     (2025, 3), (2029, 2)), ogd=0.0, lane="EU"),
    ],
    "YVR": [
        dict(cur="USD", share=0.5665, kind="ln", p=(5.15, 1.25), ogd=0.0080, ogd_ln=(4.30, 1.10), lane="US"),
        dict(cur="CNY", share=0.3348, kind="ln", p=(7.35, 1.20), ogd=0.0060, ogd_ln=(6.30, 1.10), lane="CN"),
        dict(cur="JPY", share=0.0612, kind="ln", p=(11.95, 1.20), ogd=0.0100, ogd_ln=(11.00, 1.10), lane="JP"),
        dict(cur="CAD", share=0.0322, kind="ln", p=(5.30, 1.30), ogd=0.0100, ogd_ln=(4.60, 1.10), lane="US"),
        dict(cur="USD", share=0.0053, kind="pp", p=((2339, 3), (2345, 4), (2349, 6), (2355, 4), (2359, 5), (2365, 3),
                                                     (2369, 2)), ogd=0.0, lane="AS"),
    ],
    "YYC": [
        dict(cur="USD", share=0.9242, kind="ln", p=(5.45, 1.55), ogd=0.0100, ogd_ln=(4.40, 1.10), lane="US"),
        dict(cur="CAD", share=0.0758, kind="ln", p=(5.50, 1.40), ogd=0.0100, ogd_ln=(4.60, 1.10), lane="US"),
    ],
    "YWG": [
        dict(cur="USD", share=0.9163, kind="ln", p=(5.15, 1.35), ogd=0.0120, ogd_ln=(4.30, 1.10), lane="US"),
        dict(cur="USD", share=0.0035, kind="pp", p=((2365, 3), (2369, 4), (2375, 4), (2379, 3), (2385, 2), (2389, 2)),
             ogd=0.0, lane="US"),
        dict(cur="CAD", share=0.0802, kind="ln", p=(5.30, 1.30), ogd=0.0120, ogd_ln=(4.60, 1.10), lane="US"),
    ],
}
# inbound international shipments a month at the centre of the base year, before seasonality
BASE_LEVEL = {"YYZ": 114900, "YUL": 64800, "YVR": 74600, "YYC": 33500, "YWG": 41900}
TREND = {"YYZ": 0.035, "YUL": 0.040, "YVR": 0.050, "YYC": 0.025, "YWG": 0.030}       # a year, 2021 to 2026
SEASON = [0.90, 0.88, 0.98, 0.98, 1.00, 0.98, 0.96, 0.97, 1.00, 1.05, 1.15, 1.15]
# the 2027 network plan's growth on the twelve months to September 2026
PLAN_GROWTH = {"YYZ": 0.026, "YUL": 0.034, "YVR": 0.048, "YYC": 0.019, "YWG": 0.029}


def season(m):
    s = SEASON[m - 1]
    return s / (sum(SEASON) / 12.0)


# ---------------------------------------------------------------------------------------------------- helpers
def rng(*keys):
    """An independent numpy stream per name: blake2b of the seed and the keys (hash() is salted per process)."""
    h = hashlib.blake2b(("%d|" % SEED + "|".join(str(k) for k in keys)).encode(), digest_size=8).digest()
    return np.random.default_rng(int.from_bytes(h, "big"))


def write_csv(path, cols, rows, crlf=False, delimiter=","):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\r\n" if crlf else "\n", delimiter=delimiter)
    w.writerow(cols)
    n = 0
    for r in rows:
        w.writerow(["" if r.get(c) is None else r.get(c) for c in cols] if isinstance(r, dict) else r)
        n += 1
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(buf.getvalue())
    return n


def round_to(x, step):
    """Round half away from zero to a multiple of step (the deliverables' convention)."""
    q = x / step
    return int(math.floor(q + 0.5)) * step if q >= 0 else -int(math.floor(-q + 0.5)) * step


def round_dp(x, dp):
    f = 10 ** dp
    return math.floor(x * f + 0.5) / f if x >= 0 else -math.floor(-x * f + 0.5) / f


def phi(z):
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


# ---------------------------------------------------------------------------------------------------- people
COMPANY = "Larchwood Express Canada Ltd."
PEOPLE = {
    "planner": "Laura Parks",          # lead, brokerage workforce planning (the requester; not in the prompt)
    "vp": "Robin Larson",              # vice-president, trade and brokerage services, owner of BRK-STD-03
    "network": "Wanda Armstrong",      # manager, network planning (the network plan)
    "treasury": "Brian Stewart",       # treasury manager (the planning rates)
    "clearance": "Clémence Sirois",    # manager, clearance operations, Dorval (CLR-OPS-11)
    "hrsys": "Theresa Rowe",           # HR systems analyst (the time and attendance migration)
}
