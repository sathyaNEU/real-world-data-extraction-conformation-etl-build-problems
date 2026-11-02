"""The pack's documents: the written assurance Wrenfield & Holt gave Calvermoor Trading Standards (the return's
definitions, filed once, in the assurance's own words), the Cotterby returns centre's 2025 review (the compliance
lead's close-out file, a distractor), the centre's daily operations workbook (a distractor); and PROVENANCE, each
shipped file's source and date, which goes to metadata.json and the files' saved dates. No file describes another,
how the centre's records pair, how the hall is worked, or how a return was posted."""
import datetime as dt

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                      # noqa: E402
from reportlab.lib.pagesizes import A4                                                # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                       # noqa: E402
from reportlab.lib.units import mm                                                    # noqa: E402
from reportlab.pdfbase import pdfmetrics                                              # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                          # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import world as W     # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("LiberationSerif", "Regular"), ("LiberationSerif-Bold", "Bold"), ("LiberationSerif-Italic", "Italic"),
              ("LiberationSans", "Regular"), ("LiberationSans-Bold", "Bold"), ("LiberationSans-Italic", "Italic")):
    try:
        pdfmetrics.getFont(nm)
    except KeyError:
        pdfmetrics.registerFont(TTFont(nm, FONT_DIR + nm.split("-")[0] + "-" + f + ".ttf"))
INK = colors.HexColor("#1c1c1c")
GREY = colors.HexColor("#5d6166")
PLUM = colors.HexColor("#4b2142")
SLATE = colors.HexColor("#2c3e50")
BODY = ParagraphStyle("body", fontName="LiberationSerif", fontSize=10.6, leading=14.4, textColor=INK, spaceAfter=6)
SANS = ParagraphStyle("sans", fontName="LiberationSans", fontSize=9.5, leading=13.1, textColor=INK, spaceAfter=6)
CELL = ParagraphStyle("cell", fontName="LiberationSans", fontSize=8.3, leading=10.3, textColor=INK)
CELLB = ParagraphStyle("cellb", parent=CELL, fontName="LiberationSans-Bold")
SMALL = ParagraphStyle("small", fontName="LiberationSans", fontSize=8.2, leading=10.6, textColor=GREY)
NUM = ParagraphStyle("num", fontName="LiberationSerif", fontSize=10.6, leading=14.4, textColor=INK, spaceAfter=6,
                     leftIndent=8 * mm, firstLineIndent=-8 * mm)


def heads(accent, face):
    h1 = ParagraphStyle("h1", fontName=face + "-Bold", fontSize=14.5, leading=18.5, textColor=accent, spaceAfter=3)
    h1s = ParagraphStyle("h1s", fontName=face, fontSize=9.4, leading=12.6, textColor=GREY, spaceAfter=10)
    h2 = ParagraphStyle("h2", fontName=face + "-Bold", fontSize=10.6, leading=14, textColor=INK, spaceBefore=8,
                        spaceAfter=3)
    return h1, h1s, h2


def _doc(path, title, author, footer, face="LiberationSerif"):
    def frame(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(GREY)
        canvas.setFont(face, 7.8)
        canvas.drawString(20 * mm, 11 * mm, footer)
        canvas.drawRightString(A4[0] - 20 * mm, 11 * mm, "Page %d" % doc.page)
        canvas.restoreState()
    d = SimpleDocTemplate(path, pagesize=A4, leftMargin=22 * mm, rightMargin=22 * mm, topMargin=20 * mm,
                          bottomMargin=20 * mm, title=title, author=author, subject="", creator="", producer="")
    return d, frame


def _table(rows, widths, head="#ece6ea"):
    data = [[Paragraph(str(v), CELLB if i == 0 else CELL) for v in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#a2a5aa")),
                           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(head)),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 4),
                           ("RIGHTPADDING", (0, 0), (-1, -1), 4)]))
    return t


def uk_date(d):
    return str(d.day) + d.strftime(" %B %Y")


# ------------------------------------------------------------------------------------------- the written assurance
def write_assurance(path):
    h1, h1s, h2 = heads(PLUM, "LiberationSerif")
    doc, frame = _doc(path, "Written assurance: Wrenfield & Holt Ltd", W.COUNCIL, "%s  |  Trading Standards Service  |  "
                      "Ref TS/CON/26/0417" % W.COUNCIL)
    s = [Paragraph("Written assurance", h1),
         Paragraph("Given by Wrenfield &amp; Holt Ltd to %s Trading Standards Service. Reference TS/CON/26/0417."
                   % W.COUNCIL, h1s),
         Paragraph("Background", h2),
         Paragraph("Between January and April 2026 the Service received complaints from consumers that refunds for goods "
                   "returned to Wrenfield &amp; Holt Ltd were slow. Regulation 34 of the Consumer Contracts (Information, "
                   "Cancellation and Additional Charges) Regulations 2013 requires a trader to reimburse a consumer who "
                   "withdraws from a sales contract without undue delay, and in any event within 14 days after the day on "
                   "which the trader receives the goods back. Wrenfield &amp; Holt Ltd has met the Service and gives the "
                   "assurance below. It is not an admission that any refund breached the Regulations.", BODY),
         Paragraph("Assurance", h2),
         Paragraph("1.&nbsp;&nbsp;&nbsp;Wrenfield &amp; Holt Ltd will reimburse consumers within the period regulation 34 "
                   "allows.", NUM),
         Paragraph("2.&nbsp;&nbsp;&nbsp;By 30 November 2026 Wrenfield &amp; Holt Ltd will give the Service a return for each "
                   "calendar month from January to June 2026 setting out: (a) the refunds it made in the month for goods "
                   "returned to its Cotterby returns centre; (b) how many of those refunds were made late; (c) that number "
                   "as a percentage of the refunds in (a); (d) whether the month met the commitment in paragraph 4; and "
                   "(e) the value, in pounds, of the goodwill vouchers its customer services team issued in the month.", NUM),
         Paragraph("3.&nbsp;&nbsp;&nbsp;For the return: (i) a refund is made on the date of the payment run that pays it, "
                   "and a refund that fails and is paid again is made on the date of the payment that succeeds; (ii) a "
                   "refund belongs to the month in which it is made; (iii) days are counted as calendar days from the day "
                   "the returned goods were delivered to the Cotterby returns centre, as recorded by the centre's goods-in "
                   "scan in UK time, that day being day 0, and a refund made on day 15 or later is made late.", NUM),
         Paragraph("4.&nbsp;&nbsp;&nbsp;In each month at least 95 per cent of the refunds in paragraph 2(a) will have been "
                   "made by day 14.", NUM),
         Paragraph("5.&nbsp;&nbsp;&nbsp;For each refund made late in January to June 2026, Wrenfield &amp; Holt Ltd will pay "
                   "&pound;15 into the customer goodwill fund administered by the Meridale Consumer Trust, within 28 days of "
                   "giving the return.", NUM),
         Paragraph("6.&nbsp;&nbsp;&nbsp;The Service may ask to see the records the return is drawn from.", NUM),
         Spacer(1, 10),
         _table([["Signed for Wrenfield &amp; Holt Ltd", "Signed for %s" % W.COUNCIL],
                 ["%s<br/>%s<br/>9 October 2026" % (W.PEOPLE["compliance"], W.ROLES["compliance"]),
                  "%s<br/>%s, Trading Standards Service<br/>9 October 2026" % (W.PEOPLE["officer"], W.ROLES["officer"])]],
                [80 * mm, 86 * mm], head="#f1edf0")]
    doc.build(s, onFirstPage=frame, onLaterPages=frame)


# ------------------------------------------------------------------------------------------------ the 2025 review
def write_review(path, monthly):
    """monthly: {(2025, m): (parcels received, parcels opened, refunds made)} from the clean truth."""
    h1, h1s, h2 = heads(SLATE, "LiberationSans")
    doc, frame = _doc(path, "Cotterby returns centre: 2025 in review", W.PEOPLE["centre"],
                      "Wrenfield & Holt  |  Cotterby returns centre  |  Internal", face="LiberationSans")
    rows = [["Month", "Return parcels received", "Parcels opened", "Return refunds paid"]]
    tot = [0, 0, 0]
    for m in range(1, 13):
        a, b, c = monthly[(2025, m)]
        tot = [tot[0] + a, tot[1] + b, tot[2] + c]
        rows.append([dt.date(2025, m, 1).strftime("%B"), "{:,}".format(a), "{:,}".format(b), "{:,}".format(c)])
    rows.append(["2025", "{:,}".format(tot[0]), "{:,}".format(tot[1]), "{:,}".format(tot[2])])
    s = [Paragraph("Cotterby returns centre: 2025 in review", h1),
         Paragraph("%s, %s. February 2026." % (W.PEOPLE["centre"], W.ROLES["centre"]), h1s),
         Paragraph("Volumes", h2),
         Paragraph("The centre received %s return parcels in 2025 and opened %s. January carried the post-Christmas "
                   "returns and the weeks from Black Friday to Christmas the second peak of the year; both were worked with "
                   "agency cover beside the core team." % ("{:,}".format(tot[0]), "{:,}".format(tot[1])), SANS),
         _table(rows, [42 * mm, 42 * mm, 36 * mm, 40 * mm], head="#e3e8ec"),
         Paragraph("Team", h2),
         Paragraph("The core team is 74 colleagues across the early, late and weekend shifts. The agency contract that "
                   "covered the peaks ended on 31 December 2025 and was not renewed in the 2026 budget; the centre starts "
                   "2026 on its core team, with overtime available from the second half of February.", SANS),
         Paragraph("2026", h2),
         Paragraph("Priorities are the refund promise on the website, the new goods-in scanner software going live on "
                   "1 January, and the grading guide refresh for footwear.", SANS)]
    doc.build(s, onFirstPage=frame, onLaterPages=frame)


# ----------------------------------------------------------------------------------- the daily operations workbook
def write_dailyops(path, rows):
    from openpyxl import Workbook
    from openpyxl.styles import Font
    wb = Workbook()
    ws = wb.active
    ws.title = "Daily sheet"
    ws.append(["Date", "Parcels booked in", "Parcels opened", "Refunds triggered", "Waiting at close (bay count)",
               "Team on shift"])
    for c in ws[1]:
        c.font = Font(bold=True)
    for r in rows:
        ws.append(list(r))
    for row in ws.iter_rows(min_row=2, min_col=1, max_col=1):
        for c in row:
            c.number_format = "dd/mm/yyyy"
    ws.column_dimensions["A"].width = 12
    for col in "BCDEF":
        ws.column_dimensions[col].width = 18
    ws.freeze_panes = "A2"
    wb.save(path)


PROVENANCE = [
    ("goods2025", "Cotterby returns centre goods-in scanner (software in use to 31 December 2025), export of every "
                  "goods-in scan from 2 December 2024", "2026-10-30", "goods-in scans, 2 December 2024 to 31 December 2025"),
    ("goods2026", "Cotterby returns centre goods-in scanner software (live 1 January 2026), event export",
     "2026-10-30", "goods-in scans, 1 January to 28 October 2026"),
    ("processing", "Cotterby returns processing system, record export", "2026-10-30",
     "parcels opened and graded, 2 December 2024 to 28 October 2026"),
    ("refunds", "Wrenfield & Holt finance system, refund ledger export", "2026-10-30",
     "refund payments, 2 December 2024 to 28 October 2026"),
    ("orders", "Wrenfield & Holt order system, extract for customers with a parcel delivered to Cotterby from "
               "1 December 2025 or a 2026 customer case", "2026-10-30", "their orders from 1 October 2025"),
    ("assurance", "Calvermoor County Council Trading Standards Service", "2026-10-09",
     "the written assurance and the return it requires"),
    ("review", "Cotterby returns centre operations manager", "2026-02-11", "the centre's 2025 volumes and team"),
    ("vouchers", "Wrenfield & Holt customer services goodwill voucher system, export", "2026-10-30",
     "vouchers issued 1 January to 28 October 2026"),
    ("redemptions", "Wrenfield & Holt e-commerce platform, voucher redemption export", "2026-10-30",
     "redemptions of 2026 goodwill vouchers"),
    ("cases", "Wrenfield & Holt customer services case system, export", "2026-10-30",
     "customer cases opened 1 January to 28 October 2026"),
    ("dailyops", "Cotterby returns centre shift supervisors' daily sheet", "2026-10-29",
     "daily goods-in, opening and refund counts and the team on shift"),
    ("rota", "Cotterby returns centre rota", "2026-10-29", "2026 shifts with employees and agency colleagues rostered"),
]
