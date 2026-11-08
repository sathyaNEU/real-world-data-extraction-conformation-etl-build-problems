"""task306 submission.md, written from the golden figures (every figure emitted, none typed)."""
import golden as GD


def _n(x):
    return "{:,}".format(x)


def write(fig, path):
    rv, pl = fig["reviews"], fig["pilot"]
    c, r2, r3 = fig["call"], fig["runner_up"], fig["third"]
    L, N = GD.LETTER, GD.NAME
    nets = GD.NETS
    out = []
    out.append("## Tags\n")
    out.append("**Domain:** Pharmacology, Pharmacoepidemiology & Safety (benefit-risk assessment: a GP federation "
               "choosing the deprescribing review its pharmacist team runs, by the serious harm each would avoid).")
    out.append("**Analytical objective:** Opportunity Sizing & Decision Support.\n")
    out.append("## 1. Final Recommendation\n")
    out.append("**Run review %s, %s: it would take about %s patients off their medicine and avoid about %d serious "
               "harms a year, %d more than review %s, %s, the runner-up at %d.** Not review %s, %s: its pilot off rate "
               "is the highest (%.1f per cent), but a specialist service started %d per cent of its patients in scope "
               "and the pilot took only %d of %d such patients off, so it avoids about %d. Not review %s as the "
               "first choice: it takes the most patients off (about %s), but its medicines carry the least harm per "
               "patient-year."
               % (L[c], N[c], _n(rv[c]["off_10"]), rv[c]["harms_1"], fig["gap"], L[r2], N[r2], rv[r2]["harms_1"],
                  L[r3], N[r3], pl[r3]["all"]["pct"], rv[r3]["specialist_pct"], pl["specialist_all"]["off"],
                  pl["specialist_all"]["n"], rv[r3]["harms_1"], L[r2], _n(rv[r2]["off_10"])))
    out.append("\n## 2. Critical Components\n")
    out.append("1. Patients in scope on 31 December 2026: A **%s**, B **%s**, C **%s**."
               % (_n(rv["AP"]["in_scope"]), _n(rv["BZ"]["in_scope"]), _n(rv["GB"]["in_scope"])))
    out.append("2. Pilot patients off at six months, medicine started by the practice: A **%d of %d**, B **%d of %d**, "
               "C **%d of %d**; started by a specialist service: A **%d of %d**, B **%d of %d**, C **%d of %d**."
               % tuple(sum(([pl[k]["practice"]["off"], pl[k]["practice"]["n"]] for k in ("AP", "BZ", "GB")), []) +
                       sum(([pl[k]["specialist"]["off"], pl[k]["specialist"]["n"]] for k in ("AP", "BZ", "GB")), [])))
    out.append("3. Patients in scope whose medicine a specialist service started: A **%d%%**, B **%d%%**, C **%d%%**."
               % (rv["AP"]["specialist_pct"], rv["BZ"]["specialist_pct"], rv["GB"]["specialist_pct"]))
    out.append("4. Patients off at six months and serious harms avoided a year: A **about %s** and **%d**, B **about "
               "%s** and **%d**, C **about %s** and **%d**."
               % (_n(rv["AP"]["off_10"]), rv["AP"]["harms_1"], _n(rv["BZ"]["off_10"]), rv["BZ"]["harms_1"],
                  _n(rv["GB"]["off_10"]), rv["GB"]["harms_1"]))
    out.append("\n## 3. Step-by-Step Solution\n")
    out.append("1. Ran protocols A, B and C (deprescribing_review_protocols_2026.pdf) on 31 December 2026 over "
               "prescribing_issues_2025-07_2026-12.parquet, problem_list_extract_2026-12-31.csv and "
               "patient_registrations_2020-2026.parquet for patients registered outside the Clun Valley network "
               "(programme specification, section 3): %s, %s and %s patients in scope."
               % (_n(rv["AP"]["in_scope"]), _n(rv["BZ"]["in_scope"]), _n(rv["GB"]["in_scope"])))
    out.append("2. Marked a patient's medicine as started by a specialist service when trust_medicine_letters_feed_2019-"
               "2026.csv (patients without a pseudonym resolved through trust_hospital_number_lookup.csv) holds a "
               "letter naming a medicine of the review's class dated in the %d days before the first issue of the "
               "patient's earliest course of that class in repeat_medication_courses_2026-12-31.csv: %d%%, %d%% and "
               "%d%% of patients in scope." % (fig["constants"]["window_days"], rv["AP"]["specialist_pct"],
                                               rv["BZ"]["specialist_pct"], rv["GB"]["specialist_pct"]))
    out.append("3. Split the six-month rows of deprescribing_pilot_outcome_log_2026.csv the same way: practice-started "
               "%d of %d, %d of %d and %d of %d off; specialist-started %d of %d, %d of %d and %d of %d."
               % tuple(sum(([pl[k]["practice"]["off"], pl[k]["practice"]["n"]] for k in ("AP", "BZ", "GB")), []) +
                       sum(([pl[k]["specialist"]["off"], pl[k]["specialist"]["n"]] for k in ("AP", "BZ", "GB")), [])))
    out.append("4. Gave each patient in scope the pilot rate for their review and way of starting, times the table 1 "
               "harm rate at their age on 31 December 2026, and summed (programme specification, section 3): about %s, %s and %s "
               "patients off; %d, %d and %d serious harms a year."
               % (_n(rv["AP"]["off_10"]), _n(rv["BZ"]["off_10"]), _n(rv["GB"]["off_10"]), rv["AP"]["harms_1"],
                  rv["BZ"]["harms_1"], rv["GB"]["harms_1"]))
    out.append("5. Recommended review %s, %d harms a year ahead of review %s." % (L[c], fig["gap"], L[r2]))
    out.append("6. Letters: one per letter reference in the feed, a Marches Mental Health letter dated 7 April 2026 with "
               "the same patient, service, encounter date and lines as an earlier letter counted as that letter; each "
               "letter's half and practice from its first receipt in practice_document_workflow_2026.csv "
               "(programme specification, section 4), found by its sender reference or, for a Wrekinside letter "
               "with none there (GP Connect from October 2026), as the first Wrekinside receipt for the same patient "
               "that carries no letter's reference, was received on or within %d days after the letter date and was "
               "not taken by an earlier letter, a letter with no receipt by the 6 January 2027 extract not received "
               "in 2026; the receiving practice's network; per 1,000 on registered_list_sizes_2026.csv at 1 January "
               "and 1 July." % fig["constants"]["gp_days"])
    out.append("7. Consultations: attended one-to-one rows of pharmacist_hub_appointments_2026.csv (UTC to UK time), "
               "the rows of clinical_system_pharmacist_activity_2026.csv except each hub appointment's record by the "
               "same pharmacist for the same patient on the day or the next working day, and each attended patient in "
               "hub_group_session_register_2026.xlsx (programme specification, section 4); the network of the patient's practice "
               "on the day; per 1,000 on the list at the start of the quarter.")
    out.append("\n## 4. Deliverable Answers\n")
    out.append("### %s\n" % GD.PAPER)
    out.append("1. Recommendation: run review %s, %s." % (L[c], N[c]))
    out.append("2. Runner-up: review %s, %s." % (L[r2], N[r2]))
    out.append("3. Gap: %d serious harms a year." % fig["gap"])
    out.append("4. Patients off their medicine at six months, nearest 10:")
    for k in ("AP", "BZ", "GB"):
        out.append("   - Review %s: %s" % (L[k], _n(rv[k]["off_10"])))
    out.append("5. Serious harms avoided a year, whole numbers:")
    for k in ("AP", "BZ", "GB"):
        out.append("   - Review %s: %d" % (L[k], rv[k]["harms_1"]))
    out.append("6. Chart (figure 1): each review's patients off at six months beside the serious harms avoided a year, "
               "review %s highlighted." % L[c])
    out.append("7. Hospital medicine letters received per 1,000 registered patients, one decimal:")
    for n_ in nets:
        out.append("   - %s: January to June %.1f, July to December %.1f"
                   % (n_, fig["letters"][n_]["H1"]["rate"], fig["letters"][n_]["H2"]["rate"]))
    out.append("\n### %s\n" % GD.CSV)
    out.append("1. Patient consultations per 1,000 registered patients, one decimal:")
    for n_ in nets:
        x = fig["consultations"][n_]
        out.append("   - %s: Q1 %.1f, Q2 %.1f, Q3 %.1f, Q4 %.1f"
                   % (n_, x["Q1"]["rate"], x["Q2"]["rate"], x["Q3"]["rate"], x["Q4"]["rate"]))
    open(path, "w").write("\n".join(out) + "\n")
