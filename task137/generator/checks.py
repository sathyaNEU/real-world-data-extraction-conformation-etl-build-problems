"""task137 generator checks: the input gates, the three-rules block (R1 to R3c, executed on the generator's clean
truth), the call and its bins, the ladder and every rival basis the design note and the audit name, the estimator
corridor, every semantic fork row (SF1 to SF25), the domain claims the note and write-up make, the asks' goldens,
stops and devices, the separation and distractor deletion tests, the realism sweep and the goldens' agreement with
figures.json. Run by build.py on the built pack; raises on the first failure and prints the count of assertions
passed."""
from __future__ import annotations

import datetime as dt
import json
import os
import re
import shutil
import tempfile

import numpy as np
import pandas as pd

import asks as AK
import calc as C
import golden as GD
import world as W

N = [0]
ASK_FILES = [W.F_EVENTS, W.F_TRANSFERS, W.F_HOLDINGS, W.F_KIP, W.F_BATCHES]


def ok(cond, msg):
    if not cond:
        raise AssertionError(msg)
    N[0] += 1


def h250(x):
    return GD.h250(x)


def k1000(x):
    return GD.k1000(x)


def room(x, unit):
    """Distance from x to the nearest rounding edge of its bin, in the figure's own units."""
    return abs((x % unit) - unit / 2.0)


def pdf_text(path):
    import pdfplumber
    with pdfplumber.open(path) as pdf:
        return " ".join(" ".join((p.extract_text() or "").split()) for p in pdf.pages)


def docx_text(path):
    import docx
    return " ".join(p.text for p in docx.Document(path).paragraphs)


def months_of(F, U, Cc, R, p):
    return C.hours(F, C.minutes(F, U, Cc, R, p))


def golden_on_copy(target, drop_files):
    tmp = tempfile.mkdtemp(suffix=".t137")
    try:
        for f in os.listdir(target):
            if f not in drop_files:
                shutil.copy2(os.path.join(target, f), os.path.join(tmp, f))
        L2 = C.load(tmp)
        G2 = C.golden(L2)
        out = dict(total=G2["total"], months=G2["months"])
        if not set(drop_files) & set(ASK_FILES):
            A2 = AK.load(tmp)
            out["a"] = AK.ask_a(A2)
            out["b"] = AK.ask_b(A2)
        return out
    finally:
        shutil.rmtree(tmp)


def truth_tables(Wd, F):
    """The generator's clean truth (no mess, no pack): every past conversation's class, drop and outcome as the
    simulation made them, and the coming list's classes and drops against the January to March 2027 card."""
    rows = []
    for q in W.PAST:
        for co in Wd.campaigns[q]["closeouts"]:
            if co["outcome"] in W.CONVERSATION + W.RETENTION:
                rows.append((q, co["acct"], bool(co["special"]), round(co["drop"], 2), int(co["term"]),
                             float(co["rate"]), co["outcome"] in W.RETENTION))
    past = pd.DataFrame(rows, columns=["campaign", "account", "special", "drop", "term", "rate", "ret"])
    fl = Wd.campaigns[W.FWD]["listed"]
    fwd = pd.DataFrame({"account": [d["acct"] for d in fl], "special": [bool(d["special"]) for d in fl],
                        "drop": [round(d["rate"] - W.card(W.FWD, d["term"]), 2) for d in fl],
                        "term": [d["term"] for d in fl], "rate": [d["rate"] for d in fl]}, index=F.index)
    return past, fwd


def truth_share(past, fwd, basis):
    if basis == "pooled":
        return np.full(len(fwd), past["ret"].mean())
    if basis == "term":
        return fwd["term"].map(past.groupby("term")["ret"].mean()).values
    if basis == "latest":
        return np.full(len(fwd), past[past["campaign"] == W.PAST[-1]]["ret"].mean())
    if basis == "locked rate":
        s = past.groupby(np.floor(past["rate"] / 0.25 + 1e-9))["ret"].mean()
        keys = np.array(sorted(s.index))
        return np.floor(fwd["rate"] / 0.25 + 1e-9).map(lambda k: s[keys[np.argmin(np.abs(keys - k))]]).values
    if basis == "drop":
        return C.p_from_bins(fwd["drop"], C.share_bins(past.assign(conv=True), 0.25), 0.25, fallback=True).values
    if basis == "class x drop":
        p = np.zeros(len(fwd))
        for cls in (True, False):
            idx = (fwd["special"] == cls).values
            s = C.share_bins(past[past["special"] == cls].assign(conv=True), 0.25)
            p[idx] = C.p_from_bins(fwd.loc[idx, "drop"], s, 0.25).values
        return p
    raise ValueError(basis)


def run(target, golden, Wd=None, H=None, meta_path=None):
    p = lambda f: os.path.join(target, f)
    L = C.load(target)
    G = C.golden(L)
    F, cases, R, U, Cc = G["F"], G["cases"], G["R"], G["U"], G["C"]
    cv = cases[cases["conv"]]
    g, gm = G["total"], G["months"]
    figs = json.load(open(os.path.join(os.path.dirname(golden), "generator", "figures.json")))
    sow, proc = pdf_text(p(W.F_SOW)), docx_text(p(W.F_PROCEDURE))
    briefs = {q: pdf_text(p(W.brief_name(q))) for q in W.PAST + [W.FWD]}
    prompt = open(os.path.join(os.path.dirname(golden), "prompt.txt"), encoding="utf-8").read()
    files = sorted(os.listdir(target))

    # ------------------------------------------------------------------ input gates
    ok(len(files) >= 10, "fewer than 10 files")
    fmts = {f.rsplit(".", 1)[1] for f in files}
    ok(len(fmts) >= 3, "fewer than 3 formats: %s" % fmts)
    with open(p(W.F_DIALS)) as fh:
        ok(sum(1 for _ in fh) - 1 >= 25000, "no file of 25,000 rows")
    meta = json.load(open(meta_path))
    ok(sorted(meta["distractor_files"]) == sorted(W.DISTRACTORS), "metadata distractors")
    ok(all(d in files for d in W.DISTRACTORS), "a distractor is missing from the pack")
    ok(not any("distractor" in f.lower() for f in files), "a file name says distractor")
    ok(meta["deliverables"] == [GD.BOOK, GD.NOTE], "metadata deliverables")
    ok(len(meta["files"]) == len(files) and all(x["license"] and x["source"] and x["date"] for x in meta["files"]),
       "metadata file records")

    # ------------------------------------------------------------------ the call
    ok(len(F) == W.FWD_LIST_SIZE == 18400, "list size %d" % len(F))
    ok(abs(sum(gm.values()) - g) < 1e-6, "months do not add to the total")
    ok(sum(h250(v) for v in gm.values()) == h250(g), "rounded months do not add to the rounded booking")
    ok(figs["call"]["booking_hours"] == "{:,}".format(h250(g)), "figures.json booking")
    for k, nm in GD.MONTHS.items():
        ok(figs["call"]["hours_by_month"][nm] == "{:,}".format(h250(gm[k])), "figures.json %s" % nm)
    ok(room(g, 250) >= 40, "SF13 booking %.1f within 40 hours of an edge" % g)
    for k in (1, 2, 3):
        ok(room(gm[k], 250) >= 40, "SF13 month %d %.1f within 40 hours of an edge" % (k, gm[k]))

    # ------------------------------------------------------------------ the three rules, executed (dataset-generation 7.1)
    Rg = C.rungs(L, G)
    rv = Rg["rivals"]
    csv_heads = " ".join(open(p(f), encoding="utf-8").readline().lower() for f in files if f.endswith(".csv"))
    ok(not re.search(r"special|premium|drop|class|share|promo|offer", csv_heads),
       "R1: a shipped column names the class, the drop or a share")
    lists_2025 = open(p(W.F_LISTS_2025), encoding="utf-8").readline()
    ok("Rate %" in lists_2025 and "Opened" in lists_2025 and "Term (mths)" in lists_2025,
       "R1: the 2025 lists carry each deposit's rate, term and opening date")
    ok(all(k in open(p(W.F_LISTS_2026), encoding="utf-8").readline() for k in ("int_rate", "start_date", "term_months")),
       "R1: the 2026 lists carry each deposit's rate, term and opening date")
    ok(len(cv) > 40000 and cases["special"].sum() > 3000 and F["special"].sum() > 9000,
       "R1: the class is rebuilt from %d past conversations on row-level lists" % len(cv))
    texts = " ".join([sow, proc] + list(briefs.values()) + [open(p(W.F_NOTES), encoding="utf-8").read()]).lower()
    ok("special" not in texts and "retention share" not in texts and "rollover rate" not in texts,
       "R1: no filed document names a special, a retention share or a rollover rate")
    if Wd is not None:
        past_t, fwd_t = truth_tables(Wd, F)
        ok((fwd_t.index == F.index).all() and list(fwd_t["account"]) == list(F["account"]),
           "the clean truth's coming list is the pack's")
        # R2: the mess on the call's path (two list layouts, account formats, rates in per cent and in decimals, PDF
        # cards in two layouts) leaves every past conversation's class and drop as the simulation made them
        tk = past_t.set_index(["campaign", "account"])
        ck = cv.set_index(["campaign", "account"])
        ok(len(tk) == len(ck) and tk.index.is_unique and ck.index.is_unique, "R2: conversations line up")
        j = ck.join(tk[["special", "drop", "ret"]], rsuffix="_t")
        ok((j["special"] == j["special_t"]).all(), "R2: the class read from the pack differs from the truth's")
        ok(np.allclose(j["drop"], j["drop_t"]) and (j["ret"] == j["ret_t"]).all(),
           "R2: the drop or the outcome read from the pack differs from the truth's")
        ok((fwd_t["special"].values == F["special"].values).all() and np.allclose(fwd_t["drop"], F["drop"]),
           "R2: the coming list's classes or drops differ from the truth's")
        # R3a: the easy route on the clean truth, every filed rule applied (the SOW minutes and dialling yields, the
        # release share, the wash, the procedure's rounding), files the default path's wrong answer
        for basis in ("pooled", "term", "latest", "locked rate", "drop"):
            tot, mon = months_of(F, U, Cc, R, truth_share(past_t, fwd_t, basis))
            ok(h250(tot) <= h250(g) - 500 and all(h250(mon[k]) != h250(gm[k]) for k in (1, 2, 3)),
               "R3a: the %s share on the clean truth books %d, within two bins of %d" % (basis, h250(tot), h250(g)))
            if basis in ("pooled", "drop"):
                ok(h250(tot) == int(figs["default_path"]["%s_hours" % ("pooled_share" if basis == "pooled" else "drop")]
                                   .replace(",", "")), "R3a: the clean truth's %s route is not the default path's" % basis)
        # R3b: the same route with only the decisive step changed (the class of money beside the drop) files the
        # golden; the drop alone, the term or the locked rate each leave it wrong
        tot, mon = months_of(F, U, Cc, R, truth_share(past_t, fwd_t, "class x drop"))
        ok(h250(tot) == h250(g) and all(h250(mon[k]) == h250(gm[k]) for k in (1, 2, 3)),
           "R3b: the class beside the drop on the clean truth books %d against %d" % (h250(tot), h250(g)))
    # R3c: nothing planted
    ok(not any(w in f.lower() for f in files for w in ("memo", "draft", "forecast", "booking")),
       "R3c: a memo, draft, forecast or past booking ships")
    eml = open(p(W.F_THREAD), encoding="utf-8", errors="replace").read()
    ok(not re.search(r"\b\d{1,2},\d{3} (?:agent-)?hours\b", eml + briefs[W.FWD] + proc + sow),
       "R3c: a filed document states a number of hours")

    # ------------------------------------------------------------------ the ladder and every rival
    for k in ("R0_latest", "R0_all"):
        ok(Rg[k] <= 0.92 * g and h250(Rg[k]) != h250(g), "rung %s %.1f too near the golden %.1f" % (k, Rg[k], g))
    ok(Rg["R3_no_release"] >= 1.03 * g and h250(Rg["R3_no_release"]) != h250(g), "the class without the release share")
    audit = ("pooled", "term", "latest", "trend", "locked rate", "locked rate by term logit",
             "term + locked rate logit", "locked rate by term linear", "drop bands", "drop logit")
    ok(all(a in rv for a in audit) and len(rv) >= 22, "a rival the audit measured is missing")
    for nm, (tot, mon) in rv.items():
        ok(tot <= 0.92 * g, "rival %s %.1f within 8 per cent of the golden" % (nm, tot))
        ok(h250(tot) <= h250(g) - 500, "rival %s books %d, within two bins of %d" % (nm, h250(tot), h250(g)))
        ok(all(h250(mon[k]) != h250(gm[k]) for k in (1, 2, 3)), "rival %s lands a month: %s" % (nm, mon))
    ok(figs["default_path"]["pooled_share_hours"] == "{:,}".format(h250(rv["pooled"][0])), "default path figure")
    ok(figs["default_path"]["drop_hours"] == "{:,}".format(h250(rv["drop bands"][0])), "the drop's figure")

    # ------------------------------------------------------------------ the corridor (SF7, SF8, SF9, SF22)
    fam = C.family(L, G)
    for nm, (tot, mon) in fam.items():
        ok(h250(tot) == h250(g), "SF8/SF9 %s files %d" % (nm, h250(tot)))
        ok(all(h250(mon[k]) == h250(gm[k]) for k in (1, 2, 3)), "SF8/SF9 %s month %s" % (nm, mon))
    ok(len(fam) >= 30, "family too small")
    member = cv[~cv["special"]]
    pl, coef = C.p_linear(member, F["drop"])
    ok(coef[0] + coef[1] * member["drop"].min() < 0 and member.loc[member["drop"] < -1, "ret"].mean() < 0.01,
       "SF8 the linear fit is not refused by the past data")

    # ------------------------------------------------------------------ SF rows
    ok("Agent time is billed per event at the minutes below" in sow and "agent-hours" in sow, "SF1 SOW 2.1")
    ok(not any(w in f.lower() for f in files for w in ("roster", "timesheet", "shift")), "SF1 shift data shipped")
    ok("forecast to need, rounded to the nearest 250 hours" in proc, "SF2 procedure 6.1")
    ok("in multiples of 250" in sow, "SF2 SOW 2.2 block multiples")
    ok(F["customer_no"].is_unique and "The list carries one deposit per member" in proc, "SF3 one deposit per member")
    ok(F["maturity"].min() >= pd.Timestamp("2027-01-01") and F["maturity"].max() <= pd.Timestamp("2027-03-31"),
       "SF4 maturities outside the quarter")
    dnc = L["dnc"]
    ok(pd.to_datetime(dnc["recorded"]).max() <= pd.Timestamp(W.CUT_FWD), "SF5 register entry after the cut")
    wd = pd.to_datetime(dnc["withdrawn"].replace("", None)).dropna()
    ok(wd.empty or wd.max() <= pd.Timestamp(W.CUT_FWD), "SF5 withdrawal after the cut")
    ok(pd.to_datetime(L["contacts"]["recorded"]).max() <= pd.Timestamp(W.CUT_FWD), "SF5 contact point after the cut")
    ok("reinvests for the same term at the posted rate in force on its maturity date" in proc, "SF6 Terms 9.2 in 5.1")
    ok("Reinvestment rates for deposits maturing this quarter" in briefs[W.FWD] and "draft" in briefs[W.FWD],
       "SF6 the draft brief's rates")
    ok("as approved by ALCO" in briefs[W.FWD], "SF6 the card approved")
    ok("every campaign the contact centre has closed under the statement of work" in proc, "SF7 procedure 6.1")
    for nm in ("subset/2025", "subset/2026", "subset/latest4"):
        ok(nm in fam, "SF7 %s missing" % nm)
    ok(float(G["m"][F["cfg"] == ""].abs().sum()) == 0.0, "SF10 hours on a deposit with no callable number")
    ok("A deposit with no callable number is not released" in proc, "SF10 procedure 4.3")
    rel = L["release"]
    ok(set(rel.loc[rel["status"] == "NOT RELEASED", "reason"]) == {"INSTRUCTED", "NO CALLABLE NUMBER"},
       "SF11 release reasons")
    ok(set(rel.loc[rel["status"] == "RELEASED", "reason"]) == {""}, "SF11 released rows carry a reason")
    ok("A deposit is not released if the holder has given maturity instructions by then" in proc, "SF11 procedure 4.2")
    cl = L["close"]
    ok(len(cl) == int((rel["status"] == "RELEASED").sum()), "SF11 one close-out per released case")
    ok((cl["close_reason"] == "WITHDRAWN").sum() > 100, "SF12 withdrawn cases in the close-outs")
    ok(set(cl["close_reason"]) <= {"CONVERSATION", "EXHAUSTED", "WITHDRAWN", "MATURED"}, "SF12 close reasons")
    ok("structural/class-bins0.25+0.000" in fam, "SF12 the per-number model with withdrawals")
    row22 = re.search(r"intend to withdraw ([A-Z, ]+?) 22 or move the funds", sow)
    ok(row22 is not None and set(row22.group(1).replace(",", " ").split()) == set(W.RETENTION), "SF14 SOW 22-minute row")
    row15 = re.search(r"does not reach the holder ([A-Z, ]+?) 1\.5", sow)
    ok(row15 is not None and set(row15.group(1).replace(",", " ").split()) == set(W.NOT_REACHED),
       "SF15 SOW 1.5-minute row")
    for m in sorted(set(F["maturity"].dt.date)):
        ok(len(W.dialling_days(m - dt.timedelta(days=21), m)) >= W.DIALS_PER_NUMBER,
           "SF16 %s has too few dialling days" % m)
    raw = pd.read_csv(p(W.F_LIST_FWD), dtype=str)
    st_ = pd.to_datetime(raw["start_date"])
    mt = pd.to_datetime(raw["maturity_date"])
    yrs = raw["term_months"].astype(int) // 12
    ok(all((m_.year - s_.year == y_) and (m_.month == s_.month) for s_, m_, y_ in zip(st_, mt, yrs)),
       "SF17 a term disagrees with its dates")
    # SF22: the class. Every gap from 0.30 to 0.45 classes the same deposits on every list (asserted on the premiums:
    # nothing sits between 0.25 and 0.50 above its cohort's lowest rate), and the lowest rate of a cohort is the posted
    # rate wherever a brief covers its opening quarter
    plists = L["past_lists"]
    prem = pd.concat([C.premium(plists, "campaign"), C.premium(L["fwd"])])
    ok(not ((prem > 0.25 + 1e-9) & (prem < 0.50 - 1e-9)).any() and prem.max() <= 0.60 + 1e-9,
       "SF22 a premium between 0.25 and 0.50 points")
    for gap in (0.30, 0.35, 0.45):
        ok((C.special_class(plists, "campaign", gap) == plists["special"]).all() and
           (C.special_class(L["fwd"], None, gap) == L["fwd"]["special"]).all(), "SF22 gap %.2f classes others" % gap)
        ok(("class-gap%.2f" % gap) in fam, "SF22 gap %.2f not in the family" % gap)
    lowest = list(plists.groupby(["campaign", "term", C.opening_quarter(plists["opened"])])["rate"].min().items())
    fl = L["fwd"]
    lowest += [(("2027Q1", t, oq), v) for (t, oq), v in
               fl.groupby(["term", C.opening_quarter(fl["opened"])])["rate"].min().items()]
    covered = [(qc, t, oq, v) for (qc, t, oq), v in lowest if oq in L["cards"]]
    ok(len(covered) >= 4 and all(abs(v - L["cards"][oq][t]) < 1e-9 for _, t, oq, v in covered),
       "SF22 a cohort's lowest rate is not the posted rate in its opening quarter's brief (%d cohorts)" % len(covered))
    fwd_modes = C.special_class(L["fwd"], None, base="mode")
    ok(fwd_modes.sum() < 100, "SF22 the cohort's mode classes the special itself")

    # ------------------------------------------------------------------ domain claims in the note and write-up
    sp_c, mb_c = cv[cv["special"]], cv[~cv["special"]]
    for (q, t, d_), sub in sp_c.groupby(["campaign", "term", "drop"]):
        if len(sub) >= 200:
            ok(sub["ret"].mean() >= 0.80, "special money's share %s %d %.2f is %.3f" % (q, t, d_, sub["ret"].mean()))
    ok(sp_c.groupby(["campaign", "term", "drop"]).ngroups >= 6 and sp_c["term"].nunique() >= 3,
       "special money matured at too few drops or terms")
    for q, sub in mb_c.groupby("campaign"):
        b_ = C._fit(np.column_stack([np.ones(len(sub)), sub["drop"].values]), sub["ret"].astype(float).values)
        lo_, hi_ = sub[sub["drop"] < 0.5]["ret"].mean(), sub[sub["drop"] >= 1.0]["ret"].mean()
        ok(b_[1] > 0.5 and hi_ > lo_ + 0.08, "member money's share does not rise with the drop in %s (slope %.2f, %.3f "
           "against %.3f)" % (q, b_[1], hi_, lo_))
    bk = np.floor(cv["drop"] / 0.25 + 1e-9)
    both = cv.groupby([bk, cv["special"]])["ret"].agg(["mean", "size"]).unstack()
    for b_ in both.index:
        if both.loc[b_, ("size", True)] >= 100 and both.loc[b_, ("size", False)] >= 100:
            ok(both.loc[b_, ("mean", True)] > both.loc[b_, ("mean", False)] + 0.3,
               "in the band from %.2f the classes do not separate" % (0.25 * b_))
    c_ = GD.compute(target)
    fc, fs = figs["components"], figs["steps"]
    lo_b = c_["band_lo"]
    band = cv[(cv["drop"] >= lo_b - 1e-9) & (cv["drop"] < lo_b + 0.25 - 1e-9)]
    ok(band["special"].mean() < 0.15, "the special's band is not almost all member money (%.3f)" % band["special"].mean())
    ok(fc["past_band_special_share_pct"] == GD.pct(band[band["special"]]["ret"].mean()) and
       fc["past_band_member_share_pct"] == GD.pct(band[~band["special"]]["ret"].mean()), "band shares")
    ok(fc["past_special_share_pct"] == GD.pct(sp_c["ret"].mean()) and
       fc["past_pooled_share_pct"] == GD.pct(cv["ret"].mean()), "class shares")
    ok(mb_c["ret"].mean() < 0.5 * sp_c["ret"].mean() and band["ret"].mean() < 0.5 * sp_c["ret"].mean(),
       "other deposits do not go to the offer far less often")
    ok(fs["past_special_conversations"] == "{:,}".format(len(sp_c)), "special conversations")
    sp = F[F["special"]]
    ok(fc["special_deposits"] == "{:,}".format(len(sp)) and len(sp) > 0.5 * len(F), "the special's deposits")
    oq_sp = set(C.opening_quarter(sp["opened"]))
    ok(len(oq_sp) == 1 and fc["special_opened"] == W.q_label(oq_sp.pop()) and figs["call"]["quarter"] == W.q_label(W.FWD),
       "the special's opening quarter or the list's quarter")
    ok(set(sp["drop"].round(2)) == {round(float(fc["special_rate_pct"]) - L["cards"][W.FWD][int(fc["special_term_years"])], 2)},
       "the special's drop")
    ok(lo_b <= float(fc["drop_points"]) < lo_b + 0.25, "the special's band")
    cells_ = [sub["ret"].mean() for _, sub in sp_c.groupby(["campaign", "term", "drop"]) if len(sub) >= 200]

    def holds_(x):
        p2 = G["p"].copy()
        p2[F["special"]] = x
        t_, bm_ = C.hours(F, C.minutes(F, U, Cc, R, p2))
        return h250(t_) == h250(g) and all(h250(bm_[k]) == h250(gm[k]) for k in (1, 2, 3))
    ok(max(cells_) < 0.90 and len(cells_) >= 6, "special money's share is not much the same at every drop it met")
    ok(holds_(0.805) and not holds_(0.795) and min(cells_) > 0.85,
       "the flip: the booking holds down to a special share of 0.80, under every past special cell (from %.3f)"
       % min(cells_))
    past_specials = sorted({(int(t), float(r_)) for t, r_ in zip(sp_c["term"], sp_c["rate"])})
    ok(fs["past_specials"] == GD.specials_phrase(past_specials), "the specials named in the write-up")
    ok(float(cv[cv["term"] == int(fc["special_term_years"])]["ret"].mean()) < 0.05, "past four-year share")
    ok(not cv[cv["term"] == int(fc["special_term_years"])]["special"].any(), "a past four-year special")
    d = L["dials"]
    mins = d["outcome"].map(W.billed_minutes)
    listed = L["past_lists"].groupby("campaign").size()
    per = {q: float(mins[d["case_ref"].str[2:6] == q[2:4] + q[-2:]].sum()) / listed[q] for q in W.PAST}
    ok(max(per.values()) < g * 60 / len(F), "a past campaign used more minutes per listed deposit than the forecast")
    ok(len(set(listed.values)) == len(listed), "identical list sizes across campaigns")
    share = G["ret"] / G["conv"]
    ok(fc["retention_share_pct"] == GD.pct(share), "share figure")
    ok(room(100 * share, 1.0) >= 0.2, "the list's retention share %.2f within 0.2 of a rounding edge" % (100 * share))
    for x, nm in ((sp_c["ret"].mean(), "special"), (cv["ret"].mean(), "pooled"),
                  (band[band["special"]]["ret"].mean(), "band special"),
                  (band[~band["special"]]["ret"].mean(), "band member")):
        ok(room(100 * x, 1.0) >= 0.1, "the %s share %.2f within 0.1 of a rounding edge" % (nm, 100 * x))
    ok(figs["steps"]["non_reaching_dials"] == "{:,}".format(GD.n100(G["nr"])), "non-reaching dials figure")
    ok(figs["components"]["expected_conversations"] == "{:,}".format(GD.n500(G["conv"])) ==
       "{:,}".format(GD.n100(G["conv"])), "expected conversations figure")
    ok(figs["components"]["no_callable_number"] == "{:,}".format(int((F["cfg"] == "").sum())), "no callable count")
    ok(figs["steps"]["release_share_pct"] == "%.1f" % (100 * R), "release share")

    # ------------------------------------------------------------------ the asks
    A = AK.load(target)
    st = AK.all_stops(A)
    ga, gb = st["A"]["golden"], st["B"]["golden"]
    for q in W.PAST:
        n_, a_ = ga[q]
        ok(figs["ask_a"][q]["deposits"] == "{:,}".format(n_) and figs["ask_a"][q]["principal_nzd"] == "{:,}".format(
            k1000(a_)), "ask A figures %s" % q)
        ok(room(a_, 1000) >= 150, "ask A %s principal near an edge" % q)
        for mode in ("own", "direct", "holder", "nobreak", "fullonly"):
            n2, a2 = st["A"][mode][q]
            ok(n2 != n_ and k1000(a2) != k1000(a_), "ask A %s %s lands" % (mode, q))
        for mode in ("whole", "fullprin"):
            n2, a2 = st["A"][mode][q]
            ok(n2 == n_ and k1000(a2) != k1000(a_), "ask A %s %s" % (mode, q))
        n2, a2 = st["A"]["anyreinv"][q]
        if q.startswith("2026"):
            ok(n2 != n_ and k1000(a2) != k1000(a_), "ask A anyreinv %s lands" % q)
    ok(st["A"]["own"] == st["A"]["direct"], "ask A: the settlement account hides no direct link")
    for k in (1, 2, 3, "off"):
        nm = GD.MONTHS.get(k, "off")
        got = figs["ask_b"]["maturing_nzd"][nm] if k != "off" else figs["ask_b"]["quarter_not_on_list_nzd"]
        ok(got == "{:,}".format(k1000(gb[k])), "ask B figure %s" % nm)
        ok(room(gb[k], 1000) >= 150, "ask B %s near an edge" % nm)
        for mode in AK.B_MODES[1:]:
            ok(k1000(st["B"][mode][k]) != k1000(gb[k]), "ask B %s %s lands" % (mode, nm))
    reinv, gone, opens, by_holder, out, direct = AK._index(A)
    lists = A["lists"]
    ev = A["events"]
    mature = set(zip(ev.loc[ev["event_type"] == "MATURE", "account"], ev.loc[ev["event_type"] == "MATURE", "event_date"]))
    ok(all((a, m.date().isoformat()) in mature for a, m in zip(lists["account"], lists["maturity"])),
       "ask A a listed deposit has no MATURE event at its maturity")
    near = 0
    for a, m in zip(lists["account"], lists["maturity"]):
        m = m.date()
        accts = [a] + [to for to, _ in out.get((a, m), []) if to in opens]
        for x in accts:
            near += sum(1 for d_ in gone.get(x, []) if 25 <= (d_ - m).days <= 35)
    ok(near == 0, "ask A C1: %d breaks or closes between day 25 and day 35" % near)
    tr = A["transfers"]
    sav = tr["from_account"].str.len().eq(16) & tr["from_account"].str[-3:].isin(W.SAV_SUFFIXES)
    ok(not (sav & tr["to_account"].isin(set(opens))).any(), "ask A C1: savings moved into a term deposit")
    pay = set(zip(ev.loc[ev["event_type"] == "PAYOUT", "account"], ev.loc[ev["event_type"] == "PAYOUT", "event_date"]))
    ok(not any((a, d_.isoformat()) in pay for a, d_ in reinv), "ask A a deposit both reinvested and paid out")
    ok(sum(1 for (a, m), v in out.items() for to, _ in v if to in opens) > 1000, "ask A few change-of-term chains")
    mat_rows = tr[tr["from_account"] == W.SETTLEMENT]
    ok(len(mat_rows) > 5000 and mat_rows["narrative"].str.match(r"^TD MATURITY \d{2}-\d{4}-\d{7}-\d{3}$").all() and
       not tr.loc[tr["from_account"] != W.SETTLEMENT, "narrative"].str.contains("MATURITY").any(),
       "ask A: maturity proceeds are not all paid through the settlement account with the deposit's reference")
    fresh = set(opens) - set(tr.loc[tr["from_account"] == W.SETTLEMENT, "to_account"])
    ok(len(fresh) > 200, "ask A holders opened no deposits with new money (%d)" % len(fresh))
    hold = A["hold"]

    # ------------------------------------------------------------------ ask A readings (SF18 to SF21)
    ok("how much of the principal on its list was still on term deposit with us 30 days after maturity, and from how "
       "many of its deposits" in prompt, "SF18 the prompt's wording")
    ok(st["A"]["literal"] == ga, "SF18 the prompt executed on the extracts is not the golden")
    part = 0
    for a, prin, m in zip(lists["account"], lists["principal"], lists["maturity"]):
        moved = [am for to, am in out.get((a, m.date()), []) if to in opens and opens[to][0] == m.date()]
        part += bool(moved) and abs(sum(moved) - prin) > 0.005
    ok(part > 1000, "SF18 few deposits moved part of their principal (%d)" % part)
    for q in W.PAST:
        n_, a_ = ga[q]
        n2, a2 = st["A"]["fullonly"][q]
        ok(n2 < n_ and k1000(a2) < k1000(a_), "SF18 counting only deposits kept whole lands %s" % q)
        n2, a2 = st["A"]["fullprin"][q]
        ok(n2 == n_ and k1000(a2) > k1000(a_), "SF18 the whole principal of a part kept lands %s" % q)
    listed_accts = set(lists["account"])
    kic_accts = set(hold.loc[hold["product"] == "KIC", "account"]) | set(A["kip"]["cert_no"])
    src = [AK.source_of(fa, nar) for fa, nar in zip(tr["from_account"], tr["narrative"])]
    from_listed = tr[[s_ in listed_accts for s_ in src]]
    ok(not from_listed["to_account"].isin(kic_accts).any() and
       not from_listed["to_account"].str.endswith(W.KIC_SUFFIX).any(),
       "SF19 a listed deposit's principal reached an investment certificate")
    ok("principal on term deposits and investment certificates together" in prompt,
       "SF19 the prompt names term deposits and investment certificates apart")
    td_accts = set(ev["account"])
    into_td = from_listed[from_listed["to_account"].isin(td_accts)]
    ok(len(into_td) > 1000 and all(to in opens and opens[to][0].isoformat() == d_
                                   for to, d_ in zip(into_td["to_account"], into_td["value_date"])),
       "SF20 a listed deposit's principal went into a term deposit not opened that day")
    ok(not lists.duplicated(["campaign", "customer_no"]).any(), "SF21 a holder with two deposits on one list")
    ok(all(st["A"]["holder"][q][0] > ga[q][0] for q in W.PAST), "SF21 the holder's new money changes no count")

    # ------------------------------------------------------------------ ask B readings (SF23 to SF25)
    fwd = A["fwd"].set_index("account")
    hd = hold.drop_duplicates("account").set_index("account")
    ok(set(fwd.index) <= set(hd.index), "SF24 a listed deposit is missing from the holdings view")
    ok(np.allclose(hd.loc[fwd.index, "principal"].values, fwd["principal"].values), "SF24 principal disagrees")
    ok((hd.loc[fwd.index, "maturity_date"].values == fwd["maturity_date"].values).all(), "SF24 maturity disagrees")
    ok((hd.loc[fwd.index, "product"] == "TD").all(), "SF24 a certificate on the list")
    ok("how much of the quarter's total is not on the list" in prompt, "SF24 the prompt's wording")
    dup = hold[hold["account"].duplicated(keep=False)]
    ok(len(dup) > 1000 and (dup.groupby("account")["principal"].nunique() == 1).all(),
       "SF25 an account repeated under its holders with different principals")
    bt = A["batches"]
    both_ = set(bt.loc[bt["status"] == "DEFERRED", "cert_no"]) & set(bt.loc[bt["status"] == "MIGRATED", "cert_no"])
    ok(len(both_) > 10, "ask B no certificate deferred then moved")
    mig = bt[bt["status"] == "MIGRATED"]
    kic = hold[hold["product"] == "KIC"].drop_duplicates("account")
    kip = A["kip"].set_index("cert_no")
    key = lambda i, m, r_, t: (i, m, round(float(r_), 2), int(t))
    kip_key = {key(i, m, r_, t): c for c, i, m, r_, t in zip(kip.index, kip["issue_date"], kip["maturity_date"],
                                                             kip["rate"], kip["term_months"])}
    ok(len(kip_key) == len(kip), "SF23 two register certificates share issue date, maturity, rate and term")
    core_key = {a: key(i, m, float(r_) * 100, t) for a, i, m, r_, t in zip(kic["account"], kic["start_date"],
                                                                           kic["maturity_date"], kic["int_rate"],
                                                                           kic["term_months"])}
    ok(all(k_ in kip_key for k_ in core_key.values()), "SF23 a core certificate matches no register certificate")
    logged = dict(zip(mig["new_account"], mig["cert_no"]))
    ok(all(kip_key[core_key[a]] == c for a, c in logged.items() if a in core_key),
       "SF23 a logged migration matches another certificate")
    unlogged = [a for a in core_key if a not in logged]
    ok(len(unlogged) > 20, "SF23 too few certificates moved by hand (%d)" % len(unlogged))
    cap = [kic.set_index("account").loc[a, "principal"] - kip.loc[kip_key[core_key[a]], "principal"]
           for a in core_key]
    ok(min(cap) >= -0.005 and sum(x > 0.005 for x in cap) > 0.9 * len(cap),
       "SF23 the core's principal is not the register's with interest added")
    kq1 = A["kip"][(A["kip"]["maturity_date"] >= "2027-01-01") & (A["kip"]["maturity_date"] <= "2027-03-31")]
    ok((~kq1["cert_no"].isin(set(mig["cert_no"]))).sum() > 20, "ask B no certificate left on the platform")
    ok("certificate register at close of business 30 June 2026" in open(p(W.F_NOTES), encoding="utf-8").read() and
       "held in the core at the cut" in open(p(W.F_NOTES), encoding="utf-8").read(), "SF23 the two dates are filed")

    # ------------------------------------------------------------------ separation and distractor deletion
    s1 = golden_on_copy(target, ASK_FILES)
    ok(abs(s1["total"] - g) < 1e-9 and all(abs(s1["months"][k] - gm[k]) < 1e-9 for k in (1, 2, 3)),
       "R2: the call moves without the ask files")
    s2 = golden_on_copy(target, list(W.DISTRACTORS))
    ok(abs(s2["total"] - g) < 1e-9 and s2["a"] == ga and s2["b"] == gb, "a distractor moves a figure")

    # ------------------------------------------------------------------ realism sweep
    stamp = W.EXPORT_STAMP.timestamp()
    ok(all(abs(os.path.getmtime(p(f)) - stamp) < 1 for f in files), "an mtime is off the export stamp")
    for f in files:
        if f.endswith((".csv", ".txt", ".eml")):
            txt = open(p(f), encoding="utf-8", errors="replace").read()
            ok("\u2014" not in txt and "\u2013" not in txt, "a dash in %s" % f)
    for f in [W.F_SOW, W.F_PROPOSAL] + [W.brief_name(q) for q in W.PAST + [W.FWD]]:
        ok("\u2014" not in pdf_text(p(f)), "an em dash in %s" % f)
    ok("\u2014" not in proc, "an em dash in the procedure")
    import email
    from email import policy as _pol
    msg = email.message_from_bytes(open(p(W.F_THREAD), "rb").read(), policy=_pol.default)
    eml = " ".join(str(msg[h]) for h in ("From", "To", "Cc")) + " " + msg.get_body().get_content()
    for who in ("product", "vendor", "head"):
        ok(W.PEOPLE[who] in eml, "the thread is missing %s" % who)
    ok(dt.date(2026, 11, 2).weekday() == 0 and dt.date(2026, 11, 4).weekday() == 2 and
       dt.date(2026, 11, 17).weekday() == 1 and dt.date(2026, 11, 20).weekday() == 4, "the thread's days of the week")
    ok("approved by the Deposits Committee" in proc and "Deposits Committee signs off" in eml, "the forum is filed")
    for q in W.PAST + [W.FWD]:
        n_ = W.FWD_LIST_SIZE if q == W.FWD else int(listed[q])
        ok("{:,}".format(n_) in briefs[q], "brief %s does not carry its list size" % q)
        card = C.read_card(p(W.brief_name(q)))
        ok(card == {t: W.card(q, t) for t in W.TERMS}, "R2: brief %s card does not read back" % q)
    ok(len(set(F["principal"])) > 5000, "the list's principal is too uniform")
    ok(int(F["principal"].sum()) % 1000 != 0, "a round list total")
    import openpyxl
    ok("wholesale" in str(openpyxl.load_workbook(p(W.F_OUTLOOK)).active["A2"].value), "the outlook's scope line")
    golden_hours = {h250(g)} | {h250(v) for v in gm.values()}
    ok(not any("{:,}".format(x) in pdf_text(p(W.F_PROPOSAL)) for x in golden_hours), "the proposal states a golden hour")

    # ------------------------------------------------------------------ the goldens agree with figures.json
    wb = openpyxl.load_workbook(os.path.join(golden, GD.BOOK), data_only=True)
    ws = wb["Booking"]
    vals = {ws.cell(row=r, column=1).value: ws.cell(row=r, column=8).value for r in range(5, 9)}
    ok(vals["Quarter"] == h250(g), "workbook booking")
    for k, nm in GD.MONTHS.items():
        ok(vals["%s 2027" % nm] == h250(gm[k]), "workbook %s" % nm)
    ws2 = wb["Kept at 30 days"]
    for r, q in enumerate(W.PAST, 5):
        ok(ws2.cell(row=r, column=4).value == k1000(ga[q][1]) and ws2.cell(row=r, column=5).value == ga[q][0],
           "workbook ask A %s" % q)
    ws3 = wb["Maturing Q1 2027"]
    for r, k in enumerate((1, 2, 3), 5):
        ok(ws3.cell(row=r, column=2).value == k1000(gb[k]), "workbook ask B %d" % k)
    ok(ws3.cell(row=10, column=2).value == k1000(gb["off"]), "workbook ask B off the list")
    pm = c_["per_month"]
    talk = {k: (pm[k]["conv"] * W.MIN_CONVERSATION + pm[k]["ret"] * (W.MIN_RETENTION - W.MIN_CONVERSATION)) / 60.0
            / pm[k]["hours"] for k in (1, 2, 3)}
    ok(all(0.64 <= talk[k] < 0.70 for k in (1, 2, 3)), "the chart's title: talk shares %s" % talk)
    note = docx_text(os.path.join(golden, GD.NOTE))
    ok(("Book %s agent-hours" % figs["call"]["booking_hours"]) in note, "the note does not open with the booking")
    src_ = open(__file__).read()
    for sf in range(1, 26):
        ok(("SF%d " % sf) in src_ or ("SF%d:" % sf) in src_ or ("SF%d/" % sf) in src_, "SF%d not asserted" % sf)
    print("checks: %d assertions passed (golden %.1f hours, months %s; family %d members; %d rivals)" % (
        N[0], g, {k: round(v, 1) for k, v in gm.items()}, len(fam), len(rv)))
    return N[0]
