"""submission.md from the golden figures."""


def fmt(n):
    return "{:,}".format(int(n))


def write(fig, fam, path):
    ub50 = "%.1f to %.1f ms" % (fam["ub50_lo"], fam["ub50_hi"])
    ub100 = "%.1f to %.1f ms" % (fam["ub100_lo"], fam["ub100_hi"])
    L = []
    L.append("## Tags\n")
    L.append("**Domain:** Biomedical & Clinical Research (dose-response and PK-PD modelling: the concentration-QTc "
             "relationship of an antimuscarinic from its single and multiple ascending dose studies, predicted at each "
             "phase 2b dose's high clinical exposure).")
    L.append("**Analytical objective:** Forecasting & Predictive Modeling.\n")
    L.append("## 1. Final Recommendation\n")
    L.append("**Take 50 mg once daily as the highest phase 2b dose: it is the highest dose whose predicted "
             "placebo-corrected QTcI change at its high clinical exposure (%s ng/mL) keeps the upper 90%% bound below "
             "10 ms, while 100 mg (%s ng/mL) breaches it and would need a dedicated QT study.** Not 100 mg: Fridericia's "
             "one-third exponent under-corrects the heart-rate rise VLT-317 causes and makes all three doses pass. Not "
             "25 mg: a single QT-RR line through each subject's whole drug-free day takes the night's longer QT for heart "
             "rate (mean exponent %.2f against %.2f within clock hour) and over-corrects.\n"
             % (fmt(fig["c_high_50"]), fmt(fig["c_high_100"]), fig["exp_pooled_mean"], fig["exp_hour_mean"]))
    L.append("## 2. Critical Components\n")
    L.append("1. High clinical exposure (Day 10 geometric mean Cmax in study 102 times the itraconazole Cmax ratio "
             "2.61): **%s ng/mL** at 25 mg, **%s ng/mL** at 50 mg and **%s ng/mL** at 100 mg."
             % (fmt(fig["c_high_25"]), fmt(fig["c_high_50"]), fmt(fig["c_high_100"])))
    L.append("2. Upper 90%% bound of the predicted placebo-corrected QTcI change below 10 ms: **25 mg yes, 50 mg yes "
             "(%s), 100 mg no (%s)**, under every fit that holds clock time fixed (one-hour, half-hour, two- and "
             "three-hour bins, cosinor)." % (ub50, ub100))
    L.append("3. Each subject's heart-rate exponent, fitted within clock hour on his drug-free Holter segments, averages "
             "**%.2f**; one line through the whole day gives %.2f.\n" % (fig["exp_hour_mean"], fig["exp_pooled_mean"]))
    L.append("## 3. Step-by-Step Solution\n")
    steps = [
        "Mapped holter_5min_segments_VLT317-101-102.txt recordings to subjects by the four-digit subject number in "
        "PatientID, moved SegmentStart_UTC to Brussels time and kept each subject's readable segments ending before "
        "his first dose (dosing_log_VLT317-101-102.csv).",
        "Fitted each subject's log QT on log RR with a separate level for every clock hour; the slope is his "
        "exponent b (plan section 3).",
        "Corrected every readable replicate in the two core-lab transfers (SCREENING_NO and SCRNO mapped to subjects "
        "through randomisation_unblinded_VLT317-101-102.xlsx; RR = 60,000/HR for study 102) as QT/RR^b, averaged each "
        "time point, and subtracted the same nominal time on Day -1.",
        "Paired each time point with its plasma sample (BLQ as zero, the diluted re-assay for results above range) "
        "and fitted the plan's mixed model by REML: treatment, concentration, nominal time and centred baseline QTcI, "
        "random intercept and concentration slope per subject.",
        "Took each phase 2b dose's Day 10 geometric mean Cmax in study 102 times 2.61 (VLT-317-103 synopsis) and "
        "predicted the treatment effect plus slope times that exposure with its two-sided 90% interval.",
        "For AUC, added each single-dose subject's late samples from ambulatory_lab_results_2026.csv (VOLUNTEER_NO "
        "to SCREENING_NO through screening_log_2026.csv, then to subject) and ran the plan's section 6 NCA.",
        "For night heart rate, gave each unlabelled Holter recording to the subject whose labelled recording ended "
        "within minutes of its first segment with beats, and averaged segments starting 00:00 to 06:00 local time.",
        "Recommended 50 mg: the highest dose whose bound stays below 10 ms.",
    ]
    for i, s in enumerate(steps, 1):
        L.append("%d. %s" % (i, s))
    L.append("")
    L.append("## 4. Deliverable Answers\n")
    L.append("### cqtc_dose_review.xlsx\n")
    L.append("1. Call: 50 mg once daily is the highest phase 2b dose that clears the 10 ms bound.")
    L.append("2. High clinical exposure, ng/mL, three significant figures, and whether the upper 90% bound stays "
             "below 10 ms:")
    for d in (25, 50, 100):
        L.append("   - %d mg: %s ng/mL, %s" % (d, fmt(fig["c_high_%d" % d]), fig["below10_%d" % d]))
    L.append("3. Geometric mean AUC0-inf after a single dose, ng.h/mL, two significant figures:")
    for d in (25, 50, 100, 200, 400):
        L.append("   - %d mg: %s" % (d, fmt(fig["auc_sad_%d" % d])))
    L.append("4. Change in mean heart rate over the segments starting 00:00 to 06:00 local time, night after the first "
             "dose against the night before, less the study's placebo change, bpm, one decimal:")
    for d in (25, 50, 100, 200, 400):
        L.append("   - VLT-317-101, %d mg: %+.1f" % (d, fig["night_hr_101_%d" % d]))
    for d in (25, 50, 100):
        L.append("   - VLT-317-102, %d mg: %+.1f" % (d, fig["night_hr_102_%d" % d]))
    L.append("")
    L.append("### cqtc_dose_memo.pdf\n")
    L.append("1. Call: 50 mg once daily; 100 mg breaches the 10 ms bound at its high clinical exposure.")
    L.append("2. Chart: placebo-adjusted change in QTcI against plasma concentration, with concentration-decile means, "
             "the model line and its 90%% band, the 10 ms line and a marker at each dose's high clinical exposure "
             "(%s, %s and %s ng/mL)." % (fmt(fig["c_high_25"]), fmt(fig["c_high_50"]), fmt(fig["c_high_100"])))
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
