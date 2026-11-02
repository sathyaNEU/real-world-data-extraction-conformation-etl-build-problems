"""task183 verify: an independent recompute of every golden figure from the bundle (target/ and golden/), written
apart from calc.py: its own readers, its own windows and fit, its own An Post and till routines. It reads the
goldens as a grader would (the memo's referral table and the workbook's cells) and fails on any difference."""
from __future__ import annotations

import csv
import datetime as dt
import os
import sys
import zipfile
from collections import defaultdict
from decimal import ROUND_HALF_UP, Decimal

import numpy as np
import openpyxl

FILES = dict(acct="business_account_transactions_2025-01_2026-09.csv",
             ms="merchant_services_daily_trade_2025-01_2026-09.csv", mreg="merchant_register_2026-10.xlsx",
             seg="cash_segment_review_list_2025-26.xlsx", till="till_service_daily_totals_2025-01_2026-09.csv",
             ap="an_post_business_lodgements_2025-10_2026-09.csv", tlog="till_service_z_report_log_2025-10_2026-10.csv")
Y0, Y1 = dt.date(2025, 10, 1), dt.date(2026, 9, 30)


def rows(p):
    with open(p, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def sheet(p):
    ws = openpyxl.load_workbook(p, read_only=True, data_only=True).worksheets[0]
    vals = [r for r in ws.iter_rows(values_only=True)]
    i = next(k for k, r in enumerate(vals) if r and r[0] in ("Customer ID", "MID"))
    head = list(vals[i])
    return [dict(zip(head, r)) for r in vals[i + 1:] if r and r[0] is not None]


def main(target, golden):
    t = lambda k: os.path.join(target, FILES[k])
    seg = sheet(t("seg"))
    mreg = sheet(t("mreg"))
    cust = {s["Customer ID"]: s for s in seg}
    acct = {}
    for s in seg:
        for k in ("Current account", "Second account"):
            if s.get(k):
                acct[str(s[k]).split()[-1]] = s["Customer ID"]
    mid = {str(m["MID"]): m["Customer ID"] for m in mreg}
    seen, lods = set(), defaultdict(list)
    for r in rows(t("acct")):
        if r["Transaction Ref"] in seen or r["Type"] != "LDG":
            seen.add(r["Transaction Ref"])
            continue
        seen.add(r["Transaction Ref"])
        cid = acct.get(r["Account"])
        if not cid:
            continue
        posted = dt.datetime.strptime(r["Posting Date"], "%d/%m/%Y").date()
        if r["Reference"].startswith("AP "):
            dd, mm = r["Reference"].split()[2].split("/")
            y = posted.year - (1 if int(mm) > posted.month else 0)
            day = dt.date(y, int(mm), int(dd))
        else:
            day = posted
        lods[cid].append((day, float(r["Credit"])))
    card = defaultdict(lambda: defaultdict(float))
    for r in rows(t("ms")):
        c = mid.get(r["mid"])
        if c:
            card[c][dt.date.fromisoformat(r["trading_date"])] += (int(r["gross_sales_cent"]) - int(r["refunds_cent"])) / 100
    tillc = defaultdict(float)
    for r in rows(t("till")):
        if Y0 <= dt.date.fromisoformat(r["trading_date"]) <= Y1:
            tillc[r["customer_id"]] += float(r["cash_sales"])
    fig = {}
    for cid in cust:
        ls = sorted(lods[cid])
        y, x = [], []
        for (d0, _), (d1, a) in zip(ls, ls[1:]):
            if Y0 <= d1 <= Y1:
                y.append(a)
                x.append(sum(card[cid].get(d0 + dt.timedelta(days=k), 0.0) for k in range((d1 - d0).days)))
        y, x = np.array(y), np.array(x)
        slope = np.polyfit(x, y, 1)[0]
        lodged = sum(a for d, a in ls if Y0 <= d <= Y1)
        fig[cid] = (lodged - tillc[cid]) if cust[cid]["Till service"] == "Yes" else (y.sum() - slope * x.sum())
    ref = sorted((c for c in fig if fig[c] > 40000), key=lambda c: -fig[c])
    bins = {c: int(5000 * round(fig[c] / 5000)) for c in ref}
    # the memo's referral table
    with zipfile.ZipFile(os.path.join(golden, "fci_referrals_jan2027.docx")) as z:
        doc = z.read("word/document.xml").decode("utf-8")
    bad = [c for c in ref if c not in doc or ("EUR %s" % format(bins[c], ",")) not in doc]
    # An Post and the till service
    months = [(Y0.replace(day=1) + dt.timedelta(days=31 * k)).strftime("%Y-%m") for k in range(12)]
    ap = defaultdict(lambda: [0.0, 0.0])
    refs = set()
    for r in rows(t("ap")):
        if r["ap_ref"] in refs:
            continue
        refs.add(r["ap_ref"])
        n, c = float(r["notes_eur"]), float(r["coin_eur"])
        cash = n if round(n * 100) % 500 else n + c
        ap[r["counter_date"][:7]][0] += cash
        fee = (Decimal("1.15") + Decimal("0.00065") * Decimal("%.2f" % cash)).quantize(Decimal("0.01"), ROUND_HALF_UP)
        ap[r["counter_date"][:7]][1] += float(fee)
    tl = rows(t("tlog"))
    by = defaultdict(lambda: defaultdict(list))
    for r in tl:
        by[r["till_account"]][r["received_at"]].append(r)
    till = defaultdict(lambda: [0.0, 0.0])
    for ta, groups in by.items():
        cid = next(iter(groups.values()))[0]["customer_id"]
        days = sorted(d for d, v in card[cid].items() if v > 0)
        prev = None
        for at_s in sorted(groups):
            at = dt.datetime.strptime(at_s, "%Y-%m-%d %H:%M:%S")
            hi = at.date() - dt.timedelta(days=1) if at.hour < 12 else at.date()
            lo = prev if prev else hi - dt.timedelta(days=30)
            cand = [d for d in days if lo < d <= hi]
            for r in sorted(groups[at_s], key=lambda r: int(r["z_no"])):
                d = next(d for d in cand if abs(card[cid][d] - float(r["card_sales"])) < 0.005 and (prev is None or d > prev))
                prev = d
                till[d.strftime("%Y-%m")][0] += float(r["cash_sales"])
                till[d.strftime("%Y-%m")][1] += float(r["paid_outs"])
    wb = openpyxl.load_workbook(os.path.join(golden, "cash_review_2026.xlsx"), data_only=True)
    a_rows = [r for r in wb["An Post"].iter_rows(min_row=5, values_only=True) if r[0] and r[0] != "Year"]
    t_rows = [r for r in wb["Till service"].iter_rows(min_row=5, values_only=True) if r[0] and r[0] != "Year"]
    errs = list(bad)
    for m, ra, rt in zip(months, a_rows, t_rows):
        if abs(ra[1] - round(ap[m][0], 2)) > 0.005 or abs(ra[2] - round(ap[m][1], 2)) > 0.005:
            errs.append("An Post %s" % m)
        if abs(rt[1] - round(till[m][0], 2)) > 0.005 or abs(rt[2] - round(till[m][1], 2)) > 0.005:
            errs.append("till %s" % m)
    if len(a_rows) != 12 or len(t_rows) != 12:
        errs.append("workbook months")
    print("verify: referrals %s at %s; %d An Post and %d till months recomputed; %d differences" % (
        ref, [bins[c] for c in ref], len(a_rows), len(t_rows), len(errs)))
    if errs:
        print("  " + ", ".join(errs))
        raise SystemExit(1)


if __name__ == "__main__":
    task = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(task, "target"),
         sys.argv[2] if len(sys.argv) > 2 else os.path.join(task, "golden"))
