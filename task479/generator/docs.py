"""The pack's documents: the District's permit to operate, the 2025 performance test report, the vent calculation
basis, the CVS-1 component register, the District's AQ-117 form and the accounts payable workbook."""
import datetime as dt

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                      # noqa: E402
from reportlab.lib.pagesizes import letter                                            # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                       # noqa: E402
from reportlab.lib.units import inch                                                  # noqa: E402
from reportlab.pdfbase import pdfmetrics                                              # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                          # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import world as W     # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("LiberationSerif", "Regular"), ("LiberationSerif-Bold", "Bold"), ("LiberationSans", "Regular"),
              ("LiberationSans-Bold", "Bold")):
    try:
        pdfmetrics.getFont(nm)
    except KeyError:
        pdfmetrics.registerFont(TTFont(nm, FONT_DIR + nm.split("-")[0] + "-" + f + ".ttf"))
INK = colors.HexColor("#1d2329")
GREY = colors.HexColor("#5a6168")
BLUE = colors.HexColor("#1f3e66")
BODY = ParagraphStyle("body", fontName="LiberationSerif", fontSize=10.2, leading=13.6, textColor=INK, spaceAfter=5)
SMALL = ParagraphStyle("small", fontName="LiberationSerif", fontSize=8.6, leading=11.0, textColor=GREY, spaceAfter=4)
CELL = ParagraphStyle("cell", fontName="LiberationSans", fontSize=8.2, leading=10.2, textColor=INK)
CELLB = ParagraphStyle("cellb", fontName="LiberationSans-Bold", fontSize=8.2, leading=10.2, textColor=INK)
H2 = ParagraphStyle("h2", fontName="LiberationSans-Bold", fontSize=10.4, leading=13.6, textColor=INK, spaceBefore=7, keepWithNext=1,
                    spaceAfter=3)
DISTRICT = "Chalmont County Air Quality District"


def _frame(foot):
    def frame(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(GREY)
        canvas.setFont("LiberationSans", 7.0)
        canvas.drawString(0.85 * inch, 0.55 * inch, foot)
        canvas.drawRightString(letter[0] - 0.85 * inch, 0.55 * inch, "Page %d of %s" % (doc.page, "{pages}"))
        canvas.restoreState()
    return frame


class _Doc(SimpleDocTemplate):
    pass


def _build(path, make, foot, title, author):
    # two passes so the footer can carry the page count
    import io
    from reportlab.platypus import SimpleDocTemplate as SDT
    tmp = io.BytesIO()
    d = SDT(tmp, pagesize=letter, leftMargin=0.85 * inch, rightMargin=0.85 * inch, topMargin=0.75 * inch,
            bottomMargin=0.85 * inch, title=title, author=author, subject="", creator="", producer="")
    pages = [0]

    def count(canvas, doc):
        pages[0] = doc.page
    d.build(make(), onFirstPage=count, onLaterPages=count)
    total = pages[0]

    def frame(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(GREY)
        canvas.setFont("LiberationSans", 7.0)
        canvas.drawString(0.85 * inch, 0.55 * inch, foot)
        canvas.drawRightString(letter[0] - 0.85 * inch, 0.55 * inch, "Page %d of %d" % (doc.page, total))
        canvas.restoreState()
    d2 = SDT(path, pagesize=letter, leftMargin=0.85 * inch, rightMargin=0.85 * inch, topMargin=0.75 * inch,
             bottomMargin=0.85 * inch, title=title, author=author, subject="", creator="", producer="")
    d2.build(make(), onFirstPage=frame, onLaterPages=frame)


def _table(rows, widths, header=True, size=None):
    data = [[Paragraph(str(c), CELLB if (header and i == 0) else CELL) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0)
    st = [("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9aa3ab")), ("VALIGN", (0, 0), (-1, -1), "TOP"),
          ("LEFTPADDING", (0, 0), (-1, -1), 3), ("RIGHTPADDING", (0, 0), (-1, -1), 3),
          ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]
    if header:
        st.append(("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e6eaee")))
    t.setStyle(TableStyle(st))
    return t


PERMIT = [
    ("Section A. Emission units", None),
    ("TABLE_A", None),
    ("Section B. EU-P1 process vents", [
        "B.1 Limit. VOC emitted from EU-P1 shall not exceed 2.5 tons in any calendar year.",
        "B.2 Control. Each EU-P1 vent shall be routed through closed-vent system CVS-1 to RTO-1 whenever it is venting, "
        "and RTO-1 shall be operating whenever an EU-P1 vent is venting.",
        "B.3 Operating temperature. RTO-1 shall maintain a combustion chamber temperature of not less than 1,500 F on a "
        "3-hour block average. Each 3-hour block begins at 00:00, 03:00, 06:00, 09:00, 12:00, 15:00, 18:00 or 21:00 "
        "local time. A block average is the mean of the one-minute values recorded while RTO-1 is in mode RUN; a block "
        "with fewer than 135 such values is not a valid block.",
        "B.4 Destruction efficiency. For calculating EU-P1 emissions, RTO-1's VOC destruction efficiency is the "
        "efficiency demonstrated in the most recent performance test accepted by the District.",
        "B.5 Calculation and reporting. The permittee shall calculate VOC emitted from EU-P1 for each calendar quarter "
        "from the batch records and the vent calculation basis kept under B.6, and report it on District Form AQ-117 "
        "within 30 days after the quarter. The calendar-year total is the sum of the quarters.",
        "B.6 Vent calculation basis. The permittee shall maintain, for each product and batch step vented to CVS-1, the "
        "step's vent flow at standard conditions and its VOC emission rate, and shall revise the basis before a new "
        "product or step is vented.",
        "B.7 Records. The permittee shall keep batch records showing the start and end of each batch step on each EU-P1 "
        "vent, and RTO-1's combustion chamber temperature and operating mode for each minute, for five years.",
        "B.8 Testing. The permittee shall test RTO-1's VOC destruction efficiency at least once in each five-year term, "
        "at conditions representative of normal operation."]),
    ("Section C. Other emission units", [
        "C.1 EU-T1. Storage tank emissions shall be calculated annually and reported with the annual emission statement.",
        "C.2 EU-F1. Equipment in VOC service shall be monitored quarterly by Method 21; a reading of 500 ppm or more is a "
        "leak, repaired within 15 days.",
        "C.3 EU-B1 and EU-G1. Natural gas use for EU-B1 shall be recorded monthly; EU-G1 shall operate no more than 100 "
        "hours a year for maintenance and readiness testing."]),
    ("Section D. Definitions", [
        "D.1 Ton means 2,000 pounds. Emitted means released to the atmosphere. Standard conditions means 68 F and "
        "29.92 inches of mercury. Local time means the prevailing time at the plant. Calendar years and quarters are "
        "counted in local time.",
        "D.2 VOC means volatile organic compounds as defined in District Rule 102."]),
]


def write_permit(path):
    _build(path, _permit_story, "PTO-2219-0447 R3", "PTO-2219-0447 Revision 3", DISTRICT)


def _permit_story():
    story = [Paragraph(DISTRICT.upper(), ParagraphStyle("o", fontName="LiberationSans-Bold", fontSize=8.6,
                                                        textColor=BLUE, leading=11)),
             Paragraph("Permit to Operate PTO-2219-0447, Revision 3", ParagraphStyle(
                 "t", fontName="LiberationSans-Bold", fontSize=14, leading=18, textColor=INK, spaceAfter=4)),
             Paragraph("Permittee: Pellston Fine Chemicals, LLC, Harwick plant, 1840 Quarry Road, Harwick. "
                       "Revision 3 effective 1 April 2025 (adds reactor R-106, dryer D-202, the PX product line and the "
                       "reactor bay charging exhaust to EU-P1). Term ends 31 March 2030.", SMALL), Spacer(1, 4)]
    for head, paras in PERMIT:
        if head == "TABLE_A":
            rows = [["Unit", "Description", "Control", "Release points"],
                    ["EU-P1", "Process vents: reactors R-101 to R-106, each with its manway exhaust while solids are "
                              "charged; fluid-bed dryers D-201 and D-202; solvent recovery still SR-301",
                     "Closed-vent system CVS-1 to regenerative thermal oxidizer RTO-1 (Thermavex TVX-3800)",
                     "S-1 RTO-1 stack; S-2 RTO-1 emergency bypass stack"],
                    ["EU-T1", "Solvent storage tanks T-401 to T-410", "Conservation vents", "Tank vents"],
                    ["EU-F1", "Equipment leaks, pumps, valves and connectors in VOC service", "Monitoring and repair",
                     "Fugitive"],
                    ["EU-B1", "Steam boiler B-1, natural gas, 18.4 MMBtu/hr", "None", "S-4"],
                    ["EU-G1", "Emergency generator GEN-1, diesel, 600 kW", "None", "S-5"]]
            story.append(_table(rows, [0.6 * inch, 2.55 * inch, 1.95 * inch, 1.6 * inch]))
            continue
        story.append(Paragraph(head, H2))
        if paras:
            for p in paras:
                story.append(Paragraph(p, BODY))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Issued for the Air Pollution Control Officer, 24 March 2025. Permit engineer: R. Okafor.",
                           SMALL))
    return story


TEST_RUNS = [("1", "05/13/2025 09:40-10:40", "3,342", "51.9", "0.33", "99.36"),
             ("2", "05/13/2025 12:05-13:05", "3,371", "52.8", "0.29", "99.45"),
             ("3", "05/14/2025 08:55-09:55", "3,356", "52.5", "0.32", "99.39")]


def write_test(path):
    _build(path, _test_story, "BST-25-0418", "RTO-1 VOC Destruction Efficiency Test Report", "Brightline Source Testing, Inc.")


def _test_story():
    story = [Paragraph("BRIGHTLINE SOURCE TESTING, INC.", ParagraphStyle(
        "o", fontName="LiberationSans-Bold", fontSize=8.6, textColor=BLUE, leading=11)),
        Paragraph("RTO-1 VOC Destruction Efficiency Test Report", ParagraphStyle(
            "t", fontName="LiberationSans-Bold", fontSize=14, leading=18, textColor=INK, spaceAfter=4)),
        Paragraph("Pellston Fine Chemicals, LLC, Harwick plant. Permit PTO-2219-0447 R3, condition B.8. Test dates 13 "
                  "and 14 May 2025. Report BST-25-0418, issued 9 June 2025; accepted by the "
                  "%s by letter of 7 July 2025." % DISTRICT, SMALL),
        Paragraph("1. Summary", H2),
        Paragraph("Three one-hour runs were made at the RTO-1 inlet duct and stack S-1 by EPA Methods 1 to 4 and 25A. "
                  "The VOC destruction efficiency demonstrated is <b>99.4 per cent</b>, the mean of the three runs. "
                  "The combustion chamber temperature averaged 1,561 F over the runs.", BODY),
        Paragraph("2. Results", H2),
        _table([["Run", "Time", "Inlet flow (scfm)", "Inlet VOC (lb/hr)", "Outlet VOC (lb/hr)", "Efficiency (%)"]] +
               [list(r) for r in TEST_RUNS], [0.4 * inch, 1.55 * inch, 1.0 * inch, 1.05 * inch, 1.1 * inch, 0.95 * inch]),
        Spacer(1, 6),
        Paragraph("3. Process conditions during the runs", H2),
        Paragraph("The test was run with reactors R-101 (heat to reflux and reaction hold, PFC-2140), R-103 (extraction, "
                  "PFC-2315) and R-104 (vacuum distillation, PFC-3021) venting, dryer D-201 in its drying step and the "
                  "still SR-301 on feed and reflux. Using the plant's vent calculation basis for the steps in progress, "
                  "the inlet VOC loading expected for each run was 51.0, 51.6 and 51.3 lb/hr, within 3 per cent of the "
                  "measured loading.", BODY),
        Paragraph("4. Quality assurance", H2),
        Paragraph("Analyzer calibration error, drift and response checks met Method 25A criteria before and after each "
                  "run. Flow measurements met Method 2 cyclonic flow criteria at both locations.", BODY),
        Spacer(1, 8),
        Paragraph("Prepared by: M. Halvorsen, QSTI. Reviewed by: T. Ingram, Project Manager.", SMALL)]
    return story


# --------------------------------------------------------------------------------------------- workbooks
def _book():
    import openpyxl
    return openpyxl.Workbook()


def _hdr(ws, row, cols, bold=True):
    from openpyxl.styles import Font, PatternFill, Alignment
    for j, c in enumerate(cols, 1):
        cell = ws.cell(row=row, column=j, value=c)
        cell.font = Font(bold=bold)
        cell.fill = PatternFill("solid", fgColor="DDE3EA")
        cell.alignment = Alignment(wrap_text=True, vertical="top")


def write_basis(path):
    from openpyxl.styles import Font
    wb = _book()
    ws = wb.active
    ws.title = "Cover"
    lines = ["Pellston Fine Chemicals, Harwick plant", "EU-P1 Vent Calculation Basis (permit condition B.6)",
             "Revision 7, approved 18 March 2025", "Prepared: Process Engineering (D. Gonzalez); approved: "
             "Environmental (A. Alexander)", "",
             "Revision history", "Rev 5, 02/2022: PFC-3021 vacuum distillation re-rated.",
             "Rev 6, 11/2023: PFC-2315 extraction added.",
             "Rev 7, 03/2025: R-106, D-202 and the PX-711 and PX-714 line (licensor sheet carried as issued); reactor bay "
             "charging exhaust tied into CVS-1."]
    for i, s in enumerate(lines, 1):
        if s:
            ws.cell(row=i, column=1, value=s).font = Font(bold=(i <= 2))
    ws.column_dimensions["A"].width = 110
    ws2 = wb.create_sheet("Reactor steps")
    _hdr(ws2, 1, ["Product", "Step", "Description", "Typical minutes", "Vent flow (scfm)", "VOC (lb/hr)"])
    r = 2
    for prod, (unit, steps) in W.REACTOR.items():
        if unit != "us":
            continue
        for k, (key, name, mean, flow, voc) in enumerate(steps, 1):
            for j, v in enumerate([prod, k, name, mean, flow, voc], 1):
                ws2.cell(row=r, column=j, value=(None if v == "" else v))
            r += 1
    for col, wdt in zip("ABCDEF", (12, 6, 34, 15, 15, 12)):
        ws2.column_dimensions[col].width = wdt
    ws3 = wb.create_sheet("PX line (licensor)")
    ws3.cell(row=1, column=1, value="Licensor vent sheet LS-PX-07, issue C. Gas volumes at normal reference conditions "
                                    "(0 C, 101.325 kPa); emission rates in kg/h.")
    _hdr(ws3, 2, ["Product", "Step", "Description", "Typical minutes", "Vent flow (Nm3/h)", "VOC (kg/h)"])
    r = 3
    for prod, (unit, steps) in W.REACTOR.items():
        if unit != "metric":
            continue
        for k, (key, name, mean, flow, voc) in enumerate(steps, 1):
            for j, v in enumerate([prod, k, name, mean, flow, voc], 1):
                ws3.cell(row=r, column=j, value=(None if v == "" else v))
            r += 1
    for col, wdt in zip("ABCDEF", (12, 6, 34, 15, 17, 12)):
        ws3.column_dimensions[col].width = wdt
    ws4 = wb.create_sheet("Dryer steps")
    _hdr(ws4, 1, ["Product dried", "Step", "Description", "Typical minutes", "Vent flow (scfm)", "VOC (lb/hr)"])
    r = 2
    for prod, steps in W.DRYER.items():
        for k, (key, name, mean, flow, voc) in enumerate(steps, 1):
            for j, v in enumerate([prod, k, name, mean, flow, voc], 1):
                ws4.cell(row=r, column=j, value=(None if v == "" else v))
            r += 1
    for col, wdt in zip("ABCDEF", (14, 6, 26, 15, 15, 12)):
        ws4.column_dimensions[col].width = wdt
    ws5 = wb.create_sheet("Other vents")
    _hdr(ws5, 1, ["Vent", "Step", "Description", "Typical minutes", "Vent flow (scfm)", "VOC (lb/hr)"])
    rows = [("Reactor, campaign change", 1, W.CLEAN[1], W.CLEAN[2], W.CLEAN[3], W.CLEAN[4]),
            ("Reactor, any product", "", W.HOLD[1], "as held", W.HOLD[3], W.HOLD[4]),
            ("SR-301", 1, W.STILL[0][1], "as run", W.STILL[0][3], W.STILL[0][4]),
            ("SR-301", 2, W.STILL[1][1], W.STILL[1][2], W.STILL[1][3], W.STILL[1][4])]
    for i, row in enumerate(rows, 2):
        for j, v in enumerate(row, 1):
            ws5.cell(row=i, column=j, value=(None if v == "" else v))
    for col, wdt in zip("ABCDEF", (26, 6, 32, 15, 15, 12)):
        ws5.column_dimensions[col].width = wdt
    wb.save(path)


REGISTER = [
    ("VL-101", "Vent line, reactor R-101, incl. manway exhaust branch MH-101", "R-101 to HDR-1", '3" / 8"', "", "CVS-1", "P-201", "2026-03-11"),
    ("VL-102", "Vent line, reactor R-102, incl. manway exhaust branch MH-102", "R-102 to HDR-1", '3" / 8"', "", "CVS-1", "P-201", "2026-03-11"),
    ("VL-103", "Vent line, reactor R-103, incl. manway exhaust branch MH-103", "R-103 to HDR-1", '3" / 8"', "", "CVS-1", "P-202", "2026-03-11"),
    ("VL-104", "Vent line, reactor R-104, incl. manway exhaust branch MH-104", "R-104 to HDR-1", '3" / 8"', "", "CVS-1", "P-202", "2026-03-12"),
    ("VL-105", "Vent line, reactor R-105, incl. manway exhaust branch MH-105", "R-105 to HDR-1", '4" / 10"', "", "CVS-1", "P-203", "2026-03-12"),
    ("VL-106", "Vent line, reactor R-106, incl. manway exhaust branch MH-106", "R-106 to HDR-1", '4" / 10"', "", "CVS-1", "P-203", "2026-03-12"),
    ("VL-201", "Purge line, fluid-bed dryer D-201 (after condenser E-201)", "D-201 to HDR-1", '12"', "", "CVS-1", "P-210", "2026-03-13"),
    ("VL-202", "Purge line, fluid-bed dryer D-202 (after condenser E-202)", "D-202 to HDR-1", '12"', "", "CVS-1", "P-210", "2026-03-13"),
    ("VL-301", "Vent line, solvent recovery still SR-301", "SR-301 to HDR-1", '3"', "", "CVS-1", "P-220", "2026-03-13"),
    ("FA-101", "Flame arrestor, VL-101 to VL-106 common", "HDR-1", '14"', "", "", "P-201", "2026-03-11"),
    ("XV-110", "Isolation damper, reactor bay manway exhaust", "MH-101 to MH-106", '10"', "Fail open", "", "P-201", "2026-03-11"),
    ("HDR-1", "CVS-1 header duct to RTO-1 inlet", "VL-101 to VL-301 to RTO-1", '18"', "", "", "P-230", "2026-03-14"),
    ("PSV-31", "Header pressure relief at RTO-1 inlet plenum", "HDR-1", '10" x 12"', "Set +6.0 in w.c.",
     "Atmosphere, vent stack S-3", "P-230", "2026-05-20"),
    ("XV-30", "RTO-1 emergency bypass damper", "HDR-1 to S-2", '18"', "Open whenever RTO-1 is not in RUN", "Stack S-2",
     "P-230", "2026-03-14"),
    ("FN-1", "RTO-1 induced-draft fan, VFD", "RTO-1", "40 hp", "3,800 scfm at 18 in w.c.", "", "P-231", "2026-03-14"),
    ("RTO-1", "Regenerative thermal oxidizer, Thermavex TVX-3800, two-bed", "HDR-1 to S-1", "",
     "Maximum process flow 3,800 scfm", "Stack S-1", "P-231", "2026-08-03"),
    ("TE-101A", "Combustion chamber thermocouple, DAHS chamber input", "RTO-1", "Type K", "", "", "P-231", "2026-08-26"),
    ("TE-101B", "Combustion chamber thermocouple, redundant", "RTO-1", "Type K", "", "", "P-231", "2026-03-14"),
]


def write_register(path):
    from openpyxl.styles import Font
    wb = _book()
    ws = wb.active
    ws.title = "CVS-1"
    ws.cell(row=1, column=1, value="Pellston Fine Chemicals, Harwick plant").font = Font(bold=True)
    ws.cell(row=2, column=1, value="CVS-1 closed-vent system component register, Rev 4 (2026-08-28)").font = Font(bold=True)
    ws.merge_cells("A1:H1")
    ws.merge_cells("A2:H2")
    _hdr(ws, 4, ["Tag", "Description", "Connects", "Size", "Rating / set point", "Discharge", "P&ID", "Last inspected"])
    for i, row in enumerate(REGISTER, 5):
        for j, v in enumerate(row, 1):
            ws.cell(row=i, column=j, value=(None if v == "" else v))
    for col, wdt in zip("ABCDEFGH", (9, 52, 24, 11, 26, 26, 7, 14)):
        ws.column_dimensions[col].width = wdt
    wb.save(path)


def write_form(path):
    from openpyxl.styles import Font
    wb = _book()
    ws = wb.active
    ws.title = "AQ-117"
    rows = [(DISTRICT, None), ("Form AQ-117  Quarterly Emission Unit Report (Rev. 2023-01)", None), ("", None),
            ("Permittee", ""), ("Permit No.", ""), ("Emission unit", ""), ("Pollutant", "VOC"), ("Calendar year", ""), ("", None)]
    for i, (a, b) in enumerate(rows, 1):
        if a:
            ws.cell(row=i, column=1, value=a)
        if b:
            ws.cell(row=i, column=2, value=b)
    ws.cell(row=1, column=1).font = Font(bold=True)
    ws.cell(row=2, column=1).font = Font(bold=True)
    _hdr(ws, 10, ["Quarter", "Emitted this quarter (tons)", "Calendar year to date (tons)", "Calendar-year limit (tons)"])
    for k, q in enumerate(["Q1 (Jan-Mar)", "Q2 (Apr-Jun)", "Q3 (Jul-Sep)", "Q4 (Oct-Dec)"], 11):
        ws.cell(row=k, column=1, value=q)
    ws.cell(row=16, column=1, value="Certified true, accurate and complete (responsible official):")
    ws.cell(row=17, column=1, value="Name / title / date")
    for col, wdt in zip("ABCD", (34, 28, 28, 26)):
        ws.column_dimensions[col].width = wdt
    wb.save(path)


AP_COLS = ["Invoice No", "Invoice Date", "Vendor", "PO Number", "Delivery Ticket", "Delivery Date", "Line",
           "Item Text", "Qty", "UoM", "Unit Price", "Amount", "Doc Type"]


def write_ap(path, lines):
    wb = _book()
    ws = wb.active
    ws.title = "AP lines FY2026"
    _hdr(ws, 1, AP_COLS)
    for i, r in enumerate(lines, 2):
        vals = [r["invoice"], r["date"].strftime("%Y-%m-%d"), r["vendor"], r["po"], r["ticket"],
                r["delivered"].strftime("%Y-%m-%d"), r["line"], r["text"], r["qty"], r["uom"], r["price"], r["amount"],
                r["doc"]]
        for j, v in enumerate(vals, 1):
            ws.cell(row=i, column=j, value=(None if v == "" else v))
    for col, wdt in zip("ABCDEFGHIJKLM", (14, 12, 32, 11, 13, 12, 6, 54, 10, 6, 10, 12, 8)):
        ws.column_dimensions[col].width = wdt
    wb.save(path)
