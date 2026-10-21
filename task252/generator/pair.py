"""The ask ladder on the cut pack: each complete pipeline a careful solver could run for the return's items (b) and
(c), scored plant by plant against the golden; the cracker (the call landed, the natural route on each ask) and the
mirror (the default call, the same routes); the pair ceiling from the rubric arithmetic (supplemental-stumping
Part 0)."""
import os
import sys

import params as P
import solve as S


def routes(target):
    D = S.load(target); L = S.lims(target)
    out = {}
    out["b: the analyser's stamps as given (rounds 1 and 2, three of four readers)"] = S.ask_a(target, L, shift_h=0)
    out["b: stamps as given, one row per point and collection time (the round 3 readers' bottle rule)"] = S.ask_a(
        target, L, shift_h=0, dedup="point_time")
    out["b: stamps before reception moved to reception, the rest as given"] = S.ask_a(target, L, shift_h=0,
                                                                                       fix_early=True)
    out["b: stamps as given, raw samples included"] = S.ask_a(target, L, shift_h=0, scope=("raw", "fil", "fin"))
    out["b: stamps as given, the register's codes only"] = S.ask_a(target, L, shift_h=0, current_codes_only=True)
    out["b: stamps read as UTC"] = S.ask_a(target, L, shift_h=13)
    out["b: the hour added, raw samples included"] = S.ask_a(target, L, scope=("raw", "fil", "fin"))
    out["b: the hour added, the register's codes only"] = S.ask_a(target, L, current_codes_only=True)
    out["b: the hour added, every row a sample"] = S.ask_a(target, L, dedup="none")
    out["b: the hour added, one row per point and collection time (rounds 3's readers, with the hour)"] = S.ask_a(
        target, L, dedup="point_time")
    out["b: the hour added, rows equal but for the number dropped"] = S.ask_a(target, L, dedup="content")
    out["c: unfilled runs a check followed as the analyser's faults, the rest the telemetry's (round 3, both "
        "readers)"] = S.ask_b(target, D, "checked")
    out["c: unfilled runs at every port the telemetry's, checks aside"] = S.ask_b(target, D, "allport")
    out["c: F rows with nothing filled back as the analyser's faults (stage 4 rounds 1 and 2, all four readers)"] = (
        S.ask_b(target, D, "faults"))
    out["c: gaps in the historian's G rows, two-hour hold"] = S.ask_b(target, D, "historian")
    out["c: every F row a gap, the lost hours not, two-hour hold"] = S.ask_b(target, D, "allF")
    out["c: the PLC's gaps summed whole, no hold"] = S.ask_b(target, D, "nohold")
    return out, S.ask_a(target, L), S.ask_b(target, D)


def score(r, g):
    return sum(abs(r[c] - g[c]) < 0.05 for c in P.CODES)


def main(target, quiet=False):
    R, ga, gb = routes(target)
    best = {"b": 0, "c": 0}
    for k, r in R.items():
        g = ga if k.startswith("b") else gb
        s = score(r, g)
        best[k[0]] = max(best[k[0]], s)
        if not quiet:
            print("%-60s %d of 8" % (k, s))
    crack = best["b"] + best["c"]
    Lc = crack / 16.0
    C = 38 + 7 + 55 * Lc
    Sm = 5 + 7 + 55 * Lc
    ceiling = (C + Sm) / 2
    if not quiet:
        print("cracker keeps %d of 16; mirror the same; pair ceiling %.1f ((%.1f + %.1f) / 2)" % (crack, ceiling, C, Sm))
    return dict(cracker=crack, ceiling=ceiling, C=C, S=Sm)


if __name__ == "__main__":
    t = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                                           "target")
    main(t)
