"""An independent recomputation of every graded figure from the cut pack, written apart from bundle.py (pandas and
its own Newton scoring), compared with generator/figures.json.

    python3 task479/generator/verify.py [target]"""
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
    r1 = pd.read_csv(os.path.join(target, "quantilis_spring2026_item_responses_through_2026-03-27.csv"))
    r2 = pd.read_csv(os.path.join(target, "quantilis_spring2026_item_responses_from_2026-03-30.csv"))
    r = pd.concat([pd.DataFrame({"s": r1.StudentID, "seq": r1.ItemSeq, "item": r1.ItemID, "u": r1.Scored,
                                 "t": r1.ResponseTimeMs / 1000}),
                   pd.DataFrame({"s": r2.student_id, "seq": r2.item_seq, "item": r2.item_id, "u": r2.score,
                                 "t": r2.response_time_s})])
    bank = pd.read_csv(os.path.join(target, "quantilis_item_bank_2025-26.csv")).set_index("item_id")
    r = r.join(bank[["a", "b", "c"]], on="item").sort_values(["s", "seq"])
    ids = r.s.unique()
    shape = (len(ids), 40)
    U, T, A, Bm, C = (r[k].to_numpy().reshape(shape) for k in ("u", "t", "a", "b", "c"))
    M = T >= 4.0
    th = np.zeros(len(ids))
    for _ in range(80):
        p = C + (1 - C) / (1 + np.exp(-1.7 * A * (th[:, None] - Bm)))
        g = (1.7 * A * (p - C) / (p * (1 - C)) * (U - p) * M).sum(1)
        h = ((1.7 * A) ** 2 * ((p - C) / (1 - C)) ** 2 * (1 - p) / p * M).sum(1)
        th = np.clip(th + np.clip(g / np.maximum(h, 1e-9), -1, 1), -3.75, 3.75)
    sc = pd.Series(np.clip(np.round(500 + 40 * th), 350, 650), index=ids)
    sp = pd.read_csv(os.path.join(target, "quantilis_spring2026_score_report.csv")).set_index("student_id")
    share = (sc < 470).groupby(sp.loc[ids, "campus_id"].values).mean()
    bad = 0
    for c, v in share.items():
        bad += "%.1f" % (100 * v) != fig["below_basic_pct"][c]
    bad += sorted(c for c, v in share.items() if v >= 0.35) != fig["call"]["designated"]
    fall = pd.read_csv(os.path.join(target, "quantilis_fall2025_score_report.csv"))
    tmp = pd.read_csv(os.path.join(target, "quantilis_temporary_id_register_fall2025.csv"))
    rf = pd.read_csv(os.path.join(target, "bellweather_sis_roster_2025-10-01.csv"))
    rs = pd.read_csv(os.path.join(target, "bellweather_sis_roster_2026-03-01.csv"))
    key = ["last_name", "first_name", "birth_date"]
    t2o = tmp.merge(rf, on=key).set_index("temporary_student_id").student_id
    fall["sid"] = fall.student_id.map(lambda s: t2o.get(s, s))
    fall = fall.sort_values(["test_date", "student_id"]).groupby("sid").last()
    agg = fall.groupby("campus_id").agg(n=("scale_score", "size"), p=("scale_score", lambda v: (v >= 520).mean()))
    for c, row in agg.iterrows():
        bad += int(row.n) != fig["ask_a"][c]["tested"]
        bad += "%.1f" % (100 * row.p) != fig["ask_a"][c]["proficient_pct"]
    xw = pd.read_csv(os.path.join(target, "bellweather_sis_id_crosswalk_2026-01-05.csv")).set_index("legacy_student_id").student_id
    o2n = rf.merge(rs, on=key, suffixes=("_o", "_n")).set_index("student_id_o").student_id_n
    fall["new"] = [xw.get(s, o2n.get(s)) for s in fall.index]
    win = pd.read_csv(os.path.join(target, "quantilis_winter2026_score_report.csv")).set_index("student_id")
    j = fall.dropna(subset=["new"]).join(win, on="new", rsuffix="_w", how="inner")
    j["g"] = j.scale_score_w - j.scale_score
    for c, grp in j.groupby("campus_id_w"):
        bad += len(grp) != fig["ask_b"][c]["students"]
        bad += "%.1f" % grp.g.mean() != fig["ask_b"][c]["growth"]
    print("verify: %d figures differ from figures.json" % bad)
    return bad == 0


if __name__ == "__main__":
    sys.exit(0 if main(sys.argv[1] if len(sys.argv) > 1 else None) else 1)
