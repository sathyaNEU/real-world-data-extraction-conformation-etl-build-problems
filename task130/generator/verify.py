"""Independent verifier for task130: reads only the shipped pack (target/) and the goldens, on its own code path (no
generator module is imported), and recomputes the contribution, the expected number of Claims, what each entity pays,
both asks and the default path's figure (the same window on the System's pooled experience), then compares them with
the golden workbook.

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
DICTIONARY = "data_dictionary_rm_extracts.md"
QM_SEP = "QMPL_loss_run_Corvane_val_2026-09-30.xlsx"
SC_SEP = "Stoneleigh_lossrun_CORVANE_20260930.csv"
NOTICES = "rm_carrier_notices_2012_2026.csv"
BOOK = "trust_funding_2027.xlsx"
MONTHS = {m: i for i, m in enumerate(["January", "February", "March", "April", "May", "June", "July", "August",
                                       "September", "October", "November", "December"], start=1)}
CLASS_NAMES = ["Obstetrics", "Surgery", "Emergency Medicine", "Anesthesiology", "Hospital and Medical Specialties",
               "Primary Care", "Advanced Practice"]
ENTS = ["TFH", "AMC", "CMG", "BCH"]
FULL = {"TFH": "Tolliver Falls Hospital", "AMC": "Alderwick Medical Center", "CMG": "Corvane Medical Group",
        "BCH": "Brennick Community Hospital"}


def agreement(target):
    text = "\n".join(p.extract_text() for p in PdfReader(os.path.join(target, AGREEMENT)).pages)
    flat = re.sub(r"\s+", " ", text)
    trans = {}
    for code in ENTS:
        m = re.search(r"\b%s (\d{1,2}) (\w+) (\d{4})" % code, flat)
        trans[code] = dt.date(int(m.group(3)), MONTHS[m.group(2)], int(m.group(1)))
    classes = {}
    names = "|".join(re.escape(n) for n in sorted(CLASS_NAMES, key=len, reverse=True))
    for m in re.finditer(r"(%s) (\d{5}) ([A-Z]{3}-[A-Z]{2,4})\b" % names, flat):
        classes[m.group(2)] = m.group(1)
        classes[m.group(3)] = m.group(1)
    return trans, classes, flat


def program_hospitals(target):
    """The entities whose patients the Early Resolution Program has served, as the dictionary names them."""
    text = re.sub(r"\s+", " ", open(os.path.join(target, DICTIONARY), encoding="utf-8").read())
    m = re.search(r"for the patients of ([A-Za-z ]+?) and ([A-Za-z ]+?) since", text)
    inv = {v: k for k, v in FULL.items()}
    return {inv[m.group(1).strip()], inv[m.group(2).strip()]}


def read_csv(target, name):
    with open(os.path.join(target, name), encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def num(s):
    return float(s) if s else 0.0


def experience(target, classes):
    pay = read_csv(target, PAYROLL)
    job = {}
    fte = {}
    for r in pay:
        job.setdefault((r["employee_id"], r["pay_month"]), r["job_code"])
        if "2017-01" <= r["pay_month"] <= "2024-12" and r["job_code"] in classes:
            key = (r["entity_code"], classes[r["job_code"]])
            fte[key] = fte.get(key, 0.0) + float(r["fte"]) / 12.0
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
        claims.append((rs[0]["entity_at_incident"], cls, lag, cost))
    return claims, fte


def window(target, claims, fte, ents_basis):
    """Each entity's window from its Transition Date, every day of exposure charged the basis's cost (and count) per
    FTE-year of the Claims whose delay falls by 31 December 2027."""
    trans, classes, _ = agreement(target)
    base = {}
    for (e, c), v in fte.items():
        if e in ents_basis:
            base[c] = base.get(c, 0.0) + v
    cl = [(c, lag, cost) for e, c, lag, cost in claims if e in ents_basis]
    wb = openpyxl.load_workbook(os.path.join(target, PLAN), data_only=True)
    plan = {}
    for row in wb["Covered FTE 2027"].iter_rows(min_row=6, values_only=True):
        if row[0]:
            plan[(row[0], row[2])] = [float(v) for v in row[3:15]]
    end = dt.date(2027, 12, 31)
    out, years = {}, {}
    for (e, c), f in plan.items():
        cost = count = 0.0
        d = trans[e]
        while d <= end:
            nxt = dt.date(d.year + (d.month == 12), d.month % 12 + 1, 1)
            w = f[d.month - 1] / 12.0 / (nxt - dt.date(d.year, d.month, 1)).days
            years[e] = years.get(e, 0.0) + w
            left = (end - d).days
            for cc, lag, amt in cl:
                if cc == c and lag <= left:
                    cost += w * amt
                    count += w
            d += dt.timedelta(days=1)
        out[(e, c)] = (cost / base[c], count / base[c])
    return out, years


def ask_a(target):
    reg = read_csv(target, REGISTER)
    key = lambda s: re.sub(r"[^A-Z0-9]", "", str(s).upper())
    claim_inc = {key(r["claim_no"]): r["incident_no"] for r in reg}
    notices = {key(r["notice_no"]): r for r in read_csv(target, NOTICES)}
    reg_inc = {r["incident_no"] for r in reg}
    by_event = {}
    for r in reg:
        by_event.setdefault((r["entity_at_incident"], r["incident_date"], r["allegation"]), set()).add(r["incident_no"])
    names = {"Tolliver Falls Hospital": "TFH", "Alderwick Medical Center": "AMC", "CORVANE MEDICAL GROUP": "CMG",
             "BRENNICK COMMUNITY HOSP": "BCH"}
    wb = openpyxl.load_workbook(os.path.join(target, QM_SEP), data_only=True)
    ws = wb["Loss Run"]
    hdr = [c.value for c in ws[7]]
    i_ins, i_ref, i_type = hdr.index("Named Insured"), hdr.index("Insured Reference"), hdr.index("Claim Type")
    runs = [(names[row[i_ins]], row[i_ref], row[i_type]) for row in ws.iter_rows(min_row=8, values_only=True)
            if row[3]]
    types = {"CLM": "Claim", "SUIT": "Suit", "INC": "Incident"}
    runs += [(names[r["INSURED_NAME"]], r["INSURED_REF"], types[r["CLM_TYPE"]]) for r in read_csv(target, SC_SEP)]
    on_run = {}
    for e, ref, typ in runs:
        k = key(ref)
        ino = claim_inc.get(k)
        if ino is None and k in notices:
            nrow = notices[k]
            if nrow["incident_no"] in reg_inc:
                ino = nrow["incident_no"]
            elif typ in ("Claim", "Suit"):
                hit = by_event.get((nrow["entity_code"], nrow["event_date"], nrow["event_category"]), set())
                ino = next(iter(hit)) if len(hit) == 1 else None
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


def ask_b(target, classes):
    xw = {r["job_profile_code"]: r["legacy_job_code"] for r in read_csv(target, CROSSWALK)}
    cc = {r["cost_centre"]: r["entity_code"] for r in read_csv(target, DIRECTORY)}
    seen, out = set(), {}
    for r in read_csv(target, HCM):
        if r["work_month"] != "2026-09" or xw[r["job_profile_code"]] not in classes:
            continue
        k = (r["worker_id"], r["position_id"])
        if k in seen:
            continue
        seen.add(k)
        e = cc[r["cost_centre"]]
        out[e] = out.get(e, 0.0) + float(r["fte"])
    return out


def r1000(x):
    return int(math.floor(x / 1000.0 + 0.5) * 1000)


def r1(x):
    return math.floor(x * 10 + 0.5) / 10


def main(target, golden):
    trans, classes, _ = agreement(target)
    prog = program_hospitals(target)
    claims, fte = experience(target, classes)
    out, years = window(target, claims, fte, prog)
    total = sum(v[0] for v in out.values())
    count = sum(v[1] for v in out.values())
    allx = sum(years.values())
    pays = {e: total * years[e] / allx for e in ENTS}
    pooled, _ = window(target, claims, fte, set(ENTS))
    default = sum(v[0] for v in pooled.values())
    a = ask_a(target)
    b = ask_b(target, classes)
    wb = openpyxl.load_workbook(os.path.join(golden, BOOK), data_only=True)
    ws = wb["Contribution"]
    errors = []
    if ws["B4"].value != r1000(total):
        errors.append("contribution %s against %s" % (ws["B4"].value, r1000(total)))
    if ws["B5"].value != r1(count):
        errors.append("count %s against %s" % (ws["B5"].value, r1(count)))
    rows = {r[0]: r for r in ws.iter_rows(min_row=9, values_only=True) if r[0]}
    for e in ENTS:
        r = rows[FULL[e]]
        if r[4] != r1000(pays[e]) or r[2] != r1(years[e]):
            errors.append("%s pays %s on %s FTE-years against %s on %s" % (e, r[4], r[2], r1000(pays[e]), r1(years[e])))
    if sum(r1000(v) for v in pays.values()) != r1000(total):
        errors.append("the rounded payments do not add to the contribution")
    w3 = wb["Carrier loss runs"]
    for i, e in enumerate(ENTS):
        cnt, res = w3.cell(row=4 + i, column=5).value, w3.cell(row=4 + i, column=6).value
        cnt = 0 if cnt == "None" else cnt
        if cnt != a[e][0] or res != r1000(a[e][1]):
            errors.append("ask A %s: %s %s against %s %s" % (e, cnt, res, a[e][0], r1000(a[e][1])))
    w4 = wb["Covered FTE Sep 2026"]
    for i, e in enumerate(ENTS):
        if w4.cell(row=4 + i, column=2).value != r1(b[e]):
            errors.append("ask B %s: %s against %s" % (e, w4.cell(row=4 + i, column=2).value, r1(b[e])))
    if r1000(default) == r1000(total):
        errors.append("the default path lands on the golden")
    if errors:
        raise SystemExit("verify: %d mismatches\n  " % len(errors) + "\n  ".join(errors))
    print("verify: %d experience Claims (%d at %s); contribution %s, %.1f Claims (default path, the same window on the "
          "System's pooled experience: %s); pays %s; ask A %s; ask B %s; all match the golden workbook" % (
              len(claims), sum(1 for c in claims if c[0] in prog), " and ".join(sorted(prog)),
              "{:,}".format(r1000(total)), r1(count), "{:,}".format(r1000(default)),
              ", ".join("%s %s" % (e, "{:,}".format(r1000(pays[e]))) for e in ENTS),
              ", ".join("%s %d/%s" % (e, a[e][0], "{:,}".format(r1000(a[e][1]))) for e in ENTS),
              ", ".join("%s %.1f" % (e, r1(b[e])) for e in ENTS)))
    return dict(total=total, count=count, pays=pays, a=a, b=b, default=default)


if __name__ == "__main__":
    task = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    t = sys.argv[1] if len(sys.argv) > 1 else os.path.join(task, "target")
    g = sys.argv[2] if len(sys.argv) > 2 else os.path.join(task, "golden")
    main(t, g)
