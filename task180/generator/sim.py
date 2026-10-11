"""Simulate the Ellesmere Lines zone-substation fleet: weather, load, top-oil temperature, tap
operations and counters (hourly and daily), the oil sampling calendar, the laboratory results and the
moisture readings. Everything is drawn from fixed numpy generators seeded from world.SEED.
"""
import datetime as dt
import math

import numpy as np
import pandas as pd

import world as W

ONE = dt.timedelta(days=1)


def rng(k):
    return np.random.default_rng(W.SEED * 1000 + k)


# ---------------------------------------------------------------------------------------------
# calendar
def days():
    """Local calendar days 2021-01-01 .. 2026-10-16 (the counter file carries 00:00 readings to the
    extract date)."""
    n = (W.EXTRACT_DATE - W.START).days + 1
    return [W.START + dt.timedelta(i) for i in range(n)]


def hours_utc():
    """UTC hour starts covering local 2021-01-01 00:00 to local 2026-10-16 00:00 (exclusive)."""
    a = pd.Timestamp(dt.datetime(2021, 1, 1, tzinfo=W.TZ)).tz_convert("UTC")
    b = pd.Timestamp(dt.datetime(2026, 10, 16, tzinfo=W.TZ)).tz_convert("UTC")
    return pd.date_range(a, b, freq="h", inclusive="left")


def doy_frac(d):
    return (d.timetuple().tm_yday - 1) / 365.25


# ---------------------------------------------------------------------------------------------
# outages: a tap-changer service takes the unit out from 20:00 the evening before to 07:00 the
# morning after; oil processing for its stated days (from 07:00 on the first to 17:00 on the last)
def outages():
    out = {}
    for tid, svcs in W.OLTC_SERVICES.items():
        for d, _ in svcs:
            if d < W.START:
                continue
            a = dt.datetime.combine(d - ONE, dt.time(20, 0))
            b = dt.datetime.combine(d + ONE, dt.time(7, 0))
            out.setdefault(tid, []).append((a, b, "oltc"))
    for tid, d, n in W.OIL_PROCESSING:
        a = dt.datetime.combine(d, dt.time(7, 0))
        b = dt.datetime.combine(d + dt.timedelta(n - 1), dt.time(17, 0))
        out.setdefault(tid, []).append((a, b, "oil"))
    return out


# ---------------------------------------------------------------------------------------------
# weather: daily mean with a synoptic anomaly, plus a diurnal cycle (min 06:30, max 15:00 local)
def weather(dlist):
    r = rng(1)
    n = len(dlist)
    an = np.zeros(n)
    e = r.normal(0, 1.9, n)
    for i in range(1, n):
        an[i] = 0.74 * an[i - 1] + e[i]
    seas = np.array([11.8 - 5.6 * math.cos(2 * math.pi * (doy_frac(d) - 0.04)) for d in dlist])
    tmean = seas + an
    amp = np.array([4.6 + 1.6 * (1 + math.cos(2 * math.pi * (doy_frac(d) - 0.04))) / 2 for d in dlist])
    amp = amp * np.clip(1 + r.normal(0, 0.22, n), 0.5, 1.6)
    return tmean, amp


def diurnal(h):
    """Shape in [-1, 1]: min near 06:30, max near 15:00 local."""
    x = (h - 6.5) % 24
    return np.where(x <= 8.5, -np.cos(np.pi * x / 8.5), np.cos(np.pi * (x - 8.5) / 15.5))


# ---------------------------------------------------------------------------------------------
# load: each substation's demand split between its two transformers running in parallel
SUB_MIX = {  # residential, irrigation, industrial (shares of the substation's mean demand), mean MVA
    "LST": (0.42, 0.28, 0.30, 4.9), "SBG": (0.38, 0.52, 0.10, 4.4), "DYL": (0.40, 0.55, 0.05, 3.1),
    "DSL": (0.30, 0.38, 0.32, 5.0), "LIN": (0.78, 0.07, 0.15, 10.6), "SPN": (0.66, 0.20, 0.14, 10.1),
    "LDB": (0.55, 0.40, 0.05, 4.3), "PRB": (0.85, 0.05, 0.10, 9.8), "RLS": (0.62, 0.08, 0.30, 11.2),
    "BNM": (0.40, 0.15, 0.45, 9.6), "WDS": (0.45, 0.45, 0.10, 4.5), "WML": (0.60, 0.35, 0.05, 4.6),
    "KRW": (0.42, 0.52, 0.06, 4.4), "DFD": (0.45, 0.35, 0.20, 9.9), "TPR": (0.30, 0.66, 0.04, 3.2),
    "HOR": (0.32, 0.62, 0.06, 3.3), "CGT": (0.52, 0.42, 0.06, 3.0), "GLT": (0.60, 0.35, 0.05, 2.8),
    "SHF": (0.72, 0.24, 0.04, 2.6), "SPF": (0.80, 0.15, 0.05, 2.7), "WDN": (0.58, 0.38, 0.04, 2.9),
    "GDL": (0.42, 0.54, 0.04, 3.1),
}


def irrigation_season(dlist):
    r = rng(2)
    base = np.array([max(0.0, math.cos(2 * math.pi * (doy_frac(d) - 0.05))) ** 0.75 for d in dlist])
    # dry and wet spells, weekly persistence
    wk = np.zeros(len(dlist))
    v = 1.0
    for i in range(len(dlist)):
        if i % 7 == 0:
            v = float(np.clip(0.55 * v + 0.45 * r.normal(1.0, 0.32), 0.35, 1.6))
        wk[i] = v
    return base * wk


def plant_regimes(dlist, seed, shutdown=False):
    """A processing plant's switching regime: idle, normal or heavy, held for one to five weeks.
    It drives the step loads and so the tap changes; it has no season."""
    r = rng(seed)
    levels = np.array([0.06, 1.0, 2.3])
    out = np.zeros(len(dlist))
    state = 1
    hold = 0
    for i, d in enumerate(dlist):
        if hold <= 0:
            p = {0: [0.0, 0.7, 0.3], 1: [0.3, 0.0, 0.7], 2: [0.35, 0.65, 0.0]}[state]
            state = int(r.choice(3, p=p))
            hold = int(r.integers(6, 36))
        hold -= 1
        lv = levels[state] * float(np.clip(r.normal(1.0, 0.12), 0.6, 1.4))
        if shutdown and ((d.month == 12 and d.day >= 21) or (d.month == 1 and d.day <= 17)):
            lv = 0.05
        out[i] = lv
    return out


def hourly(dlist):
    """Hourly load (MVA) and top-oil temperature (C) per transformer on the UTC hour grid."""
    hu = hours_utc()
    loc = hu.tz_convert(W.TZ)
    lhour = np.asarray(loc.hour, dtype=float) + np.asarray(loc.minute, dtype=float) / 60.0 + 0.5
    ldate = np.array([dt.date(y, m, d) for y, m, d in zip(loc.year, loc.month, loc.day)])
    di = np.array([(x - W.START).days for x in ldate])
    wkend = np.asarray(loc.dayofweek) >= 5
    tmean, amp = weather(dlist)
    amb = tmean[di] + amp[di] * diurnal(lhour)
    irr = irrigation_season(dlist)
    winter = np.array([(1 + math.cos(2 * math.pi * (doy_frac(d) - 0.54))) / 2 for d in dlist])
    heat = np.clip(13.0 - tmean, 0, None) / 10.0
    # residential daily shape
    hm = lhour
    res = (0.52 + 0.30 * np.exp(-((hm - np.where(wkend, 9.6, 8.0)) / 1.4) ** 2)
           + 0.58 * np.exp(-((hm - 18.7) / 2.1) ** 2) - 0.18 * np.exp(-((hm - 3.5) / 2.0) ** 2))
    res = res * (0.78 + 0.38 * winter[di] + 0.35 * heat[di])
    irr_h = irr[di] * (0.92 + 0.10 * np.exp(-((hm - 14.0) / 4.0) ** 2))
    ind = np.where(wkend, 0.45, np.where((hm > 6.5) & (hm < 22.0), 1.0, 0.62))
    r = rng(3)
    out = outages()
    units = W.UNITS
    load = np.zeros((len(hu), len(units)))
    sub_load = {}
    plant = {"LST": plant_regimes(dlist, 41, shutdown=True), "DSL": plant_regimes(dlist, 42)}
    for code, _ in W.SUBSTATIONS:
        rs, ir, it, mva = SUB_MIX[code]
        ind_h = ind * (0.85 + 0.12 * plant[code][di]) if code in plant else ind
        s = rs * res / 0.80 + ir * irr_h / 0.45 + it * ind_h / 0.80
        s = s * mva / max(1e-9, s.mean())
        noise = np.exp(r.normal(0, 0.035, len(hu)))
        sub_load[code] = s * noise
    # split, honouring outages (the sister transformer carries the substation)
    loc_naive = loc.tz_localize(None).to_pydatetime()
    loc_naive = np.array(loc_naive, dtype="datetime64[s]")
    for code, _ in W.SUBSTATIONS:
        t1, t2 = f"{code}-T1", f"{code}-T2"
        i1, i2 = W.IDS.index(t1), W.IDS.index(t2)
        off1 = np.zeros(len(hu), bool)
        off2 = np.zeros(len(hu), bool)
        for tid, arr in ((t1, off1), (t2, off2)):
            for a, b, _ in out.get(tid, []):
                arr |= (loc_naive >= np.datetime64(a)) & (loc_naive < np.datetime64(b))
        both = ~off1 & ~off2
        load[:, i1] = np.where(both, sub_load[code] / 2, np.where(off1, 0.0, sub_load[code]))
        load[:, i2] = np.where(both, sub_load[code] / 2, np.where(off2, 0.0, sub_load[code]))
    # top oil: first-order response to the steady-state rise, tau 2.6 h
    rated = np.array([u["rating"][1] for u in units])
    off_amb = np.array([-1.8 if W.substation_of(u["id"]) in W.FOOTHILLS else 0.0 for u in units])
    unit_off = r.normal(0, 1.4, len(units))
    rise_r = np.array([47.0 if u["pres"] == "FB" else 50.0 for u in units]) + unit_off
    k = load / rated
    ss = rise_r * ((k ** 2 * 5.0 + 1.0) / 6.0) ** 0.8
    ss = np.where(load > 0, ss, 0.0)
    a = 1 - math.exp(-1 / 2.6)
    top = np.zeros_like(load)
    th = amb[0] + off_amb + ss[0]
    for t in range(len(hu)):
        tgt = amb[t] + off_amb + ss[t]
        th = th + (tgt - th) * a
        top[t] = th
    top = top + r.normal(0, 0.12, top.shape)
    return {"utc": hu, "local": loc, "ldate": ldate, "lhour": lhour - 0.5, "load": load, "top": top,
            "amb": amb, "irr": irr, "winter": winter, "plant": plant, "tmean": tmean}


# ---------------------------------------------------------------------------------------------
# tap operations per local day, and the SCADA counters at 00:00
def daily_ops(dlist, H):
    r = rng(4)
    n = len(dlist)
    out = outages()
    ops = np.zeros((n, len(W.UNITS)), dtype=np.int64)
    # daily load swing as a driver for ordinary units
    di = np.array([(x - W.START).days for x in H["ldate"]])
    for j, u in enumerate(W.UNITS):
        ld = H["load"][:, j]
        dmax = np.zeros(n)
        dmin = np.full(n, 1e9)
        np.maximum.at(dmax, di, ld)
        np.minimum.at(dmin, di, ld)
        swing = np.clip(dmax - dmin, 0, None)
        swing = swing / max(1e-9, np.mean(swing[swing > 0]))
        role = u["role"]
        code = W.substation_of(u["id"])
        if role == "L2":
            lam = 5.0 + 33.0 * H["plant"]["DSL"]
        elif role == "L1":
            lam = 4.0 + 31.0 * H["plant"]["LST"]
        elif role == "V":
            lam = 6.5 + 36.0 * H["irr"] / 0.8
        else:
            lam = u["ops"] * (0.55 + 0.45 * swing)
        lam = lam * np.clip(r.normal(1.0, 0.10, n), 0.6, 1.4)
        k = r.poisson(np.clip(lam, 0.1, None))
        # outages: the service day carries nothing; the evening before and the morning after part
        for a, b, kind in out.get(u["id"], []):
            for i, d in enumerate(dlist):
                s = dt.datetime.combine(d, dt.time(0, 0))
                e = s + ONE
                ov = (min(e, b) - max(s, a)).total_seconds()
                if ov > 0:
                    frac = 1 - ov / 86400.0
                    k[i] = int(round(k[i] * frac))
        ops[:, j] = k
    return ops


def counters(dlist, ops):
    """Counter value at 00:00 on each day. Five digits; replaced counters restart at zero."""
    n = len(dlist)
    cnt = np.zeros((n, len(W.UNITS)), dtype=np.int64)
    r = rng(5)
    for j, u in enumerate(W.UNITS):
        tid = u["id"]
        allsv = W.OLTC_SERVICES.get(tid, [])
        repl = {d for d, rp in allsv if rp and d >= W.START}
        pre_repl = [d for d, rp in allsv if rp and d < W.START]
        cum = np.concatenate([[0], np.cumsum(ops[:, j])])[:n]   # ops before day i
        if tid in W.ROLLOVER_AT_SERVICE:
            last = allsv[-1][0]
            assert not [d for d in repl if d < last], tid
            c0 = int((W.ROLLOVER_AT_SERVICE[tid] - cum[(last - W.START).days]) % W.COUNTER_MODULUS)
        elif pre_repl:
            rate = float(ops[:365, j].mean())
            c0 = int(round(rate * (W.START - max(pre_repl)).days))
        else:
            total = int(ops[:, j].sum())
            hi = max(500, W.COUNTER_MODULUS - total - 900)
            c0 = int(r.integers(300, max(301, min(hi, 60_000))))
        v = c0
        for i, d in enumerate(dlist):
            if i > 0:
                prev = dlist[i - 1]
                if prev in repl:
                    v = int(ops[i - 1, j])   # new counter from zero; nothing counted on a service day
                else:
                    v = (v + int(ops[i - 1, j])) % W.COUNTER_MODULUS
            cnt[i, j] = v
    return cnt
