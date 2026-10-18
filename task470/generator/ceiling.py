"""The pair ceiling, measured on the cut pack (supplemental-stumping Part 0): the cracker lands the call, runs the
hygiene battery (every event's address resolves, no key repeats in MASTER, no fan-out the current register leaves
open) and executes every documented handling (UTC to Pacific time, tower hours with the winter hours and closed days,
civil columns, a touch-and-go two operations, cancelled registrations read for the addresses today's register no
longer lists); the mirror stops on the best-scoring wrong rung of the ladder. Weights 38 / 7 / 55: the main block's 38
split as the call 8 and each of the 24 fields' lead 1.25; the 55 over the towered fields' twelve figures (each
field's operations and lead). The ask reads the towered fields' events, which no rung changes, so every response's
ask row is scored on the ask path it takes.

    python3 task470/generator/ceiling.py [target]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import bundle as B      # noqa: E402
import methods as M     # noqa: E402
import world as W       # noqa: E402

TASK = os.path.dirname(HERE)


def main(target):
    P = B.Pack(target)
    gi = P.inventory()
    gold = B.qualifying(gi["lead"])
    gk = {l: round(gi["lead"][l]) for l in B.FIELDS}
    go = {l: round(gi["ops"][l] / 100.0) for l in W.TOWERED}

    def main_score(lead):
        call = B.qualifying(lead) == gold
        hits = sum(round(lead[l]) == gk[l] for l in W.UNTOWERED)
        return 8 * call + 1.25 * hits, call, hits

    def ask_score(inv):
        hits = sum((round(inv["lead"][l]) == gk[l]) + (round(inv["ops"][l] / 100.0) == go[l]) for l in W.TOWERED)
        return 55 * hits / 12.0, hits

    cracker = P.inventory(how="current")
    c_main, _, _ = main_score(gi["lead"])
    c_ask, c_hits = ask_score(cracker)
    C = c_main + 7 + c_ask
    print("cracker: call landed, main %.1f + instructions 7 + ask %.1f (%d of 12 figures) = %.1f" % (
        c_main, c_ask, c_hits, C))
    rungs, sets, par = M.rungs(P, gi)
    best = None
    for k, lead in rungs.items():
        if k.startswith("G"):
            continue
        m, call, hits = main_score(lead)
        a, ah = ask_score(cracker)
        S = m + 7 + a
        print("mirror on %-50s main %.1f (call %s, %2d of 24 leads) + 7 + ask %.1f (%d of 12) = %.1f" % (
            k, m, call, hits, a, ah, S))
        if best is None or S > best[0]:
            best = (S, k, ah)
    pair = (C + best[0]) / 2
    print("Pair ceiling: %.1f (cracker %.1f, best mirror %.1f on %s)" % (pair, C, best[0], best[1]))
    print("Mirror leakage: %.1f per cent of ask weight (%d of 12 figures)" % (100.0 * best[2] / 12, best[2]))
    for k, inv in (("today's register (the cracker)", cracker),
                   ("the register's history read by date (golden)", gi)):
        a, hits = ask_score(inv)
        print("ask stop %-50s %d of 12" % (k, hits))
    return pair


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(TASK, "target"))
