"""The ask layer's ceiling, measured on the cut pack: each response's ask figures recomputed from target/ with the
handling that response applies, scored against the golden handling on the same files, and the pair priced on the
planning weights (38 for the call and its components, 7 for instruction-following, 55 for the asks).

    python3 task160/generator/ceiling.py

Rows: the cracker lands the call and runs the battery (the queue's UTC stamps to Eastern time, the padded export
range cut to the local quarter, the alert reference's zero padding, Schedule B 3.2's desk time read off each
session's claim and close stamps), reads each session's ward off the point of care through Corvane's own location
map, and counts each signed-off task as a review; the mirror stops at the silent-mode rung on the call and handles
the asks the same way, since nothing in them comes from the call; the handle-time row is the cracker who sums the
platform's handle minutes instead (a stress row); the full includer takes each session's ward from the alert it
carries and counts each task's overridden alerts in the alert history (the golden, a check row)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(os.path.dirname(HERE), "target")
sys.path.insert(0, HERE)
import analysis as A  # noqa: E402


def figures(P, ward, time, count):
    a = P.ask_a(ward=ward, time=time)
    b = P.ask_b(count=count)
    return ({u: int(v + 0.5) for u, v in a.items()}, dict(b))


def kept(resp, gold):
    return (sum(resp[0][k] == v for k, v in gold[0].items()) + sum(resp[1][k] == v for k, v in gold[1].items()))


def main(target=TARGET):
    P = A.Pack(target)
    gold = figures(P, "alert", "timestamps", "alerts")
    n = len(gold[0]) + len(gold[1])
    if n == 0:
        raise SystemExit("ceiling: no ask figure to score (nothing to measure); refusing to print a ceiling")
    crack = kept(figures(P, "map", "timestamps", "tasks"), gold)
    hand = kept(figures(P, "map", "handle_all", "tasks"), gold)
    full = kept(gold, gold)
    lc = crack / n
    c = 38 + 7 + 55 * lc
    s = 5 + 7 + 55 * lc
    print("cracker (lands the call, battery, Corvane's location map, a review per signed-off task): keeps %d of %d "
          "ask criteria, response %.1f" % (crack, n, c))
    print("mirror (the silent-mode rung, same ask handling): keeps %d of %d, response %.1f" % (crack, n, s))
    print("handle-time cracker (sums the platform's handle minutes, stress row): keeps %d of %d" % (hand, n))
    print("full includer (ward from each alert, alerts counted per task, check row): keeps %d of %d" % (full, n))
    print("pair ceiling %.1f; mirror leakage %.1f per cent of the ask weight" % ((c + s) / 2, 100 * lc))
    return (c + s) / 2, 100 * lc, crack, n


if __name__ == "__main__":
    main()
