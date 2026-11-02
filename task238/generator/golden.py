"""The golden deliverables, written from target/ through analysis.py: price_watch_2027q1.xlsx (the Price Watch list
with every store's fourth-quarter price accuracy, the Scanner Code payouts, the flyer price misses) and
price_accuracy_q4_2026.svg (each store's accuracy against the Price Watch line), plus generator/figures.json."""
import datetime as dt
import json
import math
import os
import re
import zipfile

import analysis as A

BOOK = "price_watch_2027q1.xlsx"
CHART = "price_accuracy_q4_2026.svg"
STAMP = (2027, 1, 15, 16, 20, 0)
COUNT_WORD = {2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six", 7: "Seven", 8: "Eight", 9: "Nine"}
NAMES = {101: "Quinpool Road", 102: "Spryfield", 103: "Clayton Park", 104: "Bedford Place",
         105: "Dartmouth - Portland St", 106: "Cole Harbour", 107: "Lower Sackville", 201: "Truro (Prince St)",
         202: "New Glasgow", 203: "Antigonish", 204: "Kentville", 205: "Bridgewater", 206: "Yarmouth",
         207: "Amherst"}


def half_up(x, nd=0):
    from decimal import Decimal, ROUND_HALF_UP
    q = Decimal(1).scaleb(-nd)
    v = Decimal(repr(float(x))).quantize(q, rounding=ROUND_HALF_UP)
    return float(v) if nd else int(v)


def compute(target):
    pk = A.Pack(target)
    R = A.rungs(pk)
    pays, dups = A.ask_payouts(target, pk.by_name)
    cnt, over = A.ask_flyer(target)
    acc = {s: half_up(R["golden"][s], 1) for s in pk.stores}
    watch = [s for s in pk.stores if R["golden"][s] < A.LINE]
    off = [s for s in pk.stores if s not in watch]
    nearest = min(off, key=lambda s: R["golden"][s] - A.LINE)
    F = {
        "line": A.LINE,
        "watch": watch,
        "watch_names": [NAMES[s] for s in watch],
        "store_labels": {str(s): "%d %s" % (s, NAMES[s]) for s in pk.stores},
        "n_watch": len(watch),
        "accuracy": {str(s): acc[s] for s in pk.stores},
        "accuracy_unrounded": {str(s): R["golden"][s] for s in pk.stores},
        "nearest_off": nearest,
        "nearest_off_acc": acc[nearest],
        "audit_route": {str(s): half_up(R["r0_audit"][s], 1) for s in pk.stores},
        "audit_route_min": half_up(min(R["r0_audit"].values()), 1),
        "audit_route_floor": math.floor(10 * min(R["r0_audit"].values()) + 1e-9) / 10.0,
        "checkshare_route": [s for s in pk.stores if R["r1_checkshare"][s] < A.LINE],
        "pace": half_up(R["rate"], 1),
        "stray_share_pct": half_up(100 * R["baseline"], 2),
        "payouts": {str(s): half_up(pays.get(s, 0.0), 0) for s in pk.stores},
        "payouts_unrounded": {str(s): pays.get(s, 0.0) for s in pk.stores},
        "payout_dups": dups,
        "flyer_count": cnt,
        "flyer_over": {d: half_up(v, 0) for d, v in over.items()},
        "flyer_over_unrounded": over,
        "stale_scans": {str(s): R["golden_stale"].get(s, 0.0) for s in pk.stores},
        "total_scans": {str(s): pk.T(s) for s in pk.stores},
    }
    return F


def write_book(path, F):
    from openpyxl import Workbook
    from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
    from openpyxl.utils import get_column_letter
    wb = Workbook()
    ws = wb.active
    ws.title = "Price Watch Q1 2027"
    bold = Font(bold=True)
    ws["A1"] = "%s stores go on Price Watch for Q1 2027" % COUNT_WORD[F["n_watch"]]
    ws["A1"].font = Font(bold=True, size=13)
    ws["A2"] = "Price accuracy for Q4 2026 under PI-2 s.3.1; a store below 99.0% goes on Price Watch (s.4.1)."
    ws["A2"].font = Font(italic=True, size=9, color="555555")
    hdr = ["Store #", "Store", "Zone", "Q4 2026 price accuracy (%)", "Price Watch Q1 2027"]
    ws.append([])
    ws.append(hdr)
    for c in ws[4]:
        c.font = bold
        c.fill = PatternFill("solid", fgColor="E8EEF6")
    zone = {s: (1 if s < 200 else 2) for s in A.Pack.__init__.__code__.co_consts if False} or {}
    for s in sorted(int(k) for k in F["accuracy"]):
        on = s in F["watch"]
        ws.append([s, NAMES[s], "Zone %d" % (1 if s < 200 else 2), F["accuracy"][str(s)], "Yes" if on else "No"])
        row = ws.max_row
        ws.cell(row=row, column=4).number_format = "0.0"
        if on:
            for col in range(1, 6):
                ws.cell(row=row, column=col).fill = PatternFill("solid", fgColor="FBE3D6")
    ws.append([])
    ws.append(["Price accuracy is the share of each store's item scans in the quarter that rang up at the price on "
               "the item's shelf-edge label at the moment of the scan. Each Thursday changeover's labels are counted "
               "as showing the old price from the store's opening until its changeover batch was printed and hung."])
    ws.cell(row=ws.max_row, column=1).font = Font(size=9, color="555555")
    widths = [9, 26, 8, 26, 21]
    for i, wdt in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = wdt
    ws.freeze_panes = "A5"

    ws2 = wb.create_sheet("Scanner Code payouts")
    ws2["A1"] = "Scanner Price Accuracy Code payouts, Q4 2026"
    ws2["A1"].font = Font(bold=True, size=12)
    ws2.append(["Paid at the register (price overrides, reason SC) and at the service desk; a desk entry that "
                "repeats a register payout on the same receipt line is counted once."])
    ws2.cell(row=2, column=1).font = Font(italic=True, size=9, color="555555")
    ws2.append([])
    ws2.append(["Store #", "Store", "Paid out ($)"])
    for c in ws2[4]:
        c.font = bold
        c.fill = PatternFill("solid", fgColor="E8EEF6")
    tot = 0.0
    for s in sorted(int(k) for k in F["payouts"]):
        ws2.append([s, NAMES[s], F["payouts"][str(s)]])
        ws2.cell(row=ws2.max_row, column=3).number_format = "#,##0"
        tot += F["payouts_unrounded"][str(s)]
    ws2.append(["", "All stores (summed before rounding)", half_up(tot, 0)])
    ws2.cell(row=ws2.max_row, column=3).number_format = "#,##0"
    ws2.cell(row=ws2.max_row, column=2).font = bold
    ws2.column_dimensions["A"].width = 9
    ws2.column_dimensions["B"].width = 26
    ws2.column_dimensions["C"].width = 14
    ws2.freeze_panes = "A5"

    ws3 = wb.create_sheet("Flyer prices")
    ws3["A1"] = "Advertised items that rang up off the flyer price, by flyer week"
    ws3["A1"].font = Font(bold=True, size=12)
    ws3.append(["Register prices from the revised weekly price change release, and from a price correction's "
                "opening day on; a multi-buy is compared per unit; an assorted line covers every variety."])
    ws3.cell(row=2, column=1).font = Font(italic=True, size=9, color="555555")
    ws3.append([])
    ws3.append(["Flyer week starting", "Advertised UPCs off the flyer price", "Paid above the flyer price ($)"])
    for c in ws3[4]:
        c.font = bold
        c.fill = PatternFill("solid", fgColor="E8EEF6")
    for d in sorted(F["flyer_count"]):
        ws3.append([dt.date.fromisoformat(d), F["flyer_count"][d], F["flyer_over"][d]])
        r = ws3.max_row
        ws3.cell(row=r, column=1).number_format = "d mmm yyyy"
        ws3.cell(row=r, column=3).number_format = "#,##0"
    ws3.column_dimensions["A"].width = 20
    ws3.column_dimensions["B"].width = 34
    ws3.column_dimensions["C"].width = 30
    ws3.freeze_panes = "A5"

    ws4 = wb.create_sheet("Notes")
    notes = [
        ("Prepared", "15 January 2027, Price Integrity, for the Q1 2027 Price Watch list (PI-2 s.4.2)."),
        ("Quarter", "1 October to 31 December 2026, store local time; stores closed 12 Oct, 11 Nov, 25 and 26 Dec."),
        ("Item scans", "POS hourly item scans by store; price-changed items' units on each changeover Thursday "
                       "from the pricing team's movement report."),
        ("Changeover labels", "Each store's PCB batch on the label printer; labels go up over the minutes after "
                              "the batch prints, at the pace the Thursday checks show."),
        ("Stray labels", "Labels wrong outside a changeover, from the weekly random audits."),
        ("Rounding", "Accuracy to one decimal (compared with 99.0 unrounded); dollars to the nearest dollar."),
    ]
    for k, v in notes:
        ws4.append([k, v])
        ws4.cell(row=ws4.max_row, column=1).font = bold
    ws4.column_dimensions["A"].width = 18
    ws4.column_dimensions["B"].width = 110
    for wsx in wb.worksheets:
        for row in wsx.iter_rows():
            for c in row:
                if isinstance(c.value, (int, float)) and not isinstance(c.value, bool):
                    c.alignment = Alignment(horizontal="right")
    wb.properties.creator = "Saltmarsh Market Price Integrity"
    wb.properties.lastModifiedBy = "Saltmarsh Market Price Integrity"
    wb.properties.title = "Price Watch Q1 2027"
    when = dt.datetime(*STAMP)
    wb.properties.created = when
    wb.properties.modified = when
    wb.save(path)
    from pack import normalise_zip
    normalise_zip(path, when="2027-01-15T16:20:00Z")


def write_chart(path, F):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    matplotlib.rcParams["svg.hashsalt"] = "task238"
    matplotlib.rcParams["svg.fonttype"] = "none"
    matplotlib.rcParams["font.family"] = "DejaVu Sans"
    stores = sorted((int(k) for k in F["accuracy"]), key=lambda s: F["accuracy_unrounded"][str(s)])
    fig, ax = plt.subplots(figsize=(7.6, 5.4), dpi=100)
    fig.patch.set_facecolor("#fcfcfb")
    ax.set_facecolor("#fcfcfb")
    ys = range(len(stores))
    for y, s in zip(ys, stores):
        v = F["accuracy_unrounded"][str(s)]
        on = s in F["watch"]
        col = "#eb6834" if on else "#2a78d6"
        ax.hlines(y, 97.4, v, color="#d9d8d4", linewidth=1.2, zorder=1)
        ax.scatter([v], [y], s=64, color=col, edgecolor="#fcfcfb", linewidth=1.5, zorder=3,
                   label="Price Watch Q1 2027" if on else "Stays off")
        if on:
            ax.text(v - 0.05, y, "%.1f%%" % F["accuracy"][str(s)], va="center", ha="right", fontsize=8.5,
                    color="#0b0b0b")
    ax.axvline(99.0, color="#52514e", linestyle=(0, (4, 3)), linewidth=1.2, zorder=2)
    ax.text(99.02, len(stores) - 0.4, "Price Watch line 99.0%", fontsize=8.5, color="#52514e", va="top")
    ax.set_yticks(list(ys))
    ax.set_yticklabels(["%d %s" % (s, NAMES[s]) for s in stores], fontsize=8.5, color="#0b0b0b")
    ax.set_xlim(97.4, 100.1)
    ax.set_xlabel("Q4 2026 price accuracy (% of item scans at the shelf-edge label price)", fontsize=9,
                  color="#52514e")
    ax.tick_params(axis="x", labelsize=8.5, colors="#52514e")
    ax.xaxis.set_major_formatter(matplotlib.ticker.FormatStrFormatter("%.1f"))
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color("#bdbcb7")
    ax.grid(axis="x", color="#ecebe8", linewidth=0.8)
    ax.set_axisbelow(True)
    h, lab = ax.get_legend_handles_labels()
    uniq = dict(zip(lab, h))
    ax.legend([uniq["Price Watch Q1 2027"], uniq["Stays off"]], ["Price Watch Q1 2027", "Stays off"],
              loc="lower right", fontsize=8.5, frameon=False)
    fig.suptitle("%s stores fell below 99.0%% price accuracy in Q4 2026" % COUNT_WORD[F["n_watch"]], x=0.02,
                 ha="left", fontsize=12,
                 fontweight="bold", color="#0b0b0b")
    fig.text(0.02, 0.915, "Saltmarsh Market, PI-2 s.3.1; changeover labels counted from each store's printed batch",
             fontsize=8.5, color="#52514e")
    fig.text(0.02, 0.015, "Source: POS hourly item scans, pricing movement report, label printer fleet log, "
                          "price integrity checks and audits", fontsize=7.5, color="#7a7974")
    fig.subplots_adjust(left=0.27, right=0.97, top=0.86, bottom=0.14)
    fig.savefig(path, format="svg", metadata={"Date": None, "Creator": "Saltmarsh Market Price Integrity"})
    plt.close(fig)


def write_all(target, golden, gen):
    os.makedirs(golden, exist_ok=True)
    os.makedirs(gen, exist_ok=True)
    F = compute(target)
    write_book(os.path.join(golden, BOOK), F)
    write_chart(os.path.join(golden, CHART), F)
    with open(os.path.join(gen, "figures.json"), "w") as fh:
        json.dump(F, fh, indent=1, sort_keys=True, default=str)
        fh.write("\n")
    return F
