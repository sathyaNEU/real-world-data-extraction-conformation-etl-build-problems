"""The world behind the pack: the confined Sherwood Sandstone at Brackenholt, closed to the east by the Coldharbour
Fault, Borehole 2's 2014 constant-rate test, its abstraction since 1 April 2015, the plant's operations from April
2025 (bottling lines, sub-meters, the plant inlet meter, the wellhead pump, the bulk tanker bay) and the water levels
the observation boreholes and the regional borehole beyond the fault recorded.

Physics: drawdown in a confined aquifer is Theis's solution, and the fault, which throws the sandstone against
mudstone, is a no-flow boundary, so every point on BH2's side also carries the drawdown of an image well pumping at
BH2's rate at BH2's mirror position across the trace. Points beyond the fault (the regional borehole) are in another
block and do not respond. Nothing in the pack states any of this; the records only behave so."""
from __future__ import annotations

import datetime as dt
import math

import numpy as np
from scipy.special import exp1

import common as K

DAY = dt.timedelta(days=1)


# ------------------------------------------------------------------------------------------------- physics
def unit_resp(xy, t_days, T=K.T_M2D, S=K.S_CONF, image=True, coef=1.0):
    """Drawdown (m) per cubic metre a day of steady pumping started t_days before, at local point xy."""
    t = np.atleast_1d(np.asarray(t_days, float))
    out = np.zeros_like(t)
    m = t > 0
    x, y = xy
    r2 = max(x * x + y * y, 0.15 ** 2)
    out[m] = exp1(r2 * S / (4.0 * T * t[m])) / (4.0 * math.pi * T)
    if image:
        ix, iy = K.image_xy()
        ri2 = (x - ix) ** 2 + (y - iy) ** 2
        out[m] += coef * exp1(ri2 * S / (4.0 * T * t[m])) / (4.0 * math.pi * T)
    return out


def assessment(q_new, xy, T=K.T_M2D, S=K.S_CONF, image=True, coef=1.0, end=K.COMMON_END):
    """The derogation test's quantity: drawdown at xy at the end of `end` with BH2 at 1,200 m3/d continuously from
    1 April 2015 and at q_new from 1 April 2027."""
    t_tot = ((end + DAY) - K.LICENCE_START).days
    t_new = ((end + DAY) - K.NEW_FROM).days
    return float(K.LICENSED_QD * unit_resp(xy, t_tot, T, S, image, coef)[0]
                 + (q_new - K.LICENSED_QD) * unit_resp(xy, t_new, T, S, image, coef)[0])


def largest_quantity(T=K.T_M2D, S=K.S_CONF, image=True, coef=1.0, limits=None):
    """The continuous quantity at which each protected borehole's predicted drawdown equals its available
    drawdown, and the smallest of them (the derogation test's largest passing quantity)."""
    from scipy.optimize import brentq
    out = {}
    for name, _, _, xy, avail, _, _ in K.PROTECTED:
        lim = (limits or {}).get(name, avail)
        f = lambda q: assessment(q, xy, T, S, image, coef) - lim      # noqa: E731
        out[name] = brentq(f, -20000.0, 200000.0)
    worst = min(out, key=out.get)
    return out[worst], worst, out


# ------------------------------------------------------------------------------------------------- natural levels
def natural_series(day0, day1):
    """The regional head's natural movement (m) on each day, the same signal across both fault blocks: a damped
    seasonal swing peaking in late March and an autoregressive year-to-year departure (wet and dry winters)."""
    n = (day1 - day0).days + 1
    g = K.rng("natural")
    days = [day0 + dt.timedelta(days=i) for i in range(n)]
    doy = np.array([d.timetuple().tm_yday for d in days], float)
    seas = 0.34 * np.cos(2 * np.pi * (doy - 84.0) / 365.25)
    # monthly AR(1) departure, interpolated to days
    months = sorted({(d.year, d.month) for d in days})
    dep = np.zeros(len(months))
    for i in range(1, len(months)):
        dep[i] = 0.86 * dep[i - 1] + g.normal(0, 0.045)
    midx = {m: i for i, m in enumerate(months)}
    mid = np.array([midx[(d.year, d.month)] + (d.day - 1) / 30.0 for d in days])
    depd = np.interp(mid, np.arange(len(months)), dep)
    return days, seas + depd


# ------------------------------------------------------------------------------------------------- the 2014 test
def test_rate_ls(t_h):
    """The test's pumping rate (L/s) through the 72 hours: the meter's settling in the first hours, then steady."""
    t = np.asarray(t_h, float)
    return K.TEST_Q_LS + 0.18 * np.exp(-t / 2.5) - 0.0008 * t


def test_series():
    """Each logger's water level change (m, negative is down) at one-minute steps from 24 hours before the pump
    started to the end of recovery, at the local frame's boreholes. Returns minute index (UTC datetimes) and a
    dict of drawdowns (positive down) including recovery by superposition, before noise."""
    n = (K.TEST_PRE_H + K.TEST_PUMP_H + K.TEST_RECOVERY_H) * 60
    t0 = K.TEST_START_UTC - dt.timedelta(hours=K.TEST_PRE_H)
    times = [t0 + dt.timedelta(minutes=i) for i in range(n)]
    tmin = np.arange(n) - K.TEST_PRE_H * 60                      # minutes since pump on
    t_d = tmin / 1440.0
    # the pumping as a sequence of steps every 10 minutes (the settling rate), then off at 72 h
    steps = []
    prev = 0.0
    for k in range(0, K.TEST_PUMP_H * 6):
        q = float(test_rate_ls(k / 6.0)) * 86.4                   # m3/d
        steps.append((k * 10.0 / 1440.0, q - prev))
        prev = q
    steps.append((K.TEST_PUMP_H / 24.0, -prev))
    out = {}
    pts = dict((k, v["xy"]) for k, v in K.OBS.items())
    pts["BH2"] = (0.15, 0.0)
    for name, xy in pts.items():
        s = np.zeros(n)
        for tk, dq in steps:
            s += dq * unit_resp(xy, t_d - tk)
        if name == "BH2":
            # linear and non-linear well losses while pumping
            q = np.where((t_d > 0) & (t_d <= K.TEST_PUMP_H / 24.0), test_rate_ls(np.maximum(tmin, 0) / 60.0) * 86.4, 0.0)
            s += 3.1e-4 * q + 4.4e-8 * q * q
        out[name] = s
    return times, tmin, out


# ------------------------------------------------------------------------------------------------- abstraction history
def month_iter(a, b):
    y, m = a.year, a.month
    while (y, m) <= (b.year, b.month):
        yield y, m
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)


def history_rates():
    """BH2's mean abstraction in each month from April 2015 to March 2025 (m3/d): the plant's two lines from the
    opening, line 3 from March 2018, line 4 from August 2024, steady growth and a summer peak, all through FM-1.
    The months from April 2025 come from the operations model (the bulk trade through the bay from April 2026)."""
    g = K.rng("history")
    out = {}
    for y, m in month_iter(dt.date(2015, 4, 1), dt.date(2025, 3, 1)):
        yrs = (y - 2015) + (m - 4) / 12.0
        base = 438.0 + 15.0 * yrs + (104.0 if (y, m) >= (2018, 3) else 0.0)
        base += 38.0 * math.cos(2 * math.pi * (m - 7) / 12.0)
        if m == 12:
            base -= 70.0
        if (y, m) >= (2024, 8):
            base += 96.0
        base += g.normal(0, 14)
        out[(y, m)] = (round(base, 1), 0.0)
    return out


def month_days(y, m):
    nxt = dt.date(y + (m == 12), 1 if m == 12 else m + 1, 1)
    return (nxt - dt.date(y, m, 1)).days


def abstraction_monthly(O):
    """True mean abstraction (m3/d) and FM-1's alone in each month from April 2015 to September 2026."""
    hist = history_rates()
    out = {}
    for (y, m), (b, t) in hist.items():
        out[(y, m)] = (b + t, b)
    n = len(O["fm1"]) // 1440
    daily = O["fm1"].reshape(n, 1440).sum(1)
    tank = {}
    for f in O["fills"]:
        k = (f["start"].year, f["start"].month)
        tank[k] = tank.get(k, 0.0) + f["litres"] / 1000.0
    acc = {}
    for i in range(n):
        d = K.OPS_FROM + dt.timedelta(days=i)
        acc[(d.year, d.month)] = acc.get((d.year, d.month), 0.0) + daily[i]
    for k, v in acc.items():
        nd = month_days(*k)
        out[k] = ((v + tank.get(k, 0.0)) / nd, v / nd)
    return out


def drawdown_at(xy, when, monthly, T=K.T_M2D, S=K.S_CONF, image=True, coef=1.0):
    """Drawdown (m) at local point xy at datetime `when` from BH2's monthly abstraction steps since 1 April 2015."""
    s, prev = 0.0, 0.0
    for (y, m) in sorted(monthly):
        st = dt.datetime(y, m, 1)
        if st >= when:
            break
        q = monthly[(y, m)]
        s += (q - prev) * float(unit_resp(xy, (when - st).total_seconds() / 86400.0, T, S, image, coef)[0])
        prev = q
    return s


def long_record(O):
    """Monthly mean water level at OB1 to OB3 (metres above datum), May 2015 to March 2026, the record as returned
    with each licence year's return: the natural head (2015 rest level plus the regional movement) less BH2's
    drawdown under its monthly abstraction."""
    monthly = {k: v[0] for k, v in abstraction_monthly(O).items()}
    days, nat = natural_series(dt.date(2009, 1, 1), K.OPS_TO)
    natm = {}
    for d, v in zip(days, nat):
        natm.setdefault((d.year, d.month), []).append(v)
    natm = {k: float(np.mean(v)) for k, v in natm.items()}
    rest = {"OB1": 89.91, "OB2": 90.12, "OB3": 89.47}
    g = K.rng("longrecord")
    rows = []
    for y, m in month_iter(dt.date(2015, 5, 1), dt.date(2026, 3, 1)):
        mid = dt.datetime(y, m, 1) + dt.timedelta(days=month_days(y, m) / 2.0)
        for ob, info in K.OBS.items():
            dd = drawdown_at(info["xy"], mid, monthly)
            lvl = rest[ob] + natm[(y, m)] - natm[(2015, 4)] - dd + g.normal(0, 0.025)
            rows.append(dict(ob=ob, y=y, m=m, level=lvl, drawdown=dd))
    return rows, rest


def rmb_daily():
    """The regional borehole beyond the fault: the same regional movement on the downthrown block's head, no
    response to BH2, sensor noise, gaps at logger swaps, short outages infilled and flagged estimated, the first days
    after a swap and the odd reading flagged suspect, and the latest weeks not yet checked. Returns (date, level,
    quality)."""
    days, nat = natural_series(dt.date(2009, 1, 1), K.OPS_TO)
    g = K.rng("rmb")
    gaps = [(dt.date(2013, 3, 4), dt.date(2013, 3, 19)), (dt.date(2018, 10, 9), dt.date(2018, 10, 30)),
            (dt.date(2023, 5, 15), dt.date(2023, 5, 24))]
    out = []
    for d, v in zip(days, nat):
        if any(a <= d <= b for a, b in gaps):
            continue
        out.append([d, 84.26 + 1.04 * v + g.normal(0, 0.012), "Good"])
    gq = K.rng("rmbqual")
    idx = {r[0]: i for i, r in enumerate(out)}
    for d0, n in ((dt.date(2011, 8, 22), 4), (dt.date(2016, 7, 11), 5), (dt.date(2020, 1, 27), 3),
                  (dt.date(2024, 11, 18), 6)):
        i0 = idx[d0]
        lo, hi = out[i0 - 1][1], out[i0 + n][1]
        for j in range(n):                                  # an outage infilled between the readings either side
            out[i0 + j][1] = lo + (hi - lo) * (j + 1) / (n + 1)
            out[i0 + j][2] = "Estimated"
    for _, end in gaps:                                     # a new transducer settling after a swap
        for k in (1, 2):
            d = end + dt.timedelta(days=k)
            out[idx[d]][1] += 0.035 / k + gq.normal(0, 0.004)
            out[idx[d]][2] = "Suspect"
    for d in (dt.date(2014, 2, 9), dt.date(2019, 12, 30), dt.date(2022, 6, 14)):
        out[idx[d]][1] += 0.09 if gq.random() < 0.5 else -0.09
        out[idx[d]][2] = "Suspect"
    for r in out:
        if r[0] >= dt.date(2026, 8, 17):
            r[2] = "Unchecked"
    return [tuple(r) for r in out]


# ------------------------------------------------------------------------------------------------- the plant
LINES = ("L1", "L2", "L3", "L4")
SKUS = {
    # code: (description at the time, size ml, line, bottles per hour, rinse litres per bottle)
    "BSP-0500": ("Brackenholt Still 500ml PET", 500, "L1", 26500, 0.118),
    "BSP-0330": ("Brackenholt Still 330ml PET", 330, "L1", 28800, 0.104),
    "BSP-1500": ("Brackenholt Still 1.5L PET", 1500, "L2", 13200, 0.190),
    "BKP-1500": ("Brackenholt Sparkling 1.5L PET", 1500, "L2", 12600, 0.205),
    "BSG-1101": ("Brackenholt Still 75cl glass", 750, "L3", 7300, 0.640),
    "BKG-1102": ("Brackenholt Sparkling 75cl glass", 750, "L3", 7000, 0.660),
    "BSG-1205": ("Brackenholt Still 50cl glass", 500, "L3", 8400, 0.560),
    "BSP-0750": ("Brackenholt Still 750ml PET sports cap", 750, "L4", 18200, 0.142),
    "BKP-0750": ("Brackenholt Sparkling 750ml PET", 750, "L4", 17400, 0.150),
}
SIZE_SWITCH = dt.date(2026, 4, 13)        # BSG-1101 becomes the 70cl hospitality bottle, the code kept
SIZE_AFTER = 700
LINE_BASE_M3H = {"L1": 0.62, "L2": 0.75, "L3": 1.15, "L4": 0.66}     # seal water, lubrication, conveyor sprays while running
CIP_M3 = {"L1": (16.0, 19.0), "L2": (19.0, 23.0), "L3": (27.0, 33.0), "L4": (17.0, 21.0)}
PUMP_LS = 25.0                            # BH2's pump into the plant inlet
BYPASS_LS = 19.6                          # the same pump through the tanker bay's hose and valve
TANK_M3 = 260.0
SHUTDOWNS = [(dt.date(2025, 8, 4), dt.date(2025, 8, 8)), (dt.date(2025, 12, 24), dt.date(2026, 1, 2)),
             (dt.date(2026, 8, 3), dt.date(2026, 8, 7))]
BANK = {dt.date(2025, 5, 5), dt.date(2025, 5, 26), dt.date(2025, 8, 25), dt.date(2026, 4, 3), dt.date(2026, 4, 6),
        dt.date(2026, 5, 4), dt.date(2026, 5, 25)}


def size_at(code, d):
    if code == "BSG-1101" and d >= SIZE_SWITCH:
        return SIZE_AFTER
    return SKUS[code][1]


def production_day(d):
    if any(a <= d <= b for a, b in SHUTDOWNS) or d in BANK:
        return None
    wd = d.weekday()
    if wd <= 4:
        return "full"
    if wd == 5 and 5 <= d.month <= 9:
        return "sat"
    return None


def ops():
    """Minute-level operations from 1 April 2025 to 30 September 2026, local time: bottling runs and cleans (the MES),
    each line's water, the plant inlet meter FM-1 refilling the treated tank on level control, BH2's pump, the
    tanker fills through the bulk bay, the QC fill-weight samples. Returns a dict of record lists."""
    g = K.rng("ops")
    d0, d1 = K.OPS_FROM, K.OPS_TO
    ndays = (d1 - d0).days + 1
    nmin = ndays * 1440
    base_t = dt.datetime.combine(d0, dt.time(0, 0))
    line_use = {ln: np.zeros(nmin) for ln in LINES}          # m3 per minute through each line's sub-meter
    util = np.zeros(nmin)                                     # unmetered plant uses (boilers, washrooms, backwash)
    runs, cips, qc = [], [], []
    l3_campaign = []
    run_no = 31840
    for i in range(ndays):
        d = d0 + dt.timedelta(days=i)
        kind = production_day(d)
        m0 = i * 1440
        # unmetered plant use
        util[m0:m0 + 1440] += 0.55 / 60.0
        seas = 1.0 + 0.045 * math.cos(2 * math.pi * (d.timetuple().tm_yday - 196) / 365.25)
        if kind:
            hrs = (6 * 60, 22 * 60) if kind == "full" else (6 * 60, 14 * 60)
            util[m0 + hrs[0]:m0 + hrs[1]] += (10.6 * seas - 0.55) / 60.0
            if i % 2 == 0:
                util[m0 + 5 * 60:m0 + 5 * 60 + 40] += 18.0 / 40.0       # treatment backwash before the shift
        if not kind:
            continue
        lines_today = ["L1"] if kind == "sat" else ["L1", "L2", "L3", "L4"]
        for ln in lines_today:
            if ln == "L1":
                codes = ["BSP-0500"] if g.random() < 0.62 else ["BSP-0500", "BSP-0330"]
            elif ln == "L2":
                codes = ["BSP-1500"] if g.random() < 0.7 else ["BSP-1500", "BKP-1500"]
            elif ln == "L3":
                r = g.random()
                codes = ["BSG-1101"] if r < 0.42 else (["BSG-1101", "BKG-1102"] if r < 0.75 else ["BSG-1205", "BSG-1101"])
            else:
                codes = ["BSP-0750"] if g.random() < 0.66 else ["BSP-0750", "BKP-0750"]
            start = hrs[0] + int(g.integers(5, 25))
            end_day = hrs[1] - int(g.integers(10, 35))
            span = end_day - start
            cuts = [start]
            if len(codes) == 2:
                cuts.append(start + int(span * g.uniform(0.38, 0.62)))
            cuts.append(end_day)
            for k, code in enumerate(codes):
                rs = cuts[k] + (0 if k == 0 else int(g.integers(28, 45)))     # changeover, no water
                re_ = cuts[k + 1]
                if re_ - rs < 60:
                    continue
                bph = SKUS[code][3]
                eff = g.uniform(0.855, 0.905) * min(1.0, seas)
                filled = int(bph * (re_ - rs) / 60.0 * eff)
                reject = int(filled * g.uniform(0.004, 0.014))
                good = filled - reject
                size_l = size_at(code, d) / 1000.0
                water = filled * (size_l + SKUS[code][4]) + LINE_BASE_M3H[ln] * 1000 * (re_ - rs) / 60.0
                water *= g.uniform(0.985, 1.015)
                line_use[ln][m0 + rs:m0 + re_] += water / 1000.0 / (re_ - rs)
                run_no += int(g.integers(1, 5))
                runs.append(dict(run=run_no, line=ln, sku=code, start=base_t + dt.timedelta(minutes=m0 + rs),
                                 end=base_t + dt.timedelta(minutes=m0 + re_), good=good, reject=reject,
                                 water_m3=water / 1000.0))
                # hourly QC net fill weights (grams) while the run fills
                for qm in range(rs + 20, re_, 60):
                    nominal = size_at(code, d)
                    co2 = 0.0072 if code.startswith("BK") else 0.0      # dissolved carbon dioxide in sparkling
                    over = 1.012 if ln == "L3" else 1.0015              # glass filled to a level, PET checkweighed
                    w = nominal * (over + co2) + g.normal(0, 2.4 if ln == "L3" else 1.6)
                    if g.random() < 0.006:
                        w -= g.uniform(20, 30) if ln == "L3" else g.uniform(7, 14)   # an underfill caught and rejected
                    qc.append(dict(t=base_t + dt.timedelta(minutes=m0 + qm + int(g.integers(0, 6))), line=ln,
                                   sku=code, net_g=round(w, 1), run=run_no))
        # cleans: L1 and L2 each Friday after the shift; L3 at the end of each campaign (every second or third day)
        if kind == "full":
            todo = []
            if d.weekday() == 4:
                todo += ["L1", "L2", "L4"]
            l3_campaign.append(d)
            nxt = d + dt.timedelta(days=1)
            if len(l3_campaign) >= 3 or d.weekday() == 4 or production_day(nxt) != "full" or (len(l3_campaign) == 2 and g.random() < 0.5):
                todo.append("L3")
                l3_campaign = []
            for ln in todo:
                lo, hi = CIP_M3[ln]
                vol = g.uniform(lo, hi)
                dur = int(g.integers(80, 115))
                t_c = 21 * 60 + 58 + int(g.integers(0, 4))
                line_use[ln][m0 + t_c:m0 + t_c + dur] += vol / dur
                run_no += int(g.integers(1, 4))
                cips.append(dict(run=run_no, line=ln, start=base_t + dt.timedelta(minutes=m0 + t_c),
                                 end=base_t + dt.timedelta(minutes=m0 + t_c + dur), water_m3=vol))
    settle_l3(line_use, runs, cips, base_t)
    # a day's metered volume never sits within 2 cubic metres of the licensed quantity: where the tank's refills put
    # one there, that day's boiler blowdown runs a few cubic metres longer (the plant's usual day-to-day variation)
    for _ in range(8):
        demand = util + sum(line_use.values())
        fm1, pump_plant = tank(demand, nmin)
        daily = fm1.reshape(ndays, 1440).sum(1)
        near = np.where(abs(daily - K.LICENSED_QD) < 2.5)[0]
        if not len(near):
            break
        for i in near:
            util[i * 1440 + 9 * 60:i * 1440 + 12 * 60] += 5.5 / 180.0
    else:
        raise SystemExit("metered days still at the licensed quantity")
    k = tanker_draw(fm1, d0, ndays, nmin, base_t, pump_plant)
    fills = tanker_fills(K.rng("tankers", k), d0, ndays, nmin, base_t, pump_plant)
    fills = settle_fills(fills, fm1, d0, ndays, nmin, base_t, pump_plant)
    return dict(tanker_draw=k, base=base_t, nmin=nmin, line_use=line_use, util=util, fm1=fm1, pump_plant=pump_plant, runs=runs,
                cips=cips, qc=qc, fills=fills)


def l3_ratios(line_use, runs, base_t):
    """Line 3's water per litre packed in each local month of the 2025-26 licence year, at the sizes filled."""
    out = {}
    for y, m in month_iter(dt.date(2025, 4, 1), dt.date(2026, 3, 1)):
        a = int((dt.datetime(y, m, 1) - base_t).total_seconds() // 60)
        nxt = dt.datetime(y + (m == 12), m % 12 + 1, 1)
        b = int((nxt - base_t).total_seconds() // 60)
        water = float(line_use["L3"][a:b].sum())
        packed = sum(r["good"] * size_at(r["sku"], r["start"].date()) / 1000.0 for r in runs
                     if r["line"] == "L3" and (r["start"].year, r["start"].month) == (y, m))
        out[(y, m)] = (water, packed)
    return out


def settle_l3(line_use, runs, cips, base_t):
    """A month's line 3 cleans use 27 to 33 cubic metres each; where a month's water per litre packed sits within a
    hair of a two-decimal rounding edge, that month's cleans run a little longer or shorter on rinse (under a cubic
    metre each), moving the ratio three thousandths clear of the edge."""
    for (y, m), (water, packed) in l3_ratios(line_use, runs, base_t).items():
        r = water * 1000.0 / packed
        edge = (round(r * 100.0 - 0.5) + 0.5) / 100.0
        if abs(r - edge) >= 0.002:
            continue
        target = edge + (0.003 if r >= edge else -0.003)
        dw = (target - r) * packed / 1000.0
        mine = [c for c in cips if c["line"] == "L3" and (c["start"].year, c["start"].month) == (y, m)]
        for c in mine:
            m0 = int((c["start"] - base_t).total_seconds() // 60)
            m1 = int((c["end"] - base_t).total_seconds() // 60)
            line_use["L3"][m0:m1] += dw / len(mine) / (m1 - m0)
            c["water_m3"] += dw / len(mine)


def tank(demand, nmin):
    """The treated tank on level control: FM-1 fills it from 40 per cent to 92 per cent at the pump's rate, which
    drifts with the borehole's level and the main's back-pressure from one run to the next."""
    g = K.rng("pumprate")
    level = 0.80 * TANK_M3
    fm1 = np.zeros(nmin)
    pump_plant = np.zeros(nmin, bool)
    on = False
    q_min = PUMP_LS * 60.0 / 1000.0
    lo, hi = 0.40 * TANK_M3, 0.92 * TANK_M3
    dem = demand.tolist()
    for m in range(nmin):
        if not on and level < lo:
            on = True
            q_min = (PUMP_LS - 0.25 * m / nmin + g.normal(0, 0.16)) * 60.0 / 1000.0
        if on and level > hi:
            on = False
        if on:
            fm1[m] = q_min
            level += q_min
            pump_plant[m] = True
        level -= dem[m]
        if level < 0.0:
            level = 0.0
    return fm1, pump_plant


def tanker_fills(gt, d0, ndays, nmin, base_t, pump_plant):
    """The haulier's night shift runs 18:00 to 06:00 and its tickets carry the date the shift began. Fills are booked
    on Sunday to Thursday nights (rarely Friday or Saturday) between 22:30 and 05:20, through the bulk bay's valve on
    the raw main, never in a quarter-hour in which the plant's inlet refills the tank (the pump serves one or the
    other), and never across midnight."""
    fills = []
    for i in range(ndays):
        d = d0 + dt.timedelta(days=i)
        if d < K.BULK_FROM:
            continue
        p = 0.10 if d.weekday() in (4, 5) else 0.93
        if any(a <= d <= b for a, b in SHUTDOWNS[1:2]):
            p = 0.0
        if gt.random() > p:
            continue
        nfill = 1 + int(gt.random() < 0.70) + int(gt.random() < 0.34)
        slots = sorted(gt.choice(np.arange(0, 405, 5), size=nfill, replace=False))
        last_end = -1
        for s in slots:
            st = (i * 1440) + 22 * 60 + 30 + int(s) + int(gt.integers(0, 4))
            if st <= last_end + 20:
                st = last_end + 20 + int(gt.integers(3, 12))
            litres = float(round(gt.uniform(25800, 29900), -1))
            dur_s = litres / (BYPASS_LS + gt.normal(0, 0.07))
            en = st + int(math.ceil(dur_s / 60.0))
            midnight = (i + 1) * 1440
            if st < midnight <= en:
                st, en = midnight + 6, midnight + 6 + (en - st)
            if en >= nmin or pump_plant[(st // 15) * 15:-(-(en + 1) // 15) * 15].any() or st <= last_end:
                continue
            day_of = (base_t + dt.timedelta(minutes=st)).date()
            if day_of in (dt.date(2025, 10, 26), dt.date(2026, 3, 29)) and st % 1440 < 3 * 60:
                continue                                            # the haulier does not load across a clock change
            last_end = en
            fills.append(dict(start=base_t + dt.timedelta(minutes=st), seconds=int(round(dur_s)), litres=litres,
                              shift_date=d))
    return fills


def _months(d0, ndays):
    idx = {}
    for i in range(ndays):
        d = d0 + dt.timedelta(days=i)
        idx.setdefault((d.year, d.month), []).append(i)
    return {k: np.array(v) for k, v in idx.items() if (2026, 4) <= k <= (2026, 9)}


def separation(fm1, fills, d0, ndays, months=None):
    """For each month from April to September 2026: the days over the daily quantity on FM-1 alone, with each fill on
    its own calendar day, and with each fill on its ticket's shift date."""
    months = months or _months(d0, ndays)
    daily = fm1.reshape(ndays, 1440).sum(1)
    true, tick = daily.copy(), daily.copy()
    for f in fills:
        i = (f["start"].date() - d0).days
        j = (f["shift_date"] - d0).days
        if 0 <= i < ndays:
            true[i] += f["litres"] / 1000.0
        if 0 <= j < ndays:
            tick[j] += f["litres"] / 1000.0
    return {k: (int((daily[ix] > K.LICENSED_QD).sum()), int((true[ix] > K.LICENSED_QD).sum()),
                int((tick[ix] > K.LICENSED_QD).sum())) for k, ix in months.items()}, true


def bins_ok(true, months):
    """Every month's true volume at least 15 cubic metres from a rounding edge of the nearest 100, and no day's
    true volume within 2 cubic metres of the licensed 1,200."""
    if (abs(true - K.LICENSED_QD) < 2.0).any():
        return False
    for ix in months.values():
        v = float(true[ix].sum())
        if 50.0 - abs(v - round(v / 100.0) * 100.0) < 15.0:
            return False
    return True


def tanker_draw(fm1, d0, ndays, nmin, base_t, pump_plant):
    """The first draw of the haulier's bookings in which every month's count of days over the daily quantity differs
    between FM-1 alone and the true calendar, and between the ticket dates and the true calendar, with every month's
    true volume clear of a rounding edge and no day's true volume at the licensed quantity."""
    months = _months(d0, ndays)
    for k in range(5000):
        fills = tanker_fills(K.rng("tankers", k), d0, ndays, nmin, base_t, pump_plant)
        sep, true = separation(fm1, fills, d0, ndays, months)
        if all(c != t and k_ != t for c, t, k_ in sep.values()):
            return k
    raise SystemExit("no tanker draw separates every month")


def settle_fills(fills, fm1, d0, ndays, nmin, base_t, pump_plant):
    """Loads vary between about 25,800 and 29,900 litres. Where a day's true volume sits within 2.5 cubic metres of
    the licensed quantity, its first load is a few cubic metres larger or smaller, away from the line; where a
    month's true volume sits within 15 cubic metres of a rounding edge of the nearest 100, loads on days far from
    the line are adjusted toward the centre. No day crosses the licensed quantity, so every count stays put."""
    months = _months(d0, ndays)
    daily = fm1.reshape(ndays, 1440).sum(1)
    fills = [dict(f) for f in fills]
    rate = {id(f): f["litres"] / f["seconds"] for f in fills}

    def day_of(f):
        return (f["start"].date() - d0).days

    def true():
        t = daily.copy()
        for f in fills:
            i = day_of(f)
            if 0 <= i < ndays:
                t[i] += f["litres"] / 1000.0
        return t

    def set_litres(f, litres):
        r = f["litres"] / f["seconds"]
        litres = float(round(litres, -1))
        secs = int(round(litres / r))
        m0 = int((f["start"] - base_t).total_seconds() // 60)
        m1 = m0 + int(math.ceil(secs / 60.0))
        if not (24800.0 <= litres <= 31000.0) or m1 >= nmin or pump_plant[(m0 // 15) * 15:-(-(m1 + 1) // 15) * 15].any():
            return False
        for g_ in fills:
            if g_ is not f and abs((g_["start"] - f["start"]).total_seconds()) < 3600:
                gm0 = int((g_["start"] - base_t).total_seconds() // 60)
                if gm0 > m0 and gm0 < m1 + 3:
                    return False
        f["litres"], f["seconds"] = litres, secs
        return True
    t = true()
    for i in np.where(abs(t - K.LICENSED_QD) < 2.5)[0]:
        on = [f for f in fills if day_of(f) == i]
        sign = 1.0 if t[i] > K.LICENSED_QD else -1.0
        need = 2.5 - abs(t[i] - K.LICENSED_QD) + 0.3
        done = False
        for extra in (0.0, 0.8, 1.6, 2.4):
            for f in on:
                if set_litres(f, f["litres"] + sign * 1000.0 * (need + extra)):
                    done = True
                    break
            if done:
                break
        if not done:
            raise SystemExit("cannot clear day %s from the licensed quantity" % (d0 + dt.timedelta(days=int(i))))
    t = true()
    for key, ix in months.items():
        v = float(t[ix].sum())
        c = round(v / 100.0) * 100.0
        need = (abs(v - c) - 25.0) if 50.0 - abs(v - c) < 15.0 else 0.0
        if need <= 0:
            continue
        direction = -1.0 if v > c else 1.0
        moved = 0.0
        for f in sorted([f for f in fills if day_of(f) in set(ix.tolist())], key=lambda x: x["start"]):
            i = day_of(f)
            margin = abs(t[i] - K.LICENSED_QD) - 3.0
            if moved >= need or margin <= 0:
                continue
            step = min(need - moved, 3.8, margin) * direction
            if set_litres(f, f["litres"] + 1000.0 * step):
                moved += abs(step)
                t = true()
        if moved < need - 0.5:
            raise SystemExit("cannot centre %s" % (key,))
    return fills

