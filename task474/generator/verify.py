"""An independent recomputation of the call and every ask figure from target.zip, written apart from figs.py.

    python3 task474/generator/verify.py
"""
import io
import json
import os
import sys
import zipfile

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)


def main():
    fig = json.load(open(os.path.join(HERE, "figures.json"), encoding="utf-8"))
    z = zipfile.ZipFile(os.path.join(TASK, "target.zip"))
    reg = pd.read_csv(io.BytesIO(z.read("heatwise_candidate_register_2026-10-12.csv")), dtype=str).fillna("")
    reg["person"] = reg.groupby(["surname", "initials", "date_of_birth"], sort=False).ngroup()
    br = pd.read_csv(io.BytesIO(z.read("brindle_theory_results_2020-2026.csv")), dtype=str)
    br = br[br.status == "SAT"].merge(reg[["brindle_candidate_id", "person"]], left_on="candidate_id",
                                      right_on="brindle_candidate_id", how="left")
    assert br.person.notna().all()
    br["date"] = pd.to_datetime(br.sitting_date, format="%d/%m/%Y")
    br["score"] = br.scaled_score.astype(int)
    br["paper"] = "old"
    hg = pd.DataFrame(json.loads(z.read("harrowgate_theory_sittings_2026-04_2026-09.json"))["sittings"])
    hg = hg[hg.review.isin(["cleared", "released"])].drop_duplicates("sitting_ref")
    hg = hg.merge(reg[["harrowgate_candidate_id", "person"]], left_on="candidate_id",
                  right_on="harrowgate_candidate_id", how="left")
    t = pd.to_datetime(hg.started_at, utc=True).dt.tz_convert("Europe/London")
    hg["date"] = pd.to_datetime(t.dt.date)
    hg["score"] = hg.raw_mark.astype(int)
    hg["paper"] = "new"
    s = pd.concat([br[["person", "date", "score", "paper"]], hg[["person", "date", "score", "paper"]]])
    s = s.sort_values(["person", "date", "paper"]).reset_index(drop=True)
    s["k"] = s.groupby("person").cumcount()
    n_old = s[s.paper == "old"].groupby("person").size()
    first_new = s[s.paper == "new"].groupby("person").first()
    # cross-switch: one Brindle sitting, a fail, then Harrowgate's paper
    old1 = s[(s.paper == "old")].groupby("person").first()
    cs = first_new.join(old1, rsuffix="_old", how="inner")
    cs = cs[(n_old.reindex(cs.index) == 1) & (cs.score_old < 65)]
    # history: first sitting a Brindle fail dated 2021 to 2025, then a second Brindle sitting
    o = s[s.paper == "old"].copy()
    o["j"] = o.groupby("person").cumcount()
    f1 = o[o.j == 0].set_index("person")
    f2 = o[o.j == 1].set_index("person")
    h = f1.join(f2, rsuffix="_2", how="inner")
    h = h[(h.score < 65) & (h.date.dt.year.between(2021, 2025))]
    rate = h.groupby("score").apply(lambda g: (g.score_2 >= 65).mean())
    p = rate.reindex(cs.score_old).dropna().mean()
    marks = cs.score.to_numpy()
    mark = min(y for y in range(0, 62) if (marks >= y).mean() <= p + 1e-12)
    bad = 0

    def check(label, a, b):
        nonlocal bad
        good = a == b
        bad += not good
        print("%s  %s  %s %s" % ("ok  " if good else "FAIL", label, a, "" if good else "(figures.json %s)" % b))
    check("the pass mark", mark, fig["call"]["pass_mark"])
    check("the equivalent share", round(float(p), 4), fig["call"]["p_equivalent"])
    check("cross-switch candidates", len(cs), fig["call"]["n_cross_switch"])
    y26 = s[(s.date >= "2026-01-01") & (s.date <= "2026-09-30")]
    for m in range(1, 10):
        g = y26[y26.date.dt.month == m]
        k = "2026-%02d" % m
        check("%s first time" % k, int((g.k == 0).sum()), fig["ask_a"][k]["first_time"])
        check("%s resitting" % k, int((g.k > 0).sum()), fig["ask_a"][k]["resitting"])
    firsts = s[(s.k == 0) & (s.paper == "old")]
    for y in range(2021, 2026):
        g = firsts[firsts.date.dt.year == y]
        check("%d first sat" % y, int(len(g)), fig["ask_b"][str(y)]["first_time"])
        check("%d passed" % y, int((g.score >= 65).sum()), fig["ask_b"][str(y)]["passed"])
    print("%d failures" % bad)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
