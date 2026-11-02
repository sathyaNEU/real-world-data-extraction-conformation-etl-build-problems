"""task163 documents: the contract's service-level schedule, the pack-bench and returns-bench procedures on file,
Ravelrig's monthly invoices and the 2027 slotting plan. No document describes a data file: each says what its owner
would say in it and nothing about how the files fit together."""
from __future__ import annotations

import datetime as dt
import os

import common as K
import pack as PK
import world as W

INK = "#2B2B2B"


def _pdf(path, story_fn, title, author):
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=56, rightMargin=56, topMargin=60, bottomMargin=56,
                            title=title, author=author, creator="", producer="", invariant=1)
    doc.build(story_fn())


def _styles():
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.enums import TA_LEFT
    base = ParagraphStyle("b", fontName="Helvetica", fontSize=9.6, leading=13.2, spaceAfter=6, alignment=TA_LEFT)
    return dict(
        base=base,
        h1=ParagraphStyle("h1", parent=base, fontName="Helvetica-Bold", fontSize=14, leading=18, spaceAfter=10),
        h2=ParagraphStyle("h2", parent=base, fontName="Helvetica-Bold", fontSize=10.5, leading=14, spaceBefore=8,
                          spaceAfter=4),
        small=ParagraphStyle("s", parent=base, fontSize=8, leading=10.5, textColor="#555555"),
    )


def schedule3(path):
    from reportlab.platypus import Paragraph, Spacer
    S = _styles()

    def story():
        P = lambda t, s="base": Paragraph(t, S[s])
        return [
            P("Fulfilment Services Agreement: Lathmor Logistics Ltd and Aubrine Ltd", "small"),
            P("Schedule 3: Service levels", "h1"),
            P("This schedule forms part of the agreement dated 6 January 2025 and applies from that date. It replaces "
              "the service levels in the proposal of 14 October 2024."),
            P("3.1 Contract year", "h2"),
            P("Each contract year runs from 1 January to 31 December. Service levels are measured over the contract "
              "year unless this schedule says otherwise."),
            P("3.2 Order accuracy", "h2"),
            P("Validated mis-pick claims shall not exceed 2.5 per 10,000 order lines despatched in a contract year."),
            P("A mis-pick claim is a claim by a customer that a parcel held a product other than the one ordered, "
              "lodged with Aubrine within 28 days of delivery and validated by Lathmor against the order. A claim "
              "counts against the order line it was lodged on, in the contract year in which Lathmor despatched that "
              "line. An order line is one product on one customer order, whatever the quantity ordered."),
            P("3.3 Despatch", "h2"),
            P("Orders released to Lathmor by 14:00 on a working day shall be despatched the same day, for at least 98.0 "
              "per cent of such orders in each week."),
            P("3.4 Stock accuracy", "h2"),
            P("At least 99.5 per cent of pick faces counted in each quarter shall hold the quantity the warehouse "
              "management system records."),
            P("3.5 Service credits", "h2"),
            P("For a contract year in which order accuracy is above the level in 3.2, Lathmor shall credit Aubrine "
              "GBP 38.00 for each validated mis-pick claim above that level, on the first invoice after the contract "
              "year closes. For a week below the level in 3.3, Lathmor shall credit GBP 450.00."),
            P("3.6 Reporting and review", "h2"),
            P("Lathmor reports each service level monthly. Either party may ask for a review of a service level when "
              "a change to the operation is planned; a change that Lathmor proposes does not alter a service level "
              "unless both parties agree it in writing."),
            Spacer(1, 18),
            P("Signed for Lathmor Logistics Ltd: Brian Cook, Account Director. Signed for Aubrine Ltd: Hazel Collins, "
              "Head of E-commerce Operations.", "small"),
        ]
    _pdf(path, story, "Schedule 3 - Service levels", "Lathmor Logistics Ltd")


def pack_bench(path):
    from reportlab.platypus import Paragraph
    S = _styles()

    def story():
        P = lambda t, s="base": Paragraph(t, S[s])
        return [
            P("Lathmor Logistics, Uphall. Controlled document PB-SOP-02, issue 5, May 2025", "small"),
            P("Pack bench procedure", "h1"),
            P("1. Purpose", "h2"),
            P("To pack each customer order in the carton the warehouse management system (WMS) gives, and to stop a "
              "parcel leaving the bench when its weight does not match the order."),
            P("2. Packing", "h2"),
            P("Scan the tote. Pack the items into the carton shown on the bench screen, with the inserts and the "
              "despatch note. Seal the carton and apply the carrier label."),
            P("3. Check-weigh", "h2"),
            P("Place the sealed parcel on the bench scale. The WMS takes the expected weight from the order: each "
              "item at its unit weight in the item master, times the quantity, plus the carton's tare. A parcel more "
              "than 15 g over or under its expected weight is held: the screen shows HOLD and the parcel goes to the "
              "holds cage. A parcel within 15 g is released to the carrier cage."),
            P("4. Holds", "h2"),
            P("At the exceptions bench, open the held parcel and check every item against the order. Record the cause "
              "on the hold screen: MISPICK, an item other than the one ordered; SHORT, an item missing; EXTRA, more "
              "units than ordered; PACKAGING, the wrong carton or a missing insert; NO FAULT FOUND, nothing wrong "
              "with the contents. For a MISPICK, scan the item found and the item expected. Correct the parcel, "
              "re-seal it and re-weigh it."),
            P("5. Scales", "h2"),
            P("Each bench scale is checked at the start of every shift with the 500 g test weight. A scale reading "
              "more than 2 g away is taken out of use and reported to engineering."),
            P("Owner: Head of Quality, Uphall. Next review: May 2027.", "small"),
        ]
    _pdf(path, story, "PB-SOP-02 Pack bench procedure", "Lathmor Logistics Ltd")


def returns_bench(path):
    from reportlab.platypus import Paragraph
    S = _styles()

    def story():
        P = lambda t, s="base": Paragraph(t, S[s])
        return [
            P("Lathmor Logistics, Uphall. Controlled document RB-SOP-04, issue 3, March 2025", "small"),
            P("Returns grading procedure", "h1"),
            P("1. Purpose", "h2"),
            P("To decide what happens to each unit a customer sends back to Aubrine, and to record it against the "
              "return."),
            P("2. Receiving", "h2"),
            P("Open each returns parcel at a returns station. Scan the return reference on the returns label, then "
              "inspect each unit in turn."),
            P("3. Grades", "h2"),
            P("Grade 1: sealed and undamaged. Return to stock."),
            P("Grade 2: product sealed and undamaged, outer packaging marked or damaged. Place in the Ravelrig cage "
              "for repack; Ravelrig returns repacked units to stock."),
            P("Grade 3: opened, used, damaged or past its date. Place in the scrap cage."),
            P("4. Recording", "h2"),
            P("Write the return reference, the item code and the grade on the bench sheet. The returns administrator "
              "keys each sheet into the WMS before the end of the shift."),
            P("Owner: Returns Team Leader, Uphall. Next review: March 2027.", "small"),
        ]
    _pdf(path, story, "RB-SOP-04 Returns grading procedure", "Lathmor Logistics Ltd")


def ravelrig(path, bills):
    from reportlab.platypus import Paragraph, Table, TableStyle, PageBreak, Spacer
    from reportlab.lib import colors
    S = _styles()

    def story():
        P = lambda t, s="base": Paragraph(t, S[s])
        out = []
        for k, ((y, m), net) in enumerate(sorted(bills.items())):
            issued = dt.date(y + (m == 12), m % 12 + 1, 3)
            while issued.weekday() >= 5:
                issued += dt.timedelta(1)
            vat = round(net * 0.2, 2)
            out += [
                P("Ravelrig Packing Ltd", "h1"),
                P("Unit 7, Kirkton South Road, Livingston EH54 7BW. VAT reg. GB 318 4402 61", "small"),
                Spacer(1, 10),
                P("Invoice to: Lathmor Logistics Ltd, Uphall fulfilment centre, Uphall EH52 6AT"),
                P("Invoice number: RP-%d%02d-%03d &nbsp;&nbsp; Date: %s &nbsp;&nbsp; Account: LATH01"
                  % (y % 100, m, 40 + k, K.uk_date(issued))),
                Spacer(1, 8),
            ]
            t = Table([["Description", "Net (GBP)"],
                       ["Re-work of returned stock for Aubrine, %s %d" % (K.MONTH_NAMES[m], y), "%.2f" % net],
                       ["VAT at 20%", "%.2f" % vat],
                       ["Total due", "%.2f" % (net + vat)]], colWidths=[330, 120])
            t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", 9.5),
                                   ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 9.5),
                                   ("FONT", (0, -1), (-1, -1), "Helvetica-Bold", 9.5),
                                   ("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.black),
                                   ("LINEABOVE", (0, -1), (-1, -1), 0.6, colors.black),
                                   ("ALIGN", (1, 0), (1, -1), "RIGHT")]))
            out += [t, Spacer(1, 14),
                    P("Prices held at the 2025/26 contract rates. Payment 30 days from the invoice date to the account "
                      "on file.", "small")]
            if k < len(bills) - 1:
                out.append(PageBreak())
        return out
    _pdf(path, story, "Ravelrig Packing invoices", "Ravelrig Packing Ltd")


def plan(path, w):
    import openpyxl
    from openpyxl.styles import Font, PatternFill, Alignment
    by = {s["sku"]: s for s in w["skus"]}
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Summary"
    rows = [
        ("Aubrine shelving re-slot by product family", ""),
        ("", ""),
        ("Site", "Uphall fulfilment centre"),
        ("Scope", "Zones B, C and D (static shelving, aisles B11 to D19)"),
        ("Not in scope", "Zone A carton flow (aisle A01): unchanged"),
        ("Moves", "Christmas shutdown, 24 December 2026 to 3 January 2027"),
        ("Go-live", "Monday 4 January 2027"),
        ("Slotting rule", "Families in aisle blocks; within a family, best-selling lines first; each line's shades and "
                          "sizes side by side"),
        ("Forecast basis", "Aubrine demand plan of 12 October 2026: 2027 order lines by item (sheet Faces 2027)"),
        ("Pick travel, zones B to D", "418 m per 100 order lines now; 341 m per 100 order lines on the plan"),
        ("Picking hours saved in 2027", "3,050 (estimate)"),
        ("Prepared by", "Uphall site engineering"),
        ("Approved for go-live", "B. Cook, 14 October 2026"),
    ]
    for r in rows:
        ws.append(list(r))
    ws["A1"].font = Font(bold=True, size=13)
    for c in ws["A"][2:]:
        c.font = Font(bold=True)
    ws.column_dimensions["A"].width = 30
    ws.column_dimensions["B"].width = 96
    for row in ws.iter_rows(min_row=3):
        row[1].alignment = Alignment(wrap_text=True, vertical="top")
    ws2 = wb.create_sheet("Faces 2027")
    ws2.append(["Location", "Aubrine code", "Description", "Family", "Forecast lines 2027"])
    for c in ws2[1]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor="1F4E5F")
    for sku, (run, p) in sorted(w["plan"].items(), key=lambda kv: PK.plan_loc(*kv[1])):
        s = by[sku]
        ws2.append([PK.plan_loc(run, p), s["aub"], s["desc"], s["family"], w["fc"][sku]])
    for row in ws2.iter_rows(min_row=2):
        row[4].number_format = "#,##0"
    for col, wd in zip("ABCDE", (16, 15, 40, 15, 19)):
        ws2.column_dimensions[col].width = wd
    ws2.freeze_panes = "A2"
    wb.save(path)


def write_all(out, w):
    schedule3(os.path.join(out, PK.F_SCHED))
    pack_bench(os.path.join(out, PK.F_PBSOP))
    returns_bench(os.path.join(out, PK.F_RBSOP))
    bills = PK.ravelrig_bills(w)
    ravelrig(os.path.join(out, PK.F_RAV), bills)
    plan(os.path.join(out, PK.F_PLAN), w)
    return {PK.F_SCHED: 1, PK.F_PBSOP: 1, PK.F_RBSOP: 1, PK.F_RAV: len(bills), PK.F_PLAN: len(w["plan"])}
