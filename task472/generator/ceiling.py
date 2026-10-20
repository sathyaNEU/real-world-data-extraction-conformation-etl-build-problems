"""The ask layer measured on the cut pack: the cracker (lands the call, runs the hygiene battery, executes every filed
rule it points at) and the mirror (stops at the most attractive wrong rung) priced against generator/figures.json.

    python3 task472/generator/ceiling.py [target]

Weights 38 / 7 / 55: the call 10, the six terminal figures 3 each, the runner-up 4 and the lead 6 (38); instructions
7; the twelve ask figures 55 / 12 each. A figure is kept when it prints in the golden's cell at the ask's rounding."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import bundle as B    # noqa: E402

TASK = os.path.dirname(HERE)
ASK_W = 55.0 / 12


def kept(golden, got):
    return sum(int(round(got[t])) == golden[B.NAME[t]] for t in B.TERMS)


def main(target=None):
    target = target or os.path.join(TASK, "target")
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    ga, gb = fig["a_breakdown_hours"], fig["b_labor_hours"]
    a_routes = {r: B.breakdown_hours(target, r) for r in ("per_order", "state", "current", "order_spans", "code",
                                                          "both_counted")}
    b_routes = {r: B.labor_hours(target, r) for r in ("exact_match", "override", "all_timesheets", "ledger_only",
                                                      "current", "both_counted", "with_yard")}
    print("Ask A, breakdown hours out of service (whole hours); golden", ga)
    for k, v in a_routes.items():
        print("  %-15s keeps %d of 6  %s" % (k, kept(ga, v), {B.NAME[t]: round(v[t], 1) for t in B.TERMS}))
    print("Ask B, maintenance labor hours (whole hours); golden", gb)
    for k, v in b_routes.items():
        print("  %-15s keeps %d of 6  %s" % (k, kept(gb, v), {B.NAME[t]: round(v[t], 1) for t in B.TERMS}))
    # the cracker, as the stage 4 reader who kept every ask figure on the pack before this one worked: each crane at
    # the terminal of its working hours, February's copies once, BD at the pull, the status history paired order by
    # order and added up; a timesheet day dropped where a CONTRACT line on its order has its day and hours
    ca, cb = kept(ga, a_routes["per_order"]), kept(gb, b_routes["exact_match"])
    C = 38 + 7 + ASK_W * (ca + cb)
    # the mirror: the best response off the call, the asks handled the cracker's way
    best, best_main, best_route = None, -1.0, None
    for route in ("naive", "tide_zero", "gated_zero", "waited_zero"):
        t = B.totals(target, route)
        rk = B.ranking(t)
        if rk[0] == "MRW":
            continue
        main_ = 0.0
        main_ += 4 * (B.NAME[rk[1]] == fig["components"]["runner_up"])
        main_ += 3 * sum(int(round(t[x])) == fig["components"]["berth_hours_saved"][B.NAME[x]] for x in B.TERMS)
        main_ += 6 * (int(round(t[rk[0]])) - int(round(t[rk[1]])) == fig["components"]["gap_hours"])
        if main_ > best_main:
            best, best_main, best_route = rk, main_, route
    # the mirror's asks as the other reader handled them: the register's terminal, the timesheets over the ledger
    sa, sb = kept(ga, a_routes["current"]), kept(gb, b_routes["override"])
    S = max(best_main, 5.0) + 7 + ASK_W * (sa + sb)
    print()
    print("cracker: call landed (38), instructions (7), ask figures kept %d of 12 (A %d, B %d): %.1f" % (
        ca + cb, ca, cb, C))
    print("mirror (%s, names %s): main block %.1f, ask figures kept %d of 12: %.1f" % (
        best_route, B.NAME[best[0]], max(best_main, 5.0), sa + sb, S))
    print("Mirror leakage: %.1f per cent of ask weight" % (100.0 * (sa + sb) / 12))
    print("Pair ceiling: %.1f" % ((C + S) / 2))
    return (C + S) / 2


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
