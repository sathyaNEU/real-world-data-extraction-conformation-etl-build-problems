"""An independent recomputation of task398 from target/ alone: it imports nothing from the generator, parses every
file itself and uses its own constructions (the nearest entry to the intake for the attribution, interval
integration for the carbon, a rain-free step search for the logger), then compares with figures.json.
Usage: python3 verify.py [target]"""
import csv
import datetime as dt
import json
import math
import os
import sys
from collections import defaultdict

import numpy as np
import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
T = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")
F = json.load(open(os.path.join(HERE, "figures.json")))
NAMES = {"TES": "Tessel River", "FEN": "Fennick Creek", "OXL": "Oxley Creek", "DUN": "Dunmore Creek",
         "LAD": "Ladd Branch"}
FAILS = []


def say(name, ok, got=None, want=None):
    print("%s  %s%s" % ("ok  " if ok else "FAIL", name, "" if ok else "  got %r want %r" % (got, want)))
    if not ok:
        FAILS.append(name)


def p(rel):
    return os.path.join(T, rel)


def dst(t):          # local daylight time in force, 2026
    return dt.datetime(2026, 3, 8, 2) <= t < dt.datetime(2026, 11, 1, 2)


def from_utc(t):
    loc = t - dt.timedelta(hours=5)
    return loc if dst(loc) else t - dt.timedelta(hours=6)


def from_cst(t):
    return from_utc(t + dt.timedelta(hours=6))


# ---------------------------------------------------------------- the day's result (SOP-WQ-07 2.3) and the season
screen, conf = {}, {}
for r in csv.DictReader(open(p("plant/raw_water_log_2026-01-01_to_2026-05-26.csv"), encoding="utf-8")):
    d = dt.datetime.strptime(r["Date"], "%m/%d/%Y").date()
    if r["Atrazine ELISA (ppb)"]:
        screen[d] = float(r["Atrazine ELISA (ppb)"])
    if r["Atrazine GC/MS SHL (ug/L)"]:
        conf[d] = float(r["Atrazine GC/MS SHL (ug/L)"])
wb = openpyxl.load_workbook(p("plant/LIMS_raw_water_2026-05-20_to_2026-10-31.xlsx"), read_only=True)
for row in wb.worksheets[0].iter_rows(min_row=2, values_only=True):
    if not row[0]:
        continue
    d = dt.datetime.strptime(row[2], "%m/%d/%Y %H:%M").date()
    if row[3] == "Atrazine (screen)":
        screen[d] = float(row[4])
    elif row[3] == "Atrazine (confirmation)":
        conf[d] = float(row[4])
result = {d: conf.get(d, screen.get(d)) for d in set(screen) | set(conf)}
days = sorted(d for d, v in result.items() if dt.date(2026, 4, 15) <= d <= dt.date(2026, 10, 31) and v > 3.0)
say("days above the trigger", len(days) == F["days_total"], len(days), F["days_total"])

# ---------------------------------------------------------------- the lake: profiles and the intake's depth
rehang = None
for r in csv.DictReader(open(p("lake/buoy_service_log_2026.csv"), encoding="utf-8")):
    if r["Action"].startswith("Logging restarted") and "1.0 m" in r["Notes"]:
        rehang = dt.datetime.strptime(r["Date"] + " " + r["Time (CST)"], "%Y-%m-%d %H:%M")
acc = defaultdict(lambda: defaultdict(list))
lines = open(p("lake/MERRIN_BUOY_Hourly_2026.dat"), encoding="ascii").read().splitlines()
for ln in lines[4:]:
    f = [x.strip('"') for x in ln.split(",")]
    t = dt.datetime.strptime(f[0], "%Y-%m-%d %H:%M:%S")
    top = 0.5 if t < rehang else 1.0
    day = from_cst(t).date()
    for n, v in enumerate(f[4:20]):
        if v != "NAN":
            acc[day][top + n].append(float(v))
prof = {d: (np.array(sorted(z)), np.array([np.mean(z[k]) for k in sorted(z)])) for d, z in acc.items()}
wb = openpyxl.load_workbook(p("lake/merrin_dam_daily_log_2026.xlsx"), read_only=True)
pool = {}
for row in wb.worksheets[0].iter_rows(min_row=3, values_only=True):
    if row[0] and row[1] is not None:
        pool[dt.date.fromisoformat(row[0])] = float(row[1])
intake_ngvd = 829.24 - 0.24                     # sheet S-4: NAVD88 centreline, NAVD88 = NGVD29 + 0.24 ft
zi = {d: (e - intake_ngvd) * 0.3048 for d, e in pool.items()}


def entry(d, temp):
    z, v = prof[d]
    if temp >= v[0]:
        return 0.0
    if temp < v[-1]:
        return None
    for i in range(len(z) - 1):
        if v[i] >= temp >= v[i + 1]:
            return float(z[i] + (z[i + 1] - z[i]) * (v[i] - temp) / max(v[i] - v[i + 1], 1e-9))
    return None


def daily_temps():
    out = {}
    for k, fn in (("TES", "hydro/TR-01_tessel_r_halvard_br_2026.csv"), ("FEN", "hydro/FC-02_fennick_cr_cr_w38_2026.csv"),
                  ("OXL", "hydro/OC-03_oxley_cr_lisle_2026.csv")):
        a = defaultdict(list)
        rows = [ln for ln in open(p(fn), encoding="utf-8") if not ln.startswith("#")]
        for r in csv.DictReader(rows):
            if r["water_temp_c"]:
                a[r["datetime_local"][:10]].append(float(r["water_temp_c"]))
        out[k] = {dt.date.fromisoformat(d): float(np.mean(v)) for d, v in a.items()}
    for k, fn in (("DUN", "hydro/DC-04_logger_2087445_2026.csv"), ("LAD", "hydro/LB-05_logger_2087519_2026.csv")):
        a = defaultdict(list)
        ls = open(p(fn), encoding="utf-8").read().splitlines()
        for ln in ls[ls.index("Date,Time,ms,LEVEL,TEMPERATURE") + 1:]:
            d_, t_, ms, lv, tc = ln.split(",")
            a[from_utc(dt.datetime.strptime(d_ + " " + t_, "%Y/%m/%d %H:%M:%S")).date()].append(float(tc))
        out[k] = {d: float(np.mean(v)) for d, v in a.items()}
    return out


TT = daily_temps()
strat = sorted(d for d, (z, v) in prof.items() if v[0] - v[-1] >= 1.0 and d.month in range(4, 11))
onset = strat[0]
say("stratified from", onset.isoformat() == F["strat_first"], onset.isoformat(), F["strat_first"])
# the attribution, by its own route: on each day above the trigger, the sub-watershed whose water came nearest the
# intake's depth on that day or a stratified day before it in the last 30
count = defaultdict(int)
for d in days:
    best = None
    for n in range(31):
        dd = d - dt.timedelta(days=n)
        if dd < onset or dd not in prof or dd not in zi:
            continue
        for k in NAMES:
            if dd not in TT[k]:
                continue
            z = entry(dd, TT[k][dd])
            if z is None:
                continue
            gap = abs(z - zi[dd])
            if best is None or gap < best[0]:
                best = (gap, k)
    count[best[1]] += 1
for k, name in NAMES.items():
    say("days caused, %s" % name, count[k] == F["per_sub"][name], count[k], F["per_sub"][name])
say("the call", max(count, key=count.get) == {v: k for k, v in NAMES.items()}[F["call"]], max(count, key=count.get),
    F["call"])

# ---------------------------------------------------------------- station atrazine by month
site_k = {"TES-HB": "TES", "FEN-38": "FEN", "OXL-LS": "OXL", "DUN-230": "DUN", "LAD-MP": "LAD"}
stn_k = {"TR-01": "TES", "FC-02": "FEN", "OC-03": "OXL", "DC-04": "DUN", "LB-05": "LAD"}
wb = openpyxl.load_workbook(p("lab/field_sampling_log_2026.xlsx"), read_only=True)
bot, carousel = {}, defaultdict(list)
for row in wb.worksheets[0].iter_rows(min_row=2, values_only=True):
    if not row[0]:
        continue
    t = dt.datetime.strptime(row[2] + " " + row[3], "%m/%d/%Y %H:%M")
    bid = row[0].replace("-", "")
    bot[bid] = [site_k[row[1]], t]
    if "ISCO" in str(row[4]):
        carousel[(site_k[row[1]], t)].append(bid)
pos = defaultdict(list)
for r in csv.DictReader(open(p("lab/autosampler_run_logs_2026.csv"), encoding="utf-8")):
    if r["Status"] == "OK":
        pos[(stn_k[r["Station"]], dt.datetime.strptime(r["Carousel removed"], "%Y-%m-%d %H:%M"))].append(
            (int(r["Bottle position"]), dt.datetime.strptime(r["Sample time"], "%Y-%m-%d %H:%M")))
for key, ids in carousel.items():
    for bid, (n, ft) in zip(sorted(ids), sorted(pos[key])):
        bot[bid][1] = ft
val = {}
wb = openpyxl.load_workbook(p("lab/city_lab_ELISA_tributaries_2026.xlsx"), read_only=True)
for row in wb.worksheets[0].iter_rows(min_row=2, values_only=True):
    if row[0]:
        val[row[1].replace("-", "")] = 0.0 if str(row[5]).startswith("<") else float(row[5])
for r in csv.DictReader(open(p("lab/SHL_EDD_brennick_source_water_2026.csv"), encoding="utf-8")):
    if r["Analyte"] == "Atrazine":
        val[r["Client_Sample_ID"]] = 0.0 if r["Qualifier"] == "U" else float(r["Result"])
samples = defaultdict(list)
for bid, (k, t) in bot.items():
    if bid in val:
        samples[k].append((t, val[bid]))


def flows_station(fn):
    ts, q = [], []
    rows = [ln for ln in open(p(fn), encoding="utf-8") if not ln.startswith("#")]
    for r in csv.DictReader(rows):
        ts.append(dt.datetime.strptime(r["datetime_local"], "%Y-%m-%d %H:%M"))
        q.append(float(r["discharge_cfs"]) if r["discharge_cfs"] else float("nan"))
    return ts, np.array(q)


def flows_dc04():
    wb = openpyxl.load_workbook(p("hydro/DC-04_LB-05_ratings_and_field_visits.xlsx"), read_only=True)
    ratings, vis = [], []
    for ws in wb.worksheets:
        rows = list(ws.iter_rows(values_only=True))
        if ws.title.startswith("DC-04 rating"):
            eff = dt.datetime.strptime(rows[1][1][:16], "%Y-%m-%d %H:%M")
            h = np.array([r[0] for r in rows[4:] if r and r[0] is not None], dtype=float)
            qq = np.array([r[1] for r in rows[4:] if r and r[0] is not None], dtype=float)
            ratings.append((eff, h, qq))
        elif ws.title == "Field visits":
            for r in rows[1:]:
                if r[0] == "DC-04":
                    vis.append((dt.datetime.strptime(r[1] + " " + r[2], "%Y-%m-%d %H:%M"), float(r[3]) - float(r[4])))
    ratings.sort()
    ls = open(p("hydro/DC-04_logger_2087445_2026.csv"), encoding="utf-8").read().splitlines()
    ts, lev = [], []
    for ln in ls[ls.index("Date,Time,ms,LEVEL,TEMPERATURE") + 1:]:
        d_, t_, ms, lv, tc = ln.split(",")
        ts.append(from_utc(dt.datetime.strptime(d_ + " " + t_, "%Y/%m/%d %H:%M:%S")))
        lev.append(float(lv))
    lev = np.array(lev)
    # the visits fall into hangs of the logger; the hang changes at the one rain-free jump in the level between the
    # two visits that disagree
    rain = {}
    for ln in open(p("lake/merrin_dam_precip_daily_2026.txt"), encoding="utf-8"):
        f = ln.split()
        if len(f) >= 2 and f[0][:4] == "2026":
            try:
                rain[dt.date.fromisoformat(f[0])] = float(f[1])
            except ValueError:
                pass
    vis.sort()
    cut = None
    for (t0, o0), (t1, o1) in zip(vis, vis[1:]):
        if abs(o1 - o0) > 0.05:
            d = np.diff(lev)
            cand = [(abs(d[i - 1]), i) for i in range(1, len(ts)) if t0 < ts[i] < t1 and rain.get(ts[i].date(), 0) == 0]
            cut = ts[max(cand)[1]]
    early = np.mean([o for t, o in vis if cut is None or t < cut])
    late = np.mean([o for t, o in vis if cut is not None and t >= cut]) if cut else early
    q = []
    for t, lv in zip(ts, lev):
        h = lv + (early if cut is None or t < cut else late)
        eff, hh, qq = [r for r in ratings if r[0] <= t][-1] if any(r[0] <= t for r in ratings) else ratings[0]
        q.append(0.0 if h <= hh[0] else float(np.interp(h, hh, qq)))
    return ts, np.array(q), cut, (round(early, 2), round(late, 2))


FLOW = {"TES": flows_station("hydro/TR-01_tessel_r_halvard_br_2026.csv"),
        "FEN": flows_station("hydro/FC-02_fennick_cr_cr_w38_2026.csv"),
        "OXL": flows_station("hydro/OC-03_oxley_cr_lisle_2026.csv")}
ts_d, q_d, cut, offs = flows_dc04()
FLOW["DUN"] = (ts_d, q_d)
say("DC-04 offsets", list(offs) == F["dun_offsets_ft"], offs, F["dun_offsets_ft"])
say("DC-04 hang change", cut is not None and cut.isoformat() == F["dun_step_at"], cut, F["dun_step_at"])
MN = {4: "April", 5: "May", 6: "June", 7: "July"}
for k in ("TES", "FEN", "OXL", "DUN"):
    sm = sorted(samples[k])
    ref = dt.datetime(2026, 1, 1)
    sx = np.array([(t - ref).total_seconds() for t, _ in sm])
    sv = np.array([v for _, v in sm])
    ts, q = FLOW[k]
    x = np.array([(t - ref).total_seconds() for t in ts])
    c = np.interp(x, sx, sv)
    kg = q * c * 28.316846592 * 900.0 / 1e9
    for m, name in MN.items():
        inm = np.array([t.month == m for t in ts])
        v = int(round(float(np.nansum(kg[inm]))))
        want = F["loads_month_kg"][NAMES[k]][name]
        say("atrazine %s %s" % (NAMES[k], name), v == want, v, want)
say("Ladd Branch not sampled", not samples["LAD"], len(samples["LAD"]), 0)

# ---------------------------------------------------------------- carbon, by interval integration
sp = []
for r in csv.DictReader(open(p("plant/scada_pac_dose_setpoint_2026.csv"), encoding="utf-8")):
    sp.append((from_utc(dt.datetime.strptime(r["Timestamp (UTC)"], "%Y-%m-%d %H:%M")), float(r["Value"])))
sp.sort()
ev = []
for r in csv.DictReader(open(p("plant/scada_alarm_event_history_2026.csv"), encoding="utf-8")):
    if r["Tag"] == "PAC-FDR-1" and r["Description"] in ("RUN STATUS ON", "RUN STATUS OFF", "HOPPER LEVEL LOW-LOW NO FEED"):
        ev.append((from_utc(dt.datetime.strptime(r["Time (UTC)"], "%Y-%m-%d %H:%M")), r["Description"], r["Type"]))
wb = openpyxl.load_workbook(p("plant/daily_operating_report_2026.xlsx"), read_only=True)
mg = {}
for row in wb.worksheets[0].iter_rows(min_row=2, values_only=True):
    if row[0]:
        mg[dt.date.fromisoformat(row[0])] = float(row[1])
# change points: setpoints, feeder state, plant-day starts (06:00), month starts
pts = set(t for t, _ in sp) | set(t for t, _, _ in ev)
d0 = sp[0][0].date()
while d0 <= dt.date(2026, 10, 31):
    pts.add(dt.datetime.combine(d0, dt.time(6)))
    pts.add(dt.datetime.combine(d0, dt.time(0)))
    d0 += dt.timedelta(days=1)
pts = sorted(t for t in pts if t >= sp[0][0])
lb = defaultdict(float)
dose, running, empty = 0.0, False, False
si = ei = 0
for a, b in zip(pts, pts[1:]):
    while si < len(sp) and sp[si][0] <= a:
        dose = sp[si][1]
        si += 1
    while ei < len(ev) and ev[ei][0] <= a:
        t_, d_, ty = ev[ei]
        if d_ == "RUN STATUS ON":
            running = True
        elif d_ == "RUN STATUS OFF":
            running = False
        elif ty == "ALM":
            empty = True
        elif ty == "RTN":
            empty = False
        ei += 1
    if dose > 0 and running and not empty:
        rate = mg[(a - dt.timedelta(hours=6)).date()]
        lb[a.month] += dose * rate * 8.34 * (b - a).total_seconds() / 86400.0
for m, name in ((5, "May"), (6, "June"), (7, "July"), (8, "August")):
    v = int(round(lb[m]))
    say("carbon %s" % name, v == F["pac_lb"][name], v, F["pac_lb"][name])
print("%d failed" % len(FAILS))
sys.exit(1 if FAILS else 0)
