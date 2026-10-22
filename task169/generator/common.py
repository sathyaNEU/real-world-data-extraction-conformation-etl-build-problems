"""task169 shared constants and helpers: the in-fiction calendar, the random streams, the file names and the
writers that make every file reproduce byte for byte."""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import io

import numpy as np

STATE = "Pembroke"
COMMISSION = "Pembroke Sentencing and Policy Commission"
DOC = "Pembroke Department of Corrections"
BOARD = "Pembroke Board of Parole"
AOC = "Administrative Office of the Courts"
SBI = "State Bureau of Identification"
ACT = "Act 26-114"

RECORD_START = dt.date(2019, 1, 1)
CUT = dt.date(2026, 9, 30)                 # records run to this day
PULL = dt.date(2026, 10, 9)                # the agencies' extracts were pulled by this day
ASSEMBLED = dt.date(2026, 10, 14)          # the Commission's data folder assembled
ACT_SIGNED = dt.date(2026, 6, 30)
ACT_IN_FORCE = dt.date(2027, 1, 1)
COHORT_YEAR = 2027
WINDOW = 730                               # days from release
BOARD_SWITCH = dt.date(2024, 7, 1)         # the Board's new case-management system went live

DISTRICTS = ("Garrison", "Ridgway", "Linwood", "Corliss")
CLASSES = ("F1", "F2", "M")                # felony class A-B, felony class C-E, misdemeanour

def stream(name):
    h = int.from_bytes(hashlib.sha256(("task169/" + name).encode()).digest()[:8], "little")
    return np.random.default_rng(h)


def days(a, b):
    return (b - a).days


def add(d, n):
    return d + dt.timedelta(days=int(n))


def write_csv(path, head, rows, crlf=True, delim=","):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\r\n" if crlf else "\n", delimiter=delim)
    w.writerow(head)
    for r in rows:
        w.writerow(r)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(buf.getvalue())
    return len(rows)


def read_csv(path, delim=","):
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh, delimiter=delim))


def edge(v, unit):
    c = round(v / unit) * unit
    return unit / 2 - abs(v - c)

COUNTIES = {"Garrison": ("Garrison", "Kesler", "Marlow"), "Ridgway": ("Ridgway", "Hollister", "Danvers"),
            "Linwood": ("Linwood", "Prescott", "Whitlow"), "Corliss": ("Corliss", "Brenner", "Oakhurst")}
COUNTY_W = (0.58, 0.25, 0.17)
OFFICE = {"Garrison": "D1", "Ridgway": "D2", "Linwood": "D3", "Corliss": "D4"}
FACILITIES = ("SCI-KTR", "SCI-FNW", "SCI-DNM", "SCI-LKV", "SCI-BRW")
RECEPTION = "PRC"
OMS_UPGRADE = dt.date(2022, 3, 14)      # the Department's offender management system upgrade (movement codes)
BOARD_GOLIVE = dt.date(2026, 1, 5)      # the Board's new case system; legacy entry ran in parallel to 16 Jan
BOARD_PARALLEL_END = dt.date(2026, 1, 23)
BOARD_MIGRATE_CUT = dt.date(2026, 1, 2) # cases open at the close of 2 January 2026 were migrated
FY_START, FY_END = dt.date(2025, 7, 1), dt.date(2026, 6, 30)

F_REL = "doc_release_movements_2019-2026.csv"
F_ADM = "doc_admission_movements_2019-2026.csv"
F_ARR = "sbi_arrests_released_persons_2019-2026.parquet"
F_AOC = "aoc_case_dispositions_2019-2026.csv"
F_XW = "sbi_doc_number_crosswalk.csv"
F_BLEG = "board_violation_actions_legacy_2019-2026.xlsx"
F_BNEW = "board_case_decisions_2026.csv"
F_PROJ = "doc_projected_releases_2027.csv"
F_DEATH = "vital_records_death_matches_2019-2026.csv"
F_ACT = "act_26-114_enrolled.pdf"
F_METH = "prison_population_projection_methodology_2026.pdf"
F_CAP = "doc_population_capacity_report_2026-09.xlsx"
F_PRAT = "prat_validation_study_2023.pdf"
F_CASE = "parole_caseload_by_office_2025-2026.csv"
F_DICT = "data_dictionary.xlsx"
F_MAN = "export_manifest.csv"
ALL_FILES = (F_REL, F_ADM, F_ARR, F_AOC, F_XW, F_BLEG, F_BNEW, F_PROJ, F_DEATH, F_ACT, F_METH, F_CAP, F_PRAT,
             F_CASE, F_DICT, F_MAN)
DISTRACTORS = (F_PRAT, F_CASE)
