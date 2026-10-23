"""task170 ceiling: the cracker and the mirror run as code on the cut pack, each graded figure scored against
generator/figures.json, and the pair ceiling on supplemental-stumping Part 0's weights (38 recommendation and
critical components, 7 instruction-following, 55 for the hospital rows and the asks; a wrong call keeps r = 5).

    python3 task170/generator/ceiling.py task170/target

The cracker lands the call and runs the hygiene battery (exact duplicates, key uniqueness, unmatched joins) and
every filed rule it points at: the plan rules' match formula, the payroll's reversal and re-run netted, the two
employee numbers mapped, the register's Active status. The mirror stops at the default path (the cover's
cancellations carried as the plan's opt-outs) and takes the asks on their natural reads."""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc  # noqa: E402
import common as C  # noqa: E402


def rnd(v, unit):
    return int(round(v / float(unit))) * unit


def main(target):
    F = json.load(open(os.path.join(HERE, "figures.json")))
    G = calc.golden(target)
    cv, P = G["cv"], G["P"]
    ded = calc.deductions(target)
    keys = ["call_match_fy2027_%s" % h for h in C.H_CODES] + ["call_contributing_dec2027"] + \
           ["ask_match_paid_2026_%s" % h for h in C.H_CODES] + ["ask_members_pre2019_%s" % h for h in C.H_CODES]

    def score(call, paid, mem):
        out = {"call_contributing_dec2027": rnd(call["heads_total"], 100)}
        for h in C.H_CODES:
            out["call_match_fy2027_%s" % h] = rnd(call["by"][h], 100000)
            out["ask_match_paid_2026_%s" % h] = rnd(paid[h], 1000)
            out["ask_members_pre2019_%s" % h] = mem[h]
        return out

    crack = score(G, calc.match_paid_2026(target, "lines", ded), calc.members_pre2019(target, "register", ded))
    mirror = score(calc.forecast(target, cv, "ipc_carry", P), calc.match_paid_2026(target, "lines", ded),
                   calc.members_pre2019(target, "register", ded))
    hit_c = [k for k in keys if crack[k] == F[k]]
    hit_m = [k for k in keys if mirror[k] == F[k]]
    for k in keys:
        print("%-32s golden %10s  cracker %10s %-4s  mirror %10s %-4s" % (k, F[k], crack[k], "HIT" if k in hit_c else "miss",
                                                                     mirror[k], "HIT" if k in hit_m else "miss"))
    Lc = len(hit_c) / len(keys)
    Ls = len(hit_m) / len(keys)
    Cs = 38 + 7 + 55 * Lc
    Ss = 5 + 7 + 55 * Ls
    print("\ncracker keeps %d of %d figures (%d on the call's own construction, %d ask figures)" %
          (len(hit_c), len(keys), sum(1 for k in hit_c if k.startswith("call_")), sum(1 for k in hit_c if k.startswith("ask_"))))
    print("mirror keeps %d of %d (mirror leakage %.1f per cent)" % (len(hit_m), len(keys), 100 * Ls))
    print("pair ceiling (%.1f + %.1f) / 2 = %.1f" % (Cs, Ss, (Cs + Ss) / 2))
    one = 38 + 7 + 55 * (len(hit_c) + 6) / len(keys)
    print("if the cracker also cracks one ask's device: (%.1f + %.1f) / 2 = %.1f" % (one, Ss, (one + Ss) / 2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else C.TARGET))
