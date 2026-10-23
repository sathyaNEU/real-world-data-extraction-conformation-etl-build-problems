"""Seed search: the world whose golden family names one set, every wrong route another, with margins.

    python3 task275/generator/seedsearch.py [first] [last]"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as A   # noqa: E402
import common as K     # noqa: E402
import world as W      # noqa: E402

TARGET = ("TR1", "TR2", "NEP", "BT")


def score(seed, verbose=False):
    w = W.simulate(seed)
    T = W.analysis_trips(w)
    fam = A.family(T)
    sets = {A.designated(g) for g in fam.values()}
    R = A.routes(T)
    rs = {k: A.designated(v) for k, v in R.items()}
    tr = W.truth(w)
    whole = {s: {round(g[s]) for g in fam.values()} for s in K.SEG}
    cells = {}
    for s in K.SEG:
        for g in K.GR:
            n_obs = sum(1 for t in T if t["seg"] == s and t["ground"] == g and t["observed"])
            n_un = sum(1 for t in T if t["seg"] == s and t["ground"] == g and not t["observed"])
            if n_un:
                cells[(s, g)] = n_obs
    if verbose:
        g0 = fam["ground/hours/decl"]
        for s in K.SEG:
            print("%-4s truth %5.1f golden %5.1f family %5.1f..%5.1f | %s" % (
                s, tr[s], g0[s], min(g[s] for g in fam.values()), max(g[s] for g in fam.values()),
                " ".join("%.1f" % R[k][s] for k in R)))
        print("family sets", sets)
        for k, v in rs.items():
            print("  %-70s %s" % (k, v))
        print("margin %.2f, thinnest cell %s" % (A.margin(fam), min(cells.items(), key=lambda kv: kv[1])))
        print("whole-per-cent agreement:", {s: sorted(v) for s, v in whole.items()})
    ok = (len(sets) == 1 and next(iter(sets)) == TARGET and A.designated(tr) == TARGET
          and rs["R2 the observed discards per hour by ground, raised (default path)"] == ("NEP",)
          and rs["R4 unwanted catch per hour, grounds pooled"] not in (TARGET,)
          and rs["R3 the observed trips' unwanted share"] not in (TARGET,)
          and rs["R5 unwanted catch per hour by ground, declared BMS not netted"] not in (TARGET,))
    return ok, A.margin(fam), min(cells.values()), sum(len(v) == 1 for v in whole.values())


if __name__ == "__main__":
    if len(sys.argv) == 2:
        score(int(sys.argv[1]), verbose=True)
        sys.exit(0)
    a, b = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) > 2 else (1, 60)
    res = []
    for seed in range(a, b):
        ok, m, c, wh = score(seed)
        if ok:
            res.append((round(m, 2), wh, c, seed))
            print("seed %d ok margin %.2f whole-agree %d min cell %d" % (seed, m, wh, c), flush=True)
    res.sort(reverse=True)
    print(res[:10])
