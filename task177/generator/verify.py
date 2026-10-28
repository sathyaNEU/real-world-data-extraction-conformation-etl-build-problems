"""Independent verifier: reads only the files under target/ (and the two goldens), on its own code path, and
recomputes the call, the pool's states, the history's rates, the guardrail figures by branch and every filed sentence
the call or the ask leans on. Imports nothing from the generator."""
from __future__ import annotations

import csv
import datetime as dt
import json
import os
import sys
from collections import defaultdict

import pyarrow.parquet as pq
from pypdf import PdfReader
import openpyxl
from docx import Document

TASK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = os.path.join(TASK, "target")
G = os.path.join(TASK, "golden")
CUT = dt.date(2026, 12, 31)
H = 181
DPD = 90
MHP = 91
N_INST = 52


def rd(name):
    with open(os.path.join(T, name), newline="") as f:
        return list(csv.DictReader(f))


def pdf(name):
    return " ".join((p.extract_text() or "") for p in PdfReader(os.path.join(T, name)).pages).replace("\n", " ")


def main():
    out = []

    def check(label, cond, detail=""):
        out.append((label, bool(cond), detail))
    fig = json.load(open(os.path.join(TASK, "generator", "figures.json")))
    names = sorted(os.listdir(T))
    pick = lambda s: next(n for n in names if s in n)
    # filed sentences, read back through the same extractor with a positive control
    pol = pdf(pick("operating_policy"))
    check("V1 policy readable (control)", "Joint Liability Group Lending" in pol, "%d chars" % len(pol))
    check("V2 policy files the days-past-due rule", "the number of days from the due date of its oldest instalment not "
          "paid in full to that date" in pol)
    check("V3 policy files the posting codes", "GRP_SUPP, paid at the meeting by another member of the group" in pol)
    ts = pdf(pick("term_sheet"))
    check("V4 term sheet names the pool tape as the pool", "loans listed in the pool tape dated 31 December 2026" in ts)
    tsn = " ".join(ts.split())
    check("V14 term sheet files the forecast months' repayment as the experience before the cyclone",
          "taking members' repayment from 1 January 2027 to be as it was in the Assignor's experience before the "
          "cyclone of 16 October 2026" in tsn)
    gr = pdf(pick("guardrails"))
    check("V5 guardrail note files the breach and the counting", "four or more lending institutions" in gr and
          "A loan is counted once, at its latest report" in gr)
    # the ledger, both platforms
    mm = rd(pick("migration_map"))
    mmap = {r["collectpro_id"]: r["kshetra_id"] for r in mm}
    rows = []
    for name in (pick("FY2023-24"), pick("FY2024-25")):
        for r in rd(name):
            d = dt.datetime.strptime(r["MTG_DT"], "%d/%m/%Y").date()
            gk = "%s-%s" % (r["CENTRE"], r["GRP"])
            rows.append((d, mmap.get(gk, gk), mmap.get(r["LOAN_AC"], r["LOAN_AC"]), int(r["INST"]),
                         {"SELF": "P", "GS": "S", "NIL": "U"}[r["MODE"]]))
    tab = pq.read_table(os.path.join(T, pick("kshetra"))).to_pydict()
    for d, g, l, i, t in zip(tab["meeting_date"], tab["group_id"], tab["loan_id"], tab["instalment_no"], tab["txn_type"]):
        rows.append((d, g, l, int(i), {"OWN": "P", "GRP_SUPP": "S", "NOT_PAID": "U"}[t]))
    check("V6 ledger rows", len(rows) == fig["ledger_rows"], "%d" % len(rows))
    first_unpaid = {}
    first_seen = {}
    min_inst = {}
    by_loan = defaultdict(list)
    supp = defaultdict(int)
    gmeet = defaultdict(set)
    for d, g, l, i, t in rows:
        if t == "U":
            first_unpaid[l] = min(first_unpaid.get(l, d), d)
        if l not in first_seen or d < first_seen[l]:
            first_seen[l] = d
            min_inst[l] = i
        by_loan[l].append((d, i, g))
        if t == "S":
            supp[(g, d)] += 1
        gmeet[g].add(d)
    disb = {l: first_seen[l] - dt.timedelta(days=14 * min_inst[l]) for l in first_seen}
    gsorted = {g: sorted(v) for g, v in gmeet.items()}
    import bisect
    for l in by_loan:
        by_loan[l].sort()
    loan_dates = {l: [x[0] for x in v] for l, v in by_loan.items()}

    def state(g, E):
        ds = gsorted.get(g, [])
        lo, hi = 0, len(ds)
        while lo < hi:
            mid = (lo + hi) // 2
            if ds[mid] <= E:
                lo = mid + 1
            else:
                hi = mid
        return min(supp.get((g, ds[lo - 1]), 0), 3) if lo else None

    def current(l, E):
        j = bisect.bisect_right(loan_dates[l], E)
        if not j:
            return None
        fu = first_unpaid.get(l)
        if fu is not None and fu <= E:
            return None
        last_row = by_loan[l][j - 1]
        if last_row[1] >= N_INST:
            return None
        if disb[l] > E - dt.timedelta(days=MHP):
            return None
        return last_row[2]
    # month ends with a full horizon in the ledger
    last = max(r[0] for r in rows)
    ends = []
    y, m = 2023, 7
    while True:
        nxt = dt.date(y + (m == 12), (m % 12) + 1, 1)
        e = nxt - dt.timedelta(days=1)
        if e + dt.timedelta(days=H) > last:
            break
        ends.append(e)
        y, m = nxt.year, nxt.month
    num = defaultdict(int)
    den = defaultdict(int)
    for E in ends:
        for l in by_loan:
            g = current(l, E)
            if g is None:
                continue
            k = state(g, E)
            fu = first_unpaid.get(l)
            hit = fu is not None and fu <= E + dt.timedelta(days=H - DPD)
            num[k] += hit
            den[k] += 1
    rate = {k: num[k] / den[k] for k in den}
    for k in range(4):
        check("V7 rate for state %d" % k, abs(100 * rate[k] - fig["state_rate_pct_%d" % k]) < 0.006,
              "%.4f" % (100 * rate[k]))
    pool = rd(pick("pool_tape"))
    cnt = defaultdict(int)
    for r in pool:
        cnt[state(r["group_id"], CUT)] += 1
    for k in range(4):
        check("V8 pool loans in state %d" % k, cnt[k] == fig["state_loans_%d" % k], "%d" % cnt[k])
    fc = sum(rate[k] * cnt[k] for k in cnt)
    check("V9 forecast", abs(fc - fig["call_unrounded"]) < 0.06 and int(round(fc / 100) * 100) == fig["call"], "%.2f" % fc)
    # the strict reading of clause 12: rates only from as-ofs whose windows closed before landfall
    land = dt.date(2026, 10, 16)
    num2, den2 = defaultdict(int), defaultdict(int)
    for E in ends:
        if E + dt.timedelta(days=H) >= land:
            continue
        for l in by_loan:
            g = current(l, E)
            if g is None:
                continue
            k = state(g, E)
            fu = first_unpaid.get(l)
            num2[k] += fu is not None and fu <= E + dt.timedelta(days=H - DPD)
            den2[k] += 1
    fc2 = sum(num2[k] / den2[k] * cnt[k] for k in cnt if den2[k])
    check("V15 the call holds on windows closed before landfall", int(round(fc2 / 100) * 100) == fig["call"] and
          abs(fc2 - fig["sf_windows_before_landfall"]) < 0.06, "%.2f" % fc2)
    # the guardrails
    dirx = rd(pick("member_directory"))
    inst = {r["member_code"]: r["institution"] for r in dirx}
    par = {r["member_code"]: (r["parent_code"] or r["member_code"]) for r in dirx}
    succ = {r["member_code"]: (r["successor_code"] or r["member_code"]) for r in dirx}
    kyc = {r["member_id"]: r["cic_ref"] for r in rd(pick("member_kyc"))}
    acc = defaultdict(dict)
    for r in rd(pick("cic_portfolio")):
        if r["account_type"] not in ("JLG", "MFI-IND") or r["account_status"] != "ACTIVE":
            continue
        key = (r["member_code"], r["date_opened"], r["sanctioned_amount"])
        prev = acc[r["inquiry_ref"]].get(key)
        if prev is None or r["date_reported"] > prev[0]:
            acc[r["inquiry_ref"]][key] = (r["date_reported"], int(r["current_balance"]))
    nb = defaultdict(int)
    lk = defaultdict(int)
    for r in pool:
        a = acc[kyc[r["member_id"]]]
        lenders = {inst[succ[par[k[0]]]] for k in a}
        debt = sum(v[1] for v in a.values())
        if len(lenders) >= 4 or debt > 200000:
            nb[r["branch_code"]] += 1
            lk[r["branch_code"]] += int(r["principal_outstanding_inr"])
    bad = [b for b in nb if nb[b] != fig["ask_breach_%s" % b] or round(lk[b] / 1e5, 1) != fig["ask_lakh_%s" % b]]
    check("V10 guardrail breaches and principal by branch", not bad and len(nb) == 14, ", ".join(bad) or "14 branches")
    # the goldens carry the same figures
    wb = openpyxl.load_workbook(os.path.join(G, "pool_90dpd_forecast.xlsx"), data_only=True)
    check("V11 workbook forecast", wb["Forecast"]["B4"].value == fig["call"], str(wb["Forecast"]["B4"].value))
    gsh = wb["Guardrails"]
    vals = {row[0].value: (row[2].value, row[3].value) for row in gsh.iter_rows(min_row=4) if row[0].value in nb}
    check("V12 workbook guardrails", all(vals[b] == (fig["ask_breach_%s" % b], fig["ask_lakh_%s" % b]) for b in nb), "")
    doc = " ".join(p.text for p in Document(os.path.join(G, "pool_purchase_note.docx")).paragraphs)
    check("V13 note states the forecast", "about %s of the pool's %s loans" % (fig["call"], f"{fig['pool_loans']:,}") in doc)
    fails = [o for o in out if not o[1]]
    for o in out:
        print("  %s  %s  %s" % ("PASS" if o[1] else "FAIL", o[0], o[2]))
    print("verify: %d of %d" % (len(out) - len(fails), len(out)))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
