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


CLOSE = {"Wet well clean and level probe check": "COMPLETE", "Electrical inspection": "COMPLETE",
         "Odour complaint attended": "NFF", "Generator connection point test": "COMPLETE",
         "Pump service (6-monthly)": "COMPLETE", "Flow meter verification": "COMPLETE",
         "High level alarm attended": "ATTENDED", "Kiosk door alarm": "SECURED"}
# what the technician writes: routine phrases recur, a one-off (a part replaced, a fault put right) is used at most
# twice in the year and never twice at one station
NOTES = {
    "Wet well clean and level probe check": (
        ["wet well jetted, probes cleaned and checked against dip", "probes cleaned, reading ok after",
         "tanker on site, well cleaned out, probes wiped", "ultrasonic head cleaned, floats tested ok",
         "light grease on walls jetted down, probes cleaned", "well washed down, both probes cleaned"],
        ["fat build-up cleared off probe, reading checked against dip", "low level float cable re-clipped"]),
    "Electrical inspection": (
        ["panel inspected, RCDs tested, all ok", "fixed wire test done, cert to follow", "thermal image of panel, no hot spots",
         "IR test on pump cables within limits", "inspection done, nothing to report"],
        ["kiosk heater replaced", "loose terminal on outstation supply tightened", "labels renewed on isolators"]),
    "Odour complaint attended": (
        ["no odour at time of visit, lid seals checked", "no smell at station or in street, caller not in",
         "carbon filter and lids checked, nothing found", "no odour found, wet well lids secure"],
        ["slight smell at kiosk vent only, lids reseated"]),
    "Generator connection point test": (
        ["mobile genny connected, changeover tested ok", "changeover switch tested on load, all fine",
         "gen point tested, phase rotation correct", "generator run on load via connection point, ok"],
        []),
    "Pump service (6-monthly)": (
        ["both pumps lifted, oil and seals checked, IR readings ok", "6-monthly service, oil changed both pumps",
         "pumps lifted and hosed down, seals checked, no leaks", "both pumps serviced and returned to auto",
         "service done, both pumps back in auto"],
        ["lifting chain on P2 replaced", "cable glands resealed on P1", "guide rail bracket re-fixed"]),
    "Flow meter verification": (
        ["meter verified against clamp-on, within tolerance", "annual verification, within spec, cert filed",
         "verified with portable meter, within tolerance"],
        []),
    "High level alarm attended": {
        "high": (["level above high level float on arrival, duty pump running, standby available",
                  "high level on arrival, duty on, standby in auto, no faults on panel",
                  "level high, duty running, nothing showing on panel",
                  "high level, both pumps in auto, duty running"], []),
        "normal": (["level normal on arrival, both pumps available, alarm reset",
                    "alarm had cleared before arrival, no faults on panel",
                    "level back to normal, pumps in auto, nothing found",
                    "level normal, high level float tested ok"], [])},
    "Kiosk door alarm": (
        ["no sign of entry, door closed and secured", "door secure on arrival, wind suspected",
         "door switch realigned, alarm cleared", "no entry, door closed, alarm reset", "door shut on arrival, switch tested ok"],
        ["door found ajar, latch adjusted", "door seal replaced, switch reset"]),
}
OPEN = ["On site {t}, ", "{t} ", "", "", "Arrived {t}. "]
CLOSE_NOTE = ["", "", " Left {u}.", " NFA.", " All ok.", " Left site {u}."]
AUTO = {"Wet well clean and level probe check", "Pump service (6-monthly)", "Electrical inspection",
        "Generator connection point test"}


def workorders(tgt, S):
    """The completed work orders, one per crew visit (the visit that opened the kiosk door), and one for each kiosk
    door alarm a crew went out to secure: the closure code the system keeps and the technician's own note."""
    rng = np.random.default_rng([W.SEED, 51])
    rng_n = np.random.default_rng([W.SEED, 52])
    jobs = []
    for st in W.STATIONS:
        r = S["stations"][st["code"]]
        jobs += [(v["arr"], v["dep"], st, v["task"], v["outcome"]) for v in r["visits"]]
        jobs += [(b, b + rng_n.uniform(20, 60) * 60, st, "Kiosk door alarm", "") for a, b in r["door"]]
    jobs.sort(key=lambda x: x[0])
    rows = []
    used, used_at = {}, set()
    wo = 4127310                                     # the company's work order sequence runs across every area
    for t, u, st, task, outcome in jobs:
        wo += int(rng.integers(30, 420))
        pool = NOTES[task]
        if isinstance(pool, dict):
            pool = pool["high" if outcome.startswith("Level high") else "normal"]
        routine, oneoff = pool
        free = [x for x in oneoff if used.get(x, 0) < 2 and (st["code"], x) not in used_at]
        if free and rng_n.random() < 0.25:
            main = free[int(rng_n.integers(0, len(free)))]
            used[main] = used.get(main, 0) + 1
            used_at.add((st["code"], main))
        else:
            main = routine[int(rng_n.integers(0, len(routine)))]
        lt, lu = pack.local_dt(t).strftime("%H:%M"), pack.local_dt(u).strftime("%H:%M")
        ends = CLOSE_NOTE + ([" Back in auto."] if task in AUTO else [])
        if task == "Kiosk door alarm":
            lead = ["", "Attended {t}, ", "{t} "][int(rng_n.integers(0, 3))].format(t=lt)
            tail = ["", "", " NFA."][int(rng_n.integers(0, 3))]
        else:
            lead = OPEN[int(rng_n.integers(0, len(OPEN)))].format(t=lt)
            tail = ends[int(rng_n.integers(0, len(ends)))].format(u=lu)
        # a closing remark never restates the note it closes
        if tail == " All ok." and (" ok" in " " + main or "fine" in main):
            tail = ""
        if tail == " Back in auto." and "auto" in main:
            tail = ""
        body = main[0].upper() + main[1:] if not lead or lead.endswith(". ") else main
        note = lead + body + ("." + tail if tail else "")
        rows.append(("WO%07d" % wo, st["code"], st["name"] + " SPS", pack.local_dt(t).date().isoformat(), task,
                     CLOSE[task], note))
    pack.write_csv(os.path.join(tgt, pack.FILES["workorders"]),
                   ["work_order", "station_code", "site", "completed", "task", "closure_code", "technician_notes"], rows)


def write(tgt, FILES, S, info):
    assets(tgt, S)
    consents(tgt)
    plan(tgt)
    borehole(tgt, S)
    workorders(tgt, S)
