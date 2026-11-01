"""Writes the evidence pack under task452/target/ from the simulated works (truth.py)."""
import datetime as dt
import os
import shutil

import numpy as np

import common as C
import world as W

WORKS = "Kilcarrow Works"
COMPANY = "Kilcarrow Cement Ltd"
LICENCE = "IEL 1186-03"
LIMIT_KG = 85
ELV_HG = 50
STACK = {"K1": "A1-1", "K2": "A1-2"}
MAT_LEDGER_H1 = {"limestone": "Limestone (quarry)", "shale": "Rathmore shale", "sand": "Sand", "iron_ore": "Iron ore",
                 "steel_slag": "Steel slag (BOF)", "fly_ash": "Fly ash (PFA)"}
MAT_LEDGER_H2 = {"limestone": "Limestone", "shale": "Shale", "sand": "Sand", "iron_ore": "Iron ore",
                 "steel_slag": "Slag", "fly_ash": "PFA"}
LAB_CODE = {"limestone": "LS", "shale": "SH", "sand": "SA", "iron_ore": "FE", "steel_slag": "SL", "fly_ash": "FA",
            "coal": "CO", "srf": "RF"}
LAB_DESC = {"limestone": "Limestone, primary crusher", "shale": "Shale, Rathmore pit", "sand": "Sand, washed",
            "iron_ore": "Iron ore", "steel_slag": "Steel slag (BOF), stockpile", "fly_ash": "Fly ash (PFA), silo 4",
            "coal": "Coal, as fired (coal mills 1 and 2)", "srf": "SRF, as fired (kiln 1 calciner)"}


def utc_str(t):
    return t.strftime("%Y-%m-%d %H:%M")


def loc(t):
    return t.astimezone(W.TZ)


def write_pack(truth, target):
    if os.path.isdir(target):
        shutil.rmtree(target)
    os.makedirs(target)
    C.pdf_canvas_settings()
    files = {}
    files["licence"] = write_licence(target)
    files["historian"] = write_historian(truth, target)
    files["logger"] = write_logger(truth, target)
    files["journal"] = write_journal(truth, target)
    files["ledger"] = write_ledger(truth, target)
    files["lab"] = write_lab(truth, target)
    files["weighbridge"] = write_weighbridge(truth, target)
    files["tests"] = write_tests(truth, target)
    files["register"] = write_register(target)
    files["fuel"] = write_fuel_receipts(truth, target)
    files["quarry"] = write_quarry(truth, target)
    return files


# ------------------------------------------------------------------------------------------------- historian
SNAP_MINUTE = 0     # the minute of each half-hour at which the historian samples the raw mill's run status


def half_hour_series(truth, k):
    w = truth["world"]
    d = w["kilns"][k]
    p = W.KILNS[k]
    r = np.random.default_rng(W.SEED * 31 + (1 if k == "K1" else 2))
    n = W.NMIN // 30
    feed = d["feed"].reshape(n, 30).mean(axis=1)
    run = d["mill_on"].reshape(n, 30).mean(axis=1)
    run_snap = d["mill_on"].reshape(n, 30)[:, SNAP_MINUTE].astype(float)
    on = d["kiln_on"].reshape(n, 30).mean(axis=1)
    heat = d["heat"].reshape(n, 30).mean(axis=1)
    clk_rate = d["clk"].reshape(n, 30).sum(axis=1) * 2.0          # t/h
    o2 = np.where(on > 0, p["o2"] + r.normal(0, 0.28, n), np.where(heat > 0, 14.0 + r.normal(0, 0.4, n), 20.9))
    q_ref = np.where(on > 0, clk_rate * p["nm3_per_t"] * (1 + r.normal(0, 0.015, n)),
                     np.where(heat > 0, 0.35 * p["feed"] / 1.55 * p["nm3_per_t"], 0.0))
    q_act = np.where(o2 < 20.0, q_ref * 11.0 / (21.0 - o2), 0.0)
    t0 = np.array([W.T0 + dt.timedelta(minutes=30 * i) for i in range(n)])
    trial = np.array([W.NOX_TRIAL[0] <= t < W.NOX_TRIAL[1] for t in t0])
    nox = np.where(on > 0, p["nox"] * (1 + r.normal(0, 0.06, n)) * np.where(trial, 1.12, 1.0),
                   np.where(heat > 0, 210.0 * (1 + r.normal(0, 0.05, n)), 0.0))
    so2 = np.where(on > 0, p["so2"] * (1 + r.normal(0, 0.15, n)), np.where(heat > 0, 40.0, 0.0))
    temp = np.where(on > 0, 104.0 * run + 168.0 * (1 - run) + r.normal(0, 3.5, n),
                    np.where(heat > 0, 140.0 + r.normal(0, 5, n), 35.0 + r.normal(0, 2, n)))
    return dict(t0=t0, feed=feed, run=run, run_snap=run_snap, on=on, heat=heat, o2=o2, q_ref=q_ref, q_act=q_act, nox=nox, so2=so2,
                temp=temp)


def write_historian(truth, target):
    fn = "PI_historian_K1K2_2026_30min.csv"
    series = {k: half_hour_series(truth, k) for k in W.KILNS}
    truth["hh"] = series
    header = ["Time (UTC)", "Line", "KF.WF01.RATE t/h", "RM.MAIN.RUN", "STK.FLOW.DRY Nm3/h", "STK.O2.DRY %",
              "STK.NOX.REF10 mg/Nm3", "STK.SO2.REF10 mg/Nm3", "STK.TEMP degC"]
    rows = []
    n = len(series["K1"]["t0"])
    resend = []
    for i in range(n):
        t = series["K1"]["t0"][i]
        if W.HIST_GAP[0] <= t < W.HIST_GAP[1]:
            continue
        for k in ("K1", "K2"):
            s = series[k]
            row = [utc_str(t), k, "%.1f" % s["feed"][i], "%d" % s["run_snap"][i], "%.0f" % s["q_act"][i],
                   "%.2f" % s["o2"][i], "%.1f" % s["nox"][i], "%.1f" % s["so2"][i], "%.1f" % s["temp"][i]]
            rows.append(row)
            if k == "K1" and dt.datetime(2026, 8, 4, 2, 0, tzinfo=W.UTC) <= t < dt.datetime(2026, 8, 4, 8, 0, tzinfo=W.UTC):
                resend.append(list(row))
        if t == dt.datetime(2026, 8, 4, 9, 30, tzinfo=W.UTC):
            rows.extend(resend)          # the gateway re-sent the morning's K1 batch after the link came back
    C.write_csv(os.path.join(target, fn), header, rows)
    return fn


def write_logger(truth, target):
    fn = "CEMS_logger_A1-1_A1-2_May2026.csv"
    rows = []
    for k in ("K1", "K2"):
        s = truth["hh"][k]
        for i, t in enumerate(s["t0"]):
            if not (W.BACKFILL[0] <= t < W.BACKFILL[1]):
                continue
            end_local = loc(t + dt.timedelta(minutes=30))
            o2 = s["o2"][i]
            nox_act = s["nox"][i] * (21.0 - o2) / 11.0 if o2 < 20 else 0.0
            so2_act = s["so2"][i] * (21.0 - o2) / 11.0 if o2 < 20 else 0.0
            rows.append([end_local.strftime("%d/%m/%Y %H:%M"), STACK[k], "%.1f" % nox_act, "%.2f" % o2,
                         "%.0f" % s["q_act"][i], "%.1f" % so2_act])
    rows.sort(key=lambda r: (r[1], dt.datetime.strptime(r[0], "%d/%m/%Y %H:%M")))
    C.write_csv(os.path.join(target, fn),
                ["Interval end", "Stack", "NOx mg/Nm3 dry", "O2 % dry", "Flow Nm3/h dry", "SO2 mg/Nm3 dry"], rows,
                sep=";")
    return fn


# ------------------------------------------------------------------------------------------------- journal
ALARMS = ["PREHEATER C4 DRAFT HIGH", "COOLER GRATE 2 PRESSURE HIGH", "KILN INLET O2 LOW", "BAGHOUSE DP HIGH",
          "CALCINER TEMP DEVIATION", "COAL MILL OUTLET TEMP HIGH", "CLINKER CRUSHER OVERLOAD", "ID FAN VIBRATION",
          "TERTIARY AIR DAMPER POSITION", "KILN SHELL SCANNER HOT SPOT"]


JITTER = 0          # the seconds within each logged minute: a draw of the world, fixed below by build.py's tuning


def write_journal(truth, target):
    fn = "DCS_event_journal_2026.txt"
    w = truth["world"]
    r = np.random.default_rng(W.SEED * 53 + JITTER)
    ev = []   # (utc datetime, area, tag, description, state)
    for k in ("K1", "K2"):
        d = w["kilns"][k]
        n = k[1]
        on = d["kiln_on"]
        ch = np.flatnonzero(on[1:] != on[:-1]) + 1
        for m in ch:
            t = W.T0 + dt.timedelta(minutes=int(m), seconds=int(r.integers(0, 60)))
            ev.append((t, "KILN %s" % n, "KF.WF01", "KILN %s FEED" % n, "ON" if on[m] else "OFF"))
            if not on[m]:
                ev.append((t + dt.timedelta(seconds=int(r.integers(40, 300))), "KILN %s" % n, "BRN.MAIN",
                           "KILN %s MAIN BURNER" % n, "OFF"))
        heat = d["heat"]
        hs = np.flatnonzero(heat[1:] & ~heat[:-1]) + 1
        for m in hs:
            t = W.T0 + dt.timedelta(minutes=int(m), seconds=int(r.integers(0, 60)))
            ev.append((t, "KILN %s" % n, "BRN.MAIN", "KILN %s MAIN BURNER" % n, "ON"))
        for (m, s, kind) in d["mill_events"]:
            t = W.T0 + dt.timedelta(minutes=int(m), seconds=int(s))
            ev.append((t, "RAW MILL %s" % n, "RM%s.MAIN" % n, "RAW MILL %s" % n, kind))
    for cm in (1, 2, 3):
        t = W.T0 + dt.timedelta(hours=int(r.integers(2, 40)))
        state = True
        while t < W.T0 + dt.timedelta(days=365):
            ev.append((t, "CEMENT MILL %d" % cm, "CM%d.MAIN" % cm, "CEMENT MILL %d" % cm, "START" if state else "STOP"))
            t += dt.timedelta(minutes=int(r.integers(6 * 60, 50 * 60)) if state else int(r.integers(2 * 60, 30 * 60)))
            state = not state
    for _ in range(900):
        t = W.T0 + dt.timedelta(seconds=int(r.integers(0, 365 * 86400)))
        a = ALARMS[int(r.integers(0, len(ALARMS)))]
        line = "KILN %d" % int(r.integers(1, 3))
        ev.append((t, line, "ALM", a + " ALARM", "RAISED"))
        ev.append((t + dt.timedelta(seconds=int(r.integers(20, 3600))), line, "ALM", a + " ALARM", "CLEARED"))
    ev.append((dt.datetime(2026, 3, 29, 1, 0, 0, tzinfo=W.UTC), "SYSTEM", "OS.CLOCK", "CLOCK CHANGE GMT TO IST, +1 H", "SET"))
    ev.append((dt.datetime(2026, 10, 25, 0, 59, 59, tzinfo=W.UTC), "SYSTEM", "OS.CLOCK", "CLOCK CHANGE IST TO GMT, -1 H", "SET"))
    ev = [e for e in ev if e[0] < W.T0 + dt.timedelta(days=365)]
    ev.sort(key=lambda e: (e[0], e[1], e[3]))
    lines = ["%s DCS alarm and event journal" % WORKS,
             "Export from the operator station archive, 4 January 2027. Times are station local time.",
             "Columns: date, time, area, tag, description, state",
             ""]
    st = w["kilns"]
    lines.append("2026-01-01 00:00:00  KILN 1        KF.WF01     KILN 1 FEED                       %s     (state at start of log)"
                 % ("ON" if st["K1"]["kiln_on"][0] else "OFF"))
    lines.append("2026-01-01 00:00:00  RAW MILL 1    RM1.MAIN    RAW MILL 1                        %s     (state at start of log)"
                 % ("RUNNING" if st["K1"]["mill_on"][0] else "STOPPED"))
    lines.append("2026-01-01 00:00:00  KILN 2        KF.WF01     KILN 2 FEED                       %s     (state at start of log)"
                 % ("ON" if st["K2"]["kiln_on"][0] else "OFF"))
    lines.append("2026-01-01 00:00:00  RAW MILL 2    RM2.MAIN    RAW MILL 2                        %s     (state at start of log)"
                 % ("RUNNING" if st["K2"]["mill_on"][0] else "STOPPED"))
    for (t, area, tag, desc, state) in ev:
        lt = loc(t).strftime("%Y-%m-%d %H:%M:%S")
        lines.append("%s  %-12s  %-10s  %-32s  %s" % (lt, area, tag, desc, state))
    with open(os.path.join(target, fn), "w", encoding="utf-8", newline="") as f:
        f.write("\r\n".join(lines) + "\r\n")
    truth["journal_events"] = ev
    return fn


# ------------------------------------------------------------------------------------------------- ledger
def write_ledger(truth, target):
    from openpyxl import Workbook
    from openpyxl.styles import Font
    fn = "production_ledger_2026.xlsx"
    wb = Workbook()
    ws = wb.active
    ws.title = "H1 2026"
    ws["A1"] = "%s - production and materials ledger 2026, January to June (tonnes as weighed)" % WORKS
    ws["A1"].font = Font(bold=True)
    ws["A2"] = "Raw materials at the raw mill weigh feeders; fuels at the kiln and calciner feeders as fired; clinker from the kiln output balance."
    hdr = ["Line", "Item", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "H1"]
    ws.append([])
    ws.append(hdr)
    for c in ws[4]:
        c.font = Font(bold=True)
    led = {}
    for k in ("K1", "K2"):
        kd = truth["kiln"][k]
        items = []
        for mat in W.MIX[k]:
            items.append((mat, "mat"))
        items += [("coal", "fuel")] + ([("srf", "fuel")] if k == "K1" else []) + [("clinker", "clk"), ("silo", "silo")]
        for item, typ in items:
            vals = []
            for m in W.MONTHS:
                row = kd["rows"][m]
                if typ == "mat":
                    v = row["mats"][item]["wet"]
                elif typ == "fuel":
                    v = row["fuels"][item]["ar"]
                elif typ == "clk":
                    v = row["clk"]
                else:
                    # meal silo stock at month end
                    d = truth["world"]["kilns"][k]
                    mon = truth["world"]["mon"]
                    idx = np.flatnonzero(mon == m)[-1]
                    v = float(d["silo"][idx])
                vals.append(int(round(v)))
            led[(k, item)] = vals
    names_h1 = dict(MAT_LEDGER_H1, coal="Coal as fired", srf="SRF as fired", clinker="Clinker produced",
                    silo="Raw meal silo stock, month end")
    for k in ("K1", "K2"):
        label = "Kiln %s" % k[1]
        for (kk, item), vals in led.items():
            if kk != k:
                continue
            h1 = vals[:6]
            ws.append([label, names_h1[item]] + h1 + ([""] if item == "silo" else [sum(h1)]))
    ws2 = wb.create_sheet("H2 2026")
    ws2["A1"] = "Production and materials ledger, July to December 2026"
    ws2["A1"].font = Font(bold=True)
    ws2["A2"] = "From July the ledger is kept on the new MES template (item codes per the materials master)."
    ws2.append([])
    ws2.append(["Item", "Line", "Unit", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "H2 total"])
    for c in ws2[4]:
        c.font = Font(bold=True)
    names_h2 = dict(MAT_LEDGER_H2, coal="Coal (fired)", srf="SRF (fired)", clinker="Clinker made",
                    silo="Meal silo closing stock")
    order = ["clinker", "coal", "srf", "limestone", "shale", "fly_ash", "sand", "iron_ore", "steel_slag", "silo"]
    for item in order:
        for k in ("K1", "K2"):
            if (k, item) not in led:
                continue
            vals = led[(k, item)][6:]
            ws2.append([names_h2[item], "KL%s" % k[1], "t"] + vals + ([""] if item == "silo" else [sum(vals)]))
            if item == "clinker":
                d = truth["kiln"][k]["rows"]
                r = np.random.default_rng(W.SEED + (11 if k == "K1" else 12))
                trans = [int(round(d[m]["clk"] * float(r.uniform(0.95, 1.04)))) for m in range(7, 13)]
                ws2.append(["Clinker to cement mills", "KL%s" % k[1], "t"] + trans + [sum(trans)])
    for wsx in (ws, ws2):
        wsx.column_dimensions["A"].width = 30
        wsx.column_dimensions["B"].width = 26
    C.save_workbook(wb, os.path.join(target, fn), dt.datetime(2027, 1, 7, 16, 20), "Production Accounting")
    truth["ledger"] = led
    return fn


# ------------------------------------------------------------------------------------------------- laboratory
def write_lab(truth, target):
    from openpyxl import Workbook
    from openpyxl.styles import Font
    fn = "QC_lab_composites_2026.xlsx"
    lab = truth["lab"]
    wb = Workbook()
    ws = wb.active
    ws.title = "Results"
    hdr = ["Sample", "Description", "Line", "Period", "Moisture % (as received)", "Hg mg/kg", "CaO %", "SiO2 %",
           "Al2O3 %", "Fe2O3 %", "MgO %", "SO3 %", "LOI %", "NCV GJ/t (as received)", "Ash %", "S %"]
    ws.append(hdr)
    for c in ws[1]:
        c.font = Font(bold=True)
    mon_abbr = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    rows = []
    for mat in ["limestone", "shale", "sand", "iron_ore", "steel_slag", "fly_ash"]:
        periods = [1, 4, 7, 10] if mat in W.QUARTERLY else W.MONTHS
        line = "KL1" if mat == "steel_slag" else ("KL2" if mat == "fly_ash" else "KL1/KL2")
        for pm in periods:
            v = lab[(mat, pm)]
            code = "%s-26%s" % (LAB_CODE[mat], ("Q%d" % (1 + (pm - 1) // 3)) if mat in W.QUARTERLY else "%02d" % pm)
            per = ("Q%d 2026" % (1 + (pm - 1) // 3)) if mat in W.QUARTERLY else "%s 2026" % mon_abbr[pm - 1]
            rows.append([code, LAB_DESC[mat], line, per, v["moist"], v["hg"], v["cao"], v["sio2"], v["al2o3"],
                         v["fe2o3"], v["mgo"], v["so3"], v["loi"], None, None, None])
    for f in ("coal", "srf"):
        for pm in W.MONTHS:
            v = lab[(f, pm)]
            rows.append(["%s-26%02d" % (LAB_CODE[f], pm), LAB_DESC[f], "KL1/KL2" if f == "coal" else "KL1",
                         "%s 2026" % mon_abbr[pm - 1], v["moist"], v["hg"], None, None, None, None, None, None, None,
                         v["ncv"], v["ash"], v["s"]])
    for k in ("K1", "K2"):
        for pm in W.MONTHS:
            v = lab[("clinker_" + k, pm)]
            rows.append(["CK%s-26%02d" % (k[1], pm), "Clinker, kiln %s cooler discharge" % k[1], "KL%s" % k[1],
                         "%s 2026" % mon_abbr[pm - 1], v["moist"], v["hg"], v["cao"], v["sio2"], v["al2o3"],
                         v["fe2o3"], v["mgo"], v["so3"], v["loi"], None, None, None])
    for pm in W.MONTHS:
        v = lab[("dust_K1", pm)]
        rows.append(["FD1-26%02d" % pm, "Filter dust, silo S7 (tanker samples)", "KL1", "%s 2026" % mon_abbr[pm - 1],
                     v["moist"], v["hg"], v["cao"], None, None, None, None, None, v["loi"], None, None, None])
    for rr in rows:
        ws.append(rr)
    ws.column_dimensions["B"].width = 40
    n = wb.create_sheet("Methods")
    for line in [
        "%s quality laboratory - composite analyses 2026" % WORKS,
        "",
        "Raw materials and fuels: monthly composite of the daily increments taken at the feeders (sand, iron ore and",
        "slag: quarterly composite). Samples are dried at 105 C before analysis; every chemical result, mercury",
        "included, is on the dry sample. Moisture is the loss on drying of the sample as received.",
        "Clinker: monthly composite of the two-hourly cooler discharge samples.",
        "Filter dust (S7): monthly composite of the sample taken from each tanker loaded at silo S7.",
        "Mercury: cold vapour AAS after aqua regia digestion (contract laboratory), reporting limit 0.0005 mg/kg.",
        "Major oxides: XRF on fused beads. NCV: bomb calorimeter, reported as received.",
    ]:
        n.append([line])
    C.save_workbook(wb, os.path.join(target, fn), dt.datetime(2027, 1, 8, 11, 5), "QC Laboratory")
    return fn


# ------------------------------------------------------------------------------------------------- weighbridge
def write_weighbridge(truth, target):
    fn = "weighbridge_byproducts_2026.csv"
    r = np.random.default_rng(W.SEED * 71)
    hauliers = [("Corrib Bulk Haulage", ["221-G-4410", "221-G-4418", "191-G-2207"]),
                ("Shannonside Tankers", ["212-LK-1093", "182-LK-776"])]
    rows = []
    no = 260411
    tickets = truth["dust"]["tickets"]
    dests = ["Ballyglass landfill, cell 4", "Westway Blocks Ltd (filler)"]
    other = []
    for i in range(140):
        day = dt.date(2026, 1, 1) + dt.timedelta(days=int(r.integers(0, 365)))
        if day.weekday() >= 5:
            continue
        prod = ["KILN REFRACTORY WASTE", "SCRAP METAL", "CEMENT MILL SWEEPINGS"][int(r.integers(0, 3))]
        other.append(dict(date=day, hh=int(r.integers(7, 17)), mm=int(r.integers(0, 60)), net=round(float(r.uniform(4, 22)), 2),
                          prod=prod))
    allt = [dict(t, prod="FILTER DUST KL1 - S7") for t in tickets] + other
    allt.sort(key=lambda t: (t["date"], t["hh"], t["mm"], t["prod"]))
    reprint_days = {(3, 10): False, (9, 10): False}
    for t in allt:
        hname, vehs = hauliers[int(r.integers(0, 2))]
        veh = vehs[int(r.integers(0, len(vehs)))]
        tare = round(float(r.uniform(14300, 15600)), 0) if t["prod"].startswith("FILTER") else round(float(r.uniform(9000, 13000)), 0)
        net_kg = int(round(t["net"] * 1000))
        gross = int(tare + net_kg)
        tin = "%02d:%02d" % (t["hh"], t["mm"])
        tout = "%02d:%02d" % (t["hh"] + (1 if t["mm"] >= 25 else 0), (t["mm"] + 35) % 60)
        dest = dests[int(r.integers(0, 2))] if t["prod"].startswith("FILTER") else "Site skip area / merchant"
        row = [str(no), t["date"].strftime("%d/%m/%Y"), tin, tout, hname, veh, t["prod"], str(gross), str(int(tare)),
               str(net_kg), dest, "OK"]
        rows.append(row)
        key = (t["date"].month, 10)
        if t["prod"].startswith("FILTER") and key in reprint_days and t["date"].day >= 10 and not reprint_days[key]:
            rows.append(list(row))          # ticket reprinted at the gatehouse
            reprint_days[key] = True
        no += 1
        if t["prod"].startswith("FILTER") and int(r.integers(0, 60)) == 0:
            # a tanker weighed on the wrong product code, the ticket voided and the load re-weighed
            v = list(row)
            v[0] = str(no)
            v[6] = "FILTER DUST KL1 - S7"
            v[11] = "VOID"
            rows.append(v)
            no += 1
    C.write_csv(os.path.join(target, fn), ["Ticket", "Date", "Time in", "Time out", "Haulier", "Vehicle", "Product",
                                          "Gross kg", "Tare kg", "Net kg", "Destination", "Status"], rows)
    return fn


# ------------------------------------------------------------------------------------------------- stack tests
def test_runs(truth, k, y, mo, da, ho, mi):
    """Three runs of 90 minutes: the tested mercury rate in compound operation."""
    r = np.random.default_rng(W.SEED * 97 + y * 3 + (1 if k == "K1" else 2))
    rc = truth["kiln"][k]["r_c"] * {2024: 1.035, 2025: 0.972, 2026: 1.0}[y]
    p = W.KILNS[k]
    out = []
    start = dt.datetime(y, mo, da, ho, mi)
    for i in range(3):
        a = start + dt.timedelta(minutes=120 * i)
        b = a + dt.timedelta(minutes=90)
        if y == 2026:
            t0 = W.minute(a.replace(tzinfo=W.TZ).astimezone(W.UTC))
            d = truth["world"]["kilns"][k]
            feed = float(d["feed"][t0:t0 + 90].mean())
            assert d["mill_on"][t0:t0 + 90].all() and d["kiln_on"][t0:t0 + 90].all()
        else:
            feed = p["feed"] * float(r.uniform(0.985, 1.015))
        gph = rc * feed / p["feed"] * (1 + float(r.normal(0, 0.05)))
        clk = feed * (1 - p["loi"])
        q = clk * p["nm3_per_t"] * (1 + float(r.normal(0, 0.01)))
        conc = gph * 1e6 / q
        out.append(dict(a=a, b=b, feed=feed, clk=clk, q=q, conc=conc, gph=conc * q / 1e6,
                        o2=p["o2"] + float(r.normal(0, 0.2)), h2o=9.5 + float(r.normal(0, 0.6)),
                        temp=104 + float(r.normal(0, 3))))
    return out


def write_tests(truth, target):
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm
    from reportlab.pdfgen import canvas
    fn = "stack_tests_Hg_2024-2026.pdf"
    c = canvas.Canvas(os.path.join(target, fn), pagesize=A4, invariant=1)
    c.setAuthor("Ardcarn Emissions Monitoring Ltd")
    c.setTitle("Mercury emission tests, Kilcarrow Works, 2024 to 2026")
    truth["tests"] = {}
    for k in ("K1", "K2"):
        for (y, mo, da, ho, mi) in W.TESTS[k]:
            runs = test_runs(truth, k, y, mo, da, ho, mi)
            truth["tests"][(k, y)] = runs
            yy = 280 * mm
            c.setFont("Helvetica-Bold", 12)
            c.drawString(20 * mm, yy, "Ardcarn Emissions Monitoring Ltd - Test report AEM-%d-%s-Hg" % (y, STACK[k]))
            yy -= 7 * mm
            c.setFont("Helvetica", 9)
            for line in [
                "Client: %s, %s. Licence %s." % (COMPANY, WORKS, LICENCE),
                "Emission point %s (Kiln %s main stack). Parameter: total mercury, EN 13211 (manual, iodine/permanganate)." % (STACK[k], k[1]),
                "Test date: %s. Accreditation: ISO/IEC 17025 testing laboratory." % dt.date(y, mo, da).strftime("%d %B %Y"),
                "Results at reference conditions: 273 K, 101.3 kPa, dry gas, 10% O2. Flow at the same reference conditions.",
                "",
                "Process conditions during the test (from the client's control system):",
            ]:
                c.drawString(20 * mm, yy, line)
                yy -= 5 * mm
            c.setFont("Helvetica-Bold", 8)
            cols = [20, 34, 62, 86, 108, 130, 150, 170]
            heads = ["Run", "Time (local)", "Kiln feed t/h", "Clinker t/h", "Raw mill", "Fuel", "Stack O2 %", "H2O %"]
            for x, h in zip(cols, heads):
                c.drawString(x * mm, yy, h)
            yy -= 5 * mm
            c.setFont("Helvetica", 8)
            for i, rr in enumerate(runs):
                fuel = "coal + SRF" if k == "K1" else "coal"
                vals = [str(i + 1), "%s-%s" % (rr["a"].strftime("%H:%M"), rr["b"].strftime("%H:%M")), "%.1f" % rr["feed"],
                        "%.1f" % rr["clk"], "in operation", fuel, "%.1f" % rr["o2"], "%.1f" % rr["h2o"]]
                for x, v in zip(cols, vals):
                    c.drawString(x * mm, yy, v)
                yy -= 5 * mm
            yy -= 3 * mm
            c.setFont("Helvetica-Bold", 8)
            heads = ["Run", "Hg ug/Nm3", "Flow Nm3/h", "Hg mass g/h", "ELV ug/Nm3", "Result"]
            cols = [20, 40, 70, 100, 130, 155]
            for x, h in zip(cols, heads):
                c.drawString(x * mm, yy, h)
            yy -= 5 * mm
            c.setFont("Helvetica", 8)
            for i, rr in enumerate(runs):
                vals = [str(i + 1), "%.1f" % rr["conc"], "%.0f" % rr["q"], "%.2f" % rr["gph"], str(ELV_HG), "below ELV"]
                for x, v in zip(cols, vals):
                    c.drawString(x * mm, yy, v)
                yy -= 5 * mm
            mc = sum(rr["conc"] for rr in runs) / 3
            mg = sum(rr["gph"] for rr in runs) / 3
            mq = sum(rr["q"] for rr in runs) / 3
            vals = ["Mean", "%.1f" % mc, "%.0f" % mq, "%.2f" % mg, str(ELV_HG), "compliant"]
            c.setFont("Helvetica-Bold", 8)
            for x, v in zip(cols, vals):
                c.drawString(x * mm, yy, v)
            yy -= 8 * mm
            c.setFont("Helvetica", 8)
            for line in [
                "Expanded uncertainty of the mean concentration (k = 2): 18 per cent of the measured value.",
                "Sampling plane complies with EN 15259 (homogeneity test 2019). Blank values below 0.1 ug/Nm3.",
                "Signed for the laboratory: technical manager.",
            ]:
                c.drawString(20 * mm, yy, line)
                yy -= 5 * mm
            c.showPage()
    c.save()
    return fn


# ------------------------------------------------------------------------------------------------- register
def write_register(target):
    from openpyxl import Workbook
    from openpyxl.styles import Font
    fn = "site_register_2026.xlsx"
    wb = Workbook()
    ws = wb.active
    ws.title = "Emission points"
    ws.append(["Emission point", "Source", "Height m", "Monitoring", "Notes"])
    for c in ws[1]:
        c.font = Font(bold=True)
    for r in [["A1-1", "Kiln 1 main stack (kiln, raw mill 1 and coal mill 1 gas after the bag filter)", 92,
               "CEMS: dust, NOx, SO2, O2, flow; periodic: Hg, metals, HCl, HF, TOC", "Filter dust bled to silo S7"],
              ["A1-2", "Kiln 2 main stack (kiln, raw mill 2 and coal mill 2 gas after the bag filter)", 85,
               "CEMS: dust, NOx, SO2, O2, flow; periodic: Hg, metals, HCl, HF, TOC", "Filter dust returned to the kiln feed"],
              ["A2-1", "Cement mill 1 bag filter", 38, "Periodic: dust", ""],
              ["A2-2", "Cement mill 2 bag filter", 38, "Periodic: dust", ""],
              ["A2-3", "Cement mill 3 bag filter", 41, "Periodic: dust", ""],
              ["A3-1", "Clinker cooler exhaust (both lines, after the ESP)", 45, "Periodic: dust", ""]]:
        ws.append(r)
    ws2 = wb.create_sheet("Plant")
    ws2.append(["Unit", "Description", "Rated capacity", "Commissioned"])
    for c in ws2[1]:
        c.font = Font(bold=True)
    for r in [["Kiln 1", "Dry process kiln, five-stage preheater with calciner", "3,200 t/d clinker", 1998],
              ["Raw mill 1", "Vertical roller mill, kiln 1 line", "260 t/h raw meal", 1998],
              ["Meal silo 1", "Homogenising silo, kiln 1", "9,000 t", 1998],
              ["Coal mill 1", "Vertical roller mill", "16 t/h", 1998],
              ["Silo S7", "Filter dust silo, kiln 1 bag filter", "650 t", 2014],
              ["Kiln 2", "Dry process kiln, four-stage preheater", "2,300 t/d clinker", 1987],
              ["Raw mill 2", "Ball mill, kiln 2 line", "185 t/h raw meal", 1987],
              ["Meal silo 2", "Homogenising silo, kiln 2", "6,500 t", 1987],
              ["Coal mill 2", "Ball mill", "13 t/h", 1987],
              ["Cement mills 1 to 3", "Ball mills", "95 / 95 / 120 t/h", "1987-2009"]]:
        ws2.append(r)
    for wsx in (ws, ws2):
        wsx.column_dimensions["B"].width = 70
    C.save_workbook(wb, os.path.join(target, fn), dt.datetime(2026, 3, 2, 10, 0), "Environment and Quality")
    return fn


# ------------------------------------------------------------------------------------------------- distractors
def write_fuel_receipts(truth, target):
    fn = "fuel_receipts_2026.csv"
    r = np.random.default_rng(W.SEED * 89)
    rows = []
    for i, (d, t) in enumerate([((2025, 12, 2), 61250), ((2026, 3, 18), 58400), ((2026, 6, 22), 60120),
                               ((2026, 9, 14), 57930), ((2026, 12, 9), 59880)]):
        rows.append([dt.date(*d).strftime("%Y-%m-%d"), "Coal", "MV cargo %d (Foynes discharge, trucked)" % (i + 1), t,
                     "%.0f" % (W.FUELS["coal"][0] * 1000 * (1 - W.FUELS["coal"][1] / 100) * float(np.exp(r.normal(0, 0.15)))),
                     "%.2f" % (W.FUELS["coal"][2] * (1 + float(r.normal(0, 0.02)))), "%.1f" % (W.FUELS["coal"][1] * (1 + float(r.normal(0, 0.08))))])
    day = dt.date(2026, 1, 5)
    while day.year == 2026:
        if day.weekday() < 5:
            t = int(r.integers(600, 1150))
            rows.append([day.strftime("%Y-%m-%d"), "SRF", "Midland Recovered Fuels, weekly lot", t,
                         "%.0f" % (W.FUELS["srf"][0] * 1000 * (1 - W.FUELS["srf"][1] / 100) * float(np.exp(r.normal(0, 0.25)))),
                         "%.2f" % (W.FUELS["srf"][2] * (1 + float(r.normal(0, 0.04)))), "%.1f" % (W.FUELS["srf"][1] * (1 + float(r.normal(0, 0.1))))])
        day += dt.timedelta(days=7)
    C.write_csv(os.path.join(target, fn), ["Received", "Fuel", "Consignment", "Tonnes received",
                                          "Supplier cert. Hg ug/kg (as received)", "Supplier cert. NCV GJ/t", "Supplier cert. moisture %"], rows)
    return fn


def write_quarry(truth, target):
    fn = "quarry_extraction_2026.csv"
    r = np.random.default_rng(W.SEED * 83)
    rows = []
    day = dt.date(2026, 1, 1)
    blast = 1
    while day.year == 2026:
        if day.weekday() < 5 and not (day.month == 12 and day.day > 22):
            for face, mat, lo, hi in (("Face 2 bench 3", "Limestone", 3800, 6200), ("Face 4 bench 1", "Limestone", 900, 2400),
                                      ("Rathmore pit", "Shale", 600, 1300)):
                t = int(r.integers(lo, hi))
                b = ""
                if mat == "Limestone" and int(r.integers(0, 6)) == 0:
                    b = "B26-%03d" % blast
                    blast += 1
                rows.append([day.strftime("%Y-%m-%d"), face, mat, t, b])
        day += dt.timedelta(days=1)
    C.write_csv(os.path.join(target, fn), ["Date", "Face", "Material", "Tonnes hauled to crusher", "Blast ref"], rows)
    return fn


# ------------------------------------------------------------------------------------------------- licence
def write_licence(target):
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm
    from reportlab.pdfgen import canvas
    fn = "IEL-1186-03_conditions_consolidated_2026.pdf"
    c = canvas.Canvas(os.path.join(target, fn), pagesize=A4, invariant=1)
    c.setTitle("Industrial emissions licence 1186-03, consolidated conditions")
    blocks = [
        ("Industrial Emissions Licence %s" % LICENCE, "B", 13),
        ("Licensee: %s. Installation: %s, cement and clinker manufacture." % (COMPANY, WORKS), "", 9),
        ("Consolidated conditions incorporating the 2026 review (amendment notice of 30 June 2026). Extract: conditions 1, 5 and 6 and Schedules B and C.", "", 9),
        ("", "", 9),
        ("Condition 1  Interpretation", "B", 10),
        ("1.4  Compound operation: hours in which a kiln is producing clinker and its raw mill is running, so that the kiln gas passes through the raw mill before the bag filter.", "", 9),
        ("1.5  Direct operation: hours in which a kiln is producing clinker and its raw mill is stopped, so that the kiln gas passes from the conditioning tower to the bag filter.", "", 9),
        ("1.6  Reference conditions: 273 K, 101.3 kPa, dry gas, 10% oxygen.", "", 9),
        ("1.7  Calendar year: 1 January to 31 December, Irish local time.", "", 9),
        ("", "", 9),
        ("Condition 5  Emissions to air", "B", 10),
        ("5.1  No emission from the emission points listed in Schedule B shall exceed the limit values in Schedule B.", "", 9),
        ("5.3  Continuous monitors on emission points A1-1 and A1-2 shall be maintained to EN 14181. Periodic monitoring shall be carried out at least once a year by an accredited laboratory.", "", 9),
        ("5.6  From 1 January 2028 the mass of mercury released to air from emission points A1-1 and A1-2 together shall not exceed %d kg in any calendar year. The mass is the mercury released over every hour each kiln fires, in compound operation and in direct operation." % LIMIT_KG, "", 9),
        ("5.7  The licensee shall submit to the Agency by 31 March 2027 a mercury reduction programme setting out the measures, if any, needed to meet condition 5.6.", "", 9),
        ("", "", 9),
        ("Condition 6  Reporting", "B", 10),
        ("6.4  The annual environmental report shall state, for each emission point in Schedule C, the mass of each listed substance released to air in the calendar year, determined for every hour of the year.", "", 9),
        ("6.5  Process carbon dioxide from the calcination of raw materials shall be reported for each kiln as the carbon dioxide released by the carbonates in its raw meal in making the clinker of the year, in tonnes, with the factor per tonne of clinker.", "", 9),
        ("", "", 9),
        ("Schedule B  Emission limit values, emission points A1-1 and A1-2 (reference conditions)", "B", 10),
        ("Dust 10 mg/Nm3 (daily average). Nitrogen oxides as NO2: 450 mg/Nm3 (daily average). Sulphur dioxide 400 mg/Nm3 (daily average). Mercury: 50 ug/Nm3 (mean of the sampling period). TOC 30 mg/Nm3.", "", 9),
        ("", "", 9),
        ("Schedule C  Substances to be reported, emission points A1-1 and A1-2", "B", 10),
        ("Nitrogen oxides (as NO2), sulphur dioxide, dust, mercury, carbon dioxide.", "", 9),
    ]
    import textwrap
    y = 280 * mm
    for text, style, size in blocks:
        c.setFont("Helvetica-Bold" if style == "B" else "Helvetica", size)
        if not text:
            y -= 3 * mm
            continue
        for ln in textwrap.wrap(text, 105 if size <= 9 else 90):
            c.drawString(18 * mm, y, ln)
            y -= 4.6 * mm
    c.showPage()
    c.save()
    return fn
