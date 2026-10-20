"""The pair ceiling on the cut pack: the cracker lands the call and runs the battery; the mirror stops at the
default path (the midpoint start). Weights 38 / 7 / 55; the asks are 24 figures."""
import os
import sys

import bundle as B

W_CALL, W_INSTR, W_ASK = 38.0, 7.0, 55.0
HERE = os.path.dirname(os.path.abspath(__file__))


def main(target=None):
    target = target or os.path.join(os.path.dirname(HERE), "target")
    g, m = B.inventory(target), B.inventory(target, route="mid")
    # the graded grid: each district's leaks found (12) and its verdict (12); the call's set lives in the verdicts
    keep = sum(1 for d in g if g[d][0] == m[d][0]) + sum(1 for d in g if (g[d][3] >= B.LINE) == (m[d][3] >= B.LINE))
    mirror_call = W_CALL * 0.75 * keep / 24.0
    a_g, a_c = B.ask_a(target), B.ask_a(target, cumulative=False)
    b_g, b_c = B.ask_b(target), B.ask_b(target, meters=False)
    hit = sum(round(a_c[d]) == round(a_g[d]) for d in a_g) + sum(b_c.get(d) == b_g.get(d) for d in b_g)
    ask = W_ASK * hit / 24.0
    cracker, mirror = W_CALL + W_INSTR + ask, mirror_call + W_INSTR + ask
    print("golden %s; mirror %s" % (B.designated(g), B.designated(m)))
    print("mirror keeps %d of 24 grid figures; the asks' cracker path keeps %d of 24" % (keep, hit))
    print("cracker %.1f, mirror %.1f, pair ceiling %.1f, mirror leakage 0.0 per cent of ask weight" % (
        cracker, mirror, (cracker + mirror) / 2))
    return (cracker + mirror) / 2


if __name__ == "__main__":
    sys.exit(0 if main() <= 40.0 else 1)
