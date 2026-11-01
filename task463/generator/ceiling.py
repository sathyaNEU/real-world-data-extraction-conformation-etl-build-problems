"""The ask sheet's cracker and mirror, run on the cut pack.

The cracker lands the call, runs the hygiene battery and executes every filed rule: on the coverage ask it grosses up
Calderby's net values at the plan's 5 per cent (2.3), drops Gorsedale's trade rows, and, finding Wrenfold's category
numbers contradicted by the names beside them against the office's map, re-derives each category from its name (the
battery's repair of a code a finer key contradicts, supplemental-stumping 1.1c) in both halves of the year. Wrenfold's
report prints the names of the categories holding the numbers since its July 2025 renumbering, so the repair is right
for the second half and wrong for the first, whose sales were recorded under the numbers' 2024 meanings. The mirror
stops at the default path on the call (the chained index) and takes the same ask paths, the asks consuming nothing the
call's construction produces. A figure is kept when it equals the golden's at the prompt's rounding. Weights 38 / 7 /
55: the ask weight over 18 criteria (the coverage ask 16, the conformed product-month file 2, which both keep); the
mirror's main block 5. The stress rows (the number join in both halves, and the full includer who reads the first half
by number and the second by name) are printed beside the gate, never in it.

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


def whole(x):
    return int(x // 1 + (1 if x % 1 >= 0.5 else 0))


def kept(c, g):
    return sum(whole(c[i]) == whole(g[i]) for i in g)


def run(target):
    g_cov = B.coverage_figures(target)
    c_cov = B.coverage_figures(target, wren="name", gross_up=True, retail_only=True)
    keep_b = kept(c_cov, g_cov)
    n = len(g_cov) + FILE
    lc = (keep_b + FILE) / float(n)
    cracker, mirror = 38 + 7 + 55 * lc, 5 + 7 + 55 * lc
    rows = [("B " + i, whole(c_cov[i]), whole(g_cov[i])) for i in g_cov]
    stress = {
        "number join in both halves": kept(B.coverage_figures(target, wren="code"), g_cov),
        "full includer (first half by number, second by name)": kept(g_cov, g_cov),
        "names in both halves, trade rows kept, Calderby left net":
            kept(B.coverage_figures(target, wren="name", gross_up=False, retail_only=False), g_cov),
    }
    return dict(ask_criteria=n, cracker_kept={"B": int(keep_b), "file": FILE},
                cracker=round(cracker, 1), mirror=round(mirror, 1), pair_ceiling=round((cracker + mirror) / 2, 1),
                mirror_leakage_pct=round(100 * lc, 1), rows=rows,
                stress_rows_kept_of_16=stress,
                full_includer_pair=round((38 + 7 + 55 + 5 + 7 + 55) / 2, 1))


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
