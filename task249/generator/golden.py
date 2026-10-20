"""The two goldens: the spring review workbook and the chart of each station's published 2027 load against the
review's estimate.   GD.write(golden_dir, content)"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill, Border, Side
from openpyxl.utils import get_column_letter

import params as P
import postprocess

XLSX = "sediment_load_review_2027.xlsx"
PNG = "station_loads_2027.png"
AUTHOR = "Monitoring analytics, %s" % P.ORG
BLUE, ORANGE, INK, INK2, GRID, SURF = "#2a78d6", "#eb6834", "#0b0b0b", "#52514e", "#d9d8d4", "#fcfcfb"
THIN = Side(style="thin", color="B7B6B1")


def _rounded_estimate(t):
    return int(round(t, -2)) if t >= 10000 else int(round(t, -1))


def _sheet(ws, title, sub, head, rows, widths, fmts, start=4):
    ws["A1"] = title
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = sub
    ws["A2"].font = Font(italic=True, size=9, color="52514E")
    for j, h in enumerate(head, 1):
        c = ws.cell(row=start, column=j, value=h)
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="E8E7E3")
        c.alignment = Alignment(wrap_text=True, vertical="bottom")
        c.border = Border(bottom=THIN)
    for i, r in enumerate(rows, start + 1):
        for j, (x, f) in enumerate(zip(r, fmts), 1):
            c = ws.cell(row=i, column=j, value=x)
            if f:
                c.number_format = f
            if isinstance(x, str):
                c.alignment = Alignment(horizontal="left")
    for k, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(k)].width = w
    ws.freeze_panes = ws.cell(row=start + 1, column=2)
    return start + len(rows)


def workbook(path, G):
    wb = Workbook()
    ws = wb.active
    ws.title = "Review 2027"
    rows = []
    for code in G["order"]:
        v = G["call"][code]
        rows.append([code, G["name"][code], G["regime"][code], v["published_t"], _rounded_estimate(v["estimate_t"]),
                     v["misstatement_pct"] / 100, "Over: re-issue" if v["verdict"] == "over" else
                     ("Under: re-issue" if v["verdict"] == "under" else "Within tolerance"),
                     v["samples"], v["rising_samples"]])
    last = _sheet(ws, "Four stations' published 2027 loads overstate what passed by more than 15 per cent: SKB, JVB, FND, ESK",
                  "Spring review under SMP-03 v3 section 8 (tolerance 15 per cent either way). Review estimate: "
                  "log10 concentration on log10 turbidity and whether the river was rising at the sample, Duan's smearing.",
                  ["Station", "Name", "Regime", "Published 2027 (t)", "Review estimate 2027 (t)",
                   "Published against estimate", "Verdict", "Calibration samples 2025-27", "of which on rising water"],
                  rows, [9, 27, 13, 14, 15, 13, 17, 13, 12],
                  [None, None, None, "#,##0", "#,##0", "+0%;-0%;0%", None, "0", "0"])
    for i in range(5, last + 1):
        if ws.cell(row=i, column=7).value.startswith("Over"):
            for j in range(1, 10):
                ws.cell(row=i, column=j).font = Font(bold=True)
    ws.cell(row=last + 2, column=1, value="Estimates rounded to 100 t above 10,000 t and to 10 t below. Rising water: the "
            "15-minute discharge rose by more than 1.5 per cent an hour, averaged over the hour around the reading.").font = \
        Font(size=9, color="52514E")
    ws.print_title_rows = "4:4"

    ws2 = wb.create_sheet("Turbidity record 2025-26")
    rows = [[c, G["name"][c], G["ask_a"][c]["hours_whole"], G["ask_a"][c]["missing"], G["ask_a"][c]["flagged"],
             G["ask_a"][c]["ceiling"]] for c in G["order"]]
    last = _sheet(ws2, "Hours without a usable turbidity reading, 1 January 2025 to 31 December 2026",
                  "SMP-03 v3 section 5. Intervals are 15 minutes (UTC); four make an hour.",
                  ["Station", "Name", "Hours without a usable reading", "Intervals with no row",
                   "Intervals flagged fouled or sonde out (F, M; G, O before 14 April 2026)",
                   "Intervals at the TS-10's 1,000 FNU limit"],
                  rows, [9, 27, 15, 14, 24, 16], [None, None, "#,##0", "#,##0", "#,##0", "#,##0"])
    ws2.cell(row=last + 2, column=1, value="Letters G (fouled) and O (sonde out) were the data team's flags before the "
             "database migration of 14 April 2026, K the former C (checked, usable); they coincide with the maintenance "
             "log's cleaning visits. Re-sent rows counted once.").font = Font(size=9, color="52514E")

    ws3 = wb.create_sheet("Laboratory QC 2027")
    rows = [[c, G["name"][c], G["n27"][c], G["ask_b"][c]] for c in G["order"]]
    last = _sheet(ws3, "2027 samples weighed in a batch that failed its quality control",
                  "SMP-03 v3 section 4: blank within 0.5 mg, each control aliquot 90 to 110 per cent of the lot's "
                  "concentration (quality statement), aliquots within 10 per cent of their mean.",
                  ["Station", "Name", "2027 samples", "In a failed batch"], rows, [9, 27, 12, 14],
                  [None, None, "0", "0"])
    r0 = last + 3
    ws3.cell(row=r0, column=1, value="Failed batches").font = Font(bold=True)
    for j, h in enumerate(["Batch", "Weighed", "Check failed", "Samples"], 1):
        c = ws3.cell(row=r0 + 1, column=j, value=h)
        c.font = Font(bold=True)
        c.border = Border(bottom=THIN)
    for i, b in enumerate(G["failed_rows"], r0 + 2):
        for j, x in enumerate(b, 1):
            ws3.cell(row=i, column=j, value=x)

    ws4 = wb.create_sheet("Notes")
    notes = [
        ("As of", "13 March 2028, for the flushing plan fixed on 20 March 2028."),
        ("Population", "The 14 stations in the station register; loads for 1 January 00:00 to 31 December 23:45 UTC, 2027."),
        ("Published loads", "Suspended sediment loads 2027 (issued 15 February 2028); the procedure's regression "
                            "refitted on the same samples reproduces every load to within 0.1 per cent."),
        ("Review estimate", "Each station's samples of 2025 to 2027 (final laboratory results), each paired with the "
                            "15-minute reading nearest its time; log10 concentration on log10 turbidity and an indicator "
                            "of rising water at the sample; applied to every 15-minute interval of 2027 with that "
                            "interval's own indicator; Duan's smearing."),
        ("Why", "At SKB, JVB, FND and ESK most calibration samples were taken while the river was rising (the melt "
                "season's working-hours rounds and early flood callouts), when a unit of turbidity carries two to three "
                "times the concentration; the published regression carries that into every hour of the year."),
        ("Tolerance", "Re-issue when the published load misstates what passed by more than 15 per cent, over or under "
                      "(section 8)."),
    ]
    for i, (k, v) in enumerate(notes, 1):
        ws4.cell(row=i, column=1, value=k).font = Font(bold=True)
        c = ws4.cell(row=i, column=2, value=v)
        c.alignment = Alignment(wrap_text=True, vertical="top")
    ws4.column_dimensions["A"].width = 16
    ws4.column_dimensions["B"].width = 110
    wb.save(path)
    postprocess.scrub(path, P.ORG, "2028-03-13")
    postprocess.finish_office(path, "2028-03-08T07:55:00Z", "2028-03-13T15:10:00Z", P.ORG)


def chart(path, G):
    order = list(reversed(G["order"]))
    fig, ax = plt.subplots(figsize=(9.2, 6.4), dpi=150)
    fig.patch.set_facecolor(SURF)
    ax.set_facecolor(SURF)
    for i, code in enumerate(order):
        v = G["call"][code]
        flag = v["verdict"] != "within"
        ax.plot([v["estimate_t"], v["published_t"]], [i, i], color=INK if flag else GRID, lw=2 if flag else 1.4,
                zorder=1, solid_capstyle="round")
        ax.scatter(v["estimate_t"], i, s=46, color=BLUE, zorder=3, edgecolor=SURF, linewidth=1.5)
        ax.scatter(v["published_t"], i, s=46, color=ORANGE, zorder=3, edgecolor=SURF, linewidth=1.5)
        if flag:
            ax.text(max(v["published_t"], v["estimate_t"]) * 1.12, i, "%+.0f%%" % v["misstatement_pct"],
                    va="center", ha="left", fontsize=9, color=INK, fontweight="bold")
    ax.set_xscale("log")
    ax.set_xlim(1200, 450000)
    ax.set_yticks(range(len(order)))
    ax.set_yticklabels(["%s  %s" % (c, G["name"][c]) for c in order], fontsize=8.6, color=INK2)
    for lab, code in zip(ax.get_yticklabels(), order):
        if G["call"][code]["verdict"] != "within":
            lab.set_color(INK)
            lab.set_fontweight("bold")
    ax.set_xticks([2000, 5000, 10000, 20000, 50000, 100000, 200000])
    ax.xaxis.set_minor_locator(matplotlib.ticker.NullLocator())
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: "{:,.0f}".format(x)))
    ax.set_xlabel("Suspended sediment, 2027 (tonnes, log scale)", fontsize=9, color=INK2)
    ax.grid(axis="x", color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(axis="both", length=0, colors=INK2, labelsize=8.6)
    ax.scatter([], [], s=46, color=ORANGE, label="Published (report of 15 February 2028)")
    ax.scatter([], [], s=46, color=BLUE, label="Review estimate (what passed)")
    ax.legend(loc="lower right", frameon=False, fontsize=8.6)
    fig.suptitle("Four stations' published 2027 loads overstate what passed by more than 15 per cent",
                 x=0.02, y=0.985, ha="left", fontsize=11.5, fontweight="bold", color=INK)
    ax.set_title("Bold: outside the 15 per cent review tolerance, to be re-issued before the flushing plan",
                 loc="left", fontsize=9, color=INK2)
    fig.text(0.02, 0.01, "Source: %s, %s; 15-minute record and field samples 2025-27; review of 13 March 2028."
             % (P.ORG, P.PROGRAMME), fontsize=7.5, color=INK2)
    fig.tight_layout(rect=(0, 0.03, 1, 0.985))
    fig.savefig(path, facecolor=SURF, metadata={"Software": None})
    plt.close(fig)


def write(golden, G):
    os.makedirs(golden, exist_ok=True)
    workbook(os.path.join(golden, XLSX), G)
    chart(os.path.join(golden, PNG), G)
