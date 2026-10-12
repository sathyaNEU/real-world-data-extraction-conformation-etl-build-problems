"""The ask layer: the students the places serve in 2027 by region, each hub's students and fortnightly road
kilometres, and the 2027 visit plan that assigns schools to hubs."""
import itertools

import numpy as np

import core

HUBS = "ABCDE"


def students(census, read="golden"):
    """2027 Year 3 to 6 students from the August 2026 census (columns F,1..6)."""
    if read == "golden":            # this year's Years 2 to 5 are next year's Years 3 to 6
        return census[:, 2:6].sum(1)
    if read == "natural":           # the census's own Years 3 to 6
        return census[:, 3:7].sum(1)
    if read == "half":              # the shift seen, this year's Year 6 kept
        return census[:, 2:7].sum(1)
    if read == "over":              # Years 3 to 5 only
        return census[:, 3:6].sum(1)
    raise ValueError(read)


def by_region(weight, values, region):
    return {r: float((weight * values)[region == r].sum()) for r in core.REGIONS}


def by_hub(weight, values, hub):
    return {h: float((weight * values)[hub == h].sum()) for h in HUBS}


def hub_km(weight, road, hub):
    k = np.array([HUBS.index(h) for h in hub])
    d = road[np.arange(len(hub)), k]
    return {h: float((weight * 2 * d)[hub == h].sum()) for h in HUBS}


def plan_hubs(W, p, stu, n_e=38, n_moves=7):
    """The 2027 visit plan: E takes the 38 schools nearest it by road (beyond its six pilots) from the hubs
    that served them, and seven schools move between hubs A to D where a second hub is about as close."""
    road = W["road"]
    dh = W["dir_hub"].copy()
    S = len(dh)
    cand = np.array([i for i in range(S) if dh[i] != "E"])
    near_e = cand[np.argsort(road[cand, 4], kind="stable")][:n_e]
    plan = dh.copy()
    plan[near_e] = "E"
    # candidate moves among A to D
    moves = []
    for i in range(S):
        if plan[i] == "E":
            continue
        cur = HUBS.index(plan[i])
        for k in range(4):
            if k != cur and road[i, k] <= 1.5 * road[i, cur] and road[i, k] >= 15:
                moves.append((i, HUBS[k]))
    return plan, near_e, moves


def choose_moves(W, plan0, moves, p, stu, n_moves=7, seed=0, points=None):
    """Pick seven moves so that every hub A to D changes by at least the floor in students and kilometres,
    best margin first (exhaustive over a shortlist)."""
    road = W["road"]
    dh = W["dir_hub"]
    base_s = by_hub(p, stu, dh)
    base_k = hub_km(p, road, dh)
    rng = np.random.default_rng(seed)
    best, best_val = None, -1
    idx = list(range(len(moves)))
    for trial in range(20000):
        pick = rng.choice(idx, size=n_moves, replace=False)
        schools = [moves[t][0] for t in pick]
        if len(set(schools)) < n_moves:
            continue
        plan = plan0.copy()
        for t in pick:
            plan[moves[t][0]] = moves[t][1]
        s1 = by_hub(p, stu, plan)
        k1 = hub_km(p, road, plan)
        val = min(min(abs(s1[h] - base_s[h]) / s1[h], abs(k1[h] - base_k[h]) / k1[h]) for h in "ABCD")
        lead = sorted(k1.values())
        if k1["E"] < 1.08 * lead[-2]:
            continue
        if points is not None:
            s2 = by_hub(points, stu, plan)
            k2 = hub_km(points, road, plan)
            val = min(val, min(min(abs(s2[h] - s1[h]) / s1[h], abs(k2[h] - k1[h]) / k1[h]) for h in HUBS))
        if val > best_val:
            best_val, best = val, sorted(int(t) for t in pick)
    plan = plan0.copy()
    for t in best:
        plan[moves[t][0]] = moves[t][1]
    return plan, [moves[t] for t in best], best_val


def _clear(x, unit=1.0, margin=0.2):
    """distance of x from its nearest rounding boundary, in units of the rounding step"""
    f = (x / unit) % 1.0
    return abs(f - 0.5)


def window(c, margin=0.2, top=0.45):
    """>= 0 when a figure clears its rounding boundary by `margin` of a step and is not on the round value"""
    return min(c - margin, top - c)


def boundary_swaps(W, p, margin=0.2, seed=0, points=None, stu=None):
    """Six regional shares, per cent to one decimal, each at least `margin` of a step from a boundary:
    move schools that sit on a regional boundary (the other region's centre about as near as their own)
    into the neighbouring region until every share clears."""
    w = W["w"]
    region = w["region"].copy()
    xy = w["xy"]
    G = p.sum()
    cand = []
    for i in range(len(region)):
        own = np.hypot(*(xy[i] - np.array(core.CENTRE[region[i]]))) / max(core.SPREAD[region[i]])
        for r in core.REGIONS:
            if r == region[i]:
                continue
            oth = np.hypot(*(xy[i] - np.array(core.CENTRE[r]))) / max(core.SPREAD[r])
            if oth <= 1.6 * own and oth < 3.0 and (r in core.METRO) == (region[i] in core.METRO):
                cand.append((i, r))
    rng = np.random.default_rng(seed)

    def score(reg):
        sh = [100 * p[reg == r].sum() / G for r in core.REGIONS]
        sc = min(window(_clear(s, 0.1), margin) for s in sh)
        if points is not None:
            g = by_region(p, stu, reg)
            q = by_region(points, stu, reg)
            sc = min(sc, min(abs(q[r] - g[r]) / g[r] - 0.035 for r in core.REGIONS))
        return sc
    best, best_reg = score(region), region
    if best >= 0:
        return region, []
    for trial in range(80000):
        k = int(rng.integers(1, 6))
        pick = rng.choice(len(cand), size=k, replace=False)
        if len({cand[t][0] for t in pick}) < k:
            continue
        reg = region.copy()
        for t in pick:
            reg[cand[t][0]] = cand[t][1]
        s = score(reg)
        if s > best + 1e-12:
            best, best_reg, chosen = s, reg, [cand[t] for t in pick]
            if best >= 0:
                return best_reg, chosen
    raise AssertionError("no boundary swap set clears the shares: %.3f" % best)


def tune_census(W, p, plan, region, margin=0.2, seed=0):
    """Centre the students figures (six regions, five hubs, the total) in their whole-number bins by small
    differences in schools' Year 2 headcounts (the census is drawn, so any draw is as real as another)."""
    census = W["census"]
    rng = np.random.default_rng(seed)

    def figs(c):
        st = students(c)
        out = list(by_region(p, st, region).values()) + list(by_hub(p, st, plan).values()) + [float((p * st).sum())]
        return out

    def score(c):
        f = figs(c)
        return min(window(_clear(x), margin) for x in f) if int(round(f[-1])) % 10 else -1.0
    if score(census) >= 0:
        return census, []
    pool = np.where(p > 0.02)[0]
    for trial in range(200000):
        k = int(rng.integers(3, 13))
        pick = rng.choice(pool, size=k, replace=False)
        d = rng.integers(-6, 7, size=k)
        c = census.copy()
        c[pick, 2] = np.maximum(2, c[pick, 2] + d)
        if score(c) >= 0:
            return c, [(int(i), int(x)) for i, x in zip(pick, d)]
    raise AssertionError("census tuning failed")


def tune_roads(W, p, plan, margin=0.2, seed=0):
    """Centre each hub's fortnightly kilometres and their total by a kilometre or two on a few schools'
    one-way distances from their 2027 hub."""
    road = W["road"]
    rng = np.random.default_rng(seed)

    def score(rd):
        k = hub_km(p, rd, plan)
        if int(round(sum(k.values()))) % 10 == 0:
            return -1.0
        return min(window(_clear(x), margin) for x in list(k.values()) + [sum(k.values())])
    if score(road) >= 0:
        return road, []
    pool = np.where(p > 0.02)[0]
    hk = np.array([HUBS.index(h) for h in plan])
    for trial in range(200000):
        k = int(rng.integers(2, 8))
        pick = rng.choice(pool, size=k, replace=False)
        d = rng.integers(-2, 3, size=k)
        rd = road.copy()
        rd[pick, hk[pick]] = np.maximum(3, rd[pick, hk[pick]] + d)
        if score(rd) >= 0:
            return rd, [(int(i), int(x)) for i, x in zip(pick, d)]
    raise AssertionError("road tuning failed")
