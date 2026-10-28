"""The world's own answer, kept out of the pack: each app's 2027 revenue with the limit less without it, carried on from
the extract by the generator itself, and the analyst test run on the world's clean records (the free accounts over
three projects at their own upgrade rate, nobody leaving)."""
import json

import numpy as np

import params as P
import world as W


def analyst_test(world):
    """the easy route on the clean panel: the share of free accounts over three projects that are on Plus a year
    later, applied to every app's accounts over three projects for twelve months at the Plus price"""
    rows = {m: (ids, st, k) for (m, ids, ap, st, k, s, d, sn) in world["panel_rows"]}
    m0 = P.M_EXTRACT - 12 - 12
    ids0, st0, k0 = rows[m0]
    heavy0 = set(int(x) for x, s_, kk in zip(ids0, st0, k0) if s_ == 0 and kk >= 4)
    ids1, st1, k1 = rows[m0 + 12]
    paid1 = set(int(x) for x, s_ in zip(ids1, st1) if s_ == 1)
    share = len(heavy0 & paid1) / float(len(heavy0))
    heavy = world["heavy_%d" % P.M_EXTRACT]
    return {a: float(heavy[i] * 12 * share * P.PLUS[i]) for i, a in enumerate(P.APPS)}


def write(world, path):
    t = W.truth(world)
    out = {"add": {a: float(t["add"][i]) for i, a in enumerate(P.APPS)},
           "paid_months": {a: float(t["paid_months"][i]) for i, a in enumerate(P.APPS)},
           "free_months": {a: float(t["free_months"][i]) for i, a in enumerate(P.APPS)},
           "stock_dec_2026": {a: int(t["stock_dec"][i]) for i, a in enumerate(P.APPS)},
           "analyst_test": analyst_test(world)}
    with open(path, "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
        fh.write("\n")
    return out
