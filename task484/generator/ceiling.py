"""The pair ceiling on the cut pack: the cracker lands the call and runs the battery on the permits, classing by the
code table and counting every 2025 permit; the mirror stops at the ACS occupancy on every unit. Weights 38 / 7 / 55;
the main block grades each upper-tier city listed, no other city listed and the count; the asks are 24 figures
(single-family and multifamily units authorized in 2025 for 12 cities)."""
import os
import sys

import bundle as B

W_CALL, W_INSTR, W_ASK = 38.0, 7.0, 55.0
HERE = os.path.dirname(os.path.abspath(__file__))


def main(target=None):
    target = target or os.path.join(os.path.dirname(HERE), "target")
    g, m = B.tier(B.population(target)), B.tier(B.population(target, "textbook"))
    keep = sum(c in m for c in g) + (not set(m) - set(g)) + (len(m) == len(g))
    mirror_call = W_CALL * keep / (len(g) + 2.0)
    ga, ca = B.authorized(target), B.authorized(target, "rows")
    hit = sum(ga[c][i] == ca[c][i] for c in ga for i in (0, 1))
    ask = W_ASK * hit / 24.0
    cracker, mirror = W_CALL + W_INSTR + ask, mirror_call + W_INSTR + ask
    print("golden %s; mirror %s" % (g, m))
    print("mirror keeps %d of %d main figures; the asks' careful path keeps %d of 24" % (keep, len(g) + 2, hit))
    print("cracker %.1f, mirror %.1f, pair ceiling %.1f, mirror leakage %.1f per cent of ask weight" % (
        cracker, mirror, (cracker + mirror) / 2, 100.0 * hit / 24))
    return (cracker + mirror) / 2


if __name__ == "__main__":
    sys.exit(0 if main() <= 40.0 else 1)
