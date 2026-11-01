"""The golden deliverables, written from target/ alone: the FY2028 cartage workbook and the loads-by-grade chart."""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from openpyxl import Workbook  # noqa: E402
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side  # noqa: E402
from openpyxl.utils import get_column_letter  # noqa: E402

import params as P  # noqa: E402
import results as R  # noqa: E402
from io_util import save_xlsx  # noqa: E402

XLSX = "matiri_fy2028_log_cartage_loads.xlsx"
PNG = "fy2028_loads_by_grade.svg"
GREEN = "2E5E3E"
THIN = Side(style="thin", color="B9C4B9")


def _hdr(ws, row, values, widths=None):
    for i, v in enumerate(values, start=1):
        c = ws.cell(row=row, column=i, value=v)
        c.font = Font(bold=True, color="FFFFFF", size=10)
        c.fill = PatternFill("solid", fgColor=GREEN)
        c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="left" if i == 1 else "center")
    if widths:
        for i, w in enumerate(widths, start=1):
            ws.column_dimensions[get_column_letter(i)].width = w


def workbook(F, path):
    wb = Workbook()
    ws = wb.active
    ws.title = "FY2028 loads"
    ws["A1"] = "Matiri Forest Products - FY2028 export cartage to Port Kowhai under the 50MAX route limits"
    ws["A1"].font = Font(bold=True, size=13, color=GREEN)
    ws["A2"] = ("FY2028 = 1 July 2027 to 30 June 2028. Plan: Board-approved harvest plan of 18 September 2026. Payloads: "
                "FY2026 port loads re-run on the same units under the FY2028 limits (planning basis 3.1, 3.2).")
    ws["A2"].font = Font(italic=True, size=9, color="555555")
    ws["A4"] = "Export log loads needed in FY2028 (nearest 100)"
    ws["A4"].font = Font(bold=True)
    ws["F4"] = F["total_100"]
    ws["F4"].number_format = "#,##0"
    ws["F4"].font = Font(bold=True, size=12, color=GREEN)
    _hdr(ws, 6, ["Grade", "Plan tonnes FY2028", "FY2026 port loads", "FY2026 average payload (t)",
                 "FY2028 average payload (t)", "FY2028 loads (nearest 50)", "FY2028 loads (unrounded)"],
         [16, 15, 13, 14, 14, 14, 14])
    r = 7
    for g in P.GRADE_ORDER:
        vals = [P.GRADES[g]["name"], F["plan"][g], F["fy26_by_grade"][g], round(F["avg_pay_fy26"][g], 2),
                round(F["avg_pay"][g], 2), F["grade_50"][g], round(F["loads"][g], 1)]
        fm = [None, "#,##0", "#,##0", "0.00", "0.00", "#,##0", "#,##0.0"]
        for j, (v, f) in enumerate(zip(vals, fm), start=1):
            c = ws.cell(row=r, column=j, value=v)
            if f:
                c.number_format = f
        r += 1
    ws.cell(row=r, column=1, value="All export grades").font = Font(bold=True)
    for j, (v, f) in enumerate([(F["plan_total"], "#,##0"), (F["fy26_loads"], "#,##0"), (None, None), (None, None),
                                (F["total_100"], "#,##0"), (round(F["total"], 1), "#,##0.0")], start=2):
        c = ws.cell(row=r, column=j, value=v)
        if f:
            c.number_format = f
        c.font = Font(bold=True)
        c.border = Border(top=THIN)
    ws.cell(row=r + 2, column=1, value=("The total is rounded from the unrounded sum, so it can differ by up to 50 from the sum "
                                        "of the rounded grade figures.")).font = Font(size=9, color="555555")
    ws.cell(row=r + 3, column=1, value=("A load's FY2028 payload is the lesser of its unit's FY2028 gross limit less tare and "
                                        "what its bunks hold of the grade's log length at the load's own density.")
            ).font = Font(size=9, color="555555")
    ws.freeze_panes = "A7"
    ws.sheet_view.showGridLines = False

    w2 = wb.create_sheet("Load payloads")
    cols = ["Ticket", "Weighed", "Grade", "Unit", "Rego", "50MAX", "Tare (t)", "Net FY2026 (t)", "JAS m3", "t per JAS m3",
            "Full bunks for the grade (JAS m3)", "FY2028 payload (t)"]
    _hdr(w2, 1, cols, [10, 11, 7, 8, 9, 7, 8, 10, 9, 9, 12, 11])
    w2.row_dimensions[1].height = 42
    fm = [None, "dd/mm/yyyy", None, None, None, None, "0.00", "0.00", "0.000", "0.000", "0.0", "0.00"]
    for i, x in enumerate(F["rows"], start=2):
        vals = [x["ticket"], x["date"], x["grade"], x["unit"], x["rego"], x["permit"], x["tare"], x["net"], x["jas"],
                round(x["dens"], 4), x["bunks"], round(x["new"], 3)]
        for j, (v, f) in enumerate(zip(vals, fm), start=1):
            c = w2.cell(row=i, column=j, value=v)
            if f:
                c.number_format = f
    w2.freeze_panes = "A2"
    w2.auto_filter.ref = "A1:L%d" % (len(F["rows"]) + 1)

    w3 = wb.create_sheet("Cartage FY2026")
    w3["A1"] = "FY2026 export cartage by the carrier whose unit hauled the load (NZD thousand, net of credit notes)"
    w3["A1"].font = Font(bold=True, color=GREEN)
    _hdr(w3, 3, ["Carrier", "Cartage (NZD thousand)"], [30, 16])
    r = 4
    for c in P.CARRIERS:
        w3.cell(row=r, column=1, value=P.CARRIERS[c])
        w3.cell(row=r, column=2, value=F["ask_a_k"][c]).number_format = "#,##0"
        r += 1
    w3.cell(row=r, column=1, value="All carriers").font = Font(bold=True)
    c = w3.cell(row=r, column=2, value=R.rhu(sum(F["ask_a"].values()) / 1e3, 0))
    c.number_format, c.font = "#,##0", Font(bold=True)
    w3.cell(row=r + 2, column=1, value=("Subcontracted units are billed under their head contractor's code; each line is "
                                        "credited to the unit's own carrier on the fleet register.")).font = Font(size=9, color="555555")

    w4 = wb.create_sheet("Mill deliveries")
    w4["A1"] = "FY2026 domestic deliveries by mill and quarter, tonnes, by the date the load crossed the mill weighbridge"
    w4["A1"].font = Font(bold=True, color=GREEN)
    _hdr(w4, 3, ["Mill"] + [R.Q_LABEL[q] for q in R.QUARTERS], [30, 14, 14, 14, 14])
    r = 4
    for m in P.MILLS:
        w4.cell(row=r, column=1, value=P.MILLS[m])
        for j, q in enumerate(R.QUARTERS, start=2):
            w4.cell(row=r, column=j, value=F["ask_b_10"][(m, q)]).number_format = "#,##0"
        r += 1
    w4.cell(row=r + 1, column=1, value=("Tonnes are gross less tare on the mill weighbridge for loads carrying a Matiri docket; "
                                        "rounded to the nearest 10 t.")).font = Font(size=9, color="555555")

    w5 = wb.create_sheet("Notes")
    notes = [("Loads", "One truck-and-trailer trip from a Matiri forest to Port Kowhai, weighed on the port weighbridge (planning basis 2.1)."),
             ("Linking", "Each port weighbridge ticket is matched to the scaling record of the same truck within the hour that follows it, giving the load's JAS volume."),
             ("Units", "Units are read from the fleet register by registration, including the previous registrations of the two units re-registered on 1 February 2026."),
             ("Limits", "50MAX permit units at 50 t gross from 1 July 2027; other units 44 t gross (RDC-2026-114; planning basis 3.2)."),
             ("Bunks", "The fleet register's full-bunk volume for the grade's cut length (export grade specification 2025)."),
             ("Rounding", "Half up. Total loads to the nearest 100, grade loads to the nearest 50, cartage to the nearest NZD thousand, mill tonnes to the nearest 10 t.")]
    w5.column_dimensions["A"].width = 12
    w5.column_dimensions["B"].width = 110
    w5["A1"], w5["B1"] = "Item", "Basis"
    w5["A1"].font = w5["B1"].font = Font(bold=True)
    for i, (k, v) in enumerate(notes, start=2):
        w5.cell(row=i, column=1, value=k).alignment = Alignment(vertical="top")
        w5.cell(row=i, column=2, value=v).alignment = Alignment(wrap_text=True, vertical="top")
    for w in (w3, w4):
        w.sheet_view.showGridLines = False
    save_xlsx(wb, path, "FY2028 export log cartage loads", "Logistics", "2026-10-20T01:10:00Z")


def chart(F, path):
    grades = P.GRADE_ORDER
    old = [F["fy26_by_grade"][g] for g in grades]
    new = [F["grade_50"][g] for g in grades]
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "svg.hashsalt": "task133", "svg.fonttype": "none"})
    fig, ax = plt.subplots(figsize=(7.2, 3.6), dpi=150)
    x = list(range(len(grades)))
    ax.bar([i - 0.19 for i in x], old, width=0.36, color="#A9B9AA", label="FY2026 port loads (recorded)", zorder=2)
    ax.bar([i + 0.19 for i in x], new, width=0.36, color="#2E5E3E", label="FY2028 loads needed (plan, 50MAX limits)", zorder=2)
    for i, v in enumerate(new):
        ax.text(i + 0.19, v + 90, f"{v:,.0f}", ha="center", va="bottom", fontsize=8, color="#222222")
    ax.set_xticks(x)
    ax.set_xticklabels([P.GRADES[g]["name"] for g in grades])
    ax.set_ylabel("Loads")
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, p: f"{v:,.0f}"))
    ax.grid(axis="y", color="#DDDDDD", linewidth=0.6, zorder=0)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.legend(frameon=False, fontsize=8, loc="upper right")
    ax.set_title("FY2028 needs %s export loads; the short grades fill their bunks before 50 tonnes" % f"{F['total_100']:,.0f}",
                 fontsize=9.5, loc="left", color="#2E5E3E")
    fig.tight_layout()
    fig.savefig(path, format="svg", metadata={"Date": None, "Creator": None})
    plt.close(fig)
    txt = open(path, encoding="utf-8").read().replace('id="matplotlib.axis_', 'id="axis_')
    assert "atplotlib" not in txt
    open(path, "w", encoding="utf-8").write(txt)


def write(tdir, out):
    os.makedirs(out, exist_ok=True)
    F = R.compute(tdir)
    workbook(F, os.path.join(out, XLSX))
    chart(F, os.path.join(out, PNG))
    return F


if __name__ == "__main__":
    write(sys.argv[1], sys.argv[2])
