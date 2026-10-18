"""The cracker's and the mirror's paths, run on the cut pack.

The cracker landed the call, ran the battery (exact duplicates, key uniqueness on each file's natural key, unmatched
keys on both sides of every join it makes, join fan-out), executed every filed rule and documented definition the
asking sentences point at in its plain meaning (the HIM merge list followed), and matched every control. It does not
reconcile records across grains or files beyond those joins. For each ask this module computes what that path returns
and scores it against the golden (whole hips). The mirror stops at R1 on the call and takes the asks the same way. It
is measurement, not argument.

    python3 task265/generator/cracker.py [target]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as A   # noqa: E402
import common as K     # noqa: E402

CHART = 3              # the chart's form criteria, kept by any response that draws one


def paths(target):
    """A: each primary total hip case's implanted stems and shells less any explanted, a hip for each side the implant
    log records them on (the log is joined to the case list on the case number), mapped to a construct through the
    crosswalk. C: those hips matched to the registry's 2026 rows on MRN, side and operation date, each MRN taken
    through the HIM merge list to the numbers it retired."""
    return A.asks(target, honour_side=False, merges=True)


def score(target):
    g, got = A.asks(target), paths(target)
    return [("A", len(K.CODES) * len(K.HOSP), sum(got["A"][c][h] == g["A"][c][h] for c in K.CODES for h in K.HOSP)),
            ("C", len(K.HOSP) + len(K.CODES), sum(got["C_hosp"][h] == g["C_hosp"][h] for h in K.HOSP) +
             sum(got["C_construct"][c] == g["C_construct"][c] for c in K.CODES))]


def ceiling(cr, mi):
    """supplemental-stumping Part 0: C = 38 + 7 + 55 Lc, S = r + 7 + 55 Ls with r about 5, the chart's form to both."""
    total = sum(n for _a, n, _h in cr)
    lc = sum(h for _a, _n, h in cr) / float(total)
    ls = sum(h for _a, _n, h in mi) / float(total)
    return total, lc, ls, ((38 + 7 + CHART + 55 * lc) + (5 + 7 + CHART + 55 * ls)) / 2.0


if __name__ == "__main__":
    tgt = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")
    cr = score(tgt)
    mi = cr                # the mirror's ask paths are the cracker's
    for ask, n, h in cr:
        print("%s: %d figures, cracker keeps %d, misses %d" % (ask, n, h, n - h))
    total, lc, ls, pair = ceiling(cr, mi)
    print("total %d figures, cracker keeps %.1f per cent, mirror leakage %.1f per cent, pair ceiling %.1f"
          % (total, 100 * lc, 100 * ls, pair))
