"""Golden deliverables, figures.json and submission.md, all from the shipped pack through calc.py."""
import datetime as dt
import io
import json
import os
import re
import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter
import calc
import util

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.abspath(os.path.join(HERE, ".."))
GOLDEN = os.path.join(TASK, "golden")
F_XLSX = "tvd_projection_w49-w52.xlsx"
F_SVG = "tvd_projection_curve.svg"


def r1(v):
    return float("%.1f" % (v + 1e-9))


def figures():
    g = calc.the_call()
    naive = calc.the_call(gi="naive_gamma")
    con = calc.ask_contacts()
    lab = calc.ask_lab()
    F = {"call": {"cases_w49_52": int(round(g["total"], -3))},
         "components": {"serial_interval_days": int(round(g["mean_si"])), "R": r1(g["R"]),
                        "growth_per_day": float("%.3f" % g["r"]), "pairs": g["n_pairs"]},
         "rivals": {"register_interval_days": int(round(naive["mean_si"])), "register_R": r1(naive["R"]),
                    "register_cases_w49_52": int(round(naive["total"], -3))},
         "phase3_cut_pct": 50,
         "context": {"weeks_base": [36, 41], "weeks_window": [49, 52], "week_contacts": [37, 39], "weeks_lab": [38, 39, 40, 41],
                     "week_phase3": 45, "week_chart_first": 30, "cartridge_run_minutes": calc.cartridge_run_minutes(), "hours_window": 24}}
    for z, (n, s) in con.items():
        F["a1_%s" % z] = {"people": int(n), "pct_completed": r1(s)}
    for w, (m, s, n) in lab.items():
        F["a2_w%d" % w] = {"mean_hours": r1(m), "pct_within_24h": r1(s)}
    return F, g


def workbook(F, g):
    wb = Workbook()
    ws = wb.active
    ws.title = "Projection W49-W52"
    bold = Font(bold=True)
    head = PatternFill("solid", fgColor="DDE7F0")
    ws["A1"] = ("Dunmarrow TVD: about %s new cases in weeks 49 to 52 (30 Nov to 27 Dec 2026) even with transmission halved "
                "from 2 November (phase 3 central scenario)" % format(F["call"]["cases_w49_52"], ","))
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = "Cases confirmed and probable by date of symptom onset, seven districts. Extract of 18/10/2026; onsets complete to 11/10/2026."
    rows = [("New cases, weeks 49 to 52 (planning figure, nearest thousand)", F["call"]["cases_w49_52"]),
            ("Reproduction number, weeks 36 to 41 (from the growth of onsets)", F["components"]["R"]),
            ("Mean serial interval, days", F["components"]["serial_interval_days"]),
            ("Growth of daily onsets, weeks 36 to 41, per day", F["components"]["growth_per_day"]),
            ("Reproduction number from 2 November (central scenario, half)", float("%.2f" % (g["R"] / 2))),
            ("Source-to-case pairs used (case onset to 11/10)", F["components"]["pairs"])]
    r = 4
    for k, v in rows:
        ws.cell(r, 1, k)
        c = ws.cell(r, 2, v)
        c.alignment = Alignment(horizontal="right")
        r += 1
    ws.cell(4, 1).font = bold
    ws.cell(4, 2).font = bold
    for rr, f in zip(range(4, 10), ("#,##0", "0.0", "0", "0.000", "0.00", "#,##0")):
        ws.cell(rr, 2).number_format = f
    r += 1
    ws.cell(r, 1, "Week").font = bold
    ws.cell(r, 2, "Monday").font = bold
    ws.cell(r, 3, "Cases by onset (observed)").font = bold
    ws.cell(r, 4, "Cases (projected)").font = bold
    for c in range(1, 5):
        ws.cell(r, c).fill = head
    x = g["series"]
    r += 1
    first = r
    for wk in range(30, 53):
        d0 = (wk - 22) * 7
        mon = calc.DAY0 + dt.timedelta(days=d0)
        ws.cell(r, 1, wk)
        ws.cell(r, 2, mon.strftime("%d/%m/%Y"))
        obs = float(x[d0:d0 + 7].sum()) if d0 + 6 <= 139 else None
        if obs is not None:
            ws.cell(r, 3, int(round(obs)))
        if d0 + 6 > 139:
            ws.cell(r, 4, int(round(float(x[d0:d0 + 7].sum()), -1)))
        r += 1
    for row in ws.iter_rows(min_row=first, max_row=r - 1, min_col=3, max_col=4):
        for c in row:
            c.number_format = "#,##0"
    ws.cell(r + 1, 1, "Week 42 holds onsets to 18/10 and is not complete, so it is projected; projected weeks are rounded to the nearest ten.")
    ws.column_dimensions["A"].width = 62
    ws.column_dimensions["B"].width = 13
    ws.column_dimensions["C"].width = 22
    ws.column_dimensions["D"].width = 18
    ws.freeze_panes = "A4"
    # ask 1
    a = wb.create_sheet("Contacts W37-W39")
    a.append(["Follow-up of contacts first listed in weeks 37 to 39 (7 to 27 September 2026)"])
    a["A1"].font = Font(bold=True, size=11)
    a.append([])
    a.append(["District", "People first listed", "Completed follow-up (%)"])
    for c in a[3]:
        c.font = bold
        c.fill = head
    for z in calc.ASK_ZONES:
        d = F["a1_%s" % z]
        a.append([z, d["people"], d["pct_completed"]])
    a.append([])
    a.append(["A person listed by both the tablet team and the directorate's paper list for the same source case is counted once."])
    a.append(["Completed: the 21-day follow-up that ends last for the person recorded as completed by either team."])
    for col, w in zip("ABC", [16, 20, 24]):
        a.column_dimensions[col].width = w
    for row in a.iter_rows(min_row=4, max_row=7):
        row[2].number_format = "0.0"
    # ask 2
    b = wb.create_sheet("Tamberlow field lab")
    b.append(["Tamberlow field laboratory: diagnostic samples by week of collection"])
    b["A1"].font = Font(bold=True, size=11)
    b.append([])
    b.append(["Week", "Average hours, collection to final result", "Final result within 24 h (%)"])
    for c in b[3]:
        c.font = bold
        c.fill = head
    for w in (38, 39, 40, 41):
        d = F["a2_w%d" % w]
        b.append([w, d["mean_hours"], d["pct_within_24h"]])
    b.append([])
    b.append(["The analyser writes result times in UTC; one hour is added to bring them to Orvanthe Standard Time like the collection and reception times."])
    b.append(["A sample re-run after an indeterminate result counts once, at its final result."])
    for col, w in zip("ABC", [10, 38, 30]):
        b.column_dimensions[col].width = w
    for row in b.iter_rows(min_row=4, max_row=7):
        row[1].number_format = "0.0"
        row[2].number_format = "0.0"
    n = wb.create_sheet("Notes")
    for line in [
            ["Notes"],
            [],
            ["Cases", "Confirmed and probable under the provincial case definition, as classified in the line list extract of 18/10/2026 23:59; not a case and suspected rows excluded; a case notified twice under two numbers with one sample counted once."],
            ["Weeks", "ISO weeks, Monday to Sunday, by date of symptom onset. Weeks 49 to 52 run 30/11/2026 to 27/12/2026."],
            ["Scenario", "Planning note PN-DMW-07, central scenario: every case with onset on or after 02/11/2026 causes half as many new cases as over weeks 36 to 41."],
            ["Serial interval", "From the transmission links, each source-to-case pair read against the time its source had to 11/10/2026, the last complete day of onsets."],
            ["Reproduction number", "Implied by the exponential growth rate of daily onsets, 31/08/2026 to 11/10/2026, through the serial interval."],
            ["Rounding", "Planning figure to the nearest thousand from the unrounded projection; projected weeks to the nearest ten."]]:
        n.append(line)
    n["A1"].font = Font(bold=True, size=11)
    n.column_dimensions["A"].width = 20
    n.column_dimensions["B"].width = 120
    for row in n.iter_rows(min_row=3):
        row[0].font = bold
        row[1].alignment = Alignment(wrap_text=True, vertical="top")
    ws.print_title_rows = "1:3"
    os.makedirs(GOLDEN, exist_ok=True)
    util.save_workbook(wb, os.path.join(GOLDEN, F_XLSX), title="TVD projection W49-W52")


def chart(g):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.ticker
    matplotlib.rcParams["svg.hashsalt"] = "task179"
    matplotlib.rcParams["font.family"] = "DejaVu Sans"
    x = g["series"]
    wks = list(range(30, 53))
    obs, proj = [], []
    for wk in wks:
        d0 = (wk - 22) * 7
        s = float(x[d0:d0 + 7].sum())
        if d0 + 6 <= 139:
            obs.append((wk, s))
        else:
            proj.append((wk, s))
    fig, ax = plt.subplots(figsize=(8.6, 4.4), dpi=100)
    ax.bar([w for w, _ in obs], [v for _, v in obs], color="#3B6E8F", width=0.75, label="Observed, by week of onset")
    ax.bar([w for w, _ in proj], [v for _, v in proj], color="#E2A13B", width=0.75, label="Projected, phase 3 central scenario")
    ax.axvline(44.5, color="#7A1F1F", lw=1.2, ls="--")
    ax.text(44.6, max(v for _, v in proj) * 1.02, "Phase 3 from 2 Nov (week 45)", color="#7A1F1F", fontsize=8.5)
    ax.axvspan(48.5, 52.5, color="#E2A13B", alpha=0.12, lw=0)
    ax.text(48.7, max(v for _, v in proj) * 0.9, "Weeks 49-52: about %s cases" % format(int(round(g["total"], -3)), ","), fontsize=8.5)
    ax.set_xlabel("ISO week, 2026")
    ax.set_ylabel("New cases (confirmed and probable)")
    ax.set_title("Dunmarrow TVD: about %s cases in weeks 49 to 52 even with transmission halved from 2 November" % format(int(round(g["total"], -3)), ","), fontsize=10, loc="left")
    ax.set_xticks(wks[::2])
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: format(int(v), ",")))
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False, fontsize=8.5, loc="upper left")
    ax.grid(axis="y", color="#DDDDDD", lw=0.6)
    ax.set_axisbelow(True)
    fig.tight_layout()
    bio = io.StringIO()
    fig.savefig(bio, format="svg", metadata={"Date": None, "Creator": "LMR epidemiology cell", "Format": None, "Type": None})
    plt.close(fig)
    util.write_text(os.path.join(GOLDEN, F_SVG), bio.getvalue().replace('id="matplotlib.axis_', 'id="axis_'))


if __name__ == "__main__":
    F, g = figures()
    with open(os.path.join(HERE, "figures.json"), "w") as f:
        json.dump(F, f, indent=1, ensure_ascii=False)
        f.write("\n")
    workbook(F, g)
    chart(g)
    print(json.dumps(F, indent=1, ensure_ascii=False))
    print([round(float(g["series"][(wk - 22) * 7:(wk - 22) * 7 + 7].sum())) for wk in range(40, 53)])
