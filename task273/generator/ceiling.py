"""The ask layer's ceiling, measured on the cut pack: each response's ask figures recomputed from target/ with the
handling that response applies, scored against the golden handling on the same files, and the pair priced on the
planning weights (38 for the call and its components, 7 for instruction-following, 55 for the asks).

    python3 task273/generator/ceiling.py

Rows: the cracker lands the call and runs the battery (the UTC interval stamps to NZ local time, the PB2 CT meter's
multiplier from the ICP register, the totaliser rollovers, the missed polls), reads each council meter as the bore
the permit's Schedule 1 lists against it, leaves the meter with no Schedule 1 entry out, and splits each shared
switchboard's electricity by its pumps' run hours; the mirror stops at the distance rung on the call and handles
the asks the same way, since nothing in them comes from the call; the full includer also matches every meter to the
bore whose SCADA take it tracks and weights the split by motor rating (a stress row, not the gate)."""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(os.path.dirname(HERE), "target")
sys.path.insert(0, HERE)
import analysis as A  # noqa: E402


def figures(P, match, split):
    m = A.ask_meters(P, match=match)
    e = A.ask_energy(P, split=split, meters=m)
    return ({k: int(round(v)) for k, v in m.items()},
            {k: (int(round(v)) if not math.isnan(v) else None) for k, v in e.items()})


def kept(resp, gold):
    return sum(resp[0][k] == v for k, v in gold[0].items()) + sum(resp[1][k] == v for k, v in gold[1].items())


def main(target=TARGET):
    P = A.Pack(target)
    gold = figures(P, True, "hours_kw")
    n = len(gold[0]) + len(gold[1])
    crack = kept(figures(P, False, "hours"), gold)
    full = kept(figures(P, True, "hours_kw"), gold)
    lc = crack / n
    c = 38 + 7 + 55 * lc
    s = 5 + 7 + 55 * lc
    print("cracker (lands the call, battery, Schedule 1 meters, run-hour split): keeps %d of %d ask criteria, "
          "response %.1f" % (crack, n, c))
    print("mirror (the distance rung, same ask handling): keeps %d of %d, response %.1f" % (crack, n, s))
    print("full includer (meters matched to SCADA, motor-weighted split, stress row): keeps %d of %d, response %.1f"
          % (full, n, 38 + 7 + 55 * full / n))
    print("pair ceiling %.1f; mirror leakage %.1f per cent of the ask weight" % ((c + s) / 2, 100 * lc))
    return (c + s) / 2, 100 * lc


if __name__ == "__main__":
    main()
