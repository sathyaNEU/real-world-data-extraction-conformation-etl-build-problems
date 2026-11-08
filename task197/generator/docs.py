"""task197 architecture 2: the governing documents, the register, the lookups and the distractors."""
import os, csv, zipfile, shutil, re, datetime as dt
import numpy as np
from reportlab import rl_config
rl_config.invariant = 1          # fixed PDF control dates and ids, so a rebuild is byte-identical
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
import sim
import world

FIXED_PDF_DATE = b"D:20000101000000+00'00'"
THRESHOLD = 1.20


def _styles():
    ss = getSampleStyleSheet()
    ss.add(ParagraphStyle("Body9", parent=ss["BodyText"], fontName="Helvetica", fontSize=9.5, leading=13))
    ss.add(ParagraphStyle("H1x", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=13, spaceAfter=6))
    ss.add(ParagraphStyle("H2x", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=10.5, spaceBefore=9,
                          spaceAfter=3))
    ss.add(ParagraphStyle("Small", parent=ss["BodyText"], fontName="Helvetica", fontSize=7.8, leading=10,
                          textColor=colors.HexColor("#555555")))
    return ss


def pdf(path, title, blocks, author, issued):
    """Write a short operational PDF; its control dates carry the date the document states for itself."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    ss = _styles()
    doc = SimpleDocTemplate(path, pagesize=letter, leftMargin=22 * mm, rightMargin=22 * mm, topMargin=18 * mm,
                            bottomMargin=16 * mm, title=title, author=author, subject="", creator=author,
                            producer=author + " document control")
    flow = []
    for kind, body in blocks:
        if kind == "h1":
            flow.append(Paragraph(body, ss["H1x"]))
        elif kind == "h2":
            flow.append(Paragraph(body, ss["H2x"]))
        elif kind == "p":
            flow.append(Paragraph(body, ss["Body9"]))
            flow.append(Spacer(1, 3))
        elif kind == "small":
            flow.append(Paragraph(body, ss["Small"]))
        elif kind == "gap":
            flow.append(Spacer(1, body))
    doc.build(flow)
    stamp = ("D:%s000000+00'00'" % issued.strftime("%Y%m%d")).encode("ascii")
    assert len(stamp) == len(FIXED_PDF_DATE)
    raw = open(path, "rb").read()
    assert FIXED_PDF_DATE in raw, path
    open(path, "wb").write(raw.replace(FIXED_PDF_DATE, stamp))


WB_DEFAULTS = [rb' state="visible"', rb' visibility="visible"', rb' minimized="0"', rb' showHorizontalScroll="1"',
               rb' showVerticalScroll="1"', rb' showSheetTabs="1"', rb' tabRatio="600"', rb' firstSheet="0"',
               rb' autoFilterDateGrouping="1"', rb'<workbookProtection/>']


def strip_workbook_defaults(data):
    """Excel writes a sheet's state only for a hidden sheet and leaves default view attributes out."""
    for d in WB_DEFAULTS:
        data = data.replace(d, b"")
    return data


def normalise_zip(path, when, owner, application="Microsoft Excel"):
    """Rewrite a zip container with fixed entry timestamps, its owner as author and the office suite's own name."""
    with zipfile.ZipFile(path) as z:
        items = []
        for i in sorted(z.infolist(), key=lambda i: i.filename):
            data = z.read(i.filename)
            if i.filename == "docProps/core.xml":
                stamp = ("%04d-%02d-%02dT%02d:%02d:00Z" % when[:5]).encode()
                data = re.sub(rb"<dcterms:modified([^>]*)>[^<]*</dcterms:modified>",
                              rb"<dcterms:modified\1>" + stamp + rb"</dcterms:modified>", data)
                data = re.sub(rb"<dcterms:created([^>]*)>[^<]*</dcterms:created>",
                              rb"<dcterms:created\1>" + stamp + rb"</dcterms:created>", data)
                data = re.sub(rb"(<dc:creator[^>]*>)[^<]*(</dc:creator>)", rb"\g<1>" + owner.encode() + rb"\g<2>", data)
                if b"lastModifiedBy" in data:
                    data = re.sub(rb"(<cp:lastModifiedBy[^>]*>)[^<]*(</cp:lastModifiedBy>)", rb"\g<1>" + owner.encode() + rb"\g<2>", data)
                else:
                    data = data.replace(b"</cp:coreProperties>", b"<cp:lastModifiedBy>" + owner.encode() + b"</cp:lastModifiedBy></cp:coreProperties>")
            if i.filename == "xl/workbook.xml":
                data = strip_workbook_defaults(data)
            if i.filename == "docProps/app.xml":
                data = (b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
                        b'<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
                        b'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
                        b'<Application>' + application.encode() + b'</Application><DocSecurity>0</DocSecurity>'
                        b'<ScaleCrop>false</ScaleCrop><Company>' + world.NETWORK.encode() + b'</Company>'
                        b'<LinksUpToDate>false</LinksUpToDate><SharedDoc>false</SharedDoc>'
                        b'<HyperlinksChanged>false</HyperlinksChanged><AppVersion>16.0300</AppVersion></Properties>')
            items.append((i.filename, data))
    tmp = path + ".tmp"
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in items:
            zi = zipfile.ZipInfo(name, date_time=when)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o600 << 16
            z.writestr(zi, data)
    shutil.move(tmp, path)


def write_csv(path, header, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)
    return len(rows)


def procedure(path):
    pdf(path, "Child-Resistant Packaging Review: referral procedure CRP-3", [
        ("h1", "%s: Child-Resistant Packaging Review" % world.OFFICE),
        ("small", "Referral procedure CRP-3, issue 4, approved 9 March 2026. Supersedes issue 3 (2025)."),
        ("h2", "1. The review"),
        ("p", "Each year the Office re-examines the packaging of one over-the-counter product and may order a "
              "change to its closure or pack for the following year's sale. The 2027 review takes one product, "
              "chosen from the referrals the Office receives under this procedure."),
        ("h2", "2. Who refers, and what"),
        ("p", "A poison data network whose member poison centers record their exposure calls on a common system "
              "may refer one product from its watched-product list whose packaging changed between "
              "1 January 2024 and 30 September 2025."),
        ("h2", "3. The effect of a packaging change"),
        ("p", "3.1 The effect of a packaging change is the number of accidental exposures of children under six "
              "to the product that the network's member centers recorded in the twelve calendar months after "
              "the month in which the changed pack was first sold at retail, divided by the number the "
              "product's packs would have produced in those months had they kept their previous packaging."),
        ("p", "3.2 An accidental exposure is a case whose reason the member center recorded as unintentional "
              "general, in a patient under six years of age at the time of the call. A case involving more than "
              "one watched product counts once for each of them."),
        ("p", "3.3 A case falls in the calendar month of the date its member center recorded the call. The date "
              "the changed pack was first sold at retail is the date the network's watched-product register "
              "records for the change, and the twelve months begin on the first day of the month after it."),
        ("h2", "4. Which product is referred"),
        ("p", "The network refers the product whose packaging change had the largest effect, provided that "
              "effect is at least %.2f. If no change reaches %.2f, the network makes no referral this year." %
              (THRESHOLD, THRESHOLD)),
        ("h2", "5. Dates"),
        ("p", "Referrals for the 2027 review close on 27 November 2026. The Office acknowledges each referral "
              "within ten working days and publishes the product it takes in January 2027."),
        ("gap", 8),
        ("small", "%s, Review Secretariat. Questions on this procedure to the Review Secretary." % world.OFFICE),
    ], world.OFFICE, world.DOC_DATES["procedure"])


def call_letter(path):
    pdf(path, "Call for referrals: 2027 Child-Resistant Packaging Review", [
        ("h1", "Call for referrals: 2027 Child-Resistant Packaging Review"),
        ("small", "%s, Review Secretariat. 21 September 2026." % world.OFFICE),
        ("p", "To the Director of Toxicovigilance, %s." % world.NETWORK),
        ("p", "The Office invites your network's referral for the 2027 Child-Resistant Packaging Review under "
              "procedure CRP-3 (issue 4). The review takes one product. A referral names the product, "
              "states the effect of its packaging change as section 3 of the procedure defines it, and is "
              "received by the Secretariat no later than 27 November 2026."),
        ("p", "Networks that refer no product this year are asked to say so by the same date."),
        ("gap", 6),
        ("p", "%s<br/>Review Secretary" % world.PEOPLE["secretary"]),
    ], world.OFFICE, world.DOC_DATES["call"])


def register(path, products):
    wb = Workbook()
    ws = wb.active
    ws.title = "Watched products"
    head = ["Product code", "Product", "Manufacturer", "Active ingredient", "Strength", "Dosage form",
            "Pack", "UPC", "First marketed", "Current closure"]
    ws.append(head)
    for p in products:
        m = world.META[p["code"]]
        closure = m["closure_new"] or m["closure_old"]
        for upc, _, pack, _ in m["packs"]:
            ws.append([world.PRODUCT_CODE[p["code"]], m["name"], m["maker"], m["ingredient"], m["strength"],
                       m["form"], pack, upc, p["launch"], closure])
    ws2 = wb.create_sheet("Packaging changes")
    ws2.append(["Product code", "Product", "Previous packaging", "Changed packaging",
                "Changed pack first sold at retail", "Change notified to network"])
    for p in products:
        if p["change"] is None:
            continue
        m = world.META[p["code"]]
        ws2.append([world.PRODUCT_CODE[p["code"]], m["name"], m["closure_old"], m["closure_new"], p["change"],
                    world.NOTIFIED[p["code"]]])
    for sh in (ws, ws2):
        for c in sh[1]:
            c.font = Font(bold=True)
        for col in sh.columns:
            width = max(len(str(c.value)) if c.value is not None else 0 for c in col)
            sh.column_dimensions[col[0].column_letter].width = min(max(10, width + 2), 60)
        for row in sh.iter_rows(min_row=2):
            for c in row:
                if isinstance(c.value, dt.date):
                    c.number_format = "yyyy-mm-dd"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    wb.save(path)
    normalise_zip(path, (2026, 10, 30, 16, 40, 0), world.PEOPLE["lead"])


def centers(path):
    return write_csv(path, ["member_center", "center_name", "states_served", "call_log_time_zone"],
                     [[c[0], c[1], c[2], c[3]] for c in world.CENTERS])


def hospitals(path):
    return write_csv(path, ["hospital_code", "hospital", "city", "state", "member_center"],
                     [list(h) for h in world.HOSPITALS])


def census(path, seed):
    rng = np.random.default_rng(seed)
    base = {"KS": 214000, "NE": 147000, "ND": 63000, "SD": 72000, "MN": 401000, "MI": 640000, "OH": 806000,
            "KY": 318000, "MO": 431000, "AR": 211000, "IA": 222000, "WI": 384000, "IN": 474000, "IL": 838000,
            "CO": 371000}
    rows = []
    for st, b in base.items():
        for y in range(2019, 2027):
            v = b * (1 - 0.007 * (y - 2019)) * (1 + rng.normal(0, 0.004))
            rows.append([st, str(y), str(int(round(v, -1))), "July 1 estimate" if y < 2026 else "July 1 projection"])
    return write_csv(path, ["state", "year", "population_age_0_5", "basis"], rows)


def adverse_events(path, seed):
    rng = np.random.default_rng(seed)
    terms = {"FKJ": ["Accidental exposure to product by child", "Vomiting", "Product taste abnormal",
                     "Incorrect dose administered"],
             "DOZ": ["Somnolence", "Dry mouth", "Accidental overdose", "Hallucination"],
             "GUM": ["Accidental exposure to product by child", "Abdominal pain", "Product colour issue"],
             "EYE": ["Eye irritation", "Accidental exposure to product by child", "Somnolence"],
             "NIC": ["Nausea", "Hiccups", "Accidental exposure to product by child", "Palpitations"],
             "IBC": ["Vomiting", "Rash", "Incorrect dose administered"],
             "VAP": ["Skin irritation", "Accidental exposure to product by child", "Seizure"],
             "CGH": ["Somnolence", "Dizziness", "Accidental exposure to product by child"],
             "FKI": ["Incorrect dose administered", "Vomiting"], "ALC": ["Somnolence", "Headache"],
             "IBT": ["Dyspepsia", "Rash"], "FER": ["Constipation", "Abdominal pain", "Accidental overdose"]}
    rows = []
    n = 0
    for code, tl in terms.items():
        k = int(rng.integers(40, 160))
        for _ in range(k):
            d = dt.date(2019, 1, 1) + dt.timedelta(days=int(rng.integers(0, 2860)))
            n += 1
            rows.append(["AER-%07d" % (2210000 + n * 7 + int(rng.integers(0, 6))), d.isoformat(),
                         world.META[code]["name"], str(rng.choice(["Consumer", "Physician", "Pharmacist",
                                                                    "Manufacturer", "Nurse"])),
                         str(rng.choice(["0-5", "6-11", "12-17", "18-64", "65+", "Unknown"])),
                         tl[int(rng.integers(0, len(tl)))], "Y" if rng.random() < 0.18 else "N"])
    rows.sort(key=lambda r: r[1])
    return write_csv(path, ["report_id", "received_date", "product", "reporter_type", "patient_age_group",
                            "reaction_term", "serious"], rows)
