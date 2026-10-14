"""the processes: weather at three stations, the trimming campaigns and who worked them, and the outages the network
had from 2016 to 2025 (trees growing into the line on the regrowth clock, trees falling in from beyond the cleared
right-of-way, the other causes, secondary and planned outages, and the storms that make major event days)"""
from datetime import date, datetime, timedelta

import numpy as np
import pandas as pd

import params as P

DAYS = pd.date_range(P.OUT_START, P.OUT_END, freq="D")
D0 = pd.Timestamp(P.OUT_START)


def _ts(d):
    return pd.Timestamp(d)


def weather(rng):
    """daily peak gust (mph) and rainfall (inches) at each district's station"""
    n = len(DAYS)
    doy = DAYS.dayofyear.values
    storm_days = {pd.Timestamp(d) for d, _ in P.STORMS}
    out = {}
    for d in P.DISTRICTS:
        winter = 4.0 * np.cos(2 * np.pi * (doy - 20) / 365.25)
        gust = 17.0 + winter + rng.gamma(4.4, 4.4, n)
        wet = rng.random(n) < (0.27 + 0.08 * np.sin(2 * np.pi * (doy - 120) / 365.25))
        rain = np.where(wet, rng.gamma(0.85, 0.36, n), 0.0)
        for i, day in enumerate(DAYS):
            if day in storm_days:
                gust[i] = rng.uniform(58, 76)
                rain[i] = rain[i] + rng.uniform(0.4, 1.6)
        if d == "South":
            m = DAYS.year == 2025
            gust[m] = gust[m] + 4.6
        if d == "North":
            m = (DAYS.year == 2024) & (DAYS.month >= 5) & (DAYS.month <= 9)
            rain[m] = rain[m] * P.NORTH_WET_2024
        out[d] = pd.DataFrame({"date": DAYS, "gust": np.round(gust, 0), "rain": np.round(rain, 2)})
    return out


def mortality(d, day_index):
    """the ash mortality reaching the line in a district, 0 before it starts, rising to its maximum over the ramp"""
    on = P.MORTALITY_ONSET[d]
    if on is None:
        return np.zeros(len(day_index))
    x = (day_index - pd.Timestamp(on)).days.values.astype(float) / P.MORTALITY_RAMP_DAYS
    return np.clip(x, 0, None).clip(max=P.MORTALITY_MAX)


def trims(U, rng):
    """one row per trim of a unit: the circuit's campaign every four years, worked unit by unit by the contractor
    holding the district (with the outgoing firm finishing its open North work orders and East's 2025 campaigns
    starting late after the handover), each accepted or rejected at the audit and re-trimmed when rejected"""
    rows = []
    wo_n = 0
    circ = U.groupby("circuit")
    first = {}
    for d in P.DISTRICTS:                       # each district's circuits spread evenly over the four-year cycle
        cs = sorted(U[U.district == d].circuit.unique())
        for k, c in zip(rng.permutation(len(cs)), cs):
            first[c] = P.HIST_START + timedelta(days=int((k + rng.uniform(0.15, 0.85)) / len(cs) * P.CYCLE * 365.25))
    for c in sorted(U.circuit.unique()):
        units = circ.get_group(c).sort_values("seq")
        dist = units.district.iloc[0]
        due = first[c]
        while due <= P.OUT_END:
            start = due
            con = P.OUTGOING
            hd = P.HANDOVER.get(dist)
            if hd is not None and due >= hd:
                con = P.INCOMING
            if dist == "North" and P.HANDOVER["North"] <= due < date(2025, 1, 1):
                if rng.random() < P.NORTH_OPEN_ORDERS:
                    con = P.OUTGOING
                else:
                    start = due + timedelta(days=int(rng.integers(0, 50)))
            if dist == "East" and P.EAST_LAST_ORDER < due < date(2026, 1, 1):
                con = P.INCOMING
                start = due + timedelta(days=int(rng.integers(*P.EAST_SLIP_DAYS)))
            span = int(rng.integers(14, 48))
            wo_n += 1
            wo = "WO-%02d-%04d" % (start.year % 100, wo_n)
            live = units[(units.in_service <= start) & (units.retired.isna() | (units.retired.map(
                lambda r: r is None or r > start)))]
            k = len(live)
            for j, (_, u) in enumerate(live.iterrows()):
                if u.in_service.year >= 2024 and (start - u.in_service).days < 730:
                    continue                                   # cleared when the line was rebuilt
                done = start + timedelta(days=int(j * span / max(k, 1)))
                if con == P.OUTGOING and dist == "North" and start >= P.HANDOVER["North"]:
                    done = min(done, P.NORTH_OPEN_END - timedelta(days=int(rng.integers(0, 6))))
                    if done < start:
                        continue
                if done > P.OUT_END:
                    continue
                rej = rng.random() < 0.04
                crew = "%s-%02d" % ("HL" if con == P.OUTGOING else "GV", int(rng.integers(1, 9)))
                acc = done + timedelta(days=int(rng.integers(6, 25)))
                rows.append(dict(work_order=wo, unit_id=u.unit_id, contractor=con, completed=done,
                                 status="REJECTED" if rej else "ACCEPTED", accepted=None if rej else acc, crew=crew,
                                 measured=float(u.miles * rng.uniform(0.975, 1.025))))
                if rej:
                    d2 = done + timedelta(days=int(rng.integers(18, 50)))
                    if d2 <= P.OUT_END:
                        rows.append(dict(work_order=wo, unit_id=u.unit_id, contractor=con, completed=d2,
                                         status="ACCEPTED", accepted=d2 + timedelta(days=int(rng.integers(6, 20))),
                                         crew=crew, measured=0.0))
            due = due + timedelta(days=int(round(P.CYCLE * 365.25 + rng.normal(0, 18))))
    T = pd.DataFrame(rows).sort_values(["completed", "unit_id", "status"]).reset_index(drop=True)
    return T


def _members_on(U, M):
    """members a unit's circuit serves at the end of 2025, spread over the circuit's miles"""
    m25 = M[M.year == 2025].set_index("district").members
    circ_mi = U[U.retired.isna() | U.planned].groupby("circuit").miles.sum()
    dist_mi = U[U.retired.isna() | U.planned].groupby("district").miles.sum()
    circ_members = {c: m25[d] * circ_mi[c] / dist_mi[d] for c, d in U.groupby("circuit").district.first().items()
                    if c in circ_mi.index}
    return circ_members


def _steps(rng, members, storm):
    """restoration steps: members restored and the minutes from the start to each step"""
    if members <= 25 or rng.random() < 0.55:
        k = 1
    else:
        k = 2 if rng.random() < 0.78 else 3
    first = float(np.exp(rng.normal(np.log(260 if storm else 92), 0.55)))
    mins = [first]
    for _ in range(k - 1):
        mins.append(mins[-1] + float(np.exp(rng.normal(np.log(150 if storm else 65), 0.5))))
    if k == 1:
        parts = [members]
    else:
        w = rng.dirichlet(np.ones(k) * 1.6)
        parts = list(np.maximum(1, np.round(w * members).astype(int)))
        parts[-1] = members - sum(parts[:-1])
        if parts[-1] < 1:
            parts = [members]
            mins = mins[:1]
    return [int(round(m)) for m in mins], [int(p) for p in parts]


def outages(U, T, Wx, dens, M, rng):
    """every outage from 2016 to 2025, one record each, with its restoration steps; the generator keeps each tree
    outage's kind (growing in, falling in) for the checks, and nothing in the pack carries it"""
    ash_d, wood_d = dens
    wood_mean = float(wood_d[wood_d > 0].mean())
    circ_members = _members_on(U, M)
    circ_units = U.groupby("circuit").unit_id.count()
    doy = DAYS.dayofyear.values
    season_g = 1 + P.SEASON_G * np.sin(2 * np.pi * (doy - 118) / 365.25)
    season_animal = 1 + 0.5 * np.sin(2 * np.pi * (doy - 100) / 365.25)
    season_light = np.clip(1 + 1.6 * np.sin(2 * np.pi * (doy - 110) / 365.25), 0.05, None)
    storm_set = {pd.Timestamp(d): n for d, n in P.STORMS}
    Tg = {k: v for k, v in T.groupby("unit_id")}
    recs = []
    for _, u in U.iterrows():
        alive = (DAYS >= _ts(u.in_service)) & ((DAYS < _ts(u.retired)) if u.retired is not None else True)
        if not alive.any():
            continue
        g = Wx[u.district].gust.values
        tr = Tg.get(u.unit_id)
        cd = np.array(sorted(pd.to_datetime(tr.completed).values)) if tr is not None else np.array([], "datetime64[ns]")
        if u.in_service.year >= 2024:
            cd = np.sort(np.concatenate([cd, np.array([np.datetime64(u.in_service, "ns")])]))
        pos = np.searchsorted(cd, DAYS.values, side="right") - 1
        last = np.where(pos >= 0, cd[np.maximum(pos, 0)], np.datetime64("2011-06-01", "ns"))
        t = (DAYS.values - last).astype("timedelta64[D]").astype(float) / 365.25
        grow = P.G_AVG * (P.G_POW + 1) * (np.clip(t, 0, None) / P.CYCLE) ** P.G_POW * season_g \
            * np.exp(P.WIND_G * np.clip(g - 35, 0, None))
        ash_share = ash_d.get(u.unit_id, 0.0) / max(wood_d.get(u.unit_id, 1.0), 1e-9)
        fall = (P.F_BASE * wood_d.get(u.unit_id, wood_mean) / wood_mean
                + P.F_ASH * ash_share * wood_d.get(u.unit_id, wood_mean) / wood_mean * mortality(u.district, DAYS)) \
            * np.exp(P.WIND_F * np.clip(g - 35, 0, None))
        other = sum(P.OTHER.values())
        o_rate = (P.OTHER["ANIMAL"] * season_animal + P.OTHER["LIGHTNING"] * season_light
                  + (other - P.OTHER["ANIMAL"] - P.OTHER["LIGHTNING"])) * np.exp(0.02 * np.clip(g - 35, 0, None))
        lam = u.miles / 365.25 * np.where(alive, 1.0, 0.0)
        n_g = rng.poisson(lam * grow)
        n_f = rng.poisson(lam * fall)
        n_o = rng.poisson(lam * o_rate)
        cm = circ_members.get(u.circuit, 600.0)
        for kind, arr in (("grow", n_g), ("fall", n_f), ("other", n_o)):
            for j in np.nonzero(arr)[0]:
                for _ in range(int(arr[j])):
                    if kind == "other":
                        cause = rng.choice(["ANIMAL", "EQUIPMENT", "LIGHTNING", "VEHICLE", "UNKNOWN"],
                                           p=np.array([P.OTHER[c] for c in ("ANIMAL", "EQUIPMENT", "LIGHTNING",
                                                                             "VEHICLE", "UNKNOWN")]) / other)
                    else:
                        cause = "TREE"
                    recs.append(_outage(rng, DAYS[j], "PRIMARY", u, cause, kind, cm, circ_units[u.circuit],
                                        DAYS[j] in storm_set))
    # storms: the outages a storm day brings on top of the daily processes, mostly trees
    live = U[U.retired.isna() | U.planned]
    for day, n in P.STORMS:
        day = pd.Timestamp(day)
        w = (live.miles * (live.wood / live.wood.mean())).values
        pick = rng.choice(len(live), size=n, p=w / w.sum())
        for i in pick:
            u = live.iloc[i]
            if not (pd.Timestamp(u.in_service) <= day and (u.retired is None or pd.Timestamp(u.retired) > day)):
                continue
            cause = rng.choice(["TREE", "EQUIPMENT", "LIGHTNING", "UNKNOWN"], p=[0.62, 0.2, 0.1, 0.08])
            recs.append(_outage(rng, day, "PRIMARY", u, cause, "storm", circ_members.get(u.circuit, 600.0),
                                circ_units[u.circuit], True))
    # secondary and service outages, and planned work
    m_by = M.set_index(["district", "year"]).members
    for d in P.DISTRICTS:
        du = U[U.district == d]
        g = Wx[d].gust.values
        mem = np.array([m_by[(d, y)] for y in DAYS.year])
        lam = mem * P.SECONDARY_PER_MEMBER / 365.25 * np.exp(0.03 * np.clip(g - 35, 0, None))
        ins = pd.to_datetime(du.in_service).values
        ret = pd.to_datetime(du.retired.map(lambda r: r if r is not None else date(2099, 1, 1))).values
        for day_i in range(len(DAYS)):
            day = DAYS[day_i]
            k = rng.poisson(lam[day_i] * (3.0 if day in storm_set else 1.0))
            alive = du[(ins <= day.to_datetime64()) & (ret > day.to_datetime64())]
            for _ in range(k):
                u = alive.iloc[int(rng.integers(0, len(alive)))]
                cause = rng.choice(["TREE", "EQUIPMENT", "ANIMAL", "UNKNOWN", "VEHICLE"], p=[0.31, 0.38, 0.16, 0.1, 0.05])
                recs.append(_outage(rng, day, "SECONDARY", u, cause, "secondary", 0, 1, day in storm_set))
            if day.weekday() < 5:
                kp = rng.poisson(len(alive) * P.UNIT_MILES * P.PLANNED_PER_MILE / 261.0)
                for _ in range(kp):
                    u = alive.iloc[int(rng.integers(0, len(alive)))]
                    recs.append(_outage(rng, day, "PRIMARY", u, "PLANNED", "planned", 120.0,
                                        circ_units[u.circuit], False))
    O = pd.DataFrame(recs)
    O = O.sort_values(["start", "unit_id", "cause"], kind="stable").reset_index(drop=True)
    return O


def _outage(rng, day, level, u, cause, kind, circ_members, n_circ_units, storm):
    """one outage: the protective device that opened, the members it took out, when it started (local time) and the
    restoration steps"""
    if level == "SECONDARY":
        device = rng.choice(["TRANSFORMER", "SERVICE"], p=[0.62, 0.38])
        members = int(rng.integers(1, 14)) if device == "TRANSFORMER" else 1
    elif kind == "planned":
        device = "SWITCH"
        members = int(rng.integers(4, 90))
    else:
        device = rng.choice(["FUSE", "RECLOSER", "BREAKER"], p=[0.71, 0.24, 0.05])
        if device == "FUSE":
            members = int(np.clip(rng.lognormal(np.log(26), 0.7), 3, 0.4 * circ_members))
        elif device == "RECLOSER":
            members = int(np.clip(circ_members * rng.uniform(0.15, 0.5), 20, circ_members))
        else:
            members = int(max(30, circ_members))
    hour = rng.choice(24, p=_hour_profile(storm))
    minute = int(rng.integers(0, 60))
    start = datetime(day.year, day.month, day.day, int(hour), minute)
    if start.month == 3 and start.weekday() == 6 and 8 <= start.day <= 14 and start.hour == 2:
        start = start.replace(hour=3)                      # no local time in the spring-forward hour
    momentary = device == "RECLOSER" and kind not in ("storm", "planned") and rng.random() < P.MOMENTARY_SHARE
    if momentary:
        mins, parts = [int(rng.integers(1, 6))], [members]
    elif kind == "planned":
        mins, parts = [int(rng.integers(60, 360))], [members]
    else:
        mins, parts = _steps(rng, members, storm)
    return dict(start=start, level=level, unit_id=u.unit_id, district=u.district, circuit=u.circuit, device=device,
                cause=cause, kind=kind, members=int(sum(parts)), steps_min=mins, steps_members=parts, storm=storm)


def _hour_profile(storm):
    h = np.arange(24)
    p = 0.6 + 0.9 * np.exp(-0.5 * ((h - 16) / 4.5) ** 2) + (0.4 if storm else 0.0)
    return p / p.sum()
