"""task448 assertions: the input gates, the three rules (R1 to R3c), the ladder with every rung computed from the
pack, the separation and the grid, the semantic fork rows SF1 to SF15 and the estimator family inside every graded
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


def rk(k, x):
    """the prompt's rounding: the program year's eight-county total to the nearest 100, every other count to 10"""
    return C.r100(x) if k == "total" else C.r10(x)


def edge_k(k, x):
    return (50.0 - abs(x - C.r100(x))) if k == "total" else edge(x)


def same_bins(a, b, keys):
    return all(rk(k, a[k]) == rk(k, b[k]) for k in keys)


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
    ok(min(edge_k(k, v) for k, v in PYf.items()) >= 2.0, "Ask A every figure 2 or more from a rounding edge",
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
    ok(all(rk(k, P_cr[k]) != rk(k, PYf[k]) for k in PYf), "Ask A cracker (each lender's 2024-25 route carried "
       "into 2026) misses every figure", " ".join("%.0f/%.0f" % (P_cr[k], PYf[k]) for k in PYf))
    A_s, _ = C.ask_figures(C.market_two_year(B, sellers=True), py_g)
    ok(any(C.r10(A_s[k]) != C.r10(A[k]) for k in A), "Ask B seller-carried notes counted (7.2) moves a figure")
    _, P_rd = C.ask_figures(two_g, C.program_year(B, datecol="MTG_REC_DATE"))
    ok(any(rk(k, P_rd[k]) != rk(k, PYf[k]) for k in PYf), "SF10 Ask A the recording date for the closing moves a figure")
    ok(C.estimate(B) == gold, "SF10 the main call never reads the program year")
    wbd = openpyxl.load_workbook(os.path.join(target, DC.DICTIONARY), read_only=True)
    dict_rows = {(r[0], r[1]): r[2] for r in wbd["Fields"].iter_rows(min_row=2, values_only=True)}
    ok("geocoding" in dict_rows[(P.FILES["lar"], "county_code")],
       "Ask B pin: the dictionary files HMDA's county as the institution's geocode of the address")
    ok("the county in which the property lies" in doc_text,
       "Ask B pin: the vendor's guide files the recording county as where the property lies")
    flat = re.sub(r"\s+", " ", doc_text)
    ok("a home is in the county where it stands, which is the county in which the property is recorded" in flat,
       "SF12 pin: guidelines 2.2 place a home in the county in which the property is recorded")
    A_hy, _ = C.ask_figures(C.market_two_year(B, reporters="hybrid"), py_g)
    ok(same_bins(A, A_hy, A), "SF12 the reporters' recorded mortgages where recorded, HMDA's codes for the rest: "
       "same bins", " ".join("%.1f" % A_hy[k] for k in A))
    ok("does not hold every purchase-money mortgage recorded in a county" in flat,
       "SF11 pin: the vendor's guide files that the file does not hold every purchase-money mortgage recorded")
    feed_all_rows = C.counts(B, lambda F: F.mortgage)
    direct = {nm: float(feed_all_rows.get(n, 0)) for n, nm in short}
    t11, s11 = C.five(direct)
    ok(set(names(t11)) != set(GOLD) and C.r10(direct["Corvane Home Loans, LLC"]) != C.r10(gold["Corvane Home Loans, LLC"]),
       "SF11 every lender at its file rows (the file read as complete) files a wrong five and Corvane a bin low",
       " | ".join("%s %.0f" % (n.split()[0], x) for n, x in t11))
    r4w = C.estimate(B, sel=lambda F: F.mortgage | F.qcd)
    hn = [n for n, nm in short if nm == "Heidebrecht State Bank"][0]
    own = float(C.counts(B, lambda F: F.mortgage | F.qcd).get(hn, 0)) / caps[route(hn)]
    ok(C.r10(r4w["Heidebrecht State Bank"]) == 200 and C.r10(own) == 210,
       "write-up: the quitclaim clause's 200 counts the refinances for every lender, captures included",
       "every lender %.1f, its own rows alone %.1f" % (r4w["Heidebrecht State Bank"], own))
    pk11 = C.route_of(B)
    r_by = {"P": [], "S": []}
    for n in B["reporter_nmls"]:
        h = float(B["hmda"].get(B["lei_of"][n], 0))
        if h >= 20:
            r_by["P" if pk11.get(n, 1.0) >= 0.5 else "S"].append(float(feed_all_rows.get(n, 0)) / h)
    ok(min(r_by["P"]) >= 0.9 and max(r_by["S"]) <= 0.65 and len(r_by["S"]) >= 4,
       "SF11 the reporters' shortfall follows how each records, not where it lends (HMDA's codes no excess)",
       "with the deed %.3f to %.3f, after it %.3f to %.3f" % (min(r_by["P"]), max(r_by["P"]), min(r_by["S"]),
                                                              max(r_by["S"])))
    sf4 = {}
    feed_all = C.counts(B, lambda F: F.mortgage)
    for n, nm in short:
        sf4[nm] = float(feed_all.get(n, 0)) / caps[route(n)]
    t4, s4 = C.five(sf4)
    ok(names(t4) == GOLD and s4[0] == SIXTH and same_bins(sf4, gold, graded),
       "SF4 the reporters counted from the recorder by route as well: same five, same bins",
       " ".join("%.1f" % sf4[n] for n in graded))
    ok(abs(sum(two_g.values()) - sum(gold.values())) > 0 and sum(two_g.values()) > sum(gold.values()),
       "Ask B the eight counties hold more than the twelve shortlisted lenders made")
    ok("every mortgage a lender makes is counted, including any that no report or data file shows" in flat,
       "SF13 pin: guidelines 7.5 count every mortgage a lender makes, including any no report or data file shows")
    ok(set(names(t11)) != set(GOLD) and t11[4][0] == SIXTH,
       "SF13 the twelve ranked on the file's rows as one instrument (no lender completed) file a wrong five",
       " | ".join("%s %.0f" % (n.split()[0], x) for n, x in t11))
    pool = C.lender_counts(B, "pooled")
    tp, sp = C.five(pool)
    ok(set(names(tp)) == expect["R1"] and C.r10(pool["Mennwell Credit Union"]) < C.r10(pool[SIXTH]),
       "SF13 with every lender completed at the pooled capture (7.5 executed) the five stay wrong: the stump holds",
       "Mennwell %.1f, Shunga Valley %.1f" % (pool["Mennwell Credit Union"], pool[SIXTH]))
    A_cr2, _ = C.ask_figures(C.market_two_year_alloc(B, "county_route"), py_g)
    ok(same_bins(A, A_cr2, A), "SF14 the completed lenders at a capture measured within each county and route: "
       "same bins", " ".join("%.1f" % A_cr2[k] for k in A))
    A_ch, _ = C.ask_figures(C.market_two_year_alloc(B, "county_route_hmda"), py_g)
    ok(any(C.r10(A_ch[k]) != C.r10(A[k]) for k in A), "SF14 the county capture on HMDA's codes (not the recorded "
       "county, 2.2) moves a figure", " ".join("%.1f" % A_ch[k] for k in A))
    hc_num, hc_den = {}, {}
    dwin = B["F"][B["F"].mortgage & B["F"].MTG_INSTR_DATE.between(*C.WIN)]
    for n in B["reporter_nmls"]:
        byc = dwin[dwin.nmls == n].groupby("county").size()
        for k in C.REGION:
            hc_num[(route(n), k)] = hc_num.get((route(n), k), 0) + int(byc.get(k, 0))
            hc_den[(route(n), k)] = hc_den.get((route(n), k), 0) + int(B["hmda_county"].get((B["lei_of"][n], k), 0))
    over = [k for k in hc_num if hc_den[k] and hc_num[k] / hc_den[k] > 1.0]
    ok(len(over) >= 3, "SF14 on HMDA's codes the file holds more of a county's loans than HMDA places there",
       ", ".join("%s %s" % k for k in sorted(over)))
    A_rf, _ = C.ask_figures(C.market_two_year_alloc(B, "round_first"), py_g)
    ok(any(C.r10(A_rf[k]) != C.r10(A[k]) for k in A), "SF14 each lender's count rounded before it is spread (not "
       "each figure from its own unrounded figure) moves a figure", " ".join("%.1f" % A_rf[k] for k in A))
    _, P_hh = C.ask_figures(two_g, C.program_year(B, hmda_half=True))
    ok(same_bins(PYf, P_hh, PYf), "SF15 the reporters' July to December 2025 from their 2025 HMDA counts: same bins",
       " ".join("%.1f" % P_hh[k] for k in PYf))
    dm = B["F"][B["F"].mortgage]
    inh = {n for n in set(dm.nmls) if n and route(n) == "S"}
    late = dm[dm.MTG_INSTR_DATE.between(W.SWITCH, C.PY[1]) & dm.nmls.isin(inh)]
    early = dm[dm.MTG_INSTR_DATE.between(dt.date(2026, 1, 1), W.SWITCH - dt.timedelta(days=1)) & dm.nmls.isin(inh)]
    ok(len(late) > 100 and late.packaged.all() and len(early) > 0 and not early.packaged.any(),
       "SF15 the in-house lenders' mortgages closing from 6 April 2026 are all recorded with the deed, none before",
       "%d from the switch, %d before it" % (len(late), len(early)))
    prior = dm[dm.MTG_INSTR_DATE.between(dt.date(2025, 4, 6), dt.date(2025, 6, 30))]
    lift_i = len(late) / (prior.nmls.isin(inh)).sum()
    now_t = dm[dm.MTG_INSTR_DATE.between(W.SWITCH, C.PY[1]) & ~dm.nmls.isin(inh) & (dm.nmls != "")]
    lift_t = len(now_t) / (~prior.nmls.isin(inh)).sum()
    e25 = dm[dm.MTG_INSTR_DATE.between(dt.date(2025, 1, 1), dt.date(2025, 4, 5))]
    e26 = dm[dm.MTG_INSTR_DATE.between(dt.date(2026, 1, 1), dt.date(2026, 4, 5))]
    pre_i = e26.nmls.isin(inh).sum() / e25.nmls.isin(inh).sum()
    pre_t = (~e26.nmls.isin(inh) & (e26.nmls != "")).sum() / (~e25.nmls.isin(inh) & (e25.nmls != "")).sum()
    ok(lift_i > 1.8 and lift_t < 1.0 and abs(pre_i - pre_t) < 0.15, "SF15 the switched lenders' file rows jump with "
       "the recording while the others' do not, both groups level before it",
       "from 6 April %.2f against %.2f; before %.2f against %.2f" % (lift_i, lift_t, pre_i, pre_t))
    fam = C.capture_family(B)
    rt16 = C.route_of(B)
    r16 = lambda n: "P" if rt16.get(n, 1.0) >= 0.5 else "S"
    for k in ("mean", "mean20", "median", "low_after", "seconds_kept"):
        cp = fam[k]
        sel16 = (lambda F: F.mortgage | F.second) if k == "seconds_kept" else (lambda F: F.mortgage)
        f16 = C.counts(B, sel16)
        v16 = {nm: float(B["hmda"][B["lei_of"][n]]) if B["lei_of"].get(n, "") in B["hmda"].index
               else float(f16.get(n, 0)) / cp[r16(n)] for n, nm in short}
        t16, s16 = C.five(v16)
        ok(names(t16) == GOLD and s16[0] == SIXTH and same_bins(v16, gold, list(gold)),
           "SF16 capture by %s: the five, the sixth and all twelve counts in the golden's bins" % k,
           "P %.4f S %.4f" % (cp["P"], cp["S"]))
        A16, P16 = C.ask_figures(C.market_two_year(B, caps=cp),
                                 C.program_year(B, caps=cp, sel=sel16 if k == "seconds_kept" else None))
        ok(same_bins(A, A16, A), "SF16 capture by %s: Ask B in the golden's bins" % k,
           " ".join("%.1f" % A16[x] for x in A))
        keys16 = ["total"] if k == "median" else list(PYf)
        ok(same_bins(PYf, P16, keys16), "SF16 capture by %s: Ask A %s in the golden's bins" % (
            k, "total" if k == "median" else "rows and total"), " ".join("%.1f" % P16[x] for x in PYf))
    _, P16h = C.ask_figures(two_g, C.program_year(B, caps=fam["high_after"]))
    ok(same_bins(PYf, P16h, PYf), "SF16 the highest single after-deed ratio as a bound: Ask A in the golden's bins",
       " ".join("%.1f" % P16h[x] for x in PYf))
    gaps = 1731 - 1673
    ok(fam["median"]["P"] == 1.0 and caps["P"] < 0.97,
       "SF16 the median ratio of the with-the-deed group is 1.000 while the file misses %d of its loans" % gaps)
    first = lambda x: x.split()[0] if x else ""
    arm = B["F"][~B["F"].qcd & (B["F"].nmls != "")]
    ok(not (arm.GRANTOR_NAME.map(first) == arm.GRANTEE_NAME.map(first)).any(),
       "SF17 no lender's arm's-length sale is between parties sharing a surname (7.4's relative never arises)")

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
    ok(wc.cell(9, 3).value == C.r100(PYf["total"]), "xlsx: the program year's total, nearest 100", str(wc.cell(9, 3).value))
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
