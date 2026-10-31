"""The golden deliverables: return_officer_memo_2027.pdf and return_inspections_2027.xlsx, written from the analysis."""
import io
import os

import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill
from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import postprocess as PP

MEMO = "return_officer_memo_2027.pdf"
XLSX = "return_inspections_2027.xlsx"
GREEN = colors.HexColor("#1F5E3B")
AREA = {"A": "Marlow West", "B": "Marlow East", "C": "Marlow South and Harborview", "D": "Kessing and the North Valley",
        "E": "Ardell and Torvik", "F": "Wexby and the South Shore", "G": "Norrow and Callan",
        "H": "Marlow North and Lake Road", "J": "Elsby and the East Hills"}


def round_to(v, u):
    return int(u * int(v / u + 0.5))


def summary(F):
    G = F["G"]
    nk = G["nk"]
    n = sum(nk.values())
    return dict(total=G["total"], total_r=round_to(G["total"], 100), n=n, first=nk.get(0, 0), second=nk.get(1, 0),
                later=nk.get(2, 0), add=G["add"])


def memo(path, F):
    S = summary(F)
    G = F["G"]
    ss = getSampleStyleSheet()
    body = ParagraphStyle("b", parent=ss["Normal"], fontName="Helvetica", fontSize=10, leading=13.2, spaceAfter=7)
    head = ParagraphStyle("h", parent=ss["Normal"], fontName="Helvetica-Bold", fontSize=10.5, leading=13.5,
                          spaceAfter=3, spaceBefore=4, textColor=GREEN)
    small = ParagraphStyle("s", parent=ss["Normal"], fontName="Helvetica", fontSize=8.6, leading=11, spaceAfter=4)
    title = ParagraphStyle("t", parent=ss["Normal"], fontName="Helvetica-Bold", fontSize=13.5, leading=17, spaceAfter=2)
    r = G["rates"]
    story = [
        Paragraph("A third return-inspection officer is needed for 2027", title),
        Paragraph("To: Teresa Hansen, Environmental Health Director<br/>From: Valerie Wood, Food Safety Program "
                  "Manager<br/>Date: 25 January 2027<br/>Subject: Return-inspection staffing under section 3 of the "
                  "2027 Food Safety Program Plan", small),
        Spacer(1, 6),
        Paragraph("Add the third return-inspection officer for 2027. The routine inspections in the 2027 schedule are "
                  "forecast to produce about %s unsatisfactory inspections, against the 540 the plan sets as the two "
                  "officers' capacity." % format(S["total_r"], ","), body),
        Paragraph("Why 2027 runs well above 2026", head),
        Paragraph("The redrawn districts put %s of the %s scheduled routine inspections with an inspector who has no "
                  "earlier inspection of the establishment on the record since January 2019, and %s more at that "
                  "inspector's second. In the county's own "
                  "record for 2022 to 2026 an inspector marked a first visit unsatisfactory far more often than a third "
                  "or later visit to the same establishment: %.1f against %.1f per cent in risk category 3, %.1f "
                  "against %.1f in category 2 and %.1f against %.1f in category 1, with second visits in between. "
                  "Carried through the schedule, the first visits alone account for about %s of the forecast."
                  % (format(S["first"], ","), format(S["n"], ","), format(S["second"], ","),
                     100 * r[(3, 0)], 100 * r[(3, 2)], 100 * r[(2, 0)], 100 * r[(2, 2)], 100 * r[(1, 0)],
                     100 * r[(1, 2)], format(round_to(sum(F["first_part"].values()), 10), ",")), body),
        Paragraph("Carrying each establishment's own record forward, or giving each inspector one rate for every "
                  "establishment, lands near the 2022 to 2026 level and under the 540. Both read rates set almost "
                  "entirely by inspectors who already knew the kitchens: in each year from 2022 to 2026 fewer than one "
                  "routine inspection in ten was the inspector's first at the establishment, against nearly one in four "
                  "in the 2027 schedule.", body),
        Paragraph("How the forecast was built", head),
        Paragraph("Each scheduled inspection is read at the number of earlier inspections its named inspector has made "
                  "at the establishment, counted over both inspection systems from January 2019 (the legacy system's "
                  "inspector initials matched to the staff roster) and through the schedule's own earlier 2027 "
                  "inspections. Rates come from the "
                  "routine inspections of 2022 to 2026, by risk category and by first, second or later visit, so that "
                  "every count has at least three years of record behind it.", body),
        Spacer(1, 4),
    ]
    rows = [["2027 district", "Scheduled", "First visits", "Forecast unsatisfactory"]]
    for d in sorted(G["by"]):
        rows.append(["%s %s" % (d, AREA[d]), format(F["sched_by"][d], ","), format(F["first_by"][d], ","),
                     "%.0f" % G["by"][d]])
    rows.append(["All districts", format(S["n"], ","), format(S["first"], ","), "%.0f" % S["total"]])
    t = Table(rows, colWidths=[2.9 * inch, 0.95 * inch, 1.0 * inch, 1.55 * inch])
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8.6), ("FONT", (0, 1), (-1, -1), "Helvetica", 8.6),
                           ("FONT", (0, -1), (-1, -1), "Helvetica-Bold", 8.6), ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
                           ("LINEBELOW", (0, 0), (-1, 0), 0.6, GREEN), ("LINEABOVE", (0, -1), (-1, -1), 0.4, GREEN),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 2), ("TOPPADDING", (0, 0), (-1, -1), 1.5)]))
    story.append(t)
    story.append(Spacer(1, 4))
    story.append(Paragraph("Source: the 2027 routine inspection schedule and Table 1 of the plan; inspection records "
                           "from January 2019 to December 2026 in both systems. Unsatisfactory is as section 1 of the "
                           "plan defines it: 25 red points or more, or a closure for an imminent health hazard.", small))

    def footer(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.5)
        canvas.setFillColor(colors.HexColor("#555555"))
        canvas.drawString(0.9 * inch, 0.45 * inch, "Elkhorn County Public Health, Food Safety Program")
        canvas.drawRightString(letter[0] - 0.9 * inch, 0.45 * inch, "Page 1 of 1")
        canvas.restoreState()
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=letter, leftMargin=0.9 * inch, rightMargin=0.9 * inch, topMargin=0.7 * inch,
                            bottomMargin=0.7 * inch, title="A third return-inspection officer is needed for 2027",
                            author="Food Safety Program", creator="Food Safety Program", producer="Food Safety Program")
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    open(path, "wb").write(buf.getvalue())
    PP.normalize_pdf(path, b"D:20270125161204-08'00'", "Food Safety Program")


HEAD = Font(name="Calibri", bold=True, size=11)
FILL = PatternFill("solid", fgColor="E2EFDA")


def _table(ws, title, head, rows, widths, note=None, formats=None):
    ws.append([title])
    ws["A1"].font = Font(name="Calibri", bold=True, size=12)
    if note:
        ws.append([note])
        ws["A2"].font = Font(name="Calibri", italic=True, size=10)
    ws.append([])
    ws.append(head)
    hr = ws.max_row
    for c in ws[hr]:
        c.font, c.fill = HEAD, FILL
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for r in rows:
        ws.append(r)
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(i)].width = w
    ws.freeze_panes = "A%d" % (hr + 1)
    for col, fmtx in (formats or {}).items():
        for c in ws[col][hr:]:
            if isinstance(c.value, (int, float)):
                c.number_format = fmtx


def workbook(path, F):
    G = F["G"]
    S = summary(F)
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Forecast 2027"
    rows = [[d, AREA[d], F["sched_by"][d], F["first_by"][d], F["second_by"][d], round(G["by"][d], 1)]
            for d in sorted(G["by"])]
    rows.append(["", "All districts", S["n"], S["first"], S["second"], round(S["total"], 1)])
    _table(ws, "2027 routine inspections forecast to be marked unsatisfactory",
           ["District", "Area", "Scheduled routine inspections", "First visits", "Second visits",
            "Forecast unsatisfactory"], rows, [9, 30, 16, 12, 12, 16],
           formats={"C": "#,##0", "D": "#,##0", "E": "#,##0", "F": "0.0"},
           note="Forecast %s, rounded to the nearest 100: %s. Plan threshold 540." % ("%.1f" % S["total"],
                                                                                     format(S["total_r"], ",")))
    rr = wb.create_sheet("Rates 2022-2026")
    rrows = []
    for risk in (1, 2, 3):
        for k, lab in ((0, "First visit"), (1, "Second visit"), (2, "Third or later visit")):
            c = G["cells"][(risk, k)]
            rrows.append([risk, lab, c[1], c[0], round(100 * c[0] / c[1], 1)])
    _table(rr, "Routine inspections 2022-2026 by risk category and the inspector's visit to the establishment",
           ["Risk category", "Visit", "Routine inspections", "Unsatisfactory", "Per cent"], rrows, [13, 22, 18, 15, 10],
           formats={"C": "#,##0", "D": "#,##0", "E": "0.0"})
    wa = wb.create_sheet("Return timeliness 2026")
    _table(wa, "Median county working days, unsatisfactory routine inspection to first return inspection, 2026",
           ["District", "Return inspections", "Median working days"],
           [[d, F["A_n"][d], float(F["A"][d])] for d in sorted(F["A"])], [10, 18, 20], formats={"C": "0.0"})
    wbb = wb.create_sheet("Complaint response 2026")
    _table(wbb, "Median hours, first notice of a complaint's conditions to the inspector's arrival, 2026",
           ["District", "Complaint investigations", "Median hours"],
           [[d, F["B_n"][d], round(F["B"][d], 1)] for d in sorted(F["B"])], [10, 22, 14], formats={"C": "0.0"})
    wc = wb.create_sheet("Return visit fees 2026")
    _table(wc, "Return visit fees due for 2026 visits after 2026 unsatisfactory routine inspections",
           ["District", "Fees due (USD)"],
           [[d, F["C"].get(d, 0)] for d in sorted(F["A"])] + [["All districts", sum(F["C"].values())]], [14, 16],
           formats={"B": "#,##0"})
    wn = wb.create_sheet("Notes")
    for line in ("Inspection records from January 2019 to December 2026 in both systems; the 2027 schedule and Table 1 "
                 "of the 2027 Food Safety Program Plan.",
                 "Unsatisfactory: 25 red points or more, or a closure for an imminent health hazard (plan section 1).",
                 "Return timeliness: county working days to the first return inspection at which the officer inspected "
                 "the premises (plan section 4); return-team inspections keyed from paper day sheets are dated by the "
                 "day sheet.",
                 "Complaint response: hours from the first report of the conditions after the permit's previous "
                 "investigation to the inspector's arrival (plan section 4).",
                 "Return visit fees: each return visit after the first for the same routine inspection, made or found "
                 "closed, at the rate on the day of the visit (fee schedule as amended 1 July 2026)."):
        wn.append([line])
    wn.column_dimensions["A"].width = 110
    wb.save(path)
    PP.normalize_xlsx(path, "Food Safety Program", "2027-01-22T18:05:00Z", "2027-01-25T23:40:00Z",
                      company="Elkhorn County")


def write(golden_dir, F):
    os.makedirs(golden_dir, exist_ok=True)
    memo(os.path.join(golden_dir, MEMO), F)
    workbook(os.path.join(golden_dir, XLSX), F)
