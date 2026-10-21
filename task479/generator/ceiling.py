"""The ask layer measured on the cut pack: the cracker (lands the call, runs the hygiene battery: one cell per
group, incurred and paid month and category, the later layout's copy of a re-sent month counted once, the latest
advisory per claimant, member months as enrollment rows per member id) and the mirror (the default path on the call,
the asks handled the cracker's way), priced against generator/figures.json on the weights 38 / 7 / 55.

    python3 task479/generator/ceiling.py [target]

The call is 38: the notice set 10 and the sixteen groups' retained PMPM 28 / 16 each. Instructions 7. The 64 ask
figures (sixteen groups' member months, paid PMPM, flagged members and their claims) are 55 / 64 each. The asks read
only 2026 rows, which the call never reads, so the two responses take the same ask readings; checks.py X1 proves the
separation."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import bundle as B    # noqa: E402

TASK = os.path.dirname(HERE)
ASK_W = 55.0 / 64


def main(target=None):
    target = target or os.path.join(TASK, "target")
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    b = B.load(target)
    A = B.ask_a(b, by_person=False)
    Bx = B.ask_b(b, by_person=False, take="latest")
    k1 = sum(A[g][0] == fig["ask_a"][g]["member_months"] for g in A)
    k2 = sum("%.2f" % A[g][1] == fig["ask_a"][g]["paid_pmpm"] for g in A)
    k3 = sum(Bx[g][0] == fig["ask_b"][g]["members"] for g in Bx)
    k4 = sum(int(round(Bx[g][1])) == fig["ask_b"][g]["claims_to_date"] for g in Bx)
    kept = k1 + k2 + k3 + k4
    print("Ask A member months kept %d of 16, paid PMPM kept %d of 16 (rows per member id)" % (k1, k2))
    print("Ask B members kept %d of 16, claims to date kept %d of 16 (latest advisory per claimant number)" % (k3, k4))
    C = 38 + 7 + ASK_W * kept
    d = B.retained27(b, "default")
    hit = B.notices(b, d) == fig["call"]["notices"]
    rates = sum("%d" % round(d[g]) == fig["retained_pmpm"][g] for g in d)
    m = 10 * hit + 28.0 / 16 * rates
    S = m + 7 + ASK_W * kept
    print("cracker: call landed (38), instructions (7), ask figures kept %d of 64: %.1f" % (kept, C))
    print("mirror (the default path): main block %.1f (set %s, %d retained figures kept), ask figures kept %d of 64: "
          "%.1f" % (m, "landed" if hit else "missed", rates, kept, S))
    print("Mirror leakage: %.1f per cent of ask weight" % (100.0 * kept / 64))
    print("Pair ceiling: %.1f" % ((C + S) / 2))
    return (C + S) / 2


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
