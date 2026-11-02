"""The golden deliverables: the 2027 budget gold workbook and the low-grade stockpile chart."""
import os

from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side

from io_util import save_xlsx

BOOK = "kessock_2027_budget_gold.xlsx"
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
    ws["A1"] = "Kessock Lake Mine - 2027 budget gold (ore mined, grade-control basis)"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = "Ore cut-off 0.90 g/t from 1 January 2027; mine plan 2027 v3 schedule; prepared 24 November 2026"
    ws["A2"].font = Font(italic=True, size=9)
    _head(ws, 4, ["", "Tonnes (Mt)", "Grade (g/t Au)", "Gold (oz)"], [46, 14, 15, 14])
    rows = [("2027 budget gold, ore mined (grade control)", F["ore_mt_1dp"], F["ore_grade_1dp"], F["budget_oz"]),
            ("Plan basis, resource model 2026R at 0.90 g/t", F["plan_mt_2dp"], F["plan_grade_2dp"], F["plan_oz_100"])]
    for r, row in enumerate(rows, start=5):
        for c, v in enumerate(row, start=1):
            cell = ws.cell(row=r, column=c, value=v)
            if c == 2:
                cell.number_format = "0.0" if r == 5 else "0.00"
            if c == 3:
                cell.number_format = "0.0" if r == 5 else "0.00"
            if c == 4:
                cell.number_format = "#,##0"
        if r == 5:
            for c in range(1, 5):
                ws.cell(row=r, column=c).font = Font(bold=True)
    ws["A8"] = "Grade control against the resource model, Jan 2023 to Oct 2026 (gold, each side at its own cut)"
    ws["A8"].font = Font(bold=True)
    _head(ws, 9, ["Cut-off", "Gold factor", "", ""])
    ws["A10"], ws["B10"] = "0.50 g/t (reconciliation reports)", F["f05_2dp"]
    ws["A11"], ws["B11"] = "0.90 g/t (record re-cut)", F["f09_1dp"]
    ws["B10"].number_format = "0.00"
    ws["B11"].number_format = "0.0"
    ws["A13"] = ("Budget gold is the plan's Schedule blocks taken through the record's grade-control-to-model ratios, "
                 "gold kept where grade control reads 0.90 g/t or more; rounded to the nearest 10,000 oz.")
    ws["A13"].alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells("A13:D14")
    ws.row_dimensions[13].height = 30

    s = wb.create_sheet("LG stockpile")
    _head(s, 1, ["Date", "Tonnes", "Contained gold (oz)"], [22, 14, 20])
    for r, (lab, t, oz) in enumerate(F["stock_rows"], start=2):
        s.cell(row=r, column=1, value=lab)
        s.cell(row=r, column=2, value=t).number_format = "#,##0"
        s.cell(row=r, column=3, value=oz).number_format = "#,##0"
    s.cell(row=7, column=1, value="Opening: 2022 year-end survey; additions: dispatch hauls at each truck's nominal "
                                  "payload, local time.").font = Font(italic=True, size=9)

    h = wb.create_sheet("Ball mill hours")
    _head(h, 1, ["Quarter (local time)", "Hours run"], [22, 12])
    for r, (lab, v) in enumerate(F["hours_rows"], start=2):
        h.cell(row=r, column=1, value=lab)
        h.cell(row=r, column=2, value=v).number_format = "#,##0"

    g = wb.create_sheet("Fine gold poured")
    _head(g, 1, ["Quarter poured (local time)", "Fine gold (oz)"], [26, 14])
    for r, (lab, v) in enumerate(F["fine_rows"], start=2):
        g.cell(row=r, column=1, value=lab)
        g.cell(row=r, column=2, value=v).number_format = "#,##0"
    save_xlsx(wb, path, "2027 budget gold", "Brent Peck", "2026-11-24T15:40:00Z")


def chart(path, F):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams["svg.hashsalt"] = "kessock-lgsp"
    plt.rcParams["font.family"] = "DejaVu Sans"
    labels = [r[0] for r in F["stock_rows"]]
    tonnes = [r[1] / 1e6 for r in F["stock_rows"]]
    gold = [r[2] for r in F["stock_rows"]]
    fig, ax = plt.subplots(figsize=(7.2, 4.2), dpi=100)
    bars = ax.bar(range(len(labels)), tonnes, color="#4F6D8F", width=0.58)
    for b, t, oz in zip(bars, tonnes, gold):
        ax.text(b.get_x() + b.get_width() / 2, t + 0.12, "%.2f Mt\n%s oz" % (t, format(oz, ",")), ha="center",
                va="bottom", fontsize=8.5)
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, fontsize=9)
    ax.set_ylabel("Million tonnes", fontsize=9)
    ax.set_ylim(0, max(tonnes) * 1.25)
    ax.set_title("Low-grade stockpile (LGSP): tonnes and contained gold", fontsize=10.5, loc="left")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(axis="y", labelsize=8.5)
    fig.tight_layout()
    fig.savefig(path, format="svg", metadata={"Date": None, "Creator": None})
    plt.close(fig)


def build(out, F):
    os.makedirs(out, exist_ok=True)
    workbook(os.path.join(out, BOOK), F)
    chart(os.path.join(out, CHART), F)
