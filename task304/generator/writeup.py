"""submission.md, every figure read from the figures dict that make.py also writes to figures.json."""
import params as P

HALF = {"H1": "October 2024 to March 2025", "H2": "April to September 2025"}


def write(path, F):
    s10, f10, R = F["starts10"], F["found10"], F["rates"]
    L = ["## Tags", "",
         "**Domain:** Epidemiology & Public Health (screening and diagnostic policy evaluation: a hepatitis C "
         "find-and-treat van placed and sized by the people it starts on treatment).",
         "**Analytical objective:** Opportunity Sizing & Decision Support.", "",
         "## 1. Final Recommendation", "",
         "**The van should work with Fenwold Recovery's new entrants in 2027, where it would start about %d people on "
         "hepatitis C treatment, %d more than at the needle exchange pharmacies' new registrants.**" % (s10["DS"], F["gap10"]),
         "Not the needle exchange registrants, where the van found the most infections per test in 2026: pharmacist "
         "test and treat reaches every needle exchange pharmacy on 1 April 2027, and at the three pharmacies already "
         "running it the van found %d in %d tests. Not the city hostels, where the van had already tested %d of the %d "
         "residents in 2026, so it would start about %d. Not the approved premises, at about %d."
         % (F["pilot_found"], F["pilot_tested"], F["hh_tested"], F["census"], s10["HH"], s10["AP"]), "",
         "## 2. Critical Components", "",
         "1. The van's 2026 yield per test at the three needle exchange pharmacies running pharmacist test and treat, "
         "the rate every pharmacy carries from April 2027: **%s**, against %s at the other 21"
         % (F["F_pilot"], F["F_nonpilot"]),
         "2. City hostel residents on the 30 September 2026 lists the van had already tested in 2026: **%d of %d**, "
         "leaving %d untested" % (F["hh_tested"], F["census"], F["hh_untested"]),
         "3. People started on treatment in 2027: **Fenwold Recovery new entrants %d**, needle exchange new registrants "
         "%d, city hostels %d, approved premises %d" % (s10["DS"], s10["NSP"], s10["HH"], s10["AP"]), "",
         "## 3. Step-by-Step Solution", "",
         "1. From van_tests_2026-01_to_2026-09.csv, each contact_ref once, took each setting's share of people offered who took a test and the found per test, and from "
         "hcv_treatment_register_2015-2026.csv the share of people found by 8 July 2026 who started within 84 days: "
         "approved premises %s, %s, %s; hostels %s, %s, %s; Recovery hub %s, %s, %s; pharmacies %s, %s, %s."
         % tuple(R[s][k] for s in ("AP", "HH", "DS", "NSP") for k in ("A", "F", "ST")),
         ("2. Sized each 2027 pool as the plan's section 5 sets it: approved premises %d residents and %d arrivals "
         "(approved_premises_returns_2023-10_to_2026-09.csv), hostels %d residents on hostel_residents_2026-09-30.xlsx and "
         "%d arrivals (hostel_occupancy_returns_2023-10_to_2026-09.csv), {:,} new treatment episodes "
         "(fenwold_recovery_new_episodes_2023-10_to_2026-09.csv) and {:,} first registrations, each "
         "client_code's earliest row in nsp_registrations_2019-04_to_2026-09.csv."
         % (F["ap_residents"], F["ap_arrivals"], F["census"], F["hh_arrivals"])).format(F["ds_arrivals"], F["nsp_regs"]),
         "3. Pharmacies: fenwold_icb_commissioning_intentions_2027-28.pdf (PH-12) puts test and treat at every needle "
         "exchange pharmacy from 1 April 2027; the register's pharmacist-prescribed courses show FW318, FK207 and FN562 "
         "doing it since 2025, where the van found %d of %d tested; January to March 2027 at each pharmacy's own 2026 "
         "rate and April to December at those three's gives %s people found." % (F["pilot_found"], F["pilot_tested"],
                                                                               F["found"]["NSP"]),
         ("4. Hostels: joined the residents lists to the van's 2026 tests by pseudonym, %d of %d tested (%d of them "
         "found); the %d untested and the %d arrivals at the 2026 found per test, and the %d who tested negative at the "
         "homeless health clinic's new infections per person-year in virology_hcv_results_2015-01_to_2026-09.csv, %d "
         "in {:,}, gives %s people found." % (F["hh_tested"], F["census"], F["hh_found"], F["hh_untested"],
                                            F["hh_arrivals"], F["hh_negative"], F["inc_events"],
                                            F["found"]["HH"])).format(F["inc_py"]),
         "5. Multiplied each setting's people found by its start share: Recovery new entrants %s, pharmacies %s, "
         "hostels %s, approved premises %s people started." % (F["starts"]["DS"], F["starts"]["NSP"],
                                                                F["starts"]["HH"], F["starts"]["AP"]),
         "6. Cures: took each course's last dose as its last pack in daa_dispensing_2024-04_to_2026-09.csv plus %d "
         "days (the register's end_date is the course's planned end), followed a course open at the 1 October "
         "2024 go-live through migrated_from as one course, and counted a confirmed cure where an RNA result Not "
         "detected sits 84 days or more after that last dose and before any later course, per the pathway's section 3: "
         "the ten counts in block 4." % F["pack_tail"],
         "7. Placed the van with Fenwold Recovery's new entrants, %d people started against %d." % (s10["DS"], s10["NSP"]),
         "", "## 4. Deliverable Answers", "", "### van_2027_trustee_paper.docx", "",
         "1. Setting for 2027: Fenwold Recovery's new entrants",
         "2. People with an active infection the van would find in 2027, nearest 10: approved premises %d; city hostels "
         "%d; Fenwold Recovery's new entrants %d; needle exchange pharmacies' new registrants %d"
         % (f10["AP"], f10["HH"], f10["DS"], f10["NSP"]),
         "3. People the van would start on treatment in 2027, nearest 10: approved premises %d; city hostels %d; "
         "Fenwold Recovery's new entrants %d; needle exchange pharmacies' new registrants %d"
         % (s10["AP"], s10["HH"], s10["DS"], s10["NSP"]),
         "4. Bar chart of the four settings' 2027 starts on page 1, Fenwold Recovery's new entrants marked in blue as "
         "the setting chosen", "", "### clinic_cures_2024-25.xlsx", "",
         "1. Confirmed cures among courses that ended in each half-year, whole counts:"]
    for c in P.CLINICS:
        nm = P.CLINIC_NAME[c]
        L.append("   - %s: %s %d; %s %d" % (nm[0].upper() + nm[1:], HALF["H1"], F["cures"]["%s_H1" % c], HALF["H2"],
                                            F["cures"]["%s_H2" % c]))
    open(path, "w").write("\n".join(L) + "\n")
