"""The pack's documents: the fuel security procedure PR-07, the coal yard accounting instruction, the survey
contractor's control report for the July 2026 handover, and the first-quarter 2027 coal burn plan."""
from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                      # noqa: E402
from reportlab.lib.pagesizes import A4                                                # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                       # noqa: E402
from reportlab.lib.units import mm                                                    # noqa: E402
from reportlab.pdfbase import pdfmetrics                                              # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                          # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import world as W   # noqa: E402
import yard as Y    # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("LiberationSerif", "Regular"), ("LiberationSerif-Bold", "Bold"), ("LiberationSans", "Regular"),
              ("LiberationSans-Bold", "Bold"), ("LiberationSans-Italic", "Italic")):
    try:
        pdfmetrics.getFont(nm)
    except KeyError:
        pdfmetrics.registerFont(TTFont(nm, FONT_DIR + nm.split("-")[0] + "-" + f + ".ttf"))
INK = colors.HexColor("#1c1f22")
GREY = colors.HexColor("#5d6268")
NAVY = colors.HexColor("#1f3a5c")
BODY = ParagraphStyle("body", fontName="LiberationSerif", fontSize=10.2, leading=13.8, textColor=INK, spaceAfter=5)
NUM = ParagraphStyle("num", parent=BODY, leftIndent=26, firstLineIndent=-26)
H1 = ParagraphStyle("h1", fontName="LiberationSans-Bold", fontSize=14, leading=18, textColor=NAVY, spaceAfter=2)
SUB = ParagraphStyle("sub", fontName="LiberationSans", fontSize=9.4, leading=12.4, textColor=GREY, spaceAfter=8)
H2 = ParagraphStyle("h2", fontName="LiberationSans-Bold", fontSize=10.4, leading=14, textColor=INK, spaceBefore=7,
                    spaceAfter=3)
CELL = ParagraphStyle("cell", fontName="LiberationSans", fontSize=8.6, leading=10.8, textColor=INK)
CELLB = ParagraphStyle("cellb", parent=CELL, fontName="LiberationSans-Bold")
SMALL = ParagraphStyle("small", fontName="LiberationSans", fontSize=8.0, leading=10.3, textColor=GREY)
HEAD = ParagraphStyle("head", fontName="LiberationSans-Bold", fontSize=9.0, leading=11, textColor=NAVY)


def _doc(path, title, author, left, right):
    def frame(canvas, doc):
        canvas.saveState()
        canvas.setFont("LiberationSans-Bold", 8.4)
        canvas.setFillColor(NAVY)
        canvas.drawString(20 * mm, A4[1] - 12 * mm, left)
        canvas.setFont("LiberationSans", 7.6)
        canvas.setFillColor(GREY)
        canvas.drawRightString(A4[0] - 20 * mm, A4[1] - 12 * mm, right)
        canvas.setStrokeColor(colors.HexColor("#b8bec4"))
        canvas.setLineWidth(0.5)
        canvas.line(20 * mm, A4[1] - 14 * mm, A4[0] - 20 * mm, A4[1] - 14 * mm)
        canvas.drawString(20 * mm, 12 * mm, title)
        canvas.drawRightString(A4[0] - 20 * mm, 12 * mm, "Page %d" % doc.page)
        canvas.restoreState()
    d = SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=22 * mm,
                          bottomMargin=20 * mm, title=title, author=author, subject="", creator="", producer="")
    return d, frame


def _table(rows, widths, header=True):
    data = [[Paragraph(str(c), CELLB if (i == 0 and header) else CELL) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0, hAlign="LEFT")
    st = [("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9aa0a6")), ("VALIGN", (0, 0), (-1, -1), "TOP"),
          ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4)]
    if header:
        st.append(("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e5eaf0")))
    t.setStyle(TableStyle(st))
    return t


def _signoff(rows):
    return _table([["", "Name", "Role", "Date"]] + rows, [24 * mm, 46 * mm, 62 * mm, 30 * mm])


# --------------------------------------------------------------------------------------------- PR-07
def write_procedure(path):
    left = "%s  |  Satama power plant" % W.ORG
    doc, frame = _doc(path, "PR-07 Fuel security: winter coal reserve, revision 4", W.ORG, left,
                      "Controlled document PR-07, revision 4")
    s = [Paragraph("PR-07 Fuel security: the winter coal reserve", H1),
         Paragraph("Procedure of %s for the %s. Owner: fuel manager. Revision 4, approved by the management team on "
                   "11 March 2026; replaces revision 3 of 14 February 2023." % (W.ORG, W.PLANT), SUB)]
    p = lambda n, t: s.append(Paragraph("<b>%s</b>&nbsp;&nbsp;%s" % (n, t), NUM))
    s.append(Paragraph("1. Purpose", H2))
    s.append(Paragraph(
        "The plant burns coal in unit 2 and the peak boilers through the heating season. From January the harbour is "
        "served only by ice-class vessels and coal deliveries are few and uncertain until the spring opening, so the "
        "plant enters each year with a reserve of coal in its own yard, sized against the first quarter's planned "
        "burn. This procedure sets that reserve, how it is stated and what is done when it falls short.", BODY))
    s.append(Paragraph("2. Scope", H2))
    s.append(Paragraph(
        "The coal yard at the plant harbour, pile areas P1 to P6 as listed in the pile area register. Coal in the "
        "boiler house bunkers, on board a vessel or nominated and not yet discharged is not part of the reserve.",
        BODY))
    s.append(Paragraph("3. Definitions", H2))
    p("3.1", "<b>December survey</b>: the coal yard stock survey flown in December by the plant's survey contractor.")
    p("3.2", "<b>Reserve</b>: the tonnes of coal held in the coal yard at the December survey. For each pile area it "
             "is the volume of coal above the yard pad at the survey multiplied by the bulk density the fuel "
             "laboratory last determined for that coal before the survey; the reserve is the sum over the pile areas.")
    p("3.3", "<b>Planned burn</b>: the coal burn of January to March in the first-quarter burn plan approved by the "
             "management team, the plan's quarter total divided by the days of the quarter, in tonnes a day.")
    p("3.4", "<b>Days of cover</b>: the reserve divided by the planned burn.")
    s.append(Paragraph("4. The floor", H2))
    s.append(Paragraph("The reserve at the December survey is to be at least %d days of cover." % W.FLOOR_DAYS, BODY))
    s.append(Paragraph("5. The winter option", H2))
    s.append(Paragraph(
        "The coal supply agreement %s with %s gives the plant one additional cargo for loading in the second half of "
        "January (the winter option). Where the December survey shows fewer than %d days of cover, the fuel manager "
        "nominates the winter option to the supplier in writing by 8 January. Where it shows %d days or more, no "
        "nomination is made and the option lapses." % (W.OPTION[1], W.OPTION[0], W.FLOOR_DAYS, W.FLOOR_DAYS), BODY))
    s.append(Paragraph("6. The winter fuel statement", H2))
    s.append(Paragraph(
        "By 6 January the fuel manager prepares the winter fuel statement: the reserve by pile area, the days of "
        "cover and the decision on the winter option. The management team signs it.", BODY))
    s.append(Paragraph("7. Records", H2))
    s.append(Paragraph(
        "The survey contractor's deliveries, the fuel laboratory's density tests, the approved burn plan and the "
        "signed statement are kept for ten years in the plant's document system.", BODY))
    s.append(Spacer(1, 6))
    s.append(Paragraph("Revisions", H2))
    s.append(_table([["Rev.", "Date", "Change"],
                     ["2", "6 May 2019", "The reserve stated by pile area; laboratory density tests replace the "
                                         "standard density."],
                     ["3", "14 February 2023", "Floor 55 days; the statement signed by the management team."],
                     ["4", "11 March 2026", "Floor %d days; nomination date aligned with the 2026 supply agreements."
                      % W.FLOOR_DAYS]], [14 * mm, 32 * mm, 116 * mm]))
    s.append(Spacer(1, 8))
    s.append(_signoff([["Prepared", W.FUEL_MANAGER, "Fuel manager", "2 March 2026"],
                       ["Approved", W.CEO, "Managing director, for the management team", "11 March 2026"]]))
    doc.build(s, onFirstPage=frame, onLaterPages=frame)


# --------------------------------------------------------------------------------------------- OH-12
def write_accounting(path):
    left = "%s  |  Satama power plant" % W.ORG
    doc, frame = _doc(path, "OH-12 Coal yard accounting, revision 2", W.ORG, left, "Work instruction OH-12, revision 2")
    s = [Paragraph("OH-12 Coal yard accounting", H1),
         Paragraph("Work instruction of %s for the coal yard at the %s. Owner: fuel manager. Revision 2, 20 January "
                   "2025." % (W.ORG, W.PLANT), SUB)]
    p = lambda n, t: s.append(Paragraph("<b>%s</b>&nbsp;&nbsp;%s" % (n, t), NUM))
    s.append(Paragraph("1. The yard's book", H2))
    p("1.1", "Receipts are the coal that enters the yard from vessels. They are booked by the tonnes the stacker feed "
             "conveyor CV-01 weighs. The bill of lading and the draft survey at discharge are the commercial "
             "quantities for invoices and claims and are not booked to the yard.")
    p("1.2", "Deliveries are the coal that leaves the yard for the boiler house. They are booked by the tonnes the "
             "reclaim conveyor CV-21 weighs.")
    p("1.3", "The book stock is rolled forward from each December survey by receipts less deliveries. At the next "
             "December survey the surveyed stock is compared with the book stock and the difference is booked as a "
             "stock adjustment, with the fuel manager's explanation.")
    s.append(Paragraph("2. Time", H2))
    p("2.1", "The plant's records and the yard's book run on Finnish time. A day runs from 00:00 to 24:00; months and "
             "quarters are calendar months and quarters.")
    p("2.2", "The control room records the totaliser of each belt scale integrator, CV-01 and CV-21, in the shift log "
             "at 00:00, 08:00 and 16:00.")
    s.append(Paragraph("3. Belt scales", H2))
    p("3.1", "CV-01 and CV-21 are calibrated each spring with a material test against a weighed lorry load. A scale "
             "found outside 0.5 per cent is adjusted and the test is recorded by the maintenance department.")
    s.append(Spacer(1, 8))
    s.append(_signoff([["Prepared", W.FUEL_MANAGER, "Fuel manager", "16 January 2025"],
                       ["Approved", "Marjaana Mäkinen", "Financial controller", "20 January 2025"]]))
    doc.build(s, onFirstPage=frame, onLaterPages=frame)


# --------------------------------------------------------------------------------------------- the control report
CONTROL = [("SVL-101", 12.40, 4.85), ("SVL-102", 391.70, 7.30), ("SVL-103", 395.10, 226.20), ("SVL-104", 8.30, 223.90),
           ("SVL-105", 201.60, 113.40)]


def control_rows():
    import numpy as np
    rng = np.random.default_rng(W.SEED + 900)
    out = []
    for name, x, y in CONTROL:
        h60 = float(Y.pad_n60(np.array([x]), np.array([y]))[0]) + 0.08
        E, N = Y.to_tm35(x, y)
        out.append((name, W.X0 + x, W.Y0 + y, h60, E + rng.normal(0, 0.004), N + rng.normal(0, 0.004),
                    h60 + W.DH + rng.normal(0, 0.002)))
    return out


def write_control(path):
    doc, frame = _doc(path, "Survey control, Satama coal yard, July 2026", W.CONTRACTOR_B,
                      W.CONTRACTOR_B, "Report PDK-2026-118 for %s" % W.ORG)
    s = [Paragraph("Survey control for the Satama coal yard stock surveys", H1),
         Paragraph("Report PDK-2026-118 to %s, %s. Prepared for the handover of the monthly coal yard stock surveys "
                   "from July 2026. 3 July 2026." % (W.ORG, W.PLANT), SUB)]
    s.append(Paragraph("1. Purpose", H2))
    s.append(Paragraph(
        "From July 2026 the coal yard is surveyed by %s in ETRS-TM35FIN with N2000 heights. The plant's site grid "
        "(SVL plant grid) with N60 heights carries the pile area register and the yard's surveys to June 2026. This "
        "report gives the relation between the two systems at the yard, measured on the plant's control points on "
        "29 and 30 June 2026." % W.CONTRACTOR_B, BODY))
    s.append(Paragraph("2. Control points", H2))
    rows = [["Point", "x (SVL)", "y (SVL)", "H (N60)", "E (TM35FIN)", "N (TM35FIN)", "H (N2000)"]]
    for name, x, y, h60, E, N, h2000 in control_rows():
        rows.append([name, "%.3f" % x, "%.3f" % y, "%.3f" % h60, "%.3f" % E, "%.3f" % N, "%.3f" % h2000])
    s.append(_table(rows, [19 * mm, 22 * mm, 22 * mm, 19 * mm, 27 * mm, 29 * mm, 21 * mm]))
    s.append(Paragraph("Plant grid coordinates and N60 heights from the plant's control register; ETRS-TM35FIN "
                       "coordinates by network RTK, three sessions of 180 epochs each; N2000 heights by levelling "
                       "from benchmark 2203 of the national network.", SMALL))
    s.append(Paragraph("3. Plant grid to ETRS-TM35FIN", H2))
    s.append(Paragraph(
        "A rigid two-dimensional transformation (no scale change) fits all five points with a largest residual of "
        "0.008 m. With x' = x - %.3f and y' = y - %.3f in the plant grid:" % (W.X0, W.Y0), BODY))
    s.append(Paragraph("E = %.3f + x' cos a - y' sin a" % W.E0, NUM))
    s.append(Paragraph("N = %.3f + x' sin a + y' cos a" % W.N0, NUM))
    s.append(Paragraph("where a = %.4f degrees, the angle from grid east of ETRS-TM35FIN to the plant grid's x axis, "
                       "anticlockwise." % W.THETA_DEG, BODY))
    s.append(Paragraph("4. Heights", H2))
    s.append(Paragraph(
        "At the yard N2000 heights are %.3f m above N60 heights (mean of the five points, spread 0.004 m)." % W.DH,
        BODY))
    s.append(Paragraph("5. Deliveries from July 2026", H2))
    s.append(Paragraph(
        "Each monthly survey is delivered as an XYZ text file of the yard surface on a %.1f m lattice in "
        "ETRS-TM35FIN with N2000 heights, machines on the rails removed, checked against at least five of the "
        "plant's control points." % W.B_STEP, BODY))
    s.append(Spacer(1, 8))
    s.append(_signoff([["Surveyed", W.SURVEYOR_B, "Surveyor, %s" % W.CONTRACTOR_B, "30 June 2026"],
                       ["Checked", W.SURVEY_ENGINEER, "Survey engineer, %s" % W.ORG, "3 July 2026"]]))
    doc.build(s, onFirstPage=frame, onLaterPages=frame)


# --------------------------------------------------------------------------------------------- the burn plan
def write_plan(path):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    wb = Workbook()
    ws = wb.active
    ws.title = "Coal burn Q1 2027"
    bold = Font(name="Calibri", bold=True)
    thin = Side(style="thin", color="A6A6A6")
    ws["A1"] = "%s, %s: first-quarter 2027 coal burn plan" % (W.ORG, W.PLANT)
    ws["A1"].font = Font(name="Calibri", bold=True, size=12)
    ws["A2"] = "Version 3, approved by the management team 9 December 2026"
    hdr = ["Month", "Days", "Unit 2 coal, t/d", "Peak boilers coal, t/d", "Coal burn, t/d", "Coal burn, t"]
    for i, h in enumerate(hdr, 1):
        c = ws.cell(row=4, column=i, value=h)
        c.font = bold
        c.fill = PatternFill("solid", fgColor="DDE5EE")
        c.alignment = Alignment(wrap_text=True, vertical="top")
        c.border = Border(bottom=thin)
    r = 5
    for month, days, u2, peak in W.PLAN_Q1:
        ws.cell(row=r, column=1, value=month)
        ws.cell(row=r, column=2, value=days)
        ws.cell(row=r, column=3, value=u2)
        ws.cell(row=r, column=4, value=peak)
        ws.cell(row=r, column=5, value=u2 + peak)
        ws.cell(row=r, column=6, value=(u2 + peak) * days)
        for col in (3, 4, 5, 6):
            ws.cell(row=r, column=col).number_format = "#,##0"
        r += 1
    ws.cell(row=r, column=1, value="Quarter").font = bold
    ws.cell(row=r, column=2, value=sum(d for _, d, _, _ in W.PLAN_Q1)).font = bold
    c = ws.cell(row=r, column=6, value=sum((u + p) * d for _, d, u, p in W.PLAN_Q1))
    c.font = bold
    c.number_format = "#,##0"
    ws.cell(row=r + 2, column=1, value="Unit 2 at full heat load on coal from 1 January; the peak boilers burn coal "
                                       "below -15 C outdoor temperature per the heat plan.")
    for col, w in zip("ABCDEF", (14, 7, 15, 20, 15, 15)):
        ws.column_dimensions[col].width = w
    ws.freeze_panes = "A5"

    ws2 = wb.create_sheet("Availability")
    rows = [["Unit", "Planned stop", "From", "To", "Note"],
            ["Unit 2", "none in the quarter", None, None, "annual outage planned for June 2027"],
            ["Peak boiler K3", "burner inspection", "2027-02-15", "2027-02-17", "K4 available"],
            ["Peak boiler K4", "none in the quarter", None, None, None]]
    for i, row in enumerate(rows, 1):
        for j, v in enumerate(row, 1):
            cell = ws2.cell(row=i, column=j, value=v)
            if i == 1:
                cell.font = bold
    for col, w in zip("ABCDE", (16, 20, 12, 12, 36)):
        ws2.column_dimensions[col].width = w

    ws3 = wb.create_sheet("Heat demand")
    heat = [("January", 236400), ("February", 214900), ("March", 188200)]
    ws3.append(["Month", "District heat to the network, MWh", "Of which unit 2, MWh"])
    for c in ws3[1]:
        c.font = bold
    for mth, mwh in heat:
        ws3.append([mth, mwh, int(round(mwh * 0.71, -2))])
    for col, w in zip("ABC", (12, 32, 22)):
        ws3.column_dimensions[col].width = w
    wb.save(path)
