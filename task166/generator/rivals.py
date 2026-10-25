"""task166's rivals beyond the ladder, on the shipped files (calc.py): the curves fitted on 2023 to 2026 alone,
gradient-boosted trees on the home equity loans' own fields (with and without the region) and on the stack's own fields,
a long-run payoff rate, and the two book screens (the book behind first mortgages, or stacks, above the 2027 rate).
Prints each route's 2027 figures by region, the region it names and its margin; the design note's Ladder section quotes
these lines.

    python3 task166/generator/rivals.py [target]"""
from __future__ import annotations

import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc as C          # noqa: E402


def main(target):
    from sklearn.ensemble import HistGradientBoostingClassifier
    pd.set_option("display.width", 220)
    gold, ctx = C.golden(target)
    H, FW, curt = ctx["H"], ctx["FW"], ctx["curt"]
    he = C.he_posted_monthly(target)
    ph = C.plan_he(target)
    H = C.add_own(H, he)
    FW = C.add_own(FW, he, ph)
    regs = C.REG_ORDER
    res = {"golden": gold}
    rec = H[H.t >= C.mo(2023, 1)]
    for nm, cov in (("own rate, fitted on 2023 to 2026", ["own"]), ("first alone, fitted on 2023 to 2026", ["first"]),
                    ("blend, fitted on 2023 to 2026", ["blend"])):
        f = C.fit(rec, cov)
        res[nm] = C.project(FW, f.predict(C.design(FW, cov)), curt)
    funded = ctx["los"].funded_date.str[:4].astype(int) * 12 + ctx["los"].funded_date.str[5:7].astype(int) - 1
    for df in (H, FW):
        df["age2"] = df.key.map(funded)
        df["age2"] = df.t - df.age2
        for k, r in enumerate(regs):
            df["reg%d" % k] = (df.region == r).astype(float)
    for nm, feats in (("trees, the home equity loan's own fields", ["r2", "H", "m1", "p1", "cal", "age2", "n2"]),
                      ("trees, own fields and region", ["r2", "H", "m1", "p1", "cal", "age2", "n2", "reg1", "reg2", "reg3"]),
                      ("trees, the stack's fields", ["r1", "r2", "F", "H", "m1", "p1", "cal", "young"]),
                      ("trees, the stack's fields and both incentives",
                       ["r1", "r2", "F", "H", "m1", "p1", "cal", "young", "own", "first"])):
        for sd in (0, 1):
            g = HistGradientBoostingClassifier(max_iter=200, learning_rate=0.08, random_state=sd)
            g.fit(H[feats].values, H.y.values)
            res["%s, seed %d" % (nm, sd)] = C.project(FW, g.predict_proba(FW[feats].values)[:, 1], curt)
    bk = ctx["book"].merge(ctx["los"][["region"]], left_on="key", right_index=True)
    lr = H[H.y == 1].groupby("region").H.sum() / (H.groupby("region").H.sum() / 12.0) / (H.t.nunique() / 12.0)
    res["long-run payoff rate on the book"] = (lr * bk.groupby("region").bal.sum() / 1e6).reindex(regs)
    fw0 = FW[FW.t == C.mo(2026, 12)]
    avg27 = np.mean([ctx["plan"][C.mo(2027, k)] for k in range(1, 13)])
    res["book behind firsts above the 2027 rate"] = (fw0[fw0.r1 > avg27].groupby("region").H.sum() / 1e6).reindex(regs)
    res["book behind stacks above the 2027 rate"] = \
        (fw0[(fw0.blend + fw0.m1) > avg27].groupby("region").H.sum() / 1e6).reindex(regs)
    R = pd.DataFrame(res).T
    R["names"] = R[regs].astype(float).idxmax(axis=1)
    s = np.sort(R[regs].values.astype(float), axis=1)
    R["margin"] = np.round(s[:, -1] / s[:, -2], 2)
    print(R.round(1).to_string())
    return R


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target"))
