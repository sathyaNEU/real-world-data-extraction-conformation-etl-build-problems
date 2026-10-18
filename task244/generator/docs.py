"""task244 documents: the Director's request (eml), the survey's methodology note and the reinterview protocol (pdf), the
published 2027 flows tables (xlsx), the third-quarter labour market bulletin (pdf), the job centres' register (xlsx), the
data dictionary and the readme (md)."""
import os

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

PEOPLE = {"director": ("Atinuke Adebisi", "atinuke.adebisi"),
          "method": ("Comfort Olawale", "comfort.olawale"),
          "field": ("Babasola Oginni", "babasola.oginni"),
          "secretary": ("Ronke Shekoni", "ronke.shekoni")}


def _addr(k):
    name, user = PEOPLE[k]
    return "%s <%s@%s>" % (name, user, P.DOMAIN)


def _styles():
    ss = getSampleStyleSheet()
    body = ParagraphStyle("body", parent=ss["Normal"], fontName="Helvetica", fontSize=9.6, leading=13.4, spaceAfter=5)
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=13.5, leading=17, spaceAfter=4)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=10.5, leading=14,
                        spaceBefore=8, spaceAfter=4, keepWithNext=1)
    small = ParagraphStyle("small", parent=body, fontSize=8, leading=10.5, textColor=colors.HexColor("#444444"))
    cell = ParagraphStyle("cell", fontName="Helvetica", fontSize=8.4, leading=10.2)
    return body, h1, h2, small, cell


def _grid(rows, widths, cell):
    t = Table([[Paragraph(str(c), cell) for c in r] for r in rows], colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9AA0AB")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E3E8EF"))]))
    return t


def _footer(text):
    def foot(canvas, d):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.5)
        canvas.setFillColor(colors.HexColor("#555555"))
        canvas.drawString(20 * mm, 10 * mm, text)
        canvas.drawRightString(A4[0] - 20 * mm, 10 * mm, "Page %d" % d.page)
        canvas.restoreState()
    return foot


def _doc(path, title, author, subject):
    return SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm,
                             bottomMargin=18 * mm, title=title, author=author, creator=author, subject=subject,
                             invariant=1)


def _sections(s, sec, h2, body):
    for title, paras in sec:
        s.append(Paragraph(title, h2))
        for t in paras:
            s.append(Paragraph(t, body))


# ------------------------------------------------------------------ the request (eml)
def request(path, F):
    text = f"""From: {_addr("director")}
To: {_addr("method")}
Cc: {_addr("field")}, {_addr("secretary")}
Date: Wed, 2 Feb 2028 10:41:07 +0100
Subject: 2027 annual flows: quality note for the management meeting
Message-ID: <20280202104107.3318@{P.DOMAIN}>
MIME-Version: 1.0
Content-Type: text/plain; charset="utf-8"
Content-Transfer-Encoding: 7bit

Comfort,

The management meeting on Wednesday 16 February clears the 2027 annual labour market flows tables for release.
Ronke needs the quality note by Friday 11 February so it can go out with the meeting's papers.

As every year, the meeting wants to know whether the tables can go out without the classification-error warning,
and if not, which of the district rates carry it, with the match rate and the reinterview figures the note always
gives. Section 8 of the methodology note has what the note covers.

The tables as tabulated are in the 2027 flows folder with the five quarterly person files, the reinterview results,
Babasola's fieldwork log and the district gazetteer.

Thanks,
Atinuke

--
Atinuke Adebisi
Director, {P.DIVISION}
{P.BUREAU}
"""
    with open(path, "w", newline="\n") as fh:
        fh.write(text)


# ------------------------------------------------------------------ the methodology note (pdf)
def methodology(path, F):
    body, h1, h2, small, cell = _styles()
    doc = _doc(path, "%s: methodology note, 2027 edition" % P.SURVEY, P.BUREAU, "Methodology note")
    s = [Paragraph("%s, %s" % (P.BUREAU, P.DIVISION), small),
         Paragraph("%s (%s): methodology note" % (P.SURVEY, P.SURVEY_SHORT), h1),
         Paragraph("2027 edition, January 2027. Revised in section 6 for the district boundary change of 1 April 2027.",
                   small), Spacer(1, 4)]
    sec = [
        ("1. The survey",
         ["The %s is the bureau's quarterly household survey of the state's labour force. It interviews every person "
          "aged 15 and over in a sample of dwellings in each of the state's twelve survey districts, and publishes "
          "quarterly estimates of employment and unemployment and, once a year, the annual labour market flows tables."
          % P.SURVEY]),
        ("2. Sample and rotation",
         ["Each district's sample is drawn from its enumeration areas, and every district's sample is the same size "
          "(320 dwellings enter it each quarter), so that each district's estimates carry similar precision. A "
          "dwelling stays in the sample for four "
          "consecutive quarters (four visits) and then leaves it; each quarter about a quarter of each district's "
          "dwellings are new to the sample and about a quarter take their fourth and last interview. The visit "
          "number on each record is the dwelling's visit (1 to 4). Every household living in a sampled dwelling at a "
          "visit is interviewed. A household that moves away is not followed; the household found in the dwelling at "
          "the next visit is interviewed in its place under the next household number."]),
        ("3. Fieldwork",
         ["Interviews run over the first eleven weeks of each quarter, Monday to Saturday, on tablets. Household "
          "members absent at the visit are interviewed on a later call where possible, otherwise another adult of "
          "the household answers for them; each record carries the line of the person who answered "
          "(resp_line). The bureau rotates its interviewers between enumeration areas each quarter, so a dwelling is "
          "interviewed by a different interviewer at each visit."]),
        ("4. Labour force status",
         ["Status follows the international standard for the reference week before the interview. A person is "
          "employed who worked for pay or profit for at least one hour in the reference week (q_work) or had a job "
          "from which they were temporarily absent (q_absent). A person not employed is unemployed who looked for "
          "work in the last four weeks (q_look) or has found a job to start within three months (q_future), and is "
          "available to start within two weeks (q_avail). Everyone else is outside the labour force. The derived "
          "status is on each record (lfs_status: 1 employed, 2 unemployed, 3 outside the labour force)."]),
        ("5. Weights",
         ["Each quarter's records carry a cross-sectional weight (wt), the design weight adjusted for household "
          "non-response and calibrated to the bureau's projections of the district's population aged 15 and over by "
          "sex and age group. The flows tables use longitudinal weights, computed for the persons linked across two "
          "quarters and calibrated to the same projections; they are held on the bureau's processing server."]),
        ("6. Districts",
         ["From 1 April 2027 six enumeration areas of the Industrial Corridor (D04) belong to the Metropolitan Fringe "
          "(D02), where they are numbered 17 to 22; the district gazetteer lists each area's code before and after. "
          "Records of interviews before that date carry the codes in force when they were taken. The 2027 release "
          "reports every quarter on the districts as they stand from 1 April 2027."]),
        ("7. Linking persons across quarters and the flows tables",
         ["The flows tables link a person's interviews in two consecutive quarters on the dwelling, household and "
          "person line numbers. The 2027 annual flows tables give, for each district, the average over the year's four "
          "quarter pairs (2026Q4 to 2027Q1, 2027Q1 to 2027Q2, 2027Q2 to 2027Q3 and 2027Q3 to 2027Q4) of the weighted "
          "number of persons in each pair of statuses in the two quarters, rounded to the nearest person. The "
          "job-finding rate is the persons unemployed in the first quarter of a pair and employed in the second, as a "
          "share of the persons unemployed in the first; the job-loss rate is the persons employed in the first and "
          "unemployed in the second, as a share of the persons employed in the first."]),
        ("8. The annual quality note",
         ["Every release of the annual flows tables goes to the bureau's %s (the Statistician-General and the "
          "directors) with a quality note covering the points below." % P.FORUM,
          "8.1 Classification-error warning. A published flow rate carries the classification-error warning when a "
          "third or more of the moves it counts are not real moves: when a third or more of the persons it counts as "
          "moving from the first status in one quarter to the second status in the next did not in fact hold the "
          "first status in the first quarter and the second status in the second. A person's status in a quarter is, "
          "for this purpose, the status the supervisors' reinterview records for that quarter once every difference "
          "has been reconciled with the respondent (reinterview protocol, section 4). The check covers the 24 rates of "
          "the annual tables, each district's job-finding rate and job-loss rate.",
          "8.2 Match rate. For each district, of the persons interviewed in a quarter in a dwelling due another "
          "visit (its first, second or third), the share who were interviewed again at the dwelling's next visit, "
          "over the year's four quarter pairs. A person interviewed again is found in the next visit's records on the "
          "dwelling, household and line numbers or, in a household new to the dwelling, on sex and month and year of "
          "birth. A person counts once in each pair, so the persons the rate is based on are summed over the four "
          "pairs.",
          "8.3 Reinterview timing. For each district, the mean number of days from the date of a person's original "
          "interview to the date of the supervisor's visit that completed the reinterview, over the persons whose "
          "household reinterview was completed, within the window or after it, for the interviews of the year's four "
          "quarters (2027Q1 to 2027Q4)."]),
    ]
    _sections(s, sec, h2, body)
    s.append(Paragraph("Annex: questionnaire items on the person records", h2))
    rows = [["Item", "Question", "Codes"],
            ["q_work", "Last week, did you do any work for pay or profit, for at least one hour?", "1 yes, 2 no"],
            ["q_absent", "Do you have a job or business from which you were temporarily absent last week?",
             "1 yes, 2 no (asked if q_work is 2)"],
            ["q_look", "In the last four weeks, did you look for work or try to start a business?",
             "1 yes, 2 no (asked if not employed)"],
            ["q_future", "Have you found a job or business that you will start within three months?",
             "1 yes, 2 no (asked if q_look is 2)"],
            ["q_avail", "If a job were offered now, could you start within two weeks?",
             "1 yes, 2 no (asked if not employed)"]]
    s.append(_grid(rows, [18 * mm, 104 * mm, 48 * mm], cell))
    foot = "%s: %s methodology note, 2027 edition" % (P.BUREAU, P.SURVEY_SHORT)
    doc.build(s, onFirstPage=_footer(foot), onLaterPages=_footer(foot))
    postprocess.scrub(path, P.BUREAU, "2027-04-14")


# ------------------------------------------------------------------ the reinterview protocol (pdf)
def protocol(path, F):
    body, h1, h2, small, cell = _styles()
    doc = _doc(path, "%s: supervisors' reinterview protocol, version 3" % P.SURVEY_SHORT, P.BUREAU,
               "Reinterview protocol")
    s = [Paragraph("%s, %s" % (P.BUREAU, P.FIELD), small),
         Paragraph("Supervisors' reinterview protocol", h1),
         Paragraph("Version 3, September 2026. Applies from the fourth quarter of 2026.", small), Spacer(1, 4)]
    sec = [
        ("1. Purpose",
         ["The reinterview measures how well the survey's interviews record each person's labour force status. A "
          "field supervisor returns to a sample of the households interviewed each quarter, asks the labour force "
          "questions again for the same reference week, and settles any difference with the respondent."]),
        ("2. Selection",
         ["At the end of each fieldwork week the processing team selects households at random from the week's "
          "completed interviews, one household in about twelve, and assigns them to the district's supervisor. Every "
          "adult interviewed in a selected household is reinterviewed."]),
        ("3. Supervisors",
         ["Each supervisor covers two districts. A supervisor never reinterviews a household whose original "
          "interview they took, and does not see the original answers before the reinterview's own questions are "
          "complete."]),
        ("4. The reinterview visit and reconciliation",
         ["The supervisor visits the household, asks each adult the labour force questions for the original "
          "interview's reference week and records the answers. The tablet then shows the original interview's "
          "status beside the reinterview's; where they differ, the supervisor goes through the questions with the "
          "respondent and records the status they agree is right. The status recorded after that review is the "
          "reconciled status."]),
        ("5. The window",
         ["A reinterview must be completed within 14 days of each person's original interview (the person's own "
          "interview date on the survey record). A supervisor makes up to three calls. Reinterviews completed after "
          "the window are recorded in the fieldwork log but their results are not used."]),
        ("6. Records",
         ["The fieldwork log holds one row for each call on a selected household: the supervisor, the household, "
          "the call number, the call's date as the tablet recorded it, the tablet clock time at which the household's "
          "reinterview form was opened, and the result. The reinterview results file "
          "holds every person reinterviewed within the window: the status the original interview recorded, the "
          "status of the supervisor's own reading before review, and the reconciled status."]),
        ("7. What the reinterview measures",
         ["The reinterview is designed to measure the survey's classification error for the state over a year. Each "
          "annual release uses the reinterviews of every quarter whose interviews enter its tables; for the 2027 "
          "flows these are the reinterviews of the interviews of 2026Q4 to 2027Q4. Each person reinterviewed counts "
          "once; the reinterview carries no weights. The sample is not large enough to measure classification error "
          "for a single district or a single quarter."]),
    ]
    _sections(s, sec, h2, body)
    foot = "%s: %s supervisors' reinterview protocol, version 3" % (P.BUREAU, P.SURVEY_SHORT)
    doc.build(s, onFirstPage=_footer(foot), onLaterPages=_footer(foot))
    postprocess.scrub(path, P.BUREAU, "2026-09-22")


# ------------------------------------------------------------------ the third-quarter bulletin (pdf)
def bulletin(path, F, R):
    body, h1, h2, small, cell = _styles()
    doc = _doc(path, "%s: labour market bulletin, third quarter 2027" % P.SURVEY, P.BUREAU, "Quarterly bulletin")
    rates = R.bulletin_rates("2027Q3")
    s = [Paragraph("%s, %s" % (P.BUREAU, P.DIVISION), small),
         Paragraph("Labour market bulletin: third quarter 2027", h1),
         Paragraph("Released 14 November 2027. Estimates from the %s, persons aged 15 and over." % P.SURVEY, small),
         Paragraph("Headlines", h2),
         Paragraph("The state's unemployment rate was %.1f per cent in the third quarter of 2027, and %.1f per cent "
                   "of persons aged 15 and over were employed. Unemployment remained highest in the metropolitan and "
                   "market districts and in the Industrial Corridor, and lowest in the cocoa belt and the northern "
                   "savanna." % (rates["state"][0], rates["state"][1]), body),
         Paragraph("Unemployment and employment by district", h2)]
    rows = [["District", "Unemployment rate (per cent of the labour force)", "Employment rate (per cent of persons "
             "aged 15 and over)"]]
    for d in P.DCODES:
        rows.append(["%s %s" % (d, P.DNAME[d]), "%.1f" % rates[d][0], "%.1f" % rates[d][1]])
    rows.append(["Esinmi State", "%.1f" % rates["state"][0], "%.1f" % rates["state"][1]])
    s.append(_grid(rows, [58 * mm, 56 * mm, 56 * mm], cell))
    s.append(Paragraph("Estimates use the cross-sectional weights. The unemployment rate is the unemployed as a share "
                       "of the employed and unemployed together. The annual labour market flows tables for 2027 will "
                       "be released in February 2028.", small))
    foot = "%s: labour market bulletin, third quarter 2027" % P.BUREAU
    doc.build(s, onFirstPage=_footer(foot), onLaterPages=_footer(foot))
    postprocess.scrub(path, P.BUREAU, "2027-11-14")


# ------------------------------------------------------------------ workbooks
def _widths(ws, widths):
    for k, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(k)].width = w


def flows_workbook(path, R):
    fl, rates = R.flows_tables()
    wb = Workbook()
    ws = wb.active
    ws.title = "F1 flows"
    ws["A1"] = "%s: labour market flows, 2027" % P.SURVEY
    ws["A1"].font = Font(bold=True)
    ws["A2"] = ("Table F1. Average quarterly flows between labour force statuses, persons aged 15 and over, by "
                "district, 2027")
    ws["A4"], ws["C4"], ws["D4"] = "District", "Status in first quarter", "Status in second quarter"
    head = ["Code", "Name", "", P.STATUS_NAME["E"], P.STATUS_NAME["U"], P.STATUS_NAME["N"], "Total"]
    for j, v in enumerate(head, 1):
        c = ws.cell(row=5, column=j, value=v)
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="DDE3EA")
    for r in (4,):
        for j in range(1, 8):
            ws.cell(row=r, column=j).font = Font(bold=True)
    row = 6
    for d in P.DCODES:
        f = fl[fl.district == d]
        for i, a in enumerate(P.STATUS):
            vals = [int(f[(f.status_q1 == P.STATUS_NAME[a]) & (f.status_q2 == P.STATUS_NAME[b])].persons.iloc[0])
                    for b in P.STATUS]
            if i == 0:
                ws.cell(row=row, column=1, value=d)
                ws.cell(row=row, column=2, value=P.DNAME[d])
            ws.cell(row=row, column=3, value=P.STATUS_NAME[a])
            for j, v in enumerate(vals):
                ws.cell(row=row, column=4 + j, value=v).number_format = "#,##0"
            ws.cell(row=row, column=7, value=sum(vals)).number_format = "#,##0"
            row += 1
    row += 1
    for t in ["Persons interviewed in two consecutive quarters, linked on the dwelling, household and person line "
              "numbers and weighted on the longitudinal weights; the average of the four quarter pairs 2026Q4 to "
              "2027Q1, 2027Q1 to 2027Q2, 2027Q2 to 2027Q3 and 2027Q3 to 2027Q4.",
              "Districts as they stand from 1 April 2027. Rounded to the nearest person."]:
        ws.cell(row=row, column=1, value=t)
        row += 1
    _widths(ws, [8, 22, 26, 14, 14, 24, 12])
    ws2 = wb.create_sheet("F2 rates")
    ws2["A1"] = "Table F2. Job-finding and job-loss rates by district, 2027 (per cent, average quarterly rates)"
    ws2["A1"].font = Font(bold=True)
    head = ["Code", "Name", "Job-finding rate", "Job-loss rate", "Unemployed in first quarter",
            "Employed in first quarter"]
    for j, v in enumerate(head, 1):
        c = ws2.cell(row=3, column=j, value=v)
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="DDE3EA")
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for i, r in enumerate(rates.itertuples(), 4):
        for j, v in enumerate([r.district, r.district_name, r.job_finding, r.job_loss, r.unemployed_start,
                               r.employed_start], 1):
            c = ws2.cell(row=i, column=j, value=v)
            if j in (3, 4):
                c.number_format = "0.0"
            if j in (5, 6):
                c.number_format = "#,##0"
    _widths(ws2, [8, 22, 14, 14, 16, 16])
    wb.save(path)
    postprocess.scrub(path, P.BUREAU, "2028-01-28")
    postprocess.finish_office(path, "2028-01-24T09:12:00Z", "2028-01-28T15:47:00Z", P.BUREAU)


def jobcentre_workbook(path, R):
    df = R.jobcentre()
    wb = Workbook()
    ws = wb.active
    ws.title = "Registered job seekers"
    ws["A1"] = "Esinmi State Ministry of Labour and Productivity: job seekers on the job centres' registers, 2027"
    ws["A1"].font = Font(bold=True)
    ws["A2"] = "Persons registered as seeking work at the end of each month, by the district of the job centre."
    for j, c in enumerate(df.columns, 1):
        cell = ws.cell(row=4, column=j, value=c)
        cell.font = Font(bold=True)
        cell.fill = PatternFill("solid", fgColor="DDE3EA")
    for i, row in enumerate(df.itertuples(index=False), 5):
        for j, v in enumerate(row, 1):
            ws.cell(row=i, column=j, value=v.item() if hasattr(v, "item") else v)
    _widths(ws, [10, 22] + [9] * 12)
    wb.save(path)
    postprocess.scrub(path, "Esinmi State Ministry of Labour and Productivity", "2028-01-09")
    postprocess.finish_office(path, "2028-01-05T08:20:00Z", "2028-01-09T10:02:00Z",
                              "Esinmi State Ministry of Labour and Productivity")


# ------------------------------------------------------------------ the registers
def dictionary(F):
    pfiles = ", ".join(F["persons_" + q.lower()] for q in P.QUARTERS)
    return f"""# Data dictionary

## {pfiles}
The survey's quarterly person files, one per quarter: one row per person aged 15 and over interviewed. quarter;
district and ea (the survey district and enumeration area codes in force on the interview date); dwelling (the sampled
dwelling's number); hh (the household's number in the dwelling); line (the person's line in the household); visit (the
dwelling's visit, 1 to 4); int_date (the person's interview date, yyyy-mm-dd); interviewer; resp_line (the line of the
person who answered); sex (1 male, 2 female); birth_month; birth_year; age (completed years); relation (to the
household head: 1 head, 2 spouse, 3 child, 4 other relative); q_work, q_absent, q_look, q_avail, q_future (the
questionnaire items in the methodology note's annex; blank where not asked); lfs_status (1 employed, 2 unemployed, 3
outside the labour force); wt (the cross-sectional weight).

## {F["reint_results"]}
The supervisors' reinterview results: one row per person reinterviewed within the window. reint_id; quarter (of the
original interview); district and ea (codes in force on the original interview date); dwelling; hh; line; supervisor;
orig_status (the status the original interview recorded: 1 employed, 2 unemployed, 3 outside the labour force);
reint_status (the supervisor's own reading before review, same codes); reconciled (the status agreed with the
respondent after review, same codes); outcome (same: no difference to review; reconciled: a difference reviewed).

## {F["reint_log"]}
The supervisors' fieldwork log: one row per call on a selected household. log_row; supervisor; quarter (of the
original interview); district and ea (codes in force on the original interview date); dwelling; hh; attempt (the call
number); attempt_date (the call's date as the tablet recorded it, yyyy-mm-dd); visit_start (the tablet clock time at
which the household's reinterview form was opened, yyyy-mm-dd hh:mm); result (no contact, refused, completed).

## {F["flows"]}
The 2027 annual flows tables as tabulated: sheet F1 flows (Table F1, persons in each pair of statuses in two
consecutive quarters, by district) and sheet F2 rates (Table F2, job-finding and job-loss rates).

## {F["gazetteer"]}
The survey districts' enumeration areas as they stand from 1 April 2027: district; district_name; ea; and, for the
areas renumbered on that date, district_before, ea_before and effective.

## {F["projections"]}
The bureau's projections of the population aged 15 and over: district, year, sex (1 male, 2 female), age_group,
persons.

## {F["jobcentre"]}
The Ministry of Labour and Productivity's job centre registers, 2027: registered job seekers at the end of each month
by district.

## {F["bulletin"]}
The bureau's labour market bulletin for the third quarter of 2027.
"""


def readme(F):
    pq = "\n".join("- %s: the survey's person file for %s." % (F["persons_" + q.lower()], q) for q in P.QUARTERS)
    return f"""# {P.SURVEY_SHORT} 2027 annual flows

The {P.DIVISION}'s folder for the 2027 annual labour market flows release.

- {F["request"]}: the Director's request for the release's quality note.
- {F["method"]}: the survey's methodology note, 2027 edition.
- {F["protocol"]}: the supervisors' reinterview protocol, version 3.
{pq}
- {F["reint_results"]}: the reinterview results.
- {F["reint_log"]}: the reinterview fieldwork log.
- {F["flows"]}: the 2027 annual flows tables as tabulated.
- {F["gazetteer"]}: the district gazetteer.
- {F["projections"]}: population projections, 2026 to 2028.
- {F["jobcentre"]}: the Ministry of Labour and Productivity's job centre registers, 2027.
- {F["bulletin"]}: the labour market bulletin for the third quarter of 2027.
- DATA_DICTIONARY.md: the fields of each file.
"""


def write_all(target, F, R):
    p = lambda k: os.path.join(target, F[k])
    request(p("request"), F)
    methodology(p("method"), F)
    protocol(p("protocol"), F)
    bulletin(p("bulletin"), F, R)
    flows_workbook(p("flows"), R)
    jobcentre_workbook(p("jobcentre"), R)
    with open(p("dict"), "w") as fh:
        fh.write(dictionary(F))
    with open(p("readme"), "w") as fh:
        fh.write(readme(F))
