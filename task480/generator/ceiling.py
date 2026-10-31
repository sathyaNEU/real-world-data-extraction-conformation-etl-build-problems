"""The ask sheet's cracker and mirror, run on the cut pack.

The cracker lands the call, runs the hygiene battery and executes every filed rule. On the births it places each
record in the municipality its written city of residence names (every written city is a municipality's name); on the
deaths it takes the registrar's residence code. The mirror stops at the default path (each municipality's 2020 persons
per dwelling) and takes the same readings, the asks consuming nothing the call's construction produces. A figure is
kept when it equals the golden's whole count. The chart's two asked parts (a bar for each municipality's estimate,
the 10,000 line) are kept by both. Weights 38 / 7 / 55, the mirror's main block 5.

    python3 task480/generator/ceiling.py [target_dir]     (no argument: the figures on target.zip)
"""
import json
import os
import shutil
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import asks as A    # noqa: E402
import world as W   # noqa: E402

TASK = os.path.dirname(HERE)
CHART = 2


def run(target):
    bg, bn = A.births(target)
    dg, dn, dc = A.deaths(target)
    names = [m[1] for m in W.MUNIS]
    keep_b = sum(bn[n] == bg[n] for n in names)
    keep_d = sum(dn[n] == dg[n] for n in names)
    total = 2 * len(names) + CHART
    lc = (keep_b + keep_d + CHART) / float(total)
    ls = (keep_b + keep_d + CHART) / float(total)
    cr, mi = 38 + 7 + 55 * lc, 5 + 7 + 55 * ls
    rows = [("births " + W.SHORT[n], bn[n], bg[n]) for n in names] + [("deaths " + W.SHORT[n], dn[n], dg[n]) for n in names]
    return dict(ask_criteria=total, cracker_kept={"births": int(keep_b), "deaths": int(keep_d), "chart": CHART},
                mirror_kept={"births": int(keep_b), "deaths": int(keep_d), "chart": CHART}, cracker=round(cr, 1),
                mirror=round(mi, 1), pair_ceiling=round((cr + mi) / 2, 1), mirror_leakage_pct=round(100 * ls, 1),
                rows=rows)


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
