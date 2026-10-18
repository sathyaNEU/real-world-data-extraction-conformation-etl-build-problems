"""The cracker's and the mirror's paths, run on the cut pack.

The cracker landed the call, ran the battery (exact duplicates, key uniqueness on each file's natural key, unmatched
keys on both sides of every join it makes, join fan-out), executed every filed rule and documented definition the
asking sentences point at in its plain meaning, and matched every control. It does not reconcile amounts across
grains or files beyond those joins. For each ask this module computes what that path returns and scores it against
the golden within half a unit of the stated rounding (half a pound, half a vehicle). The mirror stops at the default
path on the call and takes the asks the same way. It is measurement, not argument.

    python3 task264/generator/cracker.py [target]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as K   # noqa: E402
import golden as G   # noqa: E402

CHART = 3            # the chart's form criteria, kept by any response that draws one


def paths(target):
    """Each ask as the cracker reads it. A: the machines' repeated tickets dropped (machine and ticket number are the
    key), the tariff workbook's note that charges include VAT executed on both the machines and the app, each machine
    at its register site. B: each receipt dated by the day the bank credited it (the manifest defines the cash book's
    date as the booking and the bank's as the credit), found in the bank's report on its reference and amount; the
    cash book's lines on the levy invoices added up; the credits of 31 March the cash book's year leaves out (the
    unmatched side of that join) taken against each payer's open invoices that make up the credit. C: the counters'
    hours as reported, each counter at its register site (no row repeats a counter and hour)."""
    return dict(A=G.parking_income(target, vat_on_app=True, dedupe=True, sites="register"),
                B=G.levy_timeliness(target, dates="bank", lines="line", yearend="payer"),
                C=G.vehicles(target, False, False, False))


def score(target, g=None):
    g = g or G.compute(target)
    got = paths(target)
    rows = []
    rows.append(("A", len(K.CHARGING), sum(abs(got["A"][p] - g["income"][p]) < .5 for p in K.CHARGING)))
    rows.append(("B", 2 * len(K.CODES), sum(abs(got["B"][c][k] - g["collection"][c][k]) < .5
                                           for c in K.CODES for k in ("on_time", "late"))))
    rows.append(("C", len(K.CHARGING), sum(abs(got["C"][p] - g["vehicles"][p]) < .5 for p in K.CHARGING)))
    return rows


def ceiling(cracker, mirror):
    """supplemental-stumping Part 0: C = 38 + 7 + 55 Lc, S = r + 7 + 55 Ls with r about 5, the chart's form to both."""
    total = sum(n for _a, n, _h in cracker)
    lc = sum(h for _a, _n, h in cracker) / float(total)
    ls = sum(h for _a, _n, h in mirror) / float(total)
    c = 38 + 7 + CHART + 55 * lc
    s = 5 + 7 + CHART + 55 * ls
    return total, lc, ls, (c + s) / 2.0


if __name__ == "__main__":
    tgt = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")
    cr = score(tgt)
    mirror = cr          # the mirror's ask paths are the cracker's: nothing on any ask's path points further
    for ask, n, h in cr:
        print("%s: %d figures, cracker keeps %d, misses %d" % (ask, n, h, n - h))
    total, lc, ls, pair = ceiling(cr, mirror)
    print("total %d figures, cracker keeps %.1f per cent, mirror leakage %.1f per cent, pair ceiling %.1f"
          % (total, 100 * lc, 100 * ls, pair))
