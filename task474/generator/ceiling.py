"""The pair ceiling on the cut pack: the cracker lands the call and runs the battery on the gate exports, merging
each truck's overlapping transactions into stays as recorded; the mirror
stops at the all-vehicle factors. Weights 38 / 7 / 55; the main block grades each designated link listed,
no other link listed and the count; the asks are 24 figures (trucks and old engines for 4 quarters and 8 carriers)."""
import os
import sys

import bundle as B
import methods as M

W_CALL, W_INSTR, W_ASK = 38.0, 7.0, 55.0
HERE = os.path.dirname(os.path.abspath(__file__))


def main(target=None):
    target = target or os.path.join(os.path.dirname(HERE), "target")
    g, m = M.designated(B.nox(target)), M.designated(B.nox(target, "classes"))
    # the main block grades each designated link listed (len(g)), no other link listed (1) and the count (1)
    keep = sum(k in m for k in g) + (not set(m) - set(g)) + (len(m) == len(g))
    mirror_call = W_CALL * keep / (len(g) + 2.0)
    gq, gcar = B.fleet_asks(target)
    cq, ccar = B.fleet_asks(target, "ids")
    n = 8 + 2 * len(gcar)
    hit = sum(gq[q][i] == cq[q][i] for q in gq for i in (0, 1)) + \
        sum(ccar.get(k, (None, None))[i] == gcar[k][i] for k in gcar for i in (0, 1))
    ask = W_ASK * hit / n
    cracker, mirror = W_CALL + W_INSTR + ask, mirror_call + W_INSTR + ask
    print("golden %s; mirror %s" % (g, m))
    print("mirror keeps %d of %d main figures; the asks' careful path keeps %d of %d" % (keep, len(g) + 2, hit, n))
    print("cracker %.1f, mirror %.1f, pair ceiling %.1f, mirror leakage %.1f per cent of ask weight" % (
        cracker, mirror, (cracker + mirror) / 2, 100.0 * hit / n))
    return (cracker + mirror) / 2


if __name__ == "__main__":
    sys.exit(0 if main() <= 40.0 else 1)
