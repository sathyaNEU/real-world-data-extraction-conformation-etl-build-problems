"""Cut target/ from the clean truth. Each file is written the way the system that produces it writes it: the
telemetry historian in UTC to the second with the outstation's level in metres above the wet well floor, the
event duration monitoring platform in UK local time with its own durations, the asset register in mAOD with each
pump's duty in the unit its datasheet gave, the consents register in the permits' own words, the radar rainfall
and the flow meters in UTC fifteen-minute steps. Layer 1 mess is what those systems really do: comms losses that
drop the historian's level polls and make outstations re-send their last events, monitors swapped mid-year whose
history stays under the old serial, two units watching one overflow through each handover week, local time against
UTC, a duty given in cubic metres an hour."""
import csv
import datetime as dt
import os
import sqlite3

import numpy as np

import sim
import world as W

FILES = {
    "telemetry": "telemetry/marsh_wolds_sps_telemetry_2026.sqlite",
    "edm_log": "edm/edm_discharge_log_2026.csv",
    "edm_status": "edm/edm_monitor_daily_status_2026.csv",
    "edm_list": "edm/edm_monitor_list_2027-01-15.csv",
    "rain": "rainfall/radar_rainfall_marsh_wolds_2026.csv",
    "assets": "registers/marsh_wolds_wastewater_assets.xlsx",
    "consents": "registers/wastewater_discharge_consents_2026.csv",
    "meters": "flow/rising_main_flow_meters_2026.csv",
    "procedure": "procedures/WW-ENV-PR-014_storm_overflow_EDM_reporting.pdf",
    "plan": "planning/storm_overflow_improvement_plan_2025-2030.xlsx",
    "borehole": "groundwater/hagworth_wold_obh_daily_2026.csv",
    "workorders": "operations/sps_work_orders_2026.csv",
}
T0 = sim.T0


def utc_str(sec):
    return (T0 + dt.timedelta(seconds=int(np.floor(sec)))).strftime("%Y-%m-%d %H:%M:%S")


def local_dt(sec):
    """UK local wall-clock time for a second of 2026 (UTC offset added, no offset written)."""
    m = int(np.floor(sec / 60.0))
    return T0 + dt.timedelta(seconds=float(sec)) + dt.timedelta(minutes=sim.local_offset_min(m))


def local_str(sec):
    return local_dt(sec).strftime("%d/%m/%Y %H:%M")


def local_str_s(sec):
    return local_dt(float(int(round(sec)))).strftime("%d/%m/%Y %H:%M:%S")


def ensure(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)


def write_csv(path, header, rows):
    ensure(path)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\r\n")
        w.writerow(header)
        w.writerows(rows)


# ---------------------------------------------------------------- site visits
ROUTINE = [("Wet well clean and level probe check", "Completed, probes cleaned", 0.38),
           ("Electrical inspection", "Completed", 0.28),
           ("Odour complaint attended", "No fault found at station", 0.17),
           ("Generator connection point test", "Completed", 0.17)]
SERVICE = ("Pump service (6-monthly)", "Completed, both pumps serviced")
METER = ("Flow meter verification", "Meter verified within tolerance")


def _weekday(day):
    while day.weekday() >= 5:
        day += dt.timedelta(days=1)
    return day


def local_to_utc_s(local_naive):
    return to_utc_sec(local_naive)


def site_visits(S):
    """Crew visits to each station in 2026: routine work on weekdays, call-outs to some high level alarms in working
    hours, and the odd kiosk door alarm with nobody there. Each visit opens the kiosk door (an INTRUDER alarm)."""
    for k, st in enumerate(W.STATIONS):
        r = S["stations"][st["code"]]
        rng = np.random.default_rng([W.SEED, 61, k])
        visits = []

        def visit(day, task, outcome, stay):
            arr = to_utc_sec(dt.datetime.combine(day, dt.time(7, 40)) + dt.timedelta(minutes=int(rng.integers(0, 400))))
            arr += float(rng.uniform(0, 59))
            visits.append(dict(arr=arr, dep=arr + rng.uniform(*stay) * 60, task=task, outcome=outcome, day=day))

        # the planned round: wet well cleans through the year, one electrical inspection, one generator point test;
        # odour complaints as they come in
        cleans = int(rng.integers(2, 5))
        for i in range(cleans):
            day = _weekday(dt.date(2026, 1, 12) + dt.timedelta(days=int(i * 350 / cleans + rng.integers(0, 40))))
            visit(day, ROUTINE[0][0], ROUTINE[0][1], (40, 150))
        for kind in (1, 3):
            day = _weekday(dt.date(2026, 1, 12) + dt.timedelta(days=int(rng.integers(0, 330))))
            visit(day, ROUTINE[kind][0], ROUTINE[kind][1], (25, 120))
        for _ in range(int(rng.integers(0, 3))):
            day = _weekday(dt.date(2026, 1, 5) + dt.timedelta(days=int(rng.integers(0, 352))))
            visit(day, ROUTINE[2][0], ROUTINE[2][1], (20, 60))
        first = _weekday(dt.date(2026, 2, 2) + dt.timedelta(days=int(rng.integers(0, 110))))
        second = _weekday(first + dt.timedelta(days=int(rng.integers(176, 192))))
        for day in (first, second):
            visit(day, SERVICE[0], SERVICE[1], (120, 260))
        r["pump_service"] = second
        if st["meter"]:
            day = _weekday(dt.date(2026, 3, 2) + dt.timedelta(days=int(rng.integers(0, 180))))
            visit(day, METER[0], METER[1], (60, 150))
            r["meter_verified"] = day
        calls = 0
        for a, b in r["highs"]:
            ld = local_dt(a)
            if ld.weekday() >= 5 or not (7 <= ld.hour < 17) or calls >= 4 or rng.random() > 0.3:
                continue
            arr = a + rng.uniform(45, 150) * 60
            outcome = ("Level high on arrival, duty pump running, standby available" if arr < b
                       else "Level normal on arrival, both pumps available")
            visits.append(dict(arr=arr, dep=arr + rng.uniform(20, 70) * 60, task="High level alarm attended",
                               outcome=outcome))
            calls += 1
        door = []
        for _ in range(int(rng.integers(0, 3))):
            t = rng.uniform(10, 350) * 86400
            door.append((t, t + rng.uniform(3, 20) * 3600))
        visits.sort(key=lambda v: v["arr"])
        r["visits"], r["door"] = visits, sorted(door)


# ---------------------------------------------------------------- telemetry
def comms_losses(rng):
    k = int(rng.integers(1, 4))
    out = []
    for _ in range(k):
        a = rng.uniform(5, 360) * 86400
        out.append((a, a + rng.uniform(2.5, 11) * 3600))
    return sorted(out)


def telemetry(tgt, S, info):
    path = os.path.join(tgt, FILES["telemetry"])
    ensure(path)
    if os.path.exists(path):
        os.remove(path)
    con = sqlite3.connect(path)
    c = con.cursor()
    c.execute("CREATE TABLE rtu (rtu INTEGER PRIMARY KEY, rtu_tag TEXT, site_label TEXT, rtu_type TEXT, scan_s INTEGER, "
              "level_ref TEXT, commissioned TEXT)")
    c.execute("CREATE TABLE pump_event (rtu INTEGER, pump INTEGER, state TEXT, event_utc TEXT, wet_well_m REAL)")
    c.execute("CREATE TABLE wet_well_level (rtu INTEGER, sample_utc TEXT, level_m REAL)")
    c.execute("CREATE TABLE alarm (rtu INTEGER, alarm TEXT, raised_utc TEXT, cleared_utc TEXT)")
    types = ["Schneider SCADAPack 470", "Servelec TBox LT2", "Schneider SCADAPack 470", "Ovarro TBox MS-CPU32"]
    n_ev = n_lv = n_dup = n_al = 0
    gaps = {}
    for k, st in enumerate(W.STATIONS):
        r = S["stations"][st["code"]]
        rng = np.random.default_rng([W.SEED, 7, k])
        comm = (dt.date(2009, 1, 1) + dt.timedelta(days=int(rng.integers(0, 4000)))).isoformat()
        rid = int(st["rtu"].split()[1])
        c.execute("INSERT INTO rtu VALUES (?,?,?,?,?,?,?)", (rid, st["rtu"], st["tlabel"], types[k % 4],
                                                             int(rng.choice([2, 5])), "metres above wet well floor", comm))
        losses = comms_losses(rng)
        gaps[st["code"]] = losses
        rows = []
        lev_noise = rng.normal(0, 0.004, len(r["events"]))
        for j, (ts, p, s) in enumerate(r["events"]):
            lvl = (st["start"] if s == 1 else st["stop"]) + lev_noise[j]
            rows.append((rid, int(p), "RUN" if s == 1 else "STOP", utc_str(ts), round(float(lvl), 2), ts))
        # after each comms loss the outstation re-sends its last few events before the loss
        dup = []
        for (a, b) in losses:
            before = [x for x in rows if x[5] < a][-int(rng.integers(3, 9)):]
            dup.extend(before)
        rows.extend(dup)
        n_dup += len(dup)
        rows.sort(key=lambda x: (x[5], x[2]))
        c.executemany("INSERT INTO pump_event VALUES (?,?,?,?,?)", [x[:5] for x in rows])
        n_ev += len(rows)
        lv = []
        for i, h in enumerate(r["levels"]):
            sec = i * 900.0
            if any(a <= sec < b for (a, b) in losses):
                continue
            lv.append((rid, utc_str(sec), round(float(h + rng.normal(0, 0.004)), 2)))
        c.executemany("INSERT INTO wet_well_level VALUES (?,?,?)", lv)
        n_lv += len(lv)
        # the outstation's overflow float switch: its own hysteresis and its own seconds
        al = []
        for (a, b) in r["spills"]:
            if b - a < 45:
                continue
            ra = a + rng.uniform(8, 40)
            cb = b + rng.uniform(30, 140)
            if al and ra <= al[-1][1] + 60:
                al[-1][1] = max(al[-1][1], cb)
            else:
                al.append([ra, cb])
        rows_al = [(rid, "OVERFLOW OPERATING", a, b) for a, b in al]
        # the other alarms the outstation and the master station raise: the high level float switch, lost comms,
        # the kiosk door
        rng2 = np.random.default_rng([W.SEED, 8, k])
        for (a, b) in r["highs"]:
            if b - a >= 20:
                rows_al.append((rid, "HIGH LEVEL", a + rng2.uniform(2, 15), b + rng2.uniform(2, 25)))
        for (a, b) in losses:
            rows_al.append((rid, "COMMS FAIL", a + rng2.uniform(120, 600), b + rng2.uniform(10, 120)))
        for v in r["visits"]:
            rows_al.append((rid, "INTRUDER", v["arr"] + rng2.uniform(5, 60), v["dep"] - rng2.uniform(0, 60)))
        for (a, b) in r["door"]:
            rows_al.append((rid, "INTRUDER", a, b))
        rows_al.sort(key=lambda x: (x[2], x[1]))
        rows_al = [(x[0], x[1], utc_str(x[2]), utc_str(x[3])) for x in rows_al]
        c.executemany("INSERT INTO alarm VALUES (?,?,?,?)", rows_al)
        n_al += len(rows_al)
        r["float_alarms"] = [(a, b) for a, b in al]
    con.commit()
    con.execute("VACUUM")
    con.close()
    info.update(telemetry_events=n_ev, telemetry_levels=n_lv, telemetry_dups=n_dup, telemetry_alarms=n_al, comms=gaps)


# ---------------------------------------------------------------- event duration monitoring
def edm(tgt, S, info):
    log_rows, status_rows, list_rows = [], [], []
    hours_truth = {}
    for k, st in enumerate(W.STATIONS):
        r = S["stations"][st["code"]]
        rng = np.random.default_rng([W.SEED, 11, k])
        for m in r["monitors"]:
            for (a, b) in m["events"]:
                log_rows.append((m["serial"], local_str_s(a), local_str_s(b), a))
            # daily status: hours the monitor was operating and reporting, per local day
            for day, hrs in status_days(m):
                status_rows.append((m["serial"], day.strftime("%d/%m/%Y"), hrs,
                                    "%.2f" % rng.uniform(3.3, 3.62) if m["model"] == "AQ7" else "%.2f" % rng.uniform(3.55, 3.68)))
        # the platform's device list as exported on the return date
    for code in sorted(W.EDM_CURRENT):
        ser = W.EDM_CURRENT[code]
        model = "HX-40 radar" if ser.startswith("HX") else "AQ-7 ultrasonic"
        if code in W.EDM_REPLACED:
            comm = W.EDM_REPLACED[code][1].strftime("%d/%m/%Y")
        else:
            comm = W.aq7_commissioned(ser).strftime("%d/%m/%Y")
        list_rows.append((ser, model, "4.2.1" if ser.startswith("HX") else "2.9.7", comm, "ACTIVE", "",
                          "WW-SO-" + code[3:]))
    for code, (old, inst, rem) in sorted(W.EDM_REPLACED.items()):
        comm = W.aq7_commissioned(old).strftime("%d/%m/%Y")
        list_rows.append((old, "AQ-7 ultrasonic", "2.9.7", comm, "RETIRED", rem.strftime("%d/%m/%Y"), ""))
    log_rows.sort(key=lambda x: (x[0], x[3]))
    write_csv(os.path.join(tgt, FILES["edm_log"]), ["monitor_serial", "discharge_start", "discharge_end"],
              [x[:3] for x in log_rows])
    status_rows.sort(key=lambda x: (x[0], dt.datetime.strptime(x[1], "%d/%m/%Y")))
    write_csv(os.path.join(tgt, FILES["edm_status"]), ["monitor_serial", "date", "hours_reporting", "battery_v"], status_rows)
    list_rows.sort(key=lambda x: x[0])
    write_csv(os.path.join(tgt, FILES["edm_list"]), ["serial", "model", "firmware", "commissioned", "status", "retired",
                                                     "site_id"], list_rows)
    info.update(edm_log_rows=len(log_rows), edm_status_rows=len(status_rows), edm_list_rows=len(list_rows))


def status_days(m):
    """The platform's daily status for one monitor: (local day, hours operating and reporting to one decimal)."""
    out = []
    lo, hi = m["active"]
    day = local_dt(max(lo, 0)).date()
    d1 = local_dt(min(hi, sim.MIN * 60.0 - 1)).date()
    while day <= d1:
        start_loc = dt.datetime.combine(day, dt.time(0, 0))
        sa = to_utc_sec(start_loc)
        sb = to_utc_sec(start_loc + dt.timedelta(days=1))
        a_, b_ = max(sa, lo), min(sb, hi)
        up = max(0.0, b_ - a_)
        for (oa, ob) in m["outages"]:
            up -= max(0.0, min(ob, b_) - max(oa, a_))
        hrs = max(0.0, up / 3600.0)
        if hrs > 0.05:
            out.append((day, "%.1f" % hrs))
        day += dt.timedelta(days=1)
    return out


def to_utc_sec(local_naive):
    """UTC seconds from T0 for a UK local wall-clock time in 2026 (the repeated October hour taken as BST)."""
    guess = (local_naive - T0).total_seconds()
    for off in (3600.0, 0.0):
        s = guess - off
        m = int(np.floor(s / 60.0))
        if sim.local_offset_min(m) * 60.0 == off:
            return s
    return guess - 3600.0


# ---------------------------------------------------------------- rainfall and meters
def rainfall(tgt, S, info):
    rain15 = S["rain"].reshape(len(W.ZONES), -1, 15).sum(axis=2)
    rows = []
    for z, zone in enumerate(W.ZONES):
        for i in range(rain15.shape[1]):
            t = (T0 + dt.timedelta(minutes=15 * i)).strftime("%Y-%m-%dT%H:%M:%SZ")
            rows.append(("MW-" + zone, t, "%.2f" % rain15[z, i]))
    write_csv(os.path.join(tgt, FILES["rain"]), ["radar_zone", "interval_start_utc", "rain_mm"], rows)
    info["rain_rows"] = len(rows)


def meters(tgt, S, info):
    """The meter historian's fifteen-minute means with the quality it writes beside each: G good, M no value (the
    outstation could not send), C the meter under test while the verification crew was on site, E estimated by the
    historian from the pump's run state while the transmitter was faulted, S suspect (the empty-pipe detector
    flickering as the main drains back after a long stop). None of them falls within two hours of a spill."""
    rows = []
    for k, st in enumerate(W.STATIONS):
        if not st["meter"]:
            continue
        r = S["stations"][st["code"]]
        rng = np.random.default_rng([W.SEED, 13, k])
        q = r["meter_15"]
        n = len(q)
        vals = [v * (1 + rng.normal(0, 0.006)) if v > 0 else 0.0 for v in q]
        qual = ["G"] * n
        near = np.zeros(n, bool)
        for a, b in r["spills"]:
            near[max(0, int((a - 7200) // 900)): min(n, int((b + 7200) // 900) + 1)] = True
        rng2 = np.random.default_rng([W.SEED, 14, k])

        def window(lo_h, hi_h):
            for _ in range(200):
                i0 = int(rng2.integers(96, n - 200))
                i1 = i0 + int(rng2.integers(lo_h * 4, hi_h * 4 + 1))
                if not near[i0:i1 + 1].any() and all(x == "G" for x in qual[i0:i1 + 1]):
                    return i0, i1
            return None

        for a, b in info["comms"][st["code"]]:
            for i in range(int(a // 900), min(n, int(b // 900) + 1)):
                if not near[i]:
                    qual[i], vals[i] = "M", None
        for v in r["visits"]:
            if v["task"] == METER[0]:
                for i in range(int(v["arr"] // 900), min(n, int(v["dep"] // 900) + 1)):
                    if not near[i]:
                        qual[i] = "C"
        ev = r["events"]
        run = np.zeros(n)
        on = None
        for (ts, p, sg) in ev:
            if sg == 1:
                on = ts
            elif on is not None:
                for i in range(int(on // 900), min(n, int(ts // 900) + 1)):
                    run[i] += max(0.0, min(ts, (i + 1) * 900.0) - max(on, i * 900.0)) / 900.0
                on = None
        for _ in range(int(rng2.integers(1, 3))):
            w = window(3, 9)
            if w:
                good = [x for x in vals[max(0, w[0] - 96):w[0]] if x and x > 0]
                rate = float(np.median(good)) / max(float(np.median([x for x in run[max(0, w[0] - 96):w[0]] if x > 0] or [1])), 0.05) \
                    if good else 0.0
                for i in range(w[0], w[1] + 1):
                    qual[i], vals[i] = "E", rate * run[i]
        for _ in range(int(rng2.integers(2, 6))):
            w = window(1, 3)
            if w:
                for i in range(w[0], w[1] + 1):
                    qual[i] = "S"
        for i in range(n):
            t = (T0 + dt.timedelta(minutes=15 * i)).strftime("%Y-%m-%dT%H:%M:%SZ")
            rows.append((st["meter"], t, "" if vals[i] is None else "%.1f" % vals[i], qual[i]))
    write_csv(os.path.join(tgt, FILES["meters"]), ["meter_tag", "interval_start_utc", "flow_ls_mean", "quality"], rows)
    info["meter_rows"] = len(rows)
    info["meter_quality"] = {str(a): int(b) for a, b in zip(*np.unique([x[3] for x in rows], return_counts=True))}


def cut(tgt, S):
    info = {}
    site_visits(S)
    telemetry(tgt, S, info)
    edm(tgt, S, info)
    rainfall(tgt, S, info)
    meters(tgt, S, info)
    import registers
    registers.write(tgt, FILES, S, info)
    return info
