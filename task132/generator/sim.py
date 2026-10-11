"""The simulated truth: substations and their bays, the VPR-340 fleet, every PSU module fitted to it since
installation (originals and replacements), every PSU failure, and the renewal programme.

A PSU module wears out with its own age. When one fails the relay is out until the corrective work order
completes, and the module fitted then starts again at age zero. The world runs from 1992; the EAM only ever
sees January 2021 on, plus the module in each position at go-live with the fitted date the legacy system held.
"""
import datetime as dt

import numpy as np
import pandas as pd

import world as W

ROOTS = ["Alder", "Amber", "Arrow", "Aspen", "Barrow", "Beech", "Bell", "Birch", "Black", "Bram", "Brant", "Briar",
         "Brock", "Camden", "Cedar", "Clay", "Clear", "Cold", "Corn", "Cran", "Crow", "Deer", "Elder", "Elk", "Elm",
         "Fair", "Fern", "Fish", "Flint", "Fox", "Glen", "Gold", "Green", "Grey", "Hart", "Hazel", "Heath", "Hemlock",
         "Heron", "High", "Holly", "Juniper", "Kettle", "King", "Lark", "Laurel", "Long", "Maple", "Marl", "Mead",
         "Mill", "Moss", "Oak", "Otter", "Owl", "Pine", "Plum", "Quarry", "Rain", "Raven", "Red", "Reed", "Rock",
         "Rose", "Rush", "Sable", "Salt", "Sand", "Silver", "Slate", "Spruce", "Stag", "Still", "Stone", "Swan",
         "Thorn", "Wolf", "Wren", "Ashby", "Carden", "Farley", "Ingle", "Pember", "Strath", "Kil", "Dun", "Bal",
         "Gar", "Lyn", "Mal", "Tal", "Wel", "Win", "Hal", "Coll", "Car", "Bran", "Tam", "Wil", "Ash", "Pell",
         "Stan", "Shel", "Har", "Lang", "Mor", "Nor", "Rad", "Sel", "Ter", "Wal", "Whit", "Yar", "Brad", "Dal",
         "Ken", "Lin", "Sum", "Ald", "Bur", "Cal", "Fal", "Hol", "Ran", "Tor", "Val", "War", "Bel", "Dor", "Gran",
         "Kel", "Mid", "Nash", "Ox", "Pen", "Rich", "Sher", "Stam", "Tew", "Up", "Wend", "Ather", "Bex", "Chat",
         "Dray", "Edge", "From", "Gil", "Hep", "Ips", "Kirk", "Lox", "Mere", "Ney", "Ock", "Pol", "Rye", "Sap"]
FRAGMENTS = {"Kil", "Dun", "Bal", "Gar", "Lyn", "Mal", "Tal", "Wel", "Win", "Hal", "Coll", "Car", "Bran", "Tam",
             "Wil", "Pell", "Stan", "Shel", "Har", "Lang", "Mor", "Nor", "Rad", "Sel", "Ter", "Wal", "Whit", "Yar",
             "Brad", "Dal", "Ken", "Lin", "Sum", "Ald", "Bur", "Cal", "Fal", "Hol", "Ran", "Tor", "Val", "War", "Bel",
             "Dor", "Gran", "Kel", "Mid", "Nash", "Ox", "Pen", "Rich", "Sher", "Stam", "Tew", "Up", "Wend", "Ather",
             "Bex", "Chat", "Dray", "Edge", "From", "Gil", "Hep", "Ips", "Kirk", "Lox", "Mere", "Ney", "Ock", "Pol",
             "Rye", "Sap", "Strath", "Ingle", "Pember", "Carden", "Farley", "Ashby"}
SUFFIX = ["ford", "field", "ton", "ville", "wood", "dale", "brook", "burn", "by", "ham", "mere", "more", "stead",
          "well", "worth", "bury", "cliff", "croft", "gate", "haven", "hurst", "ley", "mount", "port", "side",
          "view", " Creek", " Falls", " Hill", " Junction", " Lake", " Mills", " Point", " River", " Road"]
CURRENT_REGIONS = ["North", "Central", "South"]
LEGACY_REGIONS = ["Lakeshore", "Ridge", "Valley", "Harbour"]
SB_CUTOFF = dt.date(1998, 1, 1)
SEASON = np.array([0.3, 0.3, 0.6, 1.4, 1.6, 1.3, 0.5, 0.5, 1.3, 1.6, 1.3, 0.3])   # outage windows, Jan..Dec


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


def mindex(d):
    return d.year * 12 + d.month - 1


def age_on(fitted, first):
    """completed years on the first day of a month"""
    return first.year - fitted.year - ((first.month, 1) < (fitted.month, fitted.day))


def first_month(d):
    """first month a module or relay placed in service on d counts: in service on the first day"""
    m = dt.date(d.year, d.month, 1)
    return m if d.day == 1 else month_add(m, 1)


def weekday(rng, d, sat=0.04):
    """move a planned date off the weekend (a few Saturday jobs stay)"""
    if d.weekday() == 5 and rng.random() < sat:
        return d
    while d.weekday() >= 5:
        d = d + dt.timedelta(days=1)
    return d


def _name(rng, used_root, suffix_n):
    while True:
        r = ROOTS[int(rng.integers(len(ROOTS)))]
        s = SUFFIX[int(rng.integers(len(SUFFIX)))]
        if r in used_root or suffix_n.get(s, 0) >= 6:
            continue
        t = s.strip().lower()
        if s[0] == " " and r in FRAGMENTS:
            continue
        if s[0] != " " and r in FRAGMENTS and r in ("Ashby", "Carden", "Farley", "Ingle", "Pember", "Strath"):
            continue
        if r.lower()[-1] == t[0] or r.lower().endswith(t[:2]) or (r.lower() + t) in ("kington", "newton", "oxford", "brantford", "langford", "whitmore", "shelby", "deerfield", "radcliff"):
            continue
        used_root.add(r)
        suffix_n[s] = suffix_n.get(s, 0) + 1
        return r + s


def substations(rng):
    used, sn, names = set(), {}, []
    while len(names) < W.N_SUBS:
        n = _name(rng, used, sn)
        if n not in names:
            names.append(n)
    kinds = ["TS"] * W.N_TS + ["DS"] * (W.N_SUBS - W.N_TS)
    rng.shuffle(kinds)
    rows, nts, nds = [], 0, 0
    for n, kind in zip(names, kinds):
        if kind == "TS":
            nts += 1
            code = "TS-%02d" % nts
        else:
            nds += 1
            code = "DS-%03d" % nds
        legacy = LEGACY_REGIONS[int(rng.choice(4, p=[0.27, 0.24, 0.27, 0.22]))]
        # 2024 reorganisation: Lakeshore -> North, Harbour -> South, Ridge and Valley split
        cur = {"Lakeshore": "North", "Harbour": "South"}.get(legacy) or (
            "Central" if rng.random() < 0.6 else ("North" if legacy == "Ridge" else "South"))
        ntx = int(rng.integers(2, 4)) if kind == "TS" else int(rng.integers(1, 3))
        nbus = 2 if kind == "TS" else (1 if rng.random() < 0.3 else 0)
        rows.append(dict(sub_code=code, sub_name=n, station_type=kind, region=cur, legacy_region=legacy,
                         n_tx=ntx, n_bus=nbus))
    return pd.DataFrame(rows)


def _install_day(rng, y, m):
    d = dt.date(y, m, int(rng.integers(1, 29)))
    return weekday(rng, d, sat=0.0)


def fleet(rng, subs):
    """VPR-340 relays, one per feeder bay: station campaigns 1992-2018, then feeders added later.
    Campaign bays are numbered first, added bays after them."""
    yrs = np.arange(1992, 2019)
    w = 0.85 * np.exp(-0.5 * ((yrs - 2008) / 5.0) ** 2)
    w = w / w.sum() * 0.85 + (yrs <= 2000) * (0.15 / (yrs <= 2000).sum())
    w = w / w.sum()
    ts = subs[subs["station_type"] == "TS"].sample(n=12, random_state=int(rng.integers(1e9)))
    ds = subs[subs["station_type"] == "DS"].sample(n=106, random_state=int(rng.integers(1e9)))
    host = pd.concat([ts, ds]).sort_values("sub_code")
    base = np.where(host["station_type"] == "TS", 9, 3)
    extra = W.N_RELAY - int(base.sum())
    weights = np.where(host["station_type"] == "TS", 2.2, 1.0)
    counts = base + rng.multinomial(extra, weights / weights.sum())
    rows, rid = [], 0
    for (_, s), c in zip(host.iterrows(), counts):
        camp = int(rng.choice(yrs, p=w))
        cm = int(rng.integers(3, 11))
        n_camp = max(2, int(round(c * (0.8 if rng.random() < 0.7 else 0.6))))
        inst = []
        for j in range(c):
            if j < n_camp:
                y, m = camp, min(12, max(1, cm + int(rng.integers(-1, 2))))
            else:
                y = int(min(2018, camp + rng.integers(1, 10)))
                m = int(rng.integers(1, 13))
            inst.append(_install_day(rng, y, m))
        inst.sort()
        for j, d in enumerate(inst):
            rid += 1
            rows.append(dict(relay_key=rid, sub_code=s.sub_code, bay="F%02d" % (j + 1), install=d))
    return pd.DataFrame(rows)


def programme(rng, fl, subs):
    """Schemes in the approved 2026 programme for every substation still carrying VPR-340 relays (older
    stations tend to go first), schemes at stations without VPR-340, the superseded 2025 plan, and the
    stations rebuilt early (2022-2025). Large stations are replaced in two outage stages."""
    host = fl.groupby("sub_code").agg(first=("install", "min"), n=("relay_key", "size")).reset_index()
    age = np.array([(W.ASOF - d).days / 365.25 for d in host["first"]])
    score = age + rng.normal(0, 13, len(host))
    order = np.argsort(np.argsort(-score))
    n = len(host)
    early = order < 6
    rest = [i for i in np.argsort(order) if not early[i]]
    unscheduled = set(rest[-9:])
    sched_idx = [i for i in rest if i not in unscheduled]
    # commissioning months: 2027-2035, about a dozen a year, mostly in the spring and autumn outage windows
    months = months_between(dt.date(2027, 1, 1), dt.date(2036, 1, 1))
    mw = np.array([SEASON[m.month - 1] for m in months])
    picks = np.sort(rng.choice(len(months), len(sched_idx), replace=True, p=mw / mw.sum()))
    when = {i: months[p] for i, p in zip(sched_idx, picks)}
    rebuilt = {}
    for i in range(n):
        if early[i]:
            y = 2022 + int(order[i] % 4)
            rebuilt[i] = weekday(rng, dt.date(y, int(rng.choice([4, 5, 6, 9, 10, 11])), int(rng.integers(1, 29))), 0)
    rows = []
    for i, r in host.iterrows():
        bays = fl[fl["sub_code"] == r.sub_code]["bay"].tolist()
        rows.append(dict(sub_code=r.sub_code, n=int(r.n), first_bay=bays[0], last_bay=bays[-1],
                         plan_2026=when.get(i), unscheduled=i in unscheduled, retired_on=rebuilt.get(i)))
    prog = pd.DataFrame(rows)
    # two-stage schemes at the large stations: stage 2 one to three years after stage 1, inside the period
    prog["stage2_from"] = None
    prog["plan_2026_s2"] = None
    big = prog[(prog["n"] >= W.STAGE_MIN) & prog["plan_2026"].notna()].index.tolist()
    for i in big:
        p1 = prog.at[i, "plan_2026"]
        lag = int(rng.integers(W.STAGE_LAG[0], W.STAGE_LAG[1]))
        p2 = month_add(p1, lag)
        while SEASON[p2.month - 1] < 1.0:
            p2 = month_add(p2, 1)
        if p2 > W.PROGRAMME_END:
            continue
        k = prog.at[i, "n"] // 2 + int(rng.integers(-1, 2))
        prog.at[i, "stage2_from"] = "F%02d" % (k + 1)
        prog.at[i, "plan_2026_s2"] = p2
    # 2025 plan: one stage per scheme; 23 schemes moved by the 2026 revision (mostly deferred)
    p25 = list(prog["plan_2026"])
    movable = [i for i in range(n) if p25[i] is not None]
    for i in rng.choice(movable, 23, replace=False):
        shift = int(rng.integers(6, 31)) * (1 if rng.random() < 0.8 else -1)
        p25[i] = max(dt.date(2027, 1, 1), month_add(p25[i], -shift))
    prog["plan_2025"] = p25
    # schemes at stations with no VPR-340 (VPR-220 and RTU renewals), in both versions
    others = subs[~subs["sub_code"].isin(host["sub_code"])]
    pick = others.sample(n=17, random_state=int(rng.integers(1e9)))
    extra = []
    for _, s in pick.iterrows():
        m = months[int(rng.choice(len(months), p=mw / mw.sum()))]
        m25 = m if rng.random() < 0.8 else month_add(m, -int(rng.integers(6, 19)))
        extra.append(dict(sub_code=s.sub_code, plan_2026=m, plan_2025=max(dt.date(2027, 1, 1), m25)))
    return prog, pd.DataFrame(extra)


def support_end(prog_row, bay):
    """first month a relay is no longer supported (its bay's commissioning month, or the month after the
    programme period ends)"""
    if prog_row["plan_2026"] is None or (isinstance(prog_row["plan_2026"], float)):
        return month_add(W.PROGRAMME_END, 1)
    s2 = prog_row["stage2_from"]
    if s2 is not None and isinstance(s2, str) and bay >= s2:
        return prog_row["plan_2026_s2"]
    return prog_row["plan_2026"]


def modules(rng, fl, prog):
    """Every PSU module fitted to a VPR-340 position from installation to the extract date.

    Each month a module in service on the first day fails with probability hazard(age + 0.5) / 12. The
    corrective work completes 0 to 6 days later (emergency work the same day), and the module fitted then is
    in service from the next first day of a month."""
    ret = dict(zip(prog["sub_code"], prog["retired_on"]))
    keys = fl["relay_key"].tolist()
    inst = fl["install"].tolist()
    stop = [ret.get(s) for s in fl["sub_code"]]
    n = len(keys)
    fitted = list(inst)
    live_from = [first_month(d) for d in inst]
    spells, fails = [], []
    serial = [0] * n
    # Veldtek service bulletin SB-15-02 (2015): PSU modules in relays installed before 1998 replaced, station by station
    camp = {}
    for s_ in sorted(set(fl["sub_code"])):
        camp[s_] = weekday(rng, dt.date(2015, int(rng.integers(4, 12)), int(rng.integers(1, 29))), 0)
    for m in months_between(dt.date(1992, 1, 1), dt.date(2026, 10, 1)):
        if m.year == 2015:
            for i in range(n):
                c = camp[fl["sub_code"].iat[i]]
                if (c.year, c.month) == (m.year, m.month) and inst[i] < SB_CUTOFF and live_from[i] <= m and fitted[i] < dt.date(2011, 1, 1):
                    spells.append(dict(relay_key=keys[i], module=serial[i], fitted=fitted[i], removed=c, reason="CAMPAIGN"))
                    serial[i] += 1
                    fitted[i] = c
                    live_from[i] = first_month(c)
        idx = [i for i in range(n) if live_from[i] <= m and (stop[i] is None or m < first_month(stop[i]))]
        if not idx:
            continue
        ages = np.array([age_on(fitted[i], m) for i in idx])
        p = np.array([W.hazard(a + 0.5) for a in ages]) / 12.0
        hit = rng.random(len(idx)) < p
        for j in np.where(hit)[0]:
            i = idx[j]
            rep = dt.date(m.year, m.month, int(rng.integers(2, 29)))
            em = rng.random() < 0.3
            eom = month_add(m, 1) - dt.timedelta(days=1)
            done = min(rep + dt.timedelta(days=0 if em else int(rng.integers(1, 7))), eom, W.ASOF)
            if stop[i] is not None and done >= stop[i]:
                continue                                   # station rebuilt before the repair: no record
            fails.append(dict(relay_key=keys[i], reported=rep, month=m, age=int(ages[j]), em=em, done=done,
                              module=serial[i]))
            spells.append(dict(relay_key=keys[i], module=serial[i], fitted=fitted[i], removed=done, reason="FAILED"))
            serial[i] += 1
            fitted[i] = done
            live_from[i] = first_month(done)
    for i in range(n):
        spells.append(dict(relay_key=keys[i], module=serial[i], fitted=fitted[i],
                           removed=stop[i], reason="RETIRED" if stop[i] else None))
    f = pd.DataFrame(fails)
    sp = pd.DataFrame(spells).sort_values(["relay_key", "module"], kind="mergesort").reset_index(drop=True)
    return sp, f
