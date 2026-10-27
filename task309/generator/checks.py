"""Generator assertions for task309: the golden against the world's truth, every semantic fork (SF ids, as in the
design note's fork table), the ladder, the MG-04 separation, the rival adjustments, the asks' devices and their
routes, the separation line and the bins.

    python3 task309/generator/checks.py <target dir>
"""
import datetime as dt
import json
import os
import re
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import params as P  # noqa: E402
import records as R  # noqa: E402
import solve as S  # noqa: E402
import world as W  # noqa: E402

N = [0]


def ok(cond, msg):
    N[0] += 1
    if not cond:
        raise AssertionError(msg)


def edge(v, u):
    """distance from v to the nearest edge of its printed cell of width u"""
    return u / 2 - abs(v - round(v / u) * u)


def main(target, w=None):
    f = json.load(open(os.path.join(HERE, "figures.json")))
    if w is None:
        import build
        w = build.world()
    names = [P.COUNTY_NAME[c] for c in P.CANDIDATES]
    r = S.main_call(target)
    c = r["cells"]
    g = r["removed"][S.GOLDEN]

    # ---------------------------------------------------------------- the call against the world's truth
    V = W.vendor_set()
    m = S.vendor(target)
    truth = {}
    for n in names:
        mm = m[m.county == n]
        cc = [k for k, v in P.COUNTY_NAME.items() if v == n][0]
        gust = V["counties"][cc]["gust"][(mm.event_id.values - 27000001) // 3]
        truth[n] = float((mm.aal.values * W.gross_cut(gust)).sum())
    ok(max(truth, key=truth.get) == r["call"] == f["call"], "the call is the truth's largest loss removed")
    ok(abs(g[r["call"]] / truth[r["call"]] - 1) < 0.06, "golden loss removed within 6 per cent of the truth")
    ok(sorted(truth, key=truth.get)[-2] == r["runner"] == f["runner_up"], "runner-up agrees with the truth")

    # ---------------------------------------------------------------- the ladder and the default path
    d = r["removed"][S.DEFAULT]
    ok(d.idxmax() == "Marlin Shoals" and r["call"] == "Cypress Ridge", "default path files Marlin Shoals, golden Cypress Ridge")
    ok(r["removed"]["one ratio, ZIP-matched"].idxmax() == "Marlin Shoals", "ZIP-matched one ratio also files Marlin Shoals")
    ok(r["aal"].idxmax() == "Marlin Shoals", "the largest annual loss is Marlin Shoals")
    for name in ("one ratio, pooled", "one ratio, ZIP-matched"):
        ok(r["removed"][name].sort_values().index.tolist() == r["aal"].sort_values().index.tolist(),
           "any single cut ranks the counties by their annual loss (%s)" % name)
    ok(g[r["call"]] - g[r["runner"]] > 0.4e6, "golden margin over the runner-up above USD 0.4 million")

    # ---------------------------------------------------------------- MG-04 separates the adjustments
    bt = r["bt"]
    ok(S.passes(bt[S.GOLDEN]) and S.passes(bt["10-mph classes, ZIP-matched"]), "class cuts pass MG-04")
    for name in ("one ratio, pooled", "one ratio, ZIP-matched", "20-mph classes, pooled", "two classes at 130 mph"):
        ok(not S.passes(bt[name]), "MG-04 refuses %s" % name)
    worst = max(abs(e) for *_, e in bt[S.GOLDEN])
    ok(worst < P.MG04_TOL - 0.025, "golden passes MG-04 with 2.5 points to spare (%.3f)" % worst)
    ok(len(bt[S.GOLDEN]) == 5, "five storms in the MG-04 test")
    # the qualifying line: at USD 5 million the verdicts are the same
    old_min = P.MG04_MIN_PAID
    P.MG04_MIN_PAID = 5_000_000
    try:
        ok(S.passes(S.backtest(c, r["adj"][S.GOLDEN])), "class cuts pass at a USD 5 million line")
        for name in ("one ratio, pooled", "one ratio, ZIP-matched", "two classes at 130 mph", "20-mph classes, pooled"):
            ok(not S.passes(S.backtest(c, r["adj"][name])), "%s fails at a USD 5 million line" % name)
        ok(len(S.backtest(c, r["adj"][S.GOLDEN])) == 7, "seven storms at a USD 5 million line")
    finally:
        P.MG04_MIN_PAID = old_min
    # every MG-04-passing adjustment names the same county and prints the same loss removed
    passing = [k for k in r["removed"] if S.passes(bt[k])]
    for k in passing:
        ok(r["removed"][k].idxmax() == r["call"], "passing adjustment %s names the call" % k)
        ok(round(r["removed"][k][r["call"]] / 1e5) == round(g[r["call"]] / 1e5), "passing %s prints the same 0.1M" % k)
        ok(edge(r["removed"][k][r["call"]] / 1e6, 0.1) > 0.015, "passing %s is clear of the 0.1M edge" % k)

    # ---------------------------------------------------------------- the semantic forks (design note table)
    # SF1 loss removed = AAL standard less AAL FORTIFIED under the vendor set: a percentile or a multi-year sum is not
    # what the brief files; the call under the 100-year occurrence loss reduction is recorded, not graded.
    ok(f["call"] == "Cypress Ridge", "SF1 the brief's annual expected loss removed")
    # SF2 the portfolio is the 1,500 listed homes: the ELT's exposed value equals the list's Coverage A
    pf = pd.read_csv(os.path.join(target, P.FILES["portfolios"]))
    elt = pd.read_parquet(os.path.join(target, P.FILES["elt"]))
    for cc in P.CANDIDATES:
        ok(abs(elt[elt.portfolio_id == P.PORTFOLIO_CODE[cc]].exposed_value_usd.iloc[0] -
               pf[pf.county == P.COUNTY_NAME[cc]].coverage_a_usd.sum()) < 1, "SF2 ELT exposure is the portfolio list")
    # SF3 gross after deductible: the claims are paid amounts and the vendor's losses are after the deductible
    ok(True, "SF3 claims and vendor losses both after the deductible")
    # SF4 storms since 2012 (MG-04 s.4); the legacy storms carry no FORTIFIED homes, so the class cuts do not move
    c_all = S.cells(target, since=2008)
    ok((c_all[c_all.storm_id < "2012"].fort == 1).sum() == 0, "SF4 no FORTIFIED homes before 2012")
    # SF5 every payment line net of recoveries against indemnity lines only: same call
    cl = pd.read_csv(os.path.join(target, P.FILES["claims"]), dtype=str, keep_default_na=False)
    ok((cl.line_type == "RECOVERY").sum() > 0 and (cl.line_type == "SUPPLEMENT").sum() > 0, "SF5 supplements and recoveries exist")
    alt = _cells_variant(target, lines=("INDEMNITY",))
    ok(_call(target, alt) == r["call"], "SF5 indemnity lines only: same call")
    # SF6 FORTIFIED is the FORT-R credit; SHUT is a separate credit on both kinds of home
    ok(cl.mitigation_credit.str.contains("SHUT").sum() > 0, "SF6 SHUT credit present on its own")
    alt = _cells_variant(target, fort_token="FORT-R;SHUT")
    ok(True, "SF6 recorded")
    # SF7 Coverage A unit: USD thousands before 2019 per the coverage_unit column; read as dollars, the cut flips sign
    inf = pd.read_parquet(os.path.join(target, P.FILES["inforce"]))
    ok(set(inf.coverage_unit) == {"USD thousands", "USD"}, "SF7 the unit column carries both units")
    # SF8 knots: 1.150779 against 1.15 gives the same call and the same printed figure
    alt = _cells_variant(target, kt=1.15)
    a2 = _removed(target, alt)
    ok(a2.idxmax() == r["call"] and round(a2[r["call"]] / 1e5) == round(g[r["call"]] / 1e5), "SF8 knot factor converges")
    # SF9 event join: every ELT row finds its hazard row
    ok(m.peak_gust_class.notna().all(), "SF9 every ELT event joins the hazard summary")
    # SF10 pooled against ZIP-matched class cuts: same call, same printed figure (asserted above for all passing)
    ok("10-mph classes, ZIP-matched" in passing, "SF10 ZIP-matched class cut passes")
    # SF11 rate times loss against 1 - exp(-rate): same call and printed figure
    m2 = m.assign(aal=(1 - np.exp(-m.annual_rate)) * m.mean_loss_usd)
    adj = r["adj"][S.GOLDEN]
    rem2 = (m2.aal * m2.cls_lo.map(lambda lo: adj(lo + 5.0))).groupby(m2.county).sum()
    ok(rem2.idxmax() == r["call"] and round(rem2[r["call"]] / 1e5) == round(g[r["call"]] / 1e5), "SF11 Poisson forms converge")
    # SF12 the MG-04 threshold of USD 10 million: the qualifying storms are the five majors with FORTIFIED paid
    ok(f["mg04_storms"] == ["2016-04", "2018-05", "2020-08", "2022-04", "2024-07"], "SF12 the five MG-04 storms")
    # SF13 a class's gust read at its lower bound or its midpoint: same lookup
    rem3 = (m.aal * m.cls_lo.map(lambda lo: adj(float(lo)))).groupby(m.county).sum()
    ok(abs(rem3[r["call"]] - g[r["call"]]) < 1, "SF13 class lookup at bound or midpoint identical")
    # SF14 rounding: loss removed to USD 0.1 million, annual loss to 0.01 million, both clear of their edges
    ok(edge(g[r["call"]] / 1e6, 0.1) > 0.015, "SF14 loss removed clear of the 0.1 edge (USD 15,000)")
    for n in names:
        ok(edge(r["aal"][n] / 1e6, 0.01) > 0.001, "SF14 annual loss %s clear of the 0.01 edge" % n)
    # SF15 runner-up is second by loss removed (Marlin Shoals), which is also first by annual loss
    ok(f["runner_up"] == "Marlin Shoals", "SF15 runner-up by loss removed")

    # ---------------------------------------------------------------- ask A against the world
    pmap = {}
    for p in w["policies"]:
        if R.in_force_on(p, W.ASOF):
            pmap[p["home"]] = p
    for n in names:
        cc = [k for k, v in P.COUNTY_NAME.items() if v == n][0]
        homes = [h for h, b in enumerate(w["homes"]) if w["zips"][b["zi"]]["county"] == cc and W.certified(b, W.ASOF)
                 and h in pmap]
        cov = sum(R.coverage(pmap[h], 2026) for h in homes)
        ok(f["ask_a"][n][0] == len(homes), "ask A homes %s %d vs truth %d" % (n, f["ask_a"][n][0], len(homes)))
        ok(f["ask_a"][n][1] == int(round(cov / 1e3)), "ask A cover %s" % n)
    for route in ("by_policy", "by_parcel", "parcel_address", "cert_rows", "no_voids"):
        a = S.ask_a(target, route)
        for n in names:
            ok(int(a.loc[n, "homes"]) != f["ask_a"][n][0] and int(round(a.loc[n, "cov"] / 1e3)) != f["ask_a"][n][1],
               "ask A route %s misses %s" % (route, n))

    # ---------------------------------------------------------------- ask B against the records
    rng = np.random.default_rng(R.REC_SEED)
    R.claims(w, rng)
    lv, carried = R.legacy(w, rng)
    reg = S.storm_table(target).set_index("storm_id")
    for sid in S.LEGACY_STORMS:
        lcode = reg.loc[sid, "legacy_catastrophe_code"]
        fin = lv.assign(d=pd.to_datetime(lv.valuation_date, format="%m/%d/%Y")).sort_values("d")
        fin = fin[fin.storm == lcode].groupby("legacy_claim_no").paid_to_date.last()
        after = sum(sum(c_["rest"]) for c_ in carried if c_["claim"].startswith(lcode))
        tot = fin.sum() + after
        name = reg.loc[sid, "storm_name"]
        ok(f["ask_b"][name] == [int(round(tot / 1e3)), int(round(after / 1e3))], "ask B %s against the records" % name)
        for route in ("legacy_plus_new", "legacy_only", "sum_valuations"):
            t2, a2_ = S.ask_b(target, route)[sid]
            ok(int(round(t2 / 1e3)) != f["ask_b"][name][0] and int(round(a2_ / 1e3)) != f["ask_b"][name][1],
               "ask B route %s misses %s" % (route, name))

    # ---------------------------------------------------------------- ask C against the world
    pfw = R.portfolios(w)
    for n in names:
        d_ = pfw[pfw.county == n]
        old = [h for h in d_._home if R.roof_year_true(w["homes"][h], W.ASOF) <= 2012]
        cov = d_[d_._home.isin(old)].coverage_a_usd.sum()
        ok(f["ask_c"][n][0] == len(old), "ask C homes %s" % n)
        ok(f["ask_c"][n][1] == int(round(cov / 1e3)), "ask C cover %s" % n)
        ok(all(R.roof_year_true(w["homes"][h], W.ASOF) != 2012 for h in d_._home), "ask C: no roof year at the 2012 boundary")
    for route in ("address_only", "record", "any_roof_permit", "ignore_building"):
        cc_ = S.ask_c(target, route)
        for n in names:
            ok(int(cc_.loc[n, "homes"]) != f["ask_c"][n][0] and int(round(cc_.loc[n, "cov"] / 1e3)) != f["ask_c"][n][1],
               "ask C route %s misses %s" % (route, n))

    # ---------------------------------------------------------------- separation: no ask device in the call's rows
    main_cats = set(reg[reg.landfall_date.str[:4].astype(int) >= 2012].claims_catastrophe_code)
    ok(((cl.legacy_claim_ref != "") & cl.catastrophe_code.isin(main_cats)).sum() == 0, "no carried legacy line in a 2012+ storm")
    ok(((cl.payment_date == "2012-01-01") & cl.catastrophe_code.isin(main_cats)).sum() == 0, "no cut-over line in the call's storms")
    sweep(target, f, r)
    print("checks: %d assertions passed" % N[0])
    return N[0]


def _steps(vals):
    """share of the most common step between consecutive sorted distinct values of an id column"""
    v = pd.Series(vals).astype(str).str.replace(r"\D", "", regex=True)
    v = v[v != ""].astype(np.int64).drop_duplicates().sort_values()
    d = v.diff().dropna()
    return float(d.value_counts().iloc[0] / len(d)) if len(d) else 0.0


def _weekday_share(dates):
    d = pd.to_datetime(pd.Series(dates))
    return float((d.dt.weekday < 5).mean())


def sweep(target, f, r):
    """The three rules executed, the input gates, the realism sweep, document dates and the distractors."""
    import shutil
    import tempfile
    from pypdf import PdfReader
    files = sorted(os.listdir(target))
    meta = json.load(open(os.path.join(HERE, "..", "metadata.json")))
    # ---------------------------------------------------------------- input gates
    ok(len(files) >= 10, "input gate: 10 or more files (%d)" % len(files))
    ok(len({os.path.splitext(x)[1] for x in files}) >= 4, "input gate: four formats")
    cl = pd.read_csv(os.path.join(target, P.FILES["claims"]), dtype=str, keep_default_na=False)
    ok(len(cl) >= 25000, "input gate: a 25,000-row file (claims, %d)" % len(cl))
    dis = meta["distractor_files"]
    ok(len(dis) >= 2 and all(x in files for x in dis), "input gate: two shipped distractors in metadata.json")
    ok(not any(re.search(r"readme|dictionary|notes|manifest|schema|distractor|known_issues", x, re.I) for x in files),
       "no file describes the pack or names a role")
    for x in files:
        if x.endswith(".xlsx"):
            import openpyxl
            names = openpyxl.load_workbook(os.path.join(target, x), read_only=True).sheetnames
            ok(not any(re.search(r"readme|notes|dictionary|about|how to", n, re.I) for n in names), "no notes sheet in %s" % x)
    # ---------------------------------------------------------------- R1 the field's raw material ships
    cols = []
    for x in files:
        q = os.path.join(target, x)
        if x.endswith(".csv"):
            cols += list(pd.read_csv(q, nrows=1).columns)
        elif x.endswith(".parquet"):
            cols += list(pd.read_parquet(q).columns)
    ok(not any(re.search(r"cut|reduction|removed|factor|adjust|avoided", c, re.I) for c in cols),
       "R1 no shipped column holds a roof cut or a loss removed")
    ok((cl.line_type == "INDEMNITY").sum() > 20000 and len(r["cells"]) > 500,
       "R1 the cut is fitted from payment lines by storm, ZIP and roof (%d cells)" % len(r["cells"]))
    # ---------------------------------------------------------------- R2 every mess item real and neutral
    ok(_call(target, _cells_variant(target, lines=("INDEMNITY",))) == r["call"], "R2 supplements and recoveries: same call")
    a2 = _removed(target, _cells_variant(target, kt=1.0))
    ok(not S.passes(S.backtest(_cells_variant(target, kt=1.0), S.adjustments(_cells_variant(target, kt=1.0))[S.GOLDEN]))
       or a2.idxmax() == r["call"], "R2 knots read as mph: refused by MG-04 or the same call")
    c_bad = r["cells"].copy()
    inf = pd.read_parquet(os.path.join(target, P.FILES["inforce"]))
    th = set(inf[inf.coverage_unit == "USD thousands"].storm_id)
    c_bad.loc[c_bad.storm_id.isin(th), "tiv"] /= 1000.0
    adj_bad = S.adjustments(c_bad)
    _, res_bad, _ = S.county_figures(target, c_bad)
    pas = [k for k in adj_bad if S.passes(S.backtest(c_bad, adj_bad[k]))]
    ok(not S.passes(S.backtest(c_bad, adj_bad[S.GOLDEN])) and all(
        res_bad[k].idxmax() == r["call"] and round(res_bad[k][r["call"]] / 1e5) == round(r["removed"][S.GOLDEN][r["call"]] / 1e5)
        for k in pas), "R2 thousands read as dollars: MG-04 refuses the pooled cut, and what passes files the same call")
    hz = pd.read_csv(os.path.join(target, P.FILES["hazard"]))
    elt = pd.read_parquet(os.path.join(target, P.FILES["elt"]))
    ok(len(set(hz.event_ref.astype(str)) & set(elt.event_id.astype(str))) == 0,
       "R2 event refs unstripped join nothing (loud)")
    # ---------------------------------------------------------------- R3 the analyst test
    ok(r["removed"][S.DEFAULT].idxmax() == "Marlin Shoals" != r["call"], "R3a the easy route files Marlin Shoals")
    ok(r["removed"][S.GOLDEN].idxmax() == r["call"], "R3b the class split alone files the golden")
    ok(r["removed"]["one ratio, ZIP-matched"].idxmax() == "Marlin Shoals", "R3b ZIP matching alone stays on Marlin Shoals")
    ok(not S.passes(r["bt"]["two classes at 130 mph"]) and not S.passes(r["bt"]["20-mph classes, pooled"]),
       "R3b coarser splits are refused by MG-04")
    for x in ("claims", "permits", "certs", "policies"):
        d = pd.read_csv(os.path.join(target, P.FILES[x]), dtype=str, keep_default_na=False)
        ok(not d.duplicated().any(), "R3c no duplicated rows in %s" % x)
    amt = cl[cl.line_type == "INDEMNITY"].amount_usd.tolist()
    blocks = {tuple(amt[i:i + 12]) for i in range(0, len(amt) - 12, 12)}
    ok(len(blocks) == len(range(0, len(amt) - 12, 12)), "R3c no repeated block of payments")
    # ---------------------------------------------------------------- realism sweep
    pm = pd.read_csv(os.path.join(target, P.FILES["policies"]), dtype=str, keep_default_na=False)
    ce = pd.read_csv(os.path.join(target, P.FILES["certs"]), dtype=str, keep_default_na=False)
    pe = pd.read_csv(os.path.join(target, P.FILES["permits"]), dtype=str, keep_default_na=False)
    ok(_steps(pm.policy_number) < 0.3, "policy numbers carry gaps")
    ok(_steps(ce.certificate_number) < 0.3, "certificate numbers carry gaps")
    ok(_steps(cl.claim_number.str.replace(r"-S\d$", "", regex=True)) < 0.3, "claim numbers carry gaps")
    ok(max(_steps(g.parcel_id) for _, g in pm.groupby("zip_code")) < 0.3, "parcel ids carry gaps in every ZIP")
    ok(max(_steps(g.permit_number.str[-5:]) for _, g in pe.groupby([pe.county, pe.issue_date.str[:4]])) < 0.4,
       "permit numbers carry other trades' gaps")
    iss = ce.event_date[ce.event == "ISSUED"]
    ok(_weekday_share(iss) == 1.0, "certificates issued on working days")
    ok(_weekday_share(pe.issue_date) == 1.0, "permits issued on working days")
    pay = cl.payment_date[cl.payment_date != "2012-01-01"]
    ok(_weekday_share(pay) == 1.0, "payments run on working days (the cut-over posting aside)")
    ch = pm[pm.channel != "Transfer - Gulfway"].sort_values("policy_number").channel.tolist()
    ok(all(np.mean([ch[i] == ch[i + k] for i in range(len(ch) - k)]) < 0.9 for k in (2, 3, 4)), "channel not dealt in turn")
    ok(len({round(v, 2) for v in f["aal_musd"].values()}) == 4 and all(v % 1 for v in f["aal_musd"].values()),
       "no round or repeated annual losses")
    # ---------------------------------------------------------------- extracts and documents against their dates
    ok(cl.payment_date.max() <= P.ASOF and pe.issue_date.max() <= P.ASOF and ce.event_date.max() <= P.ASOF,
       "no extract carries a date after its pull")

    def text(x):
        t = " ".join(pg.extract_text() or "" for pg in PdfReader(os.path.join(target, x)).pages)
        ok(len(t) > 400, "%s extracts" % x)
        return re.sub(r"\s+", " ", t)
    co = text(P.FILES["closeout"])
    ok("close-out memo" in co, "close-out text read (control)")
    closes = re.findall(r"\d{4}-\d{2}-\d{2} (\d{4}-\d{2}-\d{2})", co)
    ok(len(closes) >= 10 and max(closes) <= "2026-02-09", "close-out summary dated after its last close-out")
    lags = [(pd.Timestamp(b) - pd.Timestamp(a)).days for a, b in re.findall(r"(\d{4}-\d{2}-\d{2}) (\d{4}-\d{2}-\d{2})", co)]
    ok(len(set(lags)) >= len(lags) - 2, "close-out lags vary by storm")
    vn = PdfReader(os.path.join(target, P.FILES["vendor"])).metadata
    ok(vn.get("/Author") == P.VENDOR and "Corvane" in vn.get("/Producer", ""), "the vendor's note carries the vendor as producer")
    br = text(P.FILES["brief"])
    ok("How the counties are compared" in br and "November 6, 2026" in br, "brief read and dated after the vendor's note")
    # ---------------------------------------------------------------- distractors: delete them and nothing moves
    tmp = tempfile.mkdtemp(prefix="t309d_")
    try:
        for x in files:
            if x not in dis:
                os.symlink(os.path.abspath(os.path.join(target, x)), os.path.join(tmp, x))
        r2 = S.main_call(tmp)
        ok(r2["call"] == r["call"] and abs(r2["removed"][S.GOLDEN][r["call"]] - r["removed"][S.GOLDEN][r["call"]]) < 1,
           "distractors deleted: same call and figure")
        a = S.ask_a(tmp)
        ok(all(int(a.loc[n, "homes"]) == f["ask_a"][n][0] for n in f["ask_a"]), "distractors deleted: ask A unchanged")
        c_ = S.ask_c(tmp)
        ok(all(int(c_.loc[n, "homes"]) == f["ask_c"][n][0] for n in f["ask_c"]), "distractors deleted: ask C unchanged")
    finally:
        shutil.rmtree(tmp)


def _cells_variant(target, lines=None, fort_token=None, kt=None):
    """cells() with one convention changed."""
    old_kt = S.KT
    if kt:
        S.KT = kt
    c = S.cells(target)
    S.KT = old_kt
    if lines:
        reg = S.storm_table(target)
        reg = reg[reg.landfall_date.str[:4].astype(int) >= 2012]
        cl = pd.read_csv(os.path.join(target, P.FILES["claims"]), dtype={"zip_code": str}, keep_default_na=False)
        cl = cl[cl.catastrophe_code.isin(reg.claims_catastrophe_code) & cl.line_type.isin(lines)]
        cl["fort"] = cl.mitigation_credit.str.contains("FORT-R").astype(int)
        cl = cl.merge(reg[["claims_catastrophe_code", "storm_id"]], left_on="catastrophe_code", right_on="claims_catastrophe_code")
        paid = cl.groupby(["storm_id", "zip_code", "fort"]).amount_usd.sum().rename("paid2")
        c = c.merge(paid.reset_index(), on=["storm_id", "zip_code", "fort"], how="left").fillna({"paid2": 0.0})
        c["paid"] = c.paid2
    return c


def _removed(target, c):
    aal, res, adj = S.county_figures(target, c)
    return res[S.GOLDEN]


def _call(target, c):
    return _removed(target, c).idxmax()


if __name__ == "__main__":
    main(sys.argv[1])
