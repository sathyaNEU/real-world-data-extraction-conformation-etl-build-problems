"""The pack's documents and workbooks: the QPI technical report for the 2027 forms, the System's placement policy, the
data dictionary (PDFs), the Office's session review log and the colleges' fall 2026 course outcomes (workbooks)."""
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
INK = colors.HexColor("#1d2533")
GREY = colors.HexColor("#5a6372")
NAVY = colors.HexColor("#1f3d6b")
BODY = ParagraphStyle("body", fontName="LiberationSerif", fontSize=10.3, leading=13.8, textColor=INK, spaceAfter=6)
SMALL = ParagraphStyle("small", fontName="LiberationSerif", fontSize=8.6, leading=11.2, textColor=GREY, spaceAfter=4)
CELL = ParagraphStyle("cell", fontName="LiberationSans", fontSize=8.2, leading=10.4, textColor=INK)
CELLB = ParagraphStyle("cellb", fontName="LiberationSans-Bold", fontSize=8.2, leading=10.4, textColor=INK)
H2 = ParagraphStyle("h2", fontName="LiberationSans-Bold", fontSize=10.6, leading=14, textColor=INK, spaceBefore=8,
                    spaceAfter=4)
ORG = "%s, %s" % (W.SYSTEM, W.OFFICE)


def _frame(foot):
    def frame(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(GREY)
        canvas.setFont("LiberationSans", 7.2)
        canvas.drawString(0.85 * inch, 0.55 * inch, foot)
        canvas.drawRightString(letter[0] - 0.85 * inch, 0.55 * inch, "Page %d" % doc.page)
        canvas.restoreState()
    return frame


def _masthead(org, title):
    return [Paragraph(org.upper(), ParagraphStyle("o", fontName="LiberationSans-Bold", fontSize=8.2, textColor=NAVY,
                                                  leading=11)),
            Paragraph(title, ParagraphStyle("t", fontName="LiberationSans-Bold", fontSize=14, leading=18,
                                            textColor=INK, spaceAfter=6))]


def _table(rows, widths, head=True):
    t = Table([[Paragraph(str(c), CELLB if (head and i == 0) else CELL) for c in r] for i, r in enumerate(rows)],
              colWidths=[w * inch for w in widths], hAlign="LEFT", repeatRows=1 if head else 0)
    st = [("LINEBELOW", (0, 0), (-1, 0), 0.6, INK), ("VALIGN", (0, 0), (-1, -1), "TOP"),
          ("LEFTPADDING", (0, 0), (-1, -1), 2), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
          ("BOTTOMPADDING", (0, 0), (-1, -1), 2), ("TOPPADDING", (0, 0), (-1, -1), 2)]
    t.setStyle(TableStyle(st))
    return t


def _doc(path, org, title, author, head, story_items, foot):
    d = SimpleDocTemplate(path, pagesize=letter, leftMargin=0.85 * inch, rightMargin=0.85 * inch, topMargin=0.8 * inch,
                          bottomMargin=0.9 * inch, title=title, author=author, subject="", creator="", producer="")
    t = Table([[Paragraph(a, CELLB), Paragraph(b, CELL)] for a, b in head], colWidths=[1.0 * inch, 5.5 * inch],
              hAlign="LEFT")
    t.setStyle(TableStyle([("LINEBELOW", (0, -1), (-1, -1), 0.6, INK), ("LEFTPADDING", (0, 0), (-1, -1), 0),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]))
    story = _masthead(org, title) + [t, Spacer(1, 8)]
    for x in story_items:
        if isinstance(x, tuple):
            story.append(Paragraph(x[0], H2))
            for p in x[1]:
                story.append(Paragraph(p, BODY) if isinstance(p, str) else p)
        else:
            story.append(x)
    d.build(story, onFirstPage=_frame(foot), onLaterPages=_frame(foot))


def write_report(path, e):
    s26 = e["scores26"]
    hist = [["Form", "Testing year", "Platform", "College Algebra", "Corequisite College Algebra"],
            ["25A", "2025", W.OLD_PLATFORM, "29", "18"], ["25B", "2025", W.OLD_PLATFORM, "28", "18"],
            ["26A", "2026", "%s, then %s" % (W.OLD_PLATFORM, W.NEW_PLATFORM), str(s26["26A"]["CA"]),
             str(s26["26A"]["CCA"])],
            ["26B", "2026", "%s, then %s" % (W.OLD_PLATFORM, W.NEW_PLATFORM), str(s26["26B"]["CA"]),
             str(s26["26B"]["CCA"])]]
    std = [["Placement", "Course", "Standard (logits)", "Standard (bank units)"],
           ["College Algebra", "MATH 131", "%.2f" % W.STANDARDS["CA"], "%.0f" % (W.BU0 + W.BU1 * W.STANDARDS["CA"])],
           ["Corequisite College Algebra", "MATH 131 with MATH 031", "%.2f" % W.STANDARDS["CCA"],
            "%.0f" % (W.BU0 + W.BU1 * W.STANDARDS["CCA"])]]
    items = [
        ("1. The QPI", [
            "The Quantitative Placement Inventory (QPI) places students entering the System's fourteen colleges into "
            "one of three mathematics levels: College Algebra (MATH 131), Corequisite College Algebra (MATH 131 taken "
            "with the MATH 031 support course) and Developmental Mathematics (MATH 091). Each form has two placement "
            "scores, and System Policy 4.12 sets how a student's sittings place them. This report documents the QPI's "
            "design and scaling for the 2027 forms; the 2026 report is superseded."]),
        ("2. Forms", [
            "Each testing year runs from 1 March to the last day of February and has two forms: form A for a student's "
            "first sitting and form B for a retest. A form has 60 scored items: the anchor block of 20 items, the same "
            "on every form and kept in positions 1 to 20, and 40 unique items written for the form, eight in each of "
            "the five content strands. Each sitting also carries one of eight field-test sets of 10 items, which are "
            "not scored. The raw score is the number of the 60 scored items answered correctly; an item left "
            "unanswered scores 0."]),
        ("3. Delivery", [
            "Until 30 June 2026 the QPI was delivered on the %s in two versions of each form. Version A presents the "
            "40 unique items in positions 21 to 60 and the field-test set in positions 61 to 70, each in form order; "
            "version B presents the unique items and the field-test set in reverse order. Sittings alternated between "
            "the versions by seat." % W.OLD_PLATFORM,
            "From 1 July 2026 the QPI is delivered on %s. The anchor block stays in positions 1 to 20, and the 40 "
            "unique items and the sitting's field-test set are presented together in positions 21 to 70, in an order "
            "drawn afresh for each sitting." % W.NEW_PLATFORM]),
        ("4. Scaling", [
            "QPI items are scaled with the Rasch model. Abilities and difficulties are on the QPI bank scale, in "
            "logits, which the 2022 base calibration of the anchor block fixed. %s, the System's item bank since "
            "2025, records an item's difficulty and its standard error in bank units: 500 plus 100 times the logit."
            % W.BANK_SYSTEM]),
        ("5. Field testing and the ready pool", [
            "A field-test item is calibrated from the sittings that carried its set, with the anchor block's "
            "difficulties fixed at their bank values. It enters the ready pool when its calibration rests on 500 or "
            "more responses, its proportion correct lies between 0.15 and 0.90 and its point-biserial correlation "
            "with the raw score is 0.20 or more. Every item in the ready pool was field-tested on the %s, in the 2023, "
            "2024 or 2025 testing year." % W.OLD_PLATFORM,
            "The 2026 field-test sets were delivered on both platforms; their calibration is in review and none of "
            "their items is in the ready pool."]),
        ("6. Standards", [
            "The two standards were set in the 2022 standard setting, on the bank scale. A student whose ability is at "
            "or above a standard is ready for that placement's course.", _table(std, (1.8, 1.7, 1.3, 1.5)),
            Spacer(1, 6)]),
        ("7. Placement scores", [
            "A form's placement scores are set before the form goes live. Each is the lowest whole raw score at or "
            "above the raw score that a student whose ability is exactly at the standard is expected to obtain on "
            "the form's 60 scored items. A raw score at or above the College Algebra score places a student into "
            "College Algebra; a raw score below it and at or above the Corequisite College Algebra score places them "
            "into Corequisite College Algebra; a lower raw score places them into Developmental Mathematics.",
            "Placement scores of recent forms, as approved:", _table(hist, (0.6, 1.0, 2.6, 1.1, 1.7)), Spacer(1, 6)]),
        ("8. The 2027 forms", [
            "Form 27A goes live on %s on 1 March 2027, and its placement scores go to the %s at its meeting on 18 "
            "February 2027. It carries the System's anchor block and 40 unique items assembled from the ready pool, "
            "eight in each strand; none of them has been on a form before. Form 27A's own field-test sets are new "
            "items and are not scored. Form 27B, the 2027 retest form, goes live on 1 April 2027 and its placement "
            "scores go to the Board in March." % (W.NEW_PLATFORM, W.BOARD)]),
        ("9. Retirement", [
            "A form's unique items are retired at the end of its testing year and do not return to the ready pool. "
            "Items are reviewed for content each year; a substantive edit sends an item back to field testing."]),
    ]
    _doc(path, ORG, "QPI technical report: the 2027 forms", W.PEOPLE["psychometrician"],
         [["Report", "QPI-TR-2027"], ["Issued", "5 February 2027"],
          ["Prepared by", "%s, Psychometrician" % W.PEOPLE["psychometrician"]],
          ["For", "%s, meeting of 18 February 2027" % W.BOARD]],
         items, "%s. QPI technical report QPI-TR-2027, 5 February 2027." % W.SYSTEM)


def write_policy(path):
    items = [
        ("1. Purpose", [
            "This policy sets how the System's colleges place entering students in mathematics with the Quantitative "
            "Placement Inventory (QPI). Placement by high school record is set by Policy 4.13; a placement made under "
            "4.13 is not a QPI placement."]),
        ("2. Registering and sitting", [
            "A student registers for the QPI through one of the System's colleges. From 1 July 2026 a student may sit "
            "the QPI at any college's testing centre.",
            "A student may sit the QPI twice in a testing year (1 March to the last day of February): a first sitting "
            "on the year's form A and one retest on form B, no sooner than 14 days after the first sitting."]),
        ("3. Placement", [
            "The score of each sitting goes to the college the student is registered through when they sit, and that "
            "college places the student. A student's placement for the testing year is the higher of the levels "
            "their sittings give; where both sittings give the same level, the later sitting places the student.",
            "A placement stands for twelve months at every college of the System. A student who moves their "
            "registration to another college keeps their placement and is not placed again."]),
        ("4. Invalidated sessions", [
            "The Office of Assessment and Placement may invalidate the attempts in a testing session where it finds "
            "an irregularity. An invalidated attempt is not a sitting: it does not place the student and does not "
            "count toward the two sittings. Where the Office withdraws an invalidation, the session's attempts stand "
            "as sittings."]),
        ("5. Records", [
            "The Office keeps each platform's attempt records, the score reports and the session review log, and "
            "reports each college's placements to the %s each year." % W.BOARD]),
    ]
    _doc(path, W.SYSTEM, "Policy 4.12: Mathematics placement", W.PEOPLE["director"],
         [["Policy", "4.12, Mathematics placement"], ["Revised", "1 July 2026 (replaces the revision of 1 March 2024)"],
          ["Owner", "%s, Director of Placement and Developmental Mathematics" % W.PEOPLE["director"]]],
         items, "%s. Policy 4.12, revised 1 July 2026." % W.SYSTEM)


DICT = {
    "pool": [("item_id", "Itemstore item identifier"), ("kts_item", "the item's identifier on the Kestrel Testing "
             "Suite, where it had one"), ("strand", "content strand: NS, AE, LE, FG or QR"),
             ("status", "anchor; ready; or the 2027 form the item is assembled on"),
             ("difficulty_bu", "Rasch difficulty in bank units (500 + 100 x logit)"),
             ("se_bu", "standard error of the difficulty, bank units"), ("n_calibration", "responses calibrated"),
             ("calibration", "the calibration the difficulty comes from"), ("calibrated_on", "date of the calibration"),
             ("key", "correct option")],
    "map27": [("form", "27A"), ("section", "anchor, unique or field test"), ("slot", "item's slot in its section; "
              "field-test slots are set.slot"), ("item_id", "Itemstore item identifier"),
              ("kts_item", "Kestrel Testing Suite identifier, where the item had one"), ("strand", "content strand"),
              ("key", "correct option"), ("position", "delivered position on Northgate Assess")],
    "layout26": [("form", "26A, 26B, or FT26-n for field-test set n"), ("section", "anchor, unique or field test"),
                 ("slot", "item's slot in its section"), ("item_id", "Itemstore item identifier"),
                 ("kts_item", "Kestrel Testing Suite identifier"), ("strand", "content strand"),
                 ("key", "correct option"),
                 ("kts_position_version_A", "position on the Kestrel Testing Suite, version A"),
                 ("kts_position_version_B", "position on the Kestrel Testing Suite, version B")],
    "kts": [("attempt_id", "attempt identifier"), ("college", "college code"), ("site", "testing site"),
            ("student_no", "the college's student number"), ("birth_date", "MM/DD/YYYY"), ("sex", "F or M"),
            ("hs_code", "high school code; GED where the student has a high school equivalency"),
            ("registered", "date the student registered for the QPI, MM/DD/YYYY"), ("form", "form sat"),
            ("version", "A or B"), ("ft_set", "field-test set"), ("test_date", "MM/DD/YYYY, local time"),
            ("start", "start time, local"), ("end", "end time, local"),
            ("responses", "the option chosen at each delivered position, 1 to 70; * where no option was chosen"),
            ("raw_score", "number of scored items answered correctly"),
            ("placement", "131 College Algebra; 131C Corequisite College Algebra; 091 Developmental Mathematics")],
    "ng_att": [("attempt_ref", "attempt reference"), ("student_id", "the student's identifier (nine digits)"),
               ("birth_date", "YYYY-MM-DD"), ("sex", "F or M"), ("hs_code", "high school code; GED where the student "
               "has a high school equivalency"), ("registered", "date the student registered for the QPI"),
               ("college", "college code"), ("centre", "testing centre"),
               ("session_ref", "testing session"), ("form", "form sat"), ("ft_set", "field-test set"),
               ("started_at", "UTC"), ("submitted_at", "UTC"), ("raw_score", "number of scored items answered "
               "correctly"), ("placement", "CA, CCA or DM")],
    "ng_resp": [("attempt_ref", "attempt reference"), ("item_id", "Itemstore item identifier"),
                ("seq", "delivered position, 1 to 70"), ("response", "option chosen; blank where none"),
                ("score", "1 correct, 0 otherwise (field-test items are scored here but not counted in raw_score)"),
                ("rt_s", "seconds on the item"), ("served_at", "UTC")],
    "reports": [("report_id", "score report"), ("attempt", "attempt_id (Kestrel Testing Suite) or attempt_ref "
                "(Northgate Assess)"), ("sent_to", "college code"), ("report", "automatic, or on request"),
                ("sent", "local time")],
    "xwalk": [("kts_college", "college code"), ("kts_student_no", "the college's student number"),
              ("northgate_student_id", "the student's identifier on Northgate Assess at migration"),
              ("migrated", "date of the migration")],
    "centres": [("centre", "testing centre code (Northgate Assess)"), ("college", "college code"),
                ("centre_name", "name"), ("kts_site", "the site's code on the Kestrel Testing Suite")],
}


def write_dictionary(path, n):
    items = []
    names = {"pool": "Itemstore assembly pool export", "map27": "Form 27A assembly", "layout26": "Forms 26A and 26B "
             "layout", "kts": "Kestrel Testing Suite attempts", "ng_att": "Northgate Assess attempts",
             "ng_resp": "Northgate Assess item responses", "reports": "Score reports", "xwalk": "Student crosswalk",
             "centres": "Testing centres"}
    for k in ("pool", "map27", "layout26", "kts", "ng_att", "ng_resp", "reports", "xwalk", "centres"):
        rows = [["Field", "Description"]] + [[a, b] for a, b in DICT[k]]
        items.append(("%s (%s, %s rows)" % (names[k], P.FILES[k], "{:,}".format(n[k])), [_table(rows, (1.6, 4.9)),
                                                                                         Spacer(1, 4)]))
    _doc(path, ORG, "QPI data dictionary, 2027", W.PEOPLE["psychometrician"],
         [["Version", "2027.1"], ["Date", "4 February 2027"], ["Covers", "the files sent with QPI-TR-2027"]],
         items, "%s. QPI data dictionary 2027.1." % W.SYSTEM)


def _sheet(ws, title, note, header, rows, widths):
    from openpyxl.styles import Font, PatternFill
    ws["A1"] = title
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = note
    ws.append([])
    ws.append(header)
    for c in ws[4]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor="1F3D6B")
    for r in rows:
        ws.append(r)
    for i, w in enumerate(widths):
        ws.column_dimensions["ABCDEFGHIJ"[i]].width = w
    ws.freeze_panes = "A5"


REASONS_INV = ["proctor left the room during the session", "workstations lost connection and restarted mid-session",
               "a candidate's phone found in use; the room's attempts reviewed", "seating chart not kept",
               "session started before identity checks were complete", "the room's clocks and timer disagreed",
               "fire alarm; attempts resumed after 25 minutes", "reference sheet left on the wall"]


def write_review(path, e):
    import openpyxl
    rng = np.random.default_rng(W.SEED + 23)
    rows = []
    for j, ir in enumerate(e["irregular"]):
        c, d, hm = ir["session"]
        sess = e["sessions"][ir["session"]]
        plat = W.OLD_PLATFORM if sess[0]["platform"] == "old" else W.NEW_PLATFORM
        ref = None if sess[0]["platform"] == "old" else P.session_ref(sess[0])
        logged = d + dt.timedelta(days=int(rng.integers(2, 9)))
        rows.append([logged, c, d, hm, plat, ref, "Attempts invalidated", len(sess), REASONS_INV[j % len(REASONS_INV)]])
        if ir["reinstated"]:
            rows.append([logged + dt.timedelta(days=int(rng.integers(12, 30))), c, d, hm, plat, ref,
                         "Invalidation withdrawn", len(sess), "review found no effect on the attempts"])
    rows.sort(key=lambda r: (r[0], r[1]))
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Session review 2026"
    _sheet(ws, "QPI session review log, 2026 testing year", "Office of Assessment and Placement. Sessions reviewed "
           "after an irregularity report; a decision applies to every attempt in the session.",
           ["Logged", "Centre", "Session date", "Session start", "Platform", "Session ref", "Decision", "Attempts",
            "Note"], rows, (12, 9, 13, 13, 22, 22, 22, 9, 52))
    for r in ws.iter_rows(min_row=5):
        for c in (r[0], r[2]):
            c.number_format = "yyyy-mm-dd"
    wb.save(path)


def write_outcomes(path, e):
    import openpyxl
    rng = np.random.default_rng(W.SEED + 29)
    rows = []
    for code, name, n, mu, _ in W.COLLEGES:
        for course, share, rate in (("MATH 091", 0.30, 0.61), ("MATH 131", 0.30, 0.64), ("MATH 131 / MATH 031", 0.27,
                                                                                            0.57)):
            enr = int(n * share * rng.uniform(0.55, 0.72))
            comp = int(enr * rng.uniform(0.84, 0.92))
            rows.append([code, name, course, enr, comp, int(comp * rate * rng.uniform(0.92, 1.08))])
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Fall 2026"
    _sheet(ws, "Mathematics course outcomes, fall 2026", "Colleges' end-of-term returns. Enrolled at each college's "
           "census date; completed with a grade other than W; success at C or better.",
           ["College", "College name", "Course", "Enrolled", "Completed", "C or better"], rows, (9, 34, 20, 10, 11, 12))
    wb.save(path)
