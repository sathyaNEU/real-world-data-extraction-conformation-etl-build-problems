"""The pack's documents: the Lowry Creek Community Emissions Reduction Plan 2027 (PDF) and the district's point source
emission inventory guidance for the 2026 reporting year, with its data dictionary (PDF)."""
from reportlab import rl_config
rl_config.invariant = 1
from reportlab.lib import colors                                     # noqa: E402
from reportlab.lib.pagesizes import letter                           # noqa: E402
from reportlab.lib.styles import ParagraphStyle                      # noqa: E402
from reportlab.lib.units import inch                                 # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import pack as P    # noqa: E402
import world as W   # noqa: E402

BODY = ParagraphStyle("b", fontName="Times-Roman", fontSize=10.5, leading=13.6, spaceAfter=6)
SMALL = ParagraphStyle("sm", fontName="Times-Roman", fontSize=9.5, leading=12, spaceAfter=4)
HEAD = ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=11, leading=14, spaceBefore=8, spaceAfter=4)
TITLE = ParagraphStyle("t", fontName="Helvetica-Bold", fontSize=15, leading=19, spaceAfter=4)
SUB = ParagraphStyle("s", fontName="Helvetica", fontSize=9, leading=12, textColor=colors.HexColor("#444444"),
                     spaceAfter=10)
CELL = ParagraphStyle("c", fontName="Helvetica", fontSize=8.2, leading=10)
ORG = W.DISTRICT
GRID = TableStyle([("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8.4), ("FONT", (0, 1), (-1, -1), "Helvetica", 8.4),
                   ("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.black), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
                   ("TOPPADDING", (0, 0), (-1, -1), 2), ("VALIGN", (0, 0), (-1, -1), "TOP")])
ADDR = {"F01": "2200 Wexley Point Road", "F02": "1 Refinery Avenue", "F03": "880 Distillery Road",
        "F04": "15500 Sedge Hollow Road", "F05": "4917 Haskett Ridge Road", "F06": "1300 Aldric Boulevard",
        "F07": "60 Mill Race Lane", "F08": "500 University Drive", "F09": "7700 Briar Flats Road",
        "F10": "210 Cannery Row", "F11": "3150 Harrow Lane", "F12": "4410 Orchard Way", "F13": "4486 Orchard Way",
        "F14": "9 Quarry Lane"}


def _doc(path, title):
    d = SimpleDocTemplate(path, pagesize=letter, leftMargin=0.95 * inch, rightMargin=0.95 * inch,
                          topMargin=0.9 * inch, bottomMargin=0.9 * inch, title=title, author=ORG,
                          creator=ORG, producer=ORG, subject=title)

    def frame(c, d_):
        c.saveState()
        c.setFont("Helvetica", 8)
        c.setFillColor(colors.HexColor("#555555"))
        c.drawString(0.95 * inch, 0.55 * inch, "%s  |  %s" % (ORG, title))
        c.drawRightString(letter[0] - 0.95 * inch, 0.55 * inch, "Page %d" % d_.page)
        c.restoreState()
    return d, frame


def write_plan(path):
    title = W.PLAN
    d, frame = _doc(path, title)
    rows = [["Facility", "Facility no.", "Address", "What it is", "Gas BTU area"]]
    for code, name, what, area in W.FACILITIES:
        rows.append([Paragraph(name, CELL), W.FAC_NO[code], Paragraph(ADDR[code], CELL), Paragraph(what, CELL),
                     W.AREA_NAME[area]])
    t = Table(rows, hAlign="LEFT", colWidths=[1.75 * inch, 0.7 * inch, 1.45 * inch, 1.75 * inch, 0.85 * inch])
    t.setStyle(GRID)
    s = [Paragraph(title, TITLE),
         Paragraph("%s, Compliance Division. Draft for the Governing Board's meeting of 11 March 2027, prepared by %s, "
                   "Director of Compliance." % (ORG, W.PEOPLE["director"]), SUB),
         Paragraph("1. The corridor and its targets", HEAD),
         Paragraph("The Lowry Creek corridor runs from the Wexley Point riverfront through the refinery district to "
                   "the Orchard Way industrial park, with three schools and some 11,000 residents inside a mile of its "
                   "stacks. In December 2026 the community steering committee adopted the plan's targets: a fifth less "
                   "stationary-source NOx in the corridor by 2031, starting with agreements at the facilities that "
                   "emit the most.", BODY),
         Paragraph("2. The NOx reduction agreements", HEAD),
         Paragraph("2.1 In 2027 the District signs a NOx reduction agreement with each of the five facilities in the "
                   "corridor whose units subject to %s emitted the most oxides of nitrogen (NOx, expressed as NO2) in "
                   "calendar year 2026, in tons." % W.RULE, BODY),
         Paragraph("2.2 A facility's emissions are the sum over its %s units, the boilers, steam generators and "
                   "process heaters the District's permit list carries under the rule. Emergency standby engines "
                   "under Rule 4702 and the small units under Rule 4307 are outside the agreements." % W.RULE, BODY),
         Paragraph("2.3 The fourteen facilities in the corridor with %s units are listed in Appendix A, with the "
                   "facility numbers the District's permit records carry and the gas utility's BTU area each is served "
                   "from." % W.RULE, BODY),
         Paragraph("2.4 The agreements are signed by 1 April 2027. Each sets the facility's 2026 NOx from its %s units "
                   "as its baseline." % W.RULE, BODY),
         Paragraph("3. What the agreements require", HEAD),
         Paragraph("Each facility agrees to cut its %s units' NOx below its 2026 baseline by 20 per cent by 2029 and "
                   "by 35 per cent by 2031, by burner replacement, controls or operating limits of its choosing, and "
                   "the District checks progress each year against its point source inventory. The District's Clean "
                   "Air Grant program will offer each signatory up to half the capital cost of the measures it "
                   "chooses." % W.RULE, BODY),
         Paragraph("4. The plan's community tables", HEAD),
         Paragraph("4.1 Each facility's 2026 NOx from its %s units, from the District's 2026 point source inventory "
                   "(the inventory guidance for the 2026 reporting year sets out how each unit's emissions are "
                   "compiled)." % W.RULE, BODY),
         Paragraph("4.2 The natural gas %s delivered to each facility in calendar 2026, for the plan's fuel balance: "
                   "from the utility's commercial billing extract under the 2025 data sharing agreement, each billing "
                   "period's therms spread evenly over the days of its read period, from the day of its prior read to "
                   "the day before its current read." % W.UTILITY, BODY),
         Paragraph("4.3 Each facility's 2026 NOx from its emergency standby engines (guidance section 6), from the "
                   "Rule 4702 operating logs the facilities submitted and the District's inspection records.", BODY),
         Paragraph("5. Sources", HEAD),
         Paragraph("The continuous emissions monitoring export, the two source test databases, the facilities' "
                   "emission statements, the permit device list and the compliance event log, all as extracted from "
                   "the District's systems between 8 and 16 February 2027; the utility's billing extract of 8 February "
                   "2027 and its published monthly heat content; the facilities' 2026 Rule 4702 logs and the District's "
                   "engine inspection records. Questions on the inventory go to %s, Senior Air Quality Engineer."
                   % W.PEOPLE["engineer"], BODY),
         Paragraph("Appendix A. The corridor's facilities with %s units" % W.RULE, HEAD), t]
    d.build(s, onFirstPage=frame, onLaterPages=frame)


def write_guidance(path, n):
    title = "Point Source Emission Inventory Guidance, 2026 Reporting Year"
    d, frame = _doc(path, title)
    tiers = Table([["Engine emission tier", "NOx (g/bhp-hr)"]] + [[k, "%.2f" % v] for k, v in W.TIER_NOX.items()],
                  hAlign="LEFT", colWidths=[1.8 * inch, 1.3 * inch])
    tiers.setStyle(GRID)
    dd = [["File", "Contents"],
          [P.FILES["cems"], "One row per operating hour of each unit with a continuous emissions monitoring system "
           "(CEMS), 2026: facility_id, unit_id (the monitoring plan's unit), op_date and op_hour (local standard "
           "time), op_time, heat_input_mmbtu, nox_rate_lb_mmbtu, nox_rate_modc (01 measured, 12 substitute data), "
           "nox_mass_lb. {:,} rows.".format(n["cems"])],
          [P.FILES["tests_old"], "The earlier source test database, tests to December 2021: NOx in ppmvd at the "
           "reference oxygen and in lb/hr, the load as a share of the device's rating, the result against the permit "
           "limit. {} tests.".format(n["tests_old"])],
          [P.FILES["tests_new"], "The newer database, tests from January 2022: the same results with lb/MMBtu, the "
           "heat input at the test and the tester. {} tests.".format(n["tests_new"])],
          [P.FILES["statements"], "The facilities' annual emission statements, one row per device per month, "
           "2018 to 2026: fuel, quantity and its unit (MMSCF, THERMS or MMBTU) and the device's operating hours in "
           "the month. {:,} rows.".format(n["statements"])],
          [P.FILES["heat"], "{}'s published monthly heat content for each BTU area, January 2018 to February 2027: "
           "the average heat content of the gas it delivered to the area in the month, BTU_FACTOR in therms per CCF "
           "and HEAT_CONTENT_BTU_SCF the same in Btu/scf. {} rows.".format(W.UTILITY, n["heat"])],
          [P.FILES["permits"], "Every permitted combustion device at the fourteen facilities, as permitted in "
           "February 2027: the rule it falls under, its rating, fuel, NOx control, monitoring, the monitoring plan's "
           "unit id where it has a CEMS, its NOx limit (ppmvd at the reference oxygen), its test frequency, and for "
           "engines the make, model and emission tier. {} devices.".format(n["permits"])],
          [P.FILES["events"], "The District's compliance tracking log, 2018 to 2026: notifications, breakdowns, "
           "inspections, test scheduling and deferrals, outages reported under Rule 4702, equipment work, audits, "
           "changes of owner. Dates were entered month first until the 2021 system change. {} entries."
           .format(n["events"])],
          [P.FILES["billing"], "{}'s commercial billing extract (meter detail) as the utility delivered it: one line "
           "per meter per billing period, read from November 2025 to January 2027; READ_TYPE A for an actual read, E "
           "for an estimate; BTU_FACTOR is the heat content the bill is priced at, in therms per CCF (the utility's "
           "factor for the month in which its read closes); USAGE_THERMS is the usage billed for the period. Accounts are by service address. {} lines.".format(W.UTILITY, n["billing"])],
          [P.FILES["engine_logs"], "The facilities' 2026 Rule 4702 operating logs as each facility submitted it, one "
           "sheet per facility (sheet name the facility number). {:,} log entries.".format(n["engine_logs"])],
          [P.FILES["inspections"], "Each emergency engine's non-resettable hour meter as the District's inspector "
           "read it, November 2025 to February 2027. {} readings.".format(n["inspections"])],
          [P.FILES["no2"], "Hourly NO2 at the corridor's three community monitors, 2026 (local standard time; AN is "
           "a machine malfunction). {:,} rows.".format(n["no2"])],
          [P.FILES["onroad"], "The District's 2026 on-road NOx estimate for the corridor's road links (MOVES, county "
           "scale). {} links.".format(n["onroad"])]]
    dd = [[Paragraph(a, CELL), Paragraph(b, CELL)] for a, b in dd]
    dt_ = Table(dd, hAlign="LEFT", colWidths=[2.2 * inch, 4.3 * inch])
    dt_.setStyle(GRID)
    s = [Paragraph(title, TITLE),
         Paragraph("%s, Engineering Division. Revised 17 February 2027 for the 2026 inventory, with the extracts it is "
                   "compiled from (section 7)." % ORG, SUB),
         Paragraph("1. Scope", HEAD),
         Paragraph("The District compiles each year's point source inventory from continuous monitoring data, source "
                   "test results and the emission statements facilities file under Rule 1160. This guidance covers "
                   "NOx from the boilers, steam generators and process heaters under %s and from emergency standby "
                   "engines under Rule 4702." % W.RULE, BODY),
         Paragraph("2. Units with a continuous emissions monitoring system", HEAD),
         Paragraph("A unit's annual NOx is the sum of the hourly NOx mass its monitoring system reports for the "
                   "year's operating hours, substitute data hours included as the monitoring plan reports them. Hours "
                   "are in local standard time throughout the year.", BODY),
         Paragraph("3. Units without a continuous emissions monitoring system", HEAD),
         Paragraph("A unit's annual NOx is the NOx it emitted over the year's operation, in pounds, from its heat "
                   "input and its NOx emission rate in lb/MMBtu. %s section 6.3 requires each unit without a "
                   "monitoring system to be source tested for NOx every 12 months, or every 24 months where the "
                   "permit allows a reduced frequency; the District's two source test databases hold the results."
                   % W.RULE, BODY),
         Paragraph("4. Heat input", HEAD),
         Paragraph("Heat input comes from the emission statements: therms divided by 10; MMBtu as reported; each "
                   "MMSCF of natural gas at the heat content %s reports for the facility's BTU area in that month, in "
                   "Btu/scf (the plan's Appendix A lists each facility's BTU area)." % W.UTILITY, BODY),
         Paragraph("5. Source test results", HEAD),
         Paragraph("A test's result is the average of its runs, normally three. lb/MMBtu follows EPA Method 19: E = C "
                   "x 1.194 x 10<super>-7</super> x Fd x 20.9 / (20.9 - %O2<sub>ref</sub>), with C in ppmvd at the "
                   "reference oxygen and Fd 8,710 dscf/MMBtu for natural gas. It also equals the test's lb/hr over its "
                   "heat input (the device's rating times the test's load).", BODY),
         Paragraph("6. Emergency standby engines (Rule 4702)", HEAD),
         Paragraph("An engine's annual NOx is the time it ran in the year, in hours, times its rated brake horsepower "
                   "times a load factor of 0.74 times the NOx factor for its emission tier, divided by 453.6 g/lb. The "
                   "facilities' Rule 4702 logs record each test, maintenance and emergency run; the District reads "
                   "each engine's non-resettable hour meter, which also counts each start's warm-up and cool-down, at "
                   "its inspections.", BODY),
         tiers, Spacer(1, 6),
         Paragraph("7. Files", HEAD), dt_]
    d.build(s, onFirstPage=frame, onLaterPages=frame)
