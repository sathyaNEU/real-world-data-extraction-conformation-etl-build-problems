"""The golden and its rivals on the clean truth.

Golden: each case's own incubation window laid over the supply path its zone actually had on each day,
read from the operations through the network; each asset's attack rate is the cases its water carried per
100,000 resident-days it served over the window. Rivals: the register, the onset-day path, the dated event,
the nearest reservoir, the per-record cells, the literal WHAT.
"""
import numpy as np

import world

WIN_FROM = 62     # 1 September 2027 (day index), the outbreak review window opens
ONSET_TO = world.NDAYS - 1


def in_window(c, lo=WIN_FROM):
    return lo <= c['onset'] <= ONSET_TO


def assets(W):
    a = set(world.RES) | set(world.ICS) | {world.ZONES[z][1] for z in world.ZONES}
    return sorted(a)


def served(W, lo=WIN_FROM, hi=ONSET_TO):
    """Resident-days each asset's water reached, days lo..hi."""
    S = {k: 0.0 for k in assets(W)}
    for d in range(lo, hi + 1):
        for z, pth in W['P'][d].items():
            if pth:
                for k in pth:
                    S[k] += W['pop'][z]
    return S


def golden(W, kmin=1, kmax=14, weights='pmf', lo=WIN_FROM, case_lo=None):
    """Attack rate per asset: incubation-weighted cases per 100,000 resident-days served."""
    inc = W['inc'] if weights == 'pmf' else None
    A = {k: 0.0 for k in assets(W)}
    case_lo = lo + 7 if case_lo is None else case_lo
    for c in W['cases']:
        if not (case_lo <= c['onset'] <= ONSET_TO):
            continue
        ks = list(range(kmin, kmax + 1))
        w = np.array([inc[k - 1] if inc is not None and k - 1 < len(inc) else 1.0 for k in ks])
        w = w / w.sum()
        for k, wk in zip(ks, w):
            d = c['onset'] - k
            if d < 0:
                continue
            pth = W['P'][d][c['zone']]
            if pth:
                for a in pth:
                    A[a] += wk
    S = served(W, lo, ONSET_TO)
    return {k: (A[k] / S[k] * 1e5 if S[k] > 0 else 0.0) for k in A}, A, S


def top(rates):
    s = sorted(rates.items(), key=lambda kv: -kv[1])
    lead = s[0][1] / s[1][1] if s[1][1] > 0 else float('inf')
    return s[0][0], lead, s[1][0]


def register_rates(W):
    """Rung 0/1: attack rate per reservoir through the supply-zone register."""
    pop = W['pop']
    cases = {r: 0 for r in world.RES}
    res = {r: 0.0 for r in world.RES}
    for z in world.ZONES:
        r = home(z)
        res[r] += pop[z]
    for c in W['cases']:
        if in_window(c):
            cases[home(c['zone'])] += 1
    return {r: cases[r] / res[r] * 1e5 for r in world.RES}


def home(z):
    p = world.ZONES[z][0]
    return p if p in world.RES else home(p)


def first_look(W):
    cnt = {}
    for c in W['cases']:
        if in_window(c):
            cnt[c['zone']] = cnt.get(c['zone'], 0) + 1
    z = max(cnt, key=cnt.get)
    return home(z)


def onset_path(W):
    """Constructing reader: the path the case's zone had on the onset day."""
    A = {k: 0.0 for k in assets(W)}
    for c in W['cases']:
        if in_window(c):
            pth = W['P'][c['onset']][c['zone']]
            if pth:
                for a in pth:
                    A[a] += 1
    S = served(W)
    return {k: (A[k] / S[k] * 1e5 if S[k] else 0.0) for k in A}


def report_path(W):
    A = {k: 0.0 for k in assets(W)}
    for c in W['cases']:
        if in_window(c):
            pth = W['P'][min(c['report'], world.NDAYS - 1)][c['zone']]
            if pth:
                for a in pth:
                    A[a] += 1
    S = served(W)
    return {k: (A[k] / S[k] * 1e5 if S[k] else 0.0) for k in A}


def dated_event(W):
    """Constructing reader: the last repair on the worst zone's own supply before its first case."""
    cnt = {}
    first = {}
    for c in W['cases']:
        if in_window(c) and c['kind'] == 'outbreak' or in_window(c):
            cnt[c['zone']] = cnt.get(c['zone'], 0) + 1
    z = max(cnt, key=cnt.get)
    onsets = sorted(c['onset'] for c in W['cases'] if c['zone'] == z and in_window(c))
    peak = int(np.median(onsets))
    chain = []
    q = z
    while q not in world.RES:
        chain.append(world.ZONES[q][1])
        q = world.ZONES[q][0]
    best = None
    for m, f, l, bf in W['reps']:
        if m in chain and peak - 21 <= f <= peak:
            best = m if best is None or f > best[1] else best
            best = (m, f)
    return best[0] if best else home(z)


def nearest_reservoir(W):
    xs, ys = [], []
    for c in W['cases']:
        if in_window(c):
            _, _, _, x, y = world.ZONES[c['zone']]
            xs.append(x)
            ys.append(y)
    cx, cy = np.mean(xs), np.mean(ys)
    return min(world.RES, key=lambda r: (world.RES_XY[r][0] - cx) ** 2 + (world.RES_XY[r][1] - cy) ** 2)


def cluster_nearest(W):
    """Spatial cluster of the two worst zones by rate, then the nearest reservoir to it."""
    pop = W['pop']
    cnt = {z: 0 for z in world.ZONES}
    for c in W['cases']:
        if in_window(c):
            cnt[c['zone']] += 1
    rate = {z: cnt[z] / pop[z] for z in world.ZONES}
    top2 = sorted(rate, key=lambda z: -rate[z])[:2]
    cx = np.mean([world.ZONES[z][3] for z in top2])
    cy = np.mean([world.ZONES[z][4] for z in top2])
    return min(world.RES, key=lambda r: (world.RES_XY[r][0] - cx) ** 2 + (world.RES_XY[r][1] - cy) ** 2)


def per_record_cells(W, width=7):
    """Per-record reader: zone-by-week cells on every joinable attribute, Poisson main effects; the asset it
    names is the register reservoir with the largest fitted effect (the network operations join to nothing)."""
    pop = W['pop']
    weeks = (world.NDAYS - WIN_FROM) // width + 1
    Y = {}
    for c in W['cases']:
        if in_window(c):
            key = (c['zone'], (c['onset'] - WIN_FROM) // width)
            Y[key] = Y.get(key, 0) + 1
    eff = {}
    for r in world.RES:
        num = sum(v for (z, w), v in Y.items() if home(z) == r)
        den = sum(pop[z] for z in world.ZONES if home(z) == r) * weeks
        eff[r] = num / den
    return max(eff, key=eff.get)
