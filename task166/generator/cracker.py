"""The ask layer measured on the cut pack: the cracker (lands the call, runs the hygiene battery, executes every filed
rule and definition it reads) and the mirror (the best response off the call, stopped at agency MBS) on Ask A, the
hedge programme's notional in effect at each 2027 quarter-end by part, and the deck's chart. Prints each path's
figures, its hits within half a unit of the asked rounding, the pair ceiling and the mirror leakage.

    python3 cracker.py [pack]          default: a fresh unzip of task166/target.zip"""
from __future__ import annotations

import os
import shutil
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc as C            # noqa: E402

TASK = os.path.dirname(HERE)
PARTS = ("overlay", "funding", "loan")
HALF = 0.05                         # half a unit of one decimal, $ millions
W_REC, W_IF, W_ASK = 38.0, 7.0, 55.0
R_MISS = 5.0                        # recommendation weight a wrong call keeps (the deck's structure, the file)
CHART_PARTS = ("one stacked bar per quarter-end", "the three parts stacked", "each segment labelled",
               "the labels carry the table's values")


def hits(path, gold):
    n = 0
    for p in PARTS:
        for a, b in zip(path[p], gold[p]):
            n += abs(a / 1e6 - round(b / 1e6, 1)) < HALF
    return n


def paths(pack):
    gold = C.programme(pack)
    out = {
        "golden": gold,
        # the cracker: the register's live ALM trades, the schedules, the policy's parts by what each swap is designated
        # against, the new overlay added; the battery passes (keys unique, no exact duplicates, every cleared trade's
        # clearing ref on the statement, no fan-out), so no trade is dropped
        "cracker": C.programme(pack, read_backload=False, by="item"),
        # the mirror reads the asks the same way (they share no row with the call)
        "mirror": C.programme(pack, read_backload=False, by="item"),
        # the over-cleaner drops every trade whose terms repeat another's
        "over-cleaner": C.programme(pack, read_backload=False, dedupe_terms=True),
        # the label reader parts the swaps by the register's strategy code
        "strategy code": C.programme(pack, read_backload=False, by="strategy"),
        "backload read, strategy code": C.programme(pack, by="strategy"),
    }
    return out


def measure(pack, quiet=False):
    P = paths(pack)
    gold = P["golden"]
    n_fig = 3 * len(C.QUARTER_ENDS)
    n_ask = n_fig + len(CHART_PARTS)
    res = {}
    for k, v in P.items():
        h = hits(v, gold)
        chart = 3 + (1 if h == n_fig else 0)
        res[k] = dict(figures=h, chart=chart, share=(h + chart) / n_ask)
        if not quiet:
            print("%-30s figures hit %2d of %d, chart parts %d of %d   %s" % (
                k, h, n_fig, chart, len(CHART_PARTS),
                "  ".join("%s %s" % (p[:4], ",".join("%.1f" % (x / 1e6) for x in v[p])) for p in PARTS)))
    c = W_REC + W_IF + W_ASK * res["cracker"]["share"]
    s = R_MISS + W_IF + W_ASK * res["mirror"]["share"]
    pair = (c + s) / 2
    leak = 100 * res["mirror"]["share"]
    if not quiet:
        print("cracker %.1f, mirror %.1f: pair ceiling %.1f; mirror leakage %.1f per cent of ask weight" % (c, s, pair,
                                                                                                          leak))
    return dict(res=res, cracker=c, mirror=s, pair=pair, leak=leak)


def main():
    if len(sys.argv) > 1:
        return measure(sys.argv[1])
    tmp = tempfile.mkdtemp(prefix="b166_crack_")
    try:
        with zipfile.ZipFile(os.path.join(TASK, "target.zip")) as z:
            z.extractall(tmp)
        return measure(tmp)
    finally:
        shutil.rmtree(tmp)


if __name__ == "__main__":
    main()
