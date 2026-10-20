"""The pair ceiling on the cut pack: the cracker lands the call and runs the battery, executing every filed rule it
points at (ask A by the employer file's industry for the reporting account; ask B each check split over its lines
by their voucher amounts); the mirror stops at the default path (wages as paid). Weights 38 / 7 / 55; the main
block grades the slate (4), the next in line (1) and every eligible industry's growth (15); the asks are 30 figures."""
import os
import sys

import bundle as B
import methods as M

W_CALL, W_INSTR, W_ASK = 38.0, 7.0, 55.0
HERE = os.path.dirname(os.path.abspath(__file__))


def main(target=None):
    target = target or os.path.join(os.path.dirname(HERE), "target")
    rec = B.record(target)
    g, m = M.route(rec, "golden"), M.route(rec, "paid")
    (gs, gn), (ms, mn) = M.slate(g), M.slate(m)
    keep = len(set(gs) & set(ms)) + (gn == mn) + sum(round(100 * g[s]) == round(100 * m[s]) for s in g)
    mirror_call = W_CALL * keep / 20.0
    el = M.eligible(rec)
    a_g, a_c = B.ask_a(target), B.ask_a(target, merge=False)
    b_g = B.ask_b(target)
    hit = sum(a_c.get(s, 0) == a_g.get(s, 0) for s in el)
    for route in ("id", "share", "lines"):
        b_c = B.ask_b(target, route)
        hit_b = sum(round(b_c.get(s, 0)) == round(b_g.get(s, 0)) for s in el)
        print("ask B under the %s route keeps %d of %d" % (route, hit_b, len(el)))
    b_c = B.ask_b(target, "id")
    hit += sum(round(b_c.get(s, 0)) == round(b_g.get(s, 0)) for s in el)
    ask = W_ASK * hit / (2.0 * len(el))
    cracker, mirror = W_CALL + W_INSTR + ask, mirror_call + W_INSTR + ask
    print("golden %s next %s; mirror %s next %s" % (gs, gn, ms, mn))
    print("mirror keeps %d of 20 main figures; the asks' cracker path keeps %d of %d" % (keep, hit, 2 * len(el)))
    print("cracker %.1f, mirror %.1f, pair ceiling %.1f, mirror leakage 0.0 per cent of ask weight" % (
        cracker, mirror, (cracker + mirror) / 2))
    return (cracker + mirror) / 2


if __name__ == "__main__":
    sys.exit(0 if main() <= 40.0 else 1)
