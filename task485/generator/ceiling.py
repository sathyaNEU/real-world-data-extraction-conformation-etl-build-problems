"""The ask layer's pair ceiling on the cut pack (supplemental-stumping Part 0 and 1.1): the cracker lands the call,
runs the hygiene battery, executes every filed rule it points at and reads Electra's 2021 report as the register it is
labelled (each property's TOTAL less its attainers and overseas electors, as the field guide says); the mirror stops
off the call and reads the same report the same way. The ask reads no row the call reads, so the two rows share their
ask reading by construction (checks.py, separation); each half-handled stop is scored beside them.

    python3 task485/generator/ceiling.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
T = os.path.join(os.path.dirname(HERE), "target")
sys.path.insert(0, HERE)
import golden as G  # noqa: E402


def keep(gold, other):
    return sum(1 for k, v in gold.items() if other.get(k) == v)


def main():
    L = G.load(T)
    A = G.ask_a(T, L["wards"])
    stops = {r: keep(A, G.ask_a(T, L["wards"], r)) for r in ("export", "total", "adds_only", "all_rows", "all_notices", "no_k")}
    n = len(A)
    print("ask A, each ward's local government electors on the register published 1 December 2021: %d figures" % n)
    print("  the 2021 report as labelled, TOTAL less attainers and overseas (the cracker)          keeps %2d" % stops["export"])
    print("  the 2021 report's TOTAL as the electors (the mirror's careless twin)                   keeps %2d" % stops["total"])
    print("  the 2022 notices' additions taken off, their deletions not put back                    keeps %2d" % stops["adds_only"])
    print("  every 2022 notice row backed out, attainers and overseas electors with the rest        keeps %2d" % stops["all_rows"])
    print("  every notice of 2021 and 2022 backed out                                               keeps %2d" % stops["all_notices"])
    print("  the 2022 notices backed out without the local-only electors                            keeps %2d" % stops["no_k"])
    crack = mirror = stops["export"]
    lc, lm = crack / n, mirror / n
    c = 38 + 7 + 55 * lc
    s = 5 + 7 + 55 * lm
    print("cracker keeps %d of %d ask figures (%.1f per cent), scores %.1f with the call" % (crack, n, 100 * lc, c))
    print("mirror keeps %d of %d (%.1f per cent), scores %.1f off it" % (mirror, n, 100 * lm, s))
    best = max(stops.values())
    print("the best half-handled response keeps %d of %d (%.1f per cent)" % (best, n, 100 * best / n))
    print("Pair ceiling: %.1f" % ((c + s) / 2))
    print("Mirror leakage: %.1f per cent of ask weight" % (100 * lm))
    return dict(crack=crack, mirror=mirror, n=n, pair=(c + s) / 2, partial=best, stops=stops)


if __name__ == "__main__":
    main()
