"""task178 cracker and mirror on the cut pack. The cracker lands the call and runs the careful path on every ask: it
executes every filed sentence, de-duplicates the re-sent rows, puts the 15-minute export on its stated clock (PST),
drops the readings inside each logged visit with the visit times read on that same clock, takes the controller offset
off from the visit log's own readings, and reads the historian's stamps and level tag as exported (its stamps on the
gage's clock, or on the local wall clock). The mirror is the default path's response, off the call, on the same asks.
Prints each graded ask figure group's hits, the pair ceiling on the 38 / 7 / 55 weights and the mirror's leakage.

    python3 task178/generator/cracker.py [target]"""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc  # noqa: E402
import common as C  # noqa: E402


def main(target):
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    st = calc.read_stage(target)
    V = calc.read_visits(target)
    a_file = calc.ask_a(target, st, V, visit_clock="as-file", fix_offset=True)
    a_nolog = calc.ask_a(target, st, [dict(arrive=v["arrive"].replace(year=1900), depart=v["depart"].replace(year=1900),
                                            notes=v["notes"], staff=v["staff"], logger=v["logger"]) for v in V],
                         visit_clock="as-file", fix_offset=True)
    b_pst = calc.ask_b(target, st, clock_fix=False, face_fix=False)
    b_loc = calc.ask_b(target, st, clock_fix=False, face_fix=False, as_local=True)
    groups = []
    ga = figs["ask_a"]
    gb = figs["ask_b"]

    sa = sum(1 for y in ga if a_file[int(y)][0] == ga[y]["stage_ft"])
    da = sum(1 for y in ga if a_file[int(y)][1] == ga[y]["date"])
    sa2 = sum(1 for y in ga if a_nolog[int(y)][0] == ga[y]["stage_ft"])
    da2 = sum(1 for y in ga if a_nolog[int(y)][1] == ga[y]["date"])
    lb = max(sum(1 for y in gb if b[int(y)][0] == gb[y]["pipe_level_ft"]) for b in (b_pst, b_loc))
    fb = max(sum(1 for y in gb if b[int(y)][1] == gb[y]["fall_ft"]) for b in (b_pst, b_loc))
    groups.append(("Ask A, ten window stages", max(sa, sa2), len(ga)))
    groups.append(("Ask A, ten window dates", max(da, da2), len(ga)))
    groups.append(("Ask B, six pipe levels", lb, len(gb)))
    groups.append(("Ask B, six falls", fb, len(gb)))
    n = sum(g[2] for g in groups)
    kept = sum(g[1] for g in groups)
    lc = kept / n
    ls = lc                                  # the asks are decoupled: the mirror's ask path is the cracker's
    C_ = 38 + 7 + 55 * lc
    S_ = 5 + 7 + 55 * ls
    for name, h, tot in groups:
        print("%-28s %d of %d  %s" % (name, h, tot, "miss" if h == 0 else "keeps"))
    print("cracker keeps %d of %d ask figures; mirror (off the call) keeps %d of %d" % (kept, n, kept, n))
    print("pair ceiling %.1f  (cracker %.1f, mirror %.1f)" % ((C_ + S_) / 2, C_, S_))
    print("mirror leakage %.1f per cent of ask weight" % (100 * ls))
    print("decoupled: no ask reads the rating, the peaks' discharges or the frequency fit (checks.py SEP rows)")
    return 0 if kept == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")))
