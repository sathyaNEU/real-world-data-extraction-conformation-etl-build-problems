"""The pair ceiling on the cut pack: the cracker (lands the call, runs the hygiene battery, takes each ask the careful
way: every CV-01 interval inside a call's berth window; the shift log's CV-21 quarters) and the mirror (stops at the
toe base and takes the same routes on the asks), each ask figure scored a hit when it lands in the golden's bin.

    python3 task462/generator/ceiling.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import solve as SV   # noqa: E402


def score(target, fig):
    a_crk = SV.ask_a(target, mode="window")
    b_crk = SV.ask_b(target, mode="shift")
    rows = []
    for kk, v in fig["ask_a"].items():
        rows.append(("A: %s received (t)" % kk, round(a_crk[kk]), v, round(a_crk[kk] / 1000) * 1000 == v))
    for i, (kk, v) in enumerate(fig["ask_b"].items()):
        rows.append(("B: %s delivered (t)" % kk, round(b_crk[i]), v, round(b_crk[i] / 1000) * 1000 == v))
    return rows


def main():
    target = os.path.join(os.path.dirname(HERE), "target")
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    rows = score(target, fig)
    kept = sum(1 for r in rows if r[3]) / len(rows)
    c = 38 + 7 + 55 * kept
    mirror = 5 + 7 + 55 * kept
    for name, crk, gold, hit in rows:
        print("%-28s cracker %9s  golden %9s  %s" % (name, "{:,}".format(crk), "{:,}".format(gold),
                                                     "hit" if hit else "miss"))
    print("Pair ceiling: %.1f (the cracker %.1f on the call keeping %.0f per cent of the asks, the mirror %.1f off it)"
          % ((c + mirror) / 2, c, 100 * kept, mirror))
    print("Mirror leakage: %.1f per cent of ask weight" % (100 * kept))
    return rows


if __name__ == "__main__":
    main()
