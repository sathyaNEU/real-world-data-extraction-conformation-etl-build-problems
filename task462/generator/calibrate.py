"""Scratch calibration (not part of the build): sets and margins under every estimator for a seed, or a seed search."""
import sys
import numpy as np
import basin as B
import methods as M
import production as PR
import world as W


def ladder(seed, verbose=False):
    x = B.world(seed)
    rng = np.random.default_rng(seed + 11)
    wl = PR.wells(rng, x["sites"])
    rows = PR.monthly(rng, x["sites"], wl)
    prod = PR.methane_produced(rows)
    sites = x["sites"]
    # attribution by the nearest site within 150 m
    pl = []
    for p, (sid, d) in zip(x["plumes"], M.attribute(x["plumes"], sites)):
        q = dict(p)
        q["site"] = sid
        pl.append(q)
    pod = M.fit_pod(x["releases"])
    res = {}
    res["truth"] = M.intensity(x["truth"], prod)
    res["E3 golden"] = M.intensity(M.emitted(sites, x["passes"], pl, lambda z: z["rate"] / pod(z["rate"])), prod)
    res["E2 zeros"] = M.intensity(M.emitted(sites, x["passes"], pl, lambda z: z["rate"]), prod)
    res["E1 carried"] = M.intensity(M.carried_sources(sites, x["passes"], pl), prod)
    res["E4 duty"] = M.intensity(M.carried_sources(sites, x["passes"], pl, duty=True), prod)
    pr = M.fit_pod(x["releases"], link="probit")
    pw = M.fit_pod(x["releases"], wind=True)
    res["E3 probit"] = M.intensity(M.emitted(sites, x["passes"], pl, lambda z: z["rate"] / pr(z["rate"])), prod)
    res["E3 wind"] = M.intensity(M.emitted(sites, x["passes"], pl, lambda z: z["rate"] / pw(z["rate"], z["wind"])), prod)
    res["E3 true pod"] = M.intensity(M.emitted(sites, x["passes"], pl, lambda z: z["rate"] / float(B.pod(z["rate"]))), prod)
    res["E3 cov0"] = M.intensity(M.emitted(sites, x["passes"], pl, lambda z: z["rate"] / pod(z["rate"]), coverage_zero=True), prod)
    res["E3 first"] = M.intensity(M.emitted(sites, x["passes"], pl, lambda z: z["rate"] / pod(z["rate"]), first_pass_only=True), prod)
    res["E3 sum2"] = M.intensity(M.emitted(sites, x["passes"], pl, lambda z: z["rate"] / pod(z["rate"]), sum_passes=True), prod)
    prod_cur = PR.methane_produced(rows, sites, by_current_operator=True)
    res["E3 current op"] = M.intensity(M.emitted(sites, x["passes"], pl, lambda z: z["rate"] / pod(z["rate"]), by_current_operator=True), prod_cur)
    res["E3 all reports"] = M.intensity(M.emitted(sites, x["passes"], pl, lambda z: z["rate"] / pod(z["rate"])), PR.methane_produced(rows, latest_only=False))
    res["E3 14.65"] = M.intensity(M.emitted(sites, x["passes"], pl, lambda z: z["rate"] / pod(z["rate"])), PR.methane_produced(rows, convert=False))
    sets = {k: M.rated(v) for k, v in res.items()}
    if verbose:
        print("pod fit q50 %.2f s %.3f" % (math.exp(-pod.b[0] / pod.b[1]), 1 / pod.b[1]))
        keys = ["truth", "E3 golden", "E2 zeros", "E1 carried", "E4 duty", "E3 probit", "E3 wind", "E3 cov0", "E3 sum2", "E3 current op"]
        print("%-24s" % "producer" + "".join("%11s" % k[:10] for k in keys))
        for p in W.NAMES:
            print("%-24s" % p + "".join("%11.3f" % res[k][p] for k in keys))
        for k in res:
            print("%-14s %d %s" % (k, len(sets[k]), [s.split()[0] for s in sets[k]]))
    return res, sets


import math
if __name__ == "__main__":
    if sys.argv[1] == "search":
        want = sorted(["Calbrent Energy", "Brushy Mesa Operating", "Corrandale Petroleum", "Ostrel Energy"])
        Ms = ["Pinyon Draw Production", "Anchell Oil & Gas", "Pellisto Gas Partners"]
        good = []
        for seed in range(int(sys.argv[2]), int(sys.argv[3])):
            res, sets = ladder(seed)
            g = sets["E3 golden"]
            ok = sorted(g) == want and sorted(sets["truth"]) == want and all(m in sets["E2 zeros"] for m in Ms) and all(w in sets["E2 zeros"] for w in want) \
                and len(sets["E1 carried"]) <= 1 and all(sorted(sets[k]) == want for k in ["E3 probit", "E3 wind", "E3 true pod", "E3 cov0", "E3 first", "E3 sum2", "E3 current op", "E3 all reports", "E3 14.65"])
            if ok:
                m3 = min(abs(res["E3 golden"][p] - W.LIMIT) / W.LIMIT for p in W.NAMES)
                m2 = min(abs(res["E2 zeros"][p] - W.LIMIT) / W.LIMIT for p in W.NAMES)
                good.append((round(min(m3, m2), 4), seed, round(m3, 4), round(m2, 4)))
        good.sort(reverse=True)
        print(len(good), good[:10])
    else:
        ladder(int(sys.argv[1]), True)
