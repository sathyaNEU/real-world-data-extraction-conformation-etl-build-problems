"""The ask sheet's measurement on the cut pack: the cracker (lands the call, executes every filed convention, runs the
two asks the careful way: Ask A every line summed where the files date it with each credit on its own date, Ask B the
delivery rows as listed) and the mirror (the default path's R1, the pooled 2025 share on the eight weeks scaled to the
window's working days, the same asks), scored figure by figure on the 38 / 7 / 55 planning weights against the golden
recomputed from the same pack.

    python3 task153/generator/pair.py [<target dir>]

Main block (38): the six yard counts, the total and the saving, each a criterion of equal weight (a route off the
total books another saving). Instruction-following (7): kept by both paths. Asks (55) over 23 criteria: Ask A's nine
account-months, Ask B's six months of gallons and six of dollars, and the chart's two series (each yard's island
draw, the card gallons of the eight weeks).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import asks as AS    # noqa: E402
import calc as CA    # noqa: E402

REC, IF, ASK = 38.0, 7.0, 55.0


def counts(d):
    return {y: CA.floor_loads(d[y]) for y in CA.YARDS}


def main_hits(route, gold):
    c, g = counts(route), counts(gold)
    hits = sum(c[y] == g[y] for y in CA.YARDS)
    same_total = sum(c.values()) == sum(g.values())
    hits += 2 if same_total and c == g else (1 if same_total else 0)
    return hits, len(CA.YARDS) + 2


def ask_hits(a, b, gold_a, gold_b, draw_series_right, card_series_right):
    n = sum(round(a[k]) == round(v) for k, v in gold_a.items())
    n += sum(round(b[k][0]) == round(v[0]) for k, v in gold_b.items())
    n += sum(round(b[k][1]) == round(v[1]) for k, v in gold_b.items())
    n += int(draw_series_right) + int(card_series_right)
    return n, len(gold_a) + 2 * len(gold_b) + 2


def score(mh, mt, ah, at):
    return REC * mh / mt + IF + ASK * ah / at


def run(target):
    P = CA.read(target)
    G = CA.golden(P)
    R, _ = CA.rungs(P, G["draw"])
    gold = G["draw"]
    mirror = R["R1a pooled 2025 share x 40/39"]
    gold_a, gold_b = AS.ask_a(P), AS.ask_b(target)
    crack_a, crack_b = AS.ask_a(P, "golden", "netted"), AS.ask_b(target, "per_drop")
    card8 = CA.card_by_yard(P, *CA.BASE)
    card_right = card8 == R["R0 card gallons, trailing eight weeks"]

    cm, mt = main_hits(gold, gold)
    ca, at = ask_hits(crack_a, crack_b, gold_a, gold_b, True, card_right)
    mm, _ = main_hits(mirror, gold)
    ma, _ = ask_hits(crack_a, crack_b, gold_a, gold_b, False, card_right)
    crack, mir = score(cm, mt, ca, at), score(mm, mt, ma, at)
    print("cracker: main %d of %d criteria, asks %d of %d, score %.1f" % (cm, mt, ca, at, crack))
    print("mirror:  main %d of %d criteria, asks %d of %d, score %.1f" % (mm, mt, ma, at, mir))
    print("mirror leakage: %.1f per cent of ask weight" % (100.0 * ma / at))
    print("pair ceiling: %.1f" % ((crack + mir) / 2))
    return crack, mir


if __name__ == "__main__":
    run(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target"))
