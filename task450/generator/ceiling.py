"""The ask sheet's cracker and mirror, run on the cut pack.

The cracker lands the call, runs the hygiene battery (key uniqueness, duplicates, unmatched joins, fan-out) and executes
every filed rule (the designation rules, the technical report's scoring and conversion, the key correction). On Ask A it
joins the 2025 file's campus codes to the campus directory, which every code joins; on Ask B it counts the district ids
enrolled in the window with no 2026 result, each id as its own student. The mirror stops at the call's most attractive
wrong rung (the 2025 conversion applied to the 2026 raw scores) and, the asks being decoupled from the call, takes the
same ask paths. Each keeps a figure when it lands on the golden's rounding (whole counts, shares to one decimal).

    python3 task450/generator/ceiling.py [target_dir]
"""
import json
import os
import shutil
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import golden as G    # noqa: E402
import reader as RD   # noqa: E402
import world as W     # noqa: E402

TASK = os.path.dirname(HERE)


def run(target):
    L = RD.load(target)
    a25, a25c = G.ask_2025(L), G.ask_2025_by_code(L)
    share = lambda v: "%.1f" % (100.0 * v[1] / v[0])
    keep_a = sum(a25c[k][0] == a25[k][0] for k in W.COMMUNITIES) + \
        sum(share(a25c[k]) == share(a25[k]) for k in W.COMMUNITIES)
    un, unc = G.ask_untested(L), G.ask_untested(L, merged=False)
    keep_b = sum(un.get(k, 0) == unc.get(k, 0) for k in W.COMMUNITIES) + (sum(un.values()) == sum(unc.values()))
    total = 2 * len(W.COMMUNITIES) + len(W.COMMUNITIES) + 1
    lc = ls = (keep_a + keep_b) / total
    cr, mi = 38 + 7 + 55 * lc, 5 + 7 + 55 * ls
    return dict(cracker_kept={"A": keep_a, "B": keep_b}, mirror_kept={"A": keep_a, "B": keep_b}, ask_criteria=total,
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
