"""The physical world behind task156, before any export is written: the hourly rainfall at the climate station, the
terrace water table, PS03's sewers and their invert levels, the station's inflow, its storage and its overflows.
Nothing here ships; records.py writes the exports from it."""
from __future__ import annotations

import datetime as dt
import functools
import zoneinfo

import numpy as np

import world as W

AKL = zoneinfo.ZoneInfo("Pacific/Auckland")


@functools.lru_cache(maxsize=1)
def clock():
    """Hourly UTC index from 2004-01-01 00:00 NZST to 2026-11-01 00:00 NZDT, with each hour's NZST date (the archive's
    and the bore's day), its local civil hour and weekday (the town's day), and its year in NZST."""
    n = int((W.H1 - W.H0).total_seconds() // 3600)
    utc = [W.H0 + dt.timedelta(hours=i) for i in range(n)]
    nzst = [u.astimezone(W.NZST) for u in utc]
    loc = [u.astimezone(AKL) for u in utc]
    C = type("Clock", (), {})()
    C.n = n
    C.utc = utc
    C.nzst_date = np.array([(x.date() - dt.date(2004, 1, 1)).days for x in nzst])
    C.year = np.array([x.year for x in nzst])
    C.month = np.array([x.month for x in nzst])
    C.local_hour = np.array([x.hour for x in loc])
    C.local_dow = np.array([x.weekday() for x in loc])
    C.nd = int(C.nzst_date[-1]) + 1
    C.dates = [dt.date(2004, 1, 1) + dt.timedelta(days=d) for d in range(C.nd)]
    C.d_year = np.array([d.year for d in C.dates])
    C.d_month = np.array([d.month for d in C.dates])
    C.d_doy = np.array([d.timetuple().tm_yday for d in C.dates])
    C.meter = C.year >= 2024
    C.replay = (C.year >= W.REPLAY_Y0) & (C.year <= W.REPLAY_Y1)
    return C


@functools.lru_cache(maxsize=1)
def rainfall():
    """Hourly rain (mm) at the climate station: storms arriving as a seasonal Poisson process, each with its own
    duration, depth and cells, summer storms shorter with a convective burst a quarter of the time."""
    C = clock()
    r = np.zeros(C.n)
    g = W.rng("rain")
    t = 0.0
    while True:
        m = C.month[min(int(t), C.n - 1)]
        rate = (1 / 70.0) * (1.0 + 0.35 * np.cos(2 * np.pi * (m - 7) / 12))
        t += g.exponential(1 / rate)
        if t >= C.n:
            break
        m = C.month[int(t)]
        summer = m in (12, 1, 2, 3)
        dur = max(1, int(g.exponential(5.0 if summer else 9.0)))
        depth = g.gamma(0.75, 14.0 if summer else 13.0)
        w = g.gamma(0.6, 1.0, dur)
        if summer and g.random() < 0.25:
            w[g.integers(0, dur)] += w.sum() * g.uniform(1.5, 4.0)
        w = w / w.sum()
        i0 = int(t)
        seg = r[i0:i0 + dur]
        seg += depth * w[:len(seg)]
    return np.round(r / 0.2) * 0.2      # whole tips of the 0.2 mm bucket


WET = {2004: 0.1, 2005: 0.8, 2006: 0.2, 2007: 0.9, 2008: 0.95, 2009: 0.3, 2010: 0.75, 2011: 0.95, 2012: 0.0,
       2013: 0.9, 2014: 0.2, 2015: 0.8, 2016: 0.1, 2017: 0.95, 2018: 0.85, 2019: 0.0, 2020: 0.3, 2021: 0.9,
       2022: 0.95, 2023: 0.4, 2024: 0.05, 2025: 0.0, 2026: 0.10}
WET_AMP, WET_WIDTH = 2.55, 100.0          # m of rise at the height of a wet winter, days of its spread
SPELL_AMP, SPELL_DOY, SPELL_WIDTH = 3.25, 170, 13.0   # the June 2025 high river


@functools.lru_cache(maxsize=1)
def water_table():
    """Daily mean water table under the low terrace (m NZVD2016): a small seasonal swing, the river's wet winters
    (the river follows its upper catchment, not the town's rain), slow recharge from local rain and a red noise."""
    C = clock()
    g = W.rng("water table")
    seas = np.zeros(C.nd)
    for i in range(C.nd):
        y, dy = C.d_year[i], C.d_doy[i]
        hump = np.exp(-0.5 * ((dy - 228) / WET_WIDTH) ** 2)
        seas[i] = 0.35 * np.cos(2 * np.pi * (dy - 240) / 365.25) + WET_AMP * WET[y] * hump
        if y == 2025:
            seas[i] += SPELL_AMP * np.exp(-0.5 * ((dy - SPELL_DOY) / SPELL_WIDTH) ** 2)
    noise = np.zeros(C.nd)
    a = 0.0
    for i in range(C.nd):
        a = 0.97 * a + g.normal(0, 0.035)
        noise[i] = a
    rd = np.bincount(C.nzst_date, weights=rainfall(), minlength=C.nd)
    rech = np.zeros(C.nd)
    s = 0.0
    for i in range(C.nd):
        s = 0.985 * s + 0.0025 * rd[i]
        rech[i] = s
    return 12.55 + seas + noise + rech - rech.mean()


@functools.lru_cache(maxsize=1)
def terrace_pipes():
    """PS03's gravity mains on the low terrace as tuples (index, length m, downstream invert, upstream invert,
    diameter mm, material, install year)."""
    return [(p["k"], p["L"], p["dsi"], p["usi"], p["dia"], p["mat"], p["yr"]) for p in terrace_network()]


@functools.lru_cache(maxsize=1)
def terrace_network():
    """PS03's low terrace sewers as a tree of manholes and pipes: the trunk rising gently from the station, branch
    sewers dropping into its manholes, sub-branches off the branches. Each pipe carries its own downstream and
    upstream invert (m NZVD2016), length, diameter, material and install year."""
    g = W.rng("terrace network")
    pipes = []
    mh = {}

    def new_mh(inv):
        k = len(mh)
        mh[k] = inv
        return k

    def era():
        yr = int(g.choice([1958, 1962, 1965, 1968, 1971, 1974, 1978, 1983, 1989, 1996, 2004],
                          p=[0.08, 0.14, 0.14, 0.13, 0.12, 0.1, 0.09, 0.07, 0.06, 0.04, 0.03]))
        mat = "AC" if yr < 1975 and g.random() < 0.55 else ("VC" if yr < 1980 else ("PVC" if yr < 2000 else "PE"))
        return yr, mat

    def chain(ds_mh, start_inv, n, Lr, grad, dia_choice):
        down = ds_mh
        inv = start_inv
        made = []
        for _ in range(n):
            L = round(float(g.uniform(*Lr)), 1)
            rise = L * g.uniform(*grad)
            if inv + rise > 16.9:
                break
            up = new_mh(inv + rise)
            yr, mat = era()
            dia = int(g.choice(dia_choice[0], p=dia_choice[1]))
            if dia >= 375 and yr < 1990:
                mat = "RCRRJ"
            pipes.append(dict(k=len(pipes), L=L, dsi=round(float(inv), 3), usi=round(float(inv + rise), 3), dia=dia,
                              mat=mat, yr=yr, us_mh=up, ds_mh=down))
            made.append(up)
            down = up
            inv = inv + rise
        return made

    outlet = new_mh(12.10)
    trunk = chain(outlet, 12.18, 44, (60, 110), (0.0014, 0.0026), ([375, 450, 525], [0.3, 0.4, 0.3]))
    second = chain(trunk[2], mh[trunk[2]] + 0.35, 36, (55, 105), (0.0016, 0.003), ([300, 375, 450], [0.3, 0.4, 0.3]))
    trunk = trunk + second
    branch_mhs = []
    for t_mh in trunk:
        for _ in range(int(g.choice([1, 2, 2, 3, 3, 4]))):
            drop = g.uniform(0.25, 0.85)
            made = chain(t_mh, mh[t_mh] + drop, int(g.integers(2, 6)), (35, 95), (0.0018, 0.0042),
                         ([150, 225, 300], [0.45, 0.4, 0.15]))
            branch_mhs.extend(made[:2])
    for b_mh in branch_mhs:
        if g.random() < 0.22 and len(pipes) < 560:
            chain(b_mh, mh[b_mh] + g.uniform(0.05, 0.3), int(g.integers(2, 5)), (30, 80), (0.0025, 0.005),
                  ([150, 225], [0.7, 0.3]))
    terrace_network.manholes = mh
    return pipes


def lsub(level, pipes=None, ref="invert"):
    """Kilometres of PS03's terrace sewer lying below a water level: each pipe's length below the level, the invert
    taken as falling straight between its two ends ("invert"), or its crown or centreline when asked."""
    pipes = pipes or terrace_pipes()
    level = np.asarray(level, dtype=float)
    out = np.zeros_like(level)
    for _, L, dsi, usi, dia, _, _ in pipes:
        off = {"invert": 0.0, "centre": dia / 2000.0, "crown": dia / 1000.0}[ref]
        a, b = dsi + off, usi + off
        out += L * np.clip((level - a) / (b - a), 0.0, 1.0)
    return out / 1000.0


def unit_hydrograph(tp, tb, step_h=1.0):
    t = np.arange(0, tb + step_h / 2, step_h)
    u = np.clip(np.where(t <= tp, t / tp, (tb - t) / (tb - tp)), 0, None)
    return u / u.sum()


DIURNAL_WD = np.array([0.42, 0.36, 0.33, 0.33, 0.38, 0.55, 1.05, 1.62, 1.78, 1.55, 1.30, 1.15,
                       1.08, 1.02, 0.96, 0.95, 1.00, 1.12, 1.30, 1.38, 1.25, 1.02, 0.78, 0.58])
DIURNAL_WE = np.roll(DIURNAL_WD, 1) * np.array([1.0] * 6 + [0.85, 0.9, 1.05, 1.15, 1.1, 1.05] + [1.0] * 12)
DIURNAL_WD = DIURNAL_WD / DIURNAL_WD.mean()
DIURNAL_WE = DIURNAL_WE / DIURNAL_WE.mean()


@functools.lru_cache(maxsize=1)
def domestic_profile():
    C = clock()
    return np.where(C.local_dow >= 5, DIURNAL_WE[C.local_hour], DIURNAL_WD[C.local_hour])


def domestic(dwellings, persons=W.PERSONS_PER_DWELLING, lpd=W.LPD_ACTUAL, profile=None):
    prof = domestic_profile() if profile is None else profile
    return dwellings * persons * lpd / 86400.0 * prof


@functools.lru_cache(maxsize=1)
def truth():
    """The station's true hourly inflow (L/s) and its parts."""
    C = clock()
    rain = rainfall()
    wt = water_table()
    ls_d = lsub(wt)
    ls_h = ls_d[C.nzst_date]
    uf = unit_hydrograph(*W.UH_FAST)
    us = unit_hydrograph(*W.UH_SLOW)
    fast = np.convolve(rain, uf)[:C.n]
    slowl = np.convolve(rain * ls_h, us)[:C.n]
    T = type("Truth", (), {})()
    T.rain, T.wt, T.ls_d, T.ls_h, T.fast, T.slowl = rain, wt, ls_d, ls_h, fast, slowl
    T.dom = domestic(W.DWELLINGS_EXISTING)
    T.gwi = W.C0 + W.G * ls_h
    T.rdii = (W.RF * fast + W.RS * slowl) / 3.6
    T.q = T.dom + T.gwi + T.rdii
    return T


def route(q, qp=W.QP, store=W.STORE, step_h=1.0):
    """Storage routing at the station: the store fills when inflow exceeds the pumps and empties when it falls below;
    a step in which the store would pass the weir spills. Returns the spill flag per step and the store per step."""
    s = 0.0
    k = 3.6 * step_h
    spill = np.zeros(len(q), dtype=bool)
    level = np.zeros(len(q))
    for i in range(len(q)):
        s += (q[i] - qp) * k
        if s < 0:
            s = 0.0
        elif s > store:
            spill[i] = True
            s = store
        level[i] = s
    return spill, level


def events(spill, sep_steps):
    out, last = [], -10 ** 9
    for i in np.nonzero(spill)[0]:
        if i - last > sep_steps:
            out.append(i)
        last = i
    return np.array(out, dtype=int)


def per_year(ev, years, y0=W.REPLAY_Y0, y1=W.REPLAY_Y1):
    ys = years[ev]
    return np.array([int(np.sum(ys == y)) for y in range(y0, y1 + 1)])


def replay_mean(q, store=W.STORE, qp=W.QP):
    C = clock()
    sp, _ = route(q, qp, store)
    ev = events(sp, W.SPILL_SEP_H)
    return float(per_year(ev, C.year).mean()), per_year(ev, C.year)


def subdivision_flow(dwellings=sum(W.SUB_DWELLINGS)):
    """The code of practice's design flow for the subdivision (its occupancy, its litres a person, its diurnal
    table read in the town's local time)."""
    import codeofpractice as CP
    C = clock()
    prof = CP.profile_factors()[C.local_hour]
    return dwellings * W.COP_OCC * W.COP_LPD / 86400.0 * prof


@functools.lru_cache(maxsize=1)
def meter15():
    """The station through the SCADA's 15-minute intervals, 2024-01-01 00:00 NZDT to 2026-10-31 23:45 NZDT: the true
    inflow (each hour's mean kept, a straight trend between neighbouring hours inside it), the store routed at 15
    minutes, the wet well level, the spill and the pumped flow."""
    C = clock()
    T = truth()
    i0 = int((dt.datetime(2023, 12, 31, 11, tzinfo=W.UTC) - W.H0).total_seconds() // 3600)
    qh = np.concatenate([T.q[i0 - 1:], T.q[-1:]])
    n = C.n - i0
    q = np.zeros(n * 4)
    for k in range(4):
        q[k::4] = qh[1:-1] + (qh[2:] - qh[:-2]) * (k - 1.5) / 8.0
    s = 0.0
    level = np.zeros(n * 4)
    spill = np.zeros(n * 4)
    pumped = np.zeros(n * 4)
    store = np.zeros(n * 4)
    for j in range(n * 4):
        s += (q[j] - W.QP) * 0.9
        sp = 0.0
        if s < 0:
            pumped[j] = W.QP + s / 0.9
            s = 0.0
        elif s > W.STORE:
            sp = (s - W.STORE) / 0.9
            s = W.STORE
            pumped[j] = W.QP
        else:
            pumped[j] = W.QP
        spill[j] = sp
        store[j] = s
        level[j] = store_to_level(s, sp)
    M = type("Meter", (), {})()
    M.i0 = i0
    M.n = n * 4
    M.utc0 = W.H0 + dt.timedelta(hours=i0)
    M.q, M.level, M.spill, M.pumped, M.store = q, level, spill, pumped, store
    return M


def store_to_level(s, spill_ls=0.0):
    """Wet well level above the floor for a store volume: the wet well's 38 m3 above the duty pump's start level, then
    the emergency chamber up to the weir crest, then the head over the weir while it spills (Q = 1.71 L h^1.5,
    L = 1.6 m)."""
    if spill_ls > 0:
        return W.WEIR_ABOVE_FLOOR + (spill_ls / 1000.0 / (1.71 * 1.6)) ** (2.0 / 3.0)
    if s <= W.WET_WELL_STORE:
        return W.DUTY_START + s / W.WET_WELL_STORE * 2.35
    return W.DUTY_START + 2.35 + (s - W.WET_WELL_STORE) / (W.STORE - W.WET_WELL_STORE) * (
        W.WEIR_ABOVE_FLOOR - W.DUTY_START - 2.35)


def spills15(M=None, sep=W.SPILL_SEP_H * 4):
    """The meter's spills as (start index, stop index) runs of 15-minute intervals with spill, and the overflows they
    make under the consent's separation."""
    M = M or meter15()
    on = M.spill > 0
    runs = []
    j = 0
    while j < M.n:
        if on[j]:
            k = j
            while k < M.n and on[k]:
                k += 1
            runs.append((j, k))
            j = k
        else:
            j += 1
    overflows = []
    for r in runs:
        if overflows and r[0] - overflows[-1][-1][1] <= sep:
            overflows[-1].append(r)
        else:
            overflows.append([r])
    return runs, overflows
