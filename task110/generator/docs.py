"""Documents in target/: the group's migration standard and verification procedure, Yacaaba's FY2025
accounts extract, the Raymond Terrace count sheet, the cutover thread, the extract notes and the
sources record. Short and functional, in the voice of the people who wrote them."""
import datetime as dt
import random
from decimal import Decimal

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import ledger as L
from params import ACCOUNTS, SITES

D = Decimal
Z = D("0")

SS = getSampleStyleSheet()
BODY = ParagraphStyle("body", parent=SS["Normal"], fontName="Helvetica", fontSize=9.6, leading=13, spaceAfter=5)
SMALL = ParagraphStyle("small", parent=BODY, fontSize=8, leading=10, textColor=colors.HexColor("#444444"))
H1 = ParagraphStyle("h1", parent=BODY, fontName="Helvetica-Bold", fontSize=13, leading=16, spaceAfter=4)
H2 = ParagraphStyle("h2", parent=BODY, fontName="Helvetica-Bold", fontSize=10.2, leading=13, spaceBefore=7, spaceAfter=3)


def _doc(path, title, author):
    return SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm,
                             bottomMargin=18 * mm, title=title, author=author, invariant=1)


CELL = ParagraphStyle("cell", parent=BODY, fontSize=8.2, leading=10, spaceAfter=0)
CELLB = ParagraphStyle("cellb", parent=CELL, fontName="Helvetica-Bold")
CELLR = ParagraphStyle("cellr", parent=CELL, alignment=2)
CELLRB = ParagraphStyle("cellrb", parent=CELLR, fontName="Helvetica-Bold")


def _control(rows):
    rows = [[Paragraph(a, CELLB), Paragraph(b, CELL)] for a, b in rows]
    t = Table(rows, colWidths=[38 * mm, 132 * mm])
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", 8.2), ("FONT", (0, 0), (0, -1), "Helvetica-Bold", 8.2),
                           ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#999999")),
                           ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#EEF2F6")), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return t


def _footer(canv, doc_):
    canv.saveState()
    canv.setFont("Helvetica", 7.5)
    canv.setFillColor(colors.HexColor("#666666"))
    canv.drawString(20 * mm, 10 * mm, "Quandong Imaging Group  |  Internal  |  Uncontrolled when printed")
    canv.drawRightString(190 * mm, 10 * mm, "Page %d" % doc_.page)
    canv.restoreState()


# --------------------------------------------------------------------------- the migration standard
def migration_standard(path):
    doc = _doc(path, "Fixed asset migration standard", "Quandong Imaging Group")
    s = [Paragraph("Fixed Asset Migration Standard", H1),
         _control([["Document", "FIN-STD-014"], ["Version", "1.3"], ["Owner", "Group Financial Controller"],
                   ["Approved", "Timothy Hill, Chief Financial Officer, 28 April 2026"], ["Effective", "1 May 2026"],
                   ["Related", "FIN-PRO-022 Asset Verification Procedure; FIN-SPEC-009 Load File Specification; FIN-POL-006 Property, Plant and Equipment Policy"]]),
         Spacer(1, 6),
         Paragraph("1. Purpose and scope", H2),
         Paragraph("This standard sets how the fixed asset register of a practice the group has acquired is moved onto the group ledger. "
                   "Bremer Radiology and Strzelecki Imaging migrated on 1 July 2026. Yacaaba Radiology migrates on 1 January 2027, "
                   "its last legacy month being December 2026.", BODY),
         Paragraph("2. What loads", H2),
         Paragraph("Every capitalised asset in use on the practice register exported for the migration, reconciled at cost to the practice "
                   "ledger. Items carried on a register for tracking that were never capitalised do not load. Assets not sighted at the "
                   "pre-cutover verification are dealt with under FIN-PRO-022. Purchases and disposals after the register export are "
                   "processed on the group ledger after cutover and are not part of the load.", BODY),
         Paragraph("3. Asset balances and lives", H2),
         Paragraph("Each asset loads at its legacy cost and at the accumulated depreciation the practice ledger will hold for it at the close "
                   "of the last legacy month, and the group ledger continues it over the remaining life the practice ledger was depreciating "
                   "it over. Migrated assets keep their legacy method and conventions. FIN-POL-006 applies to assets the group acquires "
                   "after cutover.", BODY),
         Paragraph("4. Rebuilt schedules", H2),
         Paragraph("Where a practice ledger keeps no depreciation record by asset, Finance Systems rebuilds the asset schedules from the "
                   "register and the ledger. A rebuild is accepted only if, run on the practice ledger's own conventions, it reproduces "
                   "every depreciation posting the ledger made from July 2025 to September 2026, account by account and month by month, "
                   "to the cent. An account that does not reproduce does not load.", BODY),
         Paragraph("5. Balances of record", H2),
         Paragraph("The load reconciles to the practice's balances in the last trial balance run before its September 2026 period is "
                   "locked.", BODY),
         Paragraph("6. Depreciation after cutover", H2),
         Paragraph("The group ledger depreciates each loaded asset straight line from its loaded net book value, less any residual value, "
                   "over its loaded remaining life in whole months. A full month is charged in the month of cutover and nothing once the "
                   "remaining life has run out. Monthly amounts are rounded to the cent and the last month takes the remainder.", BODY),
         Paragraph("7. Sign-off", H2),
         Paragraph("Internal Audit re-performs the rebuild and the reconciliations and signs the migration off before the go/no-go meeting. "
                   "The Chief Financial Officer approves cutover.", BODY),
         Spacer(1, 10),
         Paragraph("Version 1.3 (April 2026): section 4 added after the Strzelecki rebuild; section 5 clarified.", SMALL)]
    doc.build(s, onFirstPage=_footer, onLaterPages=_footer)


# --------------------------------------------------------------------------- verification procedure
def verification_procedure(path):
    doc = _doc(path, "Asset verification procedure", "Quandong Imaging Group")
    s = [Paragraph("Asset Verification Procedure", H1),
         _control([["Document", "FIN-PRO-022"], ["Version", "2.1"], ["Owner", "Finance Systems Lead"],
                   ["Effective", "1 August 2026"], ["Applies to", "Pre-cutover verification of practice registers"]]),
         Spacer(1, 6),
         Paragraph("1. Count window", H2),
         Paragraph("Finance Systems sets the count window for each practice. A sighting counts only if it is recorded inside the window, "
                   "before 5:00 pm local time on its last day. For Yacaaba Radiology the window is Monday 28 September to Friday 9 October "
                   "2026. Handheld scanners record the time of each scan in UTC.", BODY),
         Paragraph("2. Scanning", H2),
         Paragraph("Scan the asset tag, or scan or key the manufacturer's serial number from the rating plate. A scan of the serial "
                   "number is a valid sighting of the asset that carries it.", BODY),
         Paragraph("3. Count sheets", H2),
         Paragraph("Where a handheld is not available, the site supervisor counts against the printed count sheet for the site, ticks each "
                   "tag sighted, writes in any tagged asset found on site that is not on the sheet, signs and dates the sheet and sends a "
                   "scan of it to Finance Systems on the day. A signed count sheet is a record of sighting.", BODY),
         Paragraph("4. Items without a tag", H2),
         Paragraph("Software, licences and components installed in a system carry no tag and are not counted. They load as the register "
                   "records them.", BODY),
         Paragraph("5. Site of record", H2),
         Paragraph("An asset sighted at a site other than the one the register shows takes the site where it was sighted as its site of "
                   "record.", BODY),
         Paragraph("6. Assets not sighted", H2),
         Paragraph("An asset not sighted by the cut-off that will carry nil book value at cutover is written off on the last legacy day and "
                   "does not load. Any other asset not sighted loads and is listed for investigation in the first month after cutover.", BODY),
         Paragraph("7. Records", H2),
         Paragraph("The handheld export, the count sheets and the exception list are kept on the migration file.", BODY)]
    doc.build(s, onFirstPage=_footer, onLaterPages=_footer)


# --------------------------------------------------------------------------- FY2025 accounts extract
PPE_CATS = ["Medical imaging equipment", "Ultrasound", "Computer equipment", "Leasehold improvements", "Furniture & fittings", "Motor vehicles"]


def ppe_note(w, eng, year):
    """Note 9's figures for the year ended 30 June `year`, by class: cost, accumulated depreciation and
    impairment, and the depreciation charged in the year (assets disposed during the year included)."""
    def cls(a):
        return "Medical imaging equipment" if a["category"] in ("Medical imaging equipment", "Equipment upgrades", "Options & accessories") else a["category"]
    cost, acc, dep = {c: Z for c in PPE_CATS}, {c: Z for c in PPE_CATS}, {c: Z for c in PPE_CATS}
    y0, y1 = L.mi(year - 1, 7), L.mi(year, 6)
    for a in w.ledger_assets():
        if L.mdate(a["acquired"]) > y1:
            continue
        s = eng.schedule(a)
        if a["disposed"] and L.mdate(a["disposed"]) <= y1:
            if L.mdate(a["disposed"]) >= y0:
                dep[cls(a)] += sum((x for m, x in s.items() if y0 <= m <= y1), Z)
            continue
        c = cls(a)
        cost[c] += a["cost"]
        acc[c] += eng.accumulated(a, y1)
        dep[c] += sum((x for m, x in s.items() if y0 <= m <= y1), Z)
    return dict(cost=cost, acc=acc, dep=dep)


def fy2025_extract(path, w, eng):
    cats = PPE_CATS
    label = {"Medical imaging equipment": "Medical imaging equipment (incl. upgrades, options and accessories)"}
    years = {y: ppe_note(w, eng, y) for y in (2025, 2024)}

    def f(x):
        return "{:,.0f}".format(x)
    doc = _doc(path, "Yacaaba Radiology Pty Ltd - financial report 30 June 2025 (extract)", "Wright Accounting Partners")
    P, PR, PB, PRB = (lambda x: Paragraph(x, CELL)), (lambda x: Paragraph(x, CELLR)), (lambda x: Paragraph(x, CELLB)), (lambda x: Paragraph(x, CELLRB))

    def table(y):
        cost, acc, dep = years[y]["cost"], years[y]["acc"], years[y]["dep"]
        rows = [[PB(str(y)), PRB("Cost<br/>$"), PRB("Accumulated depreciation and impairment<br/>$"), PRB("Carrying amount<br/>$"),
                 PRB("Depreciation for the year<br/>$")]]
        for c in cats:
            rows.append([P(label.get(c, c)), PR(f(cost[c])), PR(f(acc[c])), PR(f(cost[c] - acc[c])), PR(f(dep[c]))])
        rows.append([PB("Total"), PRB(f(sum(cost.values()))), PRB(f(sum(acc.values()))), PRB(f(sum(cost.values()) - sum(acc.values()))),
                     PRB(f(sum(dep.values())))])
        t = Table(rows, colWidths=[58 * mm, 25 * mm, 33 * mm, 26 * mm, 28 * mm])
        t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.5, colors.black), ("LINEABOVE", (0, -1), (-1, -1), 0.5, colors.black),
                               ("VALIGN", (0, 0), (-1, -1), "BOTTOM"), ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]))
        return t
    t, t24 = table(2025), table(2024)
    s = [Paragraph("Yacaaba Radiology Pty Ltd", H1),
         Paragraph("ABN 41 612 087 355", SMALL),
         Paragraph("Special purpose financial report for the year ended 30 June 2025 (extract: notes 1(d), 1(e) and 9)", BODY),
         Spacer(1, 6),
         Paragraph("Note 1(d) Property, plant and equipment", H2),
         Paragraph("Property, plant and equipment is measured at cost less accumulated depreciation and impairment. Items costing less "
                   "than $1,500 (ex GST) are expensed when bought. Depreciation is charged straight line, a full month in the month of "
                   "purchase, at the following rates: medical imaging equipment 10%; options and accessories 20%; ultrasound 16.67%; "
                   "computer equipment 33.33%; leasehold improvements 6.67%; furniture and fittings 10%; motor vehicles 16.67%.", BODY),
         Paragraph("Note 1(e) Change in accounting estimate", H2),
         Paragraph("The directors reviewed the useful life of computer equipment in June 2025. From 1 July 2025 computer equipment is "
                   "depreciated over four years rather than three. The change is applied prospectively from that date.", BODY),
         Paragraph("Note 9 Property, plant and equipment", H2),
         t, Spacer(1, 8),
         t24, Spacer(1, 5),
         Paragraph("Impairment: in June 2025 the OPG/CBCT unit at Cessnock suffered a tube failure that the manufacturer will not repair "
                   "under contract. An impairment loss of $38,000 was recognised in medical imaging equipment and the unit's remaining "
                   "carrying amount is depreciated over its remaining useful life.", BODY),
         Spacer(1, 10),
         Paragraph("Prepared by Wright Accounting Partners, Newcastle. Signed for the directors 26 September 2025.", SMALL)]
    doc.build(s, onFirstPage=_footer_hcr, onLaterPages=_footer_hcr)
    return years


def _footer_hcr(canv, doc_):
    canv.saveState()
    canv.setFont("Helvetica", 7.5)
    canv.setFillColor(colors.HexColor("#666666"))
    canv.drawString(20 * mm, 10 * mm, "Yacaaba Radiology Pty Ltd  |  Financial report 30 June 2025")
    canv.drawRightString(190 * mm, 10 * mm, "%d" % (doc_.page + 11))
    canv.restoreState()


# --------------------------------------------------------------------------- the Raymond Terrace count sheet
def count_sheet(path, w):
    """A printed count sheet, ticked and annotated by hand, scanned. Text is real text (the scanner's
    OCR layer), drawn slightly askew on a grey page."""
    rng = random.Random(7110)
    v = w.verification
    ray = sorted([a for a in w.assets if a["tag"] and a["site"] == "RAY" and a["status"] != "Disposed"], key=lambda a: a["tag"])
    on_sheet = {a["id"] for a, site in v["sheet"]}
    extra = [a for a, site in v["sheet"] if a["site"] != "RAY"]
    c = canvas.Canvas(path, pagesize=A4, invariant=1)
    c.setAuthor("Raymond Terrace")
    c.setTitle("Scan 07102026 1542")
    W_, H_ = A4
    per_page = 34
    pages = [ray[i:i + per_page] for i in range(0, len(ray), per_page)]
    for pno, chunk in enumerate(pages, 1):
        c.setFillColor(colors.HexColor("#F2F0EA"))
        c.rect(0, 0, W_, H_, fill=1, stroke=0)
        c.saveState()
        c.translate(W_ / 2, H_ / 2)
        c.rotate(rng.uniform(-0.7, 0.7))
        c.translate(-W_ / 2, -H_ / 2)
        c.setFillColor(colors.HexColor("#202020"))
        c.setFont("Helvetica-Bold", 11)
        c.drawString(18 * mm, H_ - 18 * mm, "QIG ASSET VERIFICATION - COUNT SHEET")
        c.setFont("Helvetica", 8.5)
        c.drawString(18 * mm, H_ - 24 * mm, "Site: Raymond Terrace (RAY)    Register: Yacaaba Radiology    Printed 25/09/2026")
        c.drawString(18 * mm, H_ - 29 * mm, "Tick each tag sighted. Write in any tagged item found on site that is not listed. Sign and date.")
        y = H_ - 38 * mm
        c.setFont("Helvetica-Bold", 8)
        for x, t in ((18, "Tag"), (36, "Asset No"), (54, "Description"), (150, "Sighted"), (166, "Comment")):
            c.drawString(x * mm, y, t)
        c.line(18 * mm, y - 1.5 * mm, 192 * mm, y - 1.5 * mm)
        y -= 6 * mm
        c.setFont("Helvetica", 8)
        for a in chunk:
            c.setFillColor(colors.HexColor("#202020"))
            c.drawString(18 * mm, y, a["tag"])
            c.drawString(36 * mm, y, a["id"])
            c.drawString(54 * mm, y, a["description"][:58])
            c.rect(152 * mm, y - 1 * mm, 4 * mm, 4 * mm, stroke=1, fill=0)
            if a["id"] in on_sheet:
                c.setFillColor(colors.HexColor("#1F3A93"))
                c.setFont("Helvetica-Oblique", 10)
                c.drawString(152.6 * mm + rng.uniform(-0.4, 0.4) * mm, y - 0.4 * mm, "v")
                c.setFont("Helvetica", 8)
            else:
                c.setFillColor(colors.HexColor("#1F3A93"))
                c.setFont("Helvetica-Oblique", 8.5)
                c.drawString(166 * mm, y, rng.choice(["not found", "not sighted", "?? not here"]))
                c.setFont("Helvetica", 8)
            y -= 6.2 * mm
        if pno == len(pages):
            y -= 4 * mm
            c.setFillColor(colors.HexColor("#1F3A93"))
            c.setFont("Helvetica-Oblique", 9)
            c.drawString(18 * mm, y, "Also found on site, not on sheet:")
            y -= 6 * mm
            for a in extra:
                c.drawString(22 * mm, y, "%s  %s  (sticker says %s)" % (a["tag"], a["description"].split(" - ")[0], SITES[a["site"]]))
                y -= 6 * mm
            y -= 6 * mm
            c.drawString(18 * mm, y, "Handheld HH-09 dead since Tues 30/9 (screen), counted on paper.")
            y -= 10 * mm
            c.drawString(18 * mm, y, "Counted by: K. White (Site Supervisor)      Signed: K White      Date: 7/10/26")
        c.restoreState()
        c.setFont("Helvetica", 6.5)
        c.setFillColor(colors.HexColor("#777777"))
        c.drawString(10 * mm, 6 * mm, "RAY-MFD scan 07/10/2026 15:42  page %d/%d" % (pno, len(pages)))
        c.showPage()
    c.save()


# --------------------------------------------------------------------------- the thread
def thread(path):
    txt = """From: Ronald Lawrence <ronald.lawrence@quandongimaging.com.au>
To: Timothy Hill <timothy.hill@quandongimaging.com.au>
Cc: Cynthia Rice <cynthia.rice@quandongimaging.com.au>, Donna Ramirez <donna.ramirez@yacaabaradiology.com.au>
Subject: RE: Yacaaba cutover - fixed assets
Date: Mon, 12 Oct 2026 08:47:31 +1100
Message-ID: <a71f3c2e.4410@quandongimaging.com.au>
In-Reply-To: <b2c9d8e1.3982@quandongimaging.com.au>
Content-Type: text/plain; charset="utf-8"

Tim,

On track. Where we are:

- Register is the 2 October export from Lorraine's workbook.
- GL detail was pulled on the 3rd. The September TB was run again on the 9th, after her old
  firm posted the joinery reclass the FY26 audit raised, and the period was locked that evening.
- Scans are in for Charlestown, Maitland and Cessnock. Raymond Terrace counted on paper, see
  Donna below.

I've rebuilt Yacaaba's schedules off the register and the rates tab the same way we did Bremer,
and I'd like Internal Audit to re-perform before we commit the load.

Ron

> From: Timothy Hill
> Sent: Sunday, 11 October 2026 7:12 PM
> Subject: RE: Yacaaba cutover - fixed assets
>
> Ron, Cynthia - I need the Yacaaba depreciation for January to June in the reforecast pack and
> IA's sign-off in my hands before the go/no-go on 4 November. Where are we?
>
> Tim

> From: Donna Ramirez
> Sent: Friday, 9 October 2026 5:58 PM
> Subject: RE: Yacaaba cutover - fixed assets
>
> Hi Ron, Kylie counted Raymond Terrace on the sheet on Wednesday because the handheld screen
> went on the 30th. She scanned it to the finance systems folder. A few of the ultrasound and
> IT bits have moved between sites since the Cessnock room opened, so the scans will show
> things in places the register doesn't. Last of Maitland went through this arvo.
>
> Donna

> From: Lorraine Wright
> Sent: Monday, 5 October 2026 10:20 AM
> Subject: RE: Yacaaba cutover - fixed assets
>
> Hi Ron,
>
> The register workbook is Yacaaba's record and you now have it, rates tab included. The
> monthly depreciation workings are our working papers and stay with the firm under the
> engagement terms, as discussed with Tim when the group took Yacaaba on. Happy to answer
> questions in writing.
>
> Kind regards
> Lorraine Wright
> Wright Accounting Partners, Newcastle

--
Ronald Lawrence | Finance Systems Lead | Quandong Imaging Group
This email is confidential to the group.
"""
    with open(path, "w", encoding="utf-8", newline="\r\n") as fh:
        fh.write(txt)


# --------------------------------------------------------------------------- extract notes (the dictionary)
def extract_notes(path, n_gl, n_reg, n_appr, n_scan, n_brm):
    txt = """# Yacaaba extract notes

Finance Systems, Quandong Imaging Group. Migration file for Yacaaba Radiology (cutover 1 January 2027).
Last updated 13/10/2026 (R. Lawrence).

## Files

| File | What it is | Pulled |
|---|---|---|
| YCB_asset_register_2026-10-02.xlsx | Yacaaba's register workbook as kept by Wright Accounting Partners: Register and Rates tabs, %d register lines | 02/10/2026 |
| YCB_GL_detail_2025-07_to_2026-09.csv | Yacaaba general ledger, every line posted 1 July 2025 to 30 September 2026, %d lines | 03/10/2026 |
| YCB_trial_balance_30-09-2026.xlsx | Trial balance at 30/09/2026, both runs | 03/10/2026 and 09/10/2026 |
| YCB_FY2025_financial_statements_extract.pdf | Notes 1(d), 1(e) and 9 of the FY2025 report | received 05/10/2026 |
| YCB_capital_approvals_2018-2026.csv | Yacaaba's capital request log to February 2024 combined with QIG capex system requests since, %d requests | 06/10/2026 |
| verification_scans_YCB_2026.csv | Handheld export for the Yacaaba count, %d scans | 10/10/2026 |
| RAY_count_sheet_07-10-2026.pdf | Raymond Terrace count sheet, scanned | 07/10/2026 |
| BRM_load_2026-07-01.csv | Bremer's load file as loaded on 1 July 2026, %d rows | 01/07/2026 |
| group_asset_class_mapping.xlsx | Group Asset Class Mapping, all versions | 01/10/2026 |
| fa_load_specification.xlsx | FIN-SPEC-009 | |
| fa_migration_standard.pdf | FIN-STD-014 | |
| asset_verification_procedure.pdf | FIN-PRO-022 | |
| RE_Yacaaba_cutover.eml | Email thread on the cutover, 5 to 12 October | 12/10/2026 |

## Register (Register tab)

One line per register entry. Asset No is the workbook's own number. Tag is the barcode label (H + five digits); components and
software installed in a system have none. Site is the site the workbook shows. Date Acquired and Cost (ex GST) are as invoiced.
Approval Ref links to the capital approvals file where the item went through a request. Capitalised is Y for items carried in
the ledger and N for items under the threshold kept on the workbook for the insurer. Status is In use or Disposed.

## GL detail

One line per journal line. Src: OB opening balances at 1 July 2025, BIL daily billing summaries, CR receipts, CD payments,
PJ purchases, PY payroll, GJ general journals (month-end depreciation, accruals, disposals, intercompany). Job is the site
code where the line was coded to a site. Debit and Credit are in dollars and cents. Lines posted after the pull are not in
this file.

## Trial balance

Two runs of the same report. The second includes journals posted after the first into September.

## Capital approvals

One row per request. Existing Asset is the register Asset No of the equipment a replacement request retires, where it names
one. Approved Amount is the approval, not the invoice. Date Completed is when the item was received.

## Scans

One row per scan. scan_id is the handheld's own running number. site_code is where the handheld was. scanned_at_utc is
the handheld clock in UTC. tag or serial is what was
read; serial is filled when the tag was unreadable or the operator keyed the rating plate. Tags starting Q belong to group
loan stock, not to Yacaaba.
""" % (n_reg, n_gl, n_appr, n_scan, n_brm)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(txt)


def sources(path, counts):
    txt = """SOURCES AND LICENCES: Yacaaba Radiology migration file

This folder was compiled by Finance Systems, Quandong Imaging Group on 13 October 2026 and is released under CC BY 4.0.
Places, public holidays, the 2026 start of daylight saving in New South Wales (Sunday 4 October), equipment model names and
supplier names are real and are used descriptively; no supplier's records are reproduced.

YCB_asset_register_2026-10-02.xlsx: practice register workbook (%(reg)d register lines) and rate card
YCB_GL_detail_2025-07_to_2026-09.csv: practice general ledger detail (%(gl)d lines)
YCB_trial_balance_30-09-2026.xlsx: practice trial balance at 30 September 2026, two runs
YCB_FY2025_financial_statements_extract.pdf: notes extract from the practice's FY2025 report
YCB_capital_approvals_2018-2026.csv: capital request log (%(appr)d requests)
verification_scans_YCB_2026.csv: handheld scan export (%(scan)d scans)
RAY_count_sheet_07-10-2026.pdf: paper count sheet, scanned
BRM_load_2026-07-01.csv: precedent load file (%(brm)d rows)
group_asset_class_mapping.xlsx: group class mapping, three versions
fa_load_specification.xlsx: load file specification
fa_migration_standard.pdf: migration standard
asset_verification_procedure.pdf: verification procedure
RE_Yacaaba_cutover.eml: email thread
YCB_extract_notes.md: field notes for the files above
""" % counts
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(txt)
