"""task176 ask pricing on the cut pack (python3 ceiling.py <target>), on supplemental-stumping Part 0's weights: a
response on the call banks 38 for the call and its components and 7 for instructions, the asks carry 55 over their 22
figures (child-days statewide by half, 2; money by region and quarter of the payment run, 20); a response off the call
keeps 5 of the 38.

Every ask figure is scored on the cut pack under each route, a hit only when the route's figure equals the golden at
the asked rounding. The routes are the six readers' verbatim paths (round 1 scored-task176a and scored-task176b, round 2
scored-task176c and scored-task176d, round 3 scored-task176e and scored-task176f, reader_method.md), each with the call landed and off it, and every other grouping
a careful de-duplicator reaches for on the money ask:
  reader A   PAID SFCC and LFCC lines, weekdays in 2026, each child and day once; money one amount per
             (pay_run_date, provider_no), PAID, 2026 runs, quarter of the run date
  reader B   the same filters; care_days summed over the lines (the dual-provider child at each home), which the
             prompt's "counting a child once on a day" now closes, so B is priced both verbatim and with the clause read;
             money one amount per (pay_run_date, provider_no)
  reader C   PAID FCC lines, distinct (child_no, day); money one amount per (county, run date, remittance_no) "since the
             amount repeats per line and covers multi-home payees", region from the issuing county (round 2)
  reader D   the same child-days; money one amount per (county, run date, remittance_no), region by the county of the
             remittance (round 2)
  reader E   (round 3) the same child-days; money one amount per (remittance_no, pay_run_date, provider_no), region
             from the licence county
  reader F   (round 3) the same child-days; money one amount per pay run and provider, region from the licence county
Readers A and B also took the region from county_fips. Every other key is scored with the home's region.
The mirror stops at the tenure rung (300), sums care_days and sums the amount on every line.
Pair = (landed response + the best response off the call) / 2, gate 40."""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc           # noqa: E402
import common as C    # noqa: E402

N = 22.0


def score(figs, a, b):
    slug = {r: "R%d_%s" % (r, C.REGIONS[r].split()[-1]) for r in C.REGIONS}
    hit = (a.get(1) == figs["a_statewide"]["H1"]) + (a.get(2) == figs["a_statewide"]["H2"])
    for r in C.REGIONS:
        g = figs["b_" + slug[r]]
        hit += sum(int(round(b.get((r, q), 0))) == g["Q%d" % q] for q in (1, 2, 3, 4))
    return int(hit)


def landed(k):
    return 38 + 7 + 55 * k / N


def missed(k):
    return 5 + 7 + 55 * k / N


def main(target):
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    a_once = calc.ask_child_days(target)
    a_sum = calc.ask_child_days(target, union=False)
    keys = ["lines"] + [k for k in calc.MONEY_KEYS if k != "remittance"]
    b = {k: calc.ask_money(target, key=k) for k in keys}
    b_gold = calc.ask_money(target)
    b_office = calc.ask_money(target, region="office")
    b_office_rp = calc.ask_money(target, key="run_provider", region="office")
    routes = {
        "reader A verbatim": (a_once, b_office_rp),
        "reader B verbatim": (a_sum, b_office_rp),
        "reader B with the clause read": (a_once, b_office_rp),
        "home region, multi-region remittances by care_days": (a_once, calc.ask_money(target, alloc="days")),
        "home region, multi-region remittances to the first line": (a_once, calc.ask_money(target, alloc="first")),
        "home region, every line priced at the full rate": (a_once, calc.ask_money_priced(target)),
        "reader C verbatim": (a_once, b_office),
        "reader D verbatim": (a_once, b_office),
        "reader E verbatim": (a_once, b["number_run_provider"]),
        "reader F verbatim": (a_once, b["run_provider"]),
        "mirror": (a_sum, calc.ask_money(target, key="lines", region="office")),
    }
    for k in keys:
        routes["once a day, money per %s" % k] = (a_once, b[k])
    kept = {name: score(figs, *v) for name, v in routes.items()}
    print("%-44s %5s %8s %8s" % ("route", "kept", "landed", "missed"))
    for name, k in kept.items():
        print("%-44s %2d/22 %8.1f %8.1f" % (name, k, landed(k), missed(k)))
    worst = max(kept.values())
    readers = ("reader A verbatim", "reader B with the clause read", "reader C verbatim", "reader D verbatim",
               "reader E verbatim", "reader F verbatim")
    off = max(kept[r] for r in readers)
    pair = (landed(worst) + missed(off)) / 2
    print("worst route keeps %d of 22: landed %.1f; best reader off the call %.1f; pair %.1f" %
          (worst, landed(worst), missed(off), pair))
    print("both readers as filed (off the call): %.1f and %.1f, pair %.1f" %
          (missed(kept["reader A verbatim"]), missed(kept["reader B verbatim"]),
           (missed(kept["reader A verbatim"]) + missed(kept["reader B verbatim"])) / 2))
    print("mirror leakage: %.1f per cent of ask weight" % (100 * kept["mirror"] / N))
    k = score(figs, a_once, b_gold)
    print("money cracked (number, run date and county office, home region, lines' pay): keeps %d, landed %.1f, pair %.1f" %
          (k, landed(k), (landed(k) + missed(off)) / 2))
    return 0 if pair <= 40 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")))
