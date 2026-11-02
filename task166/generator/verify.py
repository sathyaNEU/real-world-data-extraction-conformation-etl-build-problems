"""verify.py: recompute every graded figure from the cut pack on a code path of its own (SQL over the ledger, the csv
module and openpyxl for the rest, no import of calc.py), then compare with generator/figures.json. Exit 1 on any
difference.

    python3 task166/generator/verify.py [target]"""
from __future__ import annotations

import csv
import datetime as dt
import json
import math
import os
import re
import sqlite3
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
YE = dt.date(2026, 10, 31)
FY0 = dt.date(2025, 11, 1)
START = dt.date(2021, 11, 1)
FMT = {"HB": "Hardback", "Hardback": "Hardback", "TPB": "Trade paperback", "Trade Paperback": "Trade paperback",
       "PB": "Paperback", "Paperback": "Paperback"}


def find(target, prefix, ext):
    f = [x for x in os.listdir(target) if x.startswith(prefix) and x.endswith(ext)]
    assert len(f) == 1, (prefix, f)
    return os.path.join(target, f[0])


def d(s):
    s = str(s)[:10]
    if "/" in s:
        dd, mm, yy = s.split("/")
        return dt.date(int(yy), int(mm), int(dd))
    return dt.date.fromisoformat(s)


def clean(isbn):
    return str(isbn).replace("-", "").strip()


def core(t):
    t = str(t).lower().split(":")[0].replace("&", " and ")
    t = " ".join(re.sub(r"[^a-z0-9 ]", " ", t).split())
    for a in ("the ", "a ", "an "):
        if t.startswith(a):
            return t[len(a):]
    return t


def who(c):
    c = str(c).strip()
    if "," in c:
        last, first = c.split(",", 1)
        c = first.strip() + " " + last.strip()
    return " ".join(c.lower().split())


def main(target):
    accts = {}
    legacy = {}
    with open(find(target, "trade_accounts", ".csv"), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            accts[r["account_code"]] = (r["channel"], r["terms"])
            if r["legacy_account_no"]:
                legacy[r["legacy_account_no"]] = r["account_code"]
    from openpyxl import load_workbook
    wb = load_workbook(find(target, "title_master", ".xlsx"), read_only=True)
    ws = wb.worksheets[0]
    it = ws.iter_rows(values_only=True)
    hdr = list(next(it))
    titles = {}
    for row in it:
        r = dict(zip(hdr, row))
        pub = r["pub_date"].date() if hasattr(r["pub_date"], "date") else d(r["pub_date"])
        titles[clean(r["isbn13"])] = (FMT[r["format"]], pub, core(r["title"]), who(r["contributor"]))
    wb.close()
    # each hardback's own paperback: same contributor and title core, published after it
    pbs = defaultdict(list)
    for i, (f, pub, k, c) in titles.items():
        if f == "Paperback":
            pbs[(k, c)].append(pub)
    quick = set()
    for i, (f, pub, k, c) in titles.items():
        if f == "Hardback":
            later = sorted(p for p in pbs.get((k, c), []) if p > pub)
            if later and (later[0] - pub).days / 30.44 <= 8.0:
                quick.add(i)
    con = sqlite3.connect(find(target, "marrowgate_sales_ledger", ".sqlite"))
    T = (YE - dt.date(2020, 11, 2)).days
    day = lambda x: (x - dt.date(2020, 11, 2)).days
    lines = {}
    for no, idate, acct, isbn, qty, net in con.execute(
            "SELECT invoice_no, invoice_date, account_ref, isbn, qty, net_value FROM invoice_lines"):
        a = legacy.get(acct, acct)
        ch, terms = accts[a]
        if terms != "SOR":
            continue
        i = clean(isbn)
        f = titles[i][0]
        seg = (f, ch, i in quick and f == "Hardback")
        lines[no] = (day(d(idate)), seg, qty, net)
    credited = defaultdict(lambda: [0.0] * 71)
    for cdate, inv, q in con.execute("SELECT credit_date, against_invoice, qty FROM credit_lines WHERE reason_code = 'RET'"):
        cd = day(d(cdate))
        if cd > T or inv not in lines:
            continue
        iday, seg, _, _ = lines[inv]
        if iday < day(START) or iday > T - 425:
            continue
        credited[seg][min(70, max(0, (cd - iday) // 7))] += q
    con.close()
    denom = defaultdict(float)
    for iday, seg, qty, net in lines.values():
        if day(START) <= iday <= T - 425:
            denom[seg] += qty
    cum = {}
    for seg, h in credited.items():
        run, out = 0.0, []
        for x in h:
            run += x
            out.append(run / denom[seg])
        cum[seg] = out
    total = hb = 0.0
    for iday, seg, qty, net in lines.values():
        if T - 365 < iday <= T and seg in cum:
            a = min(70, max(0, (T - iday) // 7))
            v = (cum[seg][70] - cum[seg][a]) * net
            total += v
            if seg[0] == "Hardback":
                hb += v
    # ---------------------------------------------------------------- returns received and written off
    auth = {}
    rachan = {}
    with open(find(target, "tallowmere_returns_authorisations", ".csv"), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            auth[(r["ra_number"], clean(r["isbn"]))] = auth.get((r["ra_number"], clean(r["isbn"])), 0) + int(r["qty_authorised"])
            rachan[r["ra_number"]] = accts[r["customer_account"]][0]
    seen_rows = set()
    rows = []
    with open(find(target, "tallowmere_returns_received", ".csv"), encoding="utf-8") as fh:
        rd = csv.reader(fh)
        h = next(rd)
        for r in rd:
            t = tuple(r)
            if t in seen_rows:
                continue
            seen_rows.add(t)
            x = dict(zip(h, r))
            i = clean(x["isbn"])
            if i not in titles:
                continue
            rows.append((d(x["received"]), x["delivery_ref"], x["ra_ref"], i, int(x["qty_received"]), int(x["grade_saleable"]),
                         int(x["grade_hurt"]), int(x["grade_unsaleable"]), x["hurts_tote"]))
    rows.sort(key=lambda r: (r[0], r[1]))
    got = defaultdict(int)
    for r in rows:
        got[(r[2], r[3])] += r[4]
    over = {k: v - auth[k] for k, v in got.items() if k in auth}
    units = defaultdict(list)
    order = []
    for r in rows:
        if r[1] not in units:
            order.append(r[1])
        units[r[1]].append(r)
    keep, sigs = [], set()
    for u in order:
        s = tuple(sorted((r[2], r[3], r[4], r[5], r[6], r[7]) for r in units[u]))
        if s in sigs and all(over.get((a, b), 0) >= q for a, b, q, *_ in s):
            for a, b, q, *_ in s:
                over[(a, b)] -= q
            continue
        sigs.add(s)
        keep += units[u]
    q_of = lambda x: {11: 1, 12: 1, 1: 1, 2: 2, 3: 2, 4: 2, 5: 3, 6: 3, 7: 3, 8: 4, 9: 4, 10: 4}[x.month]
    recv = defaultdict(int)
    for r in keep:
        if FY0 <= r[0] <= YE:
            recv["%s|Q%d" % (rachan[r[2]], q_of(r[0]))] += r[4]
    hurts = defaultdict(int)
    for r in keep:
        if r[8]:
            hurts[r[8]] += r[6]
    wb = load_workbook(find(target, "tallowmere_hurts_reinspection", ".xlsx"), read_only=True)
    ri = defaultdict(list)
    for ws in wb.worksheets:
        it = ws.iter_rows(values_only=True)
        hh = list(next(it))
        for row in it:
            x = dict(zip(hh, row))
            dd = x["inspected"].date() if hasattr(x["inspected"], "date") else d(x["inspected"])
            if dd <= YE:
                ri[str(x["tote"])].append((dd, int(x["qty_inspected"]), int(x["pulped"])))
    wb.close()
    pulped = {}
    for tote, rr in ri.items():
        rr.sort()
        H = hurts.get(tote)
        if len(rr) == 1:
            pulped[tote] = rr[0][2]
        elif H is not None and sum(x[1] for x in rr) == H:
            pulped[tote] = sum(x[2] for x in rr)
        elif H is not None and all(x[1] == H for x in rr):
            pulped[tote] = rr[-1][2]
        else:
            raise SystemExit("unresolved tote %s" % tote)
    wo = defaultdict(lambda: [0.0, 0])
    for r in keep:
        if not (FY0 <= r[0] <= YE):
            continue
        p = pulped.get(r[8], 0) * r[6] / hurts[r[8]] if (r[8] and hurts.get(r[8])) else 0.0
        for key in (("ch", rachan[r[2]]), ("fm", titles[r[3]][0])):
            wo[key][0] += r[7] + p
            wo[key][1] += r[4]
    # ---------------------------------------------------------------- compare
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    r250 = lambda x: int(250000 * math.floor(x / 250000 + 0.5))
    bad = []
    if r250(total) != fig["allowance_gbp"]["value"] or abs(total - fig["allowance_gbp"]["computed"]) > 0.05:
        bad.append(("allowance", total, fig["allowance_gbp"]))
    if r250(hb) != fig["allowance_hardback_gbp"]["value"] or abs(hb - fig["allowance_hardback_gbp"]["computed"]) > 0.05:
        bad.append(("hardback", hb, fig["allowance_hardback_gbp"]))
    for k, v in fig["received_copies"].items():
        if recv.get(k, 0) != v:
            bad.append(("received " + k, recv.get(k, 0), v))
    for k, v in fig["written_off_share_channel_pct"].items():
        x = round(100 * wo[("ch", k)][0] / wo[("ch", k)][1], 1)
        if x != v:
            bad.append(("written off " + k, x, v))
    for k, v in fig["written_off_share_format_pct"].items():
        x = round(100 * wo[("fm", k)][0] / wo[("fm", k)][1], 1)
        if x != v:
            bad.append(("written off " + k, x, v))
    n = 2 + len(fig["received_copies"]) + len(fig["written_off_share_channel_pct"]) + len(fig["written_off_share_format_pct"])
    print("verify: allowance %.2f (%d), hardbacks %.2f (%d); %d graded figures, %d differ" % (total, r250(total), hb, r250(hb), n, len(bad)))
    for b in bad:
        print("  DIFF", b)
    return not bad


if __name__ == "__main__":
    t = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")
    sys.exit(0 if main(t) else 1)
