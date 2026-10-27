"""The goldens: fy2028_relief_positions_by_unit.xlsx and fy2028_weekly_backfill_need.png, and generator/figures.json,
every figure read back from the pack."""
from __future__ import annotations

import datetime as dt
import json
import os

import numpy as np

import analysis as A
import asks as AK
import common as K
import pack as PK

WORD = {1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five"}


def half_up(x, nd=0):
    from decimal import ROUND_HALF_UP, Decimal
    q = Decimal(1).scaleb(-nd)
    return float(Decimal(repr(float(x))).quantize(q, rounding=ROUND_HALF_UP)) if nd else int(
        Decimal(repr(float(x))).quantize(Decimal(1), rounding=ROUND_HALF_UP))


def results(target):
    pk = PK.Pack(target)
    c = A.call(pk)
    return dict(pk=pk, call=c, asks=AK.golden(pk))


def figures(res):
    c = res["call"]
    g = c["golden"]
    total = c["total"]
    left = K.FUNDED - total
    units = {}
    for u in K.UNIT_CODES:
        need, h = c["need"][u], c["hours"][u]
        units[u] = dict(name=K.UNIT_NAME[u], title=K.UNIT_TITLE[u], positions=g[u],
                        fifth_week_need_hours=half_up(A.q5(need), 1), relief_hours_per_week=half_up(h, 1),
                        new_lines=len(c["comp"][u]["new"]),
                        overtime_hours_fy2026=res["asks"]["a"][u])
    if left >= 0:
        sentence = ("%d of the 60 positions placed (%s); %d returned to the Governor's reserve" %
                    (total, ", ".join("%s %d" % (u, g[u]) for u in K.UNIT_CODES), left))
    else:
        sentence = "%d positions needed, %d more than the 60 funded" % (total, -left)
    return {
        "call": {"positions": g, "placement": [g[u] for u in K.UNIT_CODES], "total": total, "funded": K.FUNDED, "returned_to_reserve": max(left, 0),
                 "short_by": max(-left, 0), "sentence": sentence},
        "units": units,
        "routes": {k: dict(zip(K.UNIT_CODES, v)) for k, v in c["counts"].items()},
        "route_totals": {k: sum(v) for k, v in c["counts"].items()},
        "ask_a_overtime_hours_by_unit": res["asks"]["a"],
        "ask_b_people_by_unit": res["asks"]["b"],
        "ask_c_people_over_600_hours": res["asks"]["c"],
        "weekly_need": {u: [half_up(x, 1) for x in c["need"][u]] for u in K.UNIT_CODES},
        "evidence": evidence(res),
    }


def evidence(res):
    pk, c = res["pk"], res["call"]
    j = pk.availability(A.july25())
    allh = pk.availability(lambda r, e: True)
    fills = sorted({(first - K.FY28_START).days // 7 + 1 for u in K.UNIT_CODES for _, first, _ in c["comp"][u]["new"]})
    return {"vacant_lines_fy2028": sum(len(c["comp"][u]["new"]) for u in K.UNIT_CODES),
            "fill_weeks": [fills[0], fills[-1]],
            "fy2026_vacant_line_hours": int(sum(c["comp"][u]["V26"].sum() for u in K.UNIT_CODES)),
            "july2025_off_post_pct": half_up(100 * (1 - j), 1), "units_off_post_pct": half_up(100 * (1 - allh), 1),
            "weeks": K.WEEKS, "funded": K.FUNDED, "overtime_threshold_hours": 600, "comp_time_credit": AK.COMP["CTE"],
            "comp_time_credit_aides": AK.COMP["CTS"],
            "relief_hours_by_title": {t: half_up(K.WEEK_H * c["comp"][[u for u in K.UNIT_CODES
                                                                      if K.UNIT_TITLE[u] == t][0]]["a1"], 1)
                                      for t in K.TITLE_ORDER},
            "unit_average_hours_range": [half_up(min(K.WEEK_H * c["comp"][u]["a_all"] for u in K.UNIT_CODES), 1),
                                         half_up(max(K.WEEK_H * c["comp"][u]["a_all"] for u in K.UNIT_CODES), 1)],
            "title_average_hours_range": [half_up(min(K.WEEK_H * c["comp"][u]["a_title"] for u in K.UNIT_CODES), 1),
                                          half_up(max(K.WEEK_H * c["comp"][u]["a_title"] for u in K.UNIT_CODES), 1)],
            "default_path_total": sum(c["counts"][A.DEFAULT]),
            "default_path_short_by": sum(c["counts"][A.DEFAULT]) - K.FUNDED,
            "clauses_cited": [2.1, 2.3, 2.4, 3.1, 3.2, 3.3, 3.4, 14.2, 14.3]}


# ------------------------------------------------------------------------------------------------ chart
def chart_png(path, fig, res):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib import font_manager
    from matplotlib.lines import Line2D
    from matplotlib.patches import Patch
    for f in ("LiberationSans-Regular.ttf", "LiberationSans-Bold.ttf"):
        for d in ("/usr/share/fonts/truetype/liberation/", os.path.expanduser("~/Library/Fonts/"), "/Library/Fonts/"):
            if os.path.exists(d + f):
                font_manager.fontManager.addfont(d + f)
                break
    plt.rcParams.update({"font.family": "Liberation Sans", "font.size": 9})
    ink, muted, grid = "#1d2329", "#5a636b", "#d9dee3"
    bar, over, cover = "#8fb3dd", "#d9622b", "#1f3b57"
    c = res["call"]
    f, axes = plt.subplots(2, 4, figsize=(13.2, 6.6), dpi=150, sharex=True)
    wk = np.arange(1, K.WEEKS + 1)
    for ax, u in zip(axes.flat, K.UNIT_CODES):
        need = c["need"][u]
        n = c["golden"][u]
        lvl = n * c["hours"][u]
        cols = [over if x > lvl + 1e-9 else bar for x in need]
        ax.bar(wk, need, width=0.78, color=cols, edgecolor="none", zorder=2)
        ax.axhline(lvl, color=cover, linewidth=1.6, zorder=3)
        ax.text(52.5, lvl, " %d positions\n %s h" % (n, format(int(round(lvl)), ",")), va="center", ha="left",
                fontsize=8, color=ink)
        ax.set_title(K.UNIT_NAME[u].replace(", Security Nursing", ""), loc="left", fontsize=9.2, color=ink,
                     fontweight="bold", pad=4)
        top = 50 * int(np.ceil(max(need.max(), lvl) * 1.08 / 50))
        ax.set_ylim(0, top)
        ax.set_xlim(0.3, 52.7)
        ax.yaxis.grid(True, color=grid, linewidth=0.6, zorder=0)
        ax.set_axisbelow(True)
        for sp in ("top", "right", "left"):
            ax.spines[sp].set_visible(False)
        ax.spines["bottom"].set_color(grid)
        ax.tick_params(axis="both", length=0, labelsize=7.8, colors=muted)
        ax.set_xticks([1, 14, 27, 40, 52])
        ax.set_xticklabels(["Jul", "Oct", "Jan", "Apr", "Jun"])
        ax.set_yticks(range(0, top + 1, 100 if top > 300 else 50))
        ax.set_yticklabels([format(v, ",") for v in range(0, top + 1, 100 if top > 300 else 50)])
    for ax in axes[:, 0]:
        ax.set_ylabel("Hours a week", fontsize=8.2, color=muted)
    total = c["total"]
    left = K.FUNDED - total
    f.suptitle("%d relief positions meet every unit's FY2028 backfill need in all but four weeks; %s of the 60 "
               "%s to the reserve" % (total, {1: "one", 2: "two", 3: "three"}.get(left, str(left)),
                                       "returns" if left == 1 else "return"), x=0.012, y=0.985, ha="left", fontsize=12.6,
               fontweight="bold", color=ink)
    f.text(0.012, 0.925, "Weekly backfill need for FY2028 (fiscal weeks from 1 July 2027) against the hours on post "
                         "each unit's relief complement works in an average week. Budget Instruction 2024-07, 3.1 to "
                         "3.4.", fontsize=8.8, color=muted, ha="left")
    handles = [Patch(facecolor=bar, edgecolor="none", label="Backfill need in the week"),
               Patch(facecolor=over, edgecolor="none", label="Weeks above the relief cover (four a unit at most)"),
               Line2D([], [], color=cover, linewidth=1.6, label="Hours the relief positions work on post a week")]
    leg = f.legend(handles=handles, loc="lower left", bbox_to_anchor=(0.012, 0.005), ncol=3, fontsize=8.2,
                   frameon=False, handlelength=1.6, columnspacing=2.0)
    for t in leg.get_texts():
        t.set_color(muted)
    f.text(0.988, 0.012, "Source: FY2026 rosters (RosterPro, ShiftLink); FY2028 position control, 1 October 2026; "
                         "entry class calendar.", fontsize=7.2, color=muted, ha="right")
    f.subplots_adjust(left=0.05, right=0.93, top=0.86, bottom=0.12, hspace=0.38, wspace=0.42)
    f.savefig(path, dpi=150, metadata={"Software": None})
    plt.close(f)


# ------------------------------------------------------------------------------------------------ workbook
def workbook(path, fig, res):
    import openpyxl
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    c = res["call"]
    navy = "1F3B57"
    thin = Side(style="thin", color="B9C1C8")
    head_font = Font(bold=True, color="FFFFFF")
    head_fill = PatternFill("solid", fgColor=navy)

    def header(ws, row, height=44):
        for cell in ws[row]:
            if cell.value is None:
                continue
            cell.font = head_font
            cell.fill = head_fill
            cell.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
        ws.row_dimensions[row].height = height

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Placement"
    ws.append(["FY2028 overtime-relief positions by unit"])
    ws["A1"].font = Font(bold=True, size=13, color=navy)
    ws.append(["Workforce Analysis Desk, Office of Budget Analysis, for the Director. Budget Instruction 2024-07 on "
               "the FY2026 rosters (the last closed year) and the FY2028 position control of 1 October 2026."])
    ws["A2"].font = Font(italic=True, size=9, color="5A636B")
    ws.append([])
    ws.append(["Unit", "Name", "Title", "FY2028 lines vacant on 1 July 2027", "Backfill need, fifth-heaviest week "
               "(hours)", "Hours on post a relief position works a week", "Relief positions", "Hours covered a week"])
    header(ws, 4, 58)
    for u in K.UNIT_CODES:
        d = fig["units"][u]
        h = c["hours"][u]
        ws.append([u, d["name"], K.TITLES[d["title"]], d["new_lines"], A.q5(c["need"][u]), h, d["positions"],
                   d["positions"] * h])
        row = ws[ws.max_row]
        row[4].number_format = "#,##0"
        row[5].number_format = "0.0"
        row[7].number_format = "#,##0"
        row[6].font = Font(bold=True, color=navy)
    ws.append(["All units", None, None, sum(fig["units"][u]["new_lines"] for u in K.UNIT_CODES), None, None,
               c["total"], None])
    row = ws[ws.max_row]
    for cell in row:
        cell.font = Font(bold=True)
        cell.border = Border(top=thin)
    ws.append(["Funded in the FY2028 allowance", None, None, None, None, None, K.FUNDED])
    ws.append(["Returned to the Governor's reserve" if K.FUNDED >= c["total"] else "Needed beyond the 60", None,
               None, None, None, None, abs(K.FUNDED - c["total"])])
    for r in ws.iter_rows(min_row=5, max_row=ws.max_row):
        for cell in r[3:]:
            cell.alignment = Alignment(horizontal="right")
    ws.append([])
    notes = [
        "Backfill need (2.3, 2.4, 3.4): each fiscal week's off-post hours on the unit's lines from the same week of "
        "FY2026, plus every scheduled hour of the lines the position control carries vacant on 1 July 2027 until "
        "their first shift on post, and their new holders' off-post hours after it.",
        "Relief position hours (3.3): 40 scheduled hours less the off-post hours of the holder. The positions are "
        "filled from the July 2027 entry classes, so the holders' off-post share is read from the July 2025 classes "
        "over their first year on post, FY2026, by title.",
        "Complement (3.1, 3.2): the smallest whole number of positions whose hours reach the fifth-heaviest week. "
        "Fiscal weeks run from 1 July; the last one or two days of the year belong to no week.",
        "Roster rows exported twice in February 2026 are counted once; Thornmere's ShiftLink status codes from 5 "
        "January 2026 are read through the timekeeping status table."]
    for line in notes:
        ws.append([line])
        ws.cell(ws.max_row, 1).font = Font(size=9, color="5A636B")
    for k, v in {"A": 10, "B": 40, "C": 30, "D": 14, "E": 15, "F": 15, "G": 11, "H": 12}.items():
        ws.column_dimensions[k].width = v
    ws.freeze_panes = "C5"
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.print_area = "A1:H%d" % ws.max_row

    w2 = wb.create_sheet("Weekly need FY2028")
    w2.append(["Weekly backfill need, FY2028, hours (fiscal weeks from 1 July 2027)"])
    w2["A1"].font = Font(bold=True, size=12, color=navy)
    w2.append([])
    w2.append(["Week", "Starts"] + K.UNIT_CODES)
    header(w2, 3, 30)
    for i in range(K.WEEKS):
        start = K.FY28_START + dt.timedelta(days=7 * i)
        w2.append([i + 1, start] + [float(c["need"][u][i]) for u in K.UNIT_CODES])
        row = w2[w2.max_row]
        row[1].number_format = "d mmm yyyy"
        for cell in row[2:]:
            cell.number_format = "#,##0.0"
    w2.append(["Cover", None] + [c["golden"][u] * c["hours"][u] for u in K.UNIT_CODES])
    row = w2[w2.max_row]
    for cell in row:
        cell.font = Font(bold=True)
        cell.border = Border(top=thin)
    for cell in row[2:]:
        cell.number_format = "#,##0.0"
    for k, v in {"A": 7, "B": 12}.items():
        w2.column_dimensions[k].width = v
    for col in "CDEFGHIJ":
        w2.column_dimensions[col].width = 9
    w2.freeze_panes = "C4"

    w3 = wb.create_sheet("Overtime FY2026")
    w3.append(["Overtime in FY2026 (work dates 1 July 2025 to 30 June 2026), from Central Payroll's overtime lines"])
    w3["A1"].font = Font(bold=True, size=12, color=navy)
    w3.append([])
    w3.append(["Unit", "Name", "Overtime hours worked", "People who worked overtime"])
    header(w3, 3, 30)
    for u in K.UNIT_CODES:
        w3.append([u, K.UNIT_NAME[u], fig["ask_a_overtime_hours_by_unit"][u], fig["ask_b_people_by_unit"][u]])
        w3.cell(w3.max_row, 3).number_format = "#,##0"
    w3.append(["All units", None, sum(fig["ask_a_overtime_hours_by_unit"].values())])
    for cell in w3[w3.max_row]:
        cell.font = Font(bold=True)
        cell.border = Border(top=thin)
    w3.cell(w3.max_row, 3).number_format = "#,##0"
    w3.append([])
    r1 = w3.max_row + 1
    w3.append(["Title", "People who worked more than 600 hours of overtime"])
    header(w3, r1, 44)
    for t in K.TITLE_ORDER:
        w3.append([K.TITLES[t], fig["ask_c_people_over_600_hours"][t]])
    w3.append([])
    for line in ["Hours worked: overtime paid at time and a half, and compensatory time at one hour worked for each "
                 "1.5 hours credited (CTE, MOU 14.2) or each hour credited (CTS, the Forensic Security Aides); "
                 "night differential and retroactive lines carry pay only, and a timesheet Central Payroll paid a "
                 "second time on a later check is one piece of work. By the unit whose post the piece was accepted "
                 "at in the offer log, else the employee's own unit (the home timekeeper; SL-0410 is Thornmere).",
                 "People: everyone with an overtime or compensatory time piece dated in FY2026 at the unit, counted "
                 "once at each unit they worked at; an employee's two records are one person. The all-units line "
                 "is not given for people, since one person can work at more than one unit.",
                 "Over 600 hours: a rehired employee's two records joined through the restored seniority date; the "
                 "title held in FY2026 (no one changed title during the year)."]:
        w3.append([line])
        w3.cell(w3.max_row, 1).font = Font(size=9, color="5A636B")
    for k, v in {"A": 32, "B": 40, "C": 18, "D": 18, "E": 18, "F": 16}.items():
        w3.column_dimensions[k].width = v
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
