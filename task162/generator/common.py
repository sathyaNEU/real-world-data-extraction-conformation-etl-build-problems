"""task162 constants and helpers shared by every generator module.

Lynmere Water supplies its Northern zone from Thornholme service reservoir down the Thornholme to Brackenby trunk main;
34 district metered areas take their supply off it, and a paper mill near Brackenby draws two weekday shifts' worth of
water from its own off-take on the same main. Coldbeck Network Partners is Lynmere's pressure management and leakage
partner on an outcome contract. Phase 3 puts a fixed-outlet pressure reducing valve on the inlet of each of the 22
districts at the main's far end, commissioned January to March 2027. Every file was taken on Monday 2 November 2026
for Coldbeck's 2027-28 delivery plan."""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import io
import json
import math

import numpy as np

SEED = 1622027

COMPANY = "Lynmere Water"
PARTNER = "Coldbeck Network Partners Ltd"
MILL = "Brackenby Paper Mill"
ZONE = "Northern zone"
RESERVOIR = "Thornholme service reservoir"
MAIN = "Thornholme to Brackenby trunk main"
LW_DOMAIN = "lynmerewater.co.uk"
CB_DOMAIN = "coldbecknp.co.uk"

PEOPLE = {
    "delivery": "Emily Fitzgerald",     # Coldbeck's Northern zone delivery lead (the requester; in no file the prompt names)
    "modeller": "Annette Patel",        # Coldbeck's network modeller: the valve schedule
    "contract": "Clive Heath",          # Lynmere's contract manager: Schedule 4 issue, the planning note
    "leakage": "Louis Lee",             # Lynmere's leakage analyst: the assessment export, the method's owner
    "commercial": "Mandy Austin",       # Coldbeck's commercial manager
}

AS_OF = dt.date(2026, 11, 2)                     # Monday: every file taken for the delivery plan
YEAR_START = dt.datetime(2025, 4, 1)             # the 2025-26 assessment year (GMT days)
YEAR_END = dt.datetime(2026, 4, 1)
TARGET = 0.48                                    # Schedule 4: Phase 3's contracted reduction, Ml/d
GANG_YIELD = 0.05                                # Schedule 4: sustained reduction a find-and-fix gang-year delivers, Ml/d
ALLOWANCE = 1.7                                  # LW-LA-04: household night use allowance, litres a household an hour
NONHH_ALLOWANCE = 8.0                            # LW-LA-04: non-household night use allowance, litres a property an hour
NIGHT_HOUR = 3                                   # LW-LA-04: 03:00 to 04:00 GMT
OPEN_LOSS = 0.1                                  # valve schedule: an open valve's loss at peak hour flow is under this, m
UNBILLED_SHARE = 0.004                           # LW-LA-04 section 8: unbilled authorised use, share of system input
UNDER_REG = 0.025                                # section 8: customer meter under-registration, share of billed metered
UNAUTH_SHARE = 0.003                             # section 8: unauthorised use, share of system input
CERT_DATE = dt.date(2025, 11, 12)                # the outlet meter's calibration: as found 1.4 per cent low
CERT_ERROR = -0.014

UTC = dt.timezone.utc

MONTHS = [dt.datetime(2025 + (3 + k) // 12, (3 + k) % 12 + 1, 1) for k in range(12)]   # April 2025 .. March 2026
MONTH = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
         "November", "December"]
WEEKDAY = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


# ------------------------------------------------------------------------------------------------- clocks
def _last_sunday(y, m):
    d = (dt.date(y, m + 1, 1) - dt.timedelta(days=1)) if m < 12 else dt.date(y, 12, 31)
    while d.weekday() != 6:
        d -= dt.timedelta(days=1)
    return d


def bst(t_gmt):
    """True when UK clocks are on British Summer Time at GMT time t (01:00 GMT on the last Sunday of March to 01:00 GMT
    on the last Sunday of October)."""
    y = t_gmt.year
    return dt.datetime.combine(_last_sunday(y, 3), dt.time(1)) <= t_gmt < dt.datetime.combine(_last_sunday(y, 10), dt.time(1))


def local(t_gmt):
    return t_gmt + dt.timedelta(hours=1 if bst(t_gmt) else 0)


# ------------------------------------------------------------------------------------------------- randomness
def rng(*keys):
    """An independent numpy stream per name (blake2b of the seed and the keys; hash() is salted per process)."""
    h = hashlib.blake2b(("%d|" % SEED + "|".join(str(k) for k in keys)).encode(), digest_size=8).digest()
    return np.random.default_rng(int.from_bytes(h, "big"))


def token(*keys, n=8, alphabet="0123456789"):
    h = hashlib.blake2b(("%d|" % SEED + "|".join(str(k) for k in keys)).encode(), digest_size=32).digest()
    return "".join(alphabet[b % len(alphabet)] for b in h[:n])


# ------------------------------------------------------------------------------------------------- writing
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


def read_csv(path):
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def write_json(path, obj, indent=None):
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(obj, fh, ensure_ascii=False, indent=indent, separators=(",", ":") if indent is None else (",", ": "))
        fh.write("\n")


def round_half_up(x, nd=0):
    q = x * 10 ** nd
    return math.floor(q + 0.5) / 10 ** nd


def ceil_div(x, step):
    """Whole steps, rounded up (Schedule 4.4's gang-years), robust to float noise at an exact multiple."""
    return int(math.ceil(x / step - 1e-9))


def bin_clearance(x, step):
    """Distance from x to the nearest edge of its rounding cell, as a share of the step (0.5 is the centre)."""
    q = x / step
    return 0.5 - abs(q - math.floor(q + 0.5))


def ceil_clearance(x, step):
    """For a value rounded up to whole steps: the distance to the nearest step boundary as a share of the step."""
    f = x / step - math.floor(x / step)
    return min(f, 1 - f)


def long_date(d):
    return "%s %d %s %d" % (WEEKDAY[d.weekday()], d.day, MONTH[d.month], d.year)


def uk_date(d):
    return "%d %s %d" % (d.day, MONTH[d.month], d.year)


def addr(name, domain=LW_DOMAIN):
    a = name.lower().split()
    return "%s.%s@%s" % (a[0], a[-1], domain)
