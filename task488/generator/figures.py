"""Every figure the goldens, the write-up and the checks use, computed once from the shipped tables (solve.py) and
written to figures.json. Nothing downstream is typed."""
from __future__ import annotations

import json
import os

import numpy as np

import pack as PK
import params as P
import solve as S

HERE = os.path.dirname(os.path.abspath(__file__))


def compute(s, tb, full=True):
    gold = S.golden(s)
    F = {"floor": P.FLOOR, "scale_a": int(P.SCALE_A), "scale_b": int(P.SCALE_B), "anchor_threshold_qss": 452}
    T = tb["T"]
    F["rekeyed_items"] = int((T.new_key != "").sum())
    F["access2025_items"] = int(T.acc25.sum())
    F["groups_cleared"] = int(T.eg_removed.sum())
    for g in P.GRADES:
        v = gold[g]
        G = v["G"]
        F["cut_%d" % g] = int(P.CUT_QSS[g])
        F["low_%d" % g] = v["low"]
        F["commission_%d" % g] = v["commission"]
        F["cal_low_%d" % g] = int((G.items.difficulty_qss[G.cal] < G.cut).sum())
        F["wk_low_%d" % g] = int((v["wk_qss"] < G.cut).sum())
        F["wk_items_%d" % g] = int(len(G.wk))
        F["pool_rows_%d" % g] = int(len(G.items))
        F["nearest_pts_%d" % g] = round(float(np.min(np.abs(v["wk_qss"] - G.cut))), 1)
        for w, (mu, sd) in zip([x[0] for x in P.WINDOWS], v["pops"]):
            F["pop_mean_%d_%s" % (g, w)] = round(float(P.SCALE_A + P.SCALE_B * mu), 1)
            F["pop_sd_%d_%s" % (g, w)] = round(float(P.SCALE_B * sd), 1)
        F["responses_%d" % g] = int(G.X.size)
        F["events_%d" % g] = int(G.NE)
    F["call"] = int(sum(F["commission_%d" % g] for g in P.GRADES))
    F["low_total"] = int(sum(F["low_%d" % g] for g in P.GRADES))
    F["wk_items_total"] = int(sum(F["wk_items_%d" % g] for g in P.GRADES))
    F["responses_total"] = int(sum(F["responses_%d" % g] for g in P.GRADES))
    ex = dict(gold=gold)
    if full:
        cat_type = tb["T"].drop_duplicates("key").set_index("key").item_type
        rv = S.rivals(s, gold, catalog=cat_type)
        for k, v in rv.items():
            for g in P.GRADES:
                F["riv_%s_low_%d" % (k, g)] = int(v[g])
            F["riv_%s_call" % k] = int(sum(max(0, P.FLOOR - v[g]) for g in P.GRADES))
        fam, near = S.family(s, gold)
        for k, v in fam.items():
            for g in P.GRADES:
                F["fam_%s_low_%d" % (k, g)] = int(v[g])
                F["fam_%s_near_%d" % (k, g)] = round(near[k][g], 1)
            F["fam_%s_call" % k] = int(sum(max(0, P.FLOOR - v[g]) for g in P.GRADES))
        ac = S.anchor_check(gold)
        for g, res in ac.items():
            for k in ("reported", "jml", "clean_mle", "clean_eap", "golden"):
                F["anchor_%s_low_%d" % (k, g)] = res[k][0]
                F["anchor_%s_mid_%d" % (k, g)] = res[k][1]
            F["anchor_nlow_%d" % g] = res["n_low"]
        ex.update(rivals=rv, family=fam, anchor=ac)
        gm = S.golden(s, mess=True)
        ex["mess"] = int(sum(v["commission"] for v in gm.values()))
        F["mess_call"] = ex["mess"]
    if any(k.startswith("anchor_reported_low_") for k in F):
        F["anchor_golden_max_abs"] = round(max(abs(F["anchor_golden_low_%d" % g]) for g in P.GRADES), 1)
        F["anchor_reported_min_abs"] = round(min(-F["anchor_reported_low_%d" % g] for g in P.GRADES), 1)
        F["anchor_reported_max_abs"] = round(max(-F["anchor_reported_low_%d" % g] for g in P.GRADES), 1)
    imp = S.import_table(s, gold)
    F["import_rows"] = int(len(imp))
    ex["imp"] = imp
    dom, en = PK.ask_truth(tb["T"], tb["G"])
    for (g, d), c in dom.items():
        F["dom_%d_%s" % (g, d)] = c
    for g, (ns, ni) in en.items():
        F["enemy_sets_%d" % g] = ns
        F["enemy_items_%d" % g] = ni
    return F, ex


def write(F, path=os.path.join(HERE, "figures.json")):
    with open(path, "w") as f:
        json.dump(F, f, indent=1, sort_keys=True)
        f.write("\n")
