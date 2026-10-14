"""The main call from the shipped pack: the register, the legacy payroll, Schedule B, Schedule A and the staffing plan
read back from target/, and the golden and every rung computed on them (calc.py)."""
from __future__ import annotations

import csv
import datetime as dt
import os

import openpyxl

import calc as CA
import claims as C
import common as K

CLASS_KEY = {v: k for k, v in K.CLASS_NAME.items()}


def _d(s):
    return dt.date.fromisoformat(s) if s else None


def _f(s):
    return float(s) if s not in ("", None) else None


def load_register(target):
    rows = []
    with open(os.path.join(target, K.REGISTER), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            rows.append(dict(claim_no=r["claim_no"], incident_no=r["incident_no"], defendant_seq=int(r["defendant_seq"]),
                             clinician_id=r["clinician_id"], defendant_role=r["defendant_role"],
                             specialty=r["specialty"], coverage_line=r["coverage_line"],
                             entity_at_incident=r["entity_at_incident"], incident_date=_d(r["incident_date"]),
                             claim_made_date=_d(r["claim_made_date"]), matter_type=r["matter_type"],
                             allegation=r["allegation"],
                             status=r["status"], closed_date=_d(r["closed_date"]),
                             indemnity_paid=_f(r["indemnity_paid"]), defense_paid=_f(r["defense_paid"]),
                             indemnity_reserve=_f(r["indemnity_reserve"]), defense_reserve=_f(r["defense_reserve"]),
                             prior_claim_no=r["prior_claim_no"]))
    return rows


def schedule_b():
    """Job code (either set) to class key, as Schedule B lists them."""
    out = {}
    for j in K.JOBS:
        if j[4]:
            out[j[1]] = j[4]
            out[j[2]] = j[4]
    return out


def load_payroll(target):
    """job[(employee, YYYY-MM)] and the experience FTE-years by (entity of the cost centre, class): all covered months
    2017 to 2024, the mature years 2017 to 2020, and the July 2016 code set alone (the whole experience, asserted)."""
    sb = schedule_b()
    job, Ee, Eem, Ee20 = {}, {}, {}, {}
    new_codes = {j[2] for j in K.JOBS}
    add = lambda d, key, v: d.__setitem__(key, d.get(key, 0.0) + v)
    with open(os.path.join(target, K.PAYROLL), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            job.setdefault((r["employee_id"], r["pay_month"]), r["job_code"])
            y = int(r["pay_month"][:4])
            k = sb.get(r["job_code"])
            if k and 2017 <= y <= 2024:
                f = float(r["fte"]) / 12.0
                key = (r["entity_code"], k)
                add(Ee, key, f)
                if y <= 2020:
                    add(Eem, key, f)
                if r["job_code"] in new_codes:
                    add(Ee20, key, f)
    return job, Ee, Eem, Ee20


def load_plan(target):
    wb = openpyxl.load_workbook(os.path.join(target, K.PLAN), data_only=True)
    ws = wb["Covered FTE 2027"]
    plan = {}
    for row in ws.iter_rows(min_row=6, values_only=True):
        if not row[0]:
            continue
        plan[(row[0], CLASS_KEY[row[2]])] = [float(v) for v in row[3:15]]
    return plan


def transitions():
    return {e: K.ENTITIES[e]["transition"] for e in K.ENTITY_ORDER}


def experience(target, rows=None, payroll=None):
    rows = rows if rows is not None else load_register(target)
    job, Ee, Eem, Ee20 = payroll if payroll is not None else load_payroll(target)
    code_to_key = {}
    for j in K.JOBS:
        code_to_key[j[1]] = j[0]
        code_to_key[j[2]] = j[0]
    job_of = lambda cid, d: code_to_key.get(job.get((cid, K.month_key(d.year, d.month))))
    ex = C.experience_from_rows(rows, job_of=job_of)
    return ex, Ee, Eem, Ee20


def payments(total, plan, tr):
    """Each entity's share of the Contribution under the funding policy's section 2: in proportion to its share of the
    Plan Year's exposure under 3.3 (the staffing plan's FTE-years from its Transition Date)."""
    X = CA.fte_years(plan, tr, K.ENTITY_ORDER, K.CLASSES)
    ex = {e: sum(v for (ee, k), v in X.items() if ee == e) for e in K.ENTITY_ORDER}
    allx = sum(ex.values())
    return {e: total * ex[e] / allx for e in K.ENTITY_ORDER}, ex


def main_call(target):
    rows = load_register(target)
    pay = load_payroll(target)
    ex, Ee, Eem, Ee20 = experience(target, rows, pay)
    plan = load_plan(target)
    tr = transitions()
    cl, en = K.CLASSES, K.ENTITY_ORDER
    rv, gold, pooled, own = CA.rivals(ex, Ee, Eem, plan, tr, cl, en)
    exP = CA.program(ex)
    P = list(CA.PROGRAM)
    EP, EA = CA.basis(Ee, P, cl), CA.basis(Ee, en, cl)
    months = CA.by_month(exP, EP, plan, tr, cl, en)
    grid = {("program",) + k: v for k, v in CA.grid(exP, EP, plan, tr, cl, en).items()}
    grid.update({("pooled",) + k: v for k, v in CA.grid(ex, EA, plan, tr, cl, en).items()})
    ent = {e: dict(cost=sum(v["cost"] for (ee, k), v in gold.items() if ee == e),
                   count=sum(v["count"] for (ee, k), v in gold.items() if ee == e),
                   fte_years=sum(v["fte_years"] for (ee, k), v in gold.items() if ee == e)) for e in en}
    total = rv["golden"]
    count = sum(v["count"] for v in gold.values())
    pay_e, expo = payments(total, plan, tr)
    return dict(rows=rows, ex=ex, exP=exP, Ee=Ee, Eem=Eem, Ee20=Ee20, EP=EP, EA=EA, plan=plan, rivals=rv, gold=gold,
                pooled=pooled, own=own, ent=ent, months=months, grid=grid, total=total, count=count, pay=pay_e,
                expo=expo)
