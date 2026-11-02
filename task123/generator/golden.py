"""The golden deliverables: the facilities manager's riser capacity workbook and the phase-loading chart."""
import os
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from common import save_workbook

TOWER_ORDER = ["A1", "A2", "A3", "A4", "A5", "A6", "B1", "B2", "B3", "B4", "B5", "B6", "C1", "C2", "C3", "C4", "C5", "C6"]


def r2(x):
    return float("%.2f" % x)


def workbook(E, path):
    C = E["call"]
    risers = C["risers"]
    wb = Workbook()
    ws = wb.active
    ws.title = "Works decision"
    bold = Font(bold=True)
    ws["A1"] = "Tannery Quay: rising mains needing works before the 2027 chargers and cooktop conversions"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = "Facilities manager's paper for the committee, November 2026. Basis: the electrification capacity standard adopted 14 October 2026."
    ws["A4"] = "Rising main"
    ws["B4"] = "Levels"
    ws["C4"] = "Rating per phase (A)"
    ws["D4"] = "Busiest phase, existing and added (kW)"
    ws["E4"] = "Share of rating (%)"
    for c in "ABCDE":
        ws[c + "4"].font = bold
        ws[c + "4"].alignment = Alignment(wrap_text=True, vertical="top")
    levels = {r["riser"]: "%d to %d" % (r["lo"], r["hi"]) for r in E["D"]["risers"]}
    row = 5
    for rid in [k for k in TOWER_ORDER if k in C["designated"]]:
        v = risers[rid]
        ws.cell(row, 1, rid)
        ws.cell(row, 2, levels[rid])
        ws.cell(row, 3, v["rating_a"])
        ws.cell(row, 4, round(v["kw"], 1))
        ws.cell(row, 5, int(round(v["share"])))
        row += 1
    row += 1
    ws.cell(row, 1, "Nearest the line without works").font = bold
    row += 1
    if C["nearest"]:
        v = risers[C["nearest"]]
        ws.cell(row, 1, C["nearest"])
        ws.cell(row, 2, levels[C["nearest"]])
        ws.cell(row, 3, v["rating_a"])
        ws.cell(row, 4, round(v["kw"], 1))
        ws.cell(row, 5, int(round(v["share"])))
    row += 2
    ws.cell(row, 1, "Works are needed where any phase's July 2026 evening demand plus its 2027 additions is above 80% of the main's rating per phase (230 V). "
                    "Each apartment's phase is the one its meter's hourly voltage moves with, 12 to 19 July; three-phase penthouses split equally.")
    ws.cell(row, 1).alignment = Alignment(wrap_text=True)
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=5)
    ws.row_dimensions[row].height = 42
    for c, w in zip("ABCDE", [14, 10, 12, 22, 12]):
        ws.column_dimensions[c].width = w

    ws2 = wb.create_sheet("Rising mains")
    hdr = ["Rising main", "Levels", "Rating per phase (A)", "Busiest phase, share of rating (%)", "July 2026 use (MWh)",
           "Charger requests lodged", "Time outside 216-253 V, week of 13 July (%)"]
    ws2.append(["All apartment rising mains, Towers A to C"])
    ws2.append([])
    ws2.append(hdr)
    for c in range(1, len(hdr) + 1):
        ws2.cell(3, c).font = bold
        ws2.cell(3, c).alignment = Alignment(wrap_text=True, vertical="top")
    for rid in TOWER_ORDER:
        v = risers[rid]
        ws2.append([rid, levels[rid], v["rating_a"], int(round(v["share"])), r2(E["july_mwh"][rid]),
                    int(E["requests"][rid]), r2(E["voltage_pct"][rid])])
    ws2.append([])
    ws2.append(["July use is each apartment's register movement over July (the exchange log carries meters changed in July). "
                "Requests count each car space once, B2 spaces lodged before the March 2025 re-marking carried to their new numbers, "
                "on the main of the apartment the space belongs to; visitor bays are not apartments' requests. "
                "Time outside the limits is each apartment's swell records joined into one span per excursion, in market time."])
    for c, w in zip("ABCDEFG", [12, 10, 12, 16, 14, 14, 18]):
        ws2.column_dimensions[c].width = w
    save_workbook(wb, path, "Kayla Hunt")


def chart(E, path):
    import matplotlib
    matplotlib.use("Agg")
    matplotlib.rcParams["svg.hashsalt"] = "tannery-quay-2026"
    matplotlib.rcParams["svg.fonttype"] = "none"
    import matplotlib.pyplot as plt
    C = E["call"]
    vals = [C["risers"][k]["share"] for k in TOWER_ORDER]
    colors = ["#b5462e" if k in C["designated"] else "#7f8c99" for k in TOWER_ORDER]
    fig, ax = plt.subplots(figsize=(9.0, 4.2), dpi=100)
    bars = ax.bar(TOWER_ORDER, vals, color=colors, width=0.7)
    ax.axhline(80, color="#222222", lw=1.2, ls="--")
    ax.text(17.45, 81.5, "80% limit", ha="right", va="bottom", fontsize=8.5)
    for b, v, k in zip(bars, vals, TOWER_ORDER):
        if k in C["designated"]:
            ax.text(b.get_x() + b.get_width() / 2, v + 1.2, "%d%%" % int(round(v)), ha="center", va="bottom", fontsize=8)
    ax.set_ylabel("Busiest phase, July 2026 evening demand plus 2027 additions\n(% of rising main rating per phase)", fontsize=8.5)
    ax.set_ylim(0, max(vals) * 1.12)
    words = {0: "No", 1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six", 7: "Seven", 8: "Eight", 9: "Nine"}
    n = len(C["designated"])
    ax.set_title("%s rising main%s over the limit once the 2027 chargers and cooktops are added" % (words.get(n, str(n)), "s go" if n != 1 else " goes"), fontsize=10.5, loc="left")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(labelsize=8.5)
    fig.tight_layout()
    fig.savefig(path, format="svg", metadata={"Date": None, "Creator": None})
    plt.close(fig)
    import re
    txt = open(path, encoding="utf-8").read()
    txt = re.sub(r"\s*<metadata>.*?</metadata>", "", txt, flags=re.S)
    txt = re.sub(r"<!--.*?-->\s*", "", txt, flags=re.S)
    txt = txt.replace('id="matplotlib.', 'id="')
    with open(path, "w", encoding="utf-8") as f:
        f.write(txt)


def write(E, outdir):
    os.makedirs(outdir, exist_ok=True)
    workbook(E, os.path.join(outdir, "riser_capacity_2027.xlsx"))
    chart(E, os.path.join(outdir, "riser_phase_loading_2027.svg"))
