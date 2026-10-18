"""The cracker and mirror sheets as code, run on the cut pack (supplemental-stumping Part 1.1 and Part 7).

The cracker lands the call, runs the hygiene battery (key uniqueness, exact duplicates, unmatched joins, fan-out)
and executes every filed rule it points at: Schedule B's billable states and its agent-by-agent credit, the
replacement invoice, the standard's wait from first joining the queue, the field guide's session as the customer.
The mirror stops at the most attractive wrong rung on the call (last season's contacts per new case) and reads each
ask the natural way. Each response is scored on a rubric modelled on Part 0's weights: the call and its components
38, the instructions 7, the asks 55 spread evenly over every ask figure. A figure scores when it lands within half a
unit of its stated rounding.

    python3 task173/generator/cracker.py [target]"""
from __future__ import annotations

import datetime as dt
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import asks as AS           # noqa: E402
import common as K          # noqa: E402

TASK = os.path.dirname(HERE)


def r1(x):
    return K.round_half_up(x, 1)


def r0(x):
    return int(K.round_half_up(x, 0))


def figures_of(a_daily, a_unsup, b_daily, b_share):
    out = {}
    for d in AS.fortnight_days():
        out["A day %s" % d] = r1(a_daily[d])
        out["B day %s" % d] = r0(b_daily[d])
    for w in AS.weeks():
        out["A week %s" % w] = r1(a_unsup[w])
        out["B week %s" % w] = r1(b_share[w])
    return out


def paths(target):
    a_true = AS.ask_a(target)
    ar = AS.ask_a_routes(target)
    aw = AS.ask_a_week_routes(target)
    rows, crm = AS.ask_b_rows(target)
    b_true = AS.ask_b(target, rows, crm)
    br = AS.ask_b_routes(target, rows, crm)
    P = {}
    P["golden"] = figures_of(a_true["daily"], a_true["unsupported"], b_true["daily"], b_true["share"])
    # the cracker: every billable row split at Eastern midnight; each agent's logins mapped through the onboarding
    # list and the user list's emails, the replacement invoice, Schedule B's agent-by-agent credit; each customer's
    # session from its first time in the queue to the accepted offer that reached the CRM
    ck = "per session, first queued to the answered row that reached the CRM"
    P["cracker"] = figures_of(ar["sum of billable rows split at midnight"], aw["summed rows, every login"],
                              br[ck]["daily"], br[ck]["share"])
    # the mirror: the natural read of each export
    mk = "each answered row, queued to answered"
    P["mirror"] = figures_of(ar["Duration column by row start date"], aw["summed rows, onboarding logins only"],
                             br[mk]["daily"], br[mk]["share"])
    # sensitivities: one device cracked at a time
    P["cracker, ghosts handled"] = figures_of(a_true["daily"], a_true["unsupported"], br[ck]["daily"], br[ck]["share"])
    P["cracker, the CRM's start used"] = figures_of(ar["sum of billable rows split at midnight"],
                                                    aw["summed rows, every login"], b_true["daily"], b_true["share"])
    return P


def score(P, who, call_landed):
    g = P["golden"]
    f = P[who]
    unit = {"A day": 0.1, "A week": 0.1, "B day": 1.0, "B week": 0.1}
    hits = []
    for k, v in g.items():
        u = unit[" ".join(k.split()[:2])]
        hits.append(abs(f[k] - v) < u / 2 - 1e-9)
    share = sum(hits) / len(hits)
    pts = (38.0 if call_landed else 5.0) + 7.0 + 55.0 * share
    return pts, share, sum(hits), len(hits)


def main(target=None):
    target = target or os.path.join(TASK, "target")
    P = paths(target)
    out = {}
    for who, landed in (("cracker", True), ("mirror", False), ("cracker, ghosts handled", True),
                        ("cracker, the CRM's start used", True)):
        pts, share, h, n = score(P, who, landed)
        out[who] = dict(points=round(pts, 1), ask_share=round(100 * share, 1), hits=h, of=n)
        print("%-32s %5.1f points, %d of %d ask figures (%.1f per cent of ask weight)" % (who, pts, h, n, 100 * share))
    pair = (out["cracker"]["points"] + out["mirror"]["points"]) / 2
    print("pair ceiling %.1f; mirror leakage %.1f per cent of ask weight" % (pair, out["mirror"]["ask_share"]))
    for who in ("cracker, ghosts handled", "cracker, the CRM's start used"):
        print("  with %s: pair %.1f" % (who.split(", ")[1], (out[who]["points"] + out["mirror"]["points"]) / 2))
    near = {}
    for k in P["golden"]:
        u = 1.0 if k.startswith("B day") else 0.1
        near.setdefault(" ".join(k.split()[:2]), []).append(abs(P["cracker"][k] - P["golden"][k]) / u)
    for grp, v in near.items():
        print("  cracker's nearest miss on %s: %.1f printed units" % (grp, min(v)))
    return out, pair, P


if __name__ == "__main__":
    main(*sys.argv[1:2])
