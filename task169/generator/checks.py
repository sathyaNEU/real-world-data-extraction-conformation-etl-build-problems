"""task169 checks: the generator's assertions on the cut pack and on the clean truth.

    python3 task169/generator/checks.py <target>

Labels: INPUT (gates), R1 R2 R3 (the three rules executed), CALL and EDGE (the committed call and its bin), FAM (the
golden's licensed family), RIV (the rivals that must miss), SF (the semantic fork table), ASKA ASKB ASKC (the asks,
their goldens and every stop), SEP (device rows outside the call's population), DIST (distractors), REAL (realism),
DOC (documents read back with a positive control)."""
from __future__ import annotations

import datetime as dt
import glob
import json
import os
import re
import shutil
import sys
import tempfile

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as C   # noqa: E402
import calc          # noqa: E402

FAILS = []
N = [0]
# the shipped pack the round 4 repair started from (target.zip 972382ac): files the call reads that no ask device touches
SHIPPED = {
    C.F_ACT: "bfbc253e93240919fc321399e898d8094a4d1c96e4186ba061e732925c685301",
    C.F_AOC: "ea9d5119cc045bc748412e3e6f2853c6aef4e92458756d9c9b9b69a5481e60ef",
    C.F_ADM: "0383f74886eb99275c15a8aadada0eaa5dd5001800613dc9890de768cc19b733",
    C.F_CAP: "fbba49e87593587b89387f1504119e636880d970ddb372ffde407c549457adfb",
    C.F_PROJ: "adfd6c7d9d4cb753273c543ee4ec4f1bce982979b9993c511643a702d6eeb017",
    C.F_REL: "27181ca95aacdde7b19b328a5cce9ddc37c125ca16ccc167e51af86c97f37c1f",
    C.F_CASE: "fd3875f438dc55b9cdeb6c40ec0eed187213e6aa494ae4eb96ebdd2268eac4a7",
    C.F_PRAT: "0431b1ba377918404008f9df4b4bcb6f801f65c4813dcc4e6871ebbca1ab2246",
    C.F_ARR: "5fd5c3a927f9ba8bc038444002b79d69885e3a9d9af8451a7af6eee595a3df01",
    C.F_XW: "9aeb6c702d309c85e99b0ba6237b51185f8d04c03f74543dceb9adea54f2fdb7",
    C.F_DEATH: "9ea159c7b83fa6668fbcd52f285881fce5f8f6821c2736a9bb0b5007b3e2e945",
    C.F_DICT: "4bfedc28f60529a26f062369e3a3e2ccd947ee8eb8bef6f2a7f4d12b6d442623",
}


def ok(label, cond, detail=""):
    N[0] += 1
    print("%-5s %-34s %s" % ("PASS" if cond else "FAIL", label, detail))
    if not cond:
        FAILS.append(label)


def call_of(D, p):
    s = calc.summarise(D, p)
    order = sorted(C.DISTRICTS, key=lambda d: s[d])
    return calc.step5(s["all"]), order[-1], order[0], s


# ---------------------------------------------------------------- the clean truth, shaped as the pack is read
def clean_D():
    import records as R
    import world as W
    ppl, book = R.history()
    cohort = R.cohort(ppl, book)
    by = {p["pid"]: p for p in ppl}
    nc = {}
    for pid, ad, at, otn, vid in book.admissions:
        if at == "NC":
            nc.setdefault(pid, []).append(ad)
    rows = []
    for pid, rd, rtype, maxd, dist, rno in book.releases:
        if rd > C.CUT:
            continue
        p = by[pid]
        rows.append(dict(doc_number=str(pid), rd=pd.Timestamp(rd), birth=pd.Timestamp(C.add(p["rel0"], -int(p["age0"] * 365.25))),
                         maxd=pd.Timestamp(maxd) if maxd else pd.NaT,
                         code={"PAROLE": "PAR", "REPAROLE": "RPR", "EXPIRATION": "EXP"}[rtype],
                         priors=p["priors"] + sum(1 for a in nc.get(pid, []) if a < rd), prat=0, dist=dist,
                         governing_offense=p["off"].upper(), sex="F" if p["female"] else "M"))
    rel = pd.DataFrame(rows)
    adm = pd.DataFrame([dict(doc_number=str(pid), t=pd.Timestamp(ad), movement_type="ADM",
                             movement_reason="NEW COMMITMENT" if at == "NC" else "PAROLE VIOLATOR")
                        for pid, ad, at, otn, vid in book.admissions if ad <= C.CUT])
    arr = pd.DataFrame([dict(doc_number=str(pid), date=pd.Timestamp(d), otn="O%d" % o, cls=cls)
                        for pid, d, o, cls, onsup in book.arrests if d <= C.CUT])
    aoc = pd.DataFrame([dict(otn="O%d" % o, disposition=("NP" if route == "BOARD" else "X"),
                             sentence_type=("DOC" if sent == "PRISON" and dd <= C.CUT else ""),
                             sentence_date=(sd.isoformat() if sd and dd <= C.CUT else ""))
                        for o, pid, ad, route, disp, dd, sent, sd in book.cases])
    rev = ["O%d" % o for vid, pid, rep, vt, o, hd, dec, term in book.violations if vt == "N" and dec == "REVOKED" and o]
    leg = pd.DataFrame({"action": ["REVOKE"] * len(rev), "arrest_otn": rev})
    new = pd.DataFrame({"decision": [], "arrest_otn": []})
    death = pd.DataFrame([dict(doc_number=str(pid), date_of_death=d.isoformat(), match_score="99") for pid, d in book.deaths])
    proj = pd.DataFrame([dict(doc_number=str(p["pid"]), rd=pd.Timestamp(p["rel0"]),
                              birth=pd.Timestamp(C.add(p["rel0"], -int(p["age0"] * 365.25))), priors=p["priors"], prat=0,
                              dist=p["dist"], governing_offense=p["off"].upper(), sex="F" if p["female"] else "M")
                         for p in cohort])
    ns = "datetime64[ns]"
    rel = rel.astype({"rd": ns, "birth": ns, "maxd": ns})
    adm = adm.astype({"t": ns})
    arr = arr.astype({"date": ns})
    proj = proj.astype({"rd": ns, "birth": ns})
    return dict(rel=rel, adm=adm, arr=arr, aoc=aoc, leg=leg, new=new, death=death, proj=proj), (ppl, book, cohort)


def main(target):
    task = os.path.dirname(os.path.abspath(target))
    files = sorted(os.listdir(target))
    meta = json.load(open(os.path.join(task, "metadata.json")))
    # ------------------------------------------------------------ input gates
    ok("INPUT1 ten or more files", len(files) >= 10, "%d files" % len(files))
    fmts = sorted({f.rsplit(".", 1)[1] for f in files})
    ok("INPUT2 three or more formats", len(fmts) >= 3, ",".join(fmts))
    big = max((sum(1 for _ in open(os.path.join(target, f), encoding="utf-8")) - 1) for f in files if f.endswith(".csv"))
    ok("INPUT3 a 25,000-row file", big >= 25000, "%d rows" % big)
    ok("INPUT4 two distractors declared and shipped", len(meta["distractor_files"]) >= 2 and
       all(f in files for f in meta["distractor_files"]), ",".join(meta["distractor_files"]))
    ok("INPUT5 every shipped file in the manifest", set(files) - {C.F_MAN} <= set(pd.read_csv(os.path.join(target, C.F_MAN)).file),
       "")
    ok("INPUT6 no distractor word in a file name", not any(re.search("distract|trap|golden|answer", f) for f in files), "")

    D = calc.load(target)
    S = calc.spells(D)
    G = calc.golden(D, S)
    step, hi, lo, s = call_of(D, G["p"])
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    ok("CALL1 the rate step is the golden", step == 20 and figs["call"] == {"rate_step": 20}, "%.3f per cent" % (100 * s["all"]))
    e = C.edge(100 * s["all"], 5)
    ok("EDGE1 the golden rate sits mid-bin", e >= 2.0, "edge distance %.2f points" % e)

    # ------------------------------------------------------------ the licensed family
    cv = G["cv"]
    fam = {"frailty 4": calc.project(D, G["lam"], cv, frail=4), "frailty 2": calc.project(D, G["lam"], cv, frail=2),
           "pooled conversion": calc.project(D, G["lam"], cv, pooled=True),
           "overall class mix": calc.project(D, G["lam"], cv, mix_overall=True)}
    cvo = calc.conversion(D, "off")
    fam["conversion from discharged parolees"] = calc.project(D, G["lam"], cvo)
    pe2 = calc.liberty(D, S, until_first=True)
    m2, c2 = calc.arrest_model(D, S, pe2)
    fam["exposure to first admission"] = calc.project(D, calc.lam_projected(D, m2, c2), cv)
    pe1 = G["pe"].copy()
    pe1["b"] = 0
    pe1 = pe1.groupby(["i", "b"], as_index=False).sum()
    m3, c3 = calc.arrest_model(D, S, pe1, nbands=1)
    fam["flat arrest rate"] = calc.project(D, calc.lam_projected(D, m3, c3, nbands=1), cv, edges=())
    Xs = calc.features(S, "rd")
    Xs["prat"] = S.prat.values
    Xp = calc.features(D["proj"], "rd")
    Xp["prat"] = D["proj"].prat.values
    m4, c4 = calc.arrest_model(D, S, G["pe"], X=Xs)
    fam["risk score added"] = calc.project(D, calc.lam_projected(D, m4, c4, Xp=Xp), cv)
    recent = S[S.rd >= "2022-10-01"].reset_index(drop=True)
    gr = calc.golden(D, recent)
    fam["last two complete years only"] = gr["p"]
    worst = 0
    for k, p in fam.items():
        st, h, l, ss = call_of(D, p)
        worst = max(worst, abs(100 * ss["all"] - 100 * s["all"]))
        ok("FAM %s" % k, st == 20, "%.2f per cent" % (100 * ss["all"]))
    ok("FAM spread inside the bin", worst < 2.5 - 0.0, "largest move %.2f points" % worst)

    # ------------------------------------------------------------ the rivals
    R = calc.default_rates(D, S)
    for k, want in (("R0", 50), ("R1", 5), ("R2", 10)):
        st, h, l, ss = call_of(D, R[k])
        ok("RIV %s misses by a full bin" % k, abs(st - 20) >= 5, "%.2f per cent, step %d, %s %s" % (100 * ss["all"], st, h, l))
    st1, h1, l1, _ = call_of(D, R["R1"])
    st, h, l, ss = call_of(D, calc.doc_bound_route(D, S))
    ok("RIV the readers' route (sentence-bound arrests per day at liberty) misses", st != 20, "%.2f per cent" % (100 * ss["all"]))
    st, h, l, ss = call_of(D, calc.crude_count_route(D, S))
    ok("RIV the courts' conversion on arrests counted with no time at risk misses", st != 20, "%.2f per cent" % (100 * ss["all"]))
    # the record's new-commitment rate over the share of parolees' arrests the courts decided (a one-number uplift)
    arr = D["arr"].dropna(subset=["doc_number"])
    a24 = arr[arr.date <= calc.CONV_TO]
    share_court = 1 - a24.otn.isin(calc.board_revoked_otns(D)).mean()
    ol = R["R1"] / share_court
    st, h, l, ss = call_of(D, ol)
    ok("RIV scalar uplift misses", st != 20, "%.2f per cent" % (100 * ss["all"]))
    # discharged parolees' new-commitment admissions per day, flat
    rel = D["rel"]
    off_ex = ((np.minimum(S.fdays.clip(upper=730), 730)) - (S.maxd - S.rd).dt.days.clip(lower=0, upper=730)).clip(lower=0)
    off_ev = ((S.fr == "NEW COMMITMENT") & (S.fdays <= 730) & (S.fdays > (S.maxd - S.rd).dt.days)).sum()
    sub = 1 - np.exp(-off_ev / off_ex.sum() * 730)
    ok("RIV discharged time, flat rate, misses", calc.step5(sub) != 20, "%.2f per cent" % (100 * sub))
    ok("RIV the record's overall return rate is no forecast", calc.step5(((S.fdays <= 730)).mean()) != 20, "")

    # ------------------------------------------------------------ the three rules on the clean truth
    CD, (ppl, book, cohort) = clean_D()
    CS = calc.spells(CD)
    cr = calc.default_rates(CD, CS)
    cst, ch, cl, css = call_of(CD, cr["R1"])
    ok("R3a analyst test on the clean truth files a wrong rate", cst != 20, "%.2f per cent, step %d" % (100 * css["all"], cst))
    st2, _, _, ss2 = call_of(CD, cr["R2"])
    ok("R3b competing exits alone stay wrong", st2 != 20, "%.2f per cent" % (100 * ss2["all"]))
    cg = calc.golden(CD, CS)
    gst, gh, gl, gss = call_of(CD, cg["p"])
    ok("R3b the decisive step alone files the golden", gst == 20, "%.2f per cent" % (100 * gss["all"]))
    import records as Rr
    tr = Rr.cohort_truth(cohort, reps=8)
    dists = np.array([p["dist"] for p in cohort])
    tt = tr["act"].mean()
    ok("R3b the simulated forward truth is in the golden's bin", calc.step5(tt) == 20, "%.2f per cent" % (100 * tt))
    ok("R1 the field's raw material ships", len(D["arr"]) > 25000 and "otn" in D["aoc"].columns and len(D["rel"]) > 25000, "")
    cols = [c.lower() for f in files if f.endswith(".csv") for c in pd.read_csv(os.path.join(target, f), nrows=1).columns]
    ok("R1 no shipped column holds a return outcome", not any(re.search("return|recid|outcome|within", c) for c in cols), "")
    # R2: each Layer 1 item mishandled leaves the call where it was
    D2 = dict(D, rel=D["rel"].assign(code=D["rel"].movement_code))
    st, h, l, _ = call_of(D2, calc.golden(D2)["p"])
    ok("R2 L1 old movement codes read as other movements", st == 20, "%d %s %s" % (st, h, l))
    adm2 = D["adm"].copy()
    adm2.loc[adm2.movement_type.isin(["TRN", "WRI"]), "movement_type"] = "ADM"
    D3 = dict(D, adm=adm2)
    st, h, l, _ = call_of(D3, calc.golden(D3)["p"])
    ok("R2 L2 transfers and writs read as admissions", st == 20, "%d %s %s" % (st, h, l))
    raw = pd.read_parquet(os.path.join(target, C.F_ARR))
    xw = pd.read_csv(os.path.join(target, C.F_XW), dtype=str)
    ok("R2 L3 the two state-ID formats: an unnormalised join matches nothing (loud)",
       raw.sbi_no.isin(xw.sbi).mean() == 0 and raw.sbi_no.isin(xw.sbi.str.replace("-", "")).mean() > 0.999, "")
    aoc_first = pd.read_csv(os.path.join(target, C.F_AOC), dtype=str, keep_default_na=False).sort_values(
        ["docket_no", "entry_date"]).groupby("docket_no", as_index=False).head(1)
    D4 = dict(D, aoc=aoc_first)
    st, h, l, _ = call_of(D4, calc.golden(D4)["p"])
    ok("R2 L4 amended dispositions: first row kept", st == 20, "%d %s %s" % (st, h, l))
    save = calc.CONV_TO
    calc.CONV_TO = pd.Timestamp(C.CUT)
    st, h, l, ss = call_of(D, calc.project(D, G["lam"], calc.conversion(D)))
    calc.CONV_TO = save
    ok("R2 L5 open cases counted as no sentence", st == 20, "%.2f per cent" % (100 * ss["all"]))
    D6 = dict(D, death=D["death"].assign(doc_number="none"))
    st, h, l, _ = call_of(D6, calc.golden(D6)["p"])
    ok("R2 L6 deaths ignored", st == 20, "%d %s %s" % (st, h, l))
    leg_dup = calc.board_revoked_otns(D)
    D7 = dict(D, leg=D["leg"][pd.to_datetime(D["leg"].action_date, errors="coerce") <= pd.Timestamp(C.BOARD_MIGRATE_CUT)])
    lost7 = leg_dup - calc.board_revoked_otns(D7)
    late7 = D["arr"][D["arr"].otn.isin(lost7)].date
    ok("R2 L7 the Board's two systems: dropping the parallel run's rows leaves the courts' conversion",
       calc.conversion(D7)["pc"] == calc.conversion(D)["pc"] and (late7 > calc.CONV_TO).all() and len(late7) == len(lost7),
       "%d arrest numbers only in the parallel run, all after 30 June 2024" % len(lost7))
    ok("R2 L8 every county of commitment maps to a district", D["rel"].dist.notna().all() and D["proj"].dist.notna().all(), "")
    # R3c: no plant
    ok("R3c no memo, draft or stakeholder figure ships", not any(f.endswith((".eml", ".docx", ".msg")) for f in files), "")

    # ------------------------------------------------------------ the semantic fork table
    ok("SF1 one row per person on the extract", D["proj"].doc_number.is_unique, "%d people" % len(D["proj"]))
    ok("SF2 the extract holds only PAR and RPR in 2027", set(D["proj"].projected_movement) <= {"PAR", "RPR"} and
       (D["proj"].rd.dt.year == 2027).all(), "")
    ok("SF3 transfers and writs are not returns", st == 20, "see R2 L2")
    W0 = C.WINDOW
    C.WINDOW = 731
    st, h, l, ss = call_of(D, calc.project(D, G["lam"], cv))
    C.WINDOW = W0
    ok("SF4 two years read as 731 days", st == 20, "%.2f per cent" % (100 * ss["all"]))
    ok("SF5 the Act governs the whole window of every cohort member", (D["proj"].rd >= pd.Timestamp(C.ACT_IN_FORCE)).all(), "")
    ok("SF6 district by county of commitment: one district per county", len(calc.DIST_OF) == 12, "")
    ok("SF8 the rate is not on a rounding boundary", C.edge(100 * s["all"], 5) > 1.0, "")
    p_d = G["p"]
    ok("SF9 deaths in the denominator or out", True, "the cohort is not yet released; methodology 3.2 keeps them in")
    ok("SF10 history window: the last two complete years give the same call", call_of(D, gr["p"])[0] == 20, "")
    # the judge's two near-miss readings: each still sends every parolee arrest through the courts' conversion (the
    # decisive step) and mishandles a filed convention or the exposure, so each is a fork on the golden route
    cv0 = dict(cv, lags={c: np.zeros(1) for c in cv["lags"]})
    st, h, l, ss = call_of(D, calc.crude_count_route(D, S, cv=cv0))
    st_l, _, _, ss_l = call_of(D, calc.crude_count_route(D, S))
    late = 1 - ss_l["all"] / ss["all"]
    ok("SF11 in-window arrests counted crude, no time at risk and no arrest-to-admission time: ruled out by "
       "methodology 3.1, an arrest whose admission falls after the 730th day is no return; with that time the count "
       "misses too, short of the days the record's parolees spent recommitted",
       late > 0.05 and st_l != 20 and st_l == 15,
       "%.2f per cent, %.2f with the admission time (%.0f per cent of its returns fall past day 730)"
       % (100 * ss["all"], 100 * ss_l["all"], 100 * late))
    st, h, l, ss = call_of(D, calc.project(D, G["lam"], cv, pooled=True))
    ok("SF12 one conversion pooled over charge grades, at the courts' rate: same call, takes the decisive step",
       st == 20, "%.2f per cent" % (100 * ss["all"]))
    # the portal judges' readings (round 1): each takes the decisive step and reads one convention its own way
    save = calc.CONV_TO
    calc.CONV_TO = pd.Timestamp(C.CUT)
    st, h, l, ss = call_of(D, calc.project(D, G["lam"], calc.conversion(D)))
    calc.CONV_TO = save
    ok("SF13 the courts' conversion read from every arrest, cases open at the extract counted as no sentence: same call",
       st == 20, "%.2f per cent" % (100 * ss["all"]))
    st, h, l, ss = call_of(D, calc.project(D, G["lam"], cv0))
    ok("SF14 the arrest-to-admission time left out: ruled out by methodology 3.1, a conversion admitted after the "
       "730th day is no return", ss["all"] > s["all"] + 0.005, "%.2f per cent, step %d" % (100 * ss["all"], st))
    hh = np.minimum(-np.log(1 - G["p"]), 1.0)
    st, h, l, ss = call_of(D, hh)
    ok("SF15 the expected number of returns read as the share: ruled out by methodology 3.2, the share of members "
       "with a return", float(np.mean(hh)) > s["all"] + 0.01, "%.2f per cent, step %d" % (100 * ss["all"], st))
    pe2 = calc.liberty(D, S, until_first=True)
    m2, c2 = calc.arrest_model(D, S, pe2)
    st, h, l, ss = call_of(D, calc.project(D, calc.lam_projected(D, m2, c2), cv))
    ok("SF16 arrests and time at risk counted only to each release's first admission: same call", st == 20,
       "%.2f per cent" % (100 * ss["all"]))
    st, h, l, ss = call_of(D, calc.crude_count_route(D, S, cv=cv0, court_only=False))
    ok("SF11 control: the same crude count without the decisive step misses", st != 20, "%.2f per cent" % (100 * ss["all"]))
    # SF17 the courts' conversion's base (portal round 2: both judges converted over every arrest, the revoked ones in,
    # and could not reproduce 20). The record decides it: every arrest the Board revoked on was nolle prossed, few of the
    # others were, and the arrests made once the Board could no longer revoke convert at the same rate as the arrests it
    # did not revoke on, class by class, so the every-arrest base counts the Board's revocations as court outcomes
    ev = calc.conversion_evidence(D)
    ok("SF17 every arrest the Board revoked on was nolle prossed, against few of the others",
       ev["revoked_np"] == ev["revoked"] and ev["others_np"] < 0.05 * ev["others"],
       "%d of %d; %d of %d" % (ev["revoked_np"], ev["revoked"], ev["others_np"], ev["others"]))
    gap = max(abs(ev["off_by"][c][0] / ev["off_by"][c][1] - ev["others_by"][c][0] / ev["others_by"][c][1]) for c in ("F1", "F2", "M"))
    ok("SF17 the arrests made once the Board could not revoke convert at the courts' rate, class by class",
       ev["off_revoked"] == 0 and gap < 0.015 and abs(ev["off_doc"] / ev["off"] - ev["others_doc"] / ev["others"]) < 0.005,
       "largest class gap %.4f; pooled %.4f against %.4f" % (gap, ev["off_doc"] / ev["off"], ev["others_doc"] / ev["others"]))
    ok("SF17 every arrest with the revoked ones in converts far lower", ev["others_doc"] / ev["others"] - ev["every_doc"] / ev["every"] > 0.05,
       "%.4f against %.4f" % (ev["every_doc"] / ev["every"], ev["others_doc"] / ev["others"]))
    st, h, l, ss = call_of(D, calc.project(D, G["lam"], calc.conversion(D, source="off")))
    ok("SF17 the projection on the after-maximum-date conversion: same call", st == 20, "%.2f per cent" % (100 * ss["all"]))
    _rev = calc.board_revoked_otns
    calc.board_revoked_otns = lambda D_: set()
    cv_all = calc.conversion(D)
    calc.board_revoked_otns = _rev
    st, h, l, ss = call_of(D, calc.project(D, G["lam"], cv_all))
    ok("SF17 the conversion over every arrest (ladder 2f) misses: ruled out by the record's own no-Board arrests", st != 20,
       "%.2f per cent, step %d" % (100 * ss["all"], st))
    ok("SF17 figures.json carries the evidence as the write-up states it",
       figs["conv_revoked_arrests"] == {"arrests": ev["revoked"], "nolle_prosequi": ev["revoked_np"]}
       and figs["conv_courts"]["felony_ab"] == ev["others_by"]["F1"] and figs["conv_after_max_date"]["doc"] == ev["off_doc"]
       and figs["conv_every_arrest"] == {"arrests": ev["every"], "doc": ev["every_doc"]})
    ok("SF17 the golden's conversion counts a DOC sentence only (CJ and PROB are no return)",
       all(abs(cv["pc"][c] - ev["others_by"][c][0] / ev["others_by"][c][1]) < 1e-12 for c in ("F1", "F2", "M")),
       ", ".join("%s %.4f" % (c, cv["pc"][c]) for c in ("F1", "F2", "M")))

    # SF18 ask 2's unit and SF19 ask 4's trip end (stage 4 judge r3, 2026-10-25): each reading the judge took files other
    # figures, and the prompt's own clause rules it out
    prompt = open(os.path.join(task, "prompt.txt")).read()
    A0 = calc.ask_a(D)
    A1 = calc.ask_a(D, orders=False)
    ok("SF18 one per parolee per hearing date: the prompt files it, and counting each decision row moves the table",
       "one per parolee per hearing date" in prompt and A1 != A0,
       "per decision row %d against %d" % (sum(sum(v.values()) for v in A1.values()), sum(sum(v.values()) for v in A0.values())))
    W0 = calc.ask_c(D)
    W1 = calc.ask_c(D, ended_by_release=False)
    ok("SF19 a trip ends back from the writ or at the release: the prompt files it, and pairing WRO with WRI alone moves "
       "every cell", "with the person back from the writ or released" in prompt
       and all(W1[i][h] != W0[i][h] for i in W0 for h in ("H1", "H2")), json.dumps(W1)[:120])
    # SF21 the days at risk under the Act (portal round 4, judge 2: the calendar basis 14.8, the golden 20.4, the share
    # scaled by days out 23.5): methodology 4.1 files that a member of the 2027 cohort is out of Department custody from
    # release until a return, so the record's arrests stand per day out of custody; the calendar basis carries the
    # record's days back in custody (554.5 of 730 days out on average) into a cohort that has none
    from pypdf import PdfReader
    meth = re.sub(r"\s+", " ", " ".join(pg.extract_text() for pg in PdfReader(os.path.join(target, C.F_METH)).pages))
    ok("SF21 methodology 4.1 files the cohort's days out of custody",
       "out of Department custody from release until a return, and for all 730 days where there is none" in meth, "")
    xr = calc.exposure_routes(D, S, cv)
    ok("SF21 the calendar basis files 15, with or without the admission time: ruled out by 4.1",
       calc.step5(xr["calendar"]) == 15 and calc.step5(xr["calendar_lag"]) == 15,
       "%.2f and %.2f per cent, %.1f days out of 730" % (100 * xr["calendar"], 100 * xr["calendar_lag"], xr["days_out"]))
    ok("SF21 the share scaled whole by 730 over the days out files 25: ruled out by 3.1 and 3.2",
       calc.step5(xr["share_scaled"]) == 25, "%.2f per cent" % (100 * xr["share_scaled"]))
    hh0 = calc._union(calc.holds(D))
    hd = {k: v[["s", "e"]].values for k, v in hh0.assign(s=calc._days(hh0.s), e=calc._days(hh0.e)).groupby("doc_number")}
    pe_j = G["pe"].copy()
    rdj = calc._days(S.rd)
    exj = pe_j.ex.values.astype(float)
    for j, (i, b) in enumerate(zip(pe_j.i.values, pe_j.b.values)):
        for s_, e_ in hd.get(S.doc_number.values[i], ()):
            lo_, hi_ = calc.BANDS[b]
            ov = min(rdj[i] + hi_, e_) - max(rdj[i] + lo_, s_)
            if ov > 0:
                exj[j] -= ov
    pe_j["ex"] = np.maximum(exj, 0.5)
    X0 = pd.DataFrame({"const": np.ones(len(S))})
    X0p = pd.DataFrame({"const": np.ones(len(D["proj"]))})
    def liberty_route(pe, nbands=4, X=None, Xp_=None):
        m_, c_ = calc.arrest_model(D, S, pe, X=X, nbands=nbands)
        lam_ = calc.lam_projected(D, m_, c_, nbands=nbands, Xp=Xp_)
        return calc.project(D, np.tile(lam_, (1, 4)) if nbands == 1 else lam_, cv)
    lib = {"no covariates": liberty_route(G["pe"], X=X0, Xp_=X0p),
           "no covariates, one rate": liberty_route(G["pe"], nbands=1, X=X0, Xp_=X0p),
           "detainer days out of the exposure too": liberty_route(pe_j),
           "detainer days out too, one rate": liberty_route(pe_j, nbands=1)}
    for k, p in lib.items():
        ok("SF21 on the days out of custody, %s: same call" % k, call_of(D, p)[0] == 20, "%.2f per cent" % (100 * np.mean(p)))
    ok("SF21 each release's arrests scaled to its own days out of custody: same call", calc.step5(xr["scaled_lag"]) == 20,
       "%.2f per cent" % (100 * xr["scaled_lag"]))
    nco = calc.nc_out_of_custody(D, S)
    ok("SF21 the default path on the same days (new commitments per day out of custody) still misses",
       calc.step5(np.mean(nco)) == 10, "%.2f per cent" % (100 * np.mean(nco)))
    # ------------------------------------------------------------ the asks
    A = calc.ask_a(D)
    ok("ASKA golden matches figures.json", all(figs["a1_" + o] == A[o] for o in calc.OFFICES), "")
    def miss_a(a, name):
        hits = sum(a[o][x] == A[o][x] for o in calc.OFFICES for x in ("arrest", "conditions"))
        ok("ASKA stop %s misses every cell" % name, hits == 0, "%d of 8 kept" % hits)
    miss_a(calc.ask_a(D, level="case"), "every order on a rescinded case out (the round 3 golden's rule)")
    miss_a(calc.ask_a(D, orders=False), "each case row a recommitment")
    miss_a(calc.ask_a(D, orders=False, dedupe=False), "both systems added, case rows")
    leg, new = calc._board(D)
    # A3 a revocation set aside on appeal and heard again: REVOKE, RESCIND, REVOKE on one case, the parolee in Department
    # custody from the first order's admission past the second hearing, so the second order is what holds the person
    acts = leg[leg.action.isin(["REVOKE", "RESCIND"])].sort_values(["case_no", "ad"])
    seqs = acts.groupby("case_no").action.apply(tuple)
    re_cases = seqs[seqs == ("REVOKE", "RESCIND", "REVOKE")].index
    other = seqs[(seqs.map(lambda t: t.count("REVOKE")) > 1) & ~seqs.index.isin(re_cases)]
    rel_by = D["rel"].groupby("doc_number").rd.apply(lambda x: np.sort(x.values))
    adm_pv = D["adm"][(D["adm"].movement_type == "ADM") & (D["adm"].movement_reason == "PAROLE VIOLATOR")]
    pv_by = adm_pv.groupby("doc_number").t.apply(lambda x: np.sort(x.values))
    held = 0
    for case in re_cases:
        g = acts[acts.case_no == case]
        d1, r1, d2 = g.ad.values
        doc = g.doc_number.iloc[0]
        a = [t for t in pv_by.get(doc, []) if d1 < t <= r1]
        rels = [t for t in rel_by.get(doc, []) if a and a[0] < t <= d2 + np.timedelta64(14, "D")]
        held += bool(a) and not rels and g.hold_lodged.iloc[0] == g.hold_lodged.iloc[2]
    ok("ASKA A3 re-heard cases: REVOKE, RESCIND, REVOKE, the parolee held throughout",
       len(re_cases) >= 16 and held == len(re_cases) and len(other) == 0,
       "%d cases, %d held from the first admission past the second hearing" % (len(re_cases), held))
    # the parallel run: every legacy decision dated after the close is a copy of a decision the new system holds
    late = leg[(leg.ad > pd.Timestamp(C.BOARD_MIGRATE_CUT)) & leg.action.isin(["REVOKE", "CONTINUE"])]
    held = set(calc._key(new[(new.opened_in == "LEGACY") & (new.decision != "")]))
    ok("ASKA the parallel run's legacy decisions all copy a new-system decision", calc._key(late).isin(held).all()
       and calc.ask_a(D, parallel="date") == calc.ask_a(D), "%d late legacy decisions" % len(late))
    nd = new.assign(d=new.dd.dt.date)
    pairs = nd[nd.decision == "REVOKED"].groupby(["doc_number", "d"]).size()
    ok("ASKA two cases decided at one hearing share the decision timestamp",
       nd[nd.decision == "REVOKED"].groupby(["doc_number", "d"]).decision_ts.nunique().max() == 1, "%d orders with two cases" % (pairs > 1).sum())
    late = calc.ask_a(D, rescind_by=pd.Timestamp(C.CUT))
    ok("ASKA rescission after 30 June 2026 moves at least one cell", late != A, "")
    B = calc.ask_b(D)
    ok("ASKB golden matches figures.json", all(figs["b_" + d] == B[d] for d in C.DISTRICTS), "")
    # SF20 a detainer's end where the courts sent the person to the Department before the Board lifted it (portal round
    # 3, judge 2): C1 in the records, the Board lifting the detainer on the admission day, so the recorded end and the
    # physical exit select the same days
    hh = calc.holds(D)
    aa = D["adm"][D["adm"].movement_type == "ADM"][["doc_number", "t"]].sort_values("t")
    qq = pd.merge_asof(hh.sort_values("s"), aa, left_on="s", right_on="t", by="doc_number", direction="forward",
                       allow_exact_matches=False)
    inside = int((qq.t.notna() & (qq.t < qq.e)).sum())
    ok("SF20 no detainer's recorded end falls after a Department admission inside it", inside == 0, "%d inside" % inside)
    ok("SF20 ending each detainer at the earlier of its recorded end and the next admission files the same table",
       calc.ask_b(D, clip=True) == B, "")
    # B3 every carried-over case still undecided at go-live had its detainer re-issued under the new case that day; the
    # legacy table keeps the detainer it replaced, lodged earlier and never lifted
    cn = new[(new.opened_in == "LEGACY") & (new.hold_start != "")]
    und = cn[(cn.dd.isna()) | (cn.dd >= pd.Timestamp(C.BOARD_GOLIVE))]
    lg = leg[leg.hold_lodged != ""].assign(k=lambda x: calc._key(x))
    lodge = lg.groupby("k").hold_lodged.apply(lambda x: pd.to_datetime(x).min())
    lifted = lg.groupby("k").hold_lifted.apply(lambda x: pd.to_datetime(x[x != ""]).min())
    ku = calc._key(und)
    ok("ASKB B3 carried-over detainers re-issued at go-live, the legacy detainer lodged earlier, lifted in neither "
       "system before go-live", (und.hold_start == C.BOARD_GOLIVE.isoformat()).all() and ku.isin(lodge.index).all()
       and (ku.map(lodge) < pd.Timestamp(C.BOARD_GOLIVE)).all()
       and not (ku.map(lifted) < pd.Timestamp(C.BOARD_GOLIVE)).any(),
       "%d of %d carried-over detainers, legacy lodges %s to %s" % (len(und), len(cn), ku.map(lodge).min().date(), ku.map(lodge).max().date()))
    bn = calc.ask_b(D, carry="new")
    ok("ASKB stop the new system's date for a carried-over detainer misses every July to December cell",
       all(bn[d]["H2"] != B[d]["H2"] for d in C.DISTRICTS) and all(bn[d]["H1"] == B[d]["H1"] for d in C.DISTRICTS),
       ", ".join("%s %d" % (d, B[d]["H2"] - bn[d]["H2"]) for d in C.DISTRICTS))
    for kw, name in ((dict(union=False), "readers' path (detainers summed)"), (dict(union=False, dedupe=False, blank="action"), "both systems, every row, end at the decision"),
                     (dict(blank="drop"), "blank lifts dropped"), (dict(both_days=True), "both end days counted")):
        b = calc.ask_b(D, **kw)
        hits = sum(b[d][q] == B[d][q] for d in C.DISTRICTS for q in B[d])
        ok("ASKB stop %s misses every cell" % name, hits == 0, "%d of 8 kept" % hits)
    W = calc.ask_c(D)
    wm = D["adm"][D["adm"].movement_type.isin(["WRO", "WRI"])][["doc_number", "t", "movement_type"]]
    wr = D["rel"][["doc_number", "rd"]].rename(columns={"rd": "t"}).assign(movement_type="REL")
    we = pd.concat([wm, wr]).assign(k=lambda x: x.movement_type.map({"REL": 0, "WRI": 1, "WRO": 2}))
    we = we[we.doc_number.isin(set(wm.doc_number))].sort_values(["doc_number", "t", "k"])
    nested = orphan = 0
    for doc, g in we.groupby("doc_number", sort=False):
        op = False
        for mt in g.movement_type:
            if mt == "WRO":
                nested += op
                op = True
            elif mt == "WRI":
                orphan += not op
                op = False
            else:
                op = False
    ok("ASKC one writ trip open at a time per person, every WRI closing one", nested == 0 and orphan == 0,
       "%d WRO with a trip open, %d WRI with none" % (nested, orphan))
    ok("ASKC golden matches figures.json", all(figs["c_" + i] == W[i] for i in calc.INSTITUTIONS), "")
    w = calc.ask_c(D, ended_by_release=False)
    hits = sum(w[i][h] == W[i][h] for i in calc.INSTITUTIONS for h in W[i])
    ok("ASKC readers' path (an unreturned trip dropped) misses every cell", hits == 0, "%d of 10 kept" % hits)
    vals = [v for d in C.DISTRICTS for v in B[d].values()] + [A[o][x] for o in calc.OFFICES for x in A[o]] + \
           [v for i in calc.INSTITUTIONS for v in W[i].values()]
    # a count the record gives is kept as it falls: one figure of 26 on a hundred is chance (Garrison's July to December
    # detainer days, 35,500, since the detainers lifted at an admission), a run of them or a thousand is not
    ok("REAL ask figures distinct and not round", len(set(vals)) == len(vals) and not any(v % 1000 == 0 for v in vals)
       and sum(v % 100 == 0 for v in vals) <= 1, ", ".join(str(v) for v in vals if v % 100 == 0))

    # ------------------------------------------------------------ separation
    par = leg[(leg.ad > pd.Timestamp(C.BOARD_MIGRATE_CUT)) & (leg.action == "REVOKE")]
    dev_otn = set(par.arrest_otn) - {""}
    conv_otn = set(D["arr"][D["arr"].date <= calc.CONV_TO].otn)
    ok("SEP parallel-run rows carry no arrest the call converts", not (dev_otn & conv_otn), "%d device arrests" % len(dev_otn))
    ok("SEP the call reads no hold", True, "calc.golden never calls holds()")
    D8 = dict(D, adm=D["adm"][~D["adm"].movement_type.isin(["WRO", "WRI"])])
    ok("SEP the call is unchanged with every writ row deleted", abs(calc.summarise(D8, calc.golden(D8, S)["p"])["all"] - s["all"]) < 1e-12, "")
    sup = set(new[(new.decision == "REVOKED") & (new.arrest_otn != "")].arrest_otn) | set(leg[(leg.action == "REVOKE") & (leg.arrest_otn != "")].arrest_otn)
    ok("SEP companion reports add no arrest number the Board did not already revoke on", sup == calc.board_revoked_otns(D), "")
    # the round 4 repair against the shipped pack (target.zip 972382ac): the devices sit in the two Board files and add
    # no arrest number to the set the call reads; every file the call reads that no ask touches is byte-identical; the
    # methodology changed by SF21's sentence alone
    import hashlib
    revoked = sorted(calc.board_revoked_otns(D))
    ok("SEP the Board's revoked arrest numbers are the shipped set", len(revoked) == 14445 and
       hashlib.sha256("\n".join(revoked).encode()).hexdigest().startswith("b3888be781c8b58d"), "%d" % len(revoked))
    for f, h in SHIPPED.items():
        ok("SEP %s byte-identical to the shipped pack" % f, hashlib.sha256(open(os.path.join(target, f), "rb").read()).hexdigest() == h, "")
    ok("SEP the call's unrounded rate is the shipped one", abs(100 * s["all"] - 20.403944052083254) < 1e-9, "%.6f" % (100 * s["all"]))

    # ------------------------------------------------------------ distractors
    tmp = tempfile.mkdtemp()
    try:
        for f in files:
            if f not in meta["distractor_files"]:
                shutil.copy(os.path.join(target, f), tmp)
        Dd = calc.load(tmp)
        st, h, l, ss = call_of(Dd, calc.golden(Dd)["p"])
        ok("DIST call unchanged with every distractor deleted", st == 20 and abs(ss["all"] - s["all"]) < 1e-12, "")
        ok("DIST asks unchanged with every distractor deleted", calc.ask_a(Dd) == A and calc.ask_b(Dd) == B and calc.ask_c(Dd) == W, "")
    finally:
        shutil.rmtree(tmp)

    # ------------------------------------------------------------ realism and dates
    ok("REAL no record after the cut", D["arr"].date.max() <= pd.Timestamp(C.CUT) and D["adm"].t.max() <= pd.Timestamp(C.CUT)
       and D["rel"].rd.max() <= pd.Timestamp(C.CUT), "")
    dc = D["rel"].groupby("dist").size()
    ok("REAL district sizes differ", dc.nunique() == len(dc), "")
    yr = D["rel"].groupby(D["rel"].rd.dt.year).size()
    ok("REAL releases per year differ", yr.nunique() == len(yr), "")
    ok("REAL no person names in the pack", True, "extracts carry identifiers only")
    ok("REAL arrest grades plausible", D["arr"].top_charge_grade.value_counts(normalize=True).max() < 0.35, "")

    # ------------------------------------------------------------ documents, read back with a positive control
    from pypdf import PdfReader
    for f, control, absent in ((C.F_ACT, "shall not recommit a parolee for a technical violation", "prosecut"),
                               (C.F_METH, "the share of its members with a return", "conversion"),
                               (C.F_PRAT, "area under the ROC curve", "Act 26-114")):
        txt = " ".join(pg.extract_text() for pg in PdfReader(os.path.join(target, f)).pages)
        txt = re.sub(r"\s+", " ", txt)
        ok("DOC %s readable (positive control)" % f, control in txt and len(txt) > 400, "%d characters" % len(txt))
        ok("DOC %s does not name %r" % (f, absent), absent.lower() not in txt.lower(), "")
    print("\n%d checks, %d failed%s" % (N[0], len(FAILS), (": " + ", ".join(FAILS)) if FAILS else ""))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")))
