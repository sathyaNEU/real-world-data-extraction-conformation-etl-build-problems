"""The independent verifier: reads only the shipped bundle (target/) and the golden deliverables, on its own code
path, and recomputes the 2027 forecast, the call and the three 2026 asks.

    python3 task130/generator/verify.py
"""
import csv
import datetime as dt
import json
import os
import re
import sys

import openpyxl
import pypdf

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)


def rows(target, name):
    with open(os.path.join(target, name), encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def sunday(y, m, n):
    d = dt.date(y, m, 1)
    while d.weekday() != 6:
        d += dt.timedelta(days=1)
    return d + dt.timedelta(days=7 * (n - 1))


def pacific(s):
    u = dt.datetime.fromisoformat(s.replace("Z", ""))
    start = dt.datetime.combine(sunday(u.year, 3, 2), dt.time(10, 0))
    end = dt.datetime.combine(sunday(u.year, 11, 1), dt.time(9, 0))
    return u - dt.timedelta(hours=7) if start <= u < end else u - dt.timedelta(hours=8)


def bad(res):
    return res in ("UNSAT", "IHH CLOSURE", "Unsatisfactory", "Closed - imminent health hazard")


def closed(res):
    return res in ("NO ACCESS", "No access")


def recompute(target):
    perm = {r["permit_id"]: r for r in rows(target, "food_establishment_permits.csv")}
    wb = openpyxl.load_workbook(os.path.join(target, "food_program_staff_roster.xlsx"), read_only=True)
    init, name2emp, officers = {}, {}, set()
    for sh in wb.sheetnames:
        for i, r in enumerate(wb[sh].iter_rows(values_only=True)):
            if i == 0 or not r[0]:
                continue
            m = re.match(r"(.+), (.+) (\w)\.$", r[1])
            last, first, mid = m.group(1), m.group(2), m.group(3)
            init[first[0] + mid + last[0]] = r[0]
            name2emp[first + " " + last] = r[0]
            if r[2] == "Return Inspection Officer":
                officers.add(r[0])
    ev = []
    for r in rows(target, "inspections_2019-01_2024-03.csv"):
        t = dt.datetime.strptime("%s %s" % (r["insp_date"], r["time_in"]), "%m/%d/%Y %I:%M %p")
        ev.append((t, r["inspection_no"], r["permit_no"], init[r["inspector"]], r["insp_type"].title(), r["result"], "", None))
    for r in rows(target, "inspections_2024-03_2026-12.csv"):
        ev.append((pacific(r["inspected_at_utc"]), r["inspection_id"], r["permit_id"], r["inspector_employee_no"],
                   r["inspection_type"].title(), r["result"], r["complaint_id"], r["inspected_at_utc"]))
    ev.sort(key=lambda e: (e[0], e[1]))
    # the call
    count = {}
    cell = {}
    for t, iid, pid, who, typ, res, cref, tu in ev:
        n = count.get((who, pid), 0)
        if typ == "Routine" and not closed(res) and 2022 <= t.year <= 2026:
            key = (int(perm[pid]["risk_category"]), min(n, 2))
            a = cell.setdefault(key, [0, 0])
            a[0] += bad(res)
            a[1] += 1
        if not closed(res):
            count[(who, pid)] = n + 1
    sw = openpyxl.load_workbook(os.path.join(target, "routine_inspection_schedule_2027.xlsx"), read_only=True)
    named = {r[0]: r[3] for i, r in enumerate(sw["Districts 2027"].iter_rows(values_only=True)) if i}
    total = 0.0
    for i, r in enumerate(sw["Schedule 2027"].iter_rows(values_only=True)):
        if i == 0:
            continue
        pid, risk, dist, n = r[0], int(r[4]), r[5], int(r[6])
        k0 = count.get((named[dist], pid), 0)
        for j in range(n):
            a = cell[(risk, min(k0 + j, 2))]
            total += a[0] / a[1]
    # holidays
    hj = json.load(open(os.path.join(target, "county_holidays_2025-2027.json"), encoding="utf-8"))
    hol = {dt.date.fromisoformat(x["date"]) for y in hj["years"].values() for x in y}

    def wdays(a, b):
        n = 0
        while a < b:
            a += dt.timedelta(days=1)
            n += a.weekday() < 5 and a not in hol
        return n
    # day sheets: each return-team record keyed from a sheet takes the sheet's date
    cw = openpyxl.load_workbook(os.path.join(target, "return_team_capacity_report_2026.xlsx"), read_only=True)
    sheet = []
    for i, r in enumerate(cw["Day sheet log"].iter_rows(values_only=True)):
        if i and r[0]:
            sheet.append([r[0].date(), name2emp[r[1]], key_addr(r[3]), False])
    date_of = {}
    for t, iid, pid, who, typ, res, cref, tu in ev:
        if typ != "Return" or closed(res):
            continue
        d = t.date()
        if tu and who in officers and d <= dt.date(2026, 9, 15):
            ka = key_addr(perm[pid]["street_address"])
            c = [s for s in sheet if not s[3] and s[1] == who and s[2] == ka and 1 <= (d - s[0]).days <= 20]
            if c:
                s = min(c, key=lambda s: s[0])
                s[3] = True
                d = s[0]
        date_of[iid] = d
    # episodes per permit
    byp = {}
    for e in ev:
        byp.setdefault(e[2], []).append(e)
    closed_calls = {}
    for t, iid, pid, who, typ, res, cref, tu in ev:
        if typ == "Return" and closed(res):
            closed_calls.setdefault(pid, set()).add(t.date())
    for r in rows(target, "correspondence_log_2026.csv"):
        if r["template"].startswith("RV-NA"):
            closed_calls.setdefault(r["permit_id"], set()).add(dt.date.fromisoformat(r["visit_date"]))
    A, Cfee = {}, {}
    for pid, es in byp.items():
        routines = [e for e in es if e[4] == "Routine" and not closed(e[5])]
        for j, e in enumerate(routines):
            if not bad(e[5]) or e[0].year != 2026:
                continue
            nxt = routines[j + 1][0] if j + 1 < len(routines) else dt.datetime(2099, 1, 1)
            done = [date_of[x[1]] for x in es if x[4] == "Return" and not closed(x[5]) and e[0] < x[0] < nxt]
            dist = int(perm[pid]["district_2026"])
            if done and min(done).year == 2026:
                A.setdefault(dist, []).append(wdays(e[0].date(), min(done)))
            visits = sorted(set(done) | {d for d in closed_calls.get(pid, ()) if e[0].date() < d < nxt.date()})
            for d in visits[1:]:
                if d.year == 2026:
                    Cfee[dist] = Cfee.get(dist, 0) + (152 if d < dt.date(2026, 7, 1) else 168)
    med = lambda v: (sorted(v)[len(v) // 2] if len(v) % 2 else (sorted(v)[len(v) // 2 - 1] + sorted(v)[len(v) // 2]) / 2)
    A = {d: med(v) for d, v in A.items()}
    # complaints: first notice since the permit's last complaint investigation
    comp = {}
    for r in rows(target, "complaints_2024-03_2026-12.csv"):
        comp.setdefault(r["permit_id"], []).append(dt.datetime.fromisoformat(r["received_at_utc"].replace("Z", "")))
    last, B = {}, {}
    for t, iid, pid, who, typ, res, cref, tu in sorted((e for e in ev if e[4] == "Complaint" and e[7]),
                                                       key=lambda e: e[7]):
        s = dt.datetime.fromisoformat(tu.replace("Z", ""))
        lo = last.get(pid)
        first = min(x for x in comp.get(pid, []) if x < s and (lo is None or x > lo))
        last[pid] = s
        if t.year == 2026:
            B.setdefault(int(perm[pid]["district_2026"]), []).append((s - first).total_seconds() / 3600)
    B = {d: med(v) for d, v in B.items()}
    return total, A, B, Cfee


def key_addr(a):
    a = a.upper().replace(".", "")
    for full, short in (("STREET", "ST"), ("AVENUE", "AVE"), ("ROAD", "RD"), ("DRIVE", "DR"), ("HIGHWAY", "HWY"),
                        ("LANE", "LN"), ("BOULEVARD", "BLVD")):
        a = re.sub(r"\b%s\b" % full, short, a)
    p = a.split()
    if p and p[-1] in ("ST", "AVE", "RD", "DR", "HWY", "LN", "BLVD", "WAY", "LOOP", "GRADE"):
        p = p[:-1]
    return " ".join(p)


def main(target=os.path.join(TASK, "target"), golden=os.path.join(TASK, "golden")):
    total, A, B, C = recompute(target)
    gw = openpyxl.load_workbook(os.path.join(golden, "return_inspections_2027.xlsx"), read_only=True)

    def table(sheet):
        out = {}
        for r in gw[sheet].iter_rows(values_only=True):
            if r and isinstance(r[0], int):
                out[r[0]] = r[-1]
        return out
    fc = [r for r in gw["Forecast 2027"].iter_rows(values_only=True) if r and r[1] == "All districts"][0]
    assert abs(fc[-1] - round(total, 1)) < 0.051, ("forecast", fc[-1], total)
    assert total > 540, "the call"
    ga, gb, gc = table("Return timeliness 2026"), table("Complaint response 2026"), table("Return visit fees 2026")
    assert all(abs(ga[d] - A[d]) < 1e-9 for d in A) and set(ga) == set(A), ("ask A", ga, A)
    assert all(abs(gb[d] - round(B[d], 1)) < 0.051 for d in B) and set(gb) == set(B), ("ask B", gb, B)
    assert all(gc[d] == C.get(d, 0) for d in gc), ("ask C", gc, C)
    memo = "\n".join(p.extract_text() or "" for p in pypdf.PdfReader(os.path.join(golden, "return_officer_memo_2027.pdf")).pages)
    assert "Add the third return-inspection officer" in memo and format(int(100 * int(total / 100 + 0.5)), ",") in memo
    print("verify: match (forecast %.1f, the call, ask A %d districts, ask B %d, ask C %d, the memo)"
          % (total, len(A), len(B), len(gc)))


if __name__ == "__main__":
    main()
