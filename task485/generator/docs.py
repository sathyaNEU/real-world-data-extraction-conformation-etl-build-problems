"""The pack's documents: the Directorate's note on the 2027 Order's schedule, its 2026 inventory guidance, the two
scrubber vendors' performance guarantee schedules as attached to the permits, and the two test laboratories' 2026
summary reports."""
import datetime as dt

import numpy as np
import reportlab.rl_config
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import pack as PK
import tests as TS
import world as W

reportlab.rl_config.invariant = 1
STY = getSampleStyleSheet()
BODY = ParagraphStyle("b", parent=STY["BodyText"], fontName="Helvetica", fontSize=9.5, leading=12.8, spaceAfter=6)
SMALL = ParagraphStyle("s", parent=BODY, fontSize=8, leading=10)
H = ParagraphStyle("h", parent=STY["Heading2"], fontName="Helvetica-Bold", fontSize=11, spaceBefore=8, spaceAfter=4)
T = ParagraphStyle("t", parent=STY["Title"], fontName="Helvetica-Bold", fontSize=14, spaceAfter=10, alignment=0)
CAP = ParagraphStyle("c", parent=BODY, fontName="Helvetica-Oblique", fontSize=8, leading=10, spaceBefore=2)
MIN = "Ministry of the Environment"
AQD = "Air Quality Directorate"
KELLFOLD = "Kellfold Process Systems"
HOLM = "Lundsett Absorber Engineering"


def _pdf(path, title, story, author, org, size=A4):
    doc = SimpleDocTemplate(path, pagesize=size, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=17 * mm,
                            bottomMargin=17 * mm, title=title, author=author, creator=org, subject=title, producer=org)

    def footer(c, d):
        c.saveState()
        c.setFont("Helvetica", 7.5)
        c.drawString(18 * mm, 10 * mm, org + "  |  " + title)
        c.drawRightString(size[0] - 18 * mm, 10 * mm, "%d" % d.page)
        c.restoreState()

    doc.build(story, onFirstPage=footer, onLaterPages=footer)


def P(text, style=BODY):
    return Paragraph(text, style)


def _table(rows, widths=None, size=8.5, left=1):
    t = Table(rows, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", size), ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", size),
                           ("LINEBELOW", (0, 0), (-1, 0), 0.5, colors.black), ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
                           ("ALIGN", (left, 1), (-1, -1), "RIGHT"), ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                           ("TOPPADDING", (0, 0), (-1, -1), 2)]))
    return t


def _h(text, size=8):
    return Paragraph(text, ParagraphStyle("th", parent=SMALL, fontName="Helvetica-Bold", fontSize=size,
                                          leading=size + 1.5, alignment=2))


def _hl(text, size=8):
    return Paragraph(text, ParagraphStyle("thl", parent=SMALL, fontName="Helvetica-Bold", fontSize=size,
                                          leading=size + 1.5, alignment=0))


def _c(text, size=7.5):
    return Paragraph(text, ParagraphStyle("cell", parent=SMALL, fontName="Helvetica", fontSize=size,
                                          leading=size + 1.5, alignment=0))


def long_date(d):
    return "%d %s %d" % (d.day, d.strftime("%B"), d.year)


def order_note(path):
    s = [P("The Sulphur Dioxide (Northern Priority Area) Order 2027: the schedule of listed boilers", T),
         P("Note to the Minister's Private Office. %s, %s. Reference AQD/ORD/2027/01, 8 February 2027." % (AQD, MIN),
           SMALL),
         P("1. The Order", H),
         P("Section 14 of the Clean Air Act 2011 lets the Minister list, by order, the permitted combustion units in a "
           "priority area whose sulphur dioxide over a year reached a line the order sets. The 2027 Order sets the "
           "line for the Northern Priority Area at 250 tonnes. The Directorate puts the schedule of listed units to "
           "the Minister by 26 February 2027, each unit with its 2026 figure, and the Order is laid in March."),
         P("2. The test", H),
         P("A boiler is listed if its sulphur dioxide leaving the stack over calendar 2026, compiled under the "
           "Directorate's guidance for the 2026 inventory year, was 250 tonnes or more."),
         P("3. The units", H),
         P("The Order's units are the 18 coal boilers on the Northern Priority Area's permit register at 31 December "
           "2026, at 16 sites. Where a site holds two permitted boilers, each boiler is a unit and is tested on its "
           "own figure. Gas-fired plant on the same sites is outside the Order, as is gas oil fired at start-up."),
         P("4. What listing brings", H),
         P("A listed boiler must have continuous emission monitoring for sulphur dioxide in service by 1 October "
           "2027. By 1 October 2029 it must either upgrade its abatement plant to a removal the Directorate approves "
           "or fire only coal of not more than 0.8 per cent sulphur as received. No boiler in the Area has continuous "
           "monitoring today; each is tested once a year under permit condition C11."),
         P("5. Records", H),
         P("The fourth-quarter returns were due on 31 January 2027 and all 18 are in. The suppliers' statements of "
           "coal delivered to the Area's permitted sites in 2026 were collated by the Directorate in January."),
         Spacer(1, 10),
         P("Maria Burgess<br/>Head of Industrial Emissions, %s" % AQD)]
    _pdf(path, "The Sulphur Dioxide (Northern Priority Area) Order 2027: the schedule of listed boilers", s,
         "Maria Burgess", AQD)


def guidance(path):
    s = [P("Annual sulphur dioxide inventory of permitted coal-fired boilers", T),
         P("Guidance for the 2026 inventory year. %s, %s. Reference AQD/INV/2026/03, issued 2 November 2026; replaces "
           "the guidance for the 2025 inventory year." % (AQD, MIN), SMALL),
         P("1. Purpose and scope", H),
         P("1.1 This guidance sets how the Directorate compiles the annual inventory of sulphur dioxide from the "
           "permitted coal-fired boilers of the Northern Priority Area, on which the Minister's orders under section "
           "14 of the Clean Air Act 2011 and the Area's lines in the national emissions inventory both draw."),
         P("1.2 It applies to every boiler on the Area's permit register that fires coal. Gas-fired plant on the same "
           "sites, and gas oil fired at start-up, are outside it."),
         P("2. The inventory year", H),
         P("2.1 The 2026 inventory year is calendar 2026: the coal a boiler fired from 1 January to 31 December 2026."),
         P("3. The measure", H),
         P("3.1 A boiler's sulphur dioxide for the year is the sulphur dioxide leaving its stack: the sulphur dioxide "
           "formed from the sulphur in the coal it fired, less the sulphur retained in its ash, less the sulphur "
           "dioxide its abatement plant removed over the year."),
         P("3.2 Sulphur converts to sulphur dioxide at 64.066 tonnes for every 32.065 tonnes of sulphur."),
         P("3.3 Each boiler is compiled on its own, including a boiler that shares a site and a coal yard with "
           "another; each has its own abatement plant."),
         P("4. Coal fired and its sulphur", H),
         P("4.1 The coal a boiler fired is the coal burned that its operator reports for it in the four quarterly "
           "returns for the year under permit condition C7."),
         P("4.2 The sulphur of a boiler's coal is the total sulphur, as received, of the coal delivered to its site "
           "in the inventory year: the average of the delivered lots' analyses, each weighted by the tonnes "
           "delivered. A delivery belongs to the year in which it was received at the site."),
         P("4.3 Where two boilers share a site's coal yard, both take the site's figure."),
         P("4.4 A certificate a supplier's laboratory has re-issued is read at its latest issue."),
         P("5. Sulphur retained in ash", H),
         P("5.1 The share of the sulphur fired that a boiler's bottom ash and fly ash retain is the permit register's "
           "figure for the boiler, set at permitting from the boiler's type."),
         P("6. Reporting", H),
         P("6.1 The inventory states each boiler's sulphur dioxide in tonnes. A comparison with a line in an order is "
           "made on the unrounded figure."),
         P("6.2 The Directorate publishes the inventory with the Area's lines in the national emissions inventory in "
           "the autumn after the year.")]
    _pdf(path, "Annual sulphur dioxide inventory of permitted coal-fired boilers: guidance for 2026", s, AQD, AQD)


def guarantees(path, w):
    rng = np.random.default_rng(W.SEED + 91)
    vend = w.vendor
    rows = {KELLFOLD: [], HOLM: []}
    for b in w.B:
        v = vend[b["id"]]
        flow = int(np.round(b["mwth"] * 3600 * TS.VFG6 * rng.uniform(1.04, 1.12), -3))
        mix = b["mix"][0][1]
        s_des = sum(sh * W.SUPPLIERS[s]["s"] for s, sh in mix.items()) * rng.uniform(1.10, 1.30)
        gcv = sum(sh * W.SUPPLIERS[s]["gcv"] for s, sh in mix.items())
        inlet = int(np.round(s_des / 100 * 2 * (1 - b["ash_ret"]) / gcv * 1e6 / TS.VFG6, -1))
        outlet = int(np.round(inlet * (1 - b["design"]), 0))
        lg = float(np.round(rng.uniform(8.5, 15.5), 1))
        dp = float(np.round(rng.uniform(1.1, 1.7), 2))
        kw = int(np.round(b["mwth"] * rng.uniform(8.5, 11.5), -1))
        water = float(np.round(b["mwth"] * rng.uniform(0.16, 0.24), 1))
        rows[v].append([PK.PERMIT[b["id"]], _c(w.sites[b["site"]]["firm"]), PK.unit_label(b["id"]), "{:,}".format(flow),
                        "{:,}".format(inlet), "%.1f" % (100 * b["design"]), "{:,}".format(outlet), "%.2f" % b["ratio"],
                        "%.1f" % lg, "%.2f" % dp, "{:,}".format(kw), "%.1f" % water])
    head = [_hl("Permit"), _hl("Site"), _hl("Unit"), _h("Design flue gas (Nm3/h)"), _h("Design inlet SO2 (mg/Nm3)"),
            _h("SO2 removal (%)"), _h("Outlet SO2 (mg/Nm3)"), _h("Limestone (mol CaCO3 / mol SO2 removed)"),
            _h("L/G (l/Nm3)"), _h("Pressure drop (kPa)"), _h("Absorbed power (kW)"), _h("Make-up water (m3/h)")]
    widths = [21 * mm, 42 * mm, 19 * mm, 21 * mm, 21 * mm, 16 * mm, 18 * mm, 27 * mm, 14 * mm, 17 * mm, 18 * mm,
              19 * mm]
    s = [P("Performance guarantee schedules: wet limestone absorbers", T),
         P("Northern Priority Area retrofit programme, 2019 to 2023. The two suppliers' guarantee schedules as attached "
           "to each boiler's permit on the absorber's acceptance; copied from the permit files by the %s, %s, 14 March "
           "2024." % (AQD, MIN), SMALL),
         P("Schedule 4: %s" % KELLFOLD, H),
         P("4.1 The guarantees below hold at the boiler's rated thermal input on the design coal, for limestone of not "
           "less than 92 per cent calcium carbonate as delivered and 90 per cent passing 63 microns. Flue gas volumes and concentrations are dry, at "
           "6 per cent oxygen. The limestone figure is the absorber's operating stoichiometry under its pH control: the "
           "moles of calcium carbonate fed for each mole of sulphur dioxide removed."),
         P("4.2 Mist eliminator carry-over not more than 50 mg/Nm3. Each guarantee was demonstrated at the acceptance "
           "test within the tolerances of Schedule 6."),
         _table([head] + rows[KELLFOLD], widths, size=7.5, left=3),
         P("Signed for %s: Brenda Cook, Performance Engineer." % KELLFOLD, CAP),
         P("Schedule C: %s" % HOLM, H),
         P("C1. Guarantee conditions: the boiler at its rated input on the design coal; limestone of 92 per cent "
           "calcium carbonate or more as delivered, ground to 90 per cent passing 63 microns. Gas volumes and concentrations dry at 6 per cent oxygen. The limestone stoichiometry "
           "is stated in moles of calcium carbonate per mole of sulphur dioxide removed, as held by the absorber's "
           "slurry pH set point in normal operation."),
         P("C2. Droplet carry-over at the mist eliminator outlet not more than 50 mg/Nm3."),
         _table([head] + rows[HOLM], widths, size=7.5, left=3),
         P("For %s: Process Guarantees." % HOLM, CAP)]
    _pdf(path, "Performance guarantee schedules: wet limestone absorbers", s, AQD, AQD, size=landscape(A4))


def test_report(path, w, lab):
    tests = sorted([x for x in w.tests if x["lab"] == lab], key=lambda x: x["day"])
    o2 = TS.LABS[lab]
    north = lab.startswith("Iverstow")
    last = W.day(max(x["day"] for x in tests))
    issued = last + dt.timedelta(days=17 if north else 24)
    prefix = "IET/26/" if north else "JST-2026-"
    rows1 = [[_hl("Report"), _hl("Site"), _hl("Unit"), _hl("Permit"), _h("Test date"), _h("Load (% of rating)"),
              _h("Duration (h)"), _h("Oxygen (% dry)")]]
    rows2 = [[_hl("Report"), _h("Flue gas flow (Nm3/h)"), _h("SO2 absorber inlet (mg/Nm3)"),
              _h("SO2 stack (mg/Nm3)"), _h("SO2 removal (%)")]]
    for i, x in enumerate(tests, start=1):
        rep = "%s%03d" % (prefix, 40 + 3 * i) if north else "%s%02d" % (prefix, 11 + 2 * i)
        rows1.append([rep, _c(w.sites[x["site"]]["firm"]), PK.unit_label(x["boiler"]), PK.PERMIT[x["boiler"]],
                      W.day(x["day"]).strftime("%d %b %Y"), "%.0f" % x["load"], "%.1f" % x["hours"], "%.1f" % x["o2"]])
        rows2.append([rep, "{:,.0f}".format(x["flow"]), "{:,.0f}".format(x["so2_in"]), "{:,.0f}".format(x["so2_out"]),
                      "%.1f" % x["removal"]])
    if north:
        title = "Annual abatement performance tests, 2026: summary of results"
        intro = ("Iverstow Emission Testing, accredited stack emission laboratory no. 0417. Summary of the 2026 "
                 "annual tests of wet limestone absorbers under permit condition C11, Northern Priority Area. Issued "
                 "%s." % long_date(issued))
        method = ("Each test was run by arrangement with the operator, with the boiler at not less than 60 per cent "
                  "of its rating. Sulphur dioxide was sampled simultaneously at the absorber "
                  "inlet and in the stack by absorption in hydrogen peroxide, analysed by ion chromatography, as three "
                  "or more runs of 60 minutes; flue gas flow by pitot traverse in the stack. Concentrations and flows "
                  "are dry and are stated at %.0f per cent oxygen. The removal is one minus the ratio of the stack to "
                  "the inlet concentration over the runs. Expanded uncertainty of a removal: 0.4 percentage points." % o2)
        sign = "Timothy Peterson, Technical Manager"
    else:
        title = "Stack testing programme 2026: FGD performance tests, results summary"
        intro = ("Jarrness Stack Testing Ltd, accreditation 1185. Results of the 2026 periodic performance tests of "
                 "the flue gas desulphurisation absorbers the laboratory tested for operators in the Northern Priority "
                 "Area (permit condition C11). Issued %s." % long_date(issued))
        method = ("Tests were booked with the operator and run at not less than 60 per cent of boiler rating, with "
                  "paired sampling of sulphur dioxide before the absorber and at the stack (hydrogen peroxide "
                  "absorption, ion chromatography; three runs of one hour or more) and stack flow by pitot traverse. "
                  "All concentrations and flows are given dry and referenced to %.0f per cent oxygen. Removal is "
                  "calculated from the paired concentrations. Uncertainty of a removal: plus or minus 0.4 percentage "
                  "points at 95 per cent confidence." % o2)
        sign = "Laboratory Manager, for Jarrness Stack Testing Ltd"
    s = [P(title, T), P(intro, SMALL), P("1. Method", H), P(method), P("2. Test conditions", H),
         _table(rows1, [21 * mm, 40 * mm, 19 * mm, 21 * mm, 19 * mm, 17 * mm, 16 * mm, 17 * mm], size=7.5, left=4),
         P("Table 1. The tests in date order.", CAP), Spacer(1, 4), P("3. Results", H),
         _table(rows2, [24 * mm, 30 * mm, 32 * mm, 26 * mm, 22 * mm], size=7.5),
         P("Table 2. Results at %.0f per cent oxygen, dry. Each result is the mean of the test's runs." % o2, CAP),
         Spacer(1, 8), P("Signed: %s" % sign, SMALL)]
    _pdf(path, title, s, sign.split(",")[0], lab)
    return issued
