"""The independent verifier: recomputes every graded figure from target/ alone, with its own readers and none of the
generator's modules, and compares with generator/figures.json and the golden workbook.

    python3 task485/generator/verify.py
"""
import csv
import datetime as dt
import json
import math
import os
import re
import sys

import openpyxl
import pdfplumber

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
GOLD = os.path.join(TASK, "golden")
MS, MSO2, MCACO3 = 32.065, 64.066, 100.087
N, BAD = [0], []


def ok(label, cond, detail=""):
    N[0] += 1
    if not cond:
        BAD.append(label)
    print("%s  %s%s" % ("ok  " if cond else "FAIL", label, ("  (" + detail + ")") if detail else ""))


def ten(x):
    return int(math.floor(x / 10.0 + 0.5) * 10)


def hundred(x):
    return int(math.floor(x / 100.0 + 0.5) * 100)


def r1(x):
    return math.floor(x * 10 + 0.5) / 10.0


def date(s):
    s = str(s)[:10]
    return dt.date.fromisoformat(s) if "-" in s else dt.datetime.strptime(s, "%d/%m/%Y").date()


def read_csv(name):
    with open(os.path.join(T, name), newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def text(name):
    with pdfplumber.open(os.path.join(T, name)) as p:
        return "\n".join(pg.extract_text() or "" for pg in p.pages)


def main():
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    y0, y1 = dt.date(2026, 1, 1), dt.date(2026, 12, 31)
    # the register: permit, operator, unit, ash retention
    reg = {}
    for r in openpyxl.load_workbook(os.path.join(T, "permitted_boilers_register_2026.xlsx"),
                                    read_only=True)["Register"].iter_rows(min_row=2, values_only=True):
        if r[0]:
            reg[r[0]] = dict(op=r[1], unit=r[2], ret=r[11] / 100.0, design=r[10] / 100.0)
    ok("register: 18 permitted coal boilers at 16 sites", len(reg) == 18 and len({v["op"] for v in reg.values()}) == 16)
    # coal: each site's 2026 receipts, sulphur weighted by tonnes
    cust = {}
    for r in read_csv("coal_supplier_customers.csv"):
        cust[(r["Supplier"], r["Customer Code"])] = r["Customer"]
    num, den = {}, {}
    rows = read_csv("coal_deliveries_2026.csv")
    for r in rows:
        rec = date(r["Received"])
        if not (y0 <= rec <= y1):
            continue
        site = cust[(r["Supplier"], r["Customer Code"])]
        t = float(r["Net Tonnes"])
        num[site] = num.get(site, 0.0) + t * float(r["Total Sulphur % (ar)"])
        den[site] = den.get(site, 0.0) + t
    S = {k: num[k] / den[k] for k in num}
    ok("coal: every site has 2026 receipts", len(S) == 16)
    # the returns: coal burned and silo stocks by permit, read by header in both templates
    wb = openpyxl.load_workbook(os.path.join(T, "boiler_returns_2026.xlsx"), read_only=True)
    coal, ls = {}, {}
    for q in range(1, 5):
        it = wb["Q%d 2026" % q].iter_rows(values_only=True)
        head = list(next(it))
        col = {h: i for i, h in enumerate(head)}
        pk = "Permit No" if "Permit No" in col else "Permit reference"
        ck = "Coal burned (t)" if "Coal burned (t)" in col else "Fuel fired: coal (tonnes)"
        lo = "Reagent held at start of quarter (t)" if q <= 2 else "Limestone in silo, opening (tonnes)"
        lc = "Reagent held at end of quarter (t)" if q <= 2 else "Limestone in silo, closing (tonnes)"
        for r in it:
            if not r[0]:
                continue
            coal[r[col[pk]]] = coal.get(r[col[pk]], 0) + r[col[ck]]
            ls.setdefault(r[col[pk]], {})[q] = (r[col[lo]], r[col[lc]])
    ok("returns: four quarters for every boiler", all(len(v) == 4 for v in ls.values()) and len(ls) == 18)
    # limestone: tickets to permits, each at its ISO week's certificate
    wbc = openpyxl.load_workbook(os.path.join(T, "limestone_certificates_2026.xlsx"), read_only=True)
    pur = {}
    for q, sh in (("Bromscar Quarry", "Bromscar weekly"), ("Molhope Lime and Stone", "Molhope weekly")):
        pur[q] = {r[0]: r[2] for r in wbc[sh].iter_rows(min_row=2, values_only=True) if r[0]}
    dp = {}
    for r in wbc["Delivery points"].iter_rows(min_row=2, values_only=True):
        if r[0]:
            dp[(r[0], r[1], r[3])] = r[4]
    tons, caco3 = {}, {}
    for r in read_csv("limestone_tickets_2026.csv"):
        p = dp[(r["Quarry"], r["Account"], r["Delivery Point"])]
        d = date(r["Date"])
        wk = d.isocalendar()[1]
        t = float(r["Net t"])
        tons[p] = tons.get(p, 0.0) + t
        caco3[p] = caco3.get(p, 0.0) + t * pur[r["Quarry"]][wk] / 100.0
    # the guarantees' stoichiometry, parsed from the schedules
    g = text("scrubber_guarantee_schedules.pdf")
    ratio = {}
    for m in re.finditer(r"(NPA/CB/\d{4})", g):
        tail = g[m.end():m.end() + 400]
        n = re.search(r"([\d,]{5,}) ([\d,]{3,}) (\d{2}\.\d) ([\d,]+) (\d\.\d{2}) ", tail)
        if n and m.group(1) not in ratio:
            ratio[m.group(1)] = float(n.group(5))
    ok("guarantees: a stoichiometry for each of the 18 permits", len(ratio) == 18,
       ", ".join(sorted(set("%.2f" % v for v in ratio.values()))))
    # the balance
    so2, formed, removed = {}, {}, {}
    for p, v in reg.items():
        s_gas = coal[p] * S[v["op"]] / 100.0 * (1 - v["ret"])
        used = tons[p] - (ls[p][4][1] - ls[p][1][0])
        ca = caco3[p] / tons[p] * used
        formed[p] = s_gas * MSO2 / MS
        removed[p] = ca / MCACO3 / ratio[p] * MSO2
        so2[p] = formed[p] - removed[p]
    listed = sorted(p for p in so2 if so2[p] >= 250)

    def label(p):
        v = reg[p]
        two = sum(1 for x in reg.values() if x["op"] == v["op"]) > 1
        if not two:
            return v["op"]
        u = v["unit"]
        return "%s %s" % (v["op"], u[0].lower() + u[1:]) if u.startswith("Boiler") else "%s %s" % (v["op"], u)
    want = sorted(figs["call"]["listed"])
    ok("call: the boilers at or over 250 tonnes are the write-up's six", sorted(label(p) for p in listed) == want,
       ", ".join(sorted(label(p) for p in listed)))
    for p in sorted(so2):
        f = figs["boilers"][label(p)]
        ok("%s: %s tonnes, %s" % (label(p), ten(so2[p]), "listed" if so2[p] >= 250 else "not listed"),
           f["so2"] == ten(so2[p]) and f["listed"] == ("listed" if so2[p] >= 250 else "not listed"))
    ok("component: sulphur dioxide formed, to the nearest 100", figs["components"]["formed"] == hundred(sum(formed.values())),
       "{:,}".format(hundred(sum(formed.values()))))
    ok("component: sulphur dioxide removed, to the nearest 100", figs["components"]["removed"] ==
       hundred(sum(removed.values())), "{:,}".format(hundred(sum(removed.values()))))
    ok("step 1: coal burned in all", figs["components"]["coal"] == round(sum(coal.values())),
       "{:,}".format(round(sum(coal.values()))))
    # the default path: each test's removal carried over the year
    rem = {}
    for f in ("scrubber_tests_2026_iverstow.pdf", "scrubber_tests_2026_jarrness.pdf"):
        s = text(f)
        rep_permit = dict(re.findall(r"((?:IET/26/|JST-2026-)\d+).*?(NPA/CB/\d{4})", s))
        for rep, val in re.findall(r"((?:IET/26/|JST-2026-)\d+) [\d,]+ [\d,]+ [\d,]+ (\d{2}\.\d)", s):
            rem[rep_permit[rep]] = float(val) / 100.0
    tested = {p: coal[p] * S[reg[p]["op"]] / 100.0 * (1 - reg[p]["ret"]) * (1 - rem[p]) * MSO2 / MS for p in reg}
    ok("default path: the tested removal over the year lists Candrigg Soda Works alone",
       [label(p) for p in tested if tested[p] >= 250] == ["Candrigg Soda Works"] and len(rem) == 18)
    # the ask: the three ash exports, a Whinmoss line billing a local job dropped
    xref = {}
    for r in read_csv("ash_contractor_customers.csv"):
        ops = {reg[p.strip()]["op"] for p in r["Permit Numbers"].split(";")}
        xref[(r["Contractor"], r["Customer as recorded"])] = ops.pop()
    tol = read_csv("carnhope_jobs_2026.csv")
    gre = [r for r in openpyxl.load_workbook(os.path.join(T, "pellrigg_dockets_2026.xlsx"),
                                             read_only=True)["Dockets"].iter_rows(min_row=2, values_only=True) if r[0]]
    local_jobs = {r["Job No"] for r in tol} | {r[0] for r in gre}
    tot, rec = {}, {}

    def add(site, d, t, dest, material):
        if not (y0 <= d <= y1) or "ash" not in material.lower() and "pfa" not in material.lower():
            return
        tot[site] = tot.get(site, 0.0) + t
        if "Yarrdale" in dest or "Velthwaite" in dest:
            rec[site] = rec.get(site, 0.0) + t
    for r in openpyxl.load_workbook(os.path.join(T, "whinmoss_invoice_lines_2026.xlsx"),
                                    read_only=True)["Invoice lines"].iter_rows(min_row=2, values_only=True):
        if not r[0] or r[10] in local_jobs:
            continue
        add(xref[("Whinmoss Waste Haulage", r[3])], date(r[1]), float(r[6]), r[5], r[5])
    for r in tol:
        add(xref[("Carnhope Skips", r["Site"])], date(r["Date"]), int(r["Net kg"]) / 1000.0, r["Destination"],
            r["Material"])
    for r in gre:
        add(xref[("Pellrigg and Sons Haulage", r[2])], date(r[1]), float(r[5]), r[4], r[3])
    for site in sorted(tot):
        f = figs["ash"][site]
        ok("ask A %s: %s tonnes, %.1f per cent" % (site, "{:,}".format(ten(tot[site])), r1(100 * rec[site] / tot[site])),
           f["t"] == ten(tot[site]) and abs(f["rec"] - r1(100 * rec[site] / tot[site])) < 1e-9)
    ok("ask A: sixteen sites", len(tot) == 16)
    # the golden workbook carries the same figures
    wg = openpyxl.load_workbook(os.path.join(GOLD, "sulphur_dioxide_order_schedule_2027.xlsx"), read_only=True)
    sched = {r[0]: r for r in wg["Schedule"].iter_rows(min_row=5, values_only=True) if r[0] and str(r[0]).startswith("NPA")}
    ok("golden workbook: every boiler's tonnes and listing as verified",
       all(sched[p][10] == ten(so2[p]) and (sched[p][11] == "Listed") == (so2[p] >= 250) for p in reg))
    ash = {r[0]: r for r in wg["Ash 2026"].iter_rows(min_row=5, values_only=True) if r[0] in tot}
    ok("golden workbook: every site's ash and recovery share as verified",
       all(ash[s][2] == ten(tot[s]) and abs(ash[s][3] - r1(100 * rec[s] / tot[s])) < 1e-9 for s in tot))
    md = open(os.path.join(TASK, "submission.md")).read()
    ok("submission.md: every boiler's line as verified", all(
        "   - %s: %s tonnes, %s" % (label(p), "{:,}".format(ten(so2[p])), "listed" if so2[p] >= 250 else "not listed") in md
        for p in reg))
    ok("submission.md: every site's ash line as verified", all(
        "   - %s: %s tonnes, %.1f per cent" % (s, "{:,}".format(ten(tot[s])), r1(100 * rec[s] / tot[s])) in md for s in tot))
    print("\n%d of %d verified" % (N[0] - len(BAD), N[0]))
    if BAD:
        sys.exit(1)


if __name__ == "__main__":
    main()
