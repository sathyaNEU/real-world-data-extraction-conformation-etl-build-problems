"""The cracker and the mirror, scored on the asks.

The cracker lands the call, runs the hygiene battery (key uniqueness, exact duplicates, unmatched joins, fan-out),
executes every filed rule and documented convention (the funding clause with the declared times, Crestfield's UTC
converted, Inland Seas' payroll date read as the day a shift ends, the roster's keys) and counts Crestfield's billing
lines as shifts. The mirror stops at the most attractive wrong rung of the asks: the census night's level for the whole
day, the payroll date read as the date a shift started, the billing lines counted. Each is scored figure by figure
against the golden (a hit is an exact whole shift) on the house weights: 38 for the call and its components, 7 for
instruction-following, 55 for the asks. The chart is graded on its two labelled figures; the chart file itself is an
instruction-following point, so no chart part is free.

    python3 cracker.py [pack]     score on the cut pack (target/ by default)"""
from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

CHART_FIGURES = 2        # the busiest week's funded total and the shifts billed to the pool that week
FREE_PARTS = 0           # chart parts a response gets without the device work
W_CALL, W_IF, W_ASK, R_MISS = 38.0, 7.0, 55.0, 5.0


def pair(kept_cracker, kept_mirror, n_ask):
    c = W_CALL + W_IF + W_ASK * kept_cracker / n_ask
    s = R_MISS + W_IF + W_ASK * kept_mirror / n_ask
    return c, s, (c + s) / 2


def report(rows, gold_f, gold_b, gold_chart, south, quiet=False):
    n_ask = 2 * len(south) + CHART_FIGURES + FREE_PARTS
    out = {}
    for name, (f, b, ch) in rows.items():
        hf = sum(1 for fid in south if f[fid] == gold_f[fid])
        hb = sum(1 for fid in south if b[fid] == gold_b[fid])
        hc = sum(1 for x, y in zip(ch, gold_chart) if x == y)
        out[name] = (hf, hb, hc, hf + hb + hc + FREE_PARTS)
        if not quiet:
            print("%-34s funded %2d/%d  billed-not-funded %2d/%d  chart %d/%d  kept %2d of %d" % (
                name, hf, len(south), hb, len(south), hc, CHART_FIGURES, hf + hb + hc + FREE_PARTS, n_ask))
    c, s, p = pair(out["cracker"][3], out["mirror"][3], n_ask)
    c2, s2, p2 = pair(out["cracker, A2 cracked"][3], out["mirror"][3], n_ask)
    both = c
    leak = 100.0 * out["mirror"][3] / n_ask
    if not quiet:
        print("pair ceiling %.1f (cracker %.1f, mirror %.1f); both top responses on the call %.1f; with A2 cracked %.1f"
              % (p, c, s, both, p2))
        print("mirror leakage %.1f per cent of ask weight" % leak)
    return out, p, p2, both, leak


def pack_mode(pack=None, quiet=False):
    import pack_read as P
    return P.cracker_report(report, pack, quiet)


if __name__ == "__main__":
    pack_mode(next((a for a in sys.argv[1:] if not a.startswith("--")), None))
