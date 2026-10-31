"""The ask layer's ceiling, measured on the cut pack: each response's ask figures recomputed from target/ with the
handling that response applies, scored against the golden, and the pair priced on the planning weights (38 for the
call and its components, 7 for instruction-following, 55 for the asks).

    python3 task127/generator/ceiling.py

Rows: the cracker lands the split, runs the hygiene battery (latest submission, dates by the evening, postcodes
normalised, the BRK join, day-first dates) and executes every filed rule, but reads each spell's nights at the
spell's own site and a Closed referral as not started; the mirror stops at R1 and handles the asks the same way,
since they carry nothing from the call; the full includer also finds both primaries (a stress row, not the gate)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(os.path.dirname(HERE), "target")
sys.path.insert(0, HERE)
import analysis as AN  # noqa: E402

CHART = 2          # the chart's structural criteria, banked by every response that draws it


def scored(target, site_from, spot):
    gold_a, gold_p = AN.ask_a(target), AN.ask_a(target, patients=True)
    gold_b = AN.ask_b(target)[0]
    a = AN.ask_a(target, site_from=site_from)
    p = AN.ask_a(target, site_from=site_from, patients=True)
    b = AN.ask_b(target, spot=spot)[0]
    hits = sum(a[k] == gold_a[k] for k in gold_a) + sum(p[k] == gold_p[k] for k in gold_p) + \
        sum(b[k] == gold_b[k] for k in gold_b)
    n = len(gold_a) + len(gold_p) + len(gold_b) + CHART
    return hits + CHART, n


def main():
    crack, n = scored(TARGET, "spell", False)
    full, _ = scored(TARGET, "wards", True)
    lc = crack / n
    c = 38 + 7 + 55 * lc
    s = 5 + 7 + 55 * lc          # the mirror's ask handling is the cracker's: the asks carry nothing from the call
    print("cracker (lands the split, battery, filed rules; spell site, Closed as not started): keeps %d of %d ask "
          "criteria, response %.1f" % (crack, n, c))
    print("mirror (off the split at R1, same ask handling): keeps %d of %d, response %.1f" % (crack, n, s))
    print("full includer (also finds A1 and B1, stress row): keeps %d of %d, response %.1f" % (full, n, 38 + 7 + 55 * full / n))
    print("pair ceiling %.1f; mirror leakage %.1f per cent of the ask weight" % ((c + s) / 2, 100 * lc))


if __name__ == "__main__":
    main()
