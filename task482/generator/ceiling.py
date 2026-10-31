"""The ask layer's pair ceiling on the cut pack (supplemental-stumping Part 0 and 1.1). The cracker lands the call,
runs the hygiene battery and executes every filed rule it points at: Schedule C's 5:00 p.m. Central rule, its
holidays and its five business days on Central-time stamps, the plan summary's coverage rule for installments; it
reads the platforms' own records as the units (each Nexus estimate a request, each orthodontic case a treatment). The
mirror stops off the call and reads the stamps as written (UTC) and every case as its own treatment, coverage
unchecked. Each is scored figure by figure against the golden.

    python3 task482/generator/ceiling.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
T = os.path.join(os.path.dirname(HERE), "target")
sys.path.insert(0, HERE)
import golden as G  # noqa: E402


def flat_a(a):
    return [(q, j, a.get(q, (0, 0))[j]) for q in G.QUARTERS for j in (0, 1)]


def flat_b(b):
    owed, kids = b
    return [(y, j, (kids, owed)[j][y]) for y in G.START_YEARS for j in (0, 1)]


def kept(gold, other):
    return sum(1 for x, y in zip(gold, other) if x == y)


def main():
    res = G.solve(T)
    p, key = res["p"], res["key"]
    gold_a, gold_b = flat_a(res["ask_a"]), flat_b(res["ortho"])
    est_c = res["est"]
    est_u = G.estimate_lines(p, key, conv=G.utc_naive)
    routes_a = {
        "each Nexus estimate a request, Central time (the cracker)": G.turnaround(p, key, est_c, group_new=False),
        "each Nexus estimate a request, the stamps as written in UTC (the mirror)": G.turnaround(p, key, est_u, group_new=False),
        "requests grouped, the stamps as written in UTC": G.turnaround(p, key, est_u),
        "requests grouped, Central time, no holidays": G.turnaround(p, key, est_c, holidays=False),
        "requests grouped, Central time, receipt on the day it arrived": G.turnaround(p, key, est_c, rule=False),
    }
    routes_b = {
        "each case a treatment, coverage checked (the cracker)": G.ortho_owed(p, key, by_child=False),
        "each case a treatment, coverage unchecked (the mirror)": G.ortho_owed(p, key, by_child=False, check_coverage=False),
        "each child once, coverage unchecked": G.ortho_owed(p, key, check_coverage=False),
    }
    n = len(gold_a) + len(gold_b)
    print("ask A, predetermination requests by quarter (received, answered within five business days): %d figures" % len(gold_a))
    ka = {}
    for name, a in routes_a.items():
        ka[name] = kept(gold_a, flat_a(a))
        print("  %-76s keeps %2d" % (name, ka[name]))
    print("ask B, orthodontic treatment by the year it began (children, owed): %d figures" % len(gold_b))
    kb = {}
    for name, b in routes_b.items():
        kb[name] = kept(gold_b, flat_b(b))
        print("  %-76s keeps %2d" % (name, kb[name]))
    crack = ka["each Nexus estimate a request, Central time (the cracker)"] + kb["each case a treatment, coverage checked (the cracker)"]
    mirror = ka["each Nexus estimate a request, the stamps as written in UTC (the mirror)"] + \
        kb["each case a treatment, coverage unchecked (the mirror)"]
    lc, lm = crack / float(n), mirror / float(n)
    c = 38 + 7 + 55 * lc
    s = 5 + 7 + 55 * lm
    best = max(ka.values()) + max(kb.values())
    print("cracker keeps %d of %d ask figures (%.1f per cent), scores %.1f with the call" % (crack, n, 100 * lc, c))
    print("mirror keeps %d of %d (%.1f per cent), scores %.1f off it" % (mirror, n, 100 * lm, s))
    print("the best half-handled response keeps %d of %d (%.1f per cent)" % (best, n, 100.0 * best / n))
    print("Pair ceiling: %.1f" % ((c + s) / 2))
    print("Mirror leakage: %.1f per cent of ask weight" % (100 * lm))
    return dict(crack=crack, mirror=mirror, n=n, pair=(c + s) / 2, ka=ka, kb=kb)


if __name__ == "__main__":
    main()
