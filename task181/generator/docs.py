"""The pack's documents and workbooks: the Centre's published rates, its outlier notice and response guide, the
CSSD set register and equipment log."""
import datetime as dt
import re

import openpyxl
from openpyxl.styles import Font
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import common as C

ST = {
    "h1": ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=13, leading=16, spaceAfter=4),
    "h2": ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=10.5, leading=13, spaceBefore=8, spaceAfter=3),
    "p": ParagraphStyle("p", fontName="Helvetica", fontSize=9.5, leading=12.5, spaceAfter=4),
    "small": ParagraphStyle("small", fontName="Helvetica", fontSize=8, leading=10, textColor=colors.HexColor("#444444")),
    "cell": ParagraphStyle("cell", fontName="Helvetica", fontSize=8.6, leading=10.6),
}
CENTRE = "Healthcare-Associated Infection Surveillance Centre"


def _pdf(path, story, title, author, created, modified=None):
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm,
                            bottomMargin=18 * mm, title=title, author=author, subject="", creator=author,
                            producer=author, invariant=1)
    doc.build(story)
    data = open(path, "rb").read()
    data = re.sub(rb"/CreationDate \(D:[^)]*\)", b"/CreationDate (" + created.encode() + b")", data)
    data = re.sub(rb"/ModDate \(D:[^)]*\)", b"/ModDate (" + (modified or created).encode() + b")", data)
    open(path, "wb").write(data)
    C.scrub_pdf(path)
    C.set_mtime(path)


def _table(rows, widths, head=True):
    t = Table([[Paragraph(str(c), ST["cell"]) for c in r] for r in rows], colWidths=[w * mm for w in widths])
    style = [("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#999999")), ("VALIGN", (0, 0), (-1, -1), "TOP")]
    if head:
        style.append(("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8edf2")))
    t.setStyle(TableStyle(style))
    return t


def rates_pdf(path):
    s = [Paragraph("Surgical site infection surveillance: procedure rates 2026", ST["h1"]),
         Paragraph("%s, Annual Report 2026, Table 7. Published 14 April 2027." % CENTRE, ST["small"]),
         Spacer(1, 6),
         Paragraph("Each surveilled procedure is assigned a risk index of 0 to 3: one point for an ASA class of 3 or "
                   "more, one point for a wound class of contaminated or dirty, and one point for an operation whose "
                   "duration, from incision to closure, exceeds the category's cut-point. The rates below are "
                   "surgical site infections per 100 procedures in the state's 2022 to 2026 surveillance, all "
                   "contributing hospitals pooled.", ST["p"])]
    rows = [["Category", "Procedures", "Cut-point (minutes)", "Index 0", "Index 1", "Index 2", "Index 3"]]
    for k in C.PROCS:
        rows.append([k, C.PROC_NAME[k], C.CUT_MIN[k]] + ["%.1f" % v for v in C.RATES[k]])
    s.append(_table(rows, [20, 46, 26, 17, 17, 17, 17]))
    s.append(Spacer(1, 6))
    s.append(Paragraph("Notes. A procedure exactly at the cut-point takes no duration point. Index 3 is reported for "
                       "every category; where fewer than 200 state procedures carried index 3 the 2 and 3 strata "
                       "were pooled before the rate was set. Rates are reviewed each April.", ST["small"]))
    _pdf(path, s, "HAISC Annual Report 2026 Table 7", CENTRE, "D:20270414093000+10'00'")


def guide_pdf(path):
    s = [Paragraph("Responding to an outlier notice: guide for health services", ST["h1"]),
         Paragraph("%s. Edition 3, effective 1 February 2027." % CENTRE, ST["small"]),
         Spacer(1, 4),
         Paragraph("1. When a notice is sent", ST["h2"]),
         Paragraph("The Centre sends an outlier notice when a health service's surveilled procedures in a quarter "
                   "carry more surgical site infections than the upper control limit for the number the Centre's "
                   "rates expect. The notice names the period the service is to review and the date its response "
                   "is due.", ST["p"]),
         Paragraph("2. What the response contains", ST["h2"]),
         Paragraph("The response names the consultants whose own practice raised their patients' risk of a "
                   "surgical site infection above the upper control limit over the period under review, so that "
                   "the service's professional practice review can take them, or states that there are none. It "
                   "also states any cause the service has found outside the consultants' practice and what the "
                   "service has done about it.", ST["p"]),
         Paragraph("3. What the Centre counts", ST["h2"]),
         Paragraph("A procedure is an operation through an incision in a surveilled category, counted once, in the "
                   "category of its principal procedure. A return to theatre for a complication of an earlier "
                   "procedure is not a new procedure. A procedure belongs to the consultant the theatre record holds "
                   "responsible for it.", ST["p"]),
         Paragraph("A surgical site infection counts when it meets the Centre's definition within 30 days of its "
                   "procedure, or within 90 days where an implant was placed, and it is counted once for its "
                   "procedure, at the deepest level it reached: superficial incisional, deep incisional or "
                   "organ/space.", ST["p"]),
         Paragraph("4. Expected infections and the control limit", ST["h2"]),
         Paragraph("A procedure's expected infection is the Centre's published rate for its category and risk index, "
                   "and a set of procedures expects the sum. The upper control limit for an expected number is the "
                   "97.5th centile of a Poisson count with that mean; infections above it are above the limit.",
                   ST["p"]),
         Spacer(1, 8),
         _table([["Contact", "Surveillance Coordinator, %s" % CENTRE]], [30, 130], head=False)]
    _pdf(path, s, "HAISC outlier response guide", CENTRE, "D:20270118110000+11'00'", "D:20270201090000+11'00'")


def notice_pdf(path, T):
    win = [o for o in T["ops"] if dt.date(2027, 4, 1) <= o["start"].date() <= dt.date(2027, 6, 30)]
    inf = {i["op"] for i in T["inf"]}
    exp_n = sum(C.expected_rate(o["proc"], o["idx"]) for o in win)
    obs = sum(o["id"] in inf for o in win)
    lim = C.poisson_upper(exp_n)
    s = [Paragraph("Outlier notice: Kooralong Hospital, general surgery", ST["h1"]),
         Paragraph("%s. Issued 18 October 2027. Reference HAISC/ON/2027/031." % CENTRE, ST["small"]),
         Spacer(1, 6),
         Paragraph("To the Chief Executive, Kooralong Health.", ST["p"]),
         Paragraph("The general surgery procedures Kooralong Hospital submitted for the second quarter of 2027 "
                   "carried %d surgical site infections against %.1f expected from the Centre's rates, above the "
                   "upper control limit of %d. The Centre asks the health service to review its general surgery "
                   "procedures from 1 April to 30 September 2027, once each procedure's surveillance period has "
                   "closed, and to respond under the Centre's outlier response guide by 31 January 2028."
                   % (obs, exp_n, lim), ST["p"]),
         Paragraph("The quarter's figures are as the hospital submitted them by 30 September 2027; infections "
                   "recorded after that date are not in them.", ST["small"])]
    _pdf(path, s, "HAISC outlier notice HAISC/ON/2027/031", CENTRE, "D:20271018143000+11'00'")
    return obs, exp_n, lim


def _xlsx(path, sheets, creator, created, modified):
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    for title, rows, bold in sheets:
        ws = wb.create_sheet(title)
        for r in rows:
            ws.append(list(r))
        for i in bold:
            for c in ws[i]:
                c.font = Font(bold=True)
        for col, width in zip("ABCDEFGH", (14, 34, 16, 18, 11, 14, 14, 30)):
            ws.column_dimensions[col].width = width
    wb.properties.creator = creator
    wb.properties.lastModifiedBy = creator
    wb.save(path)
    C.normalise_zip(path, created, modified)


def set_register(path, inst):
    rows = [("Kooralong Hospital CSSD: instrument set register (general surgery)", "", "", "", "", "", "", ""),
            ("Exported 4 January 2028", "", "", "", "", "", "", ""),
            ("Barcode", "Set name", "Owner", "Container", "Weight kg", "Commissioned", "Status", "Notes")]
    items = []
    for c, pool in inst["trays"].items():
        items += pool
    for g, pool in inst["sets"].items():
        items += pool
    r = C.rng("register")
    for it in sorted(items, key=lambda x: x["barcode"]):
        comm = dt.date(2019, 1, 1) + dt.timedelta(days=int(r.integers(0, 2200)))
        owner = it["owner"] or ("Emergency theatre" if it["name"].startswith("Emergency") else "General surgery")
        rows.append((it["barcode"], it["name"], owner, it["container"], it["kg"], comm.isoformat(), "In service", ""))
    _xlsx(path, [("Register", rows, [3])], "Kooralong Health CSSD", "2025-02-11T08:15:00Z", "2028-01-03T22:40:00Z")


def equipment_log(path):
    rows = [("Kooralong Hospital CSSD: equipment maintenance log", "", "", "", "", ""),
            ("Equipment", "Date", "Work order", "Work done", "Returned to service", "Engineer")]
    ev = [("S1", "2026-03-09", "Annual revalidation (thermometric and load tests)"),
          ("S2", "2026-03-10", "Annual revalidation (thermometric and load tests)"),
          ("S3", "2026-03-11", "Annual revalidation (thermometric and load tests)"),
          ("S4", "2026-03-12", "Annual revalidation (thermometric and load tests)"),
          ("WD2", "2026-05-20", "Spray arm bearing replaced"),
          ("S2", "2026-08-04", "Door seal replaced"),
          ("S1", "2026-11-16", "Steam trap replaced"),
          ("WD1", "2027-01-27", "Dosing pump serviced"),
          ("S1", "2027-03-08", "Annual revalidation (thermometric and load tests)"),
          ("S2", "2027-03-09", "Annual revalidation (thermometric and load tests)"),
          ("S3", "2027-03-10", "Annual revalidation (thermometric and load tests)"),
          ("S4", "2027-03-11", "Annual revalidation (thermometric and load tests)"),
          ("S3", "2027-05-12", "Vacuum pump replaced after a pump failure on the night shift; controller board "
                               "replaced; Bowie-Dick test and a validation load passed"),
          ("WD3", "2027-06-22", "Chamber door switch replaced"),
          ("S4", "2027-08-17", "Door seal replaced"),
          ("S2", "2027-09-28", "Printer replaced")]
    # the hospital's work orders run on through every department's jobs, so the CSSD's numbers climb unevenly with
    # the calendar; each job is back in service when its engineer signs it off
    back_at = ["15:25", "16:05", "15:50", "16:40", "11:35", "13:20", "10:15", "12:50", "15:40", "16:20", "15:05",
               "16:55", "14:40", "09:45", "13:55", "11:10"]
    spread = [0, 3, 11, 2, 9, 5, 14, 7, 1, 12, 4, 8, 6, 13, 10, 15]
    wo, prev = 31240, None
    for k, (eq, d, work) in enumerate(ev):
        back = "%s %s" % (d, back_at[k])
        day = dt.date.fromisoformat(d)
        if prev is not None:
            wo += max(2, round((day - prev).days * 4.6)) + spread[k]
        prev = day
        rows.append((eq, d, "WO-%05d" % wo, work, back, "Medsteril Service"))
    _xlsx(path, [("Log", rows, [2])], "Kooralong Health CSSD", "2026-01-06T22:15:00Z", "2027-09-29T05:55:00Z")
