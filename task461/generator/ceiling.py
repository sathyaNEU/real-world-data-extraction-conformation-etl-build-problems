"""The pair ceiling on the cut pack (supplemental-stumping Parts 0, 1.1 and 5): the cracker lands the call and takes
the careful route on the asks (a straight line between dips for the quarter stocks, the re-tube recharges left out of
the refrigerant); the mirror stops at rung 0 (every tenancy meter subtracted) and takes the same route on the asks.
Each ask figure is scored as a hit within the prompt's rounding; planning weights 38 / 7 / 55.

    python3 task461/generator/ceiling.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import golden as G   # noqa: E402
import world as W    # noqa: E402


def main(target):
    c = G.compute(target)
    lin = G.diesel_quarters(target, "linear")
    top = G.refrigerant(target, "topups")
    rows = []
    for q in range(1, 5):
        rows.append(("A: Q%d gas oil (litres)" % q, round(lin[q]), round(c["diesel"][q])))
        rows.append(("A: Q%d gas oil (kg CO2e)" % q, round(lin[q] * W.DIESEL_KG_PER_L),
                     round(c["diesel"][q] * W.DIESEL_KG_PER_L)))
    for ch in sorted(W.CHILLERS):
        rows.append(("B: %s refrigerant (kg)" % ch, round(top[ch], 1), round(c["refrigerant"][ch], 1)))
        rows.append(("B: %s refrigerant (kg CO2e)" % ch, round(top[ch] * W.GWP_R134A),
                     round(c["refrigerant"][ch] * W.GWP_R134A)))
    print("| Ask figure | Cracker (a straight line between dips, the re-tube recharges left out) | Golden | Cracker |")
    print("|---|---|---|---|")
    kept = 0
    for name, got, want in rows:
        hit = got == want
        kept += hit
        print("| %s | %s | %s | %s |" % (name, got, want, "hit" if hit else "miss"))
    lc = kept / float(len(rows))
    gold = c["monthly"]
    mirror = G.base_building(target, "all")
    main_n = 17
    mirror_main = sum(1 for m in range(1, 13) if round(mirror[m] / 1000) == round(gold[m] / 1000))
    r = 38.0 * mirror_main / main_n
    cr = 38 + 7 + 55 * lc
    mr = r + 7 + 55 * lc
    print("asks: the cracker keeps %d of %d" % (kept, len(rows)))
    print("Pair ceiling: %.1f (cracker %.1f on the call, mirror %.1f off it at %.1f kg; r %.1f)"
          % ((cr + mr) / 2, cr, mr, c["rungs"]["all"]["kpi"], r))
    print("Mirror leakage: %.1f per cent of ask weight" % (100 * lc))


if __name__ == "__main__":
    main(os.path.join(os.path.dirname(HERE), "target"))
