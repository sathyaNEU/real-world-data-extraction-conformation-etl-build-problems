"""The pack's documents: the Authority's licence conditions for the Warrenby terminal, its return protocol for
petroleum storage and loading premises, and VRU-1's 2026 annual emission test report."""
from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                      # noqa: E402
from reportlab.lib.pagesizes import A4                                                # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                       # noqa: E402
from reportlab.lib.units import mm                                                    # noqa: E402
from reportlab.pdfbase import pdfmetrics                                              # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                          # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import world as W   # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("LiberationSerif", "Regular"), ("LiberationSerif-Bold", "Bold"), ("LiberationSans", "Regular"),
              ("LiberationSans-Bold", "Bold"), ("LiberationSans-Italic", "Italic")):
    try:
        pdfmetrics.getFont(nm)
    except KeyError:
        pdfmetrics.registerFont(TTFont(nm, FONT_DIR + nm.split("-")[0] + "-" + f + ".ttf"))
INK = colors.HexColor("#1b1d1f")
GREY = colors.HexColor("#5b6066")
TEAL = colors.HexColor("#0f4c5c")
BODY = ParagraphStyle("body", fontName="LiberationSerif", fontSize=10.2, leading=13.8, textColor=INK, spaceAfter=5)
NUM = ParagraphStyle("num", parent=BODY, leftIndent=26, firstLineIndent=-26)
H1 = ParagraphStyle("h1", fontName="LiberationSans-Bold", fontSize=14, leading=18, textColor=TEAL, spaceAfter=2)
SUB = ParagraphStyle("sub", fontName="LiberationSans", fontSize=9.6, leading=12.5, textColor=GREY, spaceAfter=9)
H2 = ParagraphStyle("h2", fontName="LiberationSans-Bold", fontSize=10.4, leading=14, textColor=INK, spaceBefore=7,
                    spaceAfter=3)
CELL = ParagraphStyle("cell", fontName="LiberationSans", fontSize=8.6, leading=10.8, textColor=INK)
CELLB = ParagraphStyle("cellb", parent=CELL, fontName="LiberationSans-Bold")
SMALL = ParagraphStyle("small", fontName="LiberationSans", fontSize=8.2, leading=10.5, textColor=GREY)


def _doc(path, title, author, footer):
    def frame(canvas, doc):
        canvas.saveState()
        canvas.setFont("LiberationSans", 7.4)
        canvas.setFillColor(GREY)
        canvas.drawString(20 * mm, 12 * mm, footer)
        canvas.drawRightString(A4[0] - 20 * mm, 12 * mm, "Page %d" % doc.page)
        canvas.restoreState()
    d = SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm,
                          bottomMargin=20 * mm, title=title, author=author, subject="", creator="", producer="")
    return d, frame


def _table(rows, widths):
    data = [[Paragraph(str(c), CELLB if i == 0 else CELL) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9aa0a6")),
                           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e6ecee")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 4),
                           ("RIGHTPADDING", (0, 0), (-1, -1), 4)]))
    return t


# ------------------------------------------------------------------------------------------------- the licence
def write_licence(path):
    doc, frame = _doc(path, "Environment Protection Licence 20514", W.AUTHORITY,
                      "%s  |  Environment Protection Licence 20514, Brennock Fuels Pty Ltd  |  Variation 4, 3 March 2025"
                      % W.AUTHORITY)
    s = [Paragraph("Environment Protection Licence 20514", H1),
         Paragraph("%s. Licensee: Brennock Fuels Pty Ltd (ABN 41 118 626 035). Premises: Warrenby terminal, 14 Wharf "
                   "Road, Port Warrenby. Variation 4, issued 3 March 2025; anniversary date 1 July." % W.AUTHORITY, SUB)]
    p = lambda n, t: s.append(Paragraph("<b>%s</b>&nbsp;&nbsp;%s" % (n, t), NUM))
    s.append(Paragraph("1. Scheduled activities", H2))
    p("1.1", "Petroleum products storage: bulk storage of unleaded petrol, premium unleaded petrol and diesel in five "
             "tanks (TK-1 to TK-5), receipt by ship at No 1 berth, and loading into road tankers at bays 1 to 5.")
    p("1.2", "Scale: storage capacity above 20,000 kilolitres.")
    s.append(Paragraph("2. Operating conditions", H2))
    p("O1", "Petrol may be loaded into road tankers at the premises only at bays 1, 2 and 3, with the tanker's vapour "
            "coupling connected to vapour recovery unit VRU-1, and only while VRU-1 is in service. The loading control "
            "system must stop petrol loading at those bays whenever VRU-1 is stopped.")
    p("O2", "The VOC concentration at the VRU-1 stack must not exceed 10 grams per cubic metre as a 15-minute average, "
            "measured at 0 degrees Celsius and 101.3 kilopascals.")
    p("O3", "Bays 4 and 5 are distillate loading bays and are not connected to VRU-1.")
    s.append(Paragraph("3. Load limits", H2))
    p("L1", "The mass of volatile organic compounds released to air from product loading at the premises must not "
            "exceed 20 tonnes in any calendar year.")
    s.append(Paragraph("4. Monitoring", H2))
    p("M1", "The licensee must operate the continuous emission monitor on the VRU-1 stack approved by the Authority on "
            "19 November 2019 (as replaced from time to time with the Authority's approval), record the VOC mass rate "
            "for every 15-minute interval and keep the records for four years.")
    s.append(Paragraph("5. Reporting", H2))
    p("R1", "The licensee must lodge an annual return for each calendar year by 31 January of the following year, "
            "through the Authority's online portal, in the file layout of the Authority's Return Protocol for "
            "Petroleum Products Storage and Loading Premises, reporting the release of VOC from product loading at "
            "each loading point in each quarter and from each storage tank over the year, worked as that protocol "
            "requires.")
    p("R2", "Where a load limit in condition L1 was exceeded in the year, the return must be accompanied by a "
            "covering note stating the year's release and the amount by which the limit was exceeded.")
    s.append(Paragraph("6. Dictionary", H2))
    p("D1", "<b>Calendar year</b> means 1 January to 31 December in the premises' local time.")
    p("D2", "<b>Product loading</b> means the loading of petroleum product from the premises' storage into road "
            "tankers at the premises' loading bays.")
    p("D3", "<b>Volatile organic compounds (VOC)</b> means hydrocarbon vapour, reported as its own mass.")
    s.append(Spacer(1, 6))
    s.append(Paragraph("Issued under the Protection of the Environment Act by a delegate of the Authority, "
                       "Licensing and Approvals, Coastal Region.", SMALL))
    doc.build(s, onFirstPage=frame, onLaterPages=frame)


# ------------------------------------------------------------------------------------------------- the protocol
def write_protocol(path):
    doc, frame = _doc(path, "Return Protocol: Petroleum Products Storage and Loading Premises", W.AUTHORITY,
                      "%s  |  Return Protocol: Petroleum Products Storage and Loading Premises  |  2026 edition, "
                      "published 2 February 2026" % W.AUTHORITY)
    s = [Paragraph("Return Protocol: Petroleum Products Storage and Loading Premises", H1),
         Paragraph("%s. 2026 edition, published 2 February 2026, for returns on calendar years from 2026. Replaces the "
                   "2021 edition." % W.AUTHORITY, SUB)]
    p = lambda n, t: s.append(Paragraph("<b>%s</b>&nbsp;&nbsp;%s" % (n, t), NUM))
    s.append(Paragraph("1. Application", H2))
    p("1.1", "This protocol applies to every licensed premises that stores petroleum products and loads them into road "
             "tankers, rail tank cars or ships, and sets out what the annual return reports and the file it is lodged "
             "in.")
    s.append(Paragraph("2. Definitions", H2))
    p("2.1", "<b>Reporting year:</b> the calendar year, in the premises' local time. A quarter is three calendar "
             "months of the reporting year (Q1 January to March).")
    p("2.2", "<b>Loading point:</b> each bay or berth where product is loaded. Where bays send the vapour displaced "
             "during loading to a vapour recovery or vapour combustion unit, that unit's stack is the loading point "
             "for those bays.")
    p("2.3", "<b>Release:</b> the mass of volatile organic compounds discharged to air at a loading point, or from a "
             "storage tank, in the period.")
    s.append(Paragraph("3. Measured releases", H2))
    p("3.1", "The release at a loading point that is a unit's stack fitted with a continuous emission monitor approved "
             "by the Authority is the sum, over the 15-minute intervals that begin in the period, of the monitor's VOC "
             "mass rate times the interval.")
    p("3.2", "An interval without a valid reading (a calibration check or a fault) takes the mean of the valid "
             "readings in the hour before it and the hour after it. An interval in which the unit was stopped, with "
             "loading at its bays stopped by interlock, releases nothing.")
    s.append(Paragraph("4. Estimated releases", H2))
    p("4.1", "A release that is not measured is estimated by the licensee by a recognised estimation method, using "
             "the liquid properties in this section.")
    p("4.2", "The true vapour pressure of a liquid at a liquid temperature T in degrees Celsius is given by ln(P / kPa) "
             "= A - B / (T + 273.15), with A and B from Table 1. Its vapour's molecular weight is in Table 2.")
    p("4.3", "Petrol is supplied in a summer grade from 1 November to 31 March and a winter grade from 1 April to 31 "
             "October. A load takes the grade season of the month in which it is loaded.")
    p("4.4", "The liquid temperature and volume used in an estimate are the temperature and the observed volume (at "
             "that temperature) the loading meter records for the load.")
    s.append(_table([["Table 1. Liquid", "A", "B"],
                     ["Petrol, summer grade", "13.687", "2952.8"],
                     ["Petrol, winter grade", "13.642", "2891.9"],
                     ["Aviation gasoline", "13.904", "3150.0"],
                     ["Kerosene and jet A-1", "16.800", "5100.0"],
                     ["Diesel", "14.032", "4948.3"]], [80 * mm, 30 * mm, 30 * mm]))
    s.append(Spacer(1, 5))
    s.append(_table([["Table 2. Vapour of", "Molecular weight (kg/kmol)"],
                     ["Petrol, summer grade", "67"], ["Petrol, winter grade", "65"], ["Aviation gasoline", "69"],
                     ["Kerosene and jet A-1", "130"], ["Diesel", "130"]], [80 * mm, 60 * mm]))
    s.append(Paragraph("5. Storage tanks", H2))
    p("5.1", "The release from a storage tank in a period is its standing loss plus its working loss.")
    p("5.2", "Standing loss: for each day of the period, the Table 3 rate for the tank's construction, rim seal and "
             "vents times the tank's diameter in metres. A day takes the rate for the construction, seal and vents the "
             "tank had at the start of that day.")
    p("5.3", "Working loss: the Table 4 rate times the megalitres the tank received from ships in the period, as shore "
             "received at 15 degrees Celsius.")
    s.append(_table([["Table 3. Construction, rim seal and vents", "kg per metre of diameter per day"],
                     ["External floating roof, primary seal only", "0.52"],
                     ["External floating roof, primary and rim-mounted secondary", "0.21"],
                     ["Internal floating roof, primary seal only", "0.31"],
                     ["Internal floating roof, primary and rim-mounted secondary", "0.12"],
                     ["Fixed roof, distillate service, open vents", "0.0175"],
                     ["Fixed roof, distillate service, pressure-vacuum vents", "0.0105"]], [100 * mm, 60 * mm]))
    s.append(Spacer(1, 5))
    s.append(_table([["Table 4. Service", "kg per megalitre received"],
                     ["Petrol, floating roof", "6.4"], ["Distillate, fixed roof", "0.9"]], [100 * mm, 60 * mm]))
    s.append(Paragraph("6. The return file", H2))
    p("6.1", "The return is lodged as one comma-separated file, one row per figure, with a header row naming the "
             "columns licence_no, year, section, point_id, period, substance, quantity and unit.")
    p("6.2", "section is LOADING for a loading point and TANKS for a storage tank. point_id is the loading point or "
             "tank as the licence names it (a unit's stack by the unit's identifier, a bay as BAY- and its number, a "
             "tank by its tank number). period is Q1, Q2, Q3 or Q4 for a loading point's quarter and YEAR for a "
             "tank's year. substance is VOC.")
    p("6.3", "quantity is in tonnes (unit t) for loading points and in kilograms (unit kg) for storage tanks.")
    s.append(Spacer(1, 6))
    s.append(Paragraph("Enquiries: Industry Reporting, %s, Coastal Region." % W.AUTHORITY, SMALL))
    doc.build(s, onFirstPage=frame, onLaterPages=frame)


# ------------------------------------------------------------------------------------------------- the stack test
def write_stack_test(path):
    doc, frame = _doc(path, "VRU-1 annual emission test 2026", "Brightwater Emission Testing",
                      "Brightwater Emission Testing  |  Report BET-26-0817  |  Brennock Fuels, Warrenby terminal, VRU-1")
    s = [Paragraph("VRU-1 Annual Emission Test, 2026", H1),
         Paragraph("Brightwater Emission Testing, report BET-26-0817, issued 2 September 2026. Client: Brennock Fuels "
                   "Pty Ltd, Warrenby terminal. Test dates 18 and 19 August 2026.", SUB)]
    p = lambda n, t: s.append(Paragraph("<b>%s</b>&nbsp;&nbsp;%s" % (n, t), NUM))
    s.append(Paragraph("1. Purpose", H2))
    p("1.1", "Annual compliance test of vapour recovery unit VRU-1 against licence condition O2, and a check of the "
             "continuous emission monitor against the reference method during the same runs.")
    s.append(Paragraph("2. Results", H2))
    s.append(_table([["Run", "Start", "Duration", "Petrol loaded (kL)", "Inlet VOC (g/m3)", "Outlet VOC (g/m3)",
                      "Removal (%)", "CEMS against reference"],
                     ["1", "18/08/2026 07:10", "60 min", "28.4", "612", "6.4", "98.95", "+3.1%"],
                     ["2", "18/08/2026 09:35", "60 min", "24.1", "598", "6.9", "98.85", "-2.4%"],
                     ["3", "19/08/2026 07:05", "60 min", "31.2", "631", "6.1", "99.03", "+1.8%"]],
                    [10 * mm, 27 * mm, 15 * mm, 20 * mm, 20 * mm, 20 * mm, 17 * mm, 22 * mm]))
    s.append(Spacer(1, 5))
    p("2.1", "The mean outlet concentration was 6.5 g/m3 against the licence limit of 10 g/m3 (O2): compliant.")
    p("2.2", "The CEMS agreed with the reference method within plus or minus 10 per cent on every run: the monitor "
             "remains fit for its approval.")
    s.append(Paragraph("3. Method", H2))
    p("3.1", "Reference concentrations by flame ionisation (as propane), stack flow by pitot traverse, three one-hour "
             "runs during normal loading.")
    s.append(Spacer(1, 6))
    s.append(Paragraph("Tested by M. Ellery (team leader). Reviewed by S. Nakamura, Brightwater Emission Testing.",
                       SMALL))
    doc.build(s, onFirstPage=frame, onLaterPages=frame)
