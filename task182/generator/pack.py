"""The folder the environmental engineer was handed: the meters' exports, the survey paperwork, the plant's
own records, the met mast, and two files the question does not use."""
import csv as _csv
import datetime as dt
import math
import os
import random

import numpy as np

import sim as SM
import world as W

FILES = {
    "levels": "sound_levels_1min_2026.parquet",
    "deployments": "meter_deployments_2026.csv",
    "positions": "monitoring_positions.xlsx",
    "plan": "noise_management_plan.pdf",
    "notes": "survey_notes.md",
    "events": "plant_equipment_events_2026.csv",
    "scada": "scada_15min_2026.csv",
    "weather": "weather_10min_2026.csv",
    "bands": "third_octave_15min_2026.csv",
    "calibration": "calibration_records_2026.csv",
    "complaints": "complaints_register_2026.xlsx",
    "effluent": "effluent_quality_2026.csv",
    "manifest": "export_manifest.csv",
}
BANDS = [25, 31.5, 40, 50, 63, 80, 100, 125, 160, 200, 250, 315, 400, 500, 630, 800, 1000, 1250,
         1600, 2000, 2500, 3150, 4000, 5000, 6300, 8000, 10000, 12500]


def _write_csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = _csv.writer(fh, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)
    return path


def utc(stamp_local):
    return stamp_local - dt.timedelta(hours=SM.LOCAL_OFFSET)


def write_levels(target, series):
    """The meters' own export: one row a minute, stamped UTC, as the download software writes it."""
    import pyarrow as pa
    import pyarrow.parquet as pq
    meters, stamps, laeq, la90, lamax, lamin = [], [], [], [], [], []
    dup = None
    for sid in sorted(series):
        s = series[sid]
        lg = SM.logged(s)
        n = len(s["stamps"])
        meters.extend([W_serial(s["dep"]["meter"])] * n)
        stamps.extend([utc(x) for x in s["stamps"]])
        laeq.extend(lg["laeq"].tolist())
        la90.extend(lg["la90"].tolist())
        lamax.extend(lg["lamax"].tolist())
        lamin.extend(lg["lamin"].tolist())
        if (s["dep"]["code"], s["dep"]["k"]) == W.DUP_DEPLOYMENT:
            m = np.array([(x.date() == W.DUP_DAY) and (W.DUP_FROM <= x.hour < W.DUP_TO)
                          for x in s["stamps"]])
            dup = {"meter": W_serial(s["dep"]["meter"]),
                   "stamps": [utc(x) for x, k in zip(s["stamps"], m) if k],
                   "laeq": lg["laeq"][m].tolist(), "la90": lg["la90"][m].tolist(),
                   "lamax": lg["lamax"][m].tolist(), "lamin": lg["lamin"][m].tolist()}
    if dup:
        meters.extend([dup["meter"]] * len(dup["stamps"]))
        stamps.extend(dup["stamps"])
        laeq.extend(dup["laeq"]); la90.extend(dup["la90"])
        lamax.extend(dup["lamax"]); lamin.extend(dup["lamin"])
    order = sorted(range(len(stamps)), key=lambda i: (meters[i], stamps[i]))
    tbl = pa.table({
        "meter_serial": pa.array([meters[i] for i in order], pa.string()),
        "measured_at_utc": pa.array([stamps[i] for i in order], pa.timestamp("s")),
        "laeq_db": pa.array([laeq[i] for i in order], pa.float32()),
        "la90_db": pa.array([la90[i] for i in order], pa.float32()),
        "lamax_db": pa.array([lamax[i] for i in order], pa.float32()),
        "lamin_db": pa.array([lamin[i] for i in order], pa.float32()),
    })
    path = os.path.join(target, FILES["levels"])
    pq.write_table(tbl, path, compression="snappy", version="2.6")
    return path, len(order), dup


def W_serial(meter_id):
    return [m["serial"] for m in W.METERS if m["id"] == meter_id][0]


def write_deployments(target, deps):
    rows = []
    for d in sorted(deps, key=lambda x: x["id"]):
        m = [x for x in W.METERS if x["id"] == d["meter"]][0]
        rem = ""
        if (d["code"], d["k"]) == W.DUP_DEPLOYMENT:
            rem = "card read error on collection, download repeated"
        if d["code"] == "NSL08" and d["k"] == 0:
            rem = "mic moved 3 m west on the Wednesday, stock had reached the tripod"
        if d["code"] == "NSL04" and d["k"] == 1:
            rem = "windshield replaced at mid-week check"
        rows.append([d["id"], m["serial"], d["code"], d["start"].isoformat(), d["end"].isoformat(),
                     "%.1f" % d["mount"], "%.1f" % m["pre"], "%.1f" % m["post"],
                     W.PEOPLE["technician"][1], rem])
    return _write_csv(os.path.join(target, FILES["deployments"]),
                      ["deployment_ref", "meter_serial", "position_code", "start_date", "end_date",
                       "mic_height_m", "cal_check_before_db", "cal_check_after_db", "operator",
                       "remarks"], rows)


def write_positions(target):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font
    wb = Workbook()
    ws = wb.active
    ws.title = "Monitoring positions"
    ws["A1"] = "%s %s: noise monitoring positions" % (W.OPERATOR, W.SITE)
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = "Schedule held under the site noise management plan, clause 2.1. Grid references are Irish " \
               "Transverse Mercator. Distances are to the blower house gable."
    ws["A3"] = "Maintained by the environmental engineer. Positions with a complaint reference were added " \
               "after the reference was logged."
    head = ["position_code", "dwelling_ref", "dwelling", "easting", "northing", "distance_m",
            "bearing_deg", "mic_height_m", "mounting", "screening", "complaint_ref"]
    for j, h in enumerate(head):
        c = ws.cell(row=5, column=1 + j, value=h)
        c.font = Font(bold=True)
        c.alignment = Alignment(horizontal="left")
    rng = random.Random(W.SEED + 5)
    for i, p in enumerate(W.POSITIONS):
        code, dref, desc, dist, bear = p[0], p[1], p[2], p[3], p[4]
        ang = math.radians(bear)
        e = 612430 + int(round(dist * math.sin(ang)))
        n = 748215 + int(round(dist * math.cos(ang)))
        cref = "" if W.COMPLAINTS[code] == 0 else "C%02d" % (1 + sorted(
            [c for c in W.CODES if W.COMPLAINTS[c] > 0], key=lambda c: -W.COMPLAINTS[c]).index(code))
        ws.append([])
        r = 6 + i
        for j, v in enumerate([code, dref, desc, e, n, dist, bear, 1.5, "free field, 3.5 m from facade",
                               W.SCREEN[code], cref]):
            ws.cell(row=r, column=1 + j, value=v)
    for col, wd in zip("ABCDEFGHIJK", (14, 12, 34, 9, 9, 11, 12, 13, 28, 42, 13)):
        ws.column_dimensions[col].width = wd
    ws.freeze_panes = "A6"
    path = os.path.join(target, FILES["positions"])
    wb.save(path)
    return path


def write_events(target):
    """The process operator's equipment log, local time, as the shift writes it."""
    rows = []
    stops = [(s, m, r, "planned") for s, m, r in W.PLANNED_STOPS] + \
            [(s, m, r, "unplanned") for s, m, r in W.UNPLANNED_STOPS]
    day = dt.date(2026, 8, 24)
    end = dt.date(2026, 10, 16)
    rng = random.Random(W.SEED + 17)
    while day <= end:
        if day.weekday() <= 5:
            for cf, t0 in zip(W.CENTRIFUGES, (6, 6)):
                h = t0
                mi = rng.choice([2, 4, 7, 9, 12, 14, 18])
                rows.append([dt.datetime(day.year, day.month, day.day, h, mi), cf, "START",
                             W.PEOPLE["operator"][1], "dewatering shift start"])
                rows.append([dt.datetime(day.year, day.month, day.day, 17, 40 + rng.choice([0, 5, 9, 14])),
                             cf, "STOP", W.PEOPLE["operator"][1], "dewatering shift end"])
        day += dt.timedelta(days=1)
    for start, mins, reason, kind in stops:
        who = W.PEOPLE["planner"][1] if kind == "planned" else W.PEOPLE["operator"][1]
        for eq in W.BLOWERS + W.CENTRIFUGES + [W.ENGINE]:
            rows.append([start, eq, "STOP", who, reason])
            rows.append([start + dt.timedelta(minutes=mins), eq, "START", who,
                         "returned to service after %s" % reason])
    # the blowers and the engine otherwise run on, with the quarterly oil change noted
    rows.append([dt.datetime(2026, 8, 24, 6, 5), W.ENGINE, "START", W.PEOPLE["operator"][1],
                 "returned to service after oil change"])
    for eq in W.BLOWERS:
        rows.append([dt.datetime(2026, 8, 24, 6, 12), eq, "START", W.PEOPLE["operator"][1],
                     "returned to service after oil change"])
    rows.sort(key=lambda r: (r[0], r[1], r[2]))
    out = [[r[0].strftime("%Y-%m-%d %H:%M"), r[1], r[2], r[3], r[4]] for r in rows]
    return _write_csv(os.path.join(target, FILES["events"]),
                      ["logged_at", "equipment", "event", "logged_by", "reason"], out)


def write_scada(target):
    """Fifteen-minute process channels. The biogas meter is a counter and rolls over; the engine's hour
    counter was replaced; one spell is missing where the link to the PLC dropped."""
    rng = np.random.default_rng(W.SEED + 23)
    t0 = dt.datetime(2026, 8, 1, 0, 0)
    n = int((dt.datetime(2026, 10, 17) - t0).total_seconds() // 900)
    stamps = [t0 + dt.timedelta(minutes=15 * i) for i in range(n)]
    stopped = np.zeros(n, dtype=bool)
    for start, mins, _ in W.PLANNED_STOPS + W.UNPLANNED_STOPS:
        e = start + dt.timedelta(minutes=mins)
        stopped |= np.array([(s >= start - dt.timedelta(minutes=14)) and (s < e) for s in stamps])
    hours = np.array([s.hour + s.minute / 60.0 for s in stamps])
    dows = np.array([s.weekday() for s in stamps])
    air = 4120 + 180 * np.sin(2 * math.pi * hours / 24.0 - 1.2) + rng.normal(0, 46, n)
    air = np.where(stopped, 0.0, air)
    cf_on = (hours >= 6.2) & (hours < 17.7) & (dows <= 5) & ~stopped
    feed = np.where(cf_on, 31.5 + rng.normal(0, 1.4, n), 0.0)
    gas_rate = np.where(stopped, 0.0, 212 + 9.5 * np.sin(2 * math.pi * hours / 24.0 + 0.4)
                        + rng.normal(0, 4.0, n))      # m3 an hour to the engine
    counter = (18640.0 + np.cumsum(gas_rate * 0.25)) % 100000.0
    kw = np.where(stopped, 0.0, 268 + 7.0 * np.sin(2 * math.pi * hours / 24.0 + 0.4) + rng.normal(0, 3.1, n))
    inflow = (96 + 34 * np.exp(-((hours - 10.5) ** 2) / 9.0) + 26 * np.exp(-((hours - 19.0) ** 2) / 7.0)
              + rng.normal(0, 4.5, n))
    eng_hours = np.cumsum(np.where(stopped, 0.0, 0.25))
    replaced = np.array([s >= dt.datetime(2026, 9, 18, 7, 0) for s in stamps])
    base = eng_hours[np.argmax(replaced)] if replaced.any() else 0.0
    eng_hours = np.where(replaced, eng_hours - base, 41820.0 + eng_hours)
    gap = np.array([(s >= dt.datetime(2026, 9, 24, 13, 0)) and (s < dt.datetime(2026, 9, 25, 9, 0))
                    for s in stamps])
    rows = []
    for i, s in enumerate(stamps):
        if gap[i]:
            continue
        rows.append([s.strftime("%Y-%m-%d %H:%M"), "%.0f" % max(air[i], 0.0), "%.1f" % max(feed[i], 0.0),
                     "%.0f" % counter[i], "%.1f" % max(kw[i], 0.0), "%.1f" % eng_hours[i],
                     "%.1f" % max(inflow[i], 0.0)])
    return _write_csv(os.path.join(target, FILES["scada"]),
                      ["logged_at", "blower_air_nm3_h", "centrifuge_feed_m3_h", "biogas_meter_m3",
                       "engine_export_kw", "engine_hours_run", "inlet_flow_m3_h"], rows)


def write_weather(target):
    """The met mast, UTC, ten-minute means. The anemometer was swapped and reports in km an hour after it;
    the rain gauge reports its tip count since midnight."""
    rows = []
    for i in range(SM.MET["n"]):
        stamp = SM.MET["t0"] + dt.timedelta(minutes=10 * i)
        ws = SM.MET["wind_ms"][i]
        if stamp.date() >= W.MAST_SWAP:
            val = "%.1f" % (ws * 3.6)
        else:
            val = "%.1f" % ws
        mid = dt.datetime(stamp.year, stamp.month, stamp.day)
        j0 = int((mid - SM.MET["t0"]).total_seconds() // 600)
        tips = int(round(SM.MET["rain_mm"][max(j0, 0):i + 1].sum() / W.RAIN_TIP_MM))
        rows.append([stamp.strftime("%Y-%m-%d %H:%M"), val, "%d" % int((37 + 211 * math.sin(i / 97.0)) % 360),
                     "%d" % tips, "%.1f" % SM.MET["temp_c"][i]])
    return _write_csv(os.path.join(target, FILES["weather"]),
                      ["measured_at_utc", "wind_speed", "wind_direction_deg", "rain_tips_today",
                       "air_temp_c"], rows)


def write_bands(target, series):
    """One-third-octave band levels, quarter hour, unweighted, on the three meters that carry the module."""
    rng = np.random.default_rng(W.SEED + 29)
    rows = []
    licensed = {m["id"] for m in W.METERS if m["bands"]}
    for sid in sorted(series):
        s = series[sid]
        if s["dep"]["meter"] not in licensed:
            continue
        lg = SM.logged(s)
        laeq = lg["laeq"]
        stamps = s["stamps"]
        plant_share = s["plant_e"] / (s["plant_e"] + s["resid_e"])
        for q in range(0, len(stamps) - 14, 15):
            sl = slice(q, q + 15)
            lev = 10.0 * math.log10(float(np.mean(np.power(10.0, laeq[sl] / 10.0))))
            ps = float(np.mean(plant_share[sl]))
            vals = []
            for b in BANDS:
                f = float(b)
                # broadband shape of the residual, plus the plant's own two tones
                shape = -11.0 - 7.5 * abs(math.log10(f / 160.0)) ** 1.9
                tone = 0.0
                if abs(f - 400.0) < 1.0:
                    tone = 9.2 * ps
                elif abs(f - 100.0) < 1.0:
                    tone = 7.4 * ps
                elif abs(f - 800.0) < 1.0:
                    tone = 2.1 * ps
                vals.append(lev + shape + tone + float(rng.normal(0, 0.35)))
            rows.append([W_serial(s["dep"]["meter"]), stamps[q].strftime("%Y-%m-%d %H:%M")]
                        + ["%.1f" % v for v in vals])
    rows.sort(key=lambda r: (r[0], r[1]))
    return _write_csv(os.path.join(target, FILES["bands"]),
                      ["meter_serial", "logged_at"] + ["lzeq_%s_hz" % str(b).replace(".", "p")
                                                       for b in BANDS], rows)


def write_calibration(target):
    rows = []
    for m in W.METERS:
        rows.append([m["serial"], m["model"], "CAL-4621", "2026-03-12",
                     "2027-03-11", "%.1f" % W.CAL_REF, "%.1f" % m["pre"], "%.1f" % m["post"],
                     "field check at 1 kHz before and after each deployment"])
    return _write_csv(os.path.join(target, FILES["calibration"]),
                      ["meter_serial", "model", "calibrator_serial", "calibrated_on",
                       "calibration_due", "calibrator_level_db", "field_check_before_db",
                       "field_check_after_db", "note"], rows)


def write_complaints(target):
    """The complaints register. The question does not use it (metadata.json declares it)."""
    from openpyxl import Workbook
    from openpyxl.styles import Font
    wb = Workbook()
    ws = wb.active
    ws.title = "Complaints 2026"
    ws["A1"] = "%s %s: noise complaints received" % (W.OPERATOR, W.SITE)
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = "Logged under the site noise management plan, clause 5.1. One row per contact."
    head = ["complaint_ref", "received_on", "dwelling_ref", "received_by", "description", "response_sent_on"]
    for j, h in enumerate(head):
        ws.cell(row=4, column=1 + j, value=h).font = Font(bold=True)
    texts = ["hum carrying across the yard in the evening", "low drone, worse with the wind from the plant",
             "constant noise at night, cannot open the bedroom window", "whine from the new building",
             "humming through the day, worse since the summer", "noise from the plant at the gable",
             "drone in the evening, children cannot sleep", "steady hum from the direction of the works"]
    rng = random.Random(W.SEED + 31)
    rows, n = [], 0
    for code in sorted([c for c in W.CODES if W.COMPLAINTS[c] > 0], key=lambda c: -W.COMPLAINTS[c]):
        ref = "C%02d" % (1 + sorted([c for c in W.CODES if W.COMPLAINTS[c] > 0],
                                    key=lambda c: -W.COMPLAINTS[c]).index(code))
        for k in range(W.COMPLAINTS[code]):
            d = dt.date(2026, 6, 4) + dt.timedelta(days=11 * n + 3 * k)
            rows.append([ref, d.isoformat(), W.BY_CODE[code][1], W.PEOPLE["engineer"][1],
                         texts[(n + k) % len(texts)], (d + dt.timedelta(days=rng.choice([4, 6, 9]))).isoformat()])
            n += 1
    rows.sort(key=lambda r: (r[1], r[0]))
    for i, r in enumerate(rows):
        for j, v in enumerate(r):
            ws.cell(row=5 + i, column=1 + j, value=v)
    for col, wd in zip("ABCDEF", (14, 13, 13, 12, 52, 17)):
        ws.column_dimensions[col].width = wd
    path = os.path.join(target, FILES["complaints"])
    wb.save(path)
    return path


def write_effluent(target):
    """The works' discharge monitoring. Nothing in the question reads it."""
    rng = np.random.default_rng(W.SEED + 37)
    rows = []
    day = dt.date(2026, 7, 1)
    while day <= dt.date(2026, 10, 15):
        if day.weekday() in (0, 2, 4):
            rows.append([day.isoformat(), "final effluent",
                         "%.1f" % max(2.0, rng.normal(9.8, 2.6)),
                         "%.1f" % max(1.0, rng.normal(6.4, 1.9)),
                         "%.1f" % max(0.5, rng.normal(3.1, 0.9)),
                         "%.2f" % max(0.05, rng.normal(0.42, 0.14)),
                         "%.1f" % rng.normal(7.3, 0.2), "composite, 24 hour"])
        day += dt.timedelta(days=1)
    return _write_csv(os.path.join(target, FILES["effluent"]),
                      ["sampled_on", "sample_point", "bod_mg_l", "cod_mg_l", "suspended_solids_mg_l",
                       "ammonia_mg_l", "ph", "sample_type"], rows)


def write_manifest(target, counts):
    rows = [
        [FILES["levels"], "parquet", counts["levels"], "measured_at_utc",
         "every logged minute from the five meters, as downloaded; stamps are UTC",
         "the download of D%02d was repeated after a card read error" % counts["dup_dep"]],
        [FILES["deployments"], "csv", counts["deployments"], "start_date",
         "which meter stood at which position, with its field checks", ""],
        [FILES["positions"], "xlsx", len(W.POSITIONS), "",
         "the monitoring position schedule held under the plan", ""],
        [FILES["plan"], "pdf", "", "", "the site noise management plan, revision 4", "clauses 1 to 6"],
        [FILES["notes"], "md", "", "", "the monitoring technician's notes on the survey", ""],
        [FILES["events"], "csv", counts["events"], "logged_at",
         "the process operator's equipment log, local time", ""],
        [FILES["scada"], "csv", counts["scada"], "logged_at",
         "fifteen-minute process channels from the plant PLC, local time",
         "no records 24 September 13:00 to 25 September 09:00, link to the PLC down"],
        [FILES["weather"], "csv", counts["weather"], "measured_at_utc",
         "the met mast, ten-minute means, UTC",
         "anemometer replaced 20 September, the replacement reports in km an hour"],
        [FILES["bands"], "csv", counts["bands"], "logged_at",
         "one-third-octave band levels where the meter carries the module", ""],
        [FILES["calibration"], "csv", len(W.METERS), "calibrated_on",
         "meter and calibrator certificates with each deployment's field checks", ""],
        [FILES["complaints"], "xlsx", counts["complaints"], "received_on",
         "noise complaints received in 2026", ""],
        [FILES["effluent"], "csv", counts["effluent"], "sampled_on",
         "final effluent monitoring results", ""],
    ]
    return _write_csv(os.path.join(target, FILES["manifest"]),
                      ["file", "format", "rows", "date_column", "contents", "known_gaps"], rows)


def set_mtimes(target):
    stamp = dt.datetime(2026, 10, 16, 17, 25, 0).timestamp()
    for name in sorted(os.listdir(target)):
        os.utime(os.path.join(target, name), (stamp, stamp))
