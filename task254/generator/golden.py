"""The two golden deliverables: shuttle_departures_2027.xlsx (the departure, the working weekdays it and the next
departure would have arrived by 8:00, the riders, vehicles and seats left empty) and
shuttle_departure_costs_2027.html (the late staff arrivals and the 2027 cost at each departure from 6:50 to 7:20,
with a bar per departure)."""
import html
import os

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

import asks as A
import core
import postprocess as PP

XLSX = "shuttle_departures_2027.xlsx"
HTML = "shuttle_departure_costs_2027.html"
NAVY = "1F3864"


def ampm(m):
    return "%d:%02d a.m." % (m // 60, m % 60)


def hm(m):
    return "%d:%02d" % (m // 60, m % 60)


def money(x):
    return "${:,}".format(int(round(x)))


def _head(ws, row, labels, widths):
    thin = Side(style="thin", color="8EA9DB")
    for j, h in enumerate(labels, start=1):
        c = ws.cell(row=row, column=j, value=h)
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor=NAVY)
        c.alignment = Alignment(horizontal="center" if j > 1 else "left", vertical="center", wrap_text=True)
        c.border = Border(bottom=thin)
    for j, w in enumerate(widths):
        ws.column_dimensions[chr(65 + j)].width = w


def _total(ws, row, ncol):
    for j in range(1, ncol + 1):
        c = ws.cell(row=row, column=j)
        c.font = Font(bold=True)
        c.border = Border(top=Side(style="thin", color="000000"))


def workbook(path, F, G):
    call, nxt = F["call"], F["call"] + 5
    N, need = F["N"], F["need"]
    cnt = F["golden_counts"]
    wb = Workbook()
    ws = wb.active
    ws.title = "Departure"
    ws["A1"] = "The 2027 morning staff shuttle leaves Cedar Grove park-and-ride at %s for the Brook Street stop" % ampm(call)
    ws["A1"].font = Font(bold=True, size=13)
    ws["A2"] = ("For the 2027 service order with Ridgeline Transit Services. Probe travel times, 1 October 2025 to "
                "30 September 2026.")
    ws["A2"].font = Font(italic=True, color="595959")
    ws["A4"] = "Leave Cedar Grove at"
    ws["A4"].font = Font(bold=True)
    ws["B4"] = ampm(call)
    ws["B4"].font = Font(bold=True, size=14)
    ws["B4"].alignment = Alignment(horizontal="right")
    ws["A5"] = ("The latest five-minute departure whose trips would have reached the Brook Street stop by 8:00 a.m. "
                "on at least %d of the %d working weekdays (90 per cent)." % (need, N))
    ws["A5"].font = Font(color="595959", size=9)
    _head(ws, 7, ["Departure", "Working weekdays on time", "Working weekdays"], [44, 26, 18])
    for r, d in enumerate((call, nxt), start=8):
        ws.cell(row=r, column=1, value=ampm(d))
        ws.cell(row=r, column=2, value=int(cnt[d]))
        ws.cell(row=r, column=3, value=N)
    ws.freeze_panes = "A8"

    ws = wb.create_sheet("Riders")
    ws["A1"] = "Who the 2027 morning shuttle carries"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = ("Staff reassigned to Cedar Grove with an 8:00 a.m. scheduled start, less opt-outs, each person "
                "counted once.")
    ws["A2"].font = Font(italic=True, color="595959")
    rows = [("Riders", G["riders"]["golden"]), ("Vehicles (%d seats each)" % A.SEATS, G["gold"]["vehicles"]),
            ("Seats left empty", G["gold"]["seats_empty"])]
    for r, (a, v) in enumerate(rows, start=4):
        ws.cell(row=r, column=1, value=a).font = Font(bold=True)
        ws.cell(row=r, column=2, value=int(v)).number_format = "#,##0"
    _head(ws, 8, ["Department", "Riders"], [44, 14])
    r = 9
    for d in A.DEPTS:
        ws.cell(row=r, column=1, value=d)
        ws.cell(row=r, column=2, value=int(G["by_dept"][d])).number_format = "#,##0"
        r += 1
    ws.cell(row=r, column=1, value="All departments")
    ws.cell(row=r, column=2, value=int(G["riders"]["golden"])).number_format = "#,##0"
    _total(ws, r, 2)

    ws = wb.create_sheet("Departures")
    _head(ws, 1, ["Departure", "Working weekdays on time", "Working weekdays late", "Share on time"],
          [14, 26, 24, 15])
    for r, d in enumerate(core.DEPARTURES, start=2):
        ws.cell(row=r, column=1, value=ampm(d))
        ws.cell(row=r, column=2, value=int(cnt[d]))
        ws.cell(row=r, column=3, value=int(N - cnt[d]))
        c = ws.cell(row=r, column=4, value=round(cnt[d] / N, 3))
        c.number_format = "0.0%"
    ws.freeze_panes = "A2"
    ws.print_title_rows = "1:1"

    ws = wb.create_sheet("Notes")
    ws.column_dimensions["A"].width = 20
    ws.column_dimensions["B"].width = 100
    notes = [
        ("As at", "16 October 2026"),
        ("Evidence", "Trelvane TMC export, October 2025 to September 2026: passenger-vehicle travel times on the "
                     "route's sixteen segments (shuttle service standard 2.4 and 2.5)."),
        ("Working weekdays", "Monday to Friday less the nine hospital holidays in the HR calendar for 2025-26 "
                             "(standard 2.2): %d. Every one counts (standard 2.3)." % N),
        ("Trips", "Built day by day: the %d-minute lot leg, then the route's segments in order, each at the passenger "
                  "travel time for the five-minute epoch in which the shuttle enters it, then the %d-minute leg to "
                  "the stop." % (core.LOT_LEG, core.STOP_LEG)),
        ("On time", "Arriving at or before 8:00 a.m.; the bar is %d of %d working weekdays (standard 2.1)." % (need, N)),
        ("Riders", "Garage permit roll (employee no.) and spaces granted through the HR form (payroll ID), matched "
                   "on the HR extract; %d staff are on both lists and are counted once. 8:00 a.m. starts only, "
                   "less the Parking Services opt-outs." % G["both_sheets"]),
        ("Vehicles", "One convoy, one seat a rider, %d seats a vehicle (operator's 2027 schedule of charges)." % A.SEATS),
        ("Prepared by", "Ebony Robinson, Transportation Planning"),
    ]
    for r, (a, b) in enumerate(notes, start=1):
        ws.cell(row=r, column=1, value=a).font = Font(bold=True)
        c = ws.cell(row=r, column=2, value=b)
        c.alignment = Alignment(wrap_text=True, vertical="top")
    wb.save(path)
    PP.normalize_xlsx(path, "Ebony Robinson", "2026-10-16T13:20:00Z", "2026-10-19T15:02:00Z", company=PP_ORG)


PP_ORG = "Beargrass Medical Center"

CSS = """
:root { --ink:#1d2733; --muted:#5b6672; --rule:#d5dbe3; --bar:#1f3864; --bar2:#8ea9db; --bg:#ffffff; }
body { margin:0; background:var(--bg); color:var(--ink); font:15px/1.45 "Segoe UI", Calibri, Arial, sans-serif; }
main { max-width:900px; margin:0 auto; padding:28px 16px 40px; }
.org { color:var(--muted); font-size:13px; margin:0 0 6px; letter-spacing:.02em; }
h1 { font-size:21px; line-height:1.3; margin:0 0 8px; }
.meta { color:var(--muted); font-size:13px; margin:0 0 18px; }
svg { width:100%; height:auto; display:block; }
table { border-collapse:collapse; width:100%; margin:18px 0 10px; font-size:14px; }
th, td { padding:6px 8px; border-bottom:1px solid var(--rule); }
th { text-align:right; font-weight:600; background:#eef2f7; }
th:first-child, td:first-child { text-align:left; }
td { text-align:right; font-variant-numeric:tabular-nums; }
.wrap { overflow-x:auto; }
.notes { color:var(--muted); font-size:12.5px; margin:4px 0; }
@media (max-width:560px) { body { font-size:14px; } h1 { font-size:18px; } table { font-size:12.5px; }
  th, td { padding:5px 4px; } }
footer { color:var(--muted); font-size:12px; border-top:1px solid var(--rule); margin-top:22px; padding-top:8px; }
"""


def svg_chart(G, deps):
    cost = G["gold"]["cost"]
    veh = G["vehicle_charges"]
    W_, H_ = 860, 400
    left, right, top, bottom = 112, 18, 30, 64
    pw, ph = W_ - left - right, H_ - top - bottom
    ymax = 4_000_000
    ticks = [0, 1_000_000, 2_000_000, 3_000_000, 4_000_000]
    y = lambda v: top + ph - ph * v / ymax
    bw = pw / len(deps) * 0.58
    out = ['<svg viewBox="0 0 %d %d" role="img" aria-labelledby="chart-title" xmlns="http://www.w3.org/2000/svg">'
           % (W_, H_),
           '<title id="chart-title">2027 cost of holding each departure from 6:50 to 7:20 a.m.</title>']
    for t in ticks:
        out.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="#e3e7ec" stroke-width="1"/>' % (left, y(t), W_ - right, y(t)))
        out.append('<text x="%d" y="%.1f" font-size="12" text-anchor="end" fill="#5b6672">%s</text>'
                   % (left - 8, y(t) + 4, "$0" if t == 0 else "${:,.0f}".format(t)))
    out.append('<text x="18" y="%.1f" font-size="12" fill="#5b6672" transform="rotate(-90 18 %.1f)" '
               'text-anchor="middle">2027 cost (US dollars)</text>' % (top + ph / 2, top + ph / 2))
    for k, d in enumerate(deps):
        cx = left + pw * (k + 0.5) / len(deps)
        x0 = cx - bw / 2
        late = cost[d] - veh
        out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="#8ea9db"/>'
                   % (x0, y(veh), bw, y(0) - y(veh)))
        if late > 0:
            out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="#1f3864"/>'
                       % (x0, y(cost[d]), bw, y(veh) - y(cost[d])))
        out.append('<text x="%.1f" y="%.1f" font-size="12" text-anchor="middle" fill="#1d2733">%s</text>'
                   % (cx, y(cost[d]) - 6, html.escape(money(cost[d]))))
        out.append('<text x="%.1f" y="%.1f" font-size="12.5" text-anchor="middle" fill="#1d2733">%s</text>'
                   % (cx, y(0) + 18, hm(d)))
    out.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="#1d2733" stroke-width="1"/>'
               % (left, y(0), W_ - right, y(0)))
    out.append('<text x="%.1f" y="%d" font-size="12" text-anchor="middle" fill="#5b6672">Departure from Cedar Grove '
               '(a.m.)</text>' % (left + pw / 2, H_ - 26))
    lx = left + 8
    out.append('<rect x="%d" y="%d" width="12" height="12" fill="#8ea9db"/>' % (lx, top - 22))
    out.append('<text x="%d" y="%d" font-size="12" fill="#1d2733">Operator charges</text>' % (lx + 18, top - 12))
    out.append('<rect x="%d" y="%d" width="12" height="12" fill="#1f3864"/>' % (lx + 150, top - 22))
    out.append('<text x="%d" y="%d" font-size="12" fill="#1d2733">Late staff arrivals at $%.2f</text>'
               % (lx + 168, top - 12, A.HOLDOVER))
    out.append("</svg>")
    return "\n".join(out)


def page(path, F, G):
    deps = A.ASK_DEPS
    gold = G["gold"]
    cost, late = gold["cost"], gold["late_arrivals"]
    veh = G["vehicle_charges"]
    first, last = deps[0], deps[-1]
    rows = []
    for d in deps:
        rows.append("<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (
            ampm(d), "{:,}".format(late[d]), money(veh), money(A.HOLDOVER * late[d]), money(cost[d])))
    days27 = core.working_days_2027()
    doc = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Staff shuttle 2027: cost by departure</title>
<style>%(css)s</style>
</head>
<body>
<main>
<p class="org">Beargrass Medical Center &middot; Transportation Planning, for Finance (Operating Budget)</p>
<h1>Each later departure costs more in late arrivals: %(c0)s in 2027 at %(d0)s, %(c1)s at %(d1)s</h1>
<p class="meta">2027 morning staff shuttle, Cedar Grove park-and-ride to the Brook Street stop. %(riders)s riders in %(veh)s vehicles, %(days)s service days. Prepared 19 October 2026.</p>
%(svg)s
<div class="wrap"><table>
<thead><tr><th>Departure</th><th>Late staff arrivals a year</th><th>Operator charges</th><th>Late-arrival cost</th><th>2027 cost</th></tr></thead>
<tbody>
%(rows)s
</tbody>
</table></div>
<p class="notes">Operator charges: %(veh)s vehicles of %(seats)s seats for %(riders)s riders (%(empty)s seats left empty), each at the $%(day).2f day charge and $%(mile).2f a mile for the %(miles).2f-mile deadhead back to the Fern Valley yard, over the %(days)s service days of the HR 2027 calendar. The deadhead route's codes are read in network release 2025.2, the release it was set up under; in release 2026.1 its I-264 to Grade Lane code belongs to the I-264 westbound ramp.</p>
<p class="notes">Late staff arrivals: the working weekdays of October 2025 to September 2026 on which a departure's trips would have reached the stop after 8:00 a.m., each counting all %(riders)s riders, costed at $%(hold).2f each (2027 budget basis, 12 October 2026). Costs are summed in cents and rounded once to whole dollars.</p>
<footer>Sources: Trelvane TMC export and TMC identification table; Ridgeline Transit Services 2027 schedule of charges and deadhead route; Cedar Grove reassignment list and HR extract; HR holiday calendars.</footer>
</main>
</body>
</html>
""" % {"css": CSS.strip(), "c0": money(cost[first]), "d0": ampm(first), "c1": money(cost[last]), "d1": ampm(last),
       "riders": "{:,}".format(G["riders"]["golden"]), "veh": gold["vehicles"], "days": days27,
       "svg": svg_chart(G, deps), "rows": "\n".join(rows), "seats": A.SEATS, "empty": gold["seats_empty"],
       "day": A.DAY_RATE, "mile": A.MILE_RATE, "miles": G["miles"]["golden"], "hold": A.HOLDOVER}
    with open(path, "w", newline="\n", encoding="utf-8") as f:
        f.write(doc)


def write(golden_dir, F, G):
    os.makedirs(golden_dir, exist_ok=True)
    workbook(os.path.join(golden_dir, XLSX), F, G)
    page(os.path.join(golden_dir, HTML), F, G)
