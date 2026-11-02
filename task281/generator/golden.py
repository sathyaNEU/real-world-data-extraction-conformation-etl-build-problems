"""The golden deliverables: the credit file for Finance and the workbook for Internal Audit and the Court."""
import csv
import datetime as dt
import io
import math
import os

import openpyxl
from openpyxl.chart import BarChart, Reference
from openpyxl.chart.label import DataLabelList
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

import analysis as AN
import io_util as IO

FAC_NAME = {v: k for k, v in AN.FAC_NAME.items()}
FUND_CODE = {f: "CT-" + f for f in AN.FAC_ORDER}


def r100(x):
    return int(math.floor(x / 100.0 + 0.5)) * 100


def frame(target):
    """every figure the deliverables and the write-up carry, from the bundle alone"""
    g = AN.main_call(target, "golden")
    F = dict(rows=[], spend={}, uncovered={}, metered={})
    for f in AN.FAC_ORDER:
        F["rows"].append(dict(fac=f, name=FAC_NAME[f], code=FUND_CODE[f], holds=g["n"][f], hw=g["hw"][f],
                              hw100=r100(g["hw"][f]), amount=g["amount"][f], amount100=r100(g["amount"][f])))
    F["holds_total"] = sum(r["holds"] for r in F["rows"])
    F["hw_total"] = g["total_hw"]
    F["hw_total100"] = r100(g["total_hw"])
    F["amount_total100"] = sum(r["amount100"] for r in F["rows"])
    a, b, c = AN.ask_a(target), AN.ask_b(target), AN.ask_c(target)
    for f in AN.FAC_ORDER:
        F["spend"][f] = dict(exact=a[f], r100=r100(a[f]))
        F["uncovered"][f] = b[f]
        F["metered"][f] = c[f]
    F["spend_total100"] = r100(sum(a.values()))
    F["uncovered_total"] = sum(b.values())
    F["metered_total"] = sum(c.values())
    # facts the write-up states about the population and the default route
    d = AN.load(target)
    W = AN.waits(d, "golden")
    F["n_cancelled"] = sum(1 for r in W if r[5]["status"].startswith("Cancelled"))
    F["n_offered"] = sum(1 for r in W if r[5]["offered"] is not None)
    km = AN.main_call(target, "km_fac")
    F["km_amount100"] = {f: r100(km["amount"][f]) for f in AN.FAC_ORDER}
    return F


def write_csv(F, path):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\r\n")
    w.writerow(["fund_code", "faculty", "amount_gbp"])
    for r in F["rows"]:
        w.writerow([r["code"], r["name"], r["amount100"]])
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(buf.getvalue())


THIN = Side(style="thin", color="A6A6A6")
HEAD_FILL = PatternFill("solid", fgColor="DDE4EE")


def _head(ws, row, values, widths=None):
    for j, v in enumerate(values, 1):
        c = ws.cell(row=row, column=j, value=v)
        c.font = Font(bold=True)
        c.fill = HEAD_FILL
        c.alignment = Alignment(wrap_text=True, vertical="top")
        c.border = Border(bottom=THIN)
    if widths:
        for j, wd in enumerate(widths, 1):
            ws.column_dimensions[openpyxl.utils.get_column_letter(j)].width = wd


def write_xlsx(F, path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Division"
    ws["A1"] = "Course Texts Fund 2027: division among faculties (Court paper UC/26/114)"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = "Holds placed by students 12 January to 26 April 2026 (UK time); Shelfmark Lend extract of 31 October 2026."
    ws["A2"].font = Font(italic=True, size=9)
    _head(ws, 4, ["Faculty", "2026-27 fund code", "Holds counted", "Hold-weeks", "Amount (GBP)"], [30, 18, 15, 14, 15])
    r0 = 5
    for i, r in enumerate(F["rows"]):
        ws.cell(row=r0 + i, column=1, value=r["name"])
        ws.cell(row=r0 + i, column=2, value=r["code"])
        ws.cell(row=r0 + i, column=3, value=r["holds"]).number_format = "#,##0"
        ws.cell(row=r0 + i, column=4, value=r["hw100"]).number_format = "#,##0"
        ws.cell(row=r0 + i, column=5, value=r["amount100"]).number_format = "#,##0"
    rt = r0 + len(F["rows"])
    ws.cell(row=rt, column=1, value="All faculties").font = Font(bold=True)
    ws.cell(row=rt, column=3, value=F["holds_total"]).number_format = "#,##0"
    ws.cell(row=rt, column=4, value=F["hw_total100"]).number_format = "#,##0"
    ws.cell(row=rt, column=5, value=F["amount_total100"]).number_format = "#,##0"
    for j in range(1, 6):
        ws.cell(row=rt, column=j).border = Border(top=THIN)
        ws.cell(row=rt, column=j).font = Font(bold=True)
    ws.cell(row=rt + 2, column=1, value="Hold-weeks and amounts rounded to the nearest 100; amounts are each faculty's "
                                         "share of the hold-weeks applied to GBP 180,000.").font = Font(size=9)
    ch = BarChart()
    ch.type = "bar"
    ch.style = 10
    ch.title = "Course Texts Fund 2027 by faculty (GBP)"
    ch.y_axis.title = "GBP"
    ch.y_axis.numFmt = "#,##0"
    ch.y_axis.majorGridlines = None
    data = Reference(ws, min_col=5, min_row=4, max_row=rt - 1)
    cats = Reference(ws, min_col=1, min_row=5, max_row=rt - 1)
    ch.add_data(data, titles_from_data=True)
    ch.set_categories(cats)
    ch.legend = None
    ch.dataLabels = DataLabelList()
    ch.dataLabels.showVal = True
    ch.height = 9
    ch.width = 17
    ws.add_chart(ch, "G4")

    ws = wb.create_sheet("Spend Jan-Oct 2026")
    ws["A1"] = "Course text spend by faculty, invoice lines dated 1 January to 31 October 2026 (GBP)"
    ws["A1"].font = Font(bold=True)
    _head(ws, 3, ["Faculty", "Spend (GBP)"], [30, 14])
    for i, f in enumerate(AN.FAC_ORDER):
        ws.cell(row=4 + i, column=1, value=FAC_NAME[f])
        ws.cell(row=4 + i, column=2, value=F["spend"][f]["r100"]).number_format = "#,##0"
    ws.cell(row=13, column=1, value="Includes each faculty's share of the 2026 publisher packages charged to CT-CORE; "
                                    "euro and dollar lines at the Finance Office monthly rate.").font = Font(size=9)

    ws = wb.create_sheet("Spring 2026 lists")
    ws["A1"] = "Essential spring 2026 reading-list items the Library could not lend as an e-book on 12 January 2026"
    ws["A1"].font = Font(bold=True)
    _head(ws, 3, ["Faculty", "Items"], [30, 10])
    for i, f in enumerate(AN.FAC_ORDER):
        ws.cell(row=4 + i, column=1, value=FAC_NAME[f])
        ws.cell(row=4 + i, column=2, value=F["uncovered"][f])

    ws = wb.create_sheet("40-loan licences")
    ws["A1"] = "40-loan licences in force at the end of 30 October 2026 with ten or fewer loans left, by fund"
    ws["A1"].font = Font(bold=True)
    _head(ws, 3, ["Faculty", "Licences"], [30, 10])
    for i, f in enumerate(AN.FAC_ORDER):
        ws.cell(row=4 + i, column=1, value=FAC_NAME[f])
        ws.cell(row=4 + i, column=2, value=F["metered"][f])

    wb.properties.creator = "Collections and Content, Ardmuir University Library"
    wb.properties.lastModifiedBy = "Collections and Content, Ardmuir University Library"
    wb.properties.created = dt.datetime(2026, 11, 2, 10, 0, 0)
    wb.properties.modified = dt.datetime(2026, 11, 2, 10, 0, 0)
    wb.properties.title = "Course Texts Fund 2027"
    wb.save(path)
    IO.fix_zip(path)


def write_all(target, golden_dir):
    os.makedirs(golden_dir, exist_ok=True)
    F = frame(target)
    write_csv(F, os.path.join(golden_dir, "course_texts_fund_2027.csv"))
    write_xlsx(F, os.path.join(golden_dir, "course_texts_fund_2027.xlsx"))
    for fn in os.listdir(golden_dir):
        IO.set_mtime(os.path.join(golden_dir, fn))
    return F
