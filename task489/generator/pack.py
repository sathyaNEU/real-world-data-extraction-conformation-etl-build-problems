"""task489: write the pack's data files in the layouts their producing systems export: the SCADA host's plunger
cycle history and dump counters (historian, UTC), production accounting's daily allocations, re-run journal and
run log, the equipment register workbook, the laboratory's gas analyses, the maintenance system's work orders,
and two neighbouring methane records (the optical gas imaging survey, the tank vent measurements)."""
import csv
import datetime as dt

import numpy as np
import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

import sim as S
import world as W

D = dt.timedelta
EXPORT_FROM = dt.datetime(2026, 1, 1, 0, 0, 0)          # the host export: valve opens 2026-01-01 00:00 to 2027-01-01 07:59
EXPORT_TO = dt.datetime(2027, 1, 1, 8, 0, 0)


def write_csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\r\n")
        w.writerow(header)
        for r in rows:
            w.writerow(r)
    return len(rows)


def ts(t):
    return t.strftime("%Y-%m-%d %H:%M:%S")


def f1(x):
    return "%.1f" % (round(x + 0.0, 1) + 0.0)


# --------------------------------------------------------------------------------------------- facility codes
def facility_codes(wd):
    r = S.rng(11)
    codes = {}
    base = 91388
    for s in wd["sites"]:
        base += int(r.integers(41, 977))
        codes[s["code"]] = "ABBT%07d" % base
    return codes


# --------------------------------------------------------------------------------------------- plunger cycles
def cycle_rows(wd):
    rows = []
    for c in wd["cycles"]:
        op = S.local_naive(c["open_utc"])
        if not (EXPORT_FROM <= op < EXPORT_TO):
            continue
        rows.append((ts(S.local_naive(c["recv_utc"])), c["serial"], c["label"], c["cycle_no"], c["arrival_no"], ts(op),
                     "" if c["travel_s"] is None else c["travel_s"], c["result"], c["afterflow_min"],
                     c["casing_kpa"], c["tubing_kpa"]))
    return rows


# --------------------------------------------------------------------------------------------- daily volumes
def prod_rows(wd):
    fac = facility_codes(wd)
    run_of = {r["prod_month"]: r["run"] for r in wd["runs"] if r["kind"] == "Original"}
    rows = []
    for d, day in enumerate(W.DAYS):
        for s in wd["sites"]:
            for sep in s["seps"]:
                p = wd["prod"][sep["uwi"]]
                rows.append((day.isoformat(), sep["uwi"], fac[s["code"]], int(round(p["hours"][d])), f1(p["gas"][d]),
                             f1(p["cond"][d]), f1(p["water"][d]), run_of["%04d-%02d" % (day.year, day.month)]))
    return rows


def ppa_rows(wd):
    return [(p["journal"], p["posted"].isoformat(), p["run"], p["uwi"], p["product"], f1(p["vol"]), p["text"])
            for p in wd["ppa"]]


def run_rows(wd):
    who = {"Original": "VSANDERS", "Re-run": "VSANDERS"}
    r = S.rng(12)
    out = []
    for x in sorted(wd["runs"], key=lambda k: k["run"]):
        out.append((x["run"], x["prod_month"], x["run_date"].isoformat(), x["kind"],
                    who[x["kind"]] if r.random() < 0.7 else "AHUNTER"))
    return out


# --------------------------------------------------------------------------------------------- gas analyses
def analysis_rows(wd):
    r = S.rng(13)
    r2 = S.rng(19)
    rows = []
    no = 26018
    points = ["Separator gas outlet", "Sales meter run", "Separator gas outlet", "Wellhead, upstream of choke"]
    for s in wd["sites"]:
        point = points[int(r2.integers(0, len(points)))]
        labs = {2025: "Peace Country Analytical" if r2.random() < 0.8 else "Bezanson Analytical",
                2026: "Bezanson Analytical" if r2.random() < 0.55 else "Peace Country Analytical"}
        for year, x, month in ((2025, s["x2025"], int(r.integers(8, 12))), (2026, s["x2026"], int(r.integers(5, 10)))):
            no += int(r.integers(3, 40))
            c1 = round(x * 100.0, 2)
            rest = 100.0 - c1
            n2 = round(float(r.uniform(0.25, 1.1)), 2)
            co2 = round(float(r.uniform(0.3, 1.6)), 2)
            hyd = rest - n2 - co2
            c2 = round(hyd * float(r.uniform(0.55, 0.66)), 2)
            c3 = round(hyd * float(r.uniform(0.18, 0.24)), 2)
            ic4 = round(hyd * float(r.uniform(0.03, 0.05)), 2)
            nc4 = round(hyd * float(r.uniform(0.05, 0.08)), 2)
            c5 = round(100.0 - c1 - n2 - co2 - c2 - c3 - ic4 - nc4, 2)
            date = dt.date(year, month, int(r.integers(2, 28)))
            lab_no = ("GA-%d" % no) if labs[year] == "Peace Country Analytical" else ("B%02d-%05d" % (year % 100, no * 3 % 99991))
            rows.append((lab_no, s["lsd"], date.isoformat(), point, labs[year],
                         "%.2f" % c1, "%.2f" % c2, "%.2f" % c3, "%.2f" % ic4, "%.2f" % nc4, "%.2f" % c5, "%.2f" % n2,
                         "%.2f" % co2))
    rows.sort(key=lambda x: (x[2], x[0]))
    return rows


# --------------------------------------------------------------------------------------------- dump counters
def counter_tag(sep):
    return "%s_%s_LC%s.DMPCNT" % (AREA_PREFIX[sep["area"]], sep["site"][1:], sep["lc_tag"][-2:])


AREA_PREFIX = {"Kakwa": "KAK", "Elmworth": "ELM"}


def counter_rows(wd):
    r = S.rng(14)
    rows = []
    for sep in wd["seps"]:
        if not sep["auto"]:
            continue
        series = wd["counters"][sep["uwi"]]
        gaps = set()
        for _ in range(int(r.integers(3, 7))):
            g0 = int(r.integers(60, len(series) - 80))
            for k in range(g0, g0 + int(r.integers(2, 19))):
                gaps.add(k)
        if sep["site"] in ("K1122", "E0617"):
            g0 = int(r.integers(2000, 7000))
            for k in range(g0, g0 + int(r.integers(30, 70))):
                gaps.add(k)
        for k, (t, v) in enumerate(series):
            if k in gaps and t not in (W.WINDOW_START_UTC, W.WINDOW_END_UTC):
                continue
            rows.append((t.strftime("%Y-%m-%dT%H:%M:%SZ"), counter_tag(sep), v))
    rows.sort(key=lambda x: (x[0], x[1]))
    return rows


# --------------------------------------------------------------------------------------------- work orders
def order_rows(wd):
    pad = {s["code"]: s["name"] for s in wd["sites"]}
    rows = []
    for o in wd["orders"]:
        rows.append((o["wo"], ts(o["created"]), pad[o["site"]], o["tag"], o["type"], o["text"], o["tech"], o["status"]))
    return rows


# --------------------------------------------------------------------------------------------- the register
HEAD = Font(name="Calibri", bold=True, size=11)
BODY = Font(name="Calibri", size=11)
FILL = PatternFill("solid", fgColor="DDEBF7")


def _sheet(ws, header, rows, widths):
    ws.append(header)
    for c in ws[1]:
        c.font = HEAD
        c.fill = FILL
        c.alignment = Alignment(vertical="center")
    for row in rows:
        ws.append([None if v == "" else v for v in row])
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = "A2"


def register_state(wd):
    """The register as it stands at the export: removed devices gone, replaced devices under their new model and
    serial, the re-piped pads' pressure controllers renumbered."""
    devices = []
    for s in wd["sites"]:
        for sep in s["seps"]:
            devices.append({"tag": sep["lc_tag"], "site": s["code"], "class": "Intermittent vent",
                            "service": "Separator level, %s" % sep["tag"], "maker": W.LC_MODELS[sep["model"]]["maker"],
                            "model": sep["model"], "serial": sep["serial"], "in_service": sep["installed"]})
    retag = {site for site, _ in W.RETAGGED}
    for h in sorted(wd["bleed_hist"].values(), key=lambda h: (h["site"], h["tag"], h["from"])):
        if h["removed"] or h["to"] < dt.datetime(2027, 1, 1, 8):
            continue
        tag = h["tag"]
        if h["site"] in retag and tag in ("PC-1", "PC-2"):
            tag = "PC-2" if tag == "PC-1" else "PC-1"
        b = next((x for x in wd["bleeds"] if x["serial"] == h["serial"]), None)
        when = h["from"].date() if (b is None or h["from"] > dt.datetime(2026, 1, 1, 8)) else b["installed"]
        service = "Line heater bath temperature" if h["kind"] == "TC" else "Sales gas back pressure"
        devices.append({"tag": tag, "site": h["site"], "class": "Continuous bleed", "service": service,
                        "maker": W.BLEED_MODELS[h["model"]]["maker"], "model": h["model"], "serial": h["serial"],
                        "in_service": when})
    return devices


def write_register(path, wd):
    fac = facility_codes(wd)
    r = S.rng(16)
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Pads"
    _sheet(ws, ["Pad", "Surface location", "Area", "Reporting facility", "Instrument supply (kPa)", "Supply medium", "Status"],
           [(s["name"], s["lsd"], s["area"], fac[s["code"]], W.SUPPLY_KPA, "Fuel gas", "Active") for s in wd["sites"]],
           [16, 18, 11, 18, 22, 14, 10])
    ws = wb.create_sheet("Wells")
    rows = []
    for s in wd["sites"]:
        for sep, w in [(x, next(y for y in wd["wells"] if y["uwi"] == x["uwi"])) for x in s["seps"]]:
            rows.append((w["uwi"], w["name"], s["name"], w["lift"], w["plunger"] or "", "Producing", w["tubing"],
                         w["depth_m"] if w["depth_m"] else ""))
    _sheet(ws, ["UWI", "Well name", "Pad", "Artificial lift", "Plunger", "Status", "Tubing", "Bumper spring (mKB)"], rows,
           [24, 26, 16, 15, 18, 11, 10, 20])
    ws = wb.create_sheet("Vessels")
    rows = []
    for s in wd["sites"]:
        for sep in s["seps"]:
            w = next(y for y in wd["wells"] if y["uwi"] == sep["uwi"])
            sts = {20: 7.5, 24: 7.5, 30: 10.0, 36: 10.0, 42: 10.0, 48: 12.5}[sep["bore"]]
            rows.append((sep["tag"], s["name"], "Wellsite separator, two-phase", "Vertical", sep["bore"], sts,
                         sep["lc_tag"], "%s %s" % (W.MAKERS[W.LC_MODELS[sep["model"]]["maker"]], sep["model"]),
                         sep["span"], sep["valve"], w["name"], "Yes" if sep["auto"] else "", sep["low_in"],
                         sep["lshh_in"]))
    _sheet(ws, ["Vessel", "Pad", "Service", "Orientation", "Bore (in)", "Seam to seam (ft)", "Level controller",
                "Controller make and model", "Controller span (in)", "Dump valve", "Inlet from well", "SCADA dump count",
                "Lower setting (in above bottom seam)", "LSHH (in above bottom seam)"],
           rows, [10, 16, 28, 12, 10, 17, 16, 32, 19, 11, 26, 17, 20, 18])
    ws = wb.create_sheet("Pneumatic devices")
    pad = {s["code"]: s["name"] for s in wd["sites"]}
    devs = register_state(wd)
    _sheet(ws, ["Device tag", "Pad", "Vent class", "Service", "Make", "Model", "Serial", "In service"],
           [(d["tag"], pad[d["site"]], d["class"], d["service"], W.MAKERS[d["maker"]], d["model"], d["serial"],
             d["in_service"]) for d in sorted(devs, key=lambda d: (pad[d["site"]], d["tag"]))],
           [12, 16, 18, 30, 26, 9, 11, 12])
    for row in ws.iter_rows(min_row=2, min_col=8, max_col=8):
        for c in row:
            c.number_format = "yyyy-mm-dd"
    wb.save(path)


# --------------------------------------------------------------------------------------------- the template
def write_template(path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Annex B sources"
    ws.append(["MRS-03 Annex B: source-level methane inventory"])
    ws["A1"].font = Font(name="Calibri", bold=True, size=13)
    ws.append(["Operator"])
    ws.append(["Reporting year"])
    ws.append(["Prepared by"])
    ws.append([])
    ws.append(["Pad", "Surface location", "Source tag", "Source class", "Make and model", "Serial",
               "Activity basis", "Activity in the reporting year", "Activity unit", "Gas vented (m3)", "Methane (kg)"])
    for c in ws[6]:
        c.font = HEAD
        c.fill = FILL
    for i, w in enumerate([16, 18, 12, 18, 30, 11, 26, 18, 13, 15, 13], 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws2 = wb.create_sheet("Annex B pads")
    ws2.append(["Pad", "Surface location", "Intermittent-vent controllers, methane (t)",
                "Continuous-bleed controllers, methane (t)"])
    for c in ws2[1]:
        c.font = HEAD
        c.fill = FILL
    for i, w in enumerate([16, 18, 38, 38], 1):
        ws2.column_dimensions[get_column_letter(i)].width = w
    wb.save(path)


# --------------------------------------------------------------------------------------------- distractors
def ogi_rows(wd):
    r = S.rng(17)
    rows = []
    comps = ["Wellhead flange", "Separator PSV", "Thief hatch, tank 1", "Thief hatch, tank 2", "Meter run fitting",
             "Line heater fuel train", "Compressor packing vent", "Dump valve stem packing", "Threaded connector",
             "Pressure gauge fitting"]
    r2 = S.rng(20)
    for rnd, (m0, m1) in enumerate(((4, 5), (9, 10))):
        crew = (["J. Davis", "S. Stevens"], ["C. Petty", "J. Davis"])[rnd]
        for s in wd["sites"]:
            op = crew[0] if r2.random() < 0.6 else crew[1]
            date = dt.date(2026, m0, int(r.integers(3, 28)))
            n = int(r.poisson(1.3))
            if n == 0:
                rows.append((date.isoformat(), s["name"], "", "", "No leaks found", "", "", op))
            for _ in range(n):
                comp = comps[int(r.integers(0, len(comps)))]
                rate = round(float(r.lognormal(-1.6, 0.9)), 3)
                rep = date + D(days=int(r.integers(1, 30)))
                rows.append((date.isoformat(), s["name"], comp, "C-%04d" % int(r.integers(100, 9999)), "Leak",
                             "%.3f" % rate, rep.isoformat(), op))
    rows.sort(key=lambda x: (x[0], x[1]))
    return rows


def write_tanks(path, wd):
    r = S.rng(18)
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Tank vents 2026"
    rows = []
    for s in wd["sites"]:
        for k in range(1, 1 + int(r.integers(1, 3))):
            date = dt.date(2026, int(r.integers(5, 10)), int(r.integers(2, 28)))
            vent = round(float(r.uniform(0.0, 2.4)), 2)
            rows.append((s["name"], "T-%d" % k, date, "Vent flow, thermal mass meter, 30 min", vent,
                         "Thief hatch closed and latched" if r.random() < 0.85 else "Hatch gasket replaced after test"))
    _sheet(ws, ["Pad", "Tank", "Test date", "Method", "Vent rate (m3/h)", "Note"], rows, [16, 7, 11, 36, 15, 34])
    for row in ws.iter_rows(min_row=2, min_col=3, max_col=3):
        for c in row:
            c.number_format = "yyyy-mm-dd"
    wb.save(path)
