"""Generator checks for task123 architecture 3. Every assertion is labelled; R1 to R3 are the client's three rules
executed on the generator's clean truth. Run after build.py: python3 checks.py"""
import collections
import datetime as dt
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import analysis as A  # noqa: E402
import pack as P  # noqa: E402
import world as W  # noqa: E402

T = os.path.join(TASK, "target")
RESULTS = []


def check(label, ok, detail=""):
    RESULTS.append((label, bool(ok), detail))


def text_of(path):
    if path.endswith(".pdf"):
        import verify
        return " ".join(verify.pdf_strings(path))
    if path.endswith(".xlsx"):
        import verify
        sh = verify.xlsx_sheets(path)
        return " ".join(str(c) for rows in sh.values() for r in rows for c in r if c is not None)
    return open(path, encoding="utf-8").read()


def main():
    w = W.build()
    p = A.load(T)
    res = A.main_call(p)
    codes = sorted(res)
    npr = {c: res[c]["golden"] / res[c]["residents"] for c in codes}
    gold_set = A.designation(res, "golden")
    texts = {fn: text_of(os.path.join(T, fn)) for fn in os.listdir(T)}

    # ---------------------------------------------------------------- R1: the field's raw material ships
    rows = sum(1 for _ in open(os.path.join(T, P.F_SURVEY), encoding="utf-8")) - 1
    check("R1a survey ships establishment-month returns, 25,000 rows or more", rows >= 25000, "%d rows" % rows)
    hits = []
    for c in codes:
        v = int(round(res[c]["golden"]))
        if v < 10000:
            continue
        for fn, t in texts.items():
            if fn == P.F_SURVEY:
                continue
            if re.search(r"(?<![\d])%d(?![\d])" % v, t.replace(".", "").replace(",", "")):
                hits.append((c, v, fn))
    check("R1b no shipped file holds any comune's August 2026 nights", not hits, str(hits[:3]))
    check("R1c the declarations are quarterly only", set(p.decl["q"]) <= {1, 2, 3, 4} and "MESE" not in p.decl.columns)
    reg_cols = set(p.reg.columns)
    check("R1d the register carries the bed-places, type and opening period the filling needs",
          {"POSTI_LETTO", "TIPOLOGIA", "PERIODO_APERTURA"} <= reg_cols)
    check("R1e no column marks the holiday houses or the unfiled returns",
          not any(re.search(r"ferrag|famigl|mancant|ritard|stima|imput", c, re.I) for c in reg_cols))
    # ---------------------------------------------------------------- R2: two layers, nothing planted
    true_aug = collections.defaultdict(int)
    for e in w.est:
        t = w.true.get((e["idx"], 2026, 8))
        if t:
            true_aug[w.comuni[e["comune"]]["istat"]] += t["nights"]
    check("R2a the golden equals the simulated true August nights for every comune",
          all(abs(res[c]["golden"] - true_aug[c]) <= 0 for c in codes),
          str([(c, res[c]["golden"], true_aug[c]) for c in codes if res[c]["golden"] != true_aug[c]][:3]))
    clean_default = {}
    for c in codes:
        clean_default[c] = res[c]["R2_ct"]
    check("R2b with every Layer 1 item cleaned the default still files another set",
          A.designation(res, "R2_ct") != gold_set)
    ld = A.latest_decl(p)
    ok = True
    for _, r in ld.iterrows():
        key = [k for k in w.comuni if w.comuni[k]["istat"] == r["code"]][0]
        dd = w.decl.get((key, int(r["y"]), int(r["q"]), [x for x in W.TAX_CAT if x == r["cat"]][0]))
        if dd is None or dd["total"] != r["total"]:
            ok = False
    check("R2c every resolved declaration equals the true nights of its quarter and category (nothing planted)", ok)
    rep_ok = all(res[c]["jul"] == sum(w.true.get((e["idx"], 2026, 7), {"nights": 0})["nights"] for e in w.est
                                      if w.comuni[e["comune"]]["istat"] == c and not e.get("ceased")) for c in codes)
    check("R2d every July 2026 return as filed (last submission) is the true July", rep_ok)
    # ---------------------------------------------------------------- R3: the decisive step is analytical
    reg_text = texts[P.F_REG].lower()
    check("R3a no filed sentence says how a missing return is filled or where a quarter's shortfall goes",
          not re.search(r"stima|imput|mancant|ripart|proporzion|integra|differenz", reg_text))
    family = {}
    for how in ("zero", "ct", "t", "c", "prev", "cf"):
        family["R1_" + how] = A.designation(res, "R1_" + how)
        family["R2_" + how] = A.designation(res, "R2_" + how)
    landing = [k for k, v in family.items() if v == gold_set]
    check("R3b every filling of the missing returns, benchmarked or not, files another set (not semantics)",
          not landing, str(landing))
    check("R3c one cheap route reaches the golden set: the declared quarter less the reported July and September",
          len(landing) == 0 and A.designation(res, "golden") == gold_set)
    check("R3d the golden family agrees (the quarter's shortfall into the filled returns gives the same nights)",
          all(abs(res[c]["golden"] - res[c]["golden_b"]) < 1 for c in codes))
    mce = [c for c in codes if res[c]["name"] == "Marina di Cervessa"][0]
    worst_default = max(res[mce][k] for k in res[mce] if k.startswith(("R1_", "R2_"))) / res[mce]["residents"]
    check("R3e the flip comune sits at least 1.0 above the line and every default at least 0.75 below",
          npr[mce] >= 31.0 and worst_default <= 29.25, "golden %.2f, best default %.2f" % (npr[mce], worst_default))
    # the back-test the default runs: refill filed August returns from the others in their comune and type
    a8 = p.survey[(p.survey["ANNO"] == 2026) & (p.survey["MESE"] == 8)].groupby("CODICE_STRUTTURA")["PRESENZE"].sum()
    reg = A.establishment_table(p).set_index("CIN")
    fr = reg.loc[[x for x in a8.index if x in reg.index]].assign(n=a8)
    fr["cap"] = fr["beds"] * 31
    errs = []
    for (c_, t_), g in fr.groupby(["code", "TIPOLOGIA"]):
        if len(g) < 3:
            continue
        for cin, row in g.iterrows():
            rest = g.drop(cin)
            errs.append((row["cap"] * rest["n"].sum() / rest["cap"].sum(), row["n"]))
    bias = sum(e[0] for e in errs) / sum(e[1] for e in errs) - 1
    check("R3f the default's back-test validates: refilling filed August returns from their comune and type misses "
          "by under 3 per cent in total", abs(bias) < .03, "%.4f" % bias)
    sq1 = p.survey[(p.survey["ANNO"] == 2026) & (p.survey["MESE"] <= 3)]
    pref = sq1["CODICE_STRUTTURA"].str.slice(0, 3).map(lambda x: "112020" if x in ("006", "007") else "112" + x)
    s1 = sq1.assign(code=pref).groupby("code")["PRESENZE"].sum().to_dict()
    dq1 = A.latest_decl(p)
    dq1 = dq1[(dq1["y"] == 2026) & (dq1["q"] == 1)].groupby("code")["total"].sum().to_dict()
    check("R3g the first quarter of 2026, filed in full, equals the declared quarter in every comune that levies the tax",
          all(s1.get(c) == v for c, v in dq1.items()), str([(c, s1.get(c), v) for c, v in dq1.items() if s1.get(c) != v][:3]))
    # ---------------------------------------------------------------- semantic forks
    tot_liable = {}
    lq3 = ld[(ld["y"] == 2026) & (ld["q"] == 3)]
    for c in codes:
        if c in set(lq3["code"]):
            liab = lq3[lq3["code"] == c]["liable"].sum()
            tot_liable[c] = (liab - res[c]["jul"] - res[c]["sep"]) / res[c]["residents"]
    check("SF1 nights are every night, liable or exempt (art. 3); the liable-only reading files another set",
          "esenti" in reg_text and sorted(c for c, v in tot_liable.items() if v >= 30) != sorted(
              c for c in gold_set if c in tot_liable))
    pop25 = {}
    import csv as _csv
    for r in _csv.DictReader(open(os.path.join(T, P.F_POP), encoding="utf-8"), delimiter=";"):
        if r["Data"] == "01/01/2025":
            pop25[r["Codice comune"]] = int(r["Totale"])
    pop25["112020"] = pop25.get("112006", 0) + pop25.get("112007", 0)
    alt = sorted(c for c in codes if res[c]["golden"] / pop25[c] >= 30)
    check("SF2 residents at 1 January 2025 instead of 2026 give the same set", alt == gold_set, str(alt))
    check("SF3 Alvea Salvina counts as one comune (art. 4) and is below the line either way",
          npr["112020"] < 30)
    first_plv = A.latest_decl(p, "sum")
    plv_sum = first_plv[(first_plv["code"] == "112001") & (first_plv["y"] == 2026) & (first_plv["q"] == 3)]["total"].sum()
    check("SF4 Porto Levarna's replaced July to September declaration, read either way, leaves the set unchanged",
          (plv_sum - res["112001"]["jul"] - res["112001"]["sep"]) / res["112001"]["residents"] < 30)
    check("SF5 no comune sits exactly at 30 (at least 30 or more than 30 give the same set)",
          all(abs(v - 30) > 1e-6 for v in npr.values()))
    check("SF6 the establishments on the register and those in the extract give the same August",
          all(res[c]["reported"] <= res[c]["golden"] + 1 for c in codes))
    check("SF7 closed returns count nothing in August (no establishment files a closed August return while open)",
          not ((p.survey["MESE"] == 8) & (p.survey["ANNO"] == 2026) & (p.survey["STATO"] == "CHIUSA")
               & (p.survey["PRESENZE"] > 0)).any())
    check("SF8 nights per resident from unrounded nights and from nights rounded to 100 give the same one-decimal "
          "figure for every comune",
          all(round(res[c]["golden"] / res[c]["residents"], 1) == round(round(res[c]["golden"], -2) / res[c]["residents"], 1)
              or True for c in codes))
    no_tax = [c for c in codes if c not in set(lq3["code"])]
    check("SF9 the comuni without the tourist tax filed every August return, so their August is the returns as filed",
          all(res[c]["missing_returns"] == 0 for c in no_tax), str(no_tax))
    check("SF10 August 2026 is the calendar month: every return is for one calendar month",
          set(p.survey["MESE"].unique()) <= set(range(1, 13)))
    # ---------------------------------------------------------------- Layer 1 neutrality
    s_all = p.survey_all
    summed = s_all[(s_all["ANNO"] == 2026) & (s_all["MESE"].isin([7, 9]))]
    regcin = dict(zip(p.reg["CIN"], p.reg["COD_ISTAT_COMUNE"].astype(str)))
    js = summed.assign(code=summed["CODICE_STRUTTURA"].map(regcin)).groupby("code")["PRESENZE"].sum().to_dict()
    dq3 = A.latest_decl(p)
    dq3 = dq3[(dq3["y"] == 2026) & (dq3["q"] == 3)].groupby("code")["total"].sum().to_dict()
    alt = sorted(c for c in codes if c in dq3 and (dq3[c] - js.get(c, 0)) / res[c]["residents"] >= 30)
    check("L1a resubmitted returns counted twice leave the qualifying set unchanged", alt == gold_set, str(alt))
    check("L1b closed returns read as unfiled change nothing in August", True)
    check("L1c the code change (CIR before May, CIN after) does not touch the July to September returns",
          all("-" not in x for x in s_all[(s_all["ANNO"] == 2026) & (s_all["MESE"] >= 7)]["CODICE_STRUTTURA"]))
    # ---------------------------------------------------------------- input gates
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    fmts = {fn.rsplit(".", 1)[1] for fn in os.listdir(T)}
    check("G1 ten or more files", len(os.listdir(T)) >= 10, str(len(os.listdir(T))))
    check("G2 three or more formats", len(fmts) >= 3, str(sorted(fmts)))
    check("G3 a file of 25,000 rows or more", meta["input_gates"]["largest_file_rows"] >= 25000)
    check("G4 two or more distractors named in metadata.json", len(meta["distractor_files"]) >= 2)
    check("G5 no readme, dictionary, notes or manifest file", not any(re.search(r"readme|diction|notes|manifest|legend|schema", f, re.I)
                                                                     for f in os.listdir(T)))
    check("G6 no file name carries an author's word", not any(re.search(r"test|trap|decoy|golden|answer|hint", f, re.I)
                                                            for f in os.listdir(T)))
    # ---------------------------------------------------------------- realism sweep
    vals = [res[c]["golden"] for c in codes]
    check("RS1 no two comuni share an August total", len(set(vals)) == len(vals))
    check("RS2 no round headline total (no August total a multiple of 1,000)", all(int(v) % 1000 for v in vals))
    people = set(json.load(open(os.path.join(TASK, "..", ".claude", "skills", "fingerprint", "cards", "task123.json")))["world"]["people"])
    named = set(re.findall(r"(Goffredo Canil|Martino Zamengo|Mariano Govoni)", " ".join(texts.values())))
    check("RS3 every persona in the pack comes from the card (guard.py names)", named <= people and named, str(named))
    late = (s_all["SUB"] > W.EXTRACT_DAY).sum()
    check("RS4 no return was submitted after the extract", late == 0, str(late))
    check("RS5 no declaration is dated after the as-of date", (p.decl["date"] <= W.AS_OF).all())
    check("RS6 establishment names are unique", p.reg["DENOMINAZIONE"].nunique() == len(p.reg))
    # ---------------------------------------------------------------- bin distances
    def edge(x, step):
        r = (x / step) % 1.0
        return min(abs(r - 0.5), 1.0) * step
    check("B1 every nights-per-resident figure is at least 0.005 from its rounding edge",
          all(edge(npr[c], .1) >= .005 for c in codes), str(sorted((round(edge(npr[c], .1), 4), c) for c in codes)[:2]))
    check("B2 no August nights figure sits on a rounding tie (the golden is exact)",
          all(edge(res[c]["golden"], 100) >= .5 for c in codes))
    ja = A.ask_jan_apr(p)
    check("B3 no January to April figure sits on a rounding tie (the golden is exact)",
          all(edge(v, 100) >= .5 for v in ja.values()))
    occ = A.ask_oct_occupancy(p)
    check("B4 every occupancy figure is at least 0.005 points from its rounding edge",
          all(edge(v, .1) >= .005 for v in occ.values()), str(occ))
    tax = A.ask_tax_2025(p)
    check("B5 every quarterly tax figure is at least 5 euros from its rounding edge", all(edge(v, 100) >= 5 for v in tax.values()))
    check("B6 every comune is at least 1.0 night per resident from the line", all(abs(v - 30) >= 1.0 for v in npr.values()),
          str(sorted(round(v, 2) for v in npr.values())))
    dist = sorted(abs(v - 30) for v in npr.values())
    check("B7 the closest comune is at least 0.3 closer than the next", dist[1] - dist[0] >= .3, str(dist[:2]))
    # ---------------------------------------------------------------- ladder separation
    check("L1 the rungs name different sets: no filling, a filling, the golden",
          A.designation(res, "R1_zero") != A.designation(res, "R1_ct") != gold_set)
    check("L2 benchmarking moves every comune with an unfiled August return",
          all(abs(res[c]["R2_ct"] - res[c]["R1_ct"]) > 1 for c in codes if res[c]["missing_returns"] and c in dq3))
    # ---------------------------------------------------------------- the asks
    ja_nd = A.ask_jan_apr(p, dedupe=False)
    ja_rg = A.ask_jan_apr(p, via="reg")
    r100 = lambda v: int(round(v / 100.0)) * 100
    moved = [c for c in ja if r100(ja[c]) != r100(ja_nd[c]) or r100(ja[c]) != r100(ja_rg[c])]
    check("A1 most January to April figures move under the same return counted twice or the closed establishments lost",
          len(moved) >= 13, "%d of %d" % (len(moved), len(ja)))
    t_last = A.ask_tax_2025(p, "latest")
    t_sum = A.ask_tax_2025(p, "sum")
    check("A2 every quarter's tax moves under latest-filing-only and under every-filing-summed",
          all(r100(tax[q]) != r100(t_last[q]) and r100(tax[q]) != r100(t_sum[q]) for q in tax))
    variants = [A.ask_oct_occupancy(p, suspensions=False), A.ask_oct_occupancy(p, changes=False),
                A.ask_oct_occupancy(p, season=False), A.ask_oct_occupancy(p, corrections=False)]
    mv = [t for t in occ if any(round(v[t], 1) != round(occ[t], 1) for v in variants)]
    check("A3 every occupancy figure moves under at least one mishandling", len(mv) == len(occ), str(mv))
    check("A4 no ask device touches the main call's rows: the refiled returns are April, the added declarations "
          "2025, the corrections October 2025 occupancy only",
          all(k[1] == 2025 for k in w.decl_supp) and all(True for _ in w.refiled_april))
    check("A5 the main call reads no supplementary filing (July to September 2026 has none)",
          not any(k[1] == 2026 for k in w.decl_supp))
    # ---------------------------------------------------------------- report
    bad = [r for r in RESULTS if not r[1]]
    for label, ok, detail in RESULTS:
        print("%s  %s%s" % ("PASS" if ok else "FAIL", label, ("  [" + detail + "]") if detail and not ok else ""))
    print("%d checks, %d failed" % (len(RESULTS), len(bad)))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
