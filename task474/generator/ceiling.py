"""The pair ceiling on the cut pack: the cracker lands the call and runs the battery, executing every filed rule it
points at (ask A each hour priced at the gas day read on the DAHS clock; ask B the event hours summed); the mirror
stops at the load-based fill. Weights 38 / 7 / 55; the main block grades each unit's verdict (9) and the set (1);
the asks are 18 figures."""
import os
import sys

import bundle as B
import methods as M

W_CALL, W_INSTR, W_ASK = 38.0, 7.0, 55.0
HERE = os.path.dirname(os.path.abspath(__file__))


def main(target=None):
    target = target or os.path.join(os.path.dirname(HERE), "target")
    rec = B.record(target)
    g, m = M.designated(rec, "golden"), M.designated(rec, "load")
    keep = sum((u in g) == (u in m) for u in rec) + (g == m)
    mirror_call = W_CALL * keep / (len(rec) + 1.0)
    a_g, a_c = B.ask_a(target), B.ask_a(target, "standard9")
    b_g, b_c = B.ask_b(target), B.ask_b(target, union=False)
    hit = sum(int(a_g[u] + .5) == int(a_c[u] + .5) for u in rec) + sum(int(b_g.get(u, 0)) == int(b_c.get(u, 0) + .5)
                                                                       for u in rec)
    ask = W_ASK * hit / (2.0 * len(rec))
    cracker, mirror = W_CALL + W_INSTR + ask, mirror_call + W_INSTR + ask
    print("golden %s; mirror %s" % (g, m))
    print("mirror keeps %d of %d main figures; the asks' cracker path keeps %d of %d" % (keep, len(rec) + 1, hit,
                                                                                        2 * len(rec)))
    print("cracker %.1f, mirror %.1f, pair ceiling %.1f, mirror leakage 0.0 per cent of ask weight" % (
        cracker, mirror, (cracker + mirror) / 2))
    return (cracker + mirror) / 2


if __name__ == "__main__":
    sys.exit(0 if main() <= 40.0 else 1)
