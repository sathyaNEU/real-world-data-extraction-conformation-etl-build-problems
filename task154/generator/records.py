"""The pack's data files, each in the layout the system that produced it writes."""
from __future__ import annotations

import datetime as dt
import math
import os

import numpy as np
import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

import common as K
import world as W

F_TEST = "bh2_crt_june2014.xlsx"
F_OBS = "ob_monthly_levels_2015-2026.csv"
F_RMB = "windle_cross_obh_daily_levels.csv"
F_SURVEY = "site_survey_boreholes_2026.csv"
F_TELEM = "bh2_site_telemetry_15min_2025-2026.csv"
F_PUMP = "bh2_wellhead_controller_events.csv"
F_TICKETS = "teme_valley_bulk_tickets_2026.xlsx"
F_RUNS = "bottling_runs_2025-2026.csv"
F_SKU = "sku_master_export_2026-10.xlsx"
F_QC = "qc_fill_weights_2025-2026.csv"
F_QUALITY = "bh2_water_quality_2015-2026.csv"
F_RAIN = "brackenholt_rain_gauge_2015-2026.csv"

HEAD_FILL = PatternFill("solid", fgColor="DCE6F1")
BOLD = Font(bold=True)


def _autosize(ws, widths):
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w


# ------------------------------------------------------------------------------------------------- the 2014 test
def write_test(out):
    times, tmin, s = W.test_series()
    g = K.rng("testnoise")
    wb = openpyxl.Workbook()
    ws0 = wb.active
    ws0.title = "Field sheet"
    pump_on_local = K.utc_to_local(K.TEST_START_UTC)
    ws0.append(["Brackenholt BH2 constant-rate test"])
    ws0.append(["Pump on", pump_on_local.strftime("%d/%m/%Y %H:%M"), "BST"])
    ws0.append(["Pump off", (pump_on_local + dt.timedelta(hours=K.TEST_PUMP_H)).strftime("%d/%m/%Y %H:%M"), "BST"])
    ws0.append(["Discharge to", "Brackenholt Brook via the settling lagoon (consent BR/2014/07)"])
    ws0.append(["Datum for dips", "top of casing at each borehole"])
    ws0.append([])
    ws0.append(["Date", "Time (BST)", "Borehole", "Dip (m btoc)", "Flow meter (l/s)", "Remarks"])
    for c in ws0[7]:
        c.font = BOLD
        c.fill = HEAD_FILL
    rest_dtw = {"BH2": K.BH2["ct"] - (K.REST_2015 + 0.21), "OB1": K.OBS["OB1"]["ct"] - 90.08,
                "OB2": K.OBS["OB2"]["ct"] - 90.31, "OB3": K.OBS["OB3"]["ct"] - 89.66}
    sched = [-60, 10, 30, 60, 120, 240, 480, 720, 1440, 2160, 2880, 3600, 4320, 4330, 4380, 4560, 5040, 5760, 7200]
    gf = K.rng("fieldsheet")
    for mins in sched:
        t_loc = pump_on_local + dt.timedelta(minutes=mins + int(gf.integers(0, 6)))
        for bh in ("BH2", "OB1", "OB2", "OB3"):
            idx = int(round(mins + K.TEST_PRE_H * 60))
            idx = min(max(idx, 0), len(tmin) - 1)
            dd = s[bh][idx]
            dip = rest_dtw[bh] + dd + gf.normal(0, 0.006)
            flow = ""
            if bh == "BH2" and 0 < mins < K.TEST_PUMP_H * 60:
                flow = round(float(W.test_rate_ls(mins / 60.0)) + gf.normal(0, 0.05), 2)
            rem = ""
            if mins == -60 and bh == "BH2":
                rem = "rest water level before test"
            if mins == 4320 and bh == "BH2":
                rem = "pump off, recovery begins"
            ws0.append([t_loc.strftime("%d/%m/%Y"), t_loc.strftime("%H:%M"), bh, round(dip, 3), flow, rem])
    _autosize(ws0, [12, 11, 10, 13, 15, 34])
    # loggers: BH2, OB1 and OB2 a level logger set to UTC (metres of water above the sensor); OB3 a pressure
    # logger set to local time (vented, kPa above atmosphere)
    sensor_depth = {"BH2": 34.00, "OB1": 24.00, "OB2": 22.50, "OB3": 21.00}
    for bh in ("BH2", "OB1", "OB2", "OB3"):
        ws = wb.create_sheet(bh)
        base_col = rest_dtw[bh]
        col0 = sensor_depth[bh] - base_col          # water column above the sensor at rest
        rec = -0.0008 * (np.arange(len(times)) / 1440.0)   # the summer's slow natural recession, metres
        noise = g.normal(0, 0.004 if bh == "BH2" else 0.0021, len(times))
        col = col0 - s[bh] + rec + noise
        if bh != "OB3":
            ws.append(["Serial", "LL-%s" % K.token("serial", bh, n=6).upper()])
            ws.append(["Site", "Brackenholt %s" % bh])
            ws.append(["Units", "m (water above sensor)"])
            ws.append(["Clock", "UTC"])
            ws.append(["Sensor depth", "%.2f m below top of casing" % sensor_depth[bh]])
            ws.append([])
            ws.append(["Date", "Time", "Level_m", "Temp_C"])
            for c in ws[7]:
                c.font = BOLD
            for i, t in enumerate(times):
                temp = 11.4 + 0.02 * math.sin(i / 300.0)
                ws.append([t.strftime("%Y-%m-%d"), t.strftime("%H:%M:%S"), round(float(col[i]), 3), round(temp, 2)])
            _autosize(ws, [12, 10, 10, 9])
        else:
            ws.append(["Instrument", "PT-200 vented pressure transducer"])
            ws.append(["Location", "OB3 Brackenholt"])
            ws.append(["Pressure unit", "kPa (gauge)"])
            ws.append(["Time zone", "Europe/London (BST)"])
            ws.append(["Cable length", "%.1f m" % sensor_depth[bh]])
            ws.append([])
            ws.append(["Date/time", "Pressure kPa"])
            for c in ws[7]:
                c.font = BOLD
            for i, t in enumerate(times):
                tl = K.utc_to_local(t)
                ws.append([tl.strftime("%d/%m/%Y %H:%M"), round(float(col[i]) * 9.80665, 2)])
            _autosize(ws, [18, 14])
    wb.save(os.path.join(out, F_TEST))
    return sum(1 for _ in times) * 4


# ------------------------------------------------------------------------------------------------- the long record
def write_obs(out, O):
    rows, rest = W.long_record(O)
    out_rows = []
    for r in rows:
        ob = r["ob"]
        ct = K.OBS[ob]["ct"]
        when = dt.date(r["y"], r["m"], 15)
        if ob == "OB2" and when >= K.OB2_RAISE:
            ct = ct + K.OB2_RAISE_M
        dtw = ct - r["level"]
        n = W.month_days(r["y"], r["m"])
        logger = "LL-%s" % K.token("ltlogger", ob, 2015 if r["y"] < 2021 else 2021, n=6).upper()
        out_rows.append(["%04d-%02d" % (r["y"], r["m"]), ob, "%.2f" % dtw, n, logger])
    K.write_csv(os.path.join(out, F_OBS), ["month", "borehole", "mean_depth_to_water_m_btoc", "daily_readings",
                                           "logger"], out_rows)
    return len(out_rows)


def write_rmb(out):
    rows = W.rmb_daily()
    K.write_csv(os.path.join(out, F_RMB), ["Station", "Date", "Level (mAOD)", "Quality"],
                [[K.RMB["name"], d.strftime("%d/%m/%Y"), "%.3f" % v, q] for d, v, q in rows])
    return len(rows)


def write_survey(out):
    rows = []

    def add(name, kind, xy, gl, ct, depth, note):
        e, n = K.to_grid(xy)
        rows.append([name, kind, "%.1f" % e, "%.1f" % n, "%.2f" % gl, "%.2f" % ct if ct is not None else "",
                     "%.1f" % depth if depth else "", note])
    add("BH2", "production borehole", K.BH2["xy"], K.BH2["gl"], K.BH2["ct"], K.BH2["depth"], "screened 84-160 m")
    for ob, info in K.OBS.items():
        note = "logger since May 2015"
        if ob == "OB2":
            add(ob, "observation borehole", info["xy"], info["gl"], info["ct"], info["depth"],
                "casing top until 18/02/2020; logger since May 2015")
            add(ob, "observation borehole", info["xy"], info["gl"], info["ct"] + K.OB2_RAISE_M, info["depth"],
                "casing top from 18/02/2020 (headworks fitted)")
            continue
        add(ob, "observation borehole", info["xy"], info["gl"], info["ct"], info["depth"], note)
    add("BH1", "trial borehole (backfilled 2013)", (-410.0, 515.0), 98.12, None, 96.0, "backfilled October 2013")
    K.write_csv(os.path.join(out, F_SURVEY), ["point", "type", "easting", "northing", "ground_level_maod",
                                              "casing_top_maod", "depth_m", "note"], rows)
    return len(rows)


# ------------------------------------------------------------------------------------------------- operations
def telemetry(O):
    """15-minute site telemetry on a UTC clock: FM-1's register and mean flow, the four line meters' registers and
    the treated tank's level. Each UTC quarter reads the plant's local minutes (the October night's repeated hour and
    the March night's missing hour fall in hours the plant and the bay are idle, asserted). FM-1 was replaced on
    14 October 2025 and the new register starts at zero."""
    base_local = O["base"]
    nmin = O["nmin"]
    t0 = K.local_to_utc(base_local)
    t1 = K.local_to_utc(base_local + dt.timedelta(minutes=nmin - 15))
    swap_utc = K.local_to_utc(dt.datetime(2025, 10, 14, 11, 30))
    reg_old, reg_new = 418306.4, 0.0
    regs = {"L1": 52310.27, "L2": 88912.60, "L3": 40377.15, "L4": 9874.33}
    g = K.rng("tank")
    level = 82.0
    rows = []
    t = t0
    while t <= t1:
        loc = K.utc_to_local(t)
        i = int((loc - base_local).total_seconds() // 60)
        q1 = float(O["fm1"][i:i + 15].sum())
        ql = {ln: float(O["line_use"][ln][i:i + 15].sum()) for ln in W.LINES}
        if t < swap_utc:
            reg_old += q1
            fm1_reg = reg_old
        else:
            reg_new += q1
            fm1_reg = reg_new
        for ln in W.LINES:
            regs[ln] += ql[ln]
        level = min(99.0, max(30.0, level + (q1 - sum(ql.values())) / W.TANK_M3 * 100 - 0.05 + g.normal(0, 0.15)))
        rows.append([t.strftime("%Y-%m-%dT%H:%MZ"), "%.1f" % fm1_reg, "%.2f" % (q1 * 1000 / 900.0),
                     "%.2f" % regs["L1"], "%.2f" % regs["L2"], "%.2f" % regs["L3"], "%.2f" % regs["L4"],
                     "%.0f" % level])
        t += dt.timedelta(minutes=15)
    return rows


def write_telemetry(out, O):
    rows = telemetry(O)
    K.write_csv(os.path.join(out, F_TELEM), ["time_utc", "fm1_register_m3", "fm1_flow_ls", "fm_l1_register_m3",
                                             "fm_l2_register_m3", "fm_l3_register_m3", "fm_l4_register_m3",
                                             "tank_level_pct"], rows)
    return len(rows)


def pump_events(O):
    """The wellhead controller's log, local time: the pump starts whenever the plant inlet's valve or the bulk bay's
    valve opens and stops when both are shut."""
    base = O["base"]
    g = K.rng("pumpclock")
    runs = []
    pp = O["pump_plant"]
    m = 0
    n = len(pp)
    while m < n:
        if pp[m]:
            a = m
            while m < n and pp[m]:
                m += 1
            runs.append((base + dt.timedelta(minutes=a, seconds=int(g.integers(0, 50))),
                         base + dt.timedelta(minutes=m, seconds=int(g.integers(0, 50))), "plant"))
        else:
            m += 1
    for f in O["fills"]:
        st = f["start"] + dt.timedelta(seconds=int(g.integers(0, 20)))
        runs.append((st, st + dt.timedelta(seconds=f["seconds"] + int(g.integers(3, 12))), "bay"))
    runs.sort()
    for (a0, b0, _), (a1, b1, _) in zip(runs, runs[1:]):
        assert b0 < a1, (b0, a1)
    # the controller's other entries: an overload trip now and then on a plant run (logged with its stop and
    # cleared by a fault reset before the next start), the outstation's link to the telemetry lost and restored in
    # an idle spell, and a stop the outstation re-sends from its buffer when the link comes back
    gq = K.rng("pumplog")
    ev = []
    for i, (a, b, kind) in enumerate(runs):
        nxt = runs[i + 1][0] if i + 1 < len(runs) else b + dt.timedelta(hours=6)
        idle = (nxt - b).total_seconds()
        r = gq.random()
        ev.append((a, "BH2-P1", "PUMP START"))
        if kind == "plant" and r < 0.012 and idle > 1800:
            ev.append((b, "BH2-P1", "OVERLOAD TRIP"))
            ev.append((b, "BH2-P1", "PUMP STOP"))
            ev.append((b + dt.timedelta(seconds=int(gq.integers(300, int(min(idle - 60, 2400))))), "BH2-P1", "FAULT RESET"))
        elif r < 0.03 and idle > 3 * 3600:
            ev.append((b, "BH2-P1", "PUMP STOP"))
            lost = b + dt.timedelta(seconds=int(gq.integers(600, 3600)))
            back = lost + dt.timedelta(seconds=int(gq.integers(900, int(min(idle - 4200, 4 * 3600)))))
            ev.append((lost, "BH2-OS", "COMMS LOST"))
            ev.append((back, "BH2-OS", "COMMS RESTORED"))
            if gq.random() < 0.5:
                ev.append((b, "BH2-P1", "PUMP STOP"))             # the buffered stop, re-sent with its own time
        else:
            ev.append((b, "BH2-P1", "PUMP STOP"))
    return ev


def write_pump(out, O):
    ev = pump_events(O)
    K.write_csv(os.path.join(out, F_PUMP), ["timestamp", "tag", "event"],
                [[t.strftime("%d/%m/%Y %H:%M:%S"), tag, e] for t, tag, e in ev])
    return len(ev)


def tickets(O):
    """The haulier's tickets as its monthly statements carry them: a ticket number restarting each month, the date
    the night shift began, the times in and out of the bay (local), the litres the tanker's meter gave."""
    g = K.rng("tickets")
    gv = K.rng("ticketbook")
    # the night shift's usual pairings, with the spare tanker and relief drivers now and then
    crews = [("TV21 MBX", "M. Bevan"), ("TV22 LPW", "K. Price"), ("TV23 HDN", "T. Morgan"), ("TV21 MBX", "S. Lloyd")]
    spares = [("TV19 KRA", "G. Pugh"), ("TV19 KRA", "S. Lloyd"), ("TV22 LPW", "D. Rees")]
    rows = []
    bymonth = {}
    for f in sorted(O["fills"], key=lambda x: x["start"]):
        if not (dt.date(2025, 4, 1) <= f["shift_date"] <= K.OPS_TO):
            continue
        k = (f["shift_date"].year, f["shift_date"].month)
        # the haulier's monthly book numbers every load it carries; the gaps are its other customers' loads,
        # wider on busy nights, and the month's first Ferncastle load comes some way into the book
        if k not in bymonth:
            bymonth[k] = int(gv.integers(1, 14))
        else:
            bymonth[k] += 1 + int(gv.geometric(0.45)) - 1 + (int(gv.integers(4, 11)) if gv.random() < 0.08 else 0)
        wait = int(g.integers(4, 9)) + (int(gv.integers(2, 9)) if gv.random() < 0.18 else 0)
        t_in = f["start"] - dt.timedelta(minutes=wait)
        if t_in.date() != f["start"].date():               # a load the pump starts just after midnight is booked in
            since = int((f["start"] - dt.datetime.combine(f["start"].date(), dt.time(0, 0))).total_seconds() // 60)
            t_in = f["start"] - dt.timedelta(minutes=int(gv.integers(0, since + 1)))
        t_out = f["start"] + dt.timedelta(seconds=f["seconds"]) + dt.timedelta(minutes=int(g.integers(5, 11)) +
                                                                                (int(gv.integers(1, 8)) if gv.random() < 0.15 else 0))
        veh, drv = crews[int(g.integers(0, len(crews)))]
        if gv.random() < 0.07:
            veh, drv = spares[int(gv.integers(0, len(spares)))]
        g.integers(0, 5)                                     # keeps the stream aligned with the earlier draw
        rows.append(dict(month=k, no="%04d" % bymonth[k], date=f["shift_date"], t_in=t_in, t_out=t_out,
                         litres=int(f["litres"]), veh=veh, drv=drv, cust=K.BULK_CUSTOMER))
    return rows


def write_tickets(out, O):
    rows = tickets(O)
    g = K.rng("resend")
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    months = sorted({r["month"] for r in rows})
    n = 0
    for k in months:
        ws = wb.create_sheet(dt.date(k[0], k[1], 1).strftime("%b %Y"))
        ws.append([K.HAULIER, "Statement of bulk loads", dt.date(k[0], k[1], 1).strftime("%B %Y")])
        ws.append(["Loading point", "Brackenholt Spring Water, bulk bay"])
        ws.append([])
        ws.append(["Ticket", "Date", "Vehicle", "Time in", "Time out", "Litres", "Customer", "Driver"])
        for c in ws[4]:
            c.font = BOLD
            c.fill = HEAD_FILL
        mr = [r for r in rows if r["month"] == k]
        for r in mr:
            line = [r["no"], r["date"].strftime("%d/%m/%Y"), r["veh"], r["t_in"].strftime("%H:%M"),
                    r["t_out"].strftime("%H:%M"), r["litres"], r["cust"], r["drv"]]
            ws.append(line)
            n += 1
            if g.random() < 0.012:
                ws.append(line)          # a ticket re-sent with the statement's late additions
                n += 1
        ws.append([])
        ws.append(["", "", "", "", "Total", sum(r["litres"] for r in mr)])
        _autosize(ws, [8, 12, 11, 9, 9, 10, 18, 11])
    wb.save(os.path.join(out, F_TICKETS))
    return n


def write_runs(out, O):
    rows = []
    for r in O["runs"]:
        rows.append([r["run"], r["line"], r["sku"], "PROD", r["start"].strftime("%Y-%m-%d %H:%M"),
                     r["end"].strftime("%Y-%m-%d %H:%M"), r["good"], r["reject"]])
    for c in O["cips"]:
        rows.append([c["run"], c["line"], "", "CIP", c["start"].strftime("%Y-%m-%d %H:%M"),
                     c["end"].strftime("%Y-%m-%d %H:%M"), "", ""])
    rows.sort(key=lambda x: (x[4], x[1]))
    K.write_csv(os.path.join(out, F_RUNS), ["order_no", "line", "sku", "order_type", "start_local", "end_local",
                                            "qty_good", "qty_reject"], rows)
    return len(rows)


def write_sku(out):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "SKU"
    ws.append(["Material", "Description", "Pack size (ml)", "Units per case", "Line", "Status"])
    for c in ws[1]:
        c.font = BOLD
        c.fill = HEAD_FILL
    cases = {"BSP-0500": 24, "BSP-0330": 24, "BSP-1500": 6, "BKP-1500": 6, "BSG-1101": 12, "BKG-1102": 12,
             "BSG-1205": 24, "BSP-0750": 12, "BKP-0750": 12}
    for code, (desc, size, line, _, _) in W.SKUS.items():
        if code == "BSG-1101":
            desc, size = "Brackenholt Still 70cl glass", W.SIZE_AFTER
        ws.append([code, desc, size, cases[code], line, "Active"])
    ws.append(["BSG-1100", "Brackenholt Still 1L glass", 1000, 6, "L3", "Discontinued"])
    _autosize(ws, [12, 40, 15, 15, 7, 13])
    wb.save(os.path.join(out, F_SKU))
    return ws.max_row - 1


def write_qc(out, O):
    rows = []
    for q in O["qc"]:
        res = "PASS" if q["net_g"] >= 0.985 * W.size_at(q["sku"], q["t"].date()) else "FAIL"
        rows.append([q["t"].strftime("%d/%m/%Y %H:%M"), q["line"], q["sku"], "%.1f" % q["net_g"], res])
    K.write_csv(os.path.join(out, F_QC), ["sample_time", "line", "material", "net_fill_g", "result"], rows)
    return len(rows)


# ------------------------------------------------------------------------------------------------- distractors
def write_quality(out):
    g = K.rng("quality")
    rows = []
    for y, m in W.month_iter(dt.date(2015, 4, 1), dt.date(2026, 9, 1)):
        d = dt.date(y, m, 1) + dt.timedelta(days=int(g.integers(2, 20)))
        rows.append([d.strftime("%d/%m/%Y"), "BH2 raw", "%.0f" % (612 + g.normal(0, 9)), "%.2f" % (7.32 + g.normal(0, 0.04)),
                     "%.1f" % (8.6 + g.normal(0, 0.4)), "%.1f" % (31.0 + g.normal(0, 1.2)), "%.1f" % (102 + g.normal(0, 3)),
                     "%.2f" % max(0.0, 0.05 + g.normal(0, 0.02)), "<1", "0"])
    K.write_csv(os.path.join(out, F_QUALITY), ["sample_date", "sample_point", "conductivity_uS_cm", "pH",
                                               "nitrate_mg_l", "chloride_mg_l", "calcium_mg_l", "iron_mg_l",
                                               "coliforms_per_100ml", "e_coli_per_100ml"], rows)
    return len(rows)


def write_rain(out):
    g = K.rng("rain")
    rows = []
    d = dt.date(2015, 1, 1)
    while d <= K.OPS_TO:
        wet = 0.52 + 0.12 * math.cos(2 * math.pi * (d.timetuple().tm_yday - 15) / 365.25)
        mm = float(g.gamma(0.75, 4.6)) if g.random() < wet else 0.0
        rows.append([d.strftime("%Y-%m-%d"), "%.1f" % mm])
        d += dt.timedelta(days=1)
    K.write_csv(os.path.join(out, F_RAIN), ["date", "rain_mm_0900"], rows)
    return len(rows)


def write_all(out, O):
    counts = {}
    counts[F_TEST] = write_test(out)
    counts[F_OBS] = write_obs(out, O)
    counts[F_RMB] = write_rmb(out)
    counts[F_SURVEY] = write_survey(out)
    counts[F_TELEM] = write_telemetry(out, O)
    counts[F_PUMP] = write_pump(out, O)
    counts[F_TICKETS] = write_tickets(out, O)
    counts[F_RUNS] = write_runs(out, O)
    counts[F_SKU] = write_sku(out)
    counts[F_QC] = write_qc(out, O)
    counts[F_QUALITY] = write_quality(out)
    counts[F_RAIN] = write_rain(out)
    return counts
