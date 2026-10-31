"""The ask sheet's cracker and mirror, run on the cut pack.

The cracker lands the call, runs the hygiene battery and executes every filed rule. On Ask A it nets Corvane's
reversals as the code values file and B.4.1(a) direct and joins each fill to the Fund's member by cardholder and person
code, the natural join, in the member's attributed member months; on Ask B it reads the clinician roster with its
"with partner since" dates. The mirror stops at the default path and takes the same joins, the asks consuming nothing the
call's construction produces. A figure is kept when it lands on the golden's rounding (dollars to the nearest thousand,
shares to one decimal place). The chart's four parts (bars, target line, call colouring, title) are the cracker's, who
lands the call; the mirror keeps the bars and the line. Weights 38 / 7 / 55, the mirror's main block 5.

    python3 task451/generator/ceiling.py [target_dir]     (no argument: the figures on target.zip)
"""
import json
import os
import shutil
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import calc as C     # noqa: E402
import golden as G   # noqa: E402

TASK = os.path.dirname(HERE)
CHART = 4


def r1000(v):
    return int(round(v / 1000.0)) * 1000


def run(target):
    X = G.compute(target)
    gn = X["group_npi"]
    gold_rx, gold_sh = X["rx"], X["share"]
    crack_rx = C.ask_pharmacy(X["L"], X["att"], "person_code", X["elig"])
    crack_sh = C.ask_leakage(X["L"], X["d26"], gn, "since")
    keep_a = sum(r1000(crack_rx[c]) == r1000(gold_rx[c]) for c in gold_rx)
    keep_b = sum(round(crack_sh[c], 1) == round(gold_sh[c], 1) for c in gold_sh)
    total = len(gold_rx) + len(gold_sh) + CHART
    lc = (keep_a + keep_b + CHART) / float(total)
    ls = (keep_a + keep_b + 2) / float(total)
    cr, mi = 38 + 7 + 55 * lc, 5 + 7 + 55 * ls
    return dict(ask_criteria=total, cracker_kept={"A": int(keep_a), "B": int(keep_b), "chart": CHART},
                mirror_kept={"A": int(keep_a), "B": int(keep_b), "chart": 2}, cracker=round(cr, 1),
                mirror=round(mi, 1), pair_ceiling=round((cr + mi) / 2, 1), mirror_leakage_pct=round(100 * ls, 1))


def main():
    if len(sys.argv) > 1:
        print(json.dumps(run(sys.argv[1]), indent=1))
        return
    tmp = tempfile.mkdtemp()
    try:
        with zipfile.ZipFile(os.path.join(TASK, "target.zip")) as z:
            z.extractall(tmp)
        print(json.dumps(run(tmp), indent=1))
    finally:
        shutil.rmtree(tmp)


if __name__ == "__main__":
    main()
