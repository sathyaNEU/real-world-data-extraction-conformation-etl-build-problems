"""Read the cut pack the way an analyst would, and run every route the design names on it. Nothing here reads
world.py's truth; golden.py, checks.py, verify.py and ceiling.py all go through it.

    load(target)            the conformed enrollment, claims lag cells, the carrier's records and the elections
    retained27(b, route)    each group's expected 2027 retained claims PMPM under a route
    notices(b, est)         the groups over the claims component of their 2027 funding rate
    ask_a(b, persons)       January to August 2026 member months and paid claims PMPM by group
    ask_b(b, persons)       2026 advisory members and their claims to date by group"""
import csv
import os

FILES = {
    "enroll": "mba_enrollment_member_months_2025-01_to_2026-08.csv",
    "lag_old": "mba_claims_lag_report_paid_2025-01_to_2026-05.csv",
    "lag_new": "mba_claims_lag_report_paid_2026-06_to_2026-09.csv",
    "lcr": "arbor_ridge_large_claimant_report_cy2025.csv",
    "adv": "arbor_ridge_specific_advisories_2026.csv",
    "policy": "arbor_ridge_specific_policy_schedule_2025-2027.csv",
    "rates": "mba_2027_funding_elections.xlsx",
}
ATTACH = 250_000
F = 1.075 ** 2
ROUTES = ("golden", "default", "partial", "gross", "golden_runout", "default_reimbursed", "golden_rebates")


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
        k = (r["GroupNo"], _ym(r["IncurredMonth"]), _ym(r["PaidMonth"]), r["Category"])
        cells[k] = float(r["PaidAmount"])
    for r in _csv(os.path.join(target, FILES["lag_new"])):
        k = (r["group_id"], _ym(r["incurred_period"]), _ym(r["paid_period"]),
             "Medical" if r["benefit_type"] == "MED" else "Pharmacy")
        cells[k] = int(r["paid_cents"]) / 100.0          # May 2026 sent by both platforms: one cell, as a key
    lcr = _csv(os.path.join(target, FILES["lcr"]))
    adv = _csv(os.path.join(target, FILES["adv"]))
    pol = {(r["policy_no"], int(r["contract_year"])): r["group_no"] for r in _csv(os.path.join(target, FILES["policy"]))}
    ws = openpyxl.load_workbook(os.path.join(target, FILES["rates"]), data_only=True)["2027 elections"]
    rates = {r[0]: float(r[3]) for r in ws.iter_rows(min_row=2, values_only=True) if r[0]}
    groups = sorted(rates)
    rebates = {}
    for r in _csv(os.path.join(target, "mba_pharmacy_rebate_statement_2025.csv")):
        rebates[r["group_no"]] = rebates.get(r["group_no"], 0.0) + float(r["rebate_amount"])
    return {"enroll": enroll, "cells": cells, "lcr": lcr, "adv": adv, "pol": pol, "rates": rates, "groups": groups,
            "rebates": rebates}


def experience(b, runout=False):
    """Per group: 2025 member months (enrollment rows in 2025), 2025 incurred claims paid through March 2026."""
    mm, gross = {}, {}
    for r in b["enroll"]:
        if r["coverage_month"].startswith("2025"):
            mm[r["group_no"]] = mm.get(r["group_no"], 0) + 1
    for (g, inc, paid, cat), amt in b["cells"].items():
        if inc[0] == 2025 and (runout or paid <= (2026, 3)):
            gross[g] = gross.get(g, 0.0) + amt
    return mm, gross


def claimants(b):
    """Each group's 2025 large claimants' totals, by group through the 2025 policy number."""
    out = {}
    for r in b["lcr"]:
        g = b["pol"][(r["policy_no"], 2025)]
        out.setdefault(g, []).append((float(r["total_incurred"]), float(r["eligible_excess"]),
                                      float(r["reimbursed_to_date"])))
    return out


def retained27(b, route="golden"):
    mm, gross = experience(b, runout=(route == "golden_runout"))
    cl = claimants(b)
    out = {}
    for g in b["groups"]:
        c = cl.get(g, [])
        G = gross[g] - (b["rebates"][g] if route == "golden_rebates" else 0.0)
        if route in ("golden", "golden_runout", "golden_rebates"):
            v = F * G - sum(max(0.0, F * t - ATTACH) for t, e, p in c)
        elif route == "default":
            v = F * (G - sum(e for t, e, p in c))
        elif route == "default_reimbursed":
            v = F * (G - sum(p for t, e, p in c))
        elif route == "partial":
            v = F * G - sum(F * t - ATTACH for t, e, p in c if t >= ATTACH)
        elif route == "gross":
            v = F * G
        out[g] = v / mm[g]
    return out


def notices(b, est):
    return sorted(g for g in est if est[g] > b["rates"][g])


# ------------------------------------------------------------------------------------------------ ask A
def persons(b):
    """Member id to one person key: the group, birth date, sex and relationship (unique within a group)."""
    return {r["member_id"]: (r["group_no"], r["birth_date"], r["sex"], r["relationship"]) for r in b["enroll"]}


def ask_a(b, by_person=True):
    """January to August 2026: member months (a person enrolled in the month, counted once) and paid claims PMPM
    (2026 incurred January to August, paid through September 2026)."""
    pk = persons(b)
    seen = set()
    mm = {}
    for r in b["enroll"]:
        ym = _ym(r["coverage_month"])
        if ym[0] != 2026:
            continue
        key = (pk[r["member_id"]], ym) if by_person else (r["member_id"], ym)
        if key in seen:
            continue
        seen.add(key)
        mm[r["group_no"]] = mm.get(r["group_no"], 0) + 1
    paid = {}
    for (g, inc, pd, cat), amt in b["cells"].items():
        if inc[0] == 2026 and inc[1] <= 8:
            paid[g] = paid.get(g, 0.0) + amt
    return {g: (mm[g], paid[g] / mm[g]) for g in b["groups"]}


def ask_a_doubled_may(target, by_person=True):
    """Ask A with May 2026's paid cells taken from both platforms' files."""
    b = load(target)
    extra = {}
    for r in _csv(os.path.join(target, FILES["lag_old"])):
        inc, pd = _ym(r["IncurredMonth"]), _ym(r["PaidMonth"])
        if pd == (2026, 5) and inc[0] == 2026:
            extra[r["GroupNo"]] = extra.get(r["GroupNo"], 0.0) + float(r["PaidAmount"])
    a = ask_a(b, by_person)
    return {g: (a[g][0], a[g][1] + extra.get(g, 0.0) / a[g][0]) for g in a}


# ------------------------------------------------------------------------------------------------ ask B
def ask_b(b, by_person=True, take="latest"):
    """2026 specific advisories by group: the members the carrier has flagged and their claims to date as it last
    reported them. by_person links a claimant file opened under a member's new id to the person's earlier file."""
    pk = persons(b)
    last = {}
    for r in sorted(b["adv"], key=lambda r: (r["advisory_date"], r["claimant_no"])):
        g = b["pol"][(r["policy_no"], 2026)]
        who = pk[r["member_ref"]] if by_person else r["claimant_no"]
        v = float(r["incurred_to_date"])
        if take == "latest":
            last[(g, who)] = v
        elif take == "max":
            last[(g, who)] = max(v, last.get((g, who), 0.0))
        elif take == "sum":
            last[(g, who)] = last.get((g, who), 0.0) + v
    out = {g: [0, 0.0] for g in b["groups"]}
    for (g, who), v in last.items():
        out[g][0] += 1
        out[g][1] += v
    return {g: tuple(v) for g, v in out.items()}
