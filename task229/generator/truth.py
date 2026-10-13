"""task229 generator: the truth. Daily natural flows, the within-day flow and water level at every station
(the regulated reaches shaped by Talbot Canyon's release schedule), the daily means each platform reports,
and the gaugings at the instants they were made. Nothing here is shipped; build.py writes the record from it."""
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

import numpy as np

import params as P
import world as W

T0 = date(2015, 10, 1)                  # truth starts a year before the first gauging kept
T1 = P.RECORD_END
NDAY = (T1 - T0).days + 1
SPD = 24 * 60 // P.STEP_MIN             # steps per local standard day
CLOCK = ZoneInfo(P.TZ)


def rng(*k):
    return np.random.default_rng([P.SEED, *k])


def day_list():
    return [T0 + timedelta(days=i) for i in range(NDAY)]


DAYS = day_list()
MONTH = np.array([d.month for d in DAYS])


def dst_hours():
    """clock minus standard offset (0 or 1 hour) at local standard noon of every day"""
    out = np.zeros(NDAY)
    for i, d in enumerate(DAYS):
        dt = datetime(d.year, d.month, d.day, 12, tzinfo=CLOCK)
        out[i] = dt.dst().total_seconds() / 3600.0
    return out


DST = dst_hours()


def smooth_clim(series12, doy_month_frac):
    """monthly means to a smooth daily curve (periodic cubic through mid-month points), then rescaled so each
    calendar month's mean of the curve matches its monthly value"""
    return series12


def daily_natural(key, monthly, sd, phi, storm=0.0, seedk=0):
    """daily mean natural flow: monthly climatology x a water-year factor x AR(1) in logs x storm pulses;
    each calendar month of the history keeps its climatological mean on average"""
    r = rng(11, seedk)
    mid = np.array([15.2 + 30.4 * k for k in range(12)])
    doy = np.array([(d - date(d.year, 1, 1)).days for d in DAYS], float)
    lm = np.log(np.asarray(monthly, float))
    xs = np.r_[mid - 365, mid, mid + 365]
    ys = np.r_[lm, lm, lm]
    base = np.interp(doy, xs, ys)
    # water-year factors
    wy = np.array([d.year + (1 if d.month >= 10 else 0) for d in DAYS])
    fac = {y: r.normal(0, 0.12) for y in range(2016, 2027)}
    wyf = np.array([fac[y] for y in wy])
    x = np.zeros(NDAY)
    e = r.normal(0, sd * np.sqrt(1 - phi ** 2), NDAY)
    for i in range(1, NDAY):
        x[i] = phi * x[i - 1] + e[i]
    lq = base + wyf + x
    if storm:
        s = np.zeros(NDAY)
        hits = r.random(NDAY) < storm * np.where(np.isin(MONTH, [10, 11, 12, 1, 2, 3]), 1.0, 0.35)
        for i in np.nonzero(hits)[0]:
            amp = r.gamma(2.0, 0.35)
            k = np.arange(0, min(12, NDAY - i))
            s[i + k] += amp * np.exp(-k / 2.2)
        lq = lq + np.log1p(s)
    q = np.exp(lq)
    # rescale each calendar month (over all years) to its monthly value
    for m in range(1, 13):
        sel = MONTH == m
        q[sel] *= monthly[m - 1] / q[sel].mean()
    return q


REGIME_NOISE = {  # sd of log AR(1), phi, storm rate per day
    "snow": (0.22, 0.93, 0.010), "flashy": (0.30, 0.88, 0.016), "glacier": (0.20, 0.94, 0.006),
    "rain": (0.30, 0.85, 0.045), "rainsnow": (0.27, 0.88, 0.030), "spring": (0.015, 0.995, 0.0),
    "lake": (0.10, 0.985, 0.0),
}


def natural_flows():
    """daily mean natural flow by station, plus the two forebay nodes and the regulated stations' local inflow"""
    Q = {}
    for k, no in enumerate(sorted(W.ST)):
        rg = W.ST[no]["regime"]
        if rg in ("talbot", "merrin"):
            continue
        sd, phi, storm = REGIME_NOISE[rg]
        monthly = [W.clim_hist(no, m) for m in range(1, 13)]
        Q[no] = daily_natural(no, monthly, sd, phi, storm, seedk=k)
    # C110 and C122 are one creek 300 m apart: one flow series
    Q["C122"] = Q["C110"] * (W.ST["C122"]["area"] / W.ST["C110"]["area"])
    Q["talbot_node"] = daily_natural("talbot", W.TALBOT_HIST, 0.21, 0.93, 0.012, seedk=101)
    Q["merrin_node"] = daily_natural("merrin", W.MERRIN_HIST, 0.22, 0.93, 0.010, seedk=102)
    Q["vardy"] = daily_natural("vardy", [W.vardy(m) for m in range(1, 13)], 0.20, 0.93, 0.020, seedk=103)
    for no in W.PLANT_OF:
        node = Q[W.PLANT_OF[no] + "_node"]
        r = rng(12, int(no[1:]))
        wob = np.exp(r.normal(0, 0.06, NDAY))
        Q[no + "_local"] = node * W.local_share(no) * wob + (Q["vardy"] if no == "C124" else 0.0)
    return Q


def lake_smooth(q):
    """Lake Ashlin's outflow: the lake's storage smooths the inflow (linear reservoir, k = 6 days)"""
    out = np.empty_like(q)
    out[0] = q[0]
    a = 1.0 / 6.0
    for i in range(1, len(q)):
        out[i] = out[i - 1] + a * (q[i] - out[i - 1])
    return out


def within_day_natural(qd, regime, seedk):
    """5-minute flow from daily means: a linear trend between day centres and a diurnal melt cycle"""
    r = rng(13, seedk)
    n = len(qd)
    t = (np.arange(n * SPD) + 0.5) / SPD                     # days since T0 at step centres
    centres = np.arange(n) + 0.5
    base = np.interp(t, centres, qd)
    amp_m = {"snow": [0, 0, .01, .04, .09, .10, .06, .03, .01, 0, 0, 0],
             "flashy": [0, 0, .01, .05, .11, .12, .06, .02, .01, 0, 0, 0],
             "glacier": [0, 0, 0, .02, .06, .10, .13, .12, .06, .01, 0, 0],
             "rain": [0] * 12, "rainsnow": [0, 0, 0, .02, .04, .03, .01, 0, 0, 0, 0, 0],
             "spring": [0] * 12, "lake": [0] * 12}[regime]
    amp = np.repeat(np.array([amp_m[m - 1] for m in MONTH]) * np.exp(r.normal(0, 0.25, n)), SPD)
    hour = (np.arange(n * SPD) % SPD) * P.STEP_MIN / 60.0
    diurnal = 1 + amp * np.sin(2 * np.pi * (hour - 11.0) / 24.0)
    q = base * diurnal
    # keep each day's mean flow equal to its daily value
    q = q.reshape(n, SPD)
    q *= (qd / q.mean(axis=1))[:, None]
    return q.ravel()


def release_day(I, fmin, cap, peaking, dst):
    """one local-standard day of a plant's release (5-minute steps): on a peaking day the minimum release outside
    the windows and the rest of the day's inflow inside them, with 30-minute ramps; otherwise the inflow"""
    hours = (np.arange(SPD) + 0.5) * P.STEP_MIN / 60.0
    if not peaking or I <= fmin:
        return np.full(SPD, I), False
    w = np.zeros(SPD)
    for a, z in P.WINDOWS:
        a0, z0 = a - dst, z - dst                       # clock windows in standard time
        up = np.clip((hours - a0) / P.RAMP_H, 0, 1)
        dn = np.clip((z0 - hours) / P.RAMP_H, 0, 1)
        w += np.minimum(up, dn) * ((hours > a0) & (hours < z0))
    weff = w.mean() * 24.0
    F = fmin + 24.0 * (I - fmin) / weff
    if F > cap:
        return np.full(SPD, I), False
    return fmin + (F - fmin) * w, True


def regulated_series(Q, no, peaking_month, lag_min, damp):
    """5-minute flow at a regulated gauge: the release (lagged and lightly damped) plus the local inflow"""
    p = W.PLANT_OF[no]
    plant = W.TALBOT if p == "talbot" else W.MERRIN
    node = Q[p + "_node"]
    rel = np.empty(NDAY * SPD)
    peak_days = np.zeros(NDAY, bool)
    for i in range(NDAY):
        pk = peaking_month(DAYS[i])
        rel[i * SPD:(i + 1) * SPD], peak_days[i] = release_day(node[i], plant["fmin"], plant["cap"], pk, DST[i])
    k = max(1, lag_min // P.STEP_MIN)
    rel = np.r_[rel[:k], rel[:-k]]
    if damp:
        n = 7
        sm = np.convolve(np.r_[rel[:n], rel, rel[-n:]], np.ones(2 * n + 1) / (2 * n + 1), "same")[n:-n]
        rel = (1 - damp) * rel + damp * sm
    local = within_day_natural(Q[no + "_local"], "snow", 200 + int(no[1:]))
    return rel + local, peak_days


def talbot_peaking(d):
    return d.year >= W.TALBOT["since"] and d.month not in W.CONTINUOUS_MONTHS


def never(d):
    return False


LAG = {"C104": (5, 0.03), "C105": (20, 0.08), "C112": (5, 0.03), "C113": (25, 0.09), "C124": (55, 0.16)}


def flow_series(Q):
    """station -> 5-minute true flow over T0..T1 (generator), with Talbot's peaking days marked"""
    S, PK = {}, {}
    for k, no in enumerate(sorted(W.ST)):
        rg = W.ST[no]["regime"]
        if rg == "talbot":
            S[no], PK[no] = regulated_series(Q, no, talbot_peaking, *LAG[no])
        elif rg == "merrin":
            S[no], PK[no] = regulated_series(Q, no, never, *LAG[no])
        elif rg == "lake":
            S[no] = within_day_natural(lake_smooth(Q[no]), "lake", 300 + k)
        else:
            S[no] = within_day_natural(Q[no], rg, 300 + k)
    return S, PK


def level_series(S):
    """5-minute true water level through each site's true stage-discharge relation (the current rating)"""
    return {no: W.h_of_q(W.RATING[no], S[no]) for no in S}


def daily_means(H):
    """per station: the mean water level over each local standard day and over each UTC day (the UTC day d runs
    from 16:00 local standard time on d-1 to 16:00 on d)"""
    out = {}
    shift = (-P.LST_OFFSET_H) * 60 // P.STEP_MIN        # 8 hours in steps
    for no, h in H.items():
        loc = h.reshape(NDAY, SPD).mean(axis=1)
        utc = np.full(NDAY, np.nan)
        hh = np.r_[np.full(shift, np.nan), h[:-shift]]   # utc day d = local [d-1 16:00, d 16:00)
        utc_days = hh.reshape(NDAY, SPD)
        utc = utc_days.mean(axis=1)
        utc[0] = np.nan
        out[no] = {"local": loc, "utc": utc}
    return out


def build_truth():
    Q = natural_flows()
    S, PK = flow_series(Q)
    H = level_series(S)
    D = daily_means(H)
    return {"Q": Q, "S": S, "H": H, "D": D, "PK": PK}


if __name__ == "__main__":
    import time
    t = time.time()
    T = build_truth()
    print("truth built in %.1fs" % (time.time() - t))
    for no in ["C104", "C105", "C107", "C111", "C102"]:
        s = T["S"][no].reshape(NDAY, SPD)
        h = T["H"][no].reshape(NDAY, SPD)
        i = DAYS.index(date(2026, 1, 14))
        q_true = s[i].mean()
        q_pub = W.q_of_h(W.RATING[no], h[i].mean())
        print(no, "2026-01-14 true %.3f published %.3f bias %.1f%% min %.2f max %.2f" % (q_true, q_pub, 100 * (q_pub / q_true - 1), s[i].min(), s[i].max()))
