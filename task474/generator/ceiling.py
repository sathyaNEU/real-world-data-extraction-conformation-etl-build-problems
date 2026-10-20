"""The pair ceiling on the cut pack: the cracker lands the call and runs the battery on the gate exports, merging
each truck's overlapping transactions into stays as recorded; the mirror
stops at the all-vehicle factors. Weights 38 / 7 / 55; the main block grades each link's verdict (14) and the set
(1); the asks are 24 figures (visits and turn time for 3 terminals in 4 quarters)."""
import os
import sys

import bundle as B
import methods as M

W_CALL, W_INSTR, W_ASK = 38.0, 7.0, 55.0
HERE = os.path.dirname(os.path.abspath(__file__))


def main(target=None):
    target = target or os.path.join(os.path.dirname(HERE), "target")
    g, m = M.designated(B.nox(target)), M.designated(B.nox(target, "textbook"))
    links = sorted(B.links(target))
    keep = sum((k in g) == (k in m) for k in links) + (g == m)
    mirror_call = W_CALL * keep / (len(links) + 1.0)
    ga, gc = B.gate_asks(target), B.gate_asks(target, "merged")
    hit = sum(ga[k][0] == gc[k][0] for k in ga) + sum(round(ga[k][1], 1) == round(gc[k][1], 1) for k in ga)
    ask = W_ASK * hit / 24.0
    cracker, mirror = W_CALL + W_INSTR + ask, mirror_call + W_INSTR + ask
    print("golden %s; mirror %s" % (g, m))
    print("mirror keeps %d of %d main figures; the asks' careful path keeps %d of 24" % (keep, len(links) + 1, hit))
    print("cracker %.1f, mirror %.1f, pair ceiling %.1f, mirror leakage %.1f per cent of ask weight" % (
        cracker, mirror, (cracker + mirror) / 2, 100.0 * hit / 24))
    return (cracker + mirror) / 2


if __name__ == "__main__":
    sys.exit(0 if main() <= 40.0 else 1)
