"""task178 cracker: the careful solver's path on the asks, run on the cut pack, and the pair arithmetic of
supplemental-stumping Part 0. The cracker lands the call, reads every file and dictionary note, converts every datum
the datum sheet states for the file it reads, dedups exact and same-number work orders, and reads each system's times
as the wall-clock times the dictionary describes. The mirror stops on the default path for the call and walks the
same ask path.

    python3 task178/generator/cracker.py task178/target"""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc  # noqa: E402
import common as C  # noqa: E402


def cells(a, b):
    out = {}
    for i, (d, lv, _) in enumerate(a):
        out["A%d date" % (i + 1)] = d
        out["A%d level" % (i + 1)] = "%.2f" % lv
    for y, (c, h) in b.items():
        out["B%d closures" % y] = c
        out["B%d at 11.80" % y] = h
    return out


def main(target):
    gold = cells(calc.ask_a(target), calc.ask_b(target))
    paths = {
        "careful": cells(calc.ask_a(target, bracket=False, telemetry_datum="1995"),
                         calc.ask_b(target, legacy_clock="local", same_tide=False, bracket=False)),
        "careful + bracket offset": cells(calc.ask_a(target, bracket=True, telemetry_datum="1995"),
                                          calc.ask_b(target, legacy_clock="local", same_tide=False, bracket=True)),
        "careful + STND 2026": cells(calc.ask_a(target, bracket=False, telemetry_datum="2026"),
                                     calc.ask_b(target, legacy_clock="local", same_tide=False, bracket=False)),
        "careful + reset work orders merged": cells(calc.ask_a(target, bracket=False, telemetry_datum="1995"),
                                                     calc.ask_b(target, legacy_clock="local", same_tide=True, bracket=False)),
        "careful + legacy clock as UTC": cells(calc.ask_a(target, bracket=False, telemetry_datum="1995"),
                                                calc.ask_b(target, legacy_clock="utc", same_tide=False, bracket=False)),
    }
    n = len(gold)
    keep = {p: sum(1 for k, v in c.items() if gold[k] == v) for p, c in paths.items()}
    for p, x in keep.items():
        print("%-40s keeps %2d of %d ask cells" % (p, x, n))
    lc = keep["careful"] / n
    best_one = max(v for p, v in keep.items() if p != "careful") / n
    r = 5.0
    C_on = 38 + 7 + 55 * lc
    S_off = r + 7 + 55 * lc            # the mirror walks the same ask path
    pair = (C_on + S_off) / 2
    C_one = 38 + 7 + 55 * best_one
    pair_one = (C_one + S_off) / 2
    both_on = (C_on + C_on) / 2
    res = dict(cells=n, keep=keep, pair_ceiling=round(pair, 1), pair_with_one_device=round(pair_one, 1),
               pair_both_on_call=round(both_on, 1), mirror_leakage_pct=round(100 * lc, 1))
    print(json.dumps(res, indent=1))
    return res


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target"))
