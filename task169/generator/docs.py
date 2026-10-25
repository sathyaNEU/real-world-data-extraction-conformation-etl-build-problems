"""task169 documents: the enrolled Act, the Commission's projection methodology, the Department's 2023 tool
validation study (PDF), the capacity report and the data dictionary (Excel), the caseload extract and the export
manifest (CSV). Their text is held here as data so checks.py can quote it and verify.py can read it back."""
from __future__ import annotations

import datetime as dt
import os

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                        # noqa: E402
from reportlab.lib.pagesizes import letter                                              # noqa: E402
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

ACT_TITLE = "Act 26-114 of 2026 (House Bill 1407)"
ACT_HEAD = ("AN ACT amending Title 61 of the Pembroke Consolidated Statutes (Prisons and Parole), in parole "
            "violations, further providing for recommitment and for community sanctions, and providing for reporting.")
ACT = [
    ("Section 1. Short title.", [
        "This act shall be known and may be cited as the Supervision Violations Act."]),
    ("Section 2. Definitions.", [
        "The following words and phrases when used in this act shall have the meanings given to them in this section "
        "unless the context clearly indicates otherwise:",
        "\"Recommitment.\" The return of a parolee to the custody of the Department of Corrections by order of the "
        "board.",
        "\"Technical violation.\" A violation of a general or specific condition of parole that is not the parolee's "
        "conviction of a crime."]),
    ("Section 3. Recommitment.", [
        "(a) On and after January 1, 2027, the board shall not recommit a parolee for a technical violation.",
        "(b) An arrest, or a criminal charge pending against a parolee, shall not by itself be a ground for "
        "recommitment.",
        "(c) A parolee who is convicted of a crime committed while on parole and sentenced to a term of total "
        "confinement in a State correctional institution shall be committed to the department on that sentence, and "
        "the board may order that the unexpired term of parole be served before or after it."]),
    ("Section 4. Community sanctions.", [
        "(a) The board shall adopt a schedule of community sanctions for technical violations, which may include "
        "increased reporting, electronic monitoring, curfews, treatment and day reporting.",
        "(b) The board may detain a parolee in a county jail pending a violation hearing for not more than ten days, "
        "and the Commonwealth shall reimburse the county for each day of detention at the rate in effect for board "
        "detainers."]),
    ("Section 5. Reporting.", [
        "The board shall report to the Pembroke Sentencing and Policy Commission each quarter the violations reported, "
        "the sanctions imposed and the parolees detained under section 4(b)."]),
    ("Section 6. Effective date.", [
        "This act shall take effect January 1, 2027."]),
]
ACT_FOOT = ("Approved the 30th day of June, A.D. 2026. Enrolled copy, Legislative Reference Bureau, State of Pembroke.")

METH_TITLE = "Prison Population Projection 2027: Methodology"
METH_SUB = ("Pembroke Sentencing and Policy Commission, Research and Projections Unit. Issued 14 October 2026 for the "
            "projection presented to the appropriations committees of the General Assembly in January 2027.")
METH = [
    ("1. What the projection covers", [
        "1.1 The projection estimates the Department of Corrections population at the end of each fiscal year from "
        "2027-28 to 2031-32. It is built from three flows: new court commitments, releases, and returns of released "
        "people to Department custody.",
        "1.2 This document sets out the definitions used for releases and returns. The data are the extracts listed in "
        "the export manifest, drawn from the Department, the Board of Parole, the Administrative Office of the Courts "
        "and the State Bureau of Identification, with records to 30 September 2026."]),
    ("2. Release cohorts", [
        "2.1 A release cohort is the people the Department releases to parole in one calendar year, by release "
        "movement PAR (parole) or RPR (reparole).",
        "2.2 The 2027 cohort is every person on the Department's projected-release extract of 9 October 2026 whose "
        "projected movement to parole is dated in calendar 2027. A person appears on the extract once.",
        "2.3 A cohort member's parole district is the district holding the member's county of commitment (Table 1)."]),
    ("3. Returns", [
        "3.1 A return is an admission to Department custody (movement ADM) dated from the day after the release to "
        "the 730th day after it. Transfers between institutions and court-writ movements are not admissions.",
        "3.2 A cohort's two-year return rate is the share of its members with a return. A member who dies without "
        "having returned is a member without a return.",
        "3.3 The projection carries two-year return rates in steps of five percentage points, for the cohort and for "
        "each parole district."]),
    ("4. The 2027 cohort and Act 26-114", [
        "4.1 Act 26-114 takes effect on 1 January 2027 and governs the whole of the 2027 cohort's first two years "
        "after release. Under it the Board of Parole does not recommit parolees, and a parolee comes back to the "
        "Department only on a new sentence of total confinement in a State correctional institution. A member of the "
        "2027 cohort is therefore out of Department custody from release until a return, and for all 730 days where "
        "there is none.",
        "4.2 The 2027 cohort's return rate is therefore the share of the cohort the Department will admit on a new "
        "court commitment within 730 days of release."]),
    ("5. Review", [
        "5.1 The Commission's Projections Advisory Group reviews the definitions each year before the projection is "
        "run."]),
]
TABLE1 = [("Parole district", "District office", "Counties")] + [
    (d, C.OFFICE[d], ", ".join(C.COUNTIES[d])) for d in C.DISTRICTS]


def _styles():
    base = ParagraphStyle("b", fontName="Serif", fontSize=10.5, leading=14, textColor=INK, spaceAfter=6)
    head = ParagraphStyle("h", fontName="Serif-Bold", fontSize=11, leading=15, textColor=INK, spaceBefore=8, spaceAfter=4)
    title = ParagraphStyle("t", fontName="Sans-Bold", fontSize=15, leading=19, textColor=INK, spaceAfter=4)
    sub = ParagraphStyle("s", fontName="Sans", fontSize=9.5, leading=13, textColor=GREY, spaceAfter=10)
    small = ParagraphStyle("f", fontName="Sans", fontSize=8.5, leading=11, textColor=GREY, spaceBefore=12)
    return base, head, title, sub, small


def _esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _pdf(path, title, sub, sections, foot=None, table=None, table_after=None, issued=None, author="", subject=""):
    base, head, tstyle, sstyle, small = _styles()
    story = [Paragraph(_esc(title), tstyle)]
    if sub:
        story.append(Paragraph(_esc(sub), sstyle))
    for h, paras in sections:
        story.append(Paragraph(_esc(h), head))
        for p in paras:
            story.append(Paragraph(_esc(p), base))
        if table is not None and h == table_after:
            t = Table(table, hAlign="LEFT", colWidths=None)
            t.setStyle(TableStyle([("FONT", (0, 0), (-1, 0), "Sans-Bold", 9), ("FONT", (0, 1), (-1, -1), "Sans", 9),
                                   ("LINEBELOW", (0, 0), (-1, 0), 0.6, INK), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                                   ("TOPPADDING", (0, 0), (-1, -1), 3)]))
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
        canvas.drawRightString(letter[0] - 20 * mm, 12 * mm, "Page %d" % doc.page)
        canvas.restoreState()

    doc = SimpleDocTemplate(path, pagesize=letter, leftMargin=22 * mm, rightMargin=22 * mm, topMargin=20 * mm,
                            bottomMargin=20 * mm, title=title, author=author, subject=subject, creator="",
                            producer="")
    doc.build(story, onFirstPage=page, onLaterPages=page)
    stamp = ("D:%04d%02d%02d%02d%02d%02d-04'00'" % (issued.year, issued.month, issued.day, 10, 12, 0)).encode()
    PP.normalize_pdf(path, stamp, stamp)


def write_act(path):
    _pdf(path, ACT_TITLE, ACT_HEAD, ACT, foot=ACT_FOOT, issued=dt.date(2026, 7, 2),
         author="Legislative Reference Bureau", subject="Enrolled act")


def write_methodology(path):
    _pdf(path, METH_TITLE, METH_SUB, METH, foot="Research and Projections Unit, Pembroke Sentencing and Policy "
         "Commission. Questions on this document go to the unit's projections lead.",
         table=TABLE1, table_after="2. Release cohorts", issued=C.ASSEMBLED, author=C.COMMISSION,
         subject="Projection methodology")


def prat_sections(stats):
    rows = [("PRAT level", "Releases", "Returned within 730 days")]
    for lv, n, r in stats["levels"]:
        rows.append((lv, "{:,}".format(n), "%.1f per cent" % (100 * r)))
    sec = [
        ("1. Purpose", [
            "The Pembroke Release Assessment Tool (PRAT) is scored for every person the Department releases to "
            "parole, from the record and a structured interview in the last months before release. This study "
            "checks how well the total score separated the people who came back to the Department within two years "
            "from those who did not, for the people released to parole in 2019 and 2020."]),
        ("2. Data", [
            "Releases to parole and reparole from 1 January 2019 to 31 December 2020 (%s releases), each followed "
            "730 days for an admission to Department custody of any kind, from the Department's movement records "
            "as they stood on 31 March 2023." % "{:,}".format(stats["n"])]),
        ("3. Results", [
            "The area under the ROC curve for the total score was %.2f. Return within 730 days by PRAT level is "
            "shown below; the tool's levels are those adopted in 2017 (Low 0 to 7, Moderate 8 to 12, High 13 to 17, "
            "Very high 18 to 24)." % stats["auc"]]),
        ("4. Conclusion", [
            "The tool continues to separate the levels in the expected order. The Department will re-validate the "
            "tool on the 2023 releases in 2026."]),
    ]
    return sec, rows


def write_prat(path, stats):
    sec, rows = prat_sections(stats)
    _pdf(path, "PRAT Validation Study: 2019 and 2020 Releases", "Pembroke Department of Corrections, Bureau of "
         "Planning, Research and Statistics. June 2023.", sec, table=rows, table_after="3. Results",
         issued=dt.date(2023, 6, 21), author=C.DOC, subject="Risk tool validation")
