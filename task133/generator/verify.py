"""Independent check of every graded figure and every rung and stop, from the shipped bytes only: vectorised numpy over a
loan x month grid for the allowance, plain dictionaries and the csv module for the two asks, its own date arithmetic and
its own scorecard conversion read from the migration note. Nothing here imports the generator."""
import csv
import datetime as dt
import os
import re
import sys
from collections import defaultdict

import numpy as np
import openpyxl
import pandas as pd
from pypdf import PdfReader

TASK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = os.path.join(TASK, "target")
G = os.path.join(TASK, "golden")
REP = dt.date(2026, 9, 30)
JUNE = dt.date(2026, 6, 30)


def read_inputs(target):
    bk = pd.read_csv(os.path.join(target, "personal_loan_book_2026-09-30.csv"), parse_dates=["first_repayment_date", "drawdown_date"])
    cv = pd.read_csv(os.path.join(target, "pd_curve_personal_loans_2026-06.csv"), comment="#")
    dev = pd.read_parquet(os.path.join(target, "pd_model_development_sample.parquet"))
    hd = pd.read_excel(os.path.join(target, "hardship_register_2026-09-30.xlsx"),
                       parse_dates=["arrangement_start", "arrangement_end", "cancelled_date"])
    sc = openpyxl.load_workbook(os.path.join(target, "ifrs9_scenarios_2026Q3.xlsx"), data_only=True)["Q1 FY27 scenarios"]
    mult = 0.0
    for r in sc.iter_rows(min_row=5, values_only=True):
        if not r or r[0] is None:
            break
        mult += float(r[1]) * float(r[2])
    note = " ".join(p.extract_text() for p in PdfReader(os.path.join(target, "scorecard_v4_migration_note.pdf")).pages)
    a, b = map(float, re.search(r"v4 = ([\d.]+) x v3 - ([\d.]+)", note).groups())
    return bk, cv, dev, hd, mult, (a, b)


def in_force(hd, day):
    day = pd.Timestamp(day)
    sel = (hd["arrangement_start"] <= day) & (hd["arrangement_end"] >= day) & (hd["cancelled_date"].isna() | (hd["cancelled_date"] > day))
    return set(hd.loc[sel, "loan_no"])


def stages(frame, hd, conv, day, score):
    a, b = conv
    o4 = np.where(frame["origination_scorecard"] == "v3", np.floor(a * frame["origination_score"] - b + 0.5), frame["origination_score"])
    fall = o4 - np.asarray(score, float)
    hard = frame["loan_no"].isin(in_force(hd, day)).to_numpy()
    st = np.where((frame["days_past_due"].to_numpy() >= 30) | hard | (np.nan_to_num(fall, nan=-1e9) >= 60), 2, 1)
    return np.where(frame["days_past_due"].to_numpy() >= 90, 3, st)


def allowance(target, how="cond"):
    """the collective allowance by stage under one reading of the curve: 'cond' (the answer), 'r4', 'shift', 'uncond',
    'hazard', 'r4b', or 'clprev' ('cond' with a loan repaid in full during month a read as still on the books at a)"""
    bk, cv, dev, hd, mult, conv = read_inputs(target)
    rep = pd.Timestamp(REP)
    fr = bk["first_repayment_date"]
    due = (rep.year - fr.dt.year) * 12 + (rep.month - fr.dt.month) + (fr.dt.day <= rep.day).astype(int)
    due = due.clip(lower=0)
    rem = (bk["term_months"] - due).where(bk["term_months"] - due > 0, 1)
    pos = (bk["term_months"] - rem).to_numpy()
    st = stages(bk, hd, conv, REP, bk["current_score_v4"])
    lgd = bk["product"].map({"PL36": 0.70, "PL60": 0.76}).to_numpy()
    C = {p: g.sort_values("month_on_book")["cumulative_pd"].to_numpy() for p, g in cv.groupby("product")}
    gone, dflt = {}, {}
    for p, g in dev.groupby("product"):
        n = len(g)
        tm = int(g["term_months"].max())
        cnt = np.bincount(g.loc[g["outcome"] != "default", "outcome_month_on_book"].to_numpy(), minlength=tm + 1)
        gone[p] = np.cumsum(cnt) / n                       # repaid in full, early or at term, by the end of each month
        cd = np.bincount(g.loc[g["outcome"] == "default", "outcome_month_on_book"].to_numpy(), minlength=tm + 1)
        dflt[p] = np.cumsum(cd) / n                        # the sample's own default share, unsmoothed
    ecl = np.zeros(len(bk))
    for p in ("PL36", "PL60"):
        idx = np.where((bk["product"] == p).to_numpy() & (st < 3))[0]
        c, cl = C[p], gone[p]
        if how == "samplecurve":                           # the curve rebuilt from the sample, unsmoothed
            c = dflt[p]
        if how == "clprev":
            cl = np.concatenate([[0.0], cl[:-1]])
        top = len(c) - 1
        aa, rr = pos[idx], rem.to_numpy()[idx]
        H = np.where(st[idx] == 2, rr, np.minimum(12, rr))
        kk = np.arange(1, 61)[None, :]
        mask = kk <= H[:, None]
        m = np.minimum(aa[:, None] + kk, top)
        inc = c[m] - c[m - 1]
        surv_a = (1 - (dflt[p] if how == "sampleS" else c)[aa] - cl[aa])[:, None]
        surv_prev = 1 - c[m - 1] - cl[m - 1]
        if how in ("cond", "r4b", "clprev", "sampleS", "samplecurve"):
            mp = inc / surv_a
        elif how == "r4":
            mp = inc / (1 - c[aa])[:, None]
        elif how == "shift":
            mp = inc
        elif how == "uncond":
            kc = np.minimum(kk, top).repeat(len(idx), 0)
            mp = np.where(kk <= top, c[kc] - c[kc - 1], 0.0)
        elif how == "hazard":
            h = np.where(mask, inc / surv_prev, 0.0)
            mp = h * np.cumprod(np.hstack([np.ones((len(idx), 1)), 1 - h[:, :-1]]), axis=1)
        else:
            raise ValueError(how)
        rate = bk["contract_rate"].to_numpy()[idx] / 12.0
        bal = bk["current_balance"].to_numpy()[idx]
        pmt = bal * rate / (1 - (1 + rate) ** (-rr.astype(float)))
        g = (1 + rate)[:, None] ** (kk - 1)
        ead = bal[:, None] * g - pmt[:, None] * (g - 1) / rate[:, None]
        if how == "r4b":
            q = np.where(mask, (cl[m] - cl[m - 1]) / surv_prev, 0.0)
            ead = ead * np.cumprod(np.hstack([np.ones((len(idx), 1)), 1 - q[:, :-1]]), axis=1)
        df = (1 + rate)[:, None] ** (-kk)
        scal = np.where(st[idx] == 2, 2.4, 1.0)[:, None]
        ecl[idx] = np.where(mask, mp * scal * mult * lgd[idx][:, None] * ead * df, 0.0).sum(axis=1)
    out = {"total": ecl[st < 3].sum(), "stage1": ecl[st == 1].sum(), "stage2": ecl[st == 2].sum()}
    return out, st, bk


def withdrawn_written_off(target, rows, led):
    """loans Collections closed as cured on a hardship arrangement withdrawn before its start date (the arrangement
    received after the default month starts on the case's resolution date and was cancelled before it started) that the
    agency went on to collect from, which it does only on written-off accounts"""
    ws = openpyxl.load_workbook(os.path.join(target, "hardship_register_2026-09-30.xlsx"), read_only=True).worksheets[0]
    it = ws.iter_rows(values_only=True)
    head = list(next(it))
    col = {h: j for j, h in enumerate(head)}
    day = lambda v: v.date() if hasattr(v, "date") else dt.date.fromisoformat(str(v)[:10])
    cured = {x["loan_no"]: x for x in rows if x["resolution"] == "Cured"}
    hit = set()
    for r in it:
        x = cured.get(r[col["loan_no"]])
        if x is None or r[col["arrangement_status"]] != "Cancelled":
            continue
        y, m = int(x["default_month"][:4]), int(x["default_month"][5:7])
        dme = dt.date(y + (m == 12), m % 12 + 1, 1) - dt.timedelta(days=1)
        start, cancel = day(r[col["arrangement_start"]]), day(r[col["cancelled_date"]])
        if day(r[col["received_date"]]) > dme and start == dt.date.fromisoformat(x["resolution_date"]) and cancel < start:
            hit.add(x["loan_no"])
    agency = {r["loan_no"] for r in led if r["source"] == "Agency remittance"}
    return hit & agency


def lgd(target, how="gold"):
    """realised loss on the 2023-24 defaults by product and quarter of the default month, in per cent"""
    rows = list(csv.DictReader(open(os.path.join(target, "collections_defaults_2023-24.csv"))))
    led = list(csv.DictReader(open(os.path.join(target, "collections_receipts_2023-07_2026-09.csv"))))
    ws = openpyxl.load_workbook(os.path.join(target, "debt_sale_2026-03_schedule.xlsx"), data_only=True).worksheets[0]
    vals = list(ws.iter_rows(values_only=True))
    head = {r[0]: r[1] for r in vals if r[0] and r[0] != "loan_no" and not str(r[0]).startswith("BPL")}
    price = float(str(head["Price"]).split()[0]) / 100.0
    face = {r[0]: float(r[3]) for r in vals if r[0] and str(r[0]).startswith("BPL")}
    mi = lambda s: int(s[:4]) * 12 + int(s[5:7])
    loans = {r["loan_no"]: r for r in rows}
    stale = withdrawn_written_off(target, rows, led)
    got, got_pv = defaultdict(float), defaultdict(float)
    bulk = None
    for r in led:
        if not r["loan_no"]:
            if r["source"] == "Debt sale":
                bulk = r
            continue
        x = loans.get(r["loan_no"])
        if x is None:
            continue
        amt = float(r["amount_aud"])
        got[r["loan_no"]] += amt
        got_pv[r["loan_no"]] += amt * (1 + float(x["contract_rate"]) / 12) ** (-(mi(r["received_date"]) - mi(x["default_month"])))
    cons = float(bulk["amount_aud"])
    wo_bal = sum(float(x["balance_at_default"]) for x in rows if x["resolution"] == "Written off")
    num, den = defaultdict(float), defaultdict(float)
    for x in rows:
        lno, B, r = x["loan_no"], float(x["balance_at_default"]), float(x["contract_rate"])
        disc = (1 + r / 12) ** (-(mi(bulk["received_date"]) - mi(x["default_month"])))
        sale = face.get(lno, 0.0) * price
        label = x["resolution"] == "Cured"
        cured = label and lno not in stale
        if how == "gold":
            loss = 0.0 if cured else B - got_pv[lno] - sale * disc
        elif how == "label":                 # every case closed as cured taken at its word
            loss = 0.0 if label else B - got_pv[lno] - sale * disc
        elif how == "s1":
            if x["resolution"] != "Written off":
                continue
            loss = B - got[lno]
        elif how == "s2":
            loss = 0.0 if label else B - got[lno]
        elif how == "s3":
            loss = 0.0 if label else B - got_pv[lno]
        elif how == "s4":
            spread = cons * B / wo_bal if x["resolution"] == "Written off" else 0.0
            loss = 0.0 if label else B - got_pv[lno] - spread * disc
        elif how == "cures_receipts":
            loss = B - got_pv[lno] - sale * disc
        elif how == "sale_undisc":
            loss = 0.0 if label else B - got_pv[lno] - sale
        else:
            raise ValueError(how)
        q = ((int(x["default_month"][5:7]) - 7) % 12) // 3 + 1
        num[(x["product"], q)] += loss
        den[(x["product"], q)] += B
    return {kq: 100.0 * num[kq] / den[kq] for kq in den}


def migration(target, june="dates", run="2026-07-01", dpd="close"):
    """the June extract was run at 07:30 on 1 July and counts days past due to the run: at close of business on 30 June
    a loan was one day less in arrears ('close'); 'extract' reads the column as it stands"""
    bk, cv, dev, hd, mult, conv = read_inputs(target)
    jb = pd.read_csv(os.path.join(target, "personal_loan_book_2026-06-30.csv"))
    if dpd == "close":
        jb["days_past_due"] = np.maximum(jb["days_past_due"].to_numpy() - 1, 0)
    sc = pd.read_parquet(os.path.join(target, "behaviour_score_runs_2026-03_2026-08.parquet"))
    sc["run_date"] = pd.to_datetime(sc["run_date"]).dt.strftime("%Y-%m-%d")
    pick = sc[sc["run_date"] == run]
    score = jb["loan_no"].map(dict(zip(pick["loan_no"], pick["score_v4"])))
    if june == "dates":
        hd2 = hd
    else:                                   # the register's labels as they stood at the September extract, or every cancellation out
        if june == "label":
            keep = hd["arrangement_status"] == "Active"
        else:
            keep = (hd["arrangement_start"] <= pd.Timestamp(JUNE)) & (hd["arrangement_end"] >= pd.Timestamp(JUNE)) & (hd["arrangement_status"] != "Cancelled")
        hd2 = hd[keep].assign(arrangement_start=pd.Timestamp("2000-01-01"), arrangement_end=pd.Timestamp("2099-12-31"),
                              cancelled_date=pd.NaT)
    jst = stages(jb, hd2, conv, JUNE, score)
    _, sst, _ = allowance(target)
    now = dict(zip(bk["loan_no"], sst))
    out = {}
    for p in ("PL36", "PL60"):
        for s0 in (1, 2):
            ids = jb.loc[((jb["product"] == p) & (jst == s0)).to_numpy(), "loan_no"]
            v = [now.get(x) for x in ids]
            for s1 in (1, 2, 3):
                out[(p, s0, "stage %d" % s1)] = sum(1 for y in v if y == s1)
            out[(p, s0, "closed")] = sum(1 for y in v if y is None)
    return out


def main(target=T, golden=G):
    fails = []

    def chk(name, got, exp, tol=0):
        good = got is not None and abs(float(got) - float(exp)) <= tol
        print(("OK  " if good else "FAIL"), name, got, exp)
        if not good:
            fails.append(name)

    k = lambda x: int(round(x / 1000.0)) * 1000
    fig, st, bk = allowance(target)
    wb = openpyxl.load_workbook(os.path.join(golden, "ecl_allowance_2026Q3.xlsx"), data_only=True)
    ws = wb["Allowance"]
    chk("allowance", ws["B4"].value, k(fig["total"]))
    chk("stage 1 allowance", ws["B5"].value, k(fig["stage1"]))
    chk("stage 2 allowance", ws["B6"].value, k(fig["stage2"]))
    chk("stage 1 loans", ws["B8"].value, int((st == 1).sum()))
    chk("stage 2 loans", ws["B9"].value, int((st == 2).sum()))
    chk("stage 3 loans", ws["B10"].value, int((st == 3).sum()))
    for how in ("uncond", "hazard", "r4b", "r4", "shift"):
        x, _, _ = allowance(target, how)
        d = x["total"] / fig["total"] - 1
        far = abs(d) >= 0.05 and all(k(x[n]) != k(fig[n]) for n in ("total", "stage1", "stage2"))
        print(("OK  " if far else "FAIL"), "rung %-7s %14.0f %+7.2f%%" % (how, x["total"], 100 * d))
        if not far:
            fails.append("rung " + how)
    for how, label in (("sampleS", "divisor's default share from the sample"), ("samplecurve", "curve rebuilt from the sample")):
        x, _, _ = allowance(target, how)
        same = all(k(x[n]) == k(fig[n]) and abs((x[n] / 1000.0) % 1 - 0.5) >= 0.05 for n in ("total", "stage1", "stage2"))
        print(("OK  " if same else "FAIL"), "%s %14.0f, all three figures in their bins" % (label, x["total"]))
        if not same:
            fails.append(label)
    x, _, _ = allowance(target, "clprev")
    off = all(k(x[n]) != k(fig[n]) for n in ("total", "stage1", "stage2"))
    print(("OK  " if off else "FAIL"), "payouts in month a at risk %14.0f %+7.2f%%, all three figures off their bins"
          % (x["total"], 100 * (x["total"] / fig["total"] - 1)))
    if not off:
        fails.append("payout month")
    L = lgd(target)
    quarter = {"Jul to Sep 2023": 1, "Oct to Dec 2023": 2, "Jan to Mar 2024": 3, "Apr to Jun 2024": 4}
    seen = 0
    for r in wb["Realised LGD"].iter_rows(min_row=4, values_only=True):
        if r[0] in ("PL36", "PL60"):
            seen += 1
            chk("realised loss %s %s" % (r[0], r[1]), r[4], round(L[(r[0], quarter[r[1]])], 1))
    chk("realised loss rows", seen, 8)
    for how in ("label", "s1", "s2", "s3", "s4", "cures_receipts", "sale_undisc"):
        x = lgd(target, how)
        apart = all(round(x[q], 1) != round(L[q], 1) for q in L)
        print(("OK  " if apart else "FAIL"), "ask A stop %-15s" % how, " ".join("%.1f" % x[q] for q in sorted(x)))
        if not apart:
            fails.append("ask A stop " + how)
    M = migration(target)
    seen = 0
    for r in wb["Stage migration"].iter_rows(min_row=4, max_row=7, values_only=True):
        for j, w in enumerate(("stage 1", "stage 2", "stage 3", "closed")):
            seen += 1
            chk("migration %s stage %s -> %s" % (r[0], r[1][-1], w), r[2 + j], M[(r[0], int(r[1][-1]), w)])
    chk("migration cells", seen, 16)
    for name, kw in (("days past due as extracted", dict(dpd="extract")),
                     ("labels, May run", dict(june="label", run="2026-06-01", dpd="extract")),
                     ("cancelled out, May run", dict(june="excl", run="2026-06-01", dpd="extract")),
                     ("dates, May run", dict(run="2026-06-01", dpd="extract")), ("cancelled out, June run", dict(june="excl"))):
        x = migration(target, **kw)
        moved = sum(x[c] != M[c] for c in M)
        print(("OK  " if moved >= 12 else "FAIL"), "ask B stop %-24s moves %d of 16" % (name, moved))
        if moved < 12:
            fails.append("ask B stop " + name)
    print("VERIFY", "FAIL" if fails else "PASS", len(fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:3]) if len(sys.argv) > 2 else main())
