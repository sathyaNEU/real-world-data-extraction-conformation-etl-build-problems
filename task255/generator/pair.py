"""The ask layer measured on the built pack: the cracker is loop 1's portal-proven path (each member's declared total
once, the largest where a member declared twice, every member that declared; one vehicle per latest number added
under the member that added it), run on the generator's own records; the mirror stops at the pooled curve and prices
the same way. Prints each ask figure's hit or miss and the pair ceiling.

    python3 task255/generator/pair.py"""
import collections
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import analysis as A   # noqa: E402
import world as W      # noqa: E402

CLASSES = ("city", "fire district", "water-sewer district", "port district", "transit authority",
           "park and recreation district", "library district")


def figures_by(toe, units, kind):
    T, U = sum(toe.values()), sum(units.values())
    out = {}
    for a in W.OPTIONS:
        out["premium.%d" % a] = round(A.premium(T, U, a))
    for k in CLASSES:
        out["toe_000.%s" % k] = round(sum(v for m, v in toe.items() if kind[m] == k) / 1000)
        out["units.%s" % k] = sum(v for m, v in units.items() if kind[m] == k)
    return out


def main():
    st = A.world_state()
    mem, dec, log = st["mem"], st["dec"], st["log"]
    kind = {m["no"]: m["kind"] for m in mem}
    leaving = {m["no"] for m in mem if m.get("withdraws")}
    gold = figures_by({k: d["toe"] for k, d in W.rated(dec, mem).items()},
                      A.scheduled_units(log, leaving=leaving), kind)
    by = collections.defaultdict(list)
    for d in dec:
        by[d["member"]].append(d["toe"])
    crack = figures_by({m: max(v) for m, v in by.items()}, A.units_naive(log, mode="add_member"), kind)
    hits = [k for k in gold if crack[k] == gold[k]]
    _, _, _, cg = A.golden(st["rec"])
    lad = A.ladder(st["rec"])
    counts_gold = {a: round(cg[a], 1) for a in W.OPTIONS}
    counts_mirror = {a: round(lad["R3"]["counts"][a], 1) for a in W.OPTIONS}
    n_ask = len(gold) + len(W.OPTIONS)
    keep_c = (len(hits) + len(W.OPTIONS)) / n_ask          # the cracker lands the call and its seven counts
    keep_m = (len(hits) + sum(counts_mirror[a] == counts_gold[a] for a in W.OPTIONS)) / n_ask
    C = 38 + 7 + 55 * keep_c
    S = 5 + 7 + 55 * keep_m
    for k in gold:
        print("%-36s golden %-14s cracker %-14s %s" % (k, gold[k], crack[k], "hit" if k in hits else "miss"))
    print("ask figures %d; cracker keeps %d priced figures and the 7 counts (%.1f per cent); mirror keeps %.1f per cent"
          % (n_ask, len(hits), 100 * keep_c, 100 * keep_m))
    print("Pair ceiling: %.1f ((%.1f + %.1f) / 2); mirror leakage %.1f per cent of ask weight" % ((C + S) / 2, C, S,
                                                                                               100 * keep_m))


if __name__ == "__main__":
    main()
