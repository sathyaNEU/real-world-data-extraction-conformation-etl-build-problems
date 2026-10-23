"""task177 independent verifier: reads only the bundle (target/, golden/, figures.json, submission.md) and recomputes
every graded figure on its own code path (the csv module and plain dictionaries, no pandas, nothing from calc.py or the
generator's world). Exit 1 on any mismatch.

    python3 task177/generator/verify.py task177/target"""
from __future__ import annotations

import csv
import io
import json
import math
import os
import re
import sys
import zipfile
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = []


def check(name, cond, detail=""):
    OUT.append((name, bool(cond), detail))


def rows(path):
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def mon(s):
    s = s.strip()
    if len(s) == 6 and s.isdigit():
        return int(s[:4]) * 12 + int(s[4:]) - 1
    return int(s[:4]) * 12 + int(s[5:7]) - 1


def near(v, u):
    return int(u * math.floor(v / u + 0.5))


def xlsx_cells(path):
    """sheet name -> {cell ref: value} from the workbook's XML, shared strings resolved"""
    z = zipfile.ZipFile(path)
    ss = []
    if "xl/sharedStrings.xml" in z.namelist():
        x = z.read("xl/sharedStrings.xml").decode()
        for si in re.findall(r"<si>(.*?)</si>", x, re.S):
            ss.append("".join(re.findall(r"<t[^>]*>(.*?)</t>", si, re.S)))
    wb = z.read("xl/workbook.xml").decode()
    names = re.findall(r'<sheet [^>]*name="([^"]+)"', wb)
    out = {}
    for k, nm in enumerate(names, 1):
        x = z.read("xl/worksheets/sheet%d.xml" % k).decode()
        cells = {}
        for ref, attrs, body in re.findall(r'<c r="([A-Z]+\d+)"([^>]*)>(.*?)</c>', x, re.S):
            v = re.search(r"<v>(.*?)</v>", body)
            if not v:
                t = re.search(r"<t[^>]*>(.*?)</t>", body)
                cells[ref] = t.group(1) if t else None
            elif 't="s"' in attrs:
                cells[ref] = ss[int(v.group(1))]
            else:
                cells[ref] = v.group(1)
        out[nm] = cells
    return out


def main(target):
    task = os.path.dirname(os.path.abspath(target))
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    J = lambda f: os.path.join(target, f)

    # ------------------------------------------------------------------ public: conversion and on-payroll rate
    xw = {r["legacy_loan_no"]: r["core_loan_no"] for r in rows(J("legacy_core_crosswalk_2021.csv"))}
    loans = rows(J("payroll_loans_public_2017_2026.csv"))
    sinsal = defaultdict(set)
    for r in rows(J("treasury_deduction_returns_2017_2026.csv")):
        if r["reason"] in ("01", "SIN SALARIO"):
            sinsal[xw.get(r["loan_reference"], r["loan_reference"])].add(mon(r["period"]))
    first_def = {}
    for r in rows(J("default_register_2017_2026.csv")):
        k = xw.get(r["loan_reference"], r["loan_reference"])
        t = mon(r["default_date"][:7])
        first_def[k] = min(t, first_def.get(k, 10 ** 9))
    lim = 2025 * 12 + 11
    lags = []
    first_run = {}
    for k, ms in sinsal.items():
        ms = sorted(ms)
        starts = [m for i, m in enumerate(ms) if i == 0 or ms[i - 1] != m - 1]
        first_run[k] = starts[0]
        s0 = [m for m in starts if m <= lim]
        if s0:
            lags.append(first_def.get(k, 10 ** 9) - s0[0])
    Fv = [sum(1 for g in lags if 0 <= g <= j) / len(lags) for j in range(13)]
    expo = 0
    mdef = 0
    for r in loans:
        k = r["loan_no"]
        d = mon(r["disbursement_date"][:7])
        end = min(d + int(r["term_months"]), lim)
        stop = min(first_run.get(k, 10 ** 9), first_def.get(k, 10 ** 9))
        expo += max(0, min(end, stop) - d)
        if k in first_def and first_def[k] <= lim and (k not in first_run or first_run[k] > first_def[k]):
            mdef += 1
    resid = mdef / expo

    # ------------------------------------------------------------------ private: leaving hazards
    seen = set()
    months = defaultdict(set)
    settle = set()
    hire = {}
    for r in rows(J("employer_payroll_registers_2025_2026.csv")):
        key = tuple(r.values())
        if key in seen:
            continue
        seen.add(key)
        if r["payment_type"] not in ("NOMINA", "LIQUIDACION"):
            continue
        e = (r["employer_nit"], re.sub(r"\D", "", r["employee_id"]))
        t = mon(r["period_start"][:7])
        months[e].add(t)
        hire[e] = mon(r["hire_date"][:7])
        if r["payment_type"] == "LIQUIDACION":
            settle.add((e, t))
    ex = defaultdict(int)
    lv = defaultdict(int)
    for e, ms in months.items():
        for t in ms:
            if t - hire[e] >= 12:
                ex[e[0]] += 1
                if (e, t) in settle:
                    lv[e[0]] += 1
    haz = {n: lv[n] / ex[n] for n in ex}

    # ------------------------------------------------------------------ the launch
    agree = xlsx_cells(J("deduction_agreements_register.xlsx"))["agreements"]
    sector = {}
    for ref, v in agree.items():
        m = re.fullmatch(r"A(\d+)", ref)
        if m and int(m.group(1)) > 1:
            sector[v] = agree["C" + m.group(1)]
    launch = rows(J("libranza_empresarial_disbursement_file_2027-02-01.csv"))
    tot = 0.0
    by = defaultdict(float)
    nby = defaultdict(int)
    for r in launch:
        hh = haz[r["employer_nit"]]
        surv, p = 1.0, 0.0
        for m in range(1, 13):
            j = 11 - m
            if j >= 0:
                p += surv * hh * Fv[j]
            if m <= 9:
                p += surv * (1 - hh) * resid
            surv *= (1 - hh) * (1 - resid)
        tot += p
        by[sector[r["employer_nit"]]] += p
        nby[sector[r["employer_nit"]]] += 1
    check("call total", near(tot, 50) == fig["call_total"], "%.2f" % tot)
    check("call total unrounded", abs(tot - fig["call_total_unrounded"]) < 0.06, "%.2f" % tot)
    for s, v in fig["call_share"].items():
        check("call share %s" % s, near(100 * by[s] / nby[s], 5) == v, "%.2f" % (100 * by[s] / nby[s]))
    check("component conversion", near(100 * Fv[12], 1) == fig["cc_conversion_pct"], "%.4f" % Fv[12])
    hm = sum(haz[r["employer_nit"]] for r in launch) / len(launch)
    check("component leaving rate", near(100 * hm, 1) == fig["cc_leave_launch_pct"], "%.3f" % (100 * hm))
    check("component launch count", len(launch) == fig["counts"]["n_launch"])

    # ------------------------------------------------------------------ ask A
    sch = defaultdict(lambda: dict(rows=[], nit="", per="", filed=""))
    for r in rows(J("savings_contribution_schedules_2025_2026.csv")):
        x = sch[r["schedule_no"]]
        x["rows"].append((r["member_id"], float(r["contribution"])))
        x["nit"], x["per"], x["filed"] = r["employer_nit"], r["period"], r["filed_on"]
    groups = defaultdict(list)
    for no, x in sorted(sch.items(), key=lambda kv: (kv[1]["filed"], kv[0])):
        groups[(x["nit"], x["per"])].append(no)
    eff = {}
    for key, nos in groups.items():
        live = []
        for no in nos:
            mem = {m for m, _ in sch[no]["rows"]}
            live = [o for o in live if len(mem & {m for m, _ in sch[o]["rows"]}) < 0.5 * len(sch[o]["rows"])]
            live.append(no)
        for no in live:
            eff[no] = dict(nit=key[0], per=key[1], amt=sum(a for _, a in sch[no]["rows"]))
    stmt = rows(J("collection_account_statement_2025_2026.csv"))
    credits = []
    for r in stmt:
        if r["description"] == "TRANSFERENCIA RECIBIDA":
            credits.append([r["posting_date"], r["payer_id"], r["reference"], float(r["credit"])])
    for r in stmt:
        if r["description"] == "DEVOLUCION TRANSFERENCIA":
            for c in reversed(credits):
                if c[1] == r["payer_id"] and c[2] == r["reference"] and c[3] == float(r["debit"]) and c[0] <= r["posting_date"]:
                    credits.remove(c)
                    break
    paid = set()
    for date, payer, ref, amt in sorted(credits):
        mm = re.search(r"(\d\d)/(\d{4})", ref)
        per = "%s-%s" % (mm.group(2), mm.group(1))
        open_ = {k: v for k, v in eff.items() if k not in paid}
        same = [k for k, v in open_.items() if v["per"] == per]
        hit = None
        # one schedule of the month, the payer's own first
        for k in sorted(same, key=lambda k: open_[k]["nit"] != payer):
            if abs(open_[k]["amt"] - amt) < 0.5:
                hit = [k]
                break
        if hit is None:
            for i, a in enumerate(same):
                for b in same[i + 1:]:
                    if payer in (open_[a]["nit"], open_[b]["nit"]) and abs(open_[a]["amt"] + open_[b]["amt"] - amt) < 0.5:
                        hit = [a, b]
                        break
                if hit:
                    break
        if hit is None:
            own = sorted((k for k, v in open_.items() if v["nit"] == payer), key=lambda k: (open_[k]["per"], k))
            acc, pick = 0.0, []
            for k in own:
                if acc + open_[k]["amt"] <= amt + 0.5:
                    acc += open_[k]["amt"]
                    pick.append(k)
                if abs(acc - amt) < 0.5:
                    break
            hit = pick if abs(acc - amt) < 0.5 else []
        paid.update(hit)
    ded = defaultdict(float)
    out = defaultdict(float)
    for k, v in eff.items():
        if v["per"].startswith("2026"):
            s = sector[v["nit"]]
            ded[s] += v["amt"]
            if k not in paid:
                out[s] += v["amt"]
    for s in fig["ask_a_deducted"]:
        check("ask A deducted %s" % s, near(ded[s], 1000) == fig["ask_a_deducted"][s], "%.0f" % ded[s])
        check("ask A not received %s" % s, near(out[s], 1000) == fig["ask_a_outstanding"][s], "%.0f" % out[s])

    # ------------------------------------------------------------------ ask B
    utype = {r["loan_no"]: r["unit_type"] for r in loans}
    dyear = {}
    for r in rows(J("default_register_2017_2026.csv")):
        dyear[xw.get(r["loan_reference"], r["loan_reference"])] = int(r["default_date"][:4])
    holder = {}
    for r in rows(J("member_savings_ledger_2023_2026.csv")):
        holder[r["savings_account"]] = r["member_id"]
    rec = rows(J("defaulted_loan_receipts_2023_2026.csv"))
    reversed_ids = {r["receipt_id"][:-1] for r in rec if r["channel"] == "REVERSO"}
    sums = defaultdict(float)
    for r in rec:
        if r["channel"] == "REVERSO" or r["receipt_id"] in reversed_ids:
            continue
        if holder.get(r["originating_account"]) == r["member_id"]:
            continue
        k = xw.get(r["loan_reference"], r["loan_reference"])
        if dyear.get(k) in (2023, 2024):
            sums[(dyear[k], utype[k])] += float(r["amount"])
    for y, d in fig["ask_b_recovered"].items():
        for t, v in d.items():
            check("ask B %s %s" % (y, t), near(sums[(int(y), t)], 1000) == v, "%.0f" % sums[(int(y), t)])

    # ------------------------------------------------------------------ every format read back
    from pypdf import PdfReader
    txt = " ".join(p.extract_text() for p in PdfReader(J("libranza_empresarial_product_rules_2026.pdf")).pages)
    txt = re.sub(r"\s+", " ", txt)
    check("pdf read back: the rules carry the default definition", "in default from the month-end at which an instalment is 90 or more days past due" in txt)
    check("pdf read back: the rules carry the launch date", "disbursed together on 1 February 2027" in txt)
    stxt = " ".join(p.extract_text() for p in PdfReader(J("supervisor_annual_return_2025.pdf")).pages)
    check("pdf read back: the supervisor return has its table", "90+ days past due" in stxt)
    dic = xlsx_cells(J("data_dictionary.xlsx"))["fields"]
    check("xlsx read back: the dictionary defines SIN SALARIO", any("no salary paid to the member in the month" in str(v)
                                                                   for v in dic.values()))
    gb = xlsx_cells(os.path.join(task, "golden", "libranza_empresarial_default_forecast.xlsx"))
    check("golden workbook: the total", str(gb["Forecast"].get("B4")) == str(fig["call_total"]))
    shares = [int(float(gb["Forecast"]["D%d" % (8 + i)])) for i in range(6)]
    check("golden workbook: the sector shares", shares == [fig["call_share"][s] for s in (
        "contact centres", "retail chains", "security services", "logistics and courier", "food processing",
        "private clinics")])
    z = zipfile.ZipFile(os.path.join(task, "golden", "launch_default_note.docx"))
    doc = re.sub(r"<[^>]+>", "", z.read("word/document.xml").decode())
    check("golden note: states the forecast", "About %d of the 2,400 launch loans" % fig["call_total"] in doc)
    sub = open(os.path.join(task, "submission.md"), encoding="utf-8").read()
    check("submission: block 4 total", "by 31 January 2028: %d." % fig["call_total"] in sub)
    check("submission: no em or en dash", "—" not in sub and "–" not in sub)

    bad = [o for o in OUT if not o[1]]
    for n, g, d in OUT:
        if not g:
            print("FAIL  %s  %s" % (n, d))
    print("verify.py: %s %d of %d" % ("PASS" if not bad else "FAIL", len(OUT) - len(bad), len(OUT)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")))
