"""task157 architecture 3: the golden deliverables. The forecast workbook (the notice's routes, each route's autumn
punctuality and closure forecast against the floor, reliability, the unserved stops' boardings) and the chart of
each route's autumn and closure punctuality against the 80 per cent line."""
from __future__ import annotations

import os

import params as P

ROUTE_NAMES = {r: P.ROUTES[r]["name"] for r in P.ROUTE_ORDER}


def write_workbook(path, fig):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    wb = Workbook()
    ws = wb.active
    ws.title = "Notice"
    bold = Font(bold=True)
    hdr_fill = PatternFill("solid", fgColor="DDE3EA")
    named = fig["call"]["routes"]
    ws.append(["Routes %s forecast below the 80%% punctuality floor during the Thornsby Bridge closure" %
               (", ".join(named[:-1]) + " and " + named[-1])])
    ws["A1"].font = Font(bold=True, size=12)
    ws.append(["Disruption Notice under Schedule 7, 7.6: closure 11 January to 28 March 2027, notice due 21 December "
               "2026. Prepared 11 December 2026, Bus Network Performance."])
    ws.append([])
    ws.append([])
    head = ["Route", "Service", "Autumn 2026 punctuality (%)", "Closure forecast (%)", "Below 80% floor",
            "What moves it in the closure"]
    ws.append(head)
    for c in ws[5]:
        c.font = bold
        c.fill = hdr_fill
        c.alignment = Alignment(wrap_text=True, vertical="top")
    why = {"41": "Diverted via the Ring Road crossing (13 min in the weekday peaks, 10 min at other times); "
                 "Thornsby Road and Thornsby Quay not served",
           "27": "Drivers stepping off route 41 at Merchant Row take over its departures 3 min after the 41 arrives",
           "58": "Drivers stepping off route 41 at Merchant Row take over its departures 4 min after the 41 arrives",
           "33": "Relieved off route 41 after a personal needs break (26 min or more): the delay is absorbed",
           "6": "Ring Road crossing, 2 min in the weekday peaks", "12": "Ring Road crossing, 2 min in the weekday peaks",
           "14": "No change", "19": "No change", "22": "No change"}
    for r in P.ROUTE_ORDER:
        a = fig["autumn"][r]
        f = fig["forecast"][r]
        below = r in named
        ws.append([r, ROUTE_NAMES[r], round(a, 1), round(f), "Yes" if below else "No", why[r]])
    for row in ws.iter_rows(min_row=6, max_row=5 + len(P.ROUTE_ORDER)):
        row[2].number_format = "0.0"
        row[3].number_format = "0"
    ws.append([])
    ws.append(["Forecast to the nearest whole per cent; the notice turns only on which side of 80% each route falls."])
    ws.column_dimensions["A"].width = 7
    ws.column_dimensions["B"].width = 50
    for col in "CDE":
        ws.column_dimensions[col].width = 13
    ws.column_dimensions["F"].width = 88
    ws.freeze_panes = "C6"
    # reliability
    ws2 = wb.create_sheet("Reliability")
    ws2.append(["Lot 2 reliability %.2f%%, 1 September to 6 December 2026: the reference Schedule 7 keeps through "
                "the closure (7.6.4)" % fig["ask_a"]["reliability_lot"]])
    ws2["A1"].font = Font(bold=True, size=12)
    ws2.append([])
    ws2.append(["Route", "Scheduled km", "Lost km not excused", "Reliability (%)"])
    for c in ws2[3]:
        c.font = bold
        c.fill = hdr_fill
    A = fig["ask_a"]
    for r in P.ROUTE_ORDER:
        ws2.append([r, round(A["sched_km"][r], 1), round(A["op_km"][r]), round(A["reliability"][r], 2)])
    ws2.append(["Lot 2", round(sum(A["sched_km"].values()), 1), round(A["op_km_total"]), round(A["reliability_lot"], 2)])
    for c in ws2[ws2.max_row]:
        c.font = bold
    for row in ws2.iter_rows(min_row=4, max_row=ws2.max_row):
        row[1].number_format = "#,##0.0"
        row[2].number_format = "#,##0"
        row[3].number_format = "0.00"
    ws2.append([])
    ws2.append(["Lost km: journeys and part journeys lost (7.4.1), from the control room log and the depot's "
                "returns, each journey once; returned work the AVL saw run is not lost; excused causes (7.5.1) left out."])
    for col, w in zip("ABCD", (10, 16, 22, 16)):
        ws2.column_dimensions[col].width = w
    ws2.freeze_panes = "A4"
    # unserved stops
    ws3 = wb.create_sheet("Unserved stops")
    ws3.append(["The closure leaves about %d weekday boardings a day without a stop at Thornsby Road, Bridge End "
                "and Thornsby Quay" % round(fig["ask_b"]["total"])])
    ws3["A1"].font = Font(bold=True, size=12)
    ws3.append([])
    ws3.append(["Direction", "AM peak (07:30-09:30)", "PM peak (16:00-18:30)", "Other times", "All day"])
    for c in ws3[3]:
        c.font = bold
        c.fill = hdr_fill
    B = fig["ask_b"]
    for d, lab in (("I", "Towards the city (inbound)"), ("O", "Towards Ravensholme (outbound)")):
        cells = [B["cells"][(d, b)] for b in ("AM peak", "PM peak", "Other times")]
        ws3.append([lab] + [round(v) for v in cells] + [round(sum(cells))])
    ws3.append(["Both directions"] + [round(B["cells"][("I", b)] + B["cells"][("O", b)])
                                      for b in ("AM peak", "PM peak", "Other times")] + [round(B["total"])])
    for c in ws3[ws3.max_row]:
        c.font = bold
    ws3.append([])
    ws3.append(["Route 41 ticket machine sales at fare stages 3 and 4, average of the %d weekdays in October and "
                "November 2026. Each sale is placed on the journey its bus was running in the AVL; re-sent uploads "
                "counted once; two machines' clocks corrected from 25 October." % B["weekdays"]])
    ws3.column_dimensions["A"].width = 32
    for col in "BCDE":
        ws3.column_dimensions[col].width = 20
    ws3.freeze_panes = "A4"
    ws4 = wb.create_sheet("Notes")
    notes = [
        ("Prepared", "11 December 2026, Bus Network Performance, for the Disruption Notice due 21 December 2026"),
        ("Punctuality", "Schedule 7, 7.2.1: departures from timing points (not a journey's last), one minute early to "
                        "5:59 late, in local time; departures the AVL did not record left out"),
        ("Autumn record", "AVL timing point events, 1 September to 6 December 2026, converted from UTC; re-sent "
                          "messages counted once"),
        ("Closure", "Traffic management plan TMP-2026-117 v2: 11 January to 28 March 2027; route 41 keeps its "
                    "registered timetable; the duty schedule in force to 3 April 2027"),
        ("Forecast", "The autumn record replayed with the closure's minutes, passed on to each bus's next journey "
                     "and to the piece of work each relieved driver takes over"),
        ("Reliability", "Schedule 7, 7.4 and 7.5; scheduled km from the registered timetable, school journeys on "
                        "term days only"),
    ]
    ws4.append(["Item", "Basis"])
    for c in ws4[1]:
        c.font = bold
        c.fill = hdr_fill
    for k, v in notes:
        ws4.append([k, v])
    ws4.column_dimensions["A"].width = 16
    ws4.column_dimensions["B"].width = 110
    wb.save(path)


def write_chart(path, fig):
    import matplotlib
    matplotlib.use("Agg")
    matplotlib.rcParams["svg.hashsalt"] = "task157-closure"
    matplotlib.rcParams["svg.fonttype"] = "none"
    matplotlib.rcParams["font.family"] = "DejaVu Sans"
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    INK, MUTED, GRID, SURF = "#0b0b0b", "#52514e", "#e6e5e1", "#fcfcfb"
    AUT, FC = "#2a78d6", "#eb6834"
    routes = P.ROUTE_ORDER
    named = fig["call"]["routes"]
    a = [fig["autumn"][r] for r in routes]
    f = [fig["forecast"][r] for r in routes]
    fig_, ax = plt.subplots(figsize=(9.2, 5.2), dpi=100)
    fig_.patch.set_facecolor(SURF)
    ax.set_facecolor(SURF)
    xs = list(range(len(routes)))
    ax.axhline(P.FLOOR, color=INK, linewidth=1.2, linestyle=(0, (5, 3)), zorder=1)
    ax.text(2.5, P.FLOOR - 1.2, "80% punctuality floor", fontsize=9, ha="center", va="top", color=INK)
    for x, av, fv, r in zip(xs, a, f, routes):
        ax.plot([x, x], [av, fv], color="#a9a8a2", linewidth=2, solid_capstyle="round", zorder=2)
        ax.scatter([x], [av], s=64, color=AUT, edgecolors=SURF, linewidths=2, zorder=3)
        ax.scatter([x], [fv], s=72, color=FC, marker="D", edgecolors=SURF, linewidths=2, zorder=3)
        if r in named:
            ax.annotate("%.0f%%" % fv, (x, fv), xytext=(9, -1), textcoords="offset points", fontsize=9,
                        va="center", color=INK, fontweight="bold")
    ax.set_xticks(xs)
    ax.set_xticklabels(["Route %s" % r for r in routes], fontsize=9, color=MUTED)
    ax.set_ylabel("Departures on time (%)", fontsize=9, color=MUTED)
    ax.set_ylim(40, 95)
    ax.set_xlim(-0.6, len(routes) - 0.3)
    ax.tick_params(axis="y", labelsize=9, colors=MUTED)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    for sp in ("left", "bottom"):
        ax.spines[sp].set_color("#c9c8c2")
    ax.grid(axis="y", color=GRID, linewidth=0.7)
    ax.set_axisbelow(True)
    handles = [Line2D([], [], marker="o", color=AUT, linestyle="", markersize=8,
                      label="Autumn 2026 (AVL, 1 Sep to 6 Dec)"),
               Line2D([], [], marker="D", color=FC, linestyle="", markersize=8,
                      label="Forecast for the closure (11 Jan to 28 Mar 2027)")]
    ax.legend(handles=handles, loc="lower left", fontsize=8.5, frameon=False)
    fig_.suptitle("Routes %s fall below the 80%% floor during the Thornsby Bridge closure"
                  % (", ".join(named[:-1]) + " and " + named[-1]), x=0.02, ha="left", fontsize=11.5, color=INK,
                  fontweight="bold")
    ax.set_title("Lot 2 punctuality by route; labels give the forecast for the routes the Disruption Notice names",
                 loc="left", fontsize=9, color=MUTED)
    fig_.text(0.02, 0.012, "Source: AVL timing point events; Thornsby Bridge traffic management plan v2; Saltmeadow "
              "duty schedule, winter 2026/27.", fontsize=7.5, color=MUTED)
    fig_.tight_layout(rect=(0, 0.03, 1, 0.97))
    fig_.savefig(path, format="svg", metadata={"Date": None, "Creator": None}, facecolor=SURF)
    plt.close(fig_)
