#!/usr/bin/env python3
"""task198 pack builder: cuts target/ from the clean truth in core.py.

Deterministic: fixed seeds, fixed document dates, reportlab in invariant mode, every workbook
re-zipped with fixed member timestamps, every file's mtime set to the in-fiction export stamp.
Two consecutive runs give byte-identical target/ trees.

    python3 task198/generator/build_pack.py
"""
import csv
import hashlib
import json
import os
import shutil
import sys
import zipfile
from datetime import date, datetime, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
sys.path.insert(0, HERE)

import core  # noqa: E402
from openpyxl import Workbook  # noqa: E402
import reportlab.rl_config as rl_config  # noqa: E402

rl_config.invariant = 1
from reportlab.lib.pagesizes import A4  # noqa: E402
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet  # noqa: E402
from reportlab.lib.units import mm  # noqa: E402
from reportlab.platypus import (PageBreak, Paragraph, SimpleDocTemplate, Spacer,  # noqa: E402
                                Table, TableStyle)
from reportlab.lib import colors  # noqa: E402

ORG = "Rathbroe Pension Services"
EXPORT_DT = datetime(2026, 4, 30, 18, 0, 0)
FIXED_ZIP_DT = (2026, 4, 30, 18, 0, 0)

ORBIT = {"RQ": "MS-RQ", "RS": "MS-RS", "TO": "MS-TO", "TI": "MS-TI", "DB": "MS-DB",
         "LO": "MS-LO", "DC": "MS-DC", "IS": "MS-IS", "CQ": "MS-CQ"}
GEMINI = {"RQ": "RQ", "RS": "RS", "TO": "TO", "TI": "TI", "DB": "DB",
          "LO": "LO", "DC": "RA", "IS": "IS", "CQ": "CQ"}
FORMER = {"DC": "Record amendments"}
STD_MIN = {k: v["mpc"] for k, v in core.QUEUES.items()}
TARGETS = {k: v["tgt"] for k, v in core.QUEUES.items()}
QNAME = {k: v["nm"] for k, v in core.QUEUES.items()}


# ---------------------------------------------------------------- deterministic writers
def _utime(path):
    ts = EXPORT_DT.timestamp()
    os.utime(path, (ts, ts))


def wr_csv(name, header, rows):
    p = os.path.join(TARGET, name)
    with open(p, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\r\n")
        w.writerow(header)
        w.writerows(rows)
    _utime(p)
    return p


def wr_json(name, obj):
    p = os.path.join(TARGET, name)
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, indent=2, sort_keys=False)
        fh.write("\n")
    _utime(p)
    return p


_ISO_RE = __import__("re").compile(rb"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z")
_FIXED_ISO = EXPORT_DT.strftime("%Y-%m-%dT%H:%M:%SZ").encode()


def _fix_zip(path):
    """Rewrite a zip with fixed member timestamps, member order preserved, and the workbook's own
    stated dates normalised to the export stamp: openpyxl writes dcterms:modified at save time
    whatever the properties say, which would leave the pack unreproducible."""
    with zipfile.ZipFile(path) as z:
        items = []
        for i in z.infolist():
            data = z.read(i.filename)
            if i.filename in ("docProps/core.xml", "docProps/app.xml"):
                data = _ISO_RE.sub(_FIXED_ISO, data)
                data = __import__("re").sub(rb"<Application>[^<]*</Application>",
                                            b"<Application>Microsoft Excel</Application>", data)
            items.append((i, data))
    tmp = path + ".tmp"
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as z:
        for info, data in items:
            ni = zipfile.ZipInfo(info.filename, date_time=FIXED_ZIP_DT)
            ni.compress_type = zipfile.ZIP_DEFLATED
            ni.external_attr = info.external_attr
            ni.create_system = 0
            z.writestr(ni, data)
    os.replace(tmp, path)


def wr_xlsx(name, sheets, props_title):
    """sheets: list of (sheet_name, list_of_rows)."""
    p = os.path.join(TARGET, name)
    wb = Workbook()
    wb.remove(wb.active)
    for sn, rows in sheets:
        ws = wb.create_sheet(title=sn[:31])
        for r in rows:
            ws.append(list(r))
    pr = wb.properties
    pr.creator = ORG
    pr.lastModifiedBy = ORG
    pr.created = EXPORT_DT
    pr.modified = EXPORT_DT
    pr.title = props_title
    pr.revision = None
    wb.save(p)
    _fix_zip(p)
    _utime(p)
    return p


_SS = getSampleStyleSheet()
BODY = ParagraphStyle("b", parent=_SS["BodyText"], fontName="Helvetica", fontSize=9.2,
                      leading=12.4, spaceAfter=5)
H1 = ParagraphStyle("h1", parent=BODY, fontName="Helvetica-Bold", fontSize=12.5, spaceAfter=8,
                    spaceBefore=2)
H2 = ParagraphStyle("h2", parent=BODY, fontName="Helvetica-Bold", fontSize=9.8, spaceAfter=4,
                    spaceBefore=7)
SMALL = ParagraphStyle("s", parent=BODY, fontSize=8.0, leading=10.2, textColor=colors.HexColor("#444444"))


def wr_pdf(name, title, blocks):
    """blocks: ('h1'|'h2'|'p'|'small'|'table'|'break', payload)."""
    p = os.path.join(TARGET, name)
    doc = SimpleDocTemplate(p, pagesize=A4, title=title, author=ORG, subject=title,
                            creator=ORG, leftMargin=22 * mm, rightMargin=20 * mm,
                            topMargin=20 * mm, bottomMargin=18 * mm)
    flow = []
    for kind, payload in blocks:
        if kind == "h1":
            flow.append(Paragraph(payload, H1))
        elif kind == "h2":
            flow.append(Paragraph(payload, H2))
        elif kind == "p":
            flow.append(Paragraph(payload, BODY))
        elif kind == "small":
            flow.append(Paragraph(payload, SMALL))
        elif kind == "break":
            flow.append(PageBreak())
        elif kind == "table":
            t = Table(payload, hAlign="LEFT")
            t.setStyle(TableStyle([
                ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8.4),
                ("FONT", (0, 1), (-1, -1), "Helvetica", 8.4),
                ("LINEBELOW", (0, 0), (-1, 0), 0.5, colors.black),
                ("LINEBELOW", (0, -1), (-1, -1), 0.4, colors.HexColor("#999999")),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]))
            flow.append(t)
            flow.append(Spacer(1, 5))
    doc.build(flow)
    _scrub_pdf(p)
    _utime(p)
    return p


def _scrub_pdf(path):
    """Rewrite the document information so the pack carries the organisation's own metadata and
    not the toolchain's (reduce-house-fixes H1)."""
    from pypdf import PdfReader, PdfWriter
    rd = PdfReader(path)
    w = PdfWriter()
    for pg in rd.pages:
        w.add_page(pg)
    md = {k: v for k, v in (rd.metadata or {}).items()
          if k in ("/Title", "/Subject", "/Author", "/Keywords")}
    md.update({"/Producer": ORG, "/Creator": ORG,
               "/CreationDate": "D:20260430180000+00'00'",
               "/ModDate": "D:20260430180000+00'00'"})
    w.add_metadata(md)
    with open(path, "wb") as fh:
        w.write(fh)


# ---------------------------------------------------------------- time of day and Irish local time
def _last_sunday(y, m):
    d = date(y, m, 31)
    while d.weekday() != 6:
        d -= timedelta(days=1)
    return d


def ie_offset(d, hhmm_local):
    """Irish local offset in hours for a local date (IST = UTC+1 between the last Sunday in
    March and the last Sunday in October)."""
    start, end = _last_sunday(d.year, 3), _last_sunday(d.year, 10)
    return 1 if start <= d < end else 0


def local_time(ref):
    """Deterministic local clock time for a case, from its own reference. About one case in
    sixty arrives through the member portal overnight, which is where the two platforms'
    stored conventions part company."""
    h = int(hashlib.sha1(ref.encode()).hexdigest()[:10], 16)
    if h % 60 == 0:
        return 0, 5 + (h // 60) % 50
    return 8 + (h // 7) % 10, (h // 13) % 60


def to_utc(d, hh, mm):
    off = ie_offset(d, (hh, mm))
    dt = datetime(d.year, d.month, d.day, hh, mm) - timedelta(hours=off)
    return dt


# ---------------------------------------------------------------- the pack
def fq(d):
    return core.fiscal_quarter(d)


def build():
    if os.path.isdir(TARGET):
        shutil.rmtree(TARGET)
    os.makedirs(TARGET)

    cases, panel = core.build()
    cases = cases + core.april_tail()
    core.integerise(cases)
    sch = core.assign_schemes(cases)
    part = {c: p for c, nm, w, p, m in sch}
    for i, c in enumerate(cases):
        c["part"] = part[c["scheme"]]
    cases.sort(key=lambda c: (c["rec"], c["code"], c["scheme"]))
    for i, c in enumerate(cases):
        c["gref"] = "G%07d" % (412837 + i * 3)
        c["oref"] = "RPS-%d-%06d" % (c["rec"].year, 100000 + i * 7 % 899999)
        c["member"] = "M-%07d" % (1000003 + (int(hashlib.sha1(c["gref"].encode()).hexdigest()[:9], 16) % 886421))

    charges, big = core.billing_lines(cases, sch)
    reg, tru = core.register_and_trustee()

    # ---- 1,2 the case record, two platforms either side of the 1 April 2024 cutover
    gem_rows, orb_rows = [], []
    for c in cases:
        hh, mm = local_time(c["gref"])
        rec_local = "%02d/%02d/%d %02d:%02d" % (c["rec"].day, c["rec"].month, c["rec"].year, hh, mm)
        rec_utc = to_utc(c["rec"], hh, mm).strftime("%Y-%m-%dT%H:%M:%SZ")
        if c["ans"] is not None:
            ah, am_ = local_time(c["gref"] + "a")
            ah = max(9, min(17, ah))
            ans_local = "%02d/%02d/%d %02d:%02d" % (c["ans"].day, c["ans"].month, c["ans"].year, ah, am_)
            ans_utc = to_utc(c["ans"], ah, am_).strftime("%Y-%m-%dT%H:%M:%SZ")
        else:
            ans_local, ans_utc = "", ""
        pre = c["rec"] < core.MIGRATION
        migrated = pre and (c["ans"] is None or c["ans"] >= core.MIGRATION)
        if pre:
            gem_rows.append([c["gref"], GEMINI[c["code"]], c["scheme"], c["member"], rec_local,
                             "" if migrated else ans_local,
                             "TRF" if migrated else "CLSD", c["stop"]])
        if (not pre) or migrated:
            st = "ANSWERED" if c["ans"] is not None else ("AWAITING_MEMBER" if c["stop"] > 0 else "IN_PROGRESS")
            orb_rows.append([c["oref"], ORBIT[c["code"]], c["scheme"], c["member"], rec_utc,
                             ans_utc, st, c["stop"], c["gref"] if migrated else ""])
    wr_csv("member_cases_gemini_fy2023_fy2024.csv",
           ["case_no", "queue", "scheme", "member_ref", "received", "closed", "status", "member_days"],
           gem_rows)
    wr_csv("member_cases_orbit_fy2025_fy2026.csv",
           ["case_reference", "queue_code", "scheme_code", "member_id", "received_utc",
            "answered_utc", "case_status", "clock_stop_days", "legacy_case_ref"], orb_rows)

    # ---- 3 queue reference
    wr_csv("queue_reference.csv",
           ["orbit_queue_code", "gemini_queue_code", "queue_name", "former_queue_name", "operations_centre"],
           [[ORBIT[k], GEMINI[k], QNAME[k], FORMER.get(k, ""),
             "Dublin" if k in ("RQ", "RS", "LO", "CQ") else "Athlone"] for k in core.QUEUES])

    # ---- 4 status reference, as Orbit exports it
    wr_json("case_status_reference.json", {
        "platform": "Orbit", "export_date": "2026-04-30",
        "statuses": [
            {"code": "ANSWERED", "platform": "Orbit", "answered": True, "clock": "stopped",
             "note": "substantive response issued"},
            {"code": "IN_PROGRESS", "platform": "Orbit", "answered": False, "clock": "running"},
            {"code": "AWAITING_MEMBER", "platform": "Orbit", "answered": False, "clock": "suspended",
             "note": "days suspended are carried in clock_stop_days"},
            {"code": "CLSD", "platform": "Gemini", "answered": True, "clock": "stopped"},
            {"code": "TRF", "platform": "Gemini", "answered": False, "clock": "running",
             "note": "case open at the 1 April 2024 platform cutover and carried to Orbit; the Orbit "
                     "record holds the case from that date and quotes the Gemini case number"},
        ],
        "clock_stop_field": {"Gemini": "member_days", "Orbit": "clock_stop_days",
                             "unit": "whole working days"}})

    # ---- 5 working-day calendar
    hol = sorted(d for d in core.HOL if date(2022, 1, 1) <= d <= date(2026, 12, 31))
    nm = {"01-01": "New Year's Day", "02-02": "St Brigid's Day", "02-03": "St Brigid's Day",
          "02-05": "St Brigid's Day", "02-06": "St Brigid's Day", "03-17": "St Patrick's Day",
          "03-18": "St Patrick's Day", "12-25": "Christmas Day", "12-26": "St Stephen's Day",
          "12-27": "St Stephen's Day (substitute)", "12-28": "St Stephen's Day (substitute)",
          "01-02": "New Year's Day (substitute)", "01-03": "New Year's Day (substitute)"}
    def hname(d):
        k = "%02d-%02d" % (d.month, d.day)
        if k in nm:
            return nm[k]
        return {3: "Good Friday", 4: "Easter Monday", 5: "May public holiday",
                6: "June public holiday", 8: "August public holiday",
                10: "October public holiday"}.get(d.month, "public holiday")
    wr_csv("public_holidays_ie_2022_2026.csv", ["holiday_date", "holiday_name"],
           [[d.isoformat(), hname(d)] for d in hol])

    # ---- 6 rostered capacity, sheets changing basis at the FY2025 planning change
    sheets = []
    for fy in (2023, 2024):
        rows = [["Rostered hours by queue and month, FY%d" % fy], [],
                ["queue_code", "month", "rostered_hours"]]
        for k in core.QUEUES:
            pos = core.QUEUES[k]["pos"][fy - 2023]
            for qi in range(4):
                s_, e_ = core.qbounds((fy - 2023) * 4 + qi)
                months = []
                d = s_
                while d <= e_:
                    if (d.year, d.month) not in months:
                        months.append((d.year, d.month))
                    d += timedelta(days=1)
                for (yy, mo) in months:
                    wd = sum(1 for x in core.WD if x.year == yy and x.month == mo)
                    rows.append([ORBIT[k], "%d-%02d" % (yy, mo), round(pos * 7.0 * wd, 1)])
        sheets.append(("FY%d" % fy, rows))
    for fy in (2025, 2026):
        rows = [["Rostered positions (FTE) by queue and financial quarter, FY%d" % fy], [],
                ["queue_code", "financial_quarter", "rostered_fte"]]
        for k in core.QUEUES:
            pos = core.QUEUES[k]["pos"][fy - 2023]
            for qi in range(1, 5):
                rows.append([ORBIT[k], "FY%d Q%d" % (fy, qi), float(pos)])
        sheets.append(("FY%d" % fy, rows))
    sheets.append(("Notes", [
        ["Member operations rostered capacity record"], [],
        ["Owner", "Resource Planning, Member Operations"],
        ["Refreshed", "2026-04-17"],
        ["Basis to FY2024", "rostered hours by month"],
        ["Basis from FY2025", "rostered positions (FTE) by financial quarter"],
        ["Conversion", "one rostered position is 7.0 rostered hours a working day"],
        ["Financial year", "1 April to 31 March"], [],
        ["Note", "MS-DC carried nine temporary positions from 1 April 2023 to 31 March 2025 for the "
                 "member data remediation programme. The temporary positions and the programme both "
                 "ended on 31 March 2025."],
        ["Note", "Rostered positions exclude the operations management team and the quality team."],
    ]))
    wr_xlsx("rostered_capacity_by_queue.xlsx", sheets, "Rostered capacity by queue")

    # ---- 7 monitoring export (context artifact), computed from the case record
    mon = {}
    for c in cases:
        if c["ans"] is None:
            continue
        cy, cq = c["ans"].year, (c["ans"].month - 1) // 3 + 1
        k = (ORBIT[c["code"]], cy, cq)
        a = mon.setdefault(k, [0, 0])
        a[0] += 1
        if c["elapsed_wd"] > c["tgt"]:
            a[1] += 1
    rows = [["queue_code", "calendar_quarter", "cases_closed", "closed_outside_target", "outside_target_pct"]]
    for (qc, cy, cq) in sorted(mon):
        if (cy, cq) < (2023, 1) or (cy, cq) > (2026, 1):
            continue
        if (cy, cq) == (2024, 2):
            continue
        n, late = mon[(qc, cy, cq)]
        rows.append([qc, "%dQ%d" % (cy, cq), n, late, round(100.0 * late / n, 1)])
    wr_xlsx("service_monitoring_export.xlsx", [
        ("Performance", rows),
        ("Notes", [["Member service performance export"], [],
                   ["Source", "Orbit and Gemini case extracts"],
                   ["Owner", "Management Information, Member Operations"],
                   ["Refreshed", "2026-04-24"],
                   ["Basis", "cases closed in the calendar quarter shown"],
                   ["Measure", "elapsed working days from receipt to the response issuing"],
                   ["Note", "Elapsed working days are not reduced by days a case stood with the member."],
                   ["Note", "2024Q2 is not available: the reporting feed was rebuilt at the platform cutover."],
                   ["Note", "2026Q1 is provisional and will be restated when the quarter is signed off."],
                   ["Note", "Queues are listed in queue code order. The export does not rank queues."]])],
        "Member service performance export")

    # ---- 8 scheme charges (ask 2)
    crows = []
    for i, r in enumerate(charges):
        crows.append(["SC%06d" % (204411 + i * 13), r["billed"].isoformat(), r["scheme"],
                      ORBIT[r["queue"]],
                      "consolidated monthly" if r["consolidated"] else "per case",
                      "%.2f" % r["fee"],
                      "2025-26 R2" if r["billed"] >= core.RATE_SWITCH else "2025-26 R1", "EUR"])
    wr_csv("scheme_charges_fy2026.csv",
           ["charge_ref", "charge_date", "scheme_code", "queue_code", "statement_type",
            "charge_eur", "rate_period", "currency"], crows)

    # ---- 9 schemes register (ask 3). return_basis is generator truth and is not shipped.
    wr_csv("schemes_register_2026.csv",
           ["scheme_code", "scheme_name", "sponsor", "active_members"],
           [[r["scheme_code"], r["scheme_name"], r["sponsor"], r["active_members"]] for r in reg])

    # ---- 10 distractor: telephony
    trow = []
    for k in core.QUEUES:
        for mo in range(12):
            y = 2025 + (1 if mo >= 9 else 0)
            m = (mo + 4 - 1) % 12 + 1
            h = int(hashlib.sha1(("t%s%d%d" % (k, y, m)).encode()).hexdigest()[:8], 16)
            offered = 300 + h % 900 + 40 * (ORBIT[k] in ("MS-CQ", "MS-LO")) * 9
            ans30 = int(offered * (0.62 + (h // 97) % 24 / 100.0))
            aban = int(offered * (0.04 + (h // 311) % 9 / 100.0))
            trow.append([ORBIT[k], "%d-%02d" % (y, m), offered, ans30, aban,
                         round(100.0 * aban / offered, 1), 18 + (h // 53) % 70])
    wr_csv("telephony_statistics_fy2026.csv",
           ["queue_code", "month", "calls_offered", "answered_within_30s", "calls_abandoned",
            "abandon_pct", "asa_seconds"], trow)

    # ---- 11 distractor: satisfaction survey
    srows = [["queue_code", "financial_quarter", "responses", "satisfied_pct", "mean_score_1_5"]]
    for k in core.QUEUES:
        for q in range(1, 5):
            h = int(hashlib.sha1(("s%s%d" % (k, q)).encode()).hexdigest()[:8], 16)
            n = 40 + h % 260
            srows.append([ORBIT[k], "FY2026 Q%d" % q, n, round(68 + (h // 71) % 240 / 10.0, 1),
                          round(3.4 + (h // 37) % 130 / 100.0, 2)])
    wr_xlsx("member_satisfaction_survey_fy2026.xlsx", [
        ("Results", srows),
        ("Notes", [["Member satisfaction survey, FY2026"], [],
                   ["Owner", "Member Experience"], ["Refreshed", "2026-04-21"],
                   ["Method", "emailed to members whose case closed in the quarter, one invitation per member"],
                   ["Response rate", "voluntary; results are not weighted"]])],
        "Member satisfaction survey FY2026")

    # ---- 12 data dictionary
    dd = [
        ["member_cases_gemini_fy2023_fy2024.csv", "case_no", "Gemini case number. One row is one case received on the Gemini platform."],
        ["member_cases_gemini_fy2023_fy2024.csv", "received", "Date and time the case was received, Irish local time, dd/mm/yyyy hh:mm."],
        ["member_cases_gemini_fy2023_fy2024.csv", "closed", "Date and time the response issued, Irish local time. Empty where the case was not closed on Gemini."],
        ["member_cases_gemini_fy2023_fy2024.csv", "member_days", "Whole working days the case stood awaiting information from the member."],
        ["member_cases_orbit_fy2025_fy2026.csv", "case_reference", "Orbit case reference. One row is one case held on Orbit."],
        ["member_cases_orbit_fy2025_fy2026.csv", "received_utc", "Date and time the case was received, UTC."],
        ["member_cases_orbit_fy2025_fy2026.csv", "answered_utc", "Date and time the response issued, UTC. Empty where no response has issued."],
        ["member_cases_orbit_fy2025_fy2026.csv", "clock_stop_days", "Whole working days the case stood awaiting information from the member."],
        ["member_cases_orbit_fy2025_fy2026.csv", "legacy_case_ref", "Gemini case number where the case was carried over at the 1 April 2024 cutover. Empty for cases first received on Orbit."],
        ["queue_reference.csv", "former_queue_name", "Name the queue was reported under before FY2025."],
        ["rostered_capacity_by_queue.xlsx", "rostered_fte", "Positions rostered to the queue for the financial quarter."],
        ["schemes_register_2026.csv", "active_members", "Active members as returned by the sponsor."],
        ["schemes_register_2026.csv", "scheme_code", "One row is one participating scheme. Cases are recorded against a scheme code; the Rathbroe Master Trust's administrative sub-codes MT-CEN, MT-S01, MT-S02, MT-S03 and MT-S04 are sections of the one participating scheme RMT-000."],
        ["scheme_charges_fy2026.csv", "charge_eur", "Amount charged on the line, euro."],
        ["scheme_charges_fy2026.csv", "statement_type", "Whether the scheme is charged on a consolidated monthly statement or a line per case."],
        ["telephony_statistics_fy2026.csv", "calls_offered", "Calls presented to the queue's agent group in the month. Telephony is a separate channel and is not case work."],
        ["member_satisfaction_survey_fy2026.xlsx", "satisfied_pct", "Share of respondents answering satisfied or very satisfied."],
    ]
    wr_csv("data_dictionary.csv", ["file", "field", "definition"], dd)

    # ---- 13 provenance
    man = [
        ["member_cases_gemini_fy2023_fy2024.csv", "Gemini case extract", "cases received 1 Apr 2022 to 31 Mar 2024",
         "cases first received on Orbit", "Gemini decommissioned extract, pulled 2026-04-30", "internal"],
        ["member_cases_orbit_fy2025_fy2026.csv", "Orbit case extract", "cases received 1 Apr 2024 to 30 Apr 2026, and cases carried over at the cutover",
         "cases closed on Gemini before the cutover", "Orbit, pulled 2026-04-30", "internal"],
        ["queue_reference.csv", "queue master", "the nine member-service queues", "closed queues", "Orbit reference data", "internal"],
        ["case_status_reference.json", "status reference", "case statuses on both platforms", "workflow sub-states", "Orbit reference data", "internal"],
        ["public_holidays_ie_2022_2026.csv", "public holiday calendar", "2022 to 2026", "company closure days", "Workplace Relations Commission listings", "public"],
        ["rostered_capacity_by_queue.xlsx", "rostered capacity record", "FY2023 to FY2026", "overtime and agency cover", "Resource Planning", "internal"],
        ["service_monitoring_export.xlsx", "performance export", "2023Q1 to 2026Q1", "2024Q2; cases not yet closed", "Management Information", "internal"],
        ["scheme_charges_fy2026.csv", "scheme charging extract", "charges raised in FY2026", "credit notes and disbursements", "Billing", "internal"],
        ["schemes_register_2026.csv", "participating scheme register", "schemes administered at 31 Mar 2026", "schemes that left before 1 Apr 2025", "Scheme Secretariat", "internal"],
        ["telephony_statistics_fy2026.csv", "telephony statistics", "FY2026 by month", "web and email contact", "Contact Centre", "internal"],
        ["member_satisfaction_survey_fy2026.xlsx", "satisfaction survey", "FY2026 by quarter", "non-respondents", "Member Experience", "internal"],
        ["data_dictionary.csv", "data dictionary", "fields of the extracts", "derived fields", "Data Services", "internal"],
        ["service_assurance_framework_2026.pdf", "assurance framework, issue 3", "member service monitoring and process review", "complaints handling", "Member Operations Board, 12 Jan 2026", "internal"],
        ["member_service_standard_2025.pdf", "service standard, issue 6", "targets and the service clock from 1 Apr 2025", "telephony and web service levels", "Member Operations, 1 Apr 2025", "internal"],
        ["work_measurement_standard_2022.pdf", "work measurement standard", "standard minutes by case type", "project and bulk work", "Resource Planning, 3 Oct 2022", "internal"],
        ["fee_schedule_2025.pdf", "fee schedule 2025-26", "per case charges and statement terms", "project work and disbursements", "Billing, 1 Apr 2025", "internal"],
        ["trustee_report_membership_2026.pdf", "trustee membership statement", "active membership by scheme at 31 Mar 2026", "deferred and pensioner members", "Scheme Secretariat, 24 Apr 2026", "internal"],
        ["pensions_authority_letter_2026.pdf", "supervisory correspondence", "service improvement response required by 31 Jul 2026", "the individual complaint files", "The Pensions Authority, 17 Apr 2026", "received"],
    ]
    wr_csv("export_manifest.csv",
           ["file", "what_it_is", "covers", "omits", "source_and_pull", "licence"], man)

    # ---- 14 the service assurance framework: the pin
    wr_pdf("service_assurance_framework_2026.pdf",
           "Member Operations Service Assurance Framework", [
        ("h1", "%s<br/>Member Operations Service Assurance Framework" % ORG),
        ("small", "Issue 3. Approved by the Member Operations Board, 12 January 2026. "
                  "Owner: Head of Member Operations. Next review January 2027."),
        ("h2", "1 Purpose and scope"),
        ("p", "1.1 This framework sets out how member operations monitors the service it gives to "
              "members of the schemes it administers, and how it selects work for process review. It "
              "applies to the nine member-service case queues listed in the queue master."),
        ("p", "1.2 It sits under the Member Service Standard, which sets the target for each queue and "
              "the rules of the service clock, and alongside the Work Measurement Standard, which sets "
              "the standard minutes for each case type."),
        ("h2", "2 Definitions"),
        ("p", "2.1 The financial year runs from 1 April to 31 March. A financial quarter is a quarter of "
              "that year, so FY2026 Q1 is April to June 2025. A financial year is named for the calendar "
              "year in which it ends."),
        ("p", "2.2 A case queue is a team that handles one case type for members. A case belongs to the "
              "queue that held it when the response issued."),
        ("p", "2.3 A participating scheme is a scheme listed in the participating scheme register. A "
              "scheme may be administered in sections under their own codes."),
        ("h2", "3 Monitoring"),
        ("p", "3.1 Performance against the Member Service Standard is reported each quarter to the "
              "Member Operations Board on the basis set out in the performance export."),
        ("p", "3.2 The Board is notified where a queue falls below the ceiling in clause 4.1 of the "
              "Member Service Standard in two consecutive quarters."),
        ("h2", "4 Process review"),
        ("p", "4.1 One full process re-engineering review is commissioned in each half year. It is "
              "carried out by an external operations practice and is directed at a single case queue."),
        ("p", "4.2 The review candidate for a half year is the case queue whose share of cases received "
              "in the preceding financial year that were answered later than the target set for that "
              "queue stands furthest above, in percentage points, the share the same queue reached in "
              "those of its quarters in the three financial years before that one which carried the same "
              "offered load. Every case received in the financial year is counted, including cases not "
              "yet answered at the extract date. The unit is the case queue."),
        ("p", "4.3 Offered load is measured in positions-equivalents on the standard minutes set in the "
              "Work Measurement Standard. Staffed positions for a quarter are the positions rostered to "
              "the queue for that quarter in the rostered capacity record."),
        ("p", "4.4 The candidate is recorded in the half year's service improvement response together "
              "with its own measured share for the year and the cases it received."),
        ("h2", "5 Governance"),
        ("p", "5.1 This framework is approved by the Member Operations Board and reviewed annually. "
              "Changes to clause 4.2 require the Board's approval."),
        ("small", "Approved: Peadar MacVeagh, Head of Member Operations, 12 January 2026."),
    ])

    # ---- 15 the member service standard
    tgt_tbl = [["Queue", "Queue code", "Target (working days)"]] + \
              [[QNAME[k], ORBIT[k], str(TARGETS[k])] for k in core.QUEUES]
    wr_pdf("member_service_standard_2025.pdf", "Member Service Standard", [
        ("h1", "%s<br/>Member Service Standard" % ORG),
        ("small", "Issue 6. Effective 1 April 2025. Owner: Head of Member Operations. "
                  "Supersedes issue 5 of 1 April 2022."),
        ("h2", "1 Scope"),
        ("p", "1.1 This standard sets the service we hold ourselves to on member-service case work, and "
              "the rules by which the time taken on a case is measured."),
        ("h2", "2 Receipt"),
        ("p", "2.1 A case is received when the request reaches us by any channel, including the member "
              "portal. The date of receipt is the date in Irish local time on which it reaches us."),
        ("h2", "3 The service clock"),
        ("p", "3.1 The service clock runs in working days and starts on the working day after receipt."),
        ("p", "3.2 The target for each queue is:"),
        ("table", tgt_tbl),
        ("p", "3.3 A working day is a day other than a Saturday, a Sunday or a public holiday in the "
              "State."),
        ("p", "3.4 Days on which a case stands awaiting information from the member, or from an adviser "
              "acting for the member, are excluded from the clock. The whole working days excluded are "
              "recorded against the case."),
        ("p", "3.5 A case is answered when the substantive response issues. An acknowledgement is not a "
              "response."),
        ("p", "3.6 A case that has not been answered by the date the case record is extracted counts as "
              "answered later than target where the days its clock has run by that date already exceed "
              "the target for its queue, and counts as within target otherwise."),
        ("h2", "4 The ceiling"),
        ("p", "4.1 Not less than 95 per cent of the cases a queue receives in a financial quarter are to "
              "be answered within the target for that queue."),
        ("p", "4.2 A quarter below the ceiling is reported to the Member Operations Board with the "
              "queue's own account of the cause."),
        ("small", "Issued by Member Operations, 1 April 2025."),
    ])

    # ---- 16 the work measurement standard
    wm = [["Queue", "Queue code", "Standard minutes per case"]] + \
         [[QNAME[k], ORBIT[k], str(STD_MIN[k])] for k in core.QUEUES]
    wr_pdf("work_measurement_standard_2022.pdf", "Work Measurement Standard", [
        ("h1", "%s<br/>Work Measurement Standard, Member Operations" % ORG),
        ("small", "2022 study. Issued 3 October 2022. Owner: Resource Planning. "
                  "Standard minutes are reviewed when a case type's process changes."),
        ("h2", "1 The study"),
        ("p", "1.1 Standard minutes were measured in the 2022 study by observation and by timed sampling "
              "across both operations centres, on 2,840 cases over eleven weeks."),
        ("p", "1.2 A standard minute is a minute of handling time at standard performance, including "
              "contingency and personal allowances."),
        ("h2", "2 Standard minutes"),
        ("table", wm),
        ("h2", "3 Productive time"),
        ("p", "3.1 A rostered position is taken to give 420 productive minutes on a working day."),
        ("p", "3.2 The net productive factor is 0.88. Productive minutes available to case work on a "
              "working day are therefore 420 multiplied by 0.88."),
        ("p", "3.3 Offered load in positions-equivalents for a queue in a period is the cases received "
              "multiplied by the standard minutes for the queue, divided by the productive minutes "
              "available to one position across the working days of the period."),
        ("small", "Naoise Daniels, Resource Planning, 3 October 2022."),
    ])

    # ---- 17 the fee schedule (ask 2 referee)
    fee_tbl = [["Case type", "Queue code", "Per case to 30 Sep 2025 (EUR)", "Per case from 1 Oct 2025 (EUR)"]] + \
              [[QNAME[k], ORBIT[k], "%.2f" % core.FEE[k][0], "%.2f" % core.FEE[k][1]]
               for k in core.CHARGEABLE]
    wr_pdf("fee_schedule_2025.pdf", "Scheme Administration Fee Schedule", [
        ("h1", "%s<br/>Scheme Administration Fee Schedule 2025-26" % ORG),
        ("small", "Effective 1 April 2025. Owner: Billing. Rate period R1 runs to 30 September 2025 and "
                  "rate period R2 from 1 October 2025."),
        ("h2", "1 Case charges"),
        ("p", "1.1 The following case types are charged to the scheme per case on the response issuing. "
              "Rate period R1 applies where the response issued on or before 30 September 2025 and rate "
              "period R2 where it issued on or after 1 October 2025."),
        ("table", fee_tbl),
        ("p", "1.2 Leaver options, investment switches and contribution queries are within the core "
              "administration fee and are not charged per case."),
        ("h2", "2 Statements"),
        ("p", "2.1 A scheme is charged either on a consolidated monthly statement or on a line per case, "
              "as recorded against the charge."),
        ("p", "2.2 A scheme on a consolidated monthly statement is charged one line for each case type in "
              "each month, for the cases of that type whose response issued in the month, at the rate "
              "period in force on the charge date."),
        ("p", "2.3 Charges are raised in the month the response issues. A response issuing in the last "
              "days of a month may be charged in the month following."),
        ("h2", "3 Other charges"),
        ("p", "3.1 Project work, bulk exercises and disbursements are charged separately and are not in "
              "the case charging extract."),
        ("small", "Billing, 1 April 2025."),
    ])

    # ---- 18 the trustee membership statement (ask 3 referee)
    hdr = ["Scheme code", "Scheme", "Active, contributing", "Active, contributions suspended"]
    tru_tbl = [hdr] + [[t["scheme_code"], t["scheme_name"],
                        "{:,}".format(t["active_contributing"]),
                        "{:,}".format(t["active_suspended"])] for t in tru[:26]]
    tru_tbl2 = [hdr] + [[t["scheme_code"], t["scheme_name"],
                         "{:,}".format(t["active_contributing"]),
                         "{:,}".format(t["active_suspended"])] for t in tru[26:]]
    wr_pdf("trustee_report_membership_2026.pdf", "Active membership at 31 March 2026", [
        ("h1", "%s<br/>Administered schemes: active membership at 31 March 2026" % ORG),
        ("small", "Prepared for the trustees of the administered schemes. Issued 24 April 2026. "
                  "Owner: Scheme Secretariat."),
        ("p", "Active membership is stated for each scheme separately, as held on the administration "
              "record at 31 March 2026, and is split by contribution status: a member whose "
              "contributions are suspended remains an active member of the scheme. Where a sponsoring "
              "employer returns membership for more than one of its schemes on a single return, the "
              "figures below are the per-scheme split held on the administration record rather than the "
              "figure as returned."),
        ("table", tru_tbl),
        ("break", None),
        ("table", tru_tbl2),
        ("small", "Scheme Secretariat, 24 April 2026."),
    ])

    # ---- 19 the Pensions Authority letter (the forcing document)
    wr_pdf("pensions_authority_letter_2026.pdf", "Correspondence: service improvement response", [
        ("h1", "The Pensions Authority"),
        ("small", "Verschoyle House, 28-30 Lower Mount Street, Dublin 2. 17 April 2026. "
                  "Our reference: SUP/2026/0418."),
        ("p", "The Head of Member Operations<br/>%s" % ORG),
        ("h2", "Member service case handling: service improvement response"),
        ("p", "In the twelve months to March 2026 the Financial Services and Pensions Ombudsman upheld "
              "three complaints against the firm in which delay in handling a member's case was a "
              "ground of the complaint (FSPO references 2025-04711, 2025-09322 and 2026-00841). The "
              "firm has already given the Ombudsman its account of each case."),
        ("p", "The Authority is not minded to take further action on the individual cases. We do require "
              "the firm to satisfy itself that its own service assurance arrangements are working, and "
              "to tell us what it will change."),
        ("p", "Please send us, by 31 July 2026, a service improvement response covering the financial "
              "year ended 31 March 2026. The response should identify the case queue selected for the "
              "firm's next full process re-engineering review under clause 4 of its own Member "
              "Operations Service Assurance Framework, and should set out that queue's own measured "
              "performance for the year ended 31 March 2026."),
        ("p", "The Authority does not prescribe the basis on which the firm selects the queue. We will "
              "read the response against the framework the firm has approved."),
        ("small", "Janine Masterson<br/>Supervision, The Pensions Authority"),
    ])

    files = sorted(os.listdir(TARGET))
    return cases, panel, sch, charges, reg, tru, files


if __name__ == "__main__":
    cases, panel, sch, charges, reg, tru, files = build()
    print("target/ built: %d files" % len(files))
    for f in files:
        print("   %9d  %s" % (os.path.getsize(os.path.join(TARGET, f)), f))
