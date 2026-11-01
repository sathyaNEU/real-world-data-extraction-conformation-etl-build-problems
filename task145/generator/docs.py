"""task145 architecture 2: the network's documents (the board's Bridge policy, the attendance policy, the provider's
contract schedule, the bell schedules), the director of student services' request, and three files the solution never
reads (the family-texting log, the transportation routes, the school climate survey summary)."""
import csv
import datetime as dt
import os

import numpy as np
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import pack as PK
import params as P

DOMAIN = "cedarprairie.org"
DIRECTOR = ("Monica Shaffer", "mshaffer")       # director of student services
CFO = ("Terry Dixon", "tdixon")                 # chief financial officer
ATTEND = ("Patricia Villarreal", "pvillarreal")  # network attendance coordinator


def _styles():
    ss = getSampleStyleSheet()
    body = ParagraphStyle("b", parent=ss["Normal"], fontName="Helvetica", fontSize=9.8, leading=13.6, spaceAfter=5)
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=14, leading=18, spaceAfter=4)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=10.6, leading=14,
                        spaceBefore=8, spaceAfter=3, keepWithNext=1)
    small = ParagraphStyle("s", parent=body, fontSize=8.2, leading=10.6, textColor=colors.HexColor("#444444"))
    cell = ParagraphStyle("c", fontName="Helvetica", fontSize=8.6, leading=10.6)
    return body, h1, h2, small, cell


def _grid(rows, widths, cell):
    t = Table([[Paragraph(str(c), cell) for c in r] for r in rows], colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#8D98A7")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E6EBF1"))]))
    return t


def _footer(text):
    def foot(canvas, d):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.6)
        canvas.setFillColor(colors.HexColor("#555555"))
        canvas.drawString(0.8 * inch, 0.55 * inch, text)
        canvas.drawRightString(letter[0] - 0.8 * inch, 0.55 * inch, "Page %d" % d.page)
        canvas.restoreState()
    return foot


def _doc(path, title, author, subject):
    return SimpleDocTemplate(path, pagesize=letter, leftMargin=0.8 * inch, rightMargin=0.8 * inch,
                             topMargin=0.75 * inch, bottomMargin=0.8 * inch, title=title, author=author,
                             creator=author, subject=subject, invariant=1)


def bridge_policy(path):
    body, h1, h2, small, cell = _styles()
    doc = _doc(path, "Board Policy JF-7 Bridge Program", P.ORG + " Board of Directors", "Board policy")
    s = [Paragraph("%s, Board of Directors" % P.ORG, small),
         Paragraph("Board Policy JF-7: Bridge Program", h1),
         Paragraph("Adopted 14 March 2024; amended 11 June 2025. Administered by the Director of Student Services.",
                   small), Spacer(1, 4)]
    sec = [
        ("1. Purpose", "Bridge is the network's credit-recovery and mentoring program for students at risk of leaving "
                       "school before they finish. It is delivered by a contracted provider under a seat contract for "
                       "each spring semester."),
        ("2. Who Bridge is sized for", "Bridge is sized each spring semester for the students enrolled at any of the "
                                       "network's high schools on the first instructional day of that semester who are "
                                       "expected to leave the network without completing by 30 June of the same "
                                       "year."),
        ("3. Leaving without completing", "A student leaves without completing when they withdraw from the network "
                                          "and their withdrawal is recorded as a dropout, as leaving to enter a high "
                                          "school equivalency program, or as an expulsion. A withdrawal recorded as a "
                                          "transfer for which no other school has requested the student's records "
                                          "within 45 days of the withdrawal also counts. A move from one of the "
                                          "network's schools to another is not a withdrawal from the network."),
        ("4. The seat contract", "In December the Board funds the smallest tier of the provider's spring seat schedule "
                                 "whose seats are at least the number of students expected under section 2. Seats are "
                                 "not added after the contract is signed."),
        ("5. Review", "The Director of Student Services brings the expected number and the tier to the December "
                      "meeting with the network's attendance and enrolment records for the closing fall semester."),
    ]
    for head, para in sec:
        s.append(Paragraph(head, h2))
        s.append(Paragraph(para, body))
    doc.build(s, onFirstPage=_footer("Policy JF-7  |  " + P.ORG), onLaterPages=_footer("Policy JF-7  |  " + P.ORG))


def attendance_policy(path):
    body, h1, h2, small, cell = _styles()
    doc = _doc(path, "Administrative Regulation JH-R Attendance 2026-27", P.ORG, "Administrative regulation")
    s = [Paragraph("%s, Office of Student Services" % P.ORG, small),
         Paragraph("Administrative Regulation JH-R: Student Attendance, 2026-27", h1),
         Paragraph("Issued 28 July 2026. Supersedes JH-R 2025-26. Sections 1, 2, 3 and 5 are unchanged since 2023-24; "
                   "section 4 is new.", small), Spacer(1, 4)]
    sec = [
        ("1. Absent for the day", "A student who misses half or more of a day's instructional minutes, as the school's "
                                  "bell schedule sets them, is absent for the day. A student who misses less than half "
                                  "is present that day. A student on a school-sponsored activity is present."),
        ("2. Suspensions", "Each instructional day of an out-of-school suspension is a day absent. A suspension runs "
                           "on the school's instructional days from its start date for the number of days the "
                           "suspension carries."),
        ("3. Chronic absence", "A student is chronically absent at a school in a semester when they are absent on 10 "
                               "per cent or more of the instructional days they are enrolled at that school in the "
                               "semester. A school's chronic absence rate for a grade is the share of its students in "
                               "that grade enrolled ten or more instructional days in the semester who are chronically "
                               "absent there."),
        ("4. Family contact", "From 12 August 2026 the network's family-texting platform sends a text to a student's "
                              "family on each day the student has an unexcused absence, and a second text when the "
                              "student reaches three unexcused absences in a semester. The texts replace the "
                              "end-of-week phone calls made in earlier years."),
        ("5. Records", "Attendance is recorded in the student information system by each school's attendance office. "
                       "Mesa Vista High School records attendance by period; the other schools record the morning and "
                       "afternoon sessions."),
    ]
    for head, para in sec:
        s.append(Paragraph(head, h2))
        s.append(Paragraph(para, body))
    doc.build(s, onFirstPage=_footer("JH-R 2026-27  |  " + P.ORG), onLaterPages=_footer("JH-R 2026-27  |  " + P.ORG))


def bell_schedules(path):
    body, h1, h2, small, cell = _styles()
    doc = _doc(path, "Bell schedules 2026-27", P.ORG, "Bell schedules")
    s = [Paragraph("%s" % P.ORG, small), Paragraph("Bell schedules, 2026-27", h1),
         Paragraph("Instructional minutes by session or period. The schedules have been unchanged since 2023-24.",
                   small), Spacer(1, 6)]
    s.append(Paragraph("Cottonwood Plains Preparatory, Riverbend Academy and Sandhill Collegiate (every day)", h2))
    s.append(_grid([["Session", "Times", "Instructional minutes"],
                    ["Morning", "7:55 to 11:35 (with a 20-minute passing and advisory break)", str(P.AM_MIN)],
                    ["Afternoon", "12:10 to 3:05", str(P.PM_MIN)],
                    ["Day", "", str(P.AM_MIN + P.PM_MIN)]], [1.4 * inch, 3.6 * inch, 1.6 * inch], cell))
    s.append(Spacer(1, 8))
    s.append(Paragraph("Mesa Vista High School, Monday, Tuesday, Thursday and Friday", h2))
    s.append(_grid([["Period", "Instructional minutes"]] + [[n if n != "ADV" else "Advisory", str(m)]
                                                             for n, m in P.MVH_STD] +
                   [["Day", str(sum(m for _, m in P.MVH_STD))]], [2.4 * inch, 2.4 * inch], cell))
    s.append(Spacer(1, 8))
    s.append(Paragraph("Mesa Vista High School, Wednesday block day", h2))
    s.append(_grid([["Block", "Instructional minutes"]] + [[n, str(m)] for n, m in P.MVH_WED] +
                   [["Day", str(sum(m for _, m in P.MVH_WED))]], [2.4 * inch, 2.4 * inch], cell))
    doc.build(s, onFirstPage=_footer("Bell schedules 2026-27"), onLaterPages=_footer("Bell schedules 2026-27"))


def contract_schedule(path):
    body, h1, h2, small, cell = _styles()
    doc = _doc(path, "Bridge spring 2027 seat schedule", "Pathwise Learning Partners", "Seat schedule")
    s = [Paragraph("Pathwise Learning Partners, Denver", small),
         Paragraph("Schedule B: Bridge seats for the spring 2027 semester", h1),
         Paragraph("Attached to the master services agreement with %s. Quoted 2 December 2026, valid to 31 December "
                   "2026." % P.ORG, small), Spacer(1, 6)]
    rows = [["Tier", "Seats", "Semester fee (USD)", "Mentors assigned"]]
    for name, seats, price in P.TIERS:
        rows.append([name, str(seats), "{:,}".format(price), str(int(np.ceil(seats / 25)))])
    s.append(_grid(rows, [1.2 * inch, 1.1 * inch, 1.8 * inch, 1.6 * inch], cell))
    s.append(Spacer(1, 8))
    s.append(Paragraph("A seat serves one student for the semester; a seat vacated by a student who leaves the "
                       "program is not refilled. The tier is fixed at signature for the whole semester, from 5 "
                       "January to 28 May 2027.", body))
    doc.build(s, onFirstPage=_footer("Pathwise Schedule B 2027"), onLaterPages=_footer("Pathwise Schedule B 2027"))


def request(path):
    text = """From: %s <%s@%s>
To: Data and Assessment <data@%s>
Cc: %s <%s@%s>
Date: Mon, 21 Dec 2026 08:42:17 -0700
Subject: Bridge seats for spring
Message-ID: <20261221084217.6620.mshaffer@%s>
MIME-Version: 1.0
Content-Type: text/plain; charset="utf-8"
Content-Transfer-Encoding: 8bit

Good morning,

The fall semester closed on Friday and the student information system
export came through this morning, so the Bridge numbers can go ahead. The
board meets on the 29th and Terry needs the tier before then so the
Pathwise schedule can be signed by the 31st.

Patricia's attendance workbook goes in the same packet as the board paper,
as it does every December.

Thanks,
Monica

--
%s
Director of Student Services
%s
""" % (DIRECTOR[0], DIRECTOR[1], DOMAIN, DOMAIN, CFO[0], CFO[1], DOMAIN, DOMAIN, DIRECTOR[0], P.ORG)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


def distractors(W, target, rng):
    """The family-texting log (fall 2026), the transportation routes and the school climate survey summary."""
    rows = []
    rec = {}
    for r in W["enrol_rows"] if "enrol_rows" in W else []:
        pass
    cur = W["years"][P.CUR]
    seqn = 880000
    for sid in sorted(cur):
        r = cur[sid]
        recs = W["recmap"][(P.CUR, sid)]
        fam = "fam-%06d" % (int(sid[-6:]) * 7 % 999983)
        for d, (por, code) in sorted(r["fall_ab"].items()):
            if code != "UX":
                continue
            rc = recs[-1]
            for x in recs:
                if x["start"] <= d and (x["end"] is None or d <= x["end"]):
                    rc = x
            seqn += int(rng.integers(1, 5))
            t = PK.utc(dt.datetime.combine(d, dt.time(16, 30)) + dt.timedelta(minutes=int(rng.integers(0, 50))))
            st = "delivered" if rng.random() < 0.93 else ("undeliverable" if rng.random() < 0.6 else "opted_out")
            rows.append(["MSG%07d" % seqn, t.strftime("%Y-%m-%dT%H:%M:%SZ"), P.SCHOOL_NO[rc["school"]], rc["lid"], fam,
                         "UNEXCUSED_ABSENCE", st])
    rows.sort(key=lambda x: (x[1], x[0]))
    _csv(os.path.join(target, "family_texts_fall_2026.csv"),
         ["message_id", "sent_utc", "school_number", "local_id", "family_contact", "template", "status"], rows)
    rt = []
    for s in P.SCHOOLS:
        for k in range(1, 7 + int(rng.integers(0, 3))):
            for j in range(1, 9 + int(rng.integers(0, 6))):
                rt.append([P.SCHOOL_NO[s], "%s-%02d" % (s, k), j, "Stop %d" % (100 + 7 * j + k),
                           "%02d:%02d" % (6 + (j * 4) // 60, (j * 4) % 60 + 10 if (j * 4) % 60 < 50 else 5),
                           int(rng.integers(3, 21))])
    _csv(os.path.join(target, "transportation_routes_2026-27.csv"),
         ["school_number", "route", "stop_seq", "stop_name", "am_pickup", "riders_assigned"], rt)
    import openpyxl
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Results"
    ws.append(["School climate survey, spring 2026: share of students agreeing"])
    ws.append([])
    ws.append(["School", "Responses", "I feel I belong at this school", "Adults here care about me",
               "I feel safe at school", "My classes are interesting"])
    for s in P.SCHOOLS:
        ws.append([P.SCHOOL_NAME[s], int(rng.integers(320, 560))] +
                  [round(float(rng.uniform(0.48, 0.81)), 2) for _ in range(4)])
    wb.save(os.path.join(target, "school_climate_survey_spring_2026.xlsx"))


CODES = [
    ("entry", "C", "Continuing from the previous school year at the same school", "2024-07-01", ""),
    ("entry", "E1", "First entry to the network", "2024-07-01", ""),
    ("entry", "E2", "Re-entry after a withdrawal", "2024-07-01", ""),
    ("entry", "E3", "Entry from another of the network's schools", "2024-07-01", ""),
    ("exit", "GR", "Graduated with a regular diploma", "2024-07-01", ""),
    ("exit", "DO", "Dropped out", "2024-07-01", ""),
    ("exit", "GE", "Withdrew to enter a high school equivalency program", "2024-07-01", ""),
    ("exit", "EX", "Expelled", "2024-07-01", ""),
    ("exit", "TN", "Moved to another of the network's schools", "2024-07-01", ""),
    ("exit", "TI", "Transferred to a school in Colorado outside the network", "2024-07-01", ""),
    ("exit", "TO", "Transferred to a school outside Colorado", "2024-07-01", ""),
    ("exit", "TU", "Transfer reported by the family, receiving school not yet confirmed", "2024-07-01", ""),
    ("exit", "W0", "Graduated", "2016-07-01", "2024-06-30"),
    ("exit", "W1", "Transferred to another school in Colorado", "2016-07-01", "2024-06-30"),
    ("exit", "W2", "Transferred to a school outside Colorado", "2016-07-01", "2024-06-30"),
    ("exit", "W3", "Dropped out", "2016-07-01", "2024-06-30"),
    ("exit", "W5", "Withdrew to a high school equivalency program", "2016-07-01", "2024-06-30"),
    ("exit", "W9", "Expelled", "2016-07-01", "2024-06-30"),
    ("exit", "WT", "Transfer, receiving school unconfirmed", "2016-07-01", "2024-06-30"),
    ("attendance", "EX", "Excused absence", "2024-07-01", ""),
    ("attendance", "UX", "Unexcused absence", "2024-07-01", ""),
    ("attendance", "MED", "Medical absence (note on file)", "2024-07-01", ""),
    ("attendance", "SUS", "Out-of-school suspension", "2024-07-01", ""),
    ("attendance", "ACT", "School-sponsored activity", "2024-07-01", ""),
    ("portion", "FULL", "Whole day", "2024-07-01", ""),
    ("portion", "AM", "Morning session", "2024-07-01", ""),
    ("portion", "PM", "Afternoon session", "2024-07-01", ""),
    ("portion", "PER:", "The periods or blocks listed (Mesa Vista High School)", "2024-07-01", ""),
]


def code_reference(path):
    _csv(path, ["code_table", "code", "description", "valid_from", "valid_to"], CODES)


def _csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\r\n")
        w.writerow(header)
        for r in rows:
            w.writerow(r)


def write_all(W, target):
    rng = np.random.default_rng(P.SEED + 31)
    bridge_policy(os.path.join(target, "board_policy_JF-7_bridge_program.pdf"))
    attendance_policy(os.path.join(target, "attendance_regulation_JH-R_2026-27.pdf"))
    bell_schedules(os.path.join(target, "bell_schedules_2026-27.pdf"))
    contract_schedule(os.path.join(target, "pathwise_schedule_B_spring_2027.pdf"))
    request(os.path.join(target, "bridge_seats_for_spring.eml"))
    code_reference(os.path.join(target, "sis_code_reference.csv"))
    distractors(W, target, rng)
