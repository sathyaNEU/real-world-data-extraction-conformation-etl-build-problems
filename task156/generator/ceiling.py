"""The ask layer's ceiling, measured on the cut pack: each response's ask figures recomputed from target/ with the
handling that response applies, scored against the golden handling on the same files (a hit is the same figure at the
asked rounding), and the pair priced on the planning weights (38 for the call and its components, 7 for
instruction-following, 55 for the asks).

    python3 task156/generator/ceiling.py [target]

Rows: the cracker lands the call (the delegates in post on the ballot), runs the hygiene battery and executes every
filed rule: one copy of each advice, the bureau's payments split by its statements, each advice placed by the date it
carries, FP-04's Sunday period end read as what the period_end column already holds (Ask A); travel and administration
out, every organiser's own rows counted (the prompt's two-organiser clause), each forum's hours shared by the sign-ins,
no moved booking found because no field marks one (Ask B). The mirror files the members' own voting history and handles the asks the same
way, since they carry nothing from the call. The full includer also moves the platform's Thursday dates back to their
period ends and keeps one row per organiser, invitation and day at its last update (a stress row, not the gate)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import asks as A   # noqa: E402


def kept(resp, gold):
    return sum(A.rnd(resp[k]) == A.rnd(gold[k]) for k in gold)


def main(target):
    ga, gb = A.ask_a(target), A.ask_b(target)
    n = len(ga) + len(gb)
    ca = kept(A.ask_a(target, payday=False), ga)
    cb = kept(A.ask_b(target, key=None), gb)
    crack = ca + cb
    full = kept(A.ask_a(target), ga) + kept(A.ask_b(target), gb)
    lc = crack / n
    c = 38 + 7 + 55 * lc
    s = 5 + 7 + 55 * lc
    print("cracker (lands the call, battery, filed rules; dates as carried, every organiser row): keeps %d "
          "of %d ask figures (Ask A %d of %d, Ask B %d of %d), response %.1f" % (crack, n, ca, len(ga), cb, len(gb), c))
    print("mirror (the members' own voting history, same ask handling): keeps %d of %d, response %.1f" % (crack, n, s))
    print("full includer (Thursday dates moved back, one row per organiser, invitation and day; stress row): keeps "
          "%d of %d, response %.1f" % (full, n, 38 + 7 + 55 * full / n))
    print("natural (every advice as sent, the bureau left whole, one row per invitation and day): keeps %d of %d"
          % (kept(A.ask_a(target, dedup=False, split=False, payday=False), ga) +
             kept(A.ask_b(target, key=("invitation_uid", "date")), gb), n))
    print("pair ceiling %.1f; mirror leakage %.1f per cent of the ask weight" % ((c + s) / 2, 100 * lc))
    return {"cracker": c, "mirror": s, "pair": (c + s) / 2, "leak": 100 * lc, "ca": ca, "cb": cb, "na": len(ga),
            "nb": len(gb)}


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target"))
