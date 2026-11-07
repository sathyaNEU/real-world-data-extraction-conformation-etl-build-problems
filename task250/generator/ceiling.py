"""The cracker and the mirror, run as code on the cut pack (supplemental-stumping 1.1 and Part 5).

The cracker lands the call, runs the hygiene battery (near-exact duplicates on parcel, event, courier, handheld and
minute; the latest version of a pre-advice; the replaced depot code; piece labels and the cut references matched by
prefix and counted), executes every filed rule and matches the pickups the ask names. The mirror stops at the most
attractive wrong rung of the call (the sort plan's hub) and at the natural reads of the asks (same parcel, event and
handheld on the day; any match on a piece label or a reference). Each ask figure is a hit when it equals the golden.

    python3 ceiling.py [target]      prints the sheet, the pair ceiling and the mirror leakage, with the pack digest
"""
import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build as B
import golden as GD
import rungs as R

TASK = os.path.dirname(HERE)


def digest(target):
    h = hashlib.sha256()
    for f in sorted(os.listdir(target)):
        h.update(f.encode())
        h.update(open(os.path.join(target, f), "rb").read())
    return h.hexdigest()[:16]


def main(target=None):
    target = target or os.path.join(TASK, "target")
    d = GD.load(target, B.FILES)
    deps = list(d["depots"]["depot_code"])
    A, Bk = R.ask_rungs(d)
    M, arr, sh, gold = R.main_rungs(d)
    sheet = {
        "cracker": {"A": A["A1 near-exact, same minute"], "B": Bk["B3 pieces and references counted, pickups only"]},
        "mirror": {"A": A["A2 same parcel, event, handheld and day"],
                   "B": Bk["B2 piece labels and reference prefixes, any match"]},
    }
    n_ask = 2 * len(deps)
    keep = {}
    print("pack digest", digest(target))
    for who, s in sheet.items():
        hits = 0
        for ask, gk in (("A", A["golden"]), ("B", Bk["golden"])):
            h = [c for c in deps if s[ask].get(c, 0) == gk.get(c, 0)]
            hits += len(h)
            print("%-8s ask %s: %2d of %d figures kept %s" % (who, ask, len(h), len(deps), h))
        keep[who] = hits / n_ask
    # the call's own components: the hub rows each route gets right (parcels, missed, rate and verdict per hub)
    g = M["golden"]
    plan = M["R0 plan"]
    mirror_hub = 0
    for h in g:
        mirror_hub += sum(1 for k in ("parcels", "missed") if plan[h][k] == g[h][k])
        mirror_hub += round(plan[h]["rate"], 2) == round(g[h]["rate"], 2)
        mirror_hub += (plan[h]["rate"] > GD.TOLERANCE) == (g[h]["rate"] > GD.TOLERANCE)
    n_hub = 4 * len(g)
    lc, ls = keep["cracker"], keep["mirror"]
    C = 38 + 7 + 55 * lc
    S = 5 + 7 + 55 * ls
    print("cracker keeps %.3f of the ask weight, mirror %.3f" % (lc, ls))
    print("pair ceiling %.1f (C = 38 + 7 + 55 x %.2f = %.1f; S = 5 + 7 + 55 x %.2f = %.1f)" % ((C + S) / 2, lc, C, ls, S))
    # sensitivity: the hub rows counted inside the ask weight, the mirror keeping the rows the plan route gets right
    lc2 = (n_hub + keep["cracker"] * n_ask) / (n_hub + n_ask)
    ls2 = (mirror_hub + keep["mirror"] * n_ask) / (n_hub + n_ask)
    C2, S2 = 38 + 7 + 55 * lc2, 5 + 7 + 55 * ls2
    print("with the hub rows as asks: cracker %.3f, mirror %.3f (%d of %d hub rows), pair %.1f" %
          (lc2, ls2, mirror_hub, n_hub, (C2 + S2) / 2))
    print("mirror leakage %.1f per cent of ask weight (%.1f with the hub rows)" % (100 * ls, 100 * ls2))
    return {"pair": (C + S) / 2, "pair_hub_rows": (C2 + S2) / 2, "mirror": 100 * ls, "mirror_hub_rows": 100 * ls2,
            "cracker": lc, "digest": digest(target)}


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
