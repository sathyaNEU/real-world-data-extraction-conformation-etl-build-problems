"""The documents of task171's pack: the toll schedule and toll-by-mail policy (PDF), the AET cutover revenue plan
(DOCX), the data dictionary (XLSX), the export manifest; and the writers, with fixed stamps so two builds are
byte-identical."""
from __future__ import annotations

import datetime as dt
import re
import zipfile

import numpy as np
import pandas as pd

import common as C

FIXED = dt.datetime(2026, 11, 12, 9, 14, 0)


def money(x):
    return "$%.2f" % x


# ---------------------------------------------------------------- toll schedule and toll-by-mail policy (PDF)
def policy_text():
    c25, c26 = C.CASH[2025], C.CASH[2026]
    def row(pz, cc):
        return "  %-10s  %s" % (C.PLAZA_NAME[pz], "   ".join("class %d %s" % (k, money(cc[pz] * m)) for k, m in zip(range(1, 6), [1, 2, 3, 4, 5])))
    pages = []
    pages.append(("Marrowfield Turnpike Authority", [
        "Toll schedule and toll-by-mail policy",
        "Board resolution 2025-31 as amended by resolution 2026-08. Issued by the Office of Toll Revenue, 2 February 2026.",
        "",
        "1. Tolls",
        "1.1 A toll is charged at each mainline plaza (Vellacott, milepost 6.2; Brannock, milepost 24.8; Ostrey, milepost 41.5), in each direction. The toll class is set by the axles the lane's classifier counts: class 1 two axles, class 2 three, class 3 four, class 4 five, class 5 six or more.",
        "1.2 Cash rate, effective 1 January 2025:",
        row("VEL", c25), row("BRN", c25), row("OST", c25),
        "1.3 Cash rate, effective 1 January 2026, and unchanged for 2027:",
        row("VEL", c26), row("BRN", c26), row("OST", c26),
        "1.4 A crossing posted to a MarrowPass account is charged 80 per cent of the cash rate, rounded to the cent. A crossing billed by mail is charged the cash rate.",
        "",
        "2. Lanes",
        "2.1 Express lanes E1 and E2 at each plaza are open-road lanes for MarrowPass accounts. A crossing of an express lane by a vehicle without a valid MarrowPass is a violation.",
        "2.2 Booth lanes B1 to B4 take cash, cards and MarrowPass. From 3 March 2025 the booths are closed from 11:00 p.m. to 5:00 a.m. every night, and a vehicle crossing a closed booth lane without a MarrowPass is billed by mail (toll-by-mail).",
        "2.3 From 4 January 2027 every lane is an open-road lane and the booths are removed; every crossing without a valid MarrowPass is billed by mail.",
    ]))
    pages.append(("Marrowfield Turnpike Authority  -  toll schedule and toll-by-mail policy", [
        "3. Invoices",
        "3.1 The back office issues one invoice to the registered owner of a plate for each calendar month of its crossings billed by mail, on the eighth day of the next month or the next weekday after it. A toll-by-mail invoice carries an invoice fee of $1.50 and a violation invoice a violation fee of $5.00.",
        "3.2 An invoice is due 30 days after it is issued. A late fee of $5.00 is added to an invoice unpaid 35 days after it is issued.",
        "3.3 A payment is applied to the invoice it names, toll first, then the invoice or violation fee, then the late fee and the collection fee. A payment covering several invoices is applied oldest invoice first.",
        "",
        "4. Enforcement",
        "4.1 Sixty days after an invoice is issued, a balance still unpaid on a plate registered in this state is referred to the Division of Motor Vehicles, which places a hold on the registration. The Division does not renew a registration on hold until the Authority's balance on that plate is paid, and remits what it collects to the Authority on the day of payment.",
        "4.2 Registrations in this state run for two years and expire at the end of the owner's birth month. The Division accepts a renewal from 45 days before the expiry date to the expiry date.",
        "4.3 Ninety days after an invoice is issued, a balance still unpaid on a plate registered elsewhere, or on a plate the Division has no record of, is placed with the Authority's collection agency, and a collection fee of 20 per cent of the balance is added. The agency returns an invoice it has not collected 270 days after placement.",
        "4.4 Toll-by-mail invoices are placed with Corrigan Mott Recovery and violation invoices with Benbow Associates. Each remits what it collects on the day it is collected.",
        "4.5 A registered owner may dispute an invoice within 30 days of its issue.",
    ]))
    return pages


def write_pdf(path, pages, author="Office of Toll Revenue", title="Toll schedule and toll-by-mail policy", stamp="D:20260202101500-05'00'"):
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.utils import simpleSplit
    from reportlab.pdfgen import canvas
    c = canvas.Canvas(path, pagesize=letter, invariant=1, pageCompression=1)
    c.setAuthor(author); c.setTitle(title); c.setSubject("Resolution 2025-31 as amended"); c.setCreator(author); c.setProducer(author)
    for pno, (head, lines) in enumerate(pages, 1):
        y = 740
        c.setFont("Helvetica-Bold", 12); c.drawString(54, y, head); y -= 24
        for ln in lines:
            bold = bool(re.match(r"^\d\. ", ln)) or ln == "Toll schedule and toll-by-mail policy"
            font = "Courier" if ln.startswith("  ") else ("Helvetica-Bold" if bold else "Helvetica")
            size = 8.2 if font == "Courier" else 9.5
            c.setFont(font, size)
            for part in (simpleSplit(ln, font, size, 505) or [""]):
                c.drawString(54, y, part); y -= 13
            if bold:
                y -= 2
        c.setFont("Helvetica", 8); c.drawString(54, 40, "Marrowfield Turnpike Authority  |  Office of Toll Revenue  |  page %d of %d" % (pno, len(pages)))
        c.showPage()
    c.save()
    raw = open(path, "rb").read()
    for a in (b"ReportLab Generated PDF document http://www.reportlab.com", b"ReportLab PDF Library - www.reportlab.com", b"ReportLab"):
        while a in raw:
            rep = b"Office of Toll Revenue"[:len(a)].ljust(len(a))
            raw = raw.replace(a, rep, 1)
    raw = raw.replace(b"D:20000101000000+00'00'", stamp.encode())
    open(path, "wb").write(raw)


# ---------------------------------------------------------------- the AET cutover revenue plan (DOCX)
def plan_items():
    i, o = C.PLAN_TOLL["IS"], C.PLAN_TOLL["OS"]
    return [
        ("h", "All-electronic tolling cutover: the toll-by-mail line of the 2027 revenue certificate"),
        ("p", "AET programme note PN-14, from Brittany Moon, AET Programme Manager, to the Chief Financial Officer. 10 November 2026."),
        ("h2", "What the certificate needs from the programme"),
        ("p", "The trust agreement asks for the certificate before the year begins, and 2027 is the first year without cash. Two figures go in its toll-by-mail line. The first is the programme's: of the toll we will bill by mail in 2027 to the vehicles that pay cash at the booths today, how much we will collect. Count the toll we collect on those invoices however long the registration hold or the agency takes to collect it. Invoice, late and collection fees are budgeted separately and are not part of the figure."),
        ("p", "Traffic has put the toll on those vehicles' 2027 crossings, at 2026 traffic and the 2027 rates (unchanged from 2026), after image review, so only crossings an invoice can go to: $%s on plates registered in this state and $%s on plates registered elsewhere." % ("{:,}".format(i), "{:,}".format(o))),
        ("p", "The second figure is Enforcement's, for the violation part of the same line, which continues as toll-by-mail after the cutover: the violation crossings of each month of 2026 to September and the toll they owe, and how the out-of-state violation invoices issued from April 2025 to March 2026 have collected up to 31 October 2026, by quarter of issue."),
        ("h2", "How the cash lanes' users are billed today"),
        ("p", "Since 3 March 2025 the booths have been closed from 11 p.m. to 5 a.m., and a vehicle crossing a closed booth lane without a MarrowPass has been billed by mail at the cash rate, on the same invoice cycle and enforcement as the violation invoices. From 4 January 2027 every crossing without a MarrowPass is billed that way."),
        ("h2", "Records"),
        ("p", "Zachary Mcneil's team exported the toll-by-mail back office on 9 November: invoice lines, invoices with their status at 31 October 2026, and payments. The Division of Motor Vehicles' hold returns and the agency's placements come with it, and the account system has exported the commercial MarrowPass postings of January to September 2026."),
    ]


def write_docx(path, items, author="Brittany Moon", created=dt.datetime(2026, 11, 10, 8, 40)):
    import docx
    from docx.shared import Pt
    d = docx.Document()
    st = d.styles["Normal"]; st.font.name = "Calibri"; st.font.size = Pt(10.5)
    for kind, text in items:
        if kind == "h":
            d.add_heading(text, level=1)
        elif kind == "h2":
            d.add_heading(text, level=2)
        else:
            d.add_paragraph(text)
    cp = d.core_properties
    cp.author = author; cp.last_modified_by = author; cp.title = "PN-14 AET cutover toll-by-mail revenue"
    cp.created = created; cp.modified = created; cp.revision = 4
    d.save(path)
    normalise_zip(path, created)


def normalise_zip(path, stamp):
    with zipfile.ZipFile(path) as z:
        items = [(i, z.read(i.filename)) for i in z.infolist()]
    iso = stamp.strftime("%Y-%m-%dT%H:%M:%SZ")
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for i, data in sorted(items, key=lambda t: t[0].filename):
            if i.filename == "docProps/app.xml":
                appname = b"Microsoft Excel" if path.endswith(".xlsx") else b"Microsoft Office Word"
                data = re.sub(rb"<Application>[^<]*</Application>", b"<Application>" + appname + b"</Application>", data)
                data = re.sub(rb"<AppVersion>[^<]*</AppVersion>", b"<AppVersion>16.0300</AppVersion>", data)
            data = data.replace(b"python-docx", b"").replace(b"openpyxl", b"").replace(b"Openpyxl", b"")
            if i.filename == "docProps/core.xml":
                data = re.sub(rb"(<dcterms:modified[^>]*>)[^<]*(</dcterms:modified>)", rb"\g<1>" + iso.encode() + rb"\g<2>", data)
                data = re.sub(rb"(<dcterms:created[^>]*>)[^<]*(</dcterms:created>)", rb"\g<1>" + iso.encode() + rb"\g<2>", data)
            zi = zipfile.ZipInfo(i.filename, date_time=stamp.timetuple()[:6])
            zi.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(zi, data)


def write_xlsx(path, sheets, author="Toll systems"):
    import openpyxl
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    for name, df in sheets:
        ws = wb.create_sheet(name)
        ws.append(list(df.columns))
        for row in df.itertuples(index=False):
            ws.append([None if (isinstance(v, float) and np.isnan(v)) else v for v in row])
    wb.properties.creator = author; wb.properties.lastModifiedBy = author
    wb.properties.created = FIXED; wb.properties.modified = FIXED
    wb.save(path)
    normalise_zip(path, FIXED)


DICT = {
    C.F_LINES: [("line_id", "Invoice line"), ("invoice_no", "Invoice the crossing is billed on"), ("plate", "Plate as read and confirmed at image review"),
                ("plate_state", "Issuing jurisdiction of the plate; plates of this state are written HM"),
                ("crossed_at", "Time the lane recorded the vehicle, local time, to the millisecond"), ("plaza", "Plaza code"), ("direction", "NB or SB"),
                ("lane", "Lane at the plaza"), ("axles", "Axles counted by the lane classifier"), ("toll_class", "Toll class from the axle count"),
                ("toll", "Toll billed for the crossing at the cash rate in force on the day")],
    C.F_INV: [("invoice_no", "Invoice"), ("invoice_type", "TOLL-BY-MAIL (closed booth lanes) or VIOLATION (express lanes)"),
              ("plate", "Plate"), ("plate_state", "Issuing jurisdiction; HM is this state"), ("issued_on", "Issue date"), ("due_on", "Due date"),
              ("crossings", "Lines on the invoice"), ("toll_billed", "Toll on the invoice's lines"), ("invoice_fee", "Invoice fee or violation fee"),
              ("late_fee", "Late fee added at 35 days"), ("collection_fee", "Collection fee added at placement with the agency"),
              ("status", "Status at 31 October 2026: OPEN, PAID, DMV HOLD, AT AGENCY, RETURNED")],
    C.F_PAY: [("payment_id", "Payment"), ("invoice_no", "Invoice the payment names"), ("posted_on", "Date posted to the back office"),
              ("channel", "WEB, IVR, MAIL, WALKIN, DMV, AGENCY, or REVERSAL for a returned payment"), ("amount", "Amount, dollars; a reversal is negative"),
              ("reference", "Remittance reference")],
    C.F_MVD: [("request_id", "Hold request"), ("invoice_no", "Invoice referred"), ("plate", "Plate"), ("requested_on", "Date the hold was requested"),
              ("response", "HOLD PLACED or NO RECORD"), ("reg_expires", "Month the registration on file expires (MM/YYYY), as returned with the hold"),
              ("released_on", "Date the hold on this invoice was released"), ("release_reason", "Why it was released")],
    C.F_AGY: [("invoice_no", "Invoice placed"), ("agency", "Agency holding the invoice"), ("placed_on", "Date placed with the agency"), ("status", "AT AGENCY, COLLECTED or RETURNED UNCOLLECTED"),
              ("closed_on", "Date the agency closed it")],
    C.F_TAG: [("posting_id", "Account posting"), ("account_no", "Commercial MarrowPass account"), ("tag_id", "Transponder"), ("plate", "Plate on file for the tag"),
              ("plate_state", "Issuing jurisdiction; HM is this state"), ("posted_at", "Time the lane recorded the vehicle, local time, to the millisecond"),
              ("plaza", "Plaza code"), ("direction", "NB or SB"), ("lane", "Lane"), ("axles_detected", "Axles counted by the lane classifier"),
              ("toll_class", "Toll class from the axle count"), ("toll", "Toll posted at the MarrowPass rate")],
    C.F_LANES: [("plaza", "Plaza code"), ("plaza_name", "Plaza"), ("milepost", "Milepost"), ("direction", "Direction"), ("lane_ref", "Lane reference"),
                ("lane", "Lane"), ("lane_type", "EXPRESS or BOOTH"), ("payment", "What the lane takes")],
    C.F_TRAFFIC: [("month", "Month"), ("plaza", "Plaza"), ("direction", "Direction"), ("hour", "Hour of day, local"),
                  ("marrowpass", "Transactions posted to MarrowPass"), ("cash_or_card", "Transactions paid at a booth"),
                  ("camera_billed", "Transactions sent to image review")],
    C.F_IMG: [("capture_month", "Month of the crossings"), ("lane_type", "EXPRESS or BOOTH"), ("captures", "Vehicles without a MarrowPass read imaged"),
              ("plate_unreadable", "Images with no readable plate"), ("no_owner_found", "Plates read with no registered owner found"),
              ("invoiced", "Crossings put on an invoice")],
}
