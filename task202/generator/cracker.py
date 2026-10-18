"""The cracker and mirror sheets, measured on the cut pack rather than argued on paper.

The cracker is the response that LANDS the call, runs the hygiene battery and executes every filed
rule it points at; the mirror is the best response that stops at a wrong rung. Each ask figure is
scored a hit when it falls within half a unit of the rounding the asking sentence states. The pair is
computed on Part 0's weights (38 recommendation and components, 7 instruction-following, 55 asks) so
the figure is comparable with other builds, with r = 5 for the recommendation weight a wrong call keeps.

    python3 task202/generator/cracker.py
"""
import json
import os
import sys

import numpy as np

import build as B
import params as P
import records as RC
import sim
import solve
import writeup as WU

W_REC, W_INSTR, W_ASK, R_KEEP = 38.0, 7.0, 55.0, 5.0

# the asking sentences' own units: the prompt states ceilings in pesos to the nearest PHP 100, each
# share to one decimal place and each scale factor to three decimals
ASKS = [("A1 band ceilings", "ceiling", 100.0),
        ("A2 referred share of awards", "referred_share", 0.1),
        ("A3 referred share of award value", "referred_value_share", 0.1),
        ("A4 scale factor applied", "factor", 0.001)]
CONTENT = ["D1 workbook carries the schedule", "D2 board paper draws the distribution and the ceilings"]


def answers(mean, cnt, shape):
    """What a response filing ceiling C reports for every graded figure, on its own distribution."""
    C = solve.lowest(lambda x: solve.share_cells(x, mean, cnt, shape))
    F = solve.figures_for(C, {"mean": mean, "cnt": cnt, "shape": shape})
    out = {"call": C, "bands": {}}
    for b in P.BANDS:
        d = F["bands"][b]
        out["bands"][b] = {"ceiling": d["ceiling"], "referred_share": d["referred_share"],
                           "referred_value_share": d["referred_value_share"], "factor": d["factor"]}
    return out


def score(resp, gold):
    """Per ask, the figures this response keeps."""
    rows = []
    for label, key, unit in ASKS:
        hits = 0
        for b in P.BANDS:
            if abs(resp["bands"][b][key] - gold["bands"][b][key]) <= unit / 2.0:
                hits += 1
        rows.append((label, hits, len(P.BANDS)))
    # the two content criteria are free: any response that produces the named files earns them
    for c in CONTENT:
        rows.append((c, 1, 1))
    return rows


def pair(cracker_rows, mirror_rows):
    kept = lambda rows: sum(h for _, h, _ in rows) / float(sum(n for _, _, n in rows))
    Lc, Lm = kept(cracker_rows), kept(mirror_rows)
    C = W_REC + W_INSTR + W_ASK * Lc
    S = R_KEEP + W_INSTR + W_ASK * Lm
    return Lc, Lm, C, S, (C + S) / 2.0


def main():
    W = sim.make()
    mean, cnt, shape = W["mean"], W["cnt"], W["shape"]
    gold = answers(mean, cnt, shape)
    print("golden call PHP %s" % "{:,}".format(gold["call"]))

    cracker = gold                                     # the cracker lands the call
    crows = score(cracker, gold)
    print("\nCRACKER: lands the call, executes clause 4.2, 9.2 and 9.3 and schedule B, runs the battery")
    for label, h, n in crows:
        print("   %-46s keeps %d of %d" % (label, h, n))

    # the mirror: every response that stops at a wrong rung, scored on its own reading
    cands = {}
    cv = float(shape.std(ddof=1) / shape.mean())
    cands["rung 1, the partner-band averages (the default path)"] = answers(mean, cnt, np.array([1.0]))
    cands["rung 5a, a lognormal at the portal's CV"] = answers(mean, cnt, solve.quantiles_lognormal(cv))
    cands["rung 5b, a gamma at the portal's CV"] = answers(mean, cnt, solve.quantiles_gamma(cv))
    sh27 = np.array([a["amount"] / mean[(a["partner"], a["band"])] for a in W["por"]
                     if (a["partner"], a["band"]) in mean], float)
    cands["the shape over the portal's whole 27 months"] = answers(mean, cnt, sh27 / sh27.mean())
    best = None
    print("\nMIRRORS: each stops at a wrong rung and reports its own figures")
    for lab, resp in cands.items():
        rows = score(resp, gold)
        k = sum(h for _, h, _ in rows)
        n = sum(n for _, _, n in rows)
        print("   %-52s call PHP %-7s keeps %2d of %d" % (lab, "{:,}".format(resp["call"]), k, n))
        for label, h, nn in rows:
            if h:
                print("        keeps %d of %d on %s" % (h, nn, label))
        if best is None or k > best[1]:
            best = (lab, k, rows)
    mrows = best[2]
    Lc, Lm, C, S, pr = pair(crows, mrows)
    print("\nthe best miss is %s, keeping %d of %d ask criteria" % (best[0], best[1],
                                                                    sum(n for _, _, n in mrows)))
    print("\nPAIR on Part 0's weights (%.0f recommendation and components, %.0f instruction, %.0f asks, r = %.0f)"
          % (W_REC, W_INSTR, W_ASK, R_KEEP))
    print("   cracker keeps %.3f of the ask weight -> %.1f" % (Lc, C))
    print("   mirror  keeps %.3f of the ask weight -> %.1f" % (Lm, S))
    print("   PAIR CEILING %.1f   (bar 50, build to 40)" % pr)
    print("   MIRROR LEAKAGE %.1f per cent of ask weight (bar under 35)" % (100 * Lm))

    # solve the target keep count with the script rather than on paper
    print("\nwhat the pair would be at each cracker keep count, with this mirror held:")
    n_ask = sum(n for _, _, n in crows)
    for keep in range(0, n_ask + 1, 2):
        c = W_REC + W_INSTR + W_ASK * keep / n_ask
        print("   cracker keeps %2d of %d -> pair %.1f%s" % (keep, n_ask, (c + S) / 2.0,
                                                             "   <= 40" if (c + S) / 2.0 <= 40 else ""))
    print("\nthe cracker keeps a figure whenever it lands the call, because every graded figure in the")
    print("prompt is the call's own construction over the call's own population: supplemental-stumping")
    print("Part 2.1's corollary says no device can sit under such an ask, and this is the measurement.")
    return pr, 100 * Lm


if __name__ == "__main__":
    main()
