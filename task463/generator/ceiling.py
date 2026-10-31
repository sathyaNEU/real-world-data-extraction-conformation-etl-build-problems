"""The ask sheet's cracker and mirror, run on the cut pack.

The cracker lands the call, runs the hygiene battery and executes every filed rule: on the coverage ask it grosses up
Calderby's net values at the plan's 5 per cent (2.3), drops Gorsedale's trade rows, and places each return's category
by its name in the office's category map: the hygiene battery (supplemental-stumping 1.1c, a code contradicted by a
finer key, re-derived) catches Wrenfold's reissued codes, whose names disagree with the map's for the same code. The mirror stops at the default path on the call
(the chained index) and takes the same ask paths, the asks consuming nothing the call's construction produces. A figure
is kept when it equals the golden's at the prompt's rounding. Weights 38 / 7 / 55: the ask weight over 18 criteria
(the coverage ask 16, the conformed product-month file 2, which both keep); the mirror's main block 5.

    python3 task463/generator/ceiling.py [target_dir]     (no argument: the figures on target.zip)
"""
import json
import os
import shutil
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import bundle as B     # noqa: E402

TASK = os.path.dirname(HERE)
FILE = 2


def run(target):
    g_cov = B.coverage_figures(target)
    c_cov = B.coverage_figures(target, by_name=True, gross_up=True, retail_only=True)
    keep_b = sum(round(c_cov[i]) == round(g_cov[i]) for i in g_cov)
    n = len(g_cov) + FILE
    lc = (keep_b + FILE) / float(n)
    cracker, mirror = 38 + 7 + 55 * lc, 5 + 7 + 55 * lc
    rows = [("B " + i, round(c_cov[i]), round(g_cov[i])) for i in g_cov]
    return dict(ask_criteria=n, cracker_kept={"B": int(keep_b), "file": FILE},
                cracker=round(cracker, 1), mirror=round(mirror, 1), pair_ceiling=round((cracker + mirror) / 2, 1),
                mirror_leakage_pct=round(100 * lc, 1), rows=rows)


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
