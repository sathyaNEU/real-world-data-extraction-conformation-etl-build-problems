"""The golden deliverable, computed from the cut pack through bundle.py: the Assessment office's 2026-27 tutoring
designation workbook (each campus's share below Basic on the spring 2026 benchmark, the students it rests on, the fall
2025 benchmark and fall-to-winter growth), and generator/figures.json."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import bundle as B    # noqa: E402

FILE = "bellweather_2026-27_tutoring_designation.xlsx"
INK = "1B2430"
TEAL = "1F5A63"
PALE = "E4F0EF"
MUTED = "A7B3B1"


def compute(target):
    b = B.load(target)
    gold = B.spring(b, "golden")
    vend = B.spring(b, "vendor")
    sh = B.shares(b, gold)
    return {"b": b, "gold": gold, "vend": vend, "sh": sh, "shv": B.shares(b, vend), "des": B.designate(b, gold),
            "a": B.ask_a(b), "bb": B.ask_b(b)}


def write_xlsx(path, G):
    import openpyxl
    from openpyxl.chart import BarChart, LineChart, Reference
    from openpyxl.chart.marker import DataPoint
    from openpyxl.chart.shapes import GraphicalProperties
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    from openpyxl.utils import get_column_letter
    b = G["b"]
    wb = openpyxl.Workbook()
    hdr = Font(name="Calibri", bold=True, color="FFFFFF", size=10)
    hfill = PatternFill("solid", fgColor=TEAL)
    body = Font(name="Calibri", size=10, color=INK)
    bold = Font(name="Calibri", size=10, color=INK, bold=True)
    thin = Border(bottom=Side(style="thin", color="C3CDCB"))
    dfill = PatternFill("solid", fgColor=PALE)

    def head(ws, row, cols, widths):
        for i, (h, w) in enumerate(zip(cols, widths), 1):
            c = ws.cell(row=row, column=i, value=h)
            c.font, c.fill = hdr, hfill
            c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="left" if i == 1 else "right")
            ws.column_dimensions[get_column_letter(i)].width = w
        ws.row_dimensions[row].height = 32

    def title(ws, t, sub):
        ws["A1"] = t
        ws["A1"].font = Font(name="Calibri", size=13, bold=True, color=INK)
        ws["A2"] = sub
        ws["A2"].font = Font(name="Calibri", size=9, italic=True, color="5B6470")

    n, below, rapid = {}, {}, {}
    for s, v in G["gold"].items():
        c = b["spring"][s]["campus_id"]
        n[c] = n.get(c, 0) + 1
        below[c] = below.get(c, 0) + (v < B.BASIC)
        rapid[c] = rapid.get(c, 0) + any(x[3] < B.RAPID for x in b["resp"][s])
    ws = wb.active
    ws.title = "Designation"
    des = G["des"]
    title(ws, "%d campuses are designated for 2026-27 tutoring: %s" % (len(des), ", ".join(des)),
          "Spring 2026 benchmark; each student's scale score estimated by maximum likelihood on Quantilis's bank from "
          "the responses given with effort (responses in under five seconds treated as not administered).")
    head(ws, 4, ["Campus", "Students tested", "Students with rapid responses", "Below Basic", "Share below Basic",
                 "Designated"], [10, 12, 14, 11, 12, 11])
    for i, c in enumerate(b["campuses"]):
        vals = [c, n[c], rapid[c], below[c], round(100 * G["sh"][c], 1), "yes" if c in des else "no"]
        for j, v in enumerate(vals, 1):
            cell = ws.cell(row=5 + i, column=j, value=v)
            cell.font = bold if (c in des and j in (1, 6)) else body
            cell.border = thin
            if c in des:
                cell.fill = dfill
            if j == 5:
                cell.number_format = "0.0"
            elif j in (2, 3, 4):
                cell.number_format = "#,##0"
            if j >= 2:
                cell.alignment = Alignment(horizontal="right")
    ws.freeze_panes = "B5"
    r0 = 5 + len(b["campuses"]) + 1
    for k, t in enumerate([
        "The benchmark is untimed and no engaged response in the spring sessions took under 7.5 seconds; responses "
        "given in under 3 seconds were right a quarter of the time whatever the item's difficulty, the rate of a blind "
        "guess on four options, so they carry nothing about the student's achievement and are scored as not "
        "administered. Every student tested keeps a score.",
        "The 35 per cent line is applied to the unrounded share; shares are shown to one decimal.",
    ]):
        cell = ws.cell(row=r0 + k, column=1, value=t)
        cell.font = Font(name="Calibri", size=9, color="5B6470")
        cell.alignment = Alignment(wrap_text=True, vertical="top")
        ws.merge_cells(start_row=r0 + k, start_column=1, end_row=r0 + k, end_column=6)
        ws.row_dimensions[r0 + k].height = 48
    cs = wb.create_sheet("Chart data")
    cs.append(["Campus", "Share below Basic (%)", "35% line"])
    for c in b["campuses"]:
        cs.append([c, round(100 * G["sh"][c], 1), 35.0])
    ch = BarChart()
    ch.type = "col"
    ch.title = "Spring 2026 share of students below Basic, against the 35% line"
    ch.y_axis.title = "Per cent of students tested"
    ch.y_axis.numFmt = "0"
    ch.y_axis.scaling.min = 0
    ch.y_axis.delete = False
    ch.x_axis.delete = False
    ch.x_axis.tickLblSkip = 1
    ch.add_data(Reference(cs, min_col=2, min_row=1, max_row=len(b["campuses"]) + 1), titles_from_data=True)
    ch.set_categories(Reference(cs, min_col=1, min_row=2, max_row=len(b["campuses"]) + 1))
    s0 = ch.series[0]
    s0.graphicalProperties = GraphicalProperties(solidFill=MUTED)
    for i, c in enumerate(b["campuses"]):
        if c in des:
            pt = DataPoint(idx=i)
            pt.graphicalProperties = GraphicalProperties(solidFill=TEAL)
            s0.dPt.append(pt)
    ln = LineChart()
    ln.add_data(Reference(cs, min_col=3, min_row=1, max_row=len(b["campuses"]) + 1), titles_from_data=True)
    ln.series[0].graphicalProperties.line.solidFill = INK
    ln.series[0].graphicalProperties.line.dashStyle = "dash"
    ln.series[0].marker.symbol = "none"
    ch += ln
    ch.legend.position = "b"
    ch.height, ch.width = 10, 22
    ws.add_chart(ch, "A%d" % (r0 + 3))

    fa = wb.create_sheet("Fall 2025")
    title(fa, "Fall 2025 benchmark by campus", "Each student once: a restarted session's later administration is the "
                                               "student's score, temporary ids resolved through the register.")
    head(fa, 4, ["Campus", "Students tested", "Share at or above Proficient (%)"], [10, 14, 18])
    for i, c in enumerate(b["campuses"]):
        for j, (v, fm) in enumerate(((c, None), (G["a"][c][0], "#,##0"), (round(G["a"][c][1], 1), "0.0")), 1):
            cell = fa.cell(row=5 + i, column=j, value=v)
            cell.font, cell.border = body, thin
            if fm:
                cell.number_format = fm
    gr = wb.create_sheet("Fall to winter")
    title(gr, "Fall to winter growth by winter campus", "Students tested in both windows, linked across the January "
                                                        "2026 id migration (the crosswalk, then name and birth date).")
    head(gr, 4, ["Campus", "Students in both", "Mean growth (scale points)"], [10, 14, 16])
    for i, c in enumerate(b["campuses"]):
        for j, (v, fm) in enumerate(((c, None), (G["bb"][c][0], "#,##0"), (round(G["bb"][c][1], 1), "0.0")), 1):
            cell = gr.cell(row=5 + i, column=j, value=v)
            cell.font, cell.border = body, thin
            if fm:
                cell.number_format = fm
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
        "call": {"designated": G["des"]},
        "below_basic_pct": {c: "%.1f" % (100 * G["sh"][c]) for c in b["campuses"]},
        "ask_a": {c: {"tested": G["a"][c][0], "proficient_pct": "%.1f" % G["a"][c][1]} for c in b["campuses"]},
        "ask_b": {c: {"students": G["bb"][c][0], "growth": "%.1f" % G["bb"][c][1]} for c in b["campuses"]},
        "default_path": {"designated": B.designate(b, G["vend"]),
                         "below_basic_pct": {c: "%.1f" % (100 * G["shv"][c]) for c in b["campuses"]}},
        "conventions": {"line_pct": 35, "basic": 470, "proficient": 520, "items": 40, "seconds": [3, 5, 7.5], "scale": [500, 40, 350, 650],
                        "years": [2025, 2026, 2027], "counts": [2, 4, 14]},
    }


def main(target, gdir, fig_path):
    os.makedirs(gdir, exist_ok=True)
    G = compute(target)
    write_xlsx(os.path.join(gdir, FILE), G)
    import postprocess as PP
    PP.normalize_ooxml(os.path.join(gdir, FILE), "Sabrina Santos", "Sabrina Santos", "2026-10-06T15:10:00Z",
                       "2026-10-07T19:42:00Z", excel=True, company="Bellweather Academies")
    with open(fig_path, "w") as fh:
        json.dump(figures(G), fh, indent=1, sort_keys=True)
        fh.write("\n")
    return G
