"""The ask sheet's measurement on the cut pack: the cracker (lands the call, runs the battery, executes every filed rule)
and the mirror (the default path's call), each scored figure by figure on the 38/7/55 weights, over every path each
ask offers a response that does not meet its device.

    python3 task308/generator/pair.py <target dir>
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import params as P
import solve as S

REC, IF, ASK = 38.0, 7.0, 55.0
# the recommendation weight: the pick, the four values, the three critical components
W_PICK, W_VALUE, W_CC = 10.0, 4.0, 4.0


def r1(x):
    return round(x + 1e-9, 1)


def main(target):
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    mc = S.main_call(target)
    dflt = {r: mc["default"][r]["value"] for r in P.REGIONS}
    sign = mc["family_default"]["sign"]
    A = {"|".join(r): S.ask_a(target, r) for r in S.A_ROUTES if r != S.A_GOLDEN}
    B = {r: S.ask_b(target, r) for r in S.B_ROUTES if r != "golden"}
    gA = figs["askA"]
    gB = figs["askB"]
    ncell = 12 + 4

    def hits_a(route):
        return sum(round(A[route]["%s|%s" % (r, y)] + 1e-9, 2) == gA[r][y] for r in P.REGIONS for y in gA[r])

    def hits_b(route):
        return sum(r1(B[route][r]["si_m"]) == gB[r] for r in P.REGIONS)

    rows = []
    for ra in A:
        for rb in B:
            rows.append((ra, rb, hits_a(ra), hits_b(rb)))
    rows.sort(key=lambda t: -(t[2] + t[3]))
    best = max(rows, key=lambda t: t[2] + t[3])
    keep = (best[2] + best[3]) / ncell
    # the mirror: the default path's call, each value scored against the golden's
    mirror_rec = 0.0
    for idx in (dflt, sign):
        v = sum(W_VALUE for r in P.REGIONS if r1(idx[r]) == figs["values"][r])
        mirror_rec = max(mirror_rec, v)
    cracker = REC + IF + ASK * keep
    mirror = mirror_rec + IF + ASK * keep
    pair = (cracker + mirror) / 2
    print("ask paths (A route, B route, A cells kept of 12, B cells kept of 4):")
    for t in rows[:12]:
        print("   %-22s %-18s %2d  %d" % t)
    print("   ... %d paths in all" % len(rows))
    print("best path keeps %d of %d ask cells (%.1f per cent of ask weight)" % (best[2] + best[3], ncell, 100 * keep))
    print("cracker %.1f (call, %d of 16 ask cells); mirror %.1f (%.0f of 38 recommendation points, the same ask path)"
          % (cracker, best[2] + best[3], mirror, mirror_rec))
    print("Pair ceiling: %.1f" % pair)
    print("Mirror leakage: %.1f per cent of ask weight" % (100 * keep))
    return dict(pair=pair, keep=keep, rows=rows, mirror_rec=mirror_rec)


if __name__ == "__main__":
    tgt = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")
    main(tgt)
