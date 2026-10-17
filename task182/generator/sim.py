"""The survey, minute by minute: the plant's contribution, the residual sound and what the meters logged.

The true levels are never shipped. The meters' columns are the plant and the residual added in energy, with
the deployment's calibration deviation left in, quantised the way the instrument reports.
"""
import datetime as dt
import math

import numpy as np

import world as W

MIN = 60
LOCAL_OFFSET = 1          # Irish Standard Time through the whole survey (last Sunday in October is later)


def _e(db):
    return np.power(10.0, np.asarray(db, dtype=float) / 10.0)


def _db(e):
    return 10.0 * np.log10(np.maximum(np.asarray(e, dtype=float), 1e-12))


def week_minutes(start):
    """Local naive minute stamps for the seven days from Monday 00:00."""
    base = dt.datetime(start.year, start.month, start.day)
    n = 7 * 24 * 60
    return base, np.arange(n)


def met_series():
    """Ten-minute met records for the survey, plus per-minute wind and rain rate for the simulation."""
    rng = np.random.default_rng(W.SEED + 11)
    t0 = dt.datetime(2026, 8, 30)
    n10 = int(((dt.datetime(2026, 10, 17) - t0).total_seconds()) // 600)
    hours = np.arange(n10) / 6.0
    # wind: a slow synoptic swing plus a diurnal lift, never negative
    wind = (3.05 + 1.35 * np.sin(2 * math.pi * hours / 86.0 + 0.7)
            + 0.95 * np.sin(2 * math.pi * hours / 23.0 - 1.1)
            + rng.normal(0, 0.45, n10))
    wind = np.clip(wind, 0.2, 12.0)
    # rain: wet spells, a few per survey
    rain = np.zeros(n10)
    for c in rng.choice(n10 - 60, size=11, replace=False):
        dur = int(rng.integers(3, 16))
        rain[c:c + dur] += np.abs(rng.normal(0.20, 0.13, dur))
    temp = (11.6 + 4.1 * np.sin(2 * math.pi * hours / 24.0 - 2.2)
            + 2.2 * np.sin(2 * math.pi * hours / 150.0) + rng.normal(0, 0.4, n10))
    # what the mast's file carries, and what a reader of that file recovers
    swap = np.array([(t0 + dt.timedelta(minutes=10 * i)).date() >= W.MAST_SWAP for i in range(n10)])
    shipped_wind = np.where(swap, np.round(wind * 3.6, 1), np.round(wind, 1))
    eff_wind = np.where(swap, np.round(shipped_wind / 3.6, 6), shipped_wind)
    # no record may sit on the plan's 5 m a second, in either unit: the mast is nudged one tick clear
    for _ in range(3):
        tie = np.abs(eff_wind - 5.0) < 0.03
        if not tie.any():
            break
        step = np.where(swap, 0.4, 0.1)
        shipped_wind = np.where(tie & (eff_wind <= 5.0), np.round(shipped_wind - step, 1),
                                np.where(tie, np.round(shipped_wind + step, 1), shipped_wind))
        eff_wind = np.where(swap, np.round(shipped_wind / 3.6, 6), shipped_wind)
    day_index = np.array([(t0 + dt.timedelta(minutes=10 * i)).toordinal() for i in range(n10)])
    tips = np.zeros(n10, dtype=int)
    acc = 0.0
    last_day = day_index[0]
    for i in range(n10):
        if day_index[i] != last_day:
            acc = 0.0
            last_day = day_index[i]
        acc += rain[i]
        tips[i] = int(round(acc / W.RAIN_TIP_MM))
    inc = np.diff(np.concatenate([[0], tips]))
    inc = np.where(day_index != np.concatenate([[day_index[0]], day_index[:-1]]), tips, inc)
    rain_mm_shipped = inc * W.RAIN_TIP_MM
    return {"t0": t0, "n": n10, "wind_ms": wind, "wind_eff": eff_wind, "wind_shipped": shipped_wind,
            "rain_mm": rain, "rain_mm_shipped": rain_mm_shipped, "tips": tips,
            "temp_c": np.round(temp, 1)}


MET = met_series()


def met_index(stamps_local):
    """Index into the ten-minute met record for local-time minute stamps. The mast's file is stamped UTC,
    so the local stamp is taken back to UTC first, exactly as a reader of the two files has to."""
    secs = np.array([(s - dt.timedelta(hours=LOCAL_OFFSET) - MET["t0"]).total_seconds()
                     for s in stamps_local])
    return np.clip((secs // 600).astype(int), 0, MET["n"] - 1)


def rain_rate_mmh():
    """Rolling hourly rain rate on the ten-minute grid, mm an hour, from the tip counts the mast file
    carries: six consecutive ten-minute increments, the hour ending at the record."""
    r = MET["rain_mm_shipped"]
    out = np.zeros(len(r))
    for i in range(len(r)):
        out[i] = r[max(0, i - 5):i + 1].sum()
    return out


RAIN_H = rain_rate_mmh()


def centrifuge_window(day):
    """When the two centrifuges ran on a date: the dewatering shift, pushed back behind the weekly
    inspection on the day it falls. One definition, used by the simulation and by the shipped log."""
    if day.weekday() > 5:
        return None
    stops = [s for s, m, _ in W.PLANNED_STOPS if s.date() == day]
    o = day.toordinal()
    if stops:
        start = stops[0] + dt.timedelta(minutes=W.PLANNED_STOPS[0][1] + 5 + 2 * (o % 5))
    else:
        start = dt.datetime(day.year, day.month, day.day, 6, 2 + 2 * (o % 7))
    return start, dt.datetime(day.year, day.month, day.day, 17, 40 + 3 * (o % 4))


def all_down():
    """Every interval in which the blowers, the centrifuges and the engine are all down."""
    return [(s, s + dt.timedelta(minutes=m)) for s, m, _ in W.PLANNED_STOPS + W.UNPLANNED_STOPS]


def plant_state(stamps_local):
    """Energy factor of the plant's own sound: 0 in a stop, 1 running, more while a centrifuge runs."""
    cf = np.zeros(len(stamps_local), dtype=bool)
    days = sorted({s.date() for s in stamps_local})
    wins = {d: centrifuge_window(d) for d in days}
    for i, s in enumerate(stamps_local):
        w = wins[s.date()]
        if w and w[0] <= s < w[1]:
            cf[i] = True
    k = np.where(cf, 1.22, 1.0)
    for start, end in all_down():
        inside = np.array([(s >= start) and (s < end) for s in stamps_local])
        k = np.where(inside, 0.0, k)
    return k


def residual_shape(code, stamps_local, seed):
    """Unit-scale residual energy per minute: a steady part that drifts slowly, plus passby events."""
    p = W.BY_CODE[code]
    ev, strm = p[8], p[9]
    rng = np.random.default_rng(seed)
    n = len(stamps_local)
    hours = np.array([s.hour + s.minute / 60.0 for s in stamps_local])
    dows = np.array([s.weekday() for s in stamps_local])
    idx = met_index(stamps_local)
    wind = MET["wind_ms"][idx]
    # slow variation of the steady part, in dB: weather and the stream
    sv = W.SLOW[code]
    slow = sv * np.sin(2 * math.pi * np.arange(n) / (1440 * 2.3) + 0.9 * W.CODES.index(code))
    slow = slow + 0.055 * (wind - wind.mean()) * sv
    jit = np.zeros(n)
    a = 0.985
    wn = rng.normal(0.0, W.JITTER[code] * math.sqrt(1 - a * a), n)
    for i in range(n):
        jit[i] = a * jit[i - 1] + wn[i] if i else wn[i]
    steady = _e(slow + jit)
    # road traffic diurnal shape on the event rate
    shape = (0.78 + 0.30 * np.exp(-((hours - 8.3) ** 2) / 2.2)
             + 0.34 * np.exp(-((hours - 17.6) ** 2) / 3.0)
             + 0.18 * np.exp(-((hours - 12.5) ** 2) / 8.0))
    shape = np.where(dows <= 4, shape, shape * 0.82)
    lam = ev * shape / 60.0
    hit = rng.random(n) < lam
    amp = np.where(hit, _e(rng.uniform(W.EVENT_DB[code][0], W.EVENT_DB[code][1], n)), 0.0)
    extra = amp * steady
    # a second minute of decay on the louder events
    extra = extra + np.concatenate([[0.0], extra[:-1] * 0.35])
    total = strm * steady.mean() + (1.0 - strm) * steady + extra
    # within-minute statistics: the quiet part of a minute, and its loudest second
    quiet = strm * steady.mean() + (1.0 - strm) * steady * _e(-rng.uniform(0.25, 1.1, n))
    loud = total + extra * 2.1 + (1.0 - strm) * steady * _e(rng.uniform(1.0, 7.0, n))
    tiny = quiet * _e(-rng.uniform(0.4, 1.6, n))
    return total, quiet, loud, tiny


def assessment_mask(stamps_local):
    hours = np.array([s.hour + s.minute / 60.0 for s in stamps_local])
    dows = np.array([s.weekday() for s in stamps_local])
    return (dows <= 4) & (hours >= W.DAY_START) & (hours < W.DAY_END)


def validity_mask(stamps_local):
    """Plan 4.2: a minute is invalid where its met record shows rain above 0.5 mm an hour or wind above 5 m/s."""
    idx = met_index(stamps_local)
    return (RAIN_H[idx] <= 0.5) & (MET["wind_eff"][idx] <= 5.0)


def deployments():
    """Every deployment: position, meter, week, local start and end, mounting."""
    out = []
    for code in W.CODES:
        for k, (wk, meter) in enumerate(W.SCHEDULE[code]):
            start = W.WEEKS[wk]
            out.append({"code": code, "meter": meter, "week": wk, "start": start,
                        "end": start + dt.timedelta(days=6), "mount": W.MOUNT[k], "k": k})
    out.sort(key=lambda d: (d["start"], d["meter"]))
    for i, d in enumerate(out, start=1):
        d["id"] = "D%02d" % i
    return out


def build(codes=None):
    """Every deployment's minute series, with the plant and residual normalised on the position's own
    valid assessment minutes outside the plant's stops."""
    deps = deployments()
    by_code = {}
    for d in deps:
        by_code.setdefault(d["code"], []).append(d)
    series = {}
    for code, ds in by_code.items():
        if codes is not None and code not in codes:
            continue
        p = W.BY_CODE[code]
        S_t, R_t = p[5], p[6]
        parts = []
        for d in ds:
            base, mins = week_minutes(d["start"])
            stamps = [base + dt.timedelta(minutes=int(m)) for m in mins]
            k = plant_state(stamps)
            res, quiet, loud, tiny = residual_shape(code, stamps, W.SEED + 7919 * W.CODES.index(code) + d["week"])
            am = assessment_mask(stamps)
            vm = validity_mask(stamps)
            parts.append({"dep": d, "stamps": stamps, "k": k, "res": res, "quiet": quiet,
                          "loud": loud, "tiny": tiny, "am": am, "vm": vm})
        use = np.concatenate([(pp["am"] & pp["vm"] & (pp["k"] > 0)) for pp in parts])
        kk = np.concatenate([pp["k"] for pp in parts])
        rr = np.concatenate([pp["res"] for pp in parts])
        # plant: energetic mean over the valid assessment minutes outside stops equals S
        gp = _e(S_t + W.SHIFT.get(code, 0.0)) / kk[use].mean()
        # residual: energetic mean over the same minutes equals R
        gr = _e(R_t) / rr[use].mean()
        for pp in parts:
            pe = gp * pp["k"]
            re = gr * pp["res"]
            laeq = _db(pe + re)
            la90 = _db(pe + gr * pp["quiet"])
            lamax = _db(pe + gr * pp["loud"])
            lamin = _db(pe + gr * pp["tiny"])
            series[pp["dep"]["id"]] = {
                "dep": pp["dep"], "stamps": pp["stamps"], "laeq": laeq, "la90": la90,
                "lamax": lamax, "lamin": lamin, "am": pp["am"], "vm": pp["vm"], "k": pp["k"],
                "plant_e": pe, "resid_e": re}
    return deps, series


def meter_dev(meter):
    m = [x for x in W.METERS if x["id"] == meter][0]
    return round((m["pre"] + m["post"]) / 2.0 - W.CAL_REF, 3)


def logged(series_one):
    """What the meter wrote: the true level plus the deployment's calibration deviation, to 0.1 dB."""
    dev = meter_dev(series_one["dep"]["meter"])
    out = {}
    for key in ("laeq", "la90", "lamax", "lamin"):
        out[key] = np.round(series_one[key] + dev, 1)
    return out
