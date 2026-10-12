"""The golden deliverables: kbid_order_2027.xlsx (the order, its monthly schedule, the replay that sets it, the thirty
replays, the root zone on 31 January 2027 by crop, and the 2026 lateral balances) and kbid_order_2027.svg (the
thirty replays from smallest to largest with the order drawn across), plus generator/figures.json. Every figure is
computed from the shipped pack (calc.py)."""
from __future__ import annotations

import json
import math
import os

import numpy as np
import openpyxl
from openpyxl.styles import Border, Side, Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

import calc as C
import common as K
import postprocess as PP

MONTHS = ["February", "March", "April", "May", "June", "July", "August", "September", "October"]


def share1(x):
    return math.floor(x * 10 + 0.5) / 10.0


def compute(target):
    M = C.load(target)
    lad = C.ladder(M)
    g = lad["R3"]
    A = C.load_asks(target)
    deliv, share, inflow = C.ask_a(A)
    spill = C.ask_b(A)
    # the root zone on 31 January 2027 by crop (acre-weighted depletion, inches)
    D = M.D_golden
    by_crop = {}
    for i, f in enumerate(M.fields):
        x = by_crop.setdefault(f["crop"], dict(n=0, acres=0.0, dep=0.0, over=0))
        x["n"] += 1
        x["acres"] += M.acres[i]
        x["dep"] += D[i] * M.acres[i]
        x["over"] += int(D[i] >= M.raw[i])
    return dict(M=M, lad=lad, g=g, A=A, deliv=deliv, share=share, inflow=inflow, spill=spill, by_crop=by_crop)


def figures(c):
    g, lad = c["g"], c["lad"]
    out = {
        "call": {"order_af": "{:,}".format(g["order"]), "setting_year": g["year"],
                 "setting_requirement_af": "{:,}".format(K.round_to(g["req"], 10)),
                 "schedule_af": {m: "{:,}".format(v) for m, v in zip(MONTHS, g["months"])}},
        "steps": {
            "fields": c["M"].n, "acres": "{:,.0f}".format(c["M"].acres.sum()),
            "requirement_24th_unrounded": "{:,.2f}".format(g["req"]),
            "requirement_23rd": "{:,}".format(K.round_to(g["ranked"][22][1], 10)),
            "requirement_25th": "{:,}".format(K.round_to(g["ranked"][24][1], 10)),
            "year_23rd": g["ranked"][22][0], "year_25th": g["ranked"][24][0],
            "mean_depletion_31jan_in": "%.2f" % (float((c["M"].D_golden * c["M"].acres).sum() / c["M"].acres.sum())),
            "fields_at_allowable_31jan": int((c["M"].D_golden >= c["M"].raw).sum()),
            "replays_af": {str(y): "{:,}".format(K.round_to(v, 10)) for y, v in sorted(g["reqs"].items())},
            # the Water Order Procedure clauses the write-up's steps cite
            "procedure_clauses": ["2.3", "2.4", "3.1", "3.3", "3.4", "3.5", "4.1", "5.1", "6.1", "6.2"],
        },
        "default_path": {"order_af": "{:,}".format(lad["R0"]["order"]), "setting_year": lad["R0"]["year"],
                         "setting_requirement_af": "{:,}".format(K.round_to(lad["R0"]["req"], 10))},
        "rungs": {k: {"order_af": "{:,}".format(v["order"]), "setting_year": v["year"]} for k, v in lad.items()},
        "ask_a": {l: {"deliveries_af": "{:,}".format(K.round_to(c["deliv"][l], 10)),
                      "not_delivered_pct": "%.1f" % share1(c["share"][l]),
                      "water_in_af": "{:,}".format(K.round_to(c["inflow"][l], 10))} for l in K.LATERALS},
        "ask_b": {l: "{:,}".format(K.round_to(c["spill"][l], 10)) for l in K.LATERALS},
    }
    return out


def _head(ws, row, values, widths=None):
    for k, v in enumerate(values, 1):
        cell = ws.cell(row=row, column=k, value=v)
        cell.font = Font(name="Calibri", bold=True)
        cell.fill = PatternFill("solid", fgColor="DCE6DC")
        cell.alignment = Alignment(wrap_text=True, vertical="top")
    if widths:
        for k, w in enumerate(widths, 1):
            ws.column_dimensions[get_column_letter(k)].width = w


def write_book(path, c, figs):
    g = c["g"]
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Order 2027"
    ws["A1"] = "Kestrel Bend Irrigation District: 2027 water order, Tolan Valley Project"
    ws["A1"].font = Font(name="Calibri", bold=True, size=13)
    ws["A2"] = "Water Order Procedure (rev. December 2025), Tables for the 2027 order. Prepared 1 February 2027."
    ws["A2"].font = Font(name="Calibri", italic=True, size=10, color="595959")
    rows = [("2027 order (acre-feet)", g["order"]),
            ("Weather year whose replay sets the order", g["year"]),
            ("Headgate requirement in that replay (acre-feet)", K.round_to(g["req"], 10)),
            ("Replayed seasons the order covers", "24 of 30 (weather years 1997 to 2026)")]
    r = 4
    for label, v in rows:
        ws.cell(row=r, column=1, value=label).font = Font(name="Calibri", bold=True)
        cell = ws.cell(row=r, column=2, value=v)
        if isinstance(v, int) and v > 3000:
            cell.number_format = "#,##0"
        r += 1
    r += 1
    ws.cell(row=r, column=1, value="Monthly schedule (WOP 5.1)").font = Font(name="Calibri", bold=True, size=11)
    r += 1
    _head(ws, r, ["Month", "Acre-feet"], [52, 22])
    for m, v in zip(MONTHS, g["months"]):
        r += 1
        ws.cell(row=r, column=1, value=m)
        ws.cell(row=r, column=2, value=v).number_format = "#,##0"
    r += 1
    ws.cell(row=r, column=1, value="Season").font = Font(name="Calibri", bold=True)
    ws.cell(row=r, column=2, value=sum(g["months"])).number_format = "#,##0"
    r += 2
    ws.cell(row=r, column=1, value="Each replay starts from the root-zone depletion each field carries at the end of "
                                    "31 January 2027 (its last 2026 delivery, then the record's weather to 31 January).")
    ws.cell(row=r, column=1).font = Font(name="Calibri", italic=True, size=9, color="595959")

    ws2 = wb.create_sheet("Replays")
    ws2["A1"] = "Headgate requirement of the 2027 fields in each replayed weather year (WOP 2.4)"
    ws2["A1"].font = Font(name="Calibri", bold=True, size=12)
    ranked = [y for y, _ in g["ranked"]]
    _head(ws2, 3, ["Weather year", "Headgate requirement (acre-feet)", "Rank (smallest = 1)", "Covered by the order"],
          [14, 30, 18, 20])
    rr = 3
    for y in sorted(g["reqs"]):
        rr += 1
        ws2.cell(row=rr, column=1, value=y)
        ws2.cell(row=rr, column=2, value=K.round_to(g["reqs"][y], 10)).number_format = "#,##0"
        ws2.cell(row=rr, column=3, value=ranked.index(y) + 1)
        ws2.cell(row=rr, column=4, value="yes" if g["reqs"][y] <= g["order"] else "no")
    ws2.freeze_panes = "A4"
    ws2.print_title_rows = "3:3"

    ws3 = wb.create_sheet("Root zone 31 Jan")
    ws3["A1"] = "Root zone at the end of 31 January 2027, 2027 fields by crop"
    ws3["A1"].font = Font(name="Calibri", bold=True, size=12)
    _head(ws3, 3, ["Crop", "Fields", "Acres", "Mean depletion (in, acre-weighted)", "Fields at or past allowable depletion"],
          [20, 9, 11, 22, 22])
    rr = 3
    for crop in K.CROPS:
        x = c["by_crop"].get(crop)
        if not x:
            continue
        rr += 1
        ws3.cell(row=rr, column=1, value=K.CROP_NAME[crop])
        ws3.cell(row=rr, column=2, value=x["n"])
        ws3.cell(row=rr, column=3, value=round(x["acres"], 0)).number_format = "#,##0"
        ws3.cell(row=rr, column=4, value=round(x["dep"] / x["acres"], 2)).number_format = "0.00"
        ws3.cell(row=rr, column=5, value=x["over"])
    rr += 1
    M = c["M"]
    tot = [("All 2027 fields", None), (M.n, None), (round(float(M.acres.sum()), 0), "#,##0"),
           (round(float((M.D_golden * M.acres).sum() / M.acres.sum()), 2), "0.00"), (int((M.D_golden >= M.raw).sum()), None)]
    for k, (v, fmt) in enumerate(tot, 1):
        cell = ws3.cell(row=rr, column=k, value=v)
        cell.font = Font(name="Calibri", bold=True)
        cell.border = Border(top=Side(style="thin", color="7F7F7F"))
        if fmt:
            cell.number_format = fmt
    ws3.freeze_panes = "A4"

    ws4 = wb.create_sheet("Laterals 2026")
    ws4["A1"] = "2026 season on each lateral, from the meter book, the heading flumes and the tail weir sheets"
    ws4["A1"].font = Font(name="Calibri", bold=True, size=12)
    _head(ws4, 3, ["Lateral", "Water put in at the heading (acre-feet)", "Turnout deliveries (acre-feet)",
                   "Share of the water put in not delivered (%)", "Over the tail weir (acre-feet)",
                   "Loss allowance, Table 5 (%)"], [12, 22, 20, 22, 18, 16])
    rr = 3
    for l in K.LATERALS:
        rr += 1
        ws4.cell(row=rr, column=1, value=K.LATERAL_NAME[l])
        ws4.cell(row=rr, column=2, value=K.round_to(c["inflow"][l], 10)).number_format = "#,##0"
        ws4.cell(row=rr, column=3, value=K.round_to(c["deliv"][l], 10)).number_format = "#,##0"
        ws4.cell(row=rr, column=4, value=share1(c["share"][l])).number_format = "0.0"
        ws4.cell(row=rr, column=5, value=K.round_to(c["spill"][l], 10)).number_format = "#,##0"
        ws4.cell(row=rr, column=6, value=round(K.LOSS[l] * 100, 1)).number_format = "0.0"
    ws4.freeze_panes = "B4"
    ws4.page_setup.orientation = "landscape"

    ws5 = wb.create_sheet("Notes")
    ws5["A1"] = "Notes"
    ws5["A1"].font = Font(name="Calibri", bold=True, size=12)
    _head(ws5, 3, ["Item", "Note"], [24, 112])
    notes = [
        ("Order", "The smallest whole number of hundreds of acre-feet that would have covered the 2027 headgate "
                  "requirement in at least 24 of the thirty weather years 1997 to 2026 (WOP 2.3)."),
        ("Fields", "Each field on its latest accepted 2027 water request, with the crop, irrigation method and acres "
                   "on the request and the turnout, lateral and soil unit in the field register as it stood on 1 "
                   "February 2027 (WOP 6.2). Withdrawn requests and superseded versions are not run."),
        ("Start of each replay", "The root-zone depletion each field carries at the end of 31 January 2027: zero at "
                                 "the end of the day of its last delivered 2026 set in the irrigation orders, then "
                                 "the daily balance of WOP 3.1 on the District's weather record to 31 January."),
        ("Weather record", "Station 39 to 30 April 2014 and the yard station from 1 May 2014; a day the yard station "
                           "did not record takes station 39's values (WOP 6.1)."),
        ("Monthly schedule", "The order times each month's share of the thirty replays' summed monthly requirements, "
                             "to the nearest 10 acre-feet; October takes the difference (WOP 5.1)."),
        ("Laterals 2026", "Deliveries from the riders' meter reads, each meter changed during the season chained "
                          "through the meter shop's removal and installation readings; the Lateral 5 tail turnouts "
                          "(05-045 to 05-058) on Lateral 5 to their 15 June 2026 reads and on Lateral 6 after. Water "
                          "put in from the heading flumes' daily volumes, the Water Master's estimated days included. "
                          "Tail weir spill from the riders' morning gauge readings, each standing until the next "
                          "reading, the crest raised 2 inches for each flashboard in place."),
        ("Rounding", "The order to the whole hundred acre-feet, other volumes to the nearest 10 acre-feet, shares to "
                     "one decimal place; figures are carried unrounded until shown."),
    ]
    rr = 3
    for item, note in notes:
        rr += 1
        ws5.cell(row=rr, column=1, value=item).alignment = Alignment(vertical="top")
        cell = ws5.cell(row=rr, column=2, value=note)
        cell.alignment = Alignment(wrap_text=True, vertical="top")
    wb.save(path)
    PP.normalize_ooxml(path, K.PEOPLE["requester"], K.PEOPLE["requester"], "2027-01-28T17:40:12Z",
                       "2027-02-01T19:52:44Z", excel=True)


def write_chart(path, c, figs):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.family": "DejaVu Sans", "svg.hashsalt": "task138-kbid", "svg.fonttype": "none"})
    g = c["g"]
    ranked = g["ranked"]
    years = [str(y) for y, _ in ranked]
    vals = [v / 1000.0 for _, v in ranked]
    covered = [v <= g["order"] for _, v in ranked]
    ink, muted, surface = "#1f2421", "#5b625d", "#fcfcfb"
    blue, orange = "#2a78d6", "#eb6834"
    fig, ax = plt.subplots(figsize=(10.5, 5.6), dpi=100)
    fig.patch.set_facecolor(surface)
    ax.set_facecolor(surface)
    x = np.arange(len(vals))
    cv = np.array(covered)
    ax.scatter(x[cv], np.array(vals)[cv], s=64, color=blue, edgecolors=surface, linewidths=1.2,
               label="Covered by the order", zorder=4)
    ax.scatter(x[~cv], np.array(vals)[~cv], s=64, color=orange, edgecolors=surface, linewidths=1.2,
               label="Above the order", zorder=4)
    order_k = g["order"] / 1000.0
    ax.axhline(order_k, color=ink, linewidth=1.4, zorder=3)
    ax.text(0.2, order_k + 0.6, "Order %s acre-feet" % "{:,}".format(g["order"]), color=ink, fontsize=10,
            va="bottom", ha="left", zorder=5)
    k24 = 23
    ax.annotate("%d sets it: %s AF" % (ranked[k24][0], "{:,}".format(K.round_to(ranked[k24][1], 10))),
                xy=(k24, vals[k24]), xytext=(k24 - 9.5, vals[k24] + 5.5), color=muted, fontsize=9,
                arrowprops=dict(arrowstyle="-", color=muted, linewidth=0.8))
    lo = math.floor(min(vals) / 10.0) * 10
    hi = math.ceil(max(vals) / 10.0) * 10 + 5
    ax.set_ylim(lo, hi)
    ax.set_xticks(x)
    ax.set_xticklabels(years, rotation=90, fontsize=8.5, color=muted)
    ax.tick_params(axis="y", colors=muted, labelsize=9)
    ax.set_ylabel("Headgate requirement, thousand acre-feet", color=muted, fontsize=10)
    ax.set_xlabel("Weather year replayed (smallest requirement to largest)", color=muted, fontsize=10)
    ax.grid(axis="y", color="#d9dcd9", linewidth=0.6, zorder=0)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color("#9ea79f")
    ax.legend(loc="upper left", frameon=False, fontsize=9, labelcolor=ink)
    ax.set_title("2027 order: %s acre-feet covers 24 of the 30 replayed seasons\n" % "{:,}".format(g["order"]),
                 loc="left", fontsize=13, color=ink, fontweight="bold")
    ax.text(0.0, 1.015, "Kestrel Bend Irrigation District, 2027 fields, each replay from the root zone on 31 January "
            "2027", transform=ax.transAxes, fontsize=9.5, color=muted, va="bottom", ha="left")
    fig.tight_layout()
    fig.savefig(path, facecolor=surface, metadata={"Date": None, "Creator": None, "Format": None, "Type": None})
    plt.close(fig)
    import re
    svg = open(path, encoding="utf-8").read()
    svg = re.sub(r"<!-- Created with matplotlib.*?-->\n?", "", svg)
    svg = re.sub(r"\s*<metadata>.*?</metadata>", "", svg, flags=re.S)
    svg = svg.replace('id="matplotlib.axis_', 'id="axis_')
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(svg)


def main(target, golden, figures_path):
    os.makedirs(golden, exist_ok=True)
    c = compute(target)
    figs = figures(c)
    write_book(os.path.join(golden, K.GOLD_BOOK), c, figs)
    write_chart(os.path.join(golden, K.GOLD_CHART), c, figs)
    with open(figures_path, "w") as fh:
        json.dump(figs, fh, indent=2, sort_keys=False)
        fh.write("\n")
    return c, figs
