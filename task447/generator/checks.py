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


def seen_variant(ctx, **kw):
    X, zc, spans, ctrl, bmg = ctx
    return G.patients_seen(X, zc, ctrl, bmg, **kw)


def referred_variant(ctx, **kw):
    X, zc, spans, ctrl, bmg = ctx
    return G.patients_referred(X, zc, ctrl, spans, bmg, **kw)


# the filed rules that move a figure (the physician rule, A4, and the latest version move none: Mishicot's nurse
# practitioner holds no specialty and its patients see its physicians, a corrected visit keeps its patient, and no
# independent practice's referral is replaced or voided; both are asserted no-ops below)
SEEN_AXES = {"link": [True, False], "specialty": ["provider", "claim"], "telehealth": [False, True],
             "residence": [True, False]}
REFERRED_AXES = {"link": [True, False], "residence": [True, False]}
SEEN_STOPS = {"every member key a person (the cracker)": dict(link=False),
              "the claim's taxonomy": dict(specialty="claim"),
              "telehealth counted": dict(telehealth=True),
              "residence not read": dict(residence=False)}
REFERRED_STOPS = {"every member key a person (the cracker)": dict(link=False),
                  "residence not read": dict(residence=False)}
SEEN_NOOPS = {"nurse practitioners counted": dict(physicians=False), "versions as filed": dict(versions="as filed")}
REFERRED_NOOPS = {"versions as filed": dict(versions="as filed")}
# the asks' rows of the semantic fork table carried by the stops, the no-ops and the hazards (SF15, the person, is
# convergence_checks'; SF17, SF18, SF22 and SF23 are ask_fork_checks')
FORK_OF = {"every member key a person (the cracker)": "SF15", "residence not read": "SF16",
           "Mishicot Family Practice left out": "SF19", "the claim's taxonomy": "SF20", "telehealth counted": "SF21",
           "rule 4.03's runout read in": "SF24", "nurse practitioners counted": "SF25", "versions as filed": "SF26"}


def exhibit_truth(wd, packed):
    """Both exhibits from the simulation's own people and services, without the claim files or their keys: every
    person once, residence from the member's address on the day, specialty and practice from the physician."""
    mem, people, lines = wd["mem"], wd["people"], wd["lines"]
    spec = {"FM": "primary care", "IM": "primary care", "PED": "primary care", "GI": "gastroenterology",
            "ORTH": "orthopaedic surgery", "CARD": "cardiovascular disease"}
    office = {str(c) for c in range(99202, 99216)}
    names = {k: v[0] for k, v in O.PRACTICES.items()}
    indep = ("RRF", "AFH", "KAC", "MDC", "SOA")
    seen = defaultdict(set)
    for l in lines:
        if l["kind"] != "prof" or l["code"] not in office or l["tele"] is not None or l["tag"] in PK.MAIN_TAGS:
            continue
        if W.ZIP_COUNTY[l["site_zip"]] not in G.EX_COUNTIES or W.ZIP_COUNTY[mem.zip_on(l["member"], l["date"])] not in G.EX_COUNTIES:
            continue
        sp = spec.get(people[l["rnd_npi"]]["spec"])
        if sp is None:
            continue
        if l["practice"] in ("LMG", "MFP"):
            seen[("Ledgestone Health", sp)].add(l["member"])
        elif l["practice"] == "KPN":
            seen[("Kinnickinnic Health", sp)].add(l["member"])
        elif l["practice"] in indep:
            seen[(names[l["practice"]], None)].add(l["member"])
    referred = defaultdict(set)
    for l in lines:
        if l["kind"] != "fac" or l["date"].year != 2024 or l["practice"] not in indep:
            continue
        fam = W.CPT[l["cpt"]][1]
        if fam not in G.EX1_LINES or W.ZIP_COUNTY[mem.zip_on(l["member"], l["date"])] not in G.EX_COUNTIES:
            continue
        referred[(names[l["practice"]], fam)].add(l["member"])
    return {k: len(v) for k, v in seen.items()}, {k: len(v) for k, v in referred.items()}


def exhibit_checks(target, wd, packed, g):
    ctx = exhibit_context(target)
    t1, t2 = exhibit_truth(wd, packed)
    g1, g2 = g["ex1"], g["ex2"]
    for k, v in g1.items():
        A(v == t1.get(k, 0), "Exhibit 1 %s reproduces the simulation's patients (%d / %d)" % (k, v, t1.get(k, 0)))
    for k, v in g2.items():
        A(v == t2.get(k, 0), "Exhibit 2 %s reproduces the simulation's patients (%d / %d)" % (k, v, t2.get(k, 0)))
    A(min(g1.values()) >= 30 and min(g2.values()) >= 30, "every exhibit cell holds thirty patients or more")
    REPORT["ex1_stops"], REPORT["ex2_stops"] = {}, {}
    # the stops: the cracker files every figure off the golden; every other stop lands off the golden where it moves
    for stops, fn, gold, rep in ((SEEN_STOPS, lambda **kw: seen_variant(ctx, **kw), g1, "ex1_stops"),
                                 (REFERRED_STOPS, lambda **kw: referred_variant(ctx, **kw), g2, "ex2_stops")):
        for name, kw in stops.items():
            r = fn(**kw)
            REPORT[rep][name] = {k: r[k] - gold[k] for k in gold}
            if "cracker" in name:
                A(all(r[k] != gold[k] for k in gold), "%s: the cracker files every %s figure off the golden (%s)"
                  % (FORK_OF[name], rep[:3], {k: r[k] - gold[k] for k in gold}))
            else:
                A(any(r[k] != gold[k] for k in gold), "%s: the stop '%s' moves a figure" % (FORK_OF[name], name))
    for noops, fn, gold in ((SEEN_NOOPS, lambda **kw: seen_variant(ctx, **kw), g1),
                            (REFERRED_NOOPS, lambda **kw: referred_variant(ctx, **kw), g2)):
        for name, kw in noops.items():
            A(fn(**kw) == gold, "%s: the reading '%s' moves no figure (same figures)" % (FORK_OF[name], name))
    # two hazards that are no stop, measured for the ask sheet's hazard table: A2 and A3 count whenever paid, and A4's
    # control puts Mishicot Family Practice under Ledgestone
    X0 = ctx[0]
    mfp = G.tin_of_name(X0, "Mishicot Family Practice")
    REPORT["ex_hazards"] = {}
    for name, cut in (("rule 4.03's runout read in", {"fac": lambda df: df[df["paid"] <= G.RUNOUT],
                                                       "prof": lambda df: df[df["paid"] <= G.RUNOUT]}),
                      ("Mishicot Family Practice left out", {"prof": lambda df: df[df["billing_provider_tin"] != mfp]})):
        Y = {k: v for k, v in X0.items() if not k.startswith("_")}
        for k, f_ in cut.items():
            Y[k] = f_(Y[k])
        cy = (Y,) + tuple(ctx[1:])
        r1, r2 = seen_variant(cy), referred_variant(cy)
        REPORT["ex_hazards"][name] = ([r1[k] - g1[k] for k in g1], [r2[k] - g2[k] for k in g2])
        A(any(REPORT["ex_hazards"][name][0]), "%s: the hazard '%s' moves an Exhibit 1 figure" % (FORK_OF[name], name))
        if "Mishicot" in name:
            A(r1[("Ledgestone Health", "primary care")] == 0 and r2 == g2,
              "SF19: Ledgestone's lakeshore primary-care patients are Mishicot's, and no referral moves")
    ask_fork_checks(ctx, g, target)
    # direction discipline: no pipeline of two or more mishandlings files a figure one of them moves back on the golden
    import itertools
    n_combo = 0
    for axes, fn, gold in ((SEEN_AXES, lambda **kw: seen_variant(ctx, **kw), g1),
                           (REFERRED_AXES, lambda **kw: referred_variant(ctx, **kw), g2)):
        single = {(a, v): fn(**{a: v}) for a, vals in axes.items() for v in vals[1:]}
        for combo in itertools.product(*axes.values()):
            kw = dict(zip(axes, combo))
            mis = [(a, v) for a, v in kw.items() if v != axes[a][0]]
            if len(mis) < 2:
                continue
            r = fn(**kw)
            n_combo += 1
            for k in gold:
                if any(single[m][k] != gold[k] for m in mis):
                    A(r[k] != gold[k], "combination %s files %s back on the golden" % (mis, k))
    REPORT["combos"] = n_combo
    # the referees, and no marker
    X = ctx[0]
    pv = X["provfile"].groupby("provider_npi")["primary_taxonomy"].nunique()
    A(int(pv.max()) == 1, "the provider file gives every NPI one taxonomy")
    lake = X["prof"][X["prof"]["service_facility_zip"].map(ctx[1]).isin(("Manitowoc", "Kewaunee"))]
    A(set(lake["rendering_provider_npi"]) <= set(X["provfile"]["provider_npi"]), "every lakeshore rendering NPI is on file")
    sp = [r for r in packed["fac_rows"] + packed["prof_rows"] if "second_plan" in r["device"]]
    keyb = {PK.second_key(m): m for m in PK.unlinked_members(wd["mem"])}
    A(len(sp) > 1000 and all(r["freq"] == "1" and r["orig"] == "" and "rnd_npi" in r for r in sp),
      "second-plan claims are office claims filed as originals")
    A(all(wd["mem"].second_on(keyb.get(r["member"], r["member"]), r["dos"]) == r["product"] for r in sp),
      "a second carrier's span under each")
    for key in ("fac24", "prof24"):
        df = pd.read_csv(os.path.join(target, PK.FILES[key]), dtype=str, keep_default_na=False)
        idn = (df["allowed_amount"].astype(float) - df["plan_paid_amount"].astype(float)
               - df["member_liability_amount"].astype(float)).abs()
        A(bool((idn < 0.011).all()), "%s: allowed is plan paid plus member liability on every row" % key)
        A(int(df.drop(columns=["payer_claim_control_number"]).duplicated().sum()) == 0,
          "%s: no exact duplicate even without the claim number" % key)
    gt = [r for r in packed["prof_rows"] if "group_taxonomy" in r["device"]]
    A(len(gt) > 1000 and all(r["practice"] == "KPN" for r in gt), "the group taxonomy sits on Kinnickinnic's lines only")
    device_checks(target, wd, packed, ctx, g)
    convergence_checks(target, wd, packed, ctx, g)


ATTRIBUTION = "A visit counts for the system or the practice under whose taxpayer identification numbers its claim was billed."


def ask_fork_checks(ctx, g, target):
    """The asks' fork rows no stop carries: SF17 (a practice of a specialty), SF18 (the independent practices), SF22 (the
    referring physician's practice), SF23 (the referred patients are every resident referred, not Exhibit 1's) and SF27
    (the system or practice a visit counts for)."""
    X, zc, spans, ctrl, bmg = ctx
    # SF27: A2's attribution sentence reads back through both PDF extractors (pdfplumber, the checks'; pypdf, the
    # verifier's), and every Exhibit 1 figure files under it: the visit counts for the number its claim was billed
    # under. The one physician holding two numbers at once (Brightwater's and Kinnickinnic Physician Network's) is the
    # only place the readings part: his Kinnickinnic-billed patients are Kinnickinnic's, his Brightwater-billed ones not.
    from pypdf import PdfReader
    flat = lambda t: re.sub(r"\s+", " ", t)
    app = os.path.join(target, DC.APPENDIX)
    A(ATTRIBUTION in flat(pdf_text(app)), "SF27: A2's attribution sentence reads back through pdfplumber")
    A(ATTRIBUTION in flat(" ".join(pg.extract_text() or "" for pg in PdfReader(app).pages)),
      "SF27: A2's attribution sentence reads back through pypdf")
    rule = flat(pdf_text(os.path.join(target, DC.RULE)))
    A("billed under its taxpayer identification numbers" in rule,
      "SF27: the sentence agrees with rule 4.03's 'billed under its taxpayer identification numbers'")
    A(G.patients_seen(X, zc, ctrl, bmg, attribution="claim") == g["ex1"], "SF27: every Exhibit 1 figure files under A2's "
      "attribution sentence (each visit for the number its claim was billed under)")
    two = sorted({n for n, lst in spans.items() for d in pd.date_range(G.BASE_START, G.BASE_END, freq="MS")
                  if len({t for t, s_, e_ in lst if s_ <= d <= e_}) > 1})
    A(len(two) == 1 and {t for t, s_, e_ in spans[two[0]] if e_ >= G.BASE_START} >= {bmg, G.tin_of_name(X, "Kinnickinnic Physician Network")},
      "SF27: one physician bills under two numbers at once in 2024, Brightwater's and Kinnickinnic Physician Network's")
    kgi = ("Kinnickinnic Health", "gastroenterology")
    seen = G.patients_seen(X, zc, ctrl, bmg, sets=True)[kgi]
    alias = G.persons(X)
    p = X["prof"]
    v = p[(p["rendering_provider_npi"] == two[0]) & (p["dos"].dt.year == 2024) & p["procedure_code"].isin(G.OFFICE)]
    kpn = {alias.get(m, m) for m in v.loc[v["billing_provider_tin"] != bmg, "member_id"]}
    only_bmg = {alias.get(m, m) for m in v.loc[v["billing_provider_tin"] == bmg, "member_id"]} - kpn
    A(bool(seen & kpn) and not (seen & only_bmg), "SF27: Kinnickinnic gastroenterology (%d) holds the physician's "
      "Kinnickinnic-billed patients and none billed only under Brightwater's number" % g["ex1"][kgi])
    REPORT["sf27"] = {}
    for how in ("history", "date", "exclusive"):
        r = G.patients_seen(X, zc, ctrl, bmg, attribution=how)
        moved = {k: r[k] for k in g["ex1"] if r[k] != g["ex1"][k]}
        REPORT["sf27"][how] = moved
        A(set(moved) == {kgi}, "SF27: the reading '%s' moves Kinnickinnic gastroenterology alone (%s against %d)"
          % (how, moved, g["ex1"][kgi]))
    ind = G.independents(X, zc, ctrl, bmg)
    pv = X["provfile"]
    for tin, name, sp in ind:
        tx = {t for t in pv.loc[pv["billing_tin"] == tin, "primary_taxonomy"] if str(t)[:3] in G.PHYS_TAX}
        named = ("gastroenterology" if "Digestive" in name else "orthopaedic surgery" if "Orthopaedic" in name
                 else "primary care")
        A({G.SPECIALTY[t] for t in tx} == {sp} and sp == named, "SF17: %s's physicians all hold %s, as its name says"
          % (name, sp))
    p = X["prof"]
    lake = p[(p["dos"].dt.year == 2024) & p["procedure_code"].isin(G.OFFICE) & p["service_facility_zip"].map(zc).isin(G.EX_COUNTIES)]
    reg = X["register"]
    cin = set(reg.loc[reg["relationship"].str.contains("clinically integrated"), "entity_tin"])
    A(bool(cin) and not (cin & set(lake["billing_provider_tin"])),
      "SF18: no clinically integrated network participant bills an office visit in the two counties")
    A(len(ind) == len({t for t, _, _ in ind}) and bmg not in {t for t, _, _ in ind},
      "SF18: the independent practices are the uncontrolled numbers billing lakeshore visits, Brightwater's apart")
    pf = defaultdict(list)
    for n, t in zip(pv["provider_npi"], pv["billing_tin"]):
        if (t, pd.Timestamp.min, pd.Timestamp.max) not in pf[n]:
            pf[n].append((t, pd.Timestamp.min, pd.Timestamp.max))
    A(G.patients_referred(X, zc, ctrl, dict(pf), bmg) == g["ex2"],
      "SF22: the provider file's billing numbers name the same referring practices (same figures)")
    seen = G.patients_seen(X, zc, ctrl, bmg, sets=True)
    ref = G.patients_referred(X, zc, ctrl, spans, bmg, sets=True)
    REPORT["sf23"] = {c: len(v & seen[(c[0], None)]) - g["ex2"][c] for c, v in ref.items()}
    A(all(v < 0 for v in REPORT["sf23"].values()), "SF23: restricting the referred patients to those the practice saw "
      "in the office moves every Exhibit 2 figure (%s); the prompt names the residents" % REPORT["sf23"])


def device_checks(target, wd, packed, ctx, g):
    """The two primaries. Exhibit 1, the second plans' keys: every second key in the files holds only a second
    carrier's office claims and links back to its member through the claims alone (golden.link_members), no other key
    does, and the second keys look like any dependent's. Exhibit 2, the second records at one carrier: every one holds
    one facility service billed again under it, links back through it alone (golden.link_records), and no other key
    does. Neither touches the main call's rows or the other exhibit."""
    X, zc, spans, ctrl, bmg = ctx
    mem = wd["mem"]
    keyb = {PK.second_key(m): m for m in PK.unlinked_members(mem)}
    keyd = {inf["dup"][0]: m for m, inf in mem.info.items() if inf.get("dup")}
    A(not ((set(keyb) | set(keyd)) & set(mem.info)) and not (set(keyb) & set(keyd)), "no second key is another member's key")
    rd = lambda k: pd.read_csv(os.path.join(target, PK.FILES[k]), dtype=str, keep_default_na=False)
    f24, p24, el = rd("fac24"), rd("prof24"), rd("elig")
    b_in = set(p24["member_id"]) & set(keyb)
    d_in = set(f24["member_id"]) & set(keyd)
    A(not (set(f24["member_id"]) & set(keyb)) and not (set(p24["member_id"]) & set(keyd)),
      "the second plans' keys hold only office claims and the second records only facility claims")
    A(G.link_members(X) == {b: keyb[b] for b in b_in}, "the second plans' keys link to their members and no other key "
      "does (%d)" % len(b_in))
    # the second records, as pairs (a record opened on the day the member's own coverage starts has no earlier one);
    # the only other keys one carrier's claims join are two of the main call's own patients, namesakes on one service
    # (pack.separate_namesakes cannot move a frozen row), in no exhibit cell
    pairs = lambda d: {frozenset(kv) for kv in d.items()}
    lr = G.link_records(X)
    A(pairs({d: keyd[d] for d in d_in}) <= pairs(lr), "the second records link to their members (%d)" % len(d_in))
    extra = pairs(lr) - pairs({d: keyd[d] for d in d_in})
    frozen = {l["member"] for l in wd["lines"] if l["tag"] in PK.MAIN_TAGS}
    A(all(m in frozen for pr in extra for m in pr), "no other key is joined at one carrier but two of the main call's "
      "own patients (%d pairs)" % len(extra))
    alias = {k: v for k, v in G.persons(X).items() if not any(k in pr for pr in extra)}
    split = lambda m, d: alias.get(m, m)
    A(seen_variant(ctx, link=split) == g["ex1"] and referred_variant(ctx, link=split) == g["ex2"],
      "the main call's namesake pairs move no exhibit figure")
    REPORT["frozen_joined"] = len(extra)
    eb = el[el["member_id"].isin(b_in)]
    A(set(eb["relationship_code"]) <= {"01", "19"} and int(eb.groupby("member_id")["submitter_code"].nunique().max()) == 1,
      "a second plan's key holds spans with one carrier, as a spouse or child")
    ed = el[el["member_id"].isin(d_in)]
    own = el[el["member_id"].isin([keyd[d] for d in d_in])]
    A(set(zip(ed["submitter_code"], ed["product_id"])) <= set(zip(own["submitter_code"], own["product_id"])),
      "a second record holds the member's own carrier and product")
    span = lambda df, key: sorted(tuple(r_[1:]) for r_ in df.assign(member_id=df["member_id"].map(key)).itertuples(index=False))
    A(span(ed, keyd) == span(own, lambda m: m), "a second record's spans repeat its member's own, from the start")
    starts = el.groupby("member_id")["coverage_start"].min()
    A(set(starts[starts.index.isin(d_in)]) <= set(starts[~starts.index.isin(d_in)]),
      "a second record's coverage starts on a day other keys' coverage starts on")
    dd = f24[f24["member_id"].isin(d_in)]
    A(len(dd) >= len(d_in) and bool((dd.groupby("member_id")["payer_claim_control_number"].nunique() == 1).all()),
      "each second record holds one facility claim (%d records, %d lines)" % (len(d_in), len(dd)))
    blind = [c for c in f24.columns if c not in ("member_id", "payer_claim_control_number", "paid_date")]
    twin = f24[f24.duplicated(blind, keep=False)]
    A(not twin["member_id"].isin(d_in).any(), "a second record's claim carries its own cost sharing, so no claim line "
      "repeats it but for the member key, the claim number and the paid date")
    # every cell of each exhibit carries its own device and only its own
    t_seen = seen_variant(ctx, link=False)
    t_ref = referred_variant(ctx, link=False)
    only_b = lambda m, d: keyb.get(m, m)
    only_d = lambda m, d: keyd.get(m, m)
    A(all(seen_variant(ctx, link=only_b)[k] == g["ex1"][k] for k in g["ex1"]),
      "the second plans' keys alone account for every Exhibit 1 figure the cracker misses")
    A(all(referred_variant(ctx, link=only_d)[k] == g["ex2"][k] for k in g["ex2"]),
      "the second records alone account for every Exhibit 2 figure the cracker misses")
    A(all(t_seen[k] > g["ex1"][k] for k in g["ex1"]) and all(t_ref[k] > g["ex2"][k] for k in g["ex2"]),
      "every cell of both exhibits holds a person under two keys")
    # separation: no device row in the main call's population, by count from the shipped rows
    pmain = p24[p24["billing_provider_tin"] == bmg]
    ra = rd("reassign")
    bmg_npis = set(ra.loc[ra["billing_tin"] == bmg, "npi"])
    hist = rd("fachist")
    fmain = f24[f24["referring_provider_npi"].isin(bmg_npis | set(hist["REF_NPI"]))]
    main_members = set(fmain["member_id"]) | set(pmain["member_id"]) | set(hist["MEMBER_ID"])
    A(not (main_members & (set(keyb) | set(keyd) | set(keyb.values()) | set(keyd.values()))),
      "no main-call member is held under two keys")
    A(bool((pmain["claim_frequency_code"] == "1").all()), "Brightwater's professional rows are originals")
    A(not (set(fmain["payer_claim_control_number"]) & set(f24.loc[f24["member_id"].isin(d_in), "payer_claim_control_number"])),
      "no second record's claim is a main-call row")


def convergence_checks(target, wd, packed, ctx, g):
    """C1 on the person each exhibit counts. Every matching of member keys that reads the claims' services (birth year,
    sex and ZIP that day with one service, across carriers or at one carrier, or the golden's: with the second plan's
    pricing, or the one carrier's second submission) files the same twenty figures; the matchings that do not (each
    member key a person, birth year, sex and ZIP alone, or with the carrier) are the device and its over-cleaning half
    (the carrier's: Exhibit 2's, every figure off there; on Exhibit 1 its two errors run opposite ways and are recorded).
    pack.separate_namesakes keeps any two people outside the main call's frozen members from sharing a birth year, sex
    and ZIP and one service on one day; the frozen pairs left are Brightwater's own patients, in neither exhibit."""
    X, zc, spans, ctrl, bmg = ctx
    on = G._demo_index(X)
    el = X["elig"]
    car_of = el.groupby("member_id")["submitter_code"].first().to_dict()

    def union(pairs):
        parent = {}

        def find(m):
            while parent.get(m, m) != m:
                m = parent[m]
            return m
        for a, b in pairs:
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[max(ra, rb)] = min(ra, rb)
        return lambda m, d: find(m)

    def service_pairs(any_carrier):
        out = set()
        for df, cols in ((X["fac"], ["procedure_code", "procedure_modifier_1", "service_facility_npi", "referring_provider_npi"]),
                         (X["prof"], ["procedure_code", "procedure_modifier_1", "rendering_provider_npi", "billing_provider_tin"])):
            f = df[(df["dos"].dt.year == 2024) & (df["claim_frequency_code"] == "1")]
            groups = defaultdict(list)
            for t, sub, m in zip(zip(f["dos"], *[f[c] for c in cols], f["qty"]), f["submitter_code"], f["member_id"]):
                groups[t].append((sub, m))
            for t, lst in groups.items():
                for i in range(len(lst)):
                    for j in range(i + 1, len(lst)):
                        (s1, m1), (s2, m2) = lst[i], lst[j]
                        if m1 != m2 and (any_carrier or s1 != s2) and on(m1, t[0]) is not None and on(m1, t[0]) == on(m2, t[0]):
                            out.add((m1, m2))
        return out
    readings = {
        "every member key a person": (False, False),
        "birth year, sex and ZIP alone": (lambda m, d: ("p",) + on(m, d) if on(m, d) else m, False),
        "the carrier, birth year, sex and ZIP": (lambda m, d: ("p", car_of.get(m)) + on(m, d) if on(m, d) else m, "ex2"),
        "with one service under two carriers": (union(service_pairs(False)), None),
        "with one service under any carrier": (union(service_pairs(True)), True),
        "the golden's: the pricing and the second submission": (True, True),
    }
    REPORT["readings"] = {}
    for name, (link, must) in readings.items():
        r1 = seen_variant(ctx, link=link)
        r2 = referred_variant(ctx, link=link)
        d1 = [r1[k] - g["ex1"][k] for k in g["ex1"]]
        d2 = [r2[k] - g["ex2"][k] for k in g["ex2"]]
        REPORT["readings"][name] = (d1, d2)
        if must is True:
            A(not any(d1) and not any(d2), "SF15: matching the keys %s files the golden's twenty figures (%s; %s)"
              % (name, d1, d2))
        elif must is False:
            A(all(d1) and all(d2), "SF15: matching the keys %s files every figure off the golden (%s; %s)" % (name, d1, d2))
        elif must == "ex2":
            # Exhibit 2's own over-cleaning half; on Exhibit 1 it leaves the second plans' keys apart and merges people
            # at one carrier, two errors in opposite directions, recorded as measured (ceiling.py prints its keeps)
            A(all(d2), "SF15: matching the keys %s files every Exhibit 2 figure off the golden (%s)" % (name, d2))
            REPORT["one_carrier_ex1_kept"] = [k for k, x in zip(g["ex1"], d1) if not x]
    REPORT["frozen_namesakes"] = len(packed["frozen_namesakes"])
    main_members = {l["member"] for l in wd["lines"] if l["tag"] in PK.MAIN_TAGS}
    A(all(a in main_members and b in main_members for _, a, b in packed["frozen_namesakes"]),
      "every namesake pair left is two of the main call's own members (%d)" % len(packed["frozen_namesakes"]))


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
            A("\u2014" not in open(os.path.join(target, f), encoding="utf-8").read(), "no em dash in %s" % f)


def pdf_text(path):
    with pdfplumber.open(path) as pdf:
        return " ".join(pg.extract_text() or "" for pg in pdf.pages)


DESCRIBING = re.compile(r"dictionar|manifest|readme|read_me|codebook|field_?notes|field_?guide|definitions|schema|"
                        r"file_?list|layout|extract_?notes|export_?notes|data_?notes|how_to_read|about_the_data")


def describing_file_checks(target):
    """dataset-generation section 3: no shipped file or sheet describes the data, by name or by content. By
    name: no file, sheet or JSON key named as a dictionary, manifest, readme, notes or schema. By content: no
    document names more than a fifth of any data file's columns verbatim. The closures the removed data
    dictionary used to carry are asserted where they now live (the appendix's A6 counties, the claims' own
    frequency codes)."""
    import openpyxl
    files = sorted(os.listdir(target))
    for f in files:
        A(not DESCRIBING.search(f.lower()), "no shipped file is named as a description of the data (%s)" % f)
    for f in files:
        if f.endswith(".xlsx"):
            for sh in openpyxl.load_workbook(os.path.join(target, f), read_only=True).sheetnames:
                A(not DESCRIBING.search(sh.lower()) and "note" not in sh.lower(), "no describing sheet (%s: %s)" % (f, sh))
    cols = {}
    for f in files:
        if f.endswith(".csv"):
            cols[f] = [c for c in open(os.path.join(target, f), encoding="utf-8").readline().strip().split(",")
                       if "_" in c and len(c) > 4]
    for f in files:
        if f.endswith(".pdf"):
            t = pdf_text(os.path.join(target, f))
            for csvf, cs in cols.items():
                hit = sum(1 for c in cs if c in t)
                A(hit <= max(1, len(cs) // 5), "%s names %d of %s's %d columns" % (f, hit, csvf, len(cs)))
    # A6, the closure moved from the dictionary: the appendix assigns every ZIP the claims and spans carry to
    # one county, read through the extractor the golden and the verifier use, and it is the world's assignment
    zc = G.zip_county(target)
    A(zc == W.ZIP_COUNTY, "the appendix's A6 assigns each region ZIP to its county (%d ZIPs)" % len(zc))
    el = pd.read_csv(os.path.join(target, PK.FILES["elig"]), dtype=str, usecols=["member_zip"])
    pr = pd.read_csv(os.path.join(target, PK.FILES["prof24"]), dtype=str, usecols=["service_facility_zip"])
    A(set(el["member_zip"]) <= set(zc), "every eligibility ZIP has a county in A6")
    A(set(pr["service_facility_zip"]) <= set(zc), "every professional service location ZIP has a county in A6")
    # rows 15 and 19 of the closure table: the claims carry their own version codes (X12 frequency 1, 7, 8;
    # layout 2.4's O, R, V), a void names the claim it cancels and carries negative units and amounts, a
    # replacement names the claim it supersedes, and the main call's rows carry originals only
    fac = pd.read_csv(os.path.join(target, PK.FILES["fac24"]), dtype=str)
    A(set(fac["claim_frequency_code"]) <= {"1", "7", "8"}, "2024 facility frequency codes are 1, 7 and 8")
    cno = set(fac["payer_claim_control_number"])
    for code in ("7", "8"):
        sub = fac[fac["claim_frequency_code"] == code]
        A(len(sub) > 0 and sub["original_claim_control_number"].isin(cno).all(),
          "every frequency %s line names a claim in the file (%d lines)" % (code, len(sub)))
    v = fac[fac["claim_frequency_code"] == "8"]
    A((v["quantity"].astype(float) < 0).all() and (v["allowed_amount"].astype(float) < 0).all(),
      "every void line carries negative units and amount")
    o = fac[fac["claim_frequency_code"] == "1"]
    A(o["original_claim_control_number"].fillna("").eq("").all(), "an original names no prior claim")
    hist = pd.read_csv(os.path.join(target, PK.FILES["fachist"]), dtype=str, usecols=["CLM_STATUS"])
    A(set(hist["CLM_STATUS"]) == {"O"}, "the 2021 to 2023 extract carries originals only")


def document_checks(target):
    texts = {f: pdf_text(os.path.join(target, f)) for f in (DC.RULE, DC.APPENDIX, DC.NOTICE)}
    for f, t in texts.items():
        low = t.lower()
        A("\u2014" not in t, "no em dash in %s" % f)
        for w in ("capture", "steer", "placement", "placed", "followed", "follows their"):
            A(not re.search(r"\b%s\b" % w, low), "%s carries no '%s'" % (f, w))
        A("tier" not in low, "%s never mentions tiers" % f)
    describing_file_checks(target)
    A(sum("2,000,000" in t for t in texts.values()) == 1 and "2,000,000" in texts[DC.RULE], "the threshold is stated once, in the rule")
    rule = re.sub(r"\s+", " ", texts[DC.RULE])
    A("share expected for that service under the member's product as the product stands in the projection year"
      in rule and "in whole per cent" in rule,
      "the rule files the expected share's unit of analysis, the service and the product as it stands in the "
      "projection year, and its rounding")
    # SF13: the share's unit of analysis is filed, so no reader can pool across products
    A("A share is estimated for a service and a product" in rule and
      "the office does not estimate one share across products" in rule,
      "4.05 says what each share is a share of, so its own sentence is not a complete recipe")
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
    counts = list(g["ex1"].values()) + list(g["ex2"].values())
    A(len(set(counts)) == len(counts) and all(v % 100 for v in counts),
      "the twenty patient counts differ and none is a round hundred")


# ------------------------------------------------------------------ the semantic fork table (design note SF1 to SF14)
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
    # SF14 Bayfield's terms: the column's header names the unit and the values are whole per cent of the Medicare
    # amount; read so, they price every Bayfield code at the agreement's rate and reproduce the referred increase
    import openpyxl
    import maincall as MC
    wb = openpyxl.load_workbook(os.path.join(target, PK.FILES["exhibit"]), data_only=True)
    rows = list(wb["Bayfield terms"].iter_rows(values_only=True))
    hi = next(i for i, r in enumerate(rows) if r and r[0] == "Service category")
    vals = [r[2] for r in rows[hi + 1:] if r and r[0]]
    A(rows[hi][2] == "Percent of Medicare" and len(vals) == 5 and all(isinstance(v, int) and 100 < v < 500 for v in vals),
      "SF14 the Bayfield column names its unit and holds whole per cent (%s)" % vals)
    bay = {c: r for (car, c), r in g["fac_rate"].items() if car == "Bayfield Mutual Health"}
    A(len(bay) > 10 and all(r == PK.S.ldg_facility_rate("C2", c, 2025) for c, r in bay.items()),
      "SF14 read as per cent, the column prices every Bayfield code at the agreement's rate (%d codes)" % len(bay))
    A(abs(g["referred"] - MC.load_ref()["figures"]["referred"]) < 1e-6 and g["call"] == "proceed",
      "SF14 that reading reproduces the referred increase (%.0f) and the call" % g["referred"])


# ------------------------------------------------------------------ the write-up agrees with the golden
def submission_check(task_dir, figs, g):
    txt = open(os.path.join(task_dir, "submission.md"), encoding="utf-8").read()
    A("\u2014" not in txt, "no em dash in submission.md")
    money = lambda v: "${:,.0f}".format(v)
    A("$%s million" % figs["total_m"] in txt, "submission carries the total")
    A(money(figs["professional"]) in txt and money(figs["referred"]) in txt, "submission carries the two parts")
    A("%d%%" % round(100 * g["c1"]) in txt, "submission carries the tier-one share")
    for line in block4_lines(figs):
        A(line in txt, "submission carries %s" % line.strip())
    A(("Proceed" in txt) == (figs["call"] == "proceed"), "submission carries the call")
    gold = pdf_text(os.path.join(task_dir, "golden", "N25-014_preliminary_review.pdf"))
    flat = re.sub(r"\s+", " ", gold)
    labels = (("primary care", "Primary care"), ("gastroenterology", "Gastroenterology"),
              ("orthopaedic surgery", "Orthopaedics"), ("cardiovascular disease", "Cardiology"))
    for sp, lab in labels:
        row = "%s %s %s" % (lab, figs["ex1"]["Ledgestone Health|" + sp], figs["ex1"]["Kinnickinnic Health|" + sp])
        A(row in flat, "the golden PDF carries Exhibit 1's %s row as the write-up does" % lab)
    for k, v in figs["ex1"].items():
        if "|" not in k:
            A("%s %s" % (k, v) in flat, "the golden PDF carries %s's patients as the write-up does" % k)
    for k, v in figs["ex2"].items():
        A(v in flat, "the golden PDF carries Exhibit 2 %s" % k)


LINE_NAMES = {"IMG": "imaging", "ENDO": "endoscopy", "ARTH": "arthroscopy"}
SPEC_NAMES = (("primary care", "primary care"), ("gastroenterology", "gastroenterology"),
              ("orthopaedic surgery", "orthopaedics"), ("cardiovascular disease", "cardiology"))


def block4_lines(figs):
    """The Deliverable Answers lines for the two exhibits, as submission.md states them."""
    out = []
    for g_ in ("Ledgestone Health", "Kinnickinnic Health"):
        out.append("   - %s: %s" % (g_, "; ".join("%s %s" % (lab, figs["ex1"]["%s|%s" % (g_, sp)]) for sp, lab in SPEC_NAMES)))
    for k, v in figs["ex1"].items():
        if "|" not in k:
            out.append("   - %s: %s" % (k, v))
    pr = defaultdict(list)
    for k, v in figs["ex2"].items():
        n, ln = k.split("|")
        pr[n].append((["IMG", "ENDO", "ARTH"].index(ln), "%s %s" % (LINE_NAMES[ln], v)))
    for n in sorted(pr):
        out.append("   - %s: %s" % (n, "; ".join(x for _, x in sorted(pr[n]))))
    return out


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
