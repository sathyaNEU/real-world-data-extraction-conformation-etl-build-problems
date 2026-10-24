"""task279 cracker: the response that landed the call, ran the hygiene battery (key uniqueness, exact duplicates,
unmatched joins, fan-out) and executed every filed rule the asks point at (annex A: the grid points levelled in both
campaigns, 1997 levels less 0.054 m, per-point years; annex B: the logger's 08:00 reading of the 14th and 28th, the
hand reading where the logger has none, depth below the tube top less the register's tube height, three deepest a
hydrological year, eight years, two dipwells a unit). Scored figure by figure against figures.json: a hit is the same
figure at the asked rounding. The mirror (a response on a wrong rung of the call) reads the asks the same way, since
the asks consume nothing the call's construction produces."""
from __future__ import annotations

import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as A   # noqa: E402
import common as K     # noqa: E402


def battery(target):
    """The hygiene battery on the ask files: what it finds is a work order the cracker executes."""
    import csv
    notes = []
    grid = list(csv.DictReader(open(os.path.join(target, K.FILES["grid"]), encoding="utf-8")))
    keys = [(r["unit_code"], r["grid_point"], r["campaign"]) for r in grid]
    notes.append("grid key unique per campaign: %s" % (len(keys) == len(set(keys))))
    one = {}
    for r in grid:
        one.setdefault((r["unit_code"], r["grid_point"]), set()).add(r["campaign"])
    notes.append("grid points with one campaign only (dropped): %d" % sum(1 for v in one.values() if len(v) == 1))
    meta = list(csv.DictReader(open(os.path.join(target, K.FILES["dw_meta"]), encoding="utf-8")))
    notes.append("dipwell register one row a dipwell (no fan-out): %s" %
                 (len({m["dipwell_id"] for m in meta}) == len(meta)))
    return notes


def run(task):
    target = os.path.join(task, "target")
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    low = A.ask_lowering(target, same_place_m=None)                 # every grid point levelled in both campaigns
    glg, _ = A.ask_glg(target, tube_history=False)                 # the register's tube height on every reading
    hits = dict(A=0, B=0)
    rows = []
    for c in K.UNIT_CODES:
        u = fig["units"][c]
        a = A.half_up(low[c], 1) == u["surface_lowering_mm_yr"]
        b = int(A.half_up(glg[c], 0)) == u["glg_cm_below_surface"]
        hits["A"] += a
        hits["B"] += b
        rows.append((u["name"], A.half_up(low[c], 1), u["surface_lowering_mm_yr"], a,
                     int(A.half_up(glg[c], 0)), u["glg_cm_below_surface"], b))
    for n in battery(target):
        print("battery:", n)
    print("%-12s %8s %8s %5s %6s %6s %5s" % ("unit", "A crack", "A gold", "hit", "B crk", "B gold", "hit"))
    for r in rows:
        print("%-12s %8.1f %8.1f %5s %6d %6d %5s" % r)
    n = len(K.UNIT_CODES)
    print("cracker ask hits: A %d of %d, B %d of %d" % (hits["A"], n, hits["B"], n))
    lc = (hits["A"] + hits["B"]) / (2.0 * n)
    pair = (38 + 7 + 55 * lc + 5 + 7 + 55 * lc) / 2
    print("ask weight kept by the cracker and by the mirror: %.1f per cent; pair ceiling %.1f" % (100 * lc, pair))
    return hits


if __name__ == "__main__":
    run(sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(HERE))
