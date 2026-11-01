"""The clean truth of the Kaitanga bore field: the aquifer, the plant's draw, every bore's take and level, the
new bore's commissioning test, and the summer plan. Nothing here is messy; pack.py applies the record keeping."""
import math

import numpy as np
import pandas as pd

import params as P

IDS = [b[0] for b in P.BORES]
ALL = IDS + ["PB9"]


def bore_table():
    rows = list(P.BORES) + [P.PB9]
    t = pd.DataFrame(rows, columns=["id", "x", "y", "ground", "stick", "own", "offset", "share", "cap", "kw"])
    t["mp_rl"] = t["ground"] + t["stick"]
    t["intake_mbmp"] = t["id"].map(P.INTAKE_MBMP)
    t["mol_mbmp"] = t["id"].map(P.MOL_MBMP)
    return t.set_index("id")


def interference(bt, rng):
    """Symmetric drawdown on bore i per ML/d taken at bore j (m)."""
    a = pd.DataFrame(0.0, index=ALL, columns=ALL)
    for i in ALL:
        for j in ALL:
            if i >= j:
                continue
            r = math.hypot(bt.at[i, "x"] - bt.at[j, "x"], bt.at[i, "y"] - bt.at[j, "y"])
            v = P.INTERF_K * math.log(P.INTERF_R / r) if r < P.INTERF_R else 0.0
            v *= math.exp(rng.normal(0, P.PAIR_SPREAD))
            if j == "PB9" and i in P.PB9_PAIR:
                v = P.PB9_PAIR[i]
            if i == "PB9" and j in P.PB9_PAIR:
                v = P.PB9_PAIR[j]
            a.at[i, j] = a.at[j, i] = round(v, 4)
    return a


def monitoring_bore(days, rng):
    """Council monitoring bore level, m RL NZVD2016: a seasonal cycle, a summer recession that differs year to
    year, and slow noise. 2019-20 is the deepest summer in the record."""
    doy = days.dayofyear.values
    season = P.MB_SEASON_AMP * np.cos(2 * np.pi * (doy - 258) / 365.25)
    summer_depth = {2014: 0.42, 2015: 0.18, 2016: 0.55, 2017: -0.21, 2018: 0.30, 2019: 1.62, 2020: 0.49,
                    2021: 0.12, 2022: -0.38, 2023: 0.61, 2024: 0.27, 2025: 0.36, 2026: 0.0}
    extra = np.zeros(len(days))
    for k, d in enumerate(days):
        # A summer that starts in year y draws the aquifer down from mid-November y to mid-July y+1, deepest
        # in the third week of March.
        y = d.year if d.month >= 7 else d.year - 1
        depth = summer_depth.get(y, 0.3)
        t0 = pd.Timestamp(y, 11, 15)
        u = (d - t0).days
        if 0 <= u <= 244:
            extra[k] = -depth * math.sin(math.pi * u / 244.0) ** 1.6
    noise = np.zeros(len(days))
    e = rng.normal(0, 0.022, len(days))
    for k in range(1, len(days)):
        noise[k] = 0.985 * noise[k - 1] + e[k]
    return P.MB_MEAN + season + extra + noise


def plant_draw(days, rng):
    """The milk powder site's daily draw on the bore field, ML/d."""
    out = np.zeros(len(days))
    for k, d in enumerate(days):
        m = d.month
        base = {1: 20.6, 2: 20.0, 3: 19.1, 4: 16.8, 5: 12.9, 6: 5.6, 7: 6.4, 8: 15.2, 9: 20.4, 10: 22.3,
                11: 22.5, 12: 21.6}[m]
        growth = 1 + 0.006 * (d.year - 2014)
        out[k] = base * growth * (1 + rng.normal(0, 0.025))
    return out


def outages(days, rng):
    """Days each bore is off for maintenance, mostly in the winter shutdown."""
    off = {i: np.zeros(len(days), dtype=bool) for i in IDS}
    for i in IDS:
        for y in range(2014, 2027):
            for _ in range(rng.poisson(2.6)):
                winter = rng.random() < 0.6
                if winter:
                    start = pd.Timestamp(y, 6, 1) + pd.Timedelta(days=int(rng.integers(0, 60)))
                else:
                    start = pd.Timestamp(y, 1, 1) + pd.Timedelta(days=int(rng.integers(0, 365)))
                n = int(rng.integers(2, 13))
                mask = (days >= start) & (days < start + pd.Timedelta(days=n))
                off[i] |= np.asarray(mask)
    return off


def allocate(draw, avail, bt, rng):
    """Split one day's draw across the bores in service, each near its share, none above its pump."""
    w = np.array([bt.at[i, "share"] * (1 + rng.normal(0, 0.045)) if avail[k] else 0.0 for k, i in enumerate(IDS)])
    cap = np.array([bt.at[i, "cap"] for i in IDS])
    q = np.zeros(len(IDS))
    rem = draw
    free = w > 0
    for _ in range(6):
        if rem <= 1e-9 or not free.any():
            break
        share = np.where(free, w, 0) / np.where(free, w, 0).sum()
        add = rem * share
        q = q + add
        over = q > cap
        rem = float((q - cap)[over].sum())
        q = np.minimum(q, cap)
        free = free & ~over
    return q


def simulate():
    rng = np.random.default_rng(P.SEED)
    bt = bore_table()
    a = interference(bt, rng)
    days = pd.date_range(P.START, P.END, freq="D")
    mb = monitoring_bore(days, rng)
    draw = plant_draw(days, rng)
    off = outages(days, rng)
    q = np.zeros((len(days), len(IDS)))
    for k in range(len(days)):
        avail = [not off[i][k] for i in IDS]
        q[k] = allocate(draw[k], avail, bt, rng)
    q = np.round(q, 4)
    takes = pd.DataFrame(q, index=days, columns=IDS)
    takes["PB9"] = 0.0
    test_hourly = commissioning_test(bt, rng)
    q9_local = test_hourly.set_index("local").discharge_ls.resample("D").sum() * 3600 / 1e6  # ML per local day
    for d, v in q9_local.items():
        if d in takes.index:
            takes.at[d, "PB9"] = round(float(v), 4)
    # Levels: m RL on the Moturiki datum, each bore's natural head less its own and its neighbours' drawdown.
    mb_mot = mb + P.MB_DATUM_OFFSET
    lev = {}
    for i in ALL:
        own = bt.at[i, "own"] * takes[i].values
        nb = sum(a.at[i, j] * takes[j].values for j in ALL if j != i)
        lev[i] = mb_mot + bt.at[i, "offset"] - own - nb + rng.normal(0, P.LEVEL_NOISE, len(days))
    levels = pd.DataFrame(lev, index=days)
    return {"bt": bt, "a": a, "days": days, "mb": pd.Series(mb, index=days), "draw": pd.Series(draw, index=days),
            "takes": takes, "levels": levels, "off": off, "test": test_hourly, "rng": rng}


def commissioning_test(bt, rng):
    """PB9's hourly record, local time: a three-step test on 6 October and a seven-day constant-rate test."""
    t0 = pd.Timestamp(P.TEST_STEP_DAY) + pd.Timedelta(hours=8)
    t1 = pd.Timestamp(P.TEST_CR_END) + pd.Timedelta(hours=24)
    hours = pd.date_range(t0, t1, freq="h")
    q = np.zeros(len(hours))
    phase = np.array(["static"] * len(hours), dtype=object)
    for k, h in enumerate(hours):
        step_t = (h - pd.Timestamp(P.TEST_STEP_DAY)).total_seconds() / 3600
        if 0 <= step_t - 9 < 6 and h.date() == pd.Timestamp(P.TEST_STEP_DAY).date():
            s = int((step_t - 9) // 2)
            q[k] = P.TEST_STEPS_LS[s] * (1 + rng.normal(0, 0.006))
            phase[k] = "step %d" % (s + 1)
        elif pd.Timestamp(P.TEST_CR_START) <= h < pd.Timestamp(P.TEST_CR_END):
            q[k] = P.TEST_CR_LS * (1 + rng.normal(0, 0.004))
            phase[k] = "constant rate"
        elif pd.Timestamp(P.TEST_CR_END) <= h:
            phase[k] = "recovery"
        elif h.date() == pd.Timestamp(P.TEST_STEP_DAY).date() and step_t >= 15:
            phase[k] = "recovery"
    return pd.DataFrame({"local": hours, "phase": phase, "discharge_ls": np.round(q, 2)})


def test_levels(w):
    """PB9's hourly level during the test, m RL Moturiki: its natural head on the day less the neighbours' takes
    that day and its own drawdown, which approaches the steady cone within a few hours in these gravels."""
    bt, a, takes, mb = w["bt"], w["a"], w["takes"], w["mb"]
    t = w["test"].copy()
    rng = np.random.default_rng(P.SEED + 9)
    out, dd = [], 0.0
    lam = 1 - math.exp(-1 / 1.6)
    for _, r in t.iterrows():
        d = r.local.normalize()
        head = mb.get(d, mb.iloc[-1]) + P.MB_DATUM_OFFSET + bt.at["PB9", "offset"]
        nb = sum(a.at["PB9", j] * takes.at[d, j] for j in IDS) if d in takes.index else 0.0
        target = bt.at["PB9", "own"] * r.discharge_ls * 86400 / 1e6
        dd = dd + (target - dd) * lam
        out.append(head - nb - dd + rng.normal(0, 0.012))
    t["level_rl"] = out
    return t
