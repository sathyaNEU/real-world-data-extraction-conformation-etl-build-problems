"""Assertions over the built pack and the golden figures. Every check fails the build loudly.

    run(target, task_dir, wd, packed, g) -> number of assertions passed
"""
import json
import os
import re
import shutil
import tempfile
from collections import defaultdict
from datetime import date

import pandas as pd
import pdfplumber

import docs as DC
import golden as G
import orgs as O
import pack as PK
import world as W

T = G.THRESHOLD
N = [0]


REPORT = {}


def A(cond, msg):
    if not cond:
        raise AssertionError("CHECK FAILED: " + msg)
    N[0] += 1


def edge_distance(x, step):
    """distance to the nearest edge of the bin that rounds to the nearest multiple of step"""
    k = round(x / step)
    lo, hi = (k - 0.5) * step, (k + 0.5) * step
    return min(x - lo, hi - x)


def run(target, task_dir, wd, packed, g):
    N[0] = 0
    L = G.ladder(target, g)
    bt = G.backtest(g["hist"])
    main_checks(g, L, bt)
    corridor_checks(target, g)
    neutrality_checks(wd, packed, g)
    clean_data_check(target, g, L)
    distractor_check(target, task_dir, g)
    main_call_frozen(target, g, L, bt)
    exhibit_checks(target, wd, packed, g)
    structure_checks(target, task_dir, wd, g)
    document_checks(target)
    semantic_fork_checks(target, g, L)
    realism_checks(target, g)
    return N[0], L, bt


# ------------------------------------------------------------------ the main call
def main_checks(g, L, bt):
    A(g["call"] == "proceed", "the call is to proceed")
    A(g["total"] >= 1.08 * T, "answer at least 8 per cent above the threshold (%.0f)" % g["total"])
    A(edge_distance(g["total"], 100000) >= 20000, "total at least $20,000 inside its $0.1M bin (%.0f)" % g["total"])
    A(abs(g["total"] - round(g["total"], -5)) >= 3000, "total not on a round value")
    parts = {"P": g["P"]}
    parts.update(g["fam"])
    for k, v in parts.items():
        A(edge_distance(v, 10000) >= 1000, "%s at least $1,000 inside its $10,000 bin (%.0f)" % (k, v))
    A(abs(sum(parts.values()) - g["total"]) < 1.0, "the parts sum to the total")
    A(abs(g["other_fam"]) < 1.0, "no moved service falls outside the five lines")
    A(g["c1"] == 0.86 and g["c2"] == 0.0, "tier-one capture stated as 86 per cent, tier-two as nil")
    raw1, raw2 = g["fit"]["tier"]["1"], g["fit"]["tier"]["2"]
    A(abs(raw1 - 0.86) <= 0.003 and abs(raw2) <= 0.003,
      "the fitted shares sit at least 0.2 points inside their whole-per-cent bins (%.5f, %.5f)" % (raw1, raw2))
    R = L["rungs"]
    for k, v in R.items():
        if k != "R5 answer":
            A(v <= 0.92 * T, "rung %s at least 8 per cent below the threshold (%.0f)" % (k, v))
    A(abs(R["R5 answer"] - g["total"]) < 1.0, "the ladder's last rung is the answer")
    order = ["R0", "R1 employed group", "R2 pooled, Ledgestone", "R2 pooled, every acquisition", "R3 carrier",
             "R4 product by product", "R5 answer"]
    for a, b in zip(order, order[1:]):
        A(R[b] - R[a] >= 0.025 * T, "rungs %s and %s apart" % (a, b))
    for (model, price, base), v in L["grid"].items():
        if model == "tier, 2026 placements":
            A(v >= T, "grid cell %s/%s/%s proceeds (%.0f)" % (model, price, base, v))
        else:
            A(v < 0.97 * T, "grid cell %s/%s/%s closes with margin (%.0f)" % (model, price, base, v))
    # the records' own structure, with no filed criterion: every model that ignores the tier in force is
    # contradicted by some practice-year by 8 points or more, and the tier model fits every one within two
    worst = {k: v[0] for k, v in bt.items()}
    A(worst["tier"] < 0.02, "the tier model fits every practice-year within two points (%.4f)" % worst["tier"])
    for k, v in worst.items():
        if not k.startswith("tier"):
            A(v >= 0.08, "rival %s misses some practice-year by 8 points or more (%.4f)" % (k, v))
    A(all(v[2] == 12 for v in bt.values()), "every model is scored on the same 12 practice-years")
    REPORT["groups"] = {k: len(v) for k, v in G.fit_models(g["hist"]).items()}
    h = g["hist"]
    s0 = G.pre_shares(h)
    # C1: every finer version of the tier model a solver could carry to Brightwater states the same shares
    hh = h[h["procedure_code"].map(G.family).isin(list(G.LINES))]
    REPORT["refinements"] = {}
    for lab, fn in G.REFINEMENTS.items():
        fit = G.fit_models(hh, models={lab: fn})[lab]
        if lab.endswith(", 2024"):
            fit = {k: v for k, v in fit.items() if k.endswith("|2024")}
        for k, v in fit.items():
            want = g["c1"] if k.split("|")[0] == "1" else g["c2"]
            A(G.whole(v) == want, "C1 %s cell %s states %.0f per cent (%.4f)" % (lab, k, 100 * want, v))
        one = [v for k, v in fit.items() if k.startswith("1|")]
        two = [v for k, v in fit.items() if k.startswith("2|")]
        REPORT["refinements"][lab] = (min(one), max(one), min(two), max(two), len(fit))
    # the split is absolute in every practice, and the within-product switch is in the records: Norbridge's
    # Tiered EPO patients at Wolf River's practices stayed while it tiered Wolf River second and moved from
    # plan year 2024
    for tin, sub in hh[hh["post"]].groupby("prac_tin"):
        for t, ss in sub.groupby("tier"):
            v = (ss["at"] - s0[tin]).sum() / (1 - s0[tin]) / len(ss)
            A(G.whole(v) == (g["c1"] if t == 1 else g["c2"]), "practice %s tier %s states the same share (%.4f)" % (tin, t, v))
    w = h[(h["acq_sys"] == "Wolf River Health") & (h["product"] == "NBH-TEP4") & h["post"]]
    REPORT["switch"] = {}
    for after, ss in w.groupby(w["plan_year"] >= 2024):
        v = (ss["at"] - ss["prac_tin"].map(s0)).sum() / (1 - ss["prac_tin"].map(s0)).sum()
        want = g["c1"] if after else g["c2"]
        A(G.whole(v) == want, "Norbridge Tiered EPO at Wolf River, plan years %s: share moved %.4f" %
          ("2024" if after else "before 2024", v))
        REPORT["switch"]["2024" if after else "before 2024"] = (v, len(ss))
    A(len(REPORT["switch"]) == 2 and min(n for _, n in REPORT["switch"].values()) >= 200,
      "the switch is observed on both sides, with 200 or more services on each")
    # the composition the stump rests on
    el = g["br"][g["br"]["eligible"]]
    vtp = el.loc[el["product"] == "BMH-VTP3", "delta"].sum() / el["delta"].sum()
    A(0.30 <= vtp <= 0.45, "Value Tier patients carry 30 to 45 per cent of Brightwater's price gap (%.3f)" % vtp)
    h = g["hist"]
    hv = (h.loc[h["acq_sys"] == "Ledgestone Health", "product"] == "BMH-VTP3").mean()
    A(hv <= 0.10, "Value Tier patients are under a tenth of Ledgestone's acquired practices' referrals (%.3f)" % hv)
    A(set(el.loc[el["t26"] == 2, "product"]) <= {"CBH-TPO2", "NBH-TEP4"}, "only two products keep Ledgestone second in 2026")
    A((el["t24"] != el["t26"]).sum() > 0 and set(el.loc[el["t24"] != el["t26"], "product"]) == {"BMH-VTP3"},
      "only the Value Tier PPO changes Ledgestone's placement between 2024 and 2026")


def answer_with(g, cap_fn):
    br = g["br"]
    el = br[br["eligible"]]
    caps = cap_fn(el)
    ref = sum(c * d for c, d in zip(caps, el["delta"]))
    fam = defaultdict(float)
    for c, d, f in zip(caps, el["delta"], el["fam"]):
        fam[f] += c * d
    return g["P"] + ref, fam


def corridor_checks(target, g):
    h = g["hist"]
    variants = {}
    ldg = h[h["acq_sys"] == "Ledgestone Health"]
    variants["tier, Ledgestone's acquisitions only"] = G.fit_models(ldg)["tier"]
    reg_tins = set(G.load(target)["register"]["entity_tin"])
    variants["tier, register acquisitions only"] = G.fit_models(h[h["prac_tin"].isin(reg_tins)])["tier"]
    cal = G.fit_models(h)["tier (calendar year)"]
    variants["tier by calendar year"] = cal
    # per practice averaged
    per = []
    for tin in sorted(h["prac_tin"].unique()):
        per.append(G.fit_models(h[h["prac_tin"] == tin])["tier"]["1"])
    variants["tier, practices averaged"] = {"1": sum(per) / len(per), "2": g["c2"]}
    # Northpoint dated at its first or last physician's move
    p3 = h.groupby("prac_tin")["acq_date"].nunique()
    p3tin = p3[p3 > 1].index[0]
    for lab, fn in (("first", "min"), ("last", "max")):
        hh = h.copy()
        d = getattr(hh.loc[hh["prac_tin"] == p3tin, "acq_date"], fn)()
        hh.loc[hh["prac_tin"] == p3tin, "acq_date"] = d
        hh["post"] = hh["dos"] >= hh["acq_date"]
        variants["Northpoint dated at its %s move" % lab] = G.fit_models(hh)["tier"]
    fams = sorted(g["fam"])
    for name, fit in variants.items():
        A(G.whole(fit["1"]) == g["c1"] and G.whole(fit["2"]) == g["c2"],
          "corridor %s states the same whole-per-cent shares (%.5f, %.5f)" % (name, fit["1"], fit["2"]))
    # and a reader who projects with the unrounded share stays in every bin
    REPORT["corridor"] = {}
    for name, fit in variants.items():
        c1, c2 = fit["1"], fit["2"]
        tot, fam = answer_with(g, lambda el: [c1 if t == 1 else c2 for t in el["t26"]])
        REPORT["corridor"][name] = (c1, c2, tot)
        A(round(tot, -5) == round(g["total"], -5), "corridor %s keeps the total in its bin (%.0f)" % (name, tot))
        for f in fams:
            A(round(fam[f], -4) == round(g["fam"][f], -4), "corridor %s keeps %s in its bin (%.0f)" % (name, f, fam[f]))
    # per-family capture
    pf = {}
    for f in fams:
        sub = h[h["procedure_code"].map(G.family) == f]
        if not sub.empty:
            pf[f] = G.fit_models(sub)["tier"]
    tot, fam = answer_with(g, lambda el: [(pf.get(f, {"1": g["c1"]})["1"] if t == 1 else g["c2"])
                                          for t, f in zip(el["t26"], el["fam"])])
    REPORT["corridor"]["tier by service line"] = (min(v["1"] for v in pf.values()), max(v["1"] for v in pf.values()), tot)
    A(round(tot, -5) == round(g["total"], -5), "per-family capture keeps the total in its bin (%.0f)" % tot)
    for f in fams:
        A(round(fam[f], -4) == round(g["fam"][f], -4), "per-family capture keeps %s in its bin (%.0f)" % (f, fam[f]))


# ------------------------------------------------------------------ mess neutrality
def neutrality_checks(wd, packed, g):
    lines = wd["lines"]
    mem = wd["mem"]
    for dev, idx in packed["ledger"].items():
        bad = [i for i in idx if lines[i]["tag"] in PK.MAIN_TAGS]
        A(not bad, "device %s has zero rows in the main call's population (%d rows elsewhere)" % (dev, len(idx)))
        A(len(idx) > 0, "device %s is present" % dev)
    A(all(len(mem.info[m]["zips"]) == 1 for m in mem.by_pool["BMG"]), "no Brightwater member moves")
    A(all(len([s for s in mem.info[m]["spans"] if s[1] <= date(2024, 12, 31) and s[2] >= date(2024, 1, 1)]) == 1
          for m in mem.by_pool["BMG"]), "no Brightwater member changes product in 2024")
    for pool in ("P1", "P2", "P3", "P4", "P5", "W1", "W2"):
        A(all(len(mem.info[m]["zips"]) == 1 for m in mem.by_pool[pool]), "acquired practice %s members do not move" % pool)
    main = [r for r in packed["fac_rows"] if r["tag"] in ("bmg_ref", "hist_ref")]
    A(all(r["freq"] == "1" and r["qty"] == 1 and not r["late"] and r["paid"] <= date(2025, 6, 30) for r in main),
      "main referral rows: originals, one unit, paid by the runout")
    mp = [r for r in packed["prof_rows"] if r["tag"] == "bmg_prof"]
    A(all(r["freq"] == "1" and not r["late"] and r["paid"] <= date(2025, 6, 30) for r in mp),
      "Brightwater professional rows: originals, paid by the runout")
    late = [r for r in packed["fac_rows"] if r["late"]]
    A(all(r["paid"] > date(2025, 6, 30) for r in late) and sum(r["paid"] <= date(2025, 8, 31) for r in late) > 100,
      "late-paid lines fall after the runout, most of them inside the extract")


def clean_data_check(target, g, L):
    """Repair the ask-path mess and require the main figures and the product-by-product rung unchanged."""
    tmp = tempfile.mkdtemp()
    try:
        for f in os.listdir(target):
            shutil.copy(os.path.join(target, f), tmp)
        p = os.path.join(tmp, PK.FILES["fac24"])
        df = pd.read_csv(p, dtype=str, keep_default_na=False)
        named = set(df.loc[df["claim_frequency_code"].isin(["7", "8"]), "original_claim_control_number"])
        df = df[df["claim_frequency_code"].isin(["1", "7"]) & ~df["payer_claim_control_number"].isin(named)].copy()
        df["claim_frequency_code"] = "1"
        df["original_claim_control_number"] = ""
        df = df[df["paid_date"] <= "2025-06-30"]
        df.to_csv(p, index=False, lineterminator="\n")
        g2 = G.compute(tmp)
        A(abs(g2["total"] - g["total"]) < 0.01 and abs(g2["P"] - g["P"]) < 0.01, "clean-data test: the answer is unchanged")
        L2 = G.ladder(tmp, g2)
        A(abs(L2["rungs"]["R4 product by product"] - L["rungs"]["R4 product by product"]) < 0.01,
          "clean-data test: the product-by-product rung is unchanged")
        A(g2["call"] == "proceed" and L2["rungs"]["R4 product by product"] < T, "clean-data test: answer and naive still differ")
    finally:
        shutil.rmtree(tmp)


def distractor_check(target, task_dir, g):
    meta = json.load(open(os.path.join(task_dir, "metadata.json")))
    dis = meta["distractor_files"]
    A(len(dis) >= 2, "two or more distractors named in metadata.json")
    tmp = tempfile.mkdtemp()
    try:
        for f in os.listdir(target):
            if f not in dis:
                shutil.copy(os.path.join(target, f), tmp)
        g2 = G.compute(tmp)
        A(abs(g2["total"] - g["total"]) < 0.01 and g2["ex1"] == g["ex1"] and g2["ex2"] == g["ex2"],
          "the golden recomputes unchanged with the distractors deleted")
    finally:
        shutil.rmtree(tmp)
    for root, _, files in os.walk(target):
        for f in files:
            A("distractor" not in f.lower(), "no file name says distractor")
            if f.endswith((".csv", ".json")):
                A("distractor" not in open(os.path.join(root, f), encoding="utf-8").read().lower(),
                  "no file content says distractor (%s)" % f)


# ------------------------------------------------------------------ the exhibits (appendix A2 and A3)
BROAD = ("member_id", "dos", "procedure_code", "service_facility_npi")
MIN_D = 0.05          # half a unit of the stated rounding: a figure this close to the golden would score


def miss(x, gold):
    """A share outside the golden's bin: another rounding bin and at least half a unit away."""
    return round(x, 1) != round(gold, 1) and abs(x - gold) >= MIN_D


def exhibit_context(target):
    X = G.load(target)
    zc = G.zip_county(target)
    spans = G.billing_spans(X["reassign"])
    ctrl = G.Control(X["register"])
    with pdfplumber.open(os.path.join(target, DC.NOTICE)) as pdf:
        text = " ".join(pg.extract_text() or "" for pg in pdf.pages)
    bmg = re.search(r"Brightwater's number\s*\((\d{2}-\d{7})\)", text).group(1)
    return X, zc, spans, ctrl, bmg


def ex1_variant(ctx, second="once", residence="span", runout=False, versions="latest"):
    X, zc, spans, ctrl, bmg = ctx
    kw = dict(residence=residence, runout=runout, versions=versions)
    if second == "broad":
        kw.update(second="one per key", key=BROAD)
    else:
        kw.update(second=second)
    return G.ex1_cells(X, zc, bmg, spans, **kw)


def ex2_variant(ctx, **kw):
    X, zc, spans, ctrl, bmg = ctx
    return G.ex2_cells(X, zc, bmg, ctrl, **kw)


EX1_AXES = {"second": ["once", "every claim", "broad"], "residence": ["span", "first"], "runout": [False, True],
            "versions": ["latest", "as filed"]}
EX2_AXES = {"specialty": ["provider", "claim"], "second": ["once", "every claim"], "physicians": [True, False],
            "system": ["register", "lmg"], "telehealth": [False, True], "runout": [False, True]}
EX1_STOPS = {"every claim counted (the cracker)": dict(second="every claim"),
             "de-duplicated on member, date, code and facility": dict(second="broad"),
             "the member's first ZIP": dict(residence="first"),
             "rule 4.03's runout applied": dict(runout=True),
             "versions as filed": dict(versions="as filed")}
EX2_STOPS = {"the claim's taxonomy and both plans (the cracker)": dict(specialty="claim", second="every claim"),
             "the claim's taxonomy": dict(specialty="claim"),
             "both plans' copies": dict(second="every claim"),
             "telehealth counted": dict(telehealth=True),
             "nurse practitioner counted": dict(physicians=False),
             "Ledgestone Medical Group's number only": dict(system="lmg"),
             "rule 4.03's runout applied": dict(runout=True)}


def exhibit_truth(wd, packed):
    """Both exhibits from the simulation's own services, without the claim files: every service once, a bilateral
    service as its two sides, residence from the member's address on the day, specialty from the physician."""
    mem, people, lines = wd["mem"], wd["people"], wd["lines"]
    bil = set(packed["ledger"]["bilateral_lines"])
    t1 = defaultdict(lambda: [0, 0])
    for i, l in enumerate(lines):
        if l["kind"] != "fac" or l["date"].year != 2024:
            continue
        fam = W.CPT[l["cpt"]][1]
        if fam not in ("IMG", "ENDO", "ARTH"):
            continue
        cty = W.ZIP_COUNTY[mem.zip_on(l["member"], l["date"])]
        if cty not in ("Manitowoc", "Kewaunee"):
            continue
        n = 2 if i in bil else 1
        t1[(cty, fam)][0] += n
        if l["tag"] == "bmg_ref":
            t1[(cty, fam)][1] += n
    spec = {"FM": "primary care", "IM": "primary care", "PED": "primary care", "GI": "gastroenterology",
            "ORTH": "orthopaedic surgery", "CARD": "cardiovascular disease"}
    office = {str(c) for c in range(99202, 99216)}
    t2 = defaultdict(lambda: [0, 0, 0])
    for l in lines:
        if l["kind"] != "prof" or l["code"] not in office or l["tele"] is not None:
            continue
        if W.ZIP_COUNTY[l["site_zip"]] not in ("Manitowoc", "Kewaunee"):
            continue
        sp = spec.get(people[l["rnd_npi"]]["spec"])
        if sp is None:
            continue
        t2[sp][0] += 1
        t2[sp][1] += l["practice"] == "BMG"
        t2[sp][2] += l["practice"] in ("LMG", "MFP")
    return t1, t2


def exhibit_checks(target, wd, packed, g):
    ctx = exhibit_context(target)
    t1, t2 = exhibit_truth(wd, packed)
    g1, g2 = g["ex1"], g["ex2"]
    for k, (tot, b, sh) in g1.items():
        A([tot, b] == t1[k], "Exhibit 1 %s reproduces the simulation's services (%s / %s)" % (k, [tot, b], t1[k]))
        A(edge_distance(sh, 0.1) >= 0.01, "Exhibit 1 %s share at least 0.01 inside its bin (%.3f)" % (k, sh))
    for k, v in g2.items():
        A(list(v[:3]) == t2[k], "Exhibit 2 %s reproduces the simulation's visits (%s / %s)" % (k, list(v[:3]), t2[k]))
        A(min(edge_distance(v[3], 0.1), edge_distance(v[4], 0.1)) >= 0.01,
          "Exhibit 2 %s shares at least 0.01 inside their bins (%.3f, %.3f)" % (k, v[3], v[4]))
    REPORT["ex1_stops"], REPORT["ex2_stops"] = {}, {}
    # the stops: the cracker misses every figure; every other stop lands outside every bin it moves by a full unit
    for name, kw in EX1_STOPS.items():
        r = ex1_variant(ctx, **kw)
        REPORT["ex1_stops"][name] = {k: (r[k][0] - g1[k][0], r[k][2] - g1[k][2]) for k in g1}
        for k in g1:
            if "cracker" in name:
                A(r[k][0] != g1[k][0] and miss(r[k][2], g1[k][2]), "the cracker misses Exhibit 1 %s (%s)" % (k, r[k]))
            elif abs(r[k][2] - g1[k][2]) >= 0.1:
                A(miss(r[k][2], g1[k][2]) and r[k][0] != g1[k][0], "Exhibit 1 stop '%s' leaves %s's bin" % (name, k))
    for name, kw in EX2_STOPS.items():
        r = ex2_variant(ctx, **kw)
        REPORT["ex2_stops"][name] = {k: (r[k][3] - g2[k][3], r[k][4] - g2[k][4]) for k in g2}
        for k in g2:
            for j in (3, 4):
                if "cracker" in name:
                    A(miss(r[k][j], g2[k][j]), "the cracker misses Exhibit 2 %s %d (%.3f / %.3f)" % (k, j, r[k][j], g2[k][j]))
                elif abs(r[k][j] - g2[k][j]) >= 0.1:
                    A(miss(r[k][j], g2[k][j]), "Exhibit 2 stop '%s' leaves %s's bin" % (name, k))
    # direction discipline: no combination of mishandlings lands back inside a bin one of them leaves
    import itertools
    worst = [9.0, 9.0]
    for n_ax, (axes, fn, gold, cols) in enumerate(((EX1_AXES, lambda **kw: ex1_variant(ctx, **kw), g1, (2,)),
                                                   (EX2_AXES, lambda **kw: ex2_variant(ctx, **kw), g2, (3, 4)))):
        single = {(a, v): fn(**{a: v}) for a, vals in axes.items() for v in vals[1:]}
        for combo in itertools.product(*axes.values()):
            kw = dict(zip(axes, combo))
            mis = [(a, v) for a, v in kw.items() if v != axes[a][0]]
            if len(mis) < 2:
                continue
            r = fn(**kw)
            for k in gold:
                for j in cols:
                    if any(abs(single[m][k][j] - gold[k][j]) >= 0.1 for m in mis):
                        A(miss(r[k][j], gold[k][j]), "combination %s keeps %s %d out of its bin" % (mis, k, j))
                        worst[n_ax] = min(worst[n_ax], abs(r[k][j] - gold[k][j]))
    REPORT["combo_worst"] = worst
    # the referees, and no marker: one taxonomy per provider, a second carrier's span under every second-plan
    # claim, second-plan claims filed as ordinary originals
    X = ctx[0]
    pv = X["provfile"].groupby("provider_npi")["primary_taxonomy"].nunique()
    A(int(pv.max()) == 1, "the provider file gives every NPI one taxonomy")
    lake = X["prof"][X["prof"]["service_facility_zip"].map(ctx[1]).isin(("Manitowoc", "Kewaunee"))]
    A(set(lake["rendering_provider_npi"]) <= set(X["provfile"]["provider_npi"]), "every lakeshore rendering NPI is on file")
    sp = [r for r in packed["fac_rows"] + packed["prof_rows"] if "second_plan" in r["device"]]
    A(len(sp) > 1000 and all(r["freq"] == "1" and r["orig"] == "" for r in sp), "second-plan claims file as originals")
    A(all(wd["mem"].second_on(r["member"], r["dos"]) == r["product"] for r in sp), "a second carrier's span under each")
    for key in ("fac24", "prof24"):
        df = pd.read_csv(os.path.join(target, PK.FILES[key]), dtype=str, keep_default_na=False)
        idn = (df["allowed_amount"].astype(float) - df["plan_paid_amount"].astype(float)
               - df["member_liability_amount"].astype(float)).abs()
        A(bool((idn < 0.011).all()), "%s: allowed is plan paid plus member liability on every row" % key)
        A(int(df.drop(columns=["payer_claim_control_number"]).duplicated().sum()) == 0,
          "%s: no exact duplicate even without the claim number" % key)
    gt = [r for r in packed["prof_rows"] if "group_taxonomy" in r["device"]]
    A(len(gt) > 1000 and all(r["practice"] == "KPN" for r in gt), "the group taxonomy sits on Kinnickinnic's lines only")
    A(all(r["practice"] != "MFP" and W.FAC[r["fac"]][2] != "LDG" for r in sp if "fac" in r and r.get("fac")),
      "no second-plan claim on Mishicot's referrals or at a Ledgestone site")
    A(all(r["practice"] != "MFP" for r in sp if "rnd_npi" in r), "Mishicot's office files no second-plan claims")


def main_call_frozen(target, g, L, bt):
    """The main call's declared rows, reference files and figures reproduce the build before the ask layer."""
    import maincall as MC
    ref = MC.load_ref()
    now = MC.snapshot(target, g, L, bt)
    for k, v in ref["population"].items():
        A(now["population"][k] == v, "main call population '%s' byte-identical to the reference" % k)
    A(now["figures"] == ref["figures"], "main call figures identical to the reference")


def structure_checks(target, task_dir, wd, g):
    files = sorted(os.listdir(target))
    A(len(files) >= 10, "10 or more files (%d)" % len(files))
    fmts = {os.path.splitext(f)[1] for f in files}
    A(len(fmts) >= 3, "3 or more formats (%s)" % sorted(fmts))
    big = max(sum(1 for _ in open(os.path.join(target, f), encoding="utf-8")) - 1 for f in files if f.endswith(".csv"))
    A(big >= 25000, "a file of 25,000 or more rows (%d)" % big)
    tiers = json.load(open(os.path.join(target, PK.FILES["tiers"])))
    pl = {(f["product_id"], f["plan_year"], p["hospital_system"]): p["tier"] for f in tiers["filings"]
          for p in f["hospital_system_placements"]}
    A(all(pl[("BMH-VTP3", y, "Ledgestone Health")] == 2 for y in range(2020, 2025)) and
      all(pl[("BMH-VTP3", y, "Ledgestone Health")] == 1 for y in (2025, 2026)), "Bayfield places Ledgestone first from 2025")
    A(all(pl[("NBH-TEP4", y, "Wolf River Health")] == 2 for y in range(2020, 2024)) and
      all(pl[("NBH-TEP4", y, "Wolf River Health")] == 1 for y in range(2024, 2027)), "Norbridge places Wolf River first from 2024")
    changes = {(p, s) for (p, y, s), t in pl.items() if y > 2020 and pl[(p, y - 1, s)] != t}
    A(changes == {("BMH-VTP3", "Ledgestone Health"), ("NBH-TEP4", "Wolf River Health")}, "no other placement changes")
    A(len(g["bmg_npis"]) == 18, "eighteen Brightwater physicians")
    for f in files:
        if f.endswith((".csv", ".json")):
            A("—" not in open(os.path.join(target, f), encoding="utf-8").read(), "no em dash in %s" % f)


def pdf_text(path):
    with pdfplumber.open(path) as pdf:
        return " ".join(pg.extract_text() or "" for pg in pdf.pages)


def document_checks(target):
    texts = {f: pdf_text(os.path.join(target, f)) for f in (DC.RULE, DC.APPENDIX, DC.DICTIONARY, DC.NOTICE)}
    for f, t in texts.items():
        low = t.lower()
        A("—" not in t, "no em dash in %s" % f)
        for w in ("capture", "steer", "placement", "placed", "followed", "follows their"):
            A(not re.search(r"\b%s\b" % w, low), "%s carries no '%s'" % (f, w))
        if f != DC.DICTIONARY:
            A("tier" not in low, "%s never mentions tiers" % f)
    A("tiered network" in texts[DC.DICTIONARY].lower(), "the dictionary describes the product reference's tier flag")
    A(sum("2,000,000" in t for t in texts.values()) == 1 and "2,000,000" in texts[DC.RULE], "the threshold is stated once, in the rule")
    rule = re.sub(r"\s+", " ", texts[DC.RULE])
    A("share expected for that service in the projection year" in rule and "in whole per cent" in rule,
      "the rule files the per-service expected share for the projection year and its rounding")
    # the method is left to the records: no filed sentence selects among estimates or names what to condition on
    for w in ("closest", "largest miss", "fitted only", "back-test", "backtest", "out of sample", "more groups"):
        A(w not in rule.lower(), "the rule files no selection criterion ('%s')" % w)


# ------------------------------------------------------------------ the realism sweep (dataset-generation, stage 3 gate)
def realism_checks(target, g):
    f = pd.read_csv(os.path.join(target, PK.FILES["fac24"]), dtype=str, usecols=["service_facility_npi", "service_from_date"])
    f["m"] = f["service_from_date"].str[:7]
    annual = f.groupby("service_facility_npi").size()
    A(annual.nunique() == len(annual), "no two facilities carry the same 2024 line count")
    monthly = f.groupby(["service_facility_npi", "m"]).size().unstack(fill_value=0)
    A(int((monthly.std(axis=1) == 0).sum()) == 0, "no facility's monthly series is constant")
    for key, col, n in ((PK.FILES["fac24"], "service_from_date", 7), (PK.FILES["prof24"], "service_from_date", 7),
                        (PK.FILES["fachist"], "DOS_FROM", 6)):
        d = pd.read_csv(os.path.join(target, key), dtype=str, usecols=[col])
        tot = d[col].str[:n].value_counts()
        A(tot.value_counts().max() <= 3, "%s: no monthly total recurs more than three times" % key)
    # headline figures never sit exactly on a round value
    A(round(g["total"]) % 1000 != 0 and all(round(v) % 1000 != 0 for v in [g["P"]] + list(g["fam"].values())),
      "the total and its parts are not round thousands")
    A(all(abs(v[2] - round(v[2])) > 1e-6 for v in g["ex1"].values()) and
      all(abs(x - round(x)) > 1e-6 for v in g["ex2"].values() for x in v[3:]), "no exhibit share is an exact whole per cent")
    A(len({v[0] for v in g["ex1"].values()}) == 6 and all(v[0] % 100 for v in g["ex1"].values()),
      "the six service counts differ and none is a round hundred")


# ------------------------------------------------------------------ the semantic fork table (design note SF1 to SF12)
def semantic_fork_checks(target, g, L):
    X = G.load(target)
    rule = re.sub(r"\s+", " ", pdf_text(os.path.join(target, DC.RULE)))
    notice = re.sub(r"\s+", " ", pdf_text(os.path.join(target, DC.NOTICE)))
    pr = X["prodref"]
    br = g["br"]
    el = br[br["eligible"]]
    # SF1 commercial: the product reference's line of business; Medicare Advantage products are another
    ma = set(pr.loc[pr["line_of_business"] != "Commercial", "product_id"])
    A(bool(ma) and not (set(br["product_id"]) & ma) and "line of business Commercial" in rule,
      "SF1 commercial means line of business Commercial (4.02(b)); no baseline line carries another")
    # SF2 spending: the allowed amount, plan payment and cost sharing together
    A("the plan's payment and the member's cost sharing together" in rule, "SF2 spending is the allowed amount (4.02(c))")
    # SF3 the increase: projected less baseline spending; Ledgestone's gross new revenue reads larger, same call
    gross = g["P"] + float((el["share_moving"] * el["new_rate"] * el["qty"]).sum())
    A("projected spending less baseline spending" in rule and gross > g["total"] and gross >= T,
      "SF3 the increase is net of the baseline (4.06); the gross reading (%.0f) proceeds as well" % gross)
    # SF4 2026: the projection year; the plan year in force on a July renewer's date carries the same placement
    A(bool((el["t25"] == el["t26"]).all()), "SF4 plan years 2025 and 2026 place Ledgestone alike for every moving referral")
    # SF5 rounding: summing the rounded parts gives the same $0.1 million figure
    parts = [g["P"]] + list(g["fam"].values())
    A(round(sum(round(v, -4) for v in parts) / 1e6, 1) == round(g["total"] / 1e6, 1), "SF5 rounded parts sum to the same total")
    # SF6 the threshold: '$2,000,000 or more'; the figure is above it under either boundary
    A(g["total"] > T and "$2,000,000 or more" in rule, "SF6 the projection is strictly above the threshold")
    # SF7 the baseline window: no Brightwater line in the extract was paid after the runout
    fac = G.latest_versions(X["fac"])
    prof = G.latest_versions(X["prof"])
    late_f = fac[(fac["dos"].dt.year == 2024) & (fac["paid"] > G.RUNOUT) & fac["referring_provider_npi"].isin(g["bmg_npis"])]
    late_p = prof[(prof["dos"].dt.year == 2024) & (prof["paid"] > G.RUNOUT) & (prof["billing_provider_tin"] == g["bmg_tin"])]
    A(len(late_f) == 0 and len(late_p) == 0 and "paid on or before 30 June of the following year" in rule,
      "SF7 the extract's later payments add nothing to Brightwater's baseline (%d, %d)" % (len(late_f), len(late_p)))
    # SF8 Brightwater's physicians: billing under its number in 2024, which is Exhibit B's list
    exb = set(re.findall(r"\b(1\d{9})\b", notice[notice.index("Exhibit B. Brightwater"):]))
    spans = G.billing_spans(X["reassign"])
    in24 = {n for n, lst in spans.items() if any(t == g["bmg_tin"] and s <= pd.Timestamp("2024-12-31") and e >= pd.Timestamp("2024-01-01")
                                               for t, s, e in lst)}
    A(len(exb) == 18 and exb == in24, "SF8 the physicians billing under Brightwater's number in 2024 are Exhibit B's eighteen")
    # SF9 offers: the codes Ledgestone's sites bill, and the codes Exhibit C prices, move the same services
    ex_codes = {c for (car, c) in g["fac_rate"]}
    moving_codes = set(br.loc[~br["at_ldg"], "procedure_code"])
    A(all((c in g["offered"]) == (c in ex_codes) for c in moving_codes),
      "SF9 billed and filed codes agree on every code Brightwater refers elsewhere")
    # SF10 the facility price: the rate filed with the notice; Ledgestone's 2024 claim prices also proceed
    A("facility rate filed with the notice" in rule and L["grid"][("tier, 2026 placements", "claims2024", "outside")] >= T,
      "SF10 the filed rate (4.04(b)); the 2024-price reading proceeds as well")
    # SF11 the expected share in whole per cent; the unrounded share lands the same total and parts
    c1, c2 = g["fit"]["tier"]["1"], g["fit"]["tier"]["2"]
    tot, fam = answer_with(g, lambda d: [c1 if t == 1 else c2 for t in d["t26"]])
    A("in whole per cent" in rule and round(tot, -5) == round(g["total"], -5)
      and all(round(fam[f], -4) == round(g["fam"][f], -4) for f in g["fam"]),
      "SF11 the unrounded share keeps the total and every part in its bin (%.0f)" % tot)
    # SF12 the base: only services not already at a Ledgestone site move; the other reading proceeds as well
    A("that was not at one of the acquiring party's sites in the baseline" in rule
      and L["grid"][("tier, 2026 placements", "filed", "all")] >= T, "SF12 the base is the outside referrals (4.04(b))")


# ------------------------------------------------------------------ the write-up agrees with the golden
def submission_check(task_dir, figs, g):
    txt = open(os.path.join(task_dir, "submission.md"), encoding="utf-8").read()
    A("\u2014" not in txt, "no em dash in submission.md")
    money = lambda v: "${:,.0f}".format(v)
    A("$%s million" % figs["total_m"] in txt, "submission carries the total")
    A(money(figs["professional"]) in txt and money(figs["referred"]) in txt, "submission carries the two parts")
    A("%d%%" % round(100 * g["c1"]) in txt, "submission carries the tier-one share")
    names = {"IMG": "imaging", "ENDO": "endoscopy", "ARTH": "arthroscopy"}
    for key, (n, sh) in figs["ex1"].items():
        county, fam = key.split("|")
        A("%s County, %s: %s services, %s%%" % (county, names[fam], n, sh) in txt, "submission carries Exhibit 1 %s" % key)
    labels = {"primary care": "Primary care", "gastroenterology": "Gastroenterology",
              "orthopaedic surgery": "Orthopaedics", "cardiovascular disease": "Cardiology"}
    for sp, (b, l) in figs["ex2"].items():
        A("%s: Brightwater %s%%, Ledgestone %s%%" % (labels[sp], b, l) in txt, "submission carries Exhibit 2 %s" % sp)
    A(("Proceed" in txt) == (figs["call"] == "proceed"), "submission carries the call")
    gold = pdf_text(os.path.join(task_dir, "golden", "N25-014_preliminary_review.pdf"))
    flat = re.sub(r"\s+", " ", gold)
    for key, (n, sh) in figs["ex1"].items():
        A("%s %s%%" % (n, sh) in flat, "the golden PDF carries Exhibit 1 %s as the write-up does" % key)
    for sp, (b, l) in figs["ex2"].items():
        A("%s %s%% %s%%" % (labels[sp], b, l) in flat, "the golden PDF carries Exhibit 2 %s as the write-up does" % sp)


# ------------------------------------------------------------------ house fixes wired in (reduce-house-fixes)
def house_checks(target, task_dir, g):
    import hashlib
    import zipfile
    # H3: the golden's description of the Value Tier PPO as Brightwater's commonest plan
    X = G.load(target)
    E = G.Elig(X["elig"])
    pts = {}
    for m, d in zip(g["br"]["member_id"], g["br"]["dos"]):
        pts.setdefault(m, E.on(m, d)[0])
    prof = X["prof"]
    bp = prof[(prof["billing_provider_tin"] == g["bmg_tin"]) & (prof["dos"].dt.year == 2024)]
    for m, d in zip(bp["member_id"], bp["dos"]):
        pts.setdefault(m, E.on(m, d)[0])
    counts = pd.Series(list(pts.values())).value_counts()
    A(counts.index[0] == "BMH-VTP3", "the Value Tier PPO is the commonest plan among Brightwater's patients")
    # H9: the manifest registers every shipped file but itself
    man = pd.read_csv(os.path.join(target, "export_manifest.csv"), dtype=str)
    A(set(man["file_name"]) == set(os.listdir(target)) - {"export_manifest.csv"}, "the manifest registers every file")
    # H16: no file's dates run ahead of the stated extract dates
    tiers = json.load(open(os.path.join(target, PK.FILES["tiers"])))
    A(all(f["approved"] <= tiers["updated"][:10] for f in tiers["filings"]), "every filing approved before the compilation date")
    fh = pd.read_csv(os.path.join(target, PK.FILES["fachist"]), dtype=str)
    A(fh["PAID_DT"].max() <= "20240630", "the 2021 to 2023 extract holds claims paid by 30 June 2024")
    for k in ("fac24", "prof24", "ma"):
        f = pd.read_csv(os.path.join(target, PK.FILES[k]), dtype=str)
        A(f["paid_date"].max() <= "2025-08-31" and f["service_from_date"].min() >= "2024-01-01",
          "%s within its stated window" % k)
    el = pd.read_csv(os.path.join(target, PK.FILES["elig"]), dtype=str)
    A(el["coverage_end"].max() <= "2024-12-31", "eligibility ends with 2024")
    # H14: no degenerate subgroup inside the tier-one capture
    h = g["hist"]
    t1 = h[h["tier"] == 1]
    for col in ("carrier", "acq_sys"):
        for key, sub in t1.groupby(col):
            fit = G.fit_models(sub)["tier"]["1"]
            A(abs(fit - g["c1"]) < 0.03, "tier-one capture steady across %s %s (%.3f)" % (col, key, fit))
    fam = t1["procedure_code"].map(G.family)
    for f, sub in t1.groupby(fam):
        A(abs(G.fit_models(sub)["tier"]["1"] - g["c1"]) < 0.03, "tier-one capture steady across family %s" % f)
    # H8: every citation in the golden and the write-up resolves
    rule = pdf_text(os.path.join(target, DC.RULE))
    app = pdf_text(os.path.join(target, DC.APPENDIX))
    sub = open(os.path.join(task_dir, "submission.md"), encoding="utf-8").read()
    gold = pdf_text(os.path.join(task_dir, "golden", "N25-014_preliminary_review.pdf"))
    for txt in (sub, gold):
        for c4 in set(re.findall(r"4\.0\d", txt)):
            A(c4 + " " in rule, "rule clause %s exists" % c4)
        for a in set(re.findall(r"A\d\b", txt)):
            A(a + " " in app, "appendix section %s exists" % a)
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(target, PK.FILES["exhibit"]))
    A("Bayfield terms" in wb.sheetnames and "Bayfield terms" in gold, "the golden's sheet citation resolves")
    # H20: the prompt carries the institutional nouns the subdomain turns on
    prompt = open(os.path.join(task_dir, "prompt.txt"), encoding="utf-8").read()
    for noun in ("cost and market impact review", "commercial spending", "notice N25-014", "outpatient", "physician"):
        A(noun in prompt, "the prompt names '%s'" % noun)
    A(len(prompt) < 1000, "the prompt is under 1,000 characters")
    A("\u2014" not in prompt and "\u2013" not in prompt, "no em or en dash in the prompt")
    A("\n" not in prompt.strip() and not re.search(r"[`#|*\[\]]", prompt), "the prompt is one plain-text paragraph")
    A("?" in " ".join(re.split(r"(?<=[.?!])\s+", prompt)[:2]), "the prompt leads with its question")
    # H11: one write-up and one prompt in the task tree, and no prompt.md left
    names = []
    for root, _, files in os.walk(task_dir):
        names += [f for f in files if f in ("submission.md", "prompt.md", "prompt.txt")]
    A(sorted(names) == ["prompt.txt", "submission.md"], "one submission.md and one prompt.txt in the task tree")
