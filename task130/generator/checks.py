"""task130 assertions on the built pack and goldens: input gates, the three-rules block (R1 raw material, R2 one line
per Layer 1 item, R3a the analyst test on the clean truth, R3b the decisive step alone, R3c no plant), every route a
solver takes to the contribution (the natural routes a full bin off, the empirical constructions in the golden's
bin), the golden's sampling error, every semantic fork row (SF1 to SF30), the closure axes that can be asserted, the
asks with their stops and fairness, the separation line, distractor deletion, mid-bin figures, the realism sweep and
container hygiene."""
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
import world as WD

RESULTS = []
BIN = CA.BIN

# The natural routes: each lands a full bin or more from the golden and rounds to another figure.
MISS = ["R1_count_x_class_average", "R1m_count_x_mature_average", "R1g_count_x_lognormal_mean",
        "R1p_count_x_pooled_average", "R1y_count_x_average_made_within_year", "R1c_count_x_average_same_year",
        "R1w_count_x_average_within_entity_window",
        "R1t_count_x_average_by_matter_type", "R1a_count_x_average_by_allegation", "F1_loglog_by_class",
        "F2_loglinear_by_class", "F3_loglog_pooled", "F4_gamma_loglag_class_factors", "F5_gamma_lag_class_factors",
        "F6_gamma_quadratic_by_class", "B1_half_year_bands", "R0_mature_year", "R2_full_year_share_prorated",
        "R2b_same_year_prorated", "R3_window_length_filter"]
# The empirical constructions that condition cost on the delay finely enough: each rounds with the golden.
CONV = ["E1_30_day_bands", "E2_bands_30_90_180_365", "E3_bands_90_180_365", "E4_quarter_bands", "E5_bands_120_365",
        "S1_gamma_spline_by_class", "S2_quadratic_log_ols_by_class", "P1_pooled_lag_share_x_class_rate",
        "P2_all_classes_pooled", "P3_pooled_band_severity_x_class_counts"]
SAME_CONVENTIONS = ["lag_plus_1", "lag_minus_1", "transition_plus_1", "transition_minus_1", "window_end_plus_1",
                    "month_mid", "month_end", "calendar_day_exposure"]


def ok(name, cond, detail=""):
    RESULTS.append((name, bool(cond), detail))
    if not cond:
        print("FAIL %s %s" % (name, detail))


def r1000(x):
    return int(math.floor(x / 1000.0 + 0.5) * 1000)


def r1(x):
    return math.floor(x * 10 + 0.5) / 10


def edge(x, step):
    """Distance of x from its rounding edge as a share of the bin (0.5 at the bin's centre)."""
    return abs(((x / step) % 1.0) - 0.5)


def fmt(x):
    return "{:,}".format(int(round(x)))


def oracle(plan, tr, n=400000, seed=7):
    """The population truth, never shipped: the expected cost and count of the Claims first made in the 2027 window,
    from the claims world's own frequencies, report lags and cost distributions at the 2027 cost level (co-defendant
    shares, weekend dating and reserve noise left out)."""
    import numpy as np
    rng = np.random.default_rng(seed)
    lv = 1.05 ** 7 * np.exp(0.04 * rng.standard_normal(n))
    ln = lambda med, sig: med * np.exp(sig * rng.standard_normal(n))

    def lags(med, sig, lo, hi):
        x = np.round(med * np.exp(sig * rng.standard_normal(n * 3)))
        return np.sort(x[(x >= lo) & (x <= hi)][:n])
    cap = C.CAP_2020 * lv
    cost, lag = {}, {}
    for k in K.CLASSES:
        cost[("D", k)] = float((ln(C.DISCLOSED_IND[k], 0.35) * lv + ln(5000, 0.3) * lv).mean())
        lag[("D", k)] = lags(C.DISCLOSED_LAG[k], 0.45, 2, 75)
        esc = rng.random(n) < C.ESCALATE
        base = np.where(rng.random(n) < 0.30, 0.0, np.minimum(60000 * lv, ln(C.ERP_IND[k], 0.65) * lv)) + \
            ln(1500, 0.5) * lv
        with_ind = rng.random(n) < 0.10
        s_dfn = np.where(with_ind, ln(80000, 0.5), ln(55000, 0.5)) * lv
        s_ind = np.where(with_ind, ln(C.SUIT_IND[k], 0.6) * lv, 0.0)
        s_ind = np.where(s_ind + s_dfn > cap, np.maximum(0, cap - s_dfn), s_ind)
        cost[("E", k)] = float(np.where(esc, ln(1600, 0.6) * lv + s_ind + s_dfn, base).mean())
        lag[("E", k)] = lags(C.ERP_LAG_MEDIAN[k], C.ERP_LAG_SIGMA, 40, 365)
        dfn = np.where(rng.random(n) < 0.40, ln(95000, 0.45), ln(35000, 0.45)) * lv
        ind = np.where(rng.random(n) < 0.45, ln(C.DIRECT_IND[k], 0.6) * lv, 0.0)
        ind = np.where(ind + dfn > cap, np.maximum(0, cap - dfn), ind)
        cost[("R", k)] = float((ind + dfn).mean())
        lag[("R", k)] = lags(C.DIRECT_LAG_MEDIAN[k], C.DIRECT_LAG_SIGMA, 200, 3200)
    freq = {"D": C.F_DISCLOSED, "E": C.F_ERP, "R": C.F_DIRECT}
    tot = cnt = 0.0
    left = np.arange(CA.NDAYS - 1, -1, -1)
    for (e, k), row in sorted(plan.items()):
        w = CA.day_weights(row, tr[e])
        for r in "DER":
            p = np.searchsorted(lag[(r, k)], left, side="right") / len(lag[(r, k)])
            tot += freq[r][k] * cost[(r, k)] * float(np.dot(w, p))
            cnt += freq[r][k] * float(np.dot(w, p))
    return dict(cost=tot, count=cnt)


def run(target, golden, world=None, meta_path=None):
    del RESULTS[:]
    m = AN.main_call(target)
    g, rts, conv, rb = m["total"], m["routes"], m["conv"], m["rounded"]
    ex, E, plan, a, rows = m["ex"], m["E"], m["plan"], m["a"], m["rows"]
    tr = AN.transitions()
    files = sorted(os.listdir(target))
    golden_of = lambda claims, EE=E, pl=plan, tt=tr: CA.golden(claims, CA.lag_weights(pl, tt, EE, K.CLASSES,
                                                                                       K.ENTITY_ORDER))
    same_bin = lambda v: CA.rounded(v) == rb

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

    # ------------------------------------------------------------------ the pack agrees with the simulation
    ex_mem = E_mem = None
    if world is not None:
        ex_mem = C.experience_from_rows(world["rows"])
        lo, hi = K.EXPERIENCE
        E_mem = {k: 0.0 for k in K.CLASSES}
        for (p, y, mm, f) in WD.position_months(world["W"], (lo.year, 1), (hi.year, 12)):
            kk = K.CLASS_OF_JOB[p.job]
            if kk:
                E_mem[kk] += f / 12.0
        ok("bundle.experience_matches_simulation", len(ex_mem) == len(ex) and
           abs(sum(x["cost"] for x in ex_mem) - sum(x["cost"] for x in ex)) < 1.0,
           "%d/%d Claims" % (len(ex_mem), len(ex)))
        ok("bundle.exposure_matches_simulation", all(abs(E_mem[k] - E[k]) < 0.5 for k in K.CLASSES),
           "largest gap %.3f FTE-years" % max(abs(E_mem[k] - E[k]) for k in K.CLASSES))
        ok("bundle.plan_matches_simulation", {kk: [float(v) for v in vv] for kk, vv in world["plan"].items()} == plan)

    # ------------------------------------------------------------------ the three rules (dataset-generation 7.1)
    with open(os.path.join(target, K.REGISTER), encoding="utf-8") as fh:
        reg_cols = next(csv.reader(fh))
    with open(os.path.join(target, K.PAYROLL), encoding="utf-8") as fh:
        pay_cols = next(csv.reader(fh))
    ok("R1.register_carries_the_raw_claims", all(c in reg_cols for c in ("incident_date", "claim_made_date",
                                                                          "indemnity_paid", "defense_paid",
                                                                          "indemnity_reserve", "defense_reserve")),
       "the register ships every claim number's dates and amounts by defendant row")
    ok("R1.payroll_carries_monthly_fte", all(c in pay_cols for c in ("pay_month", "job_code", "fte")))
    shipped_cols = []
    for f in files:
        if f.endswith(".csv"):
            with open(os.path.join(target, f), encoding="utf-8") as fh:
                shipped_cols += [c.lower() for c in next(csv.reader(fh))]
    tells = [c for c in shipped_cols if re.search(r"lag|delay|window|per_fte|rate|route|program", c)]
    ok("R1.no_shipped_deciding_quantity", not tells, "no column holds a delay, a window share, a route or a rate: %s" %
       tells)
    ok("R1.golden_reads_register_rows", len(ex) > 1000 and sum(1 for c in ex if c["lag"] < CA.NDAYS) > 1000,
       "%d experience Claims, %d made within a year" % (len(ex), sum(1 for c in ex if c["lag"] < CA.NDAYS)))

    # R2: each Layer 1 item mishandled leaves the call in its bin
    by_inc = {}
    for x in rows:
        by_inc.setdefault(x["incident_no"], []).append(x)
    job_of = AN.job_lookup(m["job"])
    first_only = [x for x in rows if x["defendant_seq"] == 1]
    v = golden_of(C.experience_from_rows(first_only, job_of=job_of))
    ok("R2.defendant_rows_first_only", same_bin(v), "one defendant row a claim number: %s" % fmt(v))
    flat = [dict(cls=c["cls"], lag=L, cost=cost) for c in ex for (L, cost) in c["parts"]]
    v = golden_of(flat)
    ok("R2.claim_numbers_apart", same_bin(v), "each claim number its own Claim at its own date: %s" % fmt(v))
    contract_claims = 0
    for ino, rs in by_inc.items():
        if all(x["coverage_line"] == "CONTRACT" for x in rs) and K.EXPERIENCE[0] <= rs[0]["incident_date"] <= K.EXPERIENCE[1]:
            contract_claims += 1
    ok("R2.contracted_rows_unpriced", contract_claims > 0 and all(
        x["indemnity_paid"] is None and x["defense_paid"] is None for x in rows if x["coverage_line"] == "CONTRACT"),
       "%d experience incidents name only contracted clinicians, every contracted row unpriced, so counting them adds "
       "no cost" % contract_claims)
    saved = dict(K.CLASS_OF_JOB)
    try:
        K.CLASS_OF_JOB.update({"RES": "HM", "FEL": "HM"})
        ex_res = C.experience_from_rows(rows, job_of=job_of)
    finally:
        K.CLASS_OF_JOB.clear()
        K.CLASS_OF_JOB.update(saved)
    E_res = dict(E)
    with open(os.path.join(target, K.PAYROLL), encoding="utf-8") as fh:
        for x in csv.DictReader(fh):
            if x["job_code"] in ("25010", "GME-RES", "25020", "GME-FEL") and "2016-01" <= x["pay_month"] <= "2024-12":
                E_res["HM"] += float(x["fte"]) / 12.0
    v_res = golden_of(ex_res, E_res)
    ok("R2.trainees_on_claims", same_bin(v_res),
       "residents and fellows counted as hospital medicine (claims, rows and FTE): %s" % fmt(v_res))
    # the 2020 code set alone: claims and exposure from July 2020
    new_codes = {j[2] for j in K.JOBS}
    E20 = {k: 0.0 for k in K.CLASSES}
    sb = AN.schedule_b()
    with open(os.path.join(target, K.PAYROLL), encoding="utf-8") as fh:
        for x in csv.DictReader(fh):
            if x["job_code"] in new_codes and sb.get(x["job_code"]) and x["pay_month"] <= "2024-12":
                E20[sb[x["job_code"]]] += float(x["fte"]) / 12.0
    ex20 = [c for c in ex if (c["year"], 0) >= (2020, 0) and
            min(r_["incident_date"] for r_ in by_inc[c["incident_no"]]) >= dt.date(2020, 7, 1)]
    v20 = golden_of(ex20, E20)
    ok("R2.job_codes_2020_set_only", same_bin(v20), "claims and exposure from July 2020 only: %s" % fmt(v20))
    per_diem_ids = set()
    E_pd = {k: 0.0 for k in K.CLASSES}
    with open(os.path.join(target, K.PAYROLL), encoding="utf-8") as fh:
        for x in csv.DictReader(fh):
            if sb.get(x["job_code"]) and "2016-01" <= x["pay_month"] <= "2024-12":
                if len(x["fte"].split(".")[1]) == 2:
                    per_diem_ids.add(x["employee_id"])
                    continue
                E_pd[sb[x["job_code"]]] += float(x["fte"]) / 12.0
    v = golden_of(ex, E_pd)
    ok("R2.per_diem_rows_dropped", per_diem_ids and same_bin(v), "%d per-diem clinicians' rows out of the exposure: %s" %
       (len(per_diem_ids), fmt(v)))
    seen_month = set()
    E_one = {k: 0.0 for k in K.CLASSES}
    dual = 0
    with open(os.path.join(target, K.PAYROLL), encoding="utf-8") as fh:
        for x in csv.DictReader(fh):
            if sb.get(x["job_code"]) and "2016-01" <= x["pay_month"] <= "2024-12":
                key = (x["employee_id"], x["pay_month"])
                if key in seen_month:
                    dual += 1
                    continue
                seen_month.add(key)
                E_one[sb[x["job_code"]]] += float(x["fte"]) / 12.0
    v = golden_of(ex, E_one)
    ok("R2.second_cost_centre_row_dropped", dual > 0 and same_bin(v),
       "%d second rows (dual appointments, transfers) dropped: %s" % (dual, fmt(v)))
    reopen_free = []
    for c in ex:
        rs = [x for x in by_inc[c["incident_no"]] if x["status"] == "REOPENED"]
        reopen_free.append(dict(c, cost=c["cost"] - sum((x["defense_reserve"] or 0) for x in rs) *
                                K.trend_factor(c["year"])) if rs else c)
    v = golden_of(reopen_free)
    ok("R2.reopened_reserves_dropped", same_bin(v), "reopened claims at their paid amounts: %s" % fmt(v))
    leave_rows = 0
    with open(os.path.join(target, K.PAYROLL), encoding="utf-8") as fh:
        for x in csv.DictReader(fh):
            if x["emp_status"] == "L":
                leave_rows += 1
                if float(x["fte"]) != 0.0:
                    leave_rows = -10 ** 9
    ok("R2.leave_months_zero", leave_rows > 0, "%d leave-of-absence months, every one at 0.0 FTE" % leave_rows)
    # the asks' devices do not reach the call: the register's coverage line recoded to the carrier of the incident date
    recoded = []
    for x in rows:
        y = dict(x)
        if x["coverage_line"] != "CONTRACT":
            e = x["entity_at_incident"]
            y["coverage_line"] = "%s-%s" % (K.carrier_on(e, x["incident_date"]), e)
        recoded.append(y)
    v = golden_of(C.experience_from_rows(recoded, job_of=job_of))
    ok("R2.ask_devices_off_the_call", abs(v - g) < 1e-6,
       "the coverage line recoded by carrier era leaves the golden to the cent; the HCM lines are not read")

    # R3a: the analyst test on the clean truth, and on the pack
    if world is not None:
        rts_mem, a_mem = CA.routes(ex_mem, E_mem, world["plan"], tr, K.CLASSES, K.ENTITY_ORDER)
        g_mem = rts_mem["golden"]
        d = rts_mem["R1_count_x_class_average"]
        ok("R3a.analyst_test_clean_truth", abs(d - g_mem) >= BIN and CA.rounded(d) != CA.rounded(g_mem),
           "the claims made in the window counted per class, at the class's average Claim cost, every filed rule "
           "applied, on the generator's clean truth: %s against the golden %s" % (fmt(d), fmt(g_mem)))
        ok("R3a.clean_truth_golden_same_bin", CA.rounded(g_mem) == rb, "%s" % fmt(g_mem))
        worst = min(MISS, key=lambda k: abs(rts_mem[k] - g_mem))
        ok("R3a.every_natural_route_clean_truth", all(abs(rts_mem[k] - g_mem) >= BIN and
                                                      CA.rounded(rts_mem[k]) != CA.rounded(g_mem) for k in MISS),
           "nearest %s at %s" % (worst, fmt(abs(rts_mem[worst] - g_mem))))
    d = rts["R1_count_x_class_average"]
    ok("R3a.analyst_test_pack", abs(d - g) >= BIN and CA.rounded(d) != rb, "%s (rounds %s) against %s" % (
        fmt(d), "{:,}".format(CA.rounded(d)), fmt(g)))
    # R3b: the easy route with only the decisive step changed lands the golden; each other single correction does not
    own = sum(a[c["cls"]][c["lag"]] * c["cost"] for c in ex if c["lag"] < CA.NDAYS)
    ok("R3b.decisive_step_alone", abs(own - g) < 1e-6,
       "the default route with each window Claim at its own cost in place of the class average is the golden")
    ok("R3b.window_alone_is_not_enough", CA.rounded(rts["R1_count_x_class_average"]) != rb and
       CA.rounded(rts["R0_mature_year"]) != rb,
       "the window truncation alone (count at the class average) %s; the claim-level cost without the window (a mature "
       "year) %s" % (fmt(rts["R1_count_x_class_average"]), fmt(rts["R0_mature_year"])))
    ok("R3b.severity_by_year_not_enough", CA.rounded(rts["R1y_count_x_average_made_within_year"]) != rb and
       CA.rounded(rts["B1_half_year_bands"]) != rb,
       "a severity from the Claims made within a year %s, half-year bands %s" % (
           fmt(rts["R1y_count_x_average_made_within_year"]), fmt(rts["B1_half_year_bands"])))
    # R3c: no plant
    with open(os.path.join(target, K.PAYROLL), encoding="utf-8") as fh:
        months = {}
        for x in csv.DictReader(fh):
            months.setdefault(x["pay_month"], []).append((x["employee_id"], x["cost_centre"], x["fte"]))
    keys = sorted(months)
    repeats = sum(1 for k1, k2 in zip(keys, keys[1:]) if sorted(months[k1]) == sorted(months[k2]))
    ok("R3c.no_repeated_payroll_block", repeats == 0, "%d consecutive months identical" % repeats)
    dup = len(rows) - len({(x["claim_no"], x["defendant_seq"]) for x in rows})
    ok("R3c.no_copied_register_rows", dup == 0)
    amounts = {}
    for x in rows:
        if x["coverage_line"] != "CONTRACT" and (x["indemnity_paid"] or 0) > 0:
            amounts.setdefault((x["indemnity_paid"], x["defense_paid"]), set()).add(x["incident_no"])
    copied = sum(1 for s in amounts.values() if len(s) > 1)
    ok("R3c.no_copied_amounts", copied <= 2, "%d amount pairs on two incidents" % copied)
    memo_like = [f for f in files if re.search(r"memo|draft|note|email|letter", f, re.I)]
    ok("R3c.no_memo_or_draft", not memo_like, str(memo_like))
    figures_text = " ".join(open(os.path.join(target, f), encoding="utf-8", errors="ignore").read()
                            for f in files if f.endswith((".csv", ".md")))
    ok("R3c.no_stakeholder_figure", "{:,}".format(rb) not in figures_text and
       "{:,}".format(CA.rounded(rts["R1_count_x_class_average"])) not in figures_text)

    # ------------------------------------------------------------------ routes
    worst = min(MISS, key=lambda k: abs(rts[k] - g))
    for k in MISS:
        ok("route.miss.%s" % k, abs(rts[k] - g) >= BIN and CA.rounded(rts[k]) != rb,
           "%s (%.3fx), rounds %s" % (fmt(rts[k]), rts[k] / g, "{:,}".format(CA.rounded(rts[k]))))
    ok("route.nearest_miss", abs(rts[worst] - g) >= BIN, "%s %s from the golden" % (worst, fmt(abs(rts[worst] - g))))
    for k in CONV:
        ok("route.converges.%s" % k, same_bin(rts[k]), "%s (%.3fx)" % (fmt(rts[k]), rts[k] / g))
    ok("route.golden_mid_bin", abs(g - rb) <= 0.25 * BIN, "%s, %s from the bin's centre" % (fmt(g), fmt(abs(g - rb))))
    for name, sd in (("poisson", m["sd"]), ("bootstrap", m["boot_sd"])):
        ok("route.one_sigma_%s" % name, CA.rounded(g - sd) == rb and CA.rounded(g + sd) == rb,
           "SD %s (%.1f%%): %s to %s" % (fmt(sd), 100 * sd / g, fmt(g - sd), fmt(g + sd)))
    window_claims = [c for c in ex if c["lag"] < CA.NDAYS]
    top = sorted((a[c["cls"]][c["lag"]] * c["cost"] for c in window_claims), reverse=True)
    ok("route.not_sized_from_a_few_claims", top[0] / g < 0.05 and sum(top[:10]) / g < 0.25,
       "%d window Claims; the largest carries %.1f%%, the ten largest %.1f%%" % (len(window_claims), 100 * top[0] / g,
                                                                                100 * sum(top[:10]) / g))
    for k in SAME_CONVENTIONS:
        ok("convention.%s" % k, same_bin(conv[k]), "%s (%.4fx)" % (fmt(conv[k]), conv[k] / g))

    slips = {"first_row_only": golden_of(C.experience_from_rows(first_only, job_of=job_of)),
             "claim_numbers_apart": golden_of(flat), "trainees": v_res, "codes_2020_only": v20,
             "per_diem_dropped": golden_of(ex, E_pd), "second_rows_dropped": golden_of(ex, E_one)}
    big_slip = max(slips, key=lambda k: abs(slips[k] - g))
    decisive = abs(rts["R1_count_x_class_average"] - g)
    ok("route.dominance", decisive >= 10 * abs(slips[big_slip] - g),
       "the decisive step %s against the largest Layer 1 slip (%s) %s: %.1f times" % (
           fmt(decisive), big_slip, fmt(abs(slips[big_slip] - g)), decisive / abs(slips[big_slip] - g)))
    if world is not None:
        orc = oracle(plan, tr)
        ok("oracle.population_truth", CA.rounded(orc["cost"]) == rb and abs(orc["cost"] - g) <= 1.5 * m["sd"],
           "the generating parameters' expected 2027 window cost %s (%.2f Claims): the golden is %.3f of it; the "
           "default %.2f times it" % (fmt(orc["cost"]), orc["count"], g / orc["cost"],
                                      rts["R1_count_x_class_average"] / orc["cost"]))

    # ------------------------------------------------------------------ semantic fork table
    def _pdf(name):
        return re.sub(r"\s+", " ", " ".join(p.extract_text() for p in PdfReader(os.path.join(target, name)).pages))
    filed = _pdf(K.AGREEMENT) + " " + _pdf(K.POLICY)
    ok("SF1.no_margin", "carries no provision for the Trust's administrative expenses" in filed,
       "a 5%% loading files %s" % "{:,}".format(CA.rounded(g * 1.05)))
    ok("SF2.claims_made_trigger", CA.rounded(rts["R0_mature_year"]) != rb and
       "A Claim first made after the end of a Plan Year is not covered" in filed,
       "the occurrence reading (every Claim from 2027 incidents) %s" % fmt(rts["R0_mature_year"]))
    ok("SF3.one_claim_per_incident", same_bin(golden_of(flat)) and "are one Claim, first made on the date the earliest"
       in filed, "claim numbers apart: same call")
    ok("SF4.covered_clinicians", "Residents, fellows and other trainees" in filed,
       "residents and fellows counted: %s" % fmt(v_res))
    def rescost(fn):
        out = []
        for c in ex:
            rs = [x for x in by_inc[c["incident_no"]] if x["coverage_line"] != "CONTRACT" and
                  K.CLASS_OF_JOB.get(job_of(x["clinician_id"], x["incident_date"])) is not None]
            out.append(dict(c, cost=sum(fn(x) for x in rs) * K.trend_factor(c["year"])))
        return out
    full_check = rescost(lambda x: (x["indemnity_paid"] or 0) + (x["defense_paid"] or 0) + (x["indemnity_reserve"] or 0)
                         + (x["defense_reserve"] or 0))
    paid = rescost(lambda x: (x["indemnity_paid"] or 0) + (x["defense_paid"] or 0))
    indem = rescost(lambda x: (x["indemnity_paid"] or 0) + (x["indemnity_reserve"] or 0))
    ok("SF5.cost_basis_reproduces", abs(sum(c["cost"] for c in full_check) - sum(c["cost"] for c in ex)) < 0.01)
    ok("SF5.paid_only", True, "paid only: %s; ruled out by 3.4 (case reserves)" % fmt(golden_of(paid)))
    ok("SF5.indemnity_only", True, "indemnity only: %s; ruled out by 3.4 (indemnity and defence)" % fmt(golden_of(indem)))
    ex6 = [dict(c, cost=c["cost"] / K.trend_factor(c["year"]) * K.trend_factor(c["year"] + (0 if c["same_year"] else 1)))
           for c in ex]
    ok("SF6.trend_from_incident_year", "compounded from the calendar year of its Medical Incident" in filed,
       "trended from the year made: %s" % fmt(golden_of(ex6)))
    for lo_y in (2017, 2020):
        exy = [c for c in ex if c["year"] >= lo_y]
        Ey = AN.load_payroll(target, first="%d-01" % lo_y)[1]
        ok("SF7.experience_from_%d" % lo_y, "from 1 January 2016 to 31 December 2024" in filed,
           "experience %d to 2024: %s" % (lo_y, fmt(golden_of(exy, Ey))))
    ok("SF8.pooled_within_class", same_bin(rts["P2_all_classes_pooled"]) and "pooled within each specialty class" in filed,
       "all classes pooled: %s (same call)" % fmt(rts["P2_all_classes_pooled"]))
    tot_by_entity = 0.0
    for e in K.ENTITY_ORDER:
        ce = [c for c in ex if c["entity"] == e]
        pe = {kk: vv for kk, vv in plan.items() if kk[0] == e}
        Ee = {k: 0.0 for k in K.CLASSES}
        with open(os.path.join(target, K.PAYROLL), encoding="utf-8") as fh:
            for x in csv.DictReader(fh):
                if x["entity_code"] == e and sb.get(x["job_code"]) and "2016-01" <= x["pay_month"] <= "2024-12":
                    Ee[sb[x["job_code"]]] += float(x["fte"]) / 12.0
        ks = [k for k in K.CLASSES if (e, k) in pe and Ee[k] > 0]
        if ks:
            tot_by_entity += CA.golden([c for c in ce if c["cls"] in ks],
                                       CA.lag_weights(pe, tr, Ee, ks, [e]))
    ok("SF8.not_by_entity", True, "each entity on its own experience: %s; ruled out by 3.3 (pooled within each class)" %
       fmt(tot_by_entity))
    tr0 = {e: K.PLAN_START for e in K.ENTITY_ORDER}
    v0 = golden_of(ex, E, plan, tr0)
    ok("SF9.from_transition_date", CA.rounded(v0) != rb and "month from the entity's Transition Date" in filed,
       "every entity from 1 January: %s" % fmt(v0))
    wbp = openpyxl.load_workbook(os.path.join(target, K.PLAN), data_only=True)
    plan_note = " ".join(str(c.value) for row in wbp["Notes"].iter_rows() for c in row if c.value)
    ok("SF10.month_timing", all(same_bin(conv[k]) for k in ("month_mid", "month_end", "calendar_day_exposure")) and
       "held through the month" in plan_note,
       "mid-month %s, end of month %s, calendar days %s; each month's exposure at its first day %s, against the plan's "
       "'held through the month'" % (fmt(conv["month_mid"]), fmt(conv["month_end"]), fmt(conv["calendar_day_exposure"]),
                                     fmt(conv["month_start"])))
    spec_class = {}
    for jk, texts in C.SPECIALTY_TEXT.items():
        for t in texts:
            spec_class.setdefault(t, set()).add(K.CLASS_OF_JOB.get(jk))
    agree = 0
    for c in ex:
        rs = sorted((x for x in by_inc[c["incident_no"]] if x["coverage_line"] != "CONTRACT" and
                     K.CLASS_OF_JOB.get(job_of(x["clinician_id"], x["incident_date"])) is not None),
                    key=lambda x: (x["claim_made_date"], x["claim_no"], x["defendant_seq"]))
        if spec_class.get(rs[0]["specialty"]) == {c["cls"]}:
            agree += 1
    ok("SF11.class_text_converges", agree == len(ex), "%d of %d" % (agree, len(ex)))
    ok("SF12.four_entities_seven_classes", {e for e, _ in plan} == set(K.ENTITY_ORDER) and
       {k for _, k in plan} == set(K.CLASSES))
    ok("SF13.day_count", all(same_bin(conv[k]) for k in ("lag_plus_1", "lag_minus_1", "transition_plus_1",
                                                         "transition_minus_1", "window_end_plus_1")),
       ", ".join("%s %s" % (k, fmt(conv[k])) for k in ("lag_plus_1", "lag_minus_1", "transition_plus_1",
                                                      "transition_minus_1", "window_end_plus_1")))
    ok("SF14.rounded_once", rb == CA.rounded(g) and "rounded once, from unrounded amounts" in filed)
    ind_cost = {c["incident_no"]: c["cost"] for c in indem}
    ex15 = [c for c in ex if ind_cost[c["incident_no"]] > 0]
    ok("SF15.defence_only_claims_counted", len(ex15) < len(ex),
       "%d Claims without indemnity; left out: %s" % (len(ex) - len(ex15), fmt(golden_of(ex15))))
    biggest = max(c["cost"] for c in window_claims)
    ok("SF16.limit_cannot_bind", biggest < K.LIMIT_PER_CLAIM, "largest Claim made within a year %s" % fmt(biggest))
    chains = [c for c in ex if c["n_claim_nos"] > 1]
    repeats = 0
    for c in chains:
        sets = {}
        for x in by_inc[c["incident_no"]]:
            if x["coverage_line"] != "CONTRACT":
                sets.setdefault(x["claim_no"], []).append((x["clinician_id"], x["indemnity_paid"], x["defense_paid"],
                                                           x["indemnity_reserve"], x["defense_reserve"]))
        vals = [tuple(sorted(v_)) for v_ in sets.values()]
        repeats += len(vals) != len(set(vals))
    later = [dict(c, cost=sorted(c["parts"])[-1][1]) if c["n_claim_nos"] > 1 else c for c in ex]
    ok("SF17.claim_numbers_added", bool(chains) and repeats == 0,
       "%d chains, %d repeat an amount set; the later claim number alone %s" % (len(chains), repeats,
                                                                               fmt(golden_of(later))))
    ok("SF18.per_diem_paid_fte", True, "per-diem rows out of the exposure: same call (R2.per_diem_rows_dropped)")
    ok("SF19.month_as_twelfth", same_bin(conv["calendar_day_exposure"]), "calendar-day exposure %s" %
       fmt(conv["calendar_day_exposure"]))
    lo, hi = K.EXPERIENCE
    hi_saved = K.EXPERIENCE
    try:
        K.EXPERIENCE = (lo, dt.date(2025, 12, 31))
        ex25 = C.experience_from_rows(rows, job_of=job_of)
    finally:
        K.EXPERIENCE = hi_saved
    E25 = AN.load_payroll(target, last="2025-12")[1]
    ok("SF20.experience_to_2024", "31 December 2024" in filed, "2025 incidents added: %s" % fmt(golden_of(ex25, E25)))
    ok("SF21.escalations_at_the_request", same_bin(golden_of(flat)), "= SF3")
    E20all = {k: 0.0 for k in K.CLASSES}
    with open(os.path.join(target, K.PAYROLL), encoding="utf-8") as fh:
        for x in csv.DictReader(fh):
            if x["job_code"] in new_codes and sb.get(x["job_code"]) and "2016-01" <= x["pay_month"] <= "2024-12":
                E20all[sb[x["job_code"]]] += float(x["fte"]) / 12.0
    v22 = golden_of(ex, E20all)
    ok("SF22.both_code_sets", CA.rounded(v22) != rb, "the 2020 code set's exposure under every Claim: %s" % fmt(v22))

    # ------------------------------------------------------------------ closure axes
    lag_ok = max(dt.date(c["year"], 12, 31) + dt.timedelta(days=c["lag"]) for c in window_claims) < K.VALUATION
    ok("axis12.window_delays_reported", lag_ok, "every experience Claim made within a year is in the extract")
    perm = []
    for seed in (1, 2, 3):
        rr = list(rows)
        random.Random(seed).shuffle(rr)
        perm.append(golden_of(C.experience_from_rows(rr, job_of=job_of)))
    ok("axis14.row_order", all(abs(p - g) < 1e-6 for p in perm))
    covered_ids = {x["clinician_id"] for x in rows if x["coverage_line"] != "CONTRACT" and lo <= x["incident_date"] <= hi}
    in_pay = {k[0] for k in m["job"]}
    missing_ids = [cid for cid in covered_ids if cid not in in_pay]
    ok("axis16.ids_in_payroll", not missing_ids, "%d ids" % len(missing_ids))
    neg = [x for x in rows if any((x[f] or 0) < 0 for f in ("indemnity_paid", "defense_paid", "indemnity_reserve",
                                                              "defense_reserve"))]
    ok("axis17.no_negative_amounts", not neg)
    ok("axis22.plan_full_year", all(len(v_) == 12 and min(v_) > 0 for v_ in plan.values()))
    tr_p = {e: tr[e] + dt.timedelta(days=1) for e in tr}
    tr_m = dict({e: tr[e] - dt.timedelta(days=1) for e in tr}, TFH=tr["TFH"])
    alt_counts = [CA.count(ex, CA.lag_weights(plan, t_, E, K.CLASSES, K.ENTITY_ORDER)) for t_ in (tr_p, tr_m)]
    alt_counts.append(CA.count([dict(c, lag=c["lag"] + 1) for c in ex], a))
    ok("axis20.expected_claims_not_graded", True, "%.2f expected Claims; one-day variants %s, so no count is stated as "
       "a graded figure" % (m["count"], ", ".join("%.2f" % x for x in alt_counts)))

    # ------------------------------------------------------------------ asks
    aa = A.ask_a(target, rows)
    for e in K.ENTITY_ORDER:
        v_ = aa[e]
        gold = (v_["count"], r1000(v_["reserves"]))
        ok("askA.%s.S1_cracker_off" % e, (v_["s1"][0], r1000(v_["s1"][1])) != gold and v_["s1"][0] != v_["count"],
           "every open claim on the coverage line: %d, %s against %d, %s" % (v_["s1"][0], fmt(v_["s1"][1]), *gold))
        ok("askA.%s.S2_notices_off" % e, v_["s2"][0] != v_["count"], "%d against %d" % (v_["s2"][0], v_["count"]))
        if e in ("TFH", "AMC"):
            ok("askA.%s.S4_june_run_off" % e, v_["s4"][0] != v_["count"], "%d against %d" % (v_["s4"][0], v_["count"]))
        ok("askA.%s.old_era_open" % e, len(v_["old_era"]) >= 1, "%d open claims from incidents before %s" % (
            len(v_["old_era"]), v_["era_start"]))
    s3_off = [e for e in K.ENTITY_ORDER if (aa[e]["s3"][0], r1000(aa[e]["s3"][1])) != (aa[e]["count"],
                                                                                      r1000(aa[e]["reserves"]))]
    ok("askA.S3_claim_numbers_moves", len(s3_off) >= 2, "suits not read through their earlier claim number move %s" %
       ", ".join(s3_off))
    ok("askA.none_is_an_answer", any(aa[e]["count"] == 0 for e in K.ENTITY_ORDER))
    ok("askA.some_missing", sum(1 for e in K.ENTITY_ORDER if aa[e]["count"] > 0) >= 2)
    ok("askA.S5_contracted_moves", any(aa[e]["s5"][0] != aa[e]["count"] for e in K.ENTITY_ORDER))
    a_open = A.ask_a(target, [dict(x, status="CLOSED") if x["status"] == "REOPENED" else x for x in rows])
    ok("SF23.open_and_reopened_converge", all(a_open[e]["count"] == aa[e]["count"] and
                                              abs(a_open[e]["reserves"] - aa[e]["reserves"]) < 0.01
                                              for e in K.ENTITY_ORDER),
       "OPEN alone: " + ", ".join("%s %d" % (e, a_open[e]["count"]) for e in K.ENTITY_ORDER))
    two_open = [i for i, rs in by_inc.items() if len({x["claim_no"] for x in rs if x["status"] in ("OPEN", "REOPENED")
                                                       and x["coverage_line"] != "CONTRACT"}) > 1]
    ok("SF24.one_open_claim_number_per_incident", not two_open, str(two_open[:3]))
    ok("SF25.latest_valuation", all(aa[e]["s4"][0] != aa[e]["count"] for e in ("TFH", "AMC")),
       "the June run's revision 1 (received last) moves both Quillan entities")
    ok("SF26.carrier_era", all(aa[e]["s1"][0] != aa[e]["count"] for e in K.ENTITY_ORDER),
       "the coverage line alone moves every entity; the premium history dates each carrier's terms")
    no_contract = A.ask_a(target, [x for x in rows if x["coverage_line"] != "CONTRACT"])
    ok("SF27.reserves_on_our_rows", all(no_contract[e]["count"] == aa[e]["count"] and
                                        abs(no_contract[e]["reserves"] - aa[e]["reserves"]) < 0.01
                                        for e in K.ENTITY_ORDER))
    if world is not None:
        on_sep = {(r_["entity"], r_["incident_no"]) for r_ in world["sep"]}
        byno = {i.incident_no: i for i in world["incidents"]}
        for e in K.ENTITY_ORDER:
            line = K.ENTITIES[e]["line"]
            truth = sorted({x["incident_no"] for x in world["rows"] if x["coverage_line"] == line and
                            x["status"] in ("OPEN", "REOPENED") and
                            byno[x["incident_no"]].date >= K.ENTITIES[e]["carrier_from"]
                            and (e, x["incident_no"]) not in on_sep})
            ok("askA.%s.fair" % e, truth == sorted(aa[e]["missing"]), "%s" % truth)
            ok("askA.%s.gaps_are_real" % e, all(byno[i].unreported or byno[i].claims[0].made >= C.GAP_FIRST or
                                                any(c.made >= C.GAP_FIRST for c in byno[i].claims)
                                                for i in aa[e]["missing"]), str(aa[e]["missing"]))
            ok("askA.%s.era_start_filed" % e, aa[e]["era_start"] == K.ENTITIES[e]["carrier_from"])
    bb = A.ask_b(target)
    cells = [(e, mo) for e in K.ENTITY_ORDER for mo in A.ASK_B_MONTHS]
    for n in ("s1", "s3", "s4"):
        off = [c_ for c_ in cells if r1(bb[n][c_]) != r1(bb["gold"][c_])]
        ok("askB.%s_moves_every_cell" % n, len(off) == len(cells), "%d of %d cells" % (len(off), len(cells)))
    off2 = [c_ for c_ in cells if r1(bb["s2"][c_]) != r1(bb["gold"][c_])]
    ok("askB.s2_position_fte_moves", len(off2) >= 10, "%d of %d cells" % (len(off2), len(cells)))
    off5 = [c_ for c_ in cells if r1(bb["s5"][c_]) != r1(bb["gold"][c_])]
    ok("askB.s5_per_diem_moves", len(off5) >= 10, "%d of %d cells" % (len(off5), len(cells)))
    lines = A.hcm_lines(target)
    xw = A.crosswalk(target)
    trainee_any = {r_["worker_id"] for r_ in lines if xw[r_["job_profile_code"]] in A.TRAINEE_CODES}
    alt = {c_: 0.0 for c_ in cells}
    cc = A.directory(target)
    for r_ in lines:
        if sb.get(xw[r_["job_profile_code"]]) and r_["worker_id"] not in trainee_any:
            alt[(cc[r_["cost_centre"]], r_["work_month"])] += float(r_["hours"]) / A.HOURS_FULL
    ok("SF29.trainee_in_month_or_quarter", all(r1(alt[c_]) == r1(bb["gold"][c_]) for c_ in cells))
    alt2 = {c_: v_ * A.HOURS_FULL / (2080.0 / 12) for c_, v_ in bb["gold"].items()}
    ok("SF28.hours_per_fte_month", all(r1(alt2[c_]) == r1(bb["gold"][c_]) for c_ in cells),
       "2,080 over 12 against 173.33 gives the same figures")
    worst_b = min(cells, key=lambda c_: edge(bb["gold"][c_], 0.1))
    ok("askB.mid_bin", edge(bb["gold"][worst_b], 0.1) >= 0.1, "worst %s at %.3f of the bin" % (
        worst_b, edge(bb["gold"][worst_b], 0.1)))
    with open(os.path.join(target, K.HCM), encoding="utf-8") as fh:
        hcm_cols = next(csv.reader(fh))
    ok("SF30.entity_by_cost_centre", not any("entity" in c_ for c_ in hcm_cols), str(hcm_cols))
    if world is not None:
        W = world["W"]
        truth = {c_: 0.0 for c_ in cells}
        for p in W.positions:
            if K.CLASS_OF_JOB.get(p.job) is None or p.moonlight:
                continue
            for mo in A.ASK_B_MONTHS:
                y, mm = int(mo[:4]), int(mo[5:])
                if p.held_share(y, mm) <= 0 or (p.per_diem and p.shifts_held(y, mm) < 1):
                    continue
                import records as RC
                truth[(p.entity, mo)] += RC.hcm_hours(p, y, mm) / WD.HOURS_FULL
        ok("askB.fair", all(abs(truth[c_] - bb["gold"][c_]) < 0.02 for c_ in cells),
           "largest gap %.4f" % max(abs(truth[c_] - bb["gold"][c_]) for c_ in cells))
        moon = [p for p in W.positions if p.moonlight]
        per_cell = {c_: 0 for c_ in cells}
        for p in moon:
            for mo in A.ASK_B_MONTHS:
                y, mm = int(mo[:4]), int(mo[5:])
                if p.held_share(y, mm) > 0:
                    per_cell[(p.entity, mo)] += 1
        ok("askB.moonlighting_every_cell", all(v_ >= 1 for v_ in per_cell.values()),
           "%d additional positions; fewest in a cell %d" % (len(moon), min(per_cell.values())))

    # ------------------------------------------------------------------ separation line and deletion tests
    tmp = tempfile.mkdtemp()
    try:
        for f in (K.REGISTER, K.PAYROLL, K.PLAN, K.AGREEMENT, K.POLICY):
            shutil.copy(os.path.join(target, f), tmp)
        m2 = AN.main_call(tmp)
        ok("separation.call_reads_only_its_population", abs(m2["total"] - g) < 1e-6,
           "the call recomputes with the runs, notices, premium history, HCM lines and distractors deleted")
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
           all(a2[e]["count"] == aa[e]["count"] and a2[e]["reserves"] == aa[e]["reserves"] for e in K.ENTITY_ORDER) and
           b2["gold"] == bb["gold"])
    finally:
        shutil.rmtree(tmp)
    hcm_in_call = any(f == K.HCM for f in (K.REGISTER, K.PAYROLL, K.PLAN))
    ok("separation.zero_device_rows_in_the_call", not hcm_in_call,
       "Ask B's lines are outside the call's files; Ask A's carrier era lives in the premium history and the runs")

    # ------------------------------------------------------------------ realism sweep and hygiene
    text_files = [f for f in files if f.endswith((".csv", ".md"))]
    dash = [f for f in text_files if "—" in open(os.path.join(target, f), encoding="utf-8").read() or
            "–" in open(os.path.join(target, f), encoding="utf-8").read()]
    ok("hygiene.no_em_dash_text", not dash, str(dash))
    for f in files:
        if f.endswith((".xlsx", ".pptx", ".docx")):
            z = zipfile.ZipFile(os.path.join(target, f))
            blob = b"".join(z.read(n) for n in z.namelist() if n.startswith("docProps"))
            ok("hygiene.%s.no_library" % f, b"openpyxl" not in blob and b"python-pptx" not in blob)
            body = b"".join(z.read(n) for n in z.namelist())
            ok("hygiene.%s.no_dash" % f, "—".encode() not in body and "–".encode() not in body)
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
    card = json.load(open(os.path.join(os.path.dirname(os.path.dirname(target)), ".claude", "skills", "fingerprint",
                                       "cards", "task130.json")))
    ok("realism.personas_from_card", all(p in card["world"]["people"] for p in people))
    alleg = {}
    for x in rows:
        alleg[x["allegation"]] = alleg.get(x["allegation"], 0) + 1
    ok("realism.allegations_spread", max(alleg.values()) / len(rows) < 0.25, "top share %.2f" % (
        max(alleg.values()) / len(rows)))
    ok("realism.contribution_not_from_a_round_estimate", abs(g - rb) > 1000, fmt(g))
    month_tot = [round(sum(bb["gold"][(e, mo)] for e in K.ENTITY_ORDER), 1) for mo in A.ASK_B_MONTHS]
    ok("realism.askB_months_differ", len(set(month_tot)) == 3, str(month_tot))
    ok("realism.askA_reserves_distinct", len({r1000(aa[e]["reserves"]) for e in K.ENTITY_ORDER if aa[e]["count"]}) ==
       sum(1 for e in K.ENTITY_ORDER if aa[e]["count"]))
    with open(os.path.join(target, K.EXTRACT_LOG), encoding="utf-8") as fh:
        logged = {x["file_name"] for x in csv.DictReader(fh)}
    ok("H9.extract_log_lists_every_file", logged == set(files) - {K.EXTRACT_LOG}, str(sorted(set(files) ^ logged)))
    dic = open(os.path.join(target, K.DICTIONARY), encoding="utf-8").read()
    ok("H9.dictionary_names_its_extracts", all(f in dic for f in (K.REGISTER, K.PAYROLL, K.HCM, K.CROSSWALK,
                                                                  K.DIRECTORY, K.NOTICES, K.QM_SEP, K.QM_JUN, K.SC_SEP,
                                                                  K.SAFETY, K.INVOICES, K.PREMIUMS)))
    ok("H9.dictionary_narrates_no_device", not re.search(r"moonlight|additional job|former carrier|before .* moved|"
                                                         r"per.diem|carrier change", dic, re.I))
    vdate = K.VALUATION
    late = [x["claim_no"] for x in rows if x["claim_made_date"] > vdate or (x["closed_date"] and x["closed_date"] > vdate)]
    ok("H16.register_dates_by_valuation", not late, str(late[:3]))
    with open(os.path.join(target, K.NOTICES), encoding="utf-8") as fh:
        ok("H16.notices_by_valuation", max(x["sent_date"] for x in csv.DictReader(fh)) <= vdate.isoformat())
    with open(os.path.join(target, K.HCM), encoding="utf-8") as fh:
        ok("H16.hcm_by_september", max(x["work_month"] for x in csv.DictReader(fh)) == "2026-09")
    with open(os.path.join(target, K.SAFETY), encoding="utf-8") as fh:
        ok("H16.safety_by_valuation", max(x["event_date"] for x in csv.DictReader(fh)) <= vdate.isoformat())
    with open(os.path.join(target, K.INVOICES), encoding="utf-8") as fh:
        ok("H16.invoices_by_extract", max(x["received_date"] for x in csv.DictReader(fh)) <= "2026-10-02")
    with open(os.path.join(target, K.SC_SEP), encoding="utf-8") as fh:
        rpt = [dt.date(int(x["DATE_RPTD"][6:]), int(x["DATE_RPTD"][:2]), int(x["DATE_RPTD"][3:5]))
               for x in csv.DictReader(fh)]
    ok("H16.stoneleigh_reports_by_valuation", max(rpt) <= vdate)

    # the design note's world figures, recomputed here (H2)
    prof = []
    for lo_, hi_ in ((0, 30), (31, 90), (91, 182), (183, 364), (365, 10 ** 6)):
        cl = [c for c in ex if lo_ <= c["lag"] <= hi_]
        prof.append("%d-%s: %d Claims at %s" % (lo_, hi_ if hi_ < 10 ** 6 else "", len(cl),
                                                fmt(sum(c["cost"] for c in cl) / len(cl))))
    ok("record.experience_by_delay", True, "; ".join(prof))
    ok("record.routes", True, "; ".join("%s %s" % (k, fmt(v_)) for k, v_ in sorted(rts.items(), key=lambda kv: kv[1])))
    figs_json = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures.json")))
    ok("figures.contribution", figs_json["call"]["contribution"] == "{:,}".format(rb))

    n_ok = sum(1 for _, c, _ in RESULTS if c)
    print("checks: %d of %d passed" % (n_ok, len(RESULTS)))
    if n_ok != len(RESULTS):
        raise SystemExit("checks failed: " + ", ".join(n for n, c, _ in RESULTS if not c))
    return RESULTS
