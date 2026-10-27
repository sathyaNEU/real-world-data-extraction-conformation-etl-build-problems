"""submission.md from generator/figures.json: the five blocks, every figure taken from the generator's own output."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import common as K  # noqa: E402


def main():
    f = json.load(open(os.path.join(HERE, "figures.json")))
    fc = {d: f["forecast.%d_mg_pct" % d] for d in K.DOSES}
    A = lambda arm, k: f["askA.%s.%s" % (arm, k)]
    B = lambda arm, w: f["askB.%s.week%d.te_ada_pct" % (arm, w)]
    C = lambda arm, w: f["askC.%s.week%d.symptomatic_remission_patients" % (arm, w)]
    out = ["## Tags", "",
           "**Domain:** Pharmacology, Pharmacoepidemiology & Safety, population pharmacokinetics and exposure-response "
           "(a phase 3 induction dose for an anti-IL-23 antibody in ulcerative colitis, forecast from the exposure-response "
           "of the one dose a phase 2b trial tested, under the sponsor's dose-selection charter).",
           "**Analytical objective:** Forecasting & Predictive Modeling.", "",
           "## 1. Final Recommendation", "",
           "**Corvane should carry dovikizumab %d mg IV at weeks 0, 4 and 8 into phase 3.**" % f["call.dose_mg"],
           "The forecast week-12 clinical remission rate is %.1f per cent at 300 mg, %.1f at 600 mg and %.1f at 900 mg, so "
           "300 mg is %.1f points under the highest forecast, inside the charter's 5 points, and the lowest candidate "
           "there. The forecast rests on the week-4 pre-dose concentration, which the dose sets before healing begins: "
           "remitters and non-remitters had the same week-4 concentrations, and only later, as the colitis healed and "
           "clearance fell, did remitters' concentrations pull ahead, so an exposure-response on the later concentrations "
           "is steep because of the remission it is meant to predict and files 900 mg." % (
               fc[300], fc[600], fc[900], f["below_highest.300_mg_points"]),
           "", "## 2. Critical Components", "",
           "1. Remitters' to non-remitters' geometric mean concentration among the dovikizumab patients with a valid "
           "sample at the visit (pre-dose samples drawn after the infusion started set aside at every visit, SAP 6.8): "
           "**%.2f** before the week-4 infusion, **%.2f** before the week-8 infusion and **%.2f** at week 12." % (
               f["gmr.remitters_to_nonremitters.week4"], f["gmr.remitters_to_nonremitters.week8"],
               f["gmr.remitters_to_nonremitters.week12"]),
           "2. On the week-4 pre-dose concentration, week-12 remission is flat across exposure (quartiles %d, %d, %d and "
           "%d per cent), so every candidate dose forecasts about the same remission: **300 mg within %.2f points of the "
           "highest forecast** under every model on that concentration, with or without the randomisation stratum and "
           "baseline weight and modified Mayo score." % (tuple(f["quartile.%d.remission_pct" % j] for j in (1, 2, 3, 4)) +
                                                          (f["standing.widest_gap_300_mg_points"],)),
           "3. The exposure-response analysis set is the **%d** of %d dovikizumab patients with a valid week-4 pre-dose "
           "concentration; in that arm **%d** week-4 and %d week-8 pre-dose samples drawn after the infusion had started "
           "(laboratory UTC against the site's local start) are not pre-dose samples (SAP 6.8)." % (
               f["analysis_set.patients"], f["arm.dovikizumab_patients"], f["predose.after_start.week4_dovikizumab"],
               f["predose.after_start.week8_dovikizumab"]),
           "", "## 3. Step-by-Step Solution", "",
           "1. Joined cvn2184_201_randomisation_log.csv (randomisation to site-subject numbers and arms), "
           "cvn2184_201_serum_concentrations.csv (reportable results, ng/mL results divided by 1,000, below-limit results as "
           "below 0.100 ug/mL), cvn2184_201_infusion_records.csv and cvn2184_201_site_list.csv (the site's country for its "
           "summer time) to the week-12 remission flag in cvn2184_201_efficacy_database_lock.csv.",
           "2. Set aside each pre-dose sample whose UTC collection time was at or after the infusion's local start "
           "converted to UTC (SAP 6.8).",
           "3. Compared remitters' and non-remitters' concentrations at weeks 4, 8 and 12 (geometric means): equal at week "
           "4, apart after, as clearance falls with healing.",
           "4. Fitted week-12 remission (logistic) on the log week-4 pre-dose concentration with the randomisation stratum, "
           "scaled each patient's concentration by dose over 600 (investigator's brochure 5.2) and averaged the predicted "
           "remission over the exposure-response analysis set (charter 4).",
           "5. Applied the charter's rule (charter 5): the lowest dose whose forecast is no more than 5 points below the "
           "highest, compared unrounded.",
           "6. For safety, rebuilt each adverse event from cvn2184_201_adverse_events.csv by chaining a patient's records "
           "of one preferred term from review to review while ongoing, taking the onset entered at the latest review (an "
           "onset first entered as the visit or admission date is corrected there) and serious if any record is; then "
           "SAP 6.2 to 6.6 against the infusion dates and each patient's last visit in cvn2184_201_visit_dates.csv.",
           "7. For immunogenicity, rebuilt each draw as the patient's samples on one collection date in "
           "cvn2184_201_ada_results.csv (the backup aliquot's tube arrives on a manifest reading Unscheduled), took each "
           "tier's latest result in a run brightwater_ada_run_log.csv accepts, and applied SAP 6.7 against the baseline draw.",
           "8. For the e-diary, gave each entry to the registration holding the handset on its diary date "
           "(cvn2184_201_ediary_handset_log.csv), traced a registration the randomisation log does not know to the patient "
           "who handed that handset over the same day (the four closed sites' patients), took the last entry for each "
           "date and applied SAP 6.10 at days 43, 57 and 71.",
           "", "## 4. Deliverable Answers", "",
           "### %s" % K.MEMO, "",
           "1. Phase 3 induction dose: %d mg IV at weeks 0, 4 and 8." % f["call.dose_mg"],
           "2. Forecast week-12 clinical remission: 300 mg %.1f per cent, 600 mg %.1f per cent, 900 mg %.1f per cent "
           "(300 mg %.1f points below the highest)." % (fc[300], fc[600], fc[900], f["below_highest.300_mg_points"]),
           "", "### %s" % K.TABLES, "",
           "1. Patients with at least one treatment-emergent serious infection: dovikizumab %d, placebo %d." % (
               A("dovikizumab", "patients_serious_infection"), A("placebo", "patients_serious_infection")),
           "2. Patients with at least one infusion-related reaction: dovikizumab %d, placebo %d." % (
               A("dovikizumab", "patients_infusion_reaction"), A("placebo", "patients_infusion_reaction")),
           "3. Serious infections per 100 patient-years: dovikizumab %.1f, placebo %.1f." % (
               A("dovikizumab", "serious_infections_per_100py"), A("placebo", "serious_infections_per_100py")),
           "4. Treatment-emergent ADA incidence, per cent: dovikizumab week 4 %.1f, week 8 %.1f, week 12 %.1f; placebo "
           "week 4 %.1f, week 8 %.1f, week 12 %.1f." % (B("dovikizumab", 4), B("dovikizumab", 8), B("dovikizumab", 12),
                                                        B("placebo", 4), B("placebo", 8), B("placebo", 12)),
           "5. Patients in symptomatic remission on the e-diary: dovikizumab week 6 %d, week 8 %d, week 10 %d; placebo "
           "week 6 %d, week 8 %d, week 10 %d." % (C("dovikizumab", 6), C("dovikizumab", 8), C("dovikizumab", 10),
                                                  C("placebo", 6), C("placebo", 8), C("placebo", 10)),
           "", "### %s" % K.CHART, "",
           "1. Week-12 remission by quartile of the week-4 pre-dose concentration, flat, with the three dose forecasts; "
           "beside it the remitter to non-remitter concentration ratio rising from %.2f at week 4 to %.2f at week 12." % (
               f["gmr.remitters_to_nonremitters.week4"], f["gmr.remitters_to_nonremitters.week12"]),
           ""]
    s = "\n".join(out)
    assert "—" not in s and "–" not in s
    open(os.path.join(TASK, "submission.md"), "w").write(s)


if __name__ == "__main__":
    main()
