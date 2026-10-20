"""The pair ceiling on the cut pack: the cracker lands the call and runs the battery, executing the reflex on the
pharmacy lines (filter to the period and class, then each claim number at its latest line); the mirror stops at the
roster's member-months. Weights 38 / 7 / 55; the main block grades each group's verdict (12) and the set (1); the
asks are 24 figures (paid and fills for each of 12 classes)."""
import os
import sys

import bundle as B

W_CALL, W_INSTR, W_ASK = 38.0, 7.0, 55.0
HERE = os.path.dirname(os.path.abspath(__file__))


def sets(target, route):
    return sorted(k for k, v in B.pmpm(target, route).items() if v >= 412.0)


def main(target=None):
    target = target or os.path.join(os.path.dirname(HERE), "target")
    gs = B.groups(target)
    g, m = sets(target, "golden"), sets(target, "roster")
    keep = sum((k in g) == (k in m) for k in gs) + (g == m)
    mirror_call = W_CALL * keep / (len(gs) + 1.0)
    a_g, a_c = B.pharmacy(target), B.pharmacy(target, "filterfirst")
    d = lambda v: int(v + .5)
    hit = sum(d(a_g[c][0]) == d(a_c[c][0]) for c in a_g) + sum(a_g[c][1] == a_c[c][1] for c in a_g)
    ask = W_ASK * hit / (2.0 * len(a_g))
    cracker, mirror = W_CALL + W_INSTR + ask, mirror_call + W_INSTR + ask
    print("golden %s; mirror %s" % (g, m))
    print("mirror keeps %d of %d main figures; the asks' cracker path keeps %d of %d" % (keep, len(gs) + 1, hit,
                                                                                        2 * len(a_g)))
    print("cracker %.1f, mirror %.1f, pair ceiling %.1f" % (cracker, mirror, (cracker + mirror) / 2))
    return (cracker + mirror) / 2


if __name__ == "__main__":
    sys.exit(0 if main() <= 40.0 else 1)
