"""The ask sheet's measurement on the cut pack: the cracker (lands the call, executes every filed rule, runs the two
asks the obvious way: every F-217 hour excluded with the gaps read through the register, the whole account netted)
and the mirrors (off the call on the default path and on each rung, the same asks), scored figure by figure on the
38 / 7 / 55 planning weights against the golden recomputed from the same pack.

    python3 task152/generator/pair.py <target dir>

Main block (38): the volume, the P50 and the standard deviation at the prompt's rounding, equal weight.
Instruction-following (7): kept by every path. Asks (55) over the 26 ask figures: Ask A's 16 availabilities and
Ask B's 10 years' over or under.
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import asks as AS    # noqa: E402
import calc as CA    # noqa: E402

REC, IF, ASK = 38.0, 7.0, 55.0


def rounded(p90, G):
    """The three main figures a construction with this P90 files: energies scale with its performance ratio."""
    k = p90 / G.Hp90
    p50 = k * float(G.H.mean())
    sd = k * float(G.H.std(ddof=1))
    return (int(math.floor(p90 / 1000.0)) * 1000, int(math.floor(p50 / 1000.0 + 0.5)) * 1000,
            int(math.floor(sd / 100.0 + 0.5)) * 100)


def run(target):
    G = CA.analyse(target, CA.report_gain(target))
    r = CA.routes(G)
    gold = rounded(G.P90, G)
    _, ga, sa = AS.ask_a(target)
    _, gb, sb = AS.ask_b(target)
    ca = sa["S4 every F-217 hour excluded, gaps read through the register"]
    cb = sb["S2 the whole account netted"]
    hits = sum(round(ca[t]["avail"], 2) == round(ga[t]["avail"], 2) for t in ga) + \
        sum(AS.rnd(cb[y]) == AS.rnd(gb[y]) for y in gb)
    asks = ASK * hits / 26.0
    crack = REC * sum(a == b for a, b in zip(rounded(r["golden"], G), gold)) / 3.0 + IF + asks
    best, best_k = -1.0, ""
    for key in ("R0 the last twelve months carried with the gain", "R1 the first year carried with the gain",
                "R2 the DC-side decline on available days", "R2b the decline after washes at the inverters' AC output"):
        m = REC * sum(a == b for a, b in zip(rounded(r[key], G), gold)) / 3.0 + IF + asks
        print("mirror  %-60s main %s, score %.1f" % (key, rounded(r[key], G), m))
        if m > best:
            best, best_k = m, key
    print("golden  main %s" % (gold,))
    print("cracker: main %s, asks %d of 26, score %.1f" % (rounded(r["golden"], G), hits, crack))
    print("best mirror: %s, score %.1f" % (best_k, best))
    print("mirror leakage: %.1f per cent of ask weight" % (100.0 * hits / 26.0))
    print("pair ceiling: %.1f" % ((crack + best) / 2))
    return crack, best


if __name__ == "__main__":
    run(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target"))
