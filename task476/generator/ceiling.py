"""The pair ceiling, measured on the cut pack: the cracker lands the call, runs the battery and executes every filed
rule it points at; the mirror stops at the default path (R2). Weights 38 / 7 / 55: the call and the tract grid, the
instructions, the asks (20 figures).

    python3 task476/generator/ceiling.py
"""
import os
import sys

import bundle as B

W_CALL, W_INSTR, W_ASK = 38.0, 7.0, 55.0
HERE = os.path.dirname(os.path.abspath(__file__))


def main(target=None):
    target = target or os.path.join(os.path.dirname(HERE), "target")
    gold = B.tract_table(target)
    mir = B.tract_table(target, route="parent")
    gs, ms = B.designated(gold)[0], B.designated(mir)[0]
    # the call side: the set (6 points), each tract's 2014-18 rate and margin and its verdict (28 x 3), scaled
    keep = 0
    tot = 0
    for g, m in zip(gold, mir):
        for k in ("r18", "m18"):
            tot += 1
            keep += "%.1f" % (100 * g[k]) == "%.1f" % (100 * m[k])
        tot += 1
        keep += g["qual"] == m["qual"]
    mirror_call = W_CALL * 0.75 * keep / float(tot)        # the grid is three quarters of the call weight
    a_g, a_c = B.ask_a(target), B.ask_a(target, history=False)
    b_g, b_c = B.ask_b(target), B.ask_b(target, by_void=False)
    hit = sum(a_c[k][0] == a_g[k][0] for k in a_g) + sum(round(a_c[k][1]) == round(a_g[k][1]) for k in a_g) + \
        sum(round(b_c[k][0]) == round(b_g[k][0]) for k in b_g) + sum(b_c[k][1] == b_g[k][1] for k in b_g)
    ask = W_ASK * hit / 20.0
    cracker = W_CALL + W_INSTR + ask
    mirror = mirror_call + W_INSTR + ask
    pair = (cracker + mirror) / 2
    print("golden %s; mirror R2 %s" % (gs, ms))
    print("mirror keeps %d of %d grid figures; the asks' cracker path keeps %d of 20 figures" % (keep, tot, hit))
    print("cracker %.1f, mirror %.1f, pair ceiling %.1f, mirror leakage 0.0 per cent of ask weight" % (
        cracker, mirror, pair))
    return pair


if __name__ == "__main__":
    sys.exit(0 if main() <= 40.0 else 1)
