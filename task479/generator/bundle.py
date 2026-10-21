"""Read the cut pack the way an analyst would, and run every route the design names on it. Nothing here reads
world.py's truth; golden.py, checks.py, verify.py and ceiling.py all go through it.

    load(target)               the conformed eligibility, claims lag cells, reimbursements and the elections
    experience(b)              each employer's retained claims PMPM by plan year, trended to 2027
    expected(b, route)         each employer's expected 2027 retained PMPM under a route
    surcharged(b, est)         the employers over the claims component of their 2027 contribution
    ask_a(b, persons)          July to September 2026 member months by employer
    ask_b(b, persons)          members on the 2026 high-cost claimant report and their claims to date by employer"""
import csv
import os

FILES = {
    "enroll": "hallam_eligibility_member_months_2023-01_to_2026-09.csv",
    "lag_old": "hallam_claims_lag_report_paid_2023-01_to_2026-05.csv",
    "lag_new": "hallam_claims_lag_report_paid_2026-05_to_2026-09.csv",
    "reimb": "westerby_specific_reimbursements_2023-2025.csv",
    "hcc": "hallam_high_cost_claimant_report_2026.csv",
    "policy": "westerby_specific_policy_schedule_2023-2027.csv",
    "rates": "crbht_2027_contribution_elections.xlsx",
}
YEARS = (2023, 2024, 2025)
TREND = 0.07
SHRINK = ("buhlmann_straub", "complement_simple_mean", "limited_fluctuation_1000", "limited_fluctuation_2000",
          "limited_fluctuation_3000", "buhlmann_straub_leveraged")
ROUTES = ("golden",) + SHRINK[1:] + ("own_experience", "own_2025", "trust_level")


def _csv(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def _ym(s):
    if "/" in s:
        m, y = s.split("/")
    else:
        y, m = s.split("-")
    return int(y), int(m)


def load(target):
    import openpyxl
    enroll = _csv(os.path.join(target, FILES["enroll"]))
    cells = {}
    for r in _csv(os.path.join(target, FILES["lag_old"])):
        cells[(r["EmployerNo"], _ym(r["IncurredMonth"]), _ym(r["PaidMonth"]), r["Category"])] = float(r["PaidAmount"])
    for r in _csv(os.path.join(target, FILES["lag_new"])):
        k = (r["employer_code"], _ym(r["incurred_period"]), _ym(r["paid_period"]),
             "Medical" if r["benefit_type"] == "MED" else "Pharmacy")
        cells[k] = int(r["plan_paid_cents"]) / 100.0     # May 2026 sent by both platforms: one cell, as a key
    pol = {(r["policy_no"], int(r["contract_year"])): r["employer_id"]
           for r in _csv(os.path.join(target, FILES["policy"]))}
    reimb = _csv(os.path.join(target, FILES["reimb"]))
    hcc = _csv(os.path.join(target, FILES["hcc"]))
    ws = openpyxl.load_workbook(os.path.join(target, FILES["rates"]), data_only=True)["2027 elections"]
    rates = {r[0]: float(r[3]) for r in ws.iter_rows(min_row=5, values_only=True) if r[0] and str(r[0]).startswith("CR")}
    ids = sorted(rates)
    mm = {}
    for r in enroll:
        y = int(r["coverage_month"][:4])
        if y in YEARS:
            mm[(r["employer_id"], y)] = mm.get((r["employer_id"], y), 0) + 1
    paid = {}
    for (e, inc, pd, cat), amt in cells.items():
        if inc[0] in YEARS and pd <= (inc[0] + 1, 3):
            paid[(e, inc[0])] = paid.get((e, inc[0]), 0.0) + amt
    return {"enroll": enroll, "cells": cells, "pol": pol, "reimb": reimb, "hcc": hcc, "rates": rates, "ids": ids,
            "mm": mm, "paid": paid}


def experience(b, leveraged=False):
    """Per employer and plan year: member months, plan-paid claims (incurred in the year, paid through March of the
    next), Westerby's reimbursements, retained claims, and the retained PMPM trended to 2027. leveraged trends each
    claimant's claims before the $150,000 deductible instead of trending the retained total."""
    out = {}
    re = {}
    for r in b["reimb"]:
        y = int(r["contract_year"])
        e = b["pol"][(r["policy_no"], y)]
        re.setdefault((e, y), []).append((float(r["paid_in_contract_year"]), float(r["reimbursed"]),
                                           float(r["specific_deductible"])))
    for e in b["ids"]:
        for y in YEARS:
            f = (1 + TREND) ** (2027 - y)
            mm = b["mm"][(e, y)]
            paid = b["paid"].get((e, y), 0.0)
            rb = sum(v for p, v, d in re.get((e, y), []))
            ret = paid - rb
            if leveraged:
                x = (f * paid - sum(max(0.0, f * p - d) for p, v, d in re.get((e, y), []))) / mm
            else:
                x = ret * f / mm
            out[(e, y)] = {"mm": mm, "paid": paid, "reimb": rb, "ret": ret, "x": x}
    return out


def credibility(b, ex, form="buhlmann_straub", n_full=2000):
    ids = b["ids"]
    X = [[ex[(e, y)]["x"] for y in YEARS] for e in ids]
    W = [[ex[(e, y)]["mm"] for y in YEARS] for e in ids]
    wi = [sum(w) for w in W]
    xi = [sum(a * c for a, c in zip(xr, wr)) / s for xr, wr, s in zip(X, W, wi)]
    tot = sum(wi)
    xbar = sum(a * c for a, c in zip(xi, wi)) / tot
    r, t = len(ids), len(YEARS)
    epv = sum(w * (v - m) ** 2 for xr, wr, m in zip(X, W, xi) for v, w in zip(xr, wr)) / (r * (t - 1))
    vhm = (sum(w * (m - xbar) ** 2 for m, w in zip(xi, wi)) - (r - 1) * epv) / (tot - sum(w * w for w in wi) / tot)
    k = epv / vhm
    if form == "limited_fluctuation":
        z = [min(1.0, (w / t / 12 / n_full) ** 0.5) for w in wi]
    else:
        z = [w / (w + k) for w in wi]
    if form == "complement_simple_mean":
        xbar = sum(xi) / r
    est = {e: xbar + zz * (m - xbar) for e, zz, m in zip(ids, z, xi)}
    return {"est": est, "z": dict(zip(ids, z)), "xbar": xbar, "k": k, "own": dict(zip(ids, xi)), "epv": epv,
            "vhm": vhm}


def expected(b, route="golden"):
    ex = experience(b, leveraged=(route == "buhlmann_straub_leveraged"))
    if route in ("golden", "buhlmann_straub", "buhlmann_straub_leveraged"):
        return credibility(b, ex)["est"]
    if route == "complement_simple_mean":
        return credibility(b, ex, "complement_simple_mean")["est"]
    if route.startswith("limited_fluctuation"):
        return credibility(b, ex, "limited_fluctuation", int(route.rsplit("_", 1)[1]))["est"]
    c = credibility(b, ex)
    if route == "own_experience":
        return c["own"]
    if route == "own_2025":
        return {e: ex[(e, 2025)]["x"] for e in b["ids"]}
    if route == "trust_level":
        return {e: c["xbar"] for e in b["ids"]}


def surcharged(b, est):
    return sorted(e for e in est if est[e] > b["rates"][e])


# ------------------------------------------------------------------------------------------------ ask A
def persons(b):
    """Member id to one person key: the employer, birth date, sex and relationship (unique within an employer)."""
    return {r["member_id"]: (r["employer_id"], r["birth_date"], r["sex"], r["relationship"]) for r in b["enroll"]}


def ask_a(b, by_person=True):
    """July to September 2026 member months: a person enrolled in the month, counted once."""
    pk = persons(b)
    seen = set()
    mm = {e: 0 for e in b["ids"]}
    for r in b["enroll"]:
        if not ("2026-07" <= r["coverage_month"] <= "2026-09"):
            continue
        key = (pk[r["member_id"]], r["coverage_month"]) if by_person else (r["member_id"], r["coverage_month"])
        if key in seen:
            continue
        seen.add(key)
        mm[r["employer_id"]] += 1
    return mm


# ------------------------------------------------------------------------------------------------ ask B
def ask_b(b, by_person=True):
    """Members on the 2026 high-cost claimant report by employer and their claims to date as last reported; by_person
    links a member's rows under the new id to the rows under the old one."""
    pk = persons(b)
    last = {}
    for r in sorted(b["hcc"], key=lambda r: r["report_month"]):
        who = pk[r["member_id"]] if by_person else r["member_id"]
        last[(r["employer_id"], who)] = float(r["paid_ytd"])
    out = {e: [0, 0.0] for e in b["ids"]}
    for (e, who), v in last.items():
        out[e][0] += 1
        out[e][1] += v
    return {e: tuple(v) for e, v in out.items()}
