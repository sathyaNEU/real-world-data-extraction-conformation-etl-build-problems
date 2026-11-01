"""Write the evidence pack (target/) from the clean truth in world.py. Each file is written the way its source system
writes it; nothing here describes the data."""
import csv
import datetime as dt
import io
import json
import os
import zipfile

import numpy as np

import params as P
import world as W

D = dt.date
FIXED_ZIP_TIME = (2026, 11, 16, 16, 40, 0)


# ---------------------------------------------------------------------------------------------------------------
# helpers
def pacific_offset(d):
    """Hours behind UTC on a calendar date in Oregon (PDT from the second Sunday of March to the first Sunday of
    November)."""
    y = d.year
    mar = D(y, 3, 8)
    while mar.weekday() != 6:
        mar += dt.timedelta(days=1)
    nov = D(y, 11, 1)
    while nov.weekday() != 6:
        nov += dt.timedelta(days=1)
    return 7 if mar <= d < nov else 8


def utc_stamp(d, minute, extra_sec=0):
    local = dt.datetime(d.year, d.month, d.day) + dt.timedelta(minutes=minute, seconds=extra_sec)
    u = local + dt.timedelta(hours=pacific_offset(d))
    return u.strftime("%Y-%m-%dT%H:%M:%SZ")


def write_csv(path, header, rows, quoting=csv.QUOTE_MINIMAL):
    with open(path, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f, quoting=quoting, lineterminator="\n")
        wr.writerow(header)
        for r in rows:
            wr.writerow(r)


def normalise_zip(path, when="2026-10-01T09:12:00Z", app="Microsoft Excel"):
    """Rewrite an OOXML container with fixed member times and order, and the document dates the writer stamps at
    save time set to the export's own date, so two builds are byte-identical."""
    import re
    with zipfile.ZipFile(path) as z:
        items = [(i.filename, z.read(i.filename)) for i in z.infolist()]
    fixed = []
    for name, data in items:
        if name == "docProps/app.xml":
            data = re.sub(rb"<Application>[^<]*</Application>", b"<Application>" + app.encode() + b"</Application>", data)
            data = re.sub(rb"<AppVersion>[^<]*</AppVersion>", b"<AppVersion>16.0300</AppVersion>", data)
        if name == "docProps/core.xml":
            data = re.sub(rb"(<dcterms:created[^>]*>)[^<]*(</dcterms:created>)", rb"\g<1>" + when.encode() + rb"\g<2>",
                          data)
            data = re.sub(rb"(<dcterms:modified[^>]*>)[^<]*(</dcterms:modified>)", rb"\g<1>" + when.encode() +
                          rb"\g<2>", data)
        fixed.append((name, data))
    items = fixed
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in items:
            zi = zipfile.ZipInfo(name, date_time=FIXED_ZIP_TIME)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o600 << 16
            z.writestr(zi, data)


def xlsx_props(wb, creator, title):
    when = dt.datetime(2026, 10, 1, 9, 12, 0)
    wb.properties.creator = creator
    wb.properties.lastModifiedBy = creator
    wb.properties.created = when
    wb.properties.modified = when
    wb.properties.title = title


# ---------------------------------------------------------------------------------------------------------------
# PDF documents (reportlab, invariant, producer set to the issuing body)
def write_pdf(path, title, issuer, blocks, stamp_date="D:20261014093000+00'00'"):
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib import colors
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
            story.append(Paragraph(val, body))
            story.append(Spacer(1, 3))
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
    # the writer's banner and its fixed clock: equal-length substitutions inside comment and date values
    import re
    data = open(path, "rb").read()
    for sig in (b"ReportLab Generated PDF document (opensource)", b"ReportLab generated PDF document -- digest (opensource)",
                b"ReportLab Generated PDF document http://www.reportlab.com"):
        data = data.replace(sig, b" " * len(sig))
    for key in (b"/CreationDate", b"/ModDate"):
        def sub(m):
            old = m.group(1)
            new = stamp_date.encode()
            assert len(new) == len(old), (old, new)
            return key + b" (" + new + b")"
        data = re.sub(re.escape(key) + rb" \(([^)]*)\)", sub, data)
    assert b"ReportLab" not in data and b"reportlab" not in data
    open(path, "wb").write(data)


# ---------------------------------------------------------------------------------------------------------------
def build_pack(w, out):
    rng = np.random.default_rng(P.SEED + 17)
    fp = lambda k: os.path.join(out, P.FILES[k])
    clinic = {c[0]: c for c in P.CLINICS}
    counts = {}

    # identities the systems share
    pref = {}
    for p in w.patients:
        while True:
            ref = "K%07X" % int(rng.integers(0x1000000, 0xFFFFFFF))
            if ref not in pref.values():
                break
        pref[p["mrn"]] = ref
    # every retinal imaging study (AI screening, teleretinal photographs, re-photographs) takes the next accession
    # from one imaging sequence, in capture order
    studies = [(s["date"], s["minute"], 0, i) for i, s in enumerate(w.screens)]
    studies += [(c["opened"], c["minute"], 1, i) for i, c in enumerate(w.cases) if c["kind"] != "ai"]
    studies.sort()
    acc_seq = 26_004_118
    for d, mnt, kind, i in studies:
        acc_seq += int(rng.integers(1, 4))
        if kind == 0:
            w.screens[i]["acc"] = "RC%d" % acc_seq
        else:
            w.cases[i]["acc"] = "RC%d" % acc_seq
    order_seq = 81_340_000
    for s in w.screens:
        order_seq += int(rng.integers(1, 6))
        s["order"] = order_seq
        s["sec"] = int(rng.integers(0, 60))
        s["release_sec"] = int(rng.integers(95, 380))
        # image quality the AI reports: ungradable images under 35, gradable 41 to 99, the same on both models
        if s["ungradable"]:
            s["quality"] = int(rng.integers(8, 35))
        else:
            s["quality"] = int(min(99, max(41, round(rng.normal(81, 9)))))
    for c in w.cases:
        if c["kind"] != "ai":
            order_seq += int(rng.integers(1, 6))
            c["photo_order"] = order_seq
        if c["kind"] == "manual":
            c["order"] = c["photo_order"]
    w.make_ask_records_done = True

    # 1. the vendor portal's result export (the year's screenings, results at the Standard point the sites ran)
    cut = dict(P.OPS)["Standard"]
    rows = []
    for s in w.screens:
        res = "Ungradable" if s["ungradable"] else ("Referable" if s["score"] >= cut else "Not referable")
        sv = "4.2.1" if s["date"] < D(2026, 4, 14) else "4.3.0"
        rows.append([s["acc"], clinic[s["clinic"]][2], pref[s["patient"]["mrn"]],
                     utc_stamp(s["date"], s["minute"], s["sec"]),
                     utc_stamp(s["date"], s["minute"], s["sec"] + s["release_sec"]),
                     res, "" if s["score"] is None else s["score"], s["quality"], "Standard", sv])
    write_csv(fp("results"), ["Accession", "Site", "Patient Ref", "Captured (UTC)", "Result Released (UTC)",
                              "Result", "DR Score", "Image Quality", "Operating Point", "Software Version"], rows)
    counts["results"] = len(rows)

    # 2. the local validation study's data export
    vrows = []
    for v in w.validation:
        v["quality"] = int(rng.integers(8, 35)) if v["ungradable"] else int(min(99, max(41, round(rng.normal(81, 9)))))
        p = v["patient"]
        res = "Ungradable" if v["ungradable"] else ("Referable" if v["score"] >= cut else "Not referable")
        dme = "Y" if v["dme"] else "N"
        vrows.append(["CVR-%04d" % v["sid"], v["site"], "%d/%d/%d" % (v["date"].month, v["date"].day, v["date"].year),
                      p["age"], p["sex"], p["dtype"], p["a1c"], p["eth"], res,
                      "" if v["score"] is None else v["score"], v.get("quality", ""),
                      v["g1"], dme, v["g2"], dme, "Y" if v["adjudicated_flag"] else "N",
                      v["final"], dme])
    write_csv(fp("validation"), ["study_id", "site", "capture_date", "age_group", "sex", "diabetes_type",
                                 "hba1c_group", "ethnicity", "ai_result", "dr_score", "image_quality",
                                 "grader1_level", "grader1_dme", "grader2_level", "grader2_dme", "adjudicated",
                                 "final_level", "final_dme"], vrows)
    counts["validation"] = len(vrows)

    # 3. clinic directory
    addr = {"OF": ("1880 Mill Race Rd", "Orrin Falls", "97341"), "TB": ("44 Thistlebrook Way", "Corrowan", "97338"),
            "WM": ("903 Wendmere Ave", "Wendmere", "97352"), "PB": ("2216 Pellsbury Rd", "Pellsbury", "97326"),
            "QH": ("515 Quarry Hill Dr", "Corrowan", "97338"), "RW": ("77 Rookwood Ln", "Rookwood", "97370"),
            "SC": ("1402 Sallow Creek Pkwy", "Dunmore", "97347"), "VD": ("360 Veldane St", "Veldane", "97361"),
            "BF": ("2930 Brackenfield Rd", "Brackenfield", "97377"), "YB": ("118 Yarrowby Ct", "Yarrowby", "97335"),
            "KN": ("6021 Kestle Rd", "Dunmore", "97347"), "HM": ("49 Hollinmoor Sq", "Hollinmoor", "97389")}
    drows = []
    for code, ehr, portal, loc, _, _ in P.CLINICS:
        drows.append([code, ehr, portal, loc] + list(addr[code]))
    drows.sort(key=lambda r: r[3])
    write_csv(fp("directory"), ["clinic_code", "ehr_department", "portal_site", "biomed_location", "street", "city",
                                "zip"], drows)

    write_assets(w, fp("assets"), rng)
    write_tickets(w, fp("tickets"), rng)
    counts["orders"] = write_orders(w, fp("orders"), rng)
    counts["registry"] = write_registry(w, fp("registry"), rng)
    counts["outside"] = write_outside(w, fp("outside"), rng)
    counts["reads"] = write_reads(w, fp("reads"), rng)
    write_siteconfig(fp("siteconfig"))
    write_dashboard(w, fp("dashboard"), rng)
    counts["survey"] = write_survey(w, fp("survey"), rng)
    import docs
    docs.write_all(out)
    return pref, counts


# ---------------------------------------------------------------------------------------------------------------
LOCS = {c[0]: c[3] for c in P.CLINICS}
HIM_PULL = D(2026, 11, 13)
DEPOT = "LOC-100 Biomed Depot"
OTHER_CLASSES = [
    ("Automated BP monitor", "Welmore", "VS-300", 6), ("Vaccine refrigerator", "Thermatrue", "VR-14", 3),
    ("Spirometer", "Aerolex", "SP-2", 1), ("ECG", "Cardiax", "C12", 1), ("Exam table, powered", "Ridgeway", "PT-5", 4),
    ("Pulse oximeter", "Welmore", "OX-8", 5), ("Otoscope set", "Hallam", "DX-3", 6), ("Scale, digital", "Brenton", "M-200", 3),
    ("Point-of-care A1c analyzer", "Glycon", "A1-Plus", 1), ("Autoclave", "Steriva", "S-22", 1),
]


def write_assets(w, path, rng):
    from openpyxl import Workbook
    from openpyxl.styles import Font
    wb = Workbook()
    ws = wb.active
    ws.title = "Assets"
    head = ["Asset Tag", "Serial Number", "Equipment Class", "Manufacturer", "Model", "Acquired", "Location", "Status"]
    ws.append(head)
    tag = 30_412
    tags = {}
    rows = []
    # where each camera stands at 30 September 2026
    last_loc = {}
    for s, c, a, b, r in W.PLACEMENTS:
        if b is None:
            last_loc[s] = LOCS[c]
    for serial, model, bought in W.CAMERAS:
        tag += int(rng.integers(3, 29))
        tags[serial] = "CV%06d" % tag
        loc = last_loc.get(serial, DEPOT)
        status = "In service" if serial in last_loc else ("Out for repair" if serial in
                 {"HO-NR70-250694", "HO-NR70-250931"} else "Spare")
        rows.append([tags[serial], serial, "Retinal camera, non-mydriatic", P.CAMERA_MAKER, model,
                     bought, loc, status])
    for code in LOCS:
        for cls, mk, model, n in OTHER_CLASSES:
            for i in range(n):
                tag += int(rng.integers(3, 29))
                bought = D(2015, 1, 1) + dt.timedelta(days=int(rng.integers(0, 3800)))
                ser = "%s%05d" % (mk[:2].upper(), int(rng.integers(10000, 99999)))
                rows.append(["CV%06d" % tag, ser, cls, mk, model, bought, LOCS[code],
                             "In service" if rng.random() > 0.04 else "Spare"])
    order = rng.permutation(len(rows))
    for i in order:
        ws.append(rows[i])
    for (cell,) in ws.iter_rows(min_row=2, min_col=6, max_col=6):
        cell.number_format = "yyyy-mm-dd"
    for c in ws[1]:
        c.font = Font(bold=True)
    hs = wb.create_sheet("Location History")
    hs.append(["Asset Tag", "Serial Number", "Moved On", "From", "To", "Reason", "Entered By"])
    moves = []
    # each placement opens with a move into the clinic; a camera leaving for the depot the same day moves out first
    repair_out = {(f[0], f[3]) for f in W.FAULTS} | {("HO-NR70-241188", D(2025, 4, 12)), ("HO-NR70-250251", D(2025, 6, 7))}
    seen_serial = set()
    prev_loc = {}
    for s_, c, a_, b_, r in sorted(W.PLACEMENTS, key=lambda t: (t[2], t[1])):
        frm = prev_loc.get(s_, DEPOT)
        if r == "Loaner":
            why = "Loaner"
        elif r == "Returned from repair":
            why = "Returned from repair"
        elif s_ not in seen_serial:
            why = "New installation"
        else:
            why = "Transfer"
        seen_serial.add(s_)
        moves.append((a_, s_, frm, LOCS[c], why))
        prev_loc[s_] = LOCS[c]
        if b_ is not None:
            nxt = [t for t in W.PLACEMENTS if t[0] == s_ and t[2] == b_]
            if not nxt:
                if (s_, b_) in repair_out:
                    out_why = "Sent for repair"
                elif r == "Loaner":
                    out_why = "Loaner returned"
                else:
                    out_why = "Replaced"
                moves.append((b_, s_, LOCS[c], DEPOT, out_why))
                prev_loc[s_] = DEPOT
    # moves of other equipment between clinics (routine)
    others = [r for r in rows if not r[2].startswith("Retinal")]
    for i in range(140):
        r = others[int(rng.integers(0, len(others)))]
        d = D(2024, 1, 6) + dt.timedelta(days=int(rng.integers(0, 990)))
        moves.append((d, r[1], r[6], DEPOT if rng.random() < 0.5 else r[6], "Preventive maintenance"))
    moves.sort(key=lambda m: (m[0], m[1]))
    who = ["N. Odonnell", "J. Ferrar", "biomed-svc", "T. Ruel"]
    for d, s, frm, to, rsn in moves:
        t = tags.get(s, "")
        if not t:
            for r in rows:
                if r[1] == s:
                    t = r[0]
                    break
        sv = s
        if s.startswith("HO-") and rng.random() < 0.3:
            sv = s[3:]                       # hand-typed without the maker's prefix
        hs.append([t, sv, d, frm, to, rsn, who[int(rng.integers(0, len(who)))]])
    for (cell,) in hs.iter_rows(min_row=2, min_col=3, max_col=3):
        cell.number_format = "m/d/yyyy"
    for c in hs[1]:
        c.font = Font(bold=True)
    xlsx_props(wb, "CVCH Biomedical Engineering", "Biomedical asset register")
    wb.save(path)
    normalise_zip(path, when="2026-09-30T22:47:00Z")
    w.asset_tags = tags
    w.asset_rows = [r for r in rows if not r[2].startswith("Retinal") and r[6] in LOCS.values()]


def write_tickets(w, path, rng):
    rows = []
    tno = 51_870
    for t in w.tickets:
        rows.append(t)
    # routine tickets on other equipment across the network
    others = w.asset_rows
    code_of_loc = {v: k for k, v in LOCS.items()}
    for i in range(470):
        d = D(2025, 10, 1) + dt.timedelta(days=int(rng.integers(0, 365)))
        a = others[int(rng.integers(0, len(others)))]
        cls = a[2]
        dur = int(rng.integers(0, 21))
        rows.append({"ticket": None, "serial": a[1], "loc": code_of_loc[a[6]], "opened": d,
                     "closed": d + dt.timedelta(days=dur), "class": cls,
                     "note": ["Calibration due", "Battery replacement", "Display fault", "Annual PM",
                              "Cuff leak", "Door seal", "Error code on startup"][int(rng.integers(0, 7))]})
    rows.sort(key=lambda r: (r["opened"], r["loc"]))
    out = []
    for r in rows:
        tno += int(rng.integers(1, 6))
        st = "Closed" if r["closed"] is not None else "Open - awaiting part"
        out.append(["BT-%d" % tno, r["serial"], r["class"], LOCS[r["loc"]],
                    r["opened"].strftime("%m/%d/%Y"), "" if r["closed"] is None else r["closed"].strftime("%m/%d/%Y"),
                    r["note"], st])
    write_csv(path, ["Ticket", "Serial", "Equipment Class", "Location", "Opened", "Closed", "Problem", "Status"], out)


def write_orders(w, path, rng):
    """EHR orders: one completed AI screening order per screening (with the imaging accession), the cancelled
    screening orders, the retinal photography orders (teleretinal reads and re-photographs) and the referral orders
    to the reading center for every referred screening."""
    clinic = {c[0]: c for c in P.CLINICS}
    rows = []
    for s in w.screens:
        rows.append([s["order"], s["patient"]["mrn"], clinic[s["clinic"]][1], s["date"].strftime("%m/%d/%Y"),
                     "IMG92229", "RETINAL IMAGING AUTONOMOUS AI", "Completed", "", s["acc"]])
    oseq = 81_100_000
    for s in w.cancelled:
        oseq += int(rng.integers(1, 9))
        rows.append([oseq, s["patient"]["mrn"], clinic[s["clinic"]][1], s["date"].strftime("%m/%d/%Y"),
                     "IMG92229", "RETINAL IMAGING AUTONOMOUS AI", "Cancelled", "Equipment unavailable", ""])
    # routine cancellations and no-shows across the year
    days = [d for d in W.daterange(P.REF_START, P.REF_END) if d.weekday() < 5 and d not in W.HOLIDAYS]
    pool = w.patients
    for i in range(1850):
        p = pool[int(rng.integers(0, len(pool)))]
        d = days[int(rng.integers(0, len(days)))]
        oseq += int(rng.integers(1, 9))
        reason = ["Patient did not arrive", "Patient request", "Rescheduled", "Duplicate order"][
            int(rng.choice(4, p=[0.55, 0.2, 0.18, 0.07]))]
        rows.append([oseq, p["mrn"], clinic[p["clinic"]][1], d.strftime("%m/%d/%Y"), "IMG92229",
                     "RETINAL IMAGING AUTONOMOUS AI", "Cancelled", reason, ""])
    # retinal photography: the teleretinal reads and the re-photographs the reading center asked for
    first_of = {c["case"]: c for c in w.cases}
    for c in w.cases:
        if c["kind"] == "ai":
            continue
        if c["kind"] == "manual":
            mrn = c["patient"]["mrn"]
        else:
            mrn = first_of[c["reimage_of"]]["screen"]["patient"]["mrn"]
        rows.append([c["photo_order"], mrn, clinic[c["clinic"]][1], c["opened"].strftime("%m/%d/%Y"),
                     "IMG92250", "RETINAL PHOTOGRAPHY TELERETINAL READ", "Completed", "", c["acc"]])
    # referral orders to the reading center, one per referred screening
    for c in w.cases:
        if c["kind"] == "ai":
            s = c["screen"]
            rows.append([c["order"], s["patient"]["mrn"], clinic[s["clinic"]][1], s["date"].strftime("%m/%d/%Y"),
                         "REF7734", "AMB REFERRAL TO EYE READING CENTER", "Completed", "", s["acc"]])
    for s in w.unread:
        rows.append([s["ref_order"], s["patient"]["mrn"], clinic[s["clinic"]][1], s["date"].strftime("%m/%d/%Y"),
                     "REF7734", "AMB REFERRAL TO EYE READING CENTER", "Cancelled", s["ref_cancel"], s["acc"]])
    rows.sort(key=lambda r: (dt.datetime.strptime(r[3], "%m/%d/%Y"), r[0]))
    write_csv(path, ["ORDER_ID", "MRN", "DEPARTMENT", "ORDER_DATE", "PROC_CODE", "PROC_NAME", "ORDER_STATUS",
                     "CANCEL_REASON", "ACCESSION"], rows)
    return len(rows)


def write_registry(w, path, rng):
    clinic = {c[0]: c for c in P.CLINICS}
    rows = []
    for p in w.patients:
        prior = "" if p["retired_mrn"] is None else str(p["retired_mrn"])
        rows.append([p["mrn"], prior, clinic[p["clinic"]][1], "Active" if p["active"] else "Inactive",
                     p["age"], p["sex"], p["dtype"], p["a1c"], p["eth"]])
    rows.sort(key=lambda r: r[0])
    write_csv(path, ["MRN", "PRIOR_MRN", "HOME_DEPARTMENT", "REGISTRY_STATUS", "AGE_GROUP", "SEX", "DIABETES_TYPE",
                     "LAST_A1C_GROUP", "ETHNICITY"], rows)
    return len(rows)


def write_outside(w, path, rng):
    practices = ["Corrowan Eye Associates", "Dunmore Vision Center", "Valley Optometry Group", "Brightline Eyecare",
                 "Hollinmoor Optical", "Pacific Retina Partners", "Orrin Falls Eye Clinic"]
    rows = []
    did = 9_200_000
    for o in sorted(w.outside, key=lambda x: (x["received"], x["mrn"])):
        if o["received"] > HIM_PULL:
            continue
        did += int(rng.integers(1, 30))
        rows.append(["HIM%d" % did, o["mrn"], "OUTSIDE EYE EXAM REPORT", o["exam"].strftime("%m/%d/%Y"),
                     o["received"].strftime("%m/%d/%Y"), practices[int(rng.integers(0, len(practices)))]])
    write_csv(path, ["DOC_ID", "MRN", "DOC_TYPE", "DOC_DATE", "RECEIVED_DATE", "SOURCE"], rows)
    return len(rows)


def write_reads(w, path, rng):
    """The reading center's case log for the network: one row per case, in case order."""
    rows = []
    for c in w.cases:
        if c["kind"] == "ai":
            s = c["screen"]
            acc, mnt = s["acc"], s["minute"]
        else:
            acc, mnt = c["acc"], c["minute"]
        rec = utc_stamp(c["opened"], mnt + int(rng.integers(4, 40)), int(rng.integers(0, 60)))
        graded = utc_stamp(c["result_date"], int(rng.integers(8 * 60, 20 * 60 + 30)), int(rng.integers(0, 60)))
        rows.append([c["case"], c["order"], acc, P.PELLAM_SITE[c["clinic"]],
                     "%d/%d/%d" % (c["opened"].month, c["opened"].day, c["opened"].year), rec, c["grade"], graded,
                     "PG-%02d" % int(rng.integers(1, 15))])
    rows.sort(key=lambda r: r[0])
    write_csv(path, ["Case No", "Referral Order", "Accession", "Site", "Image Date", "Received (UTC)",
                     "Final Grade", "Graded (UTC)", "Grader"], rows)
    return len(rows)


def write_siteconfig(path):
    sites = []
    for i, (code, ehr, portal, loc, _, _) in enumerate(sorted(P.CLINICS, key=lambda c: c[2])):
        sites.append({"siteId": "cvch-%s" % (portal.lower().replace(" ", "-").replace(".", "")),
                      "displayName": portal, "operatingPoint": "Standard", "operatingPointSince": "2025-10-01",
                      "ungradableHandling": "refer", "softwareVersion": "4.3.0"})
    doc = {"tenant": "corrowan-valley-ch", "exportedAt": "2026-10-01T16:05:44Z", "product": P.PRODUCT,
           "sites": sites}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(doc, f, indent=2)
        f.write("\n")


def write_dashboard(w, path, rng):
    """The vendor's quarterly site dashboard (a distractor: referral and ungradable rates by site and quarter)."""
    from openpyxl import Workbook
    from openpyxl.styles import Font
    clinic = {c[0]: c for c in P.CLINICS}
    wb = Workbook()
    ws = wb.active
    ws.title = "Site summary"
    ws.append(["Site", "Quarter", "Screens", "Referable %", "Ungradable %", "Mean image quality"])
    cut = dict(P.OPS)["Standard"]
    qs = [("2025-Q4", D(2025, 10, 1), D(2025, 12, 31)), ("2026-Q1", D(2026, 1, 1), D(2026, 3, 31)),
          ("2026-Q2", D(2026, 4, 1), D(2026, 6, 30)), ("2026-Q3", D(2026, 7, 1), D(2026, 9, 30))]
    for code in sorted(clinic, key=lambda c: clinic[c][2]):
        for q, a, b in qs:
            ss = [s for s in w.screens if s["clinic"] == code and a <= s["date"] <= b]
            n = len(ss)
            refp = sum(1 for s in ss if not s["ungradable"] and s["score"] >= cut) / n * 100
            ungp = sum(1 for s in ss if s["ungradable"]) / n * 100
            mq = sum(s["quality"] for s in ss) / n
            ws.append([clinic[code][2], q, n, round(refp, 1), round(ungp, 1), round(mq, 1)])
    for c in ws[1]:
        c.font = Font(bold=True)
    xlsx_props(wb, "Kelvory Customer Success", "RetinaCheck site dashboard")
    wb.save(path)
    normalise_zip(path, when="2026-10-01T15:31:00Z")


def write_survey(w, path, rng):
    clinic = {c[0]: c for c in P.CLINICS}
    rows = []
    rid = 300_000
    for code in clinic:
        n = int(rng.integers(140, 260))
        for i in range(n):
            rid += int(rng.integers(1, 4))
            d = D(2026, 1, 5) + dt.timedelta(days=int(rng.integers(0, 260)))
            rows.append([rid, clinic[code][1], d.strftime("%m/%d/%Y"), int(rng.choice([1, 2, 3, 4, 5],
                         p=[0.03, 0.05, 0.14, 0.33, 0.45])), int(rng.choice([1, 2, 3, 4, 5], p=[0.04, 0.07, 0.18, 0.34, 0.37])),
                         "Y" if rng.random() < 0.82 else "N"])
    rows.sort(key=lambda r: r[0])
    write_csv(path, ["RESPONSE_ID", "DEPARTMENT", "VISIT_DATE", "Q1_EASE_OF_SCREENING", "Q2_WAIT_TIME",
                     "Q3_RESULT_EXPLAINED"], rows)
    return len(rows)
