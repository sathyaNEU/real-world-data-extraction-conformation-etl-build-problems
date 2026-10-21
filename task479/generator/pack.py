"""The pack's data files, written from the truth in world.py: Hallam's eligibility file and its claims lag reports in
two layouts across the May 2026 platform move, Westerby's specific reimbursement statements for 2023 to 2025 and its
policy schedule, Hallam's 2026 high-cost claimant report, the pharmacy rebate statement, the employer roster and a
broker's survey of small-group plans."""
import csv
import datetime as dt

import numpy as np

import world as W

FILES = {
    "enroll": "hallam_eligibility_member_months_2023-01_to_2026-09.csv",
    "lag_old": "hallam_claims_lag_report_paid_2023-01_to_2026-05.csv",
    "lag_new": "hallam_claims_lag_report_paid_2026-05_to_2026-09.csv",
    "reimb": "westerby_specific_reimbursements_2023-2025.csv",
    "hcc": "hallam_high_cost_claimant_report_2026.csv",
    "policy": "westerby_specific_policy_schedule_2023-2027.csv",
    "rates": "crbht_2027_contribution_elections.xlsx",
    "memo": "crbht_2027_renewal_review.pdf",
    "plan": "crbht_plan_summary_2023-2027.pdf",
    "rebates": "hallam_pharmacy_rebate_statement_2025.csv",
    "roster": "crbht_member_employer_roster_2026-10.csv",
    "survey": "ridgeline_brokers_small_group_survey_2025.csv",
    "dictionary": "crbht_data_dictionary.csv",
    "manifest": "crbht_extract_manifest_2026-10-07.csv",
}
COMPANY = "Corbel Ridge Business Health Trust"
TPA = "Hallam Benefit Administrators"
CARRIER = "Westerby Specialty Insurance Company"

ENROLL_COLS = ["member_id", "subscriber_id", "relationship", "birth_date", "sex", "employer_id", "coverage_month",
               "coverage_tier"]
LAG_OLD_COLS = ["EmployerNo", "IncurredMonth", "PaidMonth", "Category", "PaidAmount", "ClaimLines"]
LAG_NEW_COLS = ["employer_code", "incurred_period", "paid_period", "benefit_type", "plan_paid_cents", "line_count"]
REIMB_COLS = ["contract_year", "claimant_no", "policy_no", "member_ref", "paid_in_contract_year", "specific_deductible",
              "reimbursed"]
HCC_COLS = ["report_month", "member_id", "employer_id", "paid_ytd", "top_diagnosis_group"]
POLICY_COLS = ["policy_no", "employer_id", "contract_year", "effective", "expires", "contract_basis",
               "specific_deductible"]
REBATE_COLS = ["employer_id", "quarter", "rebate_amount", "credited_on"]
ROSTER_COLS = ["employer_id", "employer", "industry", "joined_trust", "renewal_month", "account_manager"]
SURVEY_COLS = ["group_size_band", "plans_reporting", "median_claims_pmpm_2025", "median_renewal_change_pct_2026"]


def write_csv(path, cols, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\r\n")
        w.writerow(cols)
        for r in rows:
            w.writerow(["" if v is None else v for v in r])
    return len(rows)


def ids(x):
    """Hallam member and subscriber ids; Hallam moved the trust's eligibility to its new member-id scheme employer by
    employer in July and August 2026, reissuing every member under a new id from the move month, the old ids left on
    the file for one or two months after it for the families the old feed never terminated."""
    rng = np.random.default_rng(W.SEED + 1)
    order = rng.permutation(len(x["members"]))
    for i, j in enumerate(order):
        x["members"][j]["mid"] = "H%07d" % (4105219 + 13 * i)
    subs = {}
    for m in x["members"]:
        key = (m["emp"], m["sub"])
        if key not in subs:
            subs[key] = "S%06d" % (200000 + int(rng.integers(0, 700000)))
        m["sid"] = subs[key]
    x["move"] = {e: (2026, int(rng.integers(7, 9)), int(rng.integers(1, 3))) for e in W.IDS}
    lingering = {}
    for m in x["members"]:
        m["mid2"] = "N%07d" % (7300011 + 11 * m["k"])
        m["sid2"] = "P%06d" % (500000 + int(m["sid"][1:]) % 99991)
        key = (m["emp"], m["sub"])
        if key not in lingering:
            lingering[key] = rng.random() < 0.38
        m["linger"] = lingering[key]


def tier(fam):
    rels = {m["rel"] for m in fam}
    if rels == {"EE"}:
        return "EE"
    if "SP" in rels and "CH" in rels:
        return "FAM"
    return "ES" if "SP" in rels else "EC"


def enroll_rows(x):
    fams = {}
    for m in x["members"]:
        fams.setdefault((m["emp"], m["sub"]), []).append(m)
    rows = []
    for m in x["members"]:
        t = tier(fams[(m["emp"], m["sub"])])
        mv = x["move"][m["emp"]]
        for ym in W.MONTHS:
            if not (m["start"] <= ym <= m["end"]):
                continue
            row = (m["rel"], m["birth"].isoformat(), m["sex"], m["emp"], "%d-%02d" % ym, t)
            if ym >= (mv[0], mv[1]):
                rows.append((m["mid2"], m["sid2"]) + row)
                if m["linger"] and ym <= (mv[0], mv[1] + mv[2] - 1):
                    rows.append((m["mid"], m["sid"]) + row)
            else:
                rows.append((m["mid"], m["sid"]) + row)
    rows.sort(key=lambda r: (r[6], r[5], r[0]))
    return rows


LAGS = [0.56, 0.31, 0.10, 0.03]


def _after(y, m, k):
    t = y * 12 + m - 1 + k
    return t // 12, t % 12 + 1


def lag_cells(x):
    """Each employer's plan-paid claims by incurred month, paid month and category (pharmacy a fifth of a member's
    claims), every month's claims paid within three months, the cells summing to the members' claims to the cent."""
    rng = np.random.default_rng(W.SEED + 2)
    emp_of = {m["k"]: m["emp"] for m in x["members"]}
    inc = {}
    for (k, ym), v in x["claims"].items():
        key = (emp_of[k], ym)
        inc[key] = inc.get(key, 0.0) + v
    cells = {}
    for (e, ym), amt in sorted(inc.items()):
        rx = round(amt * float(rng.uniform(0.17, 0.23)), 2)
        for cat, a0 in (("Medical", round(amt - rx, 2)), ("Pharmacy", rx)):
            w = np.array(LAGS) * (1 + rng.normal(0, 0.05, 4))
            w /= w.sum()
            parts = [round(a0 * s, 2) for s in w]
            parts[0] = round(a0 - sum(parts[1:]), 2)
            for k, a in enumerate(parts):
                pd = _after(ym[0], ym[1], k)
                if pd <= (2026, 9):
                    cells[(e, ym, pd, cat)] = (a, max(1, int(a / (160.0 if cat == "Medical" else 68.0))))
    x["lag"] = cells
    return cells


def lag_rows(x, layout):
    rows = []
    for (e, inc, pd, cat), (amt, lines) in sorted(x["lag"].items()):
        if layout == "old" and pd <= (2026, 5):
            rows.append((e, "%02d/%d" % (inc[1], inc[0]), "%02d/%d" % (pd[1], pd[0]), cat, "%.2f" % amt, lines))
        if layout == "new" and pd >= (2026, 5):
            rows.append((e, "%d-%02d" % inc, "%d-%02d" % pd, "MED" if cat == "Medical" else "RX",
                         int(round(amt * 100)), lines))
    return rows


def policies():
    """Each employer's specific policy number by contract year; five were rewritten at the 2025 renewal."""
    out = {}
    rew = {"CR113", "CR136", "CR154", "CR167", "CR176"}
    for i, e in enumerate(W.IDS):
        a = "WSI-SL-%05d" % (21409 + 17 * i)
        b = "WSI-SL-%05d" % (38611 + 23 * i) if e in rew else a
        out[e] = {2023: a, 2024: a, 2025: b, 2026: b, 2027: b}
    return out


def policy_rows():
    pol = policies()
    return [(pol[e][y], e, y, "%d-01-01" % y, "%d-12-31" % y, "12/15", W.SPECIFIC) for e in W.IDS
            for y in (2023, 2024, 2025, 2026, 2027)]


def reimb_rows(x):
    """Westerby's specific reimbursements: every member whose plan-paid claims in a contract year passed $150,000."""
    pol = policies()
    mem = {m["k"]: m for m in x["members"]}
    rows = []
    i = 0
    for (k, y), v in sorted(x["member_year"].items(), key=lambda t: (t[0][1], t[0][0])):
        if y in W.YEARS and v > W.SPECIFIC:
            m = mem[k]
            i += 1
            rows.append((y, "WSI-%d-%04d" % (y % 100, 101 + 7 * i), pol[m["emp"]][y], m["mid"], "%.2f" % v,
                         W.SPECIFIC, "%.2f" % (v - W.SPECIFIC)))
    return rows


GROUPS = ["musculoskeletal", "oncology", "cardiac", "maternity", "behavioral health", "renal", "orthopedic surgery",
          "neurology", "digestive", "respiratory"]


def hcc_rows(x):
    """Hallam's monthly high-cost claimant report for 2026: each month, every member whose 2026 claims paid to date
    are $25,000 or more, under the member id the eligibility file carried that month."""
    rng = np.random.default_rng(W.SEED + 4)
    rows = []
    x["hcc_truth"] = {}
    for e in W.IDS:
        for m in x["big26"].get(e, []):
            grp = GROUPS[int(rng.integers(0, len(GROUPS)))]
            cum = 0.0
            mv = x["move"][e]
            for mo in range(1, 10):
                cum += x["claims"].get((m["k"], (2026, mo)), 0.0)
                if cum < W.HCC:
                    continue
                ref = m["mid2"] if (2026, mo) >= (mv[0], mv[1]) else m["mid"]
                rows.append(("2026-%02d" % mo, ref, e, "%.2f" % cum, grp))
            x["hcc_truth"].setdefault(e, []).append(round(cum, 2))
    rows.sort(key=lambda r: (r[0], r[2], r[1]))
    return rows


def rebate_rows(x):
    rng = np.random.default_rng(W.SEED + 5)
    rows = []
    for e in W.IDS:
        rx = sum(v for (ee, inc, pd, c), (v, n) in x["lag"].items() if ee == e and c == "Pharmacy" and inc[0] == 2025)
        for q, cred in (("2025Q1", "2025-08-12"), ("2025Q2", "2025-11-11"), ("2025Q3", "2026-02-10"),
                        ("2025Q4", "2026-05-12")):
            rows.append((e, q, "%.2f" % (rx / 4 * float(rng.uniform(0.17, 0.23))), cred))
    return rows


MANAGERS = ["Steven Coleman", "Amy Blankenship", "Bryan Grant"]


def roster_rows():
    rng = np.random.default_rng(W.SEED + 6)
    return [(e, name, ind, int(rng.integers(2009, 2022)), "January", MANAGERS[i % 3])
            for i, (e, name, ind, n) in enumerate(W.EMPLOYERS)]


def survey_rows():
    return [("2 to 50 employees", 214, "561.30", "9.4"),
            ("51 to 100 employees", 167, "548.85", "8.8"),
            ("101 to 250 employees", 122, "537.15", "8.1"),
            ("251 to 500 employees", 64, "529.40", "7.6")]
