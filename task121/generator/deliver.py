"""The goldens: satisfaction_fall_spring2026.xlsx and satisfaction_bridge_spring2026.png, and generator/figures.json,
every figure read back from the shipped files."""
from __future__ import annotations

import json
import os

import numpy as np

import analysis as A
import common as K
import routes as RT

GNAME = {g: K.GROUPS[g]["name"] for g in K.GROUP_ORDER}
WORD = {0: "none", 1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight"}


def half_up(x, nd=0):
    from decimal import ROUND_HALF_UP, Decimal
    if nd:
        return float(Decimal(repr(float(x))).quantize(Decimal(1).scaleb(-nd), rounding=ROUND_HALF_UP))
    return int(Decimal(repr(float(x))).quantize(Decimal(1), rounding=ROUND_HALF_UP))


def results(target):
    D = A.load(target)
    J = A.journeys(D)
    c = A.call(J)
    ontime, ontime_n = A.ask_ontime(D)
    staffed, staffed_n = A.ask_staffed(D)
    standing, standing_n = A.ask_standing(D)
    return dict(D=D, J=J, call=c, ontime=ontime, ontime_n=ontime_n, staffed=staffed, staffed_n=staffed_n,
                standing=standing, standing_n=standing_n)


def figures(res):
    c, J, D = res["call"], res["J"], res["D"]
    sh = c["shares"]
    s25, s26 = half_up(sh["overall"][2025], 1), half_up(sh["overall"][2026], 1)
    pts = {k: half_up(v) for k, v in c["points"].items()}
    other = half_up(c["unexplained"])
    name = c["top"]
    sentence = ("%s accounts for most of the fall: %d of the %.1f points by which the share of passengers satisfied "
                "overall fell, from %.1f%% in spring 2025 to %.1f%% in spring 2026" %
                (name[0].upper() + name[1:], c["top_points"], s25 - s26, s25, s26))
    kda = RT.kda(D, J)
    ks = RT.kitchen_sink(D, J)
    ksm = RT.kitchen_sink(D, J, mapping="as worded")
    return {
        "call": {"driver": name, "points": c["top_points"], "sentence": sentence},
        "shares": {"spring_2025": s25, "spring_2026": s26, "fall_points": half_up(s25 - s26, 1),
                   "by_group": {g: {"spring_2025": half_up(sh["groups"][g][2025], 1),
                                    "spring_2026": half_up(sh["groups"][g][2026], 1)} for g in K.GROUP_ORDER}},
        "bridge_points": dict(pts, other=other),
        "bridge_exact": {k: round(float(v), 4) for k, v in c["points"].items()},
        "prevalence_change_points": {k: round(float(v) * (1 if k == "fare" else 100), 2) for k, v in c["delta"].items()},
        "effects": {k: round(float(v), 4) for k, v in c["beta"].items()},
        "ask_on_time_pct": {g: half_up(res["ontime"][g], 1) for g in K.GROUP_ORDER},
        "ask_on_time_trains": {g: res["ontime_n"][g][1] for g in K.GROUP_ORDER},
        "ask_staffed_pct": {g: half_up(res["staffed"][g], 1) for g in K.GROUP_ORDER},
        "ask_staffed_trains": {g: res["staffed_n"][g][1] for g in K.GROUP_ORDER},
        "ask_standing": {g: int(res["standing"][g]) for g in K.INTO_MVC},
        "ask_standing_trains": {g: res["standing_n"][g] for g in K.INTO_MVC},
        "routes": {
            "R0_derived_importance": {k: round(v, 2) for k, v in kda.items()},
            "R0_top": RT.top(kda),
            "R0_points": half_up(kda[RT.top(kda)]),
            "R1_conditions_with_ratings_as_controls": {k: round(v, 2) for k, v in ks.items()},
            "R1_top": RT.top(ks),
            "R1_points": half_up(ks[RT.top(ks)]),
            "R1_with_ratings_booked_to_drivers": {k: round(v, 2) for k, v in ksm.items()},
            "stratified": {k: round(v, 2) for k, v in RT.stratified(J).items()},
            "R2_cascade_groups": {k: round(v, 2) for k, v in RT.cascade_did(J).items()},
            "unweighted": {k: round(v, 2) for k, v in RT.unweighted(J).items()},
            "golden_family": {k: {d: round(v, 2) for d, v in f.items()} for k, f in RT.golden_family(J).items()},
            "logit": {k: round(v, 2) for k, v in RT.logit_family(J).items()},
        },
        "evidence": {"condition_share_pct": {col: {str(wv): half_up(100 * float(np.average(
                         J.loc[(J["wave"] == wv) & ~J["sat"].isna(), col],
                         weights=J.loc[(J["wave"] == wv) & ~J["sat"].isna(), "weight"])), 1) for wv in (2025, 2026)}
                         for col in ("crowded", "late", "unstaffed")},
                     "effect_points_if_met": {col: half_up(-100 * float(c["beta"][col]), 1)
                                              for col in ("crowded", "late", "unstaffed")},
                     "default_path": {"driver": RT.top(kda), "points": half_up(kda[RT.top(kda)])},
                     "seats": {"150/2": 116, "158": 138, "158/9": 126, "166": 232},
                     "class_reporting_each_vehicle": 166,
                     "standing_window": {"from_hour": 7, "to_hour": 9, "to_minute": 59},
                     "respondents": {str(w): int((J["wave"] == w).sum()) for w in (2025, 2026)},
                     "respondents_answering_q1": {str(w): int(((J["wave"] == w) & ~J["sat"].isna()).sum())
                                                  for w in (2025, 2026)},
                     "baseline_window": [K.LATEST[0].isoformat(), K.LATEST[1].isoformat()],
                     "late_minutes": K.LATE_MIN},
    }


# ------------------------------------------------------------------------------------------------ chart
LABEL = {"crowding": "Crowding", "punctuality": "Punctuality", "on-board staffing": "On-board staffing",
         "fares": "Fares", "other": "Not explained by\nthe four drivers"}


def chart_png(path, fig, res):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib import font_manager
    for f in ("LiberationSans-Regular.ttf", "LiberationSans-Bold.ttf"):
        p = "/usr/share/fonts/truetype/liberation/" + f
        if os.path.exists(p):
            font_manager.fontManager.addfont(p)
    plt.rcParams.update({"font.family": "Liberation Sans", "font.size": 9.5})
    ink, muted, grid = "#1c2733", "#5d6874", "#dde2e7"
    hero, rest, total_c, resid = "#b5482a", "#7d97ae", "#2b4257", "#c3cbd3"
    c = res["call"]
    exact = dict(c["points"], other=c["unexplained"])
    order = sorted(c["points"], key=lambda k: -c["points"][k]) + ["other"]
    f, ax = plt.subplots(figsize=(9.6, 5.4), dpi=150)
    level = 0.0
    xs = list(range(len(order) + 1))
    for i, k in enumerate(order):
        v = float(exact[k])
        lo, hi = (level, level + v) if v >= 0 else (level + v, level)
        col = hero if k == c["top"] else (resid if k == "other" else rest)
        ax.bar(i, hi - lo, bottom=lo, width=0.62, color=col, edgecolor="none", zorder=2)
        if i:
            ax.plot([i - 1 + 0.31, i - 0.31], [level, level], color=muted, linewidth=0.7, zorder=3)
        lab = "%d" % fig["bridge_points"][k]
        ax.text(i, hi + 0.08, lab + (" point" if abs(fig["bridge_points"][k]) == 1 else " points"), ha="center",
                va="bottom", fontsize=9.2, color=ink, fontweight="bold" if k == c["top"] else "normal")
        level += v
    fall = c["shares"]["fall"]
    ax.plot([len(order) - 1 + 0.31, len(order) - 0.31], [level, level], color=muted, linewidth=0.7, zorder=3)
    ax.bar(len(order), fall, width=0.62, color=total_c, edgecolor="none", zorder=2)
    ax.text(len(order), fall + 0.08, "%.1f points" % fig["shares"]["fall_points"], ha="center", va="bottom",
            fontsize=9.2, color=ink, fontweight="bold")
    ax.set_xticks(xs)
    ax.set_xticklabels([LABEL[k] for k in order] + ["Fall, spring 2025\nto spring 2026"], fontsize=9, color=ink)
    top = np.ceil(max(fall, level) + 1.0)
    ax.set_ylim(min(0, np.floor(min(0, min(exact.values())))), top)
    ax.set_ylabel("Percentage points of the share satisfied", fontsize=9, color=muted)
    ax.yaxis.grid(True, color=grid, linewidth=0.6, zorder=0)
    ax.set_axisbelow(True)
    ax.axhline(0, color=muted, linewidth=0.8, zorder=3)
    for sp in ("top", "right", "left", "bottom"):
        ax.spines[sp].set_visible(False)
    ax.tick_params(axis="both", length=0, labelsize=8.8, colors=muted)
    s25, s26 = fig["shares"]["spring_2025"], fig["shares"]["spring_2026"]
    f.suptitle("%s accounts for %d of the %.1f points the share of passengers satisfied fell between the spring "
               "waves" % (LABEL[c["top"]], fig["call"]["points"], fig["shares"]["fall_points"]),
               x=0.012, y=0.975, ha="left", fontsize=12.4, fontweight="bold", color=ink)
    f.text(0.012, 0.875, "Satisfied overall %.1f%% in spring 2025, %.1f%% in spring 2026. Each driver: the points by "
                         "which the share would have fallen less had passengers' journeys\nmet it as in spring 2025, "
                         "the other three as they were. Points rounded to the nearest whole point, each bar alone."
           % (s25, s26), fontsize=8.8, color=muted, ha="left", linespacing=1.4)
    f.text(0.988, 0.015, "Source: Customer Satisfaction Tracker, spring 2025 and 2026 waves (weighted), linked to "
                         "train movements, load-weigh, formations, crew records and fares.", fontsize=7.2,
           color=muted, ha="right")
    f.subplots_adjust(left=0.08, right=0.98, top=0.82, bottom=0.17)
    f.savefig(path, dpi=150, metadata={"Software": None})
    plt.close(f)


# ------------------------------------------------------------------------------------------------ workbook
def workbook(path, fig, res):
    import openpyxl
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    c = res["call"]
    navy = "2B4257"
    thin = Side(style="thin", color="B9C1C8")
    head_font = Font(bold=True, color="FFFFFF")
    head_fill = PatternFill("solid", fgColor=navy)

    def header(ws, row, height=32):
        for cell in ws[row]:
            if cell.value is None:
                continue
            cell.font = head_font
            cell.fill = head_fill
            cell.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
        ws.row_dimensions[row].height = height

    def note(ws, text):
        ws.append([text])
        ws.cell(ws.max_row, 1).font = Font(size=9, color="5D6874")

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Recovery plan (a)"
    ws.append(["Fall in passengers satisfied overall, spring 2025 to spring 2026: points by service driver"])
    ws["A1"].font = Font(bold=True, size=13, color=navy)
    ws.append(["%s, Contract Performance. For the recovery plan to the %s (ref WRP/CM/2026/118), "
               "Schedule 7 paragraph 9." % (K.OPERATOR, K.AUTHORITY)])
    ws["A2"].font = Font(italic=True, size=9, color="5D6874")
    ws.append([])
    ws.append(["Driver accounting for most of the fall", LABEL[c["top"]]])
    ws.append(["Points of the fall it accounts for", fig["call"]["points"]])
    for r in (4, 5):
        ws.cell(r, 1).font = Font(bold=True)
        ws.cell(r, 2).font = Font(bold=True, color="B5482A", size=12)
        ws.cell(r, 2).alignment = Alignment(horizontal="right")
    ws.append([])
    ws.append(["Share satisfied overall", "Spring 2025", "Spring 2026", "Fall (points)"])
    header(ws, ws.max_row)
    ws.append(["All passengers", fig["shares"]["spring_2025"] / 100, fig["shares"]["spring_2026"] / 100,
               fig["shares"]["fall_points"]])
    row = ws[ws.max_row]
    row[1].number_format = row[2].number_format = "0.0%"
    row[3].number_format = "0.0"
    ws.append([])
    ws.append(["Bridge", "Points of the fall", "Change in journeys meeting the driver", "Effect on the chance of "
               "being satisfied"])
    header(ws, ws.max_row, 44)
    order = sorted(c["points"], key=lambda k: -c["points"][k])
    for k in order:
        col = dict(A.DRIVERS)[k]
        d = c["delta"][col]
        b = c["beta"][col]
        ws.append([LABEL[k], fig["bridge_points"][k],
                   ("%+.1f points of journeys" % (100 * d)) if col != "fare" else ("%+.2f%% average fare change" % d),
                   ("%+.1f points if met" % (100 * b)) if col != "fare" else ("%+.2f points per 1%% on the fare" % (100 * b))])
        ws.cell(ws.max_row, 2).number_format = "0"
        if k == c["top"]:
            ws.cell(ws.max_row, 1).font = ws.cell(ws.max_row, 2).font = Font(bold=True, color="B5482A")
    ws.append(["Not explained by the four drivers", fig["bridge_points"]["other"], None, None])
    ws.append(["Fall in the share satisfied", fig["shares"]["fall_points"], None, None])
    for cell in ws[ws.max_row]:
        cell.font = Font(bold=True)
        cell.border = Border(top=thin)
    ws.cell(ws.max_row, 2).number_format = "0.0"
    for r in ws.iter_rows(min_row=8, max_row=ws.max_row):
        for cell in r[1:]:
            cell.alignment = Alignment(horizontal="right")
    ws.append([])
    note(ws, "Points are rounded to the nearest whole point and the bridge's rows are rounded separately, so they "
             "need not add to the fall.")
    note(ws, "A driver's points: the change between the waves in the share of passengers whose journey met it "
             "(Schedule 7, 3.1), times its effect on the chance of a passenger being satisfied, from a weighted "
             "linear model of being satisfied on the four drivers and the wave, both waves' respondents together.")
    note(ws, "Each questionnaire is linked to the train it was handed out on (fieldwork log) and the passenger's "
             "written-in stations: load-weigh against the seats of the units formed on every leg of the journey, "
             "arrival at the passenger's station, the on-board crew archive and the fare for the ticket type.")
    for k, v in {"A": 40, "B": 18, "C": 30, "D": 30}.items():
        ws.column_dimensions[k].width = v
    ws.freeze_panes = "A4"

    w2 = wb.create_sheet("By service group")
    w2.append(["Share satisfied overall by service group, spring waves (weighted)"])
    w2["A1"].font = Font(bold=True, size=12, color=navy)
    w2.append([])
    w2.append(["Service group", "Spring 2025", "Spring 2026", "Change (points)"])
    header(w2, 3)
    for g in K.GROUP_ORDER:
        a, b = fig["shares"]["by_group"][g]["spring_2025"], fig["shares"]["by_group"][g]["spring_2026"]
        w2.append([GNAME[g], a / 100, b / 100, round(b - a, 1)])
        row = w2[w2.max_row]
        row[1].number_format = row[2].number_format = "0.0%"
        row[3].number_format = "+0.0;-0.0;0.0"
    w2.append([])
    note(w2, "Changes of less than about four points for a single service group are within the range sampling "
             "alone produces between waves (the agency's technical note).")
    for k, v in {"A": 26, "B": 14, "C": 14, "D": 16}.items():
        w2.column_dimensions[k].width = v
    w2.freeze_panes = "A4"

    w3 = wb.create_sheet("Baseline (c)")
    w3.append(["Schedule 7 Part 2 measures, four weeks ending 19 September 2026 (23 August to 19 September)"])
    w3["A1"].font = Font(bold=True, size=12, color=navy)
    w3.append([])
    w3.append(["Service group", "Trains in the working timetable", "On time at final destination (2.1)",
               "Trains that ran", "Ran with on-board staff (2.2)", "Weekday arrivals at Marlvale Central 07:00 to "
               "09:59", "Passengers standing on arrival (2.3)"])
    header(w3, 3, 58)
    for g in K.GROUP_ORDER:
        into = g in K.INTO_MVC
        w3.append([GNAME[g], fig["ask_on_time_trains"][g], fig["ask_on_time_pct"][g] / 100,
                   fig["ask_staffed_trains"][g], fig["ask_staffed_pct"][g] / 100,
                   fig["ask_standing_trains"][g] if into else "n/a", fig["ask_standing"][g] if into else "n/a"])
        row = w3[w3.max_row]
        row[1].number_format = row[3].number_format = row[5].number_format = row[6].number_format = "#,##0"
        row[2].number_format = row[4].number_format = "0.0%"
        for cell in row[1:]:
            cell.alignment = Alignment(horizontal="right")
    w3.append([])
    note(w3, "2.1: a train arriving at its final destination less than five minutes after the working timetable "
             "is on time; one cancelled in full or part way is not. Bank Holiday Monday 31 August ran the Sunday "
             "timetable. Arrivals after midnight are timed against the previous evening's schedule.")
    note(w3, "2.2: trains that ran, in full or part, with a conductor, a host or a spare covering the turn. Cover "
             "the crew controller arranged the evening before is logged on the day before the turn.")
    note(w3, "2.3: load-weigh on departure from the station before Marlvale Central, less the standard seats of "
             "the units formed that day (seats after the 2026 interior refresh from each unit's return to traffic).")
    for k, v in {"A": 24, "B": 16, "C": 16, "D": 14, "E": 16, "F": 18, "G": 18}.items():
        w3.column_dimensions[k].width = v
    w3.freeze_panes = "B4"
    for s in (ws, w2, w3):
        s.page_setup.orientation = "landscape"
        s.page_setup.fitToWidth = 1
        s.sheet_properties.pageSetUpPr.fitToPage = True
    wb.save(path)


def write_figures(path, fig):
    with open(path, "w") as f:
        json.dump(fig, f, indent=1, sort_keys=True)
        f.write("\n")


def write(target, golden):
    os.makedirs(golden, exist_ok=True)
    res = results(target)
    fig = figures(res)
    workbook(os.path.join(golden, K.GOLDEN), fig, res)
    chart_png(os.path.join(golden, K.CHART), fig, res)
    return fig, res
