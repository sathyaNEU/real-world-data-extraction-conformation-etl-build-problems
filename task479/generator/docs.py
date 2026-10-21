"""The pack's documents: the Department of Revenue's seven annual county reports (two layouts), the Lodging Monitor's
methods note, the Rising Destinations 2027 program terms, the data dictionary and the extract manifest."""
import datetime as dt

import numpy as np
from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                      # noqa: E402
from reportlab.lib.pagesizes import letter                                            # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                       # noqa: E402
from reportlab.lib.units import inch                                                  # noqa: E402
from reportlab.pdfbase import pdfmetrics                                              # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                          # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

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
BODY = ParagraphStyle("body", fontName="LiberationSerif", fontSize=10.3, leading=13.8, textColor=INK, spaceAfter=6)
SMALL = ParagraphStyle("small", fontName="LiberationSerif", fontSize=8.6, leading=11.2, textColor=GREY, spaceAfter=4)
CELL = ParagraphStyle("cell", fontName="LiberationSans", fontSize=8.0, leading=10.0, textColor=INK)
CELLR = ParagraphStyle("cellr", parent=CELL, alignment=2)
CELLB = ParagraphStyle("cellb", fontName="LiberationSans-Bold", fontSize=8.0, leading=10.0, textColor=INK)
CELLBR = ParagraphStyle("cellbr", parent=CELLB, alignment=2)
H2 = ParagraphStyle("h2", fontName="LiberationSans-Bold", fontSize=10.6, leading=14, textColor=INK, spaceBefore=8,
                    spaceAfter=4)
DOR = "Tarrowind Department of Revenue"
DOR_BLUE = colors.HexColor("#22465f")
TLA_GREEN = colors.HexColor("#2f5d4e")


def _doc(path, title, author, footer):
    def frame(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(GREY)
        canvas.setFont("LiberationSans", 7.2)
        canvas.drawString(0.85 * inch, 0.55 * inch, footer)
        canvas.drawRightString(letter[0] - 0.85 * inch, 0.55 * inch, "Page %d" % doc.page)
        canvas.restoreState()
    d = SimpleDocTemplate(path, pagesize=letter, leftMargin=0.85 * inch, rightMargin=0.85 * inch, topMargin=0.8 * inch,
                          bottomMargin=0.9 * inch, title=title, author=author, subject="", creator="", producer="")
    return d, frame


def _table(rows, widths, right=(), total=False):
    data = []
    for i, r in enumerate(rows):
        bold = i == 0 or (total and i == len(rows) - 1)
        data.append([Paragraph(str(v), (CELLBR if k in right else CELLB) if bold else (CELLR if k in right else CELL))
                     for k, v in enumerate(r)])
    t = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    st = [("LINEBELOW", (0, 0), (-1, 0), 0.6, INK), ("VALIGN", (0, 0), (-1, -1), "TOP"),
          ("LEFTPADDING", (0, 0), (-1, -1), 3), ("RIGHTPADDING", (0, 0), (-1, -1), 3),
          ("TOPPADDING", (0, 0), (-1, -1), 1.6), ("BOTTOMPADDING", (0, 0), (-1, -1), 1.6)]
    if total:
        st.append(("LINEABOVE", (0, -1), (-1, -1), 0.5, INK))
    t.setStyle(TableStyle(st))
    return t


def fmt(n):
    return "{:,}".format(int(n))


# --------------------------------------------------------------------------------- the Department's annual reports
def dor_table(x, y):
    """Each county's first print for tax year y and the revised prior year, as the report prints them."""
    rng = np.random.default_rng(W.SEED + 100 + y)
    rows = []
    for name in W.NAMES:
        cur = x["first"][(name, y)]
        if y == 2018:
            prev = int(round(cur / float(rng.uniform(1.015, 1.058))))
        else:
            prev = x["revised"][(name, y - 1)]
        n_props = sum(1 for p in x["props"] if p["county"] == name)
        returns = int(round(n_props * x["ratio"][(name, y)] * float(rng.uniform(1.6, 2.1)) * (1 + 0.05 * (y - 2018))))
        rate = (6.0 + P.rate_on(name, y)) / 100
        rows.append((name, cur, prev, returns, int(round(cur * rate * float(rng.uniform(0.996, 1.0))))))
    return rows


def write_dor(path, x, y):
    iy, im, iday = P.DOR_ISSUED[y]
    issued = dt.date(iy, im, iday)
    d, frame = _doc(path, "Taxable Lodging Receipts by County, Tax Year %d" % y, DOR,
                    "%s, Office of Tax Research. Lodging Tax Series LT-%d. Issued %s." % (
                        DOR, y, issued.strftime("%B %-d, %Y")))
    story = [Paragraph(DOR.upper(), ParagraphStyle("o", fontName="LiberationSans-Bold", fontSize=8.4, textColor=DOR_BLUE,
                                                   leading=11)),
             Paragraph("Office of Tax Research", SMALL),
             Paragraph("Taxable Lodging Receipts by County, Tax Year %d" % y,
                       ParagraphStyle("t", fontName="LiberationSans-Bold", fontSize=14, leading=18, textColor=INK,
                                      spaceAfter=8))]
    rows = dor_table(x, y)
    tot = [sum(r[i] for r in rows) for i in (1, 2, 3, 4)]
    if y <= 2020:
        story.append(Paragraph(
            "Taxable lodging receipts are the gross receipts from the rental of rooms and other accommodations for "
            "periods of fewer than thirty days, as reported on lodging tax returns for tax periods in calendar %d "
            "and processed through %s. Receipts for %d are revised for amended returns processed since the "
            "Tax Year %d report. Amounts are in thousands of dollars." % (
                y, dt.date(iy, 9, 30).strftime("%B %-d, %Y"), y - 1, y - 1), BODY))
        head = ["County", "Tax Year %d" % y, "Tax Year %d (revised)" % (y - 1), "Change"]
        body = [head]
        for nm, cur, prev, ret, tax in rows:
            body.append([nm, fmt(round(cur / 1000)), fmt(round(prev / 1000)), "%.1f%%" % (100 * (cur / prev - 1))])
        body.append(["State total", fmt(round(tot[0] / 1000)), fmt(round(tot[1] / 1000)),
                     "%.1f%%" % (100 * (tot[0] / tot[1] - 1))])
        story.append(_table(body, [2.0 * inch, 1.45 * inch, 1.75 * inch, 0.9 * inch], right=(1, 2, 3), total=True))
    else:
        story.append(Paragraph(
            "Taxable lodging receipts are the gross receipts from the rental of rooms and other accommodations for "
            "periods of fewer than thirty days, as reported on lodging tax returns for tax periods in calendar %d "
            "and processed through %s. Receipts for %d are revised for amended returns processed since the Tax Year %d report. "
            "Amounts are in dollars; tax due is the state and county lodging tax on the receipts." % (
                y, dt.date(iy, 9, 30).strftime("%B %-d, %Y"), y - 1, y - 1), BODY))
        body = [["Code", "County", "Returns", "Taxable receipts, TY %d" % y, "TY %d, revised" % (y - 1),
                 "Change", "Tax due, TY %d" % y]]
        for nm, cur, prev, ret, tax in sorted(rows, key=lambda r: W.CODE[r[0]]):
            body.append([W.CODE[nm], nm, fmt(ret), fmt(cur), fmt(prev), "%.1f%%" % (100 * (cur / prev - 1)), fmt(tax)])
        body.append(["", "State", fmt(tot[2]), fmt(tot[0]), fmt(tot[1]), "%.1f%%" % (100 * (tot[0] / tot[1] - 1)),
                     fmt(tot[3])])
        story.append(_table(body, [0.45 * inch, 1.2 * inch, 0.65 * inch, 1.35 * inch, 1.25 * inch, 0.6 * inch,
                                   1.15 * inch], right=(2, 3, 4, 5, 6), total=True))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "Receipts are assigned to the county in which the accommodation is located. Figures for the most recent tax "
        "year are revised in the following year's report; earlier years are not revised again.", SMALL))
    d.build(story, onFirstPage=frame, onLaterPages=frame)


# ------------------------------------------------------------------------------------------ the Monitor's methods
METHODS = [
    ("1. The Lodging Monitor", [
        "The Lodging Monitor is the Association's monthly report of hotel and lodging performance in the state's "
        "sixteen counties. Each month the member properties in the Monitor panel report their rooms available, rooms "
        "sold and room revenue for the month before, and the Association publishes occupancy, average daily rate and "
        "revenue per available room for each county in the members' bulletin.",
    ]),
    ("2. The panel", [
        "The panel was drawn in January 2018 from the member properties then reporting each month. A property in the "
        "panel reports every month while it is open; a property that closes leaves the panel. A property that "
        "changes its name, brand or management company stays in the panel under the same property record.",
    ]),
    ("3. Reporting", [
        "Reports are due by the twentieth day of the following month and late reports are accepted. A property may "
        "resubmit a month's report to correct it; the later submission replaces the earlier one for that month.",
        "Until March 2022 reports were filed through the Association's own reporting system, which stamped each "
        "report with the local date and time it was received. From April 2022 reports are filed through the "
        "InnSight portal, which gave every property a new property id, records room revenue in cents and stamps each "
        "submission in Coordinated Universal Time. InnSight's migration team supplied the crosswalk from the legacy "
        "property ids to the InnSight ids when the portal went live.",
    ]),
    ("4. Definitions", [
        "Rooms available are the room-nights a property had available to sell in the month; rooms out of order for "
        "the whole month are not available. Rooms sold are the room-nights sold, complimentary rooms excluded. Room "
        "revenue is the revenue from rooms sold, before taxes and excluding fees and other departments.",
        "Occupancy is rooms sold over rooms available. Average daily rate is room revenue over rooms sold. Revenue "
        "per available room is room revenue over rooms available. A county's figures for a period are computed "
        "from the totals of its properties' reports for the months of the period, not averaged across properties "
        "or months.",
    ]),
]


def write_method(path):
    d, frame = _doc(path, "Lodging Monitor: methods", P.COMPANY,
                    "%s, Research. Lodging Monitor methods, revised February 2026." % P.COMPANY)
    story = [Paragraph(P.COMPANY.upper(), ParagraphStyle("o", fontName="LiberationSans-Bold", fontSize=8.4,
                                                         textColor=TLA_GREEN, leading=11)),
             Paragraph("Lodging Monitor: methods", ParagraphStyle("t", fontName="LiberationSans-Bold", fontSize=14,
                                                                  leading=18, textColor=INK, spaceAfter=3)),
             Paragraph("Research, revised February 2026", SMALL), Spacer(1, 6)]
    for h, paras in METHODS:
        story.append(Paragraph(h, H2))
        for t in paras:
            story.append(Paragraph(t, BODY))
    d.build(story, onFirstPage=frame, onLaterPages=frame)


# ------------------------------------------------------------------------------------------- the program terms
PROGRAM = [
    ("1. Purpose", [
        "Rising Destinations matches the summer 2027 co-op marketing campaigns of the county tourism bureaus in the "
        "counties where lodging is growing fastest, so the Association's marketing dollars follow the demand its "
        "members are building."]),
    ("2. Qualification", [
        "A county qualifies when its taxable lodging receipts for tax year 2025, as the Tarrowind Department of "
        "Revenue first publishes them in its Tax Year 2025 report, are at least 6 per cent above its taxable "
        "lodging receipts for tax year 2024 as published in the Tax Year 2024 report."]),
    ("3. Timing", [
        "The Department publishes its Tax Year 2025 report in December 2026, after the county bureaus' co-op "
        "budgets for summer 2027 close on 30 November 2026. The Board therefore designates the qualifying counties "
        "at its meeting of 27 October 2026 on the Director of Research's estimate of each county's tax year 2025 "
        "receipts on the Department's basis. A designation stands when the report is published."]),
    ("4. The match", [
        "The Rising Destinations fund of $1,800,000 is divided equally among the qualifying counties. Each county's "
        "share is paid to its tourism bureau against an equal amount the bureau commits to its summer 2027 co-op "
        "campaign."]),
    ("5. With the designation", [
        "The Director of Research brings the Board each county's Lodging Monitor occupancy and average daily rate "
        "for January to August 2026, and the standing of the Monitor panel in each county against the panel as it "
        "was drawn in January 2018."]),
]


def write_program(path):
    import docx
    from docx.shared import Pt, RGBColor
    doc = docx.Document()
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    p = doc.add_paragraph()
    r = p.add_run(P.COMPANY.upper())
    r.bold = True
    r.font.size = Pt(8.5)
    r.font.color.rgb = RGBColor(0x2f, 0x5d, 0x4e)
    p = doc.add_paragraph()
    r = p.add_run("Rising Destinations 2027: program terms")
    r.bold = True
    r.font.size = Pt(15)
    doc.add_paragraph("Adopted by the Board of Directors on 16 September 2026 (resolution 2026-31).")
    for h, paras in PROGRAM:
        q = doc.add_paragraph()
        rr = q.add_run(h)
        rr.bold = True
        for t in paras:
            doc.add_paragraph(t)
    doc.add_paragraph("Debbie Brady, Chair of the Board\nSamantha Walter, Director of Research")
    doc.core_properties.author = "Samantha Walter"
    doc.core_properties.last_modified_by = "Samantha Walter"
    doc.core_properties.created = dt.datetime(2026, 9, 16, 15, 2)
    doc.core_properties.modified = dt.datetime(2026, 9, 17, 9, 41)
    doc.core_properties.title = "Rising Destinations 2027: program terms"
    doc.core_properties.comments = ""
    doc.core_properties.keywords = ""
    doc.core_properties.subject = ""
    doc.core_properties.revision = 3
    doc.save(path)


# ----------------------------------------------------------------------------------- dictionary and manifest
DICT_COLS = ["file_name", "field", "description"]


def dictionary_rows():
    f = P.FILES
    d = [
        (f["legacy"], "Property ID", "the property's id in the Association's legacy reporting system"),
        (f["legacy"], "Property Name", "the property's name when the report was received"),
        (f["legacy"], "County", "the county the property is in"),
        (f["legacy"], "Report Month", "the month the report covers, MM/YYYY"),
        (f["legacy"], "Rooms Available", "room-nights available to sell in the month"),
        (f["legacy"], "Rooms Sold", "room-nights sold in the month, complimentary rooms excluded"),
        (f["legacy"], "Room Revenue", "revenue from rooms sold in the month, dollars, before taxes and excluding fees"),
        (f["legacy"], "Received", "local date and time the report was received, MM/DD/YYYY HH:MM"),
        (f["current"], "submission_id", "InnSight's id for the submission"),
        (f["current"], "prop_id", "the property's InnSight id"),
        (f["current"], "period", "the month the report covers, YYYY-MM"),
        (f["current"], "county_code", "the Department of Revenue's code for the county the property is in"),
        (f["current"], "avail_room_nights", "room-nights available to sell in the month"),
        (f["current"], "sold_room_nights", "room-nights sold in the month, complimentary rooms excluded"),
        (f["current"], "room_revenue_cents", "revenue from rooms sold in the month, in cents, before taxes and "
                                             "excluding fees"),
        (f["current"], "submitted_at_utc", "when the submission was made, UTC"),
        (f["register"], "prop_id", "the property's InnSight id"),
        (f["register"], "property_name", "the property's name today"),
        (f["register"], "street", "street address"),
        (f["register"], "city", "city or town"),
        (f["register"], "county", "the county the property is in"),
        (f["register"], "rooms", "rooms in the property today"),
        (f["register"], "management_company", "the company managing the property today, blank if owner-operated"),
        (f["register"], "panel_status", "reporting, or closed (the property has closed and left the panel)"),
        (f["xwalk"], "legacy_property_id", "the property's id in the legacy reporting system"),
        (f["xwalk"], "innsight_prop_id", "the property's InnSight id"),
        (f["xwalk"], "property_name_at_mapping", "the property's name in the legacy system when it was mapped"),
        (f["xwalk"], "mapped_on", "the date the mapping was made"),
        (f["rates"], "state_rate_pct", "state lodging tax rate, per cent of taxable receipts"),
        (f["rates"], "county_rate_pct", "county lodging tax rate, per cent of taxable receipts"),
        (f["rates"], "effective_from", "first day the rates apply"),
        (f["rates"], "effective_to", "last day the rates apply, blank if current"),
        (f["visitor"], "visitor_spending_usd_millions", "estimated spending by visitors in the county, all categories, "
                                                        "millions of dollars"),
        (f["visitor"], "lodging_share_pct", "the share of visitor spending on lodging, per cent"),
        (f["visitor"], "day_trip_share_pct", "the share of visitor spending by day visitors, per cent"),
        (f["visitor"], "estimate_status", "final, or preliminary (to be revised in the next release)"),
    ]
    return d


MANIFEST_COLS = ["file_name", "contents", "provided_by", "as_of_date", "coverage", "record_count"]


def manifest_rows(n):
    f = P.FILES
    rows = [
        (f["legacy"], "Lodging Monitor reports from the legacy reporting system", "TLA Research", "2022-04-04",
         "2018-01 to 2022-03", n["legacy"]),
        (f["current"], "Lodging Monitor reports from InnSight", "InnSight (export)", "2026-10-02",
         "2022-04 to 2026-09", n["current"]),
        (f["register"], "Lodging Monitor panel property register", "InnSight (export)", "2026-10-02",
         "properties migrated April 2022", n["register"]),
        (f["xwalk"], "legacy to InnSight property id crosswalk", "InnSight migration team", "2022-04-01",
         "properties migrated April 2022", n["xwalk"]),
    ]
    for y in W.BENCH:
        iy, im, iday = P.DOR_ISSUED[y]
        rows.append((f["dor%d" % y], "Taxable Lodging Receipts by County, Tax Year %d" % y, DOR,
                     "%d-%02d-%02d" % (iy, im, iday), "tax year %d and %d revised" % (y, y - 1), 16))
    rows += [
        (f["rates"], "state and county lodging tax rates", DOR, "2026-07-01", "2018-01-01 to date", n["rates"]),
        (f["visitor"], "visitor spending estimates by county", "Tarrowind Tourism Bureau", "2025-11-18",
         "2019 to 2024", n["visitor"]),
        (f["method"], "Lodging Monitor methods", "TLA Research", "2026-02-12", "", ""),
        (f["program"], "Rising Destinations 2027 program terms", "TLA Board of Directors", "2026-09-16", "", ""),
        (f["dictionary"], "field descriptions for the data files", "TLA Research", "2026-10-02", "", n["dictionary"]),
    ]
    return rows
