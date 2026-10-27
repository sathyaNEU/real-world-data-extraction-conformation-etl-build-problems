"""task270 constants and helpers shared by every generator module.

Iversford Vale GP Federation, the provider company its member practices own, runs a statin adherence service for the
twelve primary care networks those practices form, subcontracting the community pharmacies, for 2027-28. Pharmacists
contact the patients aged 65 and over who collect and take their own statins and held statin for under 80 per cent of
their 2026 days; the federation funds an enhanced tier in the networks where 30 per cent or more of those patients
fell under 80 per cent. Care home residents, and patients whose medicines a pharmacy packs into a compliance aid, are
reviewed under the structured medication review service instead. The member practices run on two clinical systems,
Quarvis and Synaris; only Quarvis's year-end list records the compliance aid. NHS Iversford Vale Integrated Care
Board's health data service supplies the dispensing and the practice lists. The federation's board fixes the tier
schedule before the service starts on 1 April 2027.

The seed was fixed by rule before any data was generated: the task number, then the extract pull's month and day."""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import io
import math
import os

import numpy as np

SEED = 2700111

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.abspath(os.path.join(HERE, ".."))
TARGET = os.environ.get("TASK270_TARGET") or os.path.join(TASK, "target")     # a scratch rebuild sets these two
GOLDEN = os.environ.get("TASK270_GOLDEN") or os.path.join(TASK, "golden")

FEDERATION = "Iversford Vale GP Federation"         # decides: its board sets the tier schedule
ICB = "NHS Iversford Vale Integrated Care Board"       # its data service supplies the extracts; it issued the guidance
DATA_SERVICE = "Iversford Vale Health Data Service"
QUARVIS = "Quarvis"
SYNARIS = "Synaris"
SERVICE = "Statin Adherence Support Service"

PEOPLE = {
    "head": "Ashleigh Shah",      # the federation's head of medicines optimisation: writes the board paper
    "chair": "Antony Evans",      # chair of the federation's board
    "pharmacy": "Frances Thomas", # community pharmacy clinical lead: the compliance-aid guidance
}

# ------------------------------------------------------------------------------------------------- calendar
DISP_START = dt.date(2025, 10, 1)        # the world's first simulated day, so every cycle is running by January
EXTRACT_START = dt.date(2025, 12, 1)     # the dispensing extract's first day
YEAR_START = dt.date(2026, 1, 1)
YEAR_END = dt.date(2026, 12, 31)
REKEY = dt.date(2026, 7, 1)              # the data service re-keyed every patient pseudonym
NETWORK_MOVE = dt.date(2026, 4, 1)       # two practices moved network
PULL = dt.date(2027, 1, 11)              # the extracts were pulled
PAPER_DATE = dt.date(2027, 1, 27)
MEETING = dt.date(2027, 2, 10)           # the federation's board meets
ISSUE = dt.date(2027, 3, 1)              # the tier schedule issues to the pharmacies with their service agreements
SERVICE_START = dt.date(2027, 4, 1)      # the service starts: the forcing event
SPEC_DATE = dt.date(2026, 11, 16)
GUIDANCE_DATE = dt.date(2025, 6, 2)
BORN_BY = 1961                           # aged 65 or over on 31 December 2026
PDC_LINE = 0.80
TIER_LINE = 0.30
BANK_HOLIDAYS = {
    dt.date(2025, 12, 25), dt.date(2025, 12, 26), dt.date(2026, 1, 1), dt.date(2026, 4, 3), dt.date(2026, 4, 6),
    dt.date(2026, 5, 4), dt.date(2026, 5, 25), dt.date(2026, 8, 31), dt.date(2026, 12, 25), dt.date(2026, 12, 28),
}

MONTH_NAMES = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
               "November", "December"]

# ------------------------------------------------------------------------------------------------- networks
# code, name, practice system, patients aged 65 and over on a statin, care home share, compliance-aid share,
# weekly share of the aid patients, self-managing patients' share under 80 per cent (the design target),
# number of practices
NETWORKS = [
    ("BRK", "Briskdale",  "T", 2450, 0.030, 0.150, 0.25, 0.331, 5),
    ("COR", "Corvendale",  "Q", 2900, 0.025, 0.060, 0.45, 0.352, 6),
    ("ELL", "Ellinholt",  "T", 1900, 0.020, 0.040, 0.50, 0.247, 4),
    ("FEL", "Feldcote",   "Q", 2200, 0.040, 0.150, 0.20, 0.342, 5),
    ("GRV", "Grevmoor",   "T", 2650, 0.035, 0.125, 0.30, 0.320, 5),
    ("IVF", "Iversford",  "Q", 1750, 0.015, 0.050, 0.55, 0.276, 4),
    ("KRT", "Krathwold",  "T", 2300, 0.025, 0.060, 0.40, 0.343, 5),
    ("LTH", "Lathcombe",  "Q", 2050, 0.030, 0.110, 0.30, 0.262, 4),
    ("MRL", "Marlwold",   "T", 1650, 0.020, 0.030, 0.50, 0.262, 3),
    ("NVG", "Nevgarth",   "Q", 2500, 0.035, 0.080, 0.40, 0.336, 5),
    ("PLH", "Pellholt",   "T", 2150, 0.030, 0.100, 0.35, 0.250, 4),
    ("TRV", "Tarvdale",   "Q", 1850, 0.020, 0.040, 0.50, 0.236, 4),
]
NETWORK_NAME = {c: n for c, n, *_ in NETWORKS}
QUARVIS_CODE_RATE = 0.66                 # Quarvis practices code about two thirds of their aid patients


# ------------------------------------------------------------------------------------------------- helpers
def rng(*keys):
    """An independent numpy stream per name: blake2b of the seed and the keys (hash() is salted per process)."""
    h = hashlib.blake2b(("%d|" % SEED + "|".join(str(k) for k in keys)).encode(), digest_size=8).digest()
    return np.random.default_rng(int.from_bytes(h, "big"))


def token(*keys, n=12):
    return hashlib.blake2b(("%d|" % SEED + "|".join(str(k) for k in keys)).encode(), digest_size=16).hexdigest()[:n]


def days(a, b):
    return (b - a).days


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


def uk_date(d):
    return "%d %s %d" % (d.day, MONTH_NAMES[d.month], d.year)
