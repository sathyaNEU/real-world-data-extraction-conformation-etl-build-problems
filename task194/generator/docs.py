"""The network's own governing documents: the improvement partnership charter, the complication indicator
specification with its two appendices, and the improvement unit's notes on the cycle."""
import os

from reportlab import rl_config
rl_config.invariant = 1
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import world as W

SS = getSampleStyleSheet()
BODY = ParagraphStyle("b", parent=SS["BodyText"], fontName="Times-Roman", fontSize=9.5, leading=13,
                      alignment=TA_JUSTIFY, spaceAfter=5)
H1 = ParagraphStyle("h1", parent=SS["Heading1"], fontName="Times-Bold", fontSize=13, spaceAfter=8)
H2 = ParagraphStyle("h2", parent=SS["Heading2"], fontName="Times-Bold", fontSize=10.5, spaceAfter=4,
                    spaceBefore=8)
SMALL = ParagraphStyle("s", parent=BODY, fontSize=8, leading=10.5)
CELL = ParagraphStyle("c", fontName="Times-Roman", fontSize=8, leading=10)
CELLB = ParagraphStyle("cb", fontName="Times-Bold", fontSize=8, leading=10)
TBL = TableStyle([("GRID", (0, 0), (-1, -1), 0.3, colors.Color(0.45, 0.45, 0.45)),
                  ("BACKGROUND", (0, 0), (-1, 0), colors.Color(0.90, 0.90, 0.88)),
                  ("VALIGN", (0, 0), (-1, -1), "TOP"),
                  ("LEFTPADDING", (0, 0), (-1, -1), 3), ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                  ("TOPPADDING", (0, 0), (-1, -1), 1.6), ("BOTTOMPADDING", (0, 0), (-1, -1), 1.6)])


def wrap(rows):
    return [[Paragraph(str(c), CELLB if i == 0 else CELL) for c in row] for i, row in enumerate(rows)]


def _doc(path, title):
    return SimpleDocTemplate(path, pagesize=A4, title=title, author="", subject="", creator="",
                             leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm,
                             bottomMargin=18 * mm)


def charter(target):
    path = os.path.join(target, "improvement_partnership_charter_v3.pdf")
    d = _doc(path, "Clinical Improvement Partnership charter")
    f = [Paragraph("Mid-Rivers Health Network: Clinical Improvement Partnership charter", H1),
         Paragraph("Version 3.0, endorsed by the Clinical Quality Committee and effective 1 July 2024. "
                   "Parts 1 to 3, Part 5 and schedules 1 to 3 are not reproduced in this extract.", SMALL),
         Paragraph("Part 4 Placement of the embedded team", H2),
         Paragraph("4.1 The partnership places its embedded improvement team with one inpatient unit for "
                   "one quarter in each cycle. The quarter the team is embedded with a unit is the "
                   "assessment quarter for that placement. The placement for a cycle is decided before the "
                   "assessment quarter begins, on the indicator data closed at the time of the decision, "
                   "and is noted by the Clinical Quality Committee at its March, June, September or "
                   "December meeting.", BODY),
         Paragraph("4.2 Every acute inpatient unit still reporting under its own cost centre at the "
                   "decision date, with four or more closed quarters of reported indicator data under the "
                   "current specification, is eligible for a placement, except a unit the team has been "
                   "placed with in the previous twelve closed quarters and except the unit the team is "
                   "placed with when the placement is decided. The partnership does not return to a unit "
                   "inside three years, so that the gains a unit holds are the unit's own to hold.", BODY),
         Paragraph("4.3 A placement is made with the unit carrying the most avoidable complications. The "
                   "complications a unit carries as avoidable over a period are the complications its own "
                   "patients had, less the complications that patients of the same risk band and age band "
                   "ordinarily have, counted patient by patient and summed over the unit's episodes in "
                   "that period.", BODY),
         Paragraph("4.4 A placement is assessed on the separations planned for the unit for the assessment "
                   "quarter, as published in the network's activity plan for that quarter.", BODY),
         Paragraph("4.5 The Director of Clinical Improvement recommends the placement for each cycle and "
                   "reports to the committee on the placement made, the complications it avoided and the "
                   "practice changes the unit holds after the team leaves.", BODY),
         Paragraph("4.6 The embedded team is 2.4 full-time equivalent improvement staff for the quarter, "
                   "funded from the partnership's recurrent allocation. The team works on the unit's own "
                   "practice and takes no part in coding, reporting or the audit of the indicator.", BODY),
         Paragraph("4.7 Where a unit the team is placed with is reconfigured, amalgamated or closed during "
                   "the assessment quarter, the cycle is reported as discontinued and the placement does not "
                   "count against clause 4.2.", BODY),
         Paragraph("Part 6 Reporting", H2),
         Paragraph("6.1 The partnership reports each cycle to the committee, and annually to the board, on "
                   "the placements made and the complications avoided across the network.", BODY),
         Paragraph("6.2 The partnership's own performance is reported against the hospital-acquired "
                   "complication indicator as the current specification defines it. The partnership "
                   "publishes no indicator of its own.", BODY)]
    d.build(f)
    return path


def specification(target):
    path = os.path.join(target, "hac_indicator_specification_v4.pdf")
    d = _doc(path, "Hospital-acquired complication indicator specification 4.0")
    strata = [["Risk band", "Under 50", "50 to 64", "65 to 79", "80 and over"]]
    for band in ("ORTH-MAJ", "ORTH-MIN", "SURG-MAJ", "SURG-MIN", "MED-COMPLEX", "MED-GEN"):
        strata.append([band] + ["%.4f" % W.STRATUM_RATE[(band, a)] for a in W.AGE_BANDS])
    rows22 = [["Code", "Category, 2022 revision", "Group"]]
    for c, n, g in W.LIST_2022:
        rows22.append([c, n, "%s %s" % (g, W.GROUP_NAME[g])])
    rows26 = [["Code", "Category, 2026 revision", "Group"]]
    for c, n, g in W.LIST_2026:
        rows26.append([c, n, "%s %s" % (g, W.GROUP_NAME[g])])
    f = [Paragraph("Hospital-acquired complication indicator: specification 4.0", H1),
         Paragraph("Clinical Governance, Mid-Rivers Health Network. Effective for separations from "
                   "1 July 2024. Supersedes specification 3.2. Sections 1, 4 and 5 and the worked "
                   "examples are not reproduced in this extract.", SMALL),
         Paragraph("2 Definition", H2),
         Paragraph("2.1 The indicator counts episodes that recorded one or more hospital-acquired "
                   "complications on the national complication list in force at separation. An episode "
                   "that recorded more than one complication counts once.", BODY),
         Paragraph("2.2 The denominator is acute multi-day episodes: episodes with a care type of Acute, "
                   "a length of stay of one night or more, separated in the period from an in-scope unit, "
                   "and carrying a diagnosis related group that the risk band map assigns to a band.", BODY),
         Paragraph("2.3 In-scope units are units whose service type is acute inpatient. Sub-acute "
                   "rehabilitation units and psychiatric inpatient units are outside the indicator.", BODY),
         Paragraph("2.4 An episode excluded from the denominator is excluded from the numerator.", BODY),
         Paragraph("2.5 An episode is reported in the period its separation date falls in.", BODY),
         Paragraph("3 Risk adjustment and reporting", H2),
         Paragraph("3.1 The expected complications of a group of episodes are the sum, over strata, of the "
                   "episodes in the stratum multiplied by the stratum's published rate. A stratum is a risk "
                   "band and an age band. The rates published with this specification are in Appendix A and "
                   "are not re-estimated between specifications.", BODY),
         Paragraph("3.2 A unit's standardised ratio for a period is its observed complications divided by "
                   "its expected complications. Its adjusted rate is the standardised ratio multiplied by "
                   "the reference rate of 96.6 complications per 1,000 episodes.", BODY),
         Paragraph("3.3 A unit's standardised ratio is reported for each closed quarter and for the "
                   "specification period to date, being every closed quarter from 1 July 2024. No other "
                   "period is reported for a unit.", BODY),
         Paragraph("3.4 Where the expected complications of a period are required before the period is "
                   "observed, they are the separations planned for the unit multiplied by the unit's "
                   "expected complications per separation over the specification period to date.", BODY),
         Paragraph("3.5 Values reported for periods before 1 July 2024 were produced under specification "
                   "3.2 on a different risk model and are not comparable with values under this "
                   "specification.", BODY),
         Paragraph("3.6 A unit formed by amalgamation is reported under its own cost centre from the date "
                   "of effect. Its predecessor units are reported under their own cost centres for earlier "
                   "periods and are not reported again under the amalgamated cost centre.", BODY),
         Paragraph("3.7 A quarter is reported once the coding of its separations is complete. Coding for a "
                   "quarter closes eight weeks after the quarter ends.", BODY),
         Spacer(1, 6),
         Paragraph("Appendix A Published stratum rates", H2),
         Paragraph("Complications expected per in-scope episode, by risk band and age band at admission. "
                   "Derived from network activity in the year ended 30 June 2024 and published with this "
                   "specification.", SMALL),
         Table(wrap(strata), colWidths=[30 * mm] + [24 * mm] * 4, style=TBL),
         Spacer(1, 8),
         Paragraph("Appendix B The national complication list", H2),
         Paragraph("Codes as recorded under each revision, with the reporting group each code belongs to. "
                   "The 2026 revision renumbered categories HAC03 to HAC06 and folded the 2022 revision's "
                   "HAC13 into HAC03. A code is read against the revision in force at separation.", SMALL),
         Table(wrap(rows22), colWidths=[18 * mm, 76 * mm, 66 * mm], style=TBL),
         Spacer(1, 6),
         Table(wrap(rows26), colWidths=[18 * mm, 76 * mm, 66 * mm], style=TBL)]
    d.build(f)
    return path


def thread(target):
    """The improvement unit's own notes on the cycle: two people, logistics, no ranking and no method."""
    director = W.PEOPLE["director"][0]
    gov = W.PEOPLE["governance"][0]
    path = os.path.join(target, "placement_cycle_notes.txt")
    text = """Notes on the IP-10 placement cycle (quarter from 1 April 2027)
Kept by Clinical Improvement. Latest note first.

5 March 2027, %(gov)s
Extract is out and in the cycle folder, with the complication detail and the quarterly series beside
it. Coding for the December quarter closed on 28 February. The March quarter will not be coded until
the end of May, which is after your committee. The activity plan for the April quarter went up on
20 February and I have put a copy in the folder with the unit register and the hospital reference.

3 March 2027, %(director)s
Thanks. Add the placement register, and the three unit-level files the consumer, nursing and
infection prevention teams sent across, in case the committee asks what else moved. Papers close on
the 20th.

24 February 2027, %(director)s
The team finishes at Rehabilitation and Aged Care on 31 March and starts wherever we land on
1 April, so the recommendation goes to the committee on the 24th with the charter extract attached.

19 February 2027, %(gov)s
Two housekeeping notes. The comorbidity score is keyed on about six episodes in seven and the rate
drops away in January and over winter, which is when the coding queue is longest. The sub-acute and
mental health units are in the extract but not in the quarterly series.
""" % dict(director=director, gov=gov)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    return path
