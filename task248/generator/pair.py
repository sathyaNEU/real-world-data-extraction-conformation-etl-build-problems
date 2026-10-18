"""task248 pair measurement on the cut pack. The cracker lands the call and takes each ask the way a careful analyst who
has not met the device would: the historian's hours on a clock grid after removing duplicate timestamps (or on every
wall-clock hour), the contract laboratory's copies per microlitre of extract scaled from the concentrate to the litre
without the aliquot step. The mirror stops at a wrong rung on the call (the published or any constant-rate count) and
takes each ask by the path that keeps it the most figures. Every ask figure is scored against the golden exactly (whole
hours and counts). The careful cracker's alternative (every device met) is printed too.

    python3 task248/generator/pair.py [target]
    python3 task248/generator/pair.py --ladder [target]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build as B
import solve

TARGET = os.path.join(os.path.dirname(HERE), "target")


def paths(pk):
    return {
        "cracker": (pk.ask_a(dedup="key"), pk.ask_b(contract_factor=pk.contract_naive)[0]),
        "wall-clock grid": (pk.ask_a(grid="naive"), pk.ask_b(contract_factor=pk.contract_naive)[0]),
        "rows only, as reported": (pk.ask_a(absent=False), pk.ask_b(contract_factor=1.0)[0]),
        "form's flow, first run": (pk.ask_a(grid="naive"), pk.ask_b(flow="form", runs="first")[0]),
        "every device met": (pk.ask_a(), pk.ask_b()[0]),
    }


def score(pk, P):
    ga, gb = pk.ask_a(), pk.ask_b()[0]
    n = 2 * len(pk.codes)
    keep = {}
    for k, (a, b) in P.items():
        hits = ["hours " + c for c in pk.codes if a[c] == ga[c]] + ["check " + c for c in pk.codes if b[c] == gb[c]]
        keep[k] = len(hits) / n
        print("%-24s keeps %2d of %d ask figures" % (k, len(hits), n))
    return keep


def main(target=TARGET):
    pk, par, rows = solve.solve(target, B.FILES)
    P = paths(pk)
    keep = score(pk, P)
    R, _ = pk.rungs()
    shed = {r["plant"]: r["shed"] for r in rows}
    for k in ("published", "constant", "pmmov", "study plants only", "additive"):
        moved = {c: R[k][c] - R["published"][c] for c in pk.codes if R[k][c] != R["published"][c]}
        print("rung %-18s total %d, moves %s, lands the call: %s" % (k, sum(R[k].values()), moved, R[k] == shed))
    # the mirror keeps the published total (the bridge's start) and nothing of the shed side: about a tenth of the
    # recommendation weight
    r_miss = round(38 * 0.12, 1)
    lazy = max(v for k, v in keep.items() if k != "every device met")
    lc = keep["cracker"]
    c, s = 38 + 7 + 55 * lc, r_miss + 7 + 55 * lazy
    print("Pair ceiling: %.1f" % ((c + s) / 2))
    print("Mirror leakage: %.1f per cent of ask weight" % (100 * lazy))
    full = keep["every device met"]
    print("If the cracker meets every device: %.1f; if both meet every device and one lands the call: %.1f" % (
        (38 + 7 + 55 * full + s) / 2, (38 + 7 + 55 * full + r_miss + 7 + 55 * full) / 2))
    return (c + s) / 2, 100 * lazy


def ladder(target=TARGET):
    pk, par, rows = solve.solve(target, B.FILES)
    R, _ = pk.rungs()
    print("decay", par)
    print("%-18s %s" % ("", " ".join("%3s" % c for c in pk.codes)))
    for k, v in R.items():
        print("%-18s %s  %d" % (k, " ".join("%3d" % v[c] for c in pk.codes), sum(v.values())))
    V = pk.variants()
    for k, v in V.items():
        print("variant %-40s %d" % (k, sum(v.values())))
    import aim
    _, kc = pk.fit("constant")
    print("constant rate %.4f an hour; additive term c0 %.3f c1 %.4f c2 %.4f" % ((kc["k"],) + tuple(pk.additive())))
    _, plev = pk.counts()
    _, slev = pk.counts(pk.shed_corr()[0])
    for c in pk.codes:
        lp, bp = plev[c]
        ls, bs = slev[c]
        w = [x for x in lp if solve.WINTER[0] <= x <= solve.WINTER[1]]
        print("%s baseline lift %.3f; winter peak published %.2f, shed %.2f; margins published %.3f, shed %.3f" % (
            c, bs - bp, max(lp[x] for x in w), max(ls[x] for x in w), aim.margins(lp), aim.margins(ls)))


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    t = args[0] if args else TARGET
    if "--ladder" in sys.argv:
        ladder(t)
    else:
        main(t)
