"""The pack's documents: the State Workforce Development Board's Workforce Value Designation Standard, the outcomes
release's technical notes, the college's 2024-25 cost of attendance and the board's in-demand occupations list (all
PDF)."""
from reportlab import rl_config
rl_config.invariant = 1
from reportlab.lib import colors                                     # noqa: E402
from reportlab.lib.pagesizes import letter                           # noqa: E402
from reportlab.lib.styles import ParagraphStyle                      # noqa: E402
from reportlab.lib.units import inch                                 # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import asks as A    # noqa: E402
import world as W   # noqa: E402

BODY = ParagraphStyle("b", fontName="Times-Roman", fontSize=10.5, leading=13.6, spaceAfter=6)
HEAD = ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=10.5, leading=14, spaceBefore=8, spaceAfter=4)
TITLE = ParagraphStyle("t", fontName="Helvetica-Bold", fontSize=14, leading=18, spaceAfter=4)
SUB = ParagraphStyle("s", fontName="Helvetica", fontSize=9, leading=12, textColor=colors.HexColor("#444444"),
                     spaceAfter=10)
GRID = TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", 8), ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8),
                   ("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.black),
                   ("LINEBELOW", (0, -1), (-1, -1), 0.4, colors.HexColor("#777777")),
                   ("BOTTOMPADDING", (0, 0), (-1, -1), 2.4), ("TOPPADDING", (0, 0), (-1, -1), 2.0),
                   ("VALIGN", (0, 0), (-1, -1), "TOP")])


def _doc(path, title, org):
    d = SimpleDocTemplate(path, pagesize=letter, leftMargin=0.9 * inch, rightMargin=0.9 * inch, topMargin=0.85 * inch,
                          bottomMargin=0.85 * inch, title=title, author=org, creator=org, producer=org, subject=title)

    def frame(c, d_):
        c.saveState()
        c.setFont("Helvetica", 7.5)
        c.setFillColor(colors.HexColor("#555555"))
        c.drawString(0.9 * inch, 0.5 * inch, "%s  |  %s" % (org, title))
        c.drawRightString(letter[0] - 0.9 * inch, 0.5 * inch, "Page %d" % d_.page)
        c.restoreState()
    return d, frame


def _p(items):
    return [Paragraph(x, BODY) for x in items]


def write_standard(path):
    title = "Workforce Value Designation Standard, 2027-28 Grant Year"
    org = W.BOARD
    d, frame = _doc(path, title, org)
    s = [Paragraph("Workforce Value Designation Standard", TITLE),
         Paragraph("%s, Career Training Grant. 2027-28 grant year. Adopted by the board on 18 June 2026. Administered "
                   "by the board's grant programs office; contact %s, Grant Programs Manager." % (org, W.PEOPLE["board"]),
                   SUB),
         Paragraph("1 Purpose", HEAD)]
    s += _p(["1.1 The %s pays tuition and fees for eligible residents enrolled in short-term programs at "
             "training providers the board designates. A provider keeps its designation from one grant year to the "
             "next only if its programs show workforce value. This standard sets how the board decides whether a "
             "provider's designation renews for the 2027-28 grant year (1 July 2027 to 30 June 2028)." % W.GRANT,
             "1.2 The board votes the 2027-28 designations at its March 2027 meeting. The grant's 2027-28 "
             "appropriation is committed to designated providers' programs from 1 July 2027."])
    s += [Paragraph("2 Programs and their tests", HEAD)]
    s += _p(["2.1 Every program on the provider's 2025-26 program inventory is reviewed.",
             "2.2 A degree program or a certificate program of one academic year or more (a credit program) takes "
             "the earnings test in section 3. A short-term program (a clock-hour program of under 600 clock hours) "
             "takes the placement test in section 4."])
    s += [Paragraph("3 Earnings test", HEAD)]
    s += _p(["3.1 A program's earnings figure is the median annual earnings of the program's completers in award "
             "years 2020-21 and 2021-22, each measured in the third full calendar year after the award year (calendar "
             "2024 for award year 2020-21, calendar 2025 for award year 2021-22), with every campus that offered the "
             "program and both award years taken as one group. The completers are those the State Education and "
             "Workforce Data Center's Postsecondary Earnings Outcomes release counts with earnings.",
             "3.2 Earnings are compared in 2025 dollars. Earnings measured in calendar 2024 are multiplied by 1.0294, "
             "the Consumer Price Index for All Urban Consumers' 2025 annual average over its 2024 annual average; "
             "earnings measured in calendar 2025 are used as published.",
             "3.3 The program passes when its earnings figure is at or above the board's earnings benchmark of "
             "USD 34,200 in 2025 dollars, the median annual earnings of the state's full-year workers aged 25 to 34 "
             "whose highest education is a high school diploma.",
             "3.4 A cell the release suppresses publishes no statistics and is left out of the group. A program is "
             "tested when the release's published cells for it, across both award years, hold at least 30 completers "
             "with earnings. A program with fewer is not tested."])
    s += [Paragraph("4 Placement test", HEAD)]
    s += _p(["4.1 A program's placement figure is the share of its grant completers who were working for an employer "
             "on the 180th day after the day they completed. Its grant completers are the %s participants who "
             "completed a section of the program that ended from 1 July 2024 to 30 June 2025. A participant completes "
             "on the last day of their section, as the grant's participant roster records it." % W.GRANT,
             "4.2 Working for an employer means employment covered by the state's unemployment insurance law. The "
             "board reads it from the wage records the state's unemployment insurance division returns for grant "
             "participants. A wage record is the wages one employer reported paying one participant in one calendar "
             "quarter; an amended report replaces the original report for the same participant, employer and "
             "quarter. Self-employment and work outside the state are not counted.",
             "4.3 The program passes when its placement figure is 70 per cent or more.",
             "4.4 A program is tested when it has at least 20 grant completers. A program with fewer is not tested."])
    s += [Paragraph("5 Designation", HEAD)]
    s += _p(["5.1 The provider's designation renews for the 2027-28 grant year when at least 75 per cent of its "
             "2024-25 completers in tested programs are in programs that pass their test. Otherwise the designation "
             "lapses on 30 June 2027, and the provider may apply again for the 2028-29 grant year.",
             "5.2 A program's 2024-25 completers are the students the provider's completion records show completing "
             "it from 1 July 2024 to 30 June 2025 at any campus, grant participants or not: for a degree or "
             "certificate, an award conferred in that period; for a short-term program, a section completed in it. "
             "Programs that are not tested count in neither the 75 per cent nor the total it is taken of.",
             "5.3 The board compares each figure with its line as computed, before any rounding."])
    s += [Paragraph("6 Data", HEAD)]
    s += _p(["6.1 Postsecondary Earnings Outcomes, 2024 and 2025 editions, %s." % W.CENTER,
             "6.2 The provider's 2024-25 completion records as each campus's student system exports them, and its "
             "2025-26 program inventory.",
             "6.3 The %s participant roster and the participants' unemployment insurance wage records, as the "
             "board holds them under the grant's participant agreement." % W.GRANT,
             "6.4 An award year runs from 1 July to 30 June."])
    d.build(s, onFirstPage=frame, onLaterPages=frame)


def write_notes(path):
    title = "Postsecondary Earnings Outcomes: Technical Notes, 2025 Edition"
    org = W.CENTER
    d, frame = _doc(path, title, org)
    s = [Paragraph("Postsecondary Earnings Outcomes: Technical Notes", TITLE),
         Paragraph("%s. 2025 edition, released 14 April 2026. Release lead: %s." % (org, W.PEOPLE["center"]), SUB),
         Paragraph("Coverage", HEAD)]
    s += _p(["The release covers the state's public colleges. Each campus that reports to the state's student data "
             "system under its own unit identifier is reported as its own unit.",
             "A cell is one unit's completers of one program (its six-digit Classification of Instructional Programs "
             "code), at one award level, in one award year (1 July to 30 June), with their earnings in one earnings "
             "year. A student who earned more than one award in the same program in an award year is counted once, "
             "at the highest award."])
    s += [Paragraph("Earnings", HEAD)]
    s += _p(["A completer's earnings are the wages that employers covered by the state's unemployment insurance law "
             "reported paying the completer in the earnings year. Completers with no such wages in the earnings year "
             "(who did not work, worked for themselves, for the federal government or outside the state) are not "
             "counted with earnings. Earnings are in the earnings year's dollars and are not adjusted for inflation.",
             "The earnings year is the calendar year a stated number of years after the award year: for award year "
             "2020-21, one year after is calendar 2022, three years after is calendar 2024 and five years after is "
             "calendar 2026."])
    s += [Paragraph("Statistics and suppression", HEAD)]
    s += _p(["For each cell the release publishes the number of completers with earnings and the 10th, 25th, 50th "
             "(median), 75th and 90th percentiles of their earnings. Percentiles are rounded to the nearest 100 "
             "dollars.",
             "A cell with fewer than 10 completers with earnings is suppressed: none of its statistics is published."])
    s += [Paragraph("Editions", HEAD)]
    s += _p(["The 2024 edition reports earnings years through 2024 and codes each cell by the CIP code recorded on "
             "the awards. From the 2025 edition every cell is coded by the program's current CIP 2020 code, so a "
             "program recoded by its college appears under its current code.",
             "The 2024 edition was published as a workbook. The 2025 edition is published as a long-format file with "
             "one row per cell and statistic; suppressed statistics carry an S in the suppression column."])
    d.build(s, onFirstPage=frame, onLaterPages=frame)


def write_coa(path):
    title = "Cost of Attendance and Financial Aid, 2024-25"
    org = W.SYSTEM
    d, frame = _doc(path, title, org)
    s = [Paragraph("Cost of Attendance and Financial Aid, 2024-25", TITLE),
         Paragraph("%s, Office of Financial Aid. Consumer information published under the Higher Education Act." % org,
                   SUB),
         Paragraph("Estimated cost of attendance, full-time student, two semesters", HEAD)]
    rows = [["", "Living with family", "Living on own"], ["Tuition (30 credits, in-district)", "4,950", "4,950"],
            ["Fees", "540", "540"], ["Books, course materials and supplies", "1,320", "1,320"],
            ["Housing and food", "4,860", "11,700"], ["Transportation", "2,100", "2,520"],
            ["Personal expenses", "1,980", "2,250"], ["Total", "15,750", "23,280"]]
    t = Table(rows, colWidths=[3.1 * inch, 1.5 * inch, 1.5 * inch])
    t.setStyle(GRID)
    s += [t, Spacer(1, 8)]
    s += _p(["Tuition is 165 dollars a credit in-district and 245 dollars a credit out of district. Short-term "
             "certificate programs are priced by program; see the program inventory.",
             ])
    s += [Paragraph("Federal Direct Loans", HEAD)]
    s += _p(["Students in eligible degree and certificate programs may borrow Federal Direct Subsidized and "
             "Unsubsidized Loans. Annual limits: first year 5,500 dollars (no more than 3,500 subsidized) for dependent "
             "students and 9,500 dollars for independent students; second year and after 6,500 dollars (no more than "
             "4,500 subsidized) for dependent students and 10,500 dollars for independent students. Parents of "
             "dependent students may borrow Direct PLUS Loans in their own names.",
             "Each loan is disbursed in installments, normally one each semester. An origination fee of 1.057 per "
             "cent is deducted from each disbursement of a Direct Subsidized or Unsubsidized Loan first disbursed on "
             "or after 1 October 2020 and before 1 October 2025; the borrower repays the full amount borrowed, "
             "including the fee.",
             "A student may cancel all or part of a disbursement within 120 days of the date it was made by returning "
             "it to the college; a returned disbursement is not owed."])
    d.build(s, onFirstPage=frame, onLaterPages=frame)


DEMAND = [("29-1141", "Registered Nurses", "Tier 1"), ("53-3032", "Heavy and Tractor-Trailer Truck Drivers", "Tier 2"),
          ("31-1131", "Nursing Assistants", "Tier 3"), ("31-9097", "Phlebotomists", "Tier 3"),
          ("29-2052", "Pharmacy Technicians", "Tier 3"), ("29-2042", "Emergency Medical Technicians", "Tier 3"),
          ("51-4121", "Welders, Cutters, Solderers, and Brazers", "Tier 2"),
          ("49-9021", "Heating, Air Conditioning, and Refrigeration Mechanics and Installers", "Tier 2"),
          ("15-1232", "Computer User Support Specialists", "Tier 2"), ("29-2072", "Medical Records Specialists", "Tier 3"),
          ("53-7051", "Industrial Truck and Tractor Operators", "Tier 3"), ("53-7065", "Stockers and Order Fillers",
          "Tier 3"), ("49-3031", "Bus and Truck Mechanics and Diesel Engine Specialists", "Tier 2"),
          ("29-2034", "Radiologic Technologists and Technicians", "Tier 1"), ("31-9092", "Medical Assistants", "Tier 3"),
          ("49-3023", "Automotive Service Technicians and Mechanics", "Tier 2")]


def write_demand(path):
    title = "In-Demand Occupations List, 2026-27"
    org = W.BOARD
    d, frame = _doc(path, title, org)
    s = [Paragraph("In-Demand Occupations List, 2026-27", TITLE),
         Paragraph("%s. Adopted 12 February 2026 for the board's sector partnership and outreach programs." % org, SUB)]
    s += _p(["The list names the occupations the board's labor market analysis projects to have the most openings "
             "in the state over the next five years. Tier 1 occupations have a projected median wage at or above "
             "the state median for all occupations; tier 2, at or above 85 per cent of it; tier 3, below.",
             "The list guides the board's outreach and its sector partnerships with employers. It is reviewed each "
             "February."])
    rows = [["SOC code", "Occupation", "Wage tier"]] + [list(x) for x in DEMAND]
    t = Table(rows, colWidths=[0.9 * inch, 4.4 * inch, 0.9 * inch])
    t.setStyle(GRID)
    s += [t]
    d.build(s, onFirstPage=frame, onLaterPages=frame)
