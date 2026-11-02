"""Design-time measurement on the clean truth (not shipped logic): the default path, the golden family and the
over-correction for the three 2027 schedules, so the world's free parameters can be set before any file is cut.

    python3 tune.py [seed]
"""
import math
import sys
from collections import Counter, defaultdict

import numpy as np

import params as P
import world


def card_table(W):
    rows = []   # (mh, trade_factor, mhw_conc, mhw_conc_mh, mhw_conc_day, mhw_conc_aircraft, defects)
    for ch in W.checks:
        ses = ch["sessions"]
        cards = ch["cards"]
        mh_area_shift = defaultdict(float)
        n_day = Counter()
        n_all = Counter()
        for s in ses:
            a = cards[s["card"]]["area"]
            mh_area_shift[(a, s["shift_idx"])] += s["hours"]
            n_day[(a, s["shift_idx"] // 2)] += 1
            n_all[s["shift_idx"]] += 1
        agg = defaultdict(lambda: [0.0, 0.0, 0.0, 0.0, 0.0])
        for s in ses:
            a = cards[s["card"]]["area"]
            g = agg[s["card"]]
            g[0] += s["hours"]
            g[1] += s["hours"] * s["n_other"]
            g[2] += s["hours"] * (mh_area_shift[(a, s["shift_idx"])] - s["hours"])
            g[3] += s["hours"] * (n_day[(a, s["shift_idx"] // 2)] - 1)
            g[4] += s["hours"] * (n_all[s["shift_idx"]] - 1)
        for ci, g in agg.items():
            c = cards[ci]
            rows.append((g[0], P.TRADE_FACTOR[c["trade"]], g[1] / g[0], g[2] / g[0], g[3] / g[0], g[4] / g[0],
                         ch["defects_true"].get(ci, 0)))
    return np.array(rows)


def plan_table(cards, ses):
    mh_area_shift = defaultdict(float)
    n_day = Counter()
    n_all = Counter()
    for s in ses:
        a = cards[s["card"]]["area"]
        mh_area_shift[(a, s["shift_idx"])] += s["hours"]
        n_day[(a, s["shift_idx"] // 2)] += 1
        n_all[s["shift_idx"]] += 1
    agg = defaultdict(lambda: [0.0, 0.0, 0.0, 0.0, 0.0])
    for s in ses:
        a = cards[s["card"]]["area"]
        g = agg[s["card"]]
        g[0] += s["hours"]
        g[1] += s["hours"] * s["n_other"]
        g[2] += s["hours"] * (mh_area_shift[(a, s["shift_idx"])] - s["hours"])
        g[3] += s["hours"] * (n_day[(a, s["shift_idx"] // 2)] - 1)
        g[4] += s["hours"] * (n_all[s["shift_idx"]] - 1)
    return np.array([(g[0], P.TRADE_FACTOR[cards[ci]["trade"]], g[1] / g[0], g[2] / g[0], g[3] / g[0], g[4] / g[0], 0)
                     for ci, g in agg.items()])


def fit(T, col, form, use_tf=True):
    mh, tf, x, y = T[:, 0], T[:, 1], T[:, col], T[:, 6]
    w = tf if use_tf else 1.0
    best = None
    grids = {"lin": np.linspace(0, 0.8, 1601), "exp": np.linspace(0, 0.2, 2001), "power": np.linspace(0, 2.0, 2001)}
    if col == 3:
        grids = {"lin": np.linspace(0, 0.2, 2001), "exp": np.linspace(0, 0.05, 2001), "power": np.linspace(0, 2.0, 2001)}
    if col == 5:
        grids = {"lin": np.linspace(0, 0.05, 2001), "exp": np.linspace(0, 0.02, 2001), "power": np.linspace(0, 2.0, 2001)}
    for k in grids[form]:
        f = {"lin": 1 + k * x, "exp": np.exp(k * x), "power": (1 + x) ** k}[form]
        u = mh * w * f
        b = y.sum() / u.sum()
        mu = b * u
        ll = float((y * np.log(mu) - mu).sum())
        if best is None or ll > best[0]:
            best = (ll, float(k), float(b))
    return best


def apply(T, col, form, k, b, use_tf=True):
    mh, tf, x = T[:, 0], T[:, 1], T[:, col]
    w = tf if use_tf else 1.0
    f = {"lin": 1 + k * x, "exp": np.exp(k * x), "power": (1 + x) ** k}[form]
    return float((b * mh * w * f).sum())


def main(seed):
    W = world.build(seed)
    H = card_table(W)
    rate = H[:, 6].sum() / H[:, 0].sum()
    days = [ch["days"] for ch in W.checks]
    print("history: %d cards, %.0f MH, %d defects (%.1f a check), %.2f per 1,000 MH; days mean %.1f range %d-%d" % (
        len(H), H[:, 0].sum(), H[:, 6].sum(), H[:, 6].sum() / len(W.checks), 1000 * rate, np.mean(days), min(days), max(days)))
    print("history MH-weighted other sessions in area-shift %.2f" % (np.sum(H[:, 0] * H[:, 2]) / H[:, 0].sum()))
    fams = [("lin", 2, True), ("exp", 2, True), ("power", 2, True), ("lin", 2, False), ("exp", 2, False),
            ("lin", 3, True), ("lin", 4, True), ("lin", 5, True)]
    fits = {}
    for form, col, tfu in fams:
        fits[(form, col, tfu)] = fit(H, col, form, tfu)
    ll0 = fit(H, 2, "lin", True)
    base_ll = float((H[:, 6] * np.log(rate * H[:, 0] * H[:, 1] / (H[:, 1] * H[:, 0]).sum() * H[:, 0].sum()) -
                     rate * H[:, 0] * H[:, 1] / (H[:, 1] * H[:, 0]).sum() * H[:, 0].sum()).sum())
    for key, v in fits.items():
        print("  fit %-22s k=%.4f ll=%.1f" % (str(key), v[1], v[0]))
    print("  no-crowding (trade only) ll=%.1f" % base_ll)
    # binned per-level empirical rates (integers of MH-weighted crowding, merged at the top)
    edges = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 24, 30, 100]
    bi = np.digitize(H[:, 2], edges)
    br = {b: H[bi == b, 6].sum() / H[bi == b, 0].sum() for b in set(bi)}
    res = {}
    for p in ("A", "B", "C"):
        S = defaultdict(float)
        for pc in W.plan_checks:
            T = plan_table(pc["cards"], pc["plans"][p])
            S["truth"] += sum(s["risk"] for s in pc["plans"][p])
            S["R0"] += rate * T[:, 0].sum()
            S["R2_crew"] += rate * T[:, 0].sum() * (T[:, 0].sum() / (2 * P.PLAN_DAYS[p])) / P.CREW_MH_PER_SHIFT
            for (form, col, tfu), v in fits.items():
                S["%s_c%d%s" % (form, col, "" if tfu else "_notr")] += apply(T, col, form, v[1], v[2], tfu)
            bj = np.digitize(T[:, 2], edges)
            S["binned"] += sum(br.get(b, rate) * T[bj == b, 0].sum() for b in set(bj))
            S["mhw_conc"] += float(np.sum(T[:, 0] * T[:, 2]) / T[:, 0].sum()) / len(W.plan_checks)
            S["mh"] += T[:, 0].sum() / len(W.plan_checks)
        res[p] = {k: (v / len(W.plan_checks) if k not in ("mhw_conc", "mh") else v) for k, v in S.items()}
    keys = [k for k in res["A"] if k not in ("mhw_conc", "mh")]
    for p in ("A", "B", "C"):
        print("plan %s (MH %.0f, crowding %.2f): " % (p, res[p]["mh"], res[p]["mhw_conc"]) +
              " ".join("%s=%.2f" % (k, res[p][k]) for k in keys))
    gold = [k for k in keys if k not in ("truth", "R0", "R2_crew")]
    core = [k for k in gold if not k.startswith(("lin_c5",))]
    for p in ("A", "B", "C"):
        vals = [res[p][k] for k in core]
        print("plan %s core family %.2f to %.2f (KPI %.1f)" % (p, min(vals), max(vals), P.KPI_DEFECTS_PER_CHECK))
    return res


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else P.SEED)
