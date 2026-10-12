"""Centring moves on the true timeline: a few deaths shortly before or after 31 December 2026 moved across it, so
every quarter-end figure of the canonical forecast sits near the middle of its rounding bin (nearest 10). Each move
is one resident whose death is dated a few weeks earlier or later; nothing else in the timeline changes."""
import itertools

import numpy as np

import estimators as E
import world as W

CENTRES = None


def target(g):
    return np.round(g / 10.0) * 10.0


def vectors(fitres):
    """the change in the four totals from one more council-funded resident in place on 31 December 2026 (by
    duration), and from one more self-funder in the pool (by duration)"""
    o, HX, HC, HS = fitres["o"], fitres["HX"], fitres["HC"], fitres["HS"]
    qm = E.qmonths("days")

    def cf(d):
        return np.array([np.exp(-(HX[0].H(np.array([d + q]))[0] - HX[0].H(np.array([d]))[0])) for q in qm])

    def sf(d):
        out = np.zeros(4)
        s, t, h = 1.0, 0.0, 0.1
        while t < qm[-1] - 1e-9:
            lc, lx = HC.at(np.array([d + t]))[0], HS.at(np.array([d + t]))[0]
            tot = lc + lx
            p = s * lc / tot * (1 - np.exp(-tot * h)) if tot > 0 else 0.0
            mid = t + h / 2
            for k in range(4):
                if mid < qm[k]:
                    out[k] += p * np.exp(-(HX[0].H(np.array([d + qm[k]]))[0] - HX[0].H(np.array([d + mid]))[0]))
            s *= np.exp(-tot * h)
            t += h
        return out
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
        cf = S.kind[i] == 0 or S.conv[i] <= A
        sf = S.kind[i] == 1 and not S.conv[i] <= A
        if A - 45 <= e < A - 3 and S.admit[i] < A - 60:
            # died shortly before: moving the death to the spring brings the resident into the as-of count
            out["cf_in" if cf else "sf_in"].append((i, dur))
        elif A + 3 < e <= A + 45 and S.admit[i] < A - 60 and (S.kind[i] == 0 or S.conv[i] < A - 45 or sf):
            out["cf_out" if cf else "sf_out"].append((i, dur))
    return out


def plan(g, fitres, S, extra=None):
    """the integer mix of moves that brings every figure closest to its bin centre"""
    cf, sf = vectors(fitres)
    C = candidates(S)
    tgt = target(g) if extra is None else extra
    r = tgt - g
    groups = []
    for key, sign in (("cf_in", 1), ("cf_out", -1)):
        lst = sorted(C[key], key=lambda x: -x[1])
        groups.append((key, sign, [(i, sign * cf(d)) for i, d in lst[:8] if d > 6]))
    for key, sign in (("sf_in", 1), ("sf_out", -1)):
        for lo, hi in ((10, 17), (17, 26), (26, 40)):
            lst = [(i, d) for i, d in C[key] if lo <= d < hi]
            groups.append((key + "%d" % lo, sign, [(i, sign * sf(d)) for i, d in lst[:6]]))
    best = None
    pools = [g_ for g_ in groups if g_[2]]
    ranges = [range(0, min(len(p[2]), 3) + 1) for p in pools]
    for combo in itertools.product(*ranges):
        if sum(combo) > 8:
            continue
        v = np.zeros(4)
        for n, p in zip(combo, pools):
            for k in range(n):
                v += p[2][k][1]
        err = np.abs(r - v).max()
        cost = err + 0.02 * sum(combo)
        if best is None or cost < best[0]:
            best = (cost, combo, err)
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


def centre(S, evaluate, rounds=3):
    """evaluate(S) gives the canonical forecast from the observed files and the fitted hazards"""
    done = []
    for _ in range(rounds):
        g, fitres = evaluate(S)
        r = target(g) - g
        if np.abs(r).max() <= 0.6:
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
            short = [i for i, d in C[key] if d < 6 and i not in used]
            if short:
                mv = [(key + "_short", short[0])]
                apply(S, mv)
                done += mv
                break
    return done
