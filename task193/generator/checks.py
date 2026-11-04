"""The generator's assertions, run on every build: the three-rules block (R1 to R3c), the semantic forks (SF1 to SF16),
the ladder and its margins, the bins, the separation of the asks from the call, the input gates, the realism sweep
and the leak words. Each assertion is named for what it measures."""
import copy
import csv
import datetime as dt
import json
import math
import os
import re
import zipfile

import numpy as np

import golden as GD
import pack as PK
import routes as RT
import world as W

EV = [e["label"] for e in W.EVENTS]
N = [0]


def ok(name, cond, detail=""):
    if not cond:
        raise AssertionError("%s: %s" % (name, detail))
    N[0] += 1


def edge(v, unit):
    c = round(v / unit) * unit
    return unit / 2 - abs(v - c)


def s3_unit(v):
    return 10 ** (math.floor(math.log10(abs(v))) - 2)


def limits_from(bg, rev):
    lim, cnt = RT.background_limits(bg, rev, EV, W.DRY)
    return lim, cnt


def run(tgt, S, g, info, figs):
    N[0] = 0
    G = g["golden"]
    oc = g["october"]
    lim = g["limits"]

    # ------------------------------------------------ the golden reproduces the clean truth
    for k in W.INDICATORS:
        ok("golden.limit_equals_truth.%s" % k, abs(G[k] - S["limits"][RT.GOLDEN][k]) < 1e-9, (G[k], S["limits"][RT.GOLDEN][k]))
    ok("golden.reversal_classification_equals_truth", all(g["rev"][(w, e)] == S["rev"][(w, e)]
                                                           for w in W.BACKGROUND for e in range(len(EV))))
    ok("golden.call", g["resample"] == ["MW-6", "MW-7", "MW-9"], g["resample"])

    # ------------------------------------------------ R1: the field's raw material ships, the decisive quantity does not
    gh = open(os.path.join(tgt, PK.FILES["gauging"]), encoding="utf-8").readline()
    ok("R1.gauging_ships_depths_not_heads", "dtw_ft_btoc" in gh and "head" not in gh.lower() and "elev" not in gh.lower(), gh)
    heads_ = [l for fn in os.listdir(tgt) if fn.endswith((".csv", ".txt"))
              for l in [open(os.path.join(tgt, fn), encoding="utf-8").readline().lower()]]
    ok("R1.no_column_states_the_gradient", not any(w in h for h in heads_ for w in ("gradient", "upgradient", "reversed",
                                                                                 "flow_dir", "affected")), heads_)
    ok("R1.background_results_are_individual_samples", g["counts"]["R0 every background result"]["chloride"] == 50)
    ok("R1.decisive_step_reads_heads_and_survey", len(g["heads"]) == info["gauging_rows"])

    # ------------------------------------------------ R3a: the analyst test, the easy route on the clean truth
    bg_truth = S["bgwin"]
    lim_t, _ = limits_from(bg_truth, S["rev"])
    oc_t = {(w, k): S["cmp"][(w, W.EVAL, k)] for w in W.COMPLIANCE for k in W.INDICATORS}
    ok("R3a.easy_route_clean_truth_files_MW6_alone", RT.designate(lim_t["R0 every background result"], oc_t) == ["MW-6"])
    ok("R3a.easy_route_on_pack_files_MW6_alone", g["sets"]["R0 every background result"] == ["MW-6"])
    # R3b: the decisive step alone, and each lower correction alone
    ok("R3b.decisive_step_alone_files_golden", RT.designate(lim_t[RT.GOLDEN], oc_t) == ["MW-6", "MW-7", "MW-9"])
    for r in RT.CHEAP_HIGH:
        ok("R3b.lower_correction_alone_wrong.%s" % r.split()[0], g["sets"][r] != g["resample"], (r, g["sets"][r]))
    ok("R3b.intrawell_wrong", g["sets"]["R2f intrawell, each well against its own record"] != g["resample"])
    for r in RT.CHEAP_LOW:
        ok("R3b.over_cut_wrong.%s" % r.split()[0], g["sets"][r] != g["resample"] and set(g["resample"]) < set(g["sets"][r]))
    # R3c: no plant: no copied block, no decoy text
    for w in W.BACKGROUND + W.COMPLIANCE:
        vals = [tuple(g["indicators"].get((w, e, k)) for k in W.INDICATORS) for e in range(len(EV))]
        vals = [v for v in vals if None not in v]
        ok("R3c.no_repeated_result_triplet.%s" % w, len(vals) == len(set(vals)))

    # ------------------------------------------------ the licensed family converges on the set
    for r in RT.LICENSED + RT.VARIANTS:
        ok("family.converges_on_set.%s" % r.split()[0], g["sets"][r] == g["resample"], (r, g["sets"][r]))
    for r in [x for x in g["sets"] if x.startswith("R3t")]:
        ok("family.tolerance_variant_converges_on_set.%s" % r[-12:].replace(" ", "_"), g["sets"][r] == g["resample"],
           (r, g["sets"][r]))
    for k in W.INDICATORS:
        ok("family.rosner_after_heads_removes_nothing.%s" % k, g["counts"]["R3r heads then Rosner"][k] == g["golden_n"][k])

    # ------------------------------------------------ margins on every check of the scorecard
    high = {k: min(lim[r][k] for r in RT.CHEAP_HIGH) for k in W.INDICATORS}
    var_hi = {k: max(lim[r][k] for r in RT.LICENSED + RT.VARIANTS) for k in W.INDICATORS}
    var_lo = {k: min(lim[r][k] for r in RT.LICENSED + RT.VARIANTS) for k in W.INDICATORS}
    for w in W.COMPLIANCE:
        for k in W.INDICATORS:
            v = oc[(w, k)]
            if g["exceed"][(w, k)]:
                ok("margin.over_golden_by_5pct.%s.%s" % (w, k), v > 1.05 * G[k], (v, G[k]))
                ok("margin.over_every_family_member.%s.%s" % (w, k), v > 1.02 * var_hi[k], (v, var_hi[k]))
                if w != "MW-6":
                    ok("margin.under_every_high_route_by_5pct.%s.%s" % (w, k), v < 0.95 * high[k], (v, high[k]))
            else:
                ok("margin.under_golden_by_5pct.%s.%s" % (w, k), v < 0.95 * G[k], (v, G[k]))
                ok("margin.under_every_family_member.%s.%s" % (w, k), v < 0.98 * var_lo[k], (v, var_lo[k]))
    for w in ("MW-7", "MW-9"):
        ok("margin.plume_well_under_high_routes_on_every_indicator.%s" % w,
           all(oc[(w, k)] < 0.95 * high[k] for k in W.INDICATORS))

    # ------------------------------------------------ bins: limits at three significant figures, asks at their units
    for k in W.INDICATORS:
        u = s3_unit(G[k])
        ok("bin.limit_mid_cell.%s" % k, edge(G[k], u) >= 0.20 * u, (G[k], edge(G[k], u)))
    for w, v in g["spc"].items():
        ok("bin.spc_mid_cell.%s" % w, edge(v, 1.0) >= 0.10, (w, v))
    for w, v in g["purge"].items():
        ok("bin.purge_mid_cell.%s" % w, edge(v, 0.1) >= 0.010, (w, v))

    # ------------------------------------------------ the step outweighs the family's spread and the limit's own error
    # (delta-method standard error of the log-normal limit, relative: s * sqrt(1/n + k^2 / (2 (n - 1))))
    from scipy.stats import t as student_t
    R0 = lim[[r for r in lim if r.startswith("R0")][0]]
    fam = RT.LICENSED + RT.VARIANTS + [x for x in g["sets"] if x.startswith("R3t")]
    for k in W.INDICATORS:
        vals = [v for (w, ei, kk), v in g["bg"].items() if kk == k and not g["rev"][(w, ei)]]
        ok("estimator.golden_background_count.%s" % k, len(vals) == g["golden_n"][k], (len(vals), g["golden_n"][k]))
        y = [math.log(v) for v in vals]
        n = len(y)
        kf = float(student_t.ppf(0.99, n - 1)) * math.sqrt(1 + 1.0 / n)
        se = float(np.std(y, ddof=1)) * math.sqrt(1.0 / n + kf ** 2 / (2 * (n - 1)))
        lift = R0[k] / G[k] - 1
        spread = max(lim[r][k] for r in fam) / min(lim[r][k] for r in fam) - 1
        ok("estimator.step_outweighs_twice_spread_plus_error.%s" % k, lift > 2 * (spread + se), (k, lift, spread, se))
        for w in ("MW-7", "MW-9"):
            if g["exceed"][(w, k)]:
                ok("estimator.deciding_result_clears_limit_by_1.5_se.%s.%s" % (w, k), oc[(w, k)] / G[k] - 1 > 1.5 * se,
                   (w, k, oc[(w, k)] / G[k] - 1, se))

    # ------------------------------------------------ Shock: the golden set is no interval of any one-indicator sort
    for k in W.INDICATORS:
        order = sorted(W.COMPLIANCE, key=lambda w: -oc[(w, k)])
        top = order[:len(g["resample"])]
        ok("shock.golden_set_not_top_of_sort.%s" % k, set(top) != set(g["resample"]), (k, top))
    ok("shock.MW7_and_MW9_lead_on_different_indicators",
       g["exceed"][("MW-7", "sodium")] and not g["exceed"][("MW-7", "boron")] and g["exceed"][("MW-9", "boron")]
       and not g["exceed"][("MW-9", "sodium")])

    # ------------------------------------------------ the head relation: clear of zero, robust to the datum
    for w in W.BACKGROUND:
        for e in W.BG_EVENTS:
            d = g["head_diff"][(w, e)]
            ok("SF11.head_relation_clear_of_zero.%s.%s" % (w, EV[e]), abs(d) >= 0.10, (w, EV[e], d))
    # every point resurveyed together, so a single datum throughout classifies the same events
    alt = reclassify_one_datum(tgt)
    ok("SF11.single_datum_same_classification", alt == {k: v for k, v in g["rev"].items()})
    # chemistry corroborates the heads at both reversing wells: every reversed sample above every other on all three
    for w in ("MW-1", "MW-2"):
        for k in W.INDICATORS:
            r_ = [v for (ww, e, kk), v in g["bg"].items() if ww == w and kk == k and g["rev"][(w, e)]]
            n_ = [v for (ww, e, kk), v in g["bg"].items() if ww == w and kk == k and not g["rev"][(w, e)]]
            ok("SF14.chemistry_separates_reversed_samples.%s.%s" % (w, k), min(r_) > max(n_), (w, k, min(r_), max(n_)))
    ok("SF14.MW3_never_reversed", not any(g["rev"][("MW-3", e)] for e in range(len(EV))))
    # the boundary point: the nearest piezometer, or the two nearest, classify the same
    ok("SF12.boundary_point_choice_inert", boundary_alternatives(g) == 0)

    # ------------------------------------------------ the semantic forks on the main call
    text_all = pack_text(tgt)
    # SF1 background population (every unaffected routine sample): the readings that drop the whole well, the whole
    # event or the next event are other sets of samples; each is a member of the route table, its set recorded
    ok("SF1.background_n", g["golden_n"] == {"chloride": 34, "sodium": 34, "boron": 33}, g["golden_n"])
    ok("SF1.whole_well_reading_wrong", g["sets"]["R2a background without MW-1"] != g["resample"])
    # SF2 field duplicates are not background: including them leaves the call
    ok("SF2.duplicates_inert", call_with(tgt, g, include_fd=True) == g["resample"])
    # SF3 re-analyses: the reportable result; keeping both runs leaves the call
    ok("SF3.reanalysis_inert", call_with(tgt, g, keep_all_runs=True) == g["resample"])
    # SF4 boron units differ by a factor of 1000 between the laboratories, so a mix is unmistakable
    bA = [v for (w, e, k), v in g["indicators"].items() if k == "boron" and e < W.LAB_SWITCH]
    ok("SF4.boron_units_converted", min(bA) > 10.0, min(bA))
    # SF5 the plan's formula: the normal-scale limit leaves the call
    ok("SF5.normal_scale_inert_on_set", normal_scale_set(g) == g["resample"])
    # SF6 strict comparison: nothing within 1 per cent of a limit
    ok("SF6.no_result_near_a_limit", all(abs(oc[(w, k)] / G[k] - 1) > 0.01 for w in W.COMPLIANCE for k in W.INDICATORS))
    # SF7 rounded or unrounded limit: the same verdicts
    ok("SF7.rounded_limit_same_verdicts", all((oc[(w, k)] > float(figs["limits"][k])) == g["exceed"][(w, k)]
                                              for w in W.COMPLIANCE for k in W.INDICATORS))
    # SF8 MW-5R in MW-5's place: MW-5R under every limit either way
    ok("SF8.MW5R_under_every_limit", not any(g["exceed"][("MW-5R", k)] for k in W.INDICATORS))
    # SF9 the October primary result, not the duplicate: same verdicts
    ok("SF9.october_duplicate_inert", call_with(tgt, g, october_fd=True) == g["resample"])
    # SF10 dissolved sodium and boron: the wells carry no total fraction of either
    ok("SF10.no_total_sodium_or_boron_at_wells", not total_fraction_at_wells(tgt))
    # SF13 the gauging day stands for the event: every event's samples follow its gauging within three days
    ok("SF13.samples_within_event_days", samples_within_event(tgt))
    # SF15 the window: through April 2026, the October 2026 background samples out; including them leaves the set
    ok("SF15.october_background_inert", call_with(tgt, g, include_oct_bg=True) == g["resample"])
    # SF16 any indicator over its limit sends the well: MW-7 and MW-9 each exceed on one indicator
    ok("SF16.one_indicator_suffices", sum(g["exceed"][("MW-7", k)] for k in W.INDICATORS) == 1
       and sum(g["exceed"][("MW-9", k)] for k in W.INDICATORS) == 1)
    # SF17 to SF20, the head-conditioned family on the graded limits and counts. Every member files the set; the ones
    # that drop more than the reversed samples print other limits and counts, and each extra sample they drop is one
    # of groundwater the landfill had not affected, which SAP 4 keeps ("every routine sample of that groundwater"):
    # the well's head stood above its boundary piezometer's by at least 0.10 ft on water levels read to 0.01 ft
    # (FS-03 1), and at MW-1 and MW-2 the sample sits below every reversed sample of its well on all three indicators
    ok("SF17.sap_files_every_sample_of_unaffected_groundwater",
       "every routine sample of that groundwater collected at the background wells" in text_all)
    lowest_reversed = {(w, k): min(v for (ww, e, kk), v in g["bg"].items() if ww == w and kk == k and g["rev"][(w, e)])
                       for w in ("MW-1", "MW-2") for k in W.INDICATORS}
    for sf, name, dropped in variant_drops(g):
        for k in W.INDICATORS:
            ok("%s.drop_set_reproduces_the_route.%s.%s" % (sf, name.split()[0], k),
               g["golden_n"][k] - sum(1 for (w, e) in dropped if (w, e, k) in g["bg"]) == g["counts"][name][k],
               (name, k, len(dropped), g["counts"][name][k]))
        ok("%s.prints_other_graded_figures.%s" % (sf, name), any(s3(lim[name][k]) != s3(G[k]) for k in W.INDICATORS)
           or g["counts"][name] != g["golden_n"], name)
        ok("%s.drops_only_unaffected_samples_by_head.%s" % (sf, name),
           all(g["head_diff"][s] >= 0.10 for s in dropped), [(s, g["head_diff"][s]) for s in dropped])
        ok("%s.drops_only_unaffected_samples_by_chemistry.%s" % (sf, name),
           all(g["bg"][(w, e, k)] < lowest_reversed[(w, k)] for (w, e) in dropped if w != "MW-3"
               for k in W.INDICATORS if (w, e, k) in g["bg"]), name)
    ok("SF19.no_head_relation_within_a_tolerance_of_zero",
       min(g["head_diff"][(w, e)] for w in W.BACKGROUND for e in W.BG_EVENTS if not g["rev"][(w, e)]) >= 0.10
       and max(g["head_diff"][(w, e)] for w in W.BACKGROUND for e in W.BG_EVENTS if g["rev"][(w, e)]) <= -0.15)
    ok("SF20.rosner_after_heads_prints_the_golden_figures",
       all(abs(lim["R3r heads then Rosner"][k] - G[k]) < 1e-12 for k in W.INDICATORS)
       and g["counts"]["R3r heads then Rosner"] == g["golden_n"])

    # ------------------------------------------------ R2: every mess item neutral on the call
    ok("R2.lab_qc_rows_excluded_by_type", call_with(tgt, g, keep_lab_qc=True) == g["resample"])
    ok("R2.mw5_history_inert", g["exceed"][("MW-5R", "chloride")] is False)
    ok("R2.datum_inert", alt == g["rev"])

    # ------------------------------------------------ the asks: devices outside the call's rows, the ladder's stops
    import ceiling as CE
    sheet = CE.measure(tgt, g)
    n_spc = len(g["spc"])
    st = sheet["A1"]["stops"]
    # A1 is a reconstruction across two systems: the set the sample was collected immediately after, found from the
    # chain of custody's local minute in the laboratory's deliverable against the field app's UTC; the meter carried
    # across the unpaired sets; the meter's reporting on that day's calibration; the conversion where it reports at
    # the sample's temperature
    handtyped = [w for w in g["spc"] if g["field_detail"][w]["sets_after_sample"] == 0]
    ok("asks.spc_sample_set_carried_and_calibrated_is_golden", st["sample_set_carried"] == n_spc, st)
    ok("asks.spc_sample_set_as_logged_misses_the_uncompensated_meter_wells", st["sample_set_as_logged"] <= n_spc - 6, st)
    ok("asks.spc_sample_set_own_serial_misses_the_unpaired_sets",
       st["sample_set_own_serial"] == n_spc - len(W.METER_UNPAIRED), st)
    ok("asks.spc_last_set_misses_every_logged_visit", st["last_set_carried"] == len(handtyped), (st, handtyped))
    ok("asks.handtyped_visits_are_the_unpaired_ones", sorted(handtyped) == sorted(W.METER_UNPAIRED), handtyped)
    ok("asks.cracker_misses_spc", sheet["A1"]["cracker"] < n_spc, sheet["A1"])
    ok("asks.cracker_misses_purge", sheet["A2"]["cracker"] < len(g["purge"]), sheet["A2"])
    ok("asks.purge_device_moves_every_well", sheet["A2"]["cracker"] == 0, sheet["A2"])
    ok("asks.purge_end_is_the_sample_set", sheet["A2"]["stops"]["sample_set_pump_stop"] == len(g["purge"]), sheet["A2"])
    ok("asks.pair_ceiling_under_60", sheet["pair"] <= 60.0, sheet["pair"])
    ok("asks.mirror_leakage_under_two_fifths", sheet["mirror_leakage"] < 40.0, sheet["mirror_leakage"])
    ok("asks.spc_device_moves_rental_wells", sum(1 for w in g["spc"] if abs(g["field_detail"][w]["recorded"] - g["spc"][w]) > 50) >= 6)
    ok("asks.field_files_not_read_by_call", PK.FILES["purge"] not in call_files() and PK.FILES["calib"] not in call_files())
    # the sample set is fixed by the collection minute with room on both sides under any minute convention: the set
    # sits at least 30 s before the chain of custody's minute begins, the next set at least 120 s after it
    rows_p = [dict(r, t=dt.datetime.strptime(r["entry_utc"], "%Y-%m-%dT%H:%M:%SZ"))
              for r in csv.DictReader(open(os.path.join(tgt, PK.FILES["purge"]), encoding="utf-8"))]
    ok("asks.purge_export_marks_no_sample", not any(r["remark"] not in ("", "decon rinse", "bottles filled, pump off")
                                                   for r in rows_p))
    for w, d in g["field_detail"].items():
        mine = [r for r in rows_p if r["location"] == w and r["visit_date"].startswith("2026-10")]
        nxt = [r["t"] for r in mine if r["remark"] == "" and r["t"] > d["set_utc"]]
        ok("asks.coc_after_sample_set.%s" % w, (d["coc_utc"] - d["set_utc"]).total_seconds() >= 30, (w, d))
        ok("asks.next_set_after_coc.%s" % w, not nxt or (min(nxt) - d["coc_utc"]).total_seconds() >= 120, (w, nxt))
        bottles = [r["t"] for r in mine if r["remark"] == "bottles filled, pump off"]
        first = min(r["t"] for r in mine)
        # only daylight time joins the two systems: an hour later every sample would follow its pump's stop, and the
        # chain of custody read as UTC would put every sample before its visit began
        ok("asks.only_daylight_time_fits.%s" % w, d["coc_utc"] + dt.timedelta(hours=1) > max(bottles)
           and d["coc_utc"] - dt.timedelta(hours=5) < first, w)
        # SF21: the counter carried from the sample's set to the custody minute (at the set's logged flow, at the rate
        # of the last interval, or on the line to the next counter) prints the same tenth of a gallon as the set's own
        sets = sorted([r for r in mine if r["remark"] == ""], key=lambda r: r["t"])
        k = [i for i, r in enumerate(sets) if r["t"] == d["set_utc"]][0]
        s_, p_ = sets[k], sets[k - 1]
        after = sorted([r for r in mine if r["t"] > s_["t"]], key=lambda r: r["t"])[0]
        lag = (d["coc_utc"] - s_["t"]).total_seconds() / 60.0
        rates = {"logged_flow": float(s_["flow_ml_min"]) / 1000.0,
                 "last_interval": (float(s_["controller_l"]) - float(p_["controller_l"])) / ((s_["t"] - p_["t"]).total_seconds() / 60.0),
                 "line_to_next": (float(after["controller_l"]) - float(s_["controller_l"])) / ((after["t"] - s_["t"]).total_seconds() / 60.0)}
        fig = round(g["purge"][w], 1)
        for name, rate in rates.items():
            carried = g["purge"][w] + rate * lag / W.L_PER_GAL
            ok("SF21.carried_to_custody_minute_same_figure.%s.%s" % (w, name),
               round(carried, 1) == fig and fig + 0.05 - carried >= 0.004, (w, name, g["purge"][w], carried))
    # SF22: the gallon is the US gallon, named in the asking sentence; the counter logs litres
    prompt_text = open(os.path.join(os.path.dirname(tgt), "prompt.txt"), encoding="utf-8").read()
    ok("SF22.prompt_names_the_us_gallon", "US gallons purged before its sample" in prompt_text)
    ok("SF22.golden_uses_the_us_gallon", abs(W.L_PER_GAL - 3.785411784) < 1e-12)
    ok("SF22.counter_logs_litres", "controller_l" in rows_p[0])
    # FS-03 3's stabilization criteria are met at no point of any 2026 visit, so the criteria name no competing set:
    # the set a sample's readings are reported from is the one it was collected immediately after
    ok("asks.no_visit_meets_the_stabilization_criteria", not stable_triples(rows_p), stable_triples(rows_p)[:5])
    # the calibration entries: every sonde-day of both events calibrated in the morning and checked at the end of the
    # day by the day's sampler, every standard of every sensor entered, the conductivity reporting in the units the
    # app prints and in the value the standard should read, agreeing morning and evening; no free text
    cal = list(csv.DictReader(open(os.path.join(tgt, PK.FILES["calib"]), encoding="utf-8")))
    ok("calib.no_free_text_column", not any(c in ("remark", "notes", "comment", "comments") for c in cal[0]))
    ok("calib.header", list(cal[0].keys()) == PK.CAL_HEAD)
    ok("calib.no_compensation_column", not any("compens" in c for c in cal[0]))
    used = {(r["visit_date"], r["meter_sn"]) for r in rows_p if r["meter_sn"]}
    for d, m in sorted(used):
        mine = [r for r in cal if r["cal_date"] == d and r["meter_sn"] == m]
        ok("calib.sonde_day_calibrated.%s.%s" % (d, m),
           sum(1 for r in mine if r["check_type"] == "calibration") == 8
           and sum(1 for r in mine if r["check_type"] == "end-of-day check") == 2, (d, m, len(mine)))
        cond = [r for r in mine if r["sensor"] == "Conductivity"]
        at25 = {r["reading_units"] == "uS/cm at 25 C" for r in cond}
        ok("calib.conductivity_reporting_agrees_through_the_day.%s.%s" % (d, m), len(at25) == 1)
        ok("calib.conductivity_reporting_is_the_meter's.%s.%s" % (d, m), at25 == {W.COND_COMPENSATED[m]}, (d, m, at25))
        for r in cond:
            at_25 = r["reading_units"] == "uS/cm at 25 C"
            want = W.KCL_STD_US_CM if at_25 else W.KCL_STD_US_CM * (1 + W.TEMP_COEF * (float(r["std_temperature_c"]) - 25))
            ok("calib.conductivity_expected_value.%s.%s.%s" % (d, m, r["check_type"][:3]),
               abs(float(r["expected_value"]) - want) <= 0.5, r)
    ok("calib.both_reportings_present", {r["reading_units"] for r in cal if r["sensor"] == "Conductivity"}
       == {"uS/cm", "uS/cm at 25 C"})
    ok("calib.rental_tags_share_one_form", re.fullmatch(r"R-\d{4}", W.RENTAL_UNCOMP) and re.fullmatch(r"R-\d{4}", W.RENTAL_OK))
    ok("calib.serial_carried_on_the_unpaired_sets", all(
        g["field_detail"][w]["meter"] == W.RENTAL_UNCOMP for w in W.METER_UNPAIRED))
    days_used = {r["cal_date"] for r in cal}
    ok("calib.only_sampling_days", days_used == {d.strftime("%Y-%m-%d") for ei in (W.EVAL - 1, W.EVAL)
                                                 for d in W.EVENTS[ei]["days"]}, days_used)

    # ------------------------------------------------ input gates
    files = sorted(os.listdir(tgt))
    ok("gate.ten_files", len(files) >= 10, files)
    ok("gate.three_formats", len({f.rsplit(".", 1)[1] for f in files}) >= 3)
    ok("gate.large_file", max(info["edd_a_rows"], info["edd_b_rows"]) >= 25000, info["edd_b_rows"])
    md = json.load(open(os.path.join(os.path.dirname(tgt), "metadata.json")))
    ok("gate.two_distractors", len(md["distractor_files"]) >= 2)
    ok("gate.no_describing_file", not any(re.search(r"readme|dictionary|manifest|notes|codebook|schema", f, re.I) for f in files))
    for d in PK.DISTRACTORS:
        ok("gate.distractor_unread.%s" % d, PK.FILES[d] not in call_files() + ask_files())

    # ------------------------------------------------ leak words: nothing in the pack names the decisive step
    text = text_all
    for wd in ("reversal", "reversed", "well field", "wellfield", "pumping", "gradient revers",
               "flow direction", "upgradient at the time", "beneath the waste"):
        ok("leak.word_absent.%s" % wd.replace(" ", "_"), wd not in text, wd)
    ok("leak.positive_control_sap_read", "background water quality is the quality of groundwater that the landfill has not affected" in text)
    # the governing documents carry their genre's furniture (title block, document control, revision history, approval
    # signatures, running header and page numbers) and the furniture names no well, indicator, meter or data file
    for key, marks in (("sap", ("mcl-gw-sap", "revision history", "environmental programs manager", "page 1 of")),
                       ("fieldproc", ("fs-03 rev. 4", "revision history", "quality assurance manager", "page 1 of"))):
        body = pdf_text(os.path.join(tgt, PK.FILES[key]))
        ok("docs.furnished.%s" % key, all(m in body for m in marks), (key, [m for m in marks if m not in body]))
        tail = body[body.index("revision history"):]
        ok("docs.furniture_names_no_data.%s" % key, not re.search(
            r"mw-\d|pz-\d|chloride|sodium|boron|r-44\d\d|21c0847|\.csv|\.txt|\.xlsx|conductiv|meter", tail), (key, tail))

    # ------------------------------------------------ realism sweep
    plan = info["plan"]
    for ei in plan:
        times = [s[2] for s in plan[ei] if s[3] == "N" and s[0].startswith("MW")]
        ok("realism.sampling_times_ascend_within_days.%s" % EV[ei], all(
            a <= b for a, b in zip(times, times[1:]) if a.date() == b.date()))
    dtw = [float(r["dtw_ft_btoc"]) for r in csv.DictReader(open(os.path.join(tgt, PK.FILES["gauging"]), encoding="utf-8"))]
    ok("realism.depths_vary", len(set(dtw)) > 200)
    ok("realism.no_round_limits", all(abs(G[k] - round(G[k])) > 0.05 for k in W.INDICATORS))
    return N[0]


# ---------------------------------------------------------------- helpers
def call_files():
    return [PK.FILES[k] for k in ("edd_a", "edd_b", "gauging", "points", "sap")]


def ask_files():
    return [PK.FILES[k] for k in ("purge", "calib", "fieldproc")]


def stable_triples(rows):
    """every run of three consecutive reading sets in a visit that agree within FS-03 3's criteria (3 per cent
    specific conductance, 0.1 pH, 10 per cent dissolved oxygen above 0.5 mg/L, 10 per cent or 1 NTU turbidity)"""
    def agree(a, b):
        s1, s2 = float(a["spc_us_cm"]), float(b["spc_us_cm"])
        d1, d2 = float(a["do_mg_l"]), float(b["do_mg_l"])
        t1, t2 = float(a["turb_ntu"]), float(b["turb_ntu"])
        return (abs(s1 - s2) <= 0.03 * max(s1, s2) and abs(float(a["ph_su"]) - float(b["ph_su"])) <= 0.1
                and (max(d1, d2) <= 0.5 or abs(d1 - d2) <= 0.10 * max(d1, d2))
                and abs(t1 - t2) <= max(1.0, 0.10 * max(t1, t2)))
    visits = {}
    for r in rows:
        if r["remark"] == "":
            visits.setdefault((r["visit_date"], r["location"]), []).append(r)
    out = []
    for key, rs in visits.items():
        rs = sorted(rs, key=lambda r: r["t"])
        for i in range(2, len(rs)):
            if agree(rs[i - 2], rs[i - 1]) and agree(rs[i - 1], rs[i]):
                out.append((key, i))
    return out


def s3(x):
    d = 3 - int(math.floor(math.log10(abs(x)))) - 1
    return ("%%.%df" % max(d, 0)) % round(x, d)


def variant_drops(g):
    """the samples each head-conditioned family member drops beyond the golden's reversed ones (routes.py's own
    predicates, restated so the checks do not share the route code's state)"""
    rev = g["rev"]
    hd = {(w, e): g["heads"][(w, e)][0] - g["heads"][(W.BOUNDARY[w], e)][0] for (w, e) in rev}
    kept = sorted({(w, e) for (w, e, k) in g["bg"] if not rev[(w, e)]})
    revents = {e for (w, e), r in rev.items() if r}
    nxt = {e + 1 for e in revents}
    out = [("SF17", "R3e whole reversed events dropped", [s for s in kept if s[1] in revents]),
           ("SF18", "R3n reversed and following events dropped", [s for s in kept if s[0] != "MW-3" and s[1] in nxt])]
    for tol in (0.15, 0.25):
        out.append(("SF19", "R3t heads with a %.2f ft tolerance" % tol, [s for s in kept if hd[s] < tol]))
    return out


def pack_text(tgt):
    import pdfplumber
    out = []
    for fn in sorted(os.listdir(tgt)):
        p = os.path.join(tgt, fn)
        if fn.endswith(".pdf"):
            with pdfplumber.open(p) as pdf:
                t = " ".join((pg.extract_text() or "") for pg in pdf.pages)
            assert len(t) > 200, fn
            out.append(t)
        elif fn.endswith(".xlsx"):
            with zipfile.ZipFile(p) as z:
                out.append(" ".join(z.read(n).decode("utf-8", "replace") for n in z.namelist() if n.endswith(".xml")))
        else:
            out.append(open(p, encoding="utf-8").read())
    return re.sub(r"\s+", " ", " ".join(out)).lower()


def pdf_text(path):
    import pdfplumber
    with pdfplumber.open(path) as pdf:
        t = " ".join((pg.extract_text() or "") for pg in pdf.pages)
    return re.sub(r"\s+", " ", t).lower()


def reclassify_one_datum(tgt):
    """heads on the 2014 and 2017 surveys only (NGVD 29 throughout, MW-5R and the trimmed MW-8 aside)"""
    from openpyxl import load_workbook
    wb = load_workbook(os.path.join(tgt, PK.FILES["points"]), read_only=True)
    toc = {}
    for row in list(wb["Survey"].iter_rows(values_only=True))[1:]:
        if row[2] == "NGVD 29":
            toc[row[0]] = float(row[3])
    h = {}
    for r in csv.DictReader(open(os.path.join(tgt, PK.FILES["gauging"]), encoding="utf-8")):
        if r["location"] in toc:
            h[(r["location"], EV.index(r["event"]))] = toc[r["location"]] - float(r["dtw_ft_btoc"])
    return {(w, e): h[(w, e)] < h[(W.BOUNDARY[w], e)] for w in W.BACKGROUND for e in range(len(EV))}


def boundary_alternatives(g):
    """count events where reading MW-2 against PZ-1, or MW-3 against PZ-1, would classify differently"""
    diffs = 0
    for e in range(len(EV)):
        h = {p: g["heads"][(p, e)][0] for p in ("MW-1", "MW-2", "MW-3", "PZ-1", "PZ-2", "PZ-3")}
        if (h["MW-2"] < min(h["PZ-2"], h["PZ-1"] + 0.0)) != g["rev"][("MW-2", e)] and h["MW-2"] < h["PZ-2"]:
            diffs += 1
        if (h["MW-3"] < h["PZ-3"]) != g["rev"][("MW-3", e)]:
            diffs += 1
    return diffs


def normal_scale_set(g):
    from scipy import stats
    bg = g["bg"]
    lim = {}
    for k in W.INDICATORS:
        v = np.array([x for (w, e, kk), x in bg.items() if kk == k and not g["rev"][(w, e)]])
        n = len(v)
        lim[k] = v.mean() + stats.t.ppf(0.99, n - 1) * v.std(ddof=1) * math.sqrt(1 + 1 / n)
    return RT.designate(lim, g["october"])


def call_with(tgt, g, include_fd=False, keep_all_runs=False, october_fd=False, include_oct_bg=False, keep_lab_qc=False):
    """the golden call with one convention or mess item handled the other way"""
    ind = {}
    extra = []
    for r in csv.DictReader(open(os.path.join(tgt, PK.FILES["edd_b"]), encoding="utf-8"), delimiter="\t"):
        key = (r["chemical_name"], r["fraction"])
        if key not in GD.IND_B:
            continue
        stype = r["sample_type_code"]
        if stype == "N" and (r["reportable_result"] == "Yes" or keep_all_runs) and r["sys_loc_code"].startswith("MW"):
            pass
        elif stype == "FD" and (include_fd or october_fd):
            pass
        elif keep_lab_qc and stype in ("MS", "SD") and r["sys_loc_code"].startswith("MW"):
            pass
        else:
            continue
        ei = GD.event_of(dt.date.fromisoformat(r["sample_date"][:10]))
        k = GD.IND_B[key]
        v = float(r["result_value"])
        if stype in ("MS", "SD"):
            continue     # percent recoveries: a reader keeping them sees a unit of %REC, not a concentration
        extra.append((GD.norm_loc(r["sys_loc_code"]), ei, k, v, stype))
    bg = dict(g["bg"])
    october = dict(g["october"])
    for loc, ei, k, v, stype in extra:
        if stype == "FD" and include_fd and loc in W.BACKGROUND and ei in W.BG_EVENTS:
            bg[(loc + "dup", ei, k)] = v
        if stype == "FD" and october_fd and ei == W.EVAL and loc in W.COMPLIANCE:
            october[(loc, k)] = v
        if stype == "N" and keep_all_runs and loc in W.BACKGROUND and ei in W.BG_EVENTS:
            if (loc, ei, k) in bg and abs(bg[(loc, ei, k)] - v) > 1e-9:
                bg[(loc + "run", ei, k)] = v
    if include_oct_bg:
        for w in W.BACKGROUND:
            for k in W.INDICATORS:
                if not g["rev"][(w, W.EVAL)]:
                    bg[(w + "oct", W.EVAL, k)] = g["indicators"][(w, W.EVAL, k)]
    rev = dict(g["rev"])
    for (w, e, k) in list(bg):
        if w not in W.BACKGROUND:
            base = w[:4]
            rev[(w, e)] = g["rev"][(base, e)]
    lim = {}
    for k in W.INDICATORS:
        v = [x for (w, e, kk), x in bg.items() if kk == k and not rev[(w, e)]]
        lim[k] = RT.upl(v)
    return RT.designate(lim, october)


def total_fraction_at_wells(tgt):
    for r in csv.DictReader(open(os.path.join(tgt, PK.FILES["edd_b"]), encoding="utf-8"), delimiter="\t"):
        if r["sys_loc_code"].startswith("MW") and r["chemical_name"] in ("Sodium", "Boron") and r["fraction"] == "T":
            return True
    return False


def samples_within_event(tgt):
    for r in csv.DictReader(open(os.path.join(tgt, PK.FILES["edd_b"]), encoding="utf-8"), delimiter="\t"):
        if r["sample_type_code"] == "N" and r["sys_loc_code"].startswith("MW"):
            GD.event_of(dt.date.fromisoformat(r["sample_date"][:10]))
    return True
