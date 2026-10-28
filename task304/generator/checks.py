"""Assertions on the built pack (target/), the figures and the clean world. Every label prints PASS or the build
stops. The three-rules block (R1, R2, R3a to R3c) runs on every build."""
import copy
import datetime as dt
import os
import re
import subprocess
from collections import Counter, defaultdict

import pandas as pd

import params as P
import solve as S

N = [0]


def ok(label, cond, detail=""):
    N[0] += 1
    if not cond:
        raise AssertionError("FAIL %s %s" % (label, detail))
    print("PASS %-58s %s" % (label, detail))


def edge10(v):
    return 5.0 - abs(v - 10 * round(v / 10.0))


def winner(F, key):
    o = sorted(P.SETTINGS, key=lambda s: -F[s][key])
    return o[0], F[o[0]][key] / F[o[1]][key]


def pdf_text(path):
    return " ".join(subprocess.run(["pdftotext", path, "-"], capture_output=True, text=True).stdout.split())


def run(target, R, G):
    F, T = R["F"], R["T"]
    files = sorted(os.listdir(target))
    # ------------------------------------------------------------------ input gates
    ok("gate.files", len(files) >= 10, "%d files" % len(files))
    fmts = {f.rsplit(".", 1)[1] for f in files}
    ok("gate.formats", len(fmts) >= 3, str(sorted(fmts)))
    big = max(sum(1 for _ in open(os.path.join(target, f), encoding="utf-8")) for f in files if f.endswith(".csv"))
    ok("gate.big_file", big >= 25000, "%d rows" % big)
    ok("gate.distractors", len(P.DISTRACTORS) >= 2, str(P.DISTRACTORS))
    ok("gate.no_description_files", not any(re.search(r"readme|dictionar|notes|manifest|schema", f, re.I) for f in files))
    ok("gate.no_stump_in_names", not any(re.search(r"cure|prison_cure|distractor|trap", f, re.I) for f in files))
    # ------------------------------------------------------------------ documents read back with positive controls
    plan = pdf_text(os.path.join(target, P.FILES["plan"]))
    path = pdf_text(os.path.join(target, P.FILES["pathway"]))
    ev = pdf_text(os.path.join(target, P.FILES["evaluation"]))
    ok("doc.plan_control", "What we count" in plan and "two years to 30" in plan, "%d chars" % len(plan))
    ok("doc.pathway_control", "twelve weeks" in path and "last dose" in path, "%d chars" % len(path))
    ok("doc.evaluation_control", "Started within 12 weeks" in ev, "%d chars" % len(ev))
    allt = (plan + path + ev).lower()
    for w in ["stays positive", "antibody stays", "for life", "cured in prison", "cured inside", "persist",
              "already cured", "past infection", "ever infected"]:
        ok("doc.no_stump_vocab[%s]" % w, w not in allt)
    ok("doc.no_method_named", "per person" not in allt and "each person's record" not in allt)
    # ------------------------------------------------------------------ R1: the field's raw material ships
    lab = T["lab"]
    ok("R1.lab_is_raw_results", set(lab["test_code"]) <= {"HCVAB", "HCV-AB-EIA", "HCVPCR", "HCV-RNA-VL"},
       str(sorted(set(lab["test_code"]))))
    cols = " ".join(list(T["reg"].columns) + list(T["peer"].columns) + list(T["arr"].columns) + list(lab.columns))
    ok("R1.no_deciding_column", not re.search(r"active|viraemic|cured|status|eligible", cols, re.I), cols[:80])
    ok("R1.prison_sheets", set(pd.ExcelFile(os.path.join(target, P.FILES["prison"])).sheet_names) ==
       {"Courses 2017-20", "Courses 2021-26", "Reception BBV positives"})
    # ------------------------------------------------------------------ the ladder (R3a, R3b) and separation
    w0, m0 = winner(F, "starts_R0")
    w1, m1 = winner(F, "starts_R1")
    w2, m2 = winner(F, "starts_R2")
    w3, m3 = winner(F, "starts_R3")
    ok("ladder.R0_names_DS", w0 == "DS", "%.2fx" % m0)
    ok("ladder.R1_names_DS", w1 == "DS" and m1 >= 1.15, "%.2fx" % m1)
    ok("R3a.analyst_test_default_R2_files_AP", w2 == "AP" and m2 >= 1.15, "%.2fx" % m2)
    ok("R3b.decisive_step_alone_files_NSP", w3 == "NSP" and m3 >= 1.2, "%.2fx" % m3)
    ok("ladder.golden_4th_or_lower_on_R1", sorted(P.SETTINGS, key=lambda s: -F[s]["starts_R1"]).index("NSP") >= 2)
    ok("ladder.R2_and_R3_differ_every_setting",
       all(S.r10(F[s]["starts_R2"]) != S.r10(F[s]["starts"]) or s == "NSP" for s in P.SETTINGS),
       str({s: (S.r10(F[s]["starts_R2"]), S.r10(F[s]["starts"])) for s in P.SETTINGS}))
    # ------------------------------------------------------------------ standing family and bins
    for s in P.SETTINGS:
        for k in ("active", "starts"):
            v = F[s][k]
            alt = F[s][k + "_R3_pilot_ratio"] if k + "_R3_pilot_ratio" in F[s] else F[s]["starts_R3_pilot_ratio"]
            ok("bin.%s_%s_edge" % (s, k), edge10(v) >= 1.0, "%.2f edge %.2f" % (v, edge10(v)))
            ok("family.%s_%s_pilot_ratio_same_bin" % (s, k), S.r10(v) == S.r10(alt), "%.2f vs %.2f" % (v, alt))
    gap = F["NSP"]["starts"] - F["DS"]["starts"]
    ok("bin.gap_edge", edge10(gap) >= 1.0, "%.2f" % gap)
    ok("rates.lab_and_pilot_ratio_agree", abs(R["R"]["lab_ratio"] - R["R"]["pilot_ratio"]) < 0.02,
       "%.3f %.3f" % (R["R"]["lab_ratio"], R["R"]["pilot_ratio"]))
    # ------------------------------------------------------------------ the default's own validation passes
    H = S.histories(T)
    A, tests = S.pool(T)
    labf = S.lab_frame(T)
    rna = labf[labf["test"] == "RNA"]
    by = defaultdict(list)
    for p, d, res in zip(rna["pseudonym"], rna["sample_taken"], rna["result"]):
        by[p].append((d, res))
    for s in P.SETTINGS:
        pos = tests[(tests["setting"] == s) & tests["reactive"]]
        k = n = 0
        for p, d in zip(pos["pid"], pos["test_date"]):
            if any(st and st <= d + dt.timedelta(days=7) and (en is None or en >= d)
                   for st, en in H["net_span"].get(p, [])):
                continue          # on a network course at the test: its RNA tests are treatment monitoring
            after = sorted(x for x in by.get(p, []) if 0 < (x[0] - d).days <= 120)
            if after:
                n += 1
                k += after[0][1] == "Detected"
        ok("validation.%s_rna_after_peer_test_near_074" % s, n >= 15 and 0.62 <= k / n <= 1.0,
           "%d of %d = %.2f" % (k, n, k / max(n, 1)))
    # ------------------------------------------------------------------ SF rows (semantic forks), each same call
    F_alt = sf_variants(T, R)
    for name, Fv in F_alt.items():
        wv, mv = winner(Fv, "starts")
        ok("%s same call" % name, wv == "NSP", "%.2fx" % mv)
    for name in ("SF6_pilot_ratio", "SF12_completed_as_cure", "SF3_invalid_as_test", "SF1_distinct_over_two_years",
                 "SF2_mean_of_pilot_sites", "SF9_rounded_per_step", "SF10_completed_is_cure", "SF11_on_course_counted",
                 "SF16_reactive_share_per_person", "SF17_rna_after_the_kit", "SF18_setting_own_share",
                 "SF19_status_at_arrival", "SF21_lost_to_follow_up_no_cure"):
        same = all(S.r10(F_alt[name][s]["starts"]) == S.r10(F[s]["starts"]) for s in P.SETTINGS)
        ok("%s same figures" % name, same, str({s: round(F_alt[name][s]["starts"], 1) for s in P.SETTINGS}))
    ok("SF11 ruled out on the active figures by the plan",
       "counted neither among the active infections it finds nor among its starts" in plan)
    ok("SF2 ruled out by the plan", "test the same share of a setting's arrivals as the pilot tested" in plan)
    ok("SF8 ruled out by the plan", "where it starts the most people" in plan)
    stops_sf = ask_stops(T)
    AHs = R["AH"]
    d13 = sum(1 for kk in AHs if stops_sf["planned_end_for_stopped"][kk]["confirmed"] != AHs[kk]["confirmed"])
    ok("SF13 last dose of a stopped course, ruled out by the pathway",
       "the date it stopped for a course stopped early" in path and d13 >= 1, "%d cells move" % d13)
    ok("SF14 first test twelve weeks on against any such test: records converge", sf14_rows(T) == 0)
    d23 = sf23_cells(T, AHs)
    ok("SF23 completed courses only, ruled out by the pathway and the prompt's ended",
       "the date it stopped for a course stopped early" in path and "courses that ended in that half-year" in
       open(os.path.join(os.path.dirname(target), "prompt.txt")).read(), "%d cells move" % d23)
    nsp_reg = pd.read_csv(os.path.join(target, P.FILES["nsp_activity"]))
    nsp_reg["py"] = pd.to_datetime(nsp_reg["week_beginning"]).dt.date.map(S.plan_year)
    by_py = nsp_reg.groupby("py")["new_registrations_paper"].sum().to_dict()
    for lab_, alt_a in (("second_year", by_py.get(2, 0)), ("both_years", (by_py.get(1, 0) + by_py.get(2, 0)) / 2)):
        Fv = copy.deepcopy(F)
        Fv["NSP"]["starts"] = F["NSP"]["starts"] * alt_a / F["NSP"]["arrivals"]
        wv, mv = winner(Fv, "starts")
        ok("SF22 needle exchange arrivals from the pharmacies' paper registrations (%s) same call" % lab_, wv == "NSP",
           "%.1f arrivals, %.2fx" % (alt_a, mv))
    ok("SF22 ruled out by the plan", "from the returns each provider sends the commissioners" in plan)
    fib = pd.read_excel(os.path.join(target, P.FILES["fibroscan"]))
    ok("SF24 the FibroScan sessions rank venues by liver disease, not people started; ruled out by the plan",
       "where it starts the most people" in plan and not any("pseud" in str(col).lower() for col in fib.columns),
       str(list(fib.columns)))
    # realism: sibling requesting sites do not share the work evenly
    locs = T["lab"].groupby(["location_type", "requesting_location"]).size()
    for ltype in ("GP", "Antenatal", "Sexual health", "Drug service", "Hospital"):
        v = locs[ltype]
        ok("realism.sites_uneven[%s]" % ltype, v.max() / v.min() >= 1.5, "%d to %d" % (v.min(), v.max()))
    d20 = sf20_cells(T, AHs)
    ok("SF20 a course lost to follow-up read as finished at its planned end, ruled out by the pathway",
       "A course lost to follow-up has no last dose on record" in path, "%d cells move" % d20)
    d15 = sf15_cells(T, AHs)
    ok("SF15 half-year by the last dose, the start ruled out by the prompt",
       "ended in that half-year" in open(os.path.join(os.path.dirname(target), "prompt.txt")).read() and d15 >= 1,
       "%d cells move" % d15)
    # ------------------------------------------------------------------ R2: Layer 1 items neutral
    for name, Fv in mess_variants(T, R).items():
        wv, mv = winner(Fv, "starts")
        ok("R2.mess_%s_call_unchanged" % name, wv == "NSP", "%.2fx" % mv)
        same = all(S.r10(Fv[s][k]) == S.r10(F[s][k]) for s in P.SETTINGS for k in ("starts", "active"))
        ok("R2.mess_%s_figures_unchanged" % name, same,
           str({s: (round(Fv[s]["starts"], 1), round(Fv[s]["active"], 1)) for s in P.SETTINGS}))
    # ------------------------------------------------------------------ R3c no plant; realism sweep
    arr = T["arr"]
    ok("R3c.no_repeated_blocks", arr.duplicated(["pseudonym", "arrival_date", "setting"]).sum() == 0)
    counts = Counter(arr["setting"])
    ok("realism.unequal_setting_counts", len(set(counts.values())) == 4, str(counts))
    for col, df in (("lab_number", lab), ("course_ref", T["reg"]), ("test_id", T["peer"])):
        ids = sorted(df[col].unique())
        nums = [int(re.sub(r"\D", "", x)[-4:]) for x in ids[:200]]
        steps = {b - a for a, b in zip(nums, nums[1:])}
        ok("realism.%s_not_arithmetic" % col, len(steps) > 3, "%d distinct steps" % len(steps))
    ok("realism.persona_names", P.DIRECTOR in plan and P.CLIN_LEAD in path and P.TEAM_LEAD in ev)
    # ------------------------------------------------------------------ H16: no record dated past its extract
    for label, (lo, hi), limit in h16_ranges(target, T):
        ok("H16.%s_on_or_before_%s" % (label, limit), hi is None or hi <= limit, "%s to %s" % (lo, hi))
    ok("H16.evaluation_after_every_12_week_window",
       max(S._date(x) for x in T["pilot"]["test_date"] if x) + dt.timedelta(days=84) <= dt.date(2020, 1, 17)
       and "17 January 2020" in ev)
    ok("H21.no_near_real_place_names", not re.search(r"tamberley|haverleigh", (plan + path + ev).lower()) and
       not any(re.search(r"Tamberley|Haverleigh", open(os.path.join(target, f), encoding="utf-8").read())
               for f in files if f.endswith(".csv")))
    # ------------------------------------------------------------------ the ask: separation and stops
    AH = R["AH"]
    sep = ask_separation(T, R)
    ok("ask.device_rows_outside_call", sep == 0, "%d device rows read by the call" % sep)
    stops = ask_stops(T)
    need = {"register_only": 10, "pseudonym_only": 10, "no_twelve_week_rule": 5, "planned_end_for_stopped": 2}
    for name, st in stops.items():
        diff = sum(1 for kk in AH if st[kk]["confirmed"] != AH[kk]["confirmed"])
        ok("ask.stop_%s_misses" % name, diff >= need[name], "%d of 10 cells differ" % diff)
    ok("ask.each_clinic_has_courses", all(AH[(c, h)]["finished"] >= 4 for c in P.CLINICS for h in (1, 2)))
    ok("ask.device_unnamed_in_register", not any(re.search(r"previous|merged|alias|former|old_", col, re.I)
                                                 for col in T["reg"].columns), str(list(T["reg"].columns)))
    AL = S.aliases(T)
    reg_ids = set(T["reg"]["pseudonym"])
    lab_ids = set(T["lab"]["pseudonym"])
    two = {tuple(v) for v in AL.values() if len(v) > 1}
    in_ask, outside = 0, 0
    for v in two:
        courses = T["reg"][T["reg"]["pseudonym"].isin(v)]
        ends = [S._date(r["stopped_on"]) if r["outcome"] == "Stopped" else S._date(r["planned_end"])
                for _, r in courses.iterrows()]
        if any(e and P.POOL_START <= e <= dt.date(2025, 9, 30) for e in ends):
            in_ask += 1
        else:
            outside += 1
    ok("ask.device_reachable_every_course_person_has_a_lab_row", all(
        any(p in lab_ids for p in v if p in reg_ids) for v in two), "%d two-number people" % len(two))
    ok("ask.device_blended_two_number_people_outside_the_ask", outside >= in_ask,
       "%d in the ask's courses, %d outside" % (in_ask, outside))
    arr_people = set(T["arr"]["pseudonym"])
    ok("ask.no_two_number_arrival", not any(p in arr_people for v in two for p in v))
    # ------------------------------------------------------------------ capacity is not binding
    ok("plan.capacity_not_binding", all(R["C"][s]["running"] < 70 for s in P.SETTINGS),
       str({s: round(R["C"][s]["running"], 1) for s in P.SETTINGS}))
    # ------------------------------------------------------------------ figures.json carries every graded figure
    ok("figures.call", G["order"][0] == "NSP" and G["starts10"]["NSP"] == S.r10(F["NSP"]["starts"]))
    # the approved premises' share cured inside prison, per test and per person, before the test or the arrival
    A_, tests_ = S.pool(T)
    pos_ = tests_[(tests_["setting"] == "AP") & tests_["reactive"]]
    for unit, q in (("test", pos_), ("person", pos_.sort_values("test_date").drop_duplicates("pid"))):
        n_ = len(q)
        po = sum(1 for p_, d_ in zip(q["pid"], q["test_date"])
                 if any(x and x < d_ for x in H["pr_cure"].get(p_, []))
                 and not any(x and x < d_ for x in H["net_cure"].get(p_, [])))
        pct = 100.0 * po / n_
        ok("component.ap_prison_pct_per_%s" % unit, int(round(pct)) == G["ap_prison_pct"] and abs(pct - round(pct)) < 0.45,
           "%.2f" % pct)
    # the write-up states it as more than half: true under every match window a solver would use, per test or person
    for w_ in (30, 42, 60, 90):
        A_w, t_w = S.pool(T, window=w_)
        pos_w = t_w[(t_w["setting"] == "AP") & t_w["reactive"]]
        for unit, q in (("test", pos_w), ("person", pos_w.sort_values("test_date").drop_duplicates("pid"))):
            k_ = sum(1 for p_, d_ in zip(q["pid"], q["test_date"])
                     if any(x and x < d_ for x in H["pr_cure"].get(p_, []))
                     and not any(x and x < d_ for x in H["net_cure"].get(p_, [])))
            ok("component.ap_more_than_half_window_%d_per_%s" % (w_, unit), k_ / len(q) > 0.5,
               "%d of %d" % (k_, len(q)))
    # the paper's comparative words hold on the pack: a quarter of the approved premises' tested arrivals react, the
    # largest intake is Fenwold Recovery's, nearly half of its positives were cured by the network's clinics, most of
    # the needle exchange registrants' positives are active
    ok("words.ap_a_quarter_react", 0.22 <= F["AP"]["ab_share"] <= 0.28, "%.3f" % F["AP"]["ab_share"])
    ok("words.ds_largest_intake", max(P.SETTINGS, key=lambda s: F[s]["arrivals"]) == "DS")
    cs = S.cured_shares(T)
    ok("words.ds_nearly_half_cured_by_network", 0.40 <= cs["DS"]["net"] / cs["DS"]["n"] < 0.5,
       "%.3f" % (cs["DS"]["net"] / cs["DS"]["n"]))
    ok("words.nsp_most_positives_active", F["NSP"]["active"] / F["NSP"]["positives"] > 0.5,
       "%.3f" % (F["NSP"]["active"] / F["NSP"]["positives"]))
    print("checks: %d assertions passed" % N[0])


def _with(T, **kw):
    T2 = dict(T)
    T2.pop("_labf", None)
    T2.update(kw)
    return T2


def sf_variants(T, R):
    """each row of the design note's semantic fork table, the golden's construction under the alternative reading"""
    import solve as S2
    out = {}
    base_R = R["R"]
    # SF1 a 2027 year's arrivals read as arrival rows (second stays counted) instead of distinct people
    T1 = _with(T)
    ar = T["arr"].copy()
    ar["pseudonym"] = ar["pseudonym"] + "_" + ar.index.astype(str)
    T1["arr"] = ar
    A1, _ = S2.pool(T1)
    F1 = copy.deepcopy(R["F"])
    for s in P.SETTINGS:
        F1[s]["starts"] = R["F"][s]["starts"] * A1[s] / R["F"][s]["arrivals"]
    out["SF1_arrival_rows"] = F1
    # SF3 an invalid kit read as a non-reactive test
    T3 = _with(T)
    pe = T["peer"].copy()
    pe.loc[pe["result"] == "Invalid", "result"] = "Non-reactive"
    T3["peer"] = pe
    out["SF3_invalid_as_test"] = S2.funnel(T3, base_R)[0]
    # SF4 the status read at 30 September 2026 instead of at the test
    H = S2.histories(T)
    A, tests = S2.pool(T)
    F4 = copy.deepcopy(R["F"])
    for s in P.SETTINGS:
        pos = tests[(tests["setting"] == s) & tests["reactive"]]
        v = sum(S2.status(p, P.AS_OF, H, base_R["lab_ratio"]) for p in pos["pid"]) / len(pos)
        F4[s]["starts"] = R["F"][s]["positives"] * v * base_R["start_share"]
    out["SF4_status_at_as_of"] = F4
    # SF5 started at any time, not within twelve weeks
    pl = T["pilot"]
    det = pl[pl["rna"] == "Detected"]
    any_share = (det["treatment_started"] == "Y").sum() / len(det)
    out["SF5_any_start"] = {s: dict(R["F"][s], starts=R["F"][s]["starts"] / base_R["start_share"] * any_share)
                            for s in P.SETTINGS}
    # SF6 the pilot's viraemic share for positives with no record
    out["SF6_pilot_ratio"] = {s: dict(R["F"][s], starts=R["F"][s]["starts_R3_pilot_ratio"]) for s in P.SETTINGS}
    # SF7 a peer test matched to an arrival within 42 days, not 60
    old = S2.pool
    try:
        S2.pool = lambda Tx, window=42: old(Tx, window=42)
        out["SF7_window_42_days"] = S2.funnel(T, base_R)[0]
    finally:
        S2.pool = old
    # SF1b distinct people over the two years, halved, instead of each year's distinct people averaged
    arr = T["arr"].copy()
    arr["d"] = arr["arrival_date"].map(S2._date)
    arr["py"] = arr["d"].map(S2.plan_year)
    F1b = copy.deepcopy(R["F"])
    for s in P.SETTINGS:
        a = arr[(arr["setting"] == s) & arr["py"].notna()]
        F1b[s]["starts"] = R["F"][s]["starts"] * (a["pseudonym"].nunique() / 2) / R["F"][s]["arrivals"]
    out["SF1_distinct_over_two_years"] = F1b
    # SF2 the van's test share read as the peer team's coverage of each setting, or the mean of the pilot's sites
    A, tests = S2.pool(T)
    F2 = copy.deepcopy(R["F"])
    for s in P.SETTINGS:
        ppl = set(arr[(arr["setting"] == s) & arr["py"].notna()]["pseudonym"])
        cov = len(set(tests[tests["setting"] == s]["pid"]) & ppl) / len(ppl)
        F2[s]["starts"] = R["F"][s]["starts"] / base_R["test_share"] * cov
    out["SF2_peer_coverage"] = F2
    pl = T["pilot"]
    sites = sorted(set(pl["pilot_site"]))
    ts = sum(((pl["pilot_site"] == x) & (pl["tested_by_van"] == "Y")).sum() / (pl["pilot_site"] == x).sum()
             for x in sites) / len(sites)
    out["SF2_mean_of_pilot_sites"] = {s: dict(R["F"][s], starts=R["F"][s]["starts"] / base_R["test_share"] * ts)
                                      for s in P.SETTINGS}
    # SF8 the setting with the most active infections instead of the most starts
    out["SF8_most_active"] = {s: dict(R["F"][s], starts=R["F"][s]["active"]) for s in P.SETTINGS}
    # SF9 every rate rounded to two places and every count to whole people at each step
    F9 = {}
    for s in P.SETTINGS:
        f = R["F"][s]
        tested = round(round(f["arrivals"]) * round(base_R["test_share"], 2))
        pos = round(tested * round(f["ab_share"], 2))
        act = round(pos * round(f["active"] / f["positives"], 2))
        F9[s] = dict(f, starts=act * round(base_R["start_share"], 2))
    out["SF9_rounded_per_step"] = F9
    # SF10 a cure read as a course completed, whatever its twelve-week result
    T10 = _with(T)
    rg = T["reg"].copy()
    m = rg["outcome"] == "Completed"
    rg.loc[m & (rg["svr12_date"] == ""), "svr12_date"] = rg.loc[m & (rg["svr12_date"] == ""), "planned_end"]
    rg.loc[m, "svr12_result"] = "Not detected"
    T10["reg"] = rg
    pr = T["prison"].copy()
    mp = pr["released"] == False
    pr.loc[mp & (pr["svr_date"] == ""), "svr_date"] = pr.loc[mp & (pr["svr_date"] == ""), "end"]
    pr.loc[mp, "svr"] = "Not detected"
    T10["prison"] = pr
    out["SF10_completed_is_cure"] = S2.funnel(T10, base_R)[0]
    # SF11 a person on a course at the test counted at the viraemic share
    H = S2.histories(T)
    F11 = copy.deepcopy(R["F"])
    for s in P.SETTINGS:
        pos = tests[(tests["setting"] == s) & tests["reactive"]]
        vals = []
        for p, d in zip(pos["pid"], pos["test_date"]):
            on = any(a is not None and a <= d and (b is None or b >= d)
                     for a, b in H["net_span"].get(p, []) + H["pr_span"].get(p, []))
            vals.append(base_R["lab_ratio"] if on else S2.status(p, d, H, base_R["lab_ratio"]))
        F11[s]["starts"] = R["F"][s]["positives"] * sum(vals) / len(vals) * base_R["start_share"]
    out["SF11_on_course_counted"] = F11
    # SF16 the reactive share per person (first test) instead of per test
    F16 = copy.deepcopy(R["F"])
    for s in P.SETTINGS:
        t = tests[tests["setting"] == s].sort_values("test_date").drop_duplicates("pid")
        pos = t[t["reactive"]]
        v = sum(S2.status(p, d, H, base_R["lab_ratio"]) for p, d in zip(pos["pid"], pos["test_date"])) / len(pos)
        F16[s]["starts"] = R["F"][s]["arrivals"] * base_R["test_share"] * len(pos) / len(t) * v * base_R["start_share"]
    out["SF16_reactive_share_per_person"] = F16
    # SF17 a positive with no earlier record read from an RNA test in the 120 days after the kit, where there is one
    labf = S2.lab_frame(T)
    rna = defaultdict(list)
    for p, d, res in zip(labf["pseudonym"], labf["sample_taken"], labf["result"]):
        if res in ("Detected", "Not detected"):
            rna[p].append((d, res))
    F17, F18 = copy.deepcopy(R["F"]), copy.deepcopy(R["F"])
    for s in P.SETTINGS:
        pos = tests[(tests["setting"] == s) & tests["reactive"]]
        vals, k, n, none = [], 0, 0, []
        for p, d in zip(pos["pid"], pos["test_date"]):
            x = S2.status(p, d, H, -1.0)
            if x == -1.0:
                after = sorted(y for y in rna.get(p, []) if 0 <= (y[0] - d).days <= 120)
                if after:
                    n += 1
                    k += after[0][1] == "Detected"
                    x = 1.0 if after[0][1] == "Detected" else 0.0
                else:
                    x = base_R["lab_ratio"]
            vals.append(x)
            none.append((p, d))
        F17[s]["starts"] = R["F"][s]["positives"] * sum(vals) / len(vals) * base_R["start_share"]
        # SF18 each setting's own share among its positives with no earlier record and an RNA test after the kit
        vs = [S2.status(p, d, H, k / n) for p, d in none]
        F18[s]["starts"] = R["F"][s]["positives"] * sum(vs) / len(vs) * base_R["start_share"]
    out["SF17_rna_after_the_kit"] = F17
    out["SF18_setting_own_share"] = F18
    # SF19 the status read at the arrival rather than at the peer team's test
    arr_by = defaultdict(list)
    for p, s, d, py in zip(arr["pseudonym"], arr["setting"], arr["d"], arr["py"]):
        if py:
            arr_by[p].append(d)
    F19 = copy.deepcopy(R["F"])
    for s in P.SETTINGS:
        pos = tests[(tests["setting"] == s) & tests["reactive"]]
        vals = [S2.status(p, max(x for x in arr_by[p] if 0 <= (d - x).days <= 60), H, base_R["lab_ratio"])
                for p, d in zip(pos["pid"], pos["test_date"])]
        F19[s]["starts"] = R["F"][s]["positives"] * sum(vals) / len(vals) * base_R["start_share"]
    out["SF19_status_at_arrival"] = F19
    # SF21 a course lost to follow-up has no last dose on record, so its keyed twelve-week result is not read as a cure
    T21 = _with(T)
    rg21 = T["reg"].copy()
    m21 = rg21["outcome"] == "Lost to follow-up"
    rg21.loc[m21, "svr12_result"] = ""
    rg21.loc[m21, "svr12_date"] = ""
    T21["reg"] = rg21
    out["SF21_lost_to_follow_up_no_cure"] = S2.funnel(T21, base_R)[0]
    # SF12 a course completed without a twelve-week result counted as a cure
    T12 = _with(T)
    rg = T["reg"].copy()
    m = (rg["outcome"] == "Completed") & (rg["svr12_result"].isin(["", "Not done"]))
    rg.loc[m, "svr12_result"] = "Not detected"
    rg.loc[m, "svr12_date"] = rg.loc[m, "planned_end"]
    T12["reg"] = rg
    out["SF12_completed_as_cure"] = S2.funnel(T12, base_R)[0]
    return out


def mess_variants(T, R):
    out = {}
    # the re-sent laboratory rows kept
    T2 = _with(T)
    T2["lab"] = pd.concat([T["lab"], T["lab"].iloc[:5000]], ignore_index=True)
    out["lab_resent_rows_kept"] = S.funnel(T2, R["R"])[0]
    # invalid kit results counted as non-reactive tests
    T3 = _with(T)
    pe = T["peer"].copy()
    pe.loc[pe["result"] == "Invalid", "result"] = "Non-reactive"
    T3["peer"] = pe
    out["invalid_kits_counted"] = S.funnel(T3, R["R"])[0]
    # the hostels' day-first dates read month-first where possible
    T4 = _with(T)
    ar = T["arr"].copy()

    def swap(s):
        if "/" in s:
            d, m, y = s.split("/")
            if int(d) <= 12:
                return "%s/%s/%s" % (m, d, y)
        return s
    ar["arrival_date"] = ar["arrival_date"].map(swap)
    T4["arr"] = ar
    out["hostel_dates_month_first"] = S.funnel(T4, R["R"])[0]
    # the older workbook sheet's day-first text dates read month-first where possible
    T5 = _with(T)
    pr = T["prison"].copy()
    old_rows = pr.index[pr["start"].str.contains("/", na=False)]
    for col in ("start", "end", "svr_date"):
        pr.loc[old_rows, col] = pr.loc[old_rows, col].map(swap)
    T5["prison"] = pr
    out["workbook_old_sheet_dates_month_first"] = S.funnel(T5, R["R"])[0]
    return out


def ask_separation(T, R):
    """register rows carrying an ask device (a blank twelve-week result since the go-live, a previous pseudonym)
    whose person is an antibody-positive arrival with the device row dated before their test"""
    A, tests = S.pool(T)
    pos = tests[tests["reactive"]]
    first_test = {}
    for p, d in zip(pos["pid"], pos["test_date"]):
        first_test[p] = min(d, first_test.get(p, d))
    labf = S.lab_frame(T)
    AL = S.aliases(T)
    rna = defaultdict(list)
    for p, d, res in zip(labf["pseudonym"], labf["sample_taken"], labf["result"]):
        if res in ("Detected", "Not detected"):
            rna[p].append(d)
    n = 0
    for _, r in T["reg"].iterrows():
        last = S._date(r["stopped_on"]) if r["outcome"] == "Stopped" else S._date(r["planned_end"])
        unkeyed = (r["svr12_result"] == "" and r["outcome"] in ("Completed", "Stopped")
                   and any((d - last).days >= 84 for d in rna.get(r["pseudonym"], [])))
        ids = AL.get(r["pseudonym"], [r["pseudonym"]])
        dev = len(ids) > 1 or unkeyed
        if not dev:
            continue
        for pid in ids:
            if pid in first_test and S._date(r["start_date"]) < first_test[pid]:
                n += 1
    return n


def ask_stops(T):
    """the ask's wrong stops: the register's keyed result only; the laboratory by pseudonym only; any negative RNA
    after the last dose; the planned end for a course stopped early"""
    labf = S.lab_frame(T)
    AL = S.aliases(T)
    rna = defaultdict(list)
    for p, d, res in zip(labf["pseudonym"], labf["sample_taken"], labf["result"]):
        if res in ("Detected", "Not detected"):
            rna[p].append((d, res))
    stops = {}
    for name in ("register_only", "pseudonym_only", "no_twelve_week_rule", "planned_end_for_stopped"):
        out = {(c, h): dict(finished=0, confirmed=0) for c in P.CLINICS for h in (1, 2)}
        for _, r in T["reg"].iterrows():
            if r["outcome"] == "Stopped":
                last = S._date(r["planned_end"]) if name == "planned_end_for_stopped" else S._date(r["stopped_on"])
            elif r["outcome"] == "Completed":
                last = S._date(r["planned_end"])
            else:
                continue
            if not (P.POOL_START <= last <= dt.date(2025, 9, 30)):
                continue
            h = 1 if last <= dt.date(2025, 3, 31) else 2
            out[(r["clinic_code"], h)]["finished"] += 1
            if name == "register_only":
                okc = r["svr12_result"] == "Not detected"
            else:
                ids = [r["pseudonym"]] if name == "pseudonym_only" else AL.get(r["pseudonym"], [r["pseudonym"]])
                lim = 0 if name == "no_twelve_week_rule" else 84
                after = sorted(x for i in ids for x in rna.get(i, []) if (x[0] - last).days >= lim)
                okc = bool(after) and after[0][1] == "Not detected"
                if r["svr12_result"] == "Not detected":
                    okc = True
            out[(r["clinic_code"], h)]["confirmed"] += int(okc)
        stops[name] = out
    return stops


def _rna_by(T):
    labf = S.lab_frame(T)
    rna = defaultdict(list)
    for p, d, res in zip(labf["pseudonym"], labf["sample_taken"], labf["result"]):
        if res in ("Detected", "Not detected"):
            rna[p].append((d, res))
    return rna


def _finished(r):
    if r["outcome"] == "Stopped":
        return S._date(r["stopped_on"])
    if r["outcome"] == "Completed":
        return S._date(r["planned_end"])
    return None


def sf14_rows(T):
    """courses in the ask whose first RNA test twelve weeks or more after the last dose and any such test disagree"""
    rna = _rna_by(T)
    n = 0
    for _, r in T["reg"].iterrows():
        last = _finished(r)
        if last is None or not (P.POOL_START <= last <= dt.date(2025, 9, 30)):
            continue
        ids = S.aliases(T).get(r["pseudonym"], [r["pseudonym"]])
        after = sorted(x for i in ids for x in rna.get(i, []) if (x[0] - last).days >= 84 and x[0] <= P.AS_OF)
        first = bool(after) and after[0][1] == "Not detected"
        anyn = any(x[1] == "Not detected" for x in after)
        n += int(first != anyn)
    return n


def sf15_cells(T, AH):
    """cells that move when the courses are put in half-years by their start instead of their last dose"""
    rna = _rna_by(T)
    out = {(c, h): 0 for c in P.CLINICS for h in (1, 2)}
    for _, r in T["reg"].iterrows():
        last = _finished(r)
        st = S._date(r["start_date"])
        if last is None or not (P.POOL_START <= st <= dt.date(2025, 9, 30)):
            continue
        h = 1 if st <= dt.date(2025, 3, 31) else 2
        ids = S.aliases(T).get(r["pseudonym"], [r["pseudonym"]])
        after = sorted(x for i in ids for x in rna.get(i, []) if (x[0] - last).days >= 84 and x[0] <= P.AS_OF)
        c = bool(after) and after[0][1] == "Not detected"
        if r["svr12_result"] == "Not detected":
            c = True
        out[(r["clinic_code"], h)] += int(c)
    return sum(1 for kk in AH if out[kk] != AH[kk]["confirmed"])


def h16_ranges(target, T):
    """each extract column's date range against the date that extract is taken to; forward-looking columns (a
    course's planned end) are on the allow-list and not checked"""
    def rng_of(vals):
        ds = [S._date(v) for v in vals if v not in ("", None) and not (isinstance(v, float) and pd.isna(v))]
        return (min(ds), max(ds)) if ds else (None, None)
    out = []
    lab = T["lab"]
    out.append(("lab.sample_taken", rng_of(lab["sample_taken"]), P.AS_OF))
    for c in ("received", "authorised"):
        out.append(("lab.%s" % c, rng_of(lab[c].str[:10]), P.EXPORT_DATE))
    reg = T["reg"]
    for c in ("start_date", "stopped_on", "svr12_date"):
        out.append(("register.%s" % c, rng_of(reg[c]), P.AS_OF))
    pr = T["prison"]
    for c in ("start", "release", "svr_date"):
        out.append(("prison.%s" % c, rng_of(pr[c]), P.AS_OF))
    out.append(("prison.reception", rng_of(T["reception"]["d"]), P.AS_OF))
    out.append(("peer.test_date", rng_of(T["peer"]["test_date"]), P.AS_OF))
    out.append(("arrivals.arrival_date", rng_of(T["arr"]["arrival_date"]), P.AS_OF))
    out.append(("pilot.test_date", rng_of(T["pilot"]["test_date"]), P.PILOT_END))
    return out


def sf20_cells(T, AH):
    """cells that move when a course lost to follow-up is read as finished on its planned end"""
    rna = _rna_by(T)
    out = {kk: AH[kk]["confirmed"] for kk in AH}
    for _, r in T["reg"].iterrows():
        if r["outcome"] != "Lost to follow-up":
            continue
        last = S._date(r["planned_end"])
        if not (P.POOL_START <= last <= dt.date(2025, 9, 30)):
            continue
        h = 1 if last <= dt.date(2025, 3, 31) else 2
        ids = S.aliases(T).get(r["pseudonym"], [r["pseudonym"]])
        after = sorted(x for i in ids for x in rna.get(i, []) if (x[0] - last).days >= 84 and x[0] <= P.AS_OF)
        c = (bool(after) and after[0][1] == "Not detected") or r["svr12_result"] == "Not detected"
        out[(r["clinic_code"], h)] += int(c)
    return sum(1 for kk in AH if out[kk] != AH[kk]["confirmed"])


def sf23_cells(T, AH):
    """cells that move when only courses completed are counted, the stopped ones left out"""
    rna = _rna_by(T)
    out = {kk: 0 for kk in AH}
    for _, r in T["reg"].iterrows():
        if r["outcome"] != "Completed":
            continue
        last = S._date(r["planned_end"])
        if not (P.POOL_START <= last <= dt.date(2025, 9, 30)):
            continue
        h = 1 if last <= dt.date(2025, 3, 31) else 2
        ids = S.aliases(T).get(r["pseudonym"], [r["pseudonym"]])
        after = sorted(x for i in ids for x in rna.get(i, []) if (x[0] - last).days >= 84 and x[0] <= P.AS_OF)
        c = bool(after) and after[0][1] == "Not detected"
        if (r["svr12_result"] == "Not detected" and S._date(r["svr12_date"])
                and (S._date(r["svr12_date"]) - last).days >= 84):
            c = True
        out[(r["clinic_code"], h)] += int(c)
    return sum(1 for kk in AH if out[kk] != AH[kk]["confirmed"])
