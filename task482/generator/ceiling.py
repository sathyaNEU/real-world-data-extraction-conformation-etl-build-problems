"""The ask layer measured on the cut pack: the cracker (lands the call, runs the hygiene battery, counts every line of
the register as a purchase at its own consideration) and the mirror (the default path on the call, the ask handled the
cracker's way), priced against generator/figures.json on the weights 38 / 7 / 55.

    python3 task482/generator/ceiling.py [target]

The call is 38: the designated set 10 and the sixteen areas' decisions 28 / 16 each. Instructions 7. The 32 ask
figures (each area's purchases and total paid) are 55 / 32 each."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import bundle as B    # noqa: E402

TASK = os.path.dirname(HERE)
ASK_W = 55.0 / 32


def main(target=None):
    target = target or os.path.join(TASK, "target")
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    b = B.load(target)
    A = B.ask(b, blocks_once=False)
    k1 = sum(A[k][0] == fig["ask"][k]["purchases"] for k in A)
    k2 = sum(int(round(A[k][1])) == fig["ask"][k]["paid"] for k in A)
    kept = k1 + k2
    print("Ask kept %d of 16 purchase counts and %d of 16 totals (every line a purchase at its own consideration)" % (
        k1, k2))
    C = 38 + 7 + ASK_W * kept
    d = B.designated(b, "pooled")
    g = fig["call"]["designated"]
    same = sum((k in d) == (k in g) for k in b["areas"])
    m = 10 * (d == g) + 28.0 / 16 * same
    S = m + 7 + ASK_W * kept
    print("cracker: call landed (38), instructions (7), ask figures kept %d of 32: %.1f" % (kept, C))
    print("mirror (the default path): main block %.1f (%d of 16 decisions kept), ask figures kept %d of 32: %.1f" % (
        m, same, kept, S))
    print("Mirror leakage: %.1f per cent of ask weight" % (100.0 * kept / 32))
    print("Pair ceiling: %.1f" % ((C + S) / 2))
    return (C + S) / 2


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
