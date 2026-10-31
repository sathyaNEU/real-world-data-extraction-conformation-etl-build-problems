"""The ask sheet's cracker and mirror, measured on the generator's ask functions.

The asks' figures come from the same functions the verifier reproduces from the cut pack alone (verify.py), so the
cracker's and the mirror's figures here are the ones a response reading the pack would file. The cracker lands 7:05,
runs the hygiene battery and executes every filed rule: it adds the two rider sheets with each person once inside a sheet
(R1) and looks the deadhead codes up in the current network release (T1). The mirror stops at the default path's 7:15,
reading each segment at the departure's period. Each keeps a figure when it lands on the golden's whole number or whole
dollar. Escapes by insight are priced as the note prices them: R1 one time in 0.40, T1 one time in 0.45, independent.

    python3 task254/generator/ceiling.py
"""
import itertools
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import analysis as AN   # noqa: E402
import asks as A        # noqa: E402
import build as B       # noqa: E402

P_R1, P_T1 = 0.40, 0.45
CHART = 4


def kept(fig, gold):
    a = sum(fig[f] == gold[f] for f in ("riders", "vehicles", "seats_empty"))
    late = sum(fig["late_arrivals"][d] == gold["late_arrivals"][d] for d in A.ASK_DEPS)
    cost = sum(round(fig["cost"][d]) == round(gold["cost"][d]) for d in A.ASK_DEPS)
    chart = CHART if cost == len(A.ASK_DEPS) else 0
    return a + late + cost + chart


def run():
    W, S = B.build()
    F = AN.main_figures(W)
    G = AN.ask_figures(F, S)
    gold = G["gold"]
    total = 3 + 2 * len(A.ASK_DEPS) + CHART
    sheet = {}
    expect_c = 0.0
    for r_esc, t_esc in itertools.product((False, True), repeat=2):
        fig = G["stops"][("golden" if r_esc else "R1", "walk", "golden" if t_esc else "current")]
        k = kept(fig, gold)
        p = (P_R1 if r_esc else 1 - P_R1) * (P_T1 if t_esc else 1 - P_T1)
        sheet["R1 %s, T1 %s" % ("escaped" if r_esc else "held", "escaped" if t_esc else "held")] = k
        expect_c += p * k
    mirror_late = [k for k in F["late"] if k != "walk"]
    expect_m = 0.0
    for r_esc in (False, True):
        fig = G["stops"][("golden" if r_esc else "R1", "period" if "period" in F["late"] else mirror_late[0],
                          "current")]
        expect_m += (P_R1 if r_esc else 1 - P_R1) * kept(fig, gold)
    lc, ls = expect_c / total, expect_m / total
    c_paper = 38 + 7 + 55 * sheet["R1 held, T1 held"] / total
    cr, mi = 38 + 7 + 55 * lc, 3 + 7 + 55 * ls
    return dict(ask_criteria=total, cracker_kept_by_escape=sheet, cracker_on_paper=round(c_paper, 1),
                cracker_expected=round(cr, 1), mirror_expected=round(mi, 1), pair_ceiling=round((cr + mi) / 2, 1),
                pair_on_paper=round((c_paper + 3 + 7) / 2, 1), mirror_leakage_pct=round(100 * ls, 1),
                late_constructions=sorted(F["late"]))


if __name__ == "__main__":
    print(json.dumps(run(), indent=1))
