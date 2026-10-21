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
    en = pd.read_csv(os.path.join(target, "hallam_eligibility_member_months_2023-01_to_2026-09.csv"), dtype=str)
    old = pd.read_csv(os.path.join(target, "hallam_claims_lag_report_paid_2023-01_to_2026-05.csv"), dtype=str)
    new = pd.read_csv(os.path.join(target, "hallam_claims_lag_report_paid_2026-05_to_2026-09.csv"), dtype=str)
    old = pd.DataFrame({"e": old.EmployerNo, "inc": old.IncurredMonth.str[-4:] + "-" + old.IncurredMonth.str[:2],
                        "paid": old.PaidMonth.str[-4:] + "-" + old.PaidMonth.str[:2],
                        "cat": old.Category.str[:3].str.upper(), "amt": old.PaidAmount.astype(float)})
    new = pd.DataFrame({"e": new.employer_code, "inc": new.incurred_period, "paid": new.paid_period,
                        "cat": new.benefit_type.map({"MED": "MED", "RX": "PHA"}),
                        "amt": new.plan_paid_cents.astype(int) / 100})
    lag = pd.concat([old, new]).drop_duplicates(["e", "inc", "paid", "cat"], keep="last")
    lag["y"] = lag.inc.str[:4].astype(int)
    lag = lag[lag.y.between(2023, 2025) & (lag.paid <= (lag.y + 1).astype(str) + "-03")]
    paid = lag.groupby(["e", "y"]).amt.sum()
    re_ = pd.read_csv(os.path.join(target, "westerby_specific_reimbursements_2023-2025.csv"))
    pol = pd.read_csv(os.path.join(target, "westerby_specific_policy_schedule_2023-2027.csv"))
    pmap = pol.set_index(["policy_no", "contract_year"]).employer_id
    re_["e"] = [pmap[(p, y)] for p, y in zip(re_.policy_no, re_.contract_year)]
    rb = re_.groupby(["e", "contract_year"]).reimbursed.sum()
    en["y"] = en.coverage_month.str[:4].astype(int)
    mm = en[en.y.between(2023, 2025)].groupby(["employer_id", "y"]).size()
    ws = openpyxl.load_workbook(os.path.join(target, "crbht_2027_contribution_elections.xlsx"),
                                data_only=True)["2027 elections"]
    rate = {r[0]: r[3] for r in ws.iter_rows(min_row=5, values_only=True) if r[0]}
    ids = sorted(rate)
    X = pd.DataFrame({y: [(paid[(e, y)] - rb.get((e, y), 0.0)) * 1.07 ** (2027 - y) / mm[(e, y)] for e in ids]
                      for y in (2023, 2024, 2025)}, index=ids)
    Wt = pd.DataFrame({y: [mm[(e, y)] for e in ids] for y in (2023, 2024, 2025)}, index=ids).astype(float)
    wi = Wt.sum(1)
    xi = (Wt * X).sum(1) / wi
    xbar = (wi * xi).sum() / wi.sum()
    epv = (Wt * X.sub(xi, axis=0) ** 2).values.sum() / (len(ids) * 2)
    vhm = ((wi * (xi - xbar) ** 2).sum() - (len(ids) - 1) * epv) / (wi.sum() - (wi ** 2).sum() / wi.sum())
    z = wi / (wi + epv / vhm)
    est = xbar + z * (xi - xbar)
    bad = 0
    for e in ids:
        bad += int(round(xi[e])) != fig["experience_pmpm"][e]
    bad += sorted(e for e in ids if est[e] > rate[e]) != fig["call"]["surcharged"]
    q3 = en[en.coverage_month.between("2026-07", "2026-09")]
    q3 = q3.drop_duplicates(["employer_id", "birth_date", "sex", "relationship", "coverage_month"])
    m3 = q3.groupby("employer_id").size()
    for e in ids:
        bad += int(m3[e]) != fig["ask_a"][e]
    hc = pd.read_csv(os.path.join(target, "hallam_high_cost_claimant_report_2026.csv"))
    who = en.drop_duplicates("member_id").set_index("member_id")
    hc["person"] = hc.member_id.map(lambda m: tuple(who.loc[m, ["birth_date", "sex", "relationship"]]))
    last = hc.sort_values("report_month").groupby(["employer_id", "person"]).paid_ytd.last()
    for e in ids:
        s = last[last.index.get_level_values(0) == e]
        bad += len(s) != fig["ask_b"][e]["members"]
        bad += int(round(s.sum())) != fig["ask_b"][e]["claims_to_date"]
    print("verify: %d figures differ from figures.json" % bad)
    return bad == 0


if __name__ == "__main__":
    sys.exit(0 if main(sys.argv[1] if len(sys.argv) > 1 else None) else 1)
