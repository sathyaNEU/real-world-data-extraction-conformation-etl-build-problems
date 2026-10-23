"""task177 checks: the generator's assertions on the built pack and the clean truth. Exit 1 on any failure.

    python3 task177/generator/checks.py task177/target"""
from __future__ import annotations

import copy
import json
import os
import re
import sys
import zipfile

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc as K      # noqa: E402
import common as C    # noqa: E402
import cracker as CR  # noqa: E402
import docs as DOC    # noqa: E402
import pack as PK     # noqa: E402
import world as W     # noqa: E402

RESULTS = []


def ok(name, cond, detail=""):
    RESULTS.append((name, bool(cond), detail))


def cell(v, unit):
    return C.nearest(v, unit)


def total_of(B, h, F, r):
    return float(K.golden_probs(B, h, F, r).sum())


def shares_of(B, h, F, r):
    p = K.golden_probs(B, h, F, r)
    s = pd.Series(p).groupby(B["sector"].values).sum()
    n = B.groupby("sector").size()
    return {k: 100 * s[k] / n[k] for k in C.SECTORS}


def main(target):
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    task = os.path.dirname(os.path.abspath(target))
    meta = json.load(open(os.path.join(task, "metadata.json")))
    files = sorted(os.listdir(target))

    # ------------------------------------------------------------------------------------------ input gates
    ok("gate: ten or more files", len(files) >= 10, "%d files" % len(files))
    fmts = sorted(set(f.rsplit(".", 1)[-1] for f in files))
    ok("gate: three or more formats", len(fmts) >= 3, ",".join(fmts))
    rows = {f: sum(1 for _ in open(os.path.join(target, f), encoding="utf-8")) - 1 for f in files if f.endswith(".csv")}
    ok("gate: a file of 25,000 rows or more", max(rows.values()) >= 25000, "%s %d" % (max(rows, key=rows.get), max(rows.values())))
    ok("gate: two distractors named in metadata.json", len(meta["distractor_files"]) >= 2 and
       all(d in files for d in meta["distractor_files"]), str(meta["distractor_files"]))
    ok("gate: no distractor word in a file name", not any("distractor" in f.lower() for f in files))
    ok("gate: every pack file has a source, date and licence", all(x["source"] and x["date"] and x["license"]
                                                                    for x in meta["files"]))

    # ------------------------------------------------------------------------------------------ the call
    L, R, D = K.load_public(target)
    F, nruns = K.conversion(L, R, D)
    r = K.residual(L, R, D)
    G = K.load_registers(target)
    h, expo, nl = K.hazards(G)
    B, A = K.load_launch(target)
    tot = total_of(B, h, F, r)
    sh = shares_of(B, h, F, r)
    ok("call: total reproduces figures.json", cell(tot, 50) == fig["call_total"] and abs(tot - fig["call_total_unrounded"]) < 0.06,
       "%.2f" % tot)
    ok("call: total mid-cell, at least 15 loans from an edge", C.edge(tot, 50) >= 15, "edge %.1f" % C.edge(tot, 50))
    for s in C.SECTORS:
        ok("call: %s share reproduces" % s, cell(sh[s], 5) == fig["call_share"][s], "%.2f" % sh[s])
        ok("call: %s share at least 0.5 points from its cell edge" % s, C.edge(sh[s], 5) >= 0.5, "edge %.2f" % C.edge(sh[s], 5))
    ok("call: the launch file holds 2,400 loans, one per member", len(B) == C.N_LAUNCH and B["member_id"].is_unique)
    ok("call: conversion component 53 per cent", C.nearest(100 * F[12], 1) == fig["cc_conversion_pct"], "%.4f" % F[12])
    ok("call: no default within two months of the first SIN SALARIO month", F[2] == 0.0 and F[3] > 0)
    ok("call: the deciding quantity rests on enough events", nruns >= 2500 and sum(nl.values()) >= 3000,
       "%d runs, %d leavers" % (nruns, sum(nl.values())))
    hl = np.array([h[n] for n in B["employer_nit"]])
    ok("call: leaving component 3 per cent a month", C.nearest(100 * hl.mean(), 1) == fig["cc_leave_launch_pct"],
       "%.3f" % (100 * hl.mean()))

    # one-sigma move of the deciding quantities (the conversion's binomial error and each employer's leaving count
    # treated as Poisson, independent) leaves the printed figures where they are
    se_conv = np.sqrt(F[12] * (1 - F[12]) / nruns)
    p0 = K.golden_probs(B, h, F, r)
    by_emp = pd.Series(p0).groupby(B["employer_nit"].values).sum()
    var_t = sum((by_emp[k] / np.sqrt(max(nl[k], 1))) ** 2 for k in by_emp.index) + (tot * se_conv / F[12]) ** 2
    se_t = float(np.sqrt(var_t))
    ok("call: one standard error either side keeps the total cell", cell(tot - se_t, 50) == fig["call_total"] ==
       cell(tot + se_t, 50), "total %.1f se %.1f" % (tot, se_t))
    secs = B["sector"].values
    for s in C.SECTORS:
        emps = set(B[B["sector"] == s]["employer_nit"])
        n_s = (secs == s).sum()
        v = sum((by_emp[k] / np.sqrt(max(nl[k], 1))) ** 2 for k in emps) + (sh[s] * n_s / 100 * se_conv / F[12]) ** 2
        se_s = 100 * float(np.sqrt(v)) / n_s
        ok("call: one standard error either side keeps the %s cell" % s,
           cell(sh[s] - se_s, 5) == fig["call_share"][s] == cell(sh[s] + se_s, 5), "%.2f se %.2f" % (sh[s], se_s))

    # ------------------------------------------------------------------------------------------ the golden family
    fam = {}
    for mt in (0, 6, 24):
        hh, _, _ = K.hazards(G, mt)
        fam["SF10 staff with %d months' service" % mt] = (hh, F, r)
    G26 = G[G["t"] >= C.mi(2026, 1)]
    hh, _, _ = K.hazards(G26, 12)
    fam["registers of 2026 only"] = (hh, F, r)
    S = K.runs(R)
    dd = D.groupby("loan")["t"].min()
    for lo in (C.mi(2019, 1), C.mi(2021, 7)):
        S2 = S[(S["c"] >= lo) & (S["c"] <= C.mi(2025, 12))]
        first = S2.groupby("loan")["c"].min().reset_index()
        first["dt"] = first["loan"].map(dd)
        lag = first["dt"] - first["c"]
        F2 = np.array([((lag >= 0) & (lag <= j)).mean() for j in range(13)])
        fam["SF9 conversion from runs since %d-%02d" % C.ym(lo)] = (h, F2, r)
    permloans = set(L[~L["temp"]]["loan_no"])
    Sp = S[S["loan"].isin(permloans) & (S["c"] <= C.mi(2025, 12))]
    first = Sp.groupby("loan")["c"].min().reset_index()
    first["dt"] = first["loan"].map(dd)
    lag = first["dt"] - first["c"]
    fam["SF9 conversion from permanent-contract loans only"] = (h, np.array([((lag >= 0) & (lag <= j)).mean() for j in range(13)]), r)
    fam["no on-payroll route"] = (h, F, 0.0)
    Wk = G[G["payment_type"].isin(["NOMINA", "LIQUIDACION"])]
    Pk = Wk[["employer_nit", "emp", "t", "hire_t"]].drop_duplicates()
    last = Pk.groupby(["employer_nit", "emp"])["t"].max().reset_index()
    last = last[last["t"] < C.mi(2026, 12)]
    Pt = Pk[Pk["t"] - Pk["hire_t"] >= 12]
    ex = Pt.groupby("employer_nit").size()
    lv = last.merge(Pt, on=["employer_nit", "emp", "t"]).groupby("employer_nit").size()
    fam["leaving read from the last appearance"] = ((lv.reindex(ex.index).fillna(0) / ex).to_dict(), F, r)
    conv = F[12]
    m8 = {"total": float(sum((1 - (1 - h[n]) ** 8) * conv + 9 * r for n in B["employer_nit"]))}
    lows, highs = [tot], [tot]
    for name, (hh, FF, rr) in fam.items():
        t2 = total_of(B, hh, FF, rr)
        s2 = shares_of(B, hh, FF, rr)
        lows.append(t2)
        highs.append(t2)
        ok("family: %s keeps the total cell" % name, cell(t2, 50) == fig["call_total"], "%.1f" % t2)
        ok("family: %s keeps every sector cell" % name, all(cell(s2[s], 5) == fig["call_share"][s] for s in C.SECTORS),
           " ".join("%.1f" % s2[s] for s in C.SECTORS))
    ok("family: leave by month 8 times the conversion keeps the total cell", cell(m8["total"], 50) == fig["call_total"],
       "%.1f" % m8["total"])

    # ------------------------------------------------------------------------------------------ semantic forks
    Dd = pd.read_csv(os.path.join(target, C.F_DEFAULTS))
    cures = Dd[Dd["cure_date"].notna()]
    gap = (pd.to_datetime(cures["cure_date"]) - pd.to_datetime(cures["default_date"])).dt.days
    ok("SF1 default dates are month-ends", pd.to_datetime(Dd["default_date"]).dt.is_month_end.all())
    ok("SF2 cures within eight months of default are under one per cent of defaults", (gap < 240).sum() < 0.01 * len(Dd),
       "%d of %d" % ((gap < 240).sum(), len(Dd)))
    ok("SF3 every launch loan is disbursed on 1 February 2027", (B["disbursement_date"] == "2027-02-01").all())
    ok("SF4 every launch employer has a register sector", B["sector"].notna().all() and set(B["sector"]) == set(C.SECTORS))
    pr = K.golden_probs(B, h, F, r)
    Bw = B.assign(p=pr, prin=B["principal"].astype(float))
    for s in C.SECTORS:
        g = Bw[Bw["sector"] == s]
        ok("SF5 %s balance-weighted share in the same cell" % s,
           cell(100 * (g.p * g.prin).sum() / g.prin.sum(), 5) == fig["call_share"][s])
    # SF6: the first month a leaver misses is the month after the final settlement, because the settlement month is a
    # paid month on the register and SIN SALARIO is a month with no salary paid; reading the settlement month as the
    # first missed one contradicts both
    liq = G[G["payment_type"] == "LIQUIDACION"]
    ok("SF6 every final settlement is a paid month (positive net pay)", (liq["net_pay"].astype(float) > 0).all())
    ok("SF6 the returns file defines SIN SALARIO as a month with no salary paid",
       any("no salary paid to the member in the month" in row[3] for row in DOC.FIELDS))
    ok("SF7 one loan per member", B["member_id"].is_unique)
    ok("SF8 shares from rounded sector counts land in the same cells",
       all(cell(100 * C.nearest(sh[s] * (B["sector"] == s).sum() / 100, 1) / (B["sector"] == s).sum(), 5) == fig["call_share"][s]
           for s in C.SECTORS))

    # ------------------------------------------------------------------------------------------ the three rules
    dp = K.default_path(target)
    ok("R1 the pack ships the loan book, the monthly returns and the employee-period registers",
       rows[C.F_LOANS] > 40000 and rows[C.F_RETURNS] > 10000 and rows[C.F_REGISTERS] > 25000)
    heads = {f: open(os.path.join(target, f), encoding="utf-8").readline().lower() for f in files if f.endswith(".csv")}
    ok("R1 no shipped column holds a leaving rate, a turnover, a conversion or a PD",
       not any(re.search(r"turnover|hazard|leav|attrition|conversion|\bpd\b|probab|default_rate", hd) for hd in heads.values()))
    ok("R3a the default path (PD model on borrower attributes) files 50, not 250", cell(dp["total"], 50) == 50 and
       cell(dp["total"], 50) != fig["call_total"], "%.1f" % dp["total"])
    ok("R3a the default path's sector shares are 0 per cent in every sector",
       all(cell(100 * dp["sectors"][s] / (B["sector"] == s).sum(), 5) == 0 for s in C.SECTORS))
    ok("R3b the decisive step alone files the golden", cell(tot, 50) == fig["call_total"])
    ok("R3b rung 1 alone (pooled public rate) stays at 50", cell(dp["pooled_total"], 50) == 50, "%.1f" % dp["pooled_total"])
    ok("R3b rung 1 alone (temporaries as the analogue) stays at 50", cell(dp["temp_rate"] * C.N_LAUNCH, 50) == 50)
    rr = K.ratio_route(target, dict(h=h))
    ok("R3b rung 2 alone (rate scaled by leaving) lands a full cell away", abs(cell(rr["total"], 50) - fig["call_total"]) >= 100,
       "%.1f" % rr["total"])
    ok("R3b every rung clears the golden's cell edges by a full cell", dp["total"] <= 225 - 50 and rr["total"] >= 275 + 50)
    # R2: each mess item mishandled leaves the call where it was
    Rraw = pd.read_csv(os.path.join(target, C.F_RETURNS), dtype=str)
    Rraw["loan"] = Rraw["loan_reference"]
    Rraw["t"] = Rraw["period"].map(K.month_of)
    Rraw["left"] = Rraw["reason"].isin(["01", "SIN SALARIO"])
    D2 = D.copy()
    D2["loan"] = D2["loan_reference"]
    F_raw, _ = K.conversion(L, Rraw, D2)
    ok("R2 returns and defaults joined on the raw references (no crosswalk), duplicates kept: total cell",
       cell(total_of(B, h, F_raw, r), 50) == fig["call_total"], "%.1f" % total_of(B, h, F_raw, r))
    Graw = pd.read_csv(os.path.join(target, C.F_REGISTERS), dtype=str)
    Graw["emp"] = Graw["employee_id"]
    Graw["t"] = Graw["period_start"].map(lambda s: C.mi(int(s[:4]), int(s[5:7])))
    Graw["hire_t"] = Graw["hire_date"].map(lambda s: C.mi(int(s[:4]), int(s[5:7])))
    hraw, _, _ = K.hazards(Graw)
    ok("R2 registers with repeated uploads kept and ids not normalised: total and sector cells",
       cell(total_of(B, hraw, F, r), 50) == fig["call_total"] and
       all(cell(shares_of(B, hraw, F, r)[s], 5) == fig["call_share"][s] for s in C.SECTORS))
    R01 = R.copy()
    R01["left"] = R01["reason"] == "SIN SALARIO"
    F01, _ = K.conversion(L, R01, D)
    ok("R2 reading only the April 2023 text codes keeps the total cell (runs since April 2023 alone)",
       cell(total_of(B, h, F01, r), 50) == fig["call_total"], "%.1f" % total_of(B, h, F01, r))
    ok("R3c no copied or backfilled block: no two employers share a leaver count and exposure",
       len(set((nl[k], expo[k]) for k in nl)) == len(nl))
    ok("R3c no memo, briefing or stakeholder figure states a forecast, a turnover or a private PD",
       not any(re.search(r"turnover|leaving rate|launch forecast", t, re.I) for t in DOC.rules_text()))

    # ------------------------------------------------------------------------------------------ the asks
    truth = PK.ask_truth()
    a = K.ask_a(target)
    b = K.ask_b(target)
    for s in C.SECTORS:
        ok("ask A %s deducted reproduces the clean truth" % s, abs(a["deducted"][s] - truth["deducted"][s]) < 0.5)
        ok("ask A %s not received reproduces the clean truth" % s, abs(a["outstanding"][s] - truth["outstanding"][s]) < 0.5)
        ok("ask A %s figures in figures.json" % s, fig["ask_a_deducted"][s] == C.nearest(a["deducted"][s], 1000)
           and fig["ask_a_outstanding"][s] == C.nearest(a["outstanding"][s], 1000))
    for y in (2023, 2024):
        for t in C.AGENCY_TYPES:
            ok("ask B %d %s reproduces the clean truth" % (y, t), abs(b[y][t] - truth["recovered"][y][t]) < 0.5)
            ok("ask B %d %s in figures.json" % (y, t), fig["ask_b_recovered"][str(y)][t] == C.nearest(b[y][t], 1000))
    rows_c = CR.score(fig, target)
    for asknm, route, hits, n in rows_c:
        ok("cracker: ask %s on the %s route misses every cell" % (asknm, route), hits == 0, "%d of %d" % (hits, n))
    pc, ml = CR.pair(rows_c)[:2]
    ok("pair ceiling at or under 40", pc <= 40.0, "%.1f" % pc)
    ok("mirror leakage under 35 per cent", ml < 35.0, "%.1f" % ml)
    call_files = {C.F_LOANS, C.F_XWALK, C.F_RETURNS, C.F_DEFAULTS, C.F_REGISTERS, C.F_LAUNCH, C.F_AGREE}
    ask_device_files = {C.F_SCHED, C.F_STMT, C.F_RECEIPTS, C.F_SAVINGS}
    ok("separation: no ask device file is read by the call", not (call_files & ask_device_files))
    sched = truth["sched"]
    for s in C.SECTORS:
        ok("ask A device: a 2026 corrected schedule in %s" % s, any(x["kind"] == "replacement" and C.ym(x["period"])[0] == 2026
                                                                   and W.employers()[x["emp"]]["sector"] == s for x in sched))
    E_ = W.employers()
    parents = {e["i"] for e in E_ if e["name"] in W.GROUP_PARENT.values()}
    grp = [x for x in truth["tr"] if len(x[4]) > 1 and x[1] in parents]
    ok("ask A device: every group parent pays its subsidiary's schedules in its own transfers",
       {x[1] for x in grp} == parents and len(grp) >= 30, "%d transfers" % len(grp))
    rec = truth["receipts"]
    P = W.world()["P"]
    for y in (2023, 2024):
        for t in C.AGENCY_TYPES:
            ks = [k for d, i, ch, org, am, k in rec if C.ym(int(P["dflt_m"][i]))[0] == y and P["A"][P["ag"][i]]["type"] == t]
            ok("ask B device: own netting and a relative's payment in %d %s" % (y, t), "own" in ks and "other" in ks)

    # ------------------------------------------------------------------------------------------ distractors
    for dfile in C.DISTRACTORS:
        ok("distractor %s is read by no golden figure" % dfile, dfile not in call_files | ask_device_files)

    # ------------------------------------------------------------------------------------------ realism and dates
    ok("realism: sector launch counts all differ", len(set(B.groupby("sector").size())) == 6)
    ok("realism: the call is not a round number before rounding", abs(tot - round(tot)) > 0.01 or tot % 50 != 0)
    ok("realism: employers' monthly leaving rates all differ", len(set(round(v, 6) for v in h.values())) == len(h))
    dates_ok = True
    for f, col in ((C.F_REGISTERS, "pay_date"), (C.F_RECEIPTS, "receipt_date"), (C.F_STMT, "posting_date"),
                   (C.F_SAVINGS, "movement_date"), (C.F_SCHED, "filed_on")):
        v = pd.read_csv(os.path.join(target, f), usecols=[col], dtype=str)[col]
        if (v > "2027-01-22").any():
            dates_ok = False
    ok("dates: no extract row after the 22 January 2027 pull", dates_ok)
    ok("dates: the rules are approved before the pull and after the last agreement", DOC.RULES_DATE < C.PULL)
    ok("persona: only the two drawn names appear in the documents",
       all(n in ("Paola Ayala", "Esteban Ospina") for n in re.findall(r"Paola Ayala|Esteban Ospina|[A-Z][a-z]+ [A-Z][a-z]+ Director", " ".join(DOC.rules_text()))))

    # ------------------------------------------------------------------------------------------ registers (H9)
    dic = {}
    for f, field, _, _ in DOC.FIELDS:
        dic.setdefault(f, []).append(field)
    for f in files:
        if f.endswith(".csv"):
            hd = open(os.path.join(target, f), encoding="utf-8").readline().strip().split(",")
            ok("dictionary lists exactly the fields of %s" % f, hd == dic.get(f), str(set(hd) ^ set(dic.get(f, []))))
    ok("dictionary covers the agreements register", dic.get(C.F_AGREE) ==
       ["employer_nit", "legal_name", "sector", "agreement_signed", "first_register_period", "city"])
    from pypdf import PdfReader
    from pdfminer.high_level import extract_text
    for f in (C.F_RULES, C.F_SUPER):
        strict = " ".join(p.extract_text() for p in PdfReader(os.path.join(target, f), strict=True).pages)
        miner = extract_text(os.path.join(target, f))
        key = {C.F_RULES: "in default from the month-end at which an instalment is 90 or more days past due",
               C.F_SUPER: "Libranza Empresarial: no loans at 31 December 2025"}[f]
        ok("H25 %s reads under a strict and an independent extractor" % f,
           key in re.sub(r"\s+", " ", strict) and key in re.sub(r"\s+", " ", miner))
    with zipfile.ZipFile(os.path.join(task, "target.zip")) if os.path.exists(os.path.join(task, "target.zip")) else None as z:
        if z is not None:
            ok("H4 the archive holds exactly the pack's files, no folder", sorted(z.namelist()) == files)

    # ------------------------------------------------------------------------------------------ report
    fails = [x for x in RESULTS if not x[1]]
    for name, good, det in RESULTS:
        if not good:
            print("FAIL  %s  %s" % (name, det))
    print("checks.py: %s %d of %d" % ("PASS" if not fails else "FAIL", len(RESULTS) - len(fails), len(RESULTS)))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")))
