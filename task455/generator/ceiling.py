"""The ask layer measured on the cut pack: the cracker (lands the call, runs the battery, executes every filed rule
it points at) and the mirror (the strong analyst's wrong rung, the new account's share) priced against
generator/figures.json.

    python3 task455/generator/ceiling.py [target]

Weights 38 / 7 / 55: the call side 38 (the designation, the runner-up and gap, and the seven counties' 2026 births,
set-aside accounts and rates), instructions 7, the ask layer 55. Inside the ask layer the 28 figures of Asks A and B
(each county's 2025 births, birth rate, deaths and death rate) carry 46.75 and the account list and the chart's
layout 8.25 (15 per cent). A figure is kept when it prints in the golden's cell at the ask's rounding. A response
off the call keeps 5 of the call side (the chart, the account list's columns, Eskwell)."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import methods as M   # noqa: E402
import world as W     # noqa: E402

TASK = os.path.dirname(HERE)
CALL, INSTR, ASKS = 38.0, 7.0, 55.0
FIG_W = ASKS * 0.85 / 28
LAYOUT = ASKS * 0.15
OFF_CALL = 5.0


def kept(fig, a, b):
    n = 0
    for code, name in W.NAME.items():
        g = fig["y2025"][name]
        n += a["births"].get(code, 0) == g["births"]
        n += round(a["rates"][code], 1) == g["birth_rate"]
        n += b["deaths"].get(code, 0) == g["deaths"]
        n += round(b["rates"][code], 1) == g["death_rate"]
    return n


def main(target=None):
    target = target or os.path.join(TASK, "target")
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    B = M.Bundle(target)
    gold = sorted(fig["designated"])

    def on_call(cls):
        rates, _ = B.rates(cls, B.base(M.QS.index((2025, 4))))
        top = sorted(W.NAME[c] for c in sorted(rates, key=lambda c: -rates[c])[:3])
        return top == gold, top

    paths = {
        "cracker": (B.classify(2026, stop="quarter"), B.ask_a(stop="quarter"), B.ask_b(mode="new_keyed"), True),
        "mirror (rung 2)": (B.classify(2026, rule="S", stop="quarter"), B.ask_a(rule="S", stop="quarter"),
                            B.ask_b(mode="S"), False),
    }
    scores = []
    for label, (cls, a, b, layout) in paths.items():
        landed, top = on_call(cls)
        k = kept(fig, a, b)
        s = (CALL if landed else OFF_CALL) + INSTR + k * FIG_W + (LAYOUT if layout else 0.0)
        ask_share = (k * FIG_W + (LAYOUT if layout else 0.0)) / ASKS
        scores.append(s)
        print("%-16s call %-5s (%s)  ask figures kept %2d of 28  ask share %4.1f%%  score %5.1f"
              % (label, landed, ", ".join(top), k, 100 * ask_share, s))
    print("pair ceiling %.1f" % (sum(scores) / 2))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
