"""Cut the pack: the price paid files and the January 2027 update, the postcode directory and ward codes, the building
control register, the Agency's methodology, programme rules, pipeline and start-on-site claims, the field guide, the
request, and two context files. Every file is written from world.py's history; nothing here reads solve.py."""
import csv
import datetime as dt
import io
import math
import os
import re
import zipfile
from collections import defaultdict
from email.message import EmailMessage
from email.utils import format_datetime

import numpy as np
import openpyxl
from openpyxl.styles import Font
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import params as P
import world as Wm

FILES = {
    "pp_hist": "pp-harrowmere-2015-2025.csv",
    "pp_2026": "pp-harrowmere-2026.csv",
    "pp_update": "pp-monthly-update-2027-01.csv",
    "postcodes": "harrowmere_postcode_directory_2026-11.csv",
    "wards": "ward_codes_names_2019_2023.csv",
    "register": "hcc_building_control_completions_2015-2026.xlsx",
    "method": "hvha_ward_house_price_index_methodology.pdf",
    "rules": "hvha_pressured_wards_uplift_2027-28_rules.pdf",
    "pipeline": "hvha_affordable_pipeline_2027-28.xlsx",
    "claims": "hvha_start_on_site_claims_2025-2027.csv",
    "request": "ward_uplift_committee_paper.eml",
    "official": "harrowmere_official_hpi_2015-2026.csv",
    "rents": "harrowmere_private_rents_by_ward_2023-2026.csv",
}
DISTRACTORS = ["official", "rents"]
AGENCY = "Harrowmere and Vale Housing Agency"
LAUA = "E06000913"
WARD19 = {name: P.WARD_CODES_2019[code] for code, name, *_ in P.WARDS}
WARD23 = {name: code for code, name, *_ in P.WARDS}
ABBREV = {"ROAD": "Rd", "STREET": "St", "AVENUE": "Ave", "GROVE": "Gr", "TERRACE": "Ter", "CLOSE": "Cl",
          "CRESCENT": "Cres", "DRIVE": "Dr", "LANE": "Ln", "PLACE": "Pl", "GARDENS": "Gdns", "COURT": "Ct"}
APPROVERS = ["Northline Building Control Ltd", "Pennant Approved Inspectors", "Quadrant BC Services"]


# ------------------------------------------------------------------------------------------------ writers

def _csv(path, header, rows, quote_all=False):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n", quoting=csv.QUOTE_ALL if quote_all else csv.QUOTE_MINIMAL)
    if header:
        w.writerow(header)
    w.writerows(rows)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(buf.getvalue())


def _xlsx(path, sheets, creator, created, modified, widths=None):
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    for title, rows, bold, fmt in sheets:
        ws = wb.create_sheet(title)
        for r in rows:
            ws.append(list(r))
        for i in bold:
            for c in ws[i]:
                c.font = Font(bold=True)
        for col, nf in (fmt or {}).items():
            for c in ws[col][1:]:
                c.number_format = nf
        for k, wdt in enumerate(widths or [12, 14, 28, 22, 12, 24, 40, 18, 14, 26, 10, 10, 16]):
            ws.column_dimensions[openpyxl.utils.get_column_letter(k + 1)].width = wdt
        ws.freeze_panes = "A2" if title not in ("Notes", "About", "Export") else None
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
            "cell": ParagraphStyle("c", parent=base, fontSize=8.4, leading=10.5, spaceAfter=0)}


def pdf(path, blocks, title, author, created, modified, footer, widths=None):
    st = _styles()

    def page(canvas, d):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.5)
        canvas.setFillColor(colors.HexColor("#5b6670"))
        canvas.drawString(20 * mm, 10 * mm, footer)
        canvas.drawRightString(A4[0] - 20 * mm, 10 * mm, "Page %d" % d.page)
        canvas.restoreState()
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm,
                            bottomMargin=18 * mm, title=title, author=author, creator=author, producer=author,
                            invariant=1)
    story = []
    for kind, val in blocks:
        if kind == "table":
            width = A4[0] - 40 * mm
            n = len(val[0])
            ws = widths or ([width * 0.24] + [width * 0.76 / (n - 1)] * (n - 1) if n > 1 else [width])
            rows = [[Paragraph(str(c).replace("&", "&amp;"), st["cell"]) for c in r] for r in val]
            t = Table(rows, colWidths=ws, hAlign="LEFT", repeatRows=1)
            t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.HexColor("#8a949c")),
                                   ("VALIGN", (0, 0), (-1, -1), "TOP"), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
            story += [t, Spacer(1, 6)]
        else:
            story.append(Paragraph(val, st[kind]))
    doc.build(story, onFirstPage=page, onLaterPages=page)
    data = open(path, "rb").read()
    data = re.sub(rb"/CreationDate \(D:[^)]*\)", b"/CreationDate (" + created.encode() + b")", data)
    data = re.sub(rb"/ModDate \(D:[^)]*\)", b"/ModDate (" + modified.encode() + b")", data)
    for sig in (b"ReportLab Generated PDF document (opensource)", b"ReportLab generated PDF document -- digest (opensource)"):
        data = data.replace(sig, b" " * len(sig))
    open(path, "wb").write(data)


# ------------------------------------------------------------------------------------------------ helpers

def guid(r):
    h = "".join("0123456789ABCDEF"[int(x)] for x in r.integers(0, 16, size=32))
    return "{%s-%s-%s-%s-%s}" % (h[:8], h[8:12], h[12:16], h[16:20], h[20:])


def round_price(r, p):
    u = r.random()
    if u < 0.72:
        return int(round(p / 500.0) * 500)
    if u < 0.9:
        return int(round(p / 50.0) * 50)
    return int(round(p))


def title_street(st, r, abbrev_p):
    words = st.split()
    if words and words[-1] in ABBREV and r.random() < abbrev_p:
        words[-1] = ABBREV[words[-1]].upper()
    return " ".join(w.capitalize() if not w.isdigit() else w for w in words)


# ------------------------------------------------------------------------------------------------ price paid

def price_paid(W):
    """the transfer records as the registry publishes them: (record, registered date, kind), plus the update rows"""
    r = Wm.rng("ppd")
    recs = []        # dict with every column and 'reg' (registration date), 'truth' fields for checks
    # recoded postcodes: a few streets had their postcodes recoded in June 2021
    recode = {}
    pcs = [pc for pc in W.stock_pcs if pc not in W.moved]
    for pc in [pcs[int(k)] for k in r.choice(len(pcs), size=0, replace=False)]:
        new = None
        while True:
            cand = pc[:4] + "%d%s%s" % (int(r.integers(1, 10)), Wm.UNIT_LETTERS[int(r.integers(0, 20))],
                                       Wm.UNIT_LETTERS[int(r.integers(0, 20))])
            if cand not in W.used_pc:
                W.used_pc.add(cand)
                new = cand
                break
        recode[pc] = new
    W.recode = recode
    loc_streets = {}
    for ward, st, _pcs in W.streets:
        if st not in loc_streets:
            loc_streets[st] = ""
    villages = {"Pellbury": "PELLBURY", "Gorsey Hill": "GORSEY", "Dunmore": "DUNMORE VILLAGE", "Hollin Edge": "HOLLINS"}
    for ward, st, _pcs in W.streets:
        if ward in villages and r.random() < 0.3:
            loc_streets[st] = villages[ward]
    for s in W.sales:
        d = W.dw[s["dw"]]
        pc = d["postcode"]
        if pc in recode and s["date"] >= dt.date(2021, 6, 1):
            pc = recode[pc]
        lag = int(min(400, max(6, r.lognormal(math.log(34), 0.55))))
        rec = dict(id=guid(r), price=round_price(r, s["price"]), date=s["date"], postcode=pc, ptype=d["ptype"],
                   new=s["new"], duration=d["duration"], paon=d["paon"], saon=d["saon"], street=d["street"],
                   locality=loc_streets.get(d["street"], ""), cat=s["cat"], reg=s["date"] + dt.timedelta(days=lag),
                   dw=s["dw"], kind=s["kind"])
        recs.append(rec)
    # other property (land, garages, shops) in the additional category
    for k in range(70):
        ward = P.WARDS[int(r.integers(0, 12))][1]
        sts = [x for x in W.streets if x[0] == ward]
        _, st, spcs = sts[int(r.integers(0, len(sts)))]
        dd = dt.date(2015, 1, 1) + dt.timedelta(days=int(r.integers(0, 4380)))
        recs.append(dict(id=guid(r), price=int(round(float(r.lognormal(math.log(140000), 0.8)) / 500) * 500),
                         date=dd, postcode=spcs[0], ptype="O", new="N", duration="F",
                         paon=["LAND AT", "GARAGE AT", "UNIT 1", "WORKSHOP"][int(r.integers(0, 4))] +
                         ("" if r.random() < 0.5 else " %d" % int(r.integers(1, 90))),
                         saon="", street=st, locality="", cat="B", reg=dd + dt.timedelta(days=int(r.integers(10, 90))),
                         dw=None, kind="other"))
    # portfolio transfers: one deed, one price, entered on every title it covers
    ports = []
    sold26 = {s["dw"] for s in W.sales if s["date"].year >= 2026}

    def pick_block(ward, ptype, n, same_street):
        groups = defaultdict(list)
        for i, d in enumerate(W.dw):
            if d["ward"] == ward and d["ptype"] == ptype and i not in sold26 and not d.get("converted") \
                    and d["built"] is None:
                groups[(d["postcode"], d["paon"]) if ptype == "F" else d["street"]].append(i)
        keys = sorted(k for k, v in groups.items() if len(v) >= n)
        if not keys:
            keys = sorted(groups, key=lambda k: (-len(groups[k]), k))[:1]
        k = keys[int(r.integers(0, len(keys)))]
        return groups[k][:n]
    for ward, ptype, n, when, total in [("Calder Bank", "F", 18, dt.date(2026, 5, 29), 2646000),
                                        ("Fennick", "T", 7, dt.date(2026, 9, 11), 1212500),
                                        ("Gorsey Hill", "S", 5, dt.date(2026, 2, 20), 1377000),
                                        ("Eastholme", "F", 9, dt.date(2025, 11, 7), 1093500),
                                        ("Hollin Edge", "T", 6, dt.date(2026, 10, 16), 987000),
                                        ("Abbots Hollow", "F", 12, dt.date(2026, 6, 26), 1524000),
                                        ("Dunmore", "D", 4, dt.date(2026, 3, 13), 1835000),
                                        ("Wexley", "T", 8, dt.date(2026, 8, 21), 1348000),
                                        ("Moss Brow", "S", 6, dt.date(2026, 4, 24), 1269000),
                                        ("Brindley Moor", "T", 5, dt.date(2026, 7, 10), 905000)]:
        ids = pick_block(ward, ptype, n, True)
        n = len(ids)
        lag = int(r.integers(30, 70))
        pid = len(ports)
        for i in ids:
            d = W.dw[i]
            recs.append(dict(id=guid(r), price=total, date=when, postcode=d["postcode"], ptype=d["ptype"], new="N",
                             duration=d["duration"], paon=d["paon"], saon=d["saon"], street=d["street"], locality="",
                             cat="B", reg=when + dt.timedelta(days=lag), dw=i, kind="portfolio", portfolio=pid))
            sold26.add(i)
        ports.append(dict(ward=ward, n=n, date=when, total=total))
    W.portfolios = ports
    # two companies each buying two dwellings the same day at the same price, on separate deeds
    for ward, ptype, when, price, k in [("Wexley", "F", dt.date(2026, 3, 27), 118000, 2),
                                        ("Kestrel Rise", "T", dt.date(2026, 7, 31), 189950, 2),
                                        ("Brindley Moor", "S", dt.date(2026, 1, 30), 214500, 3),
                                        ("Pellbury", "T", dt.date(2026, 9, 25), 167000, 2),
                                        ("Eastholme", "T", dt.date(2026, 5, 8), 176500, 2),
                                        ("Calder Bank", "F", dt.date(2026, 4, 17), 132500, 3),
                                        ("Moss Brow", "S", dt.date(2026, 6, 12), 198000, 2),
                                        ("Abbots Hollow", "T", dt.date(2026, 10, 9), 181500, 2)]:
        cands = [i for i, d in enumerate(W.dw) if d["ward"] == ward and d["ptype"] == ptype and i not in sold26
                 and d["built"] is None and not d.get("converted")]
        first = cands[int(r.integers(0, len(cands)))]
        same = [i for i in cands if W.dw[i]["street"] == W.dw[first]["street"] and i != first]
        picks = [first] + same[:k - 1]
        for i in picks:
            d = W.dw[i]
            recs.append(dict(id=guid(r), price=price, date=when, postcode=d["postcode"], ptype=d["ptype"], new="N",
                             duration=d["duration"], paon=d["paon"], saon=d["saon"], street=d["street"], locality="",
                             cat="B", reg=when + dt.timedelta(days=int(r.integers(20, 60))), dw=i, kind="twin"))
            sold26.add(i)
    # the registry's own corrections and withdrawals, published in the January 2027 update
    upd = []
    published = [x for x in recs if x["reg"] <= P.EXTRACT]
    late = [x for x in recs if P.EXTRACT < x["reg"] <= P.UPDATE_END]
    for x in late:
        upd.append(dict(x, status="A"))
    # duplicates registered twice: the second entry is withdrawn by the update
    dupes = []
    pool = [x for x in published if x["cat"] == "A" and x["kind"] in ("sale", "newsale")]
    for k in r.choice(len(pool), size=34, replace=False):
        x = dict(pool[int(k)])
        x["id"] = guid(r)
        x["reg"] = x["reg"] + dt.timedelta(days=int(r.integers(1, 20)))
        x["dupe"] = True
        dupes.append(x)
        upd.append(dict(x, status="D"))
    published += dupes
    # changes: a price keyed with two digits swapped, a postcode corrected, a standard entry that was a company
    # purchase, a transfer date corrected; the published row carries the error, the update the corrected record
    pool = [x for x in published if not x.get("dupe") and x["kind"] in ("sale", "newsale", "flipbuy")]
    picks = [pool[int(k)] for k in r.choice(len(pool), size=160, replace=False)]
    for j, x in enumerate(picks):
        kind = ["price", "price", "postcode", "category", "date", "ptype"][j % 6]
        good = dict(x)
        if kind == "price":
            s = str(x["price"])
            if len(s) >= 6 and s[1] != s[2]:
                bad = s[0] + s[2] + s[1] + s[3:]
                x["price"] = int(bad)
            else:
                x["price"] = x["price"] + 10000
        elif kind == "postcode":
            sts = [p for (w, st, pp) in W.streets if st == x["street"] for p in pp if p != x["postcode"]]
            if not sts:
                continue
            x["postcode"] = sts[0]
        elif kind == "category":
            if x["cat"] != "A":
                continue
            good["cat"] = "B"
            x["cat"] = "A"
        elif kind == "date":
            x["date"] = x["date"] + dt.timedelta(days=int(r.choice([-31, -1, 1, 30])))
        elif kind == "ptype":
            if x["ptype"] not in ("S", "T"):
                continue
            x["ptype"] = "T" if x["ptype"] == "S" else "S"
        x["changed"] = kind
        upd.append(dict(good, status="C", changed=kind))
    W.ppd_published = published
    W.ppd_update = upd
    W.ppd_all = recs
    return published, upd


def ppd_row(x, status="A"):
    return [x["id"], str(x["price"]), x["date"].strftime("%Y-%m-%d 00:00"), x["postcode"], x["ptype"], x["new"],
            x["duration"], x["paon"], x["saon"], x["street"], x["locality"], P.TOWN, P.TOWN, P.TOWN,
            x["cat"], status]


PPD_HEADER = ["Transaction unique identifier", "Price", "Date of Transfer", "Postcode", "Property Type", "Old/New",
              "Duration", "PAON", "SAON", "Street", "Locality", "Town/City", "District", "County", "PPD Category Type",
              "Record Status - monthly file only"]


def write_ppd(W, target):
    published, upd = price_paid(W)
    key = lambda x: (x["date"], x["postcode"], x["paon"], x["saon"], x["id"])
    hist = sorted([x for x in published if x["date"].year <= 2025], key=key)
    y26 = sorted([x for x in published if x["date"].year == 2026], key=key)
    _csv(os.path.join(target, FILES["pp_hist"]), PPD_HEADER, [ppd_row(x) for x in hist], quote_all=True)
    _csv(os.path.join(target, FILES["pp_2026"]), PPD_HEADER, [ppd_row(x) for x in y26], quote_all=True)
    upd_rows = sorted(upd, key=lambda x: ({"A": 0, "C": 1, "D": 2}[x["status"]],) + key(x))
    _csv(os.path.join(target, FILES["pp_update"]), PPD_HEADER, [ppd_row(x, x["status"]) for x in upd_rows],
         quote_all=True)
    return len(hist), len(y26), len(upd_rows)


# ------------------------------------------------------------------------------------------------ postcodes

def write_postcodes(W, target):
    r = Wm.rng("postcodes")
    ward_of = {}
    intro = {}
    for ward, st, pcs in W.streets:
        for pc in pcs:
            ward_of.setdefault(pc, ward)
    for d in W.dw:
        if d["built"]:
            intro.setdefault(d["postcode"], d["built"].year * 100 + max(1, d["built"].month - 2))
    rows = []
    recode_back = {v: k for k, v in W.recode.items()}
    for pc in sorted(W.used_pc):
        base = recode_back.get(pc, pc)
        ward = ward_of.get(base)
        if ward is None:
            continue
        w19 = W.moved.get(base, ward)
        di = intro.get(base, 198001 + int(r.integers(0, 30)) * 100)
        dterm = ""
        if pc in W.recode:
            dterm = "202106"
        if pc in recode_back:
            di = 202106
        e = 431000 + int(r.integers(0, 9000))
        n = 452000 + int(r.integers(0, 9000))
        pcd7 = pc if len(pc) == 7 else pc.replace(" ", "  ") if len(pc) == 6 else pc
        rows.append([pcd7, pc, str(di), dterm, LAUA, WARD23[ward], WARD19[w19], "E0109%05d" % (sum(map(ord, pc)) % 99999),
                     "0", str(e), str(n)])
    _csv(os.path.join(target, FILES["postcodes"]),
         ["pcd7", "pcds", "dointr", "doterm", "laua", "wd23cd", "wd19cd", "lsoa21", "usertype", "oseast1m", "osnrth1m"],
         rows)
    names = [[WARD23[n], n, WARD19[n], n] for _c, n, *_ in sorted(P.WARDS, key=lambda w: w[0])]
    _csv(os.path.join(target, FILES["wards"]), ["WD23CD", "WD23NM", "WD19CD", "WD19NM"], names)
    W.ward_of_pc = ward_of
    return len(rows)


# ------------------------------------------------------------------------------------------------ register

DESC = {
    "Extension (single storey)": ["Single storey rear extension", "Single storey side extension",
                                  "Single storey rear and side extension"],
    "Extension (two storey)": ["Two storey side extension", "Two storey rear extension"],
    "Loft conversion": ["Loft conversion with rear dormer", "Loft conversion with velux windows",
                        "Hip to gable loft conversion with rear dormer"],
    "Garage conversion": ["Conversion of integral garage to habitable room", "Garage conversion to living room"],
}


def register_rows(W):
    r = Wm.rng("register")
    rows = []    # dict: system, ref, received, completed, paon, saon, street, postcode, wtype, desc, created, lost,
    #              body, cert, ward19 (stale), truth fields
    seq = defaultdict(int)
    rr = Wm.rng("refs")

    def ref(system, d, kind):
        # each system numbers its applications through the year; other kinds of application take numbers between
        seq[(system, d.year)] += int(rr.integers(1, 7))
        n = 40 + seq[(system, d.year)]
        if system == "legacy":
            return "%s/%d/%04d" % ("FP" if kind == "FP" else "BN", d.year, n)
        return "%02d/%05d/%s" % (d.year % 100, n, kind)
    def pc_on(pc, when):
        return W.recode.get(pc, pc) if when >= dt.date(2021, 6, 1) else pc
    for w in W.works:
        d = W.dw[w["dw"]]
        if w["date"] > dt.date(2026, 12, 31):
            continue
        system = "legacy" if w["date"] < dt.date(2021, 1, 1) else "uniform"
        if w.get("flip"):
            wt = "Loft conversion"
            desc = "Loft conversion with rear dormer and %s rear extension" % (
                "two storey" if w.get("two_storey") else "single storey")
            body = APPROVERS[int(r.integers(0, 3))] if r.random() < 0.6 else "Harrowmere BC"
        else:
            wt = w["wtype"]
            desc = DESC[wt][int(r.integers(0, len(DESC[wt])))]
            body = APPROVERS[int(r.integers(0, 3))] if r.random() < 0.28 else "Harrowmere BC"
        rows.append(dict(system=system, ref=ref(system, w["received"], "FP" if r.random() < 0.55 else "BN"),
                         received=w["received"], completed=w["date"], paon=d["paon"], saon=d["saon"],
                         street=d["street"], postcode=pc_on(d["postcode"], w["date"]), wtype=wt, desc=desc,
                         created=0, lost=0,
                         body=body, cert="Final certificate" if body != "Harrowmere BC" else "Completion certificate",
                         ward=d["ward"], ward19=d["ward19"], dw=w["dw"], kind="work", flip=w.get("flip", False)))
    # new dwellings: a certificate per plot for houses, one per block for flats
    by_block = defaultdict(list)
    for e in W.new_events:
        if e["block"]:
            by_block[(e["site"], e["year"], e["paon"])].append(e)
        else:
            system = "legacy" if e["date"] < dt.date(2021, 1, 1) else "uniform"
            rows.append(dict(system=system, ref=ref(system, e["date"] - dt.timedelta(days=400), "FP"),
                             received=e["date"] - dt.timedelta(days=int(r.integers(300, 600))), completed=e["date"],
                             paon=e["paon"], saon="", street=e["street"], postcode=e["postcode"],
                             wtype="New dwelling(s)", desc="Erection of dwelling (plot %d, %s)" % (
                                 W.dw[e["dwelling"]]["plot"], e["site"].title()),
                             created=1, lost=0, body=APPROVERS[0] if r.random() < 0.7 else "Harrowmere BC",
                             cert="Final certificate", ward=e["ward"], ward19=e["ward19"], dw=e["dwelling"], kind="new"))
            rows[-1]["cert"] = "Final certificate" if rows[-1]["body"] != "Harrowmere BC" else "Completion certificate"
    for (site, year, paon), es in sorted(by_block.items()):
        last = max(e["date"] for e in es)
        n = len(es)
        system = "legacy" if last < dt.date(2021, 1, 1) else "uniform"
        e0 = es[0]
        base = dict(system=system, ref=ref(system, last - dt.timedelta(days=500), "FP"),
                    received=last - dt.timedelta(days=int(r.integers(420, 700))), completed=last, paon=paon, saon="",
                    street=e0["street"], postcode=e0["postcode"], wtype="New dwelling(s)",
                    desc="Erection of %d storey block of %d flats" % (4 if n < 40 else 6, n), created=n, lost=0,
                    body="Harrowmere BC", cert="Completion certificate", ward=e0["ward"], ward19=e0["ward19"], dw=None,
                    kind="newblock")
        if year == 2026:
            # the block was occupied floor by floor: a partial completion first, the completion certificate after;
            # the application's dwellings stand on both certificates
            part = dict(base, completed=dt.date(2026, 3, 20), cert="Partial completion", kind="newblock_partial")
            rows.append(part)
        rows.append(base)
    first_conv = set()
    for c in sorted(W.conv, key=lambda c: (c["date"], c["ward"])):
        uniform = c["date"] >= dt.date(2021, 1, 1)
        system = "uniform" if uniform else "legacy"
        house = c["kind"] == "conversion"
        if c["kind"] == "demolition":
            rows.append(dict(system=system, ref=ref(system, c["date"] - dt.timedelta(days=300), "FP"),
                             received=c["date"] - dt.timedelta(days=int(r.integers(200, 500))), completed=c["date"],
                             paon=c["paon"], saon="", street=c["street"], postcode=c["postcode"], wtype="Demolition",
                             desc="Demolition of %d dwellings" % c["lost"], created=0, lost=c["lost"],
                             body="Harrowmere BC", cert="Completion certificate", ward=c["ward"], ward19=c["ward19"],
                             dw=None, kind="demolition", lost_true=c["lost"]))
            continue
        approver = r.random() < (0.8 if c["date"].year == 2026 else 0.35)
        if c["date"].year == 2026 and house and c["ward"] not in first_conv:
            approver = True
            first_conv.add(c["ward"])
        body = APPROVERS[int(r.integers(0, 3))] if approver else "Harrowmere BC"
        if uniform:
            # Uniform's picklist has one conversion type; an approver's final certificate reports the dwellings it
            # creates and leaves the dwellings lost blank
            wtype = "Conversion"
            desc = "Conversion of building into %d self-contained flats" % c["created"]
            lost = None if approver else (1 if house else 0)
        else:
            wtype = "Conversion to flats" if house else "Change of use to residential"
            desc = ("Conversion of dwelling into %d self-contained flats" % c["created"]) if house else \
                "Change of use of offices to %d flats" % c["created"]
            lost = 1 if house else 0
        rows.append(dict(system=system, ref=ref(system, c["date"] - dt.timedelta(days=200), "FP"),
                         received=c["date"] - dt.timedelta(days=int(r.integers(120, 300))), completed=c["date"],
                         paon=c["paon"], saon="", street=c["street"],
                         postcode=pc_on(c["postcode"], c["date"]) if house else c["postcode"],
                         wtype=wtype, desc=desc, created=c["created"], lost=lost, body=body,
                         cert="Final certificate" if approver else "Completion certificate", ward=c["ward"],
                         ward19=c["ward19"], dw=c["dwelling"], kind=c["kind"], lost_true=1 if house else 0))
    rows.sort(key=lambda x: (x["completed"], x["ref"]))
    return rows


def write_register(W, target):
    r = Wm.rng("register_fmt")
    rows = register_rows(W)
    W.register = rows
    legacy = [["Ref", "Received", "Site address", "Description of works", "Completed", "Ward", "Units +", "Units -"]]
    uni = [["Application", "Received", "House no/name", "Street", "Postcode", "Work type", "Description",
            "Certificate", "Certificate date", "Body", "Dwellings created", "Dwellings lost", "Ward"]]
    for x in rows:
        if x["system"] == "legacy":
            num = x["paon"].title() if not x["paon"].isdigit() else x["paon"]
            street = title_street(x["street"], r, 0.45)
            pc = x["postcode"]
            form = int(r.integers(0, 4))
            if x["saon"]:
                num = "%s, %s" % (x["saon"].title(), num)
            if form == 0:
                addr = "%s %s, Harrowmere %s" % (num, street, pc)
            elif form == 1:
                addr = "%s, %s, %s" % (num, street, pc)
            elif form == 2:
                addr = "%s %s %s" % (num, street.upper(), pc)
            else:
                addr = "%s %s, Harrowmere, %s" % (num, street, pc.replace(" ", ""))
            legacy.append([x["ref"], x["received"].strftime("%d/%m/%Y"), addr, x["desc"],
                           x["completed"].strftime("%d/%m/%Y"), x["ward"], x["created"] or None, x["lost"] or None])
        else:
            num = x["paon"].title() if not x["paon"].isdigit() else x["paon"]
            if x["saon"]:
                num = "%s, %s" % (x["saon"].title(), num)
            uni.append([x["ref"], x["received"].strftime("%Y-%m-%d"), num, title_street(x["street"], r, 0.35),
                        x["postcode"], x["wtype"], x["desc"], x["cert"], x["completed"].strftime("%Y-%m-%d"), x["body"],
                        x["created"], x["lost"], x["ward"]])
    notes = [["Harrowmere City Council, Building Control: completions"],
             ["BCsys export of 14 January 2021 (completions to 31 December 2020)"],
             ["Uniform export of 12 January 2027 (completions from 1 January 2021)"]]
    _xlsx(os.path.join(target, FILES["register"]),
          [("Legacy 2015-2020", legacy, [1], None), ("Uniform 2021-2026", uni, [1], None), ("Export", notes, [1], None)],
          "Gillian Lawson", dt.datetime(2027, 1, 12, 10, 41), dt.datetime(2027, 1, 13, 15, 6),
          widths=[16, 12, 42, 46, 12, 30, 44, 22, 14, 30, 10, 10, 16])
    return len(legacy) - 1, len(uni) - 1


# ------------------------------------------------------------------------------------------------ the Agency

PY0, PY1 = P.PY0, P.PY1
PROVIDERS = ["Calderstone Housing Association", "Brackwell Homes", "Harrowmere Community Homes", "Pennine Vale Housing",
             "Moorside Housing Trust", "Kestrel Homes Group"]
TARGET_HOMES = {"Calder Bank": 148, "Kestrel Rise": 96, "Abbots Hollow": 71, "Pellbury": 118, "Fennick": 64,
                "Wexley": 52, "Moss Brow": 88, "Eastholme": 40, "Brindley Moor": 36, "Hollin Edge": 30,
                "Dunmore": 22, "Gorsey Hill": 18}


def pipeline_rows(W):
    r = Wm.rng("pipeline")
    rows = []
    sid = 2700
    for code, ward, *_ in P.WARDS:
        total = TARGET_HOMES[ward]
        parts = []
        left = total
        while left > 0:
            m = int(min(left, r.integers(10, 52)))
            if left - m < 8:
                m = left
            parts.append(m)
            left -= m
        pcs = [p for (w, st, pp) in W.streets if w == ward for p in pp]
        for m in parts:
            sid += int(r.integers(1, 9))
            start = PY0 + dt.timedelta(days=int(r.integers(5, 355)))
            rows.append(dict(sid="HV-%d" % sid, ward=ward, homes=m, start=start, status=["Approved", "In contract"][int(r.integers(0, 2))],
                             postcode=pcs[int(r.integers(0, len(pcs)))], provider=PROVIDERS[int(r.integers(0, 6))],
                             counts=True))
        # schemes outside the programme year or not yet firm
        for k in range(int(r.integers(1, 4))):
            sid += int(r.integers(1, 9))
            kind = int(r.integers(0, 4))
            if kind == 0:
                start, status = PY0 - dt.timedelta(days=int(r.integers(1, 40))), "In contract"
            elif kind == 1:
                start, status = PY1 + dt.timedelta(days=int(r.integers(1, 60))), "Approved"
            elif kind == 2:
                start, status = PY0 + dt.timedelta(days=int(r.integers(30, 300))), "On hold"
            else:
                start, status = PY0 + dt.timedelta(days=int(r.integers(30, 300))), "Bid"
            rows.append(dict(sid="HV-%d" % sid, ward=ward, homes=int(r.integers(8, 40)), start=start, status=status,
                             postcode=pcs[int(r.integers(0, len(pcs)))], provider=PROVIDERS[int(r.integers(0, 6))],
                             counts=False))
    names = ["Fold", "Yard", "Row", "Court", "Mews", "Gardens", "Place"]
    for x in rows:
        x["name"] = "%s %s" % (Wm.STREET_WORDS[int(r.integers(0, len(Wm.STREET_WORDS)))], names[int(r.integers(0, 7))])
        sr = int(round(x["homes"] * float(r.uniform(0.3, 0.6))))
        so = int(round((x["homes"] - sr) * float(r.uniform(0.2, 0.6))))
        x["sr"], x["so"], x["ar"] = sr, so, x["homes"] - sr - so
        x["grant"] = int(round(x["homes"] * float(r.uniform(62000, 88000)) / 1000) * 1000)
        x["completion"] = x["start"] + dt.timedelta(days=int(r.integers(420, 760)))
    rows.sort(key=lambda x: x["sid"])
    return rows


def write_pipeline(W, target):
    rows = pipeline_rows(W)
    W.pipeline = rows
    out = [["Scheme ID", "Scheme", "Provider", "Ward", "Site postcode", "Homes", "Social rent", "Affordable rent",
            "Shared ownership", "Start on site (planned)", "Completion (planned)", "Status", "Grant (GBP)"]]
    for x in rows:
        out.append([x["sid"], x["name"], x["provider"], x["ward"], x["postcode"], x["homes"], x["sr"], x["ar"], x["so"],
                    dt.datetime.combine(x["start"], dt.time()), dt.datetime.combine(x["completion"], dt.time()),
                    x["status"], x["grant"]])
    about = [["Harrowmere and Vale Housing Agency: Affordable Homes Programme pipeline, Harrowmere schemes"],
             ["Programme year 2027-28 runs from 1 April 2027 to 31 March 2028."],
             ["Status: Bid (not yet assessed), Approved (grant approved), In contract (grant agreement signed), "
              "On hold."],
             ["Brackwell Homes merged into Calderstone Housing Association on 1 September 2026; Brackwell's schemes are"
              " shown under Calderstone."],
             ["Prepared by Investment Team, 22 January 2027."]]
    _xlsx(os.path.join(target, FILES["pipeline"]), [("Pipeline", out, [1], {"J": "dd/mm/yyyy", "K": "dd/mm/yyyy",
                                                                            "M": "#,##0"}), ("About", about, [1], None)],
          "Sylvia Davison", dt.datetime(2026, 11, 30, 9, 12), dt.datetime(2027, 1, 22, 16, 48),
          widths=[10, 22, 32, 16, 10, 8, 10, 10, 10, 14, 14, 12, 14])
    return len(rows)


def claims_rows(W):
    r = Wm.rng("claims")
    out = []
    cid = 51000
    pcs_of = {w: [p for (ww, st, pp) in W.streets if ww == w for p in pp] for _c, w, *_ in P.WARDS}
    st_of = {p: st for (ww, st, pp) in W.streets for p in pp}
    for code, ward, *_ in P.WARDS:
        n = int(r.integers(4, 10))
        for k in range(n):
            start = dt.date(2025, 4, 1) + dt.timedelta(days=int(r.integers(0, 640)))
            if start > dt.date(2026, 12, 31):
                start = dt.date(2026, 12, 31) - dt.timedelta(days=int(r.integers(0, 60)))
            pc = pcs_of[ward][int(r.integers(0, len(pcs_of[ward])))]
            homes = int(r.integers(8, 46))
            cid += int(r.integers(1, 30))
            sub = start + dt.timedelta(days=int(r.integers(6, 50)))
            status = "Paid" if sub < dt.date(2026, 12, 1) else "Approved"
            prov = PROVIDERS[int(r.integers(0, 6))]
            if prov == "Brackwell Homes" and start >= dt.date(2026, 8, 1):
                prov = "Calderstone Housing Association"
            out.append(dict(ref="SOS-%d" % cid, sid="HV-%d" % (2100 + cid % 500), ward=ward, postcode=pc,
                            street=st_of[pc], homes=homes, start=start, submitted=min(sub, dt.date(2027, 1, 28)),
                            status=status, provider=prov, kind="claim"))
    # starts that slipped: the claim was withdrawn and claimed again when the start came
    for k in range(5):
        x = out[int(r.integers(0, len(out)))]
        if x["start"].year != 2026 or x["start"].month > 9:
            continue
        cid += 7
        w = dict(x, ref="SOS-%d" % cid, start=x["start"] - dt.timedelta(days=int(r.integers(60, 200))),
                 status="Withdrawn", kind="withdrawn")
        w["submitted"] = w["start"] + dt.timedelta(days=10)
        out.append(w)
    # Brackwell Homes claimed its 2026 sites phase by phase; it merged into Calderstone Housing Association on
    # 1 September 2026, and Calderstone, which claims a site once for all its homes, claimed each Brackwell site
    # again under its own scheme reference, dated from the site's first start
    for ward in ["Abbots Hollow", "Calder Bank", "Dunmore", "Fennick", "Gorsey Hill", "Moss Brow", "Wexley",
                 "Eastholme", "Kestrel Rise"]:
        pc = pcs_of[ward][int(r.integers(0, len(pcs_of[ward])))]
        no = int(r.integers(1, 120))
        phases = 1 if ward in ("Eastholme", "Kestrel Rise") else int(r.choice([2, 2, 3]))
        d0 = dt.date(2026, 1, 12) + dt.timedelta(days=int(r.integers(0, 150)))
        homes = []
        for k in range(phases):
            cid += int(r.integers(2, 19))
            h = int(r.integers(8, 26))
            st0 = d0 + dt.timedelta(days=int(55 * k + r.integers(0, 20))) if k else d0
            out.append(dict(ref="SOS-%d" % cid, sid="HV-%d" % (2600 + cid % 200), ward=ward, postcode=pc,
                            street=st_of[pc], homes=h, start=st0, submitted=st0 + dt.timedelta(days=int(r.integers(9, 30))),
                            status="Paid", provider="Brackwell Homes", kind="phase", site_no=no))
            homes.append(h)
        cid += int(r.integers(3, 17))
        out.append(dict(ref="SOS-%d" % cid, sid="HV-%d" % (2900 + cid % 90), ward=ward, postcode=pc, street=st_of[pc],
                        homes=sum(homes), start=d0, submitted=dt.date(2026, 9, 7) + dt.timedelta(days=int(r.integers(0, 60))),
                        status="Approved" if r.random() < 0.4 else "Paid", provider="Calderstone Housing Association",
                        kind="reclaimed", site_no=no))
    for c in out:
        sr = int(round(c["homes"] * 0.45))
        so = int(round((c["homes"] - sr) * 0.4))
        c["sr"], c["so"], c["ar"] = sr, so, c["homes"] - sr - so
    out.sort(key=lambda c: (c["submitted"], c["ref"]))
    return out


def prog_quarter(d):
    fy = d.year if d.month >= 4 else d.year - 1
    q = (d.month - 4) % 12 // 3 + 1
    return "%d-%02d Q%d" % (fy, (fy + 1) % 100, q)


def write_claims(W, target):
    r = Wm.rng("claims_fmt")
    rows = claims_rows(W)
    W.claims = rows
    out = []
    for c in rows:
        num = int(r.integers(1, 120))
        site = "%s %s" % (c.get("site_no") or num, title_street(c["street"], r, 0.9 if c["kind"] == "reclaimed" else 0.1))
        c["site_no"] = c.get("site_no") or num
        out.append([c["ref"], "AHP 2025-28", c["sid"], c["provider"], "Land at %s" % site, c["postcode"],
                    str(c["homes"]), str(c["sr"]), str(c["ar"]), str(c["so"]), c["start"].strftime("%d/%m/%Y"),
                    c["submitted"].strftime("%d/%m/%Y"), c["status"], prog_quarter(c["start"])])
    _csv(os.path.join(target, FILES["claims"]),
         ["Claim ref", "Programme", "Scheme ID", "Provider", "Site", "Site postcode", "Homes", "Social rent",
          "Affordable rent", "Shared ownership", "Start on site", "Claim submitted", "Claim status",
          "Programme quarter"], out)
    return len(out)


# ------------------------------------------------------------------------------------------------ documents

def write_method(target):
    blocks = [("t", "Ward House Price Index: methodology"),
              ("s", "%s, Housing Market Analysis. Third edition, March 2024." % AGENCY),
              ("h", "1. What the index measures"),
              ("p", "The Ward House Price Index measures the change in house prices in each of Harrowmere's wards from"
                    " one calendar year to the next. It is a constant-quality index: it measures the change in the"
                    " price of the same dwelling at the same quality, not the change in the average price of whatever"
                    " happened to sell."),
              ("h", "2. Sales"),
              ("p", "The index uses standard price paid entries (category A) for dwellings (property types D, S, T and"
                    " F) in Harrowmere, as held in the price paid data with the latest monthly update applied. A new"
                    " dwelling's first sale is a standard sale. A dwelling's ward is its ward under the boundaries in"
                    " force from May 2023, found from its postcode."),
              ("h", "3. Construction"),
              ("p", "The index compares the prices paid for the same dwelling at two dates. A pair is two consecutive"
                    " standard sales of one dwelling, the dwelling identified by its address (primary and secondary"
                    " addressable objects, street and postcode). A ward's index is estimated from its pairs by"
                    " regressing the logarithm of each pair's price ratio on indicators for the calendar years of its"
                    " two sales (plus one for the year of the later sale, minus one for the year of the earlier), by"
                    " ordinary least squares, with 2015 = 100. A pair whose two sales fall in the same calendar year"
                    " carries no information on the annual index and drops out."),
              ("h", "4. Annual change and revisions"),
              ("p", "A ward's annual change is the percentage change in its index from one year to the next, published"
                    " to one decimal place. The whole series is estimated afresh each year on the full record, so the"
                    " published changes for earlier years can revise."),
              ("h", "5. Uses"),
              ("p", "The index supports the Agency's investment programmes and its published market commentary. Where"
                    " a programme rule refers to a ward's change in house prices, it means the change in this index.")]
    pdf(os.path.join(target, FILES["method"]), blocks, "Ward House Price Index: methodology", "Jodie Khan",
        "D:20240311141200+00'00'", "D:20240318093000+00'00'", "%s. Ward House Price Index: methodology, third edition" % AGENCY)


def write_rules(target):
    blocks = [("t", "Pressured Wards Uplift 2027-28: programme rules"),
              ("s", "%s. Approved by the Board, 14 October 2026." % AGENCY),
              ("h", "1. Purpose"),
              ("p", "The uplift adds grant to affordable homes in the Harrowmere wards where house prices are rising"
                    " fastest, where land and build costs move with them."),
              ("h", "2. Pressured wards"),
              ("p", "A ward is a pressured ward for 2027-28 if its Ward House Price Index rose by more than 5.0 per cent"
                    " from 2025 to 2026."),
              ("h", "3. The uplift"),
              ("p", "The uplift for 2027-28 is GBP 12,000,000. It is shared among the pressured wards in proportion to"
                    " the affordable homes in the Agency's 2027-28 pipeline that are due to start on site in the ward"
                    " in the programme year (1 April 2027 to 31 March 2028), counting schemes that are approved or in"
                    " contract. Each ward's share is rounded to the nearest pound."),
              ("h", "4. Timetable"),
              ("p", "The Investment Committee confirms the pressured wards and their shares in March 2027, on the 2026"
                    " index compiled from the price paid data as updated in January 2027.")]
    pdf(os.path.join(target, FILES["rules"]), blocks, "Pressured Wards Uplift 2027-28: programme rules",
        "Sylvia Davison", "D:20261008112000+01'00'", "D:20261015090500+01'00'",
        "%s. Pressured Wards Uplift 2027-28" % AGENCY)


def write_request(target):
    m = EmailMessage()
    m["From"] = "Sylvia Davison <sylvia.davison@hvha.org.uk>"
    m["To"] = "Jodie Khan <jodie.khan@hvha.org.uk>"
    m["Subject"] = "Pressured wards: paper for the March Investment Committee"
    m["Date"] = format_datetime(dt.datetime(2027, 2, 3, 8, 52, tzinfo=dt.timezone.utc))
    m["Message-ID"] = "<20270203085212.1842@hvha.org.uk>"
    m.set_content(
        "Jodie,\n\n"
        "The Investment Committee meets on 17 March to confirm the 2027-28 pressured wards and their shares of the"
        " uplift. Could I have the note and the workbook by 3 March?\n\n"
        "The 2026 price paid file and the January update are in the folder with the rest of the record back to 2015."
        " Gillian Lawson has sent the council's building control completions, so the paper can show what the city"
        " added in housing beside what it did to prices, and the providers' start-on-site claims are there to the end"
        " of January.\n\n"
        "Thanks,\n\n"
        "Sylvia Davison\nDirector of Investment, %s\n" % AGENCY)
    with open(os.path.join(target, FILES["request"]), "wb") as f:
        f.write(bytes(m))


def write_official(W, target):
    """the official local authority index: a mix-adjusted series for the whole city, monthly"""
    r = Wm.rng("official")
    weights = {name: n for c, name, n, *_ in P.WARDS}
    tot = sum(weights.values())
    rows = []
    prev = {}
    base = None
    sales_by_m = defaultdict(int)
    for s in W.sales:
        if s["cat"] == "A":
            sales_by_m[(s["date"].year, s["date"].month)] += 1
    levels = []
    for y in range(2015, 2027):
        for mth in range(1, 13):
            d = dt.date(y, mth, 15)
            lv = sum(weights[w] * math.exp(Wm.level(w, d)) for w in weights) / tot
            lv *= math.exp(0.006 * math.sin((mth - 3) / 12 * 2 * math.pi) + float(r.normal(0, 0.002)))
            levels.append((y, mth, lv))
    ref = [lv for (y, m_, lv) in levels if y == 2023 and m_ == 1][0]
    for k, (y, mth, lv) in enumerate(levels):
        idx = 100 * lv / ref
        avg = 171450 * lv / ref
        m1 = "" if k == 0 else "%.1f" % (100 * (lv / levels[k - 1][2] - 1))
        m12 = "" if k < 12 else "%.1f" % (100 * (lv / levels[k - 12][2] - 1))
        rows.append(["01/%02d/%d" % (mth, y), "Harrowmere", LAUA, "%d" % round(avg), "%.2f" % idx, m1, m12,
                     str(sales_by_m[(y, mth)] if (y, mth) < (2026, 10) else ""),
                     "%d" % round(avg * 1.72), "%d" % round(avg * 1.12), "%d" % round(avg * 0.93),
                     "%d" % round(avg * 0.71)])
    _csv(os.path.join(target, FILES["official"]),
         ["Date", "RegionName", "AreaCode", "AveragePrice", "Index", "1m%Change", "12m%Change", "SalesVolume",
          "DetachedPrice", "SemiDetachedPrice", "TerracedPrice", "FlatPrice"], rows)


def write_rents(target):
    r = Wm.rng("rents")
    rows = []
    for c, ward, n, mix, lev, growth, *_ in P.WARDS:
        for fy in ("2023-24", "2024-25", "2025-26"):
            g = {"2023-24": 0, "2024-25": 1, "2025-26": 2}[fy]
            for bed, base in (("1", 640), ("2", 760), ("3", 880), ("4+", 1150)):
                rent = base * math.exp((lev - 12.25) * 0.6 + 0.055 * g + float(r.normal(0, 0.02)))
                cnt = int(r.integers(14, 160))
                rows.append([ward, fy, bed, str(cnt), "%d" % (round(rent / 5) * 5)])
    _csv(os.path.join(target, FILES["rents"]), ["Ward", "Year", "Bedrooms", "Lettings", "Median monthly rent (GBP)"],
         rows)


def build(target):
    os.makedirs(target, exist_ok=True)
    W = Wm.simulate()
    counts = {}
    counts["ppd"] = write_ppd(W, target)
    counts["postcodes"] = write_postcodes(W, target)
    counts["register"] = write_register(W, target)
    counts["pipeline"] = write_pipeline(W, target)
    counts["claims"] = write_claims(W, target)
    write_method(target)
    write_rules(target)
    write_request(target)
    write_official(W, target)
    write_rents(target)
    stamp = dt.datetime(2027, 2, 3, 9, 0).timestamp()
    for k in FILES:
        os.utime(os.path.join(target, FILES[k]), (stamp, stamp))
    W.counts = counts
    return W


if __name__ == "__main__":
    import sys
    W = build(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "target"))
    print(W.counts)
