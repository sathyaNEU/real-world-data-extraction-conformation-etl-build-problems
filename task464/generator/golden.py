#!/usr/bin/env python3
"""task464: the two deliverables the prompt names, written by script from the answers."""
import csv
import datetime as dt
import os

import openpyxl
from openpyxl.chart import BarChart, Reference
from openpyxl.styles import Alignment, Border, Font, Side
from openpyxl.utils import get_column_letter

import answers
import pack
import world

CSV_NAME = "outpatient_capacity_2027.csv"
XLSX_NAME = "area_capacity_2027.xlsx"
THIN = Side(style="thin", color="FF999999")


def _head(ws, head, widths):
    ws.append(head)
    for i, h in enumerate(head, start=1):
        ws.column_dimensions[get_column_letter(i)].width = widths[i - 1]
        c = ws.cell(row=1, column=i)
        c.font = Font(bold=True)
        c.alignment = Alignment(horizontal="left" if i <= 2 else "right", wrap_text=False)
    ws.freeze_panes = "A2"


def write(out_dir, sites, by_area, extra, rows, lic_rows, filing_rows, dir_rows, oon_main, oon_runout):
    os.makedirs(out_dir, exist_ok=True)
    C = answers.call(sites, by_area)
    S = answers.per_site(sites)
    A = answers.ask_a(sites, extra, rows, oon_main, oon_runout)
    B = answers.ask_b(lic_rows)
    D = answers.ask_c(sites, extra, filing_rows, lic_rows, dir_rows)

    with open(os.path.join(out_dir, CSV_NAME), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["plan_site_id", "site_name", "service_area_code", "service_area_name",
                    "weekly_treatment_slots"])
        for r in S:
            w.writerow([r["site"], r["name"], r["area"], r["area_name"], r["slots"]])

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Area Capacity"
    _head(ws, ["service_area_code", "service_area_name", "weekly_treatment_slots",
               "required_weekly_slots", "meets_standard", "shortfall_slots"],
          [20, 20, 22, 22, 16, 15])
    for a in C["areas"]:
        ws.append([a["code"], a["name"], a["slots"], a["required"], "yes" if a["meets"] else "no",
                   a["shortfall"] if not a["meets"] else None])
    r = ws.max_row + 1
    ws.cell(row=r, column=2, value="network").font = Font(bold=True)
    ws.cell(row=r, column=3, value=C["network"]).font = Font(bold=True)
    ws.cell(row=r, column=4, value=sum(a["required"] for a in C["areas"])).font = Font(bold=True)
    ws.cell(row=r, column=5, value="%d of 12 short" % len(C["short"])).font = Font(bold=True)
    for row in ws.iter_rows(min_row=2, max_row=r, min_col=3, max_col=6):
        for c in row:
            c.number_format = "#,##0"
    r += 2
    ws.cell(row=r, column=1, value="nearest the standard without meeting it")
    ws.cell(row=r, column=3, value=world.AREA[C["nearest"]]["name"])
    ws.cell(row=r, column=4, value=C["nearest_shortfall"]).number_format = "#,##0"
    ws.cell(row=r + 1, column=1, value="position as at")
    ws.cell(row=r + 1, column=3, value=world.ASOF.isoformat())
    ws.cell(row=r + 2, column=1, value="basis")
    ws.cell(row=r + 2, column=3,
            value="Provider Network Agreement 2027, Schedule 4, clauses 4.2 and 4.3")

    ch = BarChart()
    ch.type = "col"
    ch.style = 2
    ch.title = "Six of twelve service areas sit below the 2027 adequacy standard"
    ch.y_axis.title = "Weekly treatment slots"
    ch.x_axis.title = None
    ch.height, ch.width = 9.0, 23.0
    data = Reference(ws, min_col=3, max_col=4, min_row=1, max_row=13)
    cats = Reference(ws, min_col=2, min_row=2, max_row=13)
    ch.add_data(data, titles_from_data=True)
    ch.set_categories(cats)
    ch.gapWidth = 40
    ws.add_chart(ch, "H2")

    s2 = wb.create_sheet("Out of Network 2026")
    _head(s2, ["service_area_code", "service_area_name", "half_of_2026",
               "out_of_network_treatments", "share_of_all_area_treatments_pct"], [20, 20, 14, 26, 30])
    for a in A:
        s2.append([a["code"], a["name"], a["half"], a["treatments"], a["share"]])
    for row in s2.iter_rows(min_row=2, min_col=4, max_col=4):
        for c in row:
            c.number_format = "#,##0"
    for row in s2.iter_rows(min_row=2, min_col=5, max_col=5):
        for c in row:
            c.number_format = "0.0"

    s3 = wb.create_sheet("Licensed Supply")
    _head(s3, ["service_area_code", "service_area_name", "licensed_sites", "licensed_stations"],
          [20, 20, 16, 18])
    for b in B:
        s3.append([b["code"], b["name"], b["sites"], b["stations"]])

    s4 = wb.create_sheet("Sites Dropped")
    _head(s4, ["service_area_code", "service_area_name", "sites_in_2026_filing_without_2027_intent",
               "licensed_stations_then"], [20, 20, 40, 24])
    for d in D:
        s4.append([d["code"], d["name"], d["sites"], d["stations"]])
    for sh in (s3, s4):
        for row in sh.iter_rows(min_row=2, min_col=3, max_col=4):
            for c in row:
                c.number_format = "#,##0"
    ws.print_area = "A1:F17"
    ws.page_setup.orientation = "landscape"
    wb.save(os.path.join(out_dir, XLSX_NAME))
    return dict(call=C, sites=S, ask_a=A, ask_b=B, ask_c=D)
