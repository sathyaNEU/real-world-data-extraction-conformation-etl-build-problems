"""The ask layer measured on the built records: the cracker lands the call and keeps every graded figure (the seven
counts and the seven layer losses both follow the construction); the mirror is the path both stage 4 readers took,
one curve over the pooled record with the deductible truncation and the retention censoring, and keeps whatever of
its counts and layer losses meet the golden at the graded rounding. Prints the pair ceiling.

    python3 task255/generator/pair.py"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import analysis as A   # noqa: E402
import world as W      # noqa: E402


def graded(counts, layer):
    out = {}
    for a in W.OPTIONS:
        out["count.%d" % a] = round(counts[a], 1)
        out["layer.%d" % a] = int(round(layer[a] / 1e5))
    return out


def main():
    st = A.world_state()
    lad = A.ladder(st["rec"])
    gold = graded(lad["G"]["counts"], lad["G"]["layer"])
    rows = []
    for k in ("R3", "shift", "G_closed"):
        alt = graded(lad[k]["counts"], lad[k]["layer"])
        hits = [x for x in gold if alt[x] == gold[x]]
        rows.append((k, len(hits)))
        print("%-9s keeps %d of %d graded ask figures" % (k, len(hits), len(gold)))
    keep_m = max(h for _, h in rows) / len(gold)
    C = 38 + 7 + 55 * 1.0
    S = 5 + 7 + 55 * keep_m
    print("Pair ceiling: %.1f ((%.1f + %.1f) / 2); mirror leakage %.1f per cent of ask weight" % ((C + S) / 2, C, S,
                                                                                               100 * keep_m))


if __name__ == "__main__":
    main()
