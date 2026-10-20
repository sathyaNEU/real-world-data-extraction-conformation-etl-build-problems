"""Place each in-play municipality's register count so the ladder separates: the golden (the audit's rate by current
stay and earlier departure) puts the seasonal-work towns and the university town under 5,000 and keeps the older
immigrant towns and the commuter suburb over it, while every rung a competent analyst stops at files another set.

    python3 task471/generator/calibrate.py           print the placement and the ladder at world.COUNT
    python3 task471/generator/calibrate.py --place   search the counts for the targets below
"""
import os
import pickle
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import methods as M   # noqa: E402
import sim as S       # noqa: E402
import world as W     # noqa: E402

CACHE = os.environ.get("T471_CACHE")
TARGET = {"G": 4952, "U": 4958, "O": 5042, "S": 5038}      # golden adjusted population per decisive type


def features(p):
    """a person's features exactly as the shipped files give them (bundle.py derives the same from the files)"""
    ev = p["events"]
    imms = [e[1] for e in ev if e[0] == "IMM"]
    latest = imms[-1] if imms else None
    stay = S.completed_years(latest) if latest else None
    left = int(any(e[0] == "EMI" and e[1] < latest for e in ev)) if latest else 0
    first = S.completed_years(imms[0]) if imms else None
    return dict(stay=stay, left=left, first=first, addr=S.completed_years(p["since"]),
                abroad=int(p["bcountry"] != W.HOME[0]), foreign=int(p["nat"] != W.HOME[0]),
                age=S.completed_years(p["birth"]), sex=p["sex"])


def load_pools():
    if CACHE and os.path.exists(CACHE):
        return pickle.load(open(CACHE, "rb"))
    pool = S.pools(W.SEED)
    if CACHE:
        pickle.dump(pool, open(CACHE, "wb"))
    return pool


def ladder(counts, pool, show=True):
    reg, sample = S.register(W.SEED, counts, pool)
    audit = [(features(p), int(p["result"] in ("20", "30", "40"))) for p in sample]
    pops = {m: [features(p) for p in reg[m]] for m in W.CODES}
    methods = dict(M.RUNGS, **M.VARIANTS)
    adj = {name: M.adjusted(audit, pops, key) for name, key in methods.items()}
    adj["R0 register count"] = {m: float(len(p)) for m, p in pops.items()}
    sets = {name: M.qualifying(a) for name, a in adj.items()}
    if show:
        print("audit: %d sampled, %d absent; in-play sampled %d" % (
            len(audit), sum(a for _, a in audit), sum(1 for p in sample if p["mun"] in W.CODES)))
        cols = ["R0 register count"] + list(M.RUNGS) + list(M.VARIANTS)
        print("%-12s %s %5s  " % ("", "t", "reg") + " ".join("%7s" % c.split()[0] for c in cols))
        for m in W.CODES:
            print("%-12s %s %5d  " % (W.NAME[m], W.TYPE[m], counts[m]) + " ".join(
                "%6.0f%s" % (adj[c][m], "*" if round(adj[c][m]) < W.LINE else " ") for c in cols))
        g = sets[M.GOLDEN]
        for c in cols:
            s = sets[c]
            print("%-40s %2d %s%s" % (c, len(s), " ".join(W.NAME[m] for m in s if W.TYPE[m] != "T"),
                                      "" if c.startswith("G") else ("  (golden)" if s == g else "")))
    return adj, sets


def place(pool):
    """search each decisive municipality's count for its target under the golden"""
    counts = dict(W.COUNT)
    for _ in range(3):
        reg, sample = S.register(W.SEED, counts, pool)
        audit = [(features(p), int(p["result"] in ("20", "30", "40"))) for p in sample]
        rates, pooled = M.fit(audit, M.RUNGS[M.GOLDEN])
        for m in W.CODES:
            t = TARGET.get(W.TYPE[m])
            if not t:
                continue
            f = [features(p) for p in pool[m]]
            cum = np.cumsum([rates.get(M.RUNGS[M.GOLDEN](x), pooled) for x in f])
            n = np.arange(1, len(f) + 1)
            counts[m] = int(n[np.argmin(np.abs(n - cum - t))])
    return counts


if __name__ == "__main__":
    pool = load_pools()
    counts = place(pool) if "--place" in sys.argv else W.COUNT
    if "--place" in sys.argv:
        print("COUNT =", {m: counts[m] for m in W.CODES})
    ladder(counts, pool)
