"""Independent verifier for task130: reads only the shipped pack (target/) and the goldens, on its own code path (no
generator module is imported), and recomputes the contribution, every entity and class figure, both asks and the
default path's figure, then compares them with the golden workbook.

    python3 task130/generator/verify.py [target] [golden]"""
from __future__ import annotations

import csv
import datetime as dt
import math
import os
import re
import sys

import openpyxl
from pypdf import PdfReader

REGISTER = "rm_claims_register_extract_20261002.csv"
PAYROLL = "clinician_fte_by_month_2016-01_2025-12.csv"
HCM = "hcm_clinician_pay_lines_2026-01_2026-09.csv"
CROSSWALK = "hcm_job_profile_crosswalk.csv"
DIRECTORY = "cost_centre_directory_2026.csv"
PLAN = "clinician_staffing_plan_2027.xlsx"
AGREEMENT = "CPLT_trust_agreement_executed_2026-08-14.pdf"
QM_SEP = "QMPL_loss_run_Corvane_val_2026-09-30.xlsx"
SC_SEP = "Stoneleigh_lossrun_CORVANE_20260930.csv"
NOTICES = "rm_carrier_notices_2012_2026.csv"
BOOK = "trust_funding_2027.xlsx"
MONTHS = {m: i for i, m in enumerate(["January", "February", "March", "April", "May", "June", "July", "August",
                                       "September", "October", "November", "December"], start=1)}
CLASS_NAMES = ["Obstetrics", "Surgery", "Emergency Medicine", "Anesthesiology", "Hospital and Medical Specialties",
               "Primary Care", "Advanced Practice"]


def agreement(target):
    text = "\n".join(p.extract_text() for p in PdfReader(os.path.join(target, AGREEMENT)).pages)
    flat = re.sub(r"\s+", " ", text)
    trans = {}
    for code in ("TFH", "AMC", "CMG", "BCH"):
        m = re.search(r"\b%s (\d{1,2}) (\w+) (\d{4})" % code, flat)
        trans[code] = dt.date(int(m.group(3)), MONTHS[m.group(2)], int(m.group(1)))
    classes = {}
    names = "|".join(re.escape(n) for n in sorted(CLASS_NAMES, key=len, reverse=True))
    for m in re.finditer(r"(%s) (\d{5}) ([A-Z]{3}-[A-Z]{2,4})\b" % names, flat):
        classes[m.group(2)] = m.group(1)
        classes[m.group(3)] = m.group(1)
    return trans, classes


def read_csv(target, name):
    with open(os.path.join(target, name), encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def num(s):
    return float(s) if s else 0.0


def main_call(target):
    trans, classes = agreement(target)
    pay = read_csv(target, PAYROLL)
    job = {}
    fte_years = {c: 0.0 for c in CLASS_NAMES}
    for r in pay:
        job.setdefault((r["employee_id"], r["pay_month"]), r["job_code"])
        if "2017-01" <= r["pay_month"] <= "2024-12" and r["job_code"] in classes:
            fte_years[classes[r["job_code"]]] += float(r["fte"]) / 12.0
    reg = read_csv(target, REGISTER)
    incidents = {}
    for r in reg:
        if "2017-01-01" <= r["incident_date"] <= "2024-12-31":
            incidents.setdefault(r["incident_no"], []).append(r)
    claims = []
    for ino in sorted(incidents):
        rs = incidents[ino]
        covered = [r for r in rs if r["coverage_line"] != "CONTRACT" and
                   job.get((r["clinician_id"], r["incident_date"][:7])) in classes]
        if not covered:
            continue
        made = min(r["claim_made_date"] for r in rs)
        first_no = min((r["claim_made_date"], r["claim_no"]) for r in rs)[1]
        first = min((r for r in covered if r["claim_no"] == first_no), key=lambda r: int(r["defendant_seq"]))
        cls = classes[job[(first["clinician_id"], first["incident_date"][:7])]]
        inc = dt.date.fromisoformat(rs[0]["incident_date"])
        lag = (dt.date.fromisoformat(made) - inc).days
        cost = sum(num(r["indemnity_paid"]) + num(r["defense_paid"]) + num(r["indemnity_reserve"]) +
                   num(r["defense_reserve"]) for r in covered) * 1.05 ** (2027 - inc.year)
        claims.append((cls, lag, cost))
    wb = openpyxl.load_workbook(os.path.join(target, PLAN), data_only=True)
    plan = {}
    for row in wb["Covered FTE 2027"].iter_rows(min_row=6, values_only=True):
        if row[0]:
            plan[(row[0], row[2])] = [float(v) for v in row[3:15]]
    end = dt.date(2027, 12, 31)
    out = {}
    default = 0.0
    for (e, c), fte in plan.items():
        cost = count = 0.0
        d = trans[e]
        while d <= end:
            nxt = dt.date(d.year + (d.month == 12), d.month % 12 + 1, 1)
            w = fte[d.month - 1] / 12.0 / (nxt - dt.date(d.year, d.month, 1)).days
            left = (end - d).days
            for cls, lag, cc in claims:
                if cls == c and lag <= left:
                    cost += w * cc
                    count += w
            default += w * sum(cc for cls, lag, cc in claims if cls == c) / fte_years[c]
            d += dt.timedelta(days=1)
        out[(e, c)] = (cost / fte_years[c], count / fte_years[c])
    return out, default, len(claims)


def ask_a(target):
    reg = read_csv(target, REGISTER)
    claim_inc = {re.sub(r"[^A-Z0-9]", "", r["claim_no"].upper()): r["incident_no"] for r in reg}
    notice_inc = {re.sub(r"[^A-Z0-9]", "", r["notice_no"].upper()): r["incident_no"] for r in read_csv(target, NOTICES)}
    on_run = {}
    wb = openpyxl.load_workbook(os.path.join(target, QM_SEP), data_only=True)
    names = {"Tolliver Falls Hospital": "TFH", "Alderwick Medical Center": "AMC", "CORVANE MEDICAL GROUP": "CMG",
             "BRENNICK COMMUNITY HOSP": "BCH"}
    refs = [(names[row[2]], row[4]) for row in wb["Loss Run"].iter_rows(min_row=8, values_only=True) if row[3]]
    refs += [(names[r["INSURED_NAME"]], r["INSURED_REF"]) for r in read_csv(target, SC_SEP)]
    for e, ref in refs:
        k = re.sub(r"[^A-Z0-9]", "", str(ref).upper())
        ino = claim_inc.get(k) or notice_inc.get(k)
        if ino:
            on_run.setdefault(e, set()).add(ino)
    lines = {"TFH": "QM-TFH", "AMC": "QM-AMC", "CMG": "SC-CMG", "BCH": "SC-BCH"}
    res = {}
    for e, line in lines.items():
        opn = {r["incident_no"] for r in reg if r["coverage_line"] == line and r["status"] in ("OPEN", "REOPENED")}
        miss = sorted(i for i in opn if i not in on_run.get(e, set()))
        reserves = sum(num(r["indemnity_reserve"]) + num(r["defense_reserve"]) for r in reg
                       if r["coverage_line"] == line and r["incident_no"] in miss)
        res[e] = (len(miss), reserves)
    return res


def ask_b(target):
    _, classes = agreement(target)
    xw = {r["job_profile_code"]: r["legacy_job_code"] for r in read_csv(target, CROSSWALK)}
    cc = {r["cost_centre"]: r["entity_code"] for r in read_csv(target, DIRECTORY)}
    seen, out = set(), {}
    for r in read_csv(target, HCM):
        if r["work_month"] != "2026-09" or xw[r["job_profile_code"]] not in classes:
            continue
        key = (r["worker_id"], r["position_id"])
        if key in seen:
            continue
        seen.add(key)
        e = cc[r["cost_centre"]]
        out[e] = out.get(e, 0.0) + float(r["fte"])
    return out


def r1000(x):
    return int(math.floor(x / 1000.0 + 0.5) * 1000)


def r1(x):
    return math.floor(x * 10 + 0.5) / 10


def main(target, golden):
    out, default, n = main_call(target)
    total = sum(v[0] for v in out.values())
    ents = ["TFH", "AMC", "CMG", "BCH"]
    ent = {e: (sum(v[0] for (ee, c), v in out.items() if ee == e), sum(v[1] for (ee, c), v in out.items() if ee == e))
           for e in ents}
    cls = {c: (sum(v[0] for (e, cc), v in out.items() if cc == c), sum(v[1] for (e, cc), v in out.items() if cc == c))
           for c in CLASS_NAMES}
    a = ask_a(target)
    b = ask_b(target)
    wb = openpyxl.load_workbook(os.path.join(golden, BOOK), data_only=True)
    ws = wb["Contribution"]
    errors = []
    if ws["B4"].value != r1000(total):
        errors.append("contribution %s against %s" % (ws["B4"].value, r1000(total)))
    rows = {r[0]: r for r in ws.iter_rows(min_row=8, values_only=True) if r[0]}
    full = {"TFH": "Tolliver Falls Hospital", "AMC": "Alderwick Medical Center", "CMG": "Corvane Medical Group",
            "BCH": "Brennick Community Hospital"}
    for e in ents:
        r = rows[full[e]]
        if r[3] != r1(ent[e][1]) or r[4] != r1000(ent[e][0]):
            errors.append("%s: %s %s against %s %s" % (e, r[3], r[4], r1(ent[e][1]), r1000(ent[e][0])))
    for c in CLASS_NAMES:
        r = rows[c]
        if r[3] != r1(cls[c][1]) or r[4] != r1000(cls[c][0]):
            errors.append("%s: %s %s against %s %s" % (c, r[3], r[4], r1(cls[c][1]), r1000(cls[c][0])))
    w3 = wb["Carrier loss runs"]
    for i, e in enumerate(ents):
        cnt, res = w3.cell(row=4 + i, column=5).value, w3.cell(row=4 + i, column=6).value
        cnt = 0 if cnt == "None" else cnt
        if cnt != a[e][0] or res != r1000(a[e][1]):
            errors.append("ask A %s: %s %s against %s %s" % (e, cnt, res, a[e][0], r1000(a[e][1])))
    w4 = wb["Covered FTE Sep 2026"]
    for i, e in enumerate(ents):
        if w4.cell(row=4 + i, column=2).value != r1(b[e]):
            errors.append("ask B %s: %s against %s" % (e, w4.cell(row=4 + i, column=2).value, r1(b[e])))
    if errors:
        raise SystemExit("verify: %d mismatches\n  " % len(errors) + "\n  ".join(errors))
    print("verify: %d experience Claims; contribution %s (default path, the experience's annual cost prorated: %s); entities %s; "
          "classes %s; ask A %s; ask B %s; all match the golden workbook" % (
              n, "{:,}".format(r1000(total)), "{:,}".format(r1000(default)),
              ", ".join("%s %.1f/%s" % (e, r1(ent[e][1]), "{:,}".format(r1000(ent[e][0]))) for e in ents),
              ", ".join("%s %.1f/%s" % (c.split()[0], r1(cls[c][1]), "{:,}".format(r1000(cls[c][0]))) for c in CLASS_NAMES),
              ", ".join("%s %d/%s" % (e, a[e][0], "{:,}".format(r1000(a[e][1]))) for e in ents),
              ", ".join("%s %.1f" % (e, r1(b[e])) for e in ents)))
    return dict(total=total, ent=ent, cls=cls, a=a, b=b, default=default)


if __name__ == "__main__":
    task = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    t = sys.argv[1] if len(sys.argv) > 1 else os.path.join(task, "target")
    g = sys.argv[2] if len(sys.argv) > 2 else os.path.join(task, "golden")
    main(t, g)
