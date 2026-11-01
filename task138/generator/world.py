"""The world's clean truth for task138 architecture 3: Breckwater Electric Cooperative's Dunraith substation.

Five summers of hourly feeder loads at the Dunraith substation (eight 24.9 kV feeders) driven by the Mossford
airport's temperatures: a load that follows the hour of day and air conditioning whose duty rises with the
temperature the buildings feel. In summer 2025 three feeders ran conservation voltage reduction week on, week off:
a 3.5 per cent voltage cut lowers the voltage-sensitive load by about its own share and air-conditioner compressors
(about constant power) hardly at all, so the cut's relief is largest at night and smallest on the hottest
afternoons. Also drawn here: the members' transformer meters (summer 2026), the wholesale supplier's revenue meters
at the substation (summer 2026), the July 2026 feeder reconfiguration, and the distractors.
"""
import math

import numpy as np
import pandas as pd

import params as PR

HOURS = 24


def summer_index(year):
    return pd.date_range("%d-06-01 00:00" % year, "%d-09-30 23:00" % year, freq="h")


# ------------------------------------------------------------------ weather
def weather():
    """Hourly air temperature at the Mossford airport (deg F, local time) for the five summers."""
    rng = np.random.default_rng(PR.WEATHER_SEED)
    frames = []
    for year in PR.SUMMERS:
        days = pd.date_range("%d-06-01" % year, "%d-10-01" % year, freq="D")
        n = len(days)
        d = np.arange(n)
        mean = 87.5 + 5.6 * np.sin(np.pi * (d + 12) / 138.0)
        an = np.zeros(n)
        for i in range(1, n):
            an[i] = 0.70 * an[i - 1] + rng.normal(0, 3.1)
        tx = mean + an
        if year == 2025:
            # the heat wave of late July and early August ran across a week with the voltage cut and the weeks
            # either side without it
            wave = np.asarray(((days >= pd.Timestamp("2025-07-24")) & (days <= pd.Timestamp("2025-08-06"))) |
                              ((days >= pd.Timestamp("2025-08-21")) & (days <= pd.Timestamp("2025-08-30"))))
            tx = np.where(wave, 100.4 + rng.normal(0, 0.9, n), tx - 1.0)
        tn = tx - 19.0 - rng.normal(0, 2.2, n)
        idx = summer_index(year)
        t = np.empty(len(idx))
        for k, ts in enumerate(idx):
            i = (ts.normalize() - days[0]).days
            h = ts.hour + ts.minute / 60.0
            if h < 6:
                prev_tx = tx[i - 1] if i > 0 else tx[i]
                frac = (h + 8) / 14.0
                t[k] = prev_tx - (prev_tx - tn[i]) * (1 - math.cos(math.pi * frac)) / 2
            elif h <= 16:
                t[k] = tn[i] + (tx[i] - tn[i]) * (1 - math.cos(math.pi * (h - 6) / 10.0)) / 2
            else:
                frac = (h - 16) / 14.0
                t[k] = tx[i] - (tx[i] - tn[i + 1]) * (1 - math.cos(math.pi * frac)) / 2
        t = t + rng.normal(0, 0.35, len(t))
        frames.append(pd.DataFrame({"local": idx, "temp_f": t}))
    return pd.concat(frames, ignore_index=True)


# ------------------------------------------------------------------ loads
OTHER_PROFILE = np.array([0.60, 0.56, 0.54, 0.53, 0.54, 0.58, 0.66, 0.74, 0.79, 0.82, 0.84, 0.85,
                          0.86, 0.88, 0.92, 0.96, 0.98, 0.99, 0.995, 1.00, 0.97, 0.89, 0.78, 0.68])
WEEKEND = 0.93


def other_load(ts):
    p = OTHER_PROFILE[ts.hour]
    return p * (WEEKEND if ts.dayofweek >= 5 else 1.0)


def duty(t_eff):
    return np.clip((t_eff - PR.DUTY_T0) / (PR.DUTY_T1 - PR.DUTY_T0), 0.0, 1.0) ** PR.DUTY_EXP


def pilot_schedule():
    """The pilot as the M&V plan set it: on weeks from 2 June 2025, alternating, switched at Monday 00:00."""
    start = pd.Timestamp(PR.PILOT_START)
    end = pd.Timestamp(PR.PILOT_END)
    out = []
    k = 0
    t = start
    while t <= end:
        out.append((t, "ON" if k % 2 == 0 else "OFF"))
        t = t + pd.Timedelta(days=7)
        k += 1
    if out[-1][1] == "ON":
        out.append((out[-1][0] + pd.Timedelta(days=7), "OFF"))
    return out


# switching as done: the controller's log differs from the plan in two places
LATE = {("DUN-7", "2025-07-14 00:00"): "2025-07-14 09:40"}
MISSED = {("DUN-5", "2025-09-08 00:00")}


def switching_log():
    rows = []
    for t, act in pilot_schedule():
        for f in PR.PILOT_FEEDERS:
            key = (f, t.strftime("%Y-%m-%d %H:%M"))
            if key in MISSED:
                continue
            when = pd.Timestamp(LATE[key]) if key in LATE else t
            rows.append({"feeder": f, "local": when, "action": act})
    return pd.DataFrame(rows).sort_values(["local", "feeder"]).reset_index(drop=True)


def cvr_state(log, feeder, idx):
    """Whether the feeder ran the voltage cut at each hour (the log's actual switching)."""
    ev = log[log.feeder == feeder].sort_values("local")
    state = np.zeros(len(idx), bool)
    cur = False
    j = 0
    times = list(ev["local"])
    acts = list(ev["action"])
    for k, ts in enumerate(idx):
        while j < len(times) and times[j] <= ts:
            cur = acts[j] == "ON"
            j += 1
        state[k] = cur
    return state


def cvr_relief(other, ac):
    """Share of a feeder's load the 3.5 per cent voltage cut removes in an hour."""
    return PR.CVR_DV * (PR.CVR_OTHER * other + PR.CVR_AC * ac) / (other + ac)


# the July 2026 reconfiguration: whole transformer groups moved between feeders (share of the substation's load)
RECONFIG_DATE = pd.Timestamp("2026-07-01 00:00")
RECONFIG = [("DUN-4", "DUN-8", 0.0215), ("DUN-1", "DUN-3", 0.0128), ("DUN-6", "DUN-2", 0.0102)]


def feeder_shares(ts):
    sh = dict(zip(PR.FEEDERS, PR.SHARE))
    if ts >= RECONFIG_DATE:
        for a, b, s in RECONFIG:
            sh[a] -= s
            sh[b] += s
    return sh


def loads(wx):
    """Hourly feeder loads (MW, local time) for the five summers, with the 2025 pilot's voltage cut as switched."""
    rng = np.random.default_rng(PR.LOAD_SEED)
    log = switching_log()
    out = []
    for year in PR.SUMMERS:
        idx = summer_index(year)
        t = wx.set_index("local").loc[idx, "temp_f"].values
        t1 = np.concatenate([[t[0]], t[:-1]])
        t3 = np.concatenate([[t[0]] * 3, t[:-3]])
        t_eff = 0.6 * t1 + 0.4 * t3
        g = (1 + PR.GROWTH) ** (year - 2024)
        other = np.array([other_load(ts) for ts in idx]) * PR.OTHER_PEAK * g
        d = duty(t_eff)
        states = {f: (cvr_state(log, f, idx) if year == 2025 else np.zeros(len(idx), bool)) for f in PR.FEEDERS}
        shares = [feeder_shares(ts) for ts in idx]
        for fi, f in enumerate(PR.FEEDERS):
            sh = np.array([s[f] for s in shares])
            o = other * sh
            a = PR.AC_FULL * g * d * sh * PR.AC_WEIGHT[fi]
            # the load that does not follow the weather wanders more from hour to hour than air conditioning,
            # which thousands of thermostats smooth
            sd = PR.LOAD_NOISE * o / (o + a) + 0.0005
            mw = (o + a) * (1 + rng.normal(0, 1.0, len(idx)) * sd)
            on = states[f]
            mw = np.where(on, mw * (1 - cvr_relief(o, a)), mw)
            out.append(pd.DataFrame({"local": idx, "feeder": f, "mw": mw, "other": o, "ac": a, "cvr": on}))
    return pd.concat(out, ignore_index=True), log


def truth_relief_at_design():
    """The voltage cut's relief at the planning peak: the substation's evening peak hour (18:00) on a weekday whose
    afternoon reaches the design temperature, the buildings feeling the afternoon's heat about two hours late."""
    t_eff = PR.DESIGN_TEMP_F - 0.35
    o = PR.OTHER_PEAK * OTHER_PROFILE[18]
    a = PR.AC_FULL * float(duty(t_eff)) * sum(s * w for s, w in zip(PR.SHARE, PR.AC_WEIGHT))
    return cvr_relief(o, a)


# ------------------------------------------------------------------ members' meters (summer 2026)
def transformers():
    """The distribution transformers behind each feeder (as built), with the large-power services whose meters
    register through current transformers (multiplier 20) and the groups the July 2026 reconfiguration moved."""
    rng = np.random.default_rng(PR.MDMS_SEED)
    rows = []
    base = {"DUN-1": 61, "DUN-2": 49, "DUN-3": 55, "DUN-4": 44, "DUN-5": 58, "DUN-6": 38, "DUN-7": 51, "DUN-8": 47}
    serial = 40112
    for f in PR.FEEDERS:
        for k in range(base[f]):
            serial += int(rng.integers(3, 29))
            rows.append({"tx": "T%06d" % serial, "feeder_built": f, "kva": int(rng.choice([25, 50, 75, 100, 167])),
                         "mult": 1})
    df = pd.DataFrame(rows)
    # large-power services (grain dryers, irrigation pump stations, a cold store)
    big = rng.choice(len(df), 14, replace=False)
    df.loc[big, "mult"] = 20
    df.loc[big, "kva"] = 500
    # the reconfiguration's moved groups (current feeder after 1 July 2026)
    df["feeder_now"] = df["feeder_built"]
    moved = []
    for a, b, s in RECONFIG:
        cand = df[(df.feeder_built == a) & (df.mult == 1)].index.values
        n = {"DUN-4": 9, "DUN-1": 6, "DUN-6": 5}[a]
        pick = rng.choice(cand, n, replace=False)
        df.loc[pick, "feeder_now"] = b
        moved += list(pick)
    df["moved"] = False
    df.loc[moved, "moved"] = True
    # weights: each transformer's share of its feeder's member energy
    w = rng.gamma(2.0, 1.0, len(df)) * df["kva"].values ** 0.6
    df["w"] = w
    return df


def mdms(ld, tx):
    """Members' daily energy by transformer (kWh as the meter data system holds it), summer 2026. Each feeder's
    energy at the members' meters is its SCADA energy less 2.6 per cent losses; a moved group carries its share of
    its old feeder's energy before 1 July and of its new feeder's after. A large-power service's meter registers
    through current transformers, so the system holds its kWh divided by the multiplier."""
    rng = np.random.default_rng(PR.MDMS_SEED + 1)
    s26 = ld[ld.local.dt.year == 2026].copy()
    s26["date"] = s26.local.dt.normalize()
    daily = s26.groupby(["date", "feeder"])["mw"].sum().unstack() * 1000.0 * 0.974
    share = dict(zip(PR.FEEDERS, PR.SHARE))
    rows = []
    for date, r in daily.iterrows():
        after = date >= RECONFIG_DATE.normalize()
        for f in PR.FEEDERS:
            e = float(r[f])
            if not after:
                out = [g for g in RECONFIG if g[0] == f]
                if out:
                    a, b, s = out[0]
                    moved = tx[(tx.feeder_built == f) & tx.moved]
                    stay = tx[(tx.feeder_built == f) & ~tx.moved]
                    rows += _spread(moved, e * s / share[f], rng, date)
                    rows += _spread(stay, e * (1 - s / share[f]), rng, date)
                else:
                    rows += _spread(tx[tx.feeder_built == f], e, rng, date)
            else:
                into = [g for g in RECONFIG if g[1] == f]
                stay = tx[(tx.feeder_now == f) & ~tx.moved]
                if into:
                    a, b, s = into[0]
                    moved = tx[(tx.feeder_built == a) & tx.moved]
                    frac = s / (share[f] + s)
                    rows += _spread(moved, e * frac, rng, date)
                    rows += _spread(stay, e * (1 - frac), rng, date)
                else:
                    rows += _spread(stay, e, rng, date)
    return pd.DataFrame(rows, columns=["tx", "date", "kwh_held"])


def _spread(members, e, rng, date):
    w = members["w"].values * (1 + rng.normal(0, 0.06, len(members)))
    w = np.maximum(w, 1e-6)
    kwh = e * w / w.sum()
    return [(t, date, k / m) for t, k, m in zip(members["tx"].values, kwh, members["mult"].values)]


# ------------------------------------------------------------------ the wholesale supplier's revenue meters (2026)
GT_METERS = [("41-2207", "T1"), ("41-2208", "T2"), ("41-2391", "GRAIN")]


def revenue_meters(ld, rng=None):
    """15-minute energy at the substation's two transformers (low side) and at the grain terminal served straight
    from the 69 kV bus, summer 2026, interval ending, UTC. The transformers carry the feeders' load plus 0.8 per cent
    losses, split 52/48; the grain terminal runs its dryers in long blocks."""
    rng = np.random.default_rng(PR.GT_SEED)
    s26 = ld[ld.local.dt.year == 2026].groupby("local")["mw"].sum()
    idx_h = s26.index
    q_idx = pd.date_range(idx_h[0], idx_h[-1] + pd.Timedelta(minutes=45), freq="15min")
    hourly = s26.values * 1.008
    # within the hour the load moves toward the next hour's: the reading at quarter q is a blend
    nxt = np.concatenate([hourly[1:], hourly[-1:]])
    vals = []
    for k in range(len(hourly)):
        for q in range(4):
            frac = (q + 0.5) / 4.0
            vals.append(hourly[k] * (1 - frac) + nxt[k] * frac)
    vals = np.array(vals) * (1 + rng.normal(0, 0.006, len(vals)))
    t1 = vals * 0.52
    t2 = vals * 0.48
    days = (len(q_idx) + 95) // 96
    grain = np.zeros(len(q_idx))
    for d in range(days):
        on = rng.random() < 0.55
        if on:
            start = d * 96 + int(rng.integers(20, 60))
            length = int(rng.integers(24, 64))
            grain[start:start + length] = rng.uniform(2.6, 3.4)
    grain = grain + 0.18 + rng.normal(0, 0.02, len(q_idx))
    end_local = q_idx + pd.Timedelta(minutes=15)
    end_utc = end_local - pd.Timedelta(hours=PR.UTC_OFFSET_H)
    out = []
    for (mid, name), series in zip(GT_METERS, (t1, t2, grain)):
        out.append(pd.DataFrame({"meter": mid, "end_utc": end_utc, "kwh": series * 1000.0 / 4.0, "who": name}))
    return pd.concat(out, ignore_index=True)


# ------------------------------------------------------------------ distractors
def outages():
    rng = np.random.default_rng(PR.OTHER_SEED)
    causes = ["tree contact", "animal", "lightning", "equipment failure", "vehicle", "unknown", "planned work"]
    rows = []
    t = pd.Timestamp("2026-01-03 04:00")
    num = 26001
    while t < pd.Timestamp("2026-10-31"):
        t = t + pd.Timedelta(hours=float(rng.exponential(60)))
        num += int(rng.integers(1, 4))
        f = PR.FEEDERS[int(rng.integers(0, 8))]
        dur = float(rng.lognormal(4.2, 0.8))
        cust = int(rng.lognormal(3.2, 1.3)) + 1
        rows.append((num, t.round("min"), f, causes[int(rng.integers(0, 7))], round(dur), cust))
    return pd.DataFrame(rows, columns=["outage_no", "start", "feeder", "cause", "minutes", "members_out"])


def simulate():
    wx = weather()
    ld, log = loads(wx)
    tx = transformers()
    md = mdms(ld, tx)
    gt = revenue_meters(ld)
    return {"wx": wx, "ld": ld, "log": log, "tx": tx, "mdms": md, "gt": gt, "outages": outages()}
