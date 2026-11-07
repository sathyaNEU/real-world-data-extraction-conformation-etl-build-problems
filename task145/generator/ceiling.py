"""task145 architecture 2: the ask layer's pair ceiling on the cut pack (supplemental-stumping Parts 0 and 1.1).

The cracker lands the call, runs the hygiene battery and executes every filed rule: it links a record opened without
a state id to the same student's earlier record by name and date of birth, keeps the last-entered of two incident
rows for one student, date, behaviour and action, applies the half-day rule on each school's bell schedule and Mesa
Vista's periods, counts each suspension's days on the school's instructional days as days absent, and keeps the
ten-day floor of the chronic absence rate. What it does not do is what no sentence states: end a student's record at
the school they left on the day before the next school's entry when the exit was entered later, and read a hearing
officer's amendment filed under a re-coded behaviour as the same suspension. The mirror stops at the early-warning
tier and reads the asks the same way. Each figure is scored against the golden at the asked rounding.

    python3 task145/generator/ceiling.py [target]
"""
import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import analysis as A  # noqa: E402

CRACKER_A = dict(overlap=False, dedupe="battery")
CRACKER_B = dict(dedupe="battery")
STRESS_A = {
    "records as filed, every incident row kept": dict(overlap=False, dedupe=False),
    "suspension days from the attendance rows only, records as filed": dict(overlap=False, add_oss=False),
    "records without a state id taken as new students": dict(link_names=False),
    "one school a day, battery dedupe (the overlap found)": dict(dedupe="battery"),
    "the full includer (every device handled)": dict(),
}
STRESS_B = {
    "every incident row kept": dict(dedupe=False),
    "the full includer (every device handled)": dict(),
}


def kept_a(gold, other):
    return sum(1 for k in gold if round(other[k][0], 1) == round(gold[k][0], 1))


def kept_b(gold, other):
    return sum(1 for k in gold if other[k] == gold[k])


def main(target):
    S = A.solve(target)
    gold_a, gold_b = A.ask_a(target, S), A.ask_b(target, S)
    na, nb = len(gold_a), len(gold_b)
    n = na + nb
    ca = kept_a(gold_a, A.ask_a(target, S, **CRACKER_A))
    cb = kept_b(gold_b, A.ask_b(target, S, **CRACKER_B))
    print("cracker  ask A keeps %2d of %d (records as filed, battery dedupe)" % (ca, na))
    print("cracker  ask B keeps %2d of %d (battery dedupe)" % (cb, nb))
    for k, kw in STRESS_A.items():
        print("stress   ask A  %-58s keeps %2d of %d" % (k, kept_a(gold_a, A.ask_a(target, S, **kw)), na))
    for k, kw in STRESS_B.items():
        print("stress   ask B  %-58s keeps %2d of %d" % (k, kept_b(gold_b, A.ask_b(target, S, **kw)), nb))
    crack = ca + cb
    mirror = crack
    c = 38 + 7 + 55.0 * crack / n
    s = 5 + 7 + 55.0 * mirror / n
    zp = os.path.join(TASK, "target.zip")
    if os.path.exists(zp):
        print("measured on target.zip %s" % hashlib.sha256(open(zp, "rb").read()).hexdigest()[:8])
    print("cracker keeps %d of %d ask figures, scores %.1f with the call" % (crack, n, c))
    print("mirror keeps %d of %d, scores %.1f off it" % (mirror, n, s))
    print("Pair ceiling: %.1f" % ((c + s) / 2))
    print("Mirror leakage: %.1f per cent of ask weight" % (100.0 * mirror / n))
    return dict(crack=crack, mirror=mirror, n=n, pair=(c + s) / 2, ca=ca, cb=cb)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(TASK, "target"))
