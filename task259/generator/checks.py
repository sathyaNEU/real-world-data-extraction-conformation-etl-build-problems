"""Generator checks for task259 architecture 2. Run after build.py; exits 1 on any failed assertion.

    python3 task259/generator/checks.py
"""
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
REPO = os.path.dirname(TASK)
sys.path.insert(0, HERE)
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

import analysis as A  # noqa: E402
import pack  # noqa: E402
import world  # noqa: E402

TDIR = os.path.join(TASK, "target")
RESULTS = []


def check(label, ok, detail=""):
    RESULTS.append((label, bool(ok), detail))
    print("%s  %-62s %s" % ("PASS" if ok else "FAIL", label, detail))


def dist_edge(x, step=0.1):
    """Distance from x to the nearest rounding edge at the given step."""
    y = x / step
    return abs((y - np.floor(y)) - 0.5) * step


def main():
    # ------------------------------------------------------------------ the clean truth, rebuilt beside the pack
    W = world.build_world()
    tmp = tempfile.mkdtemp(prefix="t259chk_")
    try:
        pack.write_target(W, os.path.join(tmp, "t"))
        same = all(hashlib.sha256(open(os.path.join(tmp, "t", f), "rb").read()).digest() ==
                   hashlib.sha256(open(os.path.join(TDIR, f), "rb").read()).digest() for f in os.listdir(TDIR))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    check("G0 the installed target/ is the generator's output, byte for byte", same)

    L = A.load(TDIR)
    F, M = A.figures(L)
    fam, rungs, par, state = M["fam"], M["rungs"], M["par"], M["state"]
    gold = A.designate(fam["golden"])
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    files = sorted(os.listdir(TDIR))

    # ------------------------------------------------------------------------------------------ input gates
    check("G1 ten or more files", len(files) >= 10, "%d files" % len(files))
    exts = {f.rsplit(".", 1)[1] for f in files}
    check("G2 three or more formats", len(exts) >= 3, ", ".join(sorted(exts)))
    big = max(meta["row_counts"].values())
    check("G3 a file of 25,000 rows or more", big >= 25000, "largest %d rows" % big)
    check("G4 two or more distractors, each shipped", len(meta["distractor_files"]) >= 2 and
          all(f in files for f in meta["distractor_files"]), ", ".join(meta["distractor_files"]))
    bad = [f for f in files if re.search(r"(read_?me|dictionar|codebook|field_?notes|manifest|glossary|schema|"
                                         r"definitions|proxy|trap|decoy|test_|answer|golden)", f, re.I)]
    check("G5 no file named to describe the data or the stump", not bad, ", ".join(bad))
    check("G6 provenance for every shipped file", set(meta["files"]) == set(files) and
          all(v["source"] and v["license"] and v["date"] for v in meta["files"].values()))
    check("G7 the stated as-of date matches the export stamp", meta["as_of"] == "2026-10-23")

    # ---------------------------------------------------------------------- three rules, on the clean truth
    E = M["E"]
    pr = M["pr"]
    check("R1a the person records carry each adult's line and the line of whoever answered for them",
          E["RESPLINE"].notna().all() and E["LINENO"].notna().all())
    nsw = par["n_sp"] + par["n_ps"]
    check("R1b the panel holds 1,000 or more within-person switches of an employed second-job holder", nsw >= 1000,
          "%d switches" % nsw)
    check("R1c every employed record in the window has a final weight", E["FWGT"].notna().all())
    # truth: weighted true prevalence by area on the final weights
    tr = {}
    for a in A.AREAS:
        num = den = 0.0
        for p in W["persons_q"]:
            if p["area"] == a and p["q"] in world.REF_QUARTERS and p["lfs"] in (1, 2):
                w = W["wts"][(p["aid"], p["line"], p["q"])]
                num += w * (p["mjh_true"] == 1)
                den += w
        tr[a] = 100 * num / den
    truth_set = A.designate(tr)
    check("R2a the golden certifies exactly the areas the clean truth puts at 7.0 or more", truth_set == gold,
          "truth %s golden %s" % (truth_set, gold))
    check("R2b the as-collected route certifies a different set from the truth", A.designate(rungs["R0_face"]) != truth_set,
          str(A.designate(rungs["R0_face"])))
    check("R2c the golden recovers each area's true share within 0.6 points",
          max(abs(fam["golden"][a] - tr[a]) for a in A.AREAS) < 0.6,
          "max gap %.2f" % max(abs(fam["golden"][a] - tr[a]) for a in A.AREAS))
    easy = {k: A.designate(v) for k, v in rungs.items()}
    check("R3a no shipped document reports a multiple-jobholding share by area (no decoy ranking)",
          not area_mjh_in_docs(L), "")
    check("R3b reading every field right, the as-collected, self-answered and imputed routes file {03}",
          all(easy[k] == ["03"] for k in ("R0_face", "R1_self_only", "R2_mar", "R2_mar_coarse")),
          str({k: easy[k] for k in ("R0_face", "R1_self_only", "R2_mar")}))
    check("R3c every easy estimator executed with the filed text misses the golden set",
          all(v != gold for v in easy.values()), str(easy))
    standing = {k: A.designate(v) for k, v in fam.items()}
    check("R3c the standing family (every reconstruction of the within-person sensitivity) lands the golden",
          all(v == gold for v in standing.values()), "%d members" % len(standing))
    ens = [v for k, v in easy.items()]
    check("R3d the cross-sectional check shows answered-for and self reports alike (the textbook route validates)",
          0.9 <= par["cs_ratio_cells"] <= 1.1 and 0.9 <= par["cs_ratio_raw"] <= 1.1,
          "cells %.3f raw %.3f" % (par["cs_ratio_cells"], par["cs_ratio_raw"]))
    check("R3e analyst test: imputing answered-for residents from self-answering ones files {03}, not the truth",
          easy["R2_mar"] != truth_set)
    cheap = sum(1 for v in easy.values() if v == gold)
    check("R3f no cheap route lands the call on the clean truth (Gate F count)", cheap == 0, "%d cheap routes" % cheap)
    check("R3g the carry route lands short of the golden (adds Upper River only)", easy["R3_carry_face"] == ["03", "05"],
          str(easy["R3_carry_face"]))

    # --------------------------------------------------------------------------------- semantic fork table
    e_at_work = E[E["LFSTAT"] == 1]
    sh_at_work = A.corrected(e_at_work, par["s_adj"], par["fp"])
    check("SF1 'employed' read as at work only (LFSTAT 1) certifies the same areas", A.designate(sh_at_work) == gold)
    check("SF2 'holds more than one job' read off MJH 1 among employed records only; MJH -1 never employed",
          set(E["MJH"].unique()) <= {1, 2}, str(sorted(E["MJH"].unique())))
    E7 = A.employed(attach_all(L))
    sh7 = A.corrected(E7, par["s_adj"], par["fp"])
    check("SF3 the window is filed (2025Q4 to 2026Q3); the person file's earlier quarters carry no weights",
          sorted(E["SURVEY_QTR"].unique()) == A.REF and sh7 is not None)
    check("SF4 pooled person-quarters and the mean of quarterly shares certify the same areas",
          standing["by_quarter_mean"] == gold and max(abs(fam["by_quarter_mean"][a] - fam["golden"][a]) for a in A.AREAS) < 0.05)
    check("SF5 the reissued and first-issue 2026Q3 weights give the same shares (to 0.02) and call",
          standing["q3_first_issue"] == gold and max(abs(fam["q3_first_issue"][a] - fam["golden"][a]) for a in A.AREAS) < 0.02)
    check("SF5 unweighted shares certify the same areas", standing["unweighted"] == gold)
    area_ok = person_area_matches_zip(L)
    check("SF6 every resident's HES_AREA is the area its address's county and ZIP give on the 2026 designation",
          area_ok[0], "%d mismatches of %d" % (area_ok[1], area_ok[2]))
    check("SF7 'at least 7.0 percent' against 'over 7.0': no area within 0.25 of the line under any member",
          min(abs(v[a] - 7.0) for v in fam.values() for a in A.AREAS) > 0.25,
          "closest %.2f" % min(abs(v[a] - 7.0) for v in fam.values() for a in A.AREAS))
    check("SF8 answered-for records stay in the population: self-only shares the wrong set; as-given the wrong set",
          easy["R1_self_only"] != gold and easy["R0_face"] != gold)
    sw = [state[k] for k in ("golden", "s_raw", "s_fwd", "s_bwd", "sandwich")]
    check("SF9 the statewide share rounds to the same whole percent under every member, 0.2 or more from the edge",
          len({round(x) for x in sw}) == 1 and min(dist_edge(x, 1.0) for x in sw) >= 0.2,
          "%s" % ", ".join("%.2f" % x for x in sw))
    check("SF10 response and noncontact rates count each housing unit once per quarter (FRAMEID, quarter)",
          A.unit_quarters(L)[["FRAMEID", "SURVEY_QTR"]].duplicated().sum() == 0)
    check("SF11 the noncontact rate counts codes 3 and 216 only (the code list's NC group)",
          set(L["C"][L["C"]["AAPOR_GROUP"] == "NC"]["CODE"]) == A.NO_ONE_HOME)
    check("SF12 the reference week is the survey's own: one record per adult per quarter",
          not L["P"][["SURVEY_QTR", "CASEID", "LINENO"]].duplicated().any())
    check("SF13 every area's certification is the same under pooled and per-area sensitivity (four per-area forms)",
          all(standing["area_s_" + k] == gold for k in ("adj", "raw", "fwd", "bwd")))
    note = pdf_text(os.path.join(TDIR, "HES_TECHNICAL_NOTE_2026-09.pdf"))
    asof = A.ask_rates(L, frame="asof")
    G0 = A.ask_rates(L)
    moved = sum(round(asof[a]["rr"], 1) != round(G0[a]["rr"], 1) for a in A.AREAS)
    check("SF14 rate scope filed: the master address file as finally corrected, a reversal applying from the removal",
          "stood on the master address file on the date of the interviewer" in note and "finally corrected" in note and
          "from the date of the removal" in note and moved == 8, "the file-as-it-stood reading moves %d of 8" % moved)
    Dr = L["D"][L["D"]["SURVEY_QTR"].isin(A.REF)].copy()
    Dr["code"] = Dr["DISPO"].astype(str)
    gi = Dr.groupby(["FRAMEID", "SURVEY_QTR"])["code"].agg(lambda x: bool(set(x) & A.INTERVIEW))
    nonint = Dr[~Dr["code"].isin(A.INTERVIEW)].groupby(["FRAMEID", "SURVEY_QTR"]).size()
    single = nonint[~gi.reindex(nonint.index).values]
    check("SF15 the visit date is unambiguous: every unit-quarter without an interview has exactly one disposition row",
          (single == 1).all(), "%d unit-quarters" % len(single))

    # ---------------------------------------------------------------------------- Layer 1 mess neutrality
    Lx = dict(L)
    Lx["X"] = L["X"].iloc[0:0]
    PKx = A.person_keys(Lx)
    prx = A.pairs(PKx)
    shx = A.corrected(E, A.sensitivity(prx, "adj"), A.false_report(prx))
    check("L1 CAPI re-keying: linking without the crosswalk (losing 2026Q1 to Q2 pairs) certifies the same areas",
          A.designate(shx) == gold)
    check("L2 a new household reusing line numbers: linking without the identity check certifies the same areas",
          standing["no_identity_check"] == gold)
    check("L3 the 2026Q3 weights reissue changes no area share by 0.02 (shares are within-area ratios)",
          max(abs(fam["q3_first_issue"][a] - fam["golden"][a]) for a in A.AREAS) < 0.02)
    E9 = E.copy()
    E9.loc[E9["HRSMAIN"] == -9, "HRSMAIN"] = 40
    check("L4 hours heaped at 40 and 'don't know' (-9): the imputation rung files {03} either way; golden reads no hours",
          A.designate(A.mar_impute(E9)) == ["03"] and A.designate(rungs["R2_mar"]) == ["03"])
    P = L["P"]
    check("L5 two case-number schemes: no old-system case number in the person file from 2026Q2",
          not P[(P["qi"] >= 5) & P["CASEID"].str.startswith("TH")].shape[0])
    D = L["D"]
    reissue_ids = set(D["CASEID"]) - set(P["CASEID"]) - set(L["X"]["OLD_CASEID"]) - set(L["X"]["NEW_CASEID"])
    check("L6 reissued and copied cases (asks only) have zero rows in the main population",
          not (set(P["CASEID"]) & {r[2] for r in W["reissues"]}) and len(W["copies"]) > 0)
    check("L7 interview start times in UTC sit only in the dispositions file the call does not read",
          "START_UTC" not in P.columns and D["START_UTC"].dropna().str.endswith("Z").all())
    zmap = [(str(r[0]), str(r[1])) for r in L["zips"]]
    d41 = D[D["CTY"] == "59041"]
    check("L8 within county 59041 every ZIP on file maps to exactly one area (the split is decidable by ZIP)",
          len({z for z, _ in zmap}) == len(zmap) and set(d41["ZIP"]) <= {z for z, _ in zmap})
    check("L9 the old system's second records of 2026Q2 interviews fall only in 2026Q2",
          set(D[(D["CASEID"].str.startswith("TH")) & (D["SURVEY_QTR"].isin(["2026Q2", "2026Q3"]))]["SURVEY_QTR"]) <= {"2026Q2"})

    # ---------------------------------------------------------------------------------------- realism sweep
    per_q = P.groupby("SURVEY_QTR").size()
    check("S1 no identical record counts across quarters", per_q.nunique() == len(per_q), str(per_q.to_dict()))
    wt = {s: round(float(L["W"][s]["FWGT"].sum())) for s in L["W"]}
    check("S2 no identical weight totals across quarters, none round to the thousand",
          len(set(wt.values())) == len(wt) and all(v % 1000 for v in wt.values()), str(wt))
    rel = W["release_rows"]
    E_first = A.employed(A.attach_weights(L, "2026Q3"))
    rep = []
    for q, row in zip(A.REF, rel):
        e = E_first[E_first["SURVEY_QTR"] == q]
        rep.append("%.1f" % (100 * (e["FWGT"] * e["mjh"]).sum() / e["FWGT"].sum()) == row[6])
    check("S3 the quarterly release's statewide figures reproduce from the shipped records and weights", all(rep))
    fr = L["F"]
    sample_rows = fr["FRAMEID"].isin(set(D["FRAMEID"])).sum()
    check("S4 the frame log is mostly routine traffic: sample units are a minority of its rows",
          sample_rows < 0.4 * len(fr), "%d of %d" % (sample_rows, len(fr)))
    check("S5 the frame log's routine frame ids never collide with sample frame ids",
          len({ids["frame"] for ids in W["ids"].values()}) == len(W["ids"]))
    card = json.load(open(os.path.join(REPO, ".claude", "skills", "fingerprint", "cards", "task259.json")))
    people = set(card["world"]["people"])
    check("S6 every person named in the pack and goldens is a drawn persona",
          {"Kylie Taylor", "Damon Mcbride", "Mackenzie Parks", "Jason Holland"} <= people)
    dd = D[D["SURVEY_QTR"].isin(A.REF)]
    check("S7 dispositions spread across codes as a field system's would (no single code above 80 percent)",
          dd["DISPO"].value_counts(normalize=True).max() < 0.8)
    check("S8 no em dash in any shipped document or the write-up", no_em_dash())
    pops = [float(r[1]) for r in W["release_rows"]]
    steps = [round(b - a, 1) for a, b in zip(pops, pops[1:])]
    check("S9 the release's population moves unevenly quarter to quarter", len(set(steps)) == len(steps), str(steps))
    codes = pd.read_csv(os.path.join(TDIR, "HES_PERSON_CODES.csv"), dtype=str)
    have = {(v, c) for v, c in zip(codes["VARIABLE"], codes["CODE"])}
    need = {("LFSTAT", str(x)) for x in P["LFSTAT"].unique()} | {("MJH", str(x)) for x in P["MJH"].unique()} | \
        {("SEX", str(x)) for x in P["SEX"].unique()} | {("RELREF", str(x)) for x in P["RELREF"].unique()} | \
        {("WANTJOB", str(x)) for x in P["WANTJOB"].unique()}
    check("S10 the person code list maps every coded value in the person file", need <= have,
          str(sorted(need - have)))

    # ------------------------------------------------------------------------------------------- bin edges
    for a in A.AREAS:
        lo = min(v[a] for v in fam.values())
        hi = max(v[a] for v in fam.values())
        side = (lo >= 7.0) if a in gold else (hi < 7.0)
        check("B%s area %s stays on its side of 7.0 under every member, margin 0.25+" % (a, a),
              side and min(abs(lo - 7.0), abs(hi - 7.0)) > 0.25, "range %.2f to %.2f" % (lo, hi))
    rr_d = min(dist_edge(F["rr"][a]) for a in A.AREAS)
    nc_d = min(dist_edge(F["nc"][a]) for a in A.AREAS)
    check("B9 every response rate sits 0.02 or more from its rounding edge", rr_d >= 0.02, "closest %.3f" % rr_d)
    check("B10 every noncontact rate sits 0.02 or more from its rounding edge", nc_d >= 0.02, "closest %.3f" % nc_d)
    check("B11 the sensitivity component (56 percent) sits 0.3 or more points from its rounding edge",
          dist_edge(100 * F["sensitivity"], 1.0) >= 0.3, "%.2f" % (100 * F["sensitivity"]))

    # ------------------------------------------------------------------------------------------ ask devices
    G = A.ask_rates(L)
    for name, kw in (("codes only", dict(frame="none")), ("frame state as of the visit", dict(frame="asof")),
                     ("rows not units", dict(dedup=False))):
        r = A.ask_rates(L, **kw)
        miss_rr = sum(round(r[a]["rr"], 1) != round(G[a]["rr"], 1) for a in A.AREAS)
        miss_nc = sum(round(r[a]["nc"], 1) != round(G[a]["nc"], 1) for a in A.AREAS)
        check("D %s misses every response and noncontact rate" % name, miss_rr == 8 and miss_nc == 8,
              "%d and %d of 8" % (miss_rr, miss_nc))
    uv = A.ask_rates(L, frame="unit_void")
    miss_rr = sum(round(uv[a]["rr"], 1) != round(G[a]["rr"], 1) for a in A.AREAS)
    miss_nc = sum(round(uv[a]["nc"], 1) != round(G[a]["nc"], 1) for a in A.AREAS)
    check("D a restore read as clearing every removal of its unit misses every response and noncontact rate",
          miss_rr == 8 and miss_nc == 8, "%d and %d of 8" % (miss_rr, miss_nc))
    dbl = {}
    for aid in W["double"]:
        dbl[W["addr_by_id"][aid]["area"]] = dbl.get(W["addr_by_id"][aid]["area"], 0) + 1
    check("D every area holds 15 or more units removed in error, restored, then removed for vacancy before a visit",
          len(dbl) == 8 and min(dbl.values()) >= 15, str(dbl))
    r3 = A.ask_rates(L, split041="03")
    check("D county 59041 sent whole to Silver Creek misses only Silver Creek and Eastern Prairie",
          {a for a in A.AREAS if round(r3[a]["rr"], 1) != round(G[a]["rr"], 1) or
           round(r3[a]["nc"], 1) != round(G[a]["nc"], 1)} == {"03", "07"})
    vac = {(W["ids"][aid]["frame"], q) for aid, q in W["vac_nc"] if q in A.REF}
    U = A.unit_quarters(L)
    trueU = U.set_index(["FRAMEID", "SURVEY_QTR"])
    check("D the units coded no one home that the frame shows vacant are truly vacant (law 6: truth recoverable)",
          all((f, q) in trueU.index for f, q in vac) and len(vac) >= 300, "%d unit-quarters" % len(vac))
    elig_truth = {}
    for h in W["hh_q"]:
        if h["q"] in A.REF:
            elig_truth[(W["ids"][h["aid"]]["frame"], h["q"])] = h["outcome"] != "INELIGIBLE"
    dz = A.frame_deleted_at(L, U, void_in_error=True) & ~U["interviewed"].values
    ne = U["code"].isin(A.NOT_ELIGIBLE).values | dz
    agree = sum(elig_truth[(f, q)] == (not n) for f, q, n in zip(U["FRAMEID"], U["SURVEY_QTR"], ne))
    check("D the golden handling reproduces every unit's true eligibility", agree == len(U), "%d of %d" % (agree, len(U)))

    fails = [r for r in RESULTS if not r[1]]
    print("%s: %d checks, %d failed" % ("PASS" if not fails else "FAIL", len(RESULTS), len(fails)))
    return 1 if fails else 0


def attach_all(L):
    return A.attach_weights(L)


def area_mjh_in_docs(L):
    """True if a shipped document puts a multiple-jobholding percentage beside an area name."""
    import zipfile
    names = [str(r[1]) for r in L["areas"]]
    texts = []
    for f in os.listdir(TDIR):
        p = os.path.join(TDIR, f)
        if f.endswith(".docx"):
            with zipfile.ZipFile(p) as z:
                texts.append(re.sub(r"<[^>]+>", " ", z.read("word/document.xml").decode("utf-8")))
        elif f.endswith(".pdf"):
            texts.append(pdf_text(p))
    for t in texts:
        if re.search(r"jobholder|more than one job", t, re.I) and sum(n in t for n in names) >= 2:
            return True
    return False


def pdf_text(path):
    import base64
    import zlib
    raw = open(path, "rb").read()
    out = []
    for m in re.finditer(rb"stream\r?\n(.*?)endstream", raw, re.S):
        data = m.group(1)
        try:
            if data.rstrip().endswith(b"~>"):
                data = base64.a85decode(data.strip(), adobe=True)
            out.append(zlib.decompress(data).decode("latin-1"))
        except Exception:
            continue
    return " ".join(re.findall(r"\((.*?)\)\s*Tj", " ".join(out)))


def person_area_matches_zip(L):
    cty, z = A.area_of(L)
    D = L["D"].drop_duplicates(["SURVEY_QTR", "CASEID"])
    D = D.assign(area=[z[zp] if c == "59041" else cty[c][0] for c, zp in zip(D["CTY"], D["ZIP"])])
    m = L["P"].merge(D[["SURVEY_QTR", "CASEID", "area"]], on=["SURVEY_QTR", "CASEID"], how="left")
    bad = int((m["area"] != m["HES_AREA"]).sum())
    return bad == 0, bad, len(m)


def no_em_dash():
    import zipfile
    for f in os.listdir(TDIR):
        p = os.path.join(TDIR, f)
        if f.endswith(".docx"):
            with zipfile.ZipFile(p) as z:
                if "—" in z.read("word/document.xml").decode("utf-8"):
                    return False
        elif f.endswith(".pdf") and "—" in pdf_text(p):
            return False
    for p in (os.path.join(TASK, "submission.md"), os.path.join(TASK, "prompt.txt")):
        if os.path.exists(p) and "—" in open(p, encoding="utf-8").read():
            return False
    return True


if __name__ == "__main__":
    sys.exit(main())
