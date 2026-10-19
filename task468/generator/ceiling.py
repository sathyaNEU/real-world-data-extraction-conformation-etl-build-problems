"""The pair ceiling for task468, measured on the cut pack: the cracker lands the call and counts each candidate's
unsheltered outbound stops from the inventory joined on stop code and carried to June 30 by every work order completed
after the inspection; the mirror stops on the review's raw mix (R2) and scores the best of every wrong shelter path.
Each criterion is scored against the golden, the shelter counts as exact hits.

    python3 task468/generator/ceiling.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


import bundle as B                # noqa: E402
import golden as GO               # noqa: E402
import methods as M               # noqa: E402
import world as W                 # noqa: E402

TASK = os.path.dirname(HERE)
# planning weights: the main block 38 (the call 10, the five 8, the first route left out 4, the eleven verdicts 16),
# instruction-following 7, the eleven shelter counts 55
MAIN = {"call": 10.0, "five": 8.0, "first_left_out": 4.0, "verdicts": 16.0}
IF, ASK = 7.0, 55.0


def score(name, five, below, meets, shares, gold):
    lines = []
    call = 1.0 if five == gold["five"] else 0.0
    f5 = len(set(five) & set(gold["five"])) / 5.0
    fl = 1.0 if below == gold["below"] else 0.0
    vd = sum(1 for r in W.CANDIDATES if meets[r] == gold["meets"][r]) / len(W.CANDIDATES)
    hits = [r for r in W.CANDIDATES if shares[r] == gold["ns"][r]]
    main = MAIN["call"] * call + MAIN["five"] * f5 + MAIN["first_left_out"] * fl + MAIN["verdicts"] * vd
    ask = ASK * len(hits) / len(W.CANDIDATES)
    lines.append("%s: the five %s (call %s), first left out Route %s, verdicts %d of 11 right" % (
        name, ", ".join(five), "landed" if call else "missed", below, round(vd * 11)))
    for r in W.CANDIDATES:
        lines.append("   Route %-3s no shelter %3d  golden %3d  %s" % (r, shares[r], gold["ns"][r],
                                                                  "hit" if r in hits else "miss"))
    total = main + IF + ask
    lines.append("   main %.1f + instruction-following %.1f + asks %.1f (%d of 11) = %.1f" % (main, IF, ask, len(hits), total))
    return total, len(hits), lines


def main(target):
    g = GO.compute(target)
    F = json.load(open(os.path.join(HERE, "figures.json"), encoding="utf-8"))
    gold = {"five": g["five"], "below": g["below"], "meets": {x["route"]: x["meets"] for x in g["rows"]},
            "ns": {r: F["no_shelter"][r] for r in W.CANDIDATES}}
    crack = score("cracker (lands the call; the inventory on stop code, carried by the work orders)", g["five"],
                  g["below"], gold["meets"], M.no_shelter(target, "cracker"), gold)
    rows, five, below = M.verdicts(g["raw"], g["ride"])
    wrong = {k: M.no_shelter(target, k) for k in ("cracker", "inventory", "sign")}
    best = max(wrong, key=lambda k: sum(1 for r in W.CANDIDATES if wrong[k][r] == gold["ns"][r]))
    mirror = score("mirror (R2, the review's raw mix; the best wrong shelter path, %s)" % best, five, below,
                   {x["route"]: x["meets"] for x in rows}, wrong[best], gold)
    for _, _, lines in (crack, mirror):
        print("\n".join(lines))
    ceiling = (crack[0] + mirror[0]) / 2.0
    leak = 100.0 * mirror[1] / len(W.CANDIDATES)
    print("pair ceiling %.1f (cracker %.1f with %d of 11 counts, mirror %.1f with %d of 11); mirror leakage %.1f per cent "
          "of ask weight" % (ceiling, crack[0], crack[1], mirror[0], mirror[1], leak))
    return ceiling, crack, mirror


if __name__ == "__main__":
    main(os.path.join(TASK, "target"))
