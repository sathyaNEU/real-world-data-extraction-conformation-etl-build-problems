"""task179 shared constants: the in-fiction calendar, the university's structure, file names, random streams and
byte-stable writers."""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import io

import numpy as np

UNI = "Corriemoor University"
COUNTRY = "Republic of Aldmark"
TASK = "task179"

INTAKES = list(range(2019, 2027))          # first-time entrant cohorts in the record; 2026 is the forward cohort
FORWARD = 2026
PRE = list(range(2014, 2019))              # earlier cohorts, present only as continuing students
CENSUS_YEARS = list(range(2019, 2027))     # 1 October censuses in the census history
CUTOVER = dt.date(2026, 6, 1)              # SIRIUS to ARC
ASSEMBLED = dt.date(2026, 10, 16)


def census_date(y):
    return dt.date(y, 10, 1)


FACULTIES = [
    ("ASS", "Faculty of Arts and Social Sciences"),
    ("BUS", "Faculty of Business and Law"),
    ("SCI", "Faculty of Science"),
    ("ENG", "Faculty of Engineering and Computing"),
    ("HLT", "Faculty of Health Sciences"),
]
FAC_CODES = [f for f, _ in FACULTIES]
FAC_SHARE = {"ASS": 0.24, "BUS": 0.22, "SCI": 0.20, "ENG": 0.16, "HLT": 0.18}
FAC_EFFECT = {"ASS": 0.10, "BUS": 0.0, "SCI": -0.05, "ENG": 0.06, "HLT": -0.14}

# programme code, title, faculty, years full time, share within faculty, first-year programme papers
PROGRAMMES = [
    ("BA", "Bachelor of Arts", "ASS", 3, 0.55, ["HIST110", "ENGL110", "POLS110", "PHIL110"]),
    ("BSOCSC", "Bachelor of Social Sciences", "ASS", 3, 0.30, ["SOCI110", "PSYC110"]),
    ("BFA", "Bachelor of Fine Arts", "ASS", 3, 0.15, ["FINE110"]),
    ("BCOM", "Bachelor of Commerce", "BUS", 3, 0.50, ["ACCT110", "MKTG110"]),
    ("BBUS", "Bachelor of Business", "BUS", 3, 0.25, ["MGMT110"]),
    ("LLB", "Bachelor of Laws", "BUS", 4, 0.25, ["LAWS110"]),
    ("BSC", "Bachelor of Science", "SCI", 3, 0.70, ["BIOL110", "CHEM110", "PHYS110", "STAT110"]),
    ("BBIOMED", "Bachelor of Biomedical Science", "SCI", 3, 0.30, ["BMED110"]),
    ("BENGH", "Bachelor of Engineering with Honours", "ENG", 4, 0.60, ["ENGR120"]),
    ("BCOMPSC", "Bachelor of Computer Science", "ENG", 3, 0.40, ["COMP110"]),
    ("BNURS", "Bachelor of Nursing", "HLT", 3, 0.45, ["NURS110"]),
    ("BHSC", "Bachelor of Health Sciences", "HLT", 3, 0.35, ["HSCI110"]),
    ("BSPEX", "Bachelor of Sport and Exercise Science", "HLT", 3, 0.20, ["SPEX110"]),
]
PROG = {p[0]: p for p in PROGRAMMES}
CONJOINTS = [("BA", "LLB"), ("BCOM", "LLB"), ("BSC", "BCOM"), ("BA", "BSC"), ("BENGH", "BCOM"), ("BCOMPSC", "BSC"),
             ("BHSC", "BCOM"), ("BSPEX", "BCOM")]

# first-year papers every full-time entrant of a faculty takes in Semester 1 (with UNIV101)
FAC_PAPERS = {
    "ASS": ["ARTS101", "ARTS102"],
    "BUS": ["BUSN101", "ECON101"],
    "SCI": ["SCIE101", "MATH101"],
    "ENG": ["ENGR101", "MATH151"],
    "HLT": ["HLTH101", "HLTH102"],
}
UNIV = "UNIV101"
ELECTIVES = sorted(set(p for pr in PROGRAMMES for p in pr[5]))
CLASS_CAP = 30
BLOCK = 28

HALLS = ["Ferrier Hall", "Ashby House", "Linton Court", "Stanmore Hall", "Greyfriars Hall"]

# file names in the pack
F_SCLS = "sirius_fy_cohort_classes_2019_2025.csv"
F_ACLS = "arc_s1_2026_first_year_classes.csv"
F_CENSUS = "census_enrolments_2019_2026.csv"
F_XWALK = "sirius_arc_student_crosswalk.csv"
F_ADM = "admissions_entrants_2019_2026.xlsx"
F_PROG = "progress_check_wk6_2019_2026.csv"
F_TT = "s1_2026_class_timetable.xlsx"
F_CAT = "programme_catalogue_2026.csv"
F_TRF = "programme_transfers_2025_2026.csv"
F_CUT = "arc_cutover_notes_registry.pdf"
F_CONV = "continuing_enrolment_projection_conventions_2027.pdf"
F_DICT = "data_dictionary.txt"
F_HALL = "hall_occupancy_weekly_2019_2026.csv"
F_NSL = "national_school_leavers_2019_2026.csv"
DISTRACTORS = [F_HALL, F_NSL]

DELIV_XLSX = "continuing_enrolment_2027.xlsx"
DELIV_PNG = "s1_2026_teaching_groups.png"


SALT = ""      # screening only: a different world draw; the shipped world uses the empty salt


def stream(name):
    h = int.from_bytes(hashlib.sha256(("task179/" + SALT + name).encode()).digest()[:8], "little")
    return np.random.default_rng(h)


def write_csv(path, head, rows, crlf=True):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\r\n" if crlf else "\n")
    w.writerow(head)
    n = 0
    for r in rows:
        w.writerow(["" if v is None else v for v in r])
        n += 1
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(buf.getvalue())
    return n


def dmy(d):
    return "" if d is None else "%02d/%02d/%04d" % (d.day, d.month, d.year)


def iso(d):
    return "" if d is None else d.isoformat()
