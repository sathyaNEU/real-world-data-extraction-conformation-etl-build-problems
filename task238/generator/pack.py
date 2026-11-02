"""Write the evidence pack (target/) from the clean truth in world.py. Each file is written the way its own system
writes it (the POS host, the pricing team's report, the printer fleet console, the integrity team's handheld, the
service desk app, merchandising), with its own clock, key format and layout; nothing here describes the data."""
import csv
import datetime as dt
import json
import os
import re
import zipfile
from zoneinfo import ZoneInfo

import numpy as np

import params as P
import world as W

UTC = ZoneInfo("UTC")
FIXED_ZIP_TIME = (1980, 1, 1, 0, 0, 0)        # what Excel writes on every member
STORE = {s[0]: s for s in P.STORES}


def write_csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f, lineterminator="\n")
        wr.writerow(header)
        for r in rows:
            wr.writerow(r)


def normalise_zip(path, when, created=None):
    with zipfile.ZipFile(path) as z:
        items = [(i.filename, z.read(i.filename)) for i in z.infolist()]
    fixed = []
    for name, data in items:
        if name == "docProps/app.xml":
            data = re.sub(rb"<Application>[^<]*</Application>", b"<Application>Microsoft Excel</Application>", data)
            data = re.sub(rb"<AppVersion>[^<]*</AppVersion>", b"<AppVersion>16.0300</AppVersion>", data)
        if name == "docProps/core.xml":
            data = re.sub(rb"(<dcterms:created[^>]*>)[^<]*(</dcterms:created>)",
                          rb"\g<1>" + (created or when).encode() + rb"\g<2>", data)
            data = re.sub(rb"(<dcterms:modified[^>]*>)[^<]*(</dcterms:modified>)",
                          rb"\g<1>" + when.encode() + rb"\g<2>", data)
        fixed.append((name, data))
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in fixed:
            zi = zipfile.ZipInfo(name, date_time=FIXED_ZIP_TIME)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o600 << 16
            z.writestr(zi, data)


def xlsx_props(wb, creator, title):
    when = dt.datetime(2027, 1, 12, 9, 30, 0)
    wb.properties.creator = creator
    wb.properties.lastModifiedBy = creator
    wb.properties.created = when
    wb.properties.modified = when
    wb.properties.title = title


def write_pdf(path, title, issuer, blocks, stamp_date):
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    ss = getSampleStyleSheet()
    body = ParagraphStyle("b", parent=ss["BodyText"], fontName="Helvetica", fontSize=9.5, leading=12.5)
    head = ParagraphStyle("h", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=11, leading=14,
                          spaceBefore=8, spaceAfter=3)
    ttl = ParagraphStyle("t", parent=ss["Title"], fontName="Helvetica-Bold", fontSize=14, leading=17)
    small = ParagraphStyle("s", parent=body, fontSize=8, leading=10, textColor=colors.HexColor("#444444"))
    story = []
    for kind, val in blocks:
        if kind == "title":
            story += [Paragraph(val, ttl), Spacer(1, 4)]
        elif kind == "h":
            story.append(Paragraph(val, head))
        elif kind == "p":
            story += [Paragraph(val, body), Spacer(1, 3)]
        elif kind == "small":
            story.append(Paragraph(val, small))
        elif kind == "table":
            t = Table(val, hAlign="LEFT")
            t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", 8.5),
                                   ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8.5),
                                   ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#999999")),
                                   ("VALIGN", (0, 0), (-1, -1), "TOP")]))
            story += [t, Spacer(1, 5)]

    def stamp(canvas, doc):
        canvas.setAuthor(issuer)
        canvas.setCreator(issuer)
        canvas.setProducer(issuer)
        canvas.setTitle(title)
        canvas.setFont("Helvetica", 7.5)
        canvas.drawString(0.75 * inch, 0.5 * inch, "%s  |  %s  |  page %d" % (issuer, title, doc.page))

    doc = SimpleDocTemplate(path, pagesize=letter, leftMargin=0.8 * inch, rightMargin=0.8 * inch,
                            topMargin=0.75 * inch, bottomMargin=0.75 * inch, invariant=1, title=title,
                            author=issuer, creator=issuer, producer=issuer)
    doc.build(story, onFirstPage=stamp, onLaterPages=stamp)
    data = open(path, "rb").read()
    for sig in (b"ReportLab Generated PDF document (opensource)",
                b"ReportLab generated PDF document -- digest (opensource)",
                b"ReportLab Generated PDF document http://www.reportlab.com"):
        data = data.replace(sig, b" " * len(sig))
    for key in (b"/CreationDate", b"/ModDate"):
        def sub(m):
            new = stamp_date.encode()
            assert len(new) == len(m.group(1)), (m.group(1), new)
            return key + b" (" + new + b")"
        data = re.sub(re.escape(key) + rb" \(([^)]*)\)", sub, data)
    assert b"ReportLab" not in data and b"reportlab" not in data
    open(path, "wb").write(data)


def ean13(upc12):
    return "0" + upc12


def money(x):
    return "%.2f" % x


def zstamp(t):
    return t.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def lstamp(t):
    """local time with its UTC offset, the way the printer fleet console writes it"""
    s = t.strftime("%Y-%m-%dT%H:%M:%S%z")
    return s[:-2] + ":" + s[-2:]


def hhmm(t):
    return t.strftime("%H:%M")


# =============================================================================================================
def build(target, w=None):
    if w is None:
        w = W.build_world()
    os.makedirs(target, exist_ok=True)
    r = np.random.default_rng(P.SEED + 7)
    n = {}
    F = P.FILES

    # --- POS host: item scans by store, business date and hour (local wall clock) -------------------------
    rows = []
    for (no, d), (hrs, counts) in sorted(w.hourly.items()):
        for h, c in zip(hrs, counts):
            rows.append([no, d.isoformat(), "%02d:00" % h, int(c)])
    write_csv(os.path.join(target, F["hourly"]), ["store_no", "business_date", "hour_start", "item_scans"], rows)
    n["hourly"] = len(rows)

    # --- pricing analytics: price-changed items, units scanned on the changeover Thursday and the one before --
    rows = []
    for s in P.STORES:
        no = s[0]
        for k, c in enumerate(w.co):
            keep = w.stocked[no][c["items"]]
            t = w.thu[(no, k)]
            for j in np.where(keep)[0]:
                i = c["items"][j]
                rows.append([c["date"].isoformat(), no, w.upc[i], w.desc[i].upper(), w.dept[i], c["kind"][j],
                             int(t["prior"][j]), int(t["units"][j])])
    rows.sort(key=lambda x: (x[0], x[1], x[4], x[2]))
    write_csv(os.path.join(target, F["movement"]),
              ["changeover_date", "store_no", "upc", "item_description", "department", "change_type",
               "units_prior_thursday", "units_changeover_thursday"], rows)
    n["movement"] = len(rows)

    # --- printer fleet console: every job on every store's shelf-edge label printer, UTC ---------------------
    jobs = []
    for s in P.STORES:
        no, dev = s[0], s[3]
        device = "SM-%s-ZT411-0%d" % (dev, 1 if no % 3 else 2)
        seq = 10000 + int(r.integers(0, 5000))
        for k, c in enumerate(w.co):
            b = w.batch[(no, k)]
            name = "PCB %s" % c["date"].strftime("%d%b%y").upper()
            if b["jam"]:
                seq += 1
                tj = b["print"] - dt.timedelta(minutes=b["jam_lead"])
                jobs.append((tj, {"device": device, "job_id": "J%d-%06d" % (no, seq), "submitted_local": lstamp(tj - dt.timedelta(seconds=40)),
                                  "printed_local": lstamp(tj), "job_name": name, "template": "SEL-STD",
                                  "labels": int(b["labels"] * r.uniform(0.05, 0.4)), "status": "VOIDED"}))
            seq += 1
            jobs.append((b["print"], {"device": device, "job_id": "J%d-%06d" % (no, seq),
                                      "submitted_local": lstamp(b["print"] - dt.timedelta(seconds=int(r.integers(30, 160)))),
                                      "printed_local": lstamp(b["print"]), "job_name": name + (" RP" if b["jam"] else ""),
                                      "template": "SEL-STD", "labels": int(b["labels"]), "status": "COMPLETED"}))
            # the week's other jobs: tag replacements, new items, aisle strips, the odd test page
            for d in [c["date"] + dt.timedelta(days=j) for j in range(7)]:
                if d > P.Q_END or not W.hours_of(d):
                    continue
                for _ in range(int(r.poisson(1.6))):
                    hrs = W.hours_of(d)
                    t = W.local(d, r.uniform(hrs[0] - 0.5, hrs[-1] + 0.8))
                    kind = r.choice(["TAG REPLACE", "NEW ITEMS", "AISLE STRIP", "TEST", "ADHOC"],
                                    p=[0.42, 0.24, 0.12, 0.04, 0.18])
                    nl = {"TAG REPLACE": int(r.integers(1, 26)), "NEW ITEMS": int(r.integers(3, 40)),
                          "AISLE STRIP": int(r.integers(12, 60)), "TEST": 1, "ADHOC": int(r.integers(1, 12))}[kind]
                    tmpl = {"AISLE STRIP": "STRIP-12", "TEST": "CONFIG"}.get(kind, "SEL-STD")
                    seq += 1
                    jobs.append((t, {"device": device, "job_id": "J%d-%06d" % (no, seq),
                                     "submitted_local": lstamp(t - dt.timedelta(seconds=int(r.integers(20, 300)))),
                                     "printed_local": lstamp(t), "job_name": "%s %s" % (kind, d.strftime("%d%b").upper()),
                                     "template": tmpl, "labels": nl,
                                     "status": "COMPLETED" if r.random() > 0.015 else "VOIDED"}))
    jobs.sort(key=lambda x: (x[0], x[1]["device"]))
    with open(os.path.join(target, F["printer"]), "w", encoding="utf-8") as f:
        for _, j in jobs:
            f.write(json.dumps(j, separators=(",", ":")) + "\n")
    n["printer"] = len(jobs)

    # --- integrity team: Thursday changeover checks (handheld export, local time), one sheet a month --------
    from openpyxl import Workbook
    from openpyxl.styles import Font
    wb = Workbook()
    wb.remove(wb.active)
    by_month = {}
    for (no, t, i, label, regp) in w.check_rows:
        by_month.setdefault(t.month, []).append((no, t, i, label, regp))
    initials = ["MD", "BA", "KW", "JR", "TP"]
    for mth, name in ((10, "Oct 2026"), (11, "Nov 2026"), (12, "Dec 2026")):
        ws = wb.create_sheet(name)
        ws.append(["Saltmarsh Market Price Integrity - Thursday changeover checks"])
        ws["A1"].font = Font(bold=True)
        ws.append(["Handheld export, %s. Times are store local." % name])
        hdr = ["Store", "Visit date", "Time checked", "EAN", "Description", "Label price", "Register price", "Match"]
        if mth == 12:
            hdr = hdr[:3] + ["Checked by"] + hdr[3:]
        ws.append(hdr)
        for (no, t, i, label, regp) in sorted(by_month.get(mth, []), key=lambda x: (x[1], x[0])):
            row = [STORE[no][2], t.date(), hhmm(t), ean13(w.upc[i]), w.desc[i], label, regp,
                   "Y" if abs(label - regp) < 0.005 else "N"]
            if mth == 12:
                row = row[:3] + [initials[(no + t.day) % len(initials)]] + row[3:]
            ws.append(row)
        for row in ws.iter_rows(min_row=4):
            for cell in row:
                if hdr[cell.column - 1] == "Visit date":
                    cell.number_format = "yyyy-mm-dd"
    xlsx_props(wb, "Saltmarsh Market Price Integrity", "Thursday changeover checks Q4 2026")
    p = os.path.join(target, F["checks"])
    wb.save(p)
    normalise_zip(p, P.file_stamp_utc("checks"))
    n["checks"] = len(w.check_rows)

    # --- integrity team: the weekly random price audit (CSV export, local time) -----------------------------
    rows = []
    aid = 0
    last = None
    for (no, t, i, label, regp) in sorted(w.audit_rows, key=lambda x: (x[0], x[1])):
        key = (no, t.date().isocalendar()[1])
        if key != last:
            aid += 1
            last = key
            line = 0
            start = t
        line += 1
        rows.append(["PA-26Q4-%04d" % (aid * 7 + 113), STORE[no][2], start.strftime("%Y-%m-%d %H:%M"), line,
                     ean13(w.upc[i]), money(label), money(regp), "MATCH" if abs(label - regp) < 0.005 else "MISMATCH",
                     initials[(aid * 3) % len(initials)]])
    write_csv(os.path.join(target, F["audits"]),
              ["audit_id", "store", "audit_started", "line", "ean", "shelf_price", "register_price", "result",
               "auditor"], rows)
    n["audits"] = len(rows)

    # --- store directory ---------------------------------------------------------------------------------
    wb = Workbook()
    ws = wb.active
    ws.title = "Stores"
    ws.append(["Store #", "POS name", "Store", "Zone", "Address", "Community", "Label printer", "Hours Mon-Sat",
               "Hours Sun"])
    addr = {101: ("6140 Quinpool Rd", "Halifax"), 102: ("Unit 4, 349 Herring Cove Rd", "Halifax"),
            103: ("278 Lacewood Dr", "Halifax"), 104: ("Bedford Place Mall, 1658 Bedford Hwy", "Bedford"),
            105: ("118 Portland St", "Dartmouth"), 106: ("920 Cole Harbour Rd", "Dartmouth"),
            107: ("Sackville Centre, 752 Sackville Dr", "Lower Sackville"), 201: ("68 Prince St", "Truro"),
            202: ("610 East River Rd", "New Glasgow"), 203: ("Antigonish Mall, 133 Church St", "Antigonish"),
            204: ("9256 Commercial St", "New Minas"), 205: ("Bridgewater Mall, 421 LaHave St", "Bridgewater"),
            206: ("Unit 2, 76 Starrs Rd", "Yarmouth"), 207: ("157 South Albion St", "Amherst")}
    for s in P.STORES:
        no = s[0]
        ws.append([no, s[1], s[2], "Zone %d" % s[4], addr[no][0], addr[no][1],
                   "SM-%s-ZT411-0%d" % (s[3], 1 if no % 3 else 2), "8:00 - 22:00", "9:00 - 21:00"])
    ws2 = wb.create_sheet("Holiday hours")
    ws2.append(["Date", "Hours", "Note"])
    for d in P.CLOSED:
        ws2.append([d, "Closed", "Retail closing day (Nova Scotia)"])
    for d, h in sorted(P.SHORT_CLOSE.items()):
        ws2.append([d, "8:00 - %d:00" % h, "Early close"])
    for row in ws2.iter_rows(min_row=2):
        row[0].number_format = "yyyy-mm-dd"
    xlsx_props(wb, "Saltmarsh Market Store Operations", "Store directory January 2027")
    p = os.path.join(target, F["stores"])
    wb.save(p)
    normalise_zip(p, P.file_stamp_utc("stores"), created="2025-03-04T14:12:00Z")
    n["stores"] = len(P.STORES)

    # --- the governing standard ------------------------------------------------------------------------
    import docs
    docs.standard(os.path.join(target, F["standard"]))

    # asks and distractors
    import asks_pack
    n.update(asks_pack.write(target, w, r))

    for key, fn in F.items():
        ts = dt.datetime(*P.file_stamp(key)).timestamp()
        os.utime(os.path.join(target, fn), (ts, ts))
    return w, n
