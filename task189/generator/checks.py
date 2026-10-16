"""Every assertion the build stands on. Run from build.py or on its own against a cut bundle."""
import datetime as dt
import json
import os
import re
import sys

import pandas as pd
import pdfplumber

import est
import golden as G
import pack as PK
import sim
import world as W

N = [0]


def A(cond, msg):
    N[0] += 1
    if not cond:
        raise AssertionError(msg)


def reg_text(target):
    with pdfplumber.open(os.path.join(target, "surface_water_quality_regulations_2019.pdf")) as pdf:
        return re.sub(r"\s+", " ", " ".join(p.extract_text() or "" for p in pdf.pages))


def run(target):
    task = os.path.dirname(os.path.dirname(os.path.abspath(target.rstrip("/"))))
    task = os.path.dirname(os.path.abspath(target.rstrip("/")))
    ex, xw, rg, ab, pr = G.load(target)
    d = G.conform(ex, xw)
    g = G.compute(target)
    m, _rg = G.mcpa_population(target)
    S = W.STANDARD

    # ---- input gates ---------------------------------------------------------------------------
    files = sorted(os.listdir(target))
    A(len(files) >= 10, "input gate: %d files" % len(files))
    exts = set(os.path.splitext(f)[1] for f in files)
    A(len(exts) >= 3, "input gate: formats %s" % exts)
    A(len(ex) >= 25000, "input gate: the export holds %d rows" % len(ex))
    meta = json.load(open(os.path.join(task, "metadata.json"), encoding="utf-8"))
    A(len(meta["distractor_files"]) >= 2, "input gate: distractors")
    for dis in meta["distractor_files"]:
        A(dis["file"] in files, "distractor %s is in the bundle" % dis["file"])
        A("distractor" not in dis["file"], "a distractor names itself")

    # ---- the call ------------------------------------------------------------------------------
    A(g["count"] == 4, "the call is 4, got %s" % g["count"])
    A(g["non_compliant"] == ["Cloonfad", "Glasheen", "Kilcrohane", "Owenbeg"],
      "the non-compliant set moved: %s" % g["non_compliant"])
    A(len(g["assess"]) == 13, "13 water bodies assessed, got %d" % len(g["assess"]))

    # ---- R1 the three rules: the analyst test, executed on the generator's clean truth ---------
    # The easy route is run on the truth the generator holds, with every field read correctly and
    # every filed rule applied, and it still files the wrong count.
    truth = {}
    for wb in W.WATER_BODIES:
        rows = sim.mcpa_rows(wb)
        tp = sim.tuples(rows)
        sens = [t for r, t in zip(rows, tp) if r["lab"] == "TAS"]
        truth[wb[0]] = {"truth": sum(r["true"] for r in rows) / len(rows),
                        "half": est.substitute(tp, "half"),
                        "zero": est.substitute(tp, "zero"),
                        "full": est.substitute(tp, "full"),
                        "drop": est.substitute(tp, "drop"),
                        "mle": est.mle_fill([t[2] for t in tp], [t[3] for t in tp],
                                            [t[4] for t in tp]),
                        "km": est.km_mean([t[2] for t in tp], [t[3] for t in tp], [t[4] for t in tp]),
                        "cond": est.cond_fill(tp, sens)}
    cnt = lambda k: sum(1 for v in truth.values() if v[k] > S)
    A(cnt("half") == 7, "R1 the easy route on clean truth files 7, got %d" % cnt("half"))
    A(cnt("truth") == 4, "R1 the clean truth files 4, got %d" % cnt("truth"))
    # changing the decisive step alone, with the same clean data, gives the golden
    A(cnt("mle") == 4 and cnt("km") == 4 and cnt("cond") == 4,
      "R1 the censored estimators on clean truth: %s" % [cnt(k) for k in ("mle", "km", "cond")])
    # R2 the stump is not a reading: every constant substitution is a different wrong count
    A(cnt("zero") == 3 and cnt("full") == 11 and cnt("drop") == 8,
      "R2 substitutions: %s" % [cnt(k) for k in ("zero", "full", "drop")])
    # R3a nothing planted: no copied block, and every MCPA value is its own draw
    vals = [r.val_ugl for r in m.itertuples() if r.det]
    A(len(set("%.9f" % v for v in vals)) == len(vals),
      "R3a the quantified MCPA values are distinct draws, %d of %d" % (len(set(vals)), len(vals)))
    # R3b no filed sentence names a substitution, an estimator or what a non-detect contributes
    words = []
    for f in files:
        if f.endswith(".pdf"):
            with pdfplumber.open(os.path.join(target, f)) as pdf:
                words.append(" ".join(p.extract_text() or "" for p in pdf.pages))
        elif f.endswith((".csv", ".json")):
            words.append(open(os.path.join(target, f), encoding="utf-8", errors="ignore").read())
    blob = re.sub(r"\s+", " ", " ".join(words)).lower()
    for banned in ("half the reporting limit", "half the limit", "substitut", "censor",
                   "kaplan", "maximum likelihood", "regression on order", "non-detect",
                   "treat as zero", "divided by two", "nondetect"):
        A(banned not in blob, "R3b a shipped file says '%s'" % banned)
    # R3c no shipped artifact assesses or ranks the water bodies
    for bad in ("non-compliant", "noncompliant", "compliance assessment of", "assessed as"):
        A(bad not in blob or bad == "non-compliant", "R3c a shipped file assesses: %s" % bad)
    A("non-compliant" not in re.sub(r"\s+", " ", " ".join(
        w for w in words if "Regulations" not in w[:400])).lower(),
      "R3c only the regulations use the word non-compliant")

    # ---- the ladder ----------------------------------------------------------------------------
    L = g["rungs"]
    A(L["half"] == 7 and L["zero"] == 3 and L["full"] == 11 and L["drop"] == 8
      and L["own_points"] == 3, "the ladder moved: %s" % L)
    A(len({L["half"], L["zero"], L["full"], L["drop"], g["count"]}) == 5,
      "the rungs are not distinct: %s" % L)

    # ---- convergence and margins ---------------------------------------------------------------
    for code, o in g["assess"].items():
        for k in ("mle", "km", "cond", "fitted_dist"):
            A((o[k] > S) == (o["mle"] > S),
              "%s: %s and mle disagree (%.4f, %.4f)" % (o["name"], k, o[k], o["mle"]))
            A(abs(o[k] - S) / S >= 0.10,
              "%s: %s is %.1f per cent from the standard" % (o["name"], k, 100 * abs(o[k] - S) / S))
        A(abs(truth[o["name"]]["truth"] - S) / S >= 0.10, "%s: the truth sits near the line" % o["name"])
        A((truth[o["name"]]["truth"] > S) == (o["mle"] > S),
          "%s: the estimate and the truth disagree" % o["name"])
    # the corridor the count survives
    reads = ("mle", "km", "cond", "fitted_dist")
    ex_lo = min(min(o[k] for k in reads) for o in g["assess"].values() if o["mle"] > S)
    co_hi = max(max(o[k] for k in reads) for o in g["assess"].values() if o["mle"] <= S)
    A(co_hi < S < ex_lo, "the corridor is broken: %.4f %.4f" % (co_hi, ex_lo))
    A(ex_lo / S >= 1.10 and co_hi / S <= 0.92, "corridor margins %.3f %.3f" % (ex_lo / S, co_hi / S))

    # ---- the semantic fork table ---------------------------------------------------------------
    # SF1 the water body code: the 2024 revision renamed and merged none
    A(len(set(rg["water_body_code"])) == len(rg) == len(set(rg["code_before_2024_revision"])),
      "SF1 the register's codes are not one to one")
    # SF2 compliance samples: the QC rows are typed and excluded
    A(set(d["sample_type"]) >= {"FIELD", "FIELD_BLANK", "FIELD_DUP", "LAB_DUP", "MATRIX_SPIKE"},
      "SF2 the QC types are missing")
    A((m["sample_type"] == "FIELD").all(), "SF2 a QC row reached the main population")
    # SF3 the reporting year
    A(m["sdate"].min() >= W.YEAR_FROM and m["sdate"].max() <= W.YEAR_TO, "SF3 the window leaks")
    cal2025 = d[(d["determinand_code"] == "MCPA") & (d["sample_type"] == "FIELD")
                & (d["sample_date"].str[:4] == "2025")]
    A(len(cal2025) != len(m), "SF3 the calendar year and the reporting year coincide")
    # SF4 the date of collection against receipt and approval: nothing on the boundary
    gap_lo = min((x - W.YEAR_FROM).days for x in m["sdate"])
    gap_hi = min((W.YEAR_TO - x).days for x in m["sdate"])
    A(gap_lo >= 5 and gap_hi >= 5, "SF4 a sample sits on the year boundary (%d, %d)" % (gap_lo, gap_hi))
    rec = pd.to_datetime(m["date_received"]).dt.date
    A(all(W.YEAR_FROM <= r <= W.YEAR_TO for r in rec), "SF4 a receipt date leaves the year")
    # SF5 the governing version: no MCPA result has a second version or a withdrawal
    mc_all = d[(d["determinand_code"] == "MCPA") & (d["sample_type"] == "FIELD")]
    A((mc_all["version"] == "1").all(), "SF5 an MCPA result carries a second version")
    A((mc_all["result_status"] == "A").all(), "SF5 an MCPA result is provisional or withdrawn")
    # SF6 weighting: clause 7.2 files it, so the per point reading violates a quotable sentence
    A("each sample weighted equally" in reg_text(target),
      "SF6 clause 7.2 does not file the weighting")
    pp = 0
    for code, grp in m.groupby("wb_code"):
        per_point = [est.mle_fill(list(pg["val_ugl"]), list(pg["rl_ugl"]), list(pg["det"]))
                     for p, pg in grp.groupby("point")]
        pp += 1 if (sum(per_point) / len(per_point)) > S else 0
    A(pp != g["count"], "SF6 the per point reading is not separated from the filed one")
    # SF13 the average is of the samples, not of a distribution fitted to them
    reg = reg_text(target)
    A("the mean of the concentrations of the compliance samples" in reg
      and "one concentration for each of those samples" in reg,
      "SF13 clause 7.2 does not file the average as the mean of the samples")
    A("shall not report in place of the average any property of a distribution fitted to them" in reg,
      "SF13 clause 7.2 does not exclude a fitted distribution's own mean")
    A(L["fitted_dist"] == g["count"],
      "SF13 the fitted distribution reading no longer converges on the filed average (%d)"
      % L["fitted_dist"])
    for code, o in g["assess"].items():
        A((o["fitted_dist"] > S) == (o["mle"] > S),
          "SF13 the fitted distribution reading flips %s" % o["name"])
        A(abs(o["fitted_dist"] - S) / S >= 0.10,
          "SF13 %s sits %.1f per cent from the standard under the fitted reading"
          % (o["name"], 100 * abs(o["fitted_dist"] - S) / S))
    # SF14 the nitrate basis is in the pack, so no graded figure rests on an outside constant
    with pdfplumber.open(os.path.join(target, "lims_field_dictionary.pdf")) as pdf:
        dic = re.sub(r"\s+", " ", " ".join(p.extract_text() or "" for p in pdf.pages))
    A("4.4268 times smaller than the same water under NO3" in dic,
      "SF14 the dictionary's nitrate basis is clipped on the rendered page")
    for fld in ("lab_sample_id", "client_point_code", "sample_type", "determinand_code", "qualifier",
                "reporting_limit", "result_status", "version", "batch_id"):
        A(fld in dic, "SF14 the dictionary clips the %s row" % fld)
    with pdfplumber.open(os.path.join(target, "laboratory_method_schedule.pdf")) as pdf:
        sch = re.sub(r"\s+", " ", " ".join(p.extract_text() or "" for p in pdf.pages))
    for code in W.METHODS:
        A(code in sch, "the method schedule breaks %s across lines" % code)
    A("0.005 (5 ng/l)" in sch and "0.100" in sch,
      "the method schedule does not render both reporting limits")
    # SF7 units: both appear and every averaged value is in ug/l
    A(set(mc_all["units"]) == {"ng/l", "ug/l"}, "SF7 one unit only")
    ngl = pd.to_numeric(mc_all.loc[mc_all["units"] == "ng/l", "result"], errors="coerce")
    A(float(ngl.max()) > 1.0, "SF7 the ng/l rows do not look like ng/l")
    A(m["val_ugl"].max() < 5.0, "SF7 an unconverted value reached the average")
    # SF8 the qualifier
    nd = m[~m["det"]]
    A((nd["result"] == "").all(), "SF8 a non-detect row carries a value in the result field")
    A((nd["reporting_limit"] != "").all(), "SF8 a non-detect row carries no reporting limit")
    A(len(set(nd["rl_ugl"].round(6))) == 2, "SF8 the two reporting limits are not both in play")
    # SF9 the standard
    with pdfplumber.open(os.path.join(target, "surface_water_quality_regulations_2019.pdf")) as pdf:
        reg = re.sub(r"\s+", " ", " ".join(p.extract_text() or "" for p in pdf.pages))
    A("MCPA 0.05 ug/l annual average" in reg, "SF9 Schedule 2 does not carry the standard")
    A("the figure set out beside it in Schedule 2" in reg, "SF9 clause 7.3 is not filed")
    # SF10 the inequality
    A(all(abs(o["mle"] - S) / S >= 0.10 for o in g["assess"].values()), "SF10 an estimate is on the line")
    # SF11 the rounding path
    for nd_ in (2, 3):
        c = sum(1 for o in g["assess"].values() if round(o["mle"], nd_) > S)
        A(c == g["count"], "SF11 rounding to %d decimals gives %d" % (nd_, c))
    # SF12 the district: the register's surveillance water bodies are outside the programme
    A(len(rg) == 16 and len(g["assess"]) == 13, "SF12 the register and the programme coincide")
    A(set(m["wb_code"]) == set(rg.loc[rg["network"] == "compliance", "water_body_code"]),
      "SF12 the population is not the programme's water bodies")
    A(set(m["point"]) == G.programme_points(pr), "SF12 the population is not the programme's points")
    A((rg["network"] == "surveillance").sum() == 3, "SF12 the surveillance water bodies are missing")

    # ---- closure axes that need a row-level assertion -------------------------------------------
    for perm in (1, 2, 3):
        sh = ex.sample(frac=1.0, random_state=perm).reset_index(drop=True)
        dd = G.conform(sh, xw)
        gg = G.governing(dd)
        mm = gg[(gg["determinand_code"] == "MCPA") & (gg["sdate"] >= W.YEAR_FROM)
                & (gg["sdate"] <= W.YEAR_TO)]
        A(len(mm) == len(d[(d["determinand_code"] == "MCPA") & (d["sample_type"] == "FIELD")
                           & (d["sdate"] >= W.YEAR_FROM) & (d["sdate"] <= W.YEAR_TO)]),
          "axis 14 row order changes the population")
    A(len(set(zip(m["lab_sample_id"], m["determinand_code"]))) == len(m),
      "axis 15 the main population holds a duplicate pair")
    A(set(xw["sample_point_code"]) >= set(m["point"]), "axis 16 a point is not crosswalked")
    A((m["val_ugl"] >= 0).all(), "axis 17 a negative concentration")

    # ---- the separation line: zero device rows in the main population ---------------------------
    A(not (m["client_point_code"].str.endswith(("-WS", "W"))).any(),
      "separation: a water services submission is in the main population")
    A(not m["determinand_code"].isin(["NO3", "NO3N", "OPO4"]).any(),
      "separation: an ask determinand is in the main population")
    A(len(set(m["point"])) == 37, "separation: the compliance network is %d points" % len(set(m["point"])))
    A(len(m) == 427, "the main population is %d rows" % len(m))

    # ---- the asks ------------------------------------------------------------------------------
    a1 = g["a1"]
    A(sum(v[0] for v in a1.values()) == 427, "A1 sample counts do not sum to the population")
    A(a1["Cloonfad"] == (36, 11) and a1["Owenbeg"] == (47, 31) and a1["Tirneevin Stream"] == (30, 20),
      "A1 moved: %s" % a1)
    lazy_all = d[(d["determinand_code"] == "MCPA") & d["point"].isin(set(m["point"]))]
    for code, grp in m.groupby("wb_code"):
        name = g["assess"][code]["name"]
        lz = len(lazy_all[lazy_all["point"].isin(set(grp["point"]))])
        A(lz != a1[name][0], "A1 the lazy read matches at %s (%d)" % (name, lz))
    a2 = g["a2"]
    A(len(a2) == 6, "A2 covers %d points" % len(a2))
    A(a2["Gortaleen Borehole"] == (65.9, 25) and a2["Cloonfad Spring Chamber"] == (35.5, 0)
      and a2["Ballynure Borehole 1"] == (50.7, 14) and a2["Rathvilly Borehole 2"] == (41.3, 3)
      and a2["Sheskin Shallow Well"] == (60.1, 19) and a2["Moneycashen Intake"] == (28.5, 0),
      "A2 moved: %s" % a2)
    # the lazy A2 read, no conversion and no duplicate resolution, misses every figure
    ex2, xw2, rg2, ab2, _ = G.load(target)
    dd2 = G.conform(ex2, xw2)
    gg2 = G.governing(dd2)
    raw = gg2[gg2["point"].isin(set(ab2["sample_point_code"]))
              & gg2["determinand_code"].isin(["NO3", "NO3N"])]
    for name, (mx, c) in a2.items():
        code = ab2.loc[ab2["sample_point_name"] == name, "sample_point_code"].iloc[0]
        sub = raw[raw["point"] == code]
        lazy_max = round(float(sub["val"].max()), 1)
        lazy_cnt = int((sub["val"] >= W.NITRATE_TRIGGER).sum())
        if name not in ("Cloonfad Spring Chamber", "Moneycashen Intake"):
            A(lazy_max != mx or lazy_cnt != c, "A2 the lazy read matches at %s" % name)
        else:
            A(lazy_max != mx, "A2 the conversion does not bite at %s" % name)
    # A2's counts hold under every conversion factor a chemist would use and under a rounded path,
    # so the one sample 0.07 per cent above the trigger cannot move a graded count; the maxima to one
    # decimal are forced by the factor the dictionary files.
    nref = g["a2"]
    anames = {r.sample_point_code: r.sample_point_name for r in ab.itertuples()}
    base = G.governing(d)
    base = base[base["point"].isin(set(ab["sample_point_code"]))
                & base["determinand_code"].isin(["NO3", "NO3N"])].copy()
    for factor, round1 in ((4.426802, False), (4.4268, False), (4.43, False), (4.427, False),
                           (4.426802, True), (4.43, True)):
        nn = base.copy()
        nn["no3"] = [v * (factor if cc == "NO3N" else 1.0)
                     for v, cc in zip(nn["val"], nn["determinand_code"])]
        if round1:
            nn["no3"] = nn["no3"].round(1)
        nn = nn.sort_values(["point", "sample_date", "sample_time", "client_point_code"])
        nn = nn.groupby(["point", "sample_date", "sample_time"], as_index=False).head(1)
        for code, grp in nn.groupby("point"):
            want = nref[anames[code]][1]
            got = int((grp["no3"] >= W.NITRATE_TRIGGER).sum())
            A(got == want, "A2 the count at %s moves to %d under factor %s (rounded %s)"
              % (anames[code], got, factor, round1))
    a3 = g["a3"]
    A(a3 == {"reports": 250, "export": 242, "one_only": 18}, "A3 moved: %s" % a3)
    A(a3["reports"] != a3["export"], "A3 the two totals agree")

    # ---- the clean-data and lens-swap tests -----------------------------------------------------
    # clean data: repair every Layer 1 item in the generator and the easy route still files 7
    A(cnt("half") == 7 and cnt("truth") == 4,
      "clean-data test: the easy route reaches the answer on clean truth")
    # lens swap: the easy route and the answer are not one quantity under two lenses, they are two
    # estimates of the same quantity, one of which adds a value the laboratory never measured
    added = sum((t[3] / 2.0) for wb in W.WATER_BODIES for t in sim.tuples(sim.mcpa_rows(wb))
                if not t[4])
    quantified = sum(t[2] for wb in W.WATER_BODIES for t in sim.tuples(sim.mcpa_rows(wb)) if t[4])
    truth_below = 0.0
    for wb in W.WATER_BODIES:
        rws = sim.mcpa_rows(wb)
        truth_below += sum(r["true"] for r in rws if not r["det"])
    A(added / quantified >= 0.25,
      "lens swap: the substituted mass is not material (%.3f of %.3f)" % (added, quantified))
    A(added >= 2.5 * max(truth_below, 1e-9),
      "lens swap: half the limit is near the truth below it (%.3f against %.3f)" % (added, truth_below))

    # ---- figures.json ---------------------------------------------------------------------------
    fj = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures.json"),
                        encoding="utf-8"))
    A(fj["call"] == g["count"], "figures.json call")
    A(fj["nearest_compliant_pct_below"] >= 11 and fj["nearest_non_compliant_pct_above"] >= 11,
      "figures.json margins are too narrow: %s" % [fj["nearest_compliant_pct_below"],
                                                   fj["nearest_non_compliant_pct_above"]])
    A(fj["programme_points"] == len(set(m["point"])), "figures.json programme points")
    A(fj["legacy_limit_over_standard"] == 2.0, "figures.json the legacy limit against the standard")
    A(fj["a3_quarter"] == g["a3"], "figures.json a3")
    return N[0]


if __name__ == "__main__":
    t = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "target")
    n = run(t)
    print("checks passed:", n)
