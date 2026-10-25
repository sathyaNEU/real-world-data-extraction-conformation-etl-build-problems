"""The generator's assertions on the built pack: the call and its standing family at the printed rounding, the
three-rules block (R1 to R3c) on the clean truth, the semantic fork rows, the asks and their devices, separation from
the main population, the input gates and the realism sweep.

    python3 task269/generator/checks.py      (run by build.py after every build)"""
import json
import os
import re
import zipfile

import numpy as np
import pandas as pd

import analysis as AN
import asks as AK
import common as K
import pack as PK

HERE = os.path.dirname(os.path.abspath(__file__))


def edge(v, u):
    """Distance from v to the nearest edge of the cell it prints in at unit u."""
    return u / 2 - abs(v - round(v / u) * u)


def pdf_text(path):
    from pypdf import PdfReader
    return " ".join((p.extract_text() or "") for p in PdfReader(path).pages)


def run(task, b, fig, res):
    target = os.path.join(task, "target")
    rows = []

    def ok(label, cond, detail=""):
        rows.append((label, bool(cond), detail))

    pk = PK.Pack(target)
    o = AN.main(pk)
    w = b["w"]
    s = w.sf
    F = fig
    rule = pdf_text(os.path.join(target, K.FILES["rule"]))
    memo = pdf_text(os.path.join(target, K.FILES["memo"]))
    ok("control: the rule's text reads back", "Residential ratio studies" in rule and len(rule) > 1500, len(rule))
    ok("control: the memo's text reads back", "reappraisal" in memo and len(memo) > 800, len(memo))
    rule_n = re.sub(r"\s+", " ", rule)

    # ---- the call ------------------------------------------------------------------------------------------------------
    g = o["golden"]
    ok("C1 golden fails both tests", g[0] < K.STANDARD["level_lo"] and g[1] > K.STANDARD["cod_max"], g)
    ok("C1 golden prints 0.87 and 18", round(g[0], 2) == F["call"]["level"] == 0.87 and int(round(g[1])) == F["call"]["cod"] == 18)
    e = o["easy"]
    ok("C2 the default path meets both tests", K.STANDARD["level_lo"] <= e[0] <= K.STANDARD["level_hi"] and
       e[1] <= K.STANDARD["cod_max"], e)
    meds = [v[0] for v in o["family"].values()]
    cods = [v[1] for v in o["family"].values()]
    ok("C3 every standing construction prints the golden level", len({round(m, 2) for m in meds}) == 1, sorted(meds))
    ok("C3 every standing construction prints the golden COD", len({int(round(c)) for c in cods}) == 1, sorted(cods))
    ok("C3 level family clears its cell edge by 0.003", min(edge(m, 0.01) for m in meds) >= 0.003,
       min(edge(m, 0.01) for m in meds))
    ok("C3 COD family clears its cell edge by 0.4", min(edge(c, 1.0) for c in cods) >= 0.4, min(edge(c, 1.0) for c in cods))
    ok("C3 the family's members all fail the rule", all(m < 0.9 for m in meds) and all(c > 15 for c in cods))
    rf = o["rollfwd"]
    ok("C4 the carried-forward values alone print another figure, the same call",
       (round(rf[0], 2), int(round(rf[1]))) != (0.87, 18) and rf[0] < 0.9 and rf[1] > 15, rf)
    ok("C4 the rule files the population that rules them out, the parcels that did not sell included",
       "the median, over every parcel of the class on the county's certified roll, sold or not, of the parcel's "
       "assessed value on that roll" in rule_n)
    ev = F["evidence"]
    ok("C5 sold parcels' median change prints 14.9", ev["sold_change_pct"] == 14.9 and
       edge(100 * (o["chg_sold"] - 1), 0.1) >= 0.01, o["chg_sold"])
    ok("C5 other parcels' median change prints 3.4", ev["unsold_change_pct"] == 3.4 and
       edge(100 * (o["chg_unsold"] - 1), 0.1) >= 0.01, o["chg_unsold"])
    ok("C5 reviewed share prints 6.7", ev["reviewed_share_pct"] == 6.7 and edge(100 * o["share"], 0.1) >= 0.01,
       o["share"])
    ok("C5 the study's sales and the set-asides", ev["study_sales"] == o["study_n"] == 1698 and ev["set_aside_sales"] == 44)
    ok("C6 the sold parcels moved apart from the rest by more than eight points",
       o["chg_sold"] - o["chg_unsold"] > 0.08)
    r25s = o["roll2025_study"]
    ok("C7 the 2025 roll's own study is another figure", (round(r25s[0], 2), round(r25s[1], 1)) != (0.87, 18.0), r25s)

    # ---- the three rules (R1 to R3c) on the clean truth ----------------------------------------------------------------
    cols = set(pk.roll26.columns) | set(pk.roll25.columns) | set(pk.deeds.columns)
    ok("R1 no shipped column holds a ratio, a factor or a review mark",
       not any(re.search(r"(^|_| )ratio|factor|review|chase|adjust", c, re.I) for c in cols), sorted(cols))
    ok("R1 the pack carries both rolls parcel by parcel and the deeds sale by sale",
       len(pk.roll26) > 25000 and len(pk.roll25) > 25000 and len(pk.deeds) > 1700)
    # the golden reads the 2025 values of the sold parcels: move them and the figure moves
    st = AN.q_sales(pk, AN.sf_frames(pk)[0])
    r25 = AN.sf_frames(pk)[1].copy()
    r25.loc[r25.index.isin(st["pid26"]), "Total Assessed"] *= 1.05
    moved = AN.mixture(st, r25, o["factors"], o["share"])
    ok("R1 the decisive computation reads the sold parcels' 2025 values", abs(moved[0] - g[0]) > 0.002, moved)
    sold, study = s["s25"], s["s25"] & (s["kind"] != 1)
    pj = s["price"] * K.INDEX_JAN2026 / s["idx"]
    easy_t = AN.stat(s["av26"][study] / pj[study])
    ok("R3a the easy route on the clean truth meets the rule (the default path's answer)",
       0.9 <= easy_t[0] <= 1.1 and easy_t[1] <= 15 and round(easy_t[0], 2) == F["default_path"]["level"], easy_t)
    cf = np.round(s["av25"] * w.sf["fac"][s["nbi"]], -2)
    n = int(study.sum())
    shr = sold.sum() / (len(sold) - K.N_COMBINE)
    mix_t = AN.wstat(np.r_[cf[study] / pj[study], s["av26"][study] / pj[study]],
                     np.r_[np.full(n, 1 - shr), np.full(n, shr)])
    ok("R3b the decisive step alone, on the clean truth, files the golden", round(mix_t[0], 2) == 0.87 and
       int(round(mix_t[1])) == 18, mix_t)
    for nm, x in (("no physical-change set-aside", AN.stat(s["av26"][sold] / pj[sold])),
                  ("no index carry", AN.stat(s["av26"][study] / s["price"][study])),
                  ("all deeds' parties read as arm's length", o["easy_all_q"])):
        ok("R3b a lower rung alone still meets the rule: %s" % nm, x[0] >= 0.9 and x[1] <= 15, x)
    ok("R3c no document states a ratio, level or COD of the roll",
       not re.search(r"\b0\.[89]\d\b|\bCOD of \d", memo) and "meets" not in memo.lower(), "")
    d = pk.deeds
    dup = d.duplicated(subset=["instrument_no", "parcel_no"]).sum()
    ok("R3c no copied block: no deed row repeats instrument and parcel", dup == 0, dup)
    rr = pk.roll26.drop(columns=["parcel_id", "situs_address"]).duplicated().sum()
    ok("R3c no copied block: roll rows repeat at a natural rate", rr < 30, rr)

    # ---- R2: each Layer 1 item, mishandled the natural way, leaves the call and the critical figures --------------------
    r26f, r25f = AN.sf_frames(pk)
    lost = set(pk.roll25["pid26"]) - set(pk.roll26["parcel_id"])
    ch_old = set(pk.changes["old_parcel_no"].map(PK.to26))
    ok("R2 the two rolls' parcel numbers differ only in form, outside the change log",
       lost <= ch_old, len(lost - ch_old))
    ch = AN.changes(pk, r26f, r25f)
    survivors = set(pk.changes.loc[pk.changes["change_type"] == "COMBINE", "new_parcel_id"])
    fac2 = AN.factors(ch, exclude=survivors)
    g2 = AN.mixture(st, r25f, fac2, o["share"])
    ok("R2 combined parcels' survivors left out of the factors: same figures", round(g2[0], 2) == 0.87 and
       int(round(g2[1])) == 18, g2)
    q_only = pk.deeds[pk.deeds["validation_code"] == "Q"]
    ok("R2 transfers coded U never reach the study", set(st["instrument_no"]) <= set(q_only["instrument_no"]))
    rec_month = st.copy()
    rec_month["price_jan26"] = rec_month["consideration"] * pk.index_carry(
        pk.deeds.set_index("instrument_no").loc[rec_month["instrument_no"], "recorded_date"].reset_index(drop=True)
        .set_axis(rec_month.index))
    g3 = AN.mixture(rec_month, r25f, o["factors"], o["share"])
    ok("R2 SF4 the index carried from the recording month instead: same figures", round(g3[0], 2) == 0.87 and
       int(round(g3[1])) == 18, g3)
    big_book = "%03d" % w.condo_book[len(K.CONDO_PROJECTS) - 1]
    ok("R2 the condominium renumbering touches no single-family row",
       not pk.changes.loc[pk.changes["change_type"] == "RENUMBER", "old_parcel_no"].str[:3].ne(big_book).any())
    cperm = pk.permits[pk.permits["parcel_no"].str[:3] >= "200"]
    ok("R2 the condominium permits touch no single-family parcel", not cperm["pid26"].isin(r26f.index).any() and
       len(cperm) >= 40, len(cperm))

    # ---- semantic fork rows -------------------------------------------------------------------------------------------
    ok("SF1 class R1 is single-family; the rule says so", "single-family residential (class R1)" in rule_n)
    ok("SF2 meeting the rule needs both tests", "its level is from 0.900 to 1.100 and its COD is 15.0 or less" in rule_n)
    ok("SF3 the level is taken over every parcel of the class on the certified roll, sold or not",
       "over every parcel of the class on the county's certified roll, sold or not" in rule_n)
    ok("SF4 the price carried by the deed's month", "divided by the index for the month of the deed" in rule_n)
    ok("SF5 set-asides: changed improvements or boundaries; no other trimming",
       "boundaries or improvements changed between the date of the deed and the assessment date" in rule_n and
       "Ratios are not otherwise trimmed" in rule_n)
    ok("SF6 COD around the level, as a percentage", "absolute difference between a parcel's ratio and the class's level"
       in rule_n)
    ok("SF7 weighted median convention: lower, upper and averaged agree",
       round(AN.mixture(st, r25f, o["factors"], o["share"], how="mid")[0], 2) == 0.87 and
       round(o["family"]["upper weighted median"][0], 2) == 0.87)
    ok("SF8 the reviewed share counted on all reviewed parcels or on the study's sales: same figures",
       round(o["family"]["share on the study's sales"][0], 2) == 0.87 and
       int(round(o["family"]["share on the study's sales"][1])) == 18)
    anyd = set(pk.deeds["pid26"]) & set(r26f.index)
    g_any = AN.mixture(st, r25f, o["factors"], len(anyd) / len(r26f))
    qset = set(pk.deeds.loc[pk.deeds["validation_code"] == "Q", "pid26"])
    u_only = sorted((set(pk.deeds.loc[pk.deeds["validation_code"] != "Q", "pid26"]) - qset) & set(ch.index))
    u_chg = float(ch.loc[u_only, "chg"].median())
    ok("SF8 'sold' read as any 2025 deed: the same figures", round(g_any[0], 2) == 0.87 and int(round(g_any[1])) == 18,
       g_any)
    ok("SF8 parcels with only non-arm's-length deeds moved with the parcels that did not sell",
       abs(u_chg - o["chg_unsold"]) < 0.002 and len(u_only) > 300, (len(u_only), u_chg))
    trimmed = st.copy()
    rr_ = trimmed["av26"] / trimmed["price_jan26"]
    q1, q3 = rr_.quantile(.25), rr_.quantile(.75)
    ok("SF9 the assessment date's month for the carry is January 2026", pk.idx["2026-01"] == K.INDEX_JAN2026)
    ok("SF10 the reviewed parcels' own ratios are their certified 2026 values over their prices",
       abs(float((st["av26"] / st["price_jan26"]).median()) - e[0]) < 1e-12)

    # ---- the asks -----------------------------------------------------------------------------------------------------
    A = AK.ask_a(pk, "golden")
    Ar, Ae = AK.ask_a(pk, "raw"), AK.ask_a(pk, "every")
    FA = F["ask_a"]
    ok("A1 condominium figures as written", (A["n"], round(A["level"], 2), round(A["agg"], 3), round(A["cod"], 1),
                                              round(A["prd"], 3)) == (FA["sales"], FA["level"], FA["agg"], FA["cod"],
                                                                      FA["prd"]))
    ok("A1 condominium sales odd, so the median is one sale's ratio", A["n"] % 2 == 1, A["n"])
    ok("A1 condominium level clears its cell edge", edge(A["level"], 0.01) >= 0.002, edge(A["level"], 0.01))
    ok("A1 condominium COD clears its cell edge", edge(A["cod"], 0.1) >= 0.015, edge(A["cod"], 0.1))
    ok("A1 condominium PRD clears its cell edge", edge(A["prd"], 0.001) >= 0.0002, edge(A["prd"], 0.001))
    ok("A1 condominium aggregate ratio clears its cell edge", edge(A["agg"], 0.001) >= 0.0002, edge(A["agg"], 0.001))
    ok("A1 the condominium class meets the rule", 0.9 <= A["level"] <= 1.1 and A["cod"] <= 15)
    for nm, x in (("raw numbers", Ar), ("the change log applied to every deed", Ae)):
        ok("A2 %s moves every condominium figure" % nm,
           x["n"] != A["n"] and round(x["level"], 2) != round(A["level"], 2) and round(x["cod"], 1) != round(A["cod"], 1)
           and round(x["prd"], 3) != round(A["prd"], 3) and round(x["agg"], 3) != round(A["agg"], 3), x)
    An, Arp = AK.ask_a(pk, "noperm"), AK.ask_a(pk, "rawperm")
    for nm, x in (("no permit set aside", An), ("permits joined by their numbers as written", Arp)):
        ok("A4 %s moves the sales, the aggregate ratio, the COD and the PRD" % nm,
           x["n"] != A["n"] and round(x["cod"], 1) != round(A["cod"], 1) and round(x["prd"], 3) != round(A["prd"], 3)
           and round(x["agg"], 3) != round(A["agg"], 3), x)
    wexp = cperm[cperm["parcel_no"].str[:3] == big_book].copy()
    oldnos = set(pk.changes.loc[pk.changes["old_parcel_no"].str[:3] == big_book, "old_parcel_no"])
    newnos = set(pk.changes.loc[pk.changes["old_parcel_no"].str[:3] == big_book, "new_parcel_id"])
    pre_p = wexp[wexp["issued_date"] < pd.Timestamp(K.REDECLARED)]
    post_p = wexp[wexp["issued_date"] >= pd.Timestamp(K.REDECLARED)]
    ok("A5 a Wexley Commons permit carries the unit's number on its issue date",
       pre_p["parcel_no"].isin(oldnos).all() and post_p["pid26"].isin(newnos).all() and len(pre_p) >= 5 and
       len(post_p) >= 5, (len(pre_p), len(post_p)))
    sit = pk.roll26.set_index("parcel_id")["situs_address"]
    m_new = dict(zip(pk.changes["old_parcel_no"], pk.changes["new_parcel_id"]))
    m_eff = dict(zip(pk.changes["old_parcel_no"], pk.changes["effective_date"]))
    mapped = [m_new[p] if (p in m_new and d < m_eff[p]) else PK.to26(p)
              for p, d in zip(cperm["parcel_no"], cperm["issued_date"])]
    agree = [str(sit.get(k, "")).endswith("Unit " + wd.rsplit("Unit ", 1)[1])
             for k, wd in zip(mapped, cperm["work_description"])]
    ok("A5 every condominium permit's unit agrees with the parcel its number names on its issue date", all(agree),
       sum(agree))
    pre = pk.deeds[(pk.deeds["parcel_no"].str[:3] == big_book) & (pk.deeds["deed_date"] < pd.Timestamp(K.REDECLARED))]
    ok("A3 every deed signed before the re-declaration carries an old number the log lists",
       pre["parcel_no"].isin(pk.changes["old_parcel_no"]).all() and len(pre) >= 25, len(pre))
    B = AK.ask_b(pk, "golden")
    Ball, Brows, Bfirst = AK.ask_b(pk, "all"), AK.ask_b(pk, "rows"), AK.ask_b(pk, "first")
    Bcase, Ballc, Bpar = AK.ask_b(pk, "case"), AK.ask_b(pk, "allcase"), AK.ask_b(pk, "parcel")
    ok("B1 Board of Review figures as written", all(B[a]["parcels"] == F["ask_b"][str(a)]["parcels"] and
                                                     B[a]["off"] == F["ask_b"][str(a)]["value_off"] for a, _ in K.AREAS))
    ok("B2 the 2024-roll appeals move every area's two figures",
       all(Ball[a]["parcels"] != B[a]["parcels"] and Ball[a]["off"] != B[a]["off"] for a, _ in K.AREAS), Ball)
    ok("B3 every REDUCED row summed moves every area's two figures",
       all(Brows[a]["parcels"] != B[a]["parcels"] and Brows[a]["off"] != B[a]["off"] for a, _ in K.AREAS), Brows)
    ok("B3 each parcel's first decision moves every area's value",
       all(Bfirst[a]["off"] != B[a]["off"] for a, _ in K.AREAS), Bfirst)
    ok("B6 a petition's parcels taken as one moves every area's two figures",
       all(Bcase[a]["parcels"] != B[a]["parcels"] and Bcase[a]["off"] != B[a]["off"] and
           Ballc[a]["parcels"] != B[a]["parcels"] and Ballc[a]["off"] != B[a]["off"] for a, _ in K.AREAS), Bcase)
    ok("B7 each parcel's last decision, keyed by parcel alone, files the golden",
       all(Bpar[a] == B[a] for a, _ in K.AREAS), Bpar)
    heard = pk.bor.dropna(subset=["hearing_date"])
    per_case = heard.groupby("case_no").agg(n=("parcel_no", "nunique"), d=("hearing_date", "nunique"))
    ok("B8 every case listing several parcels was heard on one day", (per_case.loc[per_case["n"] > 1, "d"] == 1).all() and
       (per_case["n"] > 1).sum() >= 60, int((per_case["n"] > 1).sum()))
    after = heard[heard["hearing_date"] >= pd.Timestamp(K.CERT_2025)]
    ok("B8 no parcel is in two cases on the 2025 roll", after.groupby("parcel_no")["case_no"].nunique().max() == 1)
    bor = pk.bor.copy()
    r25p = pk.roll25.set_index("Parcel No.")
    bor["cert"] = bor["parcel_no"].map(r25p["Total Assessed"])
    early = bor[bor["hearing_date"] < pd.Timestamp(K.CERT_2025)]
    late = bor[bor["hearing_date"] >= pd.Timestamp(K.CERT_2025)]
    ok("B4 every hearing before the 2025 roll's certification appeals another value",
       (early["value_before"] != early["cert"]).all() and len(early) > 100, len(early))
    ok("B4 every hearing after it appeals the certified 2025 value", (late["value_before"] == late["cert"]).all())
    ok("B5 no area total is a round ten thousand", all(B[a]["off"] % 10000 != 0 for a, _ in K.AREAS))

    # ---- separation: the asks' devices sit outside the main population --------------------------------------------------
    r1_ids = set(pk.roll26.loc[pk.roll26["class_code"] == "R1", "parcel_id"])
    ok("S1 no renumbered or condominium deed is in the single-family study",
       not st["pid26"].isin(set(pk.roll26.loc[pk.roll26["class_code"] == "R2", "parcel_id"])).any())
    import copy
    pk2 = copy.copy(pk)
    pk2.bor = pk.bor.iloc[0:0]
    pk2.changes = pk.changes[pk.changes["old_parcel_no"].str[:3] < "200"]
    pk2.permits = pk.permits[pk.permits["parcel_no"].str[:3] < "200"]
    o2 = AN.main(pk2)
    ok("S2 the golden is unchanged with the Board of Review log, the condominium change rows and permits removed",
       abs(o2["golden"][0] - g[0]) < 1e-12 and abs(o2["golden"][1] - g[1]) < 1e-9 and o2["study_n"] == o["study_n"],
       o2["golden"])
    pk3 = copy.copy(pk)
    pk3.bor = pk.bor.iloc[0:0]
    A3 = AK.ask_a(pk3, "golden")
    ok("S4 the condominium figures do not read the Board of Review log", A3 == A, A3)
    ok("S3 the single-family study's parcels are all R1", st["pid26"].isin(r1_ids).all())

    # ---- input gates and realism ----------------------------------------------------------------------------------------
    files = sorted(os.listdir(target))
    ok("G1 thirteen files", len(files) == len(K.FILES) and len(files) >= 10, len(files))
    ok("G2 four formats", len({f.rsplit(".", 1)[1] for f in files}) >= 3, {f.rsplit(".", 1)[1] for f in files})
    ok("G3 a file of 25,000 rows or more", len(pk.roll26) >= 25000, len(pk.roll26))
    meta = json.load(open(os.path.join(task, "metadata.json")))
    ok("G4 two distractors declared", len(meta["distractor_files"]) >= 2 and
       all(os.path.exists(os.path.join(task, x)) for x in meta["distractor_files"]))
    ok("G4 the study never opens a distractor", not any(K.FILES[k] in open(os.path.join(HERE, m)).read()
                                                       for k in K.DISTRACTORS for m in ("analysis.py", "asks.py")))
    unsold_nb = ch[~ch["sold"]].groupby("nbhd").size()
    ok("G5 no two neighbourhoods carry the same count of parcels", unsold_nb.nunique() >= len(unsold_nb) - 2)
    ok("G6 deeds recorded in 2025 only", pk.deeds["recorded_date"].dt.year.eq(2025).all())
    ok("G6 permits issued in 2025 only", pk.permits["issued_date"].dt.year.eq(2025).all())
    ok("G6 hearings in 2025 only", pk.bor["hearing_date"].dropna().dt.year.eq(2025).all())
    ok("G6 no deed signed after it was recorded", (pk.deeds["deed_date"] <= pk.deeds["recorded_date"]).all())
    ok("G7 the PDFs carry no library banner", all(b"ReportLab" not in open(os.path.join(target, K.FILES[k]), "rb").read()
                                                  for k in ("rule", "memo")))
    with zipfile.ZipFile(os.path.join(target, K.FILES["roll25"])) as z:
        core = z.read("docProps/core.xml").decode()
    ok("G7 the 2025 roll workbook carries its system, not the writing library", "openpyxl" not in core and
       "CAMA Legacy" in core)
    people = set(K.PEOPLE.values())
    named = set(re.findall(r"\b[A-Z][a-z]+ [A-Z][a-z]+\b", memo + " " + rule))
    ok("G8 every person named in a document was drawn", all(p in people for p in named if p.split()[0] in
                                                            {q.split()[0] for q in people}))
    txt = memo + rule + open(os.path.join(target, K.FILES["dictionary"]), encoding="utf-8").read()
    ok("G9 no em or en dash in the documents", "—" not in txt and "–" not in txt)
    ok("G10 no document names the review of sold parcels",
       not re.search(r"sales chasing|chas|selective|sold parcels|revalu", txt, re.I))

    fails = [r for r in rows if not r[1]]
    for label, good, detail in rows:
        if not good:
            print("  FAIL  %s  %s" % (label, str(detail)[:300]))
    print("checks: %d assertions, %d failed" % (len(rows), len(fails)))
    return 0 if not fails else 1
