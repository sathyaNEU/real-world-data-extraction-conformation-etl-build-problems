"""The pack's three documents: the Seasonal Communities Aid Act, the Quillmere Lake Protection Fee ordinance, and the
basin's wastewater facilities fact sheet."""
import reportlab.rl_config
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import world as W

reportlab.rl_config.invariant = 1
STY = getSampleStyleSheet()
BODY = ParagraphStyle("b", parent=STY["BodyText"], fontName="Helvetica", fontSize=9.5, leading=12.5, spaceAfter=6)
SMALL = ParagraphStyle("s", parent=BODY, fontSize=8, leading=10)
H = ParagraphStyle("h", parent=STY["Heading2"], fontName="Helvetica-Bold", fontSize=11, spaceBefore=8, spaceAfter=4)
T = ParagraphStyle("t", parent=STY["Title"], fontName="Helvetica-Bold", fontSize=14, spaceAfter=10)
DISTRICT = "Quillmere Lake Protection District"
FEE_OFFICE = "Quillmere Lake Basin Fee Office"


def _pdf(path, title, story, author, org):
    doc = SimpleDocTemplate(path, pagesize=letter, leftMargin=0.8 * inch, rightMargin=0.8 * inch, topMargin=0.7 * inch,
                            bottomMargin=0.7 * inch, title=title, author=author, creator=author, subject=title,
                            producer=org)

    def footer(c, d):
        c.saveState()
        c.setFont("Helvetica", 7.5)
        c.drawString(0.8 * inch, 0.45 * inch, org + "  |  " + title)
        c.drawRightString(letter[0] - 0.8 * inch, 0.45 * inch, "Page %d" % d.page)
        c.restoreState()

    doc.build(story, onFirstPage=footer, onLaterPages=footer)


def _table(rows, widths=None):
    t = Table(rows, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", 8), ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8),
                           ("LINEBELOW", (0, 0), (-1, 0), 0.5, colors.black), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 2), ("TOPPADDING", (0, 0), (-1, -1), 2)]))
    return t


def P(text, style=BODY):
    return Paragraph(text, style)


def statute_pdf(path):
    towns = ", ".join(W.NAMES[:-1]) + " and " + W.NAMES[-1]
    s = [P("Seasonal Communities Aid Act", T),
         P("As enacted, Laws 2025, Regular Session, article 7 (Seasonal Communities Aid), sections 1 to 6. Unofficial "
           "text prepared by the Office of the State Demographer for the 2027 certification.", SMALL),
         P("Section 1. Purpose", H),
         P("Aid is paid to the cities of the Quillmere Lake basin whose public services must carry, in their busiest "
           "season, a population far larger than the people who live in them."),
         P("Section 2. Definitions", H),
         P("(a) <b>Basin city</b> means each of the cities of " + towns + "."),
         P("(b) <b>Resident population</b> means the State Demographer's estimate of a city's population on 1 July of the "
           "measurement year."),
         P("(c) <b>Measurement year</b> for an aid year means the twelve months from 1 October two years before the aid "
           "year through 30 September of the year before it. For aid year 2027 it is 1 October 2025 through "
           "30 September 2026."),
         P("(d) <b>Population present</b> on a day means the number of persons in the city that day: its residents and "
           "every other person staying in or visiting the city, each person counted for the share of the day spent in "
           "the city."),
         P("(e) <b>Average population present</b> in a month means the mean of the city's population present over the "
           "days of the month."),
         P("(f) <b>Busiest month</b> means the calendar month of the measurement year in which a city's average "
           "population present was highest."),
         P("Section 3. Qualification", H),
         P("A basin city qualifies for aid in an aid year when its average population present in its busiest month of "
           "the measurement year was at least three times its resident population."),
         P("Section 4. Appropriation and distribution", H),
         P("USD 2,400,000 is appropriated for aid year 2027. The Commissioner of Revenue distributes it in equal shares "
           "to the cities that qualify, half on 20 July 2027 and half on 26 December 2027. A city that does not qualify "
           "receives no aid for the year."),
         P("Section 5. Certification", H),
         P("By 1 December of the year before the aid year the State Demographer certifies to the Commissioner of Revenue, "
           "for each basin city, its resident population, its busiest month, its average population present in that "
           "month rounded to the nearest thousand, and whether it qualifies. The certification is final for the aid "
           "year."),
         P("Section 6. Reports with the certification", H),
         P("With the certification the State Demographer reports (1) to the Quillmere Lake Basin Fee Office, the Lake "
           "Protection Fee generated by stays in each basin city in each quarter of the fiscal year that ended on 30 "
           "June of the measurement year, for the Office's revenue report; and (2) to the Quillmere Lake Protection "
           "District, the pounds of total phosphorus each basin wastewater treatment plant discharged in each half of "
           "the calendar year before the measurement year ended, for the District's phosphorus reduction grants."),
         Spacer(1, 6),
         P("Section 6 reports are statistical and do not affect the aid.", SMALL)]
    _pdf(path, "Seasonal Communities Aid Act", s, W.PEOPLE["estimates"], W.OFFICE)


def ordinance_pdf(path):
    s = [P("Quillmere Lake Protection Fee", T),
         P("Ordinance 2019-4 of the Quillmere Lake Basin Joint Powers Board, as amended by Ordinance 2025-2. "
           "Administered by the " + FEE_OFFICE + ".", SMALL),
         P("1. Fee", H),
         P("A Lake Protection Fee is due on every paid stay of fewer than 30 consecutive nights in a hotel, motel, inn, "
           "resort, bed and breakfast, campground or whole-home rental in a basin city. The fee is charged for each "
           "guest for each night of the stay: USD 1.25 a guest-night through 31 December 2025 and USD 1.50 a "
           "guest-night from 1 January 2026, the rate being the one in force on the night of the stay. A stay of 30 "
           "consecutive nights or more is exempt."),
         P("2. Returns", H),
         P("An operator of eight or more rentable units files a return each month; any other operator files each "
           "calendar quarter. A return is due by the 20th day of the month after the period and reports the period's "
           "guest-nights, its exempt guest-nights and the fee due. An operator who finds an error files an amended "
           "return, which replaces the earlier return for the period; guest-nights left off a return are reported on a "
           "supplemental return for the same period."),
         P("3. Marketplace platforms", H),
         P("A booking platform with a collection agreement collects the fee from its guests and remits it to the Fee "
           "Office monthly with a detail of the stays remitted; the operator does not report those stays. Lakeward "
           "Stays and Kettle & Pine hold collection agreements effective 1 July 2024."),
         P("4. Use of the fee", H),
         P("The fee is deposited in the Lake Protection Fund. The Fund pays the Fee Office's costs and makes the "
           "Quillmere Lake Protection District's grants to the basin's wastewater treatment plants for phosphorus "
           "reduction.")]
    _pdf(path, "Quillmere Lake Protection Fee ordinance", s, "Fee Office", FEE_OFFICE)


def facilities_pdf(path):
    rows = [["Plant", "Permit", "Cities served", "Treatment", "Design avg flow, MGD", "Receiving water",
             "Discharge"]]
    spec = dict(BIR=("Extended aeration, chemical P removal", 0.62, "Birch Creek", "Continuous"),
                TES=("Activated sludge, chemical P removal", 1.10, "Quill River", "Continuous"),
                RUD=("Stabilization ponds, three cells", 0.29, "Ruddmere Creek", "Spring and autumn drawdowns"),
                SOR=("Activated sludge, biological P removal", 1.35, "Quill River", "Continuous"),
                PIN=("Stabilization ponds, three cells", 0.42, "Arlen Ditch No. 3", "Spring and autumn drawdowns"),
                TAM=("Sequencing batch reactor, chemical P removal", 1.05, "Tamsen Brook", "Continuous"),
                NAR=("Activated sludge, chemical P removal", 1.20, "Quill River", "Continuous"))
    for code, pl in W.PLANTS.items():
        sp = spec[code]
        rows.append([Paragraph(pl["name"], SMALL), pl["permit"], Paragraph(", ".join(pl["towns"]), SMALL),
                     Paragraph(sp[0], SMALL), "%.2f" % sp[1], sp[2], Paragraph(sp[3], SMALL)])
    s = [P("Quillmere Lake basin wastewater treatment facilities", T),
         P("Fact sheet, " + DISTRICT + ", revised March 2026.", SMALL),
         P("The basin's eight cities are served by seven treatment facilities. The townships around them are on private "
           "septic systems."),
         _table(rows, [1.55 * inch, 0.75 * inch, 0.9 * inch, 1.25 * inch, 0.7 * inch, 0.85 * inch, 0.9 * inch]),
         Spacer(1, 8),
         P("Collection", H),
         P("Under the District's shoreland rules every developed parcel in a basin city is connected to the city's "
           "sewer. Esker Narrows and Hollin Bay send their wastewater by force main to the Narrows joint plant, where "
           "each city's flow is metered at the headworks for the joint board's billing."),
         P("Reporting", H),
         P("The Birchwick, Teskadel, Sorrelton, Tamsen Point and Narrows joint plants file their discharge "
           "monitoring reports through the state's electronic reporting system. " + "Northwoods Utility Services" +
           " operates the Ruddmere and Pinehold pond systems under contract and keeps their monthly operating reports. "
           "Influent is sampled as 24-hour composites at the headworks. A load in the District's reports is the flow "
           "in million gallons a day times the concentration in milligrams per liter times 8.34, in pounds a day."),
         P("Pond systems", H),
         P("The stabilization ponds hold the year's wastewater and discharge only during drawdowns after ice-out in "
           "spring and before freeze-up in autumn, on the days the operator opens the outlet; their reports carry no "
           "discharge in the other months.")]
    _pdf(path, "Quillmere Lake basin wastewater treatment facilities", s, "District engineer", DISTRICT)
