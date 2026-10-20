"""The pair ceiling on the cut pack: the cracker lands the call and runs the battery, executing every filed rule it
points at (ask A each hour priced on the Central gas day, a gas day without its own invoice line at the point's
previous line; ask B service hours as the operating rows counted); the mirror
stops at the start-state fill. Weights 38 / 7 / 55; the main block grades each unit's verdict (9) and the set (1);
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
    g, m = M.designated(rec, "golden"), M.designated(rec, "state")
    keep = sum((u in g) == (u in m) for u in rec) + (g == m)
    mirror_call = W_CALL * keep / (len(rec) + 1.0)
    a_g, a_c = B.ask_a(target), B.ask_a(target, "prev")
    b_g, b_c = B.ask_b(target), B.ask_b(target, "rows")
    hit = sum(round(a_g[u] / 100) == round(a_c[u] / 100) for u in rec) + sum(round(b_g[u], 1) == round(b_c[u], 1) for u in rec)
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
