"""The golden deliverable, computed from the cut pack through bundle.py: the board's 2027-28 instructional investment
grant workbook (every reporting unit's fiscal 2026 instruction expense per FTE, the parents' returns apportioned to
their branches by the cost of the credit hours each campus teaches, the five awards, and the branches' fall 2026 FTE
and headcount), and generator/figures.json."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import bundle as B    # noqa: E402

FILE = "lhecb_2027-28_instructional_investment_awards.xlsx"
INK = "1B2430"
GREEN = "2C5A3F"
PALE = "E7EFE9"
MUTED = "A3ACB8"
ACCENT = "B4452F"
NAMES = "ipeds_hd2025_directory_lakemoor_public.csv"


def compute(target):
    b = B.load(target)
    v = B.per_fte(b, "golden")
    return {"b": b, "v": v, "coef": B.fit(b), "aw": B.awarded(b, v), "a": B.ask_a(b), "bb": B.ask_b(b)}


def write_xlsx(path, G, target):
    import csv
    import openpyxl
    from openpyxl.chart import BarChart, Reference
    from openpyxl.chart.series import DataPoint
    from openpyxl.chart.shapes import GraphicalProperties
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    from openpyxl.utils import get_column_letter
    b, v = G["b"], G["v"]
    names = {r["UNITID"]: r["INSTNM"] for r in csv.DictReader(open(os.path.join(target, NAMES), encoding="utf-8"))}
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
        ws.row_dimensions[row].height = 42

    def title(ws, t, sub):
        ws["A1"] = t
        ws["A1"].font = Font(name="Calibri", size=13, bold=True, color=INK)
        ws["A2"] = sub
        ws["A2"].font = Font(name="Calibri", size=9, italic=True, color="5B6470")

    coef = G["coef"]
    ws = wb.active
    ws.title = "Awards"
    aw = G["aw"]
    title(ws, "Five awards: %s" % ", ".join("%s (%s)" % (names[u], u) for u in sorted(aw, key=lambda u: v[u])),
          "Fiscal 2026 instruction expense per 2025-26 12-month FTE student. A parent's return is split among the "
          "parent and its branches by the cost of the credit hours each teaches, at the cost per credit hour by level "
          "fitted on the sixteen campuses that report alone.")
    cols = ["UNITID", "Campus", "Reports", "Lower-division credit hours", "Upper-division credit hours",
            "Graduate credit hours", "Instruction expense ($)", "12-month FTE", "Instruction per FTE ($)", "Rank",
            "Award"]
    head(ws, 4, cols, [9, 40, 14, 13, 13, 12, 15, 10, 12, 7, 8])
    order = sorted(b["ids"], key=lambda u: v[u])
    rep = {"S": "own return", "P": "parent", "C": "within parent"}
    for i, u in enumerate(order):
        c = b["ch"][u]
        vals = [u, names[u], rep[b["kind"][u]], c["Lower division"], c["Upper division"], c["Graduate"],
                round(v[u] * b["fte"][u]), b["fte"][u], round(v[u]), i + 1, "yes" if u in aw else "no"]
        for j, val in enumerate(vals, 1):
            cl = ws.cell(row=5 + i, column=j, value=val)
            cl.font = bold if (u in aw and j in (1, 2, 11)) else body
            cl.border = thin
            if u in aw:
                cl.fill = nfill
            cl.number_format = {4: "#,##0", 5: "#,##0", 6: "#,##0", 7: "#,##0", 8: "#,##0", 9: "#,##0"}.get(j,
                                                                                                           "General")
            if j >= 4:
                cl.alignment = Alignment(horizontal="right")
    ws.freeze_panes = "C5"
    r0 = 5 + len(order) + 1
    for k, t in enumerate([
        "Six branch campuses' instruction expense is reported inside their parents' returns (PRCH_F 2). Fitted on the "
        "sixteen campuses that report alone, instruction costs $%.0f a lower-division, $%.0f an upper-division and "
        "$%.0f a graduate credit hour; each parent's reported instruction is split among the parent and its branches "
        "in proportion to the cost of the credit hours each taught in 2025-26, so the parent's total is kept." % tuple(
            coef),
        "Split by FTE students instead, every branch would carry its system's average and none would be in the lowest "
        "five; the branches teach mostly lower-division hours.",
    ]):
        cl = ws.cell(row=r0 + k, column=1, value=t)
        cl.font = Font(name="Calibri", size=9, color="5B6470")
        cl.alignment = Alignment(wrap_text=True, vertical="top")
        ws.merge_cells(start_row=r0 + k, start_column=1, end_row=r0 + k, end_column=11)
        ws.row_dimensions[r0 + k].height = 40

    cs = wb.create_sheet("Chart data")
    cs.append(["Campus", "Instruction per FTE ($)"])
    for u in order:
        cs.append([u, round(v[u])])
    ch = BarChart()
    ch.type = "bar"
    ch.title = "Fiscal 2026 instruction expense per FTE, lowest first: the five awards marked"
    ch.x_axis.title = "Dollars per FTE student"
    ch.x_axis.numFmt = "#,##0"
    ch.x_axis.delete = False
    ch.y_axis.delete = False
    ch.y_axis.scaling.orientation = "maxMin"
    ch.add_data(Reference(cs, min_col=2, min_row=1, max_row=len(order) + 1), titles_from_data=True)
    ch.set_categories(Reference(cs, min_col=1, min_row=2, max_row=len(order) + 1))
    ch.series[0].graphicalProperties = GraphicalProperties(solidFill=MUTED)
    for i, u in enumerate(order):
        if u in aw:
            pt = DataPoint(idx=i)
            pt.graphicalProperties = GraphicalProperties(solidFill=ACCENT)
            ch.series[0].dPt.append(pt)
    ch.legend = None
    ch.gapWidth = 40
    ch.height, ch.width = 14, 18
    ws.add_chart(ch, "A%d" % (r0 + 3))

    br = wb.create_sheet("Branches fall 2026")
    title(br, "The six branch campuses at the fall 2026 census", "FTE: undergraduate credit hours over 15 plus graduate "
                                                                 "over 12, a cross-listed course counted once; headcount: "
                                                                 "each student once, under either id.")
    head(br, 4, ["UNITID", "Campus", "Fall 2026 FTE", "Fall 2026 headcount"], [9, 40, 12, 12])
    kids = [u for u in b["ids"] if b["kind"][u] == "C"]
    for i, u in enumerate(kids):
        for j, (val, fm) in enumerate(((u, None), (names[u], None), (G["a"][u], "#,##0.0"), (G["bb"][u], "#,##0")), 1):
            cl = br.cell(row=5 + i, column=j, value=val)
            cl.font, cl.border = body, thin
            if fm:
                cl.number_format = fm
    for w in wb.worksheets:
        w.sheet_view.showGridLines = False
        w.page_setup.orientation = "landscape"
        w.page_setup.fitToWidth = 1
        w.page_setup.fitToHeight = 0
        w.sheet_properties.pageSetUpPr.fitToPage = True
    wb.save(path)


def figures(G):
    b = G["b"]
    d = B.per_fte(b, "fte_split")
    kids = [u for u in b["ids"] if b["kind"][u] == "C"]
    return {
        "call": {"awarded": G["aw"]},
        "ask_a": {u: "%.1f" % G["a"][u] for u in kids},
        "ask_b": {u: G["bb"][u] for u in kids},
        "default_path": {"awarded": B.awarded(b, d)},
        "per_fte_standalone": {u: int(round(G["v"][u])) for u in b["ids"] if b["kind"][u] == "S"},
        "conventions": {"years": [2025, 2026, 2027, 2028], "counts": [5, 6, 16, 21, 26], "unitids": [int(u) for u in b["ids"]], "divisors": [12, 15, 24, 30],
                        "grant_million": 4.5},
    }


def main(target, gdir, fig_path):
    os.makedirs(gdir, exist_ok=True)
    G = compute(target)
    write_xlsx(os.path.join(gdir, FILE), G, target)
    import postprocess as PP
    PP.normalize_ooxml(os.path.join(gdir, FILE), "Jeremy Cortez", "Jeremy Cortez", "2026-10-12T14:10:00Z",
                       "2026-10-14T20:35:00Z", excel=True, company=PP.COMPANY)
    with open(fig_path, "w") as fh:
        json.dump(figures(G), fh, indent=1, sort_keys=True)
        fh.write("\n")
    return G
