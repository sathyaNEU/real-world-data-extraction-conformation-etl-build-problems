"""The simulated truth: substations, the VPR-340 fleet, the renewal programme and every PSU failure.

Failures are drawn for every month from installation, so the world has a full history; the work-order
system only ever sees the months from the January 2021 migration on.
"""
import datetime as dt

import numpy as np
import pandas as pd

import world as W

PLACE_A = ["Ash", "Birch", "Cedar", "Elm", "Fox", "Glen", "Hawk", "Iron", "Kings", "Lake", "Mill", "North",
           "Oak", "Pine", "Red", "Silver", "Stone", "West", "White", "Wolf", "Bear", "Deer", "Fern", "Grey",
           "High", "Long", "Maple", "Moss", "Rock", "Sand", "Spring", "Sugar", "Willow", "Clear", "Crow", "Otter",
           "Port", "Brant", "Kettle", "Heron"]
PLACE_B = ["brook", " Bay", " Bridge", " Corners", " Creek", "dale", " Falls", "field", "ford", " Hill", "hurst",
           " Junction", " Landing", " Mills", "mount", " Point", " Ridge", " River", "ton", "ville", "wood", " Road"]
_AWKWARD = ("Lake Landing", "Mill Mills", "Port Point", "Rock Ridge", "Stone Ridge", "Sand Bay", "North Point")
CURRENT_REGIONS = ["North", "Central", "South"]
LEGACY_REGIONS = ["Lakeshore", "Ridge", "Valley", "Harbour"]


def month_add(d, n):
    y, m = d.year + (d.month - 1 + n) // 12, (d.month - 1 + n) % 12 + 1
    return dt.date(y, m, 1)


def months_between(a, b):
    """month starts from a (inclusive) to b (exclusive)"""
    out, d = [], dt.date(a.year, a.month, 1)
    while d < b:
        out.append(d)
        d = month_add(d, 1)
    return out


def age_on(inst, first):
    """completed years on the first day of a month"""
    return first.year - inst.year - ((first.month, 1) < (inst.month, inst.day))


def substations(rng):
    names, seen = [], set()
    while len(names) < W.N_SUBS:
        a, b = PLACE_A[rng.integers(len(PLACE_A))], PLACE_B[rng.integers(len(PLACE_B))]
        n = a + b
        if b.strip().lower().startswith(a.lower()[-3:]) or a.lower().endswith(b.strip().lower()[:3]) or n in _AWKWARD:
            continue
        if any(n.startswith(x) and n != x and x.endswith(b) for x in seen):
            continue
        if n not in seen:
            seen.add(n)
            names.append(n)
    rows = []
    for i, n in enumerate(names):
        legacy = LEGACY_REGIONS[rng.integers(4)]
        # 2024 reorganisation: Lakeshore -> North, Harbour -> South, Ridge and Valley split
        cur = {"Lakeshore": "North", "Harbour": "South"}.get(legacy) or (
            "Central" if rng.random() < 0.6 else ("North" if legacy == "Ridge" else "South"))
        kind = "TS" if rng.random() < 0.12 else "DS"
        rows.append(dict(sub_code="%s-%03d" % (kind, i + 1), sub_name=n, region=cur, legacy_region=legacy))
    return pd.DataFrame(rows)


def fleet(rng, subs):
    """VPR-340 relays: installed in substation campaigns 1992-2018, some bays added later."""
    yrs = np.arange(1992, 2019)
    w = 0.85 * np.exp(-0.5 * ((yrs - 2008) / 5.0) ** 2)
    w = w / w.sum() * 0.85 + (yrs <= 2000) * (0.15 / (yrs <= 2000).sum())
    w = w / w.sum()
    rows, rid = [], 0
    host = subs.sample(n=118, random_state=int(rng.integers(1e9))).sort_values("sub_code")
    counts = rng.multinomial(W.N_RELAY - 118 * 3, np.full(118, 1 / 118)) + 3
    for (_, s), c in zip(host.iterrows(), counts):
        camp = int(rng.choice(yrs, p=w))
        for j in range(c):
            y = camp if rng.random() < 0.8 else int(min(2018, camp + rng.integers(1, 9)))
            m, d = int(rng.integers(1, 13)), int(rng.integers(1, 29))
            rid += 1
            rows.append(dict(relay_key=rid, sub_code=s.sub_code, install=dt.date(y, m, d)))
    return pd.DataFrame(rows)


def programme(rng, fl):
    """Approved 2026 renewal month per host substation (older campaigns tend to go first),
    the superseded 2025 plan, and the substations retired early by rebuilds."""
    subs = fl.groupby("sub_code")["install"].min().reset_index()
    age = np.array([(W.ASOF - d).days / 365.25 for d in subs["install"]])
    score = age + rng.normal(0, 15, len(subs))
    order = np.argsort(np.argsort(-score))
    n = len(subs)
    early = order < 6                                   # rebuilt 2022-2025, relays retired
    sched = []
    k = 0
    for i in range(n):
        if early[i]:
            sched.append(None)
            continue
        sched.append(None)
    rest = [i for i in np.argsort(order) if not early[i]]
    unscheduled = set(rest[-9:])                         # beyond the programme: supported to its end
    slots = len(rest) - len(unscheduled)
    for pos, i in enumerate(rest):
        if i in unscheduled:
            continue
        sched[i] = month_add(dt.date(2027, 1, 1), int(pos * 108 / slots))
    subs["plan_2026"] = sched
    subs["retired_on"] = [dt.date(2022 + int(r % 4), int(1 + rng.integers(12)), 1) if early[i] else None
                          for i, r in enumerate(order)]
    subs["unscheduled"] = [i in unscheduled for i in range(n)]
    # 2025 plan: 23 schemes moved by the 2026 revision (deferred 6 to 30 months, a few brought forward)
    p25 = list(sched)
    movable = [i for i in range(n) if sched[i] is not None]
    for i in rng.choice(movable, 23, replace=False):
        shift = int(rng.integers(6, 31)) * (1 if rng.random() < 0.8 else -1)
        p25[i] = max(dt.date(2027, 1, 1), month_add(sched[i], -shift))
    subs["plan_2025"] = p25
    return subs


def support_end(prog_row):
    """first month a relay is no longer supported (the scheme's commissioning month, or the month
    after the programme ends)"""
    if prog_row["plan_2026"] is None:
        return month_add(W.PROGRAMME_END, 1)
    return prog_row["plan_2026"]


def failures(rng, fl, prog):
    """Every PSU failure from installation to the extract date (monthly draws on the wear-out law)."""
    ret = dict(zip(prog["sub_code"], prog["retired_on"]))
    out = []
    all_months = months_between(dt.date(1992, 1, 1), dt.date(2026, 10, 1))
    inst = list(fl["install"])
    keys = list(fl["relay_key"])
    end = [ret.get(s) or dt.date(2026, 10, 1) for s in fl["sub_code"]]
    for m in all_months:
        live = [i for i in range(len(inst)) if inst[i] < m and m < end[i]]
        if not live:
            continue
        ages = np.array([age_on(inst[i], m) for i in live])
        p = np.array([W.hazard(a + 0.5) for a in ages]) / 12.0
        hit = rng.random(len(live)) < p
        for j in np.where(hit)[0]:
            day = int(rng.integers(1, 29))
            out.append(dict(relay_key=keys[live[j]], month=m, date=dt.date(m.year, m.month, day),
                            age=int(ages[j])))
    df = pd.DataFrame(out)
    post = df.index[df["month"] >= W.MIGRATION].tolist()
    inst = dict(zip(fl["relay_key"], fl["install"]))
    for k, shift in W.TUNE:
        i = post[k]
        m = month_add(df.at[i, "month"], shift)
        if W.MIGRATION <= m <= dt.date(2026, 9, 1):
            df.at[i, "month"] = m
            df.at[i, "date"] = dt.date(m.year, m.month, df.at[i, "date"].day)
            df.at[i, "age"] = age_on(inst[df.at[i, "relay_key"]], m)
    return df
