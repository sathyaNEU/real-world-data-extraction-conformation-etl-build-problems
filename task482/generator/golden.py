"""The golden deliverable, computed from the cut pack through bundle.py: the Brannagh Statistics Office's workbook
for the Minister (each area's residential property price change, year to September 2026 on the year before, the
time effect of a hedonic regression on the dwellings' type, floor area, new-dwelling status and electoral division;
the areas over 8 per cent; each area's residential purchases and the total paid in the year to September 2026), and
generator/figures.json."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import bundle as B    # noqa: E402

FILE = "bso_area_property_price_change_2026.xlsx"
INK = "1B2430"
GREEN = "2C5A3F"
PALE = "E7EFE9"
MUTED = "A3ACB8"
ACCENT = "B4452F"
NAMES = {"KB": "Kilbrannagh", "AC": "Ardcullen", "LF": "Lisnafeen", "RG": "Rathgowan", "TV": "Tullyvane",
         "MR": "Moyrath", "GS": "Glenaskin", "DM": "Dunmarra", "CT": "Clonteevan", "IR": "Innishrue",
         "CV": "Carrigvore", "KF": "Knockfeerin", "BM": "Ballymarne", "CL": "Corlespie", "AV": "Annaghvale",
         "DS": "Drumshallon"}


def compute(target):
    b = B.load(target)
    c = B.change(b, "golden")
    return {"b": b, "c": c, "d": B.designated(b, "golden"), "a": B.ask(b), "n": counts(b)}


def counts(b):
    out = {}
    for code in b["areas"]:
        ss = B._market(b, code)
        out[code] = (sum(1 for s in ss if s["date"] < B.Y2[0]), sum(1 for s in ss if s["date"] >= B.Y2[0]))
    return out


def write_xlsx(path, G):
    import openpyxl
    from openpyxl.chart import BarChart, Reference
    from openpyxl.chart.series import DataPoint
    from openpyxl.chart.shapes import GraphicalProperties
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    from openpyxl.utils import get_column_letter
    b, c, d = G["b"], G["c"], G["d"]
    order = sorted(b["areas"], key=lambda k: -c[k])
    wb = openpyxl.Workbook()
    hdr = Font(name="Calibri", bold=True, color="FFFFFF", size=10)
    hfill = PatternFill("solid", fgColor=GREEN)
    body = Font(name="Calibri", size=10, color=INK)
    bold = Font(name="Calibri", size=10, color=INK, bold=True)
    thin = Border(bottom=Side(style="thin", color="C3CAD3"))
    nfill = PatternFill("solid", fgColor=PALE)

    def head(ws, row, cols, widths):
        for i, (h, w) in enumerate(zip(cols, widths), 1):
            x = ws.cell(row=row, column=i, value=h)
            x.font, x.fill = hdr, hfill
            x.alignment = Alignment(wrap_text=True, vertical="center", horizontal="left" if i <= 2 else "right")
            ws.column_dimensions[get_column_letter(i)].width = w
        ws.row_dimensions[row].height = 44

    def title(ws, t, sub):
        ws["A1"] = t
        ws["A1"].font = Font(name="Calibri", size=13, bold=True, color=INK)
        ws["A2"] = sub
        ws["A2"].font = Font(name="Calibri", size=9, italic=True, color="5B6470")

    ws = wb.active
    ws.title = "Designation"
    title(ws, "%d of 16 areas rose more than 8 per cent and are designated: %s" % (
        len(d), ", ".join(NAMES[k] for k in sorted(d, key=lambda k: NAMES[k]))),
          "Residential property price change, year to September 2026 on the year to September 2025, for a dwelling of "
          "unchanged type, floor area, newness and electoral division (hedonic time effect), sales at full market price.")
    head(ws, 4, ["LA code", "Local authority area", "Sales, year to Sep 2025", "Sales, year to Sep 2026",
                 "Price change (%)", "Rapid price growth area"], [9, 20, 13, 13, 12, 13])
    for i, k in enumerate(order):
        vals = [k, NAMES[k], G["n"][k][0], G["n"][k][1], round(c[k], 1), "yes" if k in d else "no"]
        for j, v in enumerate(vals, 1):
            x = ws.cell(row=5 + i, column=j, value=v)
            x.font = bold if (k in d and j in (1, 2, 6)) else body
            x.border = thin
            if k in d:
                x.fill = nfill
            if j in (3, 4):
                x.number_format = "#,##0"
            elif j == 5:
                x.number_format = "0.0"
            if j >= 3:
                x.alignment = Alignment(horizontal="right")
    ws.freeze_panes = "C5"
    r0 = 5 + len(order) + 1
    for n, t in enumerate([
        "Each area's change is the year effect of a regression of the log price (including VAT) on the dwelling's type, "
        "log floor area, new-dwelling status and electoral division, fitted to the area's sales at full market price "
        "in the two years, so the homes that sold in each year are compared like with like.",
        "A sale counts in the year of its date of sale. Filings made in both systems from 1 to 10 October 2025 are "
        "counted once; the old system's VAT-exclusive prices of new dwellings are grossed up at 13.5 per cent.",
    ]):
        x = ws.cell(row=r0 + n, column=1, value=t)
        x.font = Font(name="Calibri", size=9, color="5B6470")
        x.alignment = Alignment(wrap_text=True, vertical="top")
        ws.merge_cells(start_row=r0 + n, start_column=1, end_row=r0 + n, end_column=6)
        ws.row_dimensions[r0 + n].height = 40

    cs = wb.create_sheet("Chart data")
    cs.append(["Area", "Price change (%)", "Line (%)"])
    for k in order:
        cs.append([NAMES[k], round(c[k], 1), B.LINE])
    bc = BarChart()
    bc.type = "bar"
    bc.title = "Price change by area, year to September 2026, against the 8 per cent line"
    bc.x_axis.title = None
    bc.y_axis.title = "Per cent"
    bc.y_axis.delete = False
    bc.x_axis.delete = False
    bc.x_axis.scaling.orientation = "maxMin"
    bc.add_data(Reference(cs, min_col=2, min_row=1, max_row=len(order) + 1), titles_from_data=True)
    bc.set_categories(Reference(cs, min_col=1, min_row=2, max_row=len(order) + 1))
    bc.series[0].graphicalProperties = GraphicalProperties(solidFill=MUTED)
    for i, k in enumerate(order):
        if k in d:
            pt = DataPoint(idx=i)
            pt.graphicalProperties = GraphicalProperties(solidFill=ACCENT)
            bc.series[0].dPt.append(pt)
    bc.legend = None
    bc.height, bc.width = 11, 20
    ws.add_chart(bc, "H4")

    q = wb.create_sheet("Transactions 2025-26")
    title(q, "Residential purchases, year to September 2026", "By date of sale; every purchase counts whether or not "
          "at full market price; a block of apartments bought in one purchase counts once, at its one consideration.")
    head(q, 4, ["LA code", "Local authority area", "Purchases", "Total paid incl. VAT (EUR)"], [9, 20, 12, 22])
    for i, k in enumerate(sorted(b["areas"], key=lambda k: NAMES[k])):
        for j, (v, fm) in enumerate(((k, None), (NAMES[k], None), (G["a"][k][0], "#,##0"),
                                     (int(round(G["a"][k][1])), "#,##0")), 1):
            x = q.cell(row=5 + i, column=j, value=v)
            x.font, x.border = body, thin
            if fm:
                x.number_format = fm
                x.alignment = Alignment(horizontal="right")
    tr = 5 + len(b["areas"])
    q.cell(row=tr, column=2, value="All areas").font = bold
    for j, v in ((3, sum(G["a"][k][0] for k in b["areas"])), (4, int(round(sum(G["a"][k][1] for k in b["areas"]))))):
        x = q.cell(row=tr, column=j, value=v)
        x.font, x.number_format = bold, "#,##0"
        x.alignment = Alignment(horizontal="right")
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
        "call": {"designated": G["d"]},
        "change": {k: round(G["c"][k], 1) for k in b["areas"]},
        "ask": {k: {"purchases": G["a"][k][0], "paid": int(round(G["a"][k][1]))} for k in b["areas"]},
        "default_path": {"designated": B.designated(b, "type_weighted")},
        "conventions": {"line": 8, "vat": 13.5, "years": [2019, 2024, 2025, 2026, 2027], "counts": [16],
                        "dates": [1, 10, 30]},
    }


def main(target, gdir, fig_path):
    os.makedirs(gdir, exist_ok=True)
    G = compute(target)
    write_xlsx(os.path.join(gdir, FILE), G)
    import postprocess as PP
    PP.normalize_ooxml(os.path.join(gdir, FILE), "Clare McEntee", "Clare McEntee", "2026-10-20T09:10:00Z",
                       "2026-10-22T15:35:00Z", excel=True, company=PP.COMPANY)
    with open(fig_path, "w") as fh:
        json.dump(figures(G), fh, indent=1, sort_keys=True)
        fh.write("\n")
    return G
