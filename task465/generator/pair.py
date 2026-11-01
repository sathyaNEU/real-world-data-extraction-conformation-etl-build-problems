"""The ask sheet's measurement on the cut pack: the cracker (lands the call, executes every filed rule, runs the two
asks the obvious way) and the mirror (the default path's independence call, the same asks), scored figure by figure
on the 38 / 7 / 55 planning weights against the golden recomputed from the same pack.

    python3 task465/generator/pair.py <target dir>

Main block (38): the total caseworkers, each division's caseworkers and eligible households, the eighteen cells,
each a criterion of equal weight. Instruction-following (7): kept by both paths. Asks (55) over 20 criteria: Ask A's
nine divisions, Ask B's nine, and the two files.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bundle as B    # noqa: E402
import methods as M   # noqa: E402
import world as W     # noqa: E402

REC, IF, ASK = 38.0, 7.0, 55.0


def main_figures(cells):
    tot = M.division_totals(cells)
    cw = {d: M.caseworkers(tot[d]) for d in W.DIV_NAMES}
    figs = {"total": sum(cw.values())}
    for d in W.DIV_NAMES:
        figs["cw|" + d] = cw[d]
        figs["hh|" + d] = round(tot[d] / 100)
    for k, v in cells.items():
        figs["cell|%s|%s" % k] = round(v / 100)
    return figs


def score(main, gold_main, a, b, gold_a, gold_b):
    m = sum(main[k] == gold_main[k] for k in gold_main) / len(gold_main)
    asks = sum(a[d] == gold_a[d] for d in W.DIV_NAMES) + sum(b[d] == gold_b[d] for d in W.DIV_NAMES) + 2
    return REC * m + IF + ASK * asks / 20.0, m, asks


def run(target):
    N, p, q, tabs, tabs_div = B.conformed(target)
    R, _ = M.routes(N, p, q, tabs, tabs_div)
    gold_main = main_figures(R["golden"])
    gold_a, gold_b = B.baseline_households(target), B.battery_households(target)
    # the cracker's asks: open accounts by the register's division; distinct accounts on Central Time
    ca, cb = B.baseline_households(target, unit="account"), B.battery_households(target, unit="account")
    crack, cm, cn = score(main_figures(R["golden"]), gold_main, ca, cb, gold_a, gold_b)
    mirror, mm, mn = score(main_figures(R["independence"]), gold_main, ca, cb, gold_a, gold_b)
    print("cracker: main %.0f%% of %d criteria, asks %d of 20, score %.1f" % (100 * cm, len(gold_main), cn, crack))
    print("mirror:  main %.0f%% of %d criteria, asks %d of 20, score %.1f" % (100 * mm, len(gold_main), mn, mirror))
    print("mirror leakage: %.1f per cent of ask weight" % (100.0 * mn / 20))
    print("pair ceiling: %.1f" % ((crack + mirror) / 2))
    return crack, mirror


if __name__ == "__main__":
    run(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target"))
