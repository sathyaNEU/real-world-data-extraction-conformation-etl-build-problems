"""The pack's documents and workbooks: Pellmore's June 2025 technical report, the Office's Form 26A memo, the program
review rule, Arcwright's scoring QC workbook and administration summary, the item maps, the programs' Title II
completer lists, and the test framework."""
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
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import pack as P     # noqa: E402
import sim as S      # noqa: E402
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
PLUM = colors.HexColor("#4a2f5c")
NAVY = colors.HexColor("#1f3a5f")
FOREST = colors.HexColor("#24513a")
RUST = colors.HexColor("#7a3b1d")
SANS = ParagraphStyle("sans", fontName="LiberationSans", fontSize=9.6, leading=13.2, textColor=INK, spaceAfter=6)
SERIF = ParagraphStyle("serif", fontName="LiberationSerif", fontSize=10.5, leading=14.2, textColor=INK, spaceAfter=6)
CELL = ParagraphStyle("cell", fontName="LiberationSans", fontSize=8.4, leading=10.4, textColor=INK)
CELLB = ParagraphStyle("cellb", parent=CELL, fontName="LiberationSans-Bold")
SMALL = ParagraphStyle("small", fontName="LiberationSans", fontSize=8.3, leading=10.8, textColor=GREY)
HEAD_FILL = PatternFill("solid", fgColor="DCE6F0")


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


def _table(rows, widths, head="#e6eef0", font=None, align_right=()):
    data = [[Paragraph(str(v), CELLB if i == 0 else (font or CELL)) for v in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9aa0a6")),
                           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(head)),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 4),
                           ("RIGHTPADDING", (0, 0), (-1, -1), 4)]))
    return t


def pct(a, b):
    return "%.1f" % (100.0 * a / b) if b else "-"


# ----------------------------------------------------------------------------------- statistics the documents quote
def stats(x):
    """the figures the 2025 report and Arcwright's documents state, computed from the records they describe"""
    out = {}
    s25 = x["scored"][2025]
    agree25 = []
    r = S.rng(x["seed"], 21)
    for a in range(W.N_WA):
        d = np.abs(s25["r1"][:, a] - s25["r2"][:, a])
        # Pellmore's 2025 validity papers, read by the 2025 raters against their own consensus
        base = r.normal(0.1, 1.0, 900) - x["f25"]["wa"][a]
        cons = S.rating(base)
        reads = S.rating(base + r.normal(0, W.RATER_SD, 900))
        agree25.append((100 * (d == 0).mean(), 100 * (d <= 1).mean(), 100 * (d > 1).mean(),
                        100 * (reads == cons).mean(), 100 * (np.abs(reads - cons) <= 1).mean()))
    out["agree25"] = agree25
    f = s25["first"]
    out["n25"], out["n25_first"] = len(s25["idx"]), int(f.sum())
    out["pass25_first"] = 100 * (s25["raw"][f] >= W.PASS_RAW_25A).mean()
    out["pass25_all"] = 100 * (s25["raw"] >= W.PASS_RAW_25A).mean()
    return out


def qc_tables(x, reads):
    """Arcwright's scoring statistics by assignment, from its read records"""
    by = {}
    for _rid, resp, wa, typ, reader, score, _t in reads:
        by.setdefault((resp, wa), {}).setdefault(typ, []).append(score)
    papers = {p["id"]: p for p in x["papers"]}
    summary = []
    for wa in ("WA1", "WA2", "WA3"):
        pairs = [(v["FIRST"][0], v["SECOND"][0], v.get("RESOLUTION"), v.get("BACKREAD")) for (resp, w), v in by.items()
                 if w == wa and "FIRST" in v]
        n = len(pairs)
        exact = sum(1 for a, b, _, _ in pairs if a == b)
        adj = sum(1 for a, b, _, _ in pairs if abs(a - b) <= 1)
        res = sum(1 for _, _, c, _ in pairs if c)
        br = [(a, b, c[0] if c else None, d[0]) for a, b, c, d in pairs if d]
        br_ok = sum(1 for a, b, c, d in br if abs(d - (c if c else (a + b) / 2.0)) <= 0.5)
        val = [(score, papers[resp]["consensus"]) for (resp, w), v in by.items() if w == wa and "VALIDITY" in v
               for score in v["VALIDITY"]]
        npap = len({resp for (resp, w), v in by.items() if w == wa and "VALIDITY" in v})
        summary.append([wa, n, 2 * n + res, round(100.0 * exact / n, 1), round(100.0 * adj / n, 1),
                        round(100.0 * res / n, 1), len(br), round(100.0 * br_ok / len(br), 1), npap, len(val),
                        round(100.0 * sum(1 for a, c in val if a == c) / len(val), 1),
                        round(100.0 * sum(1 for a, c in val if abs(a - c) <= 1) / len(val), 1)])
    readers = {}
    for _rid, resp, wa, typ, reader, score, _t in reads:
        d = readers.setdefault(reader, dict(op=0, val=0, val_exact=0, first=None))
        if typ in ("FIRST", "SECOND", "RESOLUTION", "BACKREAD"):
            d["op"] += 1
        if typ == "VALIDITY":
            d["val"] += 1
            d["val_exact"] += int(score == papers[resp]["consensus"])
        d["first"] = min(d["first"], _t[:10]) if d["first"] else _t[:10]
    rrows = [[k, "Scoring leader" if k.startswith("SL") else "Rater", v["first"], v["op"], v["val"],
              round(100.0 * v["val_exact"] / v["val"], 1) if v["val"] else None] for k, v in sorted(readers.items())]
    return summary, rrows


# ------------------------------------------------------------------------------------ Pellmore's 2025 technical report
def write_tr2025(path, x, st):
    h1, h1s, h2 = styles(NAVY, serif=True)
    d, frame = _doc(path, "Elementary Literacy Instruction (ELI 104): June 2025 administration, Form 25A, technical "
                    "report", W.OLD_CO, "Pellmore Testing  |  ELI 104 Technical Report, June 2025 administration",
                    layout="centre")
    a = st["agree25"]
    qc = [["Assignment", "Exact agreement, two reads (%)", "Adjacent or exact (%)", "Resolved by a scoring leader (%)",
           "Validity papers, exact (%)", "Validity papers, adjacent or exact (%)"]]
    for i, wa in enumerate(("WA1", "WA2", "WA3")):
        qc.append([wa, "%.1f" % a[i][0], "%.1f" % a[i][1], "%.1f" % a[i][2], "%.1f" % a[i][3], "%.1f" % a[i][4]])
    conv = P.conversion_rows()
    half = (len(conv) + 1) // 2
    ctab = [["Raw", "Scale", "Raw", "Scale"]] + [[conv[i][0], conv[i][1]] + (conv[i + half] if i + half < len(conv)
                                                                            else ["", ""]) for i in range(half)]
    s = [Paragraph("Elementary Literacy Instruction (ELI 104)", h1),
         Paragraph("June 2025 administration, Form 25A: technical report. Prepared for the %s by %s, September 12, "
                   "2025." % (W.BOARD, W.OLD_CO), h1s),
         Paragraph("1. The administration", h2),
         Paragraph("The test was given once in 2025, on Saturday, June 14, at the six test centres the Board "
                   "approves. %s candidates sat Form 25A, %s of them for the first time. This report covers the "
                   "scoring of the written assignments, the equating of Form 25A to the reporting scale and the "
                   "results. Candidate-level results went to the Board in the June 2025 score file." % (
                       "{:,}".format(st["n25"]), "{:,}".format(st["n25_first"])), SERIF),
         Paragraph("2. The test", h2),
         Paragraph("Each form has 60 multiple-choice items in four subareas and three written assignments: WA1, an "
                   "analysis of a student's foundational reading assessment; WA2, a comprehension instruction plan; "
                   "and WA3, written feedback on a student's draft. A multiple-choice item scores one point. Each "
                   "assignment is read by two raters working independently on the four-point scoring guide, and its score is "
                   "the sum of the two reads (2 to 8). When the two reads differ by more than one point a scoring "
                   "leader reads the response, and the assignment's score is twice the leader's read. Each assignment "
                   "score counts twice, so a form's raw score is the multiple-choice score plus twice the three "
                   "assignment scores, 0 to 108.", SERIF),
         Paragraph("3. Scoring the written assignments", h2),
         Paragraph("Raters are trained and qualified on each assignment's scoring guide and benchmark papers before they read "
                   "operational responses. Validity papers (responses with consensus scores set by the scoring "
                   "leaders) are seeded into raters' queues throughout scoring. Table 1 gives the 2025 agreement "
                   "rates.", SERIF),
         Paragraph("Table 1. Written-assignment agreement, June 2025", SMALL),
         _table(qc, [0.85 * inch, 1.05 * inch, 0.95 * inch, 1.1 * inch, 1.0 * inch, 1.15 * inch]),
         Spacer(1, 6),
         Paragraph("4. Equating", h2),
         Paragraph("Form 25A was equated to Form 24A under the common-item nonequivalent groups design, through an "
                   "internal anchor of 20 multiple-choice items and one written assignment that Form 25A carries from "
                   "Form 24A. The anchor is assembled to represent the test's content and its two item formats in "
                   "proportion: one in three of the multiple-choice items and one of the three assignments. The "
                   "equating samples are each form's first-attempt candidates. A new form's raw scores are equated to "
                   "the raw scores of the form before it; each equated raw score is rounded to a whole number and "
                   "converted to the reporting scale with that form's raw-to-scale table. Form 25A's table is in "
                   "Appendix A.", SERIF),
         Paragraph("5. The passing standard", h2),
         Paragraph("The Board set the passing standard at a scale score of 240 in 2021. On Form 25A it falls at a raw "
                   "score of %d." % W.PASS_RAW_25A, SERIF),
         Paragraph("6. Results", h2),
         Paragraph("Of the first-attempt candidates, %.1f per cent passed; of all candidates, %.1f per cent." % (
             st["pass25_first"], st["pass25_all"]), SERIF),
         Paragraph("Item positions and identifiers for Form 25A are in the Board's item map workbook.", SMALL),
         PageBreak(),
         Paragraph("Appendix A. Form 25A raw-to-scale conversion", h2),
         _table(ctab, [0.8 * inch, 0.8 * inch, 0.8 * inch, 0.8 * inch])]
    d.build(s, onFirstPage=frame, onLaterPages=frame)


# --------------------------------------------------------------------------------------- the Office's Form 26A memo
def write_memo(path, x):
    h1, h1s, h2 = styles(PLUM)
    d, frame = _doc(path, "Form 26A: assembly and the 2026 conversion", W.OFFICE,
                    W.BOARD + "  |  " + W.OFFICE, layout="top")
    s = [Paragraph("Memorandum", h1),
         Paragraph("To: Educator Preparation and Licensure staff; %s<br/>From: %s, Director, %s<br/>Date: February 9, "
                   "2026<br/>Re: ELI 104 Form 26A, assembly and the 2026 conversion" % (
                       W.NEW_CO, W.PEOPLE["director"], W.OFFICE), h1s),
         Paragraph("1. Form 26A is assembled from the item bank to the test specifications: 60 multiple-choice items "
                   "and three written assignments, given at the June 13, 2026 administration. It carries 20 "
                   "multiple-choice items and one assignment, WA2 (the comprehension instruction plan), from Form 25A. "
                   "Like the anchor before it, these items are one in three of the multiple-choice items and one of the "
                   "three assignments, 36 of the 108 raw points with 16 of them written, the same mix as the test. The "
                   "carried items sit at different positions on the two forms; the item map workbook gives both forms' "
                   "positions and identifiers.", SANS),
         Paragraph("2. From 2026 the Board's scoring contract is with %s. Arcwright scores the multiple-choice "
                   "items and the written assignments, two independent reads with resolution by a scoring leader as "
                   "before, and delivers the score file, the item response file, its read records and its scoring "
                   "statistics. %s transferred WA2's scoring guide and benchmark papers to Arcwright in January, with a "
                   "set of June 2025 WA2 responses and their scores for Arcwright's validity papers." % (
                       W.NEW_CO, W.OLD_CO), SANS),
         Paragraph("3. This Office equates Form 26A to Form 25A once scoring closes, and the Board releases 2026 scores "
                   "on September 15, 2026, on the reporting scale through Form 25A's conversion. Program pass rates for "
                   "the 2027 reviews follow from the same results.", SANS),
         Paragraph("4. Arcwright registers candidates in its own system. The licensing system matches each registration "
                   "to the candidate's educator record and keeps the match in the registration crosswalk.", SANS)]
    d.build(s, onFirstPage=frame, onLaterPages=frame)


# ------------------------------------------------------------------------------------------------ the review rule
def write_standard(path):
    h1, h1s, h2 = styles(FOREST)
    d, frame = _doc(path, "Rule 8.4: licensure test performance of educator preparation programs", W.BOARD,
                    W.BOARD + "  |  Educator Preparation Program Approval  |  Rule 8.4")
    s = [Paragraph("Rule 8.4. Licensure test performance of elementary preparation programs", h1),
         Paragraph("Adopted by the %s, effective for program years beginning July 1, 2024 and the reviews that follow "
                   "them." % W.BOARD, h1s),
         Paragraph("8.4.1 A program whose completers' first-attempt pass rate on the Elementary Literacy Instruction "
                   "test (ELI 104) is below 70 per cent for a program year is placed on formal program review in the "
                   "calendar year after the program year ends. For the 2025-26 program year the reviews begin in "
                   "2027.", SANS),
         Paragraph("8.4.2 A program year runs from July 1 to June 30. A completer is a candidate the program reports, in "
                   "its Title II completer list for the program year, as having completed its elementary pathway "
                   "(Elementary, or Elementary and Special Education) on a date in the program year. Completers of the "
                   "program's other pathways take other licensure tests and are not counted.", SANS),
         Paragraph("8.4.3 A completer's first attempt is the completer's first attempt at the test, whenever it was "
                   "taken, including an attempt before the program was completed. An attempt the Board voided is not an "
                   "attempt.", SANS),
         Paragraph("8.4.4 The rate counts the completers whose first attempt was at or before the program year's June "
                   "administration (June 13, 2026 for the 2025-26 program year). A completer who had not attempted the "
                   "test by then is not counted.", SANS),
         Paragraph("8.4.5 A first attempt passes when its reported scale score is 240 or more.", SANS),
         Paragraph("8.4.6 The Office of Assessment Research computes the rates from the Board's licensing records and "
                   "the scoring contractor's results, and reports them with the number of completers each rate "
                   "counts.", SANS)]
    d.build(s, onFirstPage=frame, onLaterPages=frame)


# --------------------------------------------------------------------------------------------- the test framework
def write_framework(path):
    h1, h1s, h2 = styles(RUST)
    d, frame = _doc(path, "ELI 104 test framework", W.BOARD, W.BOARD + "  |  ELI 104 Test Framework (2024)")
    sub = [["Subarea", "Approximate share of the multiple-choice items", "What it covers"],
           ["I. Foundational Reading Skills", "30%", "phonological awareness, phonics and word recognition, fluency"],
           ["II. Comprehension and Vocabulary", "30%", "vocabulary development, literary and informational texts"],
           ["III. Assessment and Instruction", "20%", "screening, diagnostic and progress-monitoring assessment; "
                                                      "planning differentiated instruction"],
           ["IV. Writing and Language", "20%", "the writing process, conventions, feedback on student writing"]]
    s = [Paragraph("Elementary Literacy Instruction (ELI 104): test framework", h1),
         Paragraph("Approved by the Board in 2024 for forms given from June 2025.", h1s),
         Paragraph("The test measures the knowledge an entry-level elementary teacher needs to teach reading and "
                   "writing in kindergarten through grade 6. It has 60 multiple-choice items and three written "
                   "assignments, and candidates have four hours.", SANS),
         _table(sub, [1.9 * inch, 1.4 * inch, 3.3 * inch]),
         Spacer(1, 8),
         Paragraph("The written assignments", h2),
         Paragraph("WA1 asks the candidate to analyse one student's foundational reading assessment results and "
                   "identify the student's needs. WA2 asks for a plan of comprehension instruction for a described "
                   "group, with its rationale. WA3 asks for written feedback on a student's draft and the next "
                   "instructional step. Each is scored on a four-point scoring guide: 4, a thorough and accurate response; 3, "
                   "an adequate response; 2, a limited response; 1, a weak response.", SANS)]
    d.build(s, onFirstPage=frame, onLaterPages=frame)


# --------------------------------------------------------------------------------- Arcwright's administration summary
def write_adminsum(path, x, summary):
    h1, h1s, h2 = styles(NAVY)
    d, frame = _doc(path, "ELI 104 June 13, 2026 administration summary", W.NEW_CO,
                    W.NEW_CO + "  |  ELI 104 administration summary  |  July 31, 2026")
    by = {}
    for g in x["regs"]:
        by[g["centre"]] = by.get(g["centre"], 0) + 1
    absent = {c: int(round(v * (0.035 + 0.01 * (int(c[-1]) % 3)))) for c, v in by.items()}
    rows = [["Centre", "Location", "Registered", "Absent", "Tested"]]
    for c, city, _addr in P.CENTRES:
        rows.append([c, city, by.get(c, 0) + absent.get(c, 0), absent.get(c, 0), by.get(c, 0)])
    rows.append(["All", "", sum(by.values()) + sum(absent.values()), sum(absent.values()), sum(by.values())])
    s = [Paragraph("ELI 104: June 13, 2026 administration", h1),
         Paragraph("Administration summary for the %s. %s, July 31, 2026." % (W.BOARD, W.NEW_CO), h1s),
         Paragraph("The June 13 administration ran at all six centres with no centre-wide incident. Every candidate "
                   "who tested was scored; no attempt was withheld or voided.", SANS),
         _table(rows, [0.7 * inch, 1.3 * inch, 1.0 * inch, 0.8 * inch, 0.8 * inch]),
         Spacer(1, 8),
         Paragraph("Scoring", h2),
         Paragraph("Multiple-choice scoring was completed on June 19. Written-assignment scoring ran from June 22 to "
                   "July 16 at Arcwright's scoring centre, with %d raters and %d scoring leaders. The score file, item "
                   "response file, read records and scoring statistics were delivered to the Board on July 24, 27, 29 "
                   "and 31." % (len(P.RATERS), len(P.LEADERS)), SANS),
         Paragraph("Assignment scores are the sum of the two independent reads, or twice a scoring leader's resolution "
                   "read where the two reads differ by more than one point.", SANS)]
    d.build(s, onFirstPage=frame, onLaterPages=frame)


# ------------------------------------------------------------------------------------------------- the workbooks
def _head(ws, cols, widths):
    ws.append(cols)
    for c in ws[1]:
        c.font = Font(bold=True)
        c.fill = HEAD_FILL
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for i, w in enumerate(widths):
        ws.column_dimensions[openpyxl.utils.get_column_letter(i + 1)].width = w
    ws.freeze_panes = "A2"


def write_qc(path, x, summary, readers):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Summary"
    _head(ws, ["Assignment", "Responses scored", "Operational reads", "Exact agreement, first and second read (%)",
               "Adjacent or exact (%)", "Resolved by a scoring leader (%)", "Back-reads", "Back-read agreement (%)",
               "Validity papers", "Validity reads", "Validity exact (%)", "Validity adjacent or exact (%)"],
          [11, 10, 11, 15, 11, 13, 10, 11, 9, 9, 10, 12])
    for r in summary:
        ws.append(r)
    vp = wb.create_sheet("Validity papers")
    _head(vp, ["Paper", "Assignment", "Source", "Score on file"], [18, 11, 66, 10])
    for p in x["papers"]:
        src = ("Form 25A operational response, June 2025 (%s); both June 2025 reads gave this score" % W.OLD_CO
               if p["src"] == "2025" else
               "Form 26A rangefinding response, June 2026; consensus score set by Arcwright's scoring leaders")
        vp.append([p["id"], p["wa"], src, p["consensus"]])
    rd = wb.create_sheet("Readers")
    _head(rd, ["Reader", "Role", "First read", "Operational reads", "Validity reads", "Validity exact (%)"],
          [10, 15, 12, 11, 10, 11])
    for r in readers:
        rd.append(r)
    nt = wb.create_sheet("Notes")
    lines = [("ELI 104, June 13, 2026: written-assignment scoring statistics", True),
             ("%s, delivered to the %s on July 31, 2026." % (W.NEW_CO, W.BOARD), False),
             ("", False),
             ("Exact and adjacent agreement compare the first and second operational reads of each response.", False),
             ("A back-read is a scoring leader's read of a response already scored, for monitoring; it does not change "
              "the score. Back-read agreement counts back-reads within half a point of the response's final score "
              "per read.", False),
             ("Validity papers are responses with a score on file, seeded into raters' queues; a validity read does "
              "not score a candidate. WA2's validity papers are June 2025 responses %s transferred with their scores, "
              "each one whose two June 2025 reads agreed; WA1 and WA3 are new assignments whose papers come from "
              "Arcwright's 2026 rangefinding, scored by consensus of Arcwright's scoring leaders." % W.OLD_CO, False),
             ("Contract targets: exact agreement 60 per cent or more and adjacent or exact 95 per cent or more on "
              "operational reads and on validity reads, for each assignment.", False)]
    for i, (t, b) in enumerate(lines, 1):
        c = nt.cell(row=i, column=1, value=t or None)
        c.font = Font(bold=b, size=12 if b else 10)
        c.alignment = Alignment(wrap_text=True, vertical="top")
    nt.column_dimensions["A"].width = 110
    wb.save(path)


def write_maps(path, x):
    wb = openpyxl.Workbook()
    first = True
    for yr in (2025, 2026):
        ws = wb.active if first else wb.create_sheet()
        first = False
        ws.title = "Form %s" % W.FORMS[yr]
        _head(ws, ["Position", "Item ID", "Item type", "Subarea"], [9, 12, 16, 32])
        for pos, iid, sub in x["maps"][yr]:
            ws.append([pos, iid, "Multiple choice", sub])
        for k, wid in enumerate(x["wa_ids"][yr]):
            ws.append([W.N_MC + k + 1, wid, "Written assignment", "WA%d" % (k + 1)])
    nt = wb.create_sheet("Notes")
    for i, t in enumerate(["ELI 104 item maps, Forms 25A and 26A (Office of Assessment Research, February 2026)",
                           "Position is the item's place on the form as delivered; an item keeps its identifier on "
                           "every form that uses it.",
                           "Written assignments follow the multiple-choice items and are listed by position."], 1):
        nt.cell(row=i, column=1, value=t).font = Font(bold=(i == 1))
    nt.column_dimensions["A"].width = 100
    wb.save(path)


def write_completers(path, sheets):
    wb = openpyxl.Workbook()
    first = True
    for k, (lay, rows) in sorted(sheets.items()):
        name, code, kind = W.PROGRAMS[k][0], W.PROGRAMS[k][1], W.PROGRAMS[k][2]
        ws = wb.active if first else wb.create_sheet()
        first = False
        ws.title = code
        ws.append([name])
        ws.append(["Title II program completers, program year 2025-26 (July 1, 2025 to June 30, 2026)"])
        ws.append(["Submitted %s" % (dt.date(2026, 7, 14) + dt.timedelta(days=(k * 5) % 19)).strftime("%B %d, %Y")
                   .replace(" 0", " ")])
        ws.append([])
        cols = P.LAYOUTS[lay]
        ws.append(cols)
        for c in ws[5]:
            c.font = Font(bold=True)
        ws["A1"].font = Font(bold=True, size=12)
        for r in rows:
            ws.append(r)
        for i, w in enumerate((22, 22, 20, 30, 18, 18)[:len(cols)]):
            ws.column_dimensions[openpyxl.utils.get_column_letter(i + 1)].width = w
    wb.save(path)
