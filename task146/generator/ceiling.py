"""task146 architecture 2: the ask layer's cracker and the pair ceiling, run on the cut pack (target/).

The cracker is the careful hygiene route with the field's method: account cohorts (no money followed across a
closure) and the product code read off the register's first row for each code (ES02 as Easy Saver Online throughout).
The full includer follows the money and reads ES02 by date. Each is scored on the graded ask figures of figures.json.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import golden as G  # noqa: E402

FIG = json.load(open(os.path.join(HERE, "figures.json")))
D = G.load(os.path.join(TASK, "target"))


def undated(D):
    """ES02 read as Easy Saver throughout (the register's first ES02 row)."""
    cut = D["keys"].index((2025, 7))
    E = dict(D)
    E["fam"] = {k: ("Easy Saver" if v == "Young Saver" and k[1] >= cut else v) for k, v in D["fam"].items()}
    return E


def score(res):
    hit = tot = 0
    for f in G.FAMILIES:
        tot += 1
        hit += int(round(res["now"].get(f, 0.0) / 1e6) == FIG["now_m"][f])
    tot += 1
    hit += int(round(res["book"] / 1e6) == FIG["book_m"])
    for k in G.HORIZONS:
        for f in list(G.FAMILIES) + ["total"]:
            tot += 1
            hit += int(round(res["stable"][k][f] / 1e6) == FIG["stable_m"][str(k)][f])
    return hit, tot


cr = G.stable(undated(D), money=False)
fi = G.stable(D, money=True)
ch, ct = score(cr)
fh, ft = score(fi)
asks = 58.0
call = 35.0
inst = 7.0
missed = inst + asks * ch / ct
landed = call + inst + asks * fh / ft
print("cracker keeps %d of %d ask figures; full includer %d of %d" % (ch, ct, fh, ft))
print("a response off the call scores about %.1f, one on it about %.1f" % (missed, landed))
print("Pair ceiling: %.1f (one response on the call, one off)" % ((missed + landed) / 2))
print("Mirror leakage: %.1f (the share of ask figures the cracker keeps)" % (100.0 * ch / ct))
