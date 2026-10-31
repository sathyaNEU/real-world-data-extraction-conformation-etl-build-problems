"""The governing documents: the 2027 Food Safety Program Plan and the 2026 environmental health fee schedule."""
import io

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import postprocess as PP
import world as W

GREEN = colors.HexColor("#1F5E3B")


def _styles():
    ss = getSampleStyleSheet()
    return dict(
        body=ParagraphStyle("b", parent=ss["Normal"], fontName="Helvetica", fontSize=10, leading=13.4, spaceAfter=7),
        head=ParagraphStyle("h", parent=ss["Normal"], fontName="Helvetica-Bold", fontSize=10.5, leading=14,
                            spaceBefore=6, spaceAfter=3, textColor=GREEN),
        title=ParagraphStyle("t", parent=ss["Normal"], fontName="Helvetica-Bold", fontSize=15, leading=19, spaceAfter=4),
        small=ParagraphStyle("s", parent=ss["Normal"], fontName="Helvetica-Oblique", fontSize=8.8, leading=11.5,
                             spaceAfter=12),
        lh=ParagraphStyle("lh", parent=ss["Normal"], fontName="Helvetica-Bold", fontSize=10, leading=12,
                          textColor=GREEN, alignment=2),
        lh2=ParagraphStyle("lh2", parent=ss["Normal"], fontName="Helvetica", fontSize=8.5, leading=10.5,
                           textColor=GREEN, alignment=2, spaceAfter=14),
        cell=ParagraphStyle("c", parent=ss["Normal"], fontName="Helvetica", fontSize=9, leading=11),
    )


def _footer(text):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.5)
        canvas.setFillColor(colors.HexColor("#555555"))
        canvas.drawString(0.9 * inch, 0.6 * inch, text)
        canvas.drawRightString(letter[0] - 0.9 * inch, 0.6 * inch, "Page %d" % doc.page)
        canvas.restoreState()
    return draw


def _build(path, title, story, foot, stamp, producer):
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=letter, leftMargin=0.9 * inch, rightMargin=0.9 * inch,
                            topMargin=0.75 * inch, bottomMargin=0.9 * inch, title=title, author=producer,
                            creator=producer, producer=producer)
    doc.build(story, onFirstPage=_footer(foot), onLaterPages=_footer(foot))
    open(path, "wb").write(buf.getvalue())
    PP.normalize_pdf(path, stamp, producer)


def plan_paragraphs(insp27):
    return [
        ("t", "Food Safety Program Plan 2027"),
        ("s", "Issued 11 January 2027 by Valerie Wood, Food Safety Program Manager, and approved by Teresa Hansen, "
              "Environmental Health Director. Supersedes the 2026 plan."),
        ("h", "1. The program"),
        ("p", "Elkhorn County Public Health permits and inspects the county's food establishments under the "
              "Washington State Retail Food Code (chapter 246-215 WAC) and the county's food service code. Each "
              "permitted establishment receives one, two or three routine inspections a year according to its risk "
              "category (1, 2 or 3). An establishment that operates for part of the year receives one routine "
              "inspection, in its operating months."),
        ("p", "A routine inspection is unsatisfactory when it records 25 red points or more, or when the inspector "
              "closes the establishment for an imminent health hazard. Every unsatisfactory routine inspection is "
              "followed by a return inspection."),
        ("h", "2. Districts and inspectors in 2027"),
        ("p", "Erik Mayer and Andrew Mason retire on 31 December 2026, and their positions will not be refilled in "
              "2027. From 1 January 2027 the program inspects in nine districts in place of eleven. The nine "
              "districts are drawn afresh on drive time from each inspector's base and on the 2027 schedule's "
              "inspection hours, so that each district carries close to one ninth of the year's routine inspection "
              "hours. Table 1 names the inspector for each district. The schedule workbook issued with this plan "
              "lists every permitted establishment, its 2027 district and its routine inspections for 2027."),
        ("table1", None),
        ("h", "3. Return inspections"),
        ("p", "Since February 2022 return inspections have been made by a return team of two officers, one for the "
              "north districts and one for the south, rather than by the district inspectors. The team's capacity is "
              "270 return inspections per officer per year, from the 2024 time study."),
        ("p", "A third return-inspection officer is added for 2027 if the routine inspections in the 2027 schedule "
              "that will be marked unsatisfactory exceed 540, the two officers' capacity. The forecast counts each "
              "scheduled routine inspection as the inspector named in Table 1 for its district will make it. The "
              "decision is taken by 29 January 2027, so that a third officer can start in March."),
        ("h", "4. Measures the program reports"),
        ("p", "Return timeliness is the number of county working days from an unsatisfactory routine inspection to "
              "the first return inspection at which the officer inspects the premises; a return visit that finds the "
              "premises closed does not end the count. Saturdays, Sundays and county holidays are not working days."),
        ("p", "Complaint response time is the number of hours from the program's first notice of the conditions a "
              "complaint reports, by telephone, online form, email or referral, to the inspector's arrival at the "
              "establishment."),
        ("p", "Return visit fees are charged under the county's environmental health fee schedule."),
        ("h", "5. Review"),
        ("p", "The program reviews the districts at the end of June 2027 against the first half-year's inspection "
              "hours, and reports the measures in section 4 to the Board of Health each quarter."),
    ]


def plan_pdf(path, insp27):
    st = _styles()
    story = [Paragraph("Elkhorn County Public Health", st["lh"]),
             Paragraph("Environmental Health Division, 1120 Courthouse Square, Marlow, WA 98362", st["lh2"])]
    for kind, text in plan_paragraphs(insp27):
        if kind == "table1":
            data = [["District", "Area", "Inspector"]] + [
                [d, W.DISTRICT_2027_NAME[d], W.full_name(insp27[d])] for d in sorted(insp27)]
            t = Table(data, colWidths=[0.8 * inch, 3.3 * inch, 2.0 * inch])
            t.setStyle(TableStyle([("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 9),
                                   ("FONT", (0, 1), (-1, -1), "Helvetica", 9),
                                   ("LINEBELOW", (0, 0), (-1, 0), 0.6, GREEN),
                                   ("BOTTOMPADDING", (0, 0), (-1, -1), 3), ("TOPPADDING", (0, 0), (-1, -1), 2)]))
            story += [Paragraph("Table 1. Districts and inspectors from 1 January 2027", st["cell"]), Spacer(1, 3), t,
                      Spacer(1, 9)]
            continue
        story.append(Paragraph(text, {"t": st["title"], "s": st["small"], "h": st["head"]}.get(kind, st["body"])))
    _build(path, "Food Safety Program Plan 2027", story,
           "Elkhorn County Public Health, Food Safety Program Plan 2027, issued 11 January 2027",
           b"D:20270111094512-08'00'", "Elkhorn County Public Health")


FEE_ROWS = [
    ("Annual food establishment permit, risk category 1", "$295"),
    ("Annual food establishment permit, risk category 2", "$520"),
    ("Annual food establishment permit, risk category 3", "$745"),
    ("Seasonal establishment (operating six months or less), any category", "half the annual fee"),
    ("Plan review, new or remodeled establishment", "$410"),
    ("Pre-opening inspection", "$180"),
    ("Change of ownership, new permit", "$160 plus the annual fee"),
    ("Temporary food event, per vendor per event", "$95"),
    ("Late renewal (permit fee unpaid on 1 February)", "$75"),
]


def fee_paragraphs():
    return [
        ("t", "Environmental Health Fee Schedule 2026"),
        ("s", "Adopted by the Board of Health in Resolution 2025-117, effective 1 January 2026, and amended by "
              "Resolution 2026-048 effective 1 July 2026. Fees are payable to Elkhorn County Public Health."),
        ("h", "Food establishments"),
        ("fees", None),
        ("h", "Return visits"),
        ("p", "The first return visit after an unsatisfactory routine inspection is included in the annual permit "
              "fee. Each further return visit for the same routine inspection, whether the inspection is made or the "
              "premises are found closed, is charged at the rate in force on the day of the visit: $152 for visits "
              "made up to 30 June 2026 and $168 for visits made on or after 1 July 2026 (Resolution 2026-048)."),
        ("h", "Payment"),
        ("p", "Permit fees are invoiced in November for the following calendar year and are due on 31 January. Return "
              "visit charges are invoiced at the end of the month in which the visit is made and are due in 30 days."),
    ]


def fees_pdf(path):
    st = _styles()
    story = [Paragraph("Elkhorn County Public Health", st["lh"]),
             Paragraph("Environmental Health Division, 1120 Courthouse Square, Marlow, WA 98362", st["lh2"])]
    for kind, text in fee_paragraphs():
        if kind == "fees":
            t = Table([["Item", "Fee"]] + [list(r) for r in FEE_ROWS], colWidths=[4.6 * inch, 1.6 * inch])
            t.setStyle(TableStyle([("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 9),
                                   ("FONT", (0, 1), (-1, -1), "Helvetica", 9),
                                   ("LINEBELOW", (0, 0), (-1, 0), 0.6, GREEN),
                                   ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
            story += [t, Spacer(1, 9)]
            continue
        story.append(Paragraph(text, {"t": st["title"], "s": st["small"], "h": st["head"]}.get(kind, st["body"])))
    _build(path, "Environmental Health Fee Schedule 2026", story,
           "Elkhorn County Public Health, Environmental Health Fee Schedule 2026 (as amended 1 July 2026)",
           b"D:20260612143005-07'00'", "Elkhorn County Public Health")


def text_of(kind_list):
    return "\n".join(t for k, t in kind_list if t)
