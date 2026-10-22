"""The pack's documents: the statistics office's index methodology note, the Department's circular on rapid price
growth areas, the census dwelling stock and registered rents workbooks, the data dictionary and the extract manifest."""
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

import pack as P      # noqa: E402
import world as W     # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("LiberationSerif", "Regular"), ("LiberationSerif-Bold", "Bold"), ("LiberationSans", "Regular"),
              ("LiberationSans-Bold", "Bold")):
    try:
        pdfmetrics.getFont(nm)
    except KeyError:
        pdfmetrics.registerFont(TTFont(nm, FONT_DIR + nm.split("-")[0] + "-" + f + ".ttf"))
INK = colors.HexColor("#1b2430")
GREY = colors.HexColor("#5b6470")
GREEN = colors.HexColor("#2c5a3f")
BODY = ParagraphStyle("body", fontName="LiberationSerif", fontSize=10.3, leading=13.8, textColor=INK, spaceAfter=6)
SMALL = ParagraphStyle("small", fontName="LiberationSerif", fontSize=8.6, leading=11.2, textColor=GREY, spaceAfter=4)
CELL = ParagraphStyle("cell", fontName="LiberationSans", fontSize=8.4, leading=10.6, textColor=INK)
CELLB = ParagraphStyle("cellb", fontName="LiberationSans-Bold", fontSize=8.4, leading=10.6, textColor=INK)
H2 = ParagraphStyle("h2", fontName="LiberationSans-Bold", fontSize=10.6, leading=14, textColor=INK, spaceBefore=8,
                    spaceAfter=4)

METHOD = [
    ("1. What the index measures", [
        "The residential property price index for a local authority area measures the change in the market value of "
        "the area's dwelling stock, the dwellings the 2022 census counts there, from the prices of one year to those "
        "of the next. The annual change published each October compares the year to September with the year to "
        "September before it, each year taken as a whole. The index is compiled to the Handbook on Residential "
        "Property Prices Indices (Eurostat, 2013).",
        "It is compiled from the residential property price register, the valuation register's record of each "
        "dwelling and the address point file."]),
    ("2. Which sales count", [
        "A sale counts in the year in which it took place, the date of sale on the register, whatever the day it was "
        "filed. Only sales of a dwelling at full market price count; transfers between family members, sales of a "
        "part interest and other sales filed as not at full market price are outside the index. The price of a new "
        "dwelling includes VAT."]),
    ("3. The register's two systems", [
        "The price register moved to a new filing system in October 2025. The old system took filings to 10 October "
        "2025 and the new system took filings from 1 October 2025; filings made in both in the first ten days of "
        "October appear in both extracts. The old system's public layout records the price of a new dwelling "
        "exclusive of VAT, at 13.5 per cent, and identifies a dwelling by its address and eircode; the new system "
        "records the consideration including VAT and carries the valuation register's property number."]),
    ("4. Areas", [
        "The sixteen local authority areas are those of the Local Government Act 2019, and a dwelling's area is the "
        "one the valuation register records."]),
]
CIRCULAR = [
    ("1. Designation", [
        "The Minister will designate as rapid price growth areas for 2027 the local authority areas whose residential "
        "property price index, as the Brannagh Statistics Office measures it, rose by more than 8 per cent in the year "
        "to September 2026 on the year to September 2025. A designated area receives the accelerated planning and "
        "infrastructure measures of Part 3 of the Housing Supply Act 2025 for the calendar year 2027 and an allocation "
        "from the Act's 2027 infrastructure fund."]),
    ("2. Transactions", [
        "With the designation the Department records each area's residential transactions in the year to September "
        "2026: the number of dwellings sold and the total paid for them, including VAT, every residential sale "
        "counting whether or not it was at full market price."]),
    ("3. Timing", [
        "The Office is asked to provide the figures by 6 November 2026 so that the designated areas' allocations can "
        "be settled before the fund's 2027 allocation round closes on 20 November."]),
]


def _frame(foot):
    def frame(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(GREY)
        canvas.setFont("LiberationSans", 7.2)
        canvas.drawString(0.85 * inch, 0.55 * inch, foot)
        canvas.drawRightString(letter[0] - 0.85 * inch, 0.55 * inch, "Page %d" % doc.page)
        canvas.restoreState()
    return frame


def _masthead(org, title):
    return [Paragraph(org.upper(), ParagraphStyle("o", fontName="LiberationSans-Bold", fontSize=8.4, textColor=GREEN,
                                                  leading=11)),
            Paragraph(title, ParagraphStyle("t", fontName="LiberationSans-Bold", fontSize=14, leading=18,
                                            textColor=INK, spaceAfter=6))]


def _doc(path, org, title, author, head, sections, foot):
    d = SimpleDocTemplate(path, pagesize=letter, leftMargin=0.85 * inch, rightMargin=0.85 * inch, topMargin=0.8 * inch,
                          bottomMargin=0.9 * inch, title=title, author=author, subject="", creator="", producer="")
    t = Table([[Paragraph(a, CELLB), Paragraph(b, CELL)] for a, b in head], colWidths=[0.9 * inch, 5.6 * inch],
              hAlign="LEFT")
    t.setStyle(TableStyle([("LINEBELOW", (0, -1), (-1, -1), 0.6, INK), ("LEFTPADDING", (0, 0), (-1, -1), 0),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]))
    story = _masthead(org, title) + [t, Spacer(1, 8)]
    for h, paras in sections:
        story.append(Paragraph(h, H2))
        for p in paras:
            story.append(Paragraph(p, BODY))
    d.build(story, onFirstPage=_frame(foot), onLaterPages=_frame(foot))


def write_method(path):
    _doc(path, P.COMPANY, "Residential property price index: methodology note", "Clare McEntee",
         [["Series", "Residential property price index by local authority area"], ["Issued by", "Prices Division"],
          ["Date", "2 March 2026"], ["Contact", "Clare McEntee, Head of Price Statistics"]],
         METHOD, "%s. Methodology note RPPI/2026/1, 2 March 2026." % P.COMPANY)


def write_circular(path):
    _doc(path, "Department of Housing, Local Government and Heritage", "Rapid price growth areas, 2027",
         "Evelyn Clune",
         [["To", "Brannagh Statistics Office, Prices Division"], ["From", "Evelyn Clune, Housing Supply Policy"],
          ["Date", "12 October 2026"], ["Reference", "Circular HSP 07/2026"]],
         CIRCULAR, "Department of Housing, Local Government and Heritage. Circular HSP 07/2026, 12 October 2026.")


def _sheet(ws, title, note, header, rows, widths):
    from openpyxl.styles import Font, PatternFill
    ws["A1"] = title
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = note
    ws.append([])
    ws.append(header)
    for c in ws[4]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor="2C5A3F")
    for r in rows:
        ws.append(r)
    for i, w in enumerate(widths):
        ws.column_dimensions["ABCDEFGH"[i]].width = w
    ws.freeze_panes = "A5"


def write_census(path, x):
    import openpyxl
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Dwellings by type"
    st = P.stock(x)
    rows = [[a["code"], a["name"]] + st[a["code"]] + [sum(st[a["code"]])] for a in x["areas"]]
    _sheet(ws, "Census 2022: permanent private dwellings by local authority area and type",
           "Occupied and vacant dwellings on census night, 3 April 2022. Counts rounded to the nearest ten.",
           ["LA code", "Local authority area", "Detached house", "Semi-detached house", "Terraced house", "Apartment",
            "All dwellings"], rows, (9, 22, 15, 20, 15, 12, 14))
    for r in ws.iter_rows(min_row=5, min_col=3, max_col=7):
        for c in r:
            c.number_format = "#,##0"
    wb.save(path)


def write_rents(path, x):
    import openpyxl
    rng = np.random.default_rng(W.SEED + 8)
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Rents 2026 Q2"
    rows = []
    for a in x["areas"]:
        base = float(np.exp(a["level"])) * 0.0046
        rows.append([a["code"], a["name"], int(rng.integers(300, 1600)), round(base * float(rng.uniform(0.9, 1.1))),
                     round(float(rng.uniform(2.0, 9.5)), 1)])
    _sheet(ws, "Registered tenancies: standardised average monthly rent by area, second quarter 2026",
           "New tenancies registered April to June 2026; rents in euro a month; change on the second quarter of 2025.",
           ["LA code", "Local authority area", "New tenancies", "Average rent (EUR a month)", "Annual change (%)"],
           rows, (9, 22, 14, 24, 17))
    wb.save(path)


DICT_COLS = ["file_name", "field", "description"]


def dictionary_rows():
    f = P.FILES
    return [
        (f["ppr_old"], "Date of Sale (dd/mm/yyyy)", "the date of sale, day first"),
        (f["ppr_old"], "Price (\u20ac)", "the price filed, in euro; for a new dwelling exclusive of VAT"),
        (f["ppr_old"], "Not Full Market Price", "Yes where the sale was filed as not at full market price"),
        (f["ppr_old"], "VAT Exclusive", "Yes where the price excludes VAT"),
        (f["ppr_old"], "Eircode", "the dwelling's eircode as keyed at filing; blank where none was given"),
        (f["ppr_new"], "consideration_eur", "the consideration filed, in euro, including VAT"),
        (f["ppr_new"], "market_basis", "FMP at full market price, NFMP not at full market price"),
        (f["ppr_new"], "dwelling_status", "NEW a new dwelling, SH second-hand"),
        (f["ppr_new"], "property_number", "the valuation register's property number"),
        (f["valuation"], "floor_area_m2", "internal floor area in square metres, as valued"),
        (f["valuation"], "valuation_date", "the date of the valuation the record holds"),
        (f["points"], "ed_code", "the electoral division the building stands in"),
        (f["points"], "building_id", "the building the address point stands in"),
        (f["census"], "All dwellings", "permanent private dwellings, occupied and vacant"),
        (f["mortgages"], "value_eur_m", "value of mortgage drawdowns, euro million"),
    ]


MANIFEST_COLS = ["file_name", "contents", "provided_by", "as_of_date", "coverage", "record_count"]


def manifest_rows(n):
    f = P.FILES
    return [
        (f["ppr_old"], "residential property price register, old system public layout", "Property Services Register",
         "2025-10-10", "filed 1 October 2024 to 10 October 2025", n["ppr_old"]),
        (f["ppr_new"], "residential property price register, new system", "Property Services Register", "2026-10-15",
         "filed 1 October 2025 to 14 October 2026", n["ppr_new"]),
        (f["valuation"], "valuation register, dwellings", "Valuation Office", "2026-10-15",
         "dwellings on the price register extracts", n["valuation"]),
        (f["points"], "address points", "national address database", "2026-10-15",
         "buildings of the dwellings on the price register extracts", n["points"]),
        (f["eds"], "electoral divisions", P.COMPANY, "2026-01-05", "2026", n["eds"]),
        (f["census"], "census dwelling stock", P.COMPANY, "2023-06-29", "census night 2022", 16),
        (f["method"], "index methodology note", P.COMPANY, "2026-03-02", "", ""),
        (f["circular"], "circular on rapid price growth areas", "Department of Housing, Local Government and Heritage",
         "2026-10-12", "", ""),
        (f["rents"], "registered rents", "Residential Tenancies Authority", "2026-08-14", "April to June 2026", 16),
        (f["mortgages"], "mortgage drawdowns", "lenders' federation", "2026-08-20", "2025 Q1 to 2026 Q2",
         n["mortgages"]),
        (f["dictionary"], "field descriptions", P.COMPANY, "2026-10-15", "", n["dictionary"]),
    ]
