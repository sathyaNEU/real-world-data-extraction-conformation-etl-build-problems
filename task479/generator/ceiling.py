"""The ask layer measured on the cut pack: the cracker (lands the call, runs the hygiene battery: one cell per
employer, incurred and paid month and category, the later layout's copy of the re-sent month counted once, the latest
report row per member id, member months as eligibility rows per member id) and the mirror (the default path on the
call, the asks handled the cracker's way), priced against generator/figures.json on the weights 38 / 7 / 55.

    python3 task479/generator/ceiling.py [target]

The call is 38: the surcharged set 10 and the eighteen employers' decisions 28 / 18 each. Instructions 7. The 54 ask
figures (eighteen employers' July to September member months, high-cost members and their claims) are 55 / 54 each.
The asks read only July to September 2026 enrollment and the 2026 high-cost report, which the call never reads, so the
two responses take the same ask readings; checks.py X1 proves the separation."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import bundle as B    # noqa: E402

TASK = os.path.dirname(HERE)
ASK_W = 55.0 / 54


def main(target=None):
    target = target or os.path.join(TASK, "target")
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    b = B.load(target)
    A = B.ask_a(b, by_person=False)
    Bx = B.ask_b(b, by_person=False)
    k1 = sum(A[e] == fig["ask_a"][e] for e in A)
    k3 = sum(Bx[e][0] == fig["ask_b"][e]["members"] for e in Bx)
    k4 = sum(int(round(Bx[e][1])) == fig["ask_b"][e]["claims_to_date"] for e in Bx)
    kept = k1 + k3 + k4
    print("Ask A member months kept %d of 18 (rows per member id)" % k1)
    print("Ask B members kept %d of 18, claims to date kept %d of 18 (latest row per member id)" % (k3, k4))
    C = 38 + 7 + ASK_W * kept
    d = B.surcharged(b, B.expected(b, "own_experience"))
    g = fig["call"]["surcharged"]
    hit = d == g
    same = sum((e in d) == (e in g) for e in b["ids"])
    m = 10 * hit + 28.0 / 18 * same
    S = m + 7 + ASK_W * kept
    print("cracker: call landed (38), instructions (7), ask figures kept %d of 54: %.1f" % (kept, C))
    print("mirror (the default path): main block %.1f (set %s, %d of 18 decisions kept), ask figures kept %d of 54: "
          "%.1f" % (m, "landed" if hit else "missed", same, kept, S))
    print("Mirror leakage: %.1f per cent of ask weight" % (100.0 * kept / 54))
    print("Pair ceiling: %.1f" % ((C + S) / 2))
    return (C + S) / 2


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
