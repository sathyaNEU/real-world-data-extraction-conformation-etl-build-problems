"""The pair ceiling on the cut pack (supplemental-stumping Part 0, weights 38 / 7 / 55, r = 5).

The cracker lands the call, runs the hygiene battery and executes every filed rule it points at: the old
platform's student numbers through the cutover crosswalk, each platform's attempts conformed, the review log with its
withdrawals, Policy 4.12's higher level and later sitting, and each sitting's college as the attempt records carry
it. The mirror stops at the default path (the bank difficulties as filed) and reads the asks the same way.

The asks consume nothing the call's construction produces (checks.py X1 to X3 assert the separation), so the two
rows read the asks alike by construction; the script says so rather than printing one reading twice, and scores the
half-handled readings beside them."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
TASK = os.path.dirname(HERE)

import bundle as B   # noqa: E402

FIELDS = ("placed", "CA", "CCA", "twice")


def score(read, gold):
    hits = 0
    total = 0
    for c in B.CODES:
        for k in FIELDS:
            total += 1
            hits += read[c][k] == gold[c][k]
    for k in FIELDS:
        total += 1
        hits += sum(read[c][k] for c in B.CODES) == sum(gold[c][k] for c in B.CODES)
    return hits, total


def main():
    b = B.open_pack(os.path.join(TASK, "target"))
    F = json.load(open(os.path.join(HERE, "figures.json")))
    gold = {c: F["colleges"][c] for c in B.CODES}
    reads = {
        "cracker and mirror (crosswalk ids, the attempt records' college, review log applied)":
            B.colleges(b, persons="ids", college="export"),
        "half: the score reports' college, ids as recorded":
            B.colleges(b, persons="ids", college="reports"),
        "half: one student across identifiers, the attempt records' college":
            B.colleges(b, persons="four_fields", college="export"),
        "over-merge: birth date, sex and high school only, the score reports' college":
            B.colleges(b, persons="three_fields", college="reports"),
        "both devices handled, the review log ignored":
            B.colleges(b, persons="four_fields", college="reports", sessions="ignore"),
        "golden": B.colleges(b),
    }
    out = {}
    for name, read in reads.items():
        h, t = score(read, gold)
        out[name] = (h, t)
        print("%-90s keeps %2d of %d ask figures" % (name, h, t))
    hc, tot = out["cracker and mirror (crosswalk ids, the attempt records' college, review log applied)"]
    lc = hc / tot
    cracker = 38 + 7 + 55 * lc
    mirror = 5 + 7 + 55 * lc
    pair = (cracker + mirror) / 2
    print("cracker %.1f (call, instructions, %d of %d asks); mirror %.1f (r 5, instructions, %d of %d asks)"
          % (cracker, hc, tot, mirror, hc, tot))
    print("Pair ceiling: %.1f" % pair)
    print("Mirror leakage: %.1f per cent of ask weight" % (100.0 * lc))
    print("The asks read no row the call's construction produces, so the cracker's and the mirror's ask readings "
          "coincide by construction (checks.py X1 to X3); the half-handled rows above are the measured spread.")
    assert pair <= 40.0 and lc < 0.35
    return 0


if __name__ == "__main__":
    sys.exit(main())
