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
A_WEIGHT = {25: -44.7, 31.5: -39.4, 40: -34.6, 50: -30.2, 63: -26.2, 80: -22.5, 100: -19.1,
            125: -16.1, 160: -13.4, 200: -10.9, 250: -8.6, 315: -6.6, 400: -4.8, 500: -3.2,
            630: -1.9, 800: -0.8, 1000: 0.0, 1250: 0.6, 1600: 1.0, 2000: 1.2, 2500: 1.3,
            3150: 1.2, 4000: 1.0, 5000: 0.5, 6300: -0.1, 8000: -1.1, 10000: -2.5, 12500: -4.3}
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
            serial, stamp = row[0], dt.datetime.strptime(row[1], "%Y-%m-%d %H:%M")
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
    adj = 10.0 * math.log10(np.mean(np.power(10.0, np.array(nb) / 10.0)))
    return BANDS[i], bool(levels[i] - adj >= 5.0), round(float(levels[i] - adj), 2)


def weekly_plant(target):
    """A3: the biogas burned, the blower air delivered and the centrifuge runs, per survey week."""
    import csv as _c
    rows = list(_c.DictReader(open(os.path.join(target, PK.FILES["scada"]), encoding="utf-8")))
    out = {}
    prev = {}
    for r in rows:
        t = dt.datetime.strptime(r["logged_at"], "%Y-%m-%d %H:%M")
        wk = week_of(t.date())
        if wk is None:
            prev[0] = float(r["biogas_meter_m3"])
            prev["feed"] = float(r["centrifuge_feed_m3_h"])
            continue
        d = out.setdefault(wk, {"gas": 0.0, "air": 0.0, "runs": 0, "last": None})
        c = float(r["biogas_meter_m3"])
        if prev.get(0) is not None:
            step = c - prev[0]
            if step < -50000:
                step += 100000.0
            if step >= 0:
                d["gas"] += step
        prev[0] = c
        d["air"] += float(r["blower_air_nm3_h"]) * 0.25
        feed = float(r["centrifuge_feed_m3_h"])
        if feed > 0 and prev.get("feed", 0.0) == 0:
            d["runs"] += 1
        prev["feed"] = feed
    return {k: {"biogas_m3": int(round(v["gas"])), "blower_air_knm3": int(round(v["air"] / 1000.0)),
                "centrifuge_runs": v["runs"]} for k, v in sorted(out.items())}




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
    rows = []
    for c in W.CODES:
        rows.append({
            "position": c, "dwelling": W.BY_CODE[c][1], "dwelling_name": W.BY_CODE[c][2],
            "specific_db": round(spec[c], 1), "specific_raw": spec[c],
            "valid_minutes": r[c]["minutes_valid"], "excluded_minutes": r[c]["minutes_excluded"],
            "band_hz": tones[c]["band_hz"], "tone": tones[c]["tone"],
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
    }
    g["slates"] = AN.all_slates(r)
    return g
