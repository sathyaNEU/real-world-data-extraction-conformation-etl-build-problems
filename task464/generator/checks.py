"""The generator's assertions for task464: the three rules executed on the clean truth (R1 to R3c), the convergence of
the concordance conventions (C1, SF6), every row of the semantic fork table (SF1 to SF14), the ladder and its margins,
the truth the concordance tracks, the Layer 1 items' neutrality, the ask's devices and stops, the separation of the
call from the ask, the distractors, the input gates and the realism sweep.

    python3 task464/generator/checks.py      (after build.py has written target/ and golden/)
"""
import csv
import json
import math
import os
import re
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import numpy as np     # noqa: E402

import bundle as B     # noqa: E402
import methods as M    # noqa: E402
import sim as S        # noqa: E402
import world as W      # noqa: E402

TASK = os.path.dirname(HERE)
FUNDED = {"1010", "1020", "1110", "1120", "1230", "1220"}
SIXTH, FIRST_OUT, GAP = "1220", "1240", 15
K1, K_REG = 241, 231
APP = set(W.APPLICANTS)
CUT = W.NEW_CUTS[8][0]


def slate(counts):
    top, nxt, tot = M.slate_of(counts)
    return set(top), nxt, tot[top[-1]] - tot[nxt], tot


def counts_from(pop, k, c=CUT):
    out = {d: [0, 0] for d in W.APPLICANTS}
    for p in pop:
        d, g, test, sc = p[0], p[1], p[2], p[4]
        if d in out and ((test == "new" and sc < c) or (test == "old" and sc <= k)):
            out[d][g - 9] += 1
    return out


def run(target, golden, x=None, meta_path=None, fig_path=None):
    bad = []

    def check(label, cond, detail=""):
        print("%s  %s%s" % ("PASS" if cond else "FAIL", label, ("  [" + str(detail) + "]") if detail != "" else ""))
        if not cond:
            bad.append(label)

    x = x or S.everything()
    F = json.load(open(fig_path or os.path.join(HERE, "figures.json")))
    meta = json.load(open(meta_path or os.path.join(TASK, "metadata.json")))
    for code, *_ in W.DISTRICTS:
        subs = [s for s, _, _ in W.MERGER[code]] if code in W.MERGER else [code]
        M.DIRECTORY_MID[code] = set(v for sub in subs for v in x["mid"][sub])

    # ------------------------------------------------------------------ the call from the pack
    pop = B.population(target, APP)
    old, new, schools, order = B.bridge(target)
    conv = M.conventions(old, new, CUT)
    ks = set(v[0] for k, v in conv.items() if k != "qcut_le")
    cnt = counts_from(pop, K1)
    top, nxt, gap, tot = slate(cnt)
    check("the call: fund %s; %s first left out, %d behind the sixth" % (
        ", ".join(W.short_name(d) for d in sorted(top, key=lambda d: -tot[d])), W.short_name(nxt), gap),
        top == FUNDED and nxt == FIRST_OUT and gap == GAP and ks == {K1} and set(F["call"]["funded"]) == FUNDED
        and F["call"]["gap"] == GAP and F["level1"] == tot)

    # ------------------------------------------------------------------ R1, the field's raw material ships
    heads = {}
    for f in sorted(os.listdir(target)):
        if f.endswith(".csv"):
            with open(os.path.join(target, f), encoding="utf-8") as fh:
                heads[f] = next(csv.reader(fh))
    check("R1 the bridge ships each student's two scores; both result files ship scale scores",
          {"glra_scale_score", "slm_scale_score"} <= set(heads[W.FILES["bridge"]])
          and "SCALE_SCORE" in heads[W.FILES["glra"]] and "scale_score" in heads[W.FILES["slm"]])
    conv_cols = [c for h in heads.values() for c in h if re.search(r"equiv|convert|concord|link|slm_level|placed|"
                                                                    r"predict|eligible", c, re.I)]
    check("R1 no shipped column holds the deciding quantity (an equivalent, a converted score, a placed level, an "
          "eligibility flag)", not conv_cols, conv_cols)

    # ------------------------------------------------------------------ R3, the three rules on the clean truth
    tpop = M.population(x, APP)
    K, tconv = M.placement(x)
    reg_top, reg_next, reg_gap, reg_tot = slate(counts_from(tpop, K["regression"]))
    check("R3a the analyst test: every field read right and every filed rule applied, the regression placement on the "
          "clean truth funds Harlenbrook in Elmorrow's place (Harlenbrook %d against Elmorrow %d)" % (
              reg_tot["1240"], reg_tot["1220"]),
          K["regression"] == K_REG and reg_top == FUNDED - {"1220"} | {"1240"} and reg_next == "1220"
          and (reg_tot["1240"], reg_tot["1220"]) == (323, 315))
    g_top, g_next, g_gap, g_tot = slate(counts_from(tpop, K["concordance"]))
    check("R3b the decisive step alone (a concordance from the bridge) funds the golden on the clean truth, every count "
          "equal to the pack's", K["concordance"] == K1 and g_top == FUNDED and g_tot == tot)
    from pypdf import PdfReader
    docs = {}
    for f in os.listdir(target):
        if f.endswith(".pdf"):
            docs[f] = re.sub(r"\s+", " ", " ".join(pg.extract_text() for pg in PdfReader(os.path.join(target, f)).pages))
    banned = r"concordan|equat(e|ing|ed)|\blink(ing|ed)?\b|regress|predict|equipercentile|percentile|z-score|" \
             r"standardi[sz]|equivalent|attenuat|measurement error|convert(ed|ing)? (a |the )?(retiring|score)"
    hits = {f: re.findall(banned, t, re.I) for f, t in docs.items()}
    check("R3c no document names the decisive step (a concordance, equating, linking, a regression, a prediction, "
          "percentiles, an equivalent)", not any(hits.values()), {f: v for f, v in hits.items() if v})
    graded = {v for v in list(tot.values()) + list(F["grade7_level1"].values()) if v >= 1000}
    seen = {f: sorted(v for v in graded if re.search(r"(?<![\d,.])%s(?![\d,])" % "{:,}".format(v), t))
            for f, t in docs.items()}
    check("R3c no graded count of four digits appears in a document", not any(seen.values()),
          {f: v for f, v in seen.items() if v})
    small = {v for v in list(tot.values()) + list(F["grade7_level1"].values()) if 10 <= v < 1000}
    near = {f: sorted(v for v in small if re.search(r"(?<![\d,.])%d (students|eligible)" % v, t))
            for f, t in docs.items()}
    check("R3c no graded count appears in a document as a number of students", not any(near.values()),
          {f: v for f, v in near.items() if v})
    check("R3c no file ranks or counts the applicants (the rules list them with their notice dates only)",
          not re.search(r"Level 1 students|students at Level 1|eligible students: \d", docs[W.FILES["rules"]]))

    # ------------------------------------------------------------------ C1 and SF6, the concordance conventions agree
    for c, want in zip(W.NEW_CUTS[8], F["boundaries"]):
        cv = M.conventions(old, new, c)
        kk = set(v[0] for k, v in cv.items() if k != "qcut_le")
        mins = {u: round(min(v[1] for k, v in cv.items() if v[2] == u and not k.startswith("nearest")
                             and k != "qcut_le"), 2) for u in ("points", "students")}
        check("SF6 C1 at the cut %d all %d conventions place %d highest below it, with room (%s)" % (
            c, len(cv) - 1, want, mins), kk == {want} and M.agree(cv), mins)
    rng = np.random.default_rng(464)
    for c, want in zip(W.NEW_CUTS[8], F["boundaries"]):
        ok = 0
        for t in range(25):
            keep = rng.random(len(old)) > 0.02
            ok += set(v[0] for k, v in M.conventions(old[keep], new[keep], c).items() if k != "qcut_le") == {want}
        ok_s = sum(set(v[0] for k, v in M.conventions(old[schools != s_], new[schools != s_], c).items()
                       if k != "qcut_le") == {want} for s_ in sorted(set(schools)))
        check("SF6 at the cut %d the agreement survives any 2 per cent of the rows (25 draws) and any one school left "
              "out (%d schools)" % (c, len(set(schools))), ok == 25 and ok_s == len(set(schools)), (ok, ok_s))
    half = [set(v[0] for k, v in M.conventions(old[order == o], new[order == o], CUT).items() if k != "qcut_le")
            for o in ("GLRA first", "SLM first")]
    check("SF6 each order group alone places 241 too (the order of testing moves nothing)", half == [{K1}, {K1}], half)

    # ------------------------------------------------------------------ SF5, the data separate the placements
    b, a = np.polyfit(old, new, 1)
    share_new = 100 * float(np.mean(new < CUT))
    share_reg = 100 * float(np.mean(a + b * old < CUT - 0.5))
    share_conc = 100 * float(np.mean(old <= K1))
    check("SF5 placed by the regression %.1f per cent of the bridge students sit at Level 1 against %.1f per cent on "
          "the new test; the concordance %.1f per cent, the nearest the form's scores allow" % (
              share_reg, share_new, share_conc),
          round(share_reg, 1) == 11.1 and round(share_new, 1) == 15.7 and round(share_conc, 1) == 14.6
          and abs(share_conc - share_new) < abs(100 * np.mean(old <= 249) - share_new))

    # ------------------------------------------------------------------ the ladder
    want = {"regression": (231, "1240", "1220"), "cohort_percentiles": (231, "1240", "1220"),
            "cohort_z": (231, "1240", "1220"), "old_levels": (220, "1240", "1220"), "inverse": (249, None, "1240"),
            "scale_range": (265, None, "1210")}
    for route, (k, inn, out) in want.items():
        t_, n_, g_, tt = slate(counts_from(tpop, K[route]))
        if route == "old_levels":
            ok = K[route] == k and "1240" in t_ and "1220" not in t_
        elif inn:
            ok = K[route] == k and n_ == out and t_ == (FUNDED - {"1220"}) | {inn}
        else:
            ok = K[route] == k and n_ == out and t_ == FUNDED
        check("ladder %s: retiring scores of %d and below, %s" % (route, k, "funds %s" % W.short_name(inn) if inn
                                                                  else "the golden six with every count off"),
              ok and (inn or all(tt[d] != tot[d] for d in W.APPLICANTS)), (K[route], sorted(t_), n_))
    yv = (new < CUT).astype(float)
    X = np.column_stack([np.ones_like(old, dtype=float), (old - 300) / 50.0])
    beta = np.zeros(2)
    for _ in range(60):
        p = 1 / (1 + np.exp(-X @ beta))
        beta += np.linalg.solve(X.T @ (X * (p * (1 - p))[:, None]), X.T @ (yv - p))
    xs = 300 - 50 * beta[0] / beta[1]
    A = W.glra_attainable(8)
    maj = [a_ for a_ in A if np.any(old == a_) and np.mean(new[old == a_] < CUT) > 0.5]
    check("ladder R0b: a logistic classifier (boundary %.1f) and the per-score majority both place 231 highest" % xs,
          int(A[A < xs].max()) == K_REG and max(maj) == K_REG, (round(xs, 1), max(maj)))
    check("margins: the sixth (Elmorrow 368) leads the first left out by 15, the fifth (Garnet Hills 372) by 19; under the "
          "regression Harlenbrook leads Elmorrow by 8",
          (tot["1220"], tot["1230"], tot["1240"]) == (368, 372, 353) and reg_tot["1240"] - reg_tot["1220"] == 8)

    # ------------------------------------------------------------------ the truth the concordance tracks
    exp = {d: 0.0 for d in W.APPLICANTS}
    for sp in x["spells"]:
        if sp["grade"] in (9, 10) and M.on_count_day(sp) and sp["district"] in APP:
            res = M.latest_grade8(sp["who"])
            if not res:
                continue
            if res[0] == "new":
                exp[sp["district"]] += res[2] < CUT
            else:
                z = (CUT - 0.5 - (W.NEW["mean"] + W.NEW["slope"] * sp["who"]["theta"])) / W.NEW["err"]
                exp[sp["district"]] += 0.5 * (1 + math.erf(z / math.sqrt(2)))
    o = sorted(exp, key=lambda d: -exp[d])
    check("truth: the 2025 cohort's expected Level 1 count on the new test funds the golden six (%.1f between the sixth "
          "and the seventh) and not the regression's" % (exp[o[5]] - exp[o[6]]),
          set(o[:6]) == FUNDED and exp[o[5]] - exp[o[6]] > 20 and set(o[:6]) != reg_top)

    # ------------------------------------------------------------------ the semantic fork table on the clean truth
    def variant(label, vp):
        t_, n_, g_, _ = slate(counts_from(vp, K1))
        check(label + " (sixth to seventh %d)" % g_, t_ == FUNDED and g_ >= 5, g_)

    spells = [sp for sp in x["spells"] if sp["grade"] in (9, 10) and sp["district"] in APP]
    days = [d for sp in x["spells"] for d in (sp["entry"], sp["exit"]) if d]
    check("SF1 no spell opens or closes on October 1 or 2", not any(d in ("2026-10-01", "2026-10-02") for d in days))
    allsp = []
    for sp in spells:
        res = M.latest_grade8(sp["who"])
        if res:
            allsp.append((sp["district"], sp["grade"], res[0], res[1], res[2], sp["who"]["sid"]))
    variant("SF1 every spell kept, late entrants, September withdrawals and closed transfers included: same call", allsp)
    openonly = []
    for sp in spells:
        if sp["exit"] == "" and sp["entry"] <= W.COUNT_DAY:
            res = M.latest_grade8(sp["who"])
            if res:
                openonly.append((sp["district"], sp["grade"], res[0], res[1], res[2], sp["who"]["sid"]))
    octo = sum(1 for sp in spells if sp.get("october"))
    variant("SF1 only the spells still open at the extract (%d October withdrawals and transfers left out): same call"
            % octo, openonly)
    merged = {sub: new_ for new_, parts in W.MERGER.items() for sub, _, _ in parts}
    tested = []
    for sp in x["spells"]:
        if sp["grade"] in (9, 10) and M.on_count_day(sp):
            s = sp["who"]
            res = M.latest_grade8(s)
            if res:
                tested.append((merged.get(s["tested_in"], s["tested_in"]), sp["grade"], res[0], res[1], res[2], s["sid"]))
    variant("SF2 and SF7 counted by the district of the grade 8 test, the predecessor codes joined: same call", tested)

    def latest_by(rule):
        out = []
        for sp in x["spells"]:
            if sp["grade"] in (9, 10) and M.on_count_day(sp) and sp["district"] in APP:
                best = None
                for r in sp["who"].get("records", []):
                    if r["grade"] != 8:
                        continue
                    sc = rule(r)
                    if sc is not None and (best is None or (r["year"] < best[1] if rule is early else r["year"] > best[1])):
                        best = (r["test"], r["year"], sc)
                if best:
                    out.append((sp["district"], sp["grade"], best[0], best[1], best[2], sp["who"]["sid"]))
        return out

    def early(r):
        return M.result(r)
    variant("SF3 the earliest grade 8 result: same call", latest_by(early))
    variant("SF3 make-up sessions ignored: same call", latest_by(lambda r: r["score"] if r["status"] == "scored" else None))
    variant("SF3 the invalidated score kept as the result: same call",
            latest_by(lambda r: r["score"] if r["status"] in ("scored", "invalid") else None))
    lv_ok = all(r["performance_level"] == str(1 + sum(int(r["scale_score"]) >= c for c in W.NEW_CUTS[8]))
                for r in B.rows(target, "slm") if r["grade"] == "8" and r["status"] == "Scored")
    check("SF4 the file's performance level agrees with the 2415, 2508 and 2579 cuts on every scored grade 8 row", lv_ok)
    npids = set(s["sid"] for s in x["students"] if s.get("nonpublic"))
    variant("SF8 nonpublic schools' results left out: same call", [p for p in tpop if p[5] not in npids])
    variant("SF9 grade 9 students placed through the retiring test left out: same call",
            [p for p in tpop if not (p[1] == 9 and p[2] == "old")])
    allpop = M.population(x)
    allc = {d: [0, 0] for d in set(p[0] for p in allpop)}
    for p in allpop:
        if (p[2] == "new" and p[4] < CUT) or (p[2] == "old" and p[4] <= K1):
            allc[p[0]][p[1] - 9] += 1
    at, an, ag, att = slate(allc)
    check("SF10 and SF11 no tie at the sixth place, and no district outside the fourteen would rank in the top six",
          gap > 0 and at == FUNDED, sorted(at))
    xw = set(r["TEST_TAKER_ID"] for r in B.rows(target, "crosswalk"))
    gl = B.rows(target, "glra")
    check("Closure 16: every retiring-test row's test-taker number is in the crosswalk",
          all(r["TEST_TAKER_ID"] in xw for r in gl))
    sid_blank = set()
    for s in x["students"]:
        for r in s["records"]:
            if r["test"] == "old" and r["grade"] == 8 and not r["sid_on_file"]:
                sid_blank.add(s["sid"])
    variant("Layer 1: retiring-test grade 8 results without a state identifier on the row dropped: same call",
            [p for p in tpop if not (p[2] == "old" and p[5] in sid_blank)])

    # ------------------------------------------------------------------ the ask: golden, devices and stops
    g7 = B.grade7(target)
    check("SF14 Ask A golden from the pack (scored sessions and make-ups, the directory's schools, the adopted cut) "
          "equals figures.json (14 counts, 14 shares)",
          all(g7[d][0] == F["grade7_level1"][d] and round(100.0 * g7[d][0] / g7[d][1], 1) == F["grade7_share"][d]
              for d in W.APPLICANTS))
    for by, cuts, label in (("vendor", "june", "the file's district code and its performance level (the cracker)"),
                            ("directory", "june", "the directory's schools and the file's performance level"),
                            ("vendor", "adopted", "the file's district code and the adopted cut")):
        v = B.grade7(target, by, cuts)
        miss_c = all(v[d][0] != g7[d][0] for d in W.APPLICANTS)
        miss_s = all(round(1000.0 * v[d][0] / v[d][1]) != round(1000.0 * g7[d][0] / g7[d][1]) for d in W.APPLICANTS)
        check("SF12 SF13 Ask A stop, %s: every applicant's count and share missed" % label, miss_c and miss_s,
              [W.short_name(d) for d in W.APPLICANTS if v[d][0] == g7[d][0]
               or round(1000.0 * v[d][0] / v[d][1]) == round(1000.0 * g7[d][0] / g7[d][1])])
    sch_dir, _ = B.directory(target)
    band = {d: 0 for d in W.APPLICANTS}
    npl1 = {d: 0 for d in W.APPLICANTS}
    for r in B.rows(target, "slm"):
        if r["grade"] != "7" or r["status"] != "Scored":
            continue
        sc = int(r["scale_score"])
        d = sch_dir.get(r["school_code"])
        if d in band and W.NEW_CUTS_JUNE[7][0] <= sc < W.NEW_CUTS[7][0]:
            band[d] += 1
        if d is None and sc < W.NEW_CUTS[7][0]:
            dd = merged.get(r["district_code"], r["district_code"])
            if dd in npl1:
                npl1[dd] += 1
    check("Ask A device D2: every applicant has grade 7 scores from 2383 to 2389 (Level 2 in the file, Level 1 adopted)",
          min(band.values()) >= 3, min(band.values()))
    check("Ask A device D5: every applicant has a nonpublic grade 7 test taker at Level 1 under its district code",
          min(npl1.values()) >= 1, min(npl1.values()))
    np_codes = set(r["school_code"] for r in B.rows(target, "nonpublic"))
    unmatched = set(r["school_code"] for r in B.rows(target, "slm") if r["school_code"] not in sch_dir)
    check("Ask A fairness: every school code outside the directory is a registered nonpublic school",
          unmatched == np_codes or unmatched <= np_codes, sorted(unmatched - np_codes)[:5])

    # ------------------------------------------------------------------ separation of the call and the ask
    g7ids = set(r["state_student_id"] for r in B.rows(target, "slm") if r["grade"] == "7")
    rollids = set(B.roll(target).keys())
    check("separation: none of the spring 2026 grade 7 test takers is in grade 9 or 10 on the count day",
          not (g7ids & rollids))
    check("separation: the call reads only grade 8 rows of the two result files and no registry or resolution row",
          all(p[2] in ("old", "new") for p in pop) and len(pop) == F["counted"])

    # ------------------------------------------------------------------ distractors and the input gates
    files = sorted(os.listdir(target))
    rows = {f: (sum(1 for _ in open(os.path.join(target, f), encoding="utf-8")) - 1) for f in files if f.endswith(".csv")}
    check("input gates: %d files, %d formats, the largest %s with %d rows" % (
        len(files), len({f.rsplit(".", 1)[1] for f in files}), max(rows, key=rows.get), max(rows.values())),
          len(files) >= 10 and len({f.rsplit(".", 1)[1] for f in files}) >= 3 and max(rows.values()) >= 25000)
    check("distractors: two named in metadata.json, neither read by the golden",
          sorted(meta["distractor_files"]) == sorted(W.FILES[k] for k in W.DISTRACTORS))

    # ------------------------------------------------------------------ the goldens agree with figures.json
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(golden, W.GOLDEN["workbook"]), data_only=True)
    ws = wb["Applicants"]
    wrows = [r for r in ws.iter_rows(min_row=5, values_only=True) if r[0]]
    check("golden workbook: every applicant's count, grade 7 count and share equal figures.json",
          len(wrows) == 14 and all(r[4] == F["level1"][r[0]] and r[7] == F["grade7_level1"][r[0]]
                                   and r[8] == F["grade7_share"][r[0]] and (r[5] == "Yes") == (r[0] in FUNDED)
                                   for r in wrows))
    with open(os.path.join(golden, W.GOLDEN["table"]), encoding="utf-8") as fh:
        crow = list(csv.DictReader(fh))
    lev = {k: sum(1 for r in crow if r["slm_level"] == str(k)) for k in (1, 2, 3, 4)}
    l1 = {d: 0 for d in W.APPLICANTS}
    for r in crow:
        if r["slm_level"] == "1":
            l1[r["district_code"]] += 1
    check("golden conformed file: %d rows, each applicant's Level 1 rows equal its count" % len(crow),
          len(crow) == F["conformed_rows"] == F["counted"] and l1 == tot
          and lev == {int(k): v for k, v in F["conformed_levels"].items()})
    with zipfile.ZipFile(os.path.join(golden, W.GOLDEN["workbook"])) as z:
        names = z.namelist()
        png = [n for n in names if n.endswith(".png")]
    check("golden workbook carries its chart as an image on the Chart sheet", bool(png) and "Chart" in wb.sheetnames)

    # ------------------------------------------------------------------ the realism sweep
    dash = [f for f in files if not f.endswith((".xlsx", ".pdf"))
            and re.search("[–—]", open(os.path.join(target, f), encoding="utf-8").read())]
    dash += [f for f, t in docs.items() if re.search("[–—]", t)]
    check("realism: no em or en dash in any file", not dash, dash)
    late = []
    for f in files:
        if f.endswith(".csv"):
            t = open(os.path.join(target, f), encoding="utf-8").read()
            late += [(f, d) for d in set(re.findall(r"20\d\d-\d\d-\d\d", t)) if d > W.AS_OF]
    check("realism: no date after the folder's as-of date (%s)" % W.AS_OF, not late, late[:5])
    nulls = [f for f in files if f.endswith(".csv")
             and re.search(r"(^|,)(None|nan|NaN|True|False)(,|\r?$)", open(os.path.join(target, f), encoding="utf-8").read(),
                           re.M)]
    check("realism: no Python null or boolean in any file", not nulls, nulls)
    tool = []
    for f in files:
        blob = open(os.path.join(target, f), "rb").read()
        if f.endswith(".xlsx"):
            with zipfile.ZipFile(os.path.join(target, f)) as z:
                blob = b"".join(z.read(n) for n in z.namelist())
        if re.search(rb"openpyxl|reportlab|matplotlib|ReportLab|python", blob):
            tool.append(f)
    check("realism: no writing library named in any file's container", not tool, tool)
    ids = [r["state_student_id"] for r in B.rows(target, "bridge")]
    check("realism: one bridge row per student", len(ids) == len(set(ids)))
    dups = {}
    for f in files:
        if f.endswith(".csv"):
            with open(os.path.join(target, f), encoding="utf-8") as fh:
                body = fh.read().splitlines()[1:]
            dups[f] = len(body) - len(set(body))
    check("R3c realism: no copied block, no repeated record in any file", not any(dups.values()),
          {f: v for f, v in dups.items() if v})
    per = {}
    for r in B.rows(target, "enrollment"):
        per[(r["district_code"], r["grade"])] = per.get((r["district_code"], r["grade"]), 0) + 1
    clash = [g for g in "9 10 11 12".split() if len({v for (d, gg), v in per.items() if gg == g})
             < len([1 for (d, gg) in per if gg == g])]
    check("realism: no two districts with the same enrolment count in a grade", not clash, clash)
    big = {f: n for f, n in rows.items() if n >= 1000}
    check("realism: no large file with a round number of records", all(n % 100 for n in big.values()), big)
    print("%d checks failed" % len(bad) if bad else "all checks passed")
    return not bad


if __name__ == "__main__":
    ok = run(os.path.join(TASK, "target"), os.path.join(TASK, "golden"))
    sys.exit(0 if ok else 1)
