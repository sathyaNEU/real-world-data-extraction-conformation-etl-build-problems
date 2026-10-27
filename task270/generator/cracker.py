"""task270 cracker: the asks as a careful solver who landed the call reads them, on the cut pack. It runs the hygiene
battery (exact duplicates, key uniqueness, unmatched joins) and executes every filed rule the asks point at (the DBT
programme operating standard's 3.1, 3.2 and 4.2): Ask A from the learning records joined to the 2026 catalogue,
counting the courses its titles call four-day DBT skills group facilitation, with their assignments' whole-time
equivalent; Ask B from the referral module's received
dates as they stand, each patient in the team holding their care on 31 December. Every ask figure it gives is scored
against the golden, a hit within half a unit of the stated rounding, beside each other wrong route.

    python3 task270/generator/cracker.py [TARGET]"""
from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import asks as A        # noqa: E402
import common as K      # noqa: E402

ROUTES_A = [("catalogue", "the cracker: the 2026 catalogue's four-day DBT facilitation titles"),
            ("every114", "every PTD-114 and PTD-301 completion counted"),
            ("no_chain", "training under a previous employee number left out")]
ROUTES_B = [("module", "the cracker: the module's received dates as they stand"),
            ("drop", "the referrals moved over from the service's database left out"),
            ("earliest", "the patient's earliest acknowledgement letter"),
            ("referring", "the module's referring team instead of the team on 31 December")]


def run(target=None):
    target = target or K.TARGET
    gold_a = A.ask_a(target)
    gold_b = {c: K.round_half_up(v[1], 1) for c, v in A.ask_b(target).items()}
    out = []
    for rule, desc in ROUTES_A:
        got = A.ask_a(target, rule=rule)
        hits = [(c, k) for c in gold_a for k in (0, 1) if abs(got[c][k] - gold_a[c][k]) < 0.005]
        out.append(("A", rule, desc, got, hits))
    for rule, desc in ROUTES_B:
        got = {c: K.round_half_up(v[1], 1) for c, v in A.ask_b(target, rule=rule).items()}
        hits = [c for c in gold_b if abs(got[c] - gold_b[c]) < 0.05]
        out.append(("B", rule, desc, got, hits))
    return gold_a, gold_b, out


def main(target=None):
    gold_a, gold_b, out = run(target)
    teams = [c for c, _ in K.TEAMS]
    print("%-10s %s" % ("team", " ".join("%7s" % K.TEAM_NAME[c][:7] for c in teams)))
    print("%-10s %s" % ("A golden", " ".join("%2d %4.2f" % gold_a[c] for c in teams)))
    for ask, rule, desc, got, hits in out:
        if ask == "A":
            print("%-10s %s  | keeps %d of 22 (%s)" % (rule, " ".join("%2d %4.2f" % got[c] for c in teams), len(hits),
                                                      desc))
    print("%-10s %s" % ("B golden", " ".join("%7.1f" % gold_b[c] for c in teams)))
    for ask, rule, desc, got, hits in out:
        if ask == "B":
            print("%-10s %s  | keeps %d of 11 (%s)" % (rule, " ".join("%7.1f" % got[c] for c in teams), len(hits), desc))
    crack = [o for o in out if o[1] in ("catalogue", "module")]
    kept = sum(len(o[4]) for o in crack)
    # the pair ceiling: the cracker lands the call (38 recommendation and critical components, 7 instruction
    # following) and keeps `kept` of the 33 ask figures of 55; the mirror misses the call (about 5) and reads the asks
    # the same way, since they consume nothing the call's construction produces
    lc = kept / 33.0
    pair = ((38 + 7 + 55 * lc) + (5 + 7 + 55 * lc)) / 2
    print("cracker keeps %d of 33 ask figures; mirror leakage %.0f per cent; pair ceiling %.1f"
          % (kept, 100 * lc, pair))
    return 0 if kept == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else None))
