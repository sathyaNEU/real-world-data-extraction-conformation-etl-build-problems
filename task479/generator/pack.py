"""The pack's data files, written from the truth in world.py: Marlowe's enrollment file, its claims lag reports in two
layouts across the June 2026 platform upgrade, Arbor Ridge's 2025 large claimant report and 2026 specific advisories,
the stop-loss policy schedule, the group roster, the rebate statement and the industry benchmark."""
import calendar
import csv
import datetime as dt

import numpy as np

import world as W

FILES = {
    "enroll": "mba_enrollment_member_months_2025-01_to_2026-08.csv",
    "lag_old": "mba_claims_lag_report_paid_2025-01_to_2026-05.csv",
    "lag_new": "mba_claims_lag_report_paid_2026-06_to_2026-09.csv",
    "lcr": "arbor_ridge_large_claimant_report_cy2025.csv",
    "adv": "arbor_ridge_specific_advisories_2026.csv",
    "policy": "arbor_ridge_specific_policy_schedule_2025-2027.csv",
    "roster": "mba_group_roster_2026-10.csv",
    "rates": "mba_2027_funding_elections.xlsx",
    "memo": "mba_2027_renewal_assumptions.pdf",
    "rebates": "mba_pharmacy_rebate_statement_2025.csv",
    "bench": "midwest_employer_health_cost_survey_2025.csv",
    "dictionary": "mba_data_dictionary.csv",
    "manifest": "mba_extract_manifest_2026-10-05.csv",
}
COMPANY = "Marlowe Benefit Administrators"
CARRIER = "Arbor Ridge Specialty Insurance Company"
EXTRACT = dt.datetime(2026, 10, 5, 6, 30)

ENROLL_COLS = ["member_id", "subscriber_id", "relationship", "birth_date", "sex", "group_no", "coverage_month",
               "coverage_tier"]
LAG_OLD_COLS = ["GroupNo", "IncurredMonth", "PaidMonth", "Category", "PaidAmount", "ClaimLines"]
LAG_NEW_COLS = ["group_id", "incurred_period", "paid_period", "benefit_type", "paid_cents", "line_count"]
LCR_COLS = ["claimant_no", "policy_no", "member_ref", "relationship", "birth_year", "incurred_medical",
            "incurred_pharmacy", "total_incurred", "specific_deductible", "eligible_excess", "reimbursed_to_date",
            "open_balance"]
ADV_COLS = ["advisory_date", "claimant_no", "policy_no", "member_ref", "incurred_to_date", "advisory_type"]
POLICY_COLS = ["policy_no", "group_no", "contract_year", "effective", "expires", "contract_basis",
               "specific_deductible", "aggregate_corridor_pct"]
ROSTER_COLS = ["group_no", "employer", "industry", "renewal_month", "funding_arrangement", "account_manager"]
REBATE_COLS = ["group_no", "quarter", "rebate_amount", "credited_on"]
BENCH_COLS = ["industry", "plan_type", "employers", "median_pmpm_2025", "p75_pmpm_2025"]


def write_csv(path, cols, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\r\n")
        w.writerow(cols)
        for r in rows:
            w.writerow(["" if v is None else v for v in r])
    return len(rows)


def ids(x):
    """TPA member and subscriber ids; the employers that changed payroll vendor in 2026 had their members reissued
    under new ids from the change month, the old ids left on file for one to three months after (the Ask A device)."""
    rng = np.random.default_rng(W.SEED + 1)
    order = rng.permutation(len(x["members"]))
    for i, j in enumerate(order):
        m = x["members"][j]
        m["mid"] = "M%07d" % (2210457 + 13 * i)
    subs = {}
    for m in x["members"]:
        key = (m["group"], m["sub"])
        if key not in subs:
            subs[key] = "S%06d" % (310000 + int(rng.integers(0, 600000)))
        m["sid"] = subs[key]
    x["vendor_change"] = {}
    for gno in ("G1041", "G1052", "G1063", "G1074", "G1085", "G1096", "G1107", "G1118", "G1130", "G1141", "G1152", "G1163", "G1174",
                "G1196"):
        x["vendor_change"][gno] = (2026, int(rng.integers(5, 8)), int(rng.integers(1, 3)))
    for m in x["members"]:
        if m["group"] in x["vendor_change"]:
            m["mid2"] = "M%07d" % (5400003 + 11 * m["k"])
            m["sid2"] = "S%06d" % (900000 + int(m["sid"][1:]) % 99991)


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
        fams.setdefault((m["group"], m["sub"]), []).append(m)
    rows = []
    for m in x["members"]:
        t = tier(fams[(m["group"], m["sub"])])
        vc = x["vendor_change"].get(m["group"])
        for ym in W.MONTHS25 + W.MONTHS26:
            if not (m["start"] <= ym <= m["end"]):
                continue
            ymS = "%d-%02d" % ym
            if vc and ym >= (vc[0], vc[1]):
                rows.append((m["mid2"], m["sid2"], m["rel"], m["birth"].isoformat(), m["sex"], m["group"], ymS, t))
                overlap_end = (vc[0], vc[1] + vc[2] - 1)
                if ym <= overlap_end:
                    rows.append((m["mid"], m["sid"], m["rel"], m["birth"].isoformat(), m["sex"], m["group"], ymS, t))
            else:
                rows.append((m["mid"], m["sid"], m["rel"], m["birth"].isoformat(), m["sex"], m["group"], ymS, t))
    rows.sort(key=lambda r: (r[6], r[5], r[0]))
    return rows


LAGS = [0.46, 0.33, 0.11, 0.05, 0.025, 0.012, 0.007, 0.004, 0.002]   # share of a month's claims paid k months later


def _months_after(y, m, k):
    t = y * 12 + m - 1 + k
    return t // 12, t % 12 + 1


def lag_cells(x):
    """Each group's claims by incurred month, paid month and category. 2025 incurred claims paid through March 2026
    are the experience (they equal the members' 2025 claims); a small tail paid from April 2026 on; 2024 incurred
    claims paid in early 2025; 2026 incurred claims through September 2026."""
    rng = np.random.default_rng(W.SEED + 2)
    cells = {}

    def add(g, inc, paid, cat, amt, lines):
        k = (g, inc, paid, cat)
        a = cells.setdefault(k, [0.0, 0])
        a[0] += amt
        a[1] += lines

    for gno, *_ in W.GROUPS:
        gm = [m for m in x["members"] if m["group"] == gno]
        for cat, key in (("Medical", "med25"), ("Pharmacy", "rx25")):
            tot = sum(m[key] for m in gm)
            # monthly incurred pattern, then the lag through March 2026 renormalised to the experience total
            w = rng.dirichlet(np.ones(12) * 40)
            for i, (y, mo) in enumerate(W.MONTHS25):
                inc_amt = tot * w[i]
                lags = []
                for k, s in enumerate(LAGS):
                    py, pm = _months_after(y, mo, k)
                    if (py, pm) <= (2026, 3):
                        lags.append((k, s))
                norm = sum(s for _, s in lags)
                for k, s in lags:
                    py, pm = _months_after(y, mo, k)
                    a = round(inc_amt * s / norm, 2)
                    add(gno, (y, mo), (py, pm), cat, a, max(1, int(a / (180 if cat == "Medical" else 75))))
                # the run-out paid after March 2026
                for k, s in enumerate(LAGS):
                    py, pm = _months_after(y, mo, k)
                    if (2026, 4) <= (py, pm) <= (2026, 9):
                        a = round(inc_amt * s * 0.6, 2)
                        add(gno, (y, mo), (py, pm), cat, a, max(1, int(a / 200)))
            # 2024 incurred, paid in 2025
            for mo in (10, 11, 12):
                inc_amt = tot / 12 * 0.95
                for k, s in enumerate(LAGS):
                    py, pm = _months_after(2024, mo, k)
                    if py == 2025:
                        add(gno, (2024, mo), (py, pm), cat, round(inc_amt * s, 2), max(1, int(inc_amt * s / 190)))
        # 2026 incurred, January to August, paid through September 2026
        for cat, share in (("Medical", 0.79), ("Pharmacy", 0.21)):
            tot26 = sum(m["c26"] for m in gm) * share
            w = rng.dirichlet(np.ones(8) * 40)
            for i, (y, mo) in enumerate(W.MONTHS26):
                inc_amt = tot26 * w[i]
                for k, s in enumerate(LAGS):
                    py, pm = _months_after(y, mo, k)
                    if (py, pm) <= (2026, 9):
                        a = round(inc_amt * s, 2)
                        add(gno, (y, mo), (py, pm), cat, a, max(1, int(a / 180)))
    # make the 2025 experience equal the members' claims to the cent, group and category
    for gno, *_ in W.GROUPS:
        gm = [m for m in x["members"] if m["group"] == gno]
        for cat, key in (("Medical", "med25"), ("Pharmacy", "rx25")):
            want = round(sum(m[key] for m in gm), 2)
            ks = sorted(k for k in cells if k[0] == gno and k[3] == cat and k[1][0] == 2025 and k[2] <= (2026, 3))
            have = round(sum(cells[k][0] for k in ks), 2)
            cells[ks[0]][0] = round(cells[ks[0]][0] + want - have, 2)
    x["lag"] = cells
    return cells


def lag_rows(x, layout):
    cells = x["lag"]
    rows = []
    for (g, inc, paid, cat), (amt, lines) in sorted(cells.items()):
        if layout == "old" and paid <= (2026, 5):
            rows.append((g, "%02d/%d" % (inc[1], inc[0]), "%02d/%d" % (paid[1], paid[0]), cat, "%.2f" % amt, lines))
        if layout == "new" and paid >= (2026, 5):
            # the new platform's first export carried May 2026 again, as the old platform had sent it
            rows.append((g, "%d-%02d" % inc, "%d-%02d" % paid, "MED" if cat == "Medical" else "RX",
                         int(round(amt * 100)), lines))
    return rows


def policies():
    """Each group's specific policy number by contract year; five groups were rewritten at the 2026 renewal."""
    out = {}
    rew = {"G1052", "G1085", "G1129", "G1163", "G1196"}
    for i, (gno, *_) in enumerate(W.GROUPS):
        a = "ARS-SL-%05d" % (40211 + 17 * i)
        b = "ARS-SL-%05d" % (51907 + 23 * i) if gno in rew else a
        out[gno] = {2025: a, 2026: b, 2027: b}
    return out


def policy_rows():
    pol = policies()
    rows = []
    for gno, *_ in W.GROUPS:
        for y in (2025, 2026, 2027):
            rows.append((pol[gno][y], gno, y, "%d-01-01" % y, "%d-12-31" % y, "12/15", W.ATTACH, 125))
    return rows


def lcr_rows(x):
    """The carrier's 2025 large claimant report: every member with $100,000 or more of 2025 incurred claims paid
    through March 2026 (the 12/15 contract)."""
    rng = np.random.default_rng(W.SEED + 3)
    pol = policies()
    rows = []
    big = sorted((m for m in x["members"] if m["c25"] >= 100_000), key=lambda m: m["k"])
    for i, m in enumerate(big):
        exc = max(0.0, m["c25"] - W.ATTACH)
        paid = round(exc * float(rng.choice([1.0, 1.0, 0.82, 0.64, 0.0])), 2) if exc else 0.0
        rows.append(("ARS-25-%05d" % (10441 + 7 * i), pol[m["group"]][2025], m["mid"], m["rel"], m["birth"].year,
                     "%.2f" % m["med25"], "%.2f" % m["rx25"], "%.2f" % m["c25"], W.ATTACH, "%.2f" % exc, "%.2f" % paid,
                     "%.2f" % (exc - paid)))
    return rows


def adv_rows(x):
    """The carrier's 2026 specific advisories: a row each month for every claimant at or over the 50 per cent
    threshold, restating the claimant's 2026 incurred claims to date (claims reprocessed later can lower it)."""
    rng = np.random.default_rng(W.SEED + 4)
    pol = policies()
    rows = []
    x["adv_truth"] = {}
    cand = sorted((m for m in x["members"] if m["c26"] >= W.ADVISORY), key=lambda m: m["k"])
    for i, m in enumerate(cand):
        cno = "ARS-26-%05d" % (20117 + 9 * i)
        start = int(rng.integers(2, 5))
        path = np.sort(rng.uniform(0.55, 1.0, 9 - start))
        path[-1] = 1.0
        vals = [m["c26"] * p for p in path]
        if rng.random() < 0.45 and len(vals) > 1:        # a reprocessing lowers the latest figure
            vals[-1] = vals[-2] * float(rng.uniform(0.86, 0.97))
        first = next((j for j, v in enumerate(vals) if v >= W.ADVISORY), None)
        if first is None:
            continue
        shown = [(start + j, v) for j, v in enumerate(vals) if j >= first]
        vc = x["vendor_change"].get(m["group"])
        cno2 = "ARS-26-%05d" % (60119 + 9 * i)
        for mo, v in shown:
            d = dt.date(2026, mo + 1, int(rng.integers(3, 12))) if mo < 9 else dt.date(2026, 9, 28)
            after = vc is not None and (2026, mo) >= (vc[0], vc[1])
            # the carrier opened a new claimant file when the member's id changed, and carried the claims to date
            ref, no = (m["mid2"], cno2) if after else (m["mid"], cno)
            first_of_no = not any(r[1] == no for r in rows)
            rows.append((d.isoformat(), no, pol[m["group"]][2026], ref, "%.2f" % v,
                         "initial" if first_of_no else "update"))
        x["adv_truth"].setdefault(m["group"], []).append(round(shown[-1][1], 2))
    rows.sort(key=lambda r: (r[0], r[1]))
    return rows


MANAGERS = ["Andrea Snow", "Brady Cooper", "Chelsea Petersen", "James Hernandez"]


def roster_rows():
    rows = []
    for i, (gno, emp, ind, *_) in enumerate(W.GROUPS):
        rows.append((gno, emp, ind, "January", "self-funded with specific stop-loss", MANAGERS[i % 4]))
    return rows


def rebate_rows(x):
    rng = np.random.default_rng(W.SEED + 5)
    rows = []
    for gno, *_ in W.GROUPS:
        rx = sum(m["rx25"] for m in x["members"] if m["group"] == gno)
        for q, cred in (("2025Q1", "2025-08-14"), ("2025Q2", "2025-11-13"), ("2025Q3", "2026-02-12"),
                        ("2025Q4", "2026-05-14")):
            rows.append((gno, q, "%.2f" % (rx / 4 * float(rng.uniform(0.16, 0.22))), cred))
    return rows


def bench_rows():
    rows = []
    for ind, emp, med in (("manufacturing", 212, 571.40), ("finance", 98, 498.10), ("health care", 143, 612.75),
                          ("transportation", 77, 603.20), ("food processing", 51, 556.90),
                          ("professional services", 166, 512.35), ("education", 120, 547.80), ("retail", 134, 529.60),
                          ("construction", 109, 588.15), ("hospitality", 88, 541.25), ("insurance", 61, 505.70)):
        rows.append((ind, "self-funded PPO", emp, "%.2f" % med, "%.2f" % (med * 1.24)))
    return rows
