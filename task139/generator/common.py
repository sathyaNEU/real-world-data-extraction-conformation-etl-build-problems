"""Constants and helpers shared by the task139 generator: the world's calendar, the segments and their codes, file
names, the people, one independent random stream per name, CSV writing and the rounding conventions."""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import io

import numpy as np

SEED = 139

# ---- the calendar -------------------------------------------------------------------------------------------
EXTRACT_START = dt.date(2021, 1, 1)
EXTRACT_END = dt.date(2026, 9, 30)          # the claims system and the payments register pulled on 30 September
PULL_DATE = dt.date(2026, 9, 30)
PILOT_START = dt.date(2023, 3, 1)           # triage dates of the pilot, both inclusive
PILOT_END = dt.date(2025, 2, 28)
UPGRADE = dt.date(2025, 6, 2)               # first day on the new claims system
EDI_FIX = dt.date(2025, 9, 15)              # the new system's duplicate check on first reports switched back on
PARALLEL = (dt.date(2025, 5, 29), dt.date(2025, 6, 1))   # first reports keyed in both systems
VALUATION = dt.date(2026, 6, 30)            # the review's valuation date
REVIEW_DATE = dt.date(2026, 8, 14)
CHARTER_DRAFT = dt.date(2026, 9, 18)
CHARTER_SIGNED = dt.date(2026, 10, 19)
MEMO_DATE = dt.date(2026, 10, 28)
PLAN_DATE = dt.date(2026, 10, 2)
GO_LIVE = dt.date(2027, 1, 4)
PAY_START = dt.date(2026, 1, 1)
PAY_END = dt.date(2026, 9, 30)

TEAMS = 17
PLACES = 20
MAX_TEAMS = 3
YEAR_DAYS = 365                              # 2027
TEAM_PLACE_DAYS = PLACES * YEAR_DAYS         # 7,300

# ---- segments -----------------------------------------------------------------------------------------------
# new code (from the 2 June 2025 upgrade), legacy code, name, industry key, injury class
SEGMENTS = [
    ("HC-SS", "H1", "Healthcare and social assistance, strains and sprains", "HC", "SS"),
    ("HC-OT", "H2", "Healthcare and social assistance, other injuries", "HC", "OT"),
    ("RW-SS", "R1", "Retail and warehousing, strains and sprains", "RW", "SS"),
    ("RW-OT", "R2", "Retail and warehousing, other injuries", "RW", "OT"),
    ("MF-SS", "M1", "Manufacturing, strains and sprains", "MF", "SS"),
    ("MF-OT", "M2", "Manufacturing, other injuries", "MF", "OT"),
    ("CN-SS", "C1", "Construction, strains and sprains", "CN", "SS"),
    ("CN-OT", "C2", "Construction, other injuries", "CN", "OT"),
]
OTHER_SEGMENTS = [
    ("TR-SS", "T1", "Transportation, strains and sprains", "TR", "SS"),
    ("TR-OT", "T2", "Transportation, other injuries", "TR", "OT"),
    ("GN-AL", "G0", "All other industries", "GN", "AL"),
]
PROG = [s[0] for s in SEGMENTS]
ALL_SEGMENTS = SEGMENTS + OTHER_SEGMENTS
NEW_OF_LEGACY = {s[1]: s[0] for s in ALL_SEGMENTS}
LEGACY_OF_NEW = {s[0]: s[1] for s in ALL_SEGMENTS}
NAME = {s[0]: s[2] for s in ALL_SEGMENTS}
SHORT = {"HC-SS": "Healthcare strains", "HC-OT": "Healthcare other", "RW-SS": "Retail strains",
         "RW-OT": "Retail other", "MF-SS": "Manufacturing strains", "MF-OT": "Manufacturing other",
         "CN-SS": "Construction strains", "CN-OT": "Construction other"}
# claim units: one per segment; the unit names the claims department uses
UNIT = {"HC-SS": "Healthcare 1", "HC-OT": "Healthcare 2", "RW-SS": "Retail and Distribution 1",
        "RW-OT": "Retail and Distribution 2", "MF-SS": "Manufacturing 1", "MF-OT": "Manufacturing 2",
        "CN-SS": "Construction 1", "CN-OT": "Construction 2", "TR-SS": "Transportation", "TR-OT": "Transportation",
        "GN-AL": "General"}

# NCCI classification codes by industry, with weights (Missouri manual)
CLASS_CODES = {
    "HC": [("8833", 0.30), ("8829", 0.26), ("8835", 0.16), ("9043", 0.12), ("8864", 0.10), ("8832", 0.06)],
    "RW": [("8017", 0.22), ("8018", 0.18), ("8006", 0.17), ("8292", 0.19), ("8291", 0.10), ("8044", 0.14)],
    "MF": [("3632", 0.16), ("2003", 0.12), ("4299", 0.10), ("3076", 0.17), ("3179", 0.13), ("2070", 0.09),
           ("4130", 0.11), ("3830", 0.12)],
    "CN": [("5403", 0.20), ("5183", 0.14), ("5190", 0.15), ("5645", 0.13), ("5221", 0.12), ("6217", 0.10),
           ("5474", 0.08), ("5022", 0.08)],
    "TR": [("7219", 0.48), ("7380", 0.30), ("7228", 0.14), ("7370", 0.08)],
    "GN": [("8810", 0.26), ("9015", 0.18), ("8742", 0.15), ("9101", 0.12), ("9082", 0.17), ("8380", 0.12)],
}

# ---- files ----------------------------------------------------------------------------------------------------
REGISTER = "ern_pilot_assignments_2023-25.xlsx"
NURSE_LOG = "ern_case_log_2023-25.csv"
REVIEW_BOOK = "kpa_ern_indemnity_verification_2026-06-30.xlsx"
REVIEW_PDF = "kpa_ern_pilot_review_2026-08.pdf"
CHARTER = "ern_programme_charter_2027_signed.pdf"
CHARTER_DRAFT_DOC = "ern_programme_charter_2027_draft_v3.docx"
PICK_MEMO = "ay2027_indemnity_pick_ern_credit.pdf"
EXTRACT = "claims_extract_2021-01_to_2026-09.csv"
CROSSWALK = "segment_code_crosswalk_2025.csv"
PAYMENTS = "indemnity_payments_2026-01_to_09.csv"
ACH_RETURNS = "ach_returns_2026-01_to_09.csv"
MERGES = "claim_merges_2025.csv"
DICTIONARY = "claims_data_dictionary.xlsx"
MANIFEST = "export_manifest.csv"
SURVEY = "ern_pilot_worker_survey_2023-25.csv"
STAFFING = "medical_management_staffing_plan_2027.xlsx"
DISTRACTORS = [CHARTER_DRAFT_DOC, SURVEY, STAFFING]

GOLD_BOOK = "ern_placement_ay2027.xlsx"
GOLD_NOTE = "ern_placement_note_ay2027.pdf"

# ---- people (drawn with guard.py names --geo "United States" --seed 139; on the card) --------------------------
PEOPLE = {
    "director": "Julie Winters",        # director of medical case management, the requester (in no file as author of a figure)
    "kpa": "Joanna Sullivan",           # consulting actuary, Kellerman Pryce Actuarial, signs the review
    "pricing": "Kathleen Reilly",       # chief pricing actuary, owns the AY2027 indemnity pick
    "clinical": "Joel Kelly",           # ERN clinical lead
    "claimsops": "Kristen Hansen",      # claims operations, the triage screen and the assignment register
    "data": "Juan Castillo",            # data engineering, the claims-system upgrade
    "ceo": "Gregory Friedman",          # president and chief executive officer, signs the charter
}
COMPANY = "Haverline Casualty Company"
KPA = "Kellerman Pryce Actuarial"

# ---- US federal holidays (the triage screen runs on working days) ---------------------------------------------
_HOL = {
    2021: ["01-01", "01-18", "02-15", "05-31", "06-18", "07-05", "09-06", "10-11", "11-11", "11-25", "12-24", "12-31"],
    2022: ["01-17", "02-21", "05-30", "06-20", "07-04", "09-05", "10-10", "11-11", "11-24", "12-26"],
    2023: ["01-02", "01-16", "02-20", "05-29", "06-19", "07-04", "09-04", "10-09", "11-10", "11-23", "12-25"],
    2024: ["01-01", "01-15", "02-19", "05-27", "06-19", "07-04", "09-02", "10-14", "11-11", "11-28", "12-25"],
    2025: ["01-01", "01-20", "02-17", "05-26", "06-19", "07-04", "09-01", "10-13", "11-11", "11-27", "12-25"],
    2026: ["01-01", "01-19", "02-16", "05-25", "06-19", "07-03", "09-07", "10-12", "11-11", "11-26", "12-25"],
}
HOLIDAYS = {dt.date(y, int(md[:2]), int(md[3:])) for y, mds in _HOL.items() for md in mds}


def is_working(d):
    return d.weekday() < 5 and d not in HOLIDAYS


def next_working(d):
    """The triage screen sorts each working morning the intakes reported since the last run."""
    d = d + dt.timedelta(days=1)
    while not is_working(d):
        d += dt.timedelta(days=1)
    return d


def add_working(d, n):
    for _ in range(n):
        d = next_working(d)
    return d


def rng(*keys):
    """An independent numpy stream per name: blake2b of the seed and the keys (hash() is salted per process)."""
    h = hashlib.blake2b(("%d|" % SEED + "|".join(str(k) for k in keys)).encode(), digest_size=8).digest()
    return np.random.default_rng(int.from_bytes(h, "big"))


def daterange(a, b):
    d = a
    while d <= b:
        yield d
        d += dt.timedelta(days=1)


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


def round_to(x, step):
    """Round half away from zero to a multiple of step (the deliverables' convention)."""
    import math
    q = x / step
    return int(math.floor(q + 0.5)) * step if q >= 0 else -int(math.floor(-q + 0.5)) * step


def edge_distance(x, step):
    """How far x sits from the nearest rounding edge of a step-wide bin (the edges at odd multiples of step/2)."""
    import math
    r = (x / step) - math.floor(x / step)
    return abs(r - 0.5) * step


def cents(x):
    return float("%.2f" % (x + 1e-9))


def check_digit(s):
    """Kellerman Pryce's control digit on a claim number's digits: weights 2,3,4,5,6,7 from the right, mod 11, 10 as 0."""
    digits = [int(ch) for ch in s if ch.isdigit()]
    tot = sum(dg * (2 + (k % 6)) for k, dg in enumerate(reversed(digits)))
    c = (11 - tot % 11) % 11
    return str(0 if c == 10 else c)
