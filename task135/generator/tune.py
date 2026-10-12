"""The world the pack is cut from: the market seed, the monthly polish, and the call conditions the seed scan keeps.

polish: each market's month-on-month moves inside the window are re-scaled by a drift spread over the month's market
hours, so every holding's monthly volatility sits between its daily and five-day volatilities (the design note's
single-holding agreement); daily and five-day returns are moved by a constant within each month only.
"""
import datetime as dt
import sys

import numpy as np

import world as W
import sim as SM
import book as BK
import estimators as E

KEY = {"MAND": "UK", "NAEF": "US", "EUEF": "EU", "JPEF": "JP", "GILT": "RATES", "CORP": "CREDIT"}


def returns(M, B, fp):
    fr = BK.fund_returns(fp, M, B.days)
    R = {"MAND": B.r_mand, **fr}
    return E.mat(R), B.days[1:]


def index_returns(M, days):
    R = {}
    for h, k in zip(W.HOLDINGS, ["UK", "US", "EU", "JP", "GILT", "CORP"]):
        dd, v = M["index"][k]
        pos = {d: i for i, d in enumerate(dd)}
        out = []
        for d in days:
            e = d
            while e not in pos:
                e -= dt.timedelta(days=1)
            out.append(v[pos[e]])
        R[h] = np.exp(np.diff(np.array(out))) - 1
    return E.mat(R)


def build_world(mseed, iters=4, keep_rows=False, start_total=None, knobs=None):
    drift = {k: {} for k in SM.DRIFT_KEYS}
    for it in range(iters + 1):
        M = SM.market(mseed, drift=drift)
        fp = SM.fund_prices(M, np.random.default_rng(W.SEED + 5))
        B = BK.run(M, W.SEED, fp, keep_rows=keep_rows and it == iters, start_total=start_total, knobs=knobs)
        X, dates = returns(M, B, fp)
        if it == iters:
            break
        mo = E.months(X, dates)
        keys = sorted({(d.year, d.month) for d in dates})
        for j, h in enumerate(W.HOLDINGS):
            dv = E.vol_of(X[:, j], 252)
            wv = E.vol_of(E.blocks(X, 5)[:, j], 52)
            mv = E.vol_of(mo[:, j], 12)
            c = (0.5 * (dv + wv)) / mv
            L = np.log1p(mo[:, j])
            dev = (c - 1) * (L - L.mean())
            load = 0.97 if h == "MAND" else 1.0
            for (y, m), x in zip(keys, dev):
                drift[KEY[h]][(y, m)] = drift[KEY[h]].get((y, m), 0.0) + x / load
    return M, fp, B, X, dates, drift


def conditions(X, dates, Xi, m=0.15):
    T = E.table(X, dates, [20, 30, 40, 50, 60, 70, 80, 90, 100])
    c = {}
    r0 = T["R0 daily"]
    c["R0"] = (r0[70] <= 10 - m and r0[80] >= 10 + m and r0[70] * np.sqrt(260 / 252) < 10 - 0.02
               and r0[80] * np.sqrt(250 / 252) > 10 + 0.02)
    gold = {n: v for n, v in T.items() if E.GOLDEN(n)}
    c["G"] = all(v[60] <= 10 - m and v[70] >= 10 + m for v in gold.values())
    # the weekly members on the window's own count of periods a year and on 52.18
    wk = [n for n in gold if "five-day" in n and "blocks" in n or "calendar" in n]
    ok = True
    for n in wk:
        for py in (50.5, 52.18):
            f = np.sqrt(py / 52.0)
            ok &= gold[n][60] * f <= 10 - 0.02 and gold[n][70] * f >= 10 + 0.02
    c["G-scale"] = ok
    c["G-mono"] = all(all(np.diff([v[s] for s in W.STEPS]) > 0) for v in T.values())
    c["P"] = all(v[60] <= 10 - 0.05 and v[70] >= 10 + 0.05 for n, v in T.items() if E.PARTIAL(n))

    def offcall(v):
        cl = E.call(v)
        if cl in (None, 60):
            return False
        return v[cl] <= 10 - m and (cl + 10 not in v or v[cl + 10] >= 10 + m)
    c["R1"] = offcall(T["R1 ewma 0.94"])
    r2 = {s: E.simple(Xi, s) for s in W.STEPS}
    c["R2"] = offcall(r2)
    c["R3"] = E.call(T["R3 ledoit-wolf"]) == 70 and offcall(T["R3 ledoit-wolf"])
    ac, t = E.autocorr1(X, 60)
    c["ac"] = 0.17 <= ac <= 0.26 and t >= 3.5
    s, nx, wkc = E.uk_na(X)
    c["ukna"] = 0.20 <= s <= 0.35 and nx >= 0.40 and wkc >= 0.45
    sv = E.single_vols(X, dates)
    c["single"] = all(max(v) / min(v) <= 1.12 for v in sv.values())
    c["cap-gap"] = all(abs(v[s] - 10) >= m for v in gold.values() for s in W.STEPS)
    return c, T, r2


def scan(a, b):
    good = []
    for seed in range(a, b):
        try:
            M, fp, B, X, dates, drift = build_world(seed, iters=3)
        except Exception as ex:          # a seed whose book cannot be run is skipped
            print(seed, "error", ex)
            continue
        c, T, r2 = conditions(X, dates, index_returns(M, B.days))
        if all(c.values()):
            import grants as GR
            import files as FL
            import ladder as LD
            M, fp, B, X, dates, drift = build_world(seed, iters=3, keep_rows=True)
            g, i = GR.make(117, {"scale": 1.2})
            p = GR.settle(g, i, 117, {})
            F = FL.frames(M, fp, B, g, i, p, 117)
            bad = LD.slip_ok(LD.slip_grid(F))
            if bad:
                print(seed, "slips", bad, flush=True)
                continue
            good.append(seed)
            print("PASS", seed, flush=True)
        else:
            print(seed, " ".join(k for k, v in c.items() if not v), flush=True)
    return good


if __name__ == "__main__":
    print(scan(int(sys.argv[1]), int(sys.argv[2])))
