"""The ask sheet's measurement: the cracker (lands the call, runs the hygiene battery, takes every ask at its file's
face) and the mirror (stops at the line-level rung and handles the asks the same way), scored cell by cell against
figures.json at half a unit of the stated rounding, and the pair ceiling under the rubric's weights.

    python3 task302/generator/pair.py task302/target
"""
import json
import os
import sys

import pandas as pd

import build as B
import solve as S

HERE = os.path.dirname(os.path.abspath(__file__))
REC, INSTR, ASK = 38.0, 7.0, 55.0
R_WRONG = 5.0


def face_asks(target):
    """The asks at the files' face: the trial export's on_hand the opening stock throughout; the store list's opening
    hours all year; each dispatch advice's pallets taken once."""
    t = pd.read_csv(os.path.join(target, B.FILES["trial"]))
    t["date"] = pd.to_datetime(t.date)
    A = {}
    for st in S.TRIAL_STORES:
        x = t[t.store_no == st]
        b = int((x[x.date < S.TRIAL_LIVE].on_hand == 0).sum())
        a = int((x[x.date >= S.TRIAL_LIVE].on_hand == 0).sum())
        A[st] = (a, round(100 * (a / b - 1), 1))
    s = pd.read_csv(os.path.join(target, B.FILES["stops"]))
    stores = pd.read_csv(os.path.join(target, B.FILES["stores"]))
    opens = dict(zip(stores.store_no, stores.opens))
    arr = pd.to_datetime(s.arrived)
    hhmm = arr.dt.strftime("%H:%M")
    reg = dict(zip(stores.store_no, stores.island))
    Bv = s[[h > opens[n] for h, n in zip(hhmm, s.store_no)]].groupby(s.store_no.map(reg)).size()
    po = pd.read_csv(os.path.join(target, B.FILES["po"]))
    grn = pd.read_csv(os.path.join(target, B.FILES["grn"]))
    ln = pd.read_csv(os.path.join(target, B.FILES["lines"]))
    cat = dict(zip(ln.article, ln.category))
    g = grn.drop_duplicates("delivery_ref")
    C = g.assign(cat=g.article.map(cat), m=pd.to_datetime(g.received).dt.to_period("M").astype(str)).groupby(
        ["cat", "m"]).pallets.sum()
    return A, Bv, C


def score(F, A, Bv, C):
    hits = {"A": 0, "B": 0, "C": 0}
    n = {"A": 6, "B": len(F["ask_late_stops"]), "C": 36}
    for st in S.TRIAL_STORES:
        v = F["ask_trial"][str(st)]
        hits["A"] += int(A[st][0] == v["after"]) + int(abs(A[st][1] - v["change_pct"]) < 0.05)
    for g, v in F["ask_late_stops"].items():
        hits["B"] += int(int(Bv.get(g, 0)) == v)
    for c, qs in F["ask_pallets"].items():
        for q, v in qs.items():
            hits["C"] += int(int(C[(c, q)]) == v)
    return hits, n


def main(target):
    F = json.load(open(os.path.join(HERE, "figures.json")))
    hits, n = score(F, *face_asks(target))
    cells = sum(n.values())
    kept = sum(hits.values()) / cells
    cracker = REC + INSTR + ASK * kept
    mirror = R_WRONG + INSTR + ASK * kept
    print("cracker sheet: ask A %d of %d, ask B %d of %d, ask C %d of %d" % (hits["A"], n["A"], hits["B"], n["B"],
                                                                         hits["C"], n["C"]))
    print("cracker %.1f, mirror %.1f, pair ceiling %.1f, mirror leakage %.1f per cent of ask weight"
          % (cracker, mirror, (cracker + mirror) / 2, 100 * kept))
    for name in ("A", "B", "C"):
        c2 = REC + INSTR + ASK * (sum(hits.values()) + n[name]) / cells
        print("if the cracker also finds %s: cracker %.1f, pair %.1f" % (name, c2, (c2 + mirror) / 2))
    return hits, n


if __name__ == "__main__":
    main(sys.argv[1])
