"""The pack's documents: the Cell Capacity Standard CS-3, the capacity memo, the hardware plan, the technology budgets
with the freeze, the 2026 Q3 capacity report, the MAD1 operations log, the hardware inventory, the chargeback policy,
the data dictionary, the files note, the MAD1 cells' quarterly summary and the ML Platform's H1 2027 demand note."""
from __future__ import annotations

import datetime as dt
import math

import numpy as np
import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                      # noqa: E402
from reportlab.lib.pagesizes import A4                                                # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                       # noqa: E402
from reportlab.lib.units import cm                                                    # noqa: E402
from reportlab.pdfbase import pdfmetrics                                              # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                          # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import common as K   # noqa: E402
import records as R  # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/"
for _n, _f in (("Carlito", "crosextra/Carlito-Regular.ttf"), ("Carlito-Bold", "crosextra/Carlito-Bold.ttf"),
               ("Carlito-Italic", "crosextra/Carlito-Italic.ttf"),
               ("LiberationSerif", "liberation/LiberationSerif-Regular.ttf"),
               ("LiberationSerif-Bold", "liberation/LiberationSerif-Bold.ttf")):
    pdfmetrics.registerFont(TTFont(_n, FONT_DIR + _f))
SANS, SANS_B, SANS_I = "Carlito", "Carlito-Bold", "Carlito-Italic"
SERIF, SERIF_B = "LiberationSerif", "LiberationSerif-Bold"
INK = colors.HexColor("#1d2330")
GREY = colors.HexColor("#5a6270")
BLUE = colors.HexColor("#1f4e79")
RULE = colors.HexColor("#a7b0bd")
PALE = colors.HexColor("#e8edf3")

BODY = ParagraphStyle("body", fontName=SANS, fontSize=10.2, leading=13.4, textColor=INK, spaceAfter=5)
CLAUSE = ParagraphStyle("clause", parent=BODY, leftIndent=26, firstLineIndent=-26)
H1 = ParagraphStyle("h1", fontName=SANS_B, fontSize=15.5, leading=19, textColor=BLUE, spaceAfter=3)
H1S = ParagraphStyle("h1s", fontName=SANS, fontSize=9.8, leading=12.8, textColor=GREY, spaceAfter=9)
H2 = ParagraphStyle("h2", fontName=SANS_B, fontSize=11.2, leading=14, textColor=INK, spaceBefore=8, spaceAfter=3)
NOTE = ParagraphStyle("note", fontName=SANS_I, fontSize=8.6, leading=11, textColor=GREY, spaceBefore=4)
CELL = ParagraphStyle("cell", fontName=SANS, fontSize=8.9, leading=10.8, textColor=INK)
CELLB = ParagraphStyle("cellb", fontName=SANS_B, fontSize=8.9, leading=10.8, textColor=INK)


def n0(x):
    return "{:,}".format(int(round(x)))


def n1(x):
    return "{:,.1f}".format(x)


def _footer(left, right):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFont(SANS, 7.8)
        canvas.setFillColor(GREY)
        canvas.drawString(2.0 * cm, 1.2 * cm, left)
        canvas.drawRightString(A4[0] - 2.0 * cm, 1.2 * cm, "%s  |  page %d" % (right, doc.page))
        canvas.restoreState()
    return draw


def _doc(path, title, author):
    return SimpleDocTemplate(path, pagesize=A4, leftMargin=2.2 * cm, rightMargin=2.2 * cm, topMargin=1.9 * cm,
                             bottomMargin=2.0 * cm, title=title, author=author, subject="", creator="", producer="")


def _table(rows, widths, head=True, right_from=1):
    data = [[Paragraph(str(c), CELLB if (head and i == 0) else CELL) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths, hAlign="LEFT")
    st = [("GRID", (0, 0), (-1, -1), 0.4, RULE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
          ("TOPPADDING", (0, 0), (-1, -1), 2.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5)]
    if head:
        st.append(("BACKGROUND", (0, 0), (-1, 0), PALE))
    t.setStyle(TableStyle(st))
    return t


# ---------------------------------------------------------------------------------------------------- CS-3

def write_standard(path):
    s = [Paragraph("%s  |  Infrastructure" % K.COMPANY, H1S), Paragraph("Cell Capacity Standard CS-3", H1),
         Paragraph("Quarterly capacity reviews of the compute cells at MAD1 (Alcobendas) and BCN2 (Barcelona). Revision "
                   "of June 2026, replacing the revision of January 2025. Owner: Head of Infrastructure. Approved by "
                   "%s on 22 June 2026." % K.PEOPLE["head"], H1S)]

    def sec(title, clauses):
        s.append(Paragraph(title, H2))
        for no, text in clauses:
            s.append(Paragraph("%s&nbsp;&nbsp;&nbsp;%s" % (no, text), CLAUSE))

    sec("1 Scope", [
        ("1.1", "This standard sets how the cores of each compute cell are reserved for a quarter: to the cell's firm "
                "tenants, to the platform services that run the cell, and to the batch training tier."),
        ("1.2", "Quarters are calendar quarters. Times in this standard are UTC."),
        ("1.3", "Each tenant of a cell is of one class: firm (a product service, or a deadline batch class, with a "
                "budget of its own), platform (a service that runs the cell itself) or batch (the batch training "
                "tier). Compute Operations keeps each cell's tenant directory, which gives every tenant's class.")])
    sec("2 Reservable cores", [
        ("2.1", "A cell's reservable cores for a quarter are its machines in service at the start of the quarter, as "
                "the cell's hardware plan gives them, times the cores of each machine, times the overcommit that "
                "Compute Operations sets for the quarter in the cell's capacity memo."),
        ("2.2", "Every reservation, and the batch guarantee, is a number of cores counted against the cell's "
                "reservable cores.")])
    sec("3 Firm tenants", [
        ("3.1", "A firm tenant asks for its reservation for a quarter in the quarter's request window, which Compute "
                "Operations opens six weeks before the quarter and closes on the date in the capacity memo. A firm "
                "tenant that files no request in the window holds no reservation in the cell that quarter."),
        ("3.2", "A firm tenant's reservation for the quarter is its request, held to what its monthly budget pays for "
                "at the rate card's rate for reserved cores at the site in force for the quarter: the largest whole "
                "number of cores whose monthly charge at that rate the monthly budget covers."),
        ("3.3", "A firm tenant's monthly budget is the budget Technology Controlling holds for the tenant's cost "
                "centre for its reserved cores in the cell."),
        ("3.4", "During a quarter a firm tenant may release reserved cores, and released cores may be granted to other "
                "firm tenants, through the cell's capacity desk.")])
    sec("4 Platform services", [
        ("4.1", "Each platform service is reserved for the quarter at the use forecast for its busiest hour of the "
                "quarter."),
        ("4.2", "A tenant's use in an hour is its average cores in use over the hour, as the cell monitoring export "
                "records it.")])
    sec("5 The batch guarantee", [
        ("5.1", "The batch training tier is guaranteed the largest whole thousand of cores that the cell's reservable "
                "cores leave after the firm tenants' reservations and the platform services' reservations."),
        ("5.2", "Batch training runs inside its guarantee: the cell's scheduler admits batch runs while the cores they "
                "hold stay within the guarantee. Reservable cores left after the guarantee are not reserved."),
        ("5.3", "Compute Operations publishes the guarantee to the batch training teams after the review.")])
    sec("6 The review", [
        ("6.1", "Compute Operations holds each cell's capacity review in the last month of the quarter before, after "
                "the request window has closed, and records the quarter's reservations and guarantee in the cell's "
                "reservation ledger."),
        ("6.2", "The review works from the capacity memo, the hardware plan, the requests filed in the window, the "
                "budgets and the rate card, the cell monitoring export and the tenant directory.")])
    s.append(Spacer(1, 8))
    s.append(Paragraph("Revision history: January 2025, first issue for MAD1 and BCN2 cells (replacing the MAD1 cell "
                       "allocation guideline of 2023); June 2026, section 3.4 added and the request window moved to six "
                       "weeks before the quarter.", NOTE))
    foot = _footer("%s Internal." % K.COMPANY, "CS-3 rev. June 2026")
    doc = _doc(path, "Cell Capacity Standard CS-3", K.PEOPLE["head"])
    doc.build(s, onFirstPage=foot, onLaterPages=foot)


# ---------------------------------------------------------------------------------------------------- capacity memo

def write_memo(path, W):
    import docx
    from docx.shared import Pt
    d = docx.Document()
    st = d.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    d.add_heading("Memo", level=1)
    for k, v in (("To", "Compute Operations; Storage Platform; ML Platform; Technology Controlling"),
                 ("From", "%s, Head of Infrastructure" % K.PEOPLE["head"]),
                 ("Date", "9 December 2026"),
                 ("Subject", "C-22: capacity review for the first quarter of 2027")):
        p = d.add_paragraph()
        p.add_run("%s: " % k).bold = True
        p.add_run(v)
    paras = [
        "C-22's review for 2027 Q1 is on Tuesday 15 December at 10:00 in Alcobendas (room 2.14, and on the usual call). "
        "It runs under CS-3, revision of June 2026.",
        "Machines. The December refresh brings 29 racks of Lena R4-96 into C-22, in rows 2L and 2M. The racks were "
        "delivered in November and are in burn-in. Fleet & Hardware will put them in service on 28 December and will "
        "issue the final revision of the C-22 hardware plan before the review; the review takes the machines in "
        "service from the plan.",
        "Overcommit. The overcommit for 2027 Q1 is 1.45 for every MAD1 cell, C-22 included.",
        "Requests. The request window for 2027 Q1 closed on Friday 4 December at 18:00 (Madrid). All eleven firm tenants "
        "of C-22 filed.",
        "Budgets and rates. Technology Controlling's note of 27 November holds every technology cost centre's monthly "
        "budgets for January to March 2027 at their December 2026 levels until the 2027 plan is approved. The rate "
        "card for reserved cores from 1 January 2027 was published on 1 December.",
        "Platform services. Compute Operations prepares the cell-ctl and cell-store reservations. The cell monitoring "
        "export for the review will be pulled on the morning of 14 December.",
        "Batch. The guarantee goes to the six batch training teams after the review. ML Platform's note on batch "
        "demand for the first half of 2027 is in the papers for information.",
        K.PEOPLE["head"],
    ]
    for t in paras:
        d.add_paragraph(t)
    d.core_properties.author = K.PEOPLE["head"]
    d.core_properties.title = "C-22 capacity review 2027 Q1"
    d.save(path)


# ---------------------------------------------------------------------------------------------------- spreadsheets

def _title_rows(ws, title, sub, note=None):
    ws.append([title])
    ws["A1"].font = Font(name="Calibri", bold=True, size=12)
    ws.append([sub])
    ws["A2"].font = Font(name="Calibri", italic=True, size=10, color="595959")
    if note:
        ws.append([note])
        ws.cell(row=ws.max_row, column=1).font = Font(name="Calibri", size=9, color="595959")
    ws.append([])


def _head(ws, cols, widths=None, fill="DCE6F0"):
    ws.append(cols)
    row = ws.max_row
    for c in range(1, len(cols) + 1):
        cell = ws.cell(row=row, column=c)
        cell.font = Font(name="Calibri", bold=True)
        cell.fill = PatternFill("solid", fgColor=fill)
        cell.alignment = Alignment(wrap_text=True, vertical="top")
    if widths:
        for i, w in enumerate(widths, 1):
            ws.column_dimensions[get_column_letter(i)].width = w
    return row


def write_hwplan(path, W):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Racks"
    _title_rows(ws, "C-22 hardware plan, 2027 Q1", "Fleet & Hardware, MAD1. Revision of 11 December 2026 (replaces the "
                "revision of 20 November 2026): the 29 refresh racks in service from 28 December 2026.",
                "One row per rack position in use. Every rack holds 20 machines of 96 cores.")
    hr = _head(ws, ["Rack", "Row", "Position", "Model", "In service from", "Machines"], [9, 7, 9, 13, 15, 10])
    for rk in sorted(W.racks, key=lambda x: (x["row"], x["pos"])):
        ws.append(["%s-%02d" % (rk["row"], rk["pos"]), rk["row"], rk["pos"], rk["model"], rk["in_service"].date(),
                   K.RACK])
        ws.cell(row=ws.max_row, column=5).number_format = "yyyy-mm-dd"
    ws.freeze_panes = ws.cell(row=hr + 1, column=1)
    ws2 = wb.create_sheet("By quarter")
    _title_rows(ws2, "Machines in service at the start of each quarter", "C-22, from the rack plan. 2027 Q1 includes "
                "the refresh racks in service from 28 December 2026.")
    _head(ws2, ["Quarter", "First day", "Racks in service", "Machines in service"], [10, 12, 16, 18])
    for q in K.QUARTERS + [K.NEXT_Q]:
        qs = K.q_start(q)
        n = sum(1 for x in W.racks if x["in_service"] <= qs)
        ws2.append([q, qs.date(), n, n * K.RACK])
        ws2.cell(row=ws2.max_row, column=2).number_format = "yyyy-mm-dd"
    wb.save(path)


BUDGET_OTHER = [  # cost centres' lines for other cells and other resources (EUR a month, December 2026)
    ("4120", "Inventory & Availability", "MAD1 C-24 reserved cores", 151000),
    ("4210", "Booking & Orders", "MAD1 C-21 reserved cores", 287000),
    ("4210", "Booking & Orders", "MAD1 block storage", 41000),
    ("4220", "Payments", "BCN2 C-01 reserved cores", 176500),
    ("4310", "Content & Reviews", "MAD1 block storage", 58500),
    ("4410", "Sponsored Listings", "MAD1 C-23 reserved cores", 71000),
    ("4510", "Partner Connectivity", "BCN2 C-01 reserved cores", 122000),
    ("4520", "Partner Finance Systems", "MAD1 block storage", 12500),
    ("4610", "Data Platform", "MAD1 C-25 reserved cores", 402000),
    ("4610", "Data Platform", "MAD1 block storage", 233000),
    ("4620", "Corporate IT", "BCN2 C-02 reserved cores", 64500),
]


def write_budgets(path, W):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Compute budgets"
    months = ["Jan 2026", "Feb 2026", "Mar 2026", "Apr 2026", "May 2026", "Jun 2026", "Jul 2026", "Aug 2026",
              "Sep 2026", "Oct 2026", "Nov 2026", "Dec 2026", "Jan 2027", "Feb 2027", "Mar 2027"]
    _title_rows(ws, "Technology compute budgets by cost centre, monthly, EUR",
                "Technology Controlling. 2026 as revised in April and October 2026; January to March 2027 held at "
                "December 2026 (budget freeze of 27 November 2026, Freeze sheet).",
                "One line per cost centre and budget line. Budget lines for reserved cores are per cell.")
    hr = _head(ws, ["CC", "Cost centre", "Budget line"] + months, [7, 26, 28] + [11] * 15)
    lines = []
    for t in K.FIRM:
        code, name = K.FIRM_INFO[t]["cc"][3:7], K.FIRM_INFO[t]["cc"][8:]
        b = W.budgets[t]
        lines.append((code, name, "MAD1 C-22 reserved cores", [b[m] for m in range(1, 13)] + [b[12]] * 3))
    r = K.rng("budget-other")
    for code, name, line, dec in BUDGET_OTHER:
        f1, f2 = float(r.uniform(0.94, 0.965)), float(r.uniform(0.968, 0.99))
        v1 = int(math.ceil(dec * f1 / 500.0) * 500)
        v2 = int(math.ceil(dec * f2 / 500.0) * 500)
        lines.append((code, name, line, [v1] * 3 + [v2] * 6 + [dec] * 6))
    for code, name, line, vals in sorted(lines, key=lambda x: (x[0], x[2])):
        ws.append([code, name, line] + vals)
        for c in range(4, 19):
            ws.cell(row=ws.max_row, column=c).number_format = "#,##0"
    ws.freeze_panes = ws.cell(row=hr + 1, column=4)
    ws2 = wb.create_sheet("Freeze")
    _title_rows(ws2, "Budget freeze, January to March 2027", "Technology Controlling.")
    _head(ws2, ["Item", "Record"], [20, 92])
    for k, v in (("Freeze", "TC-FRZ-2027-01"),
                 ("Entered", "27 November 2026, %s" % K.PEOPLE["finance"]),
                 ("Cost centres", "All technology cost centres, every budget line"),
                 ("Months held", "January, February and March 2027"),
                 ("Held at", "December 2026 level, line by line (columns Jan 2027 to Mar 2027 of Compute budgets)"),
                 ("Reason", "2027 technology plan not yet approved (management committee, January 2027)"),
                 ("Lifted", "On approval of the plan; revised lines apply from the month after approval")):
        ws2.append([k, v])
        ws2.cell(row=ws2.max_row, column=2).alignment = Alignment(wrap_text=True, vertical="top")
    wb.save(path)


# ---------------------------------------------------------------------------------------------------- the Q3 capacity report

def q3_report_figures(W):
    """Every figure the 2026 Q3 capacity report quotes, from the hourly values as the export writes them."""
    h0 = int((K.Q3_START - K.EXPORT_START).total_seconds() // 3600)
    h1 = int((K.Q3_END - K.EXPORT_START).total_seconds() // 3600)
    hrs = [h for h in range(h0, h1) if not R.in_gap(W.hours[h])]
    r1 = lambda a: np.array([float("%.1f" % max(0.0, float(x))) for x in a])   # as the export writes them
    ser = {"cell-ctl": r1(W.ctl_h), "cell-store": r1(W.store_h), "batch-train": r1(W.batch_h)}
    firm = sum(r1(W.firm_h[t]) for t in K.FIRM)
    out = {}
    for k, v in list(ser.items()) + [("firm", firm), ("cell", firm + ser["cell-ctl"] + ser["cell-store"] +
                                                          ser["batch-train"])]:
        h = max(hrs, key=lambda x: (v[x], -x))
        out[k] = (float(v[h]), W.hours[h])
    q = "2026Q3"
    F = sum(W.firm_res[t][q] for t in K.FIRM)
    out["reservable"] = W.reservable[q]
    out["firm_res"] = F
    out["ctl_res"], out["store_res"], out["G"] = W.ctl_res[q], W.store_res[q], W.guarantee[q]
    out["unreserved"] = W.reservable[q] - F - W.ctl_res[q] - W.store_res[q] - W.guarantee[q]
    b = ser["batch-train"]
    out["batch_hours_99"] = int(sum(1 for h in hrs if b[h] >= 0.99 * W.guarantee[q]))
    out["hours"] = len(hrs)
    out["hours_q"] = h1 - h0
    return out


def write_capreport(path, W):
    f = q3_report_figures(W)
    q = "2026Q3"
    s = [Paragraph("%s  |  Compute Operations, MAD1" % K.COMPANY, H1S),
         Paragraph("C-22 capacity report, 2026 Q3", H1),
         Paragraph("1 July to 30 September 2026 (UTC). Version 1.0, issued 6 October 2026 by %s. Reservations as "
                   "approved at the review of 16 June 2026, and the cell's use against them." % K.PEOPLE["requester"],
                   H1S)]
    s.append(Paragraph("1 Reservable cores and reservations", H2))
    s.append(Paragraph("C-22 started the quarter with %s machines in service (%d racks) and ended it with %s, three "
                       "racks of Lena R4-96 having gone into service on 14 July, 25 August and 15 September. At the "
                       "quarter's overcommit of 1.45 the reservable cores were %s." % (
                           n0(W.m_start[q]), W.m_start[q] // K.RACK, n0(W.m_end[q]), n0(f["reservable"])), BODY))
    rows = [["Reserved at the review", "Cores"],
            ["Firm tenants (eleven)", n0(f["firm_res"])],
            ["cell-ctl", n0(f["ctl_res"])],
            ["cell-store", n0(f["store_res"])],
            ["batch-train (guarantee)", n0(f["G"])],
            ["Not reserved", n0(f["unreserved"])],
            ["Reservable cores", n0(f["reservable"])]]
    s.append(_table(rows, [7.5 * cm, 3.2 * cm]))
    s.append(Paragraph("2 Use at the busiest hours", H2))
    s.append(Paragraph("Use is each tenant's average cores in use over an hour, from the cell monitoring export, which "
                       "holds %s of the quarter's %s hours." % (n0(f["hours"]), n0(f["hours_q"])), BODY))
    rows = [["", "Busiest hour (UTC)", "Cores in use"]]
    for k, lab in (("firm", "Firm tenants together"), ("cell-ctl", "cell-ctl"), ("cell-store", "cell-store"),
                   ("batch-train", "batch-train"), ("cell", "Whole cell")):
        v, t = f[k]
        rows.append([lab, t.strftime("%d %b %Y %H:%M"), n1(v)])
    s.append(_table(rows, [5.2 * cm, 4.2 * cm, 3.2 * cm]))
    s.append(Spacer(1, 4))
    s.append(Paragraph("The batch tier held %s per cent of its guarantee at its busiest hour, and 99 per cent or more of "
                       "it in %s of the quarter's hours on record." % (
                           "{:.1f}".format(100 * f["batch-train"][0] / f["G"]), n0(f["batch_hours_99"])), BODY))
    s.append(Paragraph("3 Events", H2))
    for t in ["19 August, 03:40 Madrid time (01:40 UTC): UPS B in hall 2 failed to transfer during the weekly generator "
              "test. C-22's control nodes lost power for about 40 seconds. Firm and platform services kept running; "
              "the batch scheduler restarted and drained every running batch run, admitting again from 07:15 Madrid "
              "time. The monitoring collector was down from 03:40 to 10:00 Madrid time.",
              "9 September, 04:00 to 07:35 Madrid time: the batch scheduler upgrade (release 3.12). Batch runs were "
              "drained at the start and resumed from their checkpoints after it.",
              "Monthly maintenance waves (firmware and operating system updates) ran in July, August and September in "
              "working hours, as every month."]:
        s.append(Paragraph(t, CLAUSE.clone("ev", leftIndent=12, firstLineIndent=0)))
    s.append(Paragraph("Prepared from the cell monitoring export, the C-22 reservation ledger and the hardware plan. "
                       "Questions to Compute Operations.", NOTE))
    foot = _footer("%s Internal." % K.COMPANY, "C-22 capacity report 2026 Q3")
    doc = _doc(path, "C-22 capacity report 2026 Q3", K.PEOPLE["requester"])
    doc.build(s, onFirstPage=foot, onLaterPages=foot)


# ---------------------------------------------------------------------------------------------------- operations log

def ops_entries(W):
    """MAD1's operations log for July to December 2026, Madrid time, as entered: (UTC time, initials, entry)."""
    U = lambda *a: dt.datetime(*a, tzinfo=K.UTC)
    e = []
    waves = [w0 for ms, w0 in W.waves if dt.datetime(2026, 7, 1, tzinfo=K.UTC) <= ms <= dt.datetime(2026, 12, 1,
                                                                                                        tzinfo=K.UTC)]
    wave_txt = ["July maintenance wave on C-22 started: BIOS 2.18 and the 26.06 OS image, rows 2A to 2L, working hours, "
                "about two weeks.",
                "August wave on C-22 started (NIC firmware, 26.07 OS image).",
                "September maintenance wave started on C-22. Disk controller firmware and the 26.08 image.",
                "October wave on C-22 started: BMC firmware and the 26.09 OS image.",
                "November maintenance wave started on C-22 (26.10 image, kernel live-patch tooling).",
                "December wave on C-22 started; short one, BIOS 2.19 only, finishing before the change freeze."]
    r = K.rng("opslog")
    for w0, txt in zip(waves, wave_txt):
        e.append((w0.replace(hour=6 + int(r.integers(0, 3)), minute=int(r.integers(0, 60))), "RF", txt))
    rack_txt = ["Rack %s in service in C-22 (Lena R4-96, 20 machines).", "%s racked, burnt in and handed to the "
                "scheduler: 20 machines.", "Rack %s live in C-22, 20 x Lena R4-96.", "%s in service, 20 machines.",
                "C-22 rack %s in service after burn-in.", "Rack %s handed over to the cell; 20 machines schedulable."]
    k = 0
    for rk in W.racks:
        t = rk["in_service"]
        if dt.datetime(2026, 7, 1, tzinfo=K.UTC) <= t < dt.datetime(2026, 12, 14, tzinfo=K.UTC):
            e.append((t + dt.timedelta(minutes=int(r.integers(3, 47))), "EM",
                      rack_txt[k % len(rack_txt)] % ("%s-%02d" % (rk["row"], rk["pos"]))))
            k += 1
    e += [
        (U(2026, 7, 7, 8, 15), "MA", "Reminder for the new on-call rota: cell-store's rolling daemon restart runs every "
                                     "Tuesday 03:00 to 05:00 UTC across C-22. Clients reconnect; no action needed."),
        (U(2026, 7, 21, 13, 30), "MA", "cell-store 8.4.2 rolled out across C-22, one row at a time. No client impact."),
        (U(2026, 8, 19, 1, 40), "RF", "Hall 2 UPS B failed to transfer during the weekly generator test. C-22 control "
                                      "nodes lost power, about 40 s, and restarted. Worker rows stayed up on feed A."),
        (U(2026, 8, 19, 1, 58), "MP", "Batch scheduler came back after the control-node restart and drained every "
                                      "running batch run. Firm services unaffected. Monitoring collector down."),
        (U(2026, 8, 19, 5, 15), "JS", "Batch scheduler admitting again; preempted runs resuming from their checkpoints."),
        (U(2026, 8, 19, 8, 3), "MP", "Monitoring collector back. Hours from 03:00 to 09:59 not recorded."),
        (U(2026, 8, 19, 9, 12), "MP", "Cluster manager restarted on the repaired control nodes."),
        (U(2026, 8, 20, 8, 40), "RF", "UPS B transfer switch inspected by the vendor; control board replaced. "
                                      "Generator tests suspended until the PIR."),
        (U(2026, 8, 24, 12, 0), "RF", "PIR-2026-031 (19 August power event) held. Generator tests resume on 2 "
                                      "September."),
        (U(2026, 9, 9, 2, 0), "JS", "Batch scheduler upgrade to 3.12 started. Batch runs drained."),
        (U(2026, 9, 9, 5, 35), "JS", "Scheduler 3.12 live. Batch admitting again."),
        (U(2026, 10, 6, 9, 30), "AB", "C-22 capacity report for 2026 Q3 issued."),
        (U(2026, 10, 25, 1, 6), "RF", "Clocks went back an hour at 03:00 CEST. Log times CET from this entry."),
        (U(2026, 11, 12, 10, 20), "EM", "Refresh delivery received: 29 racks of Lena R4-96 for C-22, staged in hall 2 at "
                                        "positions 2L-13 to 2M-19."),
        (U(2026, 11, 16, 8, 0), "AB", "Request window for 2027 Q1 open (closes 4 December 18:00)."),
        (U(2026, 11, 30, 15, 45), "EM", "Refresh racks cabled and powered. Burn-in started, 14 days."),
        (U(2026, 12, 4, 17, 0), "AB", "Request window for 2027 Q1 closed. Eleven firm tenants filed."),
        (U(2026, 12, 11, 12, 30), "EM", "C-22 hardware plan revised: refresh racks in service from 28 December."),
        (U(2026, 12, 14, 6, 10), "MP", "Monitoring export pulled for the 2027 Q1 review: C-22, 1 January 2025 to 13 "
                                       "December 2026 23:00 UTC."),
    ]
    out = []
    for t, by, txt in e:
        loc, _ = K.madrid(t)
        out.append((loc, by, txt))
    return sorted(out, key=lambda x: x[0])


def write_opslog(path, W):
    import docx
    from docx.shared import Inches, Pt
    d = docx.Document()
    st = d.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(9.5)
    d.add_heading("MAD1 operations log, July to December 2026", level=1)
    d.add_paragraph("Data-centre operations, MAD1 (Alcobendas). Entries as logged, Madrid local time (CEST to 25 October, "
                    "CET after). AB %s; EM %s; JS %s; MA %s; MP %s; RF %s." % (
                        K.PEOPLE["requester"], K.PEOPLE["fleet"], K.PEOPLE["batch"], K.PEOPLE["storage"],
                        K.PEOPLE["sre"], K.PEOPLE["dcops"]))
    t = d.add_table(rows=1, cols=4)
    t.style = "Table Grid"
    t.autofit = False
    widths = (Inches(0.95), Inches(0.5), Inches(4.75), Inches(0.4))
    for k, h in enumerate(("Date", "Time", "Entry", "By")):
        t.rows[0].cells[k].text = h
    for loc, by, txt in ops_entries(W):
        row = t.add_row().cells
        row[0].text = loc.date().isoformat()
        row[1].text = loc.strftime("%H:%M")
        row[2].text = txt
        row[3].text = by
    for r_ in t.rows:
        for k, w in enumerate(widths):
            r_.cells[k].width = w
    d.core_properties.author = K.PEOPLE["dcops"]
    d.core_properties.title = "MAD1 operations log 2026 H2"
    d.save(path)


# ---------------------------------------------------------------------------------------------------- hardware inventory

def write_inventory(path, W):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Assets"
    _title_rows(ws, "MAD1 hardware inventory: cell C-22", "Fleet & Hardware. Extract of 14 December 2026: every "
                "server asset installed in C-22 since the cell opened, with its slot and status.")
    hr = _head(ws, ["Asset tag", "Serial", "Model", "Row", "Rack", "Slot", "Installed", "Status", "Retired"],
               [12, 13, 12, 6, 8, 6, 12, 11, 12])
    for a in sorted(W.assets, key=lambda a: a["tag"]):
        if a["installed"] >= K.REFRESH_IN_SERVICE:
            status, inst = "staged", None
        elif a["retired"] is not None:
            status, inst = "retired", a["installed"].date()
        else:
            status, inst = "in service", a["installed"].date()
        ws.append([a["tag"], a["serial"], a["model"], a["row"], a["rack"], a["slot"], inst, status,
                   a["retired"].date() if a["retired"] is not None else None])
        for c in (7, 9):
            ws.cell(row=ws.max_row, column=c).number_format = "yyyy-mm-dd"
    ws.freeze_panes = ws.cell(row=hr + 1, column=1)
    ws.auto_filter.ref = "A%d:I%d" % (hr, ws.max_row)
    ws2 = wb.create_sheet("Cluster ids")
    _title_rows(ws2, "Cluster manager ids by asset", "Each id under which an asset has been registered with the MAD1 "
                "cluster manager, from the time of registration (UTC).")
    hr2 = _head(ws2, ["Asset tag", "Machine id", "Registered (UTC)"], [12, 12, 20])
    for a in sorted(W.assets, key=lambda a: a["tag"]):
        for t, m in a["ids"]:
            ws2.append([a["tag"], m, t.strftime("%Y-%m-%d %H:%M")])
    ws2.freeze_panes = ws2.cell(row=hr2 + 1, column=1)
    wb.save(path)


# ---------------------------------------------------------------------------------------------------- chargeback policy

def write_chargeback(path):
    s = [Paragraph("%s  |  Technology Controlling" % K.COMPANY, H1S), Paragraph("Technology chargeback policy 2026", H1),
         Paragraph("Effective 1 January 2026. Owner: %s, Technology Controlling. Applies to the compute cells at MAD1 "
                   "and BCN2." % K.PEOPLE["finance"], H1S)]

    def sec(title, clauses):
        s.append(Paragraph(title, H2))
        for no, text in clauses:
            s.append(Paragraph("%s&nbsp;&nbsp;&nbsp;%s" % (no, text), CLAUSE))

    sec("1 Who is charged", [
        ("1.1", "Firm tenants of the compute cells are charged each month, to the cost centre the tenant directory "
                "gives for them, for the reserved cores they hold in each cell."),
        ("1.2", "Platform services and the batch training tier are central costs and are not charged to product cost "
                "centres.")])
    sec("2 What a firm tenant pays", [
        ("2.1", "For each day of the month, the cores the tenant holds in the cell at 00:00 UTC that day, at the rate "
                "card's rate for reserved cores at the site in force on that day, divided by the number of days in the "
                "month. The month's charge is the sum over its days."),
        ("2.2", "The cores a tenant holds are its reservation for the quarter as approved at the cell's capacity review, "
                "with any release or grant made during the quarter through the cell's capacity desk. A release or grant "
                "counts from the first 00:00 UTC after the cell's quota service has applied it."),
        ("2.3", "Cores in use above a tenant's reservation are not charged; reserved cores left unused are charged.")])
    sec("3 Rates", [
        ("3.1", "Technology Controlling publishes the rate card. A rate applies from its effective date until the next "
                "rate for the same resource and site takes effect."),
        ("3.2", "Rates are reviewed each half year and may be adjusted between reviews for energy costs, with a month's "
                "notice.")])
    sec("4 Statements", [
        ("4.1", "Monthly charges are posted to cost centres by the fifth working day of the following month. Quarter "
                "statements are issued with the September, December, March and June postings."),
        ("4.2", "A cost centre owner may query a charge within 30 days of its posting.")])
    foot = _footer("%s Internal." % K.COMPANY, "Chargeback policy 2026")
    doc = _doc(path, "Technology chargeback policy 2026", K.PEOPLE["finance"])
    doc.build(s, onFirstPage=foot, onLaterPages=foot)


# ---------------------------------------------------------------------------------------------------- dictionary

DICT = [
    (K.USAGE, "hour_start_utc", "Start of the hour (UTC); the row covers the hour that starts then."),
    (K.USAGE, "cell", "Cell id."),
    (K.USAGE, "tenant", "Tenant id, as in the tenant directory."),
    (K.USAGE, "cores_in_use", "The tenant's average cores in use over the hour. cell-store reports from each storage "
                                 "daemon; samples that reach the collector after the hour has closed are not added "
                                 "back, so an hour in which some daemons reported late reads low."),
    (K.CELLHOURLY, "machines_installed", "Machines installed in the cell, hourly average (in service or out for repair "
                                         "or maintenance)."),
    (K.CELLHOURLY, "machines_in_service", "Schedulable machines registered with the cell's scheduler, hourly average."),
    (K.LEDGER, "reserved_cores", "The tenant's reservation for the quarter as approved at the capacity review; for "
                                 "batch-train, the batch guarantee."),
    (K.LEDGER, "approved_on", "Date of the review."),
    (K.REQUESTS, "cores_requested", "Cores the firm tenant asked to reserve for the quarter."),
    (K.REQUESTS, "filed_utc", "When the request was filed (UTC)."),
    (K.RATECARD, "eur_per_unit_month", "Euros per unit per month."),
    (K.RATECARD, "effective_from", "The rate applies from this date until the next effective date for the same "
                                   "resource and site."),
    (K.DIRECTORY, "class", "firm, platform or batch (CS-3, 1.3)."),
    (K.DIRECTORY, "cost_centre", "The cost centre the tenant's budget and charges sit in."),
    (K.RUNS, "job_id", "Training job; its runs are the first run and each resumption."),
    (K.RUNS, "cores", "Cores the run held when it started."),
    (K.RUNS, "ended_utc", "When the run ended; blank if it was still running when the snapshot was taken (1 October "
                          "2026 00:00 UTC)."),
    (K.RUNS, "end_state", "COMPLETED, PREEMPTED or RUNNING."),
    (K.RUNS, "resumed_from", "For a run that resumed a preempted run of the same job: that run."),
    (K.RUNS, "restore_checkpoint", "For a run that resumed a preempted run: the checkpoint it restored from."),
    (K.CHECKPOINTS, "run_id", "The run that wrote the checkpoint."),
    (K.CHECKPOINTS, "step", "Training step whose state the checkpoint holds."),
    (K.CHECKPOINTS, "write_started_utc", "When the state at step was snapshotted and the write began; checkpoint "
                                         "writes run in the background."),
    (K.CHECKPOINTS, "committed_utc", "When the write completed; blank if it did not complete."),
    (K.RESIZES, "at_utc", "When the resize took effect."),
    (K.RESIZES, "cores_after", "Cores held by the run from at_utc."),
    (K.MEVENTS, "machine_id", "The cluster manager's id for the machine."),
    (K.MEVENTS, "event", "REMOVED (drained out of the cell's pool) or REGISTERED (in the pool and schedulable)."),
    (K.MEVENTS, "cause", "For REMOVED: hw_fault or maintenance."),
    (K.MEVENTS, "rack", "Rack position of the machine."),
    (K.INVENTORY, "Status", "in service, retired or staged (racked, in burn-in)."),
    (K.INVENTORY, "Cluster ids", "Machine ids registered for the asset, with registration times (UTC)."),
    (K.QCHANGES, "delta_cores", "Change to the tenant's reserved cores: negative a release, positive a grant."),
    (K.QCHANGES, "requested_utc", "When the change was requested in the quota tool (UTC)."),
    (K.QRUNS, "run_started_utc", "When the quota service's reconciliation run started (UTC)."),
    (K.QRUNS, "changes_applied", "The changes the run applied to the cell's quotas, by change id."),
    (K.HWPLAN, "In service from", "Date the rack went into service in the cell, or is planned to."),
    (K.HWPLAN, "Machines", "Machines in the rack."),
    (K.BUDGETS, "CC", "Cost centre number; the tenant directory gives it with the cost centre's name."),
    (K.BUDGETS, "Budget line", "What the line pays for: reserved cores in one cell, or block storage at a site."),
    (K.BUDGETS, "Jan 2026 to Mar 2027", "The line's budget for the month, EUR."),
    (K.SISTERS, "Batch held at busiest hour (% of guarantee)", "The batch tier's use at its busiest hour of the "
                                                               "quarter, as a share of its guarantee."),
    (K.SISTERS, "Median queue wait, batch (h)", "Median time batch runs waited between submission and start."),
]


def write_dictionary(path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Fields"
    _title_rows(ws, "Data dictionary: C-22 capacity review files", "Compute Operations, MAD1. December 2026. Fields "
                "of the data files (CSV, JSON and workbooks) whose meaning their headers do not give.")
    _head(ws, ["File", "Field", "Definition"], [44, 22, 96])
    for f, c, d in DICT:
        ws.append([f, c, d])
        ws.cell(row=ws.max_row, column=3).alignment = Alignment(wrap_text=True, vertical="top")
    wb.save(path)


# ---------------------------------------------------------------------------------------------------- README

def write_readme(path, files):
    lines = ["Alisio Viajes, Compute Operations (MAD1)",
             "C-22 capacity review for 2027 Q1: files, compiled 14 December 2026",
             "",
             "File, what it is, where it came from:",
             ""]
    for name, what, source in files:
        lines.append(name)
        lines.append("    %s. %s." % (what, source))
    lines.append("")
    lines.append("Times are UTC unless a file says otherwise. Tenant ids are those of the tenant directory.")
    with open(path, "w", encoding="utf-8", newline="\r\n") as fh:
        fh.write("\n".join(lines) + "\n")


# ---------------------------------------------------------------------------------------------------- sister cells (distractor)

SISTER_CELLS = {"C-21": (3260, 0.118), "C-23": (2740, 0.141), "C-24": (3880, 0.096), "C-25": (5960, 0.083)}


def write_sisters(path, W):
    r = K.rng("sisters")
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Cells by quarter"
    _title_rows(ws, "MAD1 compute cells: quarterly summary, 2025 and 2026", "Compute Operations, MAD1. Figures at "
                "each quarter's review, with the quarter's batch delivery measures. Prepared 2 October 2026; 2026 Q4 "
                "batch measures not yet available.")
    hr = _head(ws, ["Cell", "Quarter", "Machines at start", "Reservable cores", "Firm reserved", "Batch guarantee",
                    "Batch held at busiest hour (% of guarantee)", "Median queue wait, batch (h)"],
               [7, 9, 10, 11, 11, 11, 14, 12])
    rows = []
    for cell, (m0, share) in SISTER_CELLS.items():
        m = m0
        for i, q in enumerate(K.QUARTERS):
            R_ = int(round(m * K.CORES * K.OVERCOMMIT))
            share += float(r.normal(0, 0.0035))
            G = int(round(R_ * share / 1000)) * 1000
            plat = 3.1 * m + 0.21 * G + 2000 + float(r.uniform(0, 300))
            F = int(round((R_ - G - plat - float(r.uniform(150, 900))) / 100)) * 100
            held = None if q == "2026Q4" else round(float(r.uniform(99.2, 99.95)), 1)
            wait = None if q == "2026Q4" else round(float(r.uniform(1.8, 8.5)), 1)
            rows.append([cell, q, m, R_, F, G, held, wait])
            m += 20 * int(r.integers(1, 4))
    waits = [3.1, 4.4, 2.6, 5.2, 3.7, 6.3, 4.8, None]
    for i, q in enumerate(K.QUARTERS):
        F = sum(W.firm_res[t][q] for t in K.FIRM)
        h0 = int((K.q_start(q) - K.EXPORT_START).total_seconds() // 3600)
        h1 = int((min(K.q_end(q), K.EXPORT_END) - K.EXPORT_START).total_seconds() // 3600)
        held = None if q == "2026Q4" else round(100 * max(float("%.1f" % x) for x in W.batch_h[h0:h1]) /
                                                W.guarantee[q], 1)
        rows.append(["C-22", q, W.m_start[q], W.reservable[q], F, W.guarantee[q], held, waits[i]])
    for x in sorted(rows, key=lambda x: (x[0], x[1])):
        ws.append(x)
        for c in (3, 4, 5, 6):
            ws.cell(row=ws.max_row, column=c).number_format = "#,##0"
    ws.freeze_panes = ws.cell(row=hr + 1, column=1)
    wb.save(path)


# ---------------------------------------------------------------------------------------------------- batch demand note (distractor)

DEMAND = {  # team: (peak concurrent cores wanted in H1 2027, core-hours a month in millions Jan..Jun)
    "ranking-ml": (36500, [14.2, 15.0, 16.8, 17.1, 18.4, 18.9]),
    "pricing-ml": (22400, [8.6, 9.1, 10.4, 10.8, 11.6, 12.0]),
    "fraud-ml": (13800, [6.1, 6.0, 6.7, 6.9, 7.3, 7.2]),
    "reco-ml": (33900, [12.9, 13.6, 15.2, 16.0, 16.6, 17.4]),
    "demand-ml": (17200, [6.8, 7.4, 8.9, 8.1, 7.6, 7.9]),
    "nlp-ml": (25300, [9.3, 10.2, 11.5, 12.4, 13.1, 13.8]),
}


def write_batch_demand(path, W):
    s = [Paragraph("%s  |  ML Platform" % K.COMPANY, H1S), Paragraph("Batch training demand, first half of 2027", H1),
         Paragraph("%s, batch training platform lead. 2 December 2026. For the C-22 review of 15 December." %
                   K.PEOPLE["batch"], H1S)]
    s.append(Paragraph("The six training teams sent their plans for January to June 2027 in November. The table gives "
                       "each team's training as planned, in core-hours a month, and the most cores it would want "
                       "running at once if every planned run started on time.", BODY))
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    rows = [["Team", "Peak cores wanted"] + ["%s (M core-h)" % m for m in months]]
    tot = [0.0] * 6
    peak = 0
    for t in K.TEAMS:
        p, ch = DEMAND[t]
        peak += p
        tot = [a + b for a, b in zip(tot, ch)]
        rows.append([t, n0(p)] + ["%.1f" % x for x in ch])
    rows.append(["All teams", n0(peak)] + ["%.1f" % x for x in tot])
    s.append(_table(rows, [2.6 * cm, 2.4 * cm] + [1.9 * cm] * 6))
    s.append(Spacer(1, 6))
    s.append(Paragraph("Two programmes drive the rise: the ranking and recommendation teams' move to larger models "
                       "from February, and the language team's retraining of the content models on the 2026 reviews "
                       "corpus. Peaks do not coincide across teams; in 2026 the tier's busiest hour ran at about 0.6 of "
                       "the sum of the teams' own peaks.", BODY))
    s.append(Paragraph("Planned training that does not fit the guarantee queues. Last quarter the median batch queue "
                       "wait in C-22 was 4.8 hours; teams have asked us to keep it under 6 hours for the larger "
                       "models.", BODY))
    s.append(Paragraph("Figures are the teams' plans as sent in November.", NOTE))
    foot = _footer("%s Internal." % K.COMPANY, "Batch demand H1 2027")
    doc = _doc(path, "Batch training demand H1 2027", K.PEOPLE["batch"])
    doc.build(s, onFirstPage=foot, onLaterPages=foot)
