"""The golden, computed from the pack under target/ alone (no generator state).

The call: the plant's raw-water days above the 3.0 ug/L trigger in the 15 April to 31 October season (SOP-WQ-07
2.3, plan 5.2), and for each sub-watershed the days the raw water would have stayed at or below the trigger without
its atrazine (plan 5.1). Each tributary's water enters the summer lake at the depth where the lake, read from the dam
buoy's thermistor string, is as warm as the tributary's daily mean water temperature; the intake draws the layer at
its own depth below the day's water surface; a sub-watershed's atrazine is in the water the intake drew on a day only
if its water entered within the intake's layer on some day in the weeks before. The asks: each sub-watershed's April
to September atrazine at its station, and the carbon fed by month."""
import csv
import datetime as dt
import math
import os
import re
from collections import defaultdict

import numpy as np
import openpyxl

SUBS = ["TES", "FEN", "OXL", "DUN", "LAD"]
NAME = dict(TES="Tessel River", FEN="Fennick Creek", OXL="Oxley Creek", DUN="Dunmore Creek", LAD="Ladd Branch")
STATION_FILE = dict(TES="hydro/TR-01_tessel_r_halvard_br_2026.csv", FEN="hydro/FC-02_fennick_cr_cr_w38_2026.csv",
                    OXL="hydro/OC-03_oxley_cr_lisle_2026.csv", DUN="hydro/DC-04_logger_2087445_2026.csv",
                    LAD="hydro/LB-05_logger_2087519_2026.csv")
SITE = dict(TES="TES-HB", FEN="FEN-38", OXL="OXL-LS", DUN="DUN-230", LAD="LAD-MP")
TRIGGER = 3.0
SEASON = (dt.date(2026, 4, 15), dt.date(2026, 10, 31))
LOAD_WINDOW = (dt.datetime(2026, 4, 1, 0, 0), dt.datetime(2026, 8, 1, 0, 0))
FT = 0.3048
CFS_L = 28.316846592          # litres per cubic foot
INTAKE_NAVD = 829.24
NAVD_MINUS_NGVD = 0.24


def p(target, rel):
    return os.path.join(target, rel)


def utc_to_local(t):
    if dt.datetime(2026, 3, 8, 8, 0) <= t < dt.datetime(2026, 11, 1, 7, 0):
        return t - dt.timedelta(hours=5)
    return t - dt.timedelta(hours=6)


def cst_to_local(t):
    return utc_to_local(t + dt.timedelta(hours=6))


# ------------------------------------------------------------------ the plant's day results (SOP-WQ-07 2.3)
def day_results(target):
    screen, conf = {}, {}
    with open(p(target, "plant/raw_water_log_2026-01-01_to_2026-05-26.csv"), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            d = dt.datetime.strptime(r["Date"], "%m/%d/%Y").date()
            if r["Atrazine ELISA (ppb)"]:
                screen[d] = float(r["Atrazine ELISA (ppb)"])
            if r["Atrazine GC/MS SHL (ug/L)"]:
                conf[d] = float(r["Atrazine GC/MS SHL (ug/L)"])
    wb = openpyxl.load_workbook(p(target, "plant/LIMS_raw_water_2026-05-20_to_2026-10-31.xlsx"), read_only=True)
    ws = wb["Export"]
    temp = {}
    for row in ws.iter_rows(min_row=2, values_only=True):
        sid, pt, coll, an, res, units = row[:6]
        d = dt.datetime.strptime(coll, "%m/%d/%Y %H:%M").date()
        if an == "Atrazine (screen)":
            screen[d] = float(res)
        elif an == "Atrazine (confirmation)":
            conf[d] = float(res)
        elif an == "Temperature":
            temp[d] = float(res)
    out = {}
    for d in sorted(set(screen) | set(conf)):
        out[d] = conf.get(d, screen.get(d))
    return out, screen, conf


def days_above(results):
    return sorted(d for d, v in results.items() if SEASON[0] <= d <= SEASON[1] and v > TRIGGER)


# ------------------------------------------------------------------ the tributaries
def station_series(target, k, offsets=None):
    """Local 15-minute times, discharge (cfs) and water temperature (C). `offsets` replaces the loggers' offsets
    (the asks' alternative handlings)."""
    if k in ("TES", "FEN", "OXL"):
        ts, q, tc = [], [], []
        with open(p(target, STATION_FILE[k]), encoding="utf-8") as fh:
            lines = [ln for ln in fh if not ln.startswith("#")]
        for r in csv.DictReader(lines):
            t = dt.datetime.strptime(r["datetime_local"], "%Y-%m-%d %H:%M")
            ts.append(t)
            q.append(float(r["discharge_cfs"]) if r["discharge_cfs"] else float("nan"))
            tc.append(float(r["water_temp_c"]) if r["water_temp_c"] else float("nan"))
        return ts, np.array(q), np.array(tc)
    ratings = read_ratings(target)
    segs = (offsets or logger_offset(target))[k]
    if callable(segs):
        ts, lev, tc = logger_levels(target, k)
        return ts, np.array([rated_flow(ratings, k, loc, h + segs(loc)) for loc, h in zip(ts, lev)]), np.array(tc)
    ts, lev, tc = logger_levels(target, k)
    q = []
    for loc, h in zip(ts, lev):
        off = [o for t0, o in segs if t0 is None or t0 <= loc][-1]
        q.append(rated_flow(ratings, k, loc, h + off))
    return ts, np.array(q), np.array(tc)


def logger_levels(target, k):
    """A logger's readings: local times, level (ft) and water temperature (C), from its UTC record."""
    with open(p(target, STATION_FILE[k]), encoding="utf-8") as fh:
        lines = fh.read().splitlines()
    start = lines.index("Date,Time,ms,LEVEL,TEMPERATURE")
    ts, lev, tc = [], [], []
    for ln in lines[start + 1:]:
        d, t, ms, lv, tmp = ln.split(",")
        ts.append(utc_to_local(dt.datetime.strptime(d + " " + t, "%Y/%m/%d %H:%M:%S")))
        lev.append(float(lv))
        tc.append(float(tmp))
    return ts, np.array(lev), np.array(tc)


def read_ratings(target):
    wb = openpyxl.load_workbook(p(target, "hydro/DC-04_LB-05_ratings_and_field_visits.xlsx"), read_only=True)
    out = defaultdict(list)
    for ws in wb.worksheets:
        if "rating" not in ws.title:
            continue
        rows = list(ws.iter_rows(values_only=True))
        st = rows[0][1]
        k = {"DC-04": "DUN", "LB-05": "LAD"}[st]
        eff = rows[1][1]
        sup = rows[1][4]

        def parse(s):
            if not s:
                return None
            t = dt.datetime.strptime(s[:16], "%Y-%m-%d %H:%M")
            return t
        table = [(float(r[0]), float(r[1])) for r in rows[4:] if r and r[0] is not None]
        out[k].append((parse(eff), parse(sup), np.array([a for a, _ in table]), np.array([b for _, b in table])))
    return out


def logger_offset(target):
    """Gage height minus the logger's level reading, by period. Each field visit sets the staff gage against the
    logger's level; where two visits in a row disagree by more than a few hundredths, the logger moved between them,
    and it moved at the one step in its record that no flow explains: a jump of a tenth of a foot or more between
    two readings with the level otherwise steady for the hour on either side. Within a period the offset is the mean of its
    visits. Returns, per station, [(from local time or None, offset ft), ...]."""
    wb = openpyxl.load_workbook(p(target, "hydro/DC-04_LB-05_ratings_and_field_visits.xlsx"), read_only=True)
    acc = defaultdict(list)
    for row in wb["Field visits"].iter_rows(min_row=2, values_only=True):
        if row[0] is None:
            continue
        k = {"DC-04": "DUN", "LB-05": "LAD"}[row[0]]
        t = dt.datetime.strptime(row[1] + " " + row[2], "%Y-%m-%d %H:%M")
        acc[k].append((t, float(row[3]) - float(row[4])))
    out = {}
    for k, vs in acc.items():
        vs.sort()
        cuts = []
        for (t0, o0), (t1, o1) in zip(vs, vs[1:]):
            if abs(o1 - o0) > 0.05:
                cuts.append(logger_step(target, k, t0, t1))
        bounds = [None] + cuts
        segs = []
        for n, t_from in enumerate(bounds):
            t_to = bounds[n + 1] if n + 1 < len(bounds) else None
            inside = [o for t, o in vs if (t_from is None or t >= t_from) and (t_to is None or t < t_to)]
            segs.append((t_from, float(np.mean(inside))))
        out[k] = segs
    return out


def logger_step(target, k, t0, t1):
    """The time of the reading where the logger's level steps between two visits: the largest change between two
    15-minute readings whose neighbours, four readings each side, change by less than 0.03 ft."""
    ts, lev, tc = logger_levels(target, k)
    best = None
    for i in range(5, len(ts) - 5):
        if not (t0 < ts[i] < t1):
            continue
        jump = lev[i] - lev[i - 1]
        if abs(jump) < 0.10:
            continue
        before = np.abs(np.diff(lev[i - 5:i]))
        after = np.abs(np.diff(lev[i:i + 5]))
        if before.max() < 0.03 and after.max() < 0.03 and (best is None or abs(jump) > best[0]):
            best = (abs(jump), ts[i])
    assert best is not None, (k, t0, t1)
    return best[1]


def rated_flow(ratings, k, loc, h):
    for eff, sup, hh, qq in ratings[k]:
        if eff <= loc and (sup is None or loc < sup):
            if h <= hh[0]:
                return 0.0
            return float(np.interp(h, hh, qq))
    raise KeyError((k, loc))


def daily_mean(ts, vals):
    acc = defaultdict(list)
    for t, v in zip(ts, vals):
        if not math.isnan(v):
            acc[t.date()].append(v)
    return {d: float(np.mean(v)) for d, v in acc.items()}


# ------------------------------------------------------------------ the lake
def buoy_profiles(target):
    """Daily mean temperature by depth below the surface at the dam buoy, by local date."""
    service = []
    with open(p(target, "lake/buoy_service_log_2026.csv"), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            service.append(r)
    rehang = dt.datetime(2026, 6, 10, 10, 0)
    acc = defaultdict(lambda: defaultdict(list))
    with open(p(target, "lake/MERRIN_BUOY_Hourly_2026.dat"), encoding="ascii") as fh:
        lines = fh.read().splitlines()
    for ln in lines[4:]:
        parts = [x.strip('"') for x in ln.split(",")]
        t = dt.datetime.strptime(parts[0], "%Y-%m-%d %H:%M:%S")
        depths = [0.5 + n for n in range(16)] if t < rehang else [1.0 + n for n in range(16)]
        d = cst_to_local(t).date()
        for z, v in zip(depths, parts[4:20]):
            if v != "NAN":
                acc[d][z].append(float(v))
    prof = {}
    for d, byz in acc.items():
        zs = sorted(byz)
        prof[d] = (np.array(zs), np.array([np.mean(byz[z]) for z in zs]))
    return prof


def pool_elev(target):
    wb = openpyxl.load_workbook(p(target, "lake/merrin_dam_daily_log_2026.xlsx"), read_only=True)
    ws = wb["Daily 0800"]
    out = {}
    for row in ws.iter_rows(min_row=3, values_only=True):
        if row[0] is None:
            continue
        d = dt.datetime.strptime(row[0], "%Y-%m-%d").date()
        out[d] = float(row[1])
    return out


def intake_depth(elev_ngvd):
    return (elev_ngvd - (INTAKE_NAVD - NAVD_MINUS_NGVD)) * FT


def entry(prof, temp):
    """Depth where the profile is as warm as the inflow: the surface for an inflow warmer than the top sensor,
    the bottom (None) for one colder than the deepest, otherwise interpolated between sensors."""
    zs, tt = prof
    if temp >= tt[0]:
        return 0.0
    if temp <= tt[-1]:
        return None
    for n in range(len(zs) - 1):
        a, b = tt[n], tt[n + 1]
        if (a - temp) * (b - temp) <= 0 and a != b:
            return float(zs[n] + (zs[n + 1] - zs[n]) * (a - temp) / (a - b))
    return None


def mixed(prof):
    zs, tt = prof
    return (tt[0] - tt[-1]) < 1.0


def entries(target):
    prof = buoy_profiles(target)
    elev = pool_elev(target)
    T = {}
    for k in SUBS:
        ts, q, tc = station_series(target, k)
        T[k] = daily_mean(ts, tc)
    E = {}
    for d in sorted(prof):
        if d not in elev:
            continue
        row = dict(zi=intake_depth(elev[d]), mixed=mixed(prof[d]))
        for k in SUBS:
            if d in T[k]:
                row[k] = None if row["mixed"] else entry(prof[d], T[k][d])
        E[d] = row
    return E, T, prof, elev


def reached(E, d, k, h, window):
    """Whether sub-watershed k's water entered within h metres of the intake's depth on a day in the window before
    day d. The look-back stops at a day the lake was mixed: water that came in before the lake stratified is part
    of the spring residue every depth shares, which is what the raw water keeps without any one sub-watershed."""
    for n in range(0, window + 1):
        dd = d - dt.timedelta(days=n)
        if dd not in E:
            continue
        r = E[dd]
        if r["mixed"]:
            return False
        z = r.get(k)
        if z is not None and z != 0.0 and abs(z - r["zi"]) <= h:
            return True
        if z is not None and z == 0.0 and abs(r["zi"]) <= h:
            return True
    return False


def attribute(E, days, h=2.0, window=30):
    """For each day above the trigger, the sub-watersheds whose water could be in what the intake drew. A day
    counts for a sub-watershed (plan 5.1) when that sub-watershed's water is the only atrazine-bearing water to
    have reached the intake's layer: without it the raw water keeps only the lake's spring residue."""
    per = {k: [] for k in SUBS}
    who = {}
    for d in days:
        src = [k for k in SUBS if reached(E, d, k, h, window)]
        who[d] = src
        if len(src) == 1:
            per[src[0]].append(d)
    return per, who


# ------------------------------------------------------------------ the samples and the loads (ask 1)
STATION_OF_SITE = {"TES-HB": "TR-01", "FEN-38": "FC-02", "OXL-LS": "OC-03", "DUN-230": "DC-04", "LAD-MP": "LB-05"}


def bottles(target, mode="golden"):
    """Each bottle's sample time: a routine grab's logged time (it is logged as it is taken); a storm bottle's from
    the autosampler run whose carousel came off when the bottles were logged, the bottles in their number order
    matched to the positions that drew a sample."""
    wb = openpyxl.load_workbook(p(target, "lab/field_sampling_log_2026.xlsx"), read_only=True)
    ws = wb["2026 bottles"]
    out = {}
    storm = defaultdict(list)
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0] is None:
            continue
        bid, site, date, time_ = row[:4]
        t = dt.datetime.strptime(date + " " + time_, "%m/%d/%Y %H:%M")
        key = bid.replace("-", "")
        out[key] = dict(site=site, t=t, kind=row[4], labs=row[5])
        if str(row[4]).startswith("Storm"):
            storm[(STATION_OF_SITE[site], t)].append(key)
    if mode == "logged":
        return out
    runs = defaultdict(list)
    with open(p(target, "lab/autosampler_run_logs_2026.csv"), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["Status"] != "OK" and mode != "position":
                continue
            removed = dt.datetime.strptime(r["Carousel removed"], "%Y-%m-%d %H:%M")
            runs[(r["Station"], removed)].append((int(r["Bottle position"]),
                                                  dt.datetime.strptime(r["Sample time"], "%Y-%m-%d %H:%M")))
    for key, ids in storm.items():
        fills = sorted(runs[key])
        assert mode == "position" or len(fills) == len(ids), (key, len(fills), len(ids))
        for bid, (pos, ft) in zip(sorted(ids), fills):
            out[bid]["t"] = ft
    return out


def sample_values(target, mode="golden"):
    """One value per bottle: the State laboratory's atrazine where it ran the bottle (plan 3.2), otherwise the city
    laboratory's ELISA; not detected counts as zero. A grab's time is when it was logged at the site; a storm
    bottle's is the autosampler's sample time for its position."""
    B = bottles(target, mode)
    shl = {}
    with open(p(target, "lab/SHL_EDD_brennick_source_water_2026.csv"), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["Analyte"] != "Atrazine":
                continue
            v = 0.0 if r["Qualifier"] == "U" else float(r["Result"])
            shl[r["Client_Sample_ID"].replace("-", "")] = v
    city = {}
    wb = openpyxl.load_workbook(p(target, "lab/city_lab_ELISA_tributaries_2026.xlsx"), read_only=True)
    for row in wb["Results"].iter_rows(min_row=2, values_only=True):
        if row[0] is None:
            continue
        v = 0.0 if row[8] == "<" else float(row[5])
        city[row[1].replace("-", "")] = v
    site_k = {v: k for k, v in SITE.items()}
    out = {k: [] for k in SUBS}
    for bid, b in B.items():
        v = shl.get(bid, city.get(bid))
        if v is None:
            continue
        out[site_k[b["site"]]].append((b["t"], v))
    for k in out:
        out[k].sort()
    return out


def load_kg(ts, q, samples, window=LOAD_WINDOW):
    """Atrazine past the station in the window: each 15-minute discharge times the concentration interpolated
    linearly in time between the samples either side of it."""
    st = np.array([(t - window[0]).total_seconds() for t, _ in samples])
    sv = np.array([v for _, v in samples])
    tot = 0.0
    for t, qq in zip(ts, q):
        if not (window[0] <= t < window[1]) or math.isnan(qq):
            continue
        x = (t - window[0]).total_seconds()
        c = float(np.interp(x, st, sv))
        tot += qq * CFS_L * 900.0 * c          # ug
    return tot / 1e9


MONTHS = [(m, (dt.datetime(2026, m, 1), dt.datetime(2026, m + 1, 1))) for m in (4, 5, 6, 7)]


def loads(target, mode="golden", offsets=None):
    """Season and monthly atrazine past each sampled station (Ladd Branch is not sampled, plan 3.1)."""
    S = sample_values(target, mode)
    out, series = {}, {}
    for k in SUBS:
        if not S[k]:
            continue
        ts, q, tc = station_series(target, k, offsets)
        series[k] = (ts, q)
        out[k] = load_kg(ts, q, S[k])
    return out, S, series


def monthly_loads(target, S=None, series=None):
    if S is None:
        L, S, series = loads(target)
    out = {}
    for k, (ts, q) in series.items():
        out[k] = {m: load_kg(ts, q, S[k], window=w) for m, w in MONTHS}
    return out


def daily_loads(target, S=None, series=None):
    """Atrazine past each station by local day (kg), on the same interpolation."""
    if S is None:
        L, S, series = loads(target)
    out = {}
    for k in series:
        ts, q = series[k]
        st = np.array([(t - LOAD_WINDOW[0]).total_seconds() for t, _ in S[k]])
        sv = np.array([v for _, v in S[k]])
        acc = defaultdict(float)
        for t, qq in zip(ts, q):
            if math.isnan(qq):
                continue
            c = float(np.interp((t - LOAD_WINDOW[0]).total_seconds(), st, sv))
            acc[t.date()] += qq * CFS_L * 900.0 * c / 1e9
        out[k] = dict(acc)
    return out


# ------------------------------------------------------------------ the carbon (ask 2)
def feeder_record(target):
    """The PAC feeder's dose setpoints and its run-status and low-low hopper alarms, in local time."""
    sp = []
    with open(p(target, "plant/scada_pac_dose_setpoint_2026.csv"), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            sp.append((utc_to_local(dt.datetime.strptime(r["Timestamp (UTC)"], "%Y-%m-%d %H:%M")), float(r["Value"])))
    sp.sort()
    ev = []
    with open(p(target, "plant/scada_alarm_event_history_2026.csv"), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["Tag"] == "PAC-FDR-1":
                ev.append((utc_to_local(dt.datetime.strptime(r["Time (UTC)"], "%Y-%m-%d %H:%M")), r["Description"],
                           r["Type"]))
    return sp, ev


def spans(ev, start, stop):
    """Intervals from each `start` event to the next `stop` event."""
    out, open_ = [], None
    for t, d, ty in ev:
        if (d, ty) == start and open_ is None:
            open_ = t
        elif (d, ty) == stop and open_ is not None:
            out.append((open_, t))
            open_ = None
    if open_ is not None:
        out.append((open_, dt.datetime(2026, 11, 1)))
    return out


def plant_rate(target):
    rate = {}
    wb = openpyxl.load_workbook(p(target, "plant/daily_operating_report_2026.xlsx"), read_only=True)
    for row in wb["2026"].iter_rows(min_row=2, values_only=True):
        if row[0] is not None:
            rate[dt.datetime.strptime(row[0], "%Y-%m-%d").date()] = float(row[1])
    return rate


def carbon(target, run_spans=None, empty_spans=None, sp=None):
    """Pounds of PAC fed by local calendar month: the dose setpoint (mg/L) x the plant day's raw water (MGD, the
    day running from 06:00) x 8.34 (SOP-WQ-07 3.2), over the minutes the feeder was running with carbon in its
    hopper: its run status on (a motor overload trip leaves it stopped until it is started again) and no low-low
    hopper alarm standing. Returns the monthly pounds, the feeding interruptions, the setpoints and the monthly
    pounds with no interruption."""
    sp0, ev = feeder_record(target)
    sp = sp0 if sp is None else sp
    if run_spans is None:
        run_spans = spans(ev, ("RUN STATUS ON", "EVT"), ("RUN STATUS OFF", "EVT"))
    if empty_spans is None:
        empty_spans = spans(ev, ("HOPPER LEVEL LOW-LOW NO FEED", "ALM"), ("HOPPER LEVEL LOW-LOW NO FEED", "RTN"))
    rate = plant_rate(target)
    by_month, by_month_nodown = defaultdict(float), defaultdict(float)
    down, cur_down = [], None
    t = sp[0][0]
    end = dt.datetime(2026, 11, 1, 0, 0)
    k, cur = 0, 0.0
    ri = ei = 0
    run_spans = sorted(run_spans)
    empty_spans = sorted(empty_spans)
    step = dt.timedelta(minutes=1)
    while t < end:
        while k < len(sp) and sp[k][0] <= t:
            cur = sp[k][1]
            k += 1
        if cur > 0:
            lb = cur * rate[(t - dt.timedelta(hours=6)).date()] * 8.34 / 1440.0
            by_month_nodown[t.month] += lb
            running = any(a <= t < b for a, b in run_spans)
            empty = any(a <= t < b for a, b in empty_spans)
            if running and not empty:
                by_month[t.month] += lb
                if cur_down is not None:
                    down.append((cur_down, t))
                    cur_down = None
            elif cur_down is None:
                cur_down = t
        elif cur_down is not None:
            down.append((cur_down, t))
            cur_down = None
        t += step
    return dict(by_month), down, sp, dict(by_month_nodown)


# ------------------------------------------------------------------ the ladder's rungs (the easy routes)
def mixed_lake(results, days, dl, window=30):
    """The mixed-lake reading: on each day above the trigger, each sub-watershed's share of the atrazine that
    passed the stations in the trailing window; the day counts for it if the raw water less that share is at or
    below the trigger."""
    per = {k: 0 for k in SUBS}
    for d in days:
        tot = {k: sum(dl.get(k, {}).get(d - dt.timedelta(days=n), 0.0) for n in range(window)) for k in SUBS}
        s = sum(tot.values())
        for k in SUBS:
            if results[d] * (1 - tot[k] / s) <= TRIGGER:
                per[k] += 1
    return per


def compute(target):
    results, screen, conf = day_results(target)
    days = days_above(results)
    E, T, prof, elev = entries(target)
    per, who = attribute(E, days)
    L, S, series = loads(target)
    LM = monthly_loads(target, S, series)
    dl = daily_loads(target, S, series)
    cb = carbon(target)
    pac, down, sp, pac_nodown = cb
    rungs = dict(r0_load=dict(L), r1_mixed30=mixed_lake(results, days, dl, 30),
                 r1_mixed14=mixed_lake(results, days, dl, 14), r1_mixed45=mixed_lake(results, days, dl, 45))
    return dict(results=results, screen=screen, conf=conf, days=days, E=E, T=T, per=per, who=who, loads=L,
                loads_month=LM, samples=S, pac=pac, pac_nodown=pac_nodown, down=down, setpoints=sp, rungs=rungs,
                elev=elev, offsets=logger_offset(target))


if __name__ == "__main__":
    import sys
    tgt = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "target")
    R = compute(tgt)
    print("days above trigger:", len(R["days"]), R["days"][0], R["days"][-1])
    print("per sub-watershed:", {k: len(v) for k, v in R["per"].items()})
    print("sources per day:", sorted(set(tuple(v) for v in R["who"].values())))
    print("loads kg:", {k: round(v, 1) for k, v in R["loads"].items()})
    print("monthly kg:", {k: {m: round(v, 2) for m, v in mm.items()} for k, mm in R["loads_month"].items()})
    print("logger offsets:", R["offsets"])
    print("rungs:", {k: ({kk: (round(vv, 1) if isinstance(vv, float) else vv) for kk, vv in v.items()}) for k, v in R["rungs"].items()})
    print("pac lb by month:", {k: round(v) for k, v in R["pac"].items()}, "without downtime:", {k: round(v) for k, v in R["pac_nodown"].items()})
    print("downtime:", [(a.strftime("%m-%d %H:%M"), b.strftime("%m-%d %H:%M")) for a, b in R["down"]])
