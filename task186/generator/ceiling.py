"""The pair ceiling, measured on the cut pack (target/) against the golden.

Two responses are scored on every ask figure (12 monthly currency counts, 28 lane-quarter bag counts):
  cracker  lands the call, runs the hygiene battery, executes every filed rule: X-ray time shared among the officers
           rostered on the lane at each moment, quarters on Sydney dates, every CT unit placed on the lane it stood
           on that day (the register, the spare's days and the replaced unit all worked out), every hourly count kept;
  mirror   misses the call on the raw hit rate and stops at the most attractive wrong rung of each ask: the same
           X-ray time, each unit counted on the lane the register gives it now, Sydney quarters, every count kept.
A figure is kept when it equals the golden at the asked rounding. Scores use 38 (call and components), 7
(instructions) and 55 (asks), with 5 for the call side of a response that misses it.

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
    crack_b = placed_counts(T, keep_all=True)
    mirror_a = crack_a
    mirror_b = A.ask_b(T, mode="register")
    keys_b = sorted(gold_b)

    def kept(a, b):
        ka = sum(x == y for x, y in zip(a, gold_a))
        kb = sum(A.rnd_k(b.get(k, 0)) == A.rnd_k(gold_b[k]) for k in keys_b)
        return ka, kb
    ca, cb = kept(crack_a, crack_b)
    ma, mb = kept(mirror_a, mirror_b)
    n = len(gold_a) + len(keys_b)
    lc, ls = (ca + cb) / n, (ma + mb) / n
    c_score = 38 + 7 + 55 * lc
    s_score = 5 + 7 + 55 * ls
    pair = (c_score + s_score) / 2
    rows = {
        "cracker": {"ask_a_kept": ca, "ask_b_kept": cb, "keep": round(lc, 4), "score": round(c_score, 1)},
        "mirror": {"ask_a_kept": ma, "ask_b_kept": mb, "keep": round(ls, 4), "score": round(s_score, 1)},
        "pair_ceiling": round(pair, 1), "mirror_leakage_pct": round(100 * ls, 1), "figures": n,
        "cracker_a_missed_months": [i for i, (x, y) in enumerate(zip(crack_a, gold_a)) if x != y],
        "cracker_b_missed": ["%s %s" % k for k in keys_b if A.rnd_k(crack_b.get(k, 0)) != A.rnd_k(gold_b[k])],
    }
    print(json.dumps(rows, indent=1))
    return rows


if __name__ == "__main__":
    main()
