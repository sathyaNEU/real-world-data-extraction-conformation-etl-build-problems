"""The cracker and mirror sheets on the cut pack: the response that lands the call, runs the hygiene battery and executes
every filed rule (the cracker), and the response on the default path (the mirror), scored figure by figure against
generator/figures.json, a hit within half a unit of the stated rounding.

    python3 task121/generator/cracker.py"""
from __future__ import annotations

import json
import os
import sys
import warnings

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as A    # noqa: E402
import common as K      # noqa: E402

TASK = os.path.dirname(HERE)


def score(target):
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    D = A.load(target)
    # the cracker: the working timetable for the day as the base (2.1), the bank holiday's Sunday schedules (field
    # notes), part-cancelled trains as run (2.2), Rostered turns and the controller's amendments on their dates, the
    # register's seats with the modifications from each return to traffic (field notes), a class 166's vehicles
    # summed, every unit formed; arrival minus timetable as clock times; load-weigh summed under the train's
    # headcode at the station before Marlvale Central (its key, as the export carries it)
    on = A.ask_ontime(D, midnight=False)[0]
    sf = A.ask_staffed(D, cover_by="date")[0]
    sd = A.ask_standing(D, key="headcode", vehicles="sum")[0]
    rows = []
    for g in K.GROUP_ORDER:
        rows.append(("on time %s" % g, round(on[g], 1), fig["ask_on_time_pct"][g]))
    for g in K.GROUP_ORDER:
        rows.append(("staffed %s" % g, round(sf[g], 1), fig["ask_staffed_pct"][g]))
    for g in K.INTO_MVC:
        rows.append(("standing %s" % g, int(sd[g]), fig["ask_standing"][g]))
    rows = [(n, got, want, abs(got - want) < (0.05 if isinstance(want, float) else 0.5)) for n, got, want in rows]
    hits = sum(r[3] for r in rows)
    lc = hits / len(rows)
    ls = lc          # the mirror reads the asks as the cracker does: they consume nothing the call produces
    crack = 38 + 7 + 55 * lc
    mirror = 5 + 7 + 55 * ls
    return rows, hits, (crack + mirror) / 2, ls


if __name__ == "__main__":
    rows, hits, pair, ls = score(os.path.join(TASK, "target"))
    for name, got, want, hit in rows:
        print("%-18s cracker %-9s golden %-9s %s" % (name, got, want, "HIT" if hit else "miss"))
    print("cracker keeps %d of %d ask figures; mirror leakage %.1f per cent; pair ceiling %.1f"
          % (hits, len(rows), 100 * ls, pair))
