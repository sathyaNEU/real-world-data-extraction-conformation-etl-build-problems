"""Pair ceiling and mirror leakage, scored on the cut pack (target/ and golden/).

The cracker lands the call and handles every ask the careful way the pack invites: it runs the hygiene battery,
reads every document, takes each counter's equipment change on the date the site list and the operations log give
for it, and joins the detector channels to the asset register (keeping or dropping the days before the logged
renewal, whichever keeps more). The mirror stops on the call at the textbook expansion from the permanent counters
and handles the asks the same way. Each ask figure is kept when it rounds to the golden figure. Weights: 38 for the
recommendation and critical components (the call 0.4 of it, the per-section figures 0.6), 7 for instructions, 55 for
the asks split evenly over their figures.

    python3 task484/generator/ceiling.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as C     # noqa: E402
import est             # noqa: E402
import golden as GO    # noqa: E402


def main():
    tgt = os.path.join(C.TASK, "target")
    G = GO.compute(tgt)
    R = G["R"]
    # ask A: the careful reading takes the switch on each counter's installation date
    instA = R["askA"]["install"]
    keptA = [c["site"] for c in G["counters"] if GO.r10(instA[c["site"]]) == c["hgv"]]
    curA = R["askA"]["current"]
    keptA_naive = [c["site"] for c in G["counters"] if GO.r10(curA[c["site"]]) == c["hgv"]]
    # ask B: the register join, keeping or dropping the pre-renewal days
    reg, post = R["askB"]["register"], R["askB"]["post"]
    keptB_reg = [a for a in G["approaches"] if GO.rthou(reg[(a["junction"], a["approach"])]) == a["thousands"]]
    keptB_post = [a for a in G["approaches"] if GO.rthou(post[(a["junction"], a["approach"])]) == a["thousands"]]
    keptB = max(len(keptB_reg), len(keptB_post))
    nA, nB = len(G["counters"]), len(G["approaches"])
    w = 55.0 / (nA + nB)
    kept = max(len(keptA), len(keptA_naive)) + keptB
    Lc = kept * w / 55.0
    Ls = Lc
    # the mirror's main side: the per-section figures it shares with the golden
    same = sum(1 for s in G["sections"] if round(s["default"], 1) == s["annual"] and (s["default"] > 3.0) == s["over"])
    r = 38 * 0.6 * same / len(G["sections"])
    Cc = 38 + 7 + 55 * Lc
    Sm = r + 7 + 55 * Ls
    pair = (Cc + Sm) / 2
    print("ask A kept by the careful reading: %d of %d (install date), %d (current table)" % (len(keptA), nA, len(keptA_naive)))
    print("ask B kept: %d of %d (register join), %d (pre-renewal days dropped)" % (len(keptB_reg), nB, len(keptB_post)))
    print("cracker keeps %.1f per cent of the ask weight; mirror leakage %.1f per cent" % (100 * Lc, 100 * Ls))
    print("mirror's main side: %d of %d section figures shared, r = %.1f" % (same, len(G["sections"]), r))
    print("cracker %.1f, mirror %.1f, pair ceiling %.1f" % (Cc, Sm, pair))
    return 0 if pair <= 60 and 100 * Ls < 50 else 1


if __name__ == "__main__":
    sys.exit(main())
