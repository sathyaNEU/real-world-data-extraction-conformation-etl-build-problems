"""An independent recomputation of every graded figure from the cut pack, written apart from bundle.py (pandas),
compared with generator/figures.json.

    python3 task479/generator/verify.py [target]"""
import json
import os
import re
import sys

import openpyxl
import pandas as pd
import pypdf

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)


def main(target=None, gdir=None):
    target = target or os.path.join(TASK, "target")
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    en = pd.read_csv(os.path.join(target, "tollard_eligibility_member_months_2025-01_to_2026-09.csv"), dtype=str)
    old = pd.read_csv(os.path.join(target, "tollard_claims_lag_report_paid_2025-01_to_2026-05.csv"), dtype=str)
    new = pd.read_csv(os.path.join(target, "tollard_claims_lag_report_paid_2026-05_to_2026-09.csv"), dtype=str)
    old = pd.DataFrame({"d": old.DistrictID, "inc": old.IncurredMonth.str[-4:] + "-" + old.IncurredMonth.str[:2],
                        "paid": old.PaidMonth.str[-4:] + "-" + old.PaidMonth.str[:2],
                        "cat": old.Category.str[:3].str.upper(), "amt": old.PaidAmount.astype(float)})
    new = pd.DataFrame({"d": new.district_code, "inc": new.incurred_period, "paid": new.paid_period,
                        "cat": new.benefit_type.map({"MED": "MED", "RX": "PHA"}),
                        "amt": new.plan_paid_cents.astype(int) / 100})
    lag = pd.concat([old, new]).drop_duplicates(["d", "inc", "paid", "cat"], keep="last")
    txt = " ".join(p.extract_text() for p in pypdf.PdfReader(os.path.join(target,
                                                                         "mvshc_benefit_designs_2025_2026.pdf")).pages)
    plan = {(d, int(y)): int(v.replace(",", "")) for d, y, c, v in
            re.findall(r"(MV\d\d)\s+(2025|2026)\s+(MV[ABC])\s+\$([\d,]+)", txt)}
    ws = openpyxl.load_workbook(os.path.join(target, "mvshc_2026_contribution_rates.xlsx"), data_only=True)["2026 rates"]
    rate = {r[0]: r[3] for r in ws.iter_rows(min_row=5, values_only=True) if r[0]}
    paid = lag.groupby(["d", "inc"]).amt.sum()
    mm = en.groupby(["district_id", "coverage_month"]).size()

    def tot(s, d, a, b_):
        v = s.loc[d]
        return v[(v.index >= a) & (v.index <= b_)].sum()
    k = {}
    for dz in (500, 1500, 3000):
        ids = [d for d in rate if plan[(d, 2025)] == dz]
        fy = sum(tot(paid, d, "2025-01", "2025-12") for d in ids) / sum(tot(mm, d, "2025-01", "2025-12") for d in ids)
        h = sum(tot(paid, d, "2025-01", "2025-06") for d in ids) / sum(tot(mm, d, "2025-01", "2025-06") for d in ids)
        k[dz] = fy / h
    bad = 0
    up = []
    for d in sorted(rate):
        v = tot(paid, d, "2026-01", "2026-06") / tot(mm, d, "2026-01", "2026-06") * k[plan[(d, 2026)]]
        bad += int(10 * round(v / 10)) != fig["expected_pmpm"][d]
        if v > rate[d]:
            up.append(d)
    bad += up != fig["call"]["raised"]
    q3 = en[en.coverage_month.between("2026-07", "2026-09")]
    q3 = q3.drop_duplicates(["district_id", "birth_date", "sex", "relationship", "coverage_month"])
    m3 = q3.groupby("district_id").size()
    for d in rate:
        bad += int(m3[d]) != fig["ask_a"][d]
    adv = pd.read_csv(os.path.join(target, "granfield_specific_advisories_2026.csv"), dtype={"incurred_to_date": float})
    pol = pd.read_csv(os.path.join(target, "granfield_specific_policy_schedule_2025-2027.csv"))
    p26 = pol[pol.contract_year == 2026].set_index("policy_no").district_id
    who = en.drop_duplicates("member_id").set_index("member_id")
    adv["d"] = adv.policy_no.map(p26)
    adv["person"] = adv.member_ref.map(lambda m: tuple(who.loc[m, ["birth_date", "sex", "relationship"]]))
    last = adv.sort_values(["advisory_date", "claimant_no"]).groupby(["d", "person"]).incurred_to_date.last()
    for d in rate:
        s = last[last.index.get_level_values(0) == d]
        bad += len(s) != fig["ask_b"][d]["members"]
        bad += int(round(s.sum())) != fig["ask_b"][d]["claims_to_date"]
    print("verify: %d figures differ from figures.json" % bad)
    return bad == 0


if __name__ == "__main__":
    sys.exit(0 if main(sys.argv[1] if len(sys.argv) > 1 else None) else 1)
