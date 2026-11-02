"""The Trust's three governing documents, as PDFs (reportlab, invariant mode for byte-identical rebuilds)."""
from __future__ import annotations

import datetime as dt
import os

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import world as W

SS = getSampleStyleSheet()
STAMPS = {"operational_plan_2027_28_activity_lines.pdf": b"D:20261007143000", "elective_capacity_plan_2027_28_general_surgery.pdf": b"D:20261022161500",
          "elective_access_policy_v6.pdf": b"D:20250626110000"}
H1 = ParagraphStyle("h1", parent=SS["Heading1"], fontName="Helvetica-Bold", fontSize=14, spaceAfter=6)
H2 = ParagraphStyle("h2", parent=SS["Heading2"], fontName="Helvetica-Bold", fontSize=11, spaceBefore=8, spaceAfter=4)
BODY = ParagraphStyle("b", parent=SS["BodyText"], fontName="Helvetica", fontSize=9.2, leading=12.2, spaceAfter=5)
SMALL = ParagraphStyle("s", parent=BODY, fontSize=8, leading=10)


def _pdf(path, title, author, story):
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm,
                            bottomMargin=18 * mm, title=title, author=author, creator="Marlstead and Fennick Hospitals NHS Trust", producer="Marlstead and Fennick Hospitals NHS Trust", invariant=1)

    def foot(c, d):
        c.saveState()
        c.setFont("Helvetica", 7.5)
        c.drawString(20 * mm, 10 * mm, "Marlstead and Fennick Hospitals NHS Trust")
        c.drawRightString(190 * mm, 10 * mm, "Page %d" % d.page)
        c.restoreState()
    doc.build(story, onFirstPage=foot, onLaterPages=foot)
    raw = open(path, "rb").read()
    for old in (b" ReportLab Generated PDF document (opensource)", b"% ReportLab generated PDF document -- digest (opensource)"):
        raw = raw.replace(old, (b"%" if old[:1] == b"%" else b" ") + b" " * (len(old) - 1))
    raw = raw.replace(b"D:20000101000000", STAMPS.get(os.path.basename(path), b"D:20261031090000"))
    open(path, "wb").write(raw)


def _table(data, widths, small=True):
    st = SMALL if small else BODY
    t = Table([[Paragraph(str(c), st) for c in r] for r in data], colWidths=[w * mm for w in widths], repeatRows=1)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.grey), ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#dfe6ee")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return t


def definitions(out):
    P = lambda t: Paragraph(t, BODY)
    s = [Paragraph("2027/28 Operational Plan: Activity Line Definitions", H1),
         P("Performance and Information, version 1.2, 7 October 2026. Applies to every activity and waiting list line the Trust "
           "submits in its 2027/28 operational plan through the Marlstead and Coldvale Integrated Care Board."),
         Paragraph("1. Basis of the plan", H2),
         P("Each activity line is planned as the Trust's central expectation for financial year 2027/28 (1 April 2027 to 31 March "
           "2028): the expected number, not a prudent, stretch or contract figure. Lines are planned consistently with the services, "
           "capacity and pathways set out in the Trust's 2027/28 plans as approved, including the elective capacity plan, the urgent "
           "and emergency care plan and the workforce plan. History used in planning is counted on the definitions below."),
         P("Activity is counted at the Trust's two hospitals, Marlstead General Hospital and Fennick Hospital (the Wyecross Elective "
           "Centre is part of Fennick Hospital), whatever the patient's age or place of residence. Annual lines are submitted to the "
           "nearest 50 where the line is under 5,000 a year."),
         Paragraph("2. Non-elective lines", H2),
         _table([["Line", "Definition"],
                 ["NEL-ALL-01 Emergency admissions", "Hospital provider spells with an emergency admission method (codes 21 to 2D; in the Trust EPR the methods beginning Emergency), counted once per spell in the month of the admission date."],
                 ["NEL-GS-04 Emergency admissions, general surgery", "As NEL-ALL-01, where the first finished consultant episode of the spell is under treatment function 100."],
                 ["NEL-GS-07 Emergency admissions, gallstone disease", "As NEL-ALL-01, where the primary diagnosis of the first finished consultant episode of the spell is in K80 (any fourth character), K81 (any fourth character), K83.0 or K85.1, under any treatment function."],
                 ["NEL-GS-09 Emergency admissions, acute appendicitis", "As NEL-ALL-01, first episode primary diagnosis K35 to K37."]], [55, 115]),
         Paragraph("3. Elective lines", H2),
         _table([["Line", "Definition"],
                 ["EL-GS-01 Elective day cases, general surgery", "Spells with admission method 11 or 12 under treatment function 100 in which the patient was admitted and discharged on the same day."],
                 ["EL-GS-02 Elective ordinary admissions, general surgery", "Spells with admission method 11 or 12 under treatment function 100 other than day cases."]], [55, 115]),
         Paragraph("4. Waiting list lines", H2),
         _table([["Line", "Definition"],
                 ["RTT-GS-02 Admitted waiting list, general surgery", "Patients waiting at the month end for an operation or procedure in general surgery at the hospital, one count for each operation a patient is waiting for."],
                 ["RTT-GS-03 Admitted waiting list, 52 weeks or more", "Of RTT-GS-02, those whose wait at the month end, measured from the date the Trust received the referral that began the patient's wait for the operation, is 364 days or more."]], [55, 115]),
         P("Waiting times follow the national referral to treatment rules. Month ends are the last calendar day of the month.")]
    _pdf(os.path.join(out, "operational_plan_2027_28_activity_lines.pdf"), "2027/28 Operational Plan: Activity Line Definitions",
         "Performance and Information", s)


def capacity(out, traj):
    P = lambda t: Paragraph(t, BODY)
    months = [W.month_end(m) for m in range(W.REC_MONTHS, W.N_MONTHS)]
    head = ["Month end"] + [d.strftime("%b %Y") for d in months]
    rows = [head]
    for g, name in (("chole", "Laparoscopic cholecystectomy"), ("hernia", "Hernia repair"), ("other", "Other general surgery")):
        rows.append([name] + ["{:,}".format(traj[(g, d)]) for d in months])
    half = (len(head) + 1) // 2
    t1 = [r[:1] + r[1:half] for r in rows]
    t2 = [r[:1] + r[half:] for r in rows]
    s = [Paragraph("Elective Capacity Plan 2027/28: General Surgery", H1),
         P("Planned Care Programme Board, approved by the Trust Board on 22 October 2026."),
         Paragraph("1. Summary", H2),
         P("The Wyecross Elective Centre opens on the Fennick Hospital site on 11 January 2027 with four day-case theatres, a "
           "twelve-bay recovery unit and a pre-operative assessment suite. General surgery takes 22 of its 40 weekly sessions from "
           "opening, with orthopaedic hand and foot, urology and gynaecology lists in the remainder. Marlstead General Hospital's "
           "main theatres keep their general surgery elective sessions for patients who need an overnight stay or a higher level of "
           "care, and keep their emergency lists unchanged."),
         P("From opening, Wyecross books patients in clinical priority order and then in the order they were added to the list, "
           "about twelve weeks ahead, with pre-operative assessment completed at the first visit. The general surgery admitted "
           "lists of both hospitals are pooled for Wyecross booking; a patient booked into Wyecross stays on the list of the hospital "
           "that added them."),
         Paragraph("2. Sessions", H2),
         _table([["", "Before opening (sessions a week)", "From 11 January 2027 (sessions a week)"],
                 ["Marlstead main theatres, general surgery elective", "14", "14"],
                 ["Fennick main theatres, general surgery elective", "10", "6"],
                 ["Wyecross Elective Centre, general surgery", "", "22"],
                 ["Marlstead weekend lists (independent sector staff)", "4 (2025/26 only)", "none"]], [80, 45, 45]),
         Paragraph("3. Planned admitted waiting list, general surgery, both hospitals", H2),
         P("Patients waiting at each month end, both hospitals together, as planned by the Planned Care Programme Board."),
         _table(t1, [36] + [16] * (half - 1)), Spacer(1, 4), _table(t2, [36] + [16] * (len(head) - half)),
         P("The Trust expects no general surgery patient to wait 52 weeks or more from referral by 30 June 2027."),
         Paragraph("4. Workforce", H2),
         P("Two consultant general surgeons (upper gastrointestinal and abdominal wall) and a theatre team of 31 whole-time "
           "equivalents are appointed for Wyecross from November 2026; the anaesthetic rota is shared with Fennick Hospital.")]
    _pdf(os.path.join(out, "elective_capacity_plan_2027_28_general_surgery.pdf"), "Elective Capacity Plan 2027/28: General Surgery",
         "Planned Care Programme Board", s)


def access(out):
    P = lambda t: Paragraph(t, BODY)
    s = [Paragraph("Elective Access Policy", H1),
         P("Version 6.0, approved by the Trust Board on 26 June 2025, review date June 2027."),
         Paragraph("1. Purpose", H2),
         P("This policy sets out how the Trust manages patients waiting for elective care at Marlstead General Hospital and "
           "Fennick Hospital, so that patients are treated fairly and in turn, and so that the Trust's waiting lists are accurate."),
         Paragraph("2. Clinical priority", H2),
         P("A consultant gives every patient added to the admitted waiting list a clinical priority: P1 within 72 hours, P2 within "
           "one month, P3 within three months and P4 longer than three months. Patients are booked in priority order and, within a "
           "priority, in the order they were added to the list. Priorities are reviewed at clinic or by the consultant's team."),
         Paragraph("3. Reasonable offers", H2),
         P("Patients are offered two dates with at least three weeks' notice. A patient who declines both stays on the list and is "
           "reviewed by the consultant. A patient who does not attend a date without notice is reviewed by the consultant and may be "
           "returned to the care of their GP."),
         Paragraph("4. Cancellations", H2),
         P("Where the Trust cancels a patient's operation on the day of admission or after admission for non-clinical reasons, the "
           "patient is offered another date within 28 days of the cancellation."),
         Paragraph("5. Validation", H2),
         P("Each list is validated at least every twelve weeks. Patients who no longer need or want their operation, who have moved "
           "away or who have been treated elsewhere are removed once this is confirmed with the patient and the GP."),
         Paragraph("6. Transfers between hospitals", H2),
         P("To shorten waits, patients may be offered treatment at the Trust's other hospital or at a provider working under contract "
           "to the Trust. A patient who accepts moves to the receiving hospital's list and waits there for their operation.")]
    _pdf(os.path.join(out, "elective_access_policy_v6.pdf"), "Elective Access Policy", "Planned Care", s)


def write_all(out, S):
    definitions(out)
    capacity(out, S["traj"])
    access(out)
