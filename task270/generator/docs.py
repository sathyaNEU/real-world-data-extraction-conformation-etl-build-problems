"""task270 documents: the collaborative's mood monitoring standard, the trust's DBT programme operating standard, the
learning team's 2024-25 annual report, the collaborative's 2025 pilot evaluation (a file the solution does not read)
and the committee paper. No file describes the data: every export names its own columns. The text is kept here as
data so checks.py and verify.py can quote it."""
from __future__ import annotations

import datetime as dt
import os
import re

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                      # noqa: E402
from reportlab.lib.pagesizes import A4                                                # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                       # noqa: E402
from reportlab.lib.units import cm                                                    # noqa: E402
from reportlab.pdfbase import pdfmetrics                                              # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                          # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import common as K          # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/"
for _n, _f in (("LibSans", "liberation/LiberationSans-Regular.ttf"), ("LibSans-Bold", "liberation/LiberationSans-Bold.ttf"),
               ("Carlito", "crosextra/Carlito-Regular.ttf"), ("Carlito-Bold", "crosextra/Carlito-Bold.ttf")):
    pdfmetrics.registerFont(TTFont(_n, FONT_DIR + _f))
INK = colors.HexColor("#1d2229")
GREY = colors.HexColor("#5d6570")
TEAL = colors.HexColor("#00646e")
NHS = colors.HexColor("#005eb8")
RULE = colors.HexColor("#a5adb6")
HEAD = colors.HexColor("#e8edf2")


def styles(font, bold, accent, size=10.2):
    return dict(
        body=ParagraphStyle("b" + font, fontName=font, fontSize=size, leading=size * 1.36, textColor=INK, spaceAfter=6),
        h1=ParagraphStyle("h1" + font, fontName=bold, fontSize=15, leading=19, textColor=accent, spaceAfter=3),
        sub=ParagraphStyle("s" + font, fontName=font, fontSize=8.9, leading=11.8, textColor=GREY, spaceAfter=10),
        h2=ParagraphStyle("h2" + font, fontName=bold, fontSize=10.8, leading=14, textColor=accent, spaceBefore=8,
                          spaceAfter=3),
        cell=ParagraphStyle("c" + font, fontName=font, fontSize=8.6, leading=10.8, textColor=INK),
        cellb=ParagraphStyle("cb" + font, fontName=bold, fontSize=8.6, leading=10.8, textColor=INK))


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _doc(path, title, author):
    return SimpleDocTemplate(path, pagesize=A4, leftMargin=2.3 * cm, rightMargin=2.3 * cm, topMargin=2.0 * cm,
                             bottomMargin=2.0 * cm, title=title, author=author, subject="", creator="", producer="")


def _footer(left, font):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFont(font, 7.6)
        canvas.setFillColor(GREY)
        canvas.drawString(2.1 * cm, 1.2 * cm, left)
        canvas.drawRightString(A4[0] - 2.1 * cm, 1.2 * cm, "Page %d" % doc.page)
        canvas.restoreState()
    return draw


def grid(rows, widths, st, align_right=()):
    data = []
    for k, row in enumerate(rows):
        data.append([Paragraph(esc(str(c)), st["cellb"] if k == 0 else st["cell"]) for c in row])
    t = Table(data, colWidths=[w * cm for w in widths], repeatRows=1)
    style = [("GRID", (0, 0), (-1, -1), 0.4, RULE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
             ("BACKGROUND", (0, 0), (-1, 0), HEAD), ("TOPPADDING", (0, 0), (-1, -1), 2.6),
             ("BOTTOMPADDING", (0, 0), (-1, -1), 2.6)]
    t.setStyle(TableStyle(style))
    return t


# ------------------------------------------------------------------------------------ the collaborative's standard
STANDARD = [
    ("1. Purpose and scope", [
        "1.1 This standard sets how the collaborative's member trusts measure emotional instability with the "
        "collaborative's mood app. From 1 April 2027 the adult community mental health teams of every member trust use "
        "the app for the fourteen-day mood assessment offered to patients referred for help with regulating their "
        "emotions, and the standard applies to every assessment that begins on or after that date.",
        "1.2 The measure helps a clinician and patient decide together whether a dialectical behaviour therapy (DBT) "
        "skills group is likely to help. It supports clinical judgement and does not replace it."]),
    ("2. The app", [
        "2.1 An assessment runs for fourteen days. The app prompts at 9:00, 12:00, 15:00, 18:00 and 21:00 each day, "
        "local time, and a prompt can be answered for 45 minutes after it is sent.",
        "2.2 Each prompt asks how the patient feels right now on six items, each scored from 0 (not at all) to 10 "
        "(extremely): down, anxious, irritable and ashamed (the negative affect items), cheerful and relaxed. It also "
        "asks whether the patient is alone or with other people.",
        "2.3 The app records the time each prompt is sent and the time it is answered."]),
    ("3. Measures", [
        "3.1 Negative affect at a prompt is the mean of its four negative affect items.",
        "3.2 Emotional instability is the root mean square of the change in negative affect between adjacent prompts "
        "on the same day where both were answered, taken over the assessment's fourteen days.",
        "3.3 A patient has high emotional instability when their emotional instability is 2.0 or more."]),
    ("4. Reporting", [
        "4.1 The app reports each completed assessment's emotional instability to one decimal place in the patient's "
        "record, with the number of prompts answered.",
        "4.2 Member trusts report to the collaborative each quarter the number of assessments completed and the number "
        "with high emotional instability, by community team."]),
    ("5. Document control", [
        "Version 1.0, 14 August 2026: first issue. Version 1.1, 12 October 2026: the answering window in 2.1 set at "
        "45 minutes after the pilot evaluation; 4.2 added."]),
]

# ------------------------------------------------------------------------------ the trust's DBT operating standard
DBT_STANDARD = [
    ("1. The programme", [
        "1.1 The Complex Emotional Needs Service runs a standard DBT programme for adults referred by the trust's "
        "community mental health teams: weekly individual therapy, a weekly skills group, telephone coaching between "
        "sessions and the therapists' consultation team. Each programme runs for twelve months.",
        "1.2 Programme cohorts start in January, March, May, July, September and November."]),
    ("2. Referral and triage", [
        "2.1 A community mental health team refers a patient through the referral module of the patient record.",
        "2.2 The service acknowledges each referral in a letter to the patient on the day it receives it.",
        "2.3 The service triages each referral within six weeks of receiving it and records one outcome: accepted for "
        "DBT, accepted for mentalisation-based treatment, not accepted, or returned to the referrer for more "
        "information."]),
    ("3. The waiting list", [
        "3.1 A patient accepted for DBT is on the waiting list from the day they are added until the day they are "
        "removed: when they start the programme, decline a place offered to them, are discharged by their team or "
        "move out of the area.",
        "3.2 A patient's wait on a day is the number of days since the day the service received the referral, so a "
        "referral received that day has waited none, and is reported in weeks, the days divided by seven.",
        "3.3 Places in each cohort are offered in the order the service received the referrals, unless the "
        "consultation team agrees a patient's clinical priority."]),
    ("4. Skills groups in community teams", [
        "4.1 From April 2027 the service supports DBT skills groups run within community mental health teams. A group "
        "runs 24 weekly sessions of two and a half hours, led by two co-facilitators.",
        "4.2 A clinician can co-facilitate a group when, on the day the group starts, they have completed DBT skills "
        "group facilitation training of four days or more, as recorded on their learning record; hold an assignment "
        "in a clinical staff group in the team of 0.4 whole-time equivalent or more; and have no leaving date on or "
        "before the group's last session.",
        "4.3 Each co-facilitator joins the service's consultation team for the life of the group and takes "
        "supervision from a DBT therapist."]),
    ("5. Document control", [
        "Version 3, 1 September 2025: sections 4.1 to 4.3 added. Version 3.1, 6 July 2026: section 2.1 updated for the "
        "patient record's referral module."]),
]

PILOT = [
    ("Summary", [
        "Two member trusts piloted the collaborative's mood app with adults referred to their community mental health "
        "teams for help with regulating their emotions, from March to October 2025. 146 patients began an assessment "
        "and 114 completed it. Patients answered 64 per cent of the prompts they were sent, a median of six minutes "
        "after the prompt.",
        "Patients and clinicians found the app easy to use. The evaluation recommends a longer answering window, a "
        "vibration reminder for patients who use a smartwatch and a clearer summary in the patient's record."]),
    ("Who took part", [
        "Patients were aged 18 to 67, a median of 31; 71 per cent were women. Most were referred by their care "
        "coordinator after a first appointment; 23 asked to take part after reading the team's leaflet."]),
    ("Answering", [
        "The share of prompts answered fell from 71 per cent in the first week to 57 per cent in the second. The "
        "commonest reasons patients gave for a missed prompt were being at work (38 per cent of the reasons given), "
        "driving or on public transport (21 per cent), being asleep or resting (14 per cent) and a flat or silent "
        "phone (11 per cent).",
        "With the 30-minute answering window then used, 9 per cent of prompts were opened after the window had "
        "closed."]),
    ("Usability", [
        "The mean System Usability Scale score was 74 (82 patients responded). Patients asked for a larger text "
        "option and for the app to show their answers back to them at the end of the assessment."]),
    ("Clinicians' views", [
        "Clinicians valued seeing how a patient's mood moved through the day, and asked for the assessment summary "
        "to sit in the patient record beside the team's other assessments rather than in a separate portal."]),
    ("Recommendations", [
        "1. Extend the answering window to 45 minutes. 2. Offer a vibration reminder on a smartwatch. 3. Report the "
        "assessment summary into the patient record. 4. Review the measures with the collaborative's clinical "
        "reference group before the app is used across the collaborative."]),
]


def _write(path, title, org_line, footer, sections, accent, extra=None):
    st = styles("LibSans", "LibSans-Bold", accent)
    doc = _doc(path, title, org_line.split(".")[0])
    flow = [Paragraph(esc(title), st["h1"]), Paragraph(esc(org_line), st["sub"])]
    for head, paras in sections:
        flow.append(Paragraph(esc(head), st["h2"]))
        for p in paras:
            flow.append(Paragraph(esc(p), st["body"]))
        if extra and head in extra:
            flow.extend(extra[head](st))
    doc.build(flow, onFirstPage=_footer(footer, "LibSans"), onLaterPages=_footer(footer, "LibSans"))


def ld_course_table(people):
    """Clinical skills programmes: runs (distinct dates) and completions by year, April to March, counted from the
    learning records, with the titles the courses carried in 2024-25."""
    titles = [("PTD-114", "DBT skills group facilitation", 4), ("PTD-118", "Mentalisation-based treatment: awareness", 1),
              ("PTD-205", "Motivational interviewing", 2), ("PTD-226", "Structured clinical management", 3),
              ("PTD-232", "Trauma-informed care in community teams", 1),
              ("EXT-0390", "External course: introduction to DBT", 1),
              ("EXT-0412", "External course: DBT skills training", 4)]
    years = [(dt.date(2022, 4, 1), dt.date(2023, 3, 31)), (dt.date(2023, 4, 1), dt.date(2024, 3, 31)),
             (dt.date(2024, 4, 1), dt.date(2025, 3, 31))]
    rows = [["Programme", "Days", "2022-23", "2023-24", "2024-25"]]
    for code_, title, days in titles:
        cells = []
        for a, b in years:
            recs = [d for p in people for c, d, _n in p.train if c == code_ and a <= d <= b]
            if code_.startswith("EXT"):
                cells.append("%d" % len(recs))
            else:
                cells.append("%d (%d)" % (len(recs), len(set(recs))))
        rows.append([title, str(days)] + cells)
    return rows


def ld_report(people):
    def table(st):
        rows = ld_course_table(people)
        return [grid(rows, [8.0, 1.2, 2.1, 2.1, 2.1], st), Spacer(1, 4),
                Paragraph(esc("Completions in the year, with the number of runs in brackets for courses the trust runs. "
                              "External courses are those staff completed elsewhere and recorded on the learning "
                              "system."), st["sub"])]
    total = sum(1 for p in people for c, d, _n in p.train if dt.date(2024, 4, 1) <= d <= dt.date(2025, 3, 31))
    sections = [
        ("1. The year in summary", [
            "Staff completed %s courses recorded on the learning system between April 2024 and March 2025. Statutory "
            "and mandatory training made up most of them; the clinical skills programmes in section 3 ran on the "
            "schedule agreed with the clinical directorates." % format(total, ",")]),
        ("2. Statutory and mandatory training", [
            "Compliance across the trust's five statutory and mandatory courses stood at 91 per cent at 31 March 2025 "
            "against the trust's 90 per cent target. Data security awareness and Prevent are completed online; "
            "safeguarding at level 3, basic life support and clinical risk assessment are taught in person."]),
        ("3. Clinical skills programmes", [
            "The table counts completions of the clinical skills programmes over the last three years. The DBT skills "
            "group facilitation course prepares clinicians in community teams to co-facilitate skills groups with the "
            "Complex Emotional Needs Service."]),
        ("4. Priorities for 2025-26", [
            "Trauma-informed care will be offered to every community team. The learning team will also review the "
            "course catalogue with the clinical directorates and publish the 2025-26 programme in the spring."]),
    ]
    return sections, {"3. Clinical skills programmes": table}


def write_pdfs(out, people):
    _write(os.path.join(out, K.F_STANDARD), "Mood monitoring standard: emotional instability",
           "%s. Owner: %s, Clinical Lead. Version 1.1, issued %s." % (K.COLLAB, K.PEOPLE["collab"],
                                                                     K.uk_date(K.STANDARD_DATE)),
           "Sallowdene Provider Collaborative, mood monitoring standard, version 1.1", STANDARD, TEAL)
    _write(os.path.join(out, K.F_DBTSTD), "DBT programme operating standard",
           "%s, %s. Approved by %s, Director of Psychological Therapies. Version 3.1, %s." % (
               K.HUB, K.TRUST, K.PEOPLE["director"], K.uk_date(dt.date(2026, 7, 6))),
           "Complex Emotional Needs Service, DBT programme operating standard, version 3.1", DBT_STANDARD, NHS)
    secs, extra = ld_report(people)
    _write(os.path.join(out, K.F_LDREPORT), "Learning and development annual report 2024-25",
           "%s, Learning and Development. Published %s." % (K.TRUST, K.uk_date(K.LD_REPORT_DATE)),
           "Learning and development annual report 2024-25", secs, NHS, extra)
    _write(os.path.join(out, K.F_PILOT), "Mood app pilot evaluation, 2025",
           "%s, digital mental health programme. Published %s." % (K.COLLAB, K.uk_date(dt.date(2025, 12, 3))),
           "Sallowdene Provider Collaborative, mood app pilot evaluation 2025", PILOT, TEAL)
    return [K.F_STANDARD, K.F_DBTSTD, K.F_LDREPORT, K.F_PILOT]


# ---------------------------------------------------------------------------------------------- the committee paper
PAPER = [
    ("1. Purpose", [
        "This paper asks the committee to fund dialectical behaviour therapy (DBT) skills groups in the trust's "
        "community mental health teams for 2027-28. The trust moves to the Sallowdene Provider Collaborative's mood "
        "app on 1 April 2027, and from April the Complex Emotional Needs Service supports skills groups run within "
        "teams under its DBT programme operating standard (section 4)."]),
    ("2. Which teams", [
        "We propose a group in each community mental health team where at least 30 per cent of the patients the team "
        "assessed with the trust's mood app in 2026 have high emotional instability as the collaborative's app will "
        "measure it (the collaborative's mood monitoring standard, sections 2 and 3).",
        "A patient is counted once, on their latest assessment fortnight of 2026 that was completed, with the team "
        "that held their care on the fortnight's first day. A fortnight is completed when the patient answered at "
        "least half of its 112 prompts. Teams are counted as they stand from 1 October 2026, Haddersley North and "
        "Haddersley South as one team (appendix)."]),
    ("3. The groups", [
        "Each group starts on 1 April 2027 and runs 24 weekly sessions, the last on 16 September 2027, with two "
        "co-facilitators from the team. Facilitation, room hire and the service's supervision come to about "
        "GBP 21,400 a group, within the psychological therapies investment line agreed in the 2027-28 plan."]),
    ("4. The service's waiting list", [
        "Patients from every team were waiting for the service's DBT programme at the end of 2026. A skills group in "
        "a team gives its patients skills work while they wait, and the service will review the list with each team "
        "that runs a group."]),
    ("5. Recommendation", [
        "The committee is asked to approve a DBT skills group from 1 April 2027 in each team that meets section 2."]),
]


def write_paper(path):
    import docx
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import Cm, Pt, RGBColor
    d = docx.Document()
    sec = d.sections[0]
    sec.page_width, sec.page_height = Cm(21.0), Cm(29.7)
    sec.left_margin = sec.right_margin = Cm(2.2)
    sec.top_margin, sec.bottom_margin = Cm(1.8), Cm(1.8)
    st = d.styles["Normal"]
    st.font.name = "Arial"
    st.font.size = Pt(10.5)
    st.paragraph_format.space_after = Pt(6)
    grey = RGBColor(0x5d, 0x65, 0x70)
    blue = RGBColor(0x00, 0x5e, 0xb8)
    foot = sec.footer.paragraphs[0]
    foot.text = "Finance and Performance Committee, %s. Page " % K.uk_date(K.MEETING)
    for r in foot.runs:
        r.font.size = Pt(8)
        r.font.color.rgb = grey
    run = foot.add_run()
    for tag, text in (("begin", None), (None, "PAGE"), ("end", None)):
        if tag:
            el = OxmlElement("w:fldChar")
            el.set(qn("w:fldCharType"), tag)
        else:
            el = OxmlElement("w:instrText")
            el.set(qn("xml:space"), "preserve")
            el.text = text
        run._r.append(el)
    run.font.size = Pt(8)
    p = d.add_paragraph()
    r = p.add_run("%s\nFinance and Performance Committee, %s, item 9" % (K.TRUST, K.uk_date(K.MEETING)))
    r.font.size = Pt(9)
    r.font.color.rgb = grey
    h = d.add_paragraph()
    r = h.add_run("DBT skills groups in community mental health teams, 2027-28")
    r.bold = True
    r.font.size = Pt(15)
    r.font.color.rgb = blue
    meta = d.add_table(rows=3, cols=2)
    meta.autofit = False
    for i, (a, b) in enumerate((("From", "%s, Director of Psychological Therapies" % K.PEOPLE["director"]),
                                ("Date", K.uk_date(K.PAPER_DATE)),
                                ("Purpose", "Decision: the teams that run a DBT skills group from 1 April 2027"))):
        meta.cell(i, 0).text = a
        meta.cell(i, 1).text = b
        meta.cell(i, 0).paragraphs[0].runs[0].bold = True
        meta.cell(i, 0).width = Cm(2.6)
        meta.cell(i, 1).width = Cm(14)
    d.add_paragraph()
    for head, paras in PAPER:
        d.add_paragraph().add_run(head).bold = True
        for para in paras:
            d.add_paragraph(para)
    d.add_paragraph().add_run("Appendix. Community mental health teams from 1 October 2026").bold = True
    t = d.add_table(rows=1, cols=3)
    t.style = "Table Grid"
    for j, hh in enumerate(("Team code", "Team", "Locality")):
        c = t.rows[0].cells[j]
        c.text = hh
        c.paragraphs[0].runs[0].bold = True
        c.paragraphs[0].runs[0].font.size = Pt(9.5)
    for code_, name in sorted(K.TEAMS, key=lambda z: z[1]):
        cells = t.add_row().cells
        for j, v in enumerate((code_, name + " CMHT", K.LOCALITY[code_])):
            cells[j].text = v
            cells[j].paragraphs[0].runs[0].font.size = Pt(9.5)
    note = d.add_paragraph("Haddersley CMHT (BW-CM31) was formed on 1 October 2026 from Haddersley North CMHT "
                           "(BW-CM14) and Haddersley South CMHT (BW-CM15).")
    note.runs[0].font.size = Pt(8.5)
    note.runs[0].font.color.rgb = grey
    d.core_properties.title = "DBT skills groups in community mental health teams, 2027-28"
    d.save(path)


def text_of_sections(sections):
    return " ".join(p for _h, ps in sections for p in ps)
