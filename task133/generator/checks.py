"""Assertions on task133's shipped pack: input gates; the allowance, every rung of the main ladder and the readings each
convention admits; the development sample and the curve read off it; the realism of the extracts (repayment calendar,
balances, hardship register, default definition, loss flows, pricing, scores); the June extract and the month-end
scoring runs; the Collections files and the March 2026 sale; both ask ladders; the separation of the ask devices from the
main call's rows; and the ask-layer audits (lazy sweep, necessity matrix, pair simulation, over-cleaner, oracle sweep,
hygiene battery)."""
import datetime as dt
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
import zipfile
from collections import Counter

import numpy as np
import pandas as pd
import pyarrow.parquet as pq

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import estimators as E
import officex as OX
import verify as V
import world as W

TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
G = os.path.join(TASK, "golden")
R = W.REPORT
JUNE = W.PRIOR_QE
n_ok = 0
LOG = []


def ok(cond, msg):
    global n_ok
    if not cond:
        raise AssertionError(msg)
    n_ok += 1


def say(*a):
    line = " ".join(str(x) for x in a)
    LOG.append(line)
    print(line)


def edge(v, unit):
    return abs((v / unit) % 1 - 0.5)


K = lambda x: int(round(x / 1000.0))
HOL = set()
for _y in range(2019, 2033):
    HOL |= W.nsw_holidays(_y)


def is_bd(d):
    return d.weekday() < 5 and d not in HOL


def due_dates(first, n):
    out = []
    for j in range(n):
        y, m = first.year + (first.month - 1 + j) // 12, (first.month - 1 + j) % 12 + 1
        d = dt.date(y, m, first.day)
        while not is_bd(d):
            d += dt.timedelta(days=1)
        out.append(d)
    return out


def docx_text(path):
    with zipfile.ZipFile(path) as z:
        return " ".join(re.sub(r"<[^>]+>", "", p) for p in re.findall(r"<w:p [^>]*>.*?</w:p>", z.read("word/document.xml").decode(), re.S))


POLICY = os.path.join(T, "CRM-ECL-04_expected_credit_loss_personal_loans.docx")
ASK_A_FILES = ["defaults", "receipts", "sale"]
ASK_B_FILES = ["june", "scores"]


# ---------------------------------------------------------------------------------------------------------- gates

def gates():
    files = sorted(os.listdir(T))
    ok(len(files) >= 10, "10 or more input files (%d)" % len(files))
    ok(len({f.rsplit(".", 1)[1] for f in files}) >= 3, "3 or more formats")
    bk = pd.read_csv(os.path.join(T, E.F["book"]), dtype=str)
    ok(len(bk) >= 25000, "the September loan book has 25,000 or more rows (%d)" % len(bk))
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    ok(len(meta["distractors"]) >= 2 and all(d in files for d in meta["distractors"]), "two or more distractors on disk")
    ok(set(meta["distractors"]) == {"write_offs_2025-07_2026-09.csv", "arrears_roll_rates_fy26.xlsx"},
       "the distractors are the roll-rate workbook and the aggregate write-off file")
    ok(sorted(x["path"] for x in meta["input_files"]) == files, "metadata lists every shipped file")
    ok(meta["deliverables"] == ["ecl_allowance_2026Q3.xlsx", "board_ecl_q3_2026.pptx"]
       and all(os.path.exists(os.path.join(G, d)) for d in meta["deliverables"]), "two deliverables, both built")
    for f in files:
        ok(not any(w in f.lower() for w in ("answer", "golden", "trap", "clean", "_v2", "test_", "distract")),
           "file name %s carries no author noun" % f)
    return len(files), len({f.rsplit(".", 1)[1] for f in files})


# ---------------------------------------------------------------------------------------------------------- the main call

def by_label(bk, hd, mapping):
    """staging at 30 September with the register's status label standing in for 2.2's dates"""
    st = E.stage(bk, hd, mapping)
    act = set(hd.loc[hd["arrangement_status"] == "Active", "loan_no"])
    st[bk["loan_no"].isin(act) & (st == 1)] = 2
    return st


def main_call():
    s = E.solve(T)
    A = s["total"]
    ok(abs(s["mult"] - 1.06) < 1e-12, "weighted PD multiplier 1.06")
    figs = {"allowance": A, "stage 1": s["stage1"], "stage 2": s["stage2"]}
    for name, v in figs.items():
        ok(edge(v, 1000) >= 0.05, "%s clears its rounding edge by 5 per cent of the bin (%.3f)" % (name, edge(v, 1000)))
    ok(K(s["stage1"]) + K(s["stage2"]) == K(A), "the stage amounts add to the allowance at the nearest thousand")
    # the ladder: every rung lands at least 5 per cent from the answer and misses all three figures at the nearest thousand
    rungs = {}
    for v in ("uncond", "hazard", "r4b", "r4", "shift"):
        x = E.solve(T, variant=v)
        rungs[v] = x
        d = x["total"] / A - 1
        ok(abs(d) >= 0.05, "rung %s sits at least 5 per cent from the answer (%+.2f%%)" % (v, 100 * d))
        ok(all(K(x[n]) != K(s[n]) for n in ("total", "stage1", "stage2")),
           "rung %s misses the allowance and both stage amounts at the nearest thousand" % v)
    ok(rungs["uncond"]["total"] > rungs["hazard"]["total"] > A > rungs["r4b"]["total"] > rungs["r4"]["total"] > rungs["shift"]["total"],
       "the rungs order: from origination, hazard with no repayment, the answer, repayment counted twice, survival to "
       "date, no division")
    for nm, kw, floor in (("no discounting", dict(disc=False), 0.06), ("balance held flat", dict(flat_ead=True), 0.10)):
        d = E.solve(T, **kw)["total"] / A - 1
        ok(d >= floor, "%s is at least %d per cent high (%+.2f%%)" % (nm, 100 * floor, 100 * d))
    # the readings the closure table keeps land every figure in the answer's bin
    kept = {"past-maturity loans carry nothing": dict(pm_zero=True), "the curve recomputed from the sample": dict(D_from="sample"),
            "only early repayment taken off": dict(early_only=True), "the status label stages hardship": dict(stage_fn=by_label)}
    kept_out = {}
    for nm, kw in kept.items():
        x = E.solve(T, **kw)
        kept_out[nm] = x["total"]
        for n, label in (("total", "allowance"), ("stage1", "stage 1"), ("stage2", "stage 2")):
            ok(K(x[n]) == K(s[n]) and edge(x[n], 1000) >= 0.05, "%s: %s keeps its bin with 5 per cent to spare (%.0f)" % (nm, label, x[n]))
    # exits counted to the start of the month instead of its end: the curve header's month-end definition rules it out
    sh = E.sample_shares
    starts = {}
    for nm, f in (("payouts in month a still at risk", lambda d: np.concatenate([[0.0], d["Cl"][:-1]])),):
        def patched(t, f=f):
            out = sh(t)
            for p in out:
                out[p] = dict(out[p], Cl=f(out[p]))
            return out
        E.sample_shares = patched
        try:
            x = E.solve(T)
        finally:
            E.sample_shares = sh
        starts[nm] = x["total"] / A - 1
        ok(K(x["total"]) != K(A), "%s lands off the answer's bin (%+.2f%%)" % (nm, 100 * starts[nm]))
    nh = E.solve(T, use_hardship=False)
    nm = E.solve(T, map_v3=False)
    ok(abs(nh["n2"] - s["n2"]) >= 300, "the hardship register moves at least 300 loans into stage 2 (%d)" % abs(nh["n2"] - s["n2"]))
    ok(abs(nm["n2"] - s["n2"]) >= 100, "the v3 conversion moves at least 100 loans across the stage line (%d)" % abs(nm["n2"] - s["n2"]))
    ok(s["n3"] > 0 and s["n_pm"] >= 10 and s["ecl_pm"] > 0, "stage 3 loans sit outside the model; past-maturity loans carry an "
       "allowance (%d loans, %.0f)" % (s["n_pm"], s["ecl_pm"]))
    vfig, _, _ = V.allowance(T)
    ok(all(abs(vfig[n] - s[n]) < 0.01 for n in ("total", "stage1", "stage2")), "the independent verifier agrees to the cent")
    for v in rungs:
        vx, _, _ = V.allowance(T, v)
        ok(abs(vx["total"] - rungs[v]["total"]) < 0.01, "the verifier reproduces rung %s to the cent" % v)
    return s, rungs, kept_out, starts


# ---------------------------------------------------------------------------------------------------------- the curve

def curve_and_sample():
    cv = pd.read_csv(os.path.join(T, E.F["curve"]), comment="#")
    C = {p: g.sort_values("month_on_book")["cumulative_pd"].to_numpy() for p, g in cv.groupby("product")}
    sh = E.sample_shares(T)
    for p in ("PL36", "PL60"):
        ok(np.abs(C[p] - sh[p]["D"]).max() <= 5e-7, "%s: the curve is the sample's crude default share to six decimals" % p)
        ok(np.allclose(sh[p]["Cl"][:-1], sh[p]["Cl_early"][:-1]), "%s: nothing matures before its term, so repaid early or "
           "at term is the same share at every month the book uses" % p)
        S = 1 - sh[p]["D"] - sh[p]["Cl"]
        ok((S[:-1] > 0).all() and abs(S[-1]) < 1e-12, "%s: every development loan has defaulted or been repaid by the end of its term" % p)
    dev = pd.read_parquet(os.path.join(T, E.F["dev"]))
    ok(set(dev["outcome"]) == {"default", "prepaid", "matured"}, "no development loan is still open")
    ok((dev.loc[dev["outcome"] == "matured", "outcome_month_on_book"] == dev.loc[dev["outcome"] == "matured", "term_months"]).all()
       and (dev.loc[dev["outcome"] == "prepaid", "outcome_month_on_book"] < dev.loc[dev["outcome"] == "prepaid", "term_months"]).all(),
       "matured loans close at their term, prepaid ones before it")
    for p, lo, hi in (("PL36", "2019-10", "2023-03"), ("PL60", "2019-10", "2021-03")):
        m = sorted(dev.loc[dev["product"] == p, "drawdown_month"].unique())
        span = pd.period_range(lo, hi, freq="M").astype(str).tolist()
        ok(m == span, "%s development window runs %s to %s with every month present" % (p, lo, hi))
    n = dev.groupby("product").size()
    ok(n["PL36"] > 15000 and n["PL60"] > 5000, "development samples of %d PL36 and %d PL60 loans" % (n["PL36"], n["PL60"]))
    head = open(os.path.join(T, E.F["curve"])).read().split("product,")[0].lower()
    for w in ("divid", "condition", "surviv", "attrition", "early repay", "prepa", "payout", "still open", "performing"):
        ok(w not in head, "the curve header says nothing about %r" % w)
    ok("share of the loans drawn in the development window that had defaulted by the end of that month on book" in head,
       "the header defines the column in plain words")
    pol = docx_text(POLICY)
    ok("sample" not in pol.lower(), "CRM-ECL-04 carries no sentence about the development sample")
    ok("not modelled" not in pol and "EAD(k) follows the repayment schedule; extra repayments and hardship variations after "
       "the reporting date do not change it." in pol, "7.4 says what is true of EAD and nothing about payouts")
    return dict(n=n.to_dict(), D_T={p: float(C[p][-1]) for p in C})


# ---------------------------------------------------------------------------------------------------------- realism

def realism():
    bk = pd.read_csv(os.path.join(T, E.F["book"]))
    first = bk["first_repayment_date"].map(E._d)
    draw = bk["drawdown_date"].map(E._d)
    dpd = bk["days_past_due"].values
    nomatch = gt = before = 0
    for f, d, t in zip(first, dpd, bk["term_months"]):
        if d == 0:
            continue
        sched = due_dates(f, int(t) + 6)
        nomatch += (R - dt.timedelta(days=int(d))) not in sched
        before += sched[0] >= R
        gt += d > (R - sched[0]).days
    ok(nomatch == 0 and gt == 0 and before == 0, "days past due match a due date (%d), never exceed days since the first (%d), none before it (%d)" % (nomatch, gt, before))
    ok(dpd.max() <= 179, "no loan on the book at 180 or more days past due (%d)" % dpd.max())
    a = np.array([E.months_due(f) for f in first])
    i = bk["contract_rate"].values / 12
    n = bk["term_months"].values.astype(float)
    amt = bk["original_amount"].values.astype(float)
    pay = amt * i / (1 - (1 + i) ** -n)
    k = np.minimum(a, n)
    sched = amt * (1 + i) ** k - pay * ((1 + i) ** k - 1) / i
    on = (np.abs(bk["current_balance"].values - np.round(sched, 2)) < 0.005) & (a >= 1)
    ok(on.mean() < 0.01, "balances on the textbook schedule to the cent are under 1 per cent of repaying loans (%.4f)" % on.mean())
    arr = (dpd >= 30) & (a < n)
    ok((bk["current_balance"].values[arr] > sched[arr]).mean() > 0.8, "loans 30 or more days past due sit above schedule")
    hd = pd.read_excel(os.path.join(T, E.F["hardship"]), sheet_name=0)
    st, en = hd["arrangement_start"].dt.date, hd["arrangement_end"].dt.date
    ok(all(is_bd(d) for d in st), "arrangements start on business days")
    life = dict(zip(bk["loan_no"], zip(draw, [due_dates(f, int(t))[-1] for f, t in zip(first, bk["term_months"])])))
    inside = [(life[l][0] < s0 and e0 <= life[l][1]) for l, s0, e0 in zip(hd["loan_no"], st, en) if l in life]
    ok(all(inside), "arrangements on book loans fall inside the loan's life")
    ok(((hd["cancelled_date"].notna()) == (hd["arrangement_status"] == "Cancelled")).all(), "cancelled_date is filled exactly for cancelled arrangements")
    ok(((en - st).map(lambda x: x.days) >= 1).all(), "every arrangement ends after the day it starts")
    cx = hd[hd["arrangement_status"] == "Cancelled"]
    ok((cx["cancelled_date"] <= cx["arrangement_end"]).all(), "arrangements are cancelled inside their term")
    ok((hd["received_date"].diff().dropna().dt.days >= 0).all() and hd["case_ref"].is_monotonic_increasing, "case numbers run in order of receipt")
    ok(hd.loc[hd["arrangement_status"] == "Active", "arrangement_type"].nunique() == 2, "active arrangements are of both types")
    ok((hd["loan_no"].value_counts() > 1).sum() > 100, "some loans have repeat arrangements")
    ok(hd["received_date"].min().date() < dt.date(2020, 3, 1), "the register runs from soon after go-live")
    dur = [(e0 - s0).days + 1 for s0, e0 in zip(st, en)]
    ok(np.mean([d in (60, 90, 180) for d in dur]) < 0.15, "durations run in calendar months, not fixed day counts")
    act = hd[(hd["arrangement_status"] != "Cancelled") & (st <= R) & (en >= R)]
    ok((en != R).all() and (hd["cancelled_date"].dropna().dt.date < R).all(), "no arrangement ends, or is cancelled, on the reporting date")
    ok((hd["cancelled_date"].dropna().dt.date != JUNE).all(), "no arrangement is cancelled on 30 June either")
    ok(len(set(act["loan_no"]) & set(bk["loan_no"])) == len(set(act["loan_no"])), "every arrangement in force belongs to a book loan")
    cv = pd.read_csv(os.path.join(T, E.F["curve"]), comment="#")
    C = {p: g.sort_values("month_on_book")["cumulative_pd"].values for p, g in cv.groupby("product")}
    ok(len(C["PL36"]) == 37 and len(C["PL60"]) == 61, "each curve runs to its product's term")
    for p in C:
        ok(C[p][1] == 0 and C[p][2] == 0 and C[p][3] < 0.002, "%s: no 90 day default before month 3, a trace at 3" % p)
        ok((np.diff(C[p]) >= 0).all(), "%s: the cumulative share never falls" % p)
    ok(0.07 <= C["PL60"][-1] <= 0.13 and 0.06 <= C["PL36"][-1] < C["PL60"][-1],
       "a profitable lender's lifetime default share: %.4f PL36, %.4f PL60" % (C["PL36"][-1], C["PL60"][-1]))
    ok(C["PL60"][24] / C["PL60"][-1] > 0.55, "the curve is front-loaded after month 4")
    dev = pd.read_parquet(os.path.join(T, E.F["dev"]))
    d = dev[dev["outcome"] == "default"]
    ok((d["outcome_month_on_book"] <= 2).sum() == 0 and (d["outcome_month_on_book"] == 3).sum() < 0.02 * len(d), "development defaults start at month 3 or later")
    share = dev.assign(x=dev["outcome"] == "default").groupby("risk_grade")["x"].mean()
    ok(share["A"] < 0.06 and share["E"] < 0.30 and share.is_monotonic_increasing, "default share rises A to E at a sustainable level")
    pre = (dev["outcome"] == "prepaid").groupby(dev["product"]).mean()
    ok(0.30 <= pre["PL36"] <= 0.60 and 0.35 <= pre["PL60"] <= 0.65, "about four to five loans in ten are repaid early (%s)" % pre.round(3).to_dict())
    wo = pd.read_csv(os.path.join(T, "write_offs_2025-07_2026-09.csv"))
    bands = [((dpd >= x) & (dpd < x + 30)).sum() for x in (90, 120, 150)]
    ok(0.6 <= wo["loans_written_off"].mean() / np.mean(bands) <= 1.4, "monthly write-offs agree with the stage 3 bands (%.1f vs %.1f)" % (wo["loans_written_off"].mean(), np.mean(bands)))
    ok(all(is_bd(x) for x in draw), "loans are funded on NSW business days")
    ok((draw.map(lambda x: x.day) >= 29).sum() > 100, "funding on the 29th to 31st")
    gap = np.array([(f - x).days for f, x in zip(first, draw)])
    ok(gap.min() >= 14 and gap.max() <= 44, "first repayment 2 to 6 weeks after funding")
    same = np.mean([f == dt.date(x.year + (x.month == 12), x.month % 12 + 1, min(x.day, 28)) for f, x in zip(first, draw)])
    ok(0.2 < same < 0.6, "about four in ten first repayments one month after funding")
    dv = dev["drawdown_month"].value_counts()
    bm = draw.map(lambda x: x.strftime("%Y-%m")).value_counts()
    ok(dv["2020-04"] < 0.7 * dv["2020-02"] and bm["2025-12"] < bm["2025-11"], "volumes carry the 2020 shock and December seasonality")
    f3, f4 = dict(W.BANDS_V3), dict(W.BANDS_V4)
    band = [next((g for g in W.GRADES if sc >= (f4 if card == "v4" else f3)[g]), "E")
            for sc, card in zip(bk["origination_score"], bk["origination_scorecard"])]
    ok(np.mean(np.array(band) == bk["risk_grade"].values) > 0.97, "grades follow the score bands")
    for col in ("origination_score", "current_score_v4"):
        vc = bk[col].value_counts()
        ok(vc.get(bk[col].max(), 0) < 5, "%s has no pile-up at its maximum" % col)
    med = bk.groupby(["risk_grade", "product"])["contract_rate"].median().unstack()
    ok((med["PL60"] > med["PL36"]).sum() >= 4, "PL60 priced above PL36 in most grades")
    yr = draw.map(lambda x: x.year)
    c = bk[(bk["risk_grade"] == "C") & (bk["product"] == "PL60")].assign(y=yr)
    ok(c[c.y == 2024]["contract_rate"].median() - c[c.y == 2022]["contract_rate"].median() > 0.015, "rates follow the cash rate cycle")
    vc = bk["original_amount"].value_counts()
    ok(vc.index[0] < 50000 and bk["original_amount"].max() > 50000, "the cap is not the most common amount")
    ch = bk["channel"].value_counts(normalize=True)
    ok(ch.max() - ch.min() > 0.2 and abs(bk["product"].eq("PL36").mean() - 0.5) > 0.01, "channel and product mixes are not even splits")
    vs = bk["state"].value_counts()
    shp = 100 * vs / len(bk)
    ok(vs.is_unique and (np.abs(shp - np.round(shp)) >= 0.15).sum() >= 6, "state counts all differ and sit off whole percentages")
    o4 = np.where(bk["origination_scorecard"] == "v3", np.floor(1.12 * bk["origination_score"] - 18 + 0.5), bk["origination_score"])
    fresh = a == 0
    cur = bk["current_score_v4"].values
    ok(fresh.sum() > 500 and (cur[fresh] == o4[fresh]).all(), "behaviour score is the v4 origination score until the first repayment falls due (%d loans)" % fresh.sum())
    ok((cur[~fresh] != o4[~fresh]).mean() > 0.9, "behaviour scores move once repayments fall due")
    num = bk["loan_no"].str[3:9].astype(int)
    v3 = (bk["origination_scorecard"] == "v3").values
    sw = dt.date(2024, 7, 1)
    ok(num[v3].max() < num[~v3].min(), "every v3 loan number precedes every v4 loan number")
    ok((draw[v3] >= sw).sum() >= 50 and (draw[~v3] >= sw).all(), "loans applied for before 1 July 2024 and funded after it stay on v3")
    luhn = lambda q: (10 - sum((lambda x: x - 9 if x > 9 else x)(int(c) * (2 if i % 2 == 0 else 1)) for i, c in enumerate(q[::-1])) % 10) % 10
    ok(all(int(x[-1]) == luhn(x[3:9]) for x in bk["loan_no"]), "loan numbers carry a Luhn check digit")
    pz = act.loc[act["arrangement_type"] == "Payment pause", "loan_no"]
    dp = bk.set_index("loan_no").loc[pz, "days_past_due"]
    ok(len(pz) > 50 and (dp == 0).all(), "no arrears on a loan under a payment pause in force on the reporting date (%d pauses)" % len(pz))
    red = hd.loc[hd["arrangement_type"] == "Reduced repayments", "agreed_repayment_aud"]
    ok((red % 5 == 0).mean() < 0.75 and (red % 1 != 0).mean() > 0.1 and (red <= 50).mean() > 0.03, "agreed repayments are a realistic mix")
    rec = wo["recoveries_aud"].sum() / wo["gross_write_off_aud"].sum()
    ok(0.15 <= rec <= 0.35, "recoveries run at %.3f of gross write-offs over the 15 months, the March 2026 sale included" % rec)
    ok(wo["loans_written_off"].mean() < 0.95 * ((dpd >= 90) & (dpd < 120)).sum(), "fewer loans are written off each month than reach 90 days past due")
    head = open(os.path.join(T, E.F["curve"])).read().split("product,")[0]
    meta = {k.decode(): v.decode() for k, v in pq.read_schema(os.path.join(T, E.F["dev"])).metadata.items() if not k.startswith(b"pandas")}
    ok("performance to 31 May 2026" in head and "24 June 2026" in head and meta["performance_to"] == "2026-05-31"
       and meta["performance_to"] < meta["extracted"] <= "2026-06-24" and "30 June 2026" not in head + str(meta),
       "development performance ends 31 May 2026, before extraction and the 24 June approval")
    ex = dt.date.fromisoformat(meta["extracted"])
    room = sum(is_bd(ex + dt.timedelta(days=i)) for i in range(1, (dt.date(2026, 6, 24) - ex).days))
    ok(is_bd(ex) and ex <= dt.date(2026, 6, 5) and room >= 14, "the sample is extracted early in June, leaving %d business days" % room)
    ok("pd_model_development_sample" not in head, "the curve header names the development sample, not the shipped file")
    ok("go-live to the last complete-term vintages" in head and "last complete-term vintages" in meta["population"],
       "the header and the sample say the window runs from go-live to the last complete-term vintages")


# ---------------------------------------------------------------------------------------------------------- the June extract

def june_extract():
    bk = pd.read_csv(os.path.join(T, E.F["book"]))
    jb = pd.read_csv(os.path.join(T, E.F["june"]))
    ok(list(jb.columns) == [c for c in bk.columns if c != "current_score_v4"], "the June extract has the September columns but the score")
    ok(jb["loan_no"].is_unique and jb["loan_no"].is_monotonic_increasing, "the June extract is one row per loan, by loan number")
    both = jb.merge(bk, on="loan_no", suffixes=("_j", "_s"))
    for c in ("product", "risk_grade", "drawdown_date", "first_repayment_date", "term_months", "contract_rate", "original_amount",
              "origination_score", "origination_scorecard", "channel"):
        ok((both[c + "_j"] == both[c + "_s"]).all(), "%s agrees across the two extracts" % c)
    ok(((both["state_j"] == both["state_s"]) | (both["state_j"].isna() & both["state_s"].isna())).all(), "state agrees across the two extracts")
    new = bk[~bk["loan_no"].isin(set(jb["loan_no"]))]
    ok((pd.to_datetime(new["drawdown_date"]) > pd.Timestamp(JUNE)).all(), "every September loan missing from June was drawn after 30 June (%d)" % len(new))
    up = both[(both["days_past_due_j"] == 0) & (both["days_past_due_s"] == 0)]
    ok((up["current_balance_s"] < up["current_balance_j"]).mean() > 0.95, "up-to-date loans pay their balances down over the quarter")
    ok(jb["days_past_due"].max() <= 179, "no June loan at 180 or more days past due")
    r_j, r_s = (jb["days_past_due"] >= 30).mean(), (bk["days_past_due"] >= 30).mean()
    ok(0.75 <= r_j / r_s <= 1.33, "arrears of 30 days or more run at a like share in June and September (%.4f, %.4f)" % (r_j, r_s))
    closed = jb[~jb["loan_no"].isin(set(bk["loan_no"]))]
    return len(jb), len(closed), len(new)


# ---------------------------------------------------------------------------------------------------------- the scoring runs

def scoring_runs():
    sc = E.score_runs(T)
    ok(list(sc.columns) == ["loan_no", "run_date", "score_v4"], "the scoring file carries loan, run date and score")
    runs = sorted(sc["run_date"].unique())
    ok(runs == [dt.date(2026, m, 1) for m in range(4, 10)], "six runs, made on the first day of April to September 2026")
    ok(not sc.duplicated(["loan_no", "run_date"]).any(), "one score per loan per run")
    meta = {k.decode(): v.decode() for k, v in pq.read_schema(os.path.join(T, E.F["scores"])).metadata.items() if not k.startswith(b"pandas")}
    ok("first day of the following month" in meta["run_date"] and "position at close of business on the month end" in meta["run_date"],
       "the file's own description states the run timing")
    jb = pd.read_csv(os.path.join(T, E.F["june"]))
    jun = sc[sc["run_date"] == dt.date(2026, 7, 1)]
    due = set(jb.loc[pd.to_datetime(jb["first_repayment_date"]) <= pd.Timestamp(JUNE), "loan_no"])
    ok(set(jun["loan_no"]) == due, "the June month-end run scores exactly the June loans whose first repayment has fallen due (%d)" % len(due))
    bk = pd.read_csv(os.path.join(T, E.F["book"]))
    orig = pd.concat([jb, bk]).drop_duplicates("loan_no").set_index("loan_no")
    o4 = np.where(orig["origination_scorecard"] == "v3", np.floor(1.12 * orig["origination_score"] - 18 + 0.5), orig["origination_score"])
    o4 = pd.Series(o4, index=orig.index)
    shares = {}
    for d in runs:
        x = sc[sc["run_date"] == d]
        x = x[x["loan_no"].isin(o4.index)]
        shares[d.isoformat()] = float(((o4.loc[x["loan_no"]].to_numpy() - x["score_v4"].to_numpy()) >= 60).mean())
    vals = list(shares.values())
    ok(0.05 <= min(vals) and max(vals) <= 0.09 and max(vals) - min(vals) <= 0.015,
       "the share 60 points or more below origination holds steady across the runs (%s)" % {k: round(v, 4) for k, v in shares.items()})
    jl = sc[sc["run_date"] == dt.date(2026, 8, 1)].set_index("loan_no")["score_v4"]
    jn = jun.set_index("loan_no")["score_v4"]
    chg = (jl - jn).dropna().abs()
    ok(3 <= chg.median() <= 15, "a typical score moves %.0f points from one month-end run to the next" % chg.median())
    aug = sc[sc["run_date"] == dt.date(2026, 9, 1)].set_index("loan_no")["score_v4"]
    sep = bk.set_index("loan_no")["current_score_v4"]
    common = aug.index.intersection(sep.index)
    ok((aug.loc[common] != sep.loc[common]).mean() > 0.7, "the September run in the extract is not a copy of the August run")
    return shares


# ---------------------------------------------------------------------------------------------------------- Collections files

def collections_files():
    fy, led, sale, price, head = E.collections(T)
    ok(fy["loan_no"].is_unique, "one row per 2023-24 default")
    ok(fy["default_month"].between("2023-07", "2024-06").all(), "every default month falls in July 2023 to June 2024")
    ok(set(fy["resolution"]) == {"Cured", "Settled", "Written off"}, "defaults are cured, settled or written off")
    dme = pd.to_datetime(fy["default_month"] + "-01") + pd.offsets.MonthEnd(0)
    ok((pd.to_datetime(fy["resolution_date"]) > dme).all(), "every resolution falls after the default month end")
    wo = fy[fy["resolution"] == "Written off"]
    gap = (pd.to_datetime(wo["resolution_date"]).dt.to_period("M") - pd.to_datetime(wo["default_month"]).dt.to_period("M")).map(lambda x: x.n)
    ok((pd.to_datetime(wo["resolution_date"]) == pd.to_datetime(wo["resolution_date"]) + pd.offsets.MonthEnd(0)).all()
       and gap.between(2, 4).all(), "write-offs fall in a month-end batch two to four months after the default month")
    q = [((int(m[5:7]) - 7) % 12) // 3 + 1 for m in fy["default_month"]]
    cells = Counter(zip(fy["product"], q))
    ok(min(cells.values()) >= 100, "every product and quarter holds 100 or more defaults (%s)" % dict(cells))
    share_res = (fy["resolution"] != "Written off").mean()
    ok(0.10 <= share_res <= 0.25, "about one default in six is resolved before write-off (%.3f)" % share_res)
    ok(led["receipt_ref"].is_unique and (led["receipt_ref"].str[2:].astype(int).diff().dropna() > 0).all()
       and pd.to_datetime(led["received_date"]).is_monotonic_increasing, "receipt numbers run in date order")
    ok(led["received_date"].between("2023-07-01", "2026-09-30").all(), "the receipts file runs July 2023 to September 2026")
    blank = led[led["loan_no"].isna()]
    ok(len(blank) == 1 and blank["source"].iloc[0] == "Debt sale", "the one receipt with no loan is the sale's")
    amt = led["amount_aud"].astype(float)
    neg = led[amt < 0]
    ok(len(neg) >= 5 and (neg["source"] == "Direct debit").all() and neg["narrative"].str.startswith("Dishonour of RC").all(),
       "dishonoured direct debits are reversed by negative entries that name the receipt (%d)" % len(neg))
    by_ref = led.set_index("receipt_ref")
    for _, r in neg.iterrows():
        o = by_ref.loc[r["narrative"].split()[-1]]
        ok(o["loan_no"] == r["loan_no"] and abs(float(o["amount_aud"]) + float(r["amount_aud"])) < 0.005
           and o["received_date"][:7] == r["received_date"][:7] and o["received_date"] < r["received_date"],
           "reversal %s nets its receipt inside the month" % r["receipt_ref"])
    st = led[led["source"] == "Settlement"]
    ok((st["amount_aud"].astype(float) % 50 == 0).all(), "settlements are agreed in round fifty dollars")
    x = led.merge(fy[["loan_no", "default_month", "resolution", "resolution_date"]], on="loan_no", how="inner")
    me = pd.to_datetime(x["default_month"] + "-01") + pd.offsets.MonthEnd(0)
    ok((pd.to_datetime(x["received_date"]) > me).all(), "every receipt on a 2023-24 default falls after its default month end")
    ag = x[x["source"] == "Agency remittance"]
    ok((ag["resolution"] == "Written off").all() and (ag["received_date"] > ag["resolution_date"]).all(),
       "agency remittances come only after write-off")
    cut, settled = W.SALE_CUTOFF, W.SALE_SETTLED
    ok(cut.month == settled.month and cut.year == settled.year, "the sale's cut-off and settlement fall in one month")
    ok(abs(round(float(sale["face_value_aud"].astype(float).sum()) * price, 2) - float(blank["amount_aud"].iloc[0])) < 0.01
       and abs(float(head["Consideration (AUD)"]) - float(blank["amount_aud"].iloc[0])) < 0.005
       and blank["received_date"].iloc[0] == settled.isoformat(),
       "the sale receipt is face value times price, as the schedule's header states, on the settlement date")
    ok(sale["loan_no"].is_unique and (sale["face_value_aud"].astype(float) > 0).all()
       and (sale["written_off"] <= W.SALE_WRITTEN_OFF_BY.strftime("%Y-%m")).all(), "sold accounts were written off by August 2025")
    after = led[led["loan_no"].isin(set(sale["loan_no"])) & (led["received_date"] > cut.isoformat())]
    ok(len(after) == 0, "nothing is received on a sold account after the cut-off")
    quiet = led[led["loan_no"].isin(set(sale["loan_no"])) & (led["received_date"] > (cut - dt.timedelta(days=W.SALE_QUIET_DAYS)).isoformat())
                & (led["received_date"] <= cut.isoformat())]
    ok(len(quiet) == 0, "sold accounts had nothing received in the six months to the cut-off")
    fs = fy[fy["loan_no"].isin(set(sale["loan_no"]))]
    fq = Counter(zip(fs["product"], [((int(m[5:7]) - 7) % 12) // 3 + 1 for m in fs["default_month"]]))
    ok(len(fq) == 8 and min(fq.values()) >= 20 and (fs["resolution"] == "Written off").all(),
       "the sale holds written-off 2023-24 defaults from every quarter and both products (%s)" % dict(fq))
    wof = pd.read_csv(os.path.join(T, "write_offs_2025-07_2026-09.csv"))
    mar = float(wof.loc[wof["month"] == "2026-03", "recoveries_aud"].iloc[0])
    other = wof.loc[wof["month"] != "2026-03", "recoveries_aud"].astype(float)
    ok(mar - float(blank["amount_aud"].iloc[0]) > 0 and other.between(150000, 600000).all(),
       "the March 2026 recoveries carry the sale on top of an ordinary month")
    return dict(defaults=len(fy), receipts=len(led), sold=len(sale), price=price, consideration=float(blank["amount_aud"].iloc[0]),
                fy_sold=len(fs), reversals=len(neg))


# ---------------------------------------------------------------------------------------------------------- ask A

ASK_A_STOPS = ["s1", "s2", "s3", "s4", "cures_receipts", "excl_cures", "sale_undisc", "all_undisc", "lazy"]
# discounting by days, or from the start of the month, misreads 3.3's month-end rule; reported, not designed stops
ASK_A_MISREADINGS = ["days", "month_start"]


def ask_a():
    g = E.realised_lgd(T)
    ok(len(g) == 8, "eight figures, two products by four quarters")
    ok(all(40 <= v <= 95 for v in g.values()), "realised losses sit where unsecured personal lending loses")
    for key, v in g.items():
        ok(edge(v, 0.1) >= 0.05, "realised loss %s Q%d clears its rounding edge by 5 per cent of the bin (%.3f)" % (key[0], key[1], edge(v, 0.1)))
    vg = V.lgd(T)
    ok(all(abs(vg[k] - g[k]) < 1e-9 for k in g), "the independent verifier agrees on all eight")
    stops = {}
    for v in ASK_A_STOPS:
        x = E.realised_lgd(T, v)
        stops[v] = x
        ok(all(round(x[k], 1) != round(g[k], 1) for k in g),
           "ask A stop %s misses every figure at one decimal (nearest %.2f points)" % (v, min(abs(x[k] - g[k]) for k in g)))
    for v in ASK_A_MISREADINGS:
        x = E.realised_lgd(T, v)
        stops[v] = x
        hit = sum(round(x[k], 1) == round(g[k], 1) for k in g)
        ok(hit <= 4, "3.3 misread as %s still misses %d of the 8 figures" % (v, 8 - hit))
    for v in ("s1", "s2", "s3", "s4", "cures_receipts", "sale_undisc"):
        vx = V.lgd(T, v)
        ok(all(abs(vx[k] - stops[v][k]) < 1e-9 for k in g), "the verifier reproduces ask A stop %s" % v)
    for v in ("floor", "face_alloc"):
        x = E.realised_lgd(T, v)
        ok(all(round(x[k], 1) == round(g[k], 1) and abs(x[k] - g[k]) < 0.01 for k in g),
           "%s gives the same eight figures (converged)" % v)
    return g, stops


# ---------------------------------------------------------------------------------------------------------- ask B

ASK_B_STOPS = [("1 labels, May run", dict(june_rule="label", run="may")),
               ("2 dates without any cancelled, May run", dict(june_rule="excl_cancel", run="may")),
               ("3 dates, May run", dict(run="may")),
               ("4 dates without any cancelled, June run", dict(june_rule="excl_cancel")),
               ("5 cancellation ignored, June run", dict(june_rule="ignore_cancel")),
               ("6 September scores for June", dict(run="sept")),
               ("labels, June run", dict(june_rule="label")),
               ("labels with start dates, May run", dict(june_rule="label_dated", run="may")),
               ("July run", dict(run="july")),
               ("end date excluded", dict(june_rule="end_exclusive"))]


def ask_b():
    m = E.migration(T)
    ok(len(m) == 16 and all(v > 0 for v in m.values()), "sixteen counts, none empty")
    vm = V.migration(T)
    ok(vm == m, "the independent verifier agrees on all sixteen")
    hd = pd.read_excel(os.path.join(T, E.F["hardship"]), sheet_name=0)
    j = pd.Timestamp(JUNE)
    s_, e_, c_ = hd["arrangement_start"], hd["arrangement_end"], hd["cancelled_date"]
    inf = (s_ <= j) & (e_ >= j) & (c_.isna() | (c_ > j))
    facts = dict(in_force=int(inf.sum()), still_active=int((inf & (hd["arrangement_status"] == "Active")).sum()),
                 cancelled_after=int((inf & c_.notna()).sum()), end_on_30_june=int((inf & (e_ == j)).sum()),
                 cancelled_on_30_june=int((c_ == j).sum()))
    ok(facts["in_force"] >= 500 and facts["still_active"] <= 0.3 * facts["in_force"] and facts["cancelled_after"] >= 30
       and facts["end_on_30_june"] >= 1 and facts["cancelled_on_30_june"] == 0,
       "the register at 30 June: %s" % facts)
    rr = pd.Timestamp(R)
    old_rule = set(hd.loc[(hd["arrangement_status"] != "Cancelled") & (s_ <= rr) & (e_ >= rr), "loan_no"])
    ok(E.in_force(hd, R, "dates") == old_rule, "the rewritten 2.2 changes nothing at 30 September")
    stops = {}
    for name, kw in ASK_B_STOPS:
        x = E.migration(T, **kw)
        stops[name] = x
        moved = sum(x[k] != m[k] for k in m)
        ok(moved >= 1, "ask B stop %s lands off the answer (%d of 16 move)" % (name, moved))
    devices = {"B1, the label after the switch": stops["labels, June run"], "B1, every cancelled out": stops["4 dates without any cancelled, June run"],
               "B2, the May run": stops["3 dates, May run"]}
    for name, x in devices.items():
        ok(sum(x[k] != m[k] for k in m) >= 12, "device %s moves at least 12 of the 16 counts" % name)
    for name in ("1 labels, May run", "2 dates without any cancelled, May run", "3 dates, May run", "6 September scores for June"):
        ok(sum(stops[name][k] != m[k] for k in m) >= 12, "stop %s moves at least 12 of the 16 counts" % name)
    names = [n for n, _ in ASK_B_STOPS]
    for a_ in range(len(names)):
        for b_ in range(a_ + 1, len(names)):
            ok(stops[names[a_]] != stops[names[b_]], "stops %r and %r land on different counts" % (names[a_], names[b_]))
    same = E.migration(T, june_rule="cancel_inclusive")
    ok(same == m, "reading a cancellation on 30 June either way gives the same counts (none falls on it)")
    hz = E.migration(T, sept_rule="label")
    hz_moved = sum(hz[k] != m[k] for k in m)
    ok(hz_moved <= 2, "staging September on the status label moves %d counts (the status lag, a hazard)" % hz_moved)
    for nm, kw in (("labels, May run", dict(june="label", run="2026-06-01")), ("every cancelled out, June run", dict(june="excl"))):
        vx = V.migration(T, **kw)
        ref = stops["1 labels, May run"] if nm.startswith("labels") else stops["4 dates without any cancelled, June run"]
        ok(vx == ref, "the verifier reproduces ask B stop %s" % nm)
    return m, stops, facts, hz_moved


# ---------------------------------------------------------------------------------------------------------- separation

def separation(s):
    """the main call's rows: the September book's loans in stages 1 and 2, the arrangements in force at 30 September, the
    curve and the development sample. No ask device and no hazard row sits inside them"""
    hd = pd.read_excel(os.path.join(T, E.F["hardship"]), sheet_name=0)
    j, r = pd.Timestamp(JUNE), pd.Timestamp(R)
    s_, e_, c_ = hd["arrangement_start"], hd["arrangement_end"], hd["cancelled_date"]
    june_only = (s_ <= j) & (e_ >= j) & (c_.isna() | (c_ > j)) & ~((s_ <= r) & (e_ >= r) & (c_.isna() | (c_ > r)))
    rows = hd[june_only]
    in_sept = rows[(rows["arrangement_start"] <= r) & (rows["arrangement_end"] >= r) & (rows["cancelled_date"].isna() | (rows["cancelled_date"] > r))]
    lab = rows[rows["arrangement_status"] == "Active"]
    canc = rows[rows["cancelled_date"].notna()]
    ok(len(in_sept) == 0 and len(lab) <= 2, "the arrangements in force at 30 June and not at 30 September (%d, %d of them "
       "cancelled after June) are in force at 30 September under 2.2 for none and labelled Active for %d (the status lag)"
       % (len(rows), len(canc), len(lab)))
    ok(len(canc[canc["arrangement_status"] == "Active"]) == 0, "none of the post-June cancellations carries an Active label")
    counts = dict(june_device_rows=len(rows), in_force_at_30_sept=len(in_sept), cancelled_after_june=len(canc))
    tmp = tempfile.mkdtemp()
    try:
        cut = os.path.join(tmp, "main")
        shutil.copytree(T, cut)
        for kf in ASK_A_FILES + ASK_B_FILES:
            os.remove(os.path.join(cut, E.F[kf]))
        x = E.solve(cut)
        ok(all(x[n] == s[n] for n in ("total", "stage1", "stage2")),
           "the main call never reads the June extract, the scoring runs, the Collections files or the sale schedule")
        cut2 = os.path.join(tmp, "asks")
        shutil.copytree(T, cut2)
        for kf in ("curve", "dev"):
            os.remove(os.path.join(cut2, E.F[kf]))
        ok(E.realised_lgd(cut2) == E.realised_lgd(T) and E.migration(cut2) == E.migration(T),
           "neither ask reads the curve or the development sample, so landing or missing the call moves no ask answer")
        cut3 = os.path.join(tmp, "distractors")
        shutil.copytree(T, cut3)
        for f in ("write_offs_2025-07_2026-09.csv", "arrears_roll_rates_fy26.xlsx"):
            os.remove(os.path.join(cut3, f))
        x3 = E.solve(cut3)
        ok(x3["total"] == s["total"] and E.realised_lgd(cut3) == E.realised_lgd(T) and E.migration(cut3) == E.migration(T),
           "the two distractors are read by no graded figure")
    finally:
        shutil.rmtree(tmp)
    return counts


# ---------------------------------------------------------------------------------------------------------- readings and pins

def readings(s):
    """the golden's stage 2 set; the register's status lag; what the pause pin is worth"""
    L = s["loans"]
    ids = sorted(L.loc[L["stage"] == 2, "loan_no"])
    digest = hashlib.sha256("\n".join(ids).encode()).hexdigest()
    ok(len(ids) == 3266 and digest == STAGE2_HASH, "the stage 2 set is the one CRM-ECL-04 section 2 gives (%d loans, %s)" % (len(ids), digest[:12]))
    bk, curves, hd, scen, mapping = E.load(T)
    end = hd["arrangement_end"].map(E._d)
    stale = (hd["arrangement_status"] == "Active") & (end < R)
    ok(1 <= stale.sum() <= 5, "a few arrangements that ended after the last weekly status run still show Active (%d)" % stale.sum())
    last_run = R - dt.timedelta(days=(R.weekday() - W.STATUS_RUN_WEEKDAY) % 7)
    ok((end[stale] >= last_run).all(), "each ended on or after the last Tuesday run, %s" % last_run)
    start = hd["arrangement_start"].map(E._d)
    canc = hd["arrangement_status"] == "Cancelled"
    want = [("Cancelled" if c else "Approved" if a > R else "Active" if b >= last_run else "Completed")
            for a, b, c in zip(start, end, canc)]
    ok((hd["arrangement_status"] == want).all(), "every other status agrees with the dates and the weekly run as at 30 September")
    pz = hd[(hd["arrangement_type"] == "Payment pause") & ~canc].assign(s=start, e=end)
    book = bk.set_index("loan_no")
    held = {}
    for loan, g in pz.groupby("loan_no"):
        if loan in book.index:
            f = book.at[loan, "first_rep"]
            n = sum(1 for d in due_dates(f, E.months_due(f)) if any(a <= d <= min(b, R) for a, b in zip(g["s"], g["e"])))
            if n:
                held[loan] = n
    md, le, cur = E.months_due, E.loan_ecl, {"n": 0}
    E.months_due = lambda f, report=E.REPORT: md(f, report) - cur["n"]

    def held_out(row, *a, **k):
        cur["n"] = held.get(row["loan_no"], 0)
        try:
            return le(row, *a, **k)
        finally:
            cur["n"] = 0
    E.loan_ecl = held_out
    try:
        alt = E.solve(T)
    finally:
        E.months_due, E.loan_ecl = md, le
    moved = [n for n in ("total", "stage1", "stage2") if K(alt[n]) != K(s[n])]
    ok(len(held) > 1000 and len(moved) >= 1, "leaving pause dates out of months on book (%d loans, %d dates) moves %s, the "
       "allowance to %.0f: the 3.2 pin is load-bearing" % (len(held), sum(held.values()), moved, alt["total"]))
    return (len(held), sum(held.values()), len(moved), alt["total"]), int(stale.sum())


STAGE2_HASH = "a8137550bc1822e3a354a8e4c71bfd98045823aa673609028826904547fc6d93"


def residue_and_pins():
    bk = pd.read_csv(os.path.join(T, E.F["book"]))
    nulls = bk.isna().sum()
    ok(set(nulls[nulls > 0].index) == {"state"} and 20 <= nulls["state"] <= 100,
       "the book's only blanks are the state of borrowers with an overseas address (%d)" % nulls["state"])
    jb = pd.read_csv(os.path.join(T, E.F["june"]))
    jn = jb.isna().sum()
    ok(set(jn[jn > 0].index) == {"state"}, "the June extract's only blanks are overseas addresses too")
    hd = pd.read_excel(os.path.join(T, E.F["hardship"]), sheet_name=0)
    nr = hd[hd["hardship_reason"].isna()]
    ok(3 <= len(nr) <= 12 and (nr["received_date"].dt.date < W.REASON_REQUIRED).all(),
       "a few cases from before the reason became a required field carry none (%d)" % len(nr))
    lk = hd[(hd["hardship_reason"] == "COVID-19") & (hd["received_date"].dt.year == 2021)]
    ok(len(lk) > 50 and not lk["loan_no"].isin(set(bk["loan_no"])).any() and (lk["arrangement_end"] < "2022-03-01").all(),
       "the 2021 lockdown pauses (%d) sit on loans closed before the reporting date" % len(lk))
    pol = docx_text(POLICY)
    head = open(os.path.join(T, E.F["curve"])).read().split("product,")[0]
    meta = {k.decode(): v.decode() for k, v in pq.read_schema(os.path.join(T, E.F["dev"])).metadata.items()}
    dic = " ".join(open(os.path.join(T, "ecl_extract_dictionary.txt")).read().split())
    ok("Repayment dates during a payment pause count as repayments fallen due" in pol
       and "treated as being in the final month of its term, with a remaining term of one month" in pol
       and "repayment dates during a payment pause count" in head
       and "repayment dates during a payment pause included" in meta["outcome_month_on_book"]
       and "which stay in the loan's schedule" in dic and "the maturity date does not change" in dic
       and "Completed is set by the weekly hardship batch on Tuesday nights" in dic,
       "payment pauses and past-maturity loans are pinned in the policy, the curve header, the sample metadata and the dictionary")
    ok("more than 30 days past due" in pol and "30 or more days past due" in pol, "2.5 quotes AASB 9 5.5.11 as more than 30 days")
    ok("in force from its start date to its end date, both included, and stops being in force on the day it is cancelled" in pol,
       "2.2 is written for any reporting date")
    ok("behaviour score from the month-end scoring run on the position at the reporting date" in pol, "2.1 names the scoring run")
    ok("The default is recorded at the first month end at which the loan is 90 or more days past due" in pol, "1.2 dates a default")
    ok("including proceeds from a sale of the debt" in pol and "counts at the end of the month in which it is received" in pol
       and "for each whole month between the two" in pol and "treated as recovering its balance at default in full" in pol,
       "3.3 files the realised loss measure")
    ok("change CHG-26-0418 added to the extract on 21 July 2026" in dic, "the dictionary says when the score joined the extract")
    for f in sorted(os.listdir(T)):
        if not f.endswith((".docx", ".xlsx")):
            continue
        with zipfile.ZipFile(os.path.join(T, f)) as z:
            app = "word" if f.endswith(".docx") else "excel"
            th = z.read("%s/theme/theme1.xml" % ("word" if app == "word" else "xl")).decode("utf-8")
            core = z.read("docProps/core.xml").decode()
            ok(th == OX.theme_xml(app), "%s carries the Office 2013-2022 theme as %s writes it" % (f, app.title()))
            made = re.search(r"<dcterms:created[^>]*>(\d{4}-\d\d-\d\d)", core).group(1)
            who = re.search(r"<dc:creator>([^<]*)", core).group(1)
            if app == "excel":
                ok('defaultThemeVersion="166925"' in z.read("xl/workbook.xml").decode(), "%s: workbook theme version 166925" % f)
                ok(made < "2023-07-01" or who == W.JOB_ACCOUNT, "%s: created %s, before the 2023 theme, or by the job" % (f, made))
            if f == E.F["hardship"]:
                ok(who == W.JOB_ACCOUNT and "<cp:lastModifiedBy>Kayla Stokes<" in core, "the register is written by the job's account")
    with zipfile.ZipFile(POLICY) as z:
        app = z.read("docProps/app.xml").decode()
        doc = z.read("word/document.xml").decode()
    st = {k: int(v) for k, v in re.findall(r"<(Lines|Paragraphs|Words|Characters|CharactersWithSpaces)>(\d+)<", app)}
    ok(st["Lines"] >= 1.25 * st["Paragraphs"] and st["CharactersWithSpaces"] > st["Characters"] > 4 * st["Words"],
       "the policy's statistics are the word processor's measurement (%s)" % st)
    rs = Counter(re.findall(r'<w:p [^>]*w:rsidR="([0-9A-F]{8})"', doc))
    ok(len(rs) >= 8 and rs.most_common(1)[0][1] >= 0.25 * sum(rs.values()) and doc.count('<w:r w:rsidR="') >= 10,
       "the policy's revision ids follow its history (%d sessions)" % len(rs))
    ok("Version 4.2" in pol and "Reporting dates from 30 September 2026" in pol and "25 August 2026" in pol,
       "the policy is version 4.2, approved in August 2026")


# ---------------------------------------------------------------------------------------------------------- ask-layer audits

def audits(s, rungs, g_a, m_b):
    out = {}
    # lazy sweep: the most natural competent path, no device handled and no organ read
    lazy_a = E.realised_lgd(T, "lazy")
    lazy_b = E.migration(T, june_rule="label", run="may")
    ok(all(round(lazy_a[k], 1) != round(g_a[k], 1) for k in g_a), "the lazy path misses every ask A figure")
    ok(sum(lazy_b[k] != m_b[k] for k in m_b) >= 12, "the lazy path misses at least 12 ask B counts")
    out["lazy"] = (8, sum(lazy_b[k] != m_b[k] for k in m_b))
    # necessity matrix: each device mishandled alone, everything else right
    mat = {}
    for name, x in (("A: the sale left out", E.realised_lgd(T, "s3")), ("A: receipts not discounted", E.realised_lgd(T, "all_undisc")),
                    ("A: cures from their receipts", E.realised_lgd(T, "cures_receipts")),
                    ("A: the sale receipt spread over every write-off", E.realised_lgd(T, "s4"))):
        mat[name] = sum(round(x[k], 1) != round(g_a[k], 1) for k in g_a)
        ok(mat[name] == 8, "%s moves all eight ask A figures" % name)
    for name, kw in (("B1: the label after the switch", dict(june_rule="label")), ("B1: every cancelled out", dict(june_rule="excl_cancel")),
                     ("B2: the run made before the date", dict(run="may"))):
        x = E.migration(T, **kw)
        mat[name] = sum(x[k] != m_b[k] for k in m_b)
        ok(mat[name] >= 12, "%s moves %d of the 16 ask B counts" % (name, mat[name]))
    out["matrix"] = mat
    # the pair simulation: the strongest solver's habitual path on the asks (the hygiene battery, the filed rules it
    # points at), once with the main call landed (cracker) and once at the portal's survival-to-date reading (mirror)
    REC, IF, ASK = 38.0, 7.0, 55.0
    habit_a = E.realised_lgd(T, "s3")             # per-loan sums: the receipt with no loan drops out of a group-by
    habit_b = E.migration(T, june_rule="excl_cancel", run="may")   # the September staging code at 30 June: status filter,
    #                                                                  the last run made on or before the date
    hits = sum(round(habit_a[k], 1) == round(g_a[k], 1) for k in g_a) + sum(habit_b[k] == m_b[k] for k in m_b)
    L_ = hits / 24.0
    mirror_main = rungs["r4"]
    r_keep = 5.0                                  # the stage counts and the scenario multiplier survive a wrong curve reading
    ok(all(K(mirror_main[n]) != K(s[n]) for n in ("total", "stage1", "stage2")), "the mirror sheet misses the call")
    cracker = REC + IF + ASK * L_
    mirror = r_keep + IF + ASK * L_
    pair = (cracker + mirror) / 2
    ok(pair <= 40.0, "pair simulation: cracker %.1f, mirror %.1f, pair %.1f on the habitual path" % (cracker, mirror, pair))
    careful = ((REC + IF + ASK) + (r_keep + IF + ASK)) / 2
    out["pair"] = dict(cracker=cracker, mirror=mirror, pair=pair, ask_hits=hits, careful_pair=careful)
    # over-cleaner: blanket hygiene rules land on their designed over-corrected stops, not the answer
    oc = {"A: the sale receipt spread over every write-off": E.realised_lgd(T, "s4"),
          "A: the negative rows dropped as errors": E.realised_lgd(T, "no_reversals")}
    oc_b = {"B: cancellation ignored": E.migration(T, june_rule="ignore_cancel"), "B: September scores for June": E.migration(T, run="sept")}
    ok(all(round(oc["A: the sale receipt spread over every write-off"][k], 1) != round(g_a[k], 1) for k in g_a),
       "spreading the sale receipt over every write-off misses every ask A figure")
    nr = oc["A: the negative rows dropped as errors"]
    out["no_reversals_moved"] = sum(round(nr[k], 1) != round(g_a[k], 1) for k in g_a)
    ok(out["no_reversals_moved"] == 0, "the dishonour reversals are texture: dropping them as errors moves no ask A figure")
    for name, x in oc_b.items():
        ok(sum(x[k] != m_b[k] for k in m_b) >= 1, "%s lands off the answer" % name)
    # oracle sweep: nothing in the pack states a graded figure or tabulates the asks
    texts = docx_text(POLICY) + open(os.path.join(T, "ecl_extract_dictionary.txt")).read()
    for f in sorted(os.listdir(T)):
        if f.endswith(".xlsx"):
            import openpyxl
            wb = openpyxl.load_workbook(os.path.join(T, f), read_only=True)
            for ws in wb.worksheets:
                if f == E.F["hardship"] or f == E.F["sale"]:
                    texts += " ".join(str(c) for r in ws.iter_rows(max_row=12, values_only=True) for c in r if c is not None)
                else:
                    texts += " ".join(str(c) for r in ws.iter_rows(values_only=True) for c in r if c is not None)
    for v in ["%.1f" % x for x in g_a.values()] + ["13,160,000", "13160000", "10,563,000", "2,597,000"]:
        ok(re.search(r"(?<![\d.])%s(?![\d])" % re.escape(v), texts) is None, "no document states %s" % v)
    cols = set()
    for f in os.listdir(T):
        if f.endswith(".csv"):
            cols |= set(pd.read_csv(os.path.join(T, f), comment="#", nrows=1).columns)
        if f.endswith(".parquet"):
            cols |= set(pq.read_schema(os.path.join(T, f)).names)
    ok(not any("stage" in c.lower() or "lgd" in c.lower() or "loss" in c.lower() for c in cols),
       "no shipped column carries a stage, a loss rate or an LGD")
    # the hygiene battery on the wrong paths comes back clean
    led = pd.read_csv(os.path.join(T, E.F["receipts"]), dtype=str)
    ok(led["receipt_ref"].is_unique and not led.duplicated().any(), "receipts: unique references, no exact duplicate rows")
    ok(int(led["loan_no"].isna().sum()) == 1, "receipts: one blank loan number")
    for kf in ("book", "june", "defaults"):
        x = pd.read_csv(os.path.join(T, E.F[kf]), dtype=str)
        ok(x["loan_no"].is_unique and not x.duplicated().any(), "%s: one row per loan, no duplicates" % E.F[kf])
    fy, _, sale, _, _ = E.collections(T)
    ok(sale["loan_no"].is_unique, "the sale schedule lists each account once")
    sc = E.score_runs(T)
    ok(not sc.duplicated(["loan_no", "run_date"]).any(), "the scoring runs carry one row per loan and run")
    jb = pd.read_csv(os.path.join(T, E.F["june"]), dtype=str)
    ok(set(sc.loc[sc["run_date"] == dt.date(2026, 7, 1), "loan_no"]) <= set(jb["loan_no"]), "every June-run loan joins the June extract")
    return out


# ---------------------------------------------------------------------------------------------------------- the deliverables

QLAB = {1: ("Jul to Sep 2023", "July to September 2023"), 2: ("Oct to Dec 2023", "October to December 2023"),
        3: ("Jan to Mar 2024", "January to March 2024"), 4: ("Apr to Jun 2024", "April to June 2024")}


def deliverables(s, g_a, m_b):
    """every graded figure agrees, at its stated rounding, in the workbook, the deck and submission.md, computed here
    from target/ rather than read off golden.py; and the task tree holds one live write-up and one prompt"""
    import openpyxl
    from pptx import Presentation
    wb = openpyxl.load_workbook(os.path.join(G, "ecl_allowance_2026Q3.xlsx"))
    al = wb["Allowance"]
    ok([al["B4"].value, al["B5"].value, al["B6"].value] == [1000 * K(s["total"]), 1000 * K(s["stage1"]), 1000 * K(s["stage2"])],
       "workbook: the allowance and both stage amounts at the nearest thousand")
    ok([al["B8"].value, al["B9"].value, al["B10"].value, al["B11"].value] == [s["n1"], s["n2"], s["n3"], round(s["mult"], 2)],
       "workbook: loans by stage and the multiplier")
    lg = wb["Realised LGD"]
    got = {}
    for r in range(4, 12):
        p, ql, e = lg.cell(r, 1).value, lg.cell(r, 2).value, lg.cell(r, 5).value
        q = [k for k, v in QLAB.items() if v[0] == ql][0]
        got[(p, q)] = e
        ok(lg.cell(r, 6).value == (70 if p == "PL36" else 76), "workbook: the LGD in use beside %s %s" % (p, ql))
    ok(got == {k: round(v, 1) for k, v in g_a.items()}, "workbook: the eight realised losses at one decimal")
    mg = wb["Stage migration"]
    cells = {}
    for r in range(4, 8):
        p, s0 = mg.cell(r, 1).value, int(mg.cell(r, 2).value.split()[-1])
        for j, x in enumerate(("stage 1", "stage 2", "stage 3", "closed")):
            cells[(p, s0, x)] = mg.cell(r, 3 + j).value
    ok(cells == m_b, "workbook: the sixteen migration counts")
    prs = Presentation(os.path.join(G, "board_ecl_q3_2026.pptx"))
    s1, s2 = prs.slides[0], prs.slides[1]
    t1 = " ".join(sh.text_frame.text for sh in s1.shapes if sh.has_text_frame)
    tb = [sh.table for sh in s1.shapes if sh.has_table][0]
    tv = [[tb.cell(i, j).text for j in range(3)] for i in range(4)]
    money = lambda x: "${:,}".format(1000 * K(x))
    ok(money(s["total"]) in t1 and tv[1][2] == money(s["stage1"]) and tv[2][2] == money(s["stage2"])
       and tv[3][2] == money(s["total"]), "deck slide 1: the allowance and both stage amounts")
    ch = [sh.chart for sh in s2.shapes if sh.has_chart][0]
    cats = list(ch.plots[0].categories)
    order = [("PL36", 1), ("PL36", 2), ("PL60", 1), ("PL60", 2)]
    ok(cats == ["%s, stage %d at 30 June" % o for o in order], "deck slide 2: the four groups in order")
    ser = {sr.name: list(sr.values) for sr in ch.plots[0].series}
    names = {"stage 1": "Stage 1 at 30 September", "stage 2": "Stage 2", "stage 3": "Stage 3", "closed": "Closed"}
    ok(all(int(ser[names[x]][i]) == m_b[(p, s0, x)] for i, (p, s0) in enumerate(order) for x in names),
       "deck slide 2: the chart carries the sixteen counts")
    inv = {v: k for k, v in names.items()}
    ok(all(sr.points[i].data_label.has_text_frame
           and sr.points[i].data_label.text_frame.text == "{:,}".format(m_b[order[i] + (inv[sr.name],)])
           for sr in ch.plots[0].series for i in range(4)), "deck slide 2: every segment is labelled with its count")
    sub = open(os.path.join(TASK, "submission.md")).read()
    ok("AUD {:,}".format(1000 * K(s["total"])) in sub.split("## 2.")[0], "submission: the call states the allowance")
    for v in (s["total"], s["stage1"], s["stage2"]):
        ok(sub.count("AUD {:,}".format(1000 * K(v))) >= 2, "submission: AUD {:,} in the components and the answers".format(1000 * K(v)))
    ok("**{:,}**".format(s["n2"]) in sub and "**%.2f**" % s["mult"] in sub, "submission: the stage 2 count and the multiplier")
    for (p, q), v in g_a.items():
        ok("%s, %s: %.1f" % (p, QLAB[q][1], v) in sub, "submission: realised loss %s %s" % (p, QLAB[q][1]))
    for p, s0 in order:
        line = "%s, stage %d at 30 June: %s in stage 1, %s in stage 2, %s in stage 3, %s closed" % (
            (p, s0) + tuple("{:,}".format(m_b[(p, s0, x)]) for x in ("stage 1", "stage 2", "stage 3", "closed")))
        ok(line in sub, "submission: %s" % line)
    pr = open(os.path.join(TASK, "prompt.md")).read().strip()
    ok(len(pr) < 1000, "the prompt is under 1,000 characters (%d)" % len(pr))
    ok(all(d in pr for d in ("ecl_allowance_2026Q3.xlsx", "board_ecl_q3_2026.pptx")), "the prompt names both deliverables")
    for f in ("prompt.md", "submission.md", "DESIGN_NOTE.md"):
        ok("\u2014" not in open(os.path.join(TASK, f)).read(), "no em dash in %s" % f)
    found = Counter(f for _, _, fs in os.walk(TASK) for f in fs if f in ("submission.md", "prompt.md"))
    ok(found == Counter({"submission.md": 1, "prompt.md": 1}), "one live write-up and one prompt in the task tree")
    return len(pr)


# ---------------------------------------------------------------------------------------------------------- main

def main():
    nf, nfmt = gates()
    s, rungs, kept, starts = main_call()
    cs = curve_and_sample()
    realism()
    jn = june_extract()
    shares = scoring_runs()
    cf = collections_files()
    g_a, stops_a = ask_a()
    m_b, stops_b, facts, hz = ask_b()
    sep = separation(s)
    pause, stale = readings(s)
    residue_and_pins()
    au = audits(s, rungs, g_a, m_b)
    plen = deliverables(s, g_a, m_b)
    say("CHECKS PASS", n_ok)
    say("files %d, formats %d; allowance %.0f, stage 1 %.0f, stage 2 %.0f" % (nf, nfmt, s["total"], s["stage1"], s["stage2"]))
    for v, x in rungs.items():
        say("  rung %-7s %14.0f %+7.2f%%" % (v, x["total"], 100 * (x["total"] / s["total"] - 1)))
    say("  kept readings: %s" % {k: round(v) for k, v in kept.items()})
    say("  exits to the start of the month: %s" % {k: "%+.2f%%" % (100 * v) for k, v in starts.items()})
    say("development sample %s, lifetime default share %s" % (cs["n"], {k: round(v, 4) for k, v in cs["D_T"].items()}))
    say("June extract %d loans, %d closed by 30 September, %d drawn since; score-fall shares by run %s" % (jn + ({k: round(v, 4) for k, v in shares.items()},)))
    say("Collections: %s" % cf)
    keys = sorted(g_a)
    say("ask A  gold          " + " ".join("%6.2f" % g_a[k] for k in keys))
    for v in ASK_A_STOPS + ASK_A_MISREADINGS:
        say("ask A  %-14s " % v + " ".join("%6.2f" % stops_a[v][k] for k in keys)
            + "   same at one decimal: %d" % sum(round(stops_a[v][k], 1) == round(g_a[k], 1) for k in keys))
    say("ask B  gold          " + " ".join("%6d" % m_b[k] for k in m_b))
    for name, _ in ASK_B_STOPS:
        x = stops_b[name]
        say("ask B  %-40s moves %2d/16" % (name, sum(x[k] != m_b[k] for k in m_b)))
    say("register at 30 June %s; September label staging moves %d counts" % (facts, hz))
    say("separation %s" % sep)
    say("pause dates out of months on book: %d loans, %d dates, %d main figures move, allowance %.0f; stale labels %d" % (pause + (stale,)))
    say("audits %s" % au)
    say("deliverables agree with target/; prompt %d characters" % plen)


if __name__ == "__main__":
    main()
