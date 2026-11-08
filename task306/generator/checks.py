"""task306's generator checks, run on the cut pack (target/) and the clean truth.

    python3 task306/generator/checks.py
"""
import collections
import datetime as dt
import io
import json
import os
import re
import sys
import zipfile

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")
sys.path.insert(0, HERE)
import analysis as A  # noqa: E402
import pack as PK     # noqa: E402
import world as W     # noqa: E402

RESULTS = []


def check(label, ok, detail=""):
    RESULTS.append((label, bool(ok), detail))


def rounded(M):
    s = M["summary"]
    return tuple([M["order"][0], M["order"][1]] + [int(round(s[c]["harms"])) for c in A.REVIEWS] +
                 [int(round(s[c]["off"] / 10.0)) * 10 for c in A.REVIEWS])


def pdf_text(path):
    from pypdf import PdfReader
    return "\n".join(p.extract_text() or "" for p in PdfReader(path).pages)


def main():
    D = A.load(TARGET)
    T = W.build()
    pid = T.P["pid"].values
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    files = sorted(os.listdir(TARGET))

    # ---------------------------------------------------------------------------------------------------- gates
    check("G1 ten or more input files", len(files) >= 10, "%d files" % len(files))
    exts = {os.path.splitext(f)[1] for f in files}
    check("G2 three or more formats", len(exts) >= 3, ", ".join(sorted(exts)))
    check("G3 a file of 25,000 rows or more", meta["largest_file"]["rows"] >= 25000,
          "%s %d rows" % (meta["largest_file"]["name"], meta["largest_file"]["rows"]))
    check("G4 two distractors named in metadata and shipped",
          len(meta["distractors"]) >= 2 and all(d in files for d in meta["distractors"]), str(meta["distractors"]))
    check("G5 no file describing the data", not any(re.search(r"readme|dictionary|notes|manifest|schema|glossary", f, re.I)
                                                    for f in files))
    bad = []
    for f in files:
        raw = open(os.path.join(TARGET, f), "rb").read()
        if b"ReportLab" in raw or b"reportlab" in raw or b"parquet-cpp" in raw or b"openpyxl" in raw:
            bad.append(f)
    check("G6 no toolchain signature (ReportLab, parquet-cpp, openpyxl) in any input file", not bad, str(bad))
    from pypdf import PdfReader
    meta_ok = []
    for f in [x for x in files if x.endswith(".pdf")] + [os.path.join("..", "golden", "medicines_safety_review_2027.pdf")]:
        info = PdfReader(os.path.join(TARGET, f)).metadata
        meta_ok.append(str(info.get("/Producer", "")).startswith("LibreOffice") and info.get("/Creator") == "Writer"
                       and bool(info.get("/Subject")) and info.get("/Author") == "Marches Primary Care Collaborative")
    check("G7 every PDF exported by LibreOffice Writer with a subject and the federation as author", all(meta_ok))
    dashes = []
    for root in (TARGET, GOLDEN):
        for f in os.listdir(root):
            p = os.path.join(root, f)
            txt = pdf_text(p) if f.endswith(".pdf") else (open(p, encoding="utf-8").read() if f.endswith(".csv") else "")
            if "\u2014" in txt or "\u2013" in txt:
                dashes.append(f)
    sub = open(os.path.join(TASK, "submission.md")).read()
    check("G8 no em or en dash in the pack, the goldens or the write-up", not dashes and "\u2014" not in sub
          and "\u2013" not in sub, str(dashes))

    # ------------------------------------------------------------------------------------------- clean truth
    E = A.eligible(D)
    for cls in A.REVIEWS:
        truth = set(pid[T.C[(T.C.role == "pool") & (T.C.cls == cls)]["p"].values])
        check("T1 %s: the protocol on the pack finds exactly the truth's patients in scope" % cls,
              set(E[cls]["patient_pseudonym"]) == truth, "%d against %d" % (len(E[cls]), len(truth)))
    L = A.resolved_letters(D)
    M = A.main_call(D, E=dict(E), L=L)
    tprov = {}
    for c in T.C.itertuples(index=False):
        if c.cls in A.REVIEWS and c.role in ("pool", "pilot"):
            tprov[(pid[c.p], c.cls)] = c.prov
    for cls in A.REVIEWS:
        pv = M["prov"][cls]
        check("T2 %s: provenance rebuilt from the letters equals the truth for every patient in scope" % cls,
              all(tprov[(p, cls)] == v for p, v in pv.items()), "%d patients" % len(pv))
        s = M["six"][M["six"]["cls"] == cls]
        check("T2 %s: provenance rebuilt for every pilot patient equals the truth" % cls,
              all(tprov[(p, cls)] == v for p, v in zip(s["patient_pseudonym"], s["prov"])), "%d patients" % len(s))
    # SF2: the six-month status is the 183-day rule on the issues
    I = D["issues"].copy()
    I["cls"] = I["medicine"].map(A.class_of)
    I["issue_date"] = pd.to_datetime(I["issue_date"])
    P = D["pilot"]
    rv = P[P["record_type"] == "Review"].set_index(["patient_pseudonym", "review"])["record_date"]
    six = P[P["record_type"] == "Six-month follow-up"]
    by_pc = {k: list(g["issue_date"]) for k, g in I.groupby(["patient_pseudonym", "cls"])}
    agree = 0
    for p, lab, out in zip(six["patient_pseudonym"], six["review"], six["outcome"]):
        r0 = pd.Timestamp(rv[(p, lab)])
        ds = by_pc.get((p, A.LABEL[lab]), [])
        on = any(r0 < d <= r0 + pd.Timedelta(days=183) for d in ds)
        agree += (out == "On medicine") == on
    check("T3 SF2 every six-month row equals the 183-day rule on the issue record", agree == len(six),
          "%d of %d" % (agree, len(six)))
    fi = {}
    for cls in A.REVIEWS:
        fi[cls] = A.first_issue(D, cls)
    Lc = L[L["cls"].notna()]
    gap_init, prac_clean = [], True
    by_letter = {k: list(g["date"]) for k, g in Lc.groupby(["patient_pseudonym", "cls"])}
    for (p, cls), prov in tprov.items():
        f = fi[cls].get(p)
        ds = by_letter.get((p, cls), [])
        before = [(f - d).days for d in ds if d < f]
        if prov == "specialist":
            gap_init.append(any(5 <= x <= 26 for x in before) and not any(26 < x <= 365 for x in before))
        elif any(x <= 365 for x in before):
            prac_clean = False
    check("T4 SF5 every specialist-started course has its letter 5 to 26 days before its first issue and none earlier",
          gap_init and all(gap_init), "%d courses" % len(gap_init))
    check("T4 SF5 no practice-started course has a class letter in the 365 days before its first issue", prac_clean)
    Wf = D["workflow"]
    recv = dict(zip(Wf["sender_reference"], pd.to_datetime(Wf["received"])))
    late = 0
    for x in T.L:
        if x["kind"] == "initiation" and x["ref"] in recv:
            if recv[x["ref"]].normalize() >= pd.Timestamp(W.dd(x["start"])):
                late += 1
    check("T5 SF6 every initiation letter in the workflow log was received before the practice's first issue", late == 0,
          "%d late" % late)

    # --------------------------------------------------------------------------------------------- main call
    F = A.figures_main(M)
    s = M["summary"]
    check("M1 the call is review B, the runner-up review C, review A third",
          (F["call"], F["runner_up"], F["third"]) == ("BZ", "GB", "AP"), str(M["order"]))
    check("M2 SF13 the gap from the rounded figures equals the rounded gap of the unrounded sums",
          F["gap"] == int(round(s["BZ"]["harms"] - s["GB"]["harms"])) == 4, "gap %d" % F["gap"])
    check("M3 the call leads the runner-up by 1.3 times or more", s["BZ"]["harms"] / s["GB"]["harms"] >= 1.3,
          "%.2f" % (s["BZ"]["harms"] / s["GB"]["harms"]))
    check("M3 the runner-up leads the third by 1.2 times or more", s["GB"]["harms"] / s["AP"]["harms"] >= 1.2,
          "%.2f" % (s["GB"]["harms"] / s["AP"]["harms"]))
    for cls in A.REVIEWS:
        h, o = s[cls]["harms"], s[cls]["off"]
        check("M4 %s harms sit 0.25 or more inside their whole number" % cls, abs(h - round(h)) <= 0.25, "%.3f" % h)
        check("M4 %s patients off sit 2.5 or more inside their ten" % cls, abs(o - round(o / 10.0) * 10) <= 2.5,
              "%.2f" % o)
    golden_r = rounded(M)
    variants = {
        "SF5 window 30 days": dict(prov_kw={"window": 30}),
        "SF5 window 90 days": dict(prov_kw={"window": 90}),
        "SF5 window 365 days": dict(prov_kw={"window": 365}),
        "SF5 window 180 days": dict(prov_kw={"window": 180}),
        "SF6 received date where the workflow log has it": dict(prov_kw={"basis": "received"}),
        "SF7 letters carrying only a hospital number dropped": dict(prov_kw={"drop_hn_only": True}),
        "SF8 the specialist-started rate pooled across the reviews": dict(pooled_specialist=True),
        "SF5 Start recommendations only": dict(prov_kw={"start_only": True}),
        "provenance and age band": dict(how="provenance+band"),
        "provenance and sex": dict(how="provenance+sex"),
    }
    for name, kw in variants.items():
        kw = dict(kw)
        lv = None if kw.get("prov_kw", {}).get("drop_hn_only") else L
        Mv = A.main_call(D, E=dict(E), L=lv, **kw)
        check("M5 %s: same call, runner-up and rounded figures" % name, rounded(Mv) == golden_r, str(rounded(Mv)))
    same_edge = True
    for lo in ("2026-06-29", "2026-06-30", "2026-07-02"):
        Ee = A.eligible(D, window_override=(pd.Timestamp(lo), pd.Timestamp("2026-12-31")))
        same_edge &= all(set(Ee[c]["patient_pseudonym"]) == set(E[c]["patient_pseudonym"]) for c in A.REVIEWS)
    check("M6 SF1 the six months' first day read as 29 June, 30 June or 2 July: the same patients in scope", same_edge)
    E2 = A.eligible(D, window_override=(pd.Timestamp("2026-01-01"), pd.Timestamp("2026-12-31")))
    check("M6 SF1 eligibility on calendar 2026 issues: same call", A.main_call(D, E=E2, L=L)["order"][0] == "BZ")
    E3 = A.eligible(D, outside_cv=False)
    check("M7 SF3 every member practice including the Clun Valley network: same call",
          A.main_call(D, E=E3, L=L)["order"][0] == "BZ")
    Mx = A.main_call(D, E=dict(E), L=L)
    for cls in A.REVIEWS:
        e = Mx["res"][cls]
        a = e["age"] + 1
        e["harms"] = e["chance"] * a.map(A.band).map(A.HARM[cls]).fillna(0) / 100.0
    s4, o4 = A.summarise(Mx["res"])
    check("M8 SF4 ages a year on (at review in 2027): same call", o4[0] == "BZ", str(o4))
    C_ = D["courses"].copy()
    C_["cls"] = C_["medicine"].map(A.class_of)
    two = C_[C_["cls"] == "BZ"].groupby("patient_pseudonym").size()
    two = set(two[two > 1].index) & set(E["BZ"]["patient_pseudonym"])
    check("M9 SF9 patients on two class medicines are one patient each and practice-started",
          len(two) > 0 and E["BZ"]["patient_pseudonym"].is_unique and all(M["prov"]["BZ"][p] == "practice" for p in two),
          "%d patients" % len(two))
    both = set(E["BZ"]["patient_pseudonym"]) & set(E["GB"]["patient_pseudonym"])
    ok10 = True
    for drop_from in ("BZ", "GB"):
        E4 = dict(E)
        E4[drop_from] = E4[drop_from][~E4[drop_from]["patient_pseudonym"].isin(both)]
        ok10 &= A.main_call(D, E=E4, L=L)["order"][0] == "BZ"
    check("M10 SF10 patients in scope for two reviews: same call when dropped from either", ok10, "%d patients" % len(both))
    six_r = A.pilot_rates(D, L=L)
    rv_out = P[P["record_type"] == "Review"].set_index(["patient_pseudonym", "review"])["outcome"]
    six_r["off"] = [int(rv_out[(p, lab)] in ("Stopped", "Taper agreed")) for p, lab in
                    zip(six_r["patient_pseudonym"], six_r["review"])]
    res11 = A.carry(D, dict(E), six_r, "provenance", M["prov"])
    s11, o11 = A.summarise(res11)
    check("M11 SF11 the review row read as the outcome: same call", o11[0] == "BZ", str(o11))
    reg = D["reg"]
    net = dict(zip(reg["ods_code"], reg["primary_care_network"]))
    check("M12 SF12 each merged practice sits in its successor's network",
          all(net[r_.ods_code] == net[r_.successor_ods_code] for r_ in reg.itertuples() if isinstance(r_.successor_ods_code, str)))
    first_in_file = I.groupby("course_id")["issue_date"].min()
    cc = D["courses"].set_index("course_id")
    fid = pd.to_datetime(cc["first_issue_date"])
    m = fid[fid >= pd.Timestamp("2025-07-01")]
    check("M13 SF14 the courses extract's first issue equals the issue file's first issue wherever the file covers it",
          bool((first_in_file.reindex(m.index) == m).all()) and I["issue_date"].min() >= pd.Timestamp("2025-07-01"),
          "%d courses" % len(m))
    cls_first = pd.to_datetime(C_.loc[C_["cls"].isin(A.REVIEWS), "first_issue_date"]).min()
    check("M14 SF15 no class course began before the letters feed opened", cls_first >= pd.Timestamp("2019-11-01"),
          str(cls_first.date()))

    # ------------------------------------------------------------------------------------------------ ladder
    rung0 = {c: float((E[c]["band"].map(A.HARM[c]) / 100.0).sum()) for c in A.REVIEWS}
    check("L0 rung 0, eligible patients times the harm rate, files review A", max(rung0, key=rung0.get) == "AP",
          str({k: round(v, 1) for k, v in rung0.items()}))
    R1 = A.main_call(D, how="pooled", E=dict(E), L=L)
    r1s = R1["summary"]
    check("L1 rung 1, the pilot's take-off for every patient, files review A by 1.5 times or more",
          R1["order"][0] == "AP" and r1s["AP"]["harms"] / r1s[R1["order"][1]]["harms"] >= 1.5,
          "%s" % {k: round(v["harms"], 2) for k, v in r1s.items()})
    for k in ("band", "sex"):
        Rk = A.main_call(D, how="pooled+" + k, E=dict(E), L=L)
        check("L2 rung 2, the pilot's take-off re-weighted by %s, files review A" % k, Rk["order"][0] == "AP")
    Ra = A.main_call(D, prov_kw={"any_time": True}, E=dict(E), L=L)
    check("L3 provenance read from any class letter at any time files review A", Ra["order"][0] == "AP", str(Ra["order"]))
    first_med = C_[C_["cls"].isin(A.REVIEWS)].sort_values("first_issue_date").groupby(["patient_pseudonym", "cls"])["medicine"].first()
    six_p = M["six"].copy()
    six_p["product"] = [first_med.get((p, c), "") for p, c in zip(six_p["patient_pseudonym"], six_p["cls"])]
    Ep = {}
    for cls in A.REVIEWS:
        Ep[cls] = E[cls].assign(product=[first_med.get((p, cls), "") for p in E[cls]["patient_pseudonym"]])
    resp = A.carry(D, Ep, six_p, "pooled+product", None)
    sp_, op_ = A.summarise(resp)
    check("L4 the pilot's take-off carried by product files review A", op_[0] == "AP", str(op_))
    naive = {"eligible patients": {c: s[c]["eligible"] for c in A.REVIEWS},
             "pilot take-off": {c: six_r[six_r["cls"] == c]["off"].mean() for c in A.REVIEWS},
             "pilot six-month take-off": {c: M["six"][M["six"]["cls"] == c]["off"].mean() for c in A.REVIEWS},
             "harm per patient-year": {c: float(E[c]["band"].map(A.HARM[c]).mean()) for c in A.REVIEWS},
             "pool harm": rung0,
             "patients off at the pilot rate": {c: r1s[c]["off"] for c in A.REVIEWS},
             "harms at the pilot rate": {c: r1s[c]["harms"] for c in A.REVIEWS}}
    tops = {k: max(v, key=v.get) for k, v in naive.items()}
    check("L5 the golden review tops no naive sort", "BZ" not in tops.values(), str(tops))

    # ---------------------------------------------------------------------------- R1 R2 R3, the three rules
    heads = []
    for f in files:
        p = os.path.join(TARGET, f)
        if f.endswith(".csv"):
            heads += open(p, encoding="utf-8").readline().strip().split(",")
        elif f.endswith(".parquet"):
            heads += list(pd.read_parquet(p).columns)
        elif f.endswith(".xlsx"):
            for sh, df in pd.read_excel(p, sheet_name=None).items():
                heads += list(df.columns)
    check("R1 the field's raw material ships at the patient grain and no column stores who started a medicine",
          not any(re.search(r"provenance|started|initiat|specialist|origin|prescriber", h, re.I) for h in heads),
          "%d columns" % len(heads))
    texts = {f: pdf_text(os.path.join(TARGET, f)) for f in files if f.endswith(".pdf")}
    vocab = re.compile(r"specialist|started by|who started|provenance|initiat|shared care|secondary care|consultant",
                       re.I)
    hits = {f: sorted(set(m_.group(0).lower() for m_ in vocab.finditer(t))) for f, t in texts.items()}
    check("R1 no governing document names specialists, who started a medicine or provenance",
          not any(hits.values()), str(hits))
    flat = {f: re.sub(r"\s+", " ", t) for f, t in texts.items()}
    p43 = re.search(r"4\.3 Each half-year the team also reports the hospital medicine letters received by each "
                    r"network's practices.*?at the practice of its first receipt\.", flat["medicines_safety_programme_2027.pdf"])
    out43 = dict(flat)
    if p43:
        out43["medicines_safety_programme_2027.pdf"] = flat["medicines_safety_programme_2027.pdf"].replace(p43.group(0), "")
    lets = {f: len(re.findall(r"letter", t, re.I)) for f, t in out43.items()}
    check("R1 letters appear in the governing documents only in specification 4.3, the reporting paragraph",
          p43 is not None and len(re.findall(r"letter", p43.group(0), re.I)) == 2 and not any(lets.values()),
          str(lets))
    # the clean truth: eligibility, provenance and pilot outcomes straight from the generator
    tr_rates = {}
    for cls in W.REVIEWS:
        res, _died = T.pilot_res[cls]
        for pv in ("practice", "specialist"):
            g = [x for x in res if x["c"]["prov"] == pv]
            tr_rates[(cls, pv)] = sum(x["status"] == "Off" for x in g) / len(g)
        tr_rates[(cls, "all")] = sum(x["status"] == "Off" for x in res) / len(res)
    by, bm = T.P["birth_year"].values, T.P["birth_month"].values
    tr_g, tr_e = {}, {}
    for cls in W.REVIEWS:
        cs = T.C[(T.C.role == "pool") & (T.C.cls == cls)]
        hg = he = 0.0
        for c in cs.itertuples(index=False):
            h = W.HARM[cls][W.age_band(W.age_on(by[c.p], bm[c.p], W.AS_OF))] / 100.0
            hg += tr_rates[(cls, c.prov)] * h
            he += tr_rates[(cls, "all")] * h
        tr_g[cls], tr_e[cls] = hg, he
    check("R2 the clean truth files the same call as the messy pack (Layer 1 is neutral)",
          max(tr_g, key=tr_g.get) == "BZ" and all(abs(tr_g[c] - s[c]["harms"]) < 1e-9 for c in A.REVIEWS),
          str({k: round(v, 3) for k, v in tr_g.items()}))
    check("R3 analyst test on the clean truth: every field read right, the pilot's take-off carried, files review A",
          max(tr_e, key=tr_e.get) == "AP", str({k: round(v, 2) for k, v in tr_e.items()}))
    cheap = {"rung 0": max(rung0, key=rung0.get), "rung 1": R1["order"][0], "any-time letters": Ra["order"][0],
             "product": op_[0]}
    check("R3 no cheap route lands the call", "BZ" not in cheap.values(), str(cheap))

    # -------------------------------------------------------------------------------------------------- asks
    LA = A.letters_received(D, L=L)
    for n_ in A.NETWORKS:
        for h in ("H1", "H2"):
            check("K1 ask A %s %s equals figures.json" % (n_, h),
                  A.r1(LA[(n_, h)]["rate"]) == fig["letters"][n_][h]["rate"])
    CB = A.consultations(D)
    ok = all(A.r1(CB[k]["rate"]) == fig["consultations"][k[0]][k[1]]["rate"] for k in CB)
    check("K2 ask B: all 20 figures equal figures.json", ok)

    def misses(X, G):
        return sum(A.r1(X[k]["rate"]) != A.r1(G[k]["rate"]) for k in G)
    check("K3 ask A: the letter date misses all 10", misses(A.letters_received(D, basis="letter", L=L), LA) == 10)
    check("K3 ask A: keeping the 7 April re-sends misses every first-half figure",
          misses(A.letters_received(D, dedupe_resend=False, L=L), LA) == 5)
    check("K3 ask A: dropping the whole 7 April batch misses every first-half figure",
          misses(A.letters_received(D, resend_mode="batch", L=L), LA) == 5)
    check("K3 ask A: GP Connect receipts left unmatched (letter date instead) miss every second-half figure",
          misses(A.letters_received(D, gpconnect="letter_date", L=L), LA) == 5)
    check("K3 ask A: GP Connect receipts re-keyed on patient, sender and document date miss every second-half figure",
          misses(A.letters_received(D, gpconnect="exact", L=L), LA) == 5
          and misses(A.letters_received(D, gpconnect="exact_fallback", L=L), LA) == 5)
    check("K4 ask B: the practice systems alone miss all 20", misses(A.consultations(D, use=("activity",)), CB) == 20)
    check("K4 ask B: no matching across the two systems misses all 20", misses(A.consultations(D, dedupe="none"), CB) == 20)
    check("K4 ask B: matching on patient and day misses 18 or more",
          misses(A.consultations(D, dedupe="same_day"), CB) >= 18)
    check("K4 ask B: a group session as one consultation misses 15 or more",
          misses(A.consultations(D, groups="session"), CB) >= 15)
    # the write-up identity is unique: one record per attended hub appointment at a shared-record practice
    pidx = T.pid_index
    hub_att = [h for h in T.hub if h["outcome"] == "Attended"]
    wr = [c for c in T.prac_cons if c["hub_of"]]
    check("K5 one practice-system record per attended hub appointment at a shared-record practice",
          len(wr) == sum(h["code"] in W.SHARED_RECORD for h in hub_att) and len({c["hub_of"] for c in wr}) == len(wr))
    qx = sum((c["t"].month - 1) // 3 != ([h for h in hub_att if h["aid"] == c["hub_of"]][0]["t"].month - 1) // 3
             for c in wr[:400])
    check("K5 no hub record written up in a later quarter (first 400 checked)", qx == 0)
    # separation: the asks' devices touch nothing the call reads
    L_no = L[~((L["sender"].str.startswith("Marches")) & (L["date"] == pd.Timestamp("2026-04-07")))]
    Mn = A.main_call(D, E=dict(E), L=L_no)
    check("K6 dropping the whole 7 April batch leaves every patient's provenance and the call unchanged",
          all(Mn["prov"][c] == M["prov"][c] for c in A.REVIEWS) and rounded(Mn) == golden_r)

    # the asks' forks, closed in the record or by the data (SF16 to SF18)
    spec = " ".join(pdf_text(os.path.join(TARGET, "medicines_safety_programme_2027.pdf")).split())
    check("K7 SF16 the specification counts a letter once, in the half and at the practice of its first receipt",
          "A letter counts once, in the half and at the practice of its first receipt." in spec)
    win18 = {w_: misses(A.letters_received(D, L=L, gp_window=w_), LA) for w_ in (15, 30)}
    check("K7 SF18 GP Connect receipts matched within 15 or 30 days file the same 10 letter figures",
          not any(win18.values()), str(win18))
    saved_h = A.HOLIDAYS
    A.HOLIDAYS = set()
    wk = misses(A.consultations(D), CB)
    A.HOLIDAYS = saved_h
    win17 = {k_: misses(A.consultations(D, window_days=k_), CB) for k_ in (3, 4, 5, 7, 10)}
    check("K7 SF17 weekend-only working days and windows of 3 to 10 days file the same 20 consultation figures",
          wk == 0 and not any(win17.values()), "weekend-only %d, windows %s" % (wk, win17))
    hub_by = {h["aid"]: h for h in hub_att}

    def plain_next(d):
        d = d + dt.timedelta(days=1)
        while d.weekday() >= 5:
            d = d + dt.timedelta(days=1)
        return d
    across = [c["hub_of"] for c in wr if c["t"].date() not in (hub_by[c["hub_of"]]["t"].date(),
                                                              plain_next(hub_by[c["hub_of"]]["t"].date()))]
    check("K7 SF17 every write-up falls on its appointment's day or the next weekday, none across a bank holiday",
          not across, "%d across" % len(across))

    # the clean truth for the asks: each golden count equals the world's own
    reg_net = dict(zip(D["reg"]["ods_code"], D["reg"]["primary_care_network"]))
    first = {}
    for x in T.L:
        z = x.get("recv_doc")
        if z is None:
            continue
        key = x["resend_of"] or x["ref"]
        if key not in first or z["recv"] < first[key][0]:
            first[key] = (z["recv"], z["prac"])
    tl = collections.Counter((reg_net[pr], "H1" if w_.month <= 6 else "H2") for w_, pr in first.values()
                             if w_.year == 2026)
    bad_l = {k: (LA[k]["letters"], tl.get(k, 0)) for k in LA if LA[k]["letters"] != tl.get(k, 0)}
    check("K8 ask A: every golden letter count equals the world's letters at their first receipt", not bad_l,
          str(bad_l))

    def prac_on(p, d):
        x = W.di(d)
        for a, b, c, _ in T.spells_by_p.get(p, []):
            if a <= x and (b == -1 or x < b):
                return W.survivor(c, d)
        return None
    qn = lambda d: "Q%d" % ((d.month - 1) // 3 + 1)
    tc = collections.Counter()
    for h in hub_att:
        tc[(reg_net[h["code"]], qn(h["t"].date()))] += 1
    for c in T.prac_cons:
        if not c["hub_of"]:
            tc[(reg_net[c["code"]], qn(c["t"].date()))] += 1
    for g in T.groups:
        for p, a in g["attendees"]:
            if a == "Yes":
                tc[(reg_net[prac_on(p, g["t"].date())], qn(g["t"].date()))] += 1
    bad_c = {k: (CB[k]["consultations"], tc.get(k, 0)) for k in CB if CB[k]["consultations"] != tc.get(k, 0)}
    check("K8 ask B: every golden consultation count equals the world's consultations", not bad_c, str(bad_c))

    # ------------------------------------------------------------------------------------------------ realism
    lc = collections.Counter(v["letters"] for n_ in fig["letters"].values() for v in n_.values())
    cc_ = collections.Counter(v["consultations"] for n_ in fig["consultations"].values() for v in n_.values())
    check("S1 no repeated count across the networks' halves or quarters", max(lc.values()) == 1 and max(cc_.values()) <= 2,
          "%s %s" % (lc.most_common(1), cc_.most_common(1)))
    ls = D["lists"].groupby("practice_code")["registered_patients"].nunique()
    check("S2 every practice's list size moves month to month", bool((ls > 3).all()))
    check("S3 no headline lands on a whole number", all(abs(s[c]["harms"] - round(s[c]["harms"])) > 1e-6 for c in A.REVIEWS))
    card = json.load(open(os.path.join(TASK, "..", ".claude", "skills", "fingerprint", "cards", "task306.json")))
    people = set(card["world"]["people"])
    named = set()
    for f, t in texts.items():
        for nm in re.findall(r"\b([A-Z][a-z]+ [A-Z][a-zA-Z]+), (?:Clinical|Lead|Medicines)", t):
            named.add(nm)
    check("S4 every person named in the documents is on the card", named and named <= people, str(named))
    wd = pd.to_datetime(Wf["received"])
    check("S5 nothing in the workflow log after the 6 January 2027 extract or before its letter",
          wd.max() <= pd.Timestamp("2027-01-06 23:59:59") and bool((wd.dt.normalize() >= pd.to_datetime(Wf["document_date"])).all()))
    hub_local = A._local(D["hub"]["slot_start_utc"])
    check("S5 hub slots sit in UK working hours", bool(((hub_local.dt.hour >= 8) & (hub_local.dt.hour < 18)).all()))
    check("S5 no prescription issued after 31 December 2026", I["issue_date"].max() <= pd.Timestamp("2026-12-31"))
    top = D["letters"]["medicine_line"].value_counts(normalize=True).iloc[0]
    check("S6 no free-text line recurs beyond a real rate", top < 0.02, "%.4f" % top)
    from scipy.stats import chi2
    pv_min = 1.0
    for cls in A.REVIEWS:
        g = M["six"][M["six"]["cls"] == cls]
        for k in ("practice_code", "band", "sex"):
            if k == "practice_code":
                g = g.assign(practice_code=g["patient_pseudonym"].map(dict(zip(six["patient_pseudonym"], six["practice_code"]))))
            tab = pd.crosstab(g[k], g["off"]).values
            tab = tab[tab.sum(1) > 0]
            exp = tab.sum(1, keepdims=True) * tab.sum(0, keepdims=True) / tab.sum()
            stat = ((tab - exp) ** 2 / exp).sum()
            pv_min = min(pv_min, chi2.sf(stat, (tab.shape[0] - 1) * (tab.shape[1] - 1)))
    check("S7 the pilot's take-off is homogeneous by practice, age band and sex (the close-out's claim)", pv_min > 0.1,
          "smallest p %.3f" % pv_min)
    co = texts["clun_valley_pilot_close_out_2026.pdf"]
    nums = [(int(M["six"][(M["six"]["cls"] == c)]["off"].sum()), int((M["six"]["cls"] == c).sum())) for c in A.REVIEWS]
    check("S8 the close-out's six-month figures match the log",
          all(re.search(r"\b%d\s+%d\s+[\d.]+" % (n, o), co) for o, n in nums), str(nums))
    spec = texts["medicines_safety_programme_2027.pdf"]
    check("S9 the specification's harm table is the analysis's",
          all(("%.1f" % v) in spec for d in A.HARM.values() for v in d.values()) and A.HARM == W.HARM)
    check("X1 Gate G: no shipped file prices any review across the federation",
          not re.search(r"harms? avoided a year|patients taken off", " ".join(texts.values()), re.I))

    width = max(len(r[0]) for r in RESULTS)
    fails = [r for r in RESULTS if not r[1]]
    for label, ok_, detail in RESULTS:
        print("%s  %s  %s" % ("PASS" if ok_ else "FAIL", label.ljust(width), detail))
    print("\n%d checks, %d failed" % (len(RESULTS), len(fails)))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
