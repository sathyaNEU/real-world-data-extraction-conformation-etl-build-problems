"""task230 checks: the input gates, the three rules executed on the clean truth (R1 to R3c), the ladder's rungs and
margins, the estimators' convergence, the reflex routes, the semantic fork rows (SF1 to SF14), Layer 1 neutrality, the
ask devices and their separation from the main call, the context artifact, the bins and the realism sweep."""
import json
import os
import re
import zipfile

import numpy as np
import pandas as pd

import estim as E
import params as P
import sim
import world as W

G = W.GROUPS
GOLD = ["24", "25", "35", "41", "71", "93"]
LADDER = {"default": ["35", "93"], "rule": ["35", "41", "93"], "bt_old": ["35", "93"], "bt_new": ["24", "35", "41", "93"],
          "route_old": ["24", "35", "71", "93"], "golden": GOLD}
MARGIN = 0.20     # every rung clears the warning line by at least this many points (1.1 times the line)
PEOPLE = ["Timothy Taggart", "Lesley Ahearne", "Tracey Brien", "Erica Phayre"]


def margin(b, tg):
    return min((abs(v) - P.WARNING) if g in tg else (P.WARNING - abs(v)) for g, v in zip(G, b))


def bin_margin(vals):
    """distance of every variant from the edges of the golden's one-decimal bin"""
    v = np.vstack(vals)
    b = np.array([float(f"{x:.1f}") for x in v[0]])
    return float(np.min(np.minimum(v.min(0) - (b - 0.05), (b + 0.05) - v.max(0))))


def run(target, golden, S, U, Cd, T, A, D, out, R, facts):
    n = [0]

    def ok(c, label):
        assert c, label
        n[0] += 1

    files = sorted(os.listdir(target))
    task = os.path.dirname(target)
    meta = json.load(open(os.path.join(task, "metadata.json")))
    gold = out["golden"]
    # ---------------------------------------------------------------- input gates
    ok(len(files) >= 10, "gate: 10 or more files")
    ok(len({f.rsplit(".", 1)[1] for f in files}) >= 3, "gate: 3 or more formats")
    ok(max(len(D["reg"]), len(D["ext"]), len(D["vis"])) >= 25000, "gate: a file of 25,000 rows or more")
    ok(len(meta["distractor_files"]) >= 2 and all(d in files for d in meta["distractor_files"]), "gate: two distractors")
    ok(not any("distractor" in f.lower() for f in files), "gate: no file named after its role")
    # ---------------------------------------------------------------- R1: the field's raw material ships
    for f in files:
        if f.endswith(".csv"):
            head = open(os.path.join(target, f), encoding="utf-8").readline().lower()
            ok("bias" not in head and "warning" not in head, "R1: no column holds a bias or a warning (%s)" % f)
    ok({"reference_code", "production_code", "autocoder_code", "autocoder_score", "selection_interval"} <= set(D["stu"].columns)
       and len(D["stu"]) > 50000, "R1: the study ships its write-ins with production, suggested and reference codes")
    ok("proxy_respondent" in D["vis"].columns and "questionnaire_id" in D["reg"].columns,
       "R1: the route of every form is in the field and receipt records, never a column of the study")
    ok("route" not in D["stu"].columns and "route" not in D["ext"].columns, "R1: no shipped column states the route")
    # ---------------------------------------------------------------- the clean truth (generator side)
    K = len(G)
    gi = {g: i for i, g in enumerate(G)}
    grp = lambda a: np.array([gi[x[:2]] for x in a])
    po, pn, ref = grp(Cd["prod_old"]), grp(Cd["prod_new"]), grp(Cd["ref"])
    coded = S["coded"]
    Ct = np.bincount(np.where(coded, po, pn), minlength=K)
    Tt = np.bincount(ref, minlength=K)
    truth = 100 * (Ct - Tt) / Tt
    ok(E.flags(truth) == GOLD, "truth: the release's own coding bias carries the golden flags")
    ok(margin(truth, set(GOLD)) >= 0.10, "truth: margin %.3f" % margin(truth, set(GOLD)))
    # ---------------------------------------------------------------- R3a, R3b: the ladder
    for k, want in LADDER.items():
        ok(E.flags(out[k]) == want, "rung %s files %s (got %s)" % (k, want, E.flags(out[k])))
    ok(margin(out["default"], {"35", "93"}) >= MARGIN, "R3a: the default path's margin %.3f" % margin(out["default"], {"35", "93"}))
    ok(margin(out["rule"], {"35", "41", "93"}) >= MARGIN, "rung rule margin")
    ok(margin(out["route_old"], {"24", "35", "71", "93"}) >= MARGIN, "rung route_old margin")
    ok(margin(gold, set(GOLD)) >= MARGIN, "R3b: the golden's margin %.3f" % margin(gold, set(GOLD)))
    ok(P.WARNING - abs(out["bt_new"][gi["71"]]) >= 0.20, "rung bt_new leaves 71 under the line")
    ok(len({tuple(LADDER[k]) for k in LADDER}) == 5, "separation: five distinct sets on six rungs (bt_old repeats default)")
    ok(set(E.flags(out["default"])) < set(GOLD), "R3a: the easy route's set is a strict subset: it under-warns")
    # each rung's single correction leaves a wrong answer: rule only, batch type, route only
    for k in ("rule", "bt_old", "bt_new", "route_old"):
        ok(E.flags(out[k]) != GOLD, "R3b: %s alone is wrong" % k)
    # ---------------------------------------------------------------- C1: estimator convergence (the bins)
    o_ps, _ = E.rungs(D, weights="poststrat")
    variants = [gold, out["golden_sw"], out["golden_cd"], o_ps["golden"]]
    for v in variants[1:]:
        ok(E.flags(v) == GOLD, "C1: a defensible estimator variant gives the golden flags")
    for cols in (["region_code"], ["proxy_respondent"]):
        variants.append(E.carry_finer(D, cols))
        ok(E.flags(variants[-1]) == GOLD, "C1/H14: the carry inside %s cells gives the golden flags" % cols[0])
    bm = bin_margin(variants)
    ok(bm >= 0.002, "C1: every group's bias stays in its one-decimal bin under every variant (%.4f)" % bm)
    # ---------------------------------------------------------------- reflex routes land wrong
    for f in (E.reflex_recent, E.reflex_trend, E.reflex_recode_all):
        b = f(D)
        ok(E.flags(b) != GOLD, "reflex %s lands wrong (%s)" % (f.__name__, E.flags(b)))
    tr = E.reflex_trend(D)
    away = max([P.WARNING - abs(tr[gi[g]]) for g in GOLD] + [abs(v) - P.WARNING for g, v in zip(G, tr) if g not in GOLD])
    ok(away >= 0.10, "reflex trend misses by %.3f" % away)
    o_uw, _ = E.rungs(D, weights="unweighted")
    ok(E.flags(o_uw["default"]) != GOLD, "reflex: the unweighted study on the default path lands wrong")
    # ---------------------------------------------------------------- the design forces the route carry
    reg = E.routes(D)
    stu = D["stu"].merge(reg[["doc_id", "route"]], on="doc_id")
    stu["ld"] = pd.to_datetime("20" + stu.load_batch.str[-6:], format="%Y%m%d")
    for r in ("FS", "FP"):
        s = stu[stu.route == r]
        cut = s.ld.median()
        early, late = s[s.ld <= cut], s[s.ld > cut]
        e1 = (early.production_code.str[:2] != early.reference_code.str[:2]).mean()
        e2 = (late.production_code.str[:2] != late.reference_code.str[:2]).mean()
        p_ = (e1 * len(early) + e2 * len(late)) / len(s)
        se = np.sqrt(p_ * (1 - p_) * (1 / len(early) + 1 / len(late)))
        ok(abs(e1 - e2) < 2.5 * se, "design: %s write-ins code alike in the season's two halves (%.4f, %.4f, se %.4f)"
           % (r, e1, e2, se))
    fu = stu[stu.batch_type == "FOLLOW-UP"]
    px_early = (fu[fu.ld < pd.Timestamp("2026-07-20")].route == "FP").mean()
    px_late = (fu[fu.ld >= pd.Timestamp("2026-07-20")].route == "FP").mean()
    ok(px_late > px_early + 0.15, "design: the proxy share of follow-up returns climbs through the season")
    m_px = R["FP"]["m"] / (R["FS"]["m"] + R["FP"]["m"])
    c_px = R["FP"]["nc"] / (R["FS"]["nc"] + R["FP"]["nc"])
    ok(m_px > c_px + 0.25, "data-native: proxies are %.3f of the follow-up still to code against %.3f coded" % (m_px, c_px))
    # ---------------------------------------------------------------- the 0.80 rule: the study saw these coded clerically
    band = D["stu"][(D["stu"].autocoder_score.astype(float) >= 0.80) & (D["stu"].autocoder_score.astype(float) < 0.90)]
    ok((band.coding_path == "CLERICAL").all() and len(band) > 1000,
       "layer B: write-ins scoring 0.80 to 0.90 were coded clerically, and the autocoder's suggestion is stored on them")
    # ---------------------------------------------------------------- SF rows
    aoc = pd.read_csv(os.path.join(target, "aoc2026_occupation_classification.csv"), dtype=str)
    ok(sorted(aoc.isco08_sub_major.unique()) == G, "SF1: 40 sub-major groups, no armed forces")
    ok((aoc.aoc_code.str[:2] == aoc.isco08_sub_major).all() and set(D["stu"].reference_code.str[:2]) <= set(G),
       "SF2: a five-digit AOC code and a four-digit ISCO code share their sub-major group's first two digits")
    Rr = E.bias_table(D)
    Dn = sum(Rr[r]["do"] for r in Rr) + sum(Rr[r]["dn"] * Rr[r]["m"] / Rr[r]["nc"] for r in Rr)
    Tn = sum(Rr[r]["t"] for r in Rr) + sum(Rr[r]["t"] * Rr[r]["m"] / Rr[r]["nc"] for r in Rr)
    alt = 100 * Dn / (Tn + Dn)
    ok(E.flags(alt) == GOLD, "SF3: bias on the coded count instead of the reference count: same call")
    ok(min(abs(abs(v) - P.WARNING) for v in gold) > 0.2, "SF4: beyond 2.0 or at least 2.0: same call (no group near 2.0)")
    still_self = R["O"]["m"] + R["P"]["m"]
    R2 = E.bias_table(D)
    for r in ("O", "P"):
        R2[r]["m"] = 0.0
    ok(E.flags(E.carry(R2, "dn", [[r] for r in P.ROUTES])) == GOLD,
       "SF5: self-response forms not yet loaded left out (%d write-ins): same call" % still_self)
    vis = D["vis"]
    closes = vis[vis.outcome_code.isin(["10", "20"])]
    reg_q = set(D["reg"].questionnaire_id)
    orphan = closes[~closes.questionnaire_id.isin(reg_q)].questionnaire_id.nunique()
    ok(orphan == int(S["reint"].sum()), "SF6: every closing call's questionnaire is registered but the withdrawn proxies "
                                        "(%d)" % orphan)
    ok((pd.to_datetime(D["reg"].received_date) <= pd.Timestamp(P.FIELD_CLOSE)).all(),
       "SF6: every registered form was received by the close of field operations")
    ok((D["ext"].groupby(["doc_id", "person_no"]).size() == 1).all(), "SF7: one write-in a person")
    ok(int(D["reg"].occupation_writeins.astype(int).sum()) == len(S["owner"]), "SF7: write-ins are persons with a write-in")
    ok(abs(sum(Rr[r]["sw"] for r in Rr) / sum(Rr[r]["nc"] for r in Rr) - 1) < 0.002,
       "SF8: the study's selection intervals give back the coded count")
    for r in P.ROUTES:
        ok(abs(Rr[r]["sw"] / Rr[r]["nc"] - 1) < 0.01, "SF9: route %s's weighted study count within 1 per cent" % r)
    for closing in ("any_proxy", "last_call", "first_call", "sr_as_followup"):
        o2, _ = E.rungs(D, reg=E.routes(D, closing))
        ok(E.flags(o2["golden"]) == GOLD, "SF10/R2: route read as %s: same call" % closing)
    ok(all(float(f"{v:.1f}") == A["bias_r"][g] for g, v in zip(G, gold)), "SF11: one decimal on the unrounded bias")
    ok(all(str(A["bias_r"][g]) != "-0.0" for g in G), "SF11: a bias rounding to nothing is shown as 0.0")
    plan_dec = "write-ins already coded keep their codes"
    ok(plan_dec in open_xlsx_text(os.path.join(target, "census2026_processing_plan_nov2026.xlsx")).lower(),
       "SF12: the plan files that coded write-ins keep their codes")
    ok("not yet been coded on the date of an assessment is part of the release population" in docx_text(
        os.path.join(target, "OQ-4_occupation_output_quality_standard.docx")), "SF13: OQ-4 files the unobserved members")
    # SF14: the release count of the coded write-ins taken from the extract against the study's reference count
    ext_g = np.bincount(E._grp(D["ext"].production_code.values), minlength=K).astype(float)
    live = [r for r in R if R[r]["m"] > 0]
    m_rel = sum(R[r]["cn"] * R[r]["m"] / R[r]["nc"] for r in live)
    m_ref = sum(R[r]["t"] * R[r]["m"] / R[r]["nc"] for r in live)
    m_dn = sum(R[r]["dn"] * R[r]["m"] / R[r]["nc"] for r in live)
    t_all = sum(R[r]["t"] for r in R) + m_ref
    mixed = 100 * (ext_g + m_rel - t_all) / t_all
    ok(len(E.flags(mixed)) >= 10, "SF14: exact extract counts against the study's reference count warn %d groups on "
       "sampling noise" % len(E.flags(mixed)))
    d_co = sum(R[r]["do"] for r in R)
    diff = 100 * (d_co + m_dn) / (ext_g - d_co + m_ref)
    ok(E.flags(diff) == GOLD and np.max(np.abs(diff - gold)) < 0.1,
       "SF14: the difference estimator (exact counts less the study's net difference) gives the same call")
    ok("are both estimated from the same studied write-ins" in docx_text(
        os.path.join(target, "OQ-4_occupation_output_quality_standard.docx")), "SF14: OQ-4 3.3 files both counts from "
       "the same studied write-ins")
    # ---------------------------------------------------------------- R2: Layer 1 neutrality (each item mishandled)
    ok(E.flags(E.rungs(D, reg=E.routes(D, "any_proxy"))[0]["golden"]) == GOLD, "R2: re-interviews read as proxy")
    ok(E.flags(E.rungs(D, reg=E.routes(D, "sr_as_followup"))[0]["golden"]) == GOLD, "R2: late self-responses read as follow-up")
    ok(set(D["ext"].production_code.str.len()) == {4, 5}, "R2: four- and five-digit production codes both ship")
    ok(D["ext"].coding_week.min() == 1 and D["ext"].coding_week.max() == 28, "R2: coding weeks 1 to 28")
    # ---------------------------------------------------------------- R3c: no plant
    plan_txt = open_xlsx_text(os.path.join(target, "census2026_processing_plan_nov2026.xlsx"))
    ok(not re.search(r"\b(24|25|35|41|71|93)\b.*warning", plan_txt), "R3c: no document lists warned groups")
    ok("proxy" not in plan_txt.lower(), "R3c: the capacity report never speaks of proxies")
    oq = docx_text(os.path.join(target, "OQ-4_occupation_output_quality_standard.docx"))
    ok("route" not in oq.lower() and "proxy" not in oq.lower(), "R3c: the standard files no route and no method")
    # ---------------------------------------------------------------- the context artifact recomputes
    fu_still = int(D["reg"][D["reg"].capture_mode == "FIELD"].occupation_writeins.astype(int).sum()) - int(
        D["ext"].load_batch.str.startswith("FUP").sum())
    ok(facts["plan"]["Follow-up"] == fu_still, "artifact: the plan's follow-up still to code recomputes")
    # ---------------------------------------------------------------- study design
    stu_n = D["stu"].groupby(["load_batch", "coding_path"]).size()
    ext_n = D["ext"].groupby(["load_batch", "coding_path"]).size()
    k_of = lambda lb, p: P.STUDY_K[("NRFU" if lb.startswith("FUP") else "SELF", "A" if p == "AUTO" else "C")]
    bad = 0
    for (lb, p), cnt in ext_n.items():
        k = k_of(lb, p)
        got = int(stu_n.get((lb, p), 0))
        if not (cnt // k <= got <= cnt // k + 1):
            bad += 1
    ok(bad == 0, "study: every batch and path holds its systematic share")
    ok(set(D["stu"].doc_id) <= set(D["ext"].doc_id), "study: drawn from the coded write-ins")
    # ---------------------------------------------------------------- asks
    teams, regions = A["teams"], A["regions"]
    ok(len(set(v[0] for v in teams.values())) == 5 and len(set(v[1] for v in teams.values())) == 5, "ask A: no tied team")
    ok(len(set(v[0] for v in regions.values())) == 8 and len(set(v[1] for v in regions.values())) == 8, "ask B: no tied region")
    cur = E.ask_teams(D, "current")
    ok(all(cur[t][0] != teams[t][0] for t in W.TEAMS), "ask A device: the register as at 13 November moves every team's write-ins")
    for m in ("drop_negative", "entered_on"):
        x = E.ask_teams(D, m)
        ok(all(x[t][1] != teams[t][1] for t in W.TEAMS), "ask A hazard %s moves every team's hours" % m)
    # ask A readings that converge in the records: a write-in coded after midnight belongs to the night shift that
    # started the day before; no night shift crosses a month end and no coder id changes team between the two days
    cl = D["ext"][(D["ext"].coding_path == "CLERICAL") & (D["ext"].coded_at >= "2026-05-01")]
    sday = cl.coded_at.dt.normalize() - pd.to_timedelta((cl.coded_at.dt.hour < 7).astype(int), unit="D")
    ok(int((sday.dt.month != cl.coded_at.dt.month).sum()) == 0,
       "ask A fork: every clerical write-in is coded in the month its shift started (month-end night closure)")
    oc = cl[(cl.coded_at >= "2026-09-30") & (cl.coded_at < "2026-11-02")]
    oday = oc.coded_at.dt.normalize() - pd.to_timedelta((oc.coded_at.dt.hour < 7).astype(int), unit="D")
    asg_ = E.assignments(D["moves"])
    ok((E.team_on(asg_, "coder_id", oc.coder_id.values, oc.coded_at.dt.normalize())
        == E.team_on(asg_, "coder_id", oc.coder_id.values, oday)).all(),
       "ask A fork: a coder's team on the day coded is the team on the day the shift started")
    key = E.ask_regions(D, "key_dedupe")
    ok(all(key[r][0] > regions[r][0] and key[r][1] > regions[r][1] for r in regions),
       "ask B device: re-sent calls survive a call-number dedupe in every region, calls and no-contact calls")
    day = E.ask_regions(D, "day_dedupe")
    ok(all(day[r][0] < regions[r][0] and day[r][1] < regions[r][1] for r in regions),
       "ask B over-clean: an address-and-day dedupe drops genuine same-day calls in every region")
    syn = E.ask_regions(D, "synced")
    ok(sum(syn[r][0] != regions[r][0] for r in regions) >= 6, "ask B hazard: the sync time is not the call's time")
    # separation: no device row reaches the main call
    vis_clean = vis.sort_values(["synced_at", "visit_id"]).drop_duplicates(["address_id", "visit_time", "outcome_code"])
    D2 = dict(D)
    D2["vis"] = vis_clean
    ok(E.flags(E.rungs(D2)[0]["golden"]) == GOLD and np.allclose(E.rungs(D2)[0]["golden"], gold),
       "separation: the re-sent calls move no figure of the main call")
    resent = len(vis) - len(vis_clean)
    ok(resent == int(T["vis"]["replay"].sum()) and resent > 0, "separation: the re-sent calls are exactly the replays")
    rr = vis[vis.outcome_code.isin(["10", "20"])]
    dup_q = rr[rr.duplicated("questionnaire_id", keep=False)]
    ok((dup_q.groupby("questionnaire_id").outcome_code.nunique() == 1).all(),
       "separation: a re-sent closing call repeats its questionnaire's outcome")
    # ---------------------------------------------------------------- registers (H9)
    man = pd.read_csv(os.path.join(target, "export_manifest.csv"), dtype=str)
    ok(set(man.file) == set(files) - {"export_manifest.csv"}, "H9: the manifest lists every shipped file")
    with zipfile.ZipFile(os.path.join(target, "census2026_data_dictionary.xlsx")) as z:
        dtext = " ".join(re.findall(r"<t[^>]*>([^<]*)</t>", z.read("xl/sharedStrings.xml").decode("utf-8")))
    scope = [f for f in files if f.endswith((".csv", ".parquet")) and f not in meta["distractor_files"]
             and f != "export_manifest.csv"]
    ok(all(f in dtext for f in scope), "H9: the dictionary names every extract and reference file literally")
    # ---------------------------------------------------------------- distractors
    ok(not any(d in open(E.__file__).read() for d in meta["distractor_files"]), "distractors: the golden route never reads them")
    # ---------------------------------------------------------------- realism sweep
    for f in files:
        p_ = os.path.join(target, f)
        if f.endswith(".csv"):
            txt = open(p_, encoding="utf-8").read()
            ok("—" not in txt and "–" not in txt, "realism: no em or en dash (%s)" % f)
    for f in ("OQ-4_occupation_output_quality_standard.docx",):
        t_ = docx_text(os.path.join(target, f))
        ok("—" not in t_ and "–" not in t_, "realism: no dash in %s" % f)
    names = re.findall(r"[A-Z][a-z]+ [A-Z][a-z]+", oq + plan_txt)
    ok(all(any(p in oq + plan_txt for p in PEOPLE) for _ in [0]), "realism: personas drawn by the guard")
    ok(len(set(D["reg"].ed_code)) > 1000, "realism: over a thousand enumeration districts")
    tot = [sum(v[0] for v in teams.values()), sum(v[0] for v in regions.values())]
    ok(all(x % 100 != 0 for x in tot), "realism: no round totals")
    ok(D["vis"].visit_time.str[11:16].nunique() > 600, "realism: call times spread through the day")
    return n[0]


def docx_text(path):
    with zipfile.ZipFile(path) as z:
        x = z.read("word/document.xml").decode("utf-8")
    return " ".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", x))


def open_xlsx_text(path):
    with zipfile.ZipFile(path) as z:
        s = z.read("xl/sharedStrings.xml").decode("utf-8") if "xl/sharedStrings.xml" in z.namelist() else ""
    return " ".join(re.findall(r"<t[^>]*>([^<]*)</t>", s))
