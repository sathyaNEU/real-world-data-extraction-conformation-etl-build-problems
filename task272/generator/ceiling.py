"""The ask layer's ceiling, measured on the cut pack: each response's ask figures recomputed from target/ with the
handling that response applies, scored against the golden handling, and the pair priced on the planning weights (38
for the call and its components, 7 for instruction-following, 55 for the asks).

    python3 task272/generator/ceiling.py

Rows: the cracker lands the call, runs the battery (completed fills only, each serial on its station through the
equipment register, every SET_UP joined to the product of the doses filled after it) and executes every filed rule,
but reads the server's fill times as the unit's local time (the column carries no zone) and takes each SET_UP row as
a set; the mirror stays on the capability rung on the call and handles the asks the same way, since they carry
nothing from it; the full includer also converts the fill times from UTC and takes a set as its lot (a stress row,
not the gate). The paper's chart is banked by every response that draws it."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(os.path.dirname(HERE), "target")
sys.path.insert(0, HERE)
import figs as F  # noqa: E402

BANKED = 1


def figures(rec, target, utc, lots):
    a = F.ask_a(rec, utc_as_local=not utc)
    b = F.ask_b(rec, rows_not_lots=not lots, target=target)
    keys_a = sorted(F.ask_a(rec))
    cands = sorted(c for c, p in rec["products"].items() if not p["verified"])
    return [a.get(k, 0) for k in keys_a] + [b.get(c, 0) for c in cands]


def main(target=TARGET):
    rec = F.load(target)
    gold = figures(rec, target, True, True)
    n = len(gold) + BANKED
    crack = sum(x == y for x, y in zip(figures(rec, target, False, False), gold)) + BANKED
    full = sum(x == y for x, y in zip(figures(rec, target, True, True), gold)) + BANKED
    utc_only = sum(x == y for x, y in zip(figures(rec, target, True, False), gold)) + BANKED
    lots_only = sum(x == y for x, y in zip(figures(rec, target, False, True), gold)) + BANKED
    lc = crack / n
    c = 38 + 7 + 55 * lc
    s = 5 + 7 + 55 * lc
    print("cracker (lands the call, battery, filed rules; fill times read as local, each SET_UP row a set): keeps %d "
          "of %d ask criteria, response %.1f" % (crack, n, c))
    print("mirror (the capability rung on the call, same ask handling): keeps %d of %d, response %.1f" % (crack, n, s))
    print("one device each: UTC converted only %d of %d; lots only %d of %d" % (utc_only, n, lots_only, n))
    print("full includer (UTC converted and a set as its lot, stress row): keeps %d of %d, response %.1f"
          % (full, n, 38 + 7 + 55 * full / n))
    print("pair ceiling %.1f; mirror leakage %.1f per cent of the ask weight" % ((c + s) / 2, 100 * lc))
    return (c + s) / 2, 100 * lc


if __name__ == "__main__":
    main()
