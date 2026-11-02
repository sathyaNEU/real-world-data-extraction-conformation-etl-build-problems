"""The two golden deliverables from the computed figures: claims_fund_2027.xlsx and claims_note_2027.docx (with its
chart)."""
import datetime as dt
import io
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Cm, Pt
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

import common as CM
import params as P

XLSX = "claims_fund_2027.xlsx"
DOCX = "claims_note_2027.docx"
DEPOTS = [("CRA", "Cramlington"), ("GAT", "Gateshead (Team Valley)"), ("CAR", "Carlisle"), ("DAR", "Darlington")]
QLAB = {"2025Q1": "Jan to Mar 2025", "2025Q2": "Apr to Jun 2025", "2025Q3": "Jul to Sep 2025",
        "2025Q4": "Oct to Dec 2025", "2026Q1": "Jan to Mar 2026", "2026Q2": "Apr to Jun 2026"}
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
BANDS = ["00:00 to 04:00", "04:00 to 07:00", "07:00 to 09:00", "09:00 to 15:00", "15:00 to 19:00", "19:00 to 22:00",
         "22:00 to 24:00"]
BOLD = Font(bold=True)
HEAD = PatternFill("solid", fgColor="DDEBF7")
THIN = Border(bottom=Side(style="thin", color="808080"))


def _head(ws, row, labels):
    for j, t in enumerate(labels, 1):
        c = ws.cell(row=row, column=j, value=t)
        c.font = BOLD
        c.fill = HEAD
        c.alignment = Alignment(wrap_text=True, vertical="top")


def workbook(folder, F, X):
    wb = Workbook()
    ws = wb.active
    ws.title = "Fund 2027"
    ws["A1"] = "Motor claims fund 2027: delivery trucks"
    ws["A1"].font = Font(bold=True, size=13)
    ws["A2"] = "%s, Risk and Insurance Manager, 2 November 2026. Collisions by incident date (UK time); amounts in GBP " \
               "net of VAT." % P.PEOPLE["risk_manager"]
    ws["A4"] = "Collision claims expected in 2027"
    ws["A4"].font = BOLD
    _head(ws, 5, ["Period", "Claims"])
    r = 6
    for lab, k in (("April to September 2027", "claims_2027_apr_sep"),
                   ("January to March and October to December 2027", "claims_2027_other_months")):
        ws.cell(row=r, column=1, value=lab)
        ws.cell(row=r, column=2, value=F[k])
        r += 1
    ws.cell(row=r, column=1, value="2027 year").font = BOLD
    ws.cell(row=r, column=2, value=F["claims_2027"]).font = BOLD
    ws.cell(row=r + 1, column=1, value="To the nearest 50; the unrounded expectation by month is on the next sheet.")
    r += 3
    ws.cell(row=r, column=1, value="Paid back by other insurers, by quarter of the collision (received to 31 Oct 2026)").font = BOLD
    _head(ws, r + 1, ["Collisions in", "Received £"])
    r += 2
    for q, lab in QLAB.items():
        ws.cell(row=r, column=1, value=lab)
        c = ws.cell(row=r, column=2, value=F["recoveries_by_collision_quarter"][q])
        c.number_format = "#,##0"
        r += 1
    r += 1
    ws.cell(row=r, column=1, value="Brantwick repair cost of each depot's collisions").font = BOLD
    _head(ws, r + 1, ["Depot", "Collisions Jan to Jun 2025 £", "Collisions Jul to Dec 2025 £",
                      "Collisions Jan to Jun 2026 £"])
    r += 2
    for code, name in DEPOTS:
        ws.cell(row=r, column=1, value=name)
        for j, p in enumerate(("2025H1", "2025H2", "2026H1"), 2):
            c = ws.cell(row=r, column=j, value=F["repair_cost_by_depot"]["%s %s" % (code, p)])
            c.number_format = "#,##0"
        r += 1
    ws.cell(row=r + 1, column=1, value="Money to the nearest £100. Repair cost is the bodyshop's invoices for each "
                                       "collision's repair, each invoice once.")
    ws.column_dimensions["A"].width = 46
    ws.column_dimensions["B"].width = 20
    ws.column_dimensions["C"].width = 26
    ws.column_dimensions["D"].width = 26

    w2 = wb.create_sheet("2027 by month")
    w2["A1"] = "2027 schedule: planned kilometres and expected collision claims by month"
    w2["A1"].font = BOLD
    _head(w2, 3, ["Month", "Delivery days", "Planned km", "of which before sunrise or after sunset", "Expected claims"])
    Fm = X["F"]
    for i, m in enumerate(range(1, 13)):
        g = Fm[Fm.month == m]
        row = [MONTHS[i] + " 2027", int(g.date.nunique()), round(float(g.km.sum())), round(float(g[g.dark == 1].km.sum())),
               F["claims_2027_months_unrounded"]["%02d" % m]]
        for j, v in enumerate(row, 1):
            c = w2.cell(row=4 + i, column=j, value=v)
            if j in (3, 4):
                c.number_format = "#,##0"
            if j == 5:
                c.number_format = "0.0"
    w2.cell(row=16, column=1, value="2027").font = BOLD
    w2.cell(row=16, column=2, value=len(X["X"]["days"])).font = BOLD
    w2.cell(row=16, column=3, value=round(float(Fm.km.sum()))).number_format = "#,##0"
    w2.cell(row=16, column=4, value=round(float(Fm[Fm.dark == 1].km.sum()))).number_format = "#,##0"
    c = w2.cell(row=16, column=5, value=F["claims_2027_unrounded"])
    c.number_format = "0.0"
    c.font = BOLD
    for col, w in zip("ABCDE", [12, 13, 13, 22, 15]):
        w2.column_dimensions[col].width = w

    w3 = wb.create_sheet("Rates")
    w3["A1"] = "Collision claims per 100,000 km, October 2023 to September 2026, by clock time and light"
    w3["A1"].font = BOLD
    w3["A2"] = "Light from Appendix C of the driver handbook (sunrise and sunset at the truck's depot); Poisson rate on " \
               "kilometres with clock band and light."
    _head(w3, 4, ["Clock band (UK time)", "Light", "Km driven", "Claims", "Claims per 100,000 km", "Fitted per 100,000 km"])
    rt = X["M"]["rates"]
    r = 5
    for _, x in rt.iterrows():
        vals = [BANDS[int(x.band)], "Dark" if x.dark else "Daylight", round(float(x.km)), int(x.n),
                round(float(x.n / x.km * 1e5), 2), round(float(x.fitted_per_100k_km), 2)]
        for j, v in enumerate(vals, 1):
            c = w3.cell(row=r, column=j, value=v)
            if j == 3:
                c.number_format = "#,##0"
        r += 1
    w3.cell(row=r + 1, column=1, value="Darkness multiplier")
    w3.cell(row=r + 1, column=2, value=F["dark_multiplier_1dp"])
    bt = X["BT"]
    w3.cell(row=r + 3, column=1, value="Back-test: 04:00 to 07:00 in the dark (the May to August schedule)").font = BOLD
    for k, (lab, v) in enumerate([("Km driven", round(bt["km"])), ("Claims", bt["obs"]),
                                  ("Expected, light model fitted without them", round(bt["light"], 1)),
                                  ("Expected at the 04:00 to 07:00 rate", round(bt["band"], 1)),
                                  ("Expected at each clock hour's rate", round(bt["hour"], 1))]):
        w3.cell(row=r + 4 + k, column=1, value=lab)
        c = w3.cell(row=r + 4 + k, column=2, value=v)
        if k == 0:
            c.number_format = "#,##0"
    for row in w3.iter_rows(min_row=5, max_row=4 + len(rt)):
        row[4].number_format = row[5].number_format = "0.00"
    for col, w in zip("ABCDEF", [44, 10, 14, 8, 12, 12]):
        w3.column_dimensions[col].width = w
    w3.freeze_panes = "A5"
    w2.freeze_panes = "A4"
    wn = wb.create_sheet("Notes")
    notes = [
        ("As at", "Claims listing as at 31 October 2026; Gridtrak day summaries to 30 September 2026; recovery account to "
                  "31 October 2026; AP ledger to the import of 27 October 2026."),
        ("Claims", "As the fund terms define them: collisions of the delivery trucks on the fleet register (route trucks "
                   "and spares) notified to Ravensby; company cars, duplicate notifications and withdrawn notifications "
                   "excluded. The fitted record runs October 2023 to September 2026, the months the telematics cover."),
        ("Periods", "By incident date in UK clock time: the 2027 claims split between April to September and the other "
                    "six months; recoveries by calendar quarter of the collision; repair cost by half-year of the "
                    "collision."),
        ("Light", "A kilometre is dark when driven before sunrise or after sunset at its depot, from Appendix C of the "
                  "driver handbook (GMT, one hour added under British Summer Time). Kilometres are spread evenly over each "
                  "day's first ignition on to last ignition off."),
        ("2027 exposure", "Every route of the 2027 route schedule at its planned departure, planned day and planned km, on "
                          "each delivery day of the 2027 calendar."),
        ("Money", "Net of VAT. Repair cost is Brantwick's invoices for each collision's repair (inspection and storage for "
                  "a total loss), each invoice counted once; recoveries are credited to the quarter of the collision."),
        ("Rounding", "Claims to the nearest 50; money to the nearest £100.")]
    wn.append(["Item", "Note"])
    for c in wn[1]:
        c.font = BOLD
        c.fill = HEAD
    for k, v in notes:
        wn.append([k, v])
    for row in wn.iter_rows(min_row=2):
        row[1].alignment = Alignment(wrap_text=True, vertical="top")
        row[0].alignment = Alignment(vertical="top")
    wn.column_dimensions["A"].width = 14
    wn.column_dimensions["B"].width = 100
    CM.save_xlsx(wb, os.path.join(folder, XLSX), dt.datetime(2026, 11, 2, 15, 52), P.PEOPLE["risk_manager"])


def chart(F):
    rec = F["record_claims_by_month"]
    labs = list(rec.keys())
    vals = list(rec.values())
    fut = [F["claims_2027_months_unrounded"]["%02d" % m] for m in range(1, 13)]
    x1 = np.arange(len(vals))
    x2 = np.arange(len(vals) + 4, len(vals) + 16)
    blue, orange, ink, muted = "#2a78d6", "#eb6834", "#0b0b0b", "#52514e"
    fig, ax = plt.subplots(figsize=(6.6, 2.75), dpi=150)
    fig.patch.set_facecolor("#fcfcfb")
    ax.set_facecolor("#fcfcfb")
    ax.grid(axis="y", color="#e4e3df", linewidth=0.6)
    ax.set_axisbelow(True)
    ax.bar(x1, vals, color=blue, width=0.78, label="Claims, Oct 2023 to Sep 2026")
    ax.bar(x2, fut, color=orange, width=0.78, label="Expected on the 2027 schedule")
    ticks = [i for i, l in enumerate(labs) if l.endswith("-01") or l.endswith("-07")]
    ax.set_xticks(list(ticks) + [x2[0], x2[6]])
    ax.set_xticklabels([("%s %s" % (MONTHS[int(labs[i][5:]) - 1], labs[i][:4])) for i in ticks] + ["Jan 2027", "Jul 2027"],
                       fontsize=7, color=muted)
    ax.tick_params(axis="y", labelsize=7, colors=muted)
    ax.tick_params(axis="x", length=0)
    ax.set_ylabel("Collision claims per month", fontsize=7.5, color=muted)
    ax.set_title("The 2027 schedule adds its claims in the dark months, October to March", fontsize=9, color=ink,
                 loc="left")
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color("#b9b8b2")
    ax.legend(fontsize=6.8, frameon=False, loc="upper left", ncol=2)
    top = max(max(vals), max(fut))
    ax.set_ylim(0, top * 1.32)
    k = int(np.argmax(fut))
    ax.annotate("%.0f expected in %s" % (fut[k], MONTHS[k]), xy=(x2[k], fut[k]), xytext=(x2[k] - 6.5, top * 1.12),
                fontsize=6.8, color=ink, arrowprops=dict(arrowstyle="-", color=muted, linewidth=0.6))
    ax.axvline(len(vals) + 1.5, color="#b9b8b2", linewidth=0.6, linestyle=(0, (2, 2)))
    ax.text(len(vals) + 1.2, top * 0.80, "new schedule\nfrom 2 Jan", fontsize=6.3, color=muted, va="bottom",
            ha="right")
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", metadata={"Software": None}, facecolor=fig.get_facecolor())
    plt.close(fig)
    return buf.getvalue()


def note(folder, F, X):
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10)
    st.paragraph_format.space_after = Pt(5)
    sec = doc.sections[0]
    sec.top_margin = sec.bottom_margin = Cm(1.5)
    sec.left_margin = sec.right_margin = Cm(2.0)
    fp = sec.footer.paragraphs[0]
    fp.text = "%s, motor claims fund 2027, board paper, November 2026" % P.COMPANY
    fp.runs[0].font.size = Pt(8)
    h = doc.add_paragraph()
    rr = h.add_run("The new schedule takes the trucks' 2027 collision claims to %d" % F["claims_2027"])
    rr.bold = True
    rr.font.size = Pt(13)
    meta = doc.add_paragraph()
    meta.add_run("To: the board.  From: %s, Risk and Insurance Manager.  Date: 2 November 2026.  Subject: the number of "
                 "collision claims for the 2027 motor claims fund." % P.PEOPLE["risk_manager"]).font.size = Pt(9)
    bt = X["BT"]
    rec_year = round(sum(F["record_claims_by_month"].values()) / 3)
    doc.add_paragraph(
        "I expect the delivery trucks to make %d collision claims in 2027: %d from April to September and %d in the other "
        "six months, January to March and October to December.* The last three years averaged %d a year on the current "
        "schedules." % (F["claims_2027"], F["claims_2027_apr_sep"], F["claims_2027_other_months"], rec_year))
    doc.add_paragraph(
        "The increase comes from the new schedule. From 2 January every route leaves between 03:45 and 05:15, so from "
        "October to March each truck starts its route in the dark, up to five hours before sunrise in midwinter. Over the "
        "last three years a "
        "kilometre driven before sunrise or after sunset carried about %.1f times the collision rate of a daylight "
        "kilometre at the same time of day. Our early starts so far ran only on the May to August schedule, mostly after "
        "sunrise, which is why the small hours look like our safest driving if the history is read by time of day alone. "
        "The early starts that did begin before sunrise, on the May to August schedule, had %d collisions against %.1f "
        "expected on "
        "the darkness rate and %.1f on the 04:00 to 07:00 rate." % (F["dark_multiplier"], bt["obs"], bt["light"], bt["band"]))
    doc.add_picture(io.BytesIO(chart(F)), width=Cm(16.5))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    src = doc.add_paragraph("Source: Gridtrak day summaries October 2023 to September 2026; Ravensby claims listing as at "
                            "31 October 2026; 2027 route schedule and calendar; driver handbook Appendix C.")
    src.runs[0].font.size = Pt(8)
    a = F["recoveries_by_collision_quarter"]
    doc.add_paragraph(
        "Other insurers have so far paid back %s towards the 2025 collisions and %s towards those of January to June 2026; "
        "the quarters are in the workbook. Brantwick's repair cost of each depot's collisions:" % (
            "£{:,}".format(sum(a[k] for k in ("2025Q1", "2025Q2", "2025Q3", "2025Q4"))),
            "£{:,}".format(a["2026Q1"] + a["2026Q2"])))
    t = doc.add_table(rows=1, cols=4)
    t.style = "Light List"
    for c, txt in zip(t.rows[0].cells, ["Depot", "January to June 2025", "July to December 2025", "January to June 2026"]):
        c.text = txt
    for code, name in DEPOTS:
        r = t.add_row().cells
        r[0].text = name
        for k, per in enumerate(("2025H1", "2025H2", "2026H1"), 1):
            r[k].text = "£{:,}".format(F["repair_cost_by_depot"]["%s %s" % (code, per)])
    for row in t.rows:
        for k, c in enumerate(row.cells):
            for para in c.paragraphs:
                para.paragraph_format.space_after = Pt(0)
                if k:
                    para.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                for run in para.runs:
                    run.font.size = Pt(9)
    fn = doc.add_paragraph("* Claims as the fund terms count them: collisions of the delivery trucks, route trucks and "
                           "spares, in the period of the incident date in UK clock time; company cars, duplicate "
                           "notifications and "
                           "withdrawn notifications are not claims. Money is net of VAT, to the nearest £100. Figures and "
                           "workings are in claims_fund_2027.xlsx.")
    fn.runs[0].font.size = Pt(8)
    CM.save_docx(doc, os.path.join(folder, DOCX), dt.datetime(2026, 11, 2, 16, 18), P.PEOPLE["risk_manager"])


def write(folder, F, X):
    workbook(folder, F, X)
    note(folder, F, X)
