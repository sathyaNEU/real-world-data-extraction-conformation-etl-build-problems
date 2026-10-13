"""task229 generator: the 2027 grades. Each station-month of 2027 on the outlook's monthly flow, shaped inside the
day by the operating plan where a plant peaks, published as the current rating read at the day's mean water level.

grade(...) is the literal reading the golden files; variants(...) runs every admissible reading of the release
shape, the local inflow, the damping, the lag, the clock and the day-to-day spread (the corridor, SF6 to SF10)."""
from datetime import date, datetime
from zoneinfo import ZoneInfo

import numpy as np

import params as P
import world as W

STEP = 1.0                                  # minutes
SPD = int(24 * 60 / STEP)
HOURS = (np.arange(SPD) + 0.5) * STEP / 60.0
CLOCK = ZoneInfo(P.TZ)


def dst_on(d):
    return datetime(d.year, d.month, d.day, 12, tzinfo=CLOCK).dst().total_seconds() / 3600.0


def window_weight(dst, ramp_h):
    w = np.zeros(SPD)
    for a, z in P.WINDOWS:
        a0, z0 = a - dst, z - dst
        if ramp_h > 0:
            up = np.clip((HOURS - a0) / ramp_h, 0, 1)
            dn = np.clip((z0 - HOURS) / ramp_h, 0, 1)
            w += np.minimum(up, dn) * ((HOURS > a0) & (HOURS < z0))
        else:
            w += ((HOURS >= a0) & (HOURS < z0)).astype(float)
    return w


def plant_mode(no, m):
    """'peaking', 'continuous' or 'none' for a regulated station's plant in month m of 2027"""
    p = W.PLANT_OF.get(no)
    if p is None:
        return "none"
    if p == "merrin" and date(P.YEAR, m, 1) < W.MERRIN["in_service"]:
        return "none"
    return "continuous" if m in W.CONTINUOUS_MONTHS else "peaking"


def day_flow(no, m, inflow_scale=1.0, local_scale=1.0, ramp_h=P.RAMP_H, damp=0.0, lag_min=0, dst=0.0, shape="plan",
             force_mode=None, cap_off=False):
    """one day's flow past the station at a given inflow; returns (flow array, true daily mean)"""
    Q = W.outlook_2027(no, m)
    mode = force_mode or plant_mode(no, m)
    if mode != "peaking":
        q = np.full(SPD, Q * inflow_scale)
        return q, q.mean()
    p = W.PLANT_OF[no]
    plant = W.TALBOT if p == "talbot" else W.MERRIN
    I = W.node_2027(p, m) * inflow_scale
    L = (Q - W.node_2027(p, m)) * local_scale * inflow_scale
    fmin = plant["fmin"]
    if shape == "plan":
        w = window_weight(dst, ramp_h)
        weff = w.mean() * 24.0
        F = fmin + 24.0 * (I - fmin) / weff
        if F > plant["cap"] and not cap_off:
            q = np.full(SPD, I + L)          # the plan: a day the windows cannot pass at capacity runs continuously
            return q, q.mean()
        rel = fmin + (F - fmin) * w
    elif shape == "sine":                       # not the plan: an even swing about the inflow
        rel = I + (I - fmin) * np.sin(2 * np.pi * (HOURS - 9) / 24)
    else:
        raise ValueError(shape)
    if lag_min:
        k = int(lag_min / STEP)
        rel = np.r_[rel[-k:], rel[:-k]]
    if damp:
        rel = rel.mean() + (1 - damp) * (rel - rel.mean())
    q = rel + L
    return q, q.mean()


def peak_rate(no, m, ramp_h=P.RAMP_H):
    """the generating rate on a peaking day at the month's outlook inflow (the literal reading)"""
    p = W.PLANT_OF[no]
    plant = W.TALBOT if p == "talbot" else W.MERRIN
    w = window_weight(0.0, ramp_h)
    return plant["fmin"] + 24.0 * (W.node_2027(p, m) - plant["fmin"]) / (w.mean() * 24.0), plant["cap"]


def published_over_true(no, m, **kw):
    q, qbar = day_flow(no, m, **kw)
    par = W.RATING[no]
    h = W.h_of_q(par, q)
    return float(W.q_of_h(par, h.mean()) / qbar)


def largest_gauged(gr, no):
    return gr[no]


def grade(no, m, gauged_top, **kw):
    """(error as a fraction, short of grade B?) for one station-month, the literal reading"""
    r = published_over_true(no, m, **kw) - 1.0
    extrap = W.outlook_2027(no, m) > P.EXTRAP * gauged_top[no]
    return r, (abs(r) > P.GRADE_B) or extrap, extrap


def schedule(gauged_top, **kw):
    """station -> (first month short or None, set of months short, {m: error})"""
    out = {}
    for no in W.CURRENT:
        errs, short = {}, set()
        for m in range(1, 13):
            r, s, _ = grade(no, m, gauged_top, **kw)
            errs[m] = r
            if s:
                short.add(m)
        out[no] = (min(short) if short else None, short, errs)
    return out


def month_with_days(no, m, gauged_top=None, spread=0.0, seed=0, dst_actual=True, **kw):
    """the month's grade with each day at its own inflow (a spread about the month's flow) and the clock's DST"""
    r = np.random.default_rng([P.SEED, 77, int(no[1:]), m, seed])
    nd = (date(P.YEAR + (m == 12), m % 12 + 1, 1) - date(P.YEAR, m, 1)).days
    pubs, trues = [], []
    sc = np.exp(r.normal(0, spread, nd)) if spread else np.ones(nd)
    sc = sc / sc.mean()
    par = W.RATING[no]
    for i in range(nd):
        d = date(P.YEAR, m, i + 1)
        q, qbar = day_flow(no, m, inflow_scale=sc[i], dst=dst_on(d) if dst_actual else 0.0, **kw)
        pubs.append(float(W.q_of_h(par, W.h_of_q(par, q).mean())))
        trues.append(qbar)
    return float(np.mean(pubs) / np.mean(trues) - 1.0)


if __name__ == "__main__":
    top = {no: 1e9 for no in W.CURRENT}
    sch = schedule(top)
    for no in W.CURRENT:
        f, s, e = sch[no]
        if s or no in W.PLANT_OF:
            print(no, f, sorted(s), " ".join("%6.1f" % (100 * e[m]) for m in range(1, 13)))
    worst = {}
    for no in W.PLANT_OF:
        for m in range(1, 13):
            if plant_mode(no, m) != "peaking":
                continue
            vals = []
            for damp in (0, 0.25):
                for ls in (0.8, 1.2):
                    for ramp in (0.0, 0.5, 1.0):
                        for lag in (0, 25):
                            vals.append(published_over_true(no, m, damp=damp, local_scale=ls, ramp_h=ramp, lag_min=lag) - 1)
            worst[(no, m)] = max(vals)
    print("corridor least-biased failing:", min(worst.items(), key=lambda kv: -kv[1]))
    for no in ["C105", "C104"]:
        for d in (0.30, 0.35, 0.40):
            print(no, "Jan damp", d, round(100 * (published_over_true(no, 1, damp=d, local_scale=1.2, ramp_h=1.0) - 1), 2))
