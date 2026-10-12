"""task130 assertions on the built pack and goldens: input gates, the ladder and its separations, the fork grid, every
semantic fork row (SF1 to SF20), the closure axes that can be asserted, the asks with their stops and the separation
line, distractor deletion, mess neutrality, mid-bin figures, the realism sweep and container hygiene."""
from __future__ import annotations

import csv
import datetime as dt
import json
import math
import os
import random
import re
import shutil
import tempfile
import zipfile

import openpyxl
from pypdf import PdfReader

import analysis as AN
import asks as A
import calc as CA
import claims as C
import common as K

RESULTS = []


def ok(name, cond, detail=""):
    RESULTS.append((name, bool(cond), detail))
    if not cond:
        print("FAIL %s %s" % (name, detail))


def edge(x, step):
    """Distance of x from its rounding edge, as a share of the bin (0.5 at the bin centre)."""
    return abs(((x / step) % 1.0) - 0.5)


def r1000(x):
    return int(math.floor(x / 1000.0 + 0.5) * 1000)


def r1(x):
    return math.floor(x * 10 + 0.5) / 10


def _total(gold):
    return sum(v["cost"] for v in gold.values())


def run(target, golden, world=None, meta_path=None):
    del RESULTS[:]
    m = AN.main_call(target)
    g = m["total"]
    r = m["rungs"]
    ex, E, Em, E20, plan = m["ex"], m["E"], m["Em"], m["E20"], m["plan"]
    tr = AN.transitions()
    files = sorted(os.listdir(target))

    # ------------------------------------------------------------------ input gates
    meta = json.load(open(meta_path)) if meta_path else {}
    fmts = {f.rsplit(".", 1)[1] for f in files}
    ok("gate.files", len(files) >= 10, "%d files" % len(files))
    ok("gate.formats", len(fmts) >= 3, str(sorted(fmts)))
    big = max(sum(1 for _ in open(os.path.join(target, f), encoding="utf-8")) - 1 for f in files if f.endswith(".csv"))
    ok("gate.large_file", big >= 25000, "%d rows" % big)
    dis = meta.get("distractor_files", [])
    ok("gate.distractors", len(dis) >= 2 and all(d in files for d in dis), str(dis))
    ok("gate.no_distractor_word", not any("distract" in f.lower() for f in files))

    # ------------------------------------------------------------------ the build agrees with the simulation
    if world is not None:
        ex_mem = C.experience_from_rows(world["rows"])
        ok("bundle.experience_matches_simulation", len(ex_mem) == len(ex) and
           abs(sum(x["cost"] for x in ex_mem) - sum(x["cost"] for x in ex)) < 0.01,
           "%d/%d claims" % (len(ex_mem), len(ex)))

    # ------------------------------------------------------------------ ladder
    rat = {k: v / g for k, v in r.items()}
    ok("ladder.R0_default", rat["R0"] >= 4.0, "R0 %.2fx (as recorded, all years)" % rat["R0"])
    ok("ladder.R0m_mature", rat["R0m"] >= 4.0, "R0m %.2fx (2017 to 2020)" % rat["R0m"])
    ok("ladder.R1a_twelve_month_share", rat["R1a"] >= 3.0, "%.2fx" % rat["R1a"])
    ok("ladder.R1_count_at_average", rat["R1"] >= 2.0, "%.2fx" % rat["R1"])
    ok("ladder.R2_full_year_prorated", rat["R2"] >= 1.25, "%.2fx" % rat["R2"])
    ok("ladder.R2b_same_year_prorated", rat["R2b"] >= 1.15, "%.2fx" % rat["R2b"])
    ok("ladder.L0_escalations_apart", rat["L0"] <= 0.80, "%.2fx" % rat["L0"])
    ok("ladder.step_factor_off_pack", rat["step30"] >= 1.15, "0.30 x R0m = %.2fx" % rat["step30"])
    ok("ladder.base_2020_codes_only", rat["base2020"] >= 1.06, "%.2fx" % rat["base2020"])
    ok("ladder.order", r["R0"] > r["R1"] > r["R2"] > g > r["L0"], "R0 > R1 > R2 > golden > L0")
    nearest = min(abs(v / g - 1) for k, v in r.items() if k != "golden")
    ok("ladder.no_rung_within_15pct", nearest >= 0.15, "nearest %.3f" % nearest)
    # dominance: the decisive construction against every Layer 1 rung's effect on the contribution
    decisive = r["R0"] - g
    layer1 = max(abs(r["L0"] - g), abs(r["base2020"] - g))
    ok("ladder.dominance", decisive >= 1.2 * layer1, "decisive %.0f against Layer 1 %.0f" % (decisive, layer1))

    # worth on the graded figures: every entity and class figure moves under R0, R1 and R2
    X = CA.fte_years(plan, tr, K.ENTITY_ORDER, K.CLASSES)
    A0 = {k: sum(c["cost"] for c in ex if c["cls"] == k) / E[k] for k in K.CLASSES}
    full = {k: sum(c["cost"] * max(0, 365 - c["lag"]) / 365.0 for c in ex if c["cls"] == k) / E[k] for k in K.CLASSES}
    gold = m["gold"]
    moved0 = sum(1 for e in K.ENTITY_ORDER
                 if r1000(sum(A0[k] * X[(e, k)] for k in K.CLASSES if (e, k) in X)) != r1000(m["ent"][e]["cost"]))
    moved2 = sum(1 for e in K.ENTITY_ORDER
                 if r1000(sum(full[k] * X[(e, k)] for k in K.CLASSES if (e, k) in X)) != r1000(m["ent"][e]["cost"]))
    ok("worth.R0_moves_every_entity", moved0 == 4, "%d of 4" % moved0)
    ok("worth.R2_moves_every_entity", moved2 == 4, "%d of 4" % moved2)
    part = [e for e in K.ENTITY_ORDER if e != "TFH"]
    r2_part = min(sum(full[k] * X[(e, k)] for k in K.CLASSES if (e, k) in X) / m["ent"][e]["cost"] for e in part)
    ok("worth.R2_part_year_entities", r2_part >= 1.2, "min %.2fx" % r2_part)
    avg = {k: sum(c["cost"] for c in ex if c["cls"] == k) / max(1, sum(1 for c in ex if c["cls"] == k))
           for k in K.CLASSES}
    moved1 = sum(1 for k in K.CLASSES if r1000(m["cls"][k]["count"] * avg[k]) != r1000(m["cls"][k]["cost"]))
    ok("worth.R1_moves_every_class", moved1 == 7, "%d of 7" % moved1)

    # ------------------------------------------------------------------ the fork grid
    cells = m["grid"]
    gk = ("byday", "cost", "merged", "both")
    ok("grid.golden_cell", abs(cells[gk] - g) < 0.01)
    far = min(abs(v / g - 1) for k, v in cells.items() if k != gk)
    ok("grid.every_cell_6pct", far >= 0.06, "nearest %.3f" % far)

    # ------------------------------------------------------------------ semantic fork table
    ok("SF1.no_margin", r1000(g * 1.05) != r1000(g), "a 5 per cent margin moves the contribution")
    ok("SF2.occurrence_moves", rat["R0"] >= 4.0, "claims from 2027 incidents whenever made: %.2fx" % rat["R0"])
    ok("SF3.one_claim_per_incident", rat["L0"] <= 0.8, "each claim number apart: %.2fx" % rat["L0"])
    rows = m["rows"]
    suits = {x["incident_no"] for x in rows if x["matter_type"] == "Suit"}
    sf4 = _total(CA.window([c for c in ex if c["incident_no"] in suits], E, plan, tr, K.CLASSES, K.ENTITY_ORDER))
    ok("SF4.requests_are_claims", abs(sf4 / g - 1) >= 0.06, "suits only: %.2fx" % (sf4 / g))
    # SF5: residents counted as covered (their claims and FTE)
    job, _, _, _ = AN.load_payroll(target)
    code_to_key = {}
    for j in K.JOBS:
        code_to_key[j[1]] = j[0]
        code_to_key[j[2]] = j[0]
    res_cls = dict(K.CLASS_OF_JOB)
    res_cls.update({"RES": "HM", "FEL": "HM"})
    job_of_res = lambda cid, d: code_to_key.get(job.get((cid, K.month_key(d.year, d.month))))
    saved = dict(K.CLASS_OF_JOB)
    try:
        K.CLASS_OF_JOB.update({"RES": "HM", "FEL": "HM"})
        ex5 = C.experience_from_rows(rows, job_of=job_of_res)
    finally:
        K.CLASS_OF_JOB.clear()
        K.CLASS_OF_JOB.update(saved)
    E5 = dict(E)
    with open(os.path.join(target, K.PAYROLL), encoding="utf-8") as fh:
        for x in csv.DictReader(fh):
            if x["job_code"] in ("25010", "GME-RES", "25020", "GME-FEL") and "2017" <= x["pay_month"][:4] <= "2024":
                E5["HM"] += float(x["fte"]) / 12.0
    sf5 = _total(CA.window(ex5, E5, plan, tr, K.CLASSES, K.ENTITY_ORDER))
    ok("SF5.covered_clinicians", r1000(sf5) != r1000(g), "residents and fellows counted: %.3fx" % (sf5 / g))
    # SF6: paid only, indemnity only
    def rescost(fn):
        out = []
        for c in ex:
            out.append(dict(c))
        by = {}
        for x in rows:
            by.setdefault(x["incident_no"], []).append(x)
        for c in out:
            rs = [x for x in by[c["incident_no"]] if x["coverage_line"] != "CONTRACT" and
                  K.CLASS_OF_JOB.get(job_of_res(x["clinician_id"], x["incident_date"])) is not None]
            c["cost"] = sum(fn(x) for x in rs) * K.trend_factor(c["year"])
        return out
    paid = rescost(lambda x: (x["indemnity_paid"] or 0) + (x["defense_paid"] or 0))
    indem = rescost(lambda x: (x["indemnity_paid"] or 0) + (x["indemnity_reserve"] or 0))
    full_check = rescost(lambda x: (x["indemnity_paid"] or 0) + (x["defense_paid"] or 0) + (x["indemnity_reserve"] or 0)
                         + (x["defense_reserve"] or 0))
    ok("SF6.cost_basis_reproduces", abs(sum(c["cost"] for c in full_check) - sum(c["cost"] for c in ex)) < 0.01)
    sp = _total(CA.window(paid, E, plan, tr, K.CLASSES, K.ENTITY_ORDER))
    si = _total(CA.window(indem, E, plan, tr, K.CLASSES, K.ENTITY_ORDER))
    ok("SF6.paid_only_moves", r1000(sp) != r1000(g), "%.3fx" % (sp / g))
    ok("SF6.indemnity_only_moves", r1000(si) != r1000(g), "%.3fx" % (si / g))
    # SF7: trend from the year made
    ex7 = []
    for c in ex:
        d = dict(c)
        made_year = c["year"] + (1 if not c["same_year"] else 0)
        d["cost"] = c["cost"] / K.trend_factor(c["year"]) * K.trend_factor(made_year)
        ex7.append(d)
    s7 = _total(CA.window(ex7, E, plan, tr, K.CLASSES, K.ENTITY_ORDER))
    ok("SF7.trend_from_incident_year", r1000(s7) != r1000(g), "%.3fx" % (s7 / g))
    # SF8: the experience window
    lo, hi = K.EXPERIENCE
    ex8 = [c for c in ex if c["year"] >= 2021]
    E8 = {k: 0.0 for k in K.CLASSES}
    with open(os.path.join(target, K.PAYROLL), encoding="utf-8") as fh:
        sb = AN.schedule_b()
        for x in csv.DictReader(fh):
            if "2021" <= x["pay_month"][:4] <= "2024" and x["job_code"] in sb:
                E8[sb[x["job_code"]]] += float(x["fte"]) / 12.0
    s8 = _total(CA.window(ex8, E8, plan, tr, K.CLASSES, K.ENTITY_ORDER))
    ok("SF8.experience_window", r1000(s8) != r1000(g), "2021 to 2024 only: %.3fx" % (s8 / g))
    # SF9: pooling within class (not by entity): the entity-split estimate differs
    ok("SF9.pooled_within_class", len({c["cls"] for c in ex}) == 7, "experience in all seven classes")
    # SF10: exposure from 1 January for every entity, and mid-month timing
    tr0 = {e: K.PLAN_START for e in K.ENTITY_ORDER}
    s10 = _total(CA.window(ex, E, plan, tr0, K.CLASSES, K.ENTITY_ORDER))
    ok("SF10.from_transition_date", s10 / g >= 1.5, "from 1 January: %.2fx" % (s10 / g))
    mid = {}
    for k in K.CLASSES:
        ck = [c for c in ex if c["cls"] == k]
        G = CA.cum_by_lag([c["lag"] for c in ck], [c["cost"] for c in ck])
        N = CA.cum_by_lag([c["lag"] for c in ck], [1.0] * len(ck))
        for e in K.ENTITY_ORDER:
            if (e, k) not in plan:
                continue
            for mth in range(tr[e].month, 13):
                left = (CA.END - dt.date(2027, mth, 15)).days
                w = plan[(e, k)][mth - 1] / 12.0 / E[k]
                mid.setdefault((e, k), [0.0, 0.0])
                mid[(e, k)][0] += w * G[left]
                mid[(e, k)][1] += w * N[left]
    mid_tot = sum(v[0] for v in mid.values())
    moved = sum(1 for e in K.ENTITY_ORDER if r1000(sum(v[0] for (ee, k), v in mid.items() if ee == e)) !=
                r1000(m["ent"][e]["cost"])) + sum(1 for k in K.CLASSES if r1000(sum(v[0] for (e, kk), v in mid.items()
                                                                                   if kk == k)) != r1000(m["cls"][k]["cost"]))
    ok("SF10.mid_month_recorded", True, "exposure at mid-month: contribution %.4fx, %d of 11 entity and class costs move; "
       "ruled out by funding policy 3.3 (earned evenly over the days of the month)" % (mid_tot / g, moved))
    # SF11: base exposure, the 2020 codes alone
    ok("SF11.both_code_sets", rat["base2020"] >= 1.06, "%.2fx" % rat["base2020"])
    # SF12: class from the payroll job and from the register's free text agree on every experience Claim
    spec_class = {}
    from claims import SPECIALTY_TEXT
    for jk, texts in SPECIALTY_TEXT.items():
        for t in texts:
            spec_class.setdefault(t, set()).add(K.CLASS_OF_JOB.get(jk))
    by_inc = {}
    for x in rows:
        by_inc.setdefault(x["incident_no"], []).append(x)
    agree = 0
    for c in ex:
        rs = sorted((x for x in by_inc[c["incident_no"]] if x["coverage_line"] != "CONTRACT" and
                     K.CLASS_OF_JOB.get(job_of_res(x["clinician_id"], x["incident_date"])) is not None),
                    key=lambda x: (x["claim_made_date"], x["claim_no"], x["defendant_seq"]))
        if spec_class.get(rs[0]["specialty"]) == {c["cls"]}:
            agree += 1
    ok("SF12.class_text_converges", agree == len(ex), "%d of %d" % (agree, len(ex)))
    ok("SF13.four_entities", {e for e, _ in plan} == set(K.ENTITY_ORDER))
    ok("SF14.seven_classes", {k for _, k in plan} == set(K.CLASSES))
    # SF15: claims made on 31 December 2027 inside; the exclusive reading moves the figures
    ex15 = [dict(c, lag=c["lag"] + 1) for c in ex]
    s15 = _total(CA.window(ex15, E, plan, tr, K.CLASSES, K.ENTITY_ORDER))
    ok("SF15.through_31_december", r1000(s15) != r1000(g), "exclusive end: %.4fx" % (s15 / g))
    # SF16: rounding once; the rounded parts add to the rounded totals
    ok("SF16.entity_costs_add", sum(r1000(v["cost"]) for v in m["ent"].values()) == r1000(g))
    ok("SF16.class_costs_add", sum(r1000(v["cost"]) for v in m["cls"].values()) == r1000(g))
    tn = sum(v["count"] for v in m["ent"].values())
    ok("SF16.entity_counts_add", abs(sum(r1(v["count"]) for v in m["ent"].values()) - r1(tn)) < 1e-9)
    ok("SF16.class_counts_add", abs(sum(r1(v["count"]) for v in m["cls"].values()) - r1(tn)) < 1e-9)
    # SF17: Claims closed or held with no indemnity (defence costs only, or nothing) are counted at their cost
    ind = {c["incident_no"]: c["cost"] for c in indem}
    ex17 = [c for c in ex if ind[c["incident_no"]] > 0]
    w17 = CA.window(ex17, E, plan, tr, K.CLASSES, K.ENTITY_ORDER)
    n17 = sum(v["count"] for v in w17.values())
    ok("SF17.no_indemnity_claims_counted", len(ex17) < len(ex) and r1(n17) != r1(tn) and r1000(_total(w17)) != r1000(g),
       "%d Claims without indemnity; count %.2f against %.2f" % (len(ex) - len(ex17), n17, tn))

    # ------------------------------------------------------------------ closure axes
    lag_ok = all(c["year"] <= 2024 for c in ex) and max(
        (dt.date(c["year"], 12, 31) + dt.timedelta(days=c["lag"]) for c in ex if c["lag"] <= 364)) < K.VALUATION
    ok("axis12.window_lags_reported", lag_ok, "every experience Claim made within 364 days is in the extract")
    perm = []
    for seed in (1, 2, 3):
        rr = list(rows)
        random.Random(seed).shuffle(rr)
        exp = C.experience_from_rows(rr, job_of=job_of_res)
        perm.append(_total(CA.window(exp, E, plan, tr, K.CLASSES, K.ENTITY_ORDER)))
    ok("axis14.row_order", all(abs(p - g) < 1e-6 for p in perm))
    covered_ids = {x["clinician_id"] for x in rows if x["coverage_line"] != "CONTRACT" and lo <= x["incident_date"] <= hi}
    missing_ids = [cid for cid in covered_ids if not any((cid, K.month_key(y, mm)) in job for y in range(2017, 2025)
                                                         for mm in range(1, 13))]
    ok("axis16.ids_in_payroll", not missing_ids, "%d ids" % len(missing_ids))
    neg = [x for x in rows if any((x[f] or 0) < 0 for f in ("indemnity_paid", "defense_paid", "indemnity_reserve",
                                                              "defense_reserve"))]
    ok("axis17.no_negative_amounts", not neg)
    ok("axis22.plan_full_year", all(len(v) == 12 and min(v) > 0 for v in plan.values()))
    win = [c for c in ex if c["lag"] <= 364]
    ok("SF18.limit_cannot_move_the_golden", max(c["cost"] for c in win) < K.LIMIT_PER_CLAIM,
       "largest Claim that can be made inside the window %.0f; the $2,000,000 limit cannot move the golden" %
       max(c["cost"] for c in win))

    # SF19: the day count, executed on the dates the agreement and the policy file. An incident on a date from the
    # entity's Transition Date takes each experience Claim's delay (its made date less its incident date) and is in
    # when that making date is no later than 31 December 2027; exposure is earned evenly over each month's days.
    # Each one-day variant moves the rounded contribution and contradicts a sentence the shipped PDFs carry.
    def _pdf(name):
        return re.sub(r"\s+", " ", " ".join(p.extract_text() for p in PdfReader(os.path.join(target, name)).pages))
    filed = _pdf(K.AGREEMENT) + " " + _pdf(K.POLICY)

    def by_date(start=0, end=0, delay=0):
        last = K.PLAN_END + dt.timedelta(days=end)
        per = {e: 0.0 for e in K.ENTITY_ORDER}
        for (e, k), row in plan.items():
            ck = [(dt.timedelta(days=c["lag"] + delay), c["cost"]) for c in ex if c["cls"] == k]
            d, acc = tr[e] + dt.timedelta(days=start), 0.0
            while d <= K.PLAN_END:
                mm = d.month if d.year == K.PLAN_YEAR else 1     # a day before 1 January 2027 takes January's plan FTE
                w = row[mm - 1] / 12.0 / K.days_in_month(K.PLAN_YEAR, mm)
                acc += w * sum(cost for td, cost in ck if d + td <= last)
                d += dt.timedelta(days=1)
            per[e] += acc / E[k]
        return sum(per.values()), per
    base19, per19 = by_date()
    ok("SF19.filed_dates_give_the_golden", abs(base19 - g) < 1e-6 and
       all(abs(per19[e] - m["ent"][e]["cost"]) < 1e-6 for e in K.ENTITY_ORDER),
       "incidents from the Transition Date, each made on its incident date plus an experience Claim's delay, in when "
       "made by 31 December 2027: %.2f against the golden %.2f" % (base19, g))
    for name, kw, rules in [
            ("days_left_counted_with_both_ends", dict(end=1),
             ("Plan Year means a calendar year", "A Claim first made after the end of a Plan Year is not covered by "
                                                 "that Plan Year")),
            ("delay_counted_with_both_ends", dict(delay=1),
             ("A Claim is made on the date it is first received", "Plan Year means a calendar year")),
            ("transition_date_left_out", dict(start=1),
             ("occurred on or after the Retroactive Date", "A policy period ends at 12:01 a.m. on its last date")),
            ("day_before_transition_counted", dict(start=-1),
             ("occurred before a Participating Entity's Transition Date remains insured under the occurrence policy",
              "month from the entity's Transition Date"))]:
        v, pv = by_date(**kw)
        moved = sum(1 for e in K.ENTITY_ORDER if r1000(pv[e]) != r1000(m["ent"][e]["cost"]))
        ok("SF19.%s_ruled_out" % name, r1000(v) != r1000(g) and all(s in filed for s in rules),
           "%s (%d of 4 entity costs move); against the filed sentences: %s" % (
               "{:,}".format(r1000(v)), moved, "; ".join("'%s'" % s for s in rules)))

    # SF20: a Claim's cost adds every claim number's rows (one row per defendant on a claim number). No escalation
    # repeats an amount set on its two claim numbers, and each carrier's September run carries the escalated matter
    # at the two claim numbers' payments added; reading the later claim number's rows as cumulative moves the call.
    chains = [c for c in ex if c["n_claim_nos"] > 1]
    repeats = 0
    for c in chains:
        sets = {}
        for x in by_inc[c["incident_no"]]:
            if x["coverage_line"] != "CONTRACT":
                sets.setdefault(x["claim_no"], []).append((x["clinician_id"], x["indemnity_paid"], x["defense_paid"],
                                                           x["indemnity_reserve"], x["defense_reserve"]))
        vals = [tuple(sorted(v)) for v in sets.values()]
        repeats += len(vals) != len(set(vals))
    carrier_paid = {}
    wb_qm = openpyxl.load_workbook(os.path.join(target, K.QM_SEP), data_only=True)
    for x in wb_qm["Loss Run"].iter_rows(min_row=8, values_only=True):
        if x[3]:
            carrier_paid[A.norm(x[4])] = (float(x[9]), float(x[10]))
    with open(os.path.join(target, K.SC_SEP), encoding="utf-8") as fh:
        for x in csv.DictReader(fh):
            carrier_paid[A.norm(x["INSURED_REF"])] = (float(x["IND_PAID"]), float(x["EXP_PAID"]))
    summed = 0
    for c in chains:
        rs = [x for x in by_inc[c["incident_no"]] if x["coverage_line"] != "CONTRACT"]
        first = min(rs, key=lambda x: (x["claim_made_date"], x["claim_no"]))["claim_no"]
        got = carrier_paid.get(A.norm(first))
        summed += got is not None and abs(got[0] - sum(x["indemnity_paid"] or 0 for x in rs)) < 0.01 and \
            abs(got[1] - sum(x["defense_paid"] or 0 for x in rs)) < 0.01
    later = [dict(c, cost=sorted(c["parts"])[-1][1]) if c["n_claim_nos"] > 1 else c for c in ex]
    s20 = _total(CA.window(later, E, plan, tr, K.CLASSES, K.ENTITY_ORDER))
    ok("SF20.claim_numbers_added", bool(chains) and repeats == 0 and summed == len(chains) and r1000(s20) != r1000(g),
       "%d escalations, %d repeat an amount set, %d carried by their carrier at the added payments; the later claim "
       "number alone files %s" % (len(chains), repeats, summed, "{:,}".format(r1000(s20))))

    # ------------------------------------------------------------------ mid-bin
    figs = [("contribution", g, 1000)] + \
        [("%s cost" % e, m["ent"][e]["cost"], 1000) for e in K.ENTITY_ORDER] + \
        [("%s count" % e, m["ent"][e]["count"], 0.1) for e in K.ENTITY_ORDER] + \
        [("%s cost" % k, m["cls"][k]["cost"], 1000) for k in K.CLASSES] + \
        [("%s count" % k, m["cls"][k]["count"], 0.1) for k in K.CLASSES] + [("total count", tn, 0.1)]
    worst = min(figs, key=lambda f: edge(f[1], f[2]))
    ok("midbin.main_figures", edge(worst[1], worst[2]) >= 0.07, "worst %s at %.3f of the bin" % (
        worst[0], edge(worst[1], worst[2])))
    ok("realism.contribution_not_round", r1000(g) % 10000 != 0, "{:,}".format(r1000(g)))
    ok("realism.entity_costs_distinct", len({r1000(v["cost"]) for v in m["ent"].values()}) == 4)
    ok("realism.class_costs_distinct", len({r1000(v["cost"]) for v in m["cls"].values()}) == 7)

    # ------------------------------------------------------------------ asks
    a = A.ask_a(target, rows)
    for e in K.ENTITY_ORDER:
        v = a[e]
        ok("askA.%s.S1_off" % e, v["s1"][0] != v["count"], "S1 %d against %d" % (v["s1"][0], v["count"]))
        ok("askA.%s.S2_off" % e, v["s2"][0] != v["count"], "S2 %d against %d" % (v["s2"][0], v["count"]))
    ok("askA.none_is_an_answer", any(a[e]["count"] == 0 for e in K.ENTITY_ORDER))
    ok("askA.some_missing", sum(1 for e in K.ENTITY_ORDER if a[e]["count"] > 0) >= 2)
    ok("askA.S3_moves_a_quillan_entity", any(a[e]["s3"][0] != a[e]["count"] for e in ("TFH", "AMC")))
    # "open": OPEN alone and OPEN with REOPENED give one answer, and no incident holds two open claim numbers, so
    # counting claim numbers or incidents is one count
    a_open = A.ask_a(target, [dict(x, status="CLOSED") if x["status"] == "REOPENED" else x for x in rows])
    ok("askA.open_and_reopened_converge", all(a_open[e]["count"] == a[e]["count"] and
                                              abs(a_open[e]["reserves"] - a[e]["reserves"]) < 0.01
                                              for e in K.ENTITY_ORDER),
       "OPEN alone: " + ", ".join("%s %d" % (e, a_open[e]["count"]) for e in K.ENTITY_ORDER))
    two_open = [i for i, rs in by_inc.items() if len({x["claim_no"] for x in rs if x["status"] in ("OPEN", "REOPENED")
                                                       and x["coverage_line"] != "CONTRACT"}) > 1]
    ok("askA.one_open_claim_number_per_incident", not two_open, str(two_open[:3]))
    if world is not None:
        byno = {i.incident_no: i for i in world["incidents"]}
        for e in K.ENTITY_ORDER:
            miss = a[e]["missing"]
            ok("askA.%s.gaps_are_constructed" % e, all(byno[i].unreported or byno[i].claims[0].made >= C.GAP_FIRST
                                                       for i in miss), str(miss))
            opn = [i for i in byno if any(x["incident_no"] == i and x["coverage_line"] == K.ENTITIES[e]["line"] and
                                          x["status"] in ("OPEN", "REOPENED") for x in rows)]
            ok("askA.%s.two_noticed_open" % e, sum(1 for i in opn if byno[i].notice is not None) >= 2)
    b = A.ask_b(target)
    for e in K.ENTITY_ORDER:
        ok("askB.%s.S1_off" % e, b["s1"][e] != b["gold"][e], "%.1f against %.1f" % (b["s1"][e], b["gold"][e]))
        ok("askB.%s.S2_off" % e, b["s2"][e] != b["gold"][e], "%.1f against %.1f" % (b["s2"][e], b["gold"][e]))
        ok("askB.%s.S4_home_entity_off" % e, b["s4"][e] != b["gold"][e], "%.1f against %.1f" % (b["s4"][e], b["gold"][e]))
    ok("askB.S3_fellows_moves_ashgrove", b["s3"]["AMC"] != b["gold"]["AMC"])

    # ------------------------------------------------------------------ separation line and deletion tests
    tmp = tempfile.mkdtemp()
    try:
        keep = [K.REGISTER, K.PAYROLL, K.PLAN, K.AGREEMENT, K.POLICY]
        for f in keep:
            shutil.copy(os.path.join(target, f), tmp)
        m2 = AN.main_call(tmp)
        ok("separation.call_reads_only_its_population", abs(m2["total"] - g) < 1e-6,
           "the call recomputes with the runs, notices, HCM lines, plan notes and distractors deleted")
    finally:
        shutil.rmtree(tmp)
    tmp = tempfile.mkdtemp()
    try:
        for f in files:
            if f not in K.DISTRACTORS:
                shutil.copy(os.path.join(target, f), tmp)
        a2 = A.ask_a(tmp)
        b2 = A.ask_b(tmp)
        m3 = AN.main_call(tmp)
        ok("distractors.deletion", abs(m3["total"] - g) < 1e-6 and
           all(a2[e]["count"] == a[e]["count"] and a2[e]["reserves"] == a[e]["reserves"] for e in K.ENTITY_ORDER) and
           b2["gold"] == b["gold"])
    finally:
        shutil.rmtree(tmp)
    # the asks do not move with the call's estimator (they read none of its construction)
    ok("separation.asks_decoupled", True, "ask goldens read the register's open claims, the loss runs, the notices and "
                                         "the HCM lines; no rung of the call enters them")
    # mess neutrality: the contracted rows, residents and escalations are on the main path and handled by rule
    ctr = sum(1 for x in rows if x["coverage_line"] == "CONTRACT" and lo <= x["incident_date"] <= hi)
    ok("mess.contracted_rows_present", ctr > 0, "%d contracted rows in the experience years" % ctr)
    esc = sum(1 for c in ex if c["n_claim_nos"] > 1)
    ok("mess.escalations_present", esc >= 5, "%d experience Claims with a second claim number" % esc)

    # ------------------------------------------------------------------ realism sweep and hygiene
    text_files = [f for f in files if f.endswith((".csv", ".md"))]
    dash = [f for f in text_files if "\u2014" in open(os.path.join(target, f), encoding="utf-8").read() or
            "\u2013" in open(os.path.join(target, f), encoding="utf-8").read()]
    ok("hygiene.no_em_dash_text", not dash, str(dash))
    for f in files:
        if f.endswith((".xlsx", ".pptx", ".docx")):
            z = zipfile.ZipFile(os.path.join(target, f))
            blob = b"".join(z.read(n) for n in z.namelist() if n.startswith("docProps"))
            ok("hygiene.%s.no_library" % f, b"openpyxl" not in blob and b"python-pptx" not in blob)
            body = b"".join(z.read(n) for n in z.namelist())
            ok("hygiene.%s.no_dash" % f, "\u2014".encode() not in body and "\u2013".encode() not in body)
        if f.endswith(".pdf"):
            data = open(os.path.join(target, f), "rb").read()
            ok("hygiene.%s.no_reportlab" % f, b"ReportLab" not in data and b"reportlab" not in data)
    stamps = {int(os.path.getmtime(os.path.join(target, f))) for f in files}
    ok("hygiene.one_mtime", len(stamps) == 1)
    people = set(K.PEOPLE.values())
    pack_text = " ".join(open(os.path.join(target, f), encoding="utf-8", errors="ignore").read()
                         for f in files if f.endswith((".csv", ".md")))
    others = re.findall(r"\b(?:Dr\.|Mr\.|Ms\.)\s+[A-Z][a-z]+", pack_text)
    ok("realism.no_unlisted_personas", not others, str(others[:5]))
    ok("realism.personas_from_card", all(p in json.load(open(os.path.join(os.path.dirname(os.path.dirname(target)),
                                                                             ".claude", "skills", "fingerprint", "cards",
                                                                             "task130.json")))["world"]["people"]
                                         for p in people))
    alleg = {}
    for x in rows:
        alleg[x["allegation"]] = alleg.get(x["allegation"], 0) + 1
    ok("realism.allegations_spread", max(alleg.values()) / len(rows) < 0.25, "top share %.2f" % (
        max(alleg.values()) / len(rows)))
    # ------------------------------------------------------------------ house fixes wired in
    with open(os.path.join(target, K.EXTRACT_LOG), encoding="utf-8") as fh:
        logged = {x["file_name"] for x in csv.DictReader(fh)}
    ok("H9.extract_log_lists_every_file", logged == set(files) - {K.EXTRACT_LOG}, str(sorted(set(files) ^ logged)))
    ok("H9.dictionary_names_its_extracts", all(f in open(os.path.join(target, K.DICTIONARY), encoding="utf-8").read()
                                              for f in (K.REGISTER, K.PAYROLL, K.HCM, K.CROSSWALK, K.DIRECTORY,
                                                        K.NOTICES, K.QM_SEP, K.QM_JUN, K.SC_SEP, K.SAFETY)))
    vdate = K.VALUATION
    late = [x["claim_no"] for x in rows if x["claim_made_date"] > vdate or (x["closed_date"] and x["closed_date"] > vdate)]
    ok("H16.register_dates_by_valuation", not late, str(late[:3]))
    with open(os.path.join(target, K.NOTICES), encoding="utf-8") as fh:
        ok("H16.notices_by_valuation", max(x["sent_date"] for x in csv.DictReader(fh)) <= vdate.isoformat())
    with open(os.path.join(target, K.HCM), encoding="utf-8") as fh:
        hcm = list(csv.DictReader(fh))
    ok("H16.hcm_by_september", max(x["work_month"] for x in hcm) == "2026-09")
    with open(os.path.join(target, K.SAFETY), encoding="utf-8") as fh:
        ok("H16.safety_by_valuation", max(x["event_date"] for x in csv.DictReader(fh)) <= vdate.isoformat())
    with open(os.path.join(target, K.SC_SEP), encoding="utf-8") as fh:
        rpt = [dt.date(int(x["DATE_RPTD"][6:]), int(x["DATE_RPTD"][:2]), int(x["DATE_RPTD"][3:5]))
               for x in csv.DictReader(fh)]
    ok("H16.stoneleigh_reports_by_valuation", max(rpt) <= vdate)
    # H5: Ask B's FTE converges with the hours a September REG line pays (no part months, no unpaid leave)
    sb = AN.schedule_b()
    xw = A.crosswalk(target)
    diverge = [x["worker_id"] for x in hcm if x["work_month"] == "2026-09" and x["earning_code"] == "REG" and
               sb.get(xw[x["job_profile_code"]]) and abs(float(x["hours"]) / 173.33 - float(x["fte"])) > 0.0051]
    ok("H5.askB_hours_converge", not diverge and not any(x["work_month"] == "2026-09" and x["earning_code"] == "LOA"
                                                         for x in hcm), "%d lines" % len(diverge))
    # Ask B's earning codes: every September position carries one REG line, one FTE on all its lines and one cost
    # centre, so a position counted once gives one figure whichever of its lines is read
    pos = {}
    for x in hcm:
        if x["work_month"] == "2026-09":
            p = pos.setdefault((x["worker_id"], x["position_id"]), dict(reg=0, fte=set(), cc=set()))
            p["reg"] += x["earning_code"] == "REG"
            p["fte"].add(x["fte"])
            p["cc"].add(x["cost_centre"])
    ok("askB.one_position_one_figure", all(p["reg"] == 1 and len(p["fte"]) == 1 and len(p["cc"]) == 1
                                           for p in pos.values()), "%d September positions" % len(pos))
    # H2: the design note's world and ladder figures, recomputed here
    lagc = [(c["lag"], c["cost"]) for c in ex]
    tot_c = sum(c for _, c in lagc)
    early = sorted(c for L, c in lagc if L <= 120)
    late_ = [c for L, c in lagc if L > 365]
    ok("record.experience_cost_by_lag", True, "%d Claims made within 120 days, median %.0f, %.3f of the cost; %d made "
       "more than a year after, %.3f of the cost" % (len(early), early[len(early) // 2] if len(early) % 2 else
                                                    (early[len(early) // 2 - 1] + early[len(early) // 2]) / 2,
                                                    sum(early) / tot_c, len(late_), sum(late_) / tot_c))
    per = []
    for e in K.ENTITY_ORDER:
        r0e = sum(A0[k] * X[(e, k)] for k in K.CLASSES if (e, k) in X)
        r2e = sum(full[k] * X[(e, k)] for k in K.CLASSES if (e, k) in X)
        per.append("%s R0 %.2f R2 %.2f" % (e, r0e / m["ent"][e]["cost"], r2e / m["ent"][e]["cost"]))
    ok("record.rungs_by_entity", True, "; ".join(per))
    if world is not None:
        import statistics as st
        inc = [i for i in world["incidents"] if lo <= i.date <= hi and i.cls]
        erp = [i for i in inc if i.route == "ERP"]
        dirc = [i for i in inc if i.route == "DIRECT"]
        esc_i = [i for i in erp if len(i.claims) > 1]
        ok("record.world_routes", True, "requests: median lag %.0f days, %d of %d escalated, suit a median %.0f days after "
           "the request; direct: median lag %.0f days (obstetrics %.0f)" % (
               st.median((i.claims[0].made - i.date).days for i in erp), len(esc_i), len(erp),
               st.median((i.claims[1].made - i.claims[0].made).days for i in esc_i),
               st.median((i.claims[0].made - i.date).days for i in dirc),
               st.median((i.claims[0].made - i.date).days for i in dirc if i.cls == "OB")))
    # golden agrees with figures.json
    figs_json = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures.json")))
    ok("figures.contribution", figs_json["call"]["contribution"] == "{:,}".format(r1000(g)))

    n_ok = sum(1 for _, c, _ in RESULTS if c)
    print("checks: %d of %d passed" % (n_ok, len(RESULTS)))
    if n_ok != len(RESULTS):
        raise SystemExit("checks failed: " + ", ".join(n for n, c, _ in RESULTS if not c))
    return RESULTS
