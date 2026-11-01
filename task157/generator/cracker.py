"""task157 architecture 3: the cracker and mirror sheets, run on the cut pack.

The cracker lands the call, runs the hygiene battery and executes every filed rule it is pointed at, and handles
every device it can notice: it merges the control room log with the depot's uncovered work expanded to journeys
(each journey once), applies Schedule 7's excused list and part-journey rule, drops the re-sent ticket machine
uploads and places every transaction on the journey its bus was running by the AVL, which repairs the machine's
unchanged journey selection. What it does not do is ask the AVL whether returned-uncovered work ran, or check each
machine's clock against the AVL. The mirror stops at the route-level assessment and handles the asks the same way.

    run(target, W, M, fig) -> dict(cracker_ask_kept, mirror_ask_kept, ask_figures, pair, mirror_share, rows)
"""
from __future__ import annotations

import csv
import os
from collections import defaultdict
from datetime import datetime, timedelta

import calc as C
import params as P

ASK_WEIGHT, CALL_WEIGHT, IF_WEIGHT = 55.0, 38.0, 7.0


def ask_b_cracker(target, W):
    """The full includer's table: re-sent uploads dropped, each sale placed on the journey its bus was running by
    the AVL (the timetable where the AVL lost the bus), banded on the machine's own clock."""
    import verify as V
    R = V.rules(target)
    js, names, terms = V.timetable(target)
    rec, veh = V.avl(target, js)
    cells, n, want, slow = V.ask_b(target, js, rec, veh, names, R, detect_clock=False)
    return cells, n


def run(target, W, M, fig):
    S = W["S"]
    seen = {(x["date"], x["code"]) for x in W["parsed"] if any(a is not None for a in x["actual"])}
    a_cr = C.ask_a_from_logs(S, W["log"], W["ret"], W["pieces"], "union_no_avl", avl_seen=seen)
    A = fig["ask_a"]
    rows = []
    kept = 0
    total = 0
    for r in P.ROUTE_ORDER:
        hit = round(a_cr[r]) == A["op_km"][r]
        rows.append(("Lost km, route %s" % r, A["op_km"][r], round(a_cr[r]), hit))
        kept += hit
        total += 1
        rel = round(100.0 * (A["sched_km"][r] - a_cr[r]) / A["sched_km"][r], 2)
        hit = rel == A["reliability"][r]
        rows.append(("Reliability, route %s" % r, A["reliability"][r], rel, hit))
        kept += hit
        total += 1
    tot = round(sum(a_cr.values()))
    rows.append(("Lost km, Lot 2", A["op_km_total"], tot, tot == A["op_km_total"]))
    kept += tot == A["op_km_total"]
    total += 1
    lot = round(100.0 * (sum(A["sched_km"].values()) - sum(a_cr.values())) / sum(A["sched_km"].values()), 2)
    rows.append(("Reliability, Lot 2", A["reliability_lot"], lot, lot == A["reliability_lot"]))
    kept += lot == A["reliability_lot"]
    total += 1
    b_cr, n = ask_b_cracker(target, W)
    for d in ("I", "O"):
        for b in ("AM peak", "PM peak", "Other times"):
            g = fig["ask_b"]["cells"]["%s|%s" % (d, b)]
            v = round(b_cr.get((d, b), 0.0))
            rows.append(("Boardings %s %s" % (d, b), g, v, v == g))
            kept += v == g
            total += 1
    vt = round(sum(b_cr.values()))
    rows.append(("Boardings, all", fig["ask_b"]["total"], vt, vt == fig["ask_b"]["total"]))
    kept += vt == fig["ask_b"]["total"]
    total += 1
    share = kept / total
    # the main side: the call (10), each route's floor check (13.5 over nine), each autumn figure (14.5 over nine)
    mirror_main = 13.5 * 7 / 9 + 14.5
    c = CALL_WEIGHT + IF_WEIGHT + ASK_WEIGHT * share
    s = mirror_main + IF_WEIGHT + ASK_WEIGHT * share
    with open(os.path.join(os.path.dirname(target), "generator", "cracker_sheet.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(("figure", "golden", "cracker", "kept"))
        w.writerows(rows)
    return dict(cracker_ask_kept=kept, mirror_ask_kept=kept, ask_figures=total, pair=(c + s) / 2, cracker_score=c,
                mirror_score=s, mirror_share=share, rows=rows)
