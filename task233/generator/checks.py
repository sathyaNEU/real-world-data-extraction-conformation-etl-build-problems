"""task233 checks: the three rules executed (R1 to R3c), every semantic fork row (SF1 to SF15), the margins, the rungs,
the ask devices and their stops, the separation of the call from the devices, and the input gates."""
import os
import re

import numpy as np
import pandas as pd

import estim as E
import params as P

N = [0]


def ok(cond, label):
    assert cond, label
    N[0] += 1


def flags_of(f26, Ex, dists):
    return {(d, s): E.flag(E.shifts(f26, Ex, s, d, which="golden")["golden"]) for d in dists for s in E.STATS}


def run(target, golden, o, R, A):
    N[0] = 0
    T, f26, f25, cal, Ex, dists = R["T"], R["f26"], R["f25"], R["cal"], R["E"], R["dists"]
    gold = {(c["district"], c["stat"]): c["flag"] for c in R["cells"]}
    names = T["name"]

    # ------------------------------------------------------------ R1: the field's raw material ships, no deciding column
    cols = sum((list(T[k].columns) for k in ("f26", "f25", "fu", "xw", "codes", "pts")), [])
    ok(not any(re.search(r"shift|flag|odds|sensitiv|depart", c, re.I) for c in cols), "R1 no shipped column holds a shift, flag or odds ratio")
    ok(f26["nonresp"].sum() > 5000 and all(f26.loc[f26["nonresp"], "alloc_" + s].notna().all() for s in E.STATS),
       "R1 each 2026 nonrespondent's allocation ships at the leaver grain")
    ok(len(cal) == Ex["neet"]["n"] and len(cal) > 2000, "R1 the follow-up ships case by case and the golden reads it")

    # ------------------------------------------------------------ the golden grid, its counts and its margins
    counts = {k: sum(v == k for v in gold.values()) for k in ("Standard", "Caution", "Suppressed")}
    ok(counts == {"Standard": 5, "Caution": 14, "Suppressed": 5}, "golden counts %s" % counts)
    exp_sup = {("ED03", "neet"), ("ED02", "neet"), ("ED01", "neet"), ("ED09", "he"), ("ED10", "he")}
    exp_std = {("ED06", "neet"), ("ED08", "neet"), ("ED07", "neet"), ("ED04", "he"), ("ED12", "he")}
    ok({k for k, v in gold.items() if v == "Suppressed"} == exp_sup, "golden suppressions by name")
    ok({k for k, v in gold.items() if v == "Standard"} == exp_std, "golden standard flags by name")
    for c in R["cells"]:
        for k in E.GOLD_VARIANTS:
            ok(E.flag(c["all"][k]) == c["flag"], "convergence %s %s %s" % (c["district"], c["stat"], k))
        ok(min(E.margin(c["all"][k]) for k in E.GOLD_VARIANTS) >= 0.22, "golden margin %s %s" % (c["district"], c["stat"]))
        ok(E.margin(c["default"]) >= 0.15, "default margin %s %s" % (c["district"], c["stat"]))
        ok(E.flag(c["all"]["quadratic_points"]) == c["flag"] and E.flag(c["all"]["probit"]) == c["flag"],
           "quadratic and probit agree %s %s" % (c["district"], c["stat"]))

    # ------------------------------------------------------------ R3a: the analyst test on the clean truth
    W = o["W"]
    world = {}
    for s, k in (("neet", 4), ("he", 0)):
        p = np.concatenate([np.round(W.y25[d]["alloc"][W.y25[d]["traced"], k], 4) for d in P.TRACED])
        a = np.concatenate([(W.y25[d]["cat"][W.y25[d]["traced"]] == k).astype(float) for d in P.TRACED])
        world[s] = dict(gap=a.mean() - p.mean(), delta=E._offset(p, a))
        ok(abs(world[s]["gap"] - Ex[s]["gap"]) < 1e-9 and abs(world[s]["delta"] - Ex[s]["delta"]) < 1e-9,
           "R2 the shipped follow-up gives the clean truth's departure exactly (%s)" % s)
    clean_default = {}
    for d in range(P.ND):
        c = W.y26[d]; u = c["unk"]
        for s in ("neet", "he"):
            clean_default[(P.CODE[d], s)] = E.flag(u.sum() * world[s]["gap"] / c["n"] * 100)
    wrong = {k for k in gold if clean_default[k] != gold[k]}
    ok(len(wrong) == 11, "R3a the default path on the clean truth files eleven wrong flags (%d)" % len(wrong))
    ok(wrong == {("ED06", "neet"), ("ED08", "neet"), ("ED07", "neet"), ("ED09", "neet"), ("ED10", "neet"), ("ED02", "neet"),
                 ("ED01", "neet"), ("ED09", "he"), ("ED10", "he"), ("ED04", "he"), ("ED12", "he")}, "R3a the eleven by name")
    ok(all(clean_default[k] == "Suppressed" for k in (("ED09", "neet"), ("ED10", "neet"))) and
       all(clean_default[k] == "Caution" for k in (("ED09", "he"), ("ED10", "he"), ("ED01", "neet"), ("ED02", "neet"))),
       "R3a the default suppresses Hill Country's and Northern Plains' NEET rates and misses every higher-education suppression")
    ok(all(c["default_flag"] == clean_default[(c["district"], c["stat"])] for c in R["cells"]), "R3a shipped default equals clean default")

    # ------------------------------------------------------------ R3b: the decisive step alone, and each lower rung alone
    for d in range(P.ND):
        c = W.y26[d]; u = c["unk"]
        for s, k in (("neet", 4), ("he", 0)):
            p = np.round(c["alloc"][u, k], 4)
            v = (E.expit(E.logit(E.CL(p)) + world[s]["delta"]) - p).sum() / c["n"] * 100
            ok(E.flag(v) == gold[(P.CODE[d], s)], "R3b the scale alone files the golden %s %s" % (P.CODE[d], s))
    for k, n in (("band_points", 11), ("ratio", 2), ("clipped_points", 9), ("band_ratio", 2)):
        miss = sum(E.flag(c["all"][k]) != c["flag"] for c in R["cells"])
        ok(miss == n, "R3b rung %s alone stays wrong in %d cells (%d)" % (k, n, miss))
    for k in ("analog", "linear_points"):
        ok(all(E.flag(c["all"][k]) == c["flag"] for c in R["cells"]), "allocation-conditioned route %s agrees with the golden" % k)
    for s in E.STATS:
        L = Ex[s]["ll"]; best = L["odds ratio, pooled (1 parameter)"]
        for k in ("points gap, pooled (1)", "ratio of rates, pooled (1)", "points gap, by band (4)", "ratio of rates, by band (4)"):
            ok(best - L[k] >= 8.0, "the follow-up rejects %s against one odds ratio (%s: %.1f)" % (k, s, best - L[k]))
        ok(L["odds ratio, by band (4)"] - best < 3.0, "band odds ratios add nothing to one odds ratio (%s)" % s)
    dev = {s: Ex[s]["dev"] for s in E.STATS}
    for s in E.STATS:
        ok(dev[s]["odds"] + 10 < dev[s]["points"] and dev[s]["odds"] + 10 < dev[s]["ratio"] and dev[s]["odds"] + 10 < dev[s]["linear"],
           "the follow-up rejects points, ratio and line against the odds scale (%s)" % s)
        ors = [c["odds_ratio"] for c in Ex[s]["cells"]]; gaps = [c["gap"] for c in Ex[s]["cells"]]
        ok(max(abs(np.array(gaps))) - min(abs(np.array(gaps))) > 0.10, "the points gap moves across cells (%s)" % s)

    # ------------------------------------------------------------ R2: each Layer 1 item, mishandled, leaves the call
    codes_scr = T["f26"].copy(); codes_scr["activity_code"] = codes_scr["activity_code"][::-1].to_numpy()
    codes_scr["attainment_band"] = codes_scr["attainment_band"].sample(frac=1, random_state=1).to_numpy()
    T2 = dict(T, f26=codes_scr)
    f26b, _, _ = E.conform(T2)
    ok(flags_of(f26b, Ex, dists) == gold, "R2 SF1 SF2 separation: activity codes and bands scrambled, every flag unchanged")
    f26m, f25m, calm = E.conform(T, map26="district_2025")
    ok(set(f26m["district"]) == set(dists) and flags_of(f26m, Ex, dists) == gold, "R2 SF3 the 2025 map, every flag unchanged")
    fu_all = T["fu"][T["fu"]["outcome_code"] != "F99"]
    xw = T["xw"].copy(); xw["leaver_ref"] = "L" + xw["leaver_ref"]
    caldup = fu_all.merge(xw, on="case_no").merge(f25, on="leaver_ref"); caldup = caldup[caldup["nonresp"]].copy()
    caldup["found"] = caldup["outcome_code"].map(E.FIELD)
    ok(len(caldup) > len(cal), "R2 SF10 duplicate route rows exist")
    Ed = E.departure(caldup, f25)
    ok(flags_of(f26, Ed, dists) == gold, "R2 SF10 each route row counted, every flag unchanged")
    raw = T["fu"].merge(T["xw"], on="case_no").merge(f25, on="leaver_ref")
    ok(len(raw) == 0, "R2 SF15 the raw reference join matches no case")
    allres = T["fu"][T["fu"]["outcome_code"] != "F99"].drop_duplicates("case_no").merge(xw, on="case_no").merge(f25, on="leaver_ref")
    ok(len(allres) == T["fu"][T["fu"]["outcome_code"] != "F99"]["case_no"].nunique(), "R2 SF15 every resolved case matches after normalisation")
    late = allres[~allres["nonresp"]]
    ok(len(late) > 100 and late[["alloc_neet", "alloc_he"]].isna().all().all(), "R2 SF9 late returners carry no allocation (cannot be compared)")
    ok(set(T["fu"][T["fu"]["outcome_code"] == "F99"]["resolved_on"]) == {""}, "R2 SF9 unresolved cases carry no outcome")

    # ------------------------------------------------------------ semantic forks
    ok(((f26["return_form"] == "") == f26["alloc_neet"].notna()).all(), "SF5 allocation present exactly where no form returned")
    # SF4: respondents-only denominator moves flags (ruled out by QS-4 s.2)
    alt = {}
    for d in dists:
        g = f26[f26["district"] == d]; nr = g[g["nonresp"]]; Nr = (~g["nonresp"]).sum()
        for s in E.STATS:
            p = nr["alloc_" + s].to_numpy(float)
            alt[(d, s)] = E.flag((E.expit(E.logit(E.CL(p)) + Ex[s]["delta"]) - p).sum() / Nr * 100)
    ok(alt != gold, "SF4 the respondents-only denominator moves a flag (QS-4 s.2 rules it out)")
    # SF6: current-year shares as the allocation leave every flag
    fb = E.final_band(T); g26 = f26.copy(); g26["fb"] = g26["leaver_ref"].map(fb); g26["dest"] = E.destinations(g26, T, True)
    shares = {}
    for (d, b), g in g26[~g26["nonresp"]].groupby(["district", "fb"]):
        shares[(d, b)] = {s: (g["dest"] == E.STATS[s]).mean() for s in E.STATS}
    g26b = g26.copy()
    for s in E.STATS:
        g26b.loc[g26b["nonresp"], "alloc_" + s] = [shares[(d, b)][s] for d, b in zip(g26b.loc[g26b["nonresp"], "district"], g26b.loc[g26b["nonresp"], "fb"])]
    ok(flags_of(g26b, Ex, dists) == gold, "SF6 current-year shares as the allocation, every flag unchanged")
    # SF7: signed bands would flag every HE rate standard (QS-4 s.4 bands the size)
    ok(any(c["shift"] < -1.0 for c in R["cells"] if c["stat"] == "he"), "SF7 HE shifts are negative, so a signed reading moves flags; QS-4 s.4 bands the size")
    ok(len(T["fu"]["case_no"].unique()) == A["drawn"], "SF8 one follow-up, every drawn case in the outcomes file")
    ok(sum(E.flag(c["all"]["district_mean_odds"]) != c["flag"] for c in R["cells"]) >= 1, "SF11 the district-mean application moves a flag (QS-4 s.3 rules it out)")
    ok(all(min(E.margin(c["all"][k]) for k in E.GOLD_VARIANTS) >= 0.2 for c in R["cells"]), "SF12 SF13 no shift within 0.2 of an edge")
    ok(all(E.flag(round(c["shift"], 1)) == c["flag"] for c in R["cells"]), "SF12 rounding before banding leaves every flag")
    ok(len([f for f in os.listdir(target) if "frame_2026" in f]) == 1, "SF14 one 2026 frame")
    ok(all(isinstance(f["rate"], float) for f in A["flags"] if f["flag"] == "Suppressed"), "SF16 a suppressed statistic's headline rate is computed (QS-4 s.2)")
    b7 = T["f26"][T["f26"]["form_build"].str.startswith("7.")]
    ok(len(b7) > 1000 and not (b7["activity_code"] == "8").any() and (T["f25"]["form_build"].str.startswith("7.") | (T["f25"]["form_build"] == "")).all(),
       "SF17 build-7 returns carry no code 8 and every 2025 online return is build 7: build 7 is the 2025 edition")

    # ------------------------------------------------------------ the asks
    for d, a in R["A"].items():
        for s in E.STATS:
            ok(abs(a["right"][s] - a["natural"][s]) >= 0.06, "ask A device moves %s %s" % (d, s))
            ok(_edge(a["right"][s]) >= 0.02, "ask A mid-bin %s %s" % (d, s))
    for b, q in R["B"].items():
        ok(q["leavers"] != q["frame_leavers"], "ask B band counts move %s" % b)
        for s in E.STATS:
            for stop in ("frame_band", "natural", "final_natural"):
                ok(abs(q["right"][s] - q[stop][s]) >= 0.06, "ask B stop %s %s %s" % (stop, b, s))
            ok(_edge(q["right"][s]) >= 0.02, "ask B mid-bin %s %s" % (b, s))
    ok(sum(q["leavers"] for q in R["B"].values()) == len(f26), "ask B bands cover every leaver")

    # ------------------------------------------------------------ R3c, input gates, hygiene
    for k in ("f26", "f25"):
        blocks = T[k].drop(columns=["leaver_ref", "returned_at"]).groupby("school_code").apply(
            lambda g: tuple(sorted(map(tuple, g.astype(str).to_numpy().tolist()))), include_groups=False)
        ok(blocks.is_unique, "R3c no school's block of rows repeats another's in %s" % k)
        ok(T[k]["leaver_ref"].is_unique, "leaver references unique in %s" % k)
    files = os.listdir(target)
    ok(len(files) >= 10 and len({f.rsplit(".", 1)[1] for f in files}) >= 3, "input gates: files and formats")
    ok(max(sum(1 for _ in open(os.path.join(target, f))) for f in files if f.endswith(".csv")) >= 25001, "input gate: a file of 25,000 rows")
    ok(T["f26"]["returned_at"].replace("", "0").max() <= "2026-10-30T17:00:00Z", "every 2026 return before the close")
    ok(T["f25"]["returned_at"].replace("", "0").max() <= "2026-03-31", "2025 late returns before the final file")
    for f in ("submission.md",):
        ok("\u2014" not in open(os.path.join(os.path.dirname(target), f)).read(), "no em dash in %s" % f)
    return N[0]


def _edge(x):
    s = x * 10; return abs((s - np.floor(s)) - 0.5) / 10
