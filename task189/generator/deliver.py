"""The two deliverables: the authority's return workbook and the chart that carries the decision."""
import os

import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["svg.hashsalt"] = "task189"
matplotlib.rcParams["font.family"] = "sans-serif"
matplotlib.rcParams["font.sans-serif"] = ["Arial", "Helvetica", "DejaVu Sans"]
import matplotlib.pyplot as plt
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

import world as W

THIN = Side(style="thin", color="8A8A8A")
BOX = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
HEAD = PatternFill("solid", fgColor="E4E7DF")


def workbook(path, g, rg_names):
    wb = Workbook()
    ws = wb.active
    ws.title = "Return 2025-26"
    ws["A1"] = "%s" % W.AUTHORITY
    ws["A1"].font = Font(bold=True, size=13)
    ws["A2"] = ("Annual return to the %s under regulation 7.6, reporting year 2025/26, "
                "1 April 2025 to 31 March 2026" % W.REGULATOR)
    ws["A3"] = ("Listed substances: MCPA, standard 0.05 ug/l as an annual average, and ortho-phosphate as P "
                "(Schedule 2).")
    ws["A4"] = "Return due 30 November 2026. Prepared from the laboratory export of 16 November 2026."
    for r in (2, 3, 4):
        ws.cell(row=r, column=1).font = Font(size=9)
    ws["A5"] = ("Ortho-phosphate as P: compliance samples with an approved result in the year, and "
                "those results below the reporting limit of the method used.")
    ws["A5"].font = Font(size=9)
    hdr = ["Water body code", "Water body", "MCPA assessment",
           "Ortho-phosphate compliance samples", "Ortho-phosphate results below the reporting limit"]
    for i, h in enumerate(hdr, start=1):
        c = ws.cell(row=6, column=i, value=h)
        c.font = Font(bold=True)
        c.fill = HEAD
        c.border = BOX
        c.alignment = Alignment(wrap_text=True, vertical="bottom", horizontal="center")
    row = 7
    for code, o in sorted(g["assess"].items(), key=lambda kv: kv[1]["name"]):
        n, nd = g["w"][o["name"]]
        vals = [code, o["name"], "non-compliant" if o["verdict"] == "non-compliant" else "compliant",
                n, nd]
        for i, v in enumerate(vals, start=1):
            c = ws.cell(row=row, column=i, value=v)
            c.border = BOX
            if i >= 3:
                c.alignment = Alignment(horizontal="center")
            if i == 3 and v == "non-compliant":
                c.font = Font(bold=True)
        row += 1
    ws.cell(row=row + 1, column=1, value="Water bodies assessed as non-compliant for MCPA").font = \
        Font(bold=True)
    c = ws.cell(row=row + 1, column=3, value=g["count"])
    c.font = Font(bold=True)
    c.alignment = Alignment(horizontal="center")
    ws.cell(row=row + 2, column=1,
            value="Non-compliant water bodies: " + ", ".join(g["non_compliant"])).font = Font(size=9)
    ws.cell(row=row + 4, column=1, value=(
        "Three quarters of the MCPA results in the year were reported below a reporting limit, and "
        "the two methods in the programme report to 0.005 ug/l and 0.10 ug/l. The averages behind "
        "this return were estimated from the results as reported, each at its own reporting limit, "
        "and no value was substituted for a result below a limit.")).font = Font(size=9, italic=True)
    ws.cell(row=row + 5, column=1, value="Prepared by %s, catchment monitoring"
            % W.PEOPLE["monitoring_lead"]).font = Font(size=9)
    for col, wd in zip("ABCDE", [20, 22, 16, 18, 20]):
        ws.column_dimensions[col].width = wd
    ws.row_dimensions[6].height = 42
    ws.freeze_panes = "C7"
    wb.save(path)
    return path


def chart(path, g):
    """one bar per water body: its ortho-phosphate compliance samples, quantified results below and
    results below the reporting limit above"""
    names = sorted(g["w"], key=lambda k: (-g["w"][k][0], k))
    quant = [g["w"][k][0] - g["w"][k][1] for k in names]
    below = [g["w"][k][1] for k in names]
    fig, ax = plt.subplots(figsize=(10.2, 5.4), dpi=140)
    x = range(len(names))
    ax.bar(x, quant, width=0.34, color="#2a78d6", edgecolor="#fcfcfb", linewidth=1.6,
           label="quantified results")
    ax.bar(x, below, width=0.34, bottom=quant, color="#eb6834", edgecolor="#fcfcfb", linewidth=1.6,
           label="results below the reporting limit")
    for i, k in enumerate(names):
        ax.text(i, g["w"][k][0] + 0.6, str(g["w"][k][0]), ha="center", va="bottom", fontsize=7.6,
                color="#333333")
    ax.set_xticks(list(x))
    ax.set_xticklabels(names, rotation=38, ha="right", fontsize=8.4)
    ax.set_ylabel("compliance samples with an approved result", fontsize=9, color="#555555")
    ax.set_title("Owenbeg and Ballynure hold the most ortho-phosphate compliance samples of 2025/26, "
                 "Aghavannagh the fewest\n"
                 "Araglen River Basin District, ortho-phosphate as P. Every Tirneevin ortho-phosphate result "
                 "was below its 0.10 mg/l reporting limit.", fontsize=10, loc="left", color="#222222")
    ax.legend(frameon=False, fontsize=8.4, loc="upper right")
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_ylim(0, max(g["w"][k][0] for k in names) * 1.22)
    ax.grid(axis="y", color="#e9e9e6", linewidth=0.6)
    ax.set_facecolor("#fcfcfb")
    fig.patch.set_facecolor("#fcfcfb")
    ax.tick_params(colors="#555555", labelsize=8.4)
    ax.set_axisbelow(True)
    fig.tight_layout()
    matplotlib.rcParams["svg.fonttype"] = "none"
    fig.savefig(path, format="svg", metadata={"Creator": None, "Date": None, "Format": None, "Type": None})
    svg = open(path, encoding="utf-8").read()
    svg = svg.replace('id="matplotlib.axis_', 'id="axis_').replace(", 'DejaVu Sans'", ", sans-serif")
    svg = svg.replace("sans-serif, sans-serif", "sans-serif")
    open(path, "w", encoding="utf-8").write(svg)
    plt.close(fig)
    return path
