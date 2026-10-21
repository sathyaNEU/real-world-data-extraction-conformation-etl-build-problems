"""The ask layer measured on the cut pack: the cracker (lands the call, runs the hygiene battery: one cell per
district, incurred and paid month and category, the later layout's copy of the re-sent month counted once, the latest
advisory per claimant, member months as eligibility rows per member id) and the mirror (the default path on the call,
the asks handled the cracker's way), priced against generator/figures.json on the weights 38 / 7 / 55.

    python3 task479/generator/ceiling.py [target]

The call is 38: the raised set 10 and the sixteen districts' expected PMPM 28 / 16 each. Instructions 7. The 48 ask
figures (sixteen districts' July to September member months, members on advisory and their claims) are 55 / 48 each.
The asks read only July to September 2026 enrollment and the advisories, which the call never reads, so the two
responses take the same ask readings; checks.py X1 proves the separation."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import bundle as B    # noqa: E402

TASK = os.path.dirname(HERE)
ASK_W = 55.0 / 48


def r10(v):
    return int(10 * round(v / 10))


def main(target=None):
    target = target or os.path.join(TASK, "target")
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    b = B.load(target)
    A = B.ask_a(b, by_person=False)
    Bx = B.ask_b(b, by_person=False, take="latest")
    k1 = sum(A[d] == fig["ask_a"][d] for d in A)
    k3 = sum(Bx[d][0] == fig["ask_b"][d]["members"] for d in Bx)
    k4 = sum(int(round(Bx[d][1])) == fig["ask_b"][d]["claims_to_date"] for d in Bx)
    kept = k1 + k3 + k4
    print("Ask A member months kept %d of 16 (rows per member id)" % k1)
    print("Ask B members kept %d of 16, claims to date kept %d of 16 (latest advisory per claimant number)" % (k3, k4))
    C = 38 + 7 + ASK_W * kept
    d = B.expected(b, "default")
    hit = B.raised(b, d) == fig["call"]["raised"]
    pm = sum(r10(d[i]) == fig["expected_pmpm"][i] for i in d)
    m = 10 * hit + 28.0 / 16 * pm
    S = m + 7 + ASK_W * kept
    print("cracker: call landed (38), instructions (7), ask figures kept %d of 48: %.1f" % (kept, C))
    print("mirror (the default path): main block %.1f (set %s, %d expected PMPM figures kept), ask figures kept %d of "
          "48: %.1f" % (m, "landed" if hit else "missed", pm, kept, S))
    print("Mirror leakage: %.1f per cent of ask weight" % (100.0 * kept / 48))
    print("Pair ceiling: %.1f" % ((C + S) / 2))
    return (C + S) / 2


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
