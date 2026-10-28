"""task270 goldens: district_fire_cover_2026.xlsx and district_fire_cover_2026.png, from calc.py's figures on the shipped
pack, and figures.json, the write-up's only source of numbers.

    python3 deliver.py <target> <golden_dir> <figures.json>"""
from __future__ import annotations

import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc as C        # noqa: E402
import common as K      # noqa: E402

STATION_NAMES = {c: n for d, lst in K.OC_STATIONS.items() for c, n in lst}
STATION_DISTRICT = {c: d for d, lst in K.OC_STATIONS.items() for c, _n in lst}


def r1(x):
    return "%.1f" % K.round_half_up(x, 1)


def compute(target):
    P = C.Pack(target)
    cover, pos = C.golden(P)
    a = C.ask_a(target, P)
    c = C.ask_c(target, P)
    prem = np.bincount(P.addr_dist[~P.addr_res], minlength=len(K.DISTRICTS))
    return dict(P=P, cover=cover, named=C.named(cover), a=a, c=c, prem=prem, homes=P.homes)


def figures(X):
    cov = {d: int(K.round_half_up(X["cover"][i], 0)) for i, d in enumerate(K.DISTRICTS)}
    named = X["named"]
    above = [d for d in K.DISTRICTS if d not in named and d not in K.RURAL]
    nearest = min(above, key=lambda d: X["cover"][K.DISTRICTS.index(d)])
    F = {
        "call": named,
        "call_sentence": " and ".join(named),
        "line": int(K.LINE),
        "cover": {d: str(cov[d]) for d in K.DISTRICTS},
        "cover_unrounded": {d: "%.3f" % X["cover"][i] for i, d in enumerate(K.DISTRICTS)},
        "nearest_above": nearest,
        "ask_a": {s: {"off_run_4plus": C.hm(X["a"][s][0]), "no_oic": C.hm(X["a"][s][1])} for s in C.RURAL_STATIONS},
        "ask_c": {d: {"actuations": str(X["c"][d][0]), "per_100": r1(X["c"][d][1])} for d in K.DISTRICTS},
        "minutes": str(K.MINUTES),
        "per": "100",
        "standard_minutes": str(int(K.STANDARD_MIN)),
        "turnout": {"Wholetime": "2", "On-call": "5"},
    }
    return F


def write_book(path, X, F):
    import openpyxl
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    from openpyxl.utils import get_column_letter
    wb = openpyxl.Workbook()
    hdr_fill = PatternFill("solid", fgColor="E7ECEF")
    hit_fill = PatternFill("solid", fgColor="F6DADA")
    bold = Font(bold=True, name="Calibri", size=11)
    thin = Side(style="thin", color="B8C1C9")

    def head(ws, row, cols, widths):
        for j, (c, w) in enumerate(zip(cols, widths), start=1):
            cell = ws.cell(row=row, column=j, value=c)
            cell.font = bold
            cell.fill = hdr_fill
            cell.alignment = Alignment(wrap_text=True, vertical="top")
            cell.border = Border(bottom=thin)
            ws.column_dimensions[get_column_letter(j)].width = w

    ws = wb.active
    ws.title = "District cover 2026"
    ws["A1"] = "Wrenfold and Pelmarsh fell below the 75 per cent cover line in 2026" if F["call"] == ["Wrenfold", "Pelmarsh"] \
        else "Districts below the 75 per cent cover line in 2026: %s" % (F["call_sentence"] or "none")
    ws["A1"].font = Font(bold=True, size=13, name="Calibri")
    ws["A2"] = ("Share of each district's homes a free fire engine could reach within ten minutes, turnout included, over "
                "the routing network, averaged over the 525,600 minutes of 2026 (emergency cover standard OFRS-RS-03). "
                "Each engine is placed where it stood each minute.")
    ws["A2"].alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells("A2:E2")
    ws.row_dimensions[2].height = 46
    head(ws, 4, ["District", "Homes", "2026 cover (%)", "Below 75 per cent", "Named in the plan"], [16, 10, 14, 16, 16])
    for i, d in enumerate(K.DISTRICTS):
        r = 5 + i
        v = int(F["cover"][d])
        below = d in F["call"]
        row = [d, int(X["homes"][i]), v, "Yes" if below else "No", "Yes" if below else "No"]
        for j, val in enumerate(row, start=1):
            cell = ws.cell(row=r, column=j, value=val)
            if below:
                cell.fill = hit_fill
        ws.cell(row=r, column=2).number_format = "#,##0"
        ws.cell(row=r, column=3).number_format = "0"
    ws.cell(row=13, column=1, value="Total homes").font = bold
    ws.cell(row=13, column=2, value=int(X["homes"].sum())).number_format = "#,##0"
    ws.cell(row=15, column=1, value="Source: mobilising system resource log, routing network and address register, 2026; "
                                    "cover to the nearest whole per cent, named on unrounded cover.")
    ws.freeze_panes = "A5"

    ws2 = wb.create_sheet("On-call availability")
    ws2["A1"] = "On-call engines in Altmoor and Skirwold, 2026: hours off the run with four or more firefighters booked"
    ws2["A1"].font = Font(bold=True, size=12, name="Calibri")
    head(ws2, 3, ["Station code", "Station", "District", "Off the run with 4+ booked (hours:minutes)",
                  "Of which no crew or watch commander booked (hours:minutes)"], [12, 14, 12, 24, 28])
    for k, s in enumerate(C.RURAL_STATIONS):
        r = 4 + k
        vals = [s, STATION_NAMES[s], STATION_DISTRICT[s], X["a"][s][0] / 1440.0, X["a"][s][1] / 1440.0]
        for j, val in enumerate(vals, start=1):
            ws2.cell(row=r, column=j, value=val)
        ws2.cell(row=r, column=4).number_format = "[h]:mm"
        ws2.cell(row=r, column=5).number_format = "[h]:mm"
    ws2.cell(row=13, column=1, value="Off the run: mobilising status 8, any reason. Booked: the availability system's "
                                     "bookings as they stood; officer in charge by role on the day.")
    ws2.freeze_panes = "A4"

    ws3 = wb.create_sheet("False alarms 2022-26")
    ws3["A1"] = "Fire alarm apparatus at non-domestic premises: actuations that brought engines out to a false alarm, 2022 to 2026"
    ws3["A1"].font = Font(bold=True, size=12, name="Calibri")
    head(ws3, 3, ["District", "Non-domestic premises", "Actuations 2022-2026", "Per 100 premises"], [16, 20, 20, 16])
    for i, d in enumerate(K.DISTRICTS):
        r = 4 + i
        vals = [d, int(X["prem"][i]), int(F["ask_c"][d]["actuations"]), float(F["ask_c"][d]["per_100"])]
        for j, val in enumerate(vals, start=1):
            ws3.cell(row=r, column=j, value=val)
        ws3.cell(row=r, column=2).number_format = "#,##0"
        ws3.cell(row=r, column=3).number_format = "#,##0"
        ws3.cell(row=r, column=4).number_format = "0.0"
    ws3.cell(row=12, column=1, value="Incidents classified A01 to 31 March 2024 and FAA from 1 April 2024 at addresses "
                                     "classed commercial; a call that reached control while the service was still at "
                                     "the premises for the same alarm is the same actuation.")
    ws3.freeze_panes = "A4"

    ws4 = wb.create_sheet("Notes")
    notes = [
        ("As of", "Records taken 16 February 2027 for the plan's response review."),
        ("Homes", "Addresses classed RD in the address register, by the district of their 2021 output area."),
        ("Free engine", "Mobilising status Available (code 1) at the start of the minute; times in UTC."),
        ("Turnout", "Two minutes for wholetime crews, five for on-call crews, by the fleet list's crewing."),
        ("Drive", "Routing network link times, one-way links honoured, node nearest the start to node nearest the home."),
        ("Where an engine stood", "At its station unless the resource log has it out of base (between Left base and "
                                  "Arrived base); then at its last reported location."),
        ("Rounding", "Cover to the nearest whole per cent; off-the-run time in hours and minutes; rates to one decimal."),
    ]
    head(ws4, 1, ["Item", "Note"], [22, 100])
    for i, (a, b) in enumerate(notes, start=2):
        ws4.cell(row=i, column=1, value=a)
        ws4.cell(row=i, column=2, value=b).alignment = Alignment(wrap_text=True)
    for w in (ws, ws2, ws3, ws4):
        w.sheet_view.showGridLines = False
        w.page_setup.orientation = "landscape"
        w.page_setup.fitToWidth = 1
    wb.properties.creator = K.PEOPLE["review"]
    wb.properties.title = "District fire cover 2026"
    wb.save(path)


def write_chart(path, X, F):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams["svg.hashsalt"] = "task270"
    order = sorted(range(len(K.DISTRICTS)), key=lambda i: X["cover"][i])
    names = [K.DISTRICTS[i] for i in order]
    vals = [int(F["cover"][K.DISTRICTS[i]]) for i in order]
    named = set(F["call"])
    fig, ax = plt.subplots(figsize=(8.6, 4.8), dpi=150)
    unr = [float(F["cover_unrounded"][n]) for n in names]
    for k, (n, v) in enumerate(zip(names, vals)):
        hit = n in named
        ax.plot([65, unr[k]], [k, k], color="#d5dbe0", linewidth=1.2, zorder=1)
        ax.scatter([unr[k]], [k], s=90, color="#b3261e" if hit else "#5f6f7d", zorder=3, edgecolor="white",
                   linewidth=1.5)
        ax.text(unr[k] + 0.55, k, "%d%%" % v, va="center", fontsize=9.5, color="#1d2329",
                fontweight="bold" if hit else "normal")
    ax.axvline(K.LINE, color="#1d2329", linewidth=1.3, linestyle=(0, (4, 3)), zorder=2)
    ax.set_ylim(-0.9, len(names) - 0.4)
    ax.text(K.LINE + 0.3, -0.65, "75 per cent line", fontsize=8.5, color="#1d2329", va="center", ha="left")
    from matplotlib.lines import Line2D
    ax.legend(handles=[Line2D([], [], marker="o", linestyle="", color="#b3261e", markersize=8,
                              label="Below the line: named in the plan"),
                       Line2D([], [], marker="o", linestyle="", color="#5f6f7d", markersize=8,
                              label="At or above the line")],
              loc="lower right", fontsize=8.5, frameon=False)
    ax.set_yticks(range(len(names)))
    ax.set_yticklabels(names, fontsize=9.5)
    ax.set_xlim(65, 90)
    ax.set_xlabel("Share of homes a free engine could reach within 10 minutes, 2026 average (%)", fontsize=9)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.grid(axis="x", color="#eef1f3", linewidth=0.8)
    ax.set_axisbelow(True)
    title = ("Wrenfold and Pelmarsh fell below the cover line in 2026" if F["call"] == ["Wrenfold", "Pelmarsh"]
             else "Districts below the cover line in 2026: %s" % (F["call_sentence"] or "none"))
    fig.suptitle(title, x=0.02, ha="left", fontsize=12.5, fontweight="bold", color="#1d2329")
    fig.text(0.02, 0.905, "Ostrevale Fire and Rescue Service, emergency cover standard OFRS-RS-03: each engine placed where "
                          "it stood each minute", fontsize=8.5, color="#5a6470")
    fig.text(0.02, 0.015, "Source: mobilising system resource log, routing network, address register (2026). Cover "
                          "rounded to whole per cent.", fontsize=7.5, color="#5a6470")
    fig.subplots_adjust(left=0.14, right=0.97, top=0.86, bottom=0.14)
    fig.savefig(path, dpi=150, metadata={"Software": None})
    plt.close(fig)


def main(target, golden, fig_path):
    os.makedirs(golden, exist_ok=True)
    X = compute(target)
    F = figures(X)
    write_book(os.path.join(golden, K.G_BOOK), X, F)
    write_chart(os.path.join(golden, K.G_CHART), X, F)
    K.write_json(fig_path, F, indent=1)
    return X, F


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
