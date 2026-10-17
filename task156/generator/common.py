"""task156 constants and helpers shared by every generator module.

Millrind is a developer question-and-answer network of nine topic sites, run from Toronto. Every community review
item (a question with a close vote, a new account's first post, an answer the platform scores as low quality, a
suggested edit) enters its site's review inbox and goes first to the volunteer reviewers; an item no volunteer has
reviewed 72 hours after it entered is routed to the paid moderation team, which also handles every moderator flag.
The Moderation Council sizes the paid team each year in FTE and votes its request at its December sitting. The data
were pulled on Thursday 8 October 2026 and run to Wednesday 30 September 2026.

The seed was fixed by rule before any data was generated: the task number, then the as-of month and day."""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import io
import math

import numpy as np

SEED = 1561009

NETWORK = "Millrind"
COUNCIL = "Millrind Moderation Council"

PEOPLE = {
    "ops": "Duane Zamora",       # head of moderation operations: the operations notes, the file list, the WFM notes
    "finance": "Natalie Maxwell",  # finance business partner for trust and safety: the 2027 envelope letter
    "chair": "Claudia Spence",    # council chair: signatory on the charter and the 2027 handle-time standards
}

UTC = dt.timezone.utc

# ------------------------------------------------------------------------------------------------- calendar
D0 = dt.date(2021, 1, 1)
OLD_END = dt.date(2023, 12, 31)          # the old review system's last month
NEW_START = dt.date(2024, 1, 1)          # the review platform's first day
HIST_END = dt.date(2026, 9, 30)          # last day in the pull
PULL_PRELIM = dt.date(2026, 10, 2)       # preliminary September pull
PULL_DATE = dt.date(2026, 10, 8)         # the full pull every export carries
ASOF = dt.date(2026, 10, 9)              # the file list is dated the day after the pull
PLAN_DATE = dt.date(2026, 9, 18)
ENVELOPE_DATE = dt.date(2026, 9, 30)
STANDARDS_DATE = dt.date(2026, 6, 17)
CHARTER_DATE = dt.date(2025, 3, 12)
D_END = dt.date(2027, 12, 31)
MERGER = dt.date(2023, 7, 1)             # Graphics & Shaders folded into Game Development
EDIT_QUEUE_START = dt.date(2022, 1, 1)   # suggested edits entered the old review system in January 2022

MONTH_NAMES = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
               "November", "December"]
MON3 = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# ------------------------------------------------------------------------------------------------- sites
# code, display name, the old review system's name, regime (the design's group: C comfortable, B crosses in 2027,
# A short since late 2025), 2026 mean monthly questions, AI-era fall by mid-2025, target volunteer cover (capacity
# over inbox arrivals) for January to September 2026
SITES = ["web", "mobile", "data", "databases", "devops", "gamedev", "security", "embedded", "scicomp"]
SITE = {
    "web":       dict(name="Frontend & Web", old="Web Development", grp="C", q26=29800, drop=0.598, cover=1.66),
    "mobile":    dict(name="Mobile Apps", old="Mobile Development", grp="C", q26=11900, drop=0.574, cover=1.63),
    "data":      dict(name="Data & ML", old="Data Science & ML", grp="B", q26=23600, drop=0.437, cover=1.115),
    "databases": dict(name="Databases", old="Database Administration", grp="B", q26=19700, drop=0.414, cover=1.137),
    "devops":    dict(name="Infrastructure & DevOps", old="Ops & Cloud", grp="B", q26=16800, drop=0.392, cover=1.13),
    "gamedev":   dict(name="Game Development", old="Game Development", grp="B", q26=6150, drop=0.451, cover=1.12),
    "security":  dict(name="Security", old="Information Security", grp="A", q26=8100, drop=0.268, cover=0.845),
    "embedded":  dict(name="Embedded & Hardware", old="Embedded Systems", grp="A", q26=5050, drop=0.233, cover=0.76),
    "scicomp":   dict(name="Scientific Computing", old="Scientific Computing", grp="A", q26=3550, drop=0.214, cover=0.83),
}
GRAPHICS_OLD = "Graphics & Shaders"      # an old site folded into gamedev on 1 July 2023
GRAPHICS_SHARE = 0.27                    # its share of the merged site's questions before the merger

# item types in the review inbox and their per-question rates (the network mean; each site varies a little)
ITEMS = ["close", "first_post", "low_quality", "edit"]
ITEM_LABEL = {"close": "Close votes", "first_post": "First posts", "low_quality": "Low quality",
              "edit": "Suggested edits"}
ITEM_RATE = {"close": 0.56, "first_post": 0.86, "low_quality": 0.79, "edit": 0.61}
FLAG_RATE = 0.152                        # moderator flags per question, the network mean

# handle-time standards, minutes per item handled by a paid moderator
STD_2026 = {"flag": 9.0, "close": 5.0, "first_post": 4.0, "low_quality": 3.5, "edit": 2.0}
STD_2027 = {"flag": 9.0, "close": 2.0, "first_post": 4.0, "low_quality": 3.5, "edit": 2.0}
FTE_HOURS = 1600.0
POOL_2026 = 27                           # FTE, the 2026 pool the council requested and finance funded
ENVELOPE_2027 = 26                       # FTE, finance's 2027 envelope

# volunteer reviewers
KAPPA = 40.0                             # mean reviews a reviewer completes in a month when work is plentiful
KAPPA_SIG = 0.15                         # lognormal spread of reviewers' own paces
ACT_SHAPE = 9.0                          # month-to-month variation in a reviewer's activity (gamma shape)
CHURN = 0.0205                           # monthly share of reviewers who stop (every site, every year)
PIPE_MID = dt.date(2024, 9, 15)          # the reputation pipeline runs dry around here
PIPE_WIDTH_M = 1.4                       # months
PIPE_FLOOR = 0.004                       # inflow after the pipeline dried up, share of the old steady inflow
SKIP_SHARE = 0.0058                      # the network mean of the items no volunteer ever picks up
SKIP_BY_TYPE = {"close": 0.0091, "first_post": 0.0035, "low_quality": 0.0072, "edit": 0.0040}   # by item type
HANDOFF_DAYS = 3                         # 72 hours

# question volume shape
SEAS = {1: 1.00, 2: 1.04, 3: 1.09, 4: 1.06, 5: 0.99, 6: 0.90, 7: 0.85, 8: 0.89, 9: 1.04, 10: 1.14, 11: 1.06,
        12: 0.86}
_m = sum(SEAS.values()) / 12.0
SEAS = {k: v / _m for k, v in SEAS.items()}
WD_Q = [1.12, 1.15, 1.12, 1.08, 0.98, 0.75, 0.80]        # Monday first
_w = sum(WD_Q) / 7.0
WD_Q = [v / _w for v in WD_Q]
WD_K = [1.03, 1.04, 1.03, 1.01, 0.97, 0.95, 0.97]        # volunteers review a little more on weekdays
_w = sum(WD_K) / 7.0
WD_K = [v / _w for v in WD_K]
AI_MID = dt.date(2023, 7, 1)
AI_WIDTH_M = 3.5
DRIFT_FROM = dt.date(2025, 7, 1)
DRIFT_PER_YEAR = 0.975


# ------------------------------------------------------------------------------------------------- helpers
def rng(*keys):
    """An independent numpy stream per name: blake2b of the seed and the keys (hash() is salted per process)."""
    h = hashlib.blake2b(("%d|" % SEED + "|".join(str(k) for k in keys)).encode(), digest_size=8).digest()
    return np.random.default_rng(int.from_bytes(h, "big"))


def token(*keys, n=12):
    return hashlib.blake2b(("%d|" % SEED + "|".join(str(k) for k in keys)).encode(), digest_size=16).hexdigest()[:n]


def days(a, b):
    out, d = [], a
    while d <= b:
        out.append(d)
        d += dt.timedelta(days=1)
    return out


def month_key(d):
    return (d.year, d.month)


def months(a, b):
    """(year, month) from a's month to b's month inclusive."""
    out, y, m = [], a.year, a.month
    while (y, m) <= (b.year, b.month):
        out.append((y, m))
        m += 1
        if m == 13:
            y, m = y + 1, 1
    return out


def month_index(y, m):
    return (y - D0.year) * 12 + (m - 1)


def days_in_month(y, m):
    nxt = dt.date(y + (m == 12), m % 12 + 1, 1)
    return (nxt - dt.date(y, m, 1)).days


def month_frac(d):
    """Months since D0 as a float (mid-month 0.5)."""
    return (d.year - D0.year) * 12 + (d.month - 1) + (d.day - 0.5) / days_in_month(d.year, d.month)


def logistic(x):
    return 1.0 / (1.0 + math.exp(-x))


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
    return math.floor(q + 0.5) / 10 ** nd


def bin_clearance(x, step):
    """Distance from x to the nearest rounding edge of its step-wide bin, as a share of the step (0.5 is mid-bin)."""
    q = x / step
    return 0.5 - abs(q - math.floor(q + 0.5))


def ca_date(d):
    return "%s %d, %d" % (MONTH_NAMES[d.month], d.day, d.year)
