"""task176 cracker and mirror on the cut pack (python3 cracker.py <target>), Part 0's weights: a response on the call
banks 38 for the call and its components and 7 for instructions, the asks carry 55 over their 30 figures; a response
off the call keeps 5 of the 38.

The cracker lands the call and runs the hygiene battery on both asks: it keeps the SFCC and LFCC lines, drops voided
remittances, keeps the 2026 service days and sums care_days (ask A); it sees the remittance amount repeated on every
child line and takes one amount per remittance number (ask B), and the script also scores the other keys a careful
de-duplicator reaches for (number and run date, number and provider, number and amount, number and county office,
provider and amount). The mirror stops at the tenure rung (300), sums care_days and sums the amount on every line.
One crack at a time shows what each device is worth."""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc           # noqa: E402
import common as C    # noqa: E402


def score(figs, a, b):
    slug = {r: "R%d_%s" % (r, C.REGIONS[r].split()[-1]) for r in C.REGIONS}
    hit = 0
    for r in C.REGIONS:
        g = figs["a_" + slug[r]]
        hit += (a.get((r, 1)) == g["H1"]) + (a.get((r, 2)) == g["H2"])
        g = figs["b_" + slug[r]]
        hit += sum(int(round(b.get((r, q), 0))) == g["Q%d" % q] for q in (1, 2, 3, 4))
    return hit


def main(target):
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    n = 30.0

    def pair(c_keep, m_keep):
        c = 38 + 7 + 55 * c_keep / n
        m = 5 + 7 + 55 * m_keep / n
        return c, m, (c + m) / 2
    a_sum = calc.ask_child_days(target, union=False)
    a_uni = calc.ask_child_days(target)
    keys = ("number", "number_run", "number_provider", "number_amount", "number_county", "provider_amount")
    b_alt = {k: calc.ask_money(target, key=k) for k in keys}
    b_lines = calc.ask_money(target, key="lines")
    b_gold = calc.ask_money(target)
    worst = max(score(figs, a_sum, b_alt[k]) for k in keys)
    mk = score(figs, a_sum, b_lines)
    c, m, p = pair(worst, mk)
    print("cracker keeps %d of 30 ask figures on its best de-duplication key (score %.1f); mirror keeps %d (score %.1f); "
          "pair %.1f" % (worst, c, mk, m, p))
    for k in keys:
        print("  ask B taken as one remittance per %-16s keeps %d of 20" % (k, score(figs, {}, b_alt[k])))
    print("mirror leakage: %.1f per cent of ask weight" % (100 * mk / n))
    for name, (a, b) in (("A cracked (each child-day once)", (a_uni, b_alt["number"])),
                         ("B cracked (number, run date and county office)", (a_sum, b_gold)),
                         ("both cracked", (a_uni, b_gold))):
        k = score(figs, a, b)
        print("  %-48s keeps %2d, pair %.1f" % (name, k, pair(k, mk)[2]))
    return 0 if p <= 40 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")))
