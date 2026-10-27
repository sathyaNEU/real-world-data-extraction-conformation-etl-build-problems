"""task166's ask ceiling, measured on the cut pack: every route a careful solver takes through the onboarding and billing
records is run on the shipped files and scored figure by figure against figures.json (a hit is the exact figure at the
asked precision), and the pair ceiling is computed on the rubric's weights (38 the recommendation and its components, 7
instruction following, 55 the asks over their 60 figures), with the best response off the call keeping 5 of the 38.

    python3 task166/generator/ceiling.py [target]"""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc as C          # noqa: E402

W_REC, W_IF, W_ASK, R_MISS = 38.0, 7.0, 55.0, 5.0
PLANS = ("Core", "Pro", "Enterprise")
KINDS = ("one-to-one", "group")
# what each route is, in the solver's terms
HOURS = {"listed": "one session per host and start, held when any booking completed, every listed specialist's session "
                   "counted, the roster's pods by date (both readers' measured route at round 3)",
         "roster_now": "the same sessions, each host in the pod the roster has them in today (reader A's route at round 2)",
         "customer": "the same sessions, each in the pod that serves its case's customer",
         "booking_account": "the same sessions, each in the pod of the account the booking was made under",
         "booking_dedup": "one specialist per booking reference, the first listed, the roster's pods by date"}
COHORT = {"chain_price": "the register's terms taken back through the later amendments, a day's in the order their terms "
                         "chain, the plan from price and seats (reader B's measured route at round 3)",
          "chain_catalog": "the same terms, the SKU named by today's catalog (reader A's measured route)",
          "number_price": "the amendment log read in its own order (the before terms of the first later amendment by date and "
                          "reference), the plan from price and seats (reader B's route at round 2)",
          "number_catalog": "the same terms, the SKU named by today's catalog",
          "register_catalog": "the register's SKU and value today, named by today's catalog",
          "case_catalog": "the onboarding case's SKU and value, named by today's catalog",
          "register_launch": "the register's terms today, each SKU read as sold",
          "rollback_all_launch": "the amendments on the first invoice date taken back too, each SKU read as sold"}
CRACKER_A, CRACKER_B = "listed", "chain_price"         # the measured Opus reader's own route on each ask (round 3)
MIRROR_A, MIRROR_B = "listed", "chain_catalog"          # the measured Sonnet reader's own route on each ask (round 3)


def main(target):
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    D = C.load(target)
    A = C.amendments(target)
    keys_h = [(p, q, k) for p in C.PODS for q in range(1, 5) for k in KINDS]
    keys_c = [(r, p) for r in C.REG for p in PLANS]
    n = len(keys_h) + 2 * len(keys_c)
    sc_h = {}
    for m in HOURS:
        h = C.ask_pod_hours(target, m, D)
        sc_h[m] = sum(1 for k in keys_h if abs(round(h.get(k, 0.0), 2) - figs["hours"]["%s Q%d %s" % k]) < 1e-9)
    sc_c = {}
    for m in COHORT:
        x = C.ask_cohort(target, m, D, A)
        hits = sum(1 for k in keys_c if x["counts"].get(k, 0) == figs["cohort_counts"]["%s %s" % k])
        hits += sum(1 for k in keys_c if round(x["acv"].get(k, 0.0) / 1000, 1) == figs["cohort_acv_k"]["%s %s" % k])
        sc_c[m] = hits
    print("ask A, specialist hours by pod, quarter and kind of session (24 figures)")
    for m, v in sc_h.items():
        tag = " (cracker)" if m == CRACKER_A else (" (mirror)" if m == MIRROR_A else "")
        print("  %-112s %2d of 24%s" % (HOURS[m], v, tag))
    print("ask B, 2025 new customers and their signed contract value by region and starting plan (36 figures)")
    for m, v in sc_c.items():
        tag = " (cracker)" if m == CRACKER_B else (" (mirror)" if m == MIRROR_B else "")
        print("  %-112s %2d of 36%s" % (COHORT[m], v, tag))
    best_a, best_b = max(sc_h.values()), max(sc_c.values())
    lc = (sc_h[CRACKER_A] + sc_c[CRACKER_B]) / n
    ls = (sc_h[MIRROR_A] + sc_c[MIRROR_B]) / n
    worst = (best_a + best_b) / n
    cracker = W_REC + W_IF + W_ASK * lc
    mirror = R_MISS + W_IF + W_ASK * ls
    print("every listed route keeps at most %d of 24 hours and %d of 36 starting-plan figures" % (best_a, best_b))
    print("cracker (call landed, deepest battery route on each ask) %.1f; mirror (off the call) %.1f" % (cracker, mirror))
    print("both on their best listed route: %.1f" % ((W_REC + W_IF + W_ASK * worst + R_MISS + W_IF + W_ASK * worst) / 2))
    print("one device cracked: ask A repaired, the cracker keeps %d of %d (pair %.1f); ask B repaired, %d of %d (pair %.1f)"
          % (24 + sc_c[CRACKER_B], n, (W_REC + W_IF + W_ASK * (24 + sc_c[CRACKER_B]) / n + mirror) / 2,
             36 + sc_h[CRACKER_A], n, (W_REC + W_IF + W_ASK * (36 + sc_h[CRACKER_A]) / n + mirror) / 2))
    pair = (cracker + mirror) / 2
    print("Pair ceiling: %.1f" % pair)
    print("Mirror leakage: %.1f per cent of ask weight" % (100 * ls))
    return pair


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target"))
