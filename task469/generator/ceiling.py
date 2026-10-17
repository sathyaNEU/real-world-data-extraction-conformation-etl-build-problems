"""The pair ceiling, measured on the cut pack (supplemental-stumping Part 0 and Part 7): the cracker lands the call,
runs the hygiene battery on the 2027 submissions (key uniqueness, exact duplicates, unmatched joins: none fire) and
executes every documented handling (time modes converted, the layout note's leg sequence for through stops, SFG-3's
same-day turn); the mirror stops on the best-scoring wrong rung of the ladder. Weights 38 / 7 / 55: the main block's
38 split as the call 8, each relationship's decision 2.5 and shortest ground time 2.5; the 55 over the schedule ask's
twelve figures. The asks consume nothing the call's construction produces (checks.py separation rows), so each
response's ask row is scored on the ask path it takes.

    python3 task469/generator/ceiling.py [target]
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
    reg = B.registers(target)
    pop = B.population(B.turns_2026(target, reg))
    fil = reg["filings"]
    gold = M.review(pop, fil, M.km)
    truth = B.ask_a(target, reg)

    def main_score(rv):
        call = all(rv[s]["send_back"] == gold[s]["send_back"] for s in W.ORDER)
        dec = sum(rv[s]["send_back"] == gold[s]["send_back"] for s in W.ORDER)
        sh = sum(rv[s]["shortest"] == gold[s]["shortest"] for s in W.ORDER)
        return 8 * call + 2.5 * dec + 2.5 * sh, call, dec, sh

    def ask_score(handling):
        r = B.ask_a(target, reg, **handling)
        hits = sum(r[s][j] == truth[s][j] for s in W.ORDER for j in (0, 1))
        return 55 * hits / 12.0, hits

    cracker_path = dict(dedup="none")          # every leg a key check passes; DEI meanings are not in the pack
    c_main, _, _, _ = main_score(gold)
    c_ask, c_hits = ask_score(cracker_path)
    C = c_main + 7 + c_ask
    print("cracker: call landed, main %.1f + instructions 7 + ask %.1f (%d of 12 figures) = %.1f" % (
        c_main, c_ask, c_hits, C))
    rungs = M.rung_verdicts(pop, fil)
    best = None
    for k, rv in rungs.items():
        m, call, dec, sh = main_score(rv)
        a, hits = ask_score(cracker_path)
        S = m + 7 + a
        print("mirror on %-28s main %.1f (decisions %d of 6, shortest %d of 6) + 7 + ask %.1f (%d of 12) = %.1f" % (
            k, m, dec, sh, a, hits, S))
        if best is None or S > best[0]:
            best = (S, k, hits)
    pair = (C + best[0]) / 2
    print("Pair ceiling: %.1f (cracker %.1f, best mirror %.1f on %s)" % (pair, C, best[0], best[1]))
    print("Mirror leakage: %.1f per cent of ask weight (%d of 12 figures)" % (100.0 * best[2] / 12, best[2]))
    for k, h in (("schedule fields deduplicated (over-cleaner)", dict(dedup="schedule")),
                 ("DEI 050 legs left to the operating flight (golden)", dict())):
        a, hits = ask_score(h)
        print("ask stop %-50s %d of 12" % (k, hits))
    return pair


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(TASK, "target"))
