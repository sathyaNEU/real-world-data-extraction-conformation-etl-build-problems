"""task157 constants and helpers shared by every generator module.

Larch Rides is a regional ride-hail operator in the Twin Cities (Minneapolis and Saint Paul), launched in May 2021.
Its winter guarantee pays $350 to every driver who completes 40 trips in the four weeks from the first Monday of
January; it ran in 2025 and 2026 and goes live for 2027 at 00:00 on Monday 4 January 2027, when finance funds its
account. The warehouse extract that every file comes from was run on Sunday 3 January 2027.

The seed was fixed by rule before any data was generated: the task number, then the as-of month and day."""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import io
import math

import numpy as np

SEED = 1570103

OPERATOR = "Larch Rides"
PEOPLE = {
    "supply": "Gary Mathews",      # head of driver supply: the requester (in no file the prompt names)
    "finance": "Kathy Sherman",    # finance director: the funding email
    "analytics": "Jesse Velasquez",  # supply analytics: the KPI report, the warehouse extract log and table notes
    "payments": "Melvin Harrell",  # payments operations: the payout files, the later runs, the guarantee notes
}
ONBOARDING_OWNER = "Driver onboarding"

UTC = dt.timezone.utc

# ------------------------------------------------------------------------------------------------- calendar
LAUNCH = dt.date(2021, 5, 3)             # Monday, Larch's first week on the road
MIGRATION = dt.date(2024, 7, 15)         # Monday, first day on the new dispatch platform; legacy to Sunday 14 July
AS_OF = dt.date(2027, 1, 3)              # Sunday, the warehouse extract's run date
EXTRACT_RUN = dt.datetime(2027, 1, 3, 21, 40)   # Central time
SIM_END = dt.date(2027, 3, 28)           # Sunday; the simulation runs past the 2027 window (truth only, never shipped)
GUARANTEE_YEARS = (2025, 2026, 2027)
AMOUNT = 350
THRESHOLD = 40
CAMPAIGN_FIRST = dt.date(2026, 2, 2)     # Monday, the 2026 recruitment campaign's first trips
CAMPAIGN_SIGNUP_OPEN = dt.date(2026, 1, 12)
RENTAL_FIRST = dt.date(2025, 2, 3)       # Monday, the rental programme's first drivers
RENTAL_END = dt.date(2025, 3, 31)        # the rental programme ended
FINANCE_EMAIL = dt.datetime(2026, 12, 30, 16, 12)
TERMS_DATE = dt.date(2026, 12, 14)
KPI_PUBLISHED = dt.date(2026, 12, 11)
MAIN_RUN = {2025: dt.date(2025, 2, 14), 2026: dt.date(2026, 2, 13)}
PAYMENTS_NOTES_DATE = dt.date(2026, 3, 20)
ONBOARDING_NOTES_DATE = dt.date(2026, 8, 5)

MONTH_NAMES = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
               "November", "December"]
MON3 = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
WEEKDAY = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def first_monday(y):
    j = dt.date(y, 1, 1)
    return j + dt.timedelta(days=(7 - j.weekday()) % 7)


WINDOW = {y: (first_monday(y), first_monday(y) + dt.timedelta(days=27)) for y in (2022, 2023, 2024) + GUARANTEE_YEARS}


def central_offset(t):
    """Hours Central time sits behind UTC at naive local time t (US rules since 2007: CDT from the second Sunday of
    March 02:00 to the first Sunday of November 02:00)."""
    y = t.year
    mar = dt.date(y, 3, 1)
    dst_start = dt.datetime.combine(mar + dt.timedelta(days=(6 - mar.weekday()) % 7 + 7), dt.time(2, 0))
    nov = dt.date(y, 11, 1)
    dst_end = dt.datetime.combine(nov + dt.timedelta(days=(6 - nov.weekday()) % 7), dt.time(2, 0))
    return 5 if dst_start <= t < dst_end else 6


def to_utc(t):
    return t + dt.timedelta(hours=central_offset(t))


def from_utc(t):
    # invert to_utc (the ambiguous hour at the fall change is resolved to standard time)
    for off in (5, 6):
        local = t - dt.timedelta(hours=off)
        if central_offset(local) == off:
            return local
    return t - dt.timedelta(hours=6)


# ------------------------------------------------------------------------------------------------- weeks
W0 = LAUNCH


def widx(d):
    return (d - W0).days // 7


def wdate(i):
    return W0 + dt.timedelta(days=7 * int(i))


NW = widx(SIM_END) + 1
ASOF_W = {y: widx(WINDOW[y][0]) - 1 for y in GUARANTEE_YEARS}   # the week ending the Sunday before each window
# the terms' eligibility: accounts approved by 23:59 on the Sunday before each window (Central time)
ELIGIBLE_BY = {y: WINDOW[y][0] - dt.timedelta(days=1) for y in GUARANTEE_YEARS}


def months(a, b):
    out, y, m = [], a.year, a.month
    while (y, m) <= (b.year, b.month):
        out.append((y, m))
        m += 1
        if m == 13:
            y, m = y + 1, 1
    return out


def ym(d):
    return (d.year, d.month)


def ym_str(t):
    return "%04d-%02d" % t


def add_months(t, k):
    y, m = t
    m += k
    while m > 12:
        y, m = y + 1, m - 12
    while m < 1:
        y, m = y - 1, m + 12
    return (y, m)


# ------------------------------------------------------------------------------------------------- randomness
def rng(*keys):
    """An independent numpy stream per name: blake2b of the seed and the keys (hash() is salted per process)."""
    h = hashlib.blake2b(("%d|" % SEED + "|".join(str(k) for k in keys)).encode(), digest_size=8).digest()
    return np.random.default_rng(int.from_bytes(h, "big"))


def token(*keys, n=12, alphabet="0123456789abcdef"):
    h = hashlib.blake2b(("%d|" % SEED + "|".join(str(k) for k in keys)).encode(), digest_size=32).digest()
    return "".join(alphabet[b % len(alphabet)] for b in h[:n])


B32 = "23456789ABCDEFGHJKLMNPQRSTUVWXYZ"


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


def round_half_up(x, nd=0):
    q = x * 10 ** nd
    return math.floor(q + 0.5) / 10 ** nd


def round_to(x, step):
    return step * math.floor(x / step + 0.5)


def bin_clearance(x, step):
    """Distance from x to the nearest rounding edge of its step-wide bin, as a share of the step (0.5 is mid-bin)."""
    q = x / step
    return 0.5 - abs(q - math.floor(q + 0.5))


def us_date(d):
    return "%s %d, %d" % (MONTH_NAMES[d.month], d.day, d.year)


def money(x):
    return "${:,.0f}".format(x)
