"""The golden deliverables: fendmouth_maintenance_2027-28.xlsx and placements_2025-26.svg, written from target/."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from openpyxl import Workbook  # noqa: E402
from openpyxl.styles import Alignment, Font, PatternFill  # noqa: E402
from openpyxl.utils import get_column_letter  # noqa: E402

import analysis as A  # noqa: E402
import params as P  # noqa: E402
import results as R  # noqa: E402
from io_util import save_xlsx  # noqa: E402

XLSX = "fendmouth_maintenance_2027-28.xlsx"
SVG = "placements_2025-26.svg"
MONTHS = [(2025, 10), (2025, 11), (2025, 12), (2026, 1), (2026, 2), (2026, 3), (2026, 4), (2026, 5), (2026, 6), (2026, 7),
          (2026, 8), (2026, 9)]
MNAME = ["Oct 25", "Nov 25", "Dec 25", "Jan 26", "Feb 26", "Mar 26", "Apr 26", "May 26", "Jun 26", "Jul 26", "Aug 26", "Sep 26"]


def write_xlsx(tdir, out, res):
    g = res["raw"]["call"]
    nt = A.Notice(tdir)
    wb = Workbook()
    ws = wb.active
    ws.title = "Year 1 quantity"
    bold = Font(bold=True)
    ws["A1"] = "Maintenance dredging, year 1 of the 2027-30 contract (1 Oct 2027 to 30 Sep 2028)"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = "In situ m3 as the monthly certificates measure it. Reaches and turning basin held at 14.3 m below CD from 1 Oct 2027, berth pockets as now."
    ws["A3"] = "Average year: licence years 2016-17 to 2025-26. Natural bed = mean of survey cells 50 to 300 m outside each maintained width, all 22 surveys."
    ws["A5"] = "Year 1 quantity (m3, nearest 50,000)"
    ws["A5"].font = bold
    ws["F5"] = res["total"]
    ws["F5"].font = Font(bold=True, size=12)
    ws["F5"].number_format = "#,##0"
    hdr = ["Area", "Mean m3/yr 2016-26", "Natural bed (m below CD)", "Below natural bed now (m)",
           "Below natural bed from Oct 27 (m)", "Year 1 m3", "Year 1 m3 (nearest 20,000)"]
    r0 = 7
    for c, h in enumerate(hdr, start=1):
        cell = ws.cell(row=r0, column=c, value=h)
        cell.font = bold
        cell.fill = PatternFill("solid", fgColor="DDE6F0")
        cell.alignment = Alignment(wrap_text=True, vertical="top")
    row = r0 + 1
    for name in A.REACH_NAMES:
        h = g["nat"][name]
        d0 = nt.parts[name]["depth"]
        vals = [name, round(g["V"][name]), round(h, 2), round(d0 - h, 2), round(A.NEW_DEPTH - h, 2), round(g["parts"][name]),
                res["parts"][name]]
        for c, v in enumerate(vals, start=1):
            ws.cell(row=row, column=c, value=v)
        row += 1
    vals = ["Berth pockets (NQ1, NQ3, CT5)", round(sum(g["V"][b] for b in A.BERTH_NAMES)), None, None, None,
            round(g["parts"]["Berth pockets"]), res["parts"]["Berth pockets"]]
    for c, v in enumerate(vals, start=1):
        ws.cell(row=row, column=c, value=v)
    row += 1
    ws.cell(row=row, column=1, value="Total").font = bold
    ws.cell(row=row, column=2, value=round(sum(g["V"][n] for n in A.REACH_NAMES) + sum(g["V"][b] for b in A.BERTH_NAMES)))
    ws.cell(row=row, column=6, value=round(g["total"])).font = bold
    ws.cell(row=row, column=7, value=res["total"]).font = bold
    for rr in range(r0 + 1, row + 1):
        for cc in (2, 6, 7):
            ws.cell(row=rr, column=cc).number_format = "#,##0"
    ws.cell(row=row + 2, column=1, value="Year 1 m3 = mean x (14.3 - natural bed) / (12.3 - natural bed) for each reach and the basin; berth pockets at their means; Berth 2 not maintained.")
    for i, wdt in enumerate([30, 18, 16, 16, 18, 14, 18], start=1):
        ws.column_dimensions[get_column_letter(i)].width = wdt

    ws = wb.create_sheet("Placements 2025-26")
    ws["A1"] = "Material placed at the licensed disposal sites, licence year 2025-26 (wet tonnes)"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = "Site from each load's dump position; quarters by local date of placement; wet t = dry solids / area dry-solids fraction (licence 5.3, 5.4)."
    ws.append([])
    ws.append(["Quarter"] + R.SITES)
    for c in range(1, 4):
        ws.cell(row=4, column=c).font = bold
    for q in (1, 2, 3, 4):
        ws.append([R.QUARTERS[q]] + [res["a"][(s, q)] for s in R.SITES])
        for c in (2, 3):
            ws.cell(row=ws.max_row, column=c).number_format = "#,##0"
    ws.append([])
    ws.append(["Month"] + R.SITES)
    for c in range(1, 4):
        ws.cell(row=ws.max_row, column=c).font = bold
    for (y, m), nm in zip(MONTHS, MNAME):
        ws.append([nm] + [res["monthly"].get((s, y, m), 0) for s in R.SITES])
        for c in (2, 3):
            ws.cell(row=ws.max_row, column=c).number_format = "#,##0"
    ws.column_dimensions["A"].width = 28
    ws.column_dimensions["B"].width = 14
    ws.column_dimensions["C"].width = 14

    ws = wb.create_sheet("Sediment 2026")
    ws["A1"] = "March 2026 sampling: mean concentration by area (mg/kg dry weight)"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = "Samples placed in the area they were taken in; field duplicates averaged with their primary first (licence 5.5)."
    ws.append([])
    ws.append(["Area"] + R.METALS)
    for c in range(1, 6):
        ws.cell(row=4, column=c).font = bold
    for name in A.REACH_NAMES:
        ws.append([name] + [res["b"][(name, m)] for m in R.METALS])
        for c in range(2, 6):
            ws.cell(row=ws.max_row, column=c).number_format = "0.00"
    ws.column_dimensions["A"].width = 18
    for c in "BCDE":
        ws.column_dimensions[c].width = 12
    save_xlsx(wb, os.path.join(out, XLSX), "Maintenance dredging year 1 2027-28", P.PEOPLE["manager"], "2027-01-18T08:40:00Z")


def write_svg(out, res):
    plt.rcParams["svg.hashsalt"] = "task134"
    plt.rcParams["font.family"] = "DejaVu Sans"
    fs = [res["monthly"].get(("Fend Spit", y, m), 0) / 1000.0 for (y, m) in MONTHS]
    wd = [res["monthly"].get(("Wenning Deep", y, m), 0) / 1000.0 for (y, m) in MONTHS]
    fig, ax = plt.subplots(figsize=(8.6, 4.4), dpi=100)
    x = list(range(len(MONTHS)))
    ax.bar(x, fs, width=0.56, color="#2a78d6", label="Fend Spit", edgecolor="white", linewidth=1.0, zorder=3)
    ax.bar(x, wd, width=0.56, bottom=fs, color="#eb6834", label="Wenning Deep", edgecolor="white", linewidth=1.0, zorder=3)
    for i in x:
        ax.text(i, fs[i] + wd[i] + 2.5, "%.0f" % (fs[i] + wd[i]), ha="center", va="bottom", fontsize=7.5, color="#52514e")
    ax.set_xticks(x)
    ax.set_xticklabels(MNAME, fontsize=8.5, color="#52514e")
    ax.set_ylabel("thousand wet tonnes", fontsize=9, color="#52514e")
    ax.set_ylim(0, max(a + b for a, b in zip(fs, wd)) * 1.16)
    ax.tick_params(axis="y", labelsize=8.5, colors="#52514e")
    ax.grid(axis="y", color="#e4e3df", linewidth=0.8, zorder=0)
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    ax.spines["bottom"].set_color("#b5b3ad")
    ax.set_title("Material placed by month and disposal site, licence year 2025-26", fontsize=11, loc="left", color="#0b0b0b")
    ax.legend(frameon=False, fontsize=8.5, loc="upper right", ncol=2)
    ax.text(0.0, -0.17, "Fend Spit closed December to February (licence 5.1). Month and quarter by local date of placement.",
            transform=ax.transAxes, fontsize=7.5, color="#52514e")
    fig.tight_layout()
    fig.savefig(os.path.join(out, SVG), format="svg", metadata={"Date": None, "Creator": None})
    plt.close(fig)


def main(tdir, out):
    os.makedirs(out, exist_ok=True)
    res = R.compute(tdir)
    write_xlsx(tdir, out, res)
    write_svg(out, res)
    return res


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
