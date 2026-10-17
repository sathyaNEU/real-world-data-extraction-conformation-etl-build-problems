"""The pack's documents: the program's screening and referral protocol, the data manager's notes on the 2026
season's extracts, the analyser maker's error code reference, and the export manifest."""
from __future__ import annotations

import csv

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                    # noqa: E402
from reportlab.lib.pagesizes import letter                                          # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                     # noqa: E402
from reportlab.lib.units import mm                                                  # noqa: E402
from reportlab.pdfbase import pdfmetrics                                            # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                        # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle   # noqa: E402

import askworld as AW   # noqa: E402
import common as K      # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("Sans", "LiberationSans-Regular"), ("Sans-B", "LiberationSans-Bold"), ("Sans-I", "LiberationSans-Italic"),
              ("Serif", "LiberationSerif-Regular"), ("Serif-B", "LiberationSerif-Bold"),
              ("Serif-I", "LiberationSerif-Italic")):
    pdfmetrics.registerFont(TTFont(nm, FONT_DIR + f + ".ttf"))
pdfmetrics.registerFontFamily("Sans", normal="Sans", bold="Sans-B", italic="Sans-I", boldItalic="Sans-B")
pdfmetrics.registerFontFamily("Serif", normal="Serif", bold="Serif-B", italic="Serif-I", boldItalic="Serif-B")
INK, GREY, RULE = colors.HexColor("#1d2326"), colors.HexColor("#5b646b"), colors.HexColor("#b7bec4")


def styles(font, accent):
    body = ParagraphStyle("b", fontName=font, fontSize=9.8, leading=13.6, textColor=INK, spaceAfter=5)
    return dict(
        body=body,
        h1=ParagraphStyle("h1", fontName=font + "-B", fontSize=14, leading=18, textColor=accent, spaceAfter=2),
        h2=ParagraphStyle("h2", fontName=font + "-B", fontSize=10.6, leading=14, textColor=INK, spaceBefore=7,
                          spaceAfter=2, keepWithNext=1),
        meta=ParagraphStyle("m", fontName=font, fontSize=8.4, leading=11.4, textColor=GREY, spaceAfter=9),
        cell=ParagraphStyle("c", fontName=font, fontSize=8.2, leading=10.4, textColor=INK),
        cellb=ParagraphStyle("cb", fontName=font + "-B", fontSize=8.2, leading=10.4, textColor=INK),
        clause=ParagraphStyle("p", parent=body, leftIndent=24, firstLineIndent=-24))


def _frame(left, right, font):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(GREY)
        canvas.setFont(font, 7.4)
        canvas.drawString(19 * mm, letter[1] - 11.5 * mm, left)
        canvas.drawRightString(letter[0] - 19 * mm, letter[1] - 11.5 * mm, right)
        canvas.drawRightString(letter[0] - 19 * mm, 10 * mm, "Page %d" % doc.page)
        canvas.restoreState()
    return draw


def _table(S, rows, widths, right=()):
    data = [[Paragraph(str(c), S["cellb"] if i == 0 else S["cell"]) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=[w * mm for w in widths], repeatRows=1)
    st = [("LINEBELOW", (0, 0), (-1, 0), .6, INK), ("LINEBELOW", (0, -1), (-1, -1), .4, RULE),
          ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]
    for c in right:
        st.append(("ALIGN", (c, 0), (c, -1), "RIGHT"))
    t.setStyle(TableStyle(st))
    return t


def _doc(path, title, author):
    return SimpleDocTemplate(path, pagesize=letter, leftMargin=19 * mm, rightMargin=19 * mm, topMargin=20 * mm,
                             bottomMargin=17 * mm, title=title, author=author, subject="", creator="", producer="")


# ---------------------------------------------------------------------------------------------- the protocol
def write_protocol(path):
    S = styles("Serif", colors.HexColor("#2F5D50"))
    doc = _doc(path, "Screening and referral protocol, 2026-27", K.ORG)
    st = [Paragraph("%s %s: Screening and Referral Protocol, 2026-27" % (K.ORG, K.PROGRAM), S["h1"]),
          Paragraph("Owner: %s, MD, Medical Director, %s. Approved 9 February 2026. Replaces the 2024-25 "
                    "protocol." % (K.PEOPLE["medical"], K.PROGRAM), S["meta"])]
    P = lambda t: st.append(Paragraph(t, S["body"]))
    C = lambda n, t: st.append(Paragraph("%s&nbsp;&nbsp;%s" % (n, t), S["clause"]))
    H = lambda t: st.append(Paragraph(t, S["h2"]))
    H("1. Purpose")
    P("The program screens adults at community events across the %s service region for undiagnosed type 2 diabetes "
      "and refers the adults at risk for a confirmatory test at a %s patient service center." % (K.REGION, K.LAB))
    H("2. Who is screened")
    C("2.1", "Adults aged 18 and over who report that they have not been told they have diabetes.")
    C("2.2", "Each adult counts once in a season, at the first screening of the season. An adult already screened in "
             "the season is screened again on request but is not referred or drawn again.")
    H("3. The screening")
    C("3.1", "The tablet records the diabetes risk questionnaire (a score from 0 to 10), a fingerstick random glucose "
             "in mg/dL and a point-of-care HbA1c in per cent from the program's GQ-200 analyzers.")
    H("4. Referral in the 2026 season")
    C("4.1", "The tablet refers for the confirmatory test every adult with a risk score of 6 or more or a random "
             "glucose of 140 mg/dL or more.")
    C("4.2", "To learn how the screening measurements perform, the tablet also offers the same test to one in five of "
             "the adults it does not refer, drawn at random (the evaluation draw).")
    C("4.3", "Every adult referred or drawn leaves with a referral letter and an appointment within five weeks; the "
             "program sends one reminder.")
    H("5. The confirmatory test")
    C("5.1", "A 75 g oral glucose tolerance test (OGTT): a fasting glucose and a glucose two hours after the drink. "
             "Undiagnosed diabetes is a fasting glucose of 126 mg/dL or more or a two-hour glucose of 200 mg/dL or "
             "more. A test counts when both samples were taken.")
    H("6. Choosing the referral rule for 2027")
    C("6.1", "The tablets for the 2027 season will carry one of the candidate rules listed in the candidate rules "
             "file.")
    C("6.2", "A candidate qualifies if it would have referred at least 85 of every 100 adults with undiagnosed "
             "diabetes among everyone screened in the 2026 season, counting every adult screened, whether or not "
             "they had the test, on the measurements taken at their first screening.")
    C("6.3", "The program uses the qualifying candidate that would have referred the fewest of the adults screened in "
             "2026. If no candidate qualifies, the 2026 rule stays.")
    H("7. Responsibilities")
    P("The data manager prepares the season's extracts. The medical director approves the referral rule, and the "
      "program director loads it into the tablets before the 2027 season opens on 1 March 2027.")
    doc.build(st, onFirstPage=_frame(K.PROGRAM, "Protocol 2026-27", "Serif"),
              onLaterPages=_frame(K.PROGRAM, "Protocol 2026-27", "Serif"))


# ---------------------------------------------------------------------------------------------- the notes
def write_notes(path):
    S = styles("Sans", colors.HexColor("#2F5D50"))
    doc = _doc(path, "Notes on the 2026 season extracts", K.PEOPLE["data"])
    F = K.FILES
    st = [Paragraph("Notes on the 2026 season extracts", S["h1"]),
          Paragraph("%s, data manager, %s. 15 January 2027." % (K.PEOPLE["data"], K.PROGRAM), S["meta"])]
    P = lambda t: st.append(Paragraph(t, S["body"]))
    H = lambda t: st.append(Paragraph(t, S["h2"]))
    H("1. Screening encounters (%s)" % F["encounters"])
    P("One row per screening as the tablets synced it, 2 March to 20 November 2026. encounter_id is the screening's "
      "own number. A tablet that lost its connection at an event sends the event's rows again when it reconnects, so a "
      "few rows arrive twice with the same encounter_id. program_id is given to the adult at the first screening and "
      "found by the tablet when the adult comes back. screened_at is local time. risk_score is the questionnaire's "
      "score, glucose_mg_dl the fingerstick random glucose and hba1c_pct the GQ-200 result the tablet received. "
      "ogtt_referral is RULE for an adult referred by the 2026 rule, "
      "EVAL for an adult offered the test in the evaluation draw, and NONE otherwise.")
    H("2. OGTT results (%s)" % F["ogtt"])
    P("%s's extract of every OGTT on a program referral collected by 15 January 2027, pipe-delimited, one row per "
      "test. PROGRAM_ID is the number the patient service center typed from the referral letter; the hyphen or a "
      "leading zero is sometimes dropped and some are typed in lower case, so match on the seven digits after SF. "
      "COLLECTED is month/day/year. STATUS is INCOMPLETE when the two-hour sample was not taken. An appointment that "
      "was not kept leaves no row." % K.LAB)
    H("3. Candidate rules, close-out and event calendar")
    P("%s lists the six rules the 2027 tablets could carry, in the tablet's own logic. %s is the season's close-out "
      "report. %s lists every event with its venue, service area and hours; analyzers gives the asset tags of the "
      "GQ-200 units used at the event." % (F["rules"], F["closeout"], F["events"]))
    H("4. Files from other departments")
    P("Biomedical Engineering supplied %s, %s and the maker's %s. The billing office of %s supplied %s, the "
      "program account's invoices and credit memos. %s holds the answers to the post-event card. %s is the regional public health "
      "office's 2024 community health assessment by service area." % (F["runlog"], F["assets"], F["errors"], K.LAB,
                                                                      F["invoices"], F["feedback"], F["profile"]))
    doc.build(st, onFirstPage=_frame(K.PROGRAM, "Extract notes, January 2027", "Sans"),
              onLaterPages=_frame(K.PROGRAM, "Extract notes, January 2027", "Sans"))


# ---------------------------------------------------------------------------------------------- the error codes
def write_errors(path):
    S = styles("Sans", colors.HexColor("#3A4A6B"))
    doc = _doc(path, "GQ-200 error codes", "Glyquant")
    st = [Paragraph("GQ-200 point-of-care HbA1c analyzer: error code quick reference", S["h1"]),
          Paragraph("Glyquant technical services. Document GQ-QR-07, revision C, 2025.", S["meta"]),
          Paragraph("Every run, on a patient sample or a control, takes one cartridge, except a run stopped at the "
                    "cartridge check. A code raised at the cartridge check appears before the cartridge is accepted: no "
                    "sample has entered it, and it can be inserted again. A code raised during the measurement appears "
                    "after the sample has been drawn into the cartridge: discard the cartridge and repeat with a new "
                    "one.", S["body"]), Spacer(1, 4)]
    rows = [["Code", "Message", "Raised", "What to do"]]
    todo = {"E-02": "Wipe the cartridge's barcode and insert it again", "E-04": "Use a cartridge from an in-date lot",
            "E-06": "Let the cartridge reach room temperature, then insert it again",
            "E-09": "Close the lid and start again", "E-11": "Collect a fresh sample into a new cartridge",
            "E-13": "Run a control; if it passes, repeat with a new cartridge",
            "E-15": "Repeat with a new cartridge; refer to the laboratory if it recurs",
            "E-17": "Repeat with a new cartridge"}
    for code, msg, when in AW.ERRORS:
        rows.append([code, msg, "At the cartridge check" if when == "check" else "During the measurement", todo[code]])
    st.append(_table(S, rows, [16, 58, 40, 64]))
    doc.build(st, onFirstPage=_frame("Glyquant GQ-200", "GQ-QR-07 rev C", "Sans"),
              onLaterPages=_frame("Glyquant GQ-200", "GQ-QR-07 rev C", "Sans"))


def write_manifest(path, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\r\n")
        w.writerow(["file_name", "description", "supplied_by", "extract_date", "extent"])
        for r in rows:
            w.writerow(r)
