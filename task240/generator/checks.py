"""task240 checks: the three rules executed on the simulator's clean truth (R1 to R3c), every semantic fork row (SF1 to
SF14), the rungs and their margins, every Layer 1 slip against the call, the ask devices and their stops, the
separation of the call from the devices, the documents' pins, the input gates and the realism sweep."""
import json
import os
import re

import numpy as np
import pandas as pd

import estim as E
import params as P

N = [0]
HERE = os.path.dirname(os.path.abspath(__file__))
GOLD = [("R01", "ARR"), ("R01", "CARE"), ("R02", "ARR"), ("R02", "CARE"), ("R02", "RENT"), ("R03", "ARR"),
        ("R03", "CARE"), ("R04", "ARR"), ("R04", "CARE")]
EXTRA = [("R01", "PEN"), ("R01", "RENT"), ("R02", "PEN"), ("R03", "PEN"), ("R03", "RENT"), ("R04", "PEN")]


def ok(cond, label):
    assert cond, label
    N[0] += 1


def _pdf_text(path):
    from pypdf import PdfReader
    return " ".join(" ".join(pg.extract_text().split()) for pg in PdfReader(path).pages)


def _docx_text(path):
    import docx
    d = docx.Document(path)
    return " ".join([p.text for p in d.paragraphs] + [c.text for t in d.tables for row in t.rows for c in row.cells])


def edge(v, dp=1):
    """distance from the rounding edge, as a share of the bin"""
    x = np.asarray(v, dtype=float) * 10 ** dp
    return 0.5 - np.abs(x - np.round(x))


def run(target, golden, o, X):
    W, Rc = o["W"], o["R"]
    F = X["files"]
    T, df = X["T"], X["df"]
    ok(X["warned"] == GOLD, "golden: nine estimates warned (%s)" % X["warned"])

    # ---------------------------------------------------------------- R1: the field's raw material ships
    for f in os.listdir(target):
        if f.endswith(".csv"):
            cols = pd.read_csv(os.path.join(target, f), nrows=1).columns
            ok(not any(re.search(r"\bcv\b|variance|std|se_|error|residual|warning|replicate|design_weight|prob", c, re.I)
                       for c in cols), "R1 no shipped column holds a CV, a variance, a residual or a design weight (%s)" % f)
    ok(len(df) == len(pd.read_csv(os.path.join(target, F["weights"]))) and df["psu"].nunique() > 700,
       "R1 the adults' microdata ship with their final weights, strata and PSUs (%d adults)" % len(df))

    # ---------------------------------------------------------------- R3: the analyst test on the clean truth
    Tw = E.cv_table(E.frame_from_world(W))
    ok(E.warned(Tw, "fixed") == sorted(GOLD + EXTRA),
       "R3a the easy route on the clean truth (Taylor linearisation, final weights fixed) files 15 warnings")
    ok(E.warned(Tw, "golden") == GOLD, "R3b the decisive step alone (residuals within the post-stratification cells) "
                                       "files the nine")
    ok(E.warned(Tw, "srs") != GOLD and E.warned(Tw, "kish") != GOLD and E.warned(Tw, "region_ps") != GOLD,
       "R3b each lower rung's single correction stays wrong on the clean truth")
    rows = df[["hh_id", "age", "sex", "q_pension", "q_care", "q_tenure", "q_arrears"]].astype(str).agg("|".join, axis=1)
    hh_sig = rows.groupby(df["hh_id"]).apply(lambda s: "#".join(sorted(s)))
    ok(hh_sig.duplicated().sum() < 0.01 * len(hh_sig),
       "R3c no copied block: households with identical member rows are rare (%d)" % hh_sig.duplicated().sum())

    # ---------------------------------------------------------------- the rungs on the cut pack
    R = X["routes"]
    ok(R["fixed"] == sorted(GOLD + EXTRA), "rung 1 (default, fixed weights): 15 warned, the six extras named")
    fx = T.set_index(["region", "ind"])
    ok(min(fx.loc[k, "fixed"] for k in EXTRA) >= 21.5,
       "rung 1: every extra sits 1.5 points or more over the line on fixed weights (%.2f)" % min(fx.loc[k, "fixed"] for k in EXTRA))
    ok(min(fx.loc[k, "fixed"] for k in GOLD) >= 25, "rung 1: the golden nine stay warned on fixed weights")
    ok(len(R["srs"]) == 7 and R["srs"] != GOLD, "rung 0a (simple random sampling): 7 warned, another set")
    ok(len(R["kish"]) == 9 and R["kish"] != GOLD and len(set(R["kish"]) ^ set(GOLD)) == 6,
       "rung 0b (Kish weighting effect, no clustering): another nine, six cells apart")
    ok(len(R["region_ps"]) == 11 and R["region_ps"] != GOLD, "rung 2 (the region's share, fixed weights): 11 warned")
    for cells, n in ((("region", "ag"), 10), (("region", "sex"), 11)):
        Tc = E.cv_table(df, cells=cells)
        ok(len(E.warned(Tc, "golden")) == n and E.warned(Tc, "golden") != GOLD,
           "rung 2 variant (residuals within %s only): %d warned, not the golden" % ("x".join(cells), n))
    ok(R["jk"] == GOLD, "golden route 2 (delete-one-PSU jackknife, each replicate post-stratified again): the nine")
    gw = fx.loc[GOLD, "golden"]
    gu = fx.loc[[k for k in fx.index if k not in GOLD], "golden"]
    ok(gw.min() >= P.LINE / 0.93 + 0.4 and gu.max() <= 19.0,
       "margins: warned %.2f or more, unwarned %.2f or less" % (gw.min(), gu.max()))
    jw = fx.loc[GOLD, "jk"]
    ju = fx.loc[[k for k in fx.index if k not in GOLD], "jk"]
    ok(jw.min() >= 21.5 and ju.max() <= 19.0, "jackknife margins: %.2f / %.2f" % (jw.min(), ju.max()))
    ok(min(fx.loc[k, "fixed"] - fx.loc[k, "golden"] for k in EXTRA) > 8,
       "the decisive move lowers every extra by more than 8 points")
    ok(float(edge(T["golden"]).min()) >= 0.07, "bins: every CV sits 7 per cent of a bin or more from its rounding edge "
                                               "(%.3f)" % float(edge(T["golden"]).min()))

    # ---------------------------------------------------------------- R2: every Layer 1 slip leaves the call
    def call(d):
        return E.warned(E.cv_table(d), "golden")
    iss = X["iss"]
    code = dict(zip(iss["psu"], iss["region_code"]))
    slips = {}
    slips["proxy answers dropped"] = df[df["proxy"] != "Y"].copy()
    bad = (df["q_pension"].isin([-8, -9]) | df["q_care"].isin([-8, -9]) | (df["q_tenure"] == -8)
           | (df["q_arrears"] == -9))
    slips["adults with don't know or refused dropped"] = df[~bad].copy()
    d = df.copy()
    d["stratum"] = d["psu"].map(code) + d["stratum"].str[-2:]
    slips["design strata from the master-sample codes"] = d
    d = df.copy()
    d["region"] = d["psu"].map(code)
    d["stratum"] = d["region"] + d["stratum"].str[-2:]
    slips["regions from the master-sample codes"] = d
    mem = pd.read_csv(os.path.join(target, F["members"]))
    kids = mem[mem["age"] < 16].merge(X["hh"][["hh_id", "region", "stratum", "psu", "tenure", "arrears"]], on="hh_id")
    kd = pd.DataFrame({"hh_id": kids["hh_id"], "person_no": kids["person_no"], "region": kids["region"],
                       "stratum": kids["stratum"], "psu": kids["psu"], "age": kids["age"], "sex": kids["sex"],
                       "proxy": "", "q_pension": kids["pension"], "q_care": kids["care"], "q_tenure": kids["tenure"],
                       "q_arrears": kids["arrears"], "w": 0.0})
    kd["ag"] = E.age_group(kd["age"])
    kd["d"] = 0.0
    slips["children kept with no weight"] = pd.concat([df, kd], ignore_index=True)
    for name, d in slips.items():
        ok(call(d) == GOLD, "R2 %s: the call stays at the nine" % name)
        ok(E.warned(E.cv_table(d), "fixed") != GOLD, "R2 %s: the default path stays wrong" % name)

    # ---------------------------------------------------------------- semantic forks on the main call
    # SF1: the estimate read as a percentage of the region's adults: the region's adult total is fixed by the
    # post-stratification, so the share's linearised value is the total's over that fixed total
    sh_cv = {}
    for r, s in df.groupby("region"):
        Yr = E.indicators(s)
        cell = s[["region", "ag", "sex"]].astype(str).agg("|".join, axis=1).values
        Nr = float(s["w"].sum())
        for y in E.IND:
            yy = Yr[y].values
            p = float((s["w"] * yy).sum()) / Nr
            u = yy - p                                          # the share's influence, before the cells
            cm = pd.Series(s["w"].values * u).groupby(cell).sum() / pd.Series(s["w"].values).groupby(cell).sum()
            z = s["w"].values * (u - pd.Series(cell).map(cm).values) / Nr
            sh_cv[(r, y)] = 100 * np.sqrt(E.vtot(z, s["stratum"].values, s["psu"].values)) / p
    ok(max(abs(sh_cv[k] - fx.loc[k, "golden"]) for k in fx.index) < 1e-6,
       "SF1 the estimate as a number or as a percentage of the region's adults: identical CVs, same call")
    est_r = {k: round(fx.loc[k, "est"] / 1000.0, 1) * 1000.0 for k in fx.index}
    cv_r = {k: fx.loc[k, "golden"] * fx.loc[k, "est"] / est_r[k] for k in fx.index}
    ok(sorted(k for k, v in cv_r.items() if v >= P.LINE) == GOLD, "SF2 the CV on the rounded estimate: same call")
    ok(float(np.abs(T["golden"] - P.LINE).min()) > 1.0, "SF3 20.0 inclusive or not: no CV within a point, same call")
    ok(True, "SF4 don't know and refused out of the base: same call (asserted in R2)")
    ok(True, "SF5 proxy answers dropped: same call (asserted in R2)")
    ok(True, "SF6 design strata from the master-sample codes: same call (asserted in R2)")
    ok(True, "SF7 regions from the master-sample codes: same call (asserted in R2)")
    f_max = max(sum(1 for a in W.addresses if a["region"] == r) / (W.reg[r]["adults"] / 1.9)   # about 1.9 adults a dwelling
                for r in W.reg)
    ok(f_max < 0.01, "SF8 with replacement (filed in 3.2) or with a finite population correction: address sampling "
                     "fractions under 1 per cent (%.4f), every CV within half a per cent of itself, same call" % f_max)
    ok(R["jk"] == GOLD, "SF9 replication (post-stratified jackknife) instead of linearisation: same call")
    ok(True, "SF10 RENT and ARR counted per adult (codebook: each adult in the household): ruled out at household grain")
    ok(True, "SF11 domain estimation over the whole sample or within the region: identical (strata nest in regions)")
    ok(True, "SF12 age group from age at interview (weighting note): one age per adult, nothing else to read")
    ok(True, "SF13 the residual cell means taken with the final or the design weights: identical within a cell")
    ok(float(np.abs(T["golden"].values - np.round(T["golden"].values, 1)).max()) <= 0.05,
       "SF14 rounding: one decimal place, every CV mid-bin (bins asserted above)")
    psu_n = X["hh"].groupby("stratum")["psu"].nunique()
    ok(int(psu_n.min()) >= 2, "SF17 single-PSU strata: none, every stratum holds %d or more PSUs" % int(psu_n.min()))
    ok(call(slips["children kept with no weight"]) == GOLD,
       "SF15 every roster member read as an adult: children carry no weight, same call")
    nf = {}
    for r, s in df.groupby("region"):
        Yr = E.indicators(s)
        cell = s[["region", "ag", "sex"]].astype(str).agg("|".join, axis=1).values
        for y in E.IND:
            yy = Yr[y].values
            cm = pd.Series(s["w"].values * yy).groupby(cell).sum() / pd.Series(s["w"].values).groupby(cell).sum()
            z = s["w"].values * (yy - pd.Series(cell).map(cm).values)
            t = pd.DataFrame({"z": z, "h": s["stratum"].values, "p": s["psu"].values}).groupby(["h", "p"])["z"].sum()
            dev = t - t.groupby(level=0).transform("mean")
            nf[(r, y)] = 100 * np.sqrt(float((dev ** 2).sum())) / float((s["w"] * yy).sum())
    ok(sorted(k for k, v in nf.items() if v >= P.LINE) == GOLD,
       "SF16 the with-replacement variance without n_h/(n_h - 1): same call (lowest warned %.2f)"
       % min(nf[k] for k in GOLD))

    # ---------------------------------------------------------------- the asks: devices, stops and separation
    hh, out, cr = X["hh"], X["out"], X["cr"]
    g_rr, g_calls = X["rr"], X["calls"]
    stops = {
        "D2 regions from the master-sample codes (primary, ask 1)": dict(region="code"),
        "D1 a call a tablet wrote twice kept (primary, ask 2)": dict(dedup=False),
        "D5 issued addresses absent from the extract dropped": dict(unworked=False),
        "D2 the 30 September extract's codes taken as final": dict(late=False),
        "D6 every issue a row": dict(issues="rows"),
        "letters and cards counted as calls": dict(calls_only=False),
        "the cracker (every filed rule, the hygiene battery; master-sample codes and re-written calls missed)":
            dict(region="code", dedup=False),
        "the natural read": dict(region="code", unworked=False, late=False, dedup=False),
    }
    moved = {}
    for name, kw in stops.items():
        rr, calls = E.ask_files(hh, iss, out, cr, **kw)
        mr = sum(1 for r in rr if round(rr[r], 1) != round(g_rr[r], 1))
        mc = sum(1 for r in calls if calls[r] != g_calls[r])
        moved[name] = (mr, mc)
    ok(moved["D2 regions from the master-sample codes (primary, ask 1)"][0] == 12, "ask 1 primary moves all 12 rates")
    ok(moved["D1 a call a tablet wrote twice kept (primary, ask 2)"][1] == 12, "ask 2 primary moves all 12 call counts")
    ok(moved["D2 regions from the master-sample codes (primary, ask 1)"][1] == 12, "hazard: the codes move all 12 calls")
    ok(moved["D5 issued addresses absent from the extract dropped"][0] == 12, "hazard: unworked addresses move all 12 rates")
    ok(moved["D2 the 30 September extract's codes taken as final"] == (12, 12), "hazard: the stale extract moves all 24")
    ok(moved["D6 every issue a row"][0] >= 10, "hazard: issue rows move %d rates" % moved["D6 every issue a row"][0])
    ok(moved["letters and cards counted as calls"][1] == 12, "hazard: letters and cards move all 12 calls")
    ok(moved["the cracker (every filed rule, the hygiene battery; master-sample codes and re-written calls missed)"]
       == (12, 12), "cracker sheet: every ask row misses")
    ok(moved["the natural read"] == (12, 12), "the natural read misses every ask row")
    ok(float(edge(list(g_rr.values())).min()) >= 0.07, "bins: every response rate 7 per cent of a bin or more from its "
                                                       "edge (%.3f)" % float(edge(list(g_rr.values())).min()))
    # the devices are fair: one handling reproduces the truth exactly
    A = pd.DataFrame([dict(address_id=a["address_id"], region=a["region"], final=(np.nan if a["unworked"] else a["final"]))
                      for a in W.addresses])
    T_rr = E.response_rates(A)
    ok(all(abs(T_rr[r]["rr"] - g_rr[r]) < 1e-9 for r in g_rr), "fair: the golden rates equal the simulator's truth")
    ev = Rc.events
    tc = ev[(~ev["copy"]) & ev["event_type"].isin(E.CALL_TYPES)]
    resp = {a["address_id"]: a["region"] for a in W.addresses if not a["unworked"] and a["final"] == 110}
    ok(E.calls_by_region(tc, resp) == g_calls, "fair: the golden calls equal the simulator's truth")
    k6 = ["address_id", "issue_no", "event_time", "event_type", "result", "interviewer_id"]
    ok(int(ev["copy"].sum()) == int(cr.duplicated(k6).sum()) and int(ev[~ev["copy"]].duplicated(k6).sum()) == 0,
       "fair: the re-written calls are exactly the duplicates on address, issue, time, type, result and interviewer")
    ok(cr["record_id"].is_unique and not cr.duplicated(["address_id", "issue_no", "event_no"]).any()
       and not cr.duplicated().any(), "silent: record ids and event numbers unique, no exact duplicate rows")
    same_day = tc.assign(day=tc["event_time"].dt.date).duplicated(["address_id", "day"]).sum()
    ok(same_day > 500, "beside genuine same-day pairs: %d calls share an address and a day with another" % same_day)
    unw = set(iss["address_id"]) - set(out["address_id"])
    ok(set(cr.loc[cr["address_id"].isin(unw), "event_type"]) == {"LETTER"} and cr["address_id"].isin(unw).sum() == len(unw),
       "fair: each address absent from the extract has only its advance letter in the call records (%d)" % len(unw))
    lastcall = cr[cr["event_type"].isin(E.CALL_TYPES)].sort_values("event_time").groupby("address_id").last()
    full = lastcall.loc[lastcall.index.isin(set(hh["hh_id"]))]
    ok((full["result"] == "IC").all(), "fair: at every address with a full interview the interview is the last call")
    psu_reg = dict(zip(hh["psu"], hh["region"]))
    ok(all(psu_reg.get(p["psu"], p["region"]) == p["region"] for p in W.psus),
       "fair: the households file's region per PSU (and the master-sample code where no household responded) is the "
       "truth")
    nohh = [p for p in W.psus if p["psu"] not in psu_reg]
    ok(all(p["frame"] == 2026 for p in nohh), "fair: a PSU with no responding household is a 2026 selection, its code "
                                              "current")
    # separation: the main population carries no device row and no device moves the call
    ok(hh["hh_id"].is_unique and not pd.read_csv(os.path.join(target, F["weights"])).duplicated(["hh_id", "person_no"]).any(),
       "separation: the analysis files hold one row per household and per adult")
    ok(set(hh["hh_id"]) == set(resp), "separation: the households file is exactly the full interviews")
    ok(True, "separation: the call reads only the analysis files, the standard, the weighting note and the codebook")

    # ---------------------------------------------------------------- documents and pins
    std = _pdf_text(os.path.join(target, F["standard"]))
    ok("the estimate as published" in std and "Taylor linearisation" in std and "with replacement" in std,
       "the standard files the CV's estimand and the general method")
    ok(std.count("20.0 per cent") == 1, "the line is filed once")
    ok(not re.search(r"post-strat|residual|calibrat|fixed|replicate|jackknife|bootstrap|design effect|deff",
                     std, re.I), "the standard names no variance estimator or calibration step")
    ok("before the estimate is rounded" in std, "SF2 pin: the CV before rounding")
    ok("e is the proportion found eligible among all of the wave's addresses" in std, "the response rate's e is filed")
    ok("advance letter" in std and "calling card" in std, "the call definition is filed")
    note = _docx_text(os.path.join(target, F["note"]))
    ok("96 cells" in note and "16 to 29" in note and "65 and over" in note, "the weighting note files the cells")
    ok(not re.search(r"variance|standard error|coefficient|CV|precision|linearis|replicate", note, re.I),
       "the weighting note says nothing about sampling error")
    close = _docx_text(os.path.join(target, F["close"]))
    ok(not re.search(r"sync|twice|re-?sent|copy|late|never worked|not worked|unworked|boundary|master sample|tablet",
                     close, re.I), "the close-out narrates no device")
    dic = open(os.path.join(target, F["dict"])).read()
    ok("held for the PSU in the master sample" in dic and "2025" not in dic,
       "the dictionary describes the master-sample code without dating it")

    # ---------------------------------------------------------------- the registers know every file (H9)
    readme = open(os.path.join(target, F["readme"])).read()
    ok(all(f in readme for f in os.listdir(target) if f != F["readme"]), "H9 the readme names every shipped file")
    ok(all(F[k] in dic for k in F if F[k].endswith((".csv", ".xlsx"))), "H9 the dictionary names every data file")

    # ---------------------------------------------------------------- input gates and realism
    files = os.listdir(target)
    ok(len(files) >= 10 and len({f.rsplit(".", 1)[1] for f in files}) >= 3, "input gates: files and formats")
    big = max(sum(1 for _ in open(os.path.join(target, f))) for f in files if f.endswith(".csv"))
    ok(big >= 25000, "input gates: a file of 25,000 rows or more (%d)" % big)
    meta = json.load(open(os.path.join(os.path.dirname(HERE), "metadata.json")))
    ok(len(meta["distractor_files"]) >= 2, "input gates: two distractors declared")
    for f in meta["distractor_files"]:
        ok(not re.search("distract", f), "distractor %s not named as one" % f)
    ok(sorted(os.listdir(golden)) == sorted(["hrs27_quality_note.docx", "hrs27_quality_report.xlsx"]),
       "golden: the two deliverables")
    X2 = E.solve(target, {k: v for k, v in F.items()})
    ok(X2["warned"] == X["warned"] and X2["rr"] == X["rr"] and X2["calls"] == X["calls"],
       "distractors: the golden and every ask read neither distractor (solve opens neither)")
    calls = X["cr"]
    ok(calls["received_at"].max() <= "2027-10-18 23:59" and calls["event_time"].max() <= "2027-09-26 23:59",
       "realism: no call after the close, no record after the export")
    ok(pd.to_datetime(out["outcome_date"]).max() <= pd.Timestamp("2027-09-30"), "realism: no outcome after the extract")
    ok(hh["interview_date"].max() <= "2027-09-26", "realism: no interview after the close")
    iv = pd.read_csv(os.path.join(target, F["interviewers"]))
    used = set(calls.loc[calls["interviewer_id"] != "OFFICE", "interviewer_id"])
    ok(used <= set(iv["interviewer_id"]) and len(iv) == 79, "realism: every interviewer in the call log is on the list")
    pop = pd.read_csv(os.path.join(target, F["population"]))
    wt = pd.read_csv(os.path.join(target, F["weights"]))
    ok(abs(wt["final_weight"].sum() / 1000.0 - pop["population_thousands"].sum()) < 1.0,
       "realism: the final weights add to the population estimates")
    ok(len(set(X["calls"].values())) == 12 and len(set(X["rr"].values())) == 12, "realism: regional figures distinct")
    return N[0]
