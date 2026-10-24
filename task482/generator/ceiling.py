"""The ask layer's pair ceiling on the cut pack (supplemental-stumping Part 0 and 1.1).

    python3 task482/generator/ceiling.py

The cracker lands the call, runs the hygiene battery and executes every filed rule: it counts each live session row
delivered in the district's term at the export's hours read as decimal hours, never de-duplicates a joint session, and
applies each credit by the import layout's rule. The mirror stops at the default rung (the contractor's plausible values averaged by district)
and does everything else as the cracker does. Each graded ask figure in submission.md's Deliverable Answers is scored
against the golden: a district's hours, a district's shortfall credit, a credit memo row."""
import collections
import csv
import datetime as dt
import json
import os

import numpy as np
import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")


def rows(name):
    with open(os.path.join(T, name), newline="") as f:
        return list(csv.DictReader(f))


def main():
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    ws = openpyxl.load_workbook(os.path.join(T, "order_forms_2025_26.xlsx"), read_only=True)["Order forms 2025-26"]
    it = ws.iter_rows(values_only=True)
    head = next(it)
    of = {x["Partner ID"]: x for x in (dict(zip(head, r)) for r in it)}
    pids = sorted(of)
    # the mirror's call: plausible values averaged by district over the eligible assessed students
    elig = {r["student_id"]: r["partner_id"] for r in rows("guarantee_eligibility_2025_26.csv") if r["guarantee_eligible"] == "Y"}
    xw = collections.defaultdict(list)
    for r in rows("student_id_crosswalk_2025_26.csv"):
        xw[r["test_taker_id"]].append(r["student_id"])
    hit, cnt = collections.Counter(), collections.Counter()
    cut = {6: 500.0, 7: 520.0, 8: 540.0}
    for r in rows("caldrith_plausible_values_2026.csv"):
        es = [s for s in xw[r["test_taker_id"]] if s in elig]
        if not es:
            continue
        p = elig[es[0]]
        c = cut[int(r["grade"])]
        hit[p] += np.mean([float(r["pv%d" % k]) >= c for k in range(1, 6)])
        cnt[p] += 1
    mirror_owed = sorted(p for p in pids if 100 * hit[p] / cnt[p] < of[p]["Guarantee Benchmark (%)"])
    gold_owed = figs["call"]["owed"]
    # the cracker's and the mirror's professional learning: the export's hours on every delivered live row in term
    hrs = collections.Counter()
    for r in rows("pd_sessions_2025_26.csv"):
        o = of[r["partner_id"]]
        d = dt.date.fromisoformat(r["session_date"])
        if r["status"] == "Delivered" and r["delivery"] in ("Virtual live", "On site") and \
                o["Subscription Term Start"].date() <= d <= o["Subscription Term End"].date():
            hrs[r["partner_id"]] += float(r["hours"])
    hrs = {p: float(np.floor(hrs[p] * 2 + 0.5) / 2) for p in pids}
    pl = {p: max(0.0, of[p]["Live PL Hours"] - hrs[p]) * 250 for p in pids}
    inv = rows("billing_invoices_2026_27.csv")

    def memos(owed_set):
        out = set()
        for p in pids:
            o = of[p]
            a = o["Subscription Term Start"].date().replace(year=2026)
            c = [x for x in inv if x["customer_account"] == o["Bill-to Account"] and x["status"] == "Open"
                 and x["service_period_start"] == a.isoformat() and "subscription 2026-27" in x["description"]]
            tgt = min(c, key=lambda x: (x["due_date"], x["invoice_number"]))["invoice_number"] if c else "CHECK"
            og = round(o["Subscription Fee (USD)"] * o["Credit Percentage (%)"] / 100, 2) if p in owed_set else 0
            for code, amt in (("OG", og), ("PL", pl[p])):
                if amt > 0:
                    out.add(("%s-2526-%s" % (code, p[3:]), o["Bill-to Account"], code, "%.2f" % amt, tgt))
        return out

    gold_memos = {(m["memo_reference"], m["customer_account"], m["reason_code"], "%.2f" % m["credit_amount"],
                   m["apply_to_invoice"] if m["refund_method"] == "APPLY" else "CHECK") for m in figs["memos"]}
    ds = figs["districts"]
    n_hours = len(pids)
    gold_pl = [p for p in pids if ds[p]["pl"] > 0]
    total = n_hours + len(gold_pl) + len(gold_memos)

    def keep(owed_set):
        k_h = sum(1 for p in pids if abs(hrs[p] - ds[p]["pd_delivered"]) < 0.25)
        k_p = sum(1 for p in gold_pl if abs(pl[p] - ds[p]["pl"]) < 0.005)
        k_m = len(memos(owed_set) & gold_memos)
        return k_h, k_p, k_m

    ck, mk = keep(set(gold_owed)), keep(set(mirror_owed))
    Lc, Lm = sum(ck) / total, sum(mk) / total
    C = 38 + 7 + 55 * Lc
    S = 5 + 7 + 55 * Lm
    print("ask figures: %d hours, %d shortfall credits, %d credit memos (%d in all)" % (n_hours, len(gold_pl), len(gold_memos), total))
    print("cracker keeps hours %d, credits %d, memos %d: %.1f per cent of ask weight; scores %.1f" % (ck + (100 * Lc, C)))
    print("mirror (default rung, %d owed, %d flips) keeps hours %d, credits %d, memos %d: %.1f per cent; scores %.1f"
          % ((len(mirror_owed), len(set(mirror_owed) ^ set(gold_owed))) + mk + (100 * Lm, S)))
    print("pair ceiling %.1f; mirror leakage %.1f per cent of ask weight" % ((C + S) / 2, 100 * Lm))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
