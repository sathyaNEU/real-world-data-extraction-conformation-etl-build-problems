"""The clean truth: districts, transformers, premises, the plug-in vehicle fleet to 30 September 2026, the premises'
rate schedules, the three summers' 4 to 9 pm loads and each transformer's recorded peak.

Every quantity here is the world before any extract is written or any mess applied. The summers are simulated at the
quarter hour for every transformer: the premises' evening load (air conditioning saturates above 105 F, so a heat
wave holds the evening load on a plateau) plus every vehicle present that day charging the way its owner charges under
the premise's rate. The recorded peak is the highest quarter hour ending after 16:00 and at or before 21:00."""
from __future__ import annotations

import datetime as dt

import numpy as np
import pandas as pd

import common as K


def district_params(name):
    return next(d for d in K.DISTRICTS if d[0] == name)


# ------------------------------------------------------------------------------------------------- weather
def temperatures(di, year):
    """Daily maximum temperature (F) at the district's station, 1 June to 30 September."""
    r = K.rng("wx", di, year)
    day = np.arange(K.NDAY)
    tt = 93.5 + 7.5 * np.sin(np.pi * (day + 12) / 140) + K.DISTRICTS[di][11]
    ar = np.zeros(K.NDAY)
    for i in range(1, K.NDAY):
        ar[i] = 0.72 * ar[i - 1] + r.normal(0, 2.3)
    tt = tt + ar
    start, length = K.HEAT[year]
    s = (start - K.summer_start(year)).days
    tt[s:s + length] = np.maximum(tt[s:s + length], 107.5 + 0.3 * K.DISTRICTS[di][11] + r.normal(0, 1.0, length))
    return np.round(tt, 0)


def load_factor(tt):
    return np.clip((tt - 62.0) / (105.0 - 62.0), 0.18, 1.0)


SHAPE = 0.70 + 0.30 * np.clip((K.QMID - 15.6) / 1.6, 0, 1) * (1 - 0.10 * np.clip((K.QMID - 20.4) / 0.6, 0, 1))


# ------------------------------------------------------------------------------------------------- the network
PREV_SIZE = {15.0: 10.0, 25.0: 15.0, 37.5: 25.0, 50.0: 37.5, 75.0: 50.0, 100.0: 75.0}
SEASONAL = {"Foothill": (0.40, (0.86, 0.09), (0.46, 0.10))}


def transformers():
    rows = []
    for di, d in enumerate(K.DISTRICTS):
        name, code, ntx, mix, (lm, ls) = d[0], d[1], d[2], d[3], d[4]
        r = K.rng("tx", di)
        kva = r.choice(np.array(K.SIZES), p=np.array(mix) / sum(mix), size=ntx)
        npm = np.array([r.integers(K.PREM[s][0], K.PREM[s][1] + 1) for s in kva])
        ratio = np.clip(r.normal(lm, ls, ntx), 0.25, 1.40)
        if name in SEASONAL:
            # foothill pole-tops serve either year-round homes with central air or seasonal cabins with little
            share, (m1, s1), (m2, s2) = SEASONAL[name]
            cabin = r.random(ntx) < share
            ratio = np.where(cabin, np.clip(r.normal(m2, s2, ntx), 0.25, 1.40), np.clip(r.normal(m1, s1, ntx), 0.25, 1.40))
        nfeed = max(8, ntx // 260)
        feeder = r.integers(0, nfeed, ntx)
        pad_p = {"Crestview": .85, "Lakeside": .80, "Highland": .75, "Sunrise": .65}.get(name, .12)
        mount = np.where((kva >= 50) | (r.random(ntx) < pad_p * (kva >= 25)), "PAD", "OH")
        for j in range(ntx):
            rows.append((name, di, code, float(kva[j]), int(npm[j]), float(ratio[j]), int(feeder[j]), mount[j]))
    tx = pd.DataFrame(rows, columns=["district", "di", "code", "kva", "n_prem", "ratio", "feeder", "mount"])
    tx["ti"] = np.arange(len(tx))
    tx["plateau"] = tx["ratio"] * tx["kva"] * K.PF                  # kW, the saturated evening plateau
    tx["sig"] = 0.18 * np.sqrt(tx["n_prem"])                         # kW, other-load noise on the summed premises
    tx["sg"] = tx["kva"].map(K.SIZE_GROUP)
    # GIS location numbers: one block per mapping region, assigned as the map was digitised (not by district)
    r = K.rng("loc")
    tx["loc"] = 2100000 + np.sort(r.choice(np.arange(10000, 899999), size=len(tx), replace=False))[r.permutation(len(tx))]
    # laterals: transformers on one fused tap of a feeder (overhead) or one loop (pad-mounted)
    lat = np.zeros(len(tx), int)
    nxt = 0
    for (di, fd, mt), g in tx.groupby(["di", "feeder", "mount"], sort=True):
        idx = g.index.values
        j = 0
        while j < len(idx):
            k = int(r.integers(3, 9)) if mt == "PAD" else int(r.integers(1, 7))
            lat[idx[j:j + k]] = nxt
            nxt += 1
            j += k
    tx["lateral"] = lat
    # GIS as-built errors: in the pilot districts a few units were recorded one standard size below the unit on the
    # pole; their recorded loading reads far above any real unit's, so the pilot's screen put them at the top
    tx["kva_gis0"] = tx["kva"]
    r = K.rng("gis-errors")
    for name in K.PILOT_DISTRICTS:
        sub = tx[(tx.district == name) & tx.kva.isin(list(PREV_SIZE))]
        hot = sub[(sub.ratio * sub.kva / sub.kva.map(PREV_SIZE)) > 1.45]
        n = int(r.integers(4, 9))
        pick = r.choice(hot.index.values, size=min(n, len(hot)), replace=False)
        tx.loc[pick, "kva_gis0"] = tx.loc[pick, "kva"].map(PREV_SIZE)
    tx["gis_err"] = tx["kva_gis0"] != tx["kva"]
    return tx


def premises(tx):
    pr = tx.loc[tx.index.repeat(tx["n_prem"]), ["ti", "di", "district"]].reset_index(drop=True)
    pr["pi"] = np.arange(len(pr))
    r = K.rng("premise-rates")
    care = np.array([K.DISTRICTS[d][14] for d in pr["di"]])
    u = r.random(len(pr))
    pr["base_rate"] = np.where(u < care, K.RATE_CARE, np.where(u > 0.985, K.RATE_FLAT, K.RATE_TOU))
    return pr


# ------------------------------------------------------------------------------------------------- the fleet
def fleet(tx, pr):
    """Vehicles registered 2 January 2018 to 30 September 2026 with their departures, and each premise's move to the
    EV rate when its first vehicle arrives (dated within three weeks either side of the registration)."""
    veh, ev_switch = [], {}
    base = pd.Timestamp(K.FLEET_START)
    mid24, end26 = pd.Timestamp("2024-06-01"), pd.Timestamp("2026-09-30")
    for di, d in enumerate(K.DISTRICTS):
        r = K.rng("fleet", di)
        sub = pr[pr.di == di]
        pis, tis, rates = sub["pi"].values, sub["ti"].values, sub["base_rate"].values
        cnt = np.zeros(len(tx))
        n_pre, n_hist = int(d[5] * len(sub)), int(d[6] * len(sub) * 2.33)
        days = np.concatenate([np.sort(r.integers(0, (mid24 - base).days, n_pre)),
                               (mid24 - base).days + np.sort(r.integers(0, (end26 - mid24).days + 1, n_hist))])
        for dd in days:
            w = 1.0 + d[7] * cnt[tis]
            j = r.choice(len(sub), p=w / w.sum())
            pi, ti = int(pis[j]), int(tis[j])
            cnt[ti] += 1
            reg = base + pd.Timedelta(days=int(dd))
            if pi not in ev_switch:
                ev_switch[pi] = (reg + pd.Timedelta(days=int(r.integers(-20, 11)))) \
                    if (rates[j] != K.RATE_FLAT and r.random() < d[8]) else None
            veh.append((pi, ti, di, reg))
    v = pd.DataFrame(veh, columns=["pi", "ti", "di", "reg"])
    r = K.rng("departures")
    rate_dep = np.array([K.DISTRICTS[d][13] for d in v["di"]])
    life = pd.to_timedelta((r.exponential(1.0, len(v)) / rate_dep * 365.25).astype(int), unit="D")
    dep = v["reg"] + life
    v["dep"] = pd.NaT
    v.loc[dep <= end26, "dep"] = dep[dep <= end26]
    v["phase"] = "hist"
    v = attributes(v, "hist")
    sw = {k: x for k, x in ev_switch.items() if x is not None}
    return v, sw


def attributes(v, key):
    r = K.rng("attr", key)
    n = len(v)
    bev = r.random(n) < 0.80
    v["fuel"] = np.where(bev, "BEV", "PHEV")
    v["P"] = np.where(bev, r.choice([1.4, 7.2, 9.6, 11.5], p=[.15, .60, .15, .10], size=n),
                      r.choice([1.4, 3.3], p=[.3, .7], size=n))
    v["q"] = np.where(bev, 0.50, 0.80)
    v["emean"] = np.where(bev, 10.0, 6.0)
    v["u_beh"] = r.random(n)
    return v


def rate_on(pr_base, sw, pi, day):
    s = sw.get(pi)
    if s is not None and s <= pd.Timestamp(day):
        return K.RATE_EV
    return pr_base[pi]


# ------------------------------------------------------------------------------------------------- summers
WEEKEND_OR_HOLIDAY = {dt.date(2024, 7, 4), dt.date(2024, 9, 2), dt.date(2025, 7, 4), dt.date(2025, 9, 1),
                      dt.date(2026, 7, 3), dt.date(2026, 9, 7)}


def off_day(year, i):
    d = K.day_of(year, i)
    return d.weekday() >= 5 or d in WEEKEND_OR_HOLIDAY


def simulate_district(tx, veh, sw, pr_base, di, year):
    """Recorded peak (kVA), its day index and quarter hour for every transformer in one district and summer."""
    txd = tx[tx.di == di]
    idx = txd["ti"].values
    loc = {t: i for i, t in enumerate(idx)}
    n = len(txd)
    r = K.rng("base", di, year)
    lf = load_factor(temperatures(di, year))
    z = r.standard_normal((n, K.NDAY, K.T)).astype(np.float32)
    e = np.empty_like(z)
    e[..., 0] = z[..., 0]
    for t in range(1, K.T):
        e[..., t] = 0.6 * e[..., t - 1] + 0.8 * z[..., t]
    load = (txd["plateau"].values[:, None, None] * lf[None, :, None] * SHAPE[None, None, :]).astype(np.float32)
    load += txd["sig"].values[:, None, None].astype(np.float32) * e
    ys = pd.Timestamp(K.summer_start(year))
    off = np.array([off_day(year, i) for i in range(K.NDAY)])
    rr = K.rng("charge", di, year)
    vd = veh[(veh.di == di) & (veh.reg <= pd.Timestamp("%d-09-30" % year))]
    for v in vd.itertuples():
        d0 = max(0, (v.reg - ys).days)
        d1 = K.NDAY if pd.isna(v.dep) else min(K.NDAY, (v.dep - ys).days)
        nd = max(0, d1 - d0)
        # every vehicle draws the same number of numbers whatever its dates inside this summer's window, so moving
        # one vehicle never re-rolls another
        u_slip = rr.random(K.NDAY); u_ch = rr.random(K.NDAY)
        st_w = rr.normal(17.6, 1.0, K.NDAY); st_o = rr.normal(15.8, 2.4, K.NDAY)
        en = np.clip(rr.gamma(4.0, v.emean / 4.0, K.NDAY), 1.0, 45.0)
        if nd <= 0:
            continue
        days = np.arange(d0, d1)
        s = sw.get(v.pi)
        ev2 = np.zeros(nd, bool) if s is None else (ys + pd.to_timedelta(days, unit="D") >= s)
        if pr_base[v.pi] == K.RATE_FLAT:
            ev2[:] = False
        pa = np.where(ev2, K.BEH["EV"][0], K.BEH["TOU"][0])
        pt = np.where(ev2, K.BEH["EV"][1], K.BEH["TOU"][1])
        slip = np.where(ev2, K.SLIP["EV"], K.SLIP["TOU"])
        beh = np.where(v.u_beh < pa, 0, np.where(v.u_beh < pa + pt, 1, 2))
        beh = np.where((beh > 0) & (u_slip[days] < slip), 0, beh)
        charges = u_ch[days] < v.q
        start = np.where(beh == 0, np.where(off[days], st_o[days], st_w[days]), np.where(beh == 1, 21.0, 24.0))
        end = start + en[days] / v.P
        ov = np.clip(np.minimum(end[:, None], K.QSTART + 0.25) - np.maximum(start[:, None], K.QSTART), 0, 0.25) / 0.25
        load[loc[v.ti], d0:d1, :] += (ov * v.P * charges[:, None]).astype(np.float32)
    flat = load.reshape(n, -1)
    k = flat.argmax(axis=1)
    pk = flat[np.arange(n), k] / K.PF
    return idx, pk.astype(np.float64), (k // K.T).astype(int), (k % K.T).astype(int)


def simulate(tx, veh, sw, pr_base, years=K.SUMMERS, districts=None):
    for year in years:
        for di in (range(len(K.DISTRICTS)) if districts is None else districts):
            idx, pk, dd, qq = simulate_district(tx, veh, sw, pr_base, di, year)
            tx.loc[idx, "pk%d" % year] = pk
            tx.loc[idx, "pkday%d" % year] = dd
            tx.loc[idx, "pkq%d" % year] = qq
    return tx


def peak_date(tx, year):
    return pd.Timestamp(K.summer_start(year)) + pd.to_timedelta(tx["pkday%d" % year].astype(int), unit="D")


# ------------------------------------------------------------------------------------------------- unit changes
NEXT_SIZE = {10.0: 15.0, 15.0: 25.0, 25.0: 50.0, 37.5: 50.0, 50.0: 75.0, 75.0: 100.0, 100.0: 167.0}


SUBSTITUTE = {(25.0, 50.0): 37.5, (15.0, 25.0): 37.5, (10.0, 15.0): 25.0, (37.5, 50.0): 75.0, (50.0, 75.0): 100.0}
PILOT_TARGET = {"Railyard": 94, "Canal": 81, "Brookside": 88}


def pilot(tx):
    """The 2025-26 pilot: in each pilot district the screen listed every transformer whose 2025 recorded peak exceeded
    1.15 times its GIS rating, most loaded first, and the program issued work down the list until the district's
    replacements were done, between 6 October 2025 and 24 April 2026. A unit the crew found already larger than GIS
    said was left in place and the record corrected; a few orders were cancelled; a crew working a feeder took a
    second listed unit on the same feeder under one order; and a few units went in a size other than the planned.

    Returns the physical replacements, the work orders and the record corrections."""
    repl, wos, corr = [], [], []
    for name in K.PILOT_DISTRICTS:
        di = K.NAMES.index(name)
        r = K.rng("pilot", di)
        sub = tx[(tx.district == name)]
        load = sub["pk2025"] / sub["kva_gis0"]
        cand = sub[load > 1.15].assign(load=load).sort_values("load", ascending=False)
        n_target = PILOT_TARGET[name]
        listed = []
        for i, row in cand.iterrows():
            if sum(1 for x in listed if x[1] == "REPL") >= n_target:
                break
            if row.gis_err:
                listed.append((int(row.ti), "NOWORK"))
            elif r.random() < 0.035:
                listed.append((int(row.ti), "CANC"))
            else:
                listed.append((int(row.ti), "REPL"))
        # second units taken under one order: a later listed unit on the same feeder
        firsts, seconds = {}, set()
        feeder = dict(zip(tx["ti"], tx["feeder"]))
        nb = int(r.integers(5, 10))
        reps = [t for t, k in listed if k == "REPL"]
        for a in reps:
            if len(firsts) >= nb:
                break
            if a in seconds or a in firsts:
                continue
            mates = [b for b in reps if b != a and b not in seconds and b not in firsts and feeder[b] == feeder[a]
                     and reps.index(b) > reps.index(a)]
            if mates and r.random() < 0.45:
                firsts[a] = mates[0]
                seconds.add(mates[0])
        orders = [(t, k) for t, k in listed if t not in seconds]
        span = (K.PILOT_END - K.PILOT_START).days
        days = np.sort(r.integers(0, span + 1, len(orders)))
        # the list is worked roughly in order, crews clustering by feeder: a little shuffle
        days = days[np.argsort(np.arange(len(orders)) + r.normal(0, 6, len(orders)))]
        for (t, k), dd in zip(orders, days):
            d = K.PILOT_START + dt.timedelta(days=int(dd))
            while d.weekday() >= 5:
                d += dt.timedelta(days=1)
            row = tx.loc[t]
            plan_from = float(row.kva_gis0)
            plan_to = NEXT_SIZE[plan_from]
            if k == "REPL":
                for u in ([t] + ([firsts[t]] if t in firsts else [])):
                    ru = tx.loc[u]
                    planned = NEXT_SIZE[float(ru.kva_gis0)]
                    inst = SUBSTITUTE.get((float(ru.kva_gis0), planned)) if r.random() < 0.07 else None
                    repl.append((u, name, d, float(ru.kva), inst if inst else planned, t, u != t))
            elif k == "NOWORK":
                corr.append((t, name, d, plan_from, float(row.kva), t))
            wos.append((t, name, d, plan_from, plan_to, k, firsts.get(t, -1)))
    R = pd.DataFrame(repl, columns=["ti", "district", "date", "kva_old", "kva_new", "wo_ti", "second"])
    WO = pd.DataFrame(wos, columns=["ti", "district", "date", "plan_from", "plan_to", "kind", "second_ti"])
    C = pd.DataFrame(corr, columns=["ti", "district", "date", "kva_from", "kva_to", "wo_ti"])
    return R, WO, C


def failures(tx):
    """Units that failed in service between 1 June and 30 September 2026, most of them overloaded in the September
    heat wave, each replaced by the next size up; on a transformer's own peak day a failure comes after its recorded
    peak quarter hour. Also the units that failed in a late-May hot spell, before the summer window."""
    r = K.rng("failures")
    load = tx["pk2026"] / tx["kva_mid"]
    p = np.where(load > 1.30, 0.10, np.where(load > 1.20, 0.035, 0.0025))
    fail = r.random(len(tx)) < p
    pkd = peak_date(tx, 2026)
    rows = []
    for i in np.where(fail)[0]:
        row = tx.iloc[i]
        hot = bool(load.iloc[i] > 1.20)
        if hot:
            start = K.HEAT[2026][0]
            d = start + dt.timedelta(days=int(r.integers(0, K.HEAT[2026][1] + 3)))
            hour = float(np.clip(r.normal(18.4, 1.6), 12.0, 23.5))
        else:
            d = K.summer_start(2026) + dt.timedelta(days=int(r.integers(0, K.NDAY)))
            hour = float(r.uniform(0, 24))
        pk_end = 16.25 + 0.25 * int(row.pkq2026)
        if d == pkd.iloc[i].date() and hour < pk_end:
            hour = pk_end + float(r.uniform(0.1, 1.5))
        rows.append((int(row.ti), row.district, d, round(hour, 4), float(row.kva_mid), NEXT_SIZE[float(row.kva_mid)], hot, True))
    # the late-May hot spell, and the last evening of the summer
    may = tx[(tx.pk2025 / tx.kva_mid > 1.25) & ~tx.ti.isin([x[0] for x in rows])]
    for t, day in zip(r.choice(may["ti"].values, size=3, replace=False), (30, 31, 31)):
        row = tx.loc[t]
        rows.append((int(t), row.district, dt.date(2026, 5, day), round(float(r.uniform(19.6, 22.8)), 4),
                     float(row.kva_mid), NEXT_SIZE[float(row.kva_mid)], False, False))
    late = tx[(tx.pk2026 / tx.kva_mid > 1.12) & ~tx.ti.isin([x[0] for x in rows])]
    for t, hour in zip(r.choice(late["ti"].values, size=2, replace=False), (18.6, 20.3)):
        row = tx.loc[t]
        rows.append((int(t), row.district, dt.date(2026, 9, 30), round(hour + float(r.uniform(0, 0.5)), 4),
                     float(row.kva_mid), NEXT_SIZE[float(row.kva_mid)], False, True))
    return pd.DataFrame(rows, columns=["ti", "district", "date", "hour", "kva_old", "kva_new", "hot", "in_window"])


def other_changes(tx):
    """The unit changes outside the pilot and the failures, 1 January 2024 to the pull: like-for-like condition
    replacements (leaking or rusted tanks), upsizes for customer load on lightly loaded units, and GIS record
    corrections found by field inspection outside the pilot districts (never on a unit near its rating)."""
    r = K.rng("other-changes")
    rows = []
    lo, hi = pd.Timestamp("2024-01-08"), pd.Timestamp(K.AS_OF) - pd.Timedelta(days=4)
    n = int(0.0042 * len(tx) * 3.25)
    for t in r.choice(tx["ti"].values, size=n, replace=False):
        d = lo + pd.Timedelta(days=int(r.integers(0, (hi - lo).days)))
        while d.weekday() >= 5:
            d += pd.Timedelta(days=1)
        k = float(tx.loc[t, "kva"])
        rows.append((int(t), d.date(), "MAINT", k, k))
    light = tx[(tx.pk2026 / tx.kva < 0.42) & (tx.kva >= 25) & (tx.kva <= 50)]
    for t in r.choice(light["ti"].values, size=22, replace=False):
        d = pd.Timestamp("2025-10-13") + pd.Timedelta(days=int(r.integers(0, 220)))
        while d.weekday() >= 5:
            d += pd.Timedelta(days=1)
        k = float(tx.loc[t, "kva"])
        rows.append((int(t), d.date(), "LOAD", k, NEXT_SIZE[k]))
    out_p = tx[~tx.district.isin(K.PILOT_DISTRICTS) & (tx.pk2024 / tx.kva < 0.40) & tx.kva.isin(list(PREV_SIZE))]
    for t in r.choice(out_p["ti"].values, size=14, replace=False):
        d = pd.Timestamp("2024-11-04") + pd.Timedelta(days=int(r.integers(0, 520)))
        while d.weekday() >= 5:
            d += pd.Timedelta(days=1)
        k = float(tx.loc[t, "kva"])
        rows.append((int(t), d.date(), "CORR", PREV_SIZE[k] if r.random() < 0.6 else NEXT_SIZE[k], k))
    out = pd.DataFrame(rows, columns=["ti", "date", "kind", "kva_from", "kva_to"])
    return out.drop_duplicates("ti", keep="first").sort_values(["date", "ti"]).reset_index(drop=True)
