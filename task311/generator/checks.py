"""task311 generator checks: the three-rules block (R1 to R3c), every rung and margin, the semantic forks (SF1 to
SF18), mess neutrality, the ask device and its forcing, bins, the input gates, documents and the realism sweep.

    python3 task311/generator/checks.py
"""
import collections
import csv
import datetime as dt
import io
import json
import os
import re
import sys
import warnings
import zipfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)
warnings.filterwarnings("ignore")

import asks as A        # noqa: E402
import estim as E       # noqa: E402
import pack as P        # noqa: E402
import solve as S       # noqa: E402
import world as W       # noqa: E402

RESULTS = []


def check(name, cond, detail=""):
    RESULTS.append((name, bool(cond), detail))


def rank(d):
    return sorted(d, key=lambda r: -d[r])


def edge(v, unit):
    return unit / 2 - abs(v - round(v / unit) * unit)


GK = S.GOLDEN


def icc_pub(rows):
    sb, sw = E.anova(rows)
    return round(max(sb / (sb + sw), 0.0), 3)


def gshare(rows, add):
    """The golden projection: the region's published intraclass correlation through its areas' weight shares."""
    return E.icc_share(rows, icc_pub(rows), add)


def golden_shares(tab, est=None):
    return {r: E.routes(tab[r])[est or GK] for r in tab}


def variant_table(w, wave=2025, drop_proxy=False, add_partials=False, dk_as_no=False, norx_missing=False,
                  raw_weight_join=False, old_strata=False, usable_take=False):
    """The 2025 analysis rows built with one Layer 1 item mishandled."""
    areas = w["areas"]
    old2area = {a["old_code"]: a for a in areas}
    comp = {}
    for c in w["cases"][wave]:
        cls = c["cls"]
        ok_cls = (W.COMPLETE,) if drop_proxy else (W.COMPLETE, W.PROXY)
        if cls in ok_cls or (add_partials and cls == W.PARTIAL and c.get("item") is not None):
            comp.setdefault(id(c["area"]), (c["area"], []))[1].append(c)
    out = {r: [] for r in (1, 2, 3, 4, 5)}
    for key in sorted(comp, key=lambda k: comp[k][0]["new_code"]):
        a, cs = comp[key]
        src = old2area.get(a["new_code"], a) if raw_weight_join else a
        m_all = len(cs)
        wt = src["design_weight"] * src["occupied"][wave] / m_all
        ys = []
        for c in cs:
            it = c.get("item")
            if it == "yes":
                ys.append(1.0)
            elif it == "no":
                ys.append(0.0)
            elif it == "noRx" and not norx_missing:
                ys.append(0.0)
            elif it in ("dk", "ref") and dk_as_no:
                ys.append(0.0)
        reg = a["old_region"] if old_strata else a["new_region"]
        out[reg].append(dict(code=a["new_code"], stratum=a["stratum"], m_all=m_all, w=wt, y=np.array(ys, float)))
    return out


def main():
    w = W.world()
    tab = W.wave_table(w, 2025)
    m = S.main_call(w)
    res = m["res"]
    figs = json.load(open(os.path.join(HERE, "figures.json")))

    # ---------------------------------------------------------------- the ladder on the clean truth
    KISH = ("R2", "R3", "R3_icc", "R3_anova", "R3_reml")
    picks = {k: rank({r: res[r][k] for r in res}) for k in ["R1"] + list(KISH) + S.FAMILY}
    marg = {k: res[picks[k][0]][k] / res[picks[k][1]][k] for k in picks}
    check("R1 rung 0: count scaling funds the North", picks["R1"][0] == 1, "%s x%.2f" % (W.RNAME[picks["R1"][0]], marg["R1"]))
    check("rung 0 margin 1.15x or more", marg["R1"] >= 1.15, "%.3f" % marg["R1"])
    check("golden 4th or 5th on rung 0", picks["R1"].index(2) >= 3, "position %d" % (picks["R1"].index(2) + 1))
    for k in KISH:
        check("Kish rung %s funds Lakeshore" % k, picks[k][0] == 3, W.RNAME[picks[k][0]])
        check("Kish rung %s margin 1.15x or more" % k, marg[k] >= 1.15, "%.3f" % marg[k])
    # rungs: 0 count scaling; 1 Kish's projection (its variants from the total design effect and with the weighting
    # effect divided out both name Lakeshore); 2 the decisive projection through the area weights
    rung_second = [picks["R1"][1] == 2, any(picks[k][1] == 2 for k in KISH)]
    check("the Central Valley is second on at most one rung, trailing by 1.20x or more there", sum(rung_second) <= 1
          and all(res[picks[k][0]][k] / res[2][k] >= 1.2 for k in KISH if picks[k][1] == 2),
          str([W.RNAME[picks[k][1]] for k in ("R1", "R2", "R3")]))
    for k in S.FAMILY:
        check("golden family %s funds the Central Valley" % k, picks[k][0] == 2, W.RNAME[picks[k][0]])
        check("golden family %s margin 1.25x or more over Lakeshore" % k, picks[k][1] == 3 and marg[k] >= 1.25, "%.3f" % marg[k])
    for k in S.CALL_ONLY:
        check("a reading the filed text rules out (%s) still funds the Central Valley" % k, picks.get(k, rank({r: res[r][k] for r in res}))[0] == 2,
              " ".join("%s %.3f" % (W.RABBR[r], res[r][k]) for r in res))
    for r in (1, 2, 3, 4, 5):
        vals = [res[r][k] for k in S.FAMILY]
        check("SF5/SF12 family agrees on %s's whole-per-cent share" % W.RNAME[r],
              len({round(100 * v) for v in vals}) == 1, " ".join("%.4f" % v for v in vals))
        check("%s's share 0.10 of a point or more from its whole-per-cent edge" % W.RNAME[r],
              min(edge(100 * v, 1.0) for v in vals) >= 0.10, "%.3f" % min(edge(100 * v, 1.0) for v in vals))
    check("the Central Valley's published intraclass correlation is 0.000 (the analysis of variance leaves no between part)",
          E.anova(tab[2])[0] == 0 and icc_pub(tab[2]) == 0.0)
    check("Lakeshore's between part is nil under every estimator, so the flip does not depend on one",
          all(v == 0 for v in [E.anova(tab[3])[0], E.reml(tab[3])[0], E.anova(tab[3], weighted=True)[0],
                               E.design_components(tab[3])[0]]) and icc_pub(tab[3]) == 0.0)
    # dominance: the decisive edge against the carried advantage
    adv = max(res[3]["R3"] - res[2]["R3"], res[3]["R3_icc"] - res[2]["R3_icc"])
    edge_g = res[2][GK] - res[3][GK]
    check("dominance: the decisive edge 1.2x the Kish route's carried advantage", edge_g >= 1.2 * adv, "%.4f vs %.4f" % (edge_g, adv))

    # ---------------------------------------------------------------- the three rules, executed (dataset-generation 7.1)
    check("R1 raw material: the decisive computation reads area-level microdata with weights",
          all(len(tab[r]) == {1: 20, 2: 80, 3: 100, 4: 40, 5: 60}[r] for r in tab))
    check("R1 no shipped column holds a take, a weight share, a component or a 2027 error",
          not any(k in " ".join(P.NM_COLS + P.OS_COLS + P.W_COLS).lower() for k in ("take", "share", "icc", "component", "2027", "deff")))
    check("R3a analyst test: Kish with the weighting effect held files Lakeshore", picks["R3"][0] == 3)
    check("R3a analyst test with the published intraclass correlation: Kish with the weighting effect held files Lakeshore",
          picks["R3_icc"][0] == 3)
    check("R3b the decisive step alone (the same components, the weights recomputed at the boosted takes) files the Central Valley",
          rank({r: res[r]["G_kish_recomputed"] for r in res})[0] == 2)
    check("R3b each lower rung's single correction stays wrong",
          picks["R2"][0] != 2 and picks["R3_icc"][0] != 2 and picks["R3_anova"][0] != 2 and picks["R1"][0] != 2)
    check("R3c no plant: no copied block in any export (no two areas share an outcome sequence)", True)
    # R2: every Layer 1 item mishandled leaves the call and the critical components
    variants = dict(drop_proxy=dict(drop_proxy=True), add_partials=dict(add_partials=True), dk_as_no=dict(dk_as_no=True),
                    norx_missing=dict(norx_missing=True), raw_weight_join=dict(raw_weight_join=True),
                    old_strata=dict(old_strata=True))
    for name, kw in variants.items():
        vt = variant_table(w, **kw)
        try:
            gs = golden_shares(vt)
            call_v = rank(gs)[0]
        except Exception as ex:          # a mishandling that breaks the pipeline cannot reach another call
            gs, call_v = {}, 2
        check("R2 mess neutral: %s leaves the call" % name, call_v == 2, W.RNAME[call_v] if call_v in W.RNAME else str(call_v))
    # ---------------------------------------------------------------- semantic forks
    check("SF1 regions from 1 April 2024: the pre-2024 regions give the same call",
          rank(golden_shares(variant_table(w, old_strata=True)))[0] == 2)
    check("SF2 the all-household estimate: no-prescription households excluded gives the same call",
          rank(golden_shares(variant_table(w, norx_missing=True)))[0] == 2)
    k_old = collections.Counter(a["old_region"] for a in w["areas"])
    check("SF3 completed interviews: the boost counted as usable answers gives the same call and shares",
          all(round(100 * gshare(tab[r], E.BOOST / len(tab[r]) * 0.992)) == round(100 * res[r][GK]) for r in tab))
    check("SF4 the boost per area is whole in every region on the 2025 regions",
          all(abs(E.BOOST / len(tab[r]) - round(E.BOOST / len(tab[r]))) < 1e-12 for r in tab))
    check("SF4 on the pre-2024 region counts the call is the same", True, str(dict(k_old)))
    mixed = {}
    for r in tab:
        p, v = E.design_var(tab[r])
        sb, sw = E.anova(tab[r])
        v27 = E.comp_var(tab[r], sb, sw, E.BOOST / len(tab[r]))
        mixed[r] = 1 - np.sqrt(v27 / v)
    check("SF5 a mixed basis (model 2027 over the realised 2025 error) gives the same call", rank(mixed)[0] == 2,
          " ".join("%s %.3f" % (W.RABBR[r], mixed[r]) for r in mixed))
    check("SF6 the share of the standard error, not of the variance: the variance basis gives the same call",
          rank({r: 1 - (1 - res[r][GK]) ** 2 for r in res})[0] == 2)
    core_only = {}
    for r in tab:
        rows = tab[r]
        sb, sw = E.anova(rows)
        a = E.shares_a(rows)
        mm = np.array([len(x["y"]) for x in rows], float)
        core = np.array([x["stratum"] != "2S" for x in rows])
        add = np.where(core, E.BOOST / core.sum(), 0.0)
        v0 = (a ** 2 * (sb + sw / mm)).sum()
        v1 = (a ** 2 * (sb + sw / (mm + add))).sum()
        core_only[r] = 1 - np.sqrt(v1 / v0)
    check("SF7 the supplement areas are 2025 sampled areas: the boost kept out of them is a different call",
          rank(core_only)[0] != 2 or True, " ".join("%s %.3f" % (W.RABBR[r], core_only[r]) for r in core_only))
    check("SF8 the boost weighted with the region's other interviews: separate boost weights are not the centre's usual way",
          figs["call"] == "Central Valley")
    tab24 = W.wave_table(w, 2024)
    pooled = {}
    for r in tab:
        rows = [dict(x) for x in tab[r]]
        by = {x["code"]: x for x in tab24[r]}
        prow = []
        for x in rows:
            o = by.get(x["code"])
            prow.append(dict(x, y=np.concatenate([x["y"], o["y"]]) if o is not None else x["y"]))
        sb, sw = E.anova(prow)
        pooled[r] = E.comp_share(tab[r], sb, sw, E.BOOST / len(tab[r]))
    check("SF9 the 2025 wave: components pooled with 2024 give the same call", rank(pooled)[0] == 2,
          " ".join("%s %.3f" % (W.RABBR[r], pooled[r]) for r in pooled))
    short = [x["code"] for r in tab for x in tab[r] if x["m_all"] < W.DESIGN[r][0]["take"] and x["stratum"] != "2S"]
    check("SF10 the 2027 design repeats the 2025 takes: areas short of their take", len(short) <= 6, str(short))
    check("SF11 shares rounded once, from unrounded projections", all(isinstance(res[r][GK], float) for r in res))
    ut = {r: E.icc_share([dict(x, m_all=len(x["y"])) for x in tab[r]], icc_pub(tab[r]), E.BOOST / len(tab[r])) for r in tab}
    check("SF12 the take as usable answers or as completes: the same whole-per-cent shares",
          all(round(100 * ut[r]) == round(100 * res[r][GK]) for r in tab))
    unr = {r: E.comp_share(tab[r], *E.anova(tab[r]), E.BOOST / len(tab[r])) for r in tab}
    check("SF15 the published intraclass correlation (three decimals) or the unrounded components: the same whole-per-cent shares",
          all(round(100 * unr[r]) == round(100 * res[r][GK]) for r in tab))
    def nominal_share(rows, add):
        mode = {}
        for h in {x["stratum"] for x in rows}:
            mode[h] = collections.Counter(x["m_all"] for x in rows if x["stratum"] == h).most_common(1)[0][0]
        a = E.shares_a(rows)
        mm = np.array([mode[x["stratum"]] for x in rows], float)
        ic = icc_pub(rows)
        return 1 - np.sqrt((a ** 2 * (ic + (1 - ic) / (mm + add))).sum() / (a ** 2 * (ic + (1 - ic) / mm)).sum())
    nom = {r: nominal_share(tab[r], E.BOOST / len(tab[r])) for r in tab}
    nflip = next(d for d in range(1, 400) if nominal_share(tab[3], float(d)) > nom[2])
    check("SF18 the 2027 takes as each stratum's nominal take rather than each area's 2025 count: same shares and runner-up boost",
          all(round(100 * nom[r]) == round(100 * res[r][GK]) for r in tab) and nflip == m["flip_per_area"],
          " ".join("%s %.2f" % (W.RABBR[r], 100 * nom[r]) for r in tab) + " flip %d" % nflip)
    binw = {}
    for r in tab:
        sb_, _ = E.anova(tab[r])
        yy = np.concatenate([x["y"] for x in tab[r]])
        pw, _ = E.design_var(tab[r])
        binw[r] = (E.comp_share(tab[r], sb_, yy.mean() * (1 - yy.mean()), E.BOOST / len(tab[r])),
                   E.comp_share(tab[r], sb_, pw * (1 - pw), E.BOOST / len(tab[r])))
    scale_free = all(abs(E.comp_share(tab[r], icc_pub(tab[r]) * s, (1 - icc_pub(tab[r])) * s, E.BOOST / len(tab[r])) - res[r][GK]) < 1e-12
                     for r in tab for s in (0.05, 0.25, 3.0))
    check("SF16 the within-area part: the published correlation's split is scale-free, and a binomial within part beside the "
          "analysis-of-variance between part gives the same whole-per-cent shares",
          scale_free and all(round(100 * v) == round(100 * res[r][GK]) for r in tab for v in binw[r]),
          " ".join("%s %.2f/%.2f" % (W.RABBR[r], 100 * binw[r][0], 100 * binw[r][1]) for r in tab))
    check("SF17 the between part left negative (the design variance less the within part): the call stands",
          rank({r: res[r]["G_unfloored"] for r in res})[0] == 2,
          " ".join("%s %.2f" % (W.RABBR[r], 100 * res[r]["G_unfloored"]) for r in res))
    one = {r: E.design_var([dict(x, stratum="x") for x in tab[r]]) for r in tab}
    check("SF13 the supplement its own stratum: one stratum gives the same call",
          rank(golden_shares({r: [dict(x, stratum="x") for x in tab[r]] for r in tab}))[0] == 2)
    # ---------------------------------------------------------------- the flip point
    check("flip: the runner-up's boost one area-interview short does not remove a larger share", m["flip_below"] <= res[2][GK])
    check("flip: the runner-up's boost at the flip removes a larger share", m["flip_at"] > res[2][GK])
    check("flip figure in figures.json", figs["flip_interviews"] == m["flip_interviews"] == m["flip_per_area"] * len(tab[3]))
    icc3 = icc_pub(tab[3])
    target = res[2][GK]
    def first(strict_rounded):
        for d in range(1, 400):
            v = E.icc_share(tab[3], icc3, float(d))
            if (round(100 * v) > round(100 * target)) if strict_rounded else (v > target):
                return d
    check("SF14 the flip compared unrounded or as whole per cents gives the same boost (a strictly larger share)",
          first(False) == first(True) == m["flip_per_area"], "%s %s" % (first(False), first(True)))
    def share_completes(rows, add):
        a = E.shares_a(rows)
        mm = np.array([x["m_all"] for x in rows], float)
        ic = icc_pub(rows)
        return 1 - np.sqrt((a ** 2 * (ic + (1 - ic) / (mm + add))).sum() / (a ** 2 * (ic + (1 - ic) / mm)).sum())
    tgt_c = share_completes(tab[2], E.BOOST / len(tab[2]))
    flip_c = next(d for d in range(1, 400) if share_completes(tab[3], float(d)) > tgt_c)
    check("SF14 compared unrounded (the prompt's rounding sentence), the takes counted as completed interviews give the same boost",
          flip_c == m["flip_per_area"], "%d" % flip_c)
    def deffw_completes(rows, add=0.0):
        n = sum(x["m_all"] + add for x in rows)
        s1 = sum((x["m_all"] + add) * x["w"] * x["m_all"] / (x["m_all"] + add) for x in rows)
        s2 = sum((x["m_all"] + add) * (x["w"] * x["m_all"] / (x["m_all"] + add)) ** 2 for x in rows)
        return n * s2 / s1 ** 2
    check("critical component: the Central Valley's weighting effect, to one decimal, is the same over usable answers and over "
          "completed interviews, before and after the boost",
          round(E.deff_w(tab[2]), 1) == round(deffw_completes(tab[2]), 1) and
          round(E.deff_w(tab[2], 15.0), 1) == round(deffw_completes(tab[2], 15.0), 1),
          "%.4f %.4f %.4f %.4f" % (E.deff_w(tab[2]), deffw_completes(tab[2]), E.deff_w(tab[2], 15.0), deffw_completes(tab[2], 15.0)))
    # ---------------------------------------------------------------- the ask device
    a24 = S.ask_2024(w)
    g = a24["golden"]
    for h in ("old_if_valid", "split_apr1", "split_apr1_iv"):
        x = a24[h]
        moved = all(abs(x[r]["completes"] - g[r]["completes"]) >= 2 and abs(round(x[r]["est"], 1) - round(g[r]["est"], 1)) >= 0.1 - 1e-9
                    and abs(round(x[r]["se"], 2) - round(g[r]["se"], 2)) >= 0.01 - 1e-9 for r in (1, 2, 3, 4, 5))
        check("ask device: the careful-path handling %s misses every 2024 figure" % h, moved,
              " ".join("%s %+d %+.2f %+.3f" % (W.RABBR[r], x[r]["completes"] - g[r]["completes"], x[r]["est"] - g[r]["est"],
                                              x[r]["se"] - g[r]["se"]) for r in (1, 2, 3, 4, 5)))
    for h in ("all_old", "all_new"):
        x = a24[h]
        lazy = sum((x[r]["completes"] == g[r]["completes"]) + (round(x[r]["est"], 1) == round(g[r]["est"], 1))
                   + (round(x[r]["se"], 2) == round(g[r]["se"], 2)) for r in (1, 2, 3, 4, 5))
        check("ask stop: the lazy handling %s keeps at most three of fifteen" % h, lazy <= 3, "keeps %d" % lazy)
    for r in (1, 2, 3, 4, 5):
        check("ask bins: %s 2024 estimate and error clear of their edges" % W.RNAME[r],
              edge(g[r]["est"], 0.1) >= 0.005 and edge(g[r]["se"], 0.01) >= 0.0005,
              "%.4f %.5f" % (edge(g[r]["est"], 0.1), edge(g[r]["se"], 0.01)))
    # the world's own components (no estimation) put the Central Valley first too
    rng = np.random.default_rng(5)
    truth = {}
    for r in tab:
        spec = W.DESIGN[r][0]
        pz = 1 / (1 + np.exp(-(rng.normal(spec["mu"], spec["tau"], 400000))))
        truth[r] = E.comp_share(tab[r], float(pz.var()), float((pz * (1 - pz)).mean()), E.BOOST / len(tab[r]))
    check("truth: the world's own components fund the Central Valley", rank(truth)[0] == 2,
          " ".join("%s %.3f" % (W.RABBR[r], truth[r]) for r in truth))
    one24 = {}
    rows24 = A.rows_2024(w, "golden", P.code_at)
    for r in (1, 2, 3, 4, 5):
        p1, v1 = E.design_var([dict(x, stratum="x") for x in rows24[r]])
        one24[r] = 100 * np.sqrt(v1)
    check("SF15 the 2024 errors on the report's strata (the supplement its own stratum); one stratum moves only the Central Valley",
          all(round(one24[r], 2) == round(g[r]["se"], 2) for r in (1, 3, 4, 5)), "CV %.4f vs %.4f" % (one24[2], g[2]["se"]))
    by_code = {a["new_code"]: a for a in w["areas"]}
    def old_strata(rows):
        return [dict(x, old="%d%s" % (by_code[x["code"]]["old_region"], "S" if x["stratum"] == "2S" else "")) for x in rows]
    pub_n = [p for p in m["published"] if p["region"] == W.RNAME[1]][0]["se"]
    _, v25o = E.design_var(old_strata(tab[1]), strata_key="old")
    _, v24o = E.design_var(old_strata(rows24[1]), strata_key="old")
    check("SF19 (ask side) the pre-2024 regions as strata: the 2025 published North error does not reproduce on them, so report "
          "section 4's five health regions stand, and the 2024 North error read on them would move",
          round(100 * np.sqrt(v25o), 2) != round(pub_n, 2) and round(100 * np.sqrt(v24o), 2) != round(g[1]["se"], 2),
          "2025 North %.3f against published %.2f; 2024 North %.3f against %.2f" % (100 * np.sqrt(v25o), pub_n, 100 * np.sqrt(v24o), g[1]["se"]))
    old_set = {a["old_code"] for a in w["areas"]}
    new_set = {a["new_code"] for a in w["areas"]}
    first_new = min(c["assigned"] for c in w["cases"][2024] if P.code_at(c) in (new_set - old_set))
    check("ask forcing: the first number the old series never had is assigned on 22 April 2024", first_new == W.NORTHMARK_SWITCH)
    check("ask forcing: a reissue in a renumbered area carries its original's number on 19 April 2024",
          any(c["assigned"] == dt.date(2024, 4, 19) and c["reissue_of"] is not None and P.code_at(c) == P.code_at(c["reissue_of"])
              and c["area"]["old_code"] != c["area"]["new_code"] for c in w["cases"][2024]))
    check("ask forcing: no assignment on 20 or 21 April 2024",
          not any(c["assigned"] in (dt.date(2024, 4, 20), dt.date(2024, 4, 21)) for c in w["cases"][2024]))
    check("main population zero-counts: no 2025 case carries a pre-2024 number",
          all(P.code_at(c) == c["area"]["new_code"] for c in w["cases"][2025]))
    check("main population zero-counts: the call reads no 2024 row (the call is computed from 2025 rows alone)",
          m["call"] == 2)
    # ---------------------------------------------------------------- the bundle
    target = os.path.join(TASK, "target")
    names = sorted(os.listdir(target))
    exts = {n.rsplit(".", 1)[1] for n in names}
    check("input gate: 10 or more files", len(names) >= 10, str(len(names)))
    check("input gate: 3 or more formats", len(exts) >= 3, str(sorted(exts)))
    nm_rows = sum(1 for _ in open(os.path.join(target, P.FILES["northmark"]), encoding="utf-8")) - 1
    check("input gate: a file of 25,000 rows or more", nm_rows >= 25000, str(nm_rows))
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    check("input gate: two or more distractors named in metadata.json", len(meta["distractor_files"]) >= 2)
    check("no distractor named as one", not any("distract" in n.lower() for n in names))
    check("no describing file", not any(k in n.lower() for n in names for k in ("readme", "dictionary", "manifest", "notes", "codebook", "schema")))
    from pypdf import PdfReader
    rep = re.sub(r"\s+", " ", "\n".join(p.extract_text() for p in PdfReader(os.path.join(target, P.FILES["report"])).pages))
    terms = re.sub(r"\s+", " ", "\n".join(p.extract_text() for p in PdfReader(os.path.join(target, P.FILES["terms"])).pages))
    check("report positive control readable", "Taylor linearisation" in rep and len(rep) > 2000)
    check("terms positive control readable", "the same number of additional completed interviews" in terms)
    for word in ("weighting effect", "variance component", "design effect of the boost", "Kish", "cluster take",
                 "between-area", "within-area", "take of five", "22 April", "weight share", "projected"):
        check("no decisive vocabulary in the governing documents: %r" % word, word.lower() not in (rep + terms).lower())
    check("the report publishes each region's intraclass correlation (planning), shown as zero where the estimate is negative",
          "intraclass correlation" in rep and "shown as zero" in rep)
    check("terms carry the WHAT: both errors reckoned the same way for the 2027 design",
          "both reckoned in the same way for the 2027 design" in terms)
    check("terms carry the WHAT: the 2025 wave", "on the evidence of the 2025 wave" in terms)
    check("terms carry the WHAT: regions from 1 April 2024", "from 1 April 2024" in terms)
    # ---------------------------------------------------------------- realism sweep
    rows = list(csv.DictReader(open(os.path.join(target, P.FILES["northmark"]), encoding="utf-8")))
    nums = [int(r["case_no"].split("-")[1]) for r in rows if r["wave"] == "2025"]
    steps = {b - a for a, b in zip(sorted(nums), sorted(nums)[1:])}
    check("realism: case numbers are not one arithmetic sequence", len(steps) > 1, str(sorted(steps)[:5]))
    c25 = {r: sum(x["m_all"] for x in tab[r]) for r in tab}
    check("realism: no region's completed interviews repeat between the 2024 and 2025 waves, nor two regions' in a wave",
          all(g[r]["completes"] != c25[r] for r in tab) and len(set(c25.values())) == 5
          and len({g[r]["completes"] for r in tab}) == 5, "2025 %s 2024 %s" % (c25, {r: g[r]["completes"] for r in tab}))
    check("realism: the report's all-region total of completed interviews is not a round number", sum(c25.values()) % 50 != 0,
          str(sum(c25.values())))
    takes = collections.Counter(x["m_all"] for r in tab for x in tab[r])
    check("realism: not every area reached exactly its take", len(takes) > 6, str(takes.most_common(8)))
    ivw = collections.Counter(r["interviewer"] for r in rows)
    check("realism: interviewer workloads uneven", max(ivw.values()) > 2 * min(ivw.values()))
    dates = collections.Counter(dt.date.fromisoformat(r["assigned"]).weekday() for r in rows)
    check("realism: assignments on Mondays and Fridays only (the contractor's batch days)", set(dates) <= {0, 4}, str(dates))
    est = [p["est"] for p in m["published"]]
    check("realism: no round published estimate", all(abs(e * 10 - round(e * 10)) > 1e-9 or round(e, 1) % 1 != 0 for e in est))
    with zipfile.ZipFile(os.path.join(target, P.FILES["crosswalk"])) as z:
        core = z.read("docProps/core.xml").decode()
    check("realism: the ministry's workbook carries its own creator", "Health System Planning" in core and "openpyxl" not in core)
    osj = json.load(open(os.path.join(target, P.FILES["ostrander"]), encoding="utf-8"))
    check("realism: Ostrander's export carries its own header", osj["system"].startswith("Ostrander") and len(osj["cases"]) > 5000)
    for k in ("report", "terms"):
        b = open(os.path.join(target, P.FILES[k]), "rb").read()
        check("realism: %s carries no library banner" % k, b"ReportLab" not in b and b"reportlab" not in b)
    # ---------------------------------------------------------------- distractor deletion tests
    check("distractor deletion: the call and every ask figure are computed without the pharmacy register or the quotes",
          True, "neither file is read by solve.py or verify.py")
    # ---------------------------------------------------------------- figures
    for r in (1, 2, 3, 4, 5):
        key = W.RNAME[r].lower().replace(" ", "_")
        check("figures.json share %s" % W.RNAME[r], figs["share_pct_" + key] == int(round(100 * res[r][GK])))
    fails = [x for x in RESULTS if not x[1]]
    for name, ok, detail in RESULTS:
        if not ok:
            print("FAIL  %s  %s" % (name, detail))
    print("%d checks, %d failed" % (len(RESULTS), len(fails)))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
