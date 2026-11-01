"""The governing documents: Pinewater EMC's Contractor Safety Performance Standard CS-4, Redbud's Crew Safety
Recognition Programme (HR-14) and the notice ending it on 31 December 2026."""
import io

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import postprocess as PP
import world as W

PINE = colors.HexColor("#1B4D3E")
RED = colors.HexColor("#7A2E1F")


def _styles(accent):
    ss = getSampleStyleSheet()
    return dict(
        body=ParagraphStyle("b", parent=ss["Normal"], fontName="Helvetica", fontSize=9.8, leading=13.2, spaceAfter=6),
        head=ParagraphStyle("h", parent=ss["Normal"], fontName="Helvetica-Bold", fontSize=10.4, leading=14,
                            spaceBefore=7, spaceAfter=3, textColor=accent),
        title=ParagraphStyle("t", parent=ss["Normal"], fontName="Helvetica-Bold", fontSize=14.5, leading=18,
                             spaceAfter=3),
        small=ParagraphStyle("s", parent=ss["Normal"], fontName="Helvetica-Oblique", fontSize=8.6, leading=11,
                             spaceAfter=10),
        cell=ParagraphStyle("c", parent=ss["Normal"], fontName="Helvetica", fontSize=8.8, leading=11),
    )


def _footer(text):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.4)
        canvas.setFillColor(colors.HexColor("#555555"))
        canvas.drawString(0.9 * inch, 0.6 * inch, text)
        canvas.drawRightString(letter[0] - 0.9 * inch, 0.6 * inch, "Page %d" % doc.page)
        canvas.restoreState()
    return draw


def _build(path, title, author, story, foot, created, modified):
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=letter, leftMargin=0.9 * inch, rightMargin=0.9 * inch,
                            topMargin=0.75 * inch, bottomMargin=0.9 * inch, title=title, author=author,
                            creator=author, producer=author)
    doc.build(story, onFirstPage=_footer(foot), onLaterPages=_footer(foot))
    open(path, "wb").write(buf.getvalue())
    PP.normalize_pdf(path, created, modified)


def standard_pdf(path):
    st = _styles(PINE)
    P = lambda t, s="body": Paragraph(t, st[s])
    story = [
        P("Contractor Safety Performance Standard CS-4", "title"),
        P("Pinewater Electric Membership Corporation. Revision 3, effective 1 January 2026. Owner: Jerome Warren, "
          "Contractor Safety Manager. Supersedes Revision 2 (2023).", "small"),
        P("1. Purpose", "head"),
        P("This standard sets how Pinewater EMC measures, plans and oversees the safety performance of the contractors "
          "whose field employees work on its system."),
        P("2. Scope", "head"),
        P("It applies to every contractor that works on Pinewater's system under a master services agreement with "
          "field employees of its own. Subcontractors report to the contractor that engaged them and are covered by "
          "that contractor's subcontractor safety plan, not by this standard's measures."),
        P("3. Definitions", "head"),
        P("3.1 <b>Recordable injury.</b> A work-related injury or illness that meets the general recording criteria "
          "of 29 CFR 1904.7: death, days away from work, restricted work or transfer to another job, medical "
          "treatment beyond first aid, loss of consciousness, or a significant injury or illness diagnosed by a "
          "physician or other licensed health care professional. A case is counted once, as the contractor's case "
          "record finally classifies it, and in the period of its injury date. First aid (29 CFR 1904.7(b)(5)(ii)) "
          "is not a recordable injury."),
        P("3.2 <b>Field employee.</b> Every employee of the contractor who works on Pinewater's system in the field, "
          "whether in a crew or alone."),
        P("3.3 <b>Pinewater work.</b> Work performed under a Pinewater work order, service order or locate ticket. "
          "Work for another utility, including mutual-aid restoration off Pinewater's system, is not Pinewater work, "
          "even when the contractor's crews perform it."),
        P("3.4 <b>Hours worked.</b> Hours actually worked by field employees on Pinewater work, regular and overtime. "
          "Paid leave, holiday pay and hours on work that is not Pinewater work are excluded."),
        P("3.5 <b>Recordable rate.</b> Recordable injuries multiplied by 200,000 and divided by the hours worked, for "
          "the same employees, work and period."),
        P("3.6 <b>District.</b> The Pinewater operating district of the crew or technician team the employee belongs "
          "to on the day in question."),
        P("3.7 <b>First-aid case.</b> A work-related injury to a field employee that needed first aid only (29 CFR "
          "1904.7(b)(5)(ii)). Each injury is counted once, as the contractor's case record finally classifies it, "
          "and in the period of its injury date."),
        P("4. The contract-year safety plan", "head"),
        P("By 15 November each year the contractor submits a safety plan for the next contract year (1 January to 31 "
          "December). The plan states:"),
        P("(a) the number of recordable injuries the contractor forecasts its field employees will record on "
          "Pinewater work in the contract year, in total and for each calendar quarter;"),
        P("(b) the recordable rate that number makes on the hours worked in the contractor's work plan for the "
          "contract year, in total and for each quarter; and"),
        P("(c) the contractor's recordable injuries and first-aid cases on Pinewater work in the current year, from "
          "the first pay period beginning in January to the end of the last pay period closed before the plan is "
          "prepared, by district and calendar quarter."),
        P("The forecast is the contractor's own and is made on its own records. Pinewater does not prescribe the "
          "method; it reviews the plan against the contractor's records under section 7."),
        P("5. The limit", "head"),
        P("The recordable rate limit for a contract year is 3.0. A contractor whose plan forecasts a rate above the "
          "limit enters enhanced oversight under section 6 for that contract year; a contractor whose recorded rate "
          "for a contract year exceeds the limit enters it for the following contract year."),
        P("6. Enhanced oversight", "head"),
        P("Monthly safety reviews with Pinewater's Contractor Safety Manager, a corrective action plan within 30 days "
          "of entry, and field audits at Pinewater's discretion. A contractor leaves enhanced oversight after a "
          "contract year whose recorded rate is at or below the limit."),
        P("7. Records and review", "head"),
        P("Pinewater may review the contractor's OSHA 300 log and case records, its crew and technician assignments "
          "and its timesheets for any period the plan relies on."),
    ]
    _build(path, "Contractor Safety Performance Standard CS-4", "Pinewater EMC", story,
           "Pinewater EMC  |  CS-4 Contractor Safety Performance Standard, Revision 3",
           b"D:20251119143000-05'00'", b"D:20251208091500-05'00'")


def programme_pdf(path):
    st = _styles(RED)
    P = lambda t, s="body": Paragraph(t, st[s])
    rows = [["Crew type", "In the programme"], ["Overhead line crews", "Yes"], ["Underground distribution crews", "Yes"],
            ["Substation crews", "Yes"], ["Vegetation management crews", "Yes"],
            ["Meter services technicians", "No (they work alone)"], ["Underground locating technicians", "No (they work alone)"]]
    tbl = Table([[Paragraph(c, st["cell"]) for c in r] for r in rows], colWidths=[3.0 * inch, 2.6 * inch])
    tbl.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#EFE3DF")),
                             ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#999999")),
                             ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    story = [
        P("HR-14 Crew Safety Recognition Programme", "title"),
        P("Redbud Line Services. Revision 2, effective 11 January 2021; replaces Revision 1 (2018). Owners: "
          "Samantha Galvan, Director of Environment, Health and Safety, and Sergio Phillips, Payroll and Benefits "
          "Manager.", "small"),
        P("1. Who is in the programme", "head"),
        P("Members of Redbud field crews. Technicians who work alone are not in the programme."),
        tbl,
        Spacer(1, 8),
        P("2. The award", "head"),
        P("A crew earns a safety recognition award of USD 150 for each member on the crew on the day it completes 90 "
          "consecutive calendar days without a recordable injury to any of its members. The award is paid in the "
          "first payroll after the pay period in which the 90th day falls, under earning code CREW90, to each member "
          "on the crew that day."),
        P("3. The count", "head"),
        P("Counts under Revision 1 closed on 10 January 2021, and every crew's count under this revision started on "
          "11 January 2021. After that the count starts on the day after the crew's last recordable injury or the "
          "day after the last day of its last award, whichever is later. Every calendar day counts, including "
          "weekends, holidays and days the crew works off Pinewater's system. A recordable injury to any member "
          "restarts the count from the next day. A first-aid case does not affect the count."),
        P("4. Crews that change", "head"),
        P("A member who joins a crew joins its count. When a crew is recoded at a reorganisation its count carries "
          "over under the new code."),
        P("5. Administration", "head"),
        P("The EHS office confirms recordable injuries from the case records each week and sends payroll the list of "
          "crews that completed a count in the pay period, with their members on the day."),
    ]
    _build(path, "HR-14 Crew Safety Recognition Programme", "Redbud Line Services", story,
           "Redbud Line Services  |  HR-14 Crew Safety Recognition Programme, Revision 2",
           b"D:20201207101500-05'00'", b"D:20210104163000-05'00'")


def notice_docx(path):
    """HR's notice of 2 October 2026 ending HR-14 on 31 December 2026."""
    import docx
    from docx.shared import Pt
    d = docx.Document()
    s = d.styles["Normal"]
    s.font.name = "Calibri"
    s.font.size = Pt(11)
    d.add_heading("Changes to crew recognition for 2027", level=1)
    for t in [
        "To: all field crews and supervisors. From: Sergio Phillips, Payroll and Benefits Manager, and Norma Hinton, "
        "Vice President, Operations. Date: 2 October 2026.",
        "The Crew Safety Recognition Programme (HR-14) ends on 31 December 2026. Awards for counts completed on or "
        "before 31 December 2026 will be paid in the usual way, the last of them in the payroll of 8 January 2027. "
        "Counts still running on 31 December 2026 close on that day without an award.",
        "From 1 January 2027 the recognition budget moves to the field leadership programme, which recognises "
        "supervisors and crews for the quality of their job briefings and for taking part in the safety observation "
        "programme. The EHS team will brief supervisors on the new programme in November.",
        "Report every injury to your supervisor and the EHS office on the day it happens.",
        "Questions about awards already earned go to the payroll team; questions about the field leadership "
        "programme go to your district safety coordinator.",
    ]:
        d.add_paragraph(t)
    d.save(path)
    PP.normalize_docx(path, W.PEOPLE["payroll"], W.PEOPLE["ops"], "2026-09-30T14:21:00Z", "2026-10-02T10:48:00Z",
                      3, 41, "t130-notice", title="Changes to crew recognition for 2027", company=W.COMPANY)
