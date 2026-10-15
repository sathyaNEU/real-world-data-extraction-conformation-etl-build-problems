"""Write task455/submission.md from generator/figures.json: the five blocks, every figure emitted, none typed."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
CERT = "ori_phase_one_outcome_certification_2026.pdf"
WORKBOOK = "ori_outcome_measures_2019_2026.xlsx"
DEATHS = "wendmoor_death_records_2019_2026.csv"
REVIEW = "ome_drug_death_review_2025.xlsx"
RECEIPTS = "interstate_exchange_receipts_2019_2027.csv"
STATUS = "vital_records_data_year_status.csv"
EMS = "ems_patient_care_reports_2021_2026.csv"
AGREEMENT = "ori_grant_agreement_2024.pdf"


def main():
    f = json.load(open(os.path.join(HERE, "figures.json")))
    b, r, y = f["bridge"], f["review"], f["baseline_years"]
    L = []
    L += ["## Tags", "", "**Domain:** Survey Research & Official Statistics (census, register and administrative data quality).",
          "**Analytical objective:** Data Extraction & Conformation (ETL).", ""]
    L += ["## 1. Final Recommendation", "",
          "**The trustees should release phase two of the Overdose Reduction Initiative: Wendmoor County residents' opioid "
          "overdose deaths in 2026 were %.1f per cent below their 2021 to 2023 average.**" % f["change_pct"], "",
          "The 2026 outcome is %d deaths against a baseline of %d a year, past the %d per cent Schedule B5 requires. Not the "
          "certificates as filed, which fell %.1f per cent because the coroner lists fentanyl that played no part in stimulant "
          "deaths. Not the two-by-two correction with one false-listing rate over all non-opioid deaths, which files %.1f per "
          "cent because that rate moves with the stimulant deaths' growing share." % (
              f["outcome_2026"], f["baseline"], f["threshold_pct"], f["certified_change_pct"], f["rogan_gladen_change_pct"]), ""]
    L += ["## 2. Critical Components", "",
          "1. The 2026 outcome is **%d** residents' deaths an opioid caused or contributed to." % f["outcome_2026"],
          "2. The 2021 to 2023 baseline is **%d** a year (**%d**, **%d** and **%d**)." % (f["baseline"], y["2021"], y["2022"], y["2023"]),
          "3. 2026 is **%.1f per cent** below the baseline." % f["change_pct"],
          "4. The certificates name an opioid on **%.3f** of the deaths an opioid caused and on **%.1f** of the stimulant deaths, none "
          "of the other drug deaths." % (r["sensitivity"], r["stimulant_listed_with_opioid"]), ""]
    L += ["## 3. Step-by-Step Solution", "",
          "1. Read %s as it stands at the extract (each state file number's latest version, voids dropped) for residents of "
          "Wendmoor County wherever they died whose underlying cause is a drug poisoning (Schedule B1 in %s): %d, %d, %d and %d "
          "deaths certified with an opioid in 2021, 2022, 2023 and 2026." % (DEATHS, AGREEMENT, b["2021"]["certified"],
                                                                              b["2022"]["certified"], b["2023"]["certified"], b["2026"]["certified"]),
          "2. Joined %s to the 2025 deaths by state file number and classed each by the drugs it found contributing: %d opioid, %d "
          "stimulant without an opioid, %d other." % (REVIEW, r["opioid"], r["stimulant"], r["other"]),
          "3. Measured each class's certificate categories: an opioid named on %d of %d opioid deaths, on %d of %d stimulant deaths "
          "(fentanyl present, not contributing) and on none of the %d other drug deaths." % (
              r["opioid_certified_with_opioid"], r["opioid"], r["stimulant_certified_with_opioid"], r["stimulant"], r["other"]),
          "4. Solved each year's opioid, stimulant and other deaths from its three certificate categories (an opioid named; a "
          "stimulant without an opioid; neither) through those rates (Schedule B3): %d, %d, %d and %d opioid deaths." % (
              b["2021"]["outcome"], b["2022"]["outcome"], b["2023"]["outcome"], b["2026"]["outcome"]),
          "5. Averaged 2021 to 2023 (Schedule B2) and compared 2026: %d against %d, %.1f per cent below." % (
              f["outcome_2026"], f["baseline"], f["change_pct"]),
          "6. Applied Schedule B5: at least %d per cent below the baseline, so phase two is released." % f["threshold_pct"],
          "7. Rebuilt each year's file at its close from the versions in %s, the out-of-state versions on the day %s shows "
          "them received (close dates from %s), and split each year's deaths on the file now into those already among them "
          "at the close and those that joined since, a death received through the exchange counted once by its sending "
          "state's certificate number." % (DEATHS, RECEIPTS, STATUS),
          "8. Grouped %s into patient encounters (each report that does not hand the patient on, with the reports that hand "
          "the patient to its unit) and counted those with naloxone or an opioid poisoning code (sixth character 1 to 4) on "
          "any report, a Wendmoor home county and no death (Schedule B6)." % EMS, ""]
    L += ["## 4. Deliverable Answers", "", "### %s" % CERT, "",
          "1. Phase two is released under Schedule B5.",
          "2. 2026 outcome %d; 2021 to 2023 baseline %d; %.1f per cent below." % (f["outcome_2026"], f["baseline"], f["change_pct"]),
          "3. Bridge, deaths certified with an opioid, plus opioid deaths certified without one, less deaths certified with an "
          "opioid that no opioid caused, equals the outcome:"]
    for yr in ("2021", "2022", "2023", "2026"):
        x = b[yr]
        L.append("   - %s: %d, plus %d, less %d, equals %d" % (yr, x["certified"], x["missed"], x["false"], x["outcome"]))
    L += ["", "### %s" % WORKBOOK, "",
          "1. Residents' drug overdose deaths on the state's file now, by whether they were among them the day it closed:"]
    for yr in sorted(f["after_close"]):
        a = f["after_close"][yr]
        L.append("   - %s: %d among them at the close, %d joined since" % (yr, a["among"], a["joined"]))
    L.append("2. Non-fatal opioid overdoses of residents treated by EMS, by quarter:")
    for q, n in f["ems"].items():
        L.append("   - %s %s: %d" % (q[:4], q[4:], n))
    L.append("")
    open(os.path.join(TASK, "submission.md"), "w").write("\n".join(L))


if __name__ == "__main__":
    main()
