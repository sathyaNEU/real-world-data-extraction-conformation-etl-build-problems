"""task176 documents: the family child care licensing rules (excerpt), the child care subsidy's provider payment
policy and the quarterly child care supply report (PDF). Their text is held here as data so checks.py can quote
it and verify.py can read it back."""
from __future__ import annotations

import datetime as dt

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

RULES = [
    ("Chapter 6.40 Family child care homes (excerpt of the rules in force on 1 July 2025)", []),
    ("6.40.010 Licence types", [
        "Family child care homes are licensed in two types. A small family child care home licence permits care for up "
        "to eight children in the provider's residence. A large family child care home licence permits care for up to "
        "twelve children with a second adult caregiver present whenever more than eight are in care. No more than three children under 24 months old may be in care at one "
        "time in either type of home.",
        "A licence is issued to one provider for one residence."]),
    ("6.40.030 Children counted toward capacity", [
        "Every child under 13 years of age who is present during the hours care is provided counts toward the "
        "licensed capacity, including the provider's own children and any other child who lives in the home or is "
        "related to the provider.",
        "The provider lists those children on the capacity worksheet with each child's initials, date of birth and "
        "relationship to the provider, and whether the child lives in the home. The worksheet is filed with the "
        "application, with each annual renewal, and when the provider asks for a change in capacity. A child who "
        "turns 13 is no longer listed."]),
    ("6.40.050 Renewal", [
        "A licence is renewed each year on the anniversary of its first issue, on a renewal application, a current "
        "capacity worksheet and background checks for every adult in the home. A licence not renewed lapses 30 days "
        "after its anniversary."]),
    ("6.40.070 Closing a home", [
        "A provider who stops providing care gives the department and every family in care 30 days' written notice "
        "where it can. The licence ends on the closure effective date the provider gives, or on the date the "
        "department revokes it or the licence lapses; the department records the closure with the reason the "
        "provider gives."]),
    ("6.40.090 Inspections", [
        "The department makes at least one unannounced monitoring visit to each licensed home in each calendar year, "
        "investigates every complaint, and may make follow-up visits to confirm that a violation has been corrected. "
        "Inspectors record each visit in the licensing system with its type, the date, and the times they arrived and "
        "left."]),
    ("6.40.110 Records", [
        "Licensing records are kept for seven years after a licence ends. Records of homes licensed before the "
        "department's licensing system was replaced on 1 July 2019 carry the former licence number until that date; "
        "the department keeps a table of former and current numbers."]),
]

POLICY = [
    ("Section 1. Scope", [
        "This policy governs payments to providers caring for children whose families receive assistance under the "
        "Child Care Assistance Program (CCAP). It applies to licensed centres, licensed family child care homes and "
        "license-exempt relative carers."]),
    ("Section 2. Authorisation", [
        "The program authorises care for a child at a named provider for a period of up to twelve months. A child may "
        "be authorised at two providers at once when the parent's work or school schedule needs care from both, each "
        "provider caring for part of the day."]),
    ("Section 3. Payment runs and remittances", [
        "Providers are paid monthly in arrears, in one statewide payment run in the first week of the following month. "
        "Each payee receives one remittance in a run, covering all the children it is paid for that month, and each "
        "county office numbers the remittances it issues in a run in its own sequence. Each line of a "
        "remittance covers one child for the days in the month on which care was authorised and scheduled (Monday to "
        "Friday).",
        "The full-time monthly rate is paid for a full month and prorated by scheduled days for a part month. A child "
        "authorised at two providers is paid at half the monthly rate at each.",
        "A remittance returned unpaid is voided and paid again in the next run."]),
    ("Section 4. Absence and notice", [
        "A provider is paid for scheduled days on which the child is absent, up to 20 days a year. When a child stops "
        "attending without the notice the provider's agreement requires, the provider is paid through the end of the "
        "notice period, up to ten business days after the last day the child attended."]),
    ("Section 5. Rates", [
        "Monthly full-time rates for 2026 are set by provider type: USD 812 for a small family child care home, USD 846 "
        "for a large family child care home, USD 1,138 for a licensed centre and USD 402 for a license-exempt relative "
        "carer. The schedule took effect on 1 January 2026."]),
    ("Section 6. School-age children", [
        "A child is school-age from the first day of the public school year in the calendar year in which the child "
        "turns five on or before 1 September; a child who turns five after 1 September is authorised as a preschool "
        "child until the following school year. Care for a school-age child is authorised for the hours outside the "
        "school day."]),
]


def _styles():
    base = ParagraphStyle("b", fontName="Serif", fontSize=10.5, leading=14, textColor=INK, spaceAfter=6)
    head = ParagraphStyle("h", fontName="Serif-Bold", fontSize=11, leading=15, textColor=INK, spaceBefore=8, spaceAfter=4)
    title = ParagraphStyle("t", fontName="Sans-Bold", fontSize=15, leading=19, textColor=INK, spaceAfter=4)
    sub = ParagraphStyle("s", fontName="Sans", fontSize=9.5, leading=13, textColor=GREY, spaceAfter=10)
    small = ParagraphStyle("f", fontName="Sans", fontSize=8.5, leading=11, textColor=GREY, spaceBefore=12)
    return base, head, title, sub, small


def _esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _pdf(path, title, sub, sections, foot=None, tables=None, issued=None, author="", subject=""):
    base, head, tstyle, sstyle, small = _styles()
    story = [Paragraph(_esc(title), tstyle)]
    if sub:
        story.append(Paragraph(_esc(sub), sstyle))
    for h, paras in sections:
        story.append(Paragraph(_esc(h), head))
        for p in paras:
            story.append(Paragraph(_esc(p), base))
        if tables and h in tables:
            t = Table(tables[h], hAlign="LEFT")
            t.setStyle(TableStyle([("FONT", (0, 0), (-1, 0), "Sans-Bold", 8.5), ("FONT", (0, 1), (-1, -1), "Sans", 8.5),
                                   ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
                                   ("LINEBELOW", (0, 0), (-1, 0), 0.6, INK), ("LINEABOVE", (0, -1), (-1, -1), 0.4, INK),
                                   ("BOTTOMPADDING", (0, 0), (-1, -1), 3), ("TOPPADDING", (0, 0), (-1, -1), 3)]))
            story.append(Spacer(1, 4))
            story.append(t)
            story.append(Spacer(1, 6))
    if foot:
        story.append(Paragraph(_esc(foot), small))

    def page(canvas, doc):
        canvas.saveState()
        canvas.setFont("Sans", 8)
        canvas.setFillColor(GREY)
        canvas.drawString(20 * mm, 12 * mm, C.DEPT)
        canvas.drawRightString(letter[0] - 20 * mm, 12 * mm, "Page %d" % doc.page)
        canvas.restoreState()

    doc = SimpleDocTemplate(path, pagesize=letter, leftMargin=22 * mm, rightMargin=22 * mm, topMargin=20 * mm,
                            bottomMargin=20 * mm, title=title, author=author, subject=subject, creator="",
                            producer="")
    doc.build(story, onFirstPage=page, onLaterPages=page)
    stamp = ("D:%04d%02d%02d%02d%02d%02d-05'00'" % (issued.year, issued.month, issued.day, 10, 12, 0)).encode()
    PP.normalize_pdf(path, stamp, stamp)


def write_rules(path):
    _pdf(path, "Allerton Administrative Code, Title 170, Chapter 6.40", "Family child care homes. Department of Early "
         "Learning, Office of Child Care Licensing. Excerpt; the full chapter governs.", RULES,
         foot="Excerpt prepared for the provider handbook, revision of 1 July 2025.", issued=dt.date(2025, 7, 1),
         author=C.DEPT, subject="Family child care licensing rules")


def write_policy(path):
    _pdf(path, "CCAP Provider Payment Policy 2026", "Child Care Assistance Program. Department of Early Learning, Subsidy "
         "Operations. Effective 1 January 2026.", POLICY,
         foot="Policy CCAP-PP-12, revision 4. Supersedes revision 3 (1 January 2024).", issued=dt.date(2025, 12, 9),
         author=C.DEPT, subject="CCAP provider payments")


def supply_sections(stats):
    rows = [("Region", "Homes", "Licensed places", "Homes licensed", "Homes closed")]
    for reg in sorted(C.REGIONS):
        s = stats["regions"][reg]
        rows.append((C.REGIONS[reg], "{:,}".format(s["homes"]), "{:,}".format(s["places"]), "{:,}".format(s["opened"]),
                     "{:,}".format(s["closed"])))
    t = stats["total"]
    rows.append(("Allerton", "{:,}".format(t["homes"]), "{:,}".format(t["places"]), "{:,}".format(t["opened"]),
                 "{:,}".format(t["closed"])))
    secs = [
        ("1. Licensed family child care", [
            "Family child care homes, small and large, licensed on 30 September 2026, with their "
            "licensed places, and the homes first licensed and the homes whose licence ended in the twelve months from "
            "1 October 2025 to 30 September 2026. Places are licensed capacity, which includes the provider's own "
            "children under 13 when they are present."]),
        ("2. The 2023 start-up grant round", [
            "The %s round paid from federal relief funds made %s awards to homes licensed between February and "
            "November 2023. On 30 September 2026, %s of those homes held a licence." % (C.GRANT, "{:,}".format(stats["grant_awards"]),
                                                                                       "{:,}".format(stats["grant_open"]))]),
        ("3. Sources", [
            "Licensing system extract of 6 October 2026; start-up grant award file. Figures are counts of licences."]),
    ]
    return secs, {"1. Licensed family child care": rows}


def write_supply(path, stats):
    secs, tabs = supply_sections(stats)
    _pdf(path, "Child Care Supply Report, quarter ending 30 September 2026", "Office of Child Care, supply and planning. "
         "Prepared for the Early Learning Council.", secs, tables=tabs,
         foot="Report OCC-SR-2026-3. Prepared by Misty Hawkins, supply and planning. Reviewed by Leroy Parker.",
         issued=dt.date(2026, 10, 21), author="Misty Hawkins", subject="Child care supply")
