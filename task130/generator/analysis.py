"""The main call from the shipped pack: the register, the legacy payroll, Schedule B, Schedule A and the staffing plan
read back from target/, and the golden, every route and every construction computed on them (calc.py).

The golden prices the 2027 window on the experience the System's claims process now produces: each entity's
Claims and exposure from the month its incidents first brought a Claim made within 30 days (the disclosure-and-offer
Claims), each window Claim at its own cost against the exposure with its own delay left."""
from __future__ import annotations

import csv
import os

import openpyxl

import asks as A
import calc as CA
import claims as C
import common as K

CLASS_KEY = {v: k for k, v in K.CLASS_NAME.items()}
load_register = A.load_register
schedule_b = A.schedule_b


def load_payroll(target, first="2016-01", last="2024-12"):
    """job[(employee, YYYY-MM)] (the first row's job code), the experience FTE-years by class over the payroll months
    first to last, and {(entity, class, (y, m)): FTE-years} for those months; each month's paid FTE one twelfth of an
    FTE-year."""
    sb = schedule_b()
    job, E, Eekm = {}, {k: 0.0 for k in K.CLASSES}, {}
    with open(os.path.join(target, K.PAYROLL), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            job.setdefault((r["employee_id"], r["pay_month"]), r["job_code"])
            k = sb.get(r["job_code"])
            if k and first <= r["pay_month"] <= last:
                v = float(r["fte"]) / 12.0
                E[k] += v
                key = (r["entity_code"], k, (int(r["pay_month"][:4]), int(r["pay_month"][5:])))
                Eekm[key] = Eekm.get(key, 0.0) + v
    return job, E, Eekm


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


def job_lookup(job):
    code_to_key = {}
    for j in K.JOBS:
        code_to_key[j[1]] = j[0]
        code_to_key[j[2]] = j[0]
    return lambda cid, d: code_to_key.get(job.get((cid, K.month_key(d.year, d.month))))


def experience(target, rows=None, payroll=None, **kw):
    rows = rows if rows is not None else load_register(target)
    job, E, Eekm = payroll if payroll is not None else load_payroll(target)
    return C.experience_from_rows(rows, job_of=job_lookup(job), **kw), E


def main_call(target, rows=None):
    rows = rows if rows is not None else load_register(target)
    pay = load_payroll(target)
    job, E_full, Eekm = pay
    ex, _ = experience(target, rows, pay)
    plan = load_plan(target)
    tr = transitions()
    starts = CA.regime_starts(rows)
    post = CA.after(ex, starts)
    E = CA.exposure(Eekm, K.CLASSES, starts)
    rts, a = CA.routes(post, E, plan, tr, K.CLASSES, K.ENTITY_ORDER)
    full, a_full = CA.routes(ex, E_full, plan, tr, K.CLASSES, K.ENTITY_ORDER)
    g = rts["golden"]
    conv = CA.conventions(post, E, plan, tr, K.CLASSES, K.ENTITY_ORDER)
    cons = CA.constructions(ex, Eekm, plan, tr, K.CLASSES, K.ENTITY_ORDER, starts, rows)
    riv = CA.rivals(ex, Eekm, plan, tr, K.CLASSES, K.ENTITY_ORDER, starts)
    conv_full = CA.conventions(ex, E_full, plan, tr, K.CLASSES, K.ENTITY_ORDER)
    X = CA.fte_years(plan, tr, K.ENTITY_ORDER, K.CLASSES)
    return dict(rows=rows, job=job, ex=ex, post=post, E=E, E_full=E_full, Eekm=Eekm, plan=plan, a=a, a_full=a_full,
                starts=starts, routes=rts, full=full, conv=conv, conv_full=conv_full, cons=cons, rivals=riv, total=g,
                rounded=CA.rounded(g), sd=CA.poisson_sd(post, a), boot_sd=CA.bootstrap_sd(post, a),
                count=CA.count(post, a), fte_years_2027=sum(X.values()), exp_claims=len(ex),
                exp_fte_years=sum(E_full.values()), post_claims=len(post), post_fte_years=sum(E.values()))
