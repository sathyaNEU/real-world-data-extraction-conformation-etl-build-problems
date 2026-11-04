"""The pack's workbooks: the terminal management system's export from the 29 June go-live, the tanker register, the
tank register and the ships' outturns, each laid out the way its system or its owner keeps it."""
import datetime as dt

import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

import world as W

HEAD = Font(name="Calibri", bold=True, size=11)
TITLE = Font(name="Calibri", bold=True, size=13)
GREY = PatternFill("solid", fgColor="D9D9D9")


def _widths(ws, widths):
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w


def write_tms(path, cols, rows):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Transactions"
    ws["A1"] = "Warrenby Terminal  |  Terminal Management System"
    ws["A1"].font = TITLE
    ws["A2"] = "Transaction export, loaded 29/06/2026 06:00 to 04/01/2027 06:00 (terminal local time)"
    ws["A3"] = "Run 04/01/2027 07:12 by agardner"
    for j, c in enumerate(cols, start=1):
        cell = ws.cell(row=5, column=j, value=c)
        cell.font = HEAD
        cell.fill = GREY
    for i, r in enumerate(rows, start=6):
        for j, v in enumerate(r, start=1):
            ws.cell(row=i, column=j, value=v if v != "" else None)
    _widths(ws, [14, 20, 6, 6, 9, 9, 12, 12, 11, 8, 15, 11, 10])
    ws.freeze_panes = "A6"
    wb.save(path)
    return len(rows)


def write_tankers(path, x, plate_hist):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Units"
    cols = ["Fleet unit", "Operator", "Configuration", "TMS tanker ID", "Lead trailer rego", "Dog trailer rego",
            "Lead compartments (L)", "Dog compartments (L)", "TMS compartment numbers", "Previous regos", "Notes"]
    for j, c in enumerate(cols, start=1):
        cell = ws.cell(row=1, column=j, value=c)
        cell.font = HEAD
        cell.fill = GREY
        cell.alignment = Alignment(wrap_text=True, vertical="top")
    r = 2
    for u in x["units"]:
        lead = plate_hist[(u.uid, "lead")][-1][1]
        dog = plate_hist[(u.uid, "dog")][-1][1] if u.config == "B-double" else ""
        prev = []
        for tr in ("lead", "dog"):
            h = plate_hist.get((u.uid, tr))
            if h and len(h) > 1:
                prev.append("%s %s until %s" % (tr, h[0][1], (h[1][0] - dt.timedelta(days=1)).strftime("%d/%m/%Y")))
        lc = ", ".join(str(c) for c in u.cap[:5] if True)[:200] if u.config == "B-double" else ", ".join(str(c) for c in u.cap)
        dc = ", ".join(str(c) for c in u.cap[5:]) if u.config == "B-double" else ""
        nums = "1-5 lead, 6-9 dog" if u.config == "B-double" else "1-%d" % u.comps
        note = "Oakhurst Haulage, contract carrier (diesel)" if u.operator == "OAK" else ""
        vals = [u.uid, "Brennock Fuels" if u.operator == "BRN" else "Oakhurst Haulage", u.config, u.tas_id, lead, dog,
                lc, dc, nums, "; ".join(prev), note]
        for j, v in enumerate(vals, start=1):
            ws.cell(row=r, column=j, value=v if v != "" else None)
        r += 1
    _widths(ws, [10, 17, 13, 13, 15, 15, 34, 26, 18, 30, 34])
    ws.freeze_panes = "A2"
    wb.save(path)


def write_tank_register(path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Tanks"
    cols = ["Tank", "Service", "Roof", "Rim seal", "Vents", "Diameter (m)", "Shell height (m)",
            "Nominal capacity (kL)", "Safe fill (kL)", "Heel (kL)", "Year built", "Last internal inspection"]
    insp = {"TK-1": "2019-03", "TK-2": "2021-08", "TK-3": "2023-05", "TK-4": "2020-10", "TK-5": "2022-02"}
    heights = {"TK-1": 15.2, "TK-2": 14.6, "TK-3": 14.9, "TK-4": 16.0, "TK-5": 16.0}
    for j, c in enumerate(cols, start=1):
        cell = ws.cell(row=1, column=j, value=c)
        cell.font = HEAD
        cell.fill = GREY
        cell.alignment = Alignment(wrap_text=True, vertical="top")
    for i, (tk, t) in enumerate(W.TANKS.items(), start=2):
        vents = "Pressure-vacuum vents" if t["roof"].startswith("Fixed") else "Shell and centre roof vents"
        vals = [tk, W.NAME_LONG[t["product"]], t["roof"], t["seal"], vents, t["diameter_m"], heights[tk],
                t["capacity_kl"], int(round(t["capacity_kl"] * 0.95, -1)), t["heel_kl"], t["built"], insp[tk]]
        for j, v in enumerate(vals, start=1):
            ws.cell(row=i, column=j, value=v)
    ws.cell(row=8, column=1, value="Register as at 08/01/2027. Capacities from the 2019 to 2023 strapping tables.")
    _widths(ws, [8, 22, 22, 44, 26, 12, 14, 18, 13, 10, 10, 20])
    wb.save(path)


def write_outturns(path, cols, rows):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Outturns 2026"
    for j, c in enumerate(cols, start=1):
        cell = ws.cell(row=1, column=j, value=c)
        cell.font = HEAD
        cell.fill = GREY
    for i, r in enumerate(rows, start=2):
        for j, v in enumerate(r, start=1):
            cell = ws.cell(row=i, column=j, value=v)
            if isinstance(v, dt.datetime):
                cell.number_format = "dd/mm/yyyy hh:mm"
            elif isinstance(v, dt.date):
                cell.number_format = "dd/mm/yyyy"
            elif isinstance(v, int):
                cell.number_format = "#,##0"
    _widths(ws, [8, 18, 12, 11, 22, 10, 17, 17, 13, 15, 16, 12, 26])
    ws.freeze_panes = "A2"
    wb.save(path)
