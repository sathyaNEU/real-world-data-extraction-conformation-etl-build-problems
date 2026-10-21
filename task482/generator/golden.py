"""The golden deliverable, computed from the cut pack through bundle.py: the management board's third-quarter 2026
timeliness workbook (each office's median working days for its July to September applications, the open ones censored
at their age, the offices placed on a plan, and the quarter's card payments), and generator/figures.json."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import bundle as B    # noqa: E402

FILE = "cro_timeliness_plans_q3_2026.xlsx"
INK = "1B2430"
GREEN = "2C5A3F"
PALE = "E7EFE9"
MUTED = "A3ACB8"
ACCENT = "B4452F"
NAMES = {"CRO-AD": "Ardmuir", "CRO-BN": "Bannock", "CRO-CV": "Carrick", "CRO-DL": "Dunlay", "CRO-ES": "Eskmoor",
         "CRO-FM": "Fallowmere", "CRO-GQ": "Glenquhar", "CRO-HL": "Harlaw", "CRO-IB": "Inverbeck",
         "CRO-KM": "Kelso Moss", "CRO-LW": "Lenwick", "CRO-MG": "Mossgiel", "CRO-NM": "Northmuir",
         "CRO-SL": "Strathlorn"}


def compute(target):
    b = B.load(target)
    m = B.medians(b, "golden")
    return {"b": b, "m": m, "reg": B.medians(b, "registered_only"), "pl": B.planned(b, m), "a": B.ask(b)}


def counts(b):
    out = {}
    for u in b["ids"]:
        r = sum(1 for o, rec, c, g in b["reg"] if o == u and B.Q3[0] <= rec <= B.Q3[1])
        o_ = sum(k for o, rec, c, k in b["open"] if o == u and B.Q3[0] <= rec <= B.Q3[1])
        out[u] = (r, o_)
    return out


def write_xlsx(path, G):
    import openpyxl
    from openpyxl.chart import BarChart, Reference
    from openpyxl.chart.series import DataPoint
    from openpyxl.chart.shapes import GraphicalProperties
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    from openpyxl.utils import get_column_letter
    b, m = G["b"], G["m"]
    cnt = counts(b)
    wb = openpyxl.Workbook()
    hdr = Font(name="Calibri", bold=True, color="FFFFFF", size=10)
    hfill = PatternFill("solid", fgColor=GREEN)
    body = Font(name="Calibri", size=10, color=INK)
    bold = Font(name="Calibri", size=10, color=INK, bold=True)
    thin = Border(bottom=Side(style="thin", color="C3CAD3"))
    nfill = PatternFill("solid", fgColor=PALE)

    def head(ws, row, cols, widths):
        for i, (h, w) in enumerate(zip(cols, widths), 1):
            c = ws.cell(row=row, column=i, value=h)
            c.font, c.fill = hdr, hfill
            c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="left" if i <= 2 else "right")
            ws.column_dimensions[get_column_letter(i)].width = w
        ws.row_dimensions[row].height = 44

    def title(ws, t, sub):
        ws["A1"] = t
        ws["A1"].font = Font(name="Calibri", size=13, bold=True, color=INK)
        ws["A2"] = sub
        ws["A2"].font = Font(name="Calibri", size=9, italic=True, color="5B6470")

    ws = wb.active
    ws.title = "Offices"
    pl = G["pl"]
    title(ws, "%d of 14 offices go on a timeliness improvement plan: %s" % (len(pl), ", ".join(
        "%s (%s)" % (NAMES[u], u) for u in pl)),
          "Median working days from a complete application to registration for applications received 1 July to 30 "
          "September 2026; applications still open on 9 October counted as lasting at least their age "
          "(product-limit estimate).")
    cols = ["Office", "Office name", "Received in the quarter", "Registered by 9 October", "Open on 9 October",
            "Median of the registered (working days)", "Median, open applications at risk (working days)",
            "Improvement plan"]
    head(ws, 4, cols, [9, 14, 12, 12, 11, 14, 15, 12])
    for i, u in enumerate(b["ids"]):
        r, o = cnt[u]
        vals = [u, NAMES[u], r + o, r, o, G["reg"][u], m[u], "yes" if u in pl else "no"]
        for j, v in enumerate(vals, 1):
            c = ws.cell(row=5 + i, column=j, value=v)
            c.font = bold if (u in pl and j in (1, 2, 8)) else body
            c.border = thin
            if u in pl:
                c.fill = nfill
            if 3 <= j <= 5:
                c.number_format = "#,##0"
            elif j in (6, 7):
                c.number_format = "0"
            if j >= 3:
                c.alignment = Alignment(horizontal="right")
    ws.freeze_panes = "C5"
    r0 = 5 + len(b["ids"]) + 1
    for k, t in enumerate([
        "An application still open on 9 October has lasted at least its working days since its clock started, and the "
        "open ones are the slow ones: the offices with a backlog have their slowest applications among them. Each open "
        "application stays at risk until its age and the median is read where the product-limit survival estimate "
        "first falls to one half.",
        "Working days exclude weekends and the bank holidays of 1 June, 3 August and 26 October. The clock starts on "
        "the complete day (board paper, section 2). Registrations of June and October receipts are outside the quarter.",
    ]):
        c = ws.cell(row=r0 + k, column=1, value=t)
        c.font = Font(name="Calibri", size=9, color="5B6470")
        c.alignment = Alignment(wrap_text=True, vertical="top")
        ws.merge_cells(start_row=r0 + k, start_column=1, end_row=r0 + k, end_column=8)
        ws.row_dimensions[r0 + k].height = 40

    cs = wb.create_sheet("Chart data")
    cs.append(["Office", "Median working days"])
    for u in b["ids"]:
        cs.append([u, m[u]])
    bc = BarChart()
    bc.type = "col"
    bc.title = "Median working days to registration, third-quarter applications, against the 20-day line"
    bc.y_axis.title = "Working days"
    bc.y_axis.delete = False
    bc.x_axis.delete = False
    bc.add_data(Reference(cs, min_col=2, min_row=1, max_row=len(b["ids"]) + 1), titles_from_data=True)
    bc.set_categories(Reference(cs, min_col=1, min_row=2, max_row=len(b["ids"]) + 1))
    bc.series[0].graphicalProperties = GraphicalProperties(solidFill=MUTED)
    for i, u in enumerate(b["ids"]):
        if u in pl:
            pt = DataPoint(idx=i)
            pt.graphicalProperties = GraphicalProperties(solidFill=ACCENT)
            bc.series[0].dPt.append(pt)
    bc.legend = None
    bc.height, bc.width = 10, 22
    ws.add_chart(bc, "A%d" % (r0 + 3))

    q = wb.create_sheet("Q3 2026 card payments")
    title(q, "Card payments made in the third quarter of 2026", "By the day the payment was taken (the settlement "
                                                                  "batch's terminal day), not the day it settled.")
    head(q, 4, ["Office", "Office name", "Payments", "Amount (EUR)"], [9, 14, 12, 14])
    for i, u in enumerate(b["ids"]):
        for j, (v, fm) in enumerate(((u, None), (NAMES[u], None), (G["a"][u][0], "#,##0"),
                                     (G["a"][u][1], "#,##0")), 1):
            c = q.cell(row=5 + i, column=j, value=v)
            c.font, c.border = body, thin
            if fm:
                c.number_format = fm
    for w in wb.worksheets:
        w.sheet_view.showGridLines = False
        w.page_setup.orientation = "landscape"
        w.page_setup.fitToWidth = 1
        w.page_setup.fitToHeight = 0
        w.sheet_properties.pageSetUpPr.fitToPage = True
    wb.save(path)


def figures(G):
    b = G["b"]
    return {
        "call": {"planned": G["pl"]},
        "ask": {u: {"payments": G["a"][u][0], "amount": int(round(G["a"][u][1]))} for u in b["ids"]},
        "default_path": {"planned": B.planned(b, G["reg"])},
        "conventions": {"line": 20, "years": [2026, 2027], "counts": [14], "dates": [1, 9, 30, 31]},
    }


def main(target, gdir, fig_path):
    os.makedirs(gdir, exist_ok=True)
    G = compute(target)
    write_xlsx(os.path.join(gdir, FILE), G)
    import postprocess as PP
    PP.normalize_ooxml(os.path.join(gdir, FILE), "Jennifer Dyer", "Jennifer Dyer", "2026-10-12T09:10:00Z",
                       "2026-10-14T15:35:00Z", excel=True, company=PP.COMPANY)
    with open(fig_path, "w") as fh:
        json.dump(figures(G), fh, indent=1, sort_keys=True)
        fh.write("\n")
    return G
