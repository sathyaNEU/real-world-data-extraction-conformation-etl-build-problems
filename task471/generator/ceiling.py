"""The pair ceiling on the cut pack: the cracker lands the call and runs the battery; the mirror stops at the default
path (the pooled share scaled to each county's wells). Weights 38 / 7 / 55; the ask is 32 figures.

    python3 task471/generator/ceiling.py     exit 0 at 40 or under
"""
import os
import sys

import bundle as B

W_CALL, W_INSTR, W_ASK = 38.0, 7.0, 55.0
HERE = os.path.dirname(os.path.abspath(__file__))


def main(target=None):
    target = target or os.path.join(os.path.dirname(HERE), "target")
    pk = B.Pack(target)
    gold = set(pk.qualifying())
    mirror = set(pk.qualifying("pooled"))
    # the graded grid: each county's wells on the lists (16) and its verdict (16); the call's set lives in the verdicts
    keep = len(pk.codes) + sum(1 for k in pk.codes if (k in gold) == (k in mirror))
    mirror_call = W_CALL * 0.75 * keep / 32.0
    g = pk.retests()
    # the cracker's ask path: every request matched to its well (first kit, or the phone request's address), the
    # window and the first test applied, each well counted in the county on its request
    c = pk.retests(by="request")
    hit = sum(c[k][j] == g[k][j] for k in pk.codes for j in (0, 1))
    m = pk.retests(by="request", channel="portal")
    mhit = sum(m[k][j] == g[k][j] for k in pk.codes for j in (0, 1))
    ask, mask = W_ASK * hit / 32.0, W_ASK * mhit / 32.0
    cracker, mirror_score = W_CALL + W_INSTR + ask, mirror_call + W_INSTR + mask
    print("golden %s; mirror %s" % (sorted(gold), sorted(mirror)))
    print("mirror keeps %d of 32 grid figures; the cracker's ask path keeps %d of 32, the mirror's %d" % (keep, hit, mhit))
    print("cracker %.1f, mirror %.1f, pair ceiling %.1f, mirror leakage %.1f per cent of ask weight" % (
        cracker, mirror_score, (cracker + mirror_score) / 2, 100.0 * mhit / 32))
    return (cracker + mirror_score) / 2


if __name__ == "__main__":
    sys.exit(0 if main() <= 40.0 else 1)
