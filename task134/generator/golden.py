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


def _hdr(ws, row, labels, fill="DDE6F0"):
    for c, h in enumerate(labels, start=1):
        cell = ws.cell(row=row, column=c, value=h)
        cell.font = Font(bold=True)
        cell.fill = PatternFill("solid", fgColor=fill)
        cell.alignment = Alignment(wrap_text=True, vertical="top", horizontal="left" if c == 1 else "right")


def _print_setup(ws, area, title_rows=None):
    ws.print_area = area
    ws.page_setup.orientation = "landscape"
    ws.page_setup.paperSize = ws.PAPERSIZE_A4
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    if title_rows:
        ws.print_title_rows = title_rows


def write_xlsx(tdir, out, res):
    g = res["raw"]["call"]
    nt = A.Notice(tdir)
    wb = Workbook()
    small = Font(size=9, color="52514E")
    bold = Font(bold=True)

    ws = wb.active
    ws.title = "Year 1 quantity"
    ws["A1"] = "Year 1 of the 2027-30 maintenance contract: %s m3 in situ" % R.fmt(res["total"])
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = "Harbour Department, Dredging and Hydrography. 18 January 2027."
    ws["A2"].font = small
    ws["A3"] = ("1 October 2027 to 30 September 2028, in situ m3 as the monthly certificates measure it: reaches and "
                "turning basin held at 14.3 m below chart datum, berth pockets at their present depths, a year of "
                "average conditions as the licence years 2016-17 to 2025-26 averaged them (planning basis, version 2).")
    ws["A3"].alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells("A3:G3")
    ws.row_dimensions[3].height = 44
    ws["A5"] = "Year 1 quantity (m3 in situ, nearest 50,000)"
    ws["A5"].font = bold
    ws["G5"] = res["total"]
    ws["G5"].font = Font(bold=True, size=12)
    ws["G5"].number_format = "#,##0"
    r0 = 7
    _hdr(ws, r0, ["Area", "Mean m3 a year, licence years 2016-17 to 2025-26", "Natural bed (m below CD)",
                  "Held depth below natural bed now (m)", "Held depth below natural bed from Oct 2027 (m)",
                  "Year 1 m3", "Year 1 m3, nearest 20,000"])
    ws.row_dimensions[r0].height = 46
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
    ws.cell(row=row, column=2, value=round(sum(g["V"][n] for n in A.REACH_NAMES) + sum(g["V"][b] for b in A.BERTH_NAMES))).font = bold
    ws.cell(row=row, column=6, value=round(g["total"])).font = bold
    ws.cell(row=row, column=7, value=res["total"]).font = bold
    for rr in range(r0 + 1, row + 1):
        for cc in (2, 6, 7):
            ws.cell(row=rr, column=cc).number_format = "#,##0"
        for cc in (3, 4, 5):
            ws.cell(row=rr, column=cc).number_format = "0.00"
    notes = [
        "Year 1 m3 for each reach and the basin = mean x (14.3 - natural bed) / (12.3 - natural bed); the berth pockets "
        "keep their present depths and are carried at their means.",
        "Natural bed: mean depth below chart datum of the survey cells 50 to 300 m outside each maintained width (the basin "
        "from its open south side), all 22 surveys from April 2016 to October 2026, Seaward's ODN elevations converted "
        "with chart datum 2.90 m below ODN.",
        "North Quay Berth 2 has not been maintained since 1 April 2019 and stays out of maintenance (Notice to Mariners "
        "No. 3 of 2026, planning basis), so it carries no quantity.",
        "Sources: maintenance_dredging_certificates_2016-2026.xlsx (latest issue of each certificate, financial-year sheets "
        "re-cut to licence years); holmwood_channel_surveys_2016-2023.csv; seaward_channel_surveys_2023-2026.csv.",
    ]
    for i, t in enumerate(notes):
        c = ws.cell(row=row + 2 + i, column=1, value=t)
        c.font = small
        c.alignment = Alignment(wrap_text=True, vertical="top")
        ws.merge_cells(start_row=row + 2 + i, start_column=1, end_row=row + 2 + i, end_column=7)
        ws.row_dimensions[row + 2 + i].height = 28
    for i, wdt in enumerate([30, 17, 13, 15, 15, 12, 14], start=1):
        ws.column_dimensions[get_column_letter(i)].width = wdt
    ws.freeze_panes = "B%d" % (r0 + 1)
    _print_setup(ws, "A1:G%d" % (row + 2 + len(notes) - 1), "%d:%d" % (r0, r0))

    ws = wb.create_sheet("Placements 2025-26")
    yr = {s: sum(res["a"][(s, q)] for q in (1, 2, 3, 4)) for s in R.SITES}
    ws["A1"] = "Placements, licence year 2025-26: %s t at Fend Spit, %s t at Wenning Deep" % (
        R.fmt(yr["Fend Spit"]), R.fmt(yr["Wenning Deep"]))
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = ("Wet tonnes. Site from each load's dump position; quarter and month by the local date of placement; wet t = "
                "dry solids / dry-solids fraction of the loading area from the last campaign completed before the month "
                "(licence 5.3, 5.4).")
    ws["A2"].font = small
    ws["A2"].alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells("A2:C2")
    ws.row_dimensions[2].height = 54
    _hdr(ws, 4, ["Quarter", "Fend Spit", "Wenning Deep"])
    for q in (1, 2, 3, 4):
        ws.append([R.QUARTERS[q]] + [res["a"][(s, q)] for s in R.SITES])
    ws.append(["Licence year 2025-26"] + [yr[s] for s in R.SITES])
    for c in range(1, 4):
        ws.cell(row=ws.max_row, column=c).font = bold
    for rr in range(5, ws.max_row + 1):
        for c in (2, 3):
            ws.cell(row=rr, column=c).number_format = "#,##0"
    mr = ws.max_row + 2
    _hdr(ws, mr, ["Month", "Fend Spit", "Wenning Deep"])
    for (y, m), nm in zip(MONTHS, MNAME):
        ws.append([nm] + [res["monthly"].get((s, y, m), 0) for s in R.SITES])
        for c in (2, 3):
            ws.cell(row=ws.max_row, column=c).number_format = "#,##0"
    last = ws.max_row
    tail = [
        "Fend Spit takes no material from 1 December to the end of February (licence 5.1); both sites together stayed "
        "inside the 2,000,000 wet tonnes a licence year of condition 5.2.",
        "Months and quarters are each rounded to the nearest 1,000 t from the unrounded loads, so the months may not add "
        "to their quarter.",
    ]
    for i, t in enumerate(tail):
        c = ws.cell(row=last + 2 + i, column=1, value=t)
        c.font = small
        c.alignment = Alignment(wrap_text=True, vertical="top")
        ws.merge_cells(start_row=last + 2 + i, start_column=1, end_row=last + 2 + i, end_column=3)
        ws.row_dimensions[last + 2 + i].height = 40
    ws.column_dimensions["A"].width = 30
    ws.column_dimensions["B"].width = 14
    ws.column_dimensions["C"].width = 14
    _print_setup(ws, "A1:C%d" % (last + 1 + len(tail)))

    ws = wb.create_sheet("Sediment 2026")
    ws["A1"] = "March 2026 sampling: all four metals rise from the Outer Channel to the Turning Basin"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = ("Mean of each area's 2026 samples, mg/kg dry weight. Each sample is placed in the area it was taken in, "
                "and each field duplicate is averaged with its primary before the area mean (licence 5.5); mercury "
                "reported in ug/kg is converted to mg/kg.")
    ws["A2"].font = small
    ws["A2"].alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells("A2:E2")
    ws.row_dimensions[2].height = 44
    _hdr(ws, 4, ["Area"] + R.METALS)
    for name in A.REACH_NAMES:
        ws.append([name] + [res["b"][(name, m)] for m in R.METALS])
        for c in range(2, 6):
            ws.cell(row=ws.max_row, column=c).number_format = "0.00"
    c = ws.cell(row=ws.max_row + 2, column=1,
                value="Sources: sediment_sampling_2025-2026.xlsx (field log 2026), aldern_results_FEN26.csv.")
    c.font = small
    ws.column_dimensions["A"].width = 18
    for col in "BCDE":
        ws.column_dimensions[col].width = 12
    _print_setup(ws, "A1:E%d" % ws.max_row)
    save_xlsx(wb, os.path.join(out, XLSX), "Maintenance dredging year 1 2027-28", P.PEOPLE["manager"], "2027-01-14T13:20:00Z",
              modified="2027-01-18T08:40:00Z")


def write_svg(out, res, fmt="svg"):
    plt.rcParams["svg.hashsalt"] = "task134"
    plt.rcParams["font.family"] = "DejaVu Sans"
    fs = [res["monthly"].get(("Fend Spit", y, m), 0) / 1000.0 for (y, m) in MONTHS]
    wd = [res["monthly"].get(("Wenning Deep", y, m), 0) / 1000.0 for (y, m) in MONTHS]
    top = max(a + b for a, b in zip(fs, wd))
    fig, ax = plt.subplots(figsize=(8.6, 4.4), dpi=100)
    x = list(range(len(MONTHS)))
    ax.axvspan(1.5, 4.5, color="#f1f0ec", zorder=1, linewidth=0)
    ax.text(3.0, top * 1.12, "Fend Spit closed (licence 5.1)", ha="center", va="center", fontsize=8, color="#52514e",
            zorder=4)
    ax.bar(x, fs, width=0.56, color="#2a78d6", label="Fend Spit", edgecolor="white", linewidth=1.0, zorder=3)
    ax.bar(x, wd, width=0.56, bottom=fs, color="#eb6834", label="Wenning Deep", edgecolor="white", linewidth=1.0, zorder=3)
    ax.set_xticks(x)
    ax.set_xticklabels(MNAME, fontsize=8.5, color="#52514e")
    ax.set_ylabel("thousand wet tonnes", fontsize=9, color="#52514e")
    ax.set_ylim(0, top * 1.2)
    ax.set_xlim(-0.6, len(MONTHS) - 0.4)
    ax.tick_params(axis="y", labelsize=8.5, colors="#52514e")
    ax.grid(axis="y", color="#e4e3df", linewidth=0.8, zorder=0)
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    ax.spines["bottom"].set_color("#b5b3ad")
    ax.set_title("Wenning Deep took everything placed while Fend Spit was closed, December to February", fontsize=11,
                 loc="left", color="#0b0b0b")
    ax.legend(frameon=False, fontsize=8.5, loc="upper right", ncol=2)
    ax.text(0.0, -0.17, "Licence year 2025-26, wet tonnes by local date of placement (licence 5.3, 5.4). "
            "Monthly figures in fendmouth_maintenance_2027-28.xlsx.", transform=ax.transAxes, fontsize=7.5, color="#52514e")
    fig.tight_layout()
    name = SVG if fmt == "svg" else SVG.replace(".svg", "." + fmt)
    if fmt == "svg":
        fig.savefig(os.path.join(out, name), format="svg", metadata={"Date": None, "Creator": None})
        path = os.path.join(out, name)
        with open(path, encoding="utf-8") as f:
            txt = f.read()
        txt = txt.replace('id="matplotlib.axis_1"', 'id="xaxis_1"').replace('id="matplotlib.axis_2"', 'id="yaxis_1"')
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(txt)
    else:
        fig.savefig(os.path.join(out, name), format=fmt)
    plt.close(fig)


def main(tdir, out):
    os.makedirs(out, exist_ok=True)
    res = R.compute(tdir)
    write_xlsx(tdir, out, res)
    write_svg(out, res)
    return res


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
