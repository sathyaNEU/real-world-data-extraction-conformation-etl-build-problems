"""task248 robustness (scratch): every estimator family on the paired study against every plant's count."""
import numpy as np

import aim
import estim as E
import fit
import params as P
import sim
import tune


def calendar_variants(W, comps, rows):
    tt = W["tt"]
    by, bs = {}, {}
    seasons = {12: "s", 1: "s", 2: "s", 3: "a", 4: "a", 5: "a", 6: "w", 7: "w", 8: "w", 9: "p", 10: "p", 11: "p"}
    for r in rows:
        by.setdefault(r["d"].month, []).append(-np.log(r["pl"] / r["up"]) / r["tt"])
        bs.setdefault(seasons[r["d"].month], []).append(-np.log(r["pl"] / r["up"]) / r["tt"])
    km = {m: np.mean(v) for m, v in by.items()}
    ks = {k: np.mean(v) for k, v in bs.items()}
    return {"monthly": lambda s, c: E.LOG10E * km[c["d"].month] * tt[s],
            "seasonal": lambda s, c: E.LOG10E * ks[seasons[c["d"].month]] * tt[s]}


def report(W, Hh, comps, rows):
    V = aim.variants(W, Hh, comps, rows)
    for k, f in calendar_variants(W, comps, rows).items():
        V[k] = aim.counts(W, comps, f)
    codes = [p[0] for p in P.PLANTS]
    print("%-20s" % "variant", "total", " ".join("%3s" % c for c in codes), " min margin")
    for k, v in V.items():
        print("%-20s" % k, "%5d" % sum(x[0] for x in v), " ".join("%3d" % x[0] for x in v),
              " %.3f" % min(x[1] for x in v))
    return V


if __name__ == "__main__":
    W, Hh, comps, amp, shift = tune.run(iters=5, quiet=True)
    rows = sim.study(W, Hh)
    report(W, Hh, comps, rows)
    B = aim.bases(W, Hh, comps)
    for s, p in enumerate(P.PLANTS):
        if p[0] in ("ADW", "TRN", "ADS", "CLF"):
            (lp, _), (ls, _) = B[s]
            print(p[0], "pub ", aim.series(lp))
            print(p[0], "shed", aim.series(ls))
