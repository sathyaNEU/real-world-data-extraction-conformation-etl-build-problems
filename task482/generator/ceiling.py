"""The ask layer measured on the cut pack: the cracker (lands the call, runs the hygiene battery: exact duplicates,
one row per student and course, student ids as people) and the mirror (the default path on the call, the asks handled
the cracker's way), priced against generator/figures.json on the weights 38 / 7 / 55.

    python3 task482/generator/ceiling.py [target]

The call is 38: the five awards 10 and the twenty-six campuses' award decisions 28 / 26 each. Instructions 7. The 12
ask figures (the six branches' fall 2026 FTE and headcount) are 55 / 12 each. The asks read only the fall 2026 census
file, which the call never reads."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import bundle as B    # noqa: E402

TASK = os.path.dirname(HERE)
ASK_W = 55.0 / 12


def main(target=None):
    target = target or os.path.join(TASK, "target")
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    b = B.load(target)
    A = B.ask_a(b, dedup=False)
    Bx = B.ask_b(b, persons=False)
    k1 = sum("%.1f" % A[u] == fig["ask_a"][u] for u in fig["ask_a"])
    k2 = sum(Bx[u] == fig["ask_b"][u] for u in fig["ask_b"])
    kept = k1 + k2
    print("Ask A FTE kept %d of 6 (one row per course number); Ask B headcount kept %d of 6 (student ids)" % (k1, k2))
    C = 38 + 7 + ASK_W * kept
    d = B.awarded(b, B.per_fte(b, "fte_split"))
    g = fig["call"]["awarded"]
    same = sum((u in d) == (u in g) for u in b["ids"])
    m = 10 * (d == g) + 28.0 / 26 * same
    S = m + 7 + ASK_W * kept
    print("cracker: call landed (38), instructions (7), ask figures kept %d of 12: %.1f" % (kept, C))
    print("mirror (the default path): main block %.1f (%d of 26 decisions kept), ask figures kept %d of 12: %.1f" % (
        m, same, kept, S))
    print("Mirror leakage: %.1f per cent of ask weight" % (100.0 * kept / 12))
    print("Pair ceiling: %.1f" % ((C + S) / 2))
    return (C + S) / 2


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
