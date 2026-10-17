"""The pack's documents: the service's methods notes, Quillfield Re's term sheet, the cooperative's risk policy and
enrolment notice, the folder's data dictionary and its file register."""
from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                      # noqa: E402
from reportlab.lib.pagesizes import letter                                            # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                       # noqa: E402
from reportlab.lib.units import inch                                                  # noqa: E402
from reportlab.pdfbase import pdfmetrics                                              # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                          # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import pack as P    # noqa: E402
import world as W   # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("LiberationSerif", "Regular"), ("LiberationSerif-Bold", "Bold"), ("LiberationSans", "Regular"),
              ("LiberationSans-Bold", "Bold")):
    try:
        pdfmetrics.getFont(nm)
    except KeyError:
        pdfmetrics.registerFont(TTFont(nm, FONT_DIR + nm.split("-")[0] + "-" + f + ".ttf"))
INK = colors.HexColor("#1b1d1f")
GREY = colors.HexColor("#5b6067")
GREEN = colors.HexColor("#2f5d3a")
NAVY = colors.HexColor("#1f3a5f")
BODY = ParagraphStyle("body", fontName="LiberationSerif", fontSize=10.5, leading=14.2, textColor=INK, spaceAfter=6)
NUM = ParagraphStyle("num", parent=BODY, leftIndent=28, firstLineIndent=-28)
CELL = ParagraphStyle("cell", fontName="LiberationSans", fontSize=8.8, leading=11, textColor=INK)
CELLB = ParagraphStyle("cellb", parent=CELL, fontName="LiberationSans-Bold")
SMALL = ParagraphStyle("small", fontName="LiberationSans", fontSize=8.5, leading=11, textColor=GREY)


def styles(accent):
    h1 = ParagraphStyle("h1", fontName="LiberationSans-Bold", fontSize=14, leading=18, textColor=accent, spaceAfter=2)
    h1s = ParagraphStyle("h1s", fontName="LiberationSans", fontSize=9.3, leading=12.5, textColor=GREY, spaceAfter=10)
    h2 = ParagraphStyle("h2", fontName="LiberationSans-Bold", fontSize=10.5, leading=14, textColor=INK, spaceBefore=7,
                        spaceAfter=3)
    return h1, h1s, h2


def _doc(path, title, author, footer):
    def frame(canvas, doc):
        canvas.saveState()
        canvas.setFont("LiberationSans", 7.5)
        canvas.setFillColor(GREY)
        canvas.drawString(0.9 * inch, 0.6 * inch, footer)
        canvas.drawRightString(letter[0] - 0.9 * inch, 0.6 * inch, "Page %d" % doc.page)
        canvas.restoreState()
    d = SimpleDocTemplate(path, pagesize=letter, leftMargin=0.9 * inch, rightMargin=0.9 * inch, topMargin=0.8 * inch,
                          bottomMargin=0.9 * inch, title=title, author=author, subject="", creator="", producer="")
    return d, frame


def _table(rows, widths, head="#e6eef0"):
    data = [[Paragraph(str(c), CELLB if i == 0 else CELL) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9aa0a6")),
                           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(head)),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 4),
                           ("RIGHTPADDING", (0, 0), (-1, -1), 4)]))
    return t


# ---------------------------------------------------------------- the service's methods notes
def write_methods(path):
    H1, H1S, H2 = styles(GREEN)
    doc, frame = _doc(path, "County Estimates of Field Crops: Methods, Symbols and Revisions", W.SERVICE,
                      "%s  |  County estimates of field crops: methods, symbols and revisions  |  March 2026" % W.SERVICE)
    s = [Paragraph("County Estimates of Field Crops: Methods, Symbols and Revisions", H1),
         Paragraph("%s, State Department of Agriculture. Issued 26 March 2026 with the revised county estimates for "
                   "2017 to 2021." % W.SERVICE, H1S)]
    p = lambda n, t: s.append(Paragraph("<b>%s</b>&nbsp;&nbsp;%s" % (n, t), NUM))
    s.append(Paragraph("1. The programme", H2))
    p("1.1", "The service estimates planted acres, harvested acres, production and yield of the state's principal field "
             "crops for each county, each of the state's nine agricultural statistics districts and the state as a "
             "whole. Where a crop is grown both ways the estimates are made for irrigated and non-irrigated land as well "
             "as for all practices together. County estimates for a crop year are released in late February of the "
             "following year.")
    p("1.2", "The estimates rest on the service's county agricultural production survey of farm operators, checked "
             "against administrative acreage reports and, every five years, against the Census of Agriculture.")
    s.append(Paragraph("2. Estimation", H2))
    p("2.1", "Acres and production are estimated for each county and practice first. A district's estimates are the "
             "totals of all the county estimates in the district, and the state's the totals of its nine districts, "
             "whether or not a county estimate is published.")
    p("2.2", "Yield is production divided by harvested acres. Abandoned acres, planted but not harvested for grain, count "
             "in planted acres only.")
    p("2.3", "Acres are rounded to the nearest 10. Production of grain sorghum, wheat, corn and soybeans is in bushels "
             "rounded to the nearest 100, a bushel of grain sorghum being 56 pounds at 14 per cent moisture; sunflower "
             "production is in pounds to the nearest 1,000 and alfalfa hay in tons to the nearest 10. Yields are shown "
             "to one decimal (sunflower in whole pounds, hay in hundredths of a ton).")
    s.append(Paragraph("3. Publication standards and symbols", H2))
    p("3.1", "A county estimate for a crop and practice is published when it rests on five or more reports and its "
             "coefficient of variation is 30 per cent or less. An all-practices estimate is published when it meets the "
             "standard on its own. From the 2008 crop year the coefficient of variation of each published county yield "
             "is shown beside it.")
    s.append(_table([["Symbol", "Meaning"],
                     ["(S)", "Does not meet publication standards"],
                     ["(NA)", "Not available"],
                     ["(Z)", "Less than half of the unit shown"]], [1.0 * inch, 4.6 * inch]))
    s.append(Spacer(1, 4))
    s.append(Paragraph("4. Revisions", H2))
    p("4.1", "In March 2026 the county estimates for the 2017 to 2021 crop years were revised to agree with the 2022 "
             "Census of Agriculture, and the district and state estimates were revised with them. A revised estimate "
             "replaces the one published before it; downloads made before 26 March 2026 hold the earlier estimates.")
    p("4.2", "The 2025 county estimates, released on 24 February 2026, are preliminary. They will be reviewed with the "
             "2026 estimates in February 2027 and stand as the service's estimates until then.")
    s.append(Paragraph("5. Districts", H2))
    p("5.1", "The nine districts and the counties in each have not changed since 1991. Districts were coded 1 to 9 "
             "through the 2007 crop year and carry the codes 10 to 90 from 2008 (district 2, West Central, is 20; "
             "district 3, Southwest, is 30; and so on).")
    s.append(_table([["Code", "District", "Code", "District", "Code", "District"],
                     ["10", "Northwest", "40", "North Central", "70", "Northeast"],
                     ["20", "West Central", "50", "Central", "80", "East Central"],
                     ["30", "Southwest", "60", "South Central", "90", "Southeast"]],
                    [0.55 * inch, 1.2 * inch, 0.55 * inch, 1.2 * inch, 0.55 * inch, 1.2 * inch]))
    s.append(Paragraph("6. Downloads", H2))
    p("6.1", "The county estimates database export lists one estimate per row with its crop year, geography, data item "
             "and value. Values carry thousands separators; a withheld estimate shows its symbol in place of a value. "
             "The load time is the date the estimate entered the database.")
    s.append(Spacer(1, 8))
    s.append(Paragraph("Questions to the county estimates section of the service. This note replaces the edition of "
                       "February 2023.", SMALL))
    doc.build(s, onFirstPage=frame, onLaterPages=frame)


# ---------------------------------------------------------------- Quillfield Re's term sheet
def write_terms(path, ts):
    H1, H1S, H2 = styles(NAVY)
    doc, frame = _doc(path, "Area-Yield Drought Cover, 2027 Crop Year: Term Sheet", W.REINSURER,
                      "%s  |  Area-yield drought cover, 2027 crop year  |  Term sheet, 14 October 2026  |  Indicative "
                      "and subject to contract" % W.REINSURER)
    s = [Paragraph("Area-Yield Drought Cover, 2027 Crop Year", H1),
         Paragraph("Term sheet for %s. %s, agricultural reinsurance desk, 14 October 2026. Indicative and subject to "
                   "contract." % (W.ORG, W.REINSURER), H1S)]
    row = lambda k, v: [Paragraph("<b>%s</b>" % k, CELL), Paragraph(v, CELL)]
    terms = [
        ("Insured", "%s, on behalf of its members." % W.ORG),
        ("Covers", "One cover for each of Ardley, Corvin, Elster, Pallard and Tresham counties. Each cover is quoted and "
                   "may be bought on its own."),
        ("Crop year", "2027."),
        ("Index", "The county's non-irrigated grain sorghum yield for the 2027 crop year, in bushels per harvested "
                  "acre, as estimated by the State %s in its county estimates." % W.SERVICE),
        ("Expected yield", "The county's expected 2027 yield in the table below."),
        ("Trigger", "90 per cent of the expected yield."),
        ("Payment", "When the index is below the trigger, the liability times the trigger less the index, divided by "
                    "the trigger; never more than the liability."),
        ("Liability", "The non-irrigated grain sorghum acres the cooperative's members enrol in the county, times the "
                      "expected yield, times 90 per cent, times the projected price of $%.2f per hundredweight (a "
                      "bushel of grain sorghum weighs %d pounds)." % (W.PRICE_CWT, W.BUSHEL_LB)),
        ("Premium", "The quoted rate in the quote schedule of this date times the liability, due 15 March 2027."),
        ("Rating basis", "Quillfield Re rates each cover on the county's yields for the crop years 1991 to 2025, each "
                         "brought to the 2027 level by adding the county's trend in the table below for each year from "
                         "that crop year to 2027."),
        ("Settlement", "On the service's county estimates for 2027, expected in February 2028; payment within 30 days."),
        ("Acres", "As enrolled by members through the cooperative before its enrolment close; the cooperative certifies "
                  "them to Quillfield Re by 30 November 2026."),
    ]
    t = Table([row(k, v) for k, v in terms], colWidths=[1.25 * inch, 5.45 * inch], hAlign="LEFT")
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, -1), 0.3, colors.HexColor("#c7ccd1")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 3)]))
    s.append(t)
    s.append(Paragraph("Expected yields and trends", H2))
    s.append(_table([["County", "Expected 2027 yield (bu per harvested acre)", "Trend (bu per acre per year)"]] +
                    [[c, "%.1f" % ts[c]["expected"], "%.2f" % ts[c]["trend"]] for c in W.MEMBERS],
                    [1.4 * inch, 2.6 * inch, 2.2 * inch], head="#e3e8f1"))
    s.append(Spacer(1, 4))
    s.append(Paragraph("Expected yields and trends are Quillfield Re's own.", SMALL))
    s.append(Paragraph("Conditions", H2))
    s.append(Paragraph("Covers are written by Quillfield Re as reinsurer of the cooperative's captive cell. Quotes hold to "
                       "30 November 2026. Final terms follow the cooperative's written order.", BODY))
    doc.build(s, onFirstPage=frame, onLaterPages=frame)


# ---------------------------------------------------------------- the cooperative's risk policy
def write_policy(path):
    H1, H1S, H2 = styles(GREEN)
    doc, frame = _doc(path, "Risk Management Policy", W.ORG, "%s  |  Risk management policy  |  Approved 21 January "
                      "2026" % W.ORG)
    s = [Paragraph("Risk Management Policy", H1),
         Paragraph("%s. Approved by the Board of Directors on 21 January 2026. Owner: %s, %s." % (
             W.ORG, W.PEOPLE["risk"], W.TITLE["risk"]), H1S)]
    p = lambda n, t: s.append(Paragraph("<b>%s</b>&nbsp;&nbsp;%s" % (n, t), NUM))
    s.append(Paragraph("1. Purpose", H2))
    p("1.1", "The policy sets how the cooperative manages the market, credit and weather risks of its grain business "
             "and of the programmes it runs for its members.")
    s.append(Paragraph("2. Authority", H2))
    p("2.1", "The Board approves every purchase of insurance or reinsurance cover on the members' behalf. The Risk "
             "Manager recommends; the Finance Committee reviews the recommendation before the Board meets.")
    p("2.2", "Grain hedges within the limits in section 4 are placed by the grain desk without further approval.")
    s.append(Paragraph("3. Counterparties", H2))
    p("3.1", "Cover is bought only from insurers and reinsurers rated A- or better, and no more than 60 per cent of the "
             "year's premium goes to one counterparty without the Board's specific approval.")
    s.append(Paragraph("4. Grain positions", H2))
    p("4.1", "Open, unhedged grain positions are kept under 250,000 bushels for each commodity at the close of each "
             "business day.")
    s.append(Paragraph("5. Index covers", H2))
    p("5.1", "An index cover pays on an index, such as a county's yield as a statistics service estimates it, "
             "rather than on members' own losses.")
    p("5.2", "The cooperative buys an index cover for a county only when its quoted premium rate is at most 1.4 times "
             "the cover's expected loss.")
    p("5.3", "A cover's expected loss is the average, over the crop years 1991 to 2025, of the share of its liability "
             "the cover would have paid on the county's yield for each of those crop years, the yield as the cover's "
             "index defines it, brought to the cover's crop year by the reinsurer's trend.")
    p("5.4", "Index covers are reviewed every year before the crop year they attach for, and the Board decides each "
             "county's cover on its own.")
    s.append(Paragraph("6. Reporting", H2))
    p("6.1", "The Risk Manager reports positions, cover in force and claims to the Finance Committee each month and to "
             "the Board each quarter.")
    s.append(Spacer(1, 8))
    s.append(Paragraph("Replaces the policy of 18 January 2023. Section 5 was added for the 2026 review.", SMALL))
    doc.build(s, onFirstPage=frame, onLaterPages=frame)


# ---------------------------------------------------------------- the enrolment notice
def write_notice(path):
    text = """ARDLEY PLAINS GROWERS' COOPERATIVE
Member notice, 1 September 2026

2027 AREA-YIELD DROUGHT COVER: ENROLMENT

The Board is considering area-yield drought covers on members' dryland grain sorghum for the 2027 crop year. Each
county cover would pay when the county's 2027 dryland sorghum yield falls below its trigger, whatever your own yield.
To size the covers we need to know the acres you would put under them.

Enrolment opens on Tuesday 8 September and closes at 5:00 p.m. Central time on Friday 30 October 2026.

Enrol through the member portal, one field at a time, giving the field's county, its practice and the acres you
report to the Farm Service Agency for 2026. A field counts in the county where it lies, not where your farm is based.
You may correct a field's acres until the close; your latest submission for a field is the one we use.

Submissions received after the close cannot be accepted: the cooperative certifies its enrolled acres to the
reinsurer by 30 November.

Enrolment does not commit you to anything until the Board decides at its meeting of 19 November 2026.

Questions to Brent Little, Risk Manager, at the main office or through the portal's message page.
"""
    with open(path, "w", newline="", encoding="utf-8") as fh:
        fh.write(text.replace("\n", "\r\n"))


# ---------------------------------------------------------------- dictionary and register
DICT = [
    ("pull24", "Program, Year, Period", "Survey programme, crop year and reference period of the estimate."),
    ("pull24", "Geo Level", "STATE, AGRICULTURAL DISTRICT or COUNTY."),
    ("pull24", "Ag District, Ag District Code", "The agricultural statistics district and its code as the estimate "
                                                "carried it when loaded."),
    ("pull24", "County, County ANSI", "County name and county code."),
    ("pull24", "Commodity, Data Item", "Crop, and the statistic with its practice and unit."),
    ("pull24", "Domain, Domain Category", "TOTAL and NOT SPECIFIED for every row of this download."),
    ("pull24", "Value", "The estimate as published, or the service's symbol."),
    ("pull24", "CV (%)", "Coefficient of variation of a published county yield, from 2008."),
    ("pull24", "Load Time", "When the estimate entered the service's database."),
    ("pull26", "(all columns)", "As in the March 2024 download."),
    ("enrol", "submission_id", "Portal submission number."),
    ("enrol", "submitted_at", "When the member portal received the submission, UTC (ISO 8601)."),
    ("enrol", "member_no, field_id", "Member account and the member's field identifier."),
    ("enrol", "field_county, crop, practice", "County where the field lies, crop and practice entered by the member."),
    ("enrol", "acres", "Acres entered for the field."),
    ("enrol", "action", "NEW for a field's first submission, AMEND for a correction to it."),
    ("tickets", "ticket_no, site, ticket_date", "Scale ticket number, elevator site and date weighed."),
    ("tickets", "account", "Member account the load was received for."),
    ("tickets", "commodity, origin_county", "Grain received, irrigated and dryland alike, and the county the member "
                                            "declared it grown in."),
    ("tickets", "gross_lb, tare_lb, net_lb", "Scale weights in pounds."),
    ("tickets", "moisture_pct, test_weight", "Moisture (per cent) and test weight (pounds per bushel) at the probe. A "
                                             "load's bushels at standard moisture are net_lb x (100 - moisture_pct) / "
                                             "(100 - standard moisture) / pounds per bushel; for grain sorghum, 14.0 per "
                                             "cent and 56 pounds."),
    ("tickets", "reference", "Number of the document the ticket was written against."),
    ("transfers", "transfer_no, ship_date", "Transfer number and date shipped."),
    ("transfers", "from_site, to_site", "Sending and receiving elevator sites."),
    ("transfers", "commodity, net_lb, carrier", "Grain, net weight shipped in pounds, carrier."),
    ("roster", "Member no., Entity type, Home county, Joined, Status", "Member accounts as at 30 September 2026."),
    ("drought", "MapDate, County", "Drought monitor map date and county."),
    ("drought", "None, D0 to D4", "Per cent of the county's area in each category; D0 to D4 are cumulative (D0 "
                                  "includes D1 and worse)."),
    ("drought", "ValidStart, ValidEnd", "The week the map describes."),
    ("prior", "(all columns)", "Annual statements of the 2019 to 2025 covers, as issued."),
    ("quotes", "(all sheets)", "Quillfield Re's quote schedule of 14 October 2026."),
]
SITE_NOTE = "Sites: MAIN is the Corvin terminal; ARD, ELS, PAL and TRE the Ardley, Elster, Pallard and Tresham elevators."


def write_dictionary(path):
    rows = [[W.FILES[k], fld, desc] for k, fld, desc in DICT]
    rows.append([W.FILES["tickets"], "site", SITE_NOTE])
    rows.append([W.FILES["transfers"], "from_site, to_site", SITE_NOTE])
    order = []
    for r in rows:
        if r[0] not in order:
            order.append(r[0])
    rows.sort(key=lambda r: order.index(r[0]))          # each file's columns together, in the folder's order
    return P.write_csv(path, ["File", "Column(s)", "Meaning"], rows)


REGISTER = [
    ("pull24", "Crop and Livestock Reporting Service county estimates database export, field crops, districts 20, 30, "
               "50 and 60 by county, all districts and the state, crop years 1991 to 2023", "downloaded 11 March 2024"),
    ("pull26", "The same export for crop years 2016 to 2025", "downloaded 21 October 2026"),
    ("methods", "The service's methods, symbols and revisions note", "issued 26 March 2026"),
    ("terms", "Quillfield Re term sheet, area-yield drought cover, 2027 crop year", "14 October 2026"),
    ("quotes", "Quillfield Re quote schedule", "14 October 2026"),
    ("policy", "Risk management policy", "approved 21 January 2026"),
    ("enrol", "Member portal export of 2027 cover enrolment submissions", "exported 2 November 2026"),
    ("notice", "Member notice on 2027 cover enrolment", "1 September 2026"),
    ("tickets", "Elevator scale tickets, all sites, grain sorghum, wheat and corn, 2016 to 2020", "exported 28 October 2026"),
    ("transfers", "Inter-site transfer log, 2016 to 2020", "exported 28 October 2026"),
    ("roster", "Member roster", "as at 30 September 2026"),
    ("drought", "Drought monitor county statistics for the five member counties, 2000 to 2025", "downloaded 3 March 2026"),
    ("prior", "Prior area-yield covers, annual statements 2019 to 2025", "compiled 6 October 2026"),
    ("dict", "Data dictionary for this folder", "2 November 2026"),
]


def write_register(path, counts):
    rows = [[W.FILES[k], desc, when, counts.get(k, "")] for k, desc, when in REGISTER]
    rows.append([W.FILES["register"], "This register", "2 November 2026", ""])
    return P.write_csv(path, ["file", "contents", "as of", "rows"], rows)
