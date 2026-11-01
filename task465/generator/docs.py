"""The pack's documents: the energy survey's technical notes, the screening pilot's operations report and the 2027 HEMA plan."""
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
TEAL = colors.HexColor("#1d5c63")
NAVY = colors.HexColor("#1f3a5f")
PLUM = colors.HexColor("#5a2d52")
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


def fmt(v):
    return "{:,}".format(int(v))


# ---------------------------------------------------------------- the energy survey's technical notes
def write_heas_notes(path, n):
    H1, H1S, H2 = styles(TEAL)
    doc, frame = _doc(path, "Household Energy Affordability Survey 2025: Technical Notes", W.ENERGY_OFFICE,
                      "%s  |  Household Energy Affordability Survey 2025  |  Technical notes for the public-use "
                      "household file  |  November 2025" % W.ENERGY_OFFICE)
    s = [Paragraph("Household Energy Affordability Survey 2025", H1),
         Paragraph("Technical notes for the public-use household file. %s, Research and Planning Section. Released "
                   "November 20, 2025." % W.ENERGY_OFFICE, H1S),
         Paragraph("1. About the survey", H2),
         Paragraph("The Household Energy Affordability Survey measures what households in the state pay for home "
                   "energy and how those costs compare with household income. The 2025 survey was in the field from "
                   "February 10 to June 27, 2025, and asked about electricity, natural gas and other heating fuels, "
                   "the home and its heating, and household income.", BODY),
         Paragraph("2. Sample", H2),
         Paragraph("The sample was drawn from the state's residential address frame, stratified by county, with at "
                   "least 70 completed interviews in each county and the rest allocated in proportion to the county's "
                   "households. Households answered on the web, by telephone or on a paper form (coded W, T and P). "
                   "%s households completed the survey; the public-use file holds one record for each." % fmt(n), BODY),
         Paragraph("3. Weights", H2),
         Paragraph("Each record carries two weights. The base weight is the inverse of the household's probability of "
                   "selection, adjusted for nonresponse within county and response mode. The final weight calibrates "
                   "the base weight to the State Demographer's estimates "
                   "of households by county and household income band for July 1, 2025 (under $25,000; $25,000 to "
                   "$49,999; $50,000 to $74,999; $75,000 and over), so that the weighted households of every county "
                   "and band equal those estimates. The office's published estimates use the final weight.", BODY),
         Paragraph("4. Energy costs", H2),
         Paragraph("The survey asks what the household paid for electricity over the past 12 months. Respondents who "
                   "could not give a 12-month amount gave a typical monthly bill instead; the file codes the basis of "
                   "each electricity amount A for 12 months and M for a typical month, and the annual electricity cost "
                   "of an M household is 12 times its amount. The survey also asks the 12-month cost of utility "
                   "natural gas and the 12-month cost of bottled gas, fuel oil, kerosene, wood and any other heating "
                   "fuel. A household's annual home energy cost is its annual electricity cost plus its natural gas "
                   "and other fuel costs. Amounts are whole dollars and include anything an assistance program paid "
                   "on the household's behalf.", BODY),
         Paragraph("The office reports a household's energy burden as its annual home energy cost as a share of its "
                   "household income.", BODY),
         Paragraph("5. Income, home and geography", H2),
         Paragraph("Household income is total household money income over the 12 months before the interview, in "
                   "dollars, rounded to the nearest $100 and top-coded at $248,000; missing income was imputed before "
                   "release. Tenure is coded 1 for a home owned and 2 for a home rented, and the main heating fuel 1 "
                   "utility gas, 2 electricity, 3 bottled, tank or LP gas, 4 fuel oil or kerosene, 5 wood, 6 other or "
                   "none. Counties carry the state's three-digit county codes; the file has no geography below the "
                   "county.", BODY),
         Paragraph("6. Use of the file", H2),
         Paragraph("Estimates for areas smaller than a county, or for counties and income bands with few completed "
                   "interviews, carry wide margins of error. Questions about the file go to the Research and Planning "
                   "Section.", BODY)]
    doc.build(s, onFirstPage=frame, onLaterPages=frame)


# ---------------------------------------------------------------- the screening pilot's operations report
def write_pilot_report(path, screens):
    H1, H1S, H2 = styles(NAVY)
    doc, frame = _doc(path, "HEMA Screening Pilot 2025: Operations Report", W.ORG,
                      "%s  |  Customer Programmes  |  HEMA screening pilot 2025: operations report  |  September 2025"
                      % W.ORG)
    import sim as S
    tab = [["Division", "Mode", "Screens returned", "Ended at the income question", "Complete", "Partial"]]
    for d, m, v in S.pilot_counts(screens):
        tab.append([d, m] + [fmt(n) for n in v])
    s = [Paragraph("HEMA screening pilot 2025: operations report", H1),
         Paragraph("%s, Customer Programmes. Prepared by %s, %s. September 26, 2025." % (
             W.ORG, W.PEOPLE["manager"], W.TITLES["manager"]), H1S),
         Paragraph("1. Purpose", H2),
         Paragraph("Before the 2027 programme plan, Customer Programmes tested the Home Energy Medical Assistance "
                   "screener, the mail and telephone workflow and the hand-off to caseworkers in the North Metro and "
                   "South Metro divisions.", BODY),
         Paragraph("2. Addresses and contact", H2),
         Paragraph("The billing system drew 10,800 active residential service addresses at random in each of the two "
                   "divisions, 21,600 in all. Each address was mailed the screener on March 3, 2025, with a reminder "
                   "card on March 24. From May 5 to August 29, 2025 the call centre telephoned addresses that had not "
                   "returned a screen, and some that had.", BODY),
         Paragraph("3. The screener", H2),
         Paragraph("Q1 asks the household's income over the last 12 months; a household reporting $50,000 or more is "
                   "thanked and the screen ends there. Q2 asks what the household paid for electricity over the last 12 "
                   "months, Q3 what it paid for natural gas, propane, fuel oil, wood or other heating fuels over the "
                   "same months, and Q4 whether anyone living in the home uses electrically powered medical equipment "
                   "at home (yes, no, don't know).", BODY),
         Paragraph("4. Returns", H2),
         _table(tab, [1.15 * inch, 0.7 * inch, 1.05 * inch, 1.45 * inch, 0.9 * inch, 0.8 * inch]),
         Spacer(1, 8),
         Paragraph("5. The screen records", H2),
         Paragraph("Each returned screen is one record in the pilot file. An address that returned a screen by mail "
                   "and answered again when the call centre telephoned has two records under the same address key; the "
                   "programme takes the latest complete screen as the address's answer. A partial screen stopped before "
                   "Q4.", BODY),
         Paragraph("6. What the pilot taught us", H2),
         Paragraph("A telephone screen took 6.4 minutes on average and a returned paper screen 3 minutes to key. Mail "
                   "returns peaked in the second week after each mailing. Several callers read Q3 as covering only "
                   "natural gas; the 2027 screener names propane and fuel oil first. The call centre needs two more "
                   "agents during a mailing month at the scale of a territory-wide screen.", BODY)]
    doc.build(s, onFirstPage=frame, onLaterPages=frame)


# ---------------------------------------------------------------- the 2027 HEMA plan
def write_plan(path):
    H1, H1S, H2 = styles(PLUM)
    doc, frame = _doc(path, "Home Energy Medical Assistance: 2027 Programme Plan (draft)", W.ORG,
                      "%s  |  Home Energy Medical Assistance  |  2027 programme plan, draft for filing  |  November 2026"
                      % W.ORG)
    s = [Paragraph("Home Energy Medical Assistance: 2027 programme plan", H1),
         Paragraph("Draft for filing with the %s by December 1, 2026. Prepared by %s, %s; reviewed by %s, %s. "
                   "November 12, 2026." % (W.REGULATOR, W.PEOPLE["manager"], W.TITLES["manager"], W.PEOPLE["vp"],
                                           W.TITLES["vp"]), H1S),
         Paragraph("1. Purpose", H2),
         Paragraph("Home Energy Medical Assistance (HEMA) helps households with modest incomes in which someone relies "
                   "on electrically powered medical equipment at home. Oxygen concentrators, home dialysis machines, "
                   "ventilators and similar equipment run for hours every day and add to a household's electricity "
                   "bill, and an interruption in service can endanger the person who relies on them.", BODY),
         Paragraph("2. Eligibility", H2),
         Paragraph("A household is eligible for HEMA when (a) its household income is under $50,000, (b) its annual "
                   "home energy costs (electricity, natural gas and other home heating fuels) exceed 6 per cent of its "
                   "household income, and (c) someone who lives in the home relies on electrically powered medical "
                   "equipment at home.", BODY),
         Paragraph("3. Services", H2),
         Paragraph("HEMA caseworkers enrol eligible households in the medical baseline rate, arrange payment plans "
                   "and budget billing, refer households to energy assistance and weatherization programs, and arrange "
                   "a backup battery for customers who rely on life-support equipment (placements began in December "
                   "2025). The programme's dates are the company's operating day in Central Time.", BODY),
         Paragraph("4. Staffing standard", H2),
         Paragraph("HEMA caseworkers are staffed by service division: one caseworker for every 400 eligible households "
                   "in a service division, or part of that number. The service divisions are the nine divisions of the "
                   "company's division register, and a household belongs to the division the register gives the county "
                   "of its service premise.", BODY),
         Paragraph("5. Data annex: eligible households", H2),
         Paragraph("The staffing rests on the number of eligible households in each service division and eligible "
                   "income band (under $25,000; $25,000 to $49,999) in 2025, the latest survey year, each estimated "
                   "for the division and band as a whole and filed with the plan as one table by division and band. The Commission checks such tables against the state's "
                   "official figures, so in each division and band the table reproduces the State Demographer's "
                   "household estimate for July 1, 2025, the %s's %s estimate of the share of households whose annual "
                   "home energy costs exceed 6 per cent of income, and the %s's %s estimate of the share of households "
                   "in which someone relies on electrically powered medical equipment (the department's published "
                   "percentages, which leave out don't know and refused answers)."
                   % (W.ENERGY_OFFICE, W.SURVEY_A, W.HEALTH_DEPT, W.SURVEY_B), BODY),
         Paragraph("6. Budget", H2),
         Paragraph("The 2027 budget carries each caseworker at $78,400 in salary and benefits, backup batteries at "
                   "$1,150 a unit installed, and outreach at $236,000. The caseworker line follows the staffing in "
                   "section 4.", BODY),
         Paragraph("7. Filing and timetable", H2),
         Paragraph("The plan is filed with the %s by December 1, 2026. The company expects the Commission's decision "
                   "in March 2027 and staffs the 2027 caseworker positions from April 1, 2027." % W.REGULATOR, BODY)]
    doc.build(s, onFirstPage=frame, onLaterPages=frame)
