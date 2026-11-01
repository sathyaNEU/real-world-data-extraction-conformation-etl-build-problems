"""The pack's documents and workbooks: the Capital Committee's siting charter, the supplier's power content label,
the agency's published rates for 2025 and 2024."""
from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                      # noqa: E402
from reportlab.lib.pagesizes import LETTER                                            # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                       # noqa: E402
from reportlab.lib.units import inch                                                  # noqa: E402
from reportlab.pdfbase import pdfmetrics                                              # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                          # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import pack as P    # noqa: E402
import world as W   # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("LiberationSerif", "Regular"), ("LiberationSerif-Bold", "Bold"), ("LiberationSerif-Italic", "Italic"),
              ("LiberationSans", "Regular"), ("LiberationSans-Bold", "Bold")):
    try:
        pdfmetrics.getFont(nm)
    except KeyError:
        pdfmetrics.registerFont(TTFont(nm, FONT_DIR + nm.split("-")[0] + "-" + f + ".ttf"))
INK = colors.HexColor("#1d1f21")
GREY = colors.HexColor("#5a5f66")
GREEN = colors.HexColor("#2f5d3a")
BODY = ParagraphStyle("body", fontName="LiberationSerif", fontSize=10.5, leading=14.5, textColor=INK, spaceAfter=6)
NUM = ParagraphStyle("num", parent=BODY, leftIndent=30, firstLineIndent=-30)
H1 = ParagraphStyle("h1", fontName="LiberationSans-Bold", fontSize=14, leading=18, textColor=GREEN, spaceAfter=2)
H1S = ParagraphStyle("h1s", fontName="LiberationSans", fontSize=10, leading=13, textColor=GREY, spaceAfter=10)
H2 = ParagraphStyle("h2", fontName="LiberationSans-Bold", fontSize=10.5, leading=14, textColor=INK, spaceBefore=7, spaceAfter=3)
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


# ---------------------------------------------------------------------------------------------- the charter
def write_charter(path):
    doc, frame = _doc(path, "2027 On-Site Solar Pilot: Siting Charter", W.ORG,
                      "%s  |  Capital Committee  |  2027 On-Site Solar Pilot: Siting Charter  |  Approved 15 September 2026"
                      % W.ORG)
    s = [Paragraph("2027 On-Site Solar Pilot: Siting Charter", H1),
         Paragraph("%s, Capital Committee. Approved 15 September 2026. Charter owner: %s, %s." %
                   (W.ORG, W.PEOPLE["director"], W.TITLES["director"]), H1S)]
    P_ = lambda n, t: s.append(Paragraph("<b>%s</b>&nbsp;&nbsp;%s" % (n, t), NUM))
    s.append(Paragraph("1. Purpose", H2))
    P_("1.1", "Corvane will install one rooftop solar array at one of its stores in 2027 as the pilot for a wider "
              "on-site generation program. The Committee names the pilot store in the 2027 capital plan, which it "
              "approves on 4 December 2026.")
    P_("1.2", "The pilot is sited to cut the carbon dioxide that the electric grid emits to serve Corvane.")
    s.append(Paragraph("2. Candidates", H2))
    P_("2.1", "The candidates are the eight stores in the pilot store sites file, each with the array that the 2026 "
              "feasibility study designed for its roof.")
    P_("2.2", "%s has modelled each array hour by hour on 2025 weather at its store. For this charter an array's "
              "2025 output is that model's output." % W.VENDOR_MODEL)
    s.append(Paragraph("3. The siting measure", H2))
    P_("3.1", "The pilot goes to the candidate whose array would have avoided the most grid carbon dioxide per "
              "megawatt-hour it generated in 2025, the latest calendar year of complete grid records.")
    P_("3.2", "The grid carbon dioxide an array avoids is the carbon dioxide that the generators of its store's balancing "
              "area would not have emitted in 2025 had the array been supplying the store.")
    P_("3.3", "Each megawatt-hour the array generates is one megawatt-hour less that the area's generators produce. The "
              "area's interchange with its neighbours is scheduled a day ahead and does not change with the array's "
              "output, and the store uses all of the array's output: each array is sized below its store's daytime load.")
    P_("3.4", "The measure is stated in metric tonnes of carbon dioxide per megawatt-hour of array output.")
    s.append(Paragraph("4. The recommendation", H2))
    P_("4.1", "The Director of Energy and Sustainability recommends the pilot store to the Committee in a memo that "
              "states the measure for every candidate and names the first candidate left out.")
    P_("4.2", "For the finance team's valuation of the array's output, the memo also states each candidate's 2025 metered "
              "electricity use, the share of it that its array would have supplied, and what Corvane paid for the "
              "store's electricity per megawatt-hour in 2025.")
    s.append(Paragraph("5. Records", H2))
    P_("5.1", "The %s's hourly operating data for each balancing area, its plant register and its published 2025 "
              "generation and emission rates; the array model; and Corvane's accounts payable records of its "
              "electricity invoices." % W.AGENCY)
    s.append(Spacer(1, 10))
    s.append(Paragraph("Approved by the Capital Committee at its meeting of 15 September 2026 (minute CC-26-41).", SMALL))
    doc.build(s, onFirstPage=frame, onLaterPages=frame)


# ---------------------------------------------------------------------------------------------- the supplier's label
def write_label(path):
    doc, frame = _doc(path, "Power Content Label 2025", W.SUPPLIER,
                      "%s  |  Power Content Label, calendar year 2025  |  Issued 30 June 2026" % W.SUPPLIER)
    s = [Paragraph("Power Content Label", H1),
         Paragraph("%s. Calendar year 2025. Issued 30 June 2026 under the retail electricity disclosure rules." % W.SUPPLIER,
                   H1S),
         Paragraph("This label discloses the sources of the electricity %s purchased in 2025 to serve customers on the "
                   "product below, and the carbon dioxide emitted generating it. It covers the product as sold in every "
                   "service territory where Ardley serves commercial customers." % W.SUPPLIER.replace(" LLC", ""), BODY),
         Paragraph("Product: Ardley Business Fixed (commercial fixed-price service)", H2)]
    rows = [["Energy source", "Share of product (%)", "Share of national grid mix (%)"],
            ["Coal", "19", "17"], ["Natural gas", "44", "41"], ["Nuclear", "18", "19"], ["Large hydroelectric", "6", "7"],
            ["Wind", "8", "10"], ["Solar", "3", "5"], ["Petroleum", "under 1", "under 1"], ["Unspecified sources", "2", "n/a"],
            ["Total", "100", "100"]]
    s.append(_table(rows, [2.6 * inch, 1.6 * inch, 1.9 * inch]))
    s.append(Spacer(1, 8))
    s.append(Paragraph("Carbon dioxide intensity of the product: 826 pounds per megawatt-hour delivered. Renewable energy "
                       "certificates retired for the product: none beyond the state renewable portfolio standard.", BODY))
    s.append(Paragraph("Sources are reported from supply contracts and wholesale purchases; unspecified sources are market "
                       "purchases not traceable to a generator. Figures are rounded and may not sum to 100.", SMALL))
    doc.build(s, onFirstPage=frame, onLaterPages=frame)


# ---------------------------------------------------------------------------------------------- workbooks
def write_rates(path, table, year, release):
    import openpyxl
    from openpyxl.styles import Alignment, Font, PatternFill
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "BA%02d" % (year % 100)
    ws["A1"] = "%s, %s: data year %d. Release 1.0, %s." % (W.AGENCY, W.RATES_TITLE, year,
                                                             release.strftime("%-d %B %Y"))
    ws["A1"].font = Font(bold=True)
    hdr = ["BA code", "Balancing area name", "Annual net generation (MWh)", "Annual CO2 emissions (short tons)",
           "CO2 output emission rate (lb/MWh)", "CO2 fossil output emission rate (lb/MWh)",
           "CO2 coal output emission rate (lb/MWh)", "CO2 gas output emission rate (lb/MWh)",
           "CO2 oil output emission rate (lb/MWh)", "CO2 non-baseload output emission rate (lb/MWh)",
           "Coal generation (%)", "Gas generation (%)", "Oil generation (%)", "Nuclear generation (%)",
           "Hydro generation (%)", "Wind generation (%)", "Solar generation (%)"]
    for j, h in enumerate(hdr, 1):
        c = ws.cell(row=3, column=j, value=h)
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="DCE6F1")
        c.alignment = Alignment(wrap_text=True, vertical="top")
    r = 4
    for code in W.ORDER:
        t = table[code]
        vals = [code, W.AREAS[code]["ba"], int(t["gen"]), int(t["co2_short"]), t["avg"], t["fossil"], t["coal"], t["gas"],
                t["oil"], t["nb"]] + [round(100 * t["mix"][f], 1) for f in
                                      ("coal", "natural gas", "petroleum", "nuclear", "hydro", "wind", "solar")]
        for j, v in enumerate(vals, 1):
            c = ws.cell(row=r, column=j, value=v)
            if j in (3, 4):
                c.number_format = "#,##0"
            elif 5 <= j <= 10:
                c.number_format = "#,##0.0"
            elif j >= 11:
                c.number_format = "0.0"
        r += 1
    widths = [9, 38, 16, 16, 14, 14, 14, 14, 14, 16, 10, 10, 10, 10, 10, 10, 10]
    for j, wdt in enumerate(widths, 1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(j)].width = wdt
    ws.row_dimensions[3].height = 60
    ws.freeze_panes = "C4"
    n = wb.create_sheet("Notes")
    notes = [
        "%s: %s" % (W.AGENCY, W.RATES_TITLE),
        "",
        "Coverage: every generating plant of 1 MW or more registered in the %s balancing areas, from the plant "
        "register for data year %d." % ("eight" if year else "", year),
        "Net generation: a plant's gross generation less its station service, as reported for the data year.",
        "CO2 emissions: from fuel consumed and the fuel's emission factor, in short tons (2,000 lb).",
        "Output emission rate: a balancing area's annual CO2 emissions divided by its annual net generation from all "
        "sources, in pounds per MWh.",
        "Fossil, coal, gas and oil output emission rates: the same ratio for the area's plants burning that fuel group.",
        "Non-baseload output emission rate: the output emission rate of the area's combustion plants, each plant weighted "
        "by its non-baseload share: wholly non-baseload with an annual capacity factor below 0.2, wholly baseload above "
        "0.8, and linear between.",
        "Generation shares: the area's annual net generation by primary fuel.",
        "Balancing areas are listed under the codes in use at the end of the data year.",
    ]
    for i, line in enumerate(notes, 1):
        if line:
            n.cell(row=i, column=1, value=line)
    n.column_dimensions["A"].width = 120
    wb.save(path)
