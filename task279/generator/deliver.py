"""task279 goldens: the adviser's workbook (carbon loss by point and unit, surface lowering, GLG) and the chart for the
general board, both from the pack through analysis.py, and generator/figures.json with every graded figure."""
from __future__ import annotations

import json
import os

import numpy as np

import analysis as A
import common as K

half_up = A.half_up


def results(target):
    pp, units = A.routes(target)
    low = A.ask_lowering(target)
    glg, per_dw = A.ask_glg(target)
    import csv
    by = {}
    for r in csv.DictReader(open(os.path.join(target, K.FILES["grid"]), encoding="utf-8")):
        by.setdefault((r["unit_code"], r["grid_point"]), {})[r["campaign"]] = r
    dist = [float(np.hypot(float(v["1997"]["x_rd"]) - float(v["2024"]["x_rd"]),
                           float(v["1997"]["y_rd"]) - float(v["2024"]["y_rd"]))) for v in by.values() if len(v) == 2]
    return dict(points=pp, units=units, lowering=low, glg=glg, glg_dw=per_dw,
                reshot_min_m=min(d for d in dist if d > 1.0))


def figures(res):
    u = res["units"]
    order = sorted(K.UNIT_CODES, key=lambda c: -u[c]["ash"])
    first = order[:3]
    fig = {
        "call": {"first_raise": [K.UNIT_NAME[c] for c in first], "codes": first,
                 "line": round(u[order[2]]["ash"] / u[order[3]]["ash"], 3),
                 "first_below": K.UNIT_NAME[order[3]]},
        "units": {c: {"name": K.UNIT_NAME[c], "carbon_loss_t_c_ha_yr": half_up(u[c]["ash"], 1),
                      "rank": order.index(c) + 1, "first_raise": c in first,
                      "surface_lowering_mm_yr": half_up(res["lowering"][c], 1),
                      "glg_cm_below_surface": int(half_up(res["glg"][c], 0))} for c in K.UNIT_CODES},
        "routes": {key: {c: half_up(u[c][key], 1) for c in K.UNIT_CODES}
                   for key in ("subsidence", "level", "mass", "fixed")},
        "facts": {
            "anchor_depth_cm": {c: half_up(u[c]["z_ash"], 1) for c in K.UNIT_CODES},
            "point_lowering_cm": {c: half_up(u[c]["low_cm"], 1) for c in K.UNIT_CODES},
            "base_sink_cm": {c: half_up(u[c]["low_cm"] - (K.CORE97_DEPTH - u[c]["z_ash"]), 1) for c in K.UNIT_CODES},
            "reshot_min_distance_m": int(np.floor(res["reshot_min_m"])),
            "filed": {"protocol_clauses": [5.1, 5.2, 6.1], "years_divisor": 365.25,
                      "datum_offset_m": K.DATUM_OFFSET_M},
        },
    }
    return fig


def chart_png(path, fig, res):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib import font_manager
    for f in ("LiberationSans-Regular.ttf", "LiberationSans-Bold.ttf"):
        p = "/usr/share/fonts/truetype/liberation/" + f
        if os.path.exists(p):
            font_manager.fontManager.addfont(p)
    plt.rcParams.update({"font.family": "Liberation Sans", "svg.hashsalt": "task279", "font.size": 10})
    u = fig["units"]
    order = sorted(K.UNIT_CODES, key=lambda c: u[c]["rank"], reverse=True)
    ink, muted, strong, rest, grid = "#1d2733", "#5b6672", "#1f4e79", "#b4bec8", "#c9d1d9"
    f_, ax = plt.subplots(figsize=(8.6, 5.4), dpi=150)
    ys = list(range(len(order)))
    vals = [res["units"][c]["ash"] for c in order]
    cols = [strong if u[c]["first_raise"] else rest for c in order]
    ax.barh(ys, vals, height=0.64, color=cols, edgecolor="white", linewidth=1.0, zorder=2)
    for y, c, v in zip(ys, order, vals):
        ax.text(v + 0.07, y, "%.1f" % u[c]["carbon_loss_t_c_ha_yr"], va="center", ha="left", fontsize=9.3, color=ink,
                fontweight="bold" if u[c]["first_raise"] else "normal")
    ax.set_yticks(ys)
    ax.set_yticklabels(["%s  %s" % (u[c]["name"], c) for c in order], fontsize=9.0, color=ink)
    line_y = len(order) - 3 - 0.5
    ax.axhline(line_y, color=ink, linewidth=1.0, linestyle=(0, (4, 3)), zorder=3)
    ax.text(max(vals) * 1.10, line_y - 0.14, "first raise above the line (protocol 6.1)", fontsize=8.4, color=ink,
            ha="right", va="top")
    ax.set_xlim(0, max(vals) * 1.12)
    ax.set_ylim(-0.6, len(order) - 0.4)
    xt = np.arange(0, max(vals) * 1.12, 1.0)
    ax.set_xticks(xt)
    ax.set_xticklabels(["%d" % x for x in xt], fontsize=8.8, color=muted)
    ax.xaxis.grid(True, color=grid, linewidth=0.6, zorder=0)
    ax.set_axisbelow(True)
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    ax.spines["bottom"].set_color(grid)
    ax.tick_params(axis="both", length=0)
    ax.set_xlabel("Carbon lost by the peat of the 1997 top metre, tonnes of carbon per hectare per year, 1997 to 2024",
                  fontsize=8.8, color=muted)
    names = fig["call"]["first_raise"]
    f_.suptitle("%s, %s and %s lost the most peat carbon since 1997" % tuple(names), x=0.015, y=0.975, ha="left",
                fontsize=12.5, fontweight="bold", color=ink)
    ax.set_title("Water-level order 2027: the first raise of the summer level, by unit", loc="left", fontsize=9.6,
                 color=muted, pad=8)
    f_.text(0.015, 0.018, "Source: Lageveen peat monitoring network, cores of 1997 (Bodemlab Wageveld) and 2024 "
                          "(Gouwlanden Laboratoria), three monitoring points a unit.\nThe 1997 top metre is found "
                          "again in each 2024 core as the depth holding the same cumulative ash per square metre.",
            fontsize=7.4, color=muted, ha="left", linespacing=1.4)
    f_.subplots_adjust(left=0.24, right=0.97, top=0.86, bottom=0.17)
    f_.savefig(path, dpi=150, metadata={"Software": None})
    plt.close(f_)


def workbook(path, fig, res):
    import openpyxl
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    wb = openpyxl.Workbook()
    head_fill = PatternFill("solid", fgColor="1F4E79")
    hf = Font(bold=True, color="FFFFFF")
    thin = Side(style="thin", color="B8C0C8")

    def header(sh, row, cols, widths=None):
        for i, c in enumerate(cols, 1):
            cell = sh.cell(row=row, column=i, value=c)
            cell.font, cell.fill = hf, head_fill
            cell.alignment = Alignment(wrap_text=True, vertical="center")
        if widths:
            for i, w in enumerate(widths):
                sh.column_dimensions[openpyxl.utils.get_column_letter(i + 1)].width = w

    u = fig["units"]
    order = sorted(K.UNIT_CODES, key=lambda c: u[c]["rank"])
    sh = wb.active
    sh.title = "First raise 2027"
    sh["A1"] = "Peat carbon loss 1997 to 2024 by unit, and the first raise of the 2027 water-level order"
    sh["A1"].font = Font(bold=True, size=12)
    sh["A2"] = "Protocol 5.1 and 5.2; the first raise takes the three units with the largest loss (6.1)."
    header(sh, 4, ["Rank", "Unit", "Code", "Carbon loss, t C/ha/yr", "First raise",
                   "Surface lowering, mm/yr (annex A)", "GLG, cm below surface (annex B)"],
           [6, 14, 9, 14, 10, 18, 18])
    for i, c in enumerate(order):
        r = 5 + i
        vals = [u[c]["rank"], u[c]["name"], c, u[c]["carbon_loss_t_c_ha_yr"], "yes" if u[c]["first_raise"] else "no",
                u[c]["surface_lowering_mm_yr"], u[c]["glg_cm_below_surface"]]
        for j, v in enumerate(vals, 1):
            cell = sh.cell(row=r, column=j, value=v)
            if j in (4, 6):
                cell.number_format = "0.0"
            if j == 7:
                cell.number_format = "0"
            if i == 2:
                cell.border = Border(bottom=Side(style="medium", color="1D2733"))
        if u[c]["first_raise"]:
            for j in range(1, 8):
                sh.cell(row=r, column=j).font = Font(bold=True)
    sh.freeze_panes = "A5"

    pt = wb.create_sheet("Points")
    header(pt, 1, ["Unit", "Point 1997", "Point 2024", "Cored 1997", "Cored 2024", "Years",
                   "Ash, 1997 top metre, kg/m2", "Depth holding it in 2024, cm", "Carbon, 1997 top metre, kg/m2",
                   "Carbon above that depth in 2024, kg/m2", "Carbon loss, t C/ha/yr"],
           [10, 11, 15, 11, 11, 7, 13, 13, 13, 15, 12])
    import analysis
    pts, c97, c24 = analysis.load(_TARGET[0])
    for i, p in enumerate(sorted(pts, key=lambda q: (q["unit_code"], q["point_1997"]))):
        r = res["points"][p["point_1997"]]
        e24, m24, a24, k24 = analysis.profile(c24[p["point_2024"]])
        c_after = analysis.amount_to(e24, k24, r["z_ash"])
        import datetime as _dt
        row = [p["unit_code"], p["point_1997"], p["point_2024"], _dt.date.fromisoformat(p["cored_1997"]),
               _dt.date.fromisoformat(p["cored_2024"]), r["years"], r["A97"], r["z_ash"], r["C97"], c_after, r["ash"]]
        for j, v in enumerate(row, 1):
            cell = pt.cell(row=2 + i, column=j, value=v)
            if j in (4, 5):
                cell.number_format = "dd-mm-yyyy"
            elif j == 6:
                cell.number_format = "0.00"
            elif j in (7, 9, 10):
                cell.number_format = "0.0"
            elif j == 8:
                cell.number_format = "0.0"
            elif j == 11:
                cell.number_format = "0.00"
    pt.freeze_panes = "A2"

    nt = wb.create_sheet("Notes")
    notes = [
        "Carbon loss (protocol 5.1): for each point, the 1997 core's top metre (twenty 5 cm slices) holds A kg of ash "
        "and C97 kg of carbon per square metre (dry bulk density times slice thickness, times the ash share 1 - loss on "
        "ignition, or the carbon share). Ash does not burn, so the same peat holds the same ash in 2024: its base is the "
        "depth in the 2024 core where the cumulative ash reaches A, read linearly within the 10 cm slice. The carbon lost "
        "is C97 less the 2024 carbon above that depth, times 10 for tonnes per hectare, over the years between the two "
        "coring dates (days / 365.25). A unit's loss is the mean of its three points (5.2).",
        "Not used: the surveyed lowering at topsoil carbon density, and the cores lined up on the surveyed lowering, "
        "count the compression of the newly drained and consolidating peat as carbon lost; equal total soil mass "
        "reaches into deeper peat by the organic mass oxidation removed and so hides most of the loss.",
        "Surface lowering (annex A): grid points levelled in 1997 and surveyed in 2024 at the same spot; 1997 levels "
        "less 0.054 m to current NAP (survey report). Points re-shot in 2024 at a meadow edge tens of metres from the "
        "1996 position are not a fall at the point and are left out.",
        "GLG (annex B): logger 08:00 readings of the 14th and 28th, the hand reading where the logger has none; depth "
        "below the tube top less the tube top's height above the surface at the time of the reading (the 2018 to 2022 "
        "tube renewals lowered every tube top; the old heights are in the maintenance log); the three deepest levels of "
        "each hydrological year 2017/18 to 2024/25, averaged; a unit's GLG is the mean of its two dipwells.",
        "Prepared %s from the files in the folder of 2 November 2026." % "November 2026",
    ]
    nt.column_dimensions["A"].width = 120
    for i, t in enumerate(notes, 1):
        nt.cell(row=i, column=1, value=t).alignment = Alignment(wrap_text=True, vertical="top")
    wb.save(path)


_TARGET = [None]


def write_figures(path, fig):
    with open(path, "w") as f:
        json.dump(fig, f, indent=1, sort_keys=True)
        f.write("\n")


def write(target, golden):
    _TARGET[0] = target
    os.makedirs(golden, exist_ok=True)
    res = results(target)
    fig = figures(res)
    workbook(os.path.join(golden, K.GOLDEN), fig, res)
    chart_png(os.path.join(golden, K.CHART), fig, res)
    return fig, res
