"""The golden, computed from target/ alone (the shipped files, read the way a solver reads them).

The call: a storm overflow breaches condition 2.3.1 when it discharges while its station passes forward less than
the permit's flow. A station passes forward what its running pump delivers, and an unmetered station's delivered
rate is measured from its own wet well: between the duty pump's stop and start levels the wet well holds a fixed
volume, the pump-off time fills it at the inflow, the pump-on time draws it down at the pump's rate less the
inflow, so each cycle gives the pump's rate as volume over on-time plus volume over off-time.

The asks: the return's lines per overflow (12/24 spills, hours of discharge, monitor operational time) and the
hours of discharge in each month, over every monitor that watched the overflow in 2026, one monitor's history
sometimes standing under a serial the asset register no longer lists."""
import csv
import datetime as dt
import math
import os
import re
import sqlite3
from collections import defaultdict

import numpy as np
from openpyxl import load_workbook

T0 = dt.datetime(2026, 1, 1)
BST0 = (dt.datetime(2026, 3, 29, 1) - T0).total_seconds()
BST1 = (dt.datetime(2026, 10, 25, 1) - T0).total_seconds()
YEAR_S = 365 * 86400.0
FILES = {
    "telemetry": "telemetry/marsh_wolds_sps_telemetry_2026.sqlite",
    "edm_log": "edm/edm_discharge_log_2026.csv",
    "edm_status": "edm/edm_monitor_daily_status_2026.csv",
    "edm_list": "edm/edm_monitor_list_2027-01-15.csv",
    "assets": "registers/marsh_wolds_wastewater_assets.xlsx",
    "consents": "registers/wastewater_discharge_consents_2026.csv",
    "meters": "flow/rising_main_flow_meters_2026.csv",
    "rain": "rainfall/radar_rainfall_marsh_wolds_2026.csv",
}


def utc_sec(s):
    return (dt.datetime.strptime(s, "%Y-%m-%d %H:%M:%S") - T0).total_seconds()


def local_to_utc(s):
    """'dd/mm/yyyy HH:MM:SS' UK local time to UTC seconds from 1 January 2026 (the repeated October hour as BST)."""
    t = (dt.datetime.strptime(s, "%d/%m/%Y %H:%M:%S") - T0).total_seconds()
    return t - 3600 if BST0 <= t - 3600 < BST1 else t


def utc_to_local(sec):
    return T0 + dt.timedelta(seconds=sec + (3600 if BST0 <= sec < BST1 else 0))


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


# ---------------------------------------------------------------- registers
def registers(tgt):
    wb = load_workbook(os.path.join(tgt, FILES["assets"]), data_only=True)
    ws = wb["Pumping stations"]
    hdr = [c.value for c in ws[1]]
    stations = {}
    for row in ws.iter_rows(min_row=2, values_only=True):
        r = dict(zip(hdr, row))
        dims = [float(x) for x in re.findall(r"[\d.]+", r["Wet well internal (m)"])]
        area = math.pi * (dims[0] / 2) ** 2 if r["Wet well shape"] == "Circular" else dims[0] * dims[1]
        stations[r["Station code"]] = dict(
            name=r["Station name"].replace(" Pumping Station", ""), rtu=int(str(r["Telemetry RTU"]).split()[1]),
            edm=r["EDM monitor"], edm_installed=r["EDM installed"], zone=r["Radar zone"], area=area,
            floor=float(r["Wet well floor (mAOD)"]), start=float(r["Duty pump start (mAOD)"]),
            stop=float(r["Duty pump stop (mAOD)"]), weir=float(r["Overflow weir (mAOD)"]))
    ws = wb["Pumps"]
    hdr = [c.value for c in ws[1]]
    for row in ws.iter_rows(min_row=2, values_only=True):
        r = dict(zip(hdr, row))
        v = float(r["Duty flow"])
        ls = v / 3.6 if r["Duty flow unit"] == "m3/h" else v
        stations[r["Station code"]].setdefault("rated", {})[int(r["Pump"])] = ls
    ws = wb["Flow meters"]
    hdr = [c.value for c in ws[1]]
    for row in ws.iter_rows(min_row=2, values_only=True):
        r = dict(zip(hdr, row))
        stations[r["Station code"]]["meter"] = r["Meter tag"]
    cons = {}
    for r in read_csv(os.path.join(tgt, FILES["consents"])):
        code = "SPS" + r["site_id"].split("-")[-1]
        cons[code] = dict(permit=r["permit_ref"], pff=float(r["pass_forward_ls"]), text=r["condition_text"],
                          discharge=r["discharge_name"])
    return stations, cons


# ---------------------------------------------------------------- telemetry
def telemetry(tgt):
    con = sqlite3.connect(os.path.join(tgt, FILES["telemetry"]))
    ev = defaultdict(list)
    for rtu, pump, state, ts, lvl in con.execute("SELECT DISTINCT rtu, pump, state, event_utc, wet_well_m FROM pump_event"):
        ev[rtu].append((utc_sec(ts), pump, 1 if state == "RUN" else 0, lvl))
    for k in ev:
        ev[k].sort()
    alarms = defaultdict(list)
    for rtu, a, b in con.execute("SELECT rtu, raised_utc, cleared_utc FROM alarm WHERE alarm='OVERFLOW OPERATING'"):
        alarms[rtu].append((utc_sec(a), utc_sec(b)))
    con.close()
    return ev, alarms


def cycle_rates(events, volume_l, mode="prev"):
    """One estimate per clean duty cycle (a stop, then a start, then that pump's stop): volume over on-time plus
    volume over the off-time before it ("prev") or the mean of the off-times either side ("mean")."""
    out = []
    n = len(events)
    for k in range(1, n - 2):
        t0, p0, s0, _ = events[k - 1]
        t1, p1, s1, _ = events[k]
        t2, p2, s2, _ = events[k + 1]
        if not (s0 == 0 and s1 == 1 and s2 == 0 and p1 == p2):
            continue
        toff, ton = t1 - t0, t2 - t1
        if toff <= 0 or ton <= 0 or toff > 6 * 3600 or ton > 6 * 3600:
            continue
        qin = volume_l / toff
        if mode == "mean":
            t3, p3, s3, _ = events[k + 2]
            if s3 != 1 or t3 - t2 <= 0 or t3 - t2 > 6 * 3600:
                continue
            qin = 0.5 * (volume_l / toff + volume_l / (t3 - t2))
        out.append((t1, p1, volume_l / ton + qin))
    return out


def delivered(stations, ev, estimator="median", mode="prev", night=False, per_pump=False, use_logged=False):
    res = {}
    for code, st in stations.items():
        e = ev[st["rtu"]]
        if use_logged:
            runs = [x[3] for x in e if x[2] == 1]
            stops = [x[3] for x in e if x[2] == 0]
            band = float(np.median(runs)) - float(np.median(stops))
        else:
            band = st["start"] - st["stop"]
        V = st["area"] * band * 1000.0
        rates = cycle_rates(e, V, mode)
        if night:
            rates = [x for x in rates if utc_to_local(x[0]).hour < 5]
        vals = np.array([x[2] for x in rates])
        f = {"median": np.median, "mean": np.mean,
             "trim": lambda a: float(np.mean(np.sort(a)[int(len(a) * 0.1): int(len(a) * 0.9)]))}[estimator]
        if per_pump:
            res[code] = {p: float(f(np.array([x[2] for x in rates if x[1] == p]))) for p in (1, 2)}
        else:
            res[code] = float(f(vals))
    return res


# ---------------------------------------------------------------- event duration monitoring
def edm_records(tgt):
    log = defaultdict(list)
    for r in read_csv(os.path.join(tgt, FILES["edm_log"])):
        log[r["monitor_serial"]].append((local_to_utc(r["discharge_start"]), local_to_utc(r["discharge_end"])))
    status = defaultdict(dict)
    for r in read_csv(os.path.join(tgt, FILES["edm_status"])):
        status[r["monitor_serial"]][dt.datetime.strptime(r["date"], "%d/%m/%Y").date()] = float(r["hours_reporting"])
    mlist = {r["serial"]: r for r in read_csv(os.path.join(tgt, FILES["edm_list"]))}
    return log, status, mlist


def overlap(a, b):
    tot = 0.0
    j = 0
    for (x0, x1) in a:
        for (y0, y1) in b:
            tot += max(0.0, min(x1, y1) - max(x0, y0))
    return tot


def coincide(recs, alarms):
    """How closely a monitor's discharges are a station's overflow alarms: for each discharge, the best
    intersection-over-union with any of the station's alarms, summed over the monitor's discharges."""
    tot = 0.0
    al = sorted(alarms)
    for a, b in recs:
        best = 0.0
        for (x, y) in al:
            if y < a - 3600 or x > b + 3600:
                continue
            inter = max(0.0, min(b, y) - max(a, x))
            uni = max(b, y) - min(a, x)
            if uni > 0:
                best = max(best, inter / uni)
        tot += best
    return round(tot, 3)


def map_monitors(stations, log, mlist, alarms, restrict=True):
    """Every serial to its overflow: the register's monitor where it lists one; a retired serial to the station whose
    telemetry overflow alarms its discharges start with, among the stations whose register monitor was installed in
    the week before the serial retired (restrict=False tries every station)."""
    serial_site = {st["edm"]: code for code, st in stations.items()}
    evidence = {}
    for ser, row in sorted(mlist.items()):
        if ser in serial_site:
            continue
        recs = log.get(ser, [])
        cands = stations.items()
        if restrict and row.get("retired"):
            ret = dt.datetime.strptime(row["retired"], "%d/%m/%Y").date()
            cands = [(c, st) for c, st in stations.items()
                     if hasattr(st["edm_installed"], "year")
                     and 0 <= (ret - (st["edm_installed"].date() if hasattr(st["edm_installed"], "date")
                                      else st["edm_installed"])).days <= 9]
        scores = sorted(((coincide(recs, alarms[st["rtu"]]), code) for code, st in cands), reverse=True)
        serial_site[ser] = scores[0][1]
        evidence[ser] = dict(n_records=len(recs), scores=scores[:4])
    return serial_site, evidence


def union(iv):
    out = []
    for a, b in sorted(iv):
        if out and a <= out[-1][1]:
            out[-1][1] = max(out[-1][1], b)
        else:
            out.append([a, b])
    return [(a, b) for a, b in out]


def count_1224(iv):
    """The procedure's 12/24 method on one overflow's discharges (UTC seconds), counted from discharges that start
    in the reporting year."""
    iv = union(iv)
    n, k = 0, 0
    while k < len(iv):
        start = iv[k][0]
        n += 1
        block_end = start + 12 * 3600.0
        cur = iv[k][1]
        k += 1
        while True:
            while k < len(iv) and iv[k][0] < block_end:
                cur = max(cur, iv[k][1])
                k += 1
            nxt_end = block_end + 24 * 3600.0
            if cur > block_end or (k < len(iv) and iv[k][0] < nxt_end):
                n += 1
                block_end = nxt_end
                continue
            break
    return n


def year_local_bounds():
    lo = 0.0                                         # 00:00 1 Jan local is 00:00 UTC (GMT)
    hi = YEAR_S                                      # 24:00 31 Dec local is 00:00 UTC 1 Jan 2027
    return lo, hi


def returns(stations, log, status, serial_site):
    lo, hi = year_local_bounds()
    by_site = defaultdict(list)
    for ser, recs in log.items():
        site = serial_site.get(ser)
        if site:
            by_site[site].extend(recs)
    lines = {}
    for code in stations:
        iv = [(a, b) for a, b in by_site.get(code, []) if lo <= a < hi]
        u = union(iv)
        hours = sum(min(b, hi) - a for a, b in u) / 3600.0
        months = [0.0] * 12
        for a, b in u:
            t = a
            while t < min(b, hi):
                ld = utc_to_local(t)
                nm = dt.datetime(ld.year + (ld.month == 12), ld.month % 12 + 1, 1)
                # the UTC second at which the local month ends
                nm_utc = (nm - T0).total_seconds()
                nm_utc = nm_utc - 3600 if BST0 <= nm_utc - 3600 < BST1 else nm_utc
                seg_end = min(b, hi, nm_utc)
                months[ld.month - 1] += (seg_end - t) / 3600.0
                t = seg_end
        sers = [s for s, c in serial_site.items() if c == code]
        days = defaultdict(float)
        for s in sers:
            for d, h in status.get(s, {}).items():
                days[d] = max(days[d], h)
        op = sum(min(h, 25.0) for d, h in days.items() if d.year == 2026) / 8760.0 * 100.0
        lines[code] = dict(spills=count_1224(iv), hours=hours, months=months, operational=op, serials=sorted(sers))
    return lines


# ---------------------------------------------------------------- the call
def compute(tgt):
    stations, cons = registers(tgt)
    ev, alarms = telemetry(tgt)
    log, status, mlist = edm_records(tgt)
    serial_site, evidence = map_monitors(stations, log, mlist, alarms)
    dlv = delivered(stations, ev)
    lines = returns(stations, log, status, serial_site)
    pff = {c: cons[c]["pff"] for c in stations}
    spilled = {c: lines[c]["spills"] > 0 for c in stations}
    breach = sorted(c for c in stations if spilled[c] and dlv[c] < pff[c])
    margin = {c: dlv[c] / pff[c] for c in stations}
    compliant = [c for c in stations if c not in breach]
    tight = min(compliant, key=lambda c: margin[c])
    call_code = breach[0] if len(breach) == 1 else None
    g = dict(stations=stations, cons=cons, delivered=dlv, pff=pff, margin=margin, breach=breach, lines=lines,
             serial_site=serial_site, evidence=evidence, call_code=call_code,
             call=(cons[call_code]["discharge"] if call_code else "none"), tightest=tight,
             events=ev, alarms=alarms, log=log, status=status, mlist=mlist)
    return g
