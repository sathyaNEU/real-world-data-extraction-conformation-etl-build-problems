"""The ask sheet's cracker and mirror, run on the cut pack.

The cracker lands the call, runs the hygiene battery and executes every filed rule (the prompt's estimand, guidelines
2.2, 6.1, 6.2 and 7.1 to 7.5, so each home sits in its recorded county, never HMDA's); on the asks it counts a
farmstead recorded in two counties twice and carries each lender's 2024 to 2025 way of recording into 2026. The mirror stops at
the call's most attractive wrong rung, the pooled capture, and takes each ask's construction at that capture. Each keeps
an ask figure when its value lands in the golden's rounding bin (nearest 10, the program year's total nearest 100).

    python3 task448/generator/ceiling.py [target_dir]
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
# ask-side criteria: Ask A's six program-year figures, Ask B's five two-year county figures, and the chart's four
# (the twelve lenders shown, their counts, the five marked, the layout)
CHART = 4


def rk(k, x):
    return C.r100(x) if k == "total" else C.r10(x)


def run(target):
    B = C.load(target)
    two_g, py_g = C.market_two_year(B), C.program_year(B)
    gb, ga = C.ask_figures(two_g, py_g)                       # Ask B (two-year), Ask A (program year)
    crack_b, _ = C.ask_figures(C.market_two_year(B, dedupe=False), py_g)
    _, crack_a = C.ask_figures(two_g, C.program_year(B, per_record=False))
    pooled = C.capture(B)["all"]
    caps = {"P": pooled, "S": pooled}
    mirror_b, mirror_a = C.ask_figures(C.market_two_year(B, caps=caps), C.program_year(B, caps=caps))
    gold_call = [n for n, _ in C.five(C.lender_counts(B))[0]]
    mirror_call = [n for n, _ in C.five(C.lender_counts(B, method="pooled"))[0]]

    def kept(fa, fb):
        return (sum(rk(k, fa[k]) == rk(k, ga[k]) for k in ga), sum(C.r10(fb[k]) == C.r10(gb[k]) for k in gb))

    ka, kb = kept(crack_a, crack_b)
    ma, mb = kept(mirror_a, mirror_b)
    total = len(ga) + len(gb) + CHART
    # the chart: the cracker, on the call with the right counts, keeps all four; the mirror keeps the layout only
    lc = (ka + kb + CHART) / total
    ls = (ma + mb + 1) / total
    cr = 38 + 7 + 55 * lc
    mi = (38 if mirror_call == gold_call else 5) + 7 + 55 * ls
    return dict(cracker_kept={"Ask A": ka, "Ask B": kb, "chart": CHART}, mirror_kept={"Ask A": ma, "Ask B": mb, "chart": 1},
                mirror_on_call=mirror_call == gold_call, ask_criteria=total, cracker=round(cr, 1), mirror=round(mi, 1),
                pair_ceiling=round((cr + mi) / 2, 1), mirror_leakage_pct=round(100 * ls, 1))


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
