"""task122: write submission.md from generator/figures.json (every figure emitted, never typed).

    python3 task122/generator/writeup.py
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
ARMS = ["Placebo", "5 mg", "10 mg", "20 mg", "40 mg"]
DOSES = ARMS[1:]


def sgn(v):
    return "%d" % v if v <= 0 else "%d" % v


def main():
    f = json.load(open(os.path.join(HERE, "figures.json")))
    dd = f["diff36"]
    a = f["asks"]
    e, lp = f["eased"], f["loop"]
    L = []
    L.append("# task122 submission\n")
    L.append("## Tags\n")
    L.append("**Domain:** Biomedical & Clinical Research (longitudinal outcomes with repeated measures: reading a "
             "52-week phase 2b dose-ranging trial's eGFR record for each dose's effect against placebo over a "
             "36-month phase 3).")
    L.append("**Analytical objective:** Experiment & Causal Analysis (which VMK-4410 dose goes into the phase 3, judged "
             "by each dose's eGFR difference from placebo after 36 months' treatment).\n")
    L.append("## 1. Final Recommendation\n")
    L.append("**Take VMK-4410 20 mg into the phase 3: after 36 months' treatment eGFR would be %d mL/min/1.73 m2 higher "
             "on it than on placebo.**\n" % dd["20 mg"])
    L.append("Not 40 mg (%d), which has the largest early fall and only looks best when the one-off recovery after "
             "background diuretics were eased is read as a slope; not 10 mg (%d), which leads on the week-52 "
             "difference alone; not 5 mg (%d).\n" % (dd["40 mg"], dd["10 mg"], dd["5 mg"]))
    L.append("## 2. Critical Components\n")
    L.append("1. The chronic phase of the eGFR response starts at **week 24**: on 20 and 40 mg the difference from "
             "placebo rises from week 12 to week 24, as patients whose loop diuretic was eased from the week-12 visit "
             "recover part of the early fall, and is a straight line from week 24 to week 52")
    L.append("2. At month 36, 20 mg leads the runner-up, 40 mg, by **%d** mL/min/1.73 m2\n" % f["gap36"])
    L.append("## 3. Step-by-Step Solution\n")
    L.append("1. Took every randomised patient by randomised arm from dm.csv and each patient's first and last dose from "
             "ex.csv; a patient whose last dose came before the week-52 visit in sv.csv, or who left the study, stopped "
             "study drug for good.")
    L.append("2. From lb.csv took the central laboratory's CKD-EPI 2021 eGFR at the scheduled visits (the first sample "
             "of a visit, as section 2 of VMK-4410-202_SAP_v2.0.pdf sets out), baseline the mean of the screening and "
             "day-1 values, and set aside values from samples taken after the last dose of a patient who stopped for "
             "good, as the estimand in VMK-4410-301_synopsis_draft_v0.3.pdf files it.")
    L.append("3. Took each arm's mean change from baseline at each visit less placebo's.")
    L.append("4. In cm.csv, loop diuretic doses were reduced or stopped at the week-12, 16 and 20 visits in most "
             "loop-diuretic patients on 40 mg, many on 20 mg and almost none on placebo, as section 6 of "
             "VMK-4410-202_protocol_v3.0.pdf allows from week 12; the 40 mg difference rises %.1f mL/min/1.73 m2 from "
             "week 12 to week 24 and is linear after it." % f["rise_12_24"]["40 mg"])
    L.append("5. Fitted a straight line through each dose's differences at weeks 24, 32, 40 and 52 and read it at week "
             "156: 20 mg %d, 40 mg %d, 10 mg %d, 5 mg %d mL/min/1.73 m2." % (dd["20 mg"], dd["40 mg"], dd["10 mg"], dd["5 mg"]))
    L.append("6. For the tables: serum potassium from every laboratory in lb.csv after the first dose to the last; "
             "hyperkalaemia events in ae.csv by group identifier on the SAP's two preferred terms, onset imputed by the "
             "SAP's rule; stopping and days on drug from ex.csv, each dosed day counted once, before the sv.csv week-52 "
             "visit.")
    L.append("7. Recommendation: VMK-4410 20 mg, %d mL/min/1.73 m2 above placebo at month 36.\n" % dd["20 mg"])
    L.append("## 4. Deliverable Answers\n")
    L.append("### VMK-4410_phase3_dose_recommendation.pdf\n")
    L.append("1. The call: take VMK-4410 20 mg into the phase 3.")
    L.append("2. eGFR difference from placebo after 36 months' treatment, nearest whole mL/min/1.73 m2:")
    for d in DOSES:
        L.append("   - %s: %s" % (d, sgn(dd[d])))
    L.append("3. Chart of each dose's eGFR difference from placebo by month to month 36: the phase 2b visits to week 52 "
             "and each dose's chronic-phase line from week 24 carried to month 36, the month-36 values labelled.\n")
    L.append("### VMK-4410_phase2b_tables.xlsx\n")
    L.append("1. Patients with a serum potassium above 5.5 mmol/L on treatment:")
    for x in ARMS:
        L.append("   - %s: %d" % (x, a["potassium_above_5_5_patients"][x]))
    L.append("2. Hyperkalaemia adverse events that began on treatment:")
    for x in ARMS:
        L.append("   - %s: %d" % (x, a["hyperkalaemia_events_began_on_treatment"][x]))
    L.append("3. Patients who stopped study drug for good before their week-52 visit:")
    for x in ARMS:
        L.append("   - %s: %d" % (x, a["stopped_for_good_before_week52"][x]))
    L.append("4. The arm's total years on study drug before the week-52 visit, one decimal:")
    for x in ARMS:
        L.append("   - %s: %.1f" % (x, a["years_on_drug_before_week52"][x]))
    with open(os.path.join(TASK, "submission.md"), "w") as fh:
        fh.write("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
