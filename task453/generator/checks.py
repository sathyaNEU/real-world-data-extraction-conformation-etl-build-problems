"""Assertions on the built pack, the goldens and the simulation behind them. Run by build.py after every build."""
import collections
import csv
import json
import os
import re
import sys
import zipfile

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import calc as C        # noqa: E402
import methods as M     # noqa: E402
import sim as S         # noqa: E402
import world as W       # noqa: E402
from stl import stl     # noqa: E402

GOLD_SET = ["E01", "E03", "E09"]
DEFAULT_SET = ["E03", "E08", "E09", "E10"]
DEFAULT_ROUTES = ("stl", "stl_levels", "classical", "classical_additive", "stl13")
COMPONENTS = ("E01", "E03", "E09", "E08", "E10")
RESULTS = []


def ok(label, cond, detail=""):
    RESULTS.append((label, bool(cond), detail))


def margin(df, routes):
    return float((df[list(routes)] + 1.0).abs().min().min())


def sets_of(df, routes):
    return {r: C.designated(df, r) for r in routes}


def pdf_text(path):
    from pypdf import PdfReader
    return "\n".join(p.extract_text() for p in PdfReader(path).pages)


def clean_series(world):
    """the simulation's regional series before any file is written: whole jobs, revised, no layouts or codes"""
    rep = S.reported(world["R"])
    idx = [S.month_label(i) for i in range(S.N)]
    return pd.DataFrame({c: np.round(rep[c]) for c in W.RCODE}, index=idx)


def quarterly_route(s):
    """SF12: each region's quarterly averages, log on quarter effects, a trend with a knot a year and a level shift
    from the first quarter of 2026; the first quarter of 2027 adjusted against the 2026 average"""
    out = {}
    q = s.groupby([m[:4] + "Q" + str((int(m[5:7]) - 1) // 3 + 1) for m in s.index]).mean()
    n = len(q)
    t = np.arange(n)
    qi = np.array([int(k[-1]) for k in q.index])
    brk = list(q.index).index("2026Q1")
    Q = np.zeros((n, 4))
    Q[t, qi - 1] = 1
    X = np.column_stack([Q, t, (t >= brk).astype(float)] + [np.maximum(0, t - k) for k in range(4, n, 4)])
    for c in W.RCODE:
        lv = np.log(q[c].values)
        b, *_ = np.linalg.lstsq(X, lv, rcond=None)
        eff = b[:4] - b[:4].mean()
        sa_q1 = np.exp(lv[list(q.index).index("2027Q1")] - eff[0])
        avg26 = s[c][[m for m in s.index if m.startswith("2026")]].mean()
        out[c] = 100 * (sa_q1 / avg26 - 1)
    return out


def indirect_by_division(target):
    """SF11: each census division's series adjusted with the level-shift regression and summed to its region"""
    conc = C.concordance(target)
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(target, W.FILES["conc"]), read_only=True)
    cd = {str(r[0]): str(r[2]) for r in list(wb["Municipalities"].iter_rows(values_only=True))[1:] if r[0]}
    df = pd.concat([C.wide(target), C.long(target)], ignore_index=True)
    df["cd"] = df.muni.map(cd)
    s = df.groupby(["month", "cd"]).jobs.sum().unstack().sort_index()
    F = M.Frame(list(s.index))
    out = {}
    cds = {c: [d for d in W.CD_REGION if W.CD_REGION[d] == c] for c in W.RCODE}
    for c in W.RCODE:
        sa = np.zeros(F.n)
        y = np.zeros(F.n)
        for d in cds[c]:
            v = s[d].values.astype(float)
            sf, _ = M.regression(F, np.log(v))
            sa += np.exp(np.log(v) - sf)
            y += v
        out[c] = M.pct(F, sa, y)
    return out


def run(target, golden_dir, world=None, meta_path=None):
    RESULTS.clear()
    files = sorted(os.listdir(target))
    meta = json.load(open(meta_path)) if meta_path else {}

    # ------------------------------------------------------------------ input gates
    ok("gate: 10 or more files", len(files) >= 10, len(files))
    fmts = {f.rsplit(".", 1)[1] for f in files}
    ok("gate: 3 or more formats", len(fmts) >= 3, sorted(fmts))
    rows = {f: sum(1 for _ in open(os.path.join(target, f), encoding="utf-8")) - 1 for f in files if f.endswith(".csv")}
    ok("gate: a file of 25,000 rows or more", max(rows.values()) >= 25000, max(rows.items(), key=lambda kv: kv[1]))
    dis = meta.get("distractor_files", [])
    ok("gate: two or more distractors, shipped, none named as such", len(dis) >= 2 and all(d in files for d in dis)
       and not any("distract" in f.lower() for f in files), dis)
    ok("gate: the deliverables are not in the pack", not any(f in files for f in W.DELIVERABLES))

    # ------------------------------------------------------------------ the main call
    s = C.series(target)
    df = C.routes(s)
    fam = list(C.FAMILY)
    ok("call: every step-aware route designates the Capital, Brennick Valley and Pellmarsh Hills",
       all(v == GOLD_SET for v in sets_of(df, fam).values()), sets_of(df, fam))
    ok("call: step-aware routes keep every region 0.5 or more from the line", margin(df, fam) >= 0.5, round(margin(df, fam), 3))
    ok("call: the robust STL on the restated history agrees", C.designated(df, "ls_stl_robust") == GOLD_SET,
       C.designated(df, "ls_stl_robust"))
    ok("R3a analyst test: STL across the change designates Brennick Valley, Kestrow North, Varrenby Shore and Pellmarsh Hills",
       C.designated(df, "stl") == DEFAULT_SET, C.designated(df, "stl"))
    ok("R3a: every default route designates the same wrong four", all(v == DEFAULT_SET for v in sets_of(df, DEFAULT_ROUTES).values()),
       sets_of(df, DEFAULT_ROUTES))
    ok("R3a: default routes keep every region 0.3 or more from the line", margin(df, DEFAULT_ROUTES) >= 0.3,
       round(margin(df, DEFAULT_ROUTES), 3))
    ok("R3b decisive step alone: STL on the history restated by the level shift designates the golden",
       C.designated(df, "ls_stl") == GOLD_SET, C.designated(df, "ls_stl"))
    rob = C.designated(df, "stl_robust")
    ok("rung R1: robust STL across the change files another wrong set", rob not in (GOLD_SET, DEFAULT_SET) and rob == ["E01", "E09"], rob)
    yoy = C.designated(df, "yoy")
    rng_out = [c for c in ("E01", "E03", "E09") if not (math_floor1(df.loc[c, fam].min()) <= round(df.loc[c, "yoy"], 1)
                                                         <= math_ceil1(df.loc[c, fam].max()))]
    ok("rung R1b: the year-on-year route lands the set, its Capital, Brennick Valley and Pellmarsh Hills figures outside the ranges",
       yoy == GOLD_SET and rng_out == ["E01", "E03", "E09"], (yoy, rng_out))
    lab = [c for c in DEFAULT_SET if c not in ("E08", "E10")]
    ok("grid: dropping the two regions that gained most (labelling afterwards) still misses the Capital", "E01" not in lab and lab != GOLD_SET, lab)
    for c in ("E01", "E08", "E10"):
        side_g = {bool(df.loc[c, r] < -1) for r in fam}
        side_d = {bool(df.loc[c, r] < -1) for r in DEFAULT_ROUTES}
        ok("component %s: one side on every step-aware route, the other on every default route" % W.RNAME[c],
           len(side_g) == 1 and len(side_d) == 1 and side_g != side_d, (side_g, side_d))
    for c in ("E03", "E09"):
        lo, hi = math_floor1(df.loc[c, fam].min()), math_ceil1(df.loc[c, fam].max())
        outside = [r for r in DEFAULT_ROUTES if not (lo <= round(df.loc[c, r], 1) <= hi)]
        ok("component %s: below the line on every route, the default routes' figures outside the step-aware range" % W.RNAME[c],
           all(df.loc[c, r] < -1 for r in fam + list(DEFAULT_ROUTES)) and outside == list(DEFAULT_ROUTES), (lo, hi, outside))
    ok("dominance: the default moves Kestrow North, Varrenby Shore and the Capital across the line by the step's sign",
       df.loc["E08", "stl"] < df.loc["E08", "reg12"] - 1.0 and df.loc["E10", "stl"] < df.loc["E10", "reg12"] - 1.0
       and df.loc["E01", "stl"] > df.loc["E01", "reg12"] + 0.8,
       {c: round(df.loc[c, "stl"] - df.loc[c, "reg12"], 2) for c in ("E01", "E08", "E10")})
    ok("the steps: the Capital and Saltmere Coast down, every other region up, Kestrow North and Varrenby Shore the largest",
       df.loc["E01", "level_shift"] < -10 and df.loc["E02", "level_shift"] < 0
       and all(df.loc[c, "level_shift"] > 0 for c in W.RCODE[2:])
       and sorted(W.RCODE, key=lambda c: -df.loc[c, "level_shift"])[:2] == ["E08", "E10"],
       df.level_shift.round(1).to_dict())
    prov = s.sum(axis=1)
    jump = 100 * (prov["2026-01"] / prov["2025-12"] - 1)
    jump0 = np.mean([100 * (prov["%d-01" % y] / prov["%d-12" % (y - 1)] - 1) for y in (2022, 2023, 2024, 2025)])
    ok("oracle: the province's total shows no break at January 2026 (its December to January change as in other years)",
       abs(jump - jump0) < 0.6, (round(jump, 2), round(jump0, 2)))

    # ------------------------------------------------------------------ semantic forks, each asserted
    d1 = C.routes(C.series(target, drop_retired=True))
    ok("SF1: Wexleigh and Dorran dropped before 2025 leaves the call", C.designated(d1, "reg12") == GOLD_SET
       and d1.loc["E05", "reg12"] > -1, round(d1.loc["E05", "reg12"], 2))
    for f in (W.FILES["long"], W.FILES["rev"]):
        cols = open(os.path.join(target, f), encoding="utf-8").readline().strip().split(",")
        ok("SF2: one measure of jobs in %s" % f, [c for c in cols if "jobs" in c] == ["payroll_jobs"], cols)
    s_r = s.astype(float).copy()
    pre = [m for m in s.index if m < "2026-01"]
    s_r.loc[pre] = s_r.loc[pre] * 1.3
    ok("SF3: the compared months are all from 2026 (scaling the earlier history leaves the 2026 average)",
       np.allclose(s_r.loc[[m for m in s.index if m.startswith("2026")]].mean(), s.loc[[m for m in s.index if m.startswith("2026")]].mean()))
    reg = pdf_text(os.path.join(target, W.FILES["reg"]))
    regn = re.sub(r"\s+", " ", reg)
    ok("SF4: the quarter's payroll jobs are the average of its three months (regulation 1(2))",
       "average of its payroll jobs for the three months" in regn)
    sa_sa = {}
    for c in W.RCODE:
        F_ = M.Frame(list(s.index))
        y = s[c].values.astype(float)
        sf, _ = M.regression(F_, np.log(y))
        sa = np.exp(np.log(y) - sf)
        sa_sa[c] = 100 * (sa[F_.q1].mean() / sa[F_.y26].mean() - 1)
    ok("SF5: against the seasonally adjusted 2026 average the step-aware call is the same",
       [c for c in W.RCODE if sa_sa[c] < -1] == GOLD_SET, {c: round(v, 2) for c, v in sa_sa.items()})
    ok("SF6: no region within 0.5 of the line on any step-aware route, so at-or-below and rounded readings agree",
       margin(df, fam) >= 0.5 and all(C.designated(df.round(1), r) == GOLD_SET for r in fam))
    ok("SF7: eleven step-aware routes, one set", len(fam) == 11 and all(v == GOLD_SET for v in sets_of(df, fam).values()))
    dp = C.routes(C.series(target, revised=False))
    ok("SF8: the April file's preliminary months give the same call", all(C.designated(dp, r) == GOLD_SET for r in ("reg12", "ls_stl", "pre_classical")),
       dp.reg12.round(2).to_dict())
    ok("SF8: preliminary months keep every component on its side", all((dp.loc[c, "reg12"] < -1) == (c in GOLD_SET) for c in COMPONENTS))
    ok("SF9: the regulation defines the quarter", "three months beginning on 1 January" in regn)
    ok("SF10: the comparison is unrounded (regulation 2(2)), and rounding to one decimal gives the same set",
       "made on unrounded figures" in regn and C.designated(df.round(1), "reg12") == GOLD_SET)
    ind = indirect_by_division(target)
    ok("SF11: census divisions adjusted and summed give the same call", [c for c in W.RCODE if ind[c] < -1] == GOLD_SET,
       {c: round(v, 2) for c, v in ind.items()})
    qr = quarterly_route(s)
    ok("SF12: the quarterly series adjusted with quarter effects and a level shift gives the same call",
       [c for c in W.RCODE if qr[c] < -1] == GOLD_SET, {c: round(v, 2) for c, v in qr.items()})
    d24 = C.routes(C.series(target, from_2024=True))
    ok("closure 8: the seasonal pattern from 2024 on only (the monthly file alone) gives the same call",
       C.designated(d24, "reg12") == GOLD_SET and C.designated(d24, "ls_stl") == GOLD_SET)

    # ------------------------------------------------------------------ the three rules on the clean truth
    if world is not None:
        cs = clean_series(world)
        cd = C.routes(cs)
        ok("R3a on the clean truth: STL across the change files the wrong four", C.designated(cd, "stl") == DEFAULT_SET,
           C.designated(cd, "stl"))
        ok("R3a on the clean truth: the classical decomposition files the wrong four", C.designated(cd, "classical") == DEFAULT_SET)
        ok("R3b on the clean truth: the level shift removed files the golden", C.designated(cd, "reg12") == GOLD_SET
           and C.designated(cd, "ls_stl") == GOLD_SET)
        ok("clean-data test: the pack's series equal the clean truth (the mess is all in layout, codes and revisions)",
           (cs.values == s.values).all())
        R = world["R"]
        rep = S.reported(R)
        tru = {c: S.truth(R, rep, c) for c in W.RCODE}
        ok("truth: the simulation's own seasonal factors designate the golden", [c for c in W.RCODE if tru[c] < -1] == GOLD_SET,
           {c: round(v, 2) for c, v in tru.items()})
    ok("R1 raw material: the monthly municipality by sector statistics ship for every month from January 2021",
       len(s.index) == 75 and s.index[0] == "2021-01" and s.index[-1] == "2027-03")
    adj = []
    for f in files:
        if f.endswith(".csv"):
            head = open(os.path.join(target, f), encoding="utf-8").readline().lower()
            if "season" in head or "adjust" in head or "designat" in head or "factor" in head:
                adj.append(f)
    ok("R1: no shipped column holds an adjusted figure, a factor or a designation", not adj, adj)
    ok("R2 revisions: mishandled, the call holds", C.designated(dp, "reg12") == GOLD_SET)
    ok("R2 concordance: retired codes dropped, the call holds", C.designated(d1, "reg12") == GOLD_SET)
    ok("R2 layouts: the yearly tables left out, the call holds", C.designated(d24, "reg12") == GOLD_SET)
    wide = C.wide(target)
    g24 = wide[wide.month == "2023-12"].jobs.sum()
    lng = C.long(target)
    ok("R2 industry codes: the yearly tables' groups and the monthly file's sectors carry whole totals (December 2023 to January 2024 within 3 per cent)",
       abs(lng[lng.month == "2024-01"].jobs.sum() / g24 - 1) < 0.03, (int(g24), int(lng[lng.month == "2024-01"].jobs.sum())))
    calc_src = open(os.path.join(HERE, "calc.py"), encoding="utf-8").read()
    series_src = calc_src[calc_src.index("def series"):calc_src.index("def routes")]
    ok("R2 workplace returns: the call reads no workplace line (separation line)", "work" not in series_src and "lfs" not in series_src
       and "pop" not in series_src)

    # ------------------------------------------------------------------ the asks
    wp = C.workplaces(target)
    gl = C.jobs_lost(wp, "workplace")
    for k in ("account_number", "business_address", "legal_address"):
        o = C.jobs_lost(wp, k)
        dmin = int((o - gl).abs().min().min())
        ok("ask A: keyed on %s every figure misses by 15 or more" % k, dmin >= 15, dmin)
    edge = [(c, col, int(gl.loc[c, col])) for c in W.RCODE for col in ("none", "fewer") if int(gl.loc[c, col]) % 10 not in (8, 9, 0, 1, 2)]
    ok("ask A: every golden figure mid-bin (within 2 of its ten)", not edge, edge)
    emp = C.employers(wp, "business")
    for k in ("account", "legal_name", "operating_name"):
        o = C.employers(wp, k)
        ok("ask B: counted by %s every region misses" % k, ((o - emp).abs() >= 5).all(), (o - emp).to_dict())
    wp["bn"] = wp.payroll_account.str[:9]
    wp["addr"] = wp.municipality_code + "|" + wp.street_address
    by_addr = wp.groupby("addr").agg(bns=("bn", "nunique"), accts=("payroll_account", "nunique"))
    moved = wp[wp.addr.isin(by_addr.index[by_addr.bns > 1])]
    ok("ask A device: five workplaces a region changed hands (an address under two businesses across the months)",
       (moved.groupby("region").addr.nunique() == 5).all() and len(moved.addr.unique()) == 50,
       moved.groupby("region").addr.nunique().to_dict())
    one_month = wp.groupby(["addr", "reference_month"]).bn.nunique()
    ok("ask A device: no address carries two businesses in one month", (one_month == 1).all())
    ok("ask A device: a thousand or more addresses carry lines on two accounts", int((by_addr.accts > 1).sum()) >= 1000,
       int((by_addr.accts > 1).sum()))
    keys = wp.groupby(["reference_month", "payroll_account", "workplace_no"]).size()
    ok("hygiene: account, workplace number and month unique (the battery passes)", (keys == 1).all())
    ok("hygiene: no repeated row", not wp.duplicated().any())
    ok("hygiene: every municipal code joins the concordance", wp.region.notna().all())
    two = wp[(wp.reference_month == "2027-03") & (wp.payroll_jobs > 0)].groupby(["region", "bn"]).payroll_account.nunique()
    two = two[two > 1].groupby(level=0).size()
    ok("ask B device: 15 or more businesses a region pay from two accounts", (two.reindex(W.RCODE).fillna(0) >= 15).all(), two.to_dict())
    nil = wp[(wp.reference_month == "2027-03") & (wp.payroll_jobs == 0)]
    allb = wp[wp.reference_month == "2027-03"].groupby("region").bn.nunique()
    ok("hazard: nil lines listed (seasonal workplaces with no employees paid)", len(nil) > 100, len(nil))
    ok("hazard: counting nil lines' employers moves ask B in the seasonal regions", ((allb - emp).reindex(["E02", "E04", "E05", "E06", "E10"]) >= 10).all(),
       (allb - emp).to_dict())
    lines_m = {}
    for m in ("2026-03", "2027-03"):
        a = wp[wp.reference_month == m].groupby("region").payroll_jobs.sum()
        lines_m[m] = (a.reindex(W.RCODE) == s.loc[m].reindex(W.RCODE)).all()
    ok("oracle: the workplace returns' March totals tie to the revised statistics in both months", all(lines_m.values()), lines_m)

    # ------------------------------------------------------------------ distractors
    lfs = pd.read_csv(os.path.join(target, W.FILES["lfs"]))
    e26 = lfs[lfs.reference_month.str.startswith("2026")].groupby("economic_region_code").employment_thousands.mean()
    e27 = lfs[lfs.reference_month.isin(["2027-01", "2027-02", "2027-03"])].groupby("economic_region_code").employment_thousands.mean()
    lset = sorted(c for c in W.RCODE if 100 * (e27[c] / e26[c] - 1) < -1)
    ok("distractor: the labour force survey's reading designates neither the golden nor the default", lset not in (GOLD_SET, DEFAULT_SET), lset)
    ok("distractor: the call and the asks read neither distractor", "lfs" not in calc_src.replace("self", "") and W.FILES["pop"] not in calc_src)

    # ------------------------------------------------------------------ goldens
    gcsv = pd.read_csv(os.path.join(golden_dir, "regional_payroll_jobs_2027q1.csv"))
    ok("golden CSV: every region, in the Schedule's order", list(gcsv.economic_region_code) == W.RCODE)
    ok("golden CSV: ask A figures, nearest 10", all(gcsv.jobs_lost_workplaces_none_left_2027_03 == [int(round(gl.loc[c, "none"] / 10.0)) * 10 for c in W.RCODE])
       and all(gcsv.jobs_lost_workplaces_kept_some_2027_03 == [int(round(gl.loc[c, "fewer"] / 10.0)) * 10 for c in W.RCODE]))
    ok("golden CSV: ask B figures", all(gcsv.employers_with_payroll_jobs_2027_03 == [int(emp[c]) for c in W.RCODE]))
    gtxt = pdf_text(os.path.join(golden_dir, "rapid_response_certification_2027q1.pdf"))
    ok("golden PDF: names the three designated regions", all(W.RNAME[c] in gtxt for c in GOLD_SET) and "Capital" in gtxt)
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    ok("figures.json: the call", figs["call"] == [W.RNAME[c] for c in GOLD_SET])
    ok("figures.json: the default call", figs["default_call"] == [W.RNAME[c] for c in DEFAULT_SET])

    # ------------------------------------------------------------------ realism sweep
    vec = {tuple(s.loc[m].values) for m in s.index}
    ok("realism: no two months share every region's total", len(vec) == len(s.index))
    blocks = [tuple(s[c].values[k:k + 12]) for c in W.RCODE for k in range(0, len(s.index) - 12)]
    ok("realism: no twelve-month run repeats in any region", len(set(blocks)) == len(blocks))
    diffs = s.diff().iloc[1:]
    flat2 = [(m, c) for c in W.RCODE for k, m in enumerate(diffs.index[1:], 1) if diffs[c].iloc[k] == 0 and diffs[c].iloc[k - 1] == 0]
    ok("realism: no region flat three months running", not flat2, flat2)
    graded = [v for row in gcsv.itertuples() for v in (row.jobs_lost_workplaces_none_left_2027_03, row.jobs_lost_workplaces_kept_some_2027_03)]
    for code in GOLD_SET:
        r = figs["regions"][W.RNAME[code]]
        graded += [r["sa_jobs"], r["avg_2026"]]
    ok("realism: no graded jobs figure a multiple of 100", not [v for v in graded if v % 100 == 0], [v for v in graded if v % 100 == 0])
    same = [row.economic_region for row in gcsv.itertuples() if row.jobs_lost_workplaces_none_left_2027_03 == row.jobs_lost_workplaces_kept_some_2027_03]
    ok("realism: no region's two ask A figures equal", not same, same)
    note = pdf_text(os.path.join(target, W.FILES["note"]))
    ok("realism: the release note signed by the card's liaison", W.PEOPLE["liaison"][0] in note)
    people = {p for p, _ in W.PEOPLE.values()}
    trans = open(os.path.join(target, W.FILES["trans"]), encoding="utf-8").read()
    named = set(re.findall(r"(?:From|To): ([A-Z][a-z]+ [A-Z][a-z]+)", trans))
    ok("realism: every person named in the transmittal is on the card", named and named <= people, named)
    for f in files:
        if f.endswith(".xlsx"):
            z = zipfile.ZipFile(os.path.join(target, f))
            core = z.read("docProps/core.xml").decode()
            ok("container: %s carries no writer's name" % f, "openpyxl" not in core and "openpyxl" not in z.read("docProps/app.xml").decode())
        if f.endswith(".pdf"):
            b = open(os.path.join(target, f), "rb").read()
            ok("container: %s carries no library banner" % f, b"ReportLab" not in b and b"reportlab" not in b)
    mt = {os.path.getmtime(os.path.join(target, f)) for f in files}
    ok("timestamps: every file stamped at the assembly time", len(mt) == 1, mt)
    months = set(wp.reference_month)
    ok("timestamps: no record after the extract (March 2027 the latest month)", max(months) == "2027-03" and max(s.index) == "2027-03")
    em = [f for f in files if "\u2014" in open(os.path.join(target, f), "rb").read().decode("latin-1")]
    ok("house: no em dash in a text file", not [f for f in files if f.endswith((".csv", ".txt")) and "\u2014" in open(os.path.join(target, f), encoding="utf-8").read()])

    fails = [(l, d) for l, c, d in RESULTS if not c]
    for l, c, d in RESULTS:
        print("%s  %s%s" % ("PASS" if c else "FAIL", l, "" if c else "  (%s)" % (d,)))
    print("%d checks, %d failed" % (len(RESULTS), len(fails)))
    return not fails


def math_floor1(v):
    import math
    return math.floor(v * 10 + 1e-9) / 10.0


def math_ceil1(v):
    import math
    return math.ceil(v * 10 - 1e-9) / 10.0


if __name__ == "__main__":
    T = os.path.dirname(HERE)
    sys.exit(0 if run(os.path.join(T, "target"), os.path.join(T, "golden"), meta_path=os.path.join(T, "metadata.json")) else 1)
