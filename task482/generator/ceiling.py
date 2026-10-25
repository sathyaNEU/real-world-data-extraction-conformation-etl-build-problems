"""The ask layer's pair ceiling on the cut pack (supplemental-stumping Part 0 and 1.1): the cracker lands the call, runs
the hygiene battery, executes every filed rule it points at and reads every rate against the schedules (each visit at
the level whose rate its line's allowed amount equals, Merrinlake's halved visits found: round 1's reader A); the
mirror stops off the call and reads each visit at the code on its claim. Each is scored figure by figure against the golden at the asks' rounding,
on its own readings, with the half-handled stops measured beside them.

    python3 task482/generator/ceiling.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
T = os.path.join(os.path.dirname(HERE), "target")
sys.path.insert(0, HERE)
import golden as G  # noqa: E402


def keep(gold, other, tol):
    return sum(1 for k, v in gold.items() if k in other and abs(other[k] - v) < tol)


def main():
    p = G.load(T)
    A = G.ask_a(p)
    a = {r: keep(A, G.ask_a(p, rule=r), 0.05) for r in ("line_mlh", "code", "line", "halve_all", "claim_only")}
    n = len(A)
    print("ask A, level 5 paid share by practice: %d figures" % n)
    print("  each line at its rate, Merrinlake's halved visits found (the cracker)            keeps %2d" % a["line_mlh"])
    print("  the code on the claim (the mirror)                                                keeps %2d" % a["code"])
    print("  each line at the level its own allowed amount equals                              keeps %2d" % a["line"])
    print("  every Merrinlake modifier 25 visit read at twice its line's allowed amount        keeps %2d" % a["halve_all"])
    print("  each claim at the level its allowed amount equals, Merrinlake's halving unseen    keeps %2d" % a["claim_only"])
    crack, mirror = a["line_mlh"], a["code"]
    lc, lm = crack / n, mirror / n
    c = 38 + 7 + 55 * lc
    s = 5 + 7 + 55 * lm
    print("cracker keeps %d of %d ask figures (%.1f per cent), scores %.1f with the call" % (crack, n, 100 * lc, c))
    print("mirror keeps %d of %d (%.1f per cent), scores %.1f off it" % (mirror, n, 100 * lm, s))
    best = max(a.values())
    print("the best half-handled response keeps %d of %d (%.1f per cent)" % (best, n, 100 * best / n))
    print("Pair ceiling: %.1f" % ((c + s) / 2))
    print("Mirror leakage: %.1f per cent of ask weight" % (100 * lm))
    return dict(crack=crack, mirror=mirror, n=n, pair=(c + s) / 2, partial=best, a=a)


if __name__ == "__main__":
    main()
