"""The golden deliverables: heat_resilience_grants_2027.xlsx (the scorecard with its chart, the medical examiner
offices' quarters and the registration shares) and summer_2026_deaths_by_place.csv (each place's deaths by month)."""
import csv
import datetime as dt
import io
import os

from openpyxl import Workbook
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.chart.label import DataLabelList
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

import postprocess as PP
import world as W

XLSX = "heat_resilience_grants_2027.xlsx"
CSV = "summer_2026_deaths_by_place.csv"
BLUE = "005EB8"
THIN = Side(style="thin", color="AEB7BD")


def r1(x):
    return round(x * 10 + 1e-9) / 10.0


def _head(ws, row, values, widths=None):
    for j, v in enumerate(values, start=1):
        c = ws.cell(row=row, column=j, value=v)
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor=BLUE)
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = Border(top=THIN, bottom=THIN, left=THIN, right=THIN)
    if widths:
        for j, w in enumerate(widths):
            ws.column_dimensions["ABCDEFGHIJ"[j]].width = w


def workbook(S, path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Scorecard"
    ws["A1"] = "Heat Resilience Fund 2027: qualifying places"
    ws["A1"].font = Font(bold=True, size=13, color=BLUE)
    ws["A2"] = ("Deaths of residents from 1 June to 31 August 2026 by usual address and date of death, registered or "
                "not, from the register and both medical examiner offices' logs at the close of 9 October 2026. "
                "A place qualifies at an excess of 10.0 per cent or more over Table 1.")
    ws["A2"].alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells("A2:H2")
    ws.row_dimensions[2].height = 44
    _head(ws, 4, ["Place", "Code", "Deaths", "of which not yet registered", "Expected (Table 1)", "Excess (%)",
                  "Qualifies", "Grant (GBP)"], [16, 12, 9, 13, 12, 10, 10, 13])
    ws.row_dimensions[4].height = 30
    r = 5
    for p in W.NAMES:
        q = S["excess"][p] >= 100 * W.LINE
        vals = [p, W.CODE[p], S["counts"][p], S["added"].get(p, 0), S["expected"][p], r1(S["excess"][p]),
                "Yes" if q else "No", W.GRANT if q else W.STANDARD]
        for j, v in enumerate(vals, start=1):
            c = ws.cell(row=r, column=j, value=v)
            c.border = Border(top=THIN, bottom=THIN, left=THIN, right=THIN)
            if j == 6:
                c.number_format = "0.0"
            if j == 8:
                c.number_format = "#,##0"
            if j == 7 and q:
                c.font = Font(bold=True, color=BLUE)
        r += 1
    tot = sum(S["counts"].values())
    texp = sum(S["expected"].values())
    vals = ["Ellesmoor", "", tot, sum(S["added"].values()), texp, r1(100.0 * (tot - texp) / texp), "",
            sum(W.GRANT if S["excess"][p] >= 100 * W.LINE else W.STANDARD for p in W.NAMES)]
    for j, v in enumerate(vals, start=1):
        c = ws.cell(row=r, column=j, value=v)
        c.font = Font(bold=True)
        c.border = Border(top=THIN, bottom=Side(style="double", color="425563"), left=THIN, right=THIN)
        if j == 6:
            c.number_format = "0.0"
        if j == 8:
            c.number_format = "#,##0"
    # helper column for the qualifying line on the chart
    ws.cell(row=4, column=10, value="Line (%)").font = Font(color="768692", size=8)
    for i in range(6):
        ws.cell(row=5 + i, column=10, value=10.0).font = Font(color="768692", size=8)
    ch = BarChart()
    ch.type = "col"
    ch.title = "Summer 2026 excess deaths by place"
    ch.y_axis.title = "Excess over expected (%)"
    ch.y_axis.majorGridlines = None
    ch.add_data(Reference(ws, min_col=6, min_row=4, max_row=10), titles_from_data=True)
    ch.set_categories(Reference(ws, min_col=1, min_row=5, max_row=10))
    ch.dataLabels = DataLabelList()
    ch.dataLabels.showVal = True
    ch.series[0].graphicalProperties.solidFill = BLUE
    ln = LineChart()
    ln.add_data(Reference(ws, min_col=10, min_row=4, max_row=10), titles_from_data=True)
    ln.series[0].graphicalProperties.line.solidFill = "DA291C"
    ln.series[0].graphicalProperties.line.dashStyle = "dash"
    ch += ln
    ch.height, ch.width = 8.5, 17
    ch.legend.position = "b"
    ws.add_chart(ch, "A13")

    w2 = wb.create_sheet("ME offices 2025-26")
    w2["A1"] = "Deaths scrutinised by each medical examiner office, by quarter of 2025-26"
    w2["A1"].font = Font(bold=True, size=12, color=BLUE)
    w2["A2"] = "Each death counted once, in the quarter its scrutiny was completed (local date)."
    _head(w2, 4, ["Office", "Apr to Jun 2025", "Jul to Sep 2025", "Oct to Dec 2025", "Jan to Mar 2026", "2025-26"],
          [30, 13, 13, 13, 13, 11])
    w2.row_dimensions[4].height = 30
    for i, (office, label) in enumerate((("North", "North Ellesmoor ME Office"), ("South", "South Ellesmoor ME Office"))):
        vals = [label] + [S["ask_b"][(office, q)] for q in (1, 2, 3, 4)] + [sum(S["ask_b"][(office, q)] for q in (1, 2, 3, 4))]
        for j, v in enumerate(vals, start=1):
            c = w2.cell(row=5 + i, column=j, value=v)
            c.border = Border(top=THIN, bottom=THIN, left=THIN, right=THIN)
            if j > 1:
                c.number_format = "#,##0"

    w3 = wb.create_sheet("Registration 2025")
    w3["A1"] = "Deaths in 2025 with a medical certificate registered within five days of death (%)"
    w3["A1"].font = Font(bold=True, size=12, color=BLUE)
    w3["A2"] = "By place of usual address and calendar quarter of death; each register entry's own registration date."
    _head(w3, 4, ["Place", "Jan to Mar", "Apr to Jun", "Jul to Sep", "Oct to Dec"], [16, 11, 11, 11, 11])
    for i, p in enumerate(W.NAMES):
        vals = [p] + [r1(S["ask_c"][(p, q)]) for q in (1, 2, 3, 4)]
        for j, v in enumerate(vals, start=1):
            c = w3.cell(row=5 + i, column=j, value=v)
            c.border = Border(top=THIN, bottom=THIN, left=THIN, right=THIN)
            if j > 1:
                c.number_format = "0.0"
    for s in (ws, w2, w3):
        s.sheet_view.showGridLines = False
    wb.properties.creator = "Jason Leach"
    wb.properties.lastModifiedBy = "Jason Leach"
    wb.properties.created = dt.datetime(2026, 10, 12, 9, 2, 17)
    wb.properties.modified = dt.datetime(2026, 10, 14, 16, 31, 40)
    wb.save(path)
    PP.normalize_zip(path, modified="2026-10-14T16:31:40Z")


def months_csv(S, path):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\r\n")
    w.writerow(["place_code", "place", "month_of_death", "deaths"])
    for p in W.NAMES:
        for m, label in ((6, "2026-06"), (7, "2026-07"), (8, "2026-08")):
            w.writerow([W.CODE[p], p, label, S["months"][(p, m)]])
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(buf.getvalue())


def write(S, golden_dir):
    os.makedirs(golden_dir, exist_ok=True)
    workbook(S, os.path.join(golden_dir, XLSX))
    months_csv(S, os.path.join(golden_dir, CSV))
