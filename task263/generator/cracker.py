"""The cracker's and the mirror's paths, run on the cut pack.

The cracker landed the call, ran the battery (exact duplicates, key uniqueness on each file's natural key, unmatched
keys on both sides of every join it makes, join fan-out), executed every filed rule and documented definition the
asking sentences point at in its plain meaning, and matched every control. It does not reconcile amounts across grains
or files beyond those joins. For each ask this module computes what that path returns and scores it against the golden
at the stated rounding (million gallons to one decimal, whole people). The mirror stops at R0 on the call and takes the
asks the same way. It is measurement, not argument.

    python3 task263/generator/cracker.py [target]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as A   # noqa: E402

CHART_CRACKER = 5      # the chart drawn from the call's own well levels
R_MIRROR = 5           # the recommendation weight a wrong call keeps
CHART_MIRROR = 0       # the mirror's chart is drawn on R0's levels


def paths(target):
    """A: the 2025 operating reports' gallons on every well line of a listed system (facility types from the
    inventory, the emergency well that ran included), summed by the plan's county. B: the listed systems' customers
    and every system buying all its water from them, directly or through another buyer, on the full purchases in
    service, each system's register row as the connection's id finds it, by the county it serves."""
    D = A.load(target)
    return D, A.ask_a(D, target, "every_row"), A.ask_b(D, target, "as_found")


def score(target):
    D, a, b = paths(target)
    ga, gb = A.ask_a(D, target), A.ask_b(D, target)
    return [("A", len(ga), sum(abs(a.get(c, 0) - ga[c]) < .05 for c in ga)),
            ("B", len(gb), sum(b.get(c) == gb[c] for c in gb))]


def ceiling(cr, mi):
    """supplemental-stumping Part 0: C = 38 + 7 + 55 Lc, S = r + 7 + 55 Ls, the chart's parts beside."""
    total = sum(n for _a, n, _h in cr)
    lc = sum(h for _a, _n, h in cr) / float(total)
    ls = sum(h for _a, _n, h in mi) / float(total)
    return total, lc, ls, ((38 + 7 + CHART_CRACKER + 55 * lc) + (R_MIRROR + 7 + CHART_MIRROR + 55 * ls)) / 2.0


if __name__ == "__main__":
    tgt = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")
    cr = score(tgt)
    mi = cr                # the mirror's ask paths are the cracker's
    for ask, n, h in cr:
        print("%s: %d figures, cracker keeps %d, misses %d" % (ask, n, h, n - h))
    total, lc, ls, pair = ceiling(cr, mi)
    print("total %d figures, cracker keeps %.1f per cent, mirror leakage %.1f per cent, pair ceiling %.1f"
          % (total, 100 * lc, 100 * ls, pair))
