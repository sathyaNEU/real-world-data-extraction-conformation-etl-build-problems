"""task448 assertions: the input gates, the three rules (R1 to R3c), the ladder with every rung computed from the
pack, the separation and the grid, the semantic fork rows SF1 to SF10 and the estimator family inside every graded
bin, the asks' devices and crackers, mess neutrality item by item, consistency between the deliverables, and the
realism sweep. Run by build.py after every build; exits on the first failure."""
import datetime as dt
import json
import os
import re
import shutil
import tempfile
import zipfile

import numpy as np
import pandas as pd

import calc as C
import docs as DC
import golden as G
import pack as P
import world as W

N_PASS = [0]
GOLD = ["Corvane Home Loans, LLC", "Weyrauch State Bank", "Halverd Mortgage Company", "Mennwell Credit Union",
        "Arkhaven Bank, N.A."]
SIXTH = "Shunga Valley Bank"


def ok(cond, label, detail=""):
    if not cond:
        raise SystemExit("CHECK FAILED: %s %s" % (label, detail))
    N_PASS[0] += 1
    print("  ok  %-66s %s" % (label, detail))


def names(top):
    return [n for n, _ in top]


def edge(x):
    return 5.0 - abs(x - C.r10(x))


def same_bins(a, b, keys):
    return all(C.r10(a[k]) == C.r10(b[k]) for k in keys)


def run(target, golden, world=None, meta_path=None):
    print("task448 checks")
    B = C.load(target)
    F = B["F"]
    files = sorted(os.listdir(target))
    meta = json.load(open(meta_path)) if meta_path else {}

    # ------------------------------------------------------------------------------------------ input gates ----
    ok(len(files) >= 10, "gate: ten or more files", str(len(files)))
    fmts = {f.rsplit(".", 1)[1] for f in files}
    ok(len(fmts) >= 3, "gate: three or more formats", ",".join(sorted(fmts)))
    lar_rows = sum(1 for _ in open(os.path.join(target, P.FILES["lar"]))) - 1
    ok(lar_rows >= 25000, "gate: one file of 25,000 rows or more", "%s %d" % (P.FILES["lar"], lar_rows))
    dis = meta.get("distractor_files", [])
    ok(len(dis) >= 2 and all(d in files for d in dis), "gate: two or more distractors, shipped", ", ".join(dis))
    ok(not any("distractor" in f.lower() for f in files), "gate: no file name says distractor")
    man = pd.read_csv(os.path.join(target, P.FILES["manifest"]))
    ok(set(man.file) == set(files) - {P.FILES["manifest"]}, "H9 the manifest lists every other shipped file")
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(target, DC.DICTIONARY), read_only=True)
    named = " ".join(str(c.value) for ws in wb for row in ws.iter_rows() for c in row if c.value)
    covered = [f for f in files if f in named or (f.startswith("venridge_pmm_ks8_") and "venridge_pmm_ks8_" in named)]
    ok(set(covered) >= set(files) - {P.FILES["manifest"], DC.DICTIONARY, DC.GUIDELINES, DC.LAYOUT},
       "H9 the dictionary names every data file")
    reg = pd.read_csv(os.path.join(target, P.FILES["deliveries"]))
    feed_rows = {f: sum(1 for _ in open(os.path.join(target, f))) - 1 for f in C.FEEDS}
    ok(all(int(r.rows) == feed_rows[r.file_name] for r in reg.itertuples()),
       "context artifact: the delivery register ties to every delivery", str(feed_rows))
    mt = {int(os.path.getmtime(os.path.join(target, f))) for f in files}
    ok(len(mt) == 1, "hygiene: one export time on every file")

    # ------------------------------------------------------------------------------------------- identities ----
    leis = set(B["panel"].lei) | {x for x in B["register"].lei if x}
    ok(all(W.lei_ok(x) for x in leis), "identity: every LEI carries valid ISO 17442 check digits", str(len(leis)))
    lender_rows = F[~F.seller_note]
    ok((lender_rows.nmls != "").all(), "identity: every lender's mortgagee text resolves through the alias register",
       "%d rows" % len(lender_rows))
    sn = F[F.seller_note]
    ok(len(sn) > 0 and (sn.MORTGAGEE_NAME == sn.GRANTOR_NAME).all(),
       "identity: the rows that resolve to no lender are notes carried by the seller", str(len(sn)))
    short = B["short"]
    ok(len(short) == 12 and all(n in set(B["register"].nmls_id) for n, _ in short),
       "identity: twelve shortlisted lenders, each in the lender register")
    rep = [nm for n, nm in short if B["lei_of"].get(n, "") in B["hmda"].index]
    ok(len(rep) == 7, "identity: seven shortlisted lenders report HMDA, five do not", ", ".join(rep))

    # ----------------------------------------------------------------------------- R1: the raw material ships ----
    banned = re.compile(r"route|capture|package|paired|estimate|share_of|coverage", re.I)
    cols = []
    for f in files:
        p = os.path.join(target, f)
        if f.endswith(".csv"):
            cols += list(pd.read_csv(p, nrows=0).columns)
        elif f.endswith(".txt"):
            cols += open(p).readline().strip().split("|")
    ok(not any(banned.search(c) for c in cols), "R1 no shipped column holds a route, capture or estimate",
       "%d columns" % len(cols))
    win = F[F.mortgage & F.MTG_INSTR_DATE.between(*C.WIN)]
    purity = win.groupby("nmls").packaged.mean()
    ok(set(purity.round(6).unique()) <= {0.0, 1.0},
       "R1 each lender's 2024 and 2025 mortgages record one way (built from the paired dates)",
       "%d lenders" % len(purity))
    pk = F[F.packaged & ~F.rerecord]
    num = lambda s: int(re.sub(r"\D", "", s)[-6:])
    gap = [num(a) - num(b) for a, b in zip(pk.MTG_DOC_NO, pk.DEED_DOC_NO)]
    ok(all(1 <= g <= 3 for g in gap), "R1 a mortgage recorded the same day as its deed follows it in the series",
       "%d rows" % len(gap))
    sep = F[~F.packaged & F.mortgage]
    ok((sep.MTG_REC_DATE > sep.DEED_REC_DATE).all(), "R1 every other mortgage is recorded after its deed",
       "%d rows" % len(sep))
    ok(not any(c.lower() in ("loans", "count", "volume", "originations") for c in
               list(B["alias"].columns) + list(B["register"].columns)),
       "R1 no register carries a lender's volume")

    # --------------------------------------------------------------------------------------------- the ladder ----
    caps, route = C.captures(B)
    ok(abs(caps["P"] - 0.9665) < 0.004 and abs(caps["S"] - 0.5975) < 0.004,
       "ladder: the file holds about 97 per cent packaged, 60 per cent separate", "%.4f %.4f" % (caps["P"], caps["S"]))
    rungs = {"R0": C.estimate(B) if False else C.lender_counts(B, "hmda_only"),
             "R1": C.lender_counts(B, "unscaled"), "R2": C.lender_counts(B, "pooled"),
             "R3 charter": C.estimate(B, stratum="charter"), "R3 county": C.lender_counts_county(B),
             "R3 year": C.lender_counts_year(B), "R4": C.estimate(B, sel=lambda F: F.mortgage | F.qcd),
             "golden": C.estimate(B)}
    tops = {k: C.five(v) for k, v in rungs.items()}
    ok(names(tops["golden"][0]) == GOLD and tops["golden"][1][0] == SIXTH, "ladder: the golden five in order, sixth",
       " | ".join("%s %.1f" % (n.split()[0], x) for n, x in tops["golden"][0]))
    expect = {"R0": {"Corvane Home Loans, LLC", "Halverd Mortgage Company", "Arkhaven Bank, N.A.", "Shunga Valley Bank",
                     "Tessaline Home Lending, Inc."},
              "R1": {"Corvane Home Loans, LLC", "Halverd Mortgage Company", "Arkhaven Bank, N.A.", "Weyrauch State Bank",
                     "Shunga Valley Bank"},
              "R4": {"Corvane Home Loans, LLC", "Weyrauch State Bank", "Halverd Mortgage Company",
                     "Heidebrecht State Bank", "Mennwell Credit Union"}}
    for k in ("R0", "R1", "R4"):
        ok(set(names(tops[k][0])) == expect[k], "ladder: %s recruits its own wrong five" % k,
           " | ".join("%s %.1f" % (n.split()[0], x) for n, x in tops[k][0]))
    for k in ("R2", "R3 charter", "R3 county", "R3 year"):
        ok(set(names(tops[k][0])) == expect["R1"], "ladder: %s recruits the default path's five" % k,
           " | ".join("%s %.1f" % (n.split()[0], x) for n, x in tops[k][0]))
    g = rungs["golden"]
    vals = [g[n] for n in GOLD]
    ratios = [vals[i] / vals[i + 1] for i in range(4)]
    ok(min(ratios) >= 1.11, "SF8 separation: neighbours in the golden five at least 1.11 apart",
       " ".join("%.3f" % r for r in ratios))
    ok(g[GOLD[4]] / g[SIXTH] >= 1.20, "separation: the fifth clears the sixth by 1.20", "%.3f" % (g[GOLD[4]] / g[SIXTH]))
    seventh = sorted(g.items(), key=lambda kv: -kv[1])[6]
    ok(g[SIXTH] / seventh[1] >= 1.06, "separation: the sixth clears the seventh by 1.06",
       "%s %.3f" % (seventh[0], g[SIXTH] / seventh[1]))
    for k, (t, s) in tops.items():
        if k == "golden":
            continue
        wrong = [n for n in names(t) if n not in GOLD]
        ok(wrong and all(rungs[k][n] >= 1.05 * rungs[k][t[4][0]] or rungs[k][n] > rungs[k][s[0]] for n in wrong),
           "separation: %s's intruder sits in its five, not on its edge" % k, ", ".join(w.split()[0] for w in wrong))
    d_rank = [n for n, _ in sorted(rungs["R1"].items(), key=lambda kv: -kv[1])]
    ok(d_rank.index("Mennwell Credit Union") >= 6 and d_rank.index("Weyrauch State Bank") == 3,
       "position: the default path puts Mennwell seventh or lower, Weyrauch fourth",
       "%d, %d" % (d_rank.index("Mennwell Credit Union") + 1, d_rank.index("Weyrauch State Bank") + 1))
    # the grid: route strata (S) and the erroneous enumerations out (E)
    grid = {"SE": C.estimate(B), "S-": C.estimate(B, sel=lambda F: F.mortgage | F.qcd),
            "-E": C.estimate(B, stratum="pooled"), "--": C.estimate(B, sel=lambda F: F.mortgage | F.qcd, stratum="pooled")}
    for k, v in grid.items():
        t, _ = C.five(v)
        if k == "SE":
            ok(names(t) == GOLD, "grid: route strata with the erroneous enumerations out is the golden")
        else:
            ok(set(names(t)) != set(GOLD), "grid: cell %s recruits a wrong five" % k,
               ", ".join(n.split()[0] for n in names(t)))
    pooled_c = C.capture(B)["all"]
    gap_route = caps["P"] - caps["S"]
    other = []
    for strat in ("charter",):
        cc = C.capture(B, stratum=lambda n: dict(zip(B["register"].nmls_id, B["register"].institution_type))[n])
        other.append(max(cc.values()) - min(cc.values()))
    ok(gap_route >= 1.2 * max(other), "dominance: the route splits capture wider than any filed attribute",
       "%.3f against %.3f" % (gap_route, max(other)))
    ok(abs(pooled_c - 0.898) < 0.01, "worth: the pooled capture sits between the routes", "%.4f" % pooled_c)

    # ---------------------------------------------------------------------------------------- the three rules ----
    w = world
    M = w["M"]
    LX = {x["id"]: x for x in w["LX"]}
    tw = M[M.close.map(lambda d: C.WIN[0] <= d <= C.WIN[1])]
    truth_hmda = tw.groupby("lender").size()
    truth_rows = tw[tw.captured].groupby("lender").size()
    reps_t = [i for i, x in LX.items() if x["kind"] == "R"]
    sl = W.SHORTLIST

    def truth_counts(cap):
        return {LX[i]["name"]: float(truth_hmda[i]) if LX[i]["kind"] == "R" else float(truth_rows.get(i, 0)) / cap(i)
                for i in sl}
    rt = {i: LX[i]["route"] for i in LX}
    pc = truth_rows.reindex(reps_t).fillna(0).sum() / truth_hmda.reindex(reps_t).sum()
    rc = {r: truth_rows.reindex([i for i in reps_t if rt[i] == r]).fillna(0).sum() /
          truth_hmda.reindex([i for i in reps_t if rt[i] == r]).sum() for r in "PS"}
    t_def, _ = C.five(truth_counts(lambda i: 1.0))
    t_pool, _ = C.five(truth_counts(lambda i: pc))
    t_route, t_six = C.five(truth_counts(lambda i: rc[rt[i]]))
    ok(set(names(t_def)) == expect["R1"], "R3a the default path on the clean truth files the named wrong five")
    ok(set(names(t_pool)) == expect["R1"], "R3a the strong analyst's pooled capture on the clean truth is wrong too")
    ok(names(t_route) == GOLD and t_six[0] == SIXTH, "R3b the default path with only the route strata is the golden")
    for k in ("R0", "R2", "R3 charter", "R3 county", "R3 year"):
        ok(set(names(tops[k][0])) != set(GOLD), "R3b the lower single correction %s stays wrong" % k)
    text = []
    for f in files:
        p = os.path.join(target, f)
        if f.endswith(".pdf"):
            from pypdf import PdfReader
            text.append(" ".join(pg.extract_text() for pg in PdfReader(p).pages))
        elif f.endswith(".xlsx"):
            wbx = openpyxl.load_workbook(p, read_only=True)
            text.append(" ".join(str(c.value) for ws in wbx for row in ws.iter_rows() for c in row if c.value))
    doc_text = " ".join(text).lower()
    for word in ("capture", "package", "same day", "route", "pooled", "stratif", "dual-system", "match rate"):
        ok(word not in doc_text, "R3c no document names the decisive step (%s)" % word)
    ok(not re.search(r"(?i)rank|largest|most active", doc_text), "R3c no document ranks the lenders")
    lar = pd.read_csv(os.path.join(target, P.FILES["lar"]), dtype=str)
    dup = lar.duplicated().mean()
    ok(dup < 0.005, "R3c no copied block in the loan-level file", "duplicate rows %.4f" % dup)

    # ------------------------------------------------------------------------------- R2: mess, item by item ----
    gold = C.estimate(B)
    graded = GOLD + [SIXTH]

    def mess(label, v, bins=True):
        t, s = C.five(v)
        okk = names(t) == GOLD and s[0] == SIXTH and (not bins or same_bins(v, gold, graded))
        ok(okk, "R2 %s leaves the call%s" % (label, " and its counts" if bins else ""),
           " | ".join("%s %.1f" % (n.split()[0], x) for n, x in t))
    mess("the 2026 delivery left unread", C.estimate(B, sel=lambda F: F.mortgage & (F.file != C.FEEDS[2])))
    mess("re-recordings kept", C.estimate(B, sel=lambda F: F.mortgage | (F.rerecord & (F.nmls != ""))))
    mess("SF3 second mortgages kept", C.estimate(B, sel=lambda F: F.mortgage | (F.second & ~F.rerecord & ~F.qcd)))
    mess("SF6 two-county farmsteads counted twice", C.estimate(B, sel=lambda F: F.mortgage | F.land_row))
    mess("SF1 HMDA purchased loans counted as made",
         C.estimate(B, hmda=B["hmda"].add(B["hmda_bought"], fill_value=0)))
    mess("SF2 the recording date taken for the closing", C.estimate(B, datecol="MTG_REC_DATE"))
    mess("SF3 trust and estate sellers' deeds read as non-arm's-length (7.4)",
         C.estimate(B, sel=lambda F: F.mortgage & ~F.DEED_TYPE.isin(["EXD", "TRD"])), bins=False)
    ex = lar[lar.county_code.isin(C.FIPS.values())]
    ok(not ex[["action_taken", "loan_purpose", "lien_status"]].isin(["Exempt", "1111"]).any().any(),
       "R2 the partial exemption never touches action, purpose or lien")
    hm_reg = B["hmda"]
    tot_ok = all(int(hm_reg.get(LX[i]["lei"], 0)) == int(truth_hmda[i]) for i in reps_t)
    ok(tot_ok, "R2 SF4 HMDA's postal-city county codes move no loan into or out of the eight counties")
    two_dup = M[M.land_county != ""]
    ok(not set(two_dup.lender) & {i for i in LX if LX[i]["name"] in graded},
       "R2 no two-county farmstead belongs to the five or the sixth", ", ".join(sorted(set(two_dup.lender))))
    sw = M[(M.lender.map(lambda i: LX[i]["route"]) == "S") & (M.route == "P")]
    ok(len(sw) > 0 and sw.close.min() >= W.SWITCH and not sw.close.map(lambda d: d <= C.WIN[1]).any(),
       "R2 no in-house lender's mortgage closing in 2024 or 2025 records with the deed",
       "%d switched, first %s" % (len(sw), sw.close.min()))

    # ----------------------------------------------------------------------------------------- fork table ----
    ok(not B["hmda_bought"].index.isin([B["lei_of"][n] for n, _ in short]).any(),
       "SF1 no shortlisted lender buys loans, so 'made' moves no count", str(B["hmda_bought"].to_dict()))
    ok(min(edge(gold[n]) for n in graded) >= 2.0, "SF7 every graded count sits 2 or more from a rounding edge",
       " ".join("%.1f" % gold[n] for n in graded))
    for label, v in (("SF9 mean of the reporters' ratios", C.estimate(B, estimator="mean")),
                     ("SF9 median of the reporters' ratios", C.estimate(B, estimator="median")),
                     ("SF9 capture on the shortlisted reporters only",
                      C.estimate(B, reporters={n for n, _ in short} & B["reporter_nmls"])),
                     ("axis 8 capture year by year", C.estimate(B, per_year=True))):
        t, s = C.five(v)
        ok(names(t) == GOLD and s[0] == SIXTH and same_bins(v, gold, graded), "%s: same five, same bins" % label,
           " ".join("%.1f" % v[n] for n in graded))
    occ = lar[(lar.county_code.isin(C.FIPS.values())) & (lar.action_taken == "1") & (lar.loan_purpose == "1") &
              (lar.lien_status == "1") & (lar.occupancy_type == "1")].groupby("lei").size()
    v_occ = dict(gold)
    for n, nm in short:
        lei = B["lei_of"].get(n, "")
        if lei in occ.index:
            v_occ[nm] = float(occ[lei])
    t, _ = C.five(v_occ)
    ok(set(names(t)) == set(GOLD), "SF3 owner-occupants only for the reporters: same five (7.3 counts every buyer)")
    ok(set(B["F"][B["F"].MORTGAGEE_NAME.str.contains("NOMINEE")].nmls) <= set(B["register"].nmls_id),
       "SF5 every MERS nominee row resolves to its lender, never to MERS")

    # ------------------------------------------------------------------------------------------------ asks ----
    two_g = C.market_two_year(B)
    py_g = C.program_year(B)
    A, PYf = C.ask_figures(two_g, py_g)
    ok(min(edge(v) for v in A.values()) >= 2.0, "Ask B every figure 2 or more from a rounding edge",
       " ".join("%.1f" % v for v in A.values()))
    ok(min(edge(v) for v in PYf.values()) >= 2.0, "Ask A every figure 2 or more from a rounding edge",
       " ".join("%.1f" % v for v in PYf.values()))
    A_alt, _ = C.ask_figures(C.market_two_year(B, reporters="route"), py_g)
    ok(same_bins(A, A_alt, A), "Ask B the reporters at their route's capture: same bins")
    A_un, _ = C.ask_figures(C.market_two_year(B, keep=lambda F: F.file != C.FEEDS[2]), py_g)
    ok(same_bins(A, A_un, A), "Ask B the 2026 delivery unread: same bins")
    _, P_own = C.ask_figures(two_g, C.program_year(B, own_capture=True))
    ok(same_bins(PYf, P_own, PYf), "Ask A the reporters at their own capture: same bins")
    A_cr, _ = C.ask_figures(C.market_two_year(B, hmda_county=True, dedupe=False), py_g)
    ok(all(C.r10(A_cr[k]) != C.r10(A[k]) for k in A), "Ask B cracker (HMDA county codes, farmsteads twice) misses "
       "every figure", " ".join("%.0f/%.0f" % (A_cr[k], A[k]) for k in A))
    A_h, _ = C.ask_figures(C.market_two_year(B, hmda_county=True), py_g)
    miss_h = [k for k in A if C.r10(A_h[k]) != C.r10(A[k])]
    ok(len(miss_h) >= 4, "Ask B device D9 alone (HMDA county codes) misses four or more figures", ", ".join(miss_h))
    A_d, _ = C.ask_figures(C.market_two_year(B, dedupe=False), py_g)
    miss_d = [k for k in A if C.r10(A_d[k]) != C.r10(A[k])]
    ok(len(miss_d) >= 1, "Ask B device D6 alone (farmsteads twice) misses a figure", ", ".join(miss_d))
    _, P_cr = C.ask_figures(two_g, C.program_year(B, per_record=False))
    ok(all(C.r10(P_cr[k]) != C.r10(PYf[k]) for k in PYf), "Ask A cracker (each lender's 2024-25 route carried "
       "into 2026) misses every figure", " ".join("%.0f/%.0f" % (P_cr[k], PYf[k]) for k in PYf))
    A_s, _ = C.ask_figures(C.market_two_year(B, sellers=True), py_g)
    ok(any(C.r10(A_s[k]) != C.r10(A[k]) for k in A), "Ask B seller-carried notes counted (7.2) moves a figure")
    _, P_rd = C.ask_figures(two_g, C.program_year(B, datecol="MTG_REC_DATE"))
    ok(any(C.r10(P_rd[k]) != C.r10(PYf[k]) for k in PYf), "SF10 Ask A the recording date for the closing moves a figure")
    ok(C.estimate(B) == gold, "SF10 the main call never reads the program year")
    ok(abs(sum(two_g.values()) - sum(gold.values())) > 0 and sum(two_g.values()) > sum(gold.values()),
       "Ask B the eight counties hold more than the twelve shortlisted lenders made")

    # ----------------------------------------------------------------------------------- the deliverables ----
    fig = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures.json")))
    ok(fig["five"] == [G.SHORT[n] for n in GOLD] and fig["sixth"] == G.SHORT[SIXTH], "figures.json: the call")
    ok(all(fig["five_counts"][G.SHORT[n]] == G.fmt(C.r10(gold[n])) for n in GOLD), "figures.json: the five counts")
    wbg = openpyxl.load_workbook(os.path.join(golden, G.XLSX), data_only=True)
    ws = wbg["Recruitment order"]
    rows = [(ws.cell(r, 2).value, ws.cell(r, 3).value, ws.cell(r, 4).value) for r in range(5, 17)]
    ok([r[0] for r in rows[:5]] == GOLD and all(r[2] == "Yes" for r in rows[:5]) and rows[5][0] == SIXTH,
       "xlsx: the five in order, marked, and the sixth")
    ok(all(r[1] == C.r10(gold[r[0]]) for r in rows), "xlsx: every shortlisted lender's count is the golden's")
    wc = wbg["County volumes"]
    labels = [G.COUNTY_LABEL[k] for k in G.COUNTY_ROWS]
    for i, k in enumerate(G.COUNTY_ROWS):
        ok(wc.cell(4 + i, 1).value == labels[i] and wc.cell(4 + i, 2).value == C.r10(A[k]) and
           wc.cell(4 + i, 3).value == C.r10(PYf[k]), "xlsx: %s figures" % labels[i],
           "%s, %s" % (wc.cell(4 + i, 2).value, wc.cell(4 + i, 3).value))
    ok(wc.cell(9, 3).value == C.r10(PYf["total"]), "xlsx: the program year's total", str(wc.cell(9, 3).value))
    from pptx import Presentation
    prs = Presentation(os.path.join(golden, G.PPTX))
    ch = [s for s in prs.slides[0].shapes if s.has_chart][0].chart
    cats = list(ch.plots[0].categories)
    v = list(ch.plots[0].series[0].values)
    ok(len(cats) == 12 and dict(zip(cats, v)) == {G.SHORT[n]: C.r10(x) for n, x in gold.items()},
       "pptx: the twelve lenders' counts charted as in the workbook")
    title = prs.slides[0].shapes[0].text_frame.text
    ok(all(G.SHORT[n] in title for n in GOLD), "pptx: the title names the five")

    # ------------------------------------------------------------------------------------ realism sweep ----
    fw = F[F.mortgage & F.MTG_INSTR_DATE.between(*C.WIN)]
    mc = fw.assign(m=fw.MTG_INSTR_DATE.map(lambda d: (d.year, d.month))).groupby(["county", "m"]).size()
    ok(mc.groupby(level=0).nunique().min() >= 3 and mc.groupby(level=1).nunique().min() >= 4,
       "realism: no county's months and no month's counties repeat one count",
       "%d, %d" % (mc.groupby(level=0).nunique().min(), mc.groupby(level=1).nunique().min()))
    ok(F.REC_KEY.is_unique and F.groupby("CNTY_NAME").MTG_DOC_NO.apply(lambda s: s.is_unique).all(),
       "realism: record keys and each county's document numbers are unique")
    ok((F.LOAD_DATE.map(C._date) >= F.MTG_REC_DATE).all() and (F.MTG_REC_DATE >= F.DEED_REC_DATE).all() and
       (F.MTG_INSTR_DATE <= F.DEED_REC_DATE).all(), "realism: closing, deed, mortgage and load dates run in order")
    ok(F.MTG_REC_DATE.max() <= W.FEED_LAST and F.MTG_REC_DATE.min() >= W.FEED_FIRST,
       "realism: the deliveries cover January 2024 to August 2026 recordings")
    ok(all(int(r) % 10 for r in feed_rows.values()), "realism: no delivery has a round row count",
       str(list(feed_rows.values())))
    ok(pd.to_datetime(man.received_or_pulled).max() <= pd.Timestamp(W.PULL), "realism: nothing dated after the pull")
    pers = re.compile(rb"<dc:creator>([^<]*)</dc:creator>|<cp:lastModifiedBy>([^<]*)</cp:lastModifiedBy>")
    who = set()
    for folder in (target, golden):
        for f in os.listdir(folder):
            if f.endswith((".xlsx", ".pptx", ".docx")):
                with zipfile.ZipFile(os.path.join(folder, f)) as z:
                    for nm in z.namelist():
                        if nm.endswith("core.xml"):
                            for m in pers.finditer(z.read(nm)):
                                who |= {x.decode() for x in m.groups() if x}
    ok(who <= set(W.PEOPLE.values()), "realism: office files carry only the fund's people", ", ".join(sorted(who)))
    tells = (b"openpyxl", b"python-pptx", b"ReportLab", b"reportlab", b"XlsxWriter", b"xlsxwriter")

    def bytes_of(folder, f):
        p = os.path.join(folder, f)
        if f.endswith((".xlsx", ".pptx")):
            out = b""
            with zipfile.ZipFile(p) as z:
                for nm in z.namelist():
                    d = z.read(nm)
                    if nm.endswith(".xlsx"):
                        with zipfile.ZipFile(__import__("io").BytesIO(d)) as e:
                            d = b"".join(e.read(x) for x in e.namelist())
                    out += d
            return out
        return open(p, "rb").read()
    clean = [f for f in files if f.endswith((".xlsx", ".pdf"))]
    ok(not any(t in bytes_of(target, f) for f in clean for t in tells), "H1 no writer's name in the pack's containers")
    ok(not any(t in bytes_of(golden, f) for f in os.listdir(golden) for t in tells),
       "H1 no writer's name in the goldens, embedded chart data included")
    em = []
    for folder in (target, golden):
        for f in os.listdir(folder):
            if f.endswith((".csv", ".txt")) and "\u2014" in open(os.path.join(folder, f), encoding="utf-8").read():
                em.append(f)
    ok(not em and "\u2014" not in doc_text, "standing rule: no em dash in the pack", ", ".join(em))

    # ------------------------------------------------------------------------------ distractor deletion ----
    tmp = tempfile.mkdtemp()
    try:
        for d in dis:
            sub = os.path.join(tmp, d.replace(".", "_"))
            os.makedirs(sub)
            for f in files:
                if f != d:
                    os.link(os.path.join(target, f), os.path.join(sub, f))
            Bd = C.load(sub)
            vd = C.estimate(Bd)
            Ad, Pd = C.ask_figures(C.market_two_year(Bd), C.program_year(Bd))
            ok(vd == gold and Ad == A and Pd == PYf, "distractor: deleting %s moves nothing" % d)
    finally:
        shutil.rmtree(tmp)
    print("task448 checks: %d passed" % N_PASS[0])
    return N_PASS[0]
