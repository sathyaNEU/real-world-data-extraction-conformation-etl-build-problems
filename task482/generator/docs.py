"""The pack's documents: the management board paper on third-quarter 2026 timeliness, the office staffing workbook,
the data dictionary and the extract manifest."""
import datetime as dt

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                      # noqa: E402
from reportlab.lib.pagesizes import letter                                            # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                       # noqa: E402
from reportlab.lib.units import inch                                                  # noqa: E402
from reportlab.pdfbase import pdfmetrics                                              # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                          # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import numpy as np    # noqa: E402

import pack as P      # noqa: E402
import world as W     # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("LiberationSerif", "Regular"), ("LiberationSerif-Bold", "Bold"), ("LiberationSans", "Regular"),
              ("LiberationSans-Bold", "Bold")):
    try:
        pdfmetrics.getFont(nm)
    except KeyError:
        pdfmetrics.registerFont(TTFont(nm, FONT_DIR + nm.split("-")[0] + "-" + f + ".ttf"))
INK = colors.HexColor("#1b2430")
GREY = colors.HexColor("#5b6470")
GREEN = colors.HexColor("#2c5a3f")
BODY = ParagraphStyle("body", fontName="LiberationSerif", fontSize=10.3, leading=13.8, textColor=INK, spaceAfter=6)
SMALL = ParagraphStyle("small", fontName="LiberationSerif", fontSize=8.6, leading=11.2, textColor=GREY, spaceAfter=4)
CELL = ParagraphStyle("cell", fontName="LiberationSans", fontSize=8.4, leading=10.6, textColor=INK)
CELLB = ParagraphStyle("cellb", fontName="LiberationSans-Bold", fontSize=8.4, leading=10.6, textColor=INK)
H2 = ParagraphStyle("h2", fontName="LiberationSans-Bold", fontSize=10.6, leading=14, textColor=INK, spaceBefore=8,
                    spaceAfter=4)

MEMO = [
    ("1. Purpose", [
        "At its meeting on 4 November 2026 the management board decides which regional offices go on a timeliness "
        "improvement plan for 2027, with a staffing review and monthly reporting to the board. This paper fixes the "
        "basis of the choice."]),
    ("2. The test", [
        "An office goes on a plan when the median number of working days from a complete application to registration, "
        "for the applications it received from 1 July to 30 September 2026, exceeds 20.",
        "The clock starts on the day the application is complete, its day of receipt or, where the office raised a "
        "query, the day the last reply arrived, and stops on the day of registration; the start day is not counted. "
        "Working days exclude Saturdays, Sundays and the public holidays in the office's calendar. Every application "
        "the office received in the quarter counts, those registered by the 9 October extract and those still open "
        "on it."]),
    ("3. The evidence", [
        "The registrations made in July are in the legacy system, which the offices used until 31 July, and every "
        "later registration is in the case system, to which the applications still in hand were moved on 1 August; "
        "the applications still open on 9 October are in the case system's open caseload snapshot."]),
    ("4. Alongside the decision", [
        "The board will also see each office's card payments made in the quarter, their number and amount, as the "
        "fee income the plans will be costed against."]),
]


def _frame(foot):
    def frame(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(GREY)
        canvas.setFont("LiberationSans", 7.2)
        canvas.drawString(0.85 * inch, 0.55 * inch, foot)
        canvas.drawRightString(letter[0] - 0.85 * inch, 0.55 * inch, "Page %d" % doc.page)
        canvas.restoreState()
    return frame


def _masthead(title):
    return [Paragraph(P.COMPANY.upper(), ParagraphStyle("o", fontName="LiberationSans-Bold", fontSize=8.4,
                                                        textColor=GREEN, leading=11)),
            Paragraph(title, ParagraphStyle("t", fontName="LiberationSans-Bold", fontSize=14, leading=18,
                                            textColor=INK, spaceAfter=6))]


def write_memo(path):
    d = SimpleDocTemplate(path, pagesize=letter, leftMargin=0.85 * inch, rightMargin=0.85 * inch, topMargin=0.8 * inch,
                          bottomMargin=0.9 * inch, title="Registration timeliness, third quarter 2026",
                          author="Eunan Reid", subject="", creator="", producer="")
    head = [["To", "Management board"], ["From", "Eunan Reid, Head of Registration Services"],
            ["Date", "9 October 2026"], ["Subject", "Registration timeliness, third quarter 2026: improvement plans"]]
    t = Table([[Paragraph(a, CELLB), Paragraph(b, CELL)] for a, b in head], colWidths=[0.9 * inch, 5.6 * inch],
              hAlign="LEFT")
    t.setStyle(TableStyle([("LINEBELOW", (0, -1), (-1, -1), 0.6, INK), ("LEFTPADDING", (0, 0), (-1, -1), 0),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]))
    story = _masthead("Board paper") + [t, Spacer(1, 8)]
    for h, paras in MEMO:
        story.append(Paragraph(h, H2))
        for p in paras:
            story.append(Paragraph(p, BODY))
    foot = "%s. Board paper MB/26/58, 9 October 2026." % P.COMPANY
    d.build(story, onFirstPage=_frame(foot), onLaterPages=_frame(foot))


def write_staff(path, x):
    import openpyxl
    from openpyxl.styles import Font, PatternFill
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Staffing September 2026"
    ws["A1"] = "%s: registration staff by office, September 2026" % P.COMPANY
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = "Full-time equivalents in post on 30 September 2026."
    ws.append([])
    ws.append(["Office", "Office name", "Registration officers (FTE)", "Vacancies (FTE)", "Agency staff (FTE)"])
    for c in ws[4]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor="2C5A3F")
    rng = np.random.default_rng(W.SEED + 9)
    for code, name, n, *_ in W.OFFICES:
        ws.append([code, name, round(n / 160 * float(rng.uniform(0.8, 1.2)), 1), round(float(rng.uniform(0, 3)), 1),
                   round(float(rng.uniform(0, 2)), 1)])
    for col, w in zip("ABCDE", (10, 16, 24, 16, 18)):
        ws.column_dimensions[col].width = w
    ws.freeze_panes = "A5"
    wb.save(path)


DICT_COLS = ["file_name", "field", "description"]


def dictionary_rows():
    f = P.FILES
    return [
        (f["log_old"], "Office", "the office's two-letter code"),
        (f["log_old"], "Received", "the day the application was received, DD/MM/YYYY"),
        (f["log_old"], "QueryRaised", "Y if the office raised a query on the application"),
        (f["log_old"], "Complete", "the day the application was complete (receipt, or the last reply to a query)"),
        (f["log_old"], "Registered", "the day the company was registered"),
        (f["log_new"], "clock_start", "the day the application was complete"),
        (f["log_new"], "service", "standard or two-day (the higher fee)"),
        (f["open"], "open_applications", "applications received on the day, complete on clock_start and not "
                                         "registered at the snapshot"),
        (f["pays"], "settled_on", "the day the acquirer settled the payment to the office's account"),
        (f["pays"], "batch_id", "the acquirer's settlement batch"),
        (f["batches"], "terminal_date", "the day the batch's payments were taken at the office's terminals and website"),
        (f["batches"], "settled_on", "the day the batch was settled"),
        (f["survey"], "satisfied_pct", "share of respondents satisfied or very satisfied, per cent"),
    ]


MANIFEST_COLS = ["file_name", "contents", "provided_by", "as_of_date", "coverage", "record_count"]


def manifest_rows(n):
    f = P.FILES
    return [
        (f["log_old"], "registrations, legacy system", "registration services", "2026-08-03",
         "registrations made in July 2026", n["log_old"]),
        (f["log_new"], "registrations, case system", "registration services", "2026-10-09",
         "registrations made from 1 August 2026", n["log_new"]),
        (f["open"], "open caseload snapshot", "registration services", "2026-10-09", "third-quarter receipts", n["open"]),
        (f["holidays"], "public holidays", P.COMPANY, "2025-12-01", "2026", n["holidays"]),
        (f["pays"], "card payments as settled", "finance", "2026-10-09", "settled 1 July to 9 October 2026", n["pays"]),
        (f["batches"], "card settlement batches", "finance", "2026-10-09", "settled 1 July to 9 October 2026",
         n["batches"]),
        (f["paper"], "board paper", P.COMPANY, "2026-10-09", "", ""),
        (f["staff"], "office staffing", "human resources", "2026-09-30", "", 14),
        (f["survey"], "customer survey", P.COMPANY, "2026-07-20", "January to June 2026", n["survey"]),
        (f["dictionary"], "field descriptions", P.COMPANY, "2026-10-09", "", n["dictionary"]),
    ]
