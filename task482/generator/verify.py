"""An independent recomputation of every graded figure from the cut pack, written apart from bundle.py (pandas),
compared with generator/figures.json.

    python3 task482/generator/verify.py [target]"""
import json
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)


def main(target=None, gdir=None):
    target = target or os.path.join(TASK, "target")
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    f1a = pd.read_csv(os.path.join(target, "ipeds_f1a_fy2026_finance_lakemoor_public.csv"), dtype={"UNITID": str,
                                                                                                  "IDX_F": str})
    e12 = pd.read_csv(os.path.join(target, "ipeds_e12_2025-26_enrollment_lakemoor_public.csv"), dtype={"UNITID": str})
    codes = pd.read_csv(os.path.join(target, "lhecb_campus_codes_2026.csv"), dtype={"unitid": str})
    ch = pd.read_csv(os.path.join(target, "lhecb_credit_hours_by_level_2025-26.csv"))
    ch = ch.merge(codes[["campus_code", "unitid"]], on="campus_code")
    piv = ch.pivot_table(index="unitid", columns="course_level", values="student_credit_hours", aggfunc="sum")
    piv = piv[["Lower division", "Upper division", "Graduate"]]
    f1a = f1a.set_index("UNITID")
    fte = e12.set_index("UNITID").eval("FTEUG + FTEGD")
    alone = f1a.index[f1a.PRCH_F.isna()]
    coef = np.linalg.lstsq(piv.loc[alone].values.astype(float), f1a.loc[alone, "F1C011"].values.astype(float),
                           rcond=None)[0]
    cost = pd.Series(piv.values @ coef, index=piv.index)
    v = {u: f1a.loc[u, "F1C011"] / fte[u] for u in alone}
    for p in f1a.index[f1a.PRCH_F == 1]:
        mem = [p] + list(f1a.index[f1a.IDX_F == p])
        for u in mem:
            v[u] = f1a.loc[p, "F1C011"] * cost[u] / cost[mem].sum() / fte[u]
    bad = int(sorted(sorted(v, key=v.get)[:5]) != fig["call"]["awarded"])
    for u, x in fig["per_fte_standalone"].items():
        bad += int(round(v[u])) != x
    cen = pd.read_csv(os.path.join(target, "lhecb_fall2026_census_enrollment_branch_campuses.csv"), dtype=str)
    cen = cen.merge(codes[["campus_code", "unitid"]], on="campus_code")
    one = cen.drop_duplicates(["campus_code", "student_id", "meeting_days", "start_time", "instructor_id"])
    one = one.assign(f=one.credit_hours.astype(int) / np.where(one.course_level == "GR", 12.0, 15.0))
    fa = one.groupby("unitid").f.sum()
    hc = cen.drop_duplicates(["unitid", "birth_date", "sex", "home_zip", "first_term"]).groupby("unitid").size()
    for u in fig["ask_a"]:
        bad += "%.1f" % fa[u] != fig["ask_a"][u]
        bad += int(hc[u]) != fig["ask_b"][u]
    print("verify: %d figures differ from figures.json" % bad)
    return bad == 0


if __name__ == "__main__":
    sys.exit(0 if main(sys.argv[1] if len(sys.argv) > 1 else None) else 1)
