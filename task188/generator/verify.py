#!/usr/bin/env python3
"""Independent verifier for task188: reads only the shipped bundle (target/ and golden/) and recomputes every
graded figure on its own code path, with a positive control on every format, then checks the golden
deliverables and figures.json against it.

    python3 task188/generator/verify.py

It imports nothing from the generator. Exit 1 on any mismatch.
"""
import datetime as dt
import json
import os
import re
import sys
import zipfile
from zoneinfo import ZoneInfo

import docx
import numpy as np
import openpyxl
import pandas as pd
from pypdf import PdfReader

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
GOLD = os.path.join(TASK, "golden")
PAC = ZoneInfo("America/Vancouver")
OUT = []


def ok(label, cond, detail=""):
    OUT.append((label, bool(cond), detail))


def r1k(x):
    return int(round(x / 1000.0)) * 1000


def r25k(x):
    return int(round(x / 25000.0)) * 25000


def local(ts):
    return ts.tz_localize("UTC").tz_convert(PAC)


def main():
    # ---- positive controls, one per format --------------------------------------------------------------
    pdf = PdfReader(os.path.join(T, "compliance", "hrcu_aml_atf_compliance_programme_v6-1.pdf"))
    text = " ".join(pg.extract_text() for pg in pdf.pages)
    text = re.sub(r"\s+", " ", text)
    ok("control pdf: the programme's case acceptance sentence reads", "by at least twice the cash that trade produced" in text)
    ok("control pdf: the window convention reads", "received when its bag is opened and counted" in text)
    tor = docx.Document(os.path.join(T, "compliance", "aml_compliance_committee_terms_of_reference.docx"))
    ok("control docx: the terms of reference read", any("up to four new enhanced investigations" in p.text for p in tor.paragraphs))
    reg = openpyxl.load_workbook(os.path.join(T, "membership", "member_register_2026-12-31.xlsx"), read_only=True)
    ok("control xlsx: the register's two sheets", reg.sheetnames == ["Members", "Accounts"], reg.sheetnames)
    post = pd.read_csv(os.path.join(T, "core_banking", "hrcu_business_postings_2026.csv"),
                       dtype={"account_number": str, "transit": str, "terminal_id": str})
    ok("control csv: postings read", len(post) > 300_000 and "cash_portion" in post.columns, len(post))

    # ---- the call ------------------------------------------------------------------------------------------
    members = pd.DataFrame(list(reg["Members"].iter_rows(min_row=2, values_only=True)),
                           columns=[c.value for c in next(reg["Members"].iter_rows(max_row=1))])
    accounts = pd.DataFrame(list(reg["Accounts"].iter_rows(min_row=2, values_only=True)),
                            columns=[c.value for c in next(reg["Accounts"].iter_rows(max_row=1))])
    owner = dict(zip(accounts.account_number.astype(str), accounts.member_number))
    post["m"] = post.account_number.map(owner)
    post["eff"] = pd.to_datetime(post.effective_date)
    yr = post[post.eff.dt.year == 2026]
    cashcodes = {"DEP", "ATMD", "NDEP", "COIN"}
    cash = yr[yr.transaction_code.isin(cashcodes)].groupby("m").cash_portion.sum()
    d = yr.description.fillna("")
    card = yr[d.str.match(r"^(CASCADIA MERCH DEP|NORTHGATE PAY STLMT) ")].groupby("m").credit.sum()
    seg = members.set_index("member_number")
    tab = pd.DataFrame({"cash": cash, "card": card}).reindex(seg.index).fillna(0.0)
    tab["type"] = seg.business_type_code
    tab["name"] = seg.operating_name
    ratio = (tab.cash / tab.card).groupby(tab.type).median()
    tab["produced"] = tab.type.map(ratio) * tab.card
    tab["excess"] = tab.cash - tab.produced
    meets = tab[(tab.excess >= 100_000) & (tab.excess >= 2 * tab.produced)].sort_values("excess", ascending=False)
    near = tab.drop(meets.index).excess.idxmax()
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    ref = figs["call"]["referred"]
    ok("call: the same members in the same order", list(meets.name) == [r["name"] for r in ref], list(meets.name))
    for r in ref:
        i = r["member_number"]
        ok("call: %s cash paid in" % r["name"], r1k(tab.cash[i]) == r["cash_paid_in"], (r1k(tab.cash[i]), r["cash_paid_in"]))
        ok("call: %s produced cash" % r["name"], r25k(tab.produced[i]) == r["produced"])
        ok("call: %s excess" % r["name"], r25k(tab.excess[i]) == r["excess"])
    ok("call: the largest excess not meeting the test", tab.name[near] == figs["call"]["near_miss"]["name"])

    # ---- reports required, filed and late ------------------------------------------------------------------
    c = post[post.transaction_code.isin(cashcodes) & (post.cash_portion > 0) & post.m.notna()].copy()
    c["t"] = pd.to_datetime(c.posted_at_utc.str.rstrip("Z"))
    c = c.sort_values(["m", "t", "posting_id"])
    req = {1: 0, 2: 0, 3: 0, 4: 0}
    for m, sub in c.groupby("m"):
        t0, tot = None, 0.0
        opened = []
        for t, v in zip(sub.t, sub.cash_portion):
            if t0 is None or t >= t0 + pd.Timedelta(hours=24):
                if t0 is not None and tot >= 10_000:
                    opened.append(t0)
                t0, tot = t, 0.0
            tot += v
        if t0 is not None and tot >= 10_000:
            opened.append(t0)
        for t in opened:
            lt = local(t)
            if lt.year == 2026:
                req[(lt.month - 1) // 3 + 1] += 1
    lg = pd.read_csv(os.path.join(T, "compliance", "lctr_submissions_2026.csv"), dtype={"account_number": str})
    lg = lg[lg.account_number.isin(set(owner)) & (lg.report_version == "Original")].drop_duplicates("report_reference")
    lg["td"] = pd.to_datetime(lg.transaction_date)
    lg = lg[lg.td.dt.year == 2026]
    first = c.groupby(["account_number", c.eff.dt.date]).t.min()
    rec = [local(first[(a, x.date())]).date() for a, x in zip(lg.account_number, lg.td)]
    lg["late"] = [(dt.date.fromisoformat(s) - r_).days > 15 for s, r_ in zip(lg.submitted_date, rec)]
    q = lg.td.dt.quarter
    for k in (1, 2, 3, 4):
        f = figs["lctr"]["Q%d 2026" % k]
        ok("lctr Q%d required" % k, req[k] == f["required"], (req[k], f["required"]))
        ok("lctr Q%d filed" % k, int((q == k).sum()) == f["filed"], (int((q == k).sum()), f["filed"]))
        ok("lctr Q%d late" % k, int(((q == k) & lg.late).sum()) == f["late"], (int(((q == k) & lg.late).sum()), f["late"]))

    # ---- branch cash through deposit ATMs and in night depositories -----------------------------------------
    fac = openpyxl.load_workbook(os.path.join(T, "branch_network", "branch_atm_depository_directory.xlsx"), read_only=True)
    atm_rows = list(fac["ATMs"].iter_rows(min_row=2, values_only=True))
    dep_rows = list(fac["Night depositories"].iter_rows(min_row=2, values_only=True))
    hist = {}
    for tid, loc, tr, inst, rem, takes in atm_rows:
        hist.setdefault(tid, []).append((inst.date() if hasattr(inst, "date") else inst, tr))
    depot = {r[0]: r[1] for r in dep_rows}
    cit = pd.read_csv(os.path.join(T, "cash_services", "cit_pickup_manifests_2026.csv"))
    pick = {(b, dd): depot[x] for b, dd, x in zip(cit.bag_number, cit.pickup_date, cit.depository_id)}
    atm = {}
    night = {}
    y2 = yr[yr.transaction_code.isin(cashcodes)]
    for ch, tr, tid, desc, v, ts, e in zip(y2.channel, y2.transit, y2.terminal_id, y2.description, y2.cash_portion,
                                           y2.posted_at_utc, y2.eff):
        if ch == "ATM":
            day = local(pd.Timestamp(ts.rstrip("Z"))).date()
            site = [b for (i0, b) in sorted(hist[tid]) if i0 <= day][-1]
            atm[site] = atm.get(site, 0.0) + v
        elif ch == "NIGHT":
            if tr != "19004":
                night[tr] = night.get(tr, 0.0) + v
            else:
                bag = int(re.search(r"BAG (\d+)", desc).group(1))
                b = pick[(bag, e.date().isoformat())]
                night[b] = night.get(b, 0.0) + v
    for b, f in figs["branch_cash"].items():
        ok("branch %s ATMs" % b, r1k(atm.get(b, 0.0)) == f["atm"], (r1k(atm.get(b, 0.0)), f["atm"]))
        ok("branch %s night depository" % b, r1k(night.get(b, 0.0)) == f["night"], (r1k(night.get(b, 0.0)), f["night"]))

    # ---- the golden deliverables carry the same figures -------------------------------------------------------
    memo = docx.Document(os.path.join(GOLD, "fiu_referral_slate_2027q1.docx"))
    t0 = memo.tables[0]
    rows = [[c_.text for c_ in r.cells] for r in t0.rows[1:]]
    ok("memo: the slate names the referred in order", [r[1] for r in rows] == [r["name"] for r in ref])
    for r, row in zip(ref, rows):
        ok("memo: %s figures" % r["name"], row[3:] == ["CAD {:,}".format(r["cash_paid_in"]), "CAD {:,}".format(r["produced"]),
                                                       "CAD {:,}".format(r["excess"])], row)
    body = " ".join(p.text for p in memo.paragraphs)
    ok("memo: names the largest excess not referred", figs["call"]["near_miss"]["name"] in body)
    t1 = memo.tables[1]
    for k, row in zip((1, 2, 3, 4), t1.rows[1:]):
        f = figs["lctr"]["Q%d 2026" % k]
        ok("memo: LCTR Q%d" % k, [c_.text for c_ in row.cells][1:] == [str(f["required"]), str(f["filed"]), str(f["late"])])
    t2 = memo.tables[2]
    for row in t2.rows[1:]:
        cells = [c_.text for c_ in row.cells]
        b = re.search(r"\((\d{5})\)", cells[0]).group(1)
        f = figs["branch_cash"][b]
        ok("memo: branch %s" % b, cells[1:] == ["{:,}".format(f["atm"]), "{:,}".format(f["night"])], cells)
    wb = openpyxl.load_workbook(os.path.join(GOLD, "member_cash_review_2026.xlsx"), read_only=True)
    ws = wb["Members 2026"]
    vals = list(ws.iter_rows(min_row=5, values_only=True))
    by = {v[0]: v for v in vals if v and isinstance(v[0], int)}
    ok("workbook: every member listed once", len(by) == len(seg), len(by))
    for r in ref:
        v = by[r["member_number"]]
        ok("workbook: %s" % r["name"], (v[3], v[5], v[6], v[8]) == (r["cash_paid_in"], r["produced"], r["excess"], "Yes"), v)
    ok("workbook: only the referred meet the test", sorted(k for k, v in by.items() if v[8] == "Yes") ==
       sorted(r["member_number"] for r in ref))
    ok("workbook: every member's cash paid in", all(v[3] == r1k(tab.cash[k]) for k, v in by.items()))
    png = open(os.path.join(GOLD, "cash_review_2026.png"), "rb").read()
    ok("chart: a PNG with no software stamp", png[:8] == b"\x89PNG\r\n\x1a\n" and b"matplotlib" not in png.lower())

    fails = [o for o in OUT if not o[1]]
    for lab, good, detail in OUT:
        if not good:
            print("FAIL  %s  %s" % (lab, detail))
    print("verify: %d checks, %d FAIL" % (len(OUT), len(fails)))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
