"""The ask sheet's cracker and mirror, run on the cut pack.

The cracker lands the call, runs the hygiene battery and executes every filed rule KC-DQ-04 points at. On Ask A it counts
each build's paying players through the account links, each chain followed to its end (s.6), and reads a phone that
changes account without a link as a phone changing hands; on Ask B it converts every price at its currency's minor unit
and the ECB rate in force on the purchase's Irish date, rounds line by line, and divides each build's gross bookings by
its own paying players. The mirror stops at rung 0 and, the asks being decoupled from the call, meets the same devices.
A figure is kept when it lands on the golden's whole number of players or its cent. Weights 38 / 7 / 55, the mirror's
main block 5 (one build's alert of twelve on the default path's five wrong).

    python3 task235/generator/ceiling.py [target_dir]     (no argument: the figures on target.zip)
"""
import json
import os
import shutil
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import build as B   # noqa: E402
import estim as E   # noqa: E402

TASK = os.path.dirname(HERE)


def run(target):
    D = E.load(target, B.FILES)
    p = E.conform(D)
    gold_pl = E.paying_players(D, p, "golden")
    crack_pl = E.paying_players(D, p, "chain")
    bk = E.bookings(D, p)
    gold_pp = E.per_player(bk, gold_pl)
    crack_pp = E.per_player(bk, crack_pl)
    keep_a = sum(crack_pl[b] == gold_pl[b] for b in gold_pl)
    keep_b = sum(abs(crack_pp[b] - gold_pp[b]) < 0.005 for b in gold_pp)
    total = len(gold_pl) + len(gold_pp)
    lc = ls = (keep_a + keep_b) / float(total)
    cr, mi = 38 + 7 + 55 * lc, 5 + 7 + 55 * ls
    over = {"%s %s" % b: crack_pl[b] - gold_pl[b] for b in gold_pl}
    return dict(ask_figures=total, cracker_kept={"A": int(keep_a), "B": int(keep_b)},
                cracker_players_over_golden=over, cracker=round(cr, 1), mirror=round(mi, 1),
                pair_ceiling=round((cr + mi) / 2, 1), mirror_leakage_pct=round(100 * ls, 1))


def main():
    if len(sys.argv) > 1:
        print(json.dumps(run(sys.argv[1]), indent=1))
        return
    tmp = tempfile.mkdtemp()
    try:
        with zipfile.ZipFile(os.path.join(TASK, "target.zip")) as z:
            z.extractall(tmp)
        print(json.dumps(run(tmp), indent=1))
    finally:
        shutil.rmtree(tmp)


if __name__ == "__main__":
    main()
