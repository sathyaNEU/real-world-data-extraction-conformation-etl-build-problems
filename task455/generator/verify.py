"""Independent verifier: reads only the shipped bundle (register, quarterly reports, wage records) with pandas joins of
its own, recomputes the designation, every county's 2026 births, set-aside accounts and rate, the runner-up and gap,
and each county's 2025 births, deaths and rates, and compares them with generator/figures.json."""
import json
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
FILES = {"register": "ui_employer_register_extract_2027-05-14.csv",
         "qcew": "qcew_private_establishments_2024q4_2026q4.csv",
         "wages": "ui_wage_records_2024q4_2026q4.txt"}
NAMES = {"011": "Brennock", "019": "Caldmere", "027": "Dunrath", "041": "Eskwell", "053": "Fennamore",
         "077": "Quarrin", "089": "Tolbeck"}


def main(target, golden_dir=None):
    reg = pd.read_csv(os.path.join(target, FILES["register"]), dtype=str, keep_default_na=False)
    q = pd.read_csv(os.path.join(target, FILES["qcew"]), dtype={"account_no": str, "county_code": str})
    w = pd.read_csv(os.path.join(target, FILES["wages"]), sep="|", dtype={"worker_key": str, "account_no": str})
    q["qn"] = (q["year"] - 2024) * 4 + q["qtr"] - 4            # 0 = 2024Q4
    w["qn"] = (w["year"] - 2024) * 4 + w["qtr"] - 4
    county = dict(zip(reg["account_no"], reg["county_code"]))
    # months with employment, long form
    m = pd.concat([q[["account_no", "qn"]].assign(mn=q["qn"] * 3 + k, e=q[c]) for k, c in
                   enumerate(["month1_emplvl", "month2_emplvl", "month3_emplvl"])])
    m = m[m["e"] > 0]
    first_m = m.groupby("account_no")["mn"].min()
    last_m = m.groupby("account_no")["mn"].max()

    def base(qn):
        acc = m.loc[m["qn"] == qn, "account_no"].unique()
        return pd.Series([county[a] for a in acc]).value_counts().to_dict()

    def new_accounts(y):
        lo, hi = (15, 26) if y == 2026 else (3, 14)
        acc = first_m[(first_m >= lo) & (first_m <= hi)].index
        liab = reg.set_index("account_no")["liability_date"]
        return [a for a in acc if not (liab[a] and liab[a] < "%d-01-01" % y)]

    pred = {a: p for a, p in zip(reg["account_no"], reg["predecessor_account"]) if p}

    def continuing(accts):
        """Accounts most of whose first-quarter workers were paid the quarter before by one account that reported no
        employment from that quarter on."""
        out = {}
        fq = (first_m[accts] // 3).rename("fq").reset_index()
        firstw = w.merge(fq, left_on=["account_no", "qn"], right_on=["account_no", "fq"])[["account_no", "worker_key",
                                                                                            "fq"]]
        nw = firstw.groupby("account_no")["worker_key"].nunique()
        prev = firstw.assign(pq=firstw["fq"] - 1).merge(w[["worker_key", "account_no", "qn"]].rename(
            columns={"account_no": "src", "qn": "pq"}), on=["worker_key", "pq"])
        prev = prev[prev["src"] != prev["account_no"]]
        cnt = prev.groupby(["account_no", "src"])["worker_key"].nunique().reset_index(name="n")
        cnt = cnt.sort_values(["account_no", "n", "src"], ascending=[True, False, True]).drop_duplicates("account_no")
        for a, src, n in zip(cnt["account_no"], cnt["src"], cnt["n"]):
            fqa = int(first_m[a] // 3)
            stopped = last_m.get(src, -1) < fqa * 3
            if n / nw[a] > 0.5 and stopped:
                out[a] = src
        return out

    new26 = new_accounts(2026)
    cont26 = continuing([a for a in new26 if a not in pred])
    births = pd.Series([county[a] for a in new26 if a not in pred and a not in cont26]).value_counts().to_dict()
    setaside = pd.Series([county[a] for a in new26 if a in pred or a in cont26]).value_counts().to_dict()
    b25 = base(4)
    rates = {c: 100.0 * births.get(c, 0) / b25[c] for c in b25}
    order = sorted(rates, key=lambda c: -rates[c])
    new25 = new_accounts(2025)
    cont25 = continuing([a for a in new25 if a not in pred])
    births25 = pd.Series([county[a] for a in new25 if a not in pred and a not in cont25]).value_counts().to_dict()
    b24 = base(0)
    sources = set(pred.values()) | set(cont25.values()) | set(cont26.values())
    dead = [a for a in last_m.index if 3 <= last_m[a] <= 14 and a not in sources]
    deaths25 = pd.Series([county[a] for a in dead]).value_counts().to_dict()
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    problems = []
    if [NAMES[c] for c in order[:3]] != fig["designated_order"]:
        problems.append("designation")
    if NAMES[order[3]] != fig["runner_up"] or round(rates[order[2]] - rates[order[3]], 1) != fig["gap"]:
        problems.append("runner-up or gap")
    for c, n in NAMES.items():
        f = fig["counties"][n]
        if (births.get(c, 0), setaside.get(c, 0), round(rates[c], 1)) != (f["births"], f["set_aside"], f["rate"]):
            problems.append("2026 " + n)
        y = fig["y2025"][n]
        if (births25.get(c, 0), round(100.0 * births25.get(c, 0) / b24[c], 1), deaths25.get(c, 0),
                round(100.0 * deaths25.get(c, 0) / b24[c], 1)) != (y["births"], y["birth_rate"], y["deaths"],
                                                                    y["death_rate"]):
            problems.append("2025 " + n)
    print("verify: designation %s; runner-up %s, gap %.1f; 2026 births %s; 2025 births %s; 2025 deaths %s" % (
        ", ".join(NAMES[c] for c in order[:3]), NAMES[order[3]], rates[order[2]] - rates[order[3]],
        sum(births.values()), sum(births25.values()), sum(deaths25.values())))
    if problems:
        raise SystemExit("verify: differs from figures.json: " + "; ".join(problems))
    print("verify: every figure in figures.json recomputed from the bundle on an independent path")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target"))
