"""Independent verifier for task130: reads only the shipped pack (target/) and the goldens, on its own code path (no
generator module is imported), and recomputes each entity's first month with a Claim made within 30 days of its
incident, the contribution on the experience from those months, the expected number of Claims, both asks and the
default path's figure (the same construction on the whole 2016 to 2024 experience), then compares them with the
golden workbook.

    python3 task130/generator/verify.py [target] [golden]"""
from __future__ import annotations

import bisect
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
PREMIUMS = "insurance_premium_history_2016-2026.xlsx"
BOOK = "trust_funding_2027.xlsx"
MONTHS = {m: i for i, m in enumerate(["January", "February", "March", "April", "May", "June", "July", "August",
                                       "September", "October", "November", "December"], start=1)}
CLASS_NAMES = ["Obstetrics", "Surgery", "Emergency Medicine", "Anesthesiology", "Hospital and Medical Specialties",
               "Primary Care", "Advanced Practice"]
ENTITY_NAMES = {"Tolliver Falls Hospital": "TFH", "Alderwick Medical Center": "AMC", "Corvane Medical Group": "CMG",
                "Brennick Community Hospital": "BCH"}
LINES = {"TFH": "QM-TFH", "AMC": "QM-AMC", "CMG": "SC-CMG", "BCH": "SC-BCH"}
ENTS = ["TFH", "AMC", "CMG", "BCH"]
END = dt.date(2027, 12, 31)


def agreement(target):
    flat = re.sub(r"\s+", " ", "\n".join(p.extract_text() for p in PdfReader(os.path.join(target, AGREEMENT)).pages))
    trans = {}
    for code in ENTS:
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


def starts_of(target):
    """Each entity's first incident month with a claim number made within 30 days of the incident (rows naming an
    employed clinician), as YYYY-MM."""
    first = {}
    for r in read_csv(target, REGISTER):
        if r["coverage_line"] == "CONTRACT":
            continue
        if (dt.date.fromisoformat(r["claim_made_date"]) - dt.date.fromisoformat(r["incident_date"])).days <= 30:
            e = r["entity_at_incident"]
            if e not in first or r["incident_date"] < first[e]:
                first[e] = r["incident_date"]
    return {e: d[:7] for e, d in first.items()}


def experience(target, classes, starts=None):
    """The experience's Claims (class, delay, trended cost) and covered FTE-years by class, every month of 2016 to 2024
    or, given starts, each entity's months from its start."""
    pay = read_csv(target, PAYROLL)
    job = {}
    fte_years = {c: 0.0 for c in CLASS_NAMES}
    for r in pay:
        job.setdefault((r["employee_id"], r["pay_month"]), r["job_code"])
        if "2016-01" <= r["pay_month"] <= "2024-12" and r["job_code"] in classes:
            if starts is None or r["pay_month"] >= starts[r["entity_code"]]:
                fte_years[classes[r["job_code"]]] += float(r["fte"]) / 12.0
    incidents = {}
    for r in read_csv(target, REGISTER):
        if "2016-01-01" <= r["incident_date"] <= "2024-12-31":
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
        lead = min((r for r in rs if r["claim_no"] == first_no), key=lambda r: int(r["defendant_seq"]))
        if starts is not None and rs[0]["incident_date"][:7] < starts[lead["entity_at_incident"]]:
            continue
        cls = classes[job[(first["clinician_id"], first["incident_date"][:7])]]
        inc = dt.date.fromisoformat(rs[0]["incident_date"])
        lag = (dt.date.fromisoformat(made) - inc).days
        cost = sum(num(r["indemnity_paid"]) + num(r["defense_paid"]) + num(r["indemnity_reserve"]) +
                   num(r["defense_reserve"]) for r in covered) * 1.05 ** (2027 - inc.year)
        claims.append((cls, lag, cost))
    return claims, fte_years


def window(target, trans, claims, fte_years):
    """The window's expected cost and count, and the default path's cost (the count at each class's average)."""
    wb = openpyxl.load_workbook(os.path.join(target, PLAN), data_only=True)
    plan = {}
    for row in wb["Covered FTE 2027"].iter_rows(min_row=6, values_only=True):
        if row[0]:
            plan[(row[0], row[2])] = [float(v) for v in row[3:15]]
    by_cls = {}
    for cls, lag, cost in claims:
        by_cls.setdefault(cls, []).append((lag, cost))
    cum = {}
    for cls, v in by_cls.items():
        v.sort()
        lags = [x[0] for x in v]
        cc, c_acc = [], 0.0
        for lag, cost in v:
            c_acc += cost
            cc.append(c_acc)
        cum[cls] = (lags, cc)
    avg = {c: sum(x[1] for x in v) / len(v) for c, v in by_cls.items()}
    total = count = exposure = default = 0.0
    for (e, c), fte in plan.items():
        lags, cc = cum[c]
        d = trans[e]
        while d <= END:
            nxt = dt.date(d.year + (d.month == 12), d.month % 12 + 1, 1)
            w = fte[d.month - 1] / 12.0 / (nxt - dt.date(d.year, d.month, 1)).days
            exposure += w
            k = bisect.bisect_right(lags, (END - d).days)
            if k:
                total += w * cc[k - 1] / fte_years[c]
                count += w * k / fte_years[c]
                default += w * k / fte_years[c] * avg[c]
            d += dt.timedelta(days=1)
    return total, count, exposure, default


def main_call(target):
    trans, classes = agreement(target)
    starts = starts_of(target)
    claims, fte_years = experience(target, classes, starts)
    total, count, exposure, default = window(target, trans, claims, fte_years)
    whole_claims, whole_fte = experience(target, classes)
    whole, _, _, whole_default = window(target, trans, whole_claims, whole_fte)
    return dict(total=total, count=count, exposure=exposure, default=default, claims=len(claims),
                fte_years=sum(fte_years.values()), starts=starts, whole=whole, whole_default=whole_default,
                whole_claims=len(whole_claims), whole_fte_years=sum(whole_fte.values()))


def era_starts(target):
    wb = openpyxl.load_workbook(os.path.join(target, PREMIUMS), data_only=True)
    terms = {}
    for row in wb["Premium history"].iter_rows(min_row=5, values_only=True):
        if row[0]:
            start = row[3].date() if hasattr(row[3], "date") else row[3]
            terms.setdefault(ENTITY_NAMES[row[0]], []).append((start, row[1]))
    out = {}
    for e, t in terms.items():
        t.sort()
        car, start = t[-1][1], t[-1][0]
        for s, c in reversed(t):
            if c != car:
                break
            start = s
        out[e] = start
    return out


def ask_a(target):
    reg = read_csv(target, REGISTER)
    key = lambda s: re.sub(r"[^A-Z0-9]", "", str(s).upper())
    claim_inc = {key(r["claim_no"]): r["incident_no"] for r in reg}
    notice_inc = {key(r["notice_no"]): r["incident_no"] for r in read_csv(target, NOTICES)}
    names = {"Tolliver Falls Hospital": "TFH", "Alderwick Medical Center": "AMC", "CORVANE MEDICAL GROUP": "CMG",
             "BRENNICK COMMUNITY HOSP": "BCH"}
    wb = openpyxl.load_workbook(os.path.join(target, QM_SEP), data_only=True)
    refs = [(names[row[2]], row[4]) for row in wb["Loss Run"].iter_rows(min_row=8, values_only=True) if row[3]]
    refs += [(names[r["INSURED_NAME"]], r["INSURED_REF"]) for r in read_csv(target, SC_SEP)]
    on_run = {}
    for e, ref in refs:
        ino = claim_inc.get(key(ref)) or notice_inc.get(key(ref))
        if ino:
            on_run.setdefault(e, set()).add(ino)
    eras = era_starts(target)
    res = {}
    for e, line in LINES.items():
        opn = {r["incident_no"] for r in reg if r["coverage_line"] == line and r["status"] in ("OPEN", "REOPENED")
               and r["incident_date"] >= eras[e].isoformat()}
        miss = sorted(i for i in opn if i not in on_run.get(e, set()))
        reserves = sum(num(r["indemnity_reserve"]) + num(r["defense_reserve"]) for r in reg
                       if r["coverage_line"] == line and r["incident_no"] in miss)
        res[e] = (len(miss), reserves)
    return res


def ask_b(target):
    _, classes = agreement(target)
    xw = {r["job_profile_code"]: r["legacy_job_code"] for r in read_csv(target, CROSSWALK)}
    cc = {r["cost_centre"]: r["entity_code"] for r in read_csv(target, DIRECTORY)}
    lines = [r for r in read_csv(target, HCM) if r["work_month"] in ("2026-07", "2026-08", "2026-09")]
    trainees = {(r["worker_id"], r["work_month"]) for r in lines if xw[r["job_profile_code"]].startswith("GME-")}
    out = {}
    for r in lines:
        if xw[r["job_profile_code"]] not in classes or (r["worker_id"], r["work_month"]) in trainees:
            continue
        k = (cc[r["cost_centre"]], r["work_month"])
        out[k] = out.get(k, 0.0) + float(r["hours"]) / 173.33
    return out


def r1000(x):
    return int(math.floor(x / 1000.0 + 0.5) * 1000)


def r250k(x):
    return int(math.floor(x / 250000.0 + 0.5) * 250000)


def r1(x):
    return math.floor(x * 10 + 0.5) / 10


def main(target, golden):
    mc = main_call(target)
    a = ask_a(target)
    b = ask_b(target)
    wb = openpyxl.load_workbook(os.path.join(golden, BOOK), data_only=True)
    errors = []
    if wb["Contribution"]["B4"].value != r250k(mc["total"]):
        errors.append("contribution %s against %s" % (wb["Contribution"]["B4"].value, r250k(mc["total"])))
    w3 = wb["Carrier loss runs"]
    for i, e in enumerate(ENTS):
        cnt, res = w3.cell(row=4 + i, column=6).value, w3.cell(row=4 + i, column=7).value
        cnt = 0 if cnt == "None" else cnt
        if cnt != a[e][0] or res != r1000(a[e][1]):
            errors.append("ask A %s: %s %s against %s %s" % (e, cnt, res, a[e][0], r1000(a[e][1])))
    w4 = wb["Covered FTE 2026"]
    for i, e in enumerate(ENTS):
        for j, mo in enumerate(("2026-07", "2026-08", "2026-09")):
            if w4.cell(row=4 + i, column=2 + j).value != r1(b[(e, mo)]):
                errors.append("ask B %s %s: %s against %s" % (e, mo, w4.cell(row=4 + i, column=2 + j).value,
                                                              r1(b[(e, mo)])))
    if errors:
        raise SystemExit("verify: %d mismatches\n  " % len(errors) + "\n  ".join(errors))
    print("verify: starts %s; %d experience Claims since them on %s FTE-years (whole experience %d on %s); 2027 "
          "exposure %.1f FTE-years; %.2f expected Claims; contribution %s from %s (the same construction on the whole "
          "experience, the default path: %s; the count at each class's average cost: %s); ask A %s; ask B %s; all "
          "match the golden workbook" % (
              ", ".join("%s %s" % (e, mc["starts"][e]) for e in ENTS), mc["claims"],
              "{:,.1f}".format(mc["fte_years"]), mc["whole_claims"], "{:,.1f}".format(mc["whole_fte_years"]),
              mc["exposure"], mc["count"], "{:,}".format(r250k(mc["total"])), "{:,.0f}".format(mc["total"]),
              "{:,.0f}".format(mc["whole"]), "{:,.0f}".format(mc["default"]),
              ", ".join("%s %d/%s" % (e, a[e][0], "{:,}".format(r1000(a[e][1]))) for e in ENTS),
              ", ".join("%s %s" % (e, "/".join("%.1f" % r1(b[(e, mo)]) for mo in ("2026-07", "2026-08", "2026-09")))
                        for e in ENTS)))
    return dict(main=mc, a=a, b=b)


if __name__ == "__main__":
    task = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    t = sys.argv[1] if len(sys.argv) > 1 else os.path.join(task, "target")
    g = sys.argv[2] if len(sys.argv) > 2 else os.path.join(task, "golden")
    main(t, g)
