"""The cracker and mirror sheets on the cut pack: the response that lands the call, runs the hygiene battery and executes
every filed rule (the cracker), and the response on the default path (the mirror), scored figure by figure against
generator/figures.json, a hit an exact whole number.

    python3 task280/generator/cracker.py"""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import asks as AK     # noqa: E402
import common as K    # noqa: E402

TASK = os.path.dirname(HERE)


def score(target):
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    hb = fig["hubs"]
    # the cracker: every unplanned ticket over four hours that began in the window (local time), a day for each
    # started 24 hours, the node's subscribers at the end of the month before (5.2 to 5.4), each ticket as filed
    # (ticket ids repeat only across the nodes of one report, which the battery reads as one row a node); and each
    # hub's capacity in service by the register's dates on both days (4.1), every record it lists
    a = AK.credits(target, merge=False)
    b = AK.capacity_added(target, drop_ghosts=False)
    rows = []
    for h in K.HUB:
        ga, gb = hb[h]["outage_credit_subscriber_days"], hb[h]["capacity_added_mbps"]
        rows.append(("A credits %s" % h, a[h], ga, a[h] == ga))
        rows.append(("B capacity added %s" % h, b[h], gb, b[h] == gb))
    hits = sum(r[3] for r in rows)
    lc = hits / len(rows)
    ls = lc          # the mirror reads the asks as the cracker does: they consume nothing the call produces
    crack = 38 + 7 + 55 * lc
    mirror = 5 + 7 + 55 * ls
    return rows, hits, (crack + mirror) / 2, ls


if __name__ == "__main__":
    rows, hits, pair, ls = score(os.path.join(TASK, "target"))
    for name, got, want, hit in rows:
        print("%-24s cracker %-9s golden %-9s %s" % (name, got, want, "HIT" if hit else "miss"))
    print("cracker keeps %d of %d ask figures; mirror leakage %.1f per cent; pair ceiling %.1f"
          % (hits, len(rows), 100 * ls, pair))
