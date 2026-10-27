"""The cracker and mirror sheets on the cut pack: the response that lands the call, runs the hygiene battery and executes
every filed rule (the cracker), and the response on the default path (the mirror), scored figure by figure against
generator/figures.json, a hit an exact whole number.

    python3 task281/generator/cracker.py"""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import asks as AK     # noqa: E402
import common as K    # noqa: E402
import pack as PK     # noqa: E402

TASK = os.path.dirname(HERE)


def score(target):
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    pk = PK.Pack(target)
    # the cracker: runs the hygiene battery (a piece paid again on a later check, same employee, work date, start and
    # hours, dropped everywhere as a duplicate), executes every filed rule (compensatory time credited at 1.5 an hour
    # worked under MOU 14.2 and hour for hour for the aides; each piece at the unit of its accepted offer, else the
    # employee's own unit, as the dictionary files them; SL-0410 mapped to Thornmere) and counts people as employee
    # records (no key joins two). The reader-calibrated variant also joins the rehires by their restored seniority.
    a = AK.ask_a(pk)
    b = AK.ask_b(pk, merge=False)
    c = AK.ask_c(pk, merge=False)
    a_plus = AK.ask_a(pk)
    b_plus = AK.ask_b(pk)
    c_plus = AK.ask_c(pk)
    rows = []
    for u in K.UNIT_CODES:
        rows.append(("A hours %s" % u, a[u], fig["ask_a_overtime_hours_by_unit"][u]))
    for u in K.UNIT_CODES:
        rows.append(("B people %s" % u, b[u], fig["ask_b_people_by_unit"][u]))
    for t in K.TITLE_ORDER:
        rows.append(("C people %s" % t, c[t], fig["ask_c_people_over_600_hours"][t]))
    rows = [(n, got, want, got == want) for n, got, want in rows]
    plus = sum(a_plus[u] == fig["ask_a_overtime_hours_by_unit"][u] for u in K.UNIT_CODES) + \
        sum(b_plus[u] == fig["ask_b_people_by_unit"][u] for u in K.UNIT_CODES) + \
        sum(c_plus[t] == fig["ask_c_people_over_600_hours"][t] for t in K.TITLE_ORDER)
    print("reader-calibrated cracker (the rehires joined): %d of %d" % (plus, len(rows)))
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
