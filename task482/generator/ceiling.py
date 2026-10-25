"""The ask layer's pair ceiling on the cut pack (supplemental-stumping Part 0 and 1.1): the cracker lands the call, runs
the hygiene battery and executes every filed rule it points at; the mirror stops on the default rung. Each is scored
figure by figure against the golden at the asks' rounding, with the partial handlings measured beside them.

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
    A, B = G.ask_a(p), G.ask_b(p)
    a_code = keep(A, G.ask_a(p, rule="code"), 0.05)
    a_rate = keep(A, G.ask_a(p, rule="rate"), 0.05)
    b_crack = keep(B, G.ask_b(p, pmh_by_period=True, keep_other_programs=True), 0.005)
    b_ref = keep(B, G.ask_b(p, keep_other_programs=True), 0.005)
    b_fee = keep(B, G.ask_b(p, pmh_by_period=True), 0.005)
    n = len(A) + len(B)
    print("ask A, level 5 paid share by practice: %d figures" % len(A))
    print("  the code on the claim (the cracker)                          keeps %2d" % a_code)
    print("  the full level-5 rate only                                   keeps %2d" % a_rate)
    print("ask B, care coordination fees by practice and coverage quarter: %d figures" % len(B))
    print("  every remittance line, Pemberglen by its period (the cracker) keeps %2d" % b_crack)
    print("  Pemberglen's coverage month from its reference, every line   keeps %2d" % b_ref)
    print("  the standard's fees only, Pemberglen by its period           keeps %2d" % b_fee)
    crack = a_code + b_crack
    mirror = a_code + b_crack           # the mirror reads both asks as the cracker does
    lc, lm = crack / n, mirror / n
    c = 38 + 7 + 55 * lc
    s = 5 + 7 + 55 * lm
    print("cracker keeps %d of %d ask figures (%.1f per cent), scores %.1f with the call" % (crack, n, 100 * lc, c))
    print("mirror keeps %d of %d (%.1f per cent), scores %.1f off it" % (mirror, n, 100 * lm, s))
    best_partial = max(a_rate, a_code) + max(b_ref, b_fee, b_crack)
    print("the best single-device handling keeps %d of %d (%.1f per cent)" % (best_partial, n, 100 * best_partial / n))
    print("Pair ceiling: %.1f" % ((c + s) / 2))
    print("Mirror leakage: %.1f per cent of ask weight" % (100 * lm))
    return dict(crack=crack, mirror=mirror, n=n, pair=(c + s) / 2, partial=best_partial)


if __name__ == "__main__":
    main()
