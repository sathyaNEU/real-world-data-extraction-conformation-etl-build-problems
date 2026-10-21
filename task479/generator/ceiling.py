"""The ask layer measured on the cut pack: the cracker (lands the call, runs the hygiene battery: one row per student
id, the later row of a repeated id, the crosswalk's join) and the mirror (the default path on the call, the asks
handled the cracker's way), priced against generator/figures.json on the weights 38 / 7 / 55.

    python3 task479/generator/ceiling.py [target]

The call is 38: the designated set 10 and the fourteen campuses' shares 28 / 14 each. Instructions 7. The 56 ask
figures (fourteen campuses' fall tested and proficient share, fall-and-winter students and growth) are 55 / 56 each.
The asks read only fall and winter rows, the register, the rosters and the crosswalk, which the call never reads, so
the two responses take the same ask readings."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import bundle as B    # noqa: E402

TASK = os.path.dirname(HERE)
ASK_W = 55.0 / 56


def main(target=None):
    target = target or os.path.join(TASK, "target")
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    b = B.load(target)
    A, Bx = B.ask_a(b, False), B.ask_b(b, False)
    k1 = sum(A[c][0] == fig["ask_a"][c]["tested"] for c in A)
    k2 = sum("%.1f" % A[c][1] == fig["ask_a"][c]["proficient_pct"] for c in A)
    k3 = sum(Bx[c][0] == fig["ask_b"][c]["students"] for c in Bx)
    k4 = sum("%.1f" % Bx[c][1] == fig["ask_b"][c]["growth"] for c in Bx)
    kept = k1 + k2 + k3 + k4
    print("Ask A tested kept %d of 14, proficient share kept %d of 14 (a row per student id)" % (k1, k2))
    print("Ask B students kept %d of 14, growth kept %d of 14 (the crosswalk alone)" % (k3, k4))
    C = 38 + 7 + ASK_W * kept
    v = B.spring(b, "vendor")
    sh = B.shares(b, v)
    hit = B.designate(b, v) == fig["call"]["designated"]
    rates = sum("%.1f" % (100 * sh[c]) == fig["below_basic_pct"][c] for c in sh)
    m = 10 * hit + 28.0 / 14 * rates
    S = m + 7 + ASK_W * kept
    print("cracker: call landed (38), instructions (7), ask figures kept %d of 56: %.1f" % (kept, C))
    print("mirror (the default path): main block %.1f (set %s, %d shares kept), ask figures kept %d of 56: %.1f" % (
        m, "landed" if hit else "missed", rates, kept, S))
    print("Mirror leakage: %.1f per cent of ask weight" % (100.0 * kept / 56))
    print("Pair ceiling: %.1f" % ((C + S) / 2))
    return (C + S) / 2


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
