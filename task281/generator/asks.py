"""The three asks, from Central Payroll's overtime lines, the units' overtime offer log and HR's extract: A, the overtime
hours worked at each unit in FY2026; B, the people who worked overtime at each unit in FY2026; C, the people who worked
more than 600 hours of overtime in FY2026, by the title they held that year. Each function takes the handling choices a
response might make, so the cracker and the checks can run the same code down a wrong path."""
from __future__ import annotations

import collections

import common as K
import payroll as PY

FY0, FY1 = "2025-07-01", "2026-06-30"
QUARTERS = (("Q1", "2025-07-01", "2025-09-30"), ("Q2", "2025-10-01", "2025-12-31"),
            ("Q3", "2026-01-01", "2026-03-31"), ("Q4", "2026-04-01", "2026-06-30"))
LOC = {PY.TWC_SITE: "TWC"}
HOME = "home_timekeeper"
COMP = {"CTE": 1.5, "CTS": 1.0}     # compensatory hours credited for an hour worked, as the earnings codes name them


def quarter(d):
    for q, a, b in QUARTERS:
        if a <= d <= b:
            return q
    return None


def in_fy(d):
    return bool(d) and FY0 <= d <= FY1


def piece_key(r):
    return (r["employee_id"], r["work_date"], r["start_time"], r["hours"], r["earn_code"])


def repeats(pk):
    """the lines that pay again a piece an earlier check already paid (same employee, date, start, hours and code)"""
    first = {}
    out = set()
    for n, r in sorted(enumerate(pk.payroll), key=lambda x: (x[1]["check_date"], x[0])):
        if r["earn_code"] not in ("OT", "OTN") + tuple(COMP):
            continue
        k = piece_key(r)
        if k in first and first[k] != r["check_date"]:
            out.add(n)
        else:
            first.setdefault(k, r["check_date"])
    return out


def worked_unit(pk):
    """the unit each accepted offer put a piece at: (employee, date, start, hours) -> unit"""
    out = {}
    for r in pk.offers:
        if r["response"] == "Accepted":
            out[(r["employee_id"], r["post_date"], r["start_time"], r["hours"])] = r["post_unit"]
    return out


def credit(pk, r, flat=False):
    """compensatory hours credited for an hour worked, as the line's earnings code names it: CTE one and a half
    (MOU 14.2), CTS one (the forensic security aides, whose unit the MOU does not cover); flat reads both at 1.5"""
    if flat:
        return 1.5
    return COMP.get(r["earn_code"], 1.5)


def worked_key(pk, r, flat=False):
    """the hours a line's piece took, as the offer log writes them"""
    return r["hours"] if r["earn_code"] not in COMP else "%.2f" % (float(r["hours"]) / credit(pk, r, flat))


def hours_worked(r, cte=True, otn=False, otr=False, cr=1.5):
    """overtime hours a payroll line stands for, under a handling"""
    code = r["earn_code"]
    h = float(r["hours"])
    if code == "OT":
        return h
    if code in COMP:
        return h / cr if cte is True else (h if cte == "raw" else 0.0)
    if code == "OTN":
        return h if otn else 0.0
    if code == "OTR":
        return h if otr else 0.0
    return 0.0


def ask_a(pk, cte=True, otn=False, otr=False, offers=True, drop_repeats=True, dedupe_all=False, map_site=True,
          flat=False):
    rep = repeats(pk) if drop_repeats else set()
    where = worked_unit(pk) if offers else {}
    seen = set()
    out = collections.defaultdict(float)
    for n, r in enumerate(pk.payroll):
        if r["earn_code"] == "OTR" or not in_fy(r["work_date"]) or n in rep:
            continue
        if dedupe_all:
            k = piece_key(r)
            if k in seen:
                continue
            seen.add(k)
        u = where.get((r["employee_id"], r["work_date"], r["start_time"], worked_key(pk, r, flat)))
        if u is None:
            u = r[HOME]
            u = LOC.get(u, u) if map_site else u
        out[u] += hours_worked(r, cte, otn, otr, credit(pk, r, flat))
    return {u: int(round(out.get(u, 0.0))) for u in K.UNIT_CODES}


def unit_of(pk, r, where, map_site=True, flat=False):
    """the unit a piece was worked at: the post the offer log names, else the employee's own unit (MOU 14.3)"""
    u = where.get((r["employee_id"], r["work_date"], r["start_time"], worked_key(pk, r, flat)))
    if u is None:
        u = r[HOME]
        u = LOC.get(u, u) if map_site else u
    return u


def ask_b(pk, offers=True, merge=True, map_site=True):
    """the people who worked overtime (an overtime or compensatory time piece dated in FY2026) at each unit, an
    employee's records joined into one person"""
    where = worked_unit(pk) if offers else {}
    canon = {old: new for new, old in chains(pk).items()} if merge else {}
    people = collections.defaultdict(set)
    for r in pk.payroll:
        if r["earn_code"] not in ("OT",) + tuple(COMP) or not in_fy(r["work_date"]):
            continue
        people[unit_of(pk, r, where, map_site)].add(canon.get(r["employee_id"], r["employee_id"]))
    return {u: len(people.get(u, ())) for u in K.UNIT_CODES}


def chains(pk):
    """records HR opened for an employee rehired with the seniority date restored, joined to the employee's earlier
    record: new id -> earlier id"""
    out = {}
    for e, r in pk.emp.items():
        if r["seniority_date"] and r["seniority_date"] < r["hire_date"]:
            hits = [x for x, v in pk.emp.items() if x != e and v["seniority_date"] == r["seniority_date"] and
                    v["separation_date"] and v["separation_date"] < r["hire_date"] and
                    v["title_code"] == r["title_code"]]
            if len(hits) == 1:
                out[e] = hits[0]
    return out


def person_hours(pk, merge=True, cte=True, otn=False, otr=False, drop_repeats=True, flat=False):
    rep = repeats(pk) if drop_repeats else set()
    out = collections.defaultdict(float)
    for n, r in enumerate(pk.payroll):
        if r["earn_code"] == "OTR" or not in_fy(r["work_date"]) or n in rep:
            continue
        out[r["employee_id"]] += hours_worked(r, cte, otn, otr, credit(pk, r, flat))
    if merge:
        for e, old in chains(pk).items():
            out[e] += out.pop(old, 0.0)
    return out


def ask_c(pk, title="asof", **kw):
    ph = person_hours(pk, **kw)
    c = collections.Counter()
    for e, h in ph.items():
        if h > 600:
            t = pk.title_on(e, FY1) if title == "asof" else pk.emp[e]["title_code"]
            c[t] += 1
    return {t: c.get(t, 0) for t in K.TITLE_ORDER}


def golden(pk):
    return dict(a=ask_a(pk), b=ask_b(pk), c=ask_c(pk), hours=person_hours(pk))
