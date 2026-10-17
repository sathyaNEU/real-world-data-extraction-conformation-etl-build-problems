"""task241 pair measurement on the cut pack: the cracker (lands the call, runs the hygiene battery, executes every filed
rule) and the mirror (stops at the default path on the call) each answer both asks the way that path does, and every
ask figure is scored against the golden (a count is a hit only when exact). Prints the cracker sheet, the mirror's
leakage and the pair ceiling.

    python3 task241/generator/pair.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build as B
import estim as E

TARGET = os.path.join(os.path.dirname(HERE), "target")
R_MISS = 8.0                      # recommendation weight a response on a wrong rung keeps (critical components it shares)


def main():
    D = E.load(TARGET, B.FILES)
    gold_a, gold_b = E.ref_casts_2000(D), E.timely_by_month(D)
    paths = {
        # the cracker: exact-duplicate and key checks find nothing in either reference source, the RHD depths taken to
        # pressure from the stated unit; the delivery record executed as filed (complete file, the array's ascending
        # profiles, the receipt log's stated Lisbon clock) with the profile's own time as the surfacing time
        "cracker": (E.ref_casts_2000(D, dedup=None), E.timely_by_month(D, anchor="juld")),
        # the mirror, careful on the asks as the cracker is
        "mirror": (E.ref_casts_2000(D, dedup=None), E.timely_by_month(D, anchor="juld")),
        # the mirror, careless on the asks: depths read as pressure, the first file of a resent profile
        "mirror_careless": (E.ref_casts_2000(D, dedup=None, convert=False),
                            E.timely_by_month(D, anchor="juld", version="first")),
    }
    n = len(gold_a) + len(gold_b)
    keep = {}
    for k, (a, b) in paths.items():
        hits = [("A %d" % y) for y in gold_a if a[y] == gold_a[y]] + [("B %d" % m) for m in gold_b if b[m] == gold_b[m]]
        keep[k] = len(hits) / n
        print("%-16s keeps %d of %d ask figures %s" % (k, len(hits), n, hits))
    lc, ls = keep["cracker"], max(keep["mirror"], keep["mirror_careless"])
    c, s = 38 + 7 + 55 * lc, R_MISS + 7 + 55 * ls
    print("Pair ceiling: %.1f" % ((c + s) / 2))
    print("Mirror leakage: %.1f per cent of ask weight" % (100 * ls))
    return (c + s) / 2, 100 * ls


if __name__ == "__main__":
    main()
