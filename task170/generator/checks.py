"""task170 checks: the generator's assertions on the built pack (and on the clean truth where a rule says so).

    python3 task170/generator/checks.py task170/target

Every label is printed with PASS or FAIL; exit 1 on any FAIL. Labels R1 to R3c are the client's three rules
(dataset-generation 7.1); SFn are the design note's semantic fork rows."""
from __future__ import annotations

import json
import math
import os
import re
import sys
import zipfile

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc  # noqa: E402
import common as C  # noqa: E402
import docs as DOCS  # noqa: E402
import records as R  # noqa: E402
import world as W  # noqa: E402

RESULTS = []


def check(label, ok, detail=""):
    RESULTS.append((label, bool(ok), detail))
    print("%s  %s  %s" % ("PASS" if ok else "FAIL", label, detail))


def edge(v, unit):
    return unit / 2 - abs(v - round(v / unit) * unit)


def r1000(v):
    return int(round(v / 1000.0)) * 1000


def r100(v):
    return int(round(v / 100.0)) * 100


def after22(G, bu):
    sites = []
    for s in G["sites"]:
        t = dict(s)
        tot = s["b_in"] + s["b_out"]
        t["after22"] = float(tot[4:].sum() / tot.sum())
        sites.append(t)
    qa = calc.q_estimates(sites, "after22")["ivw_origin"]
    tot = G["b_in"] + G["b_out"]
    return bu * qa * float(tot[4:].sum() / tot.sum())


def main(target):
    G = calc.golden(target)
    bu = calc.averted_with(G, 1.0)
    gold = r1000(G["total"])
    F = json.load(open(os.path.join(HERE, "figures.json")))

    # ------------------------------------------------------------------ the call and its bins
    check("call figure", F["call_cases_averted"] == gold, "%d (%.1f)" % (gold, G["total"]))
    check("call mid-bin", edge(G["total"], 1000) >= 0.02 * G["total"], "edge %.1f" % edge(G["total"], 1000))
    check("share mid-bin", edge(100 * G["share"], 1) >= 0.25, "%.3f per cent, edge %.3f" % (100 * G["share"], edge(100 * G["share"], 1)))
    check("per-bite protection mid-bin", edge(G["q"], 0.01) >= 0.003, "%.4f" % G["q"])
    check("in-bed share mid-bin", edge(G["phi"], 0.01) >= 0.0035, "%.4f" % G["phi"])
    for sc in C.SC_CODES:
        v = G["by_sc"][sc]
        check("sub-county %s mid-bin" % sc, edge(v, 100) >= 0.02 * v, "%.1f edge %.1f" % (v, edge(v, 100)))

    # ------------------------------------------------------------------ the golden family (every construction of the decisive step)
    q = calc.q_estimates(G["sites"])
    fam = {"ivw_origin": q["ivw_origin"], "ols_origin": q["ols_origin"], "mean_ratio": q["mean_ratio"],
           "ratio_pooled": q["ratio_pooled"]}
    a, b = q["ols_intercept"]
    fam_tot = {k: bu * v * G["phi"] for k, v in fam.items()}
    fam_tot["ols_intercept"] = bu * (a + b * G["phi"])
    ind2, inb2 = calc.shares_integral(calc.hbs_table(target))
    fam_tot["hour_integral"] = bu * G["q"] * calc.in_bed_share(G["b_in"], G["b_out"], ind2, inb2)
    spread = (max(fam_tot.values()) - min(fam_tot.values())) / G["total"]
    check("SF11 estimators of the per-bite protection agree", all(r1000(v) == gold for v in fam_tot.values()) and spread < 0.01,
          "spread %.2f per cent: %s" % (100 * spread, {k: round(v) for k, v in fam_tot.items()}))
    check("SF7 half-hour against hour-integral shares", r1000(fam_tot["hour_integral"]) == gold, "%.0f" % fam_tot["hour_integral"])
    for sc in C.SC_CODES:
        vals = [G["by_sc"][sc] / G["total"] * v for v in fam_tot.values()]
        check("SF11 sub-county %s holds across the family" % sc, len({r100(v) for v in vals}) == 1, "%s" % sorted({r100(v) for v in vals}))
    check("q intercept near zero", abs(a) < 0.01, "intercept %.4f slope %.4f" % (a, b))

    # ------------------------------------------------------------------ the ladder: every wrong rung outside the bin by the floor
    rungs = {
        "R0 trial pooled efficacy": bu * G["pooled"],
        "R1 pooled efficacy times the county's in-bed share": bu * G["pooled"] * G["phi"],
        "R2 nearest site's efficacy": bu * min(G["sites"], key=lambda s: abs(s["share"] - G["phi"]))["E"],
        "R3 indoor-only in-bed share": bu * calc.q_estimates(G["sites"], "share_in_only")["ivw_origin"] *
        calc.indoor_only_share(G["b_in"], G["b_out"], G["ind"], G["inb"]),
        "R4 indoor share (not in bed)": bu * calc.q_estimates(G["sites"], "share_I")["ivw_origin"] *
        calc.indoor_share(G["b_in"], G["b_out"], G["ind"], G["inb"]),
        "R5 share of bites after 22:00 as the overlap": after22(G, bu),
    }
    lo, hi = gold - 500, gold + 500
    for k, v in rungs.items():
        clear = (lo / v) if v < lo else (v / hi)
        floor = 1.0 if k.startswith("R5") else 1.15   # R5 is a fixed-clock proxy the survey's own bedtimes rule out
        check("ladder %s outside the bin by %.2fx" % (k, floor), r1000(v) != gold and clear >= floor, "%.0f (clearance %.3f)" % (v, clear))

    # ------------------------------------------------------------------ the three rules on the clean truth
    S = W.trial(np.random.default_rng(254))
    clean_share = W.in_bed_share(*W.vector_profile(**W.COUNTY_VECTOR), *W.county_population_shares(np.random.default_rng(9), 40000))
    E_pool_true = 1 - sum(s["cases_n"] for s in S) / sum(s["py_n"] for s in S) / (sum(s["cases_c"] for s in S) / sum(s["py_c"] for s in S))
    check("R1 the field's raw material ships", os.path.getsize(os.path.join(target, "hlc_sentinel_2024_2026.csv")) > 10 ** 6 and
          len(calc.hbs_table(target)) > 3000, "collector-hour catches and person-level survey times")
    txt = re.sub(r"\s+", " ", calc.pdf_text(os.path.join(target, DOCS.F_TRIAL)))
    check("R1 no shipped figure states a site's in-bed share",
          not any(("%.2f" % s["share"]) in txt and ("%.3f" % s["share"]) in txt for s in G["sites"]) and "in-bed share" not in txt.lower(),
          "the trial prints the hourly tables only")
    check("R3a the analyst test on the clean truth files the wrong answer",
          r1000(bu * E_pool_true) != r1000(bu * W.Q * clean_share), "%.0f against %.0f" % (bu * E_pool_true, bu * W.Q * clean_share))
    check("R3b the decisive step alone files the golden on the clean truth", r1000(bu * W.Q * clean_share) == gold,
          "%.0f" % (bu * W.Q * clean_share))
    check("R3b the lower rung alone stays wrong", r1000(bu * E_pool_true * clean_share) != gold, "%.0f" % (bu * E_pool_true * clean_share))
    # mess neutrality, one per item
    b1, b2, _ = calc.hlc_table(target, per_minute=False)
    v = bu * G["q"] * calc.in_bed_share(b1, b2, G["ind"], G["inb"])
    check("R2 catches read per row rather than per minute collected", r1000(v) == gold and abs(v / G["total"] - 1) < 0.005, "%.0f" % v)
    b1, b2, _ = calc.hlc_table(target, species=("an_ruvariensis", "an_tenebrosus"))
    v = bu * G["q"] * calc.in_bed_share(b1, b2, G["ind"], G["inb"])
    check("SF5 R2 every anopheline counted as the vector", r1000(v) == gold, "%.0f" % v)
    df = pd.read_csv(os.path.join(target, "hlc_sentinel_2024_2026.csv"), dtype=str, keep_default_na=False)
    bins = df["hour"].map(calc.hour_bin)
    check("R2 every hour label of the three sheet formats maps to its bin", bins.between(0, 11).all() and bins.nunique() == 12,
          "%d labels" % df["hour"].nunique())
    keep = df[~df["hour"].str.contains("m", regex=False)]
    b1, b2, _ = calc.hlc_table(target)
    dfk = keep[keep["an_ruvariensis"] != ""].copy()
    dfk["bin"] = dfk["hour"].map(calc.hour_bin)
    dfk["pos"] = dfk["position"].str[:2].str.upper().map({"IN": "IN", "OU": "OUT"})
    g = dfk.groupby(["pos", "bin"]).apply(lambda x: x["an_ruvariensis"].astype(int).sum() / x["minutes_collected"].astype(int).sum(), include_groups=False).unstack(0)
    v = bu * G["q"] * calc.in_bed_share(g["IN"].values, g["OUT"].values, G["ind"], G["inb"])
    check("R2 the 12-hour-clock sheets dropped", r1000(v) == gold, "%.0f" % v)
    for label, kw in (("SF8 R2 round 1 only", dict(rounds=(1,))), ("SF8 R2 round 2 only", dict(rounds=(2,))),
                      ("R2 revisited members counted once", dict(first_only=True))):
        h = calc.hbs_table(target, **kw)
        v = bu * G["q"] * calc.in_bed_share(G["b_in"], G["b_out"], *calc.shares(h))
        check(label, r1000(v) == gold, "%.0f" % v)
    pos_ok = set(df["position"]) == {"IN", "OUT", "Indoor", "Outdoor"}
    check("R2 position labels of both sheet eras", pos_ok, str(sorted(set(df["position"]))))
    # R3c no plant: no copied block, nothing written to carry the wrong answer
    keyset = df[["village_code", "night_of", "house", "position", "hour"]].astype(str).agg("|".join, axis=1)
    check("R3c no repeated collector-hour in the catches", keyset.is_unique, "%d rows" % len(df))
    plan_txt = " ".join(DOCS.PLAN_PARAS.values()).lower()
    check("R3c no shipped sentence carries a method for the cases averted",
          not any(w in plan_txt for w in ("efficacy", "protective", "trial", "multiply", "per cent of cases")), "")

    # ------------------------------------------------------------------ semantic forks on the main call
    check("SF1 the population is the residents under a campaign net",
          "counts no cases averted among residents who are not under a campaign net" in DOCS.PLAN_PARAS["impact"], "")
    check("SF2 the window is April to December 2027", sorted({m for (_, m) in G["base"]}) == list(range(4, 13)), "")
    check("SF3 the comparison is the planning baseline without the campaign", "without the LulaNet R campaign" in
          pd.read_excel(os.path.join(target, "obf_planning_baseline_2027.xlsx"), header=None).iloc[0, 0], "")
    check("SF4 use is the plan's Table 2", calc.usage(target) == {m: round(v, 2) for m, v in R.USAGE.items()}, str(calc.usage(target)))
    check("SF6 the trial reports one efficacy per site, nightly use verified", "96 to 98 per cent of checks" in txt, "")
    unrounded = sum(G["by_sc"].values())
    check("SF10 the county figure is the unrounded sum, rounded once", r1000(unrounded) == gold and
          r1000(sum(r100(v) for v in G["by_sc"].values())) == gold, "%.1f" % unrounded)
    check("SF12 the baseline and the trial count confirmed cases", "confirmed" in
          pd.read_excel(os.path.join(target, "obf_planning_baseline_2027.xlsx"), header=None).iloc[0, 0] and "confirmed Ombeni fever" in txt, "")
    check("SF9 per-minute and per-row catch rates agree", True, "asserted under R2 above")

    # ------------------------------------------------------------------ the asks
    nets = calc.nets_needed(target)
    for mode in ("naive", "exact", "dwelling", "idonly"):
        v = calc.nets_needed(target, mode)
        check("ask A device: %s misses every sub-county" % mode, all(v[sc] != nets[sc] for sc in C.SC_CODES),
              "county %d against %d" % (sum(v.values()), sum(nets.values())))
    reg = pd.read_parquet(os.path.join(target, "nets_registration_2026.parquet"))
    truth_rereg = make_truth_rereg()
    mop = reg[reg["round"] == "MOPUP"].drop_duplicates()
    key = ["sub_county", "ward", "dwelling_mark", "usual_members", "under_five", "sleeping_spaces"]
    main_keys = reg[reg["round"] == "MAIN"][key].drop_duplicates().assign(_m=1)
    hit = set(mop.merge(main_keys, on=key, how="left").dropna(subset=["_m"])["reg_no"])
    check("ask A fair: the matched mop-up rows are exactly the re-registrations", hit == truth_rereg,
          "%d matched, %d re-registered" % (len(hit), len(truth_rereg)))
    mk = reg[reg["round"] == "MAIN"].drop_duplicates()
    co = mk.groupby(["sub_county", "ward", "dwelling_mark"]).size()
    check("ask A over-cleaning bites: dwellings with more than one main-round household", (co > 1).sum() > 1000, "%d" % (co > 1).sum())
    cases = calc.reported_cases(target)
    for mode in ("naive", "mapped", "dedup", "export_dedup"):
        v = calc.reported_cases(target, mode)
        miss = [sc for sc in C.SC_CODES if v[sc] != cases[sc]]
        check("ask B device: %s misses every sub-county" % mode, len(miss) == 7, "county %d against %d" % (sum(v.values()), sum(cases.values())))
    kh = pd.read_csv(os.path.join(target, "khis_moh705_obf_2024_2026.csv"), dtype=str, keep_default_na=False)
    truth_b = make_truth_cases()
    check("ask B fair: the golden equals the facilities' own confirmed cases", truth_b == cases, str(truth_b))
    check("ask B no marker column isolates the device rows", (kh["comment"] != "").sum() == 42 and kh["comment"].nunique() == 2, "")
    # separation: the call reads none of the ask files
    import inspect
    src = inspect.getsource(calc.golden)
    check("separation: the call reads no ask file", "nets_registration" not in src and "khis" not in src and "reported_cases" not in src, "")
    for f in ("nets_registration_2026.parquet", "khis_moh705_obf_2024_2026.csv", "facility_list_2026.csv",
              "insecticide_susceptibility_2025.csv", "rainfall_daily_2019_2026.csv"):
        check("deletion: %s is not read by the call" % f, f not in inspect.getsource(calc.golden) + inspect.getsource(calc.hlc_table)
              + inspect.getsource(calc.hbs_table) + inspect.getsource(calc.trial_tables) + inspect.getsource(calc.baseline)
              + inspect.getsource(calc.usage), "")

    # ------------------------------------------------------------------ input gates and realism
    files = sorted(os.listdir(target))
    fmts = {f.rsplit(".", 1)[1] for f in files}
    check("gate: 10 or more files", len(files) >= 10, str(len(files)))
    check("gate: 3 or more formats", len(fmts) >= 3, str(sorted(fmts)))
    check("gate: a file of 25,000 rows", len(df) >= 25000 and len(reg) >= 25000, "%d and %d" % (len(df), len(reg)))
    meta = json.load(open(os.path.join(C.TASK_DIR, "metadata.json")))
    check("gate: two distractors declared and shipped", len(meta["distractor_files"]) >= 2 and all(f in files for f in meta["distractor_files"]), "")
    check("gate: no file named for the stump or a distractor", not any(w in f.lower() for f in files for w in ("distract", "issue", "trap", "answer")), "")
    base = G["base"]
    check("realism: no round baseline counts", sum(1 for v in base.values() if v % 100 == 0) <= 1, "")
    check("realism: sub-county baselines differ", len({sum(base[(sc, m)] for (_, m) in C.WINDOW) for sc in C.SC_CODES}) == 7, "")
    check("realism: no two villages share a nightly catch profile", df.groupby("village_code")["an_ruvariensis"].apply(lambda s: s[s != ""].astype(int).sum()).nunique() == 14, "")
    nv = reg["head_name"].value_counts()
    check("realism: no head name dominates", nv.iloc[0] / len(reg) < 0.002, "%s %d" % (nv.index[0], nv.iloc[0]))
    people = list(C.PEOPLE.values())
    check("realism: no persona in the registration or survey", not reg["head_name"].isin(people).any(), "")
    # documents: positive controls through the same extractor, and dates
    check("doc: trial report positive control", "LulaNet R repels mosquitoes from the occupied net; it does not kill them" in txt, "")
    from docx import Document
    dtext = "\n".join(p.text for p in Document(os.path.join(target, DOCS.F_PLAN)).paragraphs)
    check("doc: plan positive control", DOCS.PLAN_PARAS["impact"][:60] in dtext and "follow the ward realignment of 1 July 2026" in dtext, "")
    check("doc: plan names no efficacy or trial", "KINGA" not in dtext and "efficacy" not in dtext.lower(), "")
    check("dates: registration before the pull", reg["reg_date"].max() <= C.PULL, str(reg["reg_date"].max()))
    check("dates: KHIS edits before the pull", kh["last_updated"].max() <= C.PULL.isoformat(), kh["last_updated"].max())
    check("dates: catches end September 2026", True, "")
    with zipfile.ZipFile(os.path.join(target, DOCS.F_PLAN)) as z:
        core = z.read("docProps/core.xml").decode()
    check("dates: plan saved before the pull", "2026-10-02" in core and "python" not in core.lower(), "")
    man = pd.read_csv(os.path.join(target, "export_manifest.csv"))["file"].tolist()
    check("H9 the manifest names every shipped file but itself", sorted(man) == sorted(f for f in files if f != "export_manifest.csv"), "")
    dct = open(os.path.join(target, "data_dictionary.txt"), encoding="utf-8").read()
    check("H9 the dictionary names every shipped file but itself", all(("\n" + f) in dct for f in files if f != "data_dictionary.txt"), "")
    gold = sorted(os.listdir(C.GOLDEN))
    check("H4 the goldens are exactly the prompt's files", gold == ["cases_averted_by_subcounty.png", "ruvari_cases_averted_2027.xlsx"], str(gold))
    prompt = open(os.path.join(C.TASK_DIR, "prompt.txt")).read()
    check("H4 the prompt names the golden files", all(g in prompt for g in gold), "")
    sub = open(os.path.join(C.TASK_DIR, "submission.md")).read()
    check("submission: no em dash", "\u2014" not in sub and "\u2013" not in sub, "")
    fails = [r for r in RESULTS if not r[1]]
    print("\n%d checks, %d FAIL" % (len(RESULTS), len(fails)))
    return 1 if fails else 0


def make_truth_rereg():
    import numpy as _np
    pools = R.name_pools(C.SEED % 100000)
    _, rereg = R.registration(_np.random.default_rng(C.SEED + 5), pools)
    return rereg


def make_truth_cases():
    import numpy as _np
    pools = R.name_pools(C.SEED % 100000)
    facs = R.facilities(_np.random.default_rng(C.SEED + 6), pools)
    _, truth = R.khis(_np.random.default_rng(C.SEED + 7), facs)
    sc_of = {f["mfl"]: f["sub_county"] for f in facs}
    out = {sc: 0 for sc in C.SC_CODES}
    for (mfl, y, m, age), v in truth.items():
        if (y, m) >= (2026, 1) and (y, m) <= (2026, 9):
            out[sc_of[mfl]] += v
    return out


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else C.TARGET))
