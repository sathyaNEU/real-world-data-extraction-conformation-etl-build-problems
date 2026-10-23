"""The cracker and mirror sheets on the cut pack: the response that lands the call, runs the hygiene battery and executes
every filed rule (the cracker), and the response on the default path (the mirror), scored figure by figure against
generator/figures.json, a hit within half a unit of the asked rounding.

    python3 task275/generator/cracker.py"""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import asks as AS     # noqa: E402
import common as K    # noqa: E402

TASK = os.path.dirname(HERE)


def score(target):
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    seg = fig["segments"]
    # the cracker: 2025 landings by landing date (terms 4.3), every sales note line it holds after the battery's
    # repeat sweep (no key repeats, no line repeating another's lot, weight and price), and the VMS reports on the
    # vessel the extract names, UK days outside port limits
    a = AS.first_sale(target, drop=AS.exact_repeats(target), by="landing")
    b = AS.days_at_sea(target, attribution="label")
    rows = []
    for s in K.SEG:
        ga, gb = seg[s]["first_sale_gbp_thousands"], seg[s]["days_at_sea"]
        rows.append(("A first-sale value %s" % s, round(a[s], 1), ga, abs(round(a[s], 1) - ga) < 0.05))
        rows.append(("B days at sea %s" % s, b[s], gb, b[s] == gb))
    hits = sum(r[3] for r in rows)
    lc = hits / len(rows)
    ls = lc          # the mirror reads the asks as the cracker does: they consume nothing the call produces
    crack = 38 + 7 + 55 * lc
    mirror = 5 + 7 + 55 * ls
    return rows, hits, (crack + mirror) / 2, ls


if __name__ == "__main__":
    rows, hits, pair, ls = score(os.path.join(TASK, "target"))
    for name, got, want, hit in rows:
        print("%-28s cracker %-10s golden %-10s %s" % (name, got, want, "HIT" if hit else "miss"))
    print("cracker keeps %d of %d ask figures; mirror leakage %.1f per cent; pair ceiling %.1f"
          % (hits, len(rows), 100 * ls, pair))
