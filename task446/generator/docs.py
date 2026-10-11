"""Documents and workbooks for task446's pack (architecture 2)."""
import datetime as dt
import io
import os
import re
import zipfile

import numpy as np
import openpyxl
from openpyxl.styles import Font, Alignment
from openpyxl.utils import get_column_letter

import world
from world import D, EXTRACT_DATE

FIXED_ZIP_TIME = (2026, 10, 8, 17, 42, 0)
MODIFIED = dt.datetime(2026, 10, 8, 16, 55, 0)


def normalize_zip(path, modified=MODIFIED, app=b"Microsoft Excel"):
    """Rewrite an OOXML zip with fixed member times, fixed order and a plausible writer, so two
    builds are byte-identical and no library signature ships."""
    with zipfile.ZipFile(path) as z:
        items = [(i.filename, z.read(i.filename)) for i in z.infolist()]
    out = []
    created = (modified - dt.timedelta(days=9, hours=3)).strftime("%Y-%m-%dT%H:%M:%SZ").encode()
    stamp = modified.strftime("%Y-%m-%dT%H:%M:%SZ").encode()
    for n, data in items:
        if n == "docProps/app.xml":
            data = re.sub(rb"<Application>[^<]*</Application>", b"<Application>" + app + b"</Application>", data)
            data = re.sub(rb"<AppVersion>[^<]*</AppVersion>", b"<AppVersion>16.0300</AppVersion>", data)
        if n == "docProps/core.xml":
            data = re.sub(rb"(<dcterms:created[^>]*>)[^<]*(</dcterms:created>)", rb"\g<1>" + created + rb"\g<2>", data)
            data = re.sub(rb"(<dcterms:modified[^>]*>)[^<]*(</dcterms:modified>)", rb"\g<1>" + stamp + rb"\g<2>", data)
            data = re.sub(rb"<cp:lastPrinted>[^<]*</cp:lastPrinted>", b"", data)
        out.append((n, data))
    first = [x for x in out if x[0] == "[Content_Types].xml"]
    rest = sorted([x for x in out if x[0] != "[Content_Types].xml"])
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in first + rest:
            zi = zipfile.ZipInfo(name, date_time=FIXED_ZIP_TIME)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o600 << 16
            z.writestr(zi, data)


def set_props(wb, creator):
    p = wb.properties
    p.creator = creator
    p.lastModifiedBy = creator
    p.created = MODIFIED - dt.timedelta(days=9, hours=3)
    p.modified = MODIFIED
    p.title = None


def widths(ws, ws_widths):
    for i, w_ in enumerate(ws_widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w_


# ------------------------------------------------------------------ group register
def register_workbook(w, path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Group register"
    ws["A1"] = "Credit system: obligor group register"
    ws["A1"].font = Font(bold=True)
    ws["A2"] = "As at 30/09/2026. Reference Data quarter-end extract. Includes groups whose relationship has ended."
    hdr = ["group_id", "group_name", "ultimate_parent_lei", "relationship_start", "relationship_end", "sector_code",
           "sector", "coverage_team", "credit_officer"]
    ws.append([])
    ws.append(hdr)
    for c in ws[4]:
        c.font = Font(bold=True)
    for gid, g in sorted(w.groups.items()):
        top = g.members[0]
        code, desc, _ = world.SECTORS[g.sector]
        ws.append([gid, g.name, top.lei or "", g.active_from, g.active_to, code, desc, g.coverage, g.officer])
    for row in ws.iter_rows(min_row=5, min_col=4, max_col=5):
        for c in row:
            c.number_format = "dd/mm/yyyy"
    widths(ws, [11, 44, 23, 15, 15, 11, 36, 24, 13])
    ws.freeze_panes = "A5"
    set_props(wb, "Reference Data")
    wb.save(path)
    normalize_zip(path)


def ratings_workbook(w, path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Master scale"
    ws.append(["Halstow Bank internal rating master scale (corporate and commercial), effective 1 January 2026"])
    ws["A1"].font = Font(bold=True)
    ws.append([])
    ws.append(["grade", "description", "pd_lower", "pd_upper", "pd_midpoint", "s&p_equivalent"])
    for c in ws[3]:
        c.font = Font(bold=True)
    scale = [(1, "Exceptional", 0.0000, 0.0005, "AA"), (2, "Very strong", 0.0005, 0.0012, "A"),
             (3, "Strong", 0.0012, 0.0025, "BBB+"), (4, "Good", 0.0025, 0.0050, "BBB-"),
             (5, "Satisfactory", 0.0050, 0.0100, "BB+"), (6, "Adequate", 0.0100, 0.0200, "BB"),
             (7, "Weak", 0.0200, 0.0450, "BB-"), (8, "Vulnerable", 0.0450, 0.1000, "B"),
             (9, "Watch", 0.1000, 0.2500, "CCC"), (10, "Default", 1.0, 1.0, "D")]
    for gr, de, lo, hi, sp in scale:
        mid = round((lo * hi) ** 0.5, 5) if lo > 0 and hi < 1 else (0.0002 if gr == 1 else 1.0)
        ws.append([gr, de, lo, hi, mid, sp])
    widths(ws, [8, 16, 10, 10, 12, 16])
    ws2 = wb.create_sheet("Group ratings 30-09-2026")
    ws2.append(["group_id", "rating_grade", "rating_date", "rating_model"])
    for c in ws2[1]:
        c.font = Font(bold=True)
    rng = np.random.default_rng(world.SEED + 31)
    for gid, g in sorted(w.groups.items()):
        if not w.active(g, EXTRACT_DATE):
            continue
        base = 4.2 + (1.8 if g.flag.get(4) else 0.0) + (2.5 if w.on_list(g, EXTRACT_DATE) else 0.0)
        grade = int(np.clip(round(base + rng.normal(0, 1.1)), 1, 9))
        rdate = EXTRACT_DATE - dt.timedelta(days=int(rng.integers(10, 360)))
        ws2.append([gid, grade, rdate, "CORP-SCORE v5" if rng.random() < 0.8 else "COMMERCIAL-SCORE v3"])
    for row in ws2.iter_rows(min_row=2, min_col=3, max_col=3):
        for c in row:
            c.number_format = "dd/mm/yyyy"
    widths(ws2, [11, 13, 13, 22])
    set_props(wb, "Credit Risk Models")
    wb.save(path)
    normalize_zip(path)


def scenarios_workbook(path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Weights"
    ws.append(["IFRS 9 forward-looking scenarios, 2026 Q3 run. Approved by the Impairment Committee 6 October 2026."])
    ws["A1"].font = Font(bold=True)
    ws.append([])
    ws.append(["scenario", "weight"])
    for row in [("Upside", 0.15), ("Base", 0.50), ("Downside", 0.25), ("Severe downside", 0.10)]:
        ws.append(list(row))
    widths(ws, [18, 10])
    qs = ["2026Q4", "2027Q1", "2027Q2", "2027Q3", "2027Q4", "2028Q1", "2028Q2", "2028Q3", "2028Q4", "2029Q1",
          "2029Q2", "2029Q3", "2029Q4"]
    paths = {
        "Upside": dict(gdp=[0.5, 0.6, 0.6, 0.5, 0.5, 0.5, 0.5, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4],
                       unemp=[4.8, 4.7, 4.6, 4.5, 4.4, 4.3, 4.3, 4.2, 4.2, 4.2, 4.2, 4.1, 4.1],
                       rate=[3.75, 3.50, 3.25, 3.25, 3.00, 3.00, 3.00, 3.00, 3.00, 3.00, 3.00, 3.00, 3.00]),
        "Base": dict(gdp=[0.2, 0.3, 0.3, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4],
                     unemp=[5.1, 5.2, 5.2, 5.1, 5.0, 4.9, 4.9, 4.8, 4.8, 4.7, 4.7, 4.7, 4.6],
                     rate=[3.75, 3.75, 3.50, 3.50, 3.25, 3.25, 3.25, 3.00, 3.00, 3.00, 3.00, 3.00, 3.00]),
        "Downside": dict(gdp=[-0.3, -0.4, -0.2, 0.0, 0.2, 0.3, 0.3, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4],
                         unemp=[5.4, 5.8, 6.1, 6.3, 6.4, 6.3, 6.2, 6.0, 5.9, 5.8, 5.7, 5.6, 5.5],
                         rate=[3.75, 3.50, 3.00, 2.75, 2.50, 2.50, 2.50, 2.50, 2.75, 2.75, 2.75, 3.00, 3.00]),
        "Severe downside": dict(gdp=[-0.9, -1.2, -0.8, -0.3, 0.1, 0.3, 0.4, 0.4, 0.5, 0.5, 0.5, 0.5, 0.5],
                                unemp=[5.8, 6.6, 7.3, 7.8, 8.0, 7.9, 7.7, 7.4, 7.1, 6.9, 6.7, 6.5, 6.3],
                                rate=[3.75, 3.25, 2.50, 2.00, 1.75, 1.75, 1.75, 2.00, 2.00, 2.25, 2.25, 2.50, 2.50]),
    }
    for name, p in paths.items():
        s = wb.create_sheet(name[:28])
        s.append(["quarter", "real_gdp_qoq_pct", "unemployment_rate_pct", "bank_rate_pct_end_quarter"])
        for c in s[1]:
            c.font = Font(bold=True)
        for i, q in enumerate(qs):
            s.append([q, p["gdp"][i], p["unemp"][i], p["rate"][i]])
        widths(s, [10, 18, 22, 26])
    set_props(wb, "Impairment Analytics")
    wb.save(path)
    normalize_zip(path)


# ------------------------------------------------------------------ docx agenda
def agenda_docx(path):
    import docx
    from docx.shared import Pt
    doc = docx.Document()
    st = doc.styles["Normal"]
    st.font.name = "Arial"
    st.font.size = Pt(10)
    p = doc.add_paragraph()
    r = p.add_run("HALSTOW BANK PLC")
    r.bold = True
    doc.add_paragraph("Executive Risk Committee")
    doc.add_paragraph("Wednesday 4 November 2026, 09:30 to 12:00, Board Room 2, Halstow House")
    doc.add_paragraph("Chair: Chief Risk Officer. Members: Chief Financial Officer, Chief Credit Officer, Chief "
                      "Operating Officer. In attendance: Jill Berry (Head of Credit Risk Monitoring), Mathew Long "
                      "(Head of Restructuring), Head of Business Support, Company Secretary.")
    p = doc.add_paragraph()
    p.add_run("Agenda").bold = True
    items = [
        "1. Minutes of the meeting of 7 October 2026 and matters arising",
        "2. Q3 2026 risk appetite dashboard (Chief Risk Officer)",
        "3. 2027 resourcing budget: credit",
        "    3.1 Watch-list caseload for the year to 30 September 2027 (Credit Risk Monitoring, paper to follow). "
        "The caseload standard for Restructuring and Business Support is twelve watch-list groups per analyst.",
        "    3.2 Restructuring and Business Support headcount for 2027 (Head of Restructuring)",
        "4. Early-warning system annual performance report: taken at the Credit Risk Committee on 18 November",
        "5. Operational resilience: third-party data feeds (Chief Operating Officer)",
        "6. Any other business",
    ]
    for it in items:
        doc.add_paragraph(it)
    doc.add_paragraph("Papers to the Company Secretary by 12:00 on Wednesday 28 October. Item 3.1 papers carry the "
                      "committed exposure by caseload band so that 3.2 can be read against them.")
    p = doc.add_paragraph()
    p.add_run("Internal. Not for onward distribution.").italic = True
    cp = doc.core_properties
    cp.author = "Company Secretariat"
    cp.last_modified_by = "Company Secretariat"
    cp.created = MODIFIED - dt.timedelta(days=9, hours=3)
    cp.modified = MODIFIED
    cp.revision = 4
    cp.title = ""
    cp.comments = ""
    doc.save(path)
    normalize_zip(path, app=b"Microsoft Office Word")


# ------------------------------------------------------------------ PDF standard
def _pdf(path, title, author, blocks):
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab import rl_config
    rl_config.invariant = 1
    ss = getSampleStyleSheet()
    body = ParagraphStyle("b", parent=ss["Normal"], fontName="Helvetica", fontSize=9.5, leading=13)
    bullet = ParagraphStyle("u", parent=body, leftIndent=14)
    h = ParagraphStyle("h", parent=ss["Normal"], fontName="Helvetica-Bold", fontSize=10.5, leading=14,
                       spaceBefore=6)
    t = ParagraphStyle("t", parent=ss["Normal"], fontName="Helvetica-Bold", fontSize=13, leading=17)
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=56, rightMargin=56, topMargin=56, bottomMargin=56,
                            title=title, author=author, creator="", producer="", subject="")
    story = []
    for kind, text in blocks:
        story.append(Paragraph(text, {"t": t, "h": h, "p": body, "u": bullet}[kind]))
        story.append(Spacer(1, 4 if kind != "t" else 8))
    doc.build(story)
    data = buf.getvalue()
    stamp = b"D:20260212101500+00'00'"
    data = data.replace(b"D:20000101000000+00'00'", stamp)
    for s in (b"ReportLab Generated PDF document (opensource)",
              b"ReportLab generated PDF document -- digest (opensource)"):
        data = data.replace(s, b" " * len(s))
    with open(path, "wb") as fh:
        fh.write(data)


def standard_pdf(path):
    B = [
        ("t", "Halstow Bank plc<br/>Early-Warning and Watch-List Monitoring Standard"),
        ("p", "Standard CRM-07, version 3.1. Approved by the Credit Risk Committee on 12 February 2026. "
              "Owner: Head of Credit Risk Monitoring. Next review: February 2027."),
        ("h", "1 Scope"),
        ("p", "1.1 This standard covers the corporate and commercial book: every obligor group with a committed "
              "facility from Halstow Bank plc or Halstow Bank Ireland DAC. It sets how early-warning signals are "
              "carried to groups, how the watch list is measured against them, and how the watch-list caseload "
              "is forecast for resourcing."),
        ("p", "1.2 The early-warning system is release 3.2 of the engine, in production since 10 January 2022. "
              "Its models, triggers and bands have not changed since. A change would be a new release, approved "
              "by the Model Risk Committee before use."),
        ("h", "2 Obligor groups"),
        ("p", "2.1 An obligor group is the set of legal entities under one ultimate accounting-consolidation "
              "parent. The credit system's group register holds each group, the dates its relationship with the "
              "Bank started and ended, and the LEI of its ultimate parent where the parent has one."),
        ("p", "2.2 A group's members are the customers the credit system books to it and every legal entity "
              "whose GLEIF relationship record shows it accounting-consolidated into the group's ultimate parent "
              "(IS_ULTIMATELY_CONSOLIDATED_BY; where an entity reports only IS_DIRECTLY_CONSOLIDATED_BY, its "
              "direct parents are followed to the top), with the relationship in force at the date in question."),
        ("p", "2.3 An entity whose LEI registration has lapsed is still the entity its LEI identifies. An "
              "international branch belongs with its head office. A fund-management link is not consolidation. "
              "An entity merged into another is carried by its successor from the merger date."),
        ("h", "3 Signals and flags"),
        ("p", "3.1 The engine publishes a signal for every entity it covers at each month-end: GREEN, AMBER or "
              "RED, with a score from 0 to 99 and the triggers behind it. Entities with an LEI are keyed by LEI, "
              "entities without one by their Companies House number."),
        ("p", "3.2 A group is flagged at a date when any of its members carries AMBER or RED in the engine's "
              "publication for that month-end."),
        ("h", "4 The watch list and the cohorts"),
        ("p", "4.1 The monitored book at a cohort date, 30 September each year, is every group active on the "
              "group register at that date and not on the watch list at that date."),
        ("p", "4.2 A group in a cohort reaches the watch list if it is placed on the watch list in the twelve "
              "months after the cohort date. A group that leaves the book in that time without being placed has "
              "not reached it. A group counts once."),
        ("p", "4.3 The system's performance is reported to the Credit Risk Committee each November on the last "
              "four closed cohorts taken together:"),
        ("u", "hit rate: groups flagged at the cohort date that reach the watch list, as a share of groups "
              "flagged;"),
        ("u", "capture rate: groups reaching the watch list that were flagged at the cohort date, as a share of "
              "groups reaching it;"),
        ("u", "false-alarm rate: groups not reaching the watch list that were flagged at the cohort date, as a "
              "share of groups not reaching it."),
        ("h", "5 Watch-list caseload forecast"),
        ("p", "5.1 Each October credit risk monitoring forecasts how many groups in the monitored book at the "
              "cohort date will reach the watch list in the following twelve months, and the committed exposure "
              "they will bring, for the resourcing budget. Groups that join the book after the cohort date are "
              "outside the forecast."),
        ("p", "5.2 The forecast gives each group in the monitored book a probability of reaching the watch list "
              "that depends only on its flag status at the cohort date and is the same across the book. It is "
              "set from the performance measures in 4.3. Expected arrivals are the sum of those probabilities; "
              "expected exposure is the sum of each probability times the group's committed exposure."),
        ("p", "5.3 The caseload is reported to the nearest whole group, and expected arrivals within a band to "
              "one decimal."),
        ("h", "6 Committed exposure and caseload bands"),
        ("p", "6.1 A group's committed exposure at a date is the sum of the committed limits of its members' "
              "facilities in force at the end of that date, across Halstow Bank plc and Halstow Bank Ireland DAC, "
              "in sterling at that date's Group Treasury closing rates. A facility whose final maturity date "
              "falls on or before the date is not in force at the end of it."),
        ("p", "6.2 The caseload is reported in five bands of committed exposure: under GBP 5m; GBP 5m and under "
              "GBP 15m; GBP 15m and under GBP 40m; GBP 40m and under GBP 100m; GBP 100m and over. Groups of "
              "GBP 40m and over are worked by Restructuring, the rest by Business Support."),
        ("h", "7 Records"),
        ("p", "7.1 Signals are kept for every month-end from September 2022. Reference Data extracts the group "
              "register, the obligor master, the watch-list history and the GLEIF records for the Bank's entities "
              "at each quarter-end."),
    ]
    _pdf(path, "Early-Warning and Watch-List Monitoring Standard", "Credit Risk Monitoring", B)


# ------------------------------------------------------------------ markdown and text
def field_reference(path, files):
    txt = f"""# Credit data: field reference

Maintained by Reference Data. Covers the quarter-end extracts used by Credit Risk Monitoring.

## {files['signals']}

Month-end publications of the early-warning engine, one row per covered entity per month-end.

| field | meaning |
|---|---|
| publication_date | the month-end the publication is for |
| entity_key | the entity's LEI, or `CRN:` and the Companies House number for an entity without an LEI |
| entity_name | the name as the engine's data vendor holds it |
| country | country of registration |
| signal | GREEN, AMBER or RED |
| score | 0 to 99; GREEN below 40, AMBER 40 to 69, RED 70 and over |
| trigger_codes | triggers active at the publication, semicolon separated (see {files['triggers']}) |
| feed | the vendor feed the leading trigger came from; COMPOSITE where no trigger is active |
| engine_release | engine release that produced the publication |

## {files['obligors']}

Every customer the credit system has booked to an obligor group, open or closed.

| field | meaning |
|---|---|
| customer_id | credit system customer number |
| lei | the customer's LEI where held |
| companies_house_no | Companies House number for UK-registered customers |
| group_id | the obligor group the customer is booked to |
| customer_status | ACTIVE or CLOSED at the extract date |
| primary_booking_entity | HB-PLC (Halstow Bank plc) or HB-DAC (Halstow Bank Ireland DAC) |

## {files['register']}

One row per obligor group, including groups whose relationship has ended.

| field | meaning |
|---|---|
| ultimate_parent_lei | LEI of the group's ultimate accounting-consolidation parent; blank where the parent has none |
| relationship_start | date the group's first facility started |
| relationship_end | date the relationship ended (last facility repaid, refinanced elsewhere or transferred to Recoveries); blank while active |
| sector_code, sector | the group's sector |

## {files['watchlist']}

Every watch-list case opened since 1 January 2020.

| field | meaning |
|---|---|
| placed_on | date the group was placed on the watch list |
| watch_level | 1, 2 or 3 (case intensity); every level is on the watch list |
| removed_on | date the case closed; blank while open |
| removal_reason | CURED, REFINANCED_AWAY or TO_RECOVERY |

## Facility extracts ({files['plc']}, {files['plc_rerun']}, {files['dac']})

One row per facility held by the booking entity at the extract date.

| field | meaning |
|---|---|
| booking_entity | HB-PLC or HB-DAC |
| currency | facility currency |
| committed_limit | the facility's committed limit, in the facility currency |
| drawn_balance | drawn balance at the extract time, in the facility currency |
| start_date | date the facility became available |
| final_maturity_date | date the facility falls due for repayment and the commitment ends |
| facility_status | ACTIVE, CANCELLED or CLOSED, maintained by the overnight batch |

## {files['fx']}

| field | meaning |
|---|---|
| closing_rate | units of the currency for one pound sterling at the Group Treasury 16:00 London close |

## GLEIF files ({files['lei']}, {files['rr']}, {files['repex']})

Records from GLEIF's concatenated files published on 30 September 2026 (LEI-CDF 3.1, RR-CDF 2.1 and reporting
exceptions), filtered by Reference Data to the LEIs in the obligor master and the engine's coverage list.
Field names are GLEIF's.
"""
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(txt)


def count_rows(path):
    with open(path, encoding="utf-8") as fh:
        return sum(1 for _ in fh) - 1


def extract_log(path, files, target):
    def rows(k):
        return count_rows(os.path.join(target, files[k]))
    import csv as _csv
    with open(os.path.join(target, files["plc"]), encoding="utf-8") as fh:
        a = {r["facility_id"]: r["committed_limit"] for r in _csv.DictReader(fh)}
    with open(os.path.join(target, files["plc_rerun"]), encoding="utf-8") as fh:
        b = {r["facility_id"]: r["committed_limit"] for r in _csv.DictReader(fh)}
    assert set(a) == set(b)
    ndiff = sum(1 for k in a if a[k] != b[k])
    lines = [
        "REFERENCE DATA EXTRACT LOG",
        "Halstow Bank plc   quarter-end pack for Credit Risk Monitoring   as at 30/09/2026   compiled 08/10/2026 16:40",
        "",
        "job                          produced           rows     note",
        "EWS_MONTHEND_PUBLICATIONS    2026-10-02 06:14   %7d   publications 2022-09-30 to 2026-09-30" % rows("signals"),
        "GLEIF_LEI_CDF_SUBSET         2026-10-01 05:40   %7d   GLEIF concatenated file of 2026-09-30" % rows("lei"),
        "GLEIF_RR_CDF_SUBSET          2026-10-01 05:41   %7d   GLEIF concatenated file of 2026-09-30" % rows("rr"),
        "GLEIF_REPEX_SUBSET           2026-10-01 05:41   %7d   GLEIF concatenated file of 2026-09-30" % rows("repex"),
        "CREDIT_OBLIGOR_MASTER        2026-10-01 06:02   %7d" % rows("obligors"),
        "CREDIT_GROUP_REGISTER        2026-10-01 06:05   %7d" % (openpyxl.load_workbook(
            os.path.join(target, files["register"]))["Group register"].max_row - 4),
        "WATCH_LIST_HISTORY           2026-10-01 06:07   %7d   cases opened from 2020-01-01" % rows("watchlist"),
        "FACILITY_EXTRACT_HBPLC       2026-09-30 19:40   %7d   scheduled run" % rows("plc"),
        "FACILITY_EXTRACT_HBPLC       2026-09-30 23:05   %7d   rerun after limit amendments approved on 30/09 were "
        "posted following the scheduled run; the rerun is the record for 30/09" % rows("plc_rerun"),
        "FACILITY_EXTRACT_HBDAC       2026-10-07 11:52   %7d   Halstow Bank Ireland DAC, delivered after the Dublin "
        "ledger close; HBPLC extracts carry plc bookings only" % rows("dac"),
        "TREASURY_CLOSING_RATES       2026-09-30 16:20   %7d" % rows("fx"),
        "",
        "Control: HBPLC scheduled and rerun extracts hold the same facility list; %d committed limits differ." % ndiff,
        "Next quarter-end pack: 31/12/2026.",
    ]
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
