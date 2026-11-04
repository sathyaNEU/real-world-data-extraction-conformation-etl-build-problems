"""The registers and the operations records: the wastewater asset register (stations, pumps, flow meters), the
consents register, the storm overflow improvement plan, the observation borehole's daily levels and the year's
work orders. Each is in its own system's conventions: the asset register holds levels in mAOD, wet wells as
their internal dimensions and each pump's duty in the unit its datasheet quoted; the consents register quotes
each permit's condition in the permit's words."""
import datetime as dt
import os

import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

import pack
import sim
import world as W

HEAD = PatternFill("solid", fgColor="D9E1F2")
BOLD = Font(bold=True)


def _sheet(ws, header, rows, widths, fmts=None):
    ws.append(header)
    for c in range(1, len(header) + 1):
        ws.cell(row=1, column=c).font = BOLD
        ws.cell(row=1, column=c).fill = HEAD
        ws.cell(row=1, column=c).alignment = Alignment(vertical="top", wrap_text=True)
    for r in rows:
        ws.append(list(r))
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w
    if fmts:
        for col, f in fmts.items():
            for rr in range(2, len(rows) + 2):
                ws.cell(row=rr, column=col).number_format = f
    ws.freeze_panes = "B2"


def _ngr(rng, k):
    e = 520000 + int(rng.integers(0, 40000))
    n = 360000 + int(rng.integers(0, 50000))
    return "TF %05d %05d" % (e % 100000, n % 100000)


def assets(tgt, S):
    wb = Workbook()
    ws = wb.active
    ws.title = "Pumping stations"
    rows = []
    for k, st in enumerate(W.STATIONS):
        rng = np.random.default_rng([W.SEED, 21, k])
        well = st["well"]
        dims = ("%.1f dia" % well[1]) if well[0] == "circular" else ("%.1f x %.1f" % (well[1], well[2]))
        inst = (W.EDM_REPLACED[st["code"]][1] if st["code"] in W.EDM_REPLACED
                else W.aq7_commissioned(W.EDM_CURRENT[st["code"]]))
        hla = st["start"] + 0.55 * (st["weir"] - st["start"])
        rm_d = int(rng.choice([150, 200, 225, 250, 300] if st["rated"] > 40 else [100, 125, 150]))
        rows.append((st["code"], st["name"] + " Pumping Station", _ngr(rng, k), "MW-" + st["zone"], st["rtu"],
                     W.EDM_CURRENT[st["code"]], inst, "Circular" if well[0] == "circular" else "Rectangular", dims,
                     round(st["floor"], 2), round(st["floor"] + st["start"], 2), round(st["floor"] + st["stop"], 2),
                     round(st["floor"] + hla, 2), round(st["floor"] + st["weir"], 2), "2 (duty/standby, alternating)",
                     "%d mm %s, %d m" % (rm_d, rng.choice(["DI", "PE100", "uPVC"]), int(rng.integers(380, 4200))),
                     W.WRC if k % 3 else "Gravity sewer to " + W.WRC))
    _sheet(ws, ["Station code", "Station name", "NGR", "Radar zone", "Telemetry RTU", "EDM monitor", "EDM installed",
                "Wet well shape", "Wet well internal (m)", "Wet well floor (mAOD)", "Duty pump start (mAOD)",
                "Duty pump stop (mAOD)", "High level alarm (mAOD)", "Overflow weir (mAOD)", "Pumps",
                "Rising main", "Discharges to"], rows,
           [11, 30, 16, 9, 11, 15, 12, 12, 13, 11, 11, 11, 11, 11, 24, 24, 26],
           {7: "dd/mm/yyyy", 10: "0.00", 11: "0.00", 12: "0.00", 13: "0.00", 14: "0.00"})
    ws2 = wb.create_sheet("Pumps")
    prow = []
    for k, st in enumerate(W.STATIONS):
        rng = np.random.default_rng([W.SEED, 22, k])
        for p in (1, 2):
            duty = st["rated"] if st["unit"] == "l/s" else round(st["rated"] * 3.6, 1)
            inst = dt.date(2008 + int(rng.integers(0, 15)), int(rng.integers(1, 13)), int(rng.integers(1, 28)))
            rng.integers(2, 11), rng.integers(1, 28)
            svc = S["stations"][st["code"]]["pump_service"]
            prow.append((st["code"], p, st["model"], duty, st["unit"], st["head"], inst, svc))
    _sheet(ws2, ["Station code", "Pump", "Manufacturer and model", "Duty flow", "Duty flow unit", "Duty head (m)",
                 "Installed", "Last service"], prow, [11, 6, 26, 10, 12, 12, 12, 12],
           {4: "0.0", 6: "0.0", 7: "dd/mm/yyyy", 8: "dd/mm/yyyy"})
    ws3 = wb.create_sheet("Flow meters")
    mrow = []
    for k, st in enumerate(W.STATIONS):
        if st["meter"]:
            rng = np.random.default_rng([W.SEED, 23, k])
            mrow.append((st["code"], st["meter"], "Electromagnetic, rising main", dt.date(2019 + int(rng.integers(0, 4)),
                         int(rng.integers(1, 13)), 15), S["stations"][st["code"]]["meter_verified"]))
    _sheet(ws3, ["Station code", "Meter tag", "Type", "Installed", "Last verified"], mrow, [11, 12, 28, 12, 12],
           {4: "dd/mm/yyyy", 5: "dd/mm/yyyy"})
    path = os.path.join(tgt, pack.FILES["assets"])
    pack.ensure(path)
    wb.save(path)


def consents(tgt):
    rows = []
    for k, st in enumerate(W.STATIONS):
        rng = np.random.default_rng([W.SEED, 31, k])
        issued = dt.date(2009 + int(rng.integers(0, 6)), int(rng.integers(1, 13)), int(rng.integers(1, 28)))
        varied = dt.date(2021 + int(rng.integers(0, 3)), int(rng.integers(1, 13)), int(rng.integers(1, 28)))
        text = ("The discharge from the storm overflow shall only occur when the pumping station is passing forward "
                "to the rising main a flow of not less than %d litres per second." % st["pff"])
        rows.append((W.PERMIT[st["code"]], st["name"] + " PS storm overflow", "WW-SO-" + st["code"][3:],
                     W.RECEIVING[st["code"]], "Storm overflow, pumping station", "2.3.1", text, st["pff"], "Yes",
                     issued.isoformat(), varied.isoformat()))
    pack.write_csv(os.path.join(tgt, pack.FILES["consents"]),
                   ["permit_ref", "discharge_name", "site_id", "receiving_water", "discharge_type", "condition_ref",
                    "condition_text", "pass_forward_ls", "edm_required", "issued", "last_varied"], rows)


def plan(tgt):
    wb = Workbook()
    ws = wb.active
    ws.title = "Schemes"
    rows = []
    schemes = {"SPS0419": ("Storage, 450 m3 online tank", "Spill frequency", 10, "AMP8 year 3", "Design"),
               "SPS0415": ("Infiltration reduction, sewer relining 1.2 km", "Groundwater", 10, "AMP8 year 2",
                           "Investigation"),
               "SPS0449": ("Screen upgrade, 6 mm two-dimensional", "Aesthetics", None, "AMP8 year 1", "Complete"),
               "SPS0428": ("Storage, 1,100 m3 offline tank", "Ecology (WFD)", 20, "AMP8 year 4", "Feasibility"),
               "SPS0433": ("Screen upgrade, 6 mm two-dimensional", "Aesthetics", None, "AMP8 year 2", "Construction"),
               "SPS0407": ("Monitoring only", "Spill frequency", 20, "AMP8", "Monitoring")}
    for st in W.STATIONS:
        if st["code"] in schemes:
            s = schemes[st["code"]]
            rows.append((W.PERMIT[st["code"]], st["name"] + " PS storm overflow", s[0], s[1], s[2], s[3], s[4]))
    _sheet(ws, ["Permit", "Overflow", "Scheme", "Driver", "Target spills (annual, 12/24)", "Delivery", "Status"], rows,
           [14, 32, 40, 18, 14, 14, 14])
    path = os.path.join(tgt, pack.FILES["plan"])
    pack.ensure(path)
    wb.save(path)


def borehole(tgt, S):
    rng = np.random.default_rng([W.SEED, 41])
    rows = []
    level = 21.4
    for d in range(365):
        day = dt.date(2026, 1, 1) + dt.timedelta(days=d)
        rain = float(S["rain"][3, d * 1440:(d + 1) * 1440].sum())
        seasonal = 0.040 * np.cos(2 * np.pi * (d - 44) / 365)
        level += seasonal + 0.006 * rain - 0.012 + rng.normal(0, 0.006)
        rows.append(("HAGWORTH WOLD OBH", day.isoformat(), "%.2f" % level))
    pack.write_csv(os.path.join(tgt, pack.FILES["borehole"]), ["station", "date", "groundwater_level_maod"], rows)


def workorders(tgt, S):
    """The completed work orders, one per crew visit (the visit that opened the kiosk door), and one for each kiosk
    door alarm a crew went out to secure."""
    rng = np.random.default_rng([W.SEED, 51])
    jobs = []
    for st in W.STATIONS:
        r = S["stations"][st["code"]]
        jobs += [(v["arr"], st, v["task"], v["outcome"]) for v in r["visits"]]
        jobs += [(b, st, "Kiosk door alarm", "Door secured, no sign of entry") for a, b in r["door"]]
    jobs.sort(key=lambda x: x[0])
    rows = []
    wo = 4127310                                     # the company's work order sequence runs across every area
    for t, st, task, outcome in jobs:
        wo += int(rng.integers(30, 420))
        rows.append(("WO%07d" % wo, st["code"], st["name"] + " SPS", pack.local_dt(t).date().isoformat(), task, outcome))
    pack.write_csv(os.path.join(tgt, pack.FILES["workorders"]),
                   ["work_order", "station_code", "site", "completed", "task", "outcome"], rows)


def write(tgt, FILES, S, info):
    assets(tgt, S)
    consents(tgt)
    plan(tgt)
    borehole(tgt, S)
    workorders(tgt, S)
