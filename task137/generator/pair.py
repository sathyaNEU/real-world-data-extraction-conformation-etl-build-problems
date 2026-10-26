"""The pair ceiling on Part 0's weights (38 recommendation, 7 instruction-following, 55 asks), run on the cut pack.

The cracker lands the call and takes every ask by the route stage 4's Opus reader took on the previous pack, the careful
route: the old clinic codes named by matching the weekdays their requests were issued on to the register's clinic days,
and the sickness rate built under the annual report's definition with every unassigned e-roster line read as a vacant
post. The mirror files the default path's 42,500 and takes the asks the same way: the asks read nothing the call
constructs, so the two ask rows agree by construction (the separation assertions in checks.py). The other routes a
reader could take are printed beside it, each scored on the same cells.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import solve as S


def hits_a(F, tab):
    return sum(int(tab[sp][q] == v) for sp, qq in F["hospital_visits_2025_26"].items() for q, v in qq.items())


def hits_b(F, sk):
    return sum(int(round(sk[q]["hours"] / 7.5) == v["days_lost"]) + int(round(sk[q]["rate"], 1) == v["rate_pct"])
               for q, v in F["sickness_by_quarter"].items())


def score(target):
    F = json.load(open(os.path.join(HERE, "figures.json")))
    D, ci, ev, g = S.solve(target)
    ci.attrs["target"] = target
    days = S.clinic_days_list(target)
    weekday, _ = S.ask_hosp_weekday_route(ci, target)
    golden_a, _ = S.ask_hosp(ci, target)
    flag = S.ask_sick_flag(target, days)
    defin = S.ask_sick_definition(target, days)
    over = S.ask_sick_overclean(target, days)
    a, b = hits_a(F, weekday), max(hits_b(F, flag), hits_b(F, defin))
    cells = 28 + 8
    print("ask A, old codes by request weekday against the register's clinic days (the careful route): %d of 28" % a)
    print("ask A, the golden's link through the March 2026 issues (control): %d of 28" % hits_a(F, golden_a))
    print("ask B, unassigned lines read as vacant posts: %d of 8; filled posts from the report, sickness rows only: %d of 8"
          % (hits_b(F, flag), hits_b(F, defin)))
    print("ask B, every unassigned line read as sickness, the vacant post included (the over-cleaner): %d of 8"
          % hits_b(F, over))
    keep = a + b
    Lc = keep / float(cells)
    C = 38 + 7 + 55 * Lc
    Sm = 5 + 7 + 55 * Lc
    pair = (C + Sm) / 2.0
    print("cracker on the call: %d (plan), keeps %d of %d ask cells, scores %.1f" % (g["plan_r"], keep, cells, C))
    print("mirror at the default path 42,500, keeps %d of %d ask cells, scores %.1f" % (keep, cells, Sm))
    print("Pair ceiling: %.1f" % pair)
    print("Mirror leakage: %.1f per cent of ask weight" % (100 * Lc))
    over_keep = a + hits_b(F, over)
    print("with the over-cleaner's ask B instead: keeps %d of %d, pair %.1f"
          % (over_keep, cells, (38 + 7 + 5 + 7 + 2 * 55 * over_keep / float(cells)) / 2.0))
    return pair, 100 * Lc


if __name__ == "__main__":
    score(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target"))
