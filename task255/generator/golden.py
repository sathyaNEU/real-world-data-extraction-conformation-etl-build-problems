"""The golden deliverables (tier_g_2027.xlsx and tier_g_2027.svg) and figures.json, from target/ alone."""
import json
import os
import re

import analysis as AN
import io_util as IO

BOOK = "tier_g_2027.xlsx"
PAGE = "tier_g_2027.svg"
INK, INK2, MUTED = "#0b0b0b", "#52514e", "#c9c8c3"
TIER = "#2a78d6"


def compute(target):
    M = AN.main_call(target, "duration")
    R1 = AN.main_call(target, "linemap")
    R0 = AN.main_call(target, "none")
    RA = AN.main_call(target, "allday")
    mg = AN.make_good(target)
    sc = AN.screens_on_sale(target)
    rev = AN.net_revenue(target)
    bk = AN.load_bookings(target)
    parts = AN.net_revenue_parts(target)
    rates = {}
    for s in AN.load_statements(target):
        base = sum(parts["invoiced"][r] + sum(a for d, a in parts["credits"][r] if d <= s["date"]) for r in s["refs"])
        rates[s["agency"]] = s["amount"] / base
    return {"M": M, "R1": R1, "R0": R0, "RA": RA, "make_good": mg, "screens": sc, "revenue": rev, "bookings": bk,
            "rates": rates}


def r10(x):
    return int(round(x / 10.0)) * 10


def figures(c):
    M = c["M"]
    pk = M.packages
    f = {"call": [pk[k][0] for k in M.tier], "tier_codes": M.tier,
         "regular_riders": len(M.regular),
         "reach": {pk[k][0]: int(round(M.reach[k])) for k in pk},
         "reach_exact": {pk[k][0]: round(M.reach[k], 3) for k in pk},
         "reach_linemap": {pk[k][0]: int(round(c["R1"].reach[k])) for k in pk},
         "tier_linemap": [pk[k][0] for k in c["R1"].tier],
         "reach_gates_only": {pk[k][0]: int(round(c["R0"].reach[k])) for k in pk},
         "tier_gates_only": [pk[k][0] for k in c["R0"].tier],
         "make_good_hours": {b["booking_ref"]: c["make_good"][b["booking_ref"]]["make_good"] for b in c["bookings"]},
         "screens_on_sale_2027": {pk[k][0]: c["screens"][k] for k in pk},
         "net_revenue_eur": {pk[k][0]: r10(c["revenue"][k]) for k in pk},
         "tier_line_pct": 40, "effective_frequency": 3, "headway_min": 3, "make_good_allowance_pct": 0.5,
         "agency_rates_pct": {a: round(100 * v, 1) for a, v in c["rates"].items()},
         "booking_package": {b["booking_ref"]: b["package"] for b in c["bookings"]},
         "peak_windows": "07:00 to 09:30 and 16:00 to 18:30",
         "clauses_cited": "rate card 3.1, 3.2, 3.3, 3.4, 3.5; general terms 6.1, 6.2, 6.3, 8.2, 8.3"}
    return f


def chart(c, f, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    M = c["M"]
    pk = M.packages
    codes = sorted(pk, key=lambda k: -M.reach[k])
    vals = [int(round(M.reach[k])) for k in codes]
    names = [pk[k][0] for k in codes]
    tier = [pk[k][0] for k in codes if k in M.tier]
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8.5, "svg.hashsalt": "t255",
                         "svg.fonttype": "none"})
    fig, ax = plt.subplots(figsize=(7.4, 4.5), dpi=200)
    fig.subplots_adjust(left=0.17, right=0.97, top=0.83, bottom=0.19)
    cols = [TIER if k in M.tier else MUTED for k in codes]
    ax.barh(range(len(codes)), vals, color=cols, height=0.66, edgecolor="white", linewidth=1.0)
    ax.axvline(40, color=INK2, lw=1.0, ls=(0, (4, 3)))
    ax.text(40.5, -0.75, "Tier G line, 40%", color=INK2, fontsize=7.8, va="center")
    for i, v in enumerate(vals):
        ax.text(v + 0.7, i, "%d%%" % v, va="center", fontsize=8, color=INK)
    ax.set_yticks(range(len(codes)))
    ax.set_yticklabels(names, color=INK)
    ax.set_ylim(len(codes) - 0.4, -1.2)
    ax.set_xlim(0, 60)
    ax.set_xticks(range(0, 61, 10))
    ax.set_xticklabels(["%d%%" % x for x in range(0, 61, 10)], color=INK2)
    ax.set_xlabel("Effective reach: regular riders passing the package's screens three times or more",
                  color=INK2, fontsize=7.8)
    ax.tick_params(axis="both", length=0)
    ax.grid(axis="x", color="#ecebe7", lw=0.7)
    ax.set_axisbelow(True)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color("#bdbcb6")
    fig.text(0.02, 0.955, "%s, %s and %s clear the Tier G line for 2027" % tuple(tier), fontsize=11.5,
             fontweight="bold", color=INK, va="top")
    fig.text(0.02, 0.905, "Effective reach by package, audience window 5 October to 1 November 2026, %s regular riders"
             % format(f["regular_riders"], ","), fontsize=8.3, color=INK2, va="top")
    fig.text(0.02, 0.045, "Source: RVB OV-chipkaart metro journeys (re-export of 5 November 2026), RVB planning model "
             "2026, rate card 2027 Annex A.", fontsize=6.6, color=INK2)
    fig.text(0.02, 0.015, "Spoorbeeld Media B.V., audience research, 13 November 2026", fontsize=6.6, color=INK2)
    fig.savefig(path, format="svg", metadata={"Creator": None, "Date": None, "Format": None, "Type": None,
                                              "Title": "Tier G 2027: effective reach by package"})
    plt.close(fig)
    svg = open(path, encoding="utf-8").read()
    svg = re.sub(r"<!-- Created with [^>]*-->\n?", "", svg)
    svg = svg.replace('id="matplotlib.axis_1"', 'id="x-axis"').replace('id="matplotlib.axis_2"', 'id="y-axis"')
    assert "matplotlib" not in svg.lower()
    open(path, "w", encoding="utf-8").write(svg)


def workbook(c, f, path):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    M = c["M"]
    pk = M.packages
    wb = Workbook()
    wb.remove(wb.active)
    bold, grey = Font(bold=True), Font(color="52514E", italic=True, size=9)
    head_fill = PatternFill("solid", fgColor="EDF2F8")

    def sheet(name, title, header, rows, widths, formats, notes):
        ws = wb.create_sheet(name)
        ws.append([title])
        ws["A1"].font = Font(bold=True, size=12)
        ws.append([])
        ws.append(header)
        for cell in ws[3]:
            cell.font = bold
            cell.fill = head_fill
            cell.alignment = Alignment(wrap_text=True, vertical="bottom")
        for r in rows:
            ws.append(list(r))
        for i, w in enumerate(widths):
            ws.column_dimensions[chr(65 + i)].width = w
        for row in ws.iter_rows(min_row=4, max_row=3 + len(rows)):
            for i, cell in enumerate(row):
                if formats.get(i):
                    cell.number_format = formats[i]
                    cell.alignment = Alignment(horizontal="right")
        ws.freeze_panes = "A4"
        ws.row_dimensions[3].height = 30
        r0 = 5 + len(rows)
        for k, line in enumerate(notes):
            ws.cell(row=r0 + k, column=1, value=line).font = grey
        return ws

    order = sorted(pk, key=lambda k: -M.reach[k])
    sheet("Tier G 2027", "Tier G 2027: effective reach by package, audience window 5 October to 1 November 2026",
          ["Package", "Code", "Effective reach (%)", "Tier 2027"],
          [[pk[k][0], k, int(round(M.reach[k])), "Tier G" if k in M.tier else "standard"] for k in order],
          [20, 8, 14, 12], {2: "0"},
          ["Regular riders: %s passenger cards with a metro journey in each calendar week of the window; staff and "
           "service cards left out (rate card 3.3)." % format(len(M.regular), ","),
           "Passes: the hall of check-in, the hall of check-out and the interchange passage wherever the rider "
           "changed trains (3.4); a journey without a check-out counts its check-in hall only.",
           "Changes at Centraal read from each journey's duration: on weekday peaks (07:00 to 09:30, 16:00 to 18:30) "
           "north runs through to east and west to south."])
    bk = c["bookings"]
    sheet("Make-good", "Make-good owed on the autumn 2026 bookings",
          ["Booking", "Advertiser", "Package", "Flight", "Make-good (hours)"],
          [[b["booking_ref"], b["advertiser"], b["package"], "%s to %s" % (b["start"].strftime("%d %b"),
                                                                           b["end"].strftime("%d %b")),
            c["make_good"][b["booking_ref"]]["make_good"]] for b in bk],
          [12, 26, 16, 18, 14], {4: "#,##0"},
          ["Dark hours above 0.5 per cent of booked screen-hours, in whole hours, part of an hour counted as an hour "
           "(general terms 6.3).",
           "Player log times are UTC and were read in Ravelmond time; re-cablings dated from the receiving player's "
           "display report, not the register's entry."])
    sheet("Screens 2027", "Screens on sale on 1 January 2027",
          ["Package", "Code", "Screens"],
          [[pk[k][0], k, c["screens"][k]] for k in pk], [20, 8, 10], {2: "0"},
          ["From the screen register of 12 November 2026: one screen to a position; planned hangings and take-downs "
           "dated on or before 1 January counted; screens held outside the packages left out."])
    sheet("Net revenue", "Net revenue from the autumn 2026 bookings, by package",
          ["Package", "Code", "Net revenue (EUR)"],
          [[pk[k][0], k, r10(c["revenue"][k])] for k in pk], [20, 8, 16], {2: "#,##0"},
          ["Invoiced value excluding VAT, less credit notes, less the agency commission due at each agency's contract "
           "rate (general terms 8.2, 8.3); rounded to the nearest 10 euros."])
    for ws in wb.worksheets:
        ws.sheet_view.showGridLines = False
        ws.print_title_rows = "3:3"
    wb.save(path)
    IO.repack_xlsx(path, "Floortje Brugman", "Floortje Brugman", "2026-11-13T13:40:00Z", "2026-11-13T15:55:00Z",
                   "Tier G 2027", "Spoorbeeld Media B.V.")


def write_all(target, golden, gen):
    os.makedirs(golden, exist_ok=True)
    os.makedirs(gen, exist_ok=True)
    c = compute(target)
    f = figures(c)
    workbook(c, f, os.path.join(golden, BOOK))
    chart(c, f, os.path.join(golden, PAGE))
    json.dump(f, open(os.path.join(gen, "figures.json"), "w"), indent=1, sort_keys=True)
    return c, f
