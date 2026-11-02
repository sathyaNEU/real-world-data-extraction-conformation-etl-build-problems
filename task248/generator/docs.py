"""The pack's documents and small lookups: the register, piping record, close-out sheets, the point-of-sale grade
table, Fuel Systems Standard FS-3 and the monitoring service's onboarding letter."""
import os, zipfile, datetime as dt
import numpy as np
import params as P

TRUCKS = ["T-114", "T-121", "T-127", "T-133", "T-140"]
FIXED_ZIP = (2027, 1, 11, 16, 40, 0)


def pos_grades():
    """the new point of sale numbers each site's grades in the order its installer set the dock up"""
    tab = {}
    for m in P.MARINAS:
        prods = [P.TANKS[k][1] for k in P.TANKS if P.TANKS[k][0] == m]
        order = []
        for pr in prods:
            if pr not in order:
                order.append(pr)
        if m in ("FL", "HS", "CF"):
            order = order[::-1]
        for i, pr in enumerate(order):
            tab[(m, i + 1)] = pr
    return tab


def normalize_zip(path):
    with zipfile.ZipFile(path) as z:
        items = [(i.filename, z.read(i.filename)) for i in z.infolist()]
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in items:
            zi = zipfile.ZipInfo(name, date_time=FIXED_ZIP)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o600 << 16
            z.writestr(zi, data)


def _wb():
    from openpyxl import Workbook
    wb = Workbook()
    wb.properties.creator = "Highbank Marinas"
    wb.properties.lastModifiedBy = "Highbank Marinas"
    wb.properties.created = dt.datetime(2026, 3, 2, 9, 0, 0)
    wb.properties.modified = dt.datetime(2027, 1, 11, 16, 30, 0)
    return wb


def write_register(target, o):
    from openpyxl.styles import Font
    wb = _wb()
    ws = wb.active
    ws.title = "Register"
    ws["A1"] = "Highbank Marinas - underground storage tank register"
    ws["A1"].font = Font(bold=True)
    ws["A2"] = "Rev. 14, 2 March 2026. Heights are product heights in inches above the tank bottom as the gauge reads them."
    hdr = ["Tank", "Marina", "Product", "Capacity (gal)", "Diameter (in)", "Length (in)", "Construction", "Installed",
           "Chart no.", "Reorder height (in)", "Half-full height (in)", "Normal fill height (in)", "Overfill alarm (in)"]
    ws.append([])
    ws.append(hdr)
    for c in ws[4]:
        c.font = Font(bold=True)
    rng = np.random.default_rng(P.SEED + 3)
    for tid, t in o["tanks"].items():
        constr = "FRP double wall" if t.cap in (8000, 12000) or tid in ("BP-2", "HS-1") else "Steel, sti-P3"
        inst = int(rng.choice([1996, 1999, 2003, 2004, 2008, 2011, 2014]))
        ofa = None
        # overfill alarm at 90 per cent of capacity, as a height
        lo, hi = 0.0, t.D
        for _ in range(40):
            mid = (lo + hi) / 2
            if t.chart_gal(mid) < 0.9 * t.cap:
                lo = mid
            else:
                hi = mid
        ofa = round(lo, 1)
        ws.append([tid, P.MARINAS[t.marina][0], P.PRODUCTS[t.product], t.cap, int(t.D), round(t.L0, 1), constr, inst,
                   t.chart_no, int(t.reorder_h), int(t.half_h), int(t.fill_h), ofa])
    for col, w in zip("ABCDEFGHIJKLM", [8, 30, 20, 13, 12, 11, 16, 10, 11, 17, 18, 21, 17]):
        ws.column_dimensions[col].width = w
    path = os.path.join(target, "tank_register.xlsx")
    wb.save(path)
    normalize_zip(path)


def write_piping(target, o):
    from openpyxl.styles import Font
    wb = _wb()
    ws = wb.active
    ws.title = "Dock piping"
    ws["A1"] = "Fuel dock piping by marina (dispenser hose to tank), as built"
    ws["A1"].font = Font(bold=True)
    ws.append([])
    ws.append(["Marina", "Dispenser", "Hose", "Product", "Tank"])
    for c in ws[3]:
        c.font = Font(bold=True)
    for tid, hoses in o["hose_ids"].items():
        t = o["tanks"][tid]
        for h in hoses:
            ws.append([P.MARINAS[t.marina][0], int(h[0]), h, P.PRODUCTS[t.product], tid])
    path = os.path.join(target, "dock_piping.xlsx")
    wb.save(path)
    normalize_zip(path)


def write_closeouts(target, o):
    """the marinas' own monthly inventory reconciliations for the season (gross dock gallons as sold)"""
    from openpyxl.styles import Font
    wb = _wb()
    first = True
    S0 = dt.datetime(2026, 4, 1)
    for m in P.MARINAS:
        ws = wb.active if first else wb.create_sheet()
        first = False
        ws.title = m
        ws["A1"] = "%s - monthly inventory reconciliation, 2026 season" % P.MARINAS[m][0]
        ws["A1"].font = Font(bold=True)
        ws.append([])
        ws.append(["Tank", "Month", "Opening (gal)", "Delivered (gal)", "Sold (gal)", "Closing (gal)", "Over/short (gal)",
                   "Allowed (gal)", "Result"])
        for c in ws[3]:
            c.font = Font(bold=True)
        for tid, t in o["tanks"].items():
            if t.marina != m:
                continue
            reads = [r for r in o["readings_kept"] if r["tank"] == tid]
            for mo in range(4, 11):
                a = dt.datetime(2026, mo, 1); b = dt.datetime(2026, mo + 1, 1)
                ra = [r for r in reads if a <= r["local"] < a + dt.timedelta(hours=26)]
                rb = [r for r in reads if b - dt.timedelta(hours=2) <= r["local"] < b + dt.timedelta(hours=26)]
                if not ra or not rb:
                    continue
                op, cl = ra[0]["tc"], rb[0]["tc"]
                t0, t1 = ra[0]["local"], rb[0]["local"]
                dl = sum(x["net"] for x in o["bols"] if x["tank"] == tid and t0 <= x["local"] < t1)
                sold = sum(s["gal_reg"] for s in o["sales"] if s["tank"] == tid and t0 <= s["local"] < t1)
                os_ = cl - (op + dl - sold)
                allowed = 0.01 * sold + 130
                ws.append([tid, a.strftime("%b %Y"), round(op), round(dl), round(sold), round(cl), round(os_),
                           round(allowed), "PASS" if abs(os_) <= allowed else "FAIL"])
    path = os.path.join(target, "monthly_closeouts_2026.xlsx")
    wb.save(path)
    normalize_zip(path)


def _pdf(path, title, author, blocks):
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib import colors
    from reportlab import rl_config
    rl_config.invariant = 1
    ss = getSampleStyleSheet()
    body = ParagraphStyle("b", parent=ss["Normal"], fontName="Helvetica", fontSize=9.5, leading=12.5, spaceAfter=5)
    h = ParagraphStyle("h", parent=ss["Normal"], fontName="Helvetica-Bold", fontSize=10.5, leading=13, spaceBefore=6, spaceAfter=3)
    t = ParagraphStyle("t", parent=ss["Normal"], fontName="Helvetica-Bold", fontSize=13, leading=16, spaceAfter=6)
    story = []
    for kind, val in blocks:
        if kind == "T":
            story.append(Paragraph(val, t))
        elif kind == "H":
            story.append(Paragraph(val, h))
        elif kind == "P":
            story.append(Paragraph(val, body))
        elif kind == "S":
            story.append(Spacer(1, val))
        elif kind == "TAB":
            tb = Table(val, hAlign="LEFT")
            tb.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", 9), ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 9),
                                    ("GRID", (0, 0), (-1, -1), 0.4, colors.grey), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
            story.append(tb)
    doc = SimpleDocTemplate(path, pagesize=letter, leftMargin=60, rightMargin=60, topMargin=54, bottomMargin=54,
                            title=title, author=author, subject="", creator=author, producer=author)
    doc.build(story)


def write_fs3(target):
    blocks = [
        ("T", "Highbank Marinas - Fuel Systems Standard FS-3"),
        ("P", "Tank gauging, deliveries and inventory records. Revision 6, approved 14 September 2026 by the Director of Marina Operations. Applies to every underground tank on the tank register."),
        ("H", "1. Records"),
        ("P", "1.1 The tank register lists each tank, its chart number and its reorder, half-full and normal fill heights. The gauge console at each marina converts the probe's product height to gallons with the chart the register names."),
        ("P", "1.2 Dock sales are the gallons the dock meters register at the point of sale. Deliveries are recorded on the distributor's bill of lading."),
        ("H", "2. Units"),
        ("P", "2.1 Stock, sales and deliveries are reconciled in net gallons at 60 F. Gross gallons are corrected to 60 F as net = gross x (1 - k x (T - 60)), with T the product temperature in degrees F and k from Table 1."),
        ("TAB", [["Table 1. Product", "k per degree F"], ["REC-90 ethanol-free", "0.00068"], ["E10 unleaded", "0.00069"], ["Diesel", "0.00046"]]),
        ("H", "3. Charts"),
        ("P", "3.1 Each tank's chart is the table its console converts height with; a chart is replaced only by the calibration contractor's re-chart of that tank."),
        ("P", "3.2 Charts are reviewed before the marinas move onto a new monitoring service."),
        ("P", "3.3 The contractor enters a re-chart at the console and the register takes the new chart number the same day."),
        ("P", "3.4 Before a tank goes onto the wetstock monitoring service, its chart must not misstate the change in stock between any two of its reorder, half-full and normal fill heights by more than 25 gallons. A misstatement is the gallons by which the chart's change between two heights differs from the gallons that actually went into or out of the tank between them, read from the tank's 2026 boating season (1 April to 31 October). A tank whose chart misstates more is re-charted by the calibration contractor before the service starts."),
        ("H", "4. Monthly reconciliation"),
        ("P", "4.1 Each marina reconciles each tank monthly: closing stock against opening stock plus deliveries less sales. A month passes when the over or short is within 1 per cent of the month's sales plus 130 gallons."),
        ("H", "5. Deliveries"),
        ("P", "5.1 The bill of lading's net gallons are the gallons delivered."),
        ("H", "6. Release detection"),
        ("P", "6.1 Each tank needs a passing 0.2 gallon-per-hour test in every calendar month, the month being the one in which the test ran (local time)."),
    ]
    _pdf(os.path.join(target, "FS-3_fuel_systems_standard.pdf"), "Fuel Systems Standard FS-3", "Highbank Marinas", blocks)


def write_letter(target):
    blocks = [
        ("T", "Clearline Wetstock Services"),
        ("P", "3 December 2026"),
        ("P", "Theresa Shelton, Fuel Systems and Compliance, Highbank Marinas"),
        ("H", "Onboarding for the 2027 season"),
        ("P", "Thank you for confirming the eight marinas for monitoring from 1 April 2027. Our analysts will take each console's feed directly from that date."),
        ("P", "Feed readiness. We start a tank on full monitoring when its gauge sent an inventory reading on at least 355 of the days of 2026; a tank below that begins with a 60-day observation period. A day is the marina's local calendar day. Please let us have, for each tank, the number of days in 2026 on which its gauge sent no inventory reading."),
        ("P", "Release detection. Please send the number of tank-months in 2026, for each marina, without a passing monthly 0.2 gallon-per-hour test, so that our first report can carry the year forward."),
        ("P", "Enrolment. Your fee schedule is set on each marina's 2026 dock gallons by product."),
        ("P", "Charts. We will flag a chart that our daily analysis cannot reconcile; any tank you re-chart over the winter should reach us with its new chart number."),
        ("P", "Miranda Collins, Onboarding"),
    ]
    _pdf(os.path.join(target, "wetstock_onboarding_2027.pdf"), "Onboarding for the 2027 season", "Clearline Wetstock Services", blocks)


def write_documents(target, o, idm):
    write_register(target, o)
    write_piping(target, o)
    write_closeouts(target, o)
    write_fs3(target)
    write_letter(target)
