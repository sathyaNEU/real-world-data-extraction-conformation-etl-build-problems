"""The pair ceiling (supplemental-stumping Part 0 and 7), measured on the cut pack: the cracker lands the call, runs the
battery and executes every filed rule it points at; the mirror stops at the most attractive wrong rung (the default
path, R6). Weights 38 / 7 / 55: the call and its components, instruction-following, the asks.

    python3 task473/generator/ceiling.py
"""
import os
import sys

import bundle as B
import methods as M
import world as W

W_CALL, W_INSTR, W_ASK = 38.0, 7.0, 55.0
HERE = os.path.dirname(os.path.abspath(__file__))


def main(target=None):
    target = target or os.path.join(os.path.dirname(HERE), "target")
    dr = B.directory(target)
    cr = B.census(target, dr)
    obs = B.observed(cr, B.complete_agencies(dr))
    miles = B.vmt(target)
    g = B.golden_g(obs, miles)
    gold_set = {f for f, v in g["rates"].items() if v >= W.THRESHOLD}
    mir = M.route(obs, "R6")
    mir_rate = M.rate(mir, miles)
    mir_set = {f for f, v in mir_rate.items() if v >= W.THRESHOLD}
    # the call side: the list (6 points), each county's rate (14) and deaths (14), the chart (4)
    pts_list, pts_rate, pts_death, pts_chart = 6.0, 14.0, 14.0, 4.0
    scale = W_CALL / (pts_list + pts_rate + pts_death + pts_chart)
    keep_rate = sum(1 for f in miles if "%.2f" % mir_rate[f] == "%.2f" % g["rates"][f])
    keep_death = sum(1 for f in miles if round(mir[f]) == round(g["deaths"][f]))
    mirror_call = scale * (keep_rate + keep_death + 2.0)      # two chart parts (axes, line) survive a wrong list
    # the asks: 28 figures for the arrests and their per cents, 14 for the injury crashes; both readers take the
    # cracker's path (the asks read nothing either rung builds)
    rows = B.lab(target)
    gold_a = B.ask_a(rows, dr)
    crk_a = B.ask_a(rows, dr, county_of=lambda ag, case, k: str(dr["agencies"][ag]["county_fips"]))
    gold_b, _ = B.ask_b(target, cr)
    crk_b, _ = B.ask_b(target, cr, dedupe=False, link_census=False)
    hit = sum(crk_a.get(f, (0, 0))[0] == gold_a[f][0] for f in miles) + \
        sum("%.1f" % crk_a.get(f, (0, 0))[1] == "%.1f" % gold_a[f][1] for f in miles) + \
        sum(crk_b.get(f, 0) == gold_b.get(f, 0) for f in miles)
    ask = W_ASK * hit / 42.0
    cracker = W_CALL + W_INSTR + ask
    mirror = mirror_call + W_INSTR + ask
    pair = (cracker + mirror) / 2
    print("golden %s; mirror R6 %s" % (sorted(W.NAMES[f] for f in gold_set), sorted(W.NAMES[f] for f in mir_set)))
    print("mirror keeps %d of 14 rates and %d of 14 deaths in their bins; the asks' cracker path keeps %d of 42 "
          "figures" % (keep_rate, keep_death, hit))
    print("cracker %.1f, mirror %.1f, pair ceiling %.1f, mirror leakage 0.0 per cent of ask weight" % (
        cracker, mirror, pair))
    return pair


if __name__ == "__main__":
    sys.exit(0 if main() <= 40.0 else 1)
