"""The pack's documents and workbooks: the survey's design and fieldwork report, the 2027 allocation standard, the
Program's fact sheet, the assessors' parcel compilation and Cedarline's results workbook."""
import datetime as dt

import numpy as np
import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill
from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                      # noqa: E402
from reportlab.lib.pagesizes import letter                                            # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                       # noqa: E402
from reportlab.lib.units import inch                                                  # noqa: E402
from reportlab.pdfbase import pdfmetrics                                              # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                          # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import pack as P     # noqa: E402
import world as W    # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("LiberationSerif", "Regular"), ("LiberationSerif-Bold", "Bold"), ("LiberationSerif-Italic", "Italic"),
              ("LiberationSans", "Regular"), ("LiberationSans-Bold", "Bold"), ("LiberationSans-Italic", "Italic")):
    try:
        pdfmetrics.getFont(nm)
    except KeyError:
        pdfmetrics.registerFont(TTFont(nm, FONT_DIR + nm.split("-")[0] + "-" + f + ".ttf"))
INK = colors.HexColor("#1b1d1f")
GREY = colors.HexColor("#5b6067")
TEAL = colors.HexColor("#1d4f5c")
GREEN = colors.HexColor("#2f5a2e")
BLUE = colors.HexColor("#21456e")
SANS = ParagraphStyle("sans", fontName="LiberationSans", fontSize=9.6, leading=13.2, textColor=INK, spaceAfter=6)
SERIF = ParagraphStyle("serif", fontName="LiberationSerif", fontSize=10.5, leading=14.2, textColor=INK, spaceAfter=6)
CELL = ParagraphStyle("cell", fontName="LiberationSans", fontSize=8.2, leading=10.2, textColor=INK)
CELLB = ParagraphStyle("cellb", parent=CELL, fontName="LiberationSans-Bold")
SMALL = ParagraphStyle("small", fontName="LiberationSans", fontSize=8.0, leading=10.4, textColor=GREY)
HEAD_FILL = PatternFill("solid", fgColor="DDE7EC")


def styles(accent, serif=False):
    face = "LiberationSerif" if serif else "LiberationSans"
    h1 = ParagraphStyle("h1", fontName=face + "-Bold", fontSize=14, leading=18, textColor=accent, spaceAfter=2)
    h1s = ParagraphStyle("h1s", fontName=face, fontSize=9.3, leading=12.5, textColor=GREY, spaceAfter=10)
    h2 = ParagraphStyle("h2", fontName=face + "-Bold", fontSize=10.5, leading=14, textColor=INK, spaceBefore=7,
                        spaceAfter=3, keepWithNext=1)
    return h1, h1s, h2


def _doc(path, title, author, footer, layout="left"):
    def frame(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(GREY)
        if layout == "left":
            canvas.setFont("LiberationSans", 7.5)
            canvas.drawString(0.9 * inch, 0.6 * inch, footer)
            canvas.drawRightString(letter[0] - 0.9 * inch, 0.6 * inch, "Page %d" % doc.page)
        elif layout == "centre":
            canvas.setFont("LiberationSerif", 8.5)
            canvas.drawCentredString(letter[0] / 2, 0.6 * inch, "%s, page %d" % (footer, doc.page))
        else:
            canvas.setFont("LiberationSans", 8)
            canvas.drawString(0.9 * inch, letter[1] - 0.55 * inch, footer)
            canvas.setStrokeColor(GREY)
            canvas.setLineWidth(0.5)
            canvas.line(0.9 * inch, letter[1] - 0.6 * inch, letter[0] - 0.9 * inch, letter[1] - 0.6 * inch)
            canvas.drawCentredString(letter[0] / 2, 0.55 * inch, str(doc.page))
        canvas.restoreState()
    d = SimpleDocTemplate(path, pagesize=letter, leftMargin=0.9 * inch, rightMargin=0.9 * inch, topMargin=0.8 * inch,
                          bottomMargin=0.9 * inch, title=title, author=author, subject="", creator="", producer="")
    return d, frame


def _table(rows, widths, head="#e3ecef", right=()):
    data = []
    for i, r in enumerate(rows):
        line = []
        for j, v in enumerate(r):
            st = CELLB if i == 0 else CELL
            if i > 0 and j in right:
                st = ParagraphStyle("r", parent=st, alignment=2)
            line.append(Paragraph(str(v), st))
        data.append(line)
    t = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9aa0a6")),
                           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(head)),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 4),
                           ("RIGHTPADDING", (0, 0), (-1, -1), 4)]))
    return t


def _n(v):
    return "{:,}".format(int(v))


# ------------------------------------------------------------------------------------- the survey's own statistics
def fieldwork(x):
    """per county: the two lists' sizes on August 31, 2025, the targets, letters mailed and outcomes by list"""
    out = []
    for c in x["counties"]:
        row = dict(code=c["code"], name=c["name"], NP=c["NP"], NQ=c["NQ"], nP=c["nP"], nQ=c["nQ"], lab=c["lab"])
        for lst in ("P", "Q"):
            d = [o for l, _i, o in c["draws"] if l == lst]
            row["mailed" + lst] = len(d)
            row["tested" + lst] = sum(1 for o in d if o == "TESTED")
            row["earlier" + lst] = sum(1 for o in d if o == "TESTED_EARLIER")
            row["declined" + lst] = sum(1 for o in d if o == "DECLINED")
            row["noresp" + lst] = sum(1 for o in d if o == "NO_RESPONSE")
        out.append(row)
    return out


# --------------------------------------------------------------------------------------------------- the report
def write_design(path, x):
    acc = TEAL
    h1, h1s, h2 = styles(acc)
    d, frame = _doc(path, "2025-26 Private Well Nitrate Survey: design and fieldwork", W.PEOPLE["epi"],
                    "%s, %s  |  PWNS 2025-26 design and fieldwork  |  May 2026" % (W.DEPT, W.OFFICE))
    fw = fieldwork(x)
    s = [Paragraph("2025-26 Private Well Nitrate Survey", h1),
         Paragraph("Design and fieldwork report. %s, %s, %s. Prepared by %s, environmental epidemiologist, "
                   "for %s, %s manager. Issued May 22, 2026." % (W.DEPT, W.OFFICE, W.PROGRAM, W.PEOPLE["epi"],
                                                               W.PEOPLE["manager"], W.PROGRAM), h1s),
         Paragraph("1. Purpose", h2),
         Paragraph("The survey measures nitrate in private domestic wells in each of the state's sixteen counties so "
                   "that the Department can estimate, county by county, how many private domestic wells are above "
                   "the nitrate standard of 10 mg/L nitrate as nitrogen. The 2027 Well Water Assistance allocation "
                   "rests on those estimates. This report sets out how the survey was designed and how its fieldwork "
                   "ran; it does not report nitrate results, which go to the Program with the county estimates "
                   "after the retest period closes on June 30, 2026.", SANS),
         Paragraph("2. The survey population and its two lists", h2),
         Paragraph("No single record lists every private well in the state. The survey's population in a county is "
                   "every private domestic well on either of two lists as they stood on August 31, 2025:", SANS),
         Paragraph("<b>The permit list:</b> every well the Department's well construction permit database recorded "
                   "on August 31, 2025 as an active domestic well drilled under permit on or after January 1, 1986, "
                   "when permits became mandatory. Irrigation, livestock, monitoring and industrial wells, abandoned "
                   "wells, and the earlier permits of wells since replaced are not on it.", SANS),
         Paragraph("<b>The parcel list:</b> every residential parcel that the county assessor's 2025 roll records as "
                   "served by a private well. The assessors' water-source codes are listed in the Codes sheet of the "
                   "parcel compilation the Program assembled from the sixteen rolls.", SANS),
         Paragraph("Each list misses wells the other holds. Wells drilled before 1986 that were never re-permitted "
                   "are not on the permit list, and an assessor's water-source field is not updated when a well is "
                   "drilled, so a parcel can carry a permitted domestic well while the roll records public water or "
                   "nothing. A well drilled under permit on a parcel the roll records as served by a private well is "
                   "on both lists. The Program treats a permit and a parcel as the same well when the permit's "
                   "parcel number is the parcel's or, on a permit that carries no parcel number, when the permit's "
                   "site address is the parcel's situs address.", SANS),
         Paragraph("3. Sampling", h2),
         Paragraph("In each county the survey drew households at random from each list separately. Each list had its "
                   "own target of completed first tests in each county (Table 2), set from the laboratory budget, "
                   "with the permit list sampled more heavily because its permits record each well's depth and "
                   "construction, which the Program's well construction work also uses. Letters went to the drawn "
                   "households in the order drawn; a household that declined or did not return its kit within six "
                   "weeks was replaced by the next household drawn from the same list, until the list's target was "
                   "met. The permit list was drawn first. A household drawn from the parcel list whose well had "
                   "already been tested from the permit list was not sent a second kit: its first test counts "
                   "toward the parcel list's target as well, and the draw manifest records it as TESTED_EARLIER "
                   "with the earlier kit.", SANS),
         Paragraph("4. Kits and laboratories", h2),
         Paragraph("Each tested household collected one sample from a cold-water tap ahead of any treatment, in the "
                   "kit mailed to it, and returned it to the county's survey laboratory (Table 1). First tests closed "
                   "on April 30, 2026. The laboratories report nitrate as nitrogen, except Kinsale Water Testing, "
                   "which reports nitrate as NO3; 10 mg/L nitrate as nitrogen is 44.27 mg/L nitrate as NO3 (a factor "
                   "of 4.427). Where a laboratory reanalysed a sample, its later report replaces the earlier one. "
                   "Each laboratory also reports arsenic and total coliform and E. coli on every sample; those results "
                   "go to households with their nitrate result.", SANS),
         Paragraph("Households whose first test was above the nitrate standard were offered a free retest kit, "
                   "ordered from the kit vendor through its web portal or by phone, and analysed by a survey "
                   "laboratory.", SANS)]
    t1 = [["County", "Code", "Survey laboratory"]] + [[r["name"], r["code"], W.LABS[r["lab"]]] for r in fw]
    s += [Paragraph("Table 1. Survey laboratories", h2), _table(t1, [1.6 * inch, 0.7 * inch, 3.0 * inch])]
    t2 = [["County", "Permit list wells, Aug 31, 2025", "Parcel list wells, Aug 31, 2025", "Target, permit list",
           "Target, parcel list", "Letters, permit list", "Letters, parcel list"]]
    for r in fw:
        t2.append([r["name"], _n(r["NP"]), _n(r["NQ"]), _n(r["nP"]), _n(r["nQ"]), _n(r["mailedP"]), _n(r["mailedQ"])])
    t2.append(["All counties", _n(sum(r["NP"] for r in fw)), _n(sum(r["NQ"] for r in fw)),
               _n(sum(r["nP"] for r in fw)), _n(sum(r["nQ"] for r in fw)), _n(sum(r["mailedP"] for r in fw)),
               _n(sum(r["mailedQ"] for r in fw))])
    s += [Paragraph("Table 2. The lists, the targets and the letters", h2),
          _table(t2, [1.2 * inch, 0.95 * inch, 0.95 * inch, 0.8 * inch, 0.8 * inch, 0.75 * inch, 0.75 * inch],
                 right=(1, 2, 3, 4, 5, 6))]
    t3 = [["County", "Tested, permit list", "Declined, permit list", "No response, permit list",
           "Tested, parcel list", "Tested earlier, parcel list", "Declined, parcel list", "No response, parcel list"]]
    for r in fw:
        t3.append([r["name"], r["testedP"], r["declinedP"], r["noresp" + "P"], r["testedQ"], r["earlierQ"],
                   r["declinedQ"], r["noresp" + "Q"]])
    s += [Paragraph("Table 3. Outcomes of the letters", h2),
          _table(t3, [1.2 * inch] + [0.74 * inch] * 7, right=(1, 2, 3, 4, 5, 6, 7)),
          Spacer(1, 4),
          Paragraph("Tested earlier: drawn from the parcel list after the well had been tested from the permit list. "
                    "A household that declined or did not respond was replaced by the next draw from the same list. "
                    "Source: PWNS draw manifest, closed April 30, 2026.", SMALL)]
    d.build(s, onFirstPage=frame, onLaterPages=frame)


def write_standard(path):
    acc = GREEN
    h1, h1s, h2 = styles(acc, serif=True)
    d, frame = _doc(path, "Well Water Assistance: 2027 county allocation standard", W.DEPT,
                    "WWA-2027-01, adopted March 10, 2026", layout="centre")
    s = [Paragraph("Well Water Assistance", h1),
         Paragraph("2027 county allocation standard, WWA-2027-01. %s, %s. Adopted March 10, 2026; "
                   "coordinator %s." % (W.DEPT, W.OFFICE, W.PEOPLE["assist"]), h1s),
         Paragraph("1. Scope", h2),
         Paragraph("This standard decides which counties receive the 2027 Well Water Assistance allocation and which "
                   "households within them may receive assistance. It applies the results of the 2025-26 Private Well "
                   "Nitrate Survey (the Survey).", SERIF),
         Paragraph("2. Definitions", h2),
         Paragraph("2.1 The nitrate standard is 10 mg/L nitrate as nitrogen. A result is above the standard when it "
                   "is more than 10 mg/L nitrate as nitrogen.", SERIF),
         Paragraph("2.2 A county's survey population is the private domestic wells in the county on either of the "
                   "Survey's two lists, the permit list and the parcel list, as the Survey's design report defines "
                   "them.", SERIF),
         Paragraph("2.3 A well's first test is the Survey's first test of it. A retest is a sample from a retest kit "
                   "the household ordered after a first test.", SERIF),
         Paragraph("3. Qualifying counties", h2),
         Paragraph("3.1 A county qualifies for the 2027 allocation when the Survey estimates that 250 or more wells in "
                   "its survey population are above the standard, a well being above the standard when its first "
                   "test is. The estimate covers the whole survey population, the wells the Survey did not test as "
                   "well as those it did.", SERIF),
         Paragraph("3.2 Each qualifying county receives a base award of $140,000 for treatment systems and $25,000 "
                   "for outreach. Awards are made for calendar year 2027 and do not carry over.", SERIF),
         Paragraph("4. Households", h2),
         Paragraph("4.1 Within a qualifying county, a household may receive a point-of-use treatment system and its "
                   "first year of filters when its well was above the standard on its first test and again on a "
                   "retest.", SERIF),
         Paragraph("4.2 A retest counts for the 2027 cycle when its sample was collected on or before June 30, 2026. "
                   "Later retests are taken up in the 2028 cycle.", SERIF),
         Paragraph("5. Review", h2),
         Paragraph("The Program reviews this standard after the 2027 cycle and before the next survey.", SERIF)]
    d.build(s, onFirstPage=frame, onLaterPages=frame)


def write_factsheet(path):
    acc = BLUE
    h1, h1s, h2 = styles(acc)
    d, frame = _doc(path, "Nitrate and your well", W.PROGRAM, "%s  |  %s  |  Revised January 2025" % (W.DEPT, W.PROGRAM),
                    layout="top")
    s = [Paragraph("Nitrate and your well", h1),
         Paragraph("A fact sheet for households on private wells. %s." % W.PROGRAM, h1s),
         Paragraph("What is nitrate?", h2),
         Paragraph("Nitrate is a form of nitrogen that dissolves in water. It reaches groundwater from fertilizer, "
                   "manure, septic systems and decaying plants. Shallow wells, dug wells and wells in sandy soils are "
                   "more likely to have high nitrate, and levels can rise in spring after snowmelt and heavy rain.",
                   SANS),
         Paragraph("Why does it matter?", h2),
         Paragraph("Water above the nitrate standard should not be used to mix infant formula or for anyone who is "
                   "pregnant. Boiling water does not remove nitrate; it concentrates it.", SANS),
         Paragraph("Reading your result", h2),
         Paragraph("Laboratories report nitrate in two ways. Most report nitrate as nitrogen (nitrate-N); the "
                   "drinking water standard is 10 mg/L nitrate-N. Some report nitrate itself (NO3), where the same "
                   "standard is 44 mg/L. To compare an NO3 result with the standard, divide it by 4.4.", SANS),
         _table([["Result (nitrate-N)", "What it means", "What to do"],
                 ["Under 3 mg/L", "Typical of wells little affected by land use", "Test every two to three years"],
                 ["3 to 10 mg/L", "Affected by land use; below the standard", "Test every year"],
                 ["Over 10 mg/L", "Above the standard", "Use another source for infants; retest; consider treatment"]],
                [1.4 * inch, 2.6 * inch, 2.6 * inch]),
         Spacer(1, 6),
         Paragraph("Treatment", h2),
         Paragraph("Reverse osmosis, distillation and anion exchange remove nitrate. A point-of-use reverse osmosis "
                   "unit under the kitchen sink treats water for drinking and cooking. Water softeners and carbon "
                   "filters do not remove nitrate.", SANS),
         Paragraph("Testing", h2),
         Paragraph("Use a laboratory certified for nitrate. Collect the sample from a cold-water tap that does not "
                   "pass through a softener or filter, and get it to the laboratory within two days.", SANS)]
    d.build(s, onFirstPage=frame, onLaterPages=frame)


# ------------------------------------------------------------------------------------------------- the workbooks
def _head(ws, cols, widths):
    ws.append(cols)
    for c in ws[ws.max_row]:
        c.font = Font(bold=True)
        c.fill = HEAD_FILL
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for i, w in enumerate(widths):
        ws.column_dimensions[openpyxl.utils.get_column_letter(i + 1)].width = w
    ws.freeze_panes = "A2"


def write_parcels(path, x, sheets):
    wb = openpyxl.Workbook()
    rd = wb.active
    rd.title = "Codes"
    lines = [("Residential parcels, 2025 assessment rolls: compilation for the Private Well Program", True),
             ("Each county sheet is the residential parcel extract its assessor sent in January 2026 from the 2025 "
              "roll, kept in the assessor's own layout.", False),
             ("", False),
             ("Water-source codes by layout", True)]
    for i, (t, b) in enumerate(lines, 1):
        rd.cell(row=i, column=1, value=t or None).font = Font(bold=b, size=12 if (b and i == 1) else 10)
    rd.append(["Layout", "Counties", "Column", "Private well", "Public water", "Blank"])
    for c in rd[rd.max_row]:
        c.font = Font(bold=True)
    for lay in ("A", "B", "C"):
        cols = P.PARCEL_LAYOUTS[lay]
        pw, pub = P.WATER_CODES[lay]
        names = ", ".join(c["name"] for c in x["counties"] if c["layout"] == lay)
        rd.append([lay, names, cols[-1], pw, pub, "not recorded"])
    for col, w in zip("ABCDEF", (8, 62, 16, 12, 12, 14)):
        rd.column_dimensions[col].width = w
    for c in x["counties"]:
        lay, rows = sheets[c["code"]]
        ws = wb.create_sheet(c["code"] + " " + c["name"])
        widths = {"A": (14, 30, 14, 9, 11, 9), "B": (12, 9, 5, 18, 8, 14, 7, 8, 13),
                  "C": (15, 32, 14, 14, 10, 13)}[lay]
        _head(ws, P.PARCEL_LAYOUTS[lay], widths)
        for r in rows:
            ws.append([None if v == "" else v for v in r])
    wb.save(path)


def write_ced(path, rows):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Results"
    _head(ws, P.CED_COLS, (14, 15, 8, 12, 15, 9, 7, 9, 10, 12, 40))
    for r in rows:
        ws.append([None if v == "" else v for v in r])
        ws.cell(row=ws.max_row, column=4).number_format = "mm/dd/yyyy"
        ws.cell(row=ws.max_row, column=10).number_format = "mm/dd/yyyy"
    nt = wb.create_sheet("Report notes")
    for i, t in enumerate(["Cedarline Environmental Laboratories: Private Well Nitrate Survey results, 2025-26",
                           "Client: %s, %s" % (W.DEPT, W.PROGRAM),
                           "Qualifier U: not detected at the reporting limit shown in Result.",
                           "A reanalysis is reported on its own row with a later report date."], 1):
        nt.cell(row=i, column=1, value=t).font = Font(bold=(i == 1))
    nt.column_dimensions["A"].width = 90
    wb.save(path)
