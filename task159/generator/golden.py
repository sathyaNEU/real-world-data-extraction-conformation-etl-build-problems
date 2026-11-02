"""The golden deliverables: the 2027 budget gold workbook and the low-grade stockpile chart."""
import os

from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side

from io_util import save_xlsx

BOOK = "kelvanna_2027_budget_gold.xlsx"
CHART = "lg_stockpile_2023-2026.svg"

THIN = Side(style="thin", color="A6A6A6")
HEAD = PatternFill("solid", fgColor="DDE4EE")


def _head(ws, row, labels, widths=None):
    for c, lab in enumerate(labels, start=1):
        cell = ws.cell(row=row, column=c, value=lab)
        cell.font = Font(bold=True)
        cell.fill = HEAD
        cell.border = Border(bottom=THIN)
        cell.alignment = Alignment(wrap_text=True, vertical="bottom")
    if widths:
        for c, w in enumerate(widths, start=1):
            ws.column_dimensions[chr(64 + c)].width = w


def workbook(path, F):
    wb = Workbook()
    ws = wb.active
    ws.title = "Budget gold"
    ws["A1"] = "2027 budget gold: %s oz in %s t of ore on grade control" % (format(F["budget_oz"], ","),
                                                                         format(F["ore_t_100k"], ","))
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = "Kelvanna Lake Mine, ore cut-off 0.90 g/t from 1 January 2027; mine plan 2027 v3 Schedule sheet"
    ws["A2"].font = Font(italic=True, size=9)
    _head(ws, 4, ["Basis", "Ore (t)", "Gold (oz)"], [50, 14, 14])
    rows = [("Budget: ore mined in 2027, grade-control grades", F["ore_t_100k"], F["budget_oz"]),
            ("Plan: resource model 2026R estimates at 0.90 g/t", F["plan_t_10k"], F["plan_oz_100"])]
    for r, row in enumerate(rows, start=5):
        for c, v in enumerate(row, start=1):
            cell = ws.cell(row=r, column=c, value=v)
            if c >= 2:
                cell.number_format = "#,##0"
                cell.alignment = Alignment(horizontal="right")
        if r == 5:
            for c in range(1, 4):
                ws.cell(row=r, column=c).font = Font(bold=True)
    ws["A8"] = "Grade control's gold over the model's, January 2023 to October 2026 (each side cut on its own grade)"
    ws["A8"].font = Font(bold=True)
    _head(ws, 9, ["Cut-off", "Gold factor", ""])
    ws["A10"], ws["B10"] = "0.50 g/t (as in the monthly reconciliation reports)", F["f05_2dp"]
    ws["A11"], ws["B11"] = "0.90 g/t (the paired record re-cut)", F["f09_1dp"]
    ws["B10"].number_format = "0.00"
    ws["B11"].number_format = "0.0"
    ws["A13"] = "Source: blast-hole assays laid into the 2026R model's blocks; definitions on the Notes sheet."
    ws["A13"].font = Font(italic=True, size=9)
    ws.freeze_panes = "A5"

    s = wb.create_sheet("LG stockpile")
    _head(s, 1, ["Date", "Tonnes", "Contained gold (oz)"], [22, 14, 20])
    for r, (lab, t, oz) in enumerate(F["stock_rows"], start=2):
        s.cell(row=r, column=1, value=lab)
        s.cell(row=r, column=2, value=t).number_format = "#,##0"
        s.cell(row=r, column=3, value=oz).number_format = "#,##0"
    s.cell(row=7, column=1, value="Source: 2022 year-end survey balance plus dispatch hauls to LGSP at each hauling "
                                  "truck's nominal payload.").font = Font(italic=True, size=9)
    s.freeze_panes = "A2"

    h = wb.create_sheet("Ball mill hours")
    _head(h, 1, ["Quarter", "Hours run"], [14, 12])
    for r, (lab, v) in enumerate(F["hours_rows"], start=2):
        h.cell(row=r, column=1, value=lab)
        h.cell(row=r, column=2, value=v).number_format = "#,##0"
    h.cell(row=10, column=1, value="Source: DCS run state of BM-101 with the shutdown work orders.").font = \
        Font(italic=True, size=9)
    h.freeze_panes = "A2"

    g = wb.create_sheet("Fine gold poured")
    _head(g, 1, ["Quarter poured", "Fine gold (oz)"], [16, 14])
    for r, (lab, v) in enumerate(F["fine_rows"], start=2):
        g.cell(row=r, column=1, value=lab)
        g.cell(row=r, column=2, value=v).number_format = "#,##0"
    g.cell(row=10, column=1, value="Source: refinery outturn statements against the gold room bar register.").font = \
        Font(italic=True, size=9)
    g.freeze_panes = "A2"

    n = wb.create_sheet("Notes")
    notes = [("Budget gold", "Gold contained in the ore mined in calendar 2027, troy ounces, on grade-control grades and "
                             "the model's block tonnages (budget basis memo MP-2026-118, 12 November 2026)."),
             ("Ore", "A Main Zone block whose grade-control grade, the average of its primary blast-hole assays, is "
                     "0.90 g/t or more. Field duplicates and laboratory control samples are excluded."),
             ("Volume", "Every Main Zone block on the plan's Schedule sheet, ore and waste alike; waste outside the "
                        "Main Zone carries no gold."),
             ("Record", "Blast holes and survey depletion to 31 October 2026; resource model 2026R; plan v3 of "
                        "9 November 2026."),
             ("Time", "Quarters, year ends and pour dates in local time (Eastern)."),
             ("Rounding", "Budget gold to the nearest 10,000 oz and ore to the nearest 100,000 t; stockpile tonnes to "
                          "the nearest 1,000 t; other gold to the nearest 100 oz; hours to the nearest hour.")]
    _head(n, 1, ["Item", "Definition"], [14, 100])
    for r, (a, b) in enumerate(notes, start=2):
        n.cell(row=r, column=1, value=a).font = Font(bold=True)
        n.cell(row=r, column=2, value=b).alignment = Alignment(wrap_text=True, vertical="top")
        n.row_dimensions[r].height = 30
    save_xlsx(wb, path, "2027 budget gold", "Brent Peck", "2026-11-24T15:40:00Z")


def chart(path, F):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams["svg.hashsalt"] = "kelvanna-lgsp"
    plt.rcParams["font.family"] = "DejaVu Sans"
    labels = [r[0] for r in F["stock_rows"]]
    tonnes = [r[1] / 1e6 for r in F["stock_rows"]]
    gold = [r[2] for r in F["stock_rows"]]
    fig, ax = plt.subplots(figsize=(7.4, 4.3), dpi=100)
    bars = ax.bar(range(len(labels)), tonnes, color="#4F6D8F", width=0.56)
    for b, row in zip(bars, F["stock_rows"]):
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.15, "%s t\n%s oz" % (format(row[1], ","),
                format(row[2], ",")), ha="center", va="bottom", fontsize=8.5, color="#222222")
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, fontsize=9)
    ax.set_ylabel("Tonnes (millions)", fontsize=9, color="#444444")
    ax.set_ylim(0, max(tonnes) * 1.28)
    ax.set_title("The low-grade stockpile has grown every year since the 2022 survey", fontsize=10.5, loc="left")
    ax.yaxis.grid(True, color="#E3E3E3", linewidth=0.8)
    ax.set_axisbelow(True)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.tick_params(axis="y", labelsize=8.5, length=0, colors="#444444")
    ax.text(0, -0.17, "LGSP, local time; tonnes at each hauling truck's nominal payload, contained gold at the dig "
                      "polygon's grade-control grade.", transform=ax.transAxes, fontsize=7.5, color="#666666")
    fig.tight_layout()
    fig.savefig(path, format="svg", metadata={"Date": None, "Creator": None})
    plt.close(fig)
    import re
    svg = open(path, encoding="utf-8").read()
    svg = re.sub(r'id="matplotlib\.', 'id="', svg)
    svg = re.sub(r"<!--[^>]*[Mm]atplotlib[^>]*-->\n?", "", svg)
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)


def build(out, F):
    os.makedirs(out, exist_ok=True)
    workbook(os.path.join(out, BOOK), F)
    chart(os.path.join(out, CHART), F)
