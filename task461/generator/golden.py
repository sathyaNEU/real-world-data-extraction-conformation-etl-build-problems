"""The goldens computed from the shipped pack alone, and the wrong rungs on the same records (checks.py and ceiling.py
price them): the base building's monthly electricity and the KPI, the generator's diesel by quarter, the chillers'
refrigerant."""
import bisect
import csv
import datetime as dt
import os
from collections import defaultdict

import openpyxl

import world as W

D = dt.timedelta
MONTHS = [dt.datetime(2026, m, 1) for m in range(1, 13)] + [dt.datetime(2027, 1, 1)]
QUARTERS = [dt.datetime(2026, 1, 1), dt.datetime(2026, 4, 1), dt.datetime(2026, 7, 1), dt.datetime(2026, 10, 1),
            dt.datetime(2027, 1, 1)]


def _csv(target, key):
    with open(os.path.join(target, W.FILES[key]), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


# ------------------------------------------------------------------------------------------------ readers
def hh_monthly(target):
    out = defaultdict(float)
    for r in _csv(target, "hh"):
        d = dt.datetime.strptime(r["SETTLEMENT_DATE"], "%d/%m/%Y")
        out[d.month] += float(r["IMPORT_KWH"])
    return out


def register(target):
    wb = openpyxl.load_workbook(os.path.join(target, W.FILES["register"]), read_only=True)
    rows = list(wb["Meters"].iter_rows(values_only=True))
    head = rows[0]
    return [dict(zip(head, r)) for r in rows[1:] if r and r[0] and str(r[0]).startswith("EM-")]


def bms(target):
    """{tag: [(local timestamp, kWh register)]} in file order (the autumn hour's two passes in the order logged)."""
    out = defaultdict(list)
    for r in _csv(target, "bms"):
        v = float(r["Value"]) / (1000.0 if r["Units"] == "Wh" else 1.0)
        out[r["Point"]].append((dt.datetime.strptime(r["Timestamp"], "%d/%m/%Y %H:%M"), v))
    return out


def reading_at(series, when):
    for t, v in series:
        if t == when:
            return v
    return None


def meter_energy(series, a, b):
    """kWh between two local midnights from the cumulative register (the first logged pass of each stamp)."""
    va, vb = reading_at(series, a), reading_at(series, b)
    return vb - va


def supply_energy(regs, tag, a, b):
    if tag == "EM-110":                                     # replaced on 18 August under EM-118
        swap = W.REPLACED[2]
        if b <= swap:
            return meter_energy(regs["EM-110"], a, b)
        if a >= swap:
            return meter_energy(regs["EM-118"], a, b)
        last_old = regs["EM-110"][-1][1]
        return (last_old - reading_at(regs["EM-110"], a)) + reading_at(regs["EM-118"], b)
    return meter_energy(regs[tag], a, b)


def tenancy_meters(target):
    return [m for m in register(target) if m["Recharged to occupier"] == "Yes" and m["Meter"] != "EM-118"]


def nested_rooms(target, regs=None):
    """The tenancy meters whose half-hours sit inside another tenancy meter's: never above it, and at zero whenever
    that meter was (the June isolations). The golden's hierarchy, read from the registers alone."""
    regs = regs or bms(target)
    tags = [m["Meter"] for m in tenancy_meters(target)]

    def increments(tag):
        s = regs[tag] if tag != "EM-110" else regs["EM-110"] + [(t, v + regs["EM-110"][-1][1])
                                                                 for t, v in regs["EM-118"][1:]]
        return {s[i][0]: s[i + 1][1] - s[i][1] for i in range(len(s) - 1) if s[i + 1][0] - s[i][0] == D(minutes=30)}
    inc = {t: increments(t) for t in tags}
    out = {}
    for c in tags:
        for p in tags:
            if c == p:
                continue
            common = [k for k in inc[c] if k in inc[p]]
            inside = all(inc[c][k] <= inc[p][k] + 0.05 for k in common)
            dark = [k for k in common if inc[p][k] < 0.01]
            with_parent = bool(dark) and all(inc[c][k] < 0.01 for k in dark)
            if inside and with_parent:
                out[c] = p
    return out


# ------------------------------------------------------------------------------------------------ the main call
def base_building(target, mode="golden"):
    """Monthly base building kWh. mode: golden (each tenancy supply once), all (every tenancy meter in the register,
    rooms included), names (every meter named a comms, server or equipment room left out)."""
    imp = hh_monthly(target)
    regs = bms(target)
    meters = tenancy_meters(target)
    if mode == "golden":
        nested = nested_rooms(target, regs)
        meters = [m for m in meters if m["Meter"] not in nested]
    elif mode == "names":
        meters = [m for m in meters if not any(w in m["Description"].lower() for w in ("comms", "server", "equipment"))]
    out = {}
    for i in range(12):
        a, b = MONTHS[i], MONTHS[i + 1]
        sub = sum(supply_energy(regs, m["Meter"], a, b) for m in meters)
        out[i + 1] = imp[i + 1] - sub
    return out


def kpi(monthly):
    kwh = sum(monthly.values())
    t = kwh * W.FACTOR_KG_PER_KWH / 1000.0
    k = kwh * W.FACTOR_KG_PER_KWH / W.NLA_M2
    return dict(mwh=kwh / 1000.0, scope2_t=t, kpi=k, margin=k - W.TARGET_KG_M2, missed=k > W.TARGET_KG_M2)


# ------------------------------------------------------------------------------------------------ diesel
def calibration(target):
    wb = openpyxl.load_workbook(os.path.join(target, W.FILES["calib"]), read_only=True)
    rows = [r for r in wb["DT-1"].iter_rows(values_only=True)][1:]
    return [(float(r[0]), float(r[1])) for r in rows if isinstance(r[0], (int, float))]


def litres_at(cal, mm):
    xs = [c[0] for c in cal]
    i = min(max(bisect.bisect_right(xs, mm) - 1, 0), len(cal) - 2)
    (x0, y0), (x1, y1) = cal[i], cal[i + 1]
    return y0 + (y1 - y0) * (mm - x0) / (x1 - x0)


def diesel_records(target):
    cal = calibration(target)
    dips = [(dt.datetime.strptime(r["dip_date"] + " " + r["dip_time"], "%d/%m/%Y %H:%M"),
             litres_at(cal, float(r["product_mm"]))) for r in _csv(target, "dips")]
    dlv = [(dt.datetime.strptime(r["delivery_date"] + " " + r["delivery_time"], "%d/%m/%Y %H:%M"),
            float(r["litres"])) for r in _csv(target, "dockets")]
    ev = _csv(target, "runs")
    runs, start = [], None
    for r in ev:
        t = dt.datetime.strptime(r["event_time"], "%d/%m/%Y %H:%M:%S")
        if r["event"] == "ENGINE START":
            start = t
        elif r["event"] == "ENGINE STOP":
            runs.append((start, t))
    return sorted(dips), sorted(dlv), runs


def stock_at(target, when, mode="runs", recs=None):
    """Litres in DT-1 at a local instant. mode: runs (the bracket's burn placed on the generator's runs, the golden),
    linear (straight line between the bracketing dips), nearest (the nearer dip)."""
    dips, dlv, runs = recs or diesel_records(target)
    i = bisect.bisect_right([d[0] for d in dips], when) - 1
    (t0, s0), (t1, s1) = dips[i], dips[i + 1]
    added = sum(v for t, v in dlv if t0 < t <= t1)
    before = sum(v for t, v in dlv if t0 < t <= when)
    burn = s0 + added - s1
    if mode == "nearest":
        return s0 + before if (when - t0) <= (t1 - when) else s1 - (added - before)
    if mode == "linear":
        f = (when - t0) / (t1 - t0)
        return s0 + before - f * burn
    inside = [(a, b) for a, b in runs if a < t1 and b > t0]
    hours = sum((min(b, t1) - max(a, t0)).total_seconds() for a, b in inside)
    done = sum((min(b, when) - max(a, t0)).total_seconds() for a, b in inside if a < when)
    return s0 + before - (burn * done / hours if hours else 0.0)


def diesel_quarters(target, mode="runs"):
    recs = diesel_records(target)
    dlv = recs[1]
    out = {}
    for q in range(4):
        a, b = QUARTERS[q], QUARTERS[q + 1]
        delivered = sum(v for t, v in dlv if a <= t < b)
        out[q + 1] = stock_at(target, a, mode, recs) + delivered - stock_at(target, b, mode, recs)
    return out


# ------------------------------------------------------------------------------------------------ refrigerant
def recovery(target):
    wb = openpyxl.load_workbook(os.path.join(target, W.FILES["recovery"]), read_only=True)
    rows = list(wb["Recovery 2026"].iter_rows(values_only=True))
    head = rows[0]
    return [dict(zip(head, r)) for r in rows[1:] if r and r[0]]


def refrigerant(target, mode="golden"):
    """kg released per chiller. mode: golden (added less recovered, joined by job), added (every kilogram the F-gas
    log shows added), topups (the re-tube recharges left out)."""
    log = _csv(target, "fgas")
    rec = defaultdict(float)
    for r in recovery(target):
        rec[r["Job"]] += float(r["Recovered (kg)"])
    out = defaultdict(float)
    for r in log:
        kg = float(r["kg_added"]) if r["kg_added"] else 0.0
        if mode == "topups" and r["activity"].startswith("Recharge"):
            continue
        out[r["plant"]] += kg
        if mode == "golden":
            out[r["plant"]] -= rec.get(r["job_ref"], 0.0) if r["activity"].startswith("Recharge") else 0.0
    return dict(out)


def compute(target):
    monthly = base_building(target)
    k = kpi(monthly)
    dq = diesel_quarters(target)
    rf = refrigerant(target)
    return dict(monthly=monthly, kpi=k, diesel=dq, refrigerant=rf, nested=nested_rooms(target),
                rungs={m: kpi(base_building(target, m)) for m in ("all", "names")})
