"""Cut the pack: the server's dose log, the compounders' event export, the check register, the quarantine register,
the product master, the equipment register, the policy, the procedure, the cutover request and the context files."""
import csv
import datetime as dt
import io
import os
import re
import zipfile
from email.message import EmailMessage
from email.utils import format_datetime

import numpy as np
import openpyxl
import pyarrow as pa
import pyarrow.parquet as pq
from openpyxl.styles import Font
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import params as P
import world as W

FILES = {
    "doses": "compounder_dose_log_2026.parquet",
    "events": "compounder_events_2026.csv",
    "checks": "gravimetric_check_register_2026.xlsx",
    "quarantine": "quarantine_register_2026.xlsx",
    "master": "compounded_product_master.xlsx",
    "equipment": "compounding_equipment_register.csv",
    "policy": "PH-QP-07_batch_compounded_products_policy.pdf",
    "sop": "SC-SOP-12_batch_compounding_procedure.pdf",
    "request": "iv_workflow_cutover_product_list.eml",
    "gc1": "gc1_dose_weights_2026.csv",
    "wards": "ward_issues_2026.csv",
    "cleanroom": "cleanroom_monitoring_2026.csv",
}
DISTRACTORS = ["gc1", "wards", "cleanroom"]
UTC = dt.timezone.utc
TEMPLATE_CHANGE = dt.date(2026, 7, 1)     # the check register's template records net weights from this date
INITIALS = ["JB", "AK", "MT", "RS", "LD", "PN", "CW", "HG", "SO", "EV", "TF"]


# ------------------------------------------------------------------------------------------------ writers

def _csv(path, header, rows):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(header)
    w.writerows(rows)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(buf.getvalue())


def _xlsx(path, sheets, creator, created, modified, widths=(12, 10, 12, 40, 9, 13, 9, 10, 30)):
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    for title, rows, bold in sheets:
        ws = wb.create_sheet(title)
        for r in rows:
            ws.append(list(r))
        for i in bold:
            for c in ws[i]:
                c.font = Font(bold=True)
        for col, width in zip("ABCDEFGHIJ", widths):
            ws.column_dimensions[col].width = width
    wb.properties.creator = creator
    wb.properties.lastModifiedBy = creator
    wb.properties.created = created
    wb.properties.modified = modified
    wb.properties.title = None
    buf = io.BytesIO()
    wb.save(buf)
    src = zipfile.ZipFile(io.BytesIO(buf.getvalue()))
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for info in src.infolist():
            data = src.read(info.filename)
            if info.filename == "docProps/core.xml":
                data = re.sub(rb"(<dcterms:modified[^>]*>)[^<]*(</dcterms:modified>)",
                              b"\\g<1>" + modified.strftime("%Y-%m-%dT%H:%M:%SZ").encode() + b"\\g<2>", data)
                data = re.sub(rb"(<dcterms:created[^>]*>)[^<]*(</dcterms:created>)",
                              b"\\g<1>" + created.strftime("%Y-%m-%dT%H:%M:%SZ").encode() + b"\\g<2>", data)
            if info.filename == "docProps/app.xml":
                data = (b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
                        b'<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties">'
                        b'<Application>Microsoft Excel</Application><DocSecurity>0</DocSecurity>'
                        b'<ScaleCrop>false</ScaleCrop><LinksUpToDate>false</LinksUpToDate><SharedDoc>false</SharedDoc>'
                        b'<HyperlinksChanged>false</HyperlinksChanged><AppVersion>16.0300</AppVersion></Properties>')
            zi = zipfile.ZipInfo(info.filename, date_time=modified.timetuple()[:6])
            zi.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(zi, data)


def _styles():
    base = ParagraphStyle("p", fontName="Helvetica", fontSize=9.6, leading=13, alignment=TA_LEFT, spaceAfter=5)
    return {"t": ParagraphStyle("t", parent=base, fontName="Helvetica-Bold", fontSize=13, leading=17, spaceAfter=4),
            "s": ParagraphStyle("s", parent=base, fontSize=8.4, leading=11, textColor=colors.HexColor("#4a5560")),
            "h": ParagraphStyle("h", parent=base, fontName="Helvetica-Bold", fontSize=10.4, leading=14, spaceBefore=6),
            "p": base,
            "cell": ParagraphStyle("c", parent=base, fontSize=8.6, leading=10.6, spaceAfter=0)}


def pdf(path, blocks, title, author, created, modified, footer, first_col=0.30):
    st = _styles()

    def page(canvas, d):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.5)
        canvas.setFillColor(colors.HexColor("#5b6670"))
        canvas.drawString(20 * mm, 10 * mm, footer)
        canvas.drawRightString(A4[0] - 20 * mm, 10 * mm, "Page %d" % d.page)
        canvas.restoreState()
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm,
                            bottomMargin=18 * mm, title=title, author=author, creator=author, producer="Microsoft Word",
                            invariant=1)
    story = []
    for kind, val in blocks:
        if kind == "table":
            width = A4[0] - 40 * mm
            n = len(val[0])
            widths = [width * first_col] + [width * (1 - first_col) / (n - 1)] * (n - 1) if n > 1 else [width]
            rows = [[Paragraph(str(c).replace("&", "&amp;"), st["cell"]) for c in r] for r in val]
            t = Table(rows, colWidths=widths, hAlign="LEFT", repeatRows=1)
            t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.HexColor("#8a949c")),
                                   ("VALIGN", (0, 0), (-1, -1), "TOP"), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
            story += [t, Spacer(1, 6)]
        elif kind == "img":
            story.append(val)
        else:
            story.append(Paragraph(val, st[kind]))
    doc.build(story, onFirstPage=page, onLaterPages=page)
    data = open(path, "rb").read()
    data = re.sub(rb"/CreationDate \(D:[^)]*\)", b"/CreationDate (" + created.encode() + b")", data)
    data = re.sub(rb"/ModDate \(D:[^)]*\)", b"/ModDate (" + modified.encode() + b")", data)
    for sig in (b"ReportLab Generated PDF document (opensource)", b"ReportLab generated PDF document -- digest (opensource)",
                b"ReportLab PDF Library - www.reportlab.com"):
        data = data.replace(sig, b" " * len(sig))
    open(path, "wb").write(data)


def _pdfdate(d):
    return "D:%s-05'00'" % d.strftime("%Y%m%d%H%M%S")


# ------------------------------------------------------------------------------------------------ the records

def _utc(t):
    return t.astimezone(UTC)


def write_doses(path):
    w = W.simulate()
    counts = {}
    serial, ts, prod, batch, dose, ml, status = [], [], [], [], [], [], []
    for d in w["doses"]:
        key = d["batch_no"]
        if d["status"] == "COMPLETE":
            counts[key] = d["seq"]
            n = d["seq"]
        else:
            n = counts.get(key, 0) + 1
        serial.append(d["serial"])
        ts.append(_utc(d["t"]).strftime("%Y-%m-%d %H:%M:%S"))
        prod.append(d["product"])
        batch.append(d["batch_no"])
        dose.append(n)
        ml.append(float(W.product(d["product"])["vol"]))
        status.append(d["status"])
    order = sorted(range(len(ts)), key=lambda i: (ts[i], serial[i], batch[i], dose[i], status[i]))
    tbl = pa.table({
        "compounder_sn": pa.array([serial[i] for i in order], pa.string()),
        "fill_end_time": pa.array([ts[i] for i in order], pa.string()),
        "product_no": pa.array([prod[i] for i in order], pa.string()),
        "batch_no": pa.array([batch[i] for i in order], pa.string()),
        "dose_no": pa.array([dose[i] for i in order], pa.int32()),
        "programmed_ml": pa.array([ml[i] for i in order], pa.float64()),
        "status": pa.array([status[i] for i in order], pa.string()),
    })
    pq.write_table(tbl, path, compression="snappy", use_dictionary=True, write_statistics=False)
    return len(order)


def write_events(path):
    w = W.simulate()
    rows = sorted(((_utc(e["t"]).strftime("%Y-%m-%dT%H:%M:%SZ"), e["serial"], e["event"], e["lot"]) for e in w["events"]))
    _csv(path, ["event_time", "compounder_sn", "event", "set_lot"], [(t, s, ev, lot) for t, s, ev, lot in rows])
    return len(rows)


def _weights(c, r):
    d = c["dose"]
    p = W.product(d["product"])
    net = p["vol"] * (1 + d["dev"] / 100.0) * p["sg"]
    local = c["t"].astimezone(W.TZ)
    gross = local.date() < TEMPLATE_CHANGE
    wt = net + (p["tare"] + float(r.normal(0, 0.04)) if gross else 0.0)
    return local, round(wt, 2), gross


def check_rows():
    """Every weighed dose as the register holds it: local date and time, batch, product name, dose number, weight
    (gross until 30 June, net from 1 July), result and initials."""
    w = W.simulate()
    r = W.rng("register")
    out = []
    for c in w["checks"]:
        d = c["dose"]
        p = W.product(d["product"])
        if p.get("verified"):
            continue
        local, wt, gross = _weights(c, r)
        out.append(dict(local=local, batch=d["batch_no"], name=p["name"], dose=d["seq"], wt=wt, gross=gross,
                        result="FAIL" if c["out"] else "PASS", by=INITIALS[int(r.integers(0, len(INITIALS)))],
                        dose_ref=d))
    out.sort(key=lambda x: (x["local"], x["batch"], x["dose"]))
    return out


def write_checks(path):
    rows = check_rows()
    sheets = []
    for q, (a, b) in enumerate([((1, 1), (3, 31)), ((4, 1), (6, 30)), ((7, 1), (9, 30)), ((10, 1), (12, 31))]):
        lo, hi = dt.date(2026, *a), dt.date(2026, *b)
        gross = q < 2
        head = ["Date", "Time", "Batch", "Product", "Dose no.", "Gross wt (g)" if gross else "Net wt (g)", "Result",
                "Checked by"]
        body = [[x["local"].date().isoformat(), x["local"].strftime("%H:%M"), x["batch"], x["name"], x["dose"], x["wt"],
                 x["result"], x["by"]] for x in rows if lo <= x["local"].date() <= hi]
        sheets.append(("Q%d 2026" % (q + 1), [head] + body, [1]))
    _xlsx(path, sheets, P.PEOPLE["quality"], dt.datetime(2025, 12, 19, 14, 2, 11),
          dt.datetime(2027, 1, 15, 16, 48, 37))
    return len(rows)


def sort_rows():
    w = W.simulate()
    r = W.rng("quarantine")
    out = []
    no = 1180
    for s in sorted(w["sorts"], key=lambda x: x["t"]):
        no += int(r.integers(3, 29))
        local = s["t"].astimezone(W.TZ)
        out.append(dict(no="DEV-2026-%04d" % no, opened=local, batch=s["batch_no"], quar=s["quarantined"],
                        weighed=s["quarantined"], rej=s["rejected"], note="", recount=False, product=s["product"]))
    # two sorts were reopened by the quality pharmacist and recounted; the recount is entered under the same number
    rec = []
    picks = sorted(r.choice(len(out), size=min(2, len(out)), replace=False).tolist()) if out else []
    for i in picks:
        x = dict(out[i])
        first = dict(out[i])
        first["rej"] = max(0, x["rej"] + (1 if x["rej"] < 3 else -1))
        out[i] = first
        x["opened"] = x["opened"] + dt.timedelta(days=int(r.integers(1, 4)), hours=int(r.integers(1, 5)))
        x["note"] = "Recount by %s; replaces the entry of %s" % (P.PEOPLE["quality"].split()[0][0] +
                                                                   P.PEOPLE["quality"].split()[1][0],
                                                                   first["opened"].date().isoformat())
        x["recount"] = True
        rec.append(x)
    return out, rec


def write_quarantine(path):
    out, rec = sort_rows()
    rows = sorted(out + rec, key=lambda x: x["opened"])
    head = ["Deviation no.", "Opened", "Batch", "Doses quarantined", "Doses weighed", "Doses rejected", "Closed by",
            "Note"]
    body = [[x["no"], x["opened"].strftime("%Y-%m-%d %H:%M"), x["batch"], x["quar"], x["weighed"], x["rej"],
             "ES" if x["recount"] else "JB", x["note"]] for x in rows]
    _xlsx(path, [("Sorts 2026", [head] + body, [1])], P.PEOPLE["quality"], dt.datetime(2024, 3, 4, 9, 15, 40),
          dt.datetime(2027, 1, 14, 11, 27, 5), widths=(15, 17, 12, 17, 14, 15, 10, 50))
    return len(body)


def write_master(path):
    head = ["Product no.", "Product", "Container", "Labelled volume (mL)", "Volume tolerance (+/- %)",
            "Specific gravity", "Container tare (g)", "Station", "Weighed every dose"]
    body = []
    for p in P.PRODUCTS:
        cont = "bag" if "bag" in p["name"] else "syringe"
        body.append([p["code"], p["name"], cont, p["vol"], p["tol"], p["sg"], p["tare"], p["station"],
                     "yes" if p.get("verified") else "no"])
    _xlsx(path, [("Products", [head] + body, [1])], P.PEOPLE["lead_tech"], dt.datetime(2023, 9, 11, 10, 4, 52),
          dt.datetime(2026, 11, 30, 15, 39, 18), widths=(11, 44, 10, 12, 12, 10, 10, 9, 12))


def write_equipment(path):
    rows = []
    for st in sorted(P.STATIONS):
        for s, a, b in P.STATIONS[st]["serials"]:
            first = a if a > P.FIRST_DAY else {"PC-1": dt.date(2021, 5, 17), "PC-2": dt.date(2021, 5, 17),
                                               "PC-3": dt.date(2019, 11, 4), "PC-4": dt.date(2023, 2, 20),
                                               "GC-1": dt.date(2022, 8, 29)}[st]
            rows.append([st, s, P.STATIONS[st]["model"], first.isoformat(), b.isoformat() if b else ""])
    _csv(path, ["station", "serial", "model", "in_service_from", "in_service_to"], rows)


def write_gc1(path):
    w = W.simulate()
    rows = []
    for d in w["doses"]:
        p = W.product(d["product"])
        if not p.get("verified") or d["status"] != "COMPLETE":
            continue
        net = p["vol"] * (1 + d["dev"] / 100.0) * p["sg"]
        rows.append([d["t"].astimezone(W.TZ).strftime("%Y-%m-%d %H:%M:%S"), d["batch_no"], d["product"], d["seq"],
                     "%.2f" % net, "OUT" if abs(d["dev"]) > p["tol"] else "IN"])
    _csv(path, ["filled_local", "batch_no", "product_no", "dose_no", "net_weight_g", "verdict"], rows)


def write_wards(path):
    w = W.simulate()
    r = W.rng("wards")
    wards = ["Operating Theatres", "Day Surgery", "Labour and Delivery", "ICU", "Emergency", "Medicine 3W",
             "Surgery 4E", "Oncology Day Unit"]
    use = {"P0412": [0.55, 0.25, 0.08, 0.04, 0.03, 0.02, 0.03, 0.0], "P0413": [0.35, 0.30, 0.1, 0.05, 0.1, 0.05, 0.05, 0],
           "P0431": [0.6, 0.3, 0.0, 0.03, 0.02, 0.0, 0.05, 0.0], "P0507": [0.7, 0.15, 0.1, 0.05, 0, 0, 0, 0],
           "P0509": [0.65, 0.15, 0.15, 0.05, 0, 0, 0, 0], "P0522": [0.5, 0.1, 0.0, 0.2, 0.2, 0, 0, 0]}
    monthly = {}
    for d in w["doses"]:
        if d["status"] != "COMPLETE":
            continue
        m = d["t"].astimezone(W.TZ).month
        monthly[(d["product"], m)] = monthly.get((d["product"], m), 0) + 1
    rows = []
    for (code, m), n in sorted(monthly.items()):
        share = use.get(code, [0.1, 0.1, 0.1, 0.25, 0.15, 0.15, 0.1, 0.05])
        issued = n * float(r.uniform(0.93, 0.985))
        for wd, sh in zip(wards, share):
            q = int(round(issued * sh * float(r.uniform(0.9, 1.1))))
            if q:
                rows.append(["2026-%02d" % m, code, wd, q])
    _csv(path, ["month", "product_no", "ward", "doses_issued"], rows)


def write_cleanroom(path):
    r = W.rng("cleanroom")
    rows = []
    day = dt.date(2026, 1, 5)
    while day <= P.LAST_DAY:
        for room, grade in (("Buffer room 1", "ISO 7"), ("Buffer room 2", "ISO 7"), ("Ante room", "ISO 8"),
                            ("PEC 1 (BSC)", "ISO 5"), ("PEC 2 (BSC)", "ISO 5")):
            lim = {"ISO 5": 3520, "ISO 7": 352000, "ISO 8": 3520000}[grade]
            p05 = int(lim * float(r.uniform(0.02, 0.35)))
            cfu = int(r.poisson(0.2 if grade == "ISO 5" else 2.5))
            rows.append([day.isoformat(), room, grade, p05, cfu])
        day += dt.timedelta(days=7 + int(r.integers(-1, 2)))
    _csv(path, ["sample_date", "room", "classification", "particles_0_5um_per_m3", "viable_air_cfu_per_m3"], rows)


# ------------------------------------------------------------------------------------------------ documents

def write_policy(path):
    blocks = [
        ("t", "%s Pharmacy Services" % P.ORG),
        ("s", "Policy PH-QP-07. Batch-compounded sterile products: gravimetric verification. Version 3, approved by the "
              "Director of Pharmacy on 9 December 2025, effective 1 January 2026. Review due December 2027."),
        ("h", "1. Purpose and scope"),
        ("p", "This policy sets which of the products the Sterile Compounding Unit batch-compounds on its compounders "
              "are verified by weight dose by dose. It applies to every product listed in the compounded product "
              "master. Doses prepared one at a time for a named patient are outside its scope."),
        ("h", "2. Definitions"),
        ("p", "A <b>dose made</b> is a dose the compounder completed. A fill the compounder stopped before completion "
              "(an aborted fill) is discarded at the station and is not a dose made."),
        ("p", "An <b>out-of-tolerance dose</b> is a dose made whose delivered volume lay outside the volume tolerance "
              "the product master sets for the product, whether or not the dose was weighed or quarantined."),
        ("p", "A product's <b>out-of-tolerance rate</b> for a calendar year is its out-of-tolerance doses made in that "
              "year per 100,000 of its doses made in that year. The year is the calendar year in Ontario local time."),
        ("h", "3. Gravimetric verification of every dose"),
        ("p", "3.1 At each configuration of the pharmacy's IV workflow system, each batch-compounded product filled on "
              "the unit's peristaltic or syringe-driver compounders (PC-1 to PC-4) is configured for gravimetric "
              "verification of every dose where its out-of-tolerance rate in the last full calendar year exceeded 10. "
              "The others stay on the in-process checks of SC-SOP-12."),
        ("p", "3.2 Products filled on the gravimetric compounder (GC-1), which weighs every dose it fills, are not "
              "configured; they stay on GC-1."),
        ("p", "3.3 The quality pharmacist prepares the case for each product and the Director of Pharmacy approves the "
              "list before the configuration is locked."),
        ("h", "4. Records"),
        ("p", "The compounders' dose and event records are kept on the pharmacy server for three years. The gravimetric "
              "check register and the quarantine register are kept by the unit and copied to the server at each "
              "month end."),
        ("h", "5. Related documents"),
        ("p", "SC-SOP-12 Batch compounding on the unit's compounders. PH-QP-02 Beyond-use dating of compounded sterile "
              "preparations. PH-QP-11 Deviation reporting."),
    ]
    pdf(path, blocks, "PH-QP-07 Batch-compounded sterile products: gravimetric verification", P.PEOPLE["director"],
        _pdfdate(dt.datetime(2025, 11, 24, 10, 41, 3)), _pdfdate(dt.datetime(2025, 12, 9, 15, 12, 47)),
        "%s Pharmacy Services   PH-QP-07 v3   Controlled copy" % P.ORG)


def write_sop(path):
    blocks = [
        ("t", "SC-SOP-12 Batch compounding on the unit's compounders"),
        ("s", "%s, %s. Version 6, effective 3 March 2025. Owner: Sterile Compounding Unit lead technician. "
              "Approved: quality pharmacist." % (P.HOSPITAL, P.UNIT)),
        ("h", "1. Hours"),
        ("p", "The unit compounds on weekdays from 07:00 to 23:00 in two shifts and on Saturdays from 08:00 to 16:00. It "
              "is closed on Sundays and statutory holidays."),
        ("h", "2. Stations"),
        ("p", "PC-1, PC-2 and PC-3 are peristaltic compounders: each set-up installs a new tubing set. PC-4 is a "
              "syringe-driver compounder: each set-up installs a new fluid path set. GC-1 is the gravimetric compounder "
              "and weighs every dose it fills. Station assignments are in the compounded product master."),
        ("h", "3. Set-up"),
        ("p", "3.1 Install the set, prime it with the product's source solution and run the compounder's gravimetric "
              "calibration for the product. The compounder logs the set-up and the set lot."),
        ("p", "3.2 A set may be used for further batches of the same product, one after another, within 24 hours of "
              "its set-up. Bag products are set up afresh for each batch."),
        ("p", "3.3 After an occlusion alarm, clear the line and re-seat the set in the pump head before continuing."),
        ("h", "4. In-process checks"),
        ("p", "4.1 Weigh the first dose of each batch on the unit's check balance, then every hundredth dose of a "
              "syringe batch and every twentieth dose of a bag batch, and enter the weight in the gravimetric check "
              "register with the batch, the product, the dose number and the result."),
        ("p", "4.2 The delivered volume is the dose's net weight divided by the product's specific gravity. A dose "
              "passes where its delivered volume lies within the product's volume tolerance."),
        ("h", "5. Reaction plan"),
        ("p", "5.1 A weighed dose outside tolerance stops the batch. Quarantine every dose of the batch made since the "
              "last conforming check, weigh each quarantined dose and discard those outside tolerance. Record the sort "
              "in the quarantine register under a deviation number."),
        ("p", "5.2 Replace the set, set up again and continue the batch on the new set."),
        ("h", "6. Release"),
        ("p", "A batch is released by a pharmacist once its checks are entered and any sort is closed."),
    ]
    pdf(path, blocks, "SC-SOP-12 Batch compounding on the unit's compounders", P.PEOPLE["lead_tech"],
        _pdfdate(dt.datetime(2025, 2, 11, 9, 2, 55)), _pdfdate(dt.datetime(2025, 3, 3, 8, 21, 9)),
        "%s   SC-SOP-12 v6   Printed copies are uncontrolled" % P.HOSPITAL)


def write_request(path):
    msg = EmailMessage()
    msg["From"] = "%s <spencer.frank@ashcombevalley.example>" % P.PEOPLE["project"]
    msg["To"] = "%s <cynthia.underwood@ashcombevalley.example>" % P.PEOPLE["director"]
    msg["Cc"] = "%s <erin.stewart@ashcombevalley.example>" % P.PEOPLE["quality"]
    msg["Subject"] = "IV workflow go-live: batch products for dose-by-dose weighing"
    msg["Date"] = format_datetime(dt.datetime(2027, 1, 18, 9, 37, 12, tzinfo=W.TZ))
    msg["Message-ID"] = "<20270118093712.5521@ashcombevalley.example>"
    msg.set_content(
        "Cynthia,\n\n"
        "The IV workflow system goes live in the Sterile Compounding Unit on Monday 5 April 2027. The vendor locks the "
        "product configuration on 1 March, so I need the list of batch-compounded products to set up for gravimetric "
        "verification of every dose under PH-QP-07 by Friday 12 February, with the case for each product for the "
        "configuration file.\n\n"
        "Erin has pulled the unit's 2026 records from the pharmacy server and the unit's registers (the compounders' "
        "dose log and event export, the check register, the quarantine register, the product master and the "
        "equipment register). They are on the project share with this note.\n\n"
        "The products on GC-1 are already weighed dose by dose and do not need configuring.\n\n"
        "Thanks,\n\n"
        "Spencer Frank\nIV Workflow Project Lead, Pharmacy Informatics\n%s\n" % P.ORG)
    with open(path, "wb") as f:
        f.write(bytes(msg))


def build(target):
    os.makedirs(target, exist_ok=True)
    n = write_doses(os.path.join(target, FILES["doses"]))
    write_events(os.path.join(target, FILES["events"]))
    write_checks(os.path.join(target, FILES["checks"]))
    write_quarantine(os.path.join(target, FILES["quarantine"]))
    write_master(os.path.join(target, FILES["master"]))
    write_equipment(os.path.join(target, FILES["equipment"]))
    write_policy(os.path.join(target, FILES["policy"]))
    write_sop(os.path.join(target, FILES["sop"]))
    write_request(os.path.join(target, FILES["request"]))
    write_gc1(os.path.join(target, FILES["gc1"]))
    write_wards(os.path.join(target, FILES["wards"]))
    write_cleanroom(os.path.join(target, FILES["cleanroom"]))
    return n
