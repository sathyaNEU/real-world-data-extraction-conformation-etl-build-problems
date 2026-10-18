"""task162 goldens from the shipped pack: the staffing workbook (the call, the busiest week's forecast, the parallel
run's weekly figures and the component groups' arrivals), the parallel-run chart, and generator/figures.json (every
figure the write-up states, as it states it). Everything is computed by calc.py from the pack.

    python3 task162/generator/deliver.py <target> <golden dir> <figures.json>"""
from __future__ import annotations

import datetime as dt
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc as C            # noqa: E402
import common as K          # noqa: E402
import postprocess as PP    # noqa: E402

F_BOOK = "triage_staffing_q1_2027.xlsx"
F_CHART = "parallel_run_triage.svg"
MONTH3 = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def nearest(v, step):
    return int(K.round_half_up(v / step) * step)


def week_label(w):
    e = w + dt.timedelta(days=6)
    return "%d to %d %s" % (w.day, e.day, MONTH3[e.month]) if w.month == e.month else \
        "%d %s to %d %s" % (w.day, MONTH3[w.month], e.day, MONTH3[e.month])


def compute(target):
    D = C.load(target)
    F = C.forecast(D)
    A = C.load_asks(target, D)
    G = C.ask_figures(A)
    R1 = C.rung_default(D)
    R = C.reach_series(D)
    days, reach = C.forward_reach(D, R, F["H"])
    inst = C.project_installs(D, days)
    rw = {}
    for m, d in D.releases:
        if d in days:
            idx = [i for i, x in enumerate(days) if C.monday(x) == C.monday(d)]
            tot = sum(inst[p][idx].mean() for p in C.PLATFORMS)
            rw[m] = sum(reach[p][idx].sum() * inst[p][idx].mean() for p in C.PLATFORMS) / tot
    rec = {}
    for i, d in enumerate(D.days):
        w = C.monday(d)
        e = rec.setdefault(w, [0.0, 0.0, 0])
        e[0] += sum(R[p]["reach"][i] * D.inst[p][i] for p in C.PLATFORMS)
        e[1] += sum(D.inst[p][i] for p in C.PLATFORMS)
        e[2] += 1
    rec_max = max(v[0] / (v[1] / v[2]) for v in rec.values() if v[2] == 7)
    O = C.oos(D)
    seen, copies = set(), 0
    for i in sorted(A.issues, key=lambda i: (i["fields"]["created"], int(i["id"]))):
        n = C.legacy_id(i, "all")
        if n is None and i["fields"].get("customfield_10522"):
            n = int(i["fields"]["customfield_10522"])
        if n is None:
            continue
        copies += n in seen
        seen.add(n)
    return dict(D=D, F=F, A=A, G=G, R1=R1, release_reach=rw, record_max_reach=rec_max, oos=O, copies=copies)


def write_book(path, X):
    import openpyxl
    from openpyxl.styles import Alignment, Font, PatternFill
    F, G = X["F"], X["G"]
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Q1 2027"
    bold = Font(bold=True)
    ws["A1"] = "8 triagers for the first quarter of 2027: the busiest week, a release week, at about 900 triage items"
    ws["A1"].font = Font(bold=True, size=14)
    ws["A2"] = "Quarter: Monday 4 January to Sunday 4 April 2027, 13 weeks, Monday to Sunday, Helsinki time."
    ws["A4"] = "Triagers needed"
    ws["B4"] = F["triagers"]
    ws["A5"] = "Busiest week, forecast triage items (nearest 100)"
    ws["B5"] = nearest(F["busiest"], 100)
    ws["A6"] = "Standard"
    ws["B6"] = "120 triage items per triager-week"
    for c in ("A4", "A5", "B4", "B5"):
        ws[c].font = bold
    ws["A8"] = "Releases in the quarter"
    ws["A8"].font = bold
    row = 9
    for m, d in X["D"].releases:
        if C.Q1_WEEKS[0] <= d <= C.Q1_WEEKS[-1] + dt.timedelta(days=6):
            ws.cell(row=row, column=1, value="%d.0" % m)
            ws.cell(row=row, column=2, value=d).number_format = "d.m.yyyy"
            row += 1
    row += 1
    notes = [
        "Triage items counted as the cutover runbook sets out: every report filed through the report form, "
        "duplicates included, security reports out.",
        "Each release is forecast from how installs took the record's releases: an install updates when the "
        "browser restarts, and most Windows installs still on the old version restart on the Wednesday and "
        "Thursday after Patch Tuesday.",
        "All three releases ship on Patch Tuesday, so each meets that restart wave inside its release week.",
        "First-use reports per install reaching a new version and the baseline per active install are fitted on "
        "the old tracker's record from 1 October 2025; installs projected from the same weeks a year earlier.",
    ]
    for t in notes:
        ws.cell(row=row, column=1, value=t).alignment = Alignment(wrap_text=False)
        row += 1
    ws.column_dimensions["A"].width = 48
    ws.column_dimensions["B"].width = 32

    ws2 = wb.create_sheet("Parallel run")
    ws2["A1"] = "Parallel run on the new tracker, 2 to 29 November 2026"
    ws2["A1"].font = Font(bold=True, size=13)
    head = ["Week (filed)", "No triage action within 24 hours of filing", "Closed by the end of the run"]
    for j, h in enumerate(head):
        c = ws2.cell(row=3, column=j + 1, value=h)
        c.font = bold
        c.fill = PatternFill("solid", fgColor="DDEBF7")
    for i, w in enumerate(C.RUN_WEEKS):
        ws2.cell(row=4 + i, column=1, value=week_label(w))
        ws2.cell(row=4 + i, column=2, value=G["no_action"][w]).number_format = "#,##0"
        ws2.cell(row=4 + i, column=3, value=G["closed"][w]).number_format = "#,##0"
    ws2.cell(row=8, column=1, value="The run").font = bold
    for col, key in ((2, "no_action"), (3, "closed")):
        c = ws2.cell(row=8, column=col, value=sum(G[key][w] for w in C.RUN_WEEKS))
        c.font = bold
        c.number_format = "#,##0"
    ws2.cell(row=10, column=1, value="Triage items: the run's reports filed through the report form, by the week filed "
                                     "on the old tracker, Helsinki time; the run ended at 23:59 on Sunday 29 November.")
    ws2.freeze_panes = "A4"
    ws2.column_dimensions["A"].width = 18
    ws2.column_dimensions["B"].width = 40
    ws2.column_dimensions["C"].width = 30

    ws3 = wb.create_sheet("Component groups")
    ws3["A1"] = "Parallel run: triage items by the component group they arrived in"
    ws3["A1"].font = Font(bold=True, size=13)
    for j, h in enumerate(["Component group", "Triage items"]):
        c = ws3.cell(row=3, column=j + 1, value=h)
        c.font = bold
        c.fill = PatternFill("solid", fgColor="DDEBF7")
    for i, g in enumerate(C.GROUPS):
        ws3.cell(row=4 + i, column=1, value=g)
        ws3.cell(row=4 + i, column=2, value=G["groups"][g]).number_format = "#,##0"
    ws3.cell(row=12, column=1, value="The run").font = bold
    c = ws3.cell(row=12, column=2, value=sum(G["groups"][g] for g in C.GROUPS))
    c.font = bold
    c.number_format = "#,##0"
    ws3.cell(row=14, column=1, value="The group of the component the bridge wrote each report into; each report "
                                     "arrived in one component.")
    ws3.column_dimensions["A"].width = 26
    ws3.column_dimensions["B"].width = 14
    ws3.freeze_panes = "A4"

    ws4 = wb.create_sheet("Notes")
    rows = [
        ("As of", "Files taken on 18 December 2026; the old tracker's export holds reports filed to 17 December, the "
                  "new tracker's export of the run was taken on 4 December."),
        ("Triage item", "A report filed through the report form, duplicates included (cutover runbook). Security "
                        "reports, site reports filed with the Report a site issue tool and the team's own tasks are "
                        "not triage items."),
        ("Triage action", "A change by one of the rota's triagers to a report's status, resolution, component or "
                          "priority, or a move to another team's project (working agreement)."),
        ("Filed", "When the reporter filed the report on the old tracker (its opened time, through the old bug "
                  "number); the new tracker's Created is when the bridge wrote the copy."),
        ("Closed", "In Resolved or Closed, or in another team's project, at 23:59 on Sunday 29 November."),
        ("Copies", "The %d issues the bridge wrote a second time on 18 November carry an old bug number already in "
                   "the run and are not counted again." % X["copies"]),
        ("Rounding", "Triagers rounded up from the busiest week's forecast at 120 items per triager-week; the forecast "
                     "shown to the nearest 100."),
    ]
    ws4["A1"] = "Notes"
    ws4["A1"].font = Font(bold=True, size=13)
    for i, (k, v) in enumerate(rows):
        ws4.cell(row=3 + i, column=1, value=k).font = bold
        ws4.cell(row=3 + i, column=2, value=v)
    ws4.column_dimensions["A"].width = 16
    ws4.column_dimensions["B"].width = 110
    wb.save(path)
    PP.normalize_ooxml(path, K.PEOPLE["lead"], K.PEOPLE["lead"], "2026-12-18T07:05:00Z", "2026-12-18T13:42:00Z",
                       excel=True, company=K.VENDOR)


def write_chart(path, G):
    W, H = 760, 480
    left, right, top, bottom = 70, 30, 70, 110
    vals = [(G["no_action"][w], G["closed"][w]) for w in C.RUN_WEEKS]
    vmax = max(max(a, b) for a, b in vals)
    ymax = int(math.ceil(vmax / 50.0) * 50)
    ph = H - top - bottom
    pw = W - left - right
    gw = pw / len(vals)
    bw = gw * 0.32
    col = ("#b4532a", "#2c6e8a")
    out = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" '
           'font-family="Arial, Helvetica, sans-serif">' % (W, H, W, H),
           '<rect width="%d" height="%d" fill="#ffffff"/>' % (W, H),
           '<text x="%d" y="30" font-size="17" font-weight="bold" fill="#1f2328">Parallel run on the new tracker, '
           '2 to 29 November 2026</text>' % left,
           '<text x="%d" y="50" font-size="12" fill="#5b636b">Triage items by the week they were filed, Monday to Sunday, '
           'Helsinki time</text>' % left]
    for k in range(0, ymax + 1, 50):
        y = top + ph - ph * k / ymax
        out.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="#e1e4e8" stroke-width="1"/>' % (left, y, W - right, y))
        out.append('<text x="%d" y="%.1f" font-size="11" fill="#5b636b" text-anchor="end">%d</text>' % (left - 8, y + 4, k))
    out.append('<text x="18" y="%d" font-size="12" fill="#1f2328" transform="rotate(-90 18 %d)" '
               'text-anchor="middle">Triage items</text>' % (top + ph // 2, top + ph // 2))
    for i, (w, (a, b)) in enumerate(zip(C.RUN_WEEKS, vals)):
        x0 = left + gw * i + gw * 0.16
        for j, v in enumerate((a, b)):
            x = x0 + j * (bw + 4)
            h = ph * v / ymax
            y = top + ph - h
            out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s"/>' % (x, y, bw, h, col[j]))
            out.append('<text x="%.1f" y="%.1f" font-size="12" fill="#1f2328" text-anchor="middle">%d</text>'
                       % (x + bw / 2, y - 5, v))
        out.append('<text x="%.1f" y="%d" font-size="12" fill="#1f2328" text-anchor="middle">%s</text>'
                   % (x0 + bw + 2, top + ph + 20, week_label(w)))
    out.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#1f2328" stroke-width="1"/>' % (left, top + ph, W - right, top + ph))
    ly = H - 52
    for j, name in enumerate(("No triage action within 24 hours of filing", "Closed by the end of the run")):
        x = left + j * 330
        out.append('<rect x="%d" y="%d" width="14" height="14" fill="%s"/>' % (x, ly - 11, col[j]))
        out.append('<text x="%d" y="%d" font-size="12" fill="#1f2328">%s</text>' % (x + 20, ly, name))
    out.append('<text x="%d" y="%d" font-size="10.5" fill="#5b636b">The run ended at 23:59 on Sunday 29 November. '
               'Source: new tracker export of 4 December; filing times from the old tracker.</text>' % (left, H - 18))
    out.append("</svg>")
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(out) + "\n")


def figures(X):
    F, G, R1 = X["F"], X["G"], X["R1"]
    H = F["H"]["Windows"]
    o = X["oos"]
    prof_err = []
    rst_err = []
    for m in (46, 47):
        k = o[m][2]          # the third week: the restart wave a fortnight after the release
        prof_err.append(k["profile"] / k["actual"])
        rst_err.append(abs(k["restart"] / k["actual"] - 1))
    fig = {
        "call": {"triagers": F["triagers"], "busiest_week": "{:,}".format(nearest(F["busiest"], 100)),
                 "standard": 120, "default_triagers": R1["triagers"], "rounding_step": 100},
        "components": {
            "release_week_reach_pct": "%d" % nearest(100 * min(X["release_reach"].values()), 5),
            "record_max_reach_pct": "%d" % round(100 * X["record_max_reach"]),
            "windows_wed_pct": "%d" % round(100 * H["burst1"]),
            "windows_thu_pct": "%d" % round(100 * H["burst2"]),
            "windows_weekday_pct": "%d" % round(100 * H["weekday"]),
            "windows_two_day_pct": "%d" % round(100 * (1 - (1 - H["burst1"]) * (1 - H["burst2"]))),
        },
        "steps": {
            "last_year_busiest": "{:,}".format(int(R1["last_year"])),
            "growth_pct": "%.1f" % K.round_half_up(100 * (C.install_growth(X["D"]) - 1), 1),
            "default_busiest": "{:,}".format(nearest(R1["busiest"], 100)),
            "profile_share_pct": "%d" % nearest(100 * max(prof_err), 10),
            "restart_within_pct": "%d" % (5 * math.ceil(100 * max(rst_err) / 5)),
            "late_releases": 2, "early_releases": 13,
            "first_use_per_10000": "%.1f" % K.round_half_up(F["fit"]["rho"] * 1e4, 1), "per": "10,000",
        },
        "answers": {
            "triagers": F["triagers"], "busiest_week": "{:,}".format(nearest(F["busiest"], 100)),
            "ask_a": [{"week": week_label(w), "no_action": G["no_action"][w], "closed": G["closed"][w]}
                      for w in C.RUN_WEEKS],
            "ask_b": {g: G["groups"][g] for g in C.GROUPS},
        },
        "unrounded": {"busiest": round(F["busiest"], 2), "sigma": round(F["sigma"], 2)},
    }
    return fig


def main(target, golden, fig_path):
    os.makedirs(golden, exist_ok=True)
    X = compute(target)
    write_book(os.path.join(golden, F_BOOK), X)
    write_chart(os.path.join(golden, F_CHART), X["G"])
    with open(fig_path, "w", encoding="utf-8") as fh:
        json.dump(figures(X), fh, indent=2, ensure_ascii=False, sort_keys=True)
        fh.write("\n")
    mt = calendar_mtime()
    for f in os.listdir(golden):
        os.utime(os.path.join(golden, f), (mt, mt))
    return X


def calendar_mtime():
    import calendar
    return calendar.timegm((2026, 12, 18, 13, 42, 0, 0, 0, 0))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
