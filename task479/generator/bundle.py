"""Read the cut pack the way an analyst would, and run every route the design names on it. Nothing here reads
world.py's truth; golden.py, checks.py, verify.py and ceiling.py all go through it.

    load(target)            the conformed eligibility, claims lag cells, designs, the carrier's records and the rates
    expected(b, route)      each district's expected plan year 2026 plan-paid PMPM under a route
    raised(b, est)          the districts over the claims component of their 2026 contribution rate
    ask_a(b, persons)       July to September 2026 member months by district
    ask_b(b, persons)       2026 advisory members and their claims to date by district"""
import csv
import os
import re

FILES = {
    "enroll": "tollard_eligibility_member_months_2025-01_to_2026-09.csv",
    "lag_old": "tollard_claims_lag_report_paid_2025-01_to_2026-05.csv",
    "lag_new": "tollard_claims_lag_report_paid_2026-05_to_2026-09.csv",
    "adv": "granfield_specific_advisories_2026.csv",
    "policy": "granfield_specific_policy_schedule_2025-2027.csv",
    "rates": "mvshc_2026_contribution_rates.xlsx",
    "benefits": "mvshc_benefit_designs_2025_2026.pdf",
}
ROUTES = ("golden", "default", "pooled", "annualised", "mean_of_ratios", "paid_share")
H1 = [(2026, m) for m in range(1, 7)]
Y25 = [(2025, m) for m in range(1, 13)]


def _csv(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def _ym(s):
    if "/" in s:
        m, y = s.split("/")
    else:
        y, m = s.split("-")
    return int(y), int(m)


def designs(target):
    """The calendar-year deductible of each district's plan in 2025 and 2026, from the benefit designs PDF's table
    (district id, plan year, plan code, deductible)."""
    import pypdf
    txt = " ".join(p.extract_text() for p in pypdf.PdfReader(os.path.join(target, FILES["benefits"])).pages)
    out = {}
    for did, yr, code, ded in re.findall(r"(MV\d\d)\s+(2025|2026)\s+(MV[ABC])\s+\$([\d,]+)", txt):
        out[(did, int(yr))] = int(ded.replace(",", ""))
    return out


def load(target):
    import openpyxl
    enroll = _csv(os.path.join(target, FILES["enroll"]))
    cells = {}
    for r in _csv(os.path.join(target, FILES["lag_old"])):
        k = (r["DistrictID"], _ym(r["IncurredMonth"]), _ym(r["PaidMonth"]), r["Category"])
        cells[k] = float(r["PaidAmount"])
    for r in _csv(os.path.join(target, FILES["lag_new"])):
        k = (r["district_code"], _ym(r["incurred_period"]), _ym(r["paid_period"]),
             "Medical" if r["benefit_type"] == "MED" else "Pharmacy")
        cells[k] = int(r["plan_paid_cents"]) / 100.0     # May 2026 sent by both platforms: one cell, as a key
    adv = _csv(os.path.join(target, FILES["adv"]))
    pol = {(r["policy_no"], int(r["contract_year"])): r["district_id"]
           for r in _csv(os.path.join(target, FILES["policy"]))}
    ws = openpyxl.load_workbook(os.path.join(target, FILES["rates"]), data_only=True)["2026 rates"]
    rates = {r[0]: float(r[3]) for r in ws.iter_rows(min_row=5, values_only=True) if r[0] and str(r[0]).startswith("MV")}
    ids = sorted(rates)
    mm = {}
    for r in enroll:
        ym = _ym(r["coverage_month"])
        if ym[0] == 2025 or ym in H1:
            mm[(r["district_id"], ym)] = mm.get((r["district_id"], ym), 0) + 1
    paid = {}
    for (d, inc, pd, cat), amt in cells.items():
        paid[(d, inc)] = paid.get((d, inc), 0.0) + amt
    return {"enroll": enroll, "cells": cells, "adv": adv, "pol": pol, "rates": rates, "ids": ids, "mm": mm,
            "paid": paid, "design": designs(target)}


def _s(b, d, months, what):
    src = b["mm"] if what == "mm" else b["paid"]
    return sum(src.get((d, ym), 0) for ym in months)


def factor(b, ids):
    """The ratio of the plan year 2025 PMPM to the January to June 2025 PMPM, pooled over the districts given."""
    fy = sum(_s(b, i, Y25, "paid") for i in ids) / sum(_s(b, i, Y25, "mm") for i in ids)
    h = sum(_s(b, i, Y25[:6], "paid") for i in ids) / sum(_s(b, i, Y25[:6], "mm") for i in ids)
    return fy / h


def h1(b, d):
    return _s(b, d, H1, "paid") / _s(b, d, H1, "mm")


def expected(b, route="golden"):
    """Each district's expected plan year 2026 plan-paid PMPM. golden: its January to June 2026 PMPM completed by the
    plan-year factor of the districts that ran its 2026 design through 2025; default: by its own 2025 factor;
    pooled: by every district's; annualised: the January to June PMPM as it stands; mean_of_ratios and paid_share:
    other forms of the golden."""
    out = {}
    for d in b["ids"]:
        dz = b["design"][(d, 2026)]
        same = [i for i in b["ids"] if b["design"][(i, 2025)] == dz]
        if route == "golden":
            v = h1(b, d) * factor(b, same)
        elif route == "default":
            v = h1(b, d) * factor(b, [d])
        elif route == "pooled":
            v = h1(b, d) * factor(b, b["ids"])
        elif route == "annualised":
            v = h1(b, d)
        elif route == "mean_of_ratios":
            v = h1(b, d) * sum(factor(b, [i]) for i in same) / len(same)
        elif route == "paid_share":
            sh = sum(_s(b, i, Y25, "paid") for i in same) / sum(_s(b, i, Y25[:6], "paid") for i in same)
            v = _s(b, d, H1, "paid") * sh / (2 * _s(b, d, H1, "mm"))
        out[d] = v
    return out


def raised(b, est):
    return sorted(d for d in est if est[d] > b["rates"][d])


def factors_by_design(b):
    return {dz: factor(b, [i for i in b["ids"] if b["design"][(i, 2025)] == dz]) for dz in (500, 1500, 3000)}


# ------------------------------------------------------------------------------------------------ ask A
def persons(b):
    """Member id to one person key: the district, birth date, sex and relationship (unique within a district)."""
    return {r["member_id"]: (r["district_id"], r["birth_date"], r["sex"], r["relationship"]) for r in b["enroll"]}


def ask_a(b, by_person=True):
    """July to September 2026 member months: a person enrolled in the district's plan in the month, counted once."""
    pk = persons(b)
    seen = set()
    mm = {d: 0 for d in b["ids"]}
    for r in b["enroll"]:
        ym = _ym(r["coverage_month"])
        if not ((2026, 7) <= ym <= (2026, 9)):
            continue
        key = (pk[r["member_id"]], ym) if by_person else (r["member_id"], ym)
        if key in seen:
            continue
        seen.add(key)
        mm[r["district_id"]] += 1
    return mm


# ------------------------------------------------------------------------------------------------ ask B
def ask_b(b, by_person=True, take="latest"):
    """2026 specific advisories by district: the members the carrier has flagged and their claims to date as it last
    reported them. by_person links a claimant file opened under a member's new id to the person's earlier file."""
    pk = persons(b)
    last = {}
    for r in sorted(b["adv"], key=lambda r: (r["advisory_date"], r["claimant_no"])):
        d = b["pol"][(r["policy_no"], 2026)]
        who = pk[r["member_ref"]] if by_person else r["claimant_no"]
        v = float(r["incurred_to_date"])
        if take == "latest":
            last[(d, who)] = v
        elif take == "max":
            last[(d, who)] = max(v, last.get((d, who), 0.0))
        elif take == "sum":
            last[(d, who)] = last.get((d, who), 0.0) + v
    out = {d: [0, 0.0] for d in b["ids"]}
    for (d, who), v in last.items():
        out[d][0] += 1
        out[d][1] += v
    return {d: tuple(v) for d, v in out.items()}
