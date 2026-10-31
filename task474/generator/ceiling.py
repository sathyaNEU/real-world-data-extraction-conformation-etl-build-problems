"""The ask layer's ceiling, measured on the cut pack: each response's ask figures recomputed from target/ with the
handling that response applies, scored against the golden handling, and the pair priced on the planning weights (38
for the call and its components, 7 for instruction-following, 55 for the asks).

    python3 task474/generator/ceiling.py

Rows: the cracker lands the call, runs the battery (Brindle's SAT rows only, Harrowgate's held records set aside and
each sitting once, UK local dates) and executes every filed rule, but takes each board number as a candidate, so a
candidate who re-registered after a lapse is a new candidate at the later sitting; the mirror stays on the first-time
pass-rate rung on the call and handles the asks the same way, since they carry nothing from it; the full includer also
ties board numbers sharing a surname, initials and date of birth (a stress row, not the gate). The paper's chart is
banked by every response that draws it."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(os.path.dirname(HERE), "target")
sys.path.insert(0, HERE)
import figs as F  # noqa: E402

BANKED = 1


def figures(target, identity):
    people, _ = F.load(target, identity=identity)
    a = F.ask_a(people)
    b = F.ask_b2(people)
    return [v for k in sorted(a) for v in a[k]] + [v for k in sorted(b) for v in b[k]]


def main(target=TARGET):
    gold = figures(target, "name_dob")
    n = len(gold) + BANKED
    crack = sum(x == y for x, y in zip(figures(target, "board"), gold)) + BANKED
    full = sum(x == y for x, y in zip(figures(target, "name_dob"), gold)) + BANKED
    lc = crack / n
    c = 38 + 7 + 55 * lc
    s = 5 + 7 + 55 * lc
    print("cracker (lands the call, battery, filed rules; each board number a candidate): keeps %d of %d ask "
          "criteria, response %.1f" % (crack, n, c))
    print("mirror (the first-time pass-rate rung on the call, same ask handling): keeps %d of %d, response %.1f"
          % (crack, n, s))
    print("full includer (board numbers tied by name and date of birth, stress row): keeps %d of %d, response %.1f"
          % (full, n, 38 + 7 + 55 * full / n))
    print("pair ceiling %.1f; mirror leakage %.1f per cent of the ask weight" % ((c + s) / 2, 100 * lc))
    return (c + s) / 2, 100 * lc


if __name__ == "__main__":
    main()
