"""task240 world: the province's adults by health region, the Household Resources Survey's 2027 sample of addresses
in master-sample PSUs, who lived at each address, the fieldwork (every call, every issue, every outcome) and the
weights (the generator's clean truth: each household's real eligibility and each adult's real answers)."""
import datetime as dt

import numpy as np

import params as P


class World:
    pass


def _ages(rng):
    k = rng.choice(4, p=[0.30, 0.42, 0.18, 0.10])     # one adult, a couple, a couple and a young adult, sharers
    if k == 0:
        return [int(rng.choice([rng.integers(20, 40), rng.integers(40, 65), rng.integers(65, 92)], p=[0.35, 0.35, 0.30]))]
    if k == 1:
        a = int(rng.choice([rng.integers(22, 40), rng.integers(40, 65), rng.integers(65, 90)], p=[0.30, 0.42, 0.28]))
        return [a, int(np.clip(a + rng.integers(-5, 6), 18, 95))]
    if k == 2:
        a = int(rng.integers(40, 64))
        return [a, int(np.clip(a + rng.integers(-4, 5), 30, 70)), int(rng.integers(16, 26))]
    return [int(rng.integers(18, 35)) for _ in range(int(rng.integers(2, 5)))]


def _when(rng, start, days):
    """a call time in the evening or at the weekend more often than in office hours"""
    d = start + dt.timedelta(days=int(rng.integers(0, days)))
    h = float(rng.choice([rng.uniform(10, 16.5), rng.uniform(16.5, 20.5)], p=[0.45, 0.55]))
    return dt.datetime.combine(d, dt.time(0)) + dt.timedelta(hours=h)


def make(seed=P.SEED):
    rng = np.random.default_rng(seed)
    W = World()
    reg = {r[0]: dict(name=r[1], adults=r[2] * 1000.0, urban=r[3]) for r in P.REGIONS}
    W.reg = reg
    # ------------------------------------------------------------------ PSUs
    psus = []                                       # (psu, region, urban, frame, old_region, dep, f)
    k = 0
    for code, rr in reg.items():
        n_psu = max(7, int(round(rr["adults"] / 1000 * P.ADULTS_PER_THOUSAND / P.ADULTS_PER_PSU)))
        n_u = int(np.clip(round(n_psu * rr["urban"]), 2, n_psu - 2))
        f_strat = {1: float(rng.uniform(0.75, 1.3)), 0: float(rng.uniform(0.75, 1.3))}
        for j in range(n_psu):
            urban = 1 if j < n_u else 0
            k += 1
            frame = 2023 if rng.random() < 0.74 else 2026
            psus.append(dict(psu="P%04d" % (1000 + 7 * k + int(rng.integers(0, 5))), region=code, urban=urban,
                             frame=frame, old_region=code, dep=float(rng.normal(0, 1)), take=f_strat[urban]))
    # the 2025 boundary review moved some 2023 master-sample PSUs into a neighbouring region
    for old, new, picks in P.MOVED:
        cand = [p for p in psus if p["region"] == new and p["frame"] == 2023]
        for k in picks:
            cand[k]["old_region"] = old
    W.psus = psus
    # ------------------------------------------------------------------ addresses, households, adults
    A = []                                          # one dict per issued address
    aid = 0
    for p in psus:
        nh = int(rng.integers(9, 14))
        for _ in range(nh):
            aid += 1
            u = rng.random()
            elig = "occupied" if u >= P.P_VACANT + P.P_NONRES + P.P_DEMOL else (
                "vacant" if u < P.P_VACANT else ("nonres" if u < P.P_VACANT + P.P_NONRES else "demolished"))
            a = dict(address_id="HRS%06d" % (210000 + aid * 3 + int(rng.integers(0, 3))), psu=p["psu"], region=p["region"],
                     urban=p["urban"], elig=elig, take=p["take"])
            if elig == "occupied":
                ages = _ages(rng)
                young = float(np.mean(np.array(ages) < 35))
                a["ages"] = ages
                a["sexes"] = [int(rng.integers(1, 3)) for _ in ages]
                a["rent"] = rng.random() < 1 / (1 + np.exp(-(-1.6 + 1.6 * young + 0.6 * p["dep"] + 0.5 * p["urban"]
                                                              - 0.8 * (min(ages) >= 65))))
                a["arrears"] = rng.random() < 1 / (1 + np.exp(-(-1.75 + 0.85 * p["dep"] + (0.4 if len(ages) >= 3 else 0))))
                a["p_resp"] = 0.62 - 0.18 * young - 0.05 * p["urban"]
            A.append(a)
    W.addresses = A
    _fieldwork(W, rng)
    _adults(W, rng)
    _weights(W, seed)
    return W


OUTCOME_OF = {"vacant": 410, "nonres": 420, "demolished": 430}
LAST_RESULT = {110: "IC", 210: "RF", 220: "NC", 230: "OT", 310: "NC", 410: "VA", 420: "NR", 430: "DM"}


def _calls_for(rng, outcome):
    if outcome == 110:
        n = 1 + min(int(rng.geometric(0.45)) - 1, 8)
    elif outcome == 210:
        n = 1 + min(int(rng.geometric(0.6)) - 1, 5)
    elif outcome == 220:
        n = int(rng.integers(4, 9))
    elif outcome == 230:
        n = int(rng.integers(2, 5))
    elif outcome == 310:
        n = int(rng.integers(3, 8))
    else:
        n = int(rng.integers(1, 3))
    res = []
    for i in range(n - 1):
        res.append("AP" if (outcome in (110, 210, 230) and i == n - 2 and rng.random() < 0.55) else "NC")
    res.append(LAST_RESULT[outcome])
    return res


def _first_outcome(rng, a):
    if a["elig"] != "occupied":
        return OUTCOME_OF[a["elig"]] if rng.random() < 0.85 else 310
    if rng.random() < a["p_resp"]:
        return 110
    u = rng.random()
    if u < 0.45:
        return 210
    if u < 0.85:
        return 220 if rng.random() >= P.P_UNKNOWN_IF_NOCONTACT else 310
    return 230


def _second_outcome(rng, a):
    if a["elig"] != "occupied":
        return OUTCOME_OF[a["elig"]] if rng.random() < 0.85 else 310
    if rng.random() < P.P_REISSUE_CONVERT:
        return 110
    u = rng.random()
    return 210 if u < 0.5 else (220 if u < 0.85 else 230)


def _fieldwork(W, rng):
    """issue 1 for every worked address, a reissue for some non-response, the calls of each issue"""
    psu_of = {p["psu"]: p for p in W.psus}
    regions = list(W.reg)
    # interviewers: a pool per region, one interviewer a PSU, a different one for its reissues
    pool = {r: ["I%03d" % (100 + 10 * i + j) for j in range(max(2, len([p for p in W.psus if p["region"] == r]) // 6))]
            for i, r in enumerate(regions)}
    for p in W.psus:
        p["interviewer"] = pool[p["region"]][int(rng.integers(len(pool[p["region"]])))]
        p["start"] = P.FIELD_OPEN + dt.timedelta(days=int(rng.integers(0, 132)))
    # unworked addresses: every region has at least one
    unworked = set(int(i) for i in np.flatnonzero(rng.random(len(W.addresses)) < P.P_UNWORKED))
    for r in regions:
        idx = [i for i, a in enumerate(W.addresses) if a["region"] == r]
        if not unworked.intersection(idx):
            unworked.add(int(idx[int(rng.integers(len(idx)))]))
    for i, a in enumerate(W.addresses):
        p = psu_of[a["psu"]]
        a["issues"] = []
        if i in unworked:
            a["unworked"] = True
            continue
        a["unworked"] = False
        o1 = _first_outcome(rng, a)
        res = _calls_for(rng, o1)
        t = sorted(_when(rng, p["start"], 35) for _ in res)
        a["issues"].append(dict(issue=1, interviewer=p["interviewer"], outcome=o1, calls=list(zip(t, res))))
        if o1 in (210, 220, 230, 310) and rng.random() < P.P_REISSUE:
            s2 = t[-1].date() + dt.timedelta(days=int(rng.integers(21, 50)))
            if s2 < P.FIELD_CLOSE - dt.timedelta(days=10):
                o2 = _second_outcome(rng, a)
                res2 = _calls_for(rng, o2)
                span = min(28, (P.FIELD_CLOSE - s2).days)
                t2 = sorted(_when(rng, s2, span) for _ in res2)
                others = [x for x in pool[a["region"]] if x != p["interviewer"]] or pool[a["region"]]
                a["issues"].append(dict(issue=2, interviewer=others[int(rng.integers(len(others)))], outcome=o2,
                                        calls=list(zip(t2, res2))))
        a["final"] = a["issues"][-1]["outcome"]
    # late syncs: interviews from the last weeks whose tablet synced after the outcome extract
    late_pool = [a for a in W.addresses if not a["unworked"] and a["final"] == 110 and len(a["issues"][-1]["calls"]) >= 2
                 and a["issues"][-1]["calls"][-1][0].date() >= P.FIELD_CLOSE - dt.timedelta(days=45)]
    n_late = int(round(P.P_LATE_SYNC * sum(1 for a in W.addresses if not a["unworked"] and a["final"] == 110)))
    pick = set(int(i) for i in rng.choice(len(late_pool), min(n_late, len(late_pool)), replace=False))
    for r in regions:
        idx = [i for i, a in enumerate(late_pool) if a["region"] == r]
        if idx and not pick.intersection(idx):
            pick.add(int(idx[int(rng.integers(len(idx)))]))
    for i, a in enumerate(late_pool):
        a["late_sync"] = i in pick
    for a in W.addresses:
        a.setdefault("late_sync", False)


BANDS = [(16, 19), (20, 24), (25, 29), (30, 34), (35, 39), (40, 44), (45, 49), (50, 54), (55, 59), (60, 64), (65, 69),
         (70, 74), (75, 79), (80, 84), (85, 120)]
BAND_SHARE = np.array([5.5, 7.5, 8.0, 8.2, 8.0, 7.6, 7.2, 7.5, 8.0, 7.8, 6.6, 5.4, 3.8, 2.5, 2.4])


def _adults(W, rng):
    """every adult of each household whose interview was completed, with the answers they (or a proxy) gave"""
    rows = []
    for a in W.addresses:
        if a["unworked"] or a["final"] != 110:
            continue
        ten = 3 if a["rent"] else int(rng.choice([1, 2, 4, 5], p=[0.36, 0.44, 0.15, 0.05]))
        if rng.random() < 0.005:
            ten = -8
        arr = 1 if a["arrears"] else 2
        if rng.random() < 0.015:
            arr = -9
        for j, (age, sex) in enumerate(zip(a["ages"], a["sexes"])):
            if age >= 55:
                p_pen = 0.985 if age >= 75 else (0.95 if age >= 65 else (0.30 if age >= 60 else 0.03))
                pen = 1 if rng.random() < p_pen else 2
                u = rng.random()
                pen = -8 if u < 0.004 else (-9 if u < 0.007 else pen)
            else:
                pen = -1
            cp = (0.04 if age < 25 else 0.07 if age < 45 else 0.15 if age < 65 else 0.12 if age < 75 else 0.08) * (
                1.3 if sex == 2 else 0.75)
            care = 1 if rng.random() < cp else 2
            u = rng.random()
            care = -8 if u < 0.006 else (-9 if u < 0.008 else care)
            rows.append(dict(address_id=a["address_id"], person_no=j + 1, region=a["region"], psu=a["psu"],
                             urban=a["urban"], age=age, sex=sex, proxy=(j > 0 and rng.random() < 0.12),
                             q_pension=pen, q_tenure=ten, q_care=care, q_arrears=arr, take=a["take"]))
    W.adults = rows


def _weights(W, seed):
    """design weights, then post-stratification to the Branch's population estimates by region, age group, sex (the
    estimates' own band-to-band variation comes from a stream of its own)"""
    rng = np.random.default_rng([seed, P.POP_SEED])
    psu_n = {}
    for a in W.addresses:
        psu_n[a["psu"]] = psu_n.get(a["psu"], 0) + 1
    # the population estimates (thousands, one decimal) by region, five-year band and sex
    pop = []
    for code, rr in W.reg.items():
        north = code in ("R01", "R02", "R03", "R04")
        tilt = np.linspace(1.12, 0.82, len(BANDS)) if north else np.linspace(0.97, 1.03, len(BANDS))
        sh = BAND_SHARE * tilt * np.exp(rng.normal(0, 0.03, len(BANDS)))
        sh = sh / sh.sum()
        for (lo, hi), s in zip(BANDS, sh):
            male = 0.505 - 0.09 * max(0, (lo - 60)) / 25
            for sex, f in ((1, male), (2, 1 - male)):
                pop.append(dict(region=code, band=(lo, hi), sex=sex, thousands=round(rr["adults"] * s * f / 1000, 1)))
    W.pop = pop
    cell_N = {}
    for r in pop:
        g = int(np.digitize(r["band"][0], P.AGE_CUTS))
        key = (r["region"], g, r["sex"])
        cell_N[key] = cell_N.get(key, 0.0) + r["thousands"] * 1000
    W.cell_N = cell_N
    for x in W.adults:
        x["d"] = x["take"] * 12.0 / psu_n[x["psu"]] * 1000.0
        x["cell"] = (x["region"], int(np.digitize(x["age"], P.AGE_CUTS)), x["sex"])
    tot = {}
    for x in W.adults:
        tot[x["cell"]] = tot.get(x["cell"], 0.0) + x["d"]
    W.empty_cells = [c for c in cell_N if c not in tot]
    for x in W.adults:
        x["w"] = x["d"] * cell_N[x["cell"]] / tot[x["cell"]]
