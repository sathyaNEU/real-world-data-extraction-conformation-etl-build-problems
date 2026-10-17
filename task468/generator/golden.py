"""The golden deliverable, computed from the shipped pack: the nominations workbook (the five, every candidate's verdict
and lowest hour, on-time departures against the timetable, a chart of the lowest hours against the standard);
generator/figures.json carries every figure."""
import json
import os

import numpy as np
import pandas as pd

import bundle as B
import methods as M
import world as W

STOP_NAME = {v[0]: v[3] for v in W.STOPS.values()}


def compute(target):
    t = B.events(target)
    rv = B.review(target)
    ride = B.ridership(target)
    est, rvw, c = M.golden(t, rv)
    rows, five, below = M.verdicts(est, ride)
    raw = M.estimate(c, M.shares(rvw, None))
    prop = M.proportional(c)
    sh = M.shares(rvw, "w")
    sh_raw = M.shares(rvw, None)
    ot = M.on_time(c)
    ot_k = M.on_time(c, counts=True)
    a = c[c["attributed"]]
    return dict(t=t, c=c, rvw=rvw, est=est, rows=rows, five=five, below=below, raw=raw, prop=prop, sh=sh,
                sh_raw=sh_raw, ot=ot, ot_k=ot_k, att_n=a.groupby("route").size().to_dict(), ride=ride)


def r1(v):
    return float(np.floor(v * 10 + 0.5) / 10)


def figures(g):
    rows = {x["route"]: x for x in g["rows"]}
    lo_raw = {r: M.lowest(g["raw"], r) for r in W.CANDIDATES}
    lo_prop = {r: M.lowest(g["prop"], r) for r in W.CANDIDATES}
    qual = [x["route"] for x in sorted([x for x in g["rows"] if x["meets"]], key=lambda x: -x["boardings"])]
    f = {
        "call": {"five": g["five"], "first_left_out": g["below"], "qualifying": qual},
        "components": {
            "counting_days": M.N,
            "events_in_hours": int(len(g["c"])),
            "no_trip_in_hours": int((~g["c"]["attributed"]).sum()),
            "mall_share_17_weighted_pct": int(round(100 * g["sh"][("A",)]["17"])),
            "mall_share_17_raw_pct": int(round(100 * g["sh_raw"][("A",)]["17"])),
            "riverside_share_weighted_pct": int(round(100 * g["sh"][("B",)]["9"])),
            "riverside_share_proportional_pct": None,
        },
        "verdicts": {r: {"meets": bool(rows[r]["meets"]), "lowest": r1(rows[r]["lowest"]), "hour": int(rows[r]["hour"]),
                         "boardings": int(rows[r]["boardings"])} for r in W.CANDIDATES},
        "rivals": {
            "raw_review": {"five": M.verdicts(g["raw"], g["ride"])[1], "route17_lowest": r1(lo_raw["17"][0]),
                           "route2_lowest": r1(lo_raw["2"][0])},
            "proportional": {"five": M.verdicts(g["prop"], g["ride"])[1], "route9_lowest": r1(lo_prop["9"][0]),
                             "route17_lowest": r1(lo_prop["17"][0])},
        },
        "on_time_pct": {r: int(np.floor(g["ot"][r] + 0.5)) for r in W.CANDIDATES},
        "on_time_n": {r: int(g["att_n"][r]) for r in W.CANDIDATES},
        "on_time_k": {r: int(g["ot_k"][r]) for r in W.CANDIDATES},
        "review": {"bus_days_drawn_month": 250, "events_reviewed": int(len(g["rvw"]))},
        "routes": list(W.CANDIDATES),
        "stated": {"guidance_sections": ["3.3", "3.4", "5.1"]},
    }
    sh_b = g["c"][~g["c"]["attributed"] & (g["c"]["stop"] == "B")]
    att_b = g["c"][g["c"]["attributed"] & (g["c"]["stop"] == "B")]
    f["components"]["riverside_share_proportional_pct"] = int(round(100 * (att_b["route"] == "9").mean()))
    return f


def write_workbook(path, f):
    from openpyxl import Workbook
    from openpyxl.chart import BarChart, LineChart, Reference
    from openpyxl.chart.series import SeriesLabel
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    wb = Workbook()
    ws = wb.active
    ws.title = "Nominations"
    bold = Font(name="Calibri", bold=True)
    head = PatternFill("solid", fgColor="D9E1F2")
    keep = PatternFill("solid", fgColor="E2EFDA")
    thin = Side(style="thin", color="A6A6A6")
    five = f["call"]["five"]
    ws.append(["Frequent Transit Corridors Program, FY2027: Larkhaven Transit's nominations"])
    ws["A1"].font = Font(name="Calibri", bold=True, size=13)
    ws.append(["Service Planning and Grants, for the Transportation Committee. Prepared October 30, 2026."])
    ws.append(["Nominate Routes %s (in order of average weekday boardings). First qualifying route left out: Route %s."
               % (", ".join(five[:-1]) + " and " + five[-1], f["call"]["first_left_out"])])
    ws["A3"].font = Font(name="Calibri", bold=True, size=11, color="1F4E79")
    ws.append([])
    ws.append(["Route", "Name", "Designated stop", "Lowest hourly average (departures)", "Lowest hour begins",
               "Meets the standard", "Average weekday boardings", "Nomination"])
    for c in ws[5]:
        c.font = bold
        c.fill = head
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = Border(bottom=thin)
    order = sorted(W.CANDIDATES, key=lambda r: -f["verdicts"][r]["boardings"])
    for r in order:
        v = f["verdicts"][r]
        nom = ("Nominated, %d of 5" % (five.index(r) + 1)) if r in five else (
            "First qualifying route left out" if r == f["call"]["first_left_out"] else (
                "Qualifies, not nominated" if v["meets"] else None))
        code = W.STOPS[W.STOP_OF[r]][0]
        ws.append([int(r), W.ROUTE_NAMES[r], "%s %s" % (code, STOP_NAME[code]), v["lowest"],
                   "%d %s" % ((v["hour"] - 1) % 12 + 1, "a.m." if v["hour"] < 12 else "p.m."),
                   "Yes" if v["meets"] else "No", v["boardings"], nom])
        if r in five:
            for c in ws[ws.max_row]:
                c.fill = keep
    for row in ws.iter_rows(min_row=6, max_row=ws.max_row):
        row[0].alignment = Alignment(horizontal="center")
        row[3].number_format = "0.0"
        row[4].alignment = Alignment(horizontal="center")
        row[5].alignment = Alignment(horizontal="center")
        row[6].number_format = "#,##0"
        row[7].alignment = Alignment(indent=2)
    end = ws.max_row
    ws.append([])
    notes = [
        "The standard (guidance 3.3): at least four departures in each clock hour from 6 a.m. to 7 p.m., averaged over "
        "the %d counting days (weekdays, January to June 2026, state holidays out)." % f["components"]["counting_days"],
        "Departures from the AVL records of both systems, Arbor to March 31 and Quinnell from the cutover. Of the %s "
        "departures in the counting hours, %s carry no trip; each stop's are shared among its routes by Service "
        "Quality's review, each reviewed event weighted by its bus-day's events without a trip (the review draws one per "
        "bus-day) and each month by its bus-days listed over drawn." % ("{:,}".format(f["components"]["events_in_hours"]),
                                                                       "{:,}".format(f["components"]["no_trip_in_hours"])),
        "Weighted, Route 17 is %d per cent of the Transit Mall's departures without a trip (the review's unweighted "
        "mix gives %d per cent and leaves it short in its lowest hour at %.1f)." % (
            f["components"]["mall_share_17_weighted_pct"], f["components"]["mall_share_17_raw_pct"],
            f["rivals"]["raw_review"]["route17_lowest"]),
    ]
    for n in notes:
        ws.append([n])
        ws.cell(ws.max_row, 1).alignment = Alignment(wrap_text=True, vertical="top")
        ws.merge_cells(start_row=ws.max_row, start_column=1, end_row=ws.max_row, end_column=8)
        ws.row_dimensions[ws.max_row].height = 30
    for col, w in zip("ABCDEFGH", (7, 21, 40, 14, 11, 11, 13, 28)):
        ws.column_dimensions[col].width = w
    ws.row_dimensions[5].height = 45
    ws.freeze_panes = "C6"
    # the chart: each candidate's lowest hourly average against the standard
    cs = wb.create_sheet("Chart")
    cs.append(["Route", "Lowest hourly average (nominated routes dark green)", "Standard"])
    for r in order:
        cs.append(["Route %s" % r, f["verdicts"][r]["lowest"], W.STANDARD])
    bar = BarChart()
    bar.type = "col"
    bar.title = "Seven routes clear four departures in every hour; the five busiest are nominated"
    bar.y_axis.title = "Departures an hour"
    bar.x_axis.title = "Candidate route (by weekday boardings)"
    data = Reference(cs, min_col=2, min_row=1, max_row=len(order) + 1)
    cats = Reference(cs, min_col=1, min_row=2, max_row=len(order) + 1)
    bar.add_data(data, titles_from_data=True)
    bar.set_categories(cats)
    from openpyxl.chart.marker import DataPoint
    from openpyxl.drawing.fill import ColorChoice
    s0 = bar.series[0]
    s0.graphicalProperties.solidFill = "A6A6A6"
    s0.graphicalProperties.line.solidFill = "A6A6A6"
    for i, r in enumerate(order):
        if r in five:
            pt = DataPoint(idx=i)
            pt.graphicalProperties.solidFill = "1F5F5B"
            pt.graphicalProperties.line.solidFill = "1F5F5B"
            s0.dPt.append(pt)
    bar.legend.position = "b"
    bar.y_axis.majorGridlines = None
    bar.y_axis.number_format = "0"
    bar.y_axis.delete = False
    bar.x_axis.delete = False
    bar.y_axis.scaling.min = 0
    bar.y_axis.scaling.max = 6.5
    line = LineChart()
    line.add_data(Reference(cs, min_col=3, min_row=1, max_row=len(order) + 1), titles_from_data=True)
    line.series[0].tx = SeriesLabel(v="Standard: four an hour")
    line.series[0].graphicalProperties.line.solidFill = "C00000"
    line.series[0].graphicalProperties.line.dashStyle = "dash"
    line.series[0].graphicalProperties.line.width = 19050
    bar += line
    bar.height = 7.5
    bar.width = 24
    ws.add_chart(bar, "A%d" % (ws.max_row + 2))
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 1
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.print_title_rows = "5:5"
    for col, w in zip("ABC", (10, 22, 10)):
        cs.column_dimensions[col].width = w
    # on-time departures
    ot = wb.create_sheet("On-time departures")
    ot.append(["On-time departures, January to June 2026"])
    ot["A1"].font = Font(name="Calibri", bold=True, size=12)
    ot.append(["Departures 6 a.m. to 7 p.m. on the counting days that the AVL records tie to a trip; on time is no more "
               "than one minute before and no more than five minutes after the trip's scheduled departure from the "
               "designated stop in the GTFS feed in effect that day (guidance 4.2)."])
    ot.append([])
    ot.append(["Route", "Name", "Departures tied to a trip", "On time", "Share on time"])
    for c in ot[4]:
        c.font = bold
        c.fill = head
    for r in sorted(W.CANDIDATES, key=int):
        n = f["on_time_n"][r]
        ot.append([int(r), W.ROUTE_NAMES[r], n, f["on_time_k"][r], f["on_time_k"][r] / n])
    for row in ot.iter_rows(min_row=5, max_row=ot.max_row):
        row[2].number_format = "#,##0"
        row[3].number_format = "#,##0"
        row[4].number_format = "0%"
    ot.append([])
    ot.append(["Arbor held its schedule times to the minute; the timetable sets some departures at the five transfer "
               "points to the half minute, so every departure is timed against the feed rather than either export's "
               "schedule field."])
    for col, w in zip("ABCDE", (7, 22, 22, 10, 13)):
        ot.column_dimensions[col].width = w
    wb.save(path)


def main(target, gdir, fig_path):
    os.makedirs(gdir, exist_ok=True)
    g = compute(target)
    f = figures(g)
    write_workbook(os.path.join(gdir, W.GOLDEN["workbook"]), f)
    with open(fig_path, "w", encoding="utf-8") as fh:
        json.dump(f, fh, indent=1)
        fh.write("\n")
    return f, g
