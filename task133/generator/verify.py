"""Independent check of every graded figure from the shipped bytes only: vectorised numpy over a loan x
month grid, its own date arithmetic, its own scorecard conversion read from the note's worked example."""
import datetime as dt
import os
import re
import sys

import numpy as np
import openpyxl
import pandas as pd
from pypdf import PdfReader

TASK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = os.path.join(TASK, "target")
G = os.path.join(TASK, "golden")


def main():
    bk = pd.read_csv(os.path.join(T, "personal_loan_book_2026-09-30.csv"), parse_dates=["first_repayment_date", "drawdown_date"])
    cv = pd.read_csv(os.path.join(T, "pd_curve_personal_loans_2026-06.csv"), comment="#")
    hd = pd.read_excel(os.path.join(T, "hardship_register_2026-09-30.xlsx"), parse_dates=["arrangement_start", "arrangement_end"])
    sc = openpyxl.load_workbook(os.path.join(T, "ifrs9_scenarios_2026Q3.xlsx"), data_only=True)["Q1 FY27 scenarios"]
    mult = 0.0
    for r in sc.iter_rows(min_row=5, values_only=True):
        if not r or r[0] is None:
            break
        mult += float(r[1]) * float(r[2])
    note = " ".join(p.extract_text() for p in PdfReader(os.path.join(T, "scorecard_v4_migration_note.pdf")).pages)
    a, b = map(float, re.search(r"v4 = ([\d.]+) x v3 - ([\d.]+)", note).groups())
    rep = pd.Timestamp("2026-09-30")
    fr = bk["first_repayment_date"]
    due = (rep.year - fr.dt.year) * 12 + (rep.month - fr.dt.month) + (fr.dt.day <= rep.day).astype(int)
    due = due.clip(lower=0)
    rem = bk["term_months"] - due
    rep_ts = rep
    act = hd[(hd["arrangement_status"] != "Cancelled") & (hd["arrangement_start"] <= rep_ts) & (hd["arrangement_end"] >= rep_ts)]
    o4 = np.where(bk["origination_scorecard"] == "v3", np.floor(a * bk["origination_score"] - b + 0.5), bk["origination_score"])
    st = np.where((bk["days_past_due"] >= 30) | bk["loan_no"].isin(set(act["loan_no"])) | (o4 - bk["current_score_v4"] >= 60), 2, 1)
    st = np.where(bk["days_past_due"] >= 90, 3, st)
    lgd = bk["product"].map({"PL36": 0.70, "PL60": 0.76}).values
    C = {p: g.sort_values("month_on_book")["cumulative_pd"].values for p, g in cv.groupby("product")}
    ecl = np.zeros(len(bk))
    for p in ("PL36", "PL60"):
        idx = np.where((bk["product"] == p).values & (st < 3) & (rem.values > 0))[0]
        cp = C[p]
        aa = due.values[idx]
        rr = rem.values[idx]
        H = np.where(st[idx] == 2, rr, np.minimum(12, rr))
        rate = bk["contract_rate"].values[idx] / 12.0
        bal = bk["current_balance"].values[idx]
        pmt = bal * rate / (1 - (1 + rate) ** (-rr.astype(float)))
        K = np.arange(1, 61)
        kk = K[None, :]
        mask = kk <= H[:, None]
        top = len(cp) - 1
        ia = np.minimum(aa[:, None] + kk, top)
        mp = (cp[ia] - cp[ia - 1]) / (1 - cp[np.minimum(aa, top)])[:, None]
        # balance at the start of month k: bal*(1+i)^(k-1) - pmt*((1+i)^(k-1)-1)/i
        g = (1 + rate)[:, None] ** (kk - 1)
        ead = bal[:, None] * g - pmt[:, None] * (g - 1) / rate[:, None]
        df = (1 + rate)[:, None] ** (-kk)
        scal = np.where(st[idx] == 2, 2.4, 1.0)[:, None]
        e = np.where(mask, mp * scal * mult * lgd[idx][:, None] * ead * df, 0.0)
        ecl[idx] = e.sum(axis=1)
    bk = bk.assign(stage=st, ecl=ecl, year=[str(y) if y >= 2024 else "2023 and earlier" for y in bk["drawdown_date"].dt.year])
    inb = bk[bk["stage"] < 3]
    fails = []

    def chk(name, got, exp, tol):
        ok = got is not None and abs(float(got) - float(exp)) <= tol
        print(("OK  " if ok else "FAIL"), name, got, exp)
        if not ok:
            fails.append(name)

    k = lambda x: int(round(x / 1000.0)) * 1000
    wb = openpyxl.load_workbook(os.path.join(G, "ecl_allowance_2026Q3.xlsx"), data_only=True)
    ws = wb["Allowance"]
    chk("allowance", ws["B4"].value, k(inb["ecl"].sum()), 0)
    chk("stage 1", ws["B5"].value, k(inb[inb.stage == 1]["ecl"].sum()), 0)
    chk("stage 2", ws["B6"].value, k(inb[inb.stage == 2]["ecl"].sum()), 0)
    chk("stage 3 loans", ws["B8"].value, int((bk["stage"] == 3).sum()), 0)
    for r in wb["Stage and product"].iter_rows(min_row=2, values_only=True):
        if not r[0]:
            continue
        s, p = int(r[0][-1]), r[1]
        g = inb[(inb.stage == s) & (inb["product"] == p)]
        chk("loans %s %s" % (r[0], p), r[2], len(g), 0)
        chk("gca %s %s" % (r[0], p), r[3], k(g["current_balance"].sum()), 0)
        chk("allowance %s %s" % (r[0], p), r[4], k(g["ecl"].sum()), 0)
        chk("coverage %s %s" % (r[0], p), r[5], round(100 * g["ecl"].sum() / g["current_balance"].sum(), 2), 0.0001)
    for r in wb["By drawdown year"].iter_rows(min_row=2, values_only=True):
        if r[0] is None:
            continue
        for j, p in ((1, "PL36"), (2, "PL60")):
            g = inb[(inb["year"] == str(r[0])) & (inb["product"] == p)]
            if len(g):
                chk("year %s %s" % (r[0], p), r[j], k(g["ecl"].sum()), 0)
    print("VERIFY", "FAIL" if fails else "PASS", len(fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
