"""task482 architecture 16: the ask layer's pair ceiling on the cut pack (supplemental-stumping Parts 0 and 1.1).

The cracker lands the call, runs the hygiene battery and executes every filed rule: it conforms the weighbridge (one
row per weighing, UTC) to visits on ticket and date across the July restart, drops the rejected loads and the
returned metal, weighs each one-grade load as in-weigh less out-weigh, shares a two-grade load's net by the weights
its note declares, and weighs each dross lift as out-weigh less in-weigh. The mirror stops at the mass allocation
(every family under the limit) and reads the asks the same way. Each figure is scored against the golden.

    python3 task482/generator/ceiling.py
"""
import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
sys.path.insert(0, HERE)
import golden as G  # noqa: E402


def kept_a(gold, other):
    return sum(1 for g in G.GRADES for q in G.QUARTERS if round(other[g][q]) == round(gold[g][q]))


def kept_b(gold, other):
    return sum(1 for q in G.QUARTERS if round(other[q]) == round(gold[q]))


def main():
    gold_a, gold_b = G.scrap(T), G.dross(T)
    routes_a = {
        "two-grade loads shared by declared weight (the cracker)": G.scrap(T, split="declared"),
        "two-grade loads split at the middle weighing in line order": G.scrap(T, split="line_order"),
        "the goods-in register's declared weights (the mirror)": G.declared(T),
        "joined on the ticket number alone": G.scrap(T, key="ticket"),
    }
    routes_b = {
        "out-weigh less in-weigh on every lift (the cracker and the mirror)": G.dross(T, combined="first_last"),
    }
    ka = {k: kept_a(gold_a, v) for k, v in routes_a.items()}
    kb = {k: kept_b(gold_b, v) for k, v in routes_b.items()}
    n = 16 + 4
    for k, v in ka.items():
        print("ask A  %-64s keeps %2d of 16" % (k, v))
    for k, v in kb.items():
        print("ask B  %-64s keeps %2d of 4" % (k, v))
    crack = ka["two-grade loads shared by declared weight (the cracker)"] + \
        kb["out-weigh less in-weigh on every lift (the cracker and the mirror)"]
    mirror = ka["the goods-in register's declared weights (the mirror)"] + \
        kb["out-weigh less in-weigh on every lift (the cracker and the mirror)"]
    c = 38 + 7 + 55.0 * crack / n
    s = 5 + 7 + 55.0 * mirror / n
    zp = os.path.join(TASK, "target.zip")
    print("measured on target.zip %s" % hashlib.sha256(open(zp, "rb").read()).hexdigest()[:8])
    print("cracker keeps %d of %d ask figures, scores %.1f with the call" % (crack, n, c))
    print("mirror keeps %d of %d, scores %.1f off it" % (mirror, n, s))
    print("Pair ceiling: %.1f" % ((c + s) / 2))
    print("Mirror leakage: %.1f per cent of ask weight" % (100.0 * mirror / n))
    return dict(crack=crack, mirror=mirror, pair=(c + s) / 2)


if __name__ == "__main__":
    main()
