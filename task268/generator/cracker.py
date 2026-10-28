"""The ask layer measured on a cut pack: the cracker (lands the call, runs the hygiene battery, executes every filed rule
it points at) and the mirror (stops at the most attractive wrong rung) against the golden, cell by cell; the pair
ceiling and the mirror leakage from the pair arithmetic (supplemental-stumping Part 0).

    python3 task268/generator/cracker.py [target_dir]"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as A   # noqa: E402
import common as K     # noqa: E402


def measure(target):
    G = A.Golden(target)
    gold = {"A": G.ask_a()}
    # the cracker: the in-force file read as it stands (cover and risk district on the row)
    crack = {"A": G.ask_a(apply_changes=False)}
    # the mirror: every address and cover change in the log applied in processing order, whatever its effective date
    mirror = {"A": G.ask_a(apply_changes=True, effective_only=False)}
    rows, kc, km, n = [], 0, 0, 0
    for ask in ("A",):
        for cell, g in gold[ask].items():
            cr, m = crack[ask][cell], mirror[ask][cell]
            hc, hm = abs(cr - g) < 0.5, abs(m - g) < 0.5
            kc += hc
            km += hm
            n += 1
            rows.append((ask, cell, g, cr, m, hc, hm))
    Lc, Ls = kc / n, km / n
    C = 38 + 7 + 55 * Lc
    S = 5 + 7 + 55 * Ls
    return dict(rows=rows, Lc=Lc, Ls=Ls, pair=(C + S) / 2, leak=100 * Ls, n=n)


if __name__ == "__main__":
    tgt = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")
    M = measure(tgt)
    for ask, cell, g, c, m, hc, hm in M["rows"]:
        print("%s %-8s %-13s golden %6d  cracker %6d (%s)  mirror %6d (%s)" % (
            ask, cell[0], cell[1], g, c, "hit" if hc else "miss", m, "hit" if hm else "miss"))
    print("cracker keeps %.1f per cent, mirror keeps %.1f per cent of %d ask figures; pair ceiling %.1f"
          % (100 * M["Lc"], M["leak"], M["n"], M["pair"]))
