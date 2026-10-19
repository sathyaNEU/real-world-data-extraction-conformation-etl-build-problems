"""The golden deliverable, computed from the shipped pack: the staffing workbook (each class's caseload, its projected
managed spend for the program year, its clinical pharmacists, its 2025 rebates, and a chart of the pharmacists by
class); generator/figures.json carries every figure."""
import json
import os

import numpy as np

import bundle as B
import methods as M
import world as W


def compute(target):
    f = M.prepare(B.fills(target))
    co = M.on_therapy(f, W.LAST_DAY)
    g = dict(f=f, caseload=co.groupby("cls").size().reindex(W.CANDIDATES, fill_value=0).to_dict())
    g["spend"] = M.golden(f)
    g["pharm"] = M.pharmacists(g["spend"])
    g["rivals"] = {k: getattr(M, k)(f) for k in ("first_fill", "trailing", "run_rate", "analog", "from_start")}
    g["rebates"] = B.rebates_2025(target)
    return g


def rnd(v, unit):
    return int(np.floor(v / unit + 0.5) * unit)


def figures(g):
    P = W.PER_PHARMACIST
    f = {
        "call": {"pharmacists": {c: int(g["pharm"][c]) for c in W.CANDIDATES},
                 "total": int(sum(g["pharm"].values()))},
        "spend_m": {c: rnd(g["spend"][c], 1_000_000) // 1_000_000 for c in W.CANDIDATES},
        "spend_total_m": rnd(sum(g["spend"].values()), 1_000_000) // 1_000_000,
        "caseload": {c: int(g["caseload"][c]) for c in W.CANDIDATES},
        "rebates_k": {c: rnd(g["rebates"][c], 1000) // 1000 for c in W.CANDIDATES},
        "rivals": {k: {c: int(np.ceil(v[c] / P)) for c in W.CANDIDATES} for k, v in g["rivals"].items()},
        "classes": list(W.CANDIDATES),
        "per_pharmacist_m": P / 1_000_000,
        "duration_pooled_from_months": 36,
        "episode_gap_days": M.GAP,
        "rival_totals": {k: int(sum(np.ceil(v[c] / P) for c in W.CANDIDATES)) for k, v in g["rivals"].items()},
        "rebate_year": 2025,
        "program_year": {"start": 2026, "end": 2027},
        "charter_sections": {"caseload": 2.1, "spend": 2.2, "staffing": 3.1},
    }
    return f


def write_workbook(path, f):
    from openpyxl import Workbook
    from openpyxl.chart import BarChart, Reference
    from openpyxl.styles import Alignment, Font, PatternFill
    wb = Workbook()
    ws = wb.active
    ws.title = "Staffing"
    bold = Font(name="Calibri", bold=True)
    head = PatternFill("solid", fgColor="D9E1F2")
    ws.append(["%s: clinical pharmacists by class, program year July 2026 to June 2027" % W.PROGRAM])
    ws["A1"].font = Font(name="Calibri", bold=True, size=12)
    ws.append(["One pharmacist for each $1.5 million of a class's managed spend, or part (charter 3.1). Managed spend "
               "is projected for the members on therapy on June 30, 2026 from each class's spend and continuation by "
               "months into the current episode of therapy, at the Tallis 2026 schedule."])
    ws.append([])
    ws.append(["Class", "Class name", "Members on therapy June 30, 2026", "Managed spend, $ million",
               "Clinical pharmacists", "Rebates on fills dispensed in 2025, $ thousand"])
    for c in ws[4]:
        c.font = bold
        c.fill = head
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for c in W.CANDIDATES:
        ws.append([c, W.CLASSES[c]["name"], f["caseload"][c], f["spend_m"][c], f["call"]["pharmacists"][c],
                   f["rebates_k"][c]])
    n = ws.max_row
    ws.append(["Total", None, sum(f["caseload"].values()), f["spend_total_m"], f["call"]["total"],
               sum(f["rebates_k"].values())])
    for c in ws[ws.max_row]:
        c.font = bold
    for row in ws.iter_rows(min_row=5, max_row=ws.max_row):
        row[2].number_format = "#,##0"
        row[5].number_format = "#,##0"
    for col, w in zip("ABCDEF", (7, 50, 15, 14, 12, 18)):
        ws.column_dimensions[col].width = w
    ws.row_dimensions[4].height = 45
    ws.freeze_panes = "C5"
    chart = BarChart()
    chart.type = "bar"
    chart.title = "Clinical pharmacists by class, 2026-27"
    chart.y_axis.title = "Pharmacists"
    chart.add_data(Reference(ws, min_col=5, min_row=4, max_row=n), titles_from_data=True)
    chart.set_categories(Reference(ws, min_col=1, min_row=5, max_row=n))
    chart.legend = None
    chart.height = 8
    chart.width = 16
    ws.add_chart(chart, "A%d" % (ws.max_row + 3))
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 1
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.print_title_rows = "4:4"
    nt = wb.create_sheet("Notes")
    notes = [
        ("Prepared", "%s, %s, August 3, 2026, on the claims through June 30, 2026." % (W.PEOPLE["analyst"],
                                                                                    W.TITLES["analyst"])),
        ("Claims", "%s claims January 2019 to December 2025 and %s claims January to June 2026, reversed claims "
                   "removed, members linked through the plan's crosswalk, each fill priced at the Tallis 2026 schedule "
                   "plus its dispensing fee (charter 2.2)." % (W.OLD_PBM, W.NEW_PBM)),
        ("Caseload", "Members with a fill in the class whose days' supply reaches June 30, 2026 (charter 2.1)."),
        ("Managed spend", "Each caseload member's fills in the class from July 2026 to June 2027, projected from the "
                          "class's own record: the following twelve months' spend of members on therapy at each month "
                          "end since 2019, by months into their current episode of therapy, applied at the months each "
                          "caseload member's episode has run. A fill more than 60 days after the last supply ran out "
                          "starts a new episode, so a member back on a drug after stopping is projected as a new "
                          "starter. Members already on therapy when the Orrin file begins are counted with the "
                          "longest-standing members."),
        ("Pharmacists", "One for each $1.5 million of managed spend, or part (charter 3.1), on the unrounded spend."),
        ("Rebates", "%s rebate statement. Its contract year runs February to January (the statement's units tie "
                    "to the claims only on that calendar), so 2025's fills are contract quarters 2025-Q1 to 2025-Q4 "
                    "and January 2025, valued at contract quarter 2024-Q4's rebate per unit. Each product's quarterly "
                    "rebate is counted once, not once for each channel line it is shown on." % W.OLD_PBM),
    ]
    nt.append(["Notes"])
    nt["A1"].font = Font(name="Calibri", bold=True, size=12)
    for k, v in notes:
        nt.append([k, v])
        nt.cell(nt.max_row, 1).font = bold
        nt.cell(nt.max_row, 2).alignment = Alignment(wrap_text=True, vertical="top")
        nt.cell(nt.max_row, 1).alignment = Alignment(vertical="top")
    nt.column_dimensions["A"].width = 15
    nt.column_dimensions["B"].width = 100
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
