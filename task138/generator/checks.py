"""Generator assertions for task138 architecture 2, run on the built target/ and the world's clean truth.

    python3 task138/generator/checks.py     # exit 1 on any failed assertion
"""
import copy
import json
import math
import os
import re
import shutil
import sys
import tempfile
import zipfile

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
sys.path.insert(0, HERE)
import analysis as A  # noqa: E402
import io_util as IO  # noqa: E402
import lp3 as L  # noqa: E402
import pack as PK  # noqa: E402
import params as PR  # noqa: E402
import world as W  # noqa: E402

RES = []
PEOPLE = ["Dennis Zhang", "Kristin Lucas", "Eric Thornton", "Jesus Hernandez"]


def ok(name, cond, detail=""):
    RES.append((name, bool(cond), detail))


def edge(v, u):
    """Distance from v to the nearest rounding edge of a grid of step u."""
    c = round(v / u) * u
    return u / 2 - abs(v - c)


def rnd(v, u):
    return round(round(v / u) * u, 6)


def main():
    P = A.Pack(TARGET)
    AF = A.AskFiles(TARGET)
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    S = W.simulate()
    m = A.main_figures(P)
    rt = A.routes(P)
    q_g = m["q_design"]

    # ---------------------------------------------------------------- the ladder on the shipped pack
    ok("golden: raise 2 ft, design discharge 110,000 cfs", m["raise"] == 2 and m["q_design_5k"] == 110000,
       "%d %.0f" % (m["raise"], q_g))
    ok("golden: the railroad closure 118+70 governs every raise", set(m["governing"]) == {11870}, str(m["governing"]))
    ok("golden: shortfall at 118+70 sits mid-step (1.25 to 1.75 ft)", 1.25 <= m["need"] <= 1.75, "%.3f" % m["need"])
    r0 = rt["R0_at_site"]
    ok("rung 0 (LS-02 fit to the published Orrinsford record): no raise, 95,000 cfs",
       r0["raise"] == 0 and rnd(r0["q"], 5000) == 95000, "%.0f" % r0["q"])
    p_mk, p_pt = A.trend_tests(np.log10(P.hal.values))
    p_mk2, p_pt2 = A.trend_tests(P.hal.values)
    ok("rung 1 (homogeneity tests on the Orrinsford record): Mann-Kendall and Pettitt find nothing (p > 0.2), so "
       "rung 0 stands", min(p_mk, p_pt, p_mk2, p_pt2) > 0.2, "%.2f %.2f %.2f %.2f" % (p_mk, p_pt, p_mk2, p_pt2))
    r2 = rt["R2_post_raise_only"]
    ok("rung 2 (only the water years since the last raise): 1 ft", r2["raise"] == 1, "%.0f" % r2["q"])
    r3 = rt["R3_whole_record_relation"]
    ok("rung 3 (Coyle Bridge record at the whole-record relation): no raise", r3["raise"] == 0, "%.0f" % r3["q"])
    ok("each rung's design discharge falls outside the golden's 5,000 cfs bin",
       all(rnd(v["q"], 5000) != 110000 for k, v in rt.items() if not k.startswith("golden")),
       str({k: rnd(v["q"], 5000) for k, v in rt.items()}))
    cheap = [k for k in rt if k.startswith(("R", "off"))]
    landing = [k for k in cheap if rt[k]["raise"] == 2]
    ok("Gate F: no cheap route (rungs 0 to 3, Coyle unscaled, since 1994, drainage-area ratio at 0.5, 0.7, 1.0) "
       "files 2 ft", landing == [], str(landing))
    ok("the rungs file three different raises (0, 1, 2) across the ladder",
       {r0["raise"], r2["raise"], m["raise"]} == {0, 1, 2})
    ok("rung 2 sits 0.3 ft or more from a whole-foot edge", min(A.need(P, r2["q"]) % 1, 1 - A.need(P, r2["q"]) % 1)
       >= 0.3, "%.3f" % A.need(P, r2["q"]))

    # ---------------------------------------------------------------- the golden family and every graded bin
    fam = A.golden_family(P)
    fits = {k: A.fit(v, P) for k, v in fam.items()}
    qs = {k: L.quantile(f, P.aep) for k, f in fits.items()}
    caps = m["capacity"]
    want = [round(a, 1) for a in m["aep"]]
    for k in A.FORMS:
        a_k = [100 * L.exceedance(fits[k], cpt) for cpt in caps]
        ok("form %s (fitted 2009 to 2026, applied 1962 to 2008): 2 ft, design discharge in 107,500 to 112,500 with "
           "1,500 cfs to spare, all five annual chances in their bins with 0.02 to spare" % k,
           A.raise_for(P, qs[k]) == 2 and edge(qs[k], 5000) >= 1500 and rnd(qs[k], 5000) == 110000 and
           [round(x, 1) for x in a_k] == want and min(edge(x, 0.1) for x in a_k) >= 0.02,
           "Q %.0f, chances %s" % (qs[k], [round(x, 3) for x in a_k]))
    extra = [k for k in fam if k not in A.FORMS]
    ok("stress rows (%s): every one files 2 ft, the same design-discharge bin and the same five chances with 0.01 to "
       "spare" % ", ".join(extra),
       all(A.raise_for(P, qs[k]) == 2 and rnd(qs[k], 5000) == 110000 and
           [round(100 * L.exceedance(fits[k], cpt), 1) for cpt in caps] == want and
           min(edge(100 * L.exceedance(fits[k], cpt), 0.1) for cpt in caps) >= 0.01 for k in extra),
       str({k: round(qs[k]) for k in extra}))
    ok("design discharge: 1,500 cfs or more inside its bin under every construction",
       min(edge(q, 5000) for q in qs.values()) >= 1500, "%.0f" % min(edge(q, 5000) for q in qs.values()))
    ok("annual chances graded: 1.4, 1.1, 0.9, 0.7, 0.6", want == [1.4, 1.1, 0.9, 0.7, 0.6], str(m["aep"]))
    ok("shortfall at 118+70 between 1.2 and 1.8 ft under every member",
       all(1.2 <= A.need(P, q) <= 1.8 for q in qs.values()))
    ok("no Bulletin 17B low outlier in the golden or the published series",
       A.grubbs_beck_low(A.present_series(P)) == 0 and A.grubbs_beck_low(P.hal.values) == 0)

    # ---------------------------------------------------------------- semantic fork table
    ok("SF1 design flood = the LS-02 estimand (positive control: the standard files it)",
       "as they stand at the time of the review" in IO.pdf_text(A._find(TARGET, r"LS-02")))
    ok("SF2 annual chance per raise = exceedance of the discharge held with freeboard: without freeboard every "
       "raise holds more and the figures move", all(_cap_nofb(P, r) > caps[r] + 3000 for r in A.RAISES))
    ok("SF3 crown = the 2024 certification survey: the inventory's crown sheet equals the survey at all 21 "
       "cross-sections", _crown_matches(P, AF))
    adj = _projected_settlement(P, AF)
    ok("SF3b a crown lowered by three more years of settlement still files 2 ft", adj == 2, str(adj))
    s50 = _survey_reading(P, AF, q_g)
    ok("SF4 crown checked at every 50 ft survey shot instead of the 21 cross-sections: same raise and the same "
       "annual-chance bins", s50[0] == 2 and s50[1] == [round(a, 1) for a in m["aep"]], str(s50))
    ok("SF5 4 ft freeboard only at the bridge stations themselves (within 100 ft holds no other cross-section)",
       all(abs(s - b) > 100 for s in P.t4.index for b in P.bridges if s != b))
    ok("SF5b the pump station outlets read as closure structures too: no cross-section within 100 ft of them, so the "
       "same raise and annual-chance bins", all(abs(s - b) > 100 for s in P.t4.index for b in (1830, 16120)))
    lg = _loginterp(P, m["fit"])
    ok("SF6 Table 4 read log-linearly in discharge: same raise and annual-chance bins", lg == [round(a, 1) for a in
                                                                                             m["aep"]], str(lg))
    ok("SF7 the bridges the inventory lists are the Table 4 bridge cross-sections (62+40, 118+70)",
       sorted(P.bridges) == [6240, 11870])
    cy = _calendar_year_labels(P)
    ok("SF8 / L1 each published peak labelled by its calendar year instead of its water year: same raise and "
       "design-discharge bin", cy == (2, 110000), str(cy))
    cym = _calendar_year(P)
    ok("SF8b regrouping to calendar-year maxima drops water years' annual peaks (LS-02 section 3 takes one per water "
       "year) and "
       "still files 2 ft", cym[0] == 2 and _cy_drops(P) > 0, str(cym))
    std_txt = IO.pdf_text(A._find(TARGET, r"LS-02"))
    ok("SF21 the water years since the last raise alone (18 peaks, 1 ft) are ruled out by LS-02 section 3's window "
       "(one annual peak for every water year since the gauge opened in 1962)",
       "one annual peak discharge for every water year since the Orrinsford gauge opened in water year 1962" in
       std_txt and P.first_wy == 1962 and rt["R2_post_raise_only"]["n"] == 18 and
       len(A.present_series(P)) == 2026 - P.first_wy + 1)
    ok("SF21b LS-02 names no Coyle Bridge, extension, homogeneity, levee raise or relation",
       not any(w in std_txt.lower() for w in ("coyle", "extension", "extend", "homogene", "levee raise", "raised",
                                              "relation", "upstream gauge", "agricultural")))
    ok("SF22 LS-02 section 8 takes discharges from the State Water Survey's records without fixing which years are "
       "used as published (positive control)", "Discharges are taken from the State Water Survey's published records"
       in std_txt and "Annual peak discharges are those published" not in std_txt)
    ok("SF9 raises are uniform whole feet (LS-02 section 7): positive control",
       "uniform crown raise, in whole" in IO.pdf_text(A._find(TARGET, r"LS-02")))
    ok("SF10 regional skew and its mean square error read for region 2 (Pell and Marrow counties)",
       (P.gr, P.mse_r) == (-0.08, 0.14) and "Marrow" in IO.pdf_text(A._find(TARGET, r"regional_skew")))
    ok("SF11 the 1 per cent annual chance read from LS-02", abs(P.aep - 0.01) < 1e-12)
    pv = _drop(P, approval="P")
    ok("SF12 provisional water year 2026 left out: same raise and bins", pv == (2, 110000), str(pv))
    ok("SF13 / L1 no peak at Orrinsford or Coyle Bridge carries an estimate code (the codes sit on the other gauges)",
       P.peaks_df[P.peaks_df.site_no.isin(["05433000", "05432100"])]["peak_cd"].isna().all() and
       (P.peaks_df["peak_cd"].fillna("") == "2").sum() >= 5)
    c08 = A.present_series(P, cut=2008)
    ok("SF14 the last raise read as in force in water year 2008: same raise and bin",
       A.raise_for(P, A.q_aep(c08, P)) == 2 and rnd(A.q_aep(c08, P), 5000) == 110000)
    ok("SF15 weighted skew is the filed method: positive control in LS-02 section 3",
       "inverse of its mean square error" in IO.pdf_text(A._find(TARGET, r"LS-02")))
    ok("SF16 freeboard upstream allowance read from LS-02 (0.5 ft at 0+00 to nothing at 180+00)",
       (P.fb_up, P.len_ft) == (0.5, 18000))

    # ---------------------------------------------------------------- the three rules, on the clean truth
    pk = S["pk"]
    t_true = pk["hal_q"].values
    u_true = pk["coy_q"].values
    wy = pk["wy"].values
    q_easy = L.quantile(L.fit(t_true, PR.REGIONAL_SKEW, PR.REGIONAL_SKEW_MSE), PR.AEP)
    ok("R3a analyst test: the LS-02 fit to Orrinsford's own (clean) record files no raise",
       A.raise_for(P, q_easy) == 0, "%.0f" % q_easy)
    post = wy >= 2009
    r = np.sum(t_true[post] * u_true[post]) / np.sum(u_true[post] ** 2)
    q_dec = L.quantile(L.fit(np.where(post, t_true, r * u_true), PR.REGIONAL_SKEW, PR.REGIONAL_SKEW_MSE), PR.AEP)
    ok("R3b the decisive step alone (the record rebuilt for the river as it now runs) files 2 ft",
       A.raise_for(P, q_dec) == 2, "%.0f" % q_dec)
    q_pp = L.quantile(L.fit(t_true[post], PR.REGIONAL_SKEW, PR.REGIONAL_SKEW_MSE), PR.AEP)
    ok("R3b a lower rung's single correction (post-raise years only) stays on 1 ft", A.raise_for(P, q_pp) == 1)
    ok("R3b the clean truth's present-river flood (no attenuation anywhere) files 2 ft",
       A.raise_for(P, L.quantile(L.fit(pk["t_present"].values, PR.REGIONAL_SKEW, PR.REGIONAL_SKEW_MSE), PR.AEP)) == 2)
    ok("R1 the field's raw material ships: paired annual peaks at both gauges for every water year 1962 to 2026",
       list(P.hal.index) == list(P.coy.index) == list(range(1962, 2027)))
    ok("R1 no shipped file holds a present-river peak or the two-gauge relation",
       not _pack_mentions(["%.3f" % fig["present_relation"], "%.4f" % fig["present_relation"], "1.078"],
                          exclude=(".csv",)) and _no_present_column())
    ok("R1 the decisive computation reads the inventory's raise years for the segments between the gauges",
       len(P.raises_between()) == 6 and P.first_post_wy() == 2009)
    ok("R2 the published record's skew is not the decisive step: station skew alone on the published record also "
       "files no raise", _station_skew_only(P, P.hal.values) == 0)
    ok("R3c no repeated block: no 14-value run repeats in either annual peak series",
       not _repeats(P.hal.values) and not _repeats(P.coy.values))
    ok("R3c no plant: no file is a memo, draft or briefing arguing a raise figure", not _pack_mentions(
        ["recommend", "no raise is needed", "raise is not needed"], exclude=(".csv",)))
    ok("R3c the deciding relation shows only in large floods: below 46,000 cfs at Coyle Bridge the pre-raise and "
       "post-raise Orrinsford/Coyle ratios agree within 2 per cent", _small_flood_ratios(P) < 0.02,
       "%.4f" % _small_flood_ratios(P))

    # ---------------------------------------------------------------- Layer 1 neutrality (main path)
    ok("L1 water year: every Orrinsford and Coyle Bridge row maps to one water year (no year twice, none missing)",
       P.hal.index.is_unique and P.coy.index.is_unique)
    ok("L1 raise dates in mixed forms parse to six in-force water years 1997 to 2009",
       [w for _, w in P.raises_between()] == [1997, 1999, 2002, 2004, 2006, 2009])
    ok("L1 Table 4 read from the PDF: 21 cross-sections by 10 discharges", P.t4.shape == (21, 10))
    ok("L1 three significant figures in the published peaks", all(_sig3(v) for v in P.peaks_df["peak_va"]))

    # ---------------------------------------------------------------- asks
    st = A.settlement(AF)
    ok("ask A: settlement by reach for all eight reaches", sorted(st) == ["R%d" % i for i in range(1, 9)])
    ok("ask A: each reach's figure 0.003 ft or more inside its 0.01 ft bin",
       min(edge(v, 0.01) for v in st.values()) >= 0.003, str({k: round(v, 4) for k, v in st.items()}))
    stf = A.settlement(AF, use_features=True)
    ok("SF17 ask A: structures counted with the crown shots leave every reach in its bin",
       {k: rnd(v, 0.01) for k, v in stf.items()} == {k: rnd(v, 0.01) for k, v in st.items()})
    med = _settle_median(AF)
    ok("SF17b ask A: the median shot per reach gives the same bins as the mean",
       {k: rnd(v, 0.01) for k, v in med.items()} == {k: rnd(v, 0.01) for k, v in st.items()}, str(med))
    mrm = _mean_of_reach_means(AF)
    ok("SF17c ask A: every 2016 crown shot on today's levee pairs with exactly one 2024 shot and the reach mean of "
       "each survey differenced gives the paired figure", _one_to_one(AF) and
       all(abs(mrm[k] - st[k]) < 1e-9 for k in st), str({k: round(v, 4) for k, v in mrm.items()}))
    offs, common = A.station_offset(AF)
    ok("ask A: the four structures both surveys shot give one stationing offset (700 ft)",
       offs == [700] and len(common) == 4, str(offs))
    nv = A.settlement(AF, offset=0)
    ok("ask A device (stationing): matching by station number misses every reach and stays positive (silent)",
       all(rnd(nv[k], 0.01) != rnd(st[k], 0.01) for k in st) and min(nv.values()) > 0.05,
       str({k: round(v, 3) for k, v in nv.items()}))
    nd = A.settlement(AF, shift=0)
    ok("ask A hazard (datum): leaving the 2016 shots on NGVD 29 misses every reach and shows negative settlement",
       all(rnd(nd[k], 0.01) != rnd(st[k], 0.01) for k in st) and min(nd.values()) < 0)
    ok("SF20 ask A: the benchmark pairs give one shift (0.27 ft) at every benchmark",
       np.allclose(AF.bench["elev_navd88_ft"] - AF.bench["elev_ngvd29_ft"], 0.27))
    lt = A.lead_times(AF)
    ok("SF19 ask B: seven floods reached the Main Street sill since October 2016", len(lt) == 7, str(len(lt)))
    conv = [[int(round(h)) for _, h in A.lead_times(AF, convention=cv)] for cv in
            ("interp", "first_at_or_above", "last_below")]
    trunc = [int(math.floor(h)) for _, h in lt]
    ok("SF18 ask B: rounded, truncated, first-hour-at-or-above and last-hour-below crossings give the same whole hours",
       conv[0] == conv[1] == conv[2] == trunc, str(conv + [trunc]))
    ok("ask B: each lead time's fraction of an hour sits between 0.1 and 0.4", all(0.1 <= h % 1 <= 0.4 for _, h in lt),
       str([round(h, 2) for _, h in lt]))
    gold = [int(round(h)) for _, h in lt]
    old = [int(round(h)) for _, h in A.lead_times(AF, coy_mode="old_stage")]
    ok("ask B device (Coyle Bridge datum): 21.0 ft as printed misses all seven floods (all after the October 2019 "
       "datum change)", all(old[i] != gold[i] for i in range(7)), str(old))
    now = [int(round(h)) for _, h in A.lead_times(AF, coy_mode="elev_now")]
    ok("ask B: the warning elevation on today's Coyle Bridge datum gives the golden for every flood", now == gold,
       str(now))
    nc = [int(round(h)) for _, h in A.lead_times(AF, clock_fix=False)]
    ok("ask B device (logger clock): the ORF2 stamps read as headed miss all three 2020 floods",
       all(nc[i] != gold[i] for i in (0, 1, 2)), str(nc))
    nh = [int(round(h)) for _, h in A.lead_times(AF, hb_convert=False)]
    ok("ask B hazard (Orrinsford gauge datum on NGVD 29): misses five or more floods",
       sum(nh[i] != gold[i] for i in range(7)) >= 5, str(nh))
    chg, step = A.coy_datum_change(AF)
    ok("ask B: the Coyle Bridge stage steps 2.00 ft against discharge at 2019-10-22 15:00 UTC",
       chg == pd.Timestamp("2019-10-22 15:00") and abs(step - 2.0) < 0.03, "%s %.3f" % (chg, step))
    cr = A.clock_routes(AF)
    ok("clock route 1: the two ORF2 loggers' three-day overlap lines up at a 6 h shift and at no other",
       cr["overlap_shift_h"] == 6 and cr["overlap_mad_ft"] < 0.005 and _overlap_runner_up(AF) > 0.02,
       "%s %.4f %.4f" % (cr["overlap_shift_h"], cr["overlap_mad_ft"], _overlap_runner_up(AF)))
    ok("clock route 2: each water year's highest old-logger reading sits on the published Orrinsford peak time and "
       "each new-logger one 6 h after it", set(cr["orrinsford_old_minus_published"]) == {0.0} and
       set(cr["orrinsford_new_minus_published"]) == {6.0} and len(cr["orrinsford_old_minus_published"]) >= 4 and
       len(cr["orrinsford_new_minus_published"]) >= 4, str(cr))
    ok("clock route 3: Coyle Bridge's hourly record tops out 6 h after every published Coyle Bridge peak time (the "
       "published times are UTC less 6 h)", set(cr["coyle_hourly_minus_published"]) == {6.0} and
       len(cr["coyle_hourly_minus_published"]) == 10, str(cr["coyle_hourly_minus_published"]))
    swap, sh = A.halbrook_clock(AF)
    ok("ask B: the old logger's records sit 6 h behind UTC", sh == 6, "%s %d" % (swap, sh))
    ok("ask B device (logger clock): the ORF2 export carries stage alone, no diurnal channel",
       list(AF.hb.columns[:2]) == ["stamp", "stage"] and AF.hb.shape[1] == 3)
    ok("ask B: no telemetry gap within five days of any crossing", _no_gap_near(AF, lt))
    ok("ask B: the Coyle Bridge hourly maximum of each water year matches its published annual peak (1 per cent)",
       _coyle_max_matches(P, AF))
    ok("separation: the main call's files carry no gauge datum, stationing history, logger clock or survey",
       _main_files_clean())
    ok("separation: no ask figure is computable from the main call's files (no hourly stage, no 2016 survey there)",
       not _pack_mentions(["NGVD 29"], only=("LS-02", "Table4", "regional_skew", "levee_inventory")))

    # ---------------------------------------------------------------- figures.json, input gates, realism
    ok("figures.json carries the graded figures as computed", fig["call"]["raise_ft"] == m["raise"] and
       fig["call"]["design_discharge_cfs"] == m["q_design_5k"] and
       list(fig["aep_pct_by_raise"].values()) == [round(a, 1) for a in m["aep"]] and
       fig["settlement_ft"] == {k: round(v, 2) for k, v in st.items()})
    files = sorted(os.listdir(TARGET))
    ok("input gate: 10 or more files", len(files) >= 10, str(len(files)))
    ok("input gate: 3 or more formats", len({f.rsplit(".", 1)[1] for f in files}) >= 3)
    ok("input gate: a file of 25,000 rows or more", _rows(PK.FILES["coyle"]) >= 25000, str(_rows(PK.FILES["coyle"])))
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    ok("input gate: two distractors named in metadata.json and present", len(meta["distractor_files"]) >= 2 and
       all(f in files for f in meta["distractor_files"]))
    ok("distractors: deleting them leaves every graded figure", _without_distractors(meta) == _graded(P, AF))
    ok("no readme, dictionary, notes or manifest file or sheet", _no_describer())
    ok("realism: no id-like column steps by one constant (benchmarks, segments, sites)", _no_constant_steps(P, AF))
    ok("realism: Table 4's station-to-station falls vary (reach slopes, cross-sections, bridges)",
       _table4_irregular(P), str(_table4_irregular(P)))
    ok("realism: the 2024 crown shows low spots and steps (three or more shots 0.12 ft or more below their 1,000 ft "
       "running median)", _crown_low_spots(AF) >= 3, str(_crown_low_spots(AF)))
    ok("realism: the inspection report is a ratings table with no narrative paragraph",
       _inspection_is_table())
    ok("realism: reach point counts are not uniform", len(set(_reach_counts(AF).values())) >= 4,
       str(_reach_counts(AF)))
    ok("realism: personas are the card's (no other full name in the pack's documents)", _people_ok())
    ok("realism: every document's stated date follows the events it describes", _doc_dates_ok(P))
    ob, nb = A.hb_blocks(AF)
    ok("realism: no repeated stamp inside either logger's records or in the Coyle Bridge file; the two ORF2 loggers "
       "overlap only across the three days both ran", not AF.coy.duplicated(["datetime_utc"]).any() and
       not ob.duplicated(["stamp"]).any() and not nb.duplicated(["stamp"]).any() and
       (ob["t"].max() - nb["t"].min()) < pd.Timedelta(days=3))
    ok("PDF positive controls: every shipped PDF yields text through the shared extractor",
       all(len(IO.pdf_text(os.path.join(TARGET, f))) > 400 for f in files if f.endswith(".pdf")))
    ok("XLSX: the inventory's docProps name the issuing department", _xlsx_props_ok())

    bad = [r for r in RES if not r[1]]
    for name, passed, detail in RES:
        print("%s  %s%s" % ("PASS" if passed else "FAIL", name, ("  [" + detail + "]") if (detail and not passed)
                            else ""))
    print("%d assertions, %d failed" % (len(RES), len(bad)))
    sys.exit(1 if bad else 0)


# ------------------------------------------------------------------ helpers
def _settle_median(AF):
    off = A.station_offset(AF)[0][0]
    sh = A.datum_shift(AF)
    z24 = AF.c24[AF.c24.code == "CL"].set_index("sta")
    d = {}
    for _, r in AF.c16[AF.c16.DESC == "CL"].iterrows():
        s = int(r["sta"]) - off
        if s in z24.index:
            d.setdefault(z24.loc[s, "reach"], []).append(float(r["ELEV"]) + sh - float(z24.loc[s, "elev_ft"]))
    return {k: float(np.median(v)) for k, v in sorted(d.items())}


def _mean_of_reach_means(AF):
    off = A.station_offset(AF)[0][0]
    sh = A.datum_shift(AF)
    c24 = AF.c24[AF.c24.code == "CL"]
    c16 = AF.c16[AF.c16.DESC == "CL"].copy()
    c16["new"] = c16["sta"] - off
    reach = c24.set_index("sta")["reach"]
    c16 = c16[c16["new"].isin(reach.index)]
    c16["reach"] = c16["new"].map(reach)
    m24 = c24.groupby("reach")["elev_ft"].mean()
    m16 = c16.groupby("reach")["ELEV"].mean() + sh
    return {k: float(m16[k] - m24[k]) for k in m24.index}


def _one_to_one(AF):
    off = A.station_offset(AF)[0][0]
    s24 = set(AF.c24[AF.c24.code == "CL"]["sta"])
    s16 = set(int(s) - off for s in AF.c16[AF.c16.DESC == "CL"]["sta"] if int(s) - off >= 0)
    return s24 == s16


def _overlap_runner_up(AF):
    old, new = A.hb_blocks(AF)
    so = old.set_index("t")["stage"]
    sn = new.set_index("t")["stage"]
    out = []
    for s in range(-12, 13):
        if s == 6:
            continue
        x = sn.copy()
        x.index = x.index - pd.Timedelta(hours=s)
        common = so.index.intersection(x.index)
        if len(common) >= 24:
            out.append(float(np.mean(np.abs(so.loc[common].values - x.loc[common].values))))
    return min(out)


def _table4_irregular(P):
    d = np.diff(P.t4.values, axis=0)
    non_bridge = [i for i, s in enumerate(P.t4.index[1:]) if s not in (6240, 11870) and P.t4.index[i] not in (6240, 11870)]
    col = d[non_bridge, :]
    cv = float(np.std(col[:, 4]) / abs(np.mean(col[:, 4])))
    return round(cv, 3) if cv > 0.15 else False


def _crown_low_spots(AF):
    c = AF.c24[AF.c24.code == "CL"].sort_values("sta")
    med = c["elev_ft"].rolling(11, center=True, min_periods=5).median()
    return int(np.sum((med - c["elev_ft"]) >= 0.12))


def _inspection_is_table():
    t = IO.pdf_text(A._find(TARGET, r"inspection"))
    return "Rating" in t and "Minimally Acceptable" in t and "Overall rating" not in t and "Follow-up" not in t


def _cap_nofb(P, r):
    return min(A.q_at_wse(P, P.crown[s] + r, s) for s in P.t4.index)


def _crown_matches(P, AF):
    z = AF.c24.set_index(["sta", "code"])["elev_ft"]
    for s, v in P.crown.items():
        code = "MAIN ST CLOSURE" if s == 6240 else ("P&W RR CLOSURE" if s == 11870 else "CL")
        if abs(float(z[(s, code)]) - v) > 1e-9:
            return False
    return len(P.crown) == 21


def _projected_settlement(P, AF):
    st = A.settlement(AF)
    Q = copy.copy(P)
    Q.crown = {s: v - st[W.reach_of(s)] * 3 / 8 for s, v in P.crown.items()}
    return A.raise_for(Q, A.main_figures(P)["q_design"])


def _survey_reading(P, AF, q):
    """Crown at every 50 ft shot and structure, Table 4 water surface interpolated along the levee."""
    pts = AF.c24.groupby("sta")["elev_ft"].min()
    st = np.array(P.t4.index)
    qs = np.array(P.t4.columns, float)
    tab = P.t4.values

    def row(s):
        return np.array([np.interp(s, st, tab[:, j]) for j in range(len(qs))])

    def inv(zs, z):
        if z <= zs[0]:
            return qs[0] + (z - zs[0]) * (qs[1] - qs[0]) / (zs[1] - zs[0])
        if z >= zs[-1]:
            return qs[-1] + (z - zs[-1]) * (qs[-1] - qs[-2]) / (zs[-1] - zs[-2])
        return float(np.interp(z, zs, qs))
    rows = {s: row(s) for s in pts.index}
    need = max(float(np.interp(q, qs, rows[s])) + A.freeboard(P, s) - z for s, z in pts.items())
    rz = 0 if need <= 0 else int(math.ceil(need))
    f = A.main_figures(P)["fit"]
    out = []
    for r in A.RAISES:
        cap = min(inv(rows[s], z + r - A.freeboard(P, s)) for s, z in pts.items())
        out.append(round(100 * L.exceedance(f, cap), 1))
    return rz, out


def _loginterp(P, f):
    qs = np.log(np.array(P.t4.columns, float))
    out = []
    for r in A.RAISES:
        cap = min(math.exp(np.interp(P.crown[s] + r - A.freeboard(P, s), P.t4.loc[s].values, qs)) for s in P.t4.index)
        out.append(round(100 * L.exceedance(f, cap), 1))
    return out


def _calendar_year(P):
    df = P.peaks_df.copy()
    df["cy"] = df["peak_dt"].dt.year
    h = df[df.site_no == "05433000"].groupby("cy")["peak_va"].max()
    c = df[df.site_no == "05432100"].groupby("cy")["peak_va"].max()
    yrs = sorted(set(h.index) & set(c.index))
    T, U = h.reindex(yrs).values.astype(float), c.reindex(yrs).values.astype(float)
    post = np.array(yrs) >= 2009
    r = np.sum(T[post] * U[post]) / np.sum(U[post] ** 2)
    q = A.q_aep(np.where(post, T, r * U), P)
    return A.raise_for(P, q), rnd(q, 5000)


def _calendar_year_labels(P):
    """Every published row kept, labelled by the calendar year of its date; the cut taken on that label."""
    df = P.peaks_df.copy()
    h = df[df.site_no == "05433000"].sort_values("peak_dt")
    c = df[df.site_no == "05432100"].sort_values("peak_dt")
    T, U = h["peak_va"].values.astype(float), c["peak_va"].values.astype(float)
    post = h["peak_dt"].dt.year.values >= 2009
    r = np.sum(T[post] * U[post]) / np.sum(U[post] ** 2)
    q = A.q_aep(np.where(post, T, r * U), P)
    return A.raise_for(P, q), rnd(q, 5000)


def _cy_drops(P):
    df = P.peaks_df
    h = df[df.site_no == "05433000"]
    return len(h) - h["peak_dt"].dt.year.nunique()


def _drop(P, approval=None, code=None):
    df = P.peaks_df
    keep = np.ones(len(df), bool)
    if approval:
        keep &= df["approval"].values != approval
    if code:
        keep &= df["peak_cd"].fillna("").astype(str).values != code
    d = df[keep]
    h = d[d.site_no == "05433000"].set_index("wy")["peak_va"].astype(float)
    c = d[d.site_no == "05432100"].set_index("wy")["peak_va"].astype(float)
    yrs = sorted(set(h.index) | set(c.index))
    T, U = h.reindex(yrs).values, c.reindex(yrs).values
    post = np.array(yrs) >= 2009
    ok_ = ~np.isnan(T) & ~np.isnan(U)
    r = np.sum(T[post & ok_] * U[post & ok_]) / np.sum(U[post & ok_] ** 2)
    ser = np.where(post, T, r * U)
    ser = ser[~np.isnan(ser)]
    q = A.q_aep(ser, P)
    return A.raise_for(P, q), rnd(q, 5000)


def _station_skew_only(P, ser):
    f = A.fit(ser, P)
    f["gw"] = f["g"]
    return A.raise_for(P, L.quantile(f, P.aep))


def _small_flood_ratios(P):
    wy = np.array(P.hal.index)
    T, U = P.hal.values, P.coy.reindex(wy).values
    small = U < 46000
    pre = small & (wy < 1997)
    post = small & (wy >= 2009)
    a = np.median(T[pre] / U[pre])
    b = np.median(T[post] / U[post])
    return abs(a / b - 1)


def _repeats(x, n=14):
    s = [tuple(np.round(x[i:i + n], 6)) for i in range(len(x) - n + 1)]
    return len(s) != len(set(s))


def _sig3(v):
    v = int(v)
    s = str(v).rstrip("0")
    return len(s) <= 3


def _texts(only=None):
    out = {}
    for f in sorted(os.listdir(TARGET)):
        if only and not any(o in f for o in only):
            continue
        p = os.path.join(TARGET, f)
        if f.endswith(".pdf"):
            out[f] = IO.pdf_text(p)
        elif f.endswith(".xlsx"):
            z = zipfile.ZipFile(p)
            out[f] = " ".join(z.read(n).decode("utf-8", "ignore") for n in z.namelist() if n.endswith(".xml"))
        else:
            out[f] = open(p, encoding="utf-8").read()
    return out


def _pack_mentions(words, exclude=(), only=None):
    for f, t in _texts(only).items():
        if any(f.endswith(e) for e in exclude):
            continue
        low = t.lower()
        if any(w.lower() in low for w in words):
            return True
    return False


def _no_present_column():
    for f in os.listdir(TARGET):
        if f.endswith(".csv"):
            head = open(os.path.join(TARGET, f), encoding="utf-8").read(3000).lower()
            if "present" in head or "adjusted" in head or "ratio" in head:
                return False
    return True


def _main_files_clean():
    t = _texts(only=("annual_peaks", "LS-02", "Table4", "regional_skew", "levee_inventory"))
    joined = " ".join(t.values()).lower()
    hits = [w for w in ("gauge datum", "gage_ht", "time zone", "utc", "ngvd", "2016 survey", "old stationing")
            if w in joined]
    return not hits and len(t) == 5


def _no_gap_near(AF, lt):
    for t_h, h in lt:
        for df, col in ((AF.coy, "t"), (AF.hb, "t")):
            w = df[(df[col] > t_h - pd.Timedelta(days=5)) & (df[col] < t_h + pd.Timedelta(days=5))][col]
            if (w.diff().dropna() > pd.Timedelta(hours=1)).any():
                return False
    return True


def _coyle_max_matches(P, AF):
    c = AF.coy.copy()
    c["wy"] = [A.water_year(t) for t in c["t"]]
    mx = c.groupby("wy")["discharge_cfs"].max()
    return all(abs(mx[w] / P.coy[w] - 1) <= 0.01 for w in mx.index)


def _rows(name):
    with open(os.path.join(TARGET, name), encoding="utf-8") as fh:
        return sum(1 for line in fh if line and not line.startswith("#")) - 1


def _graded(P, AF):
    m = A.main_figures(P)
    return (m["raise"], m["q_design_5k"], [round(a, 1) for a in m["aep"]],
            {k: round(v, 2) for k, v in A.settlement(AF).items()}, [int(round(h)) for _, h in A.lead_times(AF)])


def _without_distractors(meta):
    tmp = tempfile.mkdtemp()
    for f in os.listdir(TARGET):
        if f not in meta["distractor_files"]:
            shutil.copy(os.path.join(TARGET, f), tmp)
    try:
        return _graded(A.Pack(tmp), A.AskFiles(tmp))
    finally:
        shutil.rmtree(tmp)


def _no_describer():
    for f in os.listdir(TARGET):
        if re.search(r"readme|dictionary|notes|manifest|codebook|schema", f, re.I):
            return False
    wbz = zipfile.ZipFile(os.path.join(TARGET, PK.FILES["inventory"]))
    wbx = wbz.read("xl/workbook.xml").decode()
    return not re.search(r'name="(Notes|README|Dictionary|About)', wbx, re.I)


def _no_constant_steps(P, AF):
    def const(vals):
        d = np.diff(sorted(vals))
        return len(d) >= 2 and len(set(d)) == 1
    bm = [int(re.sub(r"\D", "", b)) for b in AF.bench["benchmark"] if b.startswith("OL")]
    seg = [int(s[-2:]) for s in P.segments["Segment ID"]]
    sites = [int(s) for s in P.peaks_df["site_no"].unique()]
    return not const(bm) and not const(seg) and not const(sites)


def _reach_counts(AF):
    return AF.c24[AF.c24.code == "CL"].groupby("reach").size().to_dict()


def _people_ok():
    t = " ".join(_texts().values())
    authors = []
    for f in os.listdir(TARGET):
        if f.endswith(".pdf"):
            authors += [a.decode("latin-1") for a in re.findall(rb"/Author \((.*?)\)", open(os.path.join(TARGET, f),
                                                                                          "rb").read())]
    found = set(re.findall(r"\b(Dennis Zhang|Kristin Lucas|Eric Thornton|Jesus Hernandez)\b", t + " " +
                           " ".join(authors)))
    others = re.findall(r"\b(John Doe|Jane Doe|Acme)\b", t)
    return len(found) == 4 and all(a in PEOPLE for a in authors) and not others


def _doc_dates_ok(P):
    t4 = IO.pdf_text(A._find(TARGET, r"Table4"))
    m = re.findall(r"marks of the (\w+ \d{4}) and (\w+ \d{4}) floods", t4)
    if not m:
        return False
    for s in m[0]:
        if pd.Timestamp(s) >= pd.Timestamp("2019-12-01"):
            return False
    inv = A.Pack.__new__(A.Pack)
    seg = P.segments
    ins = [pd.Timestamp(str(x)) for x in seg["Last inspection"]]
    return max(ins) <= pd.Timestamp("2025-03-14")


def _xlsx_props_ok():
    z = zipfile.ZipFile(os.path.join(TARGET, PK.FILES["inventory"]))
    app = z.read("docProps/app.xml").decode()
    return "State Department of Natural Resources" in app


if __name__ == "__main__":
    main()
