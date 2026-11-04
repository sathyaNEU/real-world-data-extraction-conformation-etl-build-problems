"""The ladder and every reflex route, each computed from target/ the way a competent analyst would compute it.

R0  the dry-day screen: spills that begin on a dry day (the procedure's dry-day definition) name the overflow
R1  the permit check with the rated duty: during each spill, the duty of the pump the telemetry shows running
    (the meter where a station has one) against the permit's pass forward flow
R2  the high spiller: the most 12/24 spills (and the most hours) in 2026
R3  the decisive step: the pass forward each station's own wet well cycles show its pumps deliver, against the
    permit's flow
Reflexes priced beside them: run hours, starts per day, mean pump run per start, rain before each spill's onset,
spill hours per spill, spills per millimetre of rain."""
import datetime as dt
from collections import defaultdict

import numpy as np

import golden as G


def rain_daily_local(tgt):
    rows = G.read_csv(G.os.path.join(tgt, G.FILES["rain"]))
    day = defaultdict(lambda: defaultdict(float))
    q15 = defaultdict(dict)
    for r in rows:
        t = (dt.datetime.strptime(r["interval_start_utc"], "%Y-%m-%dT%H:%M:%SZ") - G.T0).total_seconds()
        v = float(r["rain_mm"])
        day[r["radar_zone"]][G.utc_to_local(t).date()] += v
        q15[r["radar_zone"]][int(t // 900)] = v
    return day, q15


def dry_day_spills(g, tgt, by="current"):
    """Spills (12/24 counts of discharges) that begin on a dry day, per overflow. by='current' joins the discharge
    log on the register's monitor only; by='all' uses every serial mapped to the overflow."""
    day, _ = rain_daily_local(tgt)
    log, status, mlist = G.edm_records(tgt)
    out = {}
    for code, st in g["stations"].items():
        sers = [st["edm"]] if by == "current" else [s for s, c in g["serial_site"].items() if c == code]
        iv = G.union([x for s in sers for x in log.get(s, [])])
        n = 0
        zone = st["zone"]
        for a, b in iv:
            d = G.utc_to_local(a).date()
            prev = d - dt.timedelta(days=1)
            if day[zone].get(d, 0.0) < 0.25 and day[zone].get(prev, 0.0) < 0.25:
                n += 1
        out[code] = n
    return out


def rated_check(g, tgt):
    """R1: the flow passed forward during each spill read as the duty of the running pump (the meter at the three
    metered stations); returns the overflows any spill of which fails the permit's flow."""
    stations = g["stations"]
    fails = []
    meter_flow = {}
    rows = G.read_csv(G.os.path.join(tgt, G.FILES["meters"]))
    mf = defaultdict(dict)
    for r in rows:
        if r["quality"] != "G" or r["flow_ls_mean"] == "":
            continue                                   # the historian's good values only
        t = (dt.datetime.strptime(r["interval_start_utc"], "%Y-%m-%dT%H:%M:%SZ") - G.T0).total_seconds()
        mf[r["meter_tag"]][int(t // 900)] = float(r["flow_ls_mean"])
    for code, st in stations.items():
        pff = g["pff"][code]
        rated = st["rated"]
        bad = False
        if st.get("meter"):
            # the meter's full fifteen-minute intervals inside each alarm period
            vals = []
            for a, b in g["alarms"][st["rtu"]]:
                for k in range(int(a // 900) + 1, int(b // 900)):
                    v = mf[st["meter"]].get(k)
                    if v is not None:
                        vals.append(v)
            meter_flow[code] = float(np.median(vals)) if vals else None
            if vals and np.median(vals) < pff:
                bad = True
        elif min(rated.values()) < pff:
            bad = True
        if bad:
            fails.append(code)
    return fails, meter_flow


def reflexes(g, tgt):
    stations = g["stations"]
    ev = g["events"]
    _, q15 = rain_daily_local(tgt)
    out = defaultdict(dict)
    for code, st in stations.items():
        e = ev[st["rtu"]]
        run = 0.0
        starts = 0
        on = None
        for t, p, s, _ in e:
            if s == 1:
                on = t
                starts += 1
            elif on is not None:
                run += t - on
                on = None
        out["run_hours_per_day"][code] = run / 3600.0 / 365.0
        out["starts_per_day"][code] = starts / 365.0
        out["mean_run_s"][code] = run / max(starts, 1)
        L = g["lines"][code]
        out["hours_per_spill"][code] = L["hours"] / max(L["spills"], 1)
        # rain over the zone in the six hours before each discharge starts (every mapped serial)
        log = g["log"]
        sers = [s for s, c in g["serial_site"].items() if c == code]
        iv = G.union([x for s in sers for x in log.get(s, [])])
        z = q15[st["zone"]]
        onset = [sum(z.get(k, 0.0) for k in range(int(a // 900) - 24, int(a // 900))) for a, _ in iv]
        out["onset_rain_6h_median"][code] = float(np.median(onset)) if onset else float("nan")
        tot = sum(z.values())
        out["spills_per_100mm"][code] = 100.0 * L["spills"] / tot if tot else 0.0
    # the telemetry's other alarms and the crews' work orders
    import sqlite3
    con = sqlite3.connect(G.os.path.join(tgt, G.FILES["telemetry"]))
    hl = defaultdict(int)
    hl_h = defaultdict(float)
    for rtu, a, b in con.execute("SELECT rtu, raised_utc, cleared_utc FROM alarm WHERE alarm='HIGH LEVEL'"):
        hl[rtu] += 1
        hl_h[rtu] += (G.utc_sec(b) - G.utc_sec(a)) / 3600.0
    con.close()
    wo = G.read_csv(G.os.path.join(tgt, "operations/sps_work_orders_2026.csv"))
    for code, st in stations.items():
        out["high_level_alarms"][code] = hl[st["rtu"]]
        out["high_level_hours"][code] = hl_h[st["rtu"]]
        out["high_level_per_spill"][code] = hl[st["rtu"]] / max(g["lines"][code]["spills"], 1)
        out["callouts"][code] = sum(1 for r in wo if r["station_code"] == code and r["task"] == "High level alarm attended")
        out["work_orders"][code] = sum(1 for r in wo if r["station_code"] == code)
    return out


def naive_drawdown(g):
    """The drawdown test read off the telemetry without the inflow: the volume between the duty pump's control levels
    over the pump-on time alone. Three ways a solver takes it: the median over every run, the median over the runs
    that start between midnight and five in the morning (the low-flow hours a drawdown test is done in), and the 90th
    percentile of the runs (the fastest drawdowns)."""
    med, night, p90 = {}, {}, {}
    for code, st in g["stations"].items():
        e = g["events"][st["rtu"]]
        V = st["area"] * (st["start"] - st["stop"]) * 1000.0
        on, on_n = [], []
        for k in range(len(e) - 1):
            if e[k][2] == 1 and e[k + 1][2] == 0 and e[k][1] == e[k + 1][1] and 0 < e[k + 1][0] - e[k][0] <= 6 * 3600:
                on.append(V / (e[k + 1][0] - e[k][0]))
                if G.utc_to_local(e[k][0]).hour < 5:
                    on_n.append(on[-1])
        med[code], night[code], p90[code] = float(np.median(on)), float(np.median(on_n)), float(np.percentile(on, 90))
    return med, night, p90


def top(d, reverse=True):
    items = sorted(((v, k) for k, v in d.items() if v == v), reverse=reverse)
    return items[0][1], items


def ladder(g, tgt):
    dd = dry_day_spills(g, tgt, by="all")
    dd_cur = dry_day_spills(g, tgt, by="current")
    r1, meter_flow = rated_check(g, tgt)
    spills = {c: g["lines"][c]["spills"] for c in g["stations"]}
    hours = {c: g["lines"][c]["hours"] for c in g["stations"]}
    rf = reflexes(g, tgt)
    nd, nd_night, nd_p90 = naive_drawdown(g)
    return dict(dry_day=dd, dry_day_current=dd_cur, R0=top(dd)[0], R1=r1 or ["none"], R1_meter_flow=meter_flow,
                naive=nd, naive_night=nd_night, naive_p90=nd_p90,
                naive_flagged=sorted(c for c in nd if nd[c] < g["pff"][c]),
                R2=top(spills)[0], R2_hours=top(hours)[0], spills=spills, hours=hours, R3=g["breach"], reflex=rf,
                reflex_top={k: top(v)[0] for k, v in rf.items()},
                reflex_bottom={k: top(v, reverse=False)[0] for k, v in rf.items()})
