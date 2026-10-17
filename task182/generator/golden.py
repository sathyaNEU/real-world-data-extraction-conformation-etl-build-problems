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
            (dt.datetime.strptime(d["deployed_at"], "%Y-%m-%d %H:%M"),
             dt.datetime.strptime(d["collected_at"], "%Y-%m-%d %H:%M"), d["position_code"]))
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
                if a <= stamp <= b:
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


def hist_rows(target):
    """The historian's rows by stamp, and the stamps whose row is no reading of its own.

    When the radio link to the PLC drops the interface holds the last value it had and writes it again, so
    the row is there and the quarter hour's reading is not. Such a row is found by what it is and by
    nothing that is written down: every channel the same as the row before, while its own flow channels
    read above zero and its counters stand still, which no reading of a running plant can be. The rows the
    weekly inspection leaves are the same row again too, and they are readings: the works is stopped, the
    flows read zero and a counter that does not advance is the state of the plant. The flow channels are
    what separate the two."""
    import csv as _c
    rows, held, prev = {}, set(), None
    with open(os.path.join(target, PK.FILES["scada"]), encoding="utf-8") as fh:
        for r in _c.DictReader(fh):
            t = dt.datetime.strptime(r["logged_at"], "%Y-%m-%d %H:%M")
            rows[t] = r
            if prev is not None and all(v == prev[k] for k, v in r.items() if k != "logged_at"):
                flowing = (float(r["aeration_header_nm3_h"]) > 0.0
                           or float(r["bl03_discharge_nm3_h"]) > 0.0)
                if flowing:
                    held.add(t)
            prev = r
    return rows, held


def air_total(row):
    """The air the blowers delivered, off the two totalisers the plant's three machines are metered on."""
    return float(row["aeration_header_total_knm3"]) + float(row["bl03_discharge_total_knm3"])


def position_windows(target):
    """Per position, per deployment, the weekday assessment windows the deployment covered, in local
    time, from the deployment record's own stamps."""
    import csv as _c
    out = {}
    for d in sorted(_c.DictReader(open(os.path.join(target, PK.FILES["deployments"]), encoding="utf-8")),
                    key=lambda r: r["deployed_at"]):
        a = dt.datetime.strptime(d["deployed_at"], "%Y-%m-%d %H:%M")
        b = dt.datetime.strptime(d["collected_at"], "%Y-%m-%d %H:%M")
        wins = []
        for k in range((b.date() - a.date()).days + 1):
            day = a.date() + dt.timedelta(days=k)
            if day.weekday() > 4:
                continue
            lo = dt.datetime(day.year, day.month, day.day, W.DAY_START)
            hi = dt.datetime(day.year, day.month, day.day, W.DAY_END)
            if lo >= a and hi <= b:
                wins.append((lo, hi))
        out.setdefault(d["position_code"], []).append(wins)
    return out


def unrecorded(rows, held, lo, hi):
    """Quarter hours in (lo, hi] the historian holds no reading of its own for, and the longest unbroken
    run of them: the ones it wrote no row for, and the ones whose row is the quarter hour before it
    written again while the plant ran on, which is what the interface does with the link down."""
    n, run, longest, t = 0, 0, 0, lo + dt.timedelta(minutes=15)
    while t <= hi:
        if t not in rows or t in held:
            n += 1
            run += 1
            longest = max(longest, run)
        else:
            run = 0
        t += dt.timedelta(minutes=15)
    return n, longest


def plant_behind_level(target):
    """A2 and A3: the air the blowers delivered through each deployment's assessment hours, and the
    quarter hours of the position's assessment period the historian did not record the plant's state in."""
    rows, held = hist_rows(target)
    out = {}
    for code, deps in position_windows(target).items():
        air, miss, longest = 0.0, 0, 0
        for wins in deps:
            for lo, hi in wins:
                air += air_total(rows[hi]) - air_total(rows[lo])
                n, lg = unrecorded(rows, held, lo, hi)
                miss += n
                longest = max(longest, lg)
        out[code] = {"air_knm3": round(air, 1), "unrecorded_quarter_hours": miss,
                     "longest_unrecorded_run": longest}
    return out


def weekly_plant(target):
    """A4: per survey week, the air the blowers delivered off the two totalisers at the week's own
    boundaries (plan 5.1), and the quarter hours the historian did not record the plant's state in."""
    rows, held = hist_rows(target)
    out = {}
    for i, wk in enumerate(W.WEEKS):
        a = dt.datetime(wk.year, wk.month, wk.day)
        b = a + dt.timedelta(days=7)
        n, lg = unrecorded(rows, held, a, b)
        out[i] = {"blower_air_knm3": int(round(air_total(rows[b]) - air_total(rows[a]))),
                  "blower_air_knm3_raw": round(air_total(rows[b]) - air_total(rows[a]), 1),
                  "unrecorded_quarter_hours": n, "longest_unrecorded_run": lg}
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
    plant = plant_behind_level(target)
    rows = []
    for c in W.CODES:
        rows.append({
            "position": c, "dwelling": W.BY_CODE[c][1], "dwelling_name": W.BY_CODE[c][2],
            "specific_db": round(spec[c], 1), "specific_raw": spec[c],
            "valid_minutes": r[c]["minutes_valid"], "excluded_minutes": r[c]["minutes_excluded"],
            "band_hz": tones[c]["band_hz"], "tone": tones[c]["tone"],
            "air_knm3": plant[c]["air_knm3"],
            "unrecorded_quarter_hours": plant[c]["unrecorded_quarter_hours"],
            "longest_unrecorded_run": plant[c]["longest_unrecorded_run"],
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
