"""task176 ask pricing on the cut pack (python3 ceiling.py <target>), on supplemental-stumping Part 0's weights: a
response on the call banks 38 for the call and its components and 7 for instructions, the asks carry 55 over their 30
figures (three tables by region and half of 2026: subsidy money, food program meals and snacks, children in split
care; ten figures each, each table on its own device); a response off the call keeps 5 of the 38.

Every figure is scored on the cut pack, a hit only when the route's figure equals the golden at the asked rounding.
Money routes are the eight readers' verbatim paths (scored-task176a to scored-task176h, reader_method.md):
  A, B   one amount per run date and provider, region of county_fips (round 1)
  C, D   one amount per number, run date and county office, region of county_fips (round 2)
  E      one amount per number, run date and provider, region of the home (round 3)
  F, H   one amount per run date and provider, region of the home (rounds 3 and 4)
  G      one amount per number, run date and county office, shared by each line's pay, region of the home (round 4,
         the golden route)
No reader has met the meals or the split-care table; each reader is priced on the careful path for both (one claim per
sponsor, site and month at its latest filing; every child paid at two homes on the same days), and every other
reading is scored as its own route. The mirror stops at the tenure rung (300), sums every line's amount, every claim
and every overlap. A single crack is one device resolved and the other two not.
Pair = (the cracker, landed with no device resolved + the best response off the call) / 2, gate 40."""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc           # noqa: E402
import common as C    # noqa: E402

N = 30.0
CELLS = [(r, h) for r in C.REGIONS for h in (1, 2)]


def score(figs, b, m, s):
    slug = {r: "R%d_%s" % (r, C.REGIONS[r].split()[-1]) for r in C.REGIONS}
    hit = 0
    for r in C.REGIONS:
        for h in (1, 2):
            k = "H%d" % h
            hit += int(round(b.get((r, h), 0))) == figs["b_" + slug[r]][k]
            hit += m.get((r, h), 0) == figs["m_" + slug[r]][k]
            hit += s.get((r, h), 0) == figs["s_" + slug[r]][k]
    return int(hit)


def landed(k):
    return 38 + 7 + 55 * k / N


def missed(k):
    return 5 + 7 + 55 * k / N


def main(target):
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    gb, gm, gs = calc.ask_money(target), calc.ask_meals(target), calc.ask_split(target)
    mb = {
        "run and provider, office region (A, B)": calc.ask_money(target, key="run_provider", region="office"),
        "number, run and office, office region (C, D)": calc.ask_money(target, region="office"),
        "number, run and provider, home region (E)": calc.ask_money(target, key="number_run_provider"),
        "run and provider, home region (F, H)": calc.ask_money(target, key="run_provider"),
    }
    careful_m = calc.ask_meals(target, key="sponsor_site_month")
    careful_s = calc.ask_split(target, rule="overlap")
    routes = {}
    for name, b in mb.items():
        routes["readers %s" % name] = (b, careful_m, careful_s)
    routes["reader G (money cracked)"] = (gb, careful_m, careful_s)
    for k in calc.MEAL_KEYS:
        if k != "claim":
            routes["meals per %s" % k] = (mb["run and provider, home region (F, H)"], calc.ask_meals(target, key=k), careful_s)
    routes["meals summed over every row"] = (mb["run and provider, home region (F, H)"], calc.ask_meals(target, key="all"), careful_s)
    routes["meals at first filing"] = (mb["run and provider, home region (F, H)"], calc.ask_meals(target, latest=False), careful_s)
    routes["mirror"] = (calc.ask_money(target, key="lines", region="office"), calc.ask_meals(target, key="all"), careful_s)
    kept = {name: score(figs, *v) for name, v in routes.items()}
    print("%-58s %5s %8s %8s" % ("route", "kept", "landed", "missed"))
    for name, k in kept.items():
        print("%-58s %2d/30 %8.1f %8.1f" % (name, k, landed(k), missed(k)))
    cracks = {
        "money alone": score(figs, gb, careful_m, careful_s),
        "meals alone": score(figs, mb["run and provider, home region (F, H)"], gm, careful_s),
        "split care alone": score(figs, mb["run and provider, home region (F, H)"], careful_m, gs),
    }
    for name, k in cracks.items():
        print("single crack, %-16s keeps %2d: off the call %.1f, landed %.1f" % (name, k, missed(k), landed(k)))
    readers = [k for n, k in kept.items() if n.startswith("reader")]
    # the cracker resolves no device: reader G's money and the meals key (number, site), which takes a claim as its
    # number within a site and so resolves the sponsors' sequences, are cracks, scored above as routes
    cr = max(kept[n] for n in kept if not n.startswith("reader G") and n != "meals per number_site")
    off = max(readers)
    pair = (landed(cr) + missed(off)) / 2
    print("cracker (landed, no device resolved) keeps %d: %.1f; best reader off the call %.1f; pair %.1f" %
          (cr, landed(cr), missed(off), pair))
    print("two readers as filed, both off the call (G and the best other): %.1f" %
          ((missed(off) + missed(max(k for n, k in kept.items() if n.startswith("readers")))) / 2))
    print("mirror leakage: %.1f per cent of ask weight" % (100 * kept["mirror"] / N))
    k2 = score(figs, gb, gm, careful_s)
    print("two devices cracked (money and meals): keeps %d, off the call %.1f" % (k2, missed(k2)))
    ok = pair < 40 and all(missed(k) < 40 for k in cracks.values())
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")))
