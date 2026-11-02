"""task154's assertions, run on every build: the input gates, the three rules on the clean truth, every semantic
fork, the ladder, the asks' devices and their literal readings, every graded figure's bin, the realism sweep and the
leak hygiene of the pack. Any failure stops the build."""
from __future__ import annotations

import csv
import datetime as dt
import json
import math
import os
import re
import zipfile

import numpy as np

import calc as C
import common as K
import deliver as DL
import docs as D
import records as R
import world as W

RESULTS = []


def check(label, ok, detail=""):
    RESULTS.append((label, bool(ok), detail))
    if not ok:
        print("FAIL  %s  %s" % (label, detail))


def pdf_text(path):
    from pypdf import PdfReader
    return "\n".join(p.extract_text() or "" for p in PdfReader(path).pages)


def docx_text(path):
    import docx
    return "\n".join(p.text for p in docx.Document(path).paragraphs)


def edge(v, unit):
    return unit / 2.0 - abs(v - round(v / unit) * unit)


def run(target, golden, Bt):
    RESULTS.clear()
    b = Bt.bundle
    res = Bt.res
    figs = Bt.figs
    mc = res["mc"]
    T, S, img, prot = mc["T"], mc["S"], mc["img"], mc["prot"]
    files = sorted(os.listdir(target))
    meta = json.load(open(os.path.join(os.path.dirname(target), "metadata.json")))

    # ---------------------------------------------------------------------------------------------- input gates
    check("gate: 10 or more files", len(files) >= 10, "%d" % len(files))
    fmts = {f.rsplit(".", 1)[-1] for f in files}
    check("gate: 3 or more formats", len(fmts) >= 3, ", ".join(sorted(fmts)))
    big = max(meta["files"], key=lambda e: e.get("rows", 0))
    check("gate: a file of 25,000 rows or more", big.get("rows", 0) >= 25000, "%s %s" % (big["path"], big.get("rows")))
    check("gate: two or more distractors named in metadata", len(meta["distractor_files"]) >= 2
          and all(d in files for d in meta["distractor_files"]), str(meta["distractor_files"]))
    check("gate: every file has source, date and licence", all(e.get("source") and e.get("date") and e.get("license")
                                                                for e in meta["files"]) and len(meta["files"]) == len(files))
    bad = [f for f in files if re.search(r"readme|dictionary|manifest|notes|codebook|schema|definitions|distractor", f, re.I)]
    check("gate: no file describes the data by name", not bad, str(bad))
    import openpyxl
    sheets = []
    for f in files:
        if f.endswith(".xlsx"):
            sheets += [s for s in openpyxl.load_workbook(os.path.join(target, f), read_only=True).sheetnames]
    check("gate: no sheet describes the data", not [s for s in sheets if re.search(r"readme|notes|dictionary|about|key", s, re.I)],
          str(sheets[:12]))

    # ---------------------------------------------------------------------------------------------- the main call
    check("call: largest passing quantity 1,300", figs["call_largest_m3d"] == 1300, str(figs["call_largest_m3d"]))
    check("call: limiting borehole Lower Hay Farm", mc["worst"] == "Lower Hay Farm", mc["worst"])
    check("call: 1,800 fails at every protected borehole", all(mc["at1800"][n] > av for n, _, av in prot))
    check("SF1 round and floor of the continuous limit agree", C.largest_passing_round(mc["golden"]) ==
          C.nearest(mc["golden"], 100.0) == 1300.0, "%.1f" % mc["golden"])
    check("bin: continuous limit clear of both edges of 1,300", 1310.0 <= mc["golden"] <= 1345.0, "%.1f" % mc["golden"])
    for n, _, av in prot:
        v = mc["at1800"][n]
        check("bin: %s drawdown at 1,800 mid-bin in whole metres" % n, edge(v, 1.0) >= 0.38, "%.3f" % v)

    # the golden family: every defensible estimate of T and S from the test, and the long record refitted with the
    # barrier, files the same quantity, the same limit and the same whole-metre drawdowns
    fam = {}
    for name, kw in (("joint Theis", {}), ("OB1 alone", dict(obs=("OB1",))), ("OB2 alone", dict(obs=("OB2",))),
                     ("OB3 alone", dict(obs=("OB3",))), ("late half", dict(t_from=2160.0)),
                     ("first day", dict(t_to=1440.0)), ("nominal 25.0 l/s", dict(q=2160.0)),
                     ("Cooper-Jacob", dict(cj=True)), ("OB1 and OB2 (OB3 set aside)", dict(obs=("OB1", "OB2")))):
        Tf, Sf = C.fit_theis(b, **kw)
        g = C.largest(prot, Tf, Sf, img)
        dd = {n: C.nearest(C.assessment(K.APPLIED_QD, xy, Tf, Sf, img), 1.0) for n, xy, _ in prot}
        fam[name] = (Tf, Sf, g[0], g[1], dd)
    for name, (Tf, Sf, gq, gw, dd) in fam.items():
        check("SF2 golden family, %s: 1,300 at Lower Hay Farm" % name,
              C.nearest(gq, 100.0) == 1300.0 and C.largest_passing_round(gq) == 1300.0 and gw == "Lower Hay Farm",
              "T %.1f S %.3e limit %.1f %s" % (Tf, Sf, gq, gw))
        check("SF3 golden family, %s: drawdowns at 1,800 unchanged" % name,
              all(dd[n] == res["at1800"][n] for n in dd), str(dd))
    check("component: T rounds to the same whole number across the test fits",
          len({int(round(v[0])) for k, v in fam.items() if k != "Cooper-Jacob"}) <= 2,
          str(sorted({round(v[0], 1) for v in fam.values()})))

    # the long record: the barrier model fits to the noise, the unbounded one does not, and the fitted barrier is
    # fully sealing; no stabilisation (no leakage) over eleven years
    v = res["verdict"]
    check("SF4 long record: closed aquifer fits to the noise", v["closed by the fault, test T and S"] < 0.04,
          "%.4f" % v["closed by the fault, test T and S"])
    check("SF4 long record: unbounded aquifer misfits by more than ten times", v["unbounded, test T and S"] >
          10 * v["closed by the fault, test T and S"], "%.4f" % v["unbounded, test T and S"])
    n_lr = 3 * len(C.ob_levels(b)["OB1"])
    lr = n_lr * math.log((v["unbounded, refitted to the long record"] / v["closed by the fault, test T and S"]) ** 2)
    check("SF4 long record: an unbounded refit, with T and S free, still misfits the closed aquifer (likelihood ratio "
          "over 100)", lr > 100.0 and v["unbounded, refitted to the long record"] > 1.5 * v["closed by the fault, test T and S"],
          "%.4f against %.4f, ratio %.1f" % (v["unbounded, refitted to the long record"],
                                            v["closed by the fault, test T and S"], lr))
    Ta, Sa = res["apparent"]
    check("SF4 long record: the unbounded refit needs a transmissivity the test refutes", Ta < 0.7 * T, "%.1f" % Ta)
    check("SF5 the fault is fully sealing: fitted coefficient within 2 per cent of one",
          abs(v["fault coefficient fitted"] - 1.0) < 0.02, "%.4f" % v["fault coefficient fitted"])
    rm = C.rmb_monthly(b)
    ks = sorted(rm)
    span = [k for k in ks if k >= (2015, 4)]
    trend = np.polyfit(np.arange(len(span)), [rm[k] for k in span], 1)[0] * 12
    monthly = C.abstraction_history(b)
    th_rmb = C.model_series(C.local_xy(b, "Windle Cross OBH") if "Windle Cross OBH" in b.survey
                            else (K.RMB["xy"]), [(2026, 3)], monthly, T, S)[0]
    th_rmb_refit = C.model_series(K.RMB["xy"], [(2026, 3)], monthly, Ta, Sa)[0]
    check("SF5 Windle Cross: no response where either unbounded model expects metres",
          abs(trend * 11) < 0.25 and th_rmb > 1.5 and th_rmb_refit > 1.5,
          "regional trend %.3f m/yr, unbounded expectation %.2f m (test) and %.2f m (refit)" % (trend, th_rmb, th_rmb_refit))
    # Windle Cross's flagged days (estimated infills, suspect readings, the unchecked latest weeks) dropped or kept:
    # the long record's misfits round the same and the closed aquifer still fits best
    orig_rmb = C.rmb_monthly
    for drop in (("Suspect",), ("Suspect", "Estimated", "Unchecked")):
        def _rmb(bb, drop=drop):
            acc_ = {}
            for r_ in bb.rmb:
                if r_["Quality"] in drop:
                    continue
                d_ = dt.datetime.strptime(r_["Date"], "%d/%m/%Y").date()
                acc_.setdefault((d_.year, d_.month), []).append(float(r_["Level (mAOD)"]))
            return {k_: float(np.mean(v_)) for k_, v_ in acc_.items()}
        C.rmb_monthly = _rmb
        try:
            vq, _, _ = C.long_record_verdict(b, T, S, img)
        finally:
            C.rmb_monthly = orig_rmb
        check("SF5 Windle Cross with its %s days left out: the long record's misfits round the same" % " and ".join(
              x.lower() for x in drop), round(vq["closed by the fault, test T and S"], 2) == figs["rms_closed_m"] and
              round(vq["unbounded, test T and S"], 2) == figs["rms_unbounded_m"] and
              vq["closed by the fault, test T and S"] < vq["unbounded, refitted to the long record"],
              "%.4f %.4f" % (vq["closed by the fault, test T and S"], vq["unbounded, test T and S"]))
    quals = {}
    for r_ in b.rmb:
        quals[r_["Quality"]] = quals.get(r_["Quality"], 0) + 1
    check("realism: Windle Cross carries its station's quality flags", set(quals) == {"Good", "Estimated", "Suspect",
                                                                                     "Unchecked"}, str(quals))
    # leakage: the unbounded model's residual against log time keeps steepening rather than flattening
    lv = C.ob_levels(b)
    ob1 = [lv["OB1"][k] - (rm[k] - rm[(2015, 4)]) for k in sorted(lv["OB1"]) if k in rm]
    early, late = np.mean(ob1[12:24]) - np.mean(ob1[0:12]), np.mean(ob1[-12:]) - np.mean(ob1[-24:-12])
    check("SF6 no leakage: OB1 still falling in the last year of the record", late < -0.05, "first-year %.2f, last %.2f" %
          (early, late))

    # ---------------------------------------------------------------------------------------------- three rules
    # R1: the field's raw material ships, and no column holds the deciding quantity
    tm, sd = C.test_drawdowns(b, "OB1")
    check("R1 raw material: minute-level test drawdowns at every observation borehole",
          all(len(C.test_drawdowns(b, ob)[0]) >= 8000 for ob in ("OB1", "OB2", "OB3")))
    heads = []
    for f in files:
        p = os.path.join(target, f)
        if f.endswith(".csv"):
            heads += next(csv.reader(open(p, encoding="utf-8")))
    check("R1 no column holds the deciding quantity", not [h for h in heads if re.search(r"drawdown|image|boundary|barrier|"
                                                                                        r"predict|transmiss", h, re.I)],
          str([h for h in heads if re.search(r"drawdown|predict", h, re.I)]))
    # R2: mess items neutral on the call and the components
    T12, S12 = C.fit_theis(b, obs=("OB1", "OB2"))
    check("R2 OB3's pressure logger set aside: call unchanged", C.nearest(C.largest(prot, T12, S12, img)[0], 100.0) == 1300.0)
    b2 = C.Bundle()
    b2.__dict__.update(b.__dict__)
    t3, l3 = b.test["OB3"]
    b2.test = dict(b.test)
    b2.test["OB3"] = ([x + dt.timedelta(hours=1) for x in t3], l3)      # OB3's BST clock read as UTC
    Tm, Sm = C.fit_theis(b2)
    check("R2 OB3's local clock read as UTC: call unchanged", C.nearest(C.largest(prot, Tm, Sm, img)[0], 100.0) == 1300.0
          and C.largest(prot, Tm, Sm, img)[1] == "Lower Hay Farm", "T %.1f" % Tm)
    b3 = C.Bundle()
    b3.__dict__.update(b.__dict__)
    b3.test = dict(b.test)
    b3.test["OB3"] = (t3, l3 * 9.80665)                                   # OB3's kPa read as metres
    T3k = C.fit_theis(b3, obs=("OB3",))[0]
    check("R2 OB3's kPa read as metres is visible, not silent: its own T is a tenth of OB1's", T3k < 0.15 * fam["OB1 alone"][0],
          "%.1f against %.1f" % (T3k, fam["OB1 alone"][0]))
    check("R2 with kPa converted, OB3's own T agrees with OB1's", abs(math.log(fam["OB1 alone"][0] / fam["OB3 alone"][0])) < 0.02)
    # the OB2 casing raise mishandled (every month from March 2020 read from the old casing top): visible as a step at
    # OB2 alone, and the long record still chooses the aquifer the fault closes
    orig_levels = C.ob_levels

    def _old_casing(bb):
        out_ = orig_levels(bb)
        for k_ in list(out_["OB2"]):
            if k_ >= (2020, 3):
                out_["OB2"][k_] -= K.OB2_RAISE_M
        return out_
    C.ob_levels = _old_casing
    try:
        vm, _, months_m = C.long_record_verdict(b, T, S, img)
        lv_m = C.ob_levels(b)
    finally:
        C.ob_levels = orig_levels
    rm_ = C.rmb_monthly(b)
    steps = {}
    for ob in ("OB1", "OB2", "OB3"):
        pre = [lv_m[ob][k_] - rm_[k_] for k_ in months_m if (2019, 3) <= k_ <= (2020, 2)]
        post = [lv_m[ob][k_] - rm_[k_] for k_ in months_m if (2020, 3) <= k_ <= (2021, 2)]
        steps[ob] = float(np.mean(post) - np.mean(pre))
    check("R2 OB2's raised casing mishandled is visible: OB2 steps down about 0.45 m more than OB1 and OB3 that year",
          steps["OB2"] - 0.5 * (steps["OB1"] + steps["OB3"]) < -0.35, str({k_: round(v_, 2) for k_, v_ in steps.items()}))
    best_m = min((v_, k_) for k_, v_ in vm.items() if k_ != "fault coefficient fitted")
    check("R2 OB2's raised casing mishandled: the long record still chooses the aquifer the fault closes",
          best_m[1].startswith("closed") and vm["closed by the fault, test T and S"] < vm["unbounded, refitted to the long record"]
          and vm["closed by the fault, test T and S"] < vm["unbounded, test T and S"] / 2.5,
          str({k_: round(v_, 3) for k_, v_ in vm.items()}))
    # R3a: the default path on the clean truth files the named wrong answer
    th = C.largest(prot, T, S, None)
    check("R3a analyst test: Theis on the test files about 2,600 with Kilnbrook Nurseries limiting",
          C.nearest(th[0], 100.0) == 2600.0 and th[1] == "Kilnbrook Nurseries", "%.1f %s" % (th[0], th[1]))
    truth = W.largest_quantity(image=False)
    check("R3a on the world's clean truth (generator T and S): the same wrong answer", C.nearest(truth[0], 100.0) == 2600.0
          and truth[1] == "Kilnbrook Nurseries", "%.1f" % truth[0])
    # R3b: only the decisive step reaches the golden
    check("R3b the easy route with only the barrier added files the golden", C.nearest(mc["golden"], 100.0) == 1300.0)
    apparent = C.largest(prot, Ta, Sa, None)
    check("R3b rung: an unbounded aquifer refitted to the long record stays wrong", C.nearest(apparent[0], 100.0) not in
          (1300.0,) and apparent[1] == "Kilnbrook Nurseries", "%.1f %s" % apparent[:2])
    for f in (1.40, 1.49, 1.54, 1.65):
        sc = C.largest(prot, T, S, None, 1.0, f)
        check("R3b rung: Theis scaled by %.2f stays wrong" % f, C.nearest(sc[0], 100.0) != 1300.0 and sc[1] ==
              "Kilnbrook Nurseries", "%.1f %s" % sc[:2])
    for cf in (0.5, 0.8):
        pb = C.largest(prot, T, S, img, cf)
        check("R3b rung: a fault sealing %d per cent stays wrong" % int(cf * 100), C.nearest(pb[0], 100.0) != 1300.0,
              "%.1f %s" % pb[:2])
    # R3c: no plant: no repeated block in any numeric series, no decoy document, no figure that ranks quantities
    tel = [float(r["fm1_flow_ls"]) for r in b.telem]
    rep = 0
    for i in range(0, len(tel) - 2 * 96, 96 * 7):
        if tel[i:i + 96] == tel[i + 96 * 7:i + 96 * 8] and sum(tel[i:i + 96]) > 0:
            rep += 1
    check("R3c no copied block in FM-1's series", rep == 0, str(rep))
    seqs = {}
    for r in b.obs:
        seqs.setdefault(r["borehole"], []).append(r["mean_depth_to_water_m_btoc"])
    runs6 = [tuple(v_[i:i + 6]) for v_ in seqs.values() for i in range(len(v_) - 5)]
    check("R3c no copied block in the long record: no six months of levels repeat, within or across boreholes",
          len(set(runs6)) == len(runs6), "%d of %d distinct" % (len(set(runs6)), len(runs6)))
    letter = pdf_text(os.path.join(target, D.F_LETTER))
    check("R3c no document states a quantity a protected borehole allows or an aquifer model",
          not re.search(r"Theis|transmissiv|storage coefficient|image|boundary|barrier|1,300|2,600|largest daily quantity "
                        r"of", letter))

    # ---------------------------------------------------------------------------------------------- forks
    check("SF7 drawdown datum: the letter files the April 2015 rest level", "measured from its rest water level in April 2015"
          in letter.replace("\n", " "))
    check("SF8 pumping basis: the letter files 1,200 from 1 April 2015 and the applied quantity from 1 April 2027",
          "1,200 cubic metres a day from 1 April 2015 to 31 March 2027" in letter.replace("\n", " ") and
          "from 1 April 2027 to 31 March 2039" in letter.replace("\n", " "))
    for off in (-1.0, 1.0):
        t_tot = ((K.COMMON_END + dt.timedelta(days=1)) - K.LICENCE_START).days + off
        t_new = ((K.COMMON_END + dt.timedelta(days=1)) - K.NEW_FROM).days + off

        def a(q, xy):
            return float(K.LICENSED_QD * C.resp(xy, t_tot, T, S, img)[0] + (q - K.LICENSED_QD) * C.resp(xy, t_new, T, S, img)[0])
        from scipy.optimize import brentq
        q = min(brentq(lambda q: a(q, xy) - av, -5e4, 5e5) for n, xy, av in prot)
        check("SF9 a day either way on the term moves nothing (offset %+d)" % off, C.nearest(q, 100.0) == 1300.0, "%.1f" % q)
    check("SF10 'passes' means not exceeding: no protected borehole sits at its available drawdown at 1,300",
          all(abs(C.assessment(1300.0, xy, T, S, img) - av) > 0.05 for n, xy, av in prot))
    a_, c_, img2 = C.fault(b)
    shift = []
    for dx in (-25.0, 25.0):
        d = (c_ - a_) / np.linalg.norm(c_ - a_)
        nrm = np.array([d[1], -d[0]])
        aa, cc = a_ + dx * nrm, c_ + dx * nrm
        dd = (cc - aa) / np.linalg.norm(cc - aa)
        foot = aa + np.dot(-aa, dd) * dd
        shift.append(C.nearest(C.largest(prot, T, S, 2 * foot)[0], 100.0))
    check("SF11 the fault trace read 25 m either way moves nothing", shift == [1300.0, 1300.0], str(shift))
    check("SF12 grid references in the letter read on the survey's grid", all(abs(xy[0]) < 4000 and abs(xy[1]) < 4000
                                                                                for _, xy, _ in prot))
    check("SF13 the applied quantity is a daily rate in cubic metres", "cubic metres a day" in letter)

    # ---------------------------------------------------------------------------------------------- ask A
    sf = C.shift_fills(b)
    check("SF14 every ticket finds exactly one pump run on its night shift", all(len(c) == 1 for _, c in sf),
          str(sum(1 for _, c in sf if len(c) != 1)))
    rate = C.bay_rate(b)
    rr = np.array([c[0][2] for _, c in sf])
    check("SF14 every matched run carries its ticket's litres at the bay's rate (within 1.5 per cent)",
          bool((abs(rr / rate - 1) <= 0.015).all()), "rate %.3f, %.3f to %.3f" % (rate, rr.min(), rr.max()))
    lit = C.match_tickets(b)
    after = [(tk, c) for tk, c in lit if int(tk["t_in"][:2]) < 12]
    imposs = 0
    for tk, cands in after:
        same = [x for x in cands if x[0].date() == tk["date"] and abs(x[2] / rate - 1) <= 0.015]
        if not same:
            imposs += 1
    check("SF15 the literal ticket date is impossible for most after-midnight tickets (no run there at the ticket's "
          "litres)", imposs >= 0.8 * len(after), "%d of %d" % (imposs, len(after)))
    tel_rows = C.telem_local(b)
    night_flat = 0
    for tk, c in sf:
        a0, z0 = c[0][0], c[0][1]
        fm = sum(v1 for loc, v1, _ in tel_rows if a0 - dt.timedelta(minutes=15) <= loc <= z0)
        night_flat += fm < 0.5
    check("SF16 FM-1 records nothing while the bay fills (the bulk loads bypass the licence meter)",
          night_flat == len(sf), "%d of %d" % (night_flat, len(sf)))
    gA = C.ask_a(b)
    cA = C.ask_a(b, tankers=False)
    tA = C.ask_a(b, shift_dating=False)
    for k in DL.MONTHS_A:
        lab = DL.month_label(k)
        check("askA %s: cracker's volume (FM-1 alone) misses by more than two bins" % lab, abs(gA[k][0] - cA[k][0]) > 200.0,
              "%.0f vs %.0f" % (gA[k][0], cA[k][0]))
        check("askA %s: cracker's day count misses" % lab, gA[k][1] != cA[k][1], "%d vs %d" % (gA[k][1], cA[k][1]))
        check("askA %s: ticket-dated day count misses" % lab, gA[k][1] != tA[k][1], "%d vs %d" % (gA[k][1], tA[k][1]))
        check("bin askA %s volume clear of an edge" % lab, edge(gA[k][0], 100.0) >= 15.0, "%.1f" % gA[k][0])
    # SF17: the licence day. Read with each quarter's flow as the quarter ending at its stamp, or from FM-1's register
    # steps, the same volumes and counts (C1); read on the UTC clock (the telemetry's dates, the loads' pump runs
    # converted to UTC) other counts, the rival the licence's own day clause rules out (local time).
    def ask_a_clock(mode, load_day="run"):
        day_fm1 = {}
        prev_reg = None
        for r_ in b.telem:
            t_ = dt.datetime.strptime(r_["time_utc"], "%Y-%m-%dT%H:%MZ")
            loc_ = K.utc_to_local(t_)
            if mode == "register":                       # the register's own steps, the meter change bridged
                reg_ = float(r_["fm1_register_m3"])
                step = 0.0 if prev_reg is None else (reg_ - prev_reg if reg_ >= prev_reg else reg_)
                prev_reg = reg_
                day_fm1[loc_.date()] = day_fm1.get(loc_.date(), 0.0) + step
                continue
            key = t_.date() if mode == "utc" else (loc_ - dt.timedelta(minutes=15) if mode == "ending" else loc_).date()
            day_fm1[key] = day_fm1.get(key, 0.0) + float(r_["fm1_flow_ls"]) * 0.9
        day_tank = {}
        for tk, cands in C.shift_fills(b):
            if load_day == "time_in":                    # the ticket's own time in, on the night its shift began
                hi_ = int(tk["t_in"].split(":")[0])
                d_ = tk["date"] + dt.timedelta(days=1 if hi_ < 12 else 0)
            elif mode == "utc":
                d_ = K.local_to_utc(cands[0][0]).date()
            else:
                d_ = cands[0][0].date()
            day_tank[d_] = day_tank.get(d_, 0.0) + tk["litres"] / 1000.0
        res_ = {}
        for y_, m_ in DL.MONTHS_A:
            days_ = [dt.date(y_, m_, 1) + dt.timedelta(days=i) for i in range(W.month_days(y_, m_))]
            tot_ = [day_fm1.get(d_, 0.0) + day_tank.get(d_, 0.0) for d_ in days_]
            res_[(y_, m_)] = (C.nearest(sum(tot_), 100.0), sum(1 for v_ in tot_ if v_ > K.LICENSED_QD))
        return res_
    gold_a = {k_: (C.nearest(v_[0], 100.0), v_[1]) for k_, v_ in gA.items()}
    for mode, words in (("ending", "with each quarter ending at its stamp"),
                        ("register", "from FM-1's register steps instead of its flow")):
        alt = ask_a_clock(mode)
        check("askA SF17 the licence day read %s files the same volumes and day counts" % words, alt == gold_a,
              str([(k_, alt[k_], gold_a[k_]) for k_ in gold_a if alt[k_] != gold_a[k_]][:3]))
    lic = re.sub(r"\s+", " ", pdf_text(os.path.join(target, D.F_LICENCE)))
    utc_alt = ask_a_clock("utc")
    check("askA SF17 the licence's day clause names local time, ruling out the UTC day (the rival files %s days over "
          "against the golden %s)" % ([utc_alt[k_][1] for k_ in DL.MONTHS_A], [gold_a[k_][1] for k_ in DL.MONTHS_A]),
          "a day is a period of 24 hours beginning at midnight, local time" in lic)
    # the ticket day: each load on its ticket's own time-in day (the shift's night read right) against its pump run's
    # start day. The two converge: no ticket's time in falls on another day than its pump run's start.
    alt_ti = ask_a_clock("local", load_day="time_in")
    split = 0
    for tk, cands in C.shift_fills(b):
        hi_, mi_ = map(int, tk["t_in"].split(":"))
        d_ = tk["date"] + dt.timedelta(days=1 if hi_ < 12 else 0)
        split += d_ != cands[0][0].date()
    check("askA SF15 every ticket's time-in day is its pump run's start day", split == 0, "%d tickets differ" % split)
    check("askA SF15 each load on its ticket's time-in day files every returns figure the pump-run day files",
          alt_ti == gold_a, str([(k_, alt_ti[k_], gold_a[k_]) for k_ in gold_a if alt_ti[k_] != gold_a[k_]][:3]))
    # the controller log's other entries (trips, resets, link drops, a re-sent stop) leave every pump run as it was
    clean_runs = []
    st_ = None
    seen_ = set()
    for r_ in b.pump:
        key_ = (r_["timestamp"], r_["tag"], r_["event"])
        if key_ in seen_:
            continue
        seen_.add(key_)
        t_ = dt.datetime.strptime(r_["timestamp"], "%d/%m/%Y %H:%M:%S")
        if r_["event"] == "PUMP START":
            st_ = t_
        elif r_["event"] == "PUMP STOP" and st_ is not None:
            clean_runs.append((st_, t_))
            st_ = None
    other = sum(1 for r_ in b.pump if r_["event"] not in ("PUMP START", "PUMP STOP"))
    check("askA the controller log's trips, resets and link drops (%d entries) and its re-sent stops leave every pump run "
          "unchanged" % other, clean_runs == C.pump_runs(b) and other > 0, "%d against %d" % (len(clean_runs),
                                                                                         len(C.pump_runs(b))))
    # ---------------------------------------------------------------------------------------------- ask B
    sizes = C.true_sizes(b)
    check("SF18 BSG-1101 was 750 ml through the 2025-26 year (QC net fills) against the export's 700",
          sizes.get("BSG-1101") == 750.0 and b.sku["BSG-1101"][1] == 700.0, str(sizes))
    w_after = [float(q["net_fill_g"]) for q in b.qc if q["material"] == "BSG-1101" and q["result"] == "PASS" and
               dt.datetime.strptime(q["sample_time"], "%d/%m/%Y %H:%M").date() >= W.SIZE_SWITCH]
    check("SF18 the export's 700 ml is the bottle filled since April 2026 (its level-filled overfill on top)",
          700 < np.median(w_after) < 716, "%.1f" % np.median(w_after))
    brief = docx_text(os.path.join(target, D.F_BRIEF))
    check("SF18 the brief sizes line 3's ratio on good bottles at the bottle's size (not fill weights, not rejects)",
          "per litre it packed (good bottles times the bottle's size)" in brief)
    lic4 = pdf_text(os.path.join(target, D.F_LICENCE)).replace("\n", " ")
    check("SF16 the licence's purposes include the bulk supply", "supply of water in bulk" in lic4)
    gB = C.ask_b(b)
    mB = C.ask_b(b, "master")
    qB = C.ask_b(b, "qc")
    for k in DL.MONTHS_B:
        lab = DL.month_label(k)
        check("askB %s: cracker (export sizes) misses by more than five bins" % lab, abs(gB[k] - mB[k]) > 0.05,
              "%.3f vs %.3f" % (gB[k], mB[k]))
        check("bin askB %s clear of a two-decimal edge" % lab, edge(gB[k], 0.01) >= 0.0008, "%.4f" % gB[k])
        check("askB %s: the fill weights read as sizes (the over-cleaner) miss" % lab, round(qB[k], 2) != round(gB[k], 2),
              "%.3f vs %.3f" % (qB[k], gB[k]))
    # the month read on the telemetry's UTC dates, or with each quarter ending at its stamp: line 3 draws nothing near
    # midnight, so every ratio is the same
    parts = C.ask_b_parts(b)
    gB_round = {k: round(gB[k], 2) for k in DL.MONTHS_B}
    for mode in ("utc", "ending"):
        wat = {}
        prev_ = None
        for r_ in b.telem:
            t_ = dt.datetime.strptime(r_["time_utc"], "%Y-%m-%dT%H:%MZ")
            reg = float(r_["fm_l3_register_m3"])
            if prev_ is not None:
                key_t = t_ if mode == "utc" else K.utc_to_local(t_) - dt.timedelta(minutes=15)
                wat[(key_t.year, key_t.month)] = wat.get((key_t.year, key_t.month), 0.0) + reg - prev_
            prev_ = reg
        alt = {k: round(wat[k] * 1000.0 / parts[k][1], 2) for k in DL.MONTHS_B}
        check("askB the month read %s gives the same ratios" % ("on the telemetry's UTC dates" if mode == "utc" else
                                                               "with each quarter ending at its stamp"),
              alt == gB_round, str([(DL.month_label(k), alt[k], gB_round[k]) for k in DL.MONTHS_B if alt[k] != gB_round[k]][:3]))
    cip = [(dt.datetime.strptime(r_["start_local"], "%Y-%m-%d %H:%M"), dt.datetime.strptime(r_["end_local"], "%Y-%m-%d %H:%M"))
           for r_ in b.runs if r_["line"] == "L3" and r_["order_type"] == "CIP"]
    cip_m3 = {}
    for loc, _, lines in tel_rows:
        if any(a_ - dt.timedelta(minutes=15) < loc <= z_ for a_, z_ in cip):
            cip_m3[(loc.year, loc.month)] = cip_m3.get((loc.year, loc.month), 0.0) + lines[2]
    lit_ = {}
    for r_ in b.runs:
        if r_["line"] == "L3" and r_["order_type"] == "PROD":
            t_ = dt.datetime.strptime(r_["start_local"], "%Y-%m-%d %H:%M")
            lit_[(t_.year, t_.month)] = lit_.get((t_.year, t_.month), 0.0) + int(r_["qty_good"]) * (
                750.0 if r_["sku"] in ("BSG-1101", "BKG-1102") else 500.0) / 1000.0
    noclean = {k: gB[k] - cip_m3.get(k, 0.0) * 1000.0 / lit_[k] for k in DL.MONTHS_B}
    check("SF19 cleans included is pinned in the asking sentence and matters: leaving them out moves every month",
          all(abs(gB[k] - noclean[k]) > 0.02 for k in DL.MONTHS_B), str({DL.month_label(k): round(gB[k] - noclean[k], 3)
                                                                         for k in DL.MONTHS_B[:3]}))
    # ---------------------------------------------------------------------------------------------- separation line
    main_files = {R.F_TEST, R.F_OBS, R.F_RMB, R.F_SURVEY, D.F_LETTER, D.F_GEOLOGY, D.F_RETURNS}
    ask_files = {R.F_TELEM, R.F_PUMP, R.F_TICKETS, R.F_RUNS, R.F_SKU, R.F_QC}
    check("separation: no device file is a main-call file", not (main_files & ask_files))
    last_ob = max(tuple(map(int, r["month"].split("-"))) for r in b.obs)
    first_load = min(c[0][0] for _, c in C.shift_fills(b))
    rm_months = sorted(C.returns_monthly(b))
    check("separation: the bulk loads begin after the observation record and the returns the long record is modelled "
          "on (zero device rows in the main call's population)", (first_load.year, first_load.month) > last_ob and
          (first_load.year, first_load.month) > rm_months[-1], "first load %s, record to %s, returns to %s" % (
              first_load, last_ob, rm_months[-1]))
    # ---------------------------------------------------------------------------------------------- realism sweep
    orders = sorted(int(r["order_no"]) for r in b.runs)
    steps = {b_ - a_ for a_, b_ in zip(orders, orders[1:])}
    check("realism: order numbers are not one constant step", len(steps) > 1, str(sorted(steps)[:5]))
    tk_steps = set()
    by = {}
    for tk in b.tickets:
        by.setdefault(tk["sheet"], []).append(int(tk["no"]))
    for nos in by.values():
        nos = sorted(set(nos))
        tk_steps |= {y - x for x, y in zip(nos, nos[1:])}
    check("realism: ticket numbers are not one constant step", len(tk_steps) > 1, str(sorted(tk_steps)))
    vols = [gA[k][0] for k in DL.MONTHS_A]
    check("realism: no round monthly volume", not [v for v in vols if v % 1000 == 0])
    check("realism: no repeated monthly figure", len({round(v) for v in vols}) == len(vols))
    flows = [float(r["fm1_flow_ls"]) for r in b.telem if float(r["fm1_flow_ls"]) > 20]
    check("realism: FM-1's full-quarter flow varies", len({round(x, 1) for x in flows}) > 8, str(sorted({round(x, 1) for x in flows})[:6]))
    people = set(K.PEOPLE.values())
    card = json.load(open(os.path.join(os.path.dirname(os.path.dirname(target)), ".claude", "skills", "fingerprint", "cards",
                                       "task154.json")))
    check("realism: personas are the card's drawn names", people == set(card["world"]["people"]), str(people))
    for f in files:
        p = os.path.join(target, f)
        raw = open(p, "rb").read()
        if f.endswith(".pdf"):
            check("container: %s carries no library banner" % f, b"ReportLab" not in raw and b"reportlab" not in raw)
        if f.endswith((".xlsx", ".docx")):
            with zipfile.ZipFile(p) as z:
                core = z.read("docProps/core.xml")
                app = z.read("docProps/app.xml")
            check("container: %s carries its owner, not the writing library" % f, b"openpyxl" not in core + app and
                  b"python-docx" not in core + app)
    # document dates: no document states a position later than its own date
    check("dates: the letter (22 September 2026) cites nothing later", "18 December 2026" in letter and
          "2026-10" not in letter)
    ret = pdf_text(os.path.join(target, D.F_RETURNS))
    late = re.findall(r"^(?:April|May|June|July|August|September|October) 2026\b", ret, re.M)
    check("dates: the returns' last year ends March 2026", "March 2026" in ret and not late, str(late))

    # ---------------------------------------------------------------------------------------------- leak hygiene
    words = r"barrier|no-flow|image well|bypass|unmetered|upstream of (?:the )?meter|shift date|night shift|lightweight|" \
            r"hydraulic|sealing|boundary condition|superposition|derogat\w+ is"
    texts = {f: pdf_text(os.path.join(target, f)) for f in files if f.endswith(".pdf")}
    texts[D.F_BRIEF] = docx_text(os.path.join(target, D.F_BRIEF))
    for f, t in texts.items():
        check("leak: %s read back (positive control)" % f, len(t) > 200)
        check("leak: %s names no device or decisive step" % f, not re.search(words, t, re.I),
              str(re.findall(words, t, re.I)[:3]))
    geo = texts[D.F_GEOLOGY]
    check("leak: the geology extract's positive control (the fault's trace) reads back",
          "Coldharbour Fault" in geo and "downthrown to the east by about 260 m" in geo.replace("\n", " "))
    check("leak: the geology says nothing about water flow", not re.search(r"flow|permeab|aquifer|transmiss|water-bearing",
                                                                          geo, re.I),
          str(re.findall(r"flow|permeab|aquifer|transmiss", geo, re.I)[:3]))
    for f in meta["distractor_files"]:
        check("distractor %s: no golden computation reads it" % f, f not in open(C.__file__).read())
    mtext = json.dumps(meta)
    check("leak: metadata names no method", not re.search(r"Theis|fault|barrier|image|tanker bay|bypass|shift|700 ml|"
                                                          r"750 ml|70cl|switch|upstream|unmetered|night", mtext, re.I),
          str(re.findall(r"Theis|fault|barrier|image|tanker bay|bypass|shift|700 ml|750 ml|70cl|switch|upstream|"
                         r"unmetered|night", mtext, re.I)[:4]))
    # figures.json carries every graded figure
    check("figures.json: every ask figure present", sum(1 for k in figs if k.startswith("askA_") or k.startswith("askB_")) == 24)
    n = len(RESULTS)
    fails = [r for r in RESULTS if not r[1]]
    print("checks: %d assertions, %d failed" % (n, len(fails)))
    if fails:
        raise SystemExit("checks failed: " + "; ".join(r[0] for r in fails[:10]))
    return RESULTS
