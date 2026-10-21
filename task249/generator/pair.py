"""The ask layer measured on the cut pack: each path a response could take through the two asks, the figures it keeps
against the golden, the cracker (on the call, every filed rule executed, the hygiene battery run, the best of the careful
routes: every WS_FAIL with the reported failures and the power cut, the round 2 readers' route, or that route with one
of its repairs; each client's losses overlapped with the clock, with the lone losses dropped or the stops taken out) and
the mirror (off the call, the first reading of each log: the WS_FAIL rows, every loss row), and the pair ceiling.
python3 pair.py [target]"""
import json
import os
import sys

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import solve as S

TASK = os.path.dirname(HERE)


A_PATHS = ["golden", "v2_route", "in_sitting", "stopped_fail", "reboots", "in_sitting_reboots", "unexplained",
           "ws_fail_only", "no_power"]
B_PATHS = ["golden", "per_booking", "per_booking_stops", "centre_only", "pairs_only", "lost_refs", "no_power"]
A_CAREFUL = ["v2_route", "in_sitting", "stopped_fail", "reboots", "in_sitting_reboots", "unexplained"]
B_CAREFUL = ["per_booking", "per_booking_stops", "centre_only", "pairs_only"]


def ask_a_paths(target, D):
    sets = S.ask_a_sets(target)
    return {k: S.ask_a(target, D=D, path=k, sets=sets)[0] for k in A_PATHS}


def ask_b_paths(target, D):
    sets = S.offline_sets(target, D)
    return {k: S.ask_b(target, D=D, path=k, sets=sets) for k in B_PATHS}


def keep(path, golden):
    return sum(path[k] == golden[k] for k in golden)


def main(target):
    D = S.load(target)
    A = ask_a_paths(target, D)
    B = ask_b_paths(target, D)
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    assert A["golden"] == fig["asks"]["interrupted"] and B["golden"] == fig["asks"]["offline"]
    print("Ask A paths (forms kept of 10):")
    for k, v in A.items():
        print("  %-26s %2d" % (k, keep(v, A["golden"])))
    print("Ask B paths (forms kept of 10):")
    for k, v in B.items():
        print("  %-26s %2d" % (k, keep(v, B["golden"])))
    n = 20
    kc = max(keep(A[k], A["golden"]) for k in A_CAREFUL) + max(keep(B[k], B["golden"]) for k in B_CAREFUL)
    km = keep(A["ws_fail_only"], A["golden"]) + keep(B["lost_refs"], B["golden"])
    c = 38 + 7 + 55 * kc / n
    s = 5 + 7 + 55 * km / n
    print("cracker keeps %d of %d ask figures; mirror keeps %d" % (kc, n, km))
    print("pair ceiling %.1f ((%.1f + %.1f) / 2); mirror leakage %.1f per cent of ask weight" % ((c + s) / 2, c, s, 100 * km / n))
    return dict(A=A, B=B, kc=kc, km=km)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(TASK, "target"))
