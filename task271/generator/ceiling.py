"""The ask layer's ceiling, measured on the cut pack: each response's ask figures recomputed from target/ with the
handling that response applies, scored against the golden handling on the same files, and the pair priced on the
planning weights (38 for the call and its components, 7 for instruction-following, 55 for the asks).

    python3 task271/generator/ceiling.py

Rows: the cracker lands the call and runs the battery (the two UTC loggers found by their warmest hour and moved to
Pacific time, each split trip's load shared by the drop crew's nets, the dead at the drop taken off, the lake names
matched through the register), reads each trip sheet raceway number in the numbering the crosswalk puts in force on
the trip date, and files each logger's readings under the station its download names; the mirror stops at the plain
count expansion on the call and handles the asks the same way, since nothing in them comes from the call; the full
includer also reads the raceway each trip emptied from the Monday inventory and splits each logger's record at its
deployments (a stress row, not the gate)."""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(os.path.dirname(HERE), "target")
sys.path.insert(0, HERE)
import analysis as A  # noqa: E402


def r100(x):
    return int(math.floor(x / 100.0 + 0.5) * 100)


def figures(raceways, mode):
    rel = {c: r100(v) for c, v in A.releases(TARGET, raceways=raceways).items()}
    warm, _ = A.warm_days(TARGET, mode=mode)
    return rel, warm


def kept(resp, gold):
    return (sum(resp[0].get(k) == v for k, v in gold[0].items()), sum(resp[1].get(k) == v for k, v in gold[1].items()))


def main():
    gold = figures("golden", "golden")
    n = len(gold[0]) + len(gold[1])
    ck = kept(figures("in_force", "site"), gold)
    fk = kept(figures("golden", "golden"), gold)
    lc = sum(ck) / n
    c = 38 + 7 + 55 * lc
    s = 5 + 7 + 55 * lc
    print("ask criteria: %d (releases %d, warm days %d)" % (n, len(gold[0]), len(gold[1])))
    print("cracker (lands the call, battery, numbering in force, download stations): keeps %d of %d release figures "
          "and %d of %d warm-day figures, response %.1f" % (ck[0], len(gold[0]), ck[1], len(gold[1]), c))
    print("mirror (the plain expansion on the call, same ask handling): keeps %d of %d, response %.1f" % (sum(ck), n, s))
    print("full includer (inventory-read raceways, deployment-split loggers; stress row): keeps %d of %d, response %.1f"
          % (sum(fk), n, 38 + 7 + 55 * sum(fk) / n))
    print("pair ceiling %.1f; mirror leakage %.1f per cent of the ask weight" % ((c + s) / 2, 100 * lc))
    return (c + s) / 2, 100 * lc


if __name__ == "__main__":
    main()
