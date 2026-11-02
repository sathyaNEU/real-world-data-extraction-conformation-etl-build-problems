"""The golden deliverables from the shipped pack: gallstone_nel_plan_2027_28.xlsx and rtt_baseline_general_surgery_2025_26.csv."""
from __future__ import annotations

import json
import os
import sys

import numpy as np
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc as C      # noqa: E402
import common         # noqa: E402

TASK = os.path.dirname(HERE)
FY_LABEL = {2021: "2021/22", 2022: "2022/23", 2023: "2023/24", 2024: "2024/25", 2025: "2025/26", 2026: "2026/27 (Apr-Oct)"}


def figures(P):
    g = C.golden(P)
    L = C.line(P)
    L, pm = C.link(L, P)
    hist = []
    for fy in range(2021, 2027):
        sub = L[L.fy == fy]
        months = [m for m in pm.index if m // 12 + 2021 == fy]
        hist.append({"fy": fy, "spells": int(len(sub)), "listed": int(sub.listed.sum()), "not_listed": int((~sub.listed).sum()),
                     "patient_months": int(pm.loc[months].sum())})
    asks = C.ask_tables(P, "golden")
    tr = C.plan_traj(P.t)
    return g, hist, asks, tr


def fmt(ws, widths):
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w


def write(P, gold_dir):
    os.makedirs(gold_dir, exist_ok=True)
    g, hist, asks, tr = figures(P)
    call = int(round(g["total"] / 50.0) * 50)
    bold = Font(bold=True)
    head = PatternFill("solid", fgColor="DCE6F1")
    wb = Workbook()
    ws = wb.active
    ws.title = "NEL-GS-07"
    rows = [["NEL-GS-07 for 2027/28: plan 400, the list part falling to 47.8 as Wyecross clears the cholecystectomy list" if call == 400 else "NEL-GS-07 for 2027/28"], ["Prepared by Alison Morgan, Capacity and Demand Planning, 2 November 2026; records to 31 October 2026"], [],
            ["Plan figure (nearest 50)", call], ["Central expectation", round(g["total"], 1)], [],
            ["Built from", "2027/28", "Basis"],
            ["Admissions of patients not on the cholecystectomy list", round(g["first"], 1),
             "2024/25 to 2026/27 (April to October) age and sex rates per head, on the 2022-based mid-2027 population"],
            ["Admissions of patients waiting for a cholecystectomy", round(g["listed_part"], 1),
             "list admission rate per patient-month x planned patient-months on the list in 2027/28"],
            ["Admission rate per patient-month on the list", round(g["hazard"], 4), "2022/23 to 2026/27 (to October): admissions of listed patients / month-end patients on the list"],
            ["Planned patient-months on the list, 2027/28", g["pm_plan"], "Elective Capacity Plan 2027/28, section 3, month ends April 2027 to March 2028"],
            [], ["Rate method on all admissions (for comparison)", round(g["default"], 1), "the same rates without the split; it carries the list at its 2022 to 2026 size"]]
    for r in rows:
        ws.append(r)
    ws["A1"].font = Font(bold=True, size=12)
    for c in ("A4", "B4", "A7", "B7", "C7"):
        ws[c].font = bold
    for c in ("A7", "B7", "C7"):
        ws[c].fill = head
    ws["B10"].number_format = "0.0000"
    ws["B11"].number_format = "#,##0"
    ws.append([])
    ws.append(["Definitions: Activity Line Definitions v1.2 (7 October 2026), NEL-GS-07; plan list: Elective Capacity Plan 2027/28, section 3."])
    ws.append(["A spell counts as a listed patient's when a cholecystectomy pathway added before the admission is on the month-end PTL of the admission month or the month before."])
    fmt(ws, [52, 14, 96])
    h = wb.create_sheet("History")
    h.append(["Financial year", "Line spells", "Patient on the cholecystectomy list at admission", "Not on the list",
              "Patient-months on the list (month ends)", "Listed admissions per patient-month"])
    for r in hist:
        h.append([FY_LABEL[r["fy"]], r["spells"], r["listed"], r["not_listed"], r["patient_months"], round(r["listed"] / r["patient_months"], 4)])
    for c in h[1]:
        c.font = bold
        c.fill = head
        c.alignment = Alignment(wrap_text=True)
    fmt(h, [20, 12, 22, 14, 20, 20])
    h.freeze_panes = "A2"
    for r in h.iter_rows(min_row=2):
        r[4].number_format = "#,##0"
        r[5].number_format = "0.0000"
    p = wb.create_sheet("Plan year")
    p.append(["Month end", "Planned cholecystectomy list (both hospitals)", "Expected admissions of listed patients"])
    keys = list(tr.keys())[5:]
    for k in keys:
        p.append([k, tr[k], round(g["hazard"] * tr[k], 1)])
    p.append(["2027/28", sum(tr[k] for k in keys), round(g["listed_part"], 1)])
    for c in p[1]:
        c.font = bold
        c.fill = head
        c.alignment = Alignment(wrap_text=True)
    fmt(p, [14, 24, 22])
    q = wb.create_sheet("RTT baseline")
    q.append(["Quarter end", "Hospital", "Waits of 52 weeks or more from referral", "Hernia repairs waited for"])
    rows = []
    for d in C.QDATES:
        for site, name in (("MGH", "Marlstead General"), ("FEN", "Fennick")):
            rows.append([d, name, asks[("A", d, site)], asks[("B", d, site)]])
            q.append(rows[-1])
    for c in q[1]:
        c.font = bold
        c.fill = head
    fmt(q, [14, 20, 22, 20])
    q.freeze_panes = "A2"
    q.append([])
    q.append(["RTT-GS-02 and RTT-GS-03 on the Activity Line Definitions; clocks from the e-Referral Service referral date where the pathway carries a UBRN."])
    path = os.path.join(gold_dir, "gallstone_nel_plan_2027_28.xlsx")
    wb.properties.creator = "Alison Morgan"
    wb.save(path)
    common.freeze_xlsx(path, "Alison Morgan")
    pd.DataFrame(rows, columns=["quarter_end", "hospital", "waits_52_weeks_or_more", "hernia_repairs_waited_for"]).to_csv(
        os.path.join(gold_dir, "rtt_baseline_general_surgery_2025_26.csv"), index=False, lineterminator="\n")
    fig = {"call.gallstone_emergency_2027_28": call, "call.central_expectation": round(g["total"], 1),
           "comp.not_listed_2027_28": round(g["first"], 1), "comp.listed_2027_28": round(g["listed_part"], 1),
           "comp.hazard_per_patient_month": round(g["hazard"], 4), "comp.planned_patient_months": g["pm_plan"],
           "default.rate_method_2027_28": round(g["default"], 1), "conv.rounding": 50, "comp.not_listed_about": int(round(g["first"] / 10.0) * 10), "conv.wait_weeks": 52, "conv.wait_days": 364}
    for (a, d, site), v in sorted(asks.items()):
        fig["ask%s.%s.%s" % (a, d, site)] = v
    json.dump(fig, open(os.path.join(HERE, "figures.json"), "w"), indent=1, sort_keys=True)
    return fig


if __name__ == "__main__":
    f = write(C.Pack(), os.path.join(TASK, "golden"))
    print(json.dumps(f, indent=1))
