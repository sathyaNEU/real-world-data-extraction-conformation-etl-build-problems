"""Seed search for the world: the calibration family agrees on the counties with room to spare, and every rung a
competent analyst can stop on names another set.

    python3 task274/generator/seedsearch.py [first] [last] [cmed]"""
import sys

import numpy as np

import analysis as A
import world as W


def records(w):
    R = []
    for p in w["P"]:
        if p.get("result") is None:
            continue
        R.append(dict(seqn=p["seqn"], county=p["county"], w=p["wtmec"], value=p["result"], analyzer=p["analyzer"],
                      lot=p["lot"], cal=p["cal"], month=p["run_time"].month))
    pairs = {b["seqn"]: b["result"] for b in w["bridge"]}
    c = w["check"]
    chk = dict(mean=c["mean"], lab=c["lab"], targets=list(W.K.CHECK_TARGETS), cal=c["cal"], lot=c["lot"],
               analyzer=0, month=W.K.CHECK_RUN.month)
    return R, pairs, chk


def assess(w):
    R, pairs, chk = records(w)
    g, info = A.golden(R, pairs, chk)
    G = A.designated(g)
    fam = A.family(R, pairs, chk)
    fam_ok = all(A.designated(v) == G for v in fam.values())
    fam_margin = min(A.margin(v) for v in fam.values())
    rt = A.routes(R, pairs, chk)
    wrong = {k: A.designated(v) != G for k, v in rt.items()}
    cross = {}
    for k, v in rt.items():
        dif = [i for i in range(A.NC) if (v[i] > A.LINE) != (g[i] > A.LINE)]
        cross[k] = max([abs(v[i] - A.LINE) for i in dif], default=0.0)
    true = np.array([0.0] * A.NC)
    den = np.array([0.0] * A.NC)
    for p in w["P"]:
        if p.get("result") is None:
            continue
        den[p["county"]] += p["wtmec"]
        if p["true"] < A.CUTOFF:
            true[p["county"]] += p["wtmec"]
    T = A.designated(true / den)
    bridge_cals = {b["cal"] for b in w["bridge"]}
    minpairs = min(info["n"].get(r["cal"], 0) for r in R)
    return dict(G=G, g=g, fam_ok=fam_ok, fam_margin=fam_margin, wrong=wrong, cross=cross, rt=rt, T=T,
                true=true / den, one_bridge_cal=len(bridge_cals) == 1, minpairs=minpairs, info=info)


if __name__ == "__main__":
    a = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    b = int(sys.argv[2]) if len(sys.argv) > 2 else 40
    cmed = [float(x) for x in sys.argv[3].split(",")] if len(sys.argv) > 3 else None
    strict = ("R0_reported", "R1_check_on_all", "R2_overall_shift", "R3_lot_analyzer",
              "R3b_lot_analyzer_bridge_as_check", "R3c_lot_only", "R3d_lot_plus_analyzer",
              "R4_calibration_bridge_as_check")
    hits = 0
    for sd in range(a, b + 1):
        w = W.simulate(sd, cmed)
        try:
            s = assess(w)
        except (KeyError, ValueError):
            continue
        ok = (s["fam_ok"] and s["fam_margin"] >= 0.015 and s["one_bridge_cal"] and s["minpairs"] >= 2
              and all(s["wrong"][k] and s["cross"][k] >= 0.01 for k in strict))
        tag = "HIT" if ok else ""
        hits += ok
        if ok or b - a < 12:
            print(sd, "G", [x + 1 for x in s["G"]], "T", [x + 1 for x in s["T"]], "fam", s["fam_ok"],
                  "fm %.3f" % s["fam_margin"], "minpairs", s["minpairs"], "month", "wrong" if s["wrong"]["R5_month_analyzer"] else "SAME",
                  " ".join("%s%s" % (k.split("_")[0], "!" if s["wrong"][k] else "=") for k in strict), tag)
            print("    G  ", np.round(100 * s["g"], 1))
            print("    R3 ", np.round(100 * s["rt"]["R3_lot_analyzer"], 1))
            print("    R1 ", np.round(100 * s["rt"]["R1_check_on_all"], 1))
    print("hits", hits, "of", b - a + 1)
