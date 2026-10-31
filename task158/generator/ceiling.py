"""The ask sheet's cracker and mirror, run on the cut pack.

The cracker lands the call, runs the hygiene battery and executes every filed rule (the stopgap policy, its section 6
on out-of-service hours, the lease's Schedule 3). On Ask A it reads both maintenance logs with the console's Amsterdam
times converted and the node's pool at the time, on the cordon and uncordon actions, and so misses the uncordons the
console logs under hand-completed jobs; on Ask B it executes Schedule 3 with the unit column read, the fitted serials
and the handover racks, takes each GPU's last run as its highest run number and reads every run in the export. The
mirror stops at the call's most attractive wrong rung and, the asks being decoupled from the call, meets the same ask
devices. A figure is kept when it lands on the golden's rounding (GPU-hours to 10, hours to 0.1, whole GPUs).

    python3 task158/generator/ceiling.py [target_dir]
"""
import json
import os
import shutil
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import calc as C   # noqa: E402

TASK = os.path.dirname(HERE)
CHART = 4                  # the chart's bars, its pools, its units and title; values move with Ask A's hours


def r10(x):
    return int(round(x / 10.0)) * 10


def run(target):
    gh, glo = C.ask_a(target)
    ch, clo = C.ask_a(target, use_job_complete=False)
    gacc, gheld = C.ask_b(target)
    cacc, cheld = C.ask_b(target, last_by="run", cutoff="none")
    keep_a = sum(r10(ch[p]) == r10(gh[p]) for p in gh) + sum(round(clo[p], 1) == round(glo[p], 1) for p in glo)
    keep_b = sum(cacc[r] == gacc[r] for r in gacc) + (sorted(cheld) == sorted(gheld))
    keep_chart = 2 if keep_a < len(gh) else CHART      # layout and labels kept; the bars carry the missed hours
    total = 2 * len(gh) + len(gacc) + 1 + CHART
    lc = ls = (keep_a + keep_b + keep_chart) / total
    cr, mi = 38 + 7 + 55 * lc, 5 + 7 + 55 * ls
    return dict(cracker_kept={"A": keep_a, "B": keep_b, "chart": keep_chart}, ask_criteria=total,
                cracker=round(cr, 1), mirror=round(mi, 1), pair_ceiling=round((cr + mi) / 2, 1),
                mirror_leakage_pct=round(100 * ls, 1))


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
