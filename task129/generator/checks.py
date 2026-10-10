"""task129 generator: every assertion the pack has to pass, run on the files as written.

Each check is recorded by name with its value; the first failure stops the build."""
import json
import os
import re
import subprocess
import sys

import numpy as np
import pandas as pd

import params as P
import golden as G
from golden import F

REC = {}
COUNT = [0]


def ok(name, cond, value=None):
    COUNT[0] += 1
    REC[name] = value if value is not None else bool(cond)
    if not cond:
        raise AssertionError(f"check failed: {name}: {value}")


def clearance(x, binw):
    """Distance from x to the nearest edge of its rounding bin (round half away)."""
    r = x / binw
    frac = r - np.floor(r)
    return min(abs(frac - 0.5), 1.0) * binw if True else 0.0


def edge_dist(x, binw):
    r = x / binw - np.floor(x / binw)
    return binw * abs(r - 0.5)


def rank_of(d, key):
    order = sorted(d, key=lambda k: -d[k])
    return order.index(key) + 1, order


def run(out, tgt, R, meta):
    # ------------------------------------------------------------ input gates
    names = sorted(os.listdir(tgt))
    ok("gate.files>=10", len(names) >= 10, len(names))
    fmts = sorted({n.rsplit(".", 1)[1] for n in names})
    ok("gate.formats>=3", len(fmts) >= 3, fmts)
    ok("gate.rows>=25000", meta["input_gates"]["largest_file_rows"] >= 25_000,
       meta["input_gates"]["largest_file_rows"])
    dis = meta["distractor_files"]
    ok("gate.distractors>=2", len(dis) >= 2 and all(d in names for d in dis), dis)
    ok("gate.deliverables", 1 <= len(meta["deliverables"]) <= 3, meta["deliverables"])
    text_ext = (".csv", ".md", ".txt", ".json")
    blob = ""
    for n in names:
        if n.endswith(text_ext):
            blob += open(os.path.join(tgt, n), encoding="utf-8").read().lower()
    ok("gate.no_distractor_word", "distractor" not in blob and
       not any("distractor" in n.lower() for n in names))
    for word in ["first load", "cached load", "warm cache", "reload of the cached", "cache state"]:
        ok(f"leak.no_word[{word}]", word not in blob)
    man = pd.read_csv(os.path.join(tgt, F["manifest"]))
    ok("h9.manifest_set", sorted(man.file) == sorted(n for n in names if n != F["manifest"]))
    guide = open(os.path.join(tgt, F["guide"]), encoding="utf-8").read()
    for k in ["registry", "subs", "editions", "release", "rollout", "crawl", "assets", "cdn"]:
        ok(f"h9.guide_names[{k}]", F[k] in guide)

    # ------------------------------------------------------------ containers (H1)
    import scrub_producer_metadata as S
    for n in names:
        if n.endswith((".pdf", ".xlsx")):
            names_, bad = S.audit(os.path.join(tgt, n), "2025-11-01", "2026-09-07")
            ok(f"h1.clean[{n}]", not names_ and not bad, (names_, bad))

    # ------------------------------------------------------------ load
    L = G.load(tgt)
    v = G.views(L)
    sw, t = G.switch_times(L)
    a = G.august(v)

    # ------------------------------------------------------------ main call: rungs 2 to 4
    M = G.main_call(v, L)
    A3, C3 = M["phone"]["A"], M["phone"]["C"]
    A4, C4 = M["state"]["A"], M["state"]["C"]
    Ar, Cr = M["raw"]["A"], M["raw"]["C"]
    T = {X: G.dated(v, L, X) for X in "DBE"}
    Tt = {X: sum(T[X].values()) for X in "DBE"}
    apz = G.puzzles_step(v, L)
    REC["figures"] = {"C": C4, "A": A4, "D": Tt["D"], "B": Tt["B"], "E": Tt["E"],
                      "grid": M["grid"], "T": T, "A_puz": M["A_puz"], "C_sub": M["C_sub"],
                      "rung3": {"A": A3, "C": C3}, "raw": {"A": Ar, "C": Cr}, "joint": M["joint"],
                      "joint_pts": M["joint_pts"], "raw_pts": M["raw_pts"], "puz_step": apz}
    r2 = {"D": Tt["D"], "B": Tt["B"], "E": Tt["E"], "A": apz}
    rk, order = rank_of(r2, "D")
    ok("rung2.leader_D", order[0] == "D", order)
    ok("rung2.margin", r2["D"] / r2[order[1]] >= 1.15, r2["D"] / r2[order[1]])
    ok("rung2.C_unplaced", "C" not in r2)
    ok("rung3raw.leader_A", Ar / Cr >= 1.15, Ar / Cr)
    r3 = {"A": A3, "C": C3, "D": Tt["D"], "B": Tt["B"], "E": Tt["E"]}
    rk3, o3 = rank_of(r3, "C")
    ok("rung3.leader_A", o3[0] == "A", o3)
    ok("rung3.C_second", rk3 == 2, rk3)
    ok("rung3.margin>=1.20", A3 / C3 >= 1.20, A3 / C3)
    r4 = {"A": A4, "C": C4, "D": Tt["D"], "B": Tt["B"], "E": Tt["E"]}
    rk4, o4 = rank_of(r4, "C")
    ok("rung4.leader_C", o4[0] == "C", o4)
    ok("rung4.margin>=1.5", C4 / A4 >= 1.5, C4 / A4)
    ok("rung4.runner_up_A", o4[1] == "A" and A4 / Tt["D"] >= 1.15, A4 / Tt["D"])
    dom = (C4 / C3) / (A4 / A3)
    ok("dominance", dom >= 1.2 * (A3 / C3), (dom, A3 / C3))
    REC["dominance"] = dom

    # ------------------------------------------------------------ rungs 0 and 1 (lab)
    lab0 = G.lab_weight(L, matched=False, by_title=False)
    lab1 = G.lab_weight(L, matched=True, by_title=False)
    l0 = {k[1]: x for k, x in lab0.items()}
    l1 = {k[1]: x for k, x in lab1.items()}
    REC["lab0"], REC["lab1"] = l0, l1
    rk0, o0 = rank_of(l0, "C")
    ok("rung0.leader_B", o0[0] == "B" and l0["B"] / l0[o0[1]] >= 1.15, (o0, l0))
    ok("rung0.C_4th_or_5th", rk0 >= 4, rk0)
    rk1, o1 = rank_of(l1, "C")
    ok("rung1.leader_E", o1[0] == "E" and l1["E"] / l1[o1[1]] >= 1.15, (o1, l1))
    ok("rung1.C_4th_or_5th", rk1 >= 4, rk1)
    ok("ladder.distinct_leaders", len({o0[0], o1[0], order[0], o3[0], o4[0]}) == 5)

    # ------------------------------------------------------------ the constructed disagreement
    def fshare(g):
        x = a[a.group == g]
        return float((x.w * (x.state == "F")).sum() / x.w.sum())
    fb, fs, fp = fshare("base"), fshare("sub"), fshare("puz")
    REC["first_share"] = {"base": fb, "sub": fs, "puz": fp}
    ok("state.base_vs_groups", fb / max(fs, fp) >= 2.5, (fb, fs, fp))
    ok("state.groups_equal", abs(fs - fp) <= 0.02, (fs, fp))
    eA, eC = M["state"]["eA"], M["state"]["eC"]
    for pc in ["low", "mid", "high"]:
        ok(f"state.C_first>cached[{pc}]", eC[(pc, "F")] > 2.5 * eC[(pc, "K")], (eC[(pc, "F")], eC[(pc, "K")]))
        ok(f"state.A_cached>first[{pc}]", eA[(pc, "K")] > 2.5 * eA[(pc, "F")], (eA[(pc, "K")], eA[(pc, "F")]))
    # complete-partition invariance: the phone-standardised split ties to the joint ramp
    base_a = a[a.group == "base"]
    split = G.apply(base_a, M["phone"]["eA"], ["pclass"]) + G.apply(base_a, M["phone"]["eC"], ["pclass"])
    tie = abs(split - M["joint"]) / M["joint"]
    raw_res = (M["joint_pts"] - M["raw_pts"]) / M["joint_pts"]
    REC["tie"], REC["raw_residual"] = tie, raw_res
    ok("L8.phone_split_ties", tie <= 0.05, tie)
    ok("L8.raw_residual", raw_res >= 0.06, raw_res)

    # ------------------------------------------------------------ correction grid (C4)
    grid = {}
    M_lp = G.main_call(v, L, by_state="landing_proxy")
    grid["landing_proxy"] = (M_lp["state"]["A"], M_lp["state"]["C"])
    for col in ["ref", "ect", "title"]:
        Mx = G.main_call(v, L, by_state=col)
        grid[col] = (Mx["state"]["A"], Mx["state"]["C"])
    Ms = G.main_call(v.assign(pclass="all"), L)
    grid["state_no_phone"] = (Ms["state"]["A"], Ms["state"]["C"])
    for k, (gA, gC) in grid.items():
        names_A = gA > gC
        off = abs(gC - C4) / C4
        REC[f"grid.{k}"] = (gA, gC)
        ok(f"grid[{k}]", names_A or off >= 0.06, (gA, gC, off))
    for wk in (21, 35):
        Mw = G.main_call(v, L, win=pd.Timedelta(days=wk))
        ok(f"corridor.window{wk}", Mw["state"]["C"] > Mw["state"]["A"] > Tt["D"],
           (Mw["state"]["C"], Mw["state"]["A"]))

    # ------------------------------------------------------------ C1 convergences on the main population
    main = v[v.ts >= pd.Timestamp(P.FORWARDER_FIX) - pd.Timedelta(hours=2)]
    allrows = G.views(L, dedup=False, phones=False)
    mainall = allrows[allrows.ts >= pd.Timestamp(P.FORWARDER_FIX) - pd.Timedelta(hours=2)]
    ok("sep.no_tablets_in_main", int((mainall.ff != "phone").sum()) == 0, int((mainall.ff != "phone").sum()))
    sp = L["spine"]
    m_ts = sp.ts_utc.dt.tz_localize(None) >= pd.Timestamp(P.FORWARDER_FIX) - pd.Timedelta(hours=2)
    ok("sep.no_duplicates_in_main", not sp[m_ts].pv_id.duplicated().any())
    ok("sep.masthead_current_in_main", bool((main.title == main.title_cur).all()))
    ok("axis9.no_lcp_4000", int((sp.lcp_ms == 4000).sum()) == 0)
    du = G.deploy_utc(L)
    tsv = sp.ts_utc.dt.tz_localize(None).values
    k = np.searchsorted(du, tsv, side="right")
    near = np.minimum(np.abs(tsv - du[np.clip(k - 1, 0, len(du) - 1)]),
                      np.abs(du[np.clip(k, 0, len(du) - 1)] - tsv))
    ok("axis9.no_view_near_deploy", bool((near >= np.timedelta64(10, "m")).all()))
    reg = L["registry"]
    ok("axis16.models_resolve", reg.device_model.is_unique and
       set(sp.device_model.unique()) <= set(reg.device_model))
    # state: per device against per device and bundle (puzzles bundle separate)
    vb = main.assign(bundle=np.where(main.template == "spil", "spil", "platform"))
    vb = vb.sort_values(["device_key", "bundle", "ts"], kind="stable")
    kk = np.searchsorted(du, vb.ts.values, side="right") - 1
    dk = (vb.device_key + "|" + vb.bundle).values
    st_b = np.where(np.r_[True, dk[1:] != dk[:-1]] | np.r_[True, kk[1:] != kk[:-1]], "F", "K")
    mg = vb.group.isin(["base", "sub", "puz"]).values
    ok("axis+.state_per_bundle", bool((st_b[mg] == vb.state.values[mg]).all()),
       int((st_b[mg] != vb.state.values[mg]).sum()))
    # state against the simulated truth on the main population
    X = R["X"]
    tr = X[X.t_local >= np.datetime64(P.FORWARDER_FIX)][["pv_id", "state"]].set_index("pv_id").state
    same = (tr.reindex(main.pv_id.values).values == main.state.values)
    ok("truth.state_matches", same.mean() == 1.0, float(same.mean()))
    # subscription status at view time and at the pull date
    sb = L["subs"]
    pull_active = set(sb[(sb.end_date == "") | (sb.end_date >= P.EXTRACT_PULLED.isoformat())].account_key)
    acc = main.account_key.fillna("").values
    pulled = np.array([x in pull_active for x in acc])
    mg2 = main.group.isin(["base", "sub", "puz", "subpuz"]).values
    ok("axis4.status_view_eq_pull", bool((pulled[mg2] == main.sub.values[mg2]).all()))
    # August scale: weights by title equal the close-out
    co = L["closeout"]
    for ti in P.TITLES:
        x = co[(co.Month == "2026-08") & (co.Title == P.TITLE_NAME[ti])]["Mobile page views"].iloc[0]
        y = v[(v.month == 8) & (v.title_cur == ti)].w.sum()
        ok(f"axis21.closeout_aug[{ti}]", int(x) == int(y), (x, y))
    return finish(out, tgt, L, v, M, T, Tt, A4, C4, A3, C3)


def finish(out, tgt, L, v, M, T, Tt, A4, C4, A3, C3):
    HB, WB = P.HEADLINE_BIN, P.WORKBOOK_BIN
    # ------------------------------------------------------------ graded figures mid-bin
    ok("bin.headline_C", edge_dist(C4, HB) >= 1500, edge_dist(C4, HB))
    ok("bin.runner_up_A", edge_dist(A4, HB) >= 1500, edge_dist(A4, HB))
    ok("tell.headline_not_round", round(C4) % 1000 != 0)
    for c in P.COHORTS:
        for k in "AC":
            x = M["grid"][c][k]
            ok(f"bin.grid[{c},{k}]", edge_dist(x, WB) >= 1000, (x, edge_dist(x, WB)))
    ok("grid.C_sums_to_headline", abs(sum(M["grid"][c]["C"] for c in P.COHORTS) - C4) < 1e-6)
    ok("grid.A_plus_puzzles_is_A", abs(sum(M["grid"][c]["A"] for c in P.COHORTS) + M["A_puz"] - A4) < 1e-6)
    for X in "DBE":
        for ti in P.TITLES:
            ok(f"bin.T[{X},{ti}]", edge_dist(T[X][ti], WB) >= 1500, (T[X][ti], edge_dist(T[X][ti], WB)))
    # rounding path: summing rounded cohort figures lands in the headline's bin
    ok("axis10.rounding_path", round(sum(round(M["grid"][c]["C"], -3) for c in P.COHORTS), -4)
       == round(C4, -4))
    # second correct handling of the tag gap converges
    for X in "DBE":
        rr = G.dated_restricted(v, L, X)
        for ti in P.TITLES:
            ok(f"T.restricted_same_bin[{X},{ti}]", round(rr[ti], -4) == round(T[X][ti], -4),
               (rr[ti], T[X][ti]))

    # ------------------------------------------------------------ T devices (necessity matrix)
    vt = G.views(L, phones=False)
    vd = G.views(L, dedup=False)
    vl = G.views(L, dedup=False, phones=False)
    mats = {
        "T1_masthead": {X: G.dated(v, L, X, title_col="title") for X in "DBE"},
        "T4_tag_gap": {X: G.dated(v, L, X, strata=False) for X in "DBE"},
        "H1_tablets": {X: G.dated(vt, L, X) for X in "DBE"},
        "H2_duplicates": {X: G.dated(vd, L, X) for X in "DBE"},
    }
    lazy = {X: G.dated(vl, L, X, title_col="title", strata=False) for X in "DBE"}
    nm = {}
    for dname, res in mats.items():
        for X in "DBE":
            for ti in P.TITLES:
                nm[(dname, X, ti)] = res[X][ti] / T[X][ti] - 1
    REC["T.necessity"] = {f"{a}|{b}|{c}": round(x, 4) for (a, b, c), x in nm.items()}
    for X in "DBE":
        for ti in P.TITLES:
            movers = [d for d in mats if abs(nm[(d, X, ti)]) >= 0.02]
            ok(f"T.two_devices[{X},{ti}]", len(movers) >= 2, movers)
            ok(f"T.lazy_off[{X},{ti}]", abs(lazy[X][ti] / T[X][ti] - 1) >= 0.05 and
               round(lazy[X][ti], -4) != round(T[X][ti], -4), (lazy[X][ti], T[X][ti]))
    for dname in mats:
        ok(f"T.device_bites[{dname}]", max(abs(nm[(dname, X, ti)]) for X in "DBE" for ti in P.TITLES) >= 0.05)
    dmax = max(sum(r["D"].values()) for r in list(mats.values()) + [lazy])
    ok("sep.D_never_reaches_A", A4 / dmax >= 1.15, A4 / dmax)

    # ------------------------------------------------------------ L ask
    Lg = G.lab_weight(L)
    Lh = G.lab_weight(L, rule="host")
    Lf = G.lab_weight(L, matched=False)
    Lr = G.lab_weight(L, run_of_record=False)
    Ll = G.lab_weight(L, matched=False, run_of_record=False, rule="host")
    REC["L"] = {f"{a}|{b}": x for (a, b), x in Lg.items()}
    for key, x in Lg.items():
        ok(f"bin.L[{key}]", edge_dist(x, 0.1) >= 0.01, (x, edge_dist(x, 0.1)))
        movers = [n for n, r in (("host", Lh), ("full", Lf), ("runs", Lr)) if abs(r[key] - x) >= 0.15]
        ok(f"L.two_devices[{key}]", len(movers) >= 1 + (key[1] in "AC"), movers)
        ok(f"L.lazy_off[{key}]", abs(Ll[key] - x) >= 0.15, (Ll[key], x))
    for key in Lg:
        if key[1] in "AC":
            ok(f"L.host_rule_bites[{key}]", abs(Lh[key] / Lg[key] - 1) >= 0.08, (Lh[key], Lg[key]))

    # ------------------------------------------------------------ I ask
    Ig = G.image_delivery(L)
    Ih = G.image_delivery(L, hits_only=True)
    Ik = G.image_delivery(L, kb_fix=False)
    Is = G.image_delivery(L, denom="scored")
    Il = G.image_delivery(L, hits_only=True, kb_fix=False)
    REC["I"] = Ig
    for m, (rq, kb) in Ig.items():
        ok(f"bin.I_req[{m}]", edge_dist(rq, 0.1) >= 0.01, (rq, edge_dist(rq, 0.1)))
        ok(f"bin.I_kb[{m}]", edge_dist(kb, 0.1) >= 0.01, (kb, edge_dist(kb, 0.1)))
        ok(f"I.hits_bite[{m}]", abs(Ih[m][0] / rq - 1) >= 0.03, Ih[m][0] / rq)
        ok(f"I.denominator_bites[{m}]", abs(Is[m][0] / rq - 1) >= 0.015, Is[m][0] / rq)
        ok(f"I.lazy_off[{m}]", round(Il[m][0], 1) != round(rq, 1), (Il[m][0], rq))
        if m in ("2026-06", "2026-07"):
            ok(f"I.kb_units_bite[{m}]", abs(Ik[m][1] / kb - 1) >= 0.08, Ik[m][1] / kb)

    # ------------------------------------------------------------ calibration roster
    ro = L["roster"]
    sv = []
    for r in ro.itertuples(index=False):
        pre_v, pre_o, post_v, post_o, mv, saving = r[4], r[5], r[6], r[7], r[9], r[10]
        rec = round((pre_o / pre_v - post_o / post_v) * mv)
        sv.append(int(saving))
        ok(f"roster.reproduces[{r[0]}]", rec == int(saving), (rec, saving))
    ok("roster.n=11", len(ro) == 11)
    kb = ro["Crawl kB removed per page"].astype(float).values
    rc = pd.Series(sv).rank().corr(pd.Series(kb).rank())
    ok("roster.lab_basis_refused", rc < 0.3, rc)
    best = max(sv)
    REC["roster_best"] = best
    ok("roster.line_below_A_and_C", best < A4 / 1.1 and best < C3 / 1.1, (best, A4, C3))
    puzfix = ro[ro.Fix == "OPS-FX-262"]
    a_pts = 100 * G.puzzles_step(v, L) / G.august(v)[G.august(v).group == "puz"].w.sum()
    ok("roster.resembles_decoy", abs(2.2 / a_pts - 1) <= 0.25, a_pts)

    # ------------------------------------------------------------ clean-data and lens-swap tests
    v_new = v[v.ts >= pd.Timestamp(P.FORWARDER_FIX)]
    Mc = G.main_call(v_new, L)
    ok("clean.collector_rows", abs(Mc["state"]["C"] - C4) < 1e-6 and abs(Mc["phone"]["A"] - A3) < 1e-6)
    lab0 = G.lab_weight(L, matched=False, by_title=False)
    lab_rep = G.lab_weight(L, matched=True, by_title=False)
    lead0 = max("ABCDE", key=lambda k: lab0[("all", k)])
    lead_rep = max("ABCDE", key=lambda k: lab_rep[("all", k)])
    ok("clean.crawl_moves_rung0_only", lead0 == "B" and lead_rep == "E")
    ok("lens.answer_ne_naive", (C4 > A4) and (A3 > C3))

    # ------------------------------------------------------------ distractors unused, relevant
    for k in G.DISTRACTORS:
        txt = open(os.path.join(tgt, F[k]), encoding="utf-8").read()
        ok(f"distractor.relevant[{k}]", any(P.TITLE_NAME[t] in txt for t in P.TITLES) and "2026" in txt)
    import inspect
    src = inspect.getsource(G)
    for k in G.DISTRACTORS:
        ok(f"distractor.unused[{k}]", f'L["{k}"]' not in src and f"F[\"{k}\"]" not in src.split("def load")[1])

    # ------------------------------------------------------------ single statement and tells
    from pypdf import PdfReader
    pdftext = {k: " ".join(p.extract_text() for p in PdfReader(os.path.join(tgt, F[k])).pages)
               for k in ["sla", "paywall", "cdnapp"]}
    allt = {**pdftext}
    for n in os.listdir(tgt):
        if n.endswith((".csv", ".md", ".txt", ".json")):
            allt[n] = open(os.path.join(tgt, n), encoding="utf-8").read()
    for pat, home in [("4.0 seconds", "sla"), ("28 days either side", "sla"),
                      ("latest full month", "sla"), ("ad-free layout on every template", "paywall")]:
        hits = [k for k, x in allt.items() if pat in " ".join(x.split())]
        ok(f"single_statement[{pat}]", hits == [home], hits)
    sp = L["spine"]
    mc = pd.to_datetime(sp.ts_utc).dt.month.value_counts()
    ok("tell.row_counts_vary", mc.nunique() == len(mc))
    co = L["closeout"]
    ok("tell.closeout_not_round", not any(float(x) == round(float(x)) for x in co["Share over line (%)"]))
    ok("assertions>=40", COUNT[0] >= 40, COUNT[0])
    REC["n_assertions"] = COUNT[0]
    print(f"checks: {COUNT[0]} assertions passed")
    return REC
