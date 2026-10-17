"""task154 constants and helpers shared by every generator module.

Tarbert Bank's economics desk sends its call on the Statistics Office's advance estimate of June-quarter 2026 GDP
growth to the bank's markets floor and, in a one-page preview, to clients at 18:00 on Wednesday 29 July 2026, the
evening before the release. Trade and Business Statistics' June bulletin of merchandise trade and business stocks,
due on Wednesday 22 July, was delayed by an outage of its processing system and came out on Tuesday 28 July as a PDF.
The world's master seed is the task number, fixed before any record was drawn; every stream below derives from it."""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import io
import math

import numpy as np

SEED = 154

OFFICE = "Statistics Office"
TBS = "Trade and Business Statistics"
TBS_DEPT = "Department of Industry"
RESERVE = "Reserve Bank"
BANK = "Tarbert Bank"
DESK = "Tarbert Economics"
POLL = "Harbourline economists' poll"
WIRE = "Harbourline"

PEOPLE = {
    "economist": "Nicola Jones",      # senior economist, Tarbert Economics; the preview's author (not in the prompt)
    "chief": "Garry Greenwood",       # Tarbert's chief economist
    "analyst": "Jodie Ford",          # economics data analyst, keeps the tracker and the desk's data folder
    "office": "Yvonne Mitchell",      # the Statistics Office's national accounts release contact
    "tbs": "Bryan O'Brien",           # Trade and Business Statistics, the bulletin's contact
    "poll": "Josh Dean",              # compiles the Harbourline poll
}

# ---------------------------------------------------------------------------------------------------- the calendar
D_Q1_THIRD = dt.date(2026, 6, 25)       # the Office's March-quarter third estimate
D_MAY_BULLETIN = dt.date(2026, 6, 23)   # TBS's May bulletin
D_PORTAL_PULL = dt.date(2026, 6, 24)    # the desk's last pull from TBS's portal
D_DB_PULL = dt.date(2026, 6, 26)        # the desk's download of the Office's real-time database
D_PRICES = dt.date(2026, 7, 16)         # producer and trade price indexes, June 2026
D_OUTAGE = dt.date(2026, 7, 13)         # TBS's processing system and portal down
D_ANNUAL = dt.date(2026, 7, 21)         # the Office's annual national accounts, with revised quarterly series
D_JUNE_DUE = dt.date(2026, 7, 22)       # the June bulletin's scheduled date
D_POLL = dt.date(2026, 7, 23)           # the poll closed at 17:00
D_NOTICE = dt.date(2026, 7, 24)         # the Office's notice
D_TRACKER = dt.date(2026, 7, 28)        # the tracker as at 08:00, before the bulletin
D_JUNE_BULLETIN = dt.date(2026, 7, 28)  # the June bulletin, 11:00
D_CALL = dt.date(2026, 7, 29)           # the desk files at 18:00
D_ADVANCE = dt.date(2026, 7, 30)        # the Office's advance estimate, 10:45

MONTHS0 = "2017-07"                     # the generator's first month (book-value windows reach back before 2018)
PRICE0 = "2018-01"                      # the first month the price indexes ship
Q0 = "2018Q1"                           # the first quarter of the national accounts history
SHIP0 = "2019-01"                       # the first month the shipped monthly files carry
LAST = "2026-06"

# the bulletin's industries: TBS code, name, end-March 2026 book value ($m), mean stock-to-sales ratio (months),
# share of the industry's input prices that moves with import prices
INDUSTRIES = [
    ("WFG", "Wholesale: food, grocery and liquor", 3150.0, 0.85, 0.15),
    ("WFP", "Wholesale: fuel and petroleum products", 1620.0, 0.50, 0.95),
    ("WME", "Wholesale: machinery and equipment", 7050.0, 2.25, 0.80),
    ("WMV", "Wholesale: motor vehicles and parts", 3620.0, 2.00, 0.85),
    ("WOT", "Wholesale: building, household and other goods", 5300.0, 1.75, 0.50),
    ("RFD", "Retail: food and groceries", 2080.0, 0.80, 0.15),
    ("ROT", "Retail: other goods", 8600.0, 1.80, 0.55),
    ("MFG", "Manufacturing", 14100.0, 1.10, 0.40),
]
IND_CODES = [c for c, *_ in INDUSTRIES]

SITC = [
    ("0", "Food and live animals"),
    ("1", "Beverages and tobacco"),
    ("2", "Crude materials, inedible, except fuels"),
    ("3", "Mineral fuels, lubricants and related materials"),
    ("4", "Animal and vegetable oils, fats and waxes"),
    ("5", "Chemicals and related products"),
    ("6", "Manufactured goods classified chiefly by material"),
    ("7", "Machinery and transport equipment"),
    ("8", "Miscellaneous manufactured articles"),
    ("9", "Commodities and transactions not classified elsewhere"),
]
SITC_CODES = [s for s, _ in SITC]


# ---------------------------------------------------------------------------------------------------- helpers
def rng(*keys):
    """An independent numpy stream per name: blake2b of the seed and the keys (hash() is salted per process)."""
    h = hashlib.blake2b(("%d|" % SEED + "|".join(str(k) for k in keys)).encode(), digest_size=8).digest()
    return np.random.default_rng(int.from_bytes(h, "big"))


def token(*keys, n=12):
    return hashlib.blake2b(("%d|" % SEED + "|".join(str(k) for k in keys)).encode(), digest_size=16).hexdigest()[:n]


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


def round_half_up(x, nd=0):
    q = x * 10 ** nd
    return math.floor(q + 0.5 + 1e-12) / 10 ** nd


def bin_clearance(x, step):
    """Distance from x to the nearest rounding edge of its step-wide bin, as a share of the step (0.5 is mid-bin)."""
    q = x / step
    return 0.5 - abs(q - math.floor(q + 0.5))


def month_list(a, b):
    """'2019-01' .. '2026-06' inclusive, as strings."""
    y, m = int(a[:4]), int(a[5:7])
    yb, mb = int(b[:4]), int(b[5:7])
    out = []
    while (y, m) <= (yb, mb):
        out.append("%04d-%02d" % (y, m))
        m += 1
        if m == 13:
            y, m = y + 1, 1
    return out


def quarter_of(month):
    y, m = int(month[:4]), int(month[5:7])
    return "%dQ%d" % (y, (m - 1) // 3 + 1)


def quarter_months(q):
    y, n = int(q[:4]), int(q[-1])
    return ["%04d-%02d" % (y, 3 * (n - 1) + k) for k in (1, 2, 3)]


def quarter_end(q):
    return quarter_months(q)[-1]


def prev_quarter(q):
    y, n = int(q[:4]), int(q[-1])
    return "%dQ%d" % (y - 1, 4) if n == 1 else "%dQ%d" % (y, n - 1)


def quarter_list(a, b):
    out, q = [], a
    while True:
        out.append(q)
        if q == b:
            return out
        y, n = int(q[:4]), int(q[-1])
        q = "%dQ%d" % (y + 1, 1) if n == 4 else "%dQ%d" % (y, n + 1)


MONTH_NAMES = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
               "November", "December"]
MON3 = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
QNAME = {1: "March", 2: "June", 3: "September", 4: "December"}


def long_date(d):
    """29 July 2026."""
    return "%d %s %d" % (d.day, MONTH_NAMES[d.month], d.year)


def day_date(d):
    """Wednesday 29 July 2026."""
    return "%s %d %s %d" % (d.strftime("%A"), d.day, MONTH_NAMES[d.month], d.year)


def qlabel(q):
    """2026Q2 -> June 2026 quarter."""
    return "%s %s quarter" % (QNAME[int(q[-1])], q[:4])


def annualise(q_pct):
    """A quarterly percentage change as a compound annual rate, per cent."""
    return ((1.0 + q_pct / 100.0) ** 4 - 1.0) * 100.0


def window_avg(p, m, T):
    """The average of the monthly indexes p over the T months ending with month index m: month m whole, then the
    months before it whole, then a fraction of the earliest (each month's index is its own average price)."""
    tot, rem, k = 0.0, float(T), m
    while rem > 1e-12:
        w = min(1.0, rem)
        tot += w * p[k]
        rem -= w
        k -= 1
    return tot / float(T)
