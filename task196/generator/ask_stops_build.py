#!/usr/bin/env python3
"""Measure each ask device's forcing on the cut pack and write generator/ask_stops.json.

For every ask: the natural read's value, the golden's, the gap, and the asking sentence's rounding. A
device whose gap does not exceed its rounding is replaced rather than defended.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import verify as V

def main():
    reg = V.rows("case_register_2024_27.csv")
    legs = V.rows("case_payments.csv")
    members = V.rows("member_register.csv")
    det = V.sheet("settlement_advices_2026_27.xlsx", "advice detail")
    adv = V.sheet("settlement_advices_2026_27.xlsx", "advices")
    q1 = V.rows("notifications_2027_28_q1.csv")
    supp = V.rows("notifications_2027_28_q1_supplementary.csv")
    stmt = V.rows("recovery_statement_2025_26.csv")
    tier = {m["member_code"]: m["contribution_tier"] for m in members}
    QM = {4:1,5:1,6:1,7:2,8:2,9:2,10:3,11:3,12:3,1:4,2:4,3:4}

    # ask A: the detail is the golden, the advice total is the natural read
    gold, nat = {}, {}
    for r in det:
        if r["cover_class"] != "unauthorised fraud": continue
        q = QM[int(str(r["settlement_month"]).split("-")[1])]
        k = "Q%d %s" % (q, tier[r["member_code"]])
        gold[k] = round(gold.get(k, 0.0) + float(r["indemnity_paid_gbp"]), 2)
    for r in adv:
        if r["cover_class"] != "unauthorised fraud": continue
        q = QM[int(str(r["settlement_month"]).split("-")[1])]
        k = "Q%d %s" % (q, tier[r["member_code"]])
        nat[k] = round(nat.get(k, 0.0) + float(r["advice_total_gbp"]), 2)
    for q in (1, 2, 3, 4):
        gold["Q%d total" % q] = round(sum(gold.get("Q%d %s" % (q, t2), 0.0) for t2 in "ABC"), 2)
        nat["Q%d total" % q] = round(sum(nat.get("Q%d %s" % (q, t2), 0.0) for t2 in "ABC"), 2)
    a_moved = {k: round(nat[k] - gold[k], 2) for k in gold if abs(nat[k]-gold[k]) > 0.005}
    a_worst = max(a_moved.items(), key=lambda kv: abs(kv[1]))

    # ask B: the main extract alone is the natural read
    b_gold, b_nat = {}, {}
    for m in members:
        c = m["member_code"]
        b_gold[c+" notified"] = sum(1 for r in q1+supp if r["member_code"] == c)
        b_nat[c+" notified"] = sum(1 for r in q1 if r["member_code"] == c)
        b_gold[c+" value"] = round(sum(float(r["payment_amount_gbp"]) for r in q1+supp
                                       if r["member_code"] == c))
        b_nat[c+" value"] = round(sum(float(r["payment_amount_gbp"]) for r in q1
                                      if r["member_code"] == c))
    b_moved = {c: b_gold[c]-b_nat[c] for c in b_gold if b_gold[c] != b_nat[c]}
    b_worst = max(b_moved.items(), key=lambda kv: kv[1])

    # ask C: the statement's stated share is the natural read
    c_gold, c_nat = {}, {}
    for q in (1,2,3,4):
        sel = [r for r in reg if r["cover_class"]=="scam reimbursement" and r["scheme_year"]=="2025/26"
               and r["closed_date"] and V._q(V.d(r["closed_date"]), "2025/26") == q]
        reimb = sum(float(r["reimbursed_amount_gbp"]) for r in sel)
        refs = {r["case_reference"] for r in sel}
        for route in V.ROUTES:
            got = sum(float(l["credit_amount_gbp"]) for l in legs
                      if l["entry_type"]=="recovery credit" and l["recovery_route"]==route
                      and l["case_reference"] in refs)
            c_gold["Q%d %s" % (q, route)] = round(got/reimb*100.0, 1)
    for r in stmt:
        q = int(r["quarter_closed"][1])
        c_nat["Q%d %s" % (q, r["recovery_route"])] = round(
            float(r["recovered_stated_gbp"])/float(r["reimbursed_in_quarter_gbp"])*100.0, 1)
    sel = [r for r in reg if r["cover_class"]=="scam reimbursement" and r["scheme_year"]=="2025/26"
           and r["closed_date"]]
    reimb_y = sum(float(r["reimbursed_amount_gbp"]) for r in sel)
    refs_y = {r["case_reference"] for r in sel}
    for route in V.ROUTES:
        got = sum(float(l["credit_amount_gbp"]) for l in legs
                  if l["entry_type"]=="recovery credit" and l["recovery_route"]==route
                  and l["case_reference"] in refs_y)
        c_gold["year %s" % route] = round(got/reimb_y*100.0, 1)
        c_nat["year %s" % route] = round(sum(float(r["recovered_stated_gbp"]) for r in stmt
                                             if r["recovery_route"] == route)
                                         / sum(float(r["reimbursed_in_quarter_gbp"]) for r in stmt
                                               if r["recovery_route"] == route) * 100.0, 1)
    c_moved = {k: round(c_gold[k]-c_nat[k], 1) for k in c_gold if abs(c_gold[k]-c_nat[k]) > 0.05}
    c_worst = max(c_moved.items(), key=lambda kv: abs(kv[1]))

    stops = {
        "C1": {"cracker_hits": True, "mirror_hits": False,
               "note": "the four review-group indices: the construction layer, free to a response that lands the call"},
        "C3": {"cracker_hits": True, "mirror_hits": True,
               "note": "the named member's bridge; its opening line is the recorded count, which a rung 2 response has right"},
        "C4": {"cracker_hits": True, "mirror_hits": True,
               "note": "the chart's six named parts; three survive a wrong estimate"},
        "A": {"cracker_hits": False, "mirror_hits": False,
              "figures": 16, "rounding": 1.0, "device": "a prior-period line inside a third of the advice totals",
              "natural_read": nat[a_worst[0]], "golden": gold[a_worst[0]],
              "gap": abs(a_worst[1]), "worst_figure": a_worst[0],
              "figures_moved": len(a_moved)},
        "B": {"cracker_hits": False, "mirror_hits": False,
              "figures": 24, "rounding": 1.0, "device": "the quarter's tail in a supplementary extract",
              "natural_read": b_nat[b_worst[0]], "golden": b_gold[b_worst[0]],
              "gap": abs(b_worst[1]), "worst_figure": b_worst[0],
              "figures_moved": len(b_moved)},
        "C": {"cracker_hits": False, "mirror_hits": False,
              "figures": 15, "rounding": 0.1, "device": "one route stated net of its own agent charge",
              "natural_read": c_nat[c_worst[0]], "golden": c_gold[c_worst[0]],
              "gap": abs(c_worst[1]), "worst_figure": c_worst[0],
              "figures_moved": len(c_moved)},
    }
    with open(os.path.join(HERE, "ask_stops.json"), "w", encoding="utf-8") as f:
        json.dump(stops, f, indent=1, sort_keys=True)
    print("%-3s %-44s %14s %14s %10s %9s %s" % ("ask","device","natural read","golden","gap","rounding","figures moved"))
    for k in ("A","B","C"):
        s = stops[k]
        print("%-3s %-44s %14s %14s %10s %9s %d of %d" % (k, s["device"], s["natural_read"], s["golden"],
              s["gap"], s["rounding"], s["figures_moved"], s["figures"]))
        assert s["gap"] > s["rounding"], "ask %s: the gap does not exceed the asking sentence's rounding" % k
    print("\nevery ask device's forcing exceeds its asking sentence's rounding")
    return 0

if __name__ == "__main__":
    sys.exit(main())
