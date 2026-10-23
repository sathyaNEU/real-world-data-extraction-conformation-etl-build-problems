"""task170 independent verifier: reads only the bundle in a target folder, on its own code path (csv and openpyxl, no
pandas, no calc.py), recomputes every graded figure and compares it with figures.json.

    python3 task170/generator/verify.py task170/target"""
from __future__ import annotations

import csv
import datetime as dt
import json
import os
import sys
from collections import defaultdict

from openpyxl import load_workbook

HERE = os.path.dirname(os.path.abspath(__file__))
HOSP = ["VCS", "RDH", "ASK", "OSV", "BRB", "LDM"]
SCALE27 = {"G1": 24900, "G2": 27300, "G3": 30100, "G4": 33800, "G5": 38600, "G6": 44900, "G7": 52700, "G8": 63400}
LAST = 2026 * 12 + 9          # the October 2026 payroll as a month index
FIRST = 2019 * 12             # January 2019
FAILS = []


def ok(label, cond, detail=""):
    print("%s  %s  %s" % ("PASS" if cond else "FAIL", label, detail))
    if not cond:
        FAILS.append(label)


def mi(d):
    return d.year * 12 + d.month - 1


def iso(s):
    return dt.date.fromisoformat(s)


def match(rate):
    r = float(rate)
    return min(r, 3.0) + 0.5 * min(max(r - 3.0, 0.0), 3.0)


def rows_of(path, sheet=None):
    wb = load_workbook(path, read_only=True, data_only=True)
    ws = wb[sheet] if sheet else wb.worksheets[0]
    it = ws.iter_rows(values_only=True)
    head = [str(h) for h in next(it)]
    return [dict(zip(head, r)) for r in it if any(v is not None for v in r)]


def as_date(v):
    return v.date() if isinstance(v, dt.datetime) else (v if isinstance(v, dt.date) else iso(str(v)[:10]))


def km(events, follow, n=96):
    """events: list of month-of-event or None; follow: months observed. Returns cumulative incidence 1..n."""
    at = defaultdict(int)
    ev = defaultdict(int)
    for e, f in zip(events, follow):
        end = f if e is None else min(e, f)
        at[end] += 1
        if e is not None and e <= f:
            ev[e] += 1
    total = len(events)
    leaving = 0
    S, out = 1.0, []
    removed = 0
    for k in range(1, n + 1):
        risk = total - removed
        d = ev.get(k, 0)
        S *= (1 - d / risk) if risk else 1.0
        out.append(1 - S)
        removed += at.get(k, 0)
    return out


def main(target):
    F = json.load(open(os.path.join(HERE, "figures.json")))
    # hires: spells from January 2019
    hr = list(csv.DictReader(open(os.path.join(target, "hr_employment_history_2019_2026.csv"), encoding="utf-8")))
    idm = {}
    for r in hr:
        idm[r["legacy_employee_no"]] = r["employee_no"]
        idm[r["employee_no"]] = r["employee_no"]
    sp = []
    for r in hr:
        s = mi(iso(r["contract_start"]))
        if s < FIRST:
            continue
        e = mi(iso(r["contract_end"])) if r["contract_end"] else None
        sp.append(dict(emp=r["employee_no"], s=s, e=e, f=(min(e, LAST) if e is not None else LAST) - s + 1))
    by_emp = defaultdict(list)
    for i, x in enumerate(sp):
        by_emp[x["emp"]].append(i)

    def spell(emp, m):
        for i in by_emp.get(emp, []):
            x = sp[i]
            if x["s"] <= m and (x["e"] is None or m <= x["e"]):
                return i
        return None

    reg = rows_of(os.path.join(target, "ledstrand_member_register_2026-10.xlsx"))
    join = {}
    rate = {}
    for r in reg:
        m = mi(as_date(r["joined"]))
        i = spell(idm.get(str(r["employer_ref"])), m)
        if i is not None:
            join[i] = m
            rate[i] = int(r["rate_at_join_pct"])
    Cj = km([(join[i] - x["s"] + 1) if i in join else None for i, x in enumerate(sp)], [x["f"] for x in sp])
    p = Cj[59]
    # staying on the payroll: P(still paid in month k)
    left = [(x["e"] - x["s"] + 1) if (x["e"] is not None and x["e"] <= LAST) else None for x in sp]
    Lc = km(left, [x["f"] for x in sp])
    Se = [1.0] + [1 - v for v in Lc[:95]]
    mb = sum(match(r) for r in rate.values()) / len(rate) / 100
    ok("five-year join share", int(round(100 * p)) == F["component_prefer_to_save_pct"], "%.4f" % p)
    ok("chosen by the twelfth payroll", int(round(100 * Cj[11] / p)) == F["component_chosen_by_12th_payroll_pct"],
       "%.4f" % (Cj[11] / p))
    plan = rows_of(os.path.join(target, "vch_hiring_plan_2027.xlsx"), "Requisitions")
    by = defaultdict(float)
    heads = 0.0
    for r in plan:
        m0 = as_date(r["planned_start"]).month
        pay = SCALE27[r["grade"]] * float(r["fte"])
        for k in range(1, 14 - m0):
            A = Cj[k - 1] / p
            by[r["hospital"]] += Se[k - 1] * pay * ((1 - A) * 0.03 + Cj[k - 1] * mb)
            if k == 13 - m0:
                heads += Se[k - 1] * ((1 - A) + Cj[k - 1])
    tot = sum(by.values())
    ok("FY2027 match, group", int(round(tot / 500000)) * 500000 == F["call_match_fy2027_tnk"], "%.0f" % tot)
    for h in HOSP:
        ok("FY2027 match, %s" % h, int(round(by[h] / 100000)) * 100000 == F["call_match_fy2027_%s" % h], "%.0f" % by[h])
    ok("December 2027 contributors", int(round(heads / 100)) * 100 == F["call_contributing_dec2027"], "%.1f" % heads)
    # ask A: ERM once per employee, payroll and run, January to October 2026
    seen = set()
    paid = defaultdict(float)
    with open(os.path.join(target, "payroll_deductions_2025-11_2026-10.csv"), encoding="utf-8") as fh:
        octo = {}
        for r in csv.DictReader(fh):
            if r["payroll"] == "202610" and r["assignment"] == "1":
                octo.setdefault(r["employee_ref"], r["cost_centre"][:3])
            if r["code"] != "ERM" or not ("202601" <= r["payroll"] <= "202610"):
                continue
            key = (r["payroll"], r["run"], r["employee_ref"])
            if key in seen:
                continue
            seen.add(key)
            paid[r["cost_centre"][:3]] += float(r["amount"])
    for h in HOSP:
        ok("ask A %s" % h, int(round(paid[h] / 1000)) * 1000 == F["ask_match_paid_2026_%s" % h], "%.2f" % paid[h])
    # ask B: memberships opened before 2019, Active, employment not ended, by the October payroll's cost centre
    open_spell = {r["employee_no"] for r in hr if not r["contract_end"]}
    cnt = defaultdict(int)
    for r in reg:
        if r["status"] != "Active" or as_date(r["joined"]) >= dt.date(2019, 1, 1):
            continue
        emp = idm.get(str(r["employer_ref"]))
        if emp in open_spell:
            cnt[octo.get(emp)] += 1
    for h in HOSP:
        ok("ask B %s" % h, cnt[h] == F["ask_members_pre2019_%s" % h], str(cnt[h]))
    print("\n%d failed" % len(FAILS))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")))
