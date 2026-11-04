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

    # ------------------------------------------------ R2: every mess item neutral on the call
    ok("R2.lab_qc_rows_excluded_by_type", call_with(tgt, g, keep_lab_qc=True) == g["resample"])
    ok("R2.mw5_history_inert", g["exceed"][("MW-5R", "chloride")] is False)
    ok("R2.datum_inert", alt == g["rev"])

    # ------------------------------------------------ the asks: devices outside the call's rows, cracker misses
    import ceiling as CE
    sheet = CE.measure(tgt, g)
    ok("asks.cracker_misses_spc", sheet["A1"]["cracker"] < len(g["spc"]), sheet["A1"])
    ok("asks.cracker_misses_purge", sheet["A2"]["cracker"] < len(g["purge"]), sheet["A2"])
    ok("asks.pair_ceiling_under_60", sheet["pair"] <= 60.0, sheet["pair"])
    ok("asks.mirror_leakage_under_50", sheet["mirror_leakage"] < 50.0, sheet["mirror_leakage"])
    ok("asks.spc_device_moves_rental_wells", sum(1 for w in g["spc"] if abs(g["field_detail"][w]["recorded"] - g["spc"][w]) > 50) >= 6)
    ok("asks.purge_device_moves_every_well", sheet["A2"]["cracker"] == 0, sheet["A2"])
    ok("asks.field_file_not_read_by_call", PK.FILES["purge"] not in call_files())

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
    text = pack_text(tgt)
    for wd in ("reversal", "reversed", "well field", "wellfield", "pumping", "gradient revers",
               "flow direction", "upgradient at the time", "beneath the waste"):
        ok("leak.word_absent.%s" % wd.replace(" ", "_"), wd not in text, wd)
    ok("leak.positive_control_sap_read", "background water quality is the quality of groundwater that the landfill has not affected" in text)

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
    return [PK.FILES[k] for k in ("purge", "fieldproc")]


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
