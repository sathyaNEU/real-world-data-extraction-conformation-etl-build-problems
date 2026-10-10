"""Document texts for the pack. Each load-bearing sentence is stated once, in the file the design note names."""

OFFICE = "Morvane Patent Office"

# ------------------------------------------------------------------------------------- charter (PDF)
CHARTER = dict(
    title="Performance Reporting Charter",
    sub="Morvane Patent Office, Office of the Commissioner. Adopted 14 June 2021; revised 9 September 2024.",
    by="Owner: Head of Performance Statistics. Distribution: Commissioner, Deputy Commissioners, Directors of "
       "Examination, Performance Statistics Unit.",
    blocks=[
        ("h", "1. What this charter covers"),
        ("p", "Section 41 of the Patents Act requires the Commissioner to file an annual performance report with "
              "the Minister for Enterprise by 31 January. This charter fixes how the figures in that report are "
              "defined and who owns them. It does not cover the trade mark and design registers, which report "
              "separately."),
        ("h", "2. Headline pendency"),
        ("p", "The headline figure is the median time from an application's filing to the office's final "
              "decision on it, for each fiscal year's filings (1 October to 30 September). The report for a "
              "reporting year carries the headline for the filings of the fiscal year that ended four years "
              "before it."),
        ("p", "Time is the number of days from the filing date to the date of the decision. It is reported in "
              "months to one decimal, a month being 30.4375 days. Shares in the report are percentages to one "
              "decimal."),
        ("p", "An application's filing date is the date the office received it. A priority or benefit claim "
              "does not move it."),
        ("p", "An application not finally decided at the extract counts as still waiting at the extract."),
        ("h", "3. The extract"),
        ("p", "Report figures are computed on the production extract cut at the close of the reporting year "
              "(30 September). The production systems manager cuts and documents the extract; the Performance "
              "Statistics Unit does not edit it."),
        ("h", "4. Other published measures"),
        ("p", "Examiner docket pendency is a production measure: the time from docketing to docket close, "
              "published in the office's production tables since 2006. The Morvane Patent Examiners' "
              "Association publishes examiner docket pendency from the production system beside the office's "
              "headline, as it has each year. That is the Association's figure and the office does not "
              "comment on it in the report."),
        ("h", "5. Sign-off"),
        ("p", "The Head of Performance Statistics drafts the headline section and the tables beneath it. The "
              "Deputy Commissioner for Operations signs off the draft before it goes to the Commissioner, "
              "normally in the first week of January."),
        ("small", "Internal. Not for onward distribution outside the office. Queries to the Performance "
                  "Statistics Unit, extension 4417."),
    ],
)

# ---------------------------------------------------------------------------- production standard (PDF)
STANDARD = dict(
    title="Examiner Production Standard",
    sub="Effective for actions served from 1 October 2018 (FY2019). Issued by the Examination Practice "
        "Directorate under the 2018 agreement with the Morvane Patent Examiners' Association.",
    by="Reference EPD/PS/2019. Supersedes EPD/PS/2014; the credit classes and counts are carried over "
       "unchanged and the expectancy table is new.",
    blocks=[
        ("h", "1. Scope"),
        ("p", "This standard sets how examining work is credited for production purposes. It applies to every "
              "examiner assigned to an examining art unit, including examiners on detail for part of a pay "
              "period. It does not apply to classification, search-only work for other offices or quality "
              "review, which are recorded as other time."),
        ("h", "2. Credit classes"),
        ("table", {"rows": [["Class", "Action credited", "Counts"],
                            ["1N", "The first action on the merits in an application, credited once per "
                                   "application.", "1.25"],
                            ["1R", "The first action on the merits after a refusal is set aside on a request "
                                   "for re-examination.", "1.00"],
                            ["DP", "A disposal: a notice of allowance, a notice of refusal or a notice of "
                                   "abandonment.", "0.75"]],
                   "widths": [40, 330, 50]}),
        ("p", "An examination report other than one credited above, an interview record and the grant earn no "
              "credit. They are recorded in the action history and count towards examining time."),
        ("h", "3. Posting"),
        ("p", "A credit is posted to the examiner who signed the action, in the biweekly pay period in which "
              "the action is served. Pay periods are numbered from the first pay period of the fiscal year. "
              "Each credit is posted to the production ledger with the action identifier it is earned on."),
        ("h", "4. Expectancy"),
        ("table", {"rows": [["Grade", "Expected counts per 80 hours examining", "Review"],
                            ["Examiner", "3.2", "Quarterly"],
                            ["Senior Examiner", "3.8", "Half-yearly"],
                            ["Principal Examiner", "4.1", "Annual"]],
                   "widths": [110, 220, 90]}),
        ("p", "Expectancy is adjusted for art unit by the Directors of Examination each October and is pro rata "
              "for part-time examiners. Overtime counts are credited at the same rates."),
        ("h", "5. Quality"),
        ("p", "A sample of credited actions is reviewed each quarter by the Quality Review Section. An action "
              "found deficient keeps its credit; the finding is recorded against the examiner's quality "
              "factor, not the ledger."),
        ("small", "Examination Practice Directorate, Morvane Patent Office. Agreed with the Morvane Patent "
                  "Examiners' Association, 21 August 2018."),
    ],
)

# ------------------------------------------------------------------------------------ codebook (md)
CODEBOOK = """# Examination production system: extract codebook

Production Systems, Morvane Patent Office. Maintained by Michael Cannon. Revised 2 October 2026 for the
30 September 2026 extract.

The extract is cut from the examination production system (EPS) at close of business on the last working
day of the fiscal year. EPS is keyed on the examination docket. A docket is one examiner's file on one
application, from the day it is docketed to the day it is closed.

## examination_dockets_FY2016_FY2026.parquet

One row per docket opened from 1 October 2015 to 30 September 2026.

| Field | Meaning |
|---|---|
| docket_no | Docket number, YY-NNNNNN, allocated in docketing order within the fiscal year the docket was opened. A few numbers are voided at allocation and never used. An application is numbered by the docket opened when it was filed. |
| docketed_on | Date the docket was opened: the day the filing it was opened on was received. |
| art_unit | Art unit holding the docket at close, or at the extract if the docket is open. |
| tg | Technology group code of the docketing art unit when the docket was opened. |
| examiner_id | Examiner holding the docket at close, or at the extract if the docket is open. |
| closed_on | Date the docket closed. Blank if the docket is open at the extract. |
| end_code | How the docket closed (below). Blank if the docket is open at the extract. |

End codes:

- **ALW** allowed. The docket closes when the patent is granted, not on the notice of allowance.
- **REF** refused. The docket closes on the date the notice of refusal is served.
- **ABN** abandoned. The docket closes on the date the notice of abandonment is served.
- **CX** file transferred. The docket closed on its refusal and its examination file passed to a new docket.
  EPS rewrites the end code from REF to CX when the new docket is opened; the closing date is unchanged.

## docket_links.csv

One row per docket opened in the extract window that was opened from an earlier docket. The parent may have
been opened before 1 October 2015, in which case it is not in the docket extract.

| Field | Meaning |
|---|---|
| parent_docket | The earlier docket. |
| child_docket | The docket opened from it. |
| link_type | CX: the child was opened on the examination file of the parent after the parent's refusal (end code CX). CN: a continuation filed while the parent docket was open, examined on a new file. DV: a divisional application filed while the parent docket was open, examined on a new file. |
| linked_on | Equal to the child's docketed_on. |

## office_actions_FY2016_FY2026.parquet

One row per action served on a docket in the docket extract, up to the extract.

| Field | Meaning |
|---|---|
| action_id | Action identifier, unique across EPS. |
| docket_no | The docket the action was served on. |
| action_code | EXR examination report (an action on the merits stating the examiner's objections); ITV interview record; NOA notice of allowance; REF notice of refusal; ABN notice of abandonment; GRT patent granted. |
| served_on | Date the action was served. |

## examiner_production_ledger_FY2016_FY2026.parquet

One row per production credit posted for an action in the action extract.

| Field | Meaning |
|---|---|
| credit_id | Ledger entry number. |
| pay_period | Fiscal year and biweekly pay period the credit was posted to, FYyyyy-PPnn. |
| examiner_id | Examiner credited. |
| action_id | The action the credit was earned on. |
| credit_class | Credit class under the Examiner Production Standard. |
| counts | Counts credited. |

## docket_transfers.csv

One row per transfer of an open docket between art units.

| Field | Meaning |
|---|---|
| docket_no | The docket transferred. |
| transferred_on | Date of the transfer. |
| from_au | Art unit the docket left. |
| to_au | Art unit the docket went to. |

## art_unit_groups.csv

Technology group of each examining art unit, effective dated. valid_to is blank for the row in force.

## examiner_roster_2026-09-30.csv

Examiners on the roster at the extract, with grade, home art unit, that art unit's technology group and FTE.

Dates are ISO 8601 throughout. Codes are upper case. Nothing in the extract is edited after it is cut.
"""

# ------------------------------------------------------------------------------- extract notes (md)
def extract_notes(rows):
    """rows: {file name: row count or None}."""
    def n(f):
        return "{:,}".format(rows[f])
    return f"""# Extract notes: annual performance report, FY2026

Michael Cannon, Production Systems Manager. 2 October 2026; file list brought up to date 15 October 2026.

The production extract for the FY2026 report was cut from EPS at 18:00 on 30 September 2026 and copied to the
Performance Statistics share on 2 October. Nothing in it has been edited since the cut. The other files in the
folder were added by the Performance Statistics Unit and are listed here so the folder has one record of what is
in it and where each file came from.

| File | What it is | Coverage | Source | Rows |
|---|---|---|---|---|
| examination_dockets_FY2016_FY2026.parquet | Docket extract | Dockets opened 1 Oct 2015 to 30 Sep 2026 | EPS | {n('examination_dockets_FY2016_FY2026.parquet')} |
| office_actions_FY2016_FY2026.parquet | Action history | Actions served on those dockets to 30 Sep 2026 | EPS | {n('office_actions_FY2016_FY2026.parquet')} |
| docket_links.csv | Docket links | Dockets in the extract opened from an earlier docket | EPS | {n('docket_links.csv')} |
| docket_transfers.csv | Art unit transfers | Transfers of dockets in the extract | EPS | {n('docket_transfers.csv')} |
| examiner_production_ledger_FY2016_FY2026.parquet | Production ledger | Credits posted for actions in the action history | EPS production ledger | {n('examiner_production_ledger_FY2016_FY2026.parquet')} |
| art_unit_groups.csv | Art unit table | Every examining art unit since FY2006 | EPS reference tables | {n('art_unit_groups.csv')} |
| examiner_roster_2026-09-30.csv | Examiner roster | Examiners on the roster at 30 Sep 2026 | HR establishment report | {n('examiner_roster_2026-09-30.csv')} |
| docketing_codebook.md | Field definitions for the files above | | Production Systems | |
| saravel_ipo_acknowledgements_FY2019-FY2022.xlsx | The Saravel Intellectual Property Office's acknowledgements of our final decisions on work-sharing programme applications filed FY2019 to FY2022, with their quarterly medians | Decisions to 30 Sep 2026 | Saravel IPO, received 14 Oct 2026 | {n('saravel_ipo_acknowledgements_FY2019-FY2022.xlsx')} |
| annual_report_2025_tables_P1_P2.xlsx | Last year's production tables P1 and P2 as published | FY2006 to FY2025 | Annual Performance Report 2025 | |
| report_table_notes.docx | Notes to the annual report tables | Standing notes | Performance Statistics Unit | |
| performance_reporting_charter.pdf | Performance Reporting Charter, revised September 2024 | | Office of the Commissioner | |
| examiner_production_standard_2019.pdf | Examiner Production Standard EPD/PS/2019 | Actions served from 1 Oct 2018 | Examination Practice Directorate | |
| international_pendency_comparison_2025.xlsx | Pendency figures published by four other offices | Their 2024 and 2025 reports | International Relations Unit | |
| headline_section_thread.eml | Correspondence on the headline section | October 2026 | Performance Statistics Unit | |

Row counts exclude header rows. The docket, action and ledger extracts are Parquet with ISO dates; the rest are
CSV (UTF-8, comma separated), Excel, Word, PDF and plain text.

Dockets opened before 1 October 2015 are not in the docket extract. A link whose parent was opened before then
is kept, so a parent docket number in docket_links.csv may not appear in the docket extract.

Published under the Morvane Government Open Data Licence (compatible with CC BY 4.0). Personal data: examiner
identifiers are pseudonymous staff numbers.
"""


# ----------------------------------------------------------------------------- table notes (docx)
TABLE_NOTES = dict(
    title="Annual Performance Report: notes to the tables",
    blocks=[
        ("meta", "Performance Statistics Unit. Standing notes, revised 11 October 2024. These notes are printed "
                 "at the back of the report and apply to every edition until revised."),
        ("h", "Headline and headline tables"),
        ("p", "The headline and its definitions are set by the Performance Reporting Charter. The tables "
              "printed under the headline use the headline's population, dates and extract."),
        ("p", "Tables by technology group are restated on the group structure in force at the extract. Each "
              "application is counted in the group, at the extract, of the art unit that docketed it at "
              "filing."),
        ("p", "A share decided within a period counts every application in the table's population in its "
              "denominator, decided or not."),
        ("h", "Production tables"),
        ("p", "Table P1, examiner docket pendency: months from docketing to docket close (for an allowed "
              "docket, the grant), by the fiscal year the docket was opened. Every docket counts, whatever "
              "it was opened on. A year is first reported once 98 per cent of its dockets have closed; the "
              "median counts dockets still open as longer than any closed docket."),
        ("p", "Table P2, dockets opened by technology group: dockets counted by the group code recorded on "
              "the docket when it was opened. P2 is not restated."),
        ("p", "Table P3, examining staff: full-time equivalents at the extract, by grade."),
        ("h", "Rounding"),
        ("p", "Figures are rounded for presentation only; totals are computed before rounding and may not equal "
              "the sum of rounded parts."),
        ("h", "Revisions"),
        ("p", "Published tables are not revised for later extracts. A figure that would change on a later "
              "extract is reported once it is final under the rule for its table."),
    ],
)

# --------------------------------------------------------------------------------------- thread (eml)
THREAD = """From: Stephen Brewer <s.brewer@mpo.gov.mv>
To: Thomas Kennedy <t.kennedy@mpo.gov.mv>, Cristina Turner <c.turner@mpo.gov.mv>,
 Lauren Mendoza <l.mendoza@mpo.gov.mv>, Michael Cannon <m.cannon@mpo.gov.mv>
Cc: Erica Ryan <secretary@mpea.org.mv>
Subject: RE: APR 2026 headline section
Date: Tue, 13 Oct 2026 16:42:09 +0000
Message-ID: <a71c09e2.4417@mpo.gov.mv>
In-Reply-To: <5d20be11.3302@mpea.org.mv>
MIME-Version: 1.0
Content-Type: text/plain; charset="utf-8"
Content-Transfer-Encoding: 8bit

Thanks all. I'll take the headline section from here and send a draft to Thomas before Christmas. The
minister's office asked for the technology group table under the headline again, same three columns as the
version they saw in the spring briefing, so I'll carry that.

Stephen

Stephen Brewer
Head of Performance Statistics | Morvane Patent Office

-----Original Message-----
From: Erica Ryan <secretary@mpea.org.mv>
Sent: Monday, 12 October 2026 09:15
Subject: RE: APR 2026 headline section

Stephen, for your planning: the Association will publish examiner docket pendency from the production
system beside the office's headline again this year, on the same basis as every year since 2006. Our members
know that series and we'll keep it. Happy to share our release date when the committee fixes it.

Erica Ryan
Secretary, Morvane Patent Examiners' Association

-----Original Message-----
From: Lauren Mendoza <l.mendoza@mpo.gov.mv>
Sent: Friday, 9 October 2026 11:58
Subject: RE: APR 2026 headline section

On Thomas's point, from the practice side: a refused file that comes back on a new docket is the same file.
It goes back to the examiner who refused it, with everything on it, and it gets picked up where it was left.
Nothing about that changed in the year.

Lauren

-----Original Message-----
From: Cristina Turner <c.turner@mpo.gov.mv>
Sent: Thursday, 8 October 2026 14:20
Subject: RE: APR 2026 headline section

Saravel have confirmed they'll send their acknowledgements for the programme cases filed FY2019 to FY2022 by
mid-month, with their quarterly medians as usual. We tie our decision dates to theirs case by case every
quarter and it's been clean since the programme started, so it's a good check on whatever goes in the
headline. I'll drop the file in the folder when it lands.

Cristina

-----Original Message-----
From: Thomas Kennedy <t.kennedy@mpo.gov.mv>
Sent: Wednesday, 7 October 2026 08:31
Subject: RE: APR 2026 headline section

Stephen, I don't want to reinvent anything this year. Our dockets are our applications, and we have twenty
years of docket pendency in the production tables that the ministry already knows. The headline should sit
on that series. Draft it that way and I'll sign it off.

Thomas

-----Original Message-----
From: Michael Cannon <m.cannon@mpo.gov.mv>
Sent: Friday, 2 October 2026 10:04
Subject: APR 2026 headline section

All, the 30 September extract is on the Performance Statistics share: dockets, actions, links, transfers, the
production ledger, the art unit table and the roster, same layout as last year. Codebook and extract notes
are alongside. Shout if anything looks off.

Michael

Michael Cannon
Production Systems Manager | Morvane Patent Office

--
OFFICIAL. Internal correspondence of the Morvane Patent Office. Do not forward outside the office.
"""
