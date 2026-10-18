"""The cracker's and the mirror's paths, run on the cut pack.

The cracker landed the call, ran the battery (exact duplicates, key uniqueness on serial and run time and on
accession lines, unmatched serials and accessions on both sides of every join it makes, join fan-out), executed every
filed rule and documented definition the asking sentences point at in its plain meaning (the maker's error rule, the
asset register by date, the season's dates), and matched every control. It does not reconcile records across rows or
files beyond those joins. For each ask this module computes what that path returns and scores it against the golden
(whole cartridges, dollars to the cent). The mirror stops off the call and takes the asks the same way. It is
measurement, not argument.

    python3 task267/generator/cracker.py [target]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as A   # noqa: E402

R_MIRROR = 11          # the mirror's six referral shares and the rule figures it shares with the golden


def paths(target):
    """A: every run row on its analyzer's tag for the season, the maker's error rule applied, no row repeated in
    every field kept once (none is). B: every invoice and credit memo line by its own service_date column, the
    program's tests those whose accession the OGTT extract carries."""
    return A.cartridges(target, twins="keep"), A.ask_b(target, month_of="row")


def score(target):
    a, b = paths(target)
    ga, gb = A.ask_a(target), A.ask_b(target)
    return [("A", len(ga), sum(a.get(k) == ga[k] for k in ga)),
            ("B", 2 * len(gb), sum((b[m][0] == gb[m][0]) + (b[m][1] == gb[m][1]) for m in gb))]


def ceiling(cr, mi):
    """supplemental-stumping Part 0: C = 38 + 7 + 55 Lc, S = r + 7 + 55 Ls."""
    total = sum(n for _a, n, _h in cr)
    lc = sum(h for _a, _n, h in cr) / float(total)
    ls = sum(h for _a, _n, h in mi) / float(total)
    return total, lc, ls, ((38 + 7 + 55 * lc) + (R_MIRROR + 7 + 55 * ls)) / 2.0


if __name__ == "__main__":
    tgt = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")
    cr = score(tgt)
    mi = cr                # the mirror's ask paths are the cracker's
    for ask, n, h in cr:
        print("%s: %d figures, cracker keeps %d, misses %d" % (ask, n, h, n - h))
    total, lc, ls, pair = ceiling(cr, mi)
    print("total %d figures, cracker keeps %.1f per cent, mirror leakage %.1f per cent, pair ceiling %.1f"
          % (total, 100 * lc, 100 * ls, pair))
