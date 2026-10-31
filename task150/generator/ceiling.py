"""The ask sheet's cracker and mirror, run on the cut pack.

The cracker lands the call (the golden placements and needs), runs the hygiene battery and executes every filed rule:
on Ask A it applies Policy FEA-R2 2 (f) to the sections (one room in one session, open on October 1 with a pupil
enrolled) and reads each class's grade off its sections' course codes; on Ask B it applies 2 (g) and places the
roster's children by the roster's own key, the case school. The mirror stops at the default path (five-year grade
progression ratios) and takes the same ask paths, the asks consuming nothing the call's construction produces. A figure
is kept when it equals the golden's whole number. The call block (the seven schools' placements and needs) weighs 32,
instructions 7, the asks 61: the 22 ask figures 52 and the chart's structural parts (the panels, the history, a
projection line, the capacity lines) 9, which both keep.

    python3 task150/generator/ceiling.py [target_dir]     (no argument: the figures on target.zip)
"""
import json
import os
import shutil
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import calc as C    # noqa: E402

TASK = os.path.dirname(HERE)
W_CALL, W_IF, W_ASKS, W_CHART = 32.0, 7.0, 52.0, 9.0


def run(target):
    M = C.main_call(target, B=0)
    D = M["D"]
    gold, dflt = M["golden"], M["default"]
    n = len(D.codes)
    kept_call_mirror = sum(int(dflt["alloc"][i]) == int(gold["alloc"][i]) for i in range(n)) + \
        sum(int(dflt["need"][i]) == int(gold["need"][i]) for i in range(n))
    A = C.ask_a(target, D.codes)
    B = C.ask_b(target, D.names)
    st, sb = A["stops"], B["stops"]
    crack_a = sum(1 for k in A["golden"] if st["classes banded by course code"][k] == A["golden"][k])
    crack_b = sum(1 for s in B["sites"] for q in ("children", "classrooms")
                  if sb["roster by case school"][s][q] == B["golden"][s][q])
    n_ask = len(A["golden"]) + 2 * len(B["sites"])
    asks_kept = (crack_a + crack_b) / float(n_ask)
    cracker = W_CALL + W_IF + W_ASKS * asks_kept + W_CHART
    mirror = W_CALL * kept_call_mirror / (2.0 * n) + W_IF + W_ASKS * asks_kept + W_CHART
    rows = [("A " + str(k), st["classes banded by course code"][k], A["golden"][k]) for k in sorted(A["golden"])]
    rows += [("B %s %s" % (s, q), sb["roster by case school"][s][q], B["golden"][s][q]) for s in B["sites"]
             for q in ("children", "classrooms")]
    return dict(ask_figures=n_ask, cracker_kept=int(crack_a + crack_b), mirror_call_criteria_kept=int(kept_call_mirror),
                cracker=round(cracker, 1), mirror=round(mirror, 1), pair_ceiling=round((cracker + mirror) / 2, 1),
                mirror_leakage_pct=round(100 * (W_ASKS * asks_kept + W_CHART) / (W_ASKS + W_CHART), 1), rows=rows)


def main():
    if len(sys.argv) > 1:
        print(json.dumps(run(sys.argv[1]), indent=1, default=str))
        return
    tmp = tempfile.mkdtemp()
    try:
        with zipfile.ZipFile(os.path.join(TASK, "target.zip")) as z:
            z.extractall(tmp)
        print(json.dumps(run(tmp), indent=1, default=str))
    finally:
        shutil.rmtree(tmp)


if __name__ == "__main__":
    main()
