"""The cracker's and the mirror's paths, run on the cut pack.

The cracker landed the call, ran the battery (exact duplicates, key uniqueness on each file's natural key, unmatched
keys on both sides of every join it makes, join fan-out), executed every filed rule and documented definition the
asking sentences point at in its plain meaning, and matched every control. It does not reconcile amounts across grains
or files beyond those joins. For each ask this module computes what that path returns and scores it against the golden
at the stated rounding (whole households, dollars to the nearest thousand). The mirror stops at rung 0 on the call (the
quadrature) and takes the asks the same way. It is measurement, not argument.

    python3 task261/generator/cracker.py [target]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as K     # noqa: E402
import deliver as G    # noqa: E402
import stops as SP     # noqa: E402

CHART_CRACKER = 7      # Ask C, the chart, drawn from the call's own differences and intervals: every part right
R_MIRROR = 10          # the six medians and the 65 and over merge the quadrature mirror shares with the golden
CHART_MIRROR = 5       # the chart's form and points, its intervals drawn half as wide again


def paths(target):
    """A: merged client numbers followed, members alive at 31 December, households from the register with a partner
    who is not a client taken from the nominations (the dictionary), and the pension of a member who died in December
    taken to the reversionary beneficiary (the PDS); every account row added. B: annuities begun and paying by 31
    December (the dictionary's payments_start), January anniversary increases taken back (the listing is at the pull,
    the key facts give the rates), every life alive at 31 December at its listed amount, each with its own household."""
    F = SP.Files(target)
    return SP.ask_a(F, **SP.A_STOPS["cracker"]), SP.ask_b(F, **SP.B_STOPS["cracker"])


def score(target, res=None):
    res = res or G.compute(target)
    a, b = paths(target)
    th = G.thousands
    return [("A", 3 * len(K.OLDER), sum((a[g]["households"] == res["A"][g]["households"]) +
                                        (th(a[g]["balance"]) == th(res["A"][g]["balance"])) +
                                        (th(a[g]["payments"]) == th(res["A"][g]["payments"])) for g in K.OLDER)),
            ("B", 2 * len(K.OLDER), sum((b[g]["households"] == res["B"][g]["households"]) +
                                        (th(b[g]["income"]) == th(res["B"][g]["income"])) for g in K.OLDER))]


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
