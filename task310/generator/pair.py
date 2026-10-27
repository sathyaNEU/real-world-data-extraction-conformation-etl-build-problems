"""The ask sheet's measurement on the cut pack: the cracker (lands the call, runs the battery, executes every filed rule
and the careful route through each ask) and the mirror (the easy route's call on the recorded readings, the same ask
routes), scored figure by figure on the 38/7/55 weights, with every path each ask offers a response that does not meet
its device.

    python3 task310/generator/pair.py <target dir>
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import params as P  # noqa: E402
import solve as S  # noqa: E402

REC, IF, ASK = 38.0, 7.0, 55.0


def rnd(v, u):
    return math.floor(v / u + 0.5) * u


def main(target):
    F = json.load(open(os.path.join(HERE, "figures.json")))
    name, inv = P.REGIONS, {v: k for k, v in P.REGIONS.items()}
    pk, res = S.solve(target)

    def call_hits(v):
        o = S.order(v)
        yrs = {name[r]: P.ROUND_YEARS[i] for i, r in enumerate(o)}
        h = sum(yrs[n] == F["schedule"][n] for n in F["schedule"])
        h += sum(rnd(v[r], 50) == F["kwh_per_battery"][name[r]] for r in P.REGION_ORDER)
        h += sum(rnd(2.4 * v[r], 100) == F["round_mwh"][name[r]] for r in P.REGION_ORDER)
        return h
    c_call, m_call = call_hits(res["golden"]), call_hits(res["recorded"])
    print("call figures (12): cracker %d, mirror %d (the recorded readings)" % (c_call, m_call))

    def score_a(mode):
        a = S.ask_eligible(target, mode)
        return sum(int(a.get(n, -1)) == F["ask_a"][n] for n in F["ask_a"])

    def score_b(mode):
        b = S.ask_pilot(target, mode)
        return sum(round(rnd(b[i], 0.1), 1) == list(F["ask_b"].values())[i] for i in range(4))

    def score_c(mode):
        c = S.ask_installs(target, mode)
        return sum(int(c.get(n, -1)) == F["ask_c"][n] for n in F["ask_c"])
    paths = [("A", "solar dated from the NMI's own earliest PV row, claims by NMI chain and address (the cracker)",
              score_a, "nmi_min"),
             ("A", "solar dated from the active PV row", score_a, "active_row"),
             ("A", "no Booster claims read", score_a, "der_only"),
             ("A", "claims by the NMI they carry only", score_a, "nmi_only"),
             ("A", "claims by address as written", score_a, "no_normalise"),
             ("B", "re-sent rows dropped, counters at quarter ends, every unit summed (the cracker)", score_b, "counters"),
             ("B", "every two-unit home counted once", score_b, "pairs_once"),
             ("B", "re-sent rows dropped, daily rows summed", score_b, "daily"),
             ("B", "every row summed", score_b, "rows"),
             ("C", "certificates after amendments, numbers mapped, by suburb (the cracker)", score_c, "careful"),
             ("C", "shared modules collapsed to the first lodgement before the amendments", score_c, "dedup_first"),
             ("C", "near-duplicates merged on installer, date, suburb and model", score_c, "neighbour_merge"),
             ("C", "amendments not applied", score_c, "no_amendments"),
             ("C", "only the new accreditation numbers recognised", score_c, "current_numbers_only"),
             ("C", "region from the postcode", score_c, "by_postcode")]
    keep = {}
    for ask, label, fn, mode in paths:
        h = fn(mode)
        print("ask %s  %-100s %d of 4" % (ask, label, h))
        if "cracker" in label:
            keep[ask] = h
    ls = sum(keep.values()) / 12.0
    cracker = REC * c_call / 12.0 + IF + ASK * ls
    mirror = REC * m_call / 12.0 + IF + ASK * ls
    print("cracker: %.1f, mirror: %.1f" % (cracker, mirror))
    print("Pair ceiling: %.1f" % ((cracker + mirror) / 2))
    print("Mirror leakage: %.1f per cent of ask weight" % (100.0 * ls))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")))
