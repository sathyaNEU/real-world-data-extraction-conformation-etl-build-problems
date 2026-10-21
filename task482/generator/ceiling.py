"""The ask layer measured on the cut pack: the cracker (lands the call, runs the hygiene battery, dates each payment by
the file's settlement date) and the mirror (the default path on the call, the ask handled the cracker's way), priced
against generator/figures.json on the weights 38 / 7 / 55.

    python3 task482/generator/ceiling.py [target]

The call is 38: the planned set 10 and the fourteen offices' decisions 28 / 14 each. Instructions 7. The 28 ask
figures (each office's payments and amount) are 55 / 28 each."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import bundle as B    # noqa: E402

TASK = os.path.dirname(HERE)
ASK_W = 55.0 / 28


def main(target=None):
    target = target or os.path.join(TASK, "target")
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    b = B.load(target)
    A = B.ask(b, by_terminal=False)
    k1 = sum(A[u][0] == fig["ask"][u]["payments"] for u in A)
    k2 = sum(int(round(A[u][1])) == fig["ask"][u]["amount"] for u in A)
    kept = k1 + k2
    print("Ask kept %d of 14 payment counts and %d of 14 amounts (settlement date read as the payment day)" % (k1, k2))
    C = 38 + 7 + ASK_W * kept
    d = B.planned(b, B.medians(b, "registered_only"))
    g = fig["call"]["planned"]
    same = sum((u in d) == (u in g) for u in b["ids"])
    m = 10 * (d == g) + 28.0 / 14 * same
    S = m + 7 + ASK_W * kept
    print("cracker: call landed (38), instructions (7), ask figures kept %d of 28: %.1f" % (kept, C))
    print("mirror (the default path): main block %.1f (%d of 14 decisions kept), ask figures kept %d of 28: %.1f" % (
        m, same, kept, S))
    print("Mirror leakage: %.1f per cent of ask weight" % (100.0 * kept / 28))
    print("Pair ceiling: %.1f" % ((C + S) / 2))
    return (C + S) / 2


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
