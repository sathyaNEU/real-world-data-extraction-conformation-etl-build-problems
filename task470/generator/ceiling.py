"""The pair ceiling, measured on the cut pack (supplemental-stumping Part 0). The cracker lands the call, runs the
hygiene battery (each hour once with the later delivery kept, UTC to Norwegian time, the meters joined by unit ID,
Snøholt's old municipality number, the changed meters added) and executes every filed rule: the population register
rolled back to 1 November by undoing every later event as the register writes it, ages on 1 November; the land register
rolled back by registration date, the municipality's enterprises by their parent and its companies through the
shareholder register with its own companies' shares added, title holders matched by organisation number and, where a
title has none, by exact name in the business register. The mirror stops on the best-scoring wrong rung of the ladder
and takes the same route through the two tables, which no rung changes.

Weights 38 / 7 / 55: the main block's 38 as the call 8 and each municipality's vacant dwellings and share 1.5 each;
the 55 over the 40 table figures (30 cells of table A, ten of table B).

    python3 task470/generator/ceiling.py [target]
"""
import hashlib
import os
import sys
import warnings

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
warnings.filterwarnings("ignore")

import methods as M     # noqa: E402
import world as W       # noqa: E402

TASK = os.path.dirname(HERE)
ALL = [m[0] for m in W.MUNICIPALITIES]


def main(target):
    d = M.load(target)
    gres, _ = M.call(d)
    gold = M.designated(gres)
    ga, gb = M.ask_a(d), M.ask_b(d)

    def main_score(res):
        call = M.designated(res) == gold
        hits = sum((res[nr]["vacant"] == gres[nr]["vacant"]) + (res[nr]["share"] == gres[nr]["share"]) for nr in ALL)
        return 8 * call + 1.5 * hits, call, hits

    def ask_score(a, b):
        ha = sum(a[nr][k] == ga[nr][k] for nr in ALL for k in ga[nr])
        hb = sum(b[nr] == gb[nr] for nr in ALL)
        return 55.0 * (ha + hb) / 40.0, ha, hb

    ca, cb = M.ask_a(d, "book"), M.ask_b(d, names="exact")
    c_main, _, _ = main_score(gres)
    c_ask, ha, hb = ask_score(ca, cb)
    C = c_main + 7 + c_ask
    print("cracker: call landed, main %.1f + instructions 7 + tables %.1f (table A %d of 30, table B %d of 10) = %.1f" % (
        c_main, c_ask, ha, hb, C))
    rungs = {"the register's empty dwellings": M.call(d, "register")[0],
             "the register's empty dwellings with no household day": M.call(d, "reg_and_shape")[0]}
    for f in (1, 3, 5, 10, 10.5, 11, 12, 15):
        rungs["a consumption floor of %s kWh a day" % f] = M.call(d, "level", float(f))[0]
    best = None
    for k, res in rungs.items():
        m, call, hits = main_score(res)
        S = m + 7 + c_ask
        print("mirror on %-55s main %.1f (call %s, %2d of 20 figures) + 7 + tables %.1f = %.1f" % (k, m, call, hits,
                                                                                                c_ask, S))
        if best is None or S > best[0]:
            best = (S, k)
    pair = (C + best[0]) / 2
    zp = os.path.join(TASK, "target.zip")
    dig = hashlib.sha256(open(zp, "rb").read()).hexdigest()[:16] if os.path.exists(zp) else "no zip"
    print("Pair ceiling: %.1f (cracker %.1f, best mirror %.1f on %s), pack %s" % (pair, C, best[0], best[1], dig))
    print("Mirror leakage: %.1f per cent of ask weight (%d of 40 figures)" % (100.0 * (ha + hb) / 40, ha + hb))
    for k, (a, b) in (("table A: the register as it stands", (M.ask_a(d, "snapshot"), cb)),
                      ("table A: the dead and emigrated left out", (M.ask_a(d, "no_deaths"), cb)),
                      ("table B: organisation numbers only", (ca, M.ask_b(d, names="none"))),
                      ("table B: every name beginning with the municipality's", (ca, M.ask_b(d, names="startswith"))),
                      ("both tables, every device handled (the golden)", (ga, gb))):
        s, x, y = ask_score(a, b)
        print("tables on %-55s A %2d of 30, B %2d of 10" % (k, x, y))
    return pair


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(TASK, "target"))
