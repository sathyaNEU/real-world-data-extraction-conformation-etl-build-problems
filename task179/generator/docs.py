"""task179 documents: the Registry's ARC cutover notes and the Planning Office's projection conventions (PDF), the
data dictionary (text). Their text is held here as data so checks.py can quote it and verify.py can read it back."""
from __future__ import annotations

import datetime as dt

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                        # noqa: E402
from reportlab.lib.pagesizes import A4                                                  # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                         # noqa: E402
from reportlab.lib.units import mm                                                      # noqa: E402
from reportlab.pdfbase import pdfmetrics                                                # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                            # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle   # noqa: E402

import common as C            # noqa: E402
import postprocess as PP      # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/"
for _n, _f in (("Serif", "liberation/LiberationSerif-Regular.ttf"), ("Serif-Bold", "liberation/LiberationSerif-Bold.ttf"),
               ("Sans", "liberation/LiberationSans-Regular.ttf"), ("Sans-Bold", "liberation/LiberationSans-Bold.ttf")):
    pdfmetrics.registerFont(TTFont(_n, FONT_DIR + _f))
INK = colors.HexColor("#1b1b1b")
GREY = colors.HexColor("#555555")

# ------------------------------------------------------------------ the Planning Office's conventions
ENROLLED_PIN = ("A student is enrolled at a census when the census history shows an enrolled programme attempt for "
                "the student on that date. A student on approved leave is not enrolled.")
INTAKE_PIN = ("The first-year intake of a year is the first-time bachelor's entrants with an enrolled programme attempt "
              "at that year's census. Entrants admitted with credit from another institution are not first-time "
              "entrants.")
CALL_PIN = ("The projection reports how many of the 2026 intake will not be enrolled at the 1 October 2027 census, to "
            "the nearest 250.")
SELECT_PIN = ("Where several models of the same outcome are fitted to the same intakes, the projection uses the one "
              "with the lowest Akaike information criterion.")
GROUP_PIN = ("The teaching plan counts teaching groups: the students taught together, in one room at one time. Each "
             "distinct set of classes meeting together in one room on the same day, start and teaching weeks is one group "
             "however often it meets, so two classes that share only one of their meetings make three groups: the two at "
             "the shared meeting and each at its own. A group belongs to the faculty that owns its paper, and its size is "
             "the number of students enrolled at the census whom it teaches. A cancelled class is not a teaching group.")

# the Registry's own statement that a class enrolment record means the same on both sides of the cutover
COMPARABLE = ("The change is in who chooses an entrant's classes, not in what a class enrolment records: in both "
              "systems it is the student on the class's list at the census, and the two systems' first-year class "
              "extracts hold the same thing.")

CONVENTIONS = [
    ("1. Purpose", [
        "Each October, once the census is final, Planning and Insight projects the continuing enrolment for the next "
        "academic year. The projection sets the number of second-year teaching groups each faculty schedules in the "
        "teaching plan and the continuing-student fee line of the budget, and goes to the Senior Leadership Team in "
        "November with the plan.",
        "These conventions govern the projection for 2027 and the working files behind it."]),
    ("2. Census and enrolment", ["The census is taken on 1 October.", ENROLLED_PIN]),
    ("3. The first-year intake", [INTAKE_PIN, CALL_PIN, SELECT_PIN]),
    ("4. Teaching groups", [GROUP_PIN,
                            "Semester 1 groups are taken from the Semester 1 timetable as it stood at the census."]),
]

CUTOVER = [
    ("1. Dates", [
        "SIRIUS was closed to updates at 17:00 on Friday 29 May 2026 and ARC went live on Monday 1 June 2026. Student, "
        "programme attempt, results and census history were loaded from SIRIUS as at 29 May. Census histories from "
        "2019 are held in ARC; earlier censuses stay in the SIRIUS archive."]),
    ("2. Student identifiers", [
        "ARC identifies a student by an ARC ID (C followed by eight digits). Every student with a SIRIUS record active "
        "at the cutover, or enrolled at the 2025 census, was given an ARC ID, and the crosswalk holds both numbers. "
        "Students first admitted from June 2026 hold an ARC ID only. Census rows before 2026 carry SIRIUS student "
        "numbers; the 2026 census carries ARC IDs.",
        "Programme transfers approved before the cutover carry the SIRIUS student number in the transfers register, "
        "and transfers approved in ARC carry the ARC ID."]),
    ("3. Codes", ["Code values changed as shown in Table 1. Programme codes are unchanged."]),
    ("Table 1. Code changes", []),
    ("4. Census extract", [
        "One row per programme attempt per census. ATTEMPT_SEQ is the attempt's sequence on the student's record. "
        "Census dates are written day first in SIRIUS rows and as ISO dates in ARC rows. EFTS is the attempt's "
        "equivalent full-time student load for the year."]),
    ("5. Timetable", [
        "Timetabling exports the Semester 1 timetable from ARC Scheduling, one row per weekly meeting of a class. A "
        "class taught in different rooms in different weeks has a row for each room. Teacher is the "
        "class's teacher of record."]),
    ("6. Class enrolments", [
        "In SIRIUS the Registry entered first-year entrants' Semester 1 class enrolments. ARC has no Registry entry "
        "of class enrolments: from Semester 1 2026 entrants choose their classes and enrol in them themselves.",
        COMPARABLE]),
]
CODE_TABLE = [
    ("Field", "SIRIUS", "ARC"),
    ("Faculty", "ASS, BUS, SCI, ENG, HLT", "FASS, FBUS, FSCI, FENG, FHLT"),
    ("Census status", "EN enrolled; LV approved leave", "Enrolled; On leave"),
    ("Attendance", "FT; PT", "Full-time; Part-time"),
    ("Week-6 progress rating", "S, C, R", "Satisfactory, Some concern, At risk"),
    ("Class", "five-digit class number, unique in a term", "paper-study period-number, e.g. UNIV101-26S1-014"),
    ("Census date", "01/10/2025", "2026-10-01"),
]


def _styles():
    base = ParagraphStyle("b", fontName="Serif", fontSize=10.5, leading=14, textColor=INK, spaceAfter=6)
    head = ParagraphStyle("h", fontName="Serif-Bold", fontSize=11, leading=15, textColor=INK, spaceBefore=8, spaceAfter=4)
    title = ParagraphStyle("t", fontName="Sans-Bold", fontSize=15, leading=19, textColor=INK, spaceAfter=4)
    sub = ParagraphStyle("s", fontName="Sans", fontSize=9.5, leading=13, textColor=GREY, spaceAfter=10)
    small = ParagraphStyle("f", fontName="Sans", fontSize=8.5, leading=11, textColor=GREY, spaceBefore=10)
    return base, head, title, sub, small


def _esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _pdf(path, title, sub, sections, foot=None, table=None, table_after=None, issued=None, author="", widths=None):
    base, head, tstyle, sstyle, small = _styles()
    story = [Paragraph(_esc(title), tstyle)]
    if sub:
        story.append(Paragraph(_esc(sub), sstyle))
    for h, paras in sections:
        if h:
            story.append(Paragraph(_esc(h), head))
        for p in paras:
            story.append(Paragraph(_esc(p), base))
        if table is not None and h == table_after:
            t = Table(table, hAlign="LEFT", colWidths=widths, repeatRows=1)
            t.setStyle(TableStyle([("FONT", (0, 0), (-1, 0), "Sans-Bold", 8.5), ("FONT", (0, 1), (-1, -1), "Sans", 8.5),
                                   ("LINEBELOW", (0, 0), (-1, 0), 0.6, INK), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
                                   ("TOPPADDING", (0, 0), (-1, -1), 2.5), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
            story.append(Spacer(1, 4))
            story.append(t)
            story.append(Spacer(1, 6))
    if foot:
        story.append(Paragraph(_esc(foot), small))

    def page(canvas, doc):
        canvas.saveState()
        canvas.setFont("Sans", 8)
        canvas.setFillColor(GREY)
        canvas.drawString(20 * mm, 12 * mm, title)
        canvas.drawRightString(A4[0] - 20 * mm, 12 * mm, "Page %d" % doc.page)
        canvas.restoreState()

    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm,
                            bottomMargin=20 * mm, title=title, author=author, subject="", creator="", producer="")
    doc.build(story, onFirstPage=page, onLaterPages=page)
    stamp = ("D:%04d%02d%02d%02d%02d%02d+13'00'" % (issued.year, issued.month, issued.day, 10, 12, 0)).encode()
    PP.normalize_pdf(path, stamp, stamp)


def write_conventions(path):
    _pdf(path, "Continuing Enrolment Projection 2027: Conventions",
         "%s, Planning and Insight. Issued 5 October 2026. Keri Keating, Director of Planning and Insight." % C.UNI,
         CONVENTIONS, issued=dt.date(2026, 10, 5), author="Keri Keating",
         foot="Questions on these conventions go to Planning and Insight.")


def write_cutover(path):
    _pdf(path, "SIRIUS to ARC Cutover: Notes for Data Users",
         "%s, Registry, Student Systems. Revised 14 August 2026. Malcolm Hussey, Student Systems Manager." % C.UNI,
         CUTOVER, table=CODE_TABLE, table_after="Table 1. Code changes", issued=dt.date(2026, 8, 14),
         author="Malcolm Hussey", widths=[40 * mm, 55 * mm, 75 * mm],
         foot="First issued 1 June 2026. This revision adds sections 5 and 6.")


DICT = """DATA DICTIONARY, CONTINUING ENROLMENT PROJECTION 2027 (Planning and Insight, assembled 16 October 2026)

sirius_fy_cohort_classes_2019_2025.csv  SIRIUS first-year cohort extract: one row per Semester 1 class enrolment of a
  first-time entrant at the census of the entrant's first year, intakes 2019 to 2025
  STUDENT_NO    SIRIUS student number
  TERM          term (yyyyS1)
  PAPER         paper code
  CLASS_NBR     class number
  POINTS        credit points
  CENSUS_STAT   E enrolled at the census
  COHORT_YR     intake year

arc_s1_2026_first_year_classes.csv  ARC first-year cohort extract: one row per Semester 1 2026 class enrolment of a
  first-time entrant at the 2026 census
  arc_student_id, study_period, paper_code, class_code, credit_points, enrolment_status, census_date

census_enrolments_2019_2026.csv  Registry census history: one row per programme attempt per student at each 1 October
  census, 2019 to 2026 (see the cutover notes, section 4)
  CENSUS_DATE, STUDENT_ID, SOURCE (SIRIUS or ARC), ATTEMPT_SEQ, PROGRAMME, FACULTY, YEAR_OF_STUDY (4 means fourth or
  later), ATTENDANCE, EFTS, STATUS

sirius_arc_student_crosswalk.csv  Registry: SIRIUS student number and ARC ID of every migrated student
  SIRIUS_STUDENT_NO, ARC_ID, MIGRATED

admissions_entrants_2019_2026.xlsx  Admissions: one sheet per intake, one row per new student enrolled in the intake
  year (first-time entrants and entrants with credit)
  Student No / Student ID   SIRIUS student number (2019 to 2025 sheets) or ARC ID (2026 sheet)
  Entry Basis               First-time or Credit transfer
  Programme, Conjoint With  programme of admission and, for a conjoint combination, the second programme
  Faculty                   faculty of the programme of admission (SIRIUS codes)
  Attendance                FT or PT at admission
  Date of Birth, Gender, Home Region
  First in Family           Y where neither parent holds a degree (self-reported)
  ASC Points / ASC Score    Aldmark Secondary Certificate points (0 to 300)
  Hardship Grant            Y where an entry hardship grant was paid
  Accommodation             hall of residence, Family home or Private
  Living-Learning Community Y where the student joined a hall's living-learning community
  Offer Accepted            date the offer of place was accepted

progress_check_wk6_2019_2026.csv  Student Success: week-6 progress check of first-time entrants, one row per student
  per Semester 1 class; RATING blank where the teacher did not return the check
  YEAR, CHECK, STUDENT, PAPER, CLASS (SIRIUS class number or ARC class code), RATING

s1_2026_class_timetable.xlsx  Timetabling: Semester 1 2026 timetable as at the census, one row per weekly meeting
  Class Code, Paper, Paper Title, Owning Faculty, Level, Day, Start, End, Teaching Weeks, Room, Room Capacity, Teacher,
  Enrolled at Census (the census enrolment ARC Scheduling holds for the class), Class Status

arc_s1_2026_class_enrolments.csv  ARC class enrolment extract: one row per Semester 1 2026 class enrolment at 200 level
  and above at the 2026 census
  arc_student_id, study_period, paper_code, class_code, credit_points, enrolment_status, census_date

programme_catalogue_2026.csv  Academic Office: bachelor's programmes and approved conjoint combinations
  TYPE, CODE, TITLE, OWNING_FACULTY, YEARS_FT, COMPONENTS (a combination's programmes, first-listed first)

programme_transfers_2025_2026.csv  Registry: internal programme transfers approved 1 October 2025 to 30 September 2026
  STUDENT, FROM_PROGRAMME, TO_PROGRAMME, APPROVED, EFFECTIVE, REASON

hall_occupancy_weekly_2019_2026.csv  Accommodation Services: beds and occupied beds by hall and teaching week

national_school_leavers_2019_2026.csv  Ministry of Education statistics (Aldmark): school leavers by region, those with
  university entrance, and those enrolled in a degree the following year

arc_cutover_notes_registry.pdf  Registry
continuing_enrolment_projection_conventions_2027.pdf  Planning and Insight
"""


def write_dict(path):
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(DICT.replace("\n", "\r\n"))
