"""The ask layer's ceiling, measured on the cut pack: each response's ask figures recomputed from target/ with the
handling that response applies, scored against the golden handling on the same files, and the pair priced on the
planning weights (38 for the call and its components, 7 for instruction-following, 55 for the asks).

    python3 task138/generator/ceiling.py

Rows: the cracker lands the call and runs the battery: it applies each meter's multiplier from the register to every
day, takes the meter data system's feeder as recorded (the register agrees with it row for row), puts the supplier's
UTC interval ends on CDT, sums the two transformer recorders that Exhibit A puts on the 24.9 kV side and drops the
one repeated T2 stamp as a duplicate. The mirror stops on the pilot's all-hours relief and handles the asks the same
way, since nothing in them comes from the call. Stress rows (not the gate): the tracer also rebuilds the sections
SO-2026-114 moved through the register's device connectivity; the full includer also takes each June meter's whole
kWh before its set date and moves the T2 replacement recorder's stamps."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(os.path.dirname(HERE), "target")
sys.path.insert(0, HERE)
import analysis as A  # noqa: E402


def r10(x):
    return int(round(x / 10.0)) * 10


def asks(target, reassign, mult_from_set, realign, days):
    e = [r10(x) for x in A.feeder_energy(target, reassign=reassign, mult_from_set=mult_from_set)]
    p = A.demand_peaks(target, days, realign=realign, dedupe=not realign)
    return e, [round(p[d][0], 1) for d in days.index]


def kept(resp, gold):
    return sum(a == b for a, b in zip(resp[0], gold[0])) + sum(a == b for a, b in zip(resp[1], gold[1]))


def main(target=TARGET):
    days, _ = A.hottest_days(target)
    gold = asks(target, True, True, True, days)
    n = len(gold[0]) + len(gold[1])
    crack = kept(asks(target, False, False, False, days), gold)
    tracer = kept(asks(target, True, False, False, days), gold)
    full = kept(asks(target, True, True, True, days), gold)
    lc = crack / float(n)
    c = 38 + 7 + 55 * lc
    s = 5 + 7 + 55 * lc
    print("cracker (lands the call; multipliers on every day, feeders as recorded, CDT, T1 + T2, duplicate stamp "
          "dropped): keeps %d of %d ask criteria, response %.1f" % (crack, n, c))
    print("mirror (all-hours relief rung, same ask handling): keeps %d of %d, response %.1f" % (crack, n, s))
    print("tracer (also rebuilds the moved sections from the device tree): keeps %d of %d, response %.1f"
          % (tracer, n, 38 + 7 + 55 * tracer / float(n)))
    print("full includer (every reconstruction, stress row): keeps %d of %d, response %.1f"
          % (full, n, 38 + 7 + 55 * full / float(n)))
    print("pair ceiling %.1f; mirror leakage %.1f per cent of the ask weight" % ((c + s) / 2, 100 * lc))
    return (c + s) / 2, 100 * lc


if __name__ == "__main__":
    main()
