"""task159 deliverables: the golden workbook and chart, generator/figures.json and submission.md, every figure computed
from the shipped pack (calc.py) and written once."""
from __future__ import annotations

import json
import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from openpyxl import Workbook  # noqa: E402
from openpyxl.styles import Alignment, Font, PatternFill  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc as C  # noqa: E402
import postprocess as PP  # noqa: E402

F_BOOK = "spring_2027_platform_conductors.xlsx"
F_CHART = "platform_escalators_am_peak.png"
DAYS = {"Mon": "Monday", "Tue": "Tuesday", "Wed": "Wednesday", "Thu": "Thursday", "Fri": "Friday"}


def compute(target):
    g = C.golden(target)
    a = C.ask_a(target)
    b = C.ask_b(target)
    return g, a, b


def _days_text(wds):
    if wds == C.WD:
        return "Monday to Friday"
    if wds == ["Tue", "Wed", "Thu"]:
        return "Tuesday to Thursday"
    return ", ".join(DAYS[w] for w in wds)


def figures(g, a, b):
    F = {"shifts_per_week": g["total"]}
    for wd in C.WD:
        F["shifts_%s" % wd] = g["per_wd"][wd]
    for code, st, lab in C.WATCH:
        F["posted_%s" % code] = g["posts"][code]
    for cx in C.WATCH_COMPLEXES:
        F["esc_down_%s" % cx] = a[cx][0]
        F["esc_up_%s" % cx] = a[cx][1]
        F["lift_hours_%s" % cx] = round(b[cx], 1)
    return F


HEAD_FILL = PatternFill("solid", fgColor="D9E4DD")
POST_FILL = PatternFill("solid", fgColor="F3D9A4")
BOLD = Font(name="Calibri", bold=True, size=11)


def write_book(path, g, a, b):
    wb = Workbook()
    ws = wb.active
    ws.title = "Postings"
    pw = g["per_wd"]
    ws.append(["Spring 2027 pick: %d platform conductor shifts a week, %d on Mondays and Fridays and %d Tuesday to Thursday"
               % (g["total"], pw["Mon"], pw["Tue"])])
    ws["A1"].font = Font(name="Calibri", bold=True, size=12)
    ws.append(["1 March to 25 June 2027, weekday mornings 06:45 to 10:00. Posted under the platform crowding standard, revision 4."])
    ws.append([])
    head = ["Code", "Complex", "Platform", "Rated capacity"] + [DAYS[w] for w in C.WD] + ["Shifts a week"]
    ws.append(head)
    for c in ws[4]:
        c.font = BOLD
        c.fill = HEAD_FILL
    for code, st, lab in C.WATCH:
        posts = g["posts"][code]
        row = [code, st, lab[0].upper() + lab[1:], g["model"].caps[code]] + ["Post" if w in posts else "" for w in C.WD] + [len(posts)]
        ws.append(row)
        r = ws.max_row
        for j, w in enumerate(C.WD):
            if w in posts:
                ws.cell(row=r, column=5 + j).fill = POST_FILL
    ws.append(["Total", "", "", ""] + [g["per_wd"][w] for w in C.WD] + [g["total"]])
    for c in ws[ws.max_row]:
        c.font = BOLD
    for col, w in zip("ABCDEFGHIJ", [9, 17, 28, 14, 10, 10, 11, 10, 9, 13]):
        ws.column_dimensions[col].width = w
    for row in ws.iter_rows(min_row=5, max_row=ws.max_row):
        row[3].number_format = "#,##0"
        for c in row[4:]:
            c.alignment = Alignment(horizontal="center")
    ws.freeze_panes = "A5"
    ws.print_title_rows = "4:4"

    ws2 = wb.create_sheet("Escalators AM peak")
    ws2.append(["Platform escalators at their rated flows between 07:00 and 09:30 on the autumn 2026 pick's weekdays (people a minute, station planning manual 5.3)"])
    ws2["A1"].font = Font(name="Calibri", bold=True, size=12)
    ws2.append([])
    ws2.append(["Complex", "Down to the platforms", "Up from the platforms"])
    for c in ws2[3]:
        c.font = BOLD
        c.fill = HEAD_FILL
    for cx in C.WATCH_COMPLEXES:
        ws2.append([cx, a[cx][0], a[cx][1]])
    for col, w in zip("ABC", [18, 22, 22]):
        ws2.column_dimensions[col].width = w

    ws3 = wb.create_sheet("Elevators")
    ws3.append(["Elevator-hours out of service, 07:00 to 09:45 on the autumn 2026 pick's weekday mornings"])
    ws3["A1"].font = Font(name="Calibri", bold=True, size=12)
    ws3.append([])
    ws3.append(["Complex", "Elevator-hours"])
    for c in ws3[3]:
        c.font = BOLD
        c.fill = HEAD_FILL
    for cx in C.WATCH_COMPLEXES:
        ws3.append([cx, round(b[cx], 1)])
        ws3.cell(row=ws3.max_row, column=2).number_format = "0.0"
    for col, w in zip("AB", [18, 16]):
        ws3.column_dimensions[col].width = w

    ws4 = wb.create_sheet("Notes")
    for line in [
        ["Notes"],
        ["Forecast: each platform's morning peak (the highest quarter-hour mean of the people on the platform as trains arrive, quarter-hours starting 07:00 to 09:30) for an average weekday of the pick, against 85 per cent of its rated capacity on 1 March 2027 (platform capacity register)."],
        ["Crowds: the October 2026 station census's flows onto and off every platform, scaled to an autumn Tuesday-to-Thursday morning and to each spring weekday by the fare export, run through the SPR27 weekday timetable at the fleet register's 150 people a car; a train takes at most the room it has after the riders it brings and those getting off, and the rest wait for the next train."],
        ["Line 5 runs eight-car trains from 1 March 2027 (spring 2027 service plan)."],
        ["Escalators: the station planning manual's rated flows (40, 60 and 80 people a minute for 600, 800 and 1,000 mm steps at 0.5 m/s, in proportion at other speeds), each escalator in the direction it was set to run and at the speed its controller is set to."],
        ["Elevators: hours not in normal passenger service between 07:00 and 09:45 on the autumn 2026 pick's weekdays (8 September to 18 December 2026, weekday timetable days), faults from the remote monitoring and planned maintenance from the work orders."],
        ["Station Planning, January 2027."],
    ]:
        ws4.append(line)
    ws4["A1"].font = BOLD
    ws4.column_dimensions["A"].width = 150
    for row in ws4.iter_rows(min_row=2):
        row[0].alignment = Alignment(wrap_text=True, vertical="top")
    wb.save(path)
    PP.normalize_ooxml(path, "Station Planning", "Station Planning", "2027-01-13T15:10:00Z", "2027-01-15T21:30:00Z",
                       excel=True, company="Vellmouth Transit Commission")


def write_chart(path, a):
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9.5, "svg.hashsalt": "task159"})
    fig, ax = plt.subplots(figsize=(8.6, 4.6), dpi=130)
    xs = list(range(len(C.WATCH_COMPLEXES)))
    w = 0.38
    down = [a[c][0] for c in C.WATCH_COMPLEXES]
    up = [a[c][1] for c in C.WATCH_COMPLEXES]
    b1 = ax.bar([x - w / 2 for x in xs], down, w, label="Down to the platforms", color="#3d7a5f")
    b2 = ax.bar([x + w / 2 for x in xs], up, w, label="Up from the platforms", color="#c9a24a")
    for bars in (b1, b2):
        for r in bars:
            ax.annotate("%d" % r.get_height(), (r.get_x() + r.get_width() / 2, r.get_height()), ha="center",
                        va="bottom", fontsize=8.5, xytext=(0, 2), textcoords="offset points")
    ax.set_xticks(xs)
    ax.set_xticklabels([c.replace(" ", "\n", 1) for c in C.WATCH_COMPLEXES])
    ax.set_ylabel("People a minute, 07:00 to 09:30")
    top = sorted(C.WATCH_COMPLEXES, key=lambda c: -a[c][0])[:2]
    ax.set_title("%s and %s can carry the most down to their platforms in the morning peak" % tuple(top),
                 fontsize=10.5)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(frameon=False, loc="upper right")
    ax.set_ylim(0, max(down + up) * 1.18)
    fig.text(0.01, 0.01, "Station planning manual 5.3 rated flows; directions from the escalator controller log, speeds "
             "from the asset register. Autumn 2026 pick weekdays.", fontsize=7.5, color="#555555")
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(path, metadata={"Software": None})
    plt.close(fig)


def write_submission(path, g, a, b):
    posts = g["posts"]
    five = [c for c, s, l in C.WATCH if posts[c] == C.WD]
    three = [c for c, s, l in C.WATCH if posts[c] == ["Tue", "Wed", "Thu"]]
    pw = g["per_wd"]
    L = []
    L.append("## Tags")
    L.append("")
    L.append("**Domain:** Urban & Regional Science (forecasting: a city subway's weekday-morning platform crowds "
             "forecast for a roster pick, the busiest platforms' counted crowds read as a backlog behind trains that "
             "arrive carrying their branch).")
    L.append("**Analytical objective:** Forecasting & Predictive Modeling.")
    L.append("")
    L.append("## 1. Final Recommendation")
    L.append("")
    L.append("**The spring 2027 pick should fund %d weekday-morning platform conductor shifts a week.** The Sallow Park "
             "Line 1 and Line 4 southbound crowds are riders left behind by trains that arrive carrying their branch, a "
             "backlog that forms only Tuesday to Thursday, and Corran Junction's Line 5 westbound backlog clears with "
             "the spring's eight-car trains. Not the count that carries last autumn's mid-week counts to Monday, "
             "Friday and the eight-car trains in proportion to entries, which posts Sallow Park on Mondays and Fridays "
             "and Corran Junction's Line 5 every weekday; not the count of one headway's arrivals, which misses the "
             "mid-week backlog." % g["total"])
    L.append("")
    L.append("## 2. Critical Components")
    L.append("")
    L.append("1. Shifts by weekday: Monday **%d**, Tuesday **%d**, Wednesday **%d**, Thursday **%d**, Friday **%d**."
             % tuple(pw[w] for w in C.WD))
    L.append("2. Posted Monday to Friday: **%s** (**%d** shifts)." % (", ".join(five), 5 * len(five)))
    L.append("3. Posted Tuesday to Thursday only: **%s** (**%d** shifts)." % (", ".join(three), 3 * len(three)))
    L.append("4. Not posted: **COR-5W** on any weekday, its backlog cleared by the eight-car trains.")
    L.append("")
    L.append("## 3. Step-by-Step Solution")
    L.append("")
    L.append("1. Converted station_census_2026-10.xlsx to people a minute onto and off each platform and through each "
             "passage, scaled each station to its autumn 2026 Tuesday-to-Thursday morning by the fare export's "
             "entries between 06:00 and 10:00 local on its census day.")
    L.append("2. From vtc_fare_entries_hourly_2024-06-03_2027-01-10.parquet (UTC to local), took each complex's "
             "autumn 2026 weekday index and the spring 2026 over autumn 2025 ratio for the spring pick.")
    L.append("3. Ran each line's trains through weekday_timetables_aut26_spr27.csv at cars times the fleet register's "
             "150-person maximum load, each train taking at most its room after the riders it brings from upstream "
             "and the riders getting off, the rest waiting for the next train.")
    L.append("4. Checked the model against platform_counts_autumn_2026.xlsx on the AUT26 timetable: it builds a backlog "
             "on the counted mid-week mornings at SAL-1S, SAL-4S and COR-5W and none on COR-5W's hybrid-day Monday and "
             "Friday, as counted, where carrying the mid-week count by entries puts COR-5W over its capacity on both.")
    L.append("5. Forecast each watch-list platform's morning peak quarter-hour for an average spring weekday on the "
             "SPR27 timetable (Line 5 eight cars) and compared it with 85 per cent of its rated capacity in "
             "platform_capacity_register.csv on 1 March 2027, per platform_crowding_standard_rev4.pdf.")
    L.append("6. Counted the platform-weekdays over the line: %d shifts a week." % g["total"])
    L.append("")
    L.append("## 4. Deliverable Answers")
    L.append("")
    L.append("### %s" % F_BOOK)
    L.append("")
    L.append("1. Shifts a week: %d (Monday %d, Tuesday %d, Wednesday %d, Thursday %d, Friday %d)."
             % ((g["total"],) + tuple(pw[w] for w in C.WD)))
    L.append("2. Posting schedule, each watch-list platform and its posted weekdays:")
    for code, st, lab in C.WATCH:
        p = posts[code]
        L.append("   - %s (%s, %s): %s" % (code, st, lab, _days_text(p) if p else "none"))
    L.append("3. Platform escalators at their rated flows between 07:00 and 09:30 on the autumn 2026 pick's weekdays, "
             "people a minute down to the platforms and up from them:")
    for cx in C.WATCH_COMPLEXES:
        L.append("   - %s: %d down, %d up" % (cx, a[cx][0], a[cx][1]))
    L.append("4. Elevator-hours out of service between 07:00 and 09:45 on the autumn 2026 pick's weekday mornings:")
    for cx in C.WATCH_COMPLEXES:
        L.append("   - %s: %.1f" % (cx, round(b[cx], 1)))
    L.append("")
    L.append("### %s" % F_CHART)
    L.append("")
    L.append("1. Grouped bar chart, one pair of bars per watch-list complex, the escalator figures down to the "
             "platforms and up from them, each bar labelled with its value.")
    L.append("")
    open(path, "w", encoding="utf-8").write("\n".join(L))


RIVALS = {}


def main(target, golden_dir, figures_path, submission_path):
    g, a, b = compute(target)
    r0 = C.tally(C.default_path(g["model"]))[0]
    r1 = C.tally(C.forecast_no_queue(g["model"]))[0]
    RIVALS.update(R0=r0, R1=r1)
    if os.path.isdir(golden_dir):
        for f in os.listdir(golden_dir):
            os.remove(os.path.join(golden_dir, f))
    os.makedirs(golden_dir, exist_ok=True)
    write_book(os.path.join(golden_dir, F_BOOK), g, a, b)
    write_chart(os.path.join(golden_dir, F_CHART), a)
    F = figures(g, a, b)
    F["rival_R0"] = r0
    F["rival_R1"] = r1
    F["params"] = {"threshold_per_cent": 85, "max_load_per_car": 150, "years": [2025, 2026, 2027]}
    with open(figures_path, "w") as f:
        json.dump(F, f, indent=1, sort_keys=True)
    write_submission(submission_path, g, a, b)
    return g, a, b


if __name__ == "__main__":
    t = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")
    main(t, os.path.join(os.path.dirname(HERE), "golden"), os.path.join(HERE, "figures.json"),
         os.path.join(os.path.dirname(HERE), "submission.md"))
