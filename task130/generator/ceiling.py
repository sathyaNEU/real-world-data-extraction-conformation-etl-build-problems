"""The ask layer's ceiling, measured on the cut pack: each response's ask figures recomputed from target/ with the
handling that response applies, scored against the golden handling on the same files at the prompt's rounding, and
the pair priced on the planning weights (38 for the call and its components, 7 for instruction-following, 55 for
the asks).

    python3 task130/generator/ceiling.py

Rows: the cracker lands the call, runs the battery (UTC stamps converted to Pacific time, county holidays from the
holidays file, closed-premises calls kept out of the return timeliness count) and executes every filed rule (the plan's
measures, the fee schedule's first visit included and its rate by visit date), but dates each return inspection by
its record in the inspection system (Ask A), measures a complaint from the report its investigation carries (Ask B)
and charges the return visits the inspection system holds (Ask C); the mirror stops at rung 0 on the call and handles
the asks the same way, since they carry nothing from the call; the full includer also takes the day sheets' dates,
each complaint's first notice and the closed-premises letters (a stress row, not the gate)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(os.path.dirname(HERE), "target")
sys.path.insert(0, HERE)
import analysis as AN   # noqa: E402


def figures(D, sheets, first_notice, letters):
    a, _ = AN.ask_a(TARGET, D, use_daysheet=sheets)
    b, _ = AN.ask_b(TARGET, D, first_notice=first_notice)
    c = AN.ask_c(TARGET, D, use_letters=letters, use_daysheet=sheets)
    return ({d: round(v, 1) for d, v in a.items()}, {d: round(v, 1) for d, v in b.items()},
            {d: int(c.get(d, 0)) for d in a})


def kept(resp, gold):
    return sum(resp[i].get(d) == v for i in range(3) for d, v in gold[i].items())


def main():
    D = AN.load(TARGET)
    gold = figures(D, True, True, True)
    n = sum(len(g) for g in gold)
    crack = kept(figures(D, False, False, False), gold)
    full = kept(gold, gold)
    lc = crack / n
    c = 38 + 7 + 55 * lc
    s = 5 + 7 + 55 * lc          # the mirror's ask handling is the cracker's: the asks carry nothing from the call
    print("cracker (lands the call, battery, filed rules; the system's own return dates, the dispatched report, the "
          "system's return visits): keeps %d of %d ask criteria, response %.1f" % (crack, n, c))
    print("mirror (rung 0 on the call, same ask handling): keeps %d of %d, response %.1f" % (crack, n, s))
    print("full includer (day sheets, first notice, closed-premises letters; stress row): keeps %d of %d, response "
          "%.1f" % (full, n, 38 + 7 + 55 * full / n))
    print("pair ceiling %.1f; mirror leakage %.1f per cent of the ask weight" % ((c + s) / 2, 100 * lc))


if __name__ == "__main__":
    main()
