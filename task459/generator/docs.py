"""The pack's documents: the district's Resource Procurement Procedure RP-7 (the emissions performance standard
section), the 2026 Baseload Request for Offers, and the evaluation data dictionary."""
from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                      # noqa: E402
from reportlab.lib.pagesizes import LETTER                                            # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                       # noqa: E402
from reportlab.lib.units import inch                                                  # noqa: E402
from reportlab.pdfbase import pdfmetrics                                              # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                          # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import world as W   # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("LiberationSerif", "Regular"), ("LiberationSerif-Bold", "Bold"), ("LiberationSerif-Italic", "Italic"),
              ("LiberationSans", "Regular"), ("LiberationSans-Bold", "Bold")):
    pdfmetrics.registerFont(TTFont(nm, FONT_DIR + nm.split("-")[0] + "-" + f + ".ttf"))
INK = colors.HexColor("#1d1f21")
GREY = colors.HexColor("#5a5f66")
BODY = ParagraphStyle("body", fontName="LiberationSerif", fontSize=10.5, leading=14.5, textColor=INK, spaceAfter=6)
NUM = ParagraphStyle("num", parent=BODY, leftIndent=30, firstLineIndent=-30)
SUB = ParagraphStyle("sub", parent=BODY, leftIndent=48, firstLineIndent=-18)
H1 = ParagraphStyle("h1", fontName="LiberationSerif-Bold", fontSize=13.5, leading=17, textColor=INK, spaceAfter=3, alignment=1)
H1S = ParagraphStyle("h1s", fontName="LiberationSerif", fontSize=10, leading=13, textColor=GREY, spaceAfter=12, alignment=1)
H2 = ParagraphStyle("h2", fontName="LiberationSerif-Bold", fontSize=11, leading=15, textColor=INK, spaceBefore=7, spaceAfter=3)
CELL = ParagraphStyle("cell", fontName="LiberationSans", fontSize=8.8, leading=11, textColor=INK)
CELLB = ParagraphStyle("cellb", parent=CELL, fontName="LiberationSans-Bold")
SMALL = ParagraphStyle("small", fontName="LiberationSans", fontSize=8.5, leading=11, textColor=GREY)


def _doc(path, title, author, footer):
    def frame(canvas, doc):
        canvas.saveState()
        canvas.setFont("LiberationSans", 7.5)
        canvas.setFillColor(GREY)
        canvas.drawString(1.0 * inch, 0.6 * inch, footer)
        canvas.drawRightString(LETTER[0] - 1.0 * inch, 0.6 * inch, "Page %d" % doc.page)
        canvas.restoreState()
    d = SimpleDocTemplate(path, pagesize=LETTER, leftMargin=1.0 * inch, rightMargin=1.0 * inch, topMargin=0.9 * inch,
                          bottomMargin=0.95 * inch, title=title, author=author, subject="", creator="", producer="")
    return d, frame


def _table(rows, widths):
    data = [[Paragraph(str(c), CELLB if i == 0 else CELL) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9aa0a6")),
                           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8eaed")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 4),
                           ("RIGHTPADDING", (0, 0), (-1, -1), 4)]))
    return t


# ---------------------------------------------------------------------------------------------- RP-7
def write_procedure(path):
    doc, frame = _doc(path, "Resource Procurement Procedure RP-7", W.DISTRICT,
                      "%s  |  Resource Procurement Procedure RP-7  |  Revised 9 June 2026" % W.DISTRICT)
    s = [Paragraph(W.DISTRICT, H1), Paragraph("Resource Procurement Procedure RP-7: Long-term resource commitments", H1S),
         Paragraph("Adopted by Resolution 2021-14 of the Board of Commissioners; revised by Resolution 2026-22, "
                   "9 June 2026. Administered by the Manager, Resource Planning.", SMALL), Spacer(1, 8)]
    P = lambda n, t: s.append(Paragraph("<b>%s</b>&nbsp;&nbsp;%s" % (n, t), NUM))
    Q = lambda t: s.append(Paragraph(t, SUB))
    s.append(Paragraph("1. Purpose and scope", H2))
    P("1.1", "This procedure governs how the District evaluates offers for long-term commitments of electric generating "
             "capacity and energy, and the screens the District applies under state law before the General Manager "
             "recommends a commitment to the Board.")
    P("1.2", "It applies to every request for offers the District issues for a term of five years or more.")
    s.append(Paragraph("2. Definitions", H2))
    P("2.1", "<i>Long-term financial commitment</i> means a new ownership interest in, or a new or renewed contract for "
             "a term of five or more years for, electricity from baseload electric generation.")
    P("2.2", "<i>Baseload electric generation</i> means electric generation from a power plant that is designed and "
             "intended to provide electricity at an annualized plant capacity factor of at least sixty percent.")
    P("2.3", "<i>Plant</i> means the generating units offered under one offer, with the equipment serving them.")
    P("2.4", "<i>Net generation</i> means the electric energy a plant delivers at its point of interconnection, as "
             "measured by its revenue meter.")
    P("2.5", "<i>Contract Capacity</i>, <i>Delivery Term</i> and <i>offer data package</i> have the meanings the "
             "request for offers gives them.")
    s.append(Paragraph("3. Evaluation", H2))
    P("3.1", "The District evaluates each offer in order: completeness of the offer and its data package; eligibility; "
             "the emissions performance standard (Section 5); price and value.")
    P("3.2", "An offer is eligible if the plant is an existing natural gas-fired combined cycle in Washington or Oregon.")
    P("3.3", "An offer that fails a screen is not evaluated further. The request for offers states the need and how the "
             "District fills it from the offers that pass every screen.")
    s.append(Paragraph("4. Records", H2))
    P("4.1", "The District relies on public records (the U.S. Environmental Protection Agency's Clean Air Markets data "
             "reported under 40 CFR Part 75, and the Energy Information Administration's Forms EIA-860 and EIA-923) and "
             "on the offer data package each respondent submits with its offer.")
    s.append(Paragraph("5. Emissions performance standard", H2))
    P("5.1", "The District shall not enter into a long-term financial commitment for baseload electric generation "
             "unless the plant complies with the state's greenhouse gas emissions performance standard, currently %d "
             "pounds of greenhouse gases per megawatt-hour of net generation. For a plant fired on natural gas, the "
             "District applies the standard to carbon dioxide." % int(W.STANDARD))
    P("5.2", "A plant's emission rate is the pounds of carbon dioxide it emits per megawatt-hour of net generation it "
             "delivers under the commitment.")
    P("5.3", "Only the plant's own records may be used to determine its emission rate: its hourly carbon dioxide mass "
             "as reported to EPA under 40 CFR Part 75 for calendar years 2024 and 2025, substitute data included as "
             "reported, and its hourly net generation in those years from its revenue meter.")
    P("5.4", "A plant complies if its emission rate does not exceed the standard. Rates are compared unrounded.")
    P("5.5", "The determination states, for every offered plant, its emission rate and whether it complies.")
    s.append(Paragraph("6. Board materials", H2))
    P("6.1", "The General Manager presents the determination to the Board with the offers that pass every screen and "
             "the District's need for the delivery term. The Board approves each long-term financial commitment by "
             "resolution.")
    doc.build(s, onFirstPage=frame, onLaterPages=frame)


# ---------------------------------------------------------------------------------------------- the request for offers
def write_terms(path):
    nm, title = W.PEOPLE["planning"]
    doc, frame = _doc(path, W.RFO, W.DISTRICT, "%s  |  %s  |  Issued 1 June 2026" % (W.DISTRICT, W.RFO))
    s = [Paragraph(W.DISTRICT, H1), Paragraph("%s: unit-contingent baseload capacity and energy, 2027 to 2036" % W.RFO, H1S),
         Spacer(1, 4)]
    P = lambda n, t: s.append(Paragraph("<b>%s</b>&nbsp;&nbsp;%s" % (n, t), NUM))
    s.append(Paragraph("1. Overview", H2))
    P("1.1", "The District needs 1,000 MW of baseload capacity and energy for 1 January 2027 through 31 December 2036 "
             "and seeks it from existing natural gas-fired combined-cycle plants in Washington and Oregon, under ten-year "
             "unit-contingent agreements.")
    P("1.2", "Each agreement under this request is a long-term financial commitment for baseload electric generation. "
             "The District evaluates offers under its Resource Procurement Procedure RP-7, including the state's "
             "emissions performance standard.")
    s.append(Paragraph("2. Schedule", H2))
    s.append(_table([["Step", "Date"],
                     ["Request for offers issued", "1 June 2026"], ["Written questions due", "1 July 2026"],
                     ["Offers and offer data packages due", "30 September 2026, 5:00 p.m. Pacific"],
                     ["Evaluation", "October and November 2026"], ["Board of Commissioners", "17 November 2026"],
                     ["Agreements executed", "by 31 December 2026"], ["Deliveries begin", "1 January 2027"]],
                    [3.2 * inch, 2.6 * inch]))
    s.append(Paragraph("3. Product", H2))
    P("3.1", "Each offer is for the entire output of one plant (the Resource).")
    P("3.2", "The Seller shall schedule and deliver the Contract Capacity to the District in every hour of the Delivery "
             "Term, except during planned outages approved under 3.5 and during forced outages. The Seller shall not "
             "sell energy or capacity from the Resource to any other party during the Delivery Term.")
    P("3.3", "<i>Contract Capacity</i> means the net capacity, in megawatts at the Resource's point of interconnection, "
             "that the Seller offers to deliver in every hour.")
    P("3.4", "<i>Delivery Term</i> means 1 January 2027 through 31 December 2036.")
    P("3.5", "Planned outages are scheduled between 1 March and 30 June and total no more than 30 days in a year, unless "
             "the District agrees otherwise.")
    P("3.6", "Pricing is a fixed capacity price in dollars per kilowatt-month of Contract Capacity, escalating annually "
             "at the offered rate, and an energy charge under the District's tolling terms (the District supplies the "
             "natural gas). Heat rate terms are negotiated with the offers that pass the evaluation screens.")
    s.append(Paragraph("4. Offer data package", H2))
    P("4.1", "Each offer includes an offer data package with:")
    for t in ("(a) the Resource's hourly net generation at its revenue meter for 2024 and 2025, in the District's "
              "template (each hour's start in local time with its UTC offset);",
              "(b) the Resource's 2025 event records for each unit from its outage log, in the event format of the NERC "
              "Generating Availability Data System (GADS); and",
              "(c) the Resource's planned outages for 2027."):
        s.append(Paragraph(t, SUB))
    s.append(Paragraph("5. Evaluation", H2))
    P("5.1", "The District screens each offer for completeness, eligibility and the emissions performance standard "
             "under RP-7.")
    P("5.2", "It fills its 1,000 MW need from the offers that pass every screen in order of capacity price, lowest "
             "first, taking each offer whole and passing over any offer that would take its total above 1,000 MW. The "
             "offers it takes go forward to negotiation.")
    s.append(Paragraph("6. Credit and security", H2))
    P("6.1", "A Seller whose offer goes forward to negotiation posts security of $50 per kilowatt of Contract Capacity "
             "when the agreement is executed, as a letter of credit from a bank rated A- or better or a guarantee from a "
             "parent the District accepts, and keeps it in place through the Delivery Term.")
    s.append(Paragraph("7. Confidentiality", H2))
    P("7.1", "The District treats offer data packages as confidential commercial information to the extent RCW 42.56.270 "
             "allows and uses them only to evaluate the offers and negotiate the agreements.")
    s.append(Paragraph("8. Contact", H2))
    s.append(Paragraph("%s, %s, %s. Questions in writing only." % (nm, title, W.DISTRICT), BODY))
    doc.build(s, onFirstPage=frame, onLaterPages=frame)


# ---------------------------------------------------------------------------------------------- data dictionary
DICTIONARY = """Calder County Public Utility District No. 1
2026 Baseload Request for Offers: evaluation data, field descriptions
Prepared by Resource Planning, 4 November 2026
Days and years in the evaluation are Pacific time; a field named _utc is in UTC.

OFFER DATA PACKAGES (submitted by the respondents with their offers; compiled by the District)

rfo2026_offers_received.xlsx
  One row per offer received. Offer ID is the District's. Resource and the resource description are the
  respondent's. EIA plant code as the respondent entered it (blank where the respondent left it blank). Contract
  Capacity in MW at the point of interconnection (request for offers 3.3). Capacity price in dollars per
  kilowatt-month of Contract Capacity for 2027, and the offered annual escalation (request for offers 3.6).

rfo2026_offer_meter_data_2024-2025.csv
  offer_id, resource
  interval_start    the hour's start, local time with its UTC offset (-08:00 standard time, -07:00 daylight time)
  interval_minutes  60
  net_mwh           net energy delivered at the point of interconnection in the hour, from the revenue meter;
                    negative when the plant draws station service while not generating

rfo2026_offer_gads_events_2025.csv
  The respondents' 2025 event records for each unit from their outage logs, in the GADS event format, unit by unit
  as submitted.
  unit          CT1, CT2: combustion turbines; ST1: steam turbine; CS1: single-shaft combined-cycle unit
  event_number  the respondent's number for the unit's event
  event_type    GADS event type: U1 immediate forced outage; U2 delayed forced outage; U3 postponed forced
                outage; SF startup failure; MO maintenance outage; PO planned outage; RS reserve shutdown;
                D1 immediate forced derate; D4 maintenance derate; PD planned derate. Forced outages are types
                U1, U2, U3 and SF. An outage takes a unit, or a whole plant, off line; a derate leaves it
                running below its net maximum capacity.
  start_utc, end_utc            event start and end, UTC
  net_available_capacity_mw     the unit's net available capacity during the event
  cause_code, description       GADS cause code and the respondent's description
  entered_utc                   when the respondent entered the record

rfo2026_offer_planned_outages_2027.csv
  Planned and maintenance outages the respondents have scheduled for 2027.

PUBLIC DATA (downloaded by Resource Planning)

camd_hourly_emissions_offered_units_2024-2025.csv
  EPA Clean Air Markets Program Data, hourly emissions of the offered plants' monitored units, 2024 and 2025,
  downloaded 6 October 2026 (2025 fourth-quarter submissions included). Facility ID is the plant's ORIS code, the
  same as its EIA plant code. Date and Hour in local standard time; Hour 0 is midnight to 1 a.m. Operating Time is
  the fraction of the hour the unit operated (0.00 when it did not operate, the other fields then blank). Gross Load
  (MW) is the average gross load while operating. Heat Input (mmBtu) and the masses are totals for the hour. A
  measure indicator says how the value was determined (Measured, Calculated or Substitute).

camd_monitoring_plans_offered_units.csv
  The monitored units' monitoring plan records: unit and stack identifiers, dates in effect, methodologies and the
  plan's comments.

epa_eia_crosswalk_2025.csv
  EPA's Power Sector Data Crosswalk, 2025 release (built on 2024 monitoring plans and the 2024 Form EIA-860),
  rows for the offered plants: each monitored unit matched to its EIA generators.

eia860_2025_generator_offered_plants.xlsx
  Form EIA-860, 2025 final release, Schedule 3 generator data (operable units) for the offered plants' EIA plant
  codes, every generator at the plant.

eia923_2024-2025_generation_and_fuel_offered_plants.xlsx
  Form EIA-923 Page 1, generation and fuel, 2024 final and 2025 final release, for the offered plants' EIA plant
  codes, by reported prime mover and fuel.
"""


def write_dictionary(path):
    with open(path, "w", encoding="utf-8", newline="\r\n") as f:
        f.write(DICTIONARY)
    return DICTIONARY.count("\n")
