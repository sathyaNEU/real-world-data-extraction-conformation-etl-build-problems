"""The pair ceiling on the cut pack. The cracker lands the call and reads the shootings the way both round-1 readers did:
the rows struck in an assault and marked inside the city, the people the Medical Examiner's list shows died of the
wound taken out on the date, block, age and sex as the log holds them, each person once by report number, time, age
and sex, a shooting as the people struck at one block and minute; the mirror stops at the per-line conversion (each
Return A line at its own October to December rate) and reads the shootings the same way. Weights 38 / 7 / 55: the
change 20, the restated 2024 total 10, the 2025 count 8; each of the 24 shooting figures 55/24. The sensitivity lines
add one find at a time: the records system's clock, the township blocks, both.

    python3 task481/generator/ceiling.py     exit 0 at 40 or under
"""
import os
import sys

import methods as M
import pack as P

W_CHANGE, W_RESTATED, W_2025, W_INSTR, W_ASK = 20.0, 10.0, 8.0, 7.0, 55.0 / 24
HERE = os.path.dirname(os.path.abspath(__file__))
CAREFUL = {"township": False, "clock": False}
LADDER = [("+ the records system's UTC shot times", {"township": False}),
          ("+ the township blocks", {"clock": False}),
          ("+ both (the golden)", {})]


def keep(gvr, me, kw, gv, gs):
    v, s = M.shootings(gvr, me, **kw)
    return sum(v[q] == gv[q] for q in M.QUARTERS) + sum(s[q] == gs[q] for q in M.QUARTERS)


def main(target=None, quiet=False):
    target = target or os.path.join(os.path.dirname(HERE), "target")
    f = lambda k: os.path.join(target, P.FILES[k])
    rows = M.read_csv(f("extract"))
    ra = {}
    for y in (2021, 2022, 2023, 2024):
        ra.update(M.read_return_a(f("ra_%d" % y)))
    dvu = M.read_csv(f("dvu"))
    lad = M.ladder(rows, ra, dvu)
    g = round(100 * lad["golden"])
    mirror_call = (W_CHANGE * (round(100 * lad["per_line"]) == g) + W_RESTATED * (
        round(lad["per_line_2024"], -2) == round(lad["golden_2024"], -2)) + W_2025)
    gvr, me = M.read_csv(f("gvr")), M.read_csv(f("me"))
    gv, gs = M.shootings(gvr, me)
    base = keep(gvr, me, CAREFUL, gv, gs)
    cracker = W_CHANGE + W_RESTATED + W_2025 + W_INSTR + W_ASK * base
    mirror = mirror_call + W_INSTR + W_ASK * base
    pair = (cracker + mirror) / 2
    if not quiet:
        print("the mirror (per-line conversion) keeps %.0f of the 38 call-side points" % mirror_call)
        print("the careful shootings reading keeps %d of 24 ask figures" % base)
        print("cracker %.2f, mirror %.2f, pair ceiling %.1f, mirror leakage %.1f per cent of ask weight" % (
            cracker, mirror, pair, 100.0 * base / 24))
        for lab, kw in LADDER:
            k = keep(gvr, me, kw, gv, gs)
            c2 = W_CHANGE + W_RESTATED + W_2025 + W_INSTR + W_ASK * k
            m2 = mirror_call + W_INSTR + W_ASK * k
            print("sensitivity %s: keeps %d of 24; cracker %.1f, pair %.1f with the mirror reading carefully, "
                  "%.1f with both finding it" % (lab, k, c2, (c2 + mirror) / 2, (c2 + m2) / 2))
    return pair


if __name__ == "__main__":
    sys.exit(0 if main() <= 40.0 else 1)
