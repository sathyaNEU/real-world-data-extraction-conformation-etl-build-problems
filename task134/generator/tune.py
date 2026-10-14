"""Centring moves on the true timeline: a few deaths shortly before or after 31 December 2026 moved across it, so
every quarter-end figure of the canonical forecast sits near the middle of its rounding bin (nearest 10). Each move
is one resident whose death is dated a few weeks earlier or later; nothing else in the timeline changes."""
import datetime as dt
import itertools

import numpy as np

import estimators as E
import world as W

CENTRES = None


# where each quarter end's figure sits against its bin centre: the golden family runs from about 2.6 below the canonical
# figure to about 2 above it, and the forecast rises about 9, 7 and 4 a quarter, so the widest room for the whole family
# at every date is with the figures about 1.7, 1.0, -1.8 and 2.2 from their bin centres
OFFSETS = np.array([1.7, 1.0, -1.8, 2.2])
TOL = 0.6


def target(g):
    return np.round((g - OFFSETS) / 10.0) * 10.0 + OFFSETS


def vectors(fitres):
    """the change in the four totals from one more council-funded resident in place on 31 December 2026 (by
    duration), and from one more self-funder in the pool (by duration, and whether they were in the pool on 6 April
    2026), under the canonical forecast"""
    o, HX, HC, HS = fitres["o"], fitres["HX"], fitres["HC"], fitres["HS"]
    qm = E.qmonths("days")
    a1 = fitres["w1"] * 7 / W.MONTH

    def cf(d):
        return np.array([np.exp(-(HX[0].H(np.array([d + q]))[0] - HX[0].H(np.array([d]))[0])) for q in qm])

    def sf(d, pre):
        return E.project_members(np.array([float(d)]), np.array([a1 if pre else 0.0]), np.array([0]), o, HX, HC, HS,
                                 fitres["w2"]).sum(axis=1)
    return cf, sf


def candidates(S):
    """residents whose death falls within 45 days either side of the as-of date"""
    A = W.ASOF
    out = {"cf_in": [], "cf_out": [], "sf_in": [], "sf_out": []}
    for i in range(S.n):
        if S.why[i] != 1 or not np.isfinite(S.exit[i]):
            continue
        e = S.exit[i]
        dur = (A - S.admit[i]) / W.MONTH
        pre = bool(S.admit[i] < W.STAGE1)
        cf = S.kind[i] == 0 or S.conv[i] <= A
        sf = S.kind[i] == 1 and not S.conv[i] <= A
        if A - 45 <= e < A - 3 and S.admit[i] < A - 60:
            # died shortly before: moving the death to the spring brings the resident into the as-of count
            out["cf_in" if cf else "sf_in"].append((i, dur, pre))
        elif A + 3 < e <= A + 45 and S.admit[i] < A - 60 and (S.kind[i] == 0 or S.conv[i] < A - 45 or sf):
            out["cf_out" if cf else "sf_out"].append((i, dur, pre))
    return out


def plan(g, fitres, S, extra=None):
    """the integer mix of moves that brings every figure nearest its target (OFFSET above the bin centre)"""
    cf, sf = vectors(fitres)
    C = candidates(S)
    tgt = target(g) if extra is None else extra
    r = tgt - g
    groups = []
    for key, sign in (("cf_in", 1), ("cf_out", -1)):
        lst = sorted(C[key], key=lambda x: -x[1])
        groups.append((key, sign, [(i, sign * cf(d)) for i, d, pre in lst[:8] if d > 6]))
    for key, sign in (("sf_in", 1), ("sf_out", -1)):
        for lo, hi in ((10, 17), (17, 26), (26, 40)):
            lst = [(i, d, pre) for i, d, pre in C[key] if lo <= d < hi]
            groups.append((key + "%d" % lo, sign, [(i, sign * sf(d, pre)) for i, d, pre in lst[:6]]))
    pools = [g_ for g_ in groups if g_[2]]
    ranges = [range(0, min(len(p[2]), 4) + 1) for p in pools]
    best = None
    for combo in itertools.product(*ranges):
        if sum(combo) > 10:
            continue
        v = np.zeros(4)
        for n, p in zip(combo, pools):
            for k in range(n):
                v += p[2][k][1]
        dev = np.abs(r - v)
        cost = np.clip(dev - TOL, 0, None).sum() * 10 + dev.max() + 0.02 * sum(combo)
        if best is None or cost < best[0]:
            best = (cost, combo, dev.max())
    moves = []
    for n, p in zip(best[1], pools):
        for k in range(n):
            moves.append((p[0], p[2][k][0]))
    return moves, best[2]


def apply(S, moves):
    A = W.ASOF
    for key, i in moves:
        if key.endswith("in") or "_in" in key:
            # the death moves from late 2026 into the following spring or summer
            S.exit[i] = A + 100 + (i % 97)
        else:
            S.exit[i] = A - 20 - (i % 17)
        if np.isfinite(S.conv[i]) and S.conv[i] >= S.exit[i]:
            S.conv[i] = np.inf
    return S


def centre(S, evaluate, rounds=4):
    """evaluate(S) gives the canonical forecast from the observed files and the fitted hazards"""
    done = []
    for _ in range(rounds):
        g, fitres = evaluate(S)
        r = target(g) - g
        if np.abs(r).max() <= TOL:
            break
        moves, err = plan(g, fitres, S)
        moves = [m for m in moves if m[1] not in {x[1] for x in done}]
        apply(S, moves)
        done += moves
    # a round pool count reads as made up: one self-funder in their first months, whose death sat a few days either
    # side of the as-of date, moves across it (this changes no figure by as much as 0.01)
    g, fitres = evaluate(S)
    if fitres["n_sf"] % 10 == 0:
        C = candidates(S)
        used = {x[1] for x in done}
        for key in ("sf_in", "sf_out"):
            short = [i for i, d, pre in C[key] if d < 6 and i not in used]
            if short:
                mv = [(key + "_short", short[0])]
                apply(S, mv)
                done += mv
                break
    return done


# ------------------------------------------------------------------------------------------------ the ordinary flow
# The 6 April 2026 conversions are read against an ordinary week's. A few conversion dates in the year either side of
# that day are moved by a few weeks so that every natural window for the ordinary week (the 4, 8, 12, 13, 26 and 52
# weeks before, the 8, 12 and 26 weeks after, calendar 2025) gives the same flow as the fitted hazard does, within
# counting: the measured stage-1 response then does not depend on the window.

WINDOWS_BEFORE = (4, 8, 12, 13, 26, 52)
WINDOWS_AFTER = (8, 12, 26)


def window_counts(c):
    D1 = W.STAGE1
    out = {}
    for k in WINDOWS_BEFORE:
        out[("b", k)] = int(((c >= D1 - 7 * k) & (c < D1)).sum())
    for k in WINDOWS_AFTER:
        out[("a", k)] = int(((c > D1) & (c <= D1 + 7 * k)).sum())
    a0, a1 = W.dn(dt.date(2025, 1, 1)), W.dn(dt.date(2026, 1, 1))
    out[("y", 2025)] = int(((c >= a0) & (c < a1)).sum())
    return out


def flow_obj(c, f):
    obj = 0.0
    for (kind, k), n in window_counts(c).items():
        wk = 365.0 / 7 if kind == "y" else k
        e = f * wk
        obj += (n - e) ** 2 / e
    return obj


def flow_moves(S, f, max_moves=14):
    """greedy moves of single conversion dates (never across 6 April 2026, never onto it, never before 15 months
    since admission or after the resident's exit) towards an ordinary week of f conversions in every window"""
    D1 = W.STAGE1
    sf = (S.kind == 1) & np.isfinite(S.conv)
    idx = np.where(sf & (S.conv >= D1 - 420) & (S.conv <= D1 + 200) & (S.conv != D1))[0]
    upr = {W.uprate_day(y) for y in range(2019, 2028)}
    deltas = [-56, -42, -35, -28, -21, -14, -7, 7, 14, 21, 28, 35, 42, 56]
    moves = []
    for _ in range(max_moves):
        c_all = S.conv[sf]
        base = flow_obj(c_all, f)
        best = None
        pos = {i: k for k, i in enumerate(np.where(sf)[0])}
        for i in idx:
            if any(m[0] == i for m in moves):
                continue
            c0 = S.conv[i]
            for dl in deltas:
                c1 = c0 + dl
                if c1 in upr or (c0 < D1) != (c1 < D1) or c1 == D1:
                    continue
                if c1 >= S.exit[i] or c1 - S.admit[i] < 15 * W.MONTH or c1 >= W.ASOF - 30 or c1 <= W.HIST_START:
                    continue
                c_all[pos[i]] = c1
                v = flow_obj(c_all, f)
                c_all[pos[i]] = c0
                if best is None or v < best[0]:
                    best = (v, int(i), float(c0), float(c1))
        if best is None or best[0] > base - 0.05:
            break
        S.conv[best[1]] = best[3]
        moves.append((best[1], best[2], best[3]))
    return moves


def apply_flow(S, moves):
    for i, c0, c1 in moves:
        assert S.conv[i] == c0
        S.conv[i] = c1
    return S
