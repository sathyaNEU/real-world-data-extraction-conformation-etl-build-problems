"""task246 pair measurement on the cut pack. The cracker lands the call and handles the household exports the way the
dictionary and the protocol say: the version 4 codes on every row, the last visit's outcome, the deaths away from home
and the births module's newborns counted, each member once, under-fives by the age unit. The mirror stops at a wrong
rung on the call and takes the household asks by the path that keeps it the most figures among the cracker's and three
lazier ones. Every ask figure is scored against the golden at its rounding (response to one decimal, death rates to
two). The mirror's share of the call's per-zone criteria is measured too (the notes it gets right, the zones' own
figures it lands inside the accepted range). Prints the cracker sheet, the mirror's leakage and the pair ceiling;
--ladder prints the design note's ladder figures.

    python3 task246/generator/pair.py [target]
    python3 task246/generator/pair.py --ladder [target]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build as B
import estim as E
import params as P
import solve

TARGET = os.path.join(os.path.dirname(HERE), "target")


def ask_paths(target):
    F = B.FILES
    v4r = solve.response(target, F, codes="v4")
    return {
        # the cracker: the dictionary's version 4 codes on every row, every documented handling right
        "cracker": (v4r, solve.mortality(target, F, codes="v4")),
        # lazier paths: deaths only where the status says died; no births module; members not deduplicated
        "deaths_by_status": (v4r, solve.mortality(target, F, codes="v4", away=False)),
        "no_births_module": (v4r, solve.mortality(target, F, codes="v4", births_module=False)),
        "no_dedupe": (v4r, solve.mortality(target, F, codes="v4", dedupe=False)),
    }


def score(target, paths):
    F = B.FILES
    gr, gm = solve.response(target, F), solve.mortality(target, F)
    n = 3 * len(P.ZCODES)
    keep = {}
    for k, (r, m) in paths.items():
        hits = ["resp " + z for z in P.ZCODES if round(r[z], 1) == round(gr[z], 1)] + \
               ["cdr " + z for z in P.ZCODES if round(m[z][0], 2) == round(gm[z][0], 2)] + \
               ["u5dr " + z for z in P.ZCODES if round(m[z][1], 2) == round(gm[z][1], 2)]
        keep[k] = len(hits) / n
        print("%-18s keeps %2d of %d ask figures %s" % (k, len(hits), n, hits))
    return keep


def mirror_on_call(target):
    """the share of the call's per-zone criteria a response stopping at each wrong rung keeps"""
    A = solve.answer(target, B.FILES)
    ZF, gold = A["ZF"], A["noted"]
    best = (None, 0.0)
    for k in ["R0_repeat", "R1_field", "R1_mse", "R2_offset_repeat", "R5_offset_mse"]:
        mnote = E.noted(ZF, k)
        right = sum((z in mnote) == (z in gold) for z in P.ZCODES)
        inside = sum(round(A["lo"][z], 1) <= round(ZF[z][k], 1) <= round(A["hi"][z], 1) for z in P.ZCODES)
        share = (right + inside) / 24.0
        print("mirror at %-17s notes %s; %2d of 12 notes right, %2d of 12 own figures inside the accepted range" % (
            k, mnote, right, inside))
        if share > best[1]:
            best = (k, share)
    return best


def main(target=TARGET):
    keep = score(target, ask_paths(target))
    rung, share = mirror_on_call(target)
    r_miss = round(38 * 0.75 * share, 1)
    print("the best wrong rung on the call: %s, keeping %.1f of the 38 recommendation points" % (rung, r_miss))
    lc = keep["cracker"]
    ls = max(keep.values())
    c, s = 38 + 7 + 55 * lc, r_miss + 7 + 55 * ls
    print("Pair ceiling: %.1f" % ((c + s) / 2))
    print("Mirror leakage: %.1f per cent of ask weight" % (100 * ls))
    return (c + s) / 2, 100 * ls


def ladder(target=TARGET):
    """the design note's ladder: each rung's measurement points per zone and its noted set"""
    A = solve.answer(target, B.FILES)
    ZF = A["ZF"]
    keys = ["R0_repeat", "R1_field", "R1_mse", "R2_offset_repeat", E.REFERENCE, "R5_offset_mse"]
    print("%-18s %s" % ("", " ".join("%5s" % z for z in P.ZCODES)))
    for k in keys:
        print("%-18s %s  %s" % (k, " ".join("%5.1f" % E.points(ZF[z], k) for z in P.ZCODES), E.noted(ZF, k)))
    for z in P.ZCODES:
        Z = ZF[z]
        print("%-3s readings %5.2f  own %5.2f (variants %5.2f to %5.2f)  points %4.1f (variants %4.1f to %4.1f)" % (
            z, Z["readings"], Z[E.REFERENCE], A["lo"][z], A["hi"][z], E.points(Z, E.REFERENCE),
            min(E.points(Z, k) for k in E.VARIANTS), max(E.points(Z, k) for k in E.VARIANTS)))


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    t = args[0] if args else TARGET
    if "--ladder" in sys.argv:
        ladder(t)
    else:
        main(t)
