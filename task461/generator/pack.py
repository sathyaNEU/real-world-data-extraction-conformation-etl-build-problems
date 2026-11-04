"""Write each system's record of the simulated year: the supplier's half-hourly import, the BMS registers, the meter
register and tenancy schedule, the generator's dips, dockets, calibration and controller events, the F-gas log, the
refrigerant contractor's recovery record and the weather."""
import csv
import datetime as dt

import numpy as np
import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill

import sim as S
import world as W

D = dt.timedelta
HEAD = Font(name="Calibri", bold=True)
GREY = PatternFill("solid", fgColor="D9DEE3")


def dmy(iso):
    return "%s/%s/%s" % (iso[8:10], iso[5:7], iso[:4])


def write_csv(path, cols, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\r\n")
        w.writerow(cols)
        w.writerows(rows)
    return len(rows)


def _sheet(ws, cols, rows, widths, fmt=None):
    for j, c in enumerate(cols, start=1):
        cell = ws.cell(row=1, column=j, value=c)
        cell.font = HEAD
        cell.fill = GREY
        cell.alignment = Alignment(wrap_text=True, vertical="top")
    for i, r in enumerate(rows, start=2):
        for j, v in enumerate(r, start=1):
            cell = ws.cell(row=i, column=j, value=None if v == "" else v)
            if fmt and fmt.get(j):
                cell.number_format = fmt[j]
    for j, w in enumerate(widths, start=1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(j)].width = w
    ws.freeze_panes = "A2"


# ---------------------------------------------------------------------------------- the supplier's half-hourly data
def hh_rows(x):
    rows, by_day = [], {}
    for t, l, e in zip(x["ts"], x["loc"], x["imp"]):
        if l.year == 2026:
            by_day.setdefault(l.date(), []).append(e * 0.5)
    for day in sorted(by_day):
        for p, kwh in enumerate(by_day[day], start=1):
            rows.append([W.MPAN, day.strftime("%d/%m/%Y"), p, "%.1f" % kwh, "A"])
    return rows


# ---------------------------------------------------------------------------------- the BMS registers
def bms_rows(x, rng):
    ts, loc = x["ts"], x["loc"]
    start = W.local_to_utc(dt.datetime(2025, 12, 31))
    end = W.local_to_utc(dt.datetime(2027, 1, 2))
    i0 = ts.index(start)
    i1 = ts.index(end)
    swap_utc = W.local_to_utc(W.REPLACED[2])
    rows = []
    regs = {}
    for tag, desc, occ, kind, parent in W.METERS:
        if tag == "EM-118":
            continue
        series = x["kw"][tag] * 0.5 * (1 + float(rng.normal(0, 0.0018)))
        cum = np.concatenate([[0.0], np.cumsum(series)])          # register at the start of each half-hour
        regs[tag] = float(rng.uniform(40_000, 900_000)) + cum
    for i in range(i0, i1 + 1):
        t, l = ts[i], loc[i]
        if W.BMS_GAP[0] <= l < W.BMS_GAP[1]:
            continue
        stamp = l.strftime("%d/%m/%Y %H:%M")
        for tag, desc, occ, kind, parent in W.METERS:
            if tag == "EM-118":
                if t < swap_utc:
                    continue
                v = regs["EM-110"][i] - regs["EM-110"][ts.index(swap_utc)]
            elif tag == "EM-110" and t > swap_utc:
                continue
            else:
                v = regs[tag][i]
            if tag in W.WH_METERS:
                rows.append((t, [stamp, tag, "%d" % round(v * 1000), "Wh"]))
            else:
                rows.append((t, [stamp, tag, "%.1f" % v, "kWh"]))
    return [r for _, r in rows]


# ---------------------------------------------------------------------------------- registers and schedules
def write_register(path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Meters"
    loc = {"EM-101": "L2 east riser", "EM-102": "L2 east riser", "EM-103": "L3 east riser", "EM-104": "L5 east riser",
           "EM-105": "L5 east riser", "EM-106": "L7 east riser", "EM-107": "L9 east riser", "EM-108": "L9 east riser",
           "EM-109": "L10 east riser", "EM-110": "L12 east riser", "EM-112": "L13 east riser",
           "EM-114": "Roof plant room", "EM-118": "L12 east riser", "EM-201": "Basement switch room",
           "EM-202": "Lift motor room", "EM-203": "Basement switch room", "EM-204": "Car park plant room"}
    ct = {"EM-101": "300/5", "EM-104": "400/5", "EM-107": "300/5", "EM-110": "300/5", "EM-118": "300/5",
          "EM-201": "600/5", "EM-106": "200/5"}
    inst = {"EM-110": "2014-03-11", "EM-118": "2026-08-18", "EM-103": "2009-06-02", "EM-204": "2009-06-02",
            "EM-102": "2019-11-26", "EM-105": "2021-02-15", "EM-108": "2018-07-09", "EM-114": "2017-04-24"}
    rows = []
    for tag, desc, occ, kind, parent in W.METERS:
        recharge = "Yes" if kind in ("supply", "room") else "No"
        note = ""
        if tag == "EM-110":
            note = "Removed 18/08/2026, replaced by EM-118"
        elif tag == "EM-118":
            note = "Replaces EM-110"
        rows.append([tag, desc, occ, loc[tag], ct.get(tag, "Whole current"), "Wh" if tag in W.WH_METERS else "kWh",
                     dmy(inst.get(tag, "2012-05-14")), recharge, note])
    _sheet(ws, ["Meter", "Description", "Occupier", "Location", "CT ratio", "Register units", "Installed",
                "Recharged to occupier", "Notes"], rows, [9, 34, 31, 21, 13, 10, 11, 12, 36])
    ws.cell(row=len(rows) + 3, column=1, value="BMS energy meters, Pellow House. Register as at 05/01/2027.")
    wb.save(path)


def write_tenancy(path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Tenancy schedule"
    leases = {"Ostrand Legal LLP": ("2019-09-01", "2029-08-31"), "Fenmore Studio Architects Ltd": ("2021-04-01", "2026-12-31"),
              "Varnhold Insurance Services Ltd": ("2020-11-01", "2030-10-31"), "Orrin Health Clinics Ltd": ("2022-06-01", "2027-05-31"),
              "Tamsett Analytics Ltd": ("2018-05-14", "2028-05-13"), "Selcourt Capital LLP": ("2023-01-09", "2028-01-08"),
              "Mordaunt Partners LLP": ("2014-03-25", "2027-03-24"), "Brindle & Moss Ltd": ("2024-07-01", "2029-06-30")}
    rows = [["Ground floor suite", "Vacant", "G", W.VACANT_M2, "", "", "Marketed"]]
    for name, t in W.TENANTS.items():
        a, b = leases[name]
        rows.append(["Level %s" % t["floors"], name, t["floors"], t["nla"], dmy(a), dmy(b), "Lease"])
    rows.append(["Roof", W.CARRIER, "Roof", 0, "24/04/2017", "23/04/2032", "Licence (equipment room and masts)"])
    _sheet(ws, ["Premises", "Occupier", "Floors", "NLA (m2)", "Term start", "Term end", "Basis"], rows,
           [20, 32, 9, 10, 11, 11, 32], fmt={4: "#,##0"})
    ws.cell(row=len(rows) + 3, column=1, value="Schedule at 31/12/2026, areas per the 2019 measured survey (NLA).")
    wb.save(path)


# ---------------------------------------------------------------------------------- the generator's records
def dip_rows(x, rng):
    out = []
    for d in x["gen"]["dips"]:
        mm = S.tank_mm(d["litres"]) + float(rng.normal(0, 0.5))
        out.append([d["at"].strftime("%d/%m/%Y"), d["at"].strftime("%H:%M"), "DT-1", int(round(mm)), 0])
    return out


def calib_rows():
    return [[mm, int(round(S.tank_litres(mm)))] for mm in range(0, W.TANK_DIAMETER_MM + 1)]


def write_calib(path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "DT-1"
    rows = calib_rows()
    _sheet(ws, ["Dip (mm)", "Contents (litres)"], rows, [10, 16], fmt={2: "#,##0"})
    ws.cell(row=len(rows) + 3, column=1, value="Day tank DT-1, horizontal cylindrical, 1250 mm dia x 2100 mm. "
                                                 "Calibration chart issued with the tank, 2011.")
    wb.save(path)


def docket_rows(x, rng):
    out, n = [], 51840
    for dlv in x["gen"]["deliveries"]:
        parts = [dlv["litres"]]
        if dlv["litres"] >= 900 and rng.random() < 0.6:
            a = float(int(dlv["litres"] * float(rng.uniform(0.45, 0.6)) / 50) * 50)
            parts = [a, dlv["litres"] - a]
        for p in parts:
            n += int(rng.integers(7, 40))
            out.append(["NLF%06d" % n, dlv["at"].strftime("%d/%m/%Y"), dlv["at"].strftime("%H:%M"), "Gas oil",
                        "%d" % p, "DT-1", "Northline Fuels"])
    return out


def event_rows(x, rng):
    rows, hours = [], 1873.4
    for r in x["gen"]["runs"]:
        hours += 0.0
        mode = r["kind"]
        start = [r["start"], "ENGINE START", mode, "%.1f" % hours]
        if mode == "Mains failure":
            rows.append((r["start"] - D(seconds=7), [r["start"] - D(seconds=7), "MAINS FAIL", "", "%.1f" % hours]))
        rows.append((r["start"], start))
        if mode != "Off-load test":
            rows.append((r["start"] + D(seconds=21), [r["start"] + D(seconds=21), "LOAD ON", mode, "%.1f" % hours]))
        hours += r["minutes"] / 60.0
        if mode == "Mains failure":
            rows.append((r["end"] - D(seconds=40), [r["end"] - D(seconds=40), "MAINS RESTORED", "", "%.1f" % hours]))
        if mode != "Off-load test":
            rows.append((r["end"] - D(seconds=30), [r["end"] - D(seconds=30), "LOAD OFF", mode, "%.1f" % hours]))
        rows.append((r["end"], [r["end"], "ENGINE STOP", mode, "%.1f" % hours]))
    for d in (dt.datetime(2026, 3, 19, 3, 12), dt.datetime(2026, 8, 7, 22, 41), dt.datetime(2026, 12, 2, 5, 3)):
        rows.append((d, [d, "BATTERY CHARGER FAULT", "", ""]))
        rows.append((d + D(minutes=26), [d + D(minutes=26), "BATTERY CHARGER FAULT CLEARED", "", ""]))
    rows.sort(key=lambda r: r[0])
    return [[r[1][0].strftime("%d/%m/%Y %H:%M:%S")] + r[1][1:] for r in rows]


# ---------------------------------------------------------------------------------- refrigerant
def fgas_rows(x):
    out = []
    jobs = {}
    n = 4410
    for r in x["fgas"]:
        if r["activity"] == "Recovery":
            continue
        if r["activity"] == "Recharge":
            key = (r["plant"], "retube")
            act = "Recharge after condenser re-tube"
        elif r["activity"] == "Top-up":
            key = (r["plant"], r["at"])
            act = "Leak located and repaired, top-up"
        else:
            key = (r["plant"], r["at"])
            act = "Leak check (electronic detector), no leak found"
        if key not in jobs:
            n += 7
            jobs[key] = "CB-26-%04d" % n
        out.append([r["at"].strftime("%d/%m/%Y"), r["plant"], "R-134a", "%.1f" % W.CHILLERS[r["plant"]]["charge"],
                    act, "%.1f" % r["kg"] if r["kg"] else "", jobs[key], "Calbrook"])
    return out, jobs


def write_recovery(path, x, jobs):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Recovery 2026"
    rows = []
    cyl = 7712
    for r in x["fgas"]:
        if r["activity"] != "Recovery":
            continue
        c = W.CHILLERS[r["plant"]]
        for kg in r["cylinders"]:
            cyl += 3
            rows.append([jobs[(r["plant"], "retube")], r["at"].date(), "Pellow House, Wexmoor", c["code"], "R-134a",
                         "RC%05d" % cyl, kg, "Returned for reclamation"])
    _sheet(ws, ["Job", "Date", "Site", "Plant ref", "Refrigerant", "Cylinder", "Recovered (kg)", "Destination"],
           rows, [12, 11, 22, 9, 11, 10, 13, 24], fmt={2: "dd/mm/yyyy", 7: "0.0"})
    wb.save(path)


def weather_rows(x):
    return [[d.strftime("%Y-%m-%d"), "%.1f" % v["tmax"], "%.1f" % v["tmin"], "%.1f" % v["rain"]]
            for d, v in sorted(x["wx"].items()) if d.year == 2026]
