"""task141 constants and helpers shared by every generator module.

Dorrance County, North Carolina (fictional; county seat Garrison) is one judicial district. Arrestees go before the
magistrate on duty at the detention center's intake for their initial appearance, where the magistrate sets the
conditions of pretrial release under the district's local bail policy. Dorrance County Pretrial Services screens
arrestees at intake with the Pretrial Assessment Scale. The draft revision of the local bail policy for 2027 adds a
presumptive release tier on the scale's new-criminal-activity score, under an 85 per cent safety floor."""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import io
import math

import numpy as np

SEED = 1410417

# ---------------------------------------------------------------------------------------------------- calendar
HIST_START = dt.date(2021, 10, 1)        # first first appearance in the legacy export
CMS_CHANGE = dt.date(2024, 3, 4)         # the clerk's new case management system from this day
HIST_LAST = dt.date(2025, 9, 30)         # the last first appearance whose 365-day window closes inside the extract
FY26_START = dt.date(2025, 10, 1)        # the asks' year
EXTRACT_END = dt.date(2026, 9, 30)       # every export runs to the end of this day (Eastern)
PULL = dt.date(2026, 10, 2)              # the exports were pulled
DRAFT_DATE = dt.date(2026, 10, 6)        # the draft revision
FILING_DATE = dt.date(2026, 12, 1)       # the revised policy is filed with the clerk by this day
EFFECTIVE = dt.date(2027, 1, 1)
BOARDING_START = dt.date(2025, 11, 3)    # the west housing unit closed; boarding at Halsey County from this day
ASKB_LAST = dt.date(2026, 6, 30)         # Ask B: releases to this day, each with 90 days inside the extract
POLICY_2024 = dt.date(2024, 7, 1)        # the current local bail policy took effect

WINDOW_DAYS = 365
FLOOR = 0.85


def d2dt(d, h=0, m=0):
    return dt.datetime(d.year, d.month, d.day, h, m)


# ---------------------------------------------------------------------------------------------------- Eastern time
def _nth_sunday(y, month, n):
    d = dt.date(y, month, 1)
    while d.weekday() != 6:
        d += dt.timedelta(days=1)
    return d + dt.timedelta(days=7 * (n - 1))


def eastern_offset_utc(t_utc):
    """Hours to add to UTC for Eastern wall time: EDT (-4) from the second Sunday of March 07:00 UTC to the first Sunday
    of November 06:00 UTC, EST (-5) otherwise."""
    y = t_utc.year
    start = d2dt(_nth_sunday(y, 3, 2), 7)
    end = d2dt(_nth_sunday(y, 11, 1), 6)
    return -4 if start <= t_utc < end else -5


def eastern_to_utc(t_local):
    """Eastern wall time (naive) to UTC (naive). The repeated hour in November takes its first (EDT) instance."""
    y = t_local.year
    start_local = d2dt(_nth_sunday(y, 3, 2), 2)       # 02:00 EST becomes 03:00 EDT
    end_local = d2dt(_nth_sunday(y, 11, 1), 1)        # 02:00 EDT becomes 01:00 EST; 01:00 to 02:00 happens twice
    off = -4 if start_local <= t_local < end_local + dt.timedelta(hours=1) else -5
    return t_local - dt.timedelta(hours=off)


def utc_to_eastern(t_utc):
    return t_utc + dt.timedelta(hours=eastern_offset_utc(t_utc))


def midnights(a, b):
    """Midnight counts (Eastern) at which a person held from a to b (naive Eastern datetimes) is in custody, each dated
    with the day it begins: the counts at 00:00 on every day after a's date up to b's date (a count at b exactly is
    taken only if b is after it). Returns the list of count dates."""
    out = []
    d = a.date() + dt.timedelta(days=1)
    while d2dt(d) < b:
        out.append(d)
        d += dt.timedelta(days=1)
    return out


# ---------------------------------------------------------------------------------------------------- the county
COUNTY = "Dorrance County"
SEAT = "Garrison"
STATE = "North Carolina"
HOST = "Halsey County"
AGENCY_PTS = "Dorrance County Pretrial Services"
SHERIFF = "Dorrance County Sheriff's Office"
DETENTION = "Dorrance County Detention Center"
COURT = "Dorrance County District Court"
SCALE = "Pretrial Assessment Scale"
EM_VENDOR = "Sentry Point Monitoring"

PEOPLE = {
    "analyst": "Lauren Mullins",          # research analyst, Pretrial Services (the requester; not in the prompt)
    "director": "Teresa Diaz",            # director, Dorrance County Pretrial Services
    "srj": "Zachary Henson",              # senior resident superior court judge (issues the local bail policy)
    "cdj": "Kristen Thompson",            # chief district court judge
    "chiefmag": "Jeffrey Francis",        # chief magistrate
    "jail": "Gina Yoder",                 # jail administrator, Sheriff's Office
    "clerk": "Colleen Cameron",           # clerk of superior court
}

# ---------------------------------------------------------------------------------------------------- the pack
FA_LEGACY = "first_appearances_2021-10-01_2024-03-03.csv"
FA_NEW = "first_appearances_2024-03-04_2026-09-30.csv"
FA_CHARGES = "first_appearance_charges_2024-03-04_2026-09-30.csv"
SCREENS = "pas_screens_2021-10-01_2026-09-30.csv"
JAIL = "jail_bookings_2021-10-01_2026-09-30.csv"
ARRESTS = "state_arrest_extract_2026-10-02.csv"
CASES = "court_case_index_2021-10-01_2026-09-30.csv"
EVENTS = "court_events_2025-10-01_2026-09-30.csv"
EM = "sentry_point_invoice_lines_2025-10_2026-09.csv"
HALSEY = "halsey_county_board_bills_2025-11_2026-09.xlsx"
CROSSWALK = "offense_code_crosswalk.xlsx"
ROSTER = "magistrate_roster.xlsx"
JAIL_CODES = "jail_code_list.csv"
COURT_CODES = "court_code_list.csv"
POLICY24 = "local_bail_policy_2024.pdf"
DRAFT = "bail_policy_revision_2027_draft.docx"
GUIDE = "pas_scoring_guide_v2.pdf"
README = "README_pretrial_extracts.txt"
CJAC = "cjac_jail_population_report_2025.pdf"
CRIME = "dorrance_county_reported_crime_2019-2025.xlsx"
DISTRACTORS = [CJAC, CRIME]

GOLD_MEMO = "presumptive_release_tier_2027.docx"
GOLD_BOOK = "presumptive_release_tier_2027.xlsx"
GOLD_CHART = "missed_court_dates_by_fta_score.png"


def rng(*keys):
    """An independent numpy stream per name: blake2b of the seed and the keys (hash() is salted per process)."""
    h = hashlib.blake2b(("%d|" % SEED + "|".join(str(k) for k in keys)).encode(), digest_size=8).digest()
    return np.random.default_rng(int.from_bytes(h, "big"))


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
    q = x / step
    return int(math.floor(q + 0.5)) * step if q >= 0 else -int(math.floor(-q + 0.5)) * step


def round1(x):
    """Half away from zero to one decimal."""
    return math.floor(x * 10 + 0.5) / 10 if x >= 0 else -math.floor(-x * 10 + 0.5) / 10
