"""task169 cracker: the pair ceiling and the mirror leakage measured on the cut pack, on Part 0's weights (the
recommendation and its components 38, instructions 7, the asks 55 shared over the 28 ask figures).

The cracker landed the call, ran the hygiene battery, executed every filed rule and every convention the asking
sentences state (rescinded revocations out, the lodge day counted and the end day not, quarters by the day held,
county jails to districts by the methodology's Table 1), added the Board's two systems together, and ended a legacy
detainer with no lift date on the decision that closed its case. The mirror stopped on the record's new-commitment
rate, and handled the asks as a careful analyst who trusts each file as written: both systems added, rescissions
kept, detainers without a lift date left out.

    python3 task169/generator/cracker.py [target]"""
from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as C   # noqa: E402
import calc          # noqa: E402

W_CALL, W_INSTR, W_ASK, R_WRONG = 38.0, 7.0, 55.0, 5.0


def figures(D, a_kw, b_kw):
    A = calc.ask_a(D, **a_kw)
    B = calc.ask_b(D, **b_kw)
    out = {}
    for o in calc.OFFICES:
        for k in ("arrest", "conditions"):
            out["a1_%s.%s" % (o, k)] = A[o][k]
    for d in C.DISTRICTS:
        for q in B[d]:
            out["b_%s.%s" % (d, q)] = B[d][q]
        out["chart.%s" % d] = sum(B[d].values())
    return out


def kept(golden, resp):
    return sum(1 for k, v in golden.items() if resp.get(k) == v)


def main(target):
    D = calc.load(target)
    gold = figures(D, {}, {})
    n = len(gold)
    crack_a = dict(dedupe=False)
    crack_b = dict(blank="action", case=False, migr=False)
    cr = figures(D, crack_a, crack_b)
    mi = figures(D, dict(dedupe=False, rescind=False), dict(blank="drop", case=False, migr=False))
    kc, km = kept(gold, cr), kept(gold, mi)
    C_ = W_CALL + W_INSTR + W_ASK * kc / n
    S_ = R_WRONG + W_INSTR + W_ASK * km / n
    print("ask figures %d" % n)
    print("cracker (call landed): keeps %d of %d ask figures, scores %.1f" % (kc, n, C_))
    print("mirror (call missed):  keeps %d of %d ask figures, scores %.1f" % (km, n, S_))
    print("pair ceiling %.1f   mirror leakage %.1f per cent of ask weight" % ((C_ + S_) / 2, 100 * km / n))
    print("\none crack at a time (the cracker repairs one device and keeps its other stops):")
    singles = (("A: the legacy entries after the close dropped", dict(dedupe=True), crack_b),
               ("B: a blank lift ended at the next admission", crack_a, dict(crack_b, blank="admission")),
               ("B: one detainer per legacy case", crack_a, dict(crack_b, case=True)),
               ("B: carried-over cases counted once", crack_a, dict(crack_b, migr=True)),
               ("B: all three detainer devices", crack_a, dict(blank="admission", case=True, migr=True)))
    for name, ak, bk in singles:
        k = kept(gold, figures(D, ak, bk))
        c1 = W_CALL + W_INSTR + W_ASK * k / n
        print("  %-48s keeps %2d of %d, cracker %.1f, pair %.1f" % (name, k, n, c1, (c1 + S_) / 2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")))
