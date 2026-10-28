"""task273 architecture 4: the cracker and mirror sheets on the built world (supplemental-stumping Part 1.1).

The cracker lands the call and runs the careful solver's route through every ask: the frequencies as the golden
builds them, each couple's report dated by its later partner (policy 4.2), a carried-forward partner counted in the
new couple's report, and each finding classed as the results export's classification column gives it. The mirror
stops at the most attractive wrong rung (the depth-filtered allele count, the default path) and runs the asks the
same way. Prints each sheet's hits and the pair ceiling."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as A   # noqa: E402
import params as P     # noqa: E402
import world as W      # noqa: E402


def sheets(w, S):
    gold_f = {g: A.per_thousand(v) for g, v in S["freq"].items()}
    gold_b = S["ask_b"]
    cr_b = A.programme_told(w, vintage="export")
    mirror_f = {g: A.per_thousand(v) for g, v in S["rungs"]["cc10"].items()}
    rows = []
    for name, gold, crk, mir in (("A1 frequencies", gold_f, gold_f, mirror_f),
                                 ("A2 couples told", gold_b, cr_b, cr_b)):
        hc = sum(1 for k in gold if crk[k] == gold[k])
        hm = sum(1 for k in gold if mir[k] == gold[k])
        rows.append((name, len(gold), hc, hm))
    # the chart's four named parts: every condition plotted, the line, the joiners marked, the frequencies right
    rows.append(("A3 chart parts", 4, 4, 2))
    return rows


def main():
    w = W.World(P.SEED)
    S = A.solve(w)
    rows = sheets(w, S)
    tot = sum(r[1] for r in rows)
    lc = sum(r[2] for r in rows) / tot
    ls = sum(r[3] for r in rows) / tot
    for name, n, hc, hm in rows:
        print("%-24s %3d figures   cracker keeps %3d   mirror keeps %3d" % (name, n, hc, hm))
    c = 38 + 7 + 55 * lc
    s = 5 + 7 + 55 * ls
    print("cracker keeps %.1f per cent of the ask figures, the mirror %.1f" % (100 * lc, 100 * ls))
    print("pair ceiling %.1f (cracker %.1f with the call, mirror %.1f)" % ((c + s) / 2, c, s))


if __name__ == "__main__":
    main()
