"""An independent recompute of task482's graded figures from the cut pack (target/), sharing no code with golden.py:
the conformance of the two platforms, the 2025 plan year at the 2027 fees, the predetermined work put off past the
plan year, each maximum's cost and increase per covered person month, the call, Schedule C's counts by quarter and
the orthodontic balances, each compared with generator/figures.json. Schedule C's holidays are typed in from its table.

    python3 task482/generator/verify.py
"""
import csv
import datetime as dt
import json
import os
import sys
from collections import defaultdict

import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
D = dt.date
COINS = {"I": 100, "II": 80, "III": 50}
HOL = {D(2025, 1, 1), D(2025, 5, 26), D(2025, 7, 4), D(2025, 9, 1), D(2025, 11, 27), D(2025, 11, 28), D(2025, 12, 24),
       D(2025, 12, 25), D(2026, 1, 1), D(2026, 5, 25), D(2026, 7, 3), D(2026, 9, 7), D(2026, 11, 26), D(2026, 11, 27),
       D(2026, 12, 24), D(2026, 12, 25)}
CUT = D(2026, 9, 30)
BAD = []


def read(n):
    with open(os.path.join(T, n), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def cents(s):
    return int(round(float(s) * 100)) if s else 0


def us(s):
    m, d, y = s[:10].split("/")
    return D(int(y), int(m), int(d))


def iso(s):
    return D(int(s[:4]), int(s[5:7]), int(s[8:10]))


def central(s):
    t = dt.datetime(int(s[:4]), int(s[5:7]), int(s[8:10]), int(s[11:13]), int(s[14:16]))

    def sunday(y, m, nth):
        d0 = D(y, m, 1)
        d0 += dt.timedelta(days=(6 - d0.weekday()) % 7)
        return d0 + dt.timedelta(days=7 * (nth - 1))
    a = dt.datetime.combine(sunday(t.year, 3, 2), dt.time(8))
    b = dt.datetime.combine(sunday(t.year, 11, 1), dt.time(7))
    return t - dt.timedelta(hours=5 if a <= t < b else 6)


def business(d):
    return d.weekday() < 5 and d not in HOL


def compare(name, got, want):
    flag = got == want
    print(("ok    " if flag else "DIFF  ") + "%s: %s%s" % (name, got, "" if flag else " (figures.json %s)" % (want,)))
    if not flag:
        BAD.append(name)


def pdf_text(name):
    import subprocess
    out = subprocess.run(["pdftotext", "-layout", os.path.join(T, name), "-"], capture_output=True, text=True).stdout
    return " ".join(out.split())


def documents():
    """Every filed sentence the call and the asks lean on, read back from the PDFs themselves, with a control."""
    import re
    f17 = pdf_text("pembrook_benefit_costing_standard_f17.pdf")
    res = pdf_text("pembrook_board_bargaining_mandate_2026-09-28.pdf")
    sc = pdf_text("ridgeline_aso_agreement_schedule_c.pdf")
    spd = pdf_text("pembrook_dental_plan_spd_2025.pdf")
    checks = [
        ("F-17 costs the change on the most recent complete plan year",
         "had the change applied to that plan year, at the fees in effect for the plan year in which the change would take effect" in f17),
        ("F-17 states the result per covered person month", "stated per covered person month of that plan year's enrolment" in f17),
        ("F-17 compares at the same fees", "at the current plan design, at the same fees" in f17),
        ("F-17 rounds to the cent", "stated to the cent" in f17),
        ("control: F-17 names no predetermination", "predetermination" not in f17.lower()),
        ("the resolution's menu", "2,000 dollars or of 3,000 dollars" in res),
        ("the resolution's limit", "no more than 1.90 dollars per covered person month" in res),
        ("Schedule C's receipt rule", "after 5:00 p.m. Central Time, or on a day that is not a business day, is received on the next business day" in sc),
        ("Schedule C's five business days and 90 per cent", "within five business days of receipt for at least 90 per cent" in sc),
        ("the plan summary's deductible", "The deductible is 50 dollars per covered person per plan year" in spd),
        ("the plan summary's maximum", "up to 1,500 dollars for each covered person in a plan year" in spd),
        ("the plan summary's corrected claims", "the corrected claim replaces the original" in spd),
        ("the plan summary's coinsurance", re.search(r"100%.*80%.*50%", spd) is not None),
    ]
    tab = sc[sc.index("Observed holiday"):sc.index("C.4")]
    months = "January February March April May June July August September October November December".split()
    hol = set(D(int(y), months.index(m) + 1, int(d)) for d, m, y in re.findall(r"(\d{1,2}) (%s) (\d{4})" % "|".join(months), tab))
    checks.append(("Schedule C's holiday table equals the calendar typed in here", hol == HOL))
    for name, flag in checks:
        print(("ok    " if flag else "DIFF  ") + "document: " + name)
        if not flag:
            BAD.append(name)


def main():
    documents()
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    xw = {r["legacy_member_id"]: r["member_key"] for r in read("rba_member_crosswalk_2025-07-01.csv")}
    who = lambda ref: xw.get(ref, ref)
    wb = openpyxl.load_workbook(os.path.join(T, "ridgeline_ppo_fee_schedule_2024-2027.xlsx"), data_only=True)
    fee, cls = {}, {}
    for ws in wb.worksheets:
        for r in ws.iter_rows(values_only=True):
            if r and isinstance(r[0], str) and len(r[0]) == 5 and r[0][0] == "D" and r[0][1:].isdigit():
                fee.setdefault(int(ws.title), {})[r[0]] = int(round(float(r[3]) * 100))
                cls[r[0]] = r[2]

    # the conformance: each claim at its final version
    L = read("rba_classic_claims_2024-01_2025-06.csv")
    N = read("rba_nexus_claim_lines_2025-07_2026-10.csv")
    gone = set(r["ORIG_CLAIM_NO"] for r in L if r["TXN"] == "VOID") | set(r["prior_claim_id"] for r in N if r["prior_claim_id"])
    lines = []
    for r in L:
        if r["TXN"] != "VOID" and r["CLAIM_NO"] not in gone:
            lines.append((who(r["MEMBER_ID"]), us(r["DOS"]), "D" + r["PROC"], r["TOOTH"], cents(r["DEDUCT"]), r["REASON"] == "FQ"))
    for r in N:
        if r["claim_status"] != "SUPERSEDED" and r["claim_id"] not in gone:
            lines.append((r["member_key"], iso(r["service_date"]), r["cdt_code"], r["tooth_number"].lstrip("0"),
                          cents(r["deductible_amt"]), r["carc"] == "151"))
    share = defaultdict(int)
    for k, dos, code, tooth, ded, frq in lines:
        if dos.year == 2025 and not frq:
            share[k] += (fee[2027][code] - ded) * COINS[cls[code]] // 100

    # covered months of 2025
    months = defaultdict(set)

    def span(k, a, b):
        a, b = max(a, D(2025, 1, 1)), min(b, D(2025, 12, 31))
        y, m = a.year, a.month
        while (y, m) <= (b.year, b.month) and a <= b:
            months[k].add(m)
            y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    for r in read("rba_classic_eligibility_2025-06-30.csv"):
        span(who(r["MEMBER_ID"]), us(r["EFF_DATE"]), min(us(r["TERM_DATE"]), D(2025, 6, 30)))
    for r in read("rba_nexus_eligibility_2026-10-09.csv"):
        span(r["member_key"], iso(r["coverage_start"]), iso(r["coverage_end"]) if r["coverage_end"] else D(2099, 1, 1))
    mm = {k: len(v) for k, v in months.items() if v}
    tm = sum(mm.values())

    # the predetermination requests
    reqs = defaultdict(list)
    for r in read("rba_classic_predeterminations_2024-01_2025-06.csv"):
        reqs[("L", r["PREDET_NO"])].append((who(r["MEMBER_ID"]), dt.datetime.strptime(r["RECEIVED"], "%m/%d/%Y %H:%M"),
                                           us(r["RESPONDED"]), "D" + r["PROC"], r["TOOTH"], cents(r["EST_ALLOWED"]),
                                           cents(r["EST_DEDUCT"]), cents(r["EST_PLAN_PMT"])))
    for r in read("rba_nexus_estimates_2025-06_2026-09.csv"):
        reqs[("N", r["member_key"], r["rendering_npi"], r["received_utc"])].append(
            (r["member_key"], central(r["received_utc"]), central(r["issued_utc"]).date(), r["cdt_code"],
             r["tooth_number"].lstrip("0"), cents(r["est_allowed_amt"]), cents(r["est_deductible_amt"]),
             cents(r["est_plan_amt"])))
    when = defaultdict(list)
    for k, dos, code, tooth, ded, frq in lines:
        when[(k, code, tooth)].append(dos)
    put, done = defaultdict(int), set()
    for rid, ls in reqs.items():
        if not any(pl < (al - de) * COINS[cls[c]] // 100 for _, _, _, c, _, al, de, pl in ls):
            continue
        for k, recv, issued, code, tooth, al, de, pl in ls:
            if issued.year != 2025 or (k, code, tooth) in done:
                continue
            ds = when.get((k, code, tooth), [])
            if any(recv.date() <= x <= D(2025, 12, 31) for x in ds):
                continue
            if not any(D(2026, 1, 1) <= x <= issued + dt.timedelta(days=365) for x in ds):
                continue
            done.add((k, code, tooth))
            put[k] += fee[2027][code] * COINS[cls[code]] // 100

    base = sum(min(share.get(k, 0), 150000) for k in mm)
    cost, inc = {}, {}
    for m, lab in ((150000, "1,500"), (200000, "2,000"), (300000, "3,000")):
        c = sum(min(share.get(k, 0) + (put.get(k, 0) if m > 150000 else 0), m) for k in mm)
        cost[lab] = "%.2f" % round(c / 100.0 / tm + 1e-9, 2)
        if m > 150000:
            inc[lab] = "%.2f" % round(float(cost[lab]) - float(cost["1,500"]), 2)
    call = max([lab for lab in ("2,000", "3,000") if float(inc[lab]) <= 1.90] or ["1,500"], key=lambda s: int(s.replace(",", "")))
    compare("covered persons and months", (len(mm), tm), (fig["plan_year"]["persons"], fig["plan_year"]["months"]))
    compare("cost per covered person month", cost, fig["cost"])
    compare("increase over 1,500", inc, fig["increase"])
    compare("the call", call, fig["call"]["maximum"])
    compare("put-off work (members, amount)", (len(put), "{:,.2f}".format(sum(put.values()) / 100.0)),
            (fig["put_off"]["members"], fig["put_off"]["amount"]))
    compare("base cost at 1,500 (dollars)", "{:,.2f}".format(base / 100.0), fig["member_year"]["cost"]["1,500"])

    # Schedule C by quarter of receipt
    out = defaultdict(lambda: [0, 0])
    for rid, ls in reqs.items():
        recv = ls[0][1]
        last = max(x[2] for x in ls)
        d = recv.date()
        if not business(d) or recv.time() > dt.time(17, 0):
            d += dt.timedelta(days=1)
            while not business(d):
                d += dt.timedelta(days=1)
        q = "%dQ%d" % (d.year, (d.month + 2) // 3)
        n, x = 0, d
        while x < last:
            x += dt.timedelta(days=1)
            n += business(x)
        out[q][0] += 1
        out[q][1] += n <= 5
    compare("Schedule C counts", {q: out[q] for q in fig["ask_a"]}, fig["ask_a"])

    # orthodontic balances
    paid = defaultdict(int)
    for r in read("rba_ortho_payments_2024-01_2026-09.csv"):
        paid[r["case_id"]] += cents(r["amount"])
    cov = {}
    for r in read("rba_nexus_eligibility_2026-10-09.csv"):
        a, b = iso(r["coverage_start"]), iso(r["coverage_end"]) if r["coverage_end"] else D(2099, 1, 1)
        if a <= CUT <= b:
            cov[r["member_key"]] = True
    kids = defaultdict(list)
    for r in read("rba_ortho_case_schedule_2026-09-30.csv"):
        kids[who(r["member_ref"])].append(r)
    res = {y: [0, 0] for y in fig["ask_b"]}
    for k, cs in kids.items():
        cs.sort(key=lambda r: r["banding_date"])
        a = cs[-1]
        start = iso(a["banding_date"])
        mo = start.month - 1 + int(a["treatment_months"])
        y2, m2 = start.year + mo // 12, mo % 12 + 1
        nxt = D(y2 + (m2 == 12), m2 % 12 + 1, 1)
        end = D(y2, m2, min(start.day, (nxt - dt.timedelta(days=1)).day))
        left = cents(a["plan_benefit"]) - paid[a["case_id"]]
        y = cs[0]["banding_date"][:4]
        if k in cov and end > CUT and left > 0 and y in res:
            res[y][0] += 1
            res[y][1] += left
    compare("orthodontic balances", {y: dict(children=v[0], owed="{:,.2f}".format(v[1] / 100.0)) for y, v in res.items()},
            fig["ask_b"])
    print("verify: %s" % ("every figure recomputes" if not BAD else "%d differ: %s" % (len(BAD), ", ".join(BAD))))
    return 1 if BAD else 0


if __name__ == "__main__":
    sys.exit(main())
