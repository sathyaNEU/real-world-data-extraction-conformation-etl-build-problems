"""task130 assertions on the built pack and goldens: input gates, the three rules executed (R1, R2, R3a to R3c), the
ladder with every rival route the audit and the design name, the fork grid on both bases, every semantic fork row
(SF1 to SF24), the closure axes that can be asserted, the asks with their stops, devices and the separation line,
distractor deletion, mid-bin figures, the realism sweep and container hygiene."""
from __future__ import annotations

import csv
import datetime as dt
import json
import math
import os
import random
import re
import shutil
import statistics as st
import tempfile
import zipfile

from pypdf import PdfReader

import analysis as AN
import asks as A
import calc as CA
import claims as C
import common as K
import world as WD

RESULTS = []
P = list(K.ERP_ENTITIES)
ENTS = K.ENTITY_ORDER
CLS = K.CLASSES


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


def money(x):
    return "{:,}".format(r1000(x))


def _pdf(target, name):
    return re.sub(r"\s+", " ", " ".join(p.extract_text() for p in PdfReader(os.path.join(target, name)).pages))


def golden_of(ex, Ee, plan, tr):
    """The golden construction on any experience and exposure: the Program hospitals' Claims and FTE-years."""
    exP = CA.program(ex)
    return CA.tot(CA.window(exP, CA.basis(Ee, P, CLS), plan, tr, CLS, ENTS))


def run(target, golden, world=None, meta_path=None):
    del RESULTS[:]
    m = AN.main_call(target)
    g = m["total"]
    rv = m["rivals"]
    rat = {k: v / g for k, v in rv.items()}
    ex, exP, Ee, plan = m["ex"], m["exP"], m["Ee"], m["plan"]
    EP, EA = m["EP"], m["EA"]
    tr = AN.transitions()
    rows = m["rows"]
    files = sorted(os.listdir(target))
    agreement, policy = _pdf(target, K.AGREEMENT), _pdf(target, K.POLICY)
    filed = agreement + " " + policy
    dictionary = open(os.path.join(target, K.DICTIONARY), encoding="utf-8").read()

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

    # ------------------------------------------------------------------ the three rules, executed
    hdr = []
    for f in files:
        if f.endswith(".csv"):
            with open(os.path.join(target, f), encoding="utf-8") as fh:
                hdr += next(csv.reader(fh))
    ok("R1.no_column_holds_the_decisive_quantity",
       not any(re.search(r"route|program|erp|lag|window|intake|channel|expected|forecast|regime|handled", c.lower())
               for c in hdr), "no shipped column carries a route, a lag, a window share, a regime or a 2027 cost")
    ok("R1.raw_material_ships", {"incident_date", "claim_made_date", "entity_at_incident", "indemnity_reserve"} <=
       set(hdr) and {"pay_month", "entity_code", "fte"} <= set(hdr),
       "the register carries each claim number's incident and made dates, entity and amounts; the payroll each "
       "employee-month's paid FTE by cost centre entity")
    ok("R1.golden_reads_the_rows", len(exP) >= 120 and len(ex) - len(exP) >= 40,
       "%d Program hospital Claims and %d others in the experience" % (len(exP), len(ex) - len(exP)))
    # R2: each Layer 1 item on the main path, mishandled the natural way, leaves the call where it was
    rows_blank0 = [dict(x, indemnity_paid=x["indemnity_paid"] or 0.0, defense_paid=x["defense_paid"] or 0.0,
                        indemnity_reserve=x["indemnity_reserve"] or 0.0, defense_reserve=x["defense_reserve"] or 0.0)
                   for x in rows]
    exb, _, _, _ = AN.experience(target, rows_blank0)
    ok("R2.contracted_blanks_read_as_zero_keep_the_call", abs(golden_of(exb, Ee, plan, tr) - g) < 1e-6)
    rows_re = [dict(x, status="CLOSED") if x["status"] == "REOPENED" else x for x in rows]
    exr, _, _, _ = AN.experience(target, rows_re)
    ok("R2.reopened_read_as_closed_keeps_the_call", abs(golden_of(exr, Ee, plan, tr) - g) < 1e-6)
    shuffled = list(rows)
    random.Random(7).shuffle(shuffled)
    exs, _, _, _ = AN.experience(target, shuffled)
    ok("R2.register_row_order_keeps_the_call", abs(golden_of(exs, Ee, plan, tr) - g) < 1e-6)
    job, _, _, _ = AN.load_payroll(target)
    sb = AN.schedule_b()
    new_codes = {j[2] for j in K.JOBS}
    Ee_new = {}
    with open(os.path.join(target, K.PAYROLL), encoding="utf-8") as fh:
        for x in csv.DictReader(fh):
            if x["job_code"] in new_codes and "2017" <= x["pay_month"][:4] <= "2024" and sb.get(x["job_code"]):
                key = (x["entity_code"], sb[x["job_code"]])
                Ee_new[key] = Ee_new.get(key, 0.0) + float(x["fte"]) / 12.0
    ok("R2.old_job_codes_ignored_keep_the_call", abs(golden_of(ex, Ee_new, plan, tr) - g) < 1e-6,
       "the July 2016 code set covers every experience month")
    ok("R2.gl_matters_off_the_register", not any(x["claim_no"].startswith("GL-") for x in rows))
    # R3a: the easy route on the clean truth (the simulation's own records), every filed rule applied
    if world is not None:
        W = world["W"]
        Ee_mem, Eem_mem = {}, {}
        for (p, y, mth, f) in WD.position_months(W, (2017, 1), (2024, 12)):
            k = K.CLASS_OF_JOB[p.job]
            if k is None:
                continue
            Ee_mem[(p.entity, k)] = Ee_mem.get((p.entity, k), 0.0) + f / 12.0
            if y <= 2020:
                Eem_mem[(p.entity, k)] = Eem_mem.get((p.entity, k), 0.0) + f / 12.0
        ex_mem = C.experience_from_rows(world["rows"])
        clean, _, _, _ = CA.rivals(ex_mem, Ee_mem, Eem_mem, world["plan"], tr, CLS, ENTS)
        ok("R3a.analyst_test_on_clean_truth", clean["pooled"] / clean["golden"] <= 0.70 and
           r1000(clean["pooled"]) != r1000(clean["golden"]),
           "the claim-by-claim window on the System's pooled experience, every filed rule applied, files %s against %s"
           % (money(clean["pooled"]), money(clean["golden"])))
        for k, lab in (("pooled_R0", "a mature year per FTE-year"), ("pooled_R1", "the window's count at the average cost"),
                       ("pooled_R2", "a full year's in-year share prorated")):
            ok("R3a.audit_route_%s_wrong_on_clean_truth" % k, abs(clean[k] / clean["golden"] - 1) >= 0.06,
               "%s files %s" % (lab, money(clean[k])))
        ok("R3b.decisive_step_alone_files_the_golden", abs(clean["golden"] - g) < 0.01,
           "the same route with only the experience moved to the Program hospitals files %s" % money(clean["golden"]))
        for k, lab in (("program_R0", "the basis right, a mature year"), ("program_R1", "the basis right, count at average"),
                       ("program_R2", "the basis right, a full year prorated"),
                       ("by_carrier", "each carrier's entities on their own experience"),
                       ("h1_own_program_hospitals", "each Program hospital on its own experience")):
            ok("R3b.%s_alone_leaves_it_off" % k, r1000(clean[k]) != r1000(clean["golden"]), "%s: %s" % (lab, money(clean[k])))
    ok("R3c.no_memo_draft_or_estimate", not any(re.search(r"memo|draft|briefing|estimate|forecast|actuar", f.lower())
                                                for f in files))
    ok("R3c.no_document_states_a_cost_or_factor",
       not re.search(r"step factor|lag table|report lag|per FTE-year of|2027 cost of|expected cost of \$", filed + dictionary),
       "no filed sentence states a 2027 cost, a claims-made factor or a lag table")
    reg_blocks = [(x["incident_date"], x["claim_made_date"], x["indemnity_paid"], x["defense_paid"]) for x in rows]
    ok("R3c.no_repeated_blocks", len(reg_blocks) - len(set(reg_blocks)) <= 0.12 * len(reg_blocks),
       "%d coincident register rows (codefendants on one claim number)" % (len(reg_blocks) - len(set(reg_blocks))))

    # ------------------------------------------------------------------ ladder and rivals
    ok("ladder.default_pooled_window", rat["pooled"] <= 0.70, "%.3fx, %s" % (rat["pooled"], money(rv["pooled"])))
    for k in ("pooled_R0", "pooled_R0m", "pooled_R1a", "pooled_R1", "program_R0", "program_R0m", "program_R1a",
              "program_R1", "program_R2", "pooled_step30", "program_step30"):
        ok("ladder.%s_above" % k, rat[k] >= 1.06, "%.3fx" % rat[k])
    for k in ("pooled_L0", "program_L0", "by_entity", "by_carrier", "h3_program_for_stoneleigh_only",
              "program_claims_over_all_fte", "stoneleigh_for_all", "pooled_R2", "pooled_R2b"):
        ok("ladder.%s_below" % k, rat[k] <= 0.94, "%.3fx" % rat[k])
    ok("ladder.program_R2b_off", abs(rat["program_R2b"] - 1) >= 0.06, "%.3fx" % rat["program_R2b"])
    ok("ladder.h1_own_hospitals_off", abs(rat["h1_own_program_hospitals"] - 1) >= 0.06,
       "%.3fx (funding policy 3.4)" % rat["h1_own_program_hospitals"])
    named = {k: v for k, v in rat.items() if k not in ("golden", "h4_quick_program_slow_pooled")}
    near = min(named, key=lambda k: abs(named[k] - 1))
    ok("ladder.every_named_rival_6pct", abs(named[near] - 1) >= 0.06, "nearest %s %.3f" % (near, named[near]))
    # the Program's reach: the Program hospitals' quicker Claims with the slower ones pooled converges when the split
    # sits at the window's own reach (364 days) and stays off the rounded golden below it
    quickP = [c for c in exP if c["lag"] <= 364]
    slowA = [c for c in ex if c["lag"] > 364]
    reach = CA.tot(CA.window(quickP, EP, plan, tr, CLS, ENTS)) + CA.tot(CA.window(slowA, EA, plan, tr, CLS, ENTS))
    ok("ladder.split_at_the_window_reach_converges", abs(reach - g) < 1e-6, "C1")
    splits = {}
    for cut in (90, 120, 180, 270, 330):
        q = [c for c in exP if c["lag"] <= cut]
        s_ = [c for c in ex if c["lag"] > cut]
        splits[cut] = CA.tot(CA.window(q, EP, plan, tr, CLS, ENTS)) + CA.tot(CA.window(s_, EA, plan, tr, CLS, ENTS))
    ok("ladder.splits_below_the_reach_off_the_bin", all(r1000(v) != r1000(g) for v in splits.values()),
       ", ".join("%d days %s" % (c_, money(v)) for c_, v in splits.items()))
    # dominance on a quantity call: the decisive correction, applied to the default path, is the one move that reaches
    # the golden and moves the contribution by more than a third of it; every Layer 1 item is neutral (R2), and the
    # filed-rule rungs the default path already executes (escalations merged, Claims from the Transition Date) are
    # recorded with their own size
    decisive = g - rv["pooled"]
    ok("ladder.dominance", decisive / g >= 0.30 and rv["pooled"] / g <= 0.70,
       "decisive %s (%.0f per cent of the golden); for the record, escalations apart on the right basis move it %s" % (
           money(decisive), 100.0 * decisive / g, money(abs(rv["program_L0"] - g))))
    pooled = m["pooled"]
    pooled_count = sum(v["count"] for v in pooled.values())
    ok("worth.default_moves_count", r1(pooled_count) != r1(m["count"]), "%.1f against %.1f" % (pooled_count, m["count"]))
    pay_def, _ = AN.payments(rv["pooled"], plan, tr)
    ok("worth.default_moves_every_payment", all(r1000(pay_def[e]) != r1000(m["pay"][e]) for e in ENTS))
    ok("worth.default_moves_every_entity_cost", all(r1000(CA.by_ent(pooled, e)) != r1000(m["ent"][e]["cost"])
                                                     for e in ENTS))

    # ------------------------------------------------------------------ the fork grid, both bases
    cells = m["grid"]
    gk = ("program", "byday", "cost", "merged")
    ok("grid.golden_cell", abs(cells[gk] - g) < 0.01)
    far_k = min((k for k in cells if k != gk), key=lambda k: abs(cells[k] / g - 1))
    ok("grid.every_cell_6pct", abs(cells[far_k] / g - 1) >= 0.06, "nearest %s %.3f" % ("/".join(far_k),
                                                                                       cells[far_k] / g))

    # ------------------------------------------------------------------ semantic fork table
    ok("SF1.no_margin", r1000(g * 1.05) != r1000(g) and "no provision for the Trust's administrative expenses" in policy)
    ok("SF2.occurrence_moves", rat["program_R0"] >= 4.0, "claims from 2027 incidents whenever made: %.2fx" %
       rat["program_R0"])
    ok("SF3.one_claim_per_incident", rat["program_L0"] <= 0.8, "each claim number apart: %.2fx" % rat["program_L0"])
    suits = {x["incident_no"] for x in rows if x["matter_type"] == "Suit"}
    sf4 = CA.tot(CA.window([c for c in exP if c["incident_no"] in suits], EP, plan, tr, CLS, ENTS))
    ok("SF4.requests_are_claims", abs(sf4 / g - 1) >= 0.06, "suits only: %.2fx" % (sf4 / g))
    code_to_key = {}
    for j in K.JOBS:
        code_to_key[j[1]] = j[0]
        code_to_key[j[2]] = j[0]
    job_of = lambda cid, d: code_to_key.get(job.get((cid, K.month_key(d.year, d.month))))
    saved = dict(K.CLASS_OF_JOB)
    try:
        K.CLASS_OF_JOB.update({"RES": "HM", "FEL": "HM"})
        ex5 = C.experience_from_rows(rows, job_of=job_of)
    finally:
        K.CLASS_OF_JOB.clear()
        K.CLASS_OF_JOB.update(saved)
    Ee5 = dict(Ee)
    with open(os.path.join(target, K.PAYROLL), encoding="utf-8") as fh:
        for x in csv.DictReader(fh):
            if x["job_code"] in ("25010", "GME-RES", "25020", "GME-FEL") and "2017" <= x["pay_month"][:4] <= "2024":
                Ee5[(x["entity_code"], "HM")] = Ee5.get((x["entity_code"], "HM"), 0.0) + float(x["fte"]) / 12.0
    sf5 = golden_of(ex5, Ee5, plan, tr)
    ok("SF5.covered_clinicians", r1000(sf5) != r1000(g), "residents and fellows counted: %.3fx" % (sf5 / g))
    by_inc = {}
    for x in rows:
        by_inc.setdefault(x["incident_no"], []).append(x)

    def rescost(fn):
        out = []
        for c in ex:
            d = dict(c)
            rs = [x for x in by_inc[c["incident_no"]] if x["coverage_line"] != "CONTRACT" and
                  K.CLASS_OF_JOB.get(job_of(x["clinician_id"], x["incident_date"])) is not None]
            d["cost"] = sum(fn(x) for x in rs) * K.trend_factor(c["year"])
            out.append(d)
        return out
    paid = rescost(lambda x: (x["indemnity_paid"] or 0) + (x["defense_paid"] or 0))
    indem = rescost(lambda x: (x["indemnity_paid"] or 0) + (x["indemnity_reserve"] or 0))
    full_check = rescost(lambda x: (x["indemnity_paid"] or 0) + (x["defense_paid"] or 0) + (x["indemnity_reserve"] or 0)
                         + (x["defense_reserve"] or 0))
    ok("SF6.cost_basis_reproduces", abs(sum(c["cost"] for c in full_check) - sum(c["cost"] for c in ex)) < 0.01)
    ok("SF6.paid_only_moves", r1000(golden_of(paid, Ee, plan, tr)) != r1000(g))
    ok("SF6.indemnity_only_moves", r1000(golden_of(indem, Ee, plan, tr)) != r1000(g))
    ex7 = []
    for c in ex:
        d = dict(c)
        made_year = c["year"] + (1 if not c["same_year"] else 0)
        d["cost"] = c["cost"] / K.trend_factor(c["year"]) * K.trend_factor(made_year)
        ex7.append(d)
    ok("SF7.trend_from_incident_year", r1000(golden_of(ex7, Ee, plan, tr)) != r1000(g))
    ex8 = [c for c in ex if c["year"] >= 2021]
    Ee8 = {}
    with open(os.path.join(target, K.PAYROLL), encoding="utf-8") as fh:
        for x in csv.DictReader(fh):
            if "2021" <= x["pay_month"][:4] <= "2024" and sb.get(x["job_code"]):
                key = (x["entity_code"], sb[x["job_code"]])
                Ee8[key] = Ee8.get(key, 0.0) + float(x["fte"]) / 12.0
    s8 = golden_of(ex8, Ee8, plan, tr)
    ok("SF8.experience_window", r1000(s8) != r1000(g), "2021 to 2024 only: %.3fx" % (s8 / g))
    ok("SF9.rated_alike", "carries the same expected cost whichever Participating Entity employs the clinician" in policy
       and abs(rat["by_entity"] - 1) >= 0.06 and abs(rat["h1_own_program_hospitals"] - 1) >= 0.06,
       "each entity on its own experience %.3fx; each Program hospital on its own %.3fx (funding policy 3.4)" %
       (rat["by_entity"], rat["h1_own_program_hospitals"]))
    tr0 = {e: K.PLAN_START for e in ENTS}
    s10 = CA.tot(CA.window(exP, EP, plan, tr0, CLS, ENTS))
    ok("SF10.from_transition_date", s10 / g >= 1.5, "from 1 January: %.2fx" % (s10 / g))
    ok("SF11.code_sets_converge", all(abs(Ee_new.get(k_, 0.0) - v) < 1e-9 for k_, v in Ee.items()),
       "C1: every experience month carries the July 2016 code set")
    spec_class = {}
    for jk, texts in C.SPECIALTY_TEXT.items():
        for t in texts:
            spec_class.setdefault(t, set()).add(K.CLASS_OF_JOB.get(jk))
    agree = 0
    for c in ex:
        rs = sorted((x for x in by_inc[c["incident_no"]] if x["coverage_line"] != "CONTRACT" and
                     K.CLASS_OF_JOB.get(job_of(x["clinician_id"], x["incident_date"])) is not None),
                    key=lambda x: (x["claim_made_date"], x["claim_no"], x["defendant_seq"]))
        agree += spec_class.get(rs[0]["specialty"]) == {c["cls"]}
    ok("SF12.class_text_converges", agree == len(ex), "%d of %d" % (agree, len(ex)))
    ok("SF13.four_entities", {e for e, _ in plan} == set(ENTS))
    ok("SF14.seven_classes", {k for _, k in plan} == set(CLS))
    ex15 = [dict(c, lag=c["lag"] + 1) for c in ex]
    ok("SF15.through_31_december", r1000(golden_of(ex15, Ee, plan, tr)) != r1000(g))
    ok("SF16.payments_add_to_the_contribution", sum(r1000(v) for v in m["pay"].values()) == r1000(g),
       "rounded payments %s" % [r1000(v) for v in m["pay"].values()])
    ok("SF16.payments_same_from_rounded_contribution",
       all(r1000(r1000(g) * m["expo"][e] / sum(m["expo"].values())) == r1000(m["pay"][e]) for e in ENTS))
    ind = {c["incident_no"]: c["cost"] for c in indem}
    ex17 = [c for c in ex if ind[c["incident_no"]] > 0]
    w17 = CA.window(CA.program(ex17), EP, plan, tr, CLS, ENTS)
    n17 = sum(v["count"] for v in w17.values())
    ok("SF17.no_indemnity_claims_counted", len(ex17) < len(ex) and r1(n17) != r1(m["count"]),
       "%d Claims without indemnity; count %.2f against %.2f" % (len(ex) - len(ex17), n17, m["count"]))
    win = [c for c in exP if c["lag"] <= 364]
    ok("SF18.limit_cannot_move_the_golden", max(c["cost"] for c in win) < K.LIMIT_PER_CLAIM,
       "largest Program Claim that can be made inside the window %s" % money(max(c["cost"] for c in win)))

    # SF19: the day count, executed on the filed dates (Program basis)
    def by_date(start=0, end=0, delay=0):
        last = K.PLAN_END + dt.timedelta(days=end)
        per = {e: 0.0 for e in ENTS}
        for (e, k), row in plan.items():
            ck = [(dt.timedelta(days=c["lag"] + delay), c["cost"]) for c in exP if c["cls"] == k]
            d, acc = tr[e] + dt.timedelta(days=start), 0.0
            while d <= K.PLAN_END:
                mm = d.month if d.year == K.PLAN_YEAR else 1
                w = row[mm - 1] / 12.0 / K.days_in_month(K.PLAN_YEAR, mm)
                acc += w * sum(cost for td, cost in ck if d + td <= last)
                d += dt.timedelta(days=1)
            per[e] += acc / EP[k]
        return sum(per.values()), per
    base19, per19 = by_date()
    ok("SF19.filed_dates_give_the_golden", abs(base19 - g) < 1e-6 and
       all(abs(per19[e] - m["ent"][e]["cost"]) < 1e-6 for e in ENTS))
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
        v, _ = by_date(**kw)
        ok("SF19.%s_ruled_out" % name, r1000(v) != r1000(g) and all(s in filed for s in rules),
           "%s against the filed sentences" % money(v))
    chains = [c for c in ex if c["n_claim_nos"] > 1]
    later = [dict(c, cost=sorted(c["parts"])[-1][1]) if c["n_claim_nos"] > 1 else c for c in ex]
    ok("SF20.claim_numbers_added", bool(chains) and r1000(golden_of(later, Ee, plan, tr)) != r1000(g),
       "%d escalations; the later claim number alone files %s" % (len(chains), money(golden_of(later, Ee, plan, tr))))
    by_cost = {e: m["ent"][e]["cost"] for e in ENTS}
    ok("SF21.payments_by_exposure_share", all(r1000(by_cost[e]) != r1000(m["pay"][e]) for e in ENTS) and
       all(r1000(m["pay"][e] / 4.0) != r1000(m["pay"][e]) for e in ENTS) and
       "in proportion to its share of the Plan Year's exposure under 3.3" in policy,
       "by expected cost %s; a quarterly instalment %s" % ([money(v) for v in by_cost.values()],
                                                         [money(v / 4) for v in m["pay"].values()]))
    parts = [dict(cls=c["cls"], lag=L, cost=cost) for c in exP for (L, cost) in c["parts"]]
    nparts = sum(v["count"] for v in CA.window(parts, EP, plan, tr, CLS, ENTS).values())
    ok("SF22.count_one_per_incident", nparts >= m["count"] and rat["program_L0"] <= 0.8,
       "claim numbers apart: %.2f Claims against %.2f (the escalated suits fall outside the window) and the cost "
       "%.2fx" % (nparts, m["count"], rat["program_L0"]))
    pay_ent = {}
    with open(os.path.join(target, K.PAYROLL), encoding="utf-8") as fh:
        for x in csv.DictReader(fh):
            pay_ent.setdefault((x["employee_id"], x["pay_month"]), set()).add(x["entity_code"])
    diff = []
    for c in ex:
        rs = sorted((x for x in by_inc[c["incident_no"]] if x["coverage_line"] != "CONTRACT" and
                     K.CLASS_OF_JOB.get(job_of(x["clinician_id"], x["incident_date"])) is not None),
                    key=lambda x: (x["claim_made_date"], x["claim_no"], x["defendant_seq"]))
        es = pay_ent.get((rs[0]["clinician_id"], K.month_key(rs[0]["incident_date"].year, rs[0]["incident_date"].month)),
                         set())
        if c["ent"] not in es:
            diff.append(c["incident_no"])
    ok("SF23.claim_entity_is_where_care_was_given", not diff,
       "every experience Claim's entity is an entity its first clinician was paid by that month (%d not)" % len(diff))
    ok("SF24.program_open_to_every_entity", "Early Resolution Program is open to the patients of every Participating "
       "Entity from its Transition Date" in agreement)
    ok("SF24.program_history_filed", "for the patients of Tolliver Falls Hospital and Alderwick Medical Center since "
       "September 2015" in dictionary)
    stone_quick = sum(1 for c in ex if c["ent"] not in P and c["lag"] <= 120)
    prog_quick = sum(1 for c in exP if c["lag"] <= 120)
    ok("SF24.records_agree_with_the_history", stone_quick <= 1 and prog_quick >= 40,
       "Claims made within 120 days of the incident: %d at the Program hospitals, %d at the medical group and "
       "Brennick" % (prog_quick, stone_quick))

    # ------------------------------------------------------------------ closure axes
    lag_ok = max((dt.date(c["year"], 12, 31) + dt.timedelta(days=c["lag"]) for c in ex if c["lag"] <= 364)) < K.VALUATION
    ok("axis12.window_lags_reported", lag_ok)
    covered_ids = {x["clinician_id"] for x in rows if x["coverage_line"] != "CONTRACT" and
                   K.EXPERIENCE[0] <= x["incident_date"] <= K.EXPERIENCE[1]}
    missing_ids = [cid for cid in covered_ids if not any((cid, K.month_key(y, mm)) in job for y in range(2017, 2025)
                                                         for mm in range(1, 13))]
    ok("axis16.ids_in_payroll", not missing_ids, "%d ids" % len(missing_ids))
    neg = [x for x in rows if any((x[f] or 0) < 0 for f in ("indemnity_paid", "defense_paid", "indemnity_reserve",
                                                              "defense_reserve"))]
    ok("axis17.no_negative_amounts", not neg)
    ok("axis22.plan_full_year", all(len(v) == 12 and min(v) > 0 for v in plan.values()))

    # ------------------------------------------------------------------ mid-bin
    figs = [("contribution", g, 1000), ("count", m["count"], 0.1)] + \
        [("%s pays" % e, m["pay"][e], 1000) for e in ENTS] + \
        [("%s pays (rounded contribution)" % e, r1000(g) * m["expo"][e] / sum(m["expo"].values()), 1000) for e in ENTS]
    worst = min(figs, key=lambda f: edge(f[1], f[2]))
    ok("midbin.main_figures", edge(worst[1], worst[2]) >= 0.15, "worst %s at %.3f of the bin" % (
        worst[0], edge(worst[1], worst[2])))
    ok("realism.contribution_not_round", r1000(g) % 10000 != 0, money(g))
    ok("realism.payments_distinct", len({r1000(v) for v in m["pay"].values()}) == 4)

    # ------------------------------------------------------------------ asks
    a = A.ask_a(target, rows)
    for e in ENTS:
        v = a[e]
        ok("askA.%s.S1_off" % e, (v["s1"][0], r1000(v["s1"][1])) != (v["count"], r1000(v["reserves"])),
           "S1 %s against %s" % (v["s1"], (v["count"], v["reserves"])))
        ok("askA.%s.S1b_off" % e, (v["s1b"][0], r1000(v["s1b"][1])) != (v["count"], r1000(v["reserves"])))
        ok("askA.%s.S2_careful_off_count_and_reserves" % e,
           v["s2"][0] != v["count"] and r1000(v["s2"][1]) != r1000(v["reserves"]),
           "careful path %s against %s" % (v["s2"], (v["count"], v["reserves"])))
        ok("askA.%s.dup_device_present" % e, len(v["dup"]) >= 1, str(v["dup"]))
    ok("askA.S3_moves_a_quillan_entity", any((a[e]["s3"][0], r1000(a[e]["s3"][1])) != (a[e]["count"],
                                                                                      r1000(a[e]["reserves"]))
                                             for e in ("TFH", "AMC")))
    ok("askA.some_missing", sum(1 for e in ENTS if a[e]["count"] > 0) >= 2)
    a_open = A.ask_a(target, [dict(x, status="CLOSED") if x["status"] == "REOPENED" else x for x in rows])
    ok("askA.open_and_reopened_converge", all(a_open[e]["count"] == a[e]["count"] and
                                              abs(a_open[e]["reserves"] - a[e]["reserves"]) < 0.01 for e in ENTS))
    ok("SF25.open_claims_converge", all(a_open[e]["count"] == a[e]["count"] for e in ENTS),
       "OPEN alone and OPEN with REOPENED give one Ask A answer")
    ok("SF26.occurrence_policies_are_the_coverage_line", all(
        all(x["coverage_line"] in (K.ENTITIES[e]["line"], "CONTRACT") or x["entity_at_incident"] != e
            for x in rows if x["incident_no"] in a[e]["missing"]) for e in ENTS),
       "each missing claim sits on its entity's own coverage line")
    _, qmj_rows = A.load_qm(target, K.QM_JUN)
    jun_header = A.load_qm(target, K.QM_JUN)[0]
    ok("SF27.latest_run_is_the_latest_valuation", jun_header == dt.date(2026, 6, 30) and
       any((a[e]["s3"][0], r1000(a[e]["s3"][1])) != (a[e]["count"], r1000(a[e]["reserves"])) for e in ("TFH", "AMC")),
       "the re-issued June run is an earlier valuation; read as the latest it moves Alderwick")
    ok("SF28.our_reserves_are_the_registers", all(r1000(a[e]["reserves"]) == r1000(sum(
        (x["indemnity_reserve"] or 0) + (x["defense_reserve"] or 0) for x in rows
        if x["incident_no"] in a[e]["missing"] and x["coverage_line"] == K.ENTITIES[e]["line"])) for e in ENTS))
    two_open = [i for i, rs in by_inc.items() if len({x["claim_no"] for x in rs if x["status"] in ("OPEN", "REOPENED")
                                                       and x["coverage_line"] != "CONTRACT"}) > 1]
    ok("askA.one_open_claim_number_per_incident", not two_open, str(two_open[:3]))
    notices = A.load_notices(target)
    notice_by_norm = {A.norm(k): v for k, v in notices.items()}
    reg_inc = {x["incident_no"] for x in rows}
    sig = {}
    for x in rows:
        sig.setdefault((x["entity_at_incident"], x["incident_date"], x["allegation"]), set()).add(x["incident_no"])
    _, qm = A.load_qm(target, K.QM_SEP)
    _, sc = A.load_sc(target)
    orphan_claims = [x for x in qm + sc if A.norm(x["ref"]).startswith("RMN") and x["ctype"] in ("Claim", "Suit")]
    n_dup, n_gl, bad = 0, 0, []
    twins = {e: 0 for e in ENTS}
    for x in orphan_claims:
        nrow = notice_by_norm[A.norm(x["ref"])]
        if nrow["incident_no"] in reg_inc:
            continue
        hits = sig.get((nrow["entity_code"], dt.date.fromisoformat(nrow["event_date"]), nrow["event_category"]), set())
        if len(hits) == 1:
            n_dup += 1
        elif not hits:
            n_gl += 1
            if x["status"] in ("Open", "O", "Reopened", "R"):
                twins[x["entity"]] += 1
        else:
            bad.append(x["ref"])
    ok("askA.dup_signatures_unique", not bad and n_dup >= 4, "%d matched, %d on claims against an entity alone, %d "
       "ambiguous" % (n_dup, n_gl, len(bad)))
    ok("SF29.notice_file_is_the_same_matter", not bad and n_dup == sum(len(a[e]["dup"]) for e in ENTS),
       "every carrier claim under a notice whose incident record holds no claim matches exactly one register claim or "
       "none (the entities' own claims)")
    ok("askA.benign_twins_every_entity", all(v >= 1 for v in twins.values()), str(twins))
    if world is not None:
        byno = {}
        for i in world["incidents"]:
            byno[getattr(i, "reg_incident_no", "") or i.incident_no] = i
        for e in ENTS:
            ok("askA.%s.gaps_are_constructed" % e, all(byno[i].unreported or byno[i].claims[0].made >= C.GAP_FIRST
                                                       for i in a[e]["missing"]), str(a[e]["missing"]))
            ok("askA.%s.dups_are_constructed" % e, all(byno[i].dup for i in a[e]["dup"]), str(a[e]["dup"]))
    b = A.ask_b(target)
    for e in ENTS:
        ok("askB.%s.S1_off" % e, b["s1"][e] != b["gold"][e], "%.1f against %.1f" % (b["s1"][e], b["gold"][e]))
        ok("askB.%s.S4_home_entity_off" % e, b["s4"][e] != b["gold"][e], "%.1f against %.1f" % (b["s4"][e], b["gold"][e]))
    ok("askB.S3_fellows_moves_alderwick", b["s3"]["AMC"] != b["gold"]["AMC"])
    ok("askB.home_entity_not_narrated", "time of the extract" not in dictionary and "at extract" not in dictionary)
    with open(os.path.join(target, K.HCM), encoding="utf-8") as fh:
        hcm = list(csv.DictReader(fh))
    cc = A.directory(target)
    xw = A.crosswalk(target)
    sept = [x for x in hcm if x["work_month"] == "2026-09" and sb.get(xw[x["job_profile_code"]])]
    dis_ = {(x["worker_id"], x["position_id"]) for x in sept if cc[x["cost_centre"]] != x["home_entity"]}
    if world is not None:
        ok("askB.only_the_movers_disagree", len(dis_) == len(world["W"].movers),
           "%d September positions charged to another entity's cost centre than the home entity" % len(dis_))
    pos = {}
    for x in hcm:
        if x["work_month"] == "2026-09":
            p_ = pos.setdefault((x["worker_id"], x["position_id"]), dict(reg=0, fte=set(), cc=set()))
            p_["reg"] += x["earning_code"] == "REG"
            p_["fte"].add(x["fte"])
            p_["cc"].add(x["cost_centre"])
    ok("askB.one_position_one_figure", all(p_["reg"] == 1 and len(p_["fte"]) == 1 and len(p_["cc"]) == 1
                                           for p_ in pos.values()), "%d September positions" % len(pos))
    workers = {}
    for (w_, p_) in pos:
        workers.setdefault(w_, set()).add(p_)
    ok("askB.one_position_per_worker", all(len(v) == 1 for v in workers.values()),
       "no clinician holds two positions in September 2026")
    diverge = [x["worker_id"] for x in sept if x["earning_code"] == "REG" and
               abs(float(x["hours"]) / 173.33 - float(x["fte"])) > 0.0051]
    ok("askB.hours_converge", not diverge and not any(x["work_month"] == "2026-09" and x["earning_code"] == "LOA"
                                                      for x in hcm), "%d lines" % len(diverge))
    ok("SF30.september_fte_converges", not diverge, "position FTE and the REG hours' FTE agree on every September line")
    with open(os.path.join(target, K.DIRECTORY), encoding="utf-8") as fh:
        opened = {x["cost_centre"]: x["effective_from"] for x in csv.DictReader(fh)}
    to_new = [x for x in sept if cc[x["cost_centre"]] != x["home_entity"] and x["home_entity"] == "BCH"]
    ok("SF31.entity_is_the_cost_centres", all(len(p_["cc"]) == 1 for p_ in pos.values()) and
       opened.get(K.cost_centre("BCH", "7110")) == "2026-10-01" and len(to_new) >= 1,
       "each September position has one cost centre; Brennick's rural clinic, the home entity of two movers, opens on "
       "1 October 2026 in the directory")

    # ------------------------------------------------------------------ separation line and deletion tests
    tmp = tempfile.mkdtemp()
    try:
        for f in (K.REGISTER, K.PAYROLL, K.PLAN, K.AGREEMENT, K.POLICY):
            shutil.copy(os.path.join(target, f), tmp)
        m2 = AN.main_call(tmp)
        ok("separation.call_reads_only_its_population", abs(m2["total"] - g) < 1e-6,
           "the call recomputes with the runs, notices, HCM lines, dictionary and distractors deleted")
    finally:
        shutil.rmtree(tmp)
    dup_inc = set()
    for e in ENTS:
        dup_inc |= set(a[e]["dup"])
    split = [i for i in dup_inc if len({x["incident_date"] for x in by_inc[i]}) != 1]
    ok("separation.dup_matters_grouped", not split, "the register keeps every claim number of a matter on one incident")
    tmp = tempfile.mkdtemp()
    try:
        for f in files:
            if f not in K.DISTRACTORS:
                shutil.copy(os.path.join(target, f), tmp)
        a2 = A.ask_a(tmp)
        b2 = A.ask_b(tmp)
        m3 = AN.main_call(tmp)
        ok("distractors.deletion", abs(m3["total"] - g) < 1e-6 and
           all(a2[e]["count"] == a[e]["count"] and a2[e]["reserves"] == a[e]["reserves"] for e in ENTS) and
           b2["gold"] == b["gold"])
    finally:
        shutil.rmtree(tmp)
    lo, hi = K.EXPERIENCE
    ctr = sum(1 for x in rows if x["coverage_line"] == "CONTRACT" and lo <= x["incident_date"] <= hi)
    ok("mess.contracted_rows_present", ctr > 0, "%d contracted rows in the experience years" % ctr)
    esc = sum(1 for c in ex if c["n_claim_nos"] > 1)
    ok("mess.escalations_present", esc >= 3, "%d experience Claims with a second claim number" % esc)

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
    ok("hygiene.pdf_no_dash", "\u2014" not in filed and "\u2013" not in filed)
    stamps = {int(os.path.getmtime(os.path.join(target, f))) for f in files}
    ok("hygiene.one_mtime", len(stamps) == 1)
    pack_text = " ".join(open(os.path.join(target, f), encoding="utf-8", errors="ignore").read()
                         for f in files if f.endswith((".csv", ".md")))
    others = re.findall(r"\b(?:Dr\.|Mr\.|Ms\.)\s+[A-Z][a-z]+", pack_text)
    ok("realism.no_unlisted_personas", not others, str(others[:5]))
    card = json.load(open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(target))), ".claude", "skills",
                                       "fingerprint", "cards", "task130.json")))
    ok("realism.personas_from_card", all(p_ in card["world"]["people"] for p_ in K.PEOPLE.values()))
    alleg = {}
    for x in rows:
        alleg[x["allegation"]] = alleg.get(x["allegation"], 0) + 1
    ok("realism.allegations_spread", max(alleg.values()) / len(rows) < 0.25)
    with open(os.path.join(target, K.EXTRACT_LOG), encoding="utf-8") as fh:
        logged = {x["file_name"] for x in csv.DictReader(fh)}
    ok("H9.extract_log_lists_every_file", logged == set(files) - {K.EXTRACT_LOG}, str(sorted(set(files) ^ logged)))
    ok("H9.dictionary_names_its_extracts", all(f in dictionary for f in (K.REGISTER, K.PAYROLL, K.HCM, K.CROSSWALK,
                                                                         K.DIRECTORY, K.NOTICES, K.QM_SEP, K.QM_JUN,
                                                                         K.SC_SEP, K.SAFETY)))
    vdate = K.VALUATION
    late = [x["claim_no"] for x in rows if x["claim_made_date"] > vdate or (x["closed_date"] and x["closed_date"] > vdate)]
    ok("H16.register_dates_by_valuation", not late, str(late[:3]))
    with open(os.path.join(target, K.NOTICES), encoding="utf-8") as fh:
        ok("H16.notices_by_valuation", max(x["sent_date"] for x in csv.DictReader(fh)) <= vdate.isoformat())
    ok("H16.hcm_by_september", max(x["work_month"] for x in hcm) == "2026-09")
    with open(os.path.join(target, K.SC_SEP), encoding="utf-8") as fh:
        rpt = [dt.date(int(x["DATE_RPTD"][6:]), int(x["DATE_RPTD"][:2]), int(x["DATE_RPTD"][3:5]))
               for x in csv.DictReader(fh)]
    ok("H16.stoneleigh_reports_by_valuation", max(rpt) <= vdate)

    # ------------------------------------------------------------------ the design note's record lines
    def lagcost(cl):
        tot_c = sum(c["cost"] for c in cl)
        early = sorted(c["cost"] for c in cl if c["lag"] <= 120)
        return "%d Claims, %d made within 120 days (median cost %s, %.2f of the cost), %d made after a year (%.2f)" % (
            len(cl), len(early), money(st.median(early)) if early else "n/a", sum(early) / tot_c,
            sum(1 for c in cl if c["lag"] > 365), sum(c["cost"] for c in cl if c["lag"] > 365) / tot_c)
    ok("record.program_experience", True, lagcost(exP))
    ok("record.other_experience", True, lagcost([c for c in ex if c["ent"] not in P]))
    ok("record.rivals", True, "; ".join("%s %s (%.3f)" % (k, money(v), v / g) for k, v in sorted(rv.items(),
                                                                                               key=lambda kv: kv[1])))
    if world is not None:
        inc = [i for i in world["incidents"] if lo <= i.date <= hi and i.cls]
        erp = [i for i in inc if i.route == "ERP"]
        dirc = [i for i in inc if i.route == "DIRECT"]
        esc_i = [i for i in erp if len(i.claims) > 1]
        ok("record.world_routes", True, "requests: median lag %.0f days, %d of %d escalated; direct: median lag %.0f "
           "days" % (st.median((i.claims[0].made - i.date).days for i in erp), len(esc_i), len(erp),
                     st.median((i.claims[0].made - i.date).days for i in dirc)))
    figs_json = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures.json")))
    ok("figures.contribution", figs_json["call"]["contribution"] == money(g))

    n_ok = sum(1 for _, c_, _ in RESULTS if c_)
    print("checks: %d of %d passed" % (n_ok, len(RESULTS)))
    if n_ok != len(RESULTS):
        raise SystemExit("checks failed: " + ", ".join(n for n, c_, _ in RESULTS if not c_))
    return RESULTS
