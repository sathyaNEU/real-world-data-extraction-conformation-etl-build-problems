"""task179 documents: Directive 26-07, the Revisor's conversion table, Belvantis's service schedule and the Department's
statewide recidivism brief (a distractor). Their text is held here as data so checks.py can quote it and verify.py can
read it back from the PDFs."""
from __future__ import annotations

import datetime as dt
import re

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                        # noqa: E402
from reportlab.lib.pagesizes import letter                                              # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                         # noqa: E402
from reportlab.lib.units import mm                                                      # noqa: E402
from reportlab.pdfbase import pdfmetrics                                                # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                            # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle   # noqa: E402

import codes as K             # noqa: E402
import common as C            # noqa: E402
import names as NM            # noqa: E402
import postprocess as PP      # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/"
for _n, _f in (("Serif", "liberation/LiberationSerif-Regular.ttf"), ("Serif-Bold", "liberation/LiberationSerif-Bold.ttf"),
               ("Sans", "liberation/LiberationSans-Regular.ttf"), ("Sans-Bold", "liberation/LiberationSans-Bold.ttf")):
    pdfmetrics.registerFont(TTFont(_n, FONT_DIR + _f))
INK = colors.HexColor("#1b1b1b")
GREY = colors.HexColor("#555555")

# ------------------------------------------------------------------ Directive 26-07
SUPERVISEE_PIN = ("A supervisee is a person with an open supervision episode in the Division's case-management system "
                  "(CMS). An episode is open from its start date through its close date.")
NEW_CHARGE_PIN = ("A booking on a new charge is a booking that a county jail records as a new arrest. A booking on a "
                  "warrant, for a violation of supervision, on a court order, as a return to custody or to serve a "
                  "sentence is not a booking on a new charge, whatever charges it lists.")
SCHED_B_PIN = ("A Category V charge is a charge under a section of the Criminal Code listed in the Appendix. A charge "
               "recorded under a section of former Title 21 or Title 8 is read as the section the Legislative "
               "Revisor's conversion table of 2024 gives for it.")
ZONE_PIN = ("For each supervisee booked on a new Category V charge the supervising officer sets, on receiving the "
            "booking notice, one exclusion zone around each residence in the City of Halverton at which a victim of the "
            "incident behind the charge lives. Victims who share a residence share one zone, and a supervisee booked "
            "again on the same incident keeps the zones already set. A business, the public, or a victim with no "
            "recorded residence in Halverton has no zone.")
ZONE_SOURCE = ("For arrests by the Halverton Police Department the victims and their residences are those in the "
               "Department's violent-incident extract received under the 2019 data-sharing agreement; for arrests by "
               "any other agency the court's no-contact order governs.")

DIRECTIVE = [
    ("1. Purpose", [
        "From 1 January 2027 a supervisee who is booked into a county jail on a new Category V charge is placed on "
        "GPS monitoring by the supervising region when released from that custody, and stays on it until the charge "
        "is disposed of or the supervision ends, whichever is earlier.",
        "The directive applies in every region. It does not change a court's own conditions of release."]),
    ("2. Definitions", [SUPERVISEE_PIN, NEW_CHARGE_PIN, SCHED_B_PIN]),
    ("3. Placement", [
        "The county jails notify the supervising region of each booking of a supervisee. The supervising officer "
        "files the GPS placement in CMS within two working days of the notice, and the device is fitted at release. "
        "A supervisee already on GPS stays on the existing enrolment, which counts as the placement. A supervisee whose "
        "custody ends in a commitment to the Department is not placed.",
        "A placement under this directive is reviewed at 90 days and may be ended early only with the regional "
        "manager's approval."]),
    ("4. Exclusion zones", [ZONE_PIN, ZONE_SOURCE]),
    ("5. Orders", [
        "Regions reserve the enrolments and the exclusion zones they expect to need for calendar 2027 in their 2027 "
        "orders under the Belvantis contract (MDOC-2025-117), filed with the Contracts Office by 15 January 2027. "
        "Reserved enrolments are billed at the reserved rate and enrolments beyond the reservation at the standard "
        "rate (Schedule C)."]),
    ("6. Contact", ["Program Integrity Unit, Division of Community Supervision."]),
]


def category_v_rows():
    rows = [("Section", "Title")]
    for s in K.SCHEDULE_B:
        rows.append((s, K.TITLE[s]))
    return rows


# ------------------------------------------------------------------ conversion table
CODE_INTRO = ("This table gives, for each section of former Title 21 (Crimes and Punishments) and Title 8 (Motor "
              "Vehicles) cited in criminal proceedings, the section of the Criminal Code that replaces it from 1 July "
              "2024. Where a former section was divided between new sections, each part is listed with its subsection.")
CODE_NOTE = ("A charge laid before 1 July 2024 keeps its former citation in court records; agencies converting records "
             "for statistical purposes use this table.")


def code_rows():
    rows = [("Former section", "Criminal Code section", "Title of the new section")]
    def order(sec):
        t, rest = sec.split("-", 1)
        m = re.match(r"(\d+)(.*)", rest)
        return int(t), int(m.group(1)), m.group(2)
    for r in sorted([x[:3] for x in K.ROWS] + list(K.EXTRA_ROWS), key=lambda x: order(x[0])):
        rows.append((r[0], r[1], r[2]))
    return rows


# ------------------------------------------------------------------ Belvantis schedule C
RATE_STD, RATE_RES, RATE_ZONE, RATE_DMG = "4.85", "4.10", "1.20", "145.00"
BILL_DAY = ("An enrolment day is billed for each calendar day in Merrow time (US Central time: six hours behind UTC, "
            "and five hours behind while daylight saving time runs, from the second Sunday in March to the first Sunday "
            "in November) on which a client holds an assigned Belvantis device under the Department region's account at "
            "any time of the day. A day on which one device is returned and another issued is one enrolment day.")
BILL_SUSPEND = ("No enrolment day is billed for a day on which the enrolment is suspended at the region's request, from the "
                "effective date of the suspension through the effective date of the resumption (a suspension and a "
                "resumption effective on the same date suspend that one day), or for any day on which the county jails' "
                "booking records show the client held for any part of the day.")
BILL_REGION = ("Belvantis moves a client to another region's account when that region confirms a transfer of "
               "supervision; a move between a region's own offices or counties leaves the account where it is. Each day "
               "is billed to the region that supervised the client that day, and the transferring region is credited for "
               "any days billed to it after its supervision ended.")
BILL_VOID = "An event that Belvantis voids is treated as never recorded. Effective dates govern billing; the logged time records data entry only."

SCHEDULE = [
    ("C.1 Rates", ["Standard enrolment day: USD %s. Reserved enrolment day (enrolments reserved in an annual order): "
                   "USD %s. Exclusion zone: USD %s per zone per month or part month. Device replaced for client damage: "
                   "USD %s." % (RATE_STD, RATE_RES, RATE_ZONE, RATE_DMG)]),
    ("C.2 Enrolment days", [BILL_DAY, BILL_SUSPEND]),
    ("C.3 Regions", [BILL_REGION]),
    ("C.4 Records", [BILL_VOID,
                     "Belvantis issues each region a monthly invoice by the tenth working day of the following month, "
                     "with an event export the region may reconcile against."]),
    ("C.5 Disputes", ["A region disputes an invoice line in writing within 60 days. Agreed credits are applied to the next "
                      "invoice."]),
]

# ------------------------------------------------------------------ recidivism brief (distractor)
BRIEF_ROWS = [("MRAS level at placement", "People placed in 2021", "Rearrested within 3 years", "Per cent"),
              ("Low", "6,214", "1,019", "16.4"), ("Moderate", "9,877", "3,229", "32.7"),
              ("High", "6,402", "3,086", "48.2"), ("Very high", "1,733", "1,016", "58.6"),
              ("All", "24,226", "8,350", "34.5")]
BRIEF = [
    ("Summary", [
        "This brief follows everyone placed on Department supervision in calendar 2021, statewide, for three years from "
        "placement, and counts anyone arrested by any Merrow agency in that time for any offence, including "
        "misdemeanours and arrests after supervision ended. Rearrest is taken from the state identification bureau's "
        "fingerprint-supported arrest records.",
        "Rearrest rose with the MRAS level at placement in every region and every offence group, as it has in each "
        "cohort the Unit has followed since 2016."]),
    ("Method", [
        "Placements are counted once per person, at the first placement in the year. Deaths in the follow-up are "
        "kept in the denominator. The 2021 cohort's follow-up ended on 31 December 2024; the 2022 cohort will be "
        "published in 2026."]),
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


def _table(rows, widths):
    t = Table(rows, hAlign="LEFT", colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, 0), "Sans-Bold", 8.5), ("FONT", (0, 1), (-1, -1), "Sans", 8.5),
                           ("LINEBELOW", (0, 0), (-1, 0), 0.6, INK), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
                           ("TOPPADDING", (0, 0), (-1, -1), 2.5), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return t


def _pdf(path, title, sub, sections, issued, foot=None, tables=(), author=""):
    """tables: (after_heading, rows, widths, caption)"""
    base, head, tstyle, sstyle, small = _styles()
    story = [Paragraph(_esc(title), tstyle)]
    if sub:
        story.append(Paragraph(_esc(sub), sstyle))
    for h, paras in sections:
        if h:
            story.append(Paragraph(_esc(h), head))
        for p in paras:
            story.append(Paragraph(_esc(p), base))
        for (after, rows, widths, cap) in tables:
            if after == h:
                if cap:
                    story.append(Paragraph(_esc(cap), head))
                story.append(Spacer(1, 3))
                story.append(_table(rows, widths))
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

    doc = SimpleDocTemplate(path, pagesize=letter, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm,
                            bottomMargin=20 * mm, title=title, author=author, subject="", creator="", producer="")
    doc.build(story, onFirstPage=page, onLaterPages=page)
    off = "-06'00'" if issued.month in (1, 2, 11, 12) or (issued.month == 3 and issued.day < 10) else "-05'00'"
    stamp = ("D:%04d%02d%02d%02d%02d%02d%s" % (issued.year, issued.month, issued.day, 10, 17, 0, off)).encode()
    PP.normalize_pdf(path, stamp, stamp)


def write_directive(path):
    _pdf(path, "Directive 26-07: GPS monitoring after a Category V booking",
         "%s, %s. Issued 16 November 2026; effective 1 January 2027. Authorized by %s, Deputy Director, Community "
         "Supervision." % (C.DEPT, C.DIVISION, NM.PERSONAS["deputy_director"]),
         DIRECTIVE + [("Appendix: Category V", ["The sections of the Criminal Code whose charges are Category V charges "
                                                "under this directive."])],
         C.DIRECTIVE_DATE, tables=[("Appendix: Category V", category_v_rows(), [28 * mm, 120 * mm], None)],
         foot="Directive 26-07, version 1.0. Questions to the Program Integrity Unit.", author="Program Integrity Unit")


def write_codes(path):
    _pdf(path, "Criminal Code Recodification Act: conversion table",
         "Office of the Legislative Revisor, %s. Published 3 June 2024; in force 1 July 2024." % C.STATE,
         [("", [CODE_INTRO, CODE_NOTE]), ("Table", [])], dt.date(2024, 6, 3),
         tables=[("Table", code_rows(), [30 * mm, 34 * mm, 100 * mm], None)],
         foot="Revisor's table RT-2024-3. The table is a finding aid; the Act and the Criminal Code govern.",
         author="Office of the Legislative Revisor")


def write_schedule(path):
    _pdf(path, "Schedule C: service charges and billing",
         "Contract MDOC-2025-117 between the %s and %s, electronic monitoring services. Schedule C as amended "
         "1 March 2025." % (C.DEPT, C.VENDOR),
         SCHEDULE, dt.date(2025, 2, 21), foot="Schedule C forms part of contract MDOC-2025-117 and is read with its "
         "general conditions.", author="Contracts Office")


def write_brief(path):
    _pdf(path, "Three-year rearrest of people placed on supervision in 2021",
         "Research and Statistics Unit, %s. Research brief 25-02, March 2025." % C.DEPT,
         [BRIEF[0], ("Table 1", []), BRIEF[1]], dt.date(2025, 3, 18),
         tables=[("Table 1", BRIEF_ROWS, [50 * mm, 38 * mm, 42 * mm, 20 * mm],
                  "Table 1. Rearrest within three years by MRAS level at placement, 2021 placements, statewide")],
         foot="Research brief 25-02. Figures are for all regions combined.", author="Research and Statistics Unit")


ALL_TEXT = {C.F_DIRECTIVE: [SUPERVISEE_PIN, NEW_CHARGE_PIN, SCHED_B_PIN, ZONE_PIN, ZONE_SOURCE],
            C.F_SCHED: [BILL_DAY, BILL_SUSPEND, BILL_REGION, BILL_VOID],
            C.F_CODE: [CODE_INTRO], C.F_BRIEF: [BRIEF[0][1][0]]}
