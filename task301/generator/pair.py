"""The ask sheet's measurement: the cracker (lands the call, runs the hygiene battery, takes every ask at its file's
face) and the mirror (stops at the pilot-gradient rung and handles the asks the same way), each scored cell by cell
against figures.json at half a unit of the stated rounding, and the pair ceiling under the rubric's weights.

    python3 task301/generator/pair.py task301/target
"""
import json
import os
import sys

import numpy as np
import pandas as pd

import build as B
import solve as S

HERE = os.path.dirname(os.path.abspath(__file__))
REC, INSTR, ASK = 38.0, 7.0, 55.0          # rubric weights: recommendation and components, instruction, asks
R_WRONG = 5.0                               # what a wrong call keeps of the recommendation weight


def face_asks(target):
    """The asks taken at the files' face: Quitline's own sub-region; every dialler leg a call and its stamp the
    clock; every answered leg's minutes summed."""
    q = pd.read_csv(os.path.join(target, B.FILES["quitline"]), dtype=str, keep_default_na=False)
    q = q[q.month.str[:4] == "2025"].copy()
    q["quarter"] = "Q" + ((q.month.str[5:7].astype(int) - 1) // 3 + 1).astype(str)
    q["referrals"] = q.referrals.astype(int)
    A = q[q.phn_sub_region.isin(S.CANDS)].pivot_table(index="phn_sub_region", columns="quarter", values="referrals",
                                                      aggfunc="sum").reindex(S.CANDS)
    d = pd.read_csv(os.path.join(target, B.FILES["dialler"]), dtype={"patient_key": str})
    d["st"] = pd.to_datetime(d.started)
    d = d.drop_duplicates()
    ev = d[d.st.dt.hour >= 17]
    Bv = pd.DataFrame({"calls": ev.groupby(ev.st.dt.day_name()).size(),
                       "reached": ev[ev.result == "Answered"].groupby(ev.st.dt.day_name()).patient_key.nunique()}
                      ).reindex(S.WEEKDAYS)
    a = d[d.result == "Answered"]
    m = a.st.dt.month
    C = (a.groupby(m).duration_s.sum() / 60.0) / a.groupby(m).patient_key.nunique()
    return A, Bv, C


def score(F, A, Bv, C):
    hits = {"A": 0, "B": 0, "C": 0}
    n = {"A": 16, "B": 10, "C": 10}
    for g in S.CANDS:
        for qq in ("Q1", "Q2", "Q3", "Q4"):
            hits["A"] += int(abs(A.loc[g, qq] - F["ask_referrals"][g][qq]) < 0.5)
    for dname in S.WEEKDAYS:
        hits["B"] += int(abs(Bv.loc[dname, "calls"] - F["ask_evening"][dname]["calls"]) < 0.5)
        hits["B"] += int(abs(Bv.loc[dname, "reached"] - F["ask_evening"][dname]["reached"]) < 0.5)
    for i, (mth, v) in enumerate(F["ask_talk_min"].items()):
        hits["C"] += int(abs(C.iloc[i] - v) < 0.05)
    return hits, n


def main(target):
    F = json.load(open(os.path.join(HERE, "figures.json")))
    A, Bv, C = face_asks(target)
    hits, n = score(F, A, Bv, C)
    cells = sum(n.values())
    kept = sum(hits.values()) / cells
    cracker = REC + INSTR + ASK * kept
    mirror = R_WRONG + INSTR + ASK * kept
    print("cracker sheet: ask A %d of %d, ask B %d of %d, ask C %d of %d" % (hits["A"], n["A"], hits["B"], n["B"],
                                                                         hits["C"], n["C"]))
    print("cracker %.1f, mirror %.1f, pair ceiling %.1f, mirror leakage %.1f per cent of ask weight"
          % (cracker, mirror, (cracker + mirror) / 2, 100 * kept))
    # a cracker that also finds each device alone, one at a time
    for name, k in (("ask A found", n["A"]), ("ask B found", n["B"]), ("ask C found", n["C"])):
        c2 = REC + INSTR + ASK * (sum(hits.values()) + k) / cells
        print("if the cracker also finds %s: cracker %.1f, pair %.1f" % (name.split()[1], c2, (c2 + mirror) / 2))
    return hits, n


if __name__ == "__main__":
    main(sys.argv[1])
