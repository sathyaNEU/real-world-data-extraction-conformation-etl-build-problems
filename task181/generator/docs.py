"""The pack's documents: PR-07 (the unit's pertussis response protocol), the line-list field notes, the
state system's extract run report, and the unit's weekly communicable diseases report for week 35."""
import csv
import datetime as dt
import hashlib
from collections import Counter, defaultdict

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                           # noqa: E402
from reportlab.lib.enums import TA_LEFT                                    # noqa: E402
from reportlab.lib.pagesizes import A4                                     # noqa: E402
from reportlab.lib.styles import ParagraphStyle                            # noqa: E402
from reportlab.lib.units import mm                                         # noqa: E402
from reportlab.platypus import (KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table,  # noqa: E402
                                TableStyle)

import postprocess as PP
import world as W

PROTOCOL = "PR-07_pertussis_response_protocol.pdf"
NOTES = "pertussis_line_list_notes.md"
RUN_REPORT = "SIPHU_PERTUSSIS_LINELIST_job_20261005_0700.txt"
BULLETIN = "cd_weekly_report_2026_wk35.pdf"

INK = colors.HexColor("#1d2733")
RULE = colors.HexColor("#7d8a99")
BODY = ParagraphStyle("body", fontName="Helvetica", fontSize=9.4, leading=12.6, textColor=INK, spaceAfter=4.5)
CLAUSE = ParagraphStyle("clause", parent=BODY, leftIndent=26, firstLineIndent=-26)
H1 = ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=15, leading=19, textColor=INK, spaceAfter=3)
H2 = ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=10.6, leading=14, textColor=INK, spaceBefore=8, spaceAfter=3)
SMALL = ParagraphStyle("small", parent=BODY, fontSize=7.8, leading=10, textColor=colors.HexColor("#4a5563"))
CELL = ParagraphStyle("cell", parent=BODY, fontSize=8.4, leading=10.4, spaceAfter=0)
CELLB = ParagraphStyle("cellb", parent=CELL, fontName="Helvetica-Bold")


def _frame(title, ref, issued):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.6)
        canvas.setFillColor(colors.HexColor("#4a5563"))
        canvas.drawString(18 * mm, A4[1] - 12 * mm, W.UNIT)
        canvas.drawRightString(A4[0] - 18 * mm, A4[1] - 12 * mm, ref)
        canvas.setStrokeColor(RULE)
        canvas.setLineWidth(0.4)
        canvas.line(18 * mm, A4[1] - 13.6 * mm, A4[0] - 18 * mm, A4[1] - 13.6 * mm)
        canvas.drawString(18 * mm, 11 * mm, "%s  |  %s" % (title, issued))
        canvas.drawRightString(A4[0] - 18 * mm, 11 * mm, "Page %d" % doc.page)
        canvas.restoreState()
    return draw


def _doc(path, title, author, subject):
    return SimpleDocTemplate(path, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=20 * mm,
                             bottomMargin=18 * mm, title=title, author=author, subject=subject,
                             creator=W.UNIT, producer="SIPHU document control")


def _table(rows, widths, header=True, align_right=()):
    data = [[Paragraph(str(c), CELLB if (header and i == 0) else CELL) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths, hAlign="LEFT")
    st = [("LINEBELOW", (0, 0), (-1, 0), 0.6, RULE), ("LINEBELOW", (0, -1), (-1, -1), 0.4, RULE),
          ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 2.2),
          ("BOTTOMPADDING", (0, 0), (-1, -1), 2.2), ("LEFTPADDING", (0, 0), (-1, -1), 3)]
    for c in align_right:
        st.append(("ALIGN", (c, 0), (c, -1), "RIGHT"))
    t.setStyle(TableStyle(st))
    return t


# ------------------------------------------------------------------ PR-07

PR07 = [
    ("1", "Purpose and scope", [
        ("1.1", "This protocol sets how the Southern Inland Public Health Unit responds to pertussis notifications: case "
                "follow-up, where the outbreak response team works, school clusters and infant cases."),
        ("1.2", "It covers residents of the unit's ten local government areas: Wagga Wagga, Griffith, Leeton, Narrandera, "
                "Murrumbidgee, Hay, Edward River, Junee, Cootamundra-Gundagai and Snowy Valleys. A notification for a "
                "person living elsewhere is referred to the public health unit for that person's area and is not counted "
                "under this protocol."),
    ]),
    ("2", "Case definition", [
        ("2.1", "A confirmed case has laboratory definitive evidence: <i>Bordetella pertussis</i> detected by nucleic acid "
                "testing (PCR) or isolated by culture."),
        ("2.2", "A probable case has laboratory suggestive evidence (<i>B. pertussis</i> IgA antibody detected) and clinical "
                "evidence, or clinical evidence and an epidemiological link to a confirmed case."),
        ("2.3", "From 1 July 2024 a case whose only laboratory evidence is serology is probable; before that date the state "
                "case definition counted it as confirmed. The case status on a notification is the status assigned when "
                "the notification was received."),
        ("2.4", "Counts under this protocol include confirmed and probable cases."),
    ]),
    ("3", "Notifications and cases", [
        ("3.1", "Laboratories notify the state notifiable conditions system, and the unit's line-list extract holds one row "
                "per laboratory notification. A person tested by two laboratories, or tested again, is notified more than "
                "once."),
        ("3.2", "Where a case's onset date is not recorded, epidemic curves take it as the specimen collection date less "
                "10 days."),
        ("3.3", "Notifications for the same person with specimens collected within 90 days of the first specimen of an "
                "episode belong to that episode and are one case. The case is confirmed if any of its notifications is "
                "confirmed. A specimen collected more than 90 days after the episode's first specimen begins a new case."),
        ("3.4", "A case's area is the local government area of its residential postcode, through the unit's postcode "
                "lookup. Where a postcode is split between areas, the case is allocated to the area holding the larger "
                "share of the postcode's population."),
        ("3.5", "Every count under this protocol dates a case by the collection date of its first specimen."),
    ]),
    ("4", "Deploying the outbreak response team", [
        ("4.1", "The outbreak response team works in one area each week. The area is set at the Monday huddle from the "
                "line-list extract run at 07:00 that morning."),
        ("4.2", "The team goes to the area with the largest excess of cases with specimens collected in the 14 days before "
                "the extract day over its expected count."),
        ("4.3", "An area's expected count is the mean, over the previous five years, of its cases with specimens collected "
                "on the same 14 calendar dates."),
        ("4.4", "The team leader confirms travel, clinic sessions and school visits with the area's council, general "
                "practices and principals by the Tuesday of the deployment week."),
    ]),
    ("5", "School clusters", [
        ("5.1", "A school cluster is two or more cases among the students of one school with specimens collected in the 30 "
                "days before the extract day. A student is a case recorded at interview as a student of that school. The "
                "huddle slide lists the clusters in the area the team goes to, each with the school and its number of "
                "cases; they are the team's school visits that week (4.4)."),
        ("5.2", "For each cluster the unit sends the school the pertussis information letter, asks for the class "
                "rosters and reviews the vaccination records of the cases' classmates."),
    ]),
    ("6", "Infants", [
        ("6.1", "An infant case is a case aged under six months on the collection date of its first specimen."),
        ("6.2", "An infant case was admitted to hospital when the respiratory admissions extract holds an admission for the "
                "infant, matched on medical record number, that began within 14 days before or after that collection date."),
        ("6.3", "An infant case was born to a vaccinated mother when the antenatal vaccination register records a "
                "pertussis-containing vaccine (dTpa) given to the mother during that pregnancy at least 14 days before the "
                "birth. Infants are linked to their mothers through the birth record."),
    ]),
    ("7", "Reporting", [
        ("7.1", "The quarterly report gives, for each area, the period's confirmed cases, probable cases, infant cases, "
                "infant cases admitted to hospital and infant cases born to a vaccinated mother."),
    ]),
]


def write_protocol(path):
    title = "PR-07 Pertussis response protocol"
    doc = _doc(path, title, W.PEOPLE["director"], "Pertussis response protocol, version 3.1")
    s = [Paragraph(title, H1),
         Paragraph("%s, %s" % (W.UNIT, W.LHD), SMALL), Spacer(1, 5),
         _table([["Version", "Effective", "Owner", "Approved", "Next review"],
                 ["3.1", "02/03/2026", "Director, %s" % W.UNIT, "Director, %s (%s)" % (W.UNIT, W.PEOPLE["director"]), "March 2028"]],
                [16 * mm, 21 * mm, 50 * mm, 58 * mm, 24 * mm]),
         Spacer(1, 8)]
    for num, head, clauses in PR07:
        block = [Paragraph("%s  %s" % (num, head), H2)]
        for cl, text in clauses:
            block.append(Paragraph("<b>%s</b>&nbsp;&nbsp;%s" % (cl, text), CLAUSE))
        s.append(KeepTogether(block))
    s += [Spacer(1, 8), Paragraph("Document history", H2),
          _table([["Version", "Date", "Change"],
                  ["3.1", "02/03/2026", "School clusters (section 5) and the huddle slide; team leader confirmations (4.4)"],
                  ["3.0", "18/11/2024", "Expected count over the previous five years (4.3); split postcodes (3.4)"],
                  ["2.2", "01/07/2024", "State case definition revision: serology-only cases probable (2.3)"],
                  ["2.0", "14/02/2022", "Infant section (6) and quarterly reporting (7)"]],
                 [16 * mm, 21 * mm, 132 * mm]),
          Spacer(1, 6),
          Paragraph("Distribution: outbreak response team; surveillance; immunisation; public health nursing. Printed "
                    "copies are uncontrolled; the current version is on the unit's shared drive.", SMALL)]
    doc.build(s, onFirstPage=_frame(title, "PR-07 v3.1", "Effective 02/03/2026"),
              onLaterPages=_frame(title, "PR-07 v3.1", "Effective 02/03/2026"))
    PP.normalize_pdf(path, b"D:20260302093000+11'00'")


# ------------------------------------------------------------------ the line-list notes

def write_notes(path):
    text = """# Pertussis line list: field notes

Southern Inland Public Health Unit, surveillance. Maintained by Tiffany Peters. Last revised 01/09/2026.

The daily extract `pertussis_notifications_2019-2026.csv` comes from the state notifiable conditions system. It holds
every pertussis notification the system has attributed to the unit since 1 January 2019, one row per laboratory
notification, as at the time the extract runs. Rows are in order of `notification_id`.

| Field | Meaning |
|---|---|
| `notification_id` | State system notification number. Numbers are issued across all conditions and units, so they are not consecutive here. |
| `received_utc` | Date and time the state system received the notification, in UTC (ISO 8601, `Z`). |
| `condition` | Always `Pertussis` in this extract. |
| `person_id` | State system person identifier. A person keeps the same identifier on every notification. |
| `sex`, `dob` | As recorded on the laboratory request. |
| `postcode` | Residential postcode on the laboratory request or as corrected at interview. |
| `specimen_date` | Date the specimen was collected (local date). |
| `onset_date` | Date of cough onset given at interview. Blank where the case was not interviewed or could not say. |
| `notifying_lab` | Laboratory that sent the notification: `Wagga Wagga Hospital Laboratory` (the district's hospital pathology service) or `Inland Pathology` (private collection network). |
| `test` | `PCR`, `Culture` or `Serology (IgA)`. |
| `result` | Result text as notified. |
| `case_status` | `Confirmed` or `Probable`, as assigned when the notification was received. |
| `mrn` | Medical record number at a Southern Inland LHD facility, eight digits, recorded at follow-up. Blank where the person has none on file. |
| `school_or_childcare` | School, preschool or childcare service the case attends or works at, as written at interview. |
| `school_role` | `Student`, `Staff` or `Parent or carer`, as ticked at interview. |

`school_or_childcare` and `school_role` were added to the case interview form on 1 September 2026 and are blank on
earlier interviews.

Linked files used in follow-up:

- `respiratory_admissions_2019-2026.csv`: inpatient episodes with a principal respiratory diagnosis at the district's
  hospitals, from the patient administration system. `mrn` is the PAS medical record number (numeric). Dates are
  dd/mm/yyyy.
- `birth_records_2024-2026.csv`: births at the district's maternity units. `baby_mrn` is the infant's medical record
  number; `mother_medicare_no` is the mother's Medicare card number followed by her individual reference number.
- `antenatal_vaccinations_2019-2026.parquet`: vaccines recorded in pregnancy for women in the district, from the
  antenatal vaccination register. `medicare_card` and `irn` identify the mother; `antigen` is the vaccine's antigen
  group (`dTpa` is the pertussis-containing vaccine); `estimated_due_date` is the due date of the pregnancy the dose was
  given in.
- `school_rosters_term3_2026.xlsx`: enrolment rosters received from schools during follow-up this term, one sheet per
  school, names removed. The school's name at the top of each sheet is as the school writes it.
- `postcode_lga_concordance.xlsx`: the unit's postcode lookup and area populations.
"""
    with open(path, "w", newline="\n") as fh:
        fh.write(text)


# ------------------------------------------------------------------ the extract run report

def write_run_report(path, ll_path, n_rows, n_cols):
    digest = hashlib.sha256(open(ll_path, "rb").read()).hexdigest()
    size = len(open(ll_path, "rb").read())
    text = (
        "STATE NOTIFIABLE CONDITIONS SYSTEM   SCHEDULED EXTRACT RUN REPORT\r\n"
        "================================================================\r\n"
        "Job              SIPHU_PERTUSSIS_LINELIST  (daily, 07:00 Australia/Sydney)\r\n"
        "Requested for    Southern Inland Public Health Unit\r\n"
        "Job owner        Cassandra Dawson (data officer)\r\n"
        "Run started      2026-10-05 07:00:02 AEDT   (2026-10-04T20:00:02Z)\r\n"
        "Run finished     2026-10-05 07:00:38 AEDT   (2026-10-04T20:00:38Z)\r\n"
        "Status           COMPLETED\r\n"
        "\r\n"
        "Parameters\r\n"
        "  condition         Pertussis\r\n"
        "  attributed unit   Southern Inland PHU\r\n"
        "  received from     2019-01-01T00:00:00Z\r\n"
        "  received to       run start\r\n"
        "  grain             one row per notification\r\n"
        "  time zone         received_utc in UTC; specimen, onset and birth dates as recorded\r\n"
        "\r\n"
        "Output\r\n"
        "  file              %s\r\n"
        "  rows              %d\r\n"
        "  columns           %d\r\n"
        "  bytes             %d\r\n"
        "  sha256            %s\r\n"
        "\r\n"
        "Notes\r\n"
        "  Clocks moved to daylight time at 02:00 on Sunday 4 October 2026 (UTC+11 from then).\r\n"
        "  Monday 5 October 2026 is a public holiday in New South Wales (Labour Day); the job runs every day.\r\n"
        % (ll_path.rsplit("/", 1)[-1], n_rows, n_cols, size, digest))
    with open(path, "w", newline="") as fh:
        fh.write(text)
    return digest


# ------------------------------------------------------------------ the weekly report (week 35)

WK = (dt.date(2026, 8, 24), dt.date(2026, 8, 30))


def _read(path):
    with open(path, newline="") as fh:
        return list(csv.DictReader(fh))


def _local_day(stamp):
    t = dt.datetime.strptime(stamp, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=W.UTC)
    return t.astimezone(W.SYD).date()


def bulletin_figures(ll_path, flu_path):
    """Notifications received by the unit, by local date received, for residents of the ten areas."""
    pert = [r for r in _read(ll_path) if W.allocate(r["postcode"])]
    flu = [r for r in _read(flu_path) if W.allocate(r["postcode"])]
    f = {}
    for name, rows in (("Pertussis", pert), ("Influenza", flu)):
        days = [(_local_day(r["received_utc"]), r) for r in rows]
        f[name] = dict(
            week=sum(1 for d, _ in days if WK[0] <= d <= WK[1]),
            four=sum(1 for d, _ in days if WK[1] - dt.timedelta(days=27) <= d <= WK[1]),
            ytd=sum(1 for d, _ in days if dt.date(2026, 1, 1) <= d <= WK[1]),
            ytd_last=sum(1 for d, _ in days if dt.date(2025, 1, 1) <= d <= dt.date(2025, 8, 31)),
            by_area=Counter(W.allocate(r["postcode"]) for d, r in days if WK[1] - dt.timedelta(days=27) <= d <= WK[1]),
            ytd_area=Counter(W.allocate(r["postcode"]) for d, r in days if dt.date(2026, 1, 1) <= d <= WK[1]),
            weekly=[sum(1 for d, _ in days if WK[0] - dt.timedelta(days=7 * k) <= d <= WK[1] - dt.timedelta(days=7 * k))
                    for k in range(7, -1, -1)])
        sub = Counter(r["result"].split(" RNA")[0].replace("Influenza ", "") for d, r in days
                      if dt.date(2026, 1, 1) <= d <= WK[1] and "subtyped" not in r["result"] and "B virus" not in r["result"]
                      and "A virus" not in r["result"])
        f[name]["top_subtype"] = sub.most_common(1)[0][0] if sub else ""
    return f


def write_bulletin(path, ll_path, flu_path):
    f = bulletin_figures(ll_path, flu_path)
    title = "Communicable diseases weekly report, week 35"
    doc = _doc(path, title, W.PEOPLE["epidemiologist"], "Week 35, 24 to 30 August 2026")
    p, fl = f["Pertussis"], f["Influenza"]
    weeks = [WK[1] - dt.timedelta(days=7 * k) for k in range(7, -1, -1)]
    s = [Paragraph("Communicable diseases weekly report", H1),
         Paragraph("Week 35: notifications received 24 to 30 August 2026. Issued Tuesday 1 September 2026. "
                   "Prepared by %s, surveillance." % W.PEOPLE["epidemiologist"], SMALL),
         Spacer(1, 6),
         Paragraph("Summary", H2),
         Paragraph("The unit received %d pertussis notifications for residents this week and %d in the four weeks to 30 "
                   "August, against %d in the four weeks before that. Wagga Wagga residents account for %d of the four "
                   "weeks' notifications. Influenza notifications have fallen from %d in the week ending %s to %d this week."
                   % (p["week"], p["four"], sum(p["weekly"][0:4]), p["by_area"].get("Wagga Wagga", 0),
                      max(fl["weekly"]), weeks[fl["weekly"].index(max(fl["weekly"]))].strftime("%d %B").lstrip("0"),
                      fl["week"]), BODY),
         Paragraph("The vaccination reminder for pregnant women and for infants due their six-week, four-month and "
                   "six-month doses goes to general practices this week.", BODY),
         Paragraph("Notifications by week received", H2),
         _table([["Week ending"] + [w.strftime("%d %b") for w in weeks],
                 ["Pertussis"] + [str(x) for x in p["weekly"]],
                 ["Influenza"] + [str(x) for x in fl["weekly"]]],
                [26 * mm] + [17.5 * mm] * 8, align_right=range(1, 9)),
         Paragraph("Residents of the unit's ten local government areas; notifications counted in the week the unit "
                   "received them.", SMALL),
         Paragraph("Pertussis by local government area", H2)]
    rows = [["Local government area", "Last 4 weeks", "Year to date", "Year-to-date rate per 100,000"]]
    for a in W.AREA_NAMES:
        rows.append([a, str(p["by_area"].get(a, 0)), str(p["ytd_area"].get(a, 0)),
                     "%.1f" % (100000.0 * p["ytd_area"].get(a, 0) / W.ERP[a])])
    tot_erp = sum(W.ERP.values())
    rows.append(["Unit total", str(p["four"]), str(p["ytd"]), "%.1f" % (100000.0 * p["ytd"] / tot_erp)])
    s += [_table(rows, [52 * mm, 26 * mm, 26 * mm, 44 * mm], align_right=(1, 2, 3)),
          Paragraph("Rates use the estimated resident population at 30 June 2025. Year to date: 1 January to 30 August 2026; "
                    "the same period of 2025 had %d pertussis notifications for residents." % p["ytd_last"], SMALL),
          Paragraph("Influenza", H2),
          Paragraph("%d influenza notifications this week and %d since 1 January. %s is the most common subtype among "
                    "subtyped specimens this year." % (fl["week"], fl["ytd"], fl["top_subtype"]), BODY),
          Spacer(1, 8),
          Paragraph("Southern Inland Public Health Unit, surveillance. For internal distribution to the unit, the "
                    "district's emergency departments and general practice liaison.", SMALL)]
    doc.build(s, onFirstPage=_frame(title, "Week 35, 2026", "Issued 01/09/2026"),
              onLaterPages=_frame(title, "Week 35, 2026", "Issued 01/09/2026"))
    PP.normalize_pdf(path, b"D:20260901101200+10'00'")
    return f
