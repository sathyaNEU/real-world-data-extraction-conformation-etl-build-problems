"""The pair ceiling on the cut pack (supplemental-stumping Part 0 weights: 38 for the call and its components, 7 for
the instructions, 55 for the asks).

The cracker lands the call on the golden's rebuild, runs the hygiene battery and takes the routes a careful solver
takes through the after-hours file: a visit is a case (the battery finds the repeated case reference and keeps one
row per case) and a resident is a client key. The mirror stops at the default path's census split and runs the asks
the same way. Each response's ask figures are scored against the golden, a hit within half a unit of the stated
rounding.

    python3 task270/generator/cracker.py [<target dir>]"""
from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc        # noqa: E402
import common as K  # noqa: E402

W_CALL, W_IF, W_ASK = 38.0, 7.0, 55.0
R_MISS = 5.0          # the recommendation weight a wrong call keeps


def measure(target):
    out, *_ = calc.rungs(target)
    by_code, _ = calc.read_corr(target)
    rows = calc.read_ah(target)
    gv, gr = calc.ah_golden(rows, by_code)
    paths = calc.ah_paths(rows, by_code)
    areas = sorted(K.AREA_NAMES)
    gold_set = {a for a in areas if out[a]["G"] < K.LINE}
    table = []
    crack = {"e85": 0, "visits": 0, "residents": 0, "chart": 4}
    mirror = {"e85": 0, "visits": 0, "residents": 0, "chart": 2}
    for a in areas:
        g1 = round(out[a]["G"], 1)
        crack["e85"] += 1
        mirror["e85"] += int(round(out[a]["R2"], 1) == g1)
        cv, cr = paths["visits_cases"][a], paths["residents_keys"][a]
        crack["visits"] += int(cv == gv[a])
        crack["residents"] += int(cr == gr[a])
        mirror["visits"] += int(cv == gv[a])
        mirror["residents"] += int(cr == gr[a])
        table.append((a, gv[a], cv, gr[a], cr))
    n_ask = 12 * 3 + 4
    keep_c = sum(crack.values()) / n_ask
    keep_m = sum(mirror.values()) / n_ask
    mirror_set = {a for a in areas if out[a]["R2"] < K.LINE}
    score_c = W_CALL + W_IF + W_ASK * keep_c
    score_m = (W_CALL if mirror_set == gold_set else R_MISS) + W_IF + W_ASK * keep_m
    return dict(table=table, crack=crack, mirror=mirror, keep_c=keep_c, keep_m=keep_m, score_c=score_c,
                score_m=score_m, pair=(score_c + score_m) / 2, n_ask=n_ask, mirror_on_call=mirror_set == gold_set)


def main(argv):
    target = argv[0] if argv else os.path.join(os.path.dirname(HERE), "target")
    m = measure(target)
    print("| Ask figures | Area | Golden | Cracker's path | Cracker's value | Verdict |")
    print("|---|---|---|---|---|---|")
    for a, gv, cv, gr, cr in m["table"]:
        print("| visits | %s | %d | one per case | %d | %s |" % (a, gv, cv, "miss" if cv != gv else "HIT"))
    for a, gv, cv, gr, cr in m["table"]:
        print("| residents | %s | %d | one per client key | %d | %s |" % (a, gr, cr, "miss" if cr != gr else "HIT"))
    print("cracker keeps %s of %d ask criteria (%.1f per cent): %.1f" % (m["crack"], m["n_ask"], 100 * m["keep_c"],
                                                                         m["score_c"]))
    print("mirror keeps %s of %d (%.1f per cent), on the call: %s: %.1f" % (m["mirror"], m["n_ask"], 100 * m["keep_m"],
                                                                          m["mirror_on_call"], m["score_m"]))
    print("pair ceiling %.1f" % m["pair"])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
