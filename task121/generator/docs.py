"""The pack's documents for task121: the quality assurance program's measures and definitions and the protocol software
release note (PDF), and the centre reference workbook (XLSX). No file describes the data (dataset-generation section
3): each export carries its own conventions and the program files what the centre itself defines."""
from __future__ import annotations

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                    # noqa: E402
from reportlab.lib.pagesizes import LETTER                                          # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                     # noqa: E402
from reportlab.lib.units import inch                                                # noqa: E402
from reportlab.pdfbase import pdfmetrics                                            # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                        # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, TableStyle      # noqa: E402

import common as K   # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("Sans", "LiberationSans-Regular"), ("Sans-B", "LiberationSans-Bold"), ("Sans-I", "LiberationSans-Italic")):
    pdfmetrics.registerFont(TTFont(nm, FONT_DIR + f + ".ttf"))
pdfmetrics.registerFontFamily("Sans", normal="Sans", bold="Sans-B", italic="Sans-I", boldItalic="Sans-B")
INK, GREY, RULE = colors.HexColor("#1b2430"), colors.HexColor("#56616c"), colors.HexColor("#b8c0c8")
NAVY = colors.HexColor("#1f3a5f")
RED = colors.HexColor("#8a2a1f")


def styles(accent=NAVY):
    body = ParagraphStyle("b", fontName="Sans", fontSize=9.8, leading=13.4, textColor=INK, spaceAfter=5)
    return dict(
        body=body,
        h1=ParagraphStyle("h1", fontName="Sans-B", fontSize=14.5, leading=18, textColor=accent, spaceAfter=2),
        h2=ParagraphStyle("h2", fontName="Sans-B", fontSize=10.6, leading=14, textColor=INK, spaceBefore=8,
                          spaceAfter=2, keepWithNext=1),
        meta=ParagraphStyle("m", fontName="Sans", fontSize=8.4, leading=11.2, textColor=GREY, spaceAfter=9),
        cell=ParagraphStyle("c", fontName="Sans", fontSize=8.2, leading=10.4, textColor=INK),
        cellb=ParagraphStyle("cb", fontName="Sans-B", fontSize=8.2, leading=10.4, textColor=INK),
        clause=ParagraphStyle("p", parent=body, leftIndent=28, firstLineIndent=-28),
        bullet=ParagraphStyle("u", parent=body, leftIndent=14, firstLineIndent=-9, spaceAfter=3))


def _frame(left, right):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(GREY)
        canvas.setFont("Sans", 7.4)
        canvas.drawString(0.8 * inch, LETTER[1] - 0.5 * inch, left)
        canvas.drawRightString(LETTER[0] - 0.8 * inch, LETTER[1] - 0.5 * inch, right)
        canvas.drawRightString(LETTER[0] - 0.8 * inch, 0.45 * inch, "Page %d" % doc.page)
        canvas.restoreState()
    return draw


def _table(S, rows, widths):
    data = [[Paragraph(str(c), S["cellb"] if i == 0 else S["cell"]) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=[w * inch for w in widths], repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), .6, INK), ("LINEBELOW", (0, -1), (-1, -1), .4, RULE),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 1.8),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 1.8)]))
    return t


def _clause(S, num, text):
    return Paragraph("<b>%s</b>&nbsp;&nbsp;%s" % (num, text), S["clause"])


def _doc(path, title, author, subject, left, right):
    return SimpleDocTemplate(path, pagesize=LETTER, leftMargin=0.8 * inch, rightMargin=0.8 * inch,
                             topMargin=0.8 * inch, bottomMargin=0.75 * inch, title=title, author=author,
                             subject=subject, creator=author, producer=author), _frame(left, right)


# ------------------------------------------------------------------------------------------------ QA program
QA_5_1 = ("Every cardiac arrest call is reviewed from its recording, and the reviewer times each event from the start of "
          "the recording. Time to first compression runs from the call being answered to the first chest compression "
          "the call-taker coached.")


def write_program(path):
    S = styles()
    title = "Quality Assurance Program: Measures and Definitions"
    doc, fr = _doc(path, title, K.PEOPLE["qa"], "Quality assurance", K.CENTRE, "QA program, effective 1 July 2025")
    st = [Paragraph(title, S["h1"]),
          Paragraph("%s. Effective 1 July 2025. Prepared by %s, Quality Assurance Manager; approved by %s, EMS "
                    "Medical Director, for the %s." % (K.CENTRE, K.PEOPLE["qa"], K.PEOPLE["md"], K.COMMITTEE_NAME),
                    S["meta"]),
          Paragraph("1. The program", S["h2"]),
          _clause(S, "1.1", "The quality assurance program reports the centre's call-taking measures to the EMS "
                            "Quality Committee each month. When a measure moves, the program reports what caused the "
                            "move: the cause is the change without which the measure would have stayed where it was."),
          _clause(S, "1.2", "Months are the centre's calendar months in local time (US Central). A call belongs to "
                            "the month in which it was answered, or for a call never answered, the month in which it "
                            "arrived."),
          Paragraph("2. Triage", S["h2"]),
          _clause(S, "2.1", "A medical call is dispatched hot (lights and sirens) at a determinant of level D or E, "
                            "and cold at a determinant of level O, A, B or C, under the county's EMS response plan."),
          _clause(S, "2.2", "A medical call is under-triaged when it was dispatched cold and the crew assessed a "
                            "patient on it at acuity 1 (critical) or 2 (emergent). The under-triage rate is the "
                            "under-triaged calls over the medical calls on which the crew assessed a patient at "
                            "acuity 1 or 2. A call counts once, at its most acute patient."),
          _clause(S, "2.3", "The crew's acuity is the acuity on the electronic patient care record, matched to the "
                            "call by its incident number."),
          Paragraph("3. Call processing", S["h2"]),
          _clause(S, "3.1", "Call processing time runs from the call being answered to the first ambulance being "
                            "assigned to it."),
          _clause(S, "3.2", "The program reports each month's 90th percentile: the month's medical calls in order of "
                            "their processing time, the time of the call at rank 0.9 times the number of calls, "
                            "rounded up."),
          Paragraph("4. Answering", S["h2"]),
          _clause(S, "4.1", "The centre answers to the national standard: 90 per cent of 911 calls answered within "
                            "15 seconds of arriving at the centre."),
          _clause(S, "4.2", "The share is the month's 911 calls answered within 15 seconds of arriving (15 seconds "
                            "or less) over the month's 911 calls answered. A call abandoned before it was answered is "
                            "reported on its own and is not in the share."),
          Paragraph("5. Telecommunicator CPR", S["h2"]),
          _clause(S, "5.1", QA_5_1),
          _clause(S, "5.2", "The program reports each month's median time to first compression over the arrests in "
                            "which the call-taker coached compressions, each arrest at its primary review. A second "
                            "review of the same call, for reviewer calibration, is not counted."),
          Paragraph("6. Records", S["h2"]),
          _clause(S, "6.1", "Calls, units and call-takers are as the CAD records them; answering is as the 911 call "
                            "handling equipment records it; acuity is as the patient care record records it; shifts "
                            "are as the scheduling system records the shifts worked.")]
    doc.build(st, onFirstPage=fr, onLaterPages=fr)


# ------------------------------------------------------------------------------------------------ release note
def write_release(path):
    S = styles(RED)
    title = "Protocol Software Release 13.3"
    doc, fr = _doc(path, title, "QCECD Systems", "Release note", K.CENTRE, "Release 13.3")
    rows = [["Protocol", "Change in 13.3"],
            ["10 Chest pain", "Key questions reordered; new question on pain spreading to the jaw or arm."],
            ["17 Falls", "Determinant suffixes revised for long falls and falls from height; key question on "
                         "anticoagulant medicines."],
            ["26 Sick person", "Key questions on alertness and breathing moved ahead of the chief complaint "
                               "questions."],
            ["28 Stroke", "Stroke diagnostic tool updated to the current scale; time last seen well recorded."],
            ["All protocols", "Breathing-status prompt shown at case entry for every caller."]]
    st = [Paragraph(title, S["h1"]),
          Paragraph("%s, systems team. Issued 20 February 2026." % K.CENTRE, S["meta"]),
          Paragraph("Go-live", S["h2"]),
          Paragraph("Release 13.3 of the protocol software goes live on every call-taking position at 06:00 on "
                    "Tuesday 3 March 2026, replacing release 13.1. Calls open at 06:00 finish on the release they "
                    "started on.", S["body"]),
          Paragraph("Changes for call-takers", S["h2"]),
          _table(S, rows, [1.6, 5.2]),
          Paragraph("Training", S["h2"]),
          Paragraph("Every call-taker completes the two-hour update course before go-live. The course is recorded "
                    "in the training system; supervisors confirm completion at the shift briefing.", S["body"]),
          Paragraph("Support", S["h2"]),
          Paragraph("The vendor's support line is staffed for the first 72 hours after go-live. Report problems to "
                    "the systems team through the usual ticket queue.", S["body"])]
    doc.build(st, onFirstPage=fr, onLaterPages=fr)


# ------------------------------------------------------------------------------------------------ reference workbook
def _style_sheet(sh, widths=None, fill="1F3A5F"):
    from openpyxl.styles import Alignment, Font, PatternFill
    for cell in sh[1]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor=fill)
        cell.alignment = Alignment(vertical="center", wrap_text=True)
    sh.freeze_panes = "A2"
    for col in sh.columns:
        letter_ = col[0].column_letter
        if widths and letter_ in widths:
            sh.column_dimensions[letter_].width = widths[letter_]
        else:
            width = max(len(str(c.value)) if c.value is not None else 0 for c in col[:200])
            sh.column_dimensions[letter_].width = min(60, max(8, width + 2))


def write_reference(path):
    import openpyxl
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Trunk groups"
    ws.append(["trunk_group", "description", "circuits"])
    for tg, desc, _ in K.TRUNKS:
        ws.append([tg, desc, {"TG01": 6, "TG02": 12, "TG03": 4, "TG05": 2, "TG07": 4}[tg]])
    _style_sheet(ws, {"B": 70})
    wu = wb.create_sheet("Units")
    wu.append(["unit", "type", "station"])
    for i, u in enumerate(K.UNITS):
        wu.append([u, "ALS" if i % 3 else "BLS", "Station %d" % (1 + i // 2)])
    _style_sheet(wu)
    wp = wb.create_sheet("Protocols")
    wp.append(["protocol", "chief_complaint"])
    for p in K.PROTOCOLS:
        wp.append([p[0], p[1]])
    _style_sheet(wp)
    wq = wb.create_sheet("Positions")
    wq.append(["position", "room"])
    for i in range(1, 21):
        wq.append(["P%02d" % i, "Call floor" if i <= 12 else ("Training room (overflow)" if i <= 14 else
                                                             "Dispatch floor")])
    _style_sheet(wq)
    wb.save(path)
