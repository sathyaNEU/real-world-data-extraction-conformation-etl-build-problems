"""task170 documents: the national guidelines' paediatric dosing annex, CMS's cycle quantification SOP, and the
programme's HIV estimates summary. Their text is kept here as data so checks.py and verify.py can quote it."""
from __future__ import annotations

import datetime as dt

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                        # noqa: E402
from reportlab.lib.pagesizes import A4                                                  # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                         # noqa: E402
from reportlab.lib.units import mm                                                      # noqa: E402
from reportlab.pdfbase import pdfmetrics                                                # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                            # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import common as C          # noqa: E402
import postprocess as PP    # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/"
for _n, _f in (("LibSans", "liberation/LiberationSans-Regular.ttf"), ("LibSans-Bold", "liberation/LiberationSans-Bold.ttf"),
               ("Carlito", "crosextra/Carlito-Regular.ttf"), ("Carlito-Bold", "crosextra/Carlito-Bold.ttf")):
    pdfmetrics.registerFont(TTFont(_n, FONT_DIR + _f))
INK = colors.HexColor("#1d2126")
GREY = colors.HexColor("#5b6169")
ACCENT = colors.HexColor("#1f4e3d")
RULE = colors.HexColor("#b9c4bd")
HEAD = colors.HexColor("#e4ece7")

F_DOSING = "paediatric_art_dosing_annex7_2026.pdf"
F_SOP = "cms_sop_qp04_v3_cycle_quantification.pdf"
F_EST = "hiv_estimates_2026_round_summary.pdf"

DOSING_DATE = dt.date(2026, 2, 9)
SOP_DATE = dt.date(2026, 2, 26)
EST_DATE = dt.date(2026, 7, 30)


def styles(font="LibSans", bold="LibSans-Bold", size=9.6):
    return dict(
        body=ParagraphStyle("b" + font, fontName=font, fontSize=size, leading=size * 1.34, textColor=INK, spaceAfter=4),
        h1=ParagraphStyle("h1" + font, fontName=bold, fontSize=13.5, leading=17.0, textColor=ACCENT, spaceAfter=2),
        sub=ParagraphStyle("s" + font, fontName=font, fontSize=8.6, leading=11.0, textColor=GREY, spaceAfter=8),
        h2=ParagraphStyle("h2" + font, fontName=bold, fontSize=10.2, leading=13.0, textColor=ACCENT, spaceBefore=5,
                          spaceAfter=2.5),
        cell=ParagraphStyle("c" + font, fontName=font, fontSize=8.1, leading=9.8, textColor=INK),
        cellr=ParagraphStyle("cr" + font, fontName=font, fontSize=8.1, leading=9.8, textColor=INK, alignment=2),
        cellb=ParagraphStyle("cb" + font, fontName=bold, fontSize=8.1, leading=9.8, textColor=INK),
        small=ParagraphStyle("sm" + font, fontName=font, fontSize=7.8, leading=10.0, textColor=GREY, spaceAfter=3))


def _doc(path, title, author):
    return SimpleDocTemplate(path, pagesize=A4, leftMargin=21 * mm, rightMargin=21 * mm, topMargin=18 * mm,
                             bottomMargin=17 * mm, title=title, author=author, subject="", creator="", producer="")


def _footer(left, font="LibSans"):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFont(font, 7.4)
        canvas.setFillColor(GREY)
        canvas.drawString(21 * mm, 9.5 * mm, left)
        canvas.drawRightString(A4[0] - 21 * mm, 9.5 * mm, "Page %d" % doc.page)
        canvas.restoreState()
    return draw


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _table(st, head, rows, widths, right=()):
    data = [[Paragraph(esc(h), st["cellb"]) for h in head]]
    for r in rows:
        data.append([Paragraph(esc(str(x)), st["cellr"] if i in right else st["cell"]) for i, x in enumerate(r)])
    t = Table(data, colWidths=[w * mm for w in widths], repeatRows=1)
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), HEAD), ("LINEBELOW", (0, 0), (-1, 0), 0.6, RULE),
                           ("LINEBELOW", (0, -1), (-1, -1), 0.6, RULE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("TOPPADDING", (0, 0), (-1, -1), 2.0), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.0),
                           ("LEFTPADDING", (0, 0), (-1, -1), 2.5), ("RIGHTPADDING", (0, 0), (-1, -1), 2.5)]))
    return t


def pdf_stamp(d, hh=9, mi=0):
    return ("D:%04d%02d%02d%02d%02d00+02'00'" % (d.year, d.month, d.day, hh, mi)).encode()


# ---------------------------------------------------------------------------------------------------- dosing annex
DOSING_INTRO = [
    "Antiretroviral drugs for children and adolescents are dosed by weight band. Weigh the child at each clinical "
    "visit and dispense the formulation and number of tablets for the band of the weight recorded at that visit. A "
    "child or adolescent started on TLD stays on TLD at later visits, whatever the weight recorded.",
    "This edition lowers the weight from which TLD is given from 35 kg to 30 kg. A child on a first-line regimen who "
    "weighs 30 kg or more at a clinical visit on or after 1 March 2026 moves onto TLD at that visit.",
    "Children aged two or over who have been on treatment for six months or more and are well may be given two or three "
    "months of medicines at a visit; the clinician sets the next appointment for the end of the supply. A caregiver may "
    "collect a child's medicines between clinical visits; a collection dispenses the regimen of the last clinical "
    "visit.",
]
DOSING_CHANGES = [
    ("TLD", "From 35 kg", "From 30 kg"),
    ("Adult second line", "From 35 kg", "From 30 kg"),
    ("25 to 29.9 kg", "ABC/3TC 600/300 mg with DTG 50 mg up to 34.9 kg", "ABC/3TC 600/300 mg with DTG 50 mg up to 29.9 kg"),
    ("Medicines at a visit", "One month as a rule; two or three at the clinician's discretion",
     "Two or three months for children two or over, six months on treatment and well"),
]
FIRST_LINE = [
    ("3 to 5.9", "ABC/3TC 120/60 mg dispersible", "1", "DTG 10 mg dispersible", "half"),
    ("6 to 9.9", "ABC/3TC 120/60 mg dispersible", "1.5", "DTG 10 mg dispersible", "1.5"),
    ("10 to 13.9", "ABC/3TC 120/60 mg dispersible", "2", "DTG 10 mg dispersible", "2"),
    ("14 to 19.9", "ABC/3TC 120/60 mg dispersible", "2.5", "DTG 10 mg dispersible", "2.5"),
    ("20 to 24.9", "ABC/3TC 120/60 mg dispersible", "3", "DTG 50 mg film-coated", "1"),
    ("25 to 29.9", "ABC/3TC 600/300 mg", "1", "DTG 50 mg film-coated", "1"),
    ("30 and over", "TDF/3TC/DTG 300/300/50 mg (TLD)", "1", "", ""),
]
SECOND_LINE = [
    ("3 to 29.9", "AZT/3TC 60/30 mg dispersible and LPV/r 40/10 mg pellets or 100/25 mg tablets, by the band table "
     "in Annex 8"),
    ("30 and over", "TDF/3TC 300/300 mg once daily and DRV/r 800/100 mg once daily"),
]


def write_dosing(out):
    st = styles()
    path = out + "/" + F_DOSING
    doc = _doc(path, "Annex 7. Antiretroviral dosing for children and adolescents", C.MOH)
    el = [Paragraph("National Guidelines for HIV Prevention, Treatment and Care, 2026 edition", st["sub"]),
          Paragraph("Annex 7. Antiretroviral dosing for children and adolescents", st["h1"]),
          Paragraph("%s, %s. Effective 1 March 2026; replaces Annex 7 of the 2023 edition." % (C.MOH, C.PROG), st["sub"]),
          Paragraph("7.1 Dosing by weight band", st["h2"])]
    for p in DOSING_INTRO:
        el.append(Paragraph(esc(p), st["body"]))
    el.append(Paragraph("7.2 First-line regimen: ABC/3TC with DTG, then TLD", st["h2"]))
    el.append(_table(st, ["Weight (kg)", "NRTI backbone", "Tablets a day", "DTG", "Tablets a day"],
                     FIRST_LINE, [22, 52, 20, 42, 22], right=(2, 4)))
    el.append(Spacer(1, 5))
    el.append(Paragraph("ABC/3TC once daily; dispersible tablets dissolved in water. DTG 10 mg dispersible and DTG 50 mg "
                        "film-coated tablets are not interchangeable mg for mg.", st["small"]))
    el.append(Paragraph("7.3 Second-line regimen: protease inhibitor based", st["h2"]))
    el.append(_table(st, ["Weight (kg)", "Regimen"], SECOND_LINE, [22, 136]))
    el.append(Paragraph("7.4 Regimen codes in the electronic patient register", st["h2"]))
    el.append(_table(st, ["Code", "Line", "Regimen", "Weight band"],
                     [(r[0], r[1], r[2], r[3]) for r in C.REGIMENS], [24, 16, 92, 26]))
    el.append(Paragraph("7.5 Changes from the 2023 edition", st["h2"]))
    el.append(_table(st, ["", "2023 edition", "This edition"], DOSING_CHANGES, [30, 64, 64]))
    doc.build(el, onFirstPage=_footer("Annex 7. %s, %s, 2026 edition" % (C.MOH, C.PROG)),
              onLaterPages=_footer("Annex 7. %s, %s, 2026 edition" % (C.MOH, C.PROG)))
    PP.normalize_pdf(path, pdf_stamp(DOSING_DATE, 10, 5), pdf_stamp(DOSING_DATE, 10, 5))


# ---------------------------------------------------------------------------------------------------- the SOP
SOP = [
    ("1. Scope", [
        "1.1 This procedure sets the cycle order for each antiretroviral product CMS buys for the national programme. "
        "Cycles run from January to June and from July to December; C5 ran from January to June 2026, C6 runs from "
        "July to December 2026 and C7 from January to June 2027.",
        "1.2 Quantities are in the product's unit of issue. The unit of issue of TDF/3TC/DTG 300/300/50 mg (TLD) is the "
        "bottle of 30 tablets.",
    ]),
    ("2. Calendar", [
        "2.1 Stock is counted at the Main warehouse and the Northern depot on the last day of February and of August.",
        "2.2 The quantification review sits in March and September and files the order for the cycle after the one in "
        "progress: the September 2026 review files the C7 order.",
    ]),
    ("3. The order", [
        "3.1 The order for a product is its forecast consumption from the first day of the month after the count to "
        "the last day of the cycle ordered, plus the maximum stock level, less the usable stock on hand at the count, "
        "less the quantities on order with a confirmed delivery date on or before the last day of the cycle ordered.",
        "3.2 The maximum stock level is six months of the product's forecast consumption in the last month of the cycle "
        "ordered.",
        "3.3 Usable stock is stock on hand that is neither quarantined nor expired. Planned call-offs under a framework "
        "agreement are not quantities on order until the supplier confirms a delivery date.",
    ]),
    ("4. Forecast consumption", [
        "4.1 Consumption is forecast by month. For a once-daily tablet in bottles of 30, a month's consumption is one "
        "bottle for each patient in care on the regimen at the end of the month; a patient who leaves care (lost to "
        "follow-up, transferred out of the programme or died) is not counted from the month the patient leaves.",
        "4.2 TLD. Patients aged 15 and over at the count, and patients who start treatment after the count, are taken "
        "from the National ART Programme's patient projection. Children aged under 15 at the count who are on treatment "
        "in the paediatric and adolescent ART register (no outcome entered) are forecast by the Quantification Unit from "
        "the register to the last day of the cycle ordered, whatever their age by then.",
        "4.3 The TLD order has two lines. Line 2, which the paediatric grant funds, carries the children of section 4.2: "
        "their forecast consumption from the first day of the month after the count to the last day of the cycle "
        "ordered, plus six months of their forecast consumption in the last month of the cycle ordered. Line 1 carries "
        "the patients of the projection on the same terms, less the usable stock on hand and the quantities on order "
        "(section 3.1), which are netted on line 1 alone.",
        "4.4 Each line is ordered in whole pallets of TLD 30s, 84 cartons of 96 bottles (8,064 bottles) to the pallet, "
        "rounded to the nearest pallet.",
        "4.5 Other products are forecast from the programme projection's regimen shares.",
    ]),
    ("5. The review", [
        "5.1 Before the order is filed, the review compares region by region the dispensing facilities reported for "
        "the last two closed cycles with the deliveries CMS made to them.",
        "5.2 The review records the order, the forecast it rests on and the stock position in the quantification "
        "workbook, which the Quantification Unit keeps.",
    ]),
    ("6. Records", [
        "6.1 The stock status report of the count, the programme projection and the register extract used are kept "
        "with the workbook.",
        "6.2 The order is sent to the Procurement Unit within five working days of the review.",
    ]),
]


def write_sop(out):
    st = styles()
    path = out + "/" + F_SOP
    doc = _doc(path, "QP-04 Cycle quantification of antiretroviral medicines", C.ORG)
    el = [Paragraph("%s, Quantification Unit" % C.ORG, st["sub"]),
          Paragraph("Standard Operating Procedure QP-04. Cycle quantification of antiretroviral medicines", st["h1"]),
          Paragraph("Version 3. Effective 1 March 2026. Supersedes version 2 of 2 October 2023. Owner: %s, "
                    "quantification lead." % C.PEOPLE["quant_lead"], st["sub"])]
    for head, paras in SOP:
        el.append(Paragraph(head, st["h2"]))
        for p in paras:
            el.append(Paragraph(esc(p), st["body"]))
    el.append(Spacer(1, 6))
    el.append(_table(st, ["Version", "Date", "Change"],
                     [("1", "14 March 2022", "First issue"),
                      ("2", "2 October 2023", "Maximum stock level set at six months; the Northern depot counted"),
                      ("3", "26 February 2026", "Sections 4.2 to 4.4: children under 15 forecast from the paediatric "
                       "register on their own line; lines ordered in whole pallets")],
                     [18, 30, 110]))
    doc.build(el, onFirstPage=_footer("CMS QP-04 v3"), onLaterPages=_footer("CMS QP-04 v3"))
    PP.normalize_pdf(path, pdf_stamp(SOP_DATE, 15, 40), pdf_stamp(SOP_DATE, 15, 40))


# ---------------------------------------------------------------------------------------------------- estimates (unused)
def write_estimates(out, est):
    """The programme's HIV estimates summary, 2026 round (a distractor: it describes people living with HIV, not
    patients on a regimen)."""
    st = styles()
    path = out + "/" + F_EST
    doc = _doc(path, "HIV estimates, 2026 round: summary tables", C.PROG)
    el = [Paragraph("%s, Strategic Information Unit" % C.PROG, st["sub"]),
          Paragraph("HIV estimates, 2026 round: summary tables", st["h1"]),
          Paragraph("Estimates for mid-2026 from the national model, fitted to antenatal surveillance, the 2024 "
                    "population HIV survey and programme data to December 2025.", st["sub"]),
          Paragraph("Table 1. People living with HIV and on antiretroviral treatment, by age group", st["h2"]),
          _table(st, ["Age group", "Living with HIV", "Lower", "Upper", "On treatment", "Coverage (%)"],
                 est["age"], [26, 30, 24, 24, 28, 26], right=(1, 2, 3, 4, 5)),
          Paragraph("Table 2. People living with HIV, all ages, by region", st["h2"]),
          _table(st, ["Region", "Living with HIV", "Lower", "Upper", "Adult prevalence 15-49 (%)"],
                 est["region"], [30, 32, 26, 26, 44], right=(1, 2, 3, 4)),
          Paragraph("Table 3. New infections and AIDS-related deaths", st["h2"]),
          _table(st, ["Year", "New infections, 0-14", "New infections, 15+", "Deaths, 0-14", "Deaths, 15+"],
                 est["trend"], [20, 36, 36, 32, 32], right=(1, 2, 3, 4)),
          Spacer(1, 4),
          Paragraph("Ranges are 95 per cent uncertainty bounds. Regions as drawn from 1 April 2026.", st["small"])]
    doc.build(el, onFirstPage=_footer("HIV estimates 2026 round"), onLaterPages=_footer("HIV estimates 2026 round"))
    PP.normalize_pdf(path, pdf_stamp(EST_DATE, 11, 20), pdf_stamp(EST_DATE, 11, 20))
