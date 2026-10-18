"""Tuning (not part of the build): choose each faulting analyser's fault multiplier and draw, and each long outage's
window, so that the ladder's margins hold under every reading. Prints the values to freeze into params.py."""
import sys

import numpy as np

import estim as E
import params as P
import sim as S


def world():
    W = S.weather()
    BG = S.background(W=W)
    n = len(P.STATIONS)
    scales = [S.fit_scale(W, BG, i) for i in range(n)]
    X = np.array([S.pm10(W, BG, i, scales[i]) for i in range(n)])
    return W, BG, X, scales


def gap_window(xd, n, xh=None, avoid=None):
    """the long outage's window: lengths n to n + 30 days starting between days 20 and 300, the fewest days above 50
    inside, ending into a dusty day whose first hour is already dusty; the longest such window wins ties (avoid: another
    outage's (start, length); this one starts and ends at least 30 days from it)"""
    best = None
    for L in range(n, n + 31, 2):
        a = np.convolve((xd > 50).astype(float), np.ones(L), "valid")
        for s in range(20, 300):
            e = s + L
            if avoid and (abs(s - avoid[0]) < 30 or abs(e - avoid[0] - avoid[1]) < 30):
                continue
            if e < len(xd) and xd[e] > 55:
                key = (a[s], -L, s)
                if best is None or key < best:
                    best = key
    return (int(best[2]), -int(best[1]))


def scan_window(X, W, gaps, i):
    """a long outage's window, starting and ending at least 25 days from any outage already placed: the lowest highest
    rebuilt count, then the highest scaled count, then the earliest start"""
    mult = [P.FAULT_MULT.get(c, 1.0) for c in P.CODES]
    seed = [P.FAULT_SEED.get(c, 0) for c in P.CODES]
    trial = dict(gaps)
    trial[i] = (20, P.STATIONS[i][10])
    base = S.outages(X, mult, seed, trial)
    best = None
    for s in range(20, 300, 3):
        for L in range(84, 132, 4):
            e = s + L
            if e >= P.DAYS or any(abs(s - s0) < 25 or abs(e - s0 - l0) < 25 for s0, l0 in gaps.values()):
                continue
            trial[i] = (s, L)
            cause = S.outages(X, mult, seed, trial, only=[i], base=base)
            R = E.readings(X, cause == "", W, which="rungs", only=[i])
            if not (R["pro_rata"][i] >= 36.6 and R["valid_days"][i] <= 31):
                continue
            R = E.readings(X, cause == "", W, only=[i])
            key = (max(R[k][i] for k in R if k.startswith("wind")), -R["pro_rata"][i], s, L)
            if best is None or key < best:
                best = key
    return (best[2], best[3])


def shifted_min(X, valid, W, i):
    """the station's lowest wind-aware count with its hours placed one hour late or one hour early on the grid (a clock
    read wrongly)"""
    out = []
    for step in (1, -1):
        X2, v2 = X.copy(), valid.copy()
        X2[i], v2[i] = np.roll(X[i], step), np.roll(valid[i], step)
        v2[i][0 if step == 1 else -1] = False
        R = E.readings(X2, v2, W, only=[i])
        out.append(min(R[k][i] for k in R if k.startswith("wind")))
    return min(out)


def ok_station(R, i, stage="full"):
    """the station's own margins: plume stations noted under every wind-aware rebuild and by no easy route (scaling,
    the 90.4th percentile, interpolation in time, the network alone); quiet-gap stations noted by scaling and by no
    wind-aware rebuild; the rest clear (stage 'rungs': the easy routes only)"""
    role = P.STATIONS[i][13]
    get = lambda k: R[k][i]
    net = [R[k][i] for k in R if k.startswith("net_")]
    p904 = [R[k][i] for k in R if k.startswith("p904")]
    interp = [R[k][i] for k in R if k.startswith("interp")]
    wind = [R[k][i] for k in R if k.startswith("wind")] if stage == "full" else []
    if role == "F":
        easy = (get("valid_days") <= 31 and get("pro_rata") <= 33.5 and get("pro_rata_month") <= 33.5
                and max(p904) < 49.5 and max(net) <= 33 and max(interp) <= 33)
        return easy and (stage != "full" or min(wind) >= 38)
    if role == "Q":
        return get("pro_rata") >= 36.6 and get("valid_days") <= 31 and (stage != "full" or max(wind) <= 33)
    if role == "E":
        return get("valid_days") >= 38
    return max(wind + [get("pro_rata")]) <= 31


def rung_calls(R):
    """each easy route's call, as a set, and the golden family's"""
    n = len(P.CODES)
    out = {}
    for k in R:
        if k == "valid_days" or k.startswith("wind"):
            continue
        if k.startswith("p904"):
            noted = [P.CODES[i] for i in range(n) if R["valid_days"][i] <= 35 and R[k][i] > 50]
        else:
            noted = [P.CODES[i] for i in range(n) if R["valid_days"][i] <= 35 and R[k][i] > 35]
        out[k] = noted
    return out


if __name__ == "__main__":
    W, BG, X, scales = world()
    n = len(P.STATIONS)
    xd = X.reshape(n, P.DAYS, 24).mean(2)
    gaps = {}
    for i in [i for i in range(n) if P.STATIONS[i][10]]:
        gaps[i] = scan_window(X, W, gaps, i)
    mult = [1.0] * n
    seed = [0] * n
    F = [i for i in range(n) if P.STATIONS[i][13] == "F"]
    base = S.outages(X, mult, seed, gaps)
    for rnd in range(2):
        for i in F:
            best = None
            for m in (1.0, 0.85, 0.7, 0.55, 0.4):
                for sd in range(12):
                    mult[i], seed[i] = m, sd
                    cause = S.outages(X, mult, seed, gaps, only=[i], base=base)
                    R = E.readings(X, cause == "", W, which="rungs", only=[i])
                    if not ok_station(R, i, "rungs"):
                        continue
                    R = E.readings(X, cause == "", W, only=[i])
                    if not ok_station(R, i):
                        continue
                    sh = shifted_min(X, cause == "", W, i)
                    if sh < 36:
                        continue
                    wind = min(R[k][i] for k in R if k.startswith("wind"))
                    easy = max(R[k][i] for k in R if k.startswith("interp") or k.startswith("net_"))
                    key = min(wind - 37, sh - 36, 33 - easy)
                    if best is None or key > best[0]:
                        best = (key, m, sd)
            if best:
                mult[i], seed[i] = best[1], best[2]
            base = S.outages(X, mult, seed, gaps, only=[i], base=base)
            print("round", rnd, P.CODES[i], "->", best and best[1:], "margin", best and best[0], flush=True)
    valid = S.outages(X, mult, seed, gaps) == ""
    R = E.readings(X, valid, W)
    bad = [P.CODES[i] for i in range(n) if not ok_station(R, i)]
    print("bad", bad)
    print("FAULT_MULT =", {P.CODES[i]: mult[i] for i in range(n) if P.STATIONS[i][9]})
    print("FAULT_SEED =", {P.CODES[i]: seed[i] for i in range(n) if P.STATIONS[i][9]})
    print("GAP_START =", {P.CODES[i]: g for i, g in gaps.items()})
    for i in range(n):
        wind = [R[k][i] for k in R if k.startswith("wind")]
        net = [R[k][i] for k in R if k.startswith("net_")]
        hyb = [R[k][i] for k in R if k.startswith("interp_hybrid")]
        print("%-5s %s M %d pro %.1f/%.1f int %d/%d hyb %d-%d net %d-%d wind %d-%d" % (
            P.CODES[i], P.STATIONS[i][13], R["valid_days"][i], R["pro_rata"][i], R["pro_rata_month"][i], R["interp_daily"][i],
            R["interp_hourly"][i], min(hyb), max(hyb), min(net), max(net), min(wind), max(wind)))
    gold = sorted(P.CODES[i] for i in range(n) if P.STATIONS[i][13] == "F")
    for k, v in rung_calls(R).items():
        print("rung %-24s %s%s" % (k, ",".join(v), "   <- LANDS THE CALL" if sorted(v) == gold else ""))
