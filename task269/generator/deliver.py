"""The goldens and figures.json, every figure computed from the shipped pack: the programme workbook
(pellbrook_2027_headway_programme_routes.xlsx) and the ranking chart (excess_wait_by_route_census_2026.png)."""
import json
import os

import numpy as np
import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

import analysis as A
import common as K
import pack as PK
import world as W

WB = "pellbrook_2027_headway_programme_routes.xlsx"
CHART = "excess_wait_by_route_census_2026.png"


def compute(target):
    L = PK.load(target)
    geo = A.geometry(L["patterns"], L["corridor"], lambda s: L["tp"].get(s, False))
    cl = A.cells(L["deps"])
    cb = A.corridor_boardings(L["jour"], geo)
    gold = A.figures(cb, cl, "golden")
    r0 = A.figures(cb, cl, "R0")
    r2 = A.figures(cb, cl, "R2")
    rank = A.ranking(gold)
    four = sorted(rank[:K.TEAMS], key=int)
    # components: route 14's and route 7's outbound corridor riders by where they go
    comp = {}
    for rt in ("14", "7"):
        sub = cb[(cb["route"] == rt) & (cb["direction"] == "out") & (cb["use"] != "?")]
        br = sub[sub["use"].isin(["A", "B"])]
        e_own = np.mean([cl[(r.day, r.route, r.direction, r.peak, r.tp, r.use)][0] for r in br.itertuples()])
        e_all = np.mean([cl[(r.day, r.route, r.direction, r.peak, r.tp, "ALL")][0] for r in br.itertuples()])
        comp[rt] = dict(branch_share=100.0 * len(br) / len(sub), branch_ewt_own=float(e_own),
                        branch_ewt_all=float(e_all))
    shifts = PK.pilot_shifts(target)
    cost = PK.pilot_cost(target, shifts)
    tot = {rt: sum(n for (r, _), n in shifts.items() if r == rt) for rt in K.ROUTES}
    fig = dict(
        call=dict(routes=[int(r) for r in four]),
        ewt={rt: round(gold[rt], 1) for rt in K.ROUTES},
        first_below=int(rank[K.TEAMS]),
        ask_a={rt: tot[rt] for rt in K.ROUTES},
        ask_b={rt: int(round(cost[rt])) for rt in K.ROUTES},
        components=dict(
            r14_branch_share=round(comp["14"]["branch_share"]),
            r14_branch_ewt_own=round(comp["14"]["branch_ewt_own"], 1),
            r14_branch_ewt_all=round(comp["14"]["branch_ewt_all"], 1),
            r7_corridor_share=round(100 - comp["7"]["branch_share"]),
            cut_fourth=dict(route=int(rank[K.TEAMS - 1]), ewt=round(gold[rank[K.TEAMS - 1]], 1)),
            cut_fifth=dict(route=int(rank[K.TEAMS]), ewt=round(gold[rank[K.TEAMS]], 1)),
        ),
        rivals=dict(
            route_level=dict(routes=sorted(int(r) for r in A.top(r0)), r14=round(r0["14"], 1), r3=round(r0["3"], 1)),
            boarded_branch=dict(routes=sorted(int(r) for r in A.top(r2)), r7=round(r2["7"], 1)),
        ),
        boardings=int(len(cb)),
        routes=[int(r) for r in K.ROUTES],
        relocated_stop=[int(r) for r in _relocated(target)],
    )
    exact = dict(gold=gold, r0=r0, r2=r2, cost=cost)
    return fig, exact


THIN = Side(style="thin", color="B8C4CC")


def _relocated(target):
    rows = PK._rows(os.path.join(target, K.FILES["stops_log"]))
    r = next(x for x in rows if x["new_stop_number"])
    return int(r["stop_number"]), int(r["new_stop_number"])


def write_workbook(path, fig, exact):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Ranking"
    ws.append(["2027 headway management programme: routes by excess wait per corridor boarding, census fortnight "
               "10 to 21 August 2026"])
    ws["A1"].font = Font(bold=True, size=12)
    ws.append(["Supervisor teams for 2027: routes %s. First route below them: route %d." %
               (", ".join(str(r) for r in fig["call"]["routes"][:-1]) + " and %d" % fig["call"]["routes"][-1],
                fig["first_below"])])
    ws.append([])
    head = ["Rank", "Route", "Corridor", "Excess wait per corridor boarding (min)", "2027 team"]
    ws.append(head)
    for c in ws[4]:
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="DDE7EE")
        c.alignment = Alignment(wrap_text=True, vertical="top")
    rank = sorted(K.ROUTES, key=lambda r: -exact["gold"][r])
    for i, rt in enumerate(rank, 1):
        team = "Yes" if int(rt) in fig["call"]["routes"] else None
        ws.append([i, int(rt), W.NET[rt]["road"], fig["ewt"][rt], team])
        row = ws.max_row
        ws.cell(row, 4).number_format = "0.0"
        if team:
            for c in ws[row]:
                c.fill = PatternFill("solid", fgColor="E3F1E8")
        if i == K.TEAMS:
            for c in ws[row]:
                c.border = Border(bottom=Side(style="medium", color="2E5E4E"))
    for col, w in zip("ABCDE", (7, 8, 18, 22, 11)):
        ws.column_dimensions[col].width = w
    ws.freeze_panes = "A5"
    p = wb.create_sheet("Pilot 2026")
    p.append(["Route", "Supervisor shifts worked", "Pilot cost ($)"])
    for c in p[1]:
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="DDE7EE")
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for rt in K.ROUTES:
        p.append([int(rt), fig["ask_a"][rt], fig["ask_b"][rt]])
        p.cell(p.max_row, 3).number_format = "#,##0"
    p.append(["Total", sum(fig["ask_a"].values()), int(round(sum(exact["cost"].values())))])
    for c in p[p.max_row]:
        c.font = Font(bold=True)
    p.cell(p.max_row, 3).number_format = "#,##0"
    for col, w in zip("ABC", (8, 14, 14)):
        p.column_dimensions[col].width = w
    p.freeze_panes = "A2"
    n = wb.create_sheet("Notes")
    notes = [
        "Excess wait as the Bus Service Reliability Standard (version 4, section 3) defines it: each corridor boarding's "
        "wait worked at its timing point for its peak and day from the vendor's revised release and the timetable in "
        "force that day, over the departures that serve the stop the rider tapped off at (both branches' buses for a "
        "corridor stop and for every inbound rider, one branch's buses for a branch stop).",
        "Boardings with no tag-off (default fare) are in each route's average; on the branched routes outbound they "
        "take the average of the boardings with a tag-off at the same timing point, peak and day.",
        "%s corridor boardings in the census weekday peaks (07:00 to 09:00 and 15:30 to 18:00)." % format(fig["boardings"], ","),
        "Pilot shifts: each supervisor's shift at a pilot post counted once (the operator's payroll timesheets and its "
        "rostering app both hold the shifts of 4 to 15 May); cancelled peaks and depot supervision out.",
        "Pilot cost: the operator's post charges on each route's cost centre (the 30 June journal out, reversed on "
        "1 July; June's invoices posted in July) plus each month's coordination fee shared by the month's shifts.",
        "Prepared by Network Performance, %s, for the December 2026 contract variation." % K.AGENCY,
    ]
    for t in notes:
        n.append([t])
    n.column_dimensions["A"].width = 120
    for row in n.iter_rows():
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical="top")
    wb.save(path)


def write_chart(path, fig, exact):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.family": "DejaVu Sans", "svg.hashsalt": "task269", "font.size": 10})
    rank = sorted(K.ROUTES, key=lambda r: exact["gold"][r])
    vals = [exact["gold"][r] for r in rank]
    team = [int(r) in fig["call"]["routes"] for r in rank]
    fg, ax = plt.subplots(figsize=(8.4, 4.8), dpi=150)
    cols = ["#2e6e57" if t else "#a7b4bc" for t in team]
    ax.barh(["Route %s" % r for r in rank], vals, color=cols, height=0.62)
    for i, v in enumerate(vals):
        ax.text(v + 0.02, i, "%.1f" % v, va="center", fontsize=9, color="#1c2428")
    cut = (len(rank) - K.TEAMS) - 0.5
    ax.axhline(cut, color="#2e3b44", lw=1.0, ls="--")
    ax.text(max(vals) * 0.98, cut + 0.12, "four teams", ha="right", va="bottom", fontsize=8.5, color="#2e3b44")
    ax.set_xlabel("Excess wait per corridor boarding, weekday peaks (minutes)")
    ax.set_xlim(0, max(vals) * 1.15)
    ax.spines[["top", "right"]].set_visible(False)
    four = fig["call"]["routes"]
    ax.set_title("Routes %s, %s, %s and %s get the 2027 supervisor teams" % tuple(four), loc="left", fontsize=11.5,
                 fontweight="bold", color="#1c2428")
    fg.text(0.01, 0.01, "Census fortnight 10 to 21 August 2026, weekday peaks. Sources: location vendor's revised "
                        "release; ticketing journeys.", fontsize=7.4, color="#5a646b")
    fg.tight_layout(rect=(0, 0.04, 1, 1))
    fg.savefig(path, metadata={"Software": None})
    plt.close(fg)


def write(target, golden):
    fig, exact = compute(target)
    if os.path.exists(golden):
        for f in os.listdir(golden):
            os.remove(os.path.join(golden, f))
    os.makedirs(golden, exist_ok=True)
    write_workbook(os.path.join(golden, WB), fig, exact)
    write_chart(os.path.join(golden, CHART), fig, exact)
    return fig, exact
