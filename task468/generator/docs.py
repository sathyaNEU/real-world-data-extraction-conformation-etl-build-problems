"""The pack's documents: the Specialty Clinical Pharmacy Program charter, the January 2026 formulary bulletin, the PBM
transition file notes, Tallis's 2026 price schedule, Orrin Rx's 2025 rebate statement, and the two distractors (Orrin's
2025 specialty trend report and the medical-benefit infusion summary), with each file's date."""
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

import numpy as np    # noqa: E402

import world as W     # noqa: E402
import sim as S       # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("LiberationSerif", "Regular"), ("LiberationSerif-Bold", "Bold"), ("LiberationSerif-Italic", "Italic"),
              ("LiberationSans", "Regular"), ("LiberationSans-Bold", "Bold"), ("LiberationSans-Italic", "Italic")):
    try:
        pdfmetrics.getFont(nm)
    except KeyError:
        pdfmetrics.registerFont(TTFont(nm, FONT_DIR + nm.split("-")[0] + "-" + f + ".ttf"))
INK = colors.HexColor("#1b1d1f")
GREY = colors.HexColor("#5b6067")
NAVY = colors.HexColor("#1d3557")
TEAL = colors.HexColor("#0f5c63")
PLUM = colors.HexColor("#5a2a4f")
BODY = ParagraphStyle("body", fontName="LiberationSerif", fontSize=10.5, leading=14.2, textColor=INK, spaceAfter=6)
SANS = ParagraphStyle("sans", fontName="LiberationSans", fontSize=9.6, leading=13.2, textColor=INK, spaceAfter=6)
CELL = ParagraphStyle("cell", fontName="LiberationSans", fontSize=8.4, leading=10.4, textColor=INK)
CELLB = ParagraphStyle("cellb", parent=CELL, fontName="LiberationSans-Bold")
SMALL = ParagraphStyle("small", fontName="LiberationSans", fontSize=8.3, leading=10.8, textColor=GREY)


def styles(accent, serif=False):
    face = "LiberationSerif" if serif else "LiberationSans"
    h1 = ParagraphStyle("h1", fontName=face + "-Bold", fontSize=14, leading=18, textColor=accent, spaceAfter=2)
    h1s = ParagraphStyle("h1s", fontName=face, fontSize=9.3, leading=12.5, textColor=GREY, spaceAfter=10)
    h2 = ParagraphStyle("h2", fontName=face + "-Bold", fontSize=10.5, leading=14, textColor=INK, spaceBefore=7,
                        spaceAfter=3, keepWithNext=1)
    return h1, h1s, h2


def _doc(path, title, author, footer, layout="left"):
    def frame(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(GREY)
        if layout == "left":
            canvas.setFont("LiberationSans", 7.5)
            canvas.drawString(0.9 * inch, 0.6 * inch, footer)
            canvas.drawRightString(letter[0] - 0.9 * inch, 0.6 * inch, "Page %d" % doc.page)
        elif layout == "centre":
            canvas.setFont("LiberationSerif", 8.5)
            canvas.drawCentredString(letter[0] / 2, 0.6 * inch, "%s  -  %d" % (footer, doc.page))
        else:
            canvas.setFont("LiberationSans", 8)
            canvas.drawString(0.9 * inch, letter[1] - 0.55 * inch, footer)
            canvas.setStrokeColor(GREY)
            canvas.setLineWidth(0.5)
            canvas.line(0.9 * inch, letter[1] - 0.6 * inch, letter[0] - 0.9 * inch, letter[1] - 0.6 * inch)
            canvas.drawCentredString(letter[0] / 2, 0.55 * inch, str(doc.page))
        canvas.restoreState()
    d = SimpleDocTemplate(path, pagesize=letter, leftMargin=0.9 * inch, rightMargin=0.9 * inch, topMargin=0.8 * inch,
                          bottomMargin=0.9 * inch, title=title, author=author, subject="", creator="", producer="")
    return d, frame


def _table(rows, widths, head="#e6eef0"):
    data = [[Paragraph(str(v), CELLB if i == 0 else CELL) for v in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9aa0a6")),
                           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(head)),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 4),
                           ("RIGHTPADDING", (0, 0), (-1, -1), 4)]))
    return t




def us_date(d):
    if isinstance(d, str):
        d = dt.date.fromisoformat(d)
    return d.strftime("%B ") + str(d.day) + d.strftime(", %Y")


def money(v):
    return "${:,.0f}".format(v)


# ---------------------------------------------------------------- the program charter
def write_charter(path):
    h1, h1s, h2 = styles(TEAL)
    d, frame = _doc(path, "Specialty Clinical Pharmacy Program: charter, program year 2026-27", W.PLAN,
                    W.PLAN + "  |  Pharmacy  |  " + W.PROGRAM + " charter, program year 2026-27")
    rows = [["Class code", "Class"]] + [[c, W.CLASSES[c]["name"]] for c in W.CANDIDATES]
    s = [Paragraph(W.PROGRAM, h1),
         Paragraph("Charter for the program year July 1, 2026 to June 30, 2027. Approved by %s, %s, May 28, 2026."
                   % (W.PEOPLE["director"], W.TITLES["director"]), h1s),
         Paragraph("1. The program", h2),
         Paragraph("1.1 The program's clinical pharmacists work with members on specialty therapy under the pharmacy "
                   "benefit: adherence and refill coordination, side-effect management, and liaison with prescribers. "
                   "Specialty drugs given under the medical benefit are outside the program.", SANS),
         Paragraph("1.2 The program manages the nine specialty classes below. A drug's class is its class code in "
                   "Tallis Pharmacy Services' specialty drug list.", SANS),
         _table(rows, [1.0 * 72, 4.6 * 72]),
         Paragraph("2. Caseloads and managed spend", h2),
         Paragraph("2.1 A class's caseload for the program year is the members who are on therapy in the class on June "
                   "30, 2026: a member is on therapy in a class on a day when a fill of one of the class's drugs, "
                   "dispensed on or before that day, has a days' supply that reaches it.", SANS),
         Paragraph("2.2 A class's managed spend for the program year is the plan's spend on its caseload members' "
                   "fills in the class dispensed from July 1, 2026 to June 30, 2027. Spend is priced at the Tallis "
                   "2026 specialty price schedule: the units dispensed times the schedule's unit price for the fill's "
                   "NDC, plus the schedule's dispensing fee for each fill, before member cost sharing. A reversed "
                   "claim is not spend.", SANS),
         Paragraph("3. Staffing", h2),
         Paragraph("3.1 Each class is staffed with one clinical pharmacist for each $1.5 million of its managed spend "
                   "for the program year, or part of $1.5 million. The staffing is set on the claims through June 30 "
                   "and presented to the executive team at its first meeting in August.", SANS),
         Paragraph("4. Reporting", h2),
         Paragraph("4.1 The program's annual report gives each class's manufacturer rebates on the previous calendar "
                   "year's utilization beside its staffing.", SANS)]
    d.build(s, onFirstPage=frame, onLaterPages=frame)


# ---------------------------------------------------------------- the formulary bulletin
def write_bulletin(path):
    h1, h1s, h2 = styles(PLUM, serif=True)
    d, frame = _doc(path, "Formulary bulletin, January 2026", W.PLAN,
                    W.PLAN + "  |  Pharmacy and Therapeutics Committee  |  Formulary bulletin, January 2026", "centre")
    s = [Paragraph("Formulary bulletin: changes effective January 1, 2026", h1),
         Paragraph("%s Pharmacy and Therapeutics Committee. Issued December 8, 2025." % W.PLAN, h1s),
         Paragraph("Pharmacy benefit manager", h2),
         Paragraph("%s administers the pharmacy benefit from January 1, 2026, replacing %s. Members continuing a "
                   "specialty therapy keep their prior authorization; the new PBM honours open authorizations until "
                   "they expire." % (W.NEW_PBM, W.OLD_PBM), BODY),
         Paragraph("Step therapy", h2),
         Paragraph("The step therapy requirement is removed for three specialty classes: weight management "
                   "(GLP-1 receptor agonists), severe asthma biologics and migraine prevention (CGRP). A prior "
                   "authorization confirming the clinical criteria is still required. Step therapy is unchanged for "
                   "the inflammatory conditions and multiple sclerosis classes.", BODY),
         Paragraph("Specialty pharmacy and mail", h2),
         Paragraph("Specialty fills continue through the network specialty pharmacies; maintenance therapies in the "
                   "HIV, multiple sclerosis, weight management and migraine classes may be dispensed as 84- or 90-day "
                   "supplies through mail order or a retail pharmacy.", BODY)]
    d.build(s, onFirstPage=frame, onLaterPages=frame)


# ---------------------------------------------------------------- the PBM transition notes
def write_transition(path):
    h1, h1s, h2 = styles(NAVY)
    d, frame = _doc(path, "PBM transition: claim file notes", W.PLAN,
                    W.PLAN + "  |  Pharmacy data  |  PBM transition file notes", "header")
    o = [["Field", "Contents"],
         ["claim_no", "Orrin's claim number. A reversal repeats the number of the claim it reverses."],
         ["line_type", "PAID, or REVERSAL for a line reversing a paid claim (its amounts and quantity negative)."],
         ["fill_date", "Date dispensed, yyyy-mm-dd."], ["member_key", "Orrin's member key."],
         ["ndc", "NDC in Orrin's 10-digit hyphenated form."], ["product_desc", "Product as Orrin labels it."],
         ["qty", "Units dispensed."], ["days_supply", "Days' supply."],
         ["ingredient_cost, dispensing_fee", "Orrin's contract amounts for the fill."],
         ["member_copay, plan_paid", "Member cost share and the plan's payment under Orrin's contract."],
         ["pharmacy_npi", "Dispensing pharmacy."]]
    t = [["Field", "Contents"],
         ["ClaimID", "Tallis's claim identifier."],
         ["Status", "P (paid) or R (reversed). A reversed claim appears as its paid line and an R line with the same "
                    "ClaimID; a corrected claim is resubmitted under a new ClaimID."],
         ["DateOfService", "Date dispensed, mm/dd/yyyy."], ["MemberNo", "Tallis's member number."],
         ["NDC11", "NDC, 11 digits, no hyphens."], ["Quantity", "Units dispensed."], ["DaysSupply", "Days' supply."],
         ["IngredientCost, DispFee", "The 2026 schedule's amounts for the fill."],
         ["CopayAmt, PlanPaidAmt", "Member cost share and the plan's payment."],
         ["PharmacyNPI, Channel", "Dispensing pharmacy and its channel (Specialty, Health-system, Mail, Retail)."]]
    s = [Paragraph("PBM transition: claim file notes", h1),
         Paragraph("%s, %s, with %s, %s. Updated July 14, 2026." % (W.PEOPLE["analyst"], W.TITLES["analyst"],
                                                                     W.PEOPLE["account"], W.TITLES["account"]), h1s),
         Paragraph("The files", h2),
         Paragraph("The specialty claims for the program come in two files: %s (Orrin Rx, fills dispensed January 1, "
                   "2019 to December 31, 2025) and %s (Tallis, fills dispensed January 1 to June 30, 2026, extracted "
                   "July 13, 2026). Each holds every specialty fill in the nine program classes under the pharmacy "
                   "benefit, with reversals. Orrin's extract starts at its 2019 archive, so a member filling in early 2019 "
                   "may have been on the drug for years before that." % (W.FILES["orrin"], W.FILES["tallis"]), SANS),
         Paragraph("Members", h2),
         Paragraph("Orrin keyed members by its own member key and Tallis by its own member number. %s gives each "
                   "member's plan ID with the Orrin key and the Tallis number the member held; a member who left the "
                   "plan before 2026 has no Tallis number and a member who joined in 2026 has no Orrin key."
                   % W.FILES["crosswalk"], SANS),
         Paragraph("Drugs and prices", h2),
         Paragraph("%s lists every NDC in the program classes with its class code; NDCs in the Orrin file are the same "
                   "products in 10-digit form. Orrin's amounts are Orrin's contract prices for each year; %s gives the "
                   "2026 Tallis schedule for every NDC." % (W.FILES["drugs"], W.FILES["prices"]), SANS),
         Paragraph(W.FILES["orrin"], h2), _table(o, [1.9 * 72, 4.7 * 72]),
         Paragraph(W.FILES["tallis"], h2), _table(t, [1.9 * 72, 4.7 * 72])]
    d.build(s, onFirstPage=frame, onLaterPages=frame)


# ---------------------------------------------------------------- distractor: Orrin's 2025 trend report
def write_trend(path, table):
    h1, h1s, h2 = styles(NAVY)
    d, frame = _doc(path, "Specialty drug trend report 2025", W.OLD_PBM,
                    W.OLD_PBM + "  |  Client analytics  |  Specialty drug trend report 2025 for " + W.PLAN)
    rows = [["Class", "Plan paid 2024", "Plan paid 2025", "Change", "Utilizers 2025"]]
    for c, a, b, u in table:
        rows.append([W.CLASSES[c]["name"], money(a), money(b), "%+.1f%%" % (100 * (b / a - 1)) if a else "new",
                     "{:,}".format(u)])
    s = [Paragraph("Specialty drug trend report 2025", h1),
         Paragraph("Prepared by %s client analytics for %s. February 20, 2026." % (W.OLD_PBM, W.PLAN), h1s),
         Paragraph("Spend", h2),
         Paragraph("Plan paid amounts under the Orrin contract for specialty fills in the plan's specialty classes, by "
                   "calendar year of dispensing, net of reversals. Utilizers are members with at least one paid fill in "
                   "the class in the year.", SANS),
         _table(rows, [2.6 * 72, 1.1 * 72, 1.1 * 72, 0.8 * 72, 1.0 * 72]),
         Paragraph("Outlook", h2),
         Paragraph("Specialty trend for commercial and Medicaid books of business ran at 9 to 12 per cent in 2025, "
                   "driven by utilization in the weight management and inflammatory classes and by price increases "
                   "averaging 5 per cent in January.", SANS)]
    d.build(s, onFirstPage=frame, onLaterPages=frame)


# ---------------------------------------------------------------- workbooks
def write_prices(path, rows):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    wb = Workbook()
    ws = wb.active
    ws.title = "Specialty schedule 2026"
    ws.append(["Tallis Pharmacy Services: specialty price schedule for %s, effective January 1, 2026" % W.PLAN])
    ws["A1"].font = Font(name="Calibri", bold=True, size=12)
    ws.append([])
    ws.append(["NDC11", "Product", "Unit price", "Dispensing fee per fill"])
    for c in ws[3]:
        c.font = Font(name="Calibri", bold=True)
        c.fill = PatternFill("solid", fgColor="E2EFDA")
    for ndc, prod, price, fee in rows:
        ws.append([ndc, prod, price, fee])
    for row in ws.iter_rows(min_row=4, max_row=ws.max_row):
        row[0].alignment = Alignment(horizontal="left")
        row[2].number_format = "#,##0.00"
        row[3].number_format = "#,##0.00"
    for col, wd in zip("ABCD", (14, 34, 12, 22)):
        ws.column_dimensions[col].width = wd
    ws.freeze_panes = "A4"
    wb.save(path)


def write_rebates(path, rows):
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill
    wb = Workbook()
    ws = wb.active
    ws.title = "Rebate statement"
    ws.append(["%s: manufacturer rebate statement for %s, contract years 2024 and 2025" % (W.OLD_PBM, W.PLAN)])
    ws["A1"].font = Font(name="Calibri", bold=True, size=12)
    ws.append(["Rebates pass through in full. Contract quarter is the quarter of the rebate contract year in which the "
               "fills were dispensed; invoice quarter is the calendar quarter the manufacturer was invoiced."])
    ws["A2"].font = Font(name="Calibri", italic=True, size=9)
    ws.append([])
    ws.append(["Invoice quarter", "Contract quarter", "Product", "Class code", "Channel", "Units", "Rebate"])
    for c in ws[4]:
        c.font = Font(name="Calibri", bold=True)
        c.fill = PatternFill("solid", fgColor="FFF2CC")
    for r in rows:
        ws.append(list(r))
    for row in ws.iter_rows(min_row=5, max_row=ws.max_row):
        row[5].number_format = "#,##0"
        row[6].number_format = "#,##0.00"
    for col, wd in zip("ABCDEFG", (15, 18, 32, 11, 11, 11, 14)):
        ws.column_dimensions[col].width = wd
    ws.freeze_panes = "A5"
    wb.save(path)


def write_infusions(path, table):
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill
    wb = Workbook()
    ws = wb.active
    ws.title = "Medical benefit 2025"
    ws.append(["%s: specialty drugs under the medical benefit, 2025 (physician-administered and infusion)" % W.PLAN])
    ws["A1"].font = Font(name="Calibri", bold=True, size=12)
    ws.append([])
    ws.append(["Therapeutic area", "Members", "Administrations", "Allowed amount"])
    for c in ws[3]:
        c.font = Font(name="Calibri", bold=True)
        c.fill = PatternFill("solid", fgColor="DDEBF7")
    for area, mem, adm, amt in table:
        ws.append([area, mem, adm, amt])
    for row in ws.iter_rows(min_row=4, max_row=ws.max_row):
        row[3].number_format = "#,##0"
    for col, wd in zip("ABCD", (34, 10, 15, 16)):
        ws.column_dimensions[col].width = wd
    wb.save(path)


# ---------------------------------------------------------------- each file's date in the folder
INDEX = [
    ("orrin", W.OLD_PBM, "2026-01-21", "Specialty claims, fills dispensed January 2019 to December 2025."),
    ("tallis", W.NEW_PBM, "2026-07-13", "Specialty claims, fills dispensed January to June 2026."),
    ("crosswalk", W.PLAN + ", Enrollment", "2026-07-08", "Member ID crosswalk across the PBM change."),
    ("drugs", W.NEW_PBM, "2026-06-01", "Specialty drug list with class codes."),
    ("prices", W.NEW_PBM, "2025-12-15", "Specialty price schedule, 2026."),
    ("charter", W.PLAN + ", Pharmacy", "2026-05-28", "Specialty Clinical Pharmacy Program charter, program year 2026-27."),
    ("bulletin", W.PLAN + ", P&T Committee", "2025-12-08", "Formulary bulletin, January 2026."),
    ("transition", W.PLAN + ", Pharmacy data", "2026-07-14", "PBM transition: claim file notes."),
    ("rebates", W.OLD_PBM, "2026-04-17", "Manufacturer rebate statement, contract years 2024 and 2025."),
    ("trend", W.OLD_PBM, "2026-02-20", "Specialty drug trend report 2025."),
    ("infusions", W.PLAN + ", Medical economics", "2026-03-09", "Specialty drugs under the medical benefit, 2025."),
]
