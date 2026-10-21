"""An independent recomputation of every graded figure from the cut pack, written apart from bundle.py (pandas),
compared with generator/figures.json.

    python3 task479/generator/verify.py [target]"""
import json
import os
import sys

import openpyxl
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)


def main(target=None, gdir=None):
    target = target or os.path.join(TASK, "target")
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    en = pd.read_csv(os.path.join(target, "mba_enrollment_member_months_2025-01_to_2026-08.csv"))
    old = pd.read_csv(os.path.join(target, "mba_claims_lag_report_paid_2025-01_to_2026-05.csv"))
    new = pd.read_csv(os.path.join(target, "mba_claims_lag_report_paid_2026-06_to_2026-09.csv"))
    old = pd.DataFrame({"g": old.GroupNo, "inc": old.IncurredMonth.str[-4:] + "-" + old.IncurredMonth.str[:2],
                        "paid": old.PaidMonth.str[-4:] + "-" + old.PaidMonth.str[:2], "cat": old.Category.str[:3].str.upper(),
                        "amt": old.PaidAmount})
    new = pd.DataFrame({"g": new.group_id, "inc": new.incurred_period, "paid": new.paid_period,
                        "cat": new.benefit_type.map({"MED": "MED", "RX": "PHA"}), "amt": new.paid_cents / 100})
    lag = pd.concat([old, new]).drop_duplicates(["g", "inc", "paid", "cat"], keep="last")
    exp = lag[lag.inc.str.startswith("2025") & (lag.paid <= "2026-03")].groupby("g").amt.sum()
    mm = en[en.coverage_month.str.startswith("2025")].groupby("group_no").size()
    lcr = pd.read_csv(os.path.join(target, "arbor_ridge_large_claimant_report_cy2025.csv"))
    pol = pd.read_csv(os.path.join(target, "arbor_ridge_specific_policy_schedule_2025-2027.csv"))
    p25 = pol[pol.contract_year == 2025].set_index("policy_no").group_no
    lcr["g"] = lcr.policy_no.map(p25)
    F = 1.075 ** 2
    lcr["x27"] = (lcr.total_incurred * F - 250000).clip(lower=0)
    ws = openpyxl.load_workbook(os.path.join(target, "mba_2027_funding_elections.xlsx"), data_only=True)["2027 elections"]
    rate = {r[0]: r[3] for r in ws.iter_rows(min_row=2, values_only=True) if r[0]}
    bad = 0
    notes = []
    for g in sorted(rate):
        v = (F * exp[g] - lcr[lcr.g == g].x27.sum()) / mm[g]
        bad += "%d" % round(v) != fig["retained_pmpm"][g]
        if v > rate[g]:
            notes.append(g)
    bad += notes != fig["call"]["notices"]
    e26 = en[en.coverage_month.str.startswith("2026")]
    e26 = e26.drop_duplicates(["group_no", "birth_date", "sex", "relationship", "coverage_month"])
    m26 = e26.groupby("group_no").size()
    p26 = lag[lag.inc.between("2026-01", "2026-08")].groupby("g").amt.sum()
    for g in rate:
        bad += int(m26[g]) != fig["ask_a"][g]["member_months"]
        bad += "%.2f" % (p26[g] / m26[g]) != fig["ask_a"][g]["paid_pmpm"]
    adv = pd.read_csv(os.path.join(target, "arbor_ridge_specific_advisories_2026.csv"))
    p26p = pol[pol.contract_year == 2026].set_index("policy_no").group_no
    who = en.drop_duplicates("member_id").set_index("member_id")
    adv["g"] = adv.policy_no.map(p26p)
    adv["person"] = adv.member_ref.map(lambda m: tuple(who.loc[m, ["birth_date", "sex", "relationship"]]))
    last = adv.sort_values(["advisory_date", "claimant_no"]).groupby(["g", "person"]).incurred_to_date.last()
    for g in rate:
        s = last[last.index.get_level_values(0) == g]
        bad += len(s) != fig["ask_b"][g]["members"]
        bad += int(round(s.sum())) != fig["ask_b"][g]["claims_to_date"]
    print("verify: %d figures differ from figures.json" % bad)
    return bad == 0


if __name__ == "__main__":
    sys.exit(0 if main(sys.argv[1] if len(sys.argv) > 1 else None) else 1)
