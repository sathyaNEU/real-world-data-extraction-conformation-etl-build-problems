"""Files a credit risk team keeps that look relevant to the allowance and do not set it: the collections roll-rate
report (computed from the book's month-end arrears positions)."""
import datetime as dt

import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill

import officex as OX


def roll_rates_xlsx(path, rolls):
    """collections MI: month-end roll rates between arrears buckets, FY26"""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Roll rates FY26"
    ws.append(["Personal loans: arrears roll rates, month end, FY26 (July 2025 to June 2026)"])
    ws["A1"].font = Font(bold=True, size=12)
    ws.append(["Share of loans in the first bucket at the previous month end that are in the second bucket at this month end, "
               "by count. Loans repaid or written off in the month count as not rolled."])
    ws["A2"].font = Font(italic=True, color="5B6670")
    ws.append([])
    hdr = ["Month end", "Current to 1-29", "1-29 to 30-59", "30-59 to 60-89", "60-89 to 90+", "Cure rate 1-29"]
    ws.append(hdr)
    for j in range(1, len(hdr) + 1):
        c = ws.cell(row=4, column=j)
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="E5E9F0")
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for d, a, b, c, e, cure in rolls:
        ws.append([d, round(a, 4), round(b, 4), round(c, 4), round(e, 4), round(cure, 4)])
    for r in range(5, 5 + len(rolls)):
        ws.cell(row=r, column=1).number_format = "mmm-yy"
        for col in range(2, 7):
            ws.cell(row=r, column=col).number_format = "0.0%"
    for col, w in zip("ABCDEF", [11, 12, 12, 12, 12, 12]):
        ws.column_dimensions[col].width = w
    ws.row_dimensions[4].height = 30
    ws.freeze_panes = "A5"
    OX.xlsx_from_openpyxl(wb, path, "Natalie Hanna", "Natalie Hanna", dt.datetime(2026, 7, 13, 14, 20, 41),
                          dt.datetime(2026, 7, 14, 9, 50, 12), seed=714)
