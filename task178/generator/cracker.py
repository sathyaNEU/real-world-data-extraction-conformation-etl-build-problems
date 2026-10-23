"""task178 cracker and mirror, run on the cut pack: the pair ceiling and the mirror's leakage on Part 0's weights (38
recommendation and components, 7 instruction-following, 55 asks; a wrong call keeps about 5).

The cracker lands the call and executes every filed rule and the hygiene battery: the release note's report of record,
ANULADA and CANCELLED rows removed, UTC put on local time, euro and Treasury deals and cancelled deals dropped. It does
not decide which records are one event: each platform execution is read as an order, and each live forward deal as
an amount falling due. The mirror is the best response off the call (the default path, priced at 8) with the same
ask handling.

    python3 task178/generator/cracker.py task178/target"""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc  # noqa: E402
import common as C  # noqa: E402


def main(target):
    task = os.path.dirname(os.path.abspath(target))
    figs = json.load(open(os.path.join(task, "generator", "figures.json")))
    golden = {}
    for q in range(1, 5):
        for b in C.SIZE_BANDS:
            golden["A Q%d %s" % (q, b[0])] = figs["ask_a_hedging_cost_tqp_per_usd"]["Q%d" % q][b[0]]
        golden["B Q%d exporters" % q] = figs["ask_b_forwards_due_2027_usd_mn"]["Q%d" % q]["exporters_sell"]
        golden["B Q%d importers" % q] = figs["ask_b_forwards_due_2027_usd_mn"]["Q%d" % q]["importers_buy"]
    a, _ = calc.ask_a(target, grouping="fill")
    s, b, _, _ = calc.ask_b(target, net_windows=False)
    resp = {}
    for q in range(1, 5):
        for band in C.SIZE_BANDS:
            v = a.get((q, band[0]))
            resp["A Q%d %s" % (q, band[0])] = None if v is None else round(v, 1)
        resp["B Q%d exporters" % q] = round(s[q], 1)
        resp["B Q%d importers" % q] = round(b[q], 1)
    hits = 0
    print("%-22s %10s %10s  %s" % ("figure", "golden", "cracker", "verdict"))
    for k, gv in golden.items():
        hit = resp[k] is not None and abs(resp[k] - gv) < 0.05 + 1e-9
        hits += hit
        print("%-22s %10s %10s  %s" % (k, gv, resp[k], "HIT" if hit else "miss"))
    n = len(golden)
    call = calc.call(target)
    cracker_call = call["setting"] == figs["call"]["pricing_volatility_pct"]
    mirror_setting = __import__("math").ceil(call["vol_ols_net"])
    crack = 38 * cracker_call + 7 + 55 * hits / n
    mirror = 5 + 7 + 55 * hits / n
    print("\ncracker: call %s, asks %d of %d -> %.1f" % ("landed" if cracker_call else "missed", hits, n, crack))
    print("mirror: call at %d (missed), asks %d of %d -> %.1f" % (mirror_setting, hits, n, mirror))
    print("asks are decoupled: both responses take the same ask path, because no ask consumes the call's construction "
          "(separation asserted in checks.py)")
    print("pair ceiling %.1f; mirror leakage %.1f per cent of ask weight" % ((crack + mirror) / 2, 100.0 * hits / n))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
