"""The ask layer's ceiling, measured on the cut pack: each response's ask figures recomputed from target/ with the
handling that response applies, scored cell by cell against the golden handling on the same files (first-aid cases
are whole numbers, so a cell is kept only when it is exact), and the pair priced on the planning weights (38 for the
call and its components, 7 for instruction-following, 55 for the asks).

    python3 task130/generator/ceiling.py

Rows. The cracker lands the call and runs the hygiene battery on the asks: it stacks the two case systems, keeps
each case's latest revision, keeps the new system's copy of a migrated case, drops linked recurrences and mutual-aid
work, places each injury on the worker's crew or team on its injury date, and runs the duplicate check a careful
solver runs, records of one worker on one injury date taken as one injury at its most serious class. It never
pairs a nurse-line case with the supervisor's case of the injury it came from when the call was made on a later
day. The mirror stops at rung 0 on the call and handles the asks the same way, since they carry nothing from the
call. The lazy row counts every first-aid record. The one-day and two-day rows pair a nurse-line case with a
supervisor's case up to one or two days before the call (stress rows). The full includer pairs every nurse-line
case with the supervisor's case of the same worker in the three days before its call (the golden handling)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(os.path.dirname(HERE), "target")
sys.path.insert(0, HERE)
import analysis as AN   # noqa: E402
import world as W       # noqa: E402


def cells(A):
    return [A[dd]["quarters"][q] for dd in W.DISTRICTS for q in range(3)] + [A[dd]["total"] for dd in W.DISTRICTS]


def kept(resp, gold):
    return sum(1 for a, b in zip(cells(resp), cells(gold)) if a == b)


def lazy(D, every):
    """Every first-aid record a case of its own (no duplicate check at all)."""
    T = {dd: [0, 0, 0] for dd in W.DISTRICTS}
    for c in every:
        if c["cls"] != "FA" or not c["pinewater"] or c["recur"]:
            continue
        for q, (a, b) in enumerate(AN.QUARTERS):
            if a <= c["date"] <= b:
                T[c["district"]][q] += 1
    return {dd: dict(quarters=v, total=sum(v)) for dd, v in T.items()}


def main(target=TARGET):
    D = AN.load(target)
    every = AN.attach(AN.cases(D), D)
    gold = AN.asks(D, every, AN.MATCH_DAYS)
    n = len(cells(gold))
    rows = {
        "cracker": AN.asks(D, every, None),
        "lazy": lazy(D, every),
        "one-day window": AN.asks(D, every, 1),
        "two-day window": AN.asks(D, every, 2),
        "full includer": AN.asks(D, every, AN.MATCH_DAYS),
    }
    k = {name: kept(r, gold) for name, r in rows.items()}
    lc = k["cracker"] / n
    c = 38 + 7 + 55 * lc
    s = 5 + 7 + 55 * lc
    print("cracker (lands the call, runs the battery, one injury per worker and injury date): keeps %d of %d ask "
          "cells, response %.1f" % (k["cracker"], n, c))
    print("mirror (rung 0 on the call, same ask handling): keeps %d of %d, response %.1f" % (k["cracker"], n, s))
    for name in ("lazy", "one-day window", "two-day window", "full includer"):
        print("%s: keeps %d of %d (stress row; on the call it scores %.1f)" % (name, k[name], n, 45 + 55 * k[name] / n))
    print("pair ceiling %.1f; mirror leakage %.1f per cent of the ask weight" % ((c + s) / 2, 100 * lc))
    print("golden %s" % {dd: gold[dd] for dd in W.DISTRICTS})
    print("cracker %s" % {dd: rows["cracker"][dd] for dd in W.DISTRICTS})
    return dict(kept=k, n=n, pair=(c + s) / 2, leakage=100 * lc, rows=rows, gold=gold)


if __name__ == "__main__":
    main()
