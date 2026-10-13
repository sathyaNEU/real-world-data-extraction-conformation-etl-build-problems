"""task129 generator: every assertion the pack has to pass, run on the files as written.

Each check is recorded by name with its value; the first failure stops the build. Blocks: the input
gates and containers; the clean truth against the frame the golden reads; the ladder by rung, the
constructed disagreement, the correction grid and the corridor; the C1 convergences on the main
population; the semantic fork table (SF1 to SF12); the three-rules block (R1 to R3c); the bins; the
two asks (T and I) with their device matrices, cracker and mirror sheets and composed mishandlings;
the clean-data and lens-swap tests; distractors, single statements and the realism sweep."""
import gc
import itertools
import os

import numpy as np
import pandas as pd

import params as P
import golden as G
from golden import F

REC = {}
COUNT = [0]
SOFT = set(os.environ.get("T129_SOFT", "").split(","))
FAILS = []


def ok(name, cond, value=None):
    COUNT[0] += 1
    if not cond and (name in SOFT or "*" in SOFT):
        FAILS.append((name, value))
        REC[name] = value
        print("SOFT FAIL", name, value)
        return
    REC[name] = value if value is not None else bool(cond)
    if not cond:
        raise AssertionError(f"check failed: {name}: {value}")


def edge_dist(x, binw):
    r = x / binw - np.floor(x / binw)
    return binw * abs(r - 0.5)


def same_bin(x, y, binw):
    return np.floor(x / binw + 0.5) == np.floor(y / binw + 0.5)


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
    for word in ["first load", "cached load", "warm cache", "reload of the cached", "cache state",
                 "second beacon", "older library", "native", "load event"]:
        ok(f"leak.no_word[{word}]", word not in blob)
    man = pd.read_csv(os.path.join(tgt, F["manifest"]))
    ok("h9.manifest_set", sorted(man.file) == sorted(n for n in names if n != F["manifest"]))
    guide = open(os.path.join(tgt, F["guide"]), encoding="utf-8").read()
    for k in ["registry", "subs", "editions", "release", "rollout", "cdn"]:
        ok(f"h9.guide_names[{k}]", F[k] in guide)

    # ------------------------------------------------------------ containers (H1)
    import scrub_producer_metadata as S
    for n in names:
        if n.endswith((".pdf", ".xlsx")):
            names_, bad = S.audit(os.path.join(tgt, n), "2025-11-01", "2026-09-07")
            ok(f"h1.clean[{n}]", not names_ and not bad, (names_, bad))

    # ------------------------------------------------------------ load, and the clean truth
    L = G.load(tgt)
    v = G.views(L)
    sw, t = G.switch_times(L)
    a = G.august(v)
    X = R["X"]
    truth_phone = set(X.pv_id.values[X.pclass.values != "tablet"])
    ok("truth.golden_frame_is_every_phone_view_once", set(v.pv_id) == truth_phone and v.pv_id.is_unique,
       (len(set(v.pv_id) ^ truth_phone)))
    Sx = R["S"]
    sec = set(Sx.pv_id.values[Sx.second.values])
    sp = L["spine"]
    spd = sp.sort_values("beacon_id", kind="stable").drop_duplicates("pv_id")
    flagged = set(spd.loc[G.repeated_beacons(spd), "pv_id"])
    ok("truth.repeat_rule_is_exact", flagged == sec and len(sec) == R["n_second"], (len(flagged), len(sec)))
    REC["n_second_beacons"] = len(sec)
    del Sx, sec, flagged, spd
    for k in ("S", "V", "ct"):
        R.pop(k, None)
    gc.collect()

    # ------------------------------------------------------------ main call: the ladder
    M = G.main_call(v, L)
    A3, C3 = M["phone"]["A"], M["phone"]["C"]
    A4, C4 = M["state"]["A"], M["state"]["C"]
    Ar, Cr = M["raw"]["A"], M["raw"]["C"]
    T = {x: G.dated(v, L, x) for x in "DBE"}
    Tt = {x: sum(T[x].values()) for x in "DBE"}
    apz = G.puzzles_step(v, L)
    M_lp = G.main_call(v, L, by_state="landing_proxy")
    A2, C2 = M_lp["state"]["A"], M_lp["state"]["C"]
    REC["figures"] = {"C": C4, "A": A4, "D": Tt["D"], "B": Tt["B"], "E": Tt["E"], "T": T,
                      "A_puz": M["A_puz"], "C_sub": M["C_sub"], "R1": {"A": A3, "C": C3},
                      "R2": {"A": A2, "C": C2}, "raw": {"A": Ar, "C": Cr}, "joint": M["joint"],
                      "joint_pts": M["joint_pts"], "raw_pts": M["raw_pts"], "puz_step": apz}
    r0 = {"D": Tt["D"], "B": Tt["B"], "E": Tt["E"], "A": apz}
    _, o0 = rank_of(r0, "D")
    ok("R0.leader_D", o0[0] == "D" and r0["D"] / r0[o0[1]] >= 1.15, (o0, r0["D"] / r0[o0[1]]))
    ok("R0.C_unplaced", "C" not in r0)
    ok("R1raw.leader_A", Ar / Cr >= 1.15, Ar / Cr)
    r1 = {"A": A3, "C": C3, "D": Tt["D"], "B": Tt["B"], "E": Tt["E"]}
    rk1, o1 = rank_of(r1, "C")
    ok("R1.leader_A", o1[0] == "A", o1)
    ok("R1.C_second", rk1 == 2, rk1)
    ok("R1.margin>=1.20", A3 / C3 >= 1.20, A3 / C3)
    ok("R2.leader_A", A2 / C2 >= 1.15, A2 / C2)
    r3 = {"A": A4, "C": C4, "D": Tt["D"], "B": Tt["B"], "E": Tt["E"]}
    _, o3 = rank_of(r3, "C")
    ok("R3.leader_C", o3[0] == "C", o3)
    ok("R3.margin>=1.5", C4 / A4 >= 1.5, C4 / A4)
    ok("R3.runner_up_A", o3[1] == "A" and A4 / Tt["D"] >= 1.15, A4 / Tt["D"])
    dom = (C4 / C3) / (A4 / A3)
    ok("dominance", dom >= 1.2 * (A3 / C3), (dom, A3 / C3))
    REC["dominance"] = dom

    # ------------------------------------------------------------ the constructed disagreement
    def fshare(g):
        x = a[a.group == g]
        return float((x.w * (x.state == "F")).sum() / x.w.sum())

    def wshare(g):
        pre, post = G.windows(v, g, sw, t)
        x = pd.concat([pre, post])
        return float((x.w * (x.state == "F")).sum() / x.w.sum())
    fb, fs, fp = fshare("base"), wshare("sub"), wshare("puz")
    REC["first_share"] = {"base": fb, "sub": fs, "puz": fp}
    ok("state.base_vs_groups", fb / max(fs, fp) >= 2.5, (fb, fs, fp))
    ok("state.groups_equal", abs(fs - fp) <= 0.02, (fs, fp))
    eA, eC = M["state"]["eA"], M["state"]["eC"]
    for pc in ["low", "mid", "high"]:
        ok(f"state.C_first>later[{pc}]", eC[(pc, "F")] > 2.5 * eC[(pc, "K")], (eC[(pc, "F")], eC[(pc, "K")]))
        ok(f"state.A_later>first[{pc}]", eA[(pc, "K")] > 2.5 * eA[(pc, "F")], (eA[(pc, "K")], eA[(pc, "F")]))
    base_a = a[a.group == "base"]
    split = G.apply(base_a, M["phone"]["eA"], ["pclass"]) + G.apply(base_a, M["phone"]["eC"], ["pclass"])
    tie = abs(split - M["joint"]) / M["joint"]
    raw_res = (M["joint_pts"] - M["raw_pts"]) / M["joint_pts"]
    REC["tie"], REC["raw_residual"] = tie, raw_res
    ok("L8.phone_split_ties", tie <= 0.05, tie)
    ok("L8.raw_residual", raw_res >= 0.06, raw_res)

    # ------------------------------------------------------------ correction grid (C4) and corridor
    grid = {"landing_proxy": (A2, C2)}
    for col in ["ref", "ect", "title", "nav"]:
        Mx = G.main_call(v, L, by_state=col)
        grid[col] = (Mx["state"]["A"], Mx["state"]["C"])
    Ms = G.main_call(v.assign(pclass="all"), L)
    grid["state_no_phone"] = (Ms["state"]["A"], Ms["state"]["C"])
    for k, (gA, gC) in grid.items():
        off = abs(gC - C4) / C4
        REC[f"grid.{k}"] = (gA, gC, off)
        ok(f"grid[{k}]", gA > gC or off >= 0.06, (gA, gC, off))
    for col in ["ref", "ect", "title", "nav"]:
        ok(f"R1.visible_column_keeps_A[{col}]", grid[col][0] > grid[col][1], grid[col])
    for wk in (21, 35):
        Mw = G.main_call(v, L, win=pd.Timedelta(days=wk))
        ok(f"corridor.window{wk}", Mw["state"]["C"] > Mw["state"]["A"] > Tt["D"],
           (Mw["state"]["C"], Mw["state"]["A"]))
        REC[f"corridor.C{wk}"] = Mw["state"]["C"]

    # ------------------------------------------------------------ C1 convergences on the main population
    # the call's rows: from 28 days before the first separating or switch-on release
    t_main = min([t["PUZ"], t["SUB"]] + list(sw.values())) - G.WIN
    REC["main_population_from"] = str(t_main)
    main = v[v.ts >= t_main]
    allrows = G.views(L, dedup=False, phones=False, repeats=False)
    mainall = allrows[allrows.ts >= t_main]
    ok("sep.no_tablets_in_main", int((mainall.ff != "phone").sum()) == 0, int((mainall.ff != "phone").sum()))
    del allrows, mainall
    gc.collect()
    m_ts = sp.ts_utc.dt.tz_convert(None) >= t_main
    ok("sep.no_duplicates_in_main", not sp[m_ts].pv_id.duplicated().any())
    ok("sep.no_repeated_beacons_in_main", len(G.repeated_beacons(sp[m_ts])) == 0)
    ok("sep.masthead_current_in_main", bool((main.title == main.title_cur).all()))
    ok("axis9.no_lcp_4000", int((sp.lcp_ms == 4000).sum()) == 0)
    ok("axis14.no_device_time_ties", not v.duplicated(["device_key", "ts"]).any())
    du = G.deploy_utc(L)
    tsv = sp.ts_utc.dt.tz_localize(None).values
    k = np.searchsorted(du, tsv, side="right")
    near = np.minimum(np.abs(tsv - du[np.clip(k - 1, 0, len(du) - 1)]),
                      np.abs(du[np.clip(k, 0, len(du) - 1)] - tsv))
    ok("axis9.no_view_near_deploy", bool((near >= np.timedelta64(10, "m")).all()))
    reg = L["registry"]
    ok("axis16.models_resolve", reg.device_model.is_unique and
       set(sp.device_model.unique()) <= set(reg.device_model))
    vb = v.assign(bundle=np.where(v.template == "spil", "spil", "platform"))
    vb = vb.sort_values(["device_key", "bundle", "ts"], kind="stable")
    kk = np.searchsorted(du, vb.ts.values, side="right") - 1
    dk = (vb.device_key + "|" + vb.bundle).values
    st_b = np.where(np.r_[True, dk[1:] != dk[:-1]] | np.r_[True, kk[1:] != kk[:-1]], "F", "K")
    mg = (vb.group.isin(["base", "sub", "puz"]) & (vb.ts >= t_main)).values
    ok("axis+.state_per_bundle", bool((st_b[mg] == vb.state.values[mg]).all()),
       int((st_b[mg] != vb.state.values[mg]).sum()))
    tr = X[["pv_id", "state"]].set_index("pv_id").state
    same = (tr.reindex(main.pv_id.values).values == main.state.values)
    ok("truth.state_matches", same.mean() == 1.0, float(same.mean()))
    del X, tr, same, truth_phone
    R.pop("X", None)
    gc.collect()
    sb = L["subs"]
    pull_active = set(sb[(sb.end_date == "") | (sb.end_date >= P.EXTRACT_PULLED.isoformat())].account_key)
    acc = main.account_key.fillna("").values
    pulled = np.array([x in pull_active for x in acc])
    mg2 = main.group.isin(["base", "sub", "puz", "subpuz"]).values
    ok("axis4.status_view_eq_pull", bool((pulled[mg2] == main["sub"].values[mg2]).all()))
    co = L["closeout"]
    for mo in P_Q3():
        for ti in P.TITLES:
            x = co[(co.Month == f"2026-{mo:02d}") & (co.Title == P.TITLE_NAME[ti])]["Mobile page views"].iloc[0]
            y = v[(v.month == mo) & (v.title_cur == ti)].w.sum()
            ok(f"axis21.closeout[{mo},{ti}]", int(x) == int(y), (x, y))
    dw = _device_weighted(v, L, sw, t)
    REC["axis7.device_weighted"] = dw
    ok("axis7.device_weighting_keeps_call", dw["C"] > dw["A"], (dw, C4, A4))
    ok("axis14.sort_invariant", abs(G.main_call(v.sample(frac=1.0, random_state=7), L)["state"]["C"] - C4) < 1e-6)

    # ------------------------------------------------------------ semantic fork table
    sf_rows(L, v, t, M, A4, C4, A3, C3, Tt, tgt)

    # ------------------------------------------------------------ the three rules, executed
    three_rules(L, v, R, M, A4, C4, A3, C3, A2, C2, grid)
    return finish(out, tgt, L, v, M, T, Tt, A4, C4, A3, C3, R)


def P_Q3():
    import ship
    return ship.Q3


def _title_matched(v, L):
    """The subscriber groups rebuilt with a subscription counted only on its own title's pages (an all-titles
    product counts everywhere): the reading paywall 4.2 rules out."""
    sb = L["subs"]
    sb = sb[sb.account_key != ""]
    code = {n: k for k, n in P.TITLE_NAME.items()}
    tab = pd.DataFrame({"account_key": sb.account_key.values, "st": pd.to_datetime(sb.start_date).values,
                        "en": pd.to_datetime(sb.end_date.replace("", "2100-01-01")).values,
                        "tt": sb.title.map(code).fillna("*").values,
                        "all": sb["product"].str.contains("alle titler").values})
    acc = v.account_key.fillna("").values
    m = acc != ""
    q = pd.DataFrame({"i": np.flatnonzero(m), "account_key": acc[m], "day": v.day.values[m],
                      "vt": v.title_cur.values[m]})
    j = q.merge(tab, on="account_key", how="inner")
    j = j[(j.day >= j.st) & (j.day <= j.en) & (j["all"] | (j.tt == j.vt))]
    act = np.zeros(len(v), bool)
    act[j.i.unique()] = True
    tpl = v.template.values
    coh = np.isin(tpl, P.COHORTS)
    g = np.full(len(v), "legacy", dtype=object)
    g[coh & act] = "sub"
    g[coh & ~act] = "base"
    g[(tpl == "spil") & act] = "subpuz"
    g[(tpl == "spil") & ~act] = "puz"
    return v.assign(sub=act, group=g)


def _device_weighted(v, L, sw, t):
    """Each group, phone and state cell's effect read with every device weighted once, then valued on
    August's views: an estimator of another quantity than the service level's share of views, recorded."""
    n = v.groupby("device_key").w.transform("size")
    x = v.assign(w=v.w / n)
    by = ["pclass", "state"]
    eA, eC = G.effects(x, "puz", sw, t, by), G.effects(x, "sub", sw, t, by)
    fA, fC = G.effects(x, "puz", sw, t, ["pclass"]), G.effects(x, "sub", sw, t, ["pclass"])
    a = G.august(v)
    base, sub, puz = a[a.group == "base"], a[a.group == "sub"], a[a.group == "puz"]
    return {"A": G.apply(base, eA, by, fA) + G.apply(puz, eA, by, fA),
            "C": G.apply(base, eC, by, fC) + G.apply(sub, eC, by, fC)}


def sf_rows(L, v, t, M, A4, C4, A3, C3, Tt, tgt):
    HB = P.HEADLINE_BIN
    # SF1 mobile views: no tablet row from the forwarder fix on
    allp = G.views(L, phones=False)
    ok("SF1.no_tablets_after_fix", int(((allp.ff != "phone") & (allp.ts >= t["D"])).sum()) == 0)
    Mt = G.main_call(allp, L)
    del allp
    gc.collect()
    ok("SF1.same_call_with_tablets", same_bin(Mt["state"]["C"], C4, HB) and same_bin(Mt["state"]["A"], A4, HB))
    # SF2 restores counted as under: both figures leave their bins, the call stays
    vr = v.assign(scored=True, over=v.over & v.scored)
    M2 = G.main_call(vr, L)
    del vr
    ok("SF2.restores_as_under_move_figures", M2["state"]["C"] > M2["state"]["A"] and
       not same_bin(M2["state"]["C"], C4, HB), (M2["state"]["C"], M2["state"]["A"]))
    # SF3 another month: June to August average, still C
    a3 = v[v.month.isin([6, 7, 8])].assign(month=8)
    a3 = a3.assign(w=a3.w / 3.0)
    vv = pd.concat([v[~v.month.isin([6, 7, 8])], a3])
    M3 = G.main_call(vv, L)
    del vv, a3
    gc.collect()
    ok("SF3.other_month_same_name", M3["state"]["C"] > M3["state"]["A"])
    # SF4 every mobile view: the ad stack applied to subscribers' views too, still C
    sub = G.august(v)
    sub = sub[sub.group == "sub"]
    extraA = G.apply(sub, M["state"]["eA"], ["pclass", "state"], M["state"]["fA"])
    ok("SF4.every_view_same_name", C4 > A4 + extraA, (C4, A4 + extraA))
    # SF5 the front end on the base only
    base = G.august(v)
    base = base[base.group == "base"]
    C_base = G.apply(base, M["state"]["eC"], ["pclass", "state"], M["state"]["fC"])
    REC["SF5.C_base_only"] = C_base
    ok("SF5.base_only_same_call", C_base > A4, (C_base, A4))
    # SF6 the window: 28 days filed; 21 and 35 keep the call (corridor asserted above)
    ok("SF6.window_filed", G.WIN == pd.Timedelta(days=28))
    # the image pipeline's templates are named in the change register's scope (the T ask's population)
    import re as _re
    chg = pd.read_excel(os.path.join(tgt, F["changes"]), header=3, dtype=str)
    scope = chg[chg.Name.str.startswith("Image pipeline")].Scope.iloc[0]
    named = set(x.strip() for x in _re.search(r"\((.*)\)", scope).group(1).split(","))
    ok("T.hero_templates_filed", named == set(P.HERO), sorted(named))
    # SF7 the separating releases are the puzzles release and the ad-free release
    ro = L["rollout"]
    ok("SF7.adfree_one_release", (ro.layout != "ad-supported").sum() == 1)
    # SF8 status at view time against the pull date: checked as axis 4
    ok("SF8.status_convergent", REC.get("axis4.status_view_eq_pull") is True)
    # SF9 the runner-up on the same footing is A
    ok("SF9.runner_up_A", A4 > max(Tt.values()), (A4, Tt))
    # SF10 phone class from the registry's band: every main model resolves to one band
    reg = L["registry"]
    ok("SF10.one_band_per_model", reg.groupby("device_model").perf_band.nunique().max() == 1)
    # SF11 deploy offsets: reading local time as UTC moves the state of views by hours; the offset
    # is in every value
    rel = L["release"]
    ok("SF11.offset_in_value", bool(rel.deployed_at.str.contains(r"[+-]\d\d:\d\d$").all()))
    # SF12 rounding once: rounding each group's figure first lands in the same bins
    gC = sum(round(M["grid"][c]["C"], -3) for c in P.COHORTS)
    ok("SF12.rounding_path", same_bin(gC, C4, HB))
    # SF14 valuation: that month's scored views the change now reaches (service level, section 4); all
    # August views, or only views after each group's switch-on, keep the call and leave both bins
    sla = " ".join(" ".join(p.extract_text().split()) for p in __import__("pypdf").PdfReader(
        os.path.join(tgt, F["sla"])).pages)
    ok("SF14.filed", "counted over all of that month's scored views on the pages and layouts the change is live on "
                     "today" in sla)
    aug_all = v[v.month == 8]
    by = ["pclass", "state"]
    eA, eC, fA, fC = M["state"]["eA"], M["state"]["eC"], M["state"]["fA"], M["state"]["fC"]

    def valued(aug):
        b_, s_, z_ = aug[aug.group == "base"], aug[aug.group == "sub"], aug[aug.group == "puz"]
        return (G.apply(b_, eC, by, fC) + G.apply(s_, eC, by, fC), G.apply(b_, eA, by, fA) + G.apply(z_, eA, by, fA))
    sw_, t_ = G.switch_times(L)
    a8 = G.august(v)
    alts = {"all_views": valued(aug_all), "after_switch": valued(a8[~((a8.template == "forside") &
                                                                      (a8.ts < sw_["forside"]))])}
    for k, (cC, cA) in alts.items():
        REC[f"SF14.{k}"] = (cC, cA)
        ok(f"SF14.{k}_off_bins_same_call", cC > cA and not (same_bin(cC, C4, HB) and same_bin(cA, A4, HB)),
           (cC, cA))
    # SF15 window boundary: from the deploy moment (service level, section 3); calendar days keep the call
    ok("SF15.filed", "the moment the release that switched it on was deployed" in sla)

    def midnight(ts):
        return pd.Timestamp(ts).tz_localize("UTC").tz_convert(P.TZ).normalize().tz_convert("UTC").tz_localize(None)
    Mc = G.main_call(v, L, times=({k: midnight(x) for k, x in sw_.items()}, {k: midnight(x) for k, x in t_.items()}))
    REC["SF15.calendar"] = (Mc["state"]["C"], Mc["state"]["A"])
    ok("SF15.calendar_same_call", Mc["state"]["C"] > Mc["state"]["A"], REC["SF15.calendar"])
    # SF16 subscribers: any active subscription, on every title's site (paywall 4.2); a subscription counted only on
    # its own title's pages keeps the call
    pay = " ".join(" ".join(p.extract_text().split()) for p in __import__("pypdf").PdfReader(
        os.path.join(tgt, F["paywall"])).pages)
    ok("SF16.filed", "on all three titles' sites whichever titles their product includes" in pay)
    Mt_ = G.main_call(_title_matched(v, L), L)
    REC["SF16.title_matched"] = (Mt_["state"]["C"], Mt_["state"]["A"])
    ok("SF16.title_matched_same_call", Mt_["state"]["C"] > Mt_["state"]["A"], REC["SF16.title_matched"])
    # SF13 weighting: the field guide's "sum it to count views"; rows counted once give sampled rows, not
    # views, far outside both bins, and still C
    Mu = G.main_call(v.assign(w=1.0), L)
    REC["SF13.unweighted"] = {"A": Mu["state"]["A"], "C": Mu["state"]["C"]}
    ok("SF13.unweighted_rows_off_bins_same_call", Mu["state"]["C"] > Mu["state"]["A"] and
       Mu["state"]["C"] < 0.1 * C4 and Mu["state"]["A"] < 0.1 * A4, REC["SF13.unweighted"])


def three_rules(L, v, R, M, A4, C4, A3, C3, A2, C2, grid):
    sp = L["spine"]
    # R1: the field's raw material ships (page-view beacons with timings, devices, times; a release
    # log with deploy instants); no column holds the state or a change's effect
    cols = set(sp.columns)
    ok("R1.raw_material", {"device_key", "ts_utc", "lcp_ms", "sample_weight", "url_path"} <= cols)
    toks = {w for c in cols for w in c.lower().split("_")}
    said = toks & {"state", "cache", "cached", "first", "bundle", "effect", "repeat", "second"}
    ok("R1.no_state_column", not said, sorted(said))
    # R2: every Layer 1 item mishandled leaves the call and both figures where they were
    HB = P.HEADLINE_BIN
    for name, kw in (("tablets", dict(phones=False)), ("forwarded_twice", dict(dedup=False)),
                     ("second_beacons", dict(repeats=False))):
        frame = G.views(L, **kw)
        Mx = G.main_call(frame, L)
        del frame
        gc.collect()
        ok(f"R2.mess_neutral[{name}]", same_bin(Mx["state"]["C"], C4, HB) and same_bin(Mx["state"]["A"], A4, HB)
           and same_bin(Mx["phone"]["A"], A3, HB), (Mx["state"]["C"], Mx["state"]["A"]))
    vt = v.assign(title_cur=v.title)
    Mx = G.main_call(vt, L)
    ok("R2.mess_neutral[masthead]", same_bin(Mx["state"]["C"], C4, HB))
    # the export as it stood before every collector repair, from the forwarder fix on
    v_new = v[v.ts >= pd.Timestamp(P.FORWARDER_FIX)]
    Mc = G.main_call(v_new, L)
    ok("R2.clean_data_answer_and_default_unchanged", abs(Mc["state"]["C"] - C4) < 1e-6 and
       abs(Mc["phone"]["A"] - A3) < 1e-6)
    # R3a: the default path on the clean truth files the ad stack
    ok("R3a.analyst_test_files_A", A3 > C3 and round(A3, -4) == 1_230_000, (A3, C3))
    # R3b: only the decisive step changed files the golden; each lower correction leaves A or a
    # figure outside the bin
    ok("R3b.decisive_step_alone_files_C", C4 > A4 and round(C4, -4) == 1_460_000, (C4, A4))
    ok("R3b.landing_proxy_leaves_A", A2 > C2)
    for k in ("ref", "ect", "title", "nav"):
        ok(f"R3b.visible_column_leaves_A[{k}]", grid[k][0] > grid[k][1])
    gA, gC, off = REC["grid.state_no_phone"]
    ok("R3b.state_without_phone_off", off >= 0.06, off)
    # R3c: no plant: no repeated block of rows, no backfilled or copied window
    # (the older library's second beacons repeat their original's timings by construction; they are the T
    # ask's device, so the sweep runs on the frame without them)
    sp2 = sp.sort_values("beacon_id").drop_duplicates("pv_id")
    sp2 = sp2.drop(index=G.repeated_beacons(sp2))
    blk = sp2[["lcp_ms", "ttfb_ms", "cls"]].astype("float64").values
    full = ~np.isnan(blk).any(axis=1)
    pair = full[1:] & full[:-1]
    run_dup = float(((blk[1:] == blk[:-1]).all(axis=1) & pair).sum() / pair.sum())
    ok("R3c.no_repeated_block", run_dup < 0.001, run_dup)
    ok("R3c.no_answer_column", "is_dup" not in sp.columns and "second" not in sp.columns)


T_DEVS = ["second", "tablets", "forwarded"]
I_DEVS = ["native", "hits", "kb", "scored", "tablets", "forwarded", "second"]
SWEEP_COLS = ["ts", "local", "month", "w", "over", "scored", "template", "edition", "title", "title_cur"]


def _frame_key(sub):
    return ("forwarded" not in sub, "tablets" not in sub, "second" not in sub)


def sweeps(L, v):
    """Both asks under every combination of their mishandlings. Each combination of the three collector
    mishandlings is one beacon frame; frames are built one at a time and dropped once read."""
    tsubs = [s for n in range(1, len(T_DEVS) + 1) for s in itertools.combinations(T_DEVS, n)]
    isubs = [s for n in range(1, len(I_DEVS) + 1) for s in itertools.combinations(I_DEVS, n) if "native" in s]
    TV, IV = {}, {}
    for key in sorted({_frame_key(s) for s in tsubs + isubs}, reverse=True):
        fr = v if key == (True, True, True) else G.views(L, dedup=key[0], phones=key[1], repeats=key[2])[SWEEP_COLS]
        for s in tsubs:
            if _frame_key(s) == key:
                TV[s] = {x: G.dated(fr, L, x) for x in "DBE"}
        for s in isubs:
            if _frame_key(s) == key:
                IV[s] = G.image_delivery(L, fr, native=True, hits_only="hits" in s, kb_fix="kb" not in s,
                                         scored="scored" in s)
        del fr
        gc.collect()
    return tsubs, TV, isubs, IV


def finish(out, tgt, L, v, M, T, Tt, A4, C4, A3, C3, R):
    HB, WB = P.HEADLINE_BIN, P.WORKBOOK_BIN
    ok("bin.headline_C", edge_dist(C4, HB) >= 1500, edge_dist(C4, HB))
    ok("bin.runner_up_A", edge_dist(A4, HB) >= 1500, edge_dist(A4, HB))
    ok("tell.headline_not_round", round(C4) % 1000 != 0)

    # ------------------------------------------------------------ T: the dated changes by title
    for x in "DBE":
        for ti in P.TITLES:
            ok(f"bin.T[{x},{ti}]", edge_dist(T[x][ti], WB) >= 1500, (T[x][ti], edge_dist(T[x][ti], WB)))
        ok(f"bin.T_total[{x}]", edge_dist(Tt[x], HB) >= 1500, (Tt[x], edge_dist(Tt[x], HB)))
    # the share read inside local-edition and other pages lands in the same bins (C1)
    for x in "DBE":
        rr = G.dated(v, L, x, strata=True)
        for ti in P.TITLES:
            ok(f"T.page_class_converges[{x},{ti}]", same_bin(rr[ti], T[x][ti], WB), (rr[ti], T[x][ti]))
    tsubs, TV, isubs, IV = sweeps(L, v)
    devs = T_DEVS
    nm = {}
    for d in devs:
        r = TV[(d,)]
        for x in "DBE":
            for ti in P.TITLES:
                nm[(d, x, ti)] = r[x][ti] / T[x][ti] - 1
    REC["T.necessity"] = {f"{a}|{b}|{c}": round(z, 4) for (a, b, c), z in nm.items()}
    for x in "DBE":
        for ti in P.TITLES:
            ok(f"T.primary_moves[{x},{ti}]", not same_bin(T[x][ti] * (1 + nm[("second", x, ti)]), T[x][ti], WB)
               and abs(nm[("second", x, ti)]) >= 0.08, nm[("second", x, ti)])
    # the cracker: tablets out, forwarded copies deduplicated, today's mastheads, the gap held by page
    # class; the older library's beacons kept
    crk = TV[("second",)]
    REC["T.cracker"] = crk
    for x in "DBE":
        for ti in P.TITLES:
            ok(f"T.cracker_misses[{x},{ti}]", not same_bin(crk[x][ti], T[x][ti], WB), (crk[x][ti], T[x][ti]))
    # every composed mishandling that keeps the older library's beacons lands outside the bin
    worst = {}
    dmax = 0.0
    for sub in tsubs:
        r = TV[sub]
        dmax = max(dmax, sum(r["D"].values()))
        if "second" in sub:
            for x in "DBE":
                for ti in P.TITLES:
                    worst[(x, ti)] = min(worst.get((x, ti), 9e9), abs(r[x][ti] - T[x][ti]))
                    ok(f"T.composed_outside[{'+'.join(sub)}|{x},{ti}]", not same_bin(r[x][ti], T[x][ti], WB),
                       (r[x][ti], T[x][ti]))
    lazy = TV[tuple(devs)]
    REC["T.lazy"] = lazy
    # the over-cleaner: one view per device, page and day, which drops genuine repeat views
    oc = _overclean_T(L, v)
    REC["T.overclean"] = oc
    ok("sep.D_never_reaches_A", A4 / dmax >= 1.15, (A4, dmax))
    REC["T.closest_composed_miss"] = {f"{x}|{ti}": z for (x, ti), z in worst.items()}

    # ------------------------------------------------------------ I: image delivery per mobile page view
    Ig = G.image_delivery(L, v)
    REC["I"] = Ig
    for m, (rq, kb) in Ig.items():
        ok(f"bin.I_req[{m}]", edge_dist(rq, 0.1) >= 0.012, (rq, edge_dist(rq, 0.1)))
        ok(f"bin.I_kb[{m}]", edge_dist(kb, 10) >= 1.2, (kb, edge_dist(kb, 10)))
    Iu = G.image_delivery(L, v, by="utc")
    for m in Ig:
        ok(f"I.month_clock_converges[{m}]", same_bin(Iu[m][0], Ig[m][0], 0.1) and same_bin(Iu[m][1], Ig[m][1], 10),
           (Iu[m], Ig[m]))
    inat = G.image_delivery(L, v, native=True)
    for m, (rq, kb) in Ig.items():
        ok(f"I.primary_moves_req[{m}]", not same_bin(inat[m][0], rq, 0.1) and inat[m][0] / rq - 1 >= 0.05,
           inat[m][0] / rq)
        ok(f"I.primary_moves_kb[{m}]", not same_bin(inat[m][1], kb, 10), inat[m][1] / kb)
    # the cracker: both request columns, the fallback's kilobytes converted, phones, each page view
    # by its key, the native clients kept, the older library's beacons in the divisor
    icr = IV[("native", "second")]
    REC["I.cracker"] = icr
    for m, (rq, kb) in Ig.items():
        ok(f"I.cracker_misses_req[{m}]", not same_bin(icr[m][0], rq, 0.1), (icr[m][0], rq))
        ok(f"I.cracker_misses_kb[{m}]", not same_bin(icr[m][1], kb, 10), (icr[m][1], kb))
    ih = G.image_delivery(L, v, hits_only=True)
    ik = G.image_delivery(L, v, kb_fix=False)
    isc = G.image_delivery(L, v, scored=True)
    for m, (rq, kb) in Ig.items():
        ok(f"I.hits_only_bites[{m}]", not same_bin(ih[m][0], rq, 0.1), ih[m][0] / rq)
        ok(f"I.scored_divisor_bites[{m}]", not same_bin(isc[m][0], rq, 0.1), isc[m][0] / rq)
        if m in ("2026-06", "2026-07"):
            ok(f"I.kb_units_bite[{m}]", not same_bin(ik[m][1], kb, 10), ik[m][1] / kb)
    # composed: every mishandling set that keeps the native clients lands outside the bin
    for sub in isubs:
        r = IV[sub]
        for m, (rq, kb) in Ig.items():
            ok(f"I.composed_outside[{'+'.join(sub)}|{m}]",
               not same_bin(r[m][0], rq, 0.1) and not same_bin(r[m][1], kb, 10), (r[m], (rq, kb)))
    REC["I.lazy"] = IV[("native", "hits", "kb", "tablets", "forwarded", "second")]

    # ------------------------------------------------------------ clean-data and lens-swap tests
    ok("lens.answer_ne_naive", (C4 > A4) and (A3 > C3))

    # ------------------------------------------------------------ distractors unused, relevant
    for k in G.DISTRACTORS:
        txt = open(os.path.join(tgt, F[k]), encoding="utf-8").read()
        ok(f"distractor.relevant[{k}]", any(P.TITLE_NAME[t_] in txt for t_ in P.TITLES) and "2026" in txt)
    import inspect
    src = inspect.getsource(G)
    for k in G.DISTRACTORS:
        ok(f"distractor.unused[{k}]", f'L["{k}"]' not in src and f"F[\"{k}\"]" not in src.split("def load")[1])

    # ------------------------------------------------------------ single statements and tells
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
    ok("no_basis_licensed", not any("page weight" in " ".join(x.split()).lower() for x in allt.values()))
    sp = L["spine"]
    mc = pd.to_datetime(sp.ts_utc).dt.month.value_counts()
    ok("tell.row_counts_vary", mc.nunique() == len(mc))
    co = L["closeout"]
    ok("tell.closeout_not_round", not any(float(x) == round(float(x)) for x in co["Share over line (%)"]))
    ok("assertions>=40", COUNT[0] >= 40, COUNT[0])
    REC["n_assertions"] = COUNT[0]
    print(f"checks: {COUNT[0]} assertions passed")
    return REC


def _overclean_T(L, v):
    x = v.assign(dd=v.day.dt.strftime("%Y-%m-%d"))
    x = x.sort_values(["device_key", "ts"], kind="stable").drop_duplicates(["device_key", "url_path", "dd"])
    return {k: G.dated(x, L, k) for k in "DBE"}
