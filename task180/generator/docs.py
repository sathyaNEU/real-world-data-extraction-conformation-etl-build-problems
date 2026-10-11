"""Writers for the task180 documents and workbooks, plus the metadata scrub."""
import csv
import datetime as dt
import os
import re
import shutil
import zipfile

import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Font

import world as W
import hist

PATCH_NAME = {p[0]: p[1] for p in W.PATCHES}


def _header(ws, lines, ncols):
    for i, line in enumerate(lines, start=1):
        ws.cell(row=i, column=1, value=line)
        if i == 1:
            ws.cell(row=i, column=1).font = Font(bold=True)
    return len(lines) + 2


def write_register(path, w, exchanges):
    wb = Workbook()
    ws = wb.active
    ws.title = "Supplies"
    r = _header(ws, ["Corran Energy | Supply point register extract (CIS)",
                     "Run 07/12/2026 05:52 | north of Scotland GSP group _P | domestic only",
                     "One row per supply number (MPAN core) registered to Corran on the run date."], 12)
    cols = ["mpan_core", "uprn", "rp_patch", "account_ref", "payment_method", "profile_class", "ssc",
            "ssc_description", "related_mpan", "meter_type", "meter_serial", "energised_on"]
    for j, c in enumerate(cols, 1):
        ws.cell(row=r, column=j, value=c).font = Font(bold=True)
    rng = np.random.default_rng(W.SEED + 23)
    cur_acct = {}
    for p in w["premises"]:
        live = [a for a in p["accounts"] if a[2] is None]
        cur_acct[p["uprn"]] = live[0][0] if live else p["accounts"][-1][0]
    e7_single = {}
    for s in w["supplies"]:
        prem_heat = s.get("related") is not None
        if s["kind"] == "heat":
            pc, ssc, desc = 2, "0244", "Heating only, off-peak (related MPAN)"
        elif prem_heat:
            pc, ssc, desc = 2, "0151", "Economy 7, two rate"
        else:
            if s["uprn"] not in e7_single:
                e7_single[s["uprn"]] = rng.random() < 0.22
            pc, ssc, desc = (2, "0151", "Economy 7, two rate") if e7_single[s["uprn"]] else (1, "0393", "Unrestricted")
        prem = next(p for p in w["premises"] if p["uprn"] == s["uprn"]) if False else None
        s["_pc"] = pc
    prem_by = {p["uprn"]: p for p in w["premises"]}
    rows = []
    for s in w["supplies"]:
        p = prem_by[s["uprn"]]
        if s["kind"] == "heat":
            pc, ssc, desc = 2, "0244", "Heating only, off-peak (related MPAN)"
        elif s.get("related"):
            pc, ssc, desc = 2, "0151", "Economy 7, two rate"
        elif e7_single.get(s["uprn"]):
            pc, ssc, desc = 2, "0151", "Economy 7, two rate"
        else:
            pc, ssc, desc = 1, "0393", "Unrestricted"
        mt = "SMETS2" if rng.random() < 0.83 else "SMETS1"
        en = dt.date(2004, 1, 1) + dt.timedelta(int(rng.integers(0, 6900)))
        rows.append([s["mpan"], p["uprn"], p["patch"], cur_acct[p["uprn"]],
                     "Prepayment" if p["prepay"] else "Credit", pc, ssc, desc, s.get("related", ""),
                     mt, s["current_serial"], en])
    rows.sort(key=lambda x: (x[2], x[1], x[0]))
    for i, row in enumerate(rows, start=r + 1):
        for j, v in enumerate(row, 1):
            c = ws.cell(row=i, column=j, value=v)
            if isinstance(v, dt.date):
                c.number_format = "dd/mm/yyyy"
            if j in (1, 9):
                c.number_format = "@"
    ws2 = wb.create_sheet("Meter exchanges")
    r2 = _header(ws2, ["Meter exchanges completed 01/10/2024 to run date",
                       "Final and initial register reads as keyed by the metering agent on the day."], 6)
    cols2 = ["mpan_core", "exchange_date", "removed_serial", "final_read_kwh", "fitted_serial", "initial_read_kwh"]
    for j, c in enumerate(cols2, 1):
        ws2.cell(row=r2, column=j, value=c).font = Font(bold=True)
    for i, e in enumerate(sorted(exchanges, key=lambda e: e["exchange_date"]), start=r2 + 1):
        vals = [e["mpan_core"], e["exchange_date"], e["removed_serial"], e["final_read_kwh"],
                e["fitted_serial"], e["initial_read_kwh"]]
        for j, v in enumerate(vals, 1):
            c = ws2.cell(row=i, column=j, value=v)
            if isinstance(v, dt.date):
                c.number_format = "dd/mm/yyyy"
    ws3 = wb.create_sheet("Account history")
    r3 = _header(ws3, ["Billing accounts at each premises, opened and closed dates",
                       "Account type Occupier is the deemed account raised while a premises has no named customer."], 5)
    cols3 = ["account_ref", "uprn", "opened_on", "closed_on", "account_type"]
    for j, c in enumerate(cols3, 1):
        ws3.cell(row=r3, column=j, value=c).font = Font(bold=True)
    arows = []
    for p in w["premises"]:
        for a in p["accounts"]:
            arows.append([a[0], p["uprn"], a[1], a[2], "Occupier" if a[3] == "occupier" else "Named"])
    arows.sort(key=lambda x: (x[1], x[2]))
    for i, row in enumerate(arows, start=r3 + 1):
        for j, v in enumerate(row, 1):
            c = ws3.cell(row=i, column=j, value=v)
            if isinstance(v, dt.date):
                c.number_format = "dd/mm/yyyy"
    wb.save(path)


def write_appeals(path, rows):
    wb = Workbook()
    ws = wb.active
    ws.title = "Register"
    r = _header(ws, ["Revenue Protection | tamper findings appealed by customers",
                     "Maintained by the RP casework desk. One row per appeal."], 6)
    cols = ["appeal_ref", "job_reference", "uprn", "lodged_on", "decision", "decided_on"]
    for j, c in enumerate(cols, 1):
        ws.cell(row=r, column=j, value=c).font = Font(bold=True)
    for i, row in enumerate(rows, start=r + 1):
        for j, v in enumerate(row, 1):
            c = ws.cell(row=i, column=j, value=v)
            if isinstance(v, dt.date):
                c.number_format = "dd/mm/yyyy"
    wb.save(path)


def write_rota(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Team"
    r = _header(ws, ["RP field team | rota for January to March 2027", "Prepared 30/11/2026, Inverness depot"], 3)
    for j, c in enumerate(["officer", "grade", "field_start"], 1):
        ws.cell(row=r, column=j, value=c).font = Font(bold=True)
    for i, (n, g, s) in enumerate(hist.TEAM, start=r + 1):
        ws.cell(row=i, column=1, value=n)
        ws.cell(row=i, column=2, value=g)
        c = ws.cell(row=i, column=3, value=s)
        c.number_format = "dd/mm/yyyy"
    ws2 = wb.create_sheet("Leave and training")
    r2 = _header(ws2, ["Booked absences, Q1 2027"], 3)
    for j, c in enumerate(["officer", "date", "code"], 1):
        ws2.cell(row=r2, column=j, value=c).font = Font(bold=True)
    for i, (n, d, code) in enumerate(sorted(hist.LEAVE, key=lambda x: (x[1], x[0])), start=r2 + 1):
        ws2.cell(row=i, column=1, value=n)
        c = ws2.cell(row=i, column=2, value=d)
        c.number_format = "dd/mm/yyyy"
        ws2.cell(row=i, column=3, value=code)
    ws3 = wb.create_sheet("Bank holidays")
    r3 = _header(ws3, ["Public holidays from the group HR calendar, January to March 2027"], 3)
    for j, c in enumerate(["date", "holiday", "calendar"], 1):
        ws3.cell(row=r3, column=j, value=c).font = Font(bold=True)
    for i, (d, n, reg) in enumerate(hist.HOLIDAYS, start=r3 + 1):
        c = ws3.cell(row=i, column=1, value=d)
        c.number_format = "dd/mm/yyyy"
        ws3.cell(row=i, column=2, value=n)
        ws3.cell(row=i, column=3, value=reg)
    ws4 = wb.create_sheet("Codes")
    for i, (k, v) in enumerate([("AL", "Annual leave"), ("TRN", "Training course, all day"),
                                ("IND", "Induction (new starter)"), ("STBY", "Standby day, out-of-hours cover")], start=1):
        ws4.cell(row=i, column=1, value=k)
        ws4.cell(row=i, column=2, value=v)
    wb.save(path)


def write_rp07(path):
    from reportlab import rl_config
    rl_config.invariant = 1
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib import colors
    ss = getSampleStyleSheet()
    body = ParagraphStyle("b", parent=ss["BodyText"], fontName="Helvetica", fontSize=9.5, leading=12.5)
    h = ParagraphStyle("h", parent=ss["Heading3"], fontName="Helvetica-Bold", fontSize=10.5, spaceBefore=8)
    t = ParagraphStyle("t", parent=ss["Title"], fontName="Helvetica-Bold", fontSize=14)
    story = [Paragraph("RP-07 Referral and placement of the field team", t),
             Paragraph("Corran Energy, Revenue Protection. Version 4, approved 14 September 2026 by Gareth Francis, "
                       "Revenue Protection Manager. Replaces version 3 (March 2024).", body),
             Spacer(1, 6)]
    secs = [
        ("1. Scope",
         "This procedure covers domestic supplies on credit-paying accounts in the north of Scotland. "
         "Prepayment supplies are dealt with under RP-09 and are not screened here. The field team works one "
         "patch for a quarter; travel between patches is not funded."),
        ("2. Screening",
         "Every supply in scope is screened against its own history each week. A week runs from 00:00 Monday to 00:00 the following Monday, local time. The screening run uses "
         "the eight complete weeks before the run date (the assessment weeks) and the 104 complete weeks "
         "before those (the history weeks)."),
        ("3. Expected consumption",
         "Expected consumption for each assessment week is the straight line of weekly kWh on weekly heating "
         "degree days (15.5 C base, from the station named for the patch) fitted by least squares to the "
         "supply's history weeks, evaluated at that week's degree days."),
        ("4. Referral",
         "A supply is referred when its recorded consumption over the eight assessment weeks is 30 per "
         "cent or more below the expected consumption for those weeks, and is below expected in each of the "
         "eight weeks."),
        ("5. Not referred",
         "No supply is referred at a premises where a change of occupier is recorded on any date in the history "
         "or assessment weeks; these go to the change of tenancy process. No supply is referred at a premises "
         "where a heating change (a heat pump, a new heating system or a change of fuel) was commissioned in "
         "the same period; insulation and solar panels are not heating changes."),
        ("6. Glossary",
         "Supply: one supply number (MPAN core) and the meter registering it. Premises: the property at a UPRN. "
         "Patch: the field area a premises sits in, as held in CIS."),
        ("7. Placement",
         "At the December planning meeting the field team is placed for January to March in the patch with the "
         "most referred supplies from the screening run on the first Monday in December. If two patches are level, the "
         "patch with more credit-paying premises is taken."),
        ("8. Reporting",
         "A patch's confirmation rate is diversions confirmed as a share of visits at which the officer gained "
         "access. A finding that is overturned on appeal is recorded as no fault found; the appeals register is "
         "the record of the decision."),
    ]
    for title, txt in secs:
        story.append(Paragraph(title, h))
        story.append(Paragraph(txt, body))
    story.append(Spacer(1, 10))
    tbl = Table([["Version", "Date", "Change"],
                 ["3", "March 2024", "Degree-day adjustment moved from patch averages to each supply's own history"],
                 ["4", "September 2026", "Change of occupier window widened to cover the history weeks"]],
                colWidths=[45, 75, 330])
    tbl.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", 8.5),
                             ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8.5),
                             ("GRID", (0, 0), (-1, -1), 0.4, colors.grey)]))
    story.append(tbl)
    story.append(Spacer(1, 8))
    story.append(Paragraph("Internal. Not for customer correspondence.", body))
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=56, rightMargin=56, topMargin=56, bottomMargin=56,
                            title="RP-07 Referral and placement of the field team", author="Corran Energy",
                            creator="Corran Energy", producer="Corran Energy document services",
                            subject="Revenue Protection procedure")
    doc.build(story)


def write_fw3(path):
    from docx import Document
    from docx.shared import Pt
    d = Document()
    st = d.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    d.add_heading("FW-3 Field working standard, revenue protection officers", level=1)
    d.add_paragraph("Corran Energy field operations. Issue 6, effective 1 April 2026.")
    d.add_paragraph("1. A field day is 7 hours 30 minutes on the district. Travel from the depot to a patch base "
                    "at the start and end of a deployment is not taken from field days.")
    d.add_paragraph("2. A planned visit is 70 minutes on site plus the patch's local travel allowance below. "
                    "An officer is planned for the whole number of visits that fits in a field day.")
    d.add_paragraph("3. Annual leave, training and induction days are not field days. A standby day is a field day. "
                    "Public holidays are not field days; officers at the Inverness depot observe the Scottish "
                    "public holidays.")
    d.add_paragraph("4. An officer's field days start on the officer's field start date in the rota.")
    t = d.add_table(rows=1, cols=3)
    t.style = "Table Grid"
    hdr = t.rows[0].cells
    hdr[0].text, hdr[1].text, hdr[2].text = "Patch", "Code", "Local travel allowance per visit (minutes)"
    for code, mins in hist.LOCAL_TRAVEL.items():
        row = t.add_row().cells
        row[0].text, row[1].text, row[2].text = PATCH_NAME[code], code, str(mins)
    d.add_paragraph("")
    d.add_paragraph("Lone working, vehicle checks and evidence handling are covered in FW-1 and FW-5.")
    d.save(path)


def write_notes(path, F):
    txt = f"""# Revenue protection extracts: field notes

Pulled for the December planning meeting. Owner: Christopher Horton, RP analytics.

## {F['mart']}
Analytics mart table `rp.account_week`. One row per billing account per ISO week (Monday start) in which
the account was open. `kwh_import` is the account's metered import for the days of that week it was open.
`rp_patch` is the patch of the premises on the account.

## {F['reads']}
Daily midnight register reads from the smart metering data service, one row per supply number per day
read. `cumulative_kwh` is the import register value at 00:00 local time on `read_date`. A missing day is a
read the meter did not return; the next read carries the consumption. After a meter exchange the
register restarts on the new serial; the exchange reads are in the register workbook.

## {F['register']}
CIS extract on the run date. `related_mpan` is populated where the supply has a related metering point.
`account_ref` is the account open on the run date. The account history sheet lists earlier accounts.

## {F['cot']}
Change of occupier events keyed by UPRN. Dates are the effective dates on the account.

## {F['measures']}
Completions from the energy efficiency team (ECO4 and Warmer Homes Scotland referrals), keyed by UPRN.

## {F['hdd']}
Daily mean temperature and heating degree days on a 15.5 C base, by station. The station for each patch
is in `{F['stations']}`.

## Field visit logs
FieldOps replaced FieldLink on 18 November 2024. FieldLink jobs dated from 4 November 2024 were re-created
in FieldOps, and `legacy_job_no` carries the FieldLink JobNo. FieldOps stamps `visit_start_utc` in UTC.
Outcome codes: CONF / DIV-CONFIRMED diversion confirmed, NFF / NO-FAULT no fault found, NOACC / NO-ACCESS
officer did not gain access.
"""
    with open(path, "w") as fh:
        fh.write(txt)


def write_vends(path, w, rng):
    rows = []
    seq = iter(range(9_000_001, 99_999_999, 17))
    for p in w["premises"]:
        if not p["prepay"]:
            continue
        mp = p["supplies"][0]["mpan"]
        d = dt.date(2026, 6, 1)
        while d <= dt.date(2026, 11, 30):
            d += dt.timedelta(int(rng.integers(3, 12)))
            if d > dt.date(2026, 11, 30):
                break
            amt = float(rng.choice([10, 15, 20, 20, 25, 30, 40]))
            ch = ["PayPoint", "App", "Post Office", "App"][int(rng.integers(0, 4))]
            ts = dt.datetime.combine(d, dt.time(int(rng.integers(7, 22)), int(rng.integers(0, 60))))
            ec = "Y" if rng.random() < 0.09 else "N"
            rows.append([f"V{next(seq)}", mp, p["patch"], ts.strftime("%d/%m/%Y %H:%M"), f"{amt:.2f}", ch, ec])
    with open(path, "w", newline="") as fh:
        wr = csv.writer(fh)
        wr.writerow(["vend_ref", "mpan_core", "rp_patch", "vend_time", "amount_gbp", "channel", "emergency_credit_on"])
        wr.writerows(rows)


def write_losses(path, rng):
    wb = Workbook()
    ws = wb.active
    ws.title = "Feeders"
    r = _header(ws, ["Distribution network operator | estimated losses by 11 kV feeder, 2025-26",
                     "Shared with suppliers under the data agreement. Losses = units entering the feeder less "
                     "units settled at metering points, all suppliers, technical and non-technical."], 6)
    cols = ["primary_substation", "feeder", "nearest_patch", "units_in_mwh", "units_settled_mwh", "loss_pct"]
    for j, c in enumerate(cols, 1):
        ws.cell(row=r, column=j, value=c).font = Font(bold=True)
    subs = {"INV": ["Inverness Raigmore", "Inverness Muirtown"], "NRN": ["Nairn"], "FRS": ["Forres"],
            "ELG": ["Elgin", "Lossiemouth"], "SPY": ["Aviemore", "Grantown"], "LOC": ["Fort William"],
            "CAI": ["Wick", "Thurso"], "SKY": ["Broadford", "Portree"]}
    i = r + 1
    for code, ss in subs.items():
        for s in ss:
            for k in range(int(rng.integers(3, 6))):
                uin = float(rng.uniform(4_000, 22_000))
                loss = float(rng.uniform(0.045, 0.092))
                vals = [s, f"{s[:3].upper()}-F{k + 1:02d}", code, round(uin, 0), round(uin * (1 - loss), 0),
                        round(loss * 100, 1)]
                for j, v in enumerate(vals, 1):
                    ws.cell(row=i, column=j, value=v)
                i += 1
    wb.save(path)


def write_log(path, F, counts):
    txt = f"""rp_extract run 2026-12-07 06:20:14 GMT  user: chorton
source            file                                                      rows
rp.account_week   {F['mart']:<57} {counts['mart']}
sms.daily_reads   {F['reads']:<57} {counts['reads']}
cis.supply_point  {F['register']:<57} {counts['supplies']}
cis.cot_events    {F['cot']:<57} {counts['cot']}
eem.completions   {F['measures']:<57} {counts['measures']}
metoffice.daily   {F['hdd']:<57} {counts['hdd']}
fieldlink.jobs    {F['fl']:<57} {counts['fl']}
fieldops.jobs     {F['fo']:<57} {counts['fo']}
rp.appeals        {F['appeals']:<57} {counts['appeals']}
prepay.vends      {F['vends']:<57}
dno.feeder_losses {F['losses']:<57}
documents: {F['rp07']}, {F['fw3']}, {F['rota']}, {F['stations']}
reads window 2024-10-01 to 2026-12-07 (00:00); mart window w/c 2023-12-04 to w/c 2026-11-30
"""
    with open(path, "w") as fh:
        fh.write(txt)


STAMP = "2026-12-07T06:31:00Z"


def _rewrite_zip_props(path, creator):
    tmp = path + ".tmp"
    with zipfile.ZipFile(path) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "docProps/core.xml":
                s = data.decode("utf8")
                s = re.sub(r"<dc:creator>.*?</dc:creator>", f"<dc:creator>{creator}</dc:creator>", s)
                s = re.sub(r"<cp:lastModifiedBy>.*?</cp:lastModifiedBy>", f"<cp:lastModifiedBy>{creator}</cp:lastModifiedBy>", s)
                s = re.sub(r"(<dcterms:created[^>]*>).*?(</dcterms:created>)", rf"\g<1>{STAMP}\g<2>", s)
                s = re.sub(r"(<dcterms:modified[^>]*>).*?(</dcterms:modified>)", rf"\g<1>{STAMP}\g<2>", s)
                data = s.encode("utf8")
            if item.filename == "docProps/app.xml":
                s = data.decode("utf8")
                s = re.sub(r"<Application>.*?</Application>", "<Application>Microsoft Office</Application>", s)
                data = s.encode("utf8")
            zi = zipfile.ZipInfo(item.filename, date_time=(2026, 12, 7, 6, 31, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zout.writestr(zi, data)
    shutil.move(tmp, path)


def scrub_metadata(target, zips=True):
    owners = {".xlsx": "Corran Energy", ".docx": "Corran Energy"}
    for fn in os.listdir(target):
        p = os.path.join(target, fn)
        ext = os.path.splitext(fn)[1]
        if zips and ext in owners:
            _rewrite_zip_props(p, owners[ext])
    ts = dt.datetime(2026, 12, 7, 6, 31).timestamp()
    for fn in os.listdir(target):
        os.utime(os.path.join(target, fn), (ts, ts))
