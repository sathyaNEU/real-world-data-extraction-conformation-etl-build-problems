"""The ask layer measured on the cut pack: each path a response could take through the two asks, the figures it keeps
against the golden, the cracker (on the call, every filed rule executed, the hygiene battery run: the event log's
failures with the power cut read off the resumes and the report, the link losses paired per client and overlapped with
the clock, the measured readers' route) and the mirror (off the call, the first reading of each log: the WS_FAIL rows,
every loss row), and the pair ceiling.
python3 pair.py [target]"""
import json
import os
import sys

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import solve as S

TASK = os.path.dirname(HERE)


A_PATHS = ["golden", "ws_fail_only", "log_only", "reports_only", "union_by_ws", "spares_all", "no_power"]
B_PATHS = ["golden", "lost_refs", "lost_within", "pairs_only", "no_power"]


def ask_a_paths(target, D):
    return {k: S.ask_a(target, D=D, path=k)[0] for k in A_PATHS}


def ask_b_paths(target, D):
    return {k: S.ask_b(target, D=D, path=k) for k in B_PATHS}


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
    kc = keep(A["log_only"], A["golden"]) + keep(B["pairs_only"], B["golden"])
    km = keep(A["ws_fail_only"], A["golden"]) + keep(B["lost_refs"], B["golden"])
    c = 38 + 7 + 55 * kc / n
    s = 5 + 7 + 55 * km / n
    print("cracker keeps %d of %d ask figures; mirror keeps %d" % (kc, n, km))
    print("pair ceiling %.1f ((%.1f + %.1f) / 2); mirror leakage %.1f per cent of ask weight" % ((c + s) / 2, c, s, 100 * km / n))
    return dict(A=A, B=B, kc=kc, km=km)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(TASK, "target"))
