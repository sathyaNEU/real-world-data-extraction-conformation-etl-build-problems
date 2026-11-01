"""The ask layer's ceiling, measured on the cut pack: each response's ask figures recomputed from target/ with the
handling that response applies, scored against the golden, and the pair priced on the planning weights (38 for the
call and its components, 7 for instruction-following, 55 for the asks).

    python3 task122/generator/ceiling.py

Rows: the cracker lands the call, runs the battery (live activations only, New Zealand months, inhibited and test
activations out) and executes every filed rule (a continuing alert counted once where it began, linked by the pair
and the hand-over second; a combined-sector activation in the first-named aircraft's sector; each flight once per
sector), but takes the latest revision of each flight and sector, the natural de-duplication of a crossing list, so a
crossing a later revision no longer flies stays in; the mirror stops at like occupancy on the call and handles the
asks the same way, since they carry nothing from it; the full includer also re-reads each flight's plan as a whole
(a stress row, not the gate). The paper's chart is banked by every response that draws it."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import figs as F  # noqa: E402
import params as P  # noqa: E402

BANKED = 1


def figures(D, revisions):
    c = F.crossings(D, revisions)
    st = F.activations(D, c)
    h = F.ask_hours(c)
    r = F.ask_rates(st, h)
    fl = F.ask_flights(c)
    out = []
    for s in P.SECTORS:
        out += [int(round(v)) for v in h[s]]
    for s in P.SECTORS:
        out += [round(v, 1) for v in r[s]]
    out += [fl[s] for s in P.SECTORS]
    return out


def main(target=F.TARGET):
    D = F.load(target)
    gold = figures(D, "flight")
    n = len(gold) + BANKED
    crack = sum(x == y for x, y in zip(figures(D, "pair"), gold)) + BANKED
    full = sum(x == y for x, y in zip(figures(D, "flight"), gold)) + BANKED
    lc = crack / n
    c = 38 + 7 + 55 * lc
    s = 5 + 7 + 55 * lc
    print("cracker (lands the call, battery, filed rules; the latest revision of each flight and sector): keeps %d of "
          "%d ask criteria, response %.1f" % (crack, n, c))
    print("mirror (like occupancy on the call, same ask handling): keeps %d of %d, response %.1f" % (crack, n, s))
    print("full includer (each flight's plan read as a whole, stress row): keeps %d of %d, response %.1f"
          % (full, n, 38 + 7 + 55 * full / n))
    print("pair ceiling %.1f; mirror leakage %.1f per cent of the ask weight" % ((c + s) / 2, 100 * lc))
    return (c + s) / 2, 100 * lc


if __name__ == "__main__":
    main()
