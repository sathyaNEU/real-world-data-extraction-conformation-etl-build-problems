"""task270 shared constants: the trust, its eleven community mental health teams, the calendar, the file names, and
one seeded random stream per purpose so a change in one part of the world leaves every other draw where it was."""
from __future__ import annotations

import datetime as dt
import hashlib
import os
from decimal import ROUND_HALF_UP, Decimal

import numpy as np

SEED = 2700901
HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.environ.get("TASK270_TARGET", os.path.join(TASK, "target"))
GOLDEN = os.environ.get("TASK270_GOLDEN", os.path.join(TASK, "golden"))

TRUST = "Brindholm and Wendholt NHS Foundation Trust"
COLLAB = "Sallowdene Provider Collaborative"
HUB = "Complex Emotional Needs Service"
PEOPLE = {"director": "Hilary O'Donnell", "collab": "Howard Harding", "ccio": "Jeremy Austin"}

# the eleven teams as from 1 October 2026; Haddersley North and South closed on 30 September 2026 and their
# patients and staff moved to the new Haddersley team
TEAMS = [("BW-CM02", "Dunnerby"), ("BW-CM05", "Marrowcombe"), ("BW-CM11", "Drystow"), ("BW-CM31", "Haddersley"),
         ("BW-CM17", "Cressbeck"), ("BW-CM03", "Rennicombe"), ("BW-CM08", "Ashwardine"), ("BW-CM20", "Hawkslow"),
         ("BW-CM09", "Garthby"), ("BW-CM22", "Sedgeholm"), ("BW-CM12", "Torrinsby")]
OLD_TEAMS = [("BW-CM14", "Haddersley North"), ("BW-CM15", "Haddersley South")]
TEAM_NAME = dict(TEAMS + OLD_TEAMS)
CURRENT = {c: (c if c not in ("BW-CM14", "BW-CM15") else "BW-CM31") for c in TEAM_NAME}
LOCALITY = {"BW-CM02": "Dunnerby and the Wynmoor villages", "BW-CM05": "Marrowcombe town",
            "BW-CM11": "Drystow and Fordwyke", "BW-CM31": "Haddersley", "BW-CM17": "Cressbeck",
            "BW-CM03": "Rennicombe and the coast", "BW-CM08": "Ashwardine", "BW-CM20": "Hawkslow",
            "BW-CM09": "Garthby", "BW-CM22": "Sedgeholm and Wraybeck", "BW-CM12": "Torrinsby"}

D = dt.date
YEAR0, YEAR1 = D(2026, 1, 1), D(2026, 12, 31)
FIRST_FORTNIGHT, LAST_FORTNIGHT = D(2026, 1, 5), D(2026, 12, 14)
V4_FROM = D(2026, 6, 15)               # the trust app's version 4 (UTC export, 0 to 10 buttons)
MERGER = D(2026, 10, 1)
HUB_GOLIVE = D(2026, 6, 22)            # the service's referrals move into the patient record's referral module
LEGACY_EXPORT = D(2026, 6, 19)         # the legacy referral database's final export
CENSUS = D(2026, 12, 31)
GROUP_START, GROUP_LAST = D(2027, 4, 1), D(2027, 9, 16)
PULL_APP, PULL_EPR, PULL_HUB, PULL_ESR, PULL_LD = D(2027, 1, 6), D(2027, 1, 6), D(2027, 1, 8), D(2027, 1, 4), D(2027, 1, 5)
PAPER_DATE, MEETING = D(2027, 1, 21), D(2027, 2, 4)
STANDARD_DATE = D(2026, 10, 12)
DBT_STANDARD_DATE = D(2025, 9, 1)
LD_REPORT_DATE = D(2025, 6, 27)
CATALOGUE_REBUILD = D(2025, 4, 1)      # PTD-114's code passes from the four-day course to the one-day refresher
BST_START = dt.datetime(2026, 3, 29, 1, 0)
BST_END = dt.datetime(2026, 10, 25, 1, 0)

BLOCKS, BLOCK_MIN, DAY_START = 8, 90, 9 * 60
PROMPTS = 14 * BLOCKS
COMPLETE = PROMPTS // 2
HIGH = 2.0
LINE = 30.0
COLLAB_TIMES = (9, 12, 15, 18, 21)

F_V3 = "mood_app_export_v3_2026-01-05_to_2026-06-14.csv"
F_V4 = "mood_app_export_v4_2026-06-15_to_2026-12-27.csv"
F_ENROL = "mood_app_enrolments_2025-2026.csv"
F_REGISTER = "assessment_fortnights_register_2026.xlsx"
F_EPISODES = "cmht_care_episodes_2025-2026.csv"
F_STANDARD = "sallowdene_mood_monitoring_standard_v1-1.pdf"
F_PAPER = "dbt_skills_groups_2027-28_committee_paper.docx"
F_ESR = "esr_clinical_assignments_2027-01-04.csv"
F_LEARN = "learning_records_2022-04_to_2026-12.csv"
F_CATALOGUE = "learning_catalogue_2026.xlsx"
F_LDREPORT = "learning_and_development_annual_report_2024-25.pdf"
F_DBTSTD = "cen_service_dbt_programme_operating_standard_v3.pdf"
F_MODULE = "cen_referrals_module_export_2027-01-08.csv"
F_LETTERS = "cen_correspondence_log_2023-04_to_2027-01.csv"
F_INDEX = "patient_index_extract_2027-01-06.csv"
F_PHQ = "phq9_gad7_at_assessment_2026.csv"
F_PILOT = "sallowdene_mood_app_pilot_evaluation_2025.pdf"

X_GOLD = "dbt_skills_groups_2027_28.xlsx"
P_GOLD = "team_instability_2026.png"


def rng(*keys):
    """A generator seeded from the build seed and the keys, so each purpose draws from its own stream."""
    h = hashlib.sha256(("%d|" % SEED + "|".join(str(k) for k in keys)).encode()).digest()
    return np.random.default_rng(int.from_bytes(h[:8], "little"))


def round_half_up(x, nd=1):
    q = Decimal(1).scaleb(-nd)
    return float(Decimal(repr(float(x))).quantize(q, rounding=ROUND_HALF_UP))


def uk_date(d):
    return "%d %s %d" % (d.day, d.strftime("%B"), d.year)


def is_bst(t):
    """t: a naive UTC datetime."""
    return BST_START <= t < BST_END


def local_to_utc(t):
    """t: a naive Europe/London wall time in 2026, never inside the skipped or repeated hour (prompts run 9:00 to
    21:30)."""
    guess = t - dt.timedelta(hours=1)
    return guess if is_bst(guess) else t


def utc_to_local(t):
    return t + dt.timedelta(hours=1) if is_bst(t) else t


def nhs_number(r):
    """A ten-digit NHS number with a valid modulus 11 check digit."""
    while True:
        d = [int(x) for x in r.integers(0, 10, 9)]
        if d[0] == 0:
            continue
        s = sum(v * (10 - i) for i, v in enumerate(d))
        c = 11 - s % 11
        if c == 11:
            c = 0
        if c == 10:
            continue
        return "".join(map(str, d)) + str(c)
