"""The pair ceiling, measured on the cut pack (target/) against the golden.

Two responses are scored on every ask figure (12 monthly currency counts, 28 lane-quarter bag counts):
  cracker  lands the call, runs the hygiene battery and executes every filed rule: X-ray time shared among the officers
           rostered on the lane at each moment (SCS-04 section 3), whole-month endorsement from the register's dates,
           quarters on Sydney dates, every count before a lane's first rostered start dropped as start-up test images
           (SCS-04 section 3), each CT unit on the lane the unit register gives it; it does not join the payroll leave
           export or rebuild where each unit stood day by day (the two devices);
  mirror   misses the call on the raw hit rate and stops at the same rungs of each ask.
A figure is kept when it equals the golden at the asked rounding. Scores use 38 (call and components), 7
(instructions) and 55 (asks), with 5 for the call side of a response that misses it. The full includer, who also
joins the leave export and rebuilds every unit's lane, is printed for the record.

    python3 task186/generator/ceiling.py
"""
import json
import os
import sys

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import analysis as A  # noqa: E402
import params as P  # noqa: E402


def placed_counts(T, keep_all=True):
    assign, c, lh = A.unit_lanes(T)
    inv = {(d, u): ln for (d, ln), u in assign.items()}
    c["lane"] = [inv.get((d, u)) for d, u in zip(c["date"], c["unit_serial"])]
    c["d"] = pd.to_datetime(c["date"]).dt.date
    c = c[c["lane"].isin(P.LANES)]
    if not keep_all:
        c = c[[h in lh.get((d, ln), set()) for d, ln, h in zip(c["date"], c["lane"], c["h"])]]
    out = {}
    for q, a, b in A.QUARTERS:
        m = (c["d"] >= a) & (c["d"] <= b)
        out.update({(ln, q): int(v) for ln, v in c[m].groupby("lane")["bags_imaged"].sum().items()})
    return out


def main():
    T = A.load(os.path.join(TASK, "target"))
    gold_a, _ = A.ask_a(T)
    gold_b = A.ask_b(T)
    crack_a, _ = A.ask_a(T, use_leave=False)
    crack_b = A.ask_b(T, mode="register_open")
    mirror_a = crack_a
    mirror_b = crack_b
    full_b = placed_counts(T, keep_all=False)
    keys_b = sorted(gold_b)

    def kept(a, b):
        ka = sum(x == y for x, y in zip(a, gold_a))
        kb = sum(A.rnd_k(b.get(k, 0)) == A.rnd_k(gold_b[k]) for k in keys_b)
        return ka, kb
    ca, cb = kept(crack_a, crack_b)
    ma, mb = kept(mirror_a, mirror_b)
    fa, fb = kept(gold_a, full_b)
    n = len(gold_a) + len(keys_b)
    lc, ls = (ca + cb) / n, (ma + mb) / n
    c_score = 38 + 7 + 55 * lc
    s_score = 5 + 7 + 55 * ls
    pair = (c_score + s_score) / 2
    rows = {
        "cracker": {"ask_a_kept": ca, "ask_b_kept": cb, "keep": round(lc, 4), "score": round(c_score, 1)},
        "mirror": {"ask_a_kept": ma, "ask_b_kept": mb, "keep": round(ls, 4), "score": round(s_score, 1)},
        "pair_ceiling": round(pair, 1), "mirror_leakage_pct": round(100 * ls, 1), "figures": n,
        "full_includer_kept": "%d of %d" % (fa + fb, n),
        "cracker_a_missed_months": [i for i, (x, y) in enumerate(zip(crack_a, gold_a)) if x != y],
        "cracker_b_missed": ["%s %s" % k for k in keys_b if A.rnd_k(crack_b.get(k, 0)) != A.rnd_k(gold_b[k])],
    }
    print(json.dumps(rows, indent=1))
    return rows


if __name__ == "__main__":
    main()
