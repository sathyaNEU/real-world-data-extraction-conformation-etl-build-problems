"""task163 constants and helpers shared by every generator module.

Kilbourne Payroll is a payroll services company in Columbus, Ohio (payroll processing and payroll tax filing for small
businesses on its own platform) selling in twelve states of the Great Lakes, Ohio Valley and their neighbours. Its 2027
operating plan is signed off by the CFO on Friday 16 October 2026; the first-time-employer line is sized from the Census
Bureau's business formation statistics, the October 2026 release.

The seed was fixed by rule before any data was generated: the task number, then the as-of month and day."""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import io
import math

import numpy as np

SEED = 1631016

COMPANY = "Kilbourne Payroll"
PEOPLE = {
    "planning": "Dominique Thomas",   # revenue planning lead, FP&A: the requester and the plan standard's owner
    "research": "Charles Fernandez",  # market research analyst: the statistics extracts and the reform log
    "salesops": "Cheryl Mitchell",    # sales operations: the onboarding export, the share tab, the counting notes
    "cfo": "Calvin Garrett",          # CFO: signs the 2027 operating plan
}

UTC = dt.timezone.utc

# ------------------------------------------------------------------------------------------------- calendar
M0 = (2022, 1)                     # first month of every monthly array (the research team's extract starts here)
SIM_END = (2027, 12)               # the simulation runs through the plan year (truth only; never shipped past the cut)
AS_OF = dt.date(2026, 10, 16)      # Friday: the plan sign-off
BFS_RELEASE = dt.date(2026, 10, 14)        # the October 2026 release (applications through September 2026)
BFS_EARLIER = dt.date(2026, 4, 15)         # the April 2026 release the research team pulled first
APPS_LAST = (2026, 9)              # last month of applications in the October release
BF4_LAST = (2025, 6)               # last application month whose formations within four quarters are published
BF8_LAST = (2024, 6)               # last application month whose formations within eight quarters are published
APPS_LAST_EARLY = (2026, 3)        # the April release
BF4_LAST_EARLY = (2024, 12)
BF8_LAST_EARLY = (2023, 12)
TTM = ((2025, 10), (2026, 9))      # the plan's application volume: the twelve months to September 2026
SHARE_BASE = ((2024, 7), (2025, 6))   # the share tab's formations base: July 2024 to June 2025 applications

MONTH_NAMES = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
               "November", "December"]
MON3 = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def midx(y, m=None):
    """Index of a month in the monthly arrays (January 2022 is 0)."""
    if m is None:
        y, m = y
    return (y - M0[0]) * 12 + (m - M0[1])


def mfrom(i):
    y, m = divmod(i, 12)
    return (M0[0] + y, M0[1] + m)


NM = midx(SIM_END) + 1


def months(a, b):
    """Inclusive list of (year, month) from a to b."""
    return [mfrom(i) for i in range(midx(a), midx(b) + 1)]


def add_months(t, k):
    return mfrom(midx(t) + k)


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
    return math.floor(q + 0.5) / 10 ** nd


def round_to(x, step):
    return step * math.floor(x / step + 0.5)


def edge_distance(x, step):
    """Distance from x to the nearest edge of the step-wide cell it prints in, as a share of the step (0.5 is the
    centre): step/2 - |x - round(x/step)*step|, divided by step."""
    return (step / 2.0 - abs(x - round_to(x, step))) / step


def us_date(d):
    return "%s %d, %d" % (MONTH_NAMES[d.month], d.day, d.year)
