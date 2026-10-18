"""The pair ceiling and mirror leakage, scored on the cut pack with the house weights 38 / 7 / 55.

Main block (38): the call, its runner-up and gap (8) and each candidate's 2026 trips (30 over the 14). Asks (55): each
candidate's passengers (14 figures). Instructions (7). The cracker lands the call, runs the battery and executes every
filed rule it points at (the collection-window weighting, the coded party); the reconciling cracker does the same and
reads Q4 in the verbatims against the coded party, as reader rounds 2 and 3 did, recoding every party from the answer
as written; the mirror stops at the default path (each wave's returned cards expanded to its quarter, the coded
party). A figure scores when it rounds to the golden's hundred. The weights where the trips count as asks are printed
beside it; the gate reads the house weights and the reconciling cracker.

    python3 task471/generator/ceiling.py [target]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import bundle as B     # noqa: E402
import methods as M    # noqa: E402


def score(P):
    cand = P.candidates
    gold_t = M.estimate(P)
    gold_p = M.estimate(P, unit="passengers")
    rows = {
        "cracker": (gold_t, M.estimate(P, unit="passengers", party="coded")),
        "reconciling": (gold_t, gold_p),
        "mirror": (M.estimate(P, how="raw"), M.estimate(P, how="raw", unit="passengers", party="coded")),
    }
    gold_call = M.top3(gold_t, cand)
    out = {}
    for who, (t, p) in rows.items():
        call = M.top3(t, cand) == gold_call
        kt = sum(1 for m in cand if B.r100(t[m]) == B.r100(gold_t[m]))
        kp = sum(1 for m in cand if B.r100(p[m]) == B.r100(gold_p[m]))
        house = (8 if call else 0) + 30.0 * kt / len(cand) + 7 + 55.0 * kp / len(cand)
        alt = (38 if call else 0) + 7 + 55.0 * (kt + kp) / (2 * len(cand))
        out[who] = dict(call=call, trips_kept=kt, pax_kept=kp, house=house, alt=alt)
    out["pair_house"] = (out["cracker"]["house"] + out["mirror"]["house"]) / 2
    out["pair_alt"] = (out["cracker"]["alt"] + out["mirror"]["alt"]) / 2
    out["pair_reconciling"] = (out["reconciling"]["house"] + out["mirror"]["house"]) / 2
    out["mirror_leakage"] = 100.0 * out["mirror"]["pax_kept"] / len(cand)
    return out


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")
    P = B.Pack(target)
    o = score(P)
    n = len(P.candidates)
    for who in ("cracker", "reconciling", "mirror"):
        r = o[who]
        print("%-11s call %-5s trips kept %2d/%d  passengers kept %2d/%d  house %.1f  alt %.1f" % (
            who, r["call"], r["trips_kept"], n, r["pax_kept"], n, r["house"], r["alt"]))
    print("pair ceiling %.1f (house weights 38/7/55) with the cracker on the coded party, %.1f with the reconciling "
          "cracker; %.1f if the trips count as asks; mirror leakage %.1f per cent"
          % (o["pair_house"], o["pair_reconciling"], o["pair_alt"], o["mirror_leakage"]))
