"""The pack's data files, written from the truth in world.py: Tollard's eligibility file and its claims lag reports in
two layouts across the May 2026 platform move, Granfield's specific stop-loss policy schedule and 2026 advisories, the
pharmacy rebate statement, the districts' fiscal 2026 contribution receipts and the state survey of school employee
plans."""
import csv
import datetime as dt

import numpy as np

import world as W

FILES = {
    "enroll": "tollard_eligibility_member_months_2025-01_to_2026-09.csv",
    "lag_old": "tollard_claims_lag_report_paid_2025-01_to_2026-05.csv",
    "lag_new": "tollard_claims_lag_report_paid_2026-05_to_2026-09.csv",
    "adv": "granfield_specific_advisories_2026.csv",
    "policy": "granfield_specific_policy_schedule_2025-2027.csv",
    "rates": "mvshc_2026_contribution_rates.xlsx",
    "memo": "mvshc_contribution_review_january_2027.pdf",
    "benefits": "mvshc_benefit_designs_2025_2026.pdf",
    "rebates": "tollard_pharmacy_rebate_statement_2025.csv",
    "receipts": "mvshc_district_contribution_receipts_fy2026.csv",
    "survey": "state_school_employee_plan_survey_2025.csv",
    "dictionary": "mvshc_data_dictionary.csv",
    "manifest": "mvshc_extract_manifest_2026-10-06.csv",
}
COMPANY = "Merrin Valley Schools Health Cooperative"
TPA = "Tollard Benefit Services"
CARRIER = "Granfield Specialty Insurance Company"
PLAN = {500: "MVA", 1500: "MVB", 3000: "MVC"}

ENROLL_COLS = ["member_id", "subscriber_id", "relationship", "birth_date", "sex", "district_id", "plan_code",
               "coverage_month", "coverage_tier"]
LAG_OLD_COLS = ["DistrictID", "IncurredMonth", "PaidMonth", "Category", "PaidAmount", "ClaimLines"]
LAG_NEW_COLS = ["district_code", "incurred_period", "paid_period", "benefit_type", "plan_paid_cents", "line_count"]
ADV_COLS = ["advisory_date", "claimant_no", "policy_no", "member_ref", "incurred_to_date", "advisory_type"]
POLICY_COLS = ["policy_no", "district_id", "contract_year", "effective", "expires", "contract_basis",
               "specific_deductible", "aggregate_corridor_pct"]
REBATE_COLS = ["district_id", "quarter", "rebate_amount", "credited_on"]
RECEIPT_COLS = ["district_id", "fiscal_year", "billing_month", "contribution_billed", "contribution_received",
                "received_on"]
SURVEY_COLS = ["plan_type", "deductible_band", "plans_reporting", "median_total_pmpm_2025", "median_employer_share_pct"]


def write_csv(path, cols, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\r\n")
        w.writerow(cols)
        for r in rows:
            w.writerow(["" if v is None else v for v in r])
    return len(rows)


def ids(x):
    """Tollard member and subscriber ids; every district moved its payroll to the county's shared HR system in July or
    August 2026, and its members had their members reissued under new ids from the move month, the old ids left on the file for
    one or two months after it for the families the old payroll feed never terminated."""
    rng = np.random.default_rng(W.SEED + 1)
    order = rng.permutation(len(x["members"]))
    for i, j in enumerate(order):
        x["members"][j]["mid"] = "T%07d" % (3104411 + 13 * i)
    subs = {}
    for m in x["members"]:
        key = (m["district"], m["sub"])
        if key not in subs:
            subs[key] = "S%06d" % (200000 + int(rng.integers(0, 700000)))
        m["sid"] = subs[key]
    x["move"] = {}
    for did in W.IDS:
        x["move"][did] = (2026, int(rng.integers(7, 9)), int(rng.integers(1, 3)))
    for m in x["members"]:
        if m["district"] in x["move"]:
            m["mid2"] = "T%07d" % (6200007 + 11 * m["k"])
            m["sid2"] = "S%06d" % (900000 + int(m["sid"][1:]) % 99991)
    # the old payroll feed sent no termination for some families, whose old ids stayed on the file
    lingering = {}
    for m in x["members"]:
        key = (m["district"], m["sub"])
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
        fams.setdefault((m["district"], m["sub"]), []).append(m)
    d25 = {d[0]: d[2] for d in W.DISTRICTS}
    d26 = {d[0]: d[3] for d in W.DISTRICTS}
    rows = []
    for m in x["members"]:
        t = tier(fams[(m["district"], m["sub"])])
        mv = x["move"].get(m["district"])
        for ym in W.MONTHS25 + W.MONTHS26:
            if not (m["start"] <= ym <= m["end"]):
                continue
            ymS = "%d-%02d" % ym
            pc = PLAN[d25[m["district"]] if ym[0] == 2025 else d26[m["district"]]]
            row = (m["rel"], m["birth"].isoformat(), m["sex"], m["district"], pc, ymS, t)
            if mv and ym >= (mv[0], mv[1]):
                rows.append((m["mid2"], m["sid2"]) + row)
                if m["linger"] and ym <= (mv[0], mv[1] + mv[2] - 1):
                    rows.append((m["mid"], m["sid"]) + row)
            else:
                rows.append((m["mid"], m["sid"]) + row)
    rows.sort(key=lambda r: (r[7], r[5], r[0]))
    return rows


LAGS = [0.56, 0.31, 0.10, 0.03]      # share of a month's plan-paid claims paid k months after the month of service


def _after(y, m, k):
    t = y * 12 + m - 1 + k
    return t // 12, t % 12 + 1


def lag_cells(x):
    """Each district's plan-paid claims by incurred month, paid month and category: every month's claims paid within
    three months of it, the cells summing to the month's claims to the cent; paid months January 2025 to September
    2026."""
    rng = np.random.default_rng(W.SEED + 2)
    cells = {}
    for (did, inc, cat), amt in sorted(x["paid"].items()):
        w = np.array(LAGS) * (1 + rng.normal(0, 0.05, 4))
        w /= w.sum()
        parts = [round(amt * s, 2) for s in w]
        parts[0] = round(amt - sum(parts[1:]), 2)
        for k, a in enumerate(parts):
            pd = _after(inc[0], inc[1], k)
            if (2025, 1) <= pd <= (2026, 9):
                lines = max(1, int(a / (165.0 if cat == "Medical" else 71.0)))
                cells[(did, inc, pd, cat)] = (a, lines)
    x["lag"] = cells
    return cells


def lag_rows(x, layout):
    rows = []
    for (did, inc, pd, cat), (amt, lines) in sorted(x["lag"].items()):
        if layout == "old" and pd <= (2026, 5):
            rows.append((did, "%02d/%d" % (inc[1], inc[0]), "%02d/%d" % (pd[1], pd[0]), cat, "%.2f" % amt, lines))
        if layout == "new" and pd >= (2026, 5):
            # the new platform's first export carried May 2026 again, as the old platform had sent it
            rows.append((did, "%d-%02d" % inc, "%d-%02d" % pd, "MED" if cat == "Medical" else "RX",
                         int(round(amt * 100)), lines))
    return rows


def policies():
    """Each district's specific policy number by contract year; four were rewritten at the 2026 renewal."""
    out = {}
    rew = {"MV11", "MV28", "MV39", "MV54"}
    for i, did in enumerate(W.IDS):
        a = "GSI-SL-%05d" % (30417 + 19 * i)
        b = "GSI-SL-%05d" % (47203 + 29 * i) if did in rew else a
        out[did] = {2025: a, 2026: b, 2027: b}
    return out


def policy_rows():
    pol = policies()
    rows = []
    for did in W.IDS:
        for y in (2025, 2026, 2027):
            rows.append((pol[did][y], did, y, "%d-01-01" % y, "%d-12-31" % y, "12/15", W.SPECIFIC, 125))
    return rows


def adv_rows(x):
    """Granfield's 2026 specific advisories: a row each month for every claimant at or over the 50 per cent threshold,
    restating the claimant's 2026 incurred claims to date (claims reprocessed later can lower it)."""
    rng = np.random.default_rng(W.SEED + 4)
    pol = policies()
    rows = []
    x["adv_truth"] = {}
    cand = sorted((m for d in W.IDS for m in x["big26"][d]), key=lambda m: m["k"])
    for i, m in enumerate(cand):
        cno = "GSI-26-%05d" % (11027 + 9 * i)
        cno2 = "GSI-26-%05d" % (58113 + 9 * i)
        start = int(rng.integers(2, 5))
        path = np.sort(rng.uniform(0.62, 1.0, 10 - start))
        path[-1] = 1.0
        vals = [m["c26"] * p for p in path]
        if rng.random() < 0.45:                        # a reprocessing lowers the latest figure
            vals[-1] = vals[-2] * float(rng.uniform(0.86, 0.97))
        first = next((j for j, v in enumerate(vals) if v >= W.ADVISORY), None)
        if first is None:
            continue
        shown = [(start + j, v) for j, v in enumerate(vals) if j >= first]
        mv = x["move"].get(m["district"])
        for mo, v in shown:
            d = dt.date(2026, mo + 1, int(rng.integers(3, 12))) if mo < 9 else dt.date(2026, 9, 29)
            after = mv is not None and (2026, mo) >= (mv[0], mv[1])
            # the carrier opened a new claimant file when the member's id changed, and carried the claims to date
            ref, no = (m["mid2"], cno2) if after else (m["mid"], cno)
            first_of_no = not any(r[1] == no for r in rows)
            rows.append((d.isoformat(), no, pol[m["district"]][2026], ref, "%.2f" % v,
                         "initial" if first_of_no else "update"))
        x["adv_truth"].setdefault(m["district"], []).append(round(shown[-1][1], 2))
    rows.sort(key=lambda r: (r[0], r[1]))
    return rows


def rebate_rows(x):
    rng = np.random.default_rng(W.SEED + 5)
    rows = []
    for did in W.IDS:
        rx = sum(v for (d, ym, c), v in x["paid"].items() if d == did and c == "Pharmacy" and ym[0] == 2025)
        for q, cred in (("2025Q1", "2025-08-12"), ("2025Q2", "2025-11-11"), ("2025Q3", "2026-02-10"),
                        ("2025Q4", "2026-05-12")):
            rows.append((did, q, "%.2f" % (rx / 4 * float(rng.uniform(0.17, 0.23))), cred))
    return rows


def receipt_rows(x):
    """Contributions billed and received by district and month, the districts' fiscal 2026 (July 2025 to June
    2026), on the 2025 and 2026 rates."""
    rng = np.random.default_rng(W.SEED + 6)
    rows = []
    for did in W.IDS:
        r25 = x["rates"][did] / W.TREND * float(rng.uniform(1.21, 1.25))
        r26 = x["rates"][did] * float(rng.uniform(1.21, 1.25))
        for ym in [(2025, m) for m in range(7, 13)] + [(2026, m) for m in range(1, 7)]:
            mm = W.member_months(x, did, [ym])
            billed = round(mm * (r25 if ym[0] == 2025 else r26), 2)
            got = billed if rng.random() > 0.04 else round(billed * float(rng.uniform(0.6, 0.95)), 2)
            day = dt.date(ym[0], ym[1], int(rng.integers(5, 21)))
            rows.append((did, "FY2026", "%d-%02d" % ym, "%.2f" % billed, "%.2f" % got, day.isoformat()))
    return rows


def survey_rows():
    return [
        ("PPO", "under $1,000", 41, "612.40", "86"),
        ("PPO", "$1,000 to $1,999", 57, "566.85", "84"),
        ("PPO", "$2,000 to $2,999", 23, "531.10", "83"),
        ("HDHP", "$3,000 and over", 34, "497.25", "81"),
        ("EPO", "under $1,000", 12, "640.90", "88"),
    ]
