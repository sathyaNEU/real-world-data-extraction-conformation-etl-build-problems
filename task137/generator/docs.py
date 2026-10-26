"""The pack's documents: the planning brief (docx), the custody demand model note (pdf), the suite allocation workbook
with the custody service's notes (xlsx), the estates register (xlsx), and the three background files (ONS ward
population, the late-night licences register, GOV.UK's bank holidays)."""
import datetime as dt
import json

import docx
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt, RGBColor, Mm
import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill
from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                      # noqa: E402
from reportlab.lib.pagesizes import A4                                                # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                       # noqa: E402
from reportlab.lib.units import mm                                                    # noqa: E402
from reportlab.pdfbase import pdfmetrics                                              # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                          # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import world as WD   # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/"
for _n, _f in (("Carlito", "crosextra/Carlito-Regular.ttf"), ("Carlito-Bold", "crosextra/Carlito-Bold.ttf"),
               ("Carlito-Italic", "crosextra/Carlito-Italic.ttf")):
    pdfmetrics.registerFont(TTFont(_n, FONT_DIR + _f))
SANS, SANS_B, SANS_I = "Carlito", "Carlito-Bold", "Carlito-Italic"
INK = colors.HexColor("#1f2428")
GREY = colors.HexColor("#5b6670")
NAVY = colors.HexColor("#1b365d")
RULE = colors.HexColor("#a7b0b8")
BODY = ParagraphStyle("body", fontName=SANS, fontSize=10, leading=13.4, textColor=INK, spaceAfter=5)
CLAUSE = ParagraphStyle("clause", parent=BODY, leftIndent=26, firstLineIndent=-26)
H1 = ParagraphStyle("h1", fontName=SANS_B, fontSize=15, leading=19, textColor=NAVY, spaceAfter=2)
H1S = ParagraphStyle("h1s", fontName=SANS, fontSize=10, leading=13, textColor=GREY, spaceAfter=10)
H2 = ParagraphStyle("h2", fontName=SANS_B, fontSize=11, leading=14, textColor=INK, spaceBefore=8, spaceAfter=3)
NOTE = ParagraphStyle("note", fontName=SANS_I, fontSize=8.6, leading=11, textColor=GREY, spaceBefore=3)
CELL = ParagraphStyle("cell", fontName=SANS, fontSize=9.2, leading=11.4, textColor=INK)
CELLB = ParagraphStyle("cellb", parent=CELL, fontName=SANS_B)
CELLR = ParagraphStyle("cellr", parent=CELL, alignment=2)
CELLBR = ParagraphStyle("cellbr", parent=CELLB, alignment=2)

PEOPLE = {"planner": "Emma Roberts", "programme": "Liam Clayton", "custody": "Emma Roberts"}   # guard.py names --geo GB --seed 137


def _footer(left, right):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFont(SANS, 7.6)
        canvas.setFillColor(GREY)
        canvas.drawString(20 * mm, 11 * mm, left)
        canvas.drawRightString(A4[0] - 20 * mm, 11 * mm, "%s  |  Page %d" % (right, doc.page))
        canvas.restoreState()
    return draw


def fmt(n):
    return "{:,}".format(int(round(n)))


# ------------------------------------------------------------------------------------------------------------------
# The custody demand model (pdf)
MODEL_METHOD = [
    ("2.1", "A suite's demand is the people arrested in the wards it serves, as set in the suite allocation."),
    ("2.2", "Each ward's arrests are counted by financial year (1 April to 31 March), by the date of arrest in UK "
            "time."),
    ("2.3", "The ward's arrests in the latest full year are carried forward at its average annual change over the "
            "three years to that year (the cube root of the latest year's arrests over the arrests three years "
            "earlier, less one), capped at 10 per cent a year in either direction."),
    ("2.4", "A suite's figure for a year is the sum of its wards' figures."),
]


def model_validation_text(rows):
    worst = max(abs(r[3] - 1) for r in rows)
    pct = int(-(-worst * 100 // 1))           # whole per cent, rounded up
    return pct


def write_model(path, val_rows):
    """val_rows: (suite, forecast, actual, ratio) for 2025-26 from the records to 31 March 2025."""
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=22 * mm, rightMargin=22 * mm, topMargin=20 * mm,
                            bottomMargin=22 * mm, title="Custody demand model, version 2.0", author="Custody Services Planning",
                            subject="", creator="", producer="")
    pct = model_validation_text(val_rows)
    s = [Paragraph("HARROWDOWN POLICE", ParagraphStyle("hp", parent=H1S, fontName=SANS_B, textColor=NAVY, spaceAfter=0)),
         Paragraph("Custody Services", H1S),
         Paragraph("Custody demand model", H1),
         Paragraph("Version 2.0. Approved by the Custody Programme Board on 11 June 2026. Owner: Custody Services "
                   "Planning, Force Headquarters, Wendle Cross.", H1S),
         Paragraph("1  Purpose", H2),
         Paragraph("The model gives each custody suite a planning figure: the detentions the suite should expect to book "
                   "in a financial year. Cells, detention officer posts and the custody healthcare contract are sized "
                   "from it.", BODY),
         Paragraph("2  Method", H2)]
    for no, t in MODEL_METHOD:
        s.append(Paragraph("%s&nbsp;&nbsp;&nbsp;%s" % (no, t), CLAUSE))
    s += [Paragraph("3  Validation", H2),
          Paragraph("The model was run on the arrest records to 31 March 2025 (base year 2024-25, change measured from "
                    "2021-22) and its forecast for 2025-26 compared with the arrest records for that year.", BODY)]
    data = [[Paragraph("Suite", CELLB), Paragraph("Forecast 2025-26", CELLBR), Paragraph("Arrest records 2025-26", CELLBR),
             Paragraph("Forecast / records", CELLBR)]]
    for suite, f, a, r in val_rows:
        data.append([Paragraph(suite, CELL), Paragraph(fmt(f), CELLR), Paragraph(fmt(a), CELLR),
                     Paragraph("%.3f" % r, CELLR)])
    t = Table(data, colWidths=[46 * mm, 36 * mm, 42 * mm, 36 * mm], hAlign="LEFT")
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.6, RULE), ("LINEBELOW", (0, -1), (-1, -1), 0.4, RULE),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 2),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]))
    s += [t, Spacer(1, 6),
          Paragraph("Every suite came within %d per cent. Version 1 (2022) carried every ward at the force-wide change "
                    "and was 6 per cent out at Eastmoor; version 2 replaced it." % pct, BODY),
          Paragraph("4  Review", H2),
          Paragraph("The model is reviewed each June, and when a suite opens or closes.", BODY)]
    doc.build(s, onFirstPage=_footer("Custody Services Planning", "Custody demand model v2.0"),
              onLaterPages=_footer("Custody Services Planning", "Custody demand model v2.0"))
    return pct


# ------------------------------------------------------------------------------------------------------------------
# The planning brief (docx)
FILES = [
    ("calderwick_police_arrests_2021-04_2026-09.csv",
     "The force's arrest records, pulled on 6 October 2026: one row per arrest by a Calderwick Police officer, 1 April "
     "2021 to 30 September 2026. custody_suite is the suite the person was booked into, and arrested_utc and "
     "booked_in_utc are in UTC. ward is the ward where the arrest was made and offence_group the main offence. "
     "detention_hhmm is the PACE detention clock in hours and minutes, from detention being authorised to release, "
     "charge or transfer."),
    ("police_uk_street_crime_2025-26.csv",
     "Street-level crime in the force area from data.police.uk, April 2025 to March 2026, as the Calderwick and Carvell "
     "Community Safety Partnership downloads it each month (anti-social behaviour taken out). Locations are "
     "data.police.uk's anonymised map points."),
    ("lsoa21_to_ward_lookup.csv", "2021 LSOAs to the wards they sit in (best fit)."),
    ("custody_suite_allocation_2027.xlsx",
     "Each ward's custody suite to 31 March 2027 and from 1 April 2027, with the custody service's notes."),
    ("custody_demand_model_v2.pdf", "The custody demand model as the Custody Programme Board approved it in June."),
    ("cju_remand_files_2025-03_2026-04.csv",
     "The Criminal Justice Unit's remand files: one row per case file prepared for a remand court, for charges from "
     "1 March 2025 to 30 April 2026. linked_arrest is the arrest reference on the file; charged and handed_to_escort "
     "are UK times."),
    ("custody_healthcare_contacts_2025-26.csv",
     "Calderwick Healthcare Partners' contact export for the four suites, 1 April 2025 to 31 March 2026: one row per "
     "clinician contact. suite is the custody suite of the clinician's team; started and ended are UK times."),
    ("custody_estate_register_2026.xlsx", "The estates team's register of the four suites."),
    ("ward_population_mid-2024.csv", "ONS mid-2024 population estimates for the force area's wards."),
    ("late_night_licences_2026.csv", "The licensing team's register of premises licensed to open past midnight."),
    ("bank-holidays.json", "Bank holidays from GOV.UK."),
]


def _para(d, text, size=10.5, bold=False, italic=False, color=None, after=6, before=0, align=None):
    p = d.add_paragraph()
    r = p.add_run(text)
    r.font.size = Pt(size)
    r.bold = bold
    r.italic = italic
    if color:
        r.font.color.rgb = RGBColor.from_string(color)
    p.paragraph_format.space_after = Pt(after)
    p.paragraph_format.space_before = Pt(before)
    if align:
        p.alignment = align
    return p


def write_brief(path):
    d = docx.Document()
    sec = d.sections[0]
    sec.page_height, sec.page_width = Mm(297), Mm(210)
    sec.left_margin = sec.right_margin = Mm(22)
    sec.top_margin, sec.bottom_margin = Mm(20), Mm(20)
    st = d.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    _para(d, "Calderwick Police  |  Estates and Custody Programme", size=9, color="5B6670", after=2)
    _para(d, "Tanner Street custody hub: planning figure for 2027-28", size=15, bold=True, color="1B365D", after=4)
    _para(d, "To: %s, Custody Services Planning\nFrom: %s, Programme Manager\nDate: 20 October 2026"
          % (PEOPLE["planner"], PEOPLE["programme"]), size=9.5, color="5B6670", after=10)
    _para(d, "The Tanner Street custody hub opens on 1 April 2027. From that date it takes the six city centre wards "
             "(Abbey Fields, Castle, Cathedral, Kingsway, Mill Bank and St Peter's), which Northgate and Eastmoor serve "
             "until 31 March 2027. The suite allocation workbook gives every ward's suite before and after the change.")
    _para(d, "The fit-out contract with Brennand Interiors is signed on 9 December. It fixes the hub's cells and "
             "detention officer posts from the hub's planning figure for 2027-28, its first year: the detentions the "
             "hub will book from 1 April 2027 to 31 March 2028, to the nearest 250.")
    _para(d, "The contract sizes the remand cells from the four suites' remand holds for the defendants charged in "
             "2025-26 and kept in custody for court, suite by suite: their cell hours from charge to handover to the "
             "court escort, and how many of them were held for more than 24 hours from booking in. It sizes the medical "
             "rooms from each suite's initial health assessments in 2025-26, those begun in the day (07:00 to 19:00) "
             "and those begun at night.")
    _para(d, "Files", size=11, bold=True, before=6, after=4)
    for name, text in FILES:
        p = d.add_paragraph()
        r = p.add_run(name)
        r.bold = True
        r.font.size = Pt(9.5)
        r2 = p.add_run("  " + text)
        r2.font.size = Pt(9.5)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.left_indent = Mm(4)
    _para(d, PEOPLE["programme"].split()[0], size=10.5, before=8, after=0)
    d.save(path)


# ------------------------------------------------------------------------------------------------------------------
# The suite allocation workbook (xlsx)
ALLOC_NOTES = [
    "This allocation takes effect at 00:00 on 1 April 2027 and replaces the allocation of 1 April 2019.",
    "A detainee is taken to the custody suite that serves the ward where the arrest was made, whichever force or agency "
    "the arresting officer belongs to, and the custody officer there decides whether to authorise detention.",
    "When the ward's suite is full or closed, the Force Control Room sends the arresting officer to the nearest suite "
    "with a free cell, and the detainee is booked in and stays there.",
    "Detainees held under section 41 of the Terrorism Act 2000 go to the regional designated suite outside the force "
    "area.",
    "People detained under section 136 of the Mental Health Act 1983 go to the health-based place of safety at "
    "Calderwick Royal Infirmary, not to a custody suite.",
    "Children aged 10 to 17 go to the ward's suite like adults; Tanner Street has two detention rooms for children.",
    "Northgate and Eastmoor keep their other wards, and no county ward changes suite.",
]


def write_allocation(path, wcode):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Allocation"
    hdr = ["ward_code", "ward", "district", "suite_to_31_march_2027", "suite_from_1_april_2027"]
    ws.append(hdr)
    for w in WD.WARDS:
        ws.append([wcode[w], w, WD.DISTRICT[w], WD.SUITE_NOW[w], WD.SUITE_2027[w]])
    for c in ws[1]:
        c.font = Font(bold=True)
    for col, wdt in zip("ABCDE", (13, 18, 15, 24, 25)):
        ws.column_dimensions[col].width = wdt
    ws.freeze_panes = "A2"
    ns = wb.create_sheet("Notes")
    ns.append(["Custody suite allocation by ward: notes"])
    ns["A1"].font = Font(bold=True, size=12)
    ns.append(["Custody Services, Force Headquarters. Approved by the Custody Programme Board, 10 September 2026."])
    ns.append([])
    for k, t in enumerate(ALLOC_NOTES, 1):
        ns.append([k, t])
        ns.cell(row=ns.max_row, column=2).alignment = Alignment(wrap_text=True, vertical="top")
        ns.cell(row=ns.max_row, column=1).alignment = Alignment(vertical="top")
    ns.column_dimensions["A"].width = 5
    ns.column_dimensions["B"].width = 110
    wb.save(path)


def write_estate(path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Suites"
    ws.append(["suite", "address", "opened", "cells", "cells_for_children", "interview_rooms", "medical_rooms",
               "constant_watch_cells", "vehicle_bays", "status"])
    for r in [("Northgate", "Northgate Police Station, 41 Prospect Row, Calderwick CK3 2QL", 1998, 32, 2, 6, 2, 4, 3, "Open"),
              ("Eastmoor", "Eastmoor Police Station, Ladysmith Road, Calderwick CK7 1BW", 2004, 18, 1, 4, 1, 2, 2, "Open"),
              ("Southfields", "Southfields Custody Centre, Carvell Road, South Carvell CL12 8NE", 2011, 40, 2, 8, 2, 4, 4, "Open"),
              ("Wendle Cross", "Force Headquarters, Wendle Cross, Wendlebury WY4 6PD", 2009, 36, 2, 7, 2, 4, 3, "Open"),
              ("Tanner Street", "Tanner Street, Calderwick CK1 4TS", 2027, None, 2, 10, 3, 6, 4, "Fit-out from January 2027")]:
        ws.append(list(r))
    for c in ws[1]:
        c.font = Font(bold=True)
    for col, wdt in zip("ABCDEFGHIJ", (14, 58, 8, 7, 18, 15, 13, 20, 13, 26)):
        ws.column_dimensions[col].width = wdt
    ws.freeze_panes = "A2"
    wb.save(path)


# ------------------------------------------------------------------------------------------------------------------
# Background files
def population_rows(W, rng, wcode):
    rows = []
    for w in WD.WARDS:
        if w in WD.HUB:
            tot = int(rng.integers(9800, 14200))
            sh = (0.11, 0.74, 0.15)
        elif w in WD.CITY:
            tot = int(rng.integers(11500, 16500))
            sh = (0.19, 0.64, 0.17)
        else:
            tot = int(rng.integers(5200, 9800))
            sh = (0.17, 0.59, 0.24)
        a = int(round(tot * (sh[0] + rng.normal(0, 0.01))))
        c = int(round(tot * (sh[2] + rng.normal(0, 0.015))))
        b = tot - a - c
        rows.append([wcode[w], w, WD.DISTRICT[w], tot, a, b, c])
    return rows


LIC_NAMES = ["The Old Bell", "Canal House", "Mill Bank Social", "The Tannery", "Velvet", "Arches", "The Cooper's Arms",
             "Kingsway Rooms", "Halo", "The Corn Exchange", "Basin Bar", "The Lamplighter", "Ritz Lounge", "Sanctuary",
             "The Abbey Tap", "Quayside", "Electric Mill", "The Jolly Sailor", "Copper Still", "Neon Lane", "The Granary",
             "Cathedral Vaults", "The Fleece", "Castle Hotel", "The Wharf", "Ballroom 23", "Glasshouse", "The Feathers",
             "Number Nine", "Bank Street Club"]


def licence_rows(rng, wcode):
    rows = []
    wards = (["Mill Bank"] * 9 + ["Abbey Fields"] * 6 + ["Castle"] * 4 + ["Cathedral"] * 3 + ["Kingsway"] * 5 +
             ["St Peter's"] * 3 + ["Northgate"] * 2 + ["Eastmoor"] * 2 + ["Highfield"] + ["Parkway"])
    for k, w in enumerate(wards):
        name = LIC_NAMES[k % len(LIC_NAMES)] + ("" if k < len(LIC_NAMES) else " (Upstairs)")
        latest_wk = ["00:30", "01:00", "01:30", "02:00"][int(rng.integers(0, 4))]
        latest_we = ["02:00", "02:30", "03:00", "04:00"][int(rng.integers(0, 4))]
        status = "Current"
        if w == "Kingsway" and k % 2 == 0:
            status = "Surrendered %s" % ["03/2023", "11/2023", "06/2024"][k % 3]
        granted = "%02d/%02d/%d" % (int(rng.integers(1, 28)), int(rng.integers(1, 13)),
                                    int(rng.integers(2023, 2025)) if w == "Mill Bank" and k % 3 else int(rng.integers(2006, 2020)))
        rows.append(["HDL/PREM/%04d" % (210 + 7 * k), name, w, wcode[w], latest_wk, latest_we,
                     int(rng.integers(8, 70)) * 10, granted, status])
    return rows


def bank_holidays():
    ev = [("New Year’s Day", "2025-01-01"), ("Good Friday", "2025-04-18"), ("Easter Monday", "2025-04-21"),
          ("Early May bank holiday", "2025-05-05"), ("Spring bank holiday", "2025-05-26"),
          ("Summer bank holiday", "2025-08-25"), ("Christmas Day", "2025-12-25"), ("Boxing Day", "2025-12-26"),
          ("New Year’s Day", "2026-01-01"), ("Good Friday", "2026-04-03"), ("Easter Monday", "2026-04-06"),
          ("Early May bank holiday", "2026-05-04"), ("Spring bank holiday", "2026-05-25"),
          ("Summer bank holiday", "2026-08-31"), ("Christmas Day", "2026-12-25"), ("Boxing Day", "2026-12-28")]
    events = [{"title": t, "date": d, "notes": "Substitute day" if t == "Boxing Day" and d == "2026-12-28" else "",
               "bunting": t not in ("Good Friday",)} for t, d in ev]
    return json.dumps({"england-and-wales": {"division": "england-and-wales", "events": events}}, ensure_ascii=False,
                      separators=(",", ":"))
