"""The cracker's and the mirror's paths, run on the cut pack.

The cracker landed the call, ran the hygiene battery, executed every rule the asking sentences point at and matched
every control. For each ask this module computes what that path returns and scores it against the golden at the
stated rounding (whole young people, spending to the nearest thousand dollars). The mirror stops at rung 0 on the call
(Halverston) and takes the asks the same way, nothing on either ask's path pointing further. It is measurement, not
argument.

    python3 task262/generator/cracker.py [target]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as K     # noqa: E402
import deliver as G    # noqa: E402
import stops as SP     # noqa: E402

CHART_CRACKER = 5      # the chart drawn from the call's own elasticities, every part right
CHART_MIRROR = 3       # the chart's form, kept with rung 0's elasticities


def paths(target):
    """A: the guidelines' transfer chains followed back to the first record, and the battery's repeated rows (office,
    intake date and date of birth) dropped. B: each office's ledger lines plus the central cost centre's lines, the
    reversals included, shared by the cracker's own starts."""
    A = SP.ask_a_stops(target)
    B, _ = SP.ask_b_stops(target, {"golden": G.starts(target), "cracker": A["dedup"]})
    return A["dedup"], B["shared reversal, starts cracker"]


def score(target, res=None):
    res = res or G.compute(target)
    a, b = paths(target)
    return [("A", len(K.NAMES), sum(a[n] == res["starts"][n] for n in K.NAMES)),
            ("B", len(K.NAMES), sum(G.thousands(b[n]) == G.thousands(res["spending"][n]) for n in K.NAMES))]


def ceiling(cr, mi):
    """supplemental-stumping Part 0: C = 38 + 7 + 55 Lc, S = r + 7 + 55 Ls with r about 5, the chart's parts beside."""
    total = sum(n for _a, n, _h in cr)
    lc = sum(h for _a, _n, h in cr) / float(total)
    ls = sum(h for _a, _n, h in mi) / float(total)
    return total, lc, ls, ((38 + 7 + CHART_CRACKER + 55 * lc) + (5 + 7 + CHART_MIRROR + 55 * ls)) / 2.0


if __name__ == "__main__":
    tgt = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")
    cr = score(tgt)
    mi = cr                # the mirror's ask paths are the cracker's
    for ask, n, h in cr:
        print("%s: %d figures, cracker keeps %d, misses %d" % (ask, n, h, n - h))
    total, lc, ls, pair = ceiling(cr, mi)
    print("total %d figures, cracker keeps %.1f per cent, mirror leakage %.1f per cent, pair ceiling %.1f"
          % (total, 100 * lc, 100 * ls, pair))
