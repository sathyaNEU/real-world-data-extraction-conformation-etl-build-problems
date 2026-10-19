"""task248 tuning (scratch, not shipped): set each plant's 2027 main and late wave amplitudes to its scenario's target
peak levels on the shed load, then report both bases' episode counts and margins."""
import numpy as np

import aim
import estim as E
import params as P
import sim

# scenario per plant: (name, main peak target on the shed load, late peak target)
SCEN = {
    "ASD": ("one", 1.42, 0.50), "BRK": ("two", 1.38, 1.30), "CRF": ("one", 1.18, 0.50), "DNK": ("one", 1.33, 0.55),
    "FNK": ("two", 1.30, 1.24), "GLO": ("one", 1.16, 0.55), "HOL": ("two", 1.45, 1.22), "INB": ("one", 1.20, 0.50),
    "KSB": ("one", 1.36, 0.55), "LRF": ("two", 1.40, 1.28), "MRB": ("one", 1.48, 0.55), "NTL": ("one", 1.32, 0.55),
    "ORB": ("two", 1.34, 1.26), "PLH": ("one", 1.42, 0.50), "QRM": ("two", 1.37, 1.30), "RVG": ("one", 1.26, 0.50),
    "ADN": ("one", 1.40, 0.40), "ADS": ("spur_main", 0.80, 0.40), "ADE": ("spur_late", 0.52, 0.80),
    "ADW": ("merge", 1.38, 1.28), "TRN": ("spur_late", 0.50, 0.78), "UWD": ("one", 1.33, 0.40),
    "CLF": ("spur_main", 0.78, 0.40), "SLT": ("spur_late", 0.48, 0.78),
}
SHIFT = {"ADW": {"w27_late": -13}, "HOL": {"w27_late": 6}}


def peaks(lev):
    import datetime as dt
    ws = sorted(lev)
    main = max(lev[w] for w in ws if P.WINTER[0] <= w <= E.monday(dt.date(2027, 7, 31)))
    late = max(lev[w] for w in ws if E.monday(dt.date(2027, 8, 16)) <= w <= P.WINTER[1])
    return main, late


def run(iters=5, quiet=False):
    amp = sim.default_amp(np.random.default_rng(7))
    shift = {}
    for s, p in enumerate(P.PLANTS):
        amp[s]["w27_main"] = SCEN[p[0]][1]
        amp[s]["w27_late"] = SCEN[p[0]][2]
        if p[0] in SHIFT:
            shift[s] = SHIFT[p[0]]
    for it in range(iters):
        W = sim.make(amp=amp, shift=shift)
        Hh = sim.hourly(W)
        comps = sim.composites(W, Hh)
        B = aim.bases(W, Hh, comps)
        worst = 0
        for s, p in enumerate(P.PLANTS):
            (lp, _), (ls, _) = B[s]
            m, l = peaks(ls)
            tm, tl = SCEN[p[0]][1], SCEN[p[0]][2]
            amp[s]["w27_main"] += (tm - m)
            amp[s]["w27_late"] += (tl - l)
            worst = max(worst, abs(tm - m), abs(tl - l))
        if not quiet:
            print("iteration", it, "worst miss", round(worst, 3))
    return W, Hh, comps, amp, shift


if __name__ == "__main__":
    W, Hh, comps, amp, shift = run()
    aim.table(W, Hh, comps)
    B = aim.bases(W, Hh, comps)
    for s, p in enumerate(P.PLANTS):
        if p[0] in ("ADN", "UWD", "ADW", "ADE", "TRN", "SLT", "ADS", "CLF", "LRF", "ORB", "QRM", "HOL"):
            (lp, _), (ls, _) = B[s]
            print(p[0], "pub ", aim.series(lp))
            print(p[0], "shed", aim.series(ls))
