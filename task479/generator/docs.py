"""The pack's documents: Quantilis's technical summary of the 2025-26 benchmark, the network's 2026-27 tutoring
designation memo, the data dictionary and the extract manifest."""
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

import pack as P      # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("LiberationSerif", "Regular"), ("LiberationSerif-Bold", "Bold"), ("LiberationSans", "Regular"),
              ("LiberationSans-Bold", "Bold")):
    try:
        pdfmetrics.getFont(nm)
    except KeyError:
        pdfmetrics.registerFont(TTFont(nm, FONT_DIR + nm.split("-")[0] + "-" + f + ".ttf"))
INK = colors.HexColor("#1b2430")
GREY = colors.HexColor("#5b6470")
TEAL = colors.HexColor("#1f5a63")
BODY = ParagraphStyle("body", fontName="LiberationSerif", fontSize=10.3, leading=13.8, textColor=INK, spaceAfter=6)
CELL = ParagraphStyle("cell", fontName="LiberationSans", fontSize=8.6, leading=10.8, textColor=INK)
CELLB = ParagraphStyle("cellb", fontName="LiberationSans-Bold", fontSize=8.6, leading=10.8, textColor=INK)
H2 = ParagraphStyle("h2", fontName="LiberationSans-Bold", fontSize=10.6, leading=14, textColor=INK, spaceBefore=8,
                    spaceAfter=4)

MANUAL = [
    ("1. The benchmark", [
        "The Quantilis Mathematics Benchmark is a fixed-form, forty-item test given three times a year (fall, winter "
        "and spring) at grades 6, 7 and 8. Each item is four-option multiple choice. The test is untimed and is given "
        "on the school's devices in Quantilis's browser client, which records each response and the seconds the "
        "student spent on the item."]),
    ("2. The item bank and the scale", [
        "Every item is calibrated to the three-parameter logistic model, P = c + (1 - c) / (1 + exp(-1.7 a (theta - b))), "
        "on a single vertical scale across the grades; the bank file gives each item's discrimination a, difficulty b "
        "and lower asymptote c. A scale score is 500 + 40 theta, rounded to the whole point and bounded at 350 and "
        "650."]),
    ("3. Scoring", [
        "A student's theta is estimated by maximum likelihood from the student's scored responses on the bank's "
        "parameters, by Newton iteration from theta = 0, and bounded to the reporting range. The score report gives "
        "each student's scale score and performance level for the administration."]),
    ("4. Performance levels", [
        "Below Basic: under 470. Basic: 470 to 519. Proficient: 520 to 569. Advanced: 570 and over. The cuts were set "
        "in the 2023 standard setting and apply to every grade on the vertical scale."]),
    ("5. Exports", [
        "Item response exports give one row per student and item. From the platform release of 30 March 2026 the "
        "export's fields were renamed and response time is given in seconds rather than milliseconds; sessions before "
        "the release were exported in the earlier layout. A session that is restarted is scored as a new administration, "
        "and the later administration is the student's score for the window. Students tested under a temporary id "
        "when the roster had no record for them are listed in the temporary id register."]),
]


def write_manual(path):
    def frame(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(GREY)
        canvas.setFont("LiberationSans", 7.2)
        canvas.drawString(0.85 * inch, 0.55 * inch, "%s. Mathematics Benchmark technical summary, 2025-26 school year."
                          % P.VENDOR)
        canvas.drawRightString(letter[0] - 0.85 * inch, 0.55 * inch, "Page %d" % doc.page)
        canvas.restoreState()
    d = SimpleDocTemplate(path, pagesize=letter, leftMargin=0.85 * inch, rightMargin=0.85 * inch, topMargin=0.8 * inch,
                          bottomMargin=0.9 * inch, title="Mathematics Benchmark technical summary 2025-26",
                          author=P.VENDOR, subject="", creator="", producer="")
    story = [Paragraph(P.VENDOR.upper(), ParagraphStyle("o", fontName="LiberationSans-Bold", fontSize=8.4,
                                                        textColor=TEAL, leading=11)),
             Paragraph("Mathematics Benchmark: technical summary, 2025-26",
                       ParagraphStyle("t", fontName="LiberationSans-Bold", fontSize=14, leading=18, textColor=INK,
                                      spaceAfter=8))]
    for h, paras in MANUAL:
        story.append(Paragraph(h, H2))
        for p in paras:
            story.append(Paragraph(p, BODY))
    d.build(story, onFirstPage=frame, onLaterPages=frame)


MEMO = [
    ("Purpose", "The network's 2026-27 high-dosage tutoring grant funds three tutors per designated campus for grade 6 "
                "to 8 mathematics. The Board designates the campuses at its meeting of 22 October 2026."),
    ("Designation", "A campus is designated when 35 per cent or more of its students tested on the spring 2026 "
                    "benchmark are below Basic in mathematics, each student's achievement estimated from the student's "
                    "spring 2026 responses on Quantilis's scale and item bank. A student tested is a student with a "
                    "spring 2026 benchmark administration."),
    ("With the designation", "The Director of Assessment brings the Board, for each campus, the students tested on the "
                             "fall 2025 benchmark and the share at or above Proficient, and the students tested in both "
                             "the fall and the winter benchmark with their mean scale-score growth from fall to winter."),
]


def write_memo(path):
    import docx
    from docx.shared import Pt
    doc = docx.Document()
    doc.styles["Normal"].font.name = "Calibri"
    doc.styles["Normal"].font.size = Pt(10.5)
    p = doc.add_paragraph()
    r = p.add_run(P.NETWORK.upper())
    r.bold = True
    r.font.size = Pt(8.5)
    p = doc.add_paragraph()
    r = p.add_run("2026-27 high-dosage tutoring: designation of campuses")
    r.bold = True
    r.font.size = Pt(15)
    doc.add_paragraph("To the Board of Directors, from Sabrina Santos, Director of Assessment, 18 September 2026.")
    for h, t in MEMO:
        q = doc.add_paragraph()
        q.add_run(h).bold = True
        doc.add_paragraph(t)
    doc.add_paragraph("Gregory Valdez, Chief Academic Officer, concurs.")
    cp = doc.core_properties
    cp.author = cp.last_modified_by = "Sabrina Santos"
    cp.title = "2026-27 high-dosage tutoring: designation of campuses"
    cp.comments = cp.keywords = cp.subject = ""
    cp.revision = 2
    doc.save(path)


DICT_COLS = ["file_name", "field", "description"]


def dictionary_rows():
    f = P.FILES
    return [
        (f["resp1"], "StudentID", "the student's id in the network's student information system"),
        (f["resp1"], "ItemSeq", "the item's position on the form, 1 to 40"),
        (f["resp1"], "Response", "the option the student selected"),
        (f["resp1"], "Scored", "1 correct, 0 incorrect"),
        (f["resp1"], "ResponseTimeMs", "time on the item, milliseconds"),
        (f["resp2"], "student_id", "the student's id in the network's student information system"),
        (f["resp2"], "item_seq", "the item's position on the form, 1 to 40"),
        (f["resp2"], "selected_option", "the option the student selected"),
        (f["resp2"], "score", "1 correct, 0 incorrect"),
        (f["resp2"], "response_time_s", "time on the item, seconds"),
        (f["spring"], "scale_score", "the student's scale score for the administration"),
        (f["spring"], "items_answered", "items with a response"),
        (f["bank"], "a", "discrimination"),
        (f["bank"], "b", "difficulty, theta metric"),
        (f["bank"], "c", "lower asymptote"),
        (f["fall"], "student_id", "the student's id, or a temporary id issued by Quantilis"),
        (f["winter"], "student_id", "the student's id in the network's student information system"),
        (f["temp"], "temporary_student_id", "a temporary id Quantilis issued for a student tested without a roster record"),
        (f["xwalk"], "legacy_student_id", "the student's id before the January 2026 migration"),
        (f["xwalk"], "student_id", "the student's id after the migration"),
        (f["roster_f"], "student_id", "the student's id before the January 2026 migration"),
        (f["roster_s"], "student_id", "the student's id after the January 2026 migration"),
        (f["state"], "pct_meets_or_exceeds", "the state test's share at Meets or Exceeds, 2025, per cent"),
        (f["attend"], "chronic_absence_pct", "students missing 10 per cent or more of days enrolled, per cent"),
    ]


MANIFEST_COLS = ["file_name", "contents", "provided_by", "as_of_date", "record_count"]


def manifest_rows(n):
    f = P.FILES
    return [
        (f["resp1"], "spring 2026 item responses, sessions to 27 March", P.VENDOR, "2026-03-28", n["resp1"]),
        (f["resp2"], "spring 2026 item responses, sessions from 30 March", P.VENDOR, "2026-04-14", n["resp2"]),
        (f["spring"], "spring 2026 score report", P.VENDOR, "2026-04-14", n["spring"]),
        (f["bank"], "item bank parameters", P.VENDOR, "2025-08-01", n["bank"]),
        (f["manual"], "technical summary", P.VENDOR, "2025-08-01", ""),
        (f["memo"], "tutoring designation memo", P.NETWORK, "2026-09-18", ""),
        (f["fall"], "fall 2025 score report", P.VENDOR, "2025-10-17", n["fall"]),
        (f["temp"], "temporary id register, fall 2025", P.VENDOR, "2025-10-17", n["temp"]),
        (f["winter"], "winter 2026 score report", P.VENDOR, "2026-02-06", n["winter"]),
        (f["roster_f"], "student roster", P.NETWORK, "2025-10-01", n["roster_f"]),
        (f["roster_s"], "student roster", P.NETWORK, "2026-03-01", n["roster_s"]),
        (f["xwalk"], "student id crosswalk", P.NETWORK, "2026-01-05", n["xwalk"]),
        (f["state"], "state accountability results, mathematics 2025", "State Department of Education", "2025-09-15",
         n["state"]),
        (f["attend"], "chronic absence by campus", P.NETWORK, "2026-05-01", n["attend"]),
        (f["dictionary"], "field descriptions", P.NETWORK, "2026-10-02", n["dictionary"]),
    ]
