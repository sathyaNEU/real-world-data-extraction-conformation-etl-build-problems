"""Every assertion the build stands on. Run from build.py or on its own against a cut bundle."""
import csv
import datetime as dt
import hashlib
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

# the files the call reads that no ask touches, and the call's own rows, as the shipped commit holds them
SHIPPED_FILES = {
    "surface_water_quality_regulations_2019.pdf": "82e8b4a35649f3f7b7cc578dcbede800820b91979fae85437cba42b72d63fbbe",
    "water_body_register.csv": "9fed7ca286f8dfefc0eb01b0e1ecf2fc41acc5959af5736cde3905d7b9d9fad5",
    "monitoring_point_crosswalk.csv": "22d5df82c50c5bf5b74bb639e99fa63ef674c64bdd9abd6c78edafeefd8ae3c0",
}
SHIPPED_PEST = "f1b008379298ac18f5253a36c99c8d40fb3eada888f1e1caba5bcfa7b9046291"
SHIPPED_PROGRAMME = "86728b59fa44cbd0c9b13b0458dfd0e228d564317ba0cea43293de587f2010ea"


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
    # the method schedule renders every nutrient determinand the export carries under each method
    with pdfplumber.open(os.path.join(target, "laboratory_method_schedule.pdf")) as pdf:
        dic = re.sub(r"\s+", " ", " ".join(p.extract_text() or "" for p in pdf.pages))
    A("NO3, NH4N, TON, CL," in dic and "SO4, OPO4" in dic,
      "the method schedule does not list the Tirneevin nutrient determinands")
    nut_methods = d[d["programme"] == "NUT"].groupby("method_code")["determinand_code"].unique()
    for mcode, dets in nut_methods.items():
        A(set(dets) <= set(W.METHODS[mcode]["analytes"]),
          "%s carries %s outside its schedule" % (mcode, sorted(set(dets) - set(W.METHODS[mcode]["analytes"]))))
    A(not any(f.startswith(("lims_field_dictionary", "export_manifest")) for f in os.listdir(target)),
      "a describing file ships")
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
    rows = PK.build_rows()
    dev = [r for r in rows if r.get("_copy_of") or r.get("_rebooked") or r.get("_misbooked_to")]
    A(len(dev) > 0 and all(r["programme"] == "NUT" and r["sample_type"] == "FIELD" for r in dev),
      "separation: a device row outside the nutrient suite's field bottles")
    A(not any(r["_month"] in ((2025, 10), (2025, 11), (2025, 12)) for r in dev),
      "separation: a device row in the quarter the laboratories' reports cover")
    A(not m["determinand_code"].isin(["NO3", "NO3N", "OPO4"]).any(),
      "separation: a nutrient determinand is in the main population")
    A(len(set(m["point"])) == 37, "separation: the compliance network is %d points" % len(set(m["point"])))
    A(len(m) == 427, "the main population is %d rows" % len(m))
    # the call's own files and rows are the shipped commit's, byte for byte
    for f, h in SHIPPED_FILES.items():
        A(hashlib.sha256(open(os.path.join(target, f), "rb").read()).hexdigest() == h,
          "separation: %s differs from the shipped commit" % f)
    lines = open(os.path.join(target, PK.FILES["export"]), encoding="utf-8").read().splitlines()
    pcol = lines[0].split(",").index("programme")
    pest = [ln for ln in lines[1:] if next(csv.reader([ln]))[pcol] == "PEST"]
    A(len(pest) == 1898 and hashlib.sha256("\n".join(pest).encode()).hexdigest() == SHIPPED_PEST,
      "separation: the pesticide suite's rows differ from the shipped commit")
    cells = ["|".join(str(pr.iloc[i, j]) for j in (0, 1, 2, 3, 4, 7, 8, 9)) for i in range(len(pr))
             if isinstance(pr.iloc[i, 0], str) and pr.iloc[i, 0].startswith("ARW-")]
    A(hashlib.sha256("\n".join(cells).encode()).hexdigest() == SHIPPED_PROGRAMME,
      "separation: the programme's points, laboratories, pesticide rounds or dates moved")

    # ---- the construction figures behind Critical Components 1 and 4 ------------------------------
    a1 = g["a1"]
    A(sum(v[0] for v in a1.values()) == 427, "A1 sample counts do not sum to the population")
    A(a1["Cloonfad"] == (36, 11) and a1["Owenbeg"] == (47, 31) and a1["Tirneevin Stream"] == (30, 20)
      and a1["Ballynure"] == (47, 35) and a1["Derryvore"] == (35, 25), "A1 moved: %s" % a1)

    # ---- the ask: the return's ortho-phosphate figures for each water body ----------------------
    w = g["w"]
    A(len(w) == 13, "the ask covers %d water bodies" % len(w))
    # the golden, read from the shipped files, is the generator's own truth: one entry per bottle at
    # the point it was taken, inside the point's programme dates, with an approved result
    pts = G.programme_points(pr)
    dates = G.programme_dates(pr)
    wbn = {}
    for (name, code, old, catch, area, tgt, points) in W.WATER_BODIES:
        for (suffix, lab, pf, place) in points:
            wbn["ARW-" + suffix] = name
    last = {}
    for r in rows:
        if r["programme"] == "NUT" and r["sample_type"] == "FIELD" and r["determinand_code"] == "OPO4":
            k = (r["lab_sample_id"], r["determinand_code"])
            if k not in last or int(r["version"]) > int(last[k]["version"]):
                last[k] = r
    wtruth = {}
    for r in last.values():
        if r.get("_copy_of") or r.get("_rebooked") or r["result_status"] != "A":
            continue
        p = r["_point"]
        dd_ = dt.date.fromisoformat(r["sample_date"])
        if p not in pts or not (dates[p][0] <= dd_ <= dates[p][1]) or not (W.YEAR_FROM <= dd_ <= W.YEAR_TO):
            continue
        n_, nd_ = wtruth.get(wbn[p], (0, 0))
        wtruth[wbn[p]] = (n_ + 1, nd_ + (1 if r["qualifier"] == "<" else 0))
    A(wtruth == w, "the ask's golden does not recompute the truth: %s against %s" % (w, wtruth))

    bk, _xw, _rg, _pr = G.bookings(target)
    # every nutrient bottle's determinands share one collection date, time and receipt, and its total
    # oxidised nitrogen is at least its nitrate as nitrogen
    per = {}
    for r in rows:
        if r["programme"] == "NUT" and r["sample_type"] == "FIELD" and not r.get("_copy_of") \
                and not r.get("_rebooked"):
            per.setdefault((r["_point"], r["_month"]), set()).add(
                (r["sample_date"], r["sample_time"], r["date_received"]))
    A(all(len(v) == 1 for v in per.values()), "a nutrient bottle's determinands carry two dates")
    for b in bk:
        sig = dict((det, res) for (det, res, q) in b["sig"])
        ton = float(sig["TON"]) if sig.get("TON") else None
        nit = float(sig["NO3N"]) if sig.get("NO3N") else (float(sig["NO3"]) / W.NO3_FACTOR if sig.get("NO3") else None)
        if ton is not None and nit is not None:
            A(ton >= nit, "TON below nitrate as N at %s %s" % (b["point"], b["date"]))

    # device 1, one bottle under two bookings at one point: every pair the rule merges is one of the
    # reception's double bookings, its two bookings carrying identical results for every determinand,
    # the same receipt and dates one to three days apart, and no two other bookings at a point agree
    by_pt = {}
    for b in bk:
        by_pt.setdefault((b["lab"], b["point"], b["received"], b["sig"]), []).append(b)
    pairs = [v for v in by_pt.values() if len(v) > 1]
    A(len(pairs) == len(W.DOUBLE_BOOKED) and all(len(v) == 2 for v in pairs),
      "device 1: %d merged pairs against %d double bookings" % (len(pairs), len(W.DOUBLE_BOOKED)))
    A(all(1 <= abs((v[0]["date"] - v[1]["date"]).days) <= 3 for v in pairs),
      "device 1: a double booking's dates are not one to three days apart")
    sched = {id(min(v, key=lambda z: z["date"])) for v in pairs}     # the pre-registration's dates
    nres = [len([x for x in b["sig"] if x[1]]) for v in pairs for b in v]
    A(min(nres) >= 4, "device 1: a double booking carries fewer than four quantified results")
    # device 2, one bottle under two points: the bottle the reception booked to a compliance point's
    # open slot and later booked again under the operational point it was taken at carries identical
    # rows under both, the second booking newer; the compliance point has no other bottle that month
    by_b = {}
    for b in bk:
        by_b.setdefault((b["lab"], b["date"], b["time"], b["received"], b["sig"]), []).append(b)
    twins = [v for v in by_b.values() if len({x["point"] for x in v}) > 1]
    A(len(twins) == len(W.MISBOOKED) and all(len(v) == 2 for v in twins),
      "device 2: %d cross-point twins against %d misbookings" % (len(twins), len(W.MISBOOKED)))
    for (wrong, own, y, mo) in W.MISBOOKED:
        tw = [v for v in twins if {x["point"] for x in v} == {wrong, own} and v[0]["date"].month == mo]
        A(len(tw) == 1, "device 2: no twin for %s and %s" % (wrong, own))
        v = tw[0]
        mis = [x for x in v if x["point"] == wrong][0]
        reb = [x for x in v if x["point"] == own][0]
        A(reb["newest"] > mis["newest"], "device 2: the booking at %s is not the newer booking" % own)
        others = [b for b in bk if b["point"] == wrong and (b["date"].year, b["date"].month) == (y, mo)
                  and b is not mis]
        A(not others, "device 2: %s has its own bottle in %d-%02d" % (wrong, y, mo))
    # device 3, a code the laboratory's numbering gives two points: Tirneevin numbers a point by its
    # catchment and the last two digits of its number, so two operational points carry a compliance
    # point's code and have no crosswalk row of their own
    sc = G.shared_codes(target, xw, rg)
    A(sc == {("TAS", "ARWA-BN-22"): ("ARW-0322", "ARW-2122"), ("TAS", "ARWA-CB-41"): ("ARW-1041", "ARW-2241")},
      "device 3: the shared codes moved: %s" % sc)
    A(not set(xw["sample_point_code"]) & {"ARW-2122", "ARW-2241"}, "device 3: an operational point has a row")
    bn = {}
    for b in bk:
        if (b["lab"], b["code"]) == ("TAS", "ARWA-BN-22"):
            bn.setdefault((b["date"].year, b["date"].month), []).append(b)
    A(len(bn) == 12 and all(len(v) == 2 for v in bn.values()),
      "device 3: ARWA-BN-22 does not carry two nutrient bottles in each month")
    cb = [b for b in bk if (b["lab"], b["code"]) == ("TAS", "ARWA-CB-41")]
    kg = [b for b in bk if b["point"] == "ARW-1041" and b["lab"] == "KGL"]
    A(len(cb) == 12 and len(kg) == 11, "device 3: Carrowbeg's two series are %d and %d" % (len(cb), len(kg)))

    # the referee, the monthly visit: a compliance point's nutrient bottle is filled on the visit that
    # takes its pesticide sample, so it carries that sample's collection date and time. Measured from
    # the shipped files: every booking under a compliance point's code falls on one of the point's
    # visits except the three devices' bookings, and every device booking falls on none
    vis = G.visits(target)
    comp_pts = set(vis)
    A(len(comp_pts) == 37 and sum(len(v) for v in vis.values()) == 427,
      "the visits are %d points and %d visits" % (len(comp_pts), sum(len(v) for v in vis.values())))
    for r in rows:
        if r["programme"] == "NUT" and r["sample_type"] == "FIELD" and r["_point"] in comp_pts \
                and not r.get("_copy_of") and not r.get("_misbooked_to"):
            A((dt.date.fromisoformat(r["sample_date"]), r["sample_time"]) in vis[r["_point"]],
              "a compliance point's own bottle is off its visit: %s %s" % (r["_point"], r["sample_date"]))
    at_comp = [b for b in bk if b["point"] in comp_pts]
    on = [b for b in at_comp if (b["date"], b["time"]) in vis[b["point"]]]
    off = [b for b in at_comp if (b["date"], b["time"]) not in vis[b["point"]]]
    seen_v = {}
    for b in on:
        seen_v[(b["point"], b["date"], b["time"])] = seen_v.get((b["point"], b["date"], b["time"]), 0) + 1
    A(max(seen_v.values()) == 1, "a visit carries two nutrient bookings")
    n_copy = sum(1 for (pnt, y, m, k) in W.DOUBLE_BOOKED if pnt in comp_pts)
    A(len(off) == n_copy + len(W.MISBOOKED) + 12 + 12,
      "the off-visit bookings at compliance points are %d, not %d" % (len(off), n_copy + len(W.MISBOOKED) + 24))
    devkeys = set()
    for r in rows:
        if r["programme"] == "NUT" and r["sample_type"] == "FIELD" and (
                r.get("_copy_of") or r.get("_misbooked_to") or r["_point"] in ("ARW-2122", "ARW-2241")):
            devkeys.add((r["lab_code"], r["client_point_code"], r["sample_date"], r["sample_time"]))
    A(all((b["lab"], b["code"], b["date"].isoformat(), b["time"]) in devkeys for b in off),
      "an off-visit booking at a compliance point is not a device booking")
    A(not any((b["lab"], b["code"], b["date"].isoformat(), b["time"]) in devkeys for b in on),
      "a device booking falls on a visit")
    # device 2's forcing: each bottle under two points was taken on a day its compliance point was not
    # visited (13 of 13, the day itself differs), the point's visit that month left no booked bottle
    for (wrong, own, yy, mo) in W.MISBOOKED:
        mis = [b for b in off if b["point"] == wrong and (b["date"].year, b["date"].month) == (yy, mo)]
        vday = [vd for (vd, vt) in vis[wrong] if (vd.year, vd.month) == (yy, mo)]
        A(len(mis) == 1 and len(vday) == 1 and mis[0]["date"] != vday[0],
          "device 2: %s's bottle of %d-%02d is not dated off the point's visit" % (wrong, yy, mo))
        A(not [b for b in on if b["point"] == wrong and (b["date"].year, b["date"].month) == (yy, mo)],
          "device 2: %s's visit of %d-%02d has a booked bottle" % (wrong, yy, mo))
    # device 1's forcing: each second booking is dated one to three days before a visit of its point and
    # repeats that visit's bottle result for result
    for (pnt, yy, mm, _k) in W.DOUBLE_BOOKED:
        if pnt not in comp_pts:
            continue
        cp = [b for b in off if b["point"] == pnt and (b["date"].year, b["date"].month) == (yy, mm)]
        vb = [b for b in on if b["point"] == pnt and (b["date"].year, b["date"].month) == (yy, mm)]
        A(len(cp) == 1 and len(vb) == 1 and cp[0]["sig"] == vb[0]["sig"]
          and 1 <= (vb[0]["date"] - cp[0]["date"]).days <= 3,
          "device 1: %s %d-%02d is not one bottle booked a few days before its visit" % (pnt, yy, mm))
    # device 3's forcing: none of the Tirneevin ARWA-CB-41 nutrient bottles falls on a visit of
    # ARW-1041, whose pesticide samples carry that code, and all of its Kilgarron bottles do; each month
    # exactly one of the two ARWA-BN-22 bottles falls on ARW-0322's visit
    A(not any((b["date"], b["time"]) in vis["ARW-1041"] for b in cb), "device 3: a CB-41 bottle is on a visit")
    A(all((b["date"], b["time"]) in vis["ARW-1041"] for b in kg), "device 3: an ARW-1041 bottle is off its visit")
    A(not any(b["date"] in {vd for (vd, vt) in vis["ARW-1041"]} for b in cb),
      "device 3: a CB-41 bottle shares a day with an ARW-1041 visit")
    A(all(sum(1 for b in v if (b["date"], b["time"]) in vis["ARW-0322"]) == 1 for v in bn.values()),
      "device 3: ARWA-BN-22 does not carry exactly one bottle on ARW-0322's visit each month")
    # the golden is the visit reading, and every booking it keeps is the generator's own truth
    A(len(on) == sum(v[0] for v in w.values()) + sum(1 for b in on if b["opo4"][0] != "A"),
      "the visit reading and the golden disagree on the number of bottles")

    # "below the reporting limit" reads the same from the qualifier and from the value against the row's
    # own limit: no quantified result sits under the limit its method achieved, at either laboratory
    q = d[(d["sample_type"] == "FIELD") & (d["programme"] == "NUT") & (d["qualifier"] != "<")]
    A(not (pd.to_numeric(q["result"]) < pd.to_numeric(q["reporting_limit"])).any(),
      "a quantified nutrient result sits below its own reporting limit")
    # the chart's footnote: every Tirneevin ortho-phosphate result sits below its 0.10 mg/l limit
    tas_op = d[(d["determinand_code"] == "OPO4") & (d["lab_code"] == "TAS") & (d["sample_type"] == "FIELD")]
    A(len(tas_op) > 0 and (tas_op["qualifier"] == "<").all() and (tas_op["reporting_limit"] == "0.1000").all(),
      "the chart's footnote is false: a Tirneevin ortho-phosphate result is quantified")
    # the late bookings are numbered with ordinary late-paperwork bottles, so no number range isolates them
    tas = d[d["lab_code"] == "TAS"].copy()
    tas["n"] = tas["lab_sample_id"].str.split("/").str[2].astype(int)
    tail = tas.sort_values("n").tail(len(dev) + 6 * W.LATE_PAPERWORK)
    devid = {r["lab_sample_id"] for r in rows if r.get("_copy_of") or r.get("_rebooked")}
    A(tail["lab_sample_id"].isin(devid).mean() < 0.5,
      "the late-numbered block is mostly device bookings (%.2f)" % tail["lab_sample_id"].isin(devid).mean())

    # every reading short of the three reconstructions misses every cell, measured on this pack
    import ceiling as CL
    for name, resp in (("cracker", CL.handled(target, False, False, False)),
                       ("plan reader", CL.plan_reader(target)),
                       ("one bottle a month", CL.one_a_month(target)),
                       ("double booking only", CL.handled(target, True, False, False)),
                       ("re-booking only", CL.handled(target, False, True, False)),
                       ("shared code only", CL.handled(target, False, False, True))):
        kept = CL.score(resp, w)[0]
        A(kept == 0, "the %s keeps %d of 26 ask cells" % (name, kept))
    A(CL.handled(target, True, True, True) == w, "the full includer does not reach the golden")

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
    # the write-up states both as lower bounds, so neither printed figure may exceed the clearance
    # the pack actually holds (11.54 printed as 12 was a claim no water body met)
    nc_true = min(min(o[k] for k in reads) for o in g["assess"].values() if o["mle"] > S)
    co_true = max(max(o[k] for k in reads) for o in g["assess"].values() if o["mle"] <= S)
    A(fj["nearest_compliant_pct_below"] <= 100 * (S - co_true) / S,
      "figures.json claims %d per cent clear below, the pack holds %.2f"
      % (fj["nearest_compliant_pct_below"], 100 * (S - co_true) / S))
    A(fj["nearest_non_compliant_pct_above"] <= 100 * (nc_true - S) / S,
      "figures.json claims %d per cent clear above, the pack holds %.2f"
      % (fj["nearest_non_compliant_pct_above"], 100 * (nc_true - S) / S))
    A(fj["programme_points"] == len(set(m["point"])), "figures.json programme points")
    A(fj["legacy_limit_over_standard"] == 2.0, "figures.json the legacy limit against the standard")
    A(fj["orthophosphate"] == {k: {"samples": v[0], "below_limit": v[1]} for k, v in g["w"].items()},
      "figures.json orthophosphate")
    return N[0]


if __name__ == "__main__":
    t = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "target")
    n = run(t)
    print("checks passed:", n)
