"""The ask layer's ceiling, measured on the cut pack: each response's ask figures recomputed from target/ with the
handling that response applies, scored against the golden handling on the same files, and the pair priced on the
planning weights (38 for the call and its components, 7 for instruction-following, 55 for the asks).

    python3 task125/generator/ceiling.py

Rows: the cracker lands the call, runs the battery (UTC read as local time, officer-started events left out,
cancelled units timed from dispatch to clear) and executes every filed definition, Directive PO-14's ward sentence
included (a call outside the City's wards belongs to none), but takes each unit's crew from the roster's tour of the
dispatch's own date; the mirror stops at the 2026 count on the call and handles the ask the same way, since it
carries nothing from it; the full includer also dates a night tour by the evening it starts (a stress row, not the
gate)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(os.path.dirname(HERE), "target")
sys.path.insert(0, HERE)
import analysis as A  # noqa: E402


def kept(resp, gold):
    return sum(resp[i][k] == v for i in range(len(gold)) for k, v in gold[i].items())


def main(target=TARGET):
    P = A.Pack(target)
    gold = A.asks(P)
    n = sum(len(g) for g in gold)
    crack = kept(A.asks(P, by_district=False, naive_tour=True), gold)
    full = kept(A.asks(P), gold)
    lc = crack / n
    c = 38 + 7 + 55 * lc
    s = 5 + 7 + 55 * lc
    print("cracker (lands the call, battery, filed definitions; crews from the dispatch's own date): keeps %d of %d "
          "ask criteria, response %.1f" % (crack, n, c))
    print("mirror (the 2026 count on the call, same ask handling): keeps %d of %d, response %.1f" % (crack, n, s))
    print("full includer (night tours dated by the evening they start, stress row): keeps %d of %d, response %.1f"
          % (full, n, 38 + 7 + 55 * full / n))
    print("pair ceiling %.1f; mirror leakage %.1f per cent of the ask weight" % ((c + s) / 2, 100 * lc))
    return (c + s) / 2, 100 * lc


if __name__ == "__main__":
    main()
