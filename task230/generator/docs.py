"""task230 documents: the output quality standard OQ-4 (docx), the coding procedures and the follow-up field manual
(pdf), the processing plan's November update (xlsx, the capacity report) and the data dictionary (xlsx)."""
from datetime import date, timedelta

import numpy as np
from docx import Document
from docx.shared import Pt, RGBColor
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import params as P
import postprocess
import sim
import world as W

COMPANY = "Office of the Registrar General"


def _styles():
    ss = getSampleStyleSheet()
    body = ParagraphStyle("body", parent=ss["Normal"], fontName="Helvetica", fontSize=9.5, leading=13, spaceAfter=5)
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=14, leading=18, spaceAfter=4)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=10.5, leading=14, spaceBefore=8,
                        spaceAfter=4)
    small = ParagraphStyle("small", parent=body, fontSize=8, leading=10, textColor=colors.HexColor("#444444"))
    return dict(body=body, h1=h1, h2=h2, small=small)


def _footer(text):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.5)
        canvas.setFillColor(colors.HexColor("#555555"))
        canvas.drawString(18 * mm, 10 * mm, text)
        canvas.drawRightString(A4[0] - 18 * mm, 10 * mm, "Page %d" % doc.page)
        canvas.restoreState()
    return draw


def _pdf(path, story, title, author, footer, stamp):
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=16 * mm,
                            bottomMargin=18 * mm, title=title, author=author, creator=author, invariant=1)
    doc.build(story, onFirstPage=_footer(footer), onLaterPages=_footer(footer))
    postprocess.scrub(path, author, stamp)


def _table(rows, widths, size=8.5):
    t = Table(rows, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", size), ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", size),
                           ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#999999")),
                           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E3E8EF")), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return t


HEAD = Font(name="Calibri", bold=True, color="FFFFFF")
FILL = PatternFill("solid", fgColor="2E4A6B")


def _sheet(ws, header, rows, widths=None, wrap=False, formats=None, start=1):
    for i, h in enumerate(header, start=1):
        c = ws.cell(row=start, column=i, value=h)
        c.font = HEAD
        c.fill = FILL
        c.alignment = Alignment(vertical="top", wrap_text=True)
    for r_i, r in enumerate(rows, start=start + 1):
        for c_i, v in enumerate(r, start=1):
            c = ws.cell(row=r_i, column=c_i, value=v)
            c.font = Font(name="Calibri", size=11)
            if wrap:
                c.alignment = Alignment(vertical="top", wrap_text=True)
    if widths:
        for i, w in enumerate(widths, start=1):
            ws.column_dimensions[get_column_letter(i)].width = w
    if formats:
        for col, fmt in formats.items():
            for row in ws.iter_rows(min_row=start + 1, min_col=col, max_col=col):
                for c in row:
                    c.number_format = fmt
    ws.freeze_panes = ws.cell(row=start + 1, column=1)


def _save(wb, path, who, created, modified):
    wb.properties.creator = who
    wb.properties.lastModifiedBy = who
    wb.save(path)
    postprocess.scrub(path, who, modified[:10])
    postprocess.finish_office(path, created, modified, COMPANY)


# ------------------------------------------------------------------------------------------------ OQ-4 (docx)
OQ4 = [
    ("1 Scope", [
        "1.1 This standard applies to the census occupation outputs: counts of persons in employment by ISCO-08 sub-major "
        "group, coded in the Aldmere Occupational Classification 2026 (AOC 2026). It sets the coding quality warning that "
        "the first occupation release of the 2026 Census of Population and Housing carries. The first occupation release "
        "is due on Tuesday 30 March 2027."]),
    ("2 The release population", [
        "2.1 The first occupation release counts every person in employment enumerated by the close of field operations "
        "whose occupation is coded from a write-in. A person whose write-in has not yet been coded on the date of an "
        "assessment is part of the release population. A person in employment whose occupation was left blank is "
        "imputed, and is outside it."]),
    ("3 Coding bias", [
        "3.1 A sub-major group's coding bias in the release is the number of persons in the release population that the "
        "release codes to the group, less the number that the reference coding puts in the group, as a percentage of "
        "the number that the reference coding puts in the group.",
        "3.2 The reference coding of a write-in is the code the coding quality study gives it: two classification "
        "specialists code the write-in independently from the whole form, and the classification lead adjudicates where "
        "they differ.",
        "3.3 In an estimate from the coding quality study, each studied write-in stands for as many coded write-ins as its "
        "selection interval, and the number that the release codes to a group and the number that the reference coding "
        "puts in it are both estimated from the same studied write-ins."]),
    ("4 The coding quality warning", [
        "4.1 A sub-major group whose coding bias is beyond plus or minus 2.0 per cent carries the coding quality warning "
        "in the release. The test is applied to the unrounded bias; the release states each group's bias as a percentage "
        "to one decimal place.",
        "4.2 The Deputy Registrar General (Census Outputs) signs the warning list on the advice of the Methodology "
        "Division and the Head of Census Coding."]),
    ("5 Review", [
        "5.1 The Methodology Division reviews this standard after the first occupation release."]),
]


def standard(path):
    d = Document()
    st = d.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(11)
    for name in ("Heading 1", "Heading 2", "Title"):
        d.styles[name].font.name = "Calibri"
        d.styles[name].font.color.rgb = RGBColor(0x1F, 0x3A, 0x5F)
    d.add_heading("Output quality standard OQ-4: occupation", level=1)
    p = d.add_paragraph("Office of the Registrar General of Aldmere, Methodology Division. Version 2.1, approved 16 March "
                        "2026 by Timothy Taggart, Deputy Registrar General (Census Outputs). Standard owner: Tracey Brien, "
                        "Methodology Division.")
    p.runs[0].font.size = Pt(9)
    for head, paras in OQ4:
        d.add_heading(head, level=2)
        for t in paras:
            d.add_paragraph(t)
    d.core_properties.title = "OQ-4 occupation output quality standard"
    d.core_properties.author = "Tracey Brien"
    d.core_properties.revision = 7
    d.save(path)
    postprocess.scrub(path, "Tracey Brien", "2026-03-16")
    postprocess.finish_office(path, "2026-02-09T10:12:00Z", "2026-03-16T15:40:00Z", COMPANY)


# ------------------------------------------------------------------------------------------------ coding procedures (pdf)
def procedures(path):
    s = _styles()
    st = [Paragraph("Census 2026 coding procedures", s["h1"]),
          Paragraph("Census Processing, Office of the Registrar General. Version 3, 4 May 2026. Owner: Lesley Ahearne, "
                    "Head of Census Coding.", s["small"]), Spacer(1, 6)]
    secs = [
        ("1 Purpose", ["These procedures set how the occupation write-ins on census forms are coded to the Aldmere "
                       "Occupational Classification 2026 (AOC 2026), which extends the ISCO-08 unit groups by a fifth "
                       "digit. The industry write-ins are coded by the same teams under the industry procedures."]),
        ("2 Load batches", ["Forms are loaded into the coding system (CODA) as load batches: one capture mode's loads of "
                            "one day make one batch (ONL for online returns, PAP for paper returns once scanned and "
                            "recognised, FUP for follow-up questionnaires from the field tablets). The batch number carries "
                            "the mode and the load date. Batches are coded first in, first out."]),
        ("3 The autocoder", ["CODA's autocoder reads each write-in and suggests an ISCO-08 unit group with a score from 0 "
                             "to 1. A suggestion scoring 0.90 or more becomes the production code (the automatic path). A "
                             "write-in scoring under 0.90 goes to a clerical coder (the clerical path), who codes it to the "
                             "five-digit AOC 2026 code from the whole form: the write-in, the industry and employer answers "
                             "and the person's qualifications. CODA stores the autocoder's suggestion and score on every "
                             "write-in, on either path."]),
        ("4 Clerical coding", ["Five clerical coding teams work the clerical path: Coding Teams 1 and 2 on the day shift "
                               "(08:00 to 16:30), Coding Teams 3 and 4 on the evening shift (14:00 to 22:30) and Coding "
                               "Team 5 on the night shift (22:00 to 06:30, Monday to Thursday nights, except the night of the "
                               "last working day of each month, when CODA closes for month-end processing). Each coder works "
                               "under a CODA coder id and saves a code write-in by write-in. A team lead in each team "
                               "supervises and does not code. Coding staff record their hours in the timesheet system "
                               "against these activities: OCC occupation coding, IND industry coding, QRY a turn on the "
                               "query desk, TRN training, SUP supervision."]),
        ("5 Queries", ["A coder who cannot place a write-in from the form refers it to the query desk in CODA and saves "
                       "the code once the desk has answered; the desk does not code. Experienced coders staff the desk in "
                       "turn and book that time as QRY."]),
        ("6 The coding front", ["CODA serves each coder the oldest loaded write-ins first, so batches are coded in the "
                                "order they were loaded. Coding weeks run from Monday to Sunday; coding week 1 began on "
                                "Monday 4 May 2026. The processing plan reports the coding front and the write-ins still "
                                "to code each week."]),
        ("7 Production codes", ["The production code is the ISCO-08 unit group (four digits) on the automatic path and "
                                "the AOC 2026 code (five digits) on the clerical path. The outputs aggregate production "
                                "codes to the ISCO-08 sub-major group, the first two digits of either code."]),
        ("8 The coding quality study", ["The study measures the coding of every load batch on both coding paths. CODA "
                                        "selects write-ins systematically from each batch and path: in self-response "
                                        "batches (ONL, PAP) one write-in in ten on the automatic path and one in four on "
                                        "the clerical path; in follow-up batches (FUP) one write-in in two on either path. "
                                        "Two classification specialists recode each selected write-in independently from "
                                        "the whole form and the classification lead adjudicates where they differ. The "
                                        "study's codes measure the coding; they are not written back to production."]),
    ]
    for h, paras in secs:
        st.append(Paragraph(h, s["h2"]))
        for t in paras:
            st.append(Paragraph(t, s["body"]))
    _pdf(path, st, "Census 2026 coding procedures", "Lesley Ahearne",
         "Census 2026 coding procedures, version 3 (4 May 2026)", "2026-05-04")


# ------------------------------------------------------------------------------------------------ field manual (pdf)
def manual(path):
    s = _styles()
    st = [Paragraph("Census 2026 field manual, chapter 5: follow-up", s["h1"]),
          Paragraph("Field Operations, Office of the Registrar General. Version 2, 1 June 2026. Owner: Erica Phayre, Field "
                    "Operations Manager.", s["small"]), Spacer(1, 6)]
    secs = [
        ("5.1 The follow-up workload", ["Follow-up covers every address on the address register with no census return "
                                        "on Friday 19 June 2026. Enumerators call from Monday 22 June; field operations "
                                        "close on Saturday 31 October 2026."]),
        ("5.2 Calls", ["Make up to six calls at an address, at different times of day and on different days of the week. "
                       "Record every call on the tablet at the doorstep with its outcome code. Number the calls at an "
                       "address in order."]),
        ("5.3 Outcome codes", []),
        ("5.4 Proxy interviews", ["From the third call, where no member of the household can be found, complete the "
                                  "questionnaire from a proxy: a neighbour, the landlord or building manager, or a relative "
                                  "living elsewhere who knows the household. Record who answered."]),
        ("5.5 Closing a case", ["A case closes on its last accepted outcome. An interview with a household member after a "
                                "proxy interview replaces the proxy questionnaire, which is withdrawn. A census return "
                                "received while a case is open closes it (outcome 60) and no further calls are made."]),
        ("5.6 Your tablet", ["Sync your tablet at the end of every working day. Report a lost or faulty tablet to your "
                             "field supervisor at once; a replacement tablet is issued with your open cases."]),
        ("5.7 Calling cards", ["When nobody answers, leave a calling card with the household's online access code and the "
                               "census helpline number, and record the call as 31."]),
        ("5.8 Your caseload", ["Your caseload is the follow-up addresses in your enumeration districts. From Tuesday 1 "
                               "September, in the mop-up phase, your field supervisor reviews every open case with you "
                               "each week and may move cases between enumerators; a case keeps its calls."]),
        ("5.9 Safety and conduct", ["Do not enter a property. Call between 09:00 and 21:00 only. Show your census "
                                    "identity card at every call and report any incident to your field supervisor the "
                                    "same day."]),
    ]
    codes = [["Code", "Outcome"], ["10", "Interview completed with a household member"],
             ["20", "Interview completed with a proxy (from the third call)"], ["31", "No contact, calling card left"],
             ["32", "Refusal"], ["40", "Vacant dwelling"], ["50", "Not a dwelling (demolished, derelict, non-residential)"],
             ["60", "Census return received (closed by the office)"]]
    for h, paras in secs:
        st.append(Paragraph(h, s["h2"]))
        for t in paras:
            st.append(Paragraph(t, s["body"]))
        if h.startswith("5.3"):
            st.append(_table(codes, [20 * mm, 120 * mm]))
            st.append(Spacer(1, 4))
    _pdf(path, st, "Census 2026 field manual, chapter 5", "Erica Phayre",
         "Census 2026 field manual, chapter 5 (version 2, 1 June 2026)", "2026-06-01")


# ------------------------------------------------------------------------------------------------ processing plan (xlsx)
def plan(path, S, T, Cd):
    """the capacity report: can the clerical path finish by the coding close; capacity only"""
    reg, ext = T["reg"], T["ext"]
    bt_reg = np.where(np.isin(reg["capture_mode"], ["ONLINE", "PAPER"]), "Self-response", "Follow-up")
    bt_ext = np.where(np.char.startswith(ext["load_batch"].astype(str), "FUP"), "Follow-up", "Self-response")
    rows = []
    out = {}
    for b in ("Self-response", "Follow-up"):
        rec = int(reg["occupation_writeins"][bt_reg == b].sum())
        m = bt_ext == b
        auto = int((m & (ext["coding_path"] == "AUTO")).sum())
        cler = int((m & (ext["coding_path"] == "CLERICAL")).sum())
        rows.append([b, rec, auto + cler, auto, cler, rec - auto - cler])
        out[b] = rec - auto - cler
    rows.append(["All", sum(r[1] for r in rows), sum(r[2] for r in rows), sum(r[3] for r in rows), sum(r[4] for r in rows),
                 sum(r[5] for r in rows)])
    recent = (bt_ext == "Follow-up") & (ext["coding_week"] >= 25)
    sc = ext["autocoder_score"][recent]
    share90 = float((sc < 0.90).mean())
    share80 = float((sc < 0.80).mean())
    remaining = rows[-1][5]
    # October's own clerical rate and occupation hours a coder, from the extract and the timesheets
    import records as R_
    oct_c = sum(1 for p_, t_ in zip(ext["coding_path"], ext["coded_at"]) if p_ == "CLERICAL" and t_.month == 10)
    oct_lines = [r for r in T["ts"] if r["activity"] == "OCC" and r["work_date"].month == 10]
    oct_h = sum(r["hours"] for r in oct_lines)
    staff_oct = len({r["staff_no"] for r in oct_lines})
    oct_days = len([x for x in R_.working_days(date(2026, 10, 1), date(2026, 10, 31))])
    rate = oct_c / oct_h
    per_coder = oct_h / staff_oct / (oct_days / 5.0)
    coders = sum(1 for s_, c_, t_, k_, f_, e_ in R_.ROSTER if k_ == "PERMANENT" and e_ is None)
    per_week = coders * per_coder * rate
    weeks = 8.0
    q90 = remaining * share90
    q80 = remaining * share80
    wb = Workbook()
    ws = wb.active
    ws.title = "Position 13 Nov"
    ws["A1"] = "Census 2026 processing plan: coding capacity to the coding close (November update)"
    ws["A1"].font = Font(name="Calibri", bold=True, size=13)
    ws["A2"] = ("Version 4, 13 November 2026. Owner: Lesley Ahearne, Head of Census Coding. Answers whether the clerical "
                "path can finish by the coding close on 22 January 2027; capacity only.")
    ws["A2"].font = Font(name="Calibri", italic=True, size=10)
    _sheet(ws, ["Batch type", "Write-ins received by the close of field operations", "Coded by 13 Nov",
                "Automatic path", "Clerical path", "Still to code"], rows, widths=[18, 22, 16, 16, 14, 14],
           formats={c: "#,##0" for c in range(2, 7)}, start=4)
    ws3 = wb.create_sheet("Capacity")
    cap_rows = [["Follow-up write-ins coded in coding weeks 25 to 28", int(recent.sum())],
                ["Of these, scoring under 0.90", round(share90, 4)],
                ["Of these, scoring under 0.80", round(share80, 4)],
                ["Clerical coders from 23 November (permanent staff; temporary contracts end 20 November)", coders],
                ["Occupation coding hours a coder a week (October timesheets)", round(per_coder, 1)],
                ["Clerical occupation write-ins an hour (October extract and timesheets)", round(rate, 1)],
                ["Clerical capacity a week", round(per_week)],
                ["Working weeks from 16 November to the coding close (closed 24 December to 1 January)", weeks],
                ["Clerical capacity to the coding close", round(per_week * weeks)],
                ["Clerical queue at acceptance score 0.90", round(q90)],
                ["Weeks to clear at 0.90", round(q90 / per_week, 1)],
                ["Clerical queue at acceptance score 0.80", round(q80)],
                ["Weeks to clear at 0.80", round(q80 / per_week, 1)]]
    _sheet(ws3, ["Item", "Value"], cap_rows, widths=[78, 14])
    for r_i, fmt in enumerate(["#,##0", "0.0%", "0.0%", "#,##0", "0.0", "0.0", "#,##0", "0", "#,##0", "#,##0", "0.0",
                               "#,##0", "0.0"], start=2):
        ws3.cell(row=r_i, column=2).number_format = fmt
    ws4 = wb.create_sheet("Decision")
    _sheet(ws4, ["Decision", "Date"],
           [["From Monday 16 November 2026 the autocoder accepts a suggestion scoring 0.80 or more as the production "
             "code. Write-ins already coded keep their codes. Agreed by the census programme board.", "2026-11-12"]],
           widths=[96, 12], wrap=True)
    _save(wb, path, "Lesley Ahearne", "2026-09-28T08:30:00Z", "2026-11-13T16:05:00Z")
    out.update(share90=share90, share80=share80, q90=q90, q80=q80, per_week=per_week)
    return out


# ------------------------------------------------------------------------------------------------ data dictionary (xlsx)
DICT = {
    "coding_extract": ("One row per person write-in coded by Friday 13 November 2026.", [
        ("doc_id", "CODA document number of the form"), ("person_no", "Person number on the form"),
        ("load_batch", "Load batch: capture mode (ONL, PAP, FUP) and load date (yymmdd)"),
        ("coding_week", "Coding week, Monday to Sunday; week 1 starts on Monday 4 May 2026"),
        ("autocoder_code", "ISCO-08 unit group the autocoder suggested"), ("autocoder_score", "Autocoder score, 0 to 1"),
        ("coding_path", "AUTO (the suggestion became the production code) or CLERICAL"),
        ("production_code", "The production code: an ISCO-08 unit group (four digits) on the automatic path, an AOC 2026 "
                            "code (five digits) on the clerical path"),
        ("coder_id", "CODA coder id of the clerical coder who saved the code (blank on the automatic path)"),
        ("coded_at", "Aldmere local time the production code was saved")]),
    "coding_quality_study": ("One row per write-in selected for the coding quality study, coded by 13 November 2026.", [
        ("study_ref", "Study record number"), ("doc_id", "CODA document number"), ("person_no", "Person number on the form"),
        ("load_batch", "Load batch"), ("batch_type", "SELF-RESPONSE (ONL, PAP) or FOLLOW-UP (FUP)"),
        ("coding_path", "AUTO or CLERICAL"), ("selection_interval", "One write-in in this many was selected from the "
                                                                    "record's batch and coding path"),
        ("occupation_writein", "The job title as captured"), ("autocoder_code", "Autocoder's suggested unit group"),
        ("autocoder_score", "Autocoder score"), ("production_code", "Production code"),
        ("reference_code", "The study's adjudicated AOC 2026 code"),
        ("reference_basis", "AGREED (both specialists gave the code) or ADJUDICATED")]),
    "receipt_register": ("One row per census form received by the close of field operations.", [
        ("doc_id", "CODA document number, issued when the form is loaded"), ("questionnaire_id", "Questionnaire number"),
        ("address_id", "Address register id"), ("ed_code", "Enumeration district"),
        ("capture_mode", "ONLINE, PAPER or FIELD"), ("received_date", "Date the form was registered as received"),
        ("load_batch", "CODA load batch (blank: not yet loaded on 13 November)"),
        ("usual_residents", "Persons usually resident"), ("in_employment", "Persons in employment"),
        ("occupation_writeins", "Persons in employment with an occupation write-in")]),
    "field_visit_log": ("One row per call stored by the field operations system, and one per administrative closure.", [
        ("visit_id", "Record number in the field operations system"), ("address_id", "Address register id (the case)"),
        ("ed_code", "Enumeration district"), ("staff_id", "Enumerator (blank on an administrative closure)"),
        ("visit_no", "Call number at the address"), ("visit_time", "Local time of the call, from the tablet"),
        ("outcome_code", "Outcome code (field manual 5.3)"),
        ("proxy_respondent", "Who answered a proxy interview"),
        ("questionnaire_id", "Questionnaire completed at the call (10, 20) or the return that closed the case (60)"),
        ("tablet_id", "Tablet that recorded the call"),
        ("synced_at", "Local time the record reached the field operations system")]),
    "coding_staff_register": ("One row per member of staff who has worked in census coding since 4 May 2026.", [
        ("staff_no", "HR staff number"), ("coder_id", "CODA coder id"), ("team", "Coding team (for a leaver, the team left)"),
        ("role", "CODER or TEAM LEAD"), ("contract", "PERMANENT or TEMPORARY"), ("status", "IN POST or LEFT"),
        ("started", "First day in census coding"), ("left", "Last day in census coding (blank: in post)")]),
    "coding_staff_movements": ("One row per movement of coding staff since 4 May 2026.", [
        ("staff_no", "HR staff number"), ("coder_id", "CODA coder id held"), ("movement", "STARTED, TRANSFERRED or LEFT"),
        ("team_from", "Team left"), ("team_to", "Team joined"),
        ("effective_date", "STARTED and TRANSFERRED: first day in the team joined; LEFT: the leaving date, the last day "
                           "in post")]),
    "coding_timesheets": ("One row per timesheet line.", [
        ("staff_no", "HR staff number"), ("work_date", "Date the shift started"), ("activity", "OCC, IND, QRY, TRN or SUP"),
        ("hours", "Hours worked on the activity (a team lead corrects a line with a further line of negative hours)"),
        ("entered_on", "Date the line was entered"), ("note", "Note")]),
    "enumeration_districts": ("One row per enumeration district.", [
        ("ed_code", "Enumeration district"), ("region_code", "Region"), ("region_name", "Region name"),
        ("addresses_listed", "Addresses on the address register")]),
    "occupation_classification": ("One row per AOC 2026 code.", [
        ("aoc_code", "AOC 2026 code: the ISCO-08 unit group and a national fifth digit (0 where the unit group has "
                     "no national detail)"), ("aoc_title", "AOC 2026 title"),
        ("isco08_unit_group", "ISCO-08 unit group"), ("isco08_unit_title", "ISCO-08 unit group title"),
        ("isco08_sub_major", "ISCO-08 sub-major group"), ("isco08_sub_major_title", "ISCO-08 sub-major group title")]),
}


DICT_FILES = {"coding_extract": "census2026_occupation_coding_extract.parquet",
              "coding_quality_study": "census2026_coding_quality_study.csv",
              "receipt_register": "census2026_receipt_register.csv",
              "field_visit_log": "field_visit_log_jun_oct_2026.csv",
              "coding_staff_register": "coding_staff_register.csv",
              "coding_staff_movements": "coding_staff_movements_2026.csv",
              "coding_timesheets": "coding_timesheets_21sep_01nov2026.csv",
              "enumeration_districts": "enumeration_districts_2026.csv",
              "occupation_classification": "aoc2026_occupation_classification.csv"}


def dictionary(path):
    wb = Workbook()
    first = True
    for name, (grain, fields) in DICT.items():
        ws = wb.active if first else wb.create_sheet()
        first = False
        ws.title = name[:31]
        ws["A1"] = DICT_FILES[name] + ": " + grain
        ws["A1"].font = Font(name="Calibri", italic=True)
        _sheet(ws, ["Field", "Description"], [list(f) for f in fields], widths=[22, 100], start=3)
    _save(wb, path, "Lesley Ahearne", "2026-07-02T09:00:00Z", "2026-11-13T15:20:00Z")


def write_all(target, FILES, S, T, Cd):
    import os
    standard(os.path.join(target, FILES["standard"]))
    procedures(os.path.join(target, FILES["procedures"]))
    manual(os.path.join(target, FILES["manual"]))
    pf = plan(os.path.join(target, FILES["plan"]), S, T, Cd)
    dictionary(os.path.join(target, FILES["dictionary"]))
    return dict(plan=pf, counts={})
