"""The pack's documents: the board's 2027-28 instructional investment grant guidelines, the fiscal 2026 state
appropriations workbook, the data dictionary and the extract manifest."""
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
    ("1. The grant", [
        "The board awards the 2027-28 instructional investment grant, $4.5 million in equal parts, to the five public "
        "four-year reporting units with the lowest instruction expense per FTE student in fiscal 2026. A reporting unit "
        "is a campus with its own federal unit identifier that files its own 12-month enrollment return; the "
        "twenty-six such campuses are in the board's campus code list. The board votes the awards on 19 November 2026 "
        "with the 2027-28 budget request."]),
    ("2. The measure", [
        "Instruction expense per FTE student is a campus's fiscal 2026 instruction expense (July 2025 to June 2026, "
        "the functional expense for instruction on the federal finance return) over its 2025-26 12-month FTE students "
        "from the federal 12-month enrollment return, undergraduate FTE plus graduate FTE.",
        "Instruction expense is the campus's own. A branch campus whose finances are reported within its parent's "
        "return is ranked on the instruction expense of the branch itself, which its parent's return includes, and the "
        "parent is ranked on its own, without its branches'. No campus's fiscal 2026 return is restated for the grant."]),
    ("3. Alongside the awards", [
        "From fiscal 2027 each branch campus files its own finance return. For each of the six branch campuses the "
        "board will also see its fall 2026 FTE students, undergraduate credit hours over 15 plus graduate credit hours "
        "over 12 at the fall census, and its unduplicated fall 2026 headcount, from the board's fall census file, as "
        "the base of the branches' first returns."]),
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
                          bottomMargin=0.9 * inch, title="Instructional investment grant guidelines, 2027-28",
                          author="John Huang", subject="", creator="", producer="")
    head = [["To", "Board members and campus finance officers"], ["From", "John Huang, Director of Finance Policy"],
            ["Date", "1 October 2026"], ["Subject", "Instructional investment grant, 2027-28: basis of the awards"]]
    t = Table([[Paragraph(a, CELLB), Paragraph(b, CELL)] for a, b in head], colWidths=[0.9 * inch, 5.6 * inch],
              hAlign="LEFT")
    t.setStyle(TableStyle([("LINEBELOW", (0, -1), (-1, -1), 0.6, INK), ("LEFTPADDING", (0, 0), (-1, -1), 0),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]))
    story = _masthead("Guidelines") + [t, Spacer(1, 8)]
    for h, paras in MEMO:
        story.append(Paragraph(h, H2))
        for p in paras:
            story.append(Paragraph(p, BODY))
    foot = "%s. Instructional investment grant guidelines, 2027-28; 1 October 2026." % P.COMPANY
    d.build(story, onFirstPage=_frame(foot), onLaterPages=_frame(foot))


def write_approp(path, x):
    import openpyxl
    from openpyxl.styles import Font, PatternFill
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "FY2026 appropriations"
    ws["A1"] = "%s: fiscal 2026 state general fund appropriations to public four-year campuses" % P.COMPANY
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = "As enacted, July 2025. Branch campus appropriations are made to the campus, not to its parent."
    ws.append([])
    ws.append(["Campus code", "Campus", "Operating appropriation ($)", "Of which: performance funding ($)",
               "Capital renewal ($)"])
    for c in ws[4]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor="2C5A3F")
    rng = np.random.default_rng(W.SEED + 9)
    for u in W.IDS:
        op = round(x["inst"][u] * float(rng.uniform(0.42, 0.58)), -3)
        ws.append([x["code"][u], W.NAME[u], op, round(op * float(rng.uniform(0.04, 0.08)), -3),
                   round(op * float(rng.uniform(0.02, 0.05)), -3)])
    for row in ws.iter_rows(min_row=5):
        for c in row[2:5]:
            c.number_format = "#,##0"
    for col, w in zip("ABCDE", (12, 40, 18, 20, 16)):
        ws.column_dimensions[col].width = w
    ws.freeze_panes = "A5"
    wb.save(path)


DICT_COLS = ["file_name", "field", "description"]


def dictionary_rows():
    f = P.FILES
    return [
        (f["hd"], "UNITID", "the federal unit identifier"),
        (f["hd"], "SECTOR", "1 public four-year or above"),
        (f["hd"], "C21BASIC", "Carnegie basic classification (2021)"),
        (f["f1a"], "PRCH_F", "parent/child indicator for finance: 1 parent reporting for itself and others, 2 child "
                             "whose finance is reported by its parent, blank reports for itself only"),
        (f["f1a"], "IDX_F", "the UNITID of the parent reporting the child's finance"),
        (f["f1a"], "F1C011", "instruction, total expense, dollars"),
        (f["f1a"], "F1C021", "research, total expense, dollars"),
        (f["f1a"], "F1C031", "public service, total expense, dollars"),
        (f["f1a"], "F1C051", "academic support, total expense, dollars"),
        (f["f1a"], "F1C061", "student services, total expense, dollars"),
        (f["f1a"], "F1C071", "institutional support, total expense, dollars"),
        (f["f1a"], "F1C191", "total expenses and deductions, dollars"),
        (f["e12"], "EFYTOTLT", "12-month unduplicated headcount, 2025-26"),
        (f["e12"], "CDACTUA", "undergraduate credit hour activity, 2025-26"),
        (f["e12"], "CDACTGA", "graduate credit hour activity, 2025-26"),
        (f["e12"], "FTEUG", "12-month undergraduate FTE (credit hours over 30)"),
        (f["e12"], "FTEGD", "12-month graduate FTE (credit hours over 24)"),
        (f["codes"], "campus_code", "the board's campus code"),
        (f["ch"], "term", "2025FA fall 2025, 2026SP spring 2026, 2026SU summer 2026"),
        (f["ch"], "course_level", "Lower division (1000 and 2000 level), Upper division (3000 and 4000), Graduate"),
        (f["ch"], "student_credit_hours", "credit hours of the students enrolled at the census date"),
        (f["census"], "student_id", "the campus student information system's id"),
        (f["census"], "crn", "the course reference number"),
        (f["census"], "credit_hours", "the course's credit hours"),
        (f["tuition"], "resident_tuition_fees", "2026-27 annual resident tuition and required fees, dollars"),
        (f["grad"], "GRRT150", "graduation rate within 150 per cent of normal time, per cent"),
    ]


MANIFEST_COLS = ["file_name", "contents", "provided_by", "as_of_date", "coverage", "record_count"]


def manifest_rows(n):
    f = P.FILES
    return [
        (f["hd"], "institutional directory", "IPEDS, board extract", "2026-09-15", "2025-26", n["hd"]),
        (f["f1a"], "finance return, public institutions", "IPEDS, board collection", "2026-10-01", "fiscal 2026",
         n["f1a"]),
        (f["e12"], "12-month enrollment return", "IPEDS, board collection", "2026-10-01", "2025-26", n["e12"]),
        (f["codes"], "campus code list", P.COMPANY, "2026-07-01", "", n["codes"]),
        (f["ch"], "student credit hours by level", P.COMPANY, "2026-08-20", "2025-26 terms", n["ch"]),
        (f["census"], "fall census enrollment, branch campuses", P.COMPANY, "2026-10-09", "fall 2026", n["census"]),
        (f["guide"], "grant guidelines", P.COMPANY, "2026-10-01", "2027-28", ""),
        (f["approp"], "state appropriations", P.COMPANY, "2025-07-15", "fiscal 2026", 26),
        (f["tuition"], "tuition and required fees", P.COMPANY, "2026-06-30", "2026-27", n["tuition"]),
        (f["grad"], "graduation rates", "IPEDS", "2026-02-10", "2019 cohort", n["grad"]),
        (f["dictionary"], "field descriptions", P.COMPANY, "2026-10-09", "", n["dictionary"]),
    ]
