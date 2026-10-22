"""The goldens: the readiness workbook (every endpoint's verdict, its forecast peak-hour volume for January 2027 and its
2026 service credits, the freeze list, the notes) and the chart of every endpoint's 99th percentile at the forecast
peak against the 800 ms line, plus figures.json."""
import datetime as dt
import json
import math
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt                       # noqa: E402
from openpyxl import Workbook                         # noqa: E402
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side   # noqa: E402
from openpyxl.utils import get_column_letter          # noqa: E402

import analysis as AN                                 # noqa: E402
import common as K                                    # noqa: E402
import docs as DC                                     # noqa: E402
import pack as P                                      # noqa: E402

NAVY = "203A5C"
THIN = Side(style="thin", color="B9C1C8")
FIX, MEETS, INK, MUTED = "#eb6834", "#8f969d", "#1c2329", "#5a646d"
ROUTE_KEYS = ("raw", "raw_warm", "drop", "hdr", "hdr_gc", "hdr_gc_pods", "lw", "golden_rawsvc", "pooled")


def tens(x):
    return int(math.floor(x / 10.0 + 0.5) * 10)


def figures(target, R, a, b, carried):
    ep, svc = P.register(target)
    fix = AN.verdicts(R)
    fam = AN.GOLDEN_FAMILY
    margin = min((R[c][f] - K.SLA_MS) if c in fix else (K.SLA_MS - R[c][f]) for c in K.CODES for f in fam)
    near = min(K.CODES, key=lambda c: min(abs(R[c][f] - K.SLA_MS) for f in fam))
    runs = {c: R[c]["runs"] for c in K.CODES}
    return {
        "call": {"fix": fix, "count": len(fix), "fix_routes": [ep[c]["route"] for c in fix],
                 "not": [c for c in K.CODES if c not in fix]},
        "verdict": {c: ("Fix before freeze" if c in fix else "Meets 2.1") for c in K.CODES},
        "routes": {k: AN.verdicts(R, k) for k in ROUTE_KEYS + fam},
        "route_counts": {k: len(AN.verdicts(R, k)) for k in ROUTE_KEYS + fam},
        "p99_tens": {c: tens(R[c]["golden"]) for c in K.CODES},
        "family_ms": {c: {f: round(R[c][f], 1) for f in fam} for c in K.CODES},
        "recorded_ms": {c: int(round(R[c]["raw"])) for c in K.CODES},
        "margin_floor_ms": int(math.floor(margin)),
        "nearest_line": near,
        "runs": {"endpoints": len(K.CODES), "runs_total": sum(runs.values()),
                 "stopped_early": sorted(c for c in K.CODES if runs[c] > 1)},
        "gc": {c: {"share_pct": round(R[c]["share"], 2), "longest_ms": int(round(R[c]["longest"]))} for c in K.CODES},
        "requests": {c: R[c]["n"] for c in K.CODES},
        "pods": {c: R[c]["pods"] for c in K.CODES},
        "ask_a": {c: a[c]["forecast"] for c in K.CODES},
        "ask_a_detail": {c: {"busiest_hour_utc": dt.datetime.utcfromtimestamp(a[c]["hour"]).strftime(
            "%Y-%m-%dT%H:00Z"), "served_customers": a[c]["peak"], "synthetic_per_hour": a[c]["synthetic"],
            "employers_nov1": a[c]["num"], "employers_jan1": a[c]["den"]} for c in K.CODES},
        "ask_b": {c: b[c]["dollars"] for c in K.CODES},
        "ask_b_total": sum(b[c]["dollars"] for c in K.CODES),
        "ask_b_carried_forward": carried,
        "filed": {"sla_ms": int(K.SLA_MS), "percentile": int(K.PCT), "warmup_min": 3, "measure_min": 10,
                  "freeze": "4 December 2026", "endpoints": len(K.CODES),
                  "clauses": ["1.2", "2.1", "2.2", "3.2", "3.3", "4.1", "4.2", "5.2"]},
        "n_mc": AN.N_MC,
        "nearest_s": round(R[near]["golden"] / 1000.0, 1),
        "fix_share_range_pct": [round(min(R[c]["share"] for c in fix), 1), round(max(R[c]["share"] for c in fix), 1)],
    }


def _head(ws, row, cols, widths):
    for j, (h, wd) in enumerate(zip(cols, widths), 1):
        cell = ws.cell(row, j, h)
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor=NAVY)
        cell.alignment = Alignment(wrap_text=True, vertical="center")
        ws.column_dimensions[get_column_letter(j)].width = wd


def workbook(path, target, fig, R):
    ep, svc = P.register(target)
    wb = Workbook()
    ws = wb.active
    ws.title = "Readiness"
    ws["A1"] = "Year-end readiness review, 2027 peak: public API endpoints"
    ws["A1"].font = Font(bold=True, size=13, color=NAVY)
    ws["A2"] = ("%d of %d endpoints miss the 800 ms objective at their forecast peak and go on the freeze list: %s."
                % (fig["call"]["count"], len(K.CODES), ", ".join(fig["call"]["fix"])))
    ws["A2"].font = Font(italic=True, size=10)
    ws["A3"] = "Capacity Planning, prepared by %s, 25 November 2026, under the readiness standard (2026 edition)." \
               % K.REQUESTER
    ws["A3"].font = Font(size=9, color="5A646D")
    cols = ["Code", "Route", "Service", "Collector", "Verdict (standard 2.1)",
            "Forecast peak-hour volume, January 2027 (requests an hour)",
            "Service credits for breaches, 1 Jan to 31 Oct 2026 (USD, net of reversals)"]
    _head(ws, 5, cols, [7, 36, 16, 10, 17, 19, 21])
    ws.row_dimensions[5].height = 62
    r = 6
    for c in K.CODES:
        vals = [c, ep[c]["route"], ep[c]["service"], svc[ep[c]["service"]]["collector"], fig["verdict"][c],
                fig["ask_a"][c], fig["ask_b"][c]]
        for j, v in enumerate(vals, 1):
            cell = ws.cell(r, j, v)
            cell.border = Border(bottom=THIN)
            if j == 6:
                cell.number_format = "#,##0"
            elif j == 7:
                cell.number_format = '"$"#,##0'
            if j >= 6:
                cell.alignment = Alignment(horizontal="right")
        if c in fig["call"]["fix"]:
            for j in range(1, 8):
                ws.cell(r, j).fill = PatternFill("solid", fgColor="FBE6DC")
                ws.cell(r, j).font = Font(bold=True)
        r += 1
    ws.cell(r, 1, "All endpoints").font = Font(bold=True)
    cell = ws.cell(r, 7, fig["ask_b_total"])
    cell.number_format = '"$"#,##0'
    cell.font = Font(bold=True)
    cell.alignment = Alignment(horizontal="right")
    cell.border = Border(top=Side(style="thin", color="1C2329"))
    ws.freeze_panes = "C6"
    ws.print_title_rows = "5:5"

    fl = wb.create_sheet("Freeze list")
    cols = ["Code", "Route", "Service", "Owner team", "Collector", "Pods", "Run of record (start, UTC)"]
    _head(fl, 1, cols, [7, 36, 16, 17, 10, 7, 22])
    starts = {}
    X = AN.call_inputs(target)
    for c in fig["call"]["fix"]:
        starts[c] = dt.datetime.utcfromtimestamp(X[c]["run"]["t0"]).strftime("%Y-%m-%d %H:%M")
    for i, c in enumerate(fig["call"]["fix"], 2):
        s = ep[c]["service"]
        for j, v in enumerate([c, ep[c]["route"], s, DC.TEAMS[s], svc[s]["collector"], svc[s]["pods"], starts[c]], 1):
            cell = fl.cell(i, j, v)
            cell.border = Border(bottom=THIN)
            if j == 6:
                cell.alignment = Alignment(horizontal="right")
    fl.freeze_panes = "A2"

    n = wb.create_sheet("Notes")
    notes = [
        "How the figures were made",
        "Verdicts (standard 2.1 and 2.3): an endpoint is on the freeze list when fewer than 99 percent of the requests "
        "customers send it at the forecast peak would have their complete response within 800 ms, compared unrounded.",
        "Evidence (standard 3.2): each endpoint's run of record, its last complete run, minutes 3 to 13 after its first "
        "request. The first runs of %s stopped early and are set aside." % ", ".join(fig["runs"]["stopped_early"]),
        "Response times at the peak: customers' requests keep arriving whatever state a pod is in, while the test's "
        "clients each waited for a response before sending again, so a pod's garbage-collection pause held only the "
        "requests already in flight. Each endpoint's percentile is taken over arrivals spread evenly across the "
        "measurement window and the service's pods (the edge turns requests across the pods in rotation), each taking "
        "a service time the run recorded (a request's response time less the pause time on its pod while it was in "
        "flight) and held by any pause on its pod. Pauses come from the GC log export: each line is written as its "
        "pause ends; lines stamped with JVM uptime (tax-forms, banking, accounting-sync) are placed from the JVM start "
        "the pod events give, after the two restarts for the restarted pods.",
        "Forecast peak-hour volume (standard 4.1 and 4.2): the requests the endpoint served customers in its busiest "
        "clock hour of January 2026 at the edge, the uptime monitors running in January taken off every hour; for "
        "the three routes renamed in January, the old path up to the rename and the new path from it (the old path's "
        "later counts are its redirects). Times the employers on the endpoint's plans on 1 November 2026 over those "
        "on 1 January 2026, each account's state on 1 January found by undoing its 2026 subscription events, latest "
        "first.",
        "Service credits (standard 5.2): credits for incidents that began from 1 January to 31 October 2026, by the "
        "route each incident hit (the old route names for incidents before a rename). Legacy amounts are in cents. A "
        "legacy credit still open on 30 April was carried into the new billing system at its unapplied balance and is "
        "counted once, at the amount issued. Reversals are netted.",
        "Rounding: volumes to the nearest whole request; credits to the nearest dollar, and their total is the sum of "
        "the endpoints' figures as shown.",
    ]
    n.column_dimensions["A"].width = 120
    for i, t in enumerate(notes, 1):
        cell = n.cell(i, 1, t)
        cell.alignment = Alignment(wrap_text=True, vertical="top")
        if i == 1:
            cell.font = Font(bold=True)
    wb.save(path)


def chart(path, target, fig, R):
    ep, _ = P.register(target)
    order = sorted(K.CODES, key=lambda c: R[c]["golden"])
    vals = [R[c]["golden"] for c in order]
    rec = [R[c]["raw"] for c in order]
    colors = [FIX if c in fig["call"]["fix"] else MEETS for c in order]
    f, ax = plt.subplots(figsize=(8.6, 8.4), dpi=150)
    ax.barh(range(len(order)), vals, color=colors, height=0.62, zorder=2)
    ax.scatter(rec, range(len(order)), marker="|", s=110, linewidths=2.0, color=INK, zorder=3)
    ax.axvline(K.SLA_MS, color=INK, lw=1.1, zorder=1)
    ax.text(K.SLA_MS + 12, len(order) - 0.35, "800 ms standard", color=INK, fontsize=8.5, va="center")
    ax.set_yticks(range(len(order)))
    ax.set_yticklabels(["%s  %s" % (c, ep[c]["route"]) for c in order], fontsize=8)
    ax.set_xlim(0, 1400)
    ax.set_xticks(range(0, 1401, 200))
    ax.set_xticklabels(["{:,}".format(x) for x in range(0, 1401, 200)], fontsize=8.5)
    ax.set_xlabel("99th-percentile response time at the forecast peak hour (ms)", fontsize=9)
    ax.grid(axis="x", color="#e3e6e9", lw=0.8, zorder=0)
    ax.set_axisbelow(True)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.tick_params(axis="y", length=0)
    from matplotlib.lines import Line2D
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=FIX, label="Freeze list: over 800 ms at the peak"),
                       Patch(color=MEETS, label="Meets the standard"),
                       Line2D([], [], color=INK, marker="|", ls="", markersize=10, markeredgewidth=2,
                              label="Recorded in the load test's run of record")],
              loc="lower right", fontsize=8, frameon=False)
    f.text(0.012, 0.975, "Five endpoints miss 800 ms at the January peak", fontsize=12.5, color=INK,
           weight="bold", va="top")
    f.text(0.012, 0.947, "Bars: the 99th percentile of the requests customers send, with every pod's garbage-collection "
                         "pauses in the run of record", fontsize=8.5, color=MUTED, va="top")
    f.text(0.012, 0.012, "Mirrendale Payroll, Capacity Planning, year-end readiness review, November 2026. Load tests "
                         "10 to 19 November 2026, performance cluster, build 2026.11.2.", fontsize=7, color=MUTED)
    f.tight_layout(rect=(0, 0.025, 1, 0.93))
    f.savefig(path, metadata={"Software": None})
    plt.close(f)


def write_figures(path, fig):
    with open(path, "w") as f:
        json.dump(fig, f, indent=1, sort_keys=True)
        f.write("\n")


def write(target, golden, n_mc=AN.N_MC):
    os.makedirs(golden, exist_ok=True)
    R = AN.routes(target, n_mc=n_mc)
    a = AN.ask_a(target)
    b, carried = AN.ask_b(target)
    fig = figures(target, R, a, b, carried)
    workbook(os.path.join(golden, K.DELIVERABLES[0]), target, fig, R)
    chart(os.path.join(golden, K.DELIVERABLES[1]), target, fig, R)
    return fig, dict(R=R, a=a, b=b, carried=carried)
