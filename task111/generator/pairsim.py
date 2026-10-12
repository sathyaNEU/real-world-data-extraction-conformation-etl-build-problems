"""Pair simulation against a modelled rubric, calibrated to the v2 portal result (both responses on the
cross-day trace, the call missed, the pair in the 60s).

Rubric model (weights out of 100, one criterion per graded cell):
  recommendation 35: the cause 8, its count 5, the change 5, the quarter's leader not recurring 7, the winter
      zero 5, the runner-up over the peak 5. A response on the cross-day trace that misses the call still shows
      322 and 571 in its family table, so it keeps the count (5) and half the leader criterion (3.5).
  instruction following 7.
  asks 58: every family's misses, credits and complaints (21 cells, 1.6 each), the six patch cells (1.2 each),
      the chart's go-live line 4, worst week with its count 5, the title as the finding 4, the seven-family
      split 4.2.

Sheets: the main path (forward = the golden call; q3cracker = the cross-day trace with Rota & cover carried
into the peak; mirror = the same-day trace), crossed with a path on each ask: credits, complaints, weeks.

    python3 pairsim.py [target_dir]
"""
import datetime as dt
import json
import sys
from collections import Counter
from pathlib import Path

import askpaths
import golden as G

D = dt.date
HERE = Path(__file__).resolve().parent
CELL, PATCH = 1.6, 1.2


def score(main, fam_ok, cred_ok, comp_ok, patch_ok, week_ok):
    s = 7.0
    if main == "forward":
        s += 35
    elif main == "q3cracker":
        s += 5 + 3.5
    else:
        s += 5
    s += CELL * (fam_ok + cred_ok + comp_ok) + PATCH * patch_ok
    s += 4 + (5 if week_ok else 0) + (4 if main == "forward" else 0) + (4.2 if main != "mirror" else 0)
    return round(s, 1)


def sheets(T):
    out, Gd, q3 = G.golden(T)
    gf, gc, gq = out["family_counts"], out["credits_by_family"], out["complaints_by_family"]
    allq = G.trace(Gd, D(2026, 6, 1), D(2026, 9, 30))
    CP = askpaths.credit_paths(Gd, q3, allq)
    QP = askpaths.complaint_paths(Gd, q3)
    same = G.trace(Gd, D(2026, 7, 1), D(2026, 9, 30), cross_day=False)
    sf = Counter(f for f, _ in same.values())
    worst = askpaths.weekly_worst(Gd, 3)
    iso = askpaths.weekly_worst(Gd, 0)

    def right(path_counts, gold, fams):
        return sum(1 for f in G.FAMILIES if f in fams and round(path_counts.get(f, 0)) == gold.get(f, 0))
    mirror_fams = {f for f in G.FAMILIES if sf.get(f, 0) == gf.get(f, 0)}
    res = {}
    for main in ("forward", "q3cracker", "mirror"):
        fams = set(G.FAMILIES) if main != "mirror" else mirror_fams
        patch_ok = 6 if main == "forward" else 0
        for cp in CP:
            for qp in QP:
                if qp == "any_category":
                    continue
                for wk, w_ok in (("planning", True), ("iso", worst == iso)):
                    res[(main, cp, qp, wk)] = score(main, len(fams), right(CP[cp], gc, fams), right(QP[qp], gq, fams),
                                                    patch_ok, w_ok)
    return res, {"credits": {p: right(CP[p], gc, G.FAMILIES) for p in CP},
                 "complaints": {p: right(QP[p], gq, G.FAMILIES) for p in QP if p != "any_category"}}


def report(T):
    res, cells = sheets(T)
    best = lambda m: res[(m, "golden", "golden", "planning")]
    careful = lambda m: res[(m, "single_hit", "refs_resolved", "planning")]
    rows = {
        "q3cracker, every ask right": best("q3cracker"),
        "q3cracker, careful (credits by matched line, complaints by reference, planning weeks)": careful("q3cracker"),
        "q3cracker, careful but ISO weeks": res[("q3cracker", "single_hit", "refs_resolved", "iso")],
        "q3cracker, credits right, complaints by reference": res[("q3cracker", "golden", "refs_resolved", "planning")],
        "q3cracker, complaints right, credits by matched line": res[("q3cracker", "single_hit", "golden", "planning")],
        "forward, every ask right": best("forward"),
        "forward, careful": careful("forward"),
        "mirror, every ask right": best("mirror"),
    }
    pairs = {
        "two q3crackers, every ask right (ceiling)": best("q3cracker"),
        "two q3crackers, careful": careful("q3cracker"),
        "q3cracker every ask right + q3cracker careful": (best("q3cracker") + careful("q3cracker")) / 2,
        "forward careful + q3cracker careful": (careful("forward") + careful("q3cracker")) / 2,
        "forward every ask right + q3cracker every ask right": (best("forward") + best("q3cracker")) / 2,
    }
    return {"sheets": rows, "pairs": {k: round(v, 1) for k, v in pairs.items()}, "cells_right": cells}


if __name__ == "__main__":
    T = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE.parent / "target"
    print(json.dumps(report(T), indent=1))
