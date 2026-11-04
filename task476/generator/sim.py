"""The truth: Tallis Creek's inflow every 10 minutes, the plant's turbine flow, release and spill, the true bypass flow,
the stage gauge BP-1 records, the hydrographer's measurements and the water temperature. golden.py never reads this;
checks.py reads it as the clean truth."""
import datetime as dt
import math

import numpy as np

import world as W


def setpoint(t):
    sp = W.SETPOINTS[0][1]
    for when, v, _ in W.SETPOINTS:
        if t >= when:
            sp = v
    return sp


def _event(t, peak_t, peak, rise_h, fall_h):
    x = (t - peak_t).total_seconds() / 3600.0
    if x < -rise_h * 3:
        return 0.0
    if x <= 0:
        return peak * math.exp(-((x / rise_h) ** 2))
    return peak * math.exp(-x / fall_h)


EVENTS = [(dt.datetime(2026, 5, 14, 3, 0, tzinfo=W.PST), 175.0, 5.0, 16.0),
          (dt.datetime(2026, 6, 2, 18, 0, tzinfo=W.PST), 75.0, 4.0, 14.0),
          (W.STORM_PEAK, 1360.0, 1.4, 4.5),
          (dt.datetime(2026, 10, 24, 9, 0, tzinfo=W.PST), 64.0, 6.0, 22.0)]


def simulate():
    rng = np.random.default_rng(W.SEED)
    rows = []
    t = W.REC_START
    ar = 0.0
    h_noise = 0.0
    while t < W.REC_END:
        doy = t.timetuple().tm_yday + t.hour / 24.0 + t.minute / 1440.0
        base = 82.0 + 45.0 * math.exp(-(doy - 121.0) / 45.0)
        fresh = 545.0 * math.exp(-(((doy - 147.0) / 16.5) ** 2))
        diurnal = 0.11 * fresh * math.sin(2 * math.pi * (t.hour + t.minute / 60.0 - 14.0) / 24.0)
        ar = 0.985 * ar + rng.normal(0, 0.0016)
        inflow = (base + fresh + diurnal) * (1 + ar) + sum(_event(t, *e) for e in EVENTS)
        sp = setpoint(t)
        tripped = W.UNIT_TRIP <= t < W.UNIT_BACK
        h_noise = 0.9 * h_noise + rng.normal(0, 0.0012)
        h_set = W.h_for(sp, W.q_rating7) + h_noise
        release = W.q_true(h_set, t)
        if tripped:
            turbine = 0.0
        else:
            turbine = min(W.TURBINE_MAX, max(0.0, inflow - release))
            if turbine < W.TURBINE_MIN:
                turbine = 0.0
        bypass = inflow - turbine
        if bypass > release + 1e-9:
            h = W.h_for(bypass, W.q_true, t)
        else:
            h = h_set
            bypass = release
        rows.append(dict(t=t, inflow=inflow, turbine=turbine, bypass=bypass, h=h, sp=sp, tripped=tripped,
                         spill=(bypass > release + 0.5) and not tripped and turbine > 0))
        t += dt.timedelta(minutes=W.STEP_MIN)
    visits = []
    for arr, setup, dur, staff_d, err in W.VISITS:
        start = arr + dt.timedelta(minutes=setup)
        end = start + dt.timedelta(minutes=dur)
        s_pst, e_pst, a_pst = start.astimezone(W.PST), end.astimezone(W.PST), arr.astimezone(W.PST)
        win = [r for r in rows if s_pst <= r["t"] <= e_pst]       # the logger's readings while the measurement ran
        gh = sum(r["h"] for r in win) / len(win)
        q = sum(r["bypass"] for r in win) / len(win)
        a = min(rows, key=lambda r: abs((r["t"] - a_pst).total_seconds()))
        visits.append(dict(t=arr, start=start, end=end, h=a["h"], gh=gh, q_true=q, q_meas=q * (1 + err), err=err,
                           staff=round(round(a["h"], 2) + staff_d, 2)))
    # water temperature (UTC logger), daily generation and powerhouse rain, the files the solution never reads
    temp = []
    for r in rows[::3]:
        doy = r["t"].timetuple().tm_yday
        hr = r["t"].astimezone(W.PDT).hour + r["t"].minute / 60.0
        c = 6.5 + 8.5 * math.sin(math.pi * (doy - 110) / 150.0) ** 1.4 if 110 <= doy <= 260 else 6.5 + 2.0 * math.cos(
            math.pi * (doy - 260) / 120.0)
        amp = 1.6 if r["bypass"] < 120 else 0.7
        temp.append((r["t"], c + amp * math.sin(2 * math.pi * (hr - 10.0) / 24.0) + float(rng.normal(0, 0.08))))
    gen = {}
    for r in rows:
        d = r["t"].astimezone(W.PDT).date()
        g = gen.setdefault(d, [0.0, 0.0])
        g[0] += r["turbine"] * 182.0 * 0.0846 * 0.86 / 1000.0 / 6.0
        g[1] += (1 / 6.0) if r["turbine"] > 0 else 0.0
    rain = {}
    for r in rows:
        d = r["t"].astimezone(W.PDT).date()
        storm = sum(_event(r["t"], *e) for e in EVENTS)
        rain[d] = rain.get(d, 0.0) + storm / 4200.0
    return dict(rows=rows, visits=visits, temp=temp, gen=gen, rain=rain)


def daily_truth(x):
    """True and Rating 7 daily means on local (PDT) calendar days."""
    out = {}
    for r in x["rows"]:
        d = r["t"].astimezone(W.PDT).date()
        if not (W.SEASON[0] <= d <= W.SEASON[1]):
            continue
        a = out.setdefault(d, [0.0, 0.0, 0])
        a[0] += r["bypass"]
        a[1] += W.q_rating7(round(r["h"], 3))
        a[2] += 1
    return {d: dict(true=v[0] / v[2], rated=v[1] / v[2], n=v[2]) for d, v in out.items()}
