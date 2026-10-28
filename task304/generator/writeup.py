"""submission.md, drafted from figures.json: every figure in it is read from there."""
import golden as GD
import params as P

NAME = {"AP": "the approved premises", "HH": "the city hostels", "DS": "Fenwold Recovery's new entrants",
        "NSP": "the needle exchange pharmacies' new registrants"}
SHORT = GD.SHORT
HALF = GD.HALF


def write(path, F):
    o = F["order"]
    a10, s10 = F["active10"], F["starts10"]
    L = []
    L.append("## Tags\n")
    L.append("**Domain:** Epidemiology & Public Health (screening and diagnostic policy evaluation: a hepatitis C "
             "find-and-treat programme placed and sized by the people it starts on treatment).")
    L.append("**Analytical objective:** Opportunity Sizing & Decision Support.\n")
    L.append("## 1. Final Recommendation\n")
    L.append("**The van should work the needle exchange pharmacies' new registrants in 2027, where it would start "
             "about %d people on hepatitis C treatment, %d more than at Fenwold Recovery's new entrants (about %d).**"
             % (s10[o[0]], F["gap10"], s10[o[1]]))
    L.append("Not the approved premises, where a quarter of arrivals test antibody positive: more than half of those "
             "positives had been cured inside prison by Corvane Health before they arrived, and the van would start "
             "about %d there. Not Fenwold Recovery's new entrants, the largest intake: nearly half of their positives "
             "had already been cured by the network's clinics. Not the city hostels, about %d."
             % (s10["AP"], s10["HH"]))
    L.append("\n## 2. Critical Components\n")
    L.append("1. The van's rates from the 2018-19 pilot: it tested **%.2f** of arrivals and started **%.2f** of the "
             "people with RNA detected within twelve weeks" % (F["test_share"], F["start_share"]))
    L.append("2. Approved premises arrivals the peer team found antibody positive who had been cured inside prison "
             "before they arrived, on Corvane's workbook and not the network's register: **more than half**")
    L.append("3. People started on treatment in 2027: **needle exchange registrants %d**, Fenwold Recovery new "
             "entrants %d" % (s10["NSP"], s10["DS"]))
    L.append("\n## 3. Step-by-Step Solution\n")
    L.append("1. Counted each setting's distinct arrivals in each plan year (October to September) in "
             "setting_arrivals_2023-10_to_2026-09.csv and averaged the two years to 30 September 2026, as the van "
             "plan counts a year's arrivals.")
    L.append("2. From van_pilot_2018-19_caseload.csv took the share of arrivals the van tested (%d of %s) and the "
             "share of people with RNA detected who started within twelve weeks of the test (%d of %s)."
             % (F["pilot_tested"], "{:,}".format(F["pilot_arrived"]), F["pilot_started12"], F["pilot_detected"]))
    L.append("3. Matched each valid test in peer_testing_log_2024-10_to_2026-09.csv to its person's arrival in the "
             "two years (by pseudonym, the test within 60 days of the arrival) and took each setting's share "
             "reactive.")
    L.append("4. For each reactive arrival read the records before the test: a course with a twelve-week result not "
             "detected in hcv_treatment_register_2015-2026.csv or corvane_hcv_courses_2017-2026.xlsx counts as cured "
             "and inactive unless a later RNA test before the peer test detected it; a course running at the test "
             "counts as neither found nor started; "
             "otherwise the latest RNA result (virology_hcv_results_2015-01_to_2026-09.csv or the workbook's "
             "reception tests) decides; with no record the person counts at the first-positive share %.2f."
             % F["lab_ratio"])
    L.append("5. Multiplied each setting's arrivals by the test share, the reactive share and the mean of step 4 for "
             "active infections, then by the start share for people started: needle exchange registrants %d, "
             "Fenwold Recovery new entrants %d, city hostels %d, approved premises %d."
             % (s10["NSP"], s10["DS"], s10["HH"], s10["AP"]))
    L.append("6. Clinic outcomes: a course in hcv_treatment_register_2015-2026.csv ended on its last dose (the "
             "planned end, or the date it stopped, as the pathway puts it) in the half-year, and is a confirmed cure "
             "when its keyed twelve-week result is not detected or, where none is keyed, the first Fenwold Pathology "
             "RNA test taken twelve weeks or more after the last dose is not detected, read under every pseudonym "
             "Fenwold Pathology holds for the same patient (its lims_patient_id).")
    L.append("7. Placed the van with the needle exchange pharmacies' new registrants, %d starts against %d."
             % (s10[o[0]], s10[o[1]]))
    L.append("\n## 4. Deliverable Answers\n")
    L.append("### %s\n" % GD.DOCX)
    L.append("1. The van's setting: the needle exchange pharmacies' new registrants, about %d people started on "
             "treatment in 2027." % s10[o[0]])
    L.append("2. People with an active infection the van would find in 2027:")
    for s in P.SETTINGS:
        L.append("   - %s: %d" % (SHORT[s], a10[s]))
    L.append("3. People it would start on treatment in 2027:")
    for s in P.SETTINGS:
        L.append("   - %s: %d" % (SHORT[s], s10[s]))
    L.append("4. A horizontal bar chart of the people each setting would start, largest first, the needle exchange "
             "registrants' bar marked \"Van, 2027\".")
    L.append("\n### %s\n" % GD.XLSX)
    L.append("1. Confirmed cures among the courses each clinic ended, by half-year:")
    for c in P.CLINICS:
        for h in (1, 2):
            x = F["AH"]["%s_%d" % (c, h)]
            L.append("   - %s, %s: %d" % (P.CLINIC_LABEL[c][0].upper() + P.CLINIC_LABEL[c][1:], HALF[h],
                                          x["confirmed"]))
    open(path, "w", encoding="utf-8").write("\n".join(L) + "\n")
