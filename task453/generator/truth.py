"""The simulation's own answers for the asks, computed from the generator's records (not from the pack): checks.py
asserts the goldens, which read the pack, equal these."""
import collections

import numpy as np

import sim
import world as W


def levy_truth(ar):
    L = ar["lines"]
    base = collections.defaultdict(int)
    for ln in L:
        if ln["posted"] >= sim.FIRST_POSTING and ln["date"].year == W.YEAR and ln["item"] in sim.INCLUDED:
            base[(ln["ci"], sim.line_abated(ln["ci"], ln["date"]))] += int(round(ln["amount"] * 100))
    for c in ar["credits"]:
        for p in c["lines"]:
            ln = L[p]
            if ln["date"].year == W.YEAR and ln["item"] in sim.INCLUDED:
                base[(ln["ci"], sim.line_abated(ln["ci"], ln["date"]))] -= int(round(ln["amount"] * 100))
    out = {}
    for ci, c in enumerate(W.CREMATORIA):
        un, ab = base[(ci, False)], base[(ci, True)]
        out[c[0]] = int(np.floor((un * W.LEVY_UNABATED + ab * W.LEVY_ABATED) / 100 + 0.5))
    return out


def bypass_truth(cyc, plants):
    out = {}
    for ci, p in plants.items():
        code = W.CREMATORIA[ci][0]
        iv = p["auto"] + p["manual"]
        cnt = collections.Counter()
        for x in cyc:
            if x["ci"] != ci or x["type"] != "CREMATION":
                continue
            if any(x["start"] <= b1 and x["end"] >= b0 for b0, b1 in iv):
                cnt[(x["start"].month - 1) // 3 + 1] += 1
        first_q = 1 if W.CREMATORIA[ci][8] == "A" else (int(W.CREMATORIA[ci][9][5:7]) - 1) // 3 + 1
        out[code] = {"Q%d" % q: cnt[q] for q in range(first_q, 5)}
    return out
