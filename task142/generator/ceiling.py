"""Pair ceiling on the cut pack: the cracker (lands the call, runs the hygiene battery, reads every document) and the
mirror (stops at the pooled share) answer every ask the careful way they would; each figure is scored against the
golden at the prompt's rounding.

    python3 task142/generator/ceiling.py            # exit 1 if the pair ceiling exceeds 60 or leakage reaches 50
"""
import os
import re
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import analysis as A  # noqa: E402

TARGET = os.path.join(TASK, "target")
CALL_POINTS, OFF_POINTS, ASK_WEIGHT = 45.0, 12.0, 55.0


def cracker_gas(T):
    """The accommodation plan's EANs, the resent read dropped, each serial's first and last read in the school year."""
    eans = set(re.findall(r"8716\d{14}", T["plan"]))
    reads = defaultdict(list)
    seen = set()
    for r in T["gasreads"]:
        k = tuple(r.values())
        if k in seen or r["ean"] not in eans:
            continue
        seen.add(k)
        reads[(r["ean"], r["meternummer"])].append((r["tijdstip"][:16], int(r["meterstand_m3"])))
    out = {}
    for sy in (2023, 2024, 2025):
        a, b = "%d-08-01T06:00" % sy, "%d-08-01T06:00" % (sy + 1)
        tot = 0
        for v in reads.values():
            rs = sorted(x for x in v if a <= x[0] <= b)
            if rs:
                tot += rs[-1][1] - rs[0][1]
        out[sy] = tot
    return out


def cracker_bso(T):
    """De Kwikstaart families from the contracts, the children summed, every location code."""
    school = {r["gezinsnummer"]: r["school"] for r in T["bso_con"]}
    out = {k: 0 for k in range(5)}
    for r in T["bso"]:
        if school.get(r["gezinsnummer"]) == "De Kwikstaart":
            out[A.dmy(r["datum"]).weekday()] += int(r["aantal_kinderen"])
    return out


def score(F, gas, bso):
    figs = [("gas %d-%02d" % (sy, (sy + 1) % 100), A.rnd(gas[sy], 1000) == F["gas_m3"][str(sy)]) for sy in (2023, 2024, 2025)]
    figs += [("after-school care weekday %d" % k, bso[k] == F["bso"][str(k)]) for k in range(5)]
    return figs


def main(target=TARGET):
    F, M = A.figures(target)
    T = M["T"]
    figs = score(F, cracker_gas(T), cracker_bso(T))
    if not figs:
        raise SystemExit("ceiling: no ask figure was scored, so no verdict is printed")
    kept = sum(1 for _, h in figs if h) / len(figs)
    cracker, mirror = CALL_POINTS + ASK_WEIGHT * kept, OFF_POINTS + ASK_WEIGHT * kept
    pair = (cracker + mirror) / 2
    print("ask figures kept by the cracker: %d of %d" % (sum(1 for _, h in figs if h), len(figs)))
    for n, h in figs:
        print("  %-30s %s" % (n, "hit" if h else "miss"))
    print("cracker %.1f  mirror %.1f  pair ceiling %.1f  mirror leakage %.1f per cent" % (cracker, mirror, pair, 100 * kept))
    full = score(F, A.gas_by_year(T), A.bso_by_weekday(T))
    print("full includer keeps %d of %d" % (sum(1 for _, h in full if h), len(full)))
    return pair, 100 * kept, figs


if __name__ == "__main__":
    p, l, _ = main(sys.argv[1] if len(sys.argv) > 1 else TARGET)
    sys.exit(0 if p <= 60 and l < 50 else 1)
