#!/usr/bin/env python3
"""The ask sheet's pair arithmetic for task204, measured on the cut pack.

Stage 2 carried a design-time model with the per-ask shares assumed. This file now measures them:
`checks.cracker_sheet()` runs the careful solver's path for each ask against the shipped pack and
reports how many of that ask's graded figures the path lands. Nothing here is a reader, a probe or a
scored read (CLAUDE.md's STOP block); it is arithmetic over a measured miss rate, and the portal is
the only measurement of stump power.

    python3 task204/generator/ceiling.py
"""
import json
import os

import checks as C

HERE = os.path.dirname(os.path.abspath(__file__))

# Rubric weights, per cent of the whole response (CLAUDE.md, Current spec).
W_RECOMMENDATION = 36.0
W_INSTRUCTION = 7.0
W_ASKS = 57.0

# What a response banks on the recommendation side (stumping Part 0).
ON_CALL = 45.0
OFF_CALL = 12.0

# The one device a response is most likely to catch on its own, because the careful path's own
# output contradicts itself: dividing by every calendar day in the window puts four of the fourteen
# capture shares above one hundred per cent, which is visible without reading any convention.
SELF_EVIDENT = "B"


def main():
    rows = C.cracker_sheet()
    figures = sum(total for _, _, total, _ in rows)
    per_figure = W_ASKS / figures
    hits = {name: hit for name, hit, _, _ in rows}
    totals = {name: total for name, _, total, _ in rows}

    ask_b = sum(hits[k] for k in hits) * per_figure
    ask_a = sum(totals[k] if k == SELF_EVIDENT else hits[k] for k in hits) * per_figure
    ins_a, ins_b = 0.85 * W_INSTRUCTION, 0.80 * W_INSTRUCTION

    off_a = OFF_CALL + ask_a + ins_a
    off_b = OFF_CALL + ask_b + ins_b
    pair_off = (off_a + off_b) / 2.0
    on_a = ON_CALL + ask_a + ins_a
    on_b = ON_CALL + ask_b + ins_b
    pair_on = (on_a + on_b) / 2.0
    pair_split = (on_a + off_b) / 2.0
    mirror = 100.0 * ask_a / W_ASKS

    print("task204 ask sheet, measured on the cut pack")
    print("  graded ask figures            %d over %d asks" % (figures, len(rows)))
    print("  weight per ask figure         %.4f per cent" % per_figure)
    for name, hit, total, note in rows:
        print("  ask %s  %3d figures  the careful path lands %3d (%.0f per cent)   %s"
              % (name, total, hit, 100.0 * hit / total, note))
    print("  response A, the stronger      asks %.1f of %.1f" % (ask_a, W_ASKS))
    print("  response B                    asks %.1f of %.1f" % (ask_b, W_ASKS))
    print("  PAIR CEILING, both off the call   %.1f per cent (built to 60, bar 70)" % pair_off)
    print("  sensitivity, one on the call      %.1f per cent" % pair_split)
    print("  sensitivity, both on the call     %.1f per cent" % pair_on)
    print("  MIRROR LEAKAGE                %.1f per cent of ask weight (ceiling 50)" % mirror)
    print("  each of the top two keeps     %.0f and %.0f per cent of the ask weight (ceiling 40)"
          % (100.0 * ask_a / W_ASKS, 100.0 * ask_b / W_ASKS))
    out = {"figures": figures, "per_figure": round(per_figure, 4),
           "cracker": {name: [hit, total] for name, hit, total, _ in rows},
           "pair_off_call": round(pair_off, 1), "pair_split": round(pair_split, 1),
           "pair_on_call": round(pair_on, 1), "mirror_leakage_pct": round(mirror, 1)}
    with open(os.path.join(HERE, "ceiling.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
        fh.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
