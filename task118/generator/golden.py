"""The golden deliverables: the siting workbook and the ranked chart."""
import datetime as dt
import io
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker
import openpyxl
from openpyxl.styles import Alignment, Font

import params as P
import pack as K

XLSX = "dispatch_team_siting_2027.xlsx"
PNG = "lateness_saved_by_station.png"
PICK_BLUE = "#1f5a8a"
REST_GREY = "#a9bccb"


def r100(v):
    return int(round(v / 100.0) * 100)


def _sheet(wb, title, rows, header_row, formats, widths, notes):
    """rows start at row 1; header_row is 1-based; formats maps a column letter to a number format for the body."""
    ws = wb.create_sheet(title)
    for r in rows:
        ws.append(list(r))
    ws["A1"].font = Font(bold=True, size=12)
    for c in ws[header_row]:
        c.font = Font(bold=True)
        c.alignment = Alignment(wrap_text=True, vertical="bottom")
    for col, fmt in formats.items():
        for row in range(header_row + 1, ws.max_row + 1):
            cell = ws["%s%d" % (col, row)]
            if isinstance(cell.value, (int, float)):
                cell.number_format = fmt
    for col, w in widths.items():
        ws.column_dimensions[col].width = w
    ws.freeze_panes = "A%d" % (header_row + 1)
    ws.append([])
    for n in notes:
        ws.append([n])
        ws["A%d" % ws.max_row].font = Font(italic=True, size=9, color="555555")
    ws.print_title_rows = "%d:%d" % (header_row, header_row)
    return ws


def write(folder, fig):
    os.makedirs(folder, exist_ok=True)
    st = fig["stations"]
    order = sorted(st, key=lambda c: -st[c])
    pick, ru = fig["pick"], fig["runner_up"]
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    siting = [("%s takes the most passenger lateness off the network: %s passenger-minutes a weekday, %s ahead of %s"
               % (pick, "{:,}".format(r100(st[pick])), "{:,}".format(fig["gap"]), ru),),
              ("Platform dispatch team, 2027 Rail Plan. Autumn 2026 weekdays as they ran, 7 September to 27 November.",),
              (),
              ("Rank", "Station", "Line", "Saving (passenger-minutes a weekday)")]
    for i, c in enumerate(order):
        siting.append((i + 1, c, P.LINE_NAME[P.SHORTLIST[c][0]], r100(st[c])))
    siting += [(),
               ("Pick", pick, P.LINE_NAME[P.SHORTLIST[pick][0]], r100(st[pick])),
               ("Runner-up", ru, P.LINE_NAME[P.SHORTLIST[ru][0]], r100(st[ru])),
               ("Gap", "", "", fig["gap"])]
    _sheet(wb, "Siting", siting, 4, {"D": "#,##0"}, {"A": 11, "B": 17, "C": 17, "D": 22},
           ["Saving: the passenger lateness taken off every weekday passenger train with the team removing three fifths "
            "of each dwell overrun at the station, trains booked to depart from 06:30 up to 19:30 (siting brief, section 3).",
            "Each unit is followed into its later workings that day: a working that left late four minutes after its "
            "unit arrived leaves four minutes after the replayed arrival, never before its booked time.",
            "Passengers as counted in the census of Tuesday 13 October 2026. Averages over the 60 weekdays, rounded to "
            "the nearest 100; ranks from the unrounded averages."])
    gates = [("Passengers through the gates, Tuesday 13 October 2026",),
             ("Gated shortlisted stations, all arrays, the BST day.",),
             (),
             ("Station", "Entered", "Left")]
    for s in P.GATED:
        g = fig["gates"][s]
        gates.append((s, g["entered"], g["left"]))
    _sheet(wb, "Gatelines", gates, 4, {"B": "#,##0", "C": "#,##0"}, {"A": 18, "B": 11, "C": 11},
           ["From each array's cumulative 16-bit counters, read every quarter-hour in UTC; a counter that wraps to zero "
            "carries on from there.",
            "A tidal array set to exit only in its station's peak keeps counting in its entries counter; those passages "
            "are counted as people leaving.",
            "AMP-1's controller restarted at 07:31 and resumed from the counters it saved at 02:00; the morning quarter "
            "is taken from that save."])
    repay = [("Delay Repay compensation paid, weekday journeys to or from Ravelstoke Central",),
             ("Journeys 7 September to 27 November 2026, pounds, by how late the train reached the passenger's "
              "destination station.",),
             (),
             ("Line", "15 to 29 minutes", "30 to 59 minutes", "60 minutes or more")]
    for ln in P.LINES:
        repay.append((P.LINE_NAME[ln],) + tuple(int(round(fig["repay"]["%s|%s" % (ln, b[0])])) for b in P.ASK_BANDS))
    _sheet(wb, "Delay Repay", repay, 4, {"B": '"£"#,##0', "C": '"£"#,##0', "D": '"£"#,##0'},
           {"A": 18, "B": 13, "C": 13, "D": 13},
           ["Every approved payment in Cardale's claims extract of 15 January 2027, appeal top-ups included.",
            "Each claim matched to its train in the working timetable and banded by that train's lateness at the "
            "destination in the running record; a return ticket's claim names the ticket's stations and is matched the "
            "other way round.",
            "A claim dated the day it was first made, whose train was not 15 minutes late that day, is dated by the "
            "weekday its train was."])
    buf = io.BytesIO()
    wb.save(buf)
    K.ooxml_finish(buf.getvalue(), os.path.join(folder, XLSX), "xlsx", K.RAIL, "Julia Clayton", K.RAIL,
                   dt.datetime(2027, 1, 19, 9, 5, 0), dt.datetime(2027, 1, 21, 15, 48, 0),
                   sheets=["Siting", "Gatelines", "Delay Repay"])
    # chart: ranked bars, the pick picked out, the gap annotated
    fig_, ax = plt.subplots(figsize=(7.6, 4.1), dpi=150)
    names = list(reversed(order))
    vals = [r100(st[c]) for c in names]
    cols = [PICK_BLUE if c == pick else REST_GREY for c in names]
    ax.barh(names, vals, color=cols, height=0.62)
    for y, (c, v) in enumerate(zip(names, vals)):
        if c == pick:
            ax.text(v + 50, y, "{:,}, {:,} ahead of {}".format(v, fig["gap"], ru), va="center", fontsize=8.5,
                    color=PICK_BLUE, fontweight="bold")
        else:
            ax.text(v + 50, y, "{:,}".format(v), va="center", fontsize=8.5, color="#333333")
    ax.set_xlabel("Passenger-minutes of lateness taken off the network a weekday (nearest 100)", fontsize=9)
    ax.set_title("%s takes the most lateness off the network's weekday trains" % pick, fontsize=10.5, loc="left")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(labelsize=8.5)
    ax.set_xlim(0, max(vals) * 1.42)
    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, _p: "{:,.0f}".format(x)))
    fig_.text(0.01, 0.01, "Ravelstoke Rail, Performance and Planning. Autumn 2026 weekdays as they ran; census of "
              "13 October 2026.", fontsize=7, color="#666666")
    fig_.tight_layout(rect=(0, 0.03, 1, 1))
    buf = io.BytesIO()
    fig_.savefig(buf, format="png", metadata={"Software": None})
    plt.close(fig_)
    with open(os.path.join(folder, PNG), "wb") as fh:
        fh.write(buf.getvalue())
