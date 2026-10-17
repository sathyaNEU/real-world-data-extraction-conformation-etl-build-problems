"""The answer: every graded figure, computed from the built pack."""
import datetime as dt
import math
import os

import numpy as np

import analysis as AN
import pack as PK
import sim as SM
import world as W

BANDS = PK.BANDS
A_WEIGHT = PK.A_WEIGHT
CAP = 5


def week_of(day):
    for i, w in enumerate(W.WEEKS):
        if w <= day <= w + dt.timedelta(days=6):
            return i
    return None


def band_rows(target):
    """Per position: the energetic mean of the shipped band levels over its assessment-period quarter hours."""
    import csv as _c
    deps = list(_c.DictReader(open(os.path.join(target, PK.FILES["deployments"]), encoding="utf-8")))
    by_meter = {}
    for d in deps:
        by_meter.setdefault(d["meter_serial"], []).append(
            (dt.date.fromisoformat(d["start_date"]), dt.date.fromisoformat(d["end_date"]), d["position_code"]))
    acc = {}
    with open(os.path.join(target, PK.FILES["bands"]), encoding="utf-8") as fh:
        rd = _c.reader(fh)
        head = next(rd)
        cols = [h for h in head[2:]]
        for row in rd:
            serial = row[0]
            stamp = (dt.datetime.strptime(row[1], "%Y-%m-%d %H:%M")
                     + dt.timedelta(hours=SM.LOCAL_OFFSET))      # the band export is stamped UTC too
            if stamp.weekday() > 4 or not (W.DAY_START <= stamp.hour < W.DAY_END):
                continue
            code = None
            for a, b, c in by_meter.get(serial, []):
                if a <= stamp.date() <= b:
                    code = c
                    break
            if code is None:
                continue
            acc.setdefault(code, []).append([float(x) for x in row[2:]])
    out = {}
    for code, rows in acc.items():
        a = np.array(rows)
        out[code] = 10.0 * np.log10(np.mean(np.power(10.0, a / 10.0), axis=0))
    return out


def tone_call(levels):
    """The highest band and whether a tone is prominent there (plan 4.3)."""
    i = int(np.argmax(levels))
    lo = levels[i - 1] if i > 0 else None
    hi = levels[i + 1] if i < len(levels) - 1 else None
    nb = [x for x in (lo, hi) if x is not None]
    adj = float(np.mean(nb))                     # plan 4.3: the mean of the two adjacent band levels
    return BANDS[i], bool(levels[i] - adj >= 5.0), round(float(levels[i] - adj), 2)


def weekly_plant(target):
    """A3: the biogas burned and the blower air delivered, read off the counters at the week boundaries
    (plan 5.1), and the centrifuge runs the equipment log carries in the week (plan 5.2)."""
    import csv as _c
    scada = {}
    for r in _c.DictReader(open(os.path.join(target, PK.FILES["scada"]), encoding="utf-8")):
        scada[dt.datetime.strptime(r["logged_at"], "%Y-%m-%d %H:%M")] = r
    starts = []
    for r in _c.DictReader(open(os.path.join(target, PK.FILES["events"]), encoding="utf-8")):
        if r["equipment"] in W.CENTRIFUGES and r["event"] == "START":
            starts.append(dt.datetime.strptime(r["logged_at"], "%Y-%m-%d %H:%M"))
    out = {}
    for i, wk in enumerate(W.WEEKS):
        a = dt.datetime(wk.year, wk.month, wk.day)
        b = a + dt.timedelta(days=7)
        ra, rb = scada[a], scada[b]
        gas = float(rb["biogas_meter_m3"]) - float(ra["biogas_meter_m3"])
        while gas < 0:
            gas += 100000.0
        air = float(rb["blower_air_total_knm3"]) - float(ra["blower_air_total_knm3"])
        out[i] = {"biogas_m3": int(round(gas)),
                  "blower_air_knm3": int(round(air)),
                  "centrifuge_runs": sum(1 for t in starts if a <= t < b)}
    return out


def log_runs(target):
    """Every centrifuge run the equipment log carries, as plan 5.2 defines it: a start, and the stop the
    log records for the same machine."""
    import csv as _c
    opens, runs = {}, []
    rows = sorted(_c.DictReader(open(os.path.join(target, PK.FILES["events"]), encoding="utf-8")),
                  key=lambda r: r["logged_at"])
    for r in rows:
        if r["equipment"] not in W.CENTRIFUGES:
            continue
        t = dt.datetime.strptime(r["logged_at"], "%Y-%m-%d %H:%M")
        if r["event"] == "START":
            opens[r["equipment"]] = t
        elif r["equipment"] in opens:
            runs.append((opens.pop(r["equipment"]), t))
    return sorted(runs)


def assessment_days(target):
    """Per position, the weekday assessment windows its deployments cover, in local time."""
    import csv as _c
    out = {}
    for d in _c.DictReader(open(os.path.join(target, PK.FILES["deployments"]), encoding="utf-8")):
        a = dt.date.fromisoformat(d["start_date"])
        b = dt.date.fromisoformat(d["end_date"])
        for k in range((b - a).days + 1):
            day = a + dt.timedelta(days=k)
            if day.weekday() > 4:
                continue
            out.setdefault(d["position_code"], []).append(
                (dt.datetime(day.year, day.month, day.day, W.DAY_START),
                 dt.datetime(day.year, day.month, day.day, W.DAY_END)))
    return out


def plant_state_per_position(target):
    """A2: the minutes of each position's assessment period a centrifuge was running, and the number of
    runs that reached into it."""
    runs = log_runs(target)
    out = {}
    for code, wins in assessment_days(target).items():
        mins = 0
        for lo, hi in wins:
            iv = sorted((max(a, lo), min(b, hi)) for a, b in runs if a < hi and b > lo)
            cur = None
            for a, b in iv:
                if cur and a <= cur[1]:
                    cur = (cur[0], max(cur[1], b))
                else:
                    if cur:
                        mins += int((cur[1] - cur[0]).total_seconds() // 60)
                    cur = (a, b)
            if cur:
                mins += int((cur[1] - cur[0]).total_seconds() // 60)
        n = sum(1 for a, b in runs if any(a < hi and b > lo for lo, hi in wins))
        out[code] = {"centrifuge_minutes": mins, "centrifuge_runs": n}
    return out


def engine_hours(target):
    """A3: the hours the gas engine ran in each survey week, from its own hour counter (plan 5.1). The
    counter was changed during the inspection on 15 September, with the engine down, and starts again
    from zero."""
    import csv as _c
    rows = [(dt.datetime.strptime(r["logged_at"], "%Y-%m-%d %H:%M"), float(r["engine_hours_run"]))
            for r in _c.DictReader(open(os.path.join(target, PK.FILES["scada"]), encoding="utf-8"))]
    by_t = dict(rows)
    out = {}
    for i, wk in enumerate(W.WEEKS):
        a = dt.datetime(wk.year, wk.month, wk.day)
        b = a + dt.timedelta(days=7)
        seg, prev_t = 0.0, None
        inside = [(t, v) for t, v in rows if a <= t <= b]
        for j in range(1, len(inside)):
            step = inside[j][1] - inside[j - 1][1]
            if step < 0:                      # the counter was changed inside this week
                step = inside[j][1]
            seg += step
        out[i] = round(seg, 1)
    return out


def compute(target, series, dup):
    frames = AN.position_frames(series)
    r = AN.routes(frames)
    spec = {c: r[c]["specific"] for c in W.CODES}
    slate, margin, nxt = AN.slate(spec, CAP)
    bands = band_rows(target)
    tones = {}
    for c in W.CODES:
        if c in bands:
            b, prom, excess = tone_call(bands[c])
            tones[c] = {"band_hz": b, "tone": prom, "excess_db": excess}
        else:
            tones[c] = {"band_hz": None, "tone": None, "excess_db": None}
    weekly = weekly_plant(target)
    eng = engine_hours(target)
    for k in weekly:
        weekly[k]["engine_hours"] = eng[k]
    plant = plant_state_per_position(target)
    rows = []
    for c in W.CODES:
        rows.append({
            "position": c, "dwelling": W.BY_CODE[c][1], "dwelling_name": W.BY_CODE[c][2],
            "specific_db": round(spec[c], 1), "specific_raw": spec[c],
            "valid_minutes": r[c]["minutes_valid"], "excluded_minutes": r[c]["minutes_excluded"],
            "band_hz": tones[c]["band_hz"], "tone": tones[c]["tone"],
            "centrifuge_minutes": plant[c]["centrifuge_minutes"],
            "centrifuge_runs": plant[c]["centrifuge_runs"],
            "total_db": round(r[c]["total"], 1), "residual_db": round(r[c]["resid"], 1),
            "stop_minutes": r[c]["minutes_stop"], "distance_m": W.BY_CODE[c][3],
        })
    ordered = sorted(rows, key=lambda x: -x["specific_raw"])
    g = {
        "slate": slate,
        "slate_ordered": [x["position"] for x in ordered[:CAP]],
        "slate_dwellings": [(x["position"], x["dwelling"], x["dwelling_name"], x["specific_db"])
                            for x in ordered[:CAP]],
        "sixth": ordered[CAP]["position"],
        "sixth_dwelling": ordered[CAP]["dwelling"],
        "sixth_level": ordered[CAP]["specific_db"],
        "margin_db": round(ordered[CAP - 1]["specific_raw"] - ordered[CAP]["specific_raw"], 1),
        "rows": rows, "ordered": ordered, "routes": r, "bands": bands, "tones": tones,
        "weekly": weekly, "cap": CAP,
        "tone_positions": [c for c in W.CODES if tones[c]["tone"]],
        "tone_bands": sorted({tones[c]["band_hz"] for c in W.CODES if tones[c]["tone"]}),
        "deployment_count": len(SM.deployments()),
        "corrected_count": len([d for d in SM.deployments() if d["correction"] != 0.0]),
    }
    g["slates"] = AN.all_slates(r)
    g["series"] = series
    g["reads"] = [PK.FILES[k] for k in ("levels", "deployments", "positions", "plan", "notes",
                                        "events", "weather", "bands", "calibration", "scada")]
    g["dup_rows"] = dup_arrays(series)
    return g


def dup_arrays(series):
    """The repeated download's minutes, as position_frames takes them for the keep-both reading."""
    for sid in sorted(series):
        s = series[sid]
        if (s["dep"]["code"], s["dep"]["k"]) != W.DUP_DEPLOYMENT:
            continue
        m = np.array([(x.date() == W.DUP_DAY) and (W.DUP_FROM <= x.hour < W.DUP_TO)
                      for x in s["stamps"]])
        dev = SM.dep_dev(s["dep"])
        adj = SM.dep_correction(s["dep"])
        laeq = (np.where(s["nd"], W.NODATA_VALUE, np.round(s["laeq"] + dev, 1) - adj))[m]
        la90 = (np.where(s["nd"], W.NODATA_VALUE, np.round(s["la90"] + dev, 1) - adj))[m]
        stamps = [x for x, k in zip(s["stamps"], m) if k]
        am = AN.np.array([(x.weekday() <= 4) and (W.DAY_START <= x.hour < W.DAY_END) for x in stamps])
        vm = s["vm"][m]
        st = AN.stop_mask(stamps)
        pl = AN.planned_mask(stamps)
        return (s["dep"]["code"], laeq, la90, am & vm, st, pl, vm)
    return None
