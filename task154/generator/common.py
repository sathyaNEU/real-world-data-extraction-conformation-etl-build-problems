"""task154 constants and helpers shared by every generator module.

Brackenholt Spring Water bottles spring water at Brackenholt in the West Midlands of England from Borehole 2
(BH2), drilled in 2013 into the Sherwood Sandstone where it lies confined beneath the Mercia Mudstone. The licence
granted for the plant's opening (1,200 cubic metres a day from 1 April 2015) expires on 31 March 2027. In September
2026 the licensing team's pre-application letter set the derogation test for the renewal to the 2039 common end date
and for the variation the new line 5 needs. The world's master seed is the task number, fixed before any record was
drawn; every stream below derives from it."""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import io

import numpy as np

SEED = 154

COMPANY = "Brackenholt Spring Water Ltd"
SHORT = "Brackenholt Spring Water"
REGULATOR = "Water Resources Licensing, Mercia Area"
HAULIER = "Teme Valley Bulk Liquids"
BULK_CUSTOMER = "Ferncastle Foods"

PEOPLE = {
    "lead": "Francis Mason",        # water resources lead; keeps the licence file and the returns
    "site": "Dominic Schofield",    # site engineer; reads the meter and dips the observation boreholes
    "officer": "Wendy Hodgson",     # the licensing team's officer who signs the pre-application letter
    "previous": "William Swift",    # operations manager who signed the returns to 2018-19
}

# ------------------------------------------------------------------------------------------------- the calendar
LICENCE_NO = "MA/28/15/0042"
LICENCE_START = dt.date(2015, 4, 1)
LICENCE_END = dt.date(2027, 3, 31)
NEW_FROM = dt.date(2027, 4, 1)
COMMON_END = dt.date(2039, 3, 31)
LETTER_DATE = dt.date(2026, 9, 22)
APPLICATION_DUE = dt.date(2026, 12, 18)
EXPORT_DATE = dt.date(2026, 10, 2)          # the site's data pull for the application
NOTE_DATE = dt.date(2026, 11, 13)           # the variation note
TEST_START_UTC = dt.datetime(2014, 6, 10, 9, 0)    # pump on, 10:00 BST
TEST_PUMP_H = 72
TEST_RECOVERY_H = 48
TEST_PRE_H = 24
TEST_Q_LS = 25.0
LICENSED_QD = 1200.0                        # cubic metres a day
LICENSED_QA = 400000.0                      # cubic metres a year
APPLIED_QD = 1800.0
LINE4_FROM = dt.date(2024, 8, 5)
BULK_FROM = dt.date(2026, 4, 1)
OPS_FROM = dt.date(2025, 4, 1)              # the operational extracts start here
OPS_TO = dt.date(2026, 9, 30)               # and end here (inclusive)

# ------------------------------------------------------------------------------------------------- the aquifer
T_M2D = 205.0
S_CONF = 3.6e-4
STRIKE_DEG = 15.0                            # the Coldharbour Fault trends N15E
FAULT_DIST = 2500.0                          # BH2's perpendicular distance to the fault trace, metres
# British National Grid position of BH2 (the site's survey); the local frame is metres east and north of it
BH2_E, BH2_N = 384960.0, 341250.0


def normal():
    a = np.deg2rad(STRIKE_DEG)
    return np.array([np.cos(a), -np.sin(a)])


def image_xy():
    return 2.0 * FAULT_DIST * normal()


def fault_side(xy):
    """Signed distance from the fault trace, negative on BH2's side."""
    p0 = FAULT_DIST * normal()
    return float(np.dot(np.asarray(xy, float) - p0, normal()))


# boreholes in the local frame (metres east, north of BH2); ground and casing-top levels in metres above datum
OBS = {
    "OB1": dict(xy=(-160.0, 70.0), gl=96.42, ct=96.95, depth=120.0),
    "OB2": dict(xy=(-240.0, -410.0), gl=95.10, ct=95.58, depth=125.0),
    "OB3": dict(xy=(-860.0, 260.0), gl=99.37, ct=99.88, depth=120.0),
}
OB2_RAISE = dt.date(2020, 2, 18)             # headworks fitted, casing top raised
OB2_RAISE_M = 0.45
BH2 = dict(xy=(0.0, 0.0), gl=97.80, ct=98.31, depth=160.0)
RMB = dict(name="Windle Cross OBH", xy=(3300.0, -900.0), gl=91.05, ct=91.60, depth=410.0)
PROTECTED = [
    # name, licence, holder, local xy, available drawdown (m), rest level April 2015 (m above datum), licensed m3/d
    ("Lower Hay Farm", "MA/28/15/0117", "R. and J. Pryce", (2158.0, 405.0), 7.53, 88.62, 25.0),
    ("Kilnbrook Nurseries", "MA/28/15/0093", "Kilnbrook Nurseries Ltd", (-550.0, -300.0), 10.0, 89.94, 40.0),
    ("Hollin Bank Golf Club", "MA/28/15/0151", "Hollin Bank Golf Club", (300.0, 1300.0), 9.9, 89.31, 60.0),
]
PROT_NAMES = [p[0] for p in PROTECTED]
REST_2015 = 89.86                             # BH2's rest water level, April 2015, metres above datum


def rng(*keys):
    h = hashlib.sha256(("%d|" % SEED + "|".join(str(k) for k in keys)).encode()).digest()
    return np.random.default_rng(int.from_bytes(h[:8], "little"))


def token(*keys, n=12):
    return hashlib.sha256(("%d|" % SEED + "|".join(str(k) for k in keys)).encode()).hexdigest()[:n]


def write_csv(path, cols, rows, crlf=False):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\r\n" if crlf else "\n")
    w.writerow(cols)
    for r in rows:
        w.writerow(["" if v is None else v for v in r])
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(buf.getvalue())


def round_half_up(x, nd=0):
    q = 10 ** nd
    return float(np.floor(x * q + 0.5) / q)


def long_date(d):
    return "%d %s %d" % (d.day, d.strftime("%B"), d.year)


def bst(d):
    """True when the UK clock is on British Summer Time at local date-time d (last Sunday of March 01:00 UTC to last
    Sunday of October 01:00 UTC)."""
    y = d.year

    def last_sunday(month):
        x = dt.date(y, month, 31)
        return x - dt.timedelta(days=(x.weekday() + 1) % 7)
    start = dt.datetime.combine(last_sunday(3), dt.time(1, 0))
    end = dt.datetime.combine(last_sunday(10), dt.time(1, 0))
    return start <= d < end


def utc_to_local(t):
    return t + dt.timedelta(hours=1) if bst(t) else t


def local_to_utc(t):
    # local times inside the spring-forward gap do not occur in the records
    guess = t - dt.timedelta(hours=1)
    return guess if bst(guess) else t


def grid_ref(e, n):
    """A twelve-figure national grid reference with its 100 km square letters (the SJ square for this area)."""
    assert 300000 <= e < 400000 and 300000 <= n < 400000
    return "SJ %05d %05d" % (int(round(e)) - 300000, int(round(n)) - 300000)


def to_grid(xy):
    return BH2_E + xy[0], BH2_N + xy[1]
