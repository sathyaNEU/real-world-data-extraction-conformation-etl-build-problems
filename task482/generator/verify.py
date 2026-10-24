"""Independent verifier: recomputes every graded figure from the shipped files in target/ alone, reading each file the
way a solver would, and compares them with golden/ and generator/figures.json.

    python3 task482/generator/verify.py
"""
import collections
import csv
import datetime as dt
import json
import os
import re
import sys

import numpy as np
import openpyxl
from pypdf import PdfReader

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
GD = os.path.join(TASK, "golden")
FAIL = []


def ok(tag, cond, msg):
    print("%-5s %s %s" % (tag, "ok  " if cond else "FAIL", msg))
    if not cond:
        FAIL.append(tag)


def rows(name):
    with open(os.path.join(T, name), newline="") as f:
        return list(csv.DictReader(f))


def day(s):
    return dt.date.fromisoformat(s) if s else None


def pdf_text(name):
    return "\n".join(p.extract_text() for p in PdfReader(os.path.join(T, name)).pages)


def main():
    # order forms
    ws = openpyxl.load_workbook(os.path.join(T, "order_forms_2025_26.xlsx"), read_only=True)["Order forms 2025-26"]
    it = ws.iter_rows(values_only=True)
    head = next(it)
    of = {}
    for r in it:
        x = dict(zip(head, r))
        of[x["Partner ID"]] = x
    pids = sorted(of)
    dix = {p: i for i, p in enumerate(pids)}
    ok("V0", len(of) == 58, "58 order forms")
    # the technical report: scale, cuts, the band crosswalk
    rep = pdf_text("caldrith_lsoa_technical_report_2026.pdf")
    ok("V1", "500 + 50 theta" in rep and "500 in grade 6, 520 in grade 7 and 540 in grade 8" in rep.replace("\n", " "),
       "reporting scale and Proficient levels as the report states them")
    bands = {"EOG": ["Not Proficient", "Level 3", "Level 4", "Level 5"],
             "OST": ["Limited", "Basic", "Proficient", "Accomplished|Advanced"],
             "Georgia Milestones": ["Beginning Learner", "Developing Learner", "Proficient Learner", "Distinguished Learner"],
             "TCAP": ["Below", "Approaching", "Met Expectations", "Exceeded Expectations"],
             "CMAS": ["Did Not Yet Meet|Partially Met", "Approached", "Met", "Exceeded"],
             "AASA": ["Minimally Proficient", "Partially Proficient", "Proficient", "Highly Proficient"]}
    flat = rep.replace("\n", " ")
    ok("V2", all(lv.split("|")[0] in flat for v in bands.values() for lv in v), "Table 5 carries every level read here")
    # items
    items = {r["item_id"]: (float(r["a_discrimination"]), float(r["b_difficulty"])) for r in rows("caldrith_item_parameters_2024.csv")}
    # eligibility, crosswalk, sessions, responses, roster
    elig = {}
    for r in rows("guarantee_eligibility_2025_26.csv"):
        if r["guarantee_eligible"] == "Y":
            assert r["student_id"] not in elig
            elig[r["student_id"]] = (r["partner_id"], int(r["grade"]))
    xw = collections.defaultdict(list)
    for r in rows("student_id_crosswalk_2025_26.csv"):
        xw[r["test_taker_id"]].append(r["student_id"])
    sub = {}
    for r in rows("lsoa_spring2026_sessions.csv"):
        if r["session_status"] == "Submitted":
            assert r["test_taker_id"] not in sub
            sub[r["test_taker_id"]] = r["session_id"]
    resp = collections.defaultdict(list)
    for r in rows("lsoa_spring2026_item_responses.csv"):
        resp[r["session_id"]].append(r)
    wb = openpyxl.load_workbook(os.path.join(T, "district_roster_uploads_spring2026.xlsx"), read_only=True)
    ros = {}
    yes = {"Economically Disadvantaged": {"EDS", "Y", "F", "ED", "Free", "1"}, "English Learner": {"LEP", "L", "Y", "EL", "NEP", "1"},
           "Students with Disabilities": {"EC", "Y", "SPED", "IEP"}}
    for sh in wb.worksheets:
        itr = sh.iter_rows(values_only=True)
        h = next(itr)
        for r in itr:
            x = dict(zip(h, r))
            b = 4
            if x["Prior Test Level"]:
                test = next(k for k in bands if (x["Prior State Test"] or "").startswith(k))
                b = next(i for i, lv in enumerate(bands[test]) if x["Prior Test Level"] in lv.split("|"))
            ros[x["Student ID"]] = (b, int(str(x["Economically Disadvantaged"] or "") in yes["Economically Disadvantaged"]),
                                    int(str(x["English Learner"] or "") in yes["English Learner"]),
                                    int(str(x["Students with Disabilities"] or "") in yes["Students with Disabilities"]))
    Q = np.round(np.arange(-4.475, 4.4751, 0.05), 4)
    recs = []
    for tt, sess in sub.items():
        es = [s for s in xw[tt] if s in elig]
        if not es:
            continue
        assert len(es) == 1
        sid = es[0]
        p, g = elig[sid]
        ll = np.zeros(len(Q))
        for r in resp[sess]:
            if r["response_status"] == "Not reached":
                continue
            a, b = items[r["item_id"]]
            pq = 1 / (1 + np.exp(-a * (Q - b)))
            y = int(r["score"])
            ll += y * np.log(pq) + (1 - y) * np.log(1 - pq)
        recs.append((dix[p], g - 6, ros[sid], ll))
    n = len(recs)
    dist = np.array([x[0] for x in recs]); gr = np.array([x[1] for x in recs])
    bd = np.array([x[2][0] for x in recs]); bg = np.array([x[2][1:] for x in recs], float)
    LL = np.array([x[3] for x in recs]); L = np.exp(LL - LL.max(1, keepdims=True))
    ok("V3", n == sum(v["assessed"] for v in json.load(open(os.path.join(HERE, "figures.json")))["districts"].values()),
       "%d eligible students assessed" % n)
    X = np.column_stack([np.eye(58)[dist], np.eye(3)[gr][:, 1:], np.eye(5)[bd][:, 1:], bg])
    # EM for theta ~ N(X g, s2) on the grid
    g_ = np.zeros(X.shape[1]); s2 = 1.0
    XtXi = np.linalg.pinv(X.T @ X)
    for _ in range(400):
        mu = X @ g_
        w = L * np.exp(-0.5 * (Q[None, :] - mu[:, None]) ** 2 / s2)
        w /= w.sum(1, keepdims=True)
        gn = XtXi @ (X.T @ (w @ Q))
        mu = X @ gn
        s2 = float((w * (Q[None, :] - mu[:, None]) ** 2).sum(1).mean())
        if np.abs(gn - g_).max() < 1e-7:
            g_ = gn
            break
        g_ = gn
    mu = X @ g_
    w = L * np.exp(-0.5 * (Q[None, :] - mu[:, None]) ** 2 / s2)
    w /= w.sum(1, keepdims=True)
    cut = np.array([0.0, 0.4, 0.8])[gr]
    pa = (w * (Q[None, :] > cut[:, None])).sum(1)
    share = 100 * np.bincount(dist, pa, minlength=58) / np.bincount(dist, minlength=58)
    owed = sorted(p for p in pids if share[dix[p]] < of[p]["Guarantee Benchmark (%)"])
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    ok("V4", owed == figs["call"]["owed"], "owed set recomputed from the files: %d districts" % len(owed))
    og = {p: round(of[p]["Subscription Fee (USD)"] * of[p]["Credit Percentage (%)"] / 100, 2) for p in owed}
    ok("V5", abs(sum(og.values()) - figs["call"]["og_total"]) < 0.005, "outcomes credits USD %.2f" % sum(og.values()))
    gap = min(abs(share[dix[p]] - of[p]["Guarantee Benchmark (%)"]) for p in pids)
    ok("V6", gap > 4.0, "every district more than 4 points from its benchmark on this recomputation (min %.2f)" % gap)
    # professional learning
    cat = pdf_text("professional_learning_catalog_2025_26.pdf")
    per = {}
    for m in re.finditer(r"(LL-\d{3})\s.*?(Virtual live|On site)\s+(\d)\s+(\d+)\s+(\d+)", cat.replace("\n", " ")):
        per[m.group(1)] = float(m.group(4))
    ok("V7", len(per) == 11 and all(h == int(h) for h in per.values()),
       "the catalog schedules its %d live offerings in whole hours" % len(per))
    mins = collections.Counter()
    for r in rows("pd_sessions_2025_26.csv"):
        o = of[r["partner_id"]]
        d = day(r["session_date"])
        h, mm = r["hours"].split(".")
        assert int(mm) < 60, r["hours"]                  # hours and minutes after the point
        if r["status"] == "Delivered" and r["delivery"] in ("Virtual live", "On site") and \
                o["Subscription Term Start"].date() <= d <= o["Subscription Term End"].date():
            mins[r["partner_id"]] += 60 * int(h) + int(mm)
    assert all(mins[p] % 30 != 15 for p in pids), "a district's hours sit on a quarter hour"
    hrs = {p: float(np.floor(mins[p] / 30.0 + 0.5) / 2) for p in pids}
    ok("V8", all(abs(hrs[p] - figs["districts"][p]["pd_delivered"]) < 1e-9 for p in pids),
       "live hours delivered, 58 districts, to the nearest half hour")
    pl = {p: max(0.0, of[p]["Live PL Hours"] - hrs[p]) * 250 for p in pids}
    ok("V9", all(abs(pl[p] - figs["districts"][p]["pl"]) < 1e-9 for p in pids), "shortfall credits, total USD %.2f" % sum(pl.values()))
    # invoices and the memo file
    inv = rows("billing_invoices_2026_27.csv")
    memo_exp = []
    for p in pids:
        o = of[p]
        a = o["Subscription Term Start"].date().replace(year=2026)
        c = [x for x in inv if x["customer_account"] == o["Bill-to Account"] and x["status"] == "Open"
             and day(x["service_period_start"]) == a and "subscription 2026-27" in x["description"]]
        tgt = min(c, key=lambda x: (x["due_date"], x["invoice_number"])) if c else None
        for code, amt in (("OG", og.get(p, 0.0)), ("PL", pl[p])):
            if amt > 0:
                memo_exp.append(["%s-2526-%s" % (code, p[3:]), o["Bill-to Account"], code, "%.2f" % amt,
                                 tgt["invoice_number"] if tgt else "", "APPLY" if tgt else "CHECK", "2026-11-30"])
                if tgt:
                    assert float(tgt["balance_due"]) >= og.get(p, 0) + pl[p]
    memo_exp.sort()
    with open(os.path.join(GD, "guarantee_credit_memos_2026.csv"), newline="") as f:
        got = list(csv.reader(f))[1:]
    ok("V10", got == memo_exp, "credit memo file: %d rows match" % len(memo_exp))
    gw = openpyxl.load_workbook(os.path.join(GD, "lumenfold_guarantee_settlement_2025_26.xlsx"))["Settlement 2025-26"]
    body = [r for r in gw.iter_rows(min_row=5, values_only=True) if r[0]]
    ok("V11", len(body) == 58 and all((r[6] == "Not met") == (r[0] in owed) for r in body) and
       all(abs((r[9] or 0) - og.get(r[0], 0.0)) < 1e-9 and abs(r[11] - hrs[r[0]]) < 1e-9 and abs(r[13] - pl[r[0]]) < 1e-9
           for r in body), "settlement workbook rows agree")
    print("\n%s" % ("all checks passed" if not FAIL else "FAILED: " + ", ".join(FAIL)))
    return 1 if FAIL else 0


if __name__ == "__main__":
    raise SystemExit(main())
