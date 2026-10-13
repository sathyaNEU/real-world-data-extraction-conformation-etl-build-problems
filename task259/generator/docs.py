"""The pack's documents: Tarnwick's engineering base pay policy, Tallyband's methodology page for the extract, the
engineering job architecture and the people data team's readme for its exports."""
from __future__ import annotations

from reportlab import rl_config

rl_config.invariant = 1
from openpyxl import Workbook                                                      # noqa: E402
from openpyxl.styles import Alignment, Font, PatternFill                           # noqa: E402
from reportlab.lib import colors                                                   # noqa: E402
from reportlab.lib.pagesizes import LETTER                                         # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                    # noqa: E402
from reportlab.lib.units import inch                                               # noqa: E402
from reportlab.pdfbase import pdfmetrics                                           # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                       # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate                        # noqa: E402

import common as K   # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("Serif", "LiberationSerif-Regular"), ("Serif-B", "LiberationSerif-Bold"),
              ("Sans", "LiberationSans-Regular"), ("Sans-B", "LiberationSans-Bold")):
    pdfmetrics.registerFont(TTFont(nm, FONT_DIR + f + ".ttf"))
INK, GREY, PLUM = colors.HexColor("#1f1d24"), colors.HexColor("#5d5a66"), colors.HexColor("#4b2e5c")
BODY = ParagraphStyle("b", fontName="Serif", fontSize=10.6, leading=14.2, textColor=INK, spaceAfter=5)
CL = ParagraphStyle("c", parent=BODY, leftIndent=26, firstLineIndent=-26)
H1 = ParagraphStyle("h1", fontName="Sans-B", fontSize=15, leading=19, textColor=PLUM, spaceAfter=3)
H2 = ParagraphStyle("h2", fontName="Sans-B", fontSize=10.4, leading=14, textColor=INK, spaceBefore=10, spaceAfter=3)
META = ParagraphStyle("m", fontName="Sans", fontSize=8.4, leading=11.2, textColor=GREY, spaceAfter=12)


def _frame(left, right):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(GREY)
        canvas.setFont("Sans", 7.8)
        canvas.drawString(0.9 * inch, LETTER[1] - 0.55 * inch, left)
        canvas.drawRightString(LETTER[0] - 0.9 * inch, LETTER[1] - 0.55 * inch, right)
        canvas.drawCentredString(LETTER[0] / 2, 0.5 * inch, "%d" % doc.page)
        canvas.restoreState()
    return draw


def write_policy(path):
    head, comp = K.PEOPLE["head"], K.PEOPLE["comp"]
    story = [Paragraph("Engineering base pay policy", H1),
             Paragraph("%s, People. Owner: %s, Head of Total Rewards. Version 2026.2, approved by the executive "
                       "team on 8 September 2026; replaces version 2025.1." % (K.COMPANY, head), META)]
    sections = [
        ("1. Purpose and scope", [
            "1.1 This policy sets how %s prices base pay for its engineering jobs in the United States: the jobs "
            "and levels it prices, the annual refresh of its pay bands and the date refreshed bands take effect."
            % K.COMPANY,
            "1.2 It covers employees in the software, site reliability, data, machine learning and analytics "
            "engineering families. Bonus, equity and allowances are set in the total rewards handbook."]),
        ("2. Jobs and levels", [
            "2.1 Every engineering job and level is defined in the engineering job architecture, with its job code, "
            "its scope and its survey match.",
            "2.2 Each job and level has one pay band, set nationally. Data Engineer has four levels, I to IV."]),
        ("3. Positioning", [
            "3.1 %s pays at the market: the midpoint of a band is the market median for its job and level, and "
            "the band runs from the market's 25th percentile to its 75th." % K.COMPANY,
            "3.2 Pay zones set the share of the national band at which an employee's range is drawn; zone factors are "
            "set in the total rewards handbook and are not part of the band refresh."]),
        ("4. The annual band refresh", [
            "4.1 Base pay is annual base salary, before bonus, equity, allowances and overtime.",
            "4.2 The market for a job and level is every matched respondent of the licensed Tallyband extract: a "
            "respondent located in the United States and working full time, whose job is the %s job under the "
            "job architecture's survey match and whose employer level maps to the %s level in the level "
            "crosswalk. Each matched respondent counts once." % (K.COMPANY, K.COMPANY),
            "4.3 The market is read as in effect on the benchmark date, 1 October 2026: the base pay a job and level "
            "commands on that date.",
            "4.4 A band's 25th percentile, midpoint and 75th percentile are the 25th percentile, median and 75th "
            "percentile of the market's base pay for its job and level, each filed to the nearest $1,000.",
            "4.5 The executive team approves the refreshed bands, which take effect on 1 April 2027. From that date "
            "offers, promotions and the pay ranges published with job postings use them."]),
        ("5. Governance", [
            "5.1 The compensation analytics lead (%s) prepares the refresh; the head of total rewards (%s) "
            "submits it to the executive team with the population each band governs." % (comp, head),
            "5.2 Licensed survey data stay with the total rewards team and are used for internal benchmarking "
            "only, as the licence requires."]),
    ]
    for h, paras in sections:
        story.append(Paragraph(h, H2))
        for p in paras:
            story.append(Paragraph(p, CL))
    doc = SimpleDocTemplate(path, pagesize=LETTER, leftMargin=0.9 * inch, rightMargin=0.9 * inch,
                            topMargin=0.9 * inch, bottomMargin=0.85 * inch, title="Engineering base pay policy",
                            author=head, subject="", creator="", producer="")
    fr = _frame("%s | Engineering base pay policy" % K.COMPANY, "Version 2026.2 | Internal")
    doc.build(story, onFirstPage=fr, onLaterPages=fr)


METHODOLOGY = """# Tallyband data extract: methodology

Prepared by Tallyband Data Services for licensed subscribers. Applies to extracts taken from July 2025.

## What a report is

A report is one person's pay at one employer, filed by that person on Tallyband: their employer, the employer's
level code for their job, their title, their base salary, their years of experience, where they work and how they
are employed, as at the date they filed it. Tallyband asks respondents to report the pay they are on when they
file.

## Who is in an extract

An extract holds every respondent who filed a report in the 36 months to the extract date, once, with the latest
report they filed. When a respondent files a new report at the same employer, Tallyband keeps their earlier report's
date, level code and base salary beside the new one, in the `previous_` columns; those columns are blank for
everyone else. The profile table, delivered with the extract, holds each respondent's profile as it stood on the
extract date.

This extract (`tallyband_extract_2026-10-01.csv`, with `tallyband_profiles_2026-10-01.csv`) was taken on
1 October 2026 for Tarnwick Systems under its subscriber licence.

## Fields

| Field | What it holds |
|---|---|
| `respondent_id` | Tallyband's id for the respondent, the same in the extract and the profile table |
| `filed_on` | the date the respondent filed the report |
| `employer` | the employer's name as the respondent typed it; Tallyband does not tidy names |
| `employer_level` | the employer's own level code for the job, as the respondent gave it |
| `tallyband_level` | Tallyband's normalised level (L1 to L7), assigned from the employer's level code |
| `job_family` | Tallyband's job family, assigned from the respondent's title |
| `title` | the respondent's job title |
| `years_experience` | years of professional experience the respondent reported |
| `country` | ISO 3166 code of the country the respondent works in |
| `state` | USPS state code, for respondents working in the United States |
| `employment_type` | `full_time`, `part_time` or `contract` |
| `base_salary_usd` | annual base salary in US dollars, before bonus and equity |
| `previous_filed_on`, `previous_employer_level`, `previous_base_salary_usd` | the respondent's earlier report at the same employer, where there is one |

Profile table: `respondent_id`, `primary_focus` (the area of work the respondent chose from their family's list),
`works_remotely` and `highest_degree`.

## Levels

Employers' ladders do not line up one to one. `tallyband_level` places every employer code on one scale for the
site's own charts, so one normalised level can hold codes that employers treat as different levels. Subscribers
who keep their own mapping from employer codes to their levels should use it.

## Pay

Base salary is the respondent's annual base pay as reported, in US dollars. Respondents outside the United States
report in their own currency; Tallyband converts at the exchange rate on the filing date. Part-time respondents
report the pay they actually receive.

## Privacy

Tallyband removes reports that could identify a person and never releases names or contact details. Subscribers may
not try to identify a respondent.
"""


def write_methodology(path):
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(METHODOLOGY)


ARCH_JOBS = [
    ("Data", "Data Engineer", "DE", 4, "Data Engineering", "data pipelines and platforms",
     ("Builds and runs batch and streaming pipelines with guidance", "Owns pipelines and data models for a domain",
      "Leads the design of a data platform area across teams", "Sets technical direction for the data platform")),
    ("Data", "Analytics Engineer", "AE", 3, "Data Engineering", "analytics engineering",
     ("Builds tested data models for reporting", "Owns the modelled layer for a business area",
      "Leads modelling standards across analytics")),
    ("Machine learning", "Machine Learning Engineer", "MLE", 4, "Machine Learning Engineering",
     "machine learning platform",
     ("Ships model training and serving code with guidance", "Owns models in production for a product area",
      "Leads machine learning systems across teams", "Sets technical direction for machine learning")),
    ("Software", "Software Engineer", "SWE", 4, "Software Engineering", "backend; frontend; full stack",
     ("Ships features with guidance", "Owns features end to end", "Leads projects across a team",
      "Sets technical direction across teams")),
    ("Reliability", "Site Reliability Engineer", "SRE", 4, "Site Reliability", "infrastructure; observability",
     ("Runs services with guidance", "Owns the reliability of a service", "Leads reliability across services",
      "Sets reliability direction")),
]
ROMAN = ("I", "II", "III", "IV")


def write_architecture(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Jobs"
    ws["A1"] = "%s engineering job architecture" % K.COMPANY
    ws["A1"].font = Font(name="Calibri", size=14, bold=True)
    ws["A2"] = "Owner: %s, Head of Total Rewards. In effect from 2 March 2026." % K.PEOPLE["head"]
    ws["A2"].font = Font(name="Calibri", size=10, italic=True, color="5D5A66")
    head = ["Family", "Job", "Job code", "Level", "Title", "Scope", "Tallyband family", "Tallyband primary focus"]
    for j, h in enumerate(head, 1):
        c = ws.cell(row=K.ARCH_HEADER_ROW + 1, column=j, value=h)
        c.font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor="4B2E5C")
        c.alignment = Alignment(vertical="center")
    row = K.ARCH_HEADER_ROW + 2
    for fam, job, code, n, tfam, tfocus, scopes in ARCH_JOBS:
        for i in range(n):
            vals = [fam, job, "%s%d" % (code, i + 1), ROMAN[i], "%s %s" % (job, ROMAN[i]), scopes[i], tfam, tfocus]
            for j, v in enumerate(vals, 1):
                ws.cell(row=row, column=j, value=v).font = Font(name="Calibri", size=11)
            row += 1
    for col, w in zip("ABCDEFGH", (13, 27, 10, 7, 30, 56, 30, 33)):
        ws.column_dimensions[col].width = w
    ws.freeze_panes = "C%d" % (K.ARCH_HEADER_ROW + 2)
    lv = wb.create_sheet("Levels")
    lv.append(["Level", "Expected scope", "Typical years of experience"])
    for c in lv[1]:
        c.font = Font(name="Calibri", size=11, bold=True)
    for r in (("I", "Delivers well-defined work with guidance", "0 to 3"),
              ("II", "Delivers independently within a team", "2 to 6"),
              ("III", "Leads work across a team or domain", "5 to 10"),
              ("IV", "Leads across teams; sets direction for an area", "8 or more")):
        lv.append(list(r))
    for col, w in zip("ABC", (8, 52, 27)):
        lv.column_dimensions[col].width = w
    nt = wb.create_sheet("Notes")
    for line in ("The survey match names the Tallyband family and primary focus whose respondents price each job.",
                 "Changes to this architecture are approved by the head of total rewards."):
        nt.append([line])
    nt.column_dimensions["A"].width = 100
    wb.save(path)


PEOPLE_NOTES = """# People data exports, 14 October 2026

Prepared by {data}, People Data and Systems, for the total rewards team's band refresh. Three exports, all pulled on
14 October 2026, plus the pay zone table.

## hris_job_history_2026-10-14.csv

The job history of every worker who has held a data engineering, machine learning engineering or analytics
engineering job at {company} since 2019: one row per job record. A job record is written for a hire, a promotion, a
transfer, the start or end of a leave of absence and a termination, and each row shows the whole job as it stands
from its effective date. Changes already agreed are entered ahead, with their future effective date.

| Column | What it holds |
|---|---|
| `employee_id` | the worker's id (an `E` id for employees, a `C` id for contingent workers) |
| `effective_date` | the date the job record takes effect |
| `action` | `hire`, `promotion`, `transfer`, `leave_start`, `leave_end` or `termination` |
| `job_code`, `job_title` | the job, as coded in the engineering job architecture |
| `work_location` | the city the worker works in |
| `pay_zone` | the pay zone recorded on the job record when it was written |
| `status` | `active`, `leave` or `terminated` |
| `worker_type` | `employee`, or `contingent` for contractors engaged through an agency |

## pay_zones_2026.csv

{company}'s pay zones: the zone each work location is in, with the dates it applies.

## ats_requisitions_2026-10-14.csv

Every engineering requisition opened since June 2025, with its postings.

| Column | What it holds |
|---|---|
| `requisition_id`, `posting_id` | the requisition, and the posting of it in one city |
| `job_code`, `job_title` | the job the requisition hires for |
| `posting_city` | the city of the posting |
| `opened_on` | the date the requisition opened |
| `closed_on` | the date the requisition closed with a hire |
| `status` | the requisition's status on the export date: `open`, `filled` or `cancelled` |
| `status_date` | the date that status took effect |
"""


def write_people_notes(path):
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(PEOPLE_NOTES.format(data=K.PEOPLE["data"], company=K.COMPANY))
