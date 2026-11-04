"""The physical truth: each well's static water through the year, its pump's run schedule at quarter-hour
resolution, the operating point on its curve at the static level of the hour (flow, total head, efficiency, input
power), the water each quarter-hour delivered, the logger's instantaneous level at the top of each hour, the
barometer and the pump efficiency tests. Nothing here reads a pack file; golden.py never reads this."""
import datetime as dt
import math

import numpy as np

import world as W

QH = 4 * W.NH
DUTY_LOWER = {8: 0.86, 9: 0.78, 10: 0.42, 11: 0.16, 12: 0.03, 1: 0.03, 2: 0.08, 3: 0.32, 4: 0.58, 5: 0.76, 6: 0.86,
              7: 0.90, 8.5: 0.88, 9.5: 0.74, 10.5: 0.36}
DUTY_UPPER = {8: 0.80, 9: 0.72, 10: 0.40, 11: 0.15, 12: 0.03, 1: 0.03, 2: 0.10, 3: 0.30, 4: 0.52, 5: 0.70, 6: 0.80,
              7: 0.84, 8.5: 0.82, 9.5: 0.68, 10.5: 0.34}
RUN_MEAN = {"summer": 60.0, "shoulder": 36.0, "winter": 12.0}
TAU_ON = 0.12    # hours, the drawdown's approach to its pumping level after a start


def hour_time(h):
    return W.T0 + dt.timedelta(hours=int(h))


def month_key(t):
    if t.year == 2026 and t.month in (8, 9, 10):
        return t.month + 0.5
    return t.month


def season_of(m):
    return "summer" if m in (6, 7, 8, 8.5, 9, 9.5) else ("winter" if m in (11, 12, 1, 2) else "shoulder")


def static_level(p, h):
    """Depth to static water below ground, feet, at hour h: seasonal swing deepest about 24 August, chronic decline."""
    t = hour_time(h)
    doy = (t - dt.datetime(t.year, 1, 1, tzinfo=W.PST)).total_seconds() / 86400.0
    years = (t - dt.datetime(2025, 10, 1, tzinfo=W.PST)).total_seconds() / (365.25 * 86400)
    return p["base"] + p["amp"] * math.cos(2 * math.pi * (doy - 236.0) / 365.25) + p["trend"] * years


def operating_point(p, swl):
    """Solve the pump curve H0 - aQ^2 against the system head swl + Q/sc + discharge + column loss."""
    A, B, C = p["a"], 1.0 / p["sc"], swl + p["disch"] + p["col"] - p["h0"]
    q = (-B + math.sqrt(B * B - 4 * A * C)) / (2 * A)
    tdh = swl + q / p["sc"] + p["disch"] + p["col"]
    eta_p = p["eta_max"] * (1 - 0.9 * (q / p["q_bep"] - 1) ** 2)
    ope = eta_p * p["motor"]
    kw = q * tdh / (3960.0 * ope) * 0.7457
    return q, tdh, ope, kw


def schedule(p, rng):
    """Quarter-hour on/off from alternating runs and rests whose means follow the month's duty."""
    duty = DUTY_LOWER if p["aq"] == "Lower" else DUTY_UPPER
    on = np.zeros(QH, dtype=bool)
    q = int(rng.integers(0, 40))
    state = True
    while q < QH:
        mk = month_key(hour_time(q // 4))
        d = duty[mk]
        mean_on = RUN_MEAN[season_of(mk)]
        if state:
            length = max(1.0, rng.gamma(2.2, mean_on / 2.2))
        else:
            length = max(2.0, rng.gamma(1.8, mean_on * (1 - d) / d / 1.8))
        n = int(round(length * 4))
        if state:
            on[q:q + n] = True
        q += n
        state = not state
    return on


def force_rests(on, rng):
    """Every well's irrigation sets leave it a rest of at least 30 hours early in each static window, as the
    ranch schedules its spring and fall soundings."""
    for start in (dt.datetime(2026, 2, 2, 6, tzinfo=W.PST), dt.datetime(2026, 10, 3, 6, tzinfo=W.PST)):
        q0 = int((start - W.T0).total_seconds() // 900) + int(rng.integers(0, 4 * 24 * 6))
        run = int(rng.integers(4 * 6, 4 * 20))
        on[q0:q0 + run] = True
        on[q0 + run:q0 + run + int(rng.integers(4 * 30, 4 * 52))] = False
    return on


def simulate():
    rng = np.random.default_rng(W.SEED + 101)
    out = {}
    hours = np.arange(W.NH)
    qh = np.arange(QH) / 4.0
    baro = 33.62 + 0.46 * np.sin(2 * np.pi * qh / (24 * 4.1)) + 0.09 * np.sin(2 * np.pi * (qh - 15) / 12) \
        + np.cumsum(rng.normal(0, 0.006, QH)).clip(-0.4, 0.4)
    for w in W.WELLS:
        p = W.P[w]
        r = np.random.default_rng(W.SEED + 1000 + int(w[2:]))
        on = force_rests(schedule(p, r), r)
        swl = np.array([static_level(p, h) for h in hours]) + np.cumsum(r.normal(0, 0.02, W.NH)).clip(-0.6, 0.6)
        q_h, tdh_h, ope_h, kw_h = (np.zeros(W.NH) for _ in range(4))
        for h in hours:
            q_h[h], tdh_h[h], ope_h[h], kw_h[h] = operating_point(p, swl[h])
        onq = on.reshape(W.NH, 4)
        kwh_q = (kw_h[:, None] * 0.25 * (1 + r.normal(0, 0.004, (W.NH, 4)))) * onq
        af_q = (q_h[:, None] * 15.0 / W.AF_GAL) * onq
        # the logger's instant at each quarter-hour: drawdown toward the pumping level while running, the residual
        # drawdown recovering after a stop, both measured from the static level of the hour; a reading at the
        # instant a pump starts or stops still shows the state before the change
        lvl = np.zeros(QH)
        running, t_run, t_off, r_start, s_stop = False, 0.0, 999.0, 0.0, 0.0
        for h in hours:
            draw = q_h[h] / p["sc"]
            for k in range(4):
                if running:
                    lvl[4 * h + k] = swl[h] + r_start * math.exp(-t_run / p["tau_rec"]) + draw * (1 - math.exp(-t_run / TAU_ON))
                else:
                    lvl[4 * h + k] = swl[h] + s_stop * math.exp(-t_off / p["tau_rec"])
                now = bool(onq[h, k])
                if now and not running:
                    r_start = s_stop * math.exp(-t_off / p["tau_rec"])
                    running, t_run = True, 0.0
                elif not now and running:
                    s_stop = r_start * math.exp(-t_run / p["tau_rec"]) + draw * (1 - math.exp(-t_run / TAU_ON))
                    running, t_off = False, 0.0
                if running:
                    t_run += 0.25
                else:
                    t_off += 0.25
        lvl = lvl + r.normal(0, 0.02, QH)
        out[w] = dict(on=on, onq=onq, swl=swl, q=q_h, tdh=tdh_h, ope=ope_h, kw=kw_h, kwh_q=kwh_q, af_q=af_q, lvl=lvl)
    out["_baro"] = baro
    out["_tests"] = tests(out)
    return out


def tests(x):
    """The contractors' August and September 2025 round: each pump tested while it ran, at least two hours into a run."""
    rng = np.random.default_rng(W.SEED + 202)
    res = {}
    a0 = int((dt.datetime(2025, 8, 18, 7, tzinfo=W.PST) - W.T0).total_seconds() // 3600)
    a1 = int((dt.datetime(2025, 9, 19, 16, tzinfo=W.PST) - W.T0).total_seconds() // 3600)
    jobs_a, jobs_b = 817, 2291
    for i, w in enumerate(W.WELLS):
        p = W.P[w]
        d = x[w]
        cands = [h for h in range(a0, a1) if d["onq"][h - 3:h + 1].all() and 7 <= hour_time(h).hour <= 15]
        h = cands[int(rng.integers(0, len(cands)))]
        q, tdh, ope, kw = d["q"][h], d["tdh"][h], d["ope"][h], d["kw"][h]
        tester = W.TESTER_A if i % 2 == 0 else W.TESTER_B
        if tester == W.TESTER_A:
            jobs_a += int(rng.integers(3, 9)); job = "GPT-25-%04d" % jobs_a
        else:
            jobs_b += int(rng.integers(2, 7)); job = "BHS-%d" % jobs_b
        swl_m = round(float(d["swl"][h] + rng.normal(0, 0.25)), 1)
        pwl_m = round(float(d["swl"][h] + q / p["sc"] + rng.normal(0, 0.25)), 1)
        psi = round(float(p["disch"] / 2.31 + rng.normal(0, 0.3)), 1)
        col = round(float(p["col"]), 1)
        q_m = float(q * (1 + rng.normal(0, 0.008)))
        kw_m = round(float(kw * (1 + rng.normal(0, 0.006))), 1)
        res[w] = dict(h=h, t=hour_time(h), swl=swl_m, pwl=pwl_m, psi=psi, col=col, q=q_m, kw=kw_m,
                      tester=tester, job=job)
    return res
