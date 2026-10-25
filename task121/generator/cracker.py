"""The cracker and mirror sheets on the cut pack: the response that lands the call, runs the hygiene battery and executes
every filed rule (the cracker), and the response on the default path (the mirror), scored figure by figure against
generator/figures.json, a hit when the figure matches at the stated rounding.

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
import deliver as DV    # noqa: E402

TASK = os.path.dirname(HERE)


def score(target):
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    D = A.load(target)
    # The cracker reads the attendance note and the measures summary and executes them: each academy counts the
    # sessions of its own pupils (one enrolment a pupil and admission number), year 11 for the autumn and spring
    # terms, absence as authorised plus unauthorised over sessions possible, the thresholds as 10 and 50 per cent
    # or more; Attainment 8 with English double weighted when both were taken, combined science as two slots at its
    # mean, the technical award points, one qualification a discount code (the first entry for English, maths and
    # the EBacc subjects). It groups the extract by its academy and year group as they stand, and takes the 2026
    # cohort's results from the summer 2026 file.
    att = A.attendance(D, label="current", year="current", key="enrolment_as_extracted")
    res = A.results(D, early=False)
    rows = []
    for k in A.TRUST_NAMES:
        rows.append(("persistent %s" % k, "%.1f" % DV.half_up(att[k]["pa"], 1), fig["annex_a"][k]["pa"]))
        rows.append(("severe %s" % k, "%.1f" % DV.half_up(att[k]["sa"], 1), fig["annex_a"][k]["sa"]))
    for k in A.TRUST_NAMES:
        rows.append(("A8 %s" % k, "%.1f" % DV.half_up(res[k]["a8"], 1), fig["annex_b"][k]["a8"]))
        rows.append(("EBacc %s" % k, "%.1f" % DV.half_up(res[k]["ebacc"], 1), fig["annex_b"][k]["ebacc"]))
    rows = [(n, got, want, got == want) for n, got, want in rows]
    hits = sum(r[3] for r in rows)
    lc = hits / len(rows)
    ls = lc          # the mirror reads the annexes as the cracker does: they consume nothing the walk produces
    crack = 38 + 7 + 55 * lc
    mirror = 5 + 7 + 55 * ls
    return rows, hits, (crack + mirror) / 2, ls


if __name__ == "__main__":
    rows, hits, pair, ls = score(os.path.join(TASK, "target"))
    for name, got, want, hit in rows:
        print("%-36s cracker %-6s golden %-6s %s" % (name, got, want, "HIT" if hit else "miss"))
    print("cracker keeps %d of %d ask figures; mirror leakage %.1f per cent; pair ceiling %.1f"
          % (hits, len(rows), 100 * ls, pair))
