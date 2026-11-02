"""task163 constants and helpers shared by every generator module.

Lathmor Logistics runs e-commerce fulfilment for consumer brands. At its Uphall centre in West Lothian it picks the
online orders of Aubrine, a cosmetics and fragrance brand, from carton-flow lanes (zone A) and static shelving (zones
B, C and D). Every parcel is check-weighed at the pack benches. A slotting consultant's plan re-slots the shelving zones
by product family over the Christmas shutdown, live on Monday 4 January 2027. The pack is as of Friday 30 October 2026.

The seed was fixed by rule before any data was generated: the task number, then the as-of month and day."""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import io
import math

import numpy as np

SEED = 1631030

COMPANY = "Lathmor Logistics Ltd"
BRAND = "Aubrine"
AGENCY = "Corsley Staffing"
REPACK = "Ravelrig Packing"
PEOPLE = {
    "quality": "Kathryn Tomlinson",   # Lathmor head of quality, Uphall: the requester
    "account": "Brian Cook",          # Lathmor account director for Aubrine
    "brand": "Hazel Collins",         # Aubrine head of e-commerce operations
    "returns": "Kayleigh Ward",       # returns bench team leader
}

AS_OF = dt.date(2026, 10, 30)
GO_LIVE = dt.date(2027, 1, 4)
APP_LIVE = dt.date(2026, 6, 8)        # the returns bench's handheld app
TOL_G = 15                            # the pack benches' check-weigh tolerance, grams either way
KPI_PER_10K = 2.5                     # Schedule 3: validated mis-pick claims per 10,000 order lines, contract year

# the twelve-month baseline: ISO weeks 2025-W39 (Mon 22 Sep 2025) to 2026-W38 (Sun 20 Sep 2026)
BASE_FROM = dt.date(2025, 9, 22)
BASE_TO = dt.date(2026, 9, 20)
# the velocity export and the holds log run wider: Monday 1 September 2025 to Sunday 25 October 2026
EXPORT_FROM = dt.date(2025, 9, 1)
EXPORT_TO = dt.date(2026, 10, 25)
# Corsley: weekly invoices for the weeks 25 August 2025 to 25 October 2026; four-week pay periods from 4 August 2025
AGENCY_FROM = dt.date(2025, 8, 25)
AGENCY_TO = dt.date(2026, 10, 25)
PAY_P0 = dt.date(2025, 8, 4)
ASK_A_MONTHS = [(2025, 9), (2025, 10), (2025, 11), (2025, 12)] + [(2026, m) for m in range(1, 9)]
# returns graded at the bench: 1 September 2025 to 30 October 2026; Ask B's twelve months October 2025 to September 2026
RET_FROM = dt.date(2025, 9, 1)
RET_TO = dt.date(2026, 10, 30)
ASK_B_FROM = dt.date(2025, 10, 1)
ASK_B_TO = dt.date(2026, 9, 30)

MONTH_NAMES = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
               "November", "December"]
MON3 = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

UK_HOLIDAYS = {dt.date(2025, 12, 25), dt.date(2025, 12, 26), dt.date(2026, 1, 1), dt.date(2026, 1, 2)}


def days(a, b):
    out, d = [], a
    while d <= b:
        out.append(d)
        d += dt.timedelta(1)
    return out


def iso_week(d):
    y, w, _ = d.isocalendar()
    return "%d-W%02d" % (y, w)


def monday(d):
    return d - dt.timedelta(d.weekday())


# ------------------------------------------------------------------------------------------------- randomness
def rng(*keys):
    """An independent numpy stream per name: blake2b of the seed and the keys (hash() is salted per process)."""
    h = hashlib.blake2b(("%d|" % SEED + "|".join(str(k) for k in keys)).encode(), digest_size=8).digest()
    return np.random.default_rng(int.from_bytes(h, "big"))


def token(*keys, n=12, alphabet="0123456789abcdef"):
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


def round_half_up(x, nd=0):
    q = x * 10 ** nd
    return math.floor(q + 0.5 + 1e-9) / 10 ** nd


def round_to(x, step):
    return step * math.floor(x / step + 0.5 + 1e-12)


def edge_distance(x, step):
    """Distance from x to the nearest edge of the step-wide cell it prints in, as a share of the step (0.5 is the
    centre): step/2 - |x - round(x/step)*step|, divided by step."""
    return (step / 2.0 - abs(x - round_to(x, step))) / step


def uk_date(d):
    return "%d %s %d" % (d.day, MONTH_NAMES[d.month], d.year)
