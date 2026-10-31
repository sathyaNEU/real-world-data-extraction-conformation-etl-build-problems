"""The ask layer measured on a cut pack: each response's figures on both asks against the golden, cell by cell, and the
pair arithmetic (supplemental-stumping Part 0: the landed call scores 38 + 7 + 55 Lc, the best miss 5 + 7 + 55 Ls).

  the cracker       lands the call, runs the hygiene battery (scale 2's grams read, its January block re-dated by
                    the label numbers, reversals netted), executes every filed rule (deal versions and dates) and
                    reads every helper; counts every printed label and every saving line
  the mirror        stops at the duplication table on members (Nordhavn) and handles the asks as far as their
                    first device: card payments matched to labels without the counter lines on the tills; the
                    service desk's adjustments counted on their own receipt's date
  the full includer every device it can find handled, the silent half left: labels matched to card payments and
                    till lines with scale 2's block left where its clock put it; one multibuy per adjustment line

    python3 task268/generator/ceiling.py [target_dir]"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as A   # noqa: E402

ROWS = (("the cracker", "every_fixed", "savings"), ("the mirror", "cardonly", "adj_own_date"),
        ("the full includer", "noclock", "adj_one"))


def measure(target):
    G = A.Golden(target)
    ga, gb = G.ask_a(), G.ask_b()
    out = []
    for name, ma, mb in ROWS:
        a, b = G.ask_a(ma), G.ask_b(mb)
        ka = sum(1 for k in ga if abs(round(a[k], 1) - round(ga[k], 1)) < 0.05)
        kb = sum(1 for k in gb if round(b[k]) == round(gb[k]))
        out.append((name, ka, len(ga), kb, len(gb)))
    n = len(ga) + len(gb)
    Lc = (out[0][1] + out[0][3]) / n
    Ls = max(out[1][1] + out[1][3], out[2][1] + out[2][3]) / n
    return dict(rows=out, Lc=Lc, Ls=Ls, pair=((38 + 7 + 55 * Lc) + (5 + 7 + 55 * Ls)) / 2, leak=100 * Ls)


if __name__ == "__main__":
    tgt = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")
    M = measure(tgt)
    for name, ka, na, kb, nb in M["rows"]:
        print("%-18s ask A keeps %2d of %d   ask B keeps %2d of %d" % (name, ka, na, kb, nb))
    print("cracker keeps %.1f per cent of the ask figures; best miss keeps %.1f per cent; pair ceiling %.1f"
          % (100 * M["Lc"], M["leak"], M["pair"]))
