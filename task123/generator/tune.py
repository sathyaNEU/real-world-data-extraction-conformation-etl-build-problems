"""Bin placement: choose how many premises each county keeps so that every golden award sits within $1,100 of
a multiple of $5,000, no two counties' rounded awards are equal, and every county's golden January therms sits
within 2,500 of a multiple of 10,000. Run once; the
result is written into world.TRIM and the build uses it.

    python3 tune.py
"""
import itertools
import warnings
from collections import defaultdict

import numpy as np

import calc as K
import sim as S
import world as W

warnings.filterwarnings("ignore")


def per_premise():
    prem, U, bills, mdms = S.build(pool=True)
    base = {p.pid for p in prem if p.cls != "POOL-AMI"}
    ami_base = {pid for pid in mdms if pid in base}
    w = K.shape_from_mdms(mdms, pids=ami_base)
    contrib = defaultdict(float)
    for bl in bills:
        if K.touches_jan(bl):
            contrib[bl.pid] += bl.therms * K.jan_share(w, bl.start, bl.end)
    return prem, contrib


def totals(prem, contrib, trim):
    by = defaultdict(list)
    for p in prem:
        by[p.county].append(p)
    tot = {}
    for c, (util, n, *_r) in W.COUNTIES.items():
        made = [p for p in by[c] if p.pid and p.pk < 50000]
        made.sort(key=lambda p: p.pk)
        keep = made[:n]
        e = trim.get(c, 0)
        if e > 0:
            keep = keep + [p for p in made[n:] if not p.ami][:e]
        elif e < 0:
            idx = set([i for i in range(len(keep) - 1, -1, -1) if not keep[i].ami][:-e])
            keep = [p for i, p in enumerate(keep) if i not in idx]
        tot[c] = sum(contrib.get(p.pid, 0.0) for p in keep)
    tot["Tillery"] += sum(contrib.get(p.pid, 0.0) for p in prem if p.pk >= 50000)
    return tot


def score(tot):
    aw = K.awards(tot)
    bad = 0.0
    for c in W.COUNTY_ORDER:
        da = abs(aw[c] - 5000 * round(aw[c] / 5000))
        dt = abs(tot[c] - 10000 * round(tot[c] / 10000))
        bad += max(0, da - 1100) + max(0, dt - 2500)
    r5 = sorted(5000 * round(aw[c] / 5000) for c in W.COUNTY_ORDER)
    bad += 5000 * sum(1 for x, y in zip(r5, r5[1:]) if x == y)
    return bad


def main():
    prem, contrib = per_premise()
    rs = np.random.default_rng(W.seed("tune"))
    best_overall, trim_overall = None, None
    for restart in range(30):
        trim = {c: (0 if restart == 0 else int(rs.integers(-50, 51))) for c in W.COUNTY_ORDER}
        best = score(totals(prem, contrib, trim))
        for sweep in range(15):
            improved = False
            for c in W.COUNTY_ORDER:
                for e in range(-70, 71):
                    t2 = dict(trim)
                    t2[c] = e
                    sc = score(totals(prem, contrib, t2))
                    if sc < best - 1e-9:
                        best, trim, improved = sc, t2, True
            if best == 0 or not improved:
                break
        print("restart", restart, "score", round(best, 1))
        if best_overall is None or best < best_overall:
            best_overall, trim_overall = best, trim
        if best == 0:
            break
    trim = trim_overall
    tot = totals(prem, contrib, trim)
    aw = K.awards(tot)
    for c in W.COUNTY_ORDER:
        print("%-11s %10.0f %12.0f" % (c, tot[c], aw[c]))
    print("TRIM =", {c: v for c, v in trim.items() if v})


if __name__ == "__main__":
    main()
