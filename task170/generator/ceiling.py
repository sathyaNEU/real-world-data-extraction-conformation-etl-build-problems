"""task170 ceiling: the cracker and the mirror run as code on the cut pack, each ask figure scored against
generator/figures.json, and the pair ceiling on supplemental-stumping Part 0's weights (38 recommendation and
critical components, 7 instruction-following, 55 asks; a wrong call keeps r = 5 of the recommendation's weight).

    python3 task170/generator/ceiling.py task170/target

The cracker lands the call and runs the hygiene battery (exact duplicates, key uniqueness, unmatched joins) and
every filed rule it points at: the plan's allocation rule and its sub-county boundaries. The mirror stops at the
most attractive wrong rung on the call (the trial's pooled efficacy) and takes the asks on their natural reads."""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc  # noqa: E402
import common as C  # noqa: E402


def r100(v):
    return int(round(v / 100.0)) * 100


def main(target):
    F = json.load(open(os.path.join(HERE, "figures.json")))
    G = calc.golden(target)
    bu = calc.averted_with(G, 1.0)
    keys = ["call_share_of_expected_pct"] + ["call_cases_averted_%s" % s for s in C.SC_CODES] + \
           ["ask_nets_%s" % s for s in C.SC_CODES] + ["ask_reported_cases_2026_%s" % s for s in C.SC_CODES]
    # the cracker
    crack = {"call_share_of_expected_pct": int(round(100 * G["share"]))}
    for s in C.SC_CODES:
        crack["call_cases_averted_%s" % s] = r100(G["by_sc"][s])
    nets_c = calc.nets_needed(target, "idonly")
    cases_c = calc.reported_cases(target, "dedup")
    for s in C.SC_CODES:
        crack["ask_nets_%s" % s] = nets_c[s]
        crack["ask_reported_cases_2026_%s" % s] = cases_c[s]
    # the mirror: the trial's pooled efficacy on the call, natural reads on the asks
    eff = G["pooled"]
    mirror = {"call_share_of_expected_pct": int(round(100 * bu * eff / G["base_total"]))}
    for s in C.SC_CODES:
        mirror["call_cases_averted_%s" % s] = r100(sum(G["base"][(s, m)] * G["use"][m] * eff for (_, m) in C.WINDOW))
    nets_m = calc.nets_needed(target, "exact")
    cases_m = calc.reported_cases(target, "export_dedup")
    for s in C.SC_CODES:
        mirror["ask_nets_%s" % s] = nets_m[s]
        mirror["ask_reported_cases_2026_%s" % s] = cases_m[s]
    hit_c = [k for k in keys if crack[k] == F[k]]
    hit_m = [k for k in keys if mirror[k] == F[k]]
    for k in keys:
        print("%-36s golden %8s  cracker %8s %-4s  mirror %8s %-4s" % (k, F[k], crack[k], "HIT" if k in hit_c else "miss",
                                                                     mirror[k], "HIT" if k in hit_m else "miss"))
    Lc = len(hit_c) / len(keys)
    Ls = len(hit_m) / len(keys)
    Cs = 38 + 7 + 55 * Lc
    Ss = 5 + 7 + 55 * Ls
    print("\ncracker keeps %d of %d ask figures (all on the call's own construction), %d device figures" %
          (len(hit_c), len(keys), sum(1 for k in hit_c if k.startswith("ask_"))))
    print("mirror keeps %d of %d (mirror leakage %.1f per cent)" % (len(hit_m), len(keys), 100 * Ls))
    print("pair ceiling (%.1f + %.1f) / 2 = %.1f" % (Cs, Ss, (Cs + Ss) / 2))
    one = 38 + 7 + 55 * (len(hit_c) + 7) / len(keys)
    print("if the cracker also cracks one ask device: (%.1f + %.1f) / 2 = %.1f" % (one, Ss, (one + Ss) / 2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else C.TARGET))
