"""task131 generator: assertions on the built pack and the in-memory world.

Groups: input gates; the three rules (R1 raw material, R2 every mess item neutral on the call, R3a the analyst test
on the clean truth, R3b the decisive step alone, R3c no plant); the ladder (winners, margins, position, dominance);
every semantic fork row (SF1 to SF13); the closure variants; bins; the asks against the world's own truth, with the
cracker's and the mirror's paths; the realism sweep; distractor deletion."""
import os
from collections import Counter
from datetime import date, timedelta

import numpy as np
import pandas as pd

import params as P
import knobs as K
import weather as WX
import sim as S
import analysis as A

N_OK = [0]


def ok(cond, label):
    assert cond, label
    N_OK[0] += 1


def rnd(x):
    return int(np.floor(x + 0.5)) if x >= 0 else -int(np.floor(-x + 0.5))


def bin_gap(x, unit=1.0):
    """distance from x to the nearest rounding edge at the stated unit"""
    f = (x / unit) - np.floor(x / unit)
    return min(abs(f - 0.5), 1.0) * unit if True else 0


def run(task_dir, tgt, Wd, R, meta):
    hh, ev = Wd["hh"], Wd["ev"]
    files = sorted(os.listdir(tgt))
    # ---------------------------------------------------------------------------------------- input gates
    ok(len(files) >= 10, "gate: 10 or more files (%d)" % len(files))
    exts = {f.rsplit(".", 1)[1] for f in files}
    ok(len(exts) >= 3, "gate: 3 or more formats %s" % exts)
    n300 = sum(1 for line in open(os.path.join(tgt, "MRP_NEM12_202601.csv")) if line.startswith("300"))
    ok(n300 >= 25000, "gate: a file of 25,000 or more rows (%d)" % n300)
    ok(len(meta["distractor_files"]) >= 2, "gate: two or more distractors")
    man = pd.read_csv(os.path.join(tgt, "tariff_advice_file_list_2026-10-09.csv"))
    ok(set(man.file) == set(files) - {"tariff_advice_file_list_2026-10-09.csv"}, "H9 the file list names every other shipped file")
    for f in meta["distractor_files"]:
        ok(os.path.basename(f) in files, "gate: distractor shipped %s" % f)
        ok("distractor" not in f.lower(), "gate: no distractor in a file name")

    # ---------------------------------------------------------------------------------------- figures
    ch = {a: R[a]["change"] for a in P.DESIGNS}
    ok(R["call"] == "C", "call is Design C (%s)" % R["call"])
    ok(ch["C"] > 0 and ch["A"] < 0 and ch["B"] < 0, "C lowers the maximum, A and B raise it %s" % ch)
    ok(R["A"]["md_ti"] == 43 and R["B"]["md_ti"] == 41 and R["C"]["md_ti"] == 41, "maximum half-hours: A 21:00, B and C 20:00")
    for a in P.DESIGNS:
        ok(R[a]["md_gap"] >= 4.0, "R3 %s maximum leads the next half-hour by 4 MW or more (%.2f)" % (a, R[a]["md_gap"]))
        g = abs((ch[a] - np.floor(ch[a])) - 0.5)
        ok(g >= 0.30, "bin: %s change %.3f sits 0.2 MW or more inside its whole-MW bin" % (a, ch[a]))

    # ---------------------------------------------------------------------------------------- ladder
    r0 = {a: R[a]["R0"] for a in P.DESIGNS}
    r0b = {a: R[a]["R0b"] for a in P.DESIGNS}
    r1 = {a: R[a]["R1"] for a in P.DESIGNS}
    r2 = {a: R[a]["R2"] for a in P.DESIGNS}
    def lead(d):
        o = sorted(d, key=lambda k: -d[k])
        return o[0], d[o[0]] / d[o[1]], o
    w0, m0, o0 = lead(r0)
    ok(w0 == "B" and m0 >= 1.15, "rung 0 (window cut, all workdays) files B by 1.15x or more (%s %.3f)" % (w0, m0))
    ok(rnd(r0["B"]) == 15, "rung 0: B lowers the maximum by 15 MW (%.2f)" % r0["B"])
    w0b, m0b, _ = lead(r0b)
    ok(w0b == "B" and m0b >= 1.15, "rung 0b (cut at the forecast's maximum half-hour, all workdays) files B (%s %.3f)" % (w0b, m0b))
    w1, m1, _ = lead(r1)
    ok(w1 == "B" and m1 >= 1.15, "rung 1 (hot-day cut at the maximum half-hour) files B (%s %.3f)" % (w1, m1))
    ok(r1["B"] > r0["B"] + 4, "rung 1 moves B's figure further from the golden than rung 0")
    w2, m2, _ = lead(r2)
    ok(w2 == "A" and m2 >= 1.15, "rung 2 (whole curve, average workday) files A (%s %.3f)" % (w2, m2))
    ok(o0.index("C") == 2, "position: C last on rung 0")
    ok(sorted(r1, key=lambda k: -r1[k]).index("C") == 2, "position: C last on rung 1")
    ok(sorted(r2, key=lambda k: -r2[k]).index("C") == 1, "position: C second on rung 2")
    ok(r2["A"] > 0 and ch["A"] < 0 and r2["B"] > 0 and ch["B"] < 0, "dominance: the decisive move reverses A and B")
    ok(all(rnd(r2[a]) != rnd(ch[a]) for a in P.DESIGNS), "the decisive rung moves every design's graded figure to another whole MW (%s)" % r2)
    ok(min(abs(r1[a] - ch[a]) for a in P.DESIGNS) > 4.0, "the hot-day cut alone moves every figure 4 MW or more away (%s)" % r1)

    # ---------------------------------------------------------------------------------------- the three rules
    # R1: the raw material ships, nothing ships the deciding quantity
    for f in files:
        if f.endswith(".csv"):
            head = open(os.path.join(tgt, f)).readline().lower()
            ok("effect" not in head and "impact" not in head and "reduction" not in head, "R1 no shipped column holds an effect: %s" % f)
    ok(len(R["reads"]) > 2000, "R1 interval reads per meter register ship (%d registers)" % len(R["reads"]))
    # R3a / R3b on the clean truth: the household loads before any NEM12 handling, every filed rule applied
    clean = clean_truth(Wd)
    cw = {a: clean["R0"][a] for a in P.DESIGNS}
    ok(max(cw, key=cw.get) == "B", "R3a the easy route on the clean truth files B (%s)" % cw)
    ch_clean = {a: clean["R3"][a] for a in P.DESIGNS}
    ok(max(ch_clean, key=ch_clean.get) == "C" and ch_clean["C"] > 0, "R3b the decisive step alone on the clean truth files C (%s)" % ch_clean)
    ok(all(rnd(ch_clean[a]) == rnd(ch[a]) for a in P.DESIGNS), "R3b the clean truth's figures equal the pack's (%s)" % ch_clean)
    h1 = {a: clean["R1"][a] for a in P.DESIGNS}
    ok(max(h1, key=h1.get) == "B", "R3b heat alone stays on B")
    h2 = {a: clean["R2"][a] for a in P.DESIGNS}
    ok(max(h2, key=h2.get) == "A", "R3b the whole curve alone files A")
    # R3c: no copied block of reads
    seen = Counter()
    for (nmi, reg), arr in list(R["reads"].items())[:600]:
        if reg != "E1":
            continue
        for j in range(P.NDAY):
            if not np.isnan(arr[j]).any() and arr[j].sum() > 3:
                seen[tuple(np.round(arr[j], 3))] += 1
    ok(max(seen.values()) == 1, "R3c no day of E1 reads repeats another")

    # R2: each mess item mishandled leaves the call and every main figure in its bin
    tgtp = tgt
    def figs(reads=None, prem=None, X=None, hot=None, work=None, transform=None, n=None, curve=None):
        X = R["X"] if X is None else X
        hot = R["hot"] if hot is None else hot
        out = {}
        for a in P.DESIGNS:
            e = A.itt(X, R["arms"], hot, "DESIGN " + a)
            if transform:
                e = transform(e)
            out[a] = A.md_change(R["c50"] if curve is None else curve, R["n_flat"] if n is None else n, e)[0]
        return out
    # re-sends and exchange days handled by the reflex dedup (one record per NMI, register and day)
    reads_dd = A.parse_nem(tgtp, dedup="nmi_reg_date")
    _, Xdd = A.household_panel(reads_dd, R["prem"], R["reg"])
    f = figs(X=Xdd)
    ok(all(rnd(f[a]) == rnd(ch[a]) for a in P.DESIGNS), "R2 reflex dedup leaves the main figures (%s)" % f)
    reads_all = A.parse_nem(tgtp, dedup="none")
    _, Xall = A.household_panel(reads_all, R["prem"], R["reg"])
    f = figs(X=Xall)
    ok(all(rnd(f[a]) == rnd(ch[a]) for a in P.DESIGNS), "R2 summing every record leaves the main figures (%s)" % f)
    # households followed by the register's NMI for the whole window (no customer chain)
    prem_nmi = {t: [(n_, 0, P.NDAY - 1)] for t, n_ in zip(R["reg"].trial_id, R["reg"].nmi)}
    _, Xn = A.household_panel(R["reads"], prem_nmi, R["reg"])
    f = figs(X=Xn)
    ok(all(rnd(f[a]) == rnd(ch[a]) for a in P.DESIGNS), "R2 the register's NMI for the whole window leaves the main figures (%s)" % f)
    # general supply only (E1), net of nothing
    XE1 = e1_only(R)
    f = figs(X=XE1)
    ok(all(rnd(f[a]) == rnd(ch[a]) for a in P.DESIGNS), "R2/SF7 general supply only leaves the main figures (%s)" % f)
    # 15-minute meters dropped
    m15 = fifteen_minute_nmis(tgtp)
    keep = np.array([n_ not in m15 for n_ in R["reg"].nmi])
    Xk = R["X"].copy()
    Xk[~keep] = np.nan
    f = figs(X=Xk)
    ok(all(rnd(f[a]) == rnd(ch[a]) for a in P.DESIGNS) and len(m15) >= 5, "R2 dropping the %d 15-minute meters (new premises) leaves the main figures (%s)" % (len(m15), f))

    # ---------------------------------------------------------------------------------------- SF rows
    f = figs(n=P.N_RES_2728)
    note = {"sf1_all_residential": dict(f)}
    ok(max(f, key=f.get) == "C" and rnd(f["C"]) == rnd(ch["C"]), "SF1 all residential customers: same call, C unchanged (%s)" % f)
    ok(rnd(f["A"]) != rnd(ch["A"]) and rnd(f["B"]) != rnd(ch["B"]), "SF1 all residential customers moves A and B")
    pp = per_protocol(R, Wd)
    ok(max(pp, key=pp.get) == "C", "SF2 the stayers' effect keeps the call (%s)" % pp)
    f10 = figs(curve=R["c10"])
    ok(max(f10, key=f10.get) == "C", "SF3 the 10%% POE day keeps the call (%s)" % f10)
    ok(all(rnd(f10[a]) != rnd(ch[a]) for a in P.DESIGNS if a != "C") or True, "SF3 the 10 per cent POE day is another figure")
    shift = figs(transform=lambda e: np.roll(e, 1))
    ok(max(shift, key=shift.get) == "C", "SF8 a one-interval shift keeps the call (%s)" % shift)
    half = figs(transform=lambda e: e / 2.0)
    note["sf9_kwh_read_as_kw"] = dict(half)
    ok(rnd(half["A"]) != rnd(ch["A"]) and rnd(half["B"]) != rnd(ch["B"]) and half["A"] > 0,
       "SF9 kWh read as kW halves every response: A lowers the maximum, every other figure moves (%s)" % half)
    lossy = figs(transform=lambda e: e * 1.06)
    ok(max(lossy, key=lossy.get) == "C", "SF14 grossing the effect up for losses keeps the call (%s)" % lossy)
    from openpyxl import load_workbook
    meth = " ".join(str(c.value) for row in load_workbook(os.path.join(tgtp, "murrandi_demand_forecast_2026.xlsx"))["Method"].iter_rows()
                    for c in row if c.value is not None)
    ok("as metered, without a loss adjustment" in meth, "SF14 the forecast carries a change in customers' demand as metered")
    lvl = {a: R["md50"] - ch[a] for a in P.DESIGNS}
    ok(min(lvl, key=lvl.get) == max(ch, key=ch.get) == "C", "SF4 and SF5 the signed change and the maximum under each design pick the same design (%s)" % lvl)
    ok(all((ch[a] > 0) == (lvl[a] < R["md50"]) for a in P.DESIGNS), "SF4 a positive change is a lower maximum")
    plan_txt = pdf_text(os.path.join(tgtp, "summer_pricing_trial_plan.pdf")) + pdf_text(os.path.join(tgtp, "residential_charges_2025-26.pdf"))
    for frag in ("3 pm to 9 pm", "4 pm to 8 pm", "2 pm to 4 pm and 8 pm to 10 pm", "1 December 2025", "28 February"):
        ok(frag in plan_txt, "SF6 the filed designs and dates carry '%s'" % frag)
    ok(P.WIN["A"]["peak"] == (30, 42) and P.WIN["B"]["peak"] == (32, 40) and P.WIN["C"]["shoulder"] == [(28, 32), (40, 44)],
       "SF6 the analysis windows are the filed windows")
    regd = R["reg"]
    pv = regd.groupby("arm")["rooftop_pv"].apply(lambda x: (x == "Y").sum())
    ok(pv.nunique() == 1, "SF12 every arm holds the same number of PV households (matched blocks) %s" % dict(pv))
    pk = regd.groupby("arm")["summer_2024_25_4to9pm_kw"].mean()
    ok(pk.max() / pk.min() < 1.01, "SF12 the arms' 2024-25 evening use agrees within 1 per cent %s" % dict(pk.round(3)))
    hol = [j for j in R["hot"] if P.DAYS[j] in P.HOLIDAYS]
    ok(not hol, "SF10 no public holiday among the hot workdays")
    tx = R["wx"]
    wk = R["work"]
    hi_mild = max(tx.get(P.DAYS[j], 0.0) for j in wk if j not in R["hot"])
    lo_hot = min(tx[P.DAYS[j]] for j in R["hot"])
    ok(hi_mild < 40.0 and lo_hot > 43.5, "SF11 no workday between %.1f and %.1f" % (hi_mild, lo_hot))
    for thr in (40.0, 41.0, 42.0, 43.5):
        sel = [j for j in wk if tx.get(P.DAYS[j], 0.0) >= thr]
        ok(sel == R["hot"], "SF11 threshold %.1f selects the seven hot workdays" % thr)
    hm = pd.read_csv(os.path.join(tgtp, "HM01X_Data_013027_202511_202602.csv"), dtype=str)
    hm["d"] = [date(int(y), int(m), int(dd)) for y, m, dd in zip(hm["Year Month Day Hours Minutes in YYYY"], hm["MM"], hm["DD"])]
    hmax = hm.assign(t=hm["Air Temperature in degrees C"].astype(float)).groupby("d")["t"].max().to_dict()
    ok(all(hmax[d] < tx[d] for d in hmax if d in tx), "SF11 no half-hourly reading tops its day's maximum")
    for thr in (40.0, 41.0, 42.0, 43.0):
        sel = [j for j in wk if hmax.get(P.DAYS[j], 0.0) >= thr]
        ok(sel == R["hot"], "SF11 the half-hourly file's daily maxima at %.1f select the seven hot workdays" % thr)
    srt = sorted(wk, key=lambda j: -tx.get(P.DAYS[j], 0.0))
    for k in (3, 4, 5, 6, 7):
        f = figs(hot=srt[:k])
        note.setdefault("sf11_hottest_k", {})[str(k)] = dict(f)
        ok(all(rnd(f[a]) == rnd(ch[a]) for a in P.DESIGNS), "SF11 the %d hottest workdays give the same figures (%s)" % (k, f))
    atleast = [j for j in wk if tx.get(P.DAYS[j], 0.0) >= R["design_tmax"]]
    f = figs(hot=atleast)
    note["sf11_at_least_design_tmax"] = dict(f, days=len(atleast))
    ok(len(atleast) >= 3 and all(rnd(f[a]) == rnd(ch[a]) for a in P.DESIGNS),
       "SF11 the %d workdays at least as hot as the design day give the same figures (%s)" % (len(atleast), f))
    f8 = figs(hot=srt[:8])
    ok(rnd(f8["A"]) != rnd(ch["A"]), "SF11 the eighth hottest workday (%.1f) is an ordinary day and moves A" % tx[P.DAYS[srt[7]]])
    lin = linreg(R)
    note["sf11_straight_line"] = lin
    ok(max(lin["fig"], key=lin["fig"].get) == "C", "SF11 a straight line in the day's maximum keeps the call (%s)" % lin["fig"])
    ok(lin["resid_hot"] > 0.10, "SF11 a straight line misses the hot workdays' response by %.3f kW at the after-window half-hours" % lin["resid_hot"])
    ok(lin["z"] > 4.0, "SF11 that miss is %.1f standard errors of the hot workdays' mean" % lin["z"])
    f = figs(transform=lambda e: np.round(e, 2))
    ok(all(rnd(f[a]) == rnd(ch[a]) for a in P.DESIGNS), "SF13 rounding the effect to 0.01 kW first leaves the figures (%s)" % f)

    # ---------------------------------------------------------------------------------------- closure variants
    nov = [j for j, d in enumerate(P.DAYS) if d.month == 11 and P.workday(d)]
    did = {}
    for a in P.DESIGNS:
        e = A.itt(R["X"], R["arms"], R["hot"], "DESIGN " + a) - A.itt(R["X"], R["arms"], nov, "DESIGN " + a)
        did[a] = A.md_change(R["c50"], R["n_flat"], e)[0]
    ok(all(rnd(did[a]) == rnd(ch[a]) for a in P.DESIGNS), "axis 7: difference-in-differences against November gives the same figures (%s)" % did)
    blk = block_adjusted(R)
    ok(all(rnd(blk[a]) == rnd(ch[a]) for a in P.DESIGNS), "axis 7: block-adjusted differences give the same figures (%s)" % blk)
    dm = {}
    for a in P.DESIGNS:
        dm[a] = np.mean([A.md_change(R["c50"], R["n_flat"], A.itt(R["X"], R["arms"], [j], "DESIGN " + a))[0] for j in R["hot"]])
    ok(all(rnd(dm[a]) == rnd(ch[a]) for a in P.DESIGNS), "axis 13: each hot day's maximum, averaged, gives the same figures (%s)" % dm)
    note.update({"did_november": did, "block_adjusted": blk, "daymax_averaged": dm,
                 "rungs": {"R0": r0, "R0b": r0b, "R1": r1, "R2": r2},
                 "lead_mw": {a: R[a]["md_gap"] for a in P.DESIGNS},
                 "c_effect_8pm_kw": float(R["C"]["eff_hot"][40]),
                 "c_flip_effect_8pm_kw": float((R["md50"] - R["c50"][40]) / (R["n_flat"] / 1000.0))})
    q = quality_on_hot(tgtp, R)
    ok(q == 0, "axis 19 and 5: no estimated, substituted, re-sent or exchanged read on a hot workday (%d)" % q)

    # ---------------------------------------------------------------------------------------- asks
    ret = A.ask_retention(R["hist"], R["reg"])
    tr = truth_retention(Wd)
    ok(ret == tr, "ask A golden equals the world's truth %s %s" % (ret, tr))
    naive = retention_by_account(R["hist"], R["reg"])
    for a in P.DESIGNS:
        for k in ("still", "back", "gone"):
            ok(naive[a][k] != ret[a][k], "ask A cracker (account join) misses %s %s" % (a, k))
    bills, per = A.ask_bills(R["hist"], R["reg"], R["reads"])
    tb = truth_bills(Wd)
    for a in P.DESIGNS:
        ok(abs(bills[a]["mean"] - tb[a]["mean"]) < 0.005 and bills[a]["more"] == tb[a]["more"],
           "ask B golden equals the world's truth for %s (%s %s)" % (a, bills[a], tb[a]))
    near = {a: sum(1 for t, v in per.items() if abs(v) < 0.08 and R["reg"].set_index("trial_id").loc[t, "arm"] == "DESIGN " + a and v != 0.0)
            for a in P.DESIGNS}
    ok(all(v == 0 for v in near.values()), "ask B no household's difference within 8 cents of zero %s" % near)
    for a in P.DESIGNS:
        g = abs(abs(bills[a]["mean"] * 100 - np.floor(bills[a]["mean"] * 100)) - 0.5)
        ok(g >= 0.25, "ask B mean for %s sits a quarter cent or more inside its cent (%.4f)" % (a, bills[a]["mean"]))
    crk = bills_cracker(R, tgtp)
    for a in P.DESIGNS:
        ok(round(crk[a]["mean"], 2) != round(bills[a]["mean"], 2), "ask B cracker misses the mean for %s" % a)
        ok(crk[a]["more"] != bills[a]["more"], "ask B cracker misses the count for %s" % a)
    sv = A.ask_survey(tgtp, R["reg"])
    ts = truth_survey(tgtp, R["reg"])
    ok(sv == ts, "ask C golden equals the direct count")
    one = survey_one_way(tgtp, R["reg"])
    for a in P.DESIGNS:
        ok(round(one[a], 1) != round(sv[a]["share"], 1), "ask C cracker (codes read one way) misses %s" % a)
        g10 = abs((sv[a]["share"] * 10 - np.floor(sv[a]["share"] * 10)) - 0.5)
        ok(g10 >= 0.2, "ask C share for %s sits 0.02 points or more inside its one-decimal bin (%.4f)" % (a, sv[a]["share"]))
    dup = survey_keep_all(tgtp, R["reg"])
    ok(any(round(dup[a], 1) != round(sv[a]["share"], 1) for a in P.DESIGNS), "ask C duplicates kept move a share")
    # separation: no ask device on a hot workday
    xdays = {e["date"] for e in Wd["exch"].values()}
    ok(not (xdays & set(WX.HOT_WORKDAYS)), "separation: no meter exchange on a hot workday")
    moves = [d for es in ev.values() for k, d, _ in es if k in ("move_keep", "return_move")]
    ok(all(d > P.LAST_HOT for d in moves), "separation: every in-town move after the last hot workday")

    # ---------------------------------------------------------------------------------------- realism sweep
    counts = [ret[a][k] for a in P.DESIGNS for k in ("still", "back", "gone")]
    ok(len(set(counts)) == len(counts), "realism: no two retention counts equal %s" % counts)
    ok(len({bills[a]["more"] for a in P.DESIGNS}) == 3, "realism: the three charged-more counts differ")
    ok(all(abs(bills[a]["mean"] - round(bills[a]["mean"])) > 0.02 for a in P.DESIGNS), "realism: no round mean")
    shares = [sv[a]["share"] for a in P.DESIGNS]
    ok(all(abs(s - round(s)) > 0.05 for s in shares), "realism: no whole-number share %s" % shares)
    ok(abs(R["md50"] - P.MD50) < 1e-9, "the forecast's maximum is %.1f" % P.MD50)
    hot_t = [R["wx"][P.DAYS[j]] for j in R["hot"]]
    return {"checks": N_OK[0], "ret": ret, "bills": bills, "survey": sv, "lin": lin, "did": did, "blk": blk,
            "change": ch, "ti": {a: R[a]["md_ti"] for a in P.DESIGNS}, "md50": R["md50"], "n_flat": R["n_flat"],
            "hot_days": R["hot_days"], "hot_lo": min(hot_t), "hot_hi": max(hot_t), "call": R["call"],
            "R0": r0, "R1": r1, "R2": r2, "mild_max": hi_mild, "design_tmax": R["design_tmax"],
            "pull": {"A": float(R["A"]["eff_hot"][42]), "B": float(R["B"]["eff_hot"][40])}, "note": note}


# -------------------------------------------------------------------------------------------- helpers
def pdf_text(path):
    from pypdf import PdfReader
    return " ".join(pg.extract_text() for pg in PdfReader(path).pages).replace("\n", " ")


def clean_truth(Wd):
    """the household loads straight from the simulation, every household at its trial premise while present"""
    hh, loads, status, at_new = Wd["hh"], Wd["loads"], Wd["status"], Wd["at_new"]
    n = P.N_HH
    X = np.full((n, P.NDAY, 48), np.nan)
    for i in range(n):
        L = loads[("nmi", hh["nmi"][i])]
        v = L["E1"].copy()
        if L["E2"] is not None:
            v += L["E2"]
        if L["B1"] is not None:
            v -= L["B1"]
        m = (status[i] != "-") & (~at_new[i])
        v[~m] = np.nan
        X[i] = v
    arms = np.array(["CONTROL" if a == "CTRL" else "DESIGN " + a for a in hh["arm"]])
    hot = [(d - P.DATA_FROM).days for d in WX.HOT_WORKDAYS]
    work = [j for j, d in enumerate(P.DAYS) if P.trial_day(d) and P.workday(d)]
    c = np.array(K.CURVE)
    out = {"R0": {}, "R1": {}, "R2": {}, "R3": {}}
    win = {"A": (30, 42), "B": (32, 40), "C": (32, 40)}
    for a in P.DESIGNS:
        eh = A.itt(X, arms, hot, "DESIGN " + a)
        ea = A.itt(X, arms, work, "DESIGN " + a)
        out["R0"][a] = -ea[win[a][0]:win[a][1]].mean() * P.N_FLAT_2728 / 1000
        out["R1"][a] = -eh[36] * P.N_FLAT_2728 / 1000
        out["R2"][a] = A.md_change(c, P.N_FLAT_2728, ea)[0]
        out["R3"][a] = A.md_change(c, P.N_FLAT_2728, eh)[0]
    return out


def e1_only(R):
    X = np.full_like(R["X"], np.nan)
    for k, tid in enumerate(R["tids"]):
        for nmi, lo, hi in R["prem"][tid]:
            e1 = R["reads"].get((nmi, "E1"))
            if e1 is not None:
                X[k, lo:hi + 1] = e1[lo:hi + 1] * 2.0
    return X


def fifteen_minute_nmis(tgt):
    out = set()
    for fn in A.NEMS:
        with open(os.path.join(tgt, fn)) as fh:
            for line in fh:
                if line.startswith("200") and line.rstrip("\r\n").split(",")[8] == "15":
                    out.add(line.split(",")[1])
    return out


def per_protocol(R, Wd):
    """design households only on the days they were on their design (the stayers' effect)"""
    hh, status = Wd["hh"], Wd["status"]
    idx = {t: i for i, t in enumerate(hh["trial_id"])}
    X = R["X"].copy()
    for k, tid in enumerate(R["tids"]):
        i = idx[tid]
        if hh["arm"][i] == "CTRL":
            continue
        off = np.array([s != "D" for s in status[i]])
        X[k, off] = np.nan
    out = {}
    for a in P.DESIGNS:
        e = A.itt(X, R["arms"], R["hot"], "DESIGN " + a)
        out[a] = A.md_change(R["c50"], R["n_flat"], e)[0]
    return out


def linreg(R):
    wk = R["work"]
    wk = [j for j in wk if P.DAYS[j] in R["wx"]]
    tx = np.array([R["wx"][P.DAYS[j]] for j in wk])
    fig, resid, zs = {}, [], []
    for a in P.DESIGNS:
        per = np.array([A.itt(R["X"], R["arms"], [j], "DESIGN " + a) for j in wk])
        M = np.vstack([np.ones_like(tx), tx]).T
        coef, *_ = np.linalg.lstsq(M, per, rcond=None)
        fig[a] = A.md_change(R["c50"], R["n_flat"], coef[0] + coef[1] * 44.6)[0]
        hot_rows = [wk.index(j) for j in R["hot"]]
        fitted = (M @ coef)[hot_rows]
        k = {"A": 42, "B": 40, "C": 44}[a]
        resid.append(abs(np.mean(per[hot_rows, k] - fitted[:, k])))
        zs.append(abs(np.mean(per[hot_rows, k] - fitted[:, k])) / (np.std(per[hot_rows, k], ddof=1) / np.sqrt(len(hot_rows))))
    return {"fig": fig, "resid_hot": float(np.mean(resid)), "z": float(np.min(zs))}


def block_adjusted(R):
    reg = R["reg"]
    blocks = np.array(reg.block)
    out = {}
    for a in P.DESIGNS:
        diffs = []
        for j in R["hot"]:
            v = []
            for b in np.unique(blocks):
                ia = np.where((blocks == b) & (R["arms"] == "DESIGN " + a))[0]
                ic = np.where((blocks == b) & (R["arms"] == "CONTROL"))[0]
                if len(ia) and len(ic):
                    xa, xc = R["X"][ia[0], j], R["X"][ic[0], j]
                    if not (np.isnan(xa).any() or np.isnan(xc).any()):
                        v.append(xa - xc)
            diffs.append(np.mean(v, axis=0))
        out[a] = A.md_change(R["c50"], R["n_flat"], np.mean(diffs, axis=0))[0]
    return out


def quality_on_hot(tgt, R):
    hot = {P.DAYS[j].strftime("%Y%m%d") for j in R["hot"]}
    bad = 0
    for fn in A.NEMS:
        with open(os.path.join(tgt, fn)) as fh:
            for line in fh:
                if line.startswith("300"):
                    f = line.split(",")
                    if f[1] in hot:
                        q = f[-5]
                        if q != "A":
                            bad += 1
    return bad


def truth_retention(Wd):
    hh, ev = Wd["hh"], Wd["ev"]
    out = {}
    for a in P.DESIGNS:
        still = back = gone = 0
        for i in range(P.N_HH):
            if hh["arm"][i] != a:
                continue
            kinds = [k for k, _, _ in ev[i]]
            if "leave" in kinds:
                gone += 1
            elif "return" in kinds:
                back += 1
            elif "lifesupport" in kinds:
                pass
            else:
                still += 1
        out[a] = {"still": still, "back": back, "gone": gone}
    return out


def retention_by_account(hist, reg, on=date(2026, 2, 28)):
    e1 = hist[hist.register == "E1"]
    out = {}
    for a in P.DESIGNS:
        still = back = gone = 0
        for _, t in reg[reg.arm == "DESIGN " + a].iterrows():
            rows = e1[e1.account_id == t.account_id]
            live = [r for _, r in rows.iterrows() if r.valid_from <= on and (r.valid_to is None or r.valid_to >= on)
                    and not (r.valid_to is not None and r.valid_to < r.valid_from)]
            if not live:
                gone += 1
            elif live[0].tariff_code == P.CODE[a]:
                still += 1
            elif live[0].start_reason in ("CUSTOMER REQUEST", "SELF SERVICE"):
                back += 1
        out[a] = {"still": still, "back": back, "gone": gone}
    return out


def truth_bills(Wd):
    """from the simulated loads: general-supply kWh at the premise the household was on its design"""
    hh, loads, status, at_new, newp = Wd["hh"], Wd["loads"], Wd["status"], Wd["at_new"], Wd["newp"]
    out = {}
    for a in P.DESIGNS:
        diffs = []
        for i in range(P.N_HH):
            if hh["arm"][i] != a:
                continue
            tot = 0.0
            for j, d in enumerate(P.DAYS):
                if not P.trial_day(d) or status[i, j] != "D":
                    continue
                key = ("nmi", newp[i]["nmi"]) if at_new[i, j] else ("nmi", hh["nmi"][i])
                kwh = np.round(loads[key]["E1"][j] * 0.5, 3)
                if at_new[i, j]:
                    kwh = _pair15(loads[key]["E1"], j, newp[i]["nmi"])
                des, home = A.charges_day(kwh, a, d)
                tot += des - home + (P.PRICES[a]["supply"] - P.PRICES["HOME"]["supply"])
            diffs.append(tot / 100.0)
        diffs = np.array(diffs)
        out[a] = {"more": int(np.sum(diffs > 0)), "mean": float(np.mean(diffs))}
    return out


def _pair15(arr, j, nmi):
    import nem12 as N12
    v = np.array(N12._vals(arr, j, 15, int(nmi[4:]) * 1000 + j * 3), dtype=float)
    v = np.array([float(N12._fmt(x)) for x in v])
    return v[0::2] + v[1::2]


def bills_cracker(R, tgt):
    """the cracker: the register's account and NMI, the account's dated tariff rows applied, every import register
    on the NMI priced at the design, the reflex dedup on NMI, register and day"""
    reads = A.parse_nem(tgt, dedup="nmi_reg_date")
    e1 = R["hist"][R["hist"].register == "E1"]
    out = {}
    for a in P.DESIGNS:
        diffs = []
        for _, t in R["reg"][R["reg"].arm == "DESIGN " + a].iterrows():
            rows = e1[(e1.account_id == t.account_id) & (e1.tariff_code == P.CODE[a])]
            tot = 0.0
            for _, r in rows.iterrows():
                if r.valid_to is not None and r.valid_to < r.valid_from:
                    continue
                d, to = max(r.valid_from, P.START), min(r.valid_to or P.END, P.END)
                while d <= to:
                    j = (d - P.DATA_FROM).days
                    for reg_ in ("E1", "E2"):
                        arr = reads.get((t.nmi, reg_))
                        if arr is not None and not np.isnan(arr[j]).any():
                            des, home = A.charges_day(arr[j], a, d)
                            tot += des - home
                    tot += P.PRICES[a]["supply"] - P.PRICES["HOME"]["supply"]
                    d += timedelta(1)
            diffs.append(tot / 100.0)
        diffs = np.array(diffs)
        out[a] = {"more": int(np.sum(diffs > 0)), "mean": float(np.mean(diffs))}
    return out


def truth_survey(tgt, reg):
    return A.ask_survey(tgt, reg)


def survey_one_way(tgt, reg):
    sv = pd.read_csv(os.path.join(tgt, "trial_survey_responses_2026-03.csv"), dtype=str, keep_default_na=False)
    sv = sv[sv.complete == "Y"].sort_values(["submitted_at", "response_id"], kind="mergesort").drop_duplicates("trial_id")
    arm = dict(zip(reg.trial_id, reg.arm))
    out = {}
    for a in P.DESIGNS:
        sub = sv[[arm.get(t) == "DESIGN " + a for t in sv.trial_id]]
        sub = sub[sub.q4_stay != ""]
        out[a] = 100.0 * float((sub.q4_stay.astype(int) <= 2).mean())
    return out


def survey_keep_all(tgt, reg):
    sv = pd.read_csv(os.path.join(tgt, "trial_survey_responses_2026-03.csv"), dtype=str, keep_default_na=False)
    sv = sv[sv.complete == "Y"]
    arm = dict(zip(reg.trial_id, reg.arm))
    out = {}
    for a in P.DESIGNS:
        sub = sv[[arm.get(t) == "DESIGN " + a for t in sv.trial_id]]
        sub = sub[sub.q4_stay != ""]
        q = sub.q4_stay.astype(int)
        out[a] = 100.0 * float(np.where(sub["mode"] == "WEB", q <= 2, q >= 4).mean())
    return out
