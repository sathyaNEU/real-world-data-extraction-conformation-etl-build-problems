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
            + 1.15 * np.sin(2 * math.pi * (hours - 3.4) / 24.0)
            + 0.55 * np.sin(2 * math.pi * hours / 61.0 - 1.1)
            + rng.normal(0, 0.45, n10))
    wind = np.clip(wind, 0.2, 12.0)
    # rain: wet spells, a few per survey
    rain = np.zeros(n10)
    for c in rng.choice(n10 - 60, size=11, replace=False):
        dur = int(rng.integers(3, 16))
        rain[c:c + dur] += np.abs(rng.normal(0.20, 0.13, dur))
    # wind direction: a synoptic bearing that sits for a day or two, with the gust-to-gust scatter on it
    synoptic = (212.0 + 86.0 * np.sin(2 * math.pi * hours / 71.0 + 1.3)
                + 54.0 * np.sin(2 * math.pi * hours / 173.0 - 0.4))
    wdir = (synoptic + rng.normal(0, 11.0, n10)) % 360.0
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
            "wind_dir": np.round(wdir).astype(int) % 360,
            "temp_c": np.round(temp, 1)}


MET = met_series()


def met_index(stamps_local):
    """Index into the ten-minute met record for local-time minute stamps. The mast's file is stamped UTC,
    so the local stamp is taken back to UTC first, exactly as a reader of the two files has to."""
    secs = np.array([(s - dt.timedelta(hours=LOCAL_OFFSET) - MET["t0"]).total_seconds()
                     for s in stamps_local])
    return np.clip((secs // 600).astype(int), 0, MET["n"] - 1)


def rain_counted():
    """Whether the gauge counted rain in each ten-minute record, from the tip counts the mast file carries
    (plan 4.2). The counter resets at midnight, so the day's first record counts its own tips."""
    return MET["rain_mm_shipped"] > 0.0


RAIN_ON = rain_counted()


PLANT_T0 = dt.datetime(2026, 8, 24)
_PJ_N = 60 * 24 * 60


def _plant_jitter():
    """Minute-to-minute swing of the source itself, one series for the whole survey: the blowers' load
    valves and the engine's governor never hold a level to the tenth of a decibel."""
    rng = np.random.default_rng(W.SEED + 97)
    a, sd = 0.70, 0.38
    out = np.zeros(_PJ_N)
    wn = rng.normal(0.0, sd * math.sqrt(1 - a * a), _PJ_N)
    for i in range(_PJ_N):
        out[i] = a * out[i - 1] + wn[i] if i else wn[i]
    return _e(out)


PLANT_JIT = _plant_jitter()


def week_factor(day):
    """The site's weekly milk intake, which moves the plant's load from week to week. The process log and
    the sound both run off it."""
    w = (day - dt.date(2026, 8, 3)).days // 7
    return 1.0 + 0.021 * math.sin(2.1 * w) - 0.014 * math.cos(3.3 * w)


def plant_load(stamps_local):
    """Energy factor of the plant's own sound while it runs: the digester's feed pattern over the day, the
    week's intake, and the source's own minute-to-minute swing."""
    h = np.array([s.hour + s.minute / 60.0 for s in stamps_local])
    wf = np.array([week_factor(s.date()) for s in stamps_local])
    dow = np.array([s.weekday() for s in stamps_local])
    load = (1.0 + 0.088 * np.sin(2 * math.pi * (h - 4.2) / 24.0)
            + 0.034 * np.sin(2 * math.pi * h / 8.0 + 0.6)
            - 0.022 * (dow >= 5)) * wf
    idx = np.array([int((s - PLANT_T0).total_seconds() // 60) for s in stamps_local])
    return load * PLANT_JIT[np.clip(idx, 0, _PJ_N - 1)]


def centrifuge_runs(day):
    """Every dewatering run on a date, one entry a centrifuge a spell: unit, start, end, local time. The
    shift runs both machines on weekdays and one on a Saturday, splits a run where the liquor tank has to
    be drawn down mid-shift, and leaves a machine down on the day its scroll is checked. One definition,
    used by the simulation, by the equipment log and by the process channels."""
    if day.weekday() > 5:
        return []
    o = day.toordinal()
    stops = [s for s, m, _ in W.PLANNED_STOPS if s.date() == day]
    if stops:
        mins = [m for s, m, _ in W.PLANNED_STOPS if s.date() == day][0]
        begin = stops[0] + dt.timedelta(minutes=mins + 5 + 2 * (o % 5))
    elif o % 9 in (2, 6):
        begin = dt.datetime(day.year, day.month, day.day, 8, 25 + 4 * (o % 6))   # a late start
    else:
        begin = dt.datetime(day.year, day.month, day.day, 6, 2 + 2 * (o % 7))
    if o % 7 in (1, 4):
        finish = dt.datetime(day.year, day.month, day.day, 13, 20 + 5 * (o % 8))  # feed tank run down
    else:
        finish = dt.datetime(day.year, day.month, day.day, 17, 40 + 3 * (o % 4))
    if day.weekday() == 5:                      # Saturday: one machine, the shift alternates them
        units = [W.CENTRIFUGES[(o // 7) % 2]]
        finish = finish - dt.timedelta(hours=3, minutes=25)
    else:
        units = list(W.CENTRIFUGES)
    if day in W.CF_DOWN:
        units = [u for u in units if u not in W.CF_DOWN[day]]
    out = []
    for i, u in enumerate(units):
        a = begin + dt.timedelta(minutes=4 * i)
        b = finish - dt.timedelta(minutes=7 * i)
        if (u, day) in W.CF_SPLIT:
            mid = a + dt.timedelta(minutes=W.CF_SPLIT[(u, day)])
            out.append((u, a, mid))
            out.append((u, mid + dt.timedelta(minutes=48 + 3 * (o % 5)), b))
        else:
            out.append((u, a, b))
    return out


def centrifuge_span(day):
    """The span the dewatering shift covered on a date, or None: start of the first run to end of the
    last, used where only the plant's own sound matters."""
    rs = centrifuge_runs(day)
    if not rs:
        return None
    return min(r[1] for r in rs), max(r[2] for r in rs)


def all_down():
    """Every interval in which the blowers, the centrifuges and the engine are all down."""
    return [(s, s + dt.timedelta(minutes=m)) for s, m, _ in W.PLANNED_STOPS + W.UNPLANNED_STOPS]


def plant_state(stamps_local):
    """Energy factor of the plant's own sound: 0 in a stop, 1 running, more while a centrifuge runs."""
    cf = np.zeros(len(stamps_local), dtype=bool)
    days = sorted({s.date() for s in stamps_local})
    runs = {d: centrifuge_runs(d) for d in days}
    for i, s in enumerate(stamps_local):
        for _, a, b in runs[s.date()]:
            if a <= s < b:
                cf[i] = True
                break
    k = plant_load(stamps_local) * np.where(cf, 1.22, 1.0)
    for start, end in all_down():
        inside = np.array([(s >= start) and (s < end) for s in stamps_local])
        k = np.where(inside, 0.0, k)
    return k


def residual_shape(code, stamps_local, seed):
    """Unit-scale residual energy per minute: a steady part that drifts slowly, plus passby events."""
    p = W.BY_CODE[code]
    ev, strm = p[9], p[10]
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
    shape = (0.64 + 0.30 * np.exp(-((hours - 8.3) ** 2) / 2.2)
             + 0.34 * np.exp(-((hours - 17.6) ** 2) / 3.0)
             + 0.18 * np.exp(-((hours - 12.5) ** 2) / 8.0)
             + 0.33 * np.exp(-((hours - 6.1) ** 2) / 1.6))
    shape = np.where(dows <= 4, shape, shape * 0.82)
    lam = ev * shape / 60.0
    hit = rng.random(n) < lam
    amp = np.where(hit, _e(rng.uniform(W.EVENT_DB[code][0], W.EVENT_DB[code][1], n)), 0.0)
    extra = amp * steady
    # a second minute of decay on the louder events
    extra = extra + np.concatenate([[0.0], extra[:-1] * 0.35])
    total = strm * steady.mean() + (1.0 - strm) * steady + extra
    # within-minute statistics of the surroundings: the level the minute fell to, its loudest second and
    # its quietest. A minute of a rural background is never flat: the wind in the hedge alone moves it.
    quiet = (strm * steady.mean() * _e(-rng.uniform(0.15, 0.9, n))
             + (1.0 - strm) * steady * _e(-rng.uniform(0.8, 3.2, n)))
    loud = (total + extra * 2.1 + (1.0 - strm) * steady * _e(rng.uniform(1.0, 7.0, n))
            + 0.42 * steady * _e(rng.uniform(0.5, 6.5, n)))
    tiny = quiet * _e(-rng.uniform(0.8, 3.0, n))
    return total, quiet, loud, tiny


def assessment_mask(stamps_local):
    hours = np.array([s.hour + s.minute / 60.0 for s in stamps_local])
    dows = np.array([s.weekday() for s in stamps_local])
    return (dows <= 4) & (hours >= W.DAY_START) & (hours < W.DAY_END)


def validity_mask(stamps_local):
    """Plan 4.2: a minute is invalid where the met record for its ten minutes counted rain or shows wind
    above 5 m a second."""
    idx = met_index(stamps_local)
    return (~RAIN_ON[idx]) & (MET["wind_eff"][idx] <= 5.0)


def nodata_mask(dep, stamps_local):
    """Minutes the meter wrote no measurement for (plan 4.2's last sentence)."""
    out = np.zeros(len(stamps_local), dtype=bool)
    for start, mins, _ in dep.get("nodata", []):
        end = start + dt.timedelta(minutes=mins)
        out |= np.array([(x >= start) and (x < end) for x in stamps_local])
    return out


def deployments():
    """Every deployment: position, meter, week, local start and end, mounting."""
    out = []
    for code in W.CODES:
        for k, (wk, meter) in enumerate(W.SCHEDULE[code]):
            start = W.WEEKS[wk]
            out.append({"code": code, "meter": meter, "week": wk, "start": start,
                        "end": start + dt.timedelta(days=6),
                        "mount": W.HEIGHT_DEPART.get((code, k), W.HEIGHT[code]), "k": k})
    out.sort(key=lambda d: (d["start"], d["meter"]))
    seen = {}
    for i, d in enumerate(out, start=1):
        d["id"] = "D%02d" % i
        j = seen.get(d["meter"], 0)
        seen[d["meter"]] = j + 1
        mean = W.CAL_MEAN[d["meter"]][j]
        spread = W.CAL_SPREAD[d["meter"]][j]
        d["cal_before"] = round(mean - spread / 2.0, 1)
        d["cal_after"] = round(mean + spread / 2.0, 1)
        d["cal_mean"] = round((d["cal_before"] + d["cal_after"]) / 2.0, 1)
        d["dev"] = round(d["cal_mean"] - W.CAL_REF, 1)
        d["correction"] = d["dev"] if abs(d["dev"]) > W.CAL_THRESHOLD else 0.0
        d["crew"] = W.CREW[i - 1]
        d["nodata"] = [(a, b, c) for (sel, a, b, c) in W.NODATA if sel == (d["code"], d["k"])]
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
            nd = nodata_mask(d, stamps)
            vm = validity_mask(stamps) & ~nd
            parts.append({"dep": d, "stamps": stamps, "k": k, "res": res, "quiet": quiet,
                          "loud": loud, "tiny": tiny, "am": am, "vm": vm, "nd": nd})
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
            # the plant is steady over a minute but not flat: the blowers' blade passage and the engine's
            # governor move it a little inside the minute too
            wrng = np.random.default_rng(W.SEED + 4409 + 17 * W.CODES.index(code) + pp["dep"]["week"])
            m = len(pe)
            f90 = _e(-wrng.uniform(0.08, 0.55, m))
            fmax = _e(wrng.uniform(0.5, 2.4, m))
            fmin = f90 * _e(-wrng.uniform(0.3, 1.2, m))
            laeq = _db(pe + re)
            la90 = _db(pe * f90 + gr * pp["quiet"])
            lamax = _db(pe * fmax + gr * pp["loud"])
            lamin = _db(pe * fmin + gr * pp["tiny"])
            series[pp["dep"]["id"]] = {
                "dep": pp["dep"], "stamps": pp["stamps"], "laeq": laeq, "la90": la90,
                "lamax": lamax, "lamin": lamin, "am": pp["am"], "vm": pp["vm"], "nd": pp["nd"],
                "k": pp["k"], "plant_e": pe, "resid_e": re}
    return deps, series


def dep_dev(dep):
    """The deployment's deviation from the calibrator, the mean of its two field checks less 94.0 dB."""
    return dep["dev"]


def dep_correction(dep):
    """What plan 4.1 takes off that deployment's levels: nothing inside the 0.3 dB window."""
    return dep["correction"]


def logged(series_one):
    """What the meter wrote: the true level plus the deployment's calibration deviation, to 0.1 dB, with
    the instrument's no-data value in every level column for the minutes it recorded nothing."""
    dev = dep_dev(series_one["dep"])
    nd = series_one["nd"]
    out = {}
    for key in ("laeq", "la90", "lamax", "lamin"):
        out[key] = np.where(nd, W.NODATA_VALUE, np.round(series_one[key] + dev, 1))
    return out
