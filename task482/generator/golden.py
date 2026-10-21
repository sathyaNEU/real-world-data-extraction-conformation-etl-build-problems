"""The golden deliverable, computed from the cut pack through bundle.py: the quality board's 2027 re-validation
workbook (each region's register error rate estimated from the summer audit, each audited record weighted by the
register records of its stratum, the regions chosen, and the third-quarter registrations and dissolutions), and
generator/figures.json."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import bundle as B    # noqa: E402

FILE = "sar_register_revalidation_2027_regions.xlsx"
INK = "1B2430"
GREEN = "2C5A3F"
PALE = "E7EFE9"
MUTED = "A3ACB8"
ACCENT = "B4452F"
NAMES = "sar_region_code_crosswalk_2025.csv"


def compute(target):
    b = B.load(target)
    r = B.rates(b, "golden")
    return {"b": b, "r": r, "naive": B.rates(b, "audited_share"), "ch": B.chosen(b, r), "a": B.ask_a(b),
            "bb": B.ask_b(b)}


def strata(b):
    import datetime as dt
    cut = dt.datetime(2026, 5, 1)
    N = {}
    for k, t in b["created"].items():
        if t < cut:
            key = (b["region"][k], k in b["flagged"])
            N[key] = N.get(key, 0) + 1
    n = {}
    for k, u, e in b["audit"]:
        key = (u, k in b["flagged"])
        a = n.setdefault(key, [0, 0])
        a[0] += 1
        a[1] += e
    return N, n


def write_xlsx(path, G, target):
    import csv
    import openpyxl
    from openpyxl.chart import BarChart, Reference
    from openpyxl.chart.series import DataPoint
    from openpyxl.chart.shapes import GraphicalProperties
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    from openpyxl.utils import get_column_letter
    b, r = G["b"], G["r"]
    names = {row["region"]: row["region_name"] for row in csv.DictReader(open(os.path.join(target, NAMES),
                                                                             encoding="utf-8"))}
    N, n = strata(b)
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
    ws.title = "Regions"
    ch = G["ch"]
    title(ws, "%d of 14 regional registers go to the 2027 re-validation: %s" % (len(ch), ", ".join(
        "%s (%s)" % (names[u], u) for u in ch)),
          "Share of each region's 30 April 2026 records in error, estimated from the summer audit with each audited "
          "record standing for the register records of its stratum (referred by the May risk screen or not).")
    cols = ["Region", "Region name", "Records 30 April", "Referred by the screen", "Audited, referred",
            "In error, referred", "Audited, not referred", "In error, not referred", "Audited share in error (%)",
            "Register error rate (%)", "Re-validation"]
    head(ws, 4, cols, [8, 16, 11, 11, 10, 10, 10, 10, 11, 11, 11])
    for i, u in enumerate(b["ids"]):
        vals = [u, names[u], N[(u, True)] + N[(u, False)], N[(u, True)], n[(u, True)][0], n[(u, True)][1],
                n[(u, False)][0], n[(u, False)][1], round(100 * G["naive"][u], 1), round(100 * r[u], 1),
                "yes" if u in ch else "no"]
        for j, v in enumerate(vals, 1):
            c = ws.cell(row=5 + i, column=j, value=v)
            c.font = bold if (u in ch and j in (1, 2, 11)) else body
            c.border = thin
            if u in ch:
                c.fill = nfill
            if 3 <= j <= 8:
                c.number_format = "#,##0"
            elif j in (9, 10):
                c.number_format = "0.0"
            if j >= 3:
                c.alignment = Alignment(horizontal="right")
    ws.freeze_panes = "C5"
    r0 = 5 + len(b["ids"]) + 1
    for k, t in enumerate([
        "The audit drew close to a quarter of the records the May screen referred and one in twenty-five of the rest, "
        "and referred records are in error far more often, so the audited share overstates each register's rate. "
        "Each stratum's audited error rate is carried to that stratum's records on the 30 April register.",
        "Records registered after 30 April are outside the audit's frame (board paper, section 2). Outcomes FAIL "
        "(to 30 June) and 1 to 4 (from 1 July) are errors.",
    ]):
        c = ws.cell(row=r0 + k, column=1, value=t)
        c.font = Font(name="Calibri", size=9, color="5B6470")
        c.alignment = Alignment(wrap_text=True, vertical="top")
        ws.merge_cells(start_row=r0 + k, start_column=1, end_row=r0 + k, end_column=11)
        ws.row_dimensions[r0 + k].height = 40

    cs = wb.create_sheet("Chart data")
    cs.append(["Region", "Register error rate (%)"])
    for u in b["ids"]:
        cs.append([u, round(100 * r[u], 2)])
    bc = BarChart()
    bc.type = "col"
    bc.title = "Register error rate by region against the 4 per cent line"
    bc.y_axis.title = "Records in error, per cent"
    bc.y_axis.numFmt = "0.0"
    bc.y_axis.delete = False
    bc.x_axis.delete = False
    bc.add_data(Reference(cs, min_col=2, min_row=1, max_row=len(b["ids"]) + 1), titles_from_data=True)
    bc.set_categories(Reference(cs, min_col=1, min_row=2, max_row=len(b["ids"]) + 1))
    bc.series[0].graphicalProperties = GraphicalProperties(solidFill=MUTED)
    for i, u in enumerate(b["ids"]):
        if u in ch:
            pt = DataPoint(idx=i)
            pt.graphicalProperties = GraphicalProperties(solidFill=ACCENT)
            bc.series[0].dPt.append(pt)
    bc.legend = None
    bc.height, bc.width = 10, 22
    ws.add_chart(bc, "A%d" % (r0 + 3))

    q = wb.create_sheet("Q3 2026")
    title(q, "The third quarter of 2026 by region", "New registrations in the register's quarter (Ardmuir local time); "
                                                    "companies struck off and dissolved in the quarter and still "
                                                    "dissolved at its end.")
    head(q, 4, ["Region", "Region name", "New registrations", "Struck off and still dissolved"], [8, 16, 14, 16])
    for i, u in enumerate(b["ids"]):
        for j, (v, fm) in enumerate(((u, None), (names[u], None), (G["a"][u], "#,##0"), (G["bb"][u], "#,##0")), 1):
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
        "call": {"chosen": G["ch"]},
        "ask_a": {u: G["a"][u] for u in b["ids"]},
        "ask_b": {u: G["bb"][u] for u in b["ids"]},
        "default_path": {"chosen": B.chosen(b, G["naive"])},
        "conventions": {"line_pct": 4, "years": [2025, 2026, 2027], "counts": [14], "dates": [30, 18, 1]},
    }


def main(target, gdir, fig_path):
    os.makedirs(gdir, exist_ok=True)
    G = compute(target)
    write_xlsx(os.path.join(gdir, FILE), G, target)
    import postprocess as PP
    PP.normalize_ooxml(os.path.join(gdir, FILE), "Sophie Williams", "Sophie Williams", "2026-10-09T09:10:00Z",
                       "2026-10-12T15:35:00Z", excel=True, company=PP.COMPANY)
    with open(fig_path, "w") as fh:
        json.dump(figures(G), fh, indent=1, sort_keys=True)
        fh.write("\n")
    return G
