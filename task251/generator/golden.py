"""task251 goldens: the workbook for the spring round and the annual count report (the flagged stations with their
2027 count error, the maintenance figures of TDP-03 section 7 by district and quarter, the notes) and the chart of every
station's 2027 count error against the 5 per cent band."""
import os

import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

import build as B
import params as P
import postprocess

XLSX = "count_stations_flagged_2027.xlsx"
PNG = "count_station_errors_2027.png"
FLAG = "#eb6834"          # categorical slot 2: flagged, to the spring round
MEET = "#2a78d6"          # categorical slot 1: meets the standard
INK, INK2 = "#0b0b0b", "#52514e"
QH = ["Q1 (Jan-Mar)", "Q2 (Apr-Jun)", "Q3 (Jul-Sep)", "Q4 (Oct-Dec)"]


def _head(ws, row, head, height=30):
    thin = Side(style="thin", color="A6ADB8")
    for j, h in enumerate(head, 1):
        c = ws.cell(row=row, column=j, value=h)
        c.font = Font(bold=True, size=9.5)
        c.fill = PatternFill("solid", fgColor="E4E9F0")
        c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
        c.border = Border(bottom=thin)
    ws.row_dimensions[row].height = height


def _widths(ws, widths):
    for k, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(k)].width = w


def _title(ws, title, sub):
    ws["A1"] = title
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = sub
    ws["A2"].font = Font(italic=True, size=9, color="52514E")


def _order(G):
    reg = G["D"]["reg"].set_index("station")
    return sorted(G["errors"], key=lambda s: (P.DISTRICTS.index(reg.loc[s, "district"]), int(s[1:3]), s))


def workbook(path, fig):
    G = fig["_golden"]
    reg = G["D"]["reg"].set_index("station")
    c, a = fig["call"], fig["asks"]
    wb = Workbook()
    ws = wb.active
    ws.title = "Flagged stations"
    _title(ws, "Count stations flagged for 2027: %d of %d, to the spring 2028 recalibration round" % (c["count"],
                                                                                                    c["stations"]),
           "2027 count error beyond 5 per cent either way (TDP-03 section 5), for the annual count report and the "
           "spring round. Traffic Data Program, 1 March 2028.")
    _head(ws, 4, ["Station", "Road", "Location", "District", "Controller", "Validation site"])
    hist = G["D"]["hist"].set_index("new_station")
    for s in c["listed"]:
        ctl = reg.loc[s, "controller"]
        if s in hist.index:
            ctl = "%s since %s" % (ctl, pd.Timestamp(hist.loc[s, "from_date"]).strftime("%-d %B"))
        ws.append([s, reg.loc[s, "road"], reg.loc[s, "location"], reg.loc[s, "district"], ctl,
                   reg.loc[s, "validation_site"]])
    _widths(ws, [10, 8, 30, 10, 18, 12])
    ws.freeze_panes = "A5"

    ws2 = wb.create_sheet("Maintenance 2027")
    _title(ws2, "Maintenance of the count stations, 2027 (TDP-03 section 7)",
           "For the annual count report. Districts as in the station register; quarters by local date.")
    r = 4
    for label, key in (("Maintenance visits", "visits"), ("Power failures", "failures")):
        ws2.cell(row=r, column=1, value=label).font = Font(bold=True, size=10)
        r += 1
        _head(ws2, r, ["District"] + QH + ["2027"])
        r += 1
        tot = [0, 0, 0, 0]
        for d in P.DISTRICTS:
            vals = [a[key][d][str(q)] for q in (1, 2, 3, 4)]
            ws2.append([d] + vals + [sum(vals)])
            tot = [t + v for t, v in zip(tot, vals)]
            r += 1
        ws2.append(["All districts"] + tot + [sum(tot)])
        for j in range(1, 7):
            ws2.cell(row=r, column=j).font = Font(bold=True)
        r += 3
        ws2.cell(row=r - 2, column=1)
    _widths(ws2, [16, 13, 13, 13, 13, 10])

    ws3 = wb.create_sheet("Notes")
    notes = [
        "Notes",
        "2027 count error: the vehicles the station counted in the hours of 2027 it counted, both directions and every "
        "lane, divided by the vehicles that passed it in those hours, less one (TDP-03 section 5). Flagged when beyond "
        "5 per cent either way.",
        "Vehicles that passed: each hour's count divided by the station and direction's loops-to-video ratio on its "
        "summer validation day (Northline, July and August 2027), by one less the share of vehicles the loops lose "
        "at the hour's occupancy and, while the station ran a TCX-2 controller, by one less the share the TCX-2 misses "
        "at the day's mean temperature at Halbrook airport. Both are measured on the five Kessel River bridges, where "
        "both approaches count the same vehicles: in queued hours the upstream approach counts fewer than the approach "
        "past the deck, and on the three bridges with a TCX-2 on one side and a TCX-4 on the other the TCX-2 side "
        "falls behind as the days get colder. The validation days were summer weekdays with no queued hour and no "
        "cold.",
        "Maintenance visits: days one of %s's technicians was at a station, from the contractor's work orders; "
        "controller resets done from the contractor's office are not visits. Power failures: losses of mains power at "
        "a station's controller, from the TCX-4 controllers' events and from the breaks in the TCX-2 stations' hourly "
        "record; the two controller replacements are not power failures." % P.CONTRACTOR_MAINT,
        "Stations under their current numbers: R08-01 became R08-05 on 12 May 2027 and R19-01 became R19-03 on "
        "21 September 2027.",
        "Data as of 7 January 2028: %s, %s, %s, %s, %s, %s, %s." % (
            B.FILES["hourly"], B.FILES["validation"], B.FILES["register"], B.FILES["network"], B.FILES["weather"],
            B.FILES["events"], B.FILES["orders"]),
    ]
    for k, t in enumerate(notes, 1):
        cell = ws3.cell(row=k, column=1, value=t)
        cell.alignment = Alignment(wrap_text=True, vertical="top")
        if k == 1:
            cell.font = Font(bold=True, size=12)
    ws3.column_dimensions["A"].width = 118
    wb.save(path)


def chart(path, fig):
    G = fig["_golden"]
    reg = G["D"]["reg"].set_index("station")
    e, listed = G["errors"], G["listed"]
    order = _order(G)
    n = len(order)
    plt.rcParams["font.family"] = "DejaVu Sans"
    f, ax = plt.subplots(figsize=(8.2, 9.6), dpi=150)
    ax.axvspan(-5, 5, color="#EEF1F5", zorder=0)
    for x in (-5, 5):
        ax.axvline(x, color=INK2, lw=1.0, ls=(0, (4, 3)), zorder=1)
    ax.text(5.12, n - 0.25, "+5 %", fontsize=7.4, color=INK2, va="bottom")
    ax.text(-5.12, n - 0.25, "−5 %", fontsize=7.4, color=INK2, va="bottom", ha="right")
    ax.axvline(0, color="#C9CDD3", lw=0.8, zorder=1)
    labels = []
    prev = None
    for i, s in enumerate(order):
        y = n - 1 - i
        d = reg.loc[s, "district"]
        if prev is not None and d != prev:
            ax.axhline(y + 0.5, color="#B9BEC6", lw=0.7, zorder=1)
        prev = d
        v = 100 * e[s]
        col = FLAG if s in listed else MEET
        ax.plot([0, v], [y, y], color=col, lw=1.4, alpha=0.55, zorder=2, solid_capstyle="round")
        ax.plot([v], [y], "o", ms=6.5, color=col, mec="white", mew=1.0, zorder=3)
        labels.append("%s  %s  %s" % (s, reg.loc[s, "road"], reg.loc[s, "controller"]))
    ax.set_yticks(range(n - 1, -1, -1))
    ax.set_yticklabels(labels, fontsize=7.0, color=INK2)
    for lab, s in zip(ax.get_yticklabels(), order):
        if s in listed:
            lab.set_color(INK)
            lab.set_fontweight("bold")
    ax.set_xlim(-10, 10)
    ax.set_ylim(-0.8, n + 0.6)
    ax.set_xticks([-10, -5, 0, 5, 10])
    ax.set_xticklabels(["−10 %", "−5 %", "0", "+5 %", "+10 %"], fontsize=7.4, color=INK2)
    ax.set_xlabel("2027 count error: vehicles counted against vehicles that passed, %", fontsize=7.8, color=INK2)
    ax.grid(axis="x", color="#E6E6E4", lw=0.6, zorder=0)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color("#B9BEC6")
    starts = {}
    for i, s in enumerate(order):
        starts.setdefault(reg.loc[s, "district"], []).append(n - 1 - i)
    for d, ys in starts.items():
        ax.text(9.8, max(ys) + 0.1, d, ha="right", va="top", fontsize=7.8, color=INK2, fontstyle="italic")
    word = {3: "Three", 4: "Four", 5: "Five", 6: "Six", 7: "Seven"}.get(len(listed), str(len(listed)))
    f.suptitle("%s of the %d count stations undercounted 2027 traffic by more than 5 per cent" % (word, n), x=0.04,
               ha="left", fontsize=11.2, fontweight="bold", color=INK, y=0.985)
    f.text(0.04, 0.955, "Each station's sensitivity from its summer validation day, the vehicles the loops lose in queued "
           "traffic and, on a TCX-2,\nthe vehicles it misses on cold days, as the river bridges' paired approaches "
           "measure them, carried through every hour it counted", fontsize=7.6, color=INK2, ha="left", va="top")
    leg = [Line2D([0], [0], marker="o", color=FLAG, ls="-", lw=1.4, label="flagged, to the spring round (%d)"
                  % len(listed), markersize=6.5, mec="white"),
           Line2D([0], [0], marker="o", color=MEET, ls="-", lw=1.4, label="meets the standard (%d)" % (n - len(listed)),
                  markersize=6.5, mec="white")]
    ax.legend(handles=leg, loc="upper left", fontsize=7.2, frameon=False, bbox_to_anchor=(-0.02, -0.05), ncol=2)
    f.text(0.04, 0.008, "Controllers as in the register: R08-05 and R19-03 ran a TCX-2 until 12 May and 21 September "
           "2027.\nSource: TrafficVault hourly counts 2027; Northline validation counts, July and August 2027; Halbrook A "
           "daily data 2027; Traffic Data Program, %s, 1 March 2028." % P.ORG, fontsize=5.9, color=INK2,
           va="bottom")
    f.subplots_adjust(left=0.17, right=0.97, top=0.915, bottom=0.095)
    f.savefig(path, dpi=150, metadata={"Software": None})
    plt.close(f)


def write(outdir, fig):
    os.makedirs(outdir, exist_ok=True)
    x, p = os.path.join(outdir, XLSX), os.path.join(outdir, PNG)
    workbook(x, fig)
    postprocess.scrub(x, "Traffic Data Program", "2028-03-01")
    postprocess.finish_office(x, "2028-02-28T15:20:00Z", "2028-03-01T10:12:00Z", P.ORG)
    chart(p, fig)
    return x, p
