"""task285 pack builder: writes target/, golden/, generator/figures.json and metadata.json. Deterministic."""
import csv
import io
import json
import math
import os
import random
import shutil
import zipfile
from datetime import datetime, timedelta

import world as W
import asks as A

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")
EXPORT_TIME = (2026, 11, 2, 9, 30, 0)
EXPORT_TS = datetime(*EXPORT_TIME).timestamp()
R = random.Random(W.SEED)


# ----------------------------------------------------------------------------------------------- helpers
def write_csv(name, header, rows, folder=None):
    path = os.path.join(folder or TARGET, name)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\r\n" if name.startswith("police") else "\n")
        w.writerow(header)
        for r in rows:
            w.writerow(r)
    return path


def normalise_zip(path, modified="2026-11-02T09:12:00Z", member_time=(2026, 11, 2, 9, 30, 0)):
    """rewrite an OOXML zip with fixed member times and order, so rebuilds are byte-identical."""
    import re
    with zipfile.ZipFile(path) as z:
        items = [(i.filename, z.read(i.filename)) for i in z.infolist()]
    fixed = []
    for name, data in items:
        if name == "docProps/app.xml":
            data = re.sub(rb"<Application>[^<]*</Application>", b"<Application>Microsoft Excel</Application>", data)
            data = re.sub(rb"<AppVersion>[^<]*</AppVersion>", b"<AppVersion>16.0300</AppVersion>", data)
        if name == "docProps/core.xml":
            data = re.sub(rb"(<dcterms:modified[^>]*>)[^<]*(</dcterms:modified>)",
                          b"\\g<1>" + modified.encode() + b"\\g<2>", data)
        fixed.append((name, data))
    items = fixed
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in items:
            zi = zipfile.ZipInfo(name, date_time=member_time)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o600 << 16
            z.writestr(zi, data)


def wb_new(creator, title, created=datetime(2026, 10, 30, 16, 5, 0)):
    from openpyxl import Workbook
    wb = Workbook()
    p = wb.properties
    p.creator = creator
    p.lastModifiedBy = creator
    p.title = title
    p.created = created
    p.modified = datetime(2026, 11, 2, 9, 12, 0)
    return wb


def wb_save(wb, path, **kw):
    wb.save(path)
    normalise_zip(path, **kw)


def node_ids():
    rnd = random.Random(W.SEED + 3)
    ids, used = {}, set()
    for n in sorted(W.NODES):
        while True:
            v = "HBN-%04d" % rnd.randint(1100, 3999)
            if v not in used:
                used.add(v)
                ids[n] = v
                break
    return ids


NODE_ID = node_ids()


def link_ids():
    rnd = random.Random(W.SEED + 5)
    ids, ref19, used = {}, {}, set()
    for k, l in enumerate(W.LINKS):
        while True:
            v = "HBL-%05d" % rnd.randint(10000, 69999)
            if v not in used:
                used.add(v)
                break
        ids[k] = v
        ref19[k] = "L19-%04d" % (200 + 13 * k + rnd.randint(0, 9))
    # the 2019 survey carried the B5131 through Hollinside and through Ravelsby Bridge as single links
    k1 = [i for i, l in enumerate(W.LINKS) if (l[0], l[1]) == ("Bw7", "V1")][0]
    k2 = [i for i, l in enumerate(W.LINKS) if (l[0], l[1]) == ("V1", "Be7")][0]
    k3 = [i for i, l in enumerate(W.LINKS) if (l[0], l[1]) == ("Bw15", "V2")][0]
    k4 = [i for i, l in enumerate(W.LINKS) if (l[0], l[1]) == ("V2", "Be15")][0]
    ref19[k2] = ref19[k1]
    ref19[k4] = ref19[k3]
    return ids, ref19


LINK_ID, LINK19 = link_ids()


def km(a, b):
    (x1, y1), (x2, y2) = W.NODES[a], W.NODES[b]
    return math.hypot(x2 - x1, y2 - y1)


# ------------------------------------------------------------------------------------------- model files
def write_stages():
    for run, name, label in ((2025, "storage_area_stages_QRN25_D100CC.csv", "QRN25 D100CC"),
                             (2023, "storage_area_stages_QRN23_D100CC.csv", "QRN23 D100CC")):
        rows = []
        for sa in W.SA:
            for h in W.HOURS:
                rows.append([label, sa, h, "%.3f" % W.stage(sa, h, run)])
        write_csv(name, ["model_run", "storage_area", "hour_from_storm_start", "stage_mAOD"], rows)
    # July 2021 hindcast: the becks' event (Quarnell well within bank at the roads)
    rows = []
    t0 = datetime(2021, 7, 17, 22, 0)
    for sa in W.SA:
        _n, tp, wr, wf, base, peak = W.SA[sa]
        frac = 0.82 if sa.startswith(("SA-HB", "SA-SB", "SA-MW")) else 0.31
        for h in range(0, 49):
            tt = tp * 0.55 if sa.startswith(("SA-HB", "SA-SB", "SA-MW")) else tp * 0.6
            w = wr if h <= tt else wf
            v = base + (peak - base) * frac * math.exp(-0.5 * ((h - tt) / (w / 1.6)) ** 2)
            rows.append(["QRN25 JUL21H", sa, (t0 + timedelta(hours=h)).strftime("%Y-%m-%dT%H:%MZ"), "%.3f" % v])
    write_csv("storage_area_stages_QRN25_JUL21_hindcast.csv", ["model_run", "storage_area", "time_utc", "stage_mAOD"], rows)


def bng_ring(poly):
    ring = [list(W.bng(x, y)) for x, y in poly]
    return ring + [ring[0]]


def write_sa_geojson():
    feats = []
    for sa, poly in W.SA_POLY.items():
        feats.append({"type": "Feature", "properties": {"SA_ID": sa, "SA_NAME": W.SA[sa][0], "MODEL": "QRN25",
                                                         "RIVER": "Quarnell" if "LD" in sa else W.SA[sa][0].rsplit(" ", 1)[0]},
                      "geometry": {"type": "Polygon", "coordinates": [bng_ring(poly)]}})
    gj = {"type": "FeatureCollection", "name": "QRN25_storage_areas",
          "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:EPSG::27700"}}, "features": feats}
    with open(os.path.join(TARGET, "storage_areas_QRN25.geojson"), "w", encoding="utf-8") as f:
        json.dump(gj, f, separators=(",", ":"))


def write_network():
    feats = []
    for k, l in enumerate(W.LINKS):
        a, b, rn, name, cls, sa, d = l
        coords = [list(W.bng(*W.NODES[a])), list(W.bng(*W.NODES[b]))]
        feats.append({"type": "Feature",
                      "properties": {"LINK_ID": LINK_ID[k], "ROAD_NUMBER": rn, "ROAD_NAME": name,
                                     "ROAD_CLASS": {"A": "A Road", "B": "B Road", "C": "Classified Unnumbered",
                                                    "U": "Unclassified"}[cls],
                                     "START_NODE": NODE_ID[a], "END_NODE": NODE_ID[b],
                                     "LENGTH_M": int(round(km(a, b) * 1000 * 1.06))},
                      "geometry": {"type": "LineString", "coordinates": coords}})
    gj = {"type": "FeatureCollection", "name": "HB_highways_network_2025",
          "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:EPSG::27700"}}, "features": feats}
    with open(os.path.join(TARGET, "highways_network_2025.geojson"), "w", encoding="utf-8") as f:
        json.dump(gj, f, separators=(",", ":"))


def survey_points():
    """2019 highways levels survey: points every 20 to 30 m on every link inside the model's floodplain."""
    rnd = random.Random(W.SEED + 11)
    rows = []
    sp = 0
    done19 = {}
    for k, l in enumerate(W.LINKS):
        a, b, rn, name, cls, sa, d = l
        (x1, y1), (x2, y2) = W.NODES[a], W.NODES[b]
        L = math.hypot(x2 - x1, y2 - y1) * 1000
        n = max(2, int(L / rnd.uniform(20, 30)))
        ref = LINK19[k]
        base_ch = done19.get(ref, 0.0)
        low = W.link_peak_level(l)
        pts = []
        for j in range(n + 1):
            t = j / n
            x, y = round(x1 + t * (x2 - x1), 3), round(y1 + t * (y2 - y1), 3)
            s = W.sa_at(x, y)
            if s is None:
                continue
            pk = W.peak_stage(s)
            if sa is not None and s == sa:
                # dip profile: lowest at the middle third, rising to the embankment either side
                lev = low + 2.2 * (abs(t - 0.5) * 2) ** 2 + rnd.uniform(0, 0.03)
            else:
                lev = pk + rnd.uniform(0.6, 2.8)
            pts.append((j, t, x, y, lev, s))
        if sa is not None:
            # make sure the lowest surveyed point inside the dip's storage area carries the dip's lowest level
            mine = [q for q in range(len(pts)) if pts[q][5] == sa]
            assert mine, (a, b, sa)
            mid = sum(pts[q][1] for q in mine) / len(mine)
            jm = min(mine, key=lambda q: abs(pts[q][1] - mid))
            j, t, x, y, lev, s = pts[jm]
            pts[jm] = (j, t, x, y, low, s)
        for j, t, x, y, lev, s in pts:
            sp += 1
            e, nn = W.bng(x, y)
            rows.append(["SP19-%05d" % (40000 + 3 * sp + sp % 3), ref, "%.1f" % (base_ch + t * L), e, nn,
                         "%.2f" % lev, ("CL1", "CR1", "CL1", "CR1", "CL1", "CR1", "CL1")[(sp * 5 + len(ref)) % 7],
                         (datetime(2019, 5, 6) + timedelta(days=(sp // 40))).strftime("%d/%m/%Y")])
        done19[ref] = base_ch + L
    return rows


def write_survey_and_crosswalk():
    rows = survey_points()
    write_csv("highways_levels_survey_2019.csv",
              ["survey_point", "link_ref_2019", "chainage_m", "easting", "northing", "level_mAOD", "xsp",
               "survey_date"], rows)
    # crosswalk: 2019 link references to 2025 link identifiers (two 2019 links split at a village junction)
    cw = []
    seen = {}
    for k, l in enumerate(W.LINKS):
        ref = LINK19[k]
        (x1, y1), (x2, y2) = W.NODES[l[0]], W.NODES[l[1]]
        L = math.hypot(x2 - x1, y2 - y1) * 1000
        start = seen.get(ref, 0.0)
        cw.append([ref, LINK_ID[k], "%.1f" % start, "%.1f" % (start + L),
                   "split 2024 junction" if list(LINK19.values()).count(ref) > 1 else "renumbered"])
        seen[ref] = start + L
    write_csv("link_reference_crosswalk_2019_2025.csv",
              ["link_ref_2019", "link_id_2025", "from_chainage_m", "to_chainage_m", "change_type"], cw)
    return rows


def write_council_tax():
    rnd = random.Random(W.SEED + 13)
    rows = []
    for code, name, node, dw in W.PARISHES:
        shares = [rnd.uniform(0.5, 2.5) for _ in range(8)]
        s = sum(shares)
        bands = [int(dw * x / s) for x in shares]
        bands[2] += dw - sum(bands)
        rows.append([code, name] + bands + [dw])
    write_csv("council_tax_dwellings_by_parish_oct2026.csv",
              ["parish_code", "parish_name", "band_A", "band_B", "band_C", "band_D", "band_E", "band_F", "band_G",
               "band_H", "all_dwellings"], rows)


# --------------------------------------------------------------------------------------------- ask files
def write_register(reg):
    rows = []
    for r_ in reg:
        e, n = W.bng(r_["x"], r_["y"])
        rows.append([r_["uprn"], r_["parent"] or "", r_["cls"], r_["sao"], r_["pao"], r_["street"],
                     r_["parish"] if r_["code_shown"] == r_["code"] else W.OLD_PARISH[1], r_["code_shown"],
                     r_["pc"], e, n, "%.2f" % r_["ground_rec"], r_["src"], r_["built"]])
    rows.sort(key=lambda z: (z[7], z[5], z[0]))
    write_csv("address_register_extract_oct2026.csv",
              ["UPRN", "PARENT_UPRN", "CLASS", "SAO_TEXT", "PAO_TEXT", "STREET", "PARISH", "PARISH_CODE",
               "POSTCODE", "EASTING", "NORTHING", "GROUND_LEVEL_M", "LEVEL_SOURCE", "YEAR_BUILT"], rows)


def write_pfr_survey(sv):
    wb = wb_new("Quarnell Valley Community Foundation", "PFR property survey 2022")
    ws = wb.active
    ws.title = "Surveyed properties"
    ws.append(["Survey ref", "UPRN", "Address", "Parish", "Ground level (mAOD)", "Threshold level (mAOD)",
               "Ground floor units", "Storeys", "Surveyed"])
    for s in sv:
        ws.append([s["ref"], s["uprn"], s["addr"], s["parish"], round(s["ground"], 2), round(s["floor"], 2),
                   s["units"], s["storeys"], s["surveyed"].date()])
    for c, wdt in zip("ABCDEFGHI", [12, 14, 34, 18, 16, 18, 28, 8, 12]):
        ws.column_dimensions[c].width = wdt
    wb_save(wb, os.path.join(TARGET, "pfr_property_survey_2022.xlsx"))


def write_closures():
    rnd = random.Random(W.SEED + 17)
    rows = []
    for sid, road, loc, bars, p in A.SECTIONS:
        place = loc.split(",")[0]
        overlapping = len(bars) > 1 and bars[1][0] < bars[0][1]
        for j, (a, b) in enumerate(bars):
            if overlapping:
                pos = "%s, %s side" % (place, "west" if j == 0 else "east")
            else:
                pos = "%s" % place
            ref = A.REKEYED.get((sid, j), sid)
            rows.append([ref, road, loc, pos, a[8:10] + "/07/2021 " + a[11:], b[8:10] + "/07/2021 " + b[11:],
                         rnd.choice(["MG", "PL", "DK", "SW"]), "flood water on carriageway"])
    sid, road, loc, (a, b), _ = A.ROUTE
    rows.append([sid, road, loc, "diversion signed at both ends", a[8:10] + "/07/2021 " + a[11:],
                 b[8:10] + "/07/2021 " + b[11:], rnd.choice(["MG", "PL", "DK", "SW"]), "road closed, diversion in place"])
    rows.sort(key=lambda r: (r[4][6:10], r[4][3:5], r[4][0:2], r[4][11:]))
    write_csv("highways_road_closures_jul2021.csv",
              ["closure_ref", "road_number", "location", "barrier_position", "closed_local", "reopened_local",
               "duty_officer", "reason"], rows)
    pol = []
    used = set()
    for sid, road, loc, bars, p in A.SECTIONS:
        if not p:
            continue
        while True:
            inc = "SY-%04d-180721" % rnd.randint(1100, 1499)
            if inc not in used:
                used.add(inc)
                break
        place = loc.split(",")[-1].strip()
        remark = rnd.choice(["road closed by officers, flooding", "officers closed road, water over carriageway",
                             "closure in place, handed to highways"])
        if not p[1]:
            remark = "closure in place, handed to highways"
        pol.append([inc, "%s %s" % (road, place), p[0].replace(" ", "T") + "Z",
                    p[1].replace(" ", "T") + "Z" if p[1] else "", remark])
    pol.sort(key=lambda r: r[2])
    write_csv("police_road_closures_jul2021.csv",
              ["incident", "location_text", "closed_utc", "opened_utc", "remarks"], pol)


def write_ledger():
    wb = wb_new("Finance, Quarnell Valley Community Foundation", "Flood Ready 2026 transactions")
    ws = wb.active
    ws.title = "Transactions"
    ws.append(["Posted", "Type", "Reference", "Payee", "Method", "Cheque no", "Amount GBP"])
    lines = []
    for parish, ref, amt, var, pays in A.AWARDS_2026:
        payee = "%s Parish Council" % parish
        lines.append((datetime(2026, 2, 26), "AWARD", ref, payee, "", "", amt))
        if var:
            lines.append((datetime(2026, 6, 30), "VARIATION", var[1], payee, "", "", var[0]))
        for k, (d, m, a, ch) in enumerate(pays):
            r = ref
            to = payee
            if parish in A.MISREF and k == 1:
                r = A.MISREF[parish]
            if var and k == 1 and a == var[0]:
                r = var[1]
            if parish in A.PAYEE and k == 1:
                to = A.PAYEE[parish]
            lines.append((datetime.strptime(d, "%Y-%m-%d"), "PAYMENT", r, to, m, ch or "", a))
    lines.sort(key=lambda z: (z[0], z[2]))
    for d, t, r, p, m, ch, a in lines:
        ws.append([d.date(), t, r, p, m, ch, a])
    ws.column_dimensions["D"].width = 30
    bf = wb.create_sheet("2025 awards b-f")
    bf.append(["Reference", "Payee", "Award GBP", "Paid to 31/03/2026 GBP", "Balance GBP", "Status"])
    for ref, parish, amt in [("FR25-002", "Hollinside", 3600), ("FR25-006", "Lunnerby", 4100),
                             ("FR25-009", "Whinnerby", 2400), ("FR25-011", "Burnishaw", 3900),
                             ("FR25-014", "Tolmarsh", 2250), ("FR25-016", "Cottergill", 1600),
                             ("FR25-017", "Kestlebeck", 1350)]:
        bf.append([ref, "%s Parish Council" % parish, amt, amt, 0, "closed 31/03/2026"])
    bf.column_dimensions["B"].width = 30
    wb_save(wb, os.path.join(TARGET, "flood_ready_ledger_2026.xlsx"))
    rows = [["Quarnell Valley CF current a/c", "004817", "2026-03-18", "4480.00", "2026-09-22", "stale, 6 months unpresented"],
            ["Quarnell Valley CF current a/c", "004903", "2026-08-14", "900.00", "2026-10-19", "returned by payee bank, payee name"],
            ["Quarnell Valley CF current a/c", "004722", "2025-11-04", "1250.00", "2026-05-11", "stale, 6 months unpresented"]]
    write_csv("bank_cancelled_cheques_2026.csv",
              ["account", "cheque_no", "issue_date", "amount_gbp", "cancelled", "bank_note"], rows)


def write_distractors():
    wb = wb_new("Hawkesbridge Council Emergency Planning", "Rest centres 2026")
    ws = wb.active
    ws.title = "Rest centres"
    ws.append(["Centre", "Address", "Parish", "Capacity (persons)", "Kitchen", "Key holder ref", "Last checked"])
    for c in [("Whinnerby Village Hall", "Whinnerby Lane", "Whinnerby", 120, "Y", "KH-114", "2026-03-12"),
              ("Highfold Methodist Hall", "Highfold Road", "Highfold", 60, "N", "KH-121", "2025-11-02"),
              ("Nettlecote School", "Nettle Gill Lane", "Nettlecote", 240, "Y", "KH-102", "2026-05-20"),
              ("Quernby Moor Community Centre", "Quernby Moor Road", "Quernby Moor", 150, "Y", "KH-133", "2026-01-15"),
              ("Hawkesbridge Leisure Centre", "Moorgate", "Hawkesbridge North", 600, "Y", "KH-001", "2026-06-03"),
              ("Kestlebeck Reading Room", "Kestlebeck Lane", "Kestlebeck", 45, "N", "KH-140", "2024-09-18"),
              ("Tolmarsh Institute", "Tolmarsh Lane", "Tolmarsh", 90, "Y", "KH-128", "2026-02-27")]:
        ws.append(list(c))
    wb_save(wb, os.path.join(TARGET, "rest_centres_2026.xlsx"))
    feats = []
    for i, (code, name, poly) in enumerate([
            ("122WAF901", "River Quarnell at Whinnerby and Nettlecote", W.SA_POLY["SA-LD1"]),
            ("122WAF902", "River Quarnell at Yarrowcote and Burnishaw", W.SA_POLY["SA-LD3"]),
            ("122WAF903", "River Quarnell at Hepplewick and Quernby", W.SA_POLY["SA-LD5"]),
            ("122WAF904", "River Quarnell at Tolmarsh, Cottergill and Wrennick", W.SA_POLY["SA-LD7"]),
            ("122WAF905", "Hollin Beck at Hollinside", W.SA_POLY["SA-HB1"]),
            ("122WAF906", "Ravelsby Brook at Ravelsby Bridge", W.SA_POLY["SA-SB1"]),
            ("122WAF907", "Lunnerby Beck at Lunnerby", W.SA_POLY["SA-MW1"])]):
        feats.append({"type": "Feature", "properties": {"FWS_TACODE": code, "TA_NAME": name, "QDIAL": "Quarnell",
                                                         "DESCRIP": "Properties close to the river"},
                      "geometry": {"type": "Polygon", "coordinates": [bng_ring(poly)]}})
    with open(os.path.join(TARGET, "flood_warning_areas_2025.geojson"), "w", encoding="utf-8") as f:
        json.dump({"type": "FeatureCollection", "name": "flood_warning_areas", "features": feats}, f,
                  separators=(",", ":"))


# ------------------------------------------------------------------------------------------- documents
def _pdf(path, title, author, story_fn, stamp):
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate
    from reportlab.lib.units import mm

    def on_page(c, d):
        c.saveState()
        c.setFont("Helvetica", 7.5)
        c.drawString(18 * mm, 10 * mm, title)
        c.drawRightString(192 * mm, 10 * mm, "Page %d" % d.page)
        c.restoreState()

    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=18 * mm,
                            bottomMargin=18 * mm, title=title, author=author, subject="", creator=author,
                            producer=author, invariant=1)
    doc.build(story_fn(), onFirstPage=on_page, onLaterPages=on_page)
    _scrub_pdf(path, author, stamp)


def _scrub_pdf(path, org, stamp):
    """the writer's comment lines and its fixed invariant date replaced at equal byte length (xref offsets
    unchanged), then the file re-read with pypdf: same text, no parser complaint."""
    import re
    import logging
    from pypdf import PdfReader
    raw = open(path, "rb").read()
    before = [p.extract_text() for p in PdfReader(path).pages]
    n0 = len(raw)
    for pat in (rb"ReportLab Generated PDF document \(opensource\)",
                rb"ReportLab generated PDF document -- digest \(opensource\)"):
        for m in re.findall(pat, raw):
            raw = raw.replace(m, org.encode()[:len(m)].ljust(len(m)))
    raw = raw.replace(b"D:20000101000000", ("D:" + stamp).encode())
    assert len(raw) == n0 and b"eportLab" not in raw and b"reportlab" not in raw.lower()
    open(path, "wb").write(raw)
    cap = []
    h = logging.Handler()
    h.emit = lambda rec: cap.append(rec)
    logging.getLogger("pypdf").addHandler(h)
    try:
        after = [p.extract_text() for p in PdfReader(path).pages]
    finally:
        logging.getLogger("pypdf").removeHandler(h)
    assert after == before and not cap, (path, cap)


def styles():
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    ss = getSampleStyleSheet()
    body = ParagraphStyle("b", parent=ss["Normal"], fontName="Helvetica", fontSize=9.5, leading=12.5, spaceAfter=6)
    h = ParagraphStyle("h", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=11, spaceBefore=8, spaceAfter=4)
    t = ParagraphStyle("t", parent=ss["Title"], fontName="Helvetica-Bold", fontSize=15, spaceAfter=4, alignment=0)
    small = ParagraphStyle("s", parent=body, fontSize=8, leading=10)
    return body, h, t, small


def write_guidance():
    from reportlab.platypus import Paragraph, Spacer, Table, TableStyle
    from reportlab.lib import colors
    body, h, t, small = styles()

    def story():
        s = [Paragraph("Quarnell Valley Community Foundation", small),
             Paragraph("Flood Ready Fund 2027: grant guidance", t),
             Paragraph("Approved by the trustees on 24 September 2026. Owner: Gareth Johnston, Grants Manager. "
                       "Version 3. Replaces the 2026 guidance.", small), Spacer(1, 6),
             Paragraph("1. What the fund pays for", h),
             Paragraph("Flood Ready grants equip a parish to look after itself when floodwater closes its roads: a "
                       "community flood store, a satellite telephone and a volunteer first responder kit, held by the "
                       "parish council and checked each spring. The 2027 round also offers property flood resilience "
                       "survey vouchers to households in every parish of the valley.", body),
             Paragraph("2. Which parishes qualify for a 2027 Flood Ready grant", h),
             Paragraph("A parish qualifies when the design flood would cut its main village off from Hawkesbridge "
                       "General Hospital. A village is cut off when it has no road route to the hospital that an "
                       "emergency ambulance could use. The county ambulance service's crews will not take a "
                       "vehicle along a carriageway where floodwater stands deeper than 0.25 m.", body),
             Paragraph("The design flood is the 1 in 100 annual chance event with the 2080s central climate change "
                       "allowance in the 2025 Quarnell model (model QRN25, run D100CC), which superseded the 2023 model "
                       "in March 2026. Road routes are the public highways in the council's 2025 network; carriageway "
                       "levels are the highways authority's 2019 levels survey, which covers every road inside the "
                       "model's floodplain. The hospital is reached at its emergency department entrance on Infirmary "
                       "Road (network node HBN-%s). Each parish's main village and its access point on the network are "
                       "listed in Annex A." % NODE_ID["H"][4:], body),
             Paragraph("3. Grant amount", h),
             Paragraph("The trustees have set aside GBP 30,000 for the 2027 round. Each qualifying parish receives a "
                       "base grant of GBP 3,000 and a share of the rest of the GBP 30,000 in proportion to its "
                       "households: the rest multiplied by the parish's households and divided by the households of all "
                       "the qualifying parishes. Households are the dwellings on the council tax valuation list for the "
                       "parish at 1 October 2026. Each grant is rounded to the nearest pound once its share is worked "
                       "out. Any part of a parish's 2026 Flood Ready award still unpaid at 31 October 2026 is paid with "
                       "the 2027 grant.", body),
             Paragraph("4. Property flood resilience survey vouchers", h),
             Paragraph("A voucher is offered to every dwelling at ground floor that the design flood would reach. A "
                       "dwelling is a self-contained home: an address register record in a residential class (codes "
                       "beginning RD or RH); a parent record for a building of flats is not a dwelling, and a flat "
                       "above the ground floor of its building is not offered a voucher. The design flood reaches a "
                       "dwelling when the peak stage of the model storage area it stands in is above the dwelling's "
                       "threshold level, both in metres above Ordnance Datum Newlyn. The threshold level is the level "
                       "the 2022 property survey recorded for the dwelling or for "
                       "the building it is in, or its ground level plus 0.15 m where the survey recorded neither.", body),
             Paragraph("5. Timetable", h),
             Paragraph("Lists to the trustees by 18 November 2026; offers sent by 4 December 2026; kits delivered "
                       "before 31 March 2027.", body),
             Paragraph("Annex A. Parishes and main villages", h)]
        data = [["Parish", "Parish code", "Main village access point"]]
        for code, name, node, dw in W.PARISHES:
            data.append([name, code, NODE_ID[node]])
        tb = Table(data, colWidths=[62 * 2.83, 40 * 2.83, 60 * 2.83])
        tb.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", 8.5), ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8.5),
                                ("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.black), ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]))
        s.append(tb)
        s.append(Spacer(1, 6))
        s.append(Paragraph("Hawkesbridge West parish was merged into Hawkesbridge North on 1 April 2025.", small))
        return s

    _pdf(os.path.join(TARGET, "flood_ready_fund_guidance_2027.pdf"), "Flood Ready Fund 2027 guidance",
         "Quarnell Valley Community Foundation", story, "20260924111500")


def write_model_report():
    from reportlab.platypus import Paragraph, Spacer, Table, TableStyle
    from reportlab.lib import colors
    body, h, t, small = styles()

    def story():
        s = [Paragraph("Hawkesbridge Council and the Quarnell Catchment Partnership", small),
             Paragraph("River Quarnell flood model 2025 (QRN25): summary report", t),
             Paragraph("Report QCP-FM-25-04, issue 2, February 2026. Prepared by Eleanor Rose, hydraulic modeller, "
                       "for the Quarnell Catchment Partnership; checked by Abdul Ahmed. Issue 1 (November 2025) was "
                       "issued for consultation.", small), Spacer(1, 6),
             Paragraph("1. Scope", h),
             Paragraph("QRN25 replaces the 2023 model (QRN23). It represents the River Quarnell from Quarnell Head to "
                       "the Hawkesbridge weir and the lower reaches of Hollin Beck, Ravelsby Brook and Lunnerby Beck. The "
                       "channels are a one-dimensional model; the floodplain is represented as fourteen storage areas "
                       "linked to the channels and to each other by spill units over banks, walls and road embankments. "
                       "Storage area boundaries are supplied as polygons (storage_areas_QRN25.geojson).", body),
             Paragraph("2. Hydrology and design events", h),
             Paragraph("Design inflows use the revitalised rainfall-runoff method with a 2025 review of the Hollin "
                       "Beck and Ravelsby Brook gauges. Run D100CC is the 1 in 100 annual chance event with the 2080s "
                       "central climate change allowance applied to peak rainfall intensity, the storm starting at hour "
                       "0 and the run lasting 120 hours. Run D100CC is the planning event used by the council and its "
                       "partners.", body),
             Paragraph("3. Outputs", h),
             Paragraph("For each run the model reports the stage in every storage area at hourly intervals from the "
                       "start of the storm. Stages are in metres above Ordnance Datum Newlyn. Survey levels used to "
                       "build the model that had been taken to the Quarnell Navigation Datum, which lies 0.42 m below "
                       "Ordnance Datum Newlyn, were converted before use.", body),
             Paragraph("4. Calibration", h),
             Paragraph("The model was calibrated to the July 2021 and February 2020 events. Peak levels at the four "
                       "gauges are reproduced within 0.12 m.", body)]
        data = [["Gauge", "Event", "Recorded peak (mAOD)", "Modelled peak (mAOD)"],
                ["Hollin Beck at Hollinside", "July 2021", "43.07", "43.15"],
                ["Ravelsby Brook at Ravelsby Bridge", "July 2021", "38.92", "38.86"],
                ["Quarnell at Yarrowcote", "February 2020", "29.94", "30.03"],
                ["Quarnell at Hawkesbridge weir", "February 2020", "23.61", "23.49"]]
        tb = Table(data, colWidths=[64 * 2.83, 30 * 2.83, 36 * 2.83, 36 * 2.83])
        tb.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", 8.5), ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8.5),
                                ("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.black)]))
        s.append(tb)
        s.append(Spacer(1, 8))
        s.append(Paragraph("5. Peak stages, run D100CC", h))
        data = [["Storage area", "Name", "Peak stage (mAOD)"]]
        for sa in W.SA:
            data.append([sa, W.SA[sa][0], "%.2f" % W.peak_stage(sa)])
        tb = Table(data, colWidths=[30 * 2.83, 70 * 2.83, 36 * 2.83])
        tb.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", 8.5), ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8.5),
                                ("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.black)]))
        s.append(tb)
        s.append(Spacer(1, 8))
        s.append(Paragraph("6. Limitations", h))
        s.append(Paragraph("Storage areas represent water levels, not velocities. Levels inside a storage area are "
                           "taken as level across it. The model does not represent blockage of culverts or bridges.", body))
        return s

    _pdf(os.path.join(TARGET, "quarnell_flood_model_report_2025.pdf"), "QRN25 summary report QCP-FM-25-04",
         "Quarnell Catchment Partnership", story, "20260216093000")


# ---------------------------------------------------------------------------------------------- golden
def closure_windows():
    """first and last model hour any beck dip, and any Quarnell crossing or river road dip, is impassable."""
    out = {}
    for name, sas in (("becks", ("SA-HB1", "SA-SB1", "SA-MW1", "SA-HB2", "SA-SB2")), ("river", None)):
        hrs = [h for l in W.LINKS if l[5] and (l[5] in sas if sas else l[5].startswith("SA-LD"))
               for h in W.HOURS if W.link_impassable(l, h)]
        out[name] = [min(hrs), max(hrs)]
    return out


def golden_and_figures(reg, sv):
    gold = W.golden_set()
    env = W.envelope_set()
    env0 = W.envelope_set(limit=0.0)
    wh = W.worst_hour()
    whset = W.set_at_hour(wh)
    dw = {p[1]: p[3] for p in W.PARISHES}
    a1 = A.ask1_golden(reg, sv)
    a2 = A.ask2_golden()
    a3 = A.ask3_golden()
    hours = W.cut_off_hours()
    figs = {
        "call": {"parishes": gold, "count": len(gold), "households_total": W.dwellings(gold)},
        "households": {n: dw[n] for n in gold},
        "cut_off_hours": {n: [min(hours[n]), max(hours[n])] for n in gold},
        "default_path": {"parishes": env, "count": len(env), "households_total": W.dwellings(env)},
        "rungs": {"R0_any_water": env0, "R1_envelope": env, "R2_worst_hour": [wh, whset], "R3_every_hour": gold},
        "grant_amounts": W.grants(gold)[0],
        "grant_per_household": round(W.grants(gold)[1], 2),
        "budget": W.BUDGET,
        "base_grant": W.BASE_GRANT,
        "grant_rest": W.BUDGET - W.BASE_GRANT * len(gold),
        "default_path_grants": W.grants(env)[0],
        "ask1_dwellings_reached": {p[1]: a1.get(p[1], 0) for p in W.PARISHES},
        "ask2_closure_hours": {s[0]: int(round(a2[s[0]])) for s in A.SECTIONS},
        "ask2_closure_hours_exact": {s[0]: round(a2[s[0]], 3) for s in A.SECTIONS},
        "ask1_total": sum(a1.get(p[1], 0) for p in W.PARISHES),
        "ask3_unpaid": a3,
        "closure_windows": closure_windows(),
        "constants": {"depth_limit_m": W.DEPTH_LIMIT, "default_threshold_m": W.DEFAULT_THRESHOLD,
                      "datum_shift_m": W.DATUM_SHIFT, "hours": [W.HOURS[0], W.HOURS[-1]]},
    }
    with open(os.path.join(HERE, "figures.json"), "w") as f:
        json.dump(figs, f, indent=1, sort_keys=True)
    return figs


def write_golden(figs):
    from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
    os.makedirs(GOLDEN, exist_ok=True)
    wb = wb_new("Lindsey Mistry", "Flood Ready parishes 2027", created=datetime(2026, 11, 3, 14, 20, 0))
    head_fill = PatternFill("solid", fgColor="DCE6F0")
    thin = Side(style="thin", color="9AA5B1")
    gold = figs["call"]["parishes"]

    def header(ws, cols, widths):
        ws.append(cols)
        for c in ws[ws.max_row]:
            c.font = Font(bold=True)
            c.fill = head_fill
            c.alignment = Alignment(wrap_text=True, vertical="top")
            c.border = Border(bottom=thin)
        for col, wdt in zip("ABCDEFG", widths):
            ws.column_dimensions[col].width = wdt
        ws.freeze_panes = "A%d" % (ws.max_row + 1)

    def total(ws, cells):
        ws.append(cells)
        for c in ws[ws.max_row]:
            c.font = Font(bold=True)
            c.border = Border(top=thin)

    ws = wb.active
    ws.title = "Parishes"
    header(ws, ["Parish", "Parish code", "Cut off by the design flood", "Households (council tax list, 1 Oct 2026)",
                "2027 grant (GBP)"], [22, 13, 14, 20, 14])
    for code, name, node, dw in W.PARISHES:
        cut = name in gold
        ws.append([name, code, "Yes" if cut else "No", dw if cut else None, figs["grant_amounts"][name] if cut else None])
        ws.cell(ws.max_row, 4).number_format = "#,##0"
        ws.cell(ws.max_row, 5).number_format = "#,##0"
        ws.cell(ws.max_row, 3).alignment = Alignment(horizontal="center")
    total(ws, ["Parishes cut off", None, figs["call"]["count"], figs["call"]["households_total"],
               sum(figs["grant_amounts"].values())])
    ws.cell(ws.max_row, 4).number_format = "#,##0"
    ws.cell(ws.max_row, 5).number_format = "#,##0"
    ws.cell(ws.max_row, 3).alignment = Alignment(horizontal="center")

    ws2 = wb.create_sheet("PFR vouchers")
    header(ws2, ["Parish", "Dwellings the design flood reaches at ground floor"], [22, 20])
    for code, name, node, dw in W.PARISHES:
        ws2.append([name, figs["ask1_dwellings_reached"][name]])
        ws2.cell(ws2.max_row, 2).number_format = "#,##0"
    total(ws2, ["All parishes", figs["ask1_total"]])
    ws2.cell(ws2.max_row, 2).number_format = "#,##0"

    ws3 = wb.create_sheet("July 2021 closures")
    header(ws3, ["Closure ref", "Road", "Location", "Hours closed"], [13, 8, 30, 10])
    for sid, road, loc, bars, p in A.SECTIONS:
        ws3.append([sid, road, loc, figs["ask2_closure_hours"][sid]])

    ws4 = wb.create_sheet("2026 awards unpaid")
    header(ws4, ["Parish", "2026 award ref", "Unpaid at 31 Oct 2026 (GBP)"], [22, 14, 16])
    for parish, ref, amt, var, pays in A.AWARDS_2026:
        ws4.append([parish, ref, figs["ask3_unpaid"][parish]])
        ws4.cell(ws4.max_row, 3).number_format = "#,##0"

    ws5 = wb.create_sheet("Notes")
    ws5.column_dimensions["A"].width = 110
    notes = [
        "Flood Ready parishes 2027: list for the trustees",
        "Prepared by Lindsey Mistry, Research and Evaluation, Quarnell Valley Community Foundation, November 2026.",
        "",
        "Parishes. Cut off as the 2027 guidance (section 2) defines it: at some hour of the design flood (QRN25, run "
        "D100CC) the main village's access point has no route on the 2025 public highway network to the emergency "
        "department node HBN-%s, a link being closed where any 2019 surveyed carriageway level lies more than 0.25 m "
        "below its storage area's stage. The network was searched at every model hour." % NODE_ID["H"][4:],
        "Households are the council tax valuation list's dwellings for the parish at 1 October 2026. Grants share the "
        "GBP 30,000 budget as section 3 sets out: GBP 3,000 to each parish cut off and the rest in proportion to "
        "households, rounded to the nearest pound.",
        "PFR vouchers. Section 4 of the guidance. Register levels from source SURV08 are on the Quarnell Navigation "
        "Datum and were raised 0.42 m to Ordnance Datum Newlyn before comparison.",
        "July 2021 closures. Highways duty log and police control room log (UTC, shown here in BST). A section's hours "
        "are the time any closure was in force on it; the B5131 route closure (Hollinside to Lunnerby) is counted on "
        "each of its three sections.",
        "2026 awards. Award and variations less payments posted to 31 October 2026; cheques the bank cancelled are "
        "treated as unpaid.",
    ]
    for line in notes:
        ws5.append([line])
        ws5.cell(ws5.max_row, 1).alignment = Alignment(wrap_text=True, vertical="top")
    ws5.cell(1, 1).font = Font(bold=True, size=12)
    wb_save(wb, os.path.join(GOLDEN, "flood_ready_parishes_2027.xlsx"), modified="2026-11-04T10:47:00Z",
            member_time=(2026, 11, 4, 10, 47, 0))
    # chart
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Patch
    plt.rcParams["font.family"] = "DejaVu Sans"
    surface, ink, ink2, grid = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"
    base_c, share_c = "#2a78d6", "#eb6834"
    gr = figs["grant_amounts"]
    names = sorted(gold, key=lambda n: -gr[n])
    ys = list(range(len(names)))[::-1]
    fig, ax = plt.subplots(figsize=(7.4, 4.3), dpi=120)
    fig.patch.set_facecolor(surface)
    ax.set_facecolor(surface)
    ax.barh(ys, [W.BASE_GRANT] * len(names), height=0.58, color=base_c, edgecolor=surface, linewidth=2)
    ax.barh(ys, [gr[n] - W.BASE_GRANT for n in names], left=[W.BASE_GRANT] * len(names), height=0.58, color=share_c,
            edgecolor=surface, linewidth=2)
    for yv, n in zip(ys, names):
        ax.text(gr[n] + 80, yv, "GBP {:,}  ({:,} households)".format(gr[n], figs["households"][n]), va="center",
                fontsize=8.5, color=ink)
    ax.set_yticks(ys)
    ax.set_yticklabels(names, fontsize=9.5, color=ink)
    ax.set_xlim(0, max(gr.values()) * 1.42)
    ax.set_xlabel("2027 grant (GBP)", fontsize=9, color=ink2)
    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, p: "{:,.0f}".format(v)))
    ax.tick_params(axis="x", colors=ink2, labelsize=8.5)
    ax.tick_params(axis="y", length=0)
    ax.xaxis.grid(True, color=grid, linewidth=0.8)
    ax.set_axisbelow(True)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(grid)
    ax.legend(handles=[Patch(color=base_c, label="Base grant, GBP {:,}".format(W.BASE_GRANT)),
                       Patch(color=share_c, label="Share of the rest by households")],
              loc="upper left", bbox_to_anchor=(0.0, -0.17), ncol=2, fontsize=8, frameon=False, labelcolor=ink2)
    fig.text(0.02, 0.955, "The GBP {:,} budget across the six parishes the flood cuts off".format(
        sum(gr.values())), ha="left", va="top", fontsize=11, color=ink, fontweight="bold")
    fig.text(0.02, 0.895, "Cut off from Hawkesbridge General at some hour of the 1 in 100 design flood (QRN25 run D100CC)",
             ha="left", va="top", fontsize=9, color=ink2)
    fig.text(0.02, 0.012, "Households: council tax valuation list, 1 October 2026. Grants: Flood Ready Fund guidance 2027, "
             "section 3.", fontsize=7, color=ink2)
    fig.tight_layout(rect=(0, 0.08, 1, 0.86))
    fig.savefig(os.path.join(GOLDEN, "flood_ready_parishes_2027.png"), facecolor=surface,
                metadata={"Software": None})
    plt.close(fig)


def write_metadata():
    files = {
        "storage_area_stages_QRN25_D100CC.csv": "QRN25 model output, run D100CC, hourly storage-area stages",
        "storage_area_stages_QRN23_D100CC.csv": "QRN23 model output (superseded March 2026), run D100CC",
        "storage_area_stages_QRN25_JUL21_hindcast.csv": "QRN25 hindcast of the July 2021 event",
        "storage_areas_QRN25.geojson": "QRN25 storage area polygons",
        "highways_network_2025.geojson": "council highways network, 2025 asset upload",
        "highways_levels_survey_2019.csv": "highways authority carriageway levels survey, 2019",
        "link_reference_crosswalk_2019_2025.csv": "highways asset upload crosswalk, 2019 references to 2025 links",
        "council_tax_dwellings_by_parish_oct2026.csv": "council tax valuation list dwellings by parish, 1 October 2026",
        "flood_ready_fund_guidance_2027.pdf": "the Foundation's 2027 grant guidance",
        "quarnell_flood_model_report_2025.pdf": "QRN25 summary report",
        "address_register_extract_oct2026.csv": "council address register extract, October 2026",
        "pfr_property_survey_2022.xlsx": "2022 property flood resilience survey",
        "highways_road_closures_jul2021.csv": "highways duty officers' log of roads shut in July 2021",
        "police_road_closures_jul2021.csv": "police control room log of roads shut in July 2021",
        "flood_ready_ledger_2026.xlsx": "Foundation finance system, Flood Ready 2026 transactions",
        "bank_cancelled_cheques_2026.csv": "bank's cancelled cheque advice, 2026",
        "rest_centres_2026.xlsx": "council emergency planning rest centre list",
        "flood_warning_areas_2025.geojson": "flood warning areas in the valley",
    }
    meta = {"task": "task285", "decision": "which parishes receive the 2027 Flood Ready grants, and the households in each",
            "deliverables": ["flood_ready_parishes_2027.xlsx", "flood_ready_parishes_2027.png"],
            "distractor_files": ["target/rest_centres_2026.xlsx", "target/flood_warning_areas_2025.geojson",
                                 "target/storage_area_stages_QRN25_JUL21_hindcast.csv"],
            "files": {k: {"source": "constructed operating record (synthetic, task285 generator)", "date": "2026-11-02",
                          "licence": "CC BY 4.0 (constructed for this task)", "covers": v}
                      for k, v in sorted(files.items())}}
    with open(os.path.join(TASK, "metadata.json"), "w") as f:
        json.dump(meta, f, indent=1, sort_keys=True)
    return list(files)


def main():
    if os.path.isdir(TARGET):
        shutil.rmtree(TARGET)
    os.makedirs(TARGET)
    write_stages()
    write_sa_geojson()
    write_network()
    write_survey_and_crosswalk()
    write_council_tax()
    reg = A.build_register()
    sv = A.build_survey(reg)
    write_register(reg)
    write_pfr_survey(sv)
    write_closures()
    write_ledger()
    write_distractors()
    write_guidance()
    write_model_report()
    figs = golden_and_figures(reg, sv)
    write_golden(figs)
    names = write_metadata()
    for folder in (TARGET, GOLDEN):
        for fn in os.listdir(folder):
            os.utime(os.path.join(folder, fn), (EXPORT_TS, EXPORT_TS))
    assert sorted(os.listdir(TARGET)) == sorted(names), (sorted(os.listdir(TARGET)), sorted(names))
    cut_zip()
    print("built", len(os.listdir(TARGET)), "files; call", figs["call"])


def cut_zip():
    """target.zip cut last from target/, members in name order with the export time, so it is byte-identical on
    every rebuild and agrees with the tree it was cut from."""
    path = os.path.join(TASK, "target.zip")
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for fn in sorted(os.listdir(TARGET)):
            zi = zipfile.ZipInfo("target/" + fn, date_time=EXPORT_TIME)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(TARGET, fn), "rb").read())
    os.utime(path, (EXPORT_TS, EXPORT_TS))


if __name__ == "__main__":
    main()
