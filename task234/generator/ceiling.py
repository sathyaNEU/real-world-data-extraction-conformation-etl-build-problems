"""The ask layer's ceiling, measured on the cut pack: each response's ask figures recomputed from target/ with the
handling that response applies, scored against the golden handling on the same files, and the pair priced on the
planning weights (38 for the call and its components, 7 for instruction-following, 55 for the asks).

    python3 task234/generator/ceiling.py

Rows: the cracker lands the escalations, runs the battery (influenza A and B one test, corrections in place, cancelled
orders out, county dates for the week, the merged campus's second identifier, the report of record) and executes every
filed rule, but reads every receipt time as UTC like the extract's two _utc columns (Ask A) and counts a laboratory's
specimens by distinct accession, the protocol's key for a test (Ask B); the mirror stops at rung 0 on the call and
handles the asks the same way, since they carry nothing from the call; the full includer also reads the broker's
clock and the patient and collection keys (a stress row, not the gate). The chart's structure is banked by every
response that draws it."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(os.path.dirname(HERE), "target")
sys.path.insert(0, HERE)
import build as B   # noqa: E402
import estim as E   # noqa: E402

BANKED = 1          # the chart's structure


def figures(D, rep, clock, key):
    tests = E.conform(D, receipt_clock=clock)
    a = E.ask_a(tests, rep)
    gold_tests = E.conform(D)
    b = E.ask_b(gold_tests if key == "specimen" else tests, key=key)
    return {k: round(100 * v, 1) for k, v in a.items()}, b


def kept(resp, gold):
    a, b = resp
    ga, gb = gold
    return sum(a.get(k) == v for k, v in ga.items()) + sum(b.get(k) == v for k, v in gb.items())


def main():
    D = E.load(TARGET, B.FILES)
    rep = E.reports_of_record(D["agg"])
    gold = figures(D, rep, "switch", "specimen")
    n = len(gold[0]) + len(gold[1]) + BANKED
    crack = kept(figures(D, rep, "utc", "accession"), gold) + BANKED
    full = kept(figures(D, rep, "switch", "specimen"), gold) + BANKED
    lc = crack / n
    c = 38 + 7 + 55 * lc
    s = 5 + 7 + 55 * lc          # the mirror's ask handling is the cracker's: the asks carry nothing from the call
    print("cracker (lands the escalations, battery, filed rules; every receipt time read as UTC, specimens by "
          "accession): keeps %d of %d ask criteria, response %.1f" % (crack, n, c))
    print("mirror (rung 0 on the call, same ask handling): keeps %d of %d, response %.1f" % (crack, n, s))
    print("full includer (the broker's clock and the patient and collection keys, stress row): keeps %d of %d, "
          "response %.1f" % (full, n, 38 + 7 + 55 * full / n))
    print("pair ceiling %.1f; mirror leakage %.1f per cent of the ask weight" % ((c + s) / 2, 100 * lc))


if __name__ == "__main__":
    main()
