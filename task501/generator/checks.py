"""task501 assertions over the built pack (target/), and figures.json for figures_check.py.

Every semantic fork row (SF1 to SF15), the ladder, the golden family, the back-tests, the ask's golden and stops,
the composed mishandlings, the separation of the ask from the call, the input gates, the distractors' deletion test,
the realism sweep and the documents' quoted sentences. Exit 1 on any failed assertion."""
import itertools
import json
import os
import re
import shutil
import sys
import tempfile
import zipfile
from datetime import date

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import solve as S
import world as W

T = S.T
A = []


def ok(cond, msg):
    A.append((bool(cond), msg))
    if not cond:
        print("ASSERT FAIL:", msg)


def edges(a):
    return (a - 25) * 1e6, a * 1e6


def inside(req, a, margin):
    lo, hi = edges(a)
    return req - lo >= margin * 1e6 and hi - req >= margin * 1e6


def dist_out(req, a):
    """How far a wrong cell's requirement sits from the golden bin (positive when outside)."""
    lo, hi = edges(a)
    if req <= lo:
        return (lo - req) / 1e6
    if req > hi:
        return (req - hi) / 1e6
    return -min(req - lo, hi - req) / 1e6


def doc_text(name):
    p = os.path.join(T, name)
    if name.endswith(".docx"):
        with zipfile.ZipFile(p) as z:
            x = z.read("word/document.xml").decode("utf-8")
        return re.sub(r"<[^>]+>", "", x)
    if name.endswith(".xlsx"):
        wb = __import__("openpyxl").load_workbook(p, read_only=True)
        out = []
        for ws in wb.worksheets:
            for row in ws.iter_rows(values_only=True):
                out.append(" ".join(str(c) for c in row if c is not None))
        return "\n".join(out)
    if name.endswith(".pdf"):
        from pypdf import PdfReader
        return "\n".join(pg.extract_text() for pg in PdfReader(p).pages)
    return open(p, encoding="utf-8").read()


def flat(s):
    return re.sub(r"\s+", " ", s)


def main():
    pk = S.Pack()
    fs = pk.funds()
    fig = {}

    # ------------------------------------------------------------------ the golden
    E, grp, per, tau = S.forecast(pk, fs, "golden", detail=True)
    req = S.requirement(E)
    amt = S.amount(E)
    ok(amt == 225, f"the golden amount is CHF 225 million (requirement {req / 1e6:.2f})")
    ok(inside(req, amt, 7.0), f"the golden requirement {req / 1e6:.2f} sits at least 7 million inside 200 to 225")
    ok(abs(E / 1e6 - round(E / 1e6)) > 0.05 and abs(req / 1e6 - round(req / 1e6)) > 0.05, "expected calls and requirement are not round millions")
    sh = pk.closed_shares(fs)
    v = np.array(list(sh.values()))
    ok(len(v) == 27, f"{len(v)} funds whose investment periods ended by the plan date")
    ok(v.min() > 0.90 and v.max() < 0.95, f"every closed fund drew {v.min():.4f} to {v.max():.4f} of commitment by its investment-period end")
    group = [d for d in fs if S.WIN[0] <= d["ip"] <= S.WIN[-1]]
    four = [d for d in group if d["code"] in W.DEADLINE_GROUP]
    ok(len(four) == 4, "the four slow funds' investment periods end in 2027")
    for d in four:
        share = S.called_to(d, S.PLAN_I) / d["C"]
        ok(0.45 < share < 0.66, f"{d['code']} drawn {share:.3f} at the plan date")
        ok(d["ip_date"] >= date(2027, 9, 1), f"{d['code']} investment period ends {d['ip_date']} (September to December 2027)")
    others_in_window = [d for d in group if d["code"] not in W.DEADLINE_GROUP]
    for d in others_in_window:
        ok(S.called_to(d, S.PLAN_I) / d["C"] > 0.83, f"{d['code']} (period ends {d['ip_date']}) is on schedule")
    # nothing behind schedule with a deadline in the first half of 2028 (its drawdown would start inside 2027)
    for d in fs:
        if S.PLAN_I + 13 <= d["ip"] <= S.PLAN_I + 18:
            ok(False, f"{d['code']} has an investment period ending {d['ip_date']}, inside the half-year after 2027")
    four_bal = sum(max(0.0, tau * d["C"] - S.called_to(d, S.PLAN_I)) for d in four)
    four_undrawn = sum(d["C"] - S.called_to(d, S.PLAN_I) for d in four)
    four_r1 = sum(S.ta(d, S.rates(fs), S.WIN, d["C"] - S.called_to(d, S.PLAN_I)) for d in four)

    # ------------------------------------------------------------------ the ladder
    lad = S.ladder(pk, fs)
    expect = {"R0": 200, "R1": 125, "R1-6": 125, "R1s": 150, "R1fc": 125, "R1b": 125, "R1m": 125, "R2-12": 150, "R2-6": 150, "R2-3": 150,
              "R2s-6": 150, "X1": 275, "R3own": 100, "X2": 175}
    for k, (label, e) in lad.items():
        a = S.amount(e)
        ok(a == expect[k], f"rung {k} ({label}) lands on CHF {a} million (expected {expect[k]}), requirement {S.requirement(e) / 1e6:.2f}")
        ok(dist_out(S.requirement(e), amt) >= 7.0, f"rung {k} at least 7 million outside the golden bin ({dist_out(S.requirement(e), amt):.1f})")
    ok(S.requirement(lad["R1"][1]) < S.requirement(lad["R2-6"][1]) < req < S.requirement(lad["X1"][1]), "the golden is bracketed: R1 < R2 < golden < X1")
    decisive_move = req - S.requirement(lad["R1"][1])
    reflex_moves = [S.requirement(lad[k][1]) - S.requirement(lad["R1"][1]) for k in ("R1s", "R1b", "R2-12", "R2-6", "R2-3")]
    ok(decisive_move > 1.5 * max(reflex_moves), f"the decisive move ({decisive_move / 1e6:.1f}) is the largest on the ladder (reflexes {max(reflex_moves) / 1e6:.1f})")
    ok(four_bal > 1.8 * four_r1, f"dominance: the four funds' balance {four_bal / 1e6:.1f} against the default's {four_r1 / 1e6:.1f}")
    bts = {}
    for y in (2024, 2025, 2026):
        fc, real = S.backtest(pk, fs, y)
        bts[y] = 100 * (fc / real - 1)
    ok(abs(bts[2025]) < 5 and abs(bts[2026]) < 5, f"the default back-tests within 5 per cent on 2025 and 2026 ({bts[2025]:+.1f}, {bts[2026]:+.1f})")

    # ------------------------------------------------------------------ the golden family (C3) on the filed estimation period
    # every member lands on the golden amount; each careful-solver choice at least 2 per cent of expected calls inside both edges
    # of the bin, the two weaker estimators inside it; every combination of the careful choices inside it
    LO_E, HI_E = (amt - 25 + 150) / 1.1 * 1e6, (amt + 150) / 1.1 * 1e6
    def cmargin(e):
        return min(e / LO_E - 1.0, 1.0 - e / HI_E)
    fam = S.golden_family(pk, fs)
    weak = S.golden_family(pk, fs, weak=True)[1:]
    for nm, e in fam:
        ok(S.amount(e) == amt, f"family member '{nm}' lands on CHF {S.amount(e)} million (requirement {S.requirement(e) / 1e6:.2f})")
        ok(cmargin(e) >= 0.02, f"family member '{nm}': expected calls {e / 1e6:.1f} at least 2 per cent inside {LO_E / 1e6:.1f} to {HI_E / 1e6:.1f} "
                               f"({100 * cmargin(e):.2f} per cent)")
    for nm, e in weak:
        ok(S.amount(e) == amt and cmargin(e) >= 0.010, f"weaker member '{nm}' lands on CHF {S.amount(e)} million ({100 * cmargin(e):.2f} per cent inside)")
    cross = S.family_cross(pk, fs)
    cross_e = [e for _, e in cross]
    ok(len(cross) == 384 and all(S.amount(e) == amt for e in cross_e),
       f"every one of the {len(cross)} combinations of the careful choices lands on CHF {amt} million ({min(cross_e) / 1e6:.1f} to {max(cross_e) / 1e6:.1f})")
    cross_w = S.family_cross(pk, fs, weak=True)
    cross_w_out = sum(1 for _, e in cross_w if S.amount(e) != amt)
    canon_k = (12, "first_call", False, "sum", "mean", "all", "band", "balance")
    off = [k for k, e in cross_w if S.amount(e) != amt]
    ok(all(sum(1 for a, b in zip(k, canon_k) if a != b) >= 3 and (k[3] == "mean" or k[6] == "zero") for k in off),
       f"the {len(off)} combinations off the golden amount each take three or more departures, one of them a weaker estimator")
    # the mean of fund-month rates does not reproduce the record's own calls; the ratio of sums does
    def in_sample(weight):
        Rw = S.rates(fs, weight=weight)
        pred = act = 0.0
        for d in fs:
            cum = 0.0
            for i in range(d["first"], S.PLAN_I + 1):
                unf = d["C"] - cum
                c = d["calls"].get(i, 0.0)
                if unf > 1.0:
                    pred += Rw[(i - d["first"]) // 12] * unf
                    act += c
                cum += c
        return pred / act
    ins_sum, ins_mean = in_sample("sum"), in_sample("mean")
    ok(abs(ins_sum - 1.0) < 1e-9 and ins_mean > 1.03, f"in the record the ratio of sums reproduces the calls exactly; the mean of fund-month rates "
                                                       f"gives {100 * (ins_mean - 1):.1f} per cent more")
    fam_lo = min(S.requirement(e) for _, e in fam) / 1e6
    fam_hi = max(S.requirement(e) for _, e in fam) / 1e6
    # SF17 the estimation period: the whole record, as s.5.2 files it; a recent window is another reading of the record
    wins = S.window_variants(pk, fs)
    win_amt = {y: S.amount(e) for y, e in wins}
    ok(win_amt == {2019: amt, 2021: amt, 2022: amt, 2023: amt, 2024: amt - 25, 2025: amt},
       f"SF17: recent-window fits give {win_amt} (the fork row's calls under the alternative)")
    ok("over the programme's whole history since its first commitment in 2015" in flat(doc_text("richtlinie_liquiditaet_privatmarkt_RL-PM-05.docx")),
       "SF17: s.5.2 files the estimation period (the programme's whole history since 2015)")
    ok(min(pk.calls["value_date"]).year == 2015 and min(pk.reg["first_close"]).year == 2015, "SF17: the record and the register start in 2015")
    # the drawn share at the deadline counted by notice date converges
    sh_n = pk.closed_shares(fs, by="notice_date")
    ok(max(abs(sh_n[k] - sh[k]) for k in sh) < 1e-9, "axis 9: no call is noticed inside an investment period and due after it")
    ok(all(abs(S.called_to(d, d["ip"]) / d["C"] - sh[d["code"]]) < 1e-9 for d in fs if d["code"] in sh),
       "axis 9: the drawn share at the period end is the same counted to the day or to the month")

    # ------------------------------------------------------------------ semantic fork rows
    lg = pk.ledger
    calls_all = lg[lg["notice_type"] == "CAPITAL_CALL"]
    # SF1 the menu
    ok(S.requirement(E) / 1e6 not in [float(a) for a in S.MENU], "SF1: the requirement is not itself a menu amount")
    # SF2 the calendar year against the twelve months from the election (same deadline group, January to January)
    ok(all(d["ip_date"] <= date(2027, 12, 31) for d in four), "SF2: the four deadlines fall inside 2027 either way")
    # SF3 the expected calls, SF9 the margin, SF8 the reserve
    ok(S.amount(E, margin=0.0) != amt, f"SF9: without the margin the amount is CHF {S.amount(E, margin=0.0)} million")
    ok(S.amount(E, reserve=0.0) != amt, f"SF8: without the reserve the amount is CHF {S.amount(E, reserve=0.0)} million")
    # SF4 investments only
    inv_only = pk.calls[pk.calls["line_type"] == "INVESTMENT"]
    pk_inv = S.Pack()
    pk_inv.calls = inv_only
    E_inv = S.forecast(pk_inv, pk_inv.funds(), "golden")[0]
    ok(S.amount(E_inv) != amt, f"SF4: investments only gives CHF {S.amount(E_inv)} million")
    # SF5 notices of 2026 due in 2027
    pend = calls_all[(calls_all["notice_date"] <= S.PLAN_DATE) & (calls_all["value_date"] > S.PLAN_DATE)]
    ok(len(pend) == 0, "SF5: no notice issued by 31 December 2026 is due in 2027")
    # SF6 every registered fund has called; none signed after the plan date
    ok(all(d["first"] is not None and d["first"] <= S.PLAN_I for d in fs), "SF6: every registered commitment has called by the plan date")
    ok(all(r <= S.PLAN_DATE for r in pk.reg["first_close"]), "SF6: no registered commitment closes after the plan date")
    # SF10 distributions netted
    d26 = lg[(lg["notice_type"] == "DISTRIBUTION") & (lg["status"] == "ISSUED") & (lg["line_type"] != "IN_KIND") & (lg["value_date"].apply(lambda d: d.year) == 2026)]
    net = E - sum(a * pk.rate(S.PLAN_DATE, c) for a, c in zip(d26["amount"], d26["currency"]))
    ok(S.amount(max(net, 0.0)) != amt, "SF10: netting a year of distributions moves the amount")
    # SF11 withdrawn notices counted
    pk_w = S.Pack()
    pk_w.calls = calls_all
    E_w = S.forecast(pk_w, pk_w.funds(), "golden")[0]
    ok(S.amount(E_w) == amt, f"SF11: counting withdrawn notices too gives the same amount (requirement {S.requirement(E_w) / 1e6:.2f})")
    # SF12 nothing dated after the plan date
    ok(lg["notice_date"].max() <= S.PLAN_DATE, "SF12: no notice dated after 31 December 2026 in the extract")
    # SF13 calls dated by notice date
    E_nd = S.forecast(pk, pk.funds(by="notice_date"), "golden")[0]
    ok(S.amount(E_nd) == amt, f"SF13: dating calls by notice gives the same amount (requirement {S.requirement(E_nd) / 1e6:.2f})")
    # SF14 rounding the expected calls to the million first
    ok(S.amount(round(E / 1e6) * 1e6) == amt, "SF14: rounding the expected calls first gives the same amount")
    # SF15 the investment period counted from the final close instead of the register's date
    pk_f = S.Pack()
    for fid, r in pk_f.reg.iterrows():
        fc = r["final_close"] if not pd.isna(r["final_close"]) else r["first_close"]
        pk_f.reg.loc[fid, "investment_period_end"] = (pd.Timestamp(fc) + pd.DateOffset(months=60 if r["strategy"] != "PC" else 48)).date()
    E_f = S.forecast(pk_f, pk_f.funds(), "golden")[0]
    ok(S.amount(E_f) != amt, f"SF15: periods counted from the final close give CHF {S.amount(E_f)} million (ruled out by the register's dates)")
    sf_calls = dict(SF4=S.amount(E_inv), SF8=S.amount(E, reserve=0.0), SF9=S.amount(E, margin=0.0), SF15=S.amount(E_f))
    # SF7 the plan-date rate is the only rate for 2027 the pack can supply
    fx_days = sorted(pk.fx)
    ok(fx_days[-1] == S.PLAN_DATE and S.PLAN_DATE in pk.fx, "SF7: the rate file ends on the plan date, which carries a rate; no 2027 rate exists")
    # SF16 the fees: a flat share of the amount for the availability period, the amount fixed for the whole period
    ok("for the whole availability period" in flat(doc_text("term_sheet_lindenhof_standby_2027.pdf")), "SF16: the elected amount runs for the whole period")

    # ------------------------------------------------------------------ clean-data and lens-swap tests (determinism-check section 4)
    raw = pd.read_csv(os.path.join(T, "kapitalabrufe_ausschuettungen_2015-2026.csv"), dtype=str, keep_default_na=False)
    tmpc = tempfile.mkdtemp()
    for f_ in os.listdir(T):
        shutil.copy(os.path.join(T, f_), tmpc)
    clean = raw[(raw["status"] == "ISSUED") & ~raw["notice_id"].str.startswith("PM")].copy()
    clean["currency"] = clean["currency"].str.upper()
    clean["description"] = clean["description"].str.strip()
    clean.to_csv(os.path.join(tmpc, "kapitalabrufe_ausschuettungen_2015-2026.csv"), index=False)
    pk_c = S.Pack(root=tmpc)
    fs_c = pk_c.funds()
    E_c = S.forecast(pk_c, fs_c, "golden")[0]
    R1_c = S.forecast(pk_c, fs_c, "ta")[0]
    ok(abs(E_c - E) < 1e-6 and S.amount(R1_c) == S.amount(lad["R1"][1]) and abs(R1_c - lad["R1"][1]) < 1e-6,
       "clean-data test: with the withdrawn notices, the custodian's advices and the keying noise removed, the golden and the default are unchanged")
    shutil.rmtree(tmpc)
    _, _, per_d, _ = S.forecast(pk, fs, "ta", detail=True)
    gap = {c: per[c] - per_d[c] for c in per}
    ok(sum(gap[c] for c in W.DEADLINE_GROUP) > 0.9 * sum(gap.values()) and all(abs(gap[d["code"]]) < 1e-6 for d in fs if d not in group),
       "lens-swap test: the default and the golden forecast the same funds over the same year; they part only on the funds whose periods end in 2027, "
       f"the four carrying {100 * sum(gap[c] for c in W.DEADLINE_GROUP) / sum(gap.values()):.0f} per cent of the difference")
    # closure: the cap never binds (every band rate under one), row order does not enter, no period ends near the plan date
    ok(max(S.rates(fs).values()) < 1.0, "axis 13: every band rate is under one, so the cap at the unfunded commitment never binds")
    pk_sh = S.Pack()
    pk_sh.calls = pk_sh.calls.sample(frac=1.0, random_state=7)
    ok(abs(S.forecast(pk_sh, pk_sh.funds(), "golden")[0] - E) < 1e-3, "axis 14: the ledger's row order does not enter")
    ok(not any(date(2026, 12, 1) <= d["ip_date"] <= date(2027, 1, 6) for d in fs),
       "axis 12: no investment period ends between 1 December 2026 and the extract, so the closed set is the same at the plan date and the run")

    # ------------------------------------------------------------------ the term sheet's covenants never bind (reader's reading)
    # the programme NAV on every reading of the NAV register: the statements for 30 June or 30 September 2026 as received, or each
    # fund's latest statement, at the booked francs or at the plan-date rate
    navr = pd.read_csv(os.path.join(T, "nav_register_quartal.csv"))
    nav_readings = {}
    for lab, sub in [("30 June 2026", navr[navr["period_end"] == "2026-06-30"]), ("30 September 2026 as received", navr[navr["period_end"] == "2026-09-30"]),
                     ("each fund's latest statement", navr.sort_values("period_end").groupby("fund_id").tail(1))]:
        nav_readings[lab + ", booked"] = float(sub["nav_chf_booked"].sum())
        nav_readings[lab + ", plan-date rate"] = float(sum(a * pk.rate(S.PLAN_DATE, c.upper()) for a, c in zip(sub["nav_fund_ccy"], sub["currency"])))
    nav_min = min(nav_readings.values())
    ok(nav_min >= 900e6, f"SF18 covenant: the programme NAV is at least CHF 900 million on every reading ({nav_min / 1e6:.0f})")
    ok(0.25 * nav_min >= (amt + 25) * 1e6, f"SF18 covenant: 25 per cent of the smallest NAV reading ({0.25 * nav_min / 1e6:.0f}) is above CHF {amt + 25} million, "
                                          "so the covenant caps neither the golden amount nor the next amount up")
    # R0's basis: the 2026 calls at the plan-date rate with the franc commitments at par (s.4), and at each value date's rate
    c26 = pk.calls[pk.calls["value_date"].apply(lambda d: d.year == 2026)]
    r0_plan = sum(a * pk.rate(S.PLAN_DATE, c) for a, c in zip(c26["amount"], c26["currency"]))
    r0_vd = sum(a * pk.rate(d, c) for a, c, d in zip(c26["amount"], c26["currency"], c26["value_date"]))
    r0_nochf = sum(a * pk.rate(S.PLAN_DATE, c) for a, c in zip(c26["amount"], c26["currency"]) if c != "CHF")
    ok(abs(r0_plan - lad["R0"][1]) < 1.0, f"R0: the 2026 calls at the plan-date rate, francs at par, are CHF {r0_plan / 1e6:.1f} million")
    ok(S.amount(r0_vd) == S.amount(r0_plan) == S.amount(r0_nochf) == amt - 25,
       f"R0 lands on CHF {amt - 25} million at the plan-date rate ({r0_plan / 1e6:.1f}), at value-date rates ({r0_vd / 1e6:.1f}) and with the franc "
       f"commitments left out ({r0_nochf / 1e6:.1f})")

    # ------------------------------------------------------------------ quoted sentences at authority
    directive = flat(doc_text("richtlinie_liquiditaet_privatmarkt_RL-PM-05.docx"))
    for q in ["the smallest facility amount offered by the lender", "Facility year: the calendar year for which the facility is elected",
              "expected capital calls of the facility year plus one tenth of them", "for investments, management fees or partnership expenses",
              "A call is in the facility year when its value date is, whenever it was noticed",
              "on every commitment in the programme register at the plan date",
              "Commitments signed after the plan date are funded from the commitment budget and are not in the plan",
              "translated at the reference rate of the plan date", "they are not credited against calls",
              "Plan date: 31 December of the year before the facility year",
              "Unfunded commitment: the commitment less the capital calls with a value date on or before that day",
              "a reserve of CHF 150 million"]:
        ok(q in directive, f"directive carries: {q}")
    minutes = flat(doc_text("stiftungsrat_protokoll_auszug_2026-09-24.pdf"))
    ok("is repaid from the October transfer" in minutes and "repaid on" not in minutes,
       "the minutes of 24 September report no repayment date after the sitting")
    notes = flat(doc_text("feldbeschrieb_privatmarkt_extrakt.md"))
    for q in ["A withdrawn notice has no cash effect; the manager reissues it under a new number", "the clerks are not consistent about case"]:
        ok(q in notes, f"field notes carry: {q}")
    reg_txt = flat(doc_text("fondsregister_2026-12-31.xlsx"))
    ok("as stated in the limited partnership agreement; no extension has been requested" in reg_txt, "register notes carry the investment-period sentence")
    ts = flat(doc_text("term_sheet_lindenhof_standby_2027.pdf"))
    ok("One of CHF 50, 75, 100" in ts and "375 or 400 million" in ts, "the term sheet lists the menu")
    ok("0.30 per cent of the facility amount for the availability period, drawn or undrawn" in ts and "0.15 per cent flat on the facility amount" in ts,
       "the term sheet states the fees")
    ok("per annum" not in ts.split("Interest on drawings")[0] and "100 million" not in ts, "no day count or interim amount on the fees")
    # no document names the decisive step
    words = ["catch-up", "catch up", "behind schedule", "drawdown", "draw down", "deadline", "pacing", "Takahashi", "terminal", "balance to",
             "92 per cent", "parallel run", "keyed twice", "duplicate", "in parallel"]
    for name in os.listdir(T):
        if name.endswith((".docx", ".pdf", ".txt", ".md", ".json")) or name == "fondsregister_2026-12-31.xlsx":
            txt = flat(doc_text(name)).lower()
            hit = [w for w in words if w.lower() in txt]
            ok(not hit, f"{name} names none of the decisive or device words ({hit})")

    # ------------------------------------------------------------------ the ask
    g = S.ask_golden(pk)
    G = S.grid_figures(g)
    keys = [k for k in G if k != "top_strategy"]
    for k in keys:
        frac = abs(G[k] - np.floor(G[k]) - 0.5)
        ok(frac >= 0.02, f"ask figure {k} = {G[k]:.3f} thousand sits clear of a rounding edge ({frac:.3f})")
    ok(G["top_strategy"] == "BO", f"the golden's top strategy is {G['top_strategy']}")
    # one rounding path: every year total and every quarter total equals the sum of its rounded cells
    for s_ in S.STRATS:
        ok(round(G[f"{s_}_year"]) == sum(round(G[f"{s_}_Q{q}"]) for q in (1, 2, 3, 4)), f"{s_}: the rounded year equals the sum of the rounded quarters")
    for q in (1, 2, 3, 4):
        ok(round(G[f"total_Q{q}"]) == sum(round(G[f"{s_}_Q{q}"]) for s_ in S.STRATS), f"Q{q}: the rounded total equals the sum of the rounded cells")
    ok(round(sum(G[f"total_Q{q}"] for q in (1, 2, 3, 4))) == sum(round(G[f"{s_}_year"]) for s_ in S.STRATS)
       == sum(round(G[f"total_Q{q}"]) for q in (1, 2, 3, 4)), "the year's grand total agrees on every rounding path")
    stops = {"s1 cracker (ledger, value date)": S.ask_ledger(pk), "s2 deduplicated keeping the clerk's notice": S.ask_ledger(pk, keep="clerk"),
             "s3 deduplicated keeping the feed's advice": S.ask_ledger(pk, keep="feed"), "s4 custodian francs": S.ask_custody_chf(pk),
             "s5 lazy": S.ask_ledger(pk, cash_only=False, issued_only=False)}
    stop_min = {}
    for nm, gg in stops.items():
        F = S.grid_figures(gg)
        diffs = [abs(F[k] - G[k]) for k in keys]
        stop_min[nm] = min(diffs)
        ok(min(diffs) >= 1.0, f"stop {nm} misses all 20 figures and the 4 labels (smallest miss CHF {min(diffs):.1f} thousand)")
    s1 = S.grid_figures(stops["s1 cracker (ledger, value date)"])
    ok(s1["top_strategy"] != G["top_strategy"], f"the cracker's chart title names {s1['top_strategy']}, the golden's {G['top_strategy']}")
    q1to3 = [abs(s1[f"{s}_Q{q}"] - G[f"{s}_Q{q}"]) for s in S.STRATS for q in (1, 2, 3)]
    q4 = [abs(s1[f"{s}_Q4"] - G[f"{s}_Q4"]) for s in S.STRATS]
    ok(min(q1to3) >= 100.0, f"s1 misses every Q1 to Q3 cell by at least CHF 100 thousand ({min(q1to3):.0f})")
    ok(min(q4) >= 20.0, f"s1 misses every Q4 cell by at least CHF 20 thousand ({min(q4):.0f})")
    # composed mishandlings: P1 (no dedupe), h1 (stated dates), h2 (in specie kept), h3 (withdrawn kept), h4 (dealing rates)
    kept_by_combo = {}
    for combo in itertools.product([False, True], repeat=5):
        if not any(combo):
            continue
        p1, h1, h2, h3, h4 = combo
        F = S.grid_figures(S.ask_variant(pk, dedupe=not p1, dates="stated" if h1 else "arrival", inkind=h2, withdrawn=h3,
                                         chf="dealing" if h4 else "reference"))
        kept_keys = [k for k in keys if abs(F[k] - G[k]) < 0.5]
        kept = len(kept_keys) + (F["top_strategy"] == G["top_strategy"])
        name = "+".join(n for n, on in zip(("P1", "h1", "h2", "h3", "h4"), combo) if on)
        kept_by_combo[name] = kept
        if h1:
            ok(not kept_keys, f"mishandling {name} keeps none of the 24 figures ({kept_keys})")
        elif p1:
            # the parallel run ended in September: a path that dates by arrival but keeps both records is right in Q4 only
            ok(all(k.endswith("Q4") for k in kept_keys) and kept <= 5, f"mishandling {name} keeps only the Q4 cells ({kept_keys}, title kept: {kept - len(kept_keys)})")
        elif h4:
            ok(kept <= 6, f"mishandling {name} keeps at most 6 of the 25 ask items ({kept})")
        else:
            # a path that takes its population from the custodian's credits cannot keep the in-specie line or the withdrawn
            # notice (neither has a credit): these handlings matter on the ledger's dates only, where h1 already misses all
            ok(kept == 25, f"handling {name} is inert on the credit path ({kept})")
    ok(abs(S.grid_figures(S.ask_variant(pk))["BO_year"] - G["BO_year"]) < 1e-6, "the variant machinery reproduces the golden")
    # the reader's booking-date reading (the field notes define Valuta as the day credited): the title holds under it
    cu_b = pk.custody[(pk.custody["Buchungstext"] == "Gutschrift Ausschuettung")]
    lg_i = pk.dists[(pk.dists["status"] == "ISSUED") & (pk.dists["line_type"] != "IN_KIND")]
    tot_n, fund_n = lg_i.groupby("notice_id")["amount"].sum().to_dict(), lg_i.groupby("notice_id")["fund_id"].first().to_dict()
    gb = S._grid()
    for r in cu_b.itertuples():
        if r.Buchungsdatum.year != 2026:
            continue
        kk = [x for x in (r.Transaktionsreferenz, r.Referenz.split(" ")[0]) if x in tot_n][0]
        fid = fund_n[kk]
        gb[pk.reg.loc[fid, "strategy"]][S.quarter(r.Buchungsdatum)] += tot_n[kk] * pk.rate(r.Valuta, pk.reg.loc[fid, "currency"])
    ok(S.grid_figures(gb)["top_strategy"] == G["top_strategy"], "the booking-date reading keeps the chart's title")
    _, rows = S.ask_golden(pk, detail=True)
    ok(sum(1 for r in rows if r[7] == 2) >= 20, f"{sum(1 for r in rows if r[7] == 2)} credits of 2026 carried twice in the ledger (P1)")
    dup_q = {}
    for r in rows:
        if r[7] == 2:
            s_ = pk.reg.loc[r[1], "strategy"]
            dup_q.setdefault(s_, set()).add(S.quarter(r[0]))
    for s_ in S.STRATS:
        ok({1, 2, 3} <= dup_q.get(s_, set()) or len(dup_q.get(s_, set())) >= 2, f"P1 reaches {s_} in quarters {sorted(dup_q.get(s_, set()))}")

    # ------------------------------------------------------------------ separation of the ask from the call
    pk_s = S.Pack()
    pk_s.dists = pk_s.dists.iloc[0:0]
    pk_s.custody = pk_s.custody.iloc[0:0]
    pk_s.reg["strategy"] = "BO"
    E_s = S.forecast(pk_s, pk_s.funds(), "golden")[0]
    ok(abs(E_s - E) < 1e-6, "the call is unchanged with the distribution rows, the custodian statement and the strategy column removed")
    feed_calls = lg[(lg["notice_type"] == "CAPITAL_CALL") & (lg["notice_id"].str.startswith("PM"))]
    ok(len(feed_calls) == 0, "the custodian feed loaded no capital-call rows")

    # ------------------------------------------------------------------ distractors: deletion test
    meta = json.load(open(os.path.join(os.path.dirname(HERE), "metadata.json")))
    distractors = [os.path.basename(p) for p in meta["distractor_files"]]
    ok(len(distractors) >= 2, f"{len(distractors)} distractors declared")
    tmp = tempfile.mkdtemp()
    for f in os.listdir(T):
        if f not in distractors:
            shutil.copy(os.path.join(T, f), tmp)
    pk_d = S.Pack(root=tmp)
    E_d = S.forecast(pk_d, pk_d.funds(), "golden")[0]
    G_d = S.grid_figures(S.ask_golden(pk_d))
    ok(abs(E_d - E) < 1e-6 and max(abs(G_d[k] - G[k]) for k in keys) < 1e-9, "the golden and the ask are unchanged with every distractor deleted")
    shutil.rmtree(tmp)

    # ------------------------------------------------------------------ H9: the pack's registers name every shipped file
    man = json.load(open(os.path.join(T, "extraktprotokoll_PKW-PM-2026-12-31.json"), encoding="utf-8"))
    shipped = set(os.listdir(T))
    ok({e["file"] for e in man["files"]} == shipped - {"extraktprotokoll_PKW-PM-2026-12-31.json"}, "the manifest lists every other shipped file")
    fn = open(os.path.join(T, "feldbeschrieb_privatmarkt_extrakt.md"), encoding="utf-8").read()
    ok(all(f in fn for f in shipped - {"feldbeschrieb_privatmarkt_extrakt.md"}), "the field notes name every other shipped file")
    ok("the day the amount was credited to or debited from the account" in flat(fn), "the field notes say what Valuta is")
    fxd = pd.read_csv(os.path.join(T, "fx_referenzkurse_tagesende.csv"), usecols=["rate_date"])["rate_date"]
    first = date.fromisoformat(fxd.min())
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    ok(f"{first.day} {months[first.month - 1]} {first.year}" in flat(fn), f"the field notes give the rate file's first day ({first})")

    # ------------------------------------------------------------------ input gates and realism
    files = sorted(f for f in os.listdir(T) if not f.startswith("."))
    ok(len(files) >= 10, f"{len(files)} files in the pack")
    ok(len({f.rsplit('.', 1)[-1] for f in files}) >= 3, f"{len({f.rsplit('.', 1)[-1] for f in files})} formats")
    big = max(sum(1 for _ in open(os.path.join(T, f), encoding="utf-8")) - 1 for f in files if f.endswith(".csv"))
    ok(big >= 25000, f"the largest file has {big} rows")
    ok(not any(re.search(r"distractor|answer|golden|stump|trap|decoy", f, re.I) for f in files), "no file name broadcasts a role")
    quarter_vals = [round(G[f"{s}_Q{q}"]) for s in S.STRATS for q in (1, 2, 3, 4)]
    ok(len(set(quarter_vals)) == len(quarter_vals), "no two ask cells are equal")
    ok(all(v % 100 != 0 for v in quarter_vals), "no ask cell is a round hundred thousand")
    ok(len({round(sum(d["calls"].get(i, 0.0) for d in fs)) for i in range(S.PLAN_I - 23, S.PLAN_I + 1)}) == 24, "no two months of programme calls are equal")
    people = list(W.PEOPLE.values())
    for f in files:
        if f.endswith((".pdf", ".docx", ".txt", ".md")):
            txt = doc_text(f)
            for nm in re.findall(r"\b[A-Z][a-zé]+ [A-Z][a-zü]+(?:mann|sist|ess|tter|rti)\b", txt):
                ok(nm in people, f"{f}: person {nm} is a drawn persona")

    # ------------------------------------------------------------------ figures.json
    fees = {a: a * 1e6 * (W.COMMIT_FEE + W.ARRANGE_FEE) for a in (amt, amt - 25)}
    four_detail = {d["code"]: dict(drawn_share=round(100 * S.called_to(d, S.PLAN_I) / d["C"], 1), ip_end=str(d["ip_date"]),
                                   undrawn_chf_k=round((d["C"] - S.called_to(d, S.PLAN_I)) / 1000.0),
                                   balance_chf_k=round(max(0.0, tau * d["C"] - S.called_to(d, S.PLAN_I)) / 1000.0),
                                   calls_2027_chf_m=round(per[d["code"]] / 1e6, 1), calls_2027_chf_k=round(per[d["code"]] / 1000.0)) for d in four}
    four_2027 = sum(per[d["code"]] for d in four)
    six = [d for d in group if d["code"] not in W.DEADLINE_GROUP]
    six_2027 = sum(per[d["code"]] for d in six)
    slow = {d["code"]: dict(ip_end=str(d["ip_date"]), year_before_pct=round(100 * S.called_to(d, d["ip"] - 12) / d["C"], 1),
                            at_end_pct=round(100 * sh[d["code"]], 1)) for d in fs if d["code"] in sh and S.called_to(d, d["ip"] - 12) / d["C"] < 0.75}
    ok(len(slow) == 5 and all(v["at_end_pct"] > 91.5 for v in slow.values()), f"five closed funds were under 75 per cent drawn a year before their deadline: {slow}")
    fig.update({
        "call_amount_chf_m": amt, "next_amount_down_chf_m": amt - 25,
        "fees_at_amount_chf": round(fees[amt]), "fees_at_next_down_chf": round(fees[amt - 25]),
        "commitment_fee_at_amount": round(amt * 1e6 * W.COMMIT_FEE), "arrangement_fee_at_amount": round(amt * 1e6 * W.ARRANGE_FEE),
        "commitment_fee_next_down": round((amt - 25) * 1e6 * W.COMMIT_FEE), "arrangement_fee_next_down": round((amt - 25) * 1e6 * W.ARRANGE_FEE),
        "expected_calls_chf_m": round(E / 1e6, 1), "requirement_chf_m": round(req / 1e6, 1), "reserve_chf_m": 150, "margin_share": 0.1,
        "expected_calls_plus_tenth_chf_m": round(1.1 * E / 1e6, 1),
        "four_funds": four_detail, "four_undrawn_chf_m": round(four_undrawn / 1e6, 1), "four_balance_chf_m": round(four_bal / 1e6, 1),
        "four_default_chf_m": round(four_r1 / 1e6, 1), "four_2027_chf_m": round(four_2027 / 1e6, 1),
        "others_2027_chf_m": round((E - four_2027) / 1e6, 1), "funds_in_register": len(fs),
        "six_2027_chf_m": round(six_2027 / 1e6, 1), "six_undrawn_chf_m": {d["code"]: round((d["C"] - S.called_to(d, S.PLAN_I)) / 1e6, 1) for d in six},
        "six_drawn_range_pct": [round(100 * min(S.called_to(d, S.PLAN_I) / d["C"] for d in six), 1),
                                round(100 * max(S.called_to(d, S.PLAN_I) / d["C"] for d in six), 1)],
        "four_drawn_range_pct": [round(100 * min(S.called_to(d, S.PLAN_I) / d["C"] for d in four), 1),
                                 round(100 * max(S.called_to(d, S.PLAN_I) / d["C"] for d in four), 1)],
        "in_specie_2026": [f"{r['fund_code']} {r['notice_id']}" for r in lg[(lg["line_type"] == "IN_KIND")].to_dict("records")],
        "withdrawn_distributions_2026": [r["notice_id"] for r in lg[(lg["notice_type"] == "DISTRIBUTION") & (lg["status"] == "CANCELLED")
                                                                    & (lg["value_date"] >= date(2026, 1, 1))].drop_duplicates("notice_id").to_dict("records")], "rest_2027_chf_m": round((E - four_2027 - six_2027) / 1e6, 1),
        "rest_count": len(fs) - len(group), "six_detail": {d["code"]: dict(ip_end=str(d["ip_date"]), drawn_share=round(100 * S.called_to(d, S.PLAN_I) / d["C"], 1),
                                                                           calls_2027_chf_m=round(per[d["code"]] / 1e6, 1), calls_2027_chf_k=round(per[d["code"]] / 1000.0),
                                                                           undrawn_chf_k=round((d["C"] - S.called_to(d, S.PLAN_I)) / 1000.0)) for d in six},
        "slow_starters": slow,
        "closed_others_year_before_min_pct": round(100 * min(S.called_to(d, d["ip"] - 12) / d["C"] for d in fs if d["code"] in sh and d["code"] not in slow), 1), "shortfall_next_down_chf_m": round(req / 1e6 - (amt - 25), 1),
        "fee_difference_chf": round(fees[amt] - fees[amt - 25]),
        "commitment_fee_pct": round(100 * W.COMMIT_FEE, 2), "arrangement_fee_pct": round(100 * W.ARRANGE_FEE, 2),
        "slow_year_before_range_pct": [min(v["year_before_pct"] for v in slow.values()), max(v["year_before_pct"] for v in slow.values())], "group_2027_chf_m": round(grp / 1e6, 1), "group_count": len(group),
        "closed_funds": len(v), "closed_share_min_pct": round(100 * v.min(), 1), "closed_share_max_pct": round(100 * v.max(), 1),
        "closed_share_mean_pct": round(100 * tau, 1), "plan_date_rates": dict(USD=pk.rate(S.PLAN_DATE, "USD"), EUR=pk.rate(S.PLAN_DATE, "EUR")),
        "default_expected_calls_chf_m": round(lad["R1"][1] / 1e6, 1), "default_requirement_chf_m": round(S.requirement(lad["R1"][1]) / 1e6, 1),
        "default_amount_chf_m": S.amount(lad["R1"][1]),
        "ladder": {k: dict(label=l, expected_calls_chf_m=round(e / 1e6, 1), requirement_chf_m=round(S.requirement(e) / 1e6, 1), amount=S.amount(e))
                   for k, (l, e) in lad.items()},
        "family": {nm: dict(expected_calls_chf_m=round(e / 1e6, 1), requirement_chf_m=round(S.requirement(e) / 1e6, 1)) for nm, e in fam},
        "family_requirement_range_chf_m": [round(fam_lo, 1), round(fam_hi, 1)],
        "family_margin_pct": {nm: round(100 * cmargin(e), 2) for nm, e in fam},
        "family_weak": {nm: dict(expected_calls_chf_m=round(e / 1e6, 1), requirement_chf_m=round(S.requirement(e) / 1e6, 1),
                                 margin_pct=round(100 * cmargin(e), 2)) for nm, e in weak},
        "family_cross": dict(n=len(cross), lo_chf_m=round(min(cross_e) / 1e6, 1), hi_chf_m=round(max(cross_e) / 1e6, 1),
                             weak_n=len(cross_w), weak_off_amount=cross_w_out),
        "calls_bin_chf_m": [round(LO_E / 1e6, 1), round(HI_E / 1e6, 1)],
        "window_variants": {str(y): dict(expected_calls_chf_m=round(e / 1e6, 1), amount=S.amount(e)) for y, e in wins},
        "nav_readings_chf_m": {k: round(v / 1e6, 1) for k, v in nav_readings.items()},
        "programme_calls_2026_value_date_chf_m": round(r0_vd / 1e6, 1),
        "backtests_pct": {str(k): round(x, 1) for k, x in bts.items()},
        "sf_calls": sf_calls,
        "distributions_2026_chf_k": {k: round(G[k]) for k in keys}, "distributions_2026_exact": {k: G[k] for k in keys},
        "distributions_2026_total_chf_k": round(sum(G[f"total_Q{q}"] for q in (1, 2, 3, 4))),
        "top_strategy": W.STRATEGIES[G["top_strategy"]], "cracker_top_strategy": W.STRATEGIES[s1["top_strategy"]],
        "stops_smallest_miss_chf_k": {k: round(x, 1) for k, x in stop_min.items()},
        "mishandlings_items_kept_of_25": kept_by_combo,
        "programme_calls_2026_chf_m": round(lad["R0"][1] / 1e6, 1),
    })
    with open(os.path.join(HERE, "figures.json"), "w") as fh:
        json.dump(fig, fh, indent=1, default=str)
    nfail = sum(1 for c, _ in A if not c)
    print(f"checks: {len(A)} assertions, {nfail} failed")
    print(f"golden: CHF {amt} million, expected calls {E / 1e6:.1f}, requirement {req / 1e6:.1f}; family {fam_lo:.1f} to {fam_hi:.1f}; default {S.amount(lad['R1'][1])}")
    return nfail


if __name__ == "__main__":
    sys.exit(1 if main() else 0)
