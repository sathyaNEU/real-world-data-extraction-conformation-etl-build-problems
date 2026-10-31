"""The generator's assertions on the built pack in task172/target: the call and its standing family, every fork
row of the design note (SF1 to SF24), the analyst test on the clean truth, every ask figure against the world's
own truth, device coverage and the separation line, and the leak and date sweeps.

    python3 task172/generator/checks.py [--fast]
"""
import datetime as dt
import math
import os
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
sys.path.insert(0, HERE)
import analysis as A  # noqa: E402
import records as RC  # noqa: E402
import survival as S  # noqa: E402
import world as W  # noqa: E402

FAST = "--fast" in sys.argv
NS = 1500 if FAST else 4000
results = []


def check(name, ok, detail=""):
    results.append((name, bool(ok), detail))
    print("%s  %s  %s" % ("PASS" if ok else "FAIL", name, detail), flush=True)


def main():
    P = A.Pack(TARGET)
    w = W.World()
    R = RC.Records(w)
    cut, nxt = A.find_cut(P)
    check("cut is the 165th event and the world's cut", cut == w.cut and (nxt is None or nxt > cut), "%s, next %s" % (cut, nxt))
    I = A.interim(P, cut)
    check("165 events at the cut", I["events"] == 165, str(I["events"]))
    check("every patient randomised by the cut (SF10)", I["n"] == 450, str(I["n"]))

    # the reader's PFS equals the world's own at the cut, patient by patient
    truth = {}
    for p in w.pts:
        t, kind = W.World.event_day(p, w.cut_rel)
        truth[p["rand_no"]] = (t, True) if t is not None else (kind, False)
    mism = [x["sid"] for x in I["d"]["rows"] if truth[x["sid"]] != (int(x["time"]), bool(x["event"]))]
    check("reader PFS equals the world's PFS for every patient", not mism, "%d mismatches %s" % (len(mism), mism[:5]))

    # the call and its rungs
    golden, _ = A.conditional_power(P, cut)
    check("golden conditional power rounds to 100 per cent (SF12)", golden >= 0.95, "%.4f" % golden)
    check("band C", A.band(golden) == "continue")
    check("PH reading, B-value with the stratified Cox ratio: band A", I["cp_trend"] < 0.20, "%.4f" % I["cp_trend"])
    check("sample-size ratio, excluded by charter 4.1: band B (SF7)", 0.20 <= I["cp_design"] < 0.80, "%.4f" % I["cp_design"])
    cp_ph, _ = A.conditional_power(P, cut, kind="ph", nsim=NS)
    check("PH projection patient by patient: band A", cp_ph < 0.20, "%.4f" % cp_ph)
    cp_exp, _ = A.conditional_power(P, cut, kind="pw", breaks=(), nsim=NS)
    check("constant rate per arm projection: band A", cp_exp < 0.20, "%.4f" % cp_exp)
    check("late-period ratio carried in the B-value lands band C", I["cp_late"] >= 0.80, "%.4f" % I["cp_late"])

    # SF8, SF9, SF6, SF5, SF4, SF13: the standing family keeps band C and the 100 per cent bin
    fam = {}
    for b in (91, 98, 112, 120, 122, 140, 152, 168, 183):
        fam["break %d" % b] = A.conditional_power(P, cut, breaks=(b,), nsim=NS)[0]
    fam["per assessment visit"] = A.conditional_power(P, cut, breaks=(63, 105, 147, 196), nsim=NS)[0]
    fam["two breaks"] = A.conditional_power(P, cut, breaks=(105, 196), nsim=NS)[0]
    fam["weibull per arm"] = A.conditional_power(P, cut, kind="weibull", nsim=NS)[0]
    fam["no withdrawal (SF9)"] = A.conditional_power(P, cut, drop=False, nsim=NS)[0]
    fam["unstratified final test (SF6)"] = A.conditional_power(P, cut, stratified=False, nsim=NS)[0]
    fam["eCRF strata (SF5)"] = A.conditional_power(P, cut, strata="ecrf", nsim=NS)[0]
    fam["UTC randomisation dates (SF4)"] = A.conditional_power(P, cut, local=False, nsim=NS)[0]
    fam["another seed, 2,000 runs (SF13)"] = A.conditional_power(P, cut, nsim=2000, seed=7)[0]
    for k, v in fam.items():
        check("standing family keeps the bin: %s (SF8)" % k if k.startswith(("break", "per", "two", "weibull")) else
              "standing family keeps the bin: %s" % k, v >= 0.95, "%.4f" % v)
    # SF2 and SF3: censoring rules and data after the cut
    I2 = A.interim(P, cut, gap_rule=False)
    cp2, _ = A.conditional_power(P, cut, gap_rule=False, nsim=NS)
    check("SF2 without the NE-gap censoring rule: same bands for the PH reading and the golden",
          A.band(I2["cp_trend"]) == "stop" and cp2 >= 0.95, "%d events, PH %.4f, golden %.4f" % (I2["events"], I2["cp_trend"], cp2))
    late = [b for b in P.bicr if A.pdate(b["SCANDT"]) > cut]
    I3 = A.interim(P, cut + dt.timedelta(days=14))
    check("SF3 reads after the cut exist and do not change the band", len(late) > 0 and A.band(
        S.cp_bvalue(I3["z"], 0.5, I3["z"] / math.sqrt(0.5))) == "stop", "%d reads after the cut" % len(late))
    # SF1: the investigator's reads count other events
    inv_pd = sum(1 for r in R.inv if r["response"] == "PD" and r["assessment_date"] <= cut)
    bicr_pd = sum(1 for r in R.bicr if r["response"] == "PD" and r["scan_date"] <= cut)
    check("SF1 BICR and investigator progressions differ (the charter counts BICR)", inv_pd != bicr_pd, "%d against %d" % (inv_pd, bicr_pd))
    check("SF11 the golden is far from the 80 per cent edge", golden - 0.80 > 0.15)

    # the analyst test on the clean truth: the easy route (stratified Cox carried forward) files band A
    rows = [(p["rday"], truth[p["rand_no"]][0], truth[p["rand_no"]][1], p["arm"], p["ds"] * 3 + p["ps"]) for p in w.pts]
    a = np.array(rows, dtype=float)
    z0, _, _ = S.logrank(a[:, 1], a[:, 2].astype(bool), a[:, 3].astype(int), a[:, 4].astype(int))
    check("analyst test on the clean truth: the easy route files band A", S.cp_bvalue(z0, 0.5, z0 / math.sqrt(0.5)) < 0.20,
          "z %.3f" % z0)

    # ask A against the world's truth
    sae = A.ask_sae(P, cut)
    t_sae = {(a_, k): 0 for a_ in (0, 1) for k in ("patients", "events") + A.SOCS}
    pts = {0: set(), 1: set()}
    for e in R.events:
        p = e["pt"]
        if e.get("null") or e["onset"] > cut or e["onset"] < p["rand_date"] or not e.get("pv_dates"):
            continue
        t_sae[(p["arm"], "events")] += 1
        pts[p["arm"]].add(p["rand_no"])
        if e["final"][1] in A.SOCS:
            t_sae[(p["arm"], e["final"][1])] += 1
    for a_ in (0, 1):
        t_sae[(a_, "patients")] = len(pts[a_])
    check("ask A equals the world's serious adverse events (SF14 SF15 SF16 SF17)", sae == t_sae,
          str({k: (sae[k], t_sae[k]) for k in sae if sae[k] != t_sae[k]}))
    links = A.screening_links(P)
    firstno = {p["first_screening_no"]: p["rand_no"] for p in R.rescreened}
    check("SF18 every re-screen link is the world's and unique", links == firstno, "%d links" % len(links))
    crack = A.ask_sae(P, cut, rescreen=False)
    check("ask A: the re-screen chain moves every figure", all(crack[k] != sae[k] for k in sae),
          str([k for k in sae if crack[k] == sae[k]]))

    # ask B against the world's truth
    liv = A.ask_liver(P, cut)
    t_liv = {(a_, t): set() for a_ in (0, 1) for t in ("ALT", "AST", "TBIL")}
    first = {p["rand_no"]: min([d for d, *_ in p["doses"]]) for p in w.pts if p["doses"]}
    coll = {s["accession_no"]: s["collected"] for s in R.sample_log}
    sno = {p["screening_no"]: p for p in w.pts}
    for x in R.central:
        if x["test_code"] not in ("ALT", "AST", "TBIL"):
            continue
        p = sno[x["screening_no"]]
        d = coll[x["accession_no"]]
        if p["rand_no"] not in first or d <= first[p["rand_no"]] or d > cut:
            continue
        if x["result"] > (3.0 if x["test_code"] == "TBIL" else 5.0) * x["ref_high"]:
            t_liv[(p["arm"], x["test_code"])].add(p["rand_no"])
    nm = {"Alanine aminotransferase": "ALT", "Aspartate aminotransferase": "AST", "Bilirubin, total": "TBIL"}
    byrand = {p["rand_no"]: p for p in w.pts}
    for x in R.local:
        p = byrand[x["rand_no"]]
        if p["rand_no"] not in first or x["collected"] <= first[p["rand_no"]] or x["collected"] > cut:
            continue
        t = nm[x["test_name"]]
        if x["result"] > (3.0 if t == "TBIL" else 5.0) * x["uln"]:
            t_liv[(p["arm"], t)].add(p["rand_no"])
    t_liv = {k: len(v) for k, v in t_liv.items()}
    check("ask B equals the world's liver counts (SF19 SF20 SF21)", liv == t_liv, str({k: (liv[k], t_liv[k]) for k in liv}))
    crackb = A.ask_liver(P, cut, collection=False)
    check("ask B: the Melbourne receipt date moves every figure", all(crackb[k] != liv[k] for k in liv),
          str([k for k in liv if crackb[k] == liv[k]]))
    melb = [x for x in R.central if x["lab"].endswith("Melbourne")]
    check("SF22 the Melbourne transfer's date follows collection, Edinburgh's equals it",
          all(x["date"] > coll[x["accession_no"]] for x in melb) and
          all(x["date"] == coll[x["accession_no"]] for x in R.central if x["lab"].endswith("Edinburgh")), "%d Melbourne rows" % len(melb))

    # ask C against the world's truth
    ex = A.ask_exposure(P, cut)
    t_ex = {}
    for a_ in (0, 1):
        t_ex[(a_, "safety_population")] = sum(1 for p in w.pts if p["arm"] == a_ and p["doses"])
        t_ex[(a_, "doses")] = sum(1 for p in w.pts if p["arm"] == a_ for d, v, c, dd in p["doses"] if dd == "D1")
    check("ask C equals the world's exposure (SF23 SF24)", ex == t_ex, str({k: (ex[k], t_ex[k]) for k in ex}))
    crackc = A.ask_exposure(P, cut, irt=False)
    check("ask C: the EDC backlog moves every figure", all(crackc[k] != ex[k] for k in ex), str(crackc))
    edc_doses = {(x["rand_no"], x["admin_date"]) for x in R.dose_edc if x["drug"] == "Ravolimab/placebo"}
    irt_doses = {(x["rand_no"], x["dispensed"]) for x in R.dose_irt if x["status"] == "Administered"}
    check("SF23 every EDC dose has its IRT administration", edc_doses <= irt_doses)

    # separation: no device row in the call's population; distractors decide nothing
    check("separation: the call's files carry no device (BICR, IRT randomisation, status are untouched)",
          all(r["rand_no"] in byrand for r in R.bicr))
    gsrc = open(os.path.join(HERE, "golden.py")).read() + open(os.path.join(HERE, "analysis.py")).read()
    check("distractors unread by the golden", "talon2_investigator_tumour_assessments" not in gsrc and
          "talon2_edc_adverse_events" not in gsrc)

    # leak sweep on the filed documents and every text file
    banned = re.compile(r"proportional|delayed|time-varying|change ?point|piecewise|crossing|non-PH|onset of effect|"
                        r"week-12|after week|lag in effect|separat", re.I)
    from pypdf import PdfReader
    hits = []
    for fn in os.listdir(TARGET):
        if fn.endswith(".pdf"):
            txt = " ".join(pg.extract_text() for pg in PdfReader(os.path.join(TARGET, fn)).pages)
            if banned.search(txt):
                hits.append((fn, banned.search(txt).group(0)))
    check("no filed sentence names the stump's dimension", not hits, str(hits))
    late_dates = []
    for fn in os.listdir(TARGET):
        if fn.endswith((".csv", ".json")):
            for m in re.finditer(r"\b(20\d\d)-(\d\d)-(\d\d)\b", open(os.path.join(TARGET, fn)).read()):
                d = dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
                if d > w.snapshot:
                    late_dates.append((fn, d))
    check("no date after the snapshot in any export", not late_dates, str(late_dates[:3]))
    big = max(sum(1 for _ in open(os.path.join(TARGET, f))) - 1 for f in os.listdir(TARGET) if f.endswith(".csv"))
    check("one file of 25,000 rows or more", big >= 25000, str(big))
    check("ten files or more in three formats or more", len(os.listdir(TARGET)) >= 10 and
          len({f.rsplit(".", 1)[1] for f in os.listdir(TARGET)}) >= 3, str(len(os.listdir(TARGET))))
    fails = [r for r in results if not r[1]]
    print("%d checks, %d FAIL" % (len(results), len(fails)))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
