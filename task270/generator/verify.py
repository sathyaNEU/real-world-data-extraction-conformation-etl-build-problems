"""An independent recomputation of every graded figure from the shipped files alone (it imports nothing from the
generator but the file names): the pool and its appointees, each component's validity in the pool by the
multivariate correction on the variables the appointments were made on, the two kept, the first below and the order;
each component's cost per candidate; the people who applied to each examination and the completion rates; then the
golden workbook is read back and compared.

    python3 task270/generator/verify.py"""
import csv
import datetime as dt
import json
import os
import sys
import zoneinfo
from collections import defaultdict

import numpy as np
import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import FILES   # noqa: E402

TASK = os.path.dirname(HERE)
NAMES = ["Written test", "Oral board", "Physical ability test", "Situational judgement test", "Work style inventory"]
CC = {"4411": 0, "4412": 1, "4413": 2, "4414": 3, "4415": 4}
MIN = [150, 30, 20, 60, 40]
ET = zoneinfo.ZoneInfo("America/New_York")


def rows(t, k):
    with open(os.path.join(t, FILES[k]), encoding="utf-8") as f:
        return list(csv.DictReader(f))


def sheets(t, k):
    wb = openpyxl.load_workbook(os.path.join(t, FILES[k]), read_only=True, data_only=True)
    out = []
    for ws in wb.worksheets:
        it = ws.iter_rows(values_only=True)
        head = list(next(it))
        out.append((ws.title, [dict(zip(head, r)) for r in it if any(v is not None for v in r)]))
    return out


def scores(t):
    xw = rows(t, "crosswalk")
    hss = {r["hss_candidate_id"]: r["candidate_no"] for r in xw}
    ng = {r["pellwyn_id"]: r["candidate_no"] for r in xw if r["pellwyn_id"]}
    S = defaultdict(dict)
    for r in rows(t, "written"):
        S[r["client_reference"]][0] = float(r["scaled_score"])
    rat = defaultdict(list)
    for r in rows(t, "oral"):
        rat[r["candidate_no"]].append(float(r["rating"]))
    for c, v in rat.items():
        S[c][1] = 20.0 * sum(v) / len(v)
    run = {}
    for r in rows(t, "pat"):
        c, sec = r["candidate_no"], float(r["course_seconds"])
        if c not in run or sec < run[c][0]:
            run[c] = (sec, float(r["points"]))
    for c, (sec, pts) in run.items():
        S[c][2] = pts
    for _, sh in sheets(t, "sjt"):
        for r in sh:
            S[ng[r["Pellwyn ID"]]][3] = float(r["Scaled score"])
    for r in rows(t, "inventory"):
        S[hss[r["hss_candidate_id"]]][4] = float(r["dependability"])
    return S


def criterion(t):
    out = {}
    for title, sh in sheets(t, "academy"):
        for r in sh:
            if "Recruit No." in r:
                out[int(r["Recruit No."])] = float(r["Final Average"])
            else:
                v = r["Weighted Average"] if r["Outcome"] == "Graduated" else r["Average at Separation"]
                out[int(r["Employee ID"])] = float(v)
    return out


def validity(t):
    S = scores(t)
    reg = {r["candidate_no"]: r for r in rows(t, "roster")}
    crit = criterion(t)
    X, sel, Y, vet = [], [], [], []
    for c in sorted(S):
        if len(S[c]) < 5:
            continue
        g = reg.get(c)
        app = g is not None and g["disposition"] == "Appointed"
        X.append([S[c][j] for j in range(5)])
        vet.append(1.0 if g is not None and g["veteran_credit"] == "5.00" else 0.0)
        sel.append(app)
        Y.append(crit[int(g["employee_no"])] if app else np.nan)
    X, sel, Y, vet = np.array(X), np.array(sel), np.array(Y), np.array(vet)
    # selection variables: written, oral, veterans' credit, course points; the rest: SJT, inventory, criterion
    Z = np.column_stack([X[:, 0], X[:, 1], vet, X[:, 2], X[:, 3], X[:, 4], Y])
    s, o = [0, 1, 2, 3], [4, 5, 6]
    Sg = np.cov(Z[sel].T)
    Pss = np.cov(Z[:, s].T)
    Sss, Sso, Soo = Sg[np.ix_(s, s)], Sg[np.ix_(s, o)], Sg[np.ix_(o, o)]
    W = np.linalg.solve(Sss, Sso)
    Pso = Pss @ W
    Poo = Soo - Sso.T @ np.linalg.solve(Sss, Sso) + W.T @ Pss @ W
    P = np.block([[Pss, Pso], [Pso.T, Poo]])
    d = np.sqrt(np.diag(P))
    R = P / np.outer(d, d)
    v = [R[0, 6], R[1, 6], R[3, 6], R[4, 6], R[5, 6]]
    return v, len(X), int(sel.sum())


def exam_days(t):
    out = {}
    for r in rows(t, "calendar"):
        days = {dt.date.fromisoformat(r["written_test"]), dt.date.fromisoformat(r["physical_ability_test_from"]),
                dt.date.fromisoformat(r["physical_ability_test_to"])}
        a, b = dt.date.fromisoformat(r["oral_boards_from"]), dt.date.fromisoformat(r["oral_boards_to"])
        while a <= b:
            days.add(a)
            a += dt.timedelta(days=1)
        out[r["examination"]] = days
    return out


def cost(t, sat):
    trial = ["Spring 2024", "Autumn 2024", "Spring 2025", "Autumn 2025"]
    allx = ["Autumn 2023"] + trial + ["Spring 2026"]
    days = exam_days(t)
    own, shared = [0.0] * 5, 0.0
    for r in rows(t, "ledger"):
        desc, amt = r["line_description"], float(r["amount"])
        exam = next((x for x in allx if x in desc), None)
        if desc.startswith("Payroll PPE"):
            pe = dt.datetime.strptime(desc[12:22], "%m/%d/%Y").date()
            exam = next(x for x, ds in days.items() if any(pe - dt.timedelta(days=13) <= dd <= pe for dd in ds))
        elif desc.startswith("EMS standby"):
            last = dt.datetime.strptime(desc.split("-")[1], "%m/%d/%Y").date()
            exam = next(x for x, ds in days.items() if last in ds)
        elif desc.startswith("Retroactive pay"):
            exam = "Spring 2024"                       # 2024 and early 2025 work, all in the trial
        elif desc.startswith("Reversal of FY2024"):
            continue                                    # undoes the 2024 accruals, which their invoices repeat
        if exam not in trial:
            continue
        if desc.startswith("YE accrual") and r["posting_date"].startswith("2024"):
            continue
        if r["cost_center"] == "4410":
            shared += amt
        else:
            own[CC[r["cost_center"]]] += amt
    return [(own[j] + shared * MIN[j] / 300.0) / sat[j] for j in range(5)]


def applicants(t):
    win = {r["examination"]: (dt.datetime.fromisoformat(r["applications_open"]),
                              dt.datetime.fromisoformat(r["applications_close"]) + dt.timedelta(hours=23, minutes=59, seconds=59))
           for r in rows(t, "calendar")}
    entry = {"PO-24-0116": "Spring 2024", "PO-24-0715": "Autumn 2024", "PO-25-0121": "Spring 2025",
             "REQ-2025-0121": "Spring 2025", "REQ-2025-0714": "Autumn 2025"}
    forms = defaultdict(list)
    for r in rows(t, "ats_old"):
        if r["posting_no"] in entry and r["submitted"]:
            forms[entry[r["posting_no"]]].append((r["first_name"], r["last_name"],
                                                  dt.datetime.strptime(r["date_of_birth"], "%m/%d/%Y").date(),
                                                  r["email"], r["phone"],
                                                  dt.datetime.strptime(r["submitted"], "%m/%d/%Y %H:%M")))
    for r in rows(t, "ats_new"):
        if r["requisition_id"] in entry and r["submitted_at_utc"] and r["currently_employed_peace_officer"] != "Yes":
            u = dt.datetime.strptime(r["submitted_at_utc"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
            forms[entry[r["requisition_id"]]].append((r["first_name"], r["last_name"],
                                                      dt.date.fromisoformat(r["birth_date"]), r["email"], r["phone"],
                                                      u.astimezone(ET).replace(tzinfo=None)))
    out = {}
    for exam, fs in forms.items():
        fs = [f for f in fs if win[exam][0] <= f[5] <= win[exam][1]]
        parent = list(range(len(fs)))

        def root(i):
            while parent[i] != i:
                i = parent[i]
            return i
        keys = defaultdict(list)
        for i, (fn, ln, dob, em, ph, _) in enumerate(fs):
            nm = (fn.strip().lower(), ln.strip().lower())
            keys[("d",) + nm + (dob,)].append(i)
            if em.strip():
                keys[("e", em.strip().lower())].append(i)
            keys[("p",) + nm + ("".join(ch for ch in ph if ch.isdigit())[-10:],)].append(i)
        for ids in keys.values():
            for i in ids[1:]:
                a, b = root(ids[0]), root(i)
                if a != b:
                    parent[b] = a
        out[exam] = len({root(i) for i in range(len(fs))})
    return out


def run(task=TASK):
    t = os.path.join(task, "target")
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    bad = []
    v, pool, app = validity(t)
    order = [NAMES[j] for j in np.argsort(-np.array(v), kind="stable")]
    if pool != fig["components"]["pool"] or app != fig["components"]["appointees"]:
        bad.append("pool %d, appointees %d" % (pool, app))
    if sorted(order[:2]) != sorted(fig["call"]["keep"]):
        bad.append("kept %s" % order[:2])
    if order[2] != fig["call"]["first_below"] or order != fig["call"]["order"]:
        bad.append("order %s" % order)
    S = scores(t)
    sat = [sum(1 for s in S.values() if j in s) for j in range(5)]
    cp = cost(t, sat)
    for j, nm in enumerate(NAMES):
        if round(cp[j], 2) != fig["ask_a"][nm]:
            bad.append("%s cost per candidate %.4f against %s" % (nm, cp[j], fig["ask_a"][nm]))
    ap = applicants(t)
    for exam, n in fig["ask_b"]["applicants"].items():
        if ap.get(exam) != n:
            bad.append("%s applicants %s against %s" % (exam, ap.get(exam), n))
    tot = sum(ap.values())
    for j, nm in enumerate(NAMES):
        if round(100.0 * sat[j] / tot, 2) != fig["ask_b"]["completion"][nm]:
            bad.append("%s completion %.4f against %s" % (nm, 100.0 * sat[j] / tot, fig["ask_b"]["completion"][nm]))
    wb = openpyxl.load_workbook(os.path.join(task, "golden", "pd_2027_entry_examination_components.xlsx"), data_only=True)
    got = [r for r in wb["2027 components"].iter_rows(min_row=5, values_only=True) if r[1]]
    if [r[1] for r in got] != fig["call"]["order"] or [r[1] for r in got if r[4] == "Keep"] != fig["call"]["keep"]:
        bad.append("golden workbook ranking")
    costs = {r[0]: r[4] for r in wb["Cost per candidate"].iter_rows(min_row=2, values_only=True) if r[0] in NAMES}
    if costs != fig["ask_a"]:
        bad.append("golden workbook costs")
    sh = list(wb["Applicants and completion"].iter_rows(values_only=True))
    appl = {r[0]: r[1] for r in sh if r[0] in fig["ask_b"]["applicants"]}
    comp = {r[0]: r[2] for r in sh if r[0] in NAMES}
    if appl != fig["ask_b"]["applicants"] or comp != fig["ask_b"]["completion"]:
        bad.append("golden workbook applicants or completion")
    print("verify: %d figures recomputed, %d disagreements" % (2 + 3 + 5 + 5 + 4 + 5, len(bad)))
    for x in bad:
        print("  DISAGREE", x)
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(run())
