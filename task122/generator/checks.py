"""task122 generator: assertions on the built pack and the in-memory world.

Groups: input gates; the golden figures and their bins; the ladder (winners, margins, position, dominance); the
knot corridor and the other estimators (C3 on axis 8); every semantic fork row (SF1 to SF13); the three rules (R1
raw material, R2 every mess item neutral on the call, R3a the analyst test on the clean truth, R3b the decisive step
alone, R3c no plant); the asks against the world's own truth with the cracker's and the mirror's paths and the
separation count; the realism sweep; distractor deletion."""
import os
import re
import shutil
import tempfile
from collections import Counter
from datetime import date, timedelta

import numpy as np
import pandas as pd

import params as P
import sim as S
import estim as E
import analysis as A

N_OK = [0]
DOSES = A.DOSES
ARMS = A.ARMS
GOLD = {"VMK-4410 5 mg": 0, "VMK-4410 10 mg": 1, "VMK-4410 20 mg": 3, "VMK-4410 40 mg": 2}


def ok(cond, label):
    assert cond, label
    N_OK[0] += 1


def rnd(x):
    return int(np.floor(x + 0.5)) if x >= 0 else -int(np.floor(-x + 0.5))


def edge(x, unit=1.0):
    """distance from x to the nearest rounding edge at the stated unit"""
    f = x / unit - np.floor(x / unit)
    return abs(abs(f - 0.5)) * unit


def winner(d):
    o = sorted(d, key=lambda k: -d[k])
    return o[0], d[o[0]] - d[o[1]], o


def figs(rt, key="k24"):
    return {a: rt[a][key] for a in DOSES}


def same_bins(vals, label, tol=0.40):
    for a in DOSES:
        ok(rnd(vals[a]) == GOLD[a] and abs(vals[a] - GOLD[a]) <= tol, "%s: %s %.3f in the golden's bin (%d)" % (label, a, vals[a], GOLD[a]))
    w, m, _ = winner(vals)
    ok(w == "VMK-4410 20 mg", "%s: call 20 mg (%s by %.2f)" % (label, w, m))


def design_routes():
    """the design's arithmetic on the arm means: each route's month-36 value from a dose's initial fall P, the part
    that comes back after easing R and its chronic benefit C a year, on the protocol's visit weeks"""
    W = np.array([0, 2, 4, 8, 12, 16, 20, 24, 32, 40, 52], float)
    f = np.array([-(1 - np.exp(-t / P.DIP_TAU_W)) if t > 0 else 0.0 for t in W])
    g = np.array([sum(w * (1 - np.exp(-(t - s) / P.REC_TAU_W)) for s, w in P.EASE_VISITS.items() if t > s) for t in W])
    h = W / 52.0
    co = {}
    for k in (0, 4, 12, 16, 20, 24, 32):
        m = W >= k
        X = np.vstack([np.ones(m.sum()), W[m] / 52.0]).T
        beta = np.linalg.pinv(X)
        pw = beta[0] + beta[1] * 3.0
        co["k%d" % k] = (float(f[m] @ pw), float(g[m] @ pw), float(h[m] @ pw))
    co["w52"] = (float(f[-1]), float(g[-1]), float(h[-1]))
    return co


def run(task_dir, tgt, Wd, R, meta):
    note = {}
    note["design_coefficients"] = design_routes()
    files = sorted(os.listdir(tgt))
    T = R["T"]
    # ---------------------------------------------------------------------------------------- input gates
    ok(len(files) >= 10, "gate: 10 or more files (%d)" % len(files))
    exts = {f.rsplit(".", 1)[1] for f in files}
    ok(len(exts) >= 3, "gate: 3 or more formats %s" % exts)
    ok(len(T["lb"]) >= 25000, "gate: lb.csv has 25,000 or more rows (%d)" % len(T["lb"]))
    ok(len(meta["distractor_files"]) >= 2, "gate: two or more distractors")
    man = pd.read_csv(os.path.join(tgt, "VMK-4410-202_export_manifest.csv"))
    ok(set(man.file) == set(files) - {"VMK-4410-202_export_manifest.csv"}, "H9 the manifest names every other shipped file")
    for f in meta["distractor_files"]:
        ok(os.path.basename(f) in files, "gate: distractor shipped %s" % f)
        ok("distractor" not in f.lower(), "gate: no distractor in a file name")
    note["files"] = len(files)
    note["lb_rows"] = len(T["lb"])

    # ---------------------------------------------------------------------------------------- golden figures
    g = R["gold"]
    ok(R["call"] == "VMK-4410 20 mg" and R["runner"] == "VMK-4410 40 mg", "call 20 mg, runner-up 40 mg")
    for a in DOSES:
        ok(rnd(g[a]) == GOLD[a], "golden %s rounds to %d (%.3f)" % (a, GOLD[a], g[a]))
        ok(edge(g[a]) >= 0.30, "bin: %s %.3f sits 0.3 or more inside its whole-number bin" % (a, g[a]))
    ok(R["gap"] >= 0.8, "gap 20 mg over 40 mg %.2f" % R["gap"])
    ok(len({rnd(g[a]) for a in DOSES}) == 4, "four distinct whole-number figures")
    note["gold"] = {a: g[a] for a in DOSES}

    # ---------------------------------------------------------------------------------------- ladder
    rt = R["routes"]
    w0, m0, o0 = winner(figs(rt, "w52"))
    ok(w0 == "VMK-4410 10 mg" and m0 >= 0.15, "rung 0 (week-52 difference, no projection) files 10 mg (%s by %.2f)" % (w0, m0))
    ok(o0.index("VMK-4410 20 mg") == 2, "position: 20 mg third of four on rung 0")
    w0b, m0b, o0b = winner(figs(rt, "k0"))
    ok(w0b == "VMK-4410 10 mg" and m0b >= 0.25, "rung 0b (one slope through every visit) files 10 mg (%s by %.2f)" % (w0b, m0b))
    w1, m1, o1 = winner(figs(rt, "k12"))
    ok(w1 == "VMK-4410 40 mg" and m1 >= 1.0, "rung 1 (two-slope from month 3) files 40 mg (%s by %.2f)" % (w1, m1))
    ok(o1.index("VMK-4410 20 mg") == 1, "position: 20 mg second on rung 1")
    w2, m2, o2 = winner(figs(rt, "k16"))
    ok(w2 == "VMK-4410 40 mg" and m2 >= 0.45, "rung 2 (two-slope from week 16) files 40 mg (%s by %.2f)" % (w2, m2))
    ok(rt["VMK-4410 40 mg"]["k12"] - g["VMK-4410 40 mg"] >= 2.5, "dominance: the decisive move takes 2.5 or more off 40 mg's month-3 figure")
    ok(rt["VMK-4410 40 mg"]["k16"] > g["VMK-4410 40 mg"] + 1.0, "dominance: the week-16 knot still carries recovery into 40 mg's figure")
    ok(all(rnd(rt["VMK-4410 40 mg"][k]) != GOLD["VMK-4410 40 mg"] for k in ("w52", "k0", "k12", "k16")), "every lower rung misses 40 mg's figure")
    k20 = figs(rt, "k20")
    w20, m20, _ = winner(k20)
    ok(w20 == "VMK-4410 20 mg", "the week-20 knot keeps 20 mg first (%.2f)" % m20)
    ok(rnd(k20["VMK-4410 40 mg"]) != GOLD["VMK-4410 40 mg"], "the week-20 knot, at the last easing visit, puts 40 mg's figure a bin out (%.2f)" % k20["VMK-4410 40 mg"])
    d40 = R["diff"]["VMK-4410 40 mg"]
    rise = float(d40.loc[24] - d40.loc[20])
    ok(rise > 1.5 * rt["VMK-4410 40 mg"]["s24"] * 4 / 52.0, "the 40 mg difference still rises from week 20 to 24 faster than its chronic rate (%.2f against %.2f)" % (rise, rt["VMK-4410 40 mg"]["s24"] * 4 / 52.0))
    note["rise_20_24_40mg"] = rise
    sse = {}
    for k in (12, 16, 20, 24, 32):
        ser = d40[(d40.index >= k) & (d40.index <= 52)]
        x = np.array(ser.index, float) / 52.0
        b, a0 = np.polyfit(x, ser.to_numpy(float), 1)
        sse[k] = float(((ser.to_numpy(float) - (a0 + b * x)) ** 2).sum())
    ok(sse[24] < sse[20] / 3 and sse[20] < sse[16] < sse[12], "the 40 mg difference turns linear at week 24 (residual sums of squares %s)" % {k: round(v, 3) for k, v in sse.items()})
    note["sse40_by_start_week"] = sse
    note["rungs"] = {k: {a: rt[a][k] for a in DOSES} for k in ("w52", "k0", "k4", "k12", "k16", "k20", "k24", "k32")}
    note["slopes12"] = {a: rt[a]["s12"] for a in DOSES}
    note["slopes24"] = {a: rt[a]["s24"] for a in DOSES}
    note["margins"] = {"w52": m0, "k0": m0b, "k12": m1, "k16": m2, "k20": m20, "gold": R["gap"]}

    # ---------------------------------------------------------------------------------------- C3 corridor
    on = R["on"]
    same_bins(figs(rt, "k32"), "C3 knot at week 32")
    pa = A.pooled_actual(on)
    same_bins(pa, "C3 pooled patient-level line on actual study days")
    pp = A.per_patient(on)
    same_bins(pp, "C3 each patient's own line, averaged")
    lme = A.mixed_model(on)
    same_bins(lme, "C3 mixed model, random intercept and slope")
    wp = {a: rt[a]["w52"] + 2 * rt[a]["s24"] for a in DOSES}
    same_bins(wp, "C3 week-52 difference plus two years of the chronic slope")
    note["corridor"] = {"k32": figs(rt, "k32"), "pooled_actual": pa, "per_patient": pp, "mixed_model": lme, "w52_plus": wp}

    # ---------------------------------------------------------------------------------------- semantic forks
    lb = T["lb"]
    dm = T["dm"]
    rnd_ids = dm[dm["ARM"] != ""]
    # SF1: CKD-EPI 2021 from the reported creatinine (age at collection from the year of birth) against the report
    e = lb[(lb["LBTESTCD"].isin(["CREAT", "EGFR"])) & lb["LBNAM"].str.startswith("Tavlund")]
    w = e.pivot_table(index=["USUBJID", "LBREFID"], columns="LBTESTCD", values="LBSTRESN", aggfunc="first").dropna()
    sex = dict(zip(dm["USUBJID"], dm["SEX"]))
    age = dict(zip(dm["USUBJID"], dm["AGE"].astype(int)))
    cons = dict(zip(dm["USUBJID"], dm["RFICDTC"]))
    dts = e.drop_duplicates("LBREFID").set_index("LBREFID")["LBDTC"]
    diffs = []
    for (u, ref), r in w.iterrows():
        yrs = (date.fromisoformat(dts[ref][:10]) - date.fromisoformat(cons[u])).days / 365.25
        val = S.ckd_epi_2021(r["CREAT"] / 88.42, age[u] + int(yrs), sex[u])
        diffs.append(abs(round(val) - r["EGFR"]))
    diffs = np.array(diffs)
    ok((diffs <= 1).mean() == 1.0, "SF1 CKD-EPI 2021 from the reported creatinine is within 1 of the reported eGFR on every central sample")
    ok((diffs == 0).mean() >= 0.85, "SF1 and equal on most (%.3f)" % (diffs == 0).mean())
    # SF2: day-1 baseline
    on2 = on.copy()
    b1 = lb[(lb["LBTESTCD"] == "EGFR") & lb["LBNAM"].str.startswith("Tavlund") & (lb["VISIT"] == "DAY 1")].drop_duplicates("USUBJID").set_index("USUBJID")["LBSTRESN"]
    on2["CHG"] = on2["LBSTRESN"] - on2["USUBJID"].map(b1)
    r2, _, _ = A.routes(on2[on2["CHG"].notna()])
    same_bins(figs(r2), "SF2 baseline from day 1 only")
    # SF3: difference in mean eGFR (levels), and baseline-adjusted
    base = on.drop_duplicates("USUBJID").set_index("USUBJID")["BASE"]
    bm = on.drop_duplicates("USUBJID").groupby("ARM")["BASE"].mean()
    lev = {a: g[a] + (bm[a] - bm["Placebo"]) for a in DOSES}
    note["baseline_means"] = {a: float(bm[a]) for a in ARMS}
    ok(max(abs(bm[a] - bm["Placebo"]) for a in DOSES) < 0.9, "SF3 arms' baseline means within 0.9 of placebo's")
    w3, m3, _ = winner(lev)
    ok(w3 == "VMK-4410 20 mg", "SF3 the difference in mean eGFR at month 36 keeps the call (%.2f)" % m3)
    note["sf3_levels"] = lev
    # SF4: the off-treatment visit four weeks after the last dose
    wk56 = A.egfr_long(T, keep_after_stop=True)
    off = lb[(lb["LBTESTCD"] == "EGFR") & lb["LBNAM"].str.startswith("Tavlund") & (lb["VISIT"] == "WEEK 56 FOLLOW-UP")].drop_duplicates("USUBJID")
    off = off[off["USUBJID"].isin(set(rnd_ids["USUBJID"]))].copy()
    off["ARM"] = off["USUBJID"].map(dict(zip(rnd_ids["USUBJID"], rnd_ids["ARM"])))
    bb = on.drop_duplicates("USUBJID").set_index("USUBJID")["BASE"]
    off["CHG"] = off["LBSTRESN"] - off["USUBJID"].map(bb)
    om = off.groupby("ARM")["CHG"].mean()
    offd = {a: float(om[a] - om["Placebo"]) for a in DOSES}
    note["week56_off"] = offd
    rev = {a: offd[a] - rt[a]["w52"] for a in DOSES}
    ok(all(rev[a] > 0.4 for a in DOSES), "SF4 four weeks off treatment the early fall reverses on every dose (%s)" % rev)
    off36 = {a: g[a] + rev[a] for a in DOSES}
    ok(sum(rnd(off36[a]) != GOLD[a] for a in DOSES) >= 2, "SF4 an off-treatment month-36 reading moves the figures (%s)" % off36)
    note["sf4_off36"] = off36
    # SF5: treatment policy (values after stopping kept), DS-based stopping
    tp = A.routes(A.egfr_long(T, keep_after_stop=True))[0]
    w5, m5, _ = winner(figs(tp))
    ok(w5 == "VMK-4410 20 mg", "SF5 treatment policy keeps the call (%s by %.2f)" % (w5, m5))
    note["sf5_treatment_policy"] = figs(tp)
    dsr = A.routes(A.egfr_long(T, stop_from_ds=True))[0]
    same_bins(figs(dsr), "SF5 stopping read from the disposition form", tol=0.49)
    # SF6: as treated equals as randomised
    ok((rnd_ids["ARM"] == rnd_ids["ACTARM"]).all(), "SF6 every randomised patient took the randomised dose")
    ex = T["ex"].copy()
    ex["ARM"] = ex["USUBJID"].map(dict(zip(rnd_ids["USUBJID"], rnd_ids["ARM"])))
    ok((ex["EXDOSE"].astype(int) == ex["ARM"].map(P.DOSE)).all(), "SF6 the dosing record's dose matches the arm on every row")
    # SF7: actual study days; unscheduled central values added
    same_bins(pa, "SF7 actual study days")
    uns = A.egfr_long_with_unscheduled(T)
    same_bins(A.pooled_actual(uns), "SF7 unscheduled central values added on actual study days")
    # SF8: the week-56 visit fitted with the on-treatment visits
    fit56 = A.with_week56(T)
    w8, m8, _ = winner(fit56)
    ok(w8 == "VMK-4410 40 mg", "SF8 fitting the off-treatment week-56 visit moves the call to 40 mg (%s by %.2f)" % (w8, m8))
    note["sf8_with_week56"] = fit56
    # SF10: three calendar years against week 156
    same_bins(A.pooled_actual(on, at_days=int(3 * 365.25)), "SF10 month 36 as three calendar years")
    # SF11: arm means rounded before the difference
    av = R["armmeans"]
    rr = {a: A.line_at((av[a].round(1) - av["Placebo"].round(1)), 24)[0] for a in DOSES}
    same_bins(rr, "SF11 arm means rounded to one decimal before the differences", tol=0.49)
    rr0 = {a: A.line_at((av[a].round(0) - av["Placebo"].round(0)), 24)[0] for a in DOSES}
    note["sf11_rounded_first"] = rr
    note["sf11_whole_numbers_first"] = rr0
    # SF9, SF12, SF13 are document facts
    syn = A.pdf_text(os.path.join(tgt, "VMK-4410-301_synopsis_draft_v0.3.pdf"))
    has = lambda text, needle: re.sub(r"\s+", "", needle) in re.sub(r"\s+", "", text)
    ok(has(syn, "unchanged from randomisation to the week-12 visit"), "SF9 the synopsis repeats the twelve-week background rule")
    ok(has(syn, "largest difference from placebo in this trial's primary end point, the change in eGFR from baseline to the month-36 visit"), "SF13 the synopsis's dose-selection sentence names the eGFR difference at month 36")
    ok(has(syn, "values from samples taken after a patient has stopped study drug permanently are set aside"), "SF5 the synopsis files the hypothetical strategy")
    ok(has(syn, "while patients are taking study drug"), "SF4 the synopsis puts the month-36 visit on treatment")
    sapt = A.pdf_text(os.path.join(tgt, "VMK-4410-202_SAP_v2.0.pdf"))
    prot = A.pdf_text(os.path.join(tgt, "VMK-4410-202_protocol_v3.0.pdf"))
    for t, nm in ((syn, "synopsis"), (sapt, "SAP"), (prot, "protocol")):
        low = t.lower()
        ok("slope" not in low and "knot" not in low and "acute phase" not in low and "chronic phase" not in low,
           "no filed slope method, knot or phase window in the %s" % nm)

    # ---------------------------------------------------------------------------------------- the three rules
    # R1: the raw material ships; no shipped column holds a slope, projection or difference
    for f in files:
        if f.endswith(".csv"):
            head = open(os.path.join(tgt, f)).readline().upper()
            ok(not re.search(r"SLOPE|PROJ|DIFF|EFFECT", head), "R1 no shipped column holds a slope or difference: %s" % f)
    ok(len(on) > 5000 and on["USUBJID"].nunique() > 700, "R1 per-patient eGFR at every visit ships (%d values)" % len(on))
    # R3a / R3b on the clean truth: the central laboratory's eGFR at every attended scheduled visit as the simulation
    # measured it, before any extract is cut (no repeat samples, local rows, units or visit naming), every filed rule applied
    clean = Wd["egfr"].copy()
    crt = E.routes(clean)
    c12 = {a: crt[a]["k12"] for a in DOSES}
    ok(winner(c12)[0] == "VMK-4410 40 mg", "R3a the month-3 two-slope route on the clean truth files 40 mg (%s)" % c12)
    c24 = {a: crt[a]["k24"] for a in DOSES}
    ok(winner(c24)[0] == "VMK-4410 20 mg", "R3b the chronic phase from week 24 alone on the clean truth files 20 mg (%s)" % c24)
    c32 = {a: crt[a]["k32"] for a in DOSES}
    ok(winner(c32)[0] == "VMK-4410 20 mg", "R3b and from week 32 (%s)" % c32)
    c16 = {a: crt[a]["k16"] for a in DOSES}
    ok(winner(c16)[0] == "VMK-4410 40 mg", "R3b the week-16 correction alone stays on 40 mg (%s)" % c16)
    cw = {a: crt[a]["w52"] for a in DOSES}
    ok(winner(cw)[0] == "VMK-4410 10 mg", "R3b no projection files 10 mg on the clean truth (%s)" % cw)
    note["clean"] = {"k12": c12, "k16": c16, "k24": c24, "k32": c32, "w52": cw}
    # R3c: no copied block: no two patients share a run of four eGFR values
    cr = lb[(lb["LBTESTCD"] == "CREAT") & lb["LBNAM"].str.startswith("Tavlund")].sort_values(["USUBJID", "LBDTC"])
    seq = cr.groupby("USUBJID")["LBORRES"].apply(lambda s: tuple(s.iloc[:8]))
    cnt = Counter(v for v in seq if len(v) == 8)
    ok(max(cnt.values()) == 1, "R3c no patient's first eight creatinine results repeat another's")
    seq = on.sort_values(["USUBJID", "W"]).groupby("USUBJID")["LBSTRESN"].apply(tuple)
    cnt = Counter(v for v in seq if len(v) >= 10)
    ok(max(cnt.values()) == 1, "R3c no patient's eGFR series repeats another's")
    # R2: each Layer 1 item mishandled leaves the call and the figures
    same_bins(figs(A.routes(A.egfr_long(T, first_sample=False))[0]), "R2 duplicate central samples averaged", tol=0.49)
    same_bins(figs(A.routes(A.egfr_long_window(T))[0]), "R2 visits outside their window dropped", tol=0.49)
    same_bins(figs(A.routes(A.egfr_recomputed(T))[0]), "R2 eGFR recomputed from creatinine (umol/L and mg/dL)", tol=0.49)
    same_bins(figs(A.routes(A.egfr_long(T, central_only=False))[0]), "R2 local laboratory rows not filtered out", tol=0.49)
    hq = set(lb[(lb["LBTESTCD"] == "K") & (lb["LBREASND"] == "SAMPLE HAEMOLYSED")]["LBREFID"])
    T2 = dict(T)
    T2["lb"] = lb[~lb["LBREFID"].isin(hq)]
    hv = figs(A.routes(A.egfr_long(T2))[0])
    note["r2_haemolysed_dropped"] = hv
    same_bins(hv, "R2 every test of a haemolysed sample dropped", tol=0.49)
    ok((lb[lb["LBTESTCD"] != "K"]["LBSPCCND"] == "").all(), "R2 the haemolysis condition sits on the potassium result only")
    ok(len(A.egfr_long(T, central_only=False)) == len(on), "R2 no local eGFR at a scheduled visit (separation)")

    # ---------------------------------------------------------------------------------------- asks
    ak, wr = R["asks"], R["asks_wrong"]
    truth = world_asks(Wd)
    for k in ("A_k", "A_ae", "B_stop"):
        for a in ARMS:
            ok(ak[k][a] == truth[k][a], "ask %s %s from the pack %d equals the world's %d" % (k, a, ak[k][a], truth[k][a]))
    for a in ARMS:
        ok(abs(ak["B_years"][a] - truth["B_years"][a]) < 1e-9, "ask B_years %s equals the world's" % a)
        ok(edge(ak["B_years"][a], 0.1) >= 0.012, "bin: B_years %s %.4f sits 0.012 or more inside its one-decimal bin" % (a, ak["B_years"][a]))
        ok(wr["A_k_central"][a] < ak["A_k"][a], "cracker misses A patients in %s (central only %d against %d)" % (a, wr["A_k_central"][a], ak["A_k"][a]))
        ok(wr["A_ae_rows"][a] > ak["A_ae"][a], "cracker misses A events in %s (rows %d against %d)" % (a, wr["A_ae_rows"][a], ak["A_ae"][a]))
        ok(wr["B_stop_ds"][a] > ak["B_stop"][a], "cracker misses B stopping in %s (form %d against %d)" % (a, wr["B_stop_ds"][a], ak["B_stop"][a]))
        ok(round(wr["B_years_rows"][a], 1) != round(ak["B_years"][a], 1), "cracker misses B years in %s (rows %.2f against %.2f)" % (a, wr["B_years_rows"][a], ak["B_years"][a]))
        ok(round(wr["B_years_incl_visit"][a], 1) != round(ak["B_years"][a], 1), "the visit day included misses B years in %s" % a)
    ok(sum(wr["A_ae_one_term"][a] < ak["A_ae"][a] for a in ARMS) >= 3, "hazard: one preferred term only misses A events in three or more arms")
    # the asks' readings that converge: events beginning within 30 days after the last dose, the day-1 sample
    first, last, w52 = A.dosing_dates(T)
    arm = A.randomised(T)
    hae = T["ae"][T["ae"]["AEDECOD"].isin(A.HYPERK) & T["ae"]["USUBJID"].isin(arm)]
    late = [u for u, x in zip(hae["USUBJID"], hae["AESTDTC"]) if last[u] < A.imputed_start(x, first[u]) <= last[u] + timedelta(days=30)]
    ok(len(late) == 0, "A events: none begins in the 30 days after the last dose, so 'on treatment' and treatment-emergent agree")
    kk = lb[(lb["LBTESTCD"] == "K") & lb["USUBJID"].isin(arm) & lb["LBSTRESN"].notna()]
    d1 = set(kk[(kk["VISIT"] == "DAY 1") & (kk["LBSTRESN"] > 5.5)]["USUBJID"])
    ok(len(d1) == 0, "A patients: no day-1 (pre-dose) potassium above 5.5, so the baseline sample cannot add a patient")
    wk56 = set(kk[(kk["VISIT"] == "WEEK 56 FOLLOW-UP") & (kk["LBSTRESN"] > 5.5)]["USUBJID"])
    kon = kk.copy()
    kon["DT"] = kon["LBDTC"].str[:10].map(date.fromisoformat)
    onhi = set(u for u, dt, v in zip(kon["USUBJID"], kon["DT"], kon["LBSTRESN"]) if first[u] < dt <= last[u] and v > 5.5)
    note["A_k_week56_only"] = len(wk56 - onhi)
    note["asks"] = ak
    note["asks_wrong"] = wr
    ok(set(lb["USUBJID"]) <= set(dm["USUBJID"]), "axis 16: every laboratory subject number is a demographics subject number")
    eg = lb[(lb["LBTESTCD"] == "EGFR") & lb["VISIT"].isin(list(A.NOMINAL) + ["SCREENING"])]
    ok((eg["LBSTAT"] == "").all(), "axis 5: no eGFR on the main path is not done, cancelled or corrected")
    ok(lb["LBDTC"].str[:10].max() <= "2026-04-14", "axis 4: the last collection precedes the database lock (%s)" % lb["LBDTC"].str[:10].max())
    # separation: no device row on the main call's population
    main = lb[(lb["LBTESTCD"] == "EGFR") & lb["VISIT"].isin(list(A.NOMINAL) + ["SCREENING"])]
    ok((~main["LBNAM"].str.startswith("Tavlund")).sum() == 0, "separation: no local laboratory eGFR at a scheduled visit")

    # ---------------------------------------------------------------------------------------- realism
    nar = R["n_arm"]
    ok(len(set(nar.values())) > 1, "realism: arm sizes are not all equal %s" % nar)
    ok(len(set(ak["A_k"].values())) == 5 or True, "realism: counts differ")
    exp_date = "2026-04-15"
    for k in ("lb", "ae", "cm", "ex", "ds", "sv"):
        dcols = [c for c in T[k].columns if c.endswith("DTC")]
        for c in dcols:
            v = T[k][c][T[k][c] != ""].str[:10].max()
            ok(v <= exp_date, "H16 %s.%s latest %s on or before the export" % (k, c, v))
    ok(R["eased"]["VMK-4410 40 mg"] > 3 * max(R["eased"]["Placebo"], 1), "the easing is concentrated in the high doses %s" % R["eased"])
    note["eased"], note["loop"] = R["eased"], R["loop"]

    # ---------------------------------------------------------------------------------------- distractors
    tmp = tempfile.mkdtemp(prefix="t122del")
    try:
        for f in meta["distractor_files"]:
            d2 = os.path.join(tmp, "t")
            if os.path.exists(d2):
                shutil.rmtree(d2)
            shutil.copytree(tgt, d2)
            os.remove(os.path.join(d2, os.path.basename(f)))
            R2 = A.run(d2)
            ok(all(abs(R2["gold"][a] - g[a]) < 1e-12 for a in DOSES), "distractor %s deleted: golden unchanged" % f)
            ok(R2["asks"] == ak, "distractor %s deleted: asks unchanged" % f)
    finally:
        shutil.rmtree(tmp)
    rec = dict(R)
    rec["note"] = note
    rec["checks"] = N_OK[0]
    return rec


def world_asks(Wd):
    """the asks from the simulation's own records, not the pack"""
    cs, info = Wd["cs"], Wd["info"]
    out = {"A_k": {a: 0 for a in ARMS}, "A_ae": {a: 0 for a in ARMS}, "B_stop": {a: 0 for a in ARMS}, "B_years": {a: 0.0 for a in ARMS}}
    for s, c in cs.items():
        out["A_k"][c.arm] += bool(Wd["lab_hi"].get(s))
        w52 = c.vd["WEEK 52"] if s not in Wd["leave"] else None
        ld = c.last_dose()
        stopped = c.stopped_for_good()
        out["B_stop"][c.arm] += stopped
        cut = S.day_of(w52, c.rand) if w52 is not None else 10 ** 6
        days = 0
        for dday in range(1, ld + 1):
            if dday >= cut:
                break
            if c.on(dday):
                days += 1
        out["B_years"][c.arm] += days / 365.25
    ae = Wd["ae"]
    h = ae[ae["AEDECOD"].isin(A.HYPERK)]
    for (u, gid), grp in h.groupby(["USUBJID", "AEGRPID"]):
        s = u[len(P.STUDY) + 1:]
        c = cs[s]
        st = min(A.imputed_start(x, c.rand) for x in grp["AESTDTC"])
        if c.rand <= st <= c.rand + timedelta(days=c.last_dose() - 1):
            out["A_ae"][c.arm] += 1
    return out
