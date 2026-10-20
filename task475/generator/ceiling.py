"""The ask layer measured on the cut pack: the cracker (lands the call, runs the hygiene battery, executes every filed
rule it points at) and the mirror (stops at the most attractive wrong rung) priced against generator/figures.json.

    python3 task475/generator/ceiling.py [target]

Weights 38 / 7 / 55: the call 10, the fourteen allocations 2 each (28); instructions 7; the 28 ask figures 55 / 28
each. A figure is kept when it prints in the golden's cell at the ask's rounding."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import bundle as B    # noqa: E402

TASK = os.path.dirname(HERE)
ASK_W = 55.0 / 28


def kept(golden, got, nm):
    return sum(int(round(got[c])) == golden[nm[c]] for c in got)


def main(target=None):
    target = target or os.path.join(TASK, "target")
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    ga, gb = fig["a_dwellings"], fig["b_spending"]
    nm = B.names(target)
    a_routes = {r: B.dwellings(target, r) for r in B.A_ROUTES}
    b_routes = {r: B.spending(target, r) for r in B.B_ROUTES}
    print("Ask A, dwellings weatherized in program year 2025; golden", ga)
    for k, v in a_routes.items():
        print("  %-16s keeps %2d of 14" % (k, kept(ga, v, nm)))
    print("Ask B, spending on dwellings in program year 2025; golden", gb)
    for k, v in b_routes.items():
        print("  %-16s keeps %2d of 14" % (k, kept(gb, v, nm)))
    # the cracker, on the stage 4 readers' measured paths: first completions from the history, the job records'
    # funding codes, units, the dwelling's tract; old numbers read through the conversion notes on lines posted
    # before the move
    ca, cb = kept(ga, a_routes["label"], nm), kept(gb, b_routes["posted_cutoff"], nm)
    C = 38 + 7 + ASK_W * (ca + cb)
    # the mirror: the best response off the call (the statewide share), its asks handled the cracker's way
    best_main = 0.0
    for route in ("R0", "R1", "R1b", "R1c"):
        al = B.allocations(target, route)
        main_ = 2 * sum(int(round(al[c] / 100.0)) * 100 == fig["components"]["allocations"][nm[c]] for c in al)
        main_ += 10 * ((", ".join(nm[c] for c in B.capped(al)) or "none") == fig["call"]["capped"])
        best_main = max(best_main, main_)
    S = max(best_main, 5.0) + 7 + ASK_W * (ca + cb)
    print()
    print("cracker: call landed (38), instructions (7), ask figures kept %d of 28 (A %d, B %d): %.1f" % (
        ca + cb, ca, cb, C))
    print("mirror: main block %.1f, ask figures kept %d of 28: %.1f" % (max(best_main, 5.0), ca + cb, S))
    print("Mirror leakage: %.1f per cent of ask weight" % (100.0 * (ca + cb) / 28))
    print("Pair ceiling: %.1f" % ((C + S) / 2))
    return (C + S) / 2


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
