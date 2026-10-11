"""Assertions on task133's shipped pack: input gates, the answer, the ladder, rounding margins, the realism of the
extracts (repayment calendar, balances, hardship register, default definition, loss flows, pricing, scores), the two
conventions CRM-ECL-04 3.2 pins (payment pauses, loans past maturity) with what the other reading of each is worth, the
register's status lag, the extracts' residue and the Office containers."""
import datetime as dt
import json
import os
import sys

import numpy as np
import openpyxl
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import estimators as E
import officex as OX
import world as W

TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
R = W.REPORT
n_ok = 0


def ok(cond, msg):
    global n_ok
    if not cond:
        raise AssertionError(msg)
    n_ok += 1


def edge(v, unit):
    return abs((v / unit) % 1 - 0.5)


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


def gates():
    files = sorted(os.listdir(T))
    ok(len(files) >= 10, "10 or more input files (%d)" % len(files))
    ok(len({f.rsplit(".", 1)[1] for f in files}) >= 3, "3 or more formats")
    bk = pd.read_csv(os.path.join(T, E.F["book"]), dtype=str)
    ok(len(bk) >= 25000, "loan book has 25,000 or more rows (%d)" % len(bk))
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    ok(len(meta["distractors"]) >= 2 and all(d in files for d in meta["distractors"]), "two or more distractors on disk")
    for f in files:
        ok(not any(w in f.lower() for w in ("answer", "golden", "trap", "clean", "_v2", "test_")), "file name %s carries no author noun" % f)


def graded(s):
    """every graded figure at its reporting precision"""
    k = lambda x: int(round(x / 1000.0))
    g = {"total": k(s["total"]), "stage1": k(s["stage1"]), "stage2": k(s["stage2"]), "n3": s["n3"]}
    L = s["loans"]
    for st in (1, 2):
        for p in ("PL36", "PL60"):
            g["n_%s_%d" % (p, st)] = int(((L["stage"] == st) & (L["product"] == p)).sum())
            g["gca_%s_%d" % (p, st)] = k(s["%s_s%d_gca" % (p, st)])
            g["ecl_%s_%d" % (p, st)] = k(s["%s_s%d" % (p, st)])
            g["cov_%s_%d" % (p, st)] = round(s["%s_s%d_cov" % (p, st)], 2)
    for key, v in s["by_band"].items():
        g["year %s %s" % key] = k(v)
    return g


def answer_and_ladder():
    s = E.solve(T)
    A = s["total"]
    ok(abs(s["mult"] - 1.06) < 1e-12, "weighted PD multiplier 1.06")
    # every graded figure clears its rounding edge by at least five per cent of the bin
    vals = [("total", A, 1000), ("stage1", s["stage1"], 1000), ("stage2", s["stage2"], 1000)]
    for st in (1, 2):
        for p in ("PL36", "PL60"):
            vals += [("%s_s%d" % (p, st), s["%s_s%d" % (p, st)], 1000), ("%s_s%d_gca" % (p, st), s["%s_s%d_gca" % (p, st)], 1000),
                     ("%s_s%d_cov" % (p, st), s["%s_s%d_cov" % (p, st)], 0.01)]
    for key, v in s["by_band"].items():
        vals.append(("year %s %s" % key, v, 1000))
    for name, v, u in vals:
        ok(edge(v, u) >= 0.05, "%s clears its rounding edge (%.4f)" % (name, edge(v, u)))
    rung = {}
    for nm, kw in [("uncond", dict(variant="uncond")), ("shift", dict(variant="shift")), ("nodisc", dict(disc=False)),
                   ("flat_ead", dict(flat_ead=True))]:
        rung[nm] = E.solve(T, **kw)["total"] / A - 1
    ok(rung["uncond"] >= 0.20, "the curve read from origination for every loan is at least 20 per cent high (%.3f)" % rung["uncond"])
    # the shift rung is minus the ECL-weighted cumulative default at each loan's months on book, about 0.25 to 0.3 of the
    # lifetime rate; with lifetime default in the low teens it cannot reach the old 6 per cent floor (that needed about
    # 20 per cent lifetime default), so the floor keeps it clearly below the answer
    ok(rung["shift"] <= -0.025, "the curve shifted to months on book without the survival division is at least 2.5 per cent low (%.3f)" % rung["shift"])
    ok(rung["nodisc"] >= 0.06, "skipping the discount is at least 6 per cent high (%.3f)" % rung["nodisc"])
    ok(rung["flat_ead"] >= 0.10, "holding the balance flat is at least 10 per cent high (%.3f)" % rung["flat_ead"])
    ok(abs(rung["shift"] + rung["nodisc"]) >= 0.03, "the shift-plus-no-discount cell stays away from the answer (%.3f)" % (rung["shift"] + rung["nodisc"]))
    nh = E.solve(T, use_hardship=False)
    nm = E.solve(T, map_v3=False)
    ok(abs(nh["n2"] - s["n2"]) >= 300, "the hardship register moves at least 300 loans into stage 2 (%d)" % abs(nh["n2"] - s["n2"]))
    ok(abs(nm["n2"] - s["n2"]) >= 100, "the v3 conversion moves at least 100 loans across the stage line (%d)" % abs(nm["n2"] - s["n2"]))
    ok(s["n3"] > 0, "stage 3 loans are in the extract and outside the model")
    # loans past contractual maturity outside stage 3 carry one remaining month (CRM-ECL-04 3.2); read as carrying
    # nothing instead, every graded figure keeps its bin
    z = E.solve(T, pm_zero=True)
    ok(s["n_pm"] >= 10 and s["ecl_pm"] > 0, "loans past maturity outside stage 3 carry an allowance (%d loans, %.0f)" % (s["n_pm"], s["ecl_pm"]))
    gs, gz = graded(s), graded(z)
    ok(gs == gz, "every graded figure keeps its bin whether past-maturity loans carry one month or nothing (%s)"
       % [k for k in gs if gs[k] != gz[k]])
    return s, rung


def realism():
    bk = pd.read_csv(os.path.join(T, E.F["book"]))
    first = bk["first_repayment_date"].map(E._d)
    draw = bk["drawdown_date"].map(E._d)
    dpd = bk["days_past_due"].values
    # 1 days past due follow each loan's repayment calendar
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
    # 2 balances come from payment histories, not the textbook schedule
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
    # 3 the hardship register
    hd = pd.read_excel(os.path.join(T, E.F["hardship"]), sheet_name=0)
    st, en = hd["arrangement_start"].dt.date, hd["arrangement_end"].dt.date
    ok(all(is_bd(d) for d in st), "arrangements start on business days")
    life = dict(zip(bk["loan_no"], zip(draw, [due_dates(f, int(t))[-1] for f, t in zip(first, bk["term_months"])])))
    inside = [(life[l][0] < s0 and e0 <= life[l][1]) for l, s0, e0 in zip(hd["loan_no"], st, en) if l in life]
    ok(all(inside), "arrangements on book loans fall inside the loan's life")
    ok(((hd["cancelled_date"].notna()) == (hd["arrangement_status"] == "Cancelled")).all(), "cancelled_date is filled exactly for cancelled arrangements")
    ok(((en - st).map(lambda x: x.days) >= 1).all(), "every arrangement ends after the day it starts (shortest %d days)" % ((en - st).map(lambda x: x.days).min() + 1))
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
    ok(len(set(act["loan_no"]) & set(bk["loan_no"])) == len(set(act["loan_no"])), "every arrangement in force belongs to a book loan")
    # 4 the curve keeps the 90 days past due definition and a profitable lender's level
    cv = pd.read_csv(os.path.join(T, E.F["curve"]), comment="#")
    C = {p: g.sort_values("month_on_book")["cumulative_pd"].values for p, g in cv.groupby("product")}
    ok(len(C["PL36"]) == 37 and len(C["PL60"]) == 61, "each curve runs to its product's term")
    for p in C:
        ok(C[p][1] == 0 and C[p][2] == 0 and C[p][3] < 0.002, "%s: no 90 day default before month 3, a trace at 3" % p)
    ok(0.08 <= C["PL60"][-1] <= 0.145 and C["PL36"][-1] < C["PL60"][-1], "lifetime default in the low teens for PL60, lower for PL36")
    ok(C["PL60"][24] / C["PL60"][-1] > 0.55, "the curve is front-loaded after month 4")
    dev = pd.read_parquet(os.path.join(T, "pd_model_development_sample.parquet"))
    d = dev[dev["outcome"] == "default"]
    ok((d["outcome_month_on_book"] <= 2).sum() == 0 and (d["outcome_month_on_book"] == 3).sum() < 0.02 * len(d), "development defaults start at month 3 or later")
    share = dev.assign(x=dev["outcome"] == "default").groupby("risk_grade")["x"].mean()
    ok(share["A"] < 0.06 and share["E"] < 0.30 and share.is_monotonic_increasing, "default share rises A to E at a sustainable level")
    # 5 loss flows reconcile in scale
    wo = pd.read_csv(os.path.join(T, "write_offs_2025-07_2026-09.csv"))
    bands = [((dpd >= x) & (dpd < x + 30)).sum() for x in (90, 120, 150)]
    ok(0.6 <= wo["loans_written_off"].mean() / np.mean(bands) <= 1.4, "monthly write-offs agree with the stage 3 bands (%.1f vs %.1f)" % (wo["loans_written_off"].mean(), np.mean(bands)))
    # 6 calendars
    ok(all(is_bd(x) for x in draw), "loans are funded on NSW business days")
    ok((draw.map(lambda x: x.day) >= 29).sum() > 100, "funding on the 29th to 31st")
    gap = np.array([(f - x).days for f, x in zip(first, draw)])
    ok(gap.min() >= 14 and gap.max() <= 44, "first repayment 2 to 6 weeks after funding")
    same = np.mean([f == dt.date(x.year + (x.month == 12), x.month % 12 + 1, min(x.day, 28)) for f, x in zip(first, draw)])
    ok(0.2 < same < 0.6, "about four in ten first repayments one month after funding")
    dv = dev["drawdown_month"].value_counts()
    bm = draw.map(lambda x: x.strftime("%Y-%m")).value_counts()
    ok(dv["2020-04"] < 0.7 * dv["2020-02"] and bm["2025-12"] < bm["2025-11"], "volumes carry the 2020 shock and December seasonality")
    # 7 grades follow the application score bands; no pile-ups at the ends of the scale
    f3 = dict(W.BANDS_V3)
    f4 = dict(W.BANDS_V4)
    band = [next((g for g in W.GRADES if sc >= (f4 if card == "v4" else f3)[g]), "E")
            for sc, card in zip(bk["origination_score"], bk["origination_scorecard"])]
    ok(np.mean(np.array(band) == bk["risk_grade"].values) > 0.97, "grades follow the score bands")
    for col in ("origination_score", "current_score_v4"):
        vc = bk[col].value_counts()
        ok(vc.get(bk[col].max(), 0) < 5, "%s has no pile-up at its maximum" % col)
    # 8 pricing by grade, product and the rate cycle
    med = bk.groupby(["risk_grade", "product"])["contract_rate"].median().unstack()
    ok((med["PL60"] > med["PL36"]).sum() >= 4, "PL60 priced above PL36 in most grades")
    yr = draw.map(lambda x: x.year)
    c = bk[(bk["risk_grade"] == "C") & (bk["product"] == "PL60")].assign(y=yr)
    ok(c[c.y == 2024]["contract_rate"].median() - c[c.y == 2022]["contract_rate"].median() > 0.015, "rates follow the cash rate cycle")
    # 9 booked amounts
    vc = bk["original_amount"].value_counts()
    ok(vc.index[0] < 50000 and bk["original_amount"].max() > 50000, "the cap is not the most common amount")
    ch = bk["channel"].value_counts(normalize=True)
    ok(ch.max() - ch.min() > 0.2 and abs(bk["product"].eq("PL36").mean() - 0.5) > 0.01, "channel and product mixes are not even splits")
    vs = bk["state"].value_counts()
    sh = 100 * vs / len(bk)
    ok(vs.is_unique and (np.abs(sh - np.round(sh)) >= 0.15).sum() >= 6, "state counts all differ and the shares sit off whole percentages (%s)" % sh.round(2).to_dict())
    # 10 behaviour scores: the origination score on v4 until the first repayment falls due, moving after that
    o4 = np.where(bk["origination_scorecard"] == "v3", np.floor(1.12 * bk["origination_score"] - 18 + 0.5), bk["origination_score"])
    fresh = a == 0
    cur = bk["current_score_v4"].values
    ok(fresh.sum() > 500 and (cur[fresh] == o4[fresh]).all(), "behaviour score is the v4 origination score until the first repayment falls due (%d loans)" % fresh.sum())
    ok((cur[~fresh] != o4[~fresh]).mean() > 0.9, "behaviour scores move once repayments fall due")
    # 11 the scorecard follows the application date, and loan numbers follow applications
    num = bk["loan_no"].str[3:9].astype(int)
    v3 = (bk["origination_scorecard"] == "v3").values
    sw = dt.date(2024, 7, 1)
    ok(num[v3].max() < num[~v3].min(), "every v3 loan number precedes every v4 loan number")
    ok((draw[v3] >= sw).sum() >= 50 and (draw[~v3] >= sw).all(), "loans applied for before 1 July 2024 and funded after it stay on v3 (%d)" % (draw[v3] >= sw).sum())
    luhn = lambda q: (10 - sum((lambda x: x - 9 if x > 9 else x)(int(c) * (2 if i % 2 == 0 else 1)) for i, c in enumerate(q[::-1])) % 10) % 10
    ok(all(int(x[-1]) == luhn(x[3:9]) for x in bk["loan_no"]), "loan numbers carry a Luhn check digit")
    # 12 nothing is payable under a payment pause in force, so a loan in one carries no arrears
    pz = act.loc[act["arrangement_type"] == "Payment pause", "loan_no"]
    dp = bk.set_index("loan_no").loc[pz, "days_past_due"]
    ok(len(pz) > 50 and (dp == 0).all(), "no arrears on a loan under a payment pause in force on the reporting date (%d pauses)" % len(pz))
    # 13 agreed repayments: round amounts offered, interest only, a share of the instalment, token amounts
    red = hd.loc[hd["arrangement_type"] == "Reduced repayments", "agreed_repayment_aud"]
    ok((red % 5 == 0).mean() < 0.75 and (red % 1 != 0).mean() > 0.1 and (red <= 50).mean() > 0.03,
       "agreed repayments are a realistic mix (multiples of 5 %.2f, cents %.2f, $50 or less %.2f)" % ((red % 5 == 0).mean(), (red % 1 != 0).mean(), (red <= 50).mean()))
    # 14 loss history: recoveries against write-offs in the window, and defaults resolved before write-off
    rec = wo["recoveries_aud"].sum() / wo["gross_write_off_aud"].sum()
    ok(0.15 <= rec <= 0.30, "recoveries run at %.3f of gross write-offs over the 15 months" % rec)
    ok(wo["loans_written_off"].mean() < 0.95 * ((dpd >= 90) & (dpd < 120)).sum(), "fewer loans are written off each month than reach 90 days past due")
    # 15 the curve's development data end before it was extracted and approved
    import pyarrow.parquet as pq
    head = open(os.path.join(T, E.F["curve"])).read().split("product,")[0]
    meta = {k.decode(): v.decode() for k, v in pq.read_schema(os.path.join(T, "pd_model_development_sample.parquet")).metadata.items() if not k.startswith(b"pandas")}
    ok("performance to 31 May 2026" in head and "24 June 2026" in head and meta["performance_to"] == "2026-05-31"
       and meta["performance_to"] < meta["extracted"] <= "2026-06-24" and "30 June 2026" not in head + str(meta),
       "development performance ends 31 May 2026, before extraction on %s and approval on 24 June" % meta["extracted"])
    ex = dt.date.fromisoformat(meta["extracted"])
    room = sum(is_bd(ex + dt.timedelta(days=i)) for i in range(1, (dt.date(2026, 6, 24) - ex).days))
    ok(is_bd(ex) and ex <= dt.date(2026, 6, 5) and room >= 14,
       "the sample is extracted on a business day in the first days of June, leaving %d business days to develop and "
       "validate the curve before the 24 June approval" % room)
    ok("pd_model_development_sample" not in head, "the curve header names the development sample, not the shipped file")


def docx_text(path):
    import re
    import zipfile
    with zipfile.ZipFile(path) as z:
        return " ".join(re.sub(r"<[^>]+>", "", p) for p in re.findall(r"<w:p [^>]*>.*?</w:p>", z.read("word/document.xml").decode(), re.S))


def readings(s):
    """the golden's stage 2 set is the one CRM-ECL-04 2.2 gives whatever the register's status labels say; and what the
    two pinned conventions are worth: staging on the status label alone, and leaving repayment dates inside a payment
    pause out of months on book"""
    import hashlib
    L = s["loans"]
    ids = sorted(L.loc[L["stage"] == 2, "loan_no"])
    ok(len(ids) == 3265 and hashlib.sha256("\n".join(ids).encode()).hexdigest()
       == "a9d1f93ee50eae023bfd0e571d749ad1abe9a8e7f10ebda2ca09fcb3085e1d07", "the stage 2 set is the one built before the "
       "register carried status lag (%d loans)" % len(ids))
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
    ok((hd["arrangement_status"] == want).all(), "every other status agrees with the dates and the weekly run")
    # staging on the status label alone moves a loan or two in the stage and product table and leaves the allowance
    # in its bin
    orig = E.stage

    def by_status(bk_, hd_, mapping_, use_hardship=True, map_v3=True):
        st = orig(bk_, hd_, mapping_, use_hardship, map_v3)
        act = set(hd_.loc[hd_["arrangement_status"] == "Active", "loan_no"])
        st[bk_["loan_no"].isin(act) & (st == 1)] = 2
        return st
    E.stage = by_status
    try:
        alt = E.solve(T)
    finally:
        E.stage = orig
    g0, g1 = graded(s), graded(alt)
    by_label = [k for k in g0 if g0[k] != g1[k]]
    ok(g1["total"] == g0["total"], "staging on the status label alone keeps the allowance in its bin (%s move)" % by_label)
    # repayment dates inside a payment pause left out of months on book (the reading 3.2 rules out)
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
    g2 = graded(alt)
    moved = [k for k in g0 if g0[k] != g2[k]]
    ok(len(held) > 1000 and len(moved) >= 1, "leaving pause dates out of months on book (%d loans, %d dates) moves %d of %d "
       "graded figures, the allowance to %.0f: the 3.2 pin is load-bearing" % (len(held), sum(held.values()), len(moved),
                                                                            len(g0), alt["total"]))
    return (len(held), sum(held.values()), len(moved), alt["total"]), (int(stale.sum()), by_label)


def residue_and_pins():
    import re
    import zipfile
    bk = pd.read_csv(os.path.join(T, E.F["book"]))
    nulls = bk.isna().sum()
    ok(set(nulls[nulls > 0].index) == {"state"} and 20 <= nulls["state"] <= 100,
       "the book's only blanks are the state of borrowers with an overseas address (%d), a field the allowance never reads"
       % nulls["state"])
    hd = pd.read_excel(os.path.join(T, E.F["hardship"]), sheet_name=0)
    nr = hd[hd["hardship_reason"].isna()]
    ok(3 <= len(nr) <= 12 and (nr["received_date"].dt.date < W.REASON_REQUIRED).all(),
       "a few cases from before the reason became a required field carry none (%d)" % len(nr))
    lk = hd[(hd["hardship_reason"] == "COVID-19") & (hd["received_date"].dt.year == 2021)]
    ok(len(lk) > 50 and not lk["loan_no"].isin(set(bk["loan_no"])).any() and (lk["arrangement_end"] < "2022-03-01").all(),
       "the 2021 lockdown pauses (%d) sit on loans closed before the reporting date" % len(lk))
    # the pins, in every place that defines them
    pol = docx_text(os.path.join(T, "CRM-ECL-04_expected_credit_loss_personal_loans.docx"))
    head = open(os.path.join(T, E.F["curve"])).read().split("product,")[0]
    import pyarrow.parquet as pq
    meta = {k.decode(): v.decode() for k, v in pq.read_schema(os.path.join(T, "pd_model_development_sample.parquet")).metadata.items()}
    dic = " ".join(open(os.path.join(T, "ecl_extract_dictionary.txt")).read().split())
    ok("Repayment dates during a payment pause count as repayments fallen due" in pol
       and "treated as being in the final month of its term, with a remaining term of one month" in pol
       and "repayment dates during a payment pause count" in head
       and "repayment dates during a payment pause included" in meta["outcome_month_on_book"]
       and "which stay in the loan's schedule" in dic and "the maturity date does not change" in dic
       and "Completed is set by the weekly hardship batch on Tuesday nights" in dic,
       "payment pauses and past-maturity loans are pinned in the policy, the curve header, the sample metadata and the dictionary")
    ok("more than 30 days past due" in pol and "30 or more days past due" in pol, "2.5 quotes AASB 9 5.5.11 as more than 30 days")
    # the containers: the Office 2013-2022 theme as Word and Excel write it, a workbook theme version to match, creation
    # dates before the 2023 theme for workbooks rolled forward, the register written by the job's account
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
                ok(who == W.JOB_ACCOUNT and "<cp:lastModifiedBy>Kayla Stokes<" in core,
                   "the register is written by the job's account and last saved by Credit Risk Reporting")
    with zipfile.ZipFile(os.path.join(T, "CRM-ECL-04_expected_credit_loss_personal_loans.docx")) as z:
        app = z.read("docProps/app.xml").decode()
        doc = z.read("word/document.xml").decode()
    st = {k: int(v) for k, v in re.findall(r"<(Lines|Paragraphs|Words|Characters|CharactersWithSpaces)>(\d+)<", app)}
    ok(st["Lines"] >= 1.25 * st["Paragraphs"] and st["CharactersWithSpaces"] > st["Characters"] > 4 * st["Words"],
       "the policy's statistics are the word processor's measurement (%s)" % st)
    from collections import Counter
    rs = Counter(re.findall(r'<w:p [^>]*w:rsidR="([0-9A-F]{8})"', doc))
    ok(len(rs) >= 8 and rs.most_common(1)[0][1] >= 0.25 * sum(rs.values()) and doc.count('<w:r w:rsidR="') >= 10,
       "the policy's revision ids follow its history: %d sessions, the busiest %d of %d paragraphs, %d later edits inside "
       "paragraphs" % (len(rs), rs.most_common(1)[0][1], sum(rs.values()), doc.count('<w:r w:rsidR="')))


def main():
    gates()
    s, rung = answer_and_ladder()
    realism()
    pause, label = readings(s)
    residue_and_pins()
    print("CHECKS PASS", n_ok, {k: round(v, 4) for k, v in rung.items()})
    print("pause dates left out of months on book: %d loans, %d dates, %d graded figures move, allowance %.0f" % pause)
    print("staging on the status label alone (%d stale Active arrangements): %s move, the allowance keeps its bin" % label)


if __name__ == "__main__":
    main()
